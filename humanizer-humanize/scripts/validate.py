"""Validate that humanization preserved structure (code, URLs, paths, headings, bullets)
and reduced AI-isms (residual count must drop, never grow).

Also reports a burstiness metric (sentence-length variance). Flat burstiness is the #1
signal AI-text detectors key on (see docs/research/04-natural-language-quality/ and 05-ai-text-detection-and-evasion/).
The metric is informational — low burstiness does not fail validation, it warns."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Iterable

FENCED_CODE = re.compile(r"^```[^\n]*\n[\s\S]*?^```\s*$", re.MULTILINE)
INDENTED_CODE = re.compile(
    r"(?m)(?:^(?: {4}|\t)[^\n]+(?:\n(?: {4}|\t)[^\n]+)*)"
)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://[^\s)>\]]+")
MD_LINK = re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")
MD_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
PATH = re.compile(r"(?:^|\s)(/[A-Za-z0-9._/\-]+|[A-Za-z]:\\[A-Za-z0-9._\\\-]+|\./[A-Za-z0-9._/\-]+)")
BULLET = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
YAML_FRONTMATTER = re.compile(r"\A---\n[\s\S]*?\n---(?=\n|\Z)")
BLOCKQUOTE_BLOCK = re.compile(r"(?m)(?:^[ \t]*>[^\n]*(?:\n[ \t]*>[^\n]*)*)")
TABLE_BLOCK = re.compile(
    r"(?m)(?:^[ \t]*\|[^\n]*\|[ \t]*(?:\n[ \t]*\|[^\n]*\|[ \t]*)+)"
)


AI_ISMS = (
    # Sycophancy openers (case-insensitive)
    r"\bgreat question\b", r"\bcertainly!", r"\babsolutely!", r"\bsure!",
    r"\bi'?d be happy to help\b", r"\bwhat a (?:fascinating|wonderful|great|terrific)\b",
    # Stock vocab — context-guarded to match humanize.py's STOCK_VOCAB patterns.
    # Bare \bnavigate\b etc. caused false positives on literal uses like
    # "navigate to the next page" that the humanizer correctly preserves.
    r"\bdelve\b", r"\btapestry\b", r"\btestament to\b",
    r"\bnavigate(?=\s+(?:the|through|around|these|this|that|our|complex))\b",
    r"\bembark on\b",
    r"\bjourney(?=\s+(?:toward|to|of))\b",
    r"\brealm of\b", r"\blandscape of\b",
    r"\bpivotal\b", r"\bparamount\b", r"\bseamless\b", r"\bholistic\b",
    r"\brobust(?=\s+(?:and|solution|implementation|approach|system|architecture))\b",
    r"\bleverage\b", r"\bcutting-edge\b", r"\bstate-of-the-art\b",
    # Hedging stacks
    r"\bit'?s important to note that\b",
    r"\bit'?s worth (?:mentioning|noting|pointing out) that\b",
    r"\bgenerally speaking\b",
    r"\bin essence\b",
    r"\bat its core\b",
    r"\bit should be noted that\b",
    # Transitional AI tics at sentence start. Guard: capture only when they
    # open a sentence (line start or after sentence-end punctuation).
    r"(?:^|(?<=[.!?]\s))(?:furthermore|moreover|additionally)\b",
    r"(?:^|(?<=[.!?]\s))in conclusion\b",
    r"(?:^|(?<=[.!?]\s))to summarize\b",
)
AI_ISM_PATTERNS = [re.compile(p, re.IGNORECASE) for p in AI_ISMS]


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str]
    ai_isms_before: int
    ai_isms_after: int
    burstiness_before: float = 0.0
    burstiness_after: float = 0.0
    sentence_length_range_after: tuple[int, int] = (0, 0)


def _extract(pattern: re.Pattern, text: str) -> list[str]:
    return pattern.findall(text)


def _strip_code_for_prose(text: str) -> str:
    """Remove everything that isn't natural-language prose so burstiness reflects
    the actual writing: code (fenced, indented, inline), YAML frontmatter, tables,
    and blockquotes (those are either examples or quoted material, not the
    author's own rhythm)."""
    text = YAML_FRONTMATTER.sub("", text)
    text = FENCED_CODE.sub("", text)
    text = INDENTED_CODE.sub("", text)
    text = TABLE_BLOCK.sub("", text)
    text = BLOCKQUOTE_BLOCK.sub("", text)
    text = INLINE_CODE.sub("", text)
    return text


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])")


