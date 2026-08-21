# Agent #26 — StealthRL (GRPO Paraphrase vs Detector Ensemble)

**Topic:** Ranganath & Ramesh, *StealthRL: Reinforcement Learning Paraphrase Attacks for Multi-Detector Evasion of AI-Text Detectors* (arXiv:2602.08934)  
**Prepared:** August 19, 2026  
**Scope:** GRPO+LoRA on Qwen3-4B, Fast-DetectGPT / Binoculars collapse, held-out transfer, supporters/critics, unslop README threat-model audit  
**Status:** complete

---

## Executive summary

StealthRL (Feb 2026, UCSD) is the first open, reproducible **RL-trained paraphrase policy** optimized against a **multi-detector ensemble** at security-relevant operating points (TPR@1%FPR). It extends AuthorMist (single-detector RL) and Adversarial Paraphrasing (detector-guided search at inference) by learning a one-shot paraphrase generator that generalizes to held-out detector families.

**Headline numbers (v2, canonical):** On the full filtered MAGE test pool (15,310 human / 14,656 AI, 100–500 tokens), StealthRL (M2) drops **mean AUROC 0.789 → 0.432**, **mean TPR@1%FPR 0.450 → 0.024**, **97.6% attack success rate**. Training ensemble: RoBERTa OpenAI (60%) + Fast-DetectGPT (40%). **Held-out:** Binoculars and MAGE detector — both collapse on TPR@1%FPR despite never appearing in the reward.

**Fast-DetectGPT specifically (v2):** AUROC **0.661 → 0.089** [95% CI: 0.086–0.092]; TPR@1%FPR **0.388 → 0.002**; ASR **99.8%**.

**Binoculars transfer (v2, held-out):** AUROC **0.705 → 0.055** [0.052–0.058]; TPR@1%FPR **0.367 → 0.002**; ASR **99.8%**. Strongest evidence in the paper that curvature/cross-perplexity detectors share surface-statistic vulnerabilities with fine-tuned classifiers.

**Revision note:** v1 (2602.08934v1) reported **mean AUROC 0.74 → 0.27** and **99.9% ASR** on a smaller eval (1,000 human / 1,000 AI, three detectors only). v2 expanded to four detectors + full MAGE pool; mean AUROC rose on clean text (MAGE detector is very strong) so aggregate collapse is **0.79 → 0.43**, not 0.74 → 0.27. Per-detector Fast-DetectGPT was **0.671 → 0.071** in v1, **0.661 → 0.089** in v2 — not 0.74 → 0.27. Treat **0.74 → 0.27** as **v1 mean across RoBERTa + Fast-DetectGPT + Binoculars**, not a Fast-DetectGPT line item.

**Unslop verdict:** StealthRL is the strongest **public benchmark** for what a dedicated adversary can do with one LoRA fine-tune (~10k samples, Qwen3-4B). It **validates** unslop's README honesty: deterministic surface rewriting and burstiness moves do **not** approximate RL paraphrase against Fast-DetectGPT/Binoculars. It **does not invalidate** unslop's positioning as a polish layer — StealthRL pays a quality tax (Likert quality 2.51 vs 3.78 for simple paraphrase; PPL spikes to 148.7). unslop should cite StealthRL as the **upper bound on adaptive paraphrase**, keep anti-detector mode framed as ESL/false-positive defense, and never imply `--detector-feedback` closes the gap StealthRL opens.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | StealthRL: Reinforcement Learning Paraphrase Attacks for Multi-Detector Evasion of AI-Text Detectors |
| **Authors** | Suraj Ranganath (corresponding), Atharv Ramesh |
| **Affiliation** | University of California, San Diego |
| **Posted** | 9 February 2026 |
| **Revisions** | v1 → v2 (expanded eval: +MAGE detector, full MAGE test pool, bootstrap CIs) |
| **arXiv** | https://arxiv.org/abs/2602.08934 |
| **HTML (latest)** | https://arxiv.org/html/2602.08934v2 |
| **HTML (v1)** | https://arxiv.org/html/2602.08934v1 |
| **DOI** | https://doi.org/10.48550/arxiv.2602.08934 |
| **Code** | https://github.com/suraj-ranganath/StealthRL |
| **Demo** | https://stealthrl.dev/ |
| **Checkpoint** | https://huggingface.co/suraj-ranganath/StealthRL (LoRA on `Qwen/Qwen3-4B-Instruct-2507`) |
| **Canonical config** | `configs/tinker_mage_10k.yaml` (per repo README) |

