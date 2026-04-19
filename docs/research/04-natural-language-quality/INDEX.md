# Category 04 — Natural Language Quality (Fluency, Burstiness, Decoding)

## Scope

How "human-feeling" text is produced, measured, and defeated at the decoding, training, and evaluation layers. Covers: sampling algorithms (top-p, typical, contrastive, min-p, η, Mirostat, DRY, XTC, top-nσ, dynamic temperature), training-time interventions (unlikelihood, RLHF, character training, FTPO), distributional evaluation (MAUVE, BERTScore, HLB, EQ-Bench Creative), AI-text detection signals (perplexity curvature, burstiness, multi-model features), adversarial humanization (antislop, detector-guided paraphrase), and the commercial / OSS ecosystem pitching "natural" or "undetectable" output. Synthesizes five angles: Academic (A), Industry blogs (B), Open-source repos (C), Commercial products (D), and Practitioner forums (E).

## Executive Summary

- **Decoding is the single largest lever on "human-feel" prose.** The same model produces degenerate slop or human-like writing depending solely on the sampler. Holtzman 2020 is the origin myth; every angle (A/B/C/E) independently converges on this claim.
- **The OSS community is 12–24 months ahead of commercial APIs** on advanced sampling. A converged "naturalness stack" — **min-p (or top-nσ) + DRY + temperature-last** — is shipped across llama.cpp, ExLlamaV2, text-generation-webui, Aphrodite, KoboldCPP, and SillyTavern. OpenAI / Anthropic / Google still expose only temperature + top-p + top-k + frequency/presence penalties, reportedly for alignment and watermarking reasons.
- **RLHF is the mechanistic cause of "AI voice."** Preference optimization over short-horizon human feedback produces the hedge-bullet-emoji-warm register users now detect by sight. OpenAI's GPT-4o sycophancy rollback (2025) and Anthropic's Claude's Character essay (2024) are the industry's public confessions; `avoid_sycophancy` is now in OpenAI's Model Spec.
- **"Human-like" has an information-theoretic signature.** Meister et al.'s locally typical sampling formalizes it: humans pick tokens whose information content sits near the model's conditional entropy, not at the mode. This is the cleanest theoretical account of why high-probability LLM text reads robotic — and the basis for most modern adaptive samplers.
- **Slop is structural, not just lexical.** Banning "delve / tapestry / testament" is insufficient; AI text is also detectable via tidy five-paragraph arcs, zoom-out conclusions, flat burstiness, and log-prob curvature (DetectGPT). Effective humanization must alter paragraph architecture and sentence-length variance, not just vocabulary.
- **Humanization is now a named adversarial subfield.** Cheng et al.'s *Adversarial Paraphrasing* (2025) achieves ~87.88% average true-positive-rate reduction across detectors; sam-paech's `antislop-sampler` achieves ~90% slop reduction with preserved benchmark performance via backtracking. These set the current floor any humanizer must clear.
- **Commercial humanization splits into three archetypes:** voice-capture / style-example plays (Sudowrite, Jasper, Lex, Notion, Anyword, Grammarly), vertical-fine-tuned models (Sudowrite Muse, BrandWell, Jamba), and post-hoc paraphrase bypass tools (Undetectable.ai, QuillBot, StealthGPT, HIX Bypass). Almost nobody exposes decoding knobs directly — Sudowrite's "Creativity Dial" is the rare exception.
- **Evaluation is fragmented and mostly vibes-based.** MAUVE (distributional), BERTScore (semantic), HLB (psycholinguistic), EQ-Bench Creative Writing (LLM-judge rubric + Elo), lmscan (burstiness/Zipf/slop-density), and per-detector evasion rates all measure different things; no single "humanness score" exists. HLB additionally shows that standard-benchmark wins can *reduce* humanlikeness.

## Cross-Angle Themes

