# SYNTH-92 — Stylometry Integration Plan (Phase 1–2)

**Synthesis agent:** #92  
**Date:** 2026-08-19  
**Inputs:** AGENT-41 (contraction stylometry / Paneru), AGENT-52 (voice-match limits), AGENT-54 (sentence-length variance), AGENT-42 (Biber register), SYNTH-83 (code gap), `UPDATE-PLAN-2026-08.md`  
**Code read:** `unslop/scripts/stylometry.py`, `structural.py`, `soul.py`, `lexical_targets.py`, `humanize.py` (Phase 1–2 pipeline), `validate.py` (burstiness/contraction)

---

## Executive summary

unslop already has the **measurement layer** (`stylometry.py`, 19-field `StyleProfile`) and two **deterministic edit layers** that should consume it:

| Phase | Module | What it does today | Stylometry wired? |
|-------|--------|-------------------|-------------------|
| **Phase 1** | `structural.py` | Split long sentences in flat paragraphs; merge bullet soup | **No** — fixed thresholds (`target_sigma=5.0`, `min_words=30`) |
| **Phase 2** | `humanize.py` lexical families + `lexical_targets.py` | Regex AI-ism scrub; gap-driven Latinate/function-word nudges at `full`/`anti-detector` | **Partial** — `lexical_targets` calls `analyze()` but baseline file is missing; no burstiness/contraction fields in targeted pass |
| **Phase 4 (measure-only)** | `stylometry.py` | Extract profile; `delta()` for voice-match LLM | Used post-hoc and in LLM prompts, not to steer Phase 1–2 |
| **Phase 5 (out of scope here)** | `soul.py` | Contraction injection | Outcome measured by stylometry; not closed-loop |

**Verdict:** Phase 1–2 are **architecturally adjacent to stylometry but not closed-loop**. The research memos agree on the fix: **measure first, edit toward measured gaps, re-measure** (TinyStyler extract-then-apply; Paneru marker-shift with overshoot guards). Today unslop measures in `validate.py` and `stylometry.py` with duplicated logic, edits with static rules, and only reports deltas at the end.

**Phase 1–2 goal:** Wire `StyleProfile` into structural and lexical passes so deterministic humanization **targets numeric gaps** (σ, CV, flat paragraphs, Latinate ratio, TTR) without crossing into Phase 5 soul or LLM-only fragment injection. Contraction and short-sentence tails stay in soul / anti-detector LLM — documented boundary, not a gap to "fix" in Phase 1–2.

**Highest-ROI sequence (2–3 weeks):**

1. Unify measurement SSOT — `stylometry.analyze()` everywhere; deprecate duplicate `_burstiness()` for reporting  
2. Ship `benchmarks/results/stylometric_baseline.json` so `lexical_targets` actually runs  
3. Add `StylometryContext` pre/post wrapper around Phase 1–2 in `humanize_deterministic_with_report`  
4. Parameterize `structural.py` from profile gaps (flat paragraphs, σ, CV)  
5. Extend `lexical_targets` with safe Phase-2-only gap rules (Latinate, TTR, function words — already started)  
6. Benchmark + CI: σ/CV/flat_paragraphs before/after structural-only and full Phase 1–2 ablations

---

## 1. Research synthesis — what Phase 1–2 must optimize

### 1.1 Three axes (do not collapse)

From AGENT-52 / Jemama / Catch Me If You Can:

| Axis | Primary signals | Phase 1–2 role |
|------|-----------------|----------------|
| **Syntactic rhythm** | σ(sentence length), CV, flat paragraphs, fragment rate | **Phase 1 primary** |
| **Lexical register** | TTR, function-word rate, Latinate ratio, latinate suffix density | **Phase 2 primary** |
| **Token distribution** | Contraction rate, surprisal variance | **Phase 5 + surprisal.py** — Phase 1–2 only *measure*, do not inject |

Voice-match and anti-detector **conflict** on σ and contractions (AGENT-52). Phase 1–2 integration must accept a **mode flag**:

- `voice_sample` / persisted profile → structural targets = **sample σ/CV** (may be low for ESL)  
- `anti-detector` / no sample → structural targets = **floor bands** (σ ≥ 6, CV ≥ 0.5 per SKILL.md)  
- Default `balanced` → structural uses **human baseline bands** from `stylometric_baseline.json`, not anti-detector floor

### 1.2 Sentence-length variance (Phase 1 evidence)

AGENT-54 / Desaire 2023 / practitioner Cat 14:

- Mean sentence length **does not separate** human vs AI; **σ within paragraph does**  
- Human academic σ ~6–8+; GPT-4o ~4.1; unslop structural `target_sigma=5.0` sits between  
- CV (σ/μ) scale-invariant; `stylometry.sentence_length_cv` already exported — structural pass ignores it  
- **Split-only restoration** is intentional (low false-positive risk); short-sentence injection is **not** Phase 1 scope  
- Adversarial Paraphrasing: lexical-only rewrite **increases** detector TPR — Phase 1 must run **after** lexical scrub (already correct in `humanize.py`)

### 1.3 Contraction stylometry (Phase 1–2 boundary)

AGENT-41 / Paneru (2026), arXiv:2604.11687:

- Strong single marker: AI ~0.00 vs human ~0.17 contractions/chunk  
- Overshoot is its own tell (Mistral 0.383 vs target 0.17) — soul's `preserve_first_sentence` is the model  
- **Phase 1–2 must not inject contractions** — that's `soul.py` (Phase 5)  
- Phase 1–2 **should** record `contraction_rate` in pre/post `StyleProfile` for validator alignment and future rate-cap on soul  
- Reconcile units: Paneru ~3.3/1k vs validator ~17/1k — document dual baselines; do not hard-code Paneru into Phase 1–2 thresholds until ablation run

### 1.4 Register / Biber gap (Phase 2 ceiling)

AGENT-42 / Rallapalli: genre > model > decoding. unslop's 19 regex proxies cover ~15 surface tells, not Biber's 67 POS/register features. Phase 2 lexical_targets Latinate swap list is the **safe subset** of register work — no spaCy dependency in Phase 1–2 plan. Optional future: `--register-audit` with pybiber, not blocking this integration.

---

## 2. Current code map

### 2.1 Pipeline order (`humanize_deterministic_with_report`)

```
strip_reasoning (opt-in)
  → _protect()
  → Phase 2 lexical regex families (intensity-gated)
  → Phase 1 structural (if structural=True)     ← stylometry NOT consulted
  → lexical_targets.apply_targeted_pass (full/anti-detector only)
  → Phase 5 soul (if soul=True)                 ← out of SYNTH-92 scope
  → em-dash cap, cleanup
  → _unprotect()
```

Phase 1 runs **after** lexical scrub (correct per AdvPara). Phase 2 `lexical_targets` runs **after** structural — Latinate swaps may change word counts and σ slightly; acceptable; re-measure post-pass.

### 2.2 `stylometry.py` — SSOT for measurement

**Shipped:** `analyze(text) → StyleProfile`, `StyleProfile.delta()`, `format_delta()`, DivEye proxies (`sentence_length_cv`, `word_length_stdev`).

**Prose contract:** strips YAML, code, tables, blockquotes, inline code — aligned with validator intent.

**Not wired to Phase 1–2:** no `analyze_paragraphs()` returning per-paragraph σ; structural recomputes σ internally via `_paragraph_sigma`.

### 2.3 `structural.py` — Phase 1

| Parameter | Default | Research basis |
|-----------|---------|----------------|
| `target_sigma` | 5.0 | AI ~4, human ~8.2 |
| `flat_min_words` / `min_words` | 20 / 30 | Flat-paragraph regime |
| `min_half` | 8 | Split balance guard |

**Gaps vs stylometry:**

