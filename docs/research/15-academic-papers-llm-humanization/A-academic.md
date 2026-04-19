# A — Core Academic Survey: Humanizing LLM Output

**Research value: high** — The humanization/evasion literature is substantial, converging on a stable set of attack primitives (paraphrase, style transfer, RL-guided rewriting, watermark removal) and an equally stable set of detector countermoves (adversarial training, rewriting-based detection, augmentation). Enough reproducible code and benchmarks exist to ground the "Humazier" project in prior art.

Scope: papers that explicitly *humanize* AI-generated text (make it less detectable / more human-like), plus the detection side needed to read the humanization literature coherently. Timeframe is weighted to 2023–2026. Reproducibility is called out in every entry: **[Repro: high / medium / low]** based on whether code, data, and a specified base model are released.

---

## 1. Canonical humanization / evasion attacks

### 1.1 Sadasivan et al., *Can AI-Generated Text Be Reliably Detected?* (arXiv:2303.11156, 2023)
- **Contribution:** The foundational impossibility argument. Shows empirically that recursive paraphrasing drops detector accuracy from ~97% to 57–80%, and proves a theoretical bound: as the TV-distance between human and LLM distributions shrinks, even the best detector approaches a random classifier.
- **Also introduces** spoofing attacks (forcing human text to look AI-generated).
- **Why it matters for humanization:** supplies the theoretical license for the whole humanizer research program. Paraphrasing is not a bug of current detectors; it is near-optimal by construction.
- **[Repro: medium]** — attack procedure is simple and replicable with any off-the-shelf paraphraser; no dedicated code repo from the authors.

### 1.2 Krishna et al., *Paraphrasing Evades Detectors of AI-Generated Text, but Retrieval is an Effective Defense* (DIPPER, NeurIPS 2023, arXiv:2303.13408)
- **Contribution:** Trains **DIPPER**, an 11B T5-XXL paragraph-level paraphraser with two inference-time control knobs (lexical diversity, content reordering). Reduces DetectGPT accuracy from 70.3% → 4.6% at 1% FPR while preserving semantics. Proposes a retrieval-based defense (store generations; look them up) that recovers 80–97% of paraphrased text.
- **[Repro: high]** — model weights on HuggingFace (`kalpeshk2011/dipper-paraphraser-xxl`), official GitHub repo, explicit control parameters.
- **Project relevance:** the strongest publicly-available paragraph-scale humanizer baseline.

### 1.3 Hu, Chen & Ho, *RADAR: Robust AI-Text Detection via Adversarial Learning* (NeurIPS 2023, arXiv:2307.03838)
- **Contribution:** Joint adversarial training of a paraphraser against a detector — the humanizer and detector improve each other. Evaluated across 8 LLMs and 4 datasets; resulting detector is robust to paraphrasing, and the paraphraser itself is a capable humanizer.
- **[Repro: high]** — code at `IBM/RADAR`, web demo, published training recipe.
- **Project relevance:** canonical example of "humanizer as a byproduct of adversarial training"; directly informs the detector-in-the-loop architecture.

### 1.4 Cheng et al., *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text* (arXiv:2506.07001, 2025)
- **Contribution:** Training-free attack that uses an instruction-following LLM to paraphrase under the guidance of a target detector's score. Under OpenAI-RoBERTa-Large guidance: average T@1%F reduction of 87.88% across neural, watermark, and zero-shot detectors. Against Fast-DetectGPT, T@1%F drops by 98.96%; against RADAR, 64.49%. Mostly slight quality degradation.
- **[Repro: high]** — method is essentially a prompt loop + detector score; reproducible with any OSS detector and paraphraser.
- **Project relevance:** current state-of-the-art "no-training" humanizer pattern; simplest strong baseline to implement.

### 1.5 Zhou et al., *Humanizing Machine-Generated Content: Evading AI-Text Detection through Adversarial Attack* (LREC-COLING 2024)
- **Contribution:** Frames humanization as adversarial text perturbation; proposes a pipeline that swaps tokens guided by detector gradients / scores while constraining edit distance and semantic drift.
- **[Repro: medium]** — methods described in full; code not always released.
- **Project relevance:** establishes "humanization = constrained adversarial edit" framing that recurs in later work.

