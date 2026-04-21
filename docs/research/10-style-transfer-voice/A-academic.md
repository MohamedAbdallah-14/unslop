# Style Transfer & Voice — Academic Research Digest

> **Category:** Style Transfer & Voice (author-attribute conditioning, style transfer, voice/tone matching, stylometric control, authorial fingerprinting, register adaptation)
> **Angle:** A — Academic
> **Project:** Unslop (humanizing AI output)
> **Compiled:** April 2026

**Research value: high** — The field has mature benchmarks (GYAFC, Yelp, Shakespeare, RealToxicityPrompts), a well-established method taxonomy (disentanglement / decoding-time steering / paraphrase-pivot / prompting), and a clear recent pivot toward LLM-era author-style conditioning that maps directly onto a "humanizer" product.

---

## 1. Survey & Framing

### 1.1 Jin, Jin, Hu, Vechtomova, Mihalcea — *Deep Learning for Text Style Transfer: A Survey* — **Computational Linguistics 48(1), 2022**
- **Problem:** Unified taxonomy for 100+ style-transfer papers since the first neural approach (2017).
- **Method/Contribution:** Organizes work by (a) data availability — parallel vs. non-parallel; (b) method family — disentanglement, prototype editing, pseudo-parallel construction; (c) style attribute — sentiment, formality, politeness, humor, personality, simplicity.
- **Dataset/Benchmark:** Catalogs GYAFC, Yelp, Amazon, Shakespeare, Bible-style, Captions, Political Slant.
- **Evaluation:** Establishes the three-axis evaluation consensus — **transfer strength × content preservation × fluency**.
- **Unslop relevance:** The canonical map of the field; its three-axis evaluation is directly reusable as humanization metrics.
- **Link:** `https://aclanthology.org/2022.cl-1.6`

### 1.2 Mir, Felbo, Obradovich, Rahwan — *Evaluating Style Transfer for Text* — **NAACL 2019**
- **Problem:** Style-transfer evaluation is non-standard and under-correlated with human judgment.
- **Contribution:** Proposes direction-corrected Earth Mover's Distance for transfer intensity, Word Mover's Distance on *style-masked* text for content preservation, and adversarial classification for naturalness.
- **Key finding:** All examined models exhibit **three-way trade-offs** — no system dominates on transfer × content × naturalness simultaneously.
- **Unslop relevance:** Directly usable metric battery; also motivates *plotting* humanization systems on a trade-off surface instead of scoring a single number.
- **Link:** `https://aclanthology.org/N19-1049`

---

## 2. Parallel-Data Style Transfer (Supervised)

### 2.1 Xu, Ritter, Dolan, Grishman, Cherry — *Paraphrasing for Style* — **COLING 2012**
- **Problem:** First systematic treatment of style as a *translation* problem — Early Modern English (Shakespeare) ↔ Modern English.
- **Method:** Phrase-based MT on aligned plays (Shakespeare + No Fear Shakespeare "translations").
- **Dataset:** The `cocoxu/Shakespeare` parallel corpus, still a default benchmark.
- **Unslop relevance:** Establishes that stylistic difference can be modeled with MT machinery *if* you can manufacture parallel data — foreshadows modern paraphrase-pivot methods.
- **Link:** `https://aclanthology.org/C12-1177/`

### 2.2 Rao, Tetreault — *Dear Sir or Madam, May I Introduce the GYAFC Dataset* — **NAACL 2018**
- **Problem:** No large parallel corpus existed for formality transfer.
- **Contribution:** GYAFC — 110K informal↔formal sentence pairs from Yahoo Answers, crowdsourced rewrites. Benchmarks PBMT and NMT baselines; shows automatic metrics (BLEU, PINC) correlate weakly with human judgments on formality, fluency, meaning preservation.
- **Unslop relevance:** The de-facto benchmark dataset; any humanizer claiming formality control should ship GYAFC scores.
- **Link:** `https://aclanthology.org/N18-1012/`

---

## 3. Non-Parallel Style Transfer (Disentanglement Era, 2017–2019)

### 3.1 Hu, Yang, Liang, Salakhutdinov, Xing — *Toward Controlled Generation of Text* — **ICML 2017**
- **Method:** VAE + holistic attribute discriminators; wake-sleep-style training produces disentangled latent codes for sentiment and tense.
- **Contribution:** First end-to-end neural demonstration that *explicit attribute codes* can be decoded to controlled, fluent text.
- **Link:** `https://proceedings.mlr.press/v70/hu17e/hu17e.pdf`

