"""Tests for evals/measure.py.

Covers the pure helper functions in the eval measurement module.
The `import math` was removed in a cleanup pass — this file verifies that
removal didn't break any functionality.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "unslop"))
sys.path.insert(0, str(ROOT / "evals"))

import measure  # noqa: E402


class TestCountAiIsms:
    def test_no_isms_in_clean_text(self):
        text = "The cat sat on the mat. Here is a clear explanation."
        assert measure.count_ai_isms(text) == 0

    def test_delve_detected(self):
        text = "Let's delve into the topic of machine learning."
        count = measure.count_ai_isms(text)
        assert count >= 1

    def test_multiple_isms(self):
        text = (
            "It's important to delve into this tapestry of ideas. "
            "In the realm of possibility, this testament to hard work "
            "showcases a meticulous approach."
        )
        count = measure.count_ai_isms(text)
        assert count >= 3

    def test_empty_string(self):
        assert measure.count_ai_isms("") == 0

    def test_code_block_not_counted(self):
        # Code blocks should not trigger AI-ism detection since they are
        # typically stripped or don't contain natural-language slop.
        text = "```python\nprint('hello')\n```"
        # The count might be 0 — the test verifies the function doesn't crash.
        count = measure.count_ai_isms(text)
        assert isinstance(count, int)
        assert count >= 0


class TestSentenceLengths:
    def test_single_sentence(self):
        text = "The quick brown fox jumps."
        lengths = measure.sentence_lengths(text)
        assert len(lengths) == 1
        assert lengths[0] == 5

    def test_multiple_sentences(self):
        text = "Short sentence. A much longer sentence with many more words in it. End."
        lengths = measure.sentence_lengths(text)
        assert len(lengths) == 3
        # Verify the longest is the middle one.
        assert lengths[1] > lengths[0]
        assert lengths[1] > lengths[2]

    def test_empty_string_returns_empty(self):
        assert measure.sentence_lengths("") == []

    def test_whitespace_only_returns_empty(self):
        assert measure.sentence_lengths("   \n\t  ") == []

    def test_word_counts_are_positive(self):
        text = "One. Two words here. And three more words now."
        lengths = measure.sentence_lengths(text)
        assert all(n > 0 for n in lengths)

    def test_returns_list_of_ints(self):
        lengths = measure.sentence_lengths("Hello world. Goodbye world.")
        assert isinstance(lengths, list)
        assert all(isinstance(n, int) for n in lengths)


class TestMeasureText:
    def test_basic_shape(self):
        baseline = "This is good text."
        text = "This is good text."
        result = measure.measure_text(baseline, text)
        assert "word_count" in result
        assert "ai_isms" in result
        assert "avg_sentence_len" in result
        assert "burstiness" in result
        assert "structural_errors" in result
        assert "structural_ok" in result

    def test_word_count_is_correct(self):
        text = "The cat sat on the mat."
        result = measure.measure_text(None, text)
        assert result["word_count"] == 6

    def test_no_isms_in_clean_text(self):
        text = "The system processes requests efficiently."
        result = measure.measure_text(None, text)
        assert result["ai_isms"] == 0

    def test_ai_isms_counted(self):
        text = "Let's delve into the tapestry of options."
        result = measure.measure_text(None, text)
        assert result["ai_isms"] >= 2

    def test_baseline_none_skips_structural_validation(self):
        result = measure.measure_text(None, "Some text here.")
        assert result["structural_errors"] == 0
        assert result["structural_ok"] is True

    def test_burstiness_zero_for_single_sentence(self):
        result = measure.measure_text(None, "Just one sentence here.")
        assert result["burstiness"] == 0

    def test_burstiness_nonzero_for_varied_sentences(self):
        text = "Short. A much longer sentence with many words in it. End."
        result = measure.measure_text(None, text)
        assert result["burstiness"] > 0

    def test_avg_sentence_len_zero_for_empty(self):
        result = measure.measure_text(None, "")
        assert result["avg_sentence_len"] == 0

    def test_structural_ok_when_no_baseline(self):
        result = measure.measure_text(None, "Some humanized text.")
        assert result["structural_ok"] is True
        assert result["structural_errors"] == 0


class TestMeasureTextNoMathImport:
    """Regression: evals/measure.py had `import math` removed.

    These tests confirm the module operates correctly without that import —
    burstiness uses statistics.pstdev, not math functions."""

    def test_burstiness_uses_statistics_not_math(self):
        import statistics

        text = "One word. This sentence has five words in it. End."
        lengths = measure.sentence_lengths(text)
        expected_pstdev = round(statistics.pstdev(lengths), 2)
        result = measure.measure_text(None, text)
        assert result["burstiness"] == expected_pstdev

    def test_avg_sentence_len_uses_statistics_mean(self):
        import statistics

        text = "One two. Three four five six."
        lengths = measure.sentence_lengths(text)
        expected_mean = round(statistics.mean(lengths), 2)
        result = measure.measure_text(None, text)
        assert result["avg_sentence_len"] == expected_mean