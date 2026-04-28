# Unslop Benchmarks

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
| `delta` | `before - after`. Higher = unslop found more to strip |
| `words_before` / `words_after` | Word count before/after (expect a small drop) |
| `sentence_count_before` / `sentence_count_after` | Prose sentence count used for burstiness checks |
| `burstiness_before` / `burstiness_after` | Sentence-length stddev (higher = more human rhythm) |
| `burstiness_delta` | `after - before` |
| `structural_ok` | True iff `validate(original, humanized).ok` |

## Gates

`run.py --strict` fails with exit 2 if:

- any fixture has `delta < 0` (unslop made AI-isms *worse*)
- any fixture has `structural_ok == False` (unslop broke preservation)
- any fixture with baseline human-like rhythm (`burstiness_before >= 4`, `sentence_count_after >= 8`) is flattened below the burstiness floor (`burstiness_after < 4`)

These are the same gates applied in `evals/measure.py`, but offline.

## Intensity matrix

```bash
python3 benchmarks/run.py --all-intensities --strict
```

Runs the harness at `subtle`, `balanced`, and `full` and writes a combined matrix to `benchmarks/results/<stamp>-matrix.json`. `--strict` adds a monotonicity gate: each intensity must strip at least as many AI-isms as the level below it. This is how we keep `subtle ≤ balanced ≤ full` honest.

Current baseline (4 fixtures, 148 total AI-isms):

| Intensity  | After | Delta | % reduction |
| ---------- | ----- | ----- | ----------- |
| subtle     | 55    | 93    | 62.8%       |
| balanced   | 18    | 130   | 87.8%       |
| full       | 13    | 135   | 91.2%       |

## Stylometric baseline

```bash
python3 benchmarks/stylometric_baseline.py \
  --human benchmarks/fixtures/human_corpus \
  --llm benchmarks/fixtures/llm_corpus \
  --out benchmarks/results/stylometric_baseline.json
```

The harness measures every numeric `StyleProfile` field and writes p25, median,
and p75 bands for both corpora. Use a published human corpus subset for release
baselines; the script does not ship invented target numbers.

## Detector eval (opt-in, heavy)

Rule-counting is necessary but not sufficient. It counts whether known AI phrases left the document; it doesn't measure whether a modern transformer-based AI detector still flags the humanized output. `benchmarks/detector_bench.py` closes that gap by scoring each fixture (original + every intensity) through two SOTA open detectors:

- **TMR AI Text Detector** (`Oxidane/tmr-ai-text-detector`, RoBERTa-base, 99.28% AUROC on RAID)
- **Desklib v1.01** (`desklib/ai-text-detector-v1.01`, DeBERTa-v3-large)

```bash
pip install torch transformers huggingface_hub safetensors
python3 benchmarks/detector_bench.py --tmr-only   # ~800MB download
python3 benchmarks/detector_bench.py              # full: ~2GB download
python3 benchmarks/detector_bench.py --strict     # fails if balanced doesn't beat original
```

### Honest finding from the existing run (TMR, 3 fixtures)

| Fixture                         | Original | Subtle | Balanced | Full   |
| ------------------------------- | -------: | -----: | -------: | -----: |
| ai-slop-expanded-categories.md  |   98.6%  | 98.5%  |   98.4%  | 98.4%  |
| ai-slop-release-notes.md        |   98.6%  | 98.5%  |   98.4%  | 98.4%  |
| ai-slop-tutorial.md             |   98.5%  | 98.4%  |   98.3%  | 98.3%  |

Deterministic rule-stripping alone moves the TMR probability by 0.1–0.2 percentage points. That aligns with Cat 05 research (adversarial paraphrasing, DIPPER): stylometric fingerprints survive vocabulary substitution. The LLM pass + `anti-detector` intensity in `SKILL.md` is the path that moves this number; rules alone are not an evasion tool and by design we are not shipping a plagiarism-laundering product.

What the rule pass *does* do, verifiably, is remove the lexical tells a human reader sees (the `run.py --all-intensities` table above). That is the claim the project makes and can back up with evidence.

## Reference comparisons

Two comparison harnesses are available when the external repos and model weights
are present:

```bash
git clone https://github.com/IBM/diveye /tmp/ibm-diveye
python3 benchmarks/diveye_comparison/run.py

git clone https://github.com/chengez/Adversarial-Paraphrasing /tmp/chengez-adv
python3 benchmarks/adversarial_paraphrasing_comparison/run.py
```

They write JSON plus markdown summaries under `benchmarks/results/`. Do not
commit cloned repos or model weights.
