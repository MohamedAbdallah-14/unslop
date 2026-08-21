# Agent #13 — GPTZero v6 + Lexical Predictability Cones

**Topic:** January 2026 "v6" classifier generation, the lexical predictability cones mechanism (practitioner + official mapping), benchmarks, product blogs, user reviews, evasion, unslop integration  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh  
**Cross-refs:** Agent #57 (GPTZero product evolution broadly), Agent #60 (Pangram vs GPTZero on paraphrase), Agent #49 (burstiness/surprisal), Agent #55 (surprisal dynamics)

---

## Executive summary

**"GPTZero v6 + predictability cones" is practitioner nomenclature, not GPTZero's official product name.** GPTZero versions models as param-scaled tags (`3.7b`, `4.3b`, `4.8b`) and dated API bases (`2025-12-18-base`). The "v6" label and **lexical predictability cones** term appear almost exclusively in third-party evasion literature — chiefly [HumanizeMy.ai](https://humanizemy.ai/bypass-gptzero) — starting January 2026. GPTZero's own materials describe the same *function* (context-conditional token predictability, paraphrase resistance, multi-model likelihood features) without using "cones" or "v6."

**Mechanism (reconstructed):** For each token, estimate how predictable the chosen word is given a local context window, aggregated across multiple foundation-model token distributions. LLM output clusters in a **narrow band** of high-probability choices (practitioners call this a tight "cone"); human writing shows **wider variance** in conditional probability across the document. Document-level narrowness — many consecutive tokens sitting in the top-probability slice — flags AI even when legacy perplexity and burstiness UI metrics look human. Synonym swaps fail because substitutes drawn from the same semantic neighborhood occupy the same probability band.