- Document-level `sentence_length_stdev` in `StyleProfile` ≠ per-paragraph σ used for edits  
- No CV-aware targeting (short docs bias σ down)  
- No feedback when split candidates absent (deadlock: five 24-word sentences, no connector)  
- `StructuralReport` counts splits/merges but not Δσ or ΔCV

### 2.4 `lexical_targets.py` — Phase 2 stylometric nudges

**Shipped:** `measure_gaps()` vs `stylometric_baseline.json` p25/p75 bands; `apply_targeted_pass()` for Latinate replacement, function-word injection, synonym-cycling dampening.

**Blockers:**

- `benchmarks/results/stylometric_baseline.json` **not in repo** — `load_baselines()` returns `{}`; gap list always empty unless file shipped  
- `apply_targeted_pass` re-`_protect()`s text (double protection safe but redundant)  
- No gaps for `sentence_length_stdev`, `sentence_length_cv`, `fragment_rate`, `contraction_rate` — correctly excluded from deterministic injection in Phase 2, but should **drive Phase 1 params** and **report**

### 2.5 Duplication with `validate.py`

| Metric | validate.py | stylometry.py |
|--------|-------------|---------------|
| Burstiness σ | `_burstiness()` document-wide | `sentence_length_stdev` document-wide |
| Flat paragraphs | `_count_flat_paragraphs()` σ < 3.0 | not exposed |
| Contractions/1k | `_contraction_rate()` | `contraction_rate` |

Sentence boundary regex is shared between `structural.py` and `validate.py` / `stylometry.py` — keep aligned. **Recommendation:** validator imports burstiness + flat count helpers from stylometry after paragraph API lands.

### 2.6 `soul.py` — explicit non-scope

Contraction injection is Phase 5. SYNTH-92 only requires:

- Pre/post `contraction_rate` in `HumanizeReport.stylometry`  
- Optional soul rate-cap hook (future): if post-Phase-1–2 profile already above baseline p75, skip soul copula pass — defer to separate ticket

---

## 3. Target architecture — measure → edit → re-measure

### 3.1 New: `StylometryContext` (humanize layer)

Add to `humanize.py` (or thin `stylometry_context.py`):

```python
@dataclass
class StylometryContext:
    before: StyleProfile
    after: StyleProfile | None = None
    paragraph_stats: list[ParagraphStyleStats]  # new
    gaps: list[TargetGap]                       # from lexical_targets
    mode: Literal["default", "voice_match", "anti_detector"]

    def delta(self) -> StyleDelta: ...
    def flat_paragraph_indices(self) -> list[int]: ...
```

**Lifecycle in `humanize_deterministic_with_report`:**

1. **Pre-measure** on `_restore(protected, table)` prose (after `_protect`, before edits) — or on original text before protect if placeholders skew counts; **test both**, prefer unprotected original for measurement, protected for paragraph boundaries  
2. Build `gaps = measure_gaps(...)` when intensity ∈ (`full`, `anti-detector`)  
3. Pass `ctx` into Phase 1 structural (new optional arg)  
4. Run Phase 2 lexical + `apply_targeted_pass(gaps)`  
5. **Post-measure** on final unprotected output  
6. Attach to `HumanizeReport` + CLI `--report` / `--json`

### 3.2 New: paragraph-level API in `stylometry.py`

```python
@dataclass
class ParagraphStyleStats:
    index: int
    sentences: int
    sigma: float
    cv: float
    is_flat: bool          # sigma < threshold
    is_pure_list: bool

def analyze_paragraphs(text: str, *, flat_sigma: float = 3.0) -> list[ParagraphStyleStats]: ...
```

Implement by reusing `_strip_non_prose`, `_sentences`, word counts — **single implementation** consumed by:

- `structural.split_long_sentences` (replace `_paragraph_sigma`)  
- `validate._count_flat_paragraphs`  
- `StylometryContext.flat_paragraph_indices()`

Threshold note: structural uses 5.0 for edit trigger; validator uses 3.0 for flat warning — **keep both**, document as "edit threshold" vs "report threshold".

