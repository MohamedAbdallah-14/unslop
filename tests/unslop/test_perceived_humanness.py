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


class TestHarness:
    def test_run_with_mocked_judge_hum_always_wins(self, tmp_path, monkeypatch):
        # Create one fixture
        fixture = tmp_path / "t.md"
        fixture.write_text(
            "It is a pivotal moment in the industry. This marks a testament "
            "to the hard work of every engineer on the team."
        )
        # Mock: judge always picks the humanized one regardless of A/B
        def fake_judge(passage_a, passage_b, model):
            # Decide based on which side has fewer AI-isms (proxy for humanized).
            if "pivotal moment" in passage_a or "testament" in passage_a:
                return "B", "B less inflated"
            return "A", "A less inflated"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=3,
            seed=1,
        )
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
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=2,
            seed=1,
        )
        assert report["totals"]["humanized_wins"] == 0
        assert report["totals"]["ties"] == 2

    def test_run_deterministic_with_seed(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment. Stands as a testament.")

        recorded_a_was: list[str] = []

        def fake_judge(a, b, model):
            # Record which side was humanized each time.
            if "pivotal" in a:
                recorded_a_was.append("original")
            else:
                recorded_a_was.append("humanized")
            return "A", "fine"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=5,
            seed=42,
        )
        run1 = list(recorded_a_was)

        recorded_a_was.clear()
        ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=5,
            seed=42,
        )
        run2 = list(recorded_a_was)
        assert run1 == run2

    def test_humanized_won_logic(self, tmp_path, monkeypatch):
        fixture = tmp_path / "t.md"
        fixture.write_text("It is a pivotal moment in the industry.")

        # Judge picks A. Whether humanized won depends on whether A was humanized.
        def fake_judge(a, b, model):
            return "A", "picked A"

        monkeypatch.setattr(ph, "_judge", fake_judge)
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=10,
            seed=7,
        )
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
        report = ph.run(
            tmp_path,
            intensity="balanced",
            structural=False,
            soul=False,
            judge_model="mock",
            runs=4,
            seed=1,
        )
        assert report["totals"]["invalid"] == 4
        assert report["totals"]["humanized_wins"] == 0
        assert report["totals"]["original_wins"] == 0