### 3.2 Shen, Lei, Barzilay, Jaakkola — *Style Transfer from Non-Parallel Text by Cross-Alignment* — **NIPS 2017**
- **Method:** Assumes a shared content latent across styles; aligns population distributions of encoded representations with a cross-alignment adversary rather than per-sentence pairs.
- **Tasks:** Sentiment flip (Yelp), word-substitution decipherment, word-order recovery.
- **Unslop relevance:** Canonical proof that style transfer is possible *without* parallel data — the premise behind every "convert AI-ish to human-ish" pipeline.
- **Link:** `https://arxiv.org/abs/1705.09655`

### 3.3 Li, Jia, He, Liang — *Delete, Retrieve, Generate* — **NAACL 2018**
- **Method:** Three-stage prototype editing — (1) delete phrases statistically tied to the source attribute, (2) retrieve target-attribute phrases from a memory, (3) neural fluency recombination.
- **Key finding:** Beats more complex latent-disentanglement models by 22% in "grammatical + appropriate" outputs. Style is often *lexicalized* in a small set of phrases.
- **Unslop relevance:** Strong argument for a **lexical-replacement layer** before any heavier generation step — cheap and interpretable.
- **Link:** `https://aclanthology.org/N18-1169/`

### 3.4 Prabhumoye, Tsvetkov, Salakhutdinov, Black — *Style Transfer Through Back-Translation* — **ACL 2018**
- **Method:** Translate source → pivot language → back; the translation acts as a content-preserving, style-reducing filter. Adversarial training then injects target style.
- **Tasks:** Sentiment, gender, political slant.
- **Link:** `https://arxiv.org/abs/1804.09000`

### 3.5 Lample, Subramanian, Smith, Denoyer, Ranzato, Boureau — *Multiple-Attribute Text Rewriting* — **ICLR 2019**
- **Counter-claim:** Full disentanglement is *unnecessary* and often harmful. A fully entangled seq2seq + denoising auto-encoding + back-translation, conditioned on attribute embeddings, controls multiple attributes (gender, sentiment, product type) better than adversarial disentanglement.
- **Unslop relevance:** Shifted the field away from expensive adversarial disentanglement toward simpler conditional seq2seq — the pattern LLM humanizers inherit today.
- **Link:** `https://arxiv.org/abs/1811.00552`

---

## 4. Decoding-Time / Plug-and-Play Control (2019–2021)

### 4.1 Keskar, McCann, Varshney, Xiong, Socher — *CTRL: A Conditional Transformer Language Model* — **arXiv / Salesforce 2019**
- **Method:** 1.63B-param LM trained with **control codes** (50+ domains, URLs, styles) prepended to every training document, so inference-time codes reliably condition style, genre, and entity distributions.
- **Unslop relevance:** Proof that style is learnable *directly as a prefix*, not a post-hoc filter — the ideological ancestor of system-prompt personas.
- **Link:** `https://arxiv.org/abs/1909.05858`

### 4.2 Dathathri, Madotto, Lan, Hung, Frank, Molino, Yosinski, Liu — *Plug and Play Language Models (PPLM)* — **ICLR 2020**
- **Method:** Freeze a pretrained LM; attach a tiny attribute classifier (bag-of-words or 1-layer) and use gradient updates to *shift the LM's hidden state* at each decoding step toward the attribute.
- **Appeal:** No fine-tuning of the base LM; composable attributes.
- **Weakness:** ~30× slower than greedy decoding; fluency degrades under strong control.
- **Link:** `https://arxiv.org/abs/1912.02164`

### 4.3 Krause, Gotmare, McCann, Keskar, Joty, Socher, Rajani — *GeDi: Generative Discriminator Guided Sequence Generation* — **Findings of EMNLP 2021**
- **Method:** Use a *small* class-conditional LM as a generative discriminator; reweight the base LM's next-token distribution via Bayes' rule using `P(class | prefix + token)`.
- **Wins:** ~30× faster than PPLM; strong detoxification and topic control; zero-shot generalization to unseen topics from keywords.
- **Link:** `https://arxiv.org/abs/2009.06367`

### 4.4 Yang, Klein — *FUDGE: Controlled Text Generation with Future Discriminators* — **NAACL 2021**
- **Method:** Train an attribute predictor on *partial* sequences that estimates whether the finished generation will carry the target attribute; multiply into the LM's token distribution via Bayes.
- **Tasks:** Couplet completion (poetry structure), topic control, formality in machine translation.
- **Unslop relevance:** Framework for controlling *emergent* properties ("will this sound human?") rather than per-token features.
- **Link:** `https://aclanthology.org/2021.naacl-main.276/`

