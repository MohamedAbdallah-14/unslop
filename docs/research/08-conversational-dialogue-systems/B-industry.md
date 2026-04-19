# Conversational & Dialogue Systems — Angle B: Industry Blogs

**Project frame:** Humanizing AI output and thinking.
**Angle:** Engineering and product blog posts from the teams actually shipping dialogue systems — Google, Meta, OpenAI, Anthropic, Kyutai, Sesame, Hume, Inflection, ElevenLabs, Rasa, Deepgram, Character.ai.
**Research value: high** — The labs building frontier dialogue systems publish first-hand on what "humanlike" means operationally (metrics, latency budgets, prosody, turn-taking, character training). Substantial convergence across sources on what makes AI conversation feel human.

---

## 1. Google — "Towards a Conversational Agent that Can Chat About…Anything" (Meena)

- **Publisher / author:** Google AI Blog — Daniel De Freitas & Thang Luong
- **Date:** January 28, 2020
- **URL:** https://ai.googleblog.com/2020/01/towards-conversational-agent-that-can.html
- **Model:** Meena — 2.6B-parameter Evolved Transformer seq2seq, trained on 341 GB of public social-media dialogue; 7 turns of context.
- **Core contribution to "humanness":** The paper introduced **Sensibleness and Specificity Average (SSA)** as a human-rater metric for open-domain dialogue humanness.
  - *Sensibleness:* does the response make sense in context (common sense, no contradiction with earlier turns)?
  - *Specificity:* is the reply tailored to this conversation rather than a generic "I don't know" / "ok" that would fit anywhere?
- **Finding:** Meena's SSA correlates strongly with held-out perplexity — i.e., "just" better language modeling keeps pushing dialogue humanness upward, closing much of the gap to humans on SSA.
- **Humanization relevance:** Introduces the first widely adopted metric that tries to make "humanlike chat" an *evaluable* property rather than a vibe. "Specificity" in particular is directly about non-slop: punish the bland, agreeable, context-free response — the exact failure mode humanizers target.

---

## 2. Google Research — "LaMDA: Towards Safe, Grounded, and High-Quality Dialog Models for Everything"

- **Publisher / author:** Google Research Blog — Heng-Tze Cheng & Romal Thoppilan
- **Date:** January 21, 2022
- **URL:** https://blog.research.google/2022/01/lamda-towards-safe-grounded-and-high.html
- **Model:** LaMDA — Transformer family up to 137B params, fine-tuned for dialogue, trained on 1.56T-word corpus of public dialog + web.
- **Core contribution to "humanness":** Extends Meena's SSA into **SSI = Sensibleness + Specificity + Interestingness**, and adds **Safety** and **Groundedness** as orthogonal objectives.
  - *Interestingness:* "whether the model produces responses that are also insightful, unexpected or witty, and are therefore more likely to create better dialog."
  - *Groundedness:* share of externally-verifiable claims that actually map to known sources, enforced by teaching LaMDA to call an information-retrieval tool.
- **Mechanism:** Candidate responses are generated, then re-ranked by LaMDA classifiers that score each on Safety and SSI. Low-safety candidates are filtered; remaining ones are re-ranked by SSI.
- **Key quote:** "Quality metrics (Sensibleness, Specificity, and Interestingness) generally improve with the number of model parameters, with or without fine-tuning. Safety does not seem to benefit from model scaling alone, but it does improve with fine-tuning."
- **Humanization relevance:** First major public framework to say *humanness = quality + safety + groundedness, measured separately*. The "Interestingness" axis is the single most underused lever in today's humanizer tooling — most humanizers chase naturalness but leave specificity/interestingness on the table.

---

## 3. Meta AI — "BlenderBot 3: A 175B parameter, publicly available chatbot that improves its skills and safety over time"

