# Agent #27 — AuthorMist (RL Paraphrase vs Commercial Detector APIs)

**Topic:** David & Gervais, *AuthorMist: Evading AI Text Detectors with Reinforcement Learning* (arXiv:2503.08716)  
**Prepared:** August 19, 2026  
**Scope:** API-as-reward GRPO humanizer, authorship-obfuscation lineage, HF weights, StealthRL/TH-Bench benchmarks, privacy-vs-integrity debate, unslop voice-match boundary  
**Status:** complete

---

## Executive summary

AuthorMist (March 2025, University College London — Isaac David, Arthur Gervais) is the first published system to fine-tune a paraphrase policy with **commercial detector APIs inside the RL reward loop**. It trains six detector-specific variants of Qwen2.5-3B-Instruct via **Group Relative Policy Optimization (GRPO)**, then at inference generates **8 candidates per chunk** and picks the one with the lowest detector score.

**Headline numbers:** Attack success rates **78.6%–96.2%** against individual detectors on a 300-pair XSum eval set; semantic similarity **>0.94** (E5-small cosine); mean AUROC **0.49** for the Originality.ai-trained variant across six detectors. Beats DIPPER and a same-data SFT ablation on evasion while preserving meaning.

**Authorship obfuscation angle:** The paper explicitly borrows from stylometry/authorship-obfuscation literature (Anonymouth, BPSO obfuscation) but **re-targets the objective**: hide **AI-generation fingerprints**, not a named human author's idiolect. That makes AuthorMist closer to **anti-detector humanization** than to StyleRemix/TinyStyler-style voice transfer — and directly in tension with unslop **voice-match**, which optimizes fidelity to a *user sample*, not minimization of GPTZero probability.

**Code reality:** Training code **not released**. Only **`authormist/authormist-originality`** on HuggingFace (MIT, ~1.2k downloads/month as of Aug 2026). StealthRL (Feb 2026) re-benchmarks AuthorMist as attack method **M4** and shows **multi-detector ensemble RL (M2) beats single-detector RL (M4)** at TPR@1%FPR.

**unslop verdict:** AuthorMist is the academic reference for "detector API as reward oracle" — the threat model behind commercial humanizer SaaS, open-sourced as a weight file. unslop should **cite it as the upper bound on single-detector RL paraphrase**, **not integrate its weights**, and **never conflate voice-match with AuthorMist-style evasion**. For ESL false-positive defense, unslop stays at T1–T2 (deterministic + prompted anti-detector); AuthorMist is T3 (trained adversary). Optional benchmark adapter only.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | AuthorMist: Evading AI Text Detectors with Reinforcement Learning |
| **Authors** | Isaac David, Arthur Gervais (corresponding: Arthur Gervais) |
| **Affiliation** | University College London |
| **Posted** | 10 March 2025 |
| **arXiv** | https://arxiv.org/abs/2503.08716 |
| **DOI** | https://doi.org/10.48550/arxiv.2503.08716 |
| **HF Papers** | https://huggingface.co/papers/2503.08716 |
| **Code** | **Not released** (training pipeline proprietary / unreleased) |
| **Model artifact** | https://huggingface.co/authormist/authormist-originality |
| **License (weights)** | MIT |
| **One-line contribution** | First "API-as-reward" GRPO humanizer: external detector scores (commercial + open) directly optimize a 3B paraphrase policy |

**Title note:** Some unslop compendium entries use *AuthorMist: A Reinforcement Learning Approach to Text Privacy Enhancement* — that subtitle does not appear on the arXiv record. Use the arXiv title above for citations.

**Author context:** Gervais (h-index ~30) is a long-standing web-privacy / NLP researcher (quantifying web-search privacy, CCS 2014). The paper frames evasion as **author privacy** and **freedom from unfair AI-assistance stigma**, extending Liang et al.'s ESL false-positive critique — not as an academic-dishonesty tool. That framing is load-bearing for the public debate section below.

---

## 2. Method — API-as-reward GRPO

### 2.1 Threat model

| Dimension | Specification |
|-----------|---------------|
| **Attacker capability** | Black-box detector probability scores (API or HF inference). No gradient access. |
| **Attacker goal** | Paraphrase AI text \(y\) from input \(x\) so mean detector \(P_{\text{AI}}(y) \to 0\) while semantic similarity stays high. |
| **Attacker constraint** | Fluent paraphrase, not homoglyph corruption (contrast SilverSpeak / M5). |
| **Training** | Offline RL with detector queries during GRPO rollouts. |
| **Inference** | **8 candidates per 512-token chunk**; select lowest mean detector score. Test-time reranking resembles a stripped Adversarial Paraphrasing search but with a **fixed RL policy** generating candidates. |

