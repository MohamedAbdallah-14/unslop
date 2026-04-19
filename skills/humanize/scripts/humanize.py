"""Core humanization logic: deterministic regex pass and LLM-driven rewrite.

Contract:
  - Read file at `path`.
  - Write `<stem>.original.md` backup.
  - Humanize prose. Preserve fenced code, inline code, URLs, paths, headings.
  - Validate. On failure: targeted fix (LLM mode only) up to 2 retries.
  - On final success: overwrite original. On final failure: restore original.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from .validate import format_report, validate

MAX_RETRIES = 2

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
# it or reporting it, not using it (use/mention distinction). A humanizer that
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
    re.compile(r"^[ \t]*(?:Great|Excellent|Wonderful|Fantastic|Awesome) question[!.]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*(?:Certainly|Absolutely|Sure)[!.][ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*I(?:'m| am) happy to help[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*I(?:'d| would) be happy to help[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[ \t]*What a (?:fascinating|wonderful|great|terrific)[^.!\n]*[.!]?[ \t]*", re.IGNORECASE | re.MULTILINE),
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
    re.compile(r"(^|(?<=[.!?]\s))In conclusion[,]?[ \t]+", re.MULTILINE),
    re.compile(r"(^|(?<=[.!?]\s))To summarize[,]?[ \t]+", re.MULTILINE),
]

# Stock vocab → plain replacement. Keep the noun-context guard on `navigate`/`journey`
# so we don't replace literal navigation or actual journeys.
STOCK_VOCAB = [
    (re.compile(r"\bdelve into\b", re.IGNORECASE), "look at"),
    (re.compile(r"\bdelve\b", re.IGNORECASE), "look at"),
    (re.compile(r"\btapestry\b", re.IGNORECASE), "mix"),
    (re.compile(r"\b(?:is|was|are|were)\s+a\s+testament\s+to\b", re.IGNORECASE), r"shows"),
    (re.compile(r"\b(?:a|the)\s+testament\s+to\b", re.IGNORECASE), r"shows"),
    (re.compile(r"\btestament to\b", re.IGNORECASE), "shows"),
    (re.compile(r"\bnavigate\s+through\b", re.IGNORECASE), "work through"),
    (re.compile(r"\bnavigate(?=\s+(?:the|around|these|this|that|our|complex))\b", re.IGNORECASE), "work through"),
    (re.compile(r"\bembark on\b", re.IGNORECASE), "start"),
    (re.compile(r"\bjourney(?=\s+(?:toward|to|of))\b", re.IGNORECASE), "path"),
    (re.compile(r"\brealm of\b", re.IGNORECASE), "world of"),
    (re.compile(r"\blandscape of\b", re.IGNORECASE), "world of"),
    (re.compile(r"\bpivotal\b", re.IGNORECASE), "key"),
    (re.compile(r"\bparamount\b", re.IGNORECASE), "essential"),
    (re.compile(r"\bseamlessly\b", re.IGNORECASE), "smoothly"),
    (re.compile(r"\bseamless\b", re.IGNORECASE), "smooth"),
    (re.compile(r"\bholistically\b", re.IGNORECASE), "completely"),
    (re.compile(r"\bholistic\b", re.IGNORECASE), "complete"),
    (re.compile(r"\bleverag(?:e|es|ed|ing)\b", re.IGNORECASE), "use"),
    (re.compile(r"\bcutting-edge\b", re.IGNORECASE), "modern"),
    (re.compile(r"\bstate-of-the-art\b", re.IGNORECASE), "modern"),
    (re.compile(r"\bcomprehensively\b", re.IGNORECASE), "completely"),
    (re.compile(r"\bcomprehensive\b", re.IGNORECASE), "complete"),
    (re.compile(r"\brobust(?=\s+(?:and|solution|implementation|approach|system|architecture))\b", re.IGNORECASE), "solid"),
]

# Performative balance: collapse mid-sentence ", however," to ". " (sentence break),
# and strip "However, " at the start of any sentence (line OR after period+space).
PERFORMATIVE = [
    (re.compile(r",\s*however,\s*", re.IGNORECASE), ". "),
    (re.compile(r"(^|(?<=[.!?]\s))However,\s+", re.MULTILINE), r"\1"),
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
    for ch in block:
        if ch == "—":
            count += 1
            buf.append("—" if count <= max_dashes else ",")
        else:
            buf.append(ch)
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


def humanize_deterministic(text: str) -> str:
    """Pure regex pass. Preserves code/URLs via placeholders; strips canonical AI-isms."""
    protected, table = _protect(text)

    # Sycophancy stacks ("Great question! I'd be happy to help.") need multiple passes
    # because each strip can expose a new line-start pattern. Cap at 5 to avoid
    # pathological loops on adversarial input.
    for _ in range(5):
        before = protected
        for pattern in SYCOPHANCY:
            protected = pattern.sub("", protected)
        if protected == before:
            break

    for pattern in HEDGING_OPENERS:
        protected = pattern.sub("", protected)

    for pattern in TRANSITION_TICS:
        protected = pattern.sub(r"\1", protected)

    for pattern, repl in STOCK_VOCAB:
        protected = pattern.sub(repl, protected)

    for pattern, repl in PERFORMATIVE:
        protected = pattern.sub(repl, protected)

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
    _SENTENCE_ABBREVS = (
        "i.e", "e.g", "etc", "vs", "cf", "viz", "al",  # "et al."
        "Dr", "Mr", "Mrs", "Ms", "St", "Jr", "Sr", "No",
    )

    def capitalize_after_start(m: re.Match) -> str:
        return m.group(1) + m.group(2).upper()

    def capitalize_after_sentence(m: re.Match) -> str:
        start = m.start()
        prefix = m.string[max(0, start - 5):start]
        for abbr in _SENTENCE_ABBREVS:
            if prefix.endswith(abbr):
                return m.group(0)
        return m.group(1) + m.group(2).upper()

    protected = re.sub(r"(^|\n\n)([a-z])", capitalize_after_start, protected)
    protected = re.sub(r"([.!?]\s+)([a-z])", capitalize_after_sentence, protected)

    # Collapse 3+ blank lines to 2 (BUT not 1 → preserve heading/paragraph spacing)
    protected = re.sub(r"\n{3,}", "\n\n", protected)
    # Strip trailing whitespace on each line so we don't ship messy diffs
    protected = re.sub(r"[ \t]+\n", "\n", protected)

    return _restore(protected, table)


# ---------- LLM-driven humanization ----------


def _build_humanize_prompt(original: str) -> str:
    return f"""Humanize this markdown so it reads like a careful human wrote it.

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
- Drop stock vocab (delve, tapestry, testament, navigate, embark, journey, realm, landscape, pivotal, paramount, seamless, holistic, leverage as filler, robust as filler, comprehensive as filler, cutting-edge, state-of-the-art)
- Drop hedging stack openers ("It's important to note that", "It's worth mentioning that", "Generally speaking", "In essence", "At its core")
- Drop performative balance — every claim does not need a "however"
- Engineer burstiness — mix short and long sentences deliberately
- Tighten tricolons — "X, Y, and Z" stacks where two would suffice → keep two
- Merge bullet soup — three bullets that say the same thing → one sentence
- Vary paragraph length — no tidy five-paragraph essay shape

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
        model=os.environ.get("HUMANIZER_MODEL", "claude-sonnet-4-5"),
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