### 3.3 Phase 1: stylometry-guided structural pass

**New signature:**

```python
def humanize_structural(
    text: str,
    *,
    report: StructuralReport | None = None,
    targets: StructuralTargets | None = None,
) -> str: ...


@dataclass
class StructuralTargets:
    target_sigma: float = 5.0
    min_words: int = 30
    flat_min_words: int = 20
    min_half: int = 8
    flat_paragraph_indices: frozenset[int] | None = None  # if None, scan all
    prioritize_cv: bool = False  # anti-detector: also flag low CV paragraphs
```

**Target resolution (`resolve_structural_targets(ctx)`)**:

| Mode | `target_sigma` | `flat_min_words` | Notes |
|------|----------------|------------------|-------|
| `voice_match` + sample | `max(sample_σ * 0.9, 3.0)` | scale with sample mean length | Fidelity — do not force σ≥6 |
| `anti_detector` | `6.0` | `18` | Aggressive flat catch; still split-only |
| `default` / `balanced` | `5.0` | `20` | Current behavior |
| Baseline gap: σ below p25 | `5.5` | `20` | Nudge from measured gap |

**Optional second structural iteration** (bounded, max 1):

- If post-pass document σ still below target and `report.sentences_split > 0` in first pass, lower `min_words` by 2 for flat paragraphs only  
- Never loop unbounded — preservation tests forbid cascade splits

**Deadlock handling (report-only in Phase 1):**

- If flat paragraph has no splittable boundary, add warning to `StructuralReport.deadlocks: list[int]`  
- Feed deadlock list into LLM anti-detector prompt (P4 from AGENT-54) — not Phase 1 auto-fix

**Do not add in Phase 1:** fragment injection, adjacent-short merge, gamma/CV fit (BurstInjector) — high false-positive / meaning drift risk vs `TestPreservation`.

### 3.4 Phase 2: stylometry-guided lexical pass

**Ship baseline file** — run existing `benchmarks/stylometric_baseline.py` on human fixtures; commit `benchmarks/results/stylometric_baseline.json` with fields at minimum:

- `sentence_length_stdev`, `sentence_length_cv`, `fragment_rate`  
- `latinate_ratio`, `type_token_ratio`, `function_word_rate`  
- `contraction_rate`, `em_dash_rate` (report-only thresholds)

**Extend `apply_targeted_pass` (safe edits only):**

| Gap field | Direction | Action | Already shipped? |
|-----------|-----------|--------|------------------|
| `latinate_ratio` | high | `_replace_latinate()` | ✅ (also runs unconditionally at balanced+) |
| `function_word_rate` | low | `_inject_function_words()` | ✅ full/anti-detector |
| `type_token_ratio` | high | `_dampen_synonym_cycling()` | ✅ full/anti-detector |
| `latinate_ratio` | low | **no-op** | Voice-match may want Latinate — skip |
| `sentence_length_*` | any | **delegate to Phase 1** | Do not lexical-fix burstiness |
| `contraction_rate` | low | **delegate to Phase 5 soul** | Report in gaps only |

**Fix unconditional Latinate pass:** Today `apply_targeted_pass` runs `_replace_latinate` whenever intensity is balanced+, even with no gap. Change to gap-gated at `balanced`; keep unconditional at `full`/`anti-detector` if product wants stronger register shift.

**Phase 2 regex families (existing):** significance inflation, copula avoidance, etc. — no stylometry loop needed; they are subtractive. Optional: log whether copula avoidance **lowers** `latinate_ratio` / **raises** `sentence_length_mean` in report for ablation.

### 3.5 Voice-match vs anti-detector merge policy (Phase 1–2)

When `voice_sample` or persisted profile present **and** intensity is `anti-detector`:

```
structural_targets.sigma_target = max(sample.sentence_length_stdev, 6.0)
lexical_targets: preserve latinate_ratio ± ε, first_person_rate ± ε from sample
report: flag when anti-detector floor exceeds sample ("burstier than your voice")
```

