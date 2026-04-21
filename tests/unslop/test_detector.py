"""Tests for unslop/scripts/detector.py.

The feedback loop is tested against a MOCK score function — we don't download
HuggingFace weights in unit tests. Integration with the real TMR/Desklib
models is covered by the existing benchmarks/detector_bench.py, which is
opt-in.
"""

from __future__ import annotations

import os

import pytest

from unslop.scripts.detector import (
    DEFAULT_LADDER,
    DetectorUnavailable,
    FeedbackResult,
    IterationRecord,
    feedback_loop,
    score_ai_probability,
)


# ---------- env guard ----------


class TestEnvGuard:
    def test_skip_env_raises(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_UNSLOP_SKIP_DETECTOR", "1")
        with pytest.raises(DetectorUnavailable):
            score_ai_probability("hello world")

    def test_skip_env_unset_does_not_raise_on_attribute(self, monkeypatch):
        # Without the env var, the function tries to load the model. We can't
        # test the happy path without the model, so just check that removing
        # the guard doesn't preemptively short-circuit.
        monkeypatch.delenv("ANTHROPIC_UNSLOP_SKIP_DETECTOR", raising=False)
        # If the model isn't available, DetectorUnavailable is fine; just not
        # the "env var set" message.
        try:
            score_ai_probability("hello world")
        except DetectorUnavailable as exc:
            assert "ANTHROPIC_UNSLOP_SKIP_DETECTOR" not in str(exc)


# ---------- feedback loop ----------


def _make_mock_scorer(scores: list[float]) -> callable:
    """Return a scorer that yields `scores` in order, cycling on exhaust."""
    state = {"idx": 0}

    def score(_text: str) -> float:
        s = scores[state["idx"] % len(scores)]
        state["idx"] += 1
        return s

    return score


class TestFeedbackLoopEarlyStop:
    def test_stops_when_target_hit_at_first_iteration(self):
        # Original p=0.9 (pre-rewrite). After iteration 1: p=0.2 (below target 0.5).
        scorer = _make_mock_scorer([0.9, 0.2])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.5,
            max_iterations=3,
            score_fn=scorer,
        )
        assert isinstance(result, FeedbackResult)
        assert result.original_probability == pytest.approx(0.9)
        assert result.final_probability == pytest.approx(0.2)
        assert len(result.iterations) == 1
        assert result.iterations[0].intensity == "balanced"
        assert result.iterations[0].structural is False
        assert "target hit" in result.reason_stopped

    def test_stops_when_target_hit_at_second_iteration(self):
        # Original 0.9, after step 1: 0.7 (still above 0.5), after step 2: 0.3.
        scorer = _make_mock_scorer([0.9, 0.7, 0.3])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.5,
            max_iterations=3,
            score_fn=scorer,
        )
        assert len(result.iterations) == 2
        assert result.iterations[0].intensity == "balanced"
        assert result.iterations[1].intensity == "full"
        assert result.iterations[1].structural is False
        assert result.final_probability == pytest.approx(0.3)


class TestFeedbackLoopExhaust:
    def test_runs_all_steps_when_target_never_hit(self):
        # Probability stays high all three iterations.
        scorer = _make_mock_scorer([0.95, 0.9, 0.85, 0.8])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.3,
            max_iterations=3,
            score_fn=scorer,
        )
        assert len(result.iterations) == 3
        # The final iteration must use structural=True per DEFAULT_LADDER.
        assert result.iterations[-1].intensity == "full"
        assert result.iterations[-1].structural is True
        assert "ladder exhausted" in result.reason_stopped

    def test_respects_max_iterations_below_ladder_length(self):
        scorer = _make_mock_scorer([0.95, 0.9, 0.85])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.1,
            max_iterations=2,
            score_fn=scorer,
        )
        # Only two iterations allowed; ladder has three but we cap.
        assert len(result.iterations) == 2


class TestFeedbackLoopLadder:
    def test_escalation_order(self):
        scorer = _make_mock_scorer([0.9, 0.8, 0.7, 0.6])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.1,
            max_iterations=3,
            score_fn=scorer,
        )
        intensities = [r.intensity for r in result.iterations]
        structurals = [r.structural for r in result.iterations]
        assert intensities == ["balanced", "full", "full"]
        assert structurals == [False, False, True]

    def test_custom_ladder_respected(self):
        scorer = _make_mock_scorer([0.9, 0.5])
        custom = [("subtle", False), ("full", True)]
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.0,  # never hit
            max_iterations=5,
            score_fn=scorer,
            ladder=custom,
        )
        intensities = [r.intensity for r in result.iterations]
        assert intensities == ["subtle", "full"]


class TestFeedbackLoopSerialization:
    def test_to_dict_shape(self):
        scorer = _make_mock_scorer([0.9, 0.2])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.5,
            score_fn=scorer,
        )
        d = result.to_dict()
        assert "original_probability" in d
        assert "final_probability" in d
        assert "reduction_pct" in d
        assert "iterations" in d
        assert isinstance(d["iterations"], list)
        assert all(
            "iteration" in it and "intensity" in it and "ai_probability" in it
            for it in d["iterations"]
        )

    def test_reduction_pct_computed(self):
        scorer = _make_mock_scorer([0.8, 0.2])
        result = feedback_loop(
            "The team shipped. " * 20,
            target_probability=0.5,
            score_fn=scorer,
        )
        d = result.to_dict()
        # original 0.8, final 0.2 → reduction 60 pp.
        assert d["reduction_pct"] == 60.0


class TestDefaultLadder:
    def test_default_ladder_has_three_escalating_steps(self):
        assert len(DEFAULT_LADDER) == 3
        # Last step is full + structural.
        assert DEFAULT_LADDER[-1] == ("full", True)
        # First step is gentle.
        assert DEFAULT_LADDER[0] == ("balanced", False)


class TestIterationRecord:
    def test_record_fields(self):
        r = IterationRecord(
            iteration=1,
            intensity="balanced",
            structural=False,
            ai_probability=0.42,
            ai_isms_after=3,
        )
        assert r.iteration == 1
        assert r.intensity == "balanced"
        assert r.structural is False
        assert r.ai_probability == 0.42
        assert r.ai_isms_after == 3
