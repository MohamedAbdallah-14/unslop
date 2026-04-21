"""Core humanization logic: deterministic regex pass and LLM-driven rewrite.

Contract:
  - Read file at `path`.
  - Write `<stem>.original.md` backup.
  - Humanize prose. Preserve fenced code, inline code, URLs, paths, headings.
  - Validate. On failure: targeted fix (LLM mode only) up to 2 retries.
  - On final success: overwrite original. On final failure: restore original.

Intensity levels:
  - subtle   — stock vocab only. Keep structure and rhythm mostly intact.
  - balanced — default. Adds sycophancy, hedging, transition tics, em-dash cap,
               performative balance, authority tropes, signposting.
  - full     — balanced plus filler phrases, negative parallelisms, and an
               LLM pass when available.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .structural import StructuralReport, humanize_structural
from .validate import ValidationResult, validate

MAX_RETRIES = 2

Intensity = Literal["subtle", "balanced", "full"]
VALID_INTENSITIES: tuple[Intensity, ...] = ("subtle", "balanced", "full")


@dataclass
class Replacement:
    """One deterministic edit made by `humanize_deterministic_with_report`.

    `rule` is the category (e.g. `sycophancy`, `stock_vocab`, `authority_trope`);
    `pattern` is the human-readable summary of the regex that matched; `before`
    and `after` are the matched text and its replacement. Offsets refer to
    positions in the protected text (code blocks replaced with placeholders)
    so they're mainly useful for an audit trail, not for re-applying to raw
    text."""

    rule: str
    pattern: str
    before: str
    after: str


@dataclass
class HumanizeReport:
    """Summary of a deterministic humanization pass.

    Returned by `humanize_deterministic_with_report`. The CLI uses this for
    `--report` and `--json` output."""

    intensity: Intensity
    replacements: list[Replacement] = field(default_factory=list)
    em_dashes_before: int = 0
    em_dashes_after: int = 0
    structural: StructuralReport = field(default_factory=StructuralReport)

    @property
    def counts_by_rule(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.replacements:
            counts[r.rule] = counts.get(r.rule, 0) + 1
        return counts

    def to_dict(self) -> dict:
        """JSON-serializable shape. Used by the CLI's --json and --report modes."""
        return {
            "intensity": self.intensity,
            "replacements": [
                {
                    "rule": r.rule,
                    "pattern": r.pattern,
                    "before": r.before,
                    "after": r.after,
                }
                for r in self.replacements
            ],
            "counts_by_rule": self.counts_by_rule,
            "em_dashes_before": self.em_dashes_before,
            "em_dashes_after": self.em_dashes_after,
            "structural": self.structural.to_dict(),
        }


# ---------- Code block protection ----------

FENCED_CODE_BLOCK = re.compile(r"^```[^\n]*\n[\s\S]*?^```\s*$", re.MULTILINE)
INDENTED_CODE_BLOCK = re.compile(
    r"(?m)(?:^(?: {4}|\t)[^\n]+(?:\n(?: {4}|\t)[^\n]+)*)"
)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL_PATTERN = re.compile(r"https?://[^\s)>\]]+")
HEADING_LINE = re.compile(r"^#{1,6}[ \t]+[^\n]+", re.MULTILINE)
MD_LINK = re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")
# YAML frontmatter at file start: "---\n...\n---" with the closing fence on its
# own line. The regex intentionally stops AT the closing fence and does not
# consume the newline after it, so the body below still begins at a line start
# for other regexes (e.g. line-start sycophancy openers).
YAML_FRONTMATTER = re.compile(r"\A---\n[\s\S]*?\n---(?=\n|\Z)")
# Blockquotes: contiguous block of lines starting with ">". Usually quoted examples.
BLOCKQUOTE_BLOCK = re.compile(
    r"(?m)(?:^[ \t]*>[^\n]*(?:\n[ \t]*>[^\n]*)*)"
)
# GitHub-flavored markdown table row: line contains at least one inner pipe and
# starts/ends with "|" (after optional whitespace). Table separator rows (---|---)
# and content rows are both captured. Matches contiguous table blocks.
TABLE_BLOCK = re.compile(
    r"(?m)(?:^[ \t]*\|[^\n]*\|[ \t]*(?:\n[ \t]*\|[^\n]*\|[ \t]*)+)"
)
# Quoted examples: `"delve"`, `"It's important to note that"`, `"Great question!"`.
# Rationale: when a word or phrase appears in quotes, the author is discussing
# it or reporting it, not using it (use/mention distinction). A unslop that
# strips "Great question!" from `The opener "Great question!" is a tell.` has
# destroyed the sentence's point. We match straight (") and curly (“”) quotes,
# single line only, bounded at 160 chars so we don't accidentally swallow an
# entire paragraph across two opening/closing quote marks that the author
# mismatched. Placed last in _protect so inline code and markdown links inside
# the quoted span are already placeholder-swapped before we see them.
QUOTED_PROSE = re.compile(
    r'(?:"[^"\n]{1,160}"|\u201c[^\u201d\n]{1,160}\u201d)'
)


def _placeholder(idx: int, kind: str) -> str:
    return f"\x00{kind}#{idx}\x00"


def _protect(text: str) -> tuple[str, dict[str, str]]:
    """Replace anything we promise to preserve with opaque placeholders.

    Covered: YAML frontmatter, fenced code, indented code, blockquotes, markdown
    tables, headings (whole line), markdown links, inline code, bare URLs.

    Order matters: the largest / most specific pattern runs first so nested
    matches (e.g. inline code inside a table row) don't double-protect or leak
    through. Fenced code is first because it can contain every other pattern.
    YAML frontmatter can only appear at file start, so it's placeholder-swapped
    before anything else that might match its interior.

    Blockquotes and tables are protected because they're the two forms of
    "illustrative prose" markdown has: the reader expects them to remain
    verbatim (quoted examples, glossary rows, reference tables). Rewriting them
    destroys the doc's meaning."""
    table: dict[str, str] = {}

    def make_sub(kind: str):
        def sub(m: re.Match) -> str:
            ph = _placeholder(len(table), kind)
            table[ph] = m.group(0)
            return ph

        return sub

    text = YAML_FRONTMATTER.sub(make_sub("YAML"), text)
    text = FENCED_CODE_BLOCK.sub(make_sub("FENCE"), text)
    text = INDENTED_CODE_BLOCK.sub(make_sub("INDENT"), text)
    text = TABLE_BLOCK.sub(make_sub("TABLE"), text)
    text = BLOCKQUOTE_BLOCK.sub(make_sub("QUOTE"), text)
    text = HEADING_LINE.sub(make_sub("HEAD"), text)
    text = MD_LINK.sub(make_sub("LINK"), text)
    text = INLINE_CODE.sub(make_sub("INLINE"), text)
    text = URL_PATTERN.sub(make_sub("URL"), text)
    # Quoted examples go last: they sit inside prose and must not shadow code /
    # links / tables above. See QUOTED_PROSE doc for use/mention rationale.
    text = QUOTED_PROSE.sub(make_sub("QUOTED"), text)

    return text, table