**One-line contribution:** Train a paraphrase policy with GRPO+LoRA against a weighted detector ensemble; evaluate single-shot inference at TPR@1%FPR with held-out transfer — reproducible red-team protocol, not a commercial humanizer.

---

## 2. Method — GRPO + LoRA on Qwen3-4B

### 2.1 Threat model (paper)

| Dimension | Specification |
|-----------|---------------|
| **Attacker capability** | Black-box detector scores only (scalar AI probability). Gradients deliberately unused even when detectors are open-source. |
| **Attacker goal** | Paraphrase \(y\) of AI text \(x\) with \(p_{\text{det}}(y) < \tau\) at 1% FPR threshold while \(\text{sim}(x,y) > \delta\). |
| **Attacker constraint** | Fluent grammatical reformulation, not homoglyph corruption (M5 is separate baseline). |
| **Inference** | **Single-shot:** one generation per input, temp 1.0, top-p 0.9, max 512 tokens. No test-time detector queries, no reranking. |
| **Training access** | Detector ensemble queried offline during GRPO rollouts only. |

This is a **stronger** threat model than unslop's `--detector-feedback` ladder (local rewrites + optional TMR scoring) and **weaker** than Adversarial Paraphrasing M3 (multi-candidate + detector reranking at eval time). StealthRL amortizes search into learned weights.

### 2.2 Reward

\[
R(x,y) = \alpha \cdot R_{\text{det}}(y) + \beta \cdot R_{\text{sem}}(x,y)
\]

| Parameter | Value |
|-----------|-------|
| \(\alpha\) (detector weight) | 1.0 |
| \(\beta\) (semantic weight) | 0.1 |
| \(R_{\text{det}}(y)\) | \(1 - [0.6 \cdot p_{\text{RoBERTa}}(y) + 0.4 \cdot p_{\text{Fast-DetectGPT}}(y)]\) |
| \(R_{\text{sem}}(x,y)\) | E5 embedding cosine similarity |
| KL penalty \(\lambda_{\text{KL}}\) | 0.05 vs frozen Qwen3-4B reference |

GRPO: group size 8, group-relative advantage normalization, clipped policy gradient.

### 2.3 Training hyperparameters (Appendix C / repo)

| Parameter | Value |
|-----------|-------|
| Base model | `Qwen/Qwen3-4B-Instruct-2507` |
| LoRA rank / α / dropout | 32 / 32 / 0.05 |
| Algorithm | GRPO |
| Learning rate | 2.8×10⁻⁴ |
| Batch size | 16 |
| Epochs | 3 |
| Training samples | 10,000 AI-only MAGE subset |
| Framework | Tinker API (Thinking Machines research credits) |
| Prompt | "Paraphrase the following text while preserving its meaning: [TEXT]" |

**Compute implication:** One modest fine-tune (4B + LoRA, 10k × 3 epochs) suffices to break four detector families at 1% FPR. This is the number unslop's README should fear — not Undetectable.ai marketing.

---

## 3. Detectors evaluated

| Detector | Paradigm | Training ensemble? | Scoring stack |
|----------|----------|-------------------|---------------|
| **RoBERTa OpenAI** | Fine-tuned classifier | ✅ 60% weight | `openai-community/roberta-large-openai-detector` |
| **Fast-DetectGPT** | Zero-shot curvature | ✅ 40% weight | Scoring LM: `EleutherAI/gpt-neo-2.7B` |
| **Binoculars** | Paired-LM cross-perplexity | ❌ held-out | gpt2-medium + gpt2-large |
| **MAGE detector** | Longformer classifier | ❌ held-out | `yaful/MAGE` |

**Threshold protocol:** For each detector, threshold = 99th percentile of scores on **15,310 human** eval samples (v2). AI samples scored at fixed threshold. Primary metric: **TPR@1%FPR** (not AUROC alone).

---

## 4. Results — v2 (canonical)

### 4.1 Aggregate (four detectors)

| Method | Mean AUROC | Mean TPR@1%FPR | Mean ASR |
|--------|------------|----------------|----------|
| M0 No attack | 0.789 | 0.450 | 0.550 |
| M1 Simple paraphrase | — | 0.284 | 0.716 |
| **M2 StealthRL** | **0.432** | **0.024** | **0.976** |
| M3 Adv. paraphrase | — | 0.217 | 0.783 |
| M4 AuthorMist | — | 0.203 | 0.797 |
| M5 Homoglyph | — | 0.034 | 0.966 |

