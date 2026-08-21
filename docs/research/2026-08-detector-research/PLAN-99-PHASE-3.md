# PLAN-99 — Phase 3: LLM Pipeline, Cross-Model Orchestration, TempParaphraser Selection, Voice PEFT Research

**Master Integration Agent #99**  
**Date:** 2026-08-19  
**Scope:** Phase 3 implementation plan — `llm_pipeline.py`, multi-stage orchestration, cross-model routing, TempParaphraser-style candidate selection, voice PEFT research track  
**Inputs:** All 16 SYNTH memos (#81–#96), `UPDATE-PLAN-2026-08.md`, `AGENT-47-PROFILE-TO-PEFT.md`, codebase anchors (`humanize.py`, `detector.py`, `stylometry.py`, `style_memory.py`, `surprisal.py`, `validate.py`)  
**Audience:** unslop maintainers — implementation sprints, CLI surface, benchmark matrix, Boundaries  
**Timeline:** 6–8 weeks (after Phase 1 prerequisites; Phase 2 dynamics optional but recommended for multi-objective stop)

---

## Executive summary

Phase 3 closes the **distribution-layer gap**. Deterministic Phases 1–2 (lexical, structural, soul, stylometry-guided targets) and Phase 2 surprisal dynamics (TSD, SurpMark, cone proxy) address Signals 1–5 at the regex/measurement layer. Single-call `humanize_llm()` is the weakest link: one pass, one provider, no N-sample selection, no cross-model swap, no detector-guided span repair.

**Phase 3 ships `llm_pipeline.py`:** a gated orchestrator composing five research-backed stages behind `--intensity anti-detector --llm-pipeline {fast|balanced|max}`.

| Stage | Research analog | Mechanism | Balanced cost (~1K words) |
|-------|-----------------|-----------|---------------------------|
| **S1** | MASH Stages 2–4 | Draft → critique → fix → optional PPL-gated polish | 3–4 calls |
| **S2** | HIP | Cross-model iterative plain paraphrase | 1–2 rounds |
| **S3** | TempParaphraser | Hot-sentence N-candidate + detector argmin | 2 batched |
| **S4** | Adversarial Paraphrasing | Detector-guided span rewrite (document analog) | 3 calls |
| **S5** | Cross-model capstone (Agent #35) | Final pass via different provider than S2 | 1 call |

**Parallel research track (not in default wheel):** voice PEFT — StyleTunedLM-style per-user LoRA and P2P hypernetwork path for `/unslop voice-match` Tier 4 parametric voice. Orthogonal to anti-detector pipeline; gated on Catch Me AV eval (SYNTH-90).

**Honest targets (SYNTH-81, #83, #85, #88):**

- ≥5 pp TMR improvement vs legacy `humanize_llm()` on ≥3 fixtures
- Semantic preservation ≥0.92 (embedding or judge)
- `TestPreservation` 100% pass
- Balanced preset ≤$0.35/1K words at Aug 2026 API pricing
- **Not** MASH 92% ASR, TempParaphraser 82.5 pp accuracy drop, or StealthRL 97.6% ASR

**Boundaries unchanged (SYNTH-87, #94, #95):** ESL false-positive defense, resume polish, voice-match — not academic misconduct. No score-targeting schedulers (RateAudit). No watermark strip modes. Gate full pipeline behind explicit anti-detector intent.

---

## 1. Why Phase 3 exists — synthesis from 16 SYNTH memos

### 1.1 The five-signal stack (SYNTH-81, #83, #89)

2026 detectors fuse largely independent signals. unslop must address all five for anti-detector mode to be honest:

```
Signal 1: Lexical AI-isms          → humanize.py           ✅ strong
Signal 2: Burstiness (σ/CV)        → structural.py         ⚠️ split-only
Signal 3: Surprisal variance       → surprisal.py          ⚠️ measure only → Phase 2 closes loop
Signal 4: Late-stage stability     → TSD                   ❌ Phase 2
Signal 5: Predictability cones     → GPTZero v6 analog     ❌ Phase 2
Cross:  Transition recovery        → SurpMark              ❌ Phase 2
```

**Cross-cutting insight (SYNTH-81, #89):** Vocabulary humanization is solved and largely irrelevant against 2026 commercial detectors. Temporal surprisal dynamics and structural entropy are the frontier. Cross-model paraphrase remains the strongest documented lever when the deterministic ladder exhausts (Sadasivan TV framework; HIP; Agent #35).

### 1.2 The single-pass gap (SYNTH-86, #85)

| Component today | Gap |
|-----------------|-----|
| `humanize_llm()` | 1 pass + optional audit; no iteration, cross-model, or N-sample pick |
| `feedback_loop()` | Deterministic-only; re-humanizes **original** text; never reaches `anti-detector`; no LLM inside loop |
| `detector.py:390–392` | Comment incorrectly implies TempParaphraser needs "no LLM call" — fix in Phase 3 P0 |

Empirical constraint: deterministic passes drop AI-isms 88–92% but move TMR **~0.0–0.2 pp** on fixtures (SYNTH-83, #84, #88).

### 1.3 Two-axis doctrine (SYNTH-90, #91, #96)

| Axis | Mode | Optimizes | Pipeline routing |
|------|------|-----------|------------------|
| **Style fidelity** | `voice-match` | Stylometric delta vs reference | S1a + S1c with profile; **skip S2–S5** |
| **Statistical naturalness** | `anti-detector` | DivEye σ, TSD, burstiness, TMR | Full S1–S5 pipeline |
| **Slop removal** | `balanced`/`full` | Lexical + light rhythm | No pipeline |

Jemama: 99.9% style-matching coexists with perplexity 15.2 vs human 29.5. Merging modes requires explicit precedence (SYNTH-90 §5.3): `--voice-floor-σ`, register anchors when both flags set.

### 1.4 User segments (SYNTH-96)

| Segment | Phase 3 relevance |
|---------|-------------------|
| **ESL / L2** | Primary anti-detector warrant — cross-model + dynamics, not voice-match alone |
| **Resume / job seekers** | Sequenced voice-match → optional anti-detector; short-form harder for S3 hot-sentence pick |
| **Developers** | Default `balanced`; pipeline not default |
| **Students** | Intent gate; decline AI ghostwriting; pipeline only for own human drafts falsely flagged |

### 1.5 What we refuse (SYNTH-87, #94, #95)

| Refusal | Phase 3 implication |
|---------|----------------------|
| Score-targeting (RateAudit, γ-as-optimizer) | TMR is diagnostic stop, not optimization target |
| Watermark strip modes | No SynthID/KGW-aware prompts; document collateral side effect |
| Academic bypass marketing | No "beat Turnitin" copy; bench honestly on May detector-test panel |
| StealthRL/MASH weights in product | Cite as upper bound only |
| TempParaphraser 1B weight bundle | Algorithm port via API N-sample, not vendored weights (license) |

---

## 2. Prerequisites and dependencies

### 2.1 Phase 1 blockers (must ship before Phase 3 GA)

| # | Prerequisite | Source | Why Phase 3 needs it |
|---|--------------|--------|----------------------|
| P1 | `anti-detector` on feedback ladder | SYNTH-83, UPDATE-PLAN | S3/S4 assume ladder step 4 exists |
| P2 | `stylometric_baseline.json` committed | SYNTH-92 | S1d PPL-gate + dynamics human bands |
| P3 | `--detector-surprisal` wired to CLI feedback | SYNTH-83 | S1d refine + multi-objective stop |
| P4 | Fix `detector.py` TempParaphraser comment | SYNTH-86 §3.3 | Accurate docs for S3 |

### 2.2 Phase 2 soft dependencies (recommended)

| Capability | Module | Phase 3 use |
|------------|--------|-------------|
| `compute_tsd_reading()` | `surprisal.py` | Multi-objective stop; S3 hot-sentence scoring |
| `compute_surpmark_reading()` | `surprisal.py` | Stop policy; benchmark reporting |
| `compute_lexical_cone_reading()` | `surprisal.py` | GPTZero v6 proxy in S3 argmin |
| `dynamics_targets.py` | new | Pre-pipeline deterministic pass |
| `--dynamics-feedback` | `cli.py` | Combined stop with TMR |

Phase 3 can ship with TMR-only stop; dynamics multi-objective is P2 within Phase 3 if Phase 2 slips.

### 2.3 Existing code reuse

| Module | Phase 3 role |
|--------|--------------|
| `humanize.py` | S1 prompt templates; `_build_voice_block` for voice-match S1a |
| `validate.py` | Hard stop after every stage; preservation contract |
| `detector.py` | `score_ai_probability` for S3 argmin, S4 span loop; post-pipeline `feedback_loop` |
| `stylometry.py` | S1 voice conditioning; post-pipeline delta report |
| `style_memory.py` | Persisted profile for voice-match S1 |
| `surprisal.py` | S1d sentence ranking; S3 local surprisal for hot-sentence selection |
| `structural.py` / `soul.py` | Pre-pipeline deterministic pass (unchanged order) |

---

## 3. Architecture — `llm_pipeline.py`

### 3.1 End-to-end flow

```
Input text
  │
  ├─► validate.py eligibility (size, sensitivity)
  │
  ├─► [Pre-pipeline deterministic]
  │       humanize → structural → soul
  │       optional: dynamics_targets (Phase 2)
  │       optional: lexical_targets at anti-detector
  │
  ├─► [Phase 3] llm_pipeline.run(config, intensity, voice_profile?)
  │       S1  MASH align + critique + fix [+ refine]
  │       S2  HIP cross-model iterative paraphrase (1–4 rounds)
  │       S3  TempParaphraser hot-sentence multi-sample argmin
  │       S4  AdvPara span loop (detector-guided)
  │       S5  cross-model capstone
  │       (short-circuit when should_stop() after any stage)
  │
  ├─► validate.py (preservation + AI_ISMS residual)
  │
  └─► [optional] detector.feedback_loop() on pipeline output
          multi-objective: TMR ≤ target AND dynamics in human band
```

**Gate:** `--intensity anti-detector --llm-pipeline {fast|balanced|max}`. Default off.

**Voice-match routing:** When `intensity == "voice-match"` and `--llm-pipeline` set (future `--voice-pipeline`), run **S1a + S1c only** with profile; skip S2–S5 unless user also sets anti-detector.

### 3.2 Stage dependency graph

```
S1 (style alignment) ──► S2 (distribution shift) ──► S3 (sentence entropy)
                              │                           │
                              └───────────┬───────────────┘
                                          ▼
                                    S4 (span repair)
                                          │
                                          ▼
                                    S5 (capstone swap)
```

Skip rules: if `should_stop(readings)` after any stage, short-circuit remaining stages; log `stages_run` and which stage succeeded.

### 3.3 Module API (sketch)

```python
# unslop/scripts/llm_pipeline.py

@dataclass
class PipelineConfig:
    preset: Literal["fast", "balanced", "max"]
    hip_rounds: int = 2
    hip_model: str | None = None          # UNSLOP_HIP_MODEL
    s3_n_candidates: int = 5
    s3_hot_fraction: float = 0.15
    s4_top_spans: int = 5
    s4_candidates_per_span: int = 3
    enable_s1d_refine: bool = False
    capstone_model: str | None = None
    target_p_ai: float = 0.5
    short_circuit: bool = True
    voice_profile: StyleProfile | None = None
    enable_dynamics_stop: bool = False      # Phase 2 dep

@dataclass
class PipelineReport:
    stages_run: list[str]
    tmr_before: float
    tmr_after: float
    dynamics_before: dict[str, float] | None
    dynamics_after: dict[str, float] | None
    semantic_score: float | None
    stylometry_delta: dict[str, float] | None
    llm_calls: int
    estimated_cost_usd: float
    short_circuited_at: str | None
    preservation_ok: bool

def run_pipeline(
    text: str,
    *,
    config: PipelineConfig,
    intensity: Intensity = "anti-detector",
    score_fn: Callable[[str], float] | None = None,
    llm_call_fn: Callable[..., str] | None = None,
) -> tuple[str, PipelineReport]: ...
```

### 3.4 LLM provider abstraction

Extend `humanize.py` provider layer (currently Anthropic SDK + `claude` CLI only):

```python
# unslop/scripts/llm_providers.py (new, Phase 3)

ProviderRole = Literal["author", "hip_rewriter", "candidate_gen", "capstone"]

def resolve_provider(role: ProviderRole, *, exclude: set[str] | None = None) -> Provider:
    """Env-driven: UNSLOP_HIP_MODEL, UNSLOP_CAPSTONE_MODEL, default author."""
    ...

def call_llm(prompt: str, *, provider: Provider, temperature: float = 0.7) -> str: ...
```

**Family rotation rule (SYNTH-86 §5.1):** S2 provider ≠ S1 author family; S5 provider ≠ S2 family. Boundaries: OpenAI ↔ Anthropic ↔ Google ↔ Meta.

---

## 4. Stage specifications

### 4.1 S1 — MASH-style align + refine (SYNTH-85 L3, SYNTH-86 §3.1)

**Research:** Style-SFT → DPO → PPL-gated sentence polish (Gu et al., ACL Findings 2026, 92% avg ASR on 5 detectors). **unslop maps prompt chain only — no fine-tune.**

| Sub-stage | Calls | Prompt intent |
|-----------|-------|---------------|
| **S1a Draft** | 1 | Natural human register; unslop anti-slop rules; inject `StyleProfile` if voice-match |
| **S1b Critique** | 1 | Diagnose machine tells as detector would: uniform rhythm, hedging, safe parallelism, low-entropy phrasing — cite spans |
| **S1c Fix** | 1 | Revise flagged spans only; strict preservation contract |
| **S1d Refine** (optional, max preset) | 0–K | Sort sentences by proxy PPL/surprisal; polish top-K flat sentences; accept only if TMR holds or improves |

**Voice conditioning:** Map `stylometry.py` + `style_memory.py` into S1a system block — partial MASH style embedding analog.

**Preserve vs inject (SYNTH-91):** S1 must **preserve** stance, disagreement, specifics; **inject** burstiness and de-homogenization only where critique flags machine uniformity — never sycophancy or stance softening.

**Do not ship:** Style-SFT, DPO training, BART 0.1B local rewriter.

### 4.2 S2 — HIP iterative cross-model paraphrase (SYNTH-86 §3.2)

**Research:** Minimal LoRA on base model + N=10 document iterations; GPTZero 0%→100% human prob by round 10 (Xu et al., arXiv:2605.19516).

**API approximation:**

1. Cross-provider rewriter — if source was Claude, S2 uses GPT/Gemini (`UNSLOP_HIP_MODEL`).
2. Plain HIP format — no chat persona:

   ```
   <source_text>
   {current draft}
   </source_text>
   <target_text>
   {rewrite as natural human prose; preserve meaning}
   </target_text>
   ```

3. Rounds: 1–4 (not 10); env `UNSLOP_HIP_ROUNDS`; balanced default 2.
4. Stop per round: `validate.py` pass; optional TMR ≤ target; semantic ≥0.92 vs round input.

**Base-model proxy without local weights:** Plain continuation prompts over assistant persona; lower temperature on S1 (0.7); document per provider — benchmark empirically, no HIP-equivalence claim.

**Do not ship:** In-plugin LoRA training; OpenAI fine-tune path (HIP Appendix A.2 negative result).

### 4.3 S3 — TempParaphraser multi-sample selection (SYNTH-86 §3.3, SYNTH-88 §1.3)

**Research:** N=7 sentence paraphrases at T=1.2; pick lowest detector score; 82.5 pp avg accuracy drop on HC3 four-detector panel (Huang et al., EMNLP 2025).

**Algorithm port (no 1B fine-tune):**

```python
def select_hot_sentences(doc: str, k_fraction: float, score_fn, surprisal_fn) -> list[SentenceSpan]:
    """Top-k by TMR_chunk_score + local_surprisal."""
    n = count_sentences(doc)
    k = max(1, ceil(k_fraction * n))
    ...

def temp_paraphraser_stage(doc: str, config: PipelineConfig, ...) -> str:
    hot = select_hot_sentences(doc, config.s3_hot_fraction, ...)
    for sent in hot:
        candidates = llm.paraphrase(sent, n=config.s3_n_candidates, temperature=1.2)
        scores = [score_fn(merge(doc, c)) for c in candidates]
        pick = argmin(scores) subject to validate.preserve(sent, pick)
        doc = merge(doc, pick)
    return doc
```

| Parameter | fast | balanced | max |
|-----------|------|----------|-----|
| N candidates | 3 | 5 | 7 |
| Hot sentence fraction | 10% | 15% | 25% |
| Batched calls | 1 | 2 | 3 |

**Multi-objective argmin (Phase 2+):** When dynamics available, score = weighted `{tmr, -surprisal_stdev, -tsd_dd, -surpmark_dgjs}` with TMR primary — not pure TMR minimization (RateAudit forbidden).

**Honest floor:** RADAR still 45.4% post-attack in paper — paraphrase-hardened detectors partially resist.

**Fix P0:** Update `detector.py:390–392` to distinguish paper (fine-tuned paraphraser + N× inference) vs unslop recommendation (API N-sample argmin).

### 4.4 S4 — Adversarial span loop (SYNTH-86 §3.4)

**Research:** Token-level detector argmin; −87.88% avg TPR across 8 detectors (Cheng et al., NeurIPS 2025). Simple paraphrase *increases* TPR on RADAR/Fast-DetectGPT — S4 runs **after** S2/S3.

**Document-level analog (no logit access):**

1. Score document; segment into sentences or ≤512-token chunks.
2. Rank spans by local `p_ai`; take top-K (default 5).
3. For each span: LLM generates M=3 paraphrase candidates; pick min TMR on merged doc.
4. Re-validate preservation; reject span if code/URL/heading mutation.

**External bridge (opt-in P3):** `--adv-paraphrase /path/to/repo` subprocesses after S1–S3 fail — ethics gate. Do not bundle 8B CUDA into pip wheel.

### 4.5 S5 — Cross-model capstone (SYNTH-86 §3.5, SYNTH-88 §1.2)

**Research:** Practitioner GPT→Claude→Gemini chains; operational form of TempParaphraser + blind AdvPara.

**Mapping:**

- Single full-document rewrite via provider **≠ S2 provider** and **≠ original generator family** (if known from env).
- Prompt: structural preservation + anti-slop rules + "do not summarize."
- Automates manual recommendation already in `detector.py` ladder exhaustion message.

---

## 5. Cross-model orchestration

### 5.1 Provider matrix (SYNTH-86 §5, SYNTH-88 §1.2)

| Role | Selection rule | Rationale |
|------|----------------|-----------|
| **S1 author pass** | User's configured default (Anthropic SDK / CLI) | Voice-match continuity |
| **S2 HIP rewriter** | `UNSLOP_HIP_MODEL` ≠ default provider | Instruction-tuning fingerprint swap |
| **S3 candidate generator** | Same as S2 or third family | Entropy diversity |
| **S5 capstone** | Third provider if available; else alternate | Practitioner 2–3 hop chain |

### 5.2 Environment surface

```bash
UNSLOP_LLM_PIPELINE=balanced       # fast | balanced | max
UNSLOP_HIP_ROUNDS=2
UNSLOP_HIP_MODEL=openai/gpt-4o     # example; requires provider SDK/key
UNSLOP_CAPSTONE_MODEL=google/gemini-2.0-flash
UNSLOP_S3_N_CANDIDATES=5
UNSLOP_S4_TOP_SPANS=5
UNSLOP_PIPELINE_SHORT_CIRCUIT=1
UNSLOP_ORIGINAL_PROVIDER=anthropic # optional; for family rotation
```

### 5.3 Sequenced workflows (SYNTH-90 §5.2, SYNTH-96)

**ESL defense (primary warrant):**

1. Deterministic `anti-detector` + dynamics targets
2. `--llm-pipeline balanced` (full S1–S5)
3. `--detector-feedback --dynamics-feedback`
4. Re-score on target detector(s) — dual reporting; one green ≠ universal pass (SYNTH-82)

**Voice + detector (merged, documented second pass):**

1. `voice-match` rewrite (S1a+S1c or deterministic + LLM voice)
2. User opts anti-detector with register anchors: `σ ≥ max(sample_σ, 6)`, contractions ≥ max(sample, human floor), Latinate ±ε
3. `--llm-pipeline fast` (S1+S2 only) — skip aggressive S3–S5 unless still flagged

**Developer default:** No pipeline. `balanced` deterministic only.

---

## 6. Detector-in-loop design

### 6.1 Scorers (SYNTH-86 §4, SYNTH-84)

| Scorer | Source | Role |
|--------|--------|------|
| **TMR / Desklib** | `detector.py` | Primary stop: `p_ai ≤ target` (default 0.5) |
| **DivEye σ, Δ, Δ²** | `surprisal.py` | Secondary: human band p25–p75 |
| **TSD second-half DD/LV** | Phase 2 | Anti "AI settles down" |
| **SurpMark ΔGJS** | Phase 2 | Anti recovery-pattern |
| **Cone-width proxy** | Phase 2 | GPTZero v6 analog |
| **Burstiness σ** | `stylometry.py` | Structural sanity |

**Stop policy:**

```python
def should_stop(readings: PipelineReadings, target_p_ai: float = 0.5) -> bool:
    return (
        readings.tmr <= target_p_ai
        and (not readings.dynamics_required or readings.dynamics_in_human_band())
        and readings.ai_isms == 0
    )
```

### 6.2 What the loop must NOT do (SYNTH-87, SYNTH-85)

| Anti-pattern | Why forbidden |
|--------------|---------------|
| RateAudit-style chunk scheduler targeting document-level % AI | Gameable |
| γ-as-hard-optimizer sweeping perturbation until score hits floor | StyleShield destroys honesty |
| Watermark-targeted guidance | EU AI Act Art. 50 |
| Score-targeting intensity tiers | Map preset to rewrite depth, not TMR setpoints |

### 6.3 Feedback loop integration (SYNTH-83, SYNTH-86 §4.3)

**Changes to `detector.feedback_loop()`:**

1. Accept optional `llm_pipeline_fn` — run pipeline **before** ladder when `--llm-pipeline` set.
2. Operate on **pipeline output**, not original — cumulative refinement.
3. Add `anti-detector` as ladder step 4 (Phase 1).
4. Log `PipelineReport` in `FeedbackResult` extension or sibling field.

---

## 7. Voice PEFT research track (parallel to anti-detector pipeline)

**Scope:** Phase 3 **research** and optional power-user path — **not** default pip wheel feature. Sources: SYNTH-90, AGENT-47, AGENT-43, AGENT-48.

### 7.1 Why prompt voice-match hits a ceiling

| Evidence | Number | Implication |
|----------|--------|-------------|
| Catch Me Blog AV (5-shot LLM) | ~17–21% vs human 91.4% | Prompt-only fails informal idiolect |
| StyleTunedLM authorship classifier | 87.9% vs 69.3% 5-shot | PEFT beats prompting on authorship |
| P2P deployment | 0.57 s/user vs OPPU 20.44 s | Hypernetwork scales personalization |
| Jemama style vs perplexity | 99.9% match vs μ PPL 15.2 vs 29.5 | Voice ≠ detector escape |

unslop ships **T1 micro prompt-match** today. Phase 3 research targets **T4 parametric match** gated on eval.

### 7.2 Three-tier voice fidelity model (SYNTH-90 §4.1)

| Tier | Mechanism | Phase 3 status |
|------|-----------|------------------|
| **T1** | `StyleProfile` → LLM targets | Shipped |
| **T2** | T1 + Biber fingerprint + RG register prompt | P1 eval + prompt (parallel Phase 3 docs) |
| **T3** | T2 + discourse move counters (ZeroStylus-inspired) | P2 research |
| **T4** | LoRA / P2P hypernetwork | **Phase 3 research spike** |

### 7.3 PEFT research roadmap (AGENT-47)

| Phase | Deliverable | Dependency | Ship in plugin? |
|-------|-------------|------------|-----------------|
| **3a — eval** | Catch Me `deploy_AV_models.py` wrapper on unslop output | Wang repo + Blog subset | Bench only |
| **3b — prototype** | Single-user StyleTunedLM-style qlora (local) | User consent, ~5k–10k words | Opt-in extra |
| **3c — hypernetwork spike** | NL summary + `StyleProfile` → LoRA via P2P fork eval | HF `Zhaoxuan/P2P_ckpt`, Personal Reddit | Research doc |
| **4 — product** | Infer-only weights OR "bring your own LoRA" | One base model documented | Future |

**Input modality (recommended hybrid):**

- NL summary from user samples (P2P ablation: summary dominates)
- Numeric `StyleProfile` side-channel for cues NL misses (contraction rate, σ, em-dash rate)
- Closed-schema rhetorical-move counters (ZeroStylus Tier 2 shortcut) — no free-text in memory

**Product boundaries:**

- Never auto-train on user data without explicit consent
- Ephemeral LoRA in memory; optional encrypted cache
- Anti-detector remains separate; no implied Turnitin evasion from voice LoRA
- Ship infer-only OR document external LoRA path — not bundled training in hooks

### 7.4 Voice PEFT vs llm_pipeline interaction

| Scenario | Behavior |
|----------|----------|
| `voice-match` only | S1a+S1c with profile; no PEFT required |
| `voice-match` + user LoRA (future) | Plug adapter before S1a; skip S2–S5 |
| `anti-detector` + voice profile | S1 weak voice conditioner; full S2–S5 for distribution |
| PEFT-trained voice + detector flag | **Sequenced:** LoRA rewrite → anti-detector with register anchors — not single merged objective |

**Eval oracle before product claims:** Catch Me AV harness + two-axis dashboard (style fidelity vs TMR/perplexity) per SYNTH-90 Phase C.

### 7.5 Research artifacts (Phase 3 deliverables)

| Artifact | Path | Purpose |
|----------|------|---------|
| Voice PEFT research memo | `docs/research/10-style-transfer-voice/PEFT-PHASE3.md` | StyleTunedLM/P2P/TinyStyler comparison |
| Bench wrapper | `benchmarks/voice_match_bench.py` | AV score + StyleProfile.delta |
| Spike script | `research/voice_peft/spike_qlora.py` | Opt-in; not in wheel |
| P2P eval notes | `research/voice_peft/p2p_infer_only.md` | Infer-only checkpoint eval protocol |

---

## 8. Budget presets and cost model

| Preset | Stages | Est. calls | Est. cost / 1K words |
|--------|--------|------------|------------------------|
| **fast** | S1 (3) + S2 (1 round) | ~4 | ~$0.10 |
| **balanced** | S1 + S2 (2) + S3 (2 batched) | ~7 | ~$0.30 |
| **max** | S1 + S1d + S2 (4) + S3 + S4 + S5 | ~12–15 | ~$0.70 |

**Semantic drift guard:** After each stage, run `validate.py`; on failure, revert stage output and log. Embedding similarity gate ≥0.92 vs pre-stage text (Jemama dual-axis).

**CLI:**

```bash
python3 -m unslop.scripts.cli humanize doc.md \
  --intensity anti-detector \
  --llm-pipeline balanced \
  --detector-feedback \
  --dynamics-feedback   # Phase 2 dep

python3 -m unslop.scripts.cli humanize doc.md \
  --intensity voice-match \
  --voice-sample my-emails.txt \
  --llm-pipeline fast   # S1 only; future flag
```

---

## 9. Methods explicitly out of scope

| Method | Headline | Why not in unslop v1 |
|--------|----------|----------------------|
| StealthRL | 97.6% ASR | GRPO+LoRA; quality tax |
| MASH Stages 1–3 | 92% ASR | Style-SFT + DPO + detector oracle training |
| StyleShield | ≥94.6% evade | 128×A800 embedding diffusion |
| GradEscape | 139M beats 11B DIPPER | White-box gradient optimization |
| AuthorMist / RL watermark attacks | High ASR | Training + ethics |
| DIPPER 11B local | Historical baseline | 40GB GPU |
| CoPA logit contrast | +57.72% fooling | Requires logit access |
| RateAudit scheduling | ≤1.4 pp to任意 target % | Anti-pattern |
| TempParaphraser 1B weights | EMNLP 2025 | License; API algorithm port instead |
| SaaS humanizer API wrappers | Undetectable.ai etc. | SYNTH-88 refuse |

**Optional external bridges:** AdvPara repo subprocess, HIP vLLM adapter, user LoRA — power-user flags with ethics gate.

---

## 10. Benchmark and acceptance criteria

### 10.1 Phase 3 exit criteria (SYNTH-84, SYNTH-86 §11)

| Criterion | Target |
|-----------|--------|
| TMR improvement vs `humanize_llm()` | ≥5 pp on ≥3 fixtures |
| Semantic preservation | ≥0.92 embedding or judge score |
| `TestPreservation` | 100% pass |
| Dynamics (when Phase 2 shipped) | 2nd-half DD rises on ≥7/9 fixtures |
| Cost envelope | balanced ≤$0.35/1K words |
| Docs | SKILL.md: pipeline stages, Boundaries, no ASR marketing |
| Bench | `detector_bench.py` adds `llm_pipeline_{fast,balanced,max}` variants |

### 10.2 Benchmark matrix (SYNTH-84)

**Three-axis reporting (TH-Bench frame):**

| Axis | Harness |
|------|---------|
| Slop removal | `benchmarks/run.py` |
| Detector signal | `detector_bench.py` + TPR@FPR=5% |
| Human quality | TH-Bench quality metrics (schema adopt) |

**Variants to add:**

- `humanize_llm` (baseline)
- `llm_pipeline_fast`
- `llm_pipeline_balanced`
- `llm_pipeline_max`
- `deterministic + llm_pipeline_balanced` (full stack)

**Dual reporting rule:** Consumer screenshot panel (May detector-test CSV when populated) + academic ensemble (TMR + DivEye + TSD when Phase 2 ships). Never cite single-detector "100% pass."

### 10.3 Voice PEFT research acceptance (not GA blocker)

| Criterion | Target |
|-----------|--------|
| AV bench wrapper runs | Green on mock; opt-in live |
| Blog AV movement measured | Report delta, not "pass" claim |
| qlora spike | Documented protocol; no plugin ship |
| SKILL.md citation fix | 23.5× → Jemama; Catch Me Blog AV caveat |

---

## 11. Implementation sprints (6–8 weeks)

### Sprint 0 — Prerequisites (Phase 1, parallel)

| ID | Task | Effort | Owner |
|----|------|--------|-------|
| 0.1 | `anti-detector` on feedback ladder | S | detector.py |
| 0.2 | Ship `stylometric_baseline.json` | S | benchmarks |
| 0.3 | Wire `--detector-surprisal` | S | cli.py |
| 0.4 | Fix TempParaphraser comment | S | detector.py |

### Sprint 1 — Skeleton + S1 + providers (week 1–2)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| 1.1 | `llm_pipeline.py` skeleton + `PipelineConfig`/`PipelineReport` | new | Imports; mock tests |
| 1.2 | `llm_providers.py` multi-provider abstraction | new | Anthropic + OpenAI stub |
| 1.3 | S1 MASH 3-call chain + prompts | llm_pipeline.py, prompts/ | Preservation pass |
| 1.4 | CLI `--llm-pipeline` flag (fast preset) | cli.py | End-to-end mock |
| 1.5 | Integrate pre-pipeline deterministic pass | humanize.py hook | Order unchanged |

### Sprint 2 — S2 HIP + cross-model (week 2–3)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| 2.1 | HIP plain template + round loop | llm_pipeline.py | 2-round mock |
| 2.2 | Provider rotation + env config | llm_providers.py | Family ≠ author |
| 2.3 | Semantic similarity gate | llm_pipeline.py | Revert on drift |
| 2.4 | `balanced` preset wiring | cli.py | 7-call budget cap |

### Sprint 3 — S3 TempParaphraser selection (week 3–4)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| 3.1 | Hot-sentence selection (TMR chunk + surprisal) | llm_pipeline.py | Unit tests |
| 3.2 | N-candidate batch paraphrase @ T=1.2 | llm_pipeline.py | Argmin picks lower TMR |
| 3.3 | Batched call optimization | llm_pipeline.py | ≤2 batched balanced |
| 3.4 | Short-circuit on `should_stop()` | llm_pipeline.py | Log stage |

### Sprint 4 — S4/S5 + feedback integration (week 4–5)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| 4.1 | S4 span loop | llm_pipeline.py | Top-5 spans |
| 4.2 | S5 capstone | llm_pipeline.py | Third provider |
| 4.3 | `max` preset | cli.py | Full stage list |
| 4.4 | Post-pipeline `feedback_loop` on output | detector.py, cli.py | Cumulative |
| 4.5 | S1d PPL-gated refine (max only) | llm_pipeline.py | surprisal dep |

### Sprint 5 — Benchmark + docs + voice PEFT research (week 5–7)

| ID | Task | Files | Acceptance |
|----|------|-------|------------|
| 5.1 | `detector_bench.py` pipeline variants | benchmarks/ | JSON output |
| 5.2 | SKILL.md Phase 3 section + Boundaries | skills/unslop/SKILL.md | Sync mirrors |
| 5.3 | `benchmarks/voice_match_bench.py` AV wrapper | benchmarks/ | Opt-in live |
| 5.4 | Voice PEFT research memo | docs/research/ | StyleTunedLM/P2P |
| 5.5 | `research/voice_peft/spike_qlora.py` | research/ | Not in wheel |
| 5.6 | May detector-test panel eval (manual) | drafts/2026-05-detector-test/ | CSV when ready |

### Sprint 6 — Hardening (week 7–8)

| ID | Task | Acceptance |
|----|------|------------|
| 6.1 | Live LLM tests opt-in `UNSLOP_RUN_LLM_TESTS=1` | CI optional job |
| 6.2 | Cost telemetry in `PipelineReport` | Per-run USD estimate |
| 6.3 | Multi-objective stop (Phase 2 dep) | TMR + dynamics band |
| 6.4 | `--adv-paraphrase` external bridge stub | Ethics gate only |
| 6.5 | README benchmark numbers from real runs only | No invented stats |

---

## 12. Risk register

| Risk | Mitigation | SYNTH source |
|------|------------|--------------|
| Semantic drift across S2 rounds | Per-round validate + embedding gate | Jemama #50 |
| Multi-provider key management | Env-only; refuse if missing; clear errors | — |
| Cost overrun on long docs | Word-budget cap; stage skip on short-circuit | SYNTH-86 |
| Voice-match + anti-detector conflict | Register anchors; `--voice-floor-σ` | SYNTH-90, #52 |
| Score-gaming accusation | Diagnostic stop only; no RateAudit | SYNTH-87 |
| Commercial bench stale | May detector-test panel; date-stamp results | SYNTH-82, #93 |
| PEFT scope creep | Research track separate from GA pipeline | SYNTH-90 |
| Preservation regression | Full `TestPreservation` every sprint | CLAUDE.md |
| Phase 2 slip | TMR-only stop for v1; dynamics additive | SYNTH-83 |

---

## 13. Documentation and claims matrix

### 13.1 Allowed claims (SYNTH-90 §8, SYNTH-93)

| Claim | Wording |
|-------|---------|
| Multi-stage LLM pipeline for anti-detector | Gated; ESL/resume defense framing |
| Cross-model paraphrase automation | "Strongest documented lever"; not guaranteed pass |
| TempParaphraser-style sentence selection | "Detector-guided pick among candidates" |
| ≥5 pp TMR improvement target | On fixtures; not commercial panel |
| Voice PEFT research | "Evaluating StyleTunedLM/P2P path"; not shipped |

### 13.2 Forbidden claims

| Claim | Why |
|-------|-----|
| "Beat Turnitin / 100% undetectable" | SYNTH-87, #66 |
| MASH/TempParaphraser paper ASR as product guarantee | DAMAGE 20–100 pp gap |
| "Voice LoRA passes detectors" | Jemama orthogonality |
| Watermark-safe humanization | SYNTH-95 |
| "Cheaper Undetectable.ai" | SYNTH-88, #93 |

---

## 14. SYNTH cross-reference index

| SYNTH | Phase 3 contribution |
|-------|---------------------|
| **81** Academic detection | Five-signal stack; cross-model lever; TMR default |
| **82** Commercial detection | Dual reporting; no Turnitin bypass marketing |
| **83** Code gap | Prerequisites; feedback loop semantics |
| **84** Benchmarks | TPR@FPR; three-axis eval; pipeline variants |
| **85** Evasion prompt | L0–L6 layer map; stop rules |
| **86** LLM pipeline | Primary stage spec (S1–S5) |
| **87** Refusals | Score-targeting + watermark hard lines |
| **88** Practitioner tools | Cross-model workflow; SaaS refuse |
| **89** Stylometry signals | S3 hot-sentence signals; two-axis |
| **90** Voice-match strategy | PEFT research track; mode routing |
| **91** Human cues | S1 preserve/inject policy |
| **92** Stylometry integration | Pre-pipeline targets; voice vs anti-detector |
| **93** Commercial landscape | Positioning; honesty |
| **94** Regulatory | ESL warrant; Art. 50 boundaries |
| **95** Watermark | Collateral side effect doc |
| **96** User segments | Mode recommendations per segment |

---

## 15. Bottom line

Phase 3 is **compose the 2026 evasion stack into a bounded, API-deliverable orchestrator**: MASH-shaped alignment, HIP-shaped cross-model iteration, TempParaphraser-shaped sentence selection, AdvPara-shaped detector-guided repair, practitioner capstone — all behind `anti-detector`, all subordinate to `validate.py`, all measured on unslop fixtures rather than paper ASR tables.

Deterministic unslop remains the foundation. The pipeline is the **optional distribution layer** for ESL false positives and resume polish — the cases Boundaries allow.

Voice PEFT runs **parallel** as research: StyleTunedLM proves the objective, P2P proves deployment economics, Catch Me proves the eval oracle. Ship T1 prompt voice today; parametric T4 only after AV bench moves the numbers.

Ship it honest. Ship it gated. Bench it on fixtures first, commercial panel when the May detector-test CSV exists. Never pretend regex ate StealthRL.

---

*PLAN-99 complete. Master Integration Agent #99. Next: approve Sprint 0 prerequisites → Sprint 1 `llm_pipeline.py` skeleton.*
