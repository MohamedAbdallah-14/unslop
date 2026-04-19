# 05 · AI Text Detection & Evasion — Angle A: Academic & Scholarly

Research digest for the Humazier project. Focus: peer-reviewed and preprint literature on detecting LLM-generated text, watermarking schemes, and the red-team / evasion work that defeats them. Sources limited to arXiv, ACL/EMNLP/NAACL/EACL, ICLR, ICML, NeurIPS, COLT, USENIX Security, and Nature.

**Research value: high** — The topic has a dense, recent, and highly contested academic literature, with named canonical papers, formal impossibility and possibility results, and a well-developed adversarial sub-field.

---

## Snapshot: What the academic field looks like in 2026

Three camps are visible in the literature:

1. **Detector builders.** Zero-shot statistical detectors (DetectGPT → Fast-DetectGPT → Binoculars), trained classifiers (OpenAI's RoBERTa detector, Ghostbuster, RADAR), and retrieval-based defenses. AUROC on clean same-domain text is now ≥0.99 for several methods.
2. **Watermarkers.** Green-list biasing (Kirchenbauer), Gumbel / cryptographic hashing (Aaronson, Christ–Gunn–Zamir), and production-scale schemes (SynthID-Text). Work has moved from "does it work?" to "is it robust and undetectable?"
3. **Red-teamers.** Paraphrase attacks (DIPPER, recursive paraphrasing), watermark stealing/spoofing, homoglyph substitution, and adaptive optimization attacks. These regularly drop SOTA detector AUROC to near-chance.

The field's core open question is no longer *can* machine text be detected, but *under what distribution shift, adversary budget, and false-positive tolerance*. Theoretical results point both ways: Sadasivan et al. show an impossibility bound as models approach human text; Chakraborty et al. counter with a sample-complexity possibility result.

A persistent secondary concern is **equity**: detectors systematically misfire on non-native English writers and constrained vocabulary — arguably the most serious academic-integrity finding of the cycle.

---

## 1. DetectGPT: Zero-Shot Detection via Probability Curvature

- **Authors / venue:** Mitchell, Lee, Khazatsky, Manning, Finn — ICML 2023 (Oral).
- **URL:** https://arxiv.org/abs/2301.11305
- **One-line:** Detect machine text by measuring that LLM samples sit in negative-curvature regions of the source model's log-probability function; no training, no watermark.
- **Method:** For a passage `x`, perturb with a mask-fill model (T5) to get `x̃₁..x̃ₙ`, then score `log pθ(x) − (1/n)Σ log pθ(x̃ᵢ)`. Positive gap ⇒ likely machine-generated.
- **Headline numbers:** On GPT-NeoX-20B fake news, AUROC 0.81 (best prior zero-shot) → **0.95**.
- **Why it matters:** Launched the current generation of zero-shot detectors; the probability-curvature framing is the template followed by Fast-DetectGPT, Binoculars, Raidar, and others.

## 2. Fast-DetectGPT: Conditional Probability Curvature

- **Authors / venue:** Bao, Zhao, Teng, Yang, Zhang — ICLR 2024.
- **URL:** https://arxiv.org/abs/2310.05130
- **One-line:** Replace DetectGPT's expensive mask-fill perturbations with a single-pass conditional sampling step; same idea, ~340× faster.
- **Headline numbers:** 75% relative AUROC improvement over DetectGPT in both white-box (0.9887) and black-box (ChatGPT/GPT-4: 0.9338) settings, with **340× speedup**.
- **Implication for humanizers:** Raises the bar for adversaries: cheap enough to be deployed online, so latency is no longer a reason to prefer weaker detectors.

## 3. Binoculars: Zero-Shot Detection by Contrasting Two LLMs

- **Authors / venue:** Hans, Schwarzschild, Cherepanova, Kazemi, Saha, Goldblum, Geiping, Goldstein — ICML 2024.
- **URL:** https://arxiv.org/abs/2401.12070
- **One-line:** Score text using the ratio between a base model's perplexity and an instruction-tuned sibling's cross-perplexity (Falcon-7B vs Falcon-7B-Instruct by default).
- **Headline numbers:** "Detects over 90% of ChatGPT-generated samples … at a false positive rate of 0.01%." No training data from ChatGPT required.
- **Significance:** One of the strongest zero-shot, training-free detectors; interesting because it leverages the *gap* between base and instruct models rather than needing the generating model.

## 4. Ghostbuster: Structured-Search over Weak-Model Probabilities

- **Authors / venue:** Verma, Fleisig, Tomlin, Klein — NAACL 2024.
- **URL:** https://aclanthology.org/2024.naacl-long.95/ (BAIR blog: https://bair.berkeley.edu/blog/2023/11/14/ghostbuster/)
- **One-line:** Pass the document through several *weak* LMs (unigram, trigram, non-instruction-tuned GPT-3), run structured feature search over their token probabilities, and train a small linear classifier.
- **Headline numbers:** 99.0 F1 in-domain; "outperforms DetectGPT and GPTZero by an average margin of 23.7 F1"; +7.5 F1 cross-domain, +4.4 F1 cross-model.
- **Distinctive claim:** Does not need token probabilities from the *target* model, so it works on black-box ChatGPT/Claude output — a key property when bigger models close their APIs.

## 5. Kirchenbauer et al. — A Watermark for Large Language Models

- **Authors / venue:** Kirchenbauer, Geiping, Wen, Katz, Miers, Goldstein — ICML 2023 (Outstanding Paper).
- **URL:** https://arxiv.org/abs/2301.10226 · https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf
- **One-line:** Before each token, hash the prior token to split the vocabulary into a "green" and "red" list; softly boost green logits. Detect via a one-sided z-test on green-token frequency.
- **Headline numbers:** Detectable from "as short as 25 words," with interpretable p-values; tested on OPT-family models. No model access required at detection time.
- **Why it's canonical:** The green-list / red-list construction is now the reference point every subsequent watermarking or evasion paper is measured against.

## 6. Kirchenbauer et al. — On the Reliability of Watermarks for LLMs

- **Authors / venue:** Kirchenbauer, Geiping, et al. — ICLR 2024.
- **URL:** https://arxiv.org/abs/2306.04634
- **One-line:** Stress-tests the original green-list watermark under human rewriting, LLM paraphrasing, and partial embedding in long documents.
- **Headline numbers:** "After strong human paraphrasing, watermarks were detectable on average after observing 800 tokens (at a 1e-5 false positive rate)." Watermarks leak through paraphrases as n-gram fragments.
- **Tension:** Frames watermarking as *robust but not invulnerable* — sets up the Sadasivan / Jovanovic counter-attacks.

## 7. SynthID-Text: Scalable Watermarking Deployed in Gemini

- **Authors / venue:** Dathathri et al., Google DeepMind — *Nature* 2024 (October).
- **URL:** https://www.nature.com/articles/s41586-024-08025-4 · Code: https://github.com/google-deepmind/synthid-text
- **One-line:** Tournament-style modulation of token probabilities at sampling time; composable with speculative sampling so it runs at production speed.
- **Headline evidence:** "A live experiment assessed feedback from nearly 20 million Gemini responses, confirming preservation of text quality." No measurable degradation on standard benchmarks or human ratings.
- **Why it matters:** First large-scale evidence that a watermark can ship behind a real consumer LLM without user-visible quality loss; also the first to publish detector thresholds and failure modes under deployment scale.

## 8. Christ, Gunn, Zamir — Undetectable Watermarks for Language Models

- **Authors / venue:** Christ, Gunn, Zamir — COLT 2024.
- **URL:** https://arxiv.org/abs/2306.09194
- **One-line:** Cryptographic construction (assuming one-way functions) whose output distribution is computationally indistinguishable from the un-watermarked model.
- **Core properties:** Undetectability even under adaptive queries; completeness under a secret key (works on substrings); soundness (independent text has negligible false-positive probability).
- **Significance:** Theoretical counterpoint to Sadasivan's impossibility result — shows that *cryptographic* watermarks can exist without a distribution-quality tradeoff, even if they can still be broken by editing.

## 9. Sadasivan et al. — Can AI-Generated Text Be Reliably Detected?

- **Authors / venue:** Sadasivan, Kumar, Balasubramanian, Wang, Feizi — arXiv 2303.11156 (first posted 2023, heavily revised through 2024).
- **URL:** https://arxiv.org/abs/2303.11156
- **One-line:** Both empirically (recursive paraphrasing) and theoretically (a Total-Variation-distance bound) argue that no detector can reliably distinguish sufficiently good LLM text from human text.
- **Key quote (paraphrased from abstract):** "As language models become more sophisticated and better at emulating human text, the performance of even the best-possible detector decreases … may only perform marginally better than a random classifier."
- **Attacks demonstrated:** Recursive paraphrasing beats watermarks, neural classifiers, zero-shot detectors, and retrieval-based detectors; watermarks are separately vulnerable to **spoofing** (flagging human text).

## 10. Chakraborty et al. — Position: On the Possibilities of AI-Generated Text Detection

- **Authors / venue:** Chakraborty, Bedi, Zhu, An, Manocha, Huang — ICML 2024 (Position).
- **URL:** https://arxiv.org/abs/2304.04736 · https://proceedings.mlr.press/v235/chakraborty24a.html
- **One-line:** Counter to Sadasivan: detection is "consistently feasible, except when human and machine text distributions are indistinguishable across their entire support" — derives sample-complexity bounds tying detection to sequence length.
- **Empirical backing:** XSum, SQuAD, IMDb, Kaggle FakeNews; generators include GPT-2, GPT-3.5-Turbo, Llama variants.
- **Why both Sadasivan and Chakraborty matter:** Together they define the theoretical envelope — reliable detection requires either (a) enough text, or (b) distributions that still have some separable support. Once neither holds, detection collapses to chance.

## 11. Krishna et al. — Paraphrasing Evades Detectors; Retrieval Defends (DIPPER)

- **Authors / venue:** Krishna, Song, Karpinska, Wieting, Iyyer — NeurIPS 2023.
- **URL:** https://arxiv.org/abs/2303.13408
- **One-line:** Introduces DIPPER, an 11B-parameter controllable paraphraser with lexical-diversity and reorder knobs; uses it to evade GPTZero, DetectGPT, OpenAI's classifier, and green-list watermarks.
- **Headline numbers:** "DIPPER reduced DetectGPT's detection accuracy from **70.3% to 4.6%** (at a 1% false positive rate)." Proposed retrieval defense (provider stores previously generated sequences) recovers 80-97% detection.
- **Why it's canonical:** Most cited evasion paper; the "paraphrase defeats detector, retrieval defends" pattern is now the default adversarial frame in every subsequent watermark paper.

## 12. Hu, Chen, Ho — RADAR: Robust AI-Text Detection via Adversarial Learning

- **Authors / venue:** Hu, Chen, Ho — NeurIPS 2023 (IBM Research).
- **URL:** https://arxiv.org/abs/2307.03838
- **One-line:** Co-train a paraphraser and a RoBERTa-large detector in a GAN-style loop; the paraphraser learns to evade, the detector learns to catch the paraphrase.
- **Evaluation:** 8 LLMs (Pythia, Dolly 1.0/2.0, Palmyra, Camel, GPT-J, LLaMA, Vicuna) × 4 datasets; substantial robustness gains specifically under paraphrasing, plus transfer to GPT-3.5-Turbo.
- **Pattern it illustrates:** Detection becomes an arms race that each side can formalize as a minimax; RADAR is the cleanest academic instance of this framing.

## 13. Jovanović, Staab, Vechev — Watermark Stealing in Large Language Models

- **Authors / venue:** Jovanović, Staab, Vechev — ICML 2024 (ETH SRI Lab).
- **URL:** https://arxiv.org/abs/2402.19361 · https://watermark-stealing.org
- **One-line:** Query a watermarked API to approximately reverse-engineer its secret green-list rules, then use the stolen rules for both **spoofing** (fabricate "watermarked" text) and **scrubbing** (strip watermark from arbitrary text).
- **Headline quote:** "For under **$50**, attackers can both spoof and scrub state-of-the-art schemes that were previously considered safe, with an average success rate over 80%."
- **Why it matters:** Empirical rebuttal to "watermark is deployment-ready"; especially corrosive to schemes like Kirchenbauer green-list where the secret is a static per-prefix partition.

## 14. Mao et al. — RAIDAR: geneRative AI Detection viA Rewriting

- **Authors / venue:** Mao, Vondrick, Wang, Yang — ICLR 2024 (Columbia).
- **URL:** https://arxiv.org/abs/2401.12970
- **One-line:** Prompt an LLM to rewrite the candidate text and measure edit distance; LLMs edit *human* text more and *AI* text less, because they already view AI text as high-quality.
- **Headline numbers:** Up to **+29 F1 points** across news, creative writing, student essays, code, Yelp reviews, and arXiv papers. Black-box compatible (GPT-3.5 / GPT-4).
- **Pattern signal:** Second-generation detectors are moving away from log-probability access and toward behavioral probes that work even on closed APIs.

## 15. Liang et al. — GPT Detectors Are Biased Against Non-Native English Writers

- **Authors / venue:** Liang, Yuksekgonul, Mao, Wu, Zou — *Patterns* (Cell Press) July 2023; arXiv 2304.02819.
- **URL:** https://arxiv.org/abs/2304.02819
- **One-line:** Detectors misclassify more than half of TOEFL essays as AI-generated while being near-perfect on native English college essays.
- **Headline quote:** "TOEFL essays unanimously misclassified as AI-generated showed significantly lower perplexity compared to others" — i.e., detectors conflate limited lexical diversity with machine output.
- **Bypass finding:** Prompting ChatGPT with "Enhance the word choices to sound more like that of a native speaker" *both* removes the false-positive bias for real ESL essays *and* lets actual AI output evade detection — the same transformation.
- **Why humanizers care:** This is the single most important equity result in the literature, and it is also a direct recipe for a lightweight humanization prompt.

## 16. Tulchinskii et al. — Intrinsic Dimension Estimation for Robust Detection

- **Authors / venue:** Tulchinskii, Kuznetsov, Kushnareva, Cherniavskii, Nikolenko, Burnaev, Barannikov, Piontkovskaya — NeurIPS 2023.
- **URL:** https://arxiv.org/abs/2306.04723
- **One-line:** Measure the *persistent-homology / intrinsic dimension* of contextual embeddings; human text sits at a systematically higher manifold dimension than AI text.
- **Headline numbers:** Human IΔ ≈ 9 (alphabetic languages), ≈ 7 (Chinese); AI text ≈ 1.5 lower on average. Stable across domains and models.
- **Significance:** Geometry-based detector that is not defeated by surface-level edits; suggestive for humanizers that *structural* diversity, not just lexical, is what detectors are starting to score.

## 17. Wang et al. — M4: Multi-Generator, Multi-Domain, Multi-Lingual Detection

- **Authors / venue:** Wang, Mansurov, Ivanov, Su, Shelmanov, Tsvigun, Whitehouse, Afzal, Mahmoud, Sasaki, Arnold, Aji, Habash, Gurevych, Nakov — EACL 2024 (Best Resource Paper).
- **URL:** https://arxiv.org/abs/2305.14902 · https://github.com/mbzuai-nlp/M4
- **One-line:** Large cross-language, cross-generator, cross-domain benchmark; became the basis for SemEval-2024 Task 8.
- **Key finding:** Detectors "struggle to generalize well on unseen domains or LLM instances" and "tend to misclassify machine-generated text as human-written" in out-of-distribution settings — the failure mode is false *negatives*, the opposite of the ESL-writer false-positive problem.
- **Implication:** Generalization — not peak in-domain AUROC — is the binding constraint for real deployments.

## 18. He et al. — MGTBench

- **Authors / venue:** He, Shen, Backes, Zhang — later CCS 2024 benchmark release.
- **URL:** https://arxiv.org/abs/2303.14822
- **One-line:** First comprehensive MGT-detection benchmark across metric-based (log-likelihood, rank, DetectGPT) and model-based (OpenAI detector, ChatGPT detector) methods, with explicit adversarial-robustness track (paraphrase, random spacing, perturbations).
- **Takeaway quote:** "Even the best detectors can be evaded by small adversarial perturbations."
- **Why it's cited:** Standard ablation harness; later extended to M4GT-Bench and IMGTB.

## 19. Creo & Pudasaini — SilverSpeak: Evading Detectors via Homoglyphs

- **Authors / venue:** Creo, Pudasaini — arXiv 2406.11239 (latest v3 2025).
- **URL:** https://arxiv.org/abs/2406.11239
- **One-line:** Replace Latin characters with visually identical Cyrillic/Greek homoglyphs (e.g. Latin `A` → Cyrillic `А`) to break subword tokenization and collapse detector accuracy.
- **Headline quote:** "Homoglyph-based attacks can effectively circumvent state-of-the-art detectors, leading them to classify all texts as either AI-generated or human-written (**decreasing the average Matthews Correlation Coefficient from 0.64 to –0.01**)."
- **Detectors broken:** ArguGPT, Binoculars, DetectGPT, Fast-DetectGPT, Ghostbuster, OpenAI detector, green-list watermarks — all seven.
- **Ethical note:** Trivial attack, deeply broken defense — this is currently the loudest evidence that character-level normalization is not a solved preprocessing step.

## 20. Aaronson — Gumbel Watermark (OpenAI)

- **Authors / venue:** Scott Aaronson — Simons Institute talk (2023-08-17), not a peer-reviewed paper; multiple formalizations since (see Ruan et al. 2024, "Refined Detection for Gumbel Watermarking," arXiv 2603.30017).
- **URL:** https://simons.berkeley.edu/talks/scott-aaronson-ut-austin-openai-2023-08-17
- **One-line:** Sample via `argmaxₐ log P(a) − log U(a)` with pseudo-random `U` derived from a hash of a secret key and the prior context; detection reconstructs `U` and tests for non-uniformity.
- **Why it's included:** Parallel design to Kirchenbauer's green-list with a cryptographic flavor; the basis of many follow-on schemes (GumbelSoft, refined-detection Gumbel). Closes the loop with the Christ–Gunn–Zamir "undetectable watermarks" theoretical line.

---

## Patterns across the literature

1. **Clean-setting AUROC is basically solved; distribution shift is not.** Fast-DetectGPT, Binoculars, Ghostbuster, and RAIDAR all push same-domain AUROC ≥0.99. M4 and MGTBench both show that cross-domain / cross-generator performance drops sharply, and consistently in the direction of false negatives.
2. **Paraphrasing is the universal solvent.** DIPPER (Krishna), recursive paraphrasing (Sadasivan), Bias-Inversion Rewriting (BIRA), RADAR's adversarial paraphraser — every published evasion pipeline uses paraphrasing as its primary tool. Watermarks degrade but don't vanish; neural detectors often collapse.
3. **Watermarks are caught between quality and security.** SynthID-Text achieves production-grade quality with acceptable detectability. But Jovanović's stealing attack ($50, 80% success) and Kirchenbauer-reliability's 800-token leakage show that the same determinism that enables detection enables both scrubbing and spoofing.
4. **Theory is split.** Sadasivan's TV-distance impossibility and Chakraborty's sample-complexity possibility result are not contradictory — they are the same curve read from opposite ends. The practical question is whether a deployment has enough tokens *and* a big enough human-vs-machine distribution gap.
5. **The "bad detector" failure mode is socially concentrated.** Liang's TOEFL result (over half of non-native essays flagged as AI) plus M4's cross-domain false negatives mean detectors misfire *asymmetrically*: false positives fall on ESL writers and constrained-vocabulary styles; false negatives fall on domain-shifted, paraphrased, or homoglyph-processed machine text.
6. **New-generation detectors probe behavior, not logits.** RAIDAR (rewrite-edit-distance), Binoculars (two-model contrast), Tulchinskii (manifold dimension) are all moving away from requiring access to the generator's logits — a direct response to closed APIs and watermark stealing.

## Gaps / open problems

- **Adaptive adversary evaluations are still rare.** Most detector papers test against DIPPER or GPT-3.5 paraphrase; few retrain their detector *against an adaptively optimized* paraphraser. BIRA-style query-free optimization attacks are not yet standard in detector benchmarks.
- **Character-level and Unicode normalization is unsolved in practice.** SilverSpeak's MCC drop to –0.01 with trivial homoglyph substitution suggests that pre-processing pipelines have not caught up with the 2024 academic literature.
- **No robust "humanization" benchmark.** The literature evaluates *attacks* (paraphrase rate, watermark removal) but not *quality-controlled humanization* — i.e., how much semantic/stylistic distortion is introduced per bit of detection reduction. This is the specific gap a humanizer product lives in.
- **ESL-fairness auditing is not a standard reporting axis.** Liang et al. is uniformly cited but rarely rerun on new detectors; most 2024-2025 papers report only in-domain AUROC, not TOEFL / non-native false-positive rates.
- **Theoretical impossibility vs watermark cryptography is unresolved.** Sadasivan's bound assumes no side-channel; Christ–Gunn–Zamir's undetectable cryptographic watermarks show side-channels can exist. The practical robustness of cryptographic watermarks under editing attacks has not been empirically validated at scale.

## Trends (2023 → 2026)

- **2023:** Zero-shot detection (DetectGPT), first green-list watermarks (Kirchenbauer), first impossibility result (Sadasivan), first ESL-bias exposure (Liang), DIPPER paraphrase attack. Fast expansion, everyone races to publish a detector.
- **2024:** Second-generation detectors that drop the "access the generator's logits" assumption (Binoculars, Ghostbuster, RAIDAR). Watermark realism (Kirchenbauer-reliability, SynthID-Text). Explicit stealing/spoofing attacks (Jovanović). Possibility/impossibility theoretical duel (Chakraborty vs Sadasivan) matures.
- **2025-2026:** The frontier has moved to (a) adaptive/optimization attacks (BIRA, adaptive watermark reverse-engineering), (b) multilingual and multi-generator generalization (M4, M4GT), (c) behavioral probes (rewrite, manifold dimension), and (d) production-scale auditing (SynthID-Text Nature paper as the rare deployed evidence). No single detector is robust to the combination of paraphrase + domain shift + homoglyphs.

## What this implies for a humanization tool

- **Target the overlap of failure modes.** Paraphrase + register change (Liang-style "enhance word choice") + modest lexical burstiness reliably moves text out of the high-curvature region exploited by DetectGPT/Fast-DetectGPT while raising the manifold dimension Tulchinskii measures.
- **Respect the ESL equity cost of "sounding human."** The Liang result is a double-edged sword: the transformation that evades detection is also the transformation that removes unfair bias against ESL writers. The humanizer's framing can honestly route through this.
- **Expect watermarks, not classifiers, to be the long-term defense.** SynthID-Text is in production and Christ–Gunn–Zamir suggests stronger schemes are theoretically possible; classifier detectors are provably fragile. Designing for watermark robustness (paraphrase + editing + possibly stealing-based scrubbing) is the forward-looking bet.
- **Benchmark against more than GPTZero.** Binoculars, Fast-DetectGPT, Ghostbuster, and RAIDAR are the current academic state of the art and should be in any honest evaluation; commercial detectors are known to trail.

---

## Source Index

| # | Paper | Venue | URL |
|---|---|---|---|
| 1 | Mitchell et al., *DetectGPT* | ICML 2023 | https://arxiv.org/abs/2301.11305 |
| 2 | Bao et al., *Fast-DetectGPT* | ICLR 2024 | https://arxiv.org/abs/2310.05130 |
| 3 | Hans et al., *Binoculars* | ICML 2024 | https://arxiv.org/abs/2401.12070 |
| 4 | Verma et al., *Ghostbuster* | NAACL 2024 | https://aclanthology.org/2024.naacl-long.95/ |
| 5 | Kirchenbauer et al., *A Watermark for LLMs* | ICML 2023 | https://arxiv.org/abs/2301.10226 |
| 6 | Kirchenbauer et al., *On the Reliability of Watermarks* | ICLR 2024 | https://arxiv.org/abs/2306.04634 |
| 7 | Dathathri et al., *SynthID-Text* | *Nature* 2024 | https://www.nature.com/articles/s41586-024-08025-4 |
| 8 | Christ, Gunn, Zamir, *Undetectable Watermarks* | COLT 2024 | https://arxiv.org/abs/2306.09194 |
| 9 | Sadasivan et al., *Can AI Text Be Reliably Detected?* | arXiv 2023–24 | https://arxiv.org/abs/2303.11156 |
| 10 | Chakraborty et al., *Position: Possibilities of Detection* | ICML 2024 | https://arxiv.org/abs/2304.04736 |
| 11 | Krishna et al., *DIPPER / Paraphrase Evades Detectors* | NeurIPS 2023 | https://arxiv.org/abs/2303.13408 |
| 12 | Hu, Chen, Ho, *RADAR* | NeurIPS 2023 | https://arxiv.org/abs/2307.03838 |
| 13 | Jovanović, Staab, Vechev, *Watermark Stealing* | ICML 2024 | https://arxiv.org/abs/2402.19361 |
| 14 | Mao et al., *RAIDAR* | ICLR 2024 | https://arxiv.org/abs/2401.12970 |
| 15 | Liang et al., *GPT Detectors Are Biased Against Non-Native English Writers* | *Patterns* 2023 | https://arxiv.org/abs/2304.02819 |
| 16 | Tulchinskii et al., *Intrinsic Dimension Detection* | NeurIPS 2023 | https://arxiv.org/abs/2306.04723 |
| 17 | Wang et al., *M4* | EACL 2024 (Best Resource) | https://arxiv.org/abs/2305.14902 |
| 18 | He et al., *MGTBench* | arXiv / CCS 2024 | https://arxiv.org/abs/2303.14822 |
| 19 | Creo & Pudasaini, *SilverSpeak (Homoglyphs)* | arXiv 2024–25 | https://arxiv.org/abs/2406.11239 |
| 20 | Aaronson, *Gumbel Watermark* (talk) + Ruan et al., *Refined Detection for Gumbel* | Simons 2023 / arXiv 2024 | https://simons.berkeley.edu/talks/scott-aaronson-ut-austin-openai-2023-08-17 |

