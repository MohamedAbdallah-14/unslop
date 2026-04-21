# Natural Language Quality — Academic & Scholarly

> Research angle: **A — Academic & Scholarly** grounding for the Unslop project
> (humanizing AI output). Focus: decoding strategies, fluency / coherence / diversity,
> burstiness, perplexity, repetition penalties, human-likeness metrics (MAUVE,
> BERTScore, HLB), and adversarial humanization. Venues prioritized: arXiv, ACL,
> EMNLP, NAACL, ICLR, NeurIPS, ICML, TACL, TMLR.

## Executive Summary

The academic literature on "natural" neural text generation is driven by one
persistent observation: likelihood-trained language models, decoded greedily,
produce text that is **statistically unlike human writing** — lower perplexity,
flatter sentence-length variance (low burstiness), narrower vocabulary, and
higher n-gram repetition. Almost every advance in this space is an attempt to
close that distributional gap, either at training time (unlikelihood,
contrastive objectives), at decoding time (nucleus, typical, contrastive,
min-p, eta, Mirostat, contrastive search), or at evaluation time (MAUVE,
BERTScore, HLB).

Five threads matter for a humanization product:

1. **Decoding dominates quality.** Holtzman et al. (ICLR 2020) and every
   follow-up show that the *same* model can generate either degenerate slop or
   human-like prose depending solely on the decoding algorithm. Humanization
   pipelines that ignore the sampler are leaving the largest lever on the table.
2. **"Human-like" has a specific information-theoretic signature.** Meister et
   al.'s *locally typical sampling* (TACL / EMNLP 2022) argues that humans pick
   tokens whose information content sits near the model's *conditional entropy*,
   not at the mode. This is the cleanest theoretical account of why flat, high-
   probability AI text reads as "off."
3. **Distributional evaluation has matured.** MAUVE (Pillutla et al., NeurIPS
   2021) compares the full distribution of generated vs. human text via
   quantized embedding divergence; BERTScore (Zhang et al., ICLR 2020) grounds
   semantic overlap; HLB (Duan et al., 2024) adds psycholinguistic probes. No
   single metric is sufficient — top labs triangulate.
4. **Burstiness and perplexity are now adversarial signals.** DetectGPT
   (Mitchell et al., ICML 2023) and Ghostbuster (Verma et al., NAACL 2024) use
   perplexity curvature and multi-model probability features to detect AI text.
   Humanization that only raises vocabulary diversity without also restoring
   perplexity variance and burstiness is detectable.
5. **Adversarial humanization is an emergent research subfield.** Cheng et
   al.'s *Adversarial Paraphrasing* (2025) formalizes detector-guided rewriting
   and shows >85 % reduction in true-positive rates across detectors — setting
   both the state of the art and the ethical stakes for Unslop.

## Sources

---

### 1. The Curious Case of Neural Text Degeneration

- **Authors:** Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi
- **Year / Venue:** 2020, **ICLR 2020** (arXiv:1904.09751)
- **URL:** https://arxiv.org/abs/1904.09751
- **Core claim:** Likelihood maximization (beam search, greedy) produces bland
  and repetitive text because it oversamples the high-probability tail that is
  statistically *unlike* human writing; truncating to a dynamic probability
  nucleus recovers human-like diversity.
- **Techniques:** Introduces **Nucleus (Top-p) Sampling**; measures
  self-BLEU, repetition rate, Zipf coefficient, and probability under the model
  against human text.
- **Takeaways for humanization:**
  - Human text is *not* the most likely text under an LM — a foundational
    insight for any "make this sound human" pipeline.
  - Plot of probability-per-token shows humans oscillate between high- and
    low-probability tokens; AI plateaus. This is the mathematical origin of
    low burstiness.
  - Nucleus sampling is still the production default for a reason — but it
    is no longer state-of-the-art (see typical, contrastive, min-p below).
- **Summary (2–3 sentences):** Holtzman et al. demonstrate the paradox that
  likelihood-trained models generate poor text when decoded by likelihood, and
  show that the surprising distributional gap between human and machine text
  can be largely closed by truncating to the top-p probability mass.
  Nucleus sampling becomes the de facto baseline for open-ended generation.
- **Key quote:** *"Using likelihood as a decoding objective leads to text that
  is bland and strangely repetitive… decoding strategies alone can dramatically
  effect the quality of machine text, even when generated from exactly the same
  neural language model."*

---

### 2. Neural Text Generation with Unlikelihood Training

- **Authors:** Sean Welleck, Ilia Kulikov, Stephen Roller, Emily Dinan,
  Kyunghyun Cho, Jason Weston
- **Year / Venue:** 2020, **ICLR 2020** (arXiv:1908.04319)
- **URL:** https://arxiv.org/abs/1908.04319
- **Core claim:** The likelihood *objective itself* is at fault — not just the
  decoder. Models trained with pure MLE assign too much mass to repeats and
  frequent tokens; adding an *unlikelihood* term that pushes down probability
  on undesired continuations gives less repetitive, less dull text under
  standard greedy or beam decoding.
- **Techniques:** Token-level and sequence-level unlikelihood loss; repetition
  penalty framed as a training objective instead of a decoder hack.
- **Takeaways for humanization:**
  - Repetition is a *training pathology*, not merely a sampling pathology.
  - Unlikelihood-trained models beat nucleus sampling in human evaluations,
    suggesting the best humanization combines the two.