### 4.2 Per-detector — StealthRL (M2) vs no attack (M0)

| Detector | M0 AUROC | M2 AUROC | M0 TPR@1% | M2 TPR@1% | M2 ASR |
|----------|----------|----------|-----------|-----------|--------|
| **Fast-DetectGPT** | 0.661 | **0.089** | 0.388 | **0.002** | 0.998 |
| **Binoculars** (held-out) | 0.705 | **0.055** | 0.367 | **0.002** | 0.998 |
| RoBERTa (in-ensemble) | 0.806 | 0.691 | 0.203 | 0.002 | 0.998 |
| MAGE (held-out) | 0.983 | 0.891 | 0.843 | 0.089 | 0.911 |

**Fast-DetectGPT:** Near-random AUROC (~0.09), effectively zero TPR at 1% FPR. Confirms Sadasivan/Cheng lineage: curvature signal is paraphrase-fragile when the paraphraser is trained to minimize it.

**Binoculars transfer:** AUROC 0.705 → 0.055 without ever appearing in reward. Paper interprets this as shared reliance on **surface token-distribution / perplexity geometry**, not detector-specific overfitting. unslop's anti-detector burstiness/surprisal moves target the same axis — but StealthRL shows **learned** redistribution beats hand-tuned structural variance against Binoculars.

**MAGE robustness:** Only detector that partially survives (TPR@1% still 8.9%, AUROC 0.891). MAGE Longformer was trained on diverse MAGE data — closest to "in-domain strong classifier" in the panel.

**RoBERTa anomaly:** AUROC stays moderate (0.691) while TPR@1%FPR → 0.002. Paper explains: RL policy pushes scores **below the strict threshold** without fully collapsing rank order — **operating-point metric matters** for integrity deployments.

### 4.3 v1 numbers (superseded but cited in landscape JSON)

| Metric | v1 (3 det, 1k/1k) | v2 (4 det, full pool) |
|--------|-------------------|------------------------|
| Mean AUROC M0 → M2 | 0.74 → **0.27** | 0.79 → 0.43 |
| Mean ASR | 99.9% | 97.6% |
| Fast-DetectGPT AUROC | 0.671 → 0.071 | 0.661 → 0.089 |
| Binoculars AUROC | 0.716 → 0.041 | 0.705 → 0.055 |
| E5 similarity (M2) | 0.896 | 0.901 |
| Likert quality (M2) | 2.59 | 2.51 |

Use **v2** for README citations; note v1 when explaining why older summaries say 0.74→0.27.

### 4.4 Quality–evasion tradeoff

| Method | E5 sim | Likert quality (1–5) | Likert similarity | Mean ASR |
|--------|--------|----------------------|-------------------|----------|
| M1 Simple para | 0.974 | 3.78 | 4.06 | 0.716 |
| M3 Adv. para | 0.973 | 3.77 | 4.02 | 0.783 |
| **M2 StealthRL** | **0.901** | **2.51** | 2.64 | **0.976** |
| M5 Homoglyph | 0.923 | 1.97 | 2.92 | 0.966 |

StealthRL wins evasion; loses readability. PPL jumps 26.7 → 148.7 (M2). For unslop: **human-read ≠ detector-evade**. StealthRL is optimized for the latter.

### 4.5 Baseline comparison (why StealthRL > M3/M4)

| Attack | Mechanism | Mean TPR@1% (v2) | Notes |
|--------|-----------|------------------|-------|
| M3 Adversarial Paraphrasing | Multi-candidate + detector rerank at **inference** | 0.217 | Cheng et al. NeurIPS 2025; no weight update |
| M4 AuthorMist | RL vs **single** RoBERTa | 0.203 | David & Gervais 2025 |
| **M2 StealthRL** | RL vs **ensemble**; single-shot inference | **0.024** | Multi-detector training is key |

Ensemble training + GRPO beats single-detector RL and beats inference-time search (M3) on this benchmark at 1% FPR.

---

## 5. Supporters — who cites StealthRL and why

