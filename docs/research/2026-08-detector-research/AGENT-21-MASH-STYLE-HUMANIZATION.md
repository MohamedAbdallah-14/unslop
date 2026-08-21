# Agent #21 — MASH (Multi-stage Alignment for Style Humanization)

**Topic:** Style-transfer fine-tuning for black-box detector evasion  
**Paper:** Gu, Li & Hu, *MASH: Evading Black-Box AI-Generated Text Detectors via Style Humanization* (arXiv:2601.08564, ACL Findings 2026)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop Phase 3 / anti-detector integration

---

## Executive summary

MASH (Multi-stage Alignment for Style Humanization) is a **detector-aware style-transfer humanizer** from Southeast University and Shanghai AI Lab (Gu, Li, Hu). The paper's core move is reframing evasion as **machine-style → human-style text transfer** rather than synonym swap or generic paraphrase. A ~0.1B BART-base paraphraser is trained through four sequential stages: inverse parallel-data construction, Style-injection SFT (Style-SFT), DPO alignment against detector scores, and optional inference-time adversarial refinement (PPL-ordered sentence polish gated by detector acceptance).

On **6 domains × 5 detectors** (3 open-source + 2 commercial APIs), MASH reports **92% average Attack Success Rate (ASR)**, claiming +24% over the strongest of 11 baselines while maintaining competitive BERTScore/GRUEN. Commercial evaluators Writer and Scribbr show **89% average ASR**. Inference without Stage 4 runs at **~3 GB GPU / 1.7 s per sample / zero query cost**. The official repo shipped April 2026 at `githigher/MASH`.

**unslop verdict:** MASH is the **reference architecture for "humanizer as a trained model"** — the clearest 2026 blueprint for multi-stage alignment. unslop cannot ship Style-SFT or DPO training in v1 (API-only, no fine-tune loop). Phase 3 should map MASH stages to **prompt analogs**: S1 = draft → critique → fix (3 LLM calls); Stage 4 refinement = PPL-ordered sentence polish with detector gate via existing `detector.py` TMR loop. Keep behind `anti-detector` intensity. Boundaries unchanged: ESL false-positive defense and resume polish — not academic misconduct.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv)** | https://arxiv.org/abs/2601.08564 |
| **Paper (HTML v2)** | https://arxiv.org/html/2601.08564v2 |
| **DOI (arXiv)** | https://doi.org/10.48550/arxiv.2601.08564 |
| **ACL Anthology** | https://aclanthology.org/2026.findings-acl.1487/ |
| **ACL PDF** | https://aclanthology.org/2026.findings-acl.1487.pdf |
| **DOI (ACL)** | https://doi.org/10.18653/v1/2026.findings-acl.1487 |
| **Official code (GitHub)** | https://github.com/githigher/MASH |
| **Paper note (ACL 2026)** | https://en.papernotes.org/ACL2026/aigc_detection/mash_evading_black-box_ai-generated_text_detectors_via_style_humanization/ |

### Lineage and comparison papers