### 1.6 Wang et al., *RAFT: Realistic Attacks to Fool Text Detectors* (arXiv:2410.03658, 2024)
- **Contribution:** Black-box word-level attack that exploits LLM embedding transferability. Greedily perturbs high-impact words while preserving grammar. Compromises all evaluated detectors by up to 99% across domains; human eval confirms outputs are indistinguishable from human text. Shows detector-adversarial training on RAFT outputs restores robustness.
- **[Repro: high]** — published as benchmark; attack primitive is simple.
- **Project relevance:** demonstrates that *small* word-level edits are already sufficient; a low-compute humanizer path.

### 1.7 Chen et al., *MASH: Multi-stage Alignment for Style Humanization* (arXiv:2601.08564, 2026)
- **Contribution:** Three-stage pipeline — SFT on AI↔human parallel pairs, DPO with a detector-score preference signal, and inference-time refinement. ~92% avg attack success against black-box detectors.
- **[Repro: medium]** — recipe documented; depends on the parallel corpus being released.
- **Project relevance:** current reference architecture for "humanizer as a fine-tuned model" rather than inference-time prompt loop.

### 1.8 StealthRL (arXiv:2602.08934, 2026)
- **Contribution:** GRPO + LoRA on Qwen3-4B against an ensemble of detectors (RoBERTa, Fast-DetectGPT, Binoculars, MAGE). 97.6% attack success; mean AUROC 0.79 → 0.43. Attacks trained on some detectors transfer to held-out ones.
- **[Repro: high]** — GRPO recipe, base model, and detector ensemble are all public.
- **Project relevance:** cleanest recent demonstration that RL + detector rewards yields transferable humanizers.

### 1.9 Jiao et al., *AuthorMist: A Reinforcement Learning Approach to Text Privacy Enhancement* (arXiv:2503.08716, 2025)
- **Contribution:** 1B-param base model fine-tuned via RL with external *commercial* detector APIs (GPTZero, Winston) as reward. Adds a grammar-correction post-step.
- **[Repro: medium]** — methodology clear; depends on detector API quotas.
- **Project relevance:** shows humanization can be trained against *black-box* commercial detectors, not only open ones.

### 1.10 Kalemaj et al., *Please Make It Sound Like Human: Encoder-Decoder vs. Decoder-Only Transformers for AI-to-Human Text Style Transfer* (arXiv:2604.11687, 2026)
- **Contribution:** Builds a 25,140-pair AI↔human parallel corpus and identifies 11 measurable stylistic markers. BART-large beats Mistral-7B (BERTScore F1 0.924) with far fewer params.
- **[Repro: high]** — parallel corpus + fine-tuning recipe; modest compute footprint.
- **Project relevance:** evidence that humanization does not require frontier-scale models; a 400M encoder-decoder is competitive.

### 1.11 Horvitz et al., *ParaGuide: Guided Diffusion Paraphrasers for Plug-and-Play Textual Style Transfer* (AAAI 2024, arXiv:2308.15459)
- **Contribution:** Guided diffusion over paraphrases with gradient signals from classifiers and style embedders. Arbitrary target style at inference time without retraining.
- **[Repro: medium]** — code released; diffusion over text is heavier than autoregressive rewriting.
- **Project relevance:** one of the few non-autoregressive humanizer approaches; useful if controllability matters more than throughput.

### 1.12 Wang et al., *SIRA: Revealing Weaknesses in Text Watermarking Through Self-Information Rewrite Attacks* (arXiv:2505.05190, 2025)
- **Contribution:** Targets the exact tokens watermarks rely on (high-entropy positions). ~100% success against seven recent watermarking schemes including Kirchenbauer's. $0.88 per million tokens, transfers across LLMs, no access to the watermark scheme.
- **[Repro: high]** — attack is mechanical and cheap.
- **Project relevance:** if any downstream detector uses watermarking, SIRA is the reference removal attack.

---

## 2. Benchmarks & evaluation frameworks for humanization

### 2.1 Liu et al., *TH-Bench: Evaluating Evading Attacks via Humanizing AI Text on Machine-Generated Text Detectors* (arXiv:2503.08708, 2025)
- **Contribution:** First systematic humanization benchmark. 6 SOTA humanization attacks × 13 detectors × 6 datasets × 19 domains × 11 generator LLMs. Measures three axes: evasion effectiveness, text-quality preservation, compute overhead.
- **Headline finding:** no single attack dominates all three axes — genuine Pareto frontier.
- **[Repro: high]** — benchmark and attack implementations released.
- **Project relevance:** the evaluation harness to adopt rather than reinvent.

