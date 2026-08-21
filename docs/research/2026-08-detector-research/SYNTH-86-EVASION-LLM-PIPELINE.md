# SYNTH-86 — LLM-Based Evasion / Humanization Pipelines

**Synthesis Agent #86**  
**Date:** 2026-08-19  
**Scope:** Multi-stage, cross-model, detector-in-loop LLM pipelines unslop could ship in Phase 3  
**Inputs:** Agents #21–#26, #28, #31, #35, #38–#40, #50, #23; `UPDATE-PLAN-2026-08.md`; `SYNTH-83-DETECTION-CODE-GAP.md`  
**Audience:** unslop maintainers — `llm_pipeline.py` spec, CLI surface, benchmark matrix, Boundaries

---

## Executive summary

2025–2026 evasion research converged on one architectural pattern: **deterministic lexical scrubbing is prep; distributional reshaping requires LLM resampling, ideally cross-model, optionally detector-guided, almost always multi-pass.** Single-call `humanize_llm()` is the weakest link in unslop's anti-detector story — not because the prompt is wrong, but because the field moved from "remove AI vocabulary" to "leave the generator's statistical manifold."

Phase 3 should ship **`llm_pipeline.py`**: a gated orchestrator that runs after deterministic Phases 1–2 (lexical, structural, soul, dynamics targets) and composes five research-backed stages:

| Stage | Research analog | Mechanism | LLM calls (1K words, balanced) |
|-------|-----------------|-----------|-------------------------------|
| **S1** | MASH Stages 2–4 | Align → critique → fix → optional PPL-gated polish | 3–4 |
| **S2** | HIP | Cross-model iterative plain paraphrase | 1–4 rounds |
| **S3** | TempParaphraser | Hot-sentence N-candidate + detector argmin | 2 batched |
| **S4** | Adversarial Paraphrasing | Detector-guided span rewrite (document-level analog) | 3 |
| **S5** | Cross-model capstone | Final pass via different provider than S2 | 1 |

**Detector-in-loop policy:** TMR (and post–Phase 2: DivEye σ, TSD, SurpMark proxies) are **stop/diagnostic signals**, not optimization targets. StyleShield's RateAudit proves window-aggregated percentages are gameable — unslop must never ship score-targeting schedulers. The loop answers: "Did we move enough to stop?" not "How low can we drive the number?"

**Honest ceiling:** MASH reports 92% ASR on RoBERTa/Writer/Scribbr; HIP wins on GPTZero/Pangram; StealthRL hits 97.6% ASR on open detectors with RL fine-tune. unslop's API-only prompt analog will land **between deterministic (~0.2 pp TMR)** and trained adversaries — target **≥5 pp TMR improvement vs legacy `humanize_llm()`** on ≥3 fixtures, semantic preservation ≥0.92, preservation suite 100%. Never market paper ASR numbers as product guarantees (DAMAGE: 20–100 pp spread across commercial humanizers on the same input).

**Boundaries unchanged:** ESL false-positive defense, resume polish, voice-match — not academic misconduct. Refuse watermark removal (EU AI Act Art. 50 in force Aug 2026). Gate full pipeline behind `--intensity anti-detector --llm-pipeline`.

---

## 1. Why Phase 3 exists — the single-pass gap

### 1.1 What unslop ships today

| Component | Behavior | Evasion relevance |
|-----------|----------|-------------------|
| `humanize.py` deterministic | ~100 regex families + validator | Signal 1 (lexical) — strong |
| `structural.py` | Sentence-length σ restoration | Signal 2 — partial; AdvPara: lexical-only **raises** TPR +8–15% on RADAR/Fast-DetectGPT without this |
| `soul.py` | Contraction injection | Paneru-informed human marker |
| `surprisal.py` | DivEye 10-feature vector | Signal 3 — **measure only** |
| `humanize_llm()` | 1 pass + optional audit (full/anti-detector) | Partial MASH S1 analog; **no iteration, no cross-model, no N-sample pick** |
| `detector.feedback_loop()` | Deterministic intensity ladder; TMR stop | Never reaches `anti-detector`; no LLM inside loop |

Empirical constraint (repo-backed): deterministic passes drop AI-isms 88–92% but move TMR **~0.0–0.2 pp** on fixtures. Commercial detector screenshots in the May detector-test article require **distribution-layer** rewrite — documented as manual cross-model step today.

### 1.2 What the evasion memos agree on

