#!/usr/bin/env python3
"""
AI-ism scanner + burstiness / length / opener checker.

Usage:
    python scan.py <file>
    cat draft.md | python scan.py -
    echo "some text" | python scan.py -

Exits non-zero when HIGH-severity AI-isms are found or structural targets fail.
Standard library only. No network access.

Pass criteria (default):
- Zero HIGH-severity AI-ism hits.
- Sentence-length std dev >= 8.
- At least one sentence < 10 words and one > 25 words per 150 words.
- No paragraph-opener word repeated twice.
"""

from __future__ import annotations

import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Ban lists. Keep in sync with anti-aiisms.md.
# ---------------------------------------------------------------------------

HIGH_WORDS = [
    r"\bdelv(?:e|es|ing)\b",
    r"\btapestry\b",
    r"\btestament\b",
    r"\bbustling\b",
    r"\bvibrant\b",
    r"\brealm\b",
    r"\bnavigate(?=\s+(?:the|through|around|these|this|that|our|complex))\b",
    r"\bharness(?:es|ed|ing)?\b",
    r"\bleverag(?:e|es|ed|ing)\b",
    r"\bmultifaceted\b",
    r"\bunderscores?\b",
    r"\bparadigm shift\b",
    r"\btreasure trove\b",
    r"\blabyrinth(?:ine)?\b",
    r"\bmyriad\b",
    r"\bplethora\b",
    r"\bever-evolving\b",
    r"\bever-changing\b",
    r"\bgame[- ]chang(?:er|ing)\b",
    r"\bcrucial(?:ly)?\b",
    r"\bpivotal\b",
    r"\brobust(?=\s+(?:and|solution|implementation|approach|system|architecture|framework|platform))\b",
    r"\bwhimsical\b",
    r"\bmeticulous(?:ly)?\b",
    r"\bseamless(?:ly)?\b",
    r"\bunparalleled\b",
    r"\bcutting[- ]edge\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
]

HIGH_PHRASES = [
    r"\bit'?s important to note\b",
    r"\bit'?s worth noting\b",
    r"\bit'?s worth mentioning\b",
    r"\bit'?s crucial to\b",
    r"\bit'?s essential to\b",
    r"\bin conclusion,",
    r"\bin summary,",
    r"\bto summarize,",
    r"\bto conclude,",
    r"\boverall,\s",
    r"^Ultimately,\s",
    r"^Furthermore,\s",
    r"^Moreover,\s",
    r"^Additionally,\s",
    r"\bin today'?s fast[- ]paced world\b",
    r"\bin the ever[- ]evolving landscape of\b",
    r"\bin the world of\b",
    r"\bwhen it comes to\b",
    r"\blet'?s dive in\b",
    r"\bdive into\b",
    r"\bunlock the power of\b",
    r"\bunleash the potential of\b",
    r"\bat the heart of\b",
    r"\bthe rise of\b",
    r"\ba deep dive into\b",
    r"\bwhether you'?re\b[^.!?\n]{5,},\s+(?:or\b|and\b)",
    r"\bgreat question!",
    r"\bthat'?s an excellent question\b",
    r"\bwhat a thoughtful question\b",
    r"\bi hope this helps\b",
    r"\bfeel free to ask\b",
    r"\blet me know if you (?:have|need)\b",
]

# "It's not just X, it's Y" shape
SHAPE_NOT_JUST = re.compile(
    r"\bit'?s not (?:just )?[^.,;!?\n]{1,60}[—\-,]\s*it'?s\b", re.IGNORECASE
)

# Tricolon of adjectives: "X, Y, and Z" where each is a single word
TRICOLON = re.compile(
    r"\b([a-z]{3,}),\s+([a-z]{3,}),?\s+and\s+([a-z]{3,})\b", re.IGNORECASE
)

MED_HEDGES = [
    r"\bmight\b",
    r"\bperhaps\b",
    r"\bpossibly\b",
    r"\barguably\b",
    r"\bcould be seen as\b",
    r"\bsome would argue\b",
    r"\bit could be argued\b",
]

MARKETING_VERBS = [
    r"\bfoster(?:s|ed|ing)?\b",
    r"\bfacilitat(?:e|es|ed|ing)\b",
    r"\boptimiz(?:e|es|ed|ing)\b",
    r"\bstreamlin(?:e|es|ed|ing)\b",
    r"\brevolutioniz(?:e|es|ed|ing)\b",
    r"\bempower(?:s|ed|ing)?\b",
    r"\belevat(?:e|es|ed|ing)\b",
    r"\btransform(?:s|ed|ing)?\b",
    r"\bcurat(?:e|es|ed|ing)\b",
]

LOW_OPENERS = [
    "Importantly",
    "Interestingly",
    "Notably",
    "Remarkably",
    "Essentially",
    "Fundamentally",
    "Ultimately",
    "Significantly",
    "Additionally",
    "Furthermore",
    "Moreover",
]

SYCOPHANT_OPENERS = ("Certainly!", "Of course!", "Absolutely!", "Great question")

