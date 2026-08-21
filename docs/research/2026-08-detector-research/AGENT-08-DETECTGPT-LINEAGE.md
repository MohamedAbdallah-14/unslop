# Agent #08 — DetectGPT / Curvature Detection Lineage

**Focus:** Mitchell et al. (ICML 2023) and the full successor tree — DetectGPT, Fast-DetectGPT, DNA-GPT, DetectLLM/LogRank, Binoculars, BiScope, Ghostbuster, AdaDetectGPT — plus benchmark evolution, paraphrase failure modes, and the 2026 "is curvature dead?" debate.  
**Date:** 2026-08-19  
**Scope:** Full internet research + read of `unslop/scripts/detector.py`.  
**Cross-refs:** Agent #04 (AdaDetectGPT), #24 (TempParaphraser), #26 (StealthRL), #28 (CoPA), #35 (cross-model paraphrase), #49 (burstiness/surprisal).

---

## Executive summary

**DetectGPT** (Mitchell et al., ICML 2023; [arXiv:2301.11305](https://arxiv.org/abs/2301.11305)) launched the **probability-curvature** family of zero-shot AI-text detectors. Core claim: text sampled from LLM \(p_\theta\) tends to sit in **negative-curvature regions** of \(\log p_\theta\) — minor perturbations (T5 mask-fills) drop log-probability more for machine text than human text. The **perturbation discrepancy** \(d(x) = \log p_\theta(x) - \mathbb{E}[\log p_\theta(\tilde{x})]\) approximates local Hessian trace via Hutchinson's estimator. On GPT-NeoX-20B fake news, DetectGPT reached **0.95 AUROC** vs **0.81** for the strongest perplexity baseline — a landmark result that spawned an entire research program.

The lineage evolved along three axes: **speed** (Fast-DetectGPT, ICLR 2024: closed-form conditional curvature, **340× faster**, ~**75% relative AUROC gain**), **black-box access** (DNA-GPT, Binoculars, Ghostbuster: no source-model logprobs), and **formal guarantees** (AdaDetectGPT, NeurIPS 2025: learned witness function + martingale CLT thresholds). By 2024–2026, curvature methods were standard baselines on **MAGE** (ACL 2024) and **RAID** (ACL 2024), often competitive in-distribution but **fragile under paraphrase**.

**The 2026 verdict on curvature is nuanced, not binary.** Curvature is **not dead as a research signal** — it still separates clean, unperturbed AI text in white-box settings, and Fast-DetectGPT remains a canonical academic baseline. It **is dead as a standalone deployment gate** under adversarial or even casual evasion: TempParaphraser drives Fast-DetectGPT from **98.9% → 2.6%** accuracy on HC3; Adversarial Paraphrasing cuts Fast-DetectGPT TPR@1%FPR by **98.96%**; StealthRL (Feb 2026) collapses Fast-DetectGPT AUROC to **~0.09** with **99.8% attack success**. Sadasivan et al. (TMLR 2025) and Nicks et al. (ICLR 2024) provide the theoretical frame: paraphrase shrinks total-variation distance; detector rewards are cheap to optimize against.

**GPT-PINT note:** No AI-text-detection paper titled "GPT-PINT" was found in this lineage. The homonym **PINT** (Prompt Injection Test, [Lakera AI](https://github.com/lakeraai/pint-benchmark)) benchmarks **prompt-injection guardrails**, not machine-generated prose detection — out of scope here. If the manifest intended a different paper, flag for correction.

**unslop uses TMR** (125M RoBERTa classifier, 99.28% RAID AUROC), **not** curvature. `detector.py` explicitly cites Nicks et al.: detectors are "a signal, not a gate." When the feedback ladder exhausts, it recommends **cross-model paraphrase** — the attack class that breaks curvature. **Recommendation:** keep TMR for the live loop; add Fast-DetectGPT + Binoculars as **optional academic scorers** in `benchmarks/detector_bench.py`, not production defaults. Do not imply deterministic unslop moves curvature statistics meaningfully.

---

## Primary URLs

| Resource | URL |
|----------|-----|
| **DetectGPT paper** | [arXiv:2301.11305](https://arxiv.org/abs/2301.11305) · [ICML 2023 proceedings](https://proceedings.mlr.press/v202/mitchell23a.html) |
| **DetectGPT code** | https://github.com/eric-mitchell/detect-gpt · demo: https://detectgpt.ericmitchell.ai |
| **Fast-DetectGPT** | [arXiv:2310.05130](https://arxiv.org/abs/2310.05130) · [ICLR 2024](https://iclr.cc/virtual/2024/poster/19201) · https://github.com/baoguangsheng/fast-detect-gpt · https://fastdetect.net/ |
| **DNA-GPT** | [arXiv:2305.17359](https://arxiv.org/abs/2305.17359) · [OpenReview](https://openreview.net/forum?id=Xlayxj2fWp) |
| **DetectLLM (LogRank)** | [arXiv:2306.05540](https://arxiv.org/abs/2306.05540) · https://github.com/mbzuai-nlp/DetectLLM |
| **Binoculars** | [arXiv:2401.12070](https://arxiv.org/abs/2401.12070) · https://github.com/ahans30/Binoculars |
| **BiScope** | NeurIPS 2024 · https://github.com/MarkGHX/BiScope |
| **Ghostbuster** | [arXiv:2305.15047](https://arxiv.org/abs/2305.15047) · https://github.com/vivek3141/ghostbuster |
| **AdaDetectGPT** | [arXiv:2510.01268](https://arxiv.org/abs/2510.01268) · https://github.com/Mamba413/AdaDetectGPT |
| **Sadasivan impossibility** | [arXiv:2303.11156](https://arxiv.org/abs/2303.11156) · [TMLR 2025](https://mlanthology.org/tmlr/2025/sadasivan2025tmlr-aigenerated/) |
| **Nicks evasion** | [ICLR 2024](https://arxiv.org/abs/2310.14720) · https://github.com/charlottttee/llm-detector-evasion |
| **MAGE benchmark** | [ACL 2024](https://aclanthology.org/2024.acl-long.3/) · https://github.com/yafuly/MAGE |
| **RAID benchmark** | [ACL 2024](https://aclanthology.org/2024.acl-long.674/) · https://raid-bench.xyz/ |
| **TempParaphraser attack** | [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1607/) |
| **Adversarial Paraphrasing** | [NeurIPS 2025](https://arxiv.org/html/2506.07001) |
| **StealthRL** | [arXiv:2602.08934](https://arxiv.org/html/2602.08934) |
| **unslop detector** | `unslop/scripts/detector.py` |

---

## 1. The curvature hypothesis (DetectGPT)

### 1.1 Mechanism

Mitchell, Lee, Khazatsky, Manning & Finn (Stanford) observed that **zeroth-order detection** — thresholding mean token log-probability (Solaiman et al. 2019; Gehrmann et al. 2019) — ignores local geometry. Their hypothesis:

> Minor rewrites of model-generated text tend to have **lower** log-probability under the source model than the original; human rewrites may go either direction.

Machine text therefore occupies **negative-curvature** neighborhoods (local maxima of \(\log p_\theta\)). DetectGPT operationalizes this:

1. **Perturb** passage \(x\) with T5 (or similar) mask-filling → \(\tilde{x}_1, \ldots, \tilde{x}_n\)
2. **Score** \(\log p_\theta(x)\) and \(\log p_\theta(\tilde{x}_i)\) under the **candidate source model**
3. **Compute** normalized perturbation discrepancy; classify as AI if discrepancy exceeds threshold

The paper connects discrepancy to **Hutchinson's trace estimator** for the Hessian of \(\log p_\theta\) — grounding "curvature" in differential geometry, not metaphor.

### 1.2 Design constraints

| Property | Implication |
|----------|-------------|
| **Zero-shot** | No labeled training data; uses source LM only |
| **White-box ideal** | Best when scoring model = generating model |
| **Expensive** | ~100 perturbations × forward passes per document |
| **Perturbation-dependent** | T5 rewrites must preserve semantics |

### 1.3 Original benchmarks (2023)

Datasets: **XSum**, **WritingPrompts**, **WMT16** (EN/DE), following prior work. Source models: GPT-2, GPT-Neo, GPT-J, GPT-NeoX-20B. Headline: **+0.14 AUROC** over best baseline on GPT-NeoX news (0.81 → 0.95). DetectGPT also beat supervised RoBERTa on some settings when the scoring model matched the generator.

**Limitations visible even in 2023:** Requires access to source-model logits. Breaks when scoring model ≠ generator (black-box ChatGPT). Slow. Sadasivan et al. (March 2023, same year) already showed recursive paraphrase breaks zero-shot classifiers including DetectGPT-class methods.

---

## 2. Lineage map: successors and cousins

```
Perplexity / GLTR (2019)
    │
    ├── DetectGPT (2023) ── perturbation curvature
    │       ├── DetectLLM-NPR (2023) ── normalized perturbed log-rank
    │       ├── Fast-DetectGPT (2024) ── conditional curvature, 340× speedup
    │       │       ├── AdaDetectGPT (2025) ── learned witness + MCLT thresholds
    │       │       └── Sentence-DetectGPT (2024) ── paraphrase robustness patch
    │       └── DNA-GPT (2023) ── divergent n-gram regen (different mechanism, same era)
    │
    ├── DetectLLM-LRR (2023) ── log-likelihood / log-rank ratio (no perturbation)
    ├── Binoculars (2024) ── perplexity / cross-perplexity ratio (curvature cousin)
    ├── BiScope (2024) ── bidirectional CE: forward prediction + backward memorization
    ├── Ghostbuster (2024) ── multi-LM probability features + linear classifier
    └── DivEye / SurpMark / TSD (2025–2026) ── surprisal dynamics (post-curvature frontier)
```

### 2.1 Fast-DetectGPT (Bao et al., ICLR 2024)

**Key insight:** Replace expensive perturbation with **closed-form conditional probability curvature**. At each token, compare \(\log p_\theta(x_t \mid x_{<t})\) to expectations over alternative token choices from sampling distribution \(s_t\). Machine text shows **positive conditional curvature** (~3 on average); human text clusters near **zero**.

| Metric | DetectGPT | Fast-DetectGPT |
|--------|-----------|----------------|
| 5-model AUROC (white-box avg) | 0.9554 | **0.9887** (+74.7% relative) |
| ChatGPT/GPT-4 (black-box) | 0.7225 | **0.9338** (+76.1% relative) |
| Speed | 1× | **340×** |

Black-box uses surrogate scoring models (e.g., GPT-Neo-2.7B for ChatGPT text). Fast-DetectGPT became the **de facto academic baseline** — bundled in MAGE, TempParaphraser, CoPA, AdaDetectGPT repos, and StealthRL evaluation panels.

### 2.2 DNA-GPT (Yang et al., 2023)

**Different mechanism, same generation.** Truncate text mid-passage; regenerate the remainder with the LLM; compare original vs. regenerated tails via **n-gram divergence** (black-box BScore) or **log-probability ratio** (white-box WScore). State-of-the-art on GPT-3.5/GPT-4 when API logprobs were available (text-davinci-003); black-box BScore works without token probabilities.

**Curvature connection:** White-box WScore assumes a "unique probability curve" for model continuations — philosophically aligned with DetectGPT but operationally distinct (regeneration vs. perturbation). **Critical 2023–2026 shift:** OpenAI ceased exposing token logprobs after GPT-3.5, killing white-box DNA-GPT for commercial targets. Paper explicitly notes rank/entropy methods fail without vocabulary-level probabilities.

### 2.3 DetectLLM / LogRank (Su et al., EMNLP 2023)

Two variants in the perturbation family:

- **DetectLLM-LRR:** Log-likelihood / log-rank ratio — fast, no perturbation (+3.9 AUROC absolute vs. SOTA)
- **DetectLLM-NPR:** Normalized perturbed log-rank — fewer perturbations than DetectGPT for same performance (+1.75 AUROC)

DetectLLM-NPR shares DetectGPT's perturbation sensitivity hypothesis but uses **token rank** instead of raw log-probability. Often grouped with curvature methods in surveys; Binoculars paper cites both as statistical-signature baselines.

### 2.4 Binoculars (Hans et al., ICML 2024)

**Not strictly curvature**, but same **logits-statistics** family. Score = \(\log \mathrm{PPL}_{\mathcal{M}_1}(s) / \log \mathrm{xPPL}_{\mathcal{M}_1,\mathcal{M}_2}(s)\) — ratio of observer perplexity to cross-perplexity under performer predictions. Claims **>90% detection at 0.01% FPR** on news/creative/essays with Falcon-7B pair.

**vs Fast-DetectGPT:** Binoculars uses two fixed open models; Fast-DetectGPT uses conditional expectations from one scoring LM. Both collapse under RL paraphrase (StealthRL: Binoculars AUROC **0.705 → 0.055**). RAID leaderboard: Binoculars **0.844 AUROC** vs DivEye **0.984**.

### 2.5 BiScope (Guo et al., NeurIPS 2024)

Extends the logits family **bidirectionally**: forward cross-entropy (next-token prediction) + backward cross-entropy (memorization of preceding token). AI text shows "unsure what to say next, strong memory of what was just said." **>0.95 avg F1** on commercial LLM outputs; cited as DivEye's closest zero-shot peer (~0.93–0.94 AUROC on MAGE).

Slides explicitly position against DetectGPT and Ghostbuster figures. Still a **trained classifier on statistical features**, not pure zero-shot threshold.

### 2.6 Ghostbuster (Verma et al., NAACL 2024)

**Probability-feature search**, not curvature per se. Passes documents through weaker LMs (unigram, trigram, GPT-3 ada/davinci); structured feature search + linear classifier. **99.0 F1 in-domain**, +41.6 F1 over DetectGPT. Does not need target-model logprobs — designed for ChatGPT/Claude black-box.

Important for lineage context: Ghostbuster's own eval notes DetectGPT "performs poorly when scoring and target models differ" — the black-box gap Fast-DetectGPT partially closed.

### 2.7 AdaDetectGPT (Zhou et al., NeurIPS 2025)

Latest curvature successor. Learns 1D **witness function** \(w(\log q_t)\) over token log-probs; thresholds via **martingale CLT** with finite-sample FPR/FNR bounds. Beats Fast-DetectGPT by **+12.5% to +37% relative AUC** on five custom splits. Paraphrase robustness gains **modest** (~0.5 AUC); decoherence attacks show up to **85% relative** improvement.

**Gap:** Not on MAGE/RAID/HC3. Does not test TempParaphraser, DIPPER, or cross-model paraphrase. See Agent #04 for full analysis.

### 2.8 Sentence-DetectGPT (IEEE CAIT 2024)

Defense patch for Fast-DetectGPT paraphrase fragility; no RAID/HC3 replication found.

---

## 3. Benchmark evolution

| Era | Benchmark | What changed | Curvature performance |
|-----|-----------|--------------|----------------------|
| **2023** | XSum, WritingPrompts, WMT16 | Single-domain, known source models | DetectGPT SOTA white-box |
| **2023** | HC3, OpenAI Classifier sets | ChatGPT-era black-box | DNA-GPT BScore; DetectGPT degrades |
| **2024** | **MAGE** (447k+ samples, 27 LLMs, 8 testbeds) | "In the wild" OOD | DetectGPT AUROC **0.92 → 0.55** on arbitrary-model testbed; Fast-DetectGPT stronger but imbalanced human/machine recall on Testbed 2 (**0.59 AUROC** per DivEye comparison) |
| **2024** | **RAID** (6M+ generations, 12 attacks) | Adversarial robustness standard | Fast-DetectGPT strong at low FPR naively (**0.88% FPR** at one threshold); **degrades under synonym swap, homoglyph**; paraphrase with GPT-2 sometimes *helps* detectors trained on similar-era data |
| **2025** | TempParaphraser HC3 suite | Detector-aware multi-sample paraphrase | Fast-DetectGPT **98.9% → 2.6%** |
| **2025–26** | StealthRL MAGE pool | RL paraphrase vs detector ensemble | Fast-DetectGPT AUROC **0.661 → 0.089**; TPR@1%FPR **0.388 → 0.002** |

**Pattern:** Curvature methods peak on **clean, in-distribution, unparaphrased** text with a well-matched scoring LM. Each benchmark generation added **OOD models, domains, or attacks** — where curvature bleeds accuracy fastest.

---

## 4. Known failure modes

### 4.1 Structural / access failures

| Failure | Affected methods | Mechanism |
|---------|------------------|-----------|
| **Scoring ≠ source model** | DetectGPT, Fast-DetectGPT | Curvature measured under wrong \(p_\theta\); surrogate mismatch |
| **No logprobs** | DetectGPT white-box, DNA-GPT WScore | API black-box (GPT-3.5+) |
| **Short text** | All logits methods | Insufficient tokens for stable curvature estimate |
| **Non-English** | Binoculars especially | Falcon-7B pair English-centric |
| **Human text in LM training mix** | All statistical | False positives on memorized/common phrases |

### 4.2 Attack failures (evasion)

| Attack | Effect on Fast-DetectGPT | Citation |
|--------|--------------------------|----------|
| **Naive paraphrase** | Can *increase* TPR@1%FPR (+15.03%) | Adversarial Paraphrasing 2025 |
| **Detector-guided paraphrase** | −98.96% TPR@1%FPR | Adversarial Paraphrasing 2025 |
| **TempParaphraser N=7** | 98.9% → 2.6% accuracy | EMNLP 2025 |
| **DIPPER** | Often *raises* detectability on some settings; 72.9% remaining on HC3 | CoPA 2025; TempParaphraser |
| **Cross-model rewrite** | Breaks surrogate-model assumption | unslop `detector.py` recommendation |
| **RL detector reward (StealthRL)** | AUROC → 0.089 | arXiv:2602.08934 v2 |
| **Recursive paraphrase** | Breaks zero-shot classifiers broadly | Sadasivan 2023/2025 |
| **Decoherence** | Text flow disruption; AdaDetectGPT handles better | AdaDetectGPT 2025 |

**Core vulnerability:** Curvature measures **how the scoring LM views this exact token sequence**. Any rewrite that preserves semantics but changes token-level probability geometry — especially via a **different model family** — destroys the signal. Paraphrase is curvature's kryptonite because it explicitly re-samples token choices.

### 4.3 ESL / low-perplexity human text

Liang et al. (2023): GPTZero-class tools flag **>50%** of TOEFL essays. Curvature methods share the low-perplexity false-positive failure mode with raw perplexity — formal, non-native, or templated human prose can look "machine-smooth." Binoculars marketed specifically against this; still not solved at scale.

---

## 5. Community debate: "Is curvature dead in 2026?"

### 5.1 The "dead" camp

**Evidence:**
- TempParaphraser, Adversarial Paraphrasing, StealthRL, DEPO (2026) all use Fast-DetectGPT as a **canary** — it dies first or nearly first.
- Sadasivan TMLR 2025: optimal detector AUROC → random as TV distance shrinks.
- Nicks ICLR 2024 (co-author: **Eric Mitchell**, DetectGPT lead): "advise against continued reliance on LLM-generated text detectors."
- Commercial pivot: GPTZero's 2023 burstiness/perplexity blog is **historical**; 2026 stack uses multi-model likelihood + adversarial training ([arXiv:2602.13042](https://arxiv.org/abs/2602.13042)).
- DivEye (TMLR 2026): Fast-DetectGPT **0.59 AUROC** on MAGE Testbed 2 vs DivEye **0.97** — global curvature alone insufficient for 2026 frontier models.

**Practitioner consensus:** Curvature is a **benchmark baseline**, not a product architecture. Nobody shipping Turnitin/GPTZero/Originality detection in 2026 relies on raw DetectGPT.

### 5.2 The "not dead" camp

**Evidence:**
- **Clean-text detection still works.** Fast-DetectGPT 0.93+ black-box AUROC on unparaphrased ChatGPT in original paper; AdaDetectGPT pushes toward 0.96–0.98 on controlled splits.
- **Research utility.** Curvature is the standard **zero-shot academic scorer** — every attack paper needs a Fast-DetectGPT row.
- **Composable signal.** DivEye fuses with Binoculars/Fast-DetectGPT (+18.7% AUROC); TSD combines with Fast-DetectGPT (Agent #02). Curvature is one feature, not the detector.
- **Watermarking alternative collapse.** Watermarks face spoofing (Sadasivan) and EU AI Act Article 50 constraints. Curvature remains a **post-hoc** option when you can't watermark.
- **Non-adversarial use cases.** ESL false-positive *defense* (unslop positioning): moving text away from machine-smooth curvature can help borderline human writers — different ethics than evasion.

### 5.3 Synthesis verdict (Aug 2026)

| Question | Answer |
|----------|--------|
| Is the **hypothesis false**? | **Partially context-dependent.** Holds on clean samples from known LMs; fails under paraphrase and model mismatch. |
| Is the **method family deployable alone**? | **No** for high-stakes or adversarial settings. |
| Is it **dead for research**? | **No** — still the canonical zero-shot logits baseline. |
| Is it **dead for unslop**? | **Never was live.** unslop uses TMR classifier + surprisal telemetry, not curvature. |

**One-liner:** Curvature isn't dead as a **feature**; it's dead as a **fortress**.

---

## 6. unslop `detector.py` — integration analysis

### 6.1 What unslop actually runs

```python
# unslop/scripts/detector.py — defaults
DetectorName = Literal["tmr", "desklib"]
DEFAULT_DETECTOR = "tmr"  # Oxidane/tmr-ai-text-detector, 125M RoBERTa
```

TMR is a **supervised RAID-trained classifier** — single forward pass, ~500MB, no scoring LM, offline-capable. Desklib is a larger RAID-top alternative. Neither computes perturbation discrepancy or conditional curvature.

The feedback loop escalates deterministic humanization (`balanced` → `full` → `full+structural+soul`), scores with TMR, stops at target or exhausts ladder. On exhaustion:

```395:407:unslop/scripts/detector.py
    recommendation = (
        f"ladder exhausted after {len(iterations)} iteration(s); "
        f"target {target} not reached (final p_ai={final_prob:.3f}). "
        "Next step is outside this module: paraphrase the text through a "
        "different model family (e.g. if generated by GPT, rewrite via Claude "
        "or Gemini). TempParaphraser (EMNLP 2025) and Adversarial Paraphrasing "
        "(NeurIPS 2025) document this as the single most reliable detector-"
        "evasion lever. Do NOT attempt watermark removal — EU AI Act Article 50 "
        "prohibits it."
    )
```

This is **architecturally correct** for the curvature literature: unslop's deterministic passes edit surface AI-isms and light stylometry; they do **not** re-sample token geometry under a surrogate LM. Measured TMR movement on fixtures is ~**0.0–0.2 pp** — consistent with not attacking curvature.

### 6.2 Should unslop add Fast-DetectGPT?

| Pro | Con |
|-----|-----|
| Academic honesty — score against the attack papers' baseline | Requires torch + 2.7B+ scoring LM (~1GB+); 10–30s load |
| Detect when deterministic pass accidentally *increases* curvature | Fast-DetectGPT collapses under the same paraphrase unslop recommends next |
| Benchmark alignment with StealthRL/CoPA/TempParaphraser panels | False confidence if users treat it as "passed Fast-DetectGPT = safe" |

**Recommendation (aligned with Agent #04):**
- **P1:** Add optional `fast_detectgpt` + `binoculars` scorers to `benchmarks/detector_bench.py` only.
- **P2:** Log `surprisal_stdev` (already in feedback loop) — orthogonal to curvature, closer to DivEye.
- **Do not** integrate AdaDetectGPT or DetectGPT into live CLI without `--detector` opt-in and GPU path.
- **Do not** claim anti-detector mode "beats Fast-DetectGPT" — StealthRL proves dedicated RL does; unslop doesn't.

### 6.3 Threat-model alignment

| Tier | Capability | vs Curvature |
|------|------------|--------------|
| **T1** | Regex unslop (deterministic) | Does not target logits geometry |
| **T2** | LLM anti-detector polish | May shift perplexity; unlikely to survive Fast-DetectGPT under TempParaphraser-class attacks |
| **T3** | Cross-model / RL paraphrase | Collapses Fast-DetectGPT, Binoculars, TMR — StealthRL upper bound |

unslop honestly occupies **T1–T2**. The detector module's Nicks citation and ladder-exhaustion message are the right guardrails.

---

## 7. Open questions

1. Does AdaDetectGPT's witness function survive TempParaphraser? No published test.
2. What paper did "GPT-PINT" refer to? Not found in this lineage (Lakera PINT is prompt-injection, not AI-text).
3. Optimal 2026 stack is likely multi-signal (curvature + surprisal dynamics), not another curvature tweak alone.

---

## 8. Key numbers reference

| Result | Value | Source |
|--------|-------|--------|
| DetectGPT vs perplexity (GPT-NeoX news) | 0.95 vs 0.81 AUROC | Mitchell ICML 2023 |
| Fast-DetectGPT speedup | 340× | Bao ICLR 2024 |
| Fast-DetectGPT black-box ChatGPT | 0.9338 AUROC | Bao ICLR 2024 |
| MAGE arbitrary-model DetectGPT | ~0.55 AUROC | Li ACL 2024 |
| TempParaphraser → Fast-DetectGPT | 98.9% → 2.6% accuracy | Huang EMNLP 2025 |
| Adversarial Paraphrasing → Fast-DetectGPT T@1%F | −98.96% | NeurIPS 2025 |
| StealthRL → Fast-DetectGPT AUROC | 0.661 → 0.089 | arXiv:2602.08934 v2 |
| StealthRL → Binoculars AUROC | 0.705 → 0.055 | arXiv:2602.08934 v2 |
| unslop TMR RAID AUROC | 99.28% | Oxidane HF model card |
| unslop deterministic TMR delta | ~0.0–0.2 pp | Agent #35 fixtures |

---

*Agent #08 complete. Curvature lineage documented from DetectGPT (2023) through AdaDetectGPT (2025), with 2026 evasion upper bounds (StealthRL) and unslop TMR architecture confirmed as the correct production choice.*
