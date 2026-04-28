"""Tests for contraction-rate detection in unslop/scripts/validate.py.

The `_CONTRACTION_RE` comment was updated in this PR to remove a broken arXiv
citation (2604.11687 / "Kalemaj et al." resolved to an unrelated paper).
The threshold is now annotated as empirical. These tests pin the observed
behaviour so a future comment-or-code edit stays honest.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "unslop"))

from scripts.validate import _contraction_rate  # noqa: E402


# ---------------------------------------------------------------------------
# Basic _contraction_rate() behaviour
# ---------------------------------------------------------------------------


class TestContractionRate:
    def test_returns_zero_for_short_text(self):
        # Text with fewer than 20 words always returns 0.0 (guard in code).
        assert _contraction_rate("Don't") == 0.0

    def test_returns_zero_for_no_contractions(self):
        # AI-generated text often has zero contractions; this is the "near-zero"
        # case described in the updated comment.
        text = " ".join(["The system processes requests efficiently."] * 5)
        assert _contraction_rate(text) == 0.0

    def test_nonzero_for_text_with_contractions(self):
        # Human-like text with contractions should produce a positive rate.
        text = (
            "You'll find the config in the settings file. It's not obvious — "
            "I missed it the first time. We use YAML because the legacy tooling "
            "can't parse JSON5. There's a migration underway but I wouldn't hold "
            "my breath. We'd prefer TOML honestly. But the migration cost is real "
            "and nobody has volunteered. So YAML it is."
        )
        rate = _contraction_rate(text)
        assert rate > 0.0

    def test_rate_is_per_1000_words(self):
        # With exactly one contraction in a 100-word text, rate = 10.0 per 1k.
        # Build ~100 words with exactly one "don't".
        filler = "The cat sat on the mat " * 16  # 96 words
        text = "Don't do that. " + filler
        rate = _contraction_rate(text)
        # 1 contraction / ~100 words * 1000 ≈ 10
        assert 5.0 < rate < 20.0

    def test_negation_contractions_detected(self):
        negations = [
            "We don't ship on Fridays.",
            "The system doesn't retry requests.",
            "I didn't see the error coming.",
            "It won't fit in the budget.",
            "You shouldn't skip the tests.",
            "It couldn't be simpler.",
        ]
        # Build text long enough (>20 words) by repeating and mixing.
        text = " ".join(negations * 4)
        rate = _contraction_rate(text)
        assert rate > 0.0

    def test_copula_contractions_detected(self):
        # it's, that's, there's, he's, she's, we're, they're
        text = (
            "It's a common problem. That's the root cause. There's a simpler "
            "fix. He's the one who noticed. She's on the team. We're shipping "
            "next week. They're already aware. " * 3
        )
        rate = _contraction_rate(text)
        assert rate > 0.0

    def test_im_contraction_detected(self):
        text = ("I'm not sure about this approach. " * 8)
        rate = _contraction_rate(text)
        assert rate > 0.0

    def test_code_blocks_excluded(self):
        # Contractions inside fenced code blocks should not inflate the rate.
        code_heavy = (
            "```python\n"
            "# don't call this directly\n"
            "# it's not thread-safe\n"
            "def foo(): pass\n"
            "```\n"
        ) * 5
        # Prose has no contractions.
        text = code_heavy + "The system processes requests efficiently. " * 5
        rate = _contraction_rate(text)
        # Should be near zero because prose has no contractions.
        assert rate == pytest.approx(0.0, abs=5.0)

    def test_rate_increases_with_more_contractions(self):
        # More contractions in same-length text → higher rate.
        few = ("The system works well and processes data correctly. " * 5 +
               "It's done.")
        many = ("It's a problem. We're stuck. I'm not sure. They're waiting. " * 5)
        rate_few = _contraction_rate(few)
        rate_many = _contraction_rate(many)
        assert rate_many > rate_few

    def test_empty_string_returns_zero(self):
        assert _contraction_rate("") == 0.0

    def test_boundary_exactly_20_words(self):
        # Exactly 20 words: should compute a real rate (boundary ≥ 20).
        # 19 filler words + 1 contraction
        text = "word " * 19 + "don't"
        # 20 words, exactly at the threshold: code is `if words < 20: return 0.0`
        # so 20 words should NOT return 0.0 if there's a contraction.
        rate = _contraction_rate(text)
        assert rate > 0.0

    def test_19_words_returns_zero(self):
        text = "word " * 18 + "don't"
        # 19 words → below threshold → 0.0
        assert _contraction_rate(text) == 0.0
