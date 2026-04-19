# Style Transfer & Voice — Angle C: Open-Source

**Category:** Style Transfer & Voice
**Angle:** C — Open-Source repos, libraries, and prompt frameworks
**Project context:** Humanizing AI output and thinking — adopting a user's voice, erasing "LLM-isms," and steering generation toward specific stylistic attributes.
**Research value: high** — The open-source landscape here is dense and layered, with three distinct generations of tooling (classical controllable-generation → neural style transfer → LLM-era voice cloning) and clear gaps that Humanizer can exploit.

---

## Overview

Open-source style/voice work clusters into five lineages, each with a different bet on where control should live:

1. **Decoding-time steering** (PPLM, GeDi, FUDGE) — cheap, model-agnostic, no fine-tune.
2. **Pre-trained controllable LMs** (CTRL) — control codes baked into pretraining.
3. **Neural style transfer** (StyleTransformer, Styleformer, Tag-and-Generate, DualRL, StyIns) — attribute-level (formal↔casual, polite↔rude, sentiment).
4. **Stylometry & anonymization** (JStylo, Anonymouth, stylometric-transfer) — measure and erase authorial fingerprint.
5. **LLM-era voice cloning** (TinyStyler, StyleTunedLM, StyleLLM, LoRA personal-voice projects, Claude/OpenCode "skills," prompt-based style generators) — adopt an individual's idiolect from a small sample.

The center of gravity has moved decisively from (1)–(3) toward (4)–(5) since 2023. The older methods still matter because they encode *what* style is (lexical markers, n-grams, discourse features) — knowledge the LLM-era tools mostly treat as a black box.

---

## Repositories

### 1. `uber-research/PPLM` — Plug and Play Language Models

- **URL:** https://github.com/uber-research/PPLM
- **Stars / activity:** ~1.15k stars, last updated Feb 2024, Apache-2.0, Python.
- **Approach:** Attribute models (bag-of-words lists or tiny single-layer discriminators, ~100,000× smaller than the LM) push GPT-2 hidden activations during sampling via gradients — no LM fine-tuning.
- **README-style quote (from paper/repo):** "Plug in simple attribute models representing the desired steering objective… 100,000 times fewer parameters than the language model itself, without any further training."
- **Humanizer relevance:** Cheapest way to bias toward "human-like" lexical/semantic attributes on top of any open base model. Slow at inference, but the attribute model trick is directly reusable for an "anti-LLM-ism" classifier.

### 2. `salesforce/GeDi` — Generative Discriminator Guided Generation

- **URL:** https://github.com/salesforce/GeDi
- **Stars / activity:** Archived June 2025, Python, includes GPT-3 API support.
- **Approach:** Small class-conditional LMs compute per-token Bayes-rule reweighting of a larger LM's logits. Reports ~30× faster than PPLM with better diversity.
- **Humanizer relevance:** Same attribute-control goal as PPLM but practical at interactive latency. Natural fit for a "humanness" discriminator scoring candidate tokens against an AI-detector signal.

### 3. `yangkevin2/naacl-2021-fudge-controlled-generation` — FUDGE

- **URL:** https://github.com/yangkevin2/naacl-2021-fudge-controlled-generation
- **Stars / activity:** ~102 stars, MIT, Python.
- **Approach:** Trains an attribute predictor over *partial sequences*; reweights the base model's output distribution via Bayesian decomposition. Requires only logits — works with frozen black-box-ish models. Demonstrated on formality transfer, topic control, poetry couplet completion.
- **Humanizer relevance:** Strong conceptual match — "future discriminator" is exactly the shape of a humanness detector applied during decoding. Composable: stack multiple predictors (e.g., human-tone + anti-em-dash + informality).

### 4. `salesforce/ctrl` — Conditional Transformer Language Model

- **URL:** https://github.com/salesforce/ctrl
- **Stars / activity:** ~1.88k stars, archived May 2025, BSD-3-Clause.
- **Approach:** 1.63B-param LM pretrained on 50+ control codes derived from URL/domain structure (Wikipedia, Reddit subreddits, etc.). Controls style/genre/entities/dates via prepended tokens.
- **Humanizer relevance:** Historical — control-code-in-prompt is the intellectual ancestor of every "act as X" system-prompt pattern. Not worth running today, but the code-taxonomy is instructive when designing a style ontology.