### 2.2 Dugan et al., *RAID: Robust AI Detection* (ACL 2024)
- **Contribution:** 6M+ generations across 11 generators, 8 domains, 11 adversarial attacks, 4 decoding strategies. Finds that nearly all of 12 tested detectors are "easily fooled" by sampling changes, repetition penalties, unseen generators, and adversarial attacks.
- **[Repro: high]** — leaderboard + open dataset.
- **Project relevance:** the standard stress test for any claim of humanizer success.

### 2.3 He et al., *MAGE: Machine-Generated Text Detection Under Out-of-Distribution Settings* (ACL 2024)
- **Contribution:** Large cross-domain, cross-generator evaluation explicitly targeting generalization failures; now used as a detector component in humanization benchmarks (e.g., StealthRL uses MAGE as one target).
- **[Repro: high]** — data + splits released.

### 2.4 Wang et al., *M4: Multi-generator, Multi-domain, Multi-lingual Black-Box Machine-Generated Text Detection* (EACL 2024, Best Resource Paper)
- **Contribution:** The multilingual/black-box benchmark. Confirms severe generalization failure of detectors on unseen domains and generators. Fed SemEval-2024 Task 8.
- **[Repro: high]** — `mbzuai-nlp/M4` on GitHub.
- **Project relevance:** the go-to multilingual evaluation set for humanizer work that needs non-English coverage.

### 2.5 Guo et al., *How Close is ChatGPT to Human Experts? HC3 Corpus* (2023)
- **Contribution:** Earliest widely-used human↔ChatGPT parallel corpus (QA, academic, medical, finance). Still a default reference dataset in downstream humanization work.
- **[Repro: high]** — dataset public on HuggingFace (`Hello-SimpleAI/HC3`).

### 2.6 Tulchinskii et al. / DAMAGE (2025, ACL GenAIDetect workshop)
- **Contribution:** Qualitatively studies **19 real commercial humanizer/paraphraser tools** (GPT-guard, Undetectable.ai, StealthGPT, etc.), then trains a data-centric augmented detector that generalizes across humanizers. Argues detection robustness should be treated as a learned invariance, not a per-humanizer patch.
- **[Repro: medium]** — detector code public; commercial tools require accounts.
- **Project relevance:** rare academic engagement with the *commercial humanizer* ecosystem, which is the actual competitive landscape for a "Humazier"-style product.

---

## 3. Detection baselines (needed to read the humanizer literature)

### 3.1 Mitchell et al., *DetectGPT* (ICML 2023) — probability curvature under local perturbations. Public code. The default zero-shot baseline every humanizer is evaluated against.
### 3.2 Bao et al., *Fast-DetectGPT* (ICLR 2024) — conditional probability curvature; 340× faster; AUROC 0.93+ on ChatGPT/GPT-4. [Repro: high, `baoguangsheng/fast-detect-gpt`].
### 3.3 Hans et al., *Binoculars* (ICML 2024, arXiv:2401.12070) — two-LLM cross-perplexity ratio; >90% accuracy at 0.01% FPR; no training. [Repro: high, `ahans30/Binoculars`].
### 3.4 Verma et al., *Ghostbuster* (NAACL 2024) — feature-space search over LM probability features; claims robustness to paraphrase/perturbation; 99.0 F1 in-domain. [Repro: high].
### 3.5 Kirchenbauer et al., *A Watermark for Large Language Models* (ICML 2023) — green-list biased sampling; the watermarking reference point that SIRA and DIPPER attack. [Repro: high, `jwkirchenbauer/lm-watermarking`].
### 3.6 Gehrmann et al., *GLTR: Statistical Detection and Visualization of Generated Text* (ACL 2019) — the perplexity/rank visualization ancestor; pre-dates LLM detection but defines the feature language still used today.
### 3.7 Mao et al., *Raidar: geneRative AI Detection via Rewriting* (ICLR 2024, arXiv:2401.12970) — detector built on the observation that LLMs edit human text more than AI text when asked to rewrite. Adds up to +29 F1 to existing detectors; black-box; robust on new content. [Repro: high]. **Directly informs humanization research**: a humanizer that survives Raidar must either break the "LLMs leave AI text alone" asymmetry or make its output look edit-worthy.

