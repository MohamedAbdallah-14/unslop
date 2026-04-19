#!/usr/bin/env python3
"""Run prompts through a model and snapshot three conditions per prompt.

Conditions:
  - baseline: raw model output
  - deterministic: baseline run through humanize_deterministic
  - llm: baseline run through humanize_llm (requires API key; else skipped)

Usage:
  python3 evals/llm_run.py [--prompts evals/prompts] [--out evals/snapshots]
                           [--model claude-sonnet-4-5] [--max-prompts N]

Each run writes to snapshots/<UTC timestamp>/ a JSON document per prompt plus
a `meta.json` describing the run (model, cwd, git sha). Safe to commit for
regression tracking.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "humanizer-humanize"))

from scripts.humanize import humanize_deterministic, humanize_llm  # noqa: E402


def _git_sha() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
            )
            .strip()
        )
    except Exception:
        return "unknown"


def _anthropic_baseline(prompt: str, model: str) -> str | None:
    try:
        from anthropic import Anthropic
    except ImportError:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    client = Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if hasattr(b, "text")).strip()


def _claude_cli_baseline(prompt: str) -> str | None:
    from shutil import which

    if which("claude") is None:
        return None
    proc = subprocess.run(
        ["claude", "--print"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def run_prompt(prompt_id: str, prompt: str, model: str) -> dict:
    baseline = _anthropic_baseline(prompt, model) or _claude_cli_baseline(prompt)
    if baseline is None:
        return {
            "prompt_id": prompt_id,
            "skipped": True,
            "reason": "no ANTHROPIC_API_KEY and no `claude` CLI; cannot generate baseline",
        }

    det = humanize_deterministic(baseline)
    try:
        llm_out = humanize_llm(baseline)
        llm_err = None
    except Exception as exc:
        llm_out = None
        llm_err = str(exc)

    return {
        "prompt_id": prompt_id,
        "prompt": prompt,
        "conditions": {
            "baseline": {"text": baseline},
            "deterministic": {"text": det},
            "llm": (
                {"text": llm_out} if llm_out is not None else {"skipped": True, "error": llm_err}
            ),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--prompts", default=str(ROOT / "evals/prompts"))
    p.add_argument("--out", default=str(ROOT / "evals/snapshots"))
    p.add_argument(
        "--model",
        default=os.environ.get("HUMANIZER_MODEL", "claude-sonnet-4-5"),
    )
    p.add_argument("--max-prompts", type=int, default=0, help="0 = all")
    args = p.parse_args()

    prompts_dir = Path(args.prompts)
    if not prompts_dir.is_dir():
        print(f"No prompts dir: {prompts_dir}", file=sys.stderr)
        return 1

    prompts = sorted(prompts_dir.glob("*.txt"))
    if args.max_prompts:
        prompts = prompts[: args.max_prompts]
    if not prompts:
        print(f"No .txt prompts under {prompts_dir}", file=sys.stderr)
        return 1

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "timestamp": stamp,
        "model": args.model,
        "git_sha": _git_sha(),
        "prompt_count": len(prompts),
        "has_api_key": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    for prompt_file in prompts:
        prompt_id = prompt_file.stem
        text = prompt_file.read_text().strip()
        print(f"-> {prompt_id}")
        result = run_prompt(prompt_id, text, args.model)
        (out_dir / f"{prompt_id}.json").write_text(json.dumps(result, indent=2) + "\n")

    print(f"\nSnapshot written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
