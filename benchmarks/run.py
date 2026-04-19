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

from scripts.humanize import VALID_INTENSITIES, humanize_deterministic  # noqa: E402
from scripts.validate import AI_ISM_PATTERNS, _sentence_lengths, validate  # noqa: E402

WORD = re.compile(r"\w+")


def count_ai_isms(text: str) -> int:
    return sum(len(p.findall(text)) for p in AI_ISM_PATTERNS)


def run(fixtures_dir: Path, intensity: str = "balanced") -> dict:
    results = []
    for md in sorted(fixtures_dir.glob("*.md")):
        original = md.read_text()
        humanized = humanize_deterministic(original, intensity=intensity)  # type: ignore[arg-type]
        report = validate(original, humanized)
        orig_sentence_lengths = _sentence_lengths(original)
        new_sentence_lengths = _sentence_lengths(humanized)
        results.append(
            {
                "file": md.name,
                "words_before": len(WORD.findall(original)),
                "words_after": len(WORD.findall(humanized)),
                "sentence_count_before": len(orig_sentence_lengths),
                "sentence_count_after": len(new_sentence_lengths),
                "ai_isms_before": count_ai_isms(original),
                "ai_isms_after": count_ai_isms(humanized),
                "delta": count_ai_isms(original) - count_ai_isms(humanized),
                "burstiness_before": round(report.burstiness_before, 2),
                "burstiness_after": round(report.burstiness_after, 2),
                "burstiness_delta": round(
                    report.burstiness_after - report.burstiness_before, 2
                ),
                "structural_ok": report.ok,
                "structural_errors": report.errors,
                "warnings": report.warnings,
            }
        )
    total_before = sum(r["ai_isms_before"] for r in results)
    total_after = sum(r["ai_isms_after"] for r in results)
    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "intensity": intensity,
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
    if "intensity" in report:
        print(f"Intensity:           {report['intensity']}")
    print(f"Fixtures:            {report['fixture_count']}")
    print(f"AI-isms before:      {report['total_ai_isms_before']}")
    print(f"AI-isms after:       {report['total_ai_isms_after']}")
    print(f"Delta (stripped):    {report['total_delta']}")
    print(f"% reduction:         {report['percent_reduced']}%\n")
    print(f"{'file':<40}{'before':>10}{'after':>8}{'delta':>8}{'σ':>12}  struct")
    for f in report["fixtures"]:
        tag = "ok" if f["structural_ok"] else "FAIL"
        sigma = f"{f['burstiness_before']:.1f}->{f['burstiness_after']:.1f}"
        print(
            f"{f['file']:<40}"
            f"{f['ai_isms_before']:>10}"
            f"{f['ai_isms_after']:>8}"
            f"{f['delta']:>8}"
            f"{sigma:>12}  {tag}"
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", default=str(ROOT / "benchmarks/fixtures"))
    p.add_argument("--out", default=str(ROOT / "benchmarks/results"))
    p.add_argument("--strict", action="store_true")
    p.add_argument(
        "--intensity",
        "-m",
        choices=list(VALID_INTENSITIES),
        default="balanced",
        help="Intensity level to benchmark. Default: balanced.",
    )
    p.add_argument(
        "--all-intensities",
        action="store_true",
        help="Run the benchmark across subtle, balanced, and full. Useful for "
        "checking that higher intensity strips strictly more AI-isms than lower.",
    )
    args = p.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"No fixtures dir: {fixtures}", file=sys.stderr)
        return 1

    if args.all_intensities:
        # Monotonicity check: each intensity must strip >= previous.
        reports = {lvl: run(fixtures, intensity=lvl) for lvl in VALID_INTENSITIES}
        print("Humanizer benchmark — all intensities\n")
        print(f"{'intensity':<12}{'before':>10}{'after':>8}{'delta':>8}{'% reduction':>14}")
        for lvl in VALID_INTENSITIES:
            r = reports[lvl]
            print(
                f"{lvl:<12}{r['total_ai_isms_before']:>10}{r['total_ai_isms_after']:>8}"
                f"{r['total_delta']:>8}{r['percent_reduced']:>13}%"
            )
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = reports["balanced"]["timestamp"]
        (out_dir / f"{stamp}-matrix.json").write_text(json.dumps(reports, indent=2) + "\n")
        if args.strict:
            prev_delta = -1
            for lvl in VALID_INTENSITIES:
                if reports[lvl]["total_delta"] < prev_delta:
                    print(f"REGRESSION: intensity {lvl} stripped fewer AI-isms than a lower level.", file=sys.stderr)
                    return 2
                prev_delta = reports[lvl]["total_delta"]
        return 0

    report = run(fixtures, intensity=args.intensity)
    print_report(report)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = out_dir / f"{report['timestamp']}.json"
    stamp_file.write_text(json.dumps(report, indent=2) + "\n")
    (out_dir / "latest.json").write_text(json.dumps(report, indent=2) + "\n")

    if args.strict:
        regressions = []
        for f in report["fixtures"]:
            reasons: list[str] = []
            if f["delta"] < 0:
                reasons.append("AI-ism count increased")
            if not f["structural_ok"]:
                reasons.append("structural validation failed")
            # Research gate (Cat 04/05): if the source had human-like burstiness,
            # strict mode should block flattening to detector-bait uniform prose.
            burstiness_floor_breach = (
                f["sentence_count_after"] >= 8
                and f["burstiness_before"] >= 4.0
                and f["burstiness_after"] < 4.0
            )
            if burstiness_floor_breach:
                reasons.append(
                    "burstiness dropped below floor "
                    f"(σ {f['burstiness_before']:.1f}->{f['burstiness_after']:.1f})"
                )
            if reasons:
                regressions.append((f["file"], reasons))
        if regressions:
            print("\nREGRESSIONS:", file=sys.stderr)
            for filename, reasons in regressions:
                print(f"  - {filename}: {'; '.join(reasons)}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
