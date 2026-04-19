# D — Commercial Products: Conversational & Dialogue Systems

**Research value: high** — The commercial field is converging on a shared vocabulary of "humanlike," "natural," and "empathetic" conversation. Vendors differentiate on *which* naturalness dimension they own (latency, prosody, emotion, turn-taking, or empathic reasoning), giving Humazier a concrete map of how "humanization" is marketed, bench-marked, and productized today.

**Angle focus:** Voice agents (10) + text chat platforms (5), with emphasis on naturalness / humanlike marketing claims as of 2026.

---

## Voice Agent Platforms

### 1. Bland AI
- **Category:** Enterprise outbound/inbound voice agent platform (self-hosted stack).
- **Humanization positioning:** "Build AI that people actually want to talk to." Controls the full stack — proprietary transcription, inference, and TTS on dedicated GPUs/CPUs — to avoid third-party quality drift.
- **Naturalness mechanism:** Proprietary orchestration + edge delivery network; latency-optimized CPUs/GPUs; custom voices cloned from short samples.
- **Marketing quote:** *"Most people think Emily is a real person."* — customer testimonial, MPA. Latency ~800 ms; voice quality ~8.6/10 in third-party benchmarks.
- **URL:** bland.ai

### 2. Retell AI
- **Category:** LLM-native voice agent platform ("3rd Gen Voice AI").
- **Humanization positioning:** "Talks like people." Frames itself explicitly against IVR and intent-based IVA as the first "humanlike" tier.
- **Naturalness mechanism:** Proprietary turn-taking model ("knows when to stop and when to listen"); ultra-realistic voices trained on real performance data; ~600 ms median latency.
- **Marketing quote:** *"LLM based, humanlike, voice-first conversational AI platform … built from real performance data and refined through human-guided training."*
- **URL:** retellai.com

### 3. Vapi
- **Category:** Developer platform / middleware for voice agents (BYO LLM/TTS/STT).
- **Humanization positioning:** Agents that "feel human" through orchestration flexibility rather than a single proprietary voice.
- **Naturalness mechanism:** Sub-500 ms enterprise latency; sub-600 ms turn-taking; integrates ElevenLabs, PlayHT, Deepgram, OpenAI Realtime; new "Vapi Voices Beta" ($0.0025/min) for volume.
- **Marketing quote:** Agents that *"feel human"* and *"move the needle"*; "ultra-low latency conversations" via OpenAI Realtime.
- **URL:** vapi.ai

### 4. Deepgram Voice Agent API
- **Category:** Unified STT + LLM orchestration + TTS API (Aura-2 voices).
- **Humanization positioning:** "Humanity" as one of four explicit pillars (latency, accuracy, cost, humanity).
- **Naturalness mechanism:** Sub-200 ms streaming TTS latency; 40+ voices "tuned for professional conversations"; context-aware pacing/tone; domain-tuned pronunciation; "authentic voices designed to reduce listener fatigue across thousands of turns."
- **Marketing quote:** *"Natural, business-appropriate speech for professional settings."* Priced $4.50/hr full stack.
- **URL:** deepgram.com/product/voice-agent-api

### 5. ElevenLabs Conversational / ElevenAgents
- **Category:** Voice + chat agent platform built on Eleven v3 Conversational TTS.
- **Humanization positioning:** "Human-sounding" and "natural within context" as core claims.
- **Naturalness mechanism:** Expressive tags (`[laughs]`, `[whispers]`, `[sighs]`); sub-300 ms voice latency; real-time emotion/speech-pattern-driven turn-taking; 70+ languages; 10,000+ studio voices.
- **Marketing quote:** *"Natural, human-sounding agents"* with *"ultra-low latency."*
- **URL:** elevenlabs.io/voice-agents

### 6. Hume EVI (Empathic Voice Interface)
- **Category:** Empathic voice-first agent API.
- **Humanization positioning:** *"The first AI with emotional intelligence."* Frames naturalness as emotion-matching, not just prosody.
- **Naturalness mechanism:** Empathic LLM (eLLM) blending LLM + prosody measurements; detects tune/rhythm/timbre; matches apologetic, sympathetic, calm, or excited "vibe"; ~300 ms TTFB; interruptibility; chat history carries emotion data. Octave TTS reportedly beat ElevenLabs in a 180-rater blind test on naturalness (51.7%), audio quality (71.6%), and description-match (57.7%).
- **Marketing quote:** *"Conversational AI with emotional intelligence … natural, empathic conversations at scale."*
- **URL:** hume.ai/empathic-voice-interface

