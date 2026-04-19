#!/usr/bin/env python3
"""Offline benchmark runner for the deterministic humanizer.

Usage:
  python3 benchmarks/run.py [--fixtures benchmarks/fixtures]
                            [--out benchmarks/results]
                            [--strict]

Writes a JSON report per run and updates `latest.json` for CI diffing.
`--strict` exits non-zero if the humanizer made any fixture worse or broke
preservation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "humanizer-humanize"))

from scripts.humanize import humanize_deterministic  # noqa: E402
from scripts.validate import AI_ISM_PATTERNS, validate  # noqa: E402

WORD = re.compile(r"\w+")


def count_ai_isms(text: str) -> int:
    return sum(len(p.findall(text)) for p in AI_ISM_PATTERNS)


def run(fixtures_dir: Path) -> dict:
    results = []
    for md in sorted(fixtures_dir.glob("*.md")):
        original = md.read_text()
        humanized = humanize_deterministic(original)
        report = validate(original, humanized)
        results.append(
            {
                "file": md.name,
                "words_before": len(WORD.findall(original)),
                "words_after": len(WORD.findall(humanized)),
                "ai_isms_before": count_ai_isms(original),
                "ai_isms_after": count_ai_isms(humanized),
                "delta": count_ai_isms(original) - count_ai_isms(humanized),
                "structural_ok": report.ok,
                "structural_errors": report.errors,
            }
        )
    total_before = sum(r["ai_isms_before"] for r in results)
    total_after = sum(r["ai_isms_after"] for r in results)
    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "fixture_count": len(results),
        "total_ai_isms_before": total_before,
        "total_ai_isms_after": total_after,
        "total_delta": total_before - total_after,
        "percent_reduced": (
            round((total_before - total_after) / total_before * 100, 1) if total_before else 0.0
        ),
        "fixtures": results,
    }


def print_report(report: dict) -> None:
    print("Humanizer benchmark\n===================\n")
    print(f"Fixtures:            {report['fixture_count']}")
    print(f"AI-isms before:      {report['total_ai_isms_before']}")
    print(f"AI-isms after:       {report['total_ai_isms_after']}")
    print(f"Delta (stripped):    {report['total_delta']}")
    print(f"% reduction:         {report['percent_reduced']}%\n")
    print(f"{'file':<40}{'before':>10}{'after':>8}{'delta':>8}  struct")
    for f in report["fixtures"]:
        tag = "ok" if f["structural_ok"] else "FAIL"
        print(
            f"{f['file']:<40}"
            f"{f['ai_isms_before']:>10}"
            f"{f['ai_isms_after']:>8}"
            f"{f['delta']:>8}  {tag}"
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", default=str(ROOT / "benchmarks/fixtures"))
    p.add_argument("--out", default=str(ROOT / "benchmarks/results"))
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"No fixtures dir: {fixtures}", file=sys.stderr)
        return 1

    report = run(fixtures)
    print_report(report)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = out_dir / f"{report['timestamp']}.json"
    stamp_file.write_text(json.dumps(report, indent=2) + "\n")
    (out_dir / "latest.json").write_text(json.dumps(report, indent=2) + "\n")

    if args.strict:
        regressions = [f for f in report["fixtures"] if f["delta"] < 0 or not f["structural_ok"]]
        if regressions:
            print("\nREGRESSIONS:", file=sys.stderr)
            for r in regressions:
                print(f"  - {r['file']}: delta={r['delta']} struct_ok={r['structural_ok']}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