### 5. `tag-and-generate/tagger-generator` — Tag-and-Generate (Politeness Transfer)

- **URL:** https://github.com/tag-and-generate/tagger-generator
- **Stars / activity:** ~57 stars, MIT, Python, companion to ACL 2020 paper.
- **Approach:** Two-stage pipeline — a *tagger* identifies style-carrying tokens, a *generator* rewrites them toward the target style. Trained on politeness but the pattern is general.
- **Humanizer relevance:** Interpretability win — you see *which* tokens are AI-tells before rewriting them. Useful scaffold for "show the user what got humanized."

### 6. `fastnlp/style-transformer` — StyleTransformer

- **URL:** https://github.com/fastnlp/style-transformer
- **Stars / activity:** Python/PyTorch, last updated Feb 2022, official code for Dai et al. ACL 2019.
- **Approach:** Transformer + discriminator with self-reconstruction, cycle-reconstruction, and adversarial losses. Unpaired style transfer *without* disentangled latent representations — rejects the "separate content from style" assumption.
- **Humanizer relevance:** Canonical neural baseline. Aging but still the reference point for every "unpaired text-to-text" style system.

### 7. `PrithivirajDamodaran/Styleformer` — Styleformer

- **URL:** https://github.com/PrithivirajDamodaran/Styleformer
- **Stars / activity:** ~493 stars, pip-installable, last updated Dec 2023.
- **Approach:** Ready-to-use neural style transfer for formal↔casual, active↔passive, and fine-grained variants. Ships trained models, aimed at data augmentation, assisted writing, and post-processing of generated text.
- **Humanizer relevance:** Most deployable classic-style-transfer option today. Good candidate for a stage in a humanization pipeline (e.g., AI draft → Styleformer casual pass → LLM voice-match pass).

### 8. `luofuli/DualRL` — Dual Reinforcement Learning for Unsupervised Style Transfer

- **URL:** https://github.com/luofuli/DualRL
- **Stars / activity:** ~283 stars, MIT, Python, IJCAI 2019.
- **Approach:** One-step direct mapping (rejects two-step content/style separation). Source↔target treated as a dual task with two rewards: style accuracy and content preservation. +8–10 BLEU over prior SOTA on Yelp/GYAFC.
- **Humanizer relevance:** RL-from-rewards framing is directly transferable: swap style accuracy for humanness-detector score, content preservation for semantic similarity — you get an RL-based humanizer.

### 9. `XiaoyuanYi/StyIns` — Style Instance Supported Latent Space

- **URL:** https://github.com/XiaoyuanYi/StyIns
- **Stars / activity:** ~38 stars, Python, IJCAI 2020.
- **Approach:** Few-shot style transfer driven by a handful of "style instance" exemplars rather than a style label. Uses a learned latent space conditioned on the exemplar set.
- **Humanizer relevance:** Few-shot-by-example framing is exactly what voice cloning needs — "make it sound like these five emails I wrote." Predecessor in spirit to TinyStyler.

### 10. `zacharyhorvitz/tinystyler` — TinyStyler (EMNLP 2024)

- **URL:** https://github.com/zacharyhorvitz/tinystyler
- **README quote:** "Code for TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings, EMNLP 2024 Findings."
- **Approach:** ~800M-param model conditioned on authorship embeddings; unsupervised pre-training on reconstruction, then fine-tune on filtered transfer pairs. Reports outperforming GPT-4 on authorship-style transfer.
- **Humanizer relevance:** Strongest recent prior art. Authorship embeddings are the right abstraction for a user's voice, and the "small model beats GPT-4 on this narrow task" result is a direct existence proof that a humanizer doesn't need a frontier LLM.

### 11. `stylellm/stylellm_models` — StyleLLM

- **URL:** https://github.com/stylellm/stylellm_models
- **README quote (translated):** "StyleLLM 文风大模型: text style transfer based on Large Language Model."
- **Stars / activity:** ~355 stars. Four Yi-6B fine-tunes, one per Chinese classical novel (Three Kingdoms, Journey West, Water Margin, Dream of the Red Chamber); AWQ 4-bit quantized versions available.
- **Humanizer relevance:** Proof-of-concept that full-model fine-tunes on a single corpus can produce convincingly consistent voice, and that quantization makes it deployable. Template for "one LoRA per user voice" at scale.