### 2.2 Reward

For detectors \(D = \{d_1,\ldots,d_k\}\) with AI probability outputs \(P_{d_j}(Y)\):

\[
R(X,Y) = 1 - \frac{1}{k}\sum_{j=1}^{k} P_{d_j}(Y)
\]

Training uses **one detector per model** (six separate fine-tunes). Evaluation is **cross-detector** (full 6×6 matrix).

**KL regularization:** \(\beta = 0.001\) against the frozen Qwen2.5-3B-Instruct reference — anchors fluency and limits semantic drift.

### 2.3 Training stack

| Parameter | Value |
|-----------|-------|
| Base model | `Qwen/Qwen2.5-3B-Instruct` |
| Algorithm | GRPO (group size G; relative advantage vs group mean) |
| Learning rate | \(5 \times 10^{-5}\) |
| Epochs | 1 (714 steps) |
| Hardware | 8× NVIDIA H100, ~2 h / model, **16 GPU-hours each** |
| Training data | 10,000 CheckGPT human abstracts → AI paraphrases via GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 |
| Domains | CS, HSS, Physics; 100–500 words (median ~250) |
| Eval data | 300 XSum summaries → AI paraphrases (same three LLMs); 300 human controls |

**Detectors in training/eval panel:**

| Detector | Type | Role |
|----------|------|------|
| GPTZero | Commercial API | Reward target + eval |
| Winston.ai | Commercial API | Reward target + eval |
| Originality.ai | Commercial API | Reward target + eval; **best generalizer** |
| Sapling | Commercial API | Reward target + eval |
| HelloSimpleAI | Open HF classifier | Reward target + eval |
| OpenAI RoBERTa detector | Open HF classifier | Reward target + eval |

### 2.4 Mechanism of evasion (paper's own analysis)

AuthorMist learns to **raise perplexity** toward human ranges. Original AI text median PPL ~25–40 (GPT-2); human ~50–75; paraphrased outputs shift right — HelloSimpleAI and Originality variants reach PPL 300–400 on some samples. Same axis as burstiness/surprisal literature (DivEye, Fast-DetectGPT curvature): break low-predictability machine signature while KL keeps text readable.

**Not authorship obfuscation in the stylometric sense:** The policy does not receive an author embedding or style profile. It receives **detector scores only**. Any "human-like" style is **whatever minimizes commercial API probability**, which may converge to generic fluent paraphrase — not the user's idiolect.

---

## 3. Results (paper Table 1–4, Figures 2–5)

### 3.1 Attack Success Rate (ASR %) — cross-detector matrix (selected)

Diagonal = trained target; off-diagonal = transfer.

| Trained against → Eval on | GPTZero | OpenAI RoBERTa | HelloSimpleAI | Sapling | Originality | Winston | **Mean ASR** |
|---------------------------|---------|----------------|---------------|---------|-------------|---------|--------------|
| **GPTZero** | **92.33** | 19.33 | 82.33 | 99.00 | 44.00 | 100.00 | 72.83 |
| **OpenAI** | 2.00 | **95.67** | 81.67 | 2.33 | 0.00 | 12.33 | 32.33 |
| **HelloSimpleAI** | 10.00 | 42.33 | **97.67** | 23.00 | 0.33 | 72.67 | 41.00 |
| **Sapling** | 41.33 | 85.00 | 94.67 | **98.33** | 8.33 | 99.00 | 71.11 |
| **Originality** | 83.67 | 93.33 | **100.00** | **100.00** | **94.00** | **100.00** | **95.17** |
| **Winston** | 86.00 | 52.33 | 98.33 | 97.00 | 68.33 | **100.00** | 83.67 |

**Takeaways:**

1. **Originality-trained variant** is the paper's recommended generalist: 95.17% mean ASR, mean AUROC 0.49, mean F1 0.09.
2. **GPTZero and Originality detectors are harder to collapse** off-diagonal — GPTZero-trained model still leaves GPTZero AUROC ~0.79 on cross-eval; Originality.ai shows "greater resilience" in ROC plots.
3. **HelloSimpleAI** is easiest to push below random (AUROC 0.07–0.09 when targeted).

### 3.2 Semantic preservation

