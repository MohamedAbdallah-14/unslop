# Agent #23 — StyleShield + RateAudit

**Topic:** Continuous embedding-space style transfer + document-level detection-rate gaming  
**Paper:** Zheng, *StyleShield: Exposing the Fragility of AIGC Detectors through Continuous Controllable Style Transfer* (arXiv:2605.00924, May 2026)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop Phase 3 / anti-detector policy

---

## Executive summary

StyleShield is a **diagnostic adversarial probe**, not a consumer humanizer. Guantian Zheng frames it as an independent audit of AIGC detectors deployed in Chinese academic integrity markets (CNKI, Weipu, Wanfang). The method performs **AI→human style transfer in continuous token-embedding space** using flow matching on a LangFlow-pretrained DiT backbone (~85M params), with zero-initialized cross-attention adapters conditioned on frozen Qwen-2.5-7B-Instruct (layer 14). A single inference knob **γ** (SDEdit noise level, swept 5.0–7.5) traces a smooth Pareto frontier between semantic preservation and detector evasion — something discrete-token rewrites cannot do continuously.

On a **Chinese-only** benchmark (436K training pairs, 1K held-out eval across social media / news / academic), StyleShield at **γ=7.0** reports **94.6% Evade@0.5** on the training BERT detector (Det-v3), **≥99%** on three held-out BERT/GPT-2 detectors, and **0.928** Qwen embedding cosine similarity. Baselines fail or trade badly: synonym substitution (0% evasion), LLM rewrite via same Qwen-7B (0.3% evasion), backtranslation (82.6% evasion but 0.852 similarity). The paper's counterintuitive quality signal: output PPL **~21** exceeds human reference **~16.5**, which exceeds AI original **~10.7** — detectors exploit low-entropy regularity; StyleShield injects human-like variability.

**RateAudit** is the second contribution: a greedy chunk scheduler that rewrites only the highest-P(AI) ≤512-token windows until a **document-level aggregate score** hits any pre-specified target (10%–60% tested). Mean deviation from target **≤1.4 pp** (e.g., 10.1±0.8% for a 10% target). Original docs start at **98.7%** mean P(AI). The authors argue this disqualifies percentage-based verdicts as evidence in consequential decisions.

**unslop verdict:** StyleShield is **not adoptable** as shipped tech (128×A800 training, Chinese LangFlow vocab, BERT detector in loop, no English/commercial eval). Two concepts **are** adoptable: (1) **γ-as-intensity-tier** — map `subtle`/`balanced`/`full`/`anti-detector` to increasing distributional perturbation budgets with explicit semantic stop rules; (2) **RateAudit as critique, not feature** — document that window-aggregated percentages are gameable; **never ship score-targeting scheduling** in anti-detector mode. Use RateAudit findings in Boundaries, README honesty, and the May detector-test article — not in `humanize.py`. Phase 3 intensity tiers and detector feedback should treat TMR/window scores as **diagnostic**, not optimizable targets.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv abstract)** | https://arxiv.org/abs/2605.00924 |
| **Paper (HTML v1)** | https://arxiv.org/html/2605.00924v1 |
| **DOI** | https://doi.org/10.48550/arxiv.2605.00924 |
| **Interactive digest (geepity)** | https://geepity.com/2605.00924/ |
| **Third-party summary (Pith)** | https://pith.science/paper/2605.00924 |
| **Official code (GitHub)** | https://github.com/Ethan-Zheng136/StyleShield |
| **LangFlow backbone paper** | https://arxiv.org/abs/2604.11748 |
| **LangFlow code** | https://github.com/nealchen2003/LangFlow |
| **Rest of World — CNKI detector workaround culture** | https://restofworld.org/2025/ai-detector-software-workaround |
| **Sun 2025 — AI detection controversies (CN)** | http://www.csstoday.net/News/Inchina/202508/t20250801_5908569.shtml |

### Comparison papers (shared evasion / detection lineage)