### 12. `ngpepin/stylometric-transfer` — Interpretable Stylometric Transfer

- **URL:** https://github.com/ngpepin/stylometric-transfer
- **README quote:** "Interpretable stylometric profiling + author-style transfer built on explicit and LLM-generated JSON fingerprints and local measurements. Fingerprint your corpus, inspect/visualize signals, then LLM-generate stylistically similar text with meaning preserved, deterministic post-processing, normalization controls, and deviation reports. CLI + API."
- **Humanizer relevance:** Only repo in the list that tries to bridge classical stylometry with LLM generation — explicit JSON fingerprints + deviation reports is close to what a user-facing "why does this sound like you" explainer needs.

### 13. `psal/jstylo` — JStylo (authorship attribution)

- **URL:** https://github.com/psal/jstylo
- **Stars / activity:** ~190 stars, BSD-3, Java, actively versioned (v2.9.0).
- **Approach:** Drexel PSAL's stylometric feature extractor + ML classifier framework. Implements Writeprints-family features (word length, n-grams, function words, POS patterns).
- **Humanizer relevance:** *The* reference implementation of Writeprints-style features. Needed for any serious "measure how much this sounds like the user" evaluation — LLM-based similarity alone is insufficient.

### 14. `psal/anonymouth` — Anonymouth (style anonymization)

- **URL:** https://github.com/psal/anonymouth
- **Stars / activity:** ~1.94k stars, BSD-3, Java.
- **Approach:** Companion to JStylo. Uses its feature extractors to identify style markers to *remove*, guiding the user to rewrite toward a more anonymous profile.
- **Humanizer relevance:** Dual-use inspiration — the same loop (detect distinctive features → suggest rewrites) is how you'd "de-AI" text. Worth reading for the UX/iteration pattern more than the code, which is dated.

### 15. `cauchy221/StyleTunedLM` — LoRA for Style

- **URL:** https://github.com/cauchy221/StyleTunedLM
- **README quote:** "Official repository of the paper: Customizing Large Language Model Generation Style using Parameter-Efficient Finetuning."
- **Approach:** LoRA training scripts at multiple data sizes, plus linguistic-alignment evaluation metrics for style fidelity.
- **Humanizer relevance:** One of the few repos to publish *evaluation* for style-fidelity LoRAs, not just training scripts. Borrow the metrics.

### 16. `Muneeb1030/FineTune-Tiny-Llama` — Personal-Voice LoRA Pipeline

- **URL:** https://github.com/Muneeb1030/FineTune-Tiny-Llama
- **Approach:** End-to-end pipeline to mimic one person's writing — Selenium scrape → pyMuPDF clean → OpenAI-API reformat → LoRA via Llama-Factory in Colab → eyeballed eval.
- **Humanizer relevance:** Representative of the long tail of hobbyist "clone-my-voice" repos. Useful as a data-engineering reference (scrape → clean → format), not as research.

### 17. `DidierRLopes/fine-tune-llm` — Apple-Silicon Personal-Voice LoRA

- **URL:** https://github.com/DidierRLopes/fine-tune-llm
- **Approach:** Config-driven fine-tuning pipeline on Apple Silicon via MLX, aimed at personal use (author fine-tuned Phi-3 mini on his blog, updating ~0.08% of weights).
- **Humanizer relevance:** Shows that a credible personal-voice LoRA is feasible on a laptop — important signal for on-device humanization without round-tripping user text to a cloud API.

### 18. `shandley/claude-style-guide` — Anti-LLM-ism Styleguide Generator

- **URL:** https://github.com/shandley/claude-style-guide
- **README quote:** "Pipeline to analyze Claude Opus 4.5 writing patterns and generate a styleguide for avoiding LLM-isms."
- **Approach:** Analyze documents → detect AI patterns via a `prose-check` command → emit an actionable styleguide listing words/phrases to avoid with human alternatives.
- **Humanizer relevance:** Directly on-target — same product thesis as Humanizer, smaller scope. Worth studying the taxonomy of "LLM-isms" they enumerate.

