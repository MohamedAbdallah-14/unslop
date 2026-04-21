# 15.C — Open-Source Code Accompanying Academic Papers on LLM Humanization

**Research value: high** — The humanization/evasion-detection arms race is one of the best-documented open-source research threads in NLP right now; most major claims have a paper-with-code artifact, and the repos cluster cleanly into four functional camps (humanizers, detectors, metrics, benchmarks).

**Scope:** Papers-with-code repos covering (a) direct humanization / paraphrase-evasion attacks, (b) authorship style obfuscation, (c) human-likeness metrics (MAUVE, HUSE, etc.), and (d) benchmarks that compare humanizers head-to-head. All repos below are linked to a peer-reviewed or arXiv paper.

---

## Humanization & Paraphrase-Evasion Attacks (direct prior art)

### 1. Adversarial Paraphrasing — `chengez/Adversarial-Paraphrasing`
- **Paper:** Cheng et al., *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text*, NeurIPS 2025 — [arXiv 2506.07001](https://arxiv.org/abs/2506.07001)
- **Repo:** https://github.com/chengez/Adversarial-Paraphrasing (~39 ★)
- **What it does:** Training-free, detector-guided paraphrasing loop. An off-the-shelf instruction LLM rewrites AI text under feedback from a detector; the rewrite is kept when it lowers the detector score.
- **README quote:** *"Most, if not all, high-performing detectors tend to converge toward a common distribution that characterizes human-authored text. Consequently, if a paraphraser is guided to evade detection by a well-trained detector, its outputs will naturally align more closely with this shared, human-like distribution."*
- **Reported headline:** 64.49% reduction in detection on RADAR, 98.96% on Fast-DetectGPT vs. simple paraphrasing, using OpenAI-RoBERTa-Large as guide.

### 2. DIPPER — `martiansideofthemoon/ai-detection-paraphrases`
- **Paper:** Krishna et al., *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense*, NeurIPS 2023 — [arXiv 2303.13408](https://arxiv.org/abs/2303.13408)
- **Repo:** https://github.com/martiansideofthemoon/ai-detection-paraphrases (~195 ★) + mirror at `google-research/google-research/tree/master/dipper`
- **What it does:** 11B-param "Controllable Discourse Paraphraser" with two control codes (lexical diversity, order diversity, both 0–100) and optional context conditioning. Paragraph-scale rewriting.
- **README quote:** *"Our model uses `` ... `` tags instead of ``<sent>`` ... ``</sent>`` tags… The lexical and order diversity codes used by the actual model correspond to 'similarity' rather than 'diversity'."*
- **Headline:** Drops DetectGPT from 70.3% → 4.6% accuracy; defeats GPTZero, OpenAI classifier, and watermark detection. Retrieval-based defense recovers 80–97% at 1% FPR.

### 3. HMGC — `zhouying20/HMGC`
- **Paper:** Zhou, He, Sun, *Humanizing Machine-Generated Content: Evading AI-Text Detection through Adversarial Attack*, COLING 2024 — [arXiv 2404.01907](https://arxiv.org/abs/2404.01907)
- **Repo:** https://github.com/zhouying20/HMGC (~59 ★, Apache 2.0)
- **What it does:** Framework for minor adversarial perturbations (white-box + black-box) in MGT. Introduces the "DualIR" attacking method reused by TH-Bench.
- **Headline:** Compromises detectors in ~10 seconds of attack compute; iterative adversarial training partially restores robustness but does not close the gap.

### 4. RAFT — `JamesLWang/RAFT`
- **Paper:** Wang, Li, Yang, Mao, *RAFT: Realistic Attacks to Fool Text Detectors*, EMNLP 2024 — [arXiv 2410.03658](https://arxiv.org/abs/2410.03658)
- **Repo:** https://github.com/JamesLWang/RAFT
- **What it does:** Black-box word-substitution attack. Uses an auxiliary LLM embedding to pick words to perturb, and a separate LLM to propose POS-consistent candidates.
- **README quote:** *"From the substitution candidates, we choose the one that is part-of-speech consistent with the original text and decreases the LLM detection score against the target detector the most."*
- **Headline:** Up to 99% success across SQuAD/XSum/Abstract datasets against logprob, RoBERTa, DetectGPT, Ghostbuster, Fast-DetectGPT detectors; manual eval reports outputs are "indistinguishable from human-written text."

### 5. AuthorMist — (HF model only, paper on arXiv)
- **Paper:** *AuthorMist: Evading AI Text Detectors with Reinforcement Learning*, 2025 — [arXiv 2503.08716](https://arxiv.org/abs/2503.08716)
- **Model:** `authormist/authormist-originality` (Qwen2.5-3B-Instruct base) on HuggingFace; paraphraser fine-tuned via GRPO with detector APIs as reward.
- **What it does:** RL-trained paraphraser that uses GPTZero / Originality.ai / WinstonAI scores as the reward signal.
- **Headline:** 78.6%–96.2% attack success against individual commercial detectors while keeping semantic similarity >0.94. *(Note: paper code not publicly released at time of writing; only the model artifact and paper are open.)*

### 5b. TempParaphraser — `HJJWorks/TempParaphraser`
- **Paper:** Huang et al., *TempParaphraser: "Heating Up" Text to Evade AI-Text Detection through Paraphrasing*, EMNLP 2025 — [aclanthology.org/2025.emnlp-main.1607](https://aclanthology.org/2025.emnlp-main.1607/)
- **Repo:** https://github.com/HJJWorks/TempParaphraser
- **What it does:** Simulates high-temperature sampling by generating multiple normal-temperature paraphrases and selecting the most diverse. Evades curvature-based detectors (which rely on low-entropy regions) without needing access to source model logits.
- **Headline:** Average 82.5% reduction in detector accuracy while preserving text quality across tested detectors.

### 6. TH-Bench — `DrenfongWong/TH-Bench`
- **Paper:** *TH-Bench: Evaluating Evading Attacks via Humanizing AI Text on Machine-Generated Text Detectors*, 2025 — [arXiv 2503.08708](https://arxiv.org/abs/2503.08708)
- **Repo:** https://github.com/DrenfongWong/TH-Bench (fork of MGTBench-2.0)
- **What it does:** Unified benchmark across 6 humanization attacks × 13 detectors × 6 datasets × 11 LLMs, measuring *evading effectiveness, text quality, and compute overhead* simultaneously.
- **README quote (attack prompt baseline):** *"Your task is to rewrite the below article which must satisfy the following conditions: Keeping the semantic meaning of the new article unchanged; The new article should be classified as human-written. Only output the new article without anything else."*
- **Headline finding:** *No single evading attack wins on all three axes.* Trade-offs between detector evasion, fluency, and cost are unavoidable — this is a load-bearing insight for anyone building a humanizer product.

---

## Authorship / Style Obfuscation (humanizing by changing *who* the text sounds like)

### 7. StyleRemix — `jfisher52/StyleRemix`
- **Paper:** Fisher et al., *StyleRemix: Interpretable Authorship Obfuscation via Distillation and Perturbation of Style Elements*, EMNLP 2024 — [arXiv 2408.15666](https://arxiv.org/abs/2408.15666)
- **Repo:** https://github.com/jfisher52/StyleRemix (Apache 2.0, Llama-3 8B base) + [HF demo](https://huggingface.co/spaces/hallisky/StyleRemix)
- **What it does:** Multiple LoRA adapters, one per style axis (formality, length, sarcasm, etc.). Compose them to rewrite text while preserving content. Interpretable because each adapter has a named axis.
- **Datasets released:** AuthorMix (30K texts, 14 authors, 4 domains) and DiSC (1.5K parallel texts across 7 style axes × 16 directions).

### 8. TinyStyler — `zacharyhorvitz/TinyStyler`
- **Paper:** *TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings*, EMNLP 2024 Findings
- **Repo:** https://github.com/zacharyhorvitz/TinyStyler
- **What it does:** 800M-param style-transfer model conditioned on authorship embeddings. Trained via unsupervised reconstruction; does few-shot style transfer at inference by averaging target-author embeddings.

### 9. StyleTunedLM — `cauchy221/StyleTunedLM`
- **Paper:** *Customizing Large Language Model Generation Style using Parameter-Efficient Finetuning*
- **Repo:** https://github.com/cauchy221/StyleTunedLM
- **What it does:** LoRA fine-tuning on Project Gutenberg authors (10 authors packaged). Ships evaluation for linguistic alignment and style-embedding alignment.

### 10. personalized-gen — `balhafni/personalized-gen`
- **Paper:** *Personalized Text Generation with Fine-Grained Linguistic Control*, EACL 2024
- **Repo:** https://github.com/balhafni/personalized-gen
- **What it does:** Prefix-tuning on Pythia with fine-grained linguistic attributes (lexical richness, sentence length distribution, etc.) for controllable personalization.

---

## Human-Likeness Metrics (what you measure to *prove* humanization worked)

### 11. MAUVE — `krishnap25/mauve`
- **Paper:** Pillutla et al., *MAUVE: Measuring the Gap Between Neural Text and Human Text using Divergence Frontiers*, NeurIPS 2021 (**Outstanding Paper Award**); follow-up JMLR 2023 — [arXiv 2102.01454](https://arxiv.org/abs/2102.01454)
- **Repo:** https://github.com/krishnap25/mauve (~309 ★, `pip install mauve-text`) + experiments at `krishnap25/mauve-experiments`
- **What it does:** KL-divergence-based frontier integral between two text distributions (human vs. model) in a quantized embedding space (default: GPT-2 large hidden states, k-means buckets). Scalar score in [0, 1], larger = more human-like.
- **README quote:** *"MAUVE is best suited for relative comparisons while the absolute MAUVE score is less meaningful… Each distribution must contain at least a few thousand samples (we use 5000 each)."*
- **Practical caveat lifted from README:** Needs ~5K samples per side; variance on subtle differences (e.g., comparing nucleus-sampling variants) is large — MAUVE is best for coarse regressions, not fine tuning loops.

### 12. HUSE — `hughbzhang/HUSE`
- **Paper:** Hashimoto, Zhang, Liang, *Unifying Human and Statistical Evaluation for Natural Language Generation*, NAACL 2019
- **Repo:** https://github.com/hughbzhang/HUSE
- **What it does:** Defines score = 2 × error-rate of distinguishing (human judgment, p_model) pairs. Combines human quality ratings with statistical (perplexity) diversity in a single classifier.
- **Key finding cited in the paper:** Annealing / quality-boosting decoding strategies *decrease* HUSE because they collapse diversity — evidence that pure human eval is fooled by low-diversity high-quality samples.

### 13. (Meta) Burstiness / Perplexity / Entropy collection — `hrdikshrma/LLMMetricsResearch`
- **Repo:** https://github.com/hrdikshrma/LLMMetricsResearch
- **What it does:** Aggregates the stylometric features commonly used to distinguish human vs. machine text: perplexity, entropy, burstiness, vocabulary richness. Useful as a feature-engineering starting point rather than a peer-reviewed artifact.
- **Cross-cutting note:** Several 2025 papers (e.g., on diffusion LMs) document that modern LLM output has *lower* perplexity than human text — the old "high perplexity = human" heuristic has inverted, and humanizers that only raise perplexity overshoot.

---

## Detectors That Humanizers Must Beat (and thus ship with evaluation code)

### 14. DetectGPT — `eric-mitchell/detect-gpt`
- **Paper:** Mitchell et al., *DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature*, ICML 2023 — [arXiv 2301.11305](https://arxiv.org/abs/2301.11305)
- **Repo:** https://github.com/eric-mitchell/detect-gpt
- **Core idea:** Machine-generated text sits at negative-curvature regions of the source model's log-probability. Perturb with T5, measure the curvature.

### 15. Fast-DetectGPT — `baoguangsheng/fast-detect-gpt`
- **Paper:** ICLR 2024 follow-up to DetectGPT
- **Repo:** https://github.com/baoguangsheng/fast-detect-gpt
- **Headline:** 340× speedup over DetectGPT, 0.9887 AUROC on 5-model benchmark. Supports Llama3-8B / Falcon-7B / GPT-J-6B as scorer.

### 16. Ghostbuster — `vivek3141/ghostbuster`
- **Paper:** Verma, Fleisig, Tomlin, Klein, *Ghostbuster: Detecting Text Ghostwritten by Large Language Models*, NAACL 2024
- **Repo:** https://github.com/vivek3141/ghostbuster (~179 ★)
- **Core idea:** Run text through several weaker LMs (unigram → GPT-3 davinci), structured search over feature combinations, train a linear classifier. Does **not** need token probs from the target model — true black-box.
- **Headline:** 99.0 F1 cross-domain; +7.5 F1 domain-generalization over DetectGPT/GPTZero. Ships 3 benchmark datasets (student essays, creative writing, news).

### 17. RADAR — `IBM/RADAR`
- **Paper:** Hu, Chen, Ho, *RADAR: Robust AI-Text Detection via Adversarial Learning*, NeurIPS 2023
- **Repo:** https://github.com/IBM/RADAR (~73 ★, Apache 2.0) + HF model `TrustSafeAI/RADAR-Vicuna-7B`
- **Core idea:** Co-train a paraphraser (attacker) and a RoBERTa-large detector (defender) in an adversarial loop. Explicitly targets paraphrase robustness. Note: this is the exact detector that Adversarial Paraphrasing #1 breaks.

### 18. Binoculars — `ahans30/Binoculars`
- **Paper:** Hans et al., *Spotting LLMs with Binoculars*, ICML 2024 — [arXiv 2401.12070](https://arxiv.org/abs/2401.12070)
- **Repo:** https://github.com/ahans30/Binoculars (~363 ★)
- **Core idea:** Zero-shot. Contrast log-perplexity from an "observer" LM with next-token predictions from a "performer" LM. Requires *no* training data.
- **Headline:** >90% detection of ChatGPT at 0.01% FPR; 94.92% accuracy on news.

### 19. Raidar — `cvlab-columbia/RaidarLLMDetect`
- **Paper:** *Raidar: geneRative AI Detection viA Rewriting*, ICLR 2024 — [arXiv 2401.12970](https://arxiv.org/abs/2401.12970)
- **Repo:** https://github.com/cvlab-columbia/RaidarLLMDetect
- **Core idea:** Ask an LLM to rewrite the text; measure edit distance. LLMs edit human text more than AI text (they "agree" with AI output), so small edit distance ⇒ likely AI. Works on pure symbols — no token-prob access needed.
- **Headline:** +29 F1 on low-baseline detectors across news/essays/code/Yelp/arXiv.

### 20. SemStamp — `abehou/SemStamp`
- **Paper:** Semantic watermarking, NAACL 2024 (k-SemStamp variant in ACL 2024 Findings)
- **Repo:** https://github.com/abehou/SemStamp
- **Core idea:** Watermark at the *semantic* level using LSH / k-means partitions of the sentence embedding space, so paraphrase attacks that preserve meaning also preserve the watermark.

### 21. SynthID-Text — `google-deepmind/synthid-text`
- **Paper:** Google DeepMind 2024 release, accompanying *Nature* publication
- **Repo:** https://github.com/google-deepmind/synthid-text (~813 ★, Apache 2.0)
- **Core idea:** Production watermark — adjusts token sampling probabilities at generation time; detection uses either a training-free Weighted Mean detector or a trained Bayesian detector.
- **Note:** Core library is on PyPI and already integrated into HF Transformers' watermarking hooks. The only major industry-shipped watermark with open code.

### 22. OpenAI RoBERTa detector (legacy, widely reused)
- Referenced everywhere, checkpoints hosted at `openaipublic.azureedge.net/gpt-2/detector-models/v1/`. Used as a proxy detector in RAFT, as the guidance detector that leaks the "universal attack" property in Adversarial Paraphrasing #1, etc. Not itself a paper-with-code artifact but every humanizer ships integration code for it.

---

## Benchmarks / Meta-Evaluation

### 23. MGTBench — `xinleihe/MGTBench`
- Repo: https://github.com/xinleihe/MGTBench (~162 ★)
- Bundles: log-likelihood, Rank, Log-Rank, Entropy, GLTR, DetectGPT, LRR, NPR (metric-based); OpenAI Detector, ChatGPT Detector, ConDA, GPTZero, LM Detector (model-based). Essay/WritingPrompts/Reuters datasets.

### 24. M4 / M4GT-Bench — `mbzuai-nlp/M4` and `mbzuai-nlp/M4GT-Bench`
- Papers: *M4: Multi-generator, Multi-domain, and Multi-lingual Black-Box MGT Detection* (EACL 2024 Best Resource Paper); M4GT-Bench (ACL 2024)
- Multilingual, multi-domain benchmark covering same-generator/cross-domain, cross-generator/same-domain, multilingual, temporal, and zero-shot settings. Underpinned SemEval-2024 Task 8.

### 25. APT-Eval — `ShoumikSaha/ai-polished-text`
- **Paper:** Saha & Feizi, *Almost AI, Almost Human: The Challenge of Detecting AI-Polished Writing*, ACL 2025 Findings — [arXiv 2502.15666](https://arxiv.org/abs/2502.15666)
- **Repo:** https://github.com/ShoumikSaha/ai-polished-text (built on `liamdugan/raid`)
- **What it does:** 15K+ AI-polished text samples across GPT-4o / Llama3.1-70B / Llama3-8B / Llama2-7B / DeepSeek-V3 at varying *polish degrees* (percentage and degree based).
- **Covered in NYT, "The Cheat Sheet," Plagiarism Today** — the most mainstream-visible paper in this cluster.
- **Key finding (paper abstract, via README):** *"Detectors frequently flag even minimally polished text as AI-generated, struggle to differentiate between degrees of AI involvement, and exhibit biases against older and smaller models."* ← Directly relevant to product UX: *any* humanizer that "just polishes" still trips commercial detectors.

### 26. human_detectors — `jenna-russell/human_detectors`
- Repo bundling *human* detector annotations (expert labels, confidence scores, explanations) alongside machine-detector outputs. Rare dataset: what do humans themselves notice when they correctly flag AI text?

### 27. DivEye — `IBM/diveye`
- **Paper:** Basani, Chen et al., *Diversity Boosts AI-Generated Text Detection*, arXiv:2509.18880, TMLR 2026 — [arxiv.org/abs/2509.18880](https://arxiv.org/abs/2509.18880)
- **Repo:** https://github.com/IBM/diveye + HF demo at `pinyuchen/Diveye_AI_text_detector`
- **What it does:** Surprisal-variance detector. Measures how intra-document unpredictability fluctuates; LLM text has lower rhythmic variance than human text. Zero-shot; no fine-tuning required.
- **Headline:** Outperforms existing zero-shot detectors by up to 33.2%; improves fine-tuned baselines by up to 18.7% as auxiliary signal; robust to paraphrasing attacks.
- **Humanizer implication:** a humanizer that explicitly widens its per-sentence surprisal variance will evade DivEye. The repo ships interpretability hooks showing *where* in the text the flag fires — useful for targeted rewriting.

---

## Patterns, Trends, and Gaps

### Patterns
1. **Four-camp architecture is stable.** The ecosystem cleanly separates into (i) humanizers/attackers (DIPPER, RAFT, HMGC, Adversarial Paraphrasing, AuthorMist), (ii) detectors (DetectGPT, Fast-DetectGPT, Ghostbuster, RADAR, Binoculars, Raidar), (iii) watermarks (SynthID-Text, SemStamp), (iv) benchmarks + metrics (MAUVE, HUSE, TH-Bench, APT-Eval, M4, MGTBench). Any product effort should pick adversary and defender from opposite camps and measure on (iv).
2. **Detector guidance is a universal attack primitive.** Adversarial Paraphrasing (2025) and AuthorMist (2025) both converge on: use a detector score as a reward/guide. This replaces handcrafted paraphrasing prompts and is consistently the strongest reported attack.
3. **Decomposed, interpretable style axes are an emerging alternative to one-shot paraphrasing.** StyleRemix's per-axis LoRAs and TinyStyler's authorship embeddings are the current state of the art when *controllability* matters more than pure evasion.
4. **Detection and humanization share the same infrastructure.** TH-Bench, APT-Eval, M4GT-Bench, and MGTBench2 are forks or extensions of each other. Building on these saves weeks and is now the community default.
5. **Zero-shot, training-free methods win disproportionately.** Binoculars (zero-shot detector) and Adversarial Paraphrasing (training-free attack) are the two most talked-about 2024–2025 results. Infrastructure cost is a competitive moat.

### Trends (2023 → 2026)
- Early work (2023): direct paraphrase attacks (DIPPER) and curvature-based detectors (DetectGPT).
- Mid (2024): adversarially-trained detectors (RADAR), zero-shot contrastive detectors (Binoculars), rewriting-based detectors (Raidar), and feature-search detectors (Ghostbuster).
- Late (2024–2025): RL-trained humanizers (AuthorMist, StealthRL), detector-guided paraphrasers (Adversarial Paraphrasing), and benchmarks that explicitly measure the *three-way* trade-off between evasion, fluency, and compute (TH-Bench). TempParaphraser (EMNLP 2025) adds temperature-simulation as a new evasion axis.
- 2025–2026: surprisal-variance detectors (DivEye, TMLR 2026) and hardness-aware benchmarks (SHIELD, arXiv:2507.15286) shift the goalposts; multi-axis stylistic analysis (Rallapalli et al., 2026) confirms decoding strategy itself is a stylistic signal.
- The "AI-polished" framing (APT-Eval, 2025) remains the most product-relevant: users don't want full machine-generated text rewritten — they want their *own* draft lightly edited without being flagged.

### Gaps (opportunity surface for the Unslop project)
1. **No strong "think like a human" work** — every open-source artifact targets *surface text*. No paper-with-code tackles humanizing the underlying *reasoning trace* or chain-of-thought. This is a genuine whitespace.
2. **Metrics still measure distributional match, not perceived humanness.** MAUVE and HUSE both operate at distribution/classification level. No widely-adopted open metric measures *subjective humanness* from a lay reader (vs. expert annotators in `human_detectors`).
3. **No released code for AuthorMist itself** (only the HF model). An open RL-humanizer with detector-API rewards would immediately become a reference implementation.
4. **Commercial humanizers are ahead of papers.** HumanWrite, Pangram, Originality.ai, Undetectable.AI have product maturity that academic repos do not match. The TH-Bench paper is the first to systematically compare against them, and it finds no dominant attack — there is room for a well-engineered open-source humanizer that wins on the three-axis trade-off.
5. **Multi-detector ensembles are under-attacked.** Most papers evade one detector at a time. StealthRL (arXiv:2602.08934) is the clearest example targeting multi-detector ensembles and confirms transferability — this is now the expected threat model rather than an edge case.
6. **Human-likeness on non-English text is thin.** M4 covers multilingual detection, but humanization work is overwhelmingly English-first; cross-lingual humanization is essentially unstudied in open source.
7. **No open humanizer targets surprisal-variance.** DivEye (`IBM/diveye`, TMLR 2026) identifies intra-document rhythmic unpredictability as the next key detection signal, but no humanizer paper or repo yet explicitly optimizes for this. First-mover opportunity.
8. **SHIELD hardness benchmark is unused by humanizer papers.** The SHIELD framework (arXiv:2507.15286) enables hardness-stratified evaluation, but existing humanizer repos all report against flat benchmarks. Adopting SHIELD would surface which attacks work only on easy cases.

---

## Sources

- chengez/Adversarial-Paraphrasing README — https://github.com/chengez/Adversarial-Paraphrasing
- martiansideofthemoon/ai-detection-paraphrases README — https://github.com/martiansideofthemoon/ai-detection-paraphrases
- krishnap25/mauve README — https://github.com/krishnap25/mauve
- DrenfongWong/TH-Bench README — https://github.com/DrenfongWong/TH-Bench
- ShoumikSaha/ai-polished-text README (APT-Eval / ACL 2025) — https://github.com/ShoumikSaha/ai-polished-text
- JamesLWang/RAFT README — https://github.com/JamesLWang/RAFT
- IBM/RADAR README — https://github.com/IBM/RADAR
- ahans30/Binoculars README — https://github.com/ahans30/Binoculars
- hughbzhang/HUSE — https://github.com/hughbzhang/HUSE
- zhouying20/HMGC — https://github.com/zhouying20/HMGC
- jfisher52/StyleRemix — https://github.com/jfisher52/StyleRemix
- eric-mitchell/detect-gpt — https://github.com/eric-mitchell/detect-gpt
- baoguangsheng/fast-detect-gpt — https://github.com/baoguangsheng/fast-detect-gpt
- vivek3141/ghostbuster — https://github.com/vivek3141/ghostbuster
- cvlab-columbia/RaidarLLMDetect — https://github.com/cvlab-columbia/RaidarLLMDetect
- abehou/SemStamp — https://github.com/abehou/SemStamp
- google-deepmind/synthid-text — https://github.com/google-deepmind/synthid-text
- mbzuai-nlp/M4 and mbzuai-nlp/M4GT-Bench — https://github.com/mbzuai-nlp/M4
- xinleihe/MGTBench — https://github.com/xinleihe/MGTBench
- zacharyhorvitz/TinyStyler — https://github.com/zacharyhorvitz/TinyStyler
- cauchy221/StyleTunedLM — https://github.com/cauchy221/StyleTunedLM
- balhafni/personalized-gen — https://github.com/balhafni/personalized-gen
- AuthorMist paper — https://arxiv.org/abs/2503.08716
- Papers with Code: *Are AI-Generated Text Detectors Robust to Adversarial Perturbations?* — https://paperswithcode.com/paper/are-ai-generated-text-detectors-robust-to
- jenna-russell/human_detectors — https://github.com/jenna-russell/human_detectors
- HJJWorks/TempParaphraser — https://github.com/HJJWorks/TempParaphraser (EMNLP 2025)
- IBM/diveye — https://github.com/IBM/diveye (TMLR 2026, arXiv:2509.18880)
- SHIELD benchmark paper — https://arxiv.org/abs/2507.15286
