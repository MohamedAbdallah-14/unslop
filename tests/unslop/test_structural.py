"""Tests for the Phase 1 structural humanizer (unslop/scripts/structural.py).

These tests assert two contracts:
  1. Correctness — splits and merges only fire when guards are satisfied.
  2. Non-regression — sentence-length variance (σ) strictly increases after
     split_long_sentences when there is at least one splittable sentence.

The module operates on placeholder-protected text; tests simulate that by
feeding plain text without code blocks. Integration with _protect/_restore is
covered in test_humanize.py once the hookup lands.
"""

from __future__ import annotations

import math

from unslop.scripts.structural import (
    StructuralReport,
    _count_words,
    humanize_structural,
    merge_bullet_soup,
    split_long_sentences,
)


def _stdev(nums: list[int]) -> float:
    if len(nums) < 2:
        return 0.0
    mean = sum(nums) / len(nums)
    return math.sqrt(sum((x - mean) ** 2 for x in nums) / len(nums))


def _sentence_word_counts(text: str) -> list[int]:
    import re

    sentences: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", paragraph.strip()):
            sent = sent.strip()
            if sent:
                sentences.append(sent)
    return [len(re.findall(r"\w+", s)) for s in sentences]


class TestCountWords:
    def test_plain_prose(self):
        assert _count_words("The quick brown fox") == 4

    def test_placeholder_counts_as_one(self):
        text = "See \x00LINK#0\x00 for details"
        assert _count_words(text) == 4

    def test_multiple_placeholders(self):
        text = "\x00FENCE#0\x00 and \x00LINK#1\x00 both stay"
        assert _count_words(text) == 5


