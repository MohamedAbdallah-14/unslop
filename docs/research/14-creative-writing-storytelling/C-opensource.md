# Creative Writing & Storytelling — Angle C: Open-Source

> **Project:** Humanizing AI output and thinking
> **Angle:** Survey of open-source frontends, community-trained writing models, long-form story-generation systems, datasets, and benchmarks that the open-source world has built for AI-assisted creative writing.
> **Research value: high** — a full stack exists (frontends + bespoke creative-writing models + long-form generation systems + datasets + purpose-built writing benchmarks + "AI slop" detectors), much of it built specifically to push LLM prose away from the bland, assistant-voice default that the humanization project is fighting.

## Scope

This angle indexes the open-source work most directly relevant to "making AI prose feel human." That means: (1) the fiction-first frontends that established the genre (KoboldAI, text-generation-webui's creative preset tradition, NovelAI-adjacent tooling); (2) the community-merged and community-trained writing LLMs that trade benchmark scores for voice (Mytho-series, Midnight-Miqu, Goliath, Sao10K's Euryale/Fimbulvetr); (3) long-form story-generation research systems (Dramatron, Re3, DOC, autonovel, StoryDaemon); (4) the canonical creative-writing datasets (r/WritingPrompts, GPT-WritingPrompts, CoAuthor); and (5) the new generation of writing-specific benchmarks and AI-slop detectors (EQ-Bench creative-writing-v3, longform-writing-bench, WritingBench, Judgemark-v2, slop-score).

The through-line: the open-source stack has already diagnosed the main failure modes of "assistant-voice fiction" — tropes, purple prose, shivers-down-her-spine clichés, length-bias, structural collapse past ~4k tokens — and has built targeted tools for each. A humanization system that ignores this stack is re-inventing ten years of community debugging.

---

## 1. KoboldAI (henk717/united fork)

- **URL:** https://github.com/henk717/KoboldAI
- **Author:** henk717 + KoboldAI community (active fork of the original KoboldAI-Client)
- **Stars:** ~430 (henk717 fork); ~3,880 on the upstream `KoboldAI/KoboldAI-Client`
- **Updated:** Actively maintained (2025–2026); the `united` branch is the de-facto upstream for creative-writing users
- **License:** AGPL-3.0
- **Description:** Browser-based front-end for AI-assisted fiction writing. The original "bring your own model" creative-writing UI, and the direct ancestor of every modern local roleplay stack.
- **Techniques / modes:**
  - **Novel mode** — continuous long-form prose, models biased toward narrative rather than chat
  - **Adventure mode** — AI-Dungeon-style interactive fiction with action parsing
  - **Story mode** — prompt-continuation writing
  - **Chat / Instruct modes** — conversational and instruction-following
  - **Memory + Author's Note + World Info** triad (the canonical "persistent context" triangle the rest of the ecosystem copied)
  - Soft-prompts, dynamic World Info triggers, adventure action format, save/load, import of AI Dungeon adventures
- **Takeaways for humanization:** The Memory / Author's Note / World Info split is the community-hardened answer to "how do I keep the voice and world coherent over 50k words?" Author's Note in particular — a string injected N tokens before the latest output — is the single cheapest, most reliable technique for re-asserting prose style on long outputs and is directly transferable to any humanization pipeline.
- **README quote:** "KoboldAI is generative AI software optimized for fictional use, but capable of much more!"
- **Summary:** The founding project of the open-source creative-writing stack. Study its prompt architecture, sampler defaults, and mode-specific context management before designing a humanization-focused writing system.

## 2. KoboldAI Lite / KoboldCpp (creative-writing surface)

- **URL:** https://github.com/LostRuins/koboldcpp
- **Author:** LostRuins (packages KoboldAI Lite as the default web UI)
- **Stars:** ~9,900
- **Updated:** Very active (2026)
- **License:** AGPL-3.0
- **Description:** Single-binary C++ server built on llama.cpp, exposing KoboldAI's HTTP API plus a bundled Lite UI with story/adventure/chat/instruct modes.
- **Techniques relevant to creative writing:**
  - **Context shifting** — keeps the opening prompt / style anchor pinned while evicting old turns, which measurably reduces "voice drift" on long stories.
  - **Grammar-constrained generation (GBNF)** — lets you force structural beats (scene headers, act breaks, dialogue-only blocks) without relying on the model to comply.
  - Mirostat, DRY, XTC, and min-p samplers exposed in the UI — the community's answer to "too slop, too repetitive."
- **Takeaways for humanization:** Context shifting is the under-appreciated lever. Most "the story forgot its opening voice" failures come from the system prompt rolling out of context; koboldcpp solves this at the inference layer, not at the prompt layer.
- **README quote:** "KoboldCpp is an easy-to-use AI text-generation software for GGML and GGUF models, inspired by the original KoboldAI."
- **Summary:** The inference backend that most serious creative-writing setups actually sit on top of. Its sampler + context-shift combo is the cheapest known way to make a mediocre model feel more human over long outputs.

## 3. Oobabooga text-generation-webui — creative presets

