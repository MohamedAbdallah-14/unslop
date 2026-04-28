#!/usr/bin/env python3
"""Compare unslop's DivEye vector with IBM/diveye when the reference repo exists."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from unslop.scripts.surprisal import SurprisalUnavailable, compute_surprisal_variance  # noqa: E402


def _load_ibm_utils(repo: Path) -> Any:
    utils_path = repo / "diveye_utils.py"
    if not utils_path.exists():
        raise FileNotFoundError(f"IBM diveye_utils.py not found at {utils_path}")
    spec = importlib.util.spec_from_file_location("ibm_diveye_utils", utils_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {utils_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.DivEyeUtils


def _relative_errors(a: list[float], b: list[float]) -> list[float]:
    errors: list[float] = []
    for left, right in zip(a, b, strict=False):
        denom = max(abs(right), 1e-9)
        errors.append(abs(left - right) / denom)
    return errors


def run_comparison(fixtures: Path, ibm_repo: Path, out: Path, model: str) -> dict[str, Any]:
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise SurprisalUnavailable(f"Missing dependency: {exc.name}") from exc

    DivEyeUtils = _load_ibm_utils(ibm_repo)
    tokenizer = AutoTokenizer.from_pretrained(model)
    lm = AutoModelForCausalLM.from_pretrained(model)
    lm.train(False)
    ibm = DivEyeUtils(lm, tokenizer)

    rows = []
    for path in sorted(fixtures.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        ours = compute_surprisal_variance(text, model=model).to_diveye_vector()
        theirs = [float(x) for x in ibm.diveye_compute(text)]
        errors = _relative_errors(ours, theirs)
        rows.append(
            {
                "fixture": path.name,
                "max_relative_error": max(errors) if errors else 0.0,
                "relative_errors": errors,
            }
        )
    payload = {"model": model, "rows": rows}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(_markdown(rows), encoding="utf-8")
    return payload


def _markdown(rows: list[dict[str, Any]]) -> str:
    lines = ["| Fixture | Max relative error |", "|---|---:|"]
    for row in rows:
        lines.append(f"| {row['fixture']} | {row['max_relative_error']:.4f} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=ROOT / "benchmarks" / "fixtures")
    parser.add_argument("--ibm-repo", type=Path, default=Path("/tmp/ibm-diveye"))
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "benchmarks" / "results" / "diveye_comparison.json",
    )
    parser.add_argument("--model", default="gpt2")
    args = parser.parse_args(argv)
    run_comparison(args.fixtures, args.ibm_repo, args.out, args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
