# Agent #11 — Why AI Detection Fails (SHAP Cross-Domain)

**Topic:** Pudasaini et al., *Why AI-Generated Text Detection Fails: Evidence from Explainable AI Beyond Benchmark Accuracy* (arXiv:2603.23146)  
**Prepared:** August 19, 2026  
**Scope:** SHAP validity diagnostic, 38-feature stylometric framework, cross-domain/cross-generator collapse, error analysis, debate map, unslop integration  
**Status:** complete

---

## Executive summary

Pudasaini et al. (2026) is the first paper to treat **explainability as a validity test**, not just a transparency garnish, for AI-text detectors. The authors train classical ML classifiers (LR, SVM, RF, XGBoost) on **38 interpretable linguistic features** drawn from StyloAI and Terčon survey lineages, achieve **leaderboard-competitive in-domain F1** (0.9734 on PAN@CLEF 2025, 0.8025 on COLING 2025), then show those same models **collapse under cross-domain and cross-generator shift**. The diagnostic tool is **SHAP**: global and instance-level attributions reveal that **the top features differ completely between benchmarks** — PAN models lean on POS diversity; COLING models lean on paragraph count and GZIP compression ratio — proving detectors learn **corpus-specific stylistic artefacts**, not stable machine-authorship signatures.

The central tension, stated explicitly in §4.8: *the features most discriminative in-domain are the features most susceptible to domain shift, formatting variation, and text-length effects.* Three SHAP-driven failure modes dominate: (1) **paragraph count** as a formatting proxy (median TP = 1 paragraph, median TN = 17); (2) **GZIP ratio** confounded by length and genre; (3) **short-text degradation** (modal FP at 34 words, modal FN at 14 words).

**Unslop verdict (UPDATE-PLAN rating: 3/5):** This paper **validates dual-benchmark honesty** — never report a single in-domain AUROC/F1 without OOD context. It partially **supports** unslop's burstiness and sentence-variation levers (Sentence Length Variation is in the 38-feature set and appears in instance-level SHAP plots) but **warns** that optimizing any single stylometric axis is fragile: detectors swap decision criteria by corpus. Anti-detector mode should keep multi-signal distribution shaping + cross-model paraphrase as primary; `--detector-feedback` score chasing is explicitly secondary and corpus-dependent.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | Why AI-Generated Text Detection Fails: Evidence from Explainable AI Beyond Benchmark Accuracy |
| **Authors** | Shushanta Pudasaini, Luis Miralles-Pechuán, David Lillis, Marisa Llorens Salvador |
| **Affiliations** | Technological University Dublin; University College Dublin |
| **arXiv** | https://arxiv.org/abs/2603.23146 |
| **HTML** | https://arxiv.org/html/2603.23146v2 |
| **Project page** | https://shushantatud.github.io/ExplainAIGeneratedText/ |
| **GitHub** | https://github.com/ShushantaTUD/Explain_AI_Generated_Text |
| **PyPI package** | `xai-text-classifier` (also referenced as `explain-ai-generated-text` on project page) |
| **Funding** | Science Foundation Ireland Grant 18/CRT/6183 |
| **Keywords** | LLMs, AI-generated text detection, ML, XAI, academic integrity |

**One-line contribution:** Competitive feature-based detection + SHAP proof that benchmark winners learn dataset artefacts; cross-domain evaluation and instance-level error analysis expose why.

**Prior work by same group:** Pudasaini et al. also published COLING 2025 workshop papers on benchmarking detectors (GenAIDetect proceedings) and ensemble methods with frozen encoders (CLEF 2025). This arXiv paper consolidates and extends that line with the SHAP validity framework.

---

## 2. Mechanism — interpretable detection pipeline

### 2.1 Feature space (38 → 30 optimal per corpus)

Each document becomes a vector of **38 hand-crafted features** spanning five dimensions (Table 1 in paper):