---

## 4. Adversarial defenses / robust detectors (humanization counter-moves)

### 4.1 GREATER (ACL 2025, aclanthology.org/2025.acl-long.155) — synchronized adversary/detector updates that generalize across attack intensities; current SOTA adversarial-training detector.
### 4.2 RADAR (§1.3) — doubles as defense.
### 4.3 DAMAGE (§2.6) — cross-humanizer generalization via data-centric augmentation rather than per-attack patches.
### 4.4 Krishna et al. retrieval defense (§1.2) — 80–97% recovery of paraphrased outputs by storing previous generations.

---

## 5. Stylistic / linguistic studies of the human–AI boundary

### 5.1 Reinhart et al., *Do LLMs Write Like Humans? Variation in Grammatical and Rhetorical Styles* (PNAS 2025)
- Finds instruction-tuned LLMs are noun-heavy and informationally dense, and fail to adapt style across genres the way humans do. Provides a menu of *measurable* axes a humanizer should target.
### 5.2 Sardinha et al., *Stylometric Comparisons of Human vs. AI-Generated Creative Writing* (Nature HSS Comms 2025)
- LLM outputs cluster tightly by model; humans form broad heterogeneous clusters. Burrows' Delta and word-frequency distributions still separate the two even with prompting tricks.
### 5.3 Muñoz-Ortiz et al., *Differentiating Human-Written and AI-Generated Texts Using Automatically Extracted Linguistic Features* (arXiv:2407.03646 → MDPI Information 2025)
- Phonological, morphological, and modifier-level differences. Explicit feature list usable as humanizer training signal.
### 5.4 Kumarage et al., *StyloAI* (arXiv:2405.10129) — 31 stylometric features + Random Forest; 81–98% accuracy. Useful as a cheap auxiliary detector for humanizer evaluation.

---

## 6. Surveys

### 6.1 Wu et al., *A Survey on LLM-Generated Text Detection: Necessity, Methods, and Future Directions* (Computational Linguistics, 2025, aclanthology.org/2025.cl-1.8)
- Taxonomy: watermarking vs statistical vs neural vs human-assisted. Explicit section on evasion/humanization as an open problem.
### 6.2 Crothers et al., *Machine-Generated Text: A Comprehensive Survey* (arXiv:2011.01314, updated) — earlier but still cited for generation-side taxonomy.
### 6.3 Tang et al., *Detection of Machine-Generated Text: Literature Survey* (arXiv:2402.01642, 2024)
### 6.4 *Machine-Human Boundary: A Systematic Survey of Machine-Generated Text Detection* (IEEE, 2025)
- Emphasizes the human↔AI boundary as a moving target; flags humanization as a first-class threat model rather than a robustness footnote.

---

## 7. Patterns, trends, and gaps

**Patterns that recur across papers.**
1. **Detector-in-the-loop is the dominant humanizer primitive.** DIPPER+search, Adversarial Paraphrasing, RADAR, StealthRL, AuthorMist, MASH all use detector scores either as reward (RL) or as a selection signal (search/guidance). Anything not using detector feedback underperforms these by a large margin.
2. **Transferability across detectors is the rule, not the exception.** Attacks trained against one detector (or ensemble subset) transfer to held-out detectors (StealthRL, RAFT, Adversarial Paraphrasing). This is a *product* signal: a humanizer does not need to track every commercial detector individually.
3. **Humanization quality ≠ evasion quality.** TH-Bench makes this explicit and every attack paper hits a Pareto frontier between (a) detector evasion, (b) semantic preservation, (c) stylistic naturalness, (d) compute cost.
4. **Watermarks are fragile.** SIRA and similar cheap rewrites defeat nearly every published watermark; watermark-only defenses should be treated as table stakes, not a moat.
5. **Stylometric asymmetries are real and measurable.** The Reinhart / Sardinha / StyloAI line of work agrees: LLMs are over-nominal, under-varied, and over-clustered. A humanizer with explicit stylistic targets (burstiness, genre adaptation, lexical heterogeneity) is better grounded than a pure detector-reward humanizer.
6. **"Paraphrase + grammar polish" is a surprisingly strong baseline.** Multiple papers (DIPPER, AuthorMist, RAFT) find that a capable paraphraser plus a light surface-form cleanup matches or beats more elaborate pipelines.