### 4.5 Liu, Sap, Lu, Swayamdipta, Bhagavatula, Smith, Choi — *DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts* — **ACL 2021**
- **Method:** Product-of-experts combination — base LM × *expert* LM (fine-tuned on desired-attribute data) ÷ *anti-expert* LM (fine-tuned on undesired data). Tokens survive only if likely under expert and unlikely under anti-expert.
- **Tasks:** Detoxification, sentiment control; applicable even to GPT-3-scale bases using small experts.
- **Unslop relevance:** The cleanest template for a two-model "make this less AI-sounding" system — fine-tune one expert on human writing, one anti-expert on GPT output, ensemble at decode time.
- **Link:** `https://aclanthology.org/2021.acl-long.522/`

---

## 5. Paraphrase-Pivot Style Transfer

### 5.1 Krishna, Wieting, Iyyer — *Reformulating Unsupervised Style Transfer as Paraphrase Generation (STRAP)* — **EMNLP 2020**
- **Method:** (1) Diverse paraphrase generator strips style, producing pseudo-parallel `(stylized, neutral)` pairs; (2) train per-style *inverse paraphrasers* that re-inject style; (3) route any input through the target style's inverse paraphraser.
- **Key critique:** Surveyed 23 prior papers, showed automatic metrics were *gameable* (trivial copy baselines beat real systems). Proposed fixed metrics.
- **Dataset:** 15M sentences × 11 styles (including Shakespeare, Bible, tweets, lyrics).
- **Unslop relevance:** The strongest unsupervised pipeline when you have style-labeled corpora but no parallel pairs — matches the humanizer setting exactly.
- **Link:** `https://aclanthology.org/2020.emnlp-main.55/`

---

## 6. Politeness, Formality, Detoxification (Applied Styles)

### 6.1 Madaan, Setlur, Parekh, Poczos, Neubig, Yang, Salakhutdinov, Black, Prabhumoye — *Politeness Transfer: A Tag and Generate Approach* — **ACL 2020**
- **Dataset:** 1.39M automatically labeled politeness instances from Enron emails.
- **Method:** *Tag* stylistic attribute tokens in the source, then *generate* the target-style version — hybrid of delete-retrieve-generate and seq2seq.
- **Transfers:** Politeness + 5 other style tasks; SOTA on content preservation and human evaluation.
- **Link:** `https://arxiv.org/abs/2004.14257`

### 6.2 Gehman, Gururangan, Sap, Choi, Smith — *RealToxicityPrompts* — **Findings of EMNLP 2020**
- **Dataset:** 100K naturally occurring web prompts scored by Perspective API.
- **Finding:** Even *non-toxic* prompts reliably induce toxic generations from GPT-2-class models. Compares PPLM, CTRL, domain-adaptive pretraining, word banning — data/compute-intensive methods dominate, but nothing is safe end-to-end.
- **Unslop relevance:** Negative-style framing (detoxification) is the most battle-tested application of decoding-time control; humanization can borrow the same evaluation scaffolding (prompt-then-score).
- **Link:** `https://aclanthology.org/2020.findings-emnlp.301/`

---

## 7. Authorship, Stylometry, Author-Conditioning

### 7.1 Fabien, Villatoro-Tello, Motlicek, Parida — *BertAA: BERT Fine-Tuning for Authorship Attribution* — **ICON 2020**
- **Method:** BERT fine-tune + stylometric/hybrid features in an ensemble.
- **Results:** +5.3% over prior SOTA on Enron, Blog Authorship Corpus, IMDb; +2.7% with stylometry ensemble.
- **Link:** `https://aclanthology.org/2020.icon-main.16/`

### 7.2 Boenninghoff et al. — *PAN 2020/2021 Authorship Verification* (AdHominem Siamese networks)
- **Task:** Same-author verification on fanfiction pairs (~52K–275K pairs).
- **Method:** Siamese networks over linguistic embedding vectors + deep metric learning + Bayes-factor scoring + uncertainty adaptation.
- **Unslop relevance:** Author-verification classifiers are exactly the right **oracle** for author-style transfer — if the verifier can't separate AI-humanized output from the target author's writing, transfer succeeded.
- **Link:** `https://github.com/boenninghoff/pan_2020_2021_authorship_verification`

### 7.3 Huertas-Tato, Martín, Camacho — *Understanding Writing Style in Social Media with a Supervised Contrastively Pre-trained Transformer (STAR)* — **2023**
- **Method:** Supervised contrastive loss on 4.5M texts / 70K authors produces an *authorship embedding* space where same-author texts cluster.
- **Results:** 80% accuracy identifying authors from sets of 1,616 candidates.
- **Unslop relevance:** These embeddings are the dual of style-transfer — a target-style vector one can *steer toward* at decode time.
- **Link:** `https://arxiv.org/abs/2310.11081`

