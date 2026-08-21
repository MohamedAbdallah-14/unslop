# PLAN-97 — Phase 0–1 Implementation Plan

**Master Integration Agent #97**  
**Date:** 2026-08-19  
**Inputs:** All `SYNTH-81` through `SYNTH-96`, `UPDATE-PLAN-2026-08.md`, codebase audit (`detector.py`, `cli.py`, `surprisal.py`, `stylometry.py`, `lexical_targets.py`, `structural.py`, benchmarks)  
**Scope:** Phase 0 (research + citation hygiene) and Phase 1 (quick wins, TSD spike, detector bench, stylometry closed loop)  
**Out of scope here:** Phase 2 dynamics targets (`dynamics_targets.py`, SurpMark, cone proxy), Phase 3 `llm_pipeline.py`

---

## Executive summary

August 2026 research converges on one code truth: **unslop's philosophy is correct; wiring and measurement are incomplete.** Lexical scrub works (~88–92% AI-ism removal). Deterministic passes move TMR **~0.0–0.2 pp** — expected. The feedback ladder stops at `full+structural+soul` and never reaches `anti-detector`. `lexical_targets.py` is a no-op without `stylometric_baseline.json`. DivEye features compute in `surprisal.py` but do not flow into `--detector-feedback` JSON. Docs cite wrong papers (Liang → Tulchinskii), wrong benchmarks (Booth → Turnitin), and April 2026 landscape.

**Phase 0 (≈3 days, parallel):** Refresh `docs/research/` Wave A (Cat 05, 15, 16), fix SSOT citation/attribution errors, add August 2026 block to `research-updating.md`.

**Phase 1 (≈2–3 weeks):** Four UPDATE-PLAN quick wins plus three integration tracks:

| Track | Deliverable | Primary files |
|-------|-------------|---------------|
| **Quick wins** | `anti-detector` on ladder; baseline JSON; surprisal in feedback; SKILL landscape | `detector.py`, `cli.py`, `skills/unslop/SKILL.md` |
| **TSD spike** | `compute_tsd_reading()` + tests; log in feedback iterations | `surprisal.py`, `detector.py` |
| **Detector bench** | `shield_metrics.py`, TPR@FPR=5%, feedback-loop column, committed baseline JSON | `benchmarks/`, `unslop/scripts/shield_metrics.py` |
| **Stylometry loop** | Pre/post `StyleProfile`, paragraph API, gap-gated Phase 1–2 | `stylometry.py`, `structural.py`, `humanize.py`, `lexical_targets.py` |

**Honesty constraint (non-negotiable):** No marketing detector pass. TMR is diagnostic. Report slop removal first; detector deltas in research appendices with fixed-FPR metrics (SYNTH-84).

---

## Synthesis map — what each SYNTH contributes to Phase 0–1

| SYNTH | Phase 0–1 takeaway |
|-------|-------------------|
| **81** Academic detection | TMR default correct; TSD/SurpMark gaps; report TPR@FPR; fix Liang citation |
| **82** Commercial | Remove Booth/Turnitin conflation; dual-report GPTZero ≠ Pangram |
| **83** Code gap | Ladder + surprisal wiring P0; TSD ~20 LOC; `detector_feedback_bench.py` |
| **84** Benchmarks | `shield_metrics.py`; TPR@FPR=5%; URSS bundle; no CI commercial APIs |
| **85** Evasion prompts | CoPA dual-prompt in anti-detector intensity; fix TempParaphraser comment |
| **86** LLM pipeline | Phase 3 only — document exhaustion message; no `llm_pipeline.py` in P0–1 |
| **87** Refusals | No score targeting; no strip modes; four-question gate in SKILL |
| **88** Practitioner tools | Cross-model capstone docs; Ryter/Alammyan misattribution fix |
| **89** Stylometry signals | Ship baseline; measure σ/CV/contractions; split voice vs anti-detector |
| **90** Voice-match | Citation fix (23.5× → Jemama); genre caveat — docs only in P0–1 |
| **91** Human cues | ANTI-BLANDIFICATION stays; no warmth injection in anti-detector prompts |
| **92** Stylometry integration | **Core stylometry loop spec** — Sprint A–C subset for Phase 1 |
| **93–96** Market/policy/segments | README audience blocks; four-question gate; Boundaries copy |

---

