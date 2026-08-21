# SYNTH-83 — Detection Code/Gap Analysis

**Synthesis agent:** #83  
**Date:** 2026-08-19  
**Inputs:** Agent #34 (IBM DivEye impl), #80 (detector.py gap audit), #01 (DivEye theory), #49 (burstiness), #54 (sentence-length variance), #55 (TSD/SurpMark dynamics), `UPDATE-PLAN-2026-08.md`  
**Code read:** `unslop/scripts/detector.py`, `surprisal.py`, `structural.py` (+ CLI, tests, benchmarks cross-check)

---

## Executive summary

unslop's detection stack is **architecturally sound but generationally behind**. Three modules cover three orthogonal axes:

| Module | Axis | Status |
|--------|------|--------|
| `humanize.py` + validator | Lexical AI-isms | **Strong** — primary win, 92%+ AI-ism reduction on fixtures |
| `structural.py` | Syntactic burstiness (sentence-length σ) | **Moderate** — split-only restorer; half the human rhythm problem |
| `surprisal.py` | Token surprisal dynamics (DivEye vector) | **Measure only** — bit-matched to IBM code; not a stop condition |
| `detector.py` | Supervised classifier feedback (TMR/Desklib) | **Narrow loop** — single scalar, barely moves on deterministic passes |

The 2026 frontier fused **five largely independent signals**: lexical tells, sentence-length variance, global surprisal dynamics (DivEye), **position-aware** late-stage volatility (TSD), and **transition-matrix** recovery patterns (SurpMark), plus commercial stacks (GPTZero v6 cones, Pangram DAMAGE humanizer-augmented training). unslop addresses signals 1–2 well, computes signal 3 without closing the loop, and has **zero code** for signals 4–5.

**Honest efficacy (repo-backed):** Deterministic humanization drops AI-isms but moves TMR probability by ~0.1–0.2 pp on 98%+ slop fixtures. The feedback loop is mock-tested only; no CI regression on real weights or loop semantics. DivEye feature parity with IBM is proven (`benchmarks/results/diveye_comparison.json`); distilgpt2 default is not.