1. **Naive paraphrase is not neutral** — Adversarial Paraphrasing (NeurIPS 2025): synonym-level LLM rewrite *increases* detection on modern detectors. Structural + burstiness must precede or accompany LLM paraphrase.
2. **Cross-model beats same-family polish** — HIP: base/instruct gap on GPTZero (96.7% vs 30.3% human prob); Agent #35: family swap breaks perplexity curvature Binoculars reads.
3. **Iteration matters** — HIP N=10; TempParaphraser N=7 sentence samples; MASH Stage 4 sentence polish. unslop should cap at 1–4 rounds for cost/semantic drift.
4. **Detector guidance helps when available** — TempParaphraser argmin, AdvPara token pick, MASH DPO — but proxy detectors (CoPA) lose to boundary-aligned training (MASH tables: CoPA ASR ~0 on RoBERTa).
5. **Quality–evasion is a real tradeoff** — Jemama: style fidelity ⊥ statistical naturalness; StealthRL: ASR 97.6% but quality Likert 2.51 vs 3.78 simple paraphrase. unslop must preserve meaning via `validate.py` contract.
6. **Commercial eval ≠ academic ASR** — MASH: Writer/Scribbr; HIP: GPTZero/Pangram; Turnitin Feb 2026 anti-humanizer retrain invalidates pre-2025 bypass claims.

---

## 2. Unified pipeline architecture

### 2.1 End-to-end flow

```
Input text
  │
  ├─► [Phase 0] validate.py eligibility (size, sensitivity)
  │
  ├─► [Phase 1–2 deterministic] humanize → structural → soul
  │       └─ optional: dynamics_targets (TSD, SurpMark, cone proxy)  ← Phase 2 dep
  │
  ├─► [Phase 3 LLM pipeline] llm_pipeline.run()  ← THIS MEMO
  │       S1 MASH align+critique+fix [+refine]
  │       S2 HIP iterative cross-model paraphrase
  │       S3 TempParaphraser hot-sentence multi-sample
  │       S4 AdvPara span loop (detector-guided)
  │       S5 cross-model capstone
  │
  ├─► validate.py (preservation + AI-ism residual)
  │
  └─► [optional] detector.feedback_loop()
          multi-objective stop: TMR ≤ target AND dynamics in human band
```

**Gate:** `--intensity anti-detector --llm-pipeline {fast|balanced|max}`. Default off. `voice-match` uses S1a + voice profile only; skips S2–S5 evasion stages.

### 2.2 Stage dependency graph

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