### 7. Sesame (Maya & Miles / CSM)
- **Category:** Consumer-facing conversational voice companion + open-sourced Conversational Speech Model.
- **Humanization positioning:** Explicit goal is *"voice presence"* — "crossing the uncanny valley of conversational voice."
- **Naturalness mechanism:** End-to-end multimodal transformer on RVQ audio tokens; models the "one-to-many" problem (many valid ways to speak a sentence) using full conversation history; emotional intelligence, conversational dynamics, contextual awareness, consistent personality as the four pillars. Humans show *no clear preference* between CSM and real speech without context, but still prefer humans *with* context — an honest admission of the remaining gap.
- **Marketing quote:** *"A personal assistant who speaks only in a neutral tone has difficulty finding a permanent place in our daily lives … emotional flatness becomes more than just disappointing — it becomes exhausting."*
- **URL:** sesame.com/research

### 8. LiveKit Agents
- **Category:** Open-source realtime agent framework (Python + Node).
- **Humanization positioning:** Realtime "see, hear, and understand" agents with naturalness from pipeline tuning, not a single voice.
- **Naturalness mechanism:** Semantic turn detection (transformer-based); preemptive speech generation on partial transcripts to hide latency; ~1 s total response; modular STT/LLM/TTS (Cartesia, ElevenLabs) or speech-to-speech bypass mode.
- **Marketing quote:** Voice agents that enable "natural, human-sounding audio" through *semantic turn detection* (i.e., knowing when you actually finished speaking, not just when you paused).
- **URL:** livekit.com/voice-agents

### 9. Play.ai (PlayHT)
- **Category:** Conversational voice agent platform + Play 3.0 mini TTS model.
- **Humanization positioning:** "Build voice agents that sound human."
- **Naturalness mechanism:** Lifelike prosody/intonation; 320 ms UI response / 125 ms API / 143 ms model mean latency; voice cloning with accent capture; "industry-leading" acronym and number handling; 30+ languages; 50+ new conversational voices in Play 3.0 mini.
- **Marketing quote:** *"Build voice agents that sound human."* and *"the fastest, most conversational speech model yet."*
- **URL:** play.ht/voice-agents

### 10. Synthflow
- **Category:** No-code voice agent builder for SMB/enterprise phone automation.
- **Humanization positioning:** Naturalness through **configurability** rather than a proprietary voice — exposes stability, style exaggeration, similarity, patience level, and free-text intonation prompts.
- **Naturalness mechanism:** ElevenLabs Turbo v2 as default engine; "Patience Level" control adds natural pauses; voice intonation prompts like "calm, reassuring tone"; 20,000+ customers; ranked #2 on 2026 best-voice-agents lists.
- **Marketing quote:** Positioned as the no-code path to "production voice agents" with "the best visual flow builder in the category."
- **URL:** synthflow.ai

---

## Text Chat / Customer-Service Agent Platforms

### 11. Intercom Fin
- **Category:** AI agent for customer service across chat, email, voice, SMS, social (45+ languages).
- **Humanization positioning:** *"The first AI agent that delivers human-quality service."*
- **Naturalness mechanism:** Proprietary Fin AI Engine + RAG; "Procedures" that blend natural-language instructions with deterministic guardrails for complex multi-step issues; emotion-aware escalation (detects frustration, repeated phrases, keywords like "agent").
- **Marketing quote:** *"Human-quality service."* Resolution rates: 66% average, 80%+ for top 20% of customers; 99.9% accuracy on Fin 2.
- **URL:** fin.ai

### 12. Ada
- **Category:** Omnichannel AI customer service automation (50+ languages).
- **Humanization positioning:** "Quality CX at scale" with emphasis on resolution *and* empathy as joint requirements.
- **Naturalness mechanism:** Recent release notes flag *"improved empathy and follow-up questions"* — agents acknowledge issues and proactively offer follow-up. Research framing: "consumers prefer always-on AI customer service — but only when it can successfully resolve their issue" (i.e., empathy is secondary to efficacy).
- **Marketing quote:** *"Improved empathy and follow-up questions."* 84% automated resolution on chat; 34% uplift over legacy chatbots.
- **URL:** ada.cx

