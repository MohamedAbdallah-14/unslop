# Category 04 — Natural Language Quality

## Scope

This category asks why LLM output sounds like machine text and what can be done about it. It covers the full stack: how tokens are sampled at inference time, why likelihood training produces flat and repetitive prose, how "AI voice" was systematically introduced by RLHF, what metrics actually measure human-likeness, how detectors exploit the statistical fingerprints humanizers leave behind, and how the OSS and commercial ecosystems have responded. The five angles — academic papers (A), industry engineering blogs (B), open-source repos (C), commercial products (D), and practitioner forums (E) — collectively map a field that matured rapidly between 2020 and 2026.

## Executive Summary

- **Decoding is the single largest lever on naturalness.** Holtzman et al. (ICLR 2020, arXiv:1904.09751) showed that the same trained model produces degenerate or human-like prose depending only on the sampler. Every subsequent angle — A, B, C, E — independently confirmed this, and the practical community (E) converged on a three-sampler recipe (min-p + DRY + temperature-last) as the 2025-2026 production default. (A, B, C, E)
- **"Human-like" has an information-theoretic definition.** Meister et al.'s locally typical sampling (TACL 2023, arXiv:2202.00666) argues that humans pick tokens whose information content sits near the model's conditional entropy, not at the mode. This is the cleanest theoretical account of why flat, high-probability LLM text reads as robotic, and the basis for every adaptive sampler that followed. (A)
- **RLHF is the mechanistic cause of "AI voice."** Preference optimization over short-horizon human feedback produces the hedge-bullet-emoji-warm register users now detect immediately. OpenAI's GPT-4o sycophancy rollback (2025) and Anthropic's Claude's Character essay (2024) are the clearest public admissions; `avoid_sycophancy` is now a named principle in OpenAI's Model Spec. (B)
- **Slop is structural, not just lexical.** Banning "delve" or "tapestry" is a surface fix. AI text is also detectable via tidy five-paragraph arcs, flat burstiness, log-prob curvature (DetectGPT, Mitchell et al., ICML 2023), and multi-model probability features (Ghostbuster, Verma et al., NAACL 2024). AI Fire (2025) documented ~400% to ~3,900% post-ChatGPT increases in specific phrases in academic writing. (A, B, D)
- **The OSS community is 12-24 months ahead of commercial APIs.** Min-p, DRY, XTC, top-nσ, dynamic temperature, and antislop backtracking are all available in llama.cpp, ExLlamaV2, Aphrodite, and text-generation-webui. OpenAI, Anthropic, and Google still expose only temperature + top-p + top-k + frequency/presence penalties; HN commenters and the min-p paper author attribute this to alignment risk, watermarking fragility, and inertia. (C, E)
- **Humanization is now a named adversarial research subfield — with peer-reviewed landmarks.** Cheng et al.'s Adversarial Paraphrasing (2025, arXiv:2506.07001) achieves an average 87.88% true-positive-rate reduction across detectors via detector-guided paraphrase. Sam Paech's Antislop framework (arXiv:2510.15061, **ICLR 2026 accepted**, poster #10008156) achieves ~90% slop suppression across 8,000+ patterns via backtracking + FTPO fine-tuning, with maintained or improved GSM8K/MMLU/creative writing scores. A companion `auto-antislop` pipeline and published fine-tuned models (gemma-3-27b-it-antislop, gemma-3-12b-it-antislop) make this the first production-ready academic humanization stack. These are the current floor any humanizer must clear. (A, C)
- **Commercial humanization splits into three archetypes.** Voice-capture tools (Sudowrite, Jasper, Lex, Notion, Grammarly, Anyword) ingest sample writing and generate style-profile prompts. Vertical fine-tunes (Sudowrite Muse for fiction, BrandWell for long-form SEO, AI21 Jamba for long context) claim the base model is actually tuned. Post-hoc bypass tools (Undetectable.ai, HIX Bypass, QuillBot, StealthGPT) paraphrase after generation and report detection-reduction rates of 69-99.8% against known detectors. Almost nobody exposes decoding knobs directly; Sudowrite's "Creativity Dial" (1-10) is the rare exception. (D)
- **Evaluation is fragmented and mostly not reproducible — and now has a quantified bias problem.** MAUVE measures distributional gap, BERTScore measures semantic preservation, HLB measures psycholinguistic processing signatures, EQ-Bench Creative Writing uses Claude-judge + Glicko-2 Elo (upgraded to Claude Sonnet 4.6 in 2025), lmscan fingerprints burstiness and slop-word density, and commercial detectors measure evasion rates. No single score for "humanness" exists, and vendor claims ("40% fewer revision passes," "82% accuracy vs. 52% for GPT-4o") are not independently reproducible. The 2025 CALM framework and Gao et al. (Computational Linguistics, 2025) now establish a reproducible bias budget for LLM-judge: ~40% position inconsistency, ~15% verbosity inflation, 5-7% self-enhancement. Any humanness claim using LLM-judge without bias disclosure is contestable. HLB additionally found that standard-benchmark capability wins can reduce humanlikeness. (A, C, D)

## Cross-Angle Themes

**Adaptive truncation beats fixed truncation (A, B, C, E).** The progression from top-k to top-p to locally typical sampling to η-sampling to min-p to top-nσ to XTC is a consistent move toward samplers that read the local shape of the probability distribution rather than applying a fixed cut. The min-p paper (ICLR 2025 Oral, arXiv:2407.01082) scales the truncation threshold by the top token's probability; top-nσ (Tang et al., arXiv:2411.07641) uses standard-deviation distance from the top logit. Both are now in mainline llama.cpp. The Thoughtworks writeup (B) and the community rentry guides (E) are the practitioner entry points to the same insight.

**Repetition is a three-layer problem (A, C, E).** Welleck et al. (ICLR 2020, arXiv:1908.04319) showed repetition is a training objective pathology, not just a decoding artifact. Su et al.'s SimCTG (NeurIPS 2022, arXiv:2202.06417) traced it to anisotropic token embeddings. At the decoding layer, the community replaced blunt `repetition_penalty > 1.1` — which distorts grammar — with DRY (p-e-w, 2024), which penalizes n-gram continuations exponentially and was verified over 200k+ tokens without the looping failures classical penalty produced.

**Warmth and sycophancy are on the same RLHF gradient (B, D).** Anthropic's Claude's Character (2024) and OpenAI's GPT-4o sycophancy postmortem (2025) independently published that maximizing short-horizon engagement overshoots into dishonesty. Grammarly's own disclosure that GrammarlyGO outputs "can be detected by AI detectors" shows that even tools sold on naturalness acknowledge the limit. Humanization products that index on warmth reproduce the exact failure mode frontier labs had to roll back.

**Sampler order is load-bearing (C, E).** Every OSS guide and the llama.cpp reference implementation agree: temperature goes last. The canonical pipeline is `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`. Placing temperature earlier reshapes the distribution before truncation samplers see it, defeating their purpose. Ollama disables min-p by default (sets it to 0.0) and ships `repeat_penalty=1.1` by default; llama.cpp does the opposite. Switching backends without re-tuning silently degrades output.

**Structural and lexical slop need separate tools (B, C, E).** DRY and frequency penalty handle lexical and n-gram repetition. XTC (Exclude Top Choices, p-e-w, 2024) inverts standard truncation by probabilistically dropping the most probable tokens, targeting structural clichés. Antislop backtracking (Paech 2025) targets named phrases that appear more than 1,000x more often in LLM output than in human corpora. The r/LocalLLaMA field report (E) adds that prompt-state randomization (rotating mood/goal/desire across turns) handles persona-level slop that token-distribution samplers cannot reach.

**Perplexity is no longer a neutral signal — and is narrowing as a gap (A, C).** DetectGPT (Mitchell et al., ICML 2023, arXiv:2301.11305) exploits log-prob curvature; Ghostbuster (Verma et al., NAACL 2024) combines features from multiple frozen LMs and beats DetectGPT by ~6 F1; GPTZero and lmscan use burstiness as a primary signal. Humanizers that optimize only one statistic are detectable via the orthogonal ones. The commercial bypass tools (D) report detector-specific evasion rates that do not generalize across the multi-model feature space Ghostbuster uses. However, top 2025-2026 models now achieve perplexity as low as 5-10, materially narrowing the AI-vs-human perplexity gap that older detectors rely on. Burstiness is increasingly the last reliable signal, but its durability is under-studied.

## Top Sources

### Must-read papers

- Holtzman et al., *The Curious Case of Neural Text Degeneration*, ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). Foundational: human text is not the most likely text under an LM; introduces nucleus sampling.
- Meister et al., *Locally Typical Sampling*, TACL 2023 / EMNLP 2022. [arXiv:2202.00666](https://arxiv.org/abs/2202.00666). Cleanest information-theoretic account of "human-like" token choice.
- Nguyen et al., *Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs*, ICLR 2025 Oral. [arXiv:2407.01082](https://arxiv.org/abs/2407.01082). Confidence-adaptive truncation; now default in HF Transformers, vLLM, llama.cpp.
- Welleck et al., *Neural Text Generation with Unlikelihood Training*, ICLR 2020. [arXiv:1908.04319](https://arxiv.org/abs/1908.04319). Repetition as objective-level bug; beats nucleus sampling in human evals.
- Su et al., *A Contrastive Framework for Neural Text Generation (SimCTG)*, NeurIPS 2022 Spotlight. [arXiv:2202.06417](https://arxiv.org/abs/2202.06417). Anisotropy story + contrastive search decoder.
- Li et al., *Contrastive Decoding*, ACL 2023. [arXiv:2210.15097](https://arxiv.org/abs/2210.15097). Expert minus amateur log-prob subtraction; training-free, beats nucleus on three domains.
- Basu et al., *Mirostat*, ICLR 2021. [arXiv:2007.14966](https://arxiv.org/abs/2007.14966). Direct perplexity-target feedback loop; ties cross-entropy to repetition rate formally.
- Pillutla et al., *MAUVE*, NeurIPS 2021 Outstanding Paper. Distributional gap metric capturing both Type-I (degenerate) and Type-II (too-narrow) failures; gold-standard offline eval.
- Zhang et al., *BERTScore*, ICLR 2020. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675). Paraphrase-robust semantic-preservation floor; BERTScore ≥ ~0.85 is a common humanizer guardrail.
- Mitchell et al., *DetectGPT*, ICML 2023 Oral. [arXiv:2301.11305](https://arxiv.org/abs/2301.11305). Log-prob curvature as zero-shot detection; AUROC up to 0.95.
- Verma et al., *Ghostbuster*, NAACL 2024. Multi-model probability features beat single-LM perplexity by ~6 F1; sets a 99 F1 ceiling.
- Duan et al., *HLB: Benchmarking LLMs' Humanlikeness in Language Use*, 2024. [arXiv:2409.15890](https://arxiv.org/abs/2409.15890). Psycholinguistic probes across 20 LLMs and 2,000+ human participants; benchmark wins can reduce humanlikeness.
- Cheng et al., *Adversarial Paraphrasing*, 2025. [arXiv:2506.07001](https://arxiv.org/abs/2506.07001). Detector-guided paraphrase; average 87.88% T@1%F reduction across detectors.
- Paech et al., *Antislop + FTPO*, **ICLR 2026**. [arXiv:2510.15061](https://arxiv.org/abs/2510.15061). Backtracking sampler + fine-tune; 90% slop suppression across 8,000+ patterns, maintained GSM8K/MMLU/creative writing scores. Includes auto-antislop pipeline and published fine-tuned models.
- Various, *A Survey on LLM-as-a-Judge*, 2025. [arXiv:2411.15594](https://arxiv.org/abs/2411.15594). Definitive bias taxonomy; position (~40% inconsistency), verbosity (~15% inflation), self-enhancement (5-7%) are quantified benchmarks any humanization eval must account for.
- Various, *Justice or Prejudice? (CALM)*, ICLR 2025. [arXiv:2410.02736](https://arxiv.org/abs/2410.02736). 12-bias taxonomy with mitigation strategies; multilingual judge reliability is especially poor (Fleiss' Kappa ≈ 0.3).
- Gao et al., *LLM-based NLG Evaluation: Current Status and Challenges*, Computational Linguistics 51(2), 2025. Peer-reviewed survey confirming LLM-judge dominance; human–LLM collaborative evaluation achieves strongest results.

### Key essays and posts

- Patrick von Platen, *How to generate text* (Hugging Face, 2020). Canonical decoding tutorial; still the most-linked entry point.
- Maxime Labonne, *Decoding Strategies in LLMs* (Hugging Face, 2024). Modern visual re-explanation with code; practical replacement for von Platen.
- Anthropic, *Claude's Character* (2024). Character training as alignment objective; reframes humanization as trait-level shaping, not surface prompting.
- OpenAI, *Sycophancy in GPT-4o* (2025) + *Model Spec 2025-10-27*. Industry postmortem of warmth-as-failure-mode; `avoid_sycophancy` as published principle.
- Simon Willison, *Slop* (2024). Named the target state negatively; gave the community its vocabulary.
- Alan West, *How to Fix That Robotic AI Tone in Your LLM-Powered Features* (dev.to, 2025). Negative-constraint system-prompt playbook; the cheapest baseline any humanizer must beat.
- AI Fire, *Slop Evader* (2025). Documents structural (not lexical) slop patterns and ~400-3,900% vocabulary shifts post-ChatGPT.
- AlpinDale, *Dummy's Guide to Modern LLM Sampling* (rentry.org). The OSS community's canonical sampler reference; covers all modern samplers with pseudocode.
- kalomaze, *LLM Samplers Explained* (GitHub gist). Design intent from the min-p and dynamic-temperature author.
- smcleod, *LLM Sampling Parameters Guide* (Nov 2025). Cross-framework defaults and the Ollama vs. llama.cpp silent-difference warning.
- rpwithai, *Understanding Sampler Settings For AI Roleplay* (2025). The production three-sampler recipe with per-parameter tuning rules.

### Key OSS projects

- `ggml-org/llama.cpp` — reference implementation of the modern sampler stack; PRs #3841 (min-p), #9702 (DRY), #9742 (XTC), #11223 (top-nσ) are the primary-source design arguments.
- `sam-paech/antislop-sampler` + `antislop-vllm` + `auto-antislop` — **ICLR 2026 accepted**; backtracking sampler + FTPO fine-tune + automated profiling pipeline. Published fine-tuned models: `gemma-3-27b-it-antislop`, `gemma-3-12b-it-antislop`.
- `aphrodite-engine/aphrodite-engine` — vLLM fork that ships DRY, XTC, top-nσ, mirostat; the practical answer to "vLLM but with creative samplers."
- `krishnap25/mauve` — reference MAUVE implementation; 16k+ downloads/month on PyPI.
- `EQ-bench/creative-writing-bench` — 32-prompt × 3-iteration creative writing benchmark with Claude Sonnet 4.6 judge + Glicko-2 Elo; now includes Slop and Repetition columns. Longform leaderboard added 2025. Current leader: Grok-4.1 Thinking (score 1721.900).
- `lmscan` (pip-installable) — 12-feature statistical fingerprinter (burstiness, entropy, Zipf deviation, slop-word density); usable as an inner-loop reward signal, no API key, <50ms.
- `oobabooga/text-generation-webui` — de-facto sampler UI with custom sampler-order (PR #5443) and community presets (Divine Intellect, Midnight Enigma, Yara).
- `turboderp-org/exllamav2` — GPU sampler-rich backend popular for creative deployments.
- `blader/humanizer`, `lguz/humanize-writing-skill`, `brandonwise/humanizer` — prompt-layer humanization reference implementations with 29-pattern banned-word corpora.

### Notable commercial tools

- **Sudowrite (Muse)** — fiction-only fine-tune + "Style Examples" (upload ~1,000 words) + user-exposed "Creativity Dial" (1-10). Rare example of decoding surfaced as a first-class UX control. Claims 40% fewer revision passes for voice consistency.
- **Jasper (Brand Voice / Jasper IQ)** — enterprise voice-capture; Memory + Tone & Style + voice-violation flagging.
- **Lex.page** — "Style Guides" (upload samples, auto-generate detailed style instructions) + user-selectable base model.
- **Grammarly (GrammarlyGO)** — notably self-disclosed that generated content "can be detected by AI detectors" without human editing.
- **Grok 4.1 (xAI)** — 30+ persona modes including a "Style Mimic" affordance; markets humanness explicitly as character and emotional intelligence, not prose surface.
- **Content at Scale / BrandWell** — runs its own AI detector and its own humanizer; proprietary multi-LLM stack; "undetectable, humanlike content" for long-form SEO.
- **Undetectable.ai, HIX Bypass, QuillBot, StealthGPT** — post-hoc paraphrase bypass tools; third-party 2026 detection-reduction rates 69-99.8% against the best-known detectors. EU AI Act Article 50 (August 2026) creates direct compliance exposure for these products in the EU market.

### Notable community threads

- HN #43887637 (Apr 2025) — min-p author `menhguin` confirms "top-nσ is currently the best general-purpose sampler" and that temperatures of 100 are safe with proper truncation floors; attributes commercial API lag to alignment/watermarking/inertia.
- HN #41286604 (Aug 2024) — XTC launch thread; creator reports "creativity off the charts, coherence virtually unchanged."
- r/LocalLLaMA "What actually works for roleplay" (2025) — sampler changes need prompt-state randomization to kill persona-level slop.
- r/accelerate "AI slop is a skill problem, not a model problem" (2025) — counter-narrative worth holding alongside the mechanistic threads.
- exllamav2 issue #447 (p-e-w) — original DRY proposal; explains why classical repetition penalty is a "blunt instrument that distorts grammar."
- vLLM PR #11368 (DRY, closed) + issue #8581 — community calls DRY "completely mandatory" for creative writing; enterprise engines declined.

## Key Techniques & Patterns

1. **Nucleus / top-p sampling** (Holtzman 2020, A) — First method to restore human-like probability distribution; still the production default in commercial APIs.
2. **Locally typical sampling** (Meister 2022, A) — Truncates to tokens near conditional entropy; the theoretical reference for all adaptive samplers.
3. **Min-p sampling** (Nguyen 2024, A/B/C/E) — Threshold scales with top-token probability; enables high-temperature creative generation without incoherence; ICLR 2025 Oral, deployed in HF Transformers, vLLM, llama.cpp.
4. **Top-nσ sampling** (Tang 2024, C/E) — Standard-deviation truncation from top logit; stable under T ≥ 2 where min-p begins to degrade; min-p author publicly endorses it as superior for general use.
5. **Contrastive search** (Su 2022/23, A/B) — Penalizes embedding similarity between candidate tokens and prior context; addresses repetition at the representation level without retraining.
6. **Contrastive decoding (expert − amateur)** (Li 2023, A) — Log-prob difference between a large and small model cancels small-model failure modes; training-free.
7. **Mirostat** (Basu 2021, A/C) — Feedback loop maintains a target perplexity level throughout generation; directly maps "human-range surprise" to a controllable parameter.
8. **DRY (Don't Repeat Yourself)** (p-e-w 2024, C/E) — Exponential penalty `multiplier * base^(n - allowed_length)` on tokens that continue a previously-seen n-gram; replaces `repetition_penalty` without distorting grammar. Defaults: multiplier=0.8, base=1.75, allowed_length=4 for natural prose.
9. **XTC (Exclude Top Choices)** (p-e-w 2024, C/E) — Probabilistically drops the most-probable tokens before sampling; targets structural clichés that repetition penalties cannot see. Typical values: threshold=0.1, probability=0.5, applied after truncation samplers.
10. **Dynamic temperature** (kalomaze, C/E) — Per-token temperature scaled by distribution entropy (HHI); reduces temperature when the model is confident, raises it when uncertain.
11. **Unlikelihood training** (Welleck 2020, A) — Training objective that pushes down probability on repeats; frames repetition as an objective-level bug rather than a decoding problem.
12. **Negative-constraint system prompts** (West 2025, B/D) — Slop-word banlist plus structural rules injected at the system-prompt layer; cheapest humanization baseline, zero model changes required.
13. **Antislop backtracking** (Paech, ICLR 2026, C/E) — At inference time, detects disallowed phrases, rewinds to the problem token, and resamples with that branch masked. Suppresses 8,000+ patterns; the only peer-reviewed OSS sampler that directly targets named humanization defects rather than distribution shape.
14. **FTPO (Final-Token Preference Optimization)** (Paech, ICLR 2026, C) — Fine-tuning in logit-space that permanently bakes slop suppression into model weights. Achieves 90% suppression while maintaining GSM8K/MMLU scores. Auto-antislop pipeline automates the full training data generation.
15. **Detector-guided adversarial paraphrase** (Cheng 2025, A) — Uses an off-the-shelf detector as a reward signal during paraphrase; current academic state-of-the-art for evasion.
16. **MAUVE** (Pillutla 2021, A/C) — KL divergence in quantized embedding space; captures both Type-I (degenerate) and Type-II (too-narrow) failures; gold-standard offline humanness eval.
17. **BERTScore** (Zhang 2020, A) — Contextual embedding cosine similarity; paraphrase-robust semantic-preservation floor. BERTScore ≥ ~0.85 is a common guardrail.
18. **HLB psycholinguistic probes** (Duan 2024, A) — 10 classical psycholinguistic experiments across 20 LLMs and 2,000+ human participants; shows capability improvements and humanlikeness can be negatively correlated.
19. **lmscan fingerprinting** (community, C) — 12 statistical features (burstiness, Zipf deviation, slop-word density) in <50ms; usable as an inner-loop reward signal without a neural model.
20. **Prompt-state randomization** (r/LocalLLaMA, E) — Rotating mood/goal/desire fields in the system prompt across turns; addresses persona-level slop that token-distribution samplers cannot reach.

## Controversies & Debates

**Humanization vs. alignment.** Adversarial paraphrase tools (Cheng 2025) and commercial bypass products already exist as a priced category. Frontier labs are publishing anti-sycophancy principles and character-training specifics that humanizers work around. The ethical framing is contested: Unslop's use case (making assistant output less robotic for the user who asked for it) is categorically different from ghost-authoring academic work, but the underlying technique — making LLM output harder to attribute — is the same. Academic submissions will increasingly require an ethics section on this.

**Decoding vs. training as the real lever.** Welleck (2020) argues repetition is an objective-level bug only fixed by training. The practical consensus across B, C, and E is that decoding alone gets you ~80% of the way; the rest requires preference data or fine-tuning (FTPO). Su and Collier (2023) walked back the anisotropy story from SimCTG: most LMs are naturally isotropic, so contrastive search works without the contrastive training objective.

**Warmth as anti-goal.** OpenAI's GPT-4o postmortem and Anthropic's Claude's Character both treat maximally engaging prose as a failure mode. Humanization products that optimize for warmth and agreeableness are on the same RLHF gradient that OpenAI had to roll back within days.

**DRY and XTC in enterprise engines.** vLLM's PR #11368 (DRY) was closed despite users calling it "completely mandatory"; SGLang has not merged them either. llama.cpp, ExLlamaV2, Aphrodite, KoboldCPP, and text-generation-webui all shipped them. This is a deliberate market split, not an oversight.

**Temperature ceiling.** The conventional advice "keep T ≤ 1.2 for coherence" is being dismantled by min-p and top-nσ practitioners who report T = 2-100 is coherent with a proper truncation floor. The min-p paper author confirmed T = 100 on HN. Whether this extends safely to reasoning and math tasks is not yet settled.

**Slop: vibes, statistics, or skill.** Willison (2024) defines slop pragmatically as text that "took more effort to consume than to produce." AI Fire (2025) argues it's structural (paragraph architecture). Antislop (Paech 2025) shows specific phrases appear more than 1,000x more often in LLM than human corpora. The r/accelerate thread argues slop is a taste problem: users who can't detect it can't be saved by better samplers. All four framings map to different product interventions.

**Benchmark wins vs. humanlikeness.** HLB (Duan et al., 2024) found that improvements on standard NLP benchmarks can reduce humanlikeness and in some cases were negatively correlated. This means capability-chasing is not aligned with the humanization goal, and any eval harness built on standard benchmarks will give misleading signals.

## Emerging Trends

1. **Sampler proliferation has stabilized.** Every major OSS engine ships roughly the same 8-12 samplers. Differentiation has shifted to sampler-order UX, creative-sampler mainline support, and constrained decoding. Top-nσ is now merged in llama.cpp but disabled by default (requires explicit activation). (C)
2. **Tone as a product surface — now on both sides.** GPT-5.1 ships Friendly / Efficient / Professional / Candid / Quirky / Nerdy / Cynical; Grok has 30+ persona modes; Anthropic shipped Custom Styles presets (Normal/Concise/Explanatory/Formal) to Claude.ai in 2025. Humanization tools now compete with built-in tone controls on flagship products. External humanizers must deliver value beyond what a one-click style preset offers. (B, D)
3. **Distributional and psycholinguistic evaluation replacing reference-based eval.** MAUVE and HLB compare populations of text, not single references. BLEU and ROUGE are increasingly ceremonial (confirmed by Ehud Reiter's 2025 practitioner review). LLM-judge is now the default, but requires bias mitigation. (A, B)
4. **LLM-judge bias is quantified and public.** The CALM framework (ICLR 2025) and Gao et al. (Computational Linguistics, 2025) establish a reproducible bias budget: ~40% position inconsistency, ~15% verbosity inflation, 5-7% self-enhancement. Evaluations that ignore these biases are contestable. EQ-Bench's upgrade to Claude Sonnet 4.6 as judge (2025) sharpens evaluations but does not eliminate self-preference bias. (A, C)
5. **Character training moving upstream.** Anthropic's Constitutional AI character variant bakes persona into post-training rather than patching it via system prompt. Anthropic Custom Styles (2025) brings this to the product surface. This raises the ceiling for what downstream prompt-layer humanizers can change. (B)
6. **Anti-sycophancy as a published principle.** OpenAI's `avoid_sycophancy` in the Model Spec and Anthropic's explicit rejection of pandering signal a shift: excessive agreeableness is now an anti-goal in frontier model specs. (B)
7. **Training-free wins keep landing.** Contrastive decoding, contrastive search, min-p, top-nσ, XTC, antislop backtracking, and adversarial paraphrasing are all inference-time methods requiring zero retraining. Strong signal that decoding and paraphrase stacks can reach state-of-the-art without custom model training. (A, C)
8. **Antislop matures to production-ready.** ICLR 2026 acceptance, auto-antislop pipeline, and published fine-tuned models (gemma-3-27b-it-antislop, gemma-3-12b-it-antislop) move antislop from a promising sampler hack to a replicable, peer-reviewed, production-ready framework. The backtracking + FTPO combination covers inference-time and training-time suppression simultaneously. (A, C)
9. **Regulatory watermarking arrives.** EU AI Act Article 50 (effective August 2026) mandates AI text marking; the December 2025 draft Code of Practice specifies multilayered approaches and prohibits watermark removal. Detection-bypass products face compliance exposure in the EU. The watermark vs. humanization trade-off is now a legal question, not just a technical one. (B, D)
10. **Reasoning-model voice is an open frontier.** Raschka (2025) documents that o1/R1-class models optimize for correctness and tend to produce more formulaic prose; the reasoning traces themselves are a new humanization surface with no established playbook. (B)

## Open Questions & Research Gaps

- **No unified "humanness score."** MAUVE, BERTScore, HLB, burstiness, detector-evasion rate, and lmscan fingerprints each measure something different. The EQ-Bench Slop column (added 2025) is a step forward, but still covers only the lexical/n-gram surface. No composite metric validated against human judgment, detector evasion, and psycholinguistic signatures simultaneously exists. This is the clearest defensible benchmark opportunity in the field. (A, C, D)
- **Decoding-strategy behavior on post-RLHF / GPT-4/5-class models.** Nearly all decoding papers validate on base or lightly tuned LMs (GPT-2, OPT, early LLaMA). How nucleus vs. typical vs. min-p vs. contrastive search behave on instruction-tuned frontier models is under-studied. (A)
- **Sampler composition has no published ablation.** "DRY + XTC + high-T + dynatemp" is community folklore (E). No repository has grid-searched sampler combinations against MAUVE or EQ-Bench. (C, E)
- **Burstiness as a sampling-time target.** lmscan quantifies burstiness post-hoc; detectors exploit it; but no sampler explicitly biases generation toward a target sentence-length variance distribution. This is a clear gap for a humanization-native sampler. (A, C)
- **Joint decoding + prompting optimization.** Posts cover samplers or prompt-level anti-slop separately. The interaction — e.g., negative-constraint prompt + min-p 0.05 + T=1.2 — is under-documented. (B, E)
- **Style-preserving humanization.** Adversarial paraphrasing optimizes for evasion; joint objectives that humanize while matching an author's voice are absent from both academic and OSS work. (A)
- **Watermark vs. humanization trade-off is now a compliance deadline.** Kirchenbauer-style watermarks and adversarial paraphrase are natural adversaries; the Pareto frontier between watermark robustness and humanization strength has not been systematically mapped. The EU AI Act Article 50 enforcement date (August 2026) makes this urgent: any humanizer targeting EU users must either operate below the watermark detection threshold or face regulatory exposure. (A, B, D)
- **Long-form coherence past ~2,000 tokens.** GPT-5's creative-writing page gestures at it; no Anthropic or OpenAI engineering post explains the scaffolding that produces human-sounding long prose. (B)
- **Voice-capture at gradient level.** All commercial voice-capture tools ingest samples and produce a text-based style profile in the system prompt. No vendor does per-user fine-tuning at scale. Small-LoRA-per-user is economically plausible but unshipped. (D)
- **Multilingual humanization.** Most decoding work is English-centric. Su and Collier (2023) evaluated contrastive search across 16 languages; everything else is largely English. (A)
- **Reasoning-trace humanization.** o1/R1-class models expose reasoning traces as a new surface. No established academic or industry playbook exists for humanizing them. (B)

## How This Category Fits

Natural Language Quality is the technical substrate of the entire Unslop project. Every other research category touches a knob surfaced here: a sampler, a loss term, a prompt constraint, a paraphrase operator, or a metric. Three specific interfaces matter. First, this category is the upstream of any detection and evasion work — every signal that detectors exploit (perplexity, curvature, burstiness, multi-model features) maps directly to decoding, training, or post-hoc interventions catalogued here. Second, it is downstream of alignment and RLHF research: "AI voice" is not a style mistake but the visible output of preference optimization for short-horizon helpfulness, which means humanization is partly an alignment inversion — undoing trait-level shaping that frontier labs deliberately introduced. Third, because no unified humanness metric exists, Unslop must build its own eval harness combining MAUVE, BERTScore, HLB, burstiness, and detector-evasion signals — which overlaps with any evaluation-focused sibling category. Sibling categories this most directly intersects: AI-text detection and evasion, RLHF and alignment, style transfer and author voice, and evaluation infrastructure.

## Recommended Reading Order

**Fast-track (approx. 2 hours):**

1. Patrick von Platen, *How to generate text* (Hugging Face, 2020) — orientation on why samplers matter
2. Maxime Labonne, *Decoding Strategies in LLMs* (Hugging Face, 2024) — modern refresher with code
3. Simon Willison, *Slop* (2024) + Alan West, *Fix That Robotic AI Tone* (dev.to, 2025) — names the target state and shows the cheapest baseline
4. Thoughtworks, *Min-p sampling for LLMs* (2025) — practitioner framing of the 2026 default decoding upgrade
5. AlpinDale, *Dummy's Guide to Modern LLM Sampling* (rentry.org) — maps the full OSS sampler zoo
6. rpwithai, *Sampler Settings For AI Roleplay* (2025) — production three-sampler recipe with concrete defaults
7. Anthropic, *Claude's Character* (2024) + OpenAI, *Sycophancy in GPT-4o* (2025) — why "AI voice" exists and why warmth is not the solution

**Deep dive (approx. 1 day):**

8. Holtzman et al. (2020) → Meister et al. (2022) → Nguyen et al. (2024) — the decoding-theory arc from nucleus sampling through locally typical to min-p
9. Welleck et al. (2020) + Su et al. (2022, 2023) + Li et al. (2023) — training-time and representation-level alternatives; the anisotropy correction
10. Pillutla et al. (2021) MAUVE + Zhang et al. (2020) BERTScore + Duan et al. (2024) HLB — the evaluation stack and why no single metric is sufficient
11. Mitchell et al. (2023) DetectGPT + Verma et al. (2024) Ghostbuster + Cheng et al. (2025) Adversarial Paraphrasing — detection signals and adversarial humanization ceiling
12. Paech et al. (ICLR 2026) Antislop paper + `sam-paech/antislop-sampler` + `auto-antislop` repo — peer-reviewed OSS humanization stack: backtracking sampler + FTPO fine-tune + automated profiling pipeline + published fine-tuned models