| Metric | Value |
|--------|-------|
| E5-small cosine similarity | Median **>0.94** all variants; lowest outliers **>0.87** |
| OpenAI-trained variant | Highest median ~**0.975** |
| vs SFT ablation | GRPO Originality F1 0.11 vs SFT 0.90 on Originality detector |

### 3.3 vs baselines (Table 4 — Originality-trained AuthorMist)

| Method | Mean AUROC | Mean ASR | Mean F1 |
|--------|------------|----------|---------|
| Unparaphrased Qwen2.5-3B | 0.86 | 4% | — |
| **AuthorMist (Originality GRPO)** | **0.49** | **95.17%** | **0.09** |
| DIPPER | 0.83 | 40% | 0.42 |
| AuthorMist (SFT only) | 0.68 | 65% | 0.42 |

GRPO + detector reward is **load-bearing**; SFT on the same pairs without RL retains most detector discriminability.

### 3.4 Abstract-range headline

Paper abstract reports **78.6%–96.2% ASR against individual detectors** — the spread across the six specialist models and eval conditions, not a single universal number.

---

## 4. Code, weights, and reproducibility

| Asset | Status | URL |
|-------|--------|-----|
| Paper + appendix | ✅ Public | https://arxiv.org/abs/2503.08716 |
| Training code / GRPO recipe | ❌ Not released | — |
| Detector API integration code | ❌ Not released | — |
| **AuthorMist Originality weights** | ✅ HF | https://huggingface.co/authormist/authormist-originality |
| Other five detector-specific checkpoints | ❌ Not on HF (as of Aug 2026) | Paper describes six models; only Originality published |
| Demo / API hosting | Third-party | Featherless AI inference listing |

**Reproducibility grade: medium.** Methodology is detailed enough to replicate in principle (GRPO + API rewards + Qwen2.5-3B), but **detector API costs**, **undisclosed prompts**, and **missing training code** block exact reproduction. Re-implementing requires paid GPTZero/Originality/Winston quotas during RL — the paper's core dependency.

**HF usage pattern (from model card):**

```python
prompt = f"""Please paraphrase the following text to make it more human-like while preserving the original meaning:

{ai_text}

Paraphrased text:"""
# generate with temperature=0.7, top_p=0.9, max_new_tokens=512
```

**Repo doc correction:** `docs/research/15-academic-papers-llm-humanization/A-academic.md` §1.9 claims AuthorMist "adds a grammar-correction post-step." **The arXiv paper contains no grammar-correction stage** — only GRPO paraphrase + 8-way detector rerank at inference. Treat that bullet as a compendium error until a source is found.

---

## 5. Benchmark placement

### 5.1 StealthRL M4 (canonical external re-benchmark)

StealthRL (Ranganath & Ramesh, arXiv:2602.08934, Feb 2026) slots AuthorMist as **M4** in a unified MAGE eval at **TPR@1%FPR**:

| Method | Mean TPR@1%FPR | Mean ASR | Notes |
|--------|----------------|----------|-------|
| M0 No attack | 0.450 | 0.550 | — |
| M1 Simple paraphrase | 0.284 | 0.716 | — |
| M3 Adversarial Paraphrasing | 0.217 | 0.783 | Inference search |
| **M4 AuthorMist** | **0.203** | **0.797** | Single-detector RL (RoBERTa reward in StealthRL setup) |
| **M2 StealthRL** | **0.024** | **0.976** | Multi-detector ensemble GRPO |

AuthorMist is **strong but superseded** at strict FPR by ensemble RL (M2) and competitive with inference-time search (M3) on StealthRL's panel. It was **not** evaluated against Fast-DetectGPT, Binoculars, or DivEye in the original paper.

### 5.2 TH-Bench (arXiv:2503.08708)

TH-Bench evaluates six humanization attacks × 13 detectors × three axes (evasion, quality, compute). AuthorMist is in the attack taxonomy alongside DIPPER, RAFT, TempParaphraser, etc. **Headline TH-Bench finding:** no attack wins all three axes — AuthorMist likely leads on commercial API evasion while paying training cost and occasional quality/perplexity spikes.

### 5.3 DAMAGE / commercial humanizer audits

DAMAGE (Masrour et al., arXiv:2501.03437) ranks commercial humanizers qualitatively; research humanizers (AdvPara, AuthorMist, MASH) sit **20–30+ ASR points above** tier-1 SaaS. AuthorMist's **>0.94 similarity** is the semantic-preservation bar commercial tools rarely publish.

