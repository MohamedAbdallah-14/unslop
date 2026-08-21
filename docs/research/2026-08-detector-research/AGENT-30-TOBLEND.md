# Agent #30 — ToBlend Token Ensemble Humanization Attack

**Topic:** ToBlend (token-level LLM ensemble) as TH-Bench "Token Ensemble" attack family  
**Papers:** Huang et al. *ToBlend* (arXiv 2402.11167, 2024); Zheng et al. *TH-Bench* (arXiv 2503.08708, KDD 2025)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo — **unslop as comparison baseline, not attack target**

---

## Executive summary

**ToBlend** is a *generation-time* adversarial attack, not a post-hoc rewriter. At each decoding step it randomly picks one LLM from a candidate pool, generates the next *k* tokens from that model, appends them, and repeats. The output is a **mixture of next-token distributions** from multiple sources. Most detectors — especially curvature/perplexity methods and RoBERTa classifiers trained on single-model ChatGPT output — assume text came from one stationary generator. ToBlend breaks that assumption deliberately.

On **TH-Bench**, ToBlend is the **`token_ensemble`** attack. Its headline result: **ChatGPT-D AUC collapses to ~0 on WP** (0.727 → **0.000**), with Essay/Reuters/STEM also near chance (0.004–0.005). That is near-total evasion of the HC3-finetuned RoBERTa ChatGPT detector. The tradeoff is brutal: **~80 GB peak GPU**, mediocre fluency/semantics (CS ~0.57–0.66, ROUGE-L ~0.26–0.30 on MGTBench), and **no win on RADAR** (AUC often *rises*). TH-Bench's normalized Pareto plot places ToBlend high on evasion, low on quality, high on compute.

**unslop** sits in a different design space: deterministic/post-hoc prose editing (AI-ism removal, structural variance, optional detector feedback). It does not load four 2–7B models to blend token streams. Treat ToBlend as the **upper bound on detector-breaking via distribution mixing** and unslop as a **cheap, edit-time voice baseline** — comparable in *intent* (reduce detector signal) but not in *mechanism* or TH-Bench numbers. No published work scores unslop on TH-Bench; any comparison is structural, not empirical.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **ToBlend paper (arXiv)** | https://arxiv.org/abs/2402.11167 |
| **ToBlend HTML** | https://arxiv.org/html/2402.11167v2 |
| **ToBlend DOI** | https://doi.org/10.48550/arxiv.2402.11167 |
| **ToBlend code + data (anonymous mirror)** | https://anonymous.4open.science/r/ToBlend/ |
| **TH-Bench paper (arXiv)** | https://arxiv.org/abs/2503.08708 |
| **TH-Bench HTML** | https://arxiv.org/html/2503.08708v2 |
| **TH-Bench DOI (KDD 2025)** | https://doi.org/10.1145/3711896.3737418 |
| **TH-Bench GitHub** | https://github.com/DrenfongWong/TH-Bench |
| **ChatGPT Detector weights (HC3)** | https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta |
| **Fast-DetectGPT (primary ToBlend eval target)** | https://arxiv.org/abs/2310.05626 |
| **MGTBench (TH-Bench dataset lineage)** | https://arxiv.org/abs/2303.14822 |
| **HC3 (ChatGPT-D training data)** | https://arxiv.org/abs/2301.07597 |
| **Sadasivan paraphrase attack (contrast)** | https://arxiv.org/abs/2305.15047 |
| **DIPPER (TH-Bench paraphrase baseline)** | https://arxiv.org/abs/2303.13408 |

**Authors:** Fan Huang, Haewoon Kwak, Jisun An — Indiana University Bloomington (`huangfan@acm.org`).

---

## Mechanism (technical)

### Core algorithm

```
Given: prefix P, ensemble {M₁…Mₙ}, token chunk size k, stop length L
Repeat until len(P) ≥ L:
  1. Randomly select Mᵢ from ensemble
  2. Mᵢ generates (k+3) tokens conditioned on P (overshoot for quality)
  3. Append first k tokens to P
Return P
```