### 13. Cresta
- **Category:** Contact-center agent assist + Cresta AI Agent for voice/chat.
- **Humanization positioning:** Agents that *"sound and feel human"* across channels and languages.
- **Naturalness mechanism:** Explicitly rejects pure voice-to-voice models in favor of a "stitched" pipeline (STT → turn detection → LLM → TTS) so content and voice can be tuned independently. Voice cloned from a real employee, specified across **12 measurable vocal traits** (pitch, brightness, pace, melody, warmth, pacing with intentional pauses). LLM responses written "to read like spoken conversations rather than formal essays."
- **Marketing quote:** Agents that *"sound and feel human"*; agent-assist reduces manual typing by 50%+.
- **URL:** cresta.com

### 14. Forethought (SupportGPT / Solve)
- **Category:** Generative AI for customer support, embedded in Zendesk/Salesforce/Freshdesk.
- **Humanization positioning:** *"Human-like, empathetic, and conversational customer interactions."*
- **Naturalness mechanism:** Fine-tunes OpenAI models on a company's own conversation history so tone and workflow match institutional voice; classifies on sentiment, urgency, and language; auto-generates help-center articles to close coverage gaps.
- **Marketing quote:** *"Delivers human-like, empathetic, and conversational customer interactions."* Reports 77% response-time reduction, 168% ROI at 6 months.
- **URL:** forethought.ai/supportgpt

### 15. Kore.ai (XO Platform / AI for Service)
- **Category:** Multi-channel agentic AI platform (Gartner MQ leader 2025).
- **Humanization positioning:** *"The best, most memorable AI Agents have conversation flows that feel natural and human-like."*
- **Naturalness mechanism:** DialogGPT — "agentic orchestration engine that powers natural conversations at scale, providing autonomous orchestration across multiple topics." Handles interruptions, clarifications, context switching, and multi-intent utterances. v10.1 auto-generates dialogs + training-data variations from a use-case description.
- **Marketing quote:** *"Natural and human-like"* conversation flows; *"5x faster with 3x fewer operational efforts."*
- **URL:** kore.ai

### 16. (Bonus) OpenAI Realtime API — used by Vapi, LiveKit, ElevenLabs, Retell
- **Category:** Speech-to-speech model underpinning many of the above.
- **Humanization positioning:** Market reference point for "natural turn-taking" speech-to-speech.
- **Naturalness mechanism:** Native audio-in/audio-out skips the STT→LLM→TTS handoff; voices marketed as "professional" or "conversational" (marin, cedar, alloy, echo, shimmer).

---

## Patterns, Trends, and Gaps

### Converging vocabulary — and what it actually means
Virtually every vendor now claims "human-like," "natural," or "empathetic" conversation. The real differentiation is *which* of these five dimensions a vendor owns:

1. **Latency as naturalness.** Retell (~600 ms), ElevenLabs / EVI (~300 ms TTFB), Deepgram Aura-2 (<200 ms streaming), Play.ai (143 ms model), Vapi (<500 ms). Sub-second is now table stakes; sub-300 ms is the current humanlike frontier.
2. **Turn-taking and barge-in.** Retell's proprietary turn-taking model, LiveKit's semantic turn detection, ElevenLabs' emotion-aware turn-taking, Synthflow's "patience level." The field has moved past voice activity detection toward semantic end-of-utterance prediction.
3. **Prosody and expressivity.** ElevenLabs' expressive tags, Cresta's 12 measurable vocal traits, Deepgram's context-aware pacing, Play.ai's lifelike intonation, Hume Octave's context-understanding TTS.
4. **Emotion / empathy.** Hume EVI is the clearest standalone bet on this dimension; Sesame, Ada, Forethought all layer it on top of other claims.
5. **Contextual coherence.** Sesame CSM explicitly models conversation history; Intercom Fin's "Procedures" and Kore's DialogGPT chase the same goal from the dialog-management side.

### Architectural trend: unified stacks vs. orchestration kits
Two camps are now visible. **Unified proprietary stacks** (Bland, Retell, Deepgram, ElevenLabs, Hume) pitch naturalness as a side-effect of owning STT+LLM+TTS together. **Orchestration / BYO platforms** (Vapi, LiveKit, Synthflow) pitch naturalness as a side-effect of letting customers mix best-of-breed components and tune turn-taking themselves. Cresta is an outlier: it *deliberately* uses a stitched pipeline because it wants independent control over spoken-style content and vocal delivery.

