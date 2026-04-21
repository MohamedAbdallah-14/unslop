# C — Open-Source Case Study Repos & Cookbooks for AI Humanization

**Research value: high** — The OSS humanization landscape is large, fragmented, and mostly outside the flagship vendor cookbooks; real implementation patterns live in a long tail of skill repos, paraphraser research code, and stylometry projects rather than in LangChain/LlamaIndex/OpenAI proper.

**Last updated:** April 2026. Repos 1–14 are established as of pre-April 2025. The Additional supporting assets and Gaps sections have been updated to reflect 2025–2026 changes, including the proliferation of detector-bypass repos, the GPT-5 notebook shift, and new Anthropic tooling.

Scope: 14 core repos/notebooks plus new additions, covering (a) runnable humanization/style-transfer code or (b) reusable prompt/skill assets directly applicable to humanizing LLM output. Each entry uses the same fields so you can triage fast.

---

## Repo inventory

### 1. `anthropics/claude-cookbooks`
- **URL:** https://github.com/anthropics/anthropic-cookbook
- **Type:** Vendor cookbook (Jupyter notebooks)
- **Humanization relevance:** Indirect. No dedicated humanization notebook, but `misc/metaprompt.ipynb` is used as the starting point for style/tone prompts, and the repo's conventions for persona system prompts are widely copied into humanization skills.
- **Mechanism:** Metaprompt → seed style prompt → iterate. Style steering happens entirely in system prompt + examples.
- **Strength:** Canonical patterns, well-maintained.
- **Gap:** No before/after humanization eval, no anti-detection framing.

### 2. `openai/openai-cookbook` — `examples/gpt-5/prompt_personalities.ipynb`
- **URL:** https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/prompt_personalities.ipynb
- **Type:** Vendor cookbook notebook
- **Humanization relevance:** Closest official OpenAI treatment. Frames "personality" as an operational lever (consistency, drift reduction, brand alignment), not just aesthetic polish. Ships named personalities (Professional, etc.) as reusable system prompts.
- **Mechanism:** System-prompt-only; explicit note that personalities must not override task output formats.
- **Strength:** Clean mental model of persona-as-config.
- **Gap:** Examples skew corporate; no stylometric validation, no adversarial test against detectors. Updated to GPT-5 (August 2025) — notebooks now reference `reasoning_effort` as a persona-shaping dial in addition to system prompt.

### 3. `openai/openai-cookbook` — `examples/gpt-5/gpt-5-1_prompting_guide.ipynb`
- **URL:** https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5-1_prompting_guide.ipynb
- **Type:** Vendor cookbook notebook
- **Humanization relevance:** Provides the generic prompt-engineering scaffolding humanization builders build on: instruction placement (top+bottom), verbosity control, avoidance of acknowledgment filler, and `reasoning_effort` tuning.
- **Strength:** Ground truth on how GPT-5/5.1 actually follows style instructions. As of 2025, GPT-5 itself is explicitly less sycophantic than GPT-4o — the model is now a configurable humanization substrate in a way earlier models were not.
- **Gap:** Generic; humanization is left as an exercise.

### 4. `langchain-ai/langsmith-cookbook` — `optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb`
- **URL:** https://github.com/langchain-ai/langsmith-cookbook/blob/main/optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb
- **Type:** Cookbook notebook
- **Humanization relevance:** Iteratively refines a prompt using LLM+human feedback. Applicable as the optimization loop around a humanization system prompt when style is too hard to describe directly.
- **Mechanism:** Feedback-driven prompt bootstrapping.
- **Strength:** Real evaluator-in-the-loop pattern; pairs well with style eval rubrics.

### 5. LangChain Chat Loaders (blog + code)
- **URL:** https://blog.langchain.com/chat-loaders-finetune-a-chatmodel-in-your-voice
- **Type:** Official LangChain how-to + loader integrations (WhatsApp, Slack, Discord, Telegram, Messenger, Twitter)
- **Humanization relevance:** Explicitly motivates style/tone as the canonical use case for fine-tuning, because "style and tone are hard to capture in prompts." Demonstrates end-to-end pipeline: export chat logs → LC messages → fine-tune → deploy.
- **Mechanism:** Fine-tune-in-your-voice (vs prompt-only humanization).
- **Strength:** The best official reference for the "train on your own writing" pattern.
- **Gap:** No humanization eval; assumes you own a corpus.

