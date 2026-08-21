# Agent #59 — Copyleaks V9 Ensemble AI Detection

**Topic:** Copyleaks AI Detector V9 (July 2025) — three-investigator ensemble, AI Logic, independent benchmarks, humanizer evasion  
**Prepared:** August 19, 2026  
**Scope:** Production V9 release, research paper (arXiv:2503.01659), V10 successor metrics, third-party audits, supporters/critics, unslop threat-model audit  
**Status:** complete

---

## Executive summary

Copyleaks is a **commercial ensemble detector** sold as plagiarism + AI + code integrity in one LMS/API bundle. **V9 shipped July 8, 2025** (upgrade from v8.1), bundled with **AI Logic** (explainable flags: AI Phrases + AI Source Match). Copyleaks has since published **V10** internal benchmarks (test date October 16, 2025); production auto-updates, so August 2026 customers likely run V10-class weights even when literature says "V9."

The **only peer-reviewed public description of Copyleaks' "three investigators" ensemble** is the March 2025 paper *Detecting Stylistic Fingerprints of Large Language Models* (Bitton, Bitton, Nisan; Copyleaks). That work is **4-class LLM-family attribution** (Claude / Gemini / Llama / OpenAI), not a published binary human-vs-AI spec. Three diverse classifiers; **unanimous voting** yields precision **0.9988** and macro FPR **0.0004** on 200K held-out texts, at the cost of **1.06% "no-agreement" abstentions**. Marketing maps this to production "three investigators," but Copyleaks does **not** open-source V9/V10 binary fusion weights or name the three architectures.

**Independent reality check (2025–2026):** Vendor claims ~99%+ / 0.03–0.6% FP. Independent mixed-content tests land **77–96% overall**; Chicago Booth–adjacent comparisons cite **90.7% accuracy, 5.26% FPR, 86.9% recall** vs GPTZero's 99.5% / 0.05% / 99.3%. Copyleaks often **wins on paraphrased/humanized text among the Big Four** (71% recall post-humanization in one DeepSeek study vs GPTZero ~52%), but absolute post-humanization recall is still **40–71%**, and controlled reviews report **0% AI on fully humanized samples**. Perkins et al. (2024) found paraphrase drops detector accuracy ~21 pp across tools; Copyleaks was "most accurate" in that cohort but still **not integrity-grade**.

**Unslop verdict:** Copyleaks V9 ensemble is a **real multi-signal commercial detector** — frequency-ratio phrase stats, POS/syllable/hyphen stylometry, mixed-content segmentation, manipulation checks, optional retrieval (AI Source Match). It is **stronger than single-perplexity tools** and **better on edited AI than GPTZero in some paraphrase studies**, but **weaker than GPTZero/Pangram on clean English recall** and **not robust against T2–T3 adversaries** (cross-model paraphrase, RL humanizers, StealthRL-class policies). unslop should treat Copyleaks as a **screening signal**, cite the **three-signal gap** (perplexity + burstiness + stylometric fingerprint), and **never** imply deterministic unslop passes Copyleaks reliably — while keeping anti-detector framed as **ESL false-positive defense**, not academic evasion.

---

## 1. Product identity

| Field | Value |
|-------|-------|
| **Vendor** | Copyleaks Ltd. (founded 2015; plagiarism-first, AI detection added post-ChatGPT) |
| **Core SKU** | AI Detector + plagiarism + code plagiarism + AI Logic explanations |
| **V9 release** | **July 8, 2025** — upgrade from v8.1; customers told to expect score shifts vs pre-change scans |
| **V9 companion features** | AI Logic web/API (July 2025); AI Source Match (LMS rollout from **August 1, 2025**) |
| **Successor** | **V10** — internal test October 16, 2025; methodology published November 12, 2025 |
| **Deployment** | Auto-updated SaaS; API + Canvas, D2L, Moodle, Blackboard, Schoology, Edsby, Sakai |
| **Min scan length** | 350 chars (extension) / 255 chars (web); QA tests use ≥350 chars |
| **Languages** | 30+ (English highest; Japanese added April 2025 per repo research notes) |
| **Pricing (2026)** | Personal ~$13.99/mo annual; Pro ~$74.99/mo; Enterprise custom; API separate |
| **Security** | GDPR; SOC 2 / SOC 3 (per FAQ PDF) |