def _restore(text: str, table: dict[str, str]) -> str:
    for ph, original in table.items():
        text = text.replace(ph, original)
    return text


# ---------- Deterministic rules ----------

# Sycophancy openers — strip whole opener at start of any line. Trailing whitespace
# is consumed so the next sentence flows naturally. Looped until stable so multiple
# stacked openers (e.g. "Great question! I'd be happy to help.") all get stripped.
SYCOPHANCY = [
    re.compile(r"^[ \t]*(?:Great|Excellent|Wonderful|Fantastic|Awesome) question[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*(?:Certainly|Absolutely|Sure)[!.,][ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"(?<=[.!?]\s)(?:Certainly|Absolutely|Sure)[!.,][ \t]*", re.IGNORECASE),
    re.compile(r"^[ \t]*I(?:'m| am) happy to help[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*I(?:'d| would) be happy to help[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"(?<=[.!?]\s)I(?:'d| would) be happy to help[^.!\n]*[.!]?[ \t]*", re.IGNORECASE),
    re.compile(r"^[ \t]*What a (?:fascinating|wonderful|great|terrific)[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*I hope this (?:email|message) finds you well[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"(?<=[.!?]\s)I hope this (?:email|message) finds you well[.!]?[ \t]*", re.IGNORECASE),
    re.compile(r"^[ \t]*Thank you for (?:your |the )?(?:question|asking)[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
]

# Hedging stack openers — strip the opener AND the optional trailing ", " so the
# remaining sentence reads naturally.
HEDGING_OPENERS = [
    re.compile(r"\bIt(?:'s| is) (?:also )?important to note that[,]?[ \t]*", re.IGNORECASE),
    re.compile(r"\bIt(?:'s| is) (?:also )?worth (?:mentioning|noting|pointing out) that[,]?[ \t]*", re.IGNORECASE),
    re.compile(r"\bIt should be noted that[,]?[ \t]*", re.IGNORECASE),
    re.compile(r"\bIt(?:'s| is) a (?:well-known|well known) fact that[,]?[ \t]*", re.IGNORECASE),
    re.compile(r"\bNeedless to say[,]?[ \t]+", re.IGNORECASE),
    re.compile(r"\bGenerally speaking[,]?[ \t]+", re.IGNORECASE),
    re.compile(r"\bIn essence[,]?[ \t]+", re.IGNORECASE),
    re.compile(r"\bAt its core[,]?[ \t]+", re.IGNORECASE),
]

# Transitional AI tics. "Furthermore", "Moreover", "Additionally" at sentence start
# is the canonical AI-essay glue. Research category 01 (prompt engineering) and 04
# (language quality) both flag it. Strip at line-start or after ". " punctuation.
# Do NOT strip mid-sentence, where they sometimes appear legitimately.
TRANSITION_TICS = [
    re.compile(r"(^|(?<=[.!?]\s))(?:Furthermore|Moreover|Additionally)[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)(?:Furthermore|Moreover|Additionally)[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))In conclusion[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)In conclusion[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))To summarize[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)To summarize[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))(?:Firstly|Secondly|Thirdly|Finally)[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)(?:Firstly|Secondly|Thirdly|Finally)[,]?[ \t]+", re.MULTILINE),
]

# Stock vocab → plain replacement. Keep the noun-context guard on `navigate`/`journey`
# so we don't replace literal navigation or actual journeys.
#
# New additions (2026-04 audit vs blader/unslop #7–#12 and
# Wikipedia:Signs_of_AI_writing): `interplay`, `intricate`, `vibrant`,
# `underscore(s)` in the figurative-verb sense, `crucial`, `vital`,
# `ever-evolving`, `ever-changing`, `in today's (digital) world`,
# `in today's (digital) age`, and `dynamic landscape` as a compound.
# Each change has a corresponding entry in validate.py's AI_ISMS so the
# validator refuses to let the count grow.
STOCK_VOCAB = [
    (re.compile(r"\bdelving into\b", re.IGNORECASE), "looking at"),
    (re.compile(r"\bdelves into\b", re.IGNORECASE), "looks at"),
    (re.compile(r"\bdelved into\b", re.IGNORECASE), "looked at"),
    (re.compile(r"\bdelve into\b", re.IGNORECASE), "look at"),
    (re.compile(r"\bdelving\b", re.IGNORECASE), "looking at"),
    (re.compile(r"\bdelves\b", re.IGNORECASE), "looks at"),
    (re.compile(r"\bdelved\b", re.IGNORECASE), "looked at"),
    (re.compile(r"\bdelve\b", re.IGNORECASE), "look at"),
    (re.compile(r"\btapestry\b", re.IGNORECASE), "blend"),
    (re.compile(r"\bhas\s+been\s+(?:a|the)\s+testament\s+to\b", re.IGNORECASE), "shows"),
    (re.compile(r"\bhave\s+been\s+(?:a|the)\s+testament\s+to\b", re.IGNORECASE), "show"),
    (re.compile(r"\b(?:is|was)\s+(?:a|the)\s+testament\s+to\b", re.IGNORECASE), "shows"),
    (re.compile(r"\b(?:are|were)\s+(?:a|the)\s+testament\s+to\b", re.IGNORECASE), "show"),
    (re.compile(r"\b\w+(?:es|s|ed)\s+(?:a|the)\s+testament\s+to\b", re.IGNORECASE), r"shows"),
    (re.compile(r"\b(?:a|the)\s+testament\s+to\b", re.IGNORECASE), r"shows"),
    (re.compile(r"\btestament to\b", re.IGNORECASE), "shows"),
    (re.compile(r"\bnavigating\s+through\b", re.IGNORECASE), "working through"),
    (re.compile(r"\bnavigated\s+through\b", re.IGNORECASE), "worked through"),
    (re.compile(r"\bnavigates\s+through\b", re.IGNORECASE), "works through"),
    (re.compile(r"\bnavigate\s+through\b", re.IGNORECASE), "work through"),
    (re.compile(r"\bnavigating(?=\s+(?:the|around|these|this|that|our|complex))\b", re.IGNORECASE), "working through"),
    (re.compile(r"\bnavigated(?=\s+(?:the|around|these|this|that|our|complex))\b", re.IGNORECASE), "worked through"),
    (re.compile(r"\bnavigates(?=\s+(?:the|around|these|this|that|our|complex))\b", re.IGNORECASE), "works through"),
    (re.compile(r"\bnavigate(?=\s+(?:the|around|these|this|that|our|complex))\b", re.IGNORECASE), "work through"),
    (re.compile(r"\bembarking on (?:a |the )?journey of (\w+)ing\b", re.IGNORECASE),
     lambda m: "starting to " + m.group(1).lower()),
    (re.compile(r"\bembark(?:ed|s)? on (?:a |the )?journey of (\w+)ing\b", re.IGNORECASE),
     lambda m: "start " + m.group(1).lower() + "ing"),
    (re.compile(r"\bembarking on (?:a |the )?journey to ", re.IGNORECASE), "starting to "),
    (re.compile(r"\bembark(?:ed|s)? on (?:a |the )?journey to ", re.IGNORECASE), "start to "),
    (re.compile(r"\bembarking on\b", re.IGNORECASE), "starting"),
    (re.compile(r"\bembarks on\b", re.IGNORECASE), "starts"),
    (re.compile(r"\bembarked on\b", re.IGNORECASE), "started"),
    (re.compile(r"\bembark on\b", re.IGNORECASE), "start"),
    (re.compile(r"\bjourney(?=\s+(?:toward|to|of))\b", re.IGNORECASE), "path"),
    (re.compile(r"\brealm of\b", re.IGNORECASE), "world of"),
    (re.compile(r"\blandscape of\b", re.IGNORECASE), "world of"),
    (re.compile(r"\bpivotal\b", re.IGNORECASE), "key"),
    (re.compile(r"\bparamount\b", re.IGNORECASE), "essential"),
    (re.compile(r"\bseamlessly\b", re.IGNORECASE), "smoothly"),
    (re.compile(r"\bseamless\b", re.IGNORECASE), "smooth"),
    (re.compile(r"\bholistically\b", re.IGNORECASE), "as a whole"),
    (re.compile(r"\bholistic\b", re.IGNORECASE), "overall"),
    (re.compile(r"\bleverages\b", re.IGNORECASE), "uses"),
    (re.compile(r"\bleveraged\b", re.IGNORECASE), "used"),
    (re.compile(r"\bleveraging\b", re.IGNORECASE), "using"),
    (re.compile(r"\bleverage\b", re.IGNORECASE), "use"),
    (re.compile(r"\bcutting-edge\b", re.IGNORECASE), "advanced"),
    (re.compile(r"\ba state-of-the-art\b", re.IGNORECASE), "the latest"),
    (re.compile(r"\bstate-of-the-art\b", re.IGNORECASE), "latest"),
    (re.compile(r"\bcomprehensively\b", re.IGNORECASE), "thoroughly"),
    (re.compile(r"\bcomprehensive\b", re.IGNORECASE), "broad"),
    (re.compile(r"\brobust(?=\s+(?:and|solution|implementation|approach|system|architecture|framework|platform|infrastructure|backend|frontend|foundation|delivery|automation|CI/CD|pipeline|tooling|mechanism|strategy))\b", re.IGNORECASE), "reliable"),
    # Expanded vocabulary (blader/unslop + Wikipedia:Signs_of_AI_writing).
    (re.compile(r"\binterplay\s+(?:between|of)\b", re.IGNORECASE), "link between"),
    (re.compile(r"\bintricate\b", re.IGNORECASE), "detailed"),
    (re.compile(r"\bvibrant\b", re.IGNORECASE), "lively"),
    # `underscore(s)` as a figurative verb — guard so literal underscore chars
    # (in code, in variable_name discussions) pass through. We only match it in
    # verb position with a following noun phrase article.
    (re.compile(r"\bunderscores\s+(?=(?:the|our|a|an|its|their|this|that|how|why)\b)", re.IGNORECASE), "shows "),
    (re.compile(r"\bunderscored\s+(?=(?:the|our|a|an|its|their|this|that|how|why)\b)", re.IGNORECASE), "showed "),
    (re.compile(r"\bunderscoring\s+(?=(?:the|our|a|an|its|their|this|that|how|why)\b)", re.IGNORECASE), "showing "),
    (re.compile(r"\bunderscore\s+(?=(?:the|our|a|an|its|their|this|that|how|why)\b)", re.IGNORECASE), "show "),
    (re.compile(r"\bcrucial\b", re.IGNORECASE), "important"),
    (re.compile(r"\bvital(?=\s+(?:role|importance|part|component|aspect))\b", re.IGNORECASE), "important"),
    (re.compile(r"\bever[- ]evolving\b", re.IGNORECASE), "changing"),
    (re.compile(r"\bever[- ]changing\b", re.IGNORECASE), "changing"),
    (re.compile(r"\bin today'?s (?:digital )?(?:world|age|landscape|era)\b", re.IGNORECASE), "today"),
    (re.compile(r"\bdynamic landscape\b", re.IGNORECASE), "world"),
]

# Authority tropes (blader/unslop #27). Persuasive framing that signals
# AI-voice when stacked, but a bare "at its core" sometimes appears in genuine
# writing. We strip these only when they appear at sentence start (same
# position as the existing transition tics), where the tell is strongest.
AUTHORITY_TROPES = [
    re.compile(r"(^|(?<=[.!?]\s))At its core[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)At its core[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))In reality[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)In reality[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))What really matters is that[,]?[ \t]+", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))What really matters is[,]?[ \t]+", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))Fundamentally[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)Fundamentally[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))The heart of the matter is that[,]?[ \t]+", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))At the heart of [^.!?\n]+? (?:is|lies)[,]?[ \t]+", re.MULTILINE | re.IGNORECASE),
]

# Signposting announcements (blader/unslop #28). Meta-commentary that
# announces the writing rather than doing the writing. Strip whole sentence
# where possible; at sentence start, strip the lead-in and let the next clause
# carry the content.
SIGNPOSTING = [
    re.compile(r"(^|(?<=[.!?]\s))Let(?:'s| us) dive in(?:to [^.!?\n]+)?[.!]?[ \t]*", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))Let(?:'s| us) (?:break|walk) (?:this|it) down[.!]?[ \t]*", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))Here'?s what you need to know[:.!]?[ \t]*", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))Without further ado[,]?[ \t]*", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))In this (?:article|post|guide|section|piece|write-up), (?:I|we)(?:'ll| will) [^.!?\n]+?[.!][ \t]*", re.MULTILINE | re.IGNORECASE),
    re.compile(r"(^|(?<=[.!?]\s))Buckle up[.!]?[ \t]*", re.MULTILINE | re.IGNORECASE),
]

# Filler phrases (blader/unslop #23). Wordy constructions that collapse to
# one or two words with no loss of meaning. Applied only at `full` intensity:
# `due to the fact that` is occasionally justified in legal/technical text.
FILLER_PHRASES = [
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
    (re.compile(r"\bin spite of the fact that\b", re.IGNORECASE), "although"),
    (re.compile(r"\ba (?:wide )?(?:variety|range) of\b", re.IGNORECASE), "many"),
    (re.compile(r"\ba (?:significant|substantial) (?:amount|number) of\b", re.IGNORECASE), "many"),
    (re.compile(r"\bat (?:the|this) (?:point|moment) in time\b", re.IGNORECASE), "now"),
    (re.compile(r"\bfor (?:the|all) intents and purposes\b", re.IGNORECASE), "effectively"),
    (re.compile(r"\bin the event that\b", re.IGNORECASE), "if"),
    (re.compile(r"\bwith (?:regard|regards|respect) to\b", re.IGNORECASE), "about"),
    (re.compile(r"\bprior to\b", re.IGNORECASE), "before"),
    (re.compile(r"\bsubsequent to\b", re.IGNORECASE), "after"),
    (re.compile(r"\bthe fact that\b", re.IGNORECASE), "that"),
]

# Negative parallelisms + trailing negations (blader/unslop #10). Applied at
# `full` only. Example: "No guesswork. No bloated frameworks." — each clause
# flags as AI on its own but the stack is the real tell. We strip the
# standalone sentence form "No <noun>." that appears at paragraph end as a
# rhetorical punch. Conservative: only when the clause has no verb.
NEGATIVE_PARALLELISM = [
    # "No guesswork, no bloat, no surprises." — three-clause tricolon of negations
    re.compile(
        r"(^|(?<=[.!?]\s))No [A-Za-z][A-Za-z -]{1,20}(?:, no [A-Za-z][A-Za-z -]{1,20}){2,}[.!]",
        re.MULTILINE,
    ),
]

# Performative balance: collapse mid-sentence ", however," to ". " (sentence break),
# and strip "However, " at the start of any sentence (line OR after period+space).
PERFORMATIVE = [
    (re.compile(r",\s*however,\s*", re.IGNORECASE), ". "),
    (re.compile(r"(^|(?<=[.!?]\s))However,\s+", re.MULTILINE), r"\1"),
]

# --- Phase 2 new lexical families (2026-04-21) ---
#
# Source: blader/humanizer taxonomy (MIT) + Wikipedia "Signs of AI writing"
# maintained by WikiProject AI Cleanup. Each family mirrors a category named in
# that taxonomy that unslop previously did not cover. Credit due to those
# sources; original regex implementations here.
#
# Conservative stance: each pattern needs a clear semantic bound so we never
# destroy meaning. Where a pattern is borderline, we only flag in the validator
# and leave rewrite to LLM mode.

# SIGNIFICANCE_INFLATION: phrases that inflate historical importance without
# evidence. The Wikipedia article names this the single most common AI-writing
# tell on encyclopedic content. Strip the inflated framing; leave the fact.
SIGNIFICANCE_INFLATION = [
    # "marks a pivotal moment in" / "represents a defining moment in" → "happened in"
    (
        re.compile(
            r"\b(?:marks?|represents?|stands?\s+as)\s+"
            r"(?:a|an|the)\s+(?:pivotal|defining|critical|key|watershed|seminal)\s+"
            r"(?:moment|turning\s+point|milestone|chapter)\s+(?:in|for)\s+",
            re.IGNORECASE,
        ),
        "happened in ",
    ),
    # "underscores its importance" / "emphasizes the significance of X" →
    # strip the inflation; the remaining noun stands on its own.
    (
        re.compile(
            r",?\s+(?:underscor(?:es|ing)|emphasiz(?:es|ing)|highlight(?:s|ing))\s+"
            r"(?:the|its|their|his|her)\s+"
            r"(?:importance|significance|role|impact|value|relevance|necessity)"
            r"(?=[,.\s])",
            re.IGNORECASE,
        ),
        "",
    ),
    # "an enduring legacy" / "lasting legacy" → "a legacy"
    (
        re.compile(r"\b(?:an\s+)?(?:enduring|lasting|indelible)\s+legacy\b", re.IGNORECASE),
        "a legacy",
    ),
    # "leaves an indelible mark on" → "affects"
    (
        re.compile(r"\bleaves?\s+an?\s+indelible\s+mark\s+on\b", re.IGNORECASE),
        "affects",
    ),
    # "deeply rooted in" → "rooted in"
    (re.compile(r"\bdeeply\s+rooted\s+in\b", re.IGNORECASE), "rooted in"),
    # "contributing to the broader" / "shaping the broader narrative" —
    # paragraph-inflation clauses. Strip the trailing fragment.
    (
        re.compile(
            r",?\s+(?:contributing\s+to|shaping|influencing)\s+"
            r"the\s+(?:broader|wider|ongoing)\s+"
            r"(?:narrative|landscape|conversation|discourse|trajectory|movement)"
            r"(?=[,.\s])",
            re.IGNORECASE,
        ),
        "",
    ),
]

# NOTABILITY_NAMEDROPPING: "cited in <list of outlets>", "leading expert",
# "active social media presence". Classic encyclopedic puffery. Conservative:
# only the formulaic phrases, not any mention of a source.
NOTABILITY_NAMEDROPPING = [
    # "maintains an active social media presence" → removed (adds nothing)
    (
        re.compile(
            r"\b(?:maintains?|has)\s+an\s+active\s+"
            r"(?:social\s+media\s+)?presence\b"
            r"(?:\s+on\s+[A-Z][A-Za-z]+(?:\s+and\s+[A-Z][A-Za-z]+)?)?",
            re.IGNORECASE,
        ),
        "is active online",
    ),
    # "a leading expert in X" / "a leading voice on X" → "an expert on X"
    (
        re.compile(
            r"\ba\s+leading\s+(?:expert|voice|authority|figure)\s+(?:in|on)\b",
            re.IGNORECASE,
        ),
        "an expert on",
    ),
    # "renowned for his/her/their work on X" → "known for work on X"
    (
        re.compile(
            r"\brenowned\s+for\s+(?:his|her|their)\s+work\s+(?:on|in|with)\b",
            re.IGNORECASE,
        ),
        "known for work on",
    ),
    # "has been widely cited in" → "has appeared in"
    (
        re.compile(
            r"\b(?:has\s+been\s+)?widely\s+(?:cited|featured|covered)\s+(?:in|by)\b",
            re.IGNORECASE,
        ),
        "has appeared in",
    ),
    # "recognized globally as" / "internationally recognized as" → "known as"
    (
        re.compile(
            r"\b(?:internationally|globally)\s+recogni[sz]ed\s+as\b", re.IGNORECASE
        ),
        "known as",
    ),
]

# SUPERFICIAL_ING: trailing participle clauses that claim analysis without
# adding content. Wikipedia: "Superficial -ing analyses." Very conservative:
# only strip when the participle phrase is clearly filler (, VERBing the/its
# importance/significance/role/impact/need), i.e. the tail adds no new concrete
# information. Any tail containing a specific noun is left alone.
SUPERFICIAL_ING = [
    (
        re.compile(
            r",\s+(?:highlighting|underscoring|emphasizing|illustrating|"
            r"reflecting|showcasing|demonstrating|revealing)\s+"
            r"(?:the|its|their|his|her|a|an)\s+"
            r"(?:importance|significance|role|impact|value|need|necessity|"
            r"relevance|nature|essence|complexity|depth|breadth)"
            r"(?:\s+of\s+(?:the|this|that|these|those|its|their|his|her))?"
            r"(?=[.!?\n])",
            re.IGNORECASE,
        ),
        "",
    ),
]

# COPULA_AVOIDANCE: Latinate appositive ", being a/an/the X," used where simple
# "is" would do. Wikipedia lists this as a sign of AI-generated prose trying
# to sound formal. Only the appositive comma-bound form; bare "being" (gerund)
# is untouched.
COPULA_AVOIDANCE = [
    # ", being a reliable platform," → ", a reliable platform,"
    # Drop the "being" word; the remaining appositive is idiomatic English.
    (
        re.compile(
            r",\s+being\s+(?=(?:a|an|the)\s+[a-z])", re.IGNORECASE
        ),
        ", ",
    ),
]

# Em-dash per-paragraph cap. Research (Cat 04, Cat 05) says em-dash pileups are a
# top stylometric tell. Skill contract: no more than two em-dashes per paragraph.
# We implement this in code (`_cap_em_dashes_per_paragraph`) rather than regex,
# since regex can't count across paragraph boundaries reliably.
#
# Tricolon padding is intentionally NOT handled deterministically. A regex that
# collapses "X, Y, and Z" to "X and Y" would destroy legitimate enumerations
# ("red, white, and blue"). Tricolon tightening is a judgment call and stays
# in LLM mode only.


_LIST_MARKER = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]")