- **Summary:** Welleck et al. reframe neural text degeneration as an objective
  problem and introduce unlikelihood training, which penalizes the model when
  it would repeat tokens or n-grams. The method outperforms nucleus sampling
  and beam blocking in human evals while preserving perplexity.
- **Key quote:** *"The likelihood objective itself is at fault, resulting in a
  model that assigns too much probability to sequences containing repeats and
  frequent words, unlike those from the human training distribution."*

---

### 3. MAUVE: Measuring the Gap Between Neural Text and Human Text using Divergence Frontiers

- **Authors:** Krishna Pillutla, Swabha Swayamdipta, Rowan Zellers, John
  Thickstun, Sean Welleck, Yejin Choi, Zaid Harchaoui
- **Year / Venue:** 2021, **NeurIPS 2021** (Outstanding Paper)
- **URL:** https://papers.nips.cc/paper/2021/hash/260c2432a0eecc28ce03c10dadc078a4-Abstract.html
- **Core claim:** Human-likeness of generated text is best measured
  distributionally, as a KL-divergence frontier between the model distribution
  and the human distribution in a quantized embedding space.
- **Techniques:** Quantized GPT-2 embeddings, KL frontier between P_model and
  P_human, area-under-curve scalar, captures both Type-I (degenerate
  repetitions) and Type-II (missing human modes) errors.
- **Takeaways for humanization:**
  - A good humanizer should move MAUVE toward 1.0 — not just improve BLEU or
    perplexity.
  - The two-error framing (too repetitive vs. too narrow) is a useful product
    rubric: check both axes in eval dashboards.
- **Summary:** MAUVE introduces a scalable, correlate-with-human-judgment
  metric that directly compares the full distribution of model output to human
  writing. It has since become a standard evaluation for open-ended generation
  and is sensitive to the exact degeneracies that humanizers target.
- **Key quote:** *"Mauve identifies known properties of generated text, scales
  naturally with model size, and correlates with human judgments, with fewer
  restrictions than existing distributional evaluation metrics."*

---

### 4. BERTScore: Evaluating Text Generation with BERT

- **Authors:** Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q. Weinberger,
  Yoav Artzi
- **Year / Venue:** 2020, **ICLR 2020** (arXiv:1904.09675)
- **URL:** https://arxiv.org/abs/1904.09675
- **Core claim:** Token-level cosine similarity in contextual BERT embedding
  space correlates with human judgments better than n-gram metrics (BLEU,
  METEOR, ROUGE), especially under paraphrase.
- **Techniques:** Pairwise contextual embedding cosine similarity, IDF
  weighting, precision/recall/F1 formulation.
- **Takeaways for humanization:**
  - Essential as a semantic-preservation guardrail: a humanized rewrite must
    still match source meaning. BERTScore ≥ ~0.85 is a common floor.
  - Unlike BLEU, BERTScore rewards paraphrase — the exact operation a
    humanizer performs.
- **Summary:** BERTScore replaces surface-form n-gram matching with cosine
  similarity over contextual embeddings, giving a paraphrase-robust metric that
  correlates with humans across 363 MT/captioning systems.
- **Key quote:** *"BERTScore correlates better with human judgments and
  provides stronger model selection performance than existing metrics."*

---

### 5. Locally Typical Sampling

- **Authors:** Clara Meister, Tiago Pimentel, Gian Wiher, Ryan Cotterell
- **Year / Venue:** 2022 preprint → **TACL 2023 / EMNLP 2022**
- **URL:** https://arxiv.org/abs/2202.00666
- **Core claim:** Humans communicate efficiently — each token they pick has
  information content close to the model's *conditional entropy*. Sampling
  should therefore target tokens near expected information, not near the mode.
- **Techniques:** Typical set defined via |−log p(x) − H(p)| ≤ τ; truncate to
  the τ-typical set before renormalizing and sampling.
- **Takeaways for humanization:**
  - The strongest information-theoretic justification for why high-probability
    LLM text reads as robotic.
  - Typical sampling consistently reduces degenerate repetition while matching
    nucleus on quality — often a better default than top-p for long-form.
- **Summary:** Meister et al. derive a decoding criterion from Shannon-optimal
  communication: humans pick words whose information content is near the
  expected value, not the minimum. Locally typical sampling implements this
  criterion and reduces repetition competitively with nucleus sampling on
  summarization and story generation.
- **Key quote:** *"We posit that humans produce language with the goal of
  transmitting information efficiently and with minimum error... each word's
  information content [should be] close to the expected information content,
  i.e., the conditional entropy of our model."*

---

### 6. A Contrastive Framework for Neural Text Generation (SimCTG)

- **Authors:** Yixuan Su, Tian Lan, Yan Wang, Dani Yogatama, Lingpeng Kong,
  Nigel Collier
- **Year / Venue:** 2022, **NeurIPS 2022 (Spotlight)** (arXiv:2202.06417)
- **URL:** https://arxiv.org/abs/2202.06417
- **Core claim:** Degeneration stems from **anisotropic** token embeddings —
  representations cluster in a narrow cone with cosine similarity > 0.95 —
  which biases the model toward repeating itself. A contrastive training
  objective spreads tokens out; a contrastive search decoder exploits this.
- **Techniques:** SimCTG contrastive loss + Contrastive Search decoding (degen
  penalty balancing model confidence and token-level novelty).
