# Prompt Engineering for Humanization — Open-Source & GitHub

**Research value: high** — The open-source landscape around "humanizing" AI output is unusually dense and recent (most relevant repos updated 2025–2026), with two distinct camps (detector-evasion vs. style quality) and a clear set of recurring patterns that a new project can build on directly rather than reinvent.

## Executive Summary

Open-source work on humanizing AI output clusters into five layers. (1) Pattern-based rewriters like `blader/humanizer` (14.5K★) and `aaaronmiller/humanize-writing` codify "signs of AI writing" — AI vocabulary, em-dash overuse, tricolons, rule-of-three, sycophancy — into reusable Claude Code / skill files with before/after tables. (2) Detector-evasion tooling (`Mohit1053/Humanizer`, `Oct4Pie/zero-zerogpt`, `POlLLOGAMER/Humanizer-Prompt-Advanced`, `friuns2/BlackFriday-GPTs-Prompts`, `ZyluxXD/zerobypass`) optimizes for bypassing GPTZero/ZeroGPT/Copyleaks via perplexity/burstiness manipulation, Unicode tokenization attacks, Spanish round-trips, or synthetic keystroke timing. (3) Persona libraries (`f/awesome-chatgpt-prompts` / `prompts.chat` at 160K★, `ai-boost/awesome-prompts` at 7.6K★, `KudoAI/ai-personas`, `PersonaCraft`) supply "act-as" characters and voice templates. (4) Framework-level humanization is ambient in `stanfordnlp/dspy` (learnable signatures + `ChainOfThought`), `guidance-ai/guidance`, `LMQL`, `promptfoo/promptfoo`, and `LlamaIndex` built-in personas (`SHAKESPEARE_WRITING_ASSISTANT`, etc.). (5) System-prompt leak archives (`asgeirtj/system_prompts_leaks` at 38.6K★, `jujumilk3/leaked-system-prompts` at 14.5K★) give builders working examples of how frontier labs themselves instruct tone, hedging, and persona.

The strongest shared insight across repos: humanization is a *subtraction* problem more than an addition one — the single highest-leverage move is removing a known blacklist of AI-isms (tricolons, "It's not just X, it's Y", em dashes, "testament", "landscape", sycophantic openers, "In conclusion"), with voice calibration from a user-supplied writing sample as the next tier.

## Sources

### Humanization / Rewriter Skills

- **blader/humanizer** — `github.com/blader/humanizer` — author: blader — ~14,477★ — last release v2.5.1 (2026). Claude Code/OpenCode skill that rewrites AI text against a 29-pattern checklist derived from Wikipedia's "Signs of AI writing" guide. Patterns span content (significance inflation, notability name-dropping, superficial -ing analyses, promotional language, vague attributions, formulaic "despite challenges" closers), language (AI vocabulary, copula avoidance, negative parallelisms, rule-of-three, synonym cycling, false ranges, passive voice), style (em-dash overuse, boldface overuse, title-case headings, emojis, curly quotes, hyphenated word-pair overuse, persuasive-authority tropes, signposting, fragmented headers), chatbot artifacts (sycophancy, cutoff disclaimers, "I hope this helps"), and filler/hedging. Includes a second "obviously AI generated" audit pass and a voice-calibration mode that ingests user writing samples. MIT-licensed. *This is the de facto reference implementation.*

- **lguz/humanize-writing-skill** — `github.com/lguz/humanize-writing-skill` — small star count — 2025. 3-pass editing system with 36+ banned words, 10 structural patterns, and a quality checklist. Works with Claude, ChatGPT, Gemini, Cursor, Windsurf. Distributed as two markdown files or a Claude Code plugin. Explicitly targets parallel negation, tricolons, varied sentence length, and contraction injection.

- **aaaronmiller/humanize-writing** — `github.com/aaaronmiller/humanize-writing` — 2025. Production-style skill bundle (~65 KB) with a 10.6 KB `SKILL.md`, an `ai-vocabulary-blacklist.md` listing 50+ overused transitions, a `sentence-patterns-rhythm.md` with 5 common AI cadences, and `content-type-guides.md` for blog, academic, marketing, and email contexts. Notable for per-content-type guidance rather than one-size-fits-all.

- **SabrinaRamonov/prompts — humanize_ai_text.md / humanize_ai_writing.md** — `github.com/SabrinaRamonov/prompts` — ~895★ — 2024/2025. Minimal copy-paste prompts instructing the model to "act as an AI-writing humanizer": vary sentence structure, add contractions/idioms, remove "Furthermore" / "In conclusion" and excessive passive voice, inject rhetorical questions, analogies, and humor. Ships with the "ask clarifying questions until 95% confident" meta-framing pattern.