def _cap_in_block(block: str, max_dashes: int) -> str:
    count = 0
    buf: list[str] = []
    chars = list(block)
    i = 0
    while i < len(chars):
        if chars[i] == "—":
            count += 1
            if count <= max_dashes:
                buf.append("—")
            else:
                # Replace " — " with ", " to avoid ugly " , " spacing.
                if buf and buf[-1] == " ":
                    buf.pop()
                buf.append(",")
                if i + 1 < len(chars) and chars[i + 1] == " ":
                    buf.append(" ")
                    i += 1
                else:
                    buf.append(" ")
        else:
            buf.append(chars[i])
        i += 1
    return "".join(buf)


def _cap_em_dashes_per_paragraph(text: str, max_dashes: int = 2) -> str:
    """Cap em-dashes per paragraph, with a per-item carve-out for lists.

    Research basis: Cat 04 / Cat 05 name em-dash pileups as a top stylometric
    tell; the skill contract caps them at 2 per paragraph. But a list is not
    one paragraph for rhythm purposes — each bullet has its own voice. And
    lists in the wild frequently have an intro line ("Exports:"), so we can't
    require the whole paragraph to be list-only.

    Rule:
    - Paragraphs are separated by blank lines.
    - Inside a paragraph, every line that starts with a list marker opens a new
      chunk; continuation lines and leading non-list prose attach to the current
      chunk. Each chunk gets its own em-dash budget.
    - A paragraph with zero list markers is one chunk, budget = max_dashes."""
    paragraphs = text.split("\n\n")
    for i, para in enumerate(paragraphs):
        lines = para.split("\n")

        # Any list markers at all? If not, treat the whole paragraph as one chunk.
        has_list = any(_LIST_MARKER.match(line) for line in lines)
        if not has_list:
            paragraphs[i] = _cap_in_block(para, max_dashes)
            continue

        chunks: list[list[str]] = []
        current: list[str] = []
        for line in lines:
            if _LIST_MARKER.match(line):
                if current:
                    chunks.append(current)
                current = [line]
            else:
                if current:
                    current.append(line)
                else:
                    # Leading non-list prose becomes the first chunk.
                    current = [line]
        if current:
            chunks.append(current)

        paragraphs[i] = "\n".join(
            _cap_in_block("\n".join(chunk), max_dashes) for chunk in chunks
        )

    return "\n\n".join(paragraphs)