### 19. `lout33/writing-style-skill` — Claude Code / OpenCode Skill

- **URL:** https://github.com/lout33/writing-style-skill
- **README quote:** "Transform AI-generated text into your personal voice. Skill for Claude Code / OpenCode."
- **Approach:** Export real user writing (Gmail, WhatsApp, Slack, X) → have the LLM analyze patterns → save to a style file → auto-apply to future responses.
- **Humanizer relevance:** Shows the "Skill" format working end-to-end as a UX — no fine-tuning, pure in-context + persistent style file. Low ceiling on fidelity, but near-zero activation energy.

### 20. `stephenhsklarew/WritingStylePromptGenerator`

- **URL:** https://github.com/stephenhsklarew/WritingStylePromptGenerator
- **README quote:** "Analyze your writing samples and generate AI style prompts that capture your unique voice, tone, and patterns. Works with local files or Google Drive."
- **Approach:** Python tool that ingests writing samples (local or Drive), calls OpenAI/Anthropic/Google, emits a Markdown style-guide prompt for reuse in any chat UI.
- **Humanizer relevance:** Minimum-viable version of a voice cloner — no training, just a generated system prompt. Competitive baseline to beat on fidelity.

### 21. `viktorbezdek/definitive-llm-writing-style-guide` — Style Framework

- **URL:** https://github.com/viktorbezdek/definitive-llm-writing-style-guide
- **Approach:** Meta-framework that decomposes "style" across Big-Five personality traits plus assertiveness/empathy/optimism, with guidance for how each dimension maps to generated text.
- **Humanizer relevance:** Ontology source. Most projects under-specify what "voice" means; this one over-specifies it, which is easier to subset from.

### 22. `zhijing-jin/Text_Style_Transfer_Survey` — Survey Reading List

- **URL:** https://github.com/zhijing-jin/Text_Style_Transfer_Survey
- **Stars / activity:** ~245 stars.
- **Contents:** Paper list organized by method (disentanglement, prototype editing, back-translation, paraphrasing) and subtask (formality, politeness, simplification, detoxification). Companion to the MIT CL 2022 survey "Deep Learning for Text Style Transfer: A Survey."
- **Humanizer relevance:** Canonical entry point. Start here before re-inventing any mechanism.

### 23. `yd1996/awesome-text-style-transfer` — Awesome List

- **URL:** https://github.com/yd1996/awesome-text-style-transfer
- **Contents:** Supervised/unsupervised split, with code links for the foundational works (Hu et al. ICML'17, Shen et al. NIPS'17, Li et al. NAACL'18, Prabhumoye et al. ACL'18).
- **Humanizer relevance:** Secondary index, broader than the survey list but less curated.

---

## Patterns

- **Attribute-level → author-level.** 2017–2022 work focuses on binary/attribute axes (sentiment, formality, politeness, toxicity). 2023+ work reframes style as a per-author embedding or LoRA — the "axis" is now "be this specific person."
- **Decoding-time steering has a second life.** PPLM/GeDi/FUDGE looked obsoleted by RLHF fine-tuning, but their no-fine-tune stance is a near-perfect match for humanizing *closed* model outputs via API logits or re-sampling. Expect revival.
- **Two-stage pipelines recur.** Tag-and-Generate (tag → rewrite), Anonymouth (detect → remove), stylometric-transfer (fingerprint → generate), shandley/claude-style-guide (detect → guide). "Find the AI-tells, then rewrite them" is the dominant mental model.
- **Evaluation is the bottleneck.** Most LoRA/voice-clone repos evaluate by eyeballing. Only StyleTunedLM, TinyStyler, and the JStylo-adjacent ecosystem publish real style-fidelity metrics. Whoever builds reliable style evals owns the category.
- **The "skill file" pattern is emerging.** Claude Code / OpenCode skills (`lout33/writing-style-skill`, `shandley/claude-style-guide`) are quietly standardizing on "analyze once, save a Markdown style file, reuse forever." That's a shippable format.

## Trends

