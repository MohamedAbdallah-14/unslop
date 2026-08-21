# Agent #80 — unslop `detector.py` TMR Feedback Loop: State of Art vs Gap

**Topic:** Audit current detector feedback implementation against the 2026 detection stack (DivEye, TSD, SurpMark, GPTZero v6, commercial)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for detector refresh planning  
**Scope:** `unslop/scripts/detector.py`, `surprisal.py`, `structural.py`, `humanize.py`, `evals/`, `benchmarks/`  
**Cross-refs:** Agent #01 (DivEye), #02 (TSD), #03 (SurpMark), #12 (DAMAGE), #13 (GPTZero v6), #34 (IBM DivEye impl), #55 (surprisal dynamics), #67 (marketing vs audit)

---

## Executive summary

unslop ships a **working but narrow** detector feedback loop: load TMR (default) or Desklib, score AI probability, escalate deterministic humanization until `p_ai ≤ target` or the ladder exhausts. The architecture is sound for **local, offline, supervised-classifier regression** — lazy imports, HF cache, injection points for tests, graceful `DetectorUnavailable` degradation, EU Art. 50 refusal at ladder exhaustion.

It is **not aligned with the 2026 detection frontier**. The loop optimizes one scalar from a **125M RoBERTa RAID classifier** while state-of-art and commercial stacks fuse **token surprisal dynamics** (DivEye, TSD, SurpMark), **humanizer-red-team supervised models** (GPTZero 4.x, Pangram DAMAGE), and **process provenance** (Authorship/Replay). Empirical evidence in-repo confirms the gap: deterministic rule-stripping moves TMR probability by **0.1–0.2 percentage points** on slop fixtures; the feedback loop never runs in CI; `evals/` never scores detectors; `--surprisal-variance` is not wired into `--detector-feedback`.

