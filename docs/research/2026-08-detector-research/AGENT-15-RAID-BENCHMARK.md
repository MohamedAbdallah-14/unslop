# Agent #15 — RAID Benchmark (Robust AI Detection)

**Focus:** Paper, dataset, leaderboard, COLING 2025 shared task, what RAID broke, community debate, unslop `detector_bench.py` / `detector.py` implications.  
**Date:** 2026-08-19  
**Scope:** Full internet research + read of `benchmarks/detector_bench.py`, `unslop/scripts/detector.py`, sibling agent cross-refs.

---

## 1. Executive summary

**RAID** (Robust AI Detection) is the dominant open benchmark for machine-generated text detection — ACL 2024 ([arXiv:2405.07940](https://arxiv.org/abs/2405.07940), [ACL Anthology](https://aclanthology.org/2024.acl-long.674)). It ships **6.2M+ labeled generations** (paper count) expanding to **10M+ documents** on Hugging Face when adversarial splits and RAID-extra domains (code, Czech, German) are included. Coverage: **11 LLMs**, **8 core domains** (11 on site), **4 decoding strategies**, **11–12 black-box adversarial attacks**, plus a **hidden 10% test set** and public leaderboard at [raid-bench.xyz](https://raid-bench.xyz/).

**What RAID broke:** It ended the era of unverified "99% accurate" detector marketing. On off-the-shelf detectors at **TPR@FPR=5%**, repetition penalty alone drops accuracy up to **38 pp**; synonym swap drops Binoculars **−36.1 pp**; homoglyph drops Originality **−75.7 pp**; cross-model/domain generalization fails badly for single-generator RoBERTa detectors. RAID also institutionalized **fixed-FPR reporting** — accuracy only makes sense when false-positive rate is disclosed.

**The 2024–2026 arc is a tension, not a contradiction.** ACL 2024 (zero-shot / commercial baselines, no RAID training) reads bleak: detectors are not deployment-ready. COLING 2025 GenAI Detection Task 3 (teams **train on RAID**, all models/domains/attacks known at test time) reads optimistic: Pangram and Leidos hit **99.3% TPR@FPR=5%** clean and **97.7%** with all adversarial attacks. Shared-task authors themselves warn: results may **not extend** to unseen generators (Claude 3.5, Gemini 2), prompt-based evasion ("write undetectably"), or commercial humanizers (DIPPER, StealthRL, WriteHuman).

**unslop verdict:** RAID is the **correct citation anchor** for why unslop uses a RAID-trained scorer (TMR) and why deterministic humanization alone barely moves detector scores. It is **not** a claim that unslop beats RAID or evades Pangram-class detectors. `detector_bench.py` should stay TMR+Desklib; future work should add **RAID paraphrase/synonym attack slices** via `pip install raid-bench`, report **TPR@FPR=5%** alongside raw AI probability, and never conflate TMR's 99.28% AUROC with consumer-detector bypass.

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (arXiv)** | https://arxiv.org/abs/2405.07940 | Canonical; some secondary cites use wrong ID 2405.07926 |
| **ACL Anthology** | https://aclanthology.org/2024.acl-long.674 | Bangkok ACL 2024, pp. 12463–12492 |
| **Project site** | https://raid-bench.xyz | Leaderboard + shared-task tabs |
| **GitHub** | https://github.com/liamdugan/raid | Dataset, attack code, submission scripts |
| **PyPI package** | https://pypi.org/project/raid-bench/ | `pip install raid-bench` |
| **Hugging Face dataset** | https://huggingface.co/datasets/liamdugan/raid | RAID-train / RAID-test / RAID-extra splits |
| **COLING 2025 shared task paper** | https://arxiv.org/abs/2501.08913 | Task 3 results analysis (Jan 2025) |
| **Shared task repo** | https://github.com/liamdugan/COLING-2025-Workshop-on-MGT-Detection-Task-3 | Submission instructions |
| **Shared task leaderboard** | https://raid-bench.xyz/shared-task | Pangram / Leidos official numbers |
| **TMR (unslop default)** | https://huggingface.co/Oxidane/tmr-ai-text-detector | 99.28% RAID AUROC |
| **Desklib (bench gate)** | https://huggingface.co/desklib/ai-text-detector-v1.01 | RAID leaderboard top entry |
| **Paraphrase attack source** | https://arxiv.org/abs/2303.13408 | Krishna et al. T5-11B paraphraser |
| **unslop detector module** | `unslop/scripts/detector.py` | TMR + Desklib feedback loop |
| **unslop detector bench** | `benchmarks/detector_bench.py` | Fixture harness, release gate |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | ACL 2024 (62nd Annual Meeting, Volume 1: Long Papers) |
| **Authors** | Liam Dugan, Alyssa Hwang, Filip Trhlík, Andrew Zhu, Josh Magnus Ludan, Hainiu Xu, Daphne Ippolito, Chris Callison-Burch |
| **Affiliations** | UPenn (lead), UCL, King's College London, CMU |
| **Funding** | IARPA HIATUS Program (#2022-22072200005) |
| **License** | Dataset + tools on GitHub; HF dataset card CC BY 4.0 |

---

## 3. Dataset structure — how RAID is built

### 3.1 Generation grid

For each of ~2,000 human documents per domain, RAID generates one output per **(model × decoding strategy × adversarial attack)** combination. Figure 2 in the paper: roughly **2,000 continuations per cell** in the full grid; balanced so each human doc has exactly one generation per model/decoding/attack.

**Human sources (8 core domains):**

| Domain | Source | Risk rationale |
|--------|--------|----------------|
| Abstracts | ArXiv scrapes (2023+ only) | Factuality; anti-memorization filter |
| Books | Bamman & Smith plot summaries | First-person narrative |
| News | BBC articles (5 categories) | Misinformation / fake news |
| Poetry | poemhunter.com | Creative, repetitive failure modes |
| Recipes | RecipeNLG | Reasoning, structured output |
| Reddit | TL;DR summarization corpus | Informal, conversational |
| Reviews | IMDb movie reviews | Opinion + entity recall |
| Wikipedia | Intro paragraphs | Factual recall |

**RAID-extra (labeled, separate leaderboard track):** Python code, Czech news, German news.

### 3.2 Models (11)

GPT-2 XL, text-davinci-003 (GPT-3), ChatGPT, GPT-4, Cohere (+ Chat), MPT-30B (+ Chat), Mistral-7B (+ Chat), Llama-2-70B-Chat. Base models preferred over third-party fine-tunes; official chat variants included when available.

### 3.3 Decoding strategies (4) — RAID's novel axis

| Strategy | Settings | Notes |
|----------|----------|-------|
| Greedy | T=0 | Easier to detect (Ippolito et al. 2020) |
| Sampling | T=1, top-p=1 | Harder to detect |
| Greedy + repetition penalty | T=0, θ=1.2 | **First systematic eval** of Keskar et al. penalty |
| Sampling + repetition penalty | T=1, θ=1.2 | Open-weight models only; API models use frequency/presence penalties |

Repetition penalty produces text that **sounds more human** (less Self-BLEU repetition) and is among the strongest evasion axes in the paper.

### 3.4 Adversarial attacks (11 black-box, query-free)

Assumes adversary has **one query, zero detector knowledge** — no gradient attacks.

| Attack | Mechanism | Humanizer relevance |
|--------|-----------|---------------------|
| **Paraphrase** | Fine-tuned T5-11B (Krishna et al.) | Closest open proxy for humanizer behavior |
| **Synonym swap** | BERT candidate replacement | QuillBot-class lexical edit |
| Alternative spelling | British variants | Low |
| Article deletion | Remove "the/a/an" | Low |
| Insert paragraphs | `\n\n` between sentences | Structural |
| Upper-lower swap | Case flip | Trivial preprocessing defeat |
| Zero-width space | U+200B every other char | Unicode normalization defeat |
| Whitespace | Spaces between chars | Trivial preprocessing defeat |
| Homoglyph | Visually similar Unicode | SilverSpeak-class; kills some commercial APIs |
| Number swap | Shuffle digits | Niche |
| Misspelling | Common typo insertion | ESL-adjacent signal |

**Not in RAID:** DIPPER, TempParaphraser, Adversarial Paraphrasing, StealthRL, cross-model rewrite, commercial humanizers (WriteHuman, Undetectable.ai), prompt-based evasion ("write undetectably"). Shared-task future-work section explicitly calls for humanizer-paraphrase model testing.

### 3.5 Scale and splits

| Split | Labels | Size (paper) | Size (HF, w/ adversarial) |
|-------|--------|--------------|---------------------------|
| Non-adversarial core | ✅ | 509,014 gens + 14,971 human | — |
| Full w/ attacks | ✅ | **6,287,820 texts** | **10M+ documents** |
| RAID-train | ✅ | — | 802M / 11.8G compressed |
| RAID-test (hidden labels for leaderboard) | ❌ (10% held out) | — | 81M / 1.22G |
| RAID-extra | ✅ | Code + Czech + German | 275M / 3.71G |

**Evaluation metric (official):** **TPR @ FPR=5%** — true positive rate on machine text while misclassifying ≤5% of human text. Threshold tuned per detector per domain via iterative binary search (ε=0.0005, max 50 iterations). Domain-adjusted aggregation for cross-domain scores.

---

## 4. Paper findings — what RAID broke

### Finding 1: Accuracy is meaningless without FPR

Figure 4: detectors hit viral "99%" claims only at **similarly high FPR**. ZeroGPT plateaus at **16.9% FPR** minimum; Fast-DetectGPT at **0.88%**; Originality at **0.62%**. Binoculars uniquely strong at **low FPR**. **Impact:** TPR@FPR=5% (and lower) became the review standard; raw accuracy retired from serious detection papers.

### Finding 2: Decoding strategy is an evasion channel

Repetition penalty drops accuracy up to **38 pp** across all detector classes. Greedy >> sampling even with penalty. Past benchmarks ignored decoding variation entirely. **Impact:** "Same model, different sampling" is now a mandatory robustness axis; MAGE/HC3-era numbers deprecated for deployment claims.

### Finding 3: "Strong" detectors collapse on setting shifts

Table 5 (News domain): Originality, RADAR, Binoculars, Fast-DetectGPT go from **100% → 0.1–14%** when generator or decoding changes (e.g., Binoculars on Mistral + sampling + penalty: **0.1%**). **Impact:** Broke the narrative that any single detector is "the solution" for fake news / education deployment.

### Finding 4: Training-domain bias is inferable

RoBERTa-GPT2 hits **95%+ on GPT-2 domains**, rarely **>60%** on other models in same domain. GPTZero behavior suggests training-data leakage inference. **Impact:** Multi-generator training corpora (RAID-train) became necessary for serious classifiers; single-model RoBERTa detectors demoted to baselines.

### Finding 5: Attack vulnerability is detector-specific

Table 6 (accuracy @ FPR=5%, selected):

| Detector | Clean | Paraphrase | Synonym | Homoglyph |
|----------|-------|------------|---------|-----------|
| Binoculars | 79.6 | 80.3 (+0.7) | **43.5 (−36.1)** | **37.7 (−41.9)** |
| GLTR | 62.6 | 47.2 (−15.4) | **31.2 (−31.4)** | 24.3 (−38.3) |
| Originality | 85.0 | **96.7 (+11.7)** | 96.5 (+11.5) | **9.3 (−75.7)** |
| GPTZero | 66.5 | 64.0 (−2.5) | 61.0 (−5.5) | 66.2 (−0.3) |
| RADAR | 70.9 | 67.3 (−3.6) | 67.5 (−3.4) | 59.3 (−11.6) |

**Paradox:** Some attacks *improve* RoBERTa-GPT2 (+16.2 paraphrase, +22.7 synonym) — contemporaneous model families (GPT-2/RoBERTa/T5/BERT) share training distribution. **Impact:** Broke one-size-fits-all evasion advice; validated adversarially trained RADAR; showed commercial detectors are not interchangeable.

### Finding 6: Commercial vs open-source gap (ACL 2024 snapshot)

Table 4 aggregate (non-adversarial, @ FPR=5%): Binoculars **79.6%**, Originality **85.0%**, GPTZero **66.5%**, Winston **71.0%**, Fast-DetectGPT **73.6%**, RADAR **70.9%**. None of the 2024 commercial APIs match their marketing on RAID. **Impact:** Vendor blog claims require third-party benchmark; Originality's RAID paraphrase **96.7%** still cited in 2026 despite model supersession (Agent #58).

### Ethics statement (paper)

Authors **oppose punitive/detector-only disciplinary use**; cite Liang et al. ESL bias; argue poorly calibrated detectors cause more harm than they solve. RAID intended to improve evaluation standards, not greenlight high-stakes deployment.

---

## 5. Leaderboard infrastructure

### 5.1 Two-track design

[raid-bench.xyz](https://raid-bench.xyz/) splits submissions:

1. **Generalization track** — detectors **not** trained on RAID
2. **RAID-trained track** — self-reported training on RAID (TMR, Desklib, shared-task winners)

Hidden **10% test labels** prevent train-set gaming. Submission via PR to GitHub with `predictions.json`; `raid-bench` CLI scores against held-out labels.

### 5.2 Key open-model leaderboard entries (HF / model cards)

| Model | Architecture | RAID AUROC | TPR@5% FPR (all settings) | TPR@5% FPR (no adv.) | Train on RAID? |
|-------|--------------|------------|---------------------------|----------------------|----------------|
| **Desklib v1.01** | DeBERTa-v3-large (304M) | Top entry (claimed) | — | — | Yes |
| **TMR** | RoBERTa-base (125M) | **99.28%** | **95.79%** | **99.65%** | Yes (50k stratified samples) |
| **Binoculars** | Falcon-7B pair (zero-shot) | — | **79.0%** (shared task baseline) | — | No |
| **RADAR** | Vicuna-7B adversarial | — | **65.6%** | — | No |
| **OpenAI RoBERTa-L** | GPT-2 detector | — | **55.7%** avg domains | — | No |

TMR evaluated on **672,000 test samples** including adversarial attacks (model card). unslop cites this number in `detector.py` and `detector_bench.py`.

### 5.3 COLING 2025 Shared Task (Task 3) — the optimism counter-narrative

**Setup:** All 11 models + 8 domains + 11 attacks **known at train time**; hidden test articles only. 9 teams, 23 submissions. Metric: same TPR@FPR=5%.

**Subtask A (cross-domain, no adversarial):**

| Team | Total TPR@5% FPR | σ |
|------|------------------|---|
| Leidos v1.0.3 | **99.4%** | 0.6 |
| **Pangram** | **99.3%** | 0.4 |
| USTC-BUPT (RoBERTa-L focal) | 98.1% | 1.3 |
| Binoculars [Ba] | 79.0% | 2.4 |
| RADAR [Ba] | 65.6% | 25.7 |

**Subtask B (all adversarial attacks):**

| Team | Total TPR@5% FPR | Weakest attack | PP | SY | HG |
|------|------------------|----------------|-----|-----|-----|
| Leidos v1.0.2 | **97.7%** | ZW 92.7% | 92.3% | 98.6% | 97.3% |
| **Pangram** | **97.7%** | HG 91.9% | **91.6%** | 96.2% | 91.9% |
| Binoculars [Ba] | 71.3% | SY **43.5%** | 80.3% | 43.5% | 37.7% |

**Hardest attacks (avg across all submissions):** Homoglyph **49.2%**, Paraphrase **60.6%**, Synonym **61.3%**. Even winners lose ~8 pp on paraphrase vs clean.

**Winning techniques:** text normalization (Pangram), hard-negative mining (Pangram, Leidos), focal loss on misclassified RAID train examples (USTC-BUPT), adversarial preprocessing classifiers (CNLP-NITS).

---

## 6. Community debate (2024–2026)

### 6.1 Pessimists — ACL 2024 reading

- **Sadasivan impossibility camp:** RAID confirms paraphrase/sampling break static detectors; no fixed classifier survives adaptive adversary (Agent #17).
- **Vendor skepticism:** Originality homoglyph **9.3%**, Winston/ZeroGPT mid-60s — marketing vs RAID gap validates Weber-Wulff / Elkhatat education-journal findings.
- **Deployment opponents:** RAID ethics statement + Liang ESL bias → institutional Turnitin rollbacks (Vanderbilt, UT Austin, Northwestern per Cat 05 synthesis).
- **Zero-shot decline:** Binoculars best metric method at 79.6% clean but **43.5%** under synonym — curvature/perplexity family demoted from "SOTA" to "academic baseline" (Agents #05, #06, #08).

### 6.2 Optimists — COLING 2025 / detector-vendor reading

- **"Detection solved in constrained settings"** (shared-task conclusion): if you know the model set, domains, and attack catalog, **99%+ TPR@5% FPR** is achievable (Pangram, Leidos).
- **Pangram / Originality** cite RAID paraphrase splits in marketing; Originality blog claimed **#1 on RAID** with **96.7%** paraphrase (ACL-era model 2.0 Standard — stale vs Turbo 3.0.2, Agent #58).
- **Retraining narrative:** 30-day detector patch cadence (GPTZero greylist, Originality Turbo) argues static humanizer benchmarks decay.

### 6.3 Methodological critics

- **Confounding artifacts** (shared-task Limitations, Gritsai et al. 2025 survey): human recipes = paragraph form; ChatGPT recipes = numbered lists → trivial format feature. Manual clean dropped RoBERTa-base **92.67 → 89.67** (−3 pp) — authors say insufficient evidence yet, investigating.
- **Benchmark overfitting** (RAID paper Limitations): optimizing for RAID specializes to covered axes; hidden test mitigates but doesn't eliminate Goodhart's law.
- **Attack realism gap:** RAID paraphrase = T5-11B; DAMAGE/StealthRL/AdvPara use LLM rewrite policies that crush Binoculars (**94.15% → 28.23%** TPR@5%, Agent #12) — RAID paraphrase split **understates** 2025–2026 humanizer threat.
- **Train/test leakage caveat:** Human doc sources are public URLs; participants could have seen test human passages (shared task acknowledges; argues machine labels still hidden).

### 6.4 The reconciled picture

RAID broke **inflated zero-shot and commercial claims** and established **attack-inclusive evaluation**. It did **not** break the arms race — it **relocated** it: from "can you detect GPT-4 greedy?" to "can you detect GPT-4 + sampling + penalty + synonym swap?" to (2025) "can you detect RAID-trained Pangram after StealthRL?" The answer depends on **who trains on what** and **which attack generator** you use.

---

## 7. Comparison to sibling benchmarks

| Benchmark | Size | Models | Attacks | Decoding | Multilingual | unslop usage |
|-----------|------|--------|---------|----------|--------------|--------------|
| **RAID** | 6.2M–10M+ | 11 | 11–12 | ✅ 4 strategies | Partial (extra split) | **Primary** — TMR training, detector_bench citation |
| MAGE (Li et al. 2024) | 447k | 27 | Limited | Partial | No | DivEye, AdaDetectGPT comparisons |
| M4 | 122k | Multi | No | Unspecified | ✅ | Cross-lingual robustness |
| HC3 / HC3-Plus | 27k–210k | Few | No | No | No | QA-domain only |
| MGTBench 2.0 | Small | Academic cats | Some | No | No | Category-specific |
| DAMAGE eval | Vendor pool | 19 humanizers | L1–L3 tiers | N/A | No | Commercial humanizer audit |
| Chicago Booth 2026 | Independent | Consumer | Humanizers | N/A | No | GPTZero/Pangram external ref |

RAID Table 1 claim: **only public dataset** with diverse models + domains + sampling + adversarial attacks together. Still true for English prose at this scale (Aug 2026).

---

## 8. unslop bench implications

### 8.1 Current architecture (correct choices)

```python
# unslop/scripts/detector.py — DEFAULT_DETECTOR = "tmr"
# Oxidane/tmr-ai-text-detector — 99.28% RAID AUROC, MIT, ~500MB
# desklib/ai-text-detector-v1.01 — RAID leaderboard top, ~1.2GB
```

TMR is **Self-Hard-Negative mined RoBERTa-base** on **50k stratified RAID samples** (45% human / 55% AI). This is exactly the detector family RAID shared task proves can hit **99%+** when fully trained — but TMR is a **lightweight community checkpoint**, not Pangram/Leidos production stack.

`benchmarks/detector_bench.py` release gate: humanized `balanced` must score **strictly lower** AI probability than original on **both** TMR and Desklib, every fixture. This is **necessary but insufficient** vs RAID adversarial splits.

### 8.2 What unslop benchmarks today vs what RAID measures

| Dimension | `detector_bench.py` | RAID full test |
|-----------|---------------------|----------------|
| Detectors | TMR + Desklib | 12+ baselines + submissions |
| Attacks | None (clean prose only) | 11 adversarial + 4 decoding |
| Metric | Raw AI probability | TPR@FPR=5% |
| Text source | Curated fixtures (assistant output) | 11 LLMs × 8 domains |
| Humanizers | Not simulated | T5 paraphrase only |

**Measured gap (sibling agents):** Deterministic unslop moves TMR **~0.0–0.2 pp** on fixtures (Agent #35) — consistent with RAID showing **lexical/rule edits insufficient** vs modern classifiers; synonym/paraphrase attacks move scores **15–36 pp** on zero-shot methods.

### 8.3 README / marketing guardrails

From Cat 05 synthesis and Agent #58:

- **Say:** "TMR is RAID-trained; 99.28% AUROC on 672k RAID test samples including adversarial attacks."
- **Say:** "Consumer detectors disagree; RAID paraphrase split is the best open proxy for humanizer behavior."
- **Don't say:** "Unslop evades RAID" without running `raid-bench` paraphrase/synonym slices.
- **Don't say:** "Beats GPTZero/Turnitin" from TMR score alone — different training distribution, patch cadence, ensemble layers.

### 8.4 Recommended bench upgrades (priority order)

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P1** | Add `--raid-attacks paraphrase,synonym` to `detector_bench.py` via `raid-bench` attack API | Close humanizer-proxy gap (Agent #31 DIPPER) |
| **P1** | Report **TPR@FPR=5%** alongside mean AI probability in bench JSON | Align with RAID standard; raw prob misleading |
| **P2** | Fixture slice: ESL / short / list-heavy text | RAID confound + Liang bias regression |
| **P2** | Dual-report: TMR score + Binoculars score (optional flag) | Disagreement signals need structural paraphrase |
| **P3** | Submit unslop humanized outputs to RAID generalization track | Third-party eval credibility |
| **P3** | Track Pangram shared-task checkpoint if open-sourced | Harder commercial proxy than TMR |

### 8.5 Anti-detector mode framing

RAID supports unslop's **honest** anti-detector positioning:

1. **Rule-only humanization** barely moves RAID-trained classifiers — users need cross-model paraphrase (already in `detector.py` exhaustion message).
2. **RAID paraphrase @ 91.6% TPR** (Pangram, best case) still misses **~8%** — deterministic unslop will not replicate that without LLM rewrite.
3. **ESL defense** is orthogonal to RAID (Liang): humanization that removes AI-isms may help false-positive cases RAID never tested.
4. **Boundaries hold:** anti-detector for ESL/resume writers, not academic misconduct — RAID ethics statement aligns.

---

## 9. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| RAID generations (paper) | 6,287,820 texts | ACL 2024 §4.1 |
| RAID documents (site/HF) | 10M+ | raid-bench.xyz, HF card |
| Models × domains × attacks | 11 × 8 (+3 extra) × 11–12 | Paper + site |
| Binoculars clean TPR@5% | 79.6% (paper) / 79.0% (shared task) | Table 4 / Task 3 |
| Binoculars synonym TPR@5% | 43.5% | Table 6 |
| Originality homoglyph TPR@5% | 9.3% | Table 6 |
| Originality paraphrase TPR@5% | 96.7% | Table 6 (ACL-era API) |
| Repetition penalty max drop | 38 pp | Finding 2 |
| TMR RAID AUROC | 99.28% | HF model card |
| TMR TPR@5% FPR (all) | 95.79% | HF model card |
| Pangram shared task clean | 99.3% | arXiv:2501.08913 Table 4 |
| Pangram shared task + adv. | 97.7% | Table 5 |
| Pangram paraphrase attack | 91.6% | Table 5 |
| unslop deterministic Δ TMR | ~0.0–0.2 pp | Agent #35 fixtures |

---

## 10. Open questions

1. **Will RAID v2 ship?** Paper acknowledges obsolescence as models advance; no GPT-4o/Claude-3.5/Gemini generations in current set.
2. **Confound audit completion?** Shared task flagged recipe list formatting; full Gritsai-quality survey pending.
3. **TMR vs Pangram on unslop fixtures?** TMR is proxy; Pangram is production adversary for humanizer-resistant claims.
4. **DIPPER/StealthRL RAID submission?** Strongest evasion tools absent from RAID attack catalog — custom eval needed.
5. **Desklib exact leaderboard numbers?** HF timeout during research; verify before next README edit.
6. **AUROC vs TPR@FPR=5% for unslop gate?** TMR reports both; bench uses raw probability — should migrate.

---

## 11. Cross-references (sibling agents)

| Agent | Relevance |
|-------|-----------|
| #05 Fast-DetectGPT | No full RAID entry; TempParaphraser collapse |
| #06 Binoculars | RAID Table 6 synonym/homoglyph; 79.0% baseline |
| #08 DetectGPT lineage | TMR vs curvature; RAID as review gate |
| #12 DAMAGE | Humanizer tiers vs RAID T5 paraphrase gap |
| #17 Sadasivan | Impossibility vs RAID shared-task optimism |
| #31 DIPPER | RAID paraphrase split ≠ DIPPER eval |
| #58 Originality | RAID 96.7% paraphrase stale model |
| #60 Pangram vs GPTZero | Shared task winner; paraphrase robustness |
| UPDATE-PLAN-2026-08 | Dual-benchmark honesty (in-domain + OOD) |

---

## 12. Citations

```bibtex
@inproceedings{dugan-etal-2024-raid,
  title={{{RAID}}: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors},
  author={Dugan, Liam and Hwang, Alyssa and Trhl{\'\i}k, Filip and Zhu, Andrew and
          Ludan, Josh Magnus and Xu, Hainiu and Ippolito, Daphne and Callison-Burch, Chris},
  booktitle={Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
             (Volume 1: Long Papers)},
  pages={12463--12492},
  year={2024},
  url={https://aclanthology.org/2024.acl-long.674}
}

@article{dugan2025raidsharedtask,
  title={Gen{AI} Content Detection Task 3: Cross-Domain Machine-Generated Text Detection Challenge},
  author={Dugan, Liam and Zhu, Andrew and Alam, Firoj and Nakov, Preslav and
          Apidianaki, Marianna and Callison-Burch, Chris},
  journal={arXiv preprint arXiv:2501.08913},
  year={2025}
}
```

---

*Agent #15 complete. RAID is the evaluation backbone unslop already cites — the work is aligning benchmarks with RAID's adversarial splits and TPR@FPR metrics, not pretending deterministic passes solve the benchmark.*