- **Mohit1053/Humanizer** — `github.com/Mohit1053/Humanizer` — Dec 2025. Python + Ollama/Llama3 batch humanizer aimed at beating GPTZero and ZeroGPT via "perplexity variation, burstiness, human quirks, and emotional authenticity". Supports batch processing, resume, and multiple optimized prompt versions.

- **POlLLOGAMER/Humanizer-Prompt-Advanced** — `github.com/POlLLOGAMER/Humanizer-Prompt-Advanced` — 2025. Uses a translation round-trip (English → Spanish → English) plus intentional minor misspellings and structural inconsistencies; claims near-100% detector evasion. Illustrative of the "noise injection via pivot language" family.

- **x1xhlol/system-prompts-and-models-of-ai-tools PR #50 (Humanizer AI Prompt)** — `github.com/x1xhlol/system-prompts-and-models-of-ai-tools` — ~135K★ — 2025. Proposed template that parameterizes humanization: 40% word preservation, 75% semantic preservation, 60% creativity, 70% style mimicry. Interesting as an attempt at *quantified* humanization dials.

- **Brandon689/best-ai-humanizer** — `github.com/Brandon689/best-ai-humanizer` — awesome-list of hosted AI-humanizer tools (TurnItIn/GPTZero evasion). Useful for competitive landscape, not for prompts.

### Detector-Evasion Tooling

- **Oct4Pie/zero-zerogpt** — `github.com/Oct4Pie/zero-zerogpt`. JavaScript tool that replaces standard spaces with Unicode space characters, disrupting tokenization-based detectors; includes PDF support. Exploits detector pipeline rather than text style.

- **jayyt12161/GPTZero-Bypasser** — Python rewriter converting "likely AI-written" to "likely human-written" via transformation rules.

- **ZyluxXD/zerobypass** — Playwright automation that simulates human keystroke timing to defeat "document replay" detection. Complements text-level approaches with behavior-level evasion.

- **friuns2/BlackFriday-GPTs-Prompts — `evade-ai-detectors-undetectable-text-against-gpt-zero-copyleaks-etc.md`** — jailbreak-style instruction that tells the model to heavily obfuscate text while preserving meaning, through vocabulary variation and style-switching, with iteration-based effectiveness.

### Persona / Voice Libraries

- **f/awesome-chatgpt-prompts (now prompts.chat)** — `github.com/f/awesome-chatgpt-prompts` — ~160,098★ — originally Dec 2022, maintained through 2026. Largest open prompt library; 157+ "act as …" personas for ChatGPT/Claude/Gemini/Llama/Mistral. Distributed via website, CSV, Hugging Face dataset, CLI (`npx prompts.chat`), MCP servers, and Claude plugins. Referenced by 40+ academic papers. *The canonical persona-prompt corpus.*

- **ai-boost/awesome-prompts** — `github.com/ai-boost/awesome-prompts` — ~7,619★. Curated prompts pulled from top-rated GPTs in the GPT Store, explicitly separating "prompt templates" (persona system prompts) from "prompt engineering" (DSPy/promptfoo/Guidance/TextGrad/GEPA). 200+ prompts across coding, DevOps, writing, product.

- **KudoAI/ai-personas** — `github.com/KudoAI/ai-personas`. "Epic prompts to turbo-charge LLM chatbots" across OpenAI/Claude/Bard; NLP, chatbots, roleplay focus.

- **Dantheman23-coder/AI-Persona-Prompts (PersonaCraft)** — 71 persona prompts based on historical figures (Tesla, da Vinci, Curie, Einstein) with full system-prompt and voice-dictation variants, plus a Python CLI `/use` loader.

- **BOBeirne/gemini-persona-prompts** — Structured role personas (DocumentAdvocate, PsychNavigator, PromptEngineer, ITMaster) in Claude XML, Gemini markdown, GPT markdown, Microsoft 365 Copilot, and Ollama formats. Good reference for cross-model persona portability.

- **0xk1h0/ChatGPT_DAN** — `github.com/0xk1h0/chatgpt_dan` — ~11,600★. DAN and variants (Evil DAN, S-DAN II, Neo DAN V3). Not a humanization tool per se, but the oldest large-scale community study of how persona framing overrides default assistant tone — directly relevant to understanding why persona prompts shift voice.

### Frameworks (humanization as a side-effect of programmatic prompt design)

