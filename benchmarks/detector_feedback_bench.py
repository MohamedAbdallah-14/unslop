#!/usr/bin/env python3
"""CI-safe detector feedback loop regression harness.

Default mode: mock scorer — verifies ladder order, iteration counts,
anti-detector step presence, and JSON serialization without downloading
any HF weights.

Opt-in mode (UNSLOP_RUN_DETECTOR_BENCH=1): real TMR on a 3-fixture subset.

Usage:
    python3 benchmarks/detector_feedback_bench.py           # mock mode
    UNSLOP_RUN_DETECTOR_BENCH=1 python3 benchmarks/detector_feedback_bench.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from unslop.scripts.detector import (  # noqa: E402
    DEFAULT_LADDER,
    feedback_loop,
    feedback_loop_aggressive,
)

FIXTURES_DIR = REPO_ROOT / "benchmarks" / "fixtures"
RESULTS_DIR = REPO_ROOT / "benchmarks" / "results"

MOCK_FIXTURES = [
    "ai-slop-tutorial.md",
    "flat-paragraph-bait.md",
    "academic-abstract.md",
]


def _make_mock_scorer(scores: list[float]):
    state = {"idx": 0}

    def score(_text: str) -> float:
        s = scores[state["idx"] % len(scores)]
        state["idx"] += 1
        return s

    return score


def _check(condition: bool, msg: str) -> bool:
    if not condition:
        sys.stderr.write(f"FAIL: {msg}\n")
        return False
    return True


def run_mock_bench() -> tuple[list[dict], int]:
    results = []
    errors = 0

    for fixture_name in MOCK_FIXTURES:
        fixture_path = FIXTURES_DIR / fixture_name
        if not fixture_path.exists():
            sys.stderr.write(f"SKIP: {fixture_name} not found\n")
            continue

        text = fixture_path.read_text(encoding="utf-8")

        scorer_default = _make_mock_scorer([0.95, 0.88, 0.80, 0.72, 0.65])
        result = feedback_loop(
            text,
            target_probability=0.1,
            max_iterations=4,
            score_fn=scorer_default,
        )

        entry = {"fixture": fixture_name, "mode": "default_ladder", "checks": []}

        if not _check(len(result.iterations) == 4, f"{fixture_name}: expected 4 iterations"):
            errors += 1
            entry["checks"].append("iteration_count: FAIL")
        else:
            entry["checks"].append("iteration_count: OK")

        intensities = [r.intensity for r in result.iterations]
        expected = [s[0] for s in DEFAULT_LADDER[:4]]
        if not _check(intensities == expected, f"{fixture_name}: ladder order {intensities} != {expected}"):
            errors += 1
            entry["checks"].append("ladder_order: FAIL")
        else:
            entry["checks"].append("ladder_order: OK")

        if not _check(result.iterations[-1].intensity == "anti-detector",
                       f"{fixture_name}: last step not anti-detector"):
            errors += 1
            entry["checks"].append("anti_detector_present: FAIL")
        else:
            entry["checks"].append("anti_detector_present: OK")

        d = result.to_dict()
        try:
            json.dumps(d)
            entry["checks"].append("json_serializable: OK")
        except (TypeError, ValueError) as exc:
            errors += 1
            entry["checks"].append(f"json_serializable: FAIL ({exc})")

        if not _check("ladder exhausted" in result.reason_stopped,
                       f"{fixture_name}: unexpected reason_stopped"):
            errors += 1
            entry["checks"].append("reason_stopped: FAIL")
        else:
            entry["checks"].append("reason_stopped: OK")

        entry["iterations"] = len(result.iterations)
        entry["original_probability"] = round(result.original_probability, 4)
        entry["final_probability"] = round(result.final_probability, 4)
        results.append(entry)

    scorer_aggressive = _make_mock_scorer([0.95] * 7)
    agg_text = "The team shipped. " * 20
    agg_result = feedback_loop_aggressive(
        agg_text,
        target_probability=0.1,
        score_fn=scorer_aggressive,
    )

    agg_entry = {"fixture": "<synthetic>", "mode": "aggressive_ladder", "checks": []}
    if not _check(len(agg_result.iterations) == 6, "aggressive: expected 6 iterations"):
        errors += 1
        agg_entry["checks"].append("iteration_count: FAIL")
    else:
        agg_entry["checks"].append("iteration_count: OK")

    if not _check(agg_result.iterations[0].intensity == "subtle",
                   "aggressive: first step not subtle"):
        errors += 1
        agg_entry["checks"].append("first_step: FAIL")
    else:
        agg_entry["checks"].append("first_step: OK")

    if not _check(agg_result.iterations[-1].intensity == "anti-detector",
                   "aggressive: last step not anti-detector"):
        errors += 1
        agg_entry["checks"].append("last_step: FAIL")
    else:
        agg_entry["checks"].append("last_step: OK")

    agg_entry["iterations"] = len(agg_result.iterations)
    results.append(agg_entry)

    early_scorer = _make_mock_scorer([0.95, 0.3])
    early_result = feedback_loop(
        agg_text,
        target_probability=0.5,
        score_fn=early_scorer,
    )
    early_entry = {"fixture": "<synthetic>", "mode": "early_stop", "checks": []}
    if not _check(len(early_result.iterations) == 1, "early stop: expected 1 iteration"):
        errors += 1
        early_entry["checks"].append("iteration_count: FAIL")
    else:
        early_entry["checks"].append("iteration_count: OK")

    if not _check("target hit" in early_result.reason_stopped,
                   "early stop: expected 'target hit'"):
        errors += 1
        early_entry["checks"].append("reason_stopped: FAIL")
    else:
        early_entry["checks"].append("reason_stopped: OK")

    early_entry["iterations"] = len(early_result.iterations)
    results.append(early_entry)

    return results, errors


def run_real_bench() -> tuple[list[dict], int]:
    results = []
    for fixture_name in MOCK_FIXTURES:
        fixture_path = FIXTURES_DIR / fixture_name
        if not fixture_path.exists():
            sys.stderr.write(f"SKIP: {fixture_name} not found\n")
            continue

        text = fixture_path.read_text(encoding="utf-8")
        result = feedback_loop(
            text,
            target_probability=0.5,
            max_iterations=4,
        )
        results.append({
            "fixture": fixture_name,
            "mode": "real_tmr",
            "iterations": len(result.iterations),
            "original_probability": round(result.original_probability, 4),
            "final_probability": round(result.final_probability, 4),
            "reason_stopped": result.reason_stopped,
        })
    return results, 0


def main() -> int:
    use_real = os.environ.get("UNSLOP_RUN_DETECTOR_BENCH") == "1"

    if use_real:
        sys.stdout.write("detector_feedback_bench: real TMR mode\n")
        results, errors = run_real_bench()
    else:
        sys.stdout.write("detector_feedback_bench: mock mode (CI-safe)\n")
        results, errors = run_mock_bench()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"{stamp}-feedback-loop.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "timestamp": stamp,
        "mode": "real" if use_real else "mock",
        "results": results,
        "errors": errors,
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(f"wrote {output_path}\n")

    if errors > 0:
        sys.stderr.write(f"\n{errors} check(s) failed\n")
        return 1

    sys.stdout.write(f"{len(results)} scenarios, all checks passed\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