| Dimension | Example features |
|-----------|------------------|
| Surface / length | Character count, word count, sentence count, **paragraph count**, punctuation count |
| Lexical diversity | TTR, hapax ratio, word entropy, repetition rate, unique word count |
| Readability / predictability | Flesch reading ease, **GZIP compression ratio**, predictability score (mean −log unigram P) |
| Syntactic structure | Sentence complexity, clause–sentence ratio, **sentence length variation**, **sentence length difference**, POS diversity, POS n-gram variety, grammatical mistakes (LanguageTool) |
| Discourse / style / sentiment | Discourse markers, transition variety, paragraph coherence, pronoun ratio, personal voice, modal/negation frequency, hedge score, sentiment polarity/subjectivity, emotion variation, specificity, figurative language |

**Feature selection:** Recursive Feature Elimination with Cross-Validation (RFECV, XGBoost base, 5-fold stratified) reduces 38 → **30 optimal features per dataset separately**. PAN and COLING do not share the same "optimal" subset — itself evidence of dataset dependence.

**Toolchain:** NLTK Punkt, spaCy `en_core_web_sm`, LanguageTool 5.7, TextBlob, scikit-learn TF-IDF.

### 2.2 Classifiers and ensemble

Four base models: Logistic Regression, SVM, Random Forest, XGBoost. Best in-domain: **SVM (F1 0.9734)** on PAN; **Random Forest (F1 0.8025)** on COLING.

**Ensemble:** Equal-weight average of predicted probabilities from all four models. Evaluated on held-out **Ghostbuster** corpus (never used for training or feature selection).

### 2.3 SHAP as validity diagnostic

SHAP (SHapley Additive exPlanations) applied post-hoc to all classifiers:

- **Global:** summary plots / mean |SHAP| per feature — compared across PAN vs COLING trained models
- **Instance-level:** waterfall and bar plots for individual human vs AI samples
- **Error analysis:** SHAP on TP, TN, FP, FN buckets from COLING test set (10,000 samples: 2,753 FP, 139 FN, 6,141 TP, 967 TN)

The paper's methodological claim: if detectors measured universal authorship, **feature importance rankings would be stable across corpora**. They are not.

---

## 3. Datasets and domain shift setup

| Dataset | Role | Scale | Domains | Generators |
|---------|------|-------|---------|------------|
| **PAN@CLEF 2025** | Train / in-domain test | 23,707 train; 3,589 dev | Essays, news, fiction | GPT-4o + obfuscated human authorship |
| **COLING 2025 GenAIDetect** | Train / in-domain test | 610,767 EN train; 261,758 dev | Peer reviews, student essays, papers, news, 8+ more | GPT-4/4o, Mistral, Llama 3.1, Qwen-2, Claude, others |
| **Ghostbuster** | Held-out cross-corpus test only | 6,000 (2k human / 2k GPT-3.5 / 2k Claude) | Student essays, creative writing, news (WP, Reuters, Essay subsets) | GPT-3.5-turbo (train); Claude (generalisation) |

**Pre-training exploratory analysis (Table 3):** PAN texts are longer and more narrative (mean ~695 words human, ~26 paragraphs); COLING shorter and informational (~260 words, ~7 paragraphs). t-SNE shows **partial separation on PAN, substantial overlap on COLING** — COLING is intrinsically harder.

**Evaluation protocols:**
1. In-domain (train/test same benchmark)
2. Cross-domain (train PAN → test COLING, reverse)
3. Cross-generator (test on GPT-5.2, DeepSeek V3.2, Gemini 3 Pro — all post-dataset curation)
4. Ghostbuster ensemble (fully held out)

---

## 4. Headline numbers

### 4.1 In-domain (looks solved)

| Benchmark | Best model | F1 | Notes |
|-----------|------------|-----|-------|
| PAN@CLEF 2025 | SVM | **0.9734** | 2nd on official leaderboard; beats TF-IDF SVM baseline (0.904) and Binoculars baseline (0.866) |
| COLING 2025 | Random Forest | **0.8025** | 7th on leaderboard; top system (mdok/KInIT fine-tuned LLM) hits 0.989 |

**Error asymmetry even in-domain:** On PAN test set, FPR ranges **6.0–11.0%** across models despite F1 ≥ 0.95. Near-SOTA F1 still flags non-trivial share of genuine human work.

### 4.2 Cross-domain collapse (Table 8)