### 7.4 Wang et al. — *Content-Controlled Contrastive Authorship Verification (CAV)* — **arXiv 2022**
- **Problem:** Naive authorship embeddings leak topic/content.
- **Method:** Conditioning contrastive pairs on conversation or domain labels disentangles style from content.
- **Unslop relevance:** Critical — if your style vector encodes topic, "humanized" output will drift semantically.
- **Link:** `https://arxiv.org/pdf/2204.04907`

---

## 8. LLM-Era Style Transfer (2022–2025)

### 8.1 Reif, Ippolito, Yuan, Coenen, Callison-Burch, Wei — *A Recipe for Arbitrary Text Style Transfer with Large Language Models* — **ACL 2022 (Short)**
- **Method:** *Augmented zero-shot* prompting — frame style transfer as a generic sentence-rewriting instruction plus 5–6 diverse in-context examples (e.g., `make this more melodramatic`). No fine-tuning, no target-style exemplars.
- **Key finding:** Unlocks arbitrary *open-vocabulary* styles ("insert a metaphor", "make this sound like a 1920s detective") that labeled-data methods cannot reach.
- **Unslop relevance:** The dominant paradigm for production humanizers today — instruction + few-shot, no per-style training.
- **Link:** `https://aclanthology.org/2022.acl-short.94/`

### 8.2 Suzgun, Melas-Kyriazi, Jurafsky — *Prompt-and-Rerank* — **EMNLP 2022**
- **Method:** Generate k candidates via zero/few-shot prompting; rerank on a weighted combination of textual similarity × target-style strength × fluency.
- **Result:** GPT-J-6B with rerank matches 175B+ models at ~100× less compute.
- **Unslop relevance:** Cheap, verifiable layer — you can reject generations that fail any of the three Mir-style axes.
- **Link:** `https://aclanthology.org/2022.emnlp-main.141/`

### 8.3 Hallinan, Brahman, Lu, Jung, Welleck, Choi — *STEER: Unified Style Transfer with Expert Reinforcement* — **2023**
- **Method:** Auto-generates style-transfer training pairs via prompted paraphrasing; combines DExperts-style product-of-experts decoding with offline + online RL on the style classifier reward.
- **Result:** Beats GPT-3 on style-transfer quality at **226× smaller** model size; supports arbitrary, unknown source styles.
- **Link:** `https://arxiv.org/abs/2311.07167`

### 8.4 Patel, Andrews, Callison-Burch — *Learning to Generate Text in Arbitrary Writing Styles* — **2024** (arXiv 2312.17242)
- **Problem:** Instruction-tuned LLMs struggle to reproduce a specific author's style from small few-shot samples.
- **Method:** Style-embedding-conditioned decoder trained via contrastive authorship representations (Section 7); outperforms in-context prompting on author-imitation benchmarks.
- **Unslop relevance:** Directly on-target for "write like this user" — shows that **explicit author embeddings beat raw few-shot prompting** when samples are scarce.
- **Link:** `https://arxiv.org/abs/2312.17242`

### 8.5 Emulating Author Style: A Feasibility Study of Prompt-Enabled Text Stylization with Off-the-Shelf LLMs — **PERSONALIZE @ EACL 2024**
- **Finding:** GPT-4 / Claude can approximate author style with long, structured prompts but systematically regress to their RLHF "house style" on longer generations. Stylometric fingerprints diverge from the target even when surface reads plausibly.
- **Unslop relevance:** Quantifies the ceiling of pure-prompt humanization and motivates hybrid prompt + decoding-time steering.
- **Link:** `https://aclanthology.org/2024.personalize-1.6/`

### 8.6 *Personalized Text Generation with Fine-Grained Linguistic Control* — **arXiv 2402.04914, 2024**
- **Method:** Decomposes "style" into measurable linguistic dimensions (lexical diversity, sentence length, POS distributions) and uses them as controllable sliders during generation.
- **Unslop relevance:** Operationalizes style as a *vector of measurable features* rather than a monolithic label — directly mappable to a humanizer UI ("more varied sentence length", "lower lexical repetition").
- **Link:** `https://arxiv.org/abs/2402.04914`

### 8.7 *Neurobiber: Fast and Interpretable Stylistic Feature Extraction* — **arXiv 2502.18590, 2025**
- **Method:** Neural re-implementation of Biber's Multidimensional Analysis extracting 96 interpretable stylistic features.
- **Unslop relevance:** Drop-in feature extractor for measuring and steering the "register" axis — exactly the kind of auditable signal needed to claim a rewrite is "more human".
- **Link:** `https://arxiv.org/abs/2502.18590`