| Paper | URL | Relation to MASH |
|-------|-----|------------------|
| **Nicks et al. DPO-Evader** (ICLR 2024) | https://openreview.net/forum?id=... | DPO with detector reward — MASH extends with Style-SFT + hard negatives |
| **DIPPER** (NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Strongest paraphrase baseline in MASH tables; fails OOD vs MASH |
| **CoPA** (EMNLP 2025) | https://arxiv.org/abs/2505.15337 | MASH Table 1–2: CoPA ASR near zero on RoBERTa; "indirect proxy-guidance fails to capture target-specific decision boundaries" |
| **GradEscape** (SEC 2025) | https://arxiv.org/abs/... | Strong gradient baseline; MASH beats on most domains |
| **DPO-Evader / Wang proxy attacks** | ICLR 2024 / ICLR 2025 | Same DPO-on-detector-score family |
| **HIP** (May 2026) | https://arxiv.org/abs/2605.19516 | Detector-agnostic base-model iteration; cites MASH, no head-to-head |
| **TempParaphraser** (EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1607/ | Entropy-simulation paraphrase; different lever |
| **StealthRL** (2026) | https://arxiv.org/abs/2602.08934 | RL ensemble evasion; higher ASR on open detectors, weak on commercial in HIP eval |
| **Paneru BART corpus** (Apr 2026) | https://arxiv.org/abs/2604.11687 | Parallel AI↔human style transfer; validates small encoder-decoder wins |
| **Sadasivan impossibility** | https://arxiv.org/abs/2303.11156 | Paraphrase shrinks TV distance — MASH is scaled style-transfer instance |
| **TH-Bench / MGTBench** | https://arxiv.org/abs/2503.08708 · https://arxiv.org/abs/2405.07940 | Evaluation corpora MASH uses |

**Citation note:** Authors are **Yongtong Gu, Songze Li, Xia Hu** (Southeast University + Shanghai AI Lab). Pages 29749–29769 in ACL Findings 2026. Some internal unslop docs mis-attribute to "Chen et al." — correct to Gu et al.

---

## MASH mechanism (four stages)

### Threat model

Black-box attacker: no detector architecture, parameters, or gradients. Oracle access to detector score \(D(\mathbf{x}) \in [0,1]\) or label \(\hat{y}\). Goal:

\[
\minimize \ \mathbb{E}[D(G_\phi(\mathbf{x}_{ai}))] \quad \text{s.t.} \ \mathcal{S}(\mathbf{x}_{adv}, \mathbf{x}_{ai}) \geq \epsilon,\ \mathcal{Q}(\mathbf{x}_{adv}) \geq \delta
\]

Semantic consistency \(\mathcal{S}\) and fluency \(\mathcal{Q}\) must hold. MASH learns generator \(G_\phi\) as a **style-conditioned paraphraser**, not a prompt hack.

### Stage 1 — Inverse data construction

Parallel AI↔human pairs are scarce. MASH inverts the direction:

1. Collect human text \(\mathbf{x}_{human}\) from open corpora; filter to high-confidence human (\(D(\mathbf{x}_{human}) < \tau\)).
2. LLM paraphrases human → machine style \(\mathbf{x}_{ai}\); keep pairs where \(D(\mathbf{x}_{ai}) > \tau\).
3. Result: \(\mathcal{D}_{pair} = \{(\mathbf{x}_{ai}^{(i)}, \mathbf{x}_{human}^{(i)})\}_{i=1}^{N}\).

Training direction is **AI → human** (same as HIP). Solves data scarcity without harvesting detected AI text.

**Repo script:** `stage1_data_construction.py` — streams HuggingFace datasets, filters via target detector.

### Stage 2 — Style-injection SFT (Style-SFT)

Base: **BART-base** (~0.1B). Two trainable style embeddings \(\mathbf{s}_{ai}, \mathbf{s}_{human} \in \mathbb{R}^d\) fused into encoder states:

\[
\mathbf{H}_{fused}^{(t)} = \mathbf{W}_p \cdot [\mathbf{h}_{content}^{(t)}; \mathbf{s}_{style}] + \mathbf{b}_p
\]

Dual-objective loss:

- \(\mathcal{L}_{recon}\): reconstruct \(\mathbf{x}_{ai}\) given \(\mathbf{s}_{ai}\) (semantic anchor)
- \(\mathcal{L}_{trans}\): generate \(\mathbf{x}_{human}\) given \(\mathbf{x}_{ai}\) + \(\mathbf{s}_{human}\) (style transfer)

\(\mathcal{L}_{SFT} = \lambda \mathcal{L}_{recon} + (1-\lambda) \mathcal{L}_{trans}\)

**What SFT teaches:** "what human style looks like" — not yet "how far past the detector boundary."

**Repo scripts:** `stage2_style_sft.py`, `stage2_inference.py` (collect hard negatives).

### Stage 3 — DPO alignment (detector-boundary crossing)

Implicit reward from detector confidence (Theorem 1 in paper):

\[
r(\mathbf{x}, \mathbf{y}) = C \cdot (1 - D(\mathbf{y})), \quad C > 0
\]

Maximizing reward pushes policy toward \(D(\mathbf{y}) \to 0\).

**Hard negative mining:** For each \(\mathbf{x}_{ai}\):
- **Chosen** \(\mathbf{y}_w\): ground-truth human text
- **Rejected** \(\mathbf{y}_l\): sample from Stage-2 model that **still fails** evasion (\(D(\mathbf{y}_l) > \tau\))

Hard negatives maximize \(\Delta D = D(y_l) - D(y_w) \approx 1\), preventing vanishing DPO gradients (Appendix A.2).

**What DPO teaches:** cross the **target detector's decision boundary**, not generic "human-ish" prose.

**Repo script:** `stage3_dpo_alignment.py` (TRL DPO).

### Stage 4 — Inference-time adversarial refinement (optional)

Post-DPO text \(\hat{T}\) may have fluency scars. Refinement:

1. Split into sentences \(S = \{s_1, \dots, s_n\}\).
2. Rank by **perplexity descending** (fix worst fluency first).
3. LLM polisher \(\mathcal{G}\) proposes candidate \(c_i\) per sentence.
4. **Greedy accept** only if detector still predicts human.

Query-efficient: prioritizes high-PPL sentences; amortized cost negligible at scale (Figure 12, Appendix C). Paper uses GPT-5 for polish; Qwen2.5-7B-Instruct viable on budget (GRUEN 0.468 → 0.631 vs GPT-5 0.667).

**Generalizes beyond MASH:** Stage 4 applied to other attack outputs improves quality on most baselines (Figure 7) — a portable post-processor.

**Repo script:** `stage4_refinement.py`.

---

## Benchmarks and reported results

### Evaluation setup

| Axis | Detail |
|------|--------|
| **Datasets (6)** | MGTBench: Essay, Reuters, WP · MGT-Academic: STEM, Social, Humanity |
| **Detectors (5)** | Open: fine-tuned **RoBERTa**, **Binoculars**, **SCRN** · Commercial APIs: **Writer**, **Scribbr** |
| **Baselines (11)** | Perturbation: DeepWordBug, TextBugger, TextFooler, Charmer, HMGC · Prompt: PromptAttack · Paraphrase: DIPPER, DPO-Evader, ToBlend, CoPA, GradEscape |
| **Metrics** | ASR (primary), PPL, BERTScore, GRUEN |
| **Hardware** | Single NVIDIA RTX 3090; AdamW; BART-base init |

### Headline numbers

| Claim | Value | Context |
|-------|-------|---------|
| **Average ASR** | **92%** | Across 6 datasets × 5 detectors (paper abstract) |
| **vs strongest baseline** | **+24%** average | Abstract; +29.7% vs RoBERTa specifically (§4.2) |
| **Commercial ASR** | **89%** average | Writer + Scribbr, Table 3 |
| **Binoculars uplift** | **+19%** vs strongest | Zero-shot detector family |
| **1% FPR regime** | TPR → near-zero | Social + STEM domains, ROC analysis |
| **Efficiency** | ~3 GB, 1.7 s/sample, 0 queries | Stages 1–3 inference; excludes Stage 4 LLM polish |
| **Adversarial training defense** | ASR 92% → ~0% | But −18.7% clean accuracy — costly trade |

### Selected per-detector highlights (MASH vs field)

**RoBERTa (Table 1):** MASH ASR 0.73–1.00 across domains. DIPPER 0.00–0.57. CoPA 0.01–0.20. GradEscape 0.22–0.52. Charmer competitive on some domains (0.73–0.84) but worse quality metrics.

**Binoculars (Table 2):** MASH 0.85–0.99. GradEscape strong second (0.37–0.95). DIPPER 0.16–0.53.

**Commercial (Table 3):** Scribbr 0.59–1.00 ASR by domain; Writer 0.66–0.99. BERTScore ~0.78–0.93 preserved.

### Ablations (Figure 4, Appendix F)

| Component removed | Effect |
|-------------------|--------|
| **DPO only** | Large ASR drop — SFT alone insufficient for boundary crossing |
| **Refinement only** | ASR stable; GRUEN/PPL degrade — DPO hurts surface fluency |
| **Hard negatives vs ambiguous pairs** | Hard negatives +6–64 pp ASR on Reuters (Table 5, Appendix A) |
| **Data source** | Domain-sensitive — cc_news works for Reuters; some HF sets fail detector human filter |
| **Data size** | ASR scales with training pairs (Figure 6) |

### Transferability limits

- **Cross-domain:** Mostly robust except **Reuters** → other domains (ASR → ~0); Appendix G analysis.
- **Cross-detector:** Attacks optimized on supervised detectors (RoBERTa, SCRN) transfer to Binoculars; **reverse fails** — zero-shot optimization does not beat supervised-boundary training.
- **Not evaluated:** GPTZero, Pangram, Turnitin, Originality, Copyleaks — the 2026 commercial panel unslop cares about. Writer/Scribbr are commercial but not the US academic default.

### TH-Bench gap

MGTBench/MGT-Academic are MASH's primary benches. **TH-Bench** (Zheng et al., KDD 2025) predates MASH and may not include it in frozen attack sets (`AGENT-19-MGTBENCH.md` notes post-2025 attacks missing). MASH should be added to unslop's internal bench matrix, not assumed in legacy TH-Bench leaderboards.

---

## Code and reproduction

**Repository:** https://github.com/githigher/MASH  
**Created:** 2026-04-18 · **Stars:** ~12 (early) · **License:** research-only  
**Stack:** Python, PyTorch, Transformers, TRL, HuggingFace datasets

| Script | Stage |
|--------|-------|
| `stage1_data_construction.py` | Filter human corpus via detector |
| `stage2_style_sft.py` | Style-injection SFT on `train_pairs.jsonl` (`src`/`trg`) |
| `stage2_inference.py` | SFT inference + hard-negative collection |
| `stage3_dpo_alignment.py` | DPO from preference pairs |
| `stage4_refinement.py` | PPL-ranked LLM polish + detector gate |

**Dependencies:** `torch transformers datasets trl accelerate tqdm matplotlib numpy`

**Repro cost (estimated):**
- Stage 1–3: single RTX 3090 feasible (paper config)
- Stage 4: optional LLM API (GPT-5 in paper) — dominant dollar cost
- Detector oracle queries during DPO data prep — not at inference for Stages 1–3

**Gaps vs paper:**
- No pre-trained MASH weights on HuggingFace at fetch time (train-your-own)
- No bundled `train_pairs.jsonl` — user constructs via Stage 1 + LLM paraphrase
- Commercial detector APIs (Writer, Scribbr) needed to reproduce Table 3 exactly

**Maturity:** Credible — ACL Findings acceptance + stage scripts match paper Figure 2. Early community adoption; 1 open GitHub issue at fetch.

---

## Community debate — who agrees, who pushes back

### Aligns with MASH / reinforces the thesis

| Actor | Position |
|-------|----------|
| **Nicks et al. (ICLR 2024)** | Detectors are optimizable against via DPO — MASH systematizes with style vectors + hard negatives |
| **DIPPER / paraphrase line** | Paraphrase evades detectors; MASH shows **fine-tuned style transfer >> raw DIPPER** on same benches |
| **Paneru (2026)** | Small encoder-decoder (BART) beats 7B instruct on AI→human style transfer — independent validation of MASH's scale choice |
| **Practitioner consensus (2026)** | Prompt-only humanization insufficient for institutional detectors post-Turnitin Feb 2026 update — MASH-style pipelines or real editing required (`docs/research/01-prompt-engineering-humanization/E-practical.md`) |
| **DAMAGE / commercial audit line** | Research humanizers (MASH 92% ASR) far exceed commercial tier-1 products — gap widening |
| **unslop UPDATE-PLAN Phase 3** | Names MASH as S1 stage analog in `llm_pipeline.py` blueprint |

### Partial agreement / different emphasis

| Actor | Position |
|-------|----------|
| **HIP authors (May 2026)** | Agree evasion works; argue **detector-agnostic base-model recovery** suffices for GPTZero/Pangram without DPO training — different Pareto point |
| **TempParaphraser authors** | Agree multi-pass paraphrase evades; attribute vulnerability to **entropy/temperature statistics**, not style vectors |
| **CoPA authors** | Contrastive decoding helps but MASH shows **target-specific DPO >> generic machine-logit subtraction** |
| **DivEye / TSD / SurpMark (2025–2026)** | New temporal surprisal signals may survive style transfer — **MASH did not evaluate**; unslop ships DivEye proxies |
| **Detector vendors** | Will retrain on MASH outputs — paper §4.5 shows adversarial training works but hurts clean accuracy |
| **StealthRL line** | Higher ASR on open-detector ensembles (97.6%) but RL training cost >> MASH's 0.1B pipeline |

### Disagrees or limits the claim

| Actor | Position |
|-------|----------|
| **CoPA empirical results in MASH tables** | CoPA ASR near zero on RoBERTa — proxy guidance insufficient vs boundary-aligned DPO |
| **Reuters cross-domain failure** | MASH ASR collapses on some cross-domain transfers — not universal humanization |
| **English-only scope** | Paper limitations: MGTBench/MGT-Academic English; morphologically rich languages unexplored |
| **High-FPR detectors** | Style mimicry meaningless if detector already flags ground-truth human — logical prerequisite, not bug |
| **Academic integrity community** | Any evasion framework is adversarial to proctoring — ethics statement acknowledges misuse risk |
| **unslop Boundaries** | Anti-detector mode for ESL/resume defense only — MASH ASR numbers are not product guarantees |

### Notable absence

No Hacker News / Reddit thread dedicated to MASH at fetch time. Discussion is **academic-channel** (ACL Findings, arXiv, PaperNotes) plus unslop research corpus synthesis. Practitioner uptake likely via humanizer-tool blogs citing 92% ASR — treat as **research snapshot**, not independent audit.

---

## MASH vs HIP vs TempParaphraser vs CoPA

| Dimension | **MASH** | **HIP** | **TempParaphraser** | **CoPA** |
|-----------|----------|---------|---------------------|----------|
| **Core idea** | Style vectors + detector DPO + gated polish | Base-model LoRA + iterative paraphrase | Multi-pass normal-temp ≈ high-temp entropy | Contrastive decoding \(p_h - \lambda p_m\) |
| **Detector-aware training** | **Yes** — DPO reward = \(-D(y)\) | **No** | **No** | Partial (proxy machine logits) |
| **Model scale** | ~0.1B BART | 0.6B–70B base + LoRA | 1B | Any with logit access |
| **Iteration** | Sentence polish at inference (Stage 4) | Document-level N=10 | Sentence multi-round | Single-pass |
| **Commercial eval** | Writer, Scribbr | **GPTZero, Pangram** | Open detectors | Fast-DetectGPT focus |
| **unslop adoptability** | Stage 4 + prompt S1 only | S2 cross-model iteration | S3 multi-sample | Dual-prompt analog |
| **Head-to-head** | — | Cites MASH, no table | Not in MASH baselines | **Beaten badly in MASH tables** |

**Practitioner synthesis:** MASH wins when you can **train against a detector oracle** and ship a local 0.1B rewriter. HIP wins for **2026 US commercial classifiers** without detector training. TempParaphraser wins as **cheap sentence rewriter**. For API-only unslop: approximate MASH **Stage 4 + S1 prompt chain**, not Style-SFT/DPO.

---

## unslop integration — multi-stage style alignment (prompt analog)

### Current state (August 2026 codebase)

| Component | MASH relevance |
|-----------|----------------|
| `humanize.py` phases | Lexical → `structural.py` (Phase 1) → `soul.py` (Phase 5) — **deterministic style nudges**, not detector-aligned |
| `humanize_llm()` | Single pass + optional audit at `full`/`anti-detector` — **one-shot**, not 4-stage |
| `_build_humanize_prompt()` | Two-pass self-audit (draft + revise) — **partial S1 analog** already in prompt |
| `detector.feedback_loop()` | TMR escalation across deterministic intensities — **Stage 4 gate analog** if wired to sentence accepts |
| `stylometry.py` / `surprisal.py` | Measure burstiness, contractions, DivEye — orthogonal to MASH style embeddings |
| Phase 3 plan | **`llm_pipeline.py` S1 = MASH align+refine** (3 calls) per `UPDATE-PLAN-2026-08.md` |

MASH training stages (1–3) are **out of scope** for unslop v1. Stage 4 and the **multi-call alignment shape** are in scope.

### Recommended architecture

```
Input text
  → [existing] deterministic passes (lexical, structural, soul, surprisal targets)
  → [S1] MASH-style align + refine (3 LLM calls)     ← THIS MEMO (primary)
  → [S2] HIP iterative cross-model paraphrase (1–4 rounds)
  → [S3] TempParaphraser multi-sample hot sentences
  → [S4] Adversarial span loop (detector-guided)
  → [S5] Cross-model capstone
  → validate.py preservation + AI-ism residual
  → [optional] detector.feedback_loop (TMR target)
```

Gate entire pipeline behind `--intensity anti-detector` and `--llm-pipeline balanced|max`.

### S1 prompt spec (MASH Stages 2–3 analog without fine-tuning)

Three-call chain mapping Style-SFT → DPO → acceptance:

| Call | MASH analog | Prompt intent |
|------|-------------|---------------|
| **S1a Draft** | Style-SFT transfer | Rewrite AI-style prose toward natural human register; preserve meaning; apply unslop anti-slop rules |
| **S1b Critique** | DPO implicit reward | Diagnose remaining machine tells **as a detector would**: uniform rhythm, low perplexity bands, hedging, safe parallelism — cite phrases |
| **S1c Fix** | Hard-negative rejection | Revise only flagged spans; **do not** reintroduce patterns from S1b list; preservation contract strict |

This mirrors MASH's separation of "learn human style" (SFT) vs "cross boundary" (DPO) without training.

### S1d refinement (Stage 4 analog)

Optional fourth sub-stage inside S1 or post-S2:

1. Score sentences by **proxy fluency** (local perplexity if `--surprisal-variance`; else length/variance heuristic).
2. Rewrite top-K "flat" sentences via LLM polish prompt.
3. **Accept only if** TMR improves or holds vs `detector.py` — greedy gate matching MASH Stage 4.

```python
# Pseudocode — future llm_pipeline.py
for sent in sorted_by_ppl(sentences, descending=True)[:K]:
    candidate = llm_polish(sent, context=paragraph)
    if detector_score(merge(candidate)) <= detector_score(current):
        apply(candidate)
```

Wire to Phase 1 `--detector-feedback` once anti-detector is on the feedback ladder.

### What maps cleanly vs what does not

| MASH component | unslop mapping | Feasibility |
|----------------|----------------|-------------|
| Inverse data construction | N/A (user brings text) | — |
| Style embeddings \(\mathbf{s}_{human}\) | Voice profile from `stylometry.py` + `style_memory.py` | **Partial** — numeric targets, not learned embeddings |
| Style-SFT | S1a draft prompt + deterministic pre-pass | **High** |
| DPO hard negatives | S1b critique → S1c fix | **Medium** — no trained rejected samples; LLM simulates |
| Stage 4 PPL polish | S1d + `detector.feedback_loop` | **High** after Phase 1 wiring |
| 0.1B local paraphraser | Not shipped | **Out of scope** v1 |

### Environment surface (proposed)

```bash
UNSLOP_LLM_PIPELINE=balanced          # fast | balanced | max
UNSLOP_MASH_S1=1                      # 0 = skip align+refine chain
UNSLOP_MASH_REFINE=1                  # Stage 4 analog
UNSLOP_MASH_REFINE_TOPK=5             # sentences per pass
python3 -m unslop.scripts.cli humanize doc.md \
  --intensity anti-detector --llm-pipeline --detector-feedback
```

### Why optional, not default

1. **Cost** — S1 alone is 3–4 LLM calls; full pipeline ~$0.10–0.70 per 1K words (`UPDATE-PLAN` budget table).
2. **Semantic drift** — aggressive boundary-crossing rewrites risk meaning loss; `validate.py` preservation contract may reject.
3. **No fine-tune** — prompt analog lacks MASH's 92% ASR; empirical TMR/GPTZero bench required before marketing claims.
4. **Boundaries** — multi-stage evasion is powerful; ESL/resume use only; never "MASH-powered undetectable."
5. **Detector mismatch** — MASH trained vs RoBERTa/Writer/Scribbr; unslop users face GPTZero/Turnitin — transfer unknown.

### Acceptance criteria (Phase 3)

- `llm_pipeline` S1 beats legacy `humanize_llm()` by **≥5pp TMR** on ≥3 fixtures.
- Semantic preservation **≥0.92** (embedding or judge).
- `TestPreservation` suite **100% pass**.
- Document that ASR/TPR numbers are **benchmark snapshots**, not warranties (DAMAGE gap applies).

### Interaction with five-signal detector stack

MASH primarily attacks **semantic + statistical style features** (RoBERTa, Binoculars). 2026 detectors also read:

| Signal | MASH addresses? | unslop gap |
|--------|-----------------|------------|
| Lexical AI-isms | Indirectly via human style | ✅ `humanize.py` |
| Burstiness | Partially via human style transfer | ⚠️ `structural.py` |
| Surprisal variance (DivEye) | **Not evaluated** | ⚠️ measure only |
| Late-stage stability (TSD) | **Not evaluated** | ❌ Phase 2 |
| Predictability cones (GPTZero v6) | **Not evaluated** | ❌ Phase 2 |

Honest positioning: MASH S1 is **necessary but not sufficient** against 2026 five-signal stack — combine with Phase 2 dynamics targets and S2 HIP cross-model.

---

## Implementation priority for unslop

| Priority | Action | Effort |
|----------|--------|--------|
| **P0** | Phase 1: wire `anti-detector` on detector feedback ladder | S |
| **P0** | Implement `llm_pipeline.py` S1 (3-call MASH analog) | M |
| **P1** | S1d Stage-4 refinement with TMR gate + PPL sort | M |
| **P1** | Map voice profile → S1a style conditioning block | S |
| **P2** | Bench S1 vs MASH paper metrics on open detectors (RoBERTa, Binoculars) | L |
| **P2** | Evaluate against GPTZero/Pangram in May detector-test article | L |
| **P3** | Optional local BART rewriter — only if users demand offline | XL (research) |

**Do not:** Ship DPO training, detector-oracle data loops, or "92% ASR" marketing. Reference MASH as architecture inspiration.

---

## Key numbers (quick reference)

| Metric | Value | Source |
|--------|-------|--------|
| Average ASR | 92% | Abstract |
| Commercial ASR (Writer + Scribbr) | 89% | Table 3 |
| vs strongest baseline | +24% ASR | Abstract |
| Model size | ~0.1B (BART-base) | §4.1 |
| Inference memory | ~3 GB | Table 4 |
| Inference latency | 1.7 s/sample | Table 4 |
| Query cost (Stages 1–3 infer) | 0 | Table 4 |
| Adversarial training defense | ASR → ~0%, −18.7% clean acc | §4.5 |
| GitHub stars (Apr 2026) | ~12 | github.com/githigher/MASH |

---

## Bottom line

MASH established the **2026 reference pipeline for detector-aware style humanization**: invert parallel data, inject human style via supervised dual-objective training, cross detector boundaries with DPO on hard negatives, then gate fluency fixes at inference. At 0.1B parameters it beats 11B DIPPER on MASH's benches — continuing the "small model + right training signal" trend (GradEscape, AuthorMist, HIP).

unslop should **not** fine-tune BART. It should ** adopt the stage decomposition**: separate style alignment (S1a) from boundary critique (S1b) from constrained fix (S1c) from detector-gated polish (S1d/Stage 4). That architecture fits API-only delivery, preserves the preservation contract, and stays within Boundaries when gated to `anti-detector` mode. MASH's 92% ASR is a **research ceiling** for trained rewriters; unslop's honest product is **sound human prose + optional multi-stage LLM** for users facing ESL false positives — measured on our bench, not the ACL table.