### 6. `lguz/humanize-writing-skill`
- **URL:** https://github.com/lguz/humanize-writing-skill
- **Type:** Prompt/skill package (Claude Code plugin + vendor-agnostic)
- **Humanization relevance:** Direct. Explicit 3-pass editing pipeline:
  1. Vocabulary pass — 36+ banned "AI-isms" ("delve", "leverage", …).
  2. Structural pass — removes 10 patterns (parallel negation, tricolons, em-dash overuse, …).
  3. Human-texture pass — variable sentence length, contractions, unresolved thoughts.
- **Strength:** Clear staged architecture; portable across Claude, ChatGPT, Gemini, Cursor, Windsurf.
- **Gap:** Small repo, no benchmark numbers, limited tests.

### 7. `itsjwill/humanizer-x`
- **URL:** https://github.com/itsjwill/humanizer-x
- **Type:** Claude Code skill (4-pass engine + voice humanization)
- **Humanization relevance:** Direct. More aggressive sibling of (6). Notable for:
  - 30 severity-ranked AI patterns (ordered by detection risk).
  - Explicit statistical fingerprint manipulation (perplexity, burstiness, entropy).
  - SSML disfluency patterns for voice agents (uh, mm, restart fragments, …).
  - 6 voice modes and retail-API enrichment for personalized calls.
  - Pitched as a drop-in replacement for $10–20/mo paid humanizers.
- **Strength:** One of the few OSS projects that targets detector statistics *and* voice humanization in the same codebase.
- **Gap:** Small stars/forks, no third-party eval.

### 8. `conorbronsdon/avoid-ai-writing`
- **URL:** https://github.com/conorbronsdon/avoid-ai-writing
- **Type:** Portable skill (works with Claude Code, OpenClaw, Hermes)
- **Humanization relevance:** Direct. Two modes (rewrite vs detect-only), two-pass detection to catch patterns that survive the first edit, 109-entry 3-tier word replacement table with explicit alternatives ("Leverage → use", "Commence → start"). Outputs a structured audit (issues, rewrites, change summary).
- **Strength:** ~1.1k stars — the most widely adopted humanization skill in this batch. Strong auditing contract (structured diff).
- **Gap:** Vocabulary-heavy; lighter on structural/cognitive-texture passes than (7).

### 9. `ngpepin/stylometric-transfer`
- **URL:** https://github.com/ngpepin/stylometric-transfer
- **Type:** CLI + API
- **Humanization relevance:** Direct for *author-style* humanization (matching a specific human voice, not just "sound human"). Explicit JSON style fingerprints (explicit + LLM-generated), local stylometric measurements, LLM generation with deterministic post-processing, normalization controls, deviation reports.
- **Mechanism:** Fingerprint → generate → measure → diff loop.
- **Strength:** Interpretable — every style dimension is inspectable.
- **Gap:** Small repo; small corpus assumptions.

### 10. `aaddrick/written-voice-replication`
- **URL:** https://github.com/aaddrick/written-voice-replication
- **Type:** Claude Code skill pack
- **Humanization relevance:** Direct. Analyzes a writing corpus across 25 dimensions (readability, sentence structure, sentiment, rhetorical patterns). Outputs: voice agents, voice skills with detailed instruction sets, numeric profiles with measurable validation targets, 26 analysis reports.
- **Strength:** Runs entirely through Claude Code with no external NLP deps — good reference for "no-runtime" humanization.
- **Gap:** Tied to Claude Code ecosystem.

### 11. `ContextLab/llm-stylometry`
- **URL:** https://github.com/ContextLab/llm-stylometry
- **Type:** Research code + 320 pre-trained models
- **Humanization relevance:** Flip side — shows that per-author GPT-2 models *can* capture individual style well enough for authorship attribution. Directly useful as (a) evaluator for whether a humanized output matches a target author and (b) baseline for training voice clones.
- **Strength:** Ships 320 trained models + analysis/visualization package with tests.

### 12. `zacharyhorvitz/TinyStyler`
- **URL:** https://github.com/zacharyhorvitz/tinystyler
- **Type:** Research model + HF demo
- **Humanization relevance:** Few-shot text style transfer with authorship embeddings on an 800M model. Transforms source text to match a target style while preserving meaning.
- **Strength:** Small, fast, embedding-based — the efficient counterpoint to 11B DIPPER.
- **Gap:** Research project; integration work required.

