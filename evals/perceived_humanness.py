#!/usr/bin/env python3
"""Perceived-humanness benchmark: blind LLM-as-judge preference.

Problem this solves: TMR and Desklib detectors pin AI-heavy fixtures near
p_ai=1.0 regardless of how much we rewrite them. Phases 1-5 clearly improve
prose quality (contraction rate, sentence variance, AI-ism count) but the
detector metric can't reflect that. We need a metric that captures perceived
humanness from a reader's point of view.

This harness pairs (original, humanized) fixtures, shuffles A/B, asks a
judge LLM which reads more like a human wrote it, and aggregates win rate
across fixtures. Blind on the judge side — no metadata about which is which.

Research basis: Cat 17 — "no deployed system publishes a perceived-humanness
score." This closes that gap for the unslop project. Mirrors the DAMAGE
(COLING 2025) tier taxonomy by measuring L1/L2/L3 rewrites separately when
asked.

Usage:
  python3 evals/perceived_humanness.py                  # balanced vs original, Claude judge
  python3 evals/perceived_humanness.py --intensity full --structural --soul
  python3 evals/perceived_humanness.py --fixtures benchmarks/fixtures
  python3 evals/perceived_humanness.py --runs 3         # best-of-three per fixture

Output: benchmarks/results/<stamp>-humanness.json + stdout markdown table.

Judge backends:
  claude     — Anthropic SDK. Requires ANTHROPIC_API_KEY.
  claude-cli — `claude --print` on PATH. Works in environments without the SDK.

Both fall back in that order.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "unslop"))

from scripts.humanize import humanize_deterministic  # noqa: E402


JUDGE_SYSTEM_PROMPT = """\
You are a careful editor comparing two short passages.

One passage was written or refined by a human editor. The other was produced \
by an AI system. Read both carefully. Pick the passage that reads more like \
a human wrote it — not the more polished one, not the more formal one, but \
the one that feels like it came from a thinking person rather than from a \
template.

Signals of human writing include: variance in sentence length, unexpected \
concrete details, opinions held without hedging, contractions where natural, \
mild informality where appropriate, occasional rough edges. Signals of AI \
writing include: uniform rhythm, hedging stacks, persuasive framing, \
inflated significance language, a tidy five-paragraph structure, em-dash \
pileups, and stock phrases like "delve", "tapestry", "testament to", "marks \
a pivotal moment".

Reply on two lines:
  Line 1: A, B, or TIE
  Line 2: one short sentence explaining your choice (under 25 words)

Nothing else."""


JUDGE_USER_TEMPLATE = """\
Passage A:
===
{passage_a}
===

Passage B:
===
{passage_b}
===