---

## 9. Post-2025 Findings (April 2025–April 2026)

### 9.1 Wang et al. — *Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors* — **EMNLP 2025 Findings**
- **Problem:** Does in-context prompting faithfully replicate a specific individual's writing style from a few samples?
- **Contribution:** Comprehensive evaluation across GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3, and Llama-4-Maverick using four complementary metrics: authorship attribution, authorship verification, style matching, and AI detection.
- **Key finding:** All tested models — including frontier ones — fail to reliably imitate *implicit* writing styles of ordinary authors via in-context learning. Few-shot prompting yields up to 23.5× higher style-matching accuracy than zero-shot, but the ceiling is still far from the target author's fingerprint.
- **Unslop relevance:** Empirical proof that prompt-only approaches remain insufficient for individual voice cloning as of late 2025. Directly motivates embedding- or fine-tune-based approaches over pure prompting.
- **Link:** `https://arxiv.org/abs/2509.14543` | GitHub: `https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation`

### 9.2 Jemama et al. — *How Well Do LLMs Imitate Human Writing Style?* — **arXiv 2509.24930, 2025**
- **Key finding:** High-fidelity stylistic imitation and statistical undetectability are *separable*. Human essays average perplexity 29.5; stylistically matched LLM outputs average 15.2. A model can pass a style-similarity test while still being trivially detectable by a perplexity classifier.
- **Unslop relevance:** Cleaves the "humanization" objective into two distinct axes — style fidelity and statistical naturalness — that must be optimized independently. Directly challenges any single-metric evaluation of "humanized" output.
- **Link:** `https://arxiv.org/abs/2509.24930`

### 9.3 Huang, Chen et al. — *Authorship Attribution in the Era of LLMs: Problems, Methodologies, and Challenges* — **SIGKDD Explorations 2025**
- **Contribution:** Survey systematizing authorship attribution into four problems: (1) attributing unknown texts to human authors, (2) detecting LLM-generated texts, (3) identifying which LLM generated a text, and (4) classifying co-authored texts. Covers state-of-the-art methods, datasets, and benchmarks. Living paper list at `https://llm-authorship.github.io/`.
- **Unslop relevance:** Canonical reference map for the authorship verification side of humanization evaluation. The four-problem taxonomy is directly useful for deciding which evaluation oracle is appropriate.
- **Link:** `https://dl.acm.org/doi/abs/10.1145/3715073.3715076` | arXiv: `https://arxiv.org/abs/2408.08946`

### 9.4 Yang & Carpuat — *Steering Large Language Models with Register Analysis for Arbitrary Style Transfer* — **arXiv 2505.00679, 2025**
- **Method:** Prompts LLMs to analyze exemplar style using Biber's Multidimensional Register Analysis (MDA) framework before generating style-transferred output. The structured register descriptor serves as an intermediate representation that LLMs can reliably interpret.
- **Result:** Improved style-transfer strength vs. baselines, with a large gain in meaning preservation — the content-drift failure mode is partially addressed.
- **Unslop relevance:** Shows Neurobiber-style Biber features are not just an evaluation tool but a *generation conditioning* interface for arbitrary style transfer without fine-tuning.
- **Link:** `https://arxiv.org/abs/2505.00679`

### 9.5 *Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies* — **arXiv 2604.14111, April 2026**
- **Contribution:** Large-scale analysis of stylistic variation across 11 LLMs spanning 8 genres and 4 decoding strategies using Biber's lexicogrammatical features. Key finding: genre exerts a stronger influence on style than the generating model, but instruction-tuned chat models cluster together in stylistic space regardless of genre — RLHF and instruction tuning push different models toward the same stylistic attractor.
- **Unslop relevance:** Explains why "the AI voice" is a real, model-agnostic phenomenon and not an artifact of one vendor's training choices. Confirms that RLHF is the proximate cause of stylistic homogenization. Decoding strategy has less effect than model, weakening the case for decoding-time control as the sole solution.
- **Link:** `https://arxiv.org/abs/2604.14111`

### 9.6 *How LLMs Distort Our Written Language* — **arXiv 2603.18161, March 2026**
- **Key findings:** (1) LLMs alter intended meaning even when prompted only for grammar edits. (2) Heavy LLM use caused a ~70% increase in essays that stayed neutral on contested questions — the "blandification" effect. (3) Of 75,000 ICLR 2026 reviews, 21%+ were LLM-generated and another 39% showed LLM editing traces; LLM reviews shift evaluative criteria toward reproducibility/scalability over clarity/impact. (4) Users self-reported their LLM-edited writing as less creative and not in their voice.
- **Unslop relevance:** Quantifies the scale and semantic depth of the homogenization problem Unslop addresses. The 70% neutralization figure and the ICLR peer-review contamination are the strongest external framing for why voice preservation matters.
- **Link:** `https://arxiv.org/abs/2603.18161`