### 13. `martiansideofthemoon/ai-detection-paraphrases` (DIPPER)
- **URL:** https://github.com/martiansideofthemoon/ai-detection-paraphrases
- **Type:** NeurIPS 2023 research code + 11B T5-XXL checkpoint on HF
- **Humanization relevance:** The canonical "paraphrase to evade detection" baseline. Two inference-time knobs: lexical diversity and content reordering. Paragraph-level (not sentence-level) paraphrasing with optional surrounding-context conditioning.
- **Reported results:** Drops DetectGPT from 70.3% → 4.6% accuracy at 1% FPR without significant semantic loss; also bypasses watermarking, GPTZero, and OpenAI's classifier (as of the paper).
- **Strength:** Single most-cited OSS reference point for humanization-as-paraphrase.
- **Gap:** 40 GB GPU required for full experiments; detectors have moved since 2023.

### 14. `HJJWorks/TempParaphraser`
- **URL:** https://github.com/HJJWorks/TempParaphraser
- **Type:** Research code (EMNLP 2025)
- **Humanization relevance:** Multi-round paraphrasing framework using fine-tuned models; positioned as a stronger successor to DIPPER against modern detectors while preserving semantics.
- **Strength:** Most recent research baseline (late 2025).
- **Gap:** As of early 2026, still low community adoption; has not yet been adopted in practitioner workflows as tracked by E-practical posts.

### 2025–2026 notable additions to the OSS landscape

- **`blader/humanizer`** (Claude Code skill, 2025) — Removes signs of AI-generated writing based on Wikipedia's "Signs of AI writing" guide, informed by observations of thousands of instances. Includes an audit pass and a second rewrite to catch lingering patterns. Represents the growing Claude Code skill niche that sidesteps the notebook format entirely.
- **`OrbitWebTools/Humanize-AI`** (2025) — Browser-based FOSS humanizer targeting Turnitin, ZeroGPT, and Originality.ai. Notable for being fully client-side with no login; illustrates the commoditization floor of browser-side humanizers.
- **Anthropic Petri (open-sourced 2025)** — Behavioral audit tool for sycophancy across multi-turn conversations. One Claude model (auditor) simulates scenarios; another (judge) grades. Not a humanization tool per se, but the first open-source eval harness explicitly measuring sycophancy as a behavioral property. Closes one of the most-cited gaps in the OSS landscape: absence of shared evaluation infrastructure.
- **GitHub `text-humanizer` topic** — As of April 2026, 40+ repos are tagged under this GitHub topic, up from fewer than 10 in early 2024. The proliferation reflects the "AI slop" cultural moment (Merriam-Webster Word of the Year 2025); most are low-quality synonym-swap tools, but the signal is that developer interest in the category is mainstream.

### Additional supporting assets (not counted in the 14 but relevant)

- **`samrand96/Undetectable-AI`** — DOCX-in, DOCX-out rewriter using Ollama or ChatGPT; good starter for doc-level pipelines.
- **`obaskly/AiTextDetectionBypass`** — Python wrapper that automates the undetectable.ai web product; useful only as a reference "what does a commercial humanizer actually do at the chunk boundary" implementation.
- **`ADEMOLA200/Humanize-AI`** — T5-based paraphraser service (Go + Flask), customizable transformations.
- **`ZAYUVALYA/AI-Text-Humanizer`** and **`ksanyok/TextHumanize`** — purely rule-based, client-side synonym-substitution humanizers; interesting mainly as a floor (non-LLM) baseline.
- **`viktorbezdek/definitive-llm-writing-style-guide`** — a taxonomy of personality traits (Big Five + assertiveness/empathy/optimism) mapped to generation style; useful as dial set.
- **`ManuelSLemos/awesome-llm-system-prompts`**, **`dontriskit/awesome-ai-system-prompts`**, **`langgptai/awesome-system-prompts`** — curated collections of real shipping system prompts from Claude/GPT/Gemini/Grok/Cursor/v0/Lovable/etc. Highest-signal source for "what do production LLM system prompts *actually* say about voice and tone?"
- **`Poll-The-People/customgpt-cookbook/personas`** — persona recipes for customer-facing bots; reusable for voice+tone templating.
- **`AutumnsGrove/ClaudeSkills/brand-guidelines`** and **`piaoyinghuang/brand-consistency-ai-skill`** — brand-voice JSON schemas + compliance checklists; closest thing to a shared "voice profile" standard across skills.
- **`jenna-russell/human_detectors`** — paired with (13); contains `evade.py` plus detector eval harness. Useful as the *measurement* side of any humanization pipeline.

