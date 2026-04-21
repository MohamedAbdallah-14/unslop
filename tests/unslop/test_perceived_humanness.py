"""Tests for evals/perceived_humanness.py.

Judge calls are mocked — no API credits burned in unit tests. Integration
with the real Claude/OpenAI judges is covered by running the harness
manually.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "evals"))

import perceived_humanness as ph  # noqa: E402


class TestParseChoice:
    def test_clean_a(self):
        reply = "A\nA reads more like a human; it uses contractions."
        choice, rationale = ph._parse_choice(reply)
        assert choice == "A"
        assert "contractions" in rationale

    def test_clean_b(self):
        reply = "B\nB avoids the five-paragraph shape."
        choice, rationale = ph._parse_choice(reply)
        assert choice == "B"
        assert "five-paragraph" in rationale

    def test_tie(self):
        reply = "TIE\nBoth read similarly flat."
        choice, rationale = ph._parse_choice(reply)
        assert choice == "TIE"

    def test_lowercase_tie(self):
        reply = "tie\nBoth feel AI."
        choice, rationale = ph._parse_choice(reply)
        assert choice == "TIE"

    def test_unparseable_returns_question(self):
        reply = "Hmm I'm not sure which is which really"
        choice, rationale = ph._parse_choice(reply)
        assert choice == "?"
        assert rationale.startswith("Hmm")

    def test_a_with_trailing_punctuation(self):
        reply = "A.\nPassage A uses concrete tool names."
        choice, rationale = ph._parse_choice(reply)
        assert choice == "A"


def _run_single_judge(tmp_path, **kwargs):
    """Test helper: mirror the old single-judge `run()` signature."""
    defaults = dict(
        intensity="balanced",
        structural=False,
        soul=False,
        judges=["mock"],
        counterbalance=False,
        seed=1,
    )
    defaults.update(kwargs)
    return ph.run(tmp_path, **defaults)


class TestHarness:
    def test_run_with_mocked_judge_hum_always_wins(self, tmp_path, monkeypatch):
        # Create one fixture
        fixture = tmp_path / "t.md"
        fixture.write_text(
            "It is a pivotal moment in the industry. This marks a testament "
            "to the hard work of every engineer on the team."
        )

        def fake_judge(passage_a, passage_b, model):
            # Decide based on which side has fewer AI-isms (proxy for humanized).
            if "pivotal moment" in passage_a or "testament" in passage_a:
                return "B", "B less inflated"
            return "A", "A less inflated"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = _run_single_judge(tmp_path, runs=3)
        totals = report["totals"]
        assert totals["humanized_wins"] == 3
        assert totals["original_wins"] == 0
        assert totals["win_rate_pct"] == 100.0

    def test_run_handles_tie(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("Short sample.")

        def fake_judge(a, b, model):
            return "TIE", "both short"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = _run_single_judge(tmp_path, runs=2)
        assert report["totals"]["humanized_wins"] == 0
        assert report["totals"]["ties"] == 2

    def test_run_deterministic_with_seed(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment. Stands as a testament.")

        recorded_a_was: list[str] = []

        def fake_judge(a, b, model):
            if "pivotal" in a:
                recorded_a_was.append("original")
            else:
                recorded_a_was.append("humanized")
            return "A", "fine"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        _run_single_judge(tmp_path, runs=5, seed=42)
        run1 = list(recorded_a_was)

        recorded_a_was.clear()
        _run_single_judge(tmp_path, runs=5, seed=42)
        run2 = list(recorded_a_was)
        assert run1 == run2

    def test_humanized_won_logic(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment in the industry.")

        def fake_judge(a, b, model):
            return "A", "picked A"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = _run_single_judge(tmp_path, runs=10, seed=7)
        votes = report["fixtures"][0]["votes"]
        for v in votes:
            if v["a_was"] == "humanized":
                assert v["humanized_won"] is True
            else:
                assert v["humanized_won"] is False


class TestInvalidCounted:
    def test_invalid_counts_separately(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("Sample.")

        def fake_judge(a, b, model):
            return "?", "judge confused"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = _run_single_judge(tmp_path, runs=4)
        assert report["totals"]["invalid"] == 4
        assert report["totals"]["humanized_wins"] == 0
        assert report["totals"]["original_wins"] == 0


class TestCounterbalance:
    def test_counterbalance_doubles_votes_per_run(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment in the industry.")

        def fake_judge(a, b, model):
            # Always prefer whichever side has fewer AI-isms
            return ("B" if "pivotal" in a else "A"), "inflated wins lose"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judges=["mock"],
            counterbalance=True,
            runs=2,
            seed=1,
        )
        # 2 runs × 2 orientations = 4 votes per fixture
        assert len(report["fixtures"][0]["votes"]) == 4

    def test_multi_judge_jury_reports_per_judge(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment in the industry.")

        def fake_judge(a, b, model):
            # Judge A always picks humanized, judge B always picks original.
            if model == "judgeA":
                return ("B" if "pivotal" in a else "A"), "ok"
            return ("A" if "pivotal" in a else "B"), "inflated wins"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judges=["judgeA", "judgeB"],
            counterbalance=False,
            runs=1,
            seed=1,
        )
        assert "judgeA" in report["per_judge"]
        assert "judgeB" in report["per_judge"]
        assert report["per_judge"]["judgeA"]["humanized_wins"] == 1
        assert report["per_judge"]["judgeB"]["humanized_wins"] == 0

    def test_all_judges_unavailable_raises(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("Short.")

        def fake_judge(a, b, model):
            raise ph.JudgeUnavailable(f"mock: {model} down")

        monkeypatch.setattr(ph, "_judge", fake_judge)
        with pytest.raises(ph.JudgeUnavailable):
            ph.run(
                tmp_path,
                intensity="balanced",
                structural=False,
                soul=False,
                judges=["down"],
                counterbalance=False,
                runs=1,
                seed=1,
            )

    def test_bias_notes_present(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("Sample text.")

        def fake_judge(a, b, model):
            return "TIE", "both ok"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = _run_single_judge(tmp_path, runs=1)
        assert "bias_notes" in report
        bias = report["bias_notes"]
        assert bias["position_inconsistency_pct"] == 40
        assert bias["verbosity_inflation_pct"] == 15
        assert bias["self_enhancement_pct_range"] == [5, 7]
        assert len(bias["references"]) == 3