### 5.4 Suggested unslop eval protocol (research-only)

1. Run unslop T1 fixtures through `authormist/authormist-originality` adapter → GPTZero + TMR + optional Desklib.  
2. Report **TPR@1%FPR** where human negatives exist, not raw `p_ai` alone.  
3. Log **E5 similarity** and **stylometric delta** vs user sample when voice-match is enabled — expect **conflict** (detector reward ≠ profile fidelity).

---

## 6. Authorship obfuscation vs AI fingerprint masking

| Tradition | Target | Training signal | unslop analog |
|-----------|--------|-----------------|---------------|
| **Anonymouth / BPSO obfuscation** | Hide *named author* from stylometric classifier | Author-labeled corpus, feature suppression | Not shipped |
| **StyleRemix / TinyStyler** | Transfer to target author *style* | Style adapters / authorship embeddings | voice-match (prompt-only, weaker) |
| **AuthorMist** | Hide *AI origin* from detector | **Detector API probability** | anti-detector (prompt-only, much weaker) |
| **Jemama 2025** | Match author style | Few-shot / completion prompting | voice-match telemetry |

AuthorMist **cites** authorship obfuscation (refs 23–24: Shetty BPSO, Anonymouth) but **does not implement** author-specific obfuscation. The "Author" in AuthorMist is the **human writer unfairly accused**, not the **source author whose style is being mimicked**.

**Implication for voice-match:** Matching a user's contraction rate and sentence-length σ (unslop `stylometry.py`) is **orthogonal** to AuthorMist's reward. A voice-match rewrite that faithfully reproduces a low-σ ESL sample **increases** fidelity and may **increase** detector scores — the opposite of AuthorMist's optimum. See Agent #52 memo for the two-axis framework (style fidelity vs statistical naturalness).

---

## 7. Debate — privacy, integrity, dual-use

### 7.1 Authors' frame (pro-privacy)

- AI-assisted writing is widespread; detectors **over-flag** legitimate use (echoes Liang TOEFL false positives).  
- AuthorMist protects **author privacy** and prevents **discrimination against AI-assisted drafts** where assistance is permitted.  
- Recommends **transparent disclosure** of AI use where ethically required; positions detection as unsustainable arms race.  
- Suggests shifting from "who wrote this" to **content quality and appropriate attribution**.

### 7.2 Integrity / detector-vendor frame (critics)

- Same API-as-reward machinery enables **academic misconduct** at scale with **>0.94 meaning preservation** — harder to catch than homoglyph spam.  
- **Commercial detector APIs as training oracles** create a direct feedback loop: humanizers co-evolve with the same vendors educators pay.  
- **Single-vendor overfitting:** GPTZero-trained variant shows weak cross-transfer (92% on-target, poor on OpenAI RoBERTa off-diagonal). Arms race favors **ensemble attackers** (StealthRL M2).  
- **No watermark / provenance defense** — AuthorMist is post-hoc paraphrase; process-tracing tools (GPTZero Replay, Grammarly Authorship) are the institutional response.

### 7.3 Research community positioning

| Camp | Representative | Position on AuthorMist |
|------|----------------|------------------------|
| **Evasion researchers** | Cheng (AdvPara), Ranganath (StealthRL), Nicks (DPO humanizer) | AuthorMist validates detector-in-the-loop RL; superseded by ensemble training |
| **Robustness evaluators** | RAID/TH-Bench/DAMAGE | Use as attack slice; report operating-point metrics |
| **Impossibility theorists** | Sadasivan et al. | RL paraphrase approaches TV-reduction bound empirically |
| **ESL fairness** | Liang et al.; Perkins higher-ed studies | Privacy frame has merit for false positives; does not justify undisclosed cheating |
| **Reddit / ML Twitter** | r/MachineLearning threads (2025) | Grouped with AdvPara + DAMAGE as "serious academic humanization" |

### 7.4 unslop policy alignment

Matches `skills/unslop/SKILL.md` Boundaries:

- **Defensive use:** ESL false positives, resume polish — unslop anti-detector, **not** AuthorMist weights.  
- **Do not ship:** GRPO training against GPTZero API, HF AuthorMist integration in product path, or "Originality bypass" marketing.  
- **Do cite:** AuthorMist as evidence that **detector scores are not integrity proof** under adaptive paraphrase.

---

## 8. Lineage and comparison

