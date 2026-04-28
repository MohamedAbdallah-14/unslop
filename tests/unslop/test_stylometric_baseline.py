from __future__ import annotations

import json
from pathlib import Path

from benchmarks.stylometric_baseline import build_baseline, main


def _write_samples(path: Path, prefix: str) -> None:
    path.mkdir()
    for i in range(3):
        (path / f"{prefix}-{i}.md").write_text(
            (
                f"{prefix} sample {i}. We don't make every sentence the same. "
                "Short. Then a longer sentence with enough ordinary glue words "
                "to give the profile some shape."
            ),
            encoding="utf-8",
        )


def test_stylometric_baseline_runs(tmp_path: Path):
    human = tmp_path / "human"
    llm = tmp_path / "llm"
    _write_samples(human, "human")
    _write_samples(llm, "llm")
    out = tmp_path / "baseline.json"

    rc = main(["--human", str(human), "--llm", str(llm), "--out", str(out)])

    assert rc == 0
    payload = json.loads(out.read_text())
    assert payload["metadata"]["n_human"] == 3
    assert payload["metadata"]["n_llm"] == 3
    assert "function_word_rate" in payload["fields"]


def test_build_baseline_schema(tmp_path: Path):
    human = tmp_path / "human"
    llm = tmp_path / "llm"
    _write_samples(human, "human")
    _write_samples(llm, "llm")

    payload = build_baseline(human, llm)

    stats = payload["fields"]["type_token_ratio"]
    assert {"human_p25", "human_median", "human_p75", "llm_median"}.issubset(stats)