| Train → Test | Best F1 in-domain | F1 on other benchmark | Drop |
|--------------|-------------------|----------------------|------|
| PAN → COLING | 0.9694 (XGB) | **0.6723** (XGB) | −29.7 pp |
| COLING → PAN | 0.8025 (RF) | **0.8284** (LR) | asymmetric transfer |

**Asymmetry interpretation (authors):** COLING's broader diversity may produce more generalisable models; PAN models overfit narrative/obfuscation-specific cues. Lower COLING in-domain F1 (~80%) may reflect task difficulty, not just model weakness.

### 4.3 Cross-generator FNR (Table 9) — generator-specific, not universal

| Generator | Best-PAN FNR | Best-COL FNR |
|-----------|--------------|--------------|
| GPT-5.2 | **23.25%** | 3.42% |
| DeepSeek V3.2 | 0.76% | 3.51% |
| Gemini 3 Pro | 0.43% | **18.40%** |

Neither training corpus yields a model robust to all unseen generators. Performance is **stylistically coupled to generator output register**.

### 4.4 Ghostbuster held-out ensemble (Table 10)

| Condition | Avg F1 (single best) | Ensemble F1 | Gain |
|-----------|---------------------|-------------|------|
| PAN-trained | 64.0 | **94.61** | +30.6 pp |
| COLING-trained | 78.59 | **87.13** | +8.5 pp |

Ensembling **dramatically** recovers cross-corpus performance but **does not equalise domains** (WP subset: Ens-PAN 92.87 vs Ens-COL 77.77). Wikipedia's neutral encyclopaedic register remains hardest — the register LLMs default to.

---

## 5. SHAP cross-domain feature analysis

### 5.1 Global feature importance — minimal overlap

| Corpus | Top SHAP drivers (global) | Interpretation |
|--------|---------------------------|----------------|
| **PAN CLEF** | **POS diversity** dominates; POS n-gram variety, sentence complexity follow | Syntactic tag entropy separates obfuscated-fiction-style human text from GPT-4o essays |
| **COLING** | **Paragraph count**, **GZIP compression ratio** dominate | Structural/formatting + redundancy signals separate Wikipedia/Reddit human prose from shorter AI peer reviews |

**Key finding:** "If models were detecting inherent properties of machine-generated language, feature importance would remain consistent across datasets. Instead, explanations show that different corpora induce different decision criteria." (§4.6)

Figure 4–5 in paper: side-by-side SHAP summary plots show **near-zero overlap** in top-10 feature rankings.

### 5.2 Instance-level patterns

Waterfall plots (Figures 6–7) show individual predictions driven by **combinations** of:
- Sentence length variation
- Punctuation usage
- Syntactic diversity (POS patterns)
- Paragraph structure

These combinations **shift by domain** — a human Wikipedia stub and a human fiction excerpt trigger different feature bundles even when both are correctly classified in-domain.

### 5.3 Error analysis — three SHAP-diagnosed failure modes (§4.7)

**Failure I — Paragraph count is formatting, not linguistics**

- Globally #1 on COLING; largest ΔSHAP between FP and FN (+0.109)
- Learned rule: **single-paragraph → AI** (TP median = 1 para; TN median = 17)
- FP humans with 1 paragraph structurally mimic AI TPs
- FN AI with multi-paragraph structure (mean 13.2 paras) mimics human TN distribution

**Failure II — GZIP ratio is domain-confounded**

- #2 contributor to misclassification (ΔSHAP = +0.097)
- Lower compression → AI association in training distribution
- FN AI texts show **highest mean GZIP (0.724)** — high lexical diversity pushes into human-like compression range
- Not a stable generative signature; interacts with length and genre

**Failure III — Short-text feature starvation**

- FP mean 221 words vs TN mean 421 words (−47%)
- FN mean 177 words vs TP mean 243 words (−27%)
- Modal lengths: **14 words (FN), 34 words (FP)** — many errors on very short inputs
- Prior bias toward AI class makes short human text disproportionately flagged

**Practical recommendation from authors:** minimum text-length thresholds or length-aware feature normalisation before deployment.

---

## 6. Who agrees, who qualifies, who disagrees

### 6.1 Strong agreement — dataset artefacts dominate