```
DIPPER (Krishna NeurIPS 2023) — one-shot T5 paraphrase
    └── Nicks et al. (ICLR 2024) — DPO with detector reward, Llama-2-7B
            └── AuthorMist (Mar 2025) — GRPO + commercial API rewards, Qwen2.5-3B
                    ├── Adversarial Paraphrasing (Jun 2025) — inference-time token search, no weight update
                    ├── MASH (Jan 2026) — SFT→DPO→refinement, style manifold
                    └── StealthRL (Feb 2026) — multi-detector ensemble GRPO+LoRA, held-out transfer
```

| Paper | arXiv | Train cost | Inference | Semantic sim | Key difference from AuthorMist |
|-------|-------|------------|-----------|--------------|----------------------------------|
| DIPPER | 2303.13408 | Fine-tune 11B T5 | 1× paraphrase | High | No detector in training loop |
| Nicks DPO | 2404.07828 | DPO <1 day | 1× generate | PPL +0.2 | Single open detector reward |
| **AuthorMist** | **2503.08716** | **16 GPU-h × 6 models** | **8× rerank** | **>0.94** | **Commercial API rewards** |
| AdvPara | 2506.07001 | None | N× token search | ~0.97 | Training-free; beats AuthorMist at 1% FPR in StealthRL table |
| StealthRL | 2602.08934 | LoRA GRPO | 1× policy | ~0.90 | Ensemble reward; beats M4 |

---

## 9. unslop integration — voice-match, anti-detector, detector feedback

### 9.1 Mode mapping

| AuthorMist capability | unslop mode | Gap |
|----------------------|-------------|-----|
| Minimize GPTZero/Originality probability | `anti-detector` + `--detector-feedback` | unslop: prompt/regex + optional TMR ladder; **no weight update** |
| Preserve meaning (>0.94 E5) | LLM rewrite + `validate.py` preservation | Comparable goal; unslop enforces code/URL/heading byte preservation AuthorMist does not discuss |
| Match **user** idiolect | `voice-match` + `stylometry.py` | **AuthorMist does not optimize this**; may **destroy** voice fidelity |
| Raise perplexity / break AI rhythm | `structural.py`, `--surprisal-variance` | Same *axis*, orders of magnitude weaker than RL |
| 8-candidate detector rerank | `--detector-feedback` 5-step ladder | Similar *idea* at single-pass scale; no GRPO policy |

### 9.2 Voice-match conflict (critical)

**AuthorMist optimum:** \(\arg\min_Y \sum_j P_{d_j}(Y)\) subject to KL anchor.  
**Voice-match optimum:** \(\arg\min_Y \|\text{StyleProfile}(Y) - \text{StyleProfile}(\text{sample})\|\).

When the user's sample has **low burstiness, low contractions, low perplexity** (common ESL/L2 formal register):

- Voice-match instructs the model to **stay** in that basin.  
- AuthorMist / anti-detector instructs the model to **leave** it.  

