# Agent #9 — Tulchinskii PHD / Intrinsic Dimension Detector

**Topic:** Persistent Homology Dimension (PHD) for AI-text detection  
**Paper:** Tulchinskii et al., *Intrinsic Dimension Estimation for Robust Detection of AI-Generated Texts*, NeurIPS 2023  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Tulchinskii et al. propose a **zero-shot, geometry-based detector**: extract token-level contextual embeddings from a frozen LM (RoBERTa-base / XLM-R), treat them as a point cloud, estimate **intrinsic dimension (ID)** via **Persistent Homology Dimension (PHD)**, and threshold. Human fluent text clusters around **ID ≈ 9.5** (alphabetic languages); modern LLM output sits **≈1.5 lower (~7.9)**. The gap is stable across genre, domain, generator, and sampling method in their experiments.

Three claims matter for unslop:

1. **DIPPER resistance** — PHD is the rare 2023 detector that *improves* after DIPPER paraphrase on GPT-3.5 generations (40.0% → 41.2% TPR at 1% FPR), while DetectGPT collapses (70.3% → 4.6%).
2. **ESL bias reduction (partial)** — On Liang's TOEFL protocol, PHD false-positive rate on non-native essays is **26%** vs OpenAI **58%** and GPTZero **52%**. Better, not fair. After GPT-4 polish of ESL essays, PHD FPR drops to **7.7%**.
3. **Structural signal, not lexical** — ID measures **global embedding-trajectory complexity**, overlapping with but distinct from perplexity, burstiness, and surprisal variance (DivEye). Surface synonym swaps are weak against PHD; **embedding-path diversity** is the evasion/defense axis.

**unslop verdict:** PHD is the canonical "third signal" (geometry) alongside curvature (DetectGPT) and cross-perplexity (Binoculars). Deterministic unslop passes *probably* nudge ID upward via structural variance (`structural.py`, stylometry CV proxies), but **no one has measured PHD on unslop output**. PHD is not wired into `detector.py`. Highest-value next step: optional PHD scorer in `benchmarks/detector_bench.py` to test whether structural + surprisal passes move estimated ID toward the human band.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv)** | https://arxiv.org/abs/2306.04723 |
| **Paper (HTML)** | https://arxiv.org/html/2306.04723v1 |
| **NeurIPS proceedings PDF** | https://proceedings.neurips.cc/paper_files/paper/2023/file/7baa48bc166aa2013d78cbdc15010530-Paper-Conference.pdf |
| **OpenReview** | https://openreview.net/forum?id=8uOZ0kNji6 |
| **ACM DL** | https://dl.acm.org/doi/10.5555/3666122.3667828 |
| **Official code (GPTID)** | https://github.com/ArGintum/GPTID |
| **Example notebook** | https://github.com/ArGintum/GPTID/blob/main/example.ipynb |
| **HAL mirror** | https://hal.science/hal-04734180v1/file/IntrinsicDimNeurips2023.pdf |

### Related papers (same research line)

