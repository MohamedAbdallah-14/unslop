# Category 16 — GitHub Tools and Libraries

## Scope

This category covers the GitHub tooling layer for AI-text humanization: peer-reviewed attack repos, open-source skill packs, commercial humanizer APIs, and the practitioner debate about what any of it is actually doing. It spans the research tier (arXiv papers with reproducible benchmarks) and the practitioner tier (Claude Code skills, Next.js tutorial stacks, Reddit how-to threads) without conflating them. Out of scope: detector research per se, watermarking protocol design except where scrubbing humanizers touch it, and non-text modalities.

## Executive Summary

- The OSS humanizer landscape splits sharply into a **research tier** and a **practitioner tier** that barely reference each other. Research repos (DIPPER, HUMPA, StealthRL, GradEscape) produce reproducible benchmarks; practitioner skill packs produce README marketing claims. No popular Claude skill runs against TH-Bench. (A, C, E)
- **Five mechanism families** now dominate the research tier: paragraph paraphrase (DIPPER and descendants), word-level grammar-preserving perturbation (RAFT), detector-in-the-loop RL (AuthorMist, StealthRL, HUMPA), decoding-time guidance (SICO, CoPA), and **style-transfer fine-tuning** (MASH arXiv 2601.08564, BART/Mistral corpus arXiv 2604.11687). Small models beat large ones — GradEscape at 139M parameters outperforms DIPPER at 11B; MASH's 0.1B model extends the trend into 2026. (A)
- **`blader/humanizer`** (~14.7k stars, MIT, Claude Code skill) dominates the practitioner tier. It has spawned a cottage industry that grew in 2025–2026: `humanizer-x`, `slop-humanizer`, `Aboudjem/humanizer-skill` *(now 37 patterns)*, `brandonwise/humanizer`, `talk-normal`, `anti-slop-writing`, `jpeggdev/humanize-writing` *(8-pass)*, `lguz/humanize-writing-skill` *(multi-LLM)*, `aaaronmiller/humanize-writing`. None ship reproducible multi-detector eval harnesses. (C, E)
- **The commercial layer** has converged on `POST /v1/humanize` with bearer auth, intensity ladders (light/medium/aggressive) or tone ladders (HighSchool→PhD), and per-1K-word pricing. The spread is two orders of magnitude: Apify's deterministic rules engine at $0.003/text vs StealthGPT Business at $2.00/1K. **Two major new entrants: Walter Writes (surged 517% YoY in early 2026) and AuraWrite AI.** No commercial player publicly credits a named OSS library under the hood. (D)
- **Turnitin's August 2025 anti-humanizer update is the biggest single market event since DIPPER.** Turnitin now trains explicitly on humanizer outputs, adding a "AI-generated text that was AI-paraphrased" detection category. Walter Writes went from near-universal bypass to 38% flagged overnight. Any bypass numbers benchmarked before August 2025 against Turnitin are now stale. (D, B)
- **The `antislop-sampler`** (`sam-paech/antislop-sampler`) has been formalized: the ANTISLOP paper (arXiv 2510.15061) was accepted at **ICLR 2026**. `auto-antislop` automates the fine-tuning pipeline; `antislop-vllm` adds OpenAI-compatible API; `gemma-3-27b-it-antislop` on HF is a trained checkpoint. The approach still requires raw logits so stays inside LocalLLaMA and self-hosted setups. But it is no longer a practitioner hack — it is a citable, peer-reviewed technique. (A, E)
- **The engineering-critique position** — articulated by Peggy Kang's dev.to piece and `@voidborne-d` in `blader/humanizer` issue #82 — holds that prompt-only humanization is statistically self-defeating because the attacker and the source are the same distribution. Two credible escape hatches: rule-based syntactic restructuring (`voidborne-d/humanize-chinese`, `rithulkamesh/humanize`, Apify's deterministic pipeline) and the inference-time sampler. Both remain niche relative to skill-pack volume. (B, E)
- **Defenders have now explicitly counter-attacked.** DAMAGE (arXiv 2501.03437, ACL 2025 GenAIDetect) trains classifiers on humanizer-modified text. Turnitin's August 2025 update operationalizes this. The arms race has entered a second cycle. (A, D)
- **Watermarking is an unaddressed threat.** `eth-sri/watermark-stealing` (ICML 2024) can reverse-engineer watermark rules for under $50. None of the Tier A/B skill repos reference SynthID, OpenAI watermarks, or Stanford undetectable watermarks. If watermarking ships in production, every current skill-pack humanizer becomes irrelevant overnight. (A, C)
- **Two chronic naming collisions** pollute the category: `Humanizr/Humanizer` (9.5k stars, .NET string formatting) and `jehna/humanify` (3k+ stars, JavaScript deobfuscation) are routinely mislinked on Reddit and in listicles. (B, C, E)

