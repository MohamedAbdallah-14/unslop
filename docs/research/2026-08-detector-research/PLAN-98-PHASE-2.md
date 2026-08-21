# PLAN-98 — Phase 2 Implementation Plan

**Master Integration Agent #98**  
**Date:** 2026-08-19  
**Scope:** Surprisal dynamics, SurpMark lite, anti-detector ladder, stylometry-driven structural, benchmark harness  
**Inputs:** SYNTH-81 through SYNTH-96, `UPDATE-PLAN-2026-08.md`, `SYNTH-83` code-gap audit, `SYNTH-92` stylometry integration  
**Audience:** unslop maintainers — file-level spec for Phase 2 (4–6 weeks)  
**Prerequisite:** Phase 1 quick wins (anti-detector on ladder, `stylometric_baseline.json`, surprisal wired to feedback JSON) may land in parallel; Phase 2 assumes or completes them.

---

## Executive summary

August 2026 detectors read **five largely independent signals**. unslop handles lexical AI-isms well (Signal 1) and sentence-length σ partially (Signal 2). DivEye global surprisal is **computed but not optimized** (Signal 3). Signals 4–5 — late-stage volatility (TSD), transition recovery (SurpMark), predictability cones (GPTZero v6 analog) — are **absent from code**.

Phase 2 closes the measurement–optimization gap without crossing into Phase 3 LLM pipelines or bypass marketing:

| Workstream | Deliverable | Primary files |
|------------|-------------|---------------|
| **A. Surprisal dynamics** | TSD + unified `compute_surprisal_dynamics()` + cone-width proxy | `surprisal.py`, new `cone_proxy.py` (optional thin module) |
| **B. SurpMark lite** | Frozen ref matrices, `compute_surpmark_reading()`, ΔGJS vs human/machine refs | `surprisal.py` or `surpmark_lite.py` |
| **C. Anti-detector ladder** | Extended ladder + `dynamics_targets.py` + multi-objective stop | `detector.py`, `dynamics_targets.py`, `humanize.py` |
| **D. Stylometry-driven structural** | Measure → edit → re-measure Phase 1–2 loop | `stylometry.py`, `structural.py`, `lexical_targets.py`, `humanize.py` |
| **E. Benchmark harness** | TPR@FPR=5%, URSS bundle, dynamics before/after, detector feedback bench | `shield_metrics.py`, `detector_bench.py`, new benches |

**Honest ceiling (SYNTH-81, SYNTH-83):** Deterministic passes move TMR ~0.0–0.2 pp. Phase 2 targets **dynamics telemetry movement** and **honest measurement**, not commercial detector pass. Anti-detector mode stays ESL/resume defensive use (SYNTH-87, SYNTH-96).

**Exit criteria:** Anti-detector ladder raises second-half DD on ≥7/9 long fixtures; `detector_bench` emits dynamics section + TPR@FPR; structural-only ablation shows σ/CV lift on flat fixtures; `pytest tests/unslop/` green.

---

## 1. Problem statement (synthesis)

### 1.1 Five-signal stack vs unslop today

```
Signal 1: Lexical AI-isms          → humanize.py          ✅ strong
Signal 2: Sentence-length σ/CV     → structural.py        ⚠️ split-only, static thresholds
Signal 3: Global surprisal (DivEye)→ surprisal.py         ⚠️ measure only
Signal 4: Late-stage stability     → TSD                  ❌
Signal 5: Predictability cones     → GPTZero v6 analog    ❌
Cross:   Transition recovery       → SurpMark             ❌
Supervised: TMR/Desklib            → detector.py          ✅ score only; ladder incomplete
```

Sources: SYNTH-81 §1.6, SYNTH-83 §2.1, SYNTH-89 §1.3, UPDATE-PLAN Part 2.

### 1.2 Why Phase 2 exists