def _tracking_sub(
    pattern: re.Pattern,
    repl,
    text: str,
    *,
    rule: str,
    log: list[Replacement] | None,
) -> str:
    """Like `pattern.sub(repl, text)` but records each replacement when `log`
    is provided. `repl` may be a string or a callable, matching `re.sub`."""
    if log is None:
        return pattern.sub(repl, text)

    def track(match: re.Match) -> str:
        before = match.group(0)
        if callable(repl):
            after = repl(match)
        else:
            try:
                after = match.expand(repl)
            except re.error:
                after = repl
        if before != after:
            log.append(
                Replacement(
                    rule=rule,
                    pattern=pattern.pattern,
                    before=before,
                    after=after,
                )
            )
        return after

    return pattern.sub(track, text)


def humanize_deterministic(
    text: str,
    *,
    intensity: Intensity = "balanced",
    structural: bool = False,
) -> str:
    """Pure regex pass. Preserves code/URLs via placeholders; strips canonical AI-isms.

    `intensity` gates which rule families run:
      - subtle:   stock vocab only.
      - balanced: sycophancy, hedging openers, transition tics, stock vocab,
                  performative balance, authority tropes, signposting,
                  em-dash cap.
      - full:     everything balanced does, plus filler phrases and
                  negative-parallelism knockouts.

    `structural=True` also runs the Phase 1 structural rewriter (sentence-length
    rebalancer + bullet-soup merger). Off by default while the pass bakes;
    flip on after baseline benchmarks prove it doesn't regress preservation.
    """
    result, _report = humanize_deterministic_with_report(
        text, intensity=intensity, structural=structural
    )
    return result