## Cross-Angle Themes

**Pattern-stripping as an informal standard.** Approximately 29–30-item ban-lists derived from Wikipedia's *Signs of AI Writing* appear across A (BART/Mistral corpus markers), B (clawhub 16-pattern skill), C (`blader/humanizer` 29, `humanizer-x` 30, `Aboudjem/humanizer-skill` 30, `brandonwise/humanizer` 29, trailofbits plugin 24), and E (`mbodkebiz/slop-humanizer` described as "synthesized from 8 humanizer repos"). The converging taxonomy covers significance inflation, AI vocabulary ("delve", "tapestry", "testament"), copula avoidance, rule-of-three constructions, and hedging clichés.

**Perplexity + burstiness as universal marketing vocabulary.** Nearly every Tier B/C repo invokes these two GPTZero-era statistics as the thing being manipulated. The actual implementation is usually synonym swap plus sentence-length shuffling. The research tier (A) treats them as incidental rather than load-bearing. This gap — between the vocabulary and the mechanism — is a recurring source of inflated claims.

**The four-pass practitioner pipeline.** (1) Strip AI patterns via ban-list. (2) Inject voice or personality. (3) Manipulate statistical fingerprint. (4) Verify and score. Explicit in `humanizer-x`, `slop-humanizer`, StealthHumanizer's "ninja mode", and commercial `/v1/humanize` intensity ladders. The research tier achieves the same effect in a single RL policy (StealthRL, HUMPA), but the practitioner multi-pass shape is the UX standard.

**The "sounds human to readers" vs "defeats calibrated detector" split.** The `blader/humanizer` issue #82 thread captures this cleanly: `@voidborne-d` argues prompt-only humanization cannot defeat a calibrated detector; `@greg-randall` replies that the goal is often "sounds human to readers," not "defeats Turnitin." Both are correct about different goals. The OSS ecosystem rarely states which goal a repo is actually solving.

**Pricing spread implies compute is not the moat.** Apify's deterministic pipeline at $0.003/text vs StealthGPT Business at $2.00/1K vs OSS BYO-key at ~$0.07/1K (unmask-ai) means the commercial SaaS layer is defensible only through UX, detection tuning, and API maturity. (D, B)

**Ethical pushback concentrates on HN and is absent from OSS READMEs.** HN submissions for humanizer products routinely receive hostile normative responses ("machines pretending to be human speaking to machines") and rarely survive the front page. Reddit and dev.to treat the same tools as operational how-tos. SaaS products now add "don't use this to deceive evaluators"; OSS repos mostly skip it. (E, B)

**Watermarking is the looming existential threat that almost no practitioner addresses.** Both `eth-sri/watermark-stealing` and `codeboy5/revisiting-watermark-robustness` show watermarks can be reverse-engineered or scrubbed. None of the skill-pack repos reference this. The research tier discusses it; the practitioner tier does not. (A, C)

## Top Sources

### Must-read papers