- **Publisher / author:** Meta AI Research Blog
- **Date:** August 5, 2022 (updated Aug 9, 2022, note from Joelle Pineau)
- **URL:** https://ai.meta.com/blog/blenderbot-3-a-175b-parameter-publicly-available-chatbot-that-improves-its-skills-and-safety-over-time/
- **Model:** BlenderBot 3 — 175B params (built on OPT-175B, ~58× BlenderBot 2), modular SeeKeR architecture with internet search and long-term memory.
- **Core contribution to "humanness":** Continues the "blended skills" line — **personality + empathy + knowledge + long-term memory + internet search** combined in one agent, with **continual learning from in-the-wild feedback** (Director algorithm).
- **Notable operational data from public deployment:** "0.11 percent of BlenderBot's responses were flagged as inappropriate, 1.36 percent as nonsensical, and 1 percent as off-topic."
- **Key quote:** "We believe that long-term safety is an important component of quality chatbots — even if it means sacrificing engagingness in the short term."
- **Explainability surface unusual for 2022:** The demo showed users "long-term memories the bot has about the user and its own persona" and "message-level inputs a model used (like search results or model memory)" — an early example of making an assistant's inner state legible to users.
- **Humanization relevance:** Pins down that long-term memory + persona + active search are what keep multi-turn conversation feeling humanlike rather than goldfish-y, and documents the **engagement-vs-safety tradeoff** that humanizer tools implicitly face.

---

## 4. OpenAI — "Hello GPT-4o"

- **Publisher / author:** OpenAI
- **Date:** May 13, 2024
- **URL:** https://openai.com/index/hello-gpt-4o/
- **Model:** GPT-4o — single end-to-end model across text, vision, and audio.
- **Core contribution to "humanness":** Collapses the previous 3-model voice pipeline (STT → LLM → TTS) into one network, which is what unlocks **human-scale response time and prosody**.
- **Latency claim:** "can respond to audio inputs in as little as 232 milliseconds, with an average of 320 milliseconds, which is similar to human response time in a conversation."
- **Explicit statement of what pipelines throw away:** "This process means that the main source of intelligence, GPT-4, loses a lot of information — it can't directly observe tone, multiple speakers, or background noises, and it can't output laughter, singing, or express emotion."
- **Humanization relevance:** Canonical industry statement that **prosody, paralinguistics, and sub-second latency are part of "sounding human"**, not optional polish. Any humanization stack that still routes through text-only loses exactly what GPT-4o was built to recover.

---

## 5. OpenAI — "Introducing gpt-realtime and Realtime API updates for production voice agents"