**January 2026 anchor events:** Chicago Booth rebuttal blog ([gptzero.me/news/chicago-booth-2026/](https://gptzero.me/news/chicago-booth-2026/)) re-running Jabarian & Imas on `predicted_class` with model `2025-12-18-base`; February 2026 technical report ([arXiv:2602.13042](https://arxiv.org/abs/2602.13042)) formalizing adversarial training against DIPPER/TempParaphraser; quarterly benchmarking page updated with Model **4.3b** bypasser recall **91.8%**.

**Benchmark tension:** GPTZero self-reports 99.5%+ accuracy on clean paired corpora; independent essay tests land **82–89%** with **14–50%** false-positive rates on ESL/technical prose; paraphrase evasion drops vendor bypass recall to **~68–92%** depending on humanizer tier and model version. The cones signal specifically raises the bar on **T1 synonym-swap** evasion but does not close the gap on **T2–T3 structural/cross-model** humanization.

**unslop verdict:** Lexical predictability cones are the commercial formalization of what DivEye/surprisal-variance research already measured academically — intra-document predictability flatness. unslop's deterministic passes (stock-vocab deletion, contraction injection) are **necessary but insufficient** against 2026 GPTZero. `structural.py` burstiness + `--surprisal-variance` + cross-model second pass align with the evasion literature's "break the cone" prescription. Do not claim anti-detector mode reliably passes GPTZero; frame as ESL false-positive defense. Log `predicted_class` and model version in any benchmark run.

---

## 1. Nomenclature: what "v6" actually maps to

GPTZero does **not** publish a "v6" changelog. Practitioner mapping (from Agent #57, cross-validated here):

| Shorthand | Approx. period | Official signals | Relevance to cones |
|-----------|---------------|------------------|-------------------|
| v1–v2 | Jan–autumn 2023 | Perplexity + burstiness statistical layer | Historical — retired as classifier inputs |
| v3 | Late 2023 | Ternary Human / AI / Mixed taxonomy | UI still shows perplexity/burstiness as explainability |
| v4 | 2024 | Deep-learning supervised classifier | Likelihood features absorbed into neural model |
| v5 | Mid–late 2025 | Model **3.7b** (Aug 2025), **3.15b** humanizer red-team | GPT-5 zero-shot generalization; 93.5% bypass recall published |
| **v6** | Jan 2026+ | **4.x** series, `2025-12-18-base`, **4.3b**, **4.8b** | Industry "predictability cones" label; paratext masking in 4.8b |

**Critical distinction:** Perplexity and burstiness were **explicitly retired as classifier inputs in autumn 2023** ([support article](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity), [how-ai-detectors-work](https://gptzero.me/news/how-ai-detectors-work/)). Third-party "v6 adds a third signal alongside perplexity and burstiness" descriptions are **conceptually accurate for users reading the dashboard** (those metrics still appear in UI) but **technically wrong about the classifier stack** — the deep-learning model subsumed statistical signals years earlier. "Cones" describe a *refined predictability feature* in the 2026 generation, not a literal third logit fed beside two 2023-era scalars.

For reproducible evals, log the API **model version string** (e.g. `2025-12-18-base`, `4.3b`), not "v6."

---

## 2. Lexical predictability cones — mechanism

### 2.1 Practitioner definition (primary source for the term)

[HumanizeMy.ai bypass guide](https://humanizemy.ai/bypass-gptzero) (Jan 2026, updated May 2026):

> GPTZero v6 now models how predictable each word is given the surrounding context, **weighted across multiple foundation-model token distributions**. The output is a cone-shaped confidence band: if the document's words sit too narrowly inside the highest-probability range for too many tokens in sequence, the classifier flags it — even if perplexity and burstiness look human. **Synonym substitution cannot perturb this signal** because the substitutes themselves are pulled from the same predictability range.

[HumanizeMy.ai accuracy review](https://humanizemy.ai/blog/is-gptzero-accurate):

> For each word in the input text, GPTZero estimates the conditional probability of that word given a small surrounding window. A typical human writer's choices fall inside a **wide probability cone**. LLM output tends to fall inside a **narrow cone**. v6 measures the **variance of this cone width** and uses it as the third input.

**Note:** HumanizeMy.ai claims GPTZero "published a v6 architecture note" in January 2026. **No such document was found on gptzero.me** as of this research pass. The claim may conflate the Chicago Booth rebuttal, the Feb 2026 arXiv report, or internal/partner docs. Treat the cones *mechanism* as well-sourced industry reconstruction; treat the "published architecture note" citation as **unverified**.

### 2.2 Official GPTZero mapping (same function, different vocabulary)

GPTZero never uses "cone" in product copy. Closest official descriptions:

| Source | Mechanism language |
|--------|-------------------|
| [Perplexity & burstiness (historical)](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/) | "Perplexities per sentence as a measure of how likely an AI model would have chosen the exact same set of words" — retired as classifier input, retained as explainability |
| [How AI detectors work](https://gptzero.me/news/how-ai-detectors-work/) | "Seven-layered model" beyond perplexity/burstiness; deep-learning architecture since autumn 2023 |
| [arXiv:2602.13042 §2 Related Work](https://arxiv.org/abs/2602.13042) | Cites likelihood-based features, surprisal (GPT-who), cross-perplexity (Binoculars), curvature (Fast-DetectGPT) — positions GPTZero as trained detector absorbing these signals |
| [Humanizer robustness post](https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/) | "Deeper semantic and structural signals **beyond surface form**"; explicit AI-paraphrased subclass |
| [Deep Scan (arXiv §4)](https://arxiv.org/abs/2602.13042) | Saliency + occlusion adapted to **synonym-replacement edit behavior** — directly targets the evasion pattern cones are meant to catch |
| [Meaningful AI Detection / 4.8b](https://gptzero.me/news/meaningful-ai-text-detection/) | Header/paratext masking — removes bypass vector where surface formatting manipulated scores |

### 2.3 Conceptual model (synthesis)

```
For each token t_i in document D:
  1. Compute P_M(t_i | context window) for M ∈ {frontier LMs used internally}
  2. Rank t_i's realized probability against the top-k alternatives
  3. Measure local "cone width" = spread of acceptable probabilities / rank of chosen token
  4. Aggregate across document → document-level predictability variance σ_cone

Human:  high σ_cone (mix of obvious and surprising word choices)
AI:     low σ_cone  (long runs of top-1/top-2 probability picks)
Paraphrase-swap: preserves semantic neighborhood → substitutes stay in same cone → still low σ_cone
Structural rewrite: changes syntax + word-choice distribution → widens σ_cone
```

**Relationship to academic detectors:**

| Method | Overlap with "cones" |
|--------|---------------------|
| **Perplexity (GPTZero 2023)** | Single-model, document-level predictability — subset of cone width |
| **Burstiness** | Variance of perplexity across sentences — related to σ_cone but sentence-granular |
| **Binoculars (Hans et al. 2024)** | Cross-perplexity between two LMs — dual-model cone check |
| **DivEye (Ganapathi et al. 2025/26)** | Intra-document **surprisal variance** — closest academic analog; unslop implements via `surprisal.py` |
| **Fast-DetectGPT** | Curvature of log-prob under perturbation — perturbation-based cone probe |
| **GPTZero deep classifier** | Learned features + adversarial training on paraphrased corpus; cones likely one engineered or learned channel |

**"Cone" is not the LLM interpretability literature's activation-space concept cones** (e.g. Wollschläger et al. 2025). It is a **token-level conditional-probability band** metaphor from evasion vendors.

---

## 3. January 2026 product / research update

Events tied to the "v6" generation (not a single launch day):

| Date | Release | Cones relevance |
|------|---------|-----------------|
| **Aug 2025** | Model **3.7b** — training-data overhaul for GPT-4.1, o3, Gemini 2.5, Claude Sonnet 4; 95%+ GPT-5 recall without GPT-5 training data | Practitioner lit ties cones to 3.7b backbone |
| **2025 (undated)** | Model **3.15b** — humanizer red-team; 93.5% recall on 12+ bypasser corpus | Pre-cones paraphrase baseline |
| **Dec 18, 2025** | API base `2025-12-18-base` | Chicago Booth rebuttal model |
| **Jan 2026** | [Chicago Booth rebuttal](https://gptzero.me/news/chicago-booth-2026/) | 99.3% recall / 0.05% FPR on corrected API fields — defines "v6 era" benchmark posture |
| **Jan 2026 (3rd party)** | HumanizeMy.ai publishes cones explanation | Origin of "v6 + cones" meme in evasion ecosystem |
| **Feb 5, 2026** | [Quarterly benchmarking page](https://gptzero.me/news/gptzero-ai-detection-benchmarking-the-industry-standard-in-accuracy-transparency-and-fairness/) | Model **4.3b** metrics; bypasser table |
| **Feb 13, 2026** | [arXiv:2602.13042](https://arxiv.org/abs/2602.13042) technical report | Hierarchical classifier, red-team pipeline, 93.5% bypass recall (4.1b) |
| **Aug 1, 2026** | Model **4.8b** — Meaningful AI Detection (header masking) | Closes paratext bypass; orthogonal to cones but same generation |

---

## 4. Benchmarks

### 4.1 GPTZero self-reported (clean paired text)

**Chicago Booth re-run** ([Jan 2026 post](https://gptzero.me/news/chicago-booth-2026/), model `2025-12-18-base`, 1,992 passages):

| Detector | FPR | Recall | Accuracy |
|----------|-----|--------|----------|
| GPTZero | **0.05%** | **99.3%** | **99.5%** |
| Pangram | 0.05% | 98.9% | 99.1% |
| Originality | 0.11% | 81.3% | 85.0% |

**Quarterly benchmark average** (Model **4.3b**, 4 domains, frontier LLMs GPT-5.2 / Gemini 3 Pro / Claude Sonnet 4.5 / Grok 4 Fast):

| Metric | GPTZero (4.3b) |
|--------|----------------|
| FPR | 0.08% |
| Recall | 99.60% |
| Precision | 99.93% |
| Accuracy | **99.76%** |

Per-domain highlights (4.3b): essays **100%** recall; product reviews **99.0%**; creative writing **99.6%**; paper reviews **99.8%**.

**Multilingual** (Model 3.7m, 24 languages): 97.62% recall, 0.09% FPR, 98.79% accuracy.

### 4.2 Bypasser / paraphrase benchmarks (cones stress test)

| Source | Model | Setting | GPTZero recall | Notes |
|--------|-------|---------|----------------|-------|
| GPTZero humanizer post | 3.15b | 1,000 texts, 12+ bypassers | **93.5%** | vs Pangram 50.2%, Originality 57.3% |
| arXiv:2602.13042 §5.3 | 4.1b | Same bypasser corpus | **93.5%** | Pangram 49.7% |
| Quarterly bench Table 7 | **4.3b** | 1,000 bypasser-modified texts | **91.80%** | Pangram 68.11%; QuillBot detector 11.80% |
| DAMAGE (Masrour et al., COLING 2025) | Pre-2025 GPTZero | 19 humanizers, academic essays | **60.04%** TPR @ 5% FPR | Legacy model; −39.7 pp vs raw |
| Chicago Booth (StealthGPT arm) | 2025 API | Genre-matched corpus | FNR **~50%+** on humanized | Pangram held; GPTZero disputed field choice, not this arm |
| HumanizeMy.ai May 2026 | v6 (claimed) | Corpus-trained humanization | **4%** AI score | Vendor evasion product; not independent |
| ToolChase / Ryne AI (cited) | 2026 | QuillBot one-pass paraphrase | **40–43%** hit rate | Down from ~90% on raw |
| WriteHumanly May 2026 | Current | 100 essays | **89%** overall accuracy | 14% human FP; 92% raw AI catch |
| Fast.io / RAID-adjacent | 2026 | Humanized text | **~68%** | vs Originality 96.7% on same bench (vendor dispute likely) |

**Reading the table:** Cones-era GPTZero (**91.8–93.5%** on vendor bypasser sets) materially beats Pangram/Originality on GPTZero's own hardest internal corpus — but **independent humanizer tests still show 30–40%+ escape rates** on commercial tools. The cones signal closes the **synonym-swap gap** more than the **StealthRL / cross-model / corpus-trained** gap.

### 4.3 False positives (cones cut both ways)

Formal, low-variance **human** prose mimics narrow cones:

| Study | Human FP rate | Population |
|-------|---------------|------------|
| GPTZero vendor | <1% | Internal paired benchmarks |
| WriteHumanly 2026 | **14%** overall; **40–50%** ESL/technical | 50 verified human essays |
| Liang et al. 2023 | **>50%** TOEFL essays (early GPTZero) | ESL — pre-debiasing |
| Chicago Booth Review | Degrades <50 words | All commercial detectors |
| MediaFast Reddit analysis | **28–45%** on edited human (disputed) | Short-form / structured prose |

**Implication for unslop:** Anti-detector mode's structural entropy shifts can **help ESL false-positive defense** (widen cones on human text) but also **help evasion** on actual AI text. The ethical framing in SKILL.md (ESL defense, not misconduct) is load-bearing.

---

## 5. Product blog posts (cones-relevant)

| Post | URL | Takeaway |
|------|-----|----------|
| Chicago Booth 2026 rebuttal | https://gptzero.me/news/chicago-booth-2026/ | Use `predicted_class` / `class_probabilities`, not `average_generated_prob` |
| Benchmarking philosophy | https://gptzero.me/news/gptzero-ai-detection-benchmarking-the-industry-standard-in-accuracy-transparency-and-fairness/ | Version discipline; bypasser Table 7 = 91.8% (4.3b) |
| Humanizer robustness | https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/ | 93.5% on paraphrased; trains on DIPPER, TempParaphraser |
| GPT-5 / Model 3.7b | https://gptzero.me/news/gpt5/ | Zero-shot frontier generalization |
| Meaningful AI Detection | https://gptzero.me/news/meaningful-ai-text-detection/ | 4.8b header masking — paratext bypass closed |
| How AI detectors work | https://gptzero.me/news/how-ai-detectors-work/ | Autumn 2023 DL pivot; perplexity/burstiness = explainability only |
| Technology page | https://gptzero.me/technology | Trinary classification; Deep Scan; high-confidence <1% error rate claim |
| arXiv:2602.13042 | https://arxiv.org/abs/2602.13042 | Authoritative architecture + red-team spec |

---

## 6. User reviews and sentiment (2026)

**Supporters:**
- Educators cite lowest FP among peers on long-form English ([Gold Penguin review](https://goldpenguin.org/blog/gptzero-review/), vendor-aligned)
- Sentence-level highlighting + Mixed/Polished/Paraphrased taxonomy valued for academic integrity workflows
- False-positive appeals path and FERPA positioning reduce institutional risk

**Critics:**
- Reddit threads ([MediaFast synthesis](https://www.mediafa.st/reddit-ai-detection-tools-explained)): routine false flags on concise, structured human posts; "the more precise your writing, the more likely GPTZero flags it"
- [WriteHumanly 100-essay test](https://www.write-humanly.com/blog/how-accurate-is-gptzero): 89% vs 99% marketed; STEM/ESL categories 30–50% FP
- [ToolChase](https://toolchase.com/blog/gptzero-review-accuracy-test/): QuillBot paraphrase drops GPTZero to coin-flip; humanizers to 6–25% AI scores
- Paraphrase skepticism: users report passing after Undetectable AI / QuillBot Humanizer despite cones marketing

**Consensus for unslop users:** GPTZero is the **most-deployed education detector** and **strongest on raw AI + light paraphrase** in vendor benchmarks — but **not deterministic** on humanized text, **not fair** to formal ESL/technical human prose without secondary evidence, and **not a single score** (`Mixed` vs `AI Paraphrased` matters).

---

## 7. Evasion landscape vs predictability cones

### 7.1 What cones catch (T0–T1)

| Technique | vs cones | Evidence |
|-----------|----------|----------|
| Stock-vocab deletion ("delve", "tapestry") | **Partial** | Removes AI-ism markers; doesn't widen token probability bands |
| Synonym swap (QuillBot paraphrase, thesaurus) | **Designed failure** | HumanizeMy.ai + GPTZero red-team narrative; QuillBot's own detector self-fails at 95% AI |
| Adverb injection / light polish | **Partial** | Adds tokens without restructuring probability profile |
| Perplexity spoofing (rare word insertion) | **Mixed** | Can raise perplexity UI metric while cone width stays narrow if inserts are still LM-predictable |

### 7.2 What cones miss or weakly resist (T2–T3)

| Technique | vs cones | Evidence |
|-----------|----------|----------|
| **DIPPER / TempParaphraser** | **Contested** | In GPTZero training data (arXiv §3.4.2); 93.5% recall suggests partial resistance, not immunity |
| **Cross-model rewrite** (Claude→GPT) | **Stronger evasion** | Different LM fingerprint; unslop SKILL.md step 6 |
| **Corpus-trained humanization** | **Strongest evasion** | HumanizeMy.ai 4% on GPTZero v6; structural sampling from human essays |
| **StealthGPT / commercial humanizers** | **Strong evasion** | Booth FNR ~50%+; DAMAGE 60% TPR on legacy GPTZero |
| **RL humanizers (StealthRL-class)** | **Strong evasion** | Not in GPTZero public tables; research frontier |
| **Header/paratext manipulation** | **Mitigated in 4.8b** | Meaningful AI Detection gray-mask |
| **Writing Replay / Authorship** | **Out of classifier scope** | Process provenance beats post-hoc cone evasion |

### 7.3 Evasion playbook (defensive framing — ESL FP relief)

Literature-consistent order for **legitimate** false-positive reduction:

1. **Structural entropy** — sentence-length σ ≥ 6, mixed syntax (matches unslop `structural.py` + anti-detector step 1)
2. **Surprisal variance** — local unpredictable lexical choices in glue vs content spans (DivEye; `--surprisal-variance`)
3. **Contractions + fragments** — register shift (Paneru 2026; anti-detector steps 3–5)
4. **User-specific anchors** — names, numbers, dates detectors can't pattern-match (step 4)
5. **Cross-model second pass** — breaks single-model cone alignment (step 6)

**Do not promise** steps 1–4 reliably evade GPTZero on AI-origin text. They **do** help human text that reads "too smooth."

---

## 8. unslop integration

### 8.1 Current stack vs cones

| unslop component | Cones interaction | Gap |
|------------------|-------------------|-----|
| `humanize.py` lexical passes | Removes high-probability AI stock vocab | Insufficient alone — cones read full distribution |
| `structural.py` | Sentence-length CV / split-merge | **Primary cone-widening lever** — directly targets flat rhythm |
| `soul.py` contractions | Register shift | Moderate — changes local token probabilities |
| `surprisal.py` / DivEye | Measures σ_surprisal on local LM | **Closest open-source analog to cones**; not in default loop |
| `stylometry.py` proxies | `sentence_length_cv`, `word_length_stdev` | Cheap cone-variance proxies |
| `detector.py` (TMR) | Feedback loop target | TMR ≠ GPTZero; GPTZero-family signal, not API parity |
| anti-detector SKILL.md | 7-step procedure | Aligns with cone-breaking literature; missing explicit "cone" vocabulary |

### 8.2 Recommended actions

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | Document cones in anti-detector landscape (SKILL.md / help) | Users hit GPTZero v6 in education; explain why synonym swap fails |
| **P1** | Add optional GPTZero API backend to `detector.py` or benchmark harness | Version-pin `predicted_class`; log Mixed/Polished/Paraphrased |
| **P1** | Benchmark unslop outputs vs GPTZero `4.3b`+ with dual reporting (TMR + GPTZero) | Agent #60 pattern — never single-detector claims |
| **P2** | Wire `--surprisal-variance` into anti-detector feedback loop | Optimize σ_surprisal, not just TMR score |
| **P2** | Extend `structural.py` metrics in benchmark CSV | Sentence-length σ is measurable cone proxy |
| **P3** | Track GPTZero API changelog / Superhuman Go integration | Detection embedded in Grammarly/Superhuman stack post-acquisition (Agent #57) |

### 8.3 What unslop should NOT do

- Claim deterministic GPTZero pass after deterministic unslop alone
- Optimize to perplexity/burstiness UI numbers (retired classifier inputs; cosmetic)
- Treat anti-detector as academic evasion tooling
- Cite HumanizeMy.ai 4% without "vendor evasion product" disclaimer
- Use "v6" in user-facing docs without mapping to official model tags

### 8.4 SKILL.md alignment check

Current anti-detector procedure ([skills/unslop/SKILL.md](../../skills/unslop/SKILL.md)) already prescribes burstiness σ ≥ 6, structural variation, contractions, specificity, rough edges, and cross-model second pass — **consistent with cone-breaking**. Missing explicit callout:

> Detectors in 2026 (GPTZero generation) measure **intra-document lexical predictability variance** across multiple LMs — not just vocabulary hits. Synonym swap without structural rewrite preserves the narrow predictability band.

Suggested one-line addition under anti-detector landscape (future PR, not in scope for this memo).

---

## 9. Primary source URL table

| Resource | URL |
|----------|-----|
| GPTZero technical report | https://arxiv.org/abs/2602.13042 |
| Chicago Booth rebuttal (Jan 2026) | https://gptzero.me/news/chicago-booth-2026/ |
| Quarterly benchmarking (4.3b) | https://gptzero.me/news/gptzero-ai-detection-benchmarking-the-industry-standard-in-accuracy-transparency-and-fairness/ |
| Humanizer robustness (3.15b) | https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/ |
| Model 3.7b / GPT-5 | https://gptzero.me/news/gpt5/ |
| Meaningful AI Detection (4.8b) | https://gptzero.me/news/meaningful-ai-text-detection/ |
| How AI detectors work | https://gptzero.me/news/how-ai-detectors-work/ |
| Perplexity/burstiness (historical) | https://gptzero.me/news/perplexity-and-burstiness-what-is-it/ |
| API interpretation | https://support.gptzero.me/articles/8947054519-how-do-i-use-and-interpret-the-results-from-your-api |
| Technology page | https://gptzero.me/technology |
| Chicago Booth working paper | https://doi.org/10.3386/w34223 |
| Liang ESL FP study | https://arxiv.org/abs/2304.02819 |
| DivEye (surprisal variance) | arXiv 2509.18880 / TMLR 2026 |
| HumanizeMy.ai cones guide (3rd party) | https://humanizemy.ai/bypass-gptzero |
| HumanizeMy.ai accuracy (3rd party) | https://humanizemy.ai/blog/is-gptzero-accurate |
| DAMAGE paraphrase audit | https://arxiv.org/abs/2501.03437 |

---

## 10. Bottom line

**Lexical predictability cones** name what GPTZero's 2026 classifier generation does in plain language: penalize documents where token choices sit too long in the highest-probability slice of multiple LM conditional distributions. GPTZero won't call it that; the arXiv paper calls it deep learning + adversarial red-teaming; evasion vendors call it cones; DivEye calls it surprisal variance.

For unslop: the actionable shift from pre-2026 advice is **structural over lexical**. Cones explain why `structural.py` and cross-model rewrite matter more than stock-vocab deletion for GPTZero-class detectors — and why neither unslop nor any rewriter should claim reliable pass. Process verification (Replay, Authorship) is the institutional counter-move; cones are the classifier counter-move to synonym cosplay.

**Agent #57 covers the full GPTZero arc.** This memo owns the **v6/cones mechanism, evasion physics, and unslop mapping** only.