Document in `SKILL.md` — AGENT-52 P1 recommendation; code enforcement in `resolve_structural_targets`.

---

## 4. Implementation plan (ordered)

### Sprint A — Measurement foundation (3–4 days)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| A1 | Add `analyze_paragraphs()` + `ParagraphStyleStats` | `stylometry.py` | Tests: flat vs varied paragraphs; pure-list skip |
| A2 | Add `StylometryContext` + pre/post in `humanize_deterministic_with_report` | `humanize.py` | `--report` JSON includes before/after profiles |
| A3 | Refactor `structural._paragraph_sigma` to call stylometry paragraph helper | `structural.py` | Existing `test_structural.py` green |
| A4 | Run + commit `stylometric_baseline.json` | `benchmarks/` | `test_stylometric_baseline.py` green; `measure_gaps()` non-empty on AI fixtures |

### Sprint B — Phase 1 closed loop (4–5 days)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| B1 | `StructuralTargets` + `resolve_structural_targets(ctx)` | `structural.py`, `humanize.py` | Voice vs anti-detector targets differ in unit tests |
| B2 | Pass flat paragraph indices from ctx to split pass | `structural.py` | Flat para edited; varied para skipped |
| B3 | Extend `StructuralReport`: `sigma_before/after`, `cv_before/after`, `deadlocks` | `structural.py` | CLI report shows Δσ |
| B4 | Optional single retry when Δσ < 0.5 after first pass | `structural.py` | Bounded; no preservation regressions |
| B5 | Wire validator flat count to stylometry helper | `validate.py` | One SSOT for flat paragraphs |

### Sprint C — Phase 2 closed loop (3–4 days)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| C1 | Gap-gate Latinate pass at `balanced` | `lexical_targets.py` | Subtle/balanced without gap skips Latinate swap |
| C2 | Include structural-only gaps in report when intensity < full | `humanize.py` | User sees "σ below baseline" even at balanced |
| C3 | `--report-stylometric-gaps` uses post-Phase-1–2 profile | `cli.py` | Already partial; verify after ctx lands |
| C4 | Tests: AI fixture → Phase 1–2 → σ/CV/latinate move toward baseline bands | `tests/unslop/` | Deterministic; no LLM |

### Sprint D — Benchmark + docs (2–3 days)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| D1 | Benchmark row: structural-only vs Phase 1+2 vs +soul | `benchmarks/run.py` | Real numbers in JSON; README only after run |
| D2 | Document deadlock + split-only asymmetry | `structural.py` docstring, `SKILL.md` | AGENT-54 P2 |
| D3 | Fix Paneru citation (replace Kalemaj) in SKILL mirrors | `skills/unslop/SKILL.md` | AGENT-41 |
| D4 | Reconcile contraction baselines in validator message | `validate.py` | Cite Paneru + note regex/units |

---

## 5. Test plan

### 5.1 Unit

- `test_stylometry.py`: paragraph API, CV edge cases (single sentence, empty)  
- `test_structural.py`: targets override `target_sigma`; flat index scoping; deadlock report  
- `test_lexical_targets.py`: gaps with real baseline file; gap-gated Latinate  
- `test_humanize.py`: `HumanizeReport.stylometry` populated; voice vs anti-detector target resolution

### 5.2 Preservation contract

All new edits run inside existing `_protect()` flow. **No new regex on prose without `_protect`**. Run full `TestPreservation` after every Sprint B/C change.

### 5.3 Ablation metrics (benchmarks)

For each fixture in `benchmarks/samples/`:

| Metric | Source |
|--------|--------|
| `sentence_length_stdev`, `sentence_length_cv` | stylometry |
| Flat paragraph count | `analyze_paragraphs` |
| `latinate_ratio`, `type_token_ratio` | stylometry |
| `contraction_rate` | stylometry (report only for Phase 1–2 ablation) |
| TMR `p_ai` | optional `detector_bench.py` — expect small delta Phase 1–2 only |