**Version timeline (public):**

| Version | Date | Notes |
|---------|------|-------|
| V5 | July 2024 | Indonesian language; model-family detection list expanded |
| V7.1 | ~2024–2025 | Three **sensitivity levels** (Extra Safe / Balanced / Extra Sensitive) |
| V8.1 | Pre–Jul 2025 | Last gen before V9 |
| **V9** | **Jul 8, 2025** | Ensemble refresh + AI Logic stack |
| V10 | Oct 16, 2025 test | TPR 0.988 / TNR 0.999 on 500K-text DS eval; sensitivity table updated |

**Primary URLs:**

- Product: https://copyleaks.com/ai-detector  
- API: https://copyleaks.com/api/ai-detector  
- API docs: https://docs.copyleaks.com/  
- AI Logic launch: https://copyleaks.com/blog/ai-logic-has-landed  
- V10 methodology: https://copyleaks.com/ai-detector/testing-methodology  
- Help — how detection works: https://help.copyleaks.com/s/article/HowdoesCopyleaksAIDetectionwork681cc74da8fd1  
- FAQ PDF (June 2025): https://copyleaks.com/wp-content/uploads/2023/05/ai-content-detector-faqs.pdf  

**V9 campus confirmation (independent of vendor marketing):**

- University of Illinois Springfield COLRS announcement, July 10, 2025: https://www.uis.edu/news/center-online-learning-research-service/faculty-orbit-campus-announcement-staff/copyleaks-update-ai-workshop  

---

## 2. Architecture — what "V9 ensemble" actually means

Copyleaks uses **ensemble** at two levels. Public docs blur them; keep them separate.

### 2.1 Research ensemble — "three investigators" (published)

**Paper:** *Detecting Stylistic Fingerprints of Large Language Models*  
**Authors:** Yehonatan Bitton, Elad Bitton, Shai Nisan (Copyleaks)  
**Posted:** March 2025  

| Resource | URL |
|----------|-----|
| arXiv abstract | https://arxiv.org/abs/2503.01659 |
| arXiv PDF | https://arxiv.org/pdf/2503.01659 |
| DOI | https://doi.org/10.48550/arxiv.2503.01659 |
| Copyleaks PDF | https://copyleaks.com/wp-content/uploads/2025/03/Detecting_Stylistic_Fingerprints_of_Large_Language_Models.pdf |
| Blog (non-technical) | https://copyleaks.com/blog/copyleaks-research-reveals-which-ai-wrote-what |

**Task:** Multiclass **LLM-family attribution** — Claude, Gemini, Llama, OpenAI (not binary human/AI).

**Ensemble design:**

| Design choice | Detail |
|---------------|--------|
| **Count** | 3 classifiers |
| **Diversity** | Different architectures + different random training subsets per family |
| **Training** | Balanced English texts from 4 LLM families |
| **Fusion — majority vote** | Macro Fβ(0.5) = **0.9946**, macro FPR = **0.0018** |
| **Fusion — unanimous vote** | Macro Fβ(0.5) = **0.9988**, macro FPR = **0.0004**; **1.06%** abstain ("no-agreement") |
| **Test set** | 200,000 texts (50K per family) |
| **Cost-sensitive rationale** | False attribution cost >> missed attribution; unanimous vote minimizes FP |

**Individual classifier macro FPR (paper Table 6):** Classifier I 0.0052 → II 0.0022 → III 0.0078. Classifier II is strongest single model; ensemble unanimous beats II FPR by ~5×.

**Unseen-model experiment (Section 3):** On phi-4 and Grok-1, **99.3–100% no-agreement** — ensemble refuses to map novel fingerprints to trained families. DeepSeek-R1 **74.2% classified as OpenAI** (stylistic affinity claim). Mixtral: 65% abstain, 26% OpenAI, 8.8% Llama.

