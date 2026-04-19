# Humanizer Evals

Quick A/B harness to answer: "does the humanizer make output measurably less
AI-ish without breaking structure?"

Three conditions per prompt:

| Condition | What the model sees |
|---|---|
| `baseline` | Prompt only. No humanizer rules, no deterministic pass. |
| `deterministic` | Baseline response run through the regex humanizer. |
| `llm` | Baseline response run through the LLM humanizer (Anthropic SDK or `claude` CLI). |

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
```

Set `ANTHROPIC_API_KEY` to actually call the LLM. Without it, `llm_run.py`
falls back to deterministic-only mode and marks the `llm` condition as
`skipped`.

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