**Verdict:** `detector.py` is a **Phase-1 release gate** (prove rules don't *raise* TMR), not an anti-detector optimizer. Closing the gap requires (1) multi-signal scoring, (2) surprisal-aware stop/escalation, (3) feedback-loop benchmarks against DivEye/TSD/SurpMark proxies, (4) optional commercial API eval harness — without claiming GPTZero/Turnitin pass.

---

## 1. Current implementation map

### 1.1 `detector.py` — core contract

| Component | Behavior |
|-----------|----------|
| **Backends** | `tmr` → `Oxidane/tmr-ai-text-detector` (RoBERTa-base, softmax class 1); `desklib` → `desklib/ai-text-detector-v1.01` (DeBERTa-v3-large + custom head, sigmoid) |
| **Scoring** | Long docs chunked at 512 tokens, stride 256, **mean of up to 4 chunks** |
| **Cache** | Per-process `_SCORER_CACHE`; first load ~10–30s |
| **Skip** | `ANTHROPIC_UNSLOP_SKIP_DETECTOR=1` |
| **Bootstrap** | `python3 -m unslop.scripts.fetch_detectors` |

**`feedback_loop()` semantics:**

```
original_prob = score(original)
for each ladder step (intensity, structural, soul):
    out = humanize_deterministic_with_report(ORIGINAL, ...)   # ← not chained
    prob = score(out)
    log ai_isms, optional surprisal_stdev
    if prob <= target: return early
return best out + exhaustion recommendation (cross-model paraphrase; no watermark strip)
```

**Design notes (material for gap analysis):**

1. **Non-cumulative rewrites.** Each iteration humanizes the **original** text with stronger settings, not the previous iteration's output. Escalation is "try harder settings on source," not iterative refinement. Tests encode this (`test_detector.py`).

2. **Deterministic-only inner loop.** `humanize_fn` defaults to `humanize_deterministic_with_report`. LLM `anti-detector` mode is **outside** the loop unless injected.

3. **Ladder excludes `anti-detector`.** `DEFAULT_LADDER`: balanced → full → full+structural+soul. `LADDER_AGGRESSIVE`: subtle through full+structural+soul (5 steps). Neither uses `intensity="anti-detector"` or `lexical_targets.apply_targeted_pass`.

4. **Surprisal is telemetry-only.** `surprisal_fn` optional; records `surprisal_stdev` per iteration. **Not** a stop condition, ladder branch, or optimization target. CLI `--detector-feedback` does **not** pass `surprisal_fn`.

5. **Single-objective stop.** Only `p_ai <= target` (default 0.5, per-detector dict supported). No multi-arm gate (ESL FPR cap, structural preservation, surprisal floor).

6. **Chunk cap risk.** `max_chunks=4` truncates long documents before mean aggregation. DivEye/TSD/SurpMark use up to 1024+ tokens of surprisal trajectory; TSD specifically scores **second half** — front-loaded chunk scoring can miss the signal.

### 1.2 CLI integration (`cli.py`)

| Flag | Wired? |
|------|--------|
| `--detector-feedback` | Yes → `feedback_loop` / `feedback_loop_aggressive` |
| `--detector-target` | Yes (default 0.5) |
| `--detector-model` | Yes (`tmr` / `desklib`) |
| `--detector-max-iterations` | Yes |
| `--detector-loop-aggressive` | Yes (5-step ladder) |
| `--surprisal-variance` | **Separate one-shot**; not combined with detector feedback |
| `--mode anti-detector` | **Not** auto-enabled by detector feedback |

On `DetectorUnavailable`, CLI exits 1 (stdin) or degrades with stderr message (file mode).

### 1.3 Supporting modules

#### `surprisal.py` — DivEye feature extraction (measurement only)

- Loads causal LM (default **distilgpt2**, 82M); computes full DivEye-aligned vector: mean log-prob, σ, variance, skew, kurtosis, Δ and Δ² dynamics, entropy, autocorr.
- `to_diveye_vector()` matches IBM `diveye_utils.py` on GPT-2 (`benchmarks/results/diveye_comparison.json`: **max relative error 0.0000** on 9 fixtures).
- **Gap vs paper/HF Space:** DivEye production uses **GPT-2 / Falcon-7B + XGBoost classifier**, not raw σ. unslop computes features but has **no XGBoost head**, no BiScope fusion, no `model.json` from HF Space.
- Default observer **distilgpt2 ≠ GPT-2** used in IBM validation bench.

#### `structural.py` — sentence-length σ (orthogonal axis)

- `split_long_sentences`: lifts paragraph sentence-length σ when σ < 5.0 (human ~8.2, GPT-4o ~4.1 per module docstring).
- `merge_bullet_soup`: collapses parallel short bullets.
- **Does not** touch token surprisal, TSD second-half volatility, or SurpMark transition matrices.
- Research citation in-module: lexical-only paraphrase **raises** detector TPR 8–15% (Adversarial Paraphrasing); structural pass is the corrective layer.

#### `humanize.py` — pipeline the loop drives

| Intensity | Structural default | Soul default | Detector-specific |
|-----------|-------------------|--------------|-------------------|
| subtle | off | off | stock vocab only |
| balanced | on | on | full lexical family |
| full | on | on | + filler, negative-parallelism, superficial-ing |
| anti-detector | on | on | + `lexical_targets.apply_targeted_pass` (stylometric band nudges) |

**Gap:** feedback loop never reaches `anti-detector` or LLM rewrite. `lexical_targets` nudges contraction rate, sentence-length CV, word-length σ — **proxies** for DivEye, not TSD/SurpMark dynamics.

#### `stylometry.py` + `lexical_targets.py`

- Deterministic proxies: `sentence_length_cv`, `word_length_stdev`, fragment rate, contraction rate, etc.
- Baselines from `benchmarks/results/stylometric_baseline.json` (p25–p75 human bands).
- Used only when `intensity == "anti-detector"` — **not** in feedback ladder.

### 1.4 Tests

`tests/unslop/test_detector.py`: mock scorer only. Covers early stop, exhaustion, ladder order, aggressive wrapper, per-detector threshold dict, surprisal logging hook, serialization. **No integration test** with real TMR weights (by design — opt-in bench).

---

## 2. Eval and benchmark coverage

### 2.1 `evals/` — no detector dimension

| Metric | Measured | Detector? |
|--------|----------|-----------|
| AI-ism count | Yes | No |
| Structural preservation | Yes | No |
| Burstiness (sentence-length σ) | Yes | No |
| Word count / avg sentence len | Yes | No |

CI gate (`measure.py --fail-on-regression`): AI-isms must not increase; no structural breaks. **Zero** TMR/Desklib/GPTZero scoring. Perceived humanness eval (`perceived_humanness.py`) is LLM-judge, not detector.

### 2.2 `benchmarks/run.py` — rule efficacy, not evasion

- Default intensity `balanced`; gates on AI-ism delta, structural OK, burstiness floor.
- Latest run (20260428): 229 → 18 AI-isms (92.1% reduction) across 9 fixtures; several fixtures show **burstiness_delta negative** (rhythm flattened slightly while stripping slop).
- **`anti-detector` not in default matrix** (`--all-intensities` stops at full).

### 2.3 `benchmarks/detector_bench.py` — single-pass, no feedback loop

- Scores original + each intensity (`subtle`, `balanced`, `full`) through TMR and Desklib.
- **Does not** enable structural/soul explicitly (relies on intensity defaults — balanced/full get structural+soul).
- **Does not** run `feedback_loop()`.
- **No committed `*-detectors.json`** in repo at audit time; README embeds honest TMR numbers from a 3-fixture run:

| Fixture | Original | Subtle | Balanced | Full |
|---------|----------|--------|----------|------|
| ai-slop-expanded-categories.md | 98.6% | 98.5% | 98.4% | 98.4% |
| ai-slop-release-notes.md | 98.6% | 98.5% | 98.4% | 98.4% |
| ai-slop-tutorial.md | 98.5% | 98.4% | 98.3% | 98.3% |

**Interpretation:** Lexical+structural deterministic pass is **not** an evasion tool against TMR on heavy slop. Matches DAMAGE Table 3 pattern for legacy detectors under humanization — but here the "humanizer" is regex, not DIPPER.

### 2.4 `benchmarks/diveye_comparison/run.py`

- Validates `surprisal.py` **feature parity** with IBM reference (GPT-2).
- Does **not** score humanized vs original through DivEye classifier.
- Does **not** connect to `feedback_loop`.

### 2.5 Coverage matrix

| Capability | evals | run.py | detector_bench | feedback_loop |
|------------|-------|--------|----------------|---------------|
| AI-ism delta | ✓ | ✓ | — | logged per iter |
| Structural OK | ✓ | ✓ | — | implicit via humanize |
| Burstiness proxy | ✓ | ✓ | — | — |
| TMR p(AI) | — | — | ✓ single-pass | ✓ multi-step |
| Desklib p(AI) | — | — | ✓ | ✓ |
| DivEye features | — | — | parity only | telemetry optional |
| TSD / SurpMark | — | — | — | — |
| GPTZero API | — | — | — | — |
| Feedback loop regression | — | — | — | **untested in CI** |
| anti-detector intensity | — | partial | — | **excluded** |

---

## 3. 2026 detector stack — what unslop faces

### 3.1 DivEye (TMLR 2026) — global surprisal dynamics

| Aspect | State of art | unslop |
|--------|--------------|--------|
| Signal | 9-dim surprisal vector + XGBoost | 9-dim computed; **no classifier** |
| Observer LM | GPT-2 / Falcon-7B | distilgpt2 default |
| Paraphrase robustness | σ, Δ² features survive (paper + HumanizeMyAI replication) | structural + soul widen σ **proxy**; no Δ² optimization |
| RAID AUROC | 0.984 fused | Not measured |
| In feedback loop | N/A (academic) | **Logged only** |

**Gap severity: HIGH** for measurement parity, **MEDIUM** for loop control (features exist but unused).

### 3.2 TSD (arXiv:2601.04833, Jan 2026) — late-stage volatility decay

| Aspect | State of art | unslop |
|--------|--------------|--------|
| Signal | DD + LV on **second half** only | Not implemented |
| Mechanism | AI surprisal settles 24–32% faster | Global σ only |
| Fusion | TSD + Fast-DetectGPT → 85%+ AUROC | — |
| Code | No official repo | — |

**Gap severity: HIGH.** unslop can widen global burstiness while **back half stays flat** — exactly TSD's target.

### 3.3 SurpMark (ICML 2026) — transition-matrix GJS

| Aspect | State of art | unslop |
|--------|--------------|--------|
| Signal | k-means surprisal states → Markov matrix → ΔGJS vs human/machine refs | Not implemented |
| Paraphrase | 99%+ AUROC under Polish/DIPPER (paper Table 9) | — |
| Recovery phenomenon | Machine snaps to predictable glue after spikes | soul/contractions don't model transitions |
| Official code | github.com/shuangyichen/SurpMark | — |

**Gap severity: HIGH** for evasion-aware rewriting; unslop has no transition-matrix feedback.

### 3.4 GPTZero v6 / 4.x (commercial, Jan 2026+)

| Aspect | State of art | unslop |
|--------|--------------|--------|
| Architecture | Deep classifier; predictability-cone features (practitioner term); humanizer red-team | TMR proxy only |
| Bypass recall | 4.3b: 91.8% on vendor humanizer panel | Not tested |
| Independent eval | Booth: 82–89% accuracy, 14–50% FPR ESL; paraphrase drops recall | — |
| API | `predicted_class`, model version strings | No integration |
| Process shift | Authorship/Replay (Superhuman acquisition) | Out of scope for post-hoc loop |

**Gap severity: CRITICAL** for user-facing claims. TMR ≠ GPTZero. Optimizing TMR can diverge from commercial targets (Agent #67: report corpus + FPR cap always).

### 3.5 Commercial ensemble (Turnitin, Pangram, Copyleaks)

| Detector | 2026 note | vs unslop loop |
|----------|-----------|----------------|
| **Turnitin** | AI bypasser layer retained post–Jul 2026 report change (Agent #56) | No API; different feature stack |
| **Pangram DAMAGE** | Mistral-NeMo + humanizer-augmented training; holds ~98% on L1 pool where GPTZero → 60% | TMR is RAID open-weight, not DAMAGE-trained |
| **Copyleaks v9** | Multi-signal + paraphrase detection | Not integrated |
| **Originality.ai** | Allowance scoring + AI | Not integrated |

**Gap severity: CRITICAL** for institutional users. Loop optimizes open RAID classifier, not what students actually hit.

---

## 4. Gap synthesis

### 4.1 Architecture gaps

```
2026 target stack                          unslop today
─────────────────                          ────────────
[TMR/Desklib supervised]                 ✓ score_ai_probability
[DivEye XGBoost on surprisal vector]     ✗ features only (surprisal.py)
[TSD second-half DD/LV]                  ✗
[SurpMark ΔGJS transitions]              ✗
[GPTZero/Pangram API eval]               ✗
[Multi-objective stop]                   ✗ single p_ai
[Chain or LLM in loop]                   ✗ deterministic, from-original
[anti-detector in ladder]                ✗
[Position-aware surprisal optimize]        ✗
```

### 4.2 Signal alignment table

| Signal | Detected by 2026 stack | Addressed by unslop loop | Module |
|--------|------------------------|--------------------------|--------|
| Stock vocabulary / AI-isms | All | **Yes** (primary win) | humanize.py |
| Sentence-length uniformity | GPTZero legacy, structural detectors | Partial (step 3 ladder) | structural.py |
| Global surprisal σ | DivEye, cones | Proxy only; not optimized | surprisal.py (read) |
| Δ² entropy / autocorr | DivEye | Computed, ignored | surprisal.py |
| Second-half volatility | TSD | **No** | — |
| Surprisal state transitions | SurpMark | **No** | — |
| Supervised embedding fingerprint | TMR, Desklib, GPTZero 4.x | TMR only | detector.py |
| Humanizer-augmented robustness | DAMAGE, GPTZero 3.15b+ | **No** (regex ≠ L1 humanizer pool) | — |
| Process provenance | Authorship/Replay | **No** (post-hoc limit) | — |

### 4.3 Honest efficacy statement (repo-backed)

1. **Rules reduce human-visible slop** — 92%+ AI-ism reduction on fixtures (`benchmarks/results/latest.json`).
2. **Rules barely move TMR** — ~0.1–0.2 pp on 98%+ slop (`benchmarks/README.md` §Detector eval).
3. **Feedback loop untested end-to-end** — no CI bench, no committed loop audit JSON.
4. **Surprisal parity proven** — IBM vector match on GPT-2; default distilgpt2 uncertified in bench.
5. **Exhaustion path is ethically correct** — recommends cross-model paraphrase, refuses watermark strip (Art. 50).

This matches Agent #12 (DAMAGE): legacy detectors collapse under humanization; unslop's deterministic pass is **weaker than L1 commercial humanizers** for TMR movement — consistent with not shipping a bypass product.

---

## 5. Risk register

| Risk | Cause | Mitigation |
|------|-------|------------|
| **False confidence** | User runs `--detector-feedback`, sees 0.49 p_ai on TMR, submits to GPTZero | Document TMR ≠ commercial; log model IDs; never promise pass |
| **Wrong optimization target** | TMR gradient ≠ DivEye/TSD/SurpMark | Multi-signal panel before claiming anti-detector efficacy |
| **ESL collateral** | Aggressive ladder + soul/contractions native-washes L2 voice | Keep default ladder conservative; voice-match for identity preservation (Agent #78) |
| **Chunk truncation** | 4-chunk cap on long essays | Raise cap or score full doc for loop decisions |
| **Non-chaining** | Each step re-processes original | Document behavior; consider chained mode for LLM second pass |
| **distilgpt2 miscalibration** | Default LM ≠ validated GPT-2 | Align default with diveye_comparison model or label readings uncertified |

---

## 6. Recommendations (prioritized)

### P0 — Honesty & measurement (no new evasion claims)

| # | Action | Rationale |
|---|--------|-----------|
| 1 | Run `detector_bench.py` on full 9-fixture corpus + commit JSON | Baseline evidence for refresh |
| 2 | Add `benchmarks/detector_feedback_bench.py`: mock + optional TMR, run `feedback_loop` on fixtures | Close CI gap on loop semantics |
| 3 | README/SKILL: "TMR feedback ≠ GPTZero/Turnitin pass" with link to this memo | Agent #67 compliance |
| 4 | Wire `--surprisal-variance` telemetry into `--detector-feedback` JSON output (CLI one-line change) | Free observability |

### P1 — Signal expansion (defensive ESL scope)

| # | Action | Rationale |
|---|--------|-----------|
| 5 | Add `surprisal.py`: `compute_tsd_features()` — second-half DD/LV | Agent #02; ~20 LOC on existing tensor |
| 6 | Multi-metric `IterationRecord`: TMR + `surprisal_stdev` + TSD score + optional Δ² entropy | Enables Pareto stop (p_ai AND σ floor) |
| 7 | Extend ladder final step to `anti-detector` intensity | Uses existing `lexical_targets` |
| 8 | Change default surprisal LM to `gpt2` (validated) or document distilgpt2 as uncertified | Parity with diveye_comparison |
| 9 | `detector_bench.py`: add `structural`/`soul`/`anti-detector` matrix + feedback_loop column | Measure what loop actually does |

### P2 — Research integration (optional, heavy)

| # | Action | Rationale |
|---|--------|-----------|
| 10 | SurpMark ΔGJS as optional third score (reference matrices from paper repo) | Agent #03; paraphrase-robust signal |
| 11 | DivEye XGBoost head (HF Space `model.json`) as optional backend | Closes academic SOTA gap |
| 12 | GPTZero API eval harness (opt-in, version-pinned, no CI dependency) | User-facing ground truth |
| 13 | Chained feedback mode: each iter builds on prior output | May help TMR; test for structural regression |
| 14 | LLM step after ladder exhaustion (not before) | Matches exhaustion recommendation with guardrails |

### P3 — Explicit non-goals

- Watermark detector or strip optimization (Agents #71–75, #76)
- Marketing "beat Turnitin" / "EU undetectable"
- Automatic LLM paraphrase inside loop without user consent
- Using detector pass as academic integrity gate

---

## 7. Proposed target architecture (2026-aligned)

```
                    ┌─────────────────────────────────────┐
                    │         Input text                   │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │   humanize ladder (deterministic)    │
                    │   subtle → balanced → full →         │
                    │   anti-detector (+ structural/soul)  │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
   ┌─────────────┐           ┌───────────────┐           ┌─────────────────┐
   │ TMR/Desklib │           │ surprisal.py  │           │ TSD features    │
   │  p(AI)      │           │ DivEye vector │           │ (2nd-half DD/LV)│
   └──────┬──────┘           └───────┬───────┘           └────────┬────────┘
          │                           │                            │
          └───────────────────────────┼────────────────────────────┘
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  Multi-signal stop policy            │
                    │  p_ai ≤ τ AND σ ≥ σ* AND TSD ≥ t*   │
                    │  (optional SurpMark ΔGJS band)       │
                    └─────────────────┬───────────────────┘
                                      │ miss all
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  Exhaust: recommend cross-model LLM  │
                    │  (user-initiated; Art. 50 refusal)   │
                    └─────────────────────────────────────┘
```

Today only the left branch exists; center is log-only; right branch is absent.

---

## 8. Code anchors

| File | Lines (approx) | Role |
|------|----------------|------|
| `unslop/scripts/detector.py` | 1–437 | Scorers, `feedback_loop`, ladders |
| `unslop/scripts/surprisal.py` | 211–297 | DivEye feature computation |
| `unslop/scripts/structural.py` | 174–249 | Sentence-length σ pass |
| `unslop/scripts/humanize.py` | 1119–1126 | anti-detector lexical targets |
| `unslop/scripts/cli.py` | 319–340, 658–680 | Detector feedback + surprisal CLI |
| `benchmarks/detector_bench.py` | 192–276 | Single-pass TMR/Desklib bench |
| `benchmarks/README.md` | 86–94 | Honest TMR delta evidence |
| `tests/unslop/test_detector.py` | 63–187 | Mock loop tests |

---

## 9. Open questions

1. **Should feedback loop chain iterations** (out_{i} → in_{i+1}) or keep independent escalation from original? Chaining may compound structural damage; independent steps are safer but waste prior work.

2. **Is TMR the right default target** if users hit GPTZero? Consider making "panel mode" opt-in with explicit "educational detector ≠ TMR" disclaimer.

3. **Does anti-detector + feedback loop violate Boundaries** if user intent is ESL defense but TMR drops materially on AI slop fixtures? Policy says defensive use OK; bench numbers must not become marketing.

4. **distilgpt2 vs gpt2** for production surprisal telemetry — performance vs parity tradeoff.

5. **Commit detector bench artifacts** — storage vs reproducibility; maybe CI weekly not per-PR.

---

## 10. One-paragraph unslop verdict

`detector.py` implements the **right pattern** (score → escalate → audit → honest exhaustion) for an offline maintainer tool, and the **wrong detector generation** for 2026 user expectations. TMR is a RAID-era supervised checkpoint; DivEye, TSD, and SurpMark moved detection to **surprisal dynamics**; GPTZero 4.x and Pangram DAMAGE moved commercial stacks to **humanizer-augmented classifiers** and process provenance. unslop already **computes** DivEye features and **applies** structural burstiness fixes but **does not close the loop** on those signals — the feedback optimizer listens only to TMR, which barely budges on deterministic passes anyway. Next work: expand the score panel, wire surprisal/TSD into stop policy, bench the full feedback loop, and keep commercial pass out of marketing.

---

*Feeds into [`UPDATE-PLAN-2026-08.md`](./UPDATE-PLAN-2026-08.md) and Agent #80 row in [`AGENT-MANIFEST-100.md`](./AGENT-MANIFEST-100.md).*