- **S1 before S2:** MASH ablation — SFT without boundary critique underperforms; critique/fix separates "human register" from "detector-safe distribution."
- **S2 before S3:** HIP moves document-level instruct fingerprint; S3 targets residual hot sentences (high TMR chunk or high local surprisal).
- **S4 after S2/S3:** AdvPara-style repair on spans still flagged after global passes — avoids whole-document oversmooth.
- **S5 last:** Practitioner chain terminus (Agent #35); different provider than S2 rewriter.

Skip rules: if TMR ≤ target after any stage, short-circuit remaining stages (log which stage succeeded).

---

## 3. Stage specifications (research → code)

### 3.1 S1 — MASH-style align + refine (Agents #21)

**Research:** Style-SFT → DPO hard negatives → PPL-ordered sentence polish gated by detector (Gu et al., ACL Findings 2026, 92% avg ASR on 5 detectors).

**unslop mapping (no fine-tune):**

| Sub-stage | Calls | Prompt intent |
|-----------|-------|---------------|
| **S1a Draft** | 1 | Rewrite toward natural human register; apply unslop anti-slop rules; inject voice profile if `voice-match` |
| **S1b Critique** | 1 | Diagnose machine tells *as a detector would*: uniform rhythm, hedging, safe parallelism, low-entropy phrasing — cite spans |
| **S1c Fix** | 1 | Revise flagged spans only; strict preservation contract |
| **S1d Refine** (optional) | 0–K | Sort sentences by proxy PPL (surprisal if available); polish top-K flat sentences; **accept only if TMR holds or improves** |

**Voice conditioning:** Map `stylometry.py` + `style_memory.py` numeric profile into S1a system block — partial analog of MASH style embeddings, not learned vectors.

**Do not ship:** Style-SFT, DPO training, inverse data construction, BART 0.1B local rewriter (P3 research optional).

### 3.2 S2 — HIP iterative cross-model paraphrase (Agent #22)

**Research:** Minimal LoRA on base model + N=10 document iterations; GPTZero 0%→100% human prob by round 10 on sample (Xu et al., arXiv:2605.19516).

**unslop mapping (API approximation):**

1. **Cross-provider rewriter** — if source was Claude, S2 uses GPT/Gemini (or env-configured `UNSLOP_HIP_MODEL`).
2. **Plain HIP format** — no chat persona:

   ```
   <source_text>
   {current draft}
   </source_text>
   <target_text>
   {rewrite as natural human prose; preserve meaning}
   </target_text>
   ```

3. **Rounds:** 1–4 (not 10); env `UNSLOP_HIP_ROUNDS`.
4. **Stop:** `validate.py` pass; optional TMR ≤ target; semantic embedding ≥0.92 vs input to stage.

**Do not ship:** In-plugin LoRA training; OpenAI fine-tune path (HIP Appendix A.2 negative result). Optional P2 power-user backend: vLLM + upstream HF adapter — separate extra, not core wheel.

### 3.3 S3 — TempParaphraser multi-sample (Agents #24, #38)

**Research:** N=7 sentence paraphrases at T=1.2; pick lowest detector score; 82.5 pp avg accuracy drop on HC3 four-detector panel (Huang et al., EMNLP 2025).

**unslop mapping (algorithm port, no 1B fine-tune):**

```
hot_sentences = top_k_by(TMR_chunk_score + local_surprisal, k=ceil(0.15 * n_sentences))
for sent in hot_sentences:
    candidates = llm.paraphrase(sent, n=N, temperature=1.2)  # batched
    scores = [detector.score(merge(doc, c)) for c in candidates]
    pick = argmin(scores) subject to validate.preserve(sent, pick)
```

| Parameter | Default (balanced) | fast | max |
|-----------|-------------------|------|-----|
| N candidates | 5 | 3 | 7 |
| Hot sentence fraction | 15% | 10% | 25% |
| Batched calls | 2 | 1 | 3 |

**Fix existing bug:** `detector.py:390–392` incorrectly says TempParaphraser needs "no LLM call" — paper requires fine-tuned paraphraser + N× inference. Comment should distinguish **paper** vs **unslop recommendation**.

**Honest floor:** RADAR still 45.4% post-attack in paper — paraphrase-hardened detectors partially resist.

### 3.4 S4 — Adversarial span loop (Agents #25, #39)

**Research:** Token-level detector argmin at each generation step; −98.96% Fast-DetectGPT TPR, −87.88% avg across 8 detectors (Cheng et al., NeurIPS 2025). Simple paraphrase *increases* TPR on RADAR/Fast-DetectGPT.

**unslop mapping (document-level analog — no logit access):**

1. Score document with TMR; segment into spans (sentences or ≤512-token chunks matching detector windowing).
2. Rank spans by local `p_ai`; take top-K (default K=5).
3. For each span: LLM generates M paraphrase candidates (M=3); pick min TMR on merged doc.
4. Re-validate preservation; reject span if code/URL/heading mutation.

**External bridge (opt-in):** `--adv-paraphrase /path/to/chengez-clone` subprocesses `paraphrase_and_detect.py` after deterministic+S1–S3 fail — gate behind ethics prompt. Do not bundle 8B CUDA into pip wheel.

**CoPA complement (Agent #28):** Where logit access exists (local vLLM), optional dual-prompt contrastive decode — human-scene prompt minus machine "repeat paragraph" prompt, λ=0.5. API-only unslop: approximate via S1b/S1c prompt pair, not logit subtraction.

### 3.5 S5 — Cross-model capstone (Agent #35)

**Research:** Practitioner GPT→Claude→Gemini chains; operational form of TempParaphraser + blind AdvPara; DAMAGE GPTZero TPR 99.73%→60.04% on humanized academic text (ensemble effect, not single tool).

**unslop mapping:**

- Single full-document rewrite via provider **≠ S2 provider** and **≠ original generator family** (if known from env).
- Prompt: structural preservation + anti-slop rules + "do not summarize."
- Already shipped as **manual recommendation** in `detector.py` ladder exhaustion — Phase 3 automates it.

---

## 4. Detector-in-loop design

### 4.1 Scorers (multi-objective, post–Phase 2)

| Scorer | Source | Role in loop |
|--------|--------|--------------|
| **TMR / Desklib** | `detector.py` | Primary stop: `p_ai ≤ target` (default 0.5) |
| **DivEye σ, Δ, Δ²** | `surprisal.py` | Secondary: human band p25–p75 from `stylometric_baseline.json` |
| **TSD second-half DD/LV** | Phase 2 `surprisal.py` | Anti "AI settles down" tell |
| **SurpMark ΔGJS** | Phase 2 | Anti recovery-pattern tell |
| **Cone-width proxy** | Phase 2 | GPTZero v6 analog |
| **Burstiness σ** | `stylometry.py` | Structural sanity check |

**Stop policy (Phase 3 + Phase 2 deps):**

```python
def should_stop(readings, target_p_ai=0.5) -> bool:
    return (
        readings.tmr <= target_p_ai
        and readings.dynamics_in_human_band()  # all implemented dynamics metrics
        and readings.ai_isms == 0
    )
```

### 4.2 What the loop must NOT do (Agent #23 StyleShield / RateAudit)

| Anti-pattern | Why forbidden |
|--------------|---------------|
| **RateAudit-style chunk scheduler** targeting document-level % AI | Gameable; disqualifies percentage verdicts as evidence |
| **γ-as-hard-optimizer** sweeping perturbation until score hits floor | StyleShield 94.6% evade at γ=7.0 — optimizes detector, destroys honesty |
| **Watermark-targeted guidance** | EU AI Act Art. 50; already refused in `detector.py` |
| **Score-targeting intensity** | Map `subtle/balanced/full/anti-detector` to *rewrite depth*, not TMR setpoints |

**Adopt from StyleShield:** intensity tiers = increasing **perturbation budget** with explicit semantic stop rules (validate.py), not "drive P_AI to X%."

### 4.3 Feedback loop integration

Today `feedback_loop()` re-humanizes **original** text at higher deterministic intensity — non-cumulative, no LLM, no `anti-detector`.

**Phase 3 change:**

1. Run `llm_pipeline` **before** feedback loop when `--llm-pipeline` set.
2. Feedback loop operates on **pipeline output**, not original — cumulative refinement.
3. Add `anti-detector` as ladder step 4 (Phase 1 prerequisite).
4. If loop exhausts: recommend manual cross-model (already shipped) + log which pipeline stages ran.

**StealthRL calibration (Agent #26):** RL paraphrase ASR 97.6% on open detectors — upper bound for adaptive adversary. unslop loop closes **polish gap**, not red-team gap. README must say so.

---

## 5. Cross-model orchestration

### 5.1 Provider matrix

| Role | Selection rule | Rationale |
|------|----------------|-----------|
| **S1 author pass** | User's configured default (Anthropic SDK / CLI) | Voice-match continuity |
| **S2 HIP rewriter** | `UNSLOP_HIP_MODEL` ≠ default provider | Instruction-tuning fingerprint swap |
| **S3 candidate generator** | Same as S2 or third family | Entropy diversity |
| **S5 capstone** | Third provider if available; else S2 | Practitioner 2–3 hop chain |

Env surface:

```bash
UNSLOP_LLM_PIPELINE=balanced       # fast | balanced | max
UNSLOP_HIP_ROUNDS=2
UNSLOP_HIP_MODEL=openai/gpt-4o     # example
UNSLOP_S3_N_CANDIDATES=5
UNSLOP_S4_TOP_SPANS=5
UNSLOP_PIPELINE_SHORT_CIRCUIT=1      # stop when TMR target met
```

### 5.2 Base-model proxy without local weights

HIP's core insight: **commercial detectors flag instruct-tuning, not "AI-ness."** API proxies for "base-like" behavior:

- Prefer models with less aggressive RLHF smoothing (document per provider; user-configurable).
- Plain continuation prompts (HIP tags) over assistant persona.
- Lower temperature on S1 (0.7); S3 candidate gen at T=1.2 (TempParaphraser).

No claim these equal HIP LoRA — benchmark empirically.

---

## 6. Budget presets and cost model

From UPDATE-PLAN, per ~1K words:

| Preset | Stages enabled | Est. calls | Est. cost |
|--------|----------------|------------|-----------|
| **fast** | S1 (3) + S2 (1 round) | ~4 | ~$0.10 |
| **balanced** | S1 + S2 (2) + S3 (2 batched) | ~7 | ~$0.30 |
| **max** | S1 + S1d + S2 (4) + S3 + S4 + S5 | ~12–15 | ~$0.70 |

Implementation: `PipelineBudget` dataclass with stage toggles + round caps; CLI `--llm-pipeline fast|balanced|max`.

**Semantic drift guard:** After each stage, run `validate.py`; on failure, revert stage output and log. Optional embedding similarity gate ≥0.92 vs pre-stage text (Jemama axis: don't confuse fidelity with naturalness — both matter).

---

## 7. Methods explicitly out of scope

| Method | ASR / headline | Why not in unslop v1 |
|--------|----------------|----------------------|
| **StealthRL** | 97.6% ASR, GRPO+LoRA Qwen3-4B | Requires adversarial fine-tune; quality tax; cite as upper bound only |
| **MASH Stages 1–3** | 92% ASR | Style-SFT + DPO + detector oracle training |
| **StyleShield** | ≥94.6% evade | 128×A800, Chinese LangFlow, embedding diffusion — not API-portable |
| **GradEscape** | 139M beats 11B DIPPER | Gradient detector optimization; white-box |
| **AuthorMist / RL watermark attacks** | High ASR | Training + ethics |
| **DIPPER 11B local** | Historical baseline | 40GB GPU; superseded by cross-model API for unslop users |
| **CoPA logit contrast** | +57.72% fooling vs Fast-DetectGPT | Requires logit access; MASH beats CoPA on RoBERTa |
| **RateAudit scheduling** | ≤1.4 pp deviation to任意 target % | Anti-pattern for product |

**Optional external bridges:** AdvPara repo subprocess, HIP vLLM adapter — power-user flags, not default.

---

## 8. Dual-axis quality model (Agent #50 Jemama)

Humanization optimizes two **orthogonal** axes:

| Axis | Mode | Metric |
|------|------|--------|
| **Style fidelity** | `voice-match` | Stylometry delta vs reference sample |
| **Statistical naturalness** | `anti-detector` | DivEye σ, TSD, burstiness, TMR |

Phase 3 benchmark must score **both on the same rewrite**. High voice-match without surprisal shift stays detectable (Jemama: 99.9% verifier agreement, μ PPL 15–16 vs human 29.5).

**Pipeline routing:**

- `voice-match` → S1a + S1c with profile; skip S2–S5 unless user also sets `anti-detector`.
- `anti-detector` → full pipeline; voice profile optional weak conditioner in S1a only.

---

## 9. Commercial reality check (Agents #40, #56, #57)

| Detector shift | Implication for pipeline |
|----------------|-------------------------|
| **GPTZero v6 cones** (Jan 2026) | Synonym-band rewrites fail; S2+S5 structural cross-model required |
| **Turnitin anti-humanizer** (Feb 2026 EN) | Pre-Aug 2025 bypass numbers stale; bench on May detector-test panel |
| **Pangram humanizer-augmented** (Aug 2025) | Catches 90.3–100% of named SaaS tools; pipeline must beat L1 paste-box on *our* fixtures or stay silent |
| **Originality AI Allowance** (Jul 2026) | Hybrid thresholds — document partial AI % honestly |

**DAMAGE tier context:** L1 fluency ≠ evasion (StealthGPT L1 quality, 95.6% still detected by Pangram). unslop competes with **cross-model chain + manual edit**, not Undetectable.ai marketing.

---

## 10. Proposed module API

```python
# unslop/scripts/llm_pipeline.py (Phase 3 — sketch)

@dataclass
class PipelineConfig:
    preset: Literal["fast", "balanced", "max"]
    hip_rounds: int
    hip_model: str | None
    s3_n_candidates: int
    s4_top_spans: int
    enable_s1d_refine: bool
    capstone_model: str | None
    target_p_ai: float
    short_circuit: bool

@dataclass
class PipelineReport:
    stages_run: list[str]
    tmr_before: float
    tmr_after: float
    dynamics_before: dict
    dynamics_after: dict
    semantic_score: float
    llm_calls: int
    estimated_cost_usd: float

def run_pipeline(
    text: str,
    *,
    config: PipelineConfig,
    intensity: Intensity = "anti-detector",
    voice_profile=None,
    detector_score_fn=score_ai_probability,
    surprisal_fn=compute_surprisal_variance,
) -> tuple[str, PipelineReport]: ...
```

**CLI:**

```bash
python3 -m unslop.scripts.cli humanize doc.md \
  --intensity anti-detector \
  --llm-pipeline balanced \
  --detector-feedback \
  --dynamics-feedback   # Phase 2 dep
```

**Tests:** Mock LLM + mock detector; preservation suite on pipeline output; opt-in live LLM tests (`UNSLOP_RUN_LLM_TESTS=1`).

---

## 11. Acceptance criteria (Phase 3 exit)

| Criterion | Target |
|-----------|--------|
| TMR improvement vs `humanize_llm()` | ≥5 pp on ≥3 fixtures |
| Semantic preservation | ≥0.92 embedding or judge score |
| `TestPreservation` | 100% pass |
| Dynamics (when Phase 2 shipped) | 2nd-half DD rises on ≥7/9 fixtures |
| Cost envelope | balanced preset ≤$0.35/1K words at Aug 2026 API pricing |
| Docs | SKILL.md: pipeline stages, Boundaries, no ASR marketing |
| Bench | `detector_bench.py` adds `llm_pipeline_{fast,balanced,max}` variants |

---

## 12. Implementation priority

| Priority | Work item | Effort | Depends on |
|----------|-----------|--------|------------|
| **P0** | Phase 1: `anti-detector` on feedback ladder | S | — |
| **P0** | `llm_pipeline.py` skeleton + S1 (MASH 3-call) | M | — |
| **P0** | S2 HIP template + `--hip-rounds` | M | multi-provider config |
| **P1** | S3 hot-sentence batch + detector argmin | M | Phase 1 detector wiring |
| **P1** | S1d PPL-gated refine | M | surprisal CLI wiring |
| **P1** | Fix `detector.py` TempParaphraser comment | S | — |
| **P2** | S4 span loop | M | chunk scoring |
| **P2** | S5 capstone + provider rotation | S | — |
| **P2** | Multi-objective stop (TMR + dynamics) | M | Phase 2 |
| **P2** | May detector-test commercial panel eval | L | article data |
| **P3** | `--adv-paraphrase` external bridge | M | ethics gate |
| **P3** | Optional local HIP/AdvPara backends | XL | research |

---

## 13. Research cross-reference matrix

| Paper | arXiv / venue | unslop stage | Adopt | Skip |
|-------|---------------|--------------|-------|------|
| MASH | 2601.08564 ACL 2026 | S1, S1d | Prompt chain, gated polish | SFT, DPO |
| HIP | 2605.19516 | S2 | Cross-model iteration | LoRA training |
| TempParaphraser | EMNLP 2025 | S3 | N-sample argmin | 1B fine-tune |
| Adversarial Paraphrasing | 2506.07001 NeurIPS 2025 | S4 | Span loop; external bridge | Token-level in pip |
| CoPA | 2505.15337 EMNLP 2025 | S1 prompt pair | Dual-prompt analog | Logit contrast |
| StyleShield | 2605.00924 | Policy | γ-as-intensity tier | RateAudit scheduler |
| StealthRL | 2602.08934 | README | Threat-model ceiling | GRPO in product |
| DIPPER | 2303.13408 NeurIPS 2023 | S5 analog | Cross-model discourse rewrite | 11B bundle |
| Sadasivan | 2303.11156 | Frame | Paraphrase reduces TV | — |
| Jemama | 2509.24930 UEMCON 2025 | Bench | Dual-axis metrics | — |
| DAMAGE | 2501.03437 COLING 2025 | Docs | Honest commercial gap | — |

---

## 14. Bottom line

Phase 3 is not "add another LLM prompt." It is **compose the 2026 evasion stack into a bounded, API-deliverable orchestrator**: MASH-shaped alignment, HIP-shaped cross-model iteration, TempParaphraser-shaped sentence selection, AdvPara-shaped detector-guided repair, practitioner capstone — all behind `anti-detector`, all subordinate to `validate.py`, all measured on unslop fixtures rather than paper ASR tables.

Deterministic unslop remains the foundation. The pipeline is the **optional distribution layer** for users facing ESL false positives and resume polish — the cases Boundaries allow. Ship it honest, ship it gated, bench it on GPTZero/Turnitin/Pangram when the May detector-test CSV exists, and never pretend regex ate StealthRL.

---

*Synthesis #86 complete. Cross-refs: SYNTH-83 (code gaps), UPDATE-PLAN-2026-08 Phase 3, Agents #21–26, #28, #31, #35, #38–40, #50, #23.*