- **stanfordnlp/dspy** — `github.com/stanfordnlp/dspy`. Treats prompts as learnable parameters. Signatures (e.g. `"document -> summary"`) plus `ChainOfThought`, `Predict`, and optimizers (`MIPROv2`, `BootstrapFewShot`, `BootstrapFinetune`) auto-generate instructions grounded in program structure and data, typically producing more natural phrasing than hand-written prompts. Paperspace/AgentPatterns report 25%+ gains on GPT-3.5 and 65%+ on llama2-13b pipelines, 5–46% over expert-written prompts. Caveat: optimized prompts rarely transfer across models.

- **guidance-ai/guidance (Microsoft)** — Handlebars-style template syntax with token-level steering. Constraints via `select()`, `regex()`, context-free grammars. Relevant to humanization for enforcing sentence-length distributions, contraction frequencies, or register-specific vocabulary at inference.

- **LMQL** — `lmql.ai`. Python-embedded DSL with declarative `where` constraints, typed variables, and multi-backend support (OpenAI / transformers / llama.cpp). Lets humanization rules be written as hard constraints rather than prompt nudges.

- **promptfoo/promptfoo** — `github.com/promptfoo/promptfoo`. Eval and red-team CLI used by OpenAI and Anthropic. Relevant as the evaluation layer any serious humanization project needs (A/B humanized vs. raw outputs, detection-rate metrics, style-drift metrics).

- **LlamaIndex built-in personas** — `docs.llamaindex.ai/.../chat_engine_personality`. `SHAKESPEARE_WRITING_ASSISTANT`, `MARKETING_WRITING_ASSISTANT`, `IRS_TAX_CHATBOT` plus `RichPromptTemplate`/`ChatPromptTemplate`. Demonstrates the "pre-baked persona constants" pattern in framework code.

- **dair-ai/Prompt-Engineering-Guide** — `github.com/dair-ai/Prompt-Engineering-Guide` — ~73,000★, 3M+ learners, 13 languages. Reference curriculum on zero-shot, few-shot, CoT, self-consistency, and instruction design. Foundational context for any humanization prompt design.

### System-Prompt Leak Archives

- **asgeirtj/system_prompts_leaks** — `github.com/asgeirtj/system_prompts_leaks` — ~38,589★ — created May 2025, pushed Apr 17 2026. Extracted system prompts from ChatGPT (GPT-5.4, GPT-5.3, Codex), Claude (Opus 4.6, Sonnet 4.6, Claude Code), Gemini (3.1 Pro, 3 Flash, CLI), Grok (4.2, 4), Perplexity. MIT, 20 contributors. The primary source for "how do frontier labs themselves instruct tone/persona/hedging".

- **jujumilk3/leaked-system-prompts** — `github.com/jujumilk3/leaked-system-prompts` — ~14,488★ — last pushed March 2026. Second major archive, broader historical coverage.

## Key Techniques / Patterns

1. **Blacklist-driven rewriting.** The most consistent pattern across `blader/humanizer`, `lguz/humanize-writing-skill`, `aaaronmiller/humanize-writing`, and `SabrinaRamonov/prompts` is a concrete list of banned words/phrases (36–50+ items): "testament", "landscape", "nestled", "Furthermore", "In conclusion", "It's not just X, it's Y", "delve", "showcase", "intricate", "pivotal". Removal first, rewriting second.

2. **Structural pattern breaking.** Explicit rules against tricolons ("rule of three"), negative parallelisms, synonym cycling, false ranges ("from X to Y"), em-dash overuse, boldface overuse, and title-case headings. Treated as style fingerprints, not style preferences.

3. **Multi-pass / audit architecture.** `blader/humanizer` v2.2+ adds a final "obviously AI generated" audit pass and second rewrite. `lguz/humanize-writing-skill` uses a 3-pass system (content → structure → texture). The pattern: detect, rewrite, re-detect, rewrite again.

4. **Voice calibration from a user sample.** `blader/humanizer` v2.4 introduced a mode where the user pastes 2–3 paragraphs of their own writing and the skill extracts sentence rhythm, word choice, and quirks before rewriting. This is distinct from generic "sound human" and arguably the frontier technique.

5. **Parameterized humanization dials.** x1xhlol PR #50's (word preservation %, semantic preservation %, creativity %, style mimicry %) and Mohit1053's (perplexity variation, burstiness, emotional authenticity) turn qualitative goals into quantitative knobs, though without public validation.

6. **Detector-aware evasion.** Three distinct families: (a) *text-level* — vocabulary variation, sentence-length variance, contraction injection, minor misspellings; (b) *tokenizer-level* — Unicode space substitution (Oct4Pie), glyph confusables; (c) *pivot-translation* — round-trip through Spanish or another language (POlLLOGAMER); (d) *behavior-level* — synthetic keystroke timing (ZyluxXD). Each targets a different layer of the detection pipeline.