| Source | Relationship | Key overlap |
|--------|--------------|-------------|
| **Doughman et al., COLING 2025** ([2406.11073](https://arxiv.org/abs/2406.11073)) | Independent audit; **cited by Pudasaini §3.2.1** | Detectors sensitive to adverbs, sentence length, readability; F1 drops to **random on some style subsets**; overfit punctuation/whitespace |
| **Terčon & Dobrovoljc survey** ([2510.05136](https://arxiv.org/abs/2510.05136)) | Feature vocabulary source; **cited §1, §3.1** | "No single feature reliably distinguishes authorship"; feature importance varies by generator/dataset |
| **Sadasivan impossibility** ([2303.11156](https://arxiv.org/abs/2303.11156)) | Theoretical complement; **cited §1** | TV bound on detectability; distribution overlap caps AUROC — different mechanism, same deployment pessimism |
| **Liang ESL bias** ([2304.02819](https://arxiv.org/abs/2304.02819)) | Indirect support | Formal, low-contraction, constrained prose → FP; aligns with Failure I/III (short, structurally "AI-like" human text) |
| **RAID / MGTBench literature** | Benchmark ecosystem | Cross-domain FN inflation under paraphrase and domain shift — Pudasaini adds *why* via SHAP |
| **Ji et al. 2025** ([2406.18259](https://arxiv.org/abs/2406.18259)) | Cited §1 as "explainability is complicated" | XAI on detectors is hard; Pudasaini responds by using XAI specifically for **validity**, not user trust alone |

### 6.2 Partial agreement — methods that partially resist the critique

| Source | Nuance |
|--------|--------|
| **Ghostbuster (Verma et al., NAACL 2024)** | Paper uses Ghostbuster as OOD testbed. Ghostbuster's *original* claim: 97 F1 OOD via multi-LM probability features. Pudasaini shows **their** stylometric ML on Ghostbuster starts at **64 F1** (single model) before ensemble rescues to 94.61 — different feature family, different generalisation story. Not a direct refutation; shows ensemble + feature diversity matters. |
| **mdok/KInIT fine-tuned LLM** (PAN leaderboard #1, F1 0.989) | Pudasaini beats baselines but not #1. Paper does **not** cross-test mdok cross-domain with SHAP — open question whether transformer detectors share the artefact problem (likely yes per PHD/Tulchinskii RoBERTa 0.99→0.535 cross-domain). |
| **Ensemble methods** (Mobin et al., Kristanto et al.) | Pudasaini **confirms partial robustness** (+30 F1 on Ghostbuster) but states ensembles "do not fully resolve the underlying validity problem" — still corpus-cue dependent. |
| **DivEye / surprisal-variance detectors** | Not evaluated in this paper. Hypothesis: model-internal signals may be less formatting-dependent than paragraph count — but still generator-pair sensitive. orthogonal evidence needed. |

### 6.3 Disagreement or tension — where critics push back

| Counter-argument | Response / status |
|------------------|-------------------|
| **"Feature engineering is the wrong detector class; fine-tuned RoBERTa solves this"** | RoBERTa classifiers show **equal or worse** cross-domain collapse in parallel literature (Tulchinskii PHD: 0.990→0.535 Wiki→Reddit). Pudasaini's point is about **measurement validity**, not classifier family. SHAP on stylometric models makes the failure **interpretable**; black-box collapse is harder to diagnose. |
| **"Your detectors are too simple"** | Deliberate choice. Simple models + SHAP isolate *what signal exists in features*. Complexity would obscure the validity question. |
| **"Ghostbuster ensemble hits 94 F1 OOD — problem solved"** | Only on Ghostbuster's three domains after four-model averaging. WP subset still 77.77 for COLING ensemble. Wikipedia neutral register ≈ default LLM register — hardest case persists. |
| **"Commercial detectors use proprietary signals"** | True and untestable. Paper's claim is epistemic: **any** detector reporting in-domain benchmark scores without OOD + explanation evidence should not be trusted for high-stakes use. Turnitin cited (Chechitelli 2023: <1% doc-level FPR) as example of headline rate that scales to mass wrongful flags. |
| **Ji et al. — explainability is complicated** | Pudasaini agrees XAI isn't trivial but argues instance-level SHAP still beats zero explanation for **validity auditing**. |

### 6.4 Community reception (as of Aug 2026)

- Listed in unslop `docs/research/15-academic-papers-llm-humanization/` and `UPDATE-PLAN-2026-08.md` as **must-read for implementers**
- Open-source package released; early PyPI (`xai-text-classifier`) — reproducibility friendly
- No major public rebuttal located; converges with COLING 2025 "limitations" workshop thread
- HuggingFace / leaderboard community: reinforces post-RAID skepticism of single-number AUROC marketing

---

## 7. Unslop implications

### 7.1 What the paper validates in unslop's design

| unslop mechanism | Paper connection | Verdict |
|------------------|------------------|---------|
| **Burstiness / sentence-length variance** (`validate.py`, anti-detector §92) | `Sentence Length Variation` and `Sentence Length Difference` in 38-feature set; appear in instance SHAP plots | **Supported as human-like signal** — but domain-dependent; not sufficient alone |
| **Dual-benchmark honesty** (UPDATE-PLAN 3/5 rating) | Core paper thesis | **Adopt:** any unslop detector benchmark should report in-domain + OOD (e.g., TMR on RAID + domain subset) |
| **Anti-detector as false-positive defense, not forensic proof** (`SKILL.md` boundaries) | Authors: "probabilistic signal… never automated basis for punitive decisions" | **Aligned** — cite Pudasaini in product docs for ESL/education use case |
| **Multi-lever anti-detector** (burstiness + contractions + specificity + cross-model pass) | Single-feature optimisation matches Failure I–III | **Correct architecture** — paper explicitly warns against surface-feature gaming |
| **`--detector-feedback` as secondary** (`detector.py`) | Detector features shift by corpus; score chasing optimises one distribution | **Keep deprioritised** — ladder exhaustion → cross-model paraphrase recommendation is right |

### 7.2 What the paper warns unslop about

| Risk | Detail | Mitigation |
|------|--------|------------|
| **Paragraph-count blind spot** | unslop does not target paragraph structure | Consider structural pass hint: multi-paragraph breaks for long outputs in anti-detector mode (careful: don't destroy user formatting) |
| **Short-text unreliability** | Modal errors at 14–34 words | `validate.py` should warn on samples <100 words before detector check; already informational burstiness — extend to detector disclaimer |
| **GZIP / redundancy proxy** | High lexical diversity evades COLING-trained models | Lexical diversity alone can **increase** FN risk if other features don't shift — burstiness without TTR inflation |
| **Feature overlap with unslop targets** | Optimising sentence variation helps on PAN-like corpora (POS diversity regime) but may not transfer to COLING-like (paragraph/GZIP regime) | Document that anti-detector effectiveness is **genre-dependent** |
| **Ensemble detector arms race** | Commercial tools (Copyleaks V9, etc.) already ensemble | Distribution shaping beats single-detector green |

### 7.3 Codebase touchpoints

| File | Suggested action | Priority |
|------|------------------|----------|
| `unslop/scripts/validate.py` | Add optional `--min-words-for-detector` warning (≥150 words per Failure III) | Low |
| `unslop/scripts/stylometry.py` | Map overlap: sentence length σ, TTR, Flesch, punctuation — compare to paper's 38-feature list for benchmark reporting | Medium |
| `unslop/scripts/detector.py` | Docstring cite: in-domain TMR ≠ cross-domain; recommend RAID subset eval | Medium |
| `benchmarks/` | Add stylometric XGBoost baseline + SHAP dump on unslop fixtures (replicate paper methodology on internal samples) | Research |
| `docs/research/05-ai-text-detection-and-evasion/` | Cross-link Agent #11 memo; already indexed at 2603.23146 | Done via this memo |
| `skills/unslop/SKILL.md` | Optional footnote under anti-detector: "detectors swap features by corpus (Pudasaini 2026)" | Low |

### 7.4 Anti-detector lever ordering — paper-informed revision

Current SKILL.md ordering: cross-model paraphrase > burstiness > specificity > contractions.

Paper reinforces this ordering:
1. **Cross-model paraphrase** — changes full feature bundle, not one axis susceptible to domain shift
2. **Burstiness band (σ ≥ 6)** — targets Sentence Length Variation, but interact with paragraph structure
3. **Specificity / rough edges** — moves content-level signals less captured by paragraph count alone
4. **Contractions** — register signal; weak alone per Agent #41 (Paneru)

**Do not add:** paragraph-count stuffing or GZIP gaming — paper identifies both as **unstable, domain-confounded** cues that create new failure modes.

### 7.5 Product / docs quotes (ready to use)

> Benchmark accuracy is not reliable evidence of authorship detection: strong in-domain performance can coincide with substantial failure under domain and generator shift. — Pudasaini et al., §Abstract

> The features that are most discriminative on in-domain data are also the features most susceptible to domain shift, formatting variation, and text-length effects. — §4.8

Use in README "anti-detector" boundary section and ESL false-positive defense — **not** as "beat Turnitin" marketing.

---

## 8. Comparison to adjacent unslop agent memos

| Agent | Relationship |
|-------|--------------|
| **#07 Ghostbuster** | Same Ghostbuster corpus as OOD test; Pudasaini ensemble 94.61 F1 vs Ghostbuster paper's 99 F1 in-domain — different methods, same dataset, reconcilable via feature family |
| **#09 PHD/Tulchinskii** | RoBERTa cross-domain 0.535 — complements SHAP story for neural detectors |
| **#17 Sadasivan** | TV bound = why distribution shaping; Pudasaini = why benchmark scores lie about shaping success |
| **#41 Paneru contractions** | Single-feature contraction lift insufficient; Pudasaini shows **multi-feature interactions** dominate |
| **#42 Rallapalli Biber** | SHAP interactions on register features — same "no single lever" conclusion from different feature vocabulary |
| **#49 Burstiness** | Already cites 2603.23146 for Sentence Length Variation — this memo is canonical depth |

---

## 9. Open questions / future work (from paper + unslop lens)

1. **SHAP on TMR/RoBERTa detectors** — token-level vs stylometric validity diagnostic; Ji et al. says hard; still worth a spike
2. **Multilingual** — paper English-only; COLING has multilingual track not fully analysed here
3. **Longitudinal generator drift** — GPT-5.2/Gemini 3 tested; six-month re-run needed
4. **Integrate `xai-text-classifier` as optional `--explain` flag** in `detector.py` — returns SHAP alongside TMR score for power users
5. **Minimum-length policy** — institutional recommendation aligned with Failure III

---

## 10. Primary URLs (quick reference)

| Resource | URL |
|----------|-----|
| Paper (arXiv) | https://arxiv.org/abs/2603.23146 |
| Paper (HTML v2) | https://arxiv.org/html/2603.23146v2 |
| Project page | https://shushantatud.github.io/ExplainAIGeneratedText/ |
| GitHub | https://github.com/ShushantaTUD/Explain_AI_Generated_Text |
| PyPI | https://pypi.org/project/xai-text-classifier/ |
| PAN@CLEF 2025 task | https://zenodo.org/records/14962653 |
| COLING 2025 dataset | https://huggingface.co/datasets/Jinyan1/COLING_2025_MGT_en |
| Ghostbuster data | https://github.com/vivek3141/ghostbuster-data |
| Doughman limitations (supporting) | https://aclanthology.org/2025.coling-main.288/ |
| Terčon linguistic survey (feature source) | https://arxiv.org/abs/2510.05136 |
| StyloAI (feature source) | https://arxiv.org/pdf/2405.10129 |

---

## 11. Bottom line for unslop

Pudasaini et al. is the **epistemic hygiene** paper for the detector refresh: it shows *why* a 97 F1 leaderboard entry can be measuring paragraph formatting on one corpus and POS entropy on another. For unslop, that means:

1. **Keep humanizing for voice and ESL defense** — not for guaranteed detector evasion.
2. **Report OOD numbers** whenever citing detection benchmarks.
3. **Treat burstiness and sentence variation as necessary, not sufficient** — they are in the detector feature set and they shift by domain.
4. **Cross-model paraphrase stays lever #1** — only intervention that rewrites the whole feature bundle.
5. **Never ship "detector score after unslop" as product proof** without domain-matched evaluation.

The paper is low integration priority for code (3/5 in UPDATE-PLAN) but **high priority for honesty** in docs, benchmarks, and anti-detector boundary language.