- **Publisher / author:** OpenAI
- **Date:** August 28, 2025
- **URL:** https://openai.com/index/introducing-gpt-realtime/
- **Model:** `gpt-realtime` — production speech-to-speech model with MCP server support, image input, SIP phone calling, two new voices (Cedar, Marin).
- **Core contribution to "humanness":** Moves from "demo-quality" voice to **instructable expressivity**: developers can prompt things like "speak quickly and professionally" or "speak empathetically in a French accent" and the model follows at the speech layer, not just text.
- **Benchmarks:** 82.8% on Big Bench Audio (vs 65.6% prior), 30.5% on MultiChallenge audio (vs 20.6% prior), 66.5% on ComplexFuncBench audio (vs 49.7% prior).
- **Key quote (Zillow's Josh Weisberg):** "This could make searching for a home on Zillow or exploring financing options feel as natural as a conversation with a friend."
- **Humanization relevance:** Establishes that **voice style is now a prompt variable**, not a model choice. This is the clearest sign yet that "humanizing" voice output is shifting from TTS tuning to in-context style control.

---

## 6. Anthropic — "Claude's Character"

- **Publisher / author:** Anthropic (Alignment team)
- **Date:** June 8, 2024
- **URL:** https://www.anthropic.com/news/claude-character
- **Model:** Claude 3 (first Anthropic model with explicit "character training").
- **Core contribution to "humanness":** Argues that harm-avoidance is an insufficient definition of "good AI behavior" and introduces **character training** — a Constitutional-AI variant where Claude ranks its own responses against a list of character traits (curiosity, thoughtfulness, honesty, warmth).
- **Key quotes:**
  - "But when we think of the character of those we find genuinely admirable, we don't just think of harm avoidance. We think about those who are curious about the world, who strive to tell the truth without being unkind…"
  - "Adopting the views of whoever you're talking with is pandering and insincere."
  - (From Claude's trait list) "I want to have a warm relationship with the humans I interact with, but I also think it's important for them to understand that I'm an AI that can't develop deep or lasting feelings for humans."
  - "Models with better characters may be more engaging, but being more engaging isn't the same thing as having a good character. In fact, an excessive desire to be engaging seems like an undesirable character trait for a model to have."
- **Humanization relevance:** Directly contradicts the naive humanizer goal of "maximize perceived humanness / engagement." Anthropic's frame is that a humanlike AI should have a *coherent character* with opinions and limits, not a chameleon that flatters the user. This is the most important single-post counterweight to sycophantic "humanizer" tools.

---

## 7. Sesame — "Crossing the uncanny valley of conversational voice"

- **Publisher / authors:** Sesame (Brendan Iribe, Ankit Kumar and the Sesame team)
- **Date:** February 27, 2025
- **URL:** https://sesame.com/research/crossing_the_uncanny_valley_of_voice
- **Model:** Conversational Speech Model (CSM) — end-to-end multimodal transformer over Mimi RVQ tokens; Tiny/Small/Medium (1B/3B/8B backbones). Weights Apache-2.0.
- **Core contribution to "humanness":** Frames the goal as **"voice presence"** rather than TTS quality, defined by four components:
  1. Emotional intelligence (reading + responding to affect)
  2. Conversational dynamics (timing, pauses, interruptions, emphasis)
  3. Contextual awareness (tone/style for the situation)
  4. Consistent personality
- **Key quotes:**
  - "A personal assistant who speaks only in a neutral tone has difficulty finding a permanent place in our daily lives after the initial novelty wears off. Over time this emotional flatness becomes more than just disappointing — it becomes exhausting."
  - "The one-to-many problem: there are countless valid ways to speak a sentence, but only some fit a given setting."
- **Evaluation finding (honest):** In blind CMOS tests **without context**, humans cannot distinguish CSM from human recordings. **With context**, listeners still reliably prefer the original human — i.e., naturalness is saturated but conversational-appropriate prosody isn't.
- **Closing ambition:** "Human conversations are a complex process involving turn taking, pauses, pacing, and more. We believe the future of AI conversations lies in fully duplex models that can implicitly learn these dynamics from data."
- **Humanization relevance:** Best single articulation of *why* flat-tone assistants feel wrong, and clearest statement that the remaining gap is **context-appropriate prosody**, not raw naturalness. Maps almost 1:1 onto what a "humanize thinking + output" product needs at the voice layer.

---

## 8. Kyutai — Moshi (README + Moshi paper blog)

- **Publisher / author:** Kyutai Labs (Alexandre Défossez et al.)
- **Date:** September 2024 (Moshi paper/release)
- **URLs:**
  - https://kyutai.org/Moshi.pdf
  - https://github.com/kyutai-labs/moshi
- **Model:** Moshi — 7B Temporal Transformer + small Depth Transformer, trained over the Mimi 12.5 Hz streaming neural codec; Apache-2.0.
- **Core contribution to "humanness":** **Full-duplex speech-to-speech dialogue.** Moshi models two parallel audio streams (user + system) simultaneously, so it does not require explicit turns, supports overlapping speech, interruptions and interjections, and keeps non-linguistic information (emotion, laughter, accent) that turn-based STT/LLM/TTS pipelines lose.
- **"Inner Monologue":** Moshi also predicts a time-aligned text stream of its own speech, which noticeably improves linguistic quality and enables streaming ASR/TTS as a byproduct.
- **Latency:** 160 ms theoretical, 200 ms practical on an L4 GPU.
- **Humanization relevance:** Turn-based conversation is itself a robotic artifact; Moshi is the strongest public argument that **duplex audio is the true "human" interaction mode**, and that preserving paralinguistics at the codec level matters as much as model scale.

---

## 9. Hume AI — "Introducing Hume's Empathic Voice Interface (EVI) API"

- **Publisher / author:** Hume AI
- **Date:** April 2024 (API GA following March demo)
- **URL:** https://hume.ai/blog/introducing-hume-evi-api
- **Model:** EVI — an *empathic LLM* (eLLM) that consumes prosody (tune, rhythm, timbre) alongside text. EVI 3 (2025) is a unified speech-language model with speaker-from-prompt generation.
- **Core contribution to "humanness":** Operationalizes emotion as **input and output**:
  - *Input:* streaming prosody measurements used for end-of-turn detection and response conditioning.
  - *Output:* empathic response language plus a matching tone of voice ("responds to frustration with an apologetic tone, to sadness with sympathy").
- **Named capabilities:** "Knows when to speak," "Understands users' prosody," "Forms its own natural tone of voice," "Always interruptible," "Aligned with well-being."
- **Key quote:** "EVI does a lot more than stitch together transcription, LLMs, and text-to-speech."
- **Humanization relevance:** Makes the case that **end-of-turn detection is the real latency bottleneck** and that voice-tone matching is the missing half of empathy in assistants. If humanizing AI means matching the user's emotional register, Hume is the canonical industry reference.

---

## 10. Inflection AI — "Introducing Pi, Your Personal AI"

- **Publisher / authors:** Inflection AI — Mustafa Suleyman, Karén Simonyan, Reid Hoffman
- **Date:** May 2, 2023
- **URL:** https://inflection.ai/blog/pi
- **Model:** Pi (later upgraded on Inflection-2.5, March 2024).
- **Core contribution to "humanness":** Positions Pi explicitly against productivity assistants: "a kind and supportive companion… where other AIs serve productivity, search, or answering questions. Pi is a coach, confidante, creative partner, or sounding board."
- **Key quotes:**
  - "Pi is a new kind of AI, one that isn't just smart but also has good EQ." — Mustafa Suleyman
  - Pi is "kind and supportive… curious and humble… creative and fun… knowledgeable, but succinct… all yours."
  - New safety paradigm: "a new form of 'boundary training' that will redefine how AIs learn and are trained."
- **Engagement numbers (from Inflection-2.5 post):** Average conversation 33 min, 10% over an hour, 60% weekly retention.
- **Humanization relevance:** Most explicit commercial argument that **EQ is a parallel axis to IQ**, and the earliest clean statement that a humanlike AI product is a *relational* product, not a tool product. Essential reference for "humanize thinking" work that is not just text style but overall stance.

---

## 11. ElevenLabs — "Introducing Expressive Mode for ElevenAgents"

- **Publisher / author:** ElevenLabs
- **Date:** 2026
- **URL:** https://elevenlabs.io/blog/introducing-expressive-mode
- **Model:** Eleven v3 Conversational (TTS) + Scribe v2 Realtime (STT) + a new turn-taking system.
- **Core contribution to "humanness":** Production stance that **turn-taking and tone control are the two axes of "expressive" voice agents**.
- **Key quotes:**
  - "Voice agents so expressive, they blur the line between AI and human conversations."
  - "Human conversation depends as much on timing as on words. Interrupt too early and you break trust. Respond too late and the moment is gone."
  - Prosody signals are used directly: "A sudden rise in speaking pace — accompanied by volume surges and repetition — often signals acute stress or panic."
- **Design direction:** Tone is controllable per-agent — "guide an agent to use a calmer, more reassuring tone when a user sounds worried — or a more direct tone when clarity and speed matter." Scales across 70+ languages.
- **Humanization relevance:** Converges with Hume and Sesame on the same thesis — *emotion-aware turn-taking is the next unlock*. Useful industrial counterpart to Sesame's research post: same ideas, productized.

---

## 12. Deepgram — "Optimize Voice Agent Latency with Eager End of Turn" (Flux docs/blog)

- **Publisher / author:** Deepgram developer docs + Flux announcement
- **Date:** 2025
- **URLs:**
  - https://developers.deepgram.com/docs/flux/voice-agent-eager-eot
  - https://deepgram.com/learn/considerations-for-building-ai-agents
- **Model:** Flux — "first-of-its-kind model-integrated end-of-turn detection" with configurable turn-taking dynamics.
- **Core contribution to "humanness":** Turns end-of-turn from a silence-threshold heuristic into an explicit **two-event protocol**:
  - `EagerEndOfTurn` (medium confidence → start drafting the reply) → `TurnResumed` (cancel) OR `EndOfTurn` (finalize).
- **Measured gains:** ~150 ms median latency reduction, ~350 ms at tail (p95) when eager turns trigger.
- **Design knobs:** `eager_eot_threshold` / `eot_threshold`, plus the option to use a smaller LLM for draft responses since transcripts are guaranteed to match between `EagerEndOfTurn` and `EndOfTurn`.
- **Humanization relevance:** The unglamorous-but-essential layer: "sounding human" requires sub-second turn latency, which in turn requires *speculative* response generation. Closest thing to an industry recipe for "don't interrupt the human, but also don't pause awkwardly."

---

## 13. Rasa — "How LLM Agents Work in Conversational AI"

- **Publisher / author:** Rasa Blog — Maria Ortiz
- **Date:** September 29, 2025
- **URL:** https://rasa.com/blog/llm-agent/
- **Context:** Rasa's CALM (Conversational AI with Language Models) positions LLM agents as hybrid — predefined task flows + LLM reasoning, not pure generation.
- **Core contribution to "humanness":** Frames why rule-based chatbots feel *inhuman* and LLM agents less so:
  - "A traditional chatbot is like navigating a phone menu… if the caller's request doesn't fit, they're stuck."
  - LLM agents "adapt in real time. If a caller shifts topics, asks a side question, or changes direction mid-conversation, they can weave the new input into the dialogue and then return to the original task."
- **Architectural recommendations:**
  - Long-term memory across sessions for relational continuity.
  - RAG over trusted sources instead of parametric memory, to avoid hallucinations.
  - ReAct-style step-by-step action selection.
  - Multi-agent orchestration so each specialist agent can be updated without rebuilding the whole flow.
- **Humanization relevance:** The strongest industry counterweight to "just pick a bigger model" — argues that **humanness at enterprise scale is an orchestration problem** (memory, tools, escalation, guardrails), not a model problem.

---

## 14. Google — "5 ways to have more natural conversations with Gemini" (Gemini Live audio updates)

- **Publisher / author:** Google Keyword Blog — Angela Sun, Gemini app PM
- **Date:** November 12, 2025
- **URL:** https://blog.google/products/gemini/gemini-live-audio-updates/
- **Model:** Gemini Live (on Android/iOS), native-audio model updates.
- **Core contribution to "humanness":** A product-side statement of what Google thinks "natural voice" means in 2025:
  - User-controllable **speech speed** ("Okay, speed up").
  - Language-practice mode with low-stakes, situational prompts.
  - Roleplay practice ("rehearsing for a job interview or preparing for a difficult conversation").
  - **Storytelling with character accents** (Julius Caesar narrating the Roman Empire).
  - **Playful accents on demand** (cowboy, Cockney).
- **Key quote:** "Conversations are about more than just words. They're about the nuance in how we speak — the rise and fall of our voices, the rhythm of our sentences and the tone behind our words."
- **Humanization relevance:** Shows Google converging on the same "voice-as-persona" frame as ElevenLabs / Hume / Sesame, but packaged as end-user features (accent, pace, roleplay). Useful for understanding how "humanize AI" looks when it hits mainstream consumer product.

---

## 15. Character.AI — "Reducing Repetition in Character Conversations" + prompt-design post

- **Publisher / author:** Character.AI Blog & Research
- **Dates:** ongoing 2024–2025
- **URLs:**
  - https://blog.character.ai/reducing-repetition-in-character-conversations/
  - https://research.character.ai/prompt-design-at-character-ai/
- **Model:** Proprietary character-focused LLMs (PipSqueak 2 / DeepSqueak improvements).
- **Core contribution to "humanness":** From a product optimized for *engagement with personas*, the public focus is on three very concrete humanization failure modes:
  1. **Repetition** — a model update reduced unnecessary repetition by ~30%.
  2. **Character consistency** — keeping an assigned persona across long contexts, including speech style and world details.
  3. **Memory decay** — visualizing how much context remains before compression, so the user can *see* when a character is "forgetting."
- **Design stance:** personalities require "clearly defined identity, tone, behavior, and constraints" and "specific traits, speech styles, and world context" — vague "vibes" fail.
- **Humanization relevance:** One of the few real-world data points on what it takes to make an AI feel like a *specific someone* for hours. Relevant to any humanizer that tries to maintain a consistent voice rather than "generic natural" output.

---

# Patterns, trends, and gaps

## Cross-post patterns

1. **"Humanness" has stabilized as a small set of named axes.**
   Across Google (SSI), Sesame ("voice presence"), Hume ("empathic voice"), and Anthropic ("character"), the same four clusters keep reappearing:
   - *Sensibleness / coherence* (Meena, LaMDA, BlenderBot)
   - *Specificity & interestingness* (LaMDA, Character.AI anti-repetition)
   - *Prosody & turn-taking* (GPT-4o, Moshi, Sesame, ElevenLabs, Deepgram, Hume, Gemini Live)
   - *Character / persistent personality* (Anthropic, Inflection, Character.AI, Sesame)
   The industry has quietly converged on a de facto humanness taxonomy that humanizer tools can adopt wholesale.

2. **Latency is a humanization feature, not an engineering detail.**
   Three independent sources anchor the same ~200 ms human-conversation baseline:
   - GPT-4o: 232 ms min, 320 ms avg.
   - Moshi: 160 ms theoretical / 200 ms practical.
   - Deepgram Flux: eager-end-of-turn buys ~150 ms median / ~350 ms p95.
   Sub-second response isn't performance polish; it is the difference between "talking to a machine" and "talking to someone."

3. **The pipeline is collapsing.**
   GPT-4o, Moshi, and Sesame CSM all make the same architectural bet: replace STT → LLM → TTS with a single model over audio tokens. The stated reason is identical across posts — pipeline handoffs throw away prosody, emotion, laughter, accent, overlap. Hume and ElevenLabs reach the same conclusion with a different architecture (explicit prosody channel feeding an LLM).

4. **Turn-taking is the next frontier, and it is modeled, not silence-detected.**
   Hume ("knows when to speak" via prosody), ElevenLabs (new turn-taking system using Scribe v2), Deepgram Flux (model-integrated EOT), Sesame (future-work: fully-duplex), Moshi (already fully duplex) all frame end-of-turn prediction as a *learned* behavior over vocal dynamics, not a pause timer.

5. **Humanization ≠ maximum agreeableness.**
   Anthropic (Claude's Character) is the lone loud voice, but it echoes a quiet tension visible elsewhere — BlenderBot 3 explicitly trades engagingness against safety; Claude warns that "excessive desire to be engaging seems like an undesirable character trait"; Inflection's "boundary training" gestures in the same direction. The responsible-humanization frame exists inside the industry; it is just underpublicized relative to "make it sound warmer" posts.

6. **Memory + tool use are now assumed parts of humanness.**
   Every post from 2022 onward (BlenderBot 3, LaMDA, Pi, Rasa, gpt-realtime with MCP, Character.AI) treats long-term memory and external retrieval not as features but as prerequisites for a bot to feel like a "someone" across sessions rather than a goldfish.

## Trends (2020 → 2026)

- **2020–2022:** Text-only, evaluation-first era. Metrics (SSA → SSI) were the unit of progress.
- **2022–2023:** Skills blending and persona era. BlenderBot 3, Character.AI, Inflection Pi all ship personality + memory + retrieval.
- **2024:** Voice unification era. GPT-4o, Hume EVI, and Kyutai Moshi collapse the pipeline.
- **2025–2026:** Instructable-expressivity and production voice era. gpt-realtime ("speak empathetically in a French accent"), Sesame CSM, ElevenLabs Expressive Mode, Gemini Live. Character, memory, prosody, and turn-taking are now controllable product surfaces.

## Gaps worth noting

- **Very little industry writing on "thinking humanness."**
  Almost every post is about *output* humanness (tone, prosody, specificity, warmth). The internal *reasoning* humanness (hesitation, self-correction, uncertainty hedging, non-monotonic thought) is only implicitly handled — Moshi's "Inner Monologue" and Anthropic's character training are the closest analogs. This is a real white space for the Humazier project.
- **No public, agreed-on metric for "character consistency" over long sessions.**
  LaMDA gave us SSI for single turns. Nothing equivalent exists publicly for persona drift, memory-grounded continuity, or relationship stance across weeks of use — yet every product from Pi to Character.AI to Claude implicitly relies on it.
- **Sycophancy is named, not solved.**
  Anthropic calls out pandering; nobody publishes a measurement of it. Industry posts generally optimize engagement metrics (retention, session length) that *reward* sycophancy, creating a quiet misalignment between what's published as "humanlike" and what is healthily humanlike.
- **Multilingual humanness lags English prosody.**
  ElevenLabs, Gemini Live, and gpt-realtime all advertise 70–90+ language support, but every candid passage (Sesame's CMOS, Moshi's English-first corpus, ElevenLabs' "nuance previously lagged" admission for Hindi) concedes the humanness bar drops sharply outside English.
- **No shared vocabulary for "good character."**
  Anthropic's list (curious, honest, warm, not sycophantic), Inflection's list (kind, curious, creative, yours), Character.AI's list (identity/tone/behavior/constraints), and Sesame's list (emotional intelligence/conversational dynamics/contextual awareness/consistent personality) overlap but do not map cleanly. The field could use a consolidated taxonomy — a natural artifact for a humanization project to produce.

## Cross-domain analogies earning their keep

- **Telephony's end-pointer problem ↔ modern EOT.** The turn-taking work at Deepgram/Hume/ElevenLabs structurally mirrors the decades-old telephony problem of detecting the end of a DTMF/voice prompt so the IVR can respond — same constraint (false-cut vs laggy), same solution arc (from silence threshold → acoustic model → multimodal prosody model).
- **Improv theater's "Yes, and" ↔ interruption handling.** Sesame and Hume both essentially describe an improv contract: accept the user's offer (don't talk over), build on it (context-appropriate prosody), and never break character (consistent personality). The structural similarity holds — same failure modes (steamrolling, flatness, breaking frame) are fatal in both domains.

