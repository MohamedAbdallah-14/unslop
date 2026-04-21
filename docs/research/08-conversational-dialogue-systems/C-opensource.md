# Category 8 — Conversational & Dialogue Systems

**Angle C — Open-Source & GitHub**

**Project:** Unslop (humanizing AI output and thinking)
**Research date:** 2026-04-19
**Scope:** Open-source dialogue frameworks and the new generation of full-duplex voice stacks relevant to humanized conversational AI — Rasa, ParlAI, DialoGPT, Moshi, Ultravox, Pipecat, LiveKit Agents, and adjacent whisper+TTS/open-voice-agent projects.

---

## Research value: high

Very dense prior art. The open-source conversational stack has bifurcated into (a) legacy intent/dialogue frameworks in maintenance mode (ParlAI, DialoGPT, classic Rasa) and (b) a fast-moving 2024–2026 wave of real-time voice agent frameworks and full-duplex speech-text foundation models that are directly relevant to making AI *feel* human in conversation. For a humanization project, the second wave is where the interesting levers are: full-duplex turn-taking, inner monologue, semantic end-of-turn detection, and "optimistic" acknowledgments.

---

## Repository Matrix

| # | Repo | Stars (approx) | License | Language | Status | Relevance to humanization |
|---|---|---|---|---|---|---|
| 1 | [RasaHQ/rasa](https://github.com/RasaHQ/rasa) | ~21.1k | Apache 2.0 | Python | CALM framework now primary; v3.16 + Studio 1.16 Spring 2026; GPT-5.1 + Claude Sonnet 4.5 support | Hybrid LLM-reasoning + deterministic flows; enterprise-safe alternative to full-duplex wave |
| 2 | [facebookresearch/ParlAI](https://github.com/facebookresearch/ParlAI) | ~10.6k | MIT | Python | **Archived Nov 3, 2023**; v1.7.2 final | Historical corpus of 100+ dialogue datasets & baselines |
| 3 | [microsoft/DialoGPT](https://github.com/microsoft/DialoGPT) | ~2k+ | MIT | Python | No longer maintained; superseded by GODEL | Reddit-trained GPT-2 response generator; early humanness study |
| 4 | [kyutai-labs/moshi](https://github.com/kyutai-labs/moshi) | ~9.9k | MIT (Py) / Apache 2.0 (Rust); weights CC-BY 4.0 | Python / Rust / MLX | Active (weights updated Dec 2025; MoshiVis multimodal extension Jan 2026) | Full-duplex speech-text foundation model with inner monologue; ~200ms latency |
| 5 | [fixie-ai/ultravox](https://github.com/fixie-ai/ultravox) | ~4.4k | MIT | Python | Active (v0.7 default since Dec 2025; trained on GLM 4.6, leads VoiceBench) | Audio-in LLM that skips ASR stage — preserves prosody & non-verbal cues |
| 6 | [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | ~11k | BSD 2-Clause | Python | Active (230+ contributors, 108+ releases) | Pluggable real-time voice pipeline — the "LangChain of voice" |
| 7 | [livekit/agents](https://github.com/livekit/agents) | ~10k | Apache 2.0 | Python (+ TS via AgentsJS) | Active | WebRTC-native voice agent framework with semantic turn detection |
| 8 | [bolna-ai/bolna](https://github.com/bolna-ai/bolna) | ~600 | MIT | Python | Active | Voice agents tuned for Indian languages & telephony (Twilio/Plivo/Exotel) |
| 9 | [vocodedev/vocode-core](https://github.com/vocodedev/vocode-core) | ~3.7k | MIT | Python | Active | LLM-over-telephony agents (phone, Zoom, LangChain) |
| 10 | [Shaunwei/RealChar](https://github.com/Shaunwei/RealChar) | ~6.2k | MIT | Python / TS / Swift | Slower activity | Persona-first AI character companion across web/mobile/terminal |
| 11 | [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) | ~11.4k | Apache 2.0 | Python/PyTorch | Active | Full "Conversational AI" toolkit: ASR, speaker ID, TTS, chatbot recipes |
| 12 | [botpress/botpress](https://github.com/botpress/botpress) | ~14.6k | multiple (v12 AGPL-3.0) | TypeScript | Active (cloud-focused) | GPT/LLM-agent platform with NLU + channel integrations |
| 13 | [NVIDIA-NeMo/NeMo](https://github.com/NVIDIA/NeMo) | ~17k | Apache 2.0 | Python | Active (v2.7.2) | ASR/TTS/LLM framework; recently added full-duplex `Nemotron 3 VoiceChat` |
| 14 | [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) | ~36k | MIT (free commercial) | Python | Active (V2, Apr 2024) | Zero-shot cross-lingual voice cloning for persona consistency |
| 15 | [coqui-ai/TTS](https://github.com/coqui-ai/TTS) / [idiap fork](https://github.com/idiap/coqui-ai-TTS) | ~35k | MPL-2.0 | Python | Upstream unmaintained; Idiap fork active | XTTSv2 streaming TTS (<200ms); 1,100+ languages |
| 16 | [ictnlp/LLaMA-Omni](https://github.com/ictnlp/LLaMA-Omni) / [LLaMA-Omni2](https://github.com/ictnlp/LLaMA-Omni2) | — | Apache 2.0 | Python | Active — Omni 2 (0.5B–32B, Qwen2.5 backbone) released Apr 2025, ACL 2025 main | End-to-end speech-in/speech-out with autoregressive streaming decoder; 0.5B enables on-device |
| 17 | [KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) + [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) | ~9.6k / ~3.9k | MIT | Python | Community-maintained | Low-latency STT/TTS building blocks with VAD, wake-word, streaming |
| 18 | [stimm-ai/stimm](https://github.com/stimm-ai/stimm) | — | OSS | Python / TS | Active (v0.1.13, Mar 2026) | "Optimistic VUI" — dual-agent where one acknowledges while a second reasons |
| 19 | [tarun7r/Vocal-Agent](https://github.com/tarun7r/Vocal-Agent) | — | OSS | Python | Active | Reference cascading stack: Whisper large-v1 + Silero VAD + Llama 3.1 8B + Kokoro TTS |
| 20 | [theogbrand/fully_oss_realtime_voice_ai](https://github.com/theogbrand/fully_oss_realtime_voice_ai) | — | OSS | Python | Reference | OpenAI Realtime alternative: Whisper large-v2 + SEA-LIONv2 + XTTS v2 on Pipecat/Modal |
| 21 | [NVIDIA/personaplex](https://github.com/NVIDIA/personaplex) | — | MIT + NVIDIA Open Model | Python | Active (v1, Jan 2026) | 7B full-duplex model; ~170 ms latency; persona via text prompt + audio conditioning; learned backchannel from Fisher corpus |
| 22 | [pipecat-ai/smart-turn](https://github.com/pipecat-ai/smart-turn) | — | OSS | Python | Active (v3.1, 2025) | Open-source semantic VAD (8M params, Whisper Tiny base); 12 ms CPU inference; audio-only (no transcript required); 13+ languages |

---

## Representative README quotes

**Moshi — `kyutai-labs/moshi`:**
> "Moshi is a speech-text foundation model and **full-duplex** spoken dialogue framework. It uses Mimi, a state-of-the-art streaming neural audio codec." […] "Moshi models two streams of audio: one corresponds to Moshi speaking, and the other one to the user speaking. Along with these two audio streams, Moshi predicts text tokens corresponding to its own speech, its **inner monologue**, which greatly improves the quality of its generation."

**Pipecat — `pipecat-ai/pipecat`:**
> "Pipecat is an open-source Python framework for building real-time voice and multimodal conversational agents. Orchestrate audio and video, AI services, different transports, and conversation pipelines effortlessly—so you can focus on what makes your agent unique." Available service categories include STT, LLM, TTS, **Speech-to-Speech** (AWS Nova Sonic, Gemini Multimodal Live, OpenAI Realtime, Ultravox), transports (Daily/LiveKit/WebSocket/WhatsApp), and video avatars.

**LiveKit Agents — `livekit/agents`:**
> "The Agent Framework is designed for building realtime, programmable participants that run on servers. Use it to create conversational, multi-modal voice agents that can see, hear, and understand." Key feature: "**Semantic turn detection**: Uses a transformer model to detect when a user is done with their turn, helps to reduce interruptions."

**Ultravox — `fixie-ai/ultravox`:**
> "A fast multimodal LLM for real-time voice." Ultravox extends open-weight LLMs (Llama 3.3 70B, Mistral, Gemma) "with a multimodal projector that converts audio directly into the high-dimensional space used by the language model" — no separate ASR stage.

**Stimm — `stimm-ai/stimm`:**
> "The Open Source Voice Agent Platform. Orchestrate ultra-low latency AI pipelines for real-time conversations over WebRTC." Introduces **Optimistic VUI** — a dual-agent architecture where one agent acknowledges the user immediately while a second reasons in the background.

**NVIDIA PersonaPlex — `NVIDIA/personaplex`:**
> "PersonaPlex is a real-time, full-duplex speech-to-speech conversational model that enables persona control through text-based role prompts and audio-based voice conditioning, producing natural, low-latency spoken interactions with a consistent persona." Handles interruptions, backchannels, and authentic conversational rhythm with ~170 ms response time; open weights MIT + NVIDIA Open Model License.

**Pipecat Smart-Turn — `pipecat-ai/smart-turn`:**
> "Smart Turn Detection uses an advanced machine learning model to determine when a user has finished speaking and your bot should respond." Whisper Tiny base + linear classifier; 12 ms on modern CPUs; audio-only (no transcript required); v3.1 achieves "dramatic accuracy improvement for English and Spanish"; all weights, training data, and training scripts open-sourced.

**Rasa — `RasaHQ/rasa`:**
> CALM (Conversational AI with Language Models) v3.16 ships Rasa Tools for IDE copilots, built-in CSAT, faster ReAct voice agents, and GPT-5.1/Claude Sonnet 4.5 prompt support — "an engine combining LLM flexibility with business logic enforcement" that separates language from logic where most agents rely on LLMs for everything.

**ParlAI — `facebookresearch/ParlAI`:**
> "A framework for training and evaluating AI models on a variety of openly available dialogue datasets" — now archived (Nov 3, 2023); artefact value only.

**DialoGPT — `microsoft/DialoGPT`:**
> "A State-of-the-Art Large-scale Pretrained Response Generation Model" — "Human evaluation results indicate that response generated from DialoGPT is comparable to human response quality under a single-turn conversation Turing test." Superseded by GODEL.

**SpeechBrain — `speechbrain/speechbrain`:**
> "Open-Source Conversational AI for Everyone" — a PyTorch toolkit spanning ASR, speaker ID, speech enhancement/separation, TTS, spoken language understanding, and chatbot recipes with 200+ competitive training recipes across 40+ datasets.

---

## Patterns

1. **Full-duplex has become the frontier of "human-feeling" voice.** Moshi, LLaMA-Omni, NVIDIA Nemotron 3 VoiceChat, and Pipecat's Speech-to-Speech category all model two simultaneous audio streams (user + agent) rather than strict turns. This eliminates the walkie-talkie feel that classic Whisper→LLM→TTS pipelines have.
2. **Inner monologue as a humanization primitive.** Moshi's "predict time-aligned text tokens alongside audio tokens" pattern is showing up across open-weight speech LLMs (LLaMA-Omni generates text + speech in parallel). The text stream both improves quality and gives a human-readable trace of the model's thinking.
3. **Cascading pipelines are consolidating.** Pipecat and LiveKit Agents have effectively become the "LangChain of voice": both offer pluggable STT/LLM/TTS + WebRTC transport + telephony. Most vertical projects (Bolna, Stimm, Simplismart, theogbrand/fully_oss_realtime_voice_ai) build on one of them rather than rolling their own transport.
4. **Latency is the product.** Every serious 2024–2026 project publishes a concrete latency number: Moshi 200ms, LLaMA-Omni 226ms, XTTSv2 <200ms streaming, Mimi codec 80ms frame. Sub-300ms end-to-end is the implicit human-perception threshold these projects target.
5. **Semantic turn detection is replacing VAD — and now ships open-source.** LiveKit Agents (transformer-based, text-first) and Pipecat Smart-Turn (v3.1, audio-only, 12 ms CPU, 13+ languages) have independently productized semantic end-of-turn as open-source components. These two take opposite approaches — text-semantic vs. audio-prosodic — and are becoming the two community-standard VAD alternatives. Pure amplitude-based VAD is now a "Generation 1" label in practitioner write-ups.
6. **Audio-first LLMs skip the ASR stage.** Ultravox and LLaMA-Omni both remove the transcription bottleneck by projecting audio directly into the LLM's embedding space — preserving prosody, hesitation, and paralinguistic cues that a text-only pipeline discards.
7. **Persona and voice cloning are democratized.** OpenVoice V2, Coqui XTTSv2 (via Idiap fork), and Fish/Kokoro are now standard TTS options in both Pipecat and LiveKit — meaning a consistent "character voice" is no longer vendor-locked.
8. **The symbolic/intent era is winding down but not dead.** Rasa and Botpress are converging on "LLM agents with business-logic guardrails" rather than hand-authored intents. Classic NLU slot-filling is largely being absorbed into LLM function-calling.

## Trends

- **Framework → foundation model → persona-controlled full-duplex.** Mindshare moved from "dialogue managers" (Rasa, ParlAI) to "speech-text foundation models" (Moshi, LLaMA-Omni, Ultravox) and has now reached "open full-duplex models with controllable persona" (NVIDIA PersonaPlex, LLaMA-Omni 2 0.5B–32B, Kyutai MoshiVis). The cycle time is under two years.
- **WebRTC is the default transport.** Daily, LiveKit, and plain Pipecat WebSockets have effectively won over SIP/telephony-first stacks for product work (though Bolna, Vocode, and Pipecat Twilio serializers keep the phone story strong).
- **"Dual-agent" and "background thinking" patterns are emerging.** Stimm's Optimistic VUI, Pipecat Subagents, and LiveKit's multi-agent handoff all express the same idea: one agent owns the conversational surface while others reason in parallel — effectively giving the user the feeling of being "heard immediately" while real work happens behind the scenes.
- **Open weights are closing the gap with proprietary Realtime APIs.** The existence of `fully_oss_realtime_voice_ai` (Whisper + SEA-LIONv2 + XTTS v2 on Pipecat) as a direct stand-in for OpenAI's Realtime API signals commodification of the base stack.

## Gaps

1. **Full-duplex + tool-use gap is narrowing.** NVIDIA PersonaPlex (Jan 2026) and LLaMA-Omni 2 32B (Apr 2025) are the strongest open challengers, but neither yet matches `gpt-realtime`'s MCP server support and function-calling ecosystem. Ultravox v0.7 leads VoiceBench among open models but remains audio-in/text-out only.
2. **Humanness evaluation is ad-hoc.** None of the modern voice frameworks ship an opinionated evaluation harness for "does this feel human?" — LiveKit Agents' built-in test framework with LLM judges is the closest, but it grades task completion, not conversational naturalness.
3. **Persistent memory is bolt-on.** Memory (mem0 in Pipecat, Chroma in RealChar) is plugged in per-project rather than baked into the dialogue stack. For a humanization project, long-term recall + per-user style adaptation is mostly greenfield in open source.
4. **Legacy frameworks that still own "controllable dialogue".** ParlAI's dataset zoo, Rasa's stories/forms, and SpeechBrain's LM training recipes are still uniquely useful for grounded, constrained behavior — but they don't compose cleanly with the new voice stacks.
5. **Cross-cultural / multilingual humanness is thin.** Bolna (Indian languages) is the main player; most Moshi/LLaMA-Omni checkpoints are English-first and lose naturalness in other languages.
6. **"Thinking transparency" is a UX dead zone.** Moshi's inner monologue exists at the model level but is not surfaced in any framework's default UI. For a humanization project this is a notable leverage point.

---

## Sources

- <https://github.com/kyutai-labs/moshi> — Moshi repo (README + model card)
- <https://github.com/pipecat-ai/pipecat> — Pipecat README with full service matrix
- <https://github.com/livekit/agents> — LiveKit Agents README (architecture + examples)
- <https://github.com/fixie-ai/ultravox> — Ultravox repo / Fixie AI
- <https://github.com/RasaHQ/rasa> — Rasa OSS (status + CALM/Hello Rasa direction)
- <https://github.com/facebookresearch/ParlAI> — ParlAI (archived)
- <https://github.com/microsoft/DialoGPT> — DialoGPT (superseded by GODEL)
- <https://github.com/bolna-ai/bolna> — Bolna (Indian-language voice agents)
- <https://github.com/vocodedev/vocode-core> — Vocode (telephony-first LLM agents)
- <https://github.com/Shaunwei/RealChar> — RealChar (persona-first AI companion)
- <https://github.com/speechbrain/speechbrain> — SpeechBrain toolkit
- <https://github.com/botpress/botpress> — Botpress platform
- <https://github.com/NVIDIA/NeMo> — NVIDIA NeMo (Nemotron 3 VoiceChat, MagpieTTS)
- <https://github.com/myshell-ai/OpenVoice> — OpenVoice V2 voice cloning
- <https://github.com/coqui-ai/TTS> + <https://github.com/idiap/coqui-ai-TTS> — Coqui TTS / Idiap fork
- <https://github.com/ictnlp/LLaMA-Omni> — LLaMA-Omni (end-to-end speech LLM)
- <https://github.com/KoljaB/RealtimeSTT> / <https://github.com/KoljaB/RealtimeTTS> — low-latency STT/TTS primitives
- <https://github.com/stimm-ai/stimm> — Stimm (Optimistic VUI)
- <https://github.com/tarun7r/Vocal-Agent> — cascading Whisper + Llama 3.1 + Kokoro reference
- <https://github.com/theogbrand/fully_oss_realtime_voice_ai> — fully OSS OpenAI-Realtime alternative
- <https://github.com/NVIDIA/personaplex> — NVIDIA PersonaPlex (7B full-duplex, Jan 2026)
- <https://github.com/pipecat-ai/smart-turn> — Pipecat Smart-Turn v3.1 (open-source semantic VAD)
- <https://github.com/ictnlp/LLaMA-Omni2> — LLaMA-Omni 2 (0.5B–32B autoregressive streaming, Apr 2025)
- <https://kyutai.org/moshivis> — Kyutai MoshiVis (vision + speech, Jan 2026)
