#!/usr/bin/env python3
"""Compare the latest benchmark run against a pinned baseline, fail on regression.

Runs after benchmarks/run.py. Reads benchmarks/results/latest.json, compares
against benchmarks/results/baselines/<baseline>.json (default: most recent
post-phase*.json), and exits non-zero if any tolerance is breached.

Tolerances (generous enough to absorb small edits, tight enough to catch real
regressions):

  - AI-ism percent-reduction: must not drop by more than 2 percentage points.
    Example: baseline 89.1% → latest 86.8% (fail at <87.1%).
  - Flat-paragraph total across all fixtures: must not rise by more than 2.
    Example: baseline 13 → latest 16 (fail at >15).
  - Structural preservation: any fixture with structural_ok=False fails.
  - Sentences-split + bullet-groups-merged: informational, not gated. Shifts
    are expected as rules evolve.

Usage:
  python3 benchmarks/check_regression.py
  python3 benchmarks/check_regression.py --baseline post-phase6-20260421.json
  python3 benchmarks/check_regression.py --ai-ism-tolerance 1.0

Exit codes:
  0 — no regression
  1 — usage error (baseline missing, latest missing)
  2 — regression detected

Used by the GitHub Actions workflow to gate PRs; can also be run locally
before pushing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "benchmarks" / "results"
BASELINES = RESULTS / "baselines"


def _load_json(path: Path) -> dict:
    if not path.exists():
        print(f"Missing file: {path}", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(path.read_text())


def _pick_default_baseline() -> Path:
    """Most recent post-phase*.json baseline by mtime."""
    candidates = sorted(
        BASELINES.glob("post-phase*.json"), key=lambda p: p.stat().st_mtime
    )
    if not candidates:
        print(
            f"No post-phase*.json baselines in {BASELINES}. "
            "Run benchmarks/run.py and `cp latest.json baselines/post-phaseN-YYYYMMDD.json`.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return candidates[-1]


def compare(baseline: dict, latest: dict, *, ai_ism_tolerance: float, flat_tolerance: int) -> list[str]:
    """Return a list of human-readable regression strings. Empty = all clean."""
    errors: list[str] = []

    b_reduction = baseline.get("percent_reduced", 0.0)
    l_reduction = latest.get("percent_reduced", 0.0)
    if b_reduction - l_reduction > ai_ism_tolerance:
        errors.append(
            f"AI-ism reduction dropped: {b_reduction:.1f}% → {l_reduction:.1f}% "
            f"(tolerance: -{ai_ism_tolerance:.1f}pp)"
        )

    b_flat = sum(f.get("flat_paragraphs_after", 0) for f in baseline.get("fixtures", []))
    l_flat = sum(f.get("flat_paragraphs_after", 0) for f in latest.get("fixtures", []))
    if l_flat - b_flat > flat_tolerance:
        errors.append(
            f"Flat-paragraph total rose: {b_flat} → {l_flat} "
            f"(tolerance: +{flat_tolerance})"
        )

    for f in latest.get("fixtures", []):
        if not f.get("structural_ok", True):
            errors.append(
                f"Structural preservation broke on {f['file']}: {f.get('structural_errors', [])}"
            )

    # Per-fixture AI-ism regression: any fixture that had AI-isms stripped in
    # baseline and now has MORE after than baseline — a silent leak of stock
    # vocab or other patterns.
    b_by_file = {f["file"]: f for f in baseline.get("fixtures", [])}
    for f in latest.get("fixtures", []):
        name = f["file"]
        base = b_by_file.get(name)
        if base is None:
            continue
        if f.get("ai_isms_after", 0) > base.get("ai_isms_after", 0):
            errors.append(
                f"AI-ism residual grew on {name}: "
                f"{base['ai_isms_after']} → {f['ai_isms_after']}"
            )

    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--baseline",
        default=None,
        help="Baseline JSON filename under benchmarks/results/baselines/. "
        "Default: newest post-phase*.json.",
    )
    p.add_argument(
        "--latest",
        default=str(RESULTS / "latest.json"),
        help="Latest benchmark JSON. Default: benchmarks/results/latest.json.",
    )
    p.add_argument(
        "--ai-ism-tolerance",
        type=float,
        default=2.0,
        help="Max allowed drop in AI-ism percent-reduction, in percentage points.",
    )
    p.add_argument(
        "--flat-tolerance",
        type=int,
        default=2,
        help="Max allowed rise in total flat-paragraph count across suite.",
    )
    args = p.parse_args()

    baseline_path = (
        BASELINES / args.baseline if args.baseline else _pick_default_baseline()
    )
    latest_path = Path(args.latest)

    baseline = _load_json(baseline_path)
    latest = _load_json(latest_path)

    print(f"Baseline: {baseline_path.name}  ({baseline.get('timestamp', '?')})")
    print(f"Latest:   {latest_path.name}    ({latest.get('timestamp', '?')})\n")

    errors = compare(
        baseline,
        latest,
        ai_ism_tolerance=args.ai_ism_tolerance,
        flat_tolerance=args.flat_tolerance,
    )

    if not errors:
        print("No regression detected.")
        print(
            f"  AI-ism reduction: {latest.get('percent_reduced', 0.0):.1f}% "
            f"(baseline {baseline.get('percent_reduced', 0.0):.1f}%)"
        )
        return 0

    print("REGRESSION DETECTED:", file=sys.stderr)
    for err in errors:
        print(f"  - {err}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