- **Takeaways for humanization:**
  - Anisotropy is a mechanistic explanation for repetition; important mental
    model even if anisotropy turns out to be GPT-2–specific (see #7).
  - Contrastive search is practically useful out-of-the-box on modern LMs.
- **Summary:** Su et al. tie neural text degeneration to anisotropic
  representation geometry, then jointly propose a contrastive training
  objective and a decoding algorithm (contrastive search) that penalizes
  repetition at the representation level. Human and automatic metrics both
  improve across two languages.
- **Key quote:** *"Neural language models often generate text that is
  anisotropically distributed, which is the root cause of model degeneration."*

---

### 7. Contrastive Search Is What You Need For Neural Text Generation

- **Authors:** Yixuan Su, Nigel Collier
- **Year / Venue:** 2023, **TMLR** (arXiv:2210.14140)
- **URL:** https://arxiv.org/abs/2210.14140
- **Core claim:** Walks back part of SimCTG: across 16 languages, most LMs are
  *naturally isotropic*; the anisotropy problem is specific to English
  GPT-2-small/medium. But contrastive *search* still works on off-the-shelf
  LMs without any contrastive training.
- **Techniques:** Large-scale isotropy audit (16 languages); decoding-only
  contrastive search on pretrained LMs.
- **Takeaways for humanization:**
  - You do not need a specially trained model — decoding alone can reach
    human-level quality on 12/16 languages.
  - Scientific integrity signal: the community willingly corrects itself,
    which is useful when citing older repetition-penalty literature.
- **Summary:** A follow-up that overturns the anisotropy premise of SimCTG
  while keeping contrastive search as a top-tier decoder. Human evaluators
  rate its output comparable to human writing on 12 of 16 languages.
- **Key quote:** *"On 12 out of the 16 evaluated languages, contrastive search
  performs comparably with human-level performances as judged by human
  evaluations."*

---

### 8. Contrastive Decoding: Open-ended Text Generation as Optimization

- **Authors:** Xiang Lisa Li, Ari Holtzman, Daniel Fried, Percy Liang, Jason
  Eisner, Tatsunori Hashimoto, Luke Zettlemoyer, Mike Lewis
- **Year / Venue:** 2023, **ACL 2023** (arXiv:2210.15097)
- **URL:** https://arxiv.org/abs/2210.15097
- **Core claim:** The failure modes of LLMs (repetition, incoherence, topic
  drift) are *amplified* in smaller LMs. Decoding with the log-probability
  *difference* between a large "expert" and a small "amateur" model, subject
  to a plausibility floor, cancels out those failure modes.
- **Techniques:** Expert (OPT-13B) − Amateur (OPT-125M) log-prob subtraction;
  α-plausibility constraint; zero extra training.
- **Takeaways for humanization:**
  - An elegant, training-free way to "subtract AI-ness" from an LM's
    distribution — conceptually close to what humanization wants to do.
  - Outperforms nucleus and top-k in auto + human evals on Wikipedia, news,
    story domains.
- **Summary:** Contrastive Decoding uses a small amateur model as a contrast
  signal, emphasizing tokens that large models prefer but small models do not.
  It beats nucleus and top-k across three domains with no training and is
  cheap to deploy alongside any existing LM.
- **Key quote:** *"The failures of larger LMs (e.g., repetition, incoherence)
  are even more prevalent in smaller LMs… this difference signals which texts
  should be preferred."*

---

### 9. Truncation Sampling as Language Model Desmoothing (η-sampling / ε-sampling)

- **Authors:** John Hewitt, Christopher D. Manning, Percy Liang
- **Year / Venue:** 2022, **Findings of EMNLP 2022** (arXiv:2210.15191)
- **URL:** https://arxiv.org/abs/2210.15191
- **Core claim:** Truncation sampling should be understood as *desmoothing*
  the LM — recovering the true support of the data distribution from a
  smoothed model. Eta-sampling combines an absolute floor with an
  entropy-dependent threshold, avoiding pathological truncations like keeping
  only "Trump" after "Donald."
- **Techniques:** η-sampling: keep tokens with p > min(ε, α·exp(−H)); also
  introduces ε-sampling.
- **Takeaways for humanization:**
  - Top-p can silently truncate legitimate multi-mode distributions; eta
    preserves valid alternatives.
  - Entropy-aware truncation foreshadows modern adaptive samplers (min-p,
    entropix).
- **Summary:** Hewitt et al. reframe top-p and top-k as approximate solutions
  to a desmoothing problem and propose η-sampling, which uses an
  entropy-dependent threshold. On long English generations, eta beats top-p,
  typical, and ε-sampling on plausibility and repetition.
- **Key quote:** *"We provide theoretical foundations for sampling algorithms,
  arguing that existing algorithms can be understood as approximations to a
  smoothed model."*

---

### 10. Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs

- **Authors:** Minh Nguyen, Andrew Baker, Clement Neo, Allen Roush, Andreas
  Kirsch, Ravid Shwartz-Ziv
- **Year / Venue:** 2024 preprint → **ICLR 2025** (arXiv:2407.01082)
- **URL:** https://arxiv.org/abs/2407.01082
- **Core claim:** Scale the truncation threshold by the top token's
  probability: when the model is confident (sharp distribution), truncate
  tightly; when uncertain (flat distribution), keep more options. Enables
  high-temperature sampling without incoherence.
- **Techniques:** min-p threshold = p_min × p_top; evaluated on GPQA, GSM8K,
  AlpacaEval Creative Writing across 1B–123B models.
- **Takeaways for humanization:**
  - Unlocks creative / "bursty" outputs at high temperature without sacrificing
    coherence — directly useful for varying sentence rhythm.
  - Already adopted in HF Transformers, vLLM, llama.cpp; deployment-ready.
- **Summary:** Min-p sampling dynamically adjusts its truncation threshold
  based on model confidence, letting high-temperature creative settings stay
  coherent. Human raters prefer it over top-p, top-k, and η-sampling on
  creative-writing benchmarks across Mistral and Llama-3 families.
- **Key quote:** *"Min-p sampling improves both the quality and diversity of
  generated text across different model families… especially at higher
  temperatures."*

---

### 11. Mirostat: A Neural Text Decoding Algorithm That Directly Controls Perplexity

- **Authors:** Sourya Basu, Govardana Sachitanandam Ramachandran, Nitish
  Shirish Keskar, Lav R. Varshney
- **Year / Venue:** 2021, **ICLR 2021** (arXiv:2007.14966)
- **URL:** https://arxiv.org/abs/2007.14966
- **Core claim:** Humans prefer a specific perplexity range — neither too low
  ("boredom trap" → repetition) nor too high ("confusion trap" → incoherence).
  A feedback loop on top-k maintains a target surprise rate throughout
  generation.
- **Techniques:** Online estimation of tail index of Zipfian token
  distribution; adaptive k that targets a user-specified cross-entropy τ.
- **Takeaways for humanization:**
  - Directly actionable control knob: "generate at human-typical perplexity."
  - Connects perplexity stability to repetition in closed-form.
  - Heavily used in local-LLM communities (llama.cpp, text-generation-webui).
- **Summary:** Mirostat closes a feedback loop around the decoder so the
  generated sequence hits a pre-specified perplexity target, avoiding both
  repetition and drift. The paper formally ties perplexity to repetition rate
  under Zipfian token statistics.
- **Key quote:** *"Humans prefer perplexity that is neither too high nor too
  low, and cross-entropy (log of perplexity) has a near-linear relation with
  repetition."*

---

### 12. DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature

- **Authors:** Eric Mitchell, Yoonho Lee, Alexander Khazatsky, Christopher D.
  Manning, Chelsea Finn
- **Year / Venue:** 2023, **ICML 2023 (Oral)** (arXiv:2301.11305)
- **URL:** https://arxiv.org/abs/2301.11305
- **Core claim:** LLM-generated text sits at a local maximum of the model's
  log-probability function: small T5-perturbations of LLM text reliably lower
  log-prob, whereas perturbations of human text are symmetric. This curvature
  signal distinguishes machine from human text zero-shot.
- **Techniques:** Perturbation-and-probability-delta test; AUROC up to 0.95.
- **Takeaways for humanization:**
  - Humanization must not just change vocabulary; it must move text *off* the
    model's log-prob ridge. Pure paraphrase via the same LM can *fail* here.
  - Gives a concrete failure metric to optimize against.
- **Summary:** DetectGPT frames AI-text detection as probing the curvature of
  an LM's log-likelihood surface around a candidate passage. It requires no
  classifier training and outperforms supervised detectors on several
  benchmarks, setting a durable bar for humanization systems to clear.
- **Key quote:** *"Text sampled from an LLM tends to occupy regions of
  negative curvature of the model's log probability function."*

---

### 13. Ghostbuster: Detecting Text Ghostwritten by Large Language Models

- **Authors:** Vivek Verma, Eve Fleisig, Nicholas Tomlin, Dan Klein
- **Year / Venue:** 2024, **NAACL 2024** (arXiv:2305.15047)
- **URL:** https://aclanthology.org/2024.naacl-long.95/
- **Core claim:** Robust detection doesn't need access to the target LM's
  probabilities. Feeding a document through a bank of *weaker* LMs (unigram,
  trigram, non-instruction GPT-3) and searching feature combinations yields a
  linear classifier that beats DetectGPT and GPTZero by ~6 F1.
- **Techniques:** Token-probability features from multiple frozen LMs;
  structured-search over feature compositions; linear classifier head.
- **Takeaways for humanization:**
  - Raises the bar: humanizers must defeat *multi-model* probability
    signatures, not just single-LM perplexity.
  - Perplexity alone can perform *worse than random* on some domains
    (non-native English), which both limits naive detectors and the naive
    humanizers that optimize only against them.
- **Summary:** Ghostbuster demonstrates that combining features from several
  cheap, frozen language models gives a more robust AI-text detector than
  curvature-based methods and generalizes better across domains and prompt
  styles. It sets a 99 F1 ceiling that humanization must work around.
- **Key quote:** *"Perplexity alone was found to perform worse than random on
  some domains, including non-native English speaker data."*

---

### 14. HLB: Benchmarking LLMs' Humanlikeness in Language Use

- **Authors:** Xufeng Duan, Bei Xiao, Xuemei Tang, Zhenguang G. Cai
- **Year / Venue:** 2024, **arXiv:2409.15890**
- **URL:** https://arxiv.org/abs/2409.15890
- **Core claim:** Standard NLP metrics miss whether an LLM sounds human. HLB
  runs 10 classical psycholinguistic experiments (priming, Cloze, garden-path
  parsing, etc.) on 20 LLMs and on 2,000+ human participants, then measures
  *distributional similarity* between the two populations.
- **Techniques:** Psycholinguistic probe suite across sound, word, syntax,
  semantics, discourse; coding algorithm → response distribution → distance.
- **Takeaways for humanization:**
  - A humanizer should carry human *processing* signatures (e.g., garden-path
    recovery patterns), not just surface stats.
  - Ominous finding: improvements in standard benchmarks can *reduce*
    humanlikeness — benchmark-chasing is not aligned with the humanization goal.
- **Summary:** HLB imports methods from psycholinguistics to measure how
  closely LLM outputs replicate the *distributions* of human responses across
  10 language tasks. The authors find that LLM capability improvements and
  humanlikeness are not monotonically aligned and sometimes negatively
  correlated.
- **Key quote:** *"Improvements in other performance metrics did not
  necessarily lead to greater humanlikeness, and in some cases, even resulted
  in a decline."*

---

### 15. Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text

- **Authors:** Yize Cheng, Vinu Sankar Sadasivan, et al. (University of
  Maryland)
- **Year / Venue:** 2025 preprint (arXiv:2506.07001)
- **URL:** https://arxiv.org/abs/2506.07001
- **Core claim:** A training-free pipeline that uses an instruction-tuned LLM
  to paraphrase candidate text, guided at each step by signals from an AI-text
  detector, systematically transfers across detectors and reduces
  true-positive-at-1%-FPR by an average of **87.88 %**.
- **Techniques:** Detector-in-the-loop paraphrase sampling; no model training;
  transferability audits across DetectGPT, Ghostbuster, OpenAI-RoBERTa, RADAR.
- **Takeaways for humanization:**
  - Current state-of-the-art for adversarial humanization; a reference
    baseline for Unslop's evaluation harness.
  - Demonstrates that humanization is fundamentally a detector-guided
    optimization problem, not a "style transfer" problem.
- **Summary:** Cheng et al. formalize humanization as adversarial paraphrase
  guided by an off-the-shelf AI detector and show that a single attack
  transfers across most deployed detectors, including RADAR. The work
  simultaneously represents the current academic ceiling for humanization and
  a critical input for anyone building detectors or watermarks.
- **Key quote:** *"Adversarial paraphrasing guided by OpenAI-RoBERTa-Large
  reduces T@1%F by 64.49% on RADAR… achieves an average T@1%F reduction of
  87.88% across diverse detectors."*

---

### 16. Make Every Token Count: A Systematic Survey on Decoding Methods for Foundation Models *(supporting survey)*

- **Authors:** Various (systematic survey)
- **Year / Venue:** 2024, arXiv preprint (cited via ResearchGate)
- **URL:** https://arxiv.org/pdf/2410.06097
- **Core claim:** Organizes decoding into three paradigms — deterministic
  (beam/greedy), sampling (top-k, top-p, typical, min-p, η, ε), and
  contrastive (CD, contrastive search) — and argues hyperparameter tuning is
  the most neglected lever.
- **Takeaways for humanization:**
  - Useful map for product engineers who need to pick a decoder per task and
    per model family.
  - Documents that optimal settings differ across models and tasks — a
    Unslop benchmark must cover this grid.

---

### 17. A Survey on LLM-as-a-Judge

- **Authors:** Various (comprehensive survey, ~90 pages)
- **Year / Venue:** 2024 preprint → updated through 2025, **arXiv:2411.15594**
- **URL:** https://arxiv.org/abs/2411.15594
- **Core claim:** LLM-as-a-judge is now the dominant automatic evaluation paradigm for NLG, but persistent biases — position (~40% GPT-4 inconsistency when A/B order is flipped), verbosity (~15% inflation for longer responses), self-enhancement (5-7% boost for self-generated text), and fabricated-citation susceptibility — make it unreliable without mitigation.
- **Techniques:** Systematic taxonomy of 12 bias types (CALM framework); strategies for mitigation including calibration, chain-of-thought reasoning, reference-anchored scoring.
- **Takeaways for humanization:**
  - EQ-Bench Creative Writing uses Claude-judge, which is itself biased toward longer, more verbose text. Scores inflated ~15% by length need adjustment.
  - Self-preference bias means Claude judging Claude output is systematically inflated; the EQ-Bench upgrade to Claude Sonnet 4.6 as judge (announced 2025) does not eliminate this.
  - "LLM assigns significantly higher evaluations to outputs with lower perplexity than human evaluators" — directly relevant to any humanness metric built on LLM-judge.
- **Summary:** The most complete 2025 survey of LLM-as-judge reliability, covering over 100 judge models and establishing that even frontier models carry systematic biases large enough to reverse apparent quality improvements. Position and verbosity biases alone can change benchmark rankings.
- **Key quote:** *"Biases (e.g., position, verbosity) and hallucinations persist; even advanced models like GPT-4V display these challenges."*

---

### 18. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)

- **Authors:** Various (CALM Framework paper)
- **Year / Venue:** 2024 preprint → ICLR 2025 (arXiv:2410.02736)
- **URL:** https://arxiv.org/abs/2410.02736
- **Core claim:** 12 named bias types (position, verbosity, self-enhancement, sycophancy, bandwagon, authority, etc.) can be systematically quantified and partially mitigated. Multilingual evaluation is particularly brittle: state-of-the-art judges average Fleiss' Kappa ≈ 0.3 across languages, much worse in low-resource languages.
- **Takeaways for humanization:**
  - Any LLM-judge-based humanness eval (EQ-Bench, custom rubrics) inherits all 12 biases unless explicitly mitigated.
  - Multilingual humanization evals are essentially untrustworthy with current judge models.
- **Summary:** Establishes the most comprehensive bias taxonomy for LLM-judge evaluation and provides reproducible measurement methodology. The multilingual reliability finding is especially relevant for non-English humanization targets.
- **Key quote:** *"State-of-the-art judges average Fleiss' Kappa ≈ 0.3 and much poorer performance in low-resource languages."*

---

### 19. LLM-based NLG Evaluation: Current Status and Challenges

- **Authors:** Gao, Hu, Yin, Ruan, Pu, Wan
- **Year / Venue:** 2025, **Computational Linguistics 51(2):661** (MIT Press)
- **URL:** https://direct.mit.edu/coli/article/51/2/661/128807/LLM-based-NLG-Evaluation-Current-Status-and
- **Core claim:** LLM-based evaluation has superseded BLEU/ROUGE as the dominant paradigm for NLG quality assessment. Four approaches now coexist: (a) LLM-derived metrics, (b) prompting LLMs, (c) fine-tuning LLMs as evaluators, and (d) human–LLM collaborative evaluation. Category (d) achieves the strongest results.
- **Techniques:** Systematic survey of ~200 papers; taxonomy of scoring protocols (continuous, Likert, pairwise); human–LLM checklist collaboration.
- **Takeaways for humanization:**
  - Human–LLM collaborative eval (human constructs rubric, LLM scores at scale) is now the best practice; single-model auto-eval is insufficient for a humanness claim.
  - BLEU and ROUGE are "increasingly ceremonial" — confirmed by this 2025 authoritative survey.
- **Summary:** The peer-reviewed 2025 definitive survey of LLM-as-judge for NLG. Establishes that reference-free LLM evaluation now dominates but requires human-anchored rubrics and bias mitigation to be reliable.
- **Key quote:** *"Human–LLM collaborative evaluation… results in the strongest performance."*

---

### 20. Order in the Evaluation Court: A Critical Analysis of NLG Evaluation Trends (2025)

- **Authors:** Various
- **Year / Venue:** 2025 preprint (arXiv:2601.07648)
- **URL:** https://arxiv.org/html/2601.07648v1
- **Core claim:** A meta-analysis of evaluation practices in NLG papers from 2015 to 2025 shows BLEU/ROUGE adoption declining sharply while LLM-as-judge and human eval are ascending. However, reproducibility remains poor: most LLM-judge setups are not standardized, making cross-paper comparisons unreliable.
- **Takeaways for humanization:**
  - Reinforces that any humanness claim must specify judge model, prompt template, and bias-mitigation strategy to be reproducible.
  - "2025 best practice = LLM-judge + human calibration anchor" — not just raw LLM score.
- **Summary:** Documents the decade-scale shift away from reference-based metrics toward LLM-judge, while flagging that the shift has introduced new reproducibility problems that are not yet solved.

---

## Key Techniques / Patterns

| Technique | Where it lives | Why it matters for humanization |
|---|---|---|
| **Nucleus / top-p sampling** | Decoding (Holtzman 2020) | First method to restore human-like probability distribution; still default baseline. |
| **Unlikelihood training** | Training (Welleck 2020) | Repetition is an objective-level bug, not just decoding. |
| **Locally typical sampling** | Decoding (Meister 2022) | Targets conditional entropy — cleanest theory of "human-like" token choice. |
| **Contrastive search** | Decoding (Su 2022/2023) | Penalizes embedding-similarity between candidate and context → breaks repetition. |
| **Contrastive Decoding (expert − amateur)** | Decoding (Li 2023) | Cancels small-model pathologies from a big model's output; no extra training. |
| **η-sampling / ε-sampling** | Decoding (Hewitt 2022) | Entropy-aware truncation; cleaner than top-p in high-entropy contexts. |
| **Min-p sampling** | Decoding (Nguyen 2024/25) | Enables high-temp creative writing without incoherence; deployment-ready. |
| **Mirostat** | Decoding (Basu 2021) | Explicit perplexity-target feedback loop — lets Unslop dial "human-range" perplexity. |
| **Repetition penalty / no-repeat-n-gram** | Decoding (folklore, popularized post-Holtzman) | Coarse but cheap band-aid; still used in production. |
| **MAUVE divergence** | Evaluation (Pillutla 2021) | Captures both Type-I (degenerate) and Type-II (too-narrow) failures. |
| **BERTScore** | Evaluation (Zhang 2020) | Paraphrase-robust semantic preservation floor. |
| **Psycholinguistic probes (HLB)** | Evaluation (Duan 2024) | Surface-stat metrics are insufficient; human *processing* patterns matter. |
| **Probability-curvature detection** | Adversarial (Mitchell 2023) | Humanized text must escape the LM's log-prob ridge. |
| **Multi-model probability features** | Adversarial (Verma 2024) | Humanized text must also confuse *proxy* LMs, not just the source. |
| **Detector-guided paraphrase** | Adversarial humanization (Cheng 2025) | SOTA attack; the baseline any humanizer should match or beat. |
| **LLM-as-judge bias mitigation** | Evaluation meta (CALM 2025, Gao et al. 2025) | Any humanness claim using LLM-judge must account for position, verbosity, and self-preference biases. |
| **Human–LLM collaborative evaluation** | Evaluation methodology (Gao et al. 2025) | Human-constructed rubric + LLM scoring = current best practice for NLG quality assessment. |

## Notable Quotes

> "Using likelihood as a decoding objective leads to text that is bland and
> strangely repetitive." — Holtzman et al., *The Curious Case of Neural Text
> Degeneration* (ICLR 2020)

> "We posit that humans produce language with the goal of transmitting
> information efficiently and with minimum error… each word's information
> content [should be] close to the conditional entropy of our model." —
> Meister et al., *Locally Typical Sampling* (TACL 2023)

> "The failures of larger LMs (e.g., repetition, incoherence) are even more
> prevalent in smaller LMs, and this difference signals which texts should be
> preferred." — Li et al., *Contrastive Decoding* (ACL 2023)

> "Humans prefer perplexity that is neither too high nor too low, and
> cross-entropy has a near-linear relation with repetition." — Basu et al.,
> *Mirostat* (ICLR 2021)

> "Text sampled from an LLM tends to occupy regions of negative curvature of
> the model's log probability function." — Mitchell et al., *DetectGPT*
> (ICML 2023)

> "Improvements in other performance metrics did not necessarily lead to
> greater humanlikeness, and in some cases, even resulted in a decline." —
> Duan et al., *HLB* (2024)

> "Adversarial paraphrasing… achieves an average T@1%F reduction of 87.88%
> across diverse detectors." — Cheng et al., *Adversarial Paraphrasing* (2025)

## Emerging Trends

1. **From static truncation to adaptive sampling.** The progression from top-k
   → top-p → typical → η → min-p → entropy-aware (entropix) is unmistakably
   toward samplers that react to the *local* shape of the distribution.
   Unslop should default to adaptive, not fixed-threshold, samplers.
2. **Representation-geometry explanations of degeneration.** SimCTG's
   anisotropy story, contrastive decoding's small-vs-large geometry, and
   follow-up corrections (Su & Collier 2023) all point to a shared idea: the
   *internal geometry* of LMs, not just their output distributions, governs
   degeneracy.
3. **Distributional, not reference-based, evaluation.** MAUVE and HLB both
   compare *populations* of text rather than single references. Expect more
   psycholinguistic-style eval in 2025–26; BLEU/ROUGE are increasingly
   ceremonial.
4. **Perplexity is no longer a free signal.** Detectors (DetectGPT,
   Ghostbuster) are now weaponized perplexity; humanizers that optimize any
   single statistic can be out-flanked. The frontier is multi-signal.
5. **Humanization becoming a first-class research topic.** Cheng et al. (2025)
   is emblematic: the community is starting to publish explicit humanization
   attacks at top venues with transfer studies, evaluation suites, and
   ethical discussion. Unslop is arriving as the subfield forms.
6. **Training-free wins keep coming.** Contrastive decoding, contrastive
   search, min-p, η-sampling, adversarial paraphrasing — all *inference-time*
   methods that require zero retraining. Strong signal that decoding /
   paraphrase stacks can reach SOTA without custom model training.
7. **LLM-as-judge is the new evaluation default — with known bias budget.** BLEU/ROUGE are now ceremonial in NLG papers. LLM-judge dominates but carries quantified, reproducible biases: ~40% GPT-4 position inconsistency, ~15% verbosity inflation, 5-7% self-enhancement. The CALM framework (2025) and the Gao et al. survey (Computational Linguistics, 2025) establish this bias budget as prior art any humanization eval must account for. (A, new)
8. **Antislop accepted at ICLR 2026.** Paech et al.'s framework was accepted as a conference paper at ICLR 2026 (poster #10008156), upgrading its status from arXiv preprint to peer-reviewed venue. The FTPO fine-tuning method now shows 90% slop suppression across 8,000+ patterns while maintaining or improving GSM8K, MMLU, and creative writing benchmarks. A companion `auto-antislop` repo automates the profiling pipeline. (A, C)
9. **EU AI Act watermarking obligations land August 2026.** Article 50 of the EU AI Act (effective August 2026) requires GPAI providers to mark all AI-generated text and implement user-facing detectors. The December 2025 first draft Code of Practice recommends a multilayered approach (metadata + watermark + fingerprinting) and explicitly prohibits ToS-level removal of watermarks. This makes the watermark vs. humanization Pareto frontier a compliance question, not just a research question. (A, B, D)

## Open Questions / Gaps

- **No unified "humanness score."** MAUVE captures distribution; BERTScore
  captures semantics; HLB captures psycholinguistic patterns; burstiness and
  perplexity capture surface stats. A composite metric validated against human
  judgments *and* detector evasion does not yet exist.
- **Robustness of decoding wins under instruction-tuning / RLHF.** Almost all
  the decoding papers above were validated on base or only lightly tuned LMs
  (GPT-2, OPT, early LLaMA). How nucleus vs. typical vs. min-p vs. contrastive
  search behave on GPT-4-class or post-RLHF models is under-studied.
- **Multilingual humanization.** Most work is English-centric. Contrastive
  Search showed gains across 16 languages but isotropy findings diverged;
  extending humanization pipelines beyond English is open.
- **Burstiness as a training signal.** Burstiness is widely used *defensively*
  (by detectors) but hasn't been directly incorporated into training or
  decoding objectives. An "increase-burstiness" loss or sampler is a plausible
  contribution.
- **Style-preserving humanization.** Adversarial paraphrasing optimizes for
  evasion, not author voice preservation. Joint objectives that humanize
  *while* matching a target author/persona are a clear gap.
- **Ethical framing.** Very little academic work engages with the downstream
  implications of successful humanization (disinformation, ghost-authored
  academic work, assignment fraud). Unslop should expect this to become a
  required section in top-venue submissions within 1–2 years.
- **Watermark vs. humanization is now a compliance question.** The EU AI Act Article 50 (effective August 2026) mandates machine-readable marking of all AI-generated text. The December 2025 first draft Code of Practice requires multilayered approaches (metadata + watermark + fingerprinting) and prohibits ToS-level removal. The academic trade-off curve between watermark robustness and humanization strength has not been mapped, but the regulatory deadline makes this urgent.
- **LLM-judge bias is under-addressed in humanization evals.** EQ-Bench, custom rubrics, and detector-evasion claims all rely on LLM judges carrying quantified verbosity and position biases. The CALM framework (2025) provides tools to measure these; no humanization product has yet applied them systematically to its own evaluation pipeline.
- **2025-class model perplexity narrows the detection gap.** Top 2025-2026 models achieve perplexity as low as 5-10, significantly reducing the gap between AI and human text on the metric classical detectors rely on. Whether burstiness holds as a reliable signal at this perplexity level is under-studied.

## References

1. Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2020). *The Curious
   Case of Neural Text Degeneration.* ICLR 2020. https://arxiv.org/abs/1904.09751