| Camp | Position | Representative sources |
|------|----------|------------------------|
| **Robustness evaluators** | StealthRL is a reproducible red-team harness; TPR@1%FPR is the right metric for integrity tools | Paper authors; RAID/MAGE benchmark lineage (Dugan et al. 2405.07940) |
| **Sadasivan impossibility school** | RL paraphrase operationalizes TV-reduction at scale; detectors relying on surface stats are doomed | Sadasivan et al. 2303.11156 (cited §2.1); Agent #17 memo in this repo |
| **Adversarial paraphrase line** | StealthRL > M3/M4 on strict FPR; ensemble training generalizes | Cheng et al. 2506.07001; AuthorMist 2503.08716 |
| **Detector developers (implicit)** | Need adversarial training / semantic features / watermarking | Paper §6.1, §7 future work |
| **unslop (defensive)** | StealthRL sets **upper bound**; validates honest "polish not bypass" README | This memo; README TMR 0.0–0.2 pp benchmark |

**What supporters get right**

1. **Held-out Binoculars collapse** is the paper's strongest scientific claim — not cherry-picking the training detector.
2. **Single-shot inference** — attack is deployable without per-text detector API budget at test time.
3. **Open weights + code** — rare in humanizer space; enables defender-side adversarial training.
4. **Operating-point reporting** — TPR@1%FPR alongside AUROC matches Sadasivan's integrity critique.

---

## 6. Critics — limitations and counterarguments

| Critique | Detail | Severity |
|----------|--------|----------|
| **MAGE-only eval domain** | English, MAGE domains, 100–500 tokens. RAID multilingual/adversarial mix not tested. | Medium |
| **No watermark detectors** | Kirchenbauer et al. 2301.10226 family excluded. Paraphrase may not strip generation-time watermarks. | Medium–High for provenance, not post-hoc detection |
| **No commercial stack** | GPTZero, Turnitin (Aug 2025 bypasser model), Originality not in panel. TMR (unslop default) not tested. | High for product claims; medium for research |
| **Quality degradation** | Likert 2.51, high PPL — instructors may reject on readability alone. | Medium for evasion; **Low** for unslop (quality-first) |
| **Homoglyph rival (M5)** | Comparable ASR (96.6%) with worse quality but trivial normalization defense. | Low — different threat class |
| **Dataset shift / v1→v2** | Headline numbers changed with revision; early summaries stale. | Process critique |
| **Adaptive defense** | Adversarial fine-tuning on StealthRL outputs not evaluated. Turnitin explicitly trains on humanizer outputs. | High — arms race continues |
| **Retrieval / provenance** | Krishna et al. 2303.13408 retrieval defense not tested. Provider-side logs bypass paraphrase entirely. | High for forensic, N/A for standalone detector |
| **Ethical dual-use** | Released LoRA weights lower bar for misuse. Authors frame as stress-test + responsible disclosure. | Policy debate |

**Nicks et al. (ICLR 2024)** — "advise against continued reliance on LLM-generated text detectors" — StealthRL is empirical ammunition, not a refutation. Detectors may still be **useful signals** at low stakes if FPR is disclosed; StealthRL shows they fail as **sole evidence** under adaptive paraphrase.

**DivEye (TMLR 2026) gap:** StealthRL does not evaluate surprisal-variance detectors. unslop's `--surprisal-variance` hook is untested against StealthRL-class attacks — open benchmark opportunity.

---

## 7. Position in the evasion literature

```
Sadasivan TV bound (2023)
    └── DIPPER / recursive paraphrase (Krishna 2023)
            └── Adversarial Paraphrasing M3 (Cheng NeurIPS 2025) — inference search
                    └── AuthorMist M4 (2025) — single-detector RL
                            └── StealthRL M2 (2026) — multi-detector GRPO+LoRA, held-out transfer
                                    └── [future] adversarially trained detectors / semantic detectors
```

| Paper | arXiv | StealthRL relationship |
|-------|-------|------------------------|
| Sadasivan impossibility | 2303.11156 | Theoretical ceiling StealthRL approaches empirically |
| Adversarial Paraphrasing | 2506.07001 | M3 baseline; StealthRL beats at 1% FPR |
| AuthorMist | 2503.08716 | M4 baseline; single-detector RL insufficient |
| Fast-DetectGPT | 2310.05130 | In-ensemble target; collapsed to ~0.09 AUROC |
| Binoculars | 2401.12070 | Held-out; collapsed to ~0.055 AUROC |
| MAGE benchmark | 2305.13242 | Dataset + strongest held-out detector |
| RAID | 2405.07940 | Recommended extension for defender eval |
| SilverSpeak homoglyph | 2406.11239 | M5 baseline |

---

## 8. unslop threat model — README honesty audit

### 8.1 What unslop currently claims (README + SKILL.md)