# ---------------------------------------------------------------------------
# Sentence / paragraph splitting. Kept intentionally simple.
# ---------------------------------------------------------------------------

_ABBREVS = frozenset(
    "Dr Mr Mrs Ms Prof Jr Sr St vs etc Rev Gen Sgt Col Capt Lt Cmdr "
    "Jan Feb Mar Apr Jun Jul Aug Sep Oct Nov Dec "
    "Ave Blvd Ln".split()
)
_RAW_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'\(])")
_WORD_RE = re.compile(r"\b[\w'-]+\b")

_FENCED_BLOCK = re.compile(r"^```[^\n]*\n[\s\S]*?^```\s*$", re.MULTILINE)
_INLINE_CODE = re.compile(r"`[^`\n]+`")


def _strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so ban-list regexes
    don't fire on legitimate tokens inside code samples."""
    text = _FENCED_BLOCK.sub("", text)
    text = _INLINE_CODE.sub("", text)
    return text


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def sentences(text: str) -> list[str]:
    """Split on sentence-ending punctuation, but rejoin false splits after
    common abbreviations (Dr., U.S., e.g., etc.)."""
    raw = [s.strip() for s in _RAW_SENT_SPLIT.split(text) if s.strip()]
    merged: list[str] = []
    for chunk in raw:
        if merged:
            prev = merged[-1]
            last_word = prev.rsplit(None, 1)[-1].rstrip(".!?") if prev else ""
            if last_word in _ABBREVS or re.search(r"\b[A-Z]\.$", prev):
                merged[-1] = prev + " " + chunk
                continue
        merged.append(chunk)
    return merged


def word_count(s: str) -> int:
    return len(_WORD_RE.findall(s))


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    severity: str  # HIGH | MED | LOW | STRUCT
    kind: str
    detail: str
    line: int = 0

    def render(self) -> str:
        loc = f"L{self.line}" if self.line else "--"
        return f"  [{self.severity:<6}] {loc:<5} {self.kind:<18} {self.detail}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    words: int = 0
    sent_lengths: list[int] = field(default_factory=list)
    paragraph_openers: list[str] = field(default_factory=list)

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    def struct_fail(self) -> int:
        return sum(1 for f in self.findings if f.severity == "STRUCT")


# ---------------------------------------------------------------------------
# Scanners
# ---------------------------------------------------------------------------


def _line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _find_all(patterns: list[str], text: str, severity: str, kind: str, report: Report) -> None:
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE | re.MULTILINE):
            report.add(
                Finding(
                    severity=severity,
                    kind=kind,
                    detail=f'"{m.group(0).strip()}"',
                    line=_line_of(text, m.start()),
                )
            )


def scan_vocab(text: str, report: Report) -> None:
    _find_all(HIGH_WORDS, text, "HIGH", "vocab", report)
    _find_all(HIGH_PHRASES, text, "HIGH", "phrase", report)
    _find_all(MARKETING_VERBS, text, "MED", "marketing-verb", report)

    # Hedges: only flag when density > 3 / 200 words
    hedge_hits = sum(
        1
        for pat in MED_HEDGES
        for _ in re.finditer(pat, text, flags=re.IGNORECASE)
    )
    if report.words and hedge_hits > 3 * (report.words / 200):
        report.add(
            Finding(
                severity="MED",
                kind="hedge-density",
                detail=f"{hedge_hits} reflexive hedges in {report.words} words "
                "(use calibrated ladder: unlikely/plausible/probable/...).",
            )
        )


def scan_shape(text: str, report: Report) -> None:
    for m in SHAPE_NOT_JUST.finditer(text):
        report.add(
            Finding(
                severity="HIGH",
                kind="not-just-shape",
                detail=f'"{m.group(0)[:60]}..."',
                line=_line_of(text, m.start()),
            )
        )

    # Em-dash density (includes en-dash and double-hyphen variants)
    em = text.count("\u2014") + text.count("\u2013") + text.count("--")
    if report.words and em > max(1, report.words / 200):
        report.add(
            Finding(
                severity="HIGH",
                kind="em-dash",
                detail=f"{em} em/en-dashes in {report.words} words "
                f"(budget: \u22641 per 200 words).",
            )
        )

    # Tricolons of single-word adjectives
    tri_hits = [m.group(0) for m in TRICOLON.finditer(text)]
    # filter to avoid matching list of names, etc. (rough heuristic: short adj-ish words)
    tri_hits = [t for t in tri_hits if all(len(w) <= 12 for w in t.split())]
    if len(tri_hits) > 1:
        report.add(
            Finding(
                severity="MED",
                kind="tricolon",
                detail=f"{len(tri_hits)} tricolons "
                f'(first: "{tri_hits[0]}"; budget: ≤1).',
            )
        )