**Why it works (detector-side):** Likelihood, rank, LogRank, DetectGPT/Fast-DetectGPT curvature, and GPT-2/OpenAI/ChatGPT RoBERTa classifiers all embed a **single reference LM** or **single-domain training distribution**. Blended tokens produce local contexts whose conditional probabilities don't match any one scorer's expectations — curvature flattens, rank statistics decorrelate, supervised heads see out-of-manifold features.

**Why it fails sometimes:** **Entropy** detectors can *improve* on ToBlend text (more/less predictable mixed patterns). **RADAR** (adversarial paraphraser + detector GAN) was trained on multi-model paraphrases and resists ensemble mixing. **LM-D** (MGTBench fine-tuned LM classifier) stays strong (AUC ~0.75–0.95 post-ToBlend on most sets) — attribution-style detectors survive better than ChatGPT-D.

### Hyperparameters (original paper)

| Setting | Value |
|---------|-------|
| **Classic ensemble (TH-Bench default)** | GPT-2-xl-1.5B, OPT-2.7B, GPT-Neo-2.7B, GPT-J-6B |
| **Advanced ensemble (paper only)** | Llama-2-7B, Phi-2, Mistral-7B-v0.3, Gemma-7B |
| **Token chunk k** | 1–5 or random; **k=1–2 maximizes evasion**, hurts coherence |
| **Prompt seed** | First 30 tokens of human text (original eval) |
| **Completion length** | ~170 content tokens |
| **Hardware (paper)** | A100 80GB; ~10 s / ~170 tokens at peak |

### TH-Bench instantiation

TH-Bench labels ToBlend under **data-mixing attacks** (alongside sentence-level multi-LLM mixing). Implementation: `attack_run.py --attack token_ensemble`. Uses **classic LLMs only**, default ToBlend settings from Huang et al. Applied to **existing MGT** from 11 generators across MGTBench (Essay, WP, Reuters) + MGT-Academic (STEM, Social Science, Humanity) — not the paper's "complete from 30-token human prefix" protocol, but the same token-blending core.

---

## TH-Bench numbers

### Setup recap

- **6 attacks:** Dipper, Recursion, **ToBlend (token_ensemble)**, Prompt, HMGC, RAFT  
- **13 detectors:** 8 metric-based (Log-Likelihood, Rank, LogRank, Entropy, GLTR, Binoculars, LRR, Fast-DetectGPT) + 5 model-based (RADAR, OpenAI-D, **ChatGPT-D**, LM-D, ConDA)  
- **Metric:** AUC (binary: human vs MGT), averaged over 11 source LLMs  
- **ChatGPT-D:** RoBERTa-base fine-tuned on HC3 answered text ([Hello-SimpleAI/chatgpt-detector-roberta](https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta))

### ChatGPT-D — the AUC→0 result

| Dataset | Clean AUC | ToBlend AUC | Δ |
|---------|-----------|-------------|---|
| **WP (WritingPrompts)** | 0.727 | **0.000** | −0.727 |
| Essay | 0.724 | **0.005** | −0.719 |
| Reuters | 0.812 | **0.004** | −0.808 |
| STEM | 0.740 | **0.004** | −0.736 |
| Social Science | 0.740 | 0.169 | −0.571 |
| Humanity | 0.754 | 0.501 | −0.253 |

WP is the citation everyone repeats: **random-guess detector** after token ensemble. Humanities/Social Science are softer — longer formal prose may preserve enough ChatGPT-ish surface features for partial recovery.

TH-Bench prose (verbatim finding): *"TOBLEND is effective against ChatGPT-Detector across all datasets, even reducing the AUC from 0.727 to 0 on the WP dataset."*

### ToBlend vs other detectors (selected)

**Strong evasion targets (Essay, ToBlend AUC):**
- ChatGPT-D: 0.005  
- OpenAI-D: 0.642 (partial)  
- Fast-DetectGPT: 0.225  
- ConDA: 0.225  
- Log-Likelihood: 0.508  

**Weak or inverted:**
- **RADAR:** 0.951 (up from clean 0.947 — attack fails)  
- **LM-D:** 0.954 (attribution detector barely moves)  
- **Binoculars:** 0.744 (moderate drop only)

**HMGC contrast:** Standard HMGC crushes metric detectors (Log-Likelihood 0.913→0.185 on Essay) but needs a matched surrogate training set. ToBlend needs **no surrogate** — only GPU to host the ensemble.