def _sentence_lengths(text: str) -> list[int]:
    """Word-count per sentence across prose only. Used for burstiness."""
    prose = _strip_code_for_prose(text)
    lengths: list[int] = []
    for paragraph in re.split(r"\n\s*\n", prose):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        for sentence in _SENTENCE_SPLIT.split(paragraph):
            words = [w for w in re.split(r"\s+", sentence.strip()) if w]
            if words:
                lengths.append(len(words))
    return lengths


def _burstiness(lengths: list[int]) -> float:
    """Standard deviation of sentence lengths. Higher = more human-like rhythm.
    Returns 0.0 if fewer than 2 sentences (not meaningful)."""
    if len(lengths) < 2:
        return 0.0
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    return math.sqrt(variance)


def _extract_fenced_blocks(text: str) -> list[str]:
    """Return fenced code blocks as a list, preserving content exactly."""
    return FENCED_CODE.findall(text)


def _extract_indented_blocks(text: str) -> list[str]:
    """Return indented code blocks as a list, preserving content exactly."""
    return INDENTED_CODE.findall(text)


def _count_ai_isms(text: str) -> int:
    return sum(len(p.findall(text)) for p in AI_ISM_PATTERNS)


def validate(original: str, humanized: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    # Code blocks — exact comparison, no normalization
    orig_code = _extract_fenced_blocks(original)
    new_code = _extract_fenced_blocks(humanized)
    if orig_code != new_code:
        errors.append(
            "Code block(s) modified, reordered, removed, or added."
        )

    # Indented code blocks
    orig_indented = _extract_indented_blocks(original)
    new_indented = _extract_indented_blocks(humanized)
    if orig_indented != new_indented:
        errors.append(
            f"Indented code block(s) modified or removed. {len(orig_indented)} → {len(new_indented)}."
        )

    # YAML frontmatter
    orig_yaml = YAML_FRONTMATTER.findall(original)
    new_yaml = YAML_FRONTMATTER.findall(humanized)
    if orig_yaml != new_yaml:
        errors.append("YAML frontmatter modified, removed, or added.")

    # Blockquotes — treat as verbatim-quoted content
    orig_quotes = BLOCKQUOTE_BLOCK.findall(original)
    new_quotes = BLOCKQUOTE_BLOCK.findall(humanized)
    if orig_quotes != new_quotes:
        errors.append(
            f"Blockquote(s) modified. {len(orig_quotes)} → {len(new_quotes)}."
        )

    # Tables — treat as reference content (glossaries, comparison rows)
    orig_tables = TABLE_BLOCK.findall(original)
    new_tables = TABLE_BLOCK.findall(humanized)
    if orig_tables != new_tables:
        errors.append(
            f"Markdown table(s) modified. {len(orig_tables)} → {len(new_tables)}."
        )

    # Inline code
    orig_inline = set(_extract(INLINE_CODE, original))
    new_inline = set(_extract(INLINE_CODE, humanized))
    missing_inline = orig_inline - new_inline
    if missing_inline:
        errors.append(
            f"Inline code missing: {sorted(missing_inline)[:5]}"
            + (f" (+{len(missing_inline) - 5} more)" if len(missing_inline) > 5 else "")
        )

    # URLs
    orig_urls = set(_extract(URL, original))
    new_urls = set(_extract(URL, humanized))
    missing_urls = orig_urls - new_urls
    if missing_urls:
        errors.append(
            f"URL(s) missing: {sorted(missing_urls)[:5]}"
            + (f" (+{len(missing_urls) - 5} more)" if len(missing_urls) > 5 else "")
        )

    # Markdown links
    orig_md_links = _extract(MD_LINK, original)
    new_md_links = _extract(MD_LINK, humanized)
    if orig_md_links != new_md_links:
        errors.append("Markdown link(s) modified, reordered, removed, or added.")

    # Headings
    orig_headings = [(level, text.strip()) for level, text in MD_HEADING.findall(original)]
    new_headings = [(level, text.strip()) for level, text in MD_HEADING.findall(humanized)]
    if orig_headings != new_headings:
        if len(orig_headings) != len(new_headings):
            errors.append(
                f"Heading count changed: {len(orig_headings)} → {len(new_headings)}"
            )
        else:
            for (lo, ho), (ln, hn) in zip(orig_headings, new_headings):
                if lo != ln or ho != hn:
                    errors.append(f"Heading changed: {lo} {ho!r} → {ln} {hn!r}")
                    break

    # Paths
    orig_paths = set(m.group(1) for m in PATH.finditer(original))
    new_paths = set(m.group(1) for m in PATH.finditer(humanized))
    missing_paths = orig_paths - new_paths
    if missing_paths:
        warnings.append(
            f"Path(s) possibly missing: {sorted(missing_paths)[:3]}"
            + (f" (+{len(missing_paths) - 3} more)" if len(missing_paths) > 3 else "")
        )

    # Bullets — humanizer is allowed to consolidate, but not to drop more than half
    orig_bullets = len(BULLET.findall(original))
    new_bullets = len(BULLET.findall(humanized))
    if orig_bullets > 0 and new_bullets < orig_bullets // 2:
        warnings.append(
            f"Bullet count dropped sharply: {orig_bullets} → {new_bullets}. "
            "Humanizer may have over-consolidated."
        )

    # AI-ism residual: must not increase
    ai_before = _count_ai_isms(original)
    ai_after = _count_ai_isms(humanized)
    if ai_after > ai_before:
        errors.append(
            f"AI-ism count increased: {ai_before} → {ai_after}. Humanizer added slop."
        )
    elif ai_before > 0 and ai_after == ai_before:
        warnings.append(
            f"AI-isms unchanged ({ai_before}). Humanizer did not strip canonical phrases."
        )

    # Burstiness — sentence-length variance. Flat = detector bait. Informational.
    orig_lengths = _sentence_lengths(original)
    new_lengths = _sentence_lengths(humanized)
    burst_before = _burstiness(orig_lengths)
    burst_after = _burstiness(new_lengths)
    length_range = (
        (min(new_lengths), max(new_lengths)) if new_lengths else (0, 0)
    )
    # Threshold: stddev < 4 on a doc with ≥8 sentences means suspiciously uniform.
    if len(new_lengths) >= 8 and burst_after < 4.0:
        warnings.append(
            f"Burstiness low (σ={burst_after:.1f} across {len(new_lengths)} sentences). "
            "Flat sentence length is the #1 AI-detector signal. Vary rhythm more."
        )

    return ValidationResult(
        ok=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        ai_isms_before=ai_before,
        ai_isms_after=ai_after,
        burstiness_before=burst_before,
        burstiness_after=burst_after,
        sentence_length_range_after=length_range,
    )


def format_report(result: ValidationResult) -> str:
    parts: list[str] = []
    if result.ok:
        parts.append("Validation: OK")
    else:
        parts.append("Validation: FAILED")
    parts.append(f"  AI-isms: {result.ai_isms_before} → {result.ai_isms_after}")
    if result.burstiness_after > 0:
        lo, hi = result.sentence_length_range_after
        parts.append(
            f"  Burstiness σ: {result.burstiness_before:.1f} → {result.burstiness_after:.1f}"
            f" (range {lo}-{hi} words/sentence)"
        )
    for err in result.errors:
        parts.append(f"  ERROR: {err}")
    for warn in result.warnings:
        parts.append(f"  warn:  {warn}")
    return "\n".join(parts)