| Claim | Location | StealthRL interaction |
|-------|----------|----------------------|
| "Polish layer, not detector-defeat tool" | README L400, FAQ | ✅ **Supported** — StealthRL is a different category (trained adversary) |
| TMR deterministic moves **0.0–0.2 pp** | README L597–598, benchmarks | ✅ **Consistent** — StealthRL is not deterministic unslop |
| Adversarial Paraphrasing ~87% TPR drop | README L595 | ✅ Directionally aligned; StealthRL is stronger at 1% FPR |
| Strongest lever = **different-model paraphrase** | README L603, SKILL.md L97 | ⚠️ **Incomplete** — StealthRL shows **same-model RL paraphrase** beats M3 search when trained on ensemble |
| `--detector-feedback` escalates ladder, recommends cross-model pass | detector.py | ✅ Honest secondary layer; does not claim StealthRL-class evasion |
| anti-detector for **ESL false positives**, not misconduct | SKILL.md Boundaries | ✅ StealthRL authors share dual-use framing |
| "Never claim detector defeat" | README L671 | ✅ Must hold; StealthRL is evidence **against** defeat claims |
| Commercial humanizers ~6 pp median drop (Chicago Booth) | README L610 | ✅ StealthRL ≠ commercial SaaS; don't conflate |

### 8.2 Threat-model tiers (recommended framing)

| Tier | Actor | Capability | unslop relevance |
|------|-------|------------|------------------|
| **T0** | Casual user | No editing | Detectors work (M0 baseline) |
| **T1** | unslop user | Deterministic + optional LLM polish, burstiness | TMR ±0.2 pp; **not StealthRL-class** |
| **T2** | Manual writer | Cross-model paraphrase + manual fact restore | README's recommended path; moderate evasion (M1/M3 band) |
| **T3** | Adaptive adversary | StealthRL LoRA or equivalent GRPO fine-tune | **97.6% ASR** at 1% FPR on open detectors; unslop does not operate here |
| **T4** | Platform verifier | Retrieval, generation logs, watermark | Paraphrase irrelevant |

**Honest README addition (optional):** "Open research (StealthRL, Feb 2026) shows a fine-tuned 4B paraphrase model can collapse Fast-DetectGPT and Binoculars to near-zero TPR@1%FPR on MAGE. unslop is T1–T2, not T3."

### 8.3 What unslop should NOT claim

1. ❌ "Beats Binoculars / Fast-DetectGPT" — StealthRL proves dedicated RL beats them; unslop's measured TMR movement does not.
2. ❌ "`anti-detector` mode ≈ StealthRL" — different mechanism (prompted burstiness vs reward-optimized paraphrase policy).
3. ❌ "`--detector-feedback` closes the adversarial gap" — ladder exhausts at local rewrites; StealthRL needs weight update.
4. ❌ Implying static benchmark numbers survive adaptive attackers — StealthRL is the counterexample.

### 8.4 What unslop SHOULD claim ( strengthened by StealthRL)

1. ✅ **Detector scores are not integrity evidence** under adaptive paraphrase (StealthRL + Sadasivan).
2. ✅ **Quality and voice** remain the product value — StealthRL sacrifices Likert quality for ASR.
3. ✅ **ESL false-positive defense** — legitimate use case where users are not training RL attackers.
4. ✅ **Cross-model workflow** still helps at T2; v0.7 roadmap item remains valid but won't reach T3 without explicit adversarial training (which unslop should not ship).

### 8.5 Benchmark gaps to close (optional engineering)

| Action | Rationale |
|--------|-----------|
| Add Fast-DetectGPT + Binoculars to `benchmarks/detector_bench.py` | Align bench with StealthRL panel |
| Run unslop fixtures through `suraj-ranganath/StealthRL` adapter | Quantify T1 vs T3 gap on same texts |
| Log TPR@1%FPR not just raw probability | Match paper's security metric |
| Cite StealthRL in README adversarial paragraph | Replace vague "arms race" with dated anchor |

---

## 9. Comparison table — attack methods at a glance

| Method | Train cost | Inference | Fast-DGPT AUROC (v2 M2) | Binoculars AUROC (v2 M2) | E5 sim | Likert Q |
|--------|------------|-----------|-------------------------|--------------------------|--------|----------|
| M0 None | — | — | 0.661 | 0.705 | 1.00 | — |
| M1 Simple | — | 1× LLM | 0.588 | 0.593 | 0.974 | 3.78 |
| **M2 StealthRL** | **LoRA GRPO** | **1× policy** | **0.089** | **0.055** | 0.901 | 2.51 |
| M3 Adv. Para | — | N× + rerank | 0.536 | 0.511 | 0.973 | 3.77 |
| unslop T1 (est.) | — | regex/LLM | ~0.65* | ~0.70* | ~0.95* | ~3.5* |

