#!/usr/bin/env python3
"""Plot AI-ism reduction across prompts and conditions for an unslop snapshot.

Reads `measure.json` (produced by `evals/measure.py`) and writes:

  evals/snapshots/<timestamp>/plot.html  — interactive plotly chart
  evals/snapshots/<timestamp>/plot.png   — static export (optional, needs kaleido)

Usage:
  python3 evals/plot.py evals/snapshots/<timestamp>
  python3 evals/plot.py evals/snapshots/<timestamp> --no-png

Optional dependencies (install via `pip install plotly kaleido`):
  - plotly  — required, generates the HTML chart
  - kaleido — optional, enables PNG export (skip with --no-png if not installed)

The chart shows AI-ism counts per prompt across the three eval conditions
(baseline / deterministic / llm), making regression vs improvement visible at
a glance. Embed the PNG in PR descriptions or release notes to surface
quality trends per release.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_measure(snapshot_dir: Path) -> dict:
    measure_path = snapshot_dir / "measure.json"
    if not measure_path.is_file():
        sys.exit(
            f"No measure.json in {snapshot_dir}. Run `python3 evals/measure.py "
            f"{snapshot_dir}` first."
        )
    return json.loads(measure_path.read_text())


def _rows(summary: dict) -> tuple[list[str], dict[str, list[float | None]]]:
    prompts = list(summary["prompts"].keys())
    series: dict[str, list[float | None]] = {
        "baseline": [],
        "deterministic": [],
        "llm": [],
    }
    for pid in prompts:
        prompt = summary["prompts"][pid]
        for cond in series:
            row = prompt.get(cond)
            if isinstance(row, dict) and not row.get("skipped"):
                series[cond].append(row.get("ai_isms"))
            else:
                series[cond].append(None)
    return prompts, series


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("snapshot_dir", type=Path)
    p.add_argument(
        "--no-png", action="store_true", help="Skip PNG export (kaleido not installed)"
    )
    args = p.parse_args()

    if not args.snapshot_dir.is_dir():
        sys.exit(f"Not a directory: {args.snapshot_dir}")

    try:
        import plotly.graph_objects as go  # noqa: PLC0415
    except ImportError:
        sys.exit(
            "plotly not installed. Install with: pip install plotly\n"
            "For PNG export also: pip install kaleido"
        )

    summary = _load_measure(args.snapshot_dir)
    prompts, series = _rows(summary)

    if not prompts:
        sys.exit(f"No prompts measured in {args.snapshot_dir}")

    colors = {
        "baseline": "#bd2828",
        "deterministic": "#2a7f4f",
        "llm": "#1f4f8f",
    }

    fig = go.Figure()
    for name, values in series.items():
        if all(v is None for v in values):
            continue
        fig.add_trace(
            go.Bar(
                name=name,
                x=prompts,
                y=values,
                marker_color=colors[name],
                hovertemplate=f"<b>{name}</b><br>%{{x}}: %{{y}} AI-isms<extra></extra>",
            )
        )

    agg = summary.get("aggregate", {})
    delta = agg.get("mean_ai_ism_delta_det_vs_baseline")
    delta_str = f"{delta:+.1f}" if isinstance(delta, (int, float)) else "n/a"

    fig.update_layout(
        title=dict(
            text=(
                "<b>AI-isms per prompt — unslop eval</b><br>"
                f"<sub>Mean Δ deterministic vs baseline: <b>{delta_str}</b> · "
                f"prompts: {agg.get('prompt_count', '?')} · "
                f"structural failures: {agg.get('structural_failures', 0)}</sub>"
            ),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(title="prompt", tickangle=-30, automargin=True),
        yaxis=dict(title="AI-ism count", gridcolor="rgba(0,0,0,0.08)", zeroline=False),
        barmode="group",
        plot_bgcolor="white",
        height=520,
        width=max(720, 80 * len(prompts) + 240),
        margin=dict(l=70, r=40, t=110, b=110),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    html_out = args.snapshot_dir / "plot.html"
    fig.write_html(html_out)
    print(f"Wrote {html_out}")

    if args.no_png:
        return 0

    try:
        png_out = args.snapshot_dir / "plot.png"
        fig.write_image(png_out, scale=2)
        print(f"Wrote {png_out}")
    except Exception as exc:
        print(
            f"PNG export skipped ({exc}). Install kaleido to enable: pip install kaleido",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
