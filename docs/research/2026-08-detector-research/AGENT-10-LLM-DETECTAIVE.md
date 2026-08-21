# Agent #10 — LLM-DetectAIve 4-Way Taxonomy

**Focus:** Fine-grained machine-generated text (MGT) detection — taxonomy design, dataset, benchmarks, debate, humanization implications, unslop integration.  
**Date:** 2026-08-19  
**Authors (paper):** Abassy et al. (MBZUAI / Preslav Nakov group; 18 co-authors, summer-internship cohort)

---

## 1. Executive summary

- **LLM-DetectAIve** ([arXiv:2408.04284](https://arxiv.org/abs/2408.04284), **EMNLP 2024 System Demonstrations**, pp. 336–343) reframes MGT detection from binary "human vs AI" to a **4-way taxonomy** that tracks *how* an LLM participated in text creation — not just *whether* it did.

- **The four classes:** (I) **Human-Written** — no GenAI; (II) **Machine-Generated** — fully LLM from prompt; (III) **Machine-Written → Machine-Humanized** — LLM draft then LLM paraphrase to hide machine origin (obfuscation); (IV) **Human-Written → Machine-Polished** — human draft then LLM grammar/style polish (often acceptable in academic publishing, prohibited in K–12 essay assessment).

- **Mechanism:** Supervised fine-tuning of transformer encoders (RoBERTa, DeBERTa, DistilBERT) on an extended **M4GT-Bench** corpus with ~303K newly generated examples across classes II–IV. Production demo uses **DeBERTa-base** (`raj-tomar001/LLM-DetectAIve_deberta-base` on Hugging Face). Gradio UI on HF Spaces; MIT-licensed code.

- **In-domain headline numbers:** Universal DeBERTa — **95.71% accuracy**, **95.72% macro-F1** on held-out test from the same generator/domain pool. Domain-specific RoBERTa hits **95.79%** (arXiv) and **95.65%** (OUTFOX student essays). DANN+RoBERTa reaches **96.30% precision**, **95.24% accuracy**.

- **Out-of-domain collapse:** On unseen **IELTS ESL essays** — **66.91% accuracy**. On **MixSet** (Zhang et al., NAACL 2024 Findings) — **60.08% accuracy**, **54.95% macro-F1**. The paper acknowledges this openly: fine-grained labels learned on M4GT-style artifacts do not transfer cleanly.

- **Binary comparison (small sample):** On 120 texts (60 human + 60 machine, 10 per M4GT source), LLM-DetectAIve binary-collapsed accuracy **97.50%** vs GPTZero **87.50%**, Sapling **88.33%**, ZeroGPT **69.17%**. Not a rigorous benchmark — quota sample, binary collapse of a 4-class model.

- **Community footprint:** Low hype, low critique. ~13 GitHub stars, ~487 HF model downloads/month (Aug 2026). No dedicated HN/Reddit threads found. Conceptually influential — the taxonomy appears in later position papers (Geng & Poibeau NeurIPS 2025; Zhang et al. arXiv:2510.20810) as the kind of granularity detection *should* target, even while those papers argue detection remains unsolved.

- **Humanization implication:** Category **III** is exactly what **unslop anti-detector mode** produces when run on AI-origin text — LLM rewrite to sound human while preserving machine provenance. Category **IV** is what unslop does to **human-origin** text (Grammarly-class polish) and is the frame for **ESL false-positive defense**: legitimate human writing that was lightly AI-edited. unslop's current `detector.py` loop optimizes **binary** TMR/Desklib scores and cannot distinguish III from IV.

- **unslop gap:** No 4-class backend, no policy-aware stop condition ("fail III, allow IV"), no bench fixture mapped to DetectAIve labels. P1 integration: optional HF DeBERTa scorer + bench logging; P2: policy mode aligned with Originality AI Allowance threshold thinking (Agent #58).

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| arXiv preprint | https://arxiv.org/abs/2408.04284 | v2 Oct 2024; HTML v3 available |
| arXiv HTML | https://arxiv.org/html/2408.04284v3 | Full paper text |
| ACL Anthology | https://aclanthology.org/2024.emnlp-demo.35/ | EMNLP 2024 Demo; DOI 10.18653/v1/2024.emnlp-demo.35 |
| PDF (v2) | https://aclanthology.org/2024.emnlp-demo.35v2.pdf | Camera-ready |
| GitHub | https://github.com/mbzuai-nlp/LLM-DetectAIve | MIT license; ~13 stars Aug 2026 |
| HF Space (demo) | https://huggingface.co/spaces/raj-tomar001/LLM-DetectAIve | Gradio; 50–500 word input window |
| HF model weights | https://huggingface.co/raj-tomar001/LLM-DetectAIve_deberta-base | DeBERTa-base, 4-class head; no model card |
| Demo video | https://youtu.be/E8eT_bE7k8c | System walkthrough |
| M4GT-Bench (base dataset) | https://aclanthology.org/2024.acl-long.220/ | Wang et al., ACL 2024 |
| MixSet (OOD eval) | https://arxiv.org/abs/2401.05952 | Zhang et al., NAACL 2024 Findings |
| MixSet GitHub | https://github.com/Dongping-Chen/MixSet | 5 mixtext operations, binary/3-class baselines |
| MixSet HF dataset | https://huggingface.co/datasets/shuaishuaicdp/MixSet | Public mixtext corpus |
| Ji et al. position (cited) | https://arxiv.org/abs/2406.18259 | "Not just AI vs Humans" — explainability angle |
| IELTS OOD source | https://huggingface.co/datasets/chillies/IELTS_essay_human_feedback | ESL essay OOD test |
| GPTZero (3-class competitor) | https://gptzero.me/ | Adds "mixed" as 3rd class; 40 free scans/day |
| unslop detector | `unslop/scripts/detector.py` | Binary TMR + Desklib only |
| Agent #58 (AI Allowance) | `docs/research/2026-08-detector-research/AGENT-58-ORIGINALITY-AI-ALLOWANCE.md` | Commercial threshold-detection parallel |

---

## 3. The 4-way taxonomy — design and rationale

### 3.1 Problem statement

Binary detectors collapse distinct real-world workflows into one bit. A student who runs ChatGPT on a blank page (Class II) and a student who asks Grammarly to fix commas on their own draft (Class IV) get the same "AI detected" flag. Institutions actually care about the difference: academic journals often permit copy-editing assistance; exam integrity policies typically prohibit *any* LLM touch.

LLM-DetectAIve's taxonomy is a **provenance ladder**:

| Label | Shorthand | Creation pipeline | Typical policy stance |
|-------|-----------|-------------------|----------------------|
| **I** | Human-Written (HW) | Human author, zero GenAI | Always allowed |
| **II** | Machine-Generated (MG) | Prompt → LLM output, no human edit | Prohibited in education; flagged in journalism |
| **III** | Machine-Humanized (M→MH) | LLM draft → LLM "make this sound human" | Obfuscation; bypasser category; Turnitin "AI bypasser" target |
| **IV** | Machine-Polished (H→MP) | Human draft → LLM grammar/style polish | Often OK in academia; prohibited in zero-tolerance K–12 |

Category III is the **adversarial humanization** class — the paper names it explicitly as detecting "attempts to obfuscate the fact that a text was machine-generated." Category IV captures **assistive editing** where intellectual content remains human-origin.

### 3.2 Relationship to adjacent taxonomies

| System | Classes | Contrast with DetectAIve |
|--------|---------|--------------------------|
| **GPTZero** | 3 (human / AI / mixed) | "Mixed" is undifferentiated; no III vs IV split |
| **MixSet** (Zhang et al.) | 5 operations (polish, complete, rewrite, adapt, humanize) | Process-centric, not policy-centric; detectors fail at 0.3–0.7 acc on subtle mixtext |
| **Originality AI Allowance** (2026) | Threshold % AI (0–40%) | Commercial policy gate; continuous not categorical |
| **LLM-DetectAIve** | 4 provenance classes | Discrete labels tied to creation pipeline |

The DetectAIve taxonomy is the cleanest **academic articulation** of the III/IV split that commercial products later approximate with threshold sliders.

### 3.3 Planned fifth class

Future work (paper §6) proposes **Machine-Written → Human-Edited** — LLM draft then manual human revision. Authors cite cost of collecting human-edited data. This matters for unslop: a user who humanizes AI text *by hand* after unslop would fall between III and the proposed V.

---

## 4. Dataset construction

### 4.1 Base: M4GT-Bench extension

Built on **M4GT-Bench** (Wang et al., ACL 2024) — six domains: arXiv abstracts, WikiHow, Wikipedia, Reddit ELI5, OUTFOX student essays, PeerRead reviews. Sampled subset: **79,220** human-written + **103,075** machine-generated (legacy generators: davinci-003, GPT-3.5, Cohere, Dolly-v2, BLOOMz, GPT-4).

### 4.2 New generations (Classes II–IV)

| Class | Count | Generators used |
|-------|-------|-----------------|
| II (full MGT, new models) | 91,358 | GPT-4o, Llama3-8B/70B, Mixtral-8x7B, Gemma-7B/2-9B, Gemini-1.5, Mistral-7B |
| III (M→MH) | 103,852 | Same pool; humanization prompts |
| IV (H→MP) | 107,900 | Polish/paraphrase prompts on human-written sources |

**Total new LLM-dependent generations:** 303,110 texts (≤1,500 words each).

### 4.3 Generation prompts (verified from paper §2.2)

**Class III (humanize/obfuscate):**
- "Rewrite this text to make it sound more natural and human-written"
- "Rephrase this text to be easy to understand and personable"

**Class IV (polish):**
- "Paraphrase the provided text"
- "Rewrite this text so that it is grammatically correct and flows nicely"

All prompts include a trailing constraint: *"Only output the text in double quotes with no text before or after it."* Post-processing strips LLM preamble artifacts ("Sure!", "Here is the paraphrased text:") — the paper notes these would otherwise leak class signal.

### 4.4 Dataset release status

**The fine-grained 4-class dataset is not publicly released** as a Hugging Face dataset (Aug 2026). Only the demo model, Gradio app, and GitHub inference code are open. Reproduction requires re-generating from M4GT-Bench + the paper's prompt templates. This limits independent audit.

### 4.5 Known dataset artifacts (authors acknowledge)

- **Domain-formatting leakage:** WikiHow and PeerRead LLM outputs retain markdown lists, bullet headers — domain-correlated surface features.
- **English-only.**
- **Generator-domain coupling:** Some generator×domain cells are sparse (e.g., Gemma on PeerRead = 0 rows in Table 1).

---

## 5. Detection models and deployment

### 5.1 Architectures trained

| Model | Role | Hyperparams (full dataset) |
|-------|------|---------------------------|
| **RoBERTa-base** | Universal + domain-specific | lr 5e-5, wd 0.01, 10 epochs, batch 32 |
| **DeBERTa-base** | Universal (best) | Same |
| **DistilBERT** | Domain-specific trials; paper §3 mentions demo speed | lr 2e-5, batch 16 |
| **DANN + RoBERTa** | Domain-adversarial universal | GRL on 6 domain labels |

**Deployed backend:** DeBERTa-base fine-tuned 4-class head (~184M params). Paper §3 text mentions DistilBERT for demo speed; §4.2 and HF weights confirm **DeBERTa** shipped.

### 5.2 Demo constraints

- Input length: **50–500 words** (performance cliff outside this band).
- Longer inputs truncated to BERT context window.
- Two UI modes: (1) automatic 4-class prediction; (2) **Human Detector Playground** — gamified quiz where users guess the class.

### 5.3 Code repository

GitHub `mbzuai-nlp/LLM-DetectAIve`: Gradio app + inference wrapper. MIT license. Low maintenance (last push Dec 2024, 2 open issues Aug 2026). No training scripts or dataset shards in public repo — inference/demo only.

---

## 6. Benchmark results (verified numbers)

### 6.1 In-domain performance

| Setup | Best model | Accuracy | Macro-F1 | Notes |
|-------|------------|----------|----------|-------|
| Domain-specific | RoBERTa | 95.79 (arXiv), 95.65 (OUTFOX) | ~95.5 | Requires user to pick domain |
| Universal (full dataset) | **DeBERTa** | **95.71** | **95.72** | Deployed in HF demo |
| DANN + RoBERTa | RoBERTa + GRL | 95.24 | 96.06 | +1.4 pp precision over plain RoBERTa |

Primary confusion: **II ↔ IV** and **III ↔ IV** — adjacent provenance classes share surface statistics.

### 6.2 Commercial binary comparison (n=120 only)

LLM-DetectAIve binary-collapsed: **97.50%** vs Sapling 88.33%, GPTZero 87.50%, ZeroGPT 69.17%. Quota sample, not 4-class vs 4-class.

### 6.3 Out-of-domain (critical)

| Test set | Accuracy | Macro-F1 |
|----------|----------|----------|
| IELTS ESL essays | **66.91** | 66.55 |
| MixSet (3,600 samples) | **60.08** | 54.95 |

Paper conclusion: fine-grained labels learned on M4GT artifacts do not transfer to unseen generators/domains.

### 6.4 Not benchmarked

No RAID/MAGE/PAN numbers; no TempParaphraser, DIPPER, or commercial humanizer eval; no unslop outputs; no TPR@FPR=1%.

---

## 7. Community and academic debate

**Supporters:** EMNLP 2024 demo acceptance; first operational III/IV split; honest OOD reporting (60–67%); Human Detector Playground UX for calibrated trust. Nakov-group lineage (M4GT-Bench, SemEval Task 8) lends credibility.

**Critics:** Geng & Poibeau (NeurIPS 2025 position) — detection unsolved in practice; Zhang et al. (arXiv:2510.20810) — no unified definition of "LLM-generated"; Why AI Detection Fails (arXiv:2603.23146) — dataset artifact hypothesis explains 95%/60% split; MixSet shows pre-DetectAIve detectors at 0.3–0.7 on subtle mixtext. SHIELD (arXiv:2507.15286) — no TPR@FPR=1% reported. No public dataset; 13 GitHub stars; no independent replication.

**Overhyped:** 95.71% is in-domain synthetic labels; 97.50% vs GPTZero is n=120 binary collapse; demo capped at 500 words; Class III training is LLM-on-LLM only — not commercial humanizers or cross-model paraphrase.

**Genuinely novel:** Policy-aware provenance taxonomy; explicit M→MH obfuscation class (Turnitin "AI bypasser" precursor); DANN domain-adversarial training (+1.4 pp precision).

---

## 8. Humanization angle — mapping unslop outputs to the taxonomy

### 8.1 What unslop produces, by input origin

| Input origin | unslop mode | Likely DetectAIve class | Policy risk |
|--------------|-------------|-------------------------|-------------|
| AI-generated draft | `balanced` / `full` | Still **II** or drift to **III** | High in education |
| AI-generated draft | `anti-detector` + structural passes | **III** (M→MH) — target evasion class | Highest — explicit obfuscation |
| Human draft | `balanced` / `full` | **IV** (H→MP) if LLM rewrite heavy | Context-dependent |
| Human draft | `subtle` (regex-only, no LLM) | Stays **I** | Low |
| Human draft + voice-match | LLM with profile constraints | **IV** with voice preservation | ESL FP defense use case |

**Key insight:** unslop anti-detector on AI text optimizes for **Category III evasion** — exactly the class DetectAIve was built to catch. Binary TMR/Desklib loops measure "AI probability" without naming the class; a text could score 40% AI (TMR pass) but still classify as III (DetectAIve fail).

### 8.2 Evasion tactics at the III/IV boundary

DetectAIve confusion matrices show **III ↔ IV** as the primary error pair — the humanizer arms race lives here.

- **Obfuscate AI origin (III → I/IV):** Cross-model second pass, surprisal-variance injection (DivEye), contraction restoration, sentence-length σ ≥ 6 — unslop anti-detector stack.
- **Polish human draft (stay IV):** Light grammar fixes; preserve contractions, fragments, domain terms.
- **ESL false-positive defense:** Voice-match from prior writing; avoid heavy LLM rewrite that pushes human **I → IV**.

MixSet shows token/sentence polish drops binary detectors to near-random; DetectAIve learns in-domain III/IV from LLM prompts similar to QuillBot — but cross-model paraphrase, commercial humanizers, and unslop structural passes (`structural.py`) are untested against this classifier.

---

## 9. unslop integration plan

Current state (`detector.py`, `humanize.py`, `skills/unslop/SKILL.md`):

| Component | Today | Gap |
|-----------|-------|-----|
| `detector.py` | Binary TMR + Desklib; `score_ai_probability()` | No 4-class backend |
| `fetch_detectors.py` | TMR (~500MB) + Desklib (~1.5GB) | No DetectAIve DeBERTa fetch |
| Anti-detector mode | Binary target ≤0.5 AI prob | No III/IV distinction; no policy gate |
| Bench protocol | GPTZero, Originality, Copyleaks, TMR | DetectAIve not listed |
| SKILL.md | Names DivEye, TempParaphraser, Turnitin bypasser | No 4-way taxonomy awareness |

### 9.1 Priority changes

| Priority | Action |
|----------|--------|
| **P0** | Add DetectAIve to May 2026 bench protocol; log 4-class softmax; pilot 5 AI + 5 human fixtures × 4 intensity modes |
| **P1** | `detectaive` backend in `detector.py` + `fetch_detectors.py` (HF DeBERTa); `score_provenance()`; `--provenance-policy strict\|academic\|binary`; III/IV-aware anti-detector prompt |
| **P2** | Policy stop conditions; MixSet OOD regression (~60% baseline); map Originality AI Allowance thresholds to III/IV (Agent #58) |

---

## 10. Recommended actions

**P0:** Bench DetectAIve with 4-class logging; document unslop anti-detector → Class III, human polish → Class IV.

**P1:** Implement HF DeBERTa backend; `--provenance-policy`; III/IV-aware prompts in anti-detector mode.

**P2:** Labeled unslop before/after corpus; Originality Allowance mapping; watch for public dataset release.

---

## 11. Open questions

1. Will MBZUAI publish the 303K 4-class corpus? Without it, 95.71% is unverifiable.
2. III recall on TempParaphraser, commercial humanizers, or unslop anti-detector outputs?
3. IV false-positive rate on unmodified human OUTFOX essays (32 misclassified in confusion matrix)?
4. How to score 2,000-word essays — chunk vote vs aggregate softmax?
5. Does cross-model paraphrase drop III recall the way TempParaphraser drops binary detectors (82.5%)?

---

## Cross-references

- **Agent #58** — Originality AI Allowance; commercial threshold parallel to III/IV policy split.
- **Agent #01 / #34** — DivEye surprisal variance; orthogonal signal to BERT 4-class (ensemble opportunity).
- **Agent #25 / #39** — Adversarial paraphrasing; primary III evasion attack not in DetectAIve training.
- **Agent #36** — HumanLLM benchmark; human-AI collaboration evaluation landscape.
- **Agent #43** — Catch Me If You Can personal style; Class IV vs I boundary for voice-preserving polish.
- **MixSet / Zhang et al.** — Mixtext detection baseline showing pre-DetectAIve detector failure modes.
- **UPDATE-PLAN-2026-08** — Internal priority flag for 4-way taxonomy research.

---

*Research conducted 2026-08-19 via arXiv HTML v3, ACL Anthology PDF v2, GitHub/Hugging Face pages, MixSet paper (arXiv:2401.05952), Geng & Poibeau NeurIPS 2025 position paper metadata, Zhang et al. arXiv:2510.20810, Why AI Detection Fails arXiv:2603.23146, SHIELD arXiv:2507.15286, and unslop codebase audit (`detector.py`, `humanize.py`, `skills/unslop/SKILL.md`).*