**Do not merge the modes without explicit band constraints** (Agent #52 sequenced workflow): voice-match first for slop removal, then anti-detector with floors `max(sample_σ, 6)`, `max(sample_contractions, human_floor)` only when user opts into detector defense.

**AuthorMist is not a voice-match backend.** Feeding a user sample into `authormist-originality` **ignores** the sample — the model has no authorship embedding. unslop should never imply voice-match + AuthorMist weights ≈ "sound like me and pass GPTZero."

### 9.3 Threat-model tier

| Tier | Actor | AuthorMist relevance |
|------|-------|---------------------|
| **T1** | unslop deterministic + LLM polish | Not AuthorMist-class |
| **T2** | Cross-model manual paraphrase | Below AuthorMist ASR |
| **T3** | AuthorMist HF weights or retrained GRPO | **78–96% ASR** on commercial APIs in paper |
| **T4** | StealthRL ensemble RL | Strictly stronger at TPR@1%FPR |

### 9.4 What unslop should / should not do

**Should:**

1. Cite AuthorMist in README adversarial paragraph alongside AdvPara and StealthRL.  
2. Keep `--detector-feedback` framed as **local rewrite ladder**, not RL paraphrase.  
3. Document voice-match vs anti-detector conflict in `SKILL.md` (already started in Agent #52).  
4. Use AuthorMist similarity bar (**>0.94 E5**) when discussing semantic preservation in research docs.

**Should not:**

1. ❌ Bundle `authormist/authormist-originality` in the plugin.  
2. ❌ Train GRPO against GPTZero/Originality APIs inside unslop.  
3. ❌ Claim voice-match evades detectors AuthorMist was built to evade.  
4. ❌ Quote 95% ASR without noting detector-specific training and StealthRL M4 re-benchmark.

### 9.5 Optional engineering (research benchmark only)

| Action | Rationale |
|--------|-----------|
| Add `benchmarks/adapters/authormist.py` | Quantify T1 unslop vs T3 AuthorMist on shared fixtures |
| Log stylometric delta when running both | Empirical voice-match / evasion conflict data |
| Compare `--detector-feedback` exhaust vs 8-way rerank | Test whether ladder approximates inference rerank |

---

## 10. Limitations (paper §4.5 + Aug 2026 gaps)

**Authors acknowledge:**

- **Compute:** 16 GPU-hours per detector-specific model; impractical to retrain on every detector update.  
- **Semantic drift:** >0.94 average but technical/specialized text vulnerable to subtle meaning shifts.  
- **Cross-detector generalization:** OpenAI-reward model mean ASR only 32.33%; GPTZero remains partially resilient.  
- **API fragility:** Rate limits, format changes, downtime during training.  
- **Ethics:** Dual-use; advocate transparency.

**Not evaluated in original paper (Aug 2026 gaps):**

- Fast-DetectGPT, Binoculars, DivEye, TMR, Turnitin 2025–2026, GPTZero v6 predictability cones  
- Non-English text  
- Watermarked generations (SIRA / KGW)  
- Voice-match or authorship attribution after paraphrase  
- Long documents (>512-token chunks stitched)

---

## 11. Source index

### Primary

| Resource | URL |
|----------|-----|
| AuthorMist arXiv | https://arxiv.org/abs/2503.08716 |
| AuthorMist DOI | https://doi.org/10.48550/arxiv.2503.08716 |
| HF model (Originality) | https://huggingface.co/authormist/authormist-originality |
| HF Papers page | https://huggingface.co/papers/2503.08716 |
| CheckGPT dataset (training) | Liu et al. CCS 2024 — https://arxiv.org/abs/2401.08315 |

### Benchmarks & successors

| Resource | URL |
|----------|-----|
| StealthRL (M4 baseline) | https://arxiv.org/abs/2602.08934 |
| TH-Bench | https://arxiv.org/abs/2503.08708 |
| Adversarial Paraphrasing | https://arxiv.org/abs/2506.07001 |
| DIPPER | https://arxiv.org/abs/2303.13408 |
| DAMAGE commercial audit | https://arxiv.org/abs/2501.03437 |
| Nicks DPO humanizer | https://openreview.net/forum?id=4eJDMjYZZG |

### Authorship obfuscation lineage

| Resource | URL |
|----------|-----|
| StyleRemix (EMNLP 2024) | https://arxiv.org/abs/2408.15666 |
| TinyStyler | https://github.com/zacharyhorvitz/TinyStyler |
| Anonymouth (cited) | Brenner & Behrndt 2006 — PETS |

### unslop internal

| Resource | Path |
|----------|------|
| Voice-match limits memo | `docs/research/2026-08-detector-research/AGENT-52-VOICE-MATCH-STYLOMETRIC-LIMITS.md` |
| StealthRL memo (M4 row) | `docs/research/2026-08-detector-research/AGENT-26-STEALTHRL.md` |
| AdvPara memo | `docs/research/2026-08-detector-research/AGENT-25-ADVERSARIAL-PARAPHRASING.md` |
| stylometry.py | `unslop/scripts/stylometry.py` |
| detector feedback | `unslop/scripts/detector.py` |
| Research compendium | `docs/research/15-academic-papers-llm-humanization/C-opensource.md` §5 |

---

## 12. Citation (BibTeX)

```bibtex
@article{david2025authormist,
  title={AuthorMist: Evading AI Text Detectors with Reinforcement Learning},
  author={David, Isaac and Gervais, Arthur},
  journal={arXiv preprint arXiv:2503.08716},
  year={2025},
  url={https://arxiv.org/abs/2503.08716}
}
```

---

## 13. One-paragraph README pull-quote (optional)

> AuthorMist (David & Gervais, UCL, Mar 2025) fine-tunes a 3B paraphraser with reinforcement learning against commercial detector APIs (GPTZero, Originality.ai, Winston.ai), reporting 78–96% attack success at >0.94 semantic similarity. It is **not** voice cloning — it optimizes detector scores, not your writing sample. unslop does not ship AuthorMist weights; our anti-detector mode is a defensive polish layer for false positives, not a trained evasion policy.