\*unslop not evaluated in StealthRL paper; TMR bench shows ~0 pp movement — order-of-magnitude below M2.

---

## 10. Policy and ethics (authors + unslop alignment)

**Authors:** Position StealthRL as stress-testing for detector developers; release code for reproducible robustness benchmarking; warn against high-stakes deployment of brittle detectors.

**unslop alignment:** Matches Boundaries in `skills/unslop/SKILL.md` — anti-detector for false-positive defense, decline academic misconduct, EU AI Act Art. 50 awareness.

**Regulatory (Aug 2026):** StealthRL does not remove watermarks or forge provenance; it post-hoc paraphrases AI text. Still dual-use for integrity evasion. unslop should not integrate StealthRL weights or GRPO training into the product.

---

## 11. Open problems (August 2026)

1. **StealthRL vs DivEye / TMR / Turnitin** — no public numbers.
2. **Adversarial fine-tune defense** — detector retrained on M2 outputs.
3. **Quality-constrained StealthRL** — Pareto RL to lift Likert above 3.0 without ASR drop.
4. **RAID cross-benchmark** — transfer beyond MAGE English slice.
5. **unslop measured gap** — formal T1 fixture run vs StealthRL adapter on identical inputs.

---

## 12. Source index

### Primary

| Resource | URL |
|----------|-----|
| StealthRL arXiv | https://arxiv.org/abs/2602.08934 |
| StealthRL HTML v2 | https://arxiv.org/html/2602.08934v2 |
| StealthRL HTML v1 | https://arxiv.org/html/2602.08934v1 |
| StealthRL DOI | https://doi.org/10.48550/arxiv.2602.08934 |
| GitHub | https://github.com/suraj-ranganath/StealthRL |
| HuggingFace LoRA | https://huggingface.co/suraj-ranganath/StealthRL |
| Demo | https://stealthrl.dev/ |

### Detectors (evaluated in paper)

| Resource | URL |
|----------|-----|
| Fast-DetectGPT | https://arxiv.org/abs/2310.05130 |
| Binoculars | https://arxiv.org/abs/2401.12070 |
| MAGE benchmark | https://arxiv.org/abs/2305.13242 |
| RoBERTa OpenAI detector | https://huggingface.co/openai-community/roberta-large-openai-detector |
| MAGE detector weights | https://huggingface.co/yaful/MAGE |

### Related attacks & theory

| Resource | URL |
|----------|-----|
| Adversarial Paraphrasing (M3) | https://arxiv.org/abs/2506.07001 |
| AuthorMist (M4) | https://arxiv.org/abs/2503.08716 |
| Sadasivan impossibility | https://arxiv.org/abs/2303.11156 |
| DIPPER / paraphrase evasion | https://arxiv.org/abs/2303.13408 |
| SilverSpeak homoglyph (M5) | https://arxiv.org/abs/2406.11239 |
| RAID benchmark | https://arxiv.org/abs/2405.07940 |
| GRPO (DeepSeekMath lineage) | https://arxiv.org/abs/2402.03300 |
| LoRA | https://arxiv.org/abs/2106.09685 |
| E5 embeddings (semantic reward) | https://arxiv.org/abs/2212.03533 |

### unslop internal

| Resource | Path |
|----------|------|
| README detector honesty | `/README.md` (detector FAQ, TMR benchmark) |
| anti-detector skill | `skills/unslop/SKILL.md` §84–98 |
| detector.py | `unslop/scripts/detector.py` |
| Agent #17 Sadasivan memo | `docs/research/2026-08-detector-research/AGENT-17-SADASIVAN-IMPOSSIBILITY.md` |
| Landscape JSON (v1 numbers) | `docs/research/2026-08-detector-research/ai-detection-landscape-aug2026.json` |

---

## 13. Citation (BibTeX)

```bibtex
@misc{ranganath2026stealthrl,
  title={StealthRL: Reinforcement Learning Paraphrase Attacks for Multi-Detector Evasion of AI-Text Detectors},
  author={Ranganath, Suraj and Ramesh, Atharv},
  year={2026},
  eprint={2602.08934},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2602.08934}
}
```

---

*Agent #26 complete. Manifest row 26 → done.*
