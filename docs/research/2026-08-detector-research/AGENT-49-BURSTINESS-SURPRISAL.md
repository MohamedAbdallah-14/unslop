# AGENT-49 — Burstiness as Detection and Humanization Signal

**Topic:** Burstiness vs surprisal variance — academic literature beyond GPTZero marketing, mapped to `unslop/scripts/structural.py`  
**Date:** 2026-08-19  
**Scope:** Peer-reviewed / preprint sources, unslop implementation audit, evasion/defense implications

---

## Executive summary

"Burstiness" names **three different quantities** that the detector-marketing stack routinely conflates:

| Layer | What varies | Typical metric | Primary literature |
|-------|-------------|----------------|-------------------|
| **Syntactic burstiness** | Sentence length / structure | σ(word-count per sentence), CV, consecutive-sentence Δ | Desaire et al. 2023; Muñoz-Ortiz et al. 2024; Desaire feature #8 |
| **Token surprisal burstiness** | Per-token unpredictability under an LM | σ(−log p), Δsurprisal, Δ²surprisal | DivEye (Basani et al., TMLR 2026); GPT-who (Venkatraman, NAACL 2024) |
| **IR burstiness (original)** | Word re-appearance within documents | Poisson-mixture / negative-binomial over term counts | Church & Gale 1995 |

GPTZero popularized a **hybrid** definition: burstiness = variance of **sentence-level perplexity** across a document (see their 2023 blog/support pages). That is closer to DivEye's surprisal-dynamics family than to sentence-length σ, but GPTZero **deprecated perplexity+burstiness as primary scores in autumn 2023** and moved to a learned classifier; their current technical report is [arXiv:2602.13042](https://arxiv.org/abs/2602.13042).

**Academic consensus (2023–2026):** Human prose is **more variable** than LLM prose on both syntactic and token-surprisal axes. Mean sentence length alone is a weak discriminator; **variance** is not (Desaire et al.). Absolute perplexity is narrowing as models improve; **intra-document surprisal variance** survives paraphrase better (DivEye). Simple synonym paraphrase can **increase** detector TPR on modern zero-shot methods (+8–15% on RADAR/Fast-DetectGPT per Adversarial Paraphrasing, NeurIPS 2025) — structural restoration is not optional.

**unslop verdict:** `structural.py` targets **syntactic burstiness** (paragraph-level sentence-length σ) with thresholds aligned to practitioner measurements (~σ=4 AI vs ~σ=8 human). That is the correct cheap lever for post-hoc humanization but is **orthogonal** to DivEye's token-level signal. Full defense requires both: structural splits/merges **plus** lexical/surprisal variance (`surprisal.py`, anti-detector LLM mode). Deterministic structural pass alone cannot move Δ² surprisal entropy or Binoculars cross-perplexity.

---

## 1. Terminology — three "burstiness" families

### 1.1 Information retrieval (Church & Gale, 1995)

