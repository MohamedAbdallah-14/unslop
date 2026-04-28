#!/usr/bin/env python3
"""Compare unslop's detector ladder with an external adversarial paraphraser."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from unslop.scripts.detector import DetectorName, DetectorUnavailable, feedback_loop, score_ai_probability  # noqa: E402


def _run_external(repo: Path, text: str) -> str:
    script = repo / "paraphrase_and_detect.py"
    if not script.exists():
        raise FileNotFoundError(f"external paraphrase script not found at {script}")
    proc = subprocess.run(
        [sys.executable, str(script)],
        input=text,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"{script} exited {proc.returncode}")
    return proc.stdout.strip()


def run_comparison(
    fixtures: Path,
    external_repo: Path,
    out: Path,
    detector: DetectorName,
) -> dict[str, Any]:
    rows = []
    for path in sorted(fixtures.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        original = score_ai_probability(text, detector=detector)
        ours = feedback_loop(text, detector=detector).final_text
        ours_score = score_ai_probability(ours, detector=detector)
        external = _run_external(external_repo, text)
        external_score = score_ai_probability(external, detector=detector)
        rows.append(
            {
                "fixture": path.name,
                "original_probability": original,
                "unslop_probability": ours_score,
                "external_probability": external_score,
                "unslop_reduction": original - ours_score,
                "external_reduction": original - external_score,
            }
        )
    payload = {"detector": detector, "rows": rows}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(_markdown(rows), encoding="utf-8")
    return payload


def _markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Fixture | Original | unslop | external |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['fixture']} | {row['original_probability']:.3f} | "
            f"{row['unslop_probability']:.3f} | {row['external_probability']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=ROOT / "benchmarks" / "fixtures")
    parser.add_argument("--external-repo", type=Path, default=Path("/tmp/chengez-adv"))
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "benchmarks" / "results" / "adv_paraphrase_comparison.json",
    )
    parser.add_argument("--detector", choices=("tmr", "desklib"), default="tmr")
    args = parser.parse_args(argv)
    try:
        run_comparison(args.fixtures, args.external_repo, args.out, args.detector)
    except DetectorUnavailable as exc:
        sys.stderr.write(f"detector unavailable: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