## Phase 0 — Research corpus refresh + citation fixes

**Duration:** ~3 days (can run parallel with Phase 1 Sprint A)  
**Deliverable:** August 2026 maintainer checklist executed for priority categories; SSOT docs corrected; `docs/research/research-updating.md` gains **August 2026** block.

### 0.1 Priority research categories (Wave A)

From UPDATE-PLAN Part 4 and SYNTH-81/84:

| Cat | Path | Updates |
|-----|------|---------|
| **05** | `docs/research/05-ai-text-detection-and-evasion/` | TSD, SurpMark, DivEye, GPTZero v6 cones, HIP, Why Detection Fails, five-signal stack |
| **15** | `docs/research/15-academic-papers-llm-humanization/` | MASH, TempParaphraser, Adversarial Paraphrasing, Alignment Tax, blandification |
| **16** | `docs/research/16-github-tools-libraries/` | IBM DivEye impl, detector.py gap, peakoss/ANTISLOP stack position |
| **18** | `docs/research/18-commercial-humanizer-tools/` | Undetectable/Ryter/Walter, QuillBot, Superhuman; DAMAGE L1/L3; fix Ryter→Alammyan |
| **09** | `docs/research/09-bias-fairness-ethics/` | Liang ESL, institutional retreat, OCR Title VI, Newby |

**Cross-cutting doc edits:**

- EU AI Act Art. 50: **"in force"** (Aug 2, 2026), not "upcoming"
- Five-signal detector stack diagram (SYNTH-81 §1.6)
- RateAudit / score-gaming: cite as anti-pattern, not feature
- Watermark: side effect + refuse strip (SYNTH-95)

### 0.2 SSOT citation fixes (P0 — ship before or with Phase 1)

Edit **`skills/unslop/SKILL.md`** only (mirrors via CI sync):