| Paper | URL | Relation to StyleShield |
|-------|-----|-------------------------|
| **MASH** (Gu et al., ACL Findings 2026) | https://arxiv.org/abs/2601.08564 | Discrete-token style humanization + DPO; no continuous γ axis |
| **HIP** (Xu et al., 2605.19516) | https://arxiv.org/abs/2605.19516 | Iterative base-model paraphrase; commercial detector eval; no embedding diffusion |
| **TempParaphraser** (EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1607/ | Sentence-level multi-round; discrete tokens |
| **Diffusion-LM** (Li et al., NeurIPS 2022) | https://arxiv.org/abs/2205.14217 | Embedding-space generation ancestor |
| **SDEdit** (Meng et al., ICLR 2022) | https://arxiv.org/abs/2108.01073 | Image edit paradigm adapted to text embeddings |
| **Krishna paraphrase evasion** (NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Paraphrase breaks detectors; retrieval defense partial |
| **Sadasivan impossibility** | https://arxiv.org/abs/2303.11156 | TV-distance frame; StyleShield cites §1 |
| **MGTBench** (He et al., ACL 2024) | https://arxiv.org/abs/2303.13408 | Detector benchmark culture |
| **Why AI Detection Fails** (2603.23146) | https://arxiv.org/abs/2603.23146 | AUROC skepticism; aligns with RateAudit thesis |
| **DAMAGE humanizer audit** | https://arxiv.org/abs/2501.03437 | Commercial humanizer honesty |

**Citation note:** arXiv ID **2605.00924** (submitted May 2026). Single author: **Guantian Zheng** (guantianzheng136@gmail.com). GitHub README lists **EMNLP 2026 submission**; arXiv title emphasizes "Exposing the Fragility" — diagnostic framing, not product marketing.

---

## StyleShield mechanism

### Architectural stack

```
AI text input
  → Qwen-2.5-7B-Instruct (frozen, layers 0–13) → H_qwen semantic condition
  → LangFlow vocab embed → e_AI
  → SDEdit: noise at γ_start → z_0
  → 64-step EDM Euler denoise (DiT 12-block, d=768, ~85M + ~28M adapter params)
       └── cross-attention adapters (zero-init gates) attend to projected H_qwen each block
  → argmax decode → human-styled text
```

| Component | Detail |
|-----------|--------|
| **Backbone** | 12-block DiT, flow matching objective, pretrained on Chinese via LangFlow (Chen et al., 2604.11748) |
| **Conditioning** | Zero-initialized cross-attention after each self-attention block; Qwen hidden states at **layer 14/28** projected 3584→768 |
| **Trainable params** | ~113M total; Qwen 7B fully frozen |
| **Training data** | 436K (AI, human) pairs: social media 346K, news 68K, academic 22K; dual-end filter P_AI(human)<0.1, P_AI(AI)>0.9 |
| **Loss** | Denoising CE on human target + detector reward λ_det=0.1 after 5K warmup (Det-v3 BERT) |
| **Inference** | SDEdit on embeddings; γ_start ∈ [5.0, 7.5]; T=64 Euler steps; ~6 s/sample on A800 |
| **Compute** | 128×A800 DDP, 100K steps (~48 h main run); checkpoint step 30K selected |

### The γ dial (continuous evasion–preservation axis)

γ is the SDEdit starting noise level. Higher γ = more embedding perturbation before denoising = stronger style shift.

| γ | P_AI (Det-v3) | Evade@0.5 | Sem.Sim | PPL |
|---|---------------|-----------|---------|-----|
| 5.0 | 0.703 | 30.1% | 0.948 | 30.1 |
| 6.0 | 0.301 | 52.6% | 0.942 | 20.3 |
| 6.5 | 0.124 | 79.7% | 0.935 | 21.1 |
| **7.0** | **0.072** | **94.6%** | **0.928** | **21.2** |

Key properties (§5.1):
- **Monotonic:** P_AI drops 89.8% relative from γ=5.0→7.0; similarity loses only 2.1% relative.
- **Pareto-dominates backtranslation** at every operating point.
- **Cross-detector at γ=6.0 already >92%** evasion on all three unseen detectors — moderate γ suffices for transfer.

### Critical ablations (what actually matters)

| Variant | Finding |
|---------|---------|
| **A5: no Qwen conditioning** | 99.9% evasion but Sim 0.731, PPL 132 — evasion via content destruction, not style transfer |
| **A3/A4: Qwen layer 7 vs 21** | Near-perfect evasion but catastrophic PPL or worst similarity — mid-layer 14 is optimal |
| **A2: no detector reward** | Comparable evasion (92.4% vs 94.6%) but PPL 26.1 vs 21.2 — reward is **quality regularizer**, not evasion driver |
| **A1: single-domain only** | Slightly worse evasion + similarity — multi-domain training helps |

**Mechanistic insight:** StyleShield learns **distributional style shift** (raise PPL, inject idiosyncrasy) while Qwen conditioning anchors semantics. Without conditioning, the model fools detectors by breaking text — a warning for any humanizer that optimizes detector score without preservation contracts.

---

## RateAudit mechanism

RateAudit targets **document-level percentage verdicts** — the UX most academic platforms expose (e.g., "your thesis is 47% AI-generated").

### Algorithm (Appendix B)

Given document D, target rate r_target, tolerance ε=0.02:

1. **Segment** into chunks ≤512 tokens (matches detector windowing).
2. **Score** each chunk P_AI(c_i); aggregate weighted mean s̄ = Σ w_i P_AI(c_i), w_i = |c_i|/|D|.
3. **Allocate** — while s̄ > r_target + ε:
   - Pick chunk j = argmax P_AI(c_i)
   - Try StyleShield rewrite with γ ∈ {6.0, 6.5, 7.0, 7.5}; accept first that lowers chunk score
   - Recompute s̄
   - Overshoot-skip: stop if s̄ < r_target − ε
4. **Return** reassembled document.

### Empirical results (50 docs, 8K–12K chars, ~23 chunks each)

| Target rate | Achieved P_AI (%) | Chunks rewritten | Rewrite ratio | Time (s/doc) |
|-------------|-------------------|------------------|---------------|--------------|
| 10% | 10.1 ± 0.8 | 19.6 / 23 | 88.7% | 271 ± 18 |
| 20% | 21.3 ± 1.2 | 16.8 / 23 | 75.4% | 232 ± 21 |
| 30% | 30.5 ± 1.4 | 14.7 / 23 | 66.1% | 204 ± 19 |
| 40% | 40.8 ± 1.1 | 12.9 / 23 | 57.8% | 179 ± 16 |
| 50% | 50.2 ± 0.9 | 10.8 / 23 | 48.6% | 150 ± 14 |
| 60% | 60.7 ± 1.3 | 8.2 / 23 | 37.1% | 112 ± 12 |

Original documents: mean P_AI **98.7%**. Even aggressive targets (10%) require rewriting most chunks — but the **principle** holds: the aggregate number is a **budget allocation problem**, not a forensic measurement. A doc reported at 60% can be scheduled to 10% (or vice versa) with bounded error.

### Why this matters for unslop

Commercial detectors (Turnitin, GPTZero, Originality) expose **document- or span-level percentages**. RateAudit proves that any such scalar is:

- **Sensitive to window aggregation** (which chunks count, how weights apply)
- **Manipulable by localized rewrite** without global semantic change
- **Non-identifiable** — same prose can present multiple "true" rates depending on rewrite schedule

UPDATE-PLAN-2026-08 explicitly flags **"RateAudit trust crisis"** as a cross-cutting doc fix. unslop should cite this when explaining why anti-detector mode **does not** optimize toward a target detector score.

---

## StyleShield vs MASH vs HIP vs TempParaphraser

| Dimension | **StyleShield** | **MASH** | **HIP** | **TempParaphraser** |
|-----------|-----------------|----------|---------|---------------------|
| **Representation** | Continuous embeddings | Discrete tokens | Discrete tokens | Discrete tokens |
| **Controllability** | Single γ, smooth spectrum | Stage pipeline + DPO | Iteration count N | Sentence rounds |
| **Semantic anchor** | Frozen Qwen cross-attention | Style vectors + refinement | AI→human LoRA pairs | 1B paraphraser |
| **Detector coupling** | BERT reward in training | DPO against detector scores | None (detector-agnostic) | None |
| **Eval detectors** | 4 Chinese BERT/GPT-2 | 5 black-box (mixed) | GPTZero, Pangram | Open academic |
| **Language** | Chinese only | English-focused | English | English |
| **Evasion headline** | 94.6% @ γ=7.0 (Det-v3); ≥99% transfer | ~92% ASR avg | Best commercial Pareto | 82.5% accuracy drop |
| **Unique claim** | Continuous γ + RateAudit | Detector-aligned DPO | Base-model human-likeness | Temperature simulation |
| **Adoptable without GPU farm?** | **No** | **No** | Partial (API iter) | Partial (sentence pick) |

### Mechanistic contrast

- **StyleShield:** Detectors read **narrow statistical manifolds** (low PPL, regular syntax). Fix: **continuous embedding flow** that injects human-like entropy while Qwen gates meaning — discrete rewrites can't sweep intensity smoothly.

- **MASH:** Detectors read **style feature vectors**. Fix: explicit style transfer + detector-boundary alignment via DPO.

- **HIP:** Detectors read **instruction-tuning artifacts + AI-origin context**. Fix: base-model iterative paraphrase toward human targets.

- **TempParaphraser:** Detectors read **temperature-sensitive token distributions**. Fix: multi-pass normal-temp paraphrase widens entropy.

**No head-to-head table exists.** StyleShield never evaluated GPTZero, Turnitin, or English text. HIP never evaluated embedding diffusion. Cross-paper ranking is speculative; for unslop's English/commercial audience, StyleShield is **evidence about detector epistemology**, not a deployment recipe.

---

## Who agrees, who pushes back

### Aligns with StyleShield / RateAudit thesis

| Actor | Position |
|-------|----------|
| **Sadasivan et al. (2023)** | Paraphrase/TV reduction breaks detectors — StyleShield is a high-fidelity instance with explicit controllability |
| **Krishna et al. (2023)** | Paraphrase evades; StyleShield shows LLM rewrite baseline fails (0.3%) while embedding transfer succeeds |
| **Why AI Detection Fails (2026)** | Flat metrics mislead — RateAudit attacks the **percentage UX** directly |
| **DAMAGE / commercial audit line** | Detection + humanization same supply chain — Zheng's CNKI pricing table (641 USD/M tok vs Qwen-Turbo 0.10) |
| **Rest of World (2025)** | Chinese students already game detectors — StyleShield formalizes the mechanism |
| **Liang / ESL false-positive literature** | High-stakes classifier errors — Zheng cites 5–12% FPR and degree-revocation thresholds |
| **unslop Boundaries** | Anti-detector for ESL/resume defense, not misconduct — StyleShield ethics statement compatible |

### Partial agreement / limits

| Actor | Position |
|-------|----------|
| **Detector vendors (GPTZero, Turnitin, CNKI)** | Will retrain on StyleShield outputs; paper acknowledges arms race but argues premise is flawed |
| **MGTBench / RAID eval culture** | StyleShield uses custom Chinese BERT detectors — not comparable to commercial benchmark numbers |
| **DivEye / TSD / SurpMark (2026 detection)** | May survive embedding style shift — **untested** in StyleShield; unslop ships DivEye proxies |
| **Tulchinskii PHD** | Geometry-based ID may behave differently under flow-matching — unknown |
| **Retrieval defense (Krishna 2023)** | StyleShield doesn't test retrieval-augmented detection |

### Disagrees or reframes

| Actor | Position |
|-------|----------|
| **StyleShield author (explicit)** | Not built to help cheat — built to **disqualify percentage scores as legal/academic evidence** |
| **Academic integrity policy** | Process-based assessment (drafts, oral defense) over origin classification — Zheng §Ethics recommends this |
| **unslop UPDATE-PLAN** | **Do not ship RateAudit-style score targeting** — document trust crisis, don't implement gaming |
| **Chakraborty multi-sample detection** | Account-level signals may resist chunk-local rewrite — RateAudit is single-doc, single-detector |

---

## GitHub and artifact availability

**Repo:** https://github.com/Ethan-Zheng136/StyleShield

| Artifact | Status (Aug 2026) |
|----------|-------------------|
| Training code (`train_styleflow.py`) | Shipped |
| Inference (`transfer.py`) | Shipped |
| RateAudit (`allocator_sf.py`) | Shipped |
| Eval (`eval_acl.py`) | Shipped |
| Checkpoints | HuggingFace "upon acceptance"; README lists `step_30000.pt` + ablations |
| Requirements | `pip install -r requirements.txt` |
| License | MIT (README); Apache-2.0 on alternate branch metadata |
| Maturity | ~1 star; EMNLP 2026 submission; single-author independent research |

**Repro barrier:** 128×A800 training cluster; Chinese LangFlow vocab (64K BPE); Det-v3 BERT detector for reward (not public commercial API). Inference alone needs A800 + checkpoint + Qwen-7B for conditioning.

**LangFlow dependency:** Separate project (Chen et al., 2604.11748) — continuous diffusion LM, not the Langflow agent-builder product. PPL 30.0 LM1B / 24.6 OWT.

---

## Evaluation caveats (read before citing numbers)

1. **Chinese only** — authors state English generalization unvalidated (§Limitations).
2. **BERT-family detectors** — Det-v3 (train), Det-v2, ANX-BERT, GPT2-Det. **No GPTZero, Pangram, Turnitin, Originality.**
3. **Same-model paradox** — LLM Rewrite baseline uses Qwen-2.5-7B-Instruct (0.3% evasion); StyleShield conditions on same model yet evades — the win is **embedding flow + training objective**, not "different model."
4. **Synthetic AI side** — training pairs created by prompting Qwen to rewrite human text into AI style, then filtered. Real ChatGPT/Claude prose may differ.
5. **Automatic metrics only** — semantic similarity via Qwen embeddings; no human naturalness study at scale.
6. **Detector in training loop** — requires target detector access; generalization to unseen BERTs is strong but commercial transfer unproven.
7. **RateAudit uses same StyleShield + same Det-v3** — gaming demonstrated against one aggregation scheme; other vendors may use different windowing/normalization.

---

## unslop integration

### What to adopt

| Concept | unslop mapping | Phase |
|---------|----------------|-------|
| **γ intensity spectrum** | Map `/unslop subtle` → minimal distributional nudge; `balanced` → structural + soul; `full` → LLM rewrite; `anti-detector` → max budget with preservation contract | Phase 1–3 (conceptual; already partially exists) |
| **PPL/surprisal as signal** | StyleShield validates DivEye thesis — detectors exploit low variance; wire `surprisal.py` into feedback (UPDATE-PLAN Phase 1) | Phase 1 |
| **RateAudit as documentation** | Explain why `detector.py` TMR is diagnostic, not a target; cite in Boundaries + May detector-test article | Phase 0 docs |
| **Zero-init semantic anchor** | Analog: `validate.py` preservation + voice-match profile as "conditioning" that prevents meaning drift during aggressive passes | Existing |
| **Detector reward as quality gate** | Analog: use TMR **rise** or semantic validator failure as stop rule, not sole optimization objective (A2 ablation lesson) | Phase 1 detector loop |

### What NOT to adopt

| StyleShield feature | Why unslop refuses |
|---------------------|-------------------|
| **RateAudit score targeting** | UPDATE-PLAN: "Do not ship watermark removal, **score-gaming (RateAudit)**, or beat Turnitin marketing" |
| **Flow matching in embedding space** | Requires LangFlow + DiT training stack; out of scope for deterministic/API plugin |
| **Detector-in-loop training** | Needs fine-tune infrastructure + target detector weights |
| **γ=7.0 as default** | Aggressive setting trades 7.2% semantic similarity; unslop preservation contract is byte-exact for code/URLs |
| **Chinese-only checkpoints** | English users need English evidence chain (HIP, MASH, TempParaphraser) |

### Recommended architecture touchpoints

```
Input text
  → deterministic passes (intensity tier ≈ low γ)
  → [optional] LLM pass with escalating prompt aggressiveness (mid γ analog)
  → validate.py preservation — hard stop if semantic anchors fail
  → [optional] detector.feedback_loop — use TMR delta as DIAGNOSTIC only
  → NEVER: greedy chunk rewrite until TMR ≤ target  ← RateAudit forbidden
```

**Documentation snippet for SKILL.md / Boundaries:**

> Window-level and document-level AI percentages can be shifted by localized rewriting (Zheng 2026, RateAudit). unslop does not optimize toward a target detector score. Anti-detector mode reduces AI-ism and distributional uniformity; it does not guarantee any vendor metric.

### γ → unslop intensity mapping (conceptual, not literal)

| StyleShield γ | P_AI reduction | Sem.Sim | unslop analog |
|---------------|----------------|---------|---------------|
| 5.0–5.5 | Mild | ~0.947 | `subtle` / `balanced` — regex, stock vocab |
| 6.0–6.5 | Moderate | ~0.935–0.942 | `full` — structural + soul + LLM |
| 7.0 | Strong | 0.928 | `anti-detector` — max deterministic + optional cross-model LLM pipeline |

unslop cannot replicate embedding-space continuity; intensity tiers remain **discrete steps**. The StyleShield lesson is to **document the trade-off explicitly** rather than pretend one pass fixes all signals.

---

## Policy and market context (from paper §Ethics)

Zheng embeds a cost comparison (Table 5, early 2026):

| Service | USD / M output tokens | vs Qwen-Turbo |
|---------|----------------------|---------------|
| CNKI detection | 641 | 6,410× |
| Weipu / Wanfang | 427 | 4,270× |
| PaperPass | 321 | 3,210× |
| GPT-4o generation | 10 | 100× |
| Qwen-Turbo generation | 0.10 | 1× |

Detection priced **orders of magnitude above generation** while robustness was unaudited — the economic motive for StyleShield's release. False-positive anecdotes include classical Chinese texts flagged >50% AI and ethnographic fieldwork flagged at a top Chinese university (Sun 2025; Rest of World 2025).

**Recommended policy (authors):** process-based assessment, mandatory vendor error-rate disclosure, quality-centered evaluation. unslop aligns on **origin ≠ quality** without endorsing evasion for academic misconduct.

---

## Key numbers quick reference

| Metric | Value | Source |
|--------|-------|--------|
| Training pairs | 436K Chinese (AI→human direction) | §4.1 |
| Eval set | 1,000 balanced samples | §4.1 |
| Best operating point | γ=7.0 | §4.2 |
| Evade@0.5 (Det-v3, γ=7.0) | 94.6% | Table 1 |
| Evade@0.5 (unseen avg, γ=7.0) | ≥99% | Table 2 |
| Semantic similarity (γ=7.0) | 0.928 | Table 1 |
| Output PPL vs human vs AI | 21.2 vs 16.5 vs 10.7 | §5.2 |
| LLM Rewrite baseline evasion | 0.3% | Table 1 |
| RateAudit target precision | ≤1.4 pp mean deviation | Table 4 |
| RateAudit original doc P_AI | 98.7% mean | §4.5 |
| Trainable params | ~113M (+ frozen 7B Qwen) | §4.1 |
| Inference latency | ~6 s / 512 tokens (A800) | §4.1 |

---

## Open questions for unslop bench

1. Does **English** prose show the same γ-monotonic PPL inversion after deterministic + LLM anti-detector passes?
2. Do **GPTZero v6 predictability cones** resist chunk-local rewrite (RateAudit analog on English Turnitin/GPTZero)?
3. Does **DivEye variance** increase monotonically with unslop intensity tiers the way PPL rises with γ?
4. Can **voice-match** profile act as Qwen-conditioning analog — preserving author idiosyncrasy while shifting detector statistics?
5. Would **HIP iterative paraphrase + StyleShield-style intensity dial** compose, or saturate the same manifold?

---

## Bottom line

StyleShield is the strongest 2026 demonstration that **continuous embedding-space style transfer** breaks BERT-family AIGC detectors with a tunable evasion–preservation axis — and that **document percentages are schedulable artifacts**. RateAudit is the politically explosive half: it turns "your paper is 47% AI" from evidence into a **knob**.

For unslop: steal the **γ tier mental model** and the **RateAudit trust critique**; do not steal the **allocator** or market anti-detector mode as score minimization. Ship honest docs. Keep anti-detector mode bounded to ESL/resume use cases. Treat commercial detector screenshots as **single-point samples**, not contracts — because RateAudit proves the aggregate can be renegotiated.

---

## Internal cross-links

| Doc | Relevance |
|-----|-----------|
| `AGENT-22-HIP.md` | Closest English/commercial evasion comparator |
| `AGENT-24-TEMPPARAPHRASER.md` | Discrete multi-round alternative |
| `AGENT-25-ADVERSARIAL-PARAPHRASING.md` | Detector-guided discrete rewrite |
| `AGENT-16-SHIELD-BENCHMARK.md` | Hardness-aware eval StyleShield didn't use |
| `AGENT-17-SADASIVAN-IMPOSSIBILITY.md` | Theoretical paraphrase frame |
| `UPDATE-PLAN-2026-08.md` | γ dial → intensity tiers; RateAudit trust crisis |
| `unslop/scripts/surprisal.py` | PPL/variance signal StyleShield empirically validates |
| `unslop/scripts/detector.py` | TMR feedback — diagnostic only post-RateAudit |