7. **Persona-as-system-prompt.** The `f/awesome-chatgpt-prompts` "Act as a …" template is the dominant idiom for humanization-by-role-assignment: giving the model a specific human identity (poet, grandmother, cynical engineer) shifts cadence, vocabulary, and register more reliably than abstract "sound human" instructions.

8. **Programmatic optimization over manual prompting.** DSPy's thesis: humanlike phrasing emerges as a byproduct of optimizing against a quality metric on real examples, rather than from hand-crafting adjectives. Requires a metric, training data, and stable pipeline — not a drop-in tool.

9. **Grammar-constrained humanization.** Guidance and LMQL allow enforcing sentence-length distributions, contraction ratios, or register constraints via token-level steering. Under-explored for humanization specifically — most usage is structured-output.

10. **Persona portability across model families.** `BOBeirne/gemini-persona-prompts` provides the same persona in Claude XML, Gemini markdown, GPT markdown, Copilot, and Ollama formats — recognition that humanization prompts behave differently across models and need per-target adaptation.

## Notable Quotes

- From `blader/humanizer` README, quoting the Wikipedia *Signs of AI writing* source: *"LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."* — attribution: Wikipedia WikiProject AI Cleanup, cited by blader.

- From `SabrinaRamonov/prompts/humanize_ai_writing.md`: *"Act as an AI-writing humanizer. Your task is to take AI-generated content and rewrite it so that it reads as naturally and authentically human-written as possible. … Detect and eliminate any phrases or constructs that strongly indicate AI authorship (e.g., overuse of transitions like 'Furthermore,' or 'In conclusion,' or excessive use of passive voice)."* — attribution: Sabrina Ramonov.

- From `blader/humanizer` (after example): *"AI coding assistants can speed up the boring parts of the job. … The dangerous part is how confident the suggestions look. I've accepted code that compiled and passed lint, then discovered later it missed the point because I stopped paying attention."* — attribution: blader, illustrating target voice: first-person, specific, admits failure, no tricolons.

- From `f/awesome-chatgpt-prompts` README (self-description): *"The world's largest open-source prompt library for AI … Featured in Forbes, referenced by Harvard and Columbia, cited in 40+ academic papers."* — attribution: Fatih Kadir Akın (f).

- From `asgeirtj/system_prompts_leaks` README: *"Extracted system prompts from ChatGPT (GPT-5.4, GPT-5.3, Codex), Claude (Opus 4.6, Sonnet 4.6, Claude Code), Gemini (3.1 Pro, 3 Flash, CLI), Grok (4.2, 4), Perplexity, and more. Updated regularly."* — attribution: asgeirtj.

- From DSPy docs, as quoted in AgentPatterns.ai analysis: *"DSPy automatically optimizes how language model pipelines interact by searching the space of prompt instructions and few-shot demonstrations to maximize defined metrics."* — attribution: Stanford NLP / AgentPatterns paraphrase.

## Emerging Trends

- **Skills over scripts.** Humanization is shipping as Claude Code / OpenCode *skills* (`blader/humanizer`, `lguz/humanize-writing-skill`, `aaaronmiller/humanize-writing`) rather than standalone tools or web services. This is a 2025 shift and suggests the center of gravity is moving toward agent-integrated rewriting.

- **Wikipedia's "Signs of AI writing" as canonical reference.** Multiple independently authored repos now cite the same Wikipedia WikiProject AI Cleanup guide as the ground truth for what counts as an AI-ism. This is the closest thing the field has to a shared specification.