def humanize_deterministic_with_report(
    text: str,
    *,
    intensity: Intensity = "balanced",
    structural: bool = False,
) -> tuple[str, HumanizeReport]:
    """Like `humanize_deterministic` but returns an audit trail of every
    replacement made. Used by the CLI's `--report` and `--json` output."""
    if intensity not in VALID_INTENSITIES:
        raise ValueError(
            f"unknown intensity {intensity!r}; expected one of {VALID_INTENSITIES}"
        )

    report = HumanizeReport(intensity=intensity)
    log = report.replacements
    em_dashes_before = text.count("—")

    protected, table = _protect(text)

    # Sycophancy stacks ("Great question! I'd be happy to help.") need multiple passes
    # because each strip can expose a new line-start pattern. Cap at 5 to avoid
    # pathological loops on adversarial input.
    run_sycophancy = intensity in ("balanced", "full")
    run_hedging = intensity in ("balanced", "full")
    run_transitions = intensity in ("balanced", "full")
    run_performative = intensity in ("balanced", "full")
    run_authority = intensity in ("balanced", "full")
    run_signposting = intensity in ("balanced", "full")
    run_em_dash_cap = intensity in ("balanced", "full")
    run_significance_inflation = intensity in ("balanced", "full")
    run_notability_namedropping = intensity in ("balanced", "full")
    run_copula_avoidance = intensity in ("balanced", "full")
    run_superficial_ing = intensity == "full"
    run_filler = intensity == "full"
    run_negative_parallelism = intensity == "full"

    if run_sycophancy:
        for _ in range(5):
            before = protected
            for pattern in SYCOPHANCY:
                protected = _tracking_sub(pattern, "", protected, rule="sycophancy", log=log)
            if protected == before:
                break

    if run_hedging:
        for pattern in HEDGING_OPENERS:
            protected = _tracking_sub(pattern, "", protected, rule="hedging_opener", log=log)

    if run_transitions:
        for pattern in TRANSITION_TICS:
            protected = _tracking_sub(pattern, r"\1", protected, rule="transition_tic", log=log)

    if run_authority:
        for pattern in AUTHORITY_TROPES:
            protected = _tracking_sub(
                pattern, r"\1", protected, rule="authority_trope", log=log
            )

    if run_signposting:
        for pattern in SIGNPOSTING:
            protected = _tracking_sub(pattern, r"\1", protected, rule="signposting", log=log)

    # Stock vocab runs at every intensity, including `subtle`.
    for pattern, repl in STOCK_VOCAB:
        protected = _tracking_sub(pattern, repl, protected, rule="stock_vocab", log=log)

    if run_significance_inflation:
        for pattern, repl in SIGNIFICANCE_INFLATION:
            protected = _tracking_sub(
                pattern, repl, protected, rule="significance_inflation", log=log
            )

    if run_notability_namedropping:
        for pattern, repl in NOTABILITY_NAMEDROPPING:
            protected = _tracking_sub(
                pattern, repl, protected, rule="notability_namedropping", log=log
            )

    if run_copula_avoidance:
        for pattern, repl in COPULA_AVOIDANCE:
            protected = _tracking_sub(
                pattern, repl, protected, rule="copula_avoidance", log=log
            )

    if run_superficial_ing:
        for pattern, repl in SUPERFICIAL_ING:
            protected = _tracking_sub(
                pattern, repl, protected, rule="superficial_ing", log=log
            )

    if run_filler:
        for pattern, repl in FILLER_PHRASES:
            protected = _tracking_sub(pattern, repl, protected, rule="filler_phrase", log=log)

    if run_negative_parallelism:
        for pattern in NEGATIVE_PARALLELISM:
            protected = _tracking_sub(
                pattern, r"\1", protected, rule="negative_parallelism", log=log
            )

    if run_performative:
        for pattern, repl in PERFORMATIVE:
            protected = _tracking_sub(pattern, repl, protected, rule="performative", log=log)

    # Phase 1 structural pass — sentence-length rebalancer + bullet-soup merger.
    # Runs after lexical scrubbing because the lexical passes remove openers and
    # phrases that would otherwise skew word counts, and before the em-dash cap
    # because splitting a long sentence can move an em-dash into its own clause
    # where it's no longer an offender. Gated off by default — see flag doc.
    if structural:
        protected = humanize_structural(protected, report=report.structural)

    if run_em_dash_cap:
        protected = _cap_em_dashes_per_paragraph(protected, max_dashes=2)

    # Cleanup: strip stranded leading punctuation that openers left behind, e.g.
    # "It's worth mentioning that, generally speaking, you should..." after both
    # openers strip leaves ", you should..." — drop the leading comma+space.
    protected = re.sub(r"^[ \t]*[,;:][ \t]*", "", protected, flags=re.MULTILINE)
    # Likewise after a paragraph break.
    protected = re.sub(r"\n\n[ \t]*[,;:][ \t]*", "\n\n", protected)

    # Capitalize first letter of every sentence/paragraph that openers exposed.
    # Sentence-start = file-start, paragraph break, OR sentence-ending punctuation+space.
    # Guard against common abbreviations (i.e., e.g., etc.) so "i.e. not" doesn't
    # become "i.e. Not". Python's re does not support variable-width lookbehind,
    # so we inspect the prefix inside the replacement callback.
    _SENTENCE_ABBREVS = re.compile(
        r"(?:^|[^a-zA-Z])(?:i\.e|e\.g|etc|vs|cf|viz|et al|Dr|Mr|Mrs|Ms|St|Jr|Sr|No)\Z"
    )

    def capitalize_after_start(m: re.Match) -> str:
        return m.group(1) + m.group(2).upper()

    def capitalize_after_sentence(m: re.Match) -> str:
        start = m.start()
        prefix = m.string[max(0, start - 10):start]
        if _SENTENCE_ABBREVS.search(prefix):
            return m.group(0)
        return m.group(1) + m.group(2).upper()

    protected = re.sub(r"(^|\n\n)([a-z])", capitalize_after_start, protected)
    protected = re.sub(r"([.!?]\s+)([a-z])", capitalize_after_sentence, protected)
    # Capitalize after bullet markers when opener stripping left lowercase.
    protected = re.sub(
        r"(^[ \t]*(?:[-*+]|\d+\.)[ \t]+)([a-z])",
        lambda m: m.group(1) + m.group(2).upper(),
        protected,
        flags=re.MULTILINE,
    )

    # Article agreement: replacements like holistic→overall or state-of-the-art→latest
    # can leave "a overall" or "a advanced" which is ungrammatical. Fix "a" → "an"
    # before words starting with a vowel sound.
    protected = re.sub(
        r"\ba(?= (?:overall|advanced|essential|important|earlier|original|"
        r"open|obvious|interesting|unusual|earlier|underlying|ongoing|optional|"
        r"older|outer|initial|ideal|upper|ultimate|average|alternate|"
        r"effective|efficient|elaborate|elegant|enormous))\b",
        "an",
        protected,
        flags=re.IGNORECASE,
    )

    # Collapse 3+ blank lines to 2 (BUT not 1 → preserve heading/paragraph spacing)
    protected = re.sub(r"\n{3,}", "\n\n", protected)
    # Strip trailing whitespace on each line so we don't ship messy diffs
    protected = re.sub(r"[ \t]+\n", "\n", protected)

    restored = _restore(protected, table)
    report.em_dashes_before = em_dashes_before
    report.em_dashes_after = restored.count("—")
    return restored, report


