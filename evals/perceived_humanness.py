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

LLM-as-judge bias — what this benchmark accounts for and what it does not
------------------------------------------------------------------------
LLM-as-judge has quantified, reproducible biases (arXiv 2411.15594
"LLM-as-Judge Survey"; arXiv 2410.02736 "CALM" bias framework; arXiv
2601.07648 "Order in the Evaluation Court"). Three are first-order:

  - Position bias: ~40% inconsistency when the same pair is shown in
    opposite orders. A single A/B judgment is not a measurement — it's one
    flip of a 60/40 coin. Mitigation here: `--counterbalance` (default on)
    runs every fixture twice per run, once with humanized=A and once with
    humanized=B, and averages the vote. Random A/B shuffling is still
    applied on top so the order interleave isn't predictable.
  - Verbosity inflation: ~15% preference for longer output. Humanized
    prose sometimes adds contractions and fragments that net-shorten the
    text; sometimes splits long sentences that net-lengthen it. Report
    prints the per-fixture delta in characters so the reader can audit
    whether any win is a length artifact.
  - Self-enhancement: 5–7% bias toward the judge model's own family on
    open-ended tasks. A single-model judge (any single model, Claude
    included) is therefore an upper bound on the true human-rated win
    rate. Mitigation here: `--judges` accepts a comma-separated list
    ("claude-sonnet-4-5,gpt-5") and reports a per-judge table plus a
    jury-average row. When any judge matches the generator family used
    to create the humanized text, this value should be read as "likely
    inflated on that row".

What this benchmark still cannot do: correct for prompt drift, unmeasured
context effects, or the deeper validity question of whether
perceived-humanness correlates with actually-better writing for a given
task. This is a humanness signal, not a quality signal.

Usage:
  python3 evals/perceived_humanness.py                  # balanced vs original, Claude judge
  python3 evals/perceived_humanness.py --intensity full --structural --soul
  python3 evals/perceived_humanness.py --fixtures benchmarks/fixtures
  python3 evals/perceived_humanness.py --runs 3         # independent judgments per fixture
  python3 evals/perceived_humanness.py --judges "claude-sonnet-4-5,gpt-5"

Output: benchmarks/results/<stamp>-humanness.json + stdout markdown table.

Judge backends:
  claude-family models  — Anthropic SDK (ANTHROPIC_API_KEY), then
                          `claude --print` CLI as fallback.
  gpt-family models     — OpenAI SDK (OPENAI_API_KEY). Optional; skipped
                          with a clear warning if neither the SDK nor the
                          env var is present.

Missing a judge is a soft failure: it prints a note, drops that judge
from the jury, and continues. A fully-missing jury exits non-zero.
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


def _is_claude_model(model: str) -> bool:
    return model.lower().startswith("claude")


def _is_openai_model(model: str) -> bool:
    return model.lower().startswith(("gpt", "o1", "o3", "o4"))


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


def _call_openai_sdk(system: str, user: str, model: str, max_tokens: int = 256) -> str | None:
    """Optional OpenAI-compatible judge path. Keeps extras optional: if the
    SDK isn't installed or the API key isn't set, returns None so the caller
    can drop this judge from the jury without failing the run."""
    try:
        from openai import OpenAI  # type: ignore[import-not-found]
    except ImportError:
        return None
    if not os.environ.get("OPENAI_API_KEY"):
        return None
    client = OpenAI()
    try:
        msg = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except Exception as exc:  # network, auth, model-not-available
        sys.stderr.write(f"openai judge error ({model}): {exc}\n")
        return None
    content = msg.choices[0].message.content if msg.choices else None
    return content.strip() if content else None


class JudgeUnavailable(RuntimeError):
    """Raised only when *every* requested judge is unavailable."""