**Reproducibility landscape.**
- **High reproducibility (code + data + base models public):** DIPPER, RADAR, Binoculars, Fast-DetectGPT, Ghostbuster, Kirchenbauer watermark, RAID, MAGE, M4, HC3, Raidar, TH-Bench, RAFT, SIRA.
- **Medium:** MASH, ParaGuide, DAMAGE, AuthorMist, Zhou et al. (LREC).
- **Low:** some commercial humanizer evaluations (by necessity — closed APIs).
- Practical implication: a from-scratch humanizer can be built end-to-end on fully open artifacts.

**Open gaps the project can exploit.**
1. **Long-form coherence.** Nearly every benchmark is paragraph- or short-passage-scale. Humanizing 5k-word documents with consistent persona, argument structure, and citation style is under-served.
2. **Multilingual humanization.** M4 shows detectors degrade on non-English; almost no humanizer paper targets non-English as a primary axis.
3. **Style-conditioned humanization.** Current humanizers optimize *away from AI*, not *toward a specific human voice*. Conditioning on authorial style (ParaGuide, style-transfer work) is nascent.
4. **Agentic / multi-turn humanization.** All published humanizers are single-pass. Iterative humanization with editing feedback (self-critique, Raidar-style asymmetry inversion) is barely explored.
5. **Quality evaluation beyond BERTScore.** Field still leans on BERTScore/BLEU for semantic preservation. Human-judgment-level fidelity metrics (LLM-as-judge with calibrated rubrics, factuality checks) are missing from most humanization papers.
6. **The "authorship obfuscation vs. plagiarism evasion" asymmetry** (arXiv:2511.00416) — detectors catch humanized LLM text better than humanized human text. This is a surprising result that implies a humanizer aiming at the "human paraphrasing human" regime is genuinely harder to detect than one starting from AI text.

---

## Sources

- arXiv:2303.11156 — Sadasivan et al., *Can AI-Generated Text Be Reliably Detected?*
- arXiv:2303.13408 — Krishna et al., DIPPER
- arXiv:2307.03838 — Hu et al., RADAR
- arXiv:2506.07001 — Cheng et al., Adversarial Paraphrasing
- aclanthology.org/2024.lrec-main.739 — Zhou et al., Humanizing Machine-Generated Content
- arXiv:2410.03658 — RAFT
- arXiv:2601.08564 — MASH
- arXiv:2602.08934 — StealthRL
- arXiv:2503.08716 — AuthorMist
- arXiv:2604.11687 — Please Make It Sound Like Human
- arXiv:2308.15459 — ParaGuide (AAAI 2024)
- arXiv:2505.05190 — SIRA
- arXiv:2503.08708 — TH-Bench
- aclanthology.org/2024.acl-long.674 — RAID
- ACL 2024 — MAGE (He et al.)
- aclanthology.org/2024.eacl-long.83 — M4
- Guo et al. 2023 — HC3
- aclanthology.org/2025.genaidetect-1.9 — DAMAGE
- Mitchell et al. ICML 2023 — DetectGPT
- ICLR 2024 — Fast-DetectGPT (Bao et al.)
- arXiv:2401.12070 — Binoculars
- NAACL 2024 — Ghostbuster (Verma et al.)
- ICML 2023 — Kirchenbauer et al., LLM Watermark
- ACL 2019 — GLTR
- arXiv:2401.12970 — Raidar
- aclanthology.org/2025.acl-long.155 — GREATER
- PNAS 2025 — Reinhart et al., Do LLMs Write Like Humans?
- Nature HSS Comms 2025 — Sardinha et al., Stylometric comparisons
- arXiv:2407.03646 / MDPI Information 2025 — Linguistic feature differentiation
- arXiv:2405.10129 — StyloAI
- aclanthology.org/2025.cl-1.8 — Wu et al., Survey on LLM-Generated Text Detection
- arXiv:2402.01642 — Tang et al., Detection of Machine-Generated Text Survey
- IEEE 2025 — Machine-Human Boundary survey
- arXiv:2511.00416 — Authorship obfuscation vs plagiarism evasion asymmetry