2. Welleck, S., Kulikov, I., Roller, S., Dinan, E., Cho, K., & Weston, J.
   (2020). *Neural Text Generation with Unlikelihood Training.* ICLR 2020.
   https://arxiv.org/abs/1908.04319
3. Pillutla, K., Swayamdipta, S., Zellers, R., Thickstun, J., Welleck, S.,
   Choi, Y., & Harchaoui, Z. (2021). *MAUVE: Measuring the Gap Between Neural
   Text and Human Text using Divergence Frontiers.* NeurIPS 2021.
   https://papers.nips.cc/paper/2021/hash/260c2432a0eecc28ce03c10dadc078a4-Abstract.html
4. Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020).
   *BERTScore: Evaluating Text Generation with BERT.* ICLR 2020.
   https://arxiv.org/abs/1904.09675
5. Meister, C., Pimentel, T., Wiher, G., & Cotterell, R. (2023). *Locally
   Typical Sampling.* TACL / EMNLP 2022. https://arxiv.org/abs/2202.00666
6. Su, Y., Lan, T., Wang, Y., Yogatama, D., Kong, L., & Collier, N. (2022).
   *A Contrastive Framework for Neural Text Generation (SimCTG).* NeurIPS
   2022 (Spotlight). https://arxiv.org/abs/2202.06417
