#!/usr/bin/env python3
"""Measure a snapshot produced by llm_run.py.

Emits a plain-text summary to stdout and a machine-readable `measure.json`
next to the input snapshot. Use `--fail-on-regression` in CI to fail the
build if the unslop made AI-isms *worse* or broke structure.

Metrics per condition (baseline | deterministic | llm):
  - word_count
  - ai_isms: number of AI-ism hits (from scripts/validate.AI_ISMS)
  - structural_errors: from validate(baseline, this)
  - avg_sentence_len
  - burstiness: stddev of sentence lengths (proxy for varied cadence)
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "unslop"))

from scripts.validate import AI_ISM_PATTERNS, validate  # noqa: E402


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
WORD = re.compile(r"\w+")


def count_ai_isms(text: str) -> int:
    return sum(len(p.findall(text)) for p in AI_ISM_PATTERNS)


def sentence_lengths(text: str) -> list[int]:
    return [len(WORD.findall(s)) for s in SENTENCE_SPLIT.split(text) if s.strip()]


def measure_text(baseline: str, text: str) -> dict:
    lens = sentence_lengths(text)
    report = validate(baseline, text) if baseline else None
    return {
        "word_count": len(WORD.findall(text)),
        "ai_isms": count_ai_isms(text),
        "avg_sentence_len": round(statistics.mean(lens), 2) if lens else 0,
        "burstiness": round(statistics.pstdev(lens), 2) if len(lens) > 1 else 0,
        "structural_errors": 0 if report is None else len(report.errors),
        "structural_ok": True if report is None else report.ok,
    }


def summarize(snapshot_dir: Path) -> dict:
    summary: dict = {"prompts": {}, "aggregate": {}}
    for path in sorted(snapshot_dir.glob("*.json")):
        if path.name == "meta.json" or path.name == "measure.json":
            continue
        data = json.loads(path.read_text())
        if data.get("skipped"):
            summary["prompts"][data["prompt_id"]] = {"skipped": data.get("reason", "")}
            continue
        conds = data["conditions"]
        baseline_text = conds["baseline"]["text"]
        entry: dict = {}
        for name in ("baseline", "deterministic", "llm"):
            cond = conds[name]
            if cond.get("skipped"):
                entry[name] = {"skipped": True, "error": cond.get("error")}
                continue
            entry[name] = measure_text(baseline_text, cond["text"])
        summary["prompts"][data["prompt_id"]] = entry
    # Aggregate: mean ai-ism delta det-vs-baseline, count of structural failures.
    deltas = []
    struct_fails = 0
    for prompt in summary["prompts"].values():
        if "baseline" in prompt and "deterministic" in prompt and "ai_isms" in prompt["baseline"]:
            deltas.append(prompt["deterministic"]["ai_isms"] - prompt["baseline"]["ai_isms"])
            for name in ("deterministic", "llm"):
                if isinstance(prompt.get(name), dict) and prompt[name].get("structural_errors", 0) > 0:
                    struct_fails += 1
    summary["aggregate"] = {
        "mean_ai_ism_delta_det_vs_baseline": (
            round(statistics.mean(deltas), 2) if deltas else None
        ),
        "structural_failures": struct_fails,
        "prompt_count": len(summary["prompts"]),
    }
    return summary


def print_summary(summary: dict) -> None:
    print("Unslop eval summary\n======================\n")
    for pid, prompt in summary["prompts"].items():
        print(f"• {pid}")
        if "skipped" in prompt:
            print(f"    skipped: {prompt['skipped']}")
            continue
        header = f"    {'condition':<16}{'words':>8}{'ai-isms':>10}{'avg-sen':>10}{'burst':>8}{'struct':>8}"
        print(header)
        for name in ("baseline", "deterministic", "llm"):
            row = prompt.get(name, {})
            if row.get("skipped"):
                print(f"    {name:<16}{'(skipped)':>44}")
                continue
            struct_tag = "ok" if row.get("structural_ok", True) else "FAIL"
            print(
                f"    {name:<16}"
                f"{row['word_count']:>8}"
                f"{row['ai_isms']:>10}"
                f"{row['avg_sentence_len']:>10}"
                f"{row['burstiness']:>8}"
                f"{struct_tag:>8}"
            )
        print()
    agg = summary["aggregate"]
    print(f"aggregate: {agg}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("snapshot_dir", type=Path)
    p.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Non-zero exit if mean AI-ism delta is positive or any structural failure exists.",
    )
    args = p.parse_args()

    if not args.snapshot_dir.is_dir():
        print(f"Not a directory: {args.snapshot_dir}", file=sys.stderr)
        return 1

    summary = summarize(args.snapshot_dir)
    print_summary(summary)
    (args.snapshot_dir / "measure.json").write_text(json.dumps(summary, indent=2) + "\n")

    if args.fail_on_regression:
        agg = summary["aggregate"]
        delta = agg.get("mean_ai_ism_delta_det_vs_baseline")
        if (delta is not None and delta > 0) or agg.get("structural_failures", 0) > 0:
            print(
                f"\nREGRESSION: delta={delta} structural_failures={agg['structural_failures']}",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