Publish only measured deltas — no invented benchmark numbers in README.

---

## 6. Explicit non-goals (Phase 1–2)

| Item | Why deferred | Owner phase |
|------|--------------|-------------|
| Contraction injection | soul.py; overshoot risk | Phase 5 |
| Short-sentence / fragment injection | Meaning fabrication risk | LLM anti-detector |
| Gamma/CV-fit reshaping (BurstInjector) | Preservation / drift | Future opt-in |
| Biber 67-feature register | spaCy dependency | Optional audit |
| DivEye LM surprisal loop | surprisal.py measure-only | SYNTH-83 / detector loop |
| Authorship embedding distance | TinyStyler-class | Out of scope |
| Second structural pass on varied paragraphs | Choppiness | Blocked by design |

---

## 7. Risk register

| Risk | Mitigation |
|------|------------|
| Placeholder tokens skew word counts | Measure on restored prose; structural on protected text |
| Voice-match preserves flat ESL σ | Mode flag; document conflict; optional `--voice-floor-σ` (AGENT-52) |
| Latinate swap changes σ | Re-measure post Phase 2; acceptable side effect |
| Baseline file stale / genre-wrong | Version field in JSON; genre tags in future |
| Split retry over-chops | Max 1 retry; min_half=8; TestPreservation |
| Duplicate logic drift | Paragraph σ only in stylometry.py |

---

## 8. Success criteria

Phase 1–2 stylometry integration is **done** when:

1. Every `humanize_deterministic_with_report` run with `structural=True` records before/after `StyleProfile` and Δσ, ΔCV, flat paragraph count  
2. `lexical_targets` runs with committed baseline and gap-gated edits at `balanced`  
3. Anti-detector uses higher structural targets than voice-match on the same input  
4. Ablation shows σ/CV increase on flat AI fixtures without preservation test failures  
5. No new Kalemaj citations; Paneru (2026) for contraction baseline docs  
6. README benchmark numbers updated only from real `benchmarks/run.py` output

---

## 9. One-paragraph distillation

unslop's Phase 1 (`structural.py`) and Phase 2 (`lexical_targets.py` + lexical regex) already implement the right *classes* of fix — sentence-length splitting and register-level lexical nudges — but they operate on **static thresholds** while `stylometry.py` measures **19 fields** that go mostly unused until the LLM voice-match prompt. The research memos (Paneru on contractions, Desaire/AGENT-54 on σ, AGENT-52 on voice-vs-detector conflict) all point to the same architecture: **extract profile, apply deterministic edits toward gap-closure, re-measure, report delta**. Phase 1–2 integration means paragraph-level σ/CV feeding structural targets, shipping the missing baseline JSON for lexical gaps, unifying flat-paragraph detection under stylometry, and mode-aware targets for voice-match vs anti-detector — while leaving contractions and fragments to Phase 5 soul and LLM anti-detector respectively. Split-only structural restoration stays conservative; the product honesty is that Phase 1–2 lifts rhythm and register but does not, alone, move RAID-grade detectors.

---

## 10. Primary references

| Memo / code | Path |
|-------------|------|
| Contraction stylometry | `AGENT-41-PANERU-CONTRACTION-STYLOMETRY.md` |
| Voice-match limits | `AGENT-52-VOICE-MATCH-STYLOMETRIC-LIMITS.md` |
| Sentence-length variance | `AGENT-54-SENTENCE-LENGTH-VARIANCE.md` |
| Biber register | `AGENT-42-RALLAPALLI-BIBER.md` |
| Code gap synthesis | `SYNTH-83-DETECTION-CODE-GAP.md` |
| Paneru (2026) | https://arxiv.org/abs/2604.11687 |
| Desaire et al. (2023) | https://doi.org/10.48550/arxiv.2303.16352 |
| Liang ESL bias (2023) | https://arxiv.org/abs/2304.02819 |
| Adversarial Paraphrasing | https://arxiv.org/abs/2506.07001 |