---

## Patterns

1. **Staged rewrite pipelines dominate.** Repos 6, 7, 8 all converge on the same 3–5 stage shape: vocabulary scrub → structural scrub → human-texture injection → (optional) statistical fingerprint tuning → final checklist. This is the de-facto architecture, even without coordination.
2. **Banned-word tables are the universal starting artifact.** "Delve, leverage, commence, moreover, furthermore, in conclusion…" — every skill repo ships one. Sizes cluster at 30–110 entries, 2–3 severity tiers.
3. **Two humanization *goals* keep getting conflated but are actually distinct:**
   - (a) *Generic human-sounding* — remove AI-isms, add variance. Served by 6, 8.
   - (b) *Specific-author voice* — match fingerprint. Served by 9, 10, 11, 12. The architectures differ sharply (rules vs embeddings vs per-author models).
4. **Detector-oriented humanization is a separate third goal** that overlaps only partially with (a)/(b). Repos 7, 13, 14 explicitly target statistical signatures (perplexity, burstiness, entropy). Writers often don't need this; compliance/academic use cases do.
5. **System-prompt-only humanization is the cheap default; fine-tune-on-your-voice is the ceiling.** LangChain Chat Loaders (5) is the canonical reference for escalating from prompt to finetune when style is the bottleneck.
6. **"Skill" packaging is eating notebook packaging.** The newer high-signal artifacts (6, 7, 8, 10) ship as Claude Code / OpenClaw / Hermes skills, not `.ipynb`s. Cookbook notebooks are increasingly scaffolding, not the delivery surface.
7. **Structural/cognitive-texture injection is the hardest stage to get right.** Almost every skill leans on rules here (contractions, fragments, self-interruptions, uncertainty markers), but real human burstiness is noisier than any rule set captures — this is where pipelines visibly fail.
8. **Paragraph-level paraphrasing beats sentence-level.** DIPPER's headline contribution (contextual, paragraph-scoped rewrites) keeps reappearing as a quality floor. Sentence-by-sentence humanizers consistently underperform on cohesion.

## Gaps

1. **No official LangChain or LlamaIndex humanization cookbook.** LangSmith/LangChain have the *optimization loop* (4) and the *fine-tune path* (5), but no end-to-end humanization example. LlamaIndex has nothing beyond `Refine`/`TreeSummarize` which aren't humanization tools. Status as of April 2026: unchanged.
2. **Eval harness gap is partially addressed.** Anthropic's Petri (open-sourced 2025) provides sycophancy eval across multi-turn conversations. But no shared before/after humanization benchmark corpus exists. (13)'s evade.py + a current detector remains the closest community approximation.
3. **Voice-agent humanization is still underserved in OSS.** Only (7) (`humanizer-x`) meaningfully addresses SSML disfluencies. Commercial voice humanization has matured (Fin Voice, Sierra), but OSS tooling for voice hasn't followed.
4. **Statistical-fingerprint tooling is ad-hoc.** Perplexity/burstiness/entropy measurement is done inline in each repo; no shared library for "score these three stats and diff against a corpus." Status: unchanged.
5. **Brand voice profiles have no interchange format.** Brand-voice JSON schemas exist in 3+ repos but none are compatible; each skill re-invents the fields. Status: unchanged.
6. **Rule-based (non-LLM) humanizers are mostly toy** and have proliferated. The `text-humanizer` GitHub topic now has 40+ repos as of April 2026, most of which are synonym-swap floor implementations. The signal-to-noise ratio in the topic has fallen substantially since 2024.
7. **Detector drift is partially tracked by TempParaphraser; DIPPER numbers still widely cited.** DIPPER's 2023 numbers against DetectGPT are still cited as if current in practitioner posts (see E-practical). GPTZero, Originality.ai, and Turnitin all updated substantially through 2025. No public tracker maps how humanized corpora score over time as detectors update. TempParaphraser (EMNLP 2025) benchmarks against updated detectors but hasn't been replicated independently.
8. **The bypass-via-invisible-characters class (Concealy, unicode/homoglyph substitution) is risky and underexamined.** Several 2025 tools substitute visually-identical but machine-different characters to fool detectors. GPTZero confirmed patching one such bypass within days of discovery in 2025. No OSS repo tracks this class over time or measures how quickly counter-measures ship.