### Original ToBlend paper (pre-TH-Bench)

On **Fast-DetectGPT** with **classic LLMs**, token length 1–2:

| Dataset | Baseline AUROC | ToBlend AUROC | Δ |
|---------|----------------|---------------|---|
| XSum | 0.9845 | 0.7004 | −0.28 |
| sQuAD | 0.9937 | 0.8047 | −0.19 |
| WritingPrompts | 0.9977 | 0.9128 | −0.08 |

With **advanced LLMs**, XSum Fast-DetectGPT: **0.9845 → 0.3968** — much harsher than classic set. TH-Bench deliberately uses classic models; production evasion with Llama-3-class ensembles would likely be stronger.

**GPT-2 Detector (original paper):** WritingPrompts 0.9365 → 0.7303 (classic); advanced set pushes sQuAD to **0.5052**.

### Multiclass attribution (LM-D)

Binary: ToBlend owns LM-D on several sets. **Multiclass** (which LLM wrote this?): Recursion beats ToBlend; Dipper/Prompt also rise. Token mixing destroys *human-vs-machine* signal more than *which-model* signal.

### Adversarially adapted detectors (WP case study)

When Fast-DetectGPT or LM-D is **fine-tuned on HMGC attack data**, other attacks' AUC drops — but **cross-attack transfer is limited**. ToBlend effectiveness does not fully collapse when the defender knows a *different* attack. Independence of attack families is a TH-Bench design takeaway.

---

## Quality / cost tradeoff (TH-Bench three-axis Pareto)

TH-Bench evaluates **evasion × quality × compute**. No attack wins all three. ToBlend's position:

### Text quality (Table 2, MGTBench + Academic averages)

| Attack | Fluency (PPL vs orig) | Semantic CS | Lexical R-L | Complexity (FRE) |
|--------|----------------------|-------------|-------------|------------------|
| **Prompt** | ≈ unchanged | ~0.88 | ~0.48 | mixed |
| **RAFT** | moderate ↑ | **~0.98** | **~0.95** | ≈ unchanged |
| **ToBlend (WP)** | **+13.4** (32.4 vs 19.0) | **0.569** | **0.264** | +7.3 FRE |
| **ToBlend (Essay)** | +19.3 | 0.658 | 0.263 | +12.5 |
| **Recursion** | worst | <0.65 | <0.30 | large drift |

TH-Bench conclusion: *"TOBLEND … generates text with mediocre fluency"* and *"perform poorly across all three aspects"* vs Prompt/RAFT. Human expert scores in the original paper (1–7 scale): ToBlend TL=1–2 often **~3.9–4.3 coherence/fluency** vs GPT-2 baseline **~5.0** and ChatGPT **~6.3/6.7** — readable but choppy; high fluency scores sometimes mask low coherence.

### Compute (Figure 6, MGT-Academic overhead)

| Attack | Peak GPU | Time scaling |
|--------|----------|--------------|
| **ToBlend** | **~80 GB** (highest; 2× L20) | Grows with length |
| HMGC | ~60 GB | Moderate |
| Dipper / Prompt | ~40 GB floor | Lower |
| RAFT | ~40 GB | **Highest latency** (word-scoring loop) |

Minimum footprint across all attacks ≈40 GB — ToBlend doubles that. Original paper: **~10 s / 170 tokens** on one A100 80GB with 4 classic models loaded.

### Evasion–quality–cost triangle (interpretation)

```
        High evasion (ChatGPT-D → 0)
              ▲
              │  ToBlend ●
              │           ╲
              │            ╲  HMGC ● (metric detectors)
              │             ╲
              │   Recursion ●  ╲
              │                 ╲
              └──────────────────● RAFT / Prompt
         Low cost ◄────────────────► High cost
                    (quality ↑ toward Prompt/RAFT)
```

**Operational read:** ToBlend is for adversarial eval and red-teaming detector stacks, not for user-facing "humanize my essay" products. The text often *reads wrong* before any detector runs.

### TH-Bench mitigation: Quality-Preserving Attack (QPA)