**Critical reading:** This is **model provenance**, not proof that V9 binary detection uses identical unanimous triple-classifier fusion. Copyleaks blog maps the metaphor ("digital detectives… unanimous jury") to product marketing. Treat the paper as **evidence of stylometric ensemble philosophy**, not a V9 reverse-engineering spec.

### 2.2 Production binary detector — V9/V10 stack (partially documented)

Copyleaks describes a **layered** human-vs-AI system:

| Layer | Function | Source |
|-------|----------|--------|
| **Human-first training** | Trillions of pre-2022 human pages; detect deviation from human norms | Blog, FAQ |
| **Statistical pattern engine** | Frequency ratios, POS, syllable dispersion, hyphen patterns | Help article, product page |
| **Deep learning classifiers** | Proprietary; technique-focused (not per-LLM fine-tune) | FAQ PDF |
| **Mixed-content segmentation** | Sentence/paragraph-level AI % in hybrid docs | Product page |
| **AI Logic — AI Phrases** | Phrase-level heatmap; frequency ratio AI:human (patent-pending, Oct 2024) | Help, AI Logic blog |
| **AI Logic — AI Source Match** | Retrieval: match against **published AI text** online (Aug 2025+) | UIS announcement, St Pete College support |
| **Text manipulation detection** | Homoglyphs, hidden chars, paraphrase/spinners | API enterprise docs |
| **Sensitivity modes (≥v7.1)** | Extra Safe / Balanced / Extra Sensitive ("humanizer" mode) | V10 methodology page |

**Documented pattern features (help center):**

1. **Frequency ratios** — phrases over-represented in AI vs human corpora  
2. **Parts of speech** — grammar/syntax  
3. **Syllable dispersion** — rhythm  
4. **Hyphen use** — mechanical vs human punctuation  

Product page also lists **perplexity-adjacent** framing ("statistical modeling" of LLM outputs) and explicitly names **burstiness-like** signals via syllable dispersion.

**API philosophy (FAQ):** Detect **generation techniques**, not individual model weights — new LLMs covered if they reuse known statistical signatures.

**Sensitivity levels (V10 table, likely inherited from V7.1+):**

| ID | Mode | FP (claimed) | FN (claimed) | Use case |
|----|------|--------------|--------------|----------|
| 1 | Extra Safe | 0.009% | 1.36% | Minimize false accusations |
| 2 | Balanced (default) | 0.026% | 0.79% | General |
| 3 | Extra Sensitive | 0.05% | 0.53% | Humanizer/spinner targeting |

Extra Sensitive is Copyleaks' explicit **anti-humanizer** operating point — trades higher FP for lower FN on spun text.

### 2.3 AI Logic — V9 differentiator

