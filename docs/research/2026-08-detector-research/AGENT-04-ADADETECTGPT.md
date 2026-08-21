# Agent #04 — AdaDetectGPT Deep Research

**Focus:** Adaptive DetectGPT variant (NeurIPS 2025): mechanism, benchmarks, evasion, community debate, unslop `detector.py` comparison.  
**Date:** 2026-08-19  
**Scope:** Full internet research + read of `unslop/scripts/detector.py`.

---

## Executive summary

**AdaDetectGPT** (Zhou et al., NeurIPS 2025; [arXiv:2510.01268](https://arxiv.org/abs/2510.01268)) is a **logits-based** detector that extends **Fast-DetectGPT** (ICLR 2024) by learning a one-dimensional **witness function** \(w\) over token log-probabilities. Instead of using raw log-probs in the curvature statistic, AdaDetectGPT applies \(w(\log q_t)\) and learns \(w\) from a corpus of human-written passages by maximizing a **lower bound on true negative rate (TNR)**. Classification thresholds come from the **martingale central limit theorem (MCLT)**, giving finite-sample FNR/TPR/FPR/TNR bounds — rare formal guarantees in this field.

Empirically, AdaDetectGPT **uniformly beats Fast-DetectGPT** on the authors' five custom dataset splits (SQuAD, WritingPrompts, XSum, Yelp, Essay): **+12.5% to +37% relative AUC** in white-box settings, **up to +20%** in black-box surrogate settings (Gemma-2-9b scoring GPT-4o / Claude-3.5 / Gemini-2.5). Against paraphrase and decoherence attacks (Fast-DetectGPT's attack protocol), gains are **modest for paraphrase** (~0.5 AUC points, ≤10% relative) but **large for decoherence** (up to 85% relative).

**Critical gap for unslop:** AdaDetectGPT is **not evaluated on MAGE, RAID, or HC3**. It does not appear on the [RAID leaderboard](https://raid-bench.xyz/). The attacks tested are **not** cross-model paraphrase, TempParaphraser, DIPPER, or Adversarial Paraphrasing — the evasion vectors unslop's `detector.py` feedback loop actually faces. Fast-DetectGPT (AdaDetectGPT's parent) collapses under TempParaphraser (98.9% → 2.6% on HC3 per Agent #24); AdaDetectGPT's adaptive witness may help marginally but shares the same logits/curvature family and surrogate-model dependency.

**unslop uses TMR** (`Oxidane/tmr-ai-text-detector`, 125M RoBERTa, 99.28% RAID AUROC) — a **supervised text classifier**, not a logits-based zero-shot method. TMR is the right default for unslop's feedback loop: single forward pass, ~500MB, no source-LLM access, offline-capable. AdaDetectGPT would require loading a 9B+ scoring LM plus training data per domain — incompatible with the CLI's lazy-import, fast-fail design. **Recommendation:** keep TMR as primary; optionally add Fast-DetectGPT or Binoculars as an academic secondary scorer in benchmarks, not as a replacement. Do **not** integrate AdaDetectGPT into the live loop without a dedicated GPU path and explicit `--detector adadetect` opt-in.

---

## Primary URLs

| Resource | URL |
|----------|-----|
| **Paper (arXiv HTML v5)** | https://arxiv.org/html/2510.01268v5 |
| **Paper (PDF)** | https://arxiv.org/pdf/2510.01268 |
| **NeurIPS 2025 proceedings** | https://proceedings.neurips.cc/paper_files/paper/2025/file/808bc5e3d076c1125a87f81b42d5e52d-Paper-Conference.pdf |
| **OpenReview** | https://openreview.net/forum?id=3Qo2SRcHgU |
| **NeurIPS poster** | https://neurips.cc/virtual/2025/poster/120036 |
| **Official GitHub** | https://github.com/Mamba413/AdaDetectGPT |
| **Parent: Fast-DetectGPT** | https://github.com/baoguangsheng/fast-detect-gpt · [arXiv:2310.05130](https://arxiv.org/abs/2310.05130) |
| **Original DetectGPT** | [arXiv:2301.11305](https://arxiv.org/abs/2301.11305) (Mitchell et al., ICML 2023) |
| **Third-party explainer** | https://deep-paper.org/en/paper/2510.01268/ |
| **unslop detector module** | `unslop/scripts/detector.py` |
| **unslop TMR model** | https://huggingface.co/Oxidane/tmr-ai-text-detector |
| **RAID benchmark** | https://raid-bench.xyz/ |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | NeurIPS 2025 (poster #1803, Dec 5 2025) |
| **Authors** | Hongyi Zhou†, Jin Zhu†, Pingfan Su, Kai Ye, Ying Yang, Shakeel Gavioli-Akilagun‡, Chengchun Shi‡ |
| **Affiliations** | Tsinghua, Birmingham, LSE, CityU Hong Kong |
| **Equal contribution** | Zhou & Zhu (alphabetical) |
| **Corresponding** | Gavioli-Akilagun, Shi |
| **Funding** | EPSRC EP/W014971/1; NSFC 12271286 & 11931001; CSC |
| **License** | MIT (code); CC BY 4.0 (OpenReview) |

---

## Mechanism

### Lineage: DetectGPT → Fast-DetectGPT → AdaDetectGPT

**DetectGPT** (Mitchell et al., 2023) detects machine text via **probability curvature**: LLM-generated passages score higher on a normalized log-likelihood gap between the observed text and perturbed rewrites. Expensive — requires multiple LLM calls per passage for perturbation sampling.

**Fast-DetectGPT** (Bao et al., ICLR 2024) replaces perturbation sampling with **closed-form conditional expectations** from the source LLM's token distributions. Same curvature intuition, ~340× faster. Statistic (simplified):

\[
T(\mathbf{X}) = \frac{\sum_t \left[\log q'_t(X_t|X_{<t}) - \mathbb{E}_{\tilde{X}_t \sim s_t}\log q'_t(\tilde{X}_t|X_{<t})\right]}{\sqrt{\sum_t \mathrm{Var}_{\tilde{X}_t \sim s_t}(\log q'_t(\tilde{X}_t|X_{<t}))}}
\]

Classify as machine-generated if \(T(\mathbf{X}) > c\).

**AdaDetectGPT** modifies Fast-DetectGPT in two ways:

1. **Witness function \(w\):** Apply \(w(\log q_t(\cdot))\) instead of raw log-probs. The statistic becomes \(T_w(\mathbf{X})\) with the same martingale structure but transformed inputs. The paper proves cases where identity \(w\) fails but some learned \(w\) succeeds (the "Kingdom of Bit" toy example in §3).

2. **Adaptive threshold via MCLT:** Under white-box settings (\(q' = q\)), \(T_w(\mathbf{X})\) for machine text converges to \(\mathcal{N}(0,1)\) by the martingale CLT. Set threshold \(c = z_\alpha\) (the \(\alpha\)-quantile of standard normal) to control false negative rate at level \(\alpha\).

### Learning the witness function

Goal: maximize TNR at fixed FNR \(\alpha\). Direct optimization makes \(w\) depend on \(\alpha\). AdaDetectGPT instead maximizes a **TNR lower bound** (Theorem 1) that separates \(\alpha\) from \(w\) through a population quantity \(T_w^{(2*)}\).

Implementation:
- Function class: **B-spline basis** over log-probability space, \(\mathcal{W} = \{w(z) = \phi(z)^\top \beta : \|\beta\|_2 = 1\}\)
- Optimization reduces to solving **\(\Sigma \beta = \psi\)** (linear system)
- Training data: corpus of human passages \(\mathcal{H} = \{X^{(i)}\}_{i=1}^n \sim p\) (e.g., Wikipedia samples)
- Witness fit time: **<1 minute**, **<0.5 GB RAM** (Appendix F.3); dominated by LLM logit computation

Default B-spline config in code: `{"start": -32, "end": 0, "n_bases": 7, "spline_order": 2, "intercept": 1}`.

### White-box vs black-box

| Setting | Source LLM | Target LLM | Theory |
|---------|-----------|-----------|--------|
| **White-box** | Same as generator | Known open model | Full MCLT guarantees (Theorems 2–5) |
| **Black-box** | Open surrogate (Gemma-2-9b) | Closed (GPT-4o, Claude, Gemini) | Empirical only; guarantees don't transfer |

Black-box uses `google/gemma-2-9b` (sampling) + `google/gemma-2-9b-it` (scoring) as Fast-DetectGPT surrogates.

### Code architecture (`Mamba413/AdaDetectGPT`)

- **69 stars, 5 forks** (Aug 2026); last updated Aug 17 2026
- Fork of Fast-DetectGPT codebase; adds `detect_gpt_ada.py`, `local_infer_ada.py`
- Requirements: Python 3.10.8, PyTorch 2.7.0, CUDA GPU (paper used H20-NVLink 96GB; README notes typical usage needs less)
- Training JSON format:
  ```json
  {"original": ["human-text-1", ...], "sampled": ["machine-text-1", ...]}
  ```
- Pretrained witness params available (trained on GPT-4o / Gemini-2.5 / Claude-3.5 texts) for inference without retraining
- Bundled detector zoo: Binoculars, BiScope, DetectGPT, DNA-GPT, Fast-DetectGPT, GLTR, RADAR, RoBERTa, etc. — unified I/O for comparison

**Reproduction status:** Official repo ships experiment shell scripts (`exp_whitebox.sh`, `exp_blackbox_advanced.sh`, `exp_attack.sh`) and generated samples in `exp_gpt3to4/data/`. No independent third-party reproduction papers found (Aug 2026). Community uptake is early — low star count, zero GitHub issues filed at time of research.

---

## Benchmarks

### Datasets used (NOT MAGE / RAID / HC3)

AdaDetectGPT evaluates on **five domain-specific corpora**, following the Fast-DetectGPT protocol:

| Dataset | Domain | Protocol |
|---------|--------|----------|
| **SQuAD** | Wikipedia QA | 500 human paragraphs; LLM completes from first 120 tokens (up to 200 more) |
| **WritingPrompts** | Creative fiction | Same mixed human/LLM completion setting |
| **XSum** | News summarization | Same |
| **Yelp** | Product reviews | Same |
| **Essay** | Academic essays | Same |

Witness function trained on **two randomly selected datasets**, tested on the remaining three (cross-dataset generalization). This is a **custom 500-sample-per-dataset** setup, not the full MAGE (447k), HC3 (125k), or RAID (6.2M+) benchmarks.

**No published AdaDetectGPT numbers on MAGE, RAID, or HC3.** Cross-referencing sibling agents: TempParaphraser, CoPA, Adversarial Paraphrasing, and ToBlend all benchmark against Fast-DetectGPT on HC3/RAID — AdaDetectGPT is absent from those leaderboards.

### White-box results (Table 1, averaged across 5 source LLMs)

Source models: GPT-2 (1.5B), OPT-2.7B, GPT-Neo (2.7B), GPT-J (6B), GPT-NeoX (20B).

| Dataset | Fast-DetectGPT AUC (avg) | AdaDetectGPT AUC (avg) | Relative gain |
|---------|--------------------------|------------------------|---------------|
| SQuAD | 0.8571 | 0.8864 | +20.5% |
| WritingPrompts | 0.8886 | 0.9233 | +31.2% |
| XSum | 0.8009 | 0.8379 | +18.6% |

AdaDetectGPT wins **every cell** in Table 1 (all dataset × model combinations). Best single-cell example: WritingPrompts × GPT-2, Fast-DetectGPT 0.8972 → AdaDetectGPT 0.9352 (+36.9% relative).

Advanced LLMs (Qwen2.5-7B, Mistral-7B, LLaMA3-8B): consistent gains in Table S7.

### Black-box results (Table 2, Gemma-2-9b surrogate)

Targets: GPT-4o, Claude-3.5-Haiku. Average AUC across 4 datasets:

| Method | GPT-4o avg | Claude-3.5 avg |
|--------|-----------|----------------|
| RoBERTa-Base | 0.5655 | 0.5566 |
| Binoculars | 0.9552 | 0.9440 |
| RADAR | 0.8644 | 0.8507 |
| Fast-DetectGPT | 0.9571 | 0.9439 |
| **AdaDetectGPT** | **0.9589** | **0.9478** |

Gains over Fast-DetectGPT are **small in absolute terms** (0.001–0.004 AUC on most cells) but can reach **+20% relative** on Essay/GPT-4o. Fast-DetectGPT already saturates near 0.96–0.98 AUC; AdaDetectGPT squeezes marginal improvement. Binoculars and RADAR occasionally beat Fast-DetectGPT on specific dataset/model pairs — AdaDetectGPT doesn't dominate all supervised baselines.

### Adversarial attack results (Table 3)

Attacks follow Fast-DetectGPT protocol (Bao et al., 2024):
- **Paraphrasing:** LLM instructed to rephrase text
- **Decoherence:** Intentionally reduce text coherence to evade detection

| Attack | Fast-DetectGPT avg AUC | AdaDetectGPT avg AUC | Notes |
|--------|------------------------|----------------------|-------|
| Paraphrase (3 model configs) | 0.8679–0.8753 | 0.8781–0.8797 | +0.004–0.005 AUC; ≤10% relative |
| Decoherence (3 model configs) | 0.8449–0.8752 | 0.8882–0.9070 | Up to +0.05 AUC; up to 85% relative |

**Interpretation:** Paraphrase barely moves the needle — both methods stay above 0.87 AUC. This is **not** the same as cross-model paraphrase evasion (TempParaphraser, DIPPER, Adversarial Paraphrasing) which drives Fast-DetectGPT to near-random. Decoherence is where AdaDetectGPT's learned witness adds real value.

### Computational cost (Appendix F.3)

| Phase | Time | Memory |
|-------|------|--------|
| Witness training (vary \(d\)) | ~44 s | <0.5 GB |
| Witness training (vary \(n\)) | 9–70 s | 0.36–0.60 GB |
| Per-passage scoring | Dominated by LLM forward pass | Model-dependent (9B+ LM) |

Training is cheap; **inference requires full LLM logit computation** on every token — the bottleneck unslop's TMR avoids entirely.

---

## Debate

### What the field agrees on

1. **Logits/curvature signals work in controlled settings.** DetectGPT → Fast-DetectGPT → AdaDetectGPT shows incremental but real gains when you know (or can surrogate) the source model and have human training data.

2. **Statistical guarantees are novel.** Most detectors report AUC without FPR/FNR control. AdaDetectGPT's MCLT threshold selection and finite-sample bounds (Theorems 2–5) are a genuine contribution from the LSE/Tsinghua statistics group (Shi, Zhu, Gavioli-Akilagun have prior work on causal inference and treatment rules).

3. **Adaptive beats static on logits.** The witness function idea is sound: raw log-probability summation can cancel signal when human and machine distributions overlap in specific ways.

### Skepticism and limitations

1. **OpenReview TL;DR oversells:** "AdaDetectGPT is all your need for detecting LLM-generated text." Black-box gains are marginal at saturation; no RAID/MAGE/HC3; no cross-model paraphrase eval.

2. **Theory is white-box only.** Appendix G acknowledges: "its theoretical guarantees are mainly established in the white-box setting." Sampling temperature/top-k breaks the MCLT assumption; authors observe conservative FNR control (statistic shifts positive) but no formal fix.

3. **Sadasivan impossibility (TMLR 2025).** AdaDetectGPT cites Sadasivan et al. in related work but does not stress-test against their attack suite. Sadasivan's core claim — reliable detection is impossible under sufficiently strong adversaries — remains unaddressed. unslop's `detector.py` explicitly cites Nicks et al. (ICLR 2024): "we advise against continued reliance on LLM-generated text detectors."

4. **Non-native English bias (Liang et al., 2023).** Cited in related work; not evaluated. Logits-based methods inherit the ESL false-positive problem. TMR trained on RAID includes multilingual subsets but still faces this on OOD prose.

5. **Paraphrase attack definition mismatch.** AdaDetectGPT's "paraphrasing" attack rephrases text with an LLM — it's a **detector robustness test**, not an **evasion benchmark**. The evasion literature (Krishna et al. 2023, TempParaphraser EMNLP 2025, Adversarial Paraphrasing NeurIPS 2025) uses paraphrase to **hide AI text from detectors**. Those attacks are far stronger and target different failure modes.

6. **No RAID leaderboard submission.** Despite claims in some secondary sources, AdaDetectGPT has **not** been evaluated on the 672k-sample RAID test harness with 12 adversarial attacks. TMR's 99.28% RAID AUROC is on a fundamentally harder, standardized benchmark AdaDetectGPT hasn't touched.

7. **Same-family vulnerability.** AdaDetectGPT inherits Fast-DetectGPT's dependency on a scoring LM. If the scoring model family matches the generator family, curvature signals persist after light humanization. Cross-model paraphrase breaks the surrogate assumption — the exact technique unslop recommends when its ladder exhausts.

---

## Humanization and evasion

### Attacks that likely beat AdaDetectGPT (not directly tested)

| Attack | Effect on Fast-DetectGPT (parent) | Expected AdaDetectGPT impact |
|--------|-----------------------------------|------------------------------|
| **TempParaphraser** (EMNLP 2025) | 98.9% → 2.6% accuracy on HC3 | Likely severe — same logits family; witness trained on un-paraphrased human text |
| **Adversarial Paraphrasing** (NeurIPS 2025) | −98.96% T@1%FPR | Severe — guided paraphrase targets detector gradients |
| **Cross-model rewrite** (GPT→Claude) | Breaks surrogate scoring | Severe in black-box — Gemma surrogate mismatches post-rewrite token stats |
| **DIPPER** (NeurIPS 2023) | 72.9% Fast-DetectGPT accuracy remaining | Moderate-severe |
| **CoPA** (contrastive paraphrase) | 95.33% → 17.00% TPR on Fast-DetectGPT | Severe |
| **ToBlend** (token ensemble) | Fast-DetectGPT AUC 0.98 → 0.40 on advanced LLMs | Severe |
| **Naive synonym swap** | Can *increase* detection (+15% TPR on Fast-DetectGPT) | Humanization via synonym swap is counterproductive |

### Attacks AdaDetectGPT handles better than Fast-DetectGPT

| Attack | Mechanism | Gain |
|--------|-----------|------|
| **Decoherence** | Breaks text flow to flatten curvature | Up to 85% relative AUC improvement |
| **Light paraphrase** (paper's protocol) | Surface rewrite preserving LM token stats | ~0.5 AUC points |
| **Distribution shift** (Appendix F.4) | Train/test domain mismatch | Robust — maintains lead over baselines |

### Implications for unslop anti-detector mode

unslop's deterministic humanization (regex + structural + soul/contractions) targets **AI-ism removal and burstiness**, not logits curvature directly. The `feedback_loop` in `detector.py` escalates through balanced → full → structural+soul, scoring with **TMR** after each pass. When the ladder exhausts, it recommends **cross-model paraphrase** — exactly the attack AdaDetectGPT's paper doesn't test and Fast-DetectGPT's siblings can't survive.

AdaDetectGPT would be a **stricter** academic gate than TMR for logits-sensitive humanization (preserving GPT-family token patterns). It would **not** be a good proxy for commercial detectors (GPTZero, Turnitin, Copyleaks) that use proprietary supervised models closer to TMR's architecture.

---

## unslop integration

### Current `detector.py` design

```44:49:unslop/scripts/detector.py
DetectorName = Literal["tmr", "desklib"]
DEFAULT_DETECTOR: DetectorName = "tmr"

_MODEL_IDS = {
    "tmr": "Oxidane/tmr-ai-text-detector",
    "desklib": "desklib/ai-text-detector-v1.01",
```

| Dimension | TMR (current default) | AdaDetectGPT |
|-----------|----------------------|--------------|
| **Family** | Supervised RoBERTa classifier | Zero-shot logits + learned witness |
| **Input** | Raw text | Text + source/scoring LLM access |
| **Output** | P(AI) ∈ [0,1] via softmax | Curvature statistic vs MCLT threshold |
| **Model size** | ~125M params (~500MB) | 9B+ scoring LM + B-spline coeffs |
| **Inference cost** | Single 512-token forward pass | Full LM forward + token-wise log-prob aggregation |
| **Training** | Pre-trained on RAID (50k samples) | Requires human corpus per domain (~500+ passages) |
| **Offline** | Yes (HF cache) | Needs scoring LM in cache; witness can be pretrained |
| **RAID AUROC** | 99.28% (official leaderboard) | Not reported |
| **Statistical guarantees** | None (empirical) | FNR/TNR/TPR/FPR bounds (white-box) |
| **Paraphrase robustness** | Moderate (RAID-adversarial trained) | Untested on modern paraphrase attacks |

TMR's chunking strategy (510 tokens, max 4 chunks, mean probability) is tuned for long documents. AdaDetectGPT operates on full passages with zero-padding to fixed length \(L\).

### Architectural fit assessment

**Poor fit for live feedback loop:**
- Lazy import constraint: AdaDetectGPT needs `torch` + a 9B LM at scoring time — 10–30s load vs TMR's ~10–30s but with 10× memory
- No API for `score_ai_probability(text) -> float` without specifying scoring/sampling models and training data path
- Witness function is domain-specific; unslop humanizes arbitrary user prose (code docs, emails, essays) — would need universal pretrained witness or per-session training
- `ANTHROPIC_UNSLOP_SKIP_DETECTOR=1` escape hatch exists because detector deps are optional; AdaDetectGPT makes this worse

**Possible fit for offline benchmark harness:**
- Add to `benchmarks/detector_bench/` alongside TMR, Desklib, DivEye surprisal
- Use official pretrained witness params from `exp_gpt3to4/data/` for GPT-4o/Claude/Gemini detection scenarios
- Compare unslop humanization deltas across TMR vs AdaDetectGPT vs Fast-DetectGPT on fixed fixtures
- Report whether unslop's cross-model paraphrase recommendation actually drops AdaDetectGPT scores

**Possible fit for `--detector adadetect` opt-in (Phase 4+):**
- Only if user has GPU + cached Gemma-2-9b-it
- Ship pretrained B-spline coefficients as JSON (no runtime training)
- Map statistic to [0,1] via sigmoid for compatibility with `feedback_loop` threshold API
- Document: "academic scorer; not representative of commercial detectors"

### Comparison to Desklib (second unslop backend)

Desklib (`desklib/ai-text-detector-v1.01`) is another supervised encoder classifier — larger, slower, RAID top entry. AdaDetectGPT and Desklib occupy opposite poles: zero-shot logits vs fine-tuned embeddings. Neither replaces the other; ensemble disagreement between TMR/Desklib (supervised) and AdaDetectGPT (logits) could flag texts where humanization changed surface form but not token-level LM signature.

---

## Actions

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | **Do not integrate AdaDetectGPT into default feedback loop** | Cost, complexity, and attack-suite mismatch vs TMR |
| **P1** | **Run AdaDetectGPT on unslop benchmark fixtures** via official `local_infer_ada.py` + pretrained witness | Establish logits-family baseline; compare humanization delta to TMR |
| **P1** | **Test cross-model paraphrase against AdaDetectGPT** on 3–5 texts from `drafts/2026-05-detector-test/test-texts/` | Confirm expected collapse (TempParaphraser/Fast-DetectGPT precedent) |
| **P2** | **Submit Fast-DetectGPT (identity witness) to RAID** via `raid-bench` CLI as academic baseline | AdaDetectGPT inherits this; RAID numbers ground-truth the logits family vs TMR's 99.28% |
| **P2** | **Document detector family taxonomy in `docs/RESEARCH_AND_TECH.md`** | Supervised (TMR, Desklib) vs logits (DetectGPT family) vs surprisal (DivEye) vs watermark |
| **P3** | **Optional `--detector adadetect` backend** behind feature flag | For users with GPU who want MCLT-guaranteed FNR control in academic settings |
| **P3** | **Watch Zhou et al. follow-ups** (Learn-to-Distance ICLR 2026; Detecting LLM-Generated Text with Performance Guarantees arXiv:2601.06586) | Same author group extending statistical detection framework |

---

## Open questions

1. **Does the learned witness transfer across paraphrase?** The paper trains \(w\) on un-paraphrased human text. After TempParaphraser or cross-model rewrite, token log-prob distributions shift. No ablation exists.

2. **RAID-equivalent numbers?** Running AdaDetectGPT through `raid-bench` with Gemma-2-9b surrogate on 672k samples would finally compare apples-to-apples with TMR. Expected: strong on non-adversarial, weak on paraphrase/homoglyph attacks.

3. **Witness function interpretability.** What shape does learned \(w\) take? Monotonic? Sigmoid-like? Does it upweight low-probability tokens (DetectGPT intuition) or invert in some regions? The paper shows boxplots (Figure 2) but not the fitted spline.

4. **Interaction with unslop soul/contraction pass.** Contractions change tokenization ( `"do not"` → `"don't"` ). Logits-based scorers are tokenization-sensitive. Does humanization help or hurt AdaDetectGPT scores independent of AI-ism removal?

5. **Ensemble: TMR + AdaDetectGPT disagreement as signal.** If TMR says "human" but AdaDetectGPT says "machine," the text may have been humanized enough for supervised detectors but still carry LM token signatures — useful for anti-detector mode stopping criterion.

6. **Pretrained witness staleness.** Official pretrained params target GPT-4o/Gemini-2.5/Claude-3.5 (2025). As models update (GPT-5, Claude 4, etc.), do witnesses need retraining? The paper's distribution-shift analysis (Figure S7) suggests robustness, but only across their 5 datasets.

7. **Commercial detector proxy validity.** If unslop optimizes against TMR (RAID-trained RoBERTa), how well does that transfer to GPTZero/Turnitin/Copyleaks? AdaDetectGPT numbers wouldn't improve that transfer — different failure modes entirely.

---

*Agent #04 complete. Cross-refs: Agent #05 (Fast-DetectGPT), Agent #17 (Sadasivan impossibility), Agent #24 (TempParaphraser), Agent #25 (Adversarial Paraphrasing), Agent #34 (DivEye), Agent #35 (cross-model paraphrase), Agent #49 (burstiness/surprisal).*