- **DIPPER** — Krishna et al., NeurIPS 2023 (arXiv 2303.13408). `martiansideofthemoon/ai-detection-paraphrases`. Reduces DetectGPT accuracy from 70.3% to 4.6% AUROC. The de-facto baseline every subsequent paper benchmarks against.
- **HUMPA** — Wang et al., ICLR 2025 (arXiv 2410.19230). RL-fine-tuned proxy in front of frontier LLMs; –70.4% average AUROC, –95.0% maximum. Best-in-class for the "small humanizer head" pattern.
- **StealthRL** — arXiv 2602.08934 (2026). `suraj-ranganath/StealthRL`. GRPO on Qwen3-4B with LoRA; 97.6% ASR; mean AUROC 0.79 → 0.43; transfers to held-out detectors.
- **AuthorMist** — arXiv 2503.08716 (2025). Pioneered the commercial-detector-API-as-reward pattern. 78.6–96.2% ASR; semantic similarity ≥ 0.94.
- **GradEscape** — Meng et al., USENIX Security 2025 (arXiv 2506.08188). First gradient-based evader; 139M parameters outperform 11B DIPPER; tested in the wild against Sapling and Scribbr.
- **Adversarial Paraphrasing** — NeurIPS 2025 (arXiv 2506.07001). `chengez/Adversarial-Paraphrasing`. Training-free; TPR@1%FPR drops 64.5% on RADAR, 98.96% on Fast-DetectGPT, 87.9% average across detector families.
- **TH-Bench** — arXiv 2503.08708 (2025). `DrenfongWong/TH-Bench`. First benchmark explicitly for humanization attacks: 6 attacks × 13 detectors × 6 datasets × 19 domains × 11 LLMs. Headline finding: no single attack wins effectiveness, quality, and cost simultaneously.
- **Watermark Stealing** — Jovanović et al., ICML 2024. `eth-sri/watermark-stealing`. Reverse-engineers watermark rules via ~$50 of API queries; enables both spoofing and scrubbing.
- **MASH** — Gu, Li, Hu, arXiv 2601.08564 (January 2026). Style-injection SFT + DPO pipeline. 0.1B model outperforms larger baselines. The most current addition to the "small-model wins" research line.
- **ANTISLOP** — Paech et al., arXiv 2510.15061, **ICLR 2026**. `sam-paech/antislop-sampler`. Formalizes inference-time token-level backtracking. The only peer-reviewed technique for prevention-at-generation rather than post-hoc paraphrase.
- **BART/Mistral AI-to-Human Style Transfer** — arXiv 2604.11687 (April 2026). BART-large achieves BERTScore F1 0.924 with 17× fewer params than Mistral-7B. 25,140-pair training corpus released.
- **DAMAGE** — arXiv 2501.03437, ACL 2025 GenAIDetect workshop. Trains classifiers specifically on humanizer-modified text. Turnitin's August 2025 anti-humanizer feature is the commercial implementation of this approach.

### Key essays and posts

- **Peggy Kang, "Building an AI Humanizer: why we stopped trying to fix prompts"** (dev.to). The rigorous engineering argument: "Prompts don't fix distributions. Rewriting does." Two-stage pipeline (generation for correctness, post-processing for distribution). Became Dechecker's AI Humanizer.
- **dannwaneri, "Why I Built My Own Humanizer (And Why You Should Too)"** (dev.to). Critiques `blader/humanizer` as calibrated against a "generic human baseline" rather than the user's own voice; introduces corpus-grounded voice calibration via `CORPUS.md`.
- **retrorom, "Teaching AI to Write Like a Human: Inside the Humanizer Skill"** (dev.to). Two-pass approach (remove AI patterns, then inject voice, rhythm, opinions, ambivalence); before/after tables.
- **thehumanizeai.pro, "Why AI Humanizers Don't Work"**. 14 tools tested; 12 "did almost nothing"; QuillBot moved GPTZero only from 97% to 91%. Only structural rewriters move detector scores.
- **`blader/humanizer` issue #82 — "Prompt-based humanization won't solve detection"**. `@voidborne-d`'s synthesis of three viable approaches (fine-tuned models, rule-based syntactic restructuring, hybrid). The most lucid engineering analysis in the OSS practitioner space.