def _judge(passage_a: str, passage_b: str, model: str) -> tuple[str, str]:
    """Returns (choice, rationale). choice ∈ {"A", "B", "TIE", "?"}. Raises
    JudgeUnavailable when no backend can serve this specific model."""
    user = JUDGE_USER_TEMPLATE.format(passage_a=passage_a, passage_b=passage_b)

    reply: str | None = None
    if _is_claude_model(model):
        reply = _call_claude_sdk(JUDGE_SYSTEM_PROMPT, user, model)
        if reply is None:
            reply = _call_claude_cli(JUDGE_SYSTEM_PROMPT, user)
    elif _is_openai_model(model):
        reply = _call_openai_sdk(JUDGE_SYSTEM_PROMPT, user, model)
    else:
        # Unknown family — try Claude SDK first (it accepts arbitrary strings
        # and will return a useful error), then give up.
        reply = _call_claude_sdk(JUDGE_SYSTEM_PROMPT, user, model)

    if reply is None:
        raise JudgeUnavailable(
            f"Judge {model!r} unavailable. "
            "For claude-* models: set ANTHROPIC_API_KEY or install the anthropic "
            "SDK, or put `claude` on PATH. "
            "For gpt-* / o-* models: set OPENAI_API_KEY and install the openai SDK."
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
    original_chars: int = 0
    humanized_chars: int = 0

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

    @property
    def length_delta(self) -> int:
        """Humanized length − original length, in characters.
        Exposes verbosity bias: if a win aligns with a large positive delta
        across many fixtures, the jury may be preferring length."""
        return self.humanized_chars - self.original_chars


def _judge_one_pair(
    fixture_name: str,
    run_index: int,
    pass_index: int,
    humanized: str,
    original: str,
    a_is_humanized: bool,
    judge_model: str,
) -> JudgeVote | None:
    """Single judgment for a single (fixture, run, pass, judge) cell.
    Returns None on hard judge failure so the caller can drop that cell."""
    passage_a = humanized if a_is_humanized else original
    passage_b = original if a_is_humanized else humanized
    a_was = "humanized" if a_is_humanized else "original"
    b_was = "original" if a_is_humanized else "humanized"
    try:
        choice, rationale = _judge(passage_a, passage_b, model=judge_model)
    except JudgeUnavailable as exc:
        print(
            f"  [{fixture_name}] judge {judge_model!r} unavailable: {exc}",
            file=sys.stderr,
        )
        return None
    humanized_won = (choice == "A" and a_is_humanized) or (
        choice == "B" and not a_is_humanized
    )
    vote = JudgeVote(
        fixture=fixture_name,
        run=run_index * 10 + pass_index,  # encode counterbalance pass in the run key
        a_was=a_was,
        b_was=b_was,
        judge=judge_model,
        choice=choice,
        rationale=rationale,
        humanized_won=humanized_won,
    )
    tag = "humanized" if humanized_won else ("tie" if choice == "TIE" else "original")
    print(
        f"  [{fixture_name}] run {run_index}/pass {pass_index} "
        f"({judge_model}): {choice} → {tag}  «{rationale[:80]}»",
        file=sys.stderr,
    )
    return vote


def run(
    fixtures_dir: Path,
    *,
    intensity: str,
    structural: bool | None,
    soul: bool | None,
    judges: list[str],
    runs: int,
    seed: int,
    counterbalance: bool,
) -> dict:
    rng = random.Random(seed)
    fixture_paths = sorted(fixtures_dir.glob("*.md"))
    if not fixture_paths:
        raise SystemExit(f"No fixtures in {fixtures_dir}")

    results: list[FixtureResult] = []
    live_judges: list[str] = []
    dropped_judges: list[str] = []
    judge_seen: dict[str, bool] = {j: False for j in judges}

    for path in fixture_paths:
        original = path.read_text()
        humanized = humanize_deterministic(  # type: ignore[arg-type]
            original, intensity=intensity, structural=structural, soul=soul
        )
        fixture_result = FixtureResult(
            fixture=path.name,
            original_chars=len(original),
            humanized_chars=len(humanized),
        )
        for run_index in range(1, runs + 1):
            # Random seed orientation for this run. Counterbalance adds a
            # second pass with the orientation flipped so position bias
            # (~40% inconsistency per literature) averages out per fixture.
            base_orientation = rng.random() < 0.5
            passes = [(1, base_orientation)]
            if counterbalance:
                passes.append((2, not base_orientation))

            for pass_index, a_is_humanized in passes:
                for judge_model in judges:
                    vote = _judge_one_pair(
                        path.name,
                        run_index,
                        pass_index,
                        humanized,
                        original,
                        a_is_humanized,
                        judge_model,
                    )
                    if vote is None:
                        continue
                    judge_seen[judge_model] = True
                    fixture_result.votes.append(vote)
        results.append(fixture_result)

    live_judges = [j for j in judges if judge_seen[j]]
    dropped_judges = [j for j in judges if not judge_seen[j]]

    if not live_judges:
        raise JudgeUnavailable(
            "No judge returned a usable vote. "
            f"Requested: {judges}. See messages above for backend errors."
        )

    total_humanized = sum(r.humanized_wins for r in results)
    total_original = sum(r.original_wins for r in results)
    total_ties = sum(r.ties for r in results)
    total_votes = total_humanized + total_original + total_ties
    win_rate = (total_humanized / total_votes * 100) if total_votes else 0.0

    per_judge: dict[str, dict[str, int | float]] = {}
    for j in live_judges:
        hum = sum(
            1
            for r in results
            for v in r.votes
            if v.judge == j and v.humanized_won and v.choice in ("A", "B")
        )
        orig = sum(
            1
            for r in results
            for v in r.votes
            if v.judge == j and not v.humanized_won and v.choice in ("A", "B")
        )
        ties = sum(1 for r in results for v in r.votes if v.judge == j and v.choice == "TIE")
        votes = hum + orig + ties
        per_judge[j] = {
            "humanized_wins": hum,
            "original_wins": orig,
            "ties": ties,
            "win_rate_pct": round((hum / votes * 100) if votes else 0.0, 1),
        }

    avg_length_delta = (
        round(sum(r.length_delta for r in results) / len(results), 1) if results else 0.0
    )

    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "judges": live_judges,
        "judges_dropped": dropped_judges,
        "counterbalance": counterbalance,
        "intensity": intensity,
        "structural": structural,
        "soul": soul,
        "runs_per_fixture": runs,
        "seed": seed,
        "bias_notes": {
            "position_inconsistency_pct": 40,
            "verbosity_inflation_pct": 15,
            "self_enhancement_pct_range": [5, 7],
            "references": [
                "arXiv:2411.15594 LLM-as-Judge Survey",
                "arXiv:2410.02736 CALM",
                "arXiv:2601.07648 Order in the Evaluation Court",
            ],
            "avg_length_delta_chars": avg_length_delta,
        },
        "fixtures": [
            {
                "fixture": r.fixture,
                "humanized_wins": r.humanized_wins,
                "original_wins": r.original_wins,
                "ties": r.ties,
                "invalid": r.invalid,
                "length_delta_chars": r.length_delta,
                "votes": [asdict(v) for v in r.votes],
            }
            for r in results
        ],
        "per_judge": per_judge,
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
    print(f"Judges: {', '.join(report['judges'])}")
    if report.get("judges_dropped"):
        print(f"  (dropped, unavailable: {', '.join(report['judges_dropped'])})")
    print(
        f"Config: intensity={report['intensity']}  "
        f"structural={report['structural']}  soul={report['soul']}  "
        f"runs={report['runs_per_fixture']}  "
        f"counterbalance={report['counterbalance']}  seed={report['seed']}"
    )
    bias = report["bias_notes"]
    print(
        "LLM-judge bias baseline: "
        f"position={bias['position_inconsistency_pct']}%  "
        f"verbosity≈{bias['verbosity_inflation_pct']}%  "
        f"self-enhancement={bias['self_enhancement_pct_range'][0]}-"
        f"{bias['self_enhancement_pct_range'][1]}%  "
        f"avg Δchars={bias['avg_length_delta_chars']}\n"
    )
    print(f"{'fixture':<36}{'hum':>6}{'orig':>6}{'tie':>6}{'inv':>6}{'Δchars':>10}")
    for row in report["fixtures"]:
        print(
            f"{row['fixture']:<36}{row['humanized_wins']:>6}"
            f"{row['original_wins']:>6}{row['ties']:>6}{row['invalid']:>6}"
            f"{row['length_delta_chars']:>10}"
        )
    print()
    if report["per_judge"]:
        print("Per-judge win rate (self-enhancement check):")
        for judge, stats in report["per_judge"].items():
            print(
                f"  {judge:<28} "
                f"hum={stats['humanized_wins']:>3}  "
                f"orig={stats['original_wins']:>3}  "
                f"tie={stats['ties']:>3}  "
                f"win={stats['win_rate_pct']}%"
            )
        print()
    t = report["totals"]
    print(
        f"Totals: humanized={t['humanized_wins']}  original={t['original_wins']}  "
        f"ties={t['ties']}  invalid={t['invalid']}"
    )
    print(f"Jury-averaged win rate: {t['win_rate_pct']}%")


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
        "--judges",
        default=os.environ.get("UNSLOP_JUDGE_MODELS", "claude-sonnet-4-5"),
        help=(
            "Comma-separated list of judge model IDs. Default claude-sonnet-4-5. "
            "Example: 'claude-sonnet-4-5,gpt-5' for a two-model jury."
        ),
    )
    p.add_argument(
        "--judge-model",
        default=None,
        help="DEPRECATED: single-judge alias for --judges. Use --judges instead.",
    )
    p.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Independent A/B judgments per fixture. Higher = more robust.",
    )
    p.add_argument(
        "--counterbalance",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Run each fixture in both A/B orientations per run to average out "
            "position bias (~40% inconsistency per literature). Default on."
        ),
    )
    p.add_argument("--seed", type=int, default=20260421)
    args = p.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"No fixtures dir: {fixtures}", file=sys.stderr)
        return 1

    judges_spec = args.judge_model or args.judges
    judges = [j.strip() for j in judges_spec.split(",") if j.strip()]
    if not judges:
        print("No judges configured. See --judges.", file=sys.stderr)
        return 2

    try:
        report = run(
            fixtures,
            intensity=args.intensity,
            structural=args.structural,
            soul=args.soul,
            judges=judges,
            runs=args.runs,
            seed=args.seed,
            counterbalance=args.counterbalance,
        )
    except JudgeUnavailable as exc:
        print(f"\nAll judges unavailable: {exc}", file=sys.stderr)
        return 3

    print_summary(report)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = out_dir / f"{report['timestamp']}-humanness.json"
    stamp_file.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nWrote {stamp_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
