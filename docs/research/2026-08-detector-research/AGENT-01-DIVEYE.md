# Agent #01 — DivEye (Surprisal Variance Detection)

**Focus:** Theory, detection landscape, community debate, humanization implications — not IBM code audit (see Agent #34).  
**Date:** 2026-08-19  
**Authors (paper):** Advik Raj Basani & Pin-Yu Chen (IBM Research / BITS Goa)

---

## 1. Executive summary

- **DivEye** (*Diversity Boosts AI-Generated Text Detection*, [arXiv:2509.18880](https://arxiv.org/abs/2509.18880), **TMLR 2026**) argues that **intra-document surprisal variance and its temporal dynamics** — not mean perplexity alone — distinguish human from AI text. LLM outputs are "uniformly smooth"; human prose alternates predictable glue spans with sharp lexical surprises.

- The method extracts a **9-dimensional feature vector** (paper Eq. 6) from token surprisal \(S(x_t) = -\log P(x_t \mid x_{<t})\) computed by a frozen observer LM (default **GPT-2**). Features span distributional moments, first-order differences \(\Delta S_t\), and second-order dynamics \(\Delta^2 S_t\) (variance, 20-bin entropy, lag-1 autocorrelation). An **XGBoost classifier** is trained on these features — they are not a detector by themselves.

- **Reported headline numbers:** up to **33.2%** improvement over zero-shot baselines; **+18.7%** AUROC when fused with existing detectors; **0.984 AUROC** on RAID (within **0.20%** of leader e5-small-lora); **0.87 AUROC** under GPT-3.5 paraphrase (vs Longformer 0.76); **~0.01 s/sample** inference (~**2971×** faster than RAiDAR per paper).

- **vs legacy zero-shot:** DivEye beats **Binoculars** (RAID AUROC 0.844 → 0.984, **−14.4 pp**), **FastDetectGPT** (MAGE Testbed 2 AUROC 0.59 → 0.97), and **DetectGPT-class curvature** methods on most MAGE testbeds. **BiScope** is the closest zero-shot peer (often 0.93–0.94 AUROC); DivEye+BiScope is the deployed HF Space ensemble.

- **Community footprint is thin.** No dedicated Hacker News or Reddit threads found (Aug 2026). Academic reception is positive (TMLR acceptance, PAN@CLEF 2025 participation). Third-party summaries (Moonlight, IBM Research page) are uncritical. Skepticism comes indirectly from the broader detection literature (Sadasivan limits, Pangram on perplexity/burstiness fragility, short-text weakness acknowledged in Appendix J).

- **Humanization implication:** Raising **surprisal σ**, **Δσ**, and especially **\(H_{\Delta^2}\)** and **\(\rho_{\Delta^2}\)** is the offensive mirror of DivEye. Paraphrase attacks collapse mean perplexity but **burstiness/variance survives** (HumanizeMyAI replication). unslop already measures the IBM 10-feature vector in `surprisal.py` but does **not** optimize against it in anti-detector mode — only logs optional `surprisal_stdev` telemetry in `detector.feedback_loop()`.

- **2026 frontier:** DivEye captures **global** temporal statistics. **TSD** (Sun et al., [arXiv:2601.04833](https://arxiv.org/abs/2601.04833)) targets **late-stage volatility decay** in the second half of sequences — orthogonal and partially complementary (see Agent #55). Future humanizers must address both global variance and positional decay.

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| arXiv preprint | https://arxiv.org/abs/2509.18880 | v3 HTML: https://arxiv.org/html/2509.18880v3 |
| TMLR publication | https://mlanthology.org/tmlr/2026/basani2026tmlr-diversity/ | Accepted TMLR 2026 |
| TMLR OpenReview | https://openreview.net/forum?id=WscAU9It1l | Submission #6606; reviews behind bot check |
| ICML DIG-BUG 2025 | https://openreview.net/forum?id=QuDDXJ47nq | Workshop version; short paper |
| ICLR 2026 (withdrawn) | https://openreview.net/forum?id=DNgsOhGZBI | Same title; withdrawn submission |
| IBM GitHub | https://github.com/IBM/diveye | CC BY-NC-SA 4.0; ~17 stars Aug 2026 |
| Demo site | https://diveye.vercel.app/ | Static examples; not live inference |
| HF Space | https://huggingface.co/spaces/pinyuchen/Diveye_AI_text_detector | Falcon-7B + BiScope + XGBoost `model.json` |
| HF collection | https://huggingface.co/collections/TrustSafeAI/diveye-diversity-driven-ai-text-detector | TrustSafeAI mirror |
| IBM Research | https://research.ibm.com/publications/diveye-at-pan-2025-diversity-boosts-ai-generated-text-detection | PAN 2025 abstract |
| PAN 2025 notebook (CEUR) | https://ceur-ws.org/Vol-4038/paper_282.pdf | pp. 3597–3608, Vol-4038 |
| PAN 2025 task page | https://pan.webis.de/clef25/pan25-web/generated-content-analysis.html | Voight-Kampff leaderboard |
| Moonlight review | https://www.themoonlight.io/en/review/diversity-boosts-ai-generated-text-detection | Third-party summary |
| unslop surprisal | `unslop/scripts/surprisal.py` | Bit-matched to IBM on GPT-2 |
| unslop bench | `benchmarks/results/diveye_comparison.json` | max rel error < 3×10⁻⁶ |
| Agent #34 (implementation) | `docs/research/2026-08-detector-research/AGENT-34-IBM-DIVEYE-IMPLEMENTATION.md` | Code/HF/PAN audit |
| Agent #55 (TSD stack) | `docs/research/2026-08-detector-research/AGENT-55-SURPRISAL-DYNAMICS-BEYOND-DIVEYE.md` | Post-DivEye dynamics |

---

## 3. Mechanism — how DivEye works

### 3.1 Core hypothesis

Human writing exhibits **richer variability in lexical and structural unpredictability** than LLM output. LLMs trained with likelihood maximization (and low-temperature decoding) produce text with **narrower intra-document surprisal distributions** — the "smooth machine" fingerprint that survives synonym paraphrase because paraphrasers change word choice without restoring rhythmic variance.

This reframes the burstiness insight (GPTZero, GLTR, Holtzman et al. nucleus sampling) from sentence-level heuristics to **token-level information-theoretic statistics** computed by an observer LM.

### 3.2 Surprisal computation

For text tokens \(x_1, \ldots, x_n\) and observer LM \(P\):

\[
S(x_t) = -\log P(x_t \mid x_1, \ldots, x_{t-1})
\]

Teacher-forcing: one forward pass; at position \(t\) read log-prob of the token that actually appears at \(t+1\). IBM code and unslop truncate at **1024 tokens**. Default observer: **GPT-2** (124M); HF Space uses **Falcon-7B** + Gemma-2B for BiScope.

### 3.3 Feature vector (Equation 6)

Paper defines **9 features** in three blocks:

\[
\mathcal{D} = \{\underbrace{\mu_s, \sigma_s^2, \gamma_1, \gamma_2}_{\text{Distribution}} \oplus \underbrace{\Delta\mu, \Delta\sigma^2}_{\text{1st-Order}} \oplus \underbrace{\sigma^2_{\Delta^2}, H_{\Delta^2}, \rho_{\Delta^2}}_{\text{2nd-Order}}\}
\]

**First-order difference:**

\[
\Delta S_t = S(x_t) - S(x_{t-1}), \quad \Delta\mu = \frac{1}{n-1}\sum_{t=2}^{n}\Delta S_t, \quad \Delta\sigma^2 = \frac{1}{n-2}\sum_{t=2}^{n}(\Delta S_t - \mu_\Delta)^2
\]

**Second-order difference:**

\[
\Delta^2 S_t = \Delta S_t - \Delta S_{t-1}
\]

From the \(\Delta^2 S_t\) sequence: variance \(\sigma^2_{\Delta^2}\), **20-bin entropy** \(H_{\Delta^2}\), lag-1 **autocorrelation** \(\rho(\Delta^2 S_t)\).

**IBM shipped code / unslop:** **10 features** — adds \(\sigma_s\) alongside \(\sigma_s^2\); first-order block uses **stdev** not variance. unslop `to_diveye_vector()` matches IBM code order: `[-mean_log_prob, stdev, variance, skewness, kurtosis, delta_mean, delta_stdev, delta2_var, delta2_entropy, delta2_autocorr]`.

### 3.4 Classifier and dual use modes

1. **Standalone:** Train XGBoost on \(\mathcal{D}\) alone (max_depth=12, n_estimators=200 per IBM repo).
2. **Booster:** Concatenate \(\mathcal{D}\) with another detector's score; meta-XGBoost. Paper Table 4: **+18.7%** AUROC boost for DivEye+RADAR on MAGE Testbed 4 (0.62 → 0.90).

### 3.5 Feature importance (paper §4.7)

XGBoost SHAP-style analysis on MAGE Testbed 4:

| Block | Contribution |
|-------|-------------|
| Second-order (\(\sigma^2_{\Delta^2}, H_{\Delta^2}, \rho_{\Delta^2}\)) | **39.4%** |
| Distributional (\(\mu, \sigma^2, \gamma_1, \gamma_2\)) | **34.2%** |
| First-order (\(\Delta\mu, \Delta\sigma^2\)) | **23.7%** |

Leave-one-out ablation: removing \(H_{\Delta^2}\) drops AUROC by **0.0263** (p=0.001) — largest single-feature loss. **Second-order entropy of surprisal acceleration** is the strongest individual tell.

### 3.6 Relation to other zero-shot families

| Method | Signal | DivEye contrast |
|--------|--------|-----------------|
| **DetectGPT** (Mitchell et al., ICML 2023) | Negative curvature under perturbation | Requires multiple forward passes; paraphrase-sensitive |
| **Fast-DetectGPT** (Bao et al., ICLR 2024) | Conditional probability curvature, single pass | MAGE Testbed 2 AUROC **0.59** vs DivEye **0.97**; high machine-acc/low human-acc imbalance on some testbeds |
| **Binoculars** (Hans et al., ICML 2024) | Cross-perplexity ratio of two LMs | RAID AUROC **0.844** vs DivEye **0.984**; RAID paraphrase attack: Binoculars **N/A**, DivEye **74.4%** TPR@FPR=5% |
| **BiScope** (Guo et al., NeurIPS 2024) | Memorization of preceding tokens | Closest peer; DivEye+BiScope is production ensemble |
| **TSD** (Sun et al., Jan 2026) | Late-second-half derivative dispersion + local volatility | Targets **where** variance collapses, not global σ; TSD paper reports DivEye baseline **74.40%** AUROC on EvoBench vs TSD **83.36%** |

---

## 4. Benchmark results (verified numbers)

### 4.1 MAGE (Li et al., 2024) — Table 1

Six testbeds; metrics: HumanAcc, MachineAcc, AvgAcc, AUROC. Selected rows (GPT-2 observer unless noted):

**In-distribution**

| Testbed | Method | AvgAcc | AUROC |
|---------|--------|--------|-------|
| Arbitrary-domains & model-specific (GPT-J) | FastDetectGPT | 56.4% | 0.59 |
| | Binoculars | 62.67% | 0.69 |
| | BiScope | 87.24% | 0.93 |
| | **DivEye** | **89.60%** | **0.97** |
| Fixed-domain (WP) & arbitrary-models | Binoculars | 71.44% | 0.77 |
| | BiScope | 93.53% | 0.94 |
| | **DivEye** | **94.55%** | **0.99** |
| Arbitrary-domains & arbitrary-models | FastDetectGPT | 67.69% | 0.70 |
| | BiScope | 75.12% | 0.86 |
| | **DivEye** | **78.15%** | **0.88** |

**Out-of-distribution**

| Testbed | Method | AvgAcc | AUROC |
|---------|--------|--------|-------|
| Unseen models (BLOOM-7B) | FastDetectGPT | 54.19% | 0.54 |
| | Binoculars | 65.50% | 0.71 |
| | **DivEye** | **75.91%** | **0.86** |
| Unseen domains (WP) | Binoculars | 73.37% | 0.80 |
| | **DivEye** | **89.59%** | **0.97** |
| Unseen domains & models | BiScope | 84.24% | 0.92 |
| | **DivEye** | **76.49%** | **0.87** |

**Paper claim:** average AUROC **0.92** across all MAGE testbeds vs zero-shot baselines. The **33.2%** headline is the maximum relative improvement over zero-shot methods (likely vs GLTR-class baselines; RAID Table 2 shows GLTR at **−26.27 pp** AUROC delta from leader).

### 4.2 RAID (Dugan et al., 2024) — Table 2

Aggregated over 8 domains, 12 models, 4 decoding strategies:

| Framework | Type | TPR@FPR=5% | AUROC | δ from leader |
|-----------|------|------------|-------|---------------|
| e5-small-lora | Fine-tuned | 93.9% | **0.986** | — |
| **DivEye** | Zero-shot features + XGBoost | 93.63% | **0.984** | −0.20% |
| Desklib AI | Fine-tuned | 94.9% | 0.973 | −1.32% |
| Binoculars | Zero-shot | 79.0% | 0.844 | −14.40% |
| GLTR | Zero-shot | 59.7% | 0.727 | −26.27% |

Domain-level AUROC (Figure 4): **0.98** average across domains; **0.93** across generator families.

### 4.3 Adversarial robustness — Table 3

| Setting | Method | AvgAcc | AUROC |
|---------|--------|--------|-------|
| MAGE Testbed 8 (GPT-3.5 paraphrase) | Longformer | 69.34% | 0.76 |
| | BiScope | 69.30% | 0.81 |
| | **DivEye** | **76.49%** | **0.87** |
| RAID adversarial mix | Desklib | 91.2% | 0.948 |
| | **DivEye** | 80.52% | **0.951** |
| | Binoculars | 69.32% | — |

RAID paraphrase attack specifically: DivEye **74.4%** TPR@FPR=5% vs Binoculars **N/A** (method fails).

### 4.4 Booster mode — Table 4 (MAGE Testbed 4)

| Combo | AUROC | Boost |
|-------|-------|-------|
| DivEye alone | 0.88 | — |
| DivEye + RADAR | 0.90 | **18.7%** |
| DivEye + FastDetectGPT | 0.91 | 13.97% |
| DivEye + Binoculars | 0.87 | 11.15% |
| DivEye + BiScope | 0.93 | 9.38% |

### 4.5 PAN@CLEF 2025 (validation set)

From PAN notebook Table 1 ([CEUR Vol-4038 paper_282](https://ceur-ws.org/Vol-4038/paper_282.pdf)):

| Method | AUROC |
|--------|-------|
| DivEye + BiScope (submission) | **0.997** |
| TF-IDF Linear SVM (official baseline) | **0.996** |
| Binoculars (Llama-3.1) | 0.918 |
| PPMd compression cosine | 0.786 |

DivEye wins on paper margins but **does not dominate** — lexical TF-IDF is within **0.1 pp**. Subtask 1 leaderboard top team (mdok) reached **0.959** macro-F1 on test; DivEye team did not top the public leaderboard (task had 20+ entrants).

### 4.6 Efficiency

- **0.01 s/sample** (GPT-2 backbone + stats)
- **2971× speedup** vs RAiDAR (paper Figure 6b)
- Observer LM scaling: AUROC **0.88** (GPT-2) → **0.91** (Llama-3.1-8B) → **0.90** (Falcon-7B)

### 4.7 Non-native English (COREFL)

DivEye **82.1%** avg accuracy vs Binoculars **68.34%** vs FastDetectGPT **71.71%** on ESL-proficiency brackets — surprisal-diversity features **help** on ESL text relative to perplexity-ratio methods, though production ESL false-positive risk remains (Liang et al. 2023: >50% TOEFL essays flagged by GPTZero-class tools).

---

## 5. Community & academic debate

### 5.1 Supporters / positive signals

| Source | Position | Quote / evidence |
|--------|----------|------------------|
| **TMLR 2026 acceptance** | Peer-reviewed validation | OpenReview `WscAU9It1l`, ML Anthology entry live |
| **IBM Research / PAN 2025** | Applied deployment | "Outperforms the four official baselines" — IBM publication page |
| **Moonlight review** | Uncritical synthesis | Calls second-order dynamics "significant contribution"; reproduces all equations |
| **Paper authors** | Interpretability claim | "Rhythmic unpredictability as a powerful and underexplored signal" |
| **Ablation statistics** | Internal evidence | All 9 features significant at p<0.05 in leave-one-out |

Authors respond to TMLR reviewer requests in Appendix F: degenerate generators, prompt obfuscation, same-model scoring — all with additional experiments showing maintained performance.

### 5.2 Critics / limitations / indirect skepticism

| Source | Concern | Relevance to DivEye |
|--------|---------|---------------------|
| **Appendix J (authors)** | Short-text weakness | "Diversity metrics are less effective on very short texts" — <~100 tokens, stats unstable |
| **Appendix J (authors)** | Observer LM dependence | Features vary across architectures/tokenizers; GPT-2 recommended minimum |
| **Sadasivan et al. (2023)** | Detection impossibility as LLMs → human distribution | Paper cites but argues current LLMs still prioritize coherence over diversity |
| **Chakraborty et al. (ICML 2024)** | Sample-complexity bounds | Cited in unslop as counter — detection may remain possible with robust features |
| **Pangram blog** ([link](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)) | Perplexity/burstiness insufficient alone for production | DivEye extends burstiness to token surprisal dynamics but still statistical — "big difference between computing a statistic and building a production-grade system" |
| **HumanizeMyAI research** ([link](https://humanizemy.ai/research/surprisal-arc-nlp)) | Surprisal *arc shape* is not predictive (AUC 0.52–0.55) | Contradicts narrative that any surprisal trajectory works — **level + variance** matter, not aesthetic arcs |
| **Agent #34 audit** | PAN "beats all baselines" vs TF-IDF 0.996 | Margin **0.001 AUROC** — claim is technically true but not a knockout |
| **CC BY-NC-SA 4.0** | IBM repo license | Non-commercial — commercial integrators cannot ship IBM weights/code without separate terms |
| **No social buzz** | HN/Reddit/Twitter | Zero dedicated threads found Aug 2026 — neither viral hype nor pile-on critique |

### 5.3 Overhyped vs genuinely novel

**Genuinely novel:** Formalizing burstiness as multi-order surprisal time-series features; showing second-order entropy/autocorr dominate; demonstrating paraphrase robustness relative to curvature/perplexity methods; efficient GPT-2 observer beating Binoculars by 14+ AUROC points on RAID.

**Overhyped / caveated:**

- "Zero-shot" requires **labeled training data for XGBoost** on each deployment domain — not plug-and-play like Binoculars threshold.
- Headline **33.2%** is a **best-case delta** vs weakest zero-shot baselines, not vs fine-tuned SOTA.
- **0.984 RAID AUROC** is essentially tied with e5-small-lora (**0.986**).
- HF demo site (`diveye.vercel.app`) uses **hardcoded confidence** (95.7%) — marketing, not inference.
- ICLR 2026 submission **withdrawn** (`DNgsOhGZBI`) while TMLR accepted — normal dual-submission noise, not a red flag by itself.

---

## 6. Humanization angle — raising surprisal variance to evade DivEye-class detectors

DivEye detects **low diversity**. The offensive playbook inverts its feature vector toward human reference distributions. This section is for **defensive humanization** (ESL false positives, voice restoration) per unslop Boundaries — not academic misconduct.

### 6.1 Feature-targeted tactics

| DivEye feature | AI typical | Humanization lever |
|----------------|-----------|-------------------|
| \(\sigma_s\), \(\sigma_s^2\) | Low — uniform token predictability | Mix rare/concrete nouns with function-word glue; avoid synonym-only paraphrase |
| \(\gamma_1\) (skewness) | Lower — symmetric surprisal | Insert occasional high-surprisal content words (domain terms, proper nouns) |
| \(\Delta\sigma\) (first-order stdev) | Low — smooth transitions | Abrupt sentence boundaries; topic shifts; fragment after long clause |
| \(\sigma^2_{\Delta^2}\) | Low — stable acceleration | Vary **how quickly** unpredictability changes (don't smooth uniformly) |
| \(H_{\Delta^2}\) | Low — predictable transition bins | **Highest ablation impact** — inject irregular rhythm in edit pacing |
| \(\rho_{\Delta^2}\) | Lower — uncorrelated bursts | Cluster surprises: run of short punchy sentences after dense paragraph |

### 6.2 Structural proxies (cheap, no LM)

unslop `stylometry.py` already ships **`sentence_length_cv`** and **`word_length_stdev`** as DivEye proxies. Anti-detector SKILL.md targets sentence-length **σ ≥ 6** (human ~8.2 vs GPT-4o ~4.1). These correlate with but do not equal token surprisal variance.

### 6.3 What paraphrase does and doesn't fix

HumanizeMyAI (2025–2026 corpus study): paraphrase drops **mean perplexity** detection AUC from 0.80 → 0.58 (toward chance) but **burstiness** only 0.80 → 0.78. DivEye's design explicitly targets the **variance that survives paraphrase**. Effective evasion needs **rhythm injection**, not QuillBot-style rewording.

### 6.4 Advanced / 2026 dynamics

- **TSD evasion:** Don't let surprisal volatility **collapse in the second half**. Keep late-document sentence-length and lexical variance high — add a short punchy closing paragraph, not a tidy summary.
- **SurpMark evasion (future):** After high-surprisal tokens, avoid immediate return to predictable states — human text "recovers" more slowly (Agent #55).
- **Cross-model paraphrase:** Strongest lever per unslop SKILL.md — different model families rewrite surprisal fingerprints (TempParaphraser 82.5% detector reduction claim).
- **Nucleus sampling insight** (Holtzman et al., ICLR 2020): AI truncates low-probability tail tokens → low variance. Humanization should **restore tail choices** — concrete specifics, idioms, minor imperfections.

### 6.5 What not to do

- Uniform smoothing ("make every sentence medium length") — raises all DivEye flags simultaneously.
- Random typo injection — RAID tests homoglyph/misspelling attacks; DivEye TPR@FPR=5% stays **67–90%** on character attacks.
- Fabricate facts for "surprise" — unslop forbids; use structural variance instead.

---

## 7. unslop integration plan

Current state (from `surprisal.py`, `detector.py`, `humanize.py`, `docs/RESEARCH_AND_TECH.md`):

| Component | Today | Gap |
|-----------|-------|-----|
| `surprisal.py` | Full 10-feature IBM-aligned vector; `distilgpt2` default; `--surprisal-variance` CLI | Author typo ("Ganapathi" → Basani & Chen); default LM ≠ paper GPT-2 |
| `stylometry.py` | `sentence_length_cv`, `word_length_stdev` proxies | No Δ² features |
| `detector.py` | TMR RoBERTa loop; optional `surprisal_stdev` logging | No DivEye classifier; surprisal not a stop condition |
| `humanize.py` anti-detector | Sentence σ ≥ 6; burstiness prompt | No explicit Δ² entropy/autocorr targets |
| `SKILL.md` | Names DivEye; anti-detector procedure | No per-feature guidance |

### 7.1 `surprisal.py`

- **P0:** Fix docstring attribution to **Basani & Chen**, not Ganapathi.
- **P1:** Add `UNSLOP_SURPRISAL_MODEL` env defaulting to `gpt2` for paper parity; keep `distilgpt2` as fast fallback.
- **P1:** Export `to_paper_vector()` (9 dims, Eq. 6) alongside `to_diveye_vector()` (10 dims, IBM code).
- **P2:** Optional half-sequence split API for TSD features (coordinate with Agent #55).

### 7.2 `detector.py`

- **P1:** Wire `compute_surprisal_variance` into feedback loop as **secondary metric** — log full vector per iteration, not just stdev.
- **P2:** Optional lightweight DivEye distance score: L2 to stored human reference centroid (no XGBoost dep) for `--detector-feedback` reporting.
- **P2:** Document that TMR detector ≠ DivEye — loop optimizes RoBERTa, not surprisal variance.

### 7.3 `humanize.py` + anti-detector mode

- **P0:** Extend anti-detector LLM prompt with explicit DivEye targets: "raise surprisal stdev, delta_stdev, delta2_entropy; avoid uniform second-order transitions."
- **P1:** After deterministic passes, if `--surprisal-variance` shows \(\sigma_s\) below corpus threshold, trigger one extra structural pass (`structural.py` sentence splitting/merging).
- **P1:** Map second-order targets to concrete edits: alternate 3-word fragments with 25-word sentences; place domain-specific term bursts mid-paragraph.

### 7.4 Benchmarks & CI

- **P0:** Keep `benchmarks/diveye_comparison/` in weekly workflow — already confirms bit-match.
- **P1:** Add `benchmarks/surprisal_humanization/` — measure Δ features before/after each intensity mode on fixture corpus.
- **P2:** Track DivEye+XGBoost AUROC on RAID subset alongside TMR weekly bench.

---

## 8. Recommended actions

### P0 (do now)

1. Fix **author citation** in `surprisal.py` (Basani & Chen, arXiv:2509.18880).
2. Add **DivEye-aware anti-detector prompt lines** in `humanize.py` targeting σ, Δσ, \(H_{\Delta^2}\).
3. Document in `RESEARCH_AND_TECH.md` that unslop measures DivEye features but **detector loop uses TMR**, not surprisal classification.

### P1 (next sprint)

4. Log **full surprisal vector** in `detector.feedback_loop()` iterations JSON.
5. Add **`to_paper_vector()`** 9-dim export; env var for observer LM selection.
6. Run **before/after surprisal bench** across intensity modes; publish in `benchmarks/results/`.

### P2 (research track)

7. Implement **TSD half-sequence features** (Agent #55 dependency).
8. Evaluate optional **human-reference centroid distance** as anti-detector stop heuristic.
9. Monitor **SurpMark** (ICML 2026) for transition-matrix evasion targets.

---

## 9. Open questions

1. **33.2% provenance:** Which baseline and metric exactly? Paper states it in abstract but does not anchor to a single table row — likely max AUROC gap vs GLTR/FastDetectGPT-class on MAGE/RAID.

2. **TMLR reviewer critiques:** OpenReview behind bot check — full reviewer text not retrieved. Appendix F suggests reviewers asked about degenerate generators and prompt obfuscation; responses included but independent assessment unavailable.

3. **Commercial deployment:** Will IBM release pretrained XGBoost weights under a commercial license? HF Space `model.json` exists but NC-SA blocks direct shipping.

4. **distilgpt2 calibration:** unslop field readings (AI 0.6–0.9 stdev, literary human >1.5) — are these validated on a labeled corpus or heuristic? Needs benchmark.

5. **Same observer as generator:** Paper claims robustness when observer = generator LM. How quickly does this break for newest frontier models (GPT-4o, Claude 3.5) with matched tokenizer?

6. **Ensemble future:** DivEye+BiScope+TMR+TSD — do features remain orthogonal, or will a single meta-classifier subsume all?

7. **ESL edge case:** DivEye beats Binoculars on COREFL but Pangram warns ESL text looks "AI-low-perplexity." What is DivEye false-positive rate on TOEFL essays specifically?

8. **Humanization arms race:** If unslop optimizes \(\ H_{\Delta^2}\), will detectors add third-order features (paper Appendix tests Δ³/Δ⁴ — diminishing returns found, but adversarial fine-tuning may differ)?

---

## Cross-references

- **Agent #34** — IBM repo, HF Space, PAN notebook, numerical alignment audit.
- **Agent #55** — TSD, SurpMark, late-stage volatility; post-DivEye humanization stack.
- **Agent #34 IBM-DIVEYE-IMPLEMENTATION.md** — do not duplicate code-level findings here.

---

*Research conducted 2026-08-19 via arXiv HTML v3, OpenReview metadata, PAN CEUR notebook, IBM/GitHub/HF pages, Pangram/HumanizeMyAI/Moonlight third-party sources, and unslop codebase audit. OpenReview full review text blocked by browser verification.*
