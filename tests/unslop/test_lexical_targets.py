"""Tests for unslop/scripts/lexical_targets.py — baseline loading and gap measurement."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from unslop.scripts.lexical_targets import (
    TargetGap,
    _normalize_baseline_payload,
    apply_targeted_pass,
    load_baselines,
    measure_gaps,
)


_REPO_ROOT = Path(__file__).resolve().parents[2]
_BENCHMARK_BASELINE = _REPO_ROOT / "benchmarks" / "results" / "stylometric_baseline.json"
_PACKAGE_BASELINE = _REPO_ROOT / "unslop" / "scripts" / "data" / "stylometric_baseline.json"


def _gap(field: str, current: float, low: float, high: float) -> TargetGap:
    delta = current - low if current < low else current - high
    return TargetGap(field, current, low, high, delta)


# --- Original behavioral tests (restored from HEAD) ---


class TestMeasureGaps:
    def test_measure_gaps_reports_first_person_without_rewrite(self):
        gaps = measure_gaps(
            "The patch shipped. The tests passed.",
            {"first_person_rate": {"human_p25": 10.0, "human_p75": 20.0}},
        )
        assert gaps[0].field == "first_person_rate"
        assert gaps[0].delta < 0

    def test_returns_gaps_on_flat_text(self):
        flat = "The system works. The system runs. The system helps. " * 10
        gaps = measure_gaps(flat)
        assert isinstance(gaps, list)
        assert len(gaps) > 0, "flat repetitive text must produce at least one gap"
        assert all(isinstance(g, TargetGap) for g in gaps)

    def test_gaps_sorted_by_abs_delta(self):
        flat = "The system works. The system runs. " * 15
        gaps = measure_gaps(flat)
        assert len(gaps) >= 2, "flat text must produce multiple gaps for ordering test"
        for i in range(len(gaps) - 1):
            assert abs(gaps[i].delta) >= abs(gaps[i + 1].delta)


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


# --- Baseline loading / resource tests ---


class TestNormalizePayload:
    def test_extracts_fields_with_p25_p75(self):
        payload = {
            "fields": {
                "latinate_ratio": {
                    "human_p25": 0.04,
                    "human_median": 0.06,
                    "human_p75": 0.06,
                    "llm_p25": 0.061,
                }
            }
        }
        result = _normalize_baseline_payload(payload)
        assert "latinate_ratio" in result
        assert result["latinate_ratio"]["human_p25"] == pytest.approx(0.04)
        assert result["latinate_ratio"]["human_p75"] == pytest.approx(0.06)

    def test_skips_fields_missing_p25(self):
        payload = {"fields": {"bad": {"human_p75": 1.0}}}
        assert _normalize_baseline_payload(payload) == {}

    def test_handles_flat_dict_without_fields_key(self):
        payload = {"latinate_ratio": {"human_p25": 0.1, "human_p75": 0.2}}
        result = _normalize_baseline_payload(payload)
        assert "latinate_ratio" in result

    def test_returns_empty_on_non_dict(self):
        assert _normalize_baseline_payload({"fields": "not a dict"}) == {}


class TestLoadBaselines:
    def setup_method(self):
        load_baselines.cache_clear()

    def test_default_returns_non_empty(self):
        result = load_baselines()
        assert len(result) > 0, "default load_baselines must find the baseline JSON"

    def test_default_has_expected_fields(self):
        result = load_baselines()
        assert "latinate_ratio" in result
        assert "sentence_length_stdev" in result
        assert "type_token_ratio" in result

    def test_explicit_path_loads(self, tmp_path):
        baseline = tmp_path / "test_baseline.json"
        baseline.write_text(json.dumps({
            "fields": {"latinate_ratio": {"human_p25": 0.01, "human_p75": 0.99}}
        }), encoding="utf-8")
        result = load_baselines(str(baseline))
        assert result["latinate_ratio"]["human_p25"] == pytest.approx(0.01)

    def test_missing_path_returns_empty(self, tmp_path):
        result = load_baselines(str(tmp_path / "does_not_exist.json"))
        assert result == {}

    def test_malformed_json_returns_empty(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{not valid json", encoding="utf-8")
        result = load_baselines(str(bad))
        assert result == {}

    def test_missing_baseline_emits_diagnostic(self, tmp_path, monkeypatch, capsys):
        load_baselines.cache_clear()
        monkeypatch.setattr(
            "unslop.scripts.lexical_targets._BASELINE_PATH",
            tmp_path / "nonexistent.json",
        )
        monkeypatch.setattr(
            "unslop.scripts.lexical_targets._load_package_baseline",
            lambda: {},
        )
        result = load_baselines()
        assert result == {}
        captured = capsys.readouterr()
        assert "stylometric baseline not found" in captured.err

    def test_package_fallback_returns_non_empty(self, monkeypatch):
        """Proves the real package resource path returns non-empty data."""
        load_baselines.cache_clear()
        monkeypatch.setattr(
            "unslop.scripts.lexical_targets._BASELINE_PATH",
            Path("/nonexistent/path/stylometric_baseline.json"),
        )
        result = load_baselines()
        assert len(result) > 0, "package fallback must return baseline data"
        assert "latinate_ratio" in result


class TestPackageBaselineConsistency:
    def test_package_copy_matches_benchmark(self):
        assert _BENCHMARK_BASELINE.exists(), "benchmark baseline must exist"
        assert _PACKAGE_BASELINE.exists(), "package data baseline must exist"
        bench = json.loads(_BENCHMARK_BASELINE.read_text(encoding="utf-8"))
        pkg = json.loads(_PACKAGE_BASELINE.read_text(encoding="utf-8"))
        assert bench == pkg

    def test_package_baseline_has_development_seed_warning(self):
        pkg = json.loads(_PACKAGE_BASELINE.read_text(encoding="utf-8"))
        note = pkg.get("metadata", {}).get("note", "")
        assert "development seed corpus" in note.lower() or "development-seed" in note.lower()

    def test_no_absolute_workspace_paths(self):
        pkg = json.loads(_PACKAGE_BASELINE.read_text(encoding="utf-8"))
        raw = json.dumps(pkg)
        assert "/Users/" not in raw
        assert "/home/" not in raw
        assert "C:\\" not in raw