### 9.7 *ZeroStylus: Implementing Long Text Style Transfer with LLMs through Dual-Layered Sentence and Paragraph Structure Extraction and Mapping* — **arXiv 2505.07888, 2025**
- **Method:** Zero-shot long-text style transfer via hierarchical template acquisition — sentence-level stylistic adaptation combined with paragraph-level structural coherence. Dynamically builds sentence and paragraph template repositories from reference texts; no parallel corpora or fine-tuning required.
- **Unslop relevance:** First serious attack on paragraph- and document-level style consistency, which is the primary open gap in the field (all prior benchmarks are sentence-level). Directly relevant to long-form humanization.
- **Link:** `https://arxiv.org/abs/2505.07888`

### 9.8 Tan et al. — *Instant Personalized Large Language Model Adaptation via Hypernetwork (Profile-to-PEFT)* — **arXiv 2510.16282, 2025**
- **Method:** A hypernetwork trained end-to-end maps an encoded user profile directly to a full set of LoRA adapter weights — eliminating per-user training at deployment. At inference, a user's profile is encoded and the hypernetwork synthesizes their personalized LoRA in 0.57 seconds (vs. 20.44 seconds for standard per-user LoRA training), a 33× speedup.
- **Unslop relevance:** If style can be captured in a compact profile, hypernetwork synthesis of user-specific LoRAs could make cold-start voice cloning practical without per-user training runs.
- **Link:** `https://arxiv.org/abs/2510.16282` | GitHub: `https://github.com/TamSiuhin/P2P`

### 9.9 *GRAVITY: Personalized Text Generation via Profile-Grounded Synthetic Preferences* — **arXiv 2510.11952, 2025**
- **Method:** Generates synthetic preference data grounded in user profiles that encode demographic, cultural (Hofstede, Schwartz, World Values Survey), and psychological (Big Five OCEAN) frameworks. Fine-tunes Llama-3.1-8B-Instruct with DPO on this synthetic data.
- **Result:** 4%+ higher preference gains vs. baselines across four national cultures (USA, Brazil, Japan, India); preferred over baselines 86%+ of the time in user studies.
- **Unslop relevance:** Demonstrates that explicit cultural and psychological profiling produces verifiably better-personalized text than generic fine-tuning. Cultural and personality dimensions are underused in voice-capture tools.
- **Link:** `https://arxiv.org/abs/2510.11952`

### 9.10 Kasner et al. — *Benchmark of Stylistic Variation in LLM-Generated Texts* — **arXiv 2509.10179, 2025**
- **Contribution:** Systematic benchmark evaluating how much stylistic variation LLMs actually produce across prompting conditions. Complements the Jemama and interpretable-variation papers.
- **Link:** `https://arxiv.org/abs/2509.10179`

### 9.11 *Is Your Writing Being Mimicked by AI? Unveiling Imitation with Invisible Watermarks in Creative Writing* — **arXiv 2504.00035, April 2025**
- **Method:** WIND (Watermarking via Implicit and Non-disruptive Disentanglement) embeds invisible watermarks in creative writing corpora to detect unauthorized AI imitation. Achieves F1 above 98% in verifying copyright ownership against imitation attempts.
- **Relevance:** Emerging defensive capability that intersects with style transfer — watermarks become adversarial targets for humanizers aiming to imitate a specific corpus. Copyright law dimension of style imitation is now an active research front.
- **Link:** `https://arxiv.org/abs/2504.00035`

---

## 10. Patterns

