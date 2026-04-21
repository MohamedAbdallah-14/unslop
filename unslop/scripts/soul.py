"""Phase 5 soul injection: targeted ADDITIONS that shift token distribution
toward human defaults after the subtractive passes have cleaned slop.

Context: Phase 3 showed that lexical + structural rewriting alone moves the
TMR detector score by 0.0-0.2 percentage points on our fixtures despite
stripping 88-92% of lexical AI-isms. Token-level detectors read the
distributional fingerprint, not the offensive vocabulary list. To move that
fingerprint we need targeted injections — not rewrites, not rewordings, but
changes to how the prose distributes its tokens.

The safest high-signal lever is contraction rate. AI training data skews
toward full forms ('do not', 'it is', 'will not'); humans contract heavily
('don't', "it's", 'won't'). Flipping full → contracted where safe shifts the
n-gram distribution measurably without risking meaning.

Two passes, both inside the protected-region placeholder system:

  contract_negations
      Expand 14 auxiliary-negation pairs to their contracted form. Always
      safe — English grammar only composes these one way, and the
      contraction has the same truth value as the full form.

  contract_copula
      Contract `it is` → `it's`, `that is` → `that's`, `there is` → `there's`
      when the position clearly reads as a copula (not a possessive-
      fronting noun phrase). Conservative: skipped when the next word is a
      noun that might take a possessive reading.

Both passes are off in `subtle`, on in `balanced` and `full`. Hard-off
inside code/legal/medical blocks via the existing _protect system.

What this module does NOT do:

  - Insert sentence fragments out of thin air (risks fabrication).
  - Add parenthetical asides (risks changing meaning).
  - Rewrite openers of repeated-subject sentences (risks grammatical churn).

Those ideas are in the research but need a rewrite-capable pass (LLM or a
small local model). This module sticks to safe deterministic edits.

Research basis: Cat 04 (sampler-level slop reduction), Cat 14 (structural
tells), Cat 05 (Adversarial Paraphrasing TPR). The contraction-rate lever
is the one move that (a) is trivially deterministic, (b) measurably shifts
token distribution, (c) passes byte-for-byte preservation of code/URLs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Auxiliary-negation contractions. Each entry: (pattern, replacement).
# Patterns match case-insensitively but preserve the case of the first letter
# of the auxiliary so "Do not" → "Don't" and "do not" → "don't".
#
# Ordering: longer auxiliaries first to avoid partial-matching ("should not"
# must be tried before "would not" if both somehow overlap — they don't, but
# keep the pattern sorted by length for future safety).
_NEGATION_CONTRACTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b([Dd])o not\b"), r"\1on't"),
    (re.compile(r"\b([Dd])oes not\b"), r"\1oesn't"),
    (re.compile(r"\b([Dd])id not\b"), r"\1idn't"),
    (re.compile(r"\b([Cc])annot\b"), r"\1an't"),
    (re.compile(r"\b([Cc])an not\b"), r"\1an't"),
    (re.compile(r"\b([Ww])ill not\b"), r"\1on't"),
    (re.compile(r"\b([Ww])ould not\b"), r"\1ouldn't"),
    (re.compile(r"\b([Ss])hould not\b"), r"\1houldn't"),
    (re.compile(r"\b([Cc])ould not\b"), r"\1ouldn't"),
    (re.compile(r"\b([Mm])ight not\b"), r"\1ightn't"),
    (re.compile(r"\b([Mm])ust not\b"), r"\1ustn't"),
    (re.compile(r"\b([Ii])s not\b"), r"\1sn't"),
    (re.compile(r"\b([Aa])re not\b"), r"\1ren't"),
    (re.compile(r"\b([Ww])as not\b"), r"\1asn't"),
    (re.compile(r"\b([Ww])ere not\b"), r"\1eren't"),
    (re.compile(r"\b([Hh])as not\b"), r"\1asn't"),
    (re.compile(r"\b([Hh])ave not\b"), r"\1aven't"),
    (re.compile(r"\b([Hh])ad not\b"), r"\1adn't"),
]

# Copula contractions. Conservative: skip when the following word looks like
# a noun that could be possessive-fronted (would make "it's Y" read as
# "it is a Y" vs "it is (its) Y"). Heuristic: skip when next word is "own"
# (possessive-owner cliché) or when sentence-start pattern is capitalized
# proper noun (common in technical writing).
#
# Pattern: "it is" not followed by " own" and NOT at the very start of a
# capitalized-noun sentence context.
_COPULA_CONTRACTIONS: list[tuple[re.Pattern[str], str]] = [
    # "it is the X" / "it is a X" / "it is not" etc. — safe
    (re.compile(r"\b([Ii])t is(?=\s+(?:a|an|the|not|already|still|just|only|really|"
                r"better|worse|more|less|very|quite|pretty|also|now|then|also|"
                r"what|where|how|why|when|who|which|possible|impossible|"
                r"clear|unclear|obvious|easy|hard|time)\b)"), r"\1t's"),
    # "that is the X" etc.
    (re.compile(r"\b([Tt])hat is(?=\s+(?:a|an|the|not|why|how|what|where|when|who|"
                r"which|one|also|still|just|really|pretty|quite|our|your|their)\b)"), r"\1hat's"),
    # "there is a X" — possessive-fronting impossible here (there has no semantic referent)
    (re.compile(r"\b([Tt])here is(?=\s+(?:a|an|no|one|only|always|sometimes|often|"
                r"little|much|nothing|something|anything|everything)\b)"), r"\1here's"),
    # "we are" → "we're" — "we" is unambiguously a pronoun, always safe
    (re.compile(r"\b([Ww])e are\b"), r"\1e're"),
    # "you are" → "you're"
    (re.compile(r"\b([Yy])ou are\b"), r"\1ou're"),
    # "they are" → "they're"
    (re.compile(r"\b([Tt])hey are\b"), r"\1hey're"),
    # "I am" → "I'm"
    (re.compile(r"\bI am\b"), "I'm"),
    # "I have" → "I've" only when followed by past participle
    (re.compile(r"\bI have(?=\s+(?:seen|done|had|been|found|made|known|thought|"
                r"tried|worked|written|shipped|built|pushed|pulled|read|used|"
                r"checked|noticed|learned|heard)\b)"), "I've"),
    # "we have" / "you have" / "they have" → same
    (re.compile(r"\b([Ww])e have(?=\s+(?:seen|done|had|been|found|made|known|thought|"
                r"tried|worked|written|shipped|built|pushed|pulled|read|used|"
                r"checked|noticed|learned|heard)\b)"), r"\1e've"),
    (re.compile(r"\b([Tt])hey have(?=\s+(?:seen|done|had|been|found|made|known|thought|"
                r"tried|worked|written|shipped|built|pushed|pulled|read|used|"
                r"checked|noticed|learned|heard)\b)"), r"\1hey've"),
    # "I will" → "I'll" — always safe since "I" is unambiguously a pronoun
    (re.compile(r"\bI will\b"), "I'll"),
    (re.compile(r"\b([Ww])e will\b"), r"\1e'll"),
    (re.compile(r"\b([Yy])ou will\b"), r"\1ou'll"),
    (re.compile(r"\b([Tt])hey will\b"), r"\1hey'll"),
]


@dataclass
class SoulReport:
    """Counts of soul-pass injections."""

    negations_contracted: int = 0
    copulas_contracted: int = 0

    def to_dict(self) -> dict:
        return {
            "negations_contracted": self.negations_contracted,
            "copulas_contracted": self.copulas_contracted,
        }


def contract_negations(
    text: str,
    *,
    report: SoulReport | None = None,
) -> str:
    """Expand 18 auxiliary-negation pairs to contracted form.

    Runs on protected text — placeholders are unchanged because they
    contain no English words. Case of the auxiliary is preserved via
    backreference."""
    for pattern, repl in _NEGATION_CONTRACTIONS:
        if report is not None:
            matches = len(pattern.findall(text))
            report.negations_contracted += matches
        text = pattern.sub(repl, text)
    return text


def contract_copula(
    text: str,
    *,
    report: SoulReport | None = None,
) -> str:
    """Contract `it is`, `that is`, `there is`, `I am`, `we/you/they are`,
    `I/we/they have + participle`, `I/we/you/they will` where safe.

    Each pattern has an explicit allow-list for what can follow, so the
    contractions only fire in positions where the copula reading is
    unambiguous. Operates on protected text."""
    for pattern, repl in _COPULA_CONTRACTIONS:
        if report is not None:
            matches = len(pattern.findall(text))
            report.copulas_contracted += matches
        text = pattern.sub(repl, text)
    return text


def humanize_soul(
    text: str,
    *,
    report: SoulReport | None = None,
) -> str:
    """Apply soul-injection passes. Intended to run on protected text,
    after lexical + structural passes."""
    text = contract_negations(text, report=report)
    text = contract_copula(text, report=report)
    return text