- **Academic frontier moved** from mean perplexity to surprisal **trajectory** (TSD second-half decay 24–32%; SurpMark ΔGJS ~99% AUROC under paraphrase — SYNTH-81 §1.3).
- **Commercial stacks** (GPTZero v6 cones, Turnitin anti-humanizer) punish uniform rhythm and synonym-band rewrites (SYNTH-82 §3.2).
- **Code already computes DivEye** (IBM-aligned per SYNTH-83); tensors exist for TSD with ~20 LOC addition (Agent #02, #55).
- **Feedback loop listens only to TMR** and stops at `full+structural+soul` — never `anti-detector`, never dynamics (SYNTH-83 §1.1).
- **Structural pass ignores stylometry** — fixed `target_sigma=5.0` while `StyleProfile` measures 19 fields (SYNTH-92).

### 1.3 Explicit non-goals (Phase 2)

From SYNTH-87, SYNTH-84, SYNTH-86:

- Watermark strip modes, SIRA/BIRA integration, score-targeting schedulers (RateAudit)
- Shipping TempParaphraser weights, AdvPara token beam, MASH DPO, StealthRL
- Commercial detector APIs in CI (GPTZero/Turnitin/Pangram — manual May detector-test only)
- Marketing "beat Turnitin" / "100% undetectable"
- DivEye XGBoost classifier head in live loop (optional bench backend P2)
- Full SurpMark training pipeline — **lite port only** with frozen reference matrices

---

## 2. Architecture — target state

```
Input text
  │
  ├─► [Measure] stylometry.analyze() + analyze_paragraphs()
  │              surprisal.compute_surprisal_dynamics()  ← NEW unified API
  │
  ├─► Phase 2 lexical (humanize.py regex families)
  │
  ├─► Phase 1 structural (stylometry-guided targets)     ← SYNTH-92
  │
  ├─► lexical_targets.apply_targeted_pass (baseline gaps)
  │
  ├─► Phase 5 soul (if enabled)
  │
  ├─► dynamics_targets.apply_deterministic_pass()        ← NEW (2nd-half vol, recovery breaks)
  │
  ├─► anti-detector intensity (lexical + LLM prompt only if --mode llm)
  │
  ├─► validate.py (preservation + AI-isms + burstiness warn)
  │
  └─► [Optional] detector.feedback_loop()
          ladder: balanced → full → full+struct+soul → anti-detector   ← extended
          stop: TMR ≤ τ AND dynamics_in_human_band()                   ← multi-objective
          log: full SurprisalReading + TSD + SurpMark + stylometry delta
```

**CLI flags (Phase 2):**

```bash
python3 -m unslop.scripts.cli humanize doc.md \
  --intensity anti-detector \
  --detector-feedback \
  --dynamics-feedback          # NEW: multi-objective stop
  --surprisal-variance         # one-shot or per-iteration JSON
  --report-stylometric-gaps    # pre/post StyleProfile
```

---

## 3. Workstream A — Surprisal dynamics

**Sources:** SYNTH-81 (DivEye/TSD/SurpMark), SYNTH-83 §1.2, SYNTH-89 §1.3, Agent #01–03, #55, UPDATE-PLAN Phase 2.

### 3.1 Extend `surprisal.py`

#### A1. `compute_tsd_reading(text, *, model=...) → TSDReading`

**Paper:** TSD — "When AI Settles Down" (arXiv:2601.04833).

**Signals on second half only (positions > 50%):**

| Field | Definition | Human band (fixture-calibrated) |
|-------|------------|--------------------------------|
| `dd` | Derivative dispersion: std of \|Δ surprisal\| on H₂ | Higher = more volatile |
| `lv` | Local volatility: mean rolling-window std (window=5 tokens) | Higher = less "settled" |
| `dd_ratio` | H₂ DD / H₁ DD | AI typically < 1 (decay) |
| `settle_score` | Composite: lower = more machine-like late stability | Target: raise under anti-detector |

**Implementation:**

- Reuse existing token surprisal tensor from `compute_surprisal_variance()` — no second forward pass.
- Split sequence at `n // 2`; compute DD/LV on each half.
- Guard: `token_count < 20` → return `TSDReading(unavailable=True)` with reason.

**Effort:** ~40 LOC core + tests; 1 day.

#### A2. `compute_lexical_cone_reading(text, *, model=..., top_k=40) → ConeReading`

**Analog:** GPTZero v6 predictability cones (arXiv:2602.13042) — synonym swap stays in high-probability band.

**Proxy (no GPTZero API):**

- For each content token, compute `top_k_mass = sum(p(w_i) for w_i in top-k)` under scoring LM.
- Report: `mean_top_k_mass`, `low_entropy_token_fraction` (mass > 0.9), `cone_width_p75`.
- **Humanization target:** widen cone — lower mean top-k mass on edited spans.

**Effort:** 2–3 days + fixture calibration. Optional defer to Phase 2.1 if TSD/SurpMark ship first.

#### A3. `compute_surprisal_dynamics(text, *, model=...) → SurprisalDynamics`

Unified dataclass aggregating:

```python
@dataclass
class SurprisalDynamics:
    diveye: SurprisalReading          # existing 10-feature vector
    tsd: TSDReading
    surpmark: SurpMarkReading | None  # None if refs missing
    cone: ConeReading | None          # optional
    model: str
    token_count: int

    def to_dict(self) -> dict: ...
    def in_human_band(self, baselines: DynamicsBaselines) -> bool: ...
```

**Effort:** 1 day wiring + tests.

### 3.2 Default LM policy

| Option | Action | Source |
|--------|--------|--------|
| **Recommended** | Default `gpt2` for paper parity on dynamics bench | SYNTH-83 Agent #34 |
| **Acceptable** | Keep `distilgpt2` default but label "uncertified for dynamics thresholds" in docs | Current code |
| **CI** | Gate `diveye_comparison` weekly with `UNSLOP_RUN_REAL_SURPRISAL=1` | SYNTH-83 P0 |

Ship `benchmarks/results/dynamics_baseline.json` with p25/p75 per field on human/AI fixture slices — same pattern as stylometric baseline.

### 3.3 Deterministic dynamics nudges (via `dynamics_targets.py`)

See Workstream C. Surprisal module **measures**; `dynamics_targets.py` **applies** bounded edits:

- Second-half volatility injection: swap predictable function-word spans in H₂ only (safe word list, `_protect`-safe).
- Recovery-pattern breaks: after high-Δ tokens, insert optional comma splice or short clause break (max 2/doc) — SurpMark-motivated.
- **Never** optimize to a target TMR score — gap closure vs human p25–p75 only (SYNTH-87).

---

## 4. Workstream B — SurpMark lite

**Sources:** SYNTH-81 §1.3 (SurpMark ICML 2026), SYNTH-83 §3.2, Agent #03, #55.

### 4.1 Scope — "lite" definition

Full SurpMark trains k-means surprisal states and transition matrices on large corpora. **SurpMark lite** for unslop:

1. **Frozen reference matrices** `Q_human`, `Q_machine` (k=4 or k=6 states) — committed under `benchmarks/fixtures/surpmark_refs/` or embedded JSON (~few KB).
2. **State assignment:** Quantile bins on per-token surprisal (reuse DivEye tensor) — no online k-means.
3. **Transition matrix** `Q_doc` from consecutive state pairs.
4. **ΔGJS** = generalized Jensen-Shannon divergence vs refs (paper metric).
5. **Read-only in CI** — no training step in repo.

### 4.2 API

```python
@dataclass
class SurpMarkReading:
    k: int
    delta_gjs_human: float   # lower = more human-like transitions
    delta_gjs_machine: float
    recovery_rate: float     # high-surp → low-surp transition freq (machine tell)
    n_transitions: int
    unavailable: bool = False

def compute_surpmark_reading(
    text: str,
    *,
    surprisal_reading: SurprisalReading | None = None,
    k: int = 4,
) -> SurpMarkReading: ...
```

### 4.3 Reference matrix bootstrap (one-time maintainer task)

| Step | Action |
|------|--------|
| 1 | Run scoring LM on `benchmarks/fixtures/` human-like + AI-slop corpus |
| 2 | Build Q matrices from labeled slices (tag fixtures as proxy human/AI) |
| 3 | Commit `surpmark_refs_k4.json` with version field |
| 4 | Opt-in test: human fixture closer to Q_human than machine fixture |

**Honesty:** Proxy refs from unslop fixtures ≠ paper's full RAID training. Document as **internal regression oracle**, not SurpMark paper replication.

### 4.4 Effort

| Task | Days |
|------|------|
| State binning + transition matrix | 2 |
| ΔGJS implementation | 1 |
| Ref matrix generation script | 1 |
| Tests + bench integration | 2 |
| **Total** | ~6 days |

---

## 5. Workstream C — Anti-detector ladder + dynamics targets

**Sources:** SYNTH-83, SYNTH-85 §6, SYNTH-86 §4.3, SYNTH-87 §3, SYNTH-88 §4.2, UPDATE-PLAN Phase 1–2.

### 5.1 Extend detector feedback ladder

**Current `DEFAULT_LADDER` (`detector.py:279-282`):**

```
(balanced, off, off) → (full, off, off) → (full, on, on)
```

**Target `DEFAULT_LADDER` (Phase 2):**

```python
DEFAULT_LADDER: list[tuple[str, bool, bool]] = [
    ("balanced", False, False),
    ("full", False, False),
    ("full", True, True),
    ("anti-detector", True, True),   # NEW — intensity exists in humanize.py
]
```

**Ladder tuple evolution (optional P2):** Extend to 4-tuple `(intensity, structural, soul, dynamics: bool)` or pass `apply_dynamics=True` on final step only.

**Semantics fixes (document + optional flag):**

| Issue | Phase 2 action |
|-------|----------------|
| Non-cumulative rewrites from original | Document; add `--feedback-chained` flag (out_i → in_{i+1}) behind opt-in |
| Deterministic-only inner loop | anti-detector step runs deterministic pass; LLM remains user-initiated |
| Chunk cap 4×512 | Raise to 8 chunks for loop decisions on essay fixtures |

### 5.2 New module: `dynamics_targets.py`

```python
@dataclass
class DynamicsGap:
    field: str           # e.g. "tsd.dd", "surpmark.delta_gjs_human", "diveye.delta2_entropy"
    value: float
    band_low: float
    band_high: float
    direction: Literal["raise", "lower", "band"]

def measure_dynamics_gaps(
    dynamics: SurprisalDynamics,
    baselines: DynamicsBaselines,
) -> list[DynamicsGap]: ...

def apply_dynamics_pass(
    text: str,
    gaps: list[DynamicsGap],
    *,
    max_edits: int = 3,
) -> tuple[str, DynamicsReport]: ...
```

**Baseline file:** `benchmarks/results/dynamics_baseline.json` — p25/p75 for DivEye fields, TSD DD/LV, SurpMark ΔGJS, cone width.

**Deterministic passes (bounded):**

1. **H₂ volatility** — identify lowest-Δ span in second half; split sentence or insert mild disruption (em-dash → comma) if preservation allows.
2. **Δ² entropy** — structural pass first (SYNTH-89: orthogonal signals); if still low, one safe function-word swap in H₂.
3. **Recovery break** — if `recovery_rate` > machine ref p75, break one high→low surprisal transition via phrase reorder (deterministic template, max 1).

### 5.3 Multi-objective stop policy

```python
def should_stop(
    *,
    tmr: float,
    target_tmr: float,
    dynamics: SurprisalDynamics,
    baselines: DynamicsBaselines,
    ai_isms: int,
) -> tuple[bool, str]:
    tmr_ok = tmr <= target_tmr
    dynamics_ok = dynamics.in_human_band(baselines)
    isms_ok = ai_isms == 0
    # Phase 2: stop only when ALL implemented metrics satisfied OR ladder exhausted
    ...
```

**CLI:** `--dynamics-feedback` enables dynamics band check; default off for backward compatibility.

**Policy (SYNTH-87):** TMR and dynamics are **diagnostic stop conditions**, not optimization targets for marketing. Never add `--target-score=0`.

### 5.4 `IterationRecord` extension

```python
@dataclass
class IterationRecord:
    # existing fields...
    surprisal: dict | None = None      # full SurprisalReading.to_dict()
    tsd: dict | None = None
    surpmark: dict | None = None
    stylometry_delta: dict | None = None
```

Wire `--surprisal-variance` into `--detector-feedback` JSON (Phase 1 overlap — complete in Phase 2 if not done).

### 5.5 Fix `detector.py` TempParaphraser comment

Lines 389–392 incorrectly imply TempParaphraser needs "no LLM call." Replace with:

> TempParaphraser (EMNLP 2025) requires LLM paraphrase + N-candidate selection; unslop recommends cross-model rewrite as the user-orchestrated analog when the deterministic ladder exhausts.

(SYNTH-85, SYNTH-88 P2.)

---

## 6. Workstream D — Stylometry-driven structural

**Sources:** SYNTH-92 (primary spec), SYNTH-89 §5, SYNTH-90 §5 (voice vs anti-detector), Agent #41, #52, #54.

### 6.1 Goal

Close the loop: **measure → edit toward gap → re-measure → report delta** for Phase 1 (`structural.py`) and Phase 2 (`lexical_targets.py`).

### 6.2 Sprint breakdown (from SYNTH-92)

#### Sprint A — Measurement foundation (3–4 days)

| ID | Task | Files |
|----|------|-------|
| D-A1 | `analyze_paragraphs()` → `ParagraphStyleStats` | `stylometry.py` |
| D-A2 | `StylometryContext` pre/post in `humanize_deterministic_with_report` | `humanize.py` |
| D-A3 | Refactor `structural._paragraph_sigma` to use paragraph API | `structural.py` |
| D-A4 | Commit `benchmarks/results/stylometric_baseline.json` | `benchmarks/` |

#### Sprint B — Phase 1 closed loop (4–5 days)

| ID | Task | Files |
|----|------|-------|
| D-B1 | `StructuralTargets` + `resolve_structural_targets(ctx)` | `structural.py`, `humanize.py` |
| D-B2 | Pass flat paragraph indices from ctx to split pass | `structural.py` |
| D-B3 | `StructuralReport`: σ/CV before/after, deadlocks | `structural.py` |
| D-B4 | Optional single retry when Δσ < 0.5 | `structural.py` |
| D-B5 | Validator flat count → stylometry helper | `validate.py` |

**Mode-aware targets:**

| Mode | `target_sigma` | Notes |
|------|----------------|-------|
| `voice-match` + sample | `max(sample_σ × 0.9, 3.0)` | Fidelity — don't force σ≥6 |
| `anti-detector` | `6.0` | Aggressive flat catch; split-only |
| `balanced` / default | `5.0` | Current behavior |
| Baseline gap: σ below p25 | `5.5` | Nudge from measured gap |

#### Sprint C — Phase 2 lexical closed loop (3–4 days)

| ID | Task | Files |
|----|------|-------|
| D-C1 | Gap-gate Latinate pass at `balanced` | `lexical_targets.py` |
| D-C2 | Report structural gaps even when intensity < full | `humanize.py` |
| D-C3 | Tests: AI fixture → σ/CV/latinate toward baseline | `tests/unslop/` |

### 6.3 Explicit non-goals (Phase 1–2 stylometry)

- Contraction injection (Phase 5 `soul.py`)
- Short-sentence / fragment injection (LLM anti-detector only)
- Biber 67-feature register (optional `--biber-profile` eval — Phase 2+)

### 6.4 Integration with dynamics pass

Order in pipeline:

```
lexical regex → structural(stylometry targets) → lexical_targets → soul → dynamics_targets
```

Structural lifts **syntactic** σ; dynamics_targets lifts **token** surprisal trajectory. Both feed `SurprisalDynamics.in_human_band()`.

---

## 7. Workstream E — Benchmark harness

**Sources:** SYNTH-84 (primary), SYNTH-81 §2, SYNTH-83 §5.3, UPDATE-PLAN Phase 4 overlap.

### 7.1 Layer model

```
Layer 0 (CI every PR):     benchmarks/run.py — ai_isms, burstiness, preservation
Layer 1 (release gate):    detector_bench.py + shield_metrics + dynamics section
Layer 2 (weekly/opt-in):   surprisal humanization ablation, feedback loop bench
Layer 3 (docs only):       Booth, DAMAGE tables — cite, don't gate
```

### 7.2 New: `unslop/scripts/shield_metrics.py` (P0)

Pure numpy/scipy — no torch:

```python
def tpr_at_fpr(y_true, y_score, target_fpr=0.05, ...) -> tuple[float, float]: ...
def w_auroc(y_true, y_score, k=20 * log(2)) -> float: ...
def sfd(scenario_fprs: list[float], ...) -> float: ...
def urss(w_aurocs: list[float], sfd: float) -> float: ...
```

### 7.3 Extend `benchmarks/detector_bench.py`

| Addition | Spec |
|----------|------|
| Fixtures | +2 essay-length, +1 ESL-short, +1 résumé-bullets |
| Intensities | subtle, balanced, full, **anti-detector**, structural-only, dynamics-only |
| Metrics | P(AI), **TPR@FPR=5%**, ΔTPR, URSS bundle (≥2 scenarios) |
| Dynamics block | Before/after: DivEye vector, TSD DD/LV, SurpMark ΔGJS, cone width |
| Stylometry block | σ, CV, latinate_ratio, contraction_rate |
| Attacks | `--raid-attacks paraphrase,synonym` via `raid-bench` (opt-in) |
| Output | `benchmarks/results/<stamp>-detectors.json` + markdown |

**Release gate (revised):**

1. **Hard:** `run.py --strict` passes.
2. **Soft:** balanced must not *increase* mean P(AI) vs original.
3. **Honesty:** if ΔP(AI) < 1 pp, report "no material detector movement."
4. **Dynamics:** anti-detector raises H₂ DD on ≥7/9 long fixtures (internal regression).

### 7.4 New: `benchmarks/detector_feedback_bench.py`

Mock scorer + opt-in real TMR:

- Ladder iteration count, audit JSON shape
- anti-detector step reached
- Multi-objective stop fires when dynamics in band

### 7.5 New: `benchmarks/surprisal_humanization/`

| Column | Measures |
|--------|----------|
| Fixture × intensity | Δ surprisal_stdev, Δ delta2_entropy, Δ tsd.dd, Δ surpmark.delta_gjs |
| structural-only | Orthogonality vs DivEye (SYNTH-89) |
| anti-detector | Full ladder |

### 7.6 Dual-arm protocol (DAMAGE/Booth derived)

Every research run reports:

| Arm | Description |
|-----|-------------|
| **Clean** | Raw assistant → unslop modes |
| **Stress** | Cross-model paraphrase second pass (manual or Phase 3) |

Never imply green GPTZero → green Pangram/Turnitin (SYNTH-82, SYNTH-84 §4.2).

### 7.7 Honest reporting template

Ship in `benchmarks/README.md`:

```markdown
## Detector eval (research)

Setup: N fixtures, intensities [...], detectors [TMR, Desklib],
attacks [none|RAID paraphrase], metrics TPR@FPR=5% + URSS + dynamics.

| Condition | Mean P(AI) | TPR@5% | Δσ | Δ TSD DD | ROUGE-L |
|-----------|------------|--------|-----|----------|---------|
| Original  | ...        | ...    | —   | —        | 1.00    |
| anti-detector | ...    | ...    | ... | ...      | ...     |

Interpretation: [one sentence — e.g. "Deterministic balanced moved TMR ≤0.2 pp;
anti-detector raised H₂ DD X% with no material TMR change."]
```

---

## 8. Cross-workstream integration matrix

| Component | A Surprisal | B SurpMark | C Ladder | D Stylometry | E Bench |
|-----------|-----------|------------|----------|--------------|---------|
| `surprisal.py` | owner | owner | read | — | read |
| `dynamics_targets.py` | read | read | apply | read σ | metrics |
| `detector.py` | log | log | owner | — | test |
| `structural.py` | — | — | step 3 | owner | ablation |
| `stylometry.py` | proxies | — | — | owner | metrics |
| `humanize.py` | hook | hook | intensity | ctx | report |
| `cli.py` | flags | flags | flags | flags | invoke |

---

## 9. Implementation schedule (6 weeks)

### Week 1 — Foundations

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–2 | `compute_tsd_reading()` + tests | A |
| 2–3 | `stylometric_baseline.json` + `analyze_paragraphs()` | D-A |
| 3–4 | anti-detector on `DEFAULT_LADDER` | C |
| 4–5 | `shield_metrics.py` + `tpr_at_fpr()` | E |

### Week 2 — SurpMark + dynamics baselines

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–3 | SurpMark lite + ref matrices | B |
| 3–4 | `compute_surprisal_dynamics()` unified API | A |
| 4–5 | `dynamics_baseline.json` generation script | C, E |

### Week 3 — Stylometry structural loop

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–3 | `StructuralTargets` + mode-aware resolution | D-B |
| 3–4 | `StylometryContext` in humanize report | D-A |
| 4–5 | Gap-gated lexical_targets | D-C |

### Week 4 — Dynamics targets + feedback

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–3 | `dynamics_targets.py` deterministic passes | C |
| 3–4 | Multi-objective `should_stop()` + CLI `--dynamics-feedback` | C |
| 4–5 | Extended `IterationRecord` + JSON output | C |

### Week 5 — Benchmarks

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–2 | `detector_bench.py` dynamics + TPR@FPR | E |
| 2–3 | `detector_feedback_bench.py` | E |
| 3–4 | `surprisal_humanization/` harness | E |
| 4–5 | Run full matrix; commit JSON (no invented README numbers) | E |

### Week 6 — Cone proxy, docs, hardening

| Day | Deliverable | Workstream |
|-----|-------------|------------|
| 1–2 | `compute_lexical_cone_reading()` (if not deferred) | A |
| 2–3 | SKILL.md: five-signal stack, dynamics honesty | docs |
| 3–4 | Fix TempParaphraser comment, Liang citation, Booth attribution | docs |
| 4–5 | Acceptance run; gap review for Phase 3 | all |

**Parallel track:** Phase 0 research doc refresh (SYNTH-81 categories) — not blocking code.

---

## 10. Test plan

### 10.1 CI-safe (mock / fixture)

| Test | File | Asserts |
|------|------|---------|
| TSD on synthetic flat vs bursty sequence | `test_surprisal.py` | H₂ DD higher on bursty |
| SurpMark ΔGJS ordering | `test_surprisal.py` | human fixture < machine fixture |
| Ladder includes anti-detector | `test_detector.py` | 4th step intensity |
| Multi-objective stop | `test_detector.py` | dynamics band triggers stop |
| Paragraph flat detection | `test_stylometry.py` | matches structural |
| Structural targets by mode | `test_structural.py` | anti-detector σ > voice-match |
| dynamics_targets preservation | `test_dynamics_targets.py` | TestPreservation pass |
| shield_metrics TPR@FPR | `test_shield_metrics.py` | RAID protocol ε=0.0005 |

### 10.2 Opt-in (`UNSLOP_RUN_REAL_SURPRISAL=1`, `UNSLOP_RUN_DETECTOR_BENCH=1`)

| Test | Asserts |
|------|---------|
| diveye_comparison CI weekly | distilgpt2 vs gpt2 rank correlation |
| Real TMR feedback on 3-fixture subset | audit JSON schema |
| anti-detector raises H₂ DD on ≥7/9 fixtures | Phase 2 acceptance |
| Structural-only σ delta on flat-paragraph fixture | SYNTH-92 success |

---

## 11. Acceptance criteria (Phase 2 exit)

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | `compute_tsd_reading()` shipped with tests | `test_surprisal.py` green |
| 2 | SurpMark lite ΔGJS on fixtures | human closer to ref than AI-slop |
| 3 | `compute_surprisal_dynamics()` unified export | CLI JSON includes all fields |
| 4 | anti-detector is 4th ladder step | `test_detector.py` |
| 5 | `--dynamics-feedback` multi-objective stop | mock + opt-in integration |
| 6 | Stylometry-guided structural: mode-aware σ targets | unit tests |
| 7 | `stylometric_baseline.json` + `dynamics_baseline.json` committed | gaps non-empty on fixtures |
| 8 | `detector_bench` emits dynamics + TPR@FPR section | JSON artifact |
| 9 | anti-detector raises 2nd-half DD on ≥7/9 long fixtures | surprisal_humanization bench |
| 10 | `pytest tests/unslop/` green | CI |
| 11 | No new bypass/watermark marketing in SKILL | SYNTH-87 review |
| 12 | Preservation suite 100% on dynamics + structural passes | TestPreservation |

---

## 12. Risk register

| Risk | Mitigation | Source |
|------|------------|--------|
| distilgpt2 miscalibrates dynamics thresholds | gpt2 parity run; label uncertified defaults | SYNTH-83 |
| Dynamics edits break preservation | Max 3 edits/doc; `_protect()`; TestPreservation | SYNTH-92 |
| SurpMark lite refs not paper-faithful | Document as internal oracle | SYNTH-81 |
| User expects TMR drop from Phase 2 | Honesty gate in bench + SKILL | SYNTH-84 |
| Voice-match vs anti-detector σ conflict | Mode-aware targets; `--voice-floor-σ` doc | SYNTH-90, SYNTH-92 |
| Cone proxy false precision | Report as GPTZero analog, not equivalent | SYNTH-82 |
| `--dynamics-feedback` seen as evasion tool | Boundaries unchanged; diagnostic framing | SYNTH-87 |
| Phase 2 scope creep into LLM pipeline | Explicit non-goals; Phase 3 separate plan | SYNTH-86 |

---

## 13. Documentation updates (Phase 2)

| File | Change |
|------|--------|
| `skills/unslop/SKILL.md` | Five-signal stack; anti-detector ladder; dynamics honesty; Liang 2304.02819; remove Booth/Turnitin misattribution |
| `benchmarks/README.md` | Three-axis eval; TPR@FPR; dynamics block |
| `unslop/scripts/surprisal.py` docstring | IBM code vs paper Eq.6; TSD/SurpMark pointers |
| `docs/RESEARCH_AND_TECH.md` | DivEye/TSD/SurpMark paragraph; practitioner cross-model (SYNTH-88) |
| `detector.py` exhaustion message | TempParaphraser fix; provenance side-effect one-liner (SYNTH-87) |

SSOT only — mirrors via sync workflow.

---

## 14. Phase 3 handoff (out of scope, listed for continuity)

Phase 2 measurement + deterministic dynamics set up Phase 3 `llm_pipeline.py` (SYNTH-86):

- Multi-objective stop already accepts DivEye/TSD/SurpMark
- Hot-sentence selection uses TMR + local surprisal (TempParaphraser analog)
- Cross-model capstone remains user-orchestrated until Phase 3 automates S2/S5

Do not start Phase 3 until Phase 2 acceptance criteria met.

---

## 15. SYNTH input index

| SYNTH | Contribution to Phase 2 plan |
|-------|------------------------------|
| **81** | Five-signal stack; TSD/SurpMark priority; TMR default correct |
| **82** | Commercial cone/synonym failure; dual reporting; no Turnitin Booth cite |
| **83** | Code gap matrix; TSD ~20 LOC; ladder; test gaps |
| **84** | TPR@FPR, URSS, bench layers, honest reporting |
| **85** | Anti-detector ladder ordering; structural before lexical LLM |
| **86** | Dynamics deps for Phase 3 pipeline; not Phase 2 scope |
| **87** | Refusals: no score targeting, no strip modes |
| **88** | TempParaphraser selection loop → Phase 2 bench analog |
| **89** | Signal orthogonality; structural ≠ DivEye; three-axis eval |
| **90** | voice-match vs anti-detector target conflict |
| **91** | Preserve stance; inject variance not warmth |
| **92** | Stylometry structural sprint spec (Workstream D) |
| **93–96** | Market/regulatory/segment context for Boundaries copy |

---

## 16. Bottom line

Phase 2 makes unslop **measure and nudge the 2026 detector frontier** — surprisal dynamics, transition patterns, stylometry-guided structure — while keeping TMR as a secondary diagnostic and refusing bypass marketing. Lexical scrub stays necessary; it is no longer sufficient. The product truth unchanged: **remove slop, restore register, document limits, escalate to cross-model paraphrase with explicit ethics boundaries.**

Ship measurement first. Wire the ladder. Close the stylometry loop. Bench honestly with TPR@FPR and dynamics before/after. Phase 3 LLM pipeline builds on this foundation — it does not replace it.

---

*PLAN-98 complete. Orchestrator: Master Integration Agent #98. Feeds implementation backlog and Phase 3 planning.*