### Key OSS projects

- **`blader/humanizer`** (~14.7k stars, MIT) — dominant Claude Code skill; Wikipedia *Signs of AI Writing* foundation + 29-pattern ban-list + voice calibration + audit pass. Active as of April 2026.
- **`martiansideofthemoon/ai-detection-paraphrases` / `google-research/dipper`** — reference DIPPER implementation; NeurIPS 2023.
- **`PrithivirajDamodaran/Parrot_Paraphraser`** (~916 stars) — the T5 paraphrase framework that most DIY humanizers wrap under the hood.
- **`ColinLu50/Evade-GPT-Detector`** (SICO, TMLR 2024) — in-context optimization; cheapest humanization recipe in the research tier; no fine-tuning required.
- **`suraj-ranganath/StealthRL`**, **`zhouying20/HMGC`**, **`JamesLWang/RAFT`**, **`chengez/Adversarial-Paraphrasing`**, **`ffhibnese/CoPA_Contrastive_Paraphrase_Attacks`** — the active research attack repos.
- **`jfisher52/StyleRemix`** (arXiv 2408.15666) — interpretable per-axis LoRA modules (formality, length, function-word use, grade level, sarcasm, voice); releases AuthorMix and DiSC datasets.
- **`DrenfongWong/TH-Bench`**, **`xinleihe/MGTBench`**, **`Y-L-LIU/MGTBench-2.0`** — the evaluation scaffolding the field now runs on.
- **`sam-paech/antislop-sampler`** (~340+ stars) — inference-time backtracking; ~8,000 banned phrases; shipped into koboldcpp 1.76+ and open-webui. **ICLR 2026 peer-reviewed paper (arXiv 2510.15061).** Ecosystem expanded: `auto-antislop`, `antislop-vllm`, `gemma-3-27b-it-antislop` HF checkpoint.
- **`eth-sri/watermark-stealing`** (ICML 2024) — watermark scrubbing primitive; strategically important if watermarks ship in production.
- **`voidborne-d/humanize-chinese`**, **`rithulkamesh/humanize`** — rule-based non-LLM transforms; the only approach that produces genuinely non-LLM statistics.
- **`psal/anonymouth`** (~1.9k stars, abandoned 2021) — classic stylometric obfuscation; historical reference; not usable against modern LLM detectors.

### Notable commercial tools