**Paper:** Church, K. W., & Gale, W. A. *Poisson mixtures.* Natural Language Engineering, 1(2), 163–190.  
**URLs:** [DOI 10.1017/s1351324900000139](https://doi.org/10.1017/s1351324900000139) · [Cambridge Core](https://www.cambridge.org/core/journals/natural-language-engineering/article/abs/poisson-mixtures/52E7F9429D0EC03EEC6674E071727B64)

Burstiness here means **word re-appearance**: once a term appears in a document, it is more likely to appear again (Poisson mixture / negative binomial over document-term counts). Katz's "burstiness" statistic conditions on documents where the word already occurred.

**Detector relevance:** Indirect. Modern AI detectors do not use IR burstiness directly, but the intuition — **heterogeneous local density** — carries forward to surprisal dynamics.

### 1.2 Syntactic / stylometric burstiness (sentence-length variance)

Operationalized as:
- Standard deviation of per-sentence word counts (within paragraph or document)
- Coefficient of variation: σ/μ (scale-invariant; used in `stylometry.py` as `sentence_length_cv`)
- Consecutive-sentence length delta (Desaire feature #9)
- Count of fragments (<11 words) and long sentences (>34 words) — Desaire features #10–11

**Key finding — Desaire et al. (2023):** In academic science writing, **average sentence length does not separate human vs ChatGPT**; **σ(sentence length) within a paragraph does** (feature #8 in their 20-feature XGBoost model, >99% accuracy in-domain).

**URLs:** [Cell Reports Physical Science / arXiv:2303.16352](https://doi.org/10.48550/arxiv.2303.16352) · [PMC10328544](https://pmc.ncbi.nlm.nih.gov/articles/PMC10328544/) · [DOI 10.1016/j.xcrp.2023.101426](https://doi.org/10.1016/j.xcrp.2023.101426)

**Supporting papers:**
- Muñoz-Ortiz et al., *Paraphrasing Attack Resilience…* — stddev of sentence length as RF feature: [arXiv HTML 2605.14240](https://arxiv.org/html/2605.14240v1)
- Feature extraction study (GPT narrow length distribution): [DOI 10.54364/aaiml.2025.52217](https://doi.org/10.54364/aaiml.2025.52217)
- EMNLP 2025 linguistic profiling (sentence length mean + variability): [ACL Anthology 2025.emnlp-main.1163](https://aclanthology.org/2025.emnlp-main.1163.pdf)
- Explainable detection failure analysis (Sentence Length Variation feature): [arXiv:2603.23146](https://arxiv.org/html/2603.23146v1)

**Practitioner anchor (unslop Cat 14):** r/WritingWithAI structural thesis cites ~**8.2 vs ~4.1** word-count σ for human vs GPT-4o — community measurement, not a peer-reviewed controlled study. Treat as field heuristic, not calibrated threshold. [Reddit thread](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/)

### 1.3 Token surprisal variance ("rhythmic unpredictability")

**Core claim:** Human text alternates predictable function-word spans with unpredictable content words; LLM text is **uniformly smooth** under a scoring LM — not necessarily lower mean perplexity, but **lower variance** in per-token surprisal and in its temporal derivatives.

**DivEye (Basani & Chen, TMLR 2026):** 10 interpretable features from per-token surprisal S(x_t): mean, std, var, skew, kurtosis; first-order ΔS mean/std; second-order Δ²S variance, entropy, autocorrelation. Second-order block is especially predictive. Robust to paraphrase; +33.2% vs zero-shot baselines; +18.7% as auxiliary booster.

**URLs:** [arXiv:2509.18880](https://arxiv.org/abs/2509.18880) · [HTML v3](https://arxiv.org/html/2509.18880v3) · [IBM/diveye](https://github.com/IBM/diveye) · [OpenReview DIG-BUG](https://openreview.net/forum?id=QuDDXJ47nq)

**GPT-who (Venkatraman et al., NAACL 2024 Findings):** UID-motivated surprisal-variance feature space; outperforms statistical baselines on Turing-Bench, GPABenchmark, ArguGPT, Deepfake-in-the-wild.

**URLs:** [ACL Anthology 2024.findings-naacl.8](https://aclanthology.org/2024.findings-naacl.8.pdf) · [arXiv:2310.06202](https://arxiv.org/abs/2310.06202)

**UID theoretical basis:**
- Jaeger & Levy — uniform information density: [EMNLP 2021 main.74](https://aclanthology.org/2021.emnlp-main.74.pdf)
- Meister et al. — locally typical sampling (entropy-targeted token choice): [arXiv:2202.00666](https://arxiv.org/abs/2202.00666)
- Entropy rate constancy re-evaluation: [Findings EMNLP 2023.1039](https://aclanthology.org/2023.findings-emnlp.1039.pdf)

**Important nuance:** UID predicts speakers **smooth** information globally; humans still show **local** peaks and troughs. Detectors exploit **failure to reproduce human-like surprisal swings**, not perfect uniformity.

---

## 2. GPTZero marketing vs academic stack

### What GPTZero originally claimed (2023)

From [GPTZero perplexity/burstiness explainer](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/) (archived framing):
- **Perplexity:** document/sentence predictability under a reference LM
- **Burstiness:** variance of perplexity **across sentences** (not sentence-length σ)

Support page threshold folklore: perplexity >85 "more likely human" — **not portable across models/domains**.

### What changed

Same pages state (autumn 2023): **GPTZero no longer uses perplexity/burstiness as primary detection**; migrated to deep learning. Current report: [GPTZero: Robust Detection of LLM-Generated Texts, arXiv:2602.13042](https://arxiv.org/abs/2602.13042) — cites Binoculars, Fast-DetectGPT, DivEye-class likelihood features, adversarial training.

### Academic evaluation of GPTZero-era metrics

- Chaka (2023) — five detectors including GPTZero perplexity/burstiness: [JALT 10.37074/jalt.2023.6.2.12](https://doi.org/10.37074/jalt.2023.6.2.12)
- Liang et al. — detectors conflate low perplexity with ESL/formal human writing: [arXiv:2304.02819](https://arxiv.org/abs/2304.02819) · [Patterns / PMC10382961](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/)
- Tarım & Onan — GPTZero perplexity+burstiness heuristics fail on diffusion LMs: [arXiv:2507.10475](https://arxiv.org/pdf/2507.10475)

**Takeaway:** Treat GPTZero's 2023 burstiness blog as **historical intuition**, not state-of-the-art methodology. Modern stack = multi-model likelihood (Binoculars [arXiv:2401.12070](https://arxiv.org/abs/2401.12070)), curvature (Fast-DetectGPT [arXiv:2310.05130](https://arxiv.org/abs/2310.05130)), surprisal dynamics (DivEye), embedding geometry (PHD [arXiv:2306.04723](https://arxiv.org/abs/2306.04723)).

---

## 3. Burstiness vs surprisal variance — relationship

```
Human-like rhythm
├── Syntactic layer (observable without LM)
│   ├── σ(sentence word count)     ← structural.py, validate.py
│   ├── sentence_length_cv (σ/μ)   ← stylometry.py proxy
│   └── parallel-bullet uniformity ← merge_bullet_soup
│
└── Token layer (needs scoring LM)
    ├── σ(surprisal)               ← surprisal.py / DivEye
    ├── σ(Δsurprisal)              ← first-order volatility
    └── var/entropy/autocorr(Δ²surprisal)  ← DivEye's paraphrase-resistant block
```

| Question | Syntactic burstiness | Surprisal variance |
|----------|---------------------|-------------------|
| **Measures** | Visible sentence shape | Model-internal token predictability swings |
| **Cheap offline?** | Yes (regex + word count) | Needs LM (`distilgpt2` min.) |
| **Survives synonym swap?** | Partially (structure unchanged) | Partially — DivEye designed for paraphrase resistance |
| **Broken by naive paraphrase?** | Can worsen (uniform rewrites) | Can worsen or improve depending on attack |
| **ESL false-positive overlap** | Formal ESL can be syntactically uniform | Low perplexity + low variance (Liang et al.) |
| **unslop module** | `structural.py`, `validate.py` | `surprisal.py`, `stylometry.py` proxies |

**Zipf bridge (unslop design note):** `word_length_stdev` proxy in `stylometry.py` — shorter words correlate with higher frequency / lower surprisal; document-level variance in mean word length per sentence approximates token-level variance without torch. Correlates with, ≠ DivEye.

**Generation-side origin (Cat 04):** Holtzman et al. (ICLR 2020) — humans oscillate high/low probability tokens; greedy LM decoding plateaus: [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). Meister typical sampling targets entropy-aligned token choice: [arXiv:2202.00666](https://arxiv.org/abs/2202.00666). Mirostat holds perplexity in human-preferred band: [arXiv:2007.14966](https://arxiv.org/abs/2007.14966). **Post-hoc humanizers cannot access these levers** on closed APIs — structural + lexical passes are the available fix.

---

## 4. Detection literature — burstiness-adjacent signals

### Zero-shot likelihood family (orthogonal to sentence σ)

| Method | Signal | URL |
|--------|--------|-----|
| DetectGPT | Probability curvature under perturbation | [arXiv:2301.11305](https://arxiv.org/abs/2301.11305) |
| Fast-DetectGPT | Conditional probability curvature (340× faster) | [arXiv:2310.05130](https://arxiv.org/abs/2310.05130) |
| Binoculars | perplexity / cross-perplexity ratio | [arXiv:2401.12070](https://arxiv.org/abs/2401.12070) |
| Ghostbuster | Multi weak-LM probability features | [NAACL 2024](https://aclanthology.org/2024.naacl-long.95/) |

### Paraphrase / evasion (why lexical-only humanization backfires)

| Paper | Finding | URL |
|-------|---------|-----|
| DIPPER (Krishna et al., NeurIPS 2023) | Controllable paraphrase crushes DetectGPT | [arXiv:2303.13408](https://arxiv.org/abs/2303.13408) |
| Adversarial Paraphrasing (Cheng et al., NeurIPS 2025) | **Simple** paraphrase **increases** TPR +8.57% RADAR, +15.03% Fast-DetectGPT; adversarial guidance −87.88% avg T@1%F | [arXiv:2506.07001](https://arxiv.org/abs/2506.07001) · [NeurIPS PDF](https://papers.nips.cc/paper_files/paper/2025/file/443f314cd420ce621b6e748fd1194ed8-Paper-Conference.pdf) |
| Sadasivan et al. | TV-distance impossibility as models improve | [arXiv:2303.11156](https://arxiv.org/abs/2303.11156) |
| Chakraborty et al. (ICML 2024 position) | Detection possible with enough text / separable support | [arXiv:2304.04736](https://arxiv.org/abs/2304.04736) |

**Structural implication:** Naive "humanizers" that homogenize sentence length while swapping vocabulary move **away** from human syntactic burstiness and may **toward** detector-sensitive smooth surprisal — the worst quadrant.

---

## 5. unslop `structural.py` — target audit

**File:** `unslop/scripts/structural.py`  
**Research basis (module docstring):** uniform sentence length = #1 statistical AI-detector signal; human σ ~8.2 vs GPT-4o ~4.1 (Cat 04/14); Adversarial Paraphrasing lexical-only regression.

### Pass 1: `split_long_sentences`

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| `min_words` | 30 | Overlong-sentence floor (non-flat paragraphs) |
| `flat_min_words` | 20 | When paragraph already flat, lower floor |
| `target_sigma` | **5.0** | Flat paragraph if σ < 5 (AI band ~4; human ~8) |
| `min_half` | 8 | Balance guard — both split halves ≥8 words |

**Flat-paragraph regime:** If paragraph has ≥2 sentences and `_paragraph_sigma < 5.0`, attempt splits on sentences ≥20 words at safe boundaries (`;`, `, however,`, `, but`, `, and then`, `, so`, `, while`, em-dash). Already-varied paragraphs (σ ≥ 5) are **left alone** — avoids destroying natural human rhythm.

**Risky connectors excluded:** `, which`, `, because`, `, if` — subordinate clauses that don't become independent sentences cleanly.

### Pass 2: `merge_bullet_soup`

Collapses ≥3 parallel short bullets (same first word, ≤10 words each, ≤40 total) into one comma-separated sentence. Targets **syntactic monotony** in list-heavy AI output (uniform bullet cadence reads as machine template).

### Validator alignment (`validate.py`)

| Metric | Definition | Threshold |
|--------|------------|-----------|
| `_burstiness()` | σ(sentence word counts), document-wide | Warning if σ < **4** on docs ≥8 sentences |
| `_count_flat_paragraphs()` | Per-paragraph σ with ≥3 sentences | Flat if σ < **3.0** |
| Benchmark `--strict` | Human-like fixtures must not lose burstiness | `benchmarks/run.py` |

**Note:** Validator uses document-wide σ; structural pass uses **per-paragraph** σ — correct design (flat paragraphs can hide in document-level averages).

### Stylometry / surprisal companions

| Module | Signal | Role |
|--------|--------|------|
| `stylometry.py` | `sentence_length_stdev`, `sentence_length_cv`, `word_length_stdev` | Voice-match targets; cheap DivEye proxies |
| `surprisal.py` | `surprisal_stdev`, Δ/Δ² features, `to_diveye_vector()` | Real DivEye-aligned reading (`--surprisal-variance`) |

### What structural.py does **not** fix

- Token-level surprisal variance (DivEye Δ² block)
- Binoculars cross-perplexity gap
- Probability curvature (DetectGPT / Fast-DetectGPT)
- Embedding intrinsic dimension (PHD)
- Contraction rate (Paneru 2026 — `soul.py` territory, [arXiv:2604.11687](https://arxiv.org/abs/2604.11687))

---

## 6. Humanization playbook (evidence-ordered)

1. **Restore syntactic variance first** — split/merge structural pass; anti-detector mode asks for ≥1 sentence <10 words per 100 words and σ ≥6 band (`skills/unslop/SKILL.md`).
2. **Widen token surprisal** — unpredictable but context-faithful word choices; cross-model second pass; avoid uniform synonym substitution.
3. **Preserve stance** — blandification lowers idiolect variance and **increases** detectability (Abdulhai blandification [arXiv:2603.18161](https://arxiv.org/abs/2603.18161); RLHF homogenization Rallapalli [arXiv:2604.14111](https://arxiv.org/abs/2604.14111)).
4. **Measure both layers** — benchmark σ before/after (`benchmarks/run.py`); optional `--surprisal-variance` for DivEye vector.
5. **Do not optimize GPTZero 2023 thresholds** — commercial detectors (Turnitin Aug 2025 bypasser model, GPTZero v4.1b) train on humanizer outputs; Chicago Booth 2026 is reference for edited-text accuracy.

---

## 7. Open questions / research gaps

1. **σ=5 threshold calibration** — unslop uses practitioner 8.2/4.1 gap; no large cross-genre published table for GPT-4o/Claude 4 at paragraph level. Desaire used paragraph-internal σ in chemistry abstracts only.
2. **Structural pass vs DivEye** — no published ablation measuring DivEye feature shift after deterministic sentence splitting only. Hypothesis: Δsurprisal std rises modestly; Δ² block needs lexical entropy.
3. **ESL equity** — widening variance helps false-positive victims (Liang intervention: "enhance word choices") but must not invent voice. unslop anti-detector mode is explicitly defensive.
4. **Diffusion LMs** — Tarım & Onan 2025: AR-trained perplexity/burstiness heuristics mislead on LLaDA outputs.
5. **Genre dependence** — Feature extraction paper: sentence-length mean **inverts** by domain (sociology humans longer). σ helps but needs domain-aware floors.

---

## 8. Bibliography (URLs)

### Foundational / terminology
- Church & Gale, Poisson mixtures (1995): https://doi.org/10.1017/s1351324900000139
- Holtzman et al., Neural Text Degeneration (ICLR 2020): https://arxiv.org/abs/1904.09751
- Meister et al., Locally Typical Sampling: https://arxiv.org/abs/2202.00666
- Jaeger & Levy, Revisiting UID (EMNLP 2021): https://aclanthology.org/2021.emnlp-main.74.pdf

### Syntactic burstiness / stylometry
- Desaire et al., ChatGPT vs scientist (2023): https://doi.org/10.48550/arxiv.2303.16352
- Muñoz-Ortiz et al., paraphrase resilience: https://arxiv.org/html/2605.14240v1
- EMNLP 2025 linguistic profiling: https://aclanthology.org/2025.emnlp-main.1163.pdf
- Explainable detection failures: https://arxiv.org/html/2603.23146v1
- Feature extraction GPT vs human lengths: https://doi.org/10.54364/aaiml.2025.52217
- Gotcha GPT (sentence σ): https://doi.org/10.1021/acs.jcim.4c01203

### Surprisal variance / UID detectors
- DivEye / Basani et al. (TMLR 2026): https://arxiv.org/abs/2509.18880
- IBM DivEye code: https://github.com/IBM/diveye
- GPT-who / Venkatraman (NAACL 2024): https://arxiv.org/abs/2310.06202
- Venkatraman thesis (UID authorship): https://pike.psu.edu/publications/thesis-saranya.pdf

### Zero-shot likelihood detectors
- DetectGPT: https://arxiv.org/abs/2301.11305
- Fast-DetectGPT: https://arxiv.org/abs/2310.05130
- Binoculars: https://arxiv.org/abs/2401.12070
- Ghostbuster: https://aclanthology.org/2024.naacl-long.95/

### Evasion / equity
- Adversarial Paraphrasing (NeurIPS 2025): https://arxiv.org/abs/2506.07001
- DIPPER: https://arxiv.org/abs/2303.13408
- Liang et al., ESL bias: https://arxiv.org/abs/2304.02819
- Sadasivan impossibility: https://arxiv.org/abs/2303.11156
- Chakraborty possibility: https://arxiv.org/abs/2304.04736

### GPTZero / commercial context
- GPTZero 2023 perplexity/burstiness (historical): https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- GPTZero technical report (2026): https://arxiv.org/abs/2602.13042
- Chaka, five detectors evaluation: https://doi.org/10.37074/jalt.2023.6.2.12

### Homogenization / humanization context
- Paneru, contraction gap (2026): https://arxiv.org/abs/2604.11687
- Rallapalli, RLHF stylistic clustering (2026): https://arxiv.org/abs/2604.14111
- Abdulhai, blandification RCT: https://arxiv.org/abs/2603.18161

### unslop implementation
- `unslop/scripts/structural.py` — split/merge passes
- `unslop/scripts/validate.py` — `_burstiness`, flat-paragraph counter
- `unslop/scripts/stylometry.py` — `sentence_length_cv`, proxies
- `unslop/scripts/surprisal.py` — DivEye vector
- `docs/research/IMPLEMENTATION_TRACE.md` — research→code map
- `docs/research/04-natural-language-quality/A-academic.md` — decoding + detection synthesis

---

## 9. One-paragraph unslop maintainer summary

Burstiness in the **academic** sense is not one number — sentence-length σ (Desaire), token surprisal σ (DivEye/GPT-who), and GPTZero's deprecated sentence-perplexity variance are related but non-substitutable. unslop's `structural.py` correctly attacks the **cheapest robust layer**: flat paragraph rhythm (σ < 5 → split at 20–30 words; bullet-soup merge). That aligns with Desaire feature #8 and practitioner GPT-4o σ~4 measurements, and avoids the Adversarial Paraphrasing trap where lexical-only edits **help** detectors. It does **not** satisfy DivEye's Δ² surprisal block or Binoculars — those need `surprisal.py`, contraction/soul passes, and anti-detector LLM guidance. Treat σ≥6 as a voice-match **band**, not a detector-evasion guarantee. Calibrate against both `benchmarks/run.py` burstiness columns and optional `--surprisal-variance` before claiming paraphrase resistance.