- **URL:** https://github.com/oobabooga/text-generation-webui
- **Author:** oobabooga
- **Stars:** ~46,400
- **Updated:** Active (2026), v4.0 released
- **License:** AGPL-3.0
- **Description:** Dominant local LLM frontend; ships with a large registry of **sampler presets** ranked by a community "Preset Arena" blind vote that is the closest thing the open-source world has to a canonical list of "best settings for creative output."
- **Techniques / notable presets:**
  - **Divine Intellect**, **Big O**, **simple-1** — top instruct presets from the Arena
  - **Midnight Enigma**, **Yara**, **Shortwave** — top chat/roleplay presets (high-variance, low-repetition, lean on min-p)
  - **Mirostat**, **LLaMA-Precise**, **Debug-deterministic** — baselines
  - Full sampler stack: temperature, top-p, top-k, min-p, DRY (Don't Repeat Yourself), XTC (eXclude Top Choices), typical_p, quadratic/smoothing
  - Character tab compatible with TavernAI PNG cards; Notebook mode for raw completion
- **Takeaways for humanization:** The Preset Arena is rare ground-truth data on which sampler stacks humans actually prefer for chat/fiction. The pattern that wins is not "high temperature" but **high min-p + moderate temperature + DRY to suppress clichés** — a concrete recipe any humanization system can copy. Creative presets also turn out to matter *more* than the persona prompt for felt humanness; a well-prompted model on `Debug-deterministic` still sounds like a robot.
- **README quote:** "A Gradio web UI for Large Language Models. Supports transformers, GPTQ, AWQ, EXL2, llama.cpp (GGUF), Llama models."
- **Summary:** The sampler-preset registry is the most battle-tested open artifact in this space. A humanization pipeline should either ship text-gen-webui-compatible presets or borrow the Preset Arena's winners directly.

## 4. Gryphe/MythoMax-L2-13b

- **URL:** https://huggingface.co/Gryphe/MythoMax-L2-13b
- **Author:** Gryphe
- **Downloads:** 728k+ all-time; ~377 likes; still the most-downloaded legacy creative-writing 13B
- **Updated:** Frozen (Aug 2023 base, README last touched Apr 2024); "legacy" status now that Llama 3 has landed
- **License:** Llama 2 community (listed as "other")
- **Description:** Experimental tensor-level merge of `MythoLogic-L2` (understanding) and `Huginn` (writing), using per-tensor gradient ratios across all 363 tensors rather than a uniform weighted average.
- **Techniques:**
  - Gradient-ratio block merging via Gryphe's own [BlockMerge_Gradient](https://github.com/Gryphe/BlockMerge_Gradient) tool
  - Alpaca prompt format; standard roleplay preamble
  - Spawned a family of further merges (Mythalion, MythoMix, MythoMist)
- **Takeaways for humanization:** MythoMax codified the "understanding model → writing model" sandwich that every later creative merge riffs on, and demonstrated that **tensor-level, non-uniform merges beat uniform-weight merges for prose quality**. The practical takeaway: the interpolation ratio should not be constant across layers if you care about voice — front/back tensors behave differently from middle tensors.
- **README quote:** "This model is proficient at both roleplaying and storywriting due to its unique nature... MythoLogic-L2's robust understanding as its input and Huginn's extensive writing capability as its output seems to have resulted in a model that exceeds at both."
- **Summary:** The archetypal community creative-writing LLM and the one whose merge methodology (gradient block merges) became the template for the entire roleplay/writing model scene.

## 5. Gryphe/MythoMist-7b

- **URL:** https://huggingface.co/Gryphe/MythoMist-7b
- **Author:** Gryphe
- **Updated:** Late 2023 experimental release; deliberately superseded but methodologically important
- **License:** Llama 2 community
- **Description:** 7B Mistral-based experimental merge of **12 constituent models**, assembled layer-by-layer by an **algorithmic merger that benchmarks during construction** — optimized specifically to *reduce* canonical "ChatGPT-isms" in creative writing.
- **Techniques:**
  - Algorithmic layer-by-layer merging with an inline evaluation step
  - Top contributors: `Neural-chat-7b-v3-1` (26%), `Synatra-7B-v0.3-RP` (22%), with 10 more at smaller ratios
  - Explicit optimization target: suppression of overused GPT vocabulary ("anticipation," "ministrations," "shivers," etc.)
- **Takeaways for humanization:** MythoMist is the clearest existence proof that **"sounding less like an LLM" is an optimizable objective at merge time, not only at sampler time.** This is directly the humanization thesis — optimize against slop vocabulary and syntactic patterns rather than against MMLU.
- **README quote:** "MythoMist 7b is, as always, a highly experimental Mistral-based merge... My main goal was to reduce usage of the word anticipation, ministrations and other such often-seen generative word in ChatGPT roleplaying data."
- **Summary:** Small, niche, and partly superseded, but the methodology — "merge against a slop-vocabulary loss" — is worth lifting wholesale into a humanization pipeline.

## 6. alpindale/goliath-120b

- **URL:** https://huggingface.co/alpindale/goliath-120b
- **Author:** alpindale
- **Likes:** 217
- **Updated:** Released Nov 2023; one of the most-cited "prestige" creative-writing merges
- **License:** Llama 2 community
- **Description:** 120B auto-regressive model assembled from two Llama-2-70B fine-tunes (**Xwin** and **Euryale**) via a layered interleave using `mergekit`, not a simple weight average.
- **Techniques:**
  - mergekit-based *frankenmerge* (interleaved layer stacks from two distinct 70Bs into a 120-layer tower)
  - 6,144-token context; Vicuna or Alpaca prompt formats
  - Quantized by TheBloke and Panchovix for consumer hardware
- **Takeaways for humanization:** Goliath's "show, don't tell," willingness to use profane/colorful language on demand, and genuine humor (puns, wordplay) are repeatedly cited as the reason community users prefer it over larger closed models for fiction. The result argues that **interleaved frankenmerges of two well-chosen 70Bs can out-voice a frontier model on long-form creative prose** — even if they underperform on benchmarks.
- **Summary:** The prestige reference for "open-source creative writing model" in 2024. Its existence is the strongest community evidence that humanization and benchmark performance are partially orthogonal axes.

## 7. sophosympatheia/Midnight-Miqu-70B-v1.5

- **URL:** https://huggingface.co/sophosympatheia/Midnight-Miqu-70B-v1.5
- **Author:** sophosympatheia
- **Likes:** ~200; ~11k downloads on v1.5 alone
- **Updated:** March 2024 (v1.5); v2.0 line has continued into 2025–2026
- **License:** Derived from leaked Miqu (ambiguous licensing; widely used despite)
- **Description:** DARE Linear / SLERP merge combining Midnight-Rose and Miqu-70B (and, in v1.5, `migtissera/Tess-70B-v1.6`), specifically tuned for roleplaying and storytelling with uncensored behaviour and coherent long-context output.
- **Techniques:**
  - Long-context support — "runs coherently to 32k with alpha_rope 1, to ~64k with alpha_rope 2.5" per model card
  - Recommends **quadratic/smoothing sampler at ~0.2** as the canonical creative-writing sampler
  - Ships recommended SillyTavern prompt template and sampler preset JSON directly in the repo
- **Takeaways for humanization:** Two transferable practices: (a) **shipping the sampler/preset JSON alongside the weights** is the right way to deliver a "voice" — weights alone are underspecified; (b) quadratic sampling consistently beats temperature-only at keeping long prose varied without going incoherent.
- **README quote:** "This model was designed for roleplaying and storytelling and I think it does well at both."
- **Summary:** The benchmark creative-writing 70B for most of 2024–2025. Its "weights + sampler preset + prompt template, as one bundle" release format is the pattern to copy.

## 8. Sao10K — Euryale / Fimbulvetr / Stheno series

- **URLs:**
  - Euryale 70B — https://huggingface.co/Sao10K/L3.1-70B-Euryale-v2.2 (and L3.3 successors)
  - Fimbulvetr 11B v2 — https://huggingface.co/Sao10K/Fimbulvetr-11B-v2
  - Stheno 8B v3.3 (32K) — https://huggingface.co/Sao10K/L3-8B-Stheno-v3.3-32K
  - Lunaris 8B — https://huggingface.co/Sao10K/L3-8B-Lunaris-v1
- **Author:** Sao10K
- **Updated:** Continuously maintained 2023–2026 across Llama 2 / 3 / 3.1 / 3.3 generations
- **Description:** The most prolific single author of creative-writing-first open LLMs. Each model is explicitly positioned by size niche: Stheno 8B (fast), Fimbulvetr 11B (verbose narrator), Lunaris 8B (balanced), Euryale 70B (prestige roleplay/storytelling).
- **Techniques:**
  - Curated SFT + DPO on roleplay / creative-writing datasets, per model card notes
  - Explicit fine-tunes for each new Llama base rather than merges of other people's fine-tunes
  - Per-model sampler and prompt-format recommendations in the cards
- **Takeaways for humanization:** Sao10K's catalog is a natural experiment in "what is the minimum model size at which fiction starts feeling human?" Community consensus clusters at **~8B for acceptable short roleplay, ~11B for consistent narrator voice, ~70B for prose that rivals closed frontier models.** That is useful prior data for any humanization system sizing its target model.
- **Summary:** The single most important open-source creative-writing model author of this era. Any humanization evaluation should include at least Stheno-8B and Euryale-70B as sized reference points.

## 9. google-deepmind/dramatron

- **URL:** https://github.com/google-deepmind/dramatron
- **Author:** Google DeepMind (Mirowski et al., 2022)
- **Stars:** ~1,075
- **Updated:** Minimal maintenance since initial release; still the canonical reference for hierarchical script generation
- **License:** Apache-2.0
- **Description:** Co-writing tool for **screenplays and theatre scripts** that generates a full script top-down from a log line: title → characters → plot (Hero's Journey beats) → location descriptions → scene-by-scene dialogue, via prompt chaining.
- **Techniques:**
  - Hierarchical generation with prompt chaining — each stage's output is the next stage's context
  - Log-line → title → characters → plot points → descriptions → dialogue
  - Evaluated with 15 theatre/film industry professionals; 4 Dramatron-co-written scripts staged publicly as *Plays by Bots*
- **Takeaways for humanization:** Dramatron is the cleanest academic articulation of the pattern that almost every long-form writing system reinvents: **decompose the story into a shallow tree, generate each level conditioned on ancestors, never try to generate 10k tokens in one shot.** The user study also surfaces a crucial humanization constraint — professionals *don't* want autonomous output; they want a system that explores alternative branches around their log line.
- **README quote:** "Dramatron uses large language models to generate coherent scripts and screenplays."
- **Summary:** Required reading for anyone building long-form creative-writing systems. Its hierarchical recipe is now table stakes; its HCI finding (writers want branching, not finished drafts) is underused.

## 10. yangkevin2 — Re3 and DOC

- **URLs:**
  - Re3 — https://github.com/yangkevin2/emnlp22-re3-story-generation
  - DOC — https://github.com/yangkevin2/doc-story-generation
- **Author:** Kevin Yang et al. (UC Berkeley)
- **Stars:** ~162 (DOC), smaller on Re3
- **Updated:** Re3 (EMNLP 2022); DOC (Dec 2022 / ACL 2023)
- **Description:**
  - **Re3**: Plan → Draft → Rewrite → Edit pipeline that produces ~2000+-word stories. Generates a structured outline, drafts continuations, reranks for plot coherence / premise relevance, and edits for factual consistency.
  - **DOC**: successor that produces ~3,500+-word stories with a **detailed outline** (characters, scene breakdowns) and a **controller** that keeps the draft aligned to that outline during generation.
- **Techniques:**
  - Reranking via premise-relevance and coherence classifiers (not just likelihood)
  - Explicit factual-consistency edit pass
  - Outline as a structured object the generator is re-conditioned on at every step
- **Takeaways for humanization:** Re3/DOC operationalize the intuition that **coherent long-form prose is a search + revise problem, not a single-pass sampling problem.** Rerankers and edit passes are the humanization tools the open-source writing model scene under-uses; adding even a cheap coherence reranker on top of a good prose model is usually more impactful than swapping to a bigger model.
- **README quote:** "DOC's stories are judged by human annotators as substantially more coherent, relevant, and interesting compared to those written by our previous system, Re3."
- **Summary:** The best open-source academic pipelines for long-form story generation. Their architecture (outline object + reranker + edit pass) is directly reusable as scaffolding around any humanization-tuned base model.

## 11. NousResearch/autonovel

- **URL:** https://github.com/NousResearch/autonovel
- **Author:** Nous Research
- **Updated:** Active (2025–2026)
- **Description:** End-to-end agentic pipeline that produces a full novel from a seed concept through foundation-building, first-draft, automated-revision, typesetting, illustration, and narration phases. First public output: *The Second Son of the House of Bells*, 79,456 words across 19 chapters.
- **Techniques:**
  - Multi-phase agent loop: world-bible → outline → chapter drafts → revision pass → export/typeset/TTS
  - Explicit separation between "foundation" (worldbuilding) and "narrative" (prose) state
  - LLM-agnostic; designed to swap in frontier or open models
- **Takeaways for humanization:** autonovel is the most complete open reference for "novel-length autonomous generation" as of 2026. The concrete output (a readable 80k-word novel) is strong prior art when scoping what a humanization stack *can* produce; and the revision-pass stage is where most of the humanization leverage lives.
- **Summary:** The open-source answer to closed services like Sudowrite's auto-draft and AI Dungeon's "Explore." Worth cloning and reading end-to-end before designing a humanization-focused long-form pipeline.

## 12. EdwardAThomson/StoryDaemon

- **URL:** https://github.com/EdwardAThomson/StoryDaemon
- **Author:** Edward A. Thomson
- **Updated:** Active (2025–2026)
- **Description:** Python-based agentic novel generator built on a deliberately **no-outline, emergent-structure** philosophy — the agent plans, writes, and evolves the story as it goes, with "evolving memory" for characters.
- **Techniques:**
  - Deep-POV writing prompts
  - Evolving character/story memory kept outside the context window
  - Automatic checkpointing and manuscript compilation
  - Backend-agnostic (Codex, Gemini, Claude)
- **Takeaways for humanization:** Interesting counter-design to Dramatron/DOC. Where those systems argue "outline first, never deviate," StoryDaemon argues that **emergent structure produces more human prose** at the cost of plot coherence. Worth running as an A/B study for any humanization project since both philosophies have credible human-preference evidence.
- **Summary:** The strongest open expression of the "pantser" (vs. plotter) philosophy for AI story generation. Good natural experiment against Re3/DOC/autonovel.

## 13. raestrada/storycraftr

- **URL:** https://github.com/raestrada/storycraftr
- **Author:** Rodrigo Estrada
- **Stars:** ~122
- **Updated:** Active
- **Description:** CLI-first, open-source "AI book creation assistant" that organizes worldbuilding, book structure, and chapter generation with pluggable backends (OpenAI, OpenRouter, Ollama).
- **Techniques:** Project-level file layout (world bible, chapter scaffolds), Ollama/OpenRouter routing, iterative refinement commands.
- **Takeaways for humanization:** Demonstrates that a **filesystem-native, CLI-friendly** writing environment — as opposed to a web UI — is a viable shape for a humanization-aware writing tool and integrates cleanly with the rest of a developer's toolkit.
- **Summary:** A lightweight, production-ready reference for "how do you ship a novel-writing agent as a CLI?"

## 14. CoAuthor (dataset + interface)

- **URLs:**
  - Dataset / project page — https://coauthor.stanford.edu/
  - Interface — https://github.com/minalee-research/coauthor-interface
- **Author:** Mina Lee, Percy Liang, Qian Yang (Stanford HAI, CHI 2022)
- **Stars:** 100 (interface repo)
- **Description:** Human-AI collaborative writing **dataset and replay interface**. 1,445 writing sessions by 63 writers across 830 creative stories and 615 argumentative essays, recorded at keystroke granularity against four GPT-3 instances.
- **Techniques:**
  - **Tab-to-suggest** interaction: writer requests 5 suggestions, accepts/dismisses/edits
  - Keystroke-level event log with timestamps — full session replay
  - Public stats: 72.3% suggestion-acceptance rate, 72.6% of text human-written, avg 11.8 queries / session
- **Takeaways for humanization:** CoAuthor is the **only large open dataset that captures the fine-grained micro-behaviour of a human editing an AI suggestion.** That signal is priceless for humanization work: it reveals exactly which AI continuations humans rewrite, keep, or discard, which is a much stronger training target than "did the output look good in isolation."
- **README quote (dataset page):** "CoAuthor is a dataset designed for revealing GPT-3's capabilities in assisting creative and argumentative writing."
- **Summary:** The canonical open dataset of human-in-the-loop AI-assisted writing. Should be the first evaluation set any humanization system runs against — if your "humanized" suggestions have a lower acceptance rate than vanilla GPT-3 in 2022, you have a problem.

## 15. WritingPrompts dataset (fairseq + GPT-WritingPrompts)

- **URLs:**
  - Original (Fan et al. 2018, via fairseq) — https://github.com/facebookresearch/fairseq/tree/main/examples/stories
  - GPT-WritingPrompts (Huang et al. 2024) — https://github.com/KristinHuangg/gpt-writing-prompts
  - Filtered HF mirror — https://huggingface.co/datasets/RLAIF/WritingPrompts-Filtered
- **Author:** Fan, Lewis, Dauphin (original); Huang et al. (GPT-augmented successor)
- **Description:** The foundational open creative-writing dataset: **~300k Reddit r/WritingPrompts story–prompt pairs** (272,600 train / 15,138 test / 15,620 val, avg prompt 28 words, avg story 735 words). GPT-WritingPrompts augments the same prompts with GPT-3.5-generated stories to enable human-vs-LLM comparison — directly a "humanization" corpus.
- **Techniques:**
  - Hierarchical Neural Story Generation (Fan et al. 2018) — first generate a premise, then story conditioned on premise
  - Gated multi-scale self-attention and prompt-to-story fusion in the original model
  - GPT-WritingPrompts adds parallel LLM generations keyed to the same prompts for character-portrayal analysis
- **Takeaways for humanization:** GPT-WritingPrompts is an **off-the-shelf paired corpus of human vs. AI stories on matched prompts** — essentially a ready-made training / evaluation set for any "human vs AI style" classifier or humanization-style-transfer model.
- **Summary:** The backbone dataset for creative-writing LLM research since 2018, and, with the GPT-augmented fork, the single best open resource for training humanization classifiers and style-transfer objectives.

## 16. EQ-Bench Creative Writing (v3)

- **URL:** https://github.com/EQ-bench/creative-writing-bench
- **Author:** Sam Paech (EQ-Bench)
- **Stars:** ~99
- **Updated:** Active (2025–2026); powers the public leaderboard at https://eqbench.com/creative_writing.html
- **Description:** Open, reproducible creative-writing benchmark. Models produce 32 prompts × 3 iterations (96 pieces) at T=0.7, min_p=0.1; an LLM judge (recommended: Claude Sonnet 4) scores against a detailed rubric; scores are normalized via **Glicko-2 pairwise Elo** between neighbouring models.
- **Techniques:**
  - Hybrid evaluation: rubric scoring **plus** pairwise preference via Glicko-2
  - Explicit mitigation for **length, position, verbosity, and "poetic incoherence"** biases (the last one is aimed directly at GPT-style slop)
  - Anchor-model normalization for temporal consistency
- **Takeaways for humanization:** This is the public scoreboard the humanization project will be judged on whether it wants to be or not. The bias-mitigation list is essentially a "what AI prose gets wrong" checklist — length bloat, flowery incoherence, positional pandering — and doubles as a direct spec of what a humanization system needs to fix.
- **Summary:** The de-facto open leaderboard for creative-writing LLMs, with an unusually principled rubric. Treat it as both evaluation target *and* failure-mode taxonomy.

## 17. EQ-Bench Longform Writing Bench

- **URL:** https://github.com/EQ-bench/longform-writing-bench
- **Author:** Sam Paech
- **Stars:** ~34
- **Updated:** Active; leaderboard at https://eqbench.com/creative_writing_longform.html
- **Description:** Evaluates models on **multi-chapter short stories / novellas** (~8 chapters × ~1,000 words). Uses a 14-dimension rubric (character development, emotional engagement, plot coherence, prose quality, etc.) with Claude Sonnet as judge.
- **Techniques:** Structured four-phase prompt (brainstorm → plan → revise → write); per-chapter generation with state carried forward; 14-axis rubric scoring.
- **Takeaways for humanization:** The 14-axis rubric is one of the few public, granular breakdowns of "what makes long-form prose *good*" beyond vibes. For humanization work, the emotional-engagement and character-development axes are the ones closed models underperform on — and therefore the richest target.
- **Summary:** Sister benchmark to creative-writing-bench but for long-form work; closest public approximation to "is your model a good novelist?"

## 18. sam-paech/slop-score

- **URL:** https://github.com/sam-paech/slop-score
- **Author:** Sam Paech (same author as EQ-Bench)
- **Description:** Open-source "AI slop" detector that scores text against three learned patterns of LLM-style prose:
  - **60%** — overused "slop words" (vocabulary statistically more frequent in LLM output than human baselines)
  - **25%** — "not X, but Y" contrast constructions that LLMs over-produce
  - **15%** — slop trigrams (3-word phrases that cluster in LLM writing)
- **Techniques:** Curated slop-word list, n-gram overuse detection, contrast-pattern matching; browser-based for quick evaluation.
- **Takeaways for humanization:** **The most directly on-thesis open tool in this entire angle.** Slop-score is literally a scalar "how LLM does this sound" metric — trivially turnable into a training signal, a decoder-time reward, or a gate for humanized output. Any humanization stack should integrate it as a CI check at minimum.
- **Summary:** The open-source operationalization of "sound less like an LLM." A humanization project that doesn't measure slop-score is not measuring the thing.

## 19. EQ-Bench/Judgemark-v2

- **URL:** https://github.com/EQ-bench/Judgemark-v2
- **Author:** Sam Paech
- **Description:** Benchmark that evaluates **the judges, not the writers**: how well does a given LLM grade creative writing on axes like "nuanced characters" and "emotionally engaging"? Features a "book club" mode where judges debate before scoring.
- **Techniques:** Pairwise judge evaluation against ground-truth creative-writing rankings, with debate-aware scoring.
- **Takeaways for humanization:** If you build a humanization pipeline that uses an LLM judge somewhere in its loop (RM, DPO pairs, ranking), Judgemark tells you which judge models actually agree with humans on prose quality. Skipping this step is how humanization projects discover after the fact that they over-fit to a biased judge.
- **Summary:** The meta-benchmark every humanization pipeline needs before choosing its judge model.

## 20. WritingBench

- **URL:** https://github.com/X-PLUG/WritingBench (paper: arXiv 2503.05244)
- **Author:** Alibaba X-PLUG (2025)
- **Description:** Comprehensive generative-writing benchmark covering **6 core domains and 100 subdomains** — creative, persuasive, informative, technical. Notable for a **query-dependent evaluation framework**: instead of fixed rubrics, an LLM generates instance-specific criteria per prompt, and a fine-tuned critic model scores against them.
- **Techniques:** Dynamic per-prompt rubric generation, fine-tuned critic model, demonstration that 7B critics can match frontier judges, style/format/length-aware scoring.
- **Takeaways for humanization:** Fixed-rubric benchmarks (EQ-Bench) bias toward a specific taste; WritingBench's query-dependent rubric is a better fit for a humanization system that must serve many registers (gritty noir, whimsical fable, corporate memo). The fine-tuned-7B-critic result also lowers the cost floor of running a judge in an inner loop.
- **Summary:** The most flexible public benchmark for "does this model write well *for this specific task*" — complementary to EQ-Bench's fixed-rubric approach.

## 21. LongGenBench

- **URL:** https://github.com/mozhu621/LongGenBench (ICLR 2025)
- **Author:** Mozhu et al.
- **Description:** Benchmark specifically for **long-form generation** at 16K and 32K output tokens, covering creative writing, design proposals, and technical documentation. Measures coherence, instruction-following, and structural adherence over full generations rather than just their openings.
- **Techniques:** Instruction-laced prompts whose constraints must hold across the entire 16–32k output; automatic constraint-satisfaction metrics; per-segment coherence scoring.
- **Takeaways for humanization:** Exposes the "fine near the start, drift past 4k" failure mode that the humanization project likely cares about most. A humanization system that only measures the first 2k tokens is measuring the easy part.
- **Summary:** The best public benchmark for the specific problem where long-form AI prose dies — past ~8k tokens. Essential second evaluator alongside EQ-Bench longform.

## 22. prometheus-eval / BiGGen Bench

- **URL:** https://github.com/prometheus-eval/prometheus-eval (BiGGen paper: arXiv 2406.05761)
- **Author:** Kim et al. (NAACL 2025)
- **Description:** Open-source principled LM-as-judge framework (Prometheus 2) plus the **BiGGen Bench** — 9 capabilities × 77 tasks, **instance-specific** evaluation criteria rather than abstract "helpfulness"; 103 frontier models evaluated with 5 different judge LMs.
- **Techniques:** Instance-level rubric generation; direct comparison of multiple judge LMs to quantify judge disagreement; writing capability is one of the 9 core axes.
- **Takeaways for humanization:** Prometheus 2 is currently the best open judge model, and BiGGen's writing tasks are a cleaner alternative to proprietary-judge leaderboards. A humanization system can use Prometheus 2 as its inner-loop reward model without leaking to a commercial API.
- **Summary:** The open-weights judge stack that a humanization pipeline should default to for any LLM-as-judge step.

## 23. Picrew/awesome-llm-story-generation

- **URL:** https://github.com/Picrew/awesome-llm-story-generation
- **Author:** Picrew
- **Stars:** ~49 (small but substantive)
- **Description:** Curated list of ~145 LLM papers and open-source projects for story / novel / script generation, organized across ~10 categories (planning/decomposition, multi-agent collaboration, long-context coherence, refinement methods, etc.).
- **Takeaways for humanization:** The fastest map of the academic landscape for this angle. Any humanization roadmap should diff its planned techniques against this taxonomy before building anything.
- **Summary:** The best community-maintained index of academic work on LLM story generation; use it as a reading list, not an endpoint.

## 24. NovelAI-adjacent open tooling

- **NeviumX/NovelAI-Prompt-Preset-Manager** — https://github.com/NeviumX/NovelAI-Prompt-Preset-Manager — TypeScript userscript for managing prompt presets and wildcards on the NovelAI UI. Adds saved presets, `__token__` expansion, PNG metadata rewriting, import/export.
- **Context:** NovelAI's core storytelling models (Kayra 13B, Clio, Erato) and their prompt **Modules** and **Lorebook** features are closed-source, but the community has built open tooling around the edges (preset managers, memory/lore exporters, prompt-migration utilities).
- **Takeaways for humanization:** The pieces of NovelAI that the open-source world has successfully copied — prompt modules, lorebooks, sampler UIs — converge on the same primitives SillyTavern codified. The pieces nobody has re-implemented well (Kayra's instruction-in-braces syntax, Erato's per-module fine-tune slots) are the interesting open problems. If you are shipping a humanization writing tool, supporting Kayra-style `{ ... }` inline instructions is a low-cost compatibility win.
- **Summary:** Small repos, but collectively the community's living notes on what NovelAI got right and the open-source stack hasn't yet matched.

---

## Patterns

- **The open-source creative-writing stack is already opinionated about humanization.** Sampler presets (Midnight Enigma, Divine Intellect), merge recipes (MythoMist's explicit anti-slop optimization), and evaluators (slop-score, EQ-Bench's poetic-incoherence bias axis) are all *already* solving the same problem the humanization project is scoping. A humanization system that ignores them re-invents the wheel badly.
- **"Bundle" releases beat weight-only releases for voice.** Midnight-Miqu, Sao10K's Euryale, and MythoMax all ship weights + recommended sampler preset + prompt template as a unit. Weights alone underspecify voice by an enormous margin; this is the single most consistent practice across the winners.
- **Long-form generation is a pipeline problem, not a model problem.** Dramatron (hierarchical planning), Re3 (plan → draft → rewrite → edit), DOC (detailed outline controller), autonovel (multi-phase agent loop), and StoryDaemon (emergent agent loop) all agree that raw sampling past ~4k tokens collapses — you need **outlines + rerankers + edit passes** regardless of base model.
- **Purpose-built slop detectors now exist.** slop-score is the most direct operationalization of "sound less like an LLM" in the open world. EQ-Bench's rubric explicitly penalizes "poetic incoherence." Humanization has crossed from aesthetic opinion into a measurable, optimizable objective.
- **Human-in-the-loop datasets are the missing ingredient.** CoAuthor is the only public dataset capturing keystroke-level human *edits* of AI suggestions. GPT-WritingPrompts gives paired human/AI stories on identical prompts. Both are under-exploited; most humanization work trains against isolated human prose instead of against human reactions to AI prose, which is strictly weaker signal.
- **Sampler choice matters more than model choice at the margin.** The Preset Arena winners (Midnight Enigma, Yara, Shortwave) plus modern samplers (min-p, DRY, XTC, quadratic) consistently move outputs more than upgrading from a 13B to a 70B model. A humanization system without first-class sampler control is leaving the biggest lever on the table.
- **The "bland-assistant voice" is partly a data-mix problem, not a base-model problem.** MythoMist, Midnight-Miqu, Goliath, and the Sao10K catalog all take *fine* base models and produce dramatically more human-sounding prose by either merging against, or fine-tuning against, deliberately selected creative-writing corpora. Base-model humanization is possible with community-scale resources.

## Trends (2024 → 2026)

- **Writing-specific benchmarks became first-class.** EQ-Bench creative-writing-v3, longform-writing-bench, Judgemark-v2, WritingBench, LongGenBench — prior to 2024 there was essentially nothing; now there is a small but serious ecosystem. Expect a leaderboard war and rapid rubric refinement through 2026.
- **Slop-vocabulary suppression is moving from prompt to weights.** MythoMist merged against slop vocabulary in 2023 as a curiosity; by 2026 this is a standard objective at both merge and fine-tune time. Humanization pipelines will need to defend against an adversarial arms race between slop detectors and slop-avoiders.
- **Long-form pipelines are consolidating on: outline + controller + reranker + edit pass.** Re3 → DOC → autonovel → StoryDaemon shows convergence on the same four boxes, differing only in how rigidly the outline constrains the draft.
- **Instruction-tunable creative models are replacing pure "completion" models.** NovelAI's Kayra Instruct modules, Llama-3-based Euryale v2.2, and most 2025+ merges all support in-line directive syntax; pure pre-training-style base models for fiction are becoming legacy.
- **Small, cheap judges are beating GPT-4-as-judge for writing rubrics.** WritingBench's 7B critic, Prometheus 2, and CharacterRM (from the persona angle) all show ≥ human–human agreement on narrow prose rubrics at a fraction of the cost.
- **Community model ecosystem is consolidating around Llama 3 / 3.1 / 3.3.** The Mytho family is legacy (Llama 2 era); Midnight-Miqu is post-Miqu drift-limited; Sao10K's Llama 3.3 Euryale and similar 3.x-based merges are the live frontier.

## Gaps

- **No open dataset of *revisions* at scale.** CoAuthor is the gold standard but small (1,445 sessions). There is no public equivalent at millions-of-sessions scale, despite that being the most valuable signal for humanization training. This is the single biggest data gap in the angle.
- **No widely-agreed human-baseline corpus for slop-score-style metrics.** slop-score's word lists are hand-curated; an automated, continuously-updated, large-scale human-vs-AI reference corpus would make slop suppression reproducible. Nobody has built it openly.
- **Affect / emotional-trajectory evaluation is still subjective.** EQ-Bench rubrics ask for "emotional engagement" but have no principled arc-level metric. There is no public benchmark for "does this story *feel* real" that isn't just "does a Claude judge say it feels real."
- **Multilingual open creative-writing benchmarks are absent.** Almost all of this stack is English-only; Chinese has CharacterEval on the persona side but no equivalent on the story-craft side, and other languages have nothing.
- **Sampler/preset discovery is manual.** The Preset Arena is blind-voting at human scale; there is no public automated search for good sampler stacks against creative-writing benchmarks. A humanization project could probably produce a better Preset Arena winner in a week of automated search.
- **No open end-to-end system combines the best pieces.** The "ideal" stack — Euryale-70B weights + slop-score inner-loop reward + DOC-style outline controller + EQ-Bench rubric gate — does not exist as a single repo. Every current project picks two or three of these and leaves the rest on the table.
- **Human-AI revision interfaces are thin.** CoAuthor's tab-to-suggest is still the reference UI; nothing open has improved on it materially in four years, despite repeated evidence that **interaction design moves humanization-felt quality more than model choice**.

## Sources

- KoboldAI (henk717 / united) — https://github.com/henk717/KoboldAI
- KoboldAI-Client upstream — https://github.com/KoboldAI/KoboldAI-Client
- KoboldCpp — https://github.com/LostRuins/koboldcpp
- text-generation-webui — https://github.com/oobabooga/text-generation-webui (Parameters / Preset Arena wiki)
- Gryphe/MythoMax-L2-13b — https://huggingface.co/Gryphe/MythoMax-L2-13b
- Gryphe/MythoMist-7b — https://huggingface.co/Gryphe/MythoMist-7b
- Gryphe/BlockMerge_Gradient — https://github.com/Gryphe/BlockMerge_Gradient
- alpindale/goliath-120b — https://huggingface.co/alpindale/goliath-120b
- sophosympatheia/Midnight-Miqu-70B-v1.5 — https://huggingface.co/sophosympatheia/Midnight-Miqu-70B-v1.5
- Sao10K catalog — https://huggingface.co/Sao10K
- google-deepmind/dramatron — https://github.com/google-deepmind/dramatron (paper: arXiv 2209.14958)
- yangkevin2/emnlp22-re3-story-generation — https://github.com/yangkevin2/emnlp22-re3-story-generation (paper: arXiv 2210.06774)
- yangkevin2/doc-story-generation — https://github.com/yangkevin2/doc-story-generation
- NousResearch/autonovel — https://github.com/NousResearch/autonovel
- EdwardAThomson/StoryDaemon — https://github.com/EdwardAThomson/StoryDaemon
- raestrada/storycraftr — https://github.com/raestrada/storycraftr
- CoAuthor project — https://coauthor.stanford.edu/ (code: https://github.com/minalee-research/coauthor-interface, paper: arXiv 2201.06796)
- r/WritingPrompts via fairseq — https://github.com/facebookresearch/fairseq/tree/main/examples/stories (paper: arXiv 1805.04833)
- GPT-WritingPrompts — https://github.com/KristinHuangg/gpt-writing-prompts (paper: arXiv 2406.16767)
- EQ-Bench creative-writing-bench — https://github.com/EQ-bench/creative-writing-bench (leaderboard: https://eqbench.com/creative_writing.html)
- EQ-Bench longform-writing-bench — https://github.com/EQ-bench/longform-writing-bench
- EQ-Bench Judgemark-v2 — https://github.com/EQ-bench/Judgemark-v2
- sam-paech/slop-score — https://github.com/sam-paech/slop-score
- WritingBench — https://github.com/X-PLUG/WritingBench (paper: arXiv 2503.05244)
- LongGenBench — https://github.com/mozhu621/LongGenBench (ICLR 2025)
- prometheus-eval / BiGGen Bench — https://github.com/prometheus-eval/prometheus-eval (paper: arXiv 2406.05761)
- Picrew/awesome-llm-story-generation — https://github.com/Picrew/awesome-llm-story-generation
- NovelAI Prompt Preset Manager — https://github.com/NeviumX/NovelAI-Prompt-Preset-Manager
- NovelAI Kayra / Clio context — https://blog.novelai.net/introducing-novelai-lm-13b-402k-kayra-dabe8ff86fc6