## Cross-domain analogies worth noting

- **Code formatters as a model.** `avoid-ai-writing` (8) and `humanize-writing-skill` (6) work like `ruff`/`prettier` for prose — deterministic AST-ish passes over structured patterns. The analogy suggests humanization tooling will trend toward formatter-style single-command UX and auto-fix on save.
- **Translation post-editing.** The multi-pass pipeline (draft → edit → texture → polish) mirrors MT post-editing workflows (MT → light PE → full PE → QA). Worth borrowing MT's eval conventions (BLEU/COMET analogues, adequacy vs fluency ratings) rather than inventing new ones.
- **Adversarial ML arms race.** DIPPER ↔ detectors (13, 14) is structurally identical to GAN/adversarial-example dynamics: each side trains against the other's current state. Expect the same "published numbers stale within 6 months" cadence.

---

## Sources

- https://github.com/anthropics/anthropic-cookbook — Anthropic Claude cookbooks repo (metaprompt, persona patterns).
- https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/prompt_personalities.ipynb — OpenAI cookbook notebook on personality-as-system-prompt.
- https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5-1_prompting_guide.ipynb — GPT-5.1 prompting guide (instruction placement, verbosity).
- https://github.com/langchain-ai/langsmith-cookbook/blob/main/optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb — LangSmith assisted prompt bootstrapping.
- https://blog.langchain.com/chat-loaders-finetune-a-chatmodel-in-your-voice — LangChain Chat Loaders (fine-tune on your voice).
- https://github.com/lguz/humanize-writing-skill — 3-pass humanization skill.
- https://github.com/itsjwill/humanizer-x — 4-pass humanizer + voice humanization.
- https://github.com/conorbronsdon/avoid-ai-writing — 1.1k-star audit+rewrite skill.
- https://github.com/ngpepin/stylometric-transfer — Interpretable stylometric fingerprints.
- https://github.com/aaddrick/written-voice-replication — 25-dimension voice profiling for Claude Code.
- https://github.com/ContextLab/llm-stylometry — 320 per-author GPT-2 models.
- https://github.com/zacharyhorvitz/tinystyler — Few-shot style transfer with authorship embeddings.
- https://github.com/martiansideofthemoon/ai-detection-paraphrases — DIPPER paraphraser (NeurIPS 2023).
- https://github.com/HJJWorks/TempParaphraser — EMNLP 2025 multi-round paraphrasing.
- https://github.com/jenna-russell/human_detectors — Detector + evasion eval harness.
- https://github.com/dontriskit/awesome-ai-system-prompts — Curated real-world system prompts (5.7k stars).
- https://github.com/langgptai/awesome-system-prompts — Bilingual curated LLM/agent system prompts.
- https://github.com/viktorbezdek/definitive-llm-writing-style-guide — Big Five / trait→style mapping.
- https://github.com/Poll-The-People/customgpt-cookbook/tree/main/personas — Persona recipes.
- https://github.com/samrand96/Undetectable-AI — DOCX rewrite pipeline.
- https://github.com/obaskly/AiTextDetectionBypass — Commercial-humanizer wrapper (reference only).
- https://github.com/ADEMOLA200/Humanize-AI — T5-based humanization service.
- https://github.com/ZAYUVALYA/AI-Text-Humanizer — Rule-based client-side humanizer (baseline floor).
- https://github.com/ksanyok/TextHumanize — Multi-language rule-based humanizer (baseline floor).
- https://github.com/blader/humanizer — Claude Code skill removing AI-writing signs per Wikipedia guide (2025).
- https://github.com/OrbitWebTools/Humanize-AI — Browser-based FOSS humanizer targeting Turnitin/ZeroGPT/Originality (2025).
- https://github.com/topics/text-humanizer — GitHub topic: 40+ repos as of April 2026.
- https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models — Anthropic sycophancy research underlying Petri tool.
- https://gptzero.me/news/gptzero-by-passers/ — GPTZero's greylisting of bypass methods; confirms days-to-patch cadence.