**Verdict:** `detector.py` is a Phase-1 **release gate** (rules don't raise TMR), not a 2026 anti-detector optimizer. Next work is wiring existing measurement into multi-signal stop policy, then TSD/SurpMark implementation — not more regex.

---

## 1. What unslop has today

### 1.1 `detector.py` — supervised feedback loop

**Shipped:**

- Two HF backends: `tmr` (RoBERTa-base, default) and `desklib` (DeBERTa-v3-large)
- `score_ai_probability(text)` → [0, 1]; lazy torch import; per-process cache
- `feedback_loop()` / `feedback_loop_aggressive()` with escalation ladder
- `DetectorUnavailable` + `ANTHROPIC_UNSLOP_SKIP_DETECTOR=1` graceful degradation
- `IterationRecord` audit trail (intensity, structural, soul, ai_probability, ai_isms, optional surprisal_stdev)
- Exhaustion recommendation: cross-model paraphrase; explicit EU Art. 50 watermark refusal
- Test injection points (`score_fn`, `humanize_fn`, `surprisal_fn`)

**Semantics (material):**

1. **Non-cumulative rewrites** — each ladder step humanizes the **original** text with stronger settings, not the prior iteration output.
2. **Deterministic-only inner loop** — defaults to `humanize_deterministic_with_report`; no LLM `anti-detector` unless injected.
3. **Ladder caps at `full+structural+soul`** — never reaches `anti-detector` or `lexical_targets.apply_targeted_pass`.
4. **Single-objective stop** — `p_ai ≤ target` (default 0.5) only.
5. **Chunk cap** — mean of up to 4 × 512-token chunks; long essays truncated for scoring.

**Default ladder:**

```
(balanced, structural=off, soul=off)
→ (full, structural=off, soul=off)
→ (full, structural=on, soul=on)
```

Aggressive ladder adds `subtle` and intermediate structural steps (5 total); still no `anti-detector`.

### 1.2 `surprisal.py` — DivEye feature extraction

**Shipped:**

- `compute_surprisal_variance()` — full 10-feature IBM-aligned vector
- Fields: mean log-prob, σ, variance, skew, kurtosis, Δ mean/std, Δ² variance/entropy/autocorr, CV
- `to_diveye_vector()` — 10-dim export matching IBM `diveye_utils.py`
- `SurprisalUnavailable` + `UNSLOP_SKIP_SURPRISAL=1`; `is_available()` probe
- Default LM: **distilgpt2** (82M); 1024-token truncation
- CLI: `--surprisal-variance` (one-shot JSON dump)

**Proven alignment (Agent #34):**

- GPT-2: max relative error < 3×10⁻⁶ across 9 fixtures
- Tracks **IBM shipped code** (10 dims), not paper Eq. 6 (9 dims)

**Not shipped:**

- XGBoost / HF Space `model.json` classifier head
- BiScope fusion, zlib compression ratio (HF Space 83-dim ensemble)
- TSD second-half DD/LV
- SurpMark k-means transitions + ΔGJS
- Position-aware or half-sequence APIs
- Feedback-loop stop on any surprisal metric

### 1.3 `structural.py` — syntactic burstiness

**Shipped:**

- `split_long_sentences()` — flat-paragraph detection (σ < 5.0), split at safe boundaries (semicolon, `, but`, em-dash, etc.)
- `merge_bullet_soup()` — collapse ≥3 parallel short bullets (same first word)
- `humanize_structural()` — split then merge; `StructuralReport` counts
- Operates on `_protect()` placeholder text; one split per sentence per pass

**Thresholds:**

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| `target_sigma` | 5.0 | AI band ~4; human practitioner ~8.2 |
| `min_words` / `flat_min_words` | 30 / 20 | Overlong vs flat-paragraph regime |
| Validator burstiness floor | σ < 4 (doc), σ < 3 (flat para) | `validate.py` alignment |

**Asymmetry (Agent #54):** Split-only. No deterministic fragment injection, no adjacent-short merge, no gamma/CV targeting. Short-sentence tail lives in LLM anti-detector mode only.

### 1.4 Integration map

| Path | Detector | Surprisal | Structural | anti-detector |
|------|----------|-----------|------------|---------------|
| CLI `--detector-feedback` | ✅ | ❌ not wired | via ladder step 3 | ❌ |
| CLI `--surprisal-variance` | — | ✅ one-shot | — | — |
| `evals/measure.py` CI gate | ❌ | ❌ | burstiness proxy only | ❌ |
| `benchmarks/run.py` | ❌ | ❌ | burstiness delta | partial (no anti-detector in default matrix) |
| `benchmarks/detector_bench.py` | ✅ single-pass | ❌ | via intensity defaults | ❌ |
| `benchmarks/diveye_comparison/` | ❌ | ✅ parity only | ❌ | ❌ |

---

## 2. 2026 detection stack — what unslop faces

### 2.1 Five-signal model (from UPDATE-PLAN + Agent #80)

```
Signal 1: Lexical AI-isms          → humanize.py          ✅ strong
Signal 2: Sentence-length σ (CV)   → structural.py        ⚠️ moderate (split-only)
Signal 3: Global surprisal dynamics → surprisal.py         ⚠️ measure only
Signal 4: Late-stage volatility    → TSD (arXiv:2601.04833) ❌ absent
Signal 5: Predictability cones     → GPTZero v6           ❌ absent
Cross: Transition recovery         → SurpMark (ICML 2026) ❌ absent
Supervised: RAID classifiers       → detector.py          ✅ TMR only
Commercial: Humanizer-red-team     → GPTZero 4.x, DAMAGE  ❌ not integrated
```

### 2.2 Stack comparison table

| Method | Core signal | Paraphrase robustness | unslop coverage |
|--------|-------------|----------------------|-----------------|
| **DivEye** (TMLR 2026) | 10-dim surprisal vector + XGBoost | High (σ, Δ² survive) | Features ✅; classifier ❌ |
| **TSD** (Jan 2026) | DD + LV on **second half** only | Medium–high | ❌ |
| **SurpMark** (ICML 2026) | k-state transition ΔGJS | Very high (~99% under Polish/DIPPER) | ❌ |
| **TMR / Desklib** | Supervised RoBERTa/DeBERTa | Low vs L1 humanizers | ✅ score only |
| **GPTZero v6** | Cones + deep classifier + red-team | High vs synonym swap | ❌ |
| **Pangram DAMAGE** | Mistral-NeMo + humanizer training | Holds ~98% on L1 pool | ❌ |
| **Fast-DetectGPT / Binoculars** | Curvature / cross-PPL | Moderate | ❌ |
| **Sentence-length σ** | Desaire #8, stylometry | Survives synonym swap | Partial via structural |

### 2.3 Key empirical gaps (repo evidence)

| Claim | Evidence | Implication |
|-------|----------|-------------|
| Rules strip slop | 229→18 AI-isms (92.1%) on 9 fixtures | Human-visible win |
| Rules don't evade TMR | ~0.1–0.2 pp delta on 98%+ slop | Loop target misaligned with user expectations |
| Lexical-only hurts | Adversarial Paraphrasing +8–15% TPR | Structural pass is corrective, not optional |
| DivEye parity | diveye_comparison.json | Measurement trustworthy on GPT-2 |
| distilgpt2 uncertified | No before/after bench vs gpt2 | Default readings may miscalibrate |
| Feedback loop untested E2E | Mock tests only; no committed loop JSON | CI blind spot |

---

## 3. Code/gap synthesis

### 3.1 Architecture: today vs target

```
TODAY                                    TARGET (2026-aligned)
─────                                    ─────────────────────

Input                                    Input
  │                                        │
  ▼                                        ▼
humanize ladder                          humanize ladder
(balanced→full→full+struct+soul)         (…→anti-detector)
  │                                        │
  ├─► TMR p(AI) ──► stop if ≤ τ          ├─► TMR/Desklib p(AI)
  │     (only branch)                    ├─► DivEye vector / distance
  └─► surprisal_stdev (log optional)     ├─► TSD DD+LV (H₂)
                                         ├─► SurpMark ΔGJS (optional)
                                         └─► multi-objective stop
                                              │
                                              ▼ miss all
                                         exhaust → cross-model LLM
                                         (user-initiated; no watermark strip)
```

### 3.2 Module-level gap matrix

| Capability | 2026 stack | `detector.py` | `surprisal.py` | `structural.py` |
|------------|------------|---------------|----------------|-----------------|
| Supervised p(AI) | TMR, Desklib, GPTZero | ✅ TMR, Desklib | — | — |
| DivEye 10-vector | ✅ | log stdev only | ✅ compute | — |
| DivEye XGBoost head | HF Space | ❌ | ❌ | — |
| TSD second-half DD/LV | ✅ | ❌ | ❌ | — |
| SurpMark transitions | ✅ | ❌ | ❌ | — |
| Sentence-length σ lift | ✅ | step 3 only | — | ✅ split-only |
| Δ² entropy optimization | DivEye 39% SHAP | ❌ | computed, ignored | — |
| anti-detector intensity | lexical_targets | ❌ not in ladder | — | — |
| Multi-objective stop | Pareto gates | ❌ | ❌ | — |
| Chained iterations | optional | ❌ from-original | — | — |
| LLM in loop | post-exhaust | ❌ | — | — |
| Full-doc scoring | 1024+ tokens | 4-chunk cap | 1024 trunc | — |

### 3.3 Signal alignment: what the loop actually optimizes

| Signal | Detected by 2026 stack | Moved by current loop | Gap severity |
|--------|------------------------|----------------------|--------------|
| Stock vocab / hedging | All | **Yes** (primary) | Low |
| Sentence-length uniformity | GPTZero legacy, Desaire | Partial (ladder step 3) | Medium |
| Global surprisal σ | DivEye | Not optimized | **High** |
| Δ² entropy / autocorr | DivEye (strongest ablation) | Computed, ignored | **High** |
| Second-half volatility | TSD | **No** | **High** |
| Surprisal transitions | SurpMark | **No** | **High** |
| Supervised embedding | TMR, GPTZero 4.x | TMR only (~0 pp movement) | **Critical** (user-facing) |
| Humanizer-augmented robustness | DAMAGE, Turnitin Feb 2026 | **No** | **Critical** |

### 3.4 Partial overlaps (don't double-count)

- `delta_surprisal_stdev` ≠ TSD DD: global signed Δ std vs second-half |Δ| std
- `structural.py` σ lift ≠ DivEye σ: sentence word counts vs token surprisal under LM
- `stylometry.py` proxies (`sentence_length_cv`, `word_length_stdev`) correlate with but ≠ DivEye
- TMR optimization ≠ commercial pass (Agent #67, #80): report corpus + FPR cap always

---

## 4. Implementation priorities

Consolidated from Agents #34, #80, #55, #54, #49, #01, and `UPDATE-PLAN-2026-08.md`.

### P0 — Honesty & measurement (no new evasion claims)

| # | Action | Module | Effort | Rationale |
|---|--------|--------|--------|-----------|
| 1 | Run `detector_bench.py` on full 9-fixture corpus; commit JSON | benchmarks | hours | Baseline evidence |
| 2 | Add `benchmarks/detector_feedback_bench.py` (mock + opt-in TMR) | benchmarks | 1–2 days | Close loop CI gap |
| 3 | Wire `--surprisal-variance` into `--detector-feedback` JSON output | cli.py, detector.py | hours | Free observability (Agent #80 #4) |
| 4 | README/SKILL: "TMR ≠ GPTZero/Turnitin pass" | docs | hours | Agent #67 compliance |
| 5 | Document `to_diveye_vector()` tracks IBM **code**, not paper Eq. 6 | surprisal.py docstring | minutes | Agent #34 P1 |
| 6 | Gate `benchmarks/diveye_comparison/run.py` in CI with `UNSLOP_RUN_REAL_SURPRISAL=1` | CI | hours | Regression guard |

### P1 — Signal expansion (defensive ESL scope)

| # | Action | Module | Effort | Rationale |
|---|--------|--------|--------|-----------|
| 7 | `compute_tsd_reading()` — DD + LV on H₂, reuse surprisal tensor | surprisal.py | ~20 LOC + tests | Agent #02, #55 |
| 8 | Extend `IterationRecord`: full `SurprisalReading.to_dict()` + TSD fields | detector.py | 1 day | Multi-metric audit |
| 9 | Add `anti-detector` as final ladder step | detector.py | hours | Exists in humanize.py; loop never reaches it |
| 10 | Default surprisal LM → `gpt2` for paper parity OR label distilgpt2 uncertified | surprisal.py, CLI | hours | Agent #34 |
| 11 | `detector_bench.py`: matrix includes structural/soul/anti-detector + feedback_loop column | benchmarks | 1–2 days | Measure what loop does |
| 12 | Benchmark row: σ, CV, flat_paragraphs before/after structural-only | benchmarks | 1 day | Agent #54 ablation gap |
| 13 | Log full surprisal vector per feedback iteration (not just stdev) | detector.py | hours | Agent #01 |

### P2 — Research integration (optional, heavy)

| # | Action | Module | Effort | Rationale |
|---|--------|--------|--------|-----------|
| 14 | SurpMark lite: frozen ref matrices, `compute_surpmark_reading()` | surprisal.py | 2–3 weeks | Agent #03 |
| 15 | DivEye XGBoost head (HF Space `model.json`) as optional backend | detector.py | 1–2 weeks | NC license check |
| 16 | Multi-objective stop: `p_ai ≤ τ AND σ ∈ band AND tsd_score ≤ t*` | detector.py | 1 week | Agent #55 §5 P4 |
| 17 | GPTZero API eval harness (opt-in, version-pinned, no CI dep) | benchmarks/ | 1 week | User ground truth |
| 18 | Chained feedback mode (out_i → in_{i+1}) behind flag | detector.py | days | Test structural regression |
| 19 | LLM step after ladder exhaustion (user consent) | cli.py | days | Matches exhaustion rec |
| 20 | `compute_surprisal_dynamics()` unified API | surprisal.py | 1 week | DivEye + TSD + SurpMark |
| 21 | Cone-width proxy for GPTZero v6 signal | new module | 2+ weeks | UPDATE-PLAN Phase 2 |

### P3 — Explicit non-goals

- Watermark strip optimization (Agents #71–76)
- Marketing "beat Turnitin" / undetectable claims
- Automatic LLM paraphrase inside loop without consent
- Using detector pass as academic integrity gate
- Shipping BiScope + Falcon-7B production stack (VRAM / NC license)

---

## 5. Test gaps

### 5.1 Current coverage

| Area | File | What's tested | What's missing |
|------|------|---------------|----------------|
| Feedback loop semantics | `test_detector.py` | Mock scorer: early stop, exhaustion, ladder order, aggressive wrapper, surprisal hook, serialization | Real TMR weights; chained vs from-original policy |
| Surprisal | `test_surprisal.py` | Shape, empty input, skip flag, fake LM patch | TSD; SurpMark; distilgpt2 vs gpt2 rank order; short-text guard (<10 tokens) |
| Structural | `test_structural.py` | Split/merge guards, σ non-regression | Detector score delta after structural-only; deadlock case (uniform 24-word, no boundary) |
| CLI | `test_cli.py` | Partial detector/surprisal flags | Combined `--detector-feedback` + surprisal JSON |
| Integration | — | — | feedback_loop + real humanize + real TMR (opt-in) |
| Parity | `test_benchmark_comparisons.py` | diveye_comparison harness | Not CI-gated by default |

### 5.2 Required new tests (priority order)

**P0 — CI-safe (mock / fixture):**

1. `test_detector_feedback_bench.py` — loop produces expected iteration count and audit JSON on fixtures with mock scorer
2. `test_detector.py`: ladder includes `anti-detector` after P1 #9 lands
3. `test_cli.py`: `--detector-feedback` output includes surprisal block when flag set
4. `test_surprisal.py`: `compute_tsd_reading()` on fake LM tensor (synthetic flat vs bursty sequence)

**P1 — Opt-in (`UNSLOP_RUN_REAL_SURPRISAL=1`, `UNSLOP_RUN_DETECTOR_BENCH=1`):**

5. Real TMR: original vs balanced vs full vs feedback_loop on 3-fixture subset
6. diveye_comparison CI weekly — distilgpt2 vs gpt2 correlation on humanize before/after
7. Structural-only: σ delta + TMR delta on flat-paragraph fixture

**P2 — Research / manual:**

8. SurpMark: human fixture closer to Q-ref than machine fixture
9. TSD: anti-detector pass increases DD on ≥7/9 long samples
10. Feedback loop chained mode vs from-original A/B (structural preservation + TMR)

### 5.3 Benchmark gaps (no invented numbers)

| Bench | Exists | Measures | Missing |
|-------|--------|----------|---------|
| `run.py` | ✅ | AI-isms, burstiness, structural OK | TMR, surprisal, anti-detector |
| `detector_bench.py` | ✅ | TMR/Desklib single-pass | feedback_loop, anti-detector, surprisal |
| `diveye_comparison/` | ✅ | IBM vector parity | humanize before/after feature shift |
| `detector_feedback_bench.py` | ❌ | — | loop regression |
| `surprisal_humanization/` | ❌ | — | Δ features per intensity |
| `evals/measure.py` | ✅ | AI-isms, burstiness | any detector dimension |

---

## 6. Risk register (code-relevant)

| Risk | Cause in code | Mitigation |
|------|---------------|------------|
| False confidence | User sees TMR 0.49, submits to GPTZero | Document model IDs; never promise commercial pass |
| Wrong gradient | Loop optimizes TMR; stack uses TSD/SurpMark | Multi-signal panel before anti-detector claims |
| Orphaned surprisal | `--surprisal-variance` separate from feedback | P0 #3 wire telemetry |
| distilgpt2 miscalibration | Default ≠ validated gpt2 | P1 #10 align or label uncertified |
| Chunk truncation | `max_chunks=4` on essays | Raise cap or full-doc score for loop decisions |
| Split deadlock | Uniform 22-word sentences, no connector | Document; LLM anti-detector for fragment injection |
| Non-chaining waste | Each step re-processes original | Document; optional chained mode behind flag |
| anti-detector never reached | Ladder stops at full | P1 #9 extend ladder |

---

## 7. One-paragraph maintainer verdict

unslop built the right **shape**: lexical scrub → structural burstiness → soul/contractions → optional supervised score → honest exhaustion. The **detector generation** is wrong for August 2026: TMR is a RAID-era checkpoint that barely responds to deterministic passes; DivEye, TSD, and SurpMark moved detection to surprisal **dynamics**; GPTZero 4.x and Pangram DAMAGE moved commercial stacks to humanizer-red-team classifiers. Code already **computes** DivEye features (`surprisal.py`, IBM-aligned per Agent #34) and **applies** structural σ fixes (`structural.py`, split-only per Agent #54) but **`detector.py` listens only to TMR** and logs surprisal optionally. Closing the gap is wiring and ~20 LOC for TSD on existing tensors — not a philosophy change. Keep commercial pass out of marketing; treat the loop as maintainer release gate until multi-signal stop ships.

---

## 8. Source memo index

| Agent | Focus | Key contribution to this synth |
|-------|-------|-------------------------------|
| **#34** | IBM DivEye implementation | Numeric parity proof; HF Space vs GitHub gaps; distilgpt2 vs gpt2 |
| **#80** | detector.py gap audit | Loop semantics; eval/bench matrix; P0–P3 recommendations |
| **#01** | DivEye theory | Feature-targeted humanization; second-order H_Δ² priority |
| **#49** | Burstiness layers | Three burstiness definitions; structural vs surprisal orthogonality |
| **#54** | Sentence-length restoration | structural.py asymmetry; Desaire #8–11 mapping |
| **#55** | TSD + SurpMark | Position/transition gaps; target architecture |
| **UPDATE-PLAN** | Repo refresh | Five-signal model; phase timeline |

---

## 9. Code anchors

| File | Role |
|------|------|
| `unslop/scripts/detector.py:301-415` | `feedback_loop`, ladders, exhaustion |
| `unslop/scripts/surprisal.py:211-297` | DivEye computation |
| `unslop/scripts/surprisal.py:107-119` | `to_diveye_vector()` |
| `unslop/scripts/structural.py:174-249` | `split_long_sentences` |
| `unslop/scripts/structural.py:252-358` | `merge_bullet_soup` |
| `benchmarks/detector_bench.py` | Single-pass TMR bench |
| `benchmarks/diveye_comparison/run.py` | IBM parity harness |
| `benchmarks/results/diveye_comparison.json` | Parity evidence |
| `tests/unslop/test_detector.py` | Mock loop contract |

---

*SYNTH-83 complete. Feeds UPDATE-PLAN Phase 1–2 and implementation backlog.*