def scan_structure(text: str, report: Report) -> None:
    paras = paragraphs(text)
    sents_all = sentences(text)
    report.sent_lengths = [word_count(s) for s in sents_all if word_count(s) > 0]
    report.words = sum(report.sent_lengths)

    # burstiness: sentence-length std dev
    if len(report.sent_lengths) >= 4:
        sd = statistics.pstdev(report.sent_lengths)
        if sd < 8:
            report.add(
                Finding(
                    severity="STRUCT",
                    kind="burstiness",
                    detail=f"sentence-length σ={sd:.1f} < 8 (flatter than human prose).",
                )
            )

    # short / long distribution per 150 words
    if report.words >= 150:
        short = sum(1 for n in report.sent_lengths if n < 10)
        long_ = sum(1 for n in report.sent_lengths if n > 25)
        per150 = report.words / 150
        if short < per150:
            report.add(
                Finding(
                    severity="STRUCT",
                    kind="length-dist",
                    detail=f"{short} short (<10w) sentences in {report.words} words "
                    f"(target ≥ {per150:.1f}).",
                )
            )
        if long_ < per150:
            report.add(
                Finding(
                    severity="STRUCT",
                    kind="length-dist",
                    detail=f"{long_} long (>25w) sentences in {report.words} words "
                    f"(target ≥ {per150:.1f}).",
                )
            )

    # paragraph openers — skip markdown syntax (headings, bullets, numbered lists)
    openers: list[str] = []
    for p in paras:
        line = p.lstrip()
        if re.match(r"^#{1,6}\s", line):
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^\d+\.\s+", "", line)
        first = line.split(None, 1)
        if first:
            openers.append(first[0].strip(",.:;\"'()[]"))
    report.paragraph_openers = openers

    seen: dict[str, int] = {}
    for w in openers:
        key = w.lower()
        seen[key] = seen.get(key, 0) + 1
    repeats = {w: c for w, c in seen.items() if c >= 2 and w}
    if repeats:
        report.add(
            Finding(
                severity="STRUCT",
                kind="para-opener",
                detail="repeated paragraph openers: "
                + ", ".join(f"{w}×{c}" for w, c in repeats.items()),
            )
        )

    # five-paragraph shape (intro + 3 body + conclusion feel)
    if 5 <= len(paras) <= 6:
        joined = "\n".join(paras[-1:]).lower()
        if any(p in joined for p in ("in conclusion", "in summary", "overall,", "to conclude")):
            report.add(
                Finding(
                    severity="STRUCT",
                    kind="essay-shape",
                    detail=f"{len(paras)}-paragraph essay with tidy conclusion (classic LLM shape).",
                )
            )

    # sycophant openers in first paragraph
    if paras:
        first_p = paras[0]
        for opener in SYCOPHANT_OPENERS:
            if first_p.lower().startswith(opener.lower()):
                report.add(
                    Finding(
                        severity="HIGH",
                        kind="sycophancy",
                        detail=f'opens with "{opener}"',
                        line=1,
                    )
                )

    # repeated adverb-ly openers
    ly_count = sum(1 for o in openers if o in LOW_OPENERS)
    if ly_count >= 2:
        report.add(
            Finding(
                severity="LOW",
                kind="adverb-opener",
                detail=f"{ly_count} adverb-ly paragraph openers (Importantly/Ultimately/…).",
            )
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def scan(text: str) -> Report:
    r = Report()
    prose = _strip_code(text)
    scan_structure(prose, r)  # populates r.words used by other scanners
    scan_vocab(prose, r)
    scan_shape(prose, r)
    order = {"HIGH": 0, "MED": 1, "STRUCT": 2, "LOW": 3}
    r.findings.sort(key=lambda f: (order.get(f.severity, 9), f.line))
    return r


def render(r: Report) -> str:
    lines: list[str] = []
    lines.append("Unslop scan")
    lines.append("=" * 60)
    lines.append(
        f"words={r.words}  sentences={len(r.sent_lengths)}  "
        f"paragraphs={len(r.paragraph_openers)}"
    )
    if r.sent_lengths:
        sd = statistics.pstdev(r.sent_lengths) if len(r.sent_lengths) >= 2 else 0.0
        lines.append(
            f"sentence-length: mean={statistics.mean(r.sent_lengths):.1f}  "
            f"σ={sd:.1f}  min={min(r.sent_lengths)}  max={max(r.sent_lengths)}"
        )
    lines.append("")
    if not r.findings:
        lines.append("  (no findings — output looks clean)")
    else:
        for f in r.findings:
            lines.append(f.render())
    lines.append("")
    verdict = "PASS" if r.high_count() == 0 and r.struct_fail() == 0 else "FAIL"
    lines.append(
        f"verdict: {verdict}  "
        f"(HIGH={r.high_count()}  STRUCT={r.struct_fail()}  "
        f"total={len(r.findings)})"
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    arg = argv[1]
    if arg == "-":
        text = sys.stdin.read()
    else:
        p = Path(arg)
        if not p.is_file():
            print(f"error: not a file: {arg}", file=sys.stderr)
            return 2
        text = p.read_text(encoding="utf-8", errors="replace")
    r = scan(text)
    print(render(r))
    return 0 if (r.high_count() == 0 and r.struct_fail() == 0) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
