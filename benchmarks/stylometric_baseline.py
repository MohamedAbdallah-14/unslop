#!/usr/bin/env python3
"""Build stylometric baseline bands from human and LLM text directories."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from unslop.scripts.stylometry import StyleProfile, analyze  # noqa: E402


def _iter_texts(path: Path) -> list[Path]:
    return sorted(
        p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md"}
    )


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * pct
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] + (xs[hi] - xs[lo]) * frac


def _numeric_fields(profile: StyleProfile) -> dict[str, float]:
    return {
        key: float(value)
        for key, value in asdict(profile).items()
        if isinstance(value, (int, float))
    }


def _measure(paths: list[Path]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        profile = analyze(text)
        if profile.total_words == 0:
            continue
        rows.append(_numeric_fields(profile))
    return rows


def _summarize(human: list[dict[str, float]], llm: list[dict[str, float]]) -> dict[str, Any]:
    fields = sorted(set().union(*(row.keys() for row in human + llm)))
    summary: dict[str, Any] = {}
    for field in fields:
        human_values = [row[field] for row in human if field in row]
        llm_values = [row[field] for row in llm if field in row]
        if not human_values or not llm_values:
            continue
        summary[field] = {
            "human_p25": round(_percentile(human_values, 0.25), 4),
            "human_median": round(statistics.median(human_values), 4),
            "human_p75": round(_percentile(human_values, 0.75), 4),
            "llm_p25": round(_percentile(llm_values, 0.25), 4),
            "llm_median": round(statistics.median(llm_values), 4),
            "llm_p75": round(_percentile(llm_values, 0.75), 4),
            "human_range": round(max(human_values) - min(human_values), 4),
            "llm_range": round(max(llm_values) - min(llm_values), 4),
        }
    return summary


def _markdown_table(fields: dict[str, Any]) -> str:
    lines = [
        "| Field | Human p25 | Human median | Human p75 | LLM median |",
        "|---|---:|---:|---:|---:|",
    ]
    for field, stats in sorted(fields.items()):
        lines.append(
            f"| `{field}` | {stats['human_p25']} | {stats['human_median']} | "
            f"{stats['human_p75']} | {stats['llm_median']} |"
        )
    return "\n".join(lines) + "\n"


def build_baseline(human_dir: Path, llm_dir: Path) -> dict[str, Any]:
    human_paths = _iter_texts(human_dir)
    llm_paths = _iter_texts(llm_dir)
    human_rows = _measure(human_paths)
    llm_rows = _measure(llm_paths)
    fields = _summarize(human_rows, llm_rows)
    return {
        "metadata": {
            "human_corpus": str(human_dir),
            "llm_corpus": str(llm_dir),
            "n_human": len(human_rows),
            "n_llm": len(llm_rows),
            "note": "Use a published corpus subset when producing release baselines.",
        },
        "fields": fields,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--human", type=Path, required=True)
    parser.add_argument("--llm", type=Path, required=True)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "benchmarks" / "results" / "stylometric_baseline.json",
    )
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args(argv)

    payload = build_baseline(args.human, args.llm)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary_path = args.summary or args.out.with_suffix(".md")
    summary_path.write_text(_markdown_table(payload["fields"]), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