# ---------- LLM-driven humanization ----------


_INTENSITY_PROMPT_GUIDANCE: dict[str, str] = {
    "subtle": (
        "INTENSITY: subtle. Trim AI tells only. Keep paragraph structure and "
        "sentence count roughly intact. Do not restructure, do not merge bullets, "
        "do not break tricolons unless they are obviously redundant."
    ),
    "balanced": (
        "INTENSITY: balanced (default). Cut slop, vary rhythm, restore voice, "
        "allow contractions and short fragments. Moderate rewrite allowed. Paragraph "
        "order must stay the same; paragraph boundaries may shift."
    ),
    "full": (
        "INTENSITY: full. Strong rewrite. Restructure paragraphs for rhythm. Drop "
        "performative balance. Merge bullet-soup. Collapse filler phrases "
        "(\"in order to\" → \"to\", \"due to the fact that\" → \"because\"). Use "
        "contractions. Sound like a human with a stake."
    ),
}


def _build_humanize_prompt(original: str, intensity: Intensity = "balanced") -> str:
    guidance = _INTENSITY_PROMPT_GUIDANCE.get(intensity, _INTENSITY_PROMPT_GUIDANCE["balanced"])
    return f"""Humanize this markdown so it reads like a careful human wrote it.

{guidance}

STRICT RULES (preservation):
- Do NOT modify anything inside ``` code blocks
- Do NOT modify anything inside inline backticks
- Preserve ALL URLs exactly
- Preserve ALL headings exactly (text and level)
- Preserve file paths and commands
- Preserve technical terms, version numbers, error messages
- Return ONLY the humanized markdown body — do NOT wrap the entire output in a ```markdown fence or any other fence. Inner code blocks from the original stay as-is; do not add a new outer fence around the whole file.

HUMANIZATION RULES (only on natural-language prose between code regions):
- Drop sycophancy openers ("Great question!", "Certainly!", "I'd be happy to help")
- Drop stock vocab (delve, tapestry, testament, navigate, embark, journey, realm, landscape, pivotal, paramount, seamless, holistic, leverage as filler, robust as filler, comprehensive as filler, cutting-edge, state-of-the-art, interplay, intricate, vibrant, underscore [verb], crucial, vital [as filler], ever-evolving/ever-changing, "in today's digital world/age")
- Drop hedging stack openers ("It's important to note that", "It's worth mentioning that", "Generally speaking", "In essence", "At its core")
- Drop authority tropes at sentence start ("At its core", "In reality", "What really matters", "Fundamentally", "The heart of the matter")
- Drop signposting announcements ("Let's dive in", "Let's break this down", "Here's what you need to know", "Without further ado", "Buckle up")
- Drop performative balance — every claim does not need a "however"
- Engineer burstiness — mix short and long sentences deliberately (target a mix of 4–35 word sentences per paragraph)
- Tighten tricolons — "X, Y, and Z" stacks where two would suffice → keep two
- Merge bullet soup — three bullets that say the same thing → one sentence
- Vary paragraph length — no tidy five-paragraph essay shape
- Prefer active voice; avoid subjectless AI fragments ("Works great." by itself — add a subject)

TWO-PASS SELF-AUDIT (required):
1. After your first rewrite, silently ask yourself: "What in the draft above still reads as obviously AI-generated?"
2. Revise in place, then return the revised version only.
Do NOT include the audit in the output. Return the final text directly.

Pattern: [concrete observation]. [why or implication]. [what to do next].

TEXT:
{original}
"""