class TestSplitLongSentencesSemicolon:
    def test_long_sentence_with_semicolon_splits(self):
        # 36-word sentence with a semicolon near the middle
        text = (
            "The parent component re-renders on every state change in the provider, "
            "propagating new references to every subscribed child; the memoized "
            "selector sees fresh props and recomputes even when values are unchanged."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 1
        # Two sentences after the split
        assert out.count(".") >= 2
        # Second half capitalizes
        assert ". The " in out

    def test_short_sentence_untouched(self):
        text = "This is short; this is also short."
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 0
        assert out == text

    def test_no_split_point_untouched(self):
        # 30+ words but no safe split candidate
        text = (
            "The system evaluates each incoming request against the cached policy "
            "table before any downstream handler runs against the database or "
            "emits external calls to partner services through the network layer."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 0
        assert out == text


class TestSplitLongSentencesConjunction:
    def test_but_splits_when_balanced(self):
        text = (
            "The first implementation passed every offline benchmark we had at "
            "that point in the review, but the integration suite caught three "
            "regressions in the authentication path that were not visible in unit tests."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 1
        assert ". But " in out

    def test_but_skipped_when_unbalanced(self):
        # Long sentence but the "but" clause has only 3 words — min_half=8
        text = (
            "The first implementation passed every offline benchmark we had at "
            "that point in the extended review process we run on pull requests, "
            "but it failed."
        )
        report = StructuralReport()
        split_long_sentences(text, report=report)
        assert report.sentences_split == 0

    def test_however_splits(self):
        text = (
            "The first implementation passed every offline benchmark we had at "
            "that point in the review cycle, however, the integration suite caught "
            "three regressions in the authentication path that were not visible."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 1
        assert ". However, " in out

    def test_emdash_splits_when_balanced(self):
        text = (
            "The parent component re-renders on every single state change that "
            "fires inside the provider — the memoized selector sees fresh props "
            "and recomputes its derived value even when the underlying data has not changed."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 1
        assert ". The " in out

    def test_and_then_splits(self):
        text = (
            "The worker dequeues a job from the primary Redis queue and validates "
            "the payload against our schema registry, and then the next stage "
            "enriches the record with the canonical customer profile before write."
        )
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 1
        assert ". Then " in out


class TestSplitPreservesPlaceholders:
    def test_placeholder_not_broken(self):
        text = (
            "See \x00LINK#0\x00 for the rationale on why the parser skips "
            "escape sequences, but the runtime still honors them in every "
            "downstream writer and buffer for backward compatibility with v1."
        )
        out = split_long_sentences(text)
        assert "\x00LINK#0\x00" in out


class TestSplitSkipsListParagraphs:
    def test_pure_list_untouched(self):
        text = (
            "- Uses React for rendering across every view component in the app\n"
            "- Uses Redux for global state across the signed-in experience\n"
            "- Uses Jest for running the continuous integration test suite"
        )
        out = split_long_sentences(text)
        # Bullets should remain intact; splitting would break the list.
        assert out == text


class TestBulletSoupMerge:
    def test_three_parallel_bullets_merge(self):
        text = (
            "- Uses React for rendering\n"
            "- Uses Redux for state\n"
            "- Uses Jest for tests"
        )
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        assert report.bullet_groups_merged == 1
        # One line, shared opener, comma-joined tails
        assert out.count("\n") == 0
        assert "Uses" in out
        assert "React for rendering" in out
        assert "Redux for state" in out
        assert "Jest for tests" in out

    def test_two_bullets_do_not_merge(self):
        text = "- Uses React\n- Uses Redux"
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        assert report.bullet_groups_merged == 0
        assert out == text

    def test_different_first_word_does_not_merge(self):
        text = "- Uses React\n- Uses Redux\n- Requires Node"
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        assert report.bullet_groups_merged == 0
        assert out == text

    def test_long_bullets_do_not_merge(self):
        # Each bullet is >10 words
        text = (
            "- Uses the modern React framework with hooks and suspense for rendering all components across the entire application surface\n"
            "- Uses the modern React framework with hooks and suspense for state synchronization across every mounted container element\n"
            "- Uses the modern React framework with hooks and suspense for testing integration with the platform runtime and api layer"
        )
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        assert report.bullet_groups_merged == 0
        assert out == text

    def test_mixed_markers_split_runs(self):
        text = "- Uses A\n- Uses B\n* Uses C"
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        # The first two bullets are a run of dashes; the third is a star. Neither
        # run hits min_run=3, so nothing merges.
        assert report.bullet_groups_merged == 0
        assert out == text

    def test_four_bullets_one_outlier_does_not_merge(self):
        text = (
            "- Uses React\n"
            "- Uses Redux\n"
            "- Prefers TypeScript\n"
            "- Uses Jest"
        )
        report = StructuralReport()
        out = merge_bullet_soup(text, report=report)
        # First word is not uniform; skip.
        assert report.bullet_groups_merged == 0
        assert out == text


class TestBurstinessIncreases:
    def test_split_raises_sentence_variance_on_uniform_long_input(self):
        # Four uniformly-long sentences → σ≈0. Splitting one introduces two
        # shorter sentences alongside the remaining long ones, which pushes σ up.
        long_a = (
            "The parent component re-renders on every single state change that "
            "fires inside the provider tree, propagating fresh object references "
            "to every subscribed child component registered below it in the tree."
        )
        long_b = (
            "The memoized selector sees freshly minted props every render cycle "
            "and recomputes its derived value even when the underlying data has "
            "not actually changed; the downstream tree then recomputes in lockstep."
        )
        long_c = (
            "The profiler timeline shows a visible cascade of extra renders on "
            "every mutation, so the team estimates the overhead at roughly eight "
            "milliseconds per user keystroke across this particular production path."
        )
        long_d = (
            "The engineering review concluded that wrapping every inline object "
            "prop in a memo hook would close the gap, and then the flame graph "
            "would finally drop back under the budget the platform team had set."
        )
        text = f"{long_a}\n\n{long_b}\n\n{long_c}\n\n{long_d}"
        before = _stdev(_sentence_word_counts(text))
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        after = _stdev(_sentence_word_counts(out))
        assert report.sentences_split >= 1
        assert after > before


class TestShapeGate:
    def test_varied_paragraph_untouched(self):
        # Paragraph already has wide sentence-length variance: splitting would
        # LOWER σ. Shape gate should leave it alone.
        short = "Small fix."
        long_a = (
            "The parent component re-renders on every state change that fires "
            "inside the provider tree, propagating fresh references to every "
            "subscribed child component registered below it in the tree."
        )
        mid = "The cache hit rate stayed flat across the hour."
        text = f"{long_a} {short} {mid}"
        report = StructuralReport()
        out = split_long_sentences(text, report=report)
        assert report.sentences_split == 0
        assert out == text

    def test_flat_paragraph_gets_split(self):
        long_a = (
            "The parent component re-renders on every single state change that "
            "fires inside the provider tree, propagating fresh object references "
            "to every subscribed child component registered below it in the tree."
        )
        long_b = (
            "The memoized selector sees freshly minted props every render cycle "
            "and recomputes its derived value even when the underlying data has "
            "not actually changed; the downstream tree then recomputes in lockstep."
        )
        long_c = (
            "The engineering review concluded that wrapping every inline object "
            "prop in a memo hook would close the gap, and then the flame graph "
            "would finally drop back under the budget the platform team had set."
        )
        text = f"{long_a} {long_b} {long_c}"
        report = StructuralReport()
        split_long_sentences(text, report=report)
        assert report.sentences_split >= 1


class TestCombinedPipeline:
    def test_humanize_structural_runs_both_passes(self):
        text = (
            "The parent component re-renders on every state change in the provider, "
            "propagating new references to every subscribed child; the memoized "
            "selector sees fresh props and recomputes even when values are unchanged.\n\n"
            "- Uses React\n"
            "- Uses Redux\n"
            "- Uses Jest"
        )
        report = StructuralReport()
        humanize_structural(text, report=report)
        assert report.sentences_split == 1
        assert report.bullet_groups_merged == 1