Appendix insight: instead of random token pick, **rank candidate LLM outputs by quality proxy and take the best token**. QPA+ToBlend on STEM: PPL 48.4→**37.9**, CS 0.648→**0.735**, R-L 0.287→**0.408** — meaningful quality recovery with "minimal" evasion loss (per authors). Suggests **quality-aware blending** is the research fix; random ToBlend is the worst-case attacker.

---

## Detector family susceptibility (synthesis)

| Detector family | ToBlend effect | Mechanism |
|-----------------|----------------|-----------|
| ChatGPT-D / OpenAI-D | **Severe** | Single-source RoBERTa assumptions break |
| Fast-DetectGPT / curvature | **Strong** | Mixed curvature |
| LogLikelihood / Rank / GLTR | **Strong** | Metric drift |
| Entropy | Mixed / sometimes ↑ detection | Original paper: entropy *improves* |
| RADAR | **Fails** (AUC ↑) | Trained on multi-paraphrase distribution |
| LM-D | **Mostly survives** | Fine-tuned on diverse MGT attribution |
| Binoculars | Partial | Cross-PPL ratio less fragile than ChatGPT-D |

**2026 product caveat (unslop baseline context):** Commercial detectors (Turnitin Aug 2025 "AI bypasser" models, DivEye surprisal-variance, GPTZero v6) post-date TH-Bench's 13-detector panel. ChatGPT-D AUC→0 **does not imply** Turnitin→0. ToBlend's *distribution-mixing* principle may still transfer to perplexity-family scorers; supervised bypasser heads are an open question.

---

## unslop as comparison baseline (not target)

### Architectural contrast

| Dimension | ToBlend | unslop |
|-----------|---------|--------|
| **When** | Generation-time (decode loop) | Post-hoc edit of existing text |
| **Mechanism** | Random multi-LM token splicing | Regex + structural passes + optional LLM rewrite |
| **Goal** | Break detector statistical assumptions | Remove AI-isms; sound human; optional `--detector-feedback` |
| **Compute** | 4× 2–7B models, ~80 GB | Single-threaded Python; optional small HF detector (TMR ~125M) |
| **Semantic preservation** | Poor (R-L ~0.26) | Explicit preservation contract (code, URLs, headings) |
| **TH-Bench entry** | `token_ensemble` | **None** (not in literature or benchmark) |

### Conceptual overlap

unslop **anti-detector** mode explicitly recommends a **cross-model second pass** (Claude ↔ GPT ↔ Gemini) — the closest *practitioner* analogue to ensemble mixing, but at **paragraph/sentence granularity**, not token granularity. TempParaphraser (EMNLP 2025) formalizes temperature-simulation paraphrase (~82.5% detector reduction); still not ToBlend.

ToBlend proves **multi-distribution text** breaks ChatGPT-D completely. unslop proves **surface stylometry + slop removal** improves readability without loading an ensemble. They optimize different objectives on the TH-Bench Pareto:

- ToBlend: max evasion, accept garbled semantics  
- unslop balanced/full: max voice quality, **detector evasion optional and secondary**  
- unslop anti-detector: detector-aware, but edit-time and single-model unless user runs second pass

### What unslop should *not* do

1. **Do not implement random token ensemble** — cost, quality, and misuse profile are incompatible with unslop's preservation contract and ESL false-positive defense mission.  
2. **Do not cite ChatGPT-D AUC→0 as unslop performance** — no data exists.  
3. **Do not treat ToBlend as the humanization gold standard** — TH-Bench explicitly ranks Prompt/RAFT higher on quality; ToBlend is a **detector stress test**.

### What unslop *can* borrow (evaluation only)

1. **TH-Bench scaffolding** (`DrenfongWong/TH-Bench`) for benchmarking `--detector-feedback` against ChatGPT-D, Fast-DetectGPT, Binoculars — compare *edit-time* humanizers to `token_ensemble` on **quality axis**, not expect evasion parity.  
2. **Report three axes** (evasion, CS/R-L, wall-clock/GPU) whenever publishing anti-detector numbers — TH-Bench norm.  
3. **QPA insight:** if unslop ever experiments with multi-model passes, **quality-ranked merging** beats random blending.  
4. **RADAR + LM-D as release-gate detectors** — if unslop output passes ChatGPT-D but fails these, marketing "undetectable" claims would be misleading (same lesson as DAMAGE for commercial humanizers).