### Content-side humanization is under-marketed
Only **Cresta** explicitly calls out that LLM output must be *rewritten to read like spoken conversation rather than a formal essay* — every other voice vendor treats naturalness as a TTS/latency problem and quietly assumes the LLM already produces humanlike text. This is directly relevant to Humazier: the humanization layer on the *text* side is a gap in how the voice market sells itself, even though every voice agent needs it.

### Honest calibration is rare but useful
Sesame is the only vendor that openly publishes a benchmark showing where they still lose to humans (naturalness is saturated *without* context; humans still win *with* context). Hume publishes head-to-head win rates against ElevenLabs. Most others stop at vibes-based marketing claims. Humazier's positioning can benefit from borrowing Sesame's honest "uncanny valley" framing rather than claiming parity.

### Gaps / opportunities
- **Text-chat naturalness is thinner than voice.** Intercom/Ada/Forethought/Kore market "empathetic" or "human-quality," but none publish a CMOS-style naturalness benchmark. The text side still optimizes almost entirely for *resolution rate*, not *humanness*.
- **Cross-channel humanization is not unified.** Fin and Cresta are closest to a single humanization layer across voice + chat, but most vendors still have separate TTS-flavored voice naturalness and RAG-flavored text naturalness.
- **Emotion ≠ humanness.** The market conflates the two, but Hume (emotion) and Sesame (presence/prosody) are solving different problems — a product that combines *empathic response* with *spoken-style content rewriting* is not currently offered by any single vendor.

---

## Sources

- [Retell AI vs Bland AI vs Vapi 2026 comparison](https://ainora.lt/blog/retell-ai-vs-bland-ai-vs-vapi-comparison-2026) — head-to-head latency and voice-quality scores.
- [Retell AI homepage](https://www.retellai.com/) — humanlike / 3rd-gen voice AI positioning, ~600 ms latency.
- [Bland AI homepage](https://www.bland.ai/) — full-stack self-hosted voice agents, customer quotes.
- [Sesame — Crossing the uncanny valley of conversational voice](https://sesame.com/research/crossing_the_uncanny_valley_of_voice) — CSM architecture, CMOS benchmarks, honest limitations.
- [Hume EVI product page](https://hume.ai/empathic-voice-interface) — emotional-intelligence framing, ~300 ms TTFB.
- [Hume Octave blog](https://hume.ai/blog/octave-the-first-text-to-speech-model-that-understands-what-it-s-saying) — blind-test naturalness wins over ElevenLabs.
- [Deepgram Voice Agent API](https://deepgram.com/product/voice-agent-api) and [Aura TTS](https://deepgram.com/text-to-speech) — sub-200 ms streaming, pacing/tone tuning.
- [ElevenLabs Voice Agents](https://elevenlabs.io/voice-agents) and [Expressive mode docs](https://elevenlabs.io/docs/eleven-agents/customization/voice/expressive-mode) — expressive tags, emotion-aware turn-taking.
- [LiveKit Agents](https://livekit.com/voice-agents) — semantic turn detection, preemptive speech.
- [Play.ai Voice Agents](https://play.ht/voice-agents/) and [Play 3.0 mini launch](https://play.ht/blog/introducing-play-3-0-mini/) — latency and conversational voices.
- [Synthflow voice configuration docs](https://docs.synthflow.ai/voice-configuration) — stability, style, patience-level controls.
- [Cresta — Crafting a natural-sounding AI voice](https://www.cresta.com/blog/creating-a-natural-sounding-text-to-speech-voice) — 12 vocal traits, stitched-pipeline rationale.
- [Intercom — Fin 2 and Fin 3 announcements](https://www.intercom.com/blog/announcing-fin-2-ai-agent-customer-service) — "human-quality service," resolution stats, Procedures.
- [Ada homepage](https://www.ada.cx/) and release notes — empathy + follow-up improvements, resolution focus.
- [Forethought SupportGPT launch](https://www.businesswire.com/news/home/20230308005227/en/) and [product page](https://forethought.ai/supportgpt) — human-like + empathetic claims.
- [Kore.ai XO Platform v10.1](https://blog.kore.ai/kore.ai-xo-platform-v10.1-release-revolutionizing-iva-development-with-generative-language-models) and [intelligence docs](https://docs.kore.ai/xo/automation/intelligence/intelligence-overview/) — DialogGPT, natural conversation flow.
- [Vapi homepage](https://www.vapi.ai/) and [Vapi Voices Beta](https://vapi.ai/blog/vapi-voices-beta) — sub-500 ms, BYO-model positioning.