1. **Three-axis evaluation consensus.** Every serious paper since Mir 2019 scores on transfer strength × content preservation × fluency/naturalness and acknowledges the trade-off. Single-number "humanization scores" will not pass peer review.
2. **Disentanglement is out, attribute-conditioning is in.** The Hu/Shen 2017 disentanglement line peaked in 2018; Lample 2019, CTRL, GeDi, DExperts all show that *entangled models with explicit attribute signals* dominate empirically and are simpler.
3. **Decoding-time steering has beaten fine-tuning on cost/flexibility.** PPLM → GeDi → FUDGE → DExperts → STEER is a steady improvement in speed and attribute composability; the frontier today is small-expert ensembles rather than retraining the base LM. However, the interpretable-variation paper (2604.14111, 2026) shows decoding strategy is weaker than model choice — architecture matters more than sampling tricks.
4. **Paraphrase as the universal pivot.** STRAP's "paraphrase-then-inverse-paraphrase" recipe, and its LLM descendants, are the default when parallel data is missing — and they sidestep the content-drift failure mode.
5. **Style = embeddings, not labels.** Contrastive authorship learning (STAR, CAV) produces continuous author vectors that plug cleanly into prompt prefixes, activation steering, or reward models — the new substrate for personalization.
6. **Lexical/surface features still carry most of the signal.** Delete-retrieve-generate, tag-and-generate, and Biber-feature papers all confirm that style is heavily lexicalized — a strong cheap baseline.
7. **Style fidelity and statistical undetectability are separable objectives.** Jemama 2025 shows that high perplexity-match style can still be trivially detectable by perplexity classifiers (human perplexity ~29.5 vs. matched LLM output ~15.2). Humanization systems must be evaluated on both axes independently.
8. **RLHF is the proximate cause of stylistic homogenization.** Biber-feature analysis (2604.14111) shows chat/instruction-tuned variants of different models cluster together in stylistic space — the "AI voice" is not model-specific but RLHF-specific. Removing it requires interventions at the RLHF or fine-tuning layer, not just prompting.

## 11. Trends

- **From categorical to open-vocabulary style.** Reif 2022 reframes style transfer as arbitrary natural-language instructions; STEER 2023 handles unknown source styles; Yang & Carpuat 2025 uses structured register descriptors as the intermediate. The target is no longer a fixed label set.
- **From global style to per-author style.** Patel 2024 and the author-embedding line shift focus from "formal vs. informal" to "write like *this specific user*". The EMNLP 2025 "Catch Me If You Can" paper confirms this is still an open challenge even for frontier models.
- **Small-expert, frozen-base architectures.** DExperts and STEER show that a frozen LLM plus a small fine-tuned expert is the dominant production pattern — relevant for latency-sensitive humanizer APIs.
- **Stylometry as both detector and oracle.** PAN verifiers and STAR embeddings are used *simultaneously* as evaluation oracles and as training rewards — closing the loop between AI-text detection research (Section 05) and humanization. Neurobiber + Yang & Carpuat 2025 extend this to register-conditioned generation.
- **Register/linguistic features as controllable sliders.** Neurobiber + fine-grained linguistic control papers + Yang & Carpuat 2025 move style out of "vibes" territory into auditable Biber dimensions.
- **Hypernetwork-synthesized adapters may replace per-user LoRA.** Profile-to-PEFT (2510.16282) generates personalized LoRA weights in 0.57s from a user profile, enabling cold-start personalization without training runs. Expected to mature into practical tooling by 2026–2027.
- **Long-form style transfer is finally being addressed.** ZeroStylus (2505.07888) is the first serious attack on paragraph- and document-level consistency. Still zero-shot; quality vs. fine-tuned methods unclear.
- **Copyright and watermarking are entering the style-transfer problem.** WIND (2504.00035) embeds detectable watermarks in training corpora; LLM imitation of specific authors is becoming a legal rather than purely technical question after Anthropic's 2025 copyright settlement.

## 12. Gaps (updated April 2026)

- **Long-form author style.** ZeroStylus (2025) is the first attempt at document-level transfer, but no benchmark yet measures paragraph- or document-level voice consistency against a held-out author profile. GYAFC, Yelp, Shakespeare are still sentence-level.
- **Human evaluation of "naturalness" vs. AI-detector evasion.** Jemama 2025 shows these two objectives are separable but still co-conflated in most evaluations. No benchmark separately scores "sounds human to a reader" vs. "has human-like perplexity."
- **Content preservation under heavy stylization.** STRAP warned that attribute transfer warps semantics; Yang & Carpuat 2025 shows this is partially addressable via register-conditioned prompting, but no widely adopted metric measures semantic fidelity under strong style shift.
- **Author-conditioning with tiny data.** "Catch Me If You Can" (EMNLP 2025) confirms that even frontier LLMs fail at implicit style imitation from a few samples. Cold-start from 200–500 words remains unsolved.
- **Controllability of "humanness" as an attribute.** Still no public benchmark defining "human-like" as a first-class labeled style axis. The perplexity-vs-style-fidelity split (Jemama 2025) makes this more tractable now — two separate evaluation datasets could be constructed — but none exists.
- **Stylometric robustness of humanized output.** No paper reports whether humanized output matches a target author's Biber or Writeprints fingerprint. The interpretable-variation results (2604.14111) suggest model-specific fingerprints are durable enough to cluster even under style-transfer prompting.
- **Hypernetwork cold-start voice quality.** Profile-to-PEFT synthesizes adapters from profiles, but profile construction still requires substantial user data; true cold-start from 200 words is untested.
- **Multilingual + cross-register transfer.** Near-all benchmarks are English.

