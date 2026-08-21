from __future__ import annotations

from pathlib import Path

from benchmarks import detector_feedback_bench as feedback_bench
from benchmarks.adversarial_paraphrasing_comparison import run as adv_run
from benchmarks.diveye_comparison import run as diveye_run


def test_diveye_comparison_relative_errors():
    errors = diveye_run._relative_errors([1.0, 2.0], [1.0, 4.0])
    assert errors == [0.0, 0.5]


def test_adv_paraphrase_markdown_runs():
    rows = [
        {
            "fixture": "sample.md",
            "original_probability": 0.9,
            "unslop_probability": 0.5,
            "external_probability": 0.4,
        }
    ]
    out = adv_run._markdown(rows)
    assert "sample.md" in out
    assert "0.900" in out


def test_adv_external_subprocess_mock(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "paraphrase_and_detect.py").write_text("placeholder", encoding="utf-8")

    class Completed:
        returncode = 0
        stdout = "rewritten"
        stderr = ""

    monkeypatch.setattr(adv_run.subprocess, "run", lambda *a, **kw: Completed())
    assert adv_run._run_external(repo, "input") == "rewritten"


def test_feedback_mock_bench_fails_when_fixture_is_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(feedback_bench, "FIXTURES_DIR", tmp_path)
    monkeypatch.setattr(feedback_bench, "MOCK_FIXTURES", ["missing.md"])

    results, errors = feedback_bench.run_mock_bench()

    assert errors == 1
    assert results[0]["checks"] == ["fixture_present: FAIL"]


def test_feedback_real_bench_fails_when_fixture_is_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(feedback_bench, "FIXTURES_DIR", tmp_path)
    monkeypatch.setattr(feedback_bench, "MOCK_FIXTURES", ["missing.md"])

    results, errors = feedback_bench.run_real_bench()

    assert errors == 1
    assert results == [
        {
            "fixture": "missing.md",
            "mode": "real_tmr",
            "checks": ["fixture_present: FAIL"],
        }
    ]
