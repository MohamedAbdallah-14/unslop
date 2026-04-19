# Prompt Engineering for Humanization — Industry Blogs & Essays

## Executive Summary

**Research value: high.** Humanizing LLM output is a very active topic across industry engineering blogs, lab cookbooks, and individual essayists. The center of gravity has moved, over 2024–2026, from "clever one-shot prompts" toward three more structured artifacts:

1. **System-prompt-level style constraints** ("anti-slop" system prompts, personality presets). Lab cookbooks (OpenAI's *Prompt Personalities*, Anthropic's prompt library, the GPT-4.1 Prompting Guide) and practitioner posts (dev.to's *How to Fix That Robotic AI Tone*) converge on the same mechanism: put explicit, negative-constraint style rules in the system prompt, after the functional instructions, not in the user turn.
2. **Voice-specific style guides as reusable artifacts.** Every.to's AI Style Guide work and Gwern's system-prompts essay both argue that the prompt is not the unit of humanization — the *style guide* (voice, structure, signature moves, anti-patterns, examples) is. Prompts reference the guide; the guide is versioned.
3. **Writing samples + negative examples, not adjectives.** Simple few-shot fails (LessWrong's lsusr post; TinyStyler / TICL papers cited by HF). What works better: the writer's own samples, banned-phrase lists, and (per Every.to) paired good/bad lines.

Secondary themes: a near-unanimous "AI slop" vocabulary (em dashes, "delve," "It's important to note," "Certainly!", hedges, corporate verbs, rule-of-three lists), the mechanism being RLHF training toward verbose/helpful tone, and a quiet controversy — industry essayists disagree on whether LLMs *should* sound human when representing humans (Simon Willison refuses to let LLMs speak in his "I" voice at all; Every.to and lsusr treat it as a solvable personalization problem).

The biggest gap is empirical: nearly all guidance is craft-based, with very little public A/B data on what actually moves blind-rater humanness scores. Eugene Yan and Chip Huyen are the main voices pushing "evals before prompt engineering," but neither publishes a standard humanness eval.

## Sources

### 1. Simon Willison — "My current policy on AI writing for my blog"
- **URL:** https://simonwillison.net/2026/Mar/1/ai-writing/
- **Author/org:** Simon Willison (independent, ex-Django co-creator)
- **Year:** 2026
- **Core claim:** LLMs should not speak in a human author's first person. Humanization is not the goal; *authorship* is.
- **Techniques mentioned:** Hand-written opinion text; LLMs restricted to docs/READMEs; a proofreader prompt that flags spelling, grammar, weak arguments, logical errors, and broken links.
- **Practical takeaways:** Draw a bright line around "I"-pronoun and opinion text. Use LLMs for editorial hygiene (proofreading, alt text) rather than voice generation. Edit any LLM-generated prose to strip invented rationales like "this is designed to help."
- **Summary:** Willison's policy is the most-cited skeptical position in industry-essay discourse on humanization. He doesn't try to make Claude "sound like him" — he blocks it from that role entirely and keeps LLMs in a narrow utility lane. This frames humanization as an ethics-of-authorship question, not a prompt-engineering one.

### 2. Simon Willison — "Prompts I use" (Agentic Engineering Patterns)
- **URL:** https://simonwillison.net/guides/agentic-engineering-patterns/prompts/
- **Author/org:** Simon Willison
- **Year:** 2026
- **Core claim:** Reusable prompts should be published and versioned as artifacts, not rewritten per-session.
- **Techniques mentioned:** Proofreader prompt; alt-text prompt; artifact prompt (specifies plain HTML, vanilla JS, Helvetica, two-space indents, sentence-case headings).
- **Practical takeaways:** Treat style and format constraints as a standing prompt file. Customization ("Helvetica", "sentence case") is more effective than asking for "a clean look."
- **Summary:** A concrete example of the "style guide is not a prompt" principle in an individual's workflow — Willison externalizes constraints so they can be reused and audited.

### 3. Eugene Yan — "Prompting Fundamentals and How to Apply Them Effectively"
- **URL:** https://eugeneyan.com/writing/prompting/
- **Author/org:** Eugene Yan (Amazon / independent)
- **Year:** 2024
- **Core claim:** Prompts condition a probabilistic model; assigning a role is a high-leverage lever on tone and style, but evals must come first.
- **Techniques mentioned:** Role assignment ("You are a preschool teacher" vs. "You are an NLP professor"); structured I/O; n-shot prompting; chain-of-thought; prefilling; reducing hallucinations.
- **Practical takeaways:** Before humanizing, label ~100 examples and build a reliable eval. Otherwise, tone improvements are vibes, not signal. Treat "think step by step" and role-assignment as starting points, not magic spells.
- **Summary:** Yan's piece is the closest thing in industry essays to a methodology for humanization: specify voice via role, then *measure* whether rewrites actually improve perceived quality. His influence appears downstream in Chip Huyen's AI Engineering book and in OpenAI's Cookbook framing of personalities as an "operational lever."

### 4. Eugene Yan — "Patterns for Building LLM-based Systems & Products"
- **URL:** https://eugeneyan.com/writing/llm-patterns
- **Author/org:** Eugene Yan
- **Year:** 2023
- **Core claim:** Seven production patterns (evals, RAG, fine-tuning, caching, guardrails, defensive UX, user feedback) define the LLM product surface.
- **Techniques mentioned:** Guardrails for output quality; defensive UX to manage robotic / failure output; user-feedback flywheel to detect tone regressions.
- **Practical takeaways:** Humanization is an output-quality problem that should be wrapped by guardrails and UX — not just a prompt rewrite. Collect post-hoc user feedback as a humanness signal.
- **Summary:** Yan's framework is the reason later blogs (e.g., dev.to's Alan West) treat "robotic tone" as an engineering regression to be caught in CI, not a one-time prompt tweak.

### 5. Gwern — "Writing for LLMs So They Listen"
- **URL:** https://gwern.net/llm-writing
- **Author/org:** Gwern Branwen
- **Year:** 2024
- **Core claim:** LLMs are now part of the reader base; write personal, idiosyncratic, autobiographical content, because generic empirical facts are already commoditized.
- **Techniques mentioned:** Prioritize unique perspective; accessibility (no paywalls, no JS traps, no robots.txt bans) so content enters training data.
- **Practical takeaways:** For *authors*, humanity is the training signal — oddities, obsessions, everyday incidents. For *prompt engineers*, the corollary is: the material a model needs to sound like a specific person is autobiographical, not topical.
- **Summary:** Inverts the usual framing. Instead of asking how to make AI sound human, Gwern asks what humans should write so AIs can learn humanness from them.

### 6. Gwern — "Some 2025 LLM System Prompts"
- **URL:** https://gwern.net/system-prompts-2025
- **Author/org:** Gwern + GPT-5 Pro, Gemini-3-pro-preview, Claude-4.5-opus (co-authored)
- **Year:** 2025
- **Core claim:** A well-constructed system prompt should encode voice via explicit rules: concise/direct, declarative, calibrated uncertainty vocabulary, neutral evaluation, and citation format.
- **Techniques mentioned:** Probability-word ladder (*unlikely, plausible, probable, very probable, almost certain*); `[Surname Year](URL "Title")` citation format; declarative assertions over question-dodging; creative-writing carve-out that re-enables "vividness, narrative flow, and sensory imagery."
- **Practical takeaways:** The style contract is multi-section: assertion style, uncertainty, citation, formatting, plus explicit mode-switching (analytical vs. creative). Calibrated hedging is itself a humanization move — vague "might/perhaps" reads as AI slop, graded probabilities read as a thoughtful human.
- **Summary:** A dense, opinionated worked example of what a voice-carrying system prompt looks like in 2025. Notable for treating uncertainty language as a style axis, not a correctness axis.

### 7. Gwern — "Towards Better LLM Creative Writing"
- **URL:** https://gwern.net/blog/2025/better-llm-writing
- **Author/org:** Gwern
- **Year:** 2025
- **Core claim:** LLM creative writing is boxed in by RLHF-trained helpfulness; unlocking it requires instructions that override the "safe, balanced" default.
- **Techniques mentioned:** Relaxing conciseness constraints for creative mode; leaning on vividness, narrative flow, sensory imagery.
- **Practical takeaways:** Humanization constraints are domain-specific — what reads as human in an essay (tight, opinionated) differs from fiction (sensory, textured). One system prompt cannot carry both.
- **Summary:** Argues against a unified "human voice" system prompt and for mode-specific overrides.

### 8. Every.to / Katie Parrott — "AI Style Guides: How to Help AI Write Like You"
- **URL:** https://every.to/guides/ai-style-guide
- **Author/org:** Katie Parrott + Claude (credited), Every Inc.
- **Year:** 2025
- **Core claim:** A style guide (not a prompt) is the durable artifact that humanizes AI output. It should be concrete: voice, structure, sentence-level preferences, signature moves, anti-patterns, examples, revision checklist.
- **Techniques mentioned:** Voice rules (e.g., "write from inside the transformation, not above it"); named structural templates (Discovery Arc, Technical Deep-Dive, Workshop Report); paired good/bad concrete examples ("Claude spun up five PRs while I drank coffee" vs. "optimized workflows"); "red flag" anti-pattern tables (hedges, correlative constructions, rhetorical filler questions, meandering intros); pre-publication checklists.
- **Practical takeaways:** Write the anti-patterns section first — it's the highest-leverage part. Pair every rule with at least one positive and one negative example. Distinguish the style guide (reusable system) from the prompt (per-task invocation).
- **Summary:** The most complete industry treatment of humanization as an authoring-system problem. Every.to treats this as production tooling: their columnists' guides feed Spiral, their internal AI writing tool, daily. This is likely the single highest-value source in this digest.

### 9. Every.to — "The Science of Why AI Still Can't Write Like You"
- **URL:** https://every.to/p/the-science-of-why-ai-still-can-t-write-like-you
- **Author/org:** Every Inc.
- **Year:** 2025
- **Core claim:** LLMs' default is "the mean writer"; they converge toward the center of their training distribution and away from any specific voice.
- **Techniques mentioned:** Style guides; writer samples; negative examples to counter default-mean drift.
- **Practical takeaways:** Without explicit counter-pressure, models will regress to generic — not because prompting is weak, but because RLHF actively rewards the mean.
- **Summary:** The mechanism essay that motivates Every.to's style-guide work. Frames humanization as counter-gradient engineering.

### 10. OpenAI Cookbook — "Prompt Personalities" (Mandeep Singh, Kathy Lau)
- **URL:** https://cookbook.openai.com/examples/gpt-5/prompt_personalities
- **Author/org:** OpenAI
- **Year:** 2026 (Jan)
- **Core claim:** Personality is an "operational lever" that improves consistency, reduces drift, and aligns model behavior — not aesthetic polish. Four worked presets: Professional, Efficient, Fact-Based, Exploratory.
- **Techniques mentioned:** System-prompt-level personality definition; explicit negative constraints ("Do not use emojis, greetings, closing remarks"); explicit carve-out so personality doesn't override artifact formats (emails, JSON, code); grounded/hedged language for the Fact-Based preset ("based on the provided context...").
- **Practical takeaways:** Keep personalities scoped to *how* the agent responds, not *what* it must do. Start minimal, validate with evals, evolve deliberately. Don't force personality onto generated artifacts.
- **Summary:** The clearest official OpenAI statement that personality = production lever. Treats humanization as one end of a spectrum that also includes "efficient" (cold, terse) and "fact-based" (plainspoken, grounded) — implying there is no single "human" tone.

### 11. OpenAI Cookbook — "GPT-4.1 Prompting Guide"
- **URL:** https://cookbook.openai.com/examples/gpt4-1_prompting_guide/
- **Author/org:** OpenAI
- **Year:** 2025
- **Core claim:** GPT-4.1 follows instructions more literally; single-sentence style steering is usually sufficient if it is firm and unequivocal.
- **Techniques mentioned:** Agent "reminders" (persistence, tool-calling, planning); literal-instruction prompting; the observation that instructions increased internal SWE-bench Verified by ~20%.
- **Practical takeaways:** For style, don't hedge the prompt itself ("please try to sound natural"). Write it as a definitive rule ("Do not open with filler phrases"). Literalism cuts both ways.
- **Summary:** Provides the mechanical foundation under which "anti-slop" system prompts work: newer models will obey specific style bans if stated unambiguously.

### 12. Anthropic — Prompt Library
- **URL:** https://docs.anthropic.com/en/prompt-library/library
- **Author/org:** Anthropic
- **Year:** 2024–2026
- **Core claim:** A single-sentence role statement in the system prompt is often enough to focus Claude's behavior *and* tone.
- **Techniques mentioned:** Named tone presets — "Hal the humorous helper," "Pun-dit," "Code consultant," "Ethical dilemma navigator," "Meeting scribe"; role-setting for tone ("You are a helpful coding assistant specializing in...").
- **Practical takeaways:** Role + domain is often enough for tone. For humanization specifically, the library's playful presets (Pun-dit, Hal) show how far a light-touch system-prompt tone can travel.
- **Summary:** Anthropic's official catalogue of system-prompt personas. Demonstrates a portfolio of tones rather than one "human" setting.

### 13. Vox (Sigal Samuel) — "Claude has an 80-page constitution. Is that enough to make it good?" (on Amanda Askell)
- **URL:** https://vox.com/future-perfect/476614/ai-claude-constitution-soul-amanda-askell
- **Author/org:** Vox / Amanda Askell (Anthropic)
- **Year:** 2026
- **Core claim:** Claude's "soul" is a ~30,000-word / 100+ page document that cultivates *character traits* (honesty, charitability, phronesis) rather than imposing rigid rules.
- **Techniques mentioned:** Virtue-ethics framing; extended system-prompt / constitutional document rather than short rules; treating the model as an entity to be cultivated.
- **Practical takeaways:** At the frontier-lab scale, humanization is being handled as long-form character instruction — dozens of pages of judgment cases — not as a prompt. This bleeds into public-facing Claude's warmth and the specific ways it hedges and reflects.
- **Summary:** Shows the scale at which labs have moved past "you are a helpful assistant." It also implies a ceiling for user-side humanization: the model already has an enormous character prompt you are writing on top of.

### 14. dev.to (Alan West) — "How to Fix That Robotic AI Tone in Your LLM-Powered Features"
- **URL:** https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e
- **Author/org:** Alan West, DEV Community
- **Year:** 2025
- **Core claim:** Robotic tone is not a model problem or a fine-tuning problem — it's a missing system prompt.
- **Techniques mentioned:** "Anti-slop" system prompt (ban "Certainly!", "delve," "leverage," hedges, sycophantic closers); put style constraints *after* functional instructions; use temperature ~0.7 for natural variation; CI regex check for slop patterns; references the `talk-normal` GitHub project.
- **Practical takeaways:** Works across GPT-4o, Claude, Llama 3. Customize aggressiveness by audience (developer tools = strict; customer chatbot = warmer). Keep a banned-words list as a monitoring layer, not a replacement.
- **Summary:** The best concrete "ship it" walkthrough. Treats humanization as an engineering discipline with prompts, tests, and regression monitoring.

### 15. LessWrong / lsusr — "I finally got ChatGPT to sound like me"
- **URL:** https://www.lesswrong.com/posts/2d5o75nmTpLiSP4WL/i-finally-got-chatgpt-to-sound-like-me
- **Author/org:** lsusr, LessWrong
- **Year:** 2024
- **Core claim:** Asking a model to "write like X" yields 10% X + 90% generic, because of regression-to-the-mean. The counter-technique is *amplification prompting*: ask the model to write an exaggerated parody of X, "more X than X."
- **Techniques mentioned:** Amplification ("multiply lsusr in vector space by 10×"); building the voice profile by first having the model articulate what makes the author distinct; accepting that full ghostwriting is out of reach and aiming for satire-grade.
- **Practical takeaways:** Push the tone further than you want it; the default-mean pull will bring it back. Use the model's own self-description of the author as scaffolding.
- **Summary:** Most influential individual-author humanization technique in the essayist community. The "ask for satire" trick keeps showing up in downstream Substack / Medium posts.

### 16. Chip Huyen — *AI Engineering*, Ch. 5 ("Prompt Engineering") + blog
- **URL:** https://huyenchip.com/blog/ ; book: *AI Engineering* (O'Reilly 2025)
- **Author/org:** Chip Huyen
- **Year:** 2025
- **Core claim:** Prompt engineering is a systematic ML experiment — anatomy (task input, examples, task description), order effects, persona assignment, iteration under standardized eval.
- **Techniques mentioned:** System vs. user prompt split (global task/role/tone vs. specific instruction); persona assignment; structured output; chain-of-thought; chat template fidelity ("even extra newlines can cause dramatic output changes").
- **Practical takeaways:** Before any humanization work, separate "global tone" (system) from "per-request task" (user). Model-specific order effects matter (GPT-4 prefers task description first; Llama 3 may prefer it last).
- **Summary:** The most rigorous methodological framing. Aligns with Yan but goes deeper on chat-template mechanics.

### 17. Hugging Face blog (airabbitX) — "How to get GPT to talk like a consultant"
- **URL:** https://huggingface.co/blog/airabbitX/how-to-get-gpt-to-talk-like-a-consultant
- **Author/org:** HF community
- **Year:** 2024
- **Core claim:** Truly human conversational behavior (asking clarifying questions before answering) needs supervised fine-tuning on small curated datasets, not prompting alone.
- **Techniques mentioned:** Small ChatGPT-generated datasets; LLaMA-Factory fine-tuning; SFT toward "ask before answering" behavior; DPO/preference tuning as alignment follow-up.
- **Practical takeaways:** Some humanization behaviors (conversational pacing, reciprocity) don't reliably survive at the prompt layer. Fine-tuning is warranted when you need the model to *withhold* an immediate answer.
- **Summary:** The minority-position counter to "it's all in the system prompt." Useful as a boundary case: for reactive tone, prompts are enough; for proactive dialog shape, fine-tune.

### 18. The Humanizers (Substack) — "10 Easy Prompt Fixes that Humanize AI in Seconds"
- **URL:** https://thehumanizers.substack.com/p/10-easy-prompt-fixes-to-erase-the
- **Author/org:** The Humanizers
- **Year:** 2025
- **Core claim:** A compact ten-rule rewrite prompt can meaningfully de-AI-ify a draft.
- **Techniques mentioned:** "Less reasonable, more decisive"; shorten for punch; strip SaaS verbs (*seamless*, *unlock*, *powerful*, *elevate*); cut diplomatic hedges (*might*, *perhaps*, *often*); reduce polish by 10–15%; add one personal/quirky line.
- **Practical takeaways:** Treat the rewrite as *asymmetric* — subtract polish, subtract hedges, add specificity + one human oddity.
- **Summary:** A tight, practitioner-ready humanization prompt list. Converges closely with Every.to's anti-patterns but compressed to a handful of moves.

### 19. Ruben Hassid (Substack / notes) — Anti-AI Voice Editor prompts
- **URL:** https://substack.com/@ruben/note/c-181376166 and related notes
- **Author/org:** Ruben Hassid
- **Year:** 2025
- **Core claim:** Long "please sound human" prompts underperform a short instruction that references a standing anti-AI-pattern file.
- **Techniques mentioned:** "Anti-AI writing style file" (reusable); 29-word master prompt ("Read my anti-AI writing style file first. It contains every known pattern of AI writing I want to avoid. Apply these as rules to everything you write for me."); "Act as my Anti-AI-Voice Editor" rewrite persona; using Wikipedia's *Signs of AI writing* article as a seed document.
- **Practical takeaways:** Externalize the pattern list once; keep the in-line prompt short. Positive-only prompts fail; pattern bans work.
- **Summary:** The most widely shared practitioner workflow — a memorable formulation of Every.to's "guide, not prompt" principle at individual-user scale.

### 20. Towards AI (Louis-François Bouchard) — "How to Spot and Remove 'AI Slop' from Your Writing"
- **URL:** https://pub.towardsai.net/how-to-spot-and-remove-ai-slop-from-your-writing-73bd12b423ef
- **Author/org:** Louis-François Bouchard / Towards AI
- **Year:** 2026
- **Core claim:** "AI slop" has a stable signature (em dashes; "delve," "tapestry," "game-changing," "leverage," "unlock," "robust," "seamless"; false casual transitions like "Meanwhile..."; weak rhetorical questions; clichés like "the million-dollar question"; hyperbolic tech metaphors).
- **Techniques mentioned:** Signature-based detection; explicit bans as rewrite prompts.
- **Practical takeaways:** Maintain a slop lexicon and ban it in the system prompt *and* post-process for escapes.
- **Summary:** The most cited "what AI slop actually is" reference in 2026 essay discourse. Useful as an anti-pattern seed list.

### 21. LangChain docs — ChatPromptTemplate and message roles
- **URL:** https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.HumanMessagePromptTemplate.html
- **Author/org:** LangChain
- **Year:** 2024–2026
- **Core claim:** Structuring prompts as SystemMessage / HumanMessage / AIMessage + MessagesPlaceholder creates humanized multi-turn flow that a single PromptTemplate cannot.
- **Techniques mentioned:** ChatPromptTemplate; role-typed messages; MessagesPlaceholder for conversation history injection.
- **Practical takeaways:** For conversational humanization, the first structural choice is message-role modeling, not word choice. A chatbot without a rolling-history placeholder will feel robotic regardless of tone prompt.
- **Summary:** Framework-level scaffolding. Less about word-level tone, more about conversational presence.

## Key Techniques / Patterns

Grouped by the lever they pull, with the consensus they have across the sources above.

### A. System-prompt-level anti-slop constraints
Consensus lever. Appears in OpenAI's *Prompt Personalities* (source 10), Anthropic's Prompt Library (12), dev.to / Alan West (14), Ruben Hassid (19), Towards AI (20), and The Humanizers (18).

- **Ban specific openers:** "Certainly," "Great question," "Absolutely."
- **Ban specific verbs/adjectives:** *delve, utilize, leverage, streamline, unleash, robust, game-changer, seamless, elevate, unlock.*
- **Ban specific connective phrases:** "It's important to note," "It's worth mentioning," "At the end of the day," "In today's fast-paced world."
- **Ban sycophantic closers:** "Hope this helps," "Let me know if you need anything else."
- **Punctuation rules:** em dashes (—) called out as the single strongest AI tell; replacements are commas, periods, parens, semicolons.
- **Placement:** put style constraints *after* functional instructions (dev.to 14, reinforced by GPT-4.1 literalism principles in source 11).

### B. Voice-identity scaffolding
- **Role assignment** (Yan 3, Huyen 16, Anthropic 12): "You are a preschool teacher" / "You are an NLP professor" / "You are a customer support chatbot." Conditions tone and lexical register in one line.
- **Four-element voice identity** (from the ChatGPT-Undetected piece, repeated in The Humanizers 18): voice identity + relationship context + style constraints + a real writing sample.
- **Amplification prompting** (lsusr 15): "Write like X but more X than X" — counters regression-to-the-mean.

### C. Style guide as reusable artifact
Most structured version: Every.to's AI Style Guide (source 8). Lightweight versions: Ruben Hassid's anti-AI file (19), Willison's published prompts (2), Gwern's system prompt (6).

Canonical sections (Every.to):
1. Voice / tone (with rules, not adjectives).
2. Structure (named arcs like Discovery Arc, Technical Deep-Dive).
3. Sentence-level preferences (short vs. long, punctuation, rhythm) with paired concrete/abstract examples.
4. Signature moves (e.g., "The Borrowed Lens," "The One Big Idea").
5. Anti-patterns (a red-flag table with hedges, correlative constructions, saggy conclusions).
6. Positive + negative examples.
7. Revision checklist.

### D. Writing samples + few-shot
Consensus: few-shot with samples beats adjectives (Every.to 8, Huyen 16, The Humanizers 18). Consensus caveat: simple few-shot alone underperforms (HF/TinyStyler literature; TICL) — pair with negative examples or authorship embeddings for subtle voice.

### E. Calibrated uncertainty vocabulary
Gwern 6: replace "might/perhaps" with a graded ladder — *unlikely, plausible, probable, very probable, almost certain.* Reads as a thoughtful human rather than a hedging AI.

### F. Varied sentence rhythm + embodied concreteness
Cross-cutting. Every.to (8) gives embodied-specificity examples ("the relief felt as physical as the dread had been"). Dev.to (14) calls for short sentences. The Humanizers (18) mandates rhythm variation.

### G. Guardrails + CI regression tests
Eugene Yan (4) and dev.to (14): treat slop like a code regression. Maintain a banned-words list; fail CI on detection; log escapes to strengthen the system prompt over time.

### H. Conversational pacing beyond tone
HF / LLaMA consultant piece (17): make the model *ask clarifying questions* before answering — a dialogue pattern, not a word choice. Often requires SFT, not just prompting. LangChain (21) provides the structural substrate (MessagesPlaceholder for history).

### I. Mode-specific overrides
Gwern (7): what reads as human differs by mode (essay vs. fiction). Don't ship one universal "human" prompt.

## Notable Quotes

> "My current policy on this is that if text expresses opinions or has 'I' pronouns attached to it then it's written by me. I don't let LLMs speak for me in this way." — Simon Willison, *My current policy on AI writing for my blog* (2026)

> "Nobody talks like that. No human being has ever delved into anything during a casual conversation." — Alan West, *How to Fix That Robotic AI Tone in Your LLM-Powered Features* (dev.to, 2025)

> "When I tell ChatGPT to 'write like lsusr', it writes [a] blog post that's 10% me and 90% generic drivel. To correct for this bias, I told ChatGPT to write a post that's more me than me." — lsusr, *I finally got ChatGPT to sound like me* (LessWrong, 2024)

> "Personality should not be treated as aesthetic polish, but as an operational lever that improves consistency, reduces drift, and aligns model behavior with user expectations and business constraints." — Mandeep Singh & Kathy Lau, *Prompt Personalities* (OpenAI Cookbook, 2026)

> "A style guide is not a prompt. A prompt tells AI what to do: Draft an essay, revise a paragraph, or tighten an intro. A style guide is the reusable system underneath telling AI how to sound like you while doing it." — Katie Parrott, *AI Style Guides* (Every.to, 2025)

> "A model is perfectly consistent from the start — that's why it sounds like nobody. The challenge is to push it toward the idiosyncrasies that make writing belong to a particular person." — Katie Parrott, *AI Style Guides* (Every.to, 2025)

> "Distinguish fact from guesswork using probability terms like *unlikely, plausible, probable, very probable,* and *almost certain.*" — Gwern, *Some 2025 LLM System Prompts*

> "Read my anti-AI writing style file first. It contains every known pattern of AI writing I want to avoid. Apply these as rules to everything you write for me." — Ruben Hassid (Substack, 2025) — the full 29-word "master" humanization prompt.

> "GPT-4.1 is highly steerable and responsive to well-specified prompts — if model behavior is different from what you expect, a single sentence firmly and unequivocally clarifying your desired behavior is almost always sufficient to steer the model on course." — OpenAI, *GPT-4.1 Prompting Guide* (2025)

> "Don't just tell the model what good writing looks like. Tell it what bad writing looks like, too." — Katie Parrott, *AI Style Guides* (Every.to, 2025) — on why the anti-patterns section is the highest-leverage part of a style guide.

## Emerging Trends

1. **Anti-slop system prompts are becoming a standard product concern.** Open-source projects like `talk-normal` (referenced by dev.to 14) and the convergence of OpenAI / Anthropic / community guidance toward banned-word system prompts suggest 2026 is the year "don't sound like AI" became a shipped constraint rather than a user-side rewrite step.
2. **Style guides are displacing prompts as the primary artifact of humanization.** Every.to (8), Willison (2), Gwern (6), and Hassid (19) all describe workflows where the in-line prompt is short and references a long, versioned guide/file. This mirrors the move from "prompt engineering" to "context engineering" more broadly.
3. **Personality portfolios, not a single "human" setting.** OpenAI's *Prompt Personalities* (10) and Anthropic's Prompt Library (12) both ship *multiple* presets (Professional / Efficient / Fact-Based / Exploratory; Pun-dit / Hal / Code consultant / Ethical dilemma navigator). The trend is toward a matrix of humanlike tones selected per workload.
4. **Character-scale system prompts at the frontier.** Anthropic's 30,000-word "soul" document (Askell, source 13) and rumored / leaked 1,000-line Claude system prompts signal that the humanization work is migrating upstream, into the base persona the labs ship. Downstream prompt engineers are increasingly *editing on top of* a strong default voice.
5. **Engineering discipline around tone regressions.** CI checks for slop patterns (dev.to 14), evals-first prompting (Yan 3, Huyen 16), and user-feedback flywheels (Yan 4) are turning "sounds human" into a testable, monitorable property.
6. **Calibrated uncertainty as a humanness signal.** Gwern's probability-ladder prescription (6) is being echoed in "less hedging, more specific claims" advice across practitioner posts (18, 19). This reframes humanization partly as an epistemics problem.
7. **Amplification / "parody" prompting persists as folk wisdom** for voice replication (lsusr 15) despite its weaknesses (Every.to calls this "asking for the mean"). It will likely be replaced by authorship-embedding and TinyStyler-type approaches as those mature into products.

## Open Questions / Gaps

- **No public benchmark for "humanness."** No industry essayist publishes a standard eval for whether a rewrite is more human to blind raters. Eugene Yan and Chip Huyen strongly recommend evals; neither provides one specific to tone. This is the single largest gap.
- **Are "AI detectors" measuring anything real?** Practitioner posts (especially dev.to 14, Towards AI 20) reference users running outputs through "is this AI" detectors, but no engineering blog publishes a principled analysis of whether those detectors correlate with reader trust / engagement.
- **Does RLHF-for-helpfulness inherently fight humanization?** Alan West (14), Every.to (9), and the lsusr post (15) all diagnose AI slop as a byproduct of RLHF's reward function — but no one publicly proposes a training-level fix besides fine-tuning on style-specific data (HF 17).
- **When is fine-tuning actually warranted?** HF's consultant piece (17) claims some behaviors (asking clarifying questions first) don't survive prompt-only humanization. The boundary between "just a system prompt" and "needs SFT" is unmapped.
- **Does humanization generalize across models?** Dev.to (14) reports its anti-slop prompt works across GPT-4o / Claude / Llama 3. Huyen (16) warns about order effects and chat-template fragility. No one has published a cross-model replication study.
- **Ethics of ghostwriting someone's "I".** Willison (1) draws a hard line; Every.to (8), lsusr (15), and Hassid (19) assume style cloning is fine. The industry-essay discourse has not resolved this, and it's likely to intensify as personal AI style guides become productized.
- **Humanization vs. authenticity.** Several sources (Towards AI 20, The Humanizers 18) treat adding a "personal quirky line" as a *technique*. Is an injected quirk still humanization if it's formulaic? The aesthetic question is open.
- **Long-context style drift.** Chip Huyen (16) flags chat-template / order sensitivity, but no public analysis exists on whether a carefully crafted voice prompt decays across 20+ turn conversations.
- **Multilingual humanization.** All the sources here focus on English. The anti-slop vocabulary ("delve," "leverage") is English-specific; whether parallel slop signatures exist in other languages is unaddressed in industry blogs.

## References

1. Simon Willison, "My current policy on AI writing for my blog" (2026) — https://simonwillison.net/2026/Mar/1/ai-writing/
2. Simon Willison, "Prompts I use" (Agentic Engineering Patterns, 2026) — https://simonwillison.net/guides/agentic-engineering-patterns/prompts/
3. Eugene Yan, "Prompting Fundamentals and How to Apply Them Effectively" (2024) — https://eugeneyan.com/writing/prompting/
4. Eugene Yan, "Patterns for Building LLM-based Systems & Products" (2023) — https://eugeneyan.com/writing/llm-patterns
5. Gwern, "Writing for LLMs So They Listen" (2024) — https://gwern.net/llm-writing
6. Gwern et al., "Some 2025 LLM System Prompts" (2025) — https://gwern.net/system-prompts-2025
7. Gwern, "Towards Better LLM Creative Writing" (2025) — https://gwern.net/blog/2025/better-llm-writing
8. Katie Parrott (Every.to), "AI Style Guides: How to Help AI Write Like You" (2025) — https://every.to/guides/ai-style-guide
9. Every.to, "The Science of Why AI Still Can't Write Like You" (2025) — https://every.to/p/the-science-of-why-ai-still-can-t-write-like-you
10. Mandeep Singh & Kathy Lau (OpenAI), "Prompt Personalities" Cookbook (Jan 2026) — https://cookbook.openai.com/examples/gpt-5/prompt_personalities
11. OpenAI, "GPT-4.1 Prompting Guide" (2025) — https://cookbook.openai.com/examples/gpt4-1_prompting_guide/
12. Anthropic, Prompt Library (2024–2026) — https://docs.anthropic.com/en/prompt-library/library
13. Sigal Samuel / Amanda Askell, "Claude has an 80-page constitution" (Vox, 2026) — https://vox.com/future-perfect/476614/ai-claude-constitution-soul-amanda-askell
14. Alan West, "How to Fix That Robotic AI Tone in Your LLM-Powered Features" (dev.to, 2025) — https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e
15. lsusr, "I finally got ChatGPT to sound like me" (LessWrong, 2024) — https://www.lesswrong.com/posts/2d5o75nmTpLiSP4WL/i-finally-got-chatgpt-to-sound-like-me
16. Chip Huyen, *AI Engineering* Ch. 5 "Prompt Engineering" (O'Reilly, 2025) — https://huyenchip.com/blog/
17. airabbitX (HF Blog), "How to get GPT to talk like a consultant" (2024) — https://huggingface.co/blog/airabbitX/how-to-get-gpt-to-talk-like-a-consultant
18. The Humanizers, "10 Easy Prompt Fixes that Humanize AI in Seconds" (Substack, 2025) — https://thehumanizers.substack.com/p/10-easy-prompt-fixes-to-erase-the
19. Ruben Hassid, Anti-AI Voice Editor notes (Substack, 2025) — https://substack.com/@ruben/note/c-181376166
20. Louis-François Bouchard, "How to Spot and Remove 'AI Slop' from Your Writing" (Towards AI, 2026) — https://pub.towardsai.net/how-to-spot-and-remove-ai-slop-from-your-writing-73bd12b423ef
21. LangChain docs, ChatPromptTemplate and message roles — https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.HumanMessagePromptTemplate.html