def humanize_llm(text: str) -> str:
    prompt = _build_humanize_prompt(text)
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


def humanize_file(path: Path, *, deterministic: bool = False) -> bool:
    original_text = path.read_text(encoding="utf-8")
    backup_path = path.with_name(path.stem + ".original.md")

    if backup_path.exists():
        sys.stderr.write(
            f"Backup already exists at {backup_path}. "
            "Remove or rename it before re-humanizing.\n"
        )
        return False

    if deterministic:
        humanized = humanize_deterministic(original_text)
        result = validate(original_text, humanized)
        sys.stdout.write(format_report(result) + "\n")
        if not result.ok:
            sys.stderr.write(
                "Deterministic pass produced a structural change; refusing to write.\n"
            )
            return False
        backup_path.write_text(original_text, encoding="utf-8")
        path.write_text(humanized, encoding="utf-8")
        return True

    backup_path.write_text(original_text, encoding="utf-8")

    try:
        humanized = humanize_llm(original_text)
    except RuntimeError as exc:
        sys.stderr.write(f"{exc}\n")
        backup_path.unlink(missing_ok=True)
        return False

    for attempt in range(MAX_RETRIES + 1):
        result = validate(original_text, humanized)
        sys.stdout.write(f"Attempt {attempt + 1}:\n{format_report(result)}\n")
        if result.ok:
            path.write_text(humanized, encoding="utf-8")
            return True
        if attempt < MAX_RETRIES:
            sys.stdout.write("Requesting targeted fix...\n")
            fixed = _llm_fix(original_text, humanized, result.errors)
            if fixed is None:
                break
            humanized = fixed

    sys.stderr.write("Could not produce a structurally valid humanization. Restoring original.\n")
    sys.stderr.write(f"Backup preserved at {backup_path} for debugging.\n")
    path.write_text(original_text, encoding="utf-8")
    return False