---

## 13. Sources

- Jin et al. 2022 — `https://aclanthology.org/2022.cl-1.6`
- Mir et al. 2019 — `https://aclanthology.org/N19-1049`
- Xu et al. 2012 — `https://aclanthology.org/C12-1177/`
- Rao & Tetreault 2018 (GYAFC) — `https://aclanthology.org/N18-1012/`
- Hu et al. 2017 — `https://proceedings.mlr.press/v70/hu17e/hu17e.pdf`
- Shen et al. 2017 (Cross-Alignment) — `https://arxiv.org/abs/1705.09655`
- Li et al. 2018 (Delete-Retrieve-Generate) — `https://aclanthology.org/N18-1169/`
- Prabhumoye et al. 2018 — `https://arxiv.org/abs/1804.09000`
- Lample/Subramanian et al. 2019 — `https://arxiv.org/abs/1811.00552`
- Keskar et al. 2019 (CTRL) — `https://arxiv.org/abs/1909.05858`
- Dathathri et al. 2020 (PPLM) — `https://arxiv.org/abs/1912.02164`
- Krause et al. 2021 (GeDi) — `https://arxiv.org/abs/2009.06367`
- Yang & Klein 2021 (FUDGE) — `https://aclanthology.org/2021.naacl-main.276/`
- Liu et al. 2021 (DExperts) — `https://aclanthology.org/2021.acl-long.522/`
- Krishna et al. 2020 (STRAP) — `https://aclanthology.org/2020.emnlp-main.55/`
- Madaan et al. 2020 (Politeness Transfer) — `https://arxiv.org/abs/2004.14257`
- Gehman et al. 2020 (RealToxicityPrompts) — `https://aclanthology.org/2020.findings-emnlp.301/`
- Fabien et al. 2020 (BertAA) — `https://aclanthology.org/2020.icon-main.16/`
- Boenninghoff et al. 2020/2021 (PAN AV) — `https://github.com/boenninghoff/pan_2020_2021_authorship_verification`
- Huertas-Tato et al. 2023 (STAR) — `https://arxiv.org/abs/2310.11081`
- Wang et al. 2022 (Content-Controlled CAV) — `https://arxiv.org/pdf/2204.04907`
- Reif et al. 2022 (Augmented Zero-Shot) — `https://aclanthology.org/2022.acl-short.94/`
- Suzgun et al. 2022 (Prompt-and-Rerank) — `https://aclanthology.org/2022.emnlp-main.141/`
- Hallinan et al. 2023 (STEER) — `https://arxiv.org/abs/2311.07167`
- Patel et al. 2024 (Arbitrary Writing Styles) — `https://arxiv.org/abs/2312.17242`
- Emulating Author Style 2024 — `https://aclanthology.org/2024.personalize-1.6/`
- Personalized Text Generation w/ Fine-Grained Linguistic Control 2024 — `https://arxiv.org/abs/2402.04914`
- Neurobiber 2025 — `https://arxiv.org/abs/2502.18590`
- **[NEW]** Wang et al. 2025 (Catch Me If You Can, EMNLP 2025) — `https://arxiv.org/abs/2509.14543`
- **[NEW]** Jemama et al. 2025 (How Well Do LLMs Imitate) — `https://arxiv.org/abs/2509.24930`
- **[NEW]** Huang et al. 2025 (Authorship Attribution Survey, SIGKDD) — `https://arxiv.org/abs/2408.08946`
- **[NEW]** Yang & Carpuat 2025 (Register Analysis for Style Transfer) — `https://arxiv.org/abs/2505.00679`
- **[NEW]** Interpretable Stylistic Variation 2026 — `https://arxiv.org/abs/2604.14111`
- **[NEW]** How LLMs Distort Our Written Language 2026 — `https://arxiv.org/abs/2603.18161`
- **[NEW]** ZeroStylus 2025 (Long Text Style Transfer) — `https://arxiv.org/abs/2505.07888`
- **[NEW]** Profile-to-PEFT / Hypernetwork 2025 — `https://arxiv.org/abs/2510.16282`
- **[NEW]** GRAVITY 2025 (Profile-Grounded DPO) — `https://arxiv.org/abs/2510.11952`
- **[NEW]** Benchmark of Stylistic Variation 2025 — `https://arxiv.org/abs/2509.10179`
- **[NEW]** WIND Watermarking 2025 — `https://arxiv.org/abs/2504.00035`