Which reads more like a human wrote it?"""


# ---------------- Judge backends ----------------


def _call_claude_sdk(system: str, user: str, model: str, max_tokens: int = 256) -> str | None:
    try:
        from anthropic import Anthropic
    except ImportError:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    client = Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in msg.content if hasattr(block, "text")).strip()


def _call_claude_cli(system: str, user: str) -> str | None:
    """Fallback: pipe the prompt through `claude --print`. System + user get
    concatenated because the CLI doesn't take a separate system field."""
    if shutil.which("claude") is None:
        return None
    full_prompt = f"{system}\n\n{user}"
    proc = subprocess.run(
        ["claude", "--print"],
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(
            f"claude CLI returned {proc.returncode}: {proc.stderr.strip()[:200]}\n"
        )
        return None
    return proc.stdout.strip()


def _judge(passage_a: str, passage_b: str, model: str) -> tuple[str, str]:
    """Returns (choice, rationale). choice ∈ {"A", "B", "TIE", "?"}."""
    user = JUDGE_USER_TEMPLATE.format(passage_a=passage_a, passage_b=passage_b)
    reply = _call_claude_sdk(JUDGE_SYSTEM_PROMPT, user, model) or _call_claude_cli(
        JUDGE_SYSTEM_PROMPT, user
    )
    if reply is None:
        raise RuntimeError(
            "Judge LLM unavailable. Set ANTHROPIC_API_KEY, install anthropic "
            "SDK, or ensure `claude` CLI is on PATH."
        )
    return _parse_choice(reply)


_CHOICE_LINE = re.compile(r"^\s*(A|B|TIE|Tie|tie)\b", re.MULTILINE)


def _parse_choice(reply: str) -> tuple[str, str]:
    """Extract the choice letter and the rationale line from the judge reply.
    Tolerant of small format deviations; falls back to '?' if unparseable."""
    m = _CHOICE_LINE.search(reply)
    if not m:
        return "?", reply[:120]
    choice = m.group(1).upper()
    rationale_lines = [
        line.strip() for line in reply.split("\n") if line.strip()
    ]
    # First line containing the choice, plus any subsequent non-blank line.
    if len(rationale_lines) >= 2:
        rationale = rationale_lines[1][:200]
    else:
        rationale = ""
    return choice, rationale


# ---------------- Harness ----------------


@dataclass
class JudgeVote:
    fixture: str
    run: int
    a_was: str  # "original" or "humanized"
    b_was: str
    judge: str
    choice: str  # "A", "B", "TIE", "?"
    rationale: str
    humanized_won: bool  # computed after A/B reveal


@dataclass
class FixtureResult:
    fixture: str
    votes: list[JudgeVote] = field(default_factory=list)

    @property
    def humanized_wins(self) -> int:
        return sum(1 for v in self.votes if v.humanized_won and v.choice in ("A", "B"))

    @property
    def original_wins(self) -> int:
        return sum(
            1
            for v in self.votes
            if not v.humanized_won and v.choice in ("A", "B")
        )

    @property
    def ties(self) -> int:
        return sum(1 for v in self.votes if v.choice == "TIE")

    @property
    def invalid(self) -> int:
        return sum(1 for v in self.votes if v.choice == "?")


def run(
    fixtures_dir: Path,
    *,
    intensity: str,
    structural: bool | None,
    soul: bool | None,
    judge_model: str,
    runs: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    fixture_paths = sorted(fixtures_dir.glob("*.md"))
    if not fixture_paths:
        raise SystemExit(f"No fixtures in {fixtures_dir}")

    results: list[FixtureResult] = []
    for path in fixture_paths:
        original = path.read_text()
        humanized = humanize_deterministic(  # type: ignore[arg-type]
            original, intensity=intensity, structural=structural, soul=soul
        )
        fixture_result = FixtureResult(fixture=path.name)
        for run_index in range(1, runs + 1):
            a_is_humanized = rng.random() < 0.5
            passage_a = humanized if a_is_humanized else original
            passage_b = original if a_is_humanized else humanized
            a_was = "humanized" if a_is_humanized else "original"
            b_was = "original" if a_is_humanized else "humanized"
            try:
                choice, rationale = _judge(passage_a, passage_b, model=judge_model)
            except RuntimeError as exc:
                print(f"  [{path.name}] judge error on run {run_index}: {exc}", file=sys.stderr)
                continue
            humanized_won = False
            if choice == "A" and a_is_humanized:
                humanized_won = True
            elif choice == "B" and not a_is_humanized:
                humanized_won = True
            vote = JudgeVote(
                fixture=path.name,
                run=run_index,
                a_was=a_was,
                b_was=b_was,
                judge=judge_model,
                choice=choice,
                rationale=rationale,
                humanized_won=humanized_won,
            )
            fixture_result.votes.append(vote)
            tag = "humanized" if humanized_won else ("tie" if choice == "TIE" else "original")
            print(
                f"  [{path.name}] run {run_index}: {choice} → {tag}  «{rationale[:80]}»",
                file=sys.stderr,
            )
        results.append(fixture_result)

    total_humanized = sum(r.humanized_wins for r in results)
    total_original = sum(r.original_wins for r in results)
    total_ties = sum(r.ties for r in results)
    total_votes = total_humanized + total_original + total_ties
    win_rate = (total_humanized / total_votes * 100) if total_votes else 0.0

    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "judge_model": judge_model,
        "intensity": intensity,
        "structural": structural,
        "soul": soul,
        "runs_per_fixture": runs,
        "seed": seed,
        "fixtures": [
            {
                "fixture": r.fixture,
                "humanized_wins": r.humanized_wins,
                "original_wins": r.original_wins,
                "ties": r.ties,
                "invalid": r.invalid,
                "votes": [asdict(v) for v in r.votes],
            }
            for r in results
        ],
        "totals": {
            "humanized_wins": total_humanized,
            "original_wins": total_original,
            "ties": total_ties,
            "invalid": sum(r.invalid for r in results),
            "win_rate_pct": round(win_rate, 1),
        },
    }


def print_summary(report: dict) -> None:
    print("\nPerceived-humanness benchmark\n=============================\n")
    print(f"Judge: {report['judge_model']}")
    print(
        f"Config: intensity={report['intensity']}  "
        f"structural={report['structural']}  soul={report['soul']}  "
        f"runs={report['runs_per_fixture']}  seed={report['seed']}\n"
    )
    print(f"{'fixture':<36}{'hum':>6}{'orig':>6}{'tie':>6}{'inv':>6}")
    for row in report["fixtures"]:
        print(
            f"{row['fixture']:<36}{row['humanized_wins']:>6}"
            f"{row['original_wins']:>6}{row['ties']:>6}{row['invalid']:>6}"
        )
    print()
    t = report["totals"]
    print(
        f"Totals: humanized={t['humanized_wins']}  original={t['original_wins']}  "
        f"ties={t['ties']}  invalid={t['invalid']}"
    )
    print(f"Humanized win rate: {t['win_rate_pct']}%")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", default=str(ROOT / "benchmarks/fixtures"))
    p.add_argument("--out", default=str(ROOT / "benchmarks/results"))
    p.add_argument("--intensity", default="balanced", choices=("subtle", "balanced", "full"))
    p.add_argument(
        "--structural",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Phase 1 structural pass. Default: on for balanced/full, off for subtle.",
    )
    p.add_argument(
        "--soul",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Phase 5 soul pass. Default: on for balanced/full, off for subtle.",
    )
    p.add_argument(
        "--judge-model",
        default=os.environ.get("UNSLOP_JUDGE_MODEL", "claude-sonnet-4-5"),
        help="Model ID to use as judge. Default claude-sonnet-4-5.",
    )
    p.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Independent A/B judgments per fixture. Higher = more robust.",
    )
    p.add_argument("--seed", type=int, default=20260421)
    args = p.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"No fixtures dir: {fixtures}", file=sys.stderr)
        return 1

    report = run(
        fixtures,
        intensity=args.intensity,
        structural=args.structural,
        soul=args.soul,
        judge_model=args.judge_model,
        runs=args.runs,
        seed=args.seed,
    )
    print_summary(report)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = out_dir / f"{report['timestamp']}-humanness.json"
    stamp_file.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nWrote {stamp_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
