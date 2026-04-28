from __future__ import annotations

from unslop.scripts.lexical_targets import TargetGap, apply_targeted_pass, measure_gaps


def _gap(field: str, current: float, low: float, high: float) -> TargetGap:
    delta = current - low if current < low else current - high
    return TargetGap(field, current, low, high, delta)


class TestMeasureGaps:
    def test_measure_gaps_reports_first_person_without_rewrite(self):
        gaps = measure_gaps(
            "The patch shipped. The tests passed.",
            {"first_person_rate": {"human_p25": 10.0, "human_p75": 20.0}},
        )
        assert gaps[0].field == "first_person_rate"
        assert gaps[0].delta < 0


class TestTargetedPass:
    def test_function_word_injection_safe(self):
        text = "Cats sleep mats"
        out = apply_targeted_pass(
            text,
            [_gap("function_word_rate", 0.1, 0.4, 0.6)],
            intensity="full",
        )
        assert out == "Cats sleep on mats"

    def test_function_word_injection_skips_protected(self):
        text = "```txt\nCats sleep mats\n```\n\nCats sleep mats"
        out = apply_targeted_pass(
            text,
            [_gap("function_word_rate", 0.1, 0.4, 0.6)],
            intensity="full",
        )
        assert "```txt\nCats sleep mats\n```" in out
        assert out.endswith("Cats sleep on mats")

    def test_function_word_cap_at_5pct(self):
        text = " ".join(["Cats sleep mats."] * 40)
        out = apply_targeted_pass(
            text,
            [_gap("function_word_rate", 0.1, 0.4, 0.6)],
            intensity="full",
        )
        assert out.count("sleep on mats") <= 6

    def test_latinate_to_anglo_swap(self):
        out = apply_targeted_pass(
            "We utilize the framework and ascertain the state.",
            [_gap("latinate_ratio", 0.2, 0.0, 0.1)],
            intensity="balanced",
        )
        assert "use the framework" in out
        assert "figure out the state" in out

    def test_latinate_skipped_in_technical(self):
        out = apply_targeted_pass(
            "The utility class stays.",
            [_gap("latinate_ratio", 0.2, 0.0, 0.1)],
            intensity="balanced",
        )
        assert out == "The utility class stays."

    def test_diversity_dampener_keeps_repeat(self):
        text = "We showcase the API, highlight the API, and emphasize the API."
        out = apply_targeted_pass(
            text,
            [_gap("type_token_ratio", 0.95, 0.3, 0.7)],
            intensity="full",
        )
        assert "highlight" not in out.lower()
        assert "emphasize" not in out.lower()

    def test_first_person_no_auto_inject(self):
        text = "The patch shipped. The tests passed."
        out = apply_targeted_pass(
            text,
            [_gap("first_person_rate", 0.0, 5.0, 20.0)],
            intensity="full",
        )
        assert out == text

    def test_intensity_gating(self):
        text = "We utilize the framework. Cats sleep mats."
        gaps = [
            _gap("latinate_ratio", 0.2, 0.0, 0.1),
            _gap("function_word_rate", 0.1, 0.4, 0.6),
        ]
        assert apply_targeted_pass(text, gaps, intensity="subtle") == text
        balanced = apply_targeted_pass(text, gaps, intensity="balanced")
        full = apply_targeted_pass(text, gaps, intensity="full")
        assert "use the framework" in balanced
        assert "sleep on mats" not in balanced
        assert "sleep on mats" in full
