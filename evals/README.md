# Unslop Evals

Quick A/B harness to answer: "does the unslop make output measurably less
AI-ish without breaking structure?"

Three conditions per prompt:

| Condition | What the model sees |
|---|---|
| `baseline` | Prompt only. No unslop rules, no deterministic pass. |
| `deterministic` | Baseline response run through the regex unslop. |
| `llm` | Baseline response run through the LLM unslop (Anthropic SDK or `claude` CLI). |

For each condition we measure:
- Word count
- AI-ism count (via `scripts/validate.AI_ISMS`)
- Structural integrity (every code block / URL / heading preserved?)
- Readability proxy (average sentence length, burstiness stddev)

Results live in `snapshots/<timestamp>/` as JSON plus a plain-text summary.

## Running

```bash
python3 evals/llm_run.py --prompts evals/prompts --out evals/snapshots
python3 evals/measure.py evals/snapshots/<timestamp>
python3 evals/plot.py evals/snapshots/<timestamp>           # optional, needs plotly
```

Set `ANTHROPIC_API_KEY` to actually call the LLM. Without it, `llm_run.py`
falls back to the `claude` CLI on `PATH`. If neither is available, the
`llm` condition is marked as `skipped` and only the deterministic pass runs.

`plot.py` reads `measure.json` and writes `plot.html` (interactive) and
`plot.png` (static, requires `kaleido`) into the snapshot directory. Embed
the PNG in PRs or release notes to make AI-ism trends visible at a glance.

```bash
pip install plotly kaleido    # one-time, only needed for plot.py
```

## Baseline snapshot

`evals/snapshots/` contains a committed baseline run so future PRs can be
diffed against a known reference. Re-run the full eval whenever you change
`scripts/humanize.py`, `scripts/validate.py`, or the prompt set, and replace
the baseline if the new numbers are equal-or-better.

## Adding new prompts

Drop a plain text file under `evals/prompts/`. Filename stem becomes the
prompt ID. Each prompt should be the raw user-facing request — do not
include a system prompt. The harness is responsible for that.

## Gates

CI should fail if any of the following holds on the latest snapshot:

- `deterministic.ai_isms > baseline.ai_isms` for any prompt.
- `deterministic.structural_errors > 0`.
- `llm.structural_errors > 0` (when `llm` was not skipped).

These gates are enforced by `measure.py --fail-on-regression`.