- **Undetectable.ai** ($9.99–$49.99/mo; models v2, v11, v11sr; multiple readability modes; 86% average detection reduction claim; performs relatively well post-Turnitin August 2025 update) — market incumbent; OSS READMEs routinely name it as the target to match.
- **WriteHuman** (~$18/mo, request-based model; `POST /v1/humanize`; 40+ languages) — clearest example of the managed humanizer API productization pattern.
- **StealthGPT** (~$14.99–$19.99/mo consumer; $0.20–$2.00/1K words API; `/api/stealthify`; HS→PhD tone ladder; 0–100 detection score; multilingual API support).
- **Walter Writes** ($8–$12.99/mo; free 300–500 words/day; specialist in structural sentence restructuring; 517% YoY search growth Q1 2026; **post-Turnitin August 2025 update: 38% flagged**) — the fastest-rising and fastest-partial-falling commercial tool of 2025–2026.
- **AuraWrite AI** (new 2025–2026 entrant; claims <5% detection post-Turnitin update; #1 in multiple affiliate roundups post-update) — the clearest beneficiary of Turnitin's Walter Writes disruption.
- **AI Humanizer API** (free/$29/$99/custom; SOC 2 Type II; VPC; 99.99% SLA; SSE streaming; batch processing) — cleanest enterprise pricing grid observed.
- **Humaniser** ($19/mo; zero retention; JS + Python SDKs) — only mainstream vendor leading with privacy as the differentiator.
- **Deceptioner** — multi-detector profiles (Turnitin, GPTZero, Winston AI, Originality.ai) as a first-class API parameter; unusually transparent design.
- **Apify AI Text Humanizer** ($0.003/text; <500 ms; deterministic 12-pass; no LLM dependency) — price-floor outlier; closest thing to an OSS rules engine packaged as a managed service.

### Notable community threads

- **r/LocalLLaMA `antislop-sampler` announcement** and [llama.cpp SLOP Removal discussion #9699](https://github.com/ggml-org/llama.cpp/discussions/9699) — the inference-time wing.
- **`blader/humanizer` issue #82** — engineering critique locus; linked issues #55 and #78 for broader context.
- **r/BypassAiDetect "What AI humanizer is actually working in 2026"** — structural rewriters win (Walter Writes, Aurawrite); pure paraphrasers lose; OSS repos not mentioned.
- **HN 46694489** (`blader/humanizer` launch; 3 points; sole comment: "I think we also need a /dehumanizer skill").
- **HN 46106966** ("Ask HN: in-browser humanizer?"; sole reply: "Machines pretending to be human speaking to machines that pretend to ignore the fact they've guessed they're speaking to a machine?").
- **HN 47357745 "Slop or not"** — crowdsourced 16k-pair human-detection benchmark; Reddit posts easier to detect than HN content.

## Key Techniques & Patterns

1. **Paragraph paraphrase with diversity knobs** (DIPPER) — two scalars (lexical diversity, content reordering) find the minimum edit to flip a detector. Reference attack in every subsequent paper.
2. **Word-level grammar-preserving perturbation** (RAFT) — greedy token substitution via auxiliary embedding; black-box; keeps text error-free and human-indistinguishable in human eval.
3. **Detector-in-the-loop RL with API-as-reward** (AuthorMist, StealthRL, HUMPA) — GRPO/PPO against a joint detector loss; commercial detector APIs serve as opaque reward functions since AuthorMist (early 2025). Sidesteps gradient access entirely.
4. **Decoding-time guidance** (SICO, CoPA, HUMPA proxy) — in-context optimization or contrastive decoding that produces human-looking text at generation time without any post-hoc paraphrase step.
5. **Gradient-based evasion** (GradEscape) — weighted embeddings over the discrete token space; handles tokenizer mismatches via model extraction; 139M parameters outperform 11B DIPPER.
6. **Interpretable per-axis LoRA composition** (StyleRemix) — separate LoRA modules per style dimension (formality, length, function-word use, grade level, sarcasm, voice) composed at inference. The cleanest planning-friendly style-control primitive in the literature.
7. **Pattern stripping + voice injection + statistical manipulation + verification** (the practitioner 4-pass pipeline) — explicit in `humanizer-x`, `slop-humanizer`, StealthHumanizer ninja mode, and commercial `/v1/humanize` intensity ladders. Each pass is a separate LLM call.
8. **Skill/prompt packaging cascade** — `SKILL.md` → `AGENTS.md` → `.cursor/rules/*.mdc` → `.github/copilot-instructions.md` → `GEMINI.md`. Same prompt content, per-host envelope. Documented explicitly in `adenaufal/anti-slop-writing` and `blader/humanizer`.
9. **Voice calibration from writing samples** — paste 2–3 paragraphs, extract a style profile, rewrite against it. First-class in `blader/humanizer`; corpus-grounded version in `dannwaneri/voice-humanizer` via `CORPUS.md`.
10. **Inference-time backtracking sampler** (`antislop-sampler`) — retries token generation when output matches any of ~8,000 banned phrases; requires raw model logits; the only approach that modifies the generation distribution at the source rather than paraphrasing after the fact.
11. **Rule-based non-LLM syntactic transforms** (`voidborne-d/humanize-chinese`, `rithulkamesh/humanize`, Apify) — the only category that produces statistics genuinely outside the LLM-sampled distribution; per-language scaling cost is the tradeoff.
12. **Watermark scrubbing via query-based rule recovery** (`eth-sri/watermark-stealing`) — reverse-engineer the green-list, then paraphrase specifically around watermarked tokens. Over 80% average success rate for under $50.
13. **Post-generation CI regressions** (`brandonwise/humanizer`) — grep-style lint passes (`grep -iE "Certainly!|delve|It's important to note"`) as part of a 153-test suite. Cheapest form of ongoing quality gate.
14. **Commercial API shape conventions** — `POST /v1/humanize` with bearer auth; intensity ladder (light/medium/aggressive) or tone ladder (HighSchool→PhD/Journalist); 0–100 detection score in response; 1–7 s latency as the working band.

## Controversies & Debates

**Can prompt-only humanization defeat calibrated detectors?** The `blader/humanizer` issue #82 thread is the canonical debate. `@voidborne-d` argues no: "You are asking the same probability distribution to produce output that escapes detection algorithms trained on that exact distribution." `@greg-randall` replies that the goal is often reader-facing ("sounds human") rather than detector-facing, and for that goal pattern-stripping works. Both positions are correct about different objectives; the ecosystem rarely declares which goal a given repo is solving.

**Fine-tuned vs rule-based vs hybrid.** The #82 synthesis identifies three credible approaches: (1) fine-tuned humanizer models are effective but expensive and fragile to detector retraining, (2) rule-based syntactic restructuring produces genuinely different statistics but scales poorly across languages, (3) hybrid is the likely practical winner. No OSS project currently ships a credible fine-tuned humanizer checkpoint.

**Are published bypass-rate numbers trustworthy?** Almost every OSS README makes self-reported claims ("60–90% reduction," "99.8% bypass," "<10% AI detection") against unspecified detector versions. Only the research tier ships reproducible numbers (DIPPER, StealthRL, HUMPA, GradEscape, TH-Bench). Commercial reviewers are heavily self-interested; the thehumanizeai.pro piece found 12 of 14 tools "did almost nothing." Treat any number not from an independent academic test as marketing.

**Is detector convergence real?** StealthRL and Adversarial Paraphrasing report that attacks transfer to unseen detectors, implying detectors share a human-text manifold and humanization is tractable as a general problem. Defenders dispute this for calibrated production detectors. TH-Bench's finding that no attack wins all three axes simultaneously is the most honest current answer.

**"Sounds human to readers" vs "defeats Turnitin"** are treated as the same problem by most repos and most users. They are different problems with different metrics. The field has not cleanly separated them.

**Is humanization ethical?** HN consistently treats it as problematic. Reddit and dev.to treat it as a how-to. SaaS products now add disclaimers; OSS READMEs mostly do not. GitHub and LinkedIn content policy is tightening. The ethics framing is absent from technical discussions in OSS repos almost without exception.

**Statistical fingerprint vocabulary vs implementation.** Repos market "perplexity and burstiness manipulation" while the underlying code is synonym swap plus sentence-length shuffling. Modern detectors (Binoculars, Raidar, MAGE) do not rely primarily on perplexity/burstiness; this vocabulary is GPTZero-era framing that has persisted past its technical relevance.

## Emerging Trends

**Small models winning on signal quality.** GradEscape (139M) and AuthorMist (3B) outperform DIPPER (11B). MASH (0.1B) extends this into 2026. The frontier has moved from scale to what signal is in the training loop.

**API-as-reward is now standard.** Since AuthorMist (early 2025), treating commercial detector APIs as opaque reward functions has become the default approach in new RL-based humanizers. It sidesteps gradient access entirely and aligns training with the exact surface users face in production.

**Attack transferability is empirically established.** StealthRL and Adversarial Paraphrasing both report transfer to held-out detectors. The implicit claim — detectors learn the same human-text manifold — is the strongest argument that humanization is a general, tractable problem rather than a per-detector arms race.

**Skill-file format has crossed the chasm.** `blader/humanizer`'s ~14.7k stars marks the shift from "paste this system prompt" to installable artifacts (Claude `.skill`, OpenCode skill, Cursor `.mdc`, `AGENTS.md`). The packaging cascade is now documented in multiple repos. New multi-pass entrants (`jpeggdev/humanize-writing` 8-pass, `lguz/humanize-writing-skill` multi-LLM) show the format maturing.

**Two-layer architecture is winning over prompt-only.** Generation (clarity/correctness) separated from post-processing (distribution/flow) is explicit in Peggy Kang's piece and implicit in every 4-pass repo. Single-pass prompt humanization is being quietly conceded as the weakest variant.

**Commercial OSS shells wrapping paid APIs.** `humanizerai/agent-skills` publishes a thin OSS facade around a $19.99–$49.99/mo server-side API. Expect more of this; OSS as distribution channel rather than source of technique.

**Privacy-first positioning as a niche.** Only Humaniser (commercial) leads with zero-retention as the primary differentiator. OSS tools have this as a default. A named-OSS-library-backed commercial product with an honest zero-retention promise could credibly undercut Undetectable.ai on trust rather than price.

**Rule-based and hybrid approaches gaining credibility.** `voidborne-d/humanize-chinese`, `rithulkamesh/humanize`, and Apify's deterministic 12-pass pipeline are small but are treated as intellectually serious in the engineering-critique community. Expect more language-specific rule-based forks as the limitations of prompt-only approaches become clearer.

**Defender counter-attack is now explicit.** Turnitin's August 2025 anti-humanizer update and DAMAGE (arXiv 2501.03437) represent a new phase: defenders training on humanizer outputs specifically. The arms race is now iterative at the commercial-detector level, not just the research level. This invalidates all pre-August 2025 Turnitin bypass numbers.

**Inference-time slop prevention formalized academically.** ANTISLOP (ICLR 2026, arXiv 2510.15061) converts the LocalLLaMA `antislop-sampler` practitioner tool into a peer-reviewed technique. `auto-antislop` automates fine-tuning pipeline construction. The inference-time wing of humanization now has academic legitimacy.

**Style-transfer fine-tuning as a distinct research family.** MASH (SFT+DPO) and the BART/Mistral corpus (arXiv 2604.11687) establish style-transfer fine-tuning as the fifth research mechanism family alongside paraphrase, perturbation, RL, and decoding-time guidance. BART-large at BERTScore F1 0.924 is now the baseline for this sub-family.

**Commercial rankings are Turnitin-update-sensitive.** Walter Writes' 517% YoY search surge followed by 38% post-update flagging rate demonstrates that no commercial humanizer's bypass rate is durable without continuous detector-aware retraining. AuraWrite's ascent to #1 in post-update rankings is the inverse signal: tools that kept up with Turnitin's new signal are the new incumbents.

## Open Questions & Research Gaps

1. **No production-grade OSS humanizer exists.** Commercial tools (Undetectable.ai, WriteHuman) are closed; research repos are demos. A well-engineered OSS humanizer combining StealthRL's training recipe, StyleRemix's per-axis controls, and TH-Bench-scored eval is an empty niche.
2. **No OSS humanizer ships a reproducible multi-detector eval harness.** DIPPER has one in the paper; no practitioner skill measures itself against GPTZero + Originality + Turnitin + Pangram + Binoculars + Raidar on a public corpus. This is the single clearest differentiation opportunity.
3. **No "humanness" benchmark exists.** TH-Bench measures evasion only. A benchmark whose ground truth is human preference rankings — not detector scores — would be a cleaner training signal and is currently absent.
4. **Stylometry preservation and AI-stylometry removal are never combined.** `psal/anonymouth` and `EricX003/ALISON` address authorial stylometry; humanizer repos address AI-vs-human stylometry. No repo ships "preserve my voice while destroying the model's voice." This is the most obvious untouched niche in the catalog.
5. **Voice calibration is advertised but barely implemented.** Most "voice modes" reduce to 3–5 prompt presets. No repo ingests a user's writing corpus and fits a persistent per-user profile (vector or JSON style card) reused across rewrites.
6. **Watermark-aware humanization is absent from the practitioner tier.** `eth-sri/watermark-stealing` and `codeboy5/revisiting-watermark-robustness` exist in the research tier. None of the skill-pack repos reference SynthID, OpenAI watermarks, or Stanford undetectable watermarks.
7. **No first-class diff-with-rationale output.** Users get rewritten text with no auditable explanation of what changed and why. Academic users who need defensibility would pay for this; no OSS repo ships it.
8. **Multilingual evaluation is absent.** `ksanyok/TextHumanize` claims 25 languages; `RAW.AI` claims 50+. Public AI-text detectors are English-biased, so non-English "bypass" numbers are largely meaningless for reasons unrelated to humanization quality.
9. **Defense-aware humanization.** Turnitin's August 2025 update and DAMAGE (arXiv 2501.03437) confirm adaptive defenses are here. Attacks trained before August 2025 need re-evaluation. Almost nothing in the practitioner tier targets post-DAMAGE detector families specifically.
10. **Domain-conditioned humanizers.** Student essays, SEO posts, LinkedIn content, academic writing, and fiction all have different "human" signatures. Every OSS repo is domain-general; domain presets are nearly absent.
11. **Fine-tuned OSS humanizer checkpoint.** No public HF model card, no training dataset, no LoRA recipe for a humanizer fine-tune that competes with closed SaaS. Rephrasy and Walter Writes claim fine-tuned models; neither is open.

## How This Category Fits

This category is the implementation substrate for humanization research overall. Categories on detection (e.g., Binoculars, MAGE, Raidar) produce the adversaries that humanizer repos measure against; the transferability findings from StealthRL and Adversarial Paraphrasing directly constrain what detection can achieve long-term. The watermarking category intersects here through `eth-sri/watermark-stealing` and `codeboy5/revisiting-watermark-robustness`. The RL fine-tuning category is the source for StealthRL, HUMPA, and AuthorMist's training recipes. The stylometry / authorship-obfuscation space (ALISON, StyleRemix, JamDec, TinyStyler) is adjacent and currently uncombined with the AI-humanization repos — the gap that constitutes the clearest open niche. The evaluation methodology category should adopt TH-Bench and MGTBench-2.0 as standard scaffolding; those repos make cross-paper comparisons possible for the first time.

## Recommended Reading Order

1. **`blader/humanizer` issue #82** — read this first; it frames the central debate (prompt-only vs structural rewriting vs fine-tuned) in plain language, in ~15 minutes.
2. **Peggy Kang, "Building an AI Humanizer: why we stopped trying to fix prompts"** (dev.to) — the engineering argument for two-layer architecture.
3. **A-academic.md** — grounds the mechanism space; without it, every skill-pack README reads as magic.
4. **TH-Bench paper (arXiv 2503.08708)** — read the abstract and the "Headline finding" section; the no-single-winner result is the honest state of the art.
5. **DIPPER paper abstract (arXiv 2303.13408)** — understand the baseline every subsequent paper benchmarks against.
6. **C-opensource.md** — the concrete 35-repo catalog; what exists, what actually works, what is abandoned.
7. **E-practical.md** — how the community talks about this in Reddit, HN, and GitHub issues; the intellectual center of the practitioner tier.
8. **D-commercial.md** — pricing, API conventions, and the gap between OSS and managed-service offerings.
9. **StealthRL paper (arXiv 2602.08934)** — the current research-tier state of the art for detector-in-the-loop RL; read after the mechanism overview from A.
10. **B-industry.md** — listicle and tutorial coverage; mostly signal about what the market misses rather than what it delivers; read last.