- **Voice calibration as the next frontier.** Generic humanization is saturating; personalized humanization (match *this specific* user's style from samples) is where newer releases (`blader/humanizer` v2.4) differentiate.

- **Detection arms race.** Detector-evasion repos and detector vendors are co-evolving; tokenizer-level attacks (Unicode spaces) are being countered by normalization, pushing evasion back toward text-level and behavior-level techniques.

- **System-prompt leaks as training material.** The two leak archives (53K★ combined) are increasingly cited as primary sources for how to structure tone, hedging, refusal language, and persona — effectively a corpus of "human-optimized" system prompts built by well-resourced labs.

- **Quantified humanization dials.** Early attempts (x1xhlol PR #50, Mohit1053) to expose preservation/creativity percentages as knobs hint at a future where humanization is configurable rather than monolithic, though no repo has published validation data on whether these dials behave as labeled.

## Open Questions / Gaps

1. **No shared benchmark.** Every repo claims effectiveness; none shares a standard eval set spanning multiple detectors (GPTZero, ZeroGPT, Copyleaks, Originality, Pangram, Turnitin), genres, and languages. Promptfoo is the natural host for this, but no public promptfoo config for humanization benchmarking was found.

2. **Humanization vs. quality trade-off.** Repos consistently warn against "dumbing down" (SabrinaRamonov) but don't measure semantic drift. How much meaning is actually preserved after a 3-pass rewrite is unclear.

3. **Cross-model generalization.** DSPy-optimized humanization prompts explicitly don't transfer; hand-written prompts presumably transfer unevenly. No systematic study found.

4. **Non-English coverage.** Nearly all blacklists and pattern libraries are English-centric. Non-English humanization tooling is largely absent from the open-source landscape.

5. **Evasion vs. genuine style.** The field has two subcultures — "make my essay pass Turnitin" and "make my AI assistant sound less like an AI" — that share techniques but have opposite ethics. Most repos don't pick a lane.

6. **Voice calibration evaluation.** `blader/humanizer`'s voice-match feature is intuitively powerful but has no reported accuracy data. How many sample paragraphs are enough? Does it capture voice or just surface tics?

7. **Guidance/LMQL underused for humanization.** Both frameworks could enforce humanization as constraints (contraction rate, sentence-length variance, banned-word grammar), but no significant open-source project found does this — a genuine gap.

8. **Persona-library duplication without versioning.** Persona collections (ai-personas, awesome-prompts, PersonaCraft, BOBeirne) overlap heavily without cross-referencing or quality signals. A curated, de-duplicated, version-pinned meta-library does not yet exist.

9. **Prompt-leak ethics and freshness.** Leak archives are valuable raw material but legally and ethically fraught, and leaked prompts go stale as models rev.

## References

- `github.com/blader/humanizer` — Claude Code humanizer skill, 29 patterns, voice calibration.
- `github.com/lguz/humanize-writing-skill` — 3-pass humanization skill.
- `github.com/aaaronmiller/humanize-writing` — humanization skill bundle with per-content-type guides.
- `github.com/SabrinaRamonov/prompts` — humanize_ai_text.md and humanize_ai_writing.md.
- `github.com/Mohit1053/Humanizer` — Ollama/Llama3 batch humanizer targeting GPTZero/ZeroGPT.
- `github.com/POlLLOGAMER/Humanizer-Prompt-Advanced` — translation round-trip humanizer.
- `github.com/x1xhlol/system-prompts-and-models-of-ai-tools` PR #50 — parameterized Humanizer AI Prompt.
- `github.com/Brandon689/best-ai-humanizer` — awesome list of hosted humanizers.
- `github.com/Oct4Pie/zero-zerogpt` — Unicode-space tokenizer attack.
- `github.com/jayyt12161/GPTZero-Bypasser` — Python rewriter for detector evasion.
- `github.com/ZyluxXD/zerobypass` — Playwright-based typing-behavior evasion.
- `github.com/friuns2/BlackFriday-GPTs-Prompts` — evade-ai-detectors jailbreak prompt.
- `github.com/f/awesome-chatgpt-prompts` (prompts.chat) — 160K★ persona/prompt library.
- `github.com/ai-boost/awesome-prompts` — curated GPT-Store prompts, framework-aware.
- `github.com/KudoAI/ai-personas` — LLM chatbot persona prompts.
- `github.com/Dantheman23-coder/AI-Persona-Prompts-Unleash-the-Power-of-Great-Minds` — PersonaCraft, 71 historical-figure personas.
- `github.com/BOBeirne/gemini-persona-prompts` — cross-model persona formats.
- `github.com/0xk1h0/ChatGPT_DAN` — DAN jailbreak/persona collection.
- `github.com/asgeirtj/system_prompts_leaks` — frontier-model system prompt archive (38.6K★).
- `github.com/jujumilk3/leaked-system-prompts` — second major leak archive (14.5K★).
- `github.com/dair-ai/Prompt-Engineering-Guide` — reference curriculum (73K★).
- `github.com/stanfordnlp/dspy` — programmatic prompt optimization.
- `github.com/promptfoo/promptfoo` — LLM eval / red-team framework (used for humanization benchmarking).
- `github.com/guidance-ai/guidance` — Microsoft template-based constrained generation.
- `lmql.ai` — declarative LLM query language with hard constraints.
- `docs.llamaindex.ai/.../chat_engine_personality` — LlamaIndex built-in persona templates.
- `en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing` — primary reference adopted by multiple humanizer repos.