7. Su, Y., & Collier, N. (2023). *Contrastive Search Is What You Need For
   Neural Text Generation.* TMLR. https://arxiv.org/abs/2210.14140
8. Li, X. L., Holtzman, A., Fried, D., Liang, P., Eisner, J., Hashimoto, T.,
   Zettlemoyer, L., & Lewis, M. (2023). *Contrastive Decoding: Open-ended
   Text Generation as Optimization.* ACL 2023.
   https://arxiv.org/abs/2210.15097
9. Hewitt, J., Manning, C. D., & Liang, P. (2022). *Truncation Sampling as
   Language Model Desmoothing.* Findings of EMNLP 2022.
   https://arxiv.org/abs/2210.15191
10. Nguyen, M., Baker, A., Neo, C., Roush, A., Kirsch, A., & Shwartz-Ziv, R.
    (2025). *Turning Up the Heat: Min-p Sampling for Creative and Coherent
    LLM Outputs.* ICLR 2025. https://arxiv.org/abs/2407.01082
11. Basu, S., Ramachandran, G. S., Keskar, N. S., & Varshney, L. R. (2021).
    *Mirostat: A Neural Text Decoding Algorithm That Directly Controls
    Perplexity.* ICLR 2021. https://arxiv.org/abs/2007.14966
12. Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., & Finn, C. (2023).
    *DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability
    Curvature.* ICML 2023 (Oral). https://arxiv.org/abs/2301.11305
13. Verma, V., Fleisig, E., Tomlin, N., & Klein, D. (2024). *Ghostbuster:
    Detecting Text Ghostwritten by Large Language Models.* NAACL 2024.
    https://aclanthology.org/2024.naacl-long.95/
14. Duan, X., Xiao, B., Tang, X., & Cai, Z. G. (2024). *HLB: Benchmarking
    LLMs' Humanlikeness in Language Use.* arXiv:2409.15890.
    https://arxiv.org/abs/2409.15890
15. Cheng, Y., Sadasivan, V. S., et al. (2025). *Adversarial Paraphrasing: A
    Universal Attack for Humanizing AI-Generated Text.* arXiv:2506.07001.
    https://arxiv.org/abs/2506.07001
16. *Make Every Token Count: A Systematic Survey on Decoding Methods for
    Foundation Models* (2024). arXiv:2410.06097. https://arxiv.org/abs/2410.06097
17. Various. (2025). *A Survey on LLM-as-a-Judge.* arXiv:2411.15594.
    https://arxiv.org/abs/2411.15594
18. Various. (2025). *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM).* ICLR 2025. arXiv:2410.02736.
    https://arxiv.org/abs/2410.02736
19. Gao, et al. (2025). *LLM-based NLG Evaluation: Current Status and Challenges.* Computational Linguistics 51(2):661.
    https://direct.mit.edu/coli/article/51/2/661/128807/LLM-based-NLG-Evaluation-Current-Status-and
20. Various. (2025). *Order in the Evaluation Court: A Critical Analysis of NLG Evaluation Trends.* arXiv:2601.07648.
    https://arxiv.org/html/2601.07648v1