### unslop detector.py alignment

Current loop default: **TMR** (125M RoBERTa, RAID AUROC ~99.28%). Not ChatGPT-D. A ToBlend-hardened eval suite should add:

- `Hello-SimpleAI/chatgpt-detector-roberta` (TH-Bench headline)  
- Fast-DetectGPT (curvature)  
- Optional Binoculars / RADAR for failure-mode coverage  

Expectation: unslop anti-detector **may** move TMR/Fast-DetectGPT scores; it **will not** replicate ToBlend's ChatGPT-D collapse without multi-model token mixing.

---

## Attack family context (TH-Bench)

| Attack | Category | ChatGPT-D (WP) | Quality | Cost |
|--------|----------|----------------|---------|------|
| **ToBlend** | Data mixing | **0.000** | Low | Highest GPU |
| HMGC | Perturbation | 0.436 | Low fluency, high R-L | High + needs surrogate data |
| Recursion | Paraphrase | 0.730 | Worst semantics | ~5× Dipper time |
| Dipper | Paraphrase | 0.788 | Moderate | Moderate |
| Prompt | Paraphrase | 0.665 | **Best** | API cost |
| RAFT | Perturbation | 0.713 | High CS/R-L | **Highest time** |

**Headline:** Targeted relationships — no universal attacker. ToBlend owns ChatGPT-D; Recursion owns ConDA; HMGC owns metric detectors with matched data.

---

## Limitations and open questions

1. **Classic LLM ensemble only in TH-Bench** — Advanced set (Llama2/Mistral/Gemma) likely stronger; unreplicated in benchmark harness.  
2. **Generation vs rewrite** — TH-Bench applies ToBlend to MGT; original paper generates from human prefix. Numbers may not transfer to "humanize this ChatGPT paragraph" workflows.  
3. **Fine-tuning defense** — Llama-3.1 fine-tuned on high-quality ToBlend pairs improves detection in original paper (Table 5); arms race continues.  
4. **Human quality vs automatic metrics** — Experts rate some ToBlend configs acceptable (~5/7) while automatic CS/R-L scream degradation; product QA needs human reads.  
5. **Ethics** — Paper and TH-Bench frame misuse (disinformation, academic fraud). unslop anti-detector is scoped to false-positive defense; ToBlend is pure evasion research.

---

## Recommended citations for unslop docs

```bibtex
@article{huang2024toblend,
  title={ToBlend: Token-Level Blending With an Ensemble of LLMs to Attack AI-Generated Text Detection},
  author={Huang, Fan and Kwak, Haewoon and An, Jisun},
  journal={arXiv preprint arXiv:2402.11167},
  year={2024}
}

@inproceedings{zheng2025thbench,
  title={TH-Bench: Evaluating Evading Attacks via Humanizing AI Text on Machine-Generated Text Detectors},
  author={Zheng, Jingyi and Wang, Junfeng and Sun, Zhen and Dong, Wenhan and Liu, Yule and He, Xinlei},
  booktitle={Proceedings of KDD},
  year={2025},
  doi={10.1145/3711896.3737418}
}
```

---

## Bottom line

ToBlend is the TH-Bench **token ensemble** attack: randomly splice tokens from four classic LMs to produce text whose next-token statistics match **no single detector's world model**. It is the strongest published breaker of **ChatGPT-D** on TH-Bench (WP AUC **0.727 → 0.000**), paid for with **~80 GB GPU**, choppy prose, and ROUGE-L ~0.26. It is not a humanizer users would want to read.

**unslop** belongs on the **quality-first** side of the same literature map — voice, preservation, ESL-safe anti-detector — not as a ToBlend competitor. Use ToBlend to calibrate how hard **distribution-level** attacks hit legacy RoBERTa detectors; use unslop to measure whether **edit-time stylometry** can help legitimate writers without ensemble-grade infrastructure.

---

*Agent #30 complete. Cross-refs: Agent #19 (MGTBench/TH-Bench), Agent #5 (Fast-DetectGPT), Agent #31 (DIPPER), Agent #12 (DAMAGE), Agent #35 (cross-model paraphrase practitioner technique).*