- **Adaptive truncation beats fixed truncation.** Progression from top-k → top-p → typical → η → min-p → top-nσ → XTC is unmistakably toward samplers that react to the local shape of the distribution. Confirmed independently by A (Hewitt 2022, Nguyen 2024), B (Thoughtworks min-p, HF contrastive search), C (llama.cpp / ExLlamaV2 / Aphrodite defaults), and E (kalomaze, AlpinDale rentry, SillyTavern presets).
- **Repetition is a three-layer problem.** Training-time (unlikelihood, Welleck 2020), representation-level (anisotropy, SimCTG / contrastive search), and decoding-time (DRY, no-repeat-n-gram) all fight different pieces. Classical `repetition_penalty > 1.1` actively hurts naturalness; DRY (n-gram-continuation penalty) is the community-preferred replacement.
- **Perplexity is no longer a neutral signal.** DetectGPT, Ghostbuster, GPTZero, lmscan, and Content-at-Scale's own detector all weaponize perplexity and burstiness. Humanizers that optimize only a single statistic (e.g., lowering perplexity) are visibly detectable by the orthogonal one (burstiness). This is consistent across A and C; D's commercial humanizers report detection-reduction numbers of 69–99.8% but are not audited across multi-model-feature detectors (C's Ghostbuster finding).
- **"Warmth" and "sycophancy" are on the same RLHF gradient.** Anthropic (Claude's Character) and OpenAI (GPT-4o postmortem, Model Spec) independently published this. Naive humanization that indexes on warmth reproduces the exact failure mode frontier labs rolled back.
- **Sampler order is load-bearing.** Every OSS guide (C + E) puts **temperature last** so truncation samplers judge the model's native confidence, not a reshaped distribution. llama.cpp default order is canonical: `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`.
- **Structural vs. lexical slop need separate tools.** DRY + frequency penalty handle lexical/n-gram repetition; XTC and Antislop handle stylistic cliché ("a testament to", "it's not X, it's Y", tidy-essay shape). Writer-oriented stacks layer both.

## Top Sources (Curated)

### Must-read papers

- **Holtzman et al. — *The Curious Case of Neural Text Degeneration*** (ICLR 2020). [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). Foundational: human text is not the most likely text under an LM; introduces nucleus sampling.
- **Meister et al. — *Locally Typical Sampling*** (TACL 2023 / EMNLP 2022). [arXiv:2202.00666](https://arxiv.org/abs/2202.00666). Cleanest information-theoretic account of "human-like" token choice.
- **Nguyen et al. — *Turning Up the Heat: Min-p Sampling*** (ICLR 2025 Oral). [arXiv:2407.01082](https://arxiv.org/abs/2407.01082). Confidence-adaptive truncation; now default in HF / vLLM / llama.cpp.
- **Li et al. — *Contrastive Decoding*** (ACL 2023). [arXiv:2210.15097](https://arxiv.org/abs/2210.15097). Expert − amateur log-prob subtraction; training-free way to "subtract AI-ness."
- **Basu et al. — *Mirostat*** (ICLR 2021). [arXiv:2007.14966](https://arxiv.org/abs/2007.14966). Direct perplexity-target feedback loop; ties cross-entropy to repetition rate.
- **Pillutla et al. — *MAUVE*** (NeurIPS 2021, Outstanding Paper). Distributional gap metric; the gold-standard offline humanness eval.
- **Zhang et al. — *BERTScore*** (ICLR 2020). Paraphrase-robust semantic-preservation floor.
- **Mitchell et al. — *DetectGPT*** (ICML 2023 Oral). [arXiv:2301.11305](https://arxiv.org/abs/2301.11305). Log-prob curvature as detection signal — the bar humanizers must clear.
- **Verma et al. — *Ghostbuster*** (NAACL 2024). Multi-model probability features beat single-LM perplexity; raises the humanization bar.
- **Duan et al. — *HLB: Benchmarking LLMs' Humanlikeness in Language Use*** (2024). [arXiv:2409.15890](https://arxiv.org/abs/2409.15890). Psycholinguistic probes; benchmark wins can reduce humanlikeness.
- **Cheng et al. — *Adversarial Paraphrasing*** (2025). [arXiv:2506.07001](https://arxiv.org/abs/2506.07001). Detector-guided paraphrase; current academic ceiling for humanization.
- **Paech et al. — *Antislop* + FTPO** (2025). [arXiv:2510.15061](https://arxiv.org/abs/2510.15061). Backtracking sampler + fine-tuning; ~90% slop reduction with preserved benchmark performance.

### Must-read posts/essays

- **Patrick von Platen — "How to generate text"** (HF, 2020). [huggingface.co/blog/how-to-generate](https://huggingface.co/blog/how-to-generate). Canonical decoding tutorial.
- **Maxime Labonne — "Decoding Strategies in LLMs"** (HF, 2024). Modern visual re-explanation with code.
- **Thoughtworks (Nguyen et al.) — "Min-p sampling for LLMs"** (2025). Practitioner framing of ICLR oral.
- **Anthropic — "Claude's Character"** (2024). Character training as alignment objective.
- **OpenAI — "Sycophancy in GPT-4o"** (2025) + **Model Spec 2025-10-27**. Industry postmortem of warmth-as-failure-mode.
- **Lilian Weng — "Extrinsic Hallucinations in LLMs"** (2024). Separates "sounds human" from "is grounded."
- **Simon Willison — "Slop"** (2024) + **"Dummy's Guide to Modern LLM Sampling"** (2025). Names the target state negatively; surfaces the sampler zoo.
- **Alan West — "How to Fix That Robotic AI Tone"** (dev.to, 2025). Cheapest-baseline negative-constraint system-prompt playbook.
- **AI Fire — "Slop Evader"** (2025). Structural (not lexical) de-slopping; documents ~400–3,900% post-ChatGPT vocabulary shifts.
- **AlpinDale — "Dummy's Guide to Modern LLM Sampling"** (rentry, 2024–25). Most comprehensive OSS sampler reference.
- **kalomaze — "LLM Samplers Explained"** (gist, 2024+). Design intent from min-p / dynamic-temp author.
- **smcleod — "LLM Sampling Parameters Guide"** (Nov 2025). Cross-framework defaults and gotchas (Ollama vs. llama.cpp differ silently).
- **rpwithai — "Understanding Sampler Settings For AI Roleplay"** (2025). The production three-sampler recipe (min-p + DRY + temperature).

### Key open-source projects

- **`ggml-org/llama.cpp`** — reference implementation of the modern sampler stack (min-p, DRY, XTC, top-nσ, typical, mirostat, dynatemp).
- **`turboderp-org/exllamav2`** — GPU sampler-rich backend popular for creative deployments.
- **`vllm-project/vllm`** — production throughput engine; notable gap: DRY/XTC not merged mainline.
- **`aphrodite-engine/aphrodite-engine`** — vLLM fork that *does* ship DRY/XTC/top-nσ/no-repeat-ngram/mirostat.
- **`sgl-project/sglang`** — structured generation + standard samplers (lets humanizers combine JSON/regex constraints with stochastic decoding).
- **`oobabooga/text-generation-webui`** — de-facto sampler UI; custom sampler-order PR #5443.
- **`LostRuins/koboldcpp`** (+ `kalomaze/koboldcpp` fork) — creative-writing-first backend where min-p / DRY / XTC were first prototyped.
- **`huggingface/transformers`** — `GenerationConfig` + `LogitsProcessor` extension point (min-p upstreamed; antislop/top-nσ ship as community processors).
- **`sam-paech/antislop-sampler`** + **`antislop-vllm`** — backtracking slop-filter; the single OSS project most directly targeted at humanization.
- **`krishnap25/mauve`** — reference MAUVE implementation.
- **`EQ-bench/creative-writing-bench`** — 32-prompt × 3-iteration creative writing benchmark; public leaderboard at [eqbench.com/creative_writing.html](https://eqbench.com/creative_writing.html).
- **`lmscan`** — 12-feature statistical fingerprinter (burstiness, entropy, Zipf, slop-density); usable as inner-loop reward signal.
- **`BurhanUlTayyab/GPTZero`** — OSS reimplementation; useful adversarial target.
- **`blader/humanizer`**, **`lguz/humanize-writing-skill`**, **`brandonwise/humanizer`**, **`humania-org/humanize`** — prompt-layer humanization reference implementations with banned-word / pattern corpora.
- **`basusourya/mirostat`**, **`menhguin/minp_paper`**, **`Tomorrowdawn/top_nsigma`** — canonical algorithm implementations.

### Notable commercial tools

- **Sudowrite (Muse)** — fiction-only fine-tune + "Style Examples" + user-exposed "Creativity Dial" (1–10). Rare example of decoding surfaced as UX.
- **Jasper (Brand Voice / Jasper IQ)** — enterprise voice-capture (Memory + Tone & Style + voice-violation flagging).
- **Lex.page** — "Style Guides" (upload samples, auto-generate style instructions) + user-selectable base model.
- **Notion AI** — workspace-level custom instructions + context retrieval; competes on integration, not fine-tuning.
- **Grammarly (GrammarlyGO)** — context-aware prompt enhancement + tone dial; notable self-disclosure that outputs can be detected.
- **Anyword** — proprietary fine-tunes over customer performance-marketing data; "Performance Prediction" score (claimed 82% vs. 52% for GPT-4o).
- **Grok (xAI)** — 30+ persona modes ("Style Mimic"); markets humanness as *character*, not prose surface.
- **Content at Scale / BrandWell / RankWell** — proprietary multi-LLM stack for long-form SEO; runs its own detector (both sides of the loop).
- **Wordtune (AI21)** — "Spices" co-writer with source attribution; the rare "enhance, don't replace" pitch still alive in 2026.
- **AI21 Jamba** — Mamba-Transformer hybrid, 256K context; decoding-surface claims (multi-word tokens, fewer fragmentation artifacts).
- **The humanizer cluster: Undetectable.ai, HIX Bypass, QuillBot, StealthGPT** — post-hoc paraphrase bypass tools; third-party 2026 detection-reduction rates 69–99.8%.

### Notable community threads

- **HN #43887637 (Apr 2025)** — AlpinDale rentry discussion; min-p author `menhguin` confirms "top-nσ is currently the best general-purpose sampler" and "temps of 100 are fine with min-p or top-nσ"; attributes commercial API lag to alignment / watermarking / inertia.
- **HN #41286604 (Aug 2024)** — XTC launch thread. "Creativity off the charts, coherence virtually unchanged."
- **r/LocalLLaMA "What actually works for roleplay"** (2025) — field report that sampler changes need to be paired with prompt-state randomization (mood/goal/desire rotation) to kill persona-level slop.
- **r/accelerate "AI slop is a skill problem, not a model problem"** (2025) — counter-narrative worth holding alongside the mechanistic threads.
- **SillyTavern preset repos (Virt-io, sphiratrioth666)** — the actual shipped presets for the largest "humanizing LLM output" community; neutralize everything except Min-P + DRY + Temperature.
- **llama.cpp PR #3841 (Min-P)**, **#9702 (DRY)**, **#9742 (XTC)**, **#11223 (top-nσ)** — primary-source design arguments.
- **oobabooga PR #5677 (DRY)**, **#6335 (XTC)**, **#5443 (custom sampler order)** — canonical design notes.
- **exllamav2 issue #447 (p-e-w)** — original DRY proposal: classical repetition penalty is a "blunt instrument that distorts grammar."
- **vllm PR #11368 (DRY, closed)** + **issue #8581** — the production-engine gap: creative samplers called "completely mandatory" by users but not merged.

## Key Techniques & Patterns

| Layer | Technique | Source | Humanization use |
|---|---|---|---|
| Decoding | **Nucleus / top-p** | Holtzman 2020 (A) | Baseline that restored human-like distribution. |
| Decoding | **Locally typical** | Meister 2022 (A) | Targets conditional entropy; the theoretical reference. |
| Decoding | **Min-p** | Nguyen 2024 (A/B/C/E) | Confidence-adaptive truncation; default recommended in 2026. |
| Decoding | **Top-nσ** | Tang 2024 (C/E) | Std-dev truncation; stable under high temperature (T ≥ 2). |
| Decoding | **η / ε-sampling** | Hewitt 2022 (A) | Entropy-aware truncation; precursor to adaptive samplers. |
| Decoding | **Mirostat** | Basu 2021 (A/C) | Explicit perplexity-target feedback loop. |
| Decoding | **Contrastive search** | Su 2022/23 (A/B) | Penalizes embedding similarity to context; anti-repetition. |
| Decoding | **Contrastive decoding (expert − amateur)** | Li 2023 (A) | Training-free subtraction of small-model pathologies. |
| Decoding | **DRY (Don't Repeat Yourself)** | p-e-w 2024 (C/E) | Exponential penalty on repeated n-gram continuations; replaces crude `repetition_penalty`. |
| Decoding | **XTC (Exclude Top Choices)** | p-e-w 2024 (C/E) | Probabilistically drops the most-likely token; anti-cliché. |
| Decoding | **Dynamic temperature** | kalomaze (C/E) | Per-token temperature scaled by distribution entropy. |
| Decoding | **Smooth / quadratic sampling** | kalomaze (E) | Quadratic logit transform; soft alternative to truncation. |
| Training | **Unlikelihood training** | Welleck 2020 (A) | Repetition as objective-level bug. |
| Training | **RLHF** | Lambert et al. 2022 (B) | Root cause of "AI voice"; the target of humanization. |
| Training | **Character training / Constitutional AI** | Anthropic 2024 (B) | Trait-level persona shaping at post-training. |
| Training | **FTPO (Final-Token Preference Opt.)** | Paech 2025 (C) | Permanent slop removal via preference-like finetune. |
| Prompt | **Negative-constraint system prompts** | dev.to / AI Fire (B/D) | Cheapest baseline: slop-word banlist + structural rules. |
| Prompt | **Style examples / voice capture** | Sudowrite / Jasper / Lex / Notion (D) | User-sample-driven style profile in system prompt. |
| Prompt | **Prompt-state randomization** | r/LocalLLaMA (E) | Rotate mood/goal/desire across turns to kill caricature. |
| Post-hoc | **Adversarial paraphrase** | Cheng 2025 (A) | Detector-guided rewriting; ~87.88% avg T@1%F reduction. |
| Post-hoc | **Antislop backtracking** | Paech 2025 (C/E) | Rewind + resample on banned n-gram/phrase; ~90% reduction. |
| Post-hoc | **Multi-mode paraphrase bypass** | Undetectable.ai / HIX / QuillBot (D) | Commercial detection-evasion; 69–99.8% claimed. |
| Evaluation | **MAUVE** | Pillutla 2021 (A/C) | Distributional KL divergence; offline gold standard. |
| Evaluation | **BERTScore** | Zhang 2020 (A) | Paraphrase-robust semantic-preservation floor (≥0.85 common). |
| Evaluation | **HLB (psycholinguistic probes)** | Duan 2024 (A) | Distribution of *responses* across 10 human-language tasks. |
| Evaluation | **EQ-Bench Creative Writing** | Paech (C) | 32×3 prompt benchmark with Claude-judge + Glicko-2 Elo. |
| Evaluation | **Burstiness / lmscan / GPTZero features** | community (C) | Cheap surface fingerprinting; useful inner-loop reward. |
| Adversarial | **Log-prob curvature** | DetectGPT (A) | Humanized text must leave the LM's log-prob ridge. |
| Adversarial | **Multi-model probability features** | Ghostbuster (A) | Humanized text must confuse *proxy* LMs, not just source. |

## Controversies & Debates

- **Humanization vs. alignment.** Optimizing for naturalness overlaps with optimizing for evasion (Cheng 2025); academic work is beginning to carry explicit ethics sections. Commercial "bypass" products (D) are already a priced category; frontier labs are explicitly publishing anti-sycophancy principles (OpenAI Model Spec, Anthropic Claude's Character). Humazier arrives at a contested moment.
- **Decoding vs. training as the "real" lever.** Welleck (2020) argues repetition is an objective-level bug; Holtzman / Meister / Su / Li / Nguyen / Basu argue it's sufficiently fixable at decode. Su & Collier (2023) walked back the anisotropy story. The practical consensus across B/C/E is "decoding alone gets you ~80%"; the rest needs preference data.
- **Warmth as anti-goal.** The OpenAI GPT-4o postmortem (2025) and Anthropic's Claude's Character (2024) both published that maximally engaging/agreeable prose is a *failure* mode. Humanization products that over-index on warmth reproduce the exact issue the frontier labs rolled back.
- **DRY/XTC merge politics.** Enterprise-serving engines (vLLM, SGLang) hesitated or declined to merge DRY/XTC despite user demand; creative-writing engines (llama.cpp, ExLlamaV2, Aphrodite, KoboldCPP, text-generation-webui) shipped them. This is a real market split, not an oversight.
- **Temperature ceiling.** Conventional wisdom ("keep T ≤ 1.2 for coherence") is being dismantled by min-p and top-nσ advocates, who report T ≥ 2–100 is fine with a proper floor. Still unsettled whether reasoning / math tasks can tolerate this.
- **Is slop vibes or math?** Willison (2024) defines slop pragmatically ("took more effort to consume than to produce"); AI Fire (2025) argues it's structural (paragraph architecture); lmscan argues it's statistical (burstiness, slop-word density); Antislop (Paech 2025) shows specific phrases appear >1,000× more often in LLM than human corpora. The r/accelerate counter-thread argues it's a *taste* problem. All four framings show up in Humazier's target market.
- **Skill vs. tooling.** r/accelerate's "AI slop is a skill problem, not a model problem" (2025) challenges the entire humanizer premise: users who can't detect slop can't be saved by better samplers. A non-trivial objection for any humanization product.

## Emerging Trends

1. **Sampler proliferation has stabilized.** Every major OSS inference engine ships roughly the same 8–12 samplers. Differentiation is now in (a) sampler-order UX, (b) creativity-sampler mainline support, (c) constrained decoding. The novelty frontier is *composition*, not invention.
2. **Tone is becoming a product surface.** GPT-5.1 ships Friendly / Efficient / Professional / Candid / Quirky / Nerdy / Cynical as user-facing knobs; Anthropic Styles; Grok's 30+ persona library. Humanization tools now compete with built-in knobs.
3. **Distributional / psycholinguistic evaluation is replacing reference-based eval.** MAUVE and HLB (A) compare populations of text; BLEU/ROUGE are increasingly ceremonial. Expect more human-processing-signature probes in 2025–26.
4. **Character training is moving upstream.** Anthropic's Constitutional-AI character variant shows persona being baked in at post-training, not patched via system prompt. Raises the bar for what downstream humanizers can alter.
5. **Anti-sycophancy as published principle.** OpenAI's `avoid_sycophancy` and Anthropic's explicit rejection of pandering mark a shift: excessive agreeableness is now an anti-goal in frontier specs, not a neutral default.
6. **Humanization is now a named research subfield.** Adversarial Paraphrasing (A, 2025) + Antislop (C, 2025) publish at top venues with transfer studies, ethical framing, and evaluation suites.
7. **Reasoning-model voice is an open frontier.** Raschka 2025 (B): o1/R1-class models introduce a new artifact — reasoning traces — whose humanization properties are under-explored.
8. **Training-free wins keep landing.** Contrastive decoding, contrastive search, min-p, η-sampling, top-nσ, XTC, antislop, adversarial paraphrasing — all inference-time methods. Strong signal that decoding / paraphrase stacks reach SOTA without custom model training.
9. **Backtracking samplers** (Antislop) are a nascent architecture pattern. Only `antislop-sampler` currently does this in OSS; obvious expansion space (burstiness-target backtracking, phrase-repetition backtracking).

## Open Questions / Research Gaps

- **No unified "humanness score."** MAUVE (distribution), BERTScore (semantics), HLB (psycholinguistic), burstiness (surface), detector-evasion rate (adversarial), lmscan (fingerprint) — nothing combines them with validated weights against human judgment and detector evasion simultaneously. Sudowrite's "40% fewer revisions" and Anyword's 82% are non-reproducible vendor claims. This is a defensible benchmark opportunity.
- **Decoding-strategy wins on post-RLHF / GPT-4/5-class models.** Almost all decoding papers validate on base / lightly tuned LMs (GPT-2, OPT, early LLaMA). Nucleus vs. typical vs. min-p vs. contrastive-search behavior on instruction-tuned frontier models is under-studied.
- **Multilingual humanization.** Most work is English-centric. Su & Collier (2023) covered 16 languages for contrastive search; everything else is largely English. Open space.
- **Burstiness as a *training or sampling* objective.** Used defensively by detectors and passively by lmscan; no sampler explicitly biases generation toward target sentence-length variance. Clear gap for a humanization-native sampler.
- **Sampler composition has no published ablation.** "DRY + XTC + high-T + dynatemp" is community folklore (E). No repository grid-searches sampler combinations against MAUVE / EQ-Bench / detector evasion.
- **Joint decoding + prompting optimization.** Posts cover samplers (HF, Thoughtworks) or prompt-level anti-slop (dev.to, AI Fire) but rarely both. Interaction (e.g., "negative-constraint prompt + min-p 0.05 + T=1.2") is under-documented.
- **Long-form coherence past ~2,000 tokens.** Gestured at by GPT-5 creative-writing page; no Anthropic/OpenAI engineering essay explains the scaffolding that produces human-sounding long prose.
- **Style-preserving humanization.** Adversarial paraphrasing optimizes for evasion; joint objectives that humanize *while* matching author voice are absent.
- **Watermark ↔ humanization trade-off.** The Kirchenbauer-style watermark vs. adversarial paraphrase Pareto frontier hasn't been systematically mapped.
- **Voice-capture is shallow.** No commercial vendor does gradient-level per-user fine-tuning at scale — economics haven't landed. Small-LoRA-per-user is an open opportunity (D).
- **Character-level humanization.** Fiction tools (Sudowrite Story Bible) are the exception. Character consistency (beliefs, speech tics, affective stance) as a distinct humanization layer above style is under-tooled outside Grok.
- **Reasoning-trace humanization.** The new surface introduced by o1/R1; no established industry playbook.

## How This Category Fits in the Bigger Picture

Natural Language Quality is Humazier's **core technical substrate**. Every other category in the research (psycholinguistics, detection/evasion, style transfer, evaluation) ultimately touches a knob surfaced here: a sampler, a loss term, a prompt constraint, a paraphrase operator, or a metric. Three specific interfaces matter:

1. **Upstream of detection / evasion.** Detector research (DetectGPT, Ghostbuster, GPTZero) and humanization are a direct adversarial pair. Every signal detectors exploit (perplexity, curvature, burstiness, multi-model features, fingerprints) maps to a concrete decoding-, training-, or post-hoc intervention surfaced in this category.
2. **Downstream of alignment / RLHF.** "AI voice" is not a style mistake — it is the visible consequence of preference optimization for short-horizon helpfulness. Humanization is therefore partly an *alignment inversion*: undoing trait-level shaping that frontier labs deliberately introduced. This reframes Humazier as downstream of categories covering RLHF / Constitutional AI / Model Spec design.
3. **Adjacent to evaluation infrastructure.** Because no unified humanness metric exists, Humazier must build its own eval harness combining MAUVE / BERTScore / HLB / burstiness / detector evasion. This overlaps heavily with any evaluation-focused category.

For product design, the category implies three concrete commitments: (a) target open-weights / self-hosted runtimes to access the full sampler stack; (b) combine token-level (min-p / DRY), structural (XTC / antislop / negative-constraint prompts), and adversarial (detector-guided paraphrase) layers since each addresses orthogonal failure modes; (c) own an independent benchmark, since vendor self-reporting is saturated.

## Recommended Reading Order

**Fast-track (≈2 hrs):**
1. Patrick von Platen, *How to generate text* (HF, 2020) — orientation.
2. Maxime Labonne, *Decoding Strategies in LLMs* (HF, 2024) — modern refresher.
3. Simon Willison, *Slop* (2024) + dev.to *Fix That Robotic AI Tone* (2025) — target state + cheapest baseline.
4. Thoughtworks, *Min-p sampling* (2025) — the 2026 default decoding upgrade.
5. AlpinDale, *Dummy's Guide to Modern LLM Sampling* (rentry) — OSS sampler map.
6. rpwithai, *Sampler Settings For AI Roleplay* — production three-sampler recipe.
7. Anthropic, *Claude's Character* (2024) + OpenAI, *Sycophancy in GPT-4o* (2025) — why "AI voice" exists and why warmth is not the answer.

**Deep dive (≈1 day):**
8. Holtzman 2020 → Meister 2022 → Nguyen 2024 — the decoding-theory arc.
9. Welleck 2020 + Su 2022/23 + Li 2023 — training-time / representation-level and contrastive-decoding alternatives.
10. Pillutla 2021 (MAUVE) + Zhang 2020 (BERTScore) + Duan 2024 (HLB) — evaluation stack.
11. Mitchell 2023 (DetectGPT) + Verma 2024 (Ghostbuster) + Cheng 2025 (Adversarial Paraphrasing) — detection and adversarial humanization.
12. Paech 2025 (Antislop paper + repo) — current OSS state-of-the-art humanization sampler.

**Background / context (as needed):**
13. Lilian Weng, *Extrinsic Hallucinations* (2024).
14. HF *Illustrating RLHF* (2022).
15. Sebastian Raschka, *Understanding Reasoning LLMs* (2025).
16. OpenAI Model Spec 2025-10-27.
17. Jay Alammar, *Illustrated GPT-2* (2019).
18. Commercial-tool marketing (Sudowrite Muse, Jasper Brand Voice, Lex, Grok 4.1, BrandWell) — vendor positioning and quote bank.
19. HN threads #43887637 (AlpinDale guide) and #41286604 (XTC) — community narrative.

## File Index

| File | Angle | Focus | Notes |
|---|---|---|---|
| [`A-academic.md`](A-academic.md) | A — Academic & scholarly | arXiv / ACL / EMNLP / ICLR / NeurIPS / ICML / TACL / TMLR | 16 sources. Decoding theory, unlikelihood, MAUVE / BERTScore / HLB, DetectGPT / Ghostbuster, adversarial paraphrasing. |
| [`B-industry.md`](B-industry.md) | B — Industry engineering blogs | OpenAI, Anthropic, HF, Thoughtworks, independent researchers | 16 posts. Decoding tutorials, RLHF / character training / sycophancy, "slop" discourse, Model Spec. |
| [`C-opensource.md`](C-opensource.md) | C — Open-source & GitHub | llama.cpp, ExLlamaV2, vLLM, Aphrodite, SGLang, HF Transformers, text-generation-webui, KoboldCPP, antislop, MAUVE, EQ-Bench, lmscan, GPTZero | Sampler algorithms + eval stack + humanization-specific repos. |
| [`D-commercial.md`](D-commercial.md) | D — Commercial products & services | Sudowrite, Jasper, Copy.ai, Writesonic, Rytr, AI21, Lex, Notion, Grammarly, Grok, BrandWell, Wordtune, Anyword, Hypotenuse, Undetectable.ai / HIX / QuillBot / StealthGPT | 15 products. Archetypes, marketing rhetoric, "brand voice" vs. "personal voice," bypass / humanizer category. |
| [`E-practical.md`](E-practical.md) | E — Practitioner forums & how-tos | Reddit (r/LocalLLaMA, r/MachineLearning, r/accelerate), HN, rentries, gists, SillyTavern presets, PR / issue threads | Converged community sampler recipes, parameter presets A–F, field reports. |
| [`INDEX.md`](INDEX.md) | — | Synthesis of A–E | This file. |