| Paper | URL | Relation |
|-------|-----|----------|
| **DIPPER paraphrase attack** (Krishna et al., NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Primary adversarial eval; PHD resists where others fail |
| **Liang ESL bias** (Patterns 2023) | https://arxiv.org/abs/2304.02819 | Protocol reused for PHD fairness experiments |
| **RoFT boundary detection** (Kushnareva et al., 2024) | https://arxiv.org/abs/2311.08349 | Same author group; RoFT on generation boundaries |
| **TDA for speech** (Tulchinskii et al., INTERSPEECH 2023) | https://www.isca-speech.org/archive/interspeech_2023/tulchinskii23_interspeech.html | PHD estimator lineage |
| **DAMAGE humanizer audit** (Masrour et al., COLING 2025) | https://arxiv.org/abs/2501.03437 | Cites Tulchinskii group (RoFT); **does not evaluate PHD** |
| **DivEye surprisal variance** (TMLR 2026) | https://arxiv.org/abs/2509.18880 | Orthogonal zero-shot signal; unslop already ships surprisal |
| **MGTBench** | https://arxiv.org/abs/2303.14822 | Adversarial harness PHD predates |
| **RAID benchmark** | https://arxiv.org/abs/2405.07940 · https://github.com/liamdugan/raid | PHD **not** a default RAID baseline |
| **M4 benchmark** | https://arxiv.org/abs/2305.14902 | Cross-domain eval landscape; PHD not central |

**Citation fix for unslop docs:** README and SKILL.md cite **arXiv 2306.04723** for Liang's ESL result. That arXiv ID is **Tulchinskii PHD**, not Liang. Liang ESL is **arXiv 2304.02819** ([Patterns](https://doi.org/10.1016/j.patter.2023.100779)).

---

## PHD mechanism (technical)

### Pipeline (4 steps)

```
Text (≈200–300 tokens)
  → Frozen Transformer encoder (RoBERTa-base EN; XLM-R multilingual)
  → Last-layer token embeddings (drop [CLS]/[SEP] equivalents)
  → Point cloud X ⊂ R^d  (d = hidden size, 768 for RoBERTa-base)
  → PHD estimator → scalar ID score
  → Threshold classifier (human if ID > τ)
```

### Why intrinsic dimension?

Informally: ID = **degrees of freedom** of a point moving on the manifold underlying the embeddings. Human writing explores more independent directions in embedding space; LLM output traces a **lower-dimensional, more constrained** submanifold. The paper frames this as invariant across genre/style for fluent human text in a given language.

### PHD estimator (Persistent Homology Dimension)

Based on **topological data analysis (TDA)** and the **growth-rate theorem** (Barannikov et al.; Adams et al. 2020):

1. For point cloud `X`, build **minimal spanning tree (MST)** on subsamples `S_i ⊂ X` of varying sizes `n_i`.
2. Compute persistence score `E^0_α(S_i)` = Σ |e|^α over MST edges (0-dimensional persistent homology; α=1 in practice).
3. Regress `log E^0_α(S_i)` vs `log n_i`; slope κ → estimated dimension `d = 1/(1−κ)`.
4. **Stabilization:** multiple random subsample rounds + averaging (Birdal et al. baseline was unstable on small/noisy text clouds — variance up to 35%).

**Why PHD over MLE/TwoNN/MADA:** Paper benchmarks 12 ID estimators (scikit-dimension). PHD alone stays stable under **noise and small sample size** — both common for ~300-token texts. MLE often beats PHD on raw AUC but **craters under paraphrase** (Table 5 appendix).

### Embedding geometry intuition

| Text type | Embedding trajectory | Approx. PHD |
|-----------|---------------------|-------------|
| Fluent human prose | Wide exploration; syntactic/semantic shifts create spread | ~9.5 ± 1.2 |
| GPT-3.5 / ChatGPT fluent output | Collinear, predictable path in representation space | ~7.9 ± 0.8 |
| Random token soup | Maximum irregularity | Highest ID |
| Single-token repetition | Minimal spread | Lowest ID |
| High-temperature / bad generations | **Can exceed human ID** | Detector inverts — needs recalibration |
| Proper-noun / address heavy human text | Rare-token clusters; **false AI flags** | Low ID misclassified |

Each **token embedding is one point**. The "manifold" is the shape of the trajectory through context space as the text unfolds — not the CLS sentence vector alone.

---

## Key experimental results

### Absolute ID values (English, RoBERTa-base, ~300 tokens)

| Source | Mean PHD |
|--------|----------|
| Human (Wiki40b, multi-genre) | 9.491 ± 1.010 |
| GPT-2 | lower (see Fig. 3 boxplots) |
| OPT | lower |
| GPT-3.5 (davinci-003) | ~1.5 below human band |

Genre table (Table 1): fiction, news, Wikipedia — human ID stable (~9–10); AI consistently lower.

### Detection accuracy at 1% FPR (Wiki prompts, Table 2)

| Generator | DetectGPT | GPTZero | RankGen | **PHD** | MLE |
|-----------|-----------|---------|---------|---------|-----|
| GPT-2 | 70.3* | 21.6 | 13.9 | **25.2** | 23.8 |
| GPT-2 + DIPPER | 4.6 | 14.8 | 1.2 | **28.5** | 27.6 |
| OPT | 14.3 | 11.3 | 8.7 | **28.0** | 26.7 |
| OPT + DIPPER | 0.3 | 10.0 | 1.0 | **13.5** | 30.2 |
| GPT-3.5 | 0.0 | 30.0 | 7.1 | **40.0** | 46.7 |
| GPT-3.5 + DIPPER | 0.0 | 15.6 | 1.8 | **7.3** | 41.2 |

*DetectGPT uses GPT-2 as scoring model.

**DIPPER settings:** Lex=60, Order=60 (Krishna et al. protocol).

PHD gains on GPT-2/DIPPER and GPT-3.5/DIPPER; OPT/DIPPER is the weak cell (13.5%).

### Cross-domain robustness (Table 3, GPT-3.5 generations)

RoBERTa-CLS supervised classifier: **0.990 in-domain → 0.535 cross-domain** (Wiki→Reddit).  
PHD: **~0.76–0.85 stable** across Wikipedia / Reddit / StackExchange without retraining.

### Cross-model robustness (Table 3)

PHD accuracy ~**0.76–0.84** when train/eval generators differ (GPT-2, OPT, GPT-3.5). RoBERTa-CLS does better on average in this table but with larger generalization gap.

### Multilingual (Table 4, ChatGPT, XLM-R, ROC-AUC)

Average PHD **0.78**; best ES/IT (~0.83); worst zh/jp (~0.71–0.74).

---

## ESL bias reduction claim

### Protocol

Reuses **Liang et al. 2023** setup ([arXiv:2304.02819](https://arxiv.org/abs/2304.02819)):

- TOEFL essays by non-native English writers
- Same essays after GPT-4 "improve the text" polishing
- Native US 8th-grade essays (near-zero FPR for all detectors)
- Thresholds calibrated on Wikipedia intros (real vs GPT-3.5-turbo), EER 26.8% (PHD) / 22.5% (MLE)

### Results (Figure 6, false positive rate — lower is better)

| Detector | FPR on non-native TOEFL essays |
|----------|-------------------------------|
| OpenAI classifier | ~58% |
| GPTZero | ~52% |
| **PHD** | **~26%** |
| MLE | Better than baselines, worse than PHD |

After GPT-4 polish of TOEFL essays:

| Detector | FPR |
|----------|-----|
| GPTZero | ~19% |
| **PHD** | **~7.7%** |

Native speakers: FPR **<1%** for all (blue bars "invisible" in figure).

### Mechanism (why partial improvement)

Perplexity-based detectors (GPTZero, OpenAI) conflate **low lexical diversity** with machine authorship — the core Liang finding. PHD measures **embedding geometry**, which correlates less with surface vocabulary sophistication. ESL writers still produce human syntactic/semantic paths; they just use a narrower word choice band.

### Critique of the fairness claim

- **26% FPR is still catastrophic** in a classroom: 1-in-4 innocent ESL submissions flagged.
- PHD **does not eliminate** the Liang paradox: GPT-4 polish helps both real ESL essays (fewer false positives) **and** helps AI evade other detectors — same transformation axis.
- Failure mode: human texts with many **proper nouns, addresses, geo names** sit at **low ID** and get misclassified as AI (paper acknowledges).
- Short texts degrade PHD reliability.

**Bottom line for unslop anti-detector mode:** PHD is fair*er*, not fair. Defensive humanization for ESL false positives should not assume geometry detectors are safe — but raising structural/embedding diversity is the right axis, not synonym swapping alone.

---

## DIPPER resistance

### What the paper shows

DIPPER destroys log-probability curvature signals (DetectGPT, GPTZero). PHD **does not depend on generator logits**. Paraphrase removes generator-specific artifacts but **does not fully humanize embedding geometry** — AI paraphrases remain in the low-ID band. Mean PHD shifts slightly upward under DIPPER (Appendix C.2) but **below human threshold**.

Appendix Table 5: increasing DIPPER lexical diversity (Lex 0→100) bumps mean PHD marginally; **Order (reordering) 0→60 has almost no effect**. Surface paraphrase ≠ manifold expansion.

### Why this matters for evasion

To beat PHD you need to **raise ID by ~1.5 points**, not just reword. That implies:

- Syntactic restructuring (sentence splits/merges, clause depth)
- Discourse reordering (weak effect per Tulchinskii's DIPPER Order sweep)
- Injecting genuine unpredictability in embedding trajectory (topic shifts, register breaks, rare-but-coherent word choices)
- **Not** sufficient: synonym swap, stock-vocab scrubbing, light contraction pass

### 2026 context

DivEye ([2509.18880](https://arxiv.org/abs/2509.18880)) shows **surprisal variance** also survives paraphrase. PHD and DivEye are **complementary geometry/statistics views** — both punish "too smooth" trajectories. An evasion pipeline must move **both** ID and surprisal dynamics.

---

## Critics, limitations, and open questions

### Authors' stated limitations (Section 6)

1. **Stochastic estimator** — ID variance across rerolls; accuracy vs speed tradeoff.
2. **Fluent-generator assumption** — High-temperature or degenerate outputs can have **ID > human**; detector must recalibrate.
3. **Low-resource languages** — Only ~10 high/medium-resource langs tested.

### External / ecosystem critiques

| Issue | Detail |
|-------|--------|
| **Not in RAID/M4 standard baselines** | RAID leaderboard ([raid-bench.xyz](https://raid-bench.xyz)) ships Binoculars, Desklib, DivEye, etc.; PHD absent. Hard to compare 2026 numbers head-to-head. |
| **Not in DAMAGE audit** | DAMAGE ([2501.03437](https://arxiv.org/abs/2501.03437)) tests GPTZero, Binoculars, fine-tuned Pangram model against 19 humanizers — **no PHD score reported**. |
| **Repo maturity** | GPTID README says "under construction" (Sep 2023); ~36 GitHub stars; typo in README arXiv link (2306.04273 vs 2306.04723). |
| **Compute cost** | RoBERTa forward pass + multiple MST subsamples per document — heavier than pure perplexity, lighter than fine-tuned ensemble. |
| **Gap may shrink** | Chakraborty et al. detectability ranking: newer models (GPT-4) less separable by classic stats. No public replication that GPT-4o/o3 output still sits 1.5 ID below human. |
| **Adaptive attacks untested** | No PHD-specific optimizer (contrast Nicks ICLR 2024, Adversarial Paraphrasing NeurIPS 2025). Geometry-aware evasion is an open adversary. |
| **Single-feature threshold** | No ensemble with perplexity/stylometry; likely beatable by multi-signal fusion defending. |

### Supporters / independent reception

- NeurIPS 2023 acceptance; cited across detection surveys and unslop Cat 05 synthesis.
- Liner/OpenReview summaries emphasize cross-domain stability and DIPPER robustness.
- Positioned in literature as proof that **behavioral/structural probes** (with RAIDAR, Binoculars) can replace logit access.

---

## Reproductions and code

### Official: `ArGintum/GPTID`

- **License:** MIT  
- **Core file:** `IntrinsicDim.py` — `PHD` class  
- **Deps:** NumPy, SciPy, scikit-dimension (MLE baseline), Transformers  
- **Notebook:** `example.ipynb` — `get_phd_single()`, `get_phd()` over DataFrame  
- **Hyperparams exposed:** `alpha=1.0`, `n_points=9`, subsample stepping via `MIN_SUBSAMPLE`, `INTERMEDIATE_POINTS`

Minimal reproduction sketch:

```python
# From GPTID example.ipynb pattern
from IntrinsicDim import PHD
# 1. Tokenize text → RoBERTa-base → last_hidden_state[0][1:-1]
# 2. PHD_solver = PHD(alpha=1.0, metric='euclidean', n_points=9)
# 3. dim = solver.fit_transform(embeddings, min_points=..., max_points=..., point_jump=...)
```

### Dataset released

**WikiM** — GPT-3.5 generations + matched human Wikipedia text, 10 languages (prompt = header + first sentence → continue).

### Independent reproductions

**No peer-reviewed independent replication study found** (as of Aug 2026). PHD results live primarily in the original paper + GPTID repo. Community benchmarks (RAID, MGTBench, M4) did not adopt PHD as a standard row — reproduction gap for unslop to fill.

### Suggested unslop reproduction protocol

1. Install GPTID deps; pin RoBERTa-base `FacebookAI/roberta-base`.
2. Sample 100 human + 100 GPT-4o paragraphs (~250 tokens) from existing `benchmarks/` corpus.
3. Score PHD before/after: raw AI → `humanize --intensity balanced` → `full` → `anti-detector`.
4. Log alongside TMR (`detector.py`) and DivEye (`surprisal.py` if torch present).
5. Report ΔPHD, not just detector probability.

---

## unslop integration analysis

### Can deterministic humanization raise manifold dimension?

**Plausibly yes, partially** — but **unverified empirically** in this repo.

| unslop pass | PHD relevance | Mechanism |
|-------------|---------------|-----------|
| **Stock vocab / hedging removal** | Low–medium | Changes token identities but not necessarily trajectory dimension |
| **`structural.py`** (sentence split/merge) | **High** | Sentence-length variance restores syntactic contexts → embedding path spreads |
| **`stylometry.py` proxies** (`sentence_length_cv`, `word_length_stdev`) | Medium (proxy) | Cheap correlates of "burstiness"; **not** PHD itself |
| **`soul.py` contractions** | Low | Register shift; minor embedding effect |
| **Em-dash cap** | Low | Reduces stylistic uniformity slightly |
| **LLM `anti-detector` mode** | Unknown–high | Could add reordering/unpredictability if prompted for structural diversity |
| **DivEye / surprisal pass** | Orthogonal | Targets token-level surprisal variance, not MST dimension of embeddings |

Tulchinskii's ID axis aligns with unslop's **`structural.py` thesis** (human sentence-length σ ≈ 8 vs GPT ≈ 4). That is the closest deterministic lever. Lexical-only `subtle` mode is unlikely to move PHD enough.

**DIPPER Order=60 weak effect** suggests unslop should prioritize **sentence architecture** over clause reordering for PHD evasion/defense testing.

### Stylometry proxies vs PHD

| Signal | unslop module | PHD relationship |
|--------|---------------|------------------|
| Sentence length mean/σ | `stylometry.py` | Surface correlate of syntactic variety; may co-vary with ID |
| Type-token ratio | `stylometry.py` | Liang link: low TTR → perplexity FPs; weak direct PHD evidence |
| `sentence_length_cv` | `stylometry.py` ("cheap DivEye proxy") | DivEye ≠ PHD; both punish uniformity from different math |
| Embedding MST dimension | **Not implemented** | Ground truth for Tulchinskii axis |

**Recommendation:** Add `phd_proxy` optional field to benchmark output — either full PHD via GPTID or document that CV proxies are **insufficient** for PHD claims.

### Current unslop code gaps

| Component | PHD status |
|-----------|------------|
| `unslop/scripts/detector.py` | TMR + Desklib only; **no PHD backend** |
| `fetch_detectors.py` | No PHD model fetch |
| `benchmarks/detector_bench.py` | Should add PHD column |
| `anti-detector` feedback loop | Optimizes TMR score, not ID |
| README ESL citation | **Wrong arXiv** (2306.04723 → should split Tulchinskii vs Liang 2304.02819) |

### Proposed integration (priority order)

1. **P0 — Citation fix:** Split Tulchinskii (2306.04723) and Liang (2304.02819) in README/SKILL.md.
2. **P1 — Benchmark hook:** Optional `--score-phd` in detector bench using GPTID; report mean ID human vs AI vs unslop passes.
3. **P2 — Hypothesis test:** Does `structural=True` alone increase PHD more than lexical-only? Ablation for Cat 05 synthesis update.
4. **P3 — Detector backend:** Only if PHD bench shows unslop moves ID materially; heavyweight for production CLI.
5. **P4 — Anti-detector prompt:** If bench confirms, add explicit "embedding trajectory diversity" instruction to `anti-detector` LLM pass (careful: defensive use only per skill boundaries).

### Relationship to "three-signal consensus"

unslop Cat 05 SYNTHESIS already names Tulchinskii as the geometry leg:

- **Curvature / likelihood:** DetectGPT, Fast-DetectGPT, AdaDetectGPT  
- **Cross-perplexity:** Binoculars  
- **Manifold geometry:** Tulchinskii PHD  
- **Surprisal dynamics (2025+):** DivEye, TSD, SurpMark  

Deterministic unslop covers leg 1 partially (via anti-detector LLM), leg 4 via `surprisal.py`, **leg 3 only indirectly** via structural variance. Closing leg 3 requires measurement first.

---

## Tulchinskii vs DAMAGE (disambiguation)

| | **PHD (NeurIPS 2023)** | **DAMAGE (COLING 2025)** |
|--|------------------------|--------------------------|
| **Lead** | Eduard Tulchinskii et al. | Masrour, Emi, Spero (Pangram) |
| **arXiv** | 2306.04723 | 2501.03437 |
| **Question** | Can embedding ID separate human/AI zero-shot? | Do commercial humanizers beat detectors? |
| **PHD role** | Proposed method | Not evaluated |
| **unslop use** | Theoretical third signal | Justifies live TMR feedback loop in `detector.py` |

Same research ecosystem (Kushnareva/Tulchinskii overlap on RoFT), different papers.

---

## Decision matrix for unslop maintainers

| Question | Answer |
|----------|--------|
| Should PHD replace TMR in `detector.py`? | **No** — TMR is lighter, RAID-calibrated, already shipped. |
| Should PHD be a benchmark dimension? | **Yes** — fills reproduction gap; tests structural-pass thesis. |
| Does deterministic unslop beat PHD today? | **Unknown — measure.** |
| Is PHD safe for ESL defense claims? | **No** — 26% FPR on TOEFL; better than GPTZero, still harmful. |
| Does DIPPER beat PHD? | **Mostly no** on GPT-3.5; OPT/DIPPER weaker (13.5% TPR). |
| Best unslop lever for ID? | **`structural.py` + surprisal dynamics**, not synonym scrub. |

---

## References (BibTeX-ready)

```bibtex
@inproceedings{tulchinskii2023intrinsic,
  title={Intrinsic Dimension Estimation for Robust Detection of {AI}-Generated Texts},
  author={Tulchinskii, Eduard and Kuznetsov, Kristian and Kushnareva, Laida and others},
  booktitle={NeurIPS},
  year={2023},
  url={https://arxiv.org/abs/2306.04723}
}

@article{krishna2023paraphrasing,
  title={Paraphrasing Evades Detectors of {AI}-Generated Text, but Retrieval is an Effective Defense},
  author={Krishna, Kalpesh and Song, Yixiao and Karpinska, Marzena and Wieting, John and Iyyer, Mohit},
  journal={arXiv:2303.13408},
  year={2023}
}

@article{liang2023gpt,
  title={{GPT} Detectors are Biased Against Non-Native {English} Writers},
  author={Liang, Weixin and Yuksekgonul, Mert and Mao, Yining and Wu, Eric and Zou, James},
  journal={Patterns},
  year={2023},
  url={https://arxiv.org/abs/2304.02819}
}
```

---

*Agent #9 complete. Cross-ref: AGENT-MANIFEST-100.md row 9; UPDATE-PLAN-2026-08.md Part 1 (PHD row TBD); docs/research/05-ai-text-detection-and-evasion/A-academic.md §16.*
