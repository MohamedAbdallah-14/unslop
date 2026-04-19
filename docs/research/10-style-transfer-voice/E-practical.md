# Style Transfer & Voice — Practical How-Tos & Forums

**Category:** 10 — Style Transfer & Voice
**Angle:** E — Practical How-Tos & Forums (Reddit, HN, Substack, YouTube, creator blogs)
**Purpose:** Document the practitioner canon for "make the AI write in my voice" — the prompts, workflows, and pain points actually being shared in public.

**Research value: high** — Dense, convergent practitioner advice across Reddit, HN, Substack, LessWrong, creator blogs, and YouTube. Named patterns (Voice DNA, hyperbolic trick, voice file / .md), recurring prompt templates, and a strong skeptic counter-current are all visible.

---

## Curated Posts (20+)

### 1. r/ArtificialIntelligence — "How do you keep your AI from overwriting your tone?"
- **URL:** https://www.reddit.com/r/ArtificialInteligence/comments/1ourafh/
- **Community / date:** r/ArtificialIntelligence, late 2025
- **Summary:** OP complains that even with very specific tone instructions (sarcastic, poetic, dark), the model initially follows and then "slowly morphs back into that clean, 'neutral' AI voice." Commenters treat this as a universal complaint that spans creative writing, roleplay, dialogue sims, and personality-driven chatbots.
- **Key quote:** "Voice is multidimensional and AI defaults to predictable, generic patterns."

### 2. r/ChatGPT — "Stop fighting ChatGPT's personality — just override it from your own machine"
- **URL:** https://www.reddit.com/r/ChatGPT/comments/1rdbi9s/
- **Community / date:** r/ChatGPT, late 2025
- **Summary:** High-upvote argument that Custom Instructions "decay after ~10 messages," memory is unreliable, and model updates reset personality. Fix: keep rules, history, and context as Markdown on your own machine, inject fresh each session.
- **Pattern:** Distrust of built-in personalization; push toward client-side voice files.

### 3. r/ChatGPT — "I'll Build You a Custom GPT (Any Personality, Any Purpose) — Free"
- **URL:** https://www.reddit.com/r/ChatGPT/comments/1molg68/
- **Community / date:** r/ChatGPT, 2025
- **Summary:** Community service-post building custom GPTs / system prompts that "sound more like you," framed around locking tone across tools to prevent "AI drift."

### 4. r/ChatGPT — "Anyone found a custom instruction that fully or partly negates the new suck-up responses?"
- **URL:** https://www.reddit.com/r/ChatGPT/comments/1k9686o/
- **Community / date:** r/ChatGPT, 2025
- **Summary:** Users swap anti-sycophancy / anti-filler custom instructions. Reveals that "writing in my voice" often really means "strip the default assistant voice."

### 5. r/ChatGPT — "I want a damn Australian voice for chatgpt"
- **URL:** https://www.reddit.com/r/ChatGPT/comments/1n5qa8f/
- **Community / date:** r/ChatGPT, 2025
- **Summary:** Cultural/geographic tone mismatch thread — users want regional voice, not just "personality." Shows demand for dialect-level style control, not just formality knobs.

