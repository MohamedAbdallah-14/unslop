# Agent #03 — SurpMark (GJS Transition Detection for AI Text)

**Focus:** Paper, implementations, benchmarks, discourse, evasion implications, unslop integration.  
**Date:** 2026-08-19  
**Research window:** ~35 min (web search, arXiv v3, GitHub, cross-memo audit)

---

## Executive summary

**SurpMark** (Chen & Khisti, University of Toronto / Vector Institute) is a black-box AI-text detector that treats attribution as a **likelihood-free hypothesis test** on **discretized surprisal state transitions**, not scalar perplexity or global variance. Token surprisals from a proxy LM are k-means-binned into interpretable states (e.g., Predictable → Highly Surprising); each passage becomes a first-order Markov transition matrix; detection score is the **generalized Jensen–Shannon (GJS) gap** between how close that matrix sits to pre-built human vs. machine reference matrices.

The paper is **arXiv:2510.07500** (v3, Oct 2025), accepted at **ICML 2026** (poster #503, Jul 6). It was also submitted to **ICLR 2026** (OpenReview `eDJsc3KXZC`); venue status on OpenReview was not retrievable (bot wall). Official code: **https://github.com/shuangyichen/SurpMark** — a `surpmark` Python package, **no HuggingFace model hub entry** (uses off-the-shelf proxy LMs via Transformers).

Empirically, SurpMark **matches or beats 13 baselines** (DetectGPT, Fast-DetectGPT, Lastde++, Binoculars, DNA-GPT, R-Detect, etc.) on open-source generators (avg AUROC **91.17%** across 9 models × 3 datasets) and is **best on closed-source** models where marginal surprisal collapses (avg **78.32%** vs. Binoculars 65.09%). Its headline robustness claim: **transition dynamics survive paraphrase** — Table 9 reports **99.2–99.8% AUROC** under Polish/DIPPER/back-translation OOD, vs. Fast-DetectGPT 83–98%. The mechanism is the **recovery phenomenon**: after a high-surprisal token, LLM text snaps back to predictable glue faster than human prose.

**unslop gap:** `surprisal.py` already computes DivEye-aligned global stats plus first/second-order **delta** features, but has **zero** discretization, transition-matrix estimation, reference corpora, or ΔGJS scoring. `detector.py` optimizes against TMR/Desklib classifiers, not SurpMark dynamics. For anti-detector mode, SurpMark defines a **new evasion axis**: not just raising `surprisal_stdev`, but **breaking machine-like transition patterns** (anti-recovery, messier post-spike continuations).

**Internet discourse:** Minimal. GitHub shows **0 stars / 0 forks** (Aug 2026). No substantive Twitter/Reddit thread surfaced. Reception is academic: alphaXiv overview, papernotes.org ICML summary, ICML virtual poster. No commercial detector (GPTZero, Turnitin) claims SurpMark integration yet — paper cites GPTZero only as related work in Appendix C.

---

## URLs

| Resource | URL |
|----------|-----|
| **Paper (arXiv)** | https://arxiv.org/abs/2510.07500 |
| **Paper (HTML v3)** | https://arxiv.org/html/2510.07500v3 |
| **Paper (PDF)** | https://arxiv.org/pdf/2510.07500 |
| **DOI** | https://doi.org/10.48550/arxiv.2510.07500 |
| **OpenReview (ICLR 2026 sub.)** | https://openreview.net/forum?id=eDJsc3KXZC |
| **ICML 2026 poster** | https://icml.cc/virtual/2026/poster/65399 |
| **Official GitHub** | https://github.com/shuangyichen/SurpMark |
| **alphaXiv overview** | https://www.alphaxiv.org/overview/2510.07500 |
| **Paper note (papernotes.org)** | https://en.papernotes.org/ICML2026/aigc_detection/black-box_detection_of_llm-generated_text_using_generalized_jensen-shannon_diver/ |
| **Related: DivEye (unslop baseline)** | https://arxiv.org/abs/2509.18880 · https://github.com/IBM/diveye |
| **Related: Lastde++ (closest baseline)** | https://arxiv.org/abs/2410.06072 |
| **Related: Fast-DetectGPT** | https://arxiv.org/abs/2310.05130 |
| **Related: R-Detect (kernel relative test)** | Song et al., 2025 (cited in paper) |
| **Benchmark: DetectRL** | Used for mixed-domain, paraphrase OOD, cross-reference |
| **Benchmark: Kaggle DAIGT V2** | 15+ generators, Appendix Table 33 |
| **unslop surprisal module** | `unslop/scripts/surprisal.py` |
| **unslop detector module** | `unslop/scripts/detector.py` |
| **Cross-memo (Agent #55)** | `docs/research/2026-08-detector-research/AGENT-55-SURPRISAL-DYNAMICS-BEYOND-DIVEYE.md` |

**HuggingFace:** No `surpmark` or Chen/Khisti detector weights on HF Hub. Repo downloads standard proxy LMs (GPT-2 family, Llama, Qwen, etc.) at runtime via `transformers`.

**Third-party implementations:** None found beyond the official repo. No PyPI package indexed under `surpmark` as of this search.

---

## Mechanism

### Pipeline (offline + online)

1. **Proxy LM forward pass.** For each token \(x_t\), compute surprisal \(s_t = -\log p(x_t \mid x_{1:t-1})\) under a black-box scorer (GPT-2 Large default in throughput experiments; paper sweeps proxy size).

2. **Shared discretization.** Pool surprisals from reference corpora; **k-means** into \(k\) states (optimal \(k \approx 6\)–7 empirically; theory: \(k^* = \Theta(N^{1/5})\) for reference token count \(N\)). Equal-width / equal-mass binning are ablated and worse.

3. **Transition matrix.** Map discretized sequence \(\{a_1,\ldots,a_n\}\) to empirical first-order matrix \(\hat{M}_T\) where \(\hat{M}_T(j|i)\) = P(state \(j\) follows state \(i\)). **Higher-order Markov hurts** (state-space explosion; Table 10, Figure 2b).

4. **Reference matrices (built once).** From human corpus → \(\hat{M}_Q\); from machine corpus → \(\hat{M}_P\). Same quantizer \(q_k\).

5. **GJS score.** Generalized Jensen–Shannon divergence between reference and test matrices:
   \[
   \text{GJS}(M_A, M_B, \alpha) = \frac{\alpha}{1+\alpha} D_{\text{KL}}(M_A, M_\alpha) + \frac{1}{1+\alpha} D_{\text{KL}}(M_B, M_\alpha)
   \]
   with mixture \(M_\alpha = \frac{\alpha}{1+\alpha}M_A + \frac{1}{1+\alpha}M_B\), \(\alpha\) = reference/test length ratio.

6. **Decision statistic:**
   \[
   \Delta\text{GJS}_n = \text{GJS}(\hat{M}_P, \hat{M}_T, \alpha) - \text{GJS}(\hat{M}_Q, \hat{M}_T, \alpha)
   \]
   Positive → closer to machine reference. **Proposition 3.4:** equivalent to normalized generalized log-likelihood ratio (extends Gutman 1989 universal test to two references).

### The recovery phenomenon (core AI tell)

Figure 2(a) visualizes the discriminative signal: under 5-bin discretization, LLM text shows:
- **Stronger recovery:** P(transition *into* predictable state | leaving highly-surprising state) is higher for machines.
- **Spiking from low-surprisal contexts:** machines spike to surprising tokens from predictable runs more sharply.

Human text maintains **messier** transition structure — spikes don't always resolve immediately into function-word glue.

### Why this differs from DivEye (unslop's current surprisal stack)

| Aspect | DivEye (Basani et al., TMLR 2026) | SurpMark |
|--------|-----------------------------------|----------|
| Summary | 10 global distributional features on surprisal sequence (mean, σ, skew, Δ, Δ² stats) | Discrete-state **transition matrix** |
| Classifier | Trained XGBoost (or features alone) | Fixed reference corpora + hypothesis test |
| Paraphrase story | Intra-doc variance / Δ² block survives rewrite | **Transition pattern** invariant to surface form |
| Closed-source SOTA | Marginal stats weaken as models improve | **Transition gap persists** (Appendix E.2.12) |
| unslop status | `surprisal.py` bit-matched measurement | **Not implemented** |

DivEye's `delta2_surprisal_autocorr` and `delta2_surprisal_entropy` in unslop are **related intuitions** (local dynamics) but are **not** equivalent to a k-state Markov matrix compared via GJS. SurpMark is closer to Lastde++ (discretized probability sequences) but operates on **surprisal states** with explicit two-reference GJS rather than diversity entropy alone.

### API (official repo)

```python
import surpmark
surpmark.compute_gjs(
    p_text=human_training_text,      # builds human reference side
    q_text=ai_training_text,         # builds machine reference side
    ai_test_text=ai_test_text,
    human_test_text=human_test_text,
    device_id=0,
    max_text_length=256,
    verbose=False,
)
```

Requires PyTorch + Transformers. Reference corpora are **caller-supplied** — no bundled weights.

---

## Benchmarks

### Standard black-box setting (Tables 2–3)

**Datasets:** XSum, WritingPrompts, SQuAD. **9 open-source + 3 closed-source** generators. **13 baselines.**

**Open-source avg AUROC (across models, Table 2):**

| Method | Avg AUROC |
|--------|-----------|
| **SurpMark\(_{k=7}\)** | **91.17%** |
| **SurpMark\(_{k=6}\)** | **91.23%** |
| Lastde++ | 90.04% |
| Fast-DetectGPT | 88.01% |
| Binoculars | 86.19% |
| DetectGPT | 80.37% |

SurpMark ranks **1st on 6/9** open-source models, top-2 on 7/9.

**Closed-source avg AUROC (Table 3):**

| Method | Gemini-1.5-Flash | GPT-4.1-mini | GPT-5-Chat | **Avg** |
|--------|------------------|--------------|------------|---------|
| **SurpMark\(_{k=7}\)** | 75.14 | 78.48 | **81.33** | **78.32%** |
| SurpMark\(_{k=6}\) | 74.57 | 80.25 | 78.33 | 77.72% |
| R-Detect | 69.25 | 71.64 | 67.75 | 69.55% |
| Binoculars | 74.51 | 71.12 | 49.65 | 65.09% |
| Fast-DetectGPT | 72.49 | 68.32 | 43.39 | 61.40% |
| DetectGPT | 69.19 | 70.08 | 54.60 | 64.75% |
| Lastde++ | 71.72 | 68.23 | 43.51 | 61.15% |

Key insight from authors: on frontier models, **marginal surprisal distributions overlap human**; **transition gap** remains. SurpMark wins GPT-5-Chat by ~30 AUROC points over Lastde++.

**DivEye:** Not included in SurpMark benchmark tables (different publication track; DivEye PAN/TMLR numbers not directly comparable without shared eval harness).

### Cost / throughput

- Reference budget \(B = \#\text{refs}/\#\text{tests}\): SurpMark at **B=2** vs. DetectGPT/Lastde++/DetectNPR at **B=100**, DNA-GPT at B=10.
- **No per-input regeneration** (unlike DetectGPT curvature sampling).
- Throughput crosses Fast-DetectGPT at ~**298 test items** after one-time reference preprocessing (Figure 6, RTX 4090, GPT-2 Large proxy).

### Robustness suites

**Mixed-domain / mixed-generator (DetectRL, Tables 5–6):** SurpMark best AUROC on all source-model groups; e.g., Claude-instant: SurpMark **80.92%** vs. Fast-DetectGPT **37.16%** (below chance).

**Cross-reference / domain shift (Table 7):** +13.26 avg AUROC vs. strongest baseline in genuine cross-reference settings.

**Sentence-level corruption (Table 8):** Best on human/machine mixed sentences.

**Paraphrase OOD (Table 9 — references unparaphrased, tests paraphrased):**

| Setting | Fast-DetectGPT | Lastde++ | **SurpMark** |
|---------|----------------|----------|--------------|
| Polish | 83.47 | 82.37 | **99.21** |
| DIPPER | 94.70 | 92.82 | **99.45** |
| Back-translation | 97.69 | 94.31 | **99.79** |

**T5-Paraphraser attack (Table 23, Test-P = realistic):** SurpMark drops **≤0.67 AUROC** on SQuAD; Lastde++ drops **5.2**.

**Prompt-engineered evasion (Table 24):** "Write to evade detectors" — Lastde++ −11.5 to −15.6 AUROC; SurpMark test-attack −1.98 to −5.01.

**Non-English (Figure 7):** German WMT19, Chinese HC3 — SurpMark ranks first.

**Short text:** AUROC climbs sharply from 50→150–200 tokens; weak below ~100 tokens (theory degrades at small \(N\)).

**Commercial detectors:** Paper does **not** benchmark GPTZero, Turnitin, Copyleaks, or Originality.ai. GPTZero cited as early likelihood detector (Tian 2023) in related-work appendix only.

### Sensitivity

- **k-means > equal-width > equal-mass** for discretization.
- **k=6–7** sweet spot; overshooting k hurts with limited reference data.
- **Proxy LM:** SurpMark stable across proxy sizes; several baselines collapse or invert on mismatch.
- **First-order >> unigram** state distribution (Table 25) — transitions matter, not just state marginals.

---

## Debate

### What exists

- **Academic reception:** ICML 2026 acceptance; alphaXiv and papernotes.org summaries emphasize theoretical grounding (Gutman-style LFHT, asymptotic normality of ΔGJS) vs. ad-hoc heuristics.
- **Author self-critique (Limitations + Impact Statement):** (1) Markov assumption is on **discretized proxy states**, not true token generation. (2) Human text in pretraining may look LLM-smooth → **false positives** (Appendix E.2.18). (3) **Not forensic evidence** — high AUROC ≠ reliable individual case; no sole basis for academic penalties.
- **Venue duality:** Same work on OpenReview as ICLR 2026 submission **and** ICML 2026 poster — suggests revision between submissions; v3 arXiv adds blue theory blocks per OpenReview diff hints.

### What does not exist (Aug 2026)

- No viral community thread, HN front page, or detector-vendor response.
- No independent reproduction blog with conflicting numbers.
- No OpenReview public reviews retrieved (Cloudflare block).
- GitHub repo **0 stars** — code release is fresh/low-visibility.

### Skeptical readings (inferred, not sourced from debate)

1. **Reference dependence:** Real deployment needs curated human + machine reference pools; domain shift in references may hurt despite cross-domain experiments.
2. **Paraphrase OOD vs. humanization:** Table 9 tests paraphrase that **preserves source identity** — aggressive cross-model rewrite (unslop's recommended next step when TMR fails) may shift transition structure more than DIPPER.
3. **Mixed-text / human-edited AI:** Paper acknowledges human-edited LLM outputs sit between classes → threshold \(\tau\) misclassification (papernotes.org flags this).
4. **Arms-race framing:** Nicks et al. (ICLR 2024) caution against detector reliance — SurpMark's authors echo this in Impact Statement; unslop `detector.py` cites the same.

---

## Humanization (evasion and defensive use)

### What SurpMark rewards as "human"

From recovery analysis and transition ablations:

- **Slower snap-back** after lexical surprises — don't immediately follow an unusual word with "Furthermore," "In addition," or other high-probability glue.
- **Messier state wandering** — human transitions among surprisal bins are less deterministic; fewer low→spike→low oscillations.
- **Sustained mid-surprisal runs** — not uniformly smooth (low DivEye σ alone is insufficient if transitions stay machine-like).
- **Less pronounced spiking from predictable contexts** — avoid the LLM pattern of rare word in an otherwise boilerplate sentence.

### What unslop already does (partial overlap)

| unslop lever | SurpMark axis | Effect |
|--------------|---------------|--------|
| `structural.py` sentence split/merge | Indirect — changes token context boundaries | May alter transition counts; not targeted |
| Stock vocab / filler removal | Reduces predictable glue tokens | **Anti-recovery** if unusual words aren't followed by new glue |
| `soul.py` contractions | Token-level distribution shift | Minor transition effect |
| Anti-detector LLM mode ("vary surprisal") | DivEye σ intent | **Incomplete** without transition awareness |
| Cross-model paraphrase (detector.py recommendation) | Strongest evasion per NeurIPS 2025 lit | May reshuffle transitions; **untested vs SurpMark** |

### Anti-patterns (still look machine to SurpMark)

- **Random synonym injection** without restructuring follow-up tokens — spike without messy continuation.
- **Uniform smoothing** (short sentences, balanced rhythm) — may pass TMR while retaining recovery transitions.
- **Prompt "write messily"** — Table 24 shows Attack 1/2 drops SurpMark only ~2–5 AUROC vs. ~12–15 for Lastde++ — **explicit evasion prompts are weak** against transition features.

### Defensive use (ESL / false-positive mitigation)

SurpMark's limitation on pretraining-smoothed human text is relevant: non-native writers with formulaic phrasing may score machine-like on **transitions**, not just σ. unslop anti-detector mode should **not** assume SurpMark evasion = ethical default — boundary in `skills/unslop/SKILL.md` applies.

---

## unslop integration

### Current state (`surprisal.py`)

Implements real DivEye measurement via local LM (`distilgpt2` default):

- `surprisal_stdev`, `surprisal_variance`, skew, kurtosis
- `delta_surprisal_*`, `delta2_surprisal_variance/entropy/autocorr`
- `to_diveye_vector()` → 10-float IBM-aligned vector

**Missing for SurpMark parity:**

1. k-means discretization of surprisal stream (shared quantizer persistence)
2. First-order transition matrix estimation
3. Offline reference corpus builder (\(\hat{M}_P\), \(\hat{M}_Q\))
4. GJS / ΔGJS computation
5. Threshold calibration and classification output

`delta2_surprisal_autocorr` captures sequential dependence in **continuous** surprisal deltas; SurpMark captures **categorical** state transitions — complementary, not redundant.

### Current state (`detector.py`)

- Backends: **TMR** (RoBERTa classifier), **Desklib** — supervised embeddings, not surprisal dynamics.
- `feedback_loop()` optionally logs `surprisal_stdev` per iteration via `surprisal_fn`; **not** a stop criterion.
- Escalation ladder: balanced → full → full+structural+soul; no transition-aware pass.

### Relationship to Agent #55 memo

Agent #55 covers TSD + SurpMark + late-stage stack as one "dynamics beyond DivEye" audit. **This memo (#03) owns SurpMark specifically:** paper, code, benchmarks, discourse. Implementation recommendations align:

| Priority | Action |
|----------|--------|
| **P0** | Document SurpMark in detector research index; add to `AGENT-MANIFEST-100.md` row 3 as **done** |
| **P1** | Extend `benchmarks/` with before/after ΔGJS on fixture corpus (clone `surpmark` or port `compute_gjs` logic) |
| **P2** | `compute_surpmark_reading(text) -> {delta_gjs, transition_matrix, k}` in `surprisal.py` or sibling module |
| **P2** | Store reference matrices under `benchmarks/fixtures/surpmark_refs/` (license: verify corpus sources) |
| **P3** | Anti-detector skill addendum: **anti-recovery** editing heuristic (prose rule, not regex) |
| **P3** | Optional third oracle in `feedback_loop`: stop when ΔGJS < human-calibrated threshold **and** TMR < target |

### Minimal port estimate

SurpMark core (discretize + count transitions + GJS) is ~100–150 LOC on existing surprisal tensor from `compute_surprisal_variance`. Heavy lift is **reference corpus curation** and calibration, not LM inference (already in unslop).

---

## Actions

1. **Pin paper + commit hash** when cloning `shuangyichen/SurpMark` for benchmark port; repo had 0 stars — monitor for updates post-ICML.
2. **Run head-to-head** on `benchmarks/fixtures/*.md`: TMR vs. DivEye vector vs. SurpMark ΔGJS before/after each humanize intensity — fills gap noted in Agent #49/#50.
3. **Evaluate proxy LM choice:** unslop uses `distilgpt2`; SurpMark paper uses GPT-2 Large for throughput, sweeps smaller proxies successfully — document rank-order stability on humanized outputs.
4. **Do not ship SurpMark as gate** without dual-oracle — align with Nicks et al. and paper Impact Statement.
5. **Cross-link Agent #1 (DivEye)** and **Agent #55 (dynamics stack)** — SurpMark is the transition-detection complement to DivEye's global σ story.
6. **Track ICLR/OpenReview outcome** if public reviews appear — may contain robustness critiques not in camera-ready.

---

## Open questions

1. **Direct DivEye vs. SurpMark ablation:** Neither paper cross-benchmarks the other. Does XGBoost on DivEye features + SurpMark ΔGJS beat either alone on paraphrased RAID/MAGE?
2. **unslop humanize effect on ΔGJS:** Does deterministic unslop (no LLM) move transition matrices toward human references, or only TMR scores?
3. **Reference corpus for product:** What human/AI reference mix matches unslop's target domains (README edits, commit messages, Medium posts)?
4. **Cross-model paraphrase vs. Table 9:** DIPPER/back-trans preserve authorship labels; Claude→GPT rewrite may break transitions more — evasion or detection?
5. **Short-form content:** Tweets, PR titles (<50 tokens) — SurpMark theory predicts degradation; is unslop's primary use case safe?
6. **ESL false positives:** Appendix E.2.18 analysis depth — quantitative FPR on non-native English not extracted in this pass.
7. **Commercial detector convergence:** Will GPTZero/Turnitin 2026 models internalize transition features (cf. GPTZero arXiv:2602.13042 citing likelihood-feature families)?
8. **ICLR vs. ICML version diff:** v1 arXiv claimed asymptotic normality prominently; v3 emphasizes discretization scaling — confirm final ICML theorem set.
9. **PyPI packaging:** Will authors publish `surpmark` to PyPI or remain git-install-only?
10. **Legal/ethical:** SurpMark as feedback oracle in anti-detector mode — same boundaries as TMR (defensive ESL/resume use only).

---

## References (BibTeX from authors)

```bibtex
@misc{chen2026blackboxdetectionllmgeneratedtext,
  title={Black-Box Detection of LLM-Generated Text Using Generalized Jensen-Shannon Divergence},
  author={Shuangyi Chen and Ashish J Khisti},
  year={2026},
  eprint={2510.07500},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2510.07500},
}
```

---

**One-line takeaway:** SurpMark detects AI text by comparing **surprisal state transition matrices** to human/machine references via **ΔGJS**, exploiting LLM **recovery** after surprising tokens — a signal that survives paraphrase and closed-source marginal collapse. unslop measures DivEye globals and TMR classification but is **blind to Markov transitions**; closing that gap is the next surprisal-humanization layer after σ.