def _build_fix_prompt(original: str, broken_humanized: str, errors: list[str]) -> str:
    error_list = "\n".join(f"- {e}" for e in errors)
    return f"""Your previous humanization broke structural preservation. Fix it.

ERRORS:
{error_list}

ORIGINAL:
{original}

BROKEN HUMANIZED:
{broken_humanized}

Return ONLY the corrected humanized markdown. Restore every code block, URL, and heading exactly. Keep the humanization improvements that did not break structure.
"""


def _call_anthropic_sdk(prompt: str) -> str | None:
    try:
        from anthropic import Anthropic
    except ImportError:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    client = Anthropic()
    msg = client.messages.create(
        model=os.environ.get("UNSLOP_MODEL", "claude-sonnet-4-5"),
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in msg.content if hasattr(block, "text")).strip()


def _call_claude_cli(prompt: str) -> str | None:
    if shutil.which("claude") is None:
        return None
    proc = subprocess.run(
        ["claude", "--print"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(f"claude CLI returned {proc.returncode}: {proc.stderr.strip()[:200]}\n")
        return None
    return proc.stdout.strip()


def humanize_llm(text: str, *, intensity: Intensity = "balanced") -> str:
    prompt = _build_humanize_prompt(text, intensity=intensity)
    result = _call_anthropic_sdk(prompt) or _call_claude_cli(prompt)
    if result is None:
        raise RuntimeError(
            "LLM mode requires either ANTHROPIC_API_KEY (with `anthropic` package) "
            "or the `claude` CLI on PATH. Use --deterministic for offline use."
        )
    return _strip_outer_fence(result)


def _strip_outer_fence(text: str) -> str:
    """If the LLM wrapped the whole reply in ```markdown ... ```, strip that fence."""
    stripped = text.strip()
    m = re.match(r"^```(?:markdown|md)?\s*\n([\s\S]*?)\n```\s*$", stripped)
    if m:
        return m.group(1)
    return text


def _llm_fix(original: str, broken: str, errors: list[str]) -> str | None:
    prompt = _build_fix_prompt(original, broken, errors)
    result = _call_anthropic_sdk(prompt) or _call_claude_cli(prompt)
    if result is None:
        return None
    return _strip_outer_fence(result)


# ---------- Top-level orchestrator ----------


@dataclass
class HumanizeOutcome:
    """Result of `humanize_file_ex`. Carries enough information for the CLI's
    --json, --diff, and --report modes without duplicating the read/write."""

    ok: bool
    original: str
    humanized: str
    validation: ValidationResult | None = None
    report: HumanizeReport | None = None
    attempts: int = 1
    error: str | None = None


def humanize_file(
    path: Path,
    *,
    deterministic: bool = False,
    intensity: Intensity = "balanced",
    backup: bool = True,
) -> bool:
    """Legacy entry point: read, humanize, write, return success bool."""
    outcome = humanize_file_ex(
        path,
        deterministic=deterministic,
        intensity=intensity,
        backup=backup,
        write=True,
    )
    return outcome.ok


def humanize_file_ex(
    path: Path,
    *,
    deterministic: bool = False,
    intensity: Intensity = "balanced",
    backup: bool = True,
    write: bool = True,
    structural: bool = False,
) -> HumanizeOutcome:
    """Rich entry point. Returns the full outcome (humanized text, report,
    validation) regardless of whether we actually wrote to disk. The CLI uses
    `write=False` for `--dry-run` and `--diff`.

    `structural=True` enables the Phase 1 structural pass (sentence splitting
    and bullet-soup merging). Opt-in until we default it on for `balanced`
    after benchmark validation."""
    original_text = path.read_text(encoding="utf-8")
    backup_path = path.with_name(path.stem + ".original.md")

    if backup and write and backup_path.exists():
        return HumanizeOutcome(
            ok=False,
            original=original_text,
            humanized=original_text,
            error=(
                f"Backup already exists at {backup_path}. "
                "Remove or rename it before re-humanizing."
            ),
        )

    if deterministic:
        humanized, report = humanize_deterministic_with_report(
            original_text, intensity=intensity, structural=structural
        )
        result = validate(original_text, humanized)
        if not result.ok:
            return HumanizeOutcome(
                ok=False,
                original=original_text,
                humanized=humanized,
                validation=result,
                report=report,
                error="Deterministic pass produced a structural change.",
            )
        if write:
            if backup:
                backup_path.write_text(original_text, encoding="utf-8")
            path.write_text(humanized, encoding="utf-8")
        return HumanizeOutcome(
            ok=True,
            original=original_text,
            humanized=humanized,
            validation=result,
            report=report,
        )

    # LLM mode.
    if backup and write:
        backup_path.write_text(original_text, encoding="utf-8")

    try:
        humanized = humanize_llm(original_text, intensity=intensity)
    except RuntimeError as exc:
        if backup and write:
            backup_path.unlink(missing_ok=True)
        return HumanizeOutcome(
            ok=False,
            original=original_text,
            humanized=original_text,
            error=str(exc),
        )

    last_result = None
    for attempt in range(MAX_RETRIES + 1):
        last_result = validate(original_text, humanized)
        if last_result.ok:
            if write:
                path.write_text(humanized, encoding="utf-8")
            return HumanizeOutcome(
                ok=True,
                original=original_text,
                humanized=humanized,
                validation=last_result,
                attempts=attempt + 1,
            )
        if attempt < MAX_RETRIES:
            fixed = _llm_fix(original_text, humanized, last_result.errors)
            if fixed is None:
                break
            humanized = fixed

    if write:
        path.write_text(original_text, encoding="utf-8")
    return HumanizeOutcome(
        ok=False,
        original=original_text,
        humanized=humanized,
        validation=last_result,
        attempts=MAX_RETRIES + 1,
        error="Could not produce a structurally valid humanization.",
    )