### 6. r/AIBranding — "Brand voice with AI: how much human edit do you do?"
- **URL:** https://www.reddit.com/r/AIBranding/comments/1nwsv4a/
- **Community / date:** r/AIBranding, 2025
- **Summary:** Consensus: AI gets ~60–70% of the way structurally, but brand voice still needs human editing. Explicit style-guide-in-prompt (tone, vocabulary, dos/don'ts, humor policy) is the most-cited lever; ~85% of respondents edit before publishing.

### 7. r/AIWritingHub — "How do I rewrite AI text to make it sound real?"
- **URL:** https://www.reddit.com/r/AIWritingHub/comments/1ohxyka/
- **Community / date:** r/AIWritingHub, 2025
- **Summary:** Practitioners share rewrite heuristics: shorten sentences, kill em-dashes, cut "not X — but Y" parallelism, replace nominalizations with verbs, vary sentence length.

### 8. r/LocalLLaMA — "Vellium: open-source desktop app for creative writing with visual controls"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1r89a4y/
- **Community / date:** r/LocalLLaMA, late 2025
- **Summary:** Shift from prompt editing to slider-style controls (Mood, Pacing, Intensity, Dialogue Style, Descriptiveness, POV, Creativity, Tension, Detail, Dialogue Share) for local models via Ollama/LM Studio. Signals that pure few-shot style prompting is being wrapped by higher-level UX.

### 9. HN 39452331 — "A solution to personalize ChatGPT writing style" (Show HN)
- **URL:** https://news.ycombinator.com/item?id=39452331
- **Date:** Feb 2024
- **Summary:** OP: "Whenever I use ChatGPT to write or draft content, the output often doesn't align with my personality, feeling as though it's been crafted by someone else, way more hyperbolic and extraverted." Built a tool to configure writing style.

### 10. HN 47291513 — "LLM Writing Tropes.md"
- **URL:** https://news.ycombinator.com/item?id=47291513
- **Date:** 2025
- **Summary:** Long thread on a community-maintained list of AI writing tells. Key practitioner insights: (a) telling the model "don't use delve" can *increase* delve usage because of priming ("Streisand effect for prompts"); (b) "positive shape" instructions (describe what good writing looks like) beat "avoid this" lists; (c) style transfer via "write in the style of <named author>" activates different linguistic patterns and feels less generic; (d) separate "editor agent" that post-processes for tropes works better than inline constraints.
- **Key quote:** "I have more success telling the LLM to write in the style of a particular author I like. It seems to activate different linguistic patterns and feel less generic. Then, I make an 'editor agent' comb through, looking for tropes and rewording them."

### 11. HN 44293455 — "Writing in the Age of LLMs"
- **URL:** https://news.ycombinator.com/item?id=44293455
- **Summary:** Debate over whether cleaning up AI tropes to sound human is legitimate editing or "poisoning the well." Useful as the skeptic counter-current: a non-trivial subset of technical readers wants authors to *not* laundering LLM prose through style transfer at all.

### 12. HN 44191326 — "How I Use LLMs to Write"
- **URL:** https://news.ycombinator.com/item?id=44191326
- **Summary:** Working-writer workflows: use LLM as editor/clarifier, not ghostwriter. "Linguistic uncanny valley" framing — AI prose is "close enough to human to be recognizable, but different enough to be repulsive."

### 13. HN 46971643 — "Show HN: GHOSTYPE — AI voice input that learns your writing style"
- **URL:** https://news.ycombinator.com/item?id=46971643
- **Summary:** macOS app with "Virtual Personality Engine" ("Ghost Twin") that learns from local writing history to build a per-channel style vector (professional for email, casual for Discord). Local-first, E2E encrypted. Signals productization of continuous on-device style learning.

### 14. HN 44130623 — "Show HN: Willow Voice (YC X25)"
- **URL:** https://news.ycombinator.com/item?id=44130623
- **Summary:** Dictation tool that learns formatting, syntax, custom vocabulary over time. Shows style-transfer-as-a-service moving into the dictation layer.

### 15. OpenAI Dev Community — "Implement 'write like me' mode"
- **URL:** https://community.openai.com/t/implement-write-like-me-mode/1023273
- **Date:** Nov 2024
- **Summary:** Feature request for a structured writing assessment that extracts trends, vocabulary, sentence structure, overall style. Reply points to a community-built open-source `writelikeme.io`. Useful signal that users want this baked in, not prompted.

### 16. LessWrong — lsusr, "I finally got ChatGPT to sound like me" (the "hyperbolic trick")
- **URL:** https://www.lesswrong.com/posts/2d5o75nmTpLiSP4WL/
- **Date:** Sep 2024
- **Summary:** The canonical "more-you-than-you" prompt. Observation: asking the model to "write like lsusr" yields "10% me and 90% generic drivel" because the model regresses to the training-corpus mean. Fix: instruct it to amplify the author vector 10x toward satire.
- **Key prompt:** *"I need you to write a post like lsusr, but more lsusr than lsusr. I want it so over-the-top lsusr that it satirises lsusr. Consider everything that makes lsusr lsusr, and then make it more extreme."*

### 17. Substack — Diana Dovgopol (theaigirl), "How to Make Claude (and other AIs) Write Like You"
- **URL:** https://theaigirl.substack.com/p/voice
- **Date:** Mar 2026
- **Summary:** Popularizes the **voice `.md` file + interview method**. The key claim is counter-intuitive: most of a good voice profile is about what you *reject*, not what you like. "I'd never use semicolons because they make my writing sound like a college essay" beats "I like direct writing."
- **File contents:** Words/phrases never used; default sentence patterns; open/close conventions; formatting instincts; best-case example; admired writers and what to steal; positions you'd never take.

### 18. Substack — Sparkry AI, "Teach AI Your Voice in 15 Minutes (Then Let 4 Agents Perfect It)"
- **URL:** https://sparkryai.substack.com/p/teach-ai-your-voice-in-15-minutes
- **Summary:** Multi-agent pattern: Writer → Critic → Rewriter → Scorer. Claim: single-pass AI misses voice 30–40% of the time; scoring loop catches the drift. Advocates analyzing actual Gmail for real communication style over curated "best samples."

### 19. Substack — Prompts Daily, "Voice DNA Prompts"
- **URL:** https://promptsdaily.substack.com/p/voice-dna-prompts-how-i-get-ai-to
- **Summary:** "Voice Patterns" block structure: Identity Block + Audience Block + Voice Block + Output Block (sample paragraph in actual voice). Paste before each request.

### 20. Substack — Dean Seddon (Signal), "How I make ChatGPT sound like me"
- **URL:** https://signalnewsletter.deanseddon.io/p/how-i-make-chatgpt-sound-like-me
- **Date:** Feb 2025
- **Summary:** Five-step production system. Baseline input: 20,000+ words of your own writing. Output: a reusable Tone-of-Voice Doc + Custom GPT. Uses aggressive anti-word feedback ("I'd never use 'utilise,' say 'use'"). Frames the goal as "consistency, not perfection."
- **Key analysis prompt:**
  > "You are an AI language model skilled at analysing text for writing style and tone of voice. I will provide a document containing examples of my writing, and your job is to analyse it and create a detailed 'Writing Style and Tone of Voice Document.' This document should include: an overview of my tone and style; how my tone varies across platforms; typical sentence structure and language choices; common words and phrases I repeat; formatting preferences; how I connect emotionally with my audience."

### 21. Personal blog — Rory Callaghan, "How to Train ChatGPT to Write in Your Voice"
- **URL:** https://rorycallaghan.com/how-to-train-chatgpt-to-write-in-your-voice-a-step-by-step-style-embedding-guide/
- **Summary:** The most widely replicated 7-step practitioner recipe: (1) collect 5–10 samples, (2) extract style guide, (3) paste into Custom Instructions, (4) few-shot with 1–2 samples per request, (5) iterate with rewrite feedback, (6) build a reusable master prompt, (7) refresh every 2–3 months.
- **Master prompt template:**
  > "Write in my personal style as defined below. Style = [insert your Style Guide]. Use the following sample(s) as reference: [insert text/voice transcript]. Now write [type of content] on [topic]."

### 22. Zapier blog — Matt Giaro, "How to train ChatGPT to write like you"
- **URL:** https://zapier.com/blog/train-chatgpt-to-write-like-you/
- **Date:** Oct 2023, updated Mar 2025
- **Summary:** Canonical four-axis decomposition — **Voice / Tone / Style / Structure**. Custom-instruction template:
  > "Use this voice: [...]. Use this tone: [...]. Use this style: [...]. Use this structure: [...]."
  Also popularizes the "paste content + 'Analyze the writing voice, tone, and structure of the article above. Output bullet points.'" analysis prompt.

### 23. LinkedIn / Reddit repost — Sami Sharaf, "I AM READY / NEXT / DONE" analysis prompt
- **URL:** https://www.linkedin.com/posts/thesamisharaf_chatgpt-generates-fluff-but-i-fix-it-this-activity-7227625936513310720-sw62
- **Summary:** Widely reshared on Reddit. Structured multi-turn style-extraction prompt:
  > "I want you to analyze a few pieces of text that I have written. Go through the writing style, tone, word choice, rhythm, voice, and everything that you need in order to recognize the way it is written. We will start by you telling me 'I AM READY.' Once you tell me that, I will upload one piece of writing and then you will tell me 'NEXT' and I will upload another. We will go like that until I finally tell you 'DONE.' Once I tell you this, you will come up with the entire description of what my writing style is. Come up with as many relevant details as you can."

### 24. YouTube — "How I Trained ChatGPT to Exactly Write Like Me (Full System Guide)"
- **URL:** https://www.youtube.com/watch?v=inf4T7KG1YQ
- **Summary:** Walks through creating a Custom GPT pre-loaded with writing examples and derivative prompts for tweets/threads/emails/articles — the "one long piece → many derivative shorts" multiplier pattern.

### 25. YouTube — "How to Easily Make AI Write Like You | ChatGPT Fine Tuning"
- **URL:** https://www.youtube.com/watch?v=Txc1ubMojaQ
- **Summary:** Covers the full ladder from Custom Instructions → Custom GPT → actual fine-tuning API. Positions fine-tuning as overkill for most and prompts/CustomGPT as the 80/20.

### 26. Substack — Harshal Patil, "How I Made ChatGPT Write In My Style, My Tone"
- **URL:** https://harshalpatil.substack.com/p/my-writing-tone-style-train-chatgpt
- **Summary:** Quantitative self-report of ~80–90% tone accuracy after iteration. Emphasizes that Twitter/LinkedIn and long-form need separate style blocks — cross-channel voice leaks produce the worst slop.

### 27. HN 38382067 — "My experience trying to write human-sounding articles using Claude AI"
- **URL:** https://news.ycombinator.com/item?id=38382067
- **Summary:** Early practitioner post on Claude as a more "voice-preserving" alternative to GPT-4 for long-form. Foreshadows Claude's later first-party Styles feature.

---

## Patterns

1. **Convergent 5-step recipe.** Nearly every tutorial (Rory Callaghan, Zapier/Giaro, Dean Seddon, Leanne Calderwood, Harshal Patil, My Writing Twin) hits the same beats: collect samples (5–10 minimum, 20k words ideal) → extract style guide → paste into Custom Instructions / Custom GPT → few-shot with samples → iterate with rewrite feedback. The recipe has stabilized.

2. **"Rejection profile" beats "preference profile."** Both Diana Dovgopol and multiple r/ChatGPT threads report that listing words/phrases/structures you'd *never* use outperforms listing what you like. This is the strongest non-obvious practitioner insight.

3. **The "hyperbolic trick" / author-amplification.** lsusr's observation — that models regress toward the corpus mean, so you have to push style past where you actually want it — recurs informally across HN and Reddit ("write in the style of X and turn it up").

4. **Positive-shape instructions beat anti-pattern lists.** The HN LLM-tropes thread, the Streisand-effect observation, and the Claude-rewrite response all converge: describing good writing works better than banning bad writing, because banning primes the pattern.

5. **Voice `.md` file as portable artifact.** The emerging standard is a Markdown file you upload to any AI (Claude Projects, Custom GPT, Gemini). It outlives any one model, any one tool, and any one memory system.

6. **Multi-agent / editor-agent post-processing.** Both the Sparkry 4-agent loop and the HN "editor agent" comment point at the same idea: one agent writes in your voice, a second agent scrubs tropes and scores fidelity. Single-pass generation is increasingly seen as insufficient.

7. **Channel-specific style profiles.** Commercial tools (VoiceDNA, My Writing Twin, GHOSTYPE) and several Substack guides all reject a single monolithic "voice" in favor of per-channel profiles (LinkedIn vs. email vs. blog vs. tweet). Harshal Patil explicitly blames cross-channel voice leaks for the worst slop.

8. **Custom Instructions decay.** Strong, repeated complaint on r/ChatGPT and r/OpenAI: CI stops biting after ~10 messages, memory resets on model upgrades, sycophancy overrides tone rules. This is driving adoption of client-side injection (markdown files fed per-session) and external tools.

9. **Skeptic counter-current on HN.** Substantial minority view: cleaning up LLM output to sound human is "poisoning the well" — if you used AI, show your prompt and notes instead of laundering it through a voice file. Worth flagging to the Humanizer project because it frames voice transfer as a disclosure/integrity problem, not just a quality problem.

## Trends

- **Productization of voice profiles.** Dedicated tools (VoiceDNA, My Writing Twin, GHOSTYPE, Willow, writelikeme.io) are moving the workflow out of prompts and into per-user on-device or saved profiles.
- **Claude Styles as first-party baseline.** Anthropic shipped a built-in upload-samples feature; r/ChatGPT frequently points at this as "what OpenAI should have."
- **Context engineering framing.** r/PromptEngineering conversation has shifted from "what do I say to the model?" to "what does the model need to know before I say anything?" — voice files fit naturally into that framing.
- **Metric-driven style extraction.** VoiceDNA reports 40+ per-channel metrics; academic HN users are reverse-engineering LLM style fingerprints. The field is moving from vibes-based to quantified voice.

## Gaps / Opportunities (relevant to Humanizer project)

- **No standard voice-file schema.** Every guide invents its own `.md` structure. A portable, open schema (audience block, identity block, rejection list, voice exemplar, per-channel variants) would be immediately adopted.
- **No honest benchmarking of "does this actually sound like me."** Most claims are self-reported ("80–90% accuracy," "95% accuracy") with no held-out evaluation. Room for an objective style-fidelity score — blind human eval or a trained style classifier.
- **The decay problem is unsolved.** Client-side injection works but is a workaround. Neither sliders (Vellium) nor voice files fully fix the "model drifts back to mean after N turns" failure mode reported by every heavy user.
- **Positive-shape instruction patterns are under-documented.** The trope lists (HN 47291513) are exhaustive; the equivalent "good-writing shape" positive-prompt library barely exists.
- **Cross-channel voice consistency is mostly a manual problem.** Nobody has a convincing end-to-end system that learns from Gmail + LinkedIn + long-form posts and keeps them coherent.
- **"Amplify-then-temper" workflow underexploited.** The lsusr hyperbolic trick suggests a two-stage pipeline (amplify author vector → trim back toward realism) that no open tool currently exposes.
- **Skeptic/disclosure angle ignored by most guides.** The HN "if you used AI, share the prompt" position is a real user segment; a humanization product that offers provenance/transparency alongside voice transfer would differentiate from pure "make it undetectable" tools.

## Sources

- https://www.reddit.com/r/ArtificialInteligence/comments/1ourafh/ — r/ArtificialIntelligence on AI overwriting tone
- https://www.reddit.com/r/ChatGPT/comments/1rdbi9s/ — r/ChatGPT on client-side markdown overrides
- https://www.reddit.com/r/ChatGPT/comments/1molg68/ — r/ChatGPT Custom GPT build service
- https://www.reddit.com/r/ChatGPT/comments/1k9686o/ — r/ChatGPT anti-sycophancy custom instructions
- https://www.reddit.com/r/ChatGPT/comments/1n5qa8f/ — r/ChatGPT Australian voice request
- https://www.reddit.com/r/AIBranding/comments/1nwsv4a/ — r/AIBranding brand-voice edit rates
- https://www.reddit.com/r/AIWritingHub/comments/1ohxyka/ — r/AIWritingHub rewrite heuristics
- https://www.reddit.com/r/LocalLLaMA/comments/1r89a4y/ — r/LocalLLaMA Vellium slider-based style control
- https://news.ycombinator.com/item?id=39452331 — HN Show HN, personalize ChatGPT style
- https://news.ycombinator.com/item?id=47291513 — HN LLM Writing Tropes mega-thread
- https://news.ycombinator.com/item?id=44293455 — HN Writing in the Age of LLMs (skeptics)
- https://news.ycombinator.com/item?id=44191326 — HN How I Use LLMs to Write
- https://news.ycombinator.com/item?id=46971643 — HN Show HN GHOSTYPE
- https://news.ycombinator.com/item?id=44130623 — HN Show HN Willow Voice
- https://news.ycombinator.com/item?id=38382067 — HN Claude human-sounding articles
- https://community.openai.com/t/implement-write-like-me-mode/1023273 — OpenAI feature request
- https://www.lesswrong.com/posts/2d5o75nmTpLiSP4WL/ — LessWrong lsusr hyperbolic trick
- https://theaigirl.substack.com/p/voice — Substack voice `.md` interview method
- https://sparkryai.substack.com/p/teach-ai-your-voice-in-15-minutes — Substack 4-agent voice loop
- https://promptsdaily.substack.com/p/voice-dna-prompts-how-i-get-ai-to — Substack Voice DNA prompt blocks
- https://signalnewsletter.deanseddon.io/p/how-i-make-chatgpt-sound-like-me — Substack Dean Seddon system
- https://harshalpatil.substack.com/p/my-writing-tone-style-train-chatgpt — Substack 80–90% accuracy report
- https://rorycallaghan.com/how-to-train-chatgpt-to-write-in-your-voice-a-step-by-step-style-embedding-guide/ — Canonical 7-step recipe
- https://zapier.com/blog/train-chatgpt-to-write-like-you/ — Zapier/Giaro Voice/Tone/Style/Structure framework
- https://www.linkedin.com/posts/thesamisharaf_chatgpt-generates-fluff-but-i-fix-it-this-activity-7227625936513310720-sw62 — "I AM READY / NEXT / DONE" analysis prompt
- https://www.youtube.com/watch?v=inf4T7KG1YQ — YouTube full system guide
- https://www.youtube.com/watch?v=Txc1ubMojaQ — YouTube Custom GPT + fine-tuning walk-through
