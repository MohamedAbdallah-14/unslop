# Humanizer Benchmarks

Offline, deterministic benchmark harness. No API calls. Run locally or in CI
to confirm the regex pass is doing measurable work on a fixed corpus of
AI-slop samples.

## Running

```bash
python3 benchmarks/run.py
```

Outputs:

- `benchmarks/results/<UTC-timestamp>.json` — full per-file breakdown
- `benchmarks/results/latest.json` — symlink / copy of the newest run for CI diffing

## What it measures

For every fixture under `benchmarks/fixtures/*.md`:

| Metric | Meaning |
|---|---|
| `ai_isms_before` | Count of AI-ism regex matches in the original |
| `ai_isms_after` | Count after `humanize_deterministic` |
| `delta` | `before - after`. Higher = humanizer found more to strip |
| `words_before` / `words_after` | Word count before/after (expect a small drop) |
| `structural_ok` | True iff `validate(original, humanized).ok` |

## Gates

`run.py --strict` fails with exit 2 if:

- any fixture has `delta < 0` (humanizer made AI-isms *worse*)
- any fixture has `structural_ok == False` (humanizer broke preservation)

These are the same gates applied in `evals/measure.py`, but offline.