**Launch:** July 2025 (GlobeNewswire: https://www.globenewswire.com/news-release/2025/07/29/3123248/0/en/Copyleaks-Launches-AI-Logic-Across-Major-Learning-Management-Systems-Delivering-Transparent-AI-Detection-for-Educators.html)

| Component | What it adds |
|-----------|--------------|
| **AI Phrases** | Explain *which* phrases drove the score (purple heatmap) |
| **AI Source Match** | Explain *where* similar AI text exists on the web (bridges plagiarism + AI) |

Educator support walkthrough: https://staffsupport.spcollege.edu/hc/en-us/articles/41435997611163-Copyleaks-AI-Logic-AI-Source-Match

**Implication for evasion:** Surface paraphrase may fool the classifier but **leave phrase-frequency footprints**; AI Source Match adds **retrieval** — rewording alone may still match published AI passages.

---

## 3. Claimed performance

### 3.1 Vendor internal (V10 — post-V9)

Source: https://copyleaks.com/ai-detector/testing-methodology

| Evaluator | Dataset | TPR (AI) | TNR (human) | Notes |
|-----------|---------|----------|-------------|-------|
| Data Science | 300K human + 200K AI English, ≥350 chars, incl. "extra-hard" adversarial | **0.988** | **0.999** | Fβ(0.5) = 0.997 |
| QA — human only | 229,843 texts | — | **0.9997** | 60 FP total |
| QA — AI only | 18,712 texts (GPT-5, Claude, Gemini, Grok, etc.) | **0.992** | — | 148 FN |

Product page per-model TNR/TPR snapshots (English): https://copyleaks.com/ai-detector — e.g. human 99.97%, AI 93–99% depending on model family.

Marketing headline: **99.1% English accuracy** (internal, >1M samples, early 2025).

### 3.2 Third-party / independent

| Study / review | Copyleaks result | URL |
|----------------|------------------|-----|
| **Chicago Booth 2026** (via GPTZero rebuttal ecosystem; Copyleaks not in original 3-detector paper) | **90.7% accuracy, 86.9% recall, 5.26% FPR**; misses **45.4% of o3**; paraphrase recall **50–60%** | Secondary: https://fritz.ai/gptzero-review/ ; primary Booth context: https://gptzero.me/news/chicago-booth-2026/ |
| **GPTZero head-to-head** | 99.3% vs Copyleaks 90.7% (3K samples, 2026) | https://fast.io/resources/copyleaks-ai-detector-review-2026/ |
| **Scribbr 12-detector test** | **66%** overall (vs ~99% vendor claim) | https://www.scribbr.com/ai-tools/best-ai-detector/ ; synthesis: https://www.eyesift.com/blog/ai-detection-accuracy-benchmarks/ |
| **Supwriter 2026** | ~**77%** mixed set | https://fast.io/resources/copyleaks-ai-detector-review-2026/ |
| **10K sample study (GPT-4o + Claude 3)** | **96%** | https://fast.io/resources/copyleaks-ai-detector-review-2026/ |
| **EyeSift Apr 2026** (300 samples + QuillBot/Undetectable.AI) | F1 **0.87**; QuillBot FN **31%**; Undetectable.AI FN **23%** | https://www.eyesift.com/blog/copyleaks-ai-detector-review/ |
| **DeepSeek humanization study** | **71%** on humanized vs GPTZero **52%** | Cited: https://detectiondrama.com/ai-detector-bypass-rates-after-humanization/ |
| **Perkins et al. 2024** (805 tests, adversarial) | Copyleaks **most accurate** of tested tools at baseline; still **39.5% → 22.1%** after manipulation | https://link.springer.com/article/10.1186/s41239-024-00487-w ; arXiv: https://arxiv.org/abs/2403.19148 |
| **Weber-Wulff et al. 2023** (computing education) | Copyleaks **top** of 8 detectors on 124+40 submissions | https://arxiv.org/abs/2307.11273 (Copyleaks cites via blog) |
| **GPTHuman 2026 controlled test** | Humanized creative sample → **0% AI** | https://gpthuman.ai/copyleaks-ai-detector-review/ |
| **Proofademic 2026 stress test** | Strong on raw AI; **fails on paraphrased/humanized** | https://proofademic.ai/blog/copyleaks-review/ |

**Pattern:** Copyleaks is **top-tier on raw English AI** in many academic comparisons, **mid-pack on strict 2026 English recall** vs GPTZero/Pangram, **relatively strong on paraphrased AI among peers** but **absolutely weak** (25–71%) once humanization is serious.

---

## 4. Detection signals — mapping to literature

Copyleaks sits in the **three-signal commercial stack** unslop research already tracks:

| Signal | Copyleaks implementation | Humanizer counter |
|--------|-------------------------|-------------------|
| **1. Perplexity / predictability** | LLM "statistical modeling" language; frequency-ratio phrases | Synonym swap, paraphrase |
| **2. Burstiness / rhythm** | Syllable dispersion; sentence-level scoring | Sentence-length variance restoration (unslop structural pass) |
| **3. Stylometric fingerprint** | 3-classifier ensemble paper; POS/hyphen; model-family technique detection | Cross-model roundtrip (Claude↔GPT↔Gemini) |

Humanizers hitting **(1) only** lose to Copyleaks Extra Sensitive + phrase heatmaps. unslop's **balanced/full** modes target (1)+(2); **anti-detector** adds burstiness + cross-model guidance for (2)+(3) — still **not** StealthRL-class.

---

## 5. Humanization & adversarial evasion

### 5.1 What breaks Copyleaks

| Attack | Reported effect | Evidence |
|--------|-----------------|----------|
| **Light QuillBot paraphrase** | ~31 pp detection drop | EyeSift 2026 |
| **Undetectable.ai / dedicated humanizers** | 23–31% FN; vendor's own Jan 2024 test still flagged "humanized" whale article | https://copyleaks.com/blog/undetectable-ai-tools-are-they-worth-it ; EyeSift |
| **Full humanization + manual edit** | **0% AI** in GPTHuman test | https://gpthuman.ai/copyleaks-ai-detector-review/ |
| **DeepSeek + humanization pipeline** | 71% detected (29% bypass) | detectiondrama.com |
| **Perkins adversarial suite** | −17.4 pp mean accuracy | Springer 2024 |
| **Translation round-trip** | Copyleaks claims cross-language robustness; less effective bypass than for monolingual tools | UndetectedGPT analysis: https://www.undetectedgpt.ai/blog/bypass-copyleaks-ai-detection |
| **Homoglyphs / hidden chars** | Claimed detection via manipulation layer | https://docs.copyleaks.com/concepts/use-cases/enterprise-content-governance/ |

### 5.2 What Copyleaks resists better than peers

- **Mixed human/AI documents** — segment-level reporting  
- **AI Phrases** — even reworded text may retain high-frequency AI phrases  
- **AI Source Match** — paraphrase of **published** AI answers  
- **Multilingual** — 30+ languages (accuracy drops: 74–84% Chinese/Japanese/Arabic per repo D-commercial notes)  
- **"Humanizer" setting** — Extra Sensitive mode explicitly tuned for spinner output (vendor claim)

### 5.3 What Copyleaks does **not** stop (August 2026)

- **StealthRL / AuthorMist / RL paraphrase policies** — no public Copyleaks eval  
- **Token ensemble (ToBlend)** — distribution-level attacks; Copyleaks untested in TH-Bench  
- **DivEye / surprisal dynamics** — orthogonal signal; Copyleaks doesn't publish surprisal features  
- **True human rewrite** — all vendors concede this evades classifiers  

---

## 6. Supporters vs critics

### 6.1 Supporters (vendor + aligned studies)

| Claim | Source |
|-------|--------|
| "Most accurate" in 2023 computing-education benchmark | Copyleaks blog aggregating arXiv:2307.11273 — https://copyleaks.com/blog/ai-detector-continues-top-accuracy-third-party |
| 99.88% model attribution / stylistic fingerprints | Paper + blog |
| Best among Big Four on **humanized** DeepSeek text (71%) | detectiondrama.com |
| Lowest FP in vendor FAQ (0.2%) | https://copyleaks.com/blog/how-does-ai-detection-work |
| Enterprise LMS trust (Instructure partnership, 2026) | https://copyleaks.com/blog/ (Instructure post, July 2026) |

### 6.2 Critics

| Claim | Source |
|-------|--------|
| **33-point gap** marketing vs Scribbr independent (99% vs 66%) | https://www.eyesift.com/blog/ai-detection-accuracy-benchmarks/ |
| **5.26% FPR** in Chicago Booth secondary reporting — unusable for high-stakes alone | https://fritz.ai/gptzero-review/ |
| **ESL / formal prose false positives** — 14% FP on structured academic prose (repo B-industry) | docs/research/05-ai-text-detection-and-evasion/B-industry.md |
| Perkins: detectors **not accurate enough for academic integrity** | https://link.springer.com/article/10.1186/s41239-024-00487-w |
| "Heads we win, tails you lose" — FP obsession ignores FN / circumvention | https://www.tandfonline.com/doi/full/10.1080/1360080X.2026.2622146 |
| Humanizer vendors: real-world **~90.7%**, not 99.1% | https://www.undetectedgpt.ai/blog/bypass-copyleaks-ai-detection |

**Synthesis:** Copyleaks is **credible as enterprise screening** and **research-forward** (public ensemble paper). It is **not credible as a sole integrity verdict** at claimed FP rates — independent FPR an order of magnitude higher in several 2026 tests.

---

## 7. Comparison — commercial detectors (August 2026)

| Detector | Clean English recall | Paraphrase/humanized | FP (independent) | Differentiator |
|----------|---------------------|----------------------|------------------|----------------|
| **GPTZero v4.1b** | **99.3%** (Booth) | 60–80% / 18–52% | **0.05%** Booth | Humanizer greylist, process replay |
| **Pangram** | 98.9% Booth | Drops hard on humanized | 0.05% | Paraphrase-aware positioning |
| **Originality Turbo** | 83% Booth | Vendor claims 97% on humanized | 0.11% Booth | Monthly anti-humanizer retrain |
| **Copyleaks V9/V10** | 86.9% Booth secondary | **40–71%** (best-of-four in some tests) | **5.26%** Booth secondary | Multilingual + AI Logic + ensemble |
| **Turnitin** | 92–100% raw | 30–85% edited | Hidden 1–19% band | LMS default |

Copyleaks' niche: **multilingual enterprise + explainability + plagiarism fusion**, not raw English recall crown.

---

## 8. unslop integration audit

### 8.1 Current state

| Asset | Copyleaks relevance |
|-------|---------------------|
| `unslop/scripts/detector.py` | **No Copyleaks backend** — TMR + Desklib only (local HF) |
| README `reads-as-human.png` | Shows Copyleaks "no AI content found" — **anecdotal**, not benchmark |
| `drafts/2026-05-detector-test/` | Copyleaks rows **empty** in scores.csv — needs real runs |
| anti-detector skill | Cross-model second pass aligns with **signal (3)** vs Copyleaks fingerprint ensemble |
| Research synthesis | Already lists Copyleaks "three investigators" in three-signal consensus |

### 8.2 Threat-model placement

| Tier | Actor | vs Copyleaks V9 ensemble |
|------|-------|--------------------------|
| **T0** | Raw ChatGPT paste | Detected (~90%+) |
| **T1** | unslop balanced/full | May reduce AI %; **no published Copyleaks paired bench**; phrase heatmap may still fire |
| **T2** | Cross-model + manual edit | **Primary bypass band** — matches 0–40% AI outcomes in reviews |
| **T3** | StealthRL / adversarial RL | No data; likely **worse for Copyleaks than TMR** |
| **T4** | AI Source Match + plagiarism | Paraphrase irrelevant if text matches **published** AI source |

### 8.3 What unslop should claim

1. ✅ Copyleaks uses **ensemble + stylometry + phrase statistics** — surface slop removal alone is insufficient.  
2. ✅ **Extra Sensitive** mode exists explicitly for humanizers — anti-detector is an arms-race category Copyleaks targets.  
3. ✅ **ESL false-positive defense** remains legitimate; Copyleaks' 5.26% independent FPR >> marketed 0.2%.  
4. ✅ **Cross-model paraphrase** (README) is the right practitioner move against fingerprint ensembles — not guaranteed pass.

### 8.4 What unslop should NOT claim

1. ❌ "Beats Copyleaks" without dated, reproducible API scores on fixed fixtures.  
2. ❌ Equating README screenshot with systematic bypass.  
3. ❌ anti-detector = Copyleaks-safe for academic submission.  
4. ❌ Vendor 99%+ figures as operational bounds.

### 8.5 Recommended engineering (optional)

| Action | Rationale |
|--------|-----------|
| Fill `drafts/2026-05-detector-test/` Copyleaks columns via API | Close empty CSV gap |
| Add Copyleaks to external bench protocol (not `detector.py`) | Commercial API ≠ local TMR |
| Run unslop fixtures at **Balanced vs Extra Sensitive** | Map sensitivity tradeoff |
| Log **AI Phrases** categories when API exposes them | Tune STOCK_VOCAB / phrase avoidance research-only |
| Cross-reference StealthRL outputs against Copyleaks API | Quantify T3 vs commercial ensemble |

---

## 9. Open problems (August 2026)

1. **V9 vs V10 vs paper ensemble** — no public ablation linking unanimous 3-classifier fusion to binary API scores.  
2. **Copyleaks vs DivEye / Fast-DetectGPT / StealthRL** — zero open benchmarks.  
3. **AI Source Match false positives** — student paraphrase of common AI answers may look like "match."  
4. **o3 / reasoning-model gap** — 45.4% miss rate cited in secondary Booth reporting.  
5. **ESL cross-tab** — vendor lacks public confusion matrix by L1 language.  
6. **unslop measured gap** — deterministic + LLM modes untested against live Copyleaks API.

---

## 10. Source index

### Primary — Copyleaks

| Resource | URL |
|----------|-----|
| AI Detector product | https://copyleaks.com/ai-detector |
| How AI detectors work (blog) | https://copyleaks.com/blog/how-does-ai-detection-work |
| AI Logic launch | https://copyleaks.com/blog/ai-logic-has-landed |
| AI Logic LMS (GlobeNewswire) | https://www.globenewswire.com/news-release/2025/07/29/3123248/0/en/Copyleaks-Launches-AI-Logic-Across-Major-Learning-Management-Systems-Delivering-Transparent-AI-Detection-for-Educators.html |
| V10 testing methodology | https://copyleaks.com/ai-detector/testing-methodology |
| Stylistic fingerprints blog | https://copyleaks.com/blog/copyleaks-research-reveals-which-ai-wrote-what |
| Third-party studies aggregator | https://copyleaks.com/blog/ai-detector-continues-top-accuracy-third-party |
| Undetectable AI tools (vendor test) | https://copyleaks.com/blog/undetectable-ai-tools-are-they-worth-it |
| AI Detector API | https://copyleaks.com/api/ai-detector |
| API — enterprise governance | https://docs.copyleaks.com/concepts/use-cases/enterprise-content-governance/ |
| API — response schema | https://docs.copyleaks.com/reference/data-types/ai-detector/ai-text-detector-response |
| Help — detection mechanics | https://help.copyleaks.com/s/article/HowdoesCopyleaksAIDetectionwork681cc74da8fd1 |
| FAQ PDF (Jun 2025) | https://copyleaks.com/wp-content/uploads/2023/05/ai-content-detector-faqs.pdf |
| V9 upgrade (UIS) | https://www.uis.edu/news/center-online-learning-research-service/faculty-orbit-campus-announcement-staff/copyleaks-update-ai-workshop |
| AI Logic support walkthrough | https://staffsupport.spcollege.edu/hc/en-us/articles/41435997611163-Copyleaks-AI-Logic-AI-Source-Match |

### Primary — research paper

| Resource | URL |
|----------|-----|
| arXiv:2503.01659 | https://arxiv.org/abs/2503.01659 |
| PDF | https://arxiv.org/pdf/2503.01659 |
| DOI | https://doi.org/10.48550/arxiv.2503.01659 |
| Copyleaks-hosted PDF | https://copyleaks.com/wp-content/uploads/2025/03/Detecting_Stylistic_Fingerprints_of_Large_Language_Models.pdf |

### Independent benchmarks & reviews

| Resource | URL |
|----------|-----|
| GPTZero Chicago Booth 2026 | https://gptzero.me/news/chicago-booth-2026/ |
| Fritz.ai GPTZero review (Copyleaks row) | https://fritz.ai/gptzero-review/ |
| Fast.io Copyleaks review 2026 | https://fast.io/resources/copyleaks-ai-detector-review-2026/ |
| EyeSift Copyleaks review | https://www.eyesift.com/blog/copyleaks-ai-detector-review/ |
| EyeSift accuracy benchmarks | https://www.eyesift.com/blog/ai-detection-accuracy-benchmarks/ |
| GPTHuman Copyleaks review | https://gpthuman.ai/copyleaks-ai-detector-review/ |
| Proofademic stress test | https://proofademic.ai/blog/copyleaks-review/ |
| ChatAI.guide methodology review | https://chatai.guide/tools/copyleaks-review/ |
| Detection Drama bypass stats | https://detectiondrama.com/ai-detector-bypass-rates-after-humanization/ |
| UndetectedGPT bypass guide | https://www.undetectedgpt.ai/blog/bypass-copyleaks-ai-detection |
| AIVario accuracy analysis | https://aivario.com/tools/copyleaks |
| Scribbr best detector | https://www.scribbr.com/ai-tools/best-ai-detector/ |

### Academic — adversarial / fairness

| Resource | URL |
|----------|-----|
| Perkins et al. 2024 (Springer) | https://link.springer.com/article/10.1186/s41239-024-00487-w |
| Perkins et al. arXiv preprint | https://arxiv.org/abs/2403.19148 |
| Weber-Wulff et al. 2023 | https://arxiv.org/abs/2307.11273 |
| Detectors in education (2026) | https://www.tandfonline.com/doi/full/10.1080/1360080X.2026.2622146 |
| Liang ESL bias (Stanford) | https://arxiv.org/abs/2304.02819 |

### unslop internal

| Resource | Path |
|----------|------|
| Industry synthesis (three investigators) | `docs/research/05-ai-text-detection-and-evasion/B-industry.md` |
| Commercial profile | `docs/research/05-ai-text-detection-and-evasion/D-commercial.md` |
| Detector test protocol | `drafts/2026-05-detector-test/PROTOCOL.md` |
| Empty Copyleaks scores | `drafts/2026-05-detector-test/results/scores.csv` |
| Local detector (no Copyleaks) | `unslop/scripts/detector.py` |
| Agent #26 StealthRL (T3 bound) | `docs/research/2026-08-detector-research/AGENT-26-STEALTHRL.md` |
| Agent #30 ToBlend (distribution attacks) | `docs/research/2026-08-detector-research/AGENT-30-TOBLEND.md` |

---

## 11. Citation (BibTeX)

```bibtex
@misc{bitton2025stylometric,
  title={Detecting Stylistic Fingerprints of Large Language Models},
  author={Bitton, Yehonatan and Bitton, Elad and Nisan, Shai},
  year={2025},
  eprint={2503.01659},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2503.01659}
}

@article{perkins2024bypass,
  title={Simple techniques to bypass {GenAI} text detectors: implications for inclusive education},
  author={Perkins, Mike and Roe, Jack and Vu, Bui Hoang and Postma, Daniel and Hickerson, David and McGaughran, Jennifer and Khuat, Huong Quynh},
  journal={International Journal of Educational Technology in Higher Education},
  volume={21},
  number={1},
  pages={42},
  year={2024},
  doi={10.1186/s41239-024-00487-w},
  url={https://link.springer.com/article/10.1186/s41239-024-00487-w}
}
```

---

## 12. Bottom line

Copyleaks V9 is the **July 2025 ensemble refresh** that paired a new classifier generation with **AI Logic** explainability and (soon after) **AI Source Match** retrieval. The only rigorous ensemble description is the **March 2025 fingerprint paper**: three diverse classifiers, **unanimous vote**, extreme precision on **LLM-family attribution** — a design philosophy that likely informs, but is not identical to, the binary API.

Against humanizers, Copyleaks is **better than GPTZero in some paraphrase studies** yet **still fails outright on polished humanized samples**. Against clean English AI, it **trails GPTZero/Pangram in 2026 Booth-adjacent numbers**. For unslop: respect the **three-signal stack**, run real API benchmarks before any marketing claim, keep **anti-detector** in the ESL-defense lane, and treat Copyleaks as **one commercial ensemble in an arms race** — not the final word on authorship.