- **Small models are winning narrow tasks.** TinyStyler (~800M) beating GPT-4 on authorship transfer is the canonical data point. For humanization specifically, a specialized 1–3B model + user-LoRA likely beats frontier general-purpose models.
- **Authorship embeddings over style labels.** Moving from "formal↔casual" to "this 300-token embedding describes your voice" is the clearest post-2024 trend (TinyStyler, StyIns lineage).
- **Stylometry is coming back.** Classical Writeprints-style features are being rediscovered as (a) interpretability signal, (b) training reward, and (c) evaluation metric — because LLM-based similarity scores are polluted by the same LLM-isms you're trying to remove.
- **On-device fine-tuning is crossing the viability line.** DidierRLopes's MLX Phi-3 LoRA and the general tsmatz/LoRA-from-scratch work suggest laptop-grade personal-voice models are real by late-2025.

## Gaps

- **No open-source "humanizer" with a published detector-evasion benchmark.** Lots of commercial tools claim GPTZero/Originality evasion; almost zero open repos publish scores against any detector. Open here.
- **No public authorship-embedding model on permissive license.** TinyStyler's embeddings are tied to its paper; no drop-in, pip-installable equivalent of sentence-transformers for authorship exists.
- **No unified eval harness.** Style transfer still uses per-paper Yelp/GYAFC splits with BLEU + style-classifier accuracy; voice-clone repos don't evaluate at all. Nothing like HumanEval exists for "does this sound like the user."
- **Sparse LoRA-registry tooling.** Lots of "how I fine-tuned on my blog" one-offs, no infrastructure for managing N-users × M-tasks LoRAs, hot-swapping, or merging.
- **Weak support for ongoing drift.** All voice-clone projects assume "fit once"; none handle "my style changed, update the model" as a first-class operation.
- **The legacy stylometry tools are unmaintained.** JStylo/Anonymouth are Java-from-2013. A modern Python rewrite of the feature extractors, ideally with HuggingFace-style APIs, is an open niche.

## Sources

- https://github.com/uber-research/PPLM — PPLM (Uber Research, 2019/2024)
- https://github.com/salesforce/GeDi — GeDi (Salesforce, archived 2025)
- https://github.com/yangkevin2/naacl-2021-fudge-controlled-generation — FUDGE (NAACL 2021)
- https://github.com/salesforce/ctrl — CTRL (Salesforce, archived 2025)
- https://github.com/tag-and-generate/tagger-generator — Tag-and-Generate (ACL 2020)
- https://github.com/fastnlp/style-transformer — StyleTransformer (ACL 2019)
- https://github.com/PrithivirajDamodaran/Styleformer — Styleformer (2021–2023)
- https://github.com/luofuli/DualRL — DualRL (IJCAI 2019)
- https://github.com/XiaoyuanYi/StyIns — StyIns (IJCAI 2020)
- https://github.com/zacharyhorvitz/tinystyler — TinyStyler (EMNLP 2024 Findings)
- https://github.com/stylellm/stylellm_models — StyleLLM (Chinese classical-novel fine-tunes)
- https://github.com/ngpepin/stylometric-transfer — Stylometric-Transfer (interpretable fingerprints)
- https://github.com/psal/jstylo — JStylo (Drexel PSAL, authorship attribution)
- https://github.com/psal/anonymouth — Anonymouth (Drexel PSAL, style anonymization)
- https://github.com/cauchy221/StyleTunedLM — StyleTunedLM (LoRA for style, with eval)
- https://github.com/Muneeb1030/FineTune-Tiny-Llama — Personal-voice LoRA pipeline
- https://github.com/DidierRLopes/fine-tune-llm — Apple Silicon LoRA pipeline
- https://github.com/shandley/claude-style-guide — Anti-LLM-ism styleguide generator
- https://github.com/lout33/writing-style-skill — Claude Code / OpenCode skill for personal voice
- https://github.com/stephenhsklarew/WritingStylePromptGenerator — Style-prompt generator
- https://github.com/viktorbezdek/definitive-llm-writing-style-guide — Style framework / meta-prompt
- https://github.com/zhijing-jin/Text_Style_Transfer_Survey — Survey reading list (2022)
- https://github.com/yd1996/awesome-text-style-transfer — Awesome list
- https://direct.mit.edu/coli/article/48/1/155/108845/Deep-Learning-for-Text-Style-Transfer-A-Survey — MIT CL survey for lineage context