| Location | Current (wrong) | Correct |
|----------|-----------------|---------|
| Boundaries ESL cite | `arXiv:2306.04723` | **Liang et al. 2023 — [arXiv:2304.02819](https://arxiv.org/abs/2304.02819)** |
| Anti-detector landscape § | "Chicago Booth 2026… Turnitin drops to 60–85%" | Remove Turnitin from Booth; cite Blommerde [I] or DetectAIve Class III (#66). Booth = Jabarian & Imas 2025, **one humanizer (StealthGPT)** |
| Landscape date | "April 2026" | **August 2026** — GPTZero v6 cones, Turnitin Feb 2026 retrain, Originality AI Allowance |
| Catch Me limitation | "23.5× few-shot gain" attributed to Catch Me | **Jemama** 23.5× style match; Catch Me Blog AV ~17–21% (SYNTH-90) |
| Contraction cite | "Kalemaj" (if present) | **Paneru et al. 2026** — [arXiv:2604.11687](https://arxiv.org/abs/2604.11687) |
| Optional remove | "~6 points median accuracy drop" | Not in Jabarian & Imas — remove or cite HumanizerBench/DAMAGE with date |

**Also update (same PR wave, non-mirror):**

| File | Change |
|------|--------|
| `README.md` | Booth/Turnitin attribution; four-segment "Who this is for" (SYNTH-96); no bypass CTA |
| `docs/RESEARCH_AND_TECH.md` | Five-signal stack; TMR ≠ commercial pass; dual-report rule |
| `skills/unslop-help/SKILL.md` | Cross-links to Boundaries + four-question gate |
| `unslop/scripts/detector.py:389–392` | Fix TempParaphraser comment: paper requires LLM paraphrase; unslop recommends cross-model as **user-orchestrated** step |

### 0.3 `research-updating.md` August 2026 block

Append to `docs/research/research-updating.md`:

```markdown
## August 2026 refresh (detector research sprint)

- Five-signal stack: lexical, burstiness, DivEye σ, TSD late-half, GPTZero cones
- TMR remains feedback default; deterministic Δp_ai ~0.0–0.2 pp on fixtures
- Phase 1 wiring: anti-detector ladder, stylometric baseline, surprisal telemetry, TSD spike
- Commercial: Pangram robust under StealthGPT; GPTZero paraphrase-fragile; no Turnitin in Booth
- Regulatory: Art. 50 in force; watermark side effect documented; refuse strip modes
```

### 0.4 Phase 0 acceptance

- [ ] Liang citation is **2304.02819** in SSOT SKILL.md
- [ ] No "Turnitin at Booth" or "twelve humanizers at Booth" in SSOT/README
- [ ] Cat 05/15/16 INDEX or SYNTHESIS mention TSD, SurpMark, GPTZero v6, HIP
- [ ] `research-updating.md` has August 2026 section with date stamp
- [ ] Mirrors regenerated by CI on merge (do not hand-edit `.cursor/`, `plugins/` copies)

### 0.5 Phase 0 test plan

- Manual: grep repo for `2306.04723`, `Turnitin.*Booth`, `twelve humanizer`
- `python3 -m pytest tests/unslop/` — docs-only change must stay green
- Optional: link check on arXiv URLs in edited paragraphs

---

## Phase 1 — Quick wins (UPDATE-PLAN items 1–4)

### 1.1 Add `anti-detector` to detector feedback ladder

**Problem (SYNTH-83):** `anti-detector` exists in `humanize.py` but `DEFAULT_LADDER` caps at `("full", True, True)`.

**Files:**

| File | Change |
|------|--------|
| `unslop/scripts/detector.py` | Extend `DEFAULT_LADDER` with step 4: `("anti-detector", True, True)`. Extend `LADDER_AGGRESSIVE` similarly. Bump default `max_iterations` to **4** when using default ladder (CLI currently passes 3). |
| `unslop/scripts/detector.py` | Ensure `humanize_fn` path passes intensity through — already uses `humanize_deterministic_with_report(text, intensity=..., structural=..., soul=...)`. Step 4 must use `intensity="anti-detector"`. |
| `unslop/scripts/cli.py` | When `--detector-feedback` and not aggressive: default `max_iterations=4`. Document in `--help`. |
| `tests/unslop/test_detector.py` | Add `test_ladder_includes_anti_detector`: mock ladder exhaust reaches 4th step with `intensity=="anti-detector"`. |
| `skills/unslop/SKILL.md` | Document ladder order: balanced → full → full+struct+soul → **anti-detector+struct+soul**. Note: diagnostic only, not pass guarantee. |

**Ladder spec (final):**

```python
DEFAULT_LADDER = [
    ("balanced", False, False),
    ("full", False, False),
    ("full", True, True),
    ("anti-detector", True, True),  # NEW — invokes lexical_targets when baseline present
]
```

**Boundaries (SYNTH-87):** Ladder exhaustion message unchanged except TempParaphraser comment fix. Do **not** add score-targeting or auto LLM inside loop.

### 1.2 Ship `stylometric_baseline.json`

**Problem:** `lexical_targets.load_baselines()` reads `benchmarks/results/stylometric_baseline.json` — file absent → all gaps empty.

**Files:**

| File | Change |
|------|--------|
| `benchmarks/corpus/human/` | **Create** — seed with 8–12 human prose samples (README excerpts, public-domain essays, PERSUADE subsample if licensed). Target ≥50 words each, mixed genres. |
| `benchmarks/corpus/llm/` | **Create** — same count: raw assistant-output fixtures from `benchmarks/fixtures/*.md` (pre-humanize). |
| `benchmarks/results/stylometric_baseline.json` | **Generate** via `python3 benchmarks/stylometric_baseline.py --human benchmarks/corpus/human --llm benchmarks/corpus/llm` |
| `benchmarks/results/stylometric_baseline.md` | Auto-generated summary table (script output) |
| `tests/unslop/test_lexical_targets.py` | Assert `load_baselines()` non-empty when baseline committed; `measure_gaps()` returns ≥1 gap on `flat-paragraph-bait` fixture at `anti-detector`. |

**Minimum fields in JSON** (SYNTH-92):

` sentence_length_stdev`, `sentence_length_cv`, `latinate_ratio`, `type_token_ratio`, `function_word_rate`, `contraction_rate`, `fragment_rate`, `em_dash_rate`

**Metadata:** include `generated_at`, `n_human`, `n_llm`, unslop version/git SHA.

### 1.3 Wire surprisal into `--detector-feedback`

**Problem:** `--surprisal-variance` is one-shot; feedback loop accepts `surprisal_fn` but CLI never passes it.

**Files:**

| File | Change |
|------|--------|
| `unslop/scripts/cli.py` | Add `--detector-surprisal` flag (or extend `--detector-feedback` to auto-enable surprisal telemetry when `surprisal.is_available()`). Pass `surprisal_fn` reading `compute_surprisal_variance(text).surprisal_stdev`. |
| `unslop/scripts/detector.py` | Extend `IterationRecord` + `to_dict()` with optional `surprisal: dict | None` — full `SurprisalReading.to_dict()` when flag set (not just stdev). |
| `unslop/scripts/cli.py` | Include `surprisal` block in `--json` detector_feedback payload per iteration. |
| `tests/unslop/test_cli.py` | Mock surprisal_fn via patched `feedback_loop`; assert JSON contains `surprisal_stdev`. |
| `tests/unslop/test_detector.py` | Test `surprisal_fn` populates `IterationRecord.surprisal_stdev`. |

**Default model note (SYNTH-83 P1):** Document in CLI help that default `distilgpt2` is uncertified vs paper `gpt2`; optional `--surprisal-model gpt2` for parity runs. Do not change default in Phase 1 unless `diveye_comparison` CI proves rank-order stable.

### 1.4 Refresh SKILL.md landscape (August 2026)

**Content blocks to add/replace** (SYNTH-82, 93, 94, 96):

1. **Five-signal stack** — what 2026 detectors read; what unslop covers (table from UPDATE-PLAN Part 2)
2. **Commercial honesty** — dual-report; GPTZero ≠ Pangram; Originality Turbo vs AI Allowance
3. **Institutional context** — 60+ university detector disables; ESL defense framing (Liang **2304.02819**)
4. **Anti-detector procedure** — four-question gate (SYNTH-94 §3.2, SYNTH-96)
5. **Cross-model capstone** — practitioner workflow (SYNTH-88); user-orchestrated, not automated
6. **DetectAIve framing** — Class III vs IV; anti-detector on human drafts only
7. **Voice-match vs anti-detector** — Jemama two-axis paragraph (SYNTH-90)
8. **Watermark** — side effect paragraph unchanged; add C2PA one-liner (SYNTH-95)

**Sync:** Run `scripts/sync-mirrors.sh` locally before PR or rely on CI `sync.yml`.

### 1.5 CoPA-style anti-detector prompt (SYNTH-85 P0)

| File | Change |
|------|--------|
| `unslop/scripts/humanize.py` | Expand `_INTENSITY_PROMPT_GUIDANCE["anti-detector"]` with CoPA dual-prompt negative spec (remove assistant patterns; preserve facts). Deterministic path unchanged; LLM path only. |
| `tests/unslop/test_humanize.py` | Snapshot test: anti-detector guidance contains "hedging" and "parallel structure" negatives. |

---

## Phase 1 — TSD spike (early dynamics telemetry)

**Research basis:** TSD (arXiv:2601.04833) — second-half derivative dispersion (DD) + local volatility (LV). Orthogonal to global DivEye σ (SYNTH-81, 89, 55).

**Phase 1 scope:** Measurement + logging only. **No** stop condition, **no** `dynamics_targets.py` (Phase 2).

### 2.1 Implement `compute_tsd_reading()`

**File:** `unslop/scripts/surprisal.py`

```python
@dataclass
class TSDReading:
    second_half_dd: float      # std of |Δ surprisal| on positions > n/2
    second_half_lv: float      # mean local volatility in second half
    first_half_dd: float       # control — expect higher than second half on AI text
    token_count: int

def compute_tsd_reading(
    text: str,
    *,
    model: str | None = None,
    min_tokens: int = 20,
) -> TSDReading: ...
```

**Implementation notes:**

- Reuse existing token surprisal tensor from `compute_surprisal_variance()` internals — extract shared `_token_surprisals(text, model)` helper to avoid double forward pass.
- Split sequence at `ceil(n/2)`; compute DD as `stdev(abs(diff(surprisals[i], surprisals[i+1])))` on each half.
- LV: rolling window std (window=5) mean over second half.
- Raise `SurprisalUnavailable` same as DivEye path.
- Guard: `min_tokens` — return zeros or skip with warning if text too short (SYNTH-83 test gap).

### 2.2 Wire TSD into feedback loop (telemetry)

| File | Change |
|------|--------|
| `unslop/scripts/detector.py` | Optional `tsd_fn` injection; add `tsd_second_half_dd`, `tsd_second_half_lv` to `IterationRecord` and `to_dict()`. |
| `unslop/scripts/cli.py` | When `--detector-surprisal` enabled, also compute TSD per iteration (same model). |
| `unslop/scripts/surprisal.py` | Add `compute_surprisal_dynamics()` thin wrapper returning `{divEye: SurprisalReading, tsd: TSDReading}` — foundation for Phase 2. |

### 2.3 TSD tests

| Test | File | Assertion |
|------|------|-----------|
| Synthetic flat sequence | `tests/unslop/test_surprisal.py` | Fake LM: second_half_dd < first_half_dd (AI-settle pattern) |
| Synthetic bursty sequence | same | second_half_dd ≥ first_half_dd or no decay |
| Short text guard | same | `< min_tokens` → graceful skip |
| Feedback hook | `tests/unslop/test_detector.py` | Mock `tsd_fn` appears in iteration dict |

### 2.4 TSD benchmark (manual / opt-in)

| Command | Output |
|---------|--------|
| `UNSLOP_RUN_REAL_SURPRISAL=1 python3 -m pytest tests/unslop/test_surprisal.py -k tsd` | Real LM smoke |
| Extend `benchmarks/diveye_comparison/run.py` | Log TSD before/after on 9 fixtures — **do not gate CI** until baseline committed |

**Phase 1 TSD acceptance:** Functions exist, unit tests pass with mocked LM, feedback JSON includes TSD fields when surprisal flag set. **Not** required: anti-detector raises DD on 7/9 fixtures (Phase 2 acceptance per UPDATE-PLAN).

---

## Phase 1 — Detector bench upgrades

**Basis:** SYNTH-84, 83, 81.

### 3.1 New module: `unslop/scripts/shield_metrics.py`

Pure numpy (no torch):

```python
def w_auroc(y_true, y_score, k=20 * log(2)) -> float: ...
def sfd(scenario_fprs: list[float], lambda_=10 * log(2)) -> float: ...
def urss(w_aurocs: list[float], sfd: float) -> float: ...
def tpr_at_fpr(y_true, y_score, target_fpr=0.05, eps=0.0005, max_iter=50) -> tuple[float, float]: ...
```

**Tests:** `tests/unslop/test_shield_metrics.py` — synthetic scores where TPR@5% is known analytically.

### 3.2 Extend `benchmarks/detector_bench.py`

| Change | Detail |
|--------|--------|
| **Fixtures** | All 9 `benchmarks/fixtures/*.md` + add `benchmarks/fixtures/esl-short.md` (Liang-style formal L2 prose stub) |
| **Intensities** | `subtle`, `balanced`, `full`, `anti-detector` (deterministic) |
| **New column** | `feedback_loop` — run `detector.feedback_loop()` with mock or real TMR per fixture |
| **Metrics** | Emit `mean_p_ai`, `delta_p_ai`, `tpr_at_fpr_5` when label pairs available |
| **Output** | `benchmarks/results/<stamp>-detectors.json` + markdown summary |
| **Release gate** | Keep soft gate: balanced must not **increase** mean p_ai vs original. Add honesty line when Δ < 1 pp. |

### 3.3 New harness: `benchmarks/detector_feedback_bench.py`

**Purpose:** CI-safe loop regression (SYNTH-83 P0 #2).

| Mode | Behavior |
|------|----------|
| Default | Mock `score_fn` — verify ladder order, iteration count, anti-detector step present |
| Opt-in | `UNSLOP_RUN_DETECTOR_BENCH=1` — real TMR on 3-fixture subset |

Output: `benchmarks/results/<stamp>-feedback-loop.json`

### 3.4 Commit baseline detector results

| File | Action |
|------|--------|
| `benchmarks/results/2026-08-detector-baseline.json` | First full run post Phase 1; pin in PR |
| `benchmarks/README.md` | Document slop delta ≠ detector evasion; TPR@FPR reporting |

### 3.5 Detector bench test plan

| Layer | Command | Gate |
|-------|---------|------|
| CI always | `python3 -m pytest tests/unslop/test_detector.py tests/unslop/test_shield_metrics.py` | Hard |
| CI always | `python3 benchmarks/detector_feedback_bench.py` (mock mode) | Hard — add to CI or pre-release script |
| Release opt-in | `python3 benchmarks/detector_bench.py` | Manual / weekly |
| Real weights | `UNSLOP_RUN_DETECTOR_BENCH=1` | Optional nightly |

**Do not:** GPTZero/Pangram/Turnitin API in CI (SYNTH-84 §1.3). Commercial panel stays in `drafts/2026-05-detector-test/`.

---

## Phase 1 — Stylometry closed loop

**Basis:** SYNTH-92 (primary), SYNTH-89, 90.

**Goal:** Measure → edit toward gaps → re-measure for Phase 1 (`structural.py`) and Phase 2 (`lexical_targets.py`). Contraction injection stays in `soul.py` (Phase 5).

### 4.1 Sprint A — Measurement foundation (3–4 days)

| ID | Task | File(s) |
|----|------|---------|
| A1 | `analyze_paragraphs()` → `ParagraphStyleStats` | `unslop/scripts/stylometry.py` |
| A2 | `StylometryContext` dataclass; pre/post in `humanize_deterministic_with_report` | `unslop/scripts/humanize.py` |
| A3 | Refactor `structural._paragraph_sigma` to use stylometry helper | `unslop/scripts/structural.py` |
| A4 | Baseline JSON (see §1.2) | `benchmarks/` |

**`HumanizeReport` extension:**

```python
@dataclass
class HumanizeReport:
    ...
    stylometry_before: dict | None = None
    stylometry_after: dict | None = None
    stylometric_gaps: list[dict] | None = None
```

**CLI:** `--report` / `--json` includes `stylometry.delta` when present.

### 4.2 Sprint B — Phase 1 structural closed loop (4–5 days)

| ID | Task | File(s) |
|----|------|---------|
| B1 | `StructuralTargets` + `resolve_structural_targets(ctx, mode, voice_profile)` | `structural.py`, `humanize.py` |
| B2 | Pass `flat_paragraph_indices` from ctx into `split_long_sentences` | `structural.py` |
| B3 | `StructuralReport`: `sigma_before/after`, `cv_before/after`, `deadlocks: list[int]` | `structural.py` |
| B4 | Single bounded retry if Δσ < 0.5 after first pass | `structural.py` |
| B5 | Unify `validate._count_flat_paragraphs` with stylometry helper | `validate.py` |

**Mode-aware targets (SYNTH-92 §3.3):**

| Mode | `target_sigma` |
|------|----------------|
| `voice-match` + sample | `max(sample_σ * 0.9, 3.0)` |
| `anti-detector` | `6.0` |
| `balanced` / default | `5.0` (unchanged) |

### 4.3 Sprint C — Phase 2 lexical closed loop (3–4 days)

| ID | Task | File(s) |
|----|------|---------|
| C1 | Gap-gate `_replace_latinate` at `balanced`; unconditional at `full`/`anti-detector` | `lexical_targets.py` |
| C2 | Report structural gaps at `balanced` even when lexical_targets not run | `humanize.py` |
| C3 | Wire `apply_targeted_pass(gaps)` after structural when intensity ≥ `full` | already partial — verify with baseline |
| C4 | Ablation tests on `flat-paragraph-bait.md` | `tests/unslop/test_humanize.py` |

### 4.4 Stylometry ↔ anti-detector ladder integration

When feedback loop hits step 4 (`anti-detector`):

1. `humanize_deterministic_with_report(..., intensity="anti-detector", structural=True, soul=True)`
2. `apply_targeted_pass` runs inside humanize when baseline present
3. Log `stylometry_before/after` in iteration metadata (extend `IterationRecord` or attach `HumanizeReport` snapshot)

### 4.5 Stylometry test plan

| Test | Assertion |
|------|-----------|
| `test_stylometry_paragraphs.py` (new) | Flat vs varied paragraph σ |
| `test_structural_targets.py` (new) | voice-match vs anti-detector σ targets differ |
| `test_humanize_stylometry_report.py` | `--report` includes before/after profiles |
| `TestPreservation` | Full suite green after structural retry |
| Benchmark | `benchmarks/run.py` row: σ, CV, flat_paragraphs before/after structural-only |

---

## Master file change matrix

| File | Phase 0 | Phase 1 |
|------|---------|---------|
| `skills/unslop/SKILL.md` | Citations, landscape, gate, five-signal | Ladder docs, anti-detector CoPA prompt ref |
| `README.md` | Booth fix, segments, honesty | Benchmark numbers after real run only |
| `docs/research/**` | Wave A updates | — |
| `docs/research/research-updating.md` | Aug 2026 block | — |
| `docs/RESEARCH_AND_TECH.md` | Five-signal, dual-report | TSD telemetry note |
| `skills/unslop-help/SKILL.md` | Gate + cross-refs | — |
| `unslop/scripts/detector.py` | TempParaphraser comment | Ladder, TSD/surprisal fields, max_iter |
| `unslop/scripts/cli.py` | — | surprisal fn, max_iter=4, JSON payload |
| `unslop/scripts/surprisal.py` | — | TSD, `compute_surprisal_dynamics()` |
| `unslop/scripts/shield_metrics.py` | — | **New** |
| `unslop/scripts/stylometry.py` | — | `analyze_paragraphs()` |
| `unslop/scripts/structural.py` | — | Targets, report extensions |
| `unslop/scripts/humanize.py` | — | StylometryContext, report fields, CoPA prompt |
| `unslop/scripts/lexical_targets.py` | — | Gap-gate Latinate at balanced |
| `unslop/scripts/validate.py` | — | Flat count SSOT |
| `benchmarks/stylometric_baseline.py` | — | Run + commit output |
| `benchmarks/corpus/human/**` | — | **New** seed corpus |
| `benchmarks/corpus/llm/**` | — | **New** seed corpus |
| `benchmarks/results/stylometric_baseline.json` | — | **New** committed artifact |
| `benchmarks/detector_bench.py` | — | Intensities, fixtures, metrics |
| `benchmarks/detector_feedback_bench.py` | — | **New** |
| `benchmarks/README.md` | — | Honesty + TPR@FPR docs |
| `tests/unslop/test_surprisal.py` | — | TSD tests |
| `tests/unslop/test_detector.py` | — | anti-detector ladder, tsd/surprisal hooks |
| `tests/unslop/test_cli.py` | — | JSON surprisal block |
| `tests/unslop/test_shield_metrics.py` | — | **New** |
| `tests/unslop/test_lexical_targets.py` | — | Baseline non-empty |
| `tests/unslop/test_stylometry*.py` | — | Paragraph + targets |
| `.github/workflows/sync.yml` | — | Verify triggers include SKILL paths |

**Explicit non-goals (Phase 0–1):**

- `dynamics_targets.py`, SurpMark, cone proxy (Phase 2)
- `llm_pipeline.py` (Phase 3)
- Watermark strip, SIRA/BIRA, score-targeting scheduler
- Commercial detector API automation
- Default LM change distilgpt2 → gpt2 without ablation

---

## Sequencing — recommended sprint calendar

```
Week 1
├── P0 docs: SKILL citation fixes + landscape draft (Phase 0.2)
├── A1–A4 stylometry measurement + baseline corpus
├── shield_metrics.py + tests
└── TSD: compute_tsd_reading + unit tests

Week 2
├── detector.py ladder + cli surprisal/tsd wiring
├── detector_feedback_bench.py (mock CI)
├── Sprint B structural targets
└── Phase 0 Wave A: Cat 05/15/16 research edits

Week 3
├── Sprint C lexical gap-gating
├── detector_bench.py full fixture matrix
├── Commit detector + stylometric baseline JSON
├── SKILL final pass + sync mirrors
└── Full pytest + preservation + optional real TMR run
```

**Parallel tracks:** Docs (Phase 0) and code (Phase 1) can overlap after SSOT citation fix lands in Week 1.

---

## Combined test plan (release checklist)

### Must pass every PR (deterministic)

```bash
python3 -m pytest tests/unslop/ -q
python3 benchmarks/detector_feedback_bench.py   # mock mode
```

### Phase 1 exit gate

```bash
# 1. Preservation contract
python3 -m pytest tests/unslop/test_humanize.py::TestPreservation -q

# 2. Ladder includes anti-detector
python3 -m pytest tests/unslop/test_detector.py -q

# 3. Baseline loads
python3 -c "from unslop.scripts.lexical_targets import load_baselines; assert load_baselines()['fields']"

# 4. CLI feedback JSON shape
python3 -m pytest tests/unslop/test_cli.py -k detector -q

# 5. TSD + surprisal unit tests
python3 -m pytest tests/unslop/test_surprisal.py -q

# 6. Stylometry paragraph + structural targets
python3 -m pytest tests/unslop/ -k "stylometr or structural_target" -q

# 7. Shield metrics
python3 -m pytest tests/unslop/test_shield_metrics.py -q
```

### Opt-in heavy (pre-release / weekly)

```bash
UNSLOP_RUN_REAL_SURPRISAL=1 python3 -m pytest tests/unslop/test_surprisal.py -k "real or tsd" -q
UNSLOP_RUN_DETECTOR_BENCH=1 python3 benchmarks/detector_bench.py
UNSLOP_RUN_DETECTOR_BENCH=1 python3 benchmarks/detector_feedback_bench.py --real
python3 benchmarks/run.py --strict
python3 benchmarks/stylometric_baseline.py --human benchmarks/corpus/human --llm benchmarks/corpus/llm  # verify regen
```

### Manual verification

| Check | Method |
|-------|--------|
| Hook ladder | `bash hooks/install.sh`; `/unslop anti-detector`; `stop unslop` |
| CLI feedback | `echo "..." \| python3 -m unslop.scripts.cli --detector-feedback --detector-surprisal --json` |
| Mirror sync | Push to branch; confirm CI sync job updates `.cursor/skills/unslop/SKILL.md` |
| Doc grep | No `2306.04723`, no Turnitin-at-Booth |

---

## Acceptance criteria (Phase 0–1 complete)

### Phase 0

1. SSOT citations corrected (Liang, Booth/Turnitin, Jemama vs Catch Me)
2. August 2026 landscape in SKILL.md (date + five-signal + dual-report)
3. `research-updating.md` August block present
4. Cat 05/15/16 refreshed with TSD, SurpMark, GPTZero v6, HIP references

### Phase 1 — Quick wins

5. `DEFAULT_LADDER` step 4 is `anti-detector`; CLI default `max_iterations=4`
6. `stylometric_baseline.json` committed; `measure_gaps()` non-empty on AI fixtures
7. `--detector-feedback --detector-surprisal` emits per-iteration surprisal + TSD in JSON
8. TempParaphraser comment fixed in `detector.py`

### Phase 1 — TSD

9. `compute_tsd_reading()` shipped with mocked-LM tests
10. Feedback loop logs TSD fields when surprisal telemetry enabled

### Phase 1 — Detector bench

11. `shield_metrics.py` + tests green
12. `detector_feedback_bench.py` mock mode in CI or release script
13. `detector_bench.py` runs all fixtures × intensities including `anti-detector`
14. Baseline JSON committed with honest interpretation (Δp_ai ~0.0–0.2 pp documented)

### Phase 1 — Stylometry loop

15. `humanize_deterministic_with_report` records before/after `StyleProfile`
16. `analyze_paragraphs()` drives structural flat-paragraph detection
17. Anti-detector uses higher `target_sigma` than voice-match on same input (unit test)
18. Ablation: flat fixture σ increases after structural pass; preservation suite green

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Baseline corpus too small | Document n in JSON metadata; expand in Phase 2 with PERSUADE/RAID slices |
| TSD on short fixtures noisy | `min_tokens` guard; report-only on <200 tokens |
| anti-detector raises expectations | SKILL + JSON `reason_stopped` stress diagnostic, not pass |
| distilgpt2 miscalibration | Label uncertified; optional gpt2 flag |
| Stylometry retry chops prose | Max 1 retry; TestPreservation gate |
| Research doc scope creep | Wave A only in Phase 0; defer Cat 01–04 bulk to Phase 2 doc sprint |

---

## References

| Doc | Path |
|-----|------|
| Update plan | `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md` |
| Syntheses | `docs/research/2026-08-detector-research/SYNTH-81` … `SYNTH-96` |
| Maintainer guide | `CLAUDE.md` |
| Code gap detail | `SYNTH-83-DETECTION-CODE-GAP.md` |
| Stylometry integration | `SYNTH-92-STYLOMETRY-INTEGRATION.md` |
| Benchmark strategy | `SYNTH-84-DETECTION-BENCHMARKS.md` |
| May detector test | `drafts/2026-05-detector-test/` |

---

*PLAN-97 complete. Orchestrator: Master Integration Agent #97. Next: Phase 2 plan (`dynamics_targets.py`, SurpMark lite, multi-objective stop) after Phase 1 exit gate.*
