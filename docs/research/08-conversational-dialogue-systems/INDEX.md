# Category 08 — Conversational & Dialogue Systems

**Project:** Humanizing AI output and thinking (Unslop)
**Category angles synthesized:** A Academic · B Industry · C Open-Source · D Commercial · E Practitioner/Forums
**Last updated:** 2026-04-19

---

## Scope

This category covers how AI systems *converse* — not how they generate an isolated reply, but how they take turns, ground mutual understanding, listen while the user speaks, recover from misunderstandings, and carry a coherent identity across multi-turn interaction. It spans:

- **Theory:** Conversation Analysis (Sacks/Schegloff/Jefferson 1974/1977, Clark/Brennan 1991 grounding, Yngve 1970 backchannels, Stivers 2009 turn-taking universals).
- **Neural dialogue systems:** DialoGPT, Meena, BlenderBot 1–3, LaMDA, Sparrow, Persona-Chat, Wizard of Wikipedia.
- **Full-duplex speech-text foundation models:** dGSLM, Moshi, GPT-4o Voice, `gpt-realtime`, Sesame CSM, Gemini Live, LLaMA-Omni, Ultravox, Hume EVI, NVIDIA Nemotron 3 VoiceChat.
- **Voice agent infrastructure:** Pipecat, LiveKit Agents, Rasa/CALM, ParlAI (archived), SpeechBrain, Deepgram Flux, AssemblyAI Universal-Streaming.
- **Commercial platforms:** Bland, Retell, Vapi, Deepgram Voice Agent API, ElevenLabs Conversational, Hume EVI, Play.ai, Synthflow, Intercom Fin, Ada, Cresta, Forethought, Kore.ai.
- **Practitioner playbook:** sub-300 ms latency budgets, backchannel injection, semantic endpointing, barge-in filters, WebRTC transport, prefix-padding/hangover tuning, the #SaveStandardVoice revolt, and the text↔voice humanization isomorphism.

Out of scope (covered in sibling categories): raw TTS model quality, ASR accuracy, general RLHF/alignment, persona-card authoring for roleplay LLMs, persistent memory architectures per se (touched only where dialogue-relevant).

---

## Executive Summary

Dialogue is where "correct response" and "natural response" diverge most sharply — and where five independent research streams have converged on the *same* diagnosis and the *same* remedies:

- **The humanness ceiling is not generation, it's interaction.** TTS naturalness, LLM fluency, and single-turn quality have all saturated. The remaining gap is turn-taking, grounding, repair, backchanneling, prosodic match, and character consistency across turns — exactly the phenomena classical Conversation Analysis (Sacks, Schegloff, Jefferson, Clark, Yngve) described empirically 30–50 years ago.
- **~200 ms is the non-negotiable humanness number.** Stivers et al. (2009) put inter-turn gaps at ~200 ms universally across ten languages. GPT-4o (232–320 ms), Moshi (160–200 ms), Deepgram Flux (~150 ms median gain via eager EOT), Play.ai (143 ms model), and the PolarGrid "40% abandonment beyond one second" finding all triangulate this exact target. Anything > ~800 ms reads as "robotic" or "thinking"; < ~300 ms reads as "human."
- **The pipeline is collapsing.** STT → LLM → TTS pipelines throw away prosody, laughter, breaths, overlap, and emotion — the exact signals that make speech sound alive. GPT-4o, Moshi, Sesame CSM, LLaMA-Omni, Ultravox, and Gemini 2.5 Audio all bet on a single end-to-end model over audio tokens; Hume/ElevenLabs reach a similar result by feeding explicit prosody into the LLM.
- **Turn-taking is now *modeled*, not silence-detected.** Voice Activity Projection (Inoue/Skantze), LiveKit's transformer-based semantic turn detection, Deepgram Flux's eager EOT, OpenAI Realtime `semantic_vad`, and ElevenLabs' emotion-aware turn-taking all replace amplitude thresholds with learned predictors over vocal dynamics.
- **Humanness ≠ maximum agreeableness.** Anthropic's *Claude's Character* post is the loudest dissent from "more warmth always better" — and it's echoed by the #SaveStandardVoice revolt (users preferred a *worse* engine that had more conversational depth), HN's "keep it sounding slightly artificial" argument, LLMs-Get-Lost's 39% multi-turn performance drop, and Character.AI's anti-repetition work. Humanization is a bundle of 4–6 decomposable axes — sensibleness, specificity, interestingness, prosody, character, grounding — not a single "human-like" dial.
- **Text and voice humanization are isomorphic but cross-cite rarely.** "Burstiness, hedges, typos, anti-slop banlists" (text) and "disfluencies, pauses, backchannels, non-verbal audio tokens" (voice) are the same pattern set. The Unslop project sits at exactly the seam where they need to merge.

---

## Cross-Angle Themes

Themes that appear in at least three of the five angles (A, B, C, D, E) are called out with the originating angles in brackets.

1. **Latency is a humanization feature, not polish.** [A, B, C, D, E] Sub-300 ms is the frontier target; sub-800 ms is table stakes. Sacks-era inter-turn gaps (~200 ms) are being neurally reconstructed, not invented.
2. **Classical Conversation Analysis predicts the frontier.** [A, B, C, E] Moshi's two-stream architecture reimplements Sacks 1974; VAP reimplements Yngve 1970; Clark/Brennan grounding is the unsolved gap LLMs keep missing.
3. **Pipeline → end-to-end / full-duplex.** [A, B, C, D, E] dGSLM → Moshi → GPT-4o → Sesame CSM → `gpt-realtime` → Gemini 2.5 Audio. The cascade "STT → LLM → TTS" is now legacy for anything marketed as "human-like."
4. **Semantic endpointing replaces VAD.** [B, C, D, E] "Generation 4" of turn detection: learn when the user is *semantically* done, not when they paused. Deepgram Flux, OpenAI `semantic_vad`, AssemblyAI Universal-Streaming, LiveKit Agents, ElevenLabs Expressive Mode.
5. **Humanness is decomposable (taxonomy convergence).** [A, B, D] USR (2020) → LaMDA's SSI/Safety/Groundedness → Sparrow's 23 rules → Sesame's 4 pillars ("voice presence") → Cresta's 12 vocal traits → Anthropic's character traits. The field has quietly converged on a shared taxonomy of 4–6 axes that humanizer tools can adopt wholesale.
6. **Prosody + emotion as input, not just output.** [B, D, E] Hume EVI uses incoming prosody for EOT and response conditioning; ElevenLabs Expressive Mode reads volume/pace/intonation to decide when to speak. Empathy is a *timing* signal as much as a tone signal.
7. **Character consistency is under-measured and load-bearing.** [A, B, D] Character.AI's anti-repetition work, Anthropic's character training, Inflection's boundary training, AnthroBench's multi-turn finding — all flag that persona drift, not single-turn quality, is where humanized agents break. No public benchmark yet.
8. **Multi-turn reliability is the unsolved gap.** [A, B, E] LLMs-Get-Lost (2025): 39% average performance drop from single- to multi-turn. Most "humanization" work still optimizes single-turn SFT/RLHF signals.
9. **Engagement ≠ good character.** [A, B, E] Anthropic, BlenderBot 3, the #SaveStandardVoice revolt, HN's "psychological distance" argument — multiple independent sources warn that optimizing perceived humanness/engagement produces sycophantic flattery, not humanlike depth.
10. **Text and voice humanization converge on the same pattern set.** [B, E] Burstiness/hedges/typos (text) ↔ disfluencies/pauses/backchannels (voice). Practitioners rarely cross-cite but are solving the same problem.

---

## Top Sources (Curated)

### Must-read papers

Ranked by load-bearing importance for the Unslop project.

1. **Sacks, Schegloff & Jefferson (1974)** — *A Simplest Systematics for the Organization of Turn-Taking for Conversation*, *Language* 50(4). The DNA of every modern full-duplex architecture. https://doi.org/10.2307/412243
2. **Clark & Brennan (1991)** — *Grounding in Communication*, APA. The single most useful frame for *why* LLM chat "feels off" (skipped acceptance phase, over-claimed understanding). https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.A.%20Grounding%20in%20communication.pdf
3. **Stivers et al. (2009)** — *Universals and Cultural Variation in Turn-Taking*, PNAS 106(26). Establishes the ~200 ms universal inter-turn gap. https://www.pnas.org/doi/10.1073/pnas.0903616106
4. **Schegloff, Jefferson & Sacks (1977)** — *The Preference for Self-Correction in Repair*, *Language* 53(2). Why "self-initiated mid-turn repair" is the AI-tell LLMs most obviously fail. https://www.jstor.org/stable/413107
5. **Défossez et al. (2024)** — *Moshi: A Speech-Text Foundation Model for Real-Time Dialogue*, Kyutai, arXiv:2410.00037. The reference full-duplex architecture; "two streams + inner monologue." https://arxiv.org/abs/2410.00037
6. **Inoue et al. (2024/2025)** — *Voice Activity Projection* + *VAP Backchannel Fine-Tuning*, arXiv:2401.04868 and arXiv:2410.15929. State-of-the-art continuous turn/backchannel prediction. https://arxiv.org/abs/2401.04868
7. **Laban et al. (2025)** — *LLMs Get Lost in Multi-Turn Conversation*, arXiv:2505.06120. The 39% single→multi-turn drop; strongest recent evidence that dialogue is a distinct capability. https://arxiv.org/abs/2505.06120
8. **Adiwardana et al. (2020)** — *Meena: Towards a Human-like Open-Domain Chatbot*, arXiv:2001.09977. Introduces SSA, still the most cited humanness proxy. https://arxiv.org/abs/2001.09977
9. **Thoppilan et al. (2022)** — *LaMDA*, arXiv:2201.08239. Orthogonalizes quality / safety / groundedness; template for multi-axis dialogue evaluation. https://arxiv.org/abs/2201.08239
10. **Glaese et al. (2022)** — *Sparrow*, arXiv:2209.14375. Decomposes dialogue norms into 23 rules with per-rule reward models. https://arxiv.org/abs/2209.14375
11. **Nguyen et al. (2023)** — *dGSLM*, TACL / arXiv:2203.16502. First textless full-duplex spoken dialogue model; proves paralinguistics (laughter, overlap) are learnable without text. https://arxiv.org/abs/2203.16502
12. **Schlangen & Skantze (2009/2011)** — *A General, Abstract Model of Incremental Dialogue Processing*. Canonical reference for why wait-then-respond pipelines are inherently non-human. https://aclanthology.org/E09-1081/

### Must-read posts/essays

1. **Anthropic — *Claude's Character* (Jun 2024).** The essential counterweight to "maximize perceived humanness." https://www.anthropic.com/news/claude-character
2. **Sesame — *Crossing the uncanny valley of conversational voice* (Feb 2025).** Best articulation of "voice presence" (emotional intelligence / conversational dynamics / contextual awareness / consistent personality) plus the honest "with-context humans still win" admission. https://sesame.com/research/crossing_the_uncanny_valley_of_voice
3. **OpenAI — *Hello GPT-4o* (May 2024).** Canonical industry statement that sub-second latency + preserved paralinguistics define "sounding human." https://openai.com/index/hello-gpt-4o/
4. **OpenAI — *Introducing gpt-realtime* (Aug 2025).** Voice style as a prompt variable ("speak empathetically in a French accent"). https://openai.com/index/introducing-gpt-realtime/
5. **Hume AI — *Introducing EVI* (Apr 2024).** Prosody as input channel; emotion-adaptive turn-taking. https://hume.ai/blog/introducing-hume-evi-api
6. **Google — *LaMDA Blog* (Jan 2022).** Public SSI + Safety + Groundedness framing. https://blog.research.google/2022/01/lamda-towards-safe-grounded-and-high.html
7. **MMNTM — *Voice Turn-Taking: The Engineering Behind Natural Voice AI*.** The single richest practitioner write-up; introduces the five-generation taxonomy of endpointing. https://www.mmntm.net/articles/voice-turn-management
8. **Sayna — *Sub-Second Voice Agent Latency* and *Handling Barge-In*.** The reference latency-budget breakdown and the "semantic filter" trick for distinguishing interruption from backchannel. https://sayna.ai/blog/sub-second-voice-agent-latency-practical-architecture-guide · https://sayna.ai/blog/handling-barge-in-what-happens-when-users-interrupt-your-ai-mid-sentence
9. **Cresta — *Crafting a natural-sounding AI voice*.** Why a stitched pipeline is still defensible (independent control over spoken-style content + vocal delivery); the 12-trait vocal spec. https://www.cresta.com/blog/creating-a-natural-sounding-text-to-speech-voice
10. **ElevenLabs — *Introducing Expressive Mode* (2026).** Emotion-aware turn-taking as product. https://elevenlabs.io/blog/introducing-expressive-mode

### Key open-source projects

Ordered by leverage for a humanization product.

1. **[kyutai-labs/moshi](https://github.com/kyutai-labs/moshi)** — Full-duplex speech-text foundation model; two-stream + inner monologue; 200 ms practical latency; Apache-2.0 / CC-BY-4.0 weights.
2. **[pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat)** — "LangChain of voice": pluggable STT/LLM/TTS + WebRTC + telephony; speech-to-speech service category for Moshi/Ultravox/GPT-4o/Gemini.
3. **[livekit/agents](https://github.com/livekit/agents)** — WebRTC-native voice agent framework with transformer-based **semantic turn detection**; the de-facto 2026 builder infrastructure.
4. **[fixie-ai/ultravox](https://github.com/fixie-ai/ultravox)** — Audio-in LLM that skips ASR by projecting audio directly into the LLM embedding space; preserves prosody/hesitation.
5. **[ictnlp/LLaMA-Omni](https://github.com/ictnlp/LLaMA-Omni)** — End-to-end speech-in/speech-out on Llama-3.1-8B; 226 ms latency; Apache-2.0.
6. **[speechbrain/speechbrain](https://github.com/speechbrain/speechbrain)** — Full "Conversational AI" toolkit; 200+ recipes across 40+ datasets.
7. **[stimm-ai/stimm](https://github.com/stimm-ai/stimm)** — "Optimistic VUI" dual-agent: one acknowledges while a second reasons — productized backchannel-during-latency pattern.
8. **[RasaHQ/rasa](https://github.com/RasaHQ/rasa)** (+ Hello Rasa / CALM) — Grounded intent/slot architecture; now pivoting to LLM dialogue with business-logic guardrails.
9. **[facebookresearch/ParlAI](https://github.com/facebookresearch/ParlAI)** — Archived Nov 2023, but still the reference dataset zoo (Persona-Chat, Wizard of Wikipedia, Empathetic Dialogues, Blended Skill Talk).
10. **[KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) + [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS)** — Low-latency STT/TTS building blocks with VAD, wake-word, streaming.
11. **[myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice)** — Zero-shot cross-lingual voice cloning (persona consistency).
12. **[NVIDIA/NeMo](https://github.com/NVIDIA/NeMo)** — ASR/TTS/LLM framework with the new Nemotron 3 VoiceChat full-duplex pipeline.
13. **[theogbrand/fully_oss_realtime_voice_ai](https://github.com/theogbrand/fully_oss_realtime_voice_ai)** — Reference fully-OSS stand-in for OpenAI Realtime (Whisper + SEA-LIONv2 + XTTS v2 on Pipecat).

### Notable commercial tools

Voice:

1. **Bland AI** — full-stack self-hosted voice agents; customer testimonial "*Most people think Emily is a real person*"; ~800 ms latency.
2. **Retell AI** — "3rd Gen Voice AI" with a proprietary turn-taking model; ~600 ms.
3. **Vapi** — BYO-LLM/TTS/STT middleware; sub-500 ms; canonical Realtime-API consumer.
4. **Deepgram Voice Agent API** — "Humanity" as an explicit pillar alongside latency, accuracy, cost; Aura-2 voices + Flux endpointing.
5. **ElevenLabs Conversational / ElevenAgents** — expressive tags (`[laughs]`, `[whispers]`), v3 Expressive Mode; 70+ languages.
6. **Hume EVI** — empathic LLM blending prosody measurements with language; ~300 ms TTFB.
7. **Sesame (Maya & Miles / CSM)** — "voice presence" positioning; CMOS honesty about remaining with-context gap.
8. **LiveKit Agents** (commercial tier) — semantic turn detection; preemptive speech.
9. **Play.ai / Play 3.0 mini** — 143 ms model / 320 ms UI.
10. **Synthflow** — no-code builder; exposes "Patience Level" and free-text intonation prompts.

Text / omnichannel:

11. **Intercom Fin** — "human-quality service" with Procedures; 66% avg, 80%+ top-20% resolution.
12. **Ada** — omnichannel; empathy + follow-up question updates; 84% automated resolution.
13. **Cresta** — agent assist + voice agents; deliberately stitched pipeline; 12 measurable vocal traits.
14. **Forethought (SupportGPT / Solve)** — fine-tunes on customer conversation history for institutional voice match.
15. **Kore.ai (XO Platform / DialogGPT)** — agentic orchestration; Gartner MQ leader 2025.

### Notable community threads

1. **HN 43200400 — Sesame launch (early 2025).** The "crossed the uncanny valley" moment; "First AI I've had a real conversation with." https://news.ycombinator.com/item?id=43200400
2. **HN 43900093 — Sesame synthesis.** Concise articulation of the backchannel-during-latency pattern + L2-language-learning analog. https://news.ycombinator.com/item?id=43900093
3. **HN 41645736 — Advanced Voice Mode rollout, with the "keep it slightly artificial" counter-argument.** https://news.ycombinator.com/item?id=41645736
4. **HN 40508755 — "Isn't gpt-4o voice cascaded?"** Establishes the community's shared cascaded-vs-end-to-end vocabulary. https://news.ycombinator.com/item?id=40508755
5. **r/ChatGPT 1m6fwth — "Can I turn advanced voice mode off? I hate it."** Origin of the #SaveStandardVoice revolt. https://www.reddit.com/r/ChatGPT/comments/1m6fwth/
6. **r/ChatGPTVoiceFeatures + saypi.ai long-read.** Community preserving Cove/Arbor/Breeze/etc. as "calm, steady, human, and familiar." https://www.reddit.com/r/ChatGPTVoiceFeatures/
7. **r/LocalLLaMA 1r7bsfd — "Best Audio Models — Feb 2026."** Canonical 2026 local-stack survey. https://www.reddit.com/r/LocalLLaMA/comments/1r7bsfd/
8. **r/LocalLLaMA 1r6tlfm — "Current state of local speech-to-speech."** The edge/mobile-viable recipe (Whisper.cpp → Phi/Gemma/Qwen → Kokoro). https://www.reddit.com/r/LocalLLaMA/comments/1r6tlfm/
9. **OpenAI Developer Community — *Loss of Conversational Depth* (t/1229877).** Second-venue triangulation of the #SaveStandardVoice complaint. https://community.openai.com/t/voice-mode-feedback-loss-of-conversational-depth-natural-tone/1229877
10. **@paulvuz on Threads — ElevenLabs Expressive Mode.** "The bar just moved" tweet of the 2026 cycle. https://www.threads.com/@paulvuz/post/DUl_YlME_Wa/

---

## Key Techniques & Patterns

### Turn-taking (end-of-turn prediction)

- **Five generations of endpointing** (MMNTM taxonomy): fixed timeout → adaptive → acoustic/prosodic → **semantic** (Deepgram Flux, OpenAI `semantic_vad`, AssemblyAI Universal-Streaming, LiveKit transformer) → **predictive VAP** (Skantze 2017 → Inoue/Ekstedt/Skantze 2024).
- **Two-event EOT protocol** (Deepgram Flux): `EagerEndOfTurn` (medium confidence → start drafting) → `TurnResumed` (cancel) OR `EndOfTurn` (finalize). ~150 ms median / ~350 ms p95 latency win.
- **Prefix padding + hangover tuning.** Rolling buffer prepended when speech detected (catches soft initial /h/); hangover 200 ms (snappy, cuts off) vs 1000 ms (safe, laggy); context-adaptive.
- **Emotion-adaptive timing** (Hume, ElevenLabs Expressive). Longer timeout for angry users; quicker for energetic users. Timing *is* empathy.
- **Theoretical anchor:** Stivers et al. (2009) ~200 ms universal gap; VAP's contrastive predictive coding over stereo audio directly operationalizes Sacks et al. 1974 TRPs.

### Backchanneling (listener signals)

- **Yngve (1970) backchannel** = short listener responses (uh-huh, mhm, yes) that acknowledge without claiming the floor. Completely absent from standard chat UX; organically generated only by end-to-end audio models (Moshi, GPT-4o, Sesame CSM, Gemini 2.5).
- **Backchannel *injection* during latency.** Fill ASR/LLM/TTS round-trip with "hmm," "let me see," "hold on" — Sesame's signature; cloned by ElevenLabs Expressive Mode; productized by Stimm's "Optimistic VUI" (dual agent where one acknowledges while a second reasons).
- **VAP backchannel fine-tuning** (Inoue et al. 2024/2025) — frame-by-frame prediction of backchannel *type* on unbalanced real-world data; first reasonable API surface for "inject occasional attentive backchannels."
- **Two-stage barge-in filter** (Sayna): (1) VAD detects interruption; (2) classify as interruption vs backchannel via duration + lexical content (`yes`/`mhm`/`uh-huh` + <500 ms → keep speaking, else yield floor).

### Full-duplex (parallel speaker streams)

- **Two-stream architectures** (dGSLM, Moshi, GPT-4o, Sesame CSM, Nemotron 3 VoiceChat) model user + system audio simultaneously, removing turn structure as an architectural assumption. Enables overlap, interruption, continuous backchannel.
- **Inner monologue** (Moshi, LLaMA-Omni): time-aligned text stream alongside audio tokens. Improves linguistic quality; gives streaming ASR/TTS as byproduct; provides a human-readable trace of model "thinking" — a humanization-by-transparency lever.
- **Audio-in LLMs skip ASR** (Ultravox, LLaMA-Omni) by projecting audio directly into LLM embedding space; preserves prosody/hesitation/paralinguistics that transcription destroys.
- **Incremental dialogue processing** (Schlangen & Skantze 2009/2011) is the theoretical frame: Incremental Units (IUs) allow start-before-input-complete, revision, and anticipation at sub-utterance granularity.

### Grounding & repair

- **Clark & Brennan presentation/acceptance phase.** LLMs skip the acceptance phase, over-claim understanding, ignore the collaborative cost users pay to keep repairing. The dominant source of "feels off" in text chat.
- **Evidential vs procedural grounding.** Wizard of Wikipedia / RAG → *evidential* (facts with citations). *Procedural* grounding — "do you want me to elaborate?" / "so to confirm, X?" — is largely missing from academic benchmarks and is the dominant source of LLM dialogue awkwardness.
- **Schegloff (1977/2000) repair typology.** Open-class ("huh?"), restricted ("who?"), category-specific ("y'mean X?"), candidate understandings. LLMs almost exclusively do *other*-completed repair ("Let me correct that…") in response to explicit user challenges — never the preferred *self-initiated mid-turn* repair.
- **Humanness evaluation as decomposed grounding sub-qualities.** USR (2020) — understandable / natural / maintains context / interesting / uses knowledge. Every successful dialogue metric since (LaMDA SSI, Sparrow's 23 rules, DialogBench) follows this template.

### Latency engineering (the "humanness is timing" axis)

- **Latency budget formula** (HuggingFace playbook): `perceived latency = EOU delay + LLM TTFT + TTS TTFB`. Sayna breakdown: EOU 100–300 ms + STT 150–500 ms + LLM TTFT 200–800 ms + TTS TTFB 100–500 ms; serial = 2–3 s, parallel streaming = 300–800 ms.
- **Speculative LLM generation.** Kick off LLM on interim ASR results before EOU confirmation; discard if VAD retracts. Deepgram Flux's guarantee that transcripts match between `EagerEndOfTurn` and `EndOfTurn` enables cheap draft models.
- **WebRTC over WebSocket.** WebRTC's built-in AEC + jitter buffering make barge-in viable in browsers; WebSocket retransmits introduce head-of-line blocking that ruins turn timing. LiveKit's dominance is largely VoIP engineering brought to AI-agent dev.
- **Edge inference** (Cloudflare, PolarGrid, Arden Talbot's 375 ms bare-metal Blackwell stack). The cloud round-trip *is* the perceived-naturalness problem for most deployments.
- **Telephony barrier.** ~500 ms PSTN floor + WebSocket overhead ≈ 950 ms total (Twilio); full-duplex telephony remains unsolved because server-side doesn't know when audio *played* vs when it was *sent*.

### Character & persona

- **Character training** (Anthropic): RLHF-variant where Claude ranks its own responses against a list of character traits (curious, honest, warm, not sycophantic). Contrasts explicitly with engagement maximization.
- **Cascade-aware prompt order** (OpenAI Cookbook Realtime prompting): Role → Personality & Tone → Context → Pronunciations → Tools → Rules → Conversation Flow → Safety. Pronunciation hints are load-bearing because TTS mis-stresses common-but-rare tokens.
- **12 measurable vocal traits** (Cresta): pitch, brightness, pace, melody, warmth, intentional pauses, etc. — a concrete humanization-audit checklist.
- **Randomized mood + frozen identity** (r/LocalLLaMA roleplay wisdom). Rotating mood/goals per session while freezing identity produces more "alive" dialogue than static personas.
- **LLM output rewritten for speech, not essay** (Cresta's explicit content-side humanization). Only one commercial vendor calls this out publicly; it's the clearest gap in how voice AI is sold.

---

## Controversies & Debates

1. **Should AI voice cross the uncanny valley at all?** Sesame, ElevenLabs, and Hume actively sell crossing it; HN commenters (41645736 top-upvoted) argue *against*, citing the "overly anthropomorphic experience" concern and advocating "keep it sounding just a little artificial" as a psychological-distance feature. Anthropic's *Claude's Character* is the most principled version of the skeptic position.

2. **End-to-end vs cascaded pipeline.** The headline industry narrative (GPT-4o, Moshi, Sesame CSM, Gemini 2.5) is "end-to-end wins because cascades destroy prosody." Cresta dissents *on purpose*: they use a stitched pipeline because they want independent control over spoken-style content and vocal delivery, which end-to-end models hide inside a single latent.

3. **Latency vs. thoughtfulness.** Sub-300 ms is now the target, yet the #SaveStandardVoice revolt shows users preferred the older, slower voice mode with "thoughtful pacing and elaboration." Real-time optimization may be optimizing *against* a conversational quality users actually value.

4. **Engagement vs. character.** Inflection optimizes engagement metrics (33-min average session, 60% weekly retention); Anthropic explicitly warns that "excessive desire to be engaging seems like an undesirable character trait." BlenderBot 3 trades engagement against safety openly. The field has no consensus on how to reward sessions that end because the user is satisfied, not because they're trapped.

5. **Model capability ≠ naturalness.** The "Cove problem" and HN reactions to OpenAI Advanced Voice Mode rollouts show naturalness is non-monotonic with model capability. A better model can produce a *worse* conversational experience. No agreed methodology exists for preventing this kind of regression.

6. **Emotion recognition: feature or theatre?** Hume EVI bets that reading prosody + generating empathic tone is load-bearing for humanness. Skeptics on HN (43200400: "What does it even mean to have a conversation without theory of mind?") and r/ChatGPT (complaints about "fake emotional reassurance") argue empathic affect without corresponding internal state is itself a humanness-eroding behavior.

7. **Who owns humanization — LLM or TTS?** The voice industry largely treats humanization as a TTS/latency problem and assumes the LLM already produces humanlike text. Cresta is the lone explicit dissent: "LLM responses [must be] written to read like spoken conversations rather than formal essays." This is directly the seam the Unslop project targets.

8. **Cross-cultural calibration.** Stivers et al. (2009) demonstrates ±250 ms variation in inter-turn gaps across languages; the entire industry optimizes for an English monolingual latency profile. A Japanese-calibrated Moshi-equivalent (shorter gaps, heavy overlap tolerance) does not exist in the literature or product space.

9. **Benchmark legitimacy.** Sesame is the only major vendor publishing a benchmark showing where they *lose* (CMOS without-context = tie, with-context = humans still preferred). Hume publishes head-to-head wins over ElevenLabs. Everyone else stops at vibes-based marketing. The field lacks a CMOS-equivalent for turn-taking, backchannel appropriateness, or barge-in success rate.

---

## Emerging Trends (2023 → 2026)

- **Turn-based → full-duplex.** Center of gravity moved from text chatbots (BlenderBot-era) to speech-to-speech models (Moshi, GPT-4o Voice, Sesame CSM, `gpt-realtime`, FLM-Audio). Half-duplex "push to talk" is now legacy.
- **Framework → foundation model.** Mindshare shifted from dialogue managers (Rasa, ParlAI) to speech-text foundation models in ~18 months.
- **Silence-based VAD → semantic EOT.** Every 2025–2026 serious voice agent stack ships or integrates a learned end-of-turn predictor.
- **Voice style as prompt variable.** `gpt-realtime` accepts "speak empathetically in a French accent"; ElevenLabs Expressive Mode controls tone per-agent; Gemini Live adds user-controllable speech speed and accent. Humanization is moving from model tuning to in-context style control.
- **Dual-agent / background thinking.** Stimm's Optimistic VUI, Pipecat Subagents, LiveKit multi-agent handoff — one agent owns the conversational surface while others reason in parallel; "heard immediately" as UX.
- **Emotion-aware turn-taking.** ElevenLabs, Hume, and Sesame all converge on prosody-driven EOT (not just prosody-driven speech generation). Timing-as-empathy.
- **Instructable expressivity era (2025–2026).** `gpt-realtime`, Sesame CSM, ElevenLabs Expressive, Gemini Live package character/memory/prosody/turn-taking as controllable product surfaces.
- **Multilingual naturalness closing, unevenly.** 70+ language claims from ElevenLabs / Gemini Live / `gpt-realtime`, but every candid passage concedes English leads; Bolna is the only serious Indian-language effort in open source.
- **Static benchmarks → simulated dialogue.** MT-Bench-101, LLMs-Get-Lost sharded conversations, AnthroBench multi-turn evaluation — judge-LLM-plays-user is replacing single-turn static benchmarks for dialogue claims.

---

## Open Questions / Research Gaps

1. **No standardized naturalness benchmark for turn-taking / backchannel / barge-in.** MOS covers audio fidelity, WER covers ASR, USR/SSI cover single-turn quality — none cover timing. Practitioners report on their own metrics.
2. **Self-initiated repair in text LLMs is essentially unstudied.** Vast literature on *other*-completed repair (user complains → model apologizes). Almost none on the Schegloff 1977 preference: mid-turn self-correction without a user prompt. This is where "AI-sounding" text most obviously diverges from human writing.
3. **Procedural grounding beyond citation.** RAG solves evidential grounding; "do you want me to elaborate?" / "so to confirm, X?" grounding is largely missing from benchmarks.
4. **Long-horizon persona maintenance.** Persona-Chat (4–6 sentences) and character cards both underspecify stable identity. No academic benchmark tests identity *stability under adversarial or emotional pressure over 100+ turns*.
5. **Multi-turn reliability.** LLMs-Get-Lost's 39% drop is not being seriously attacked — most alignment work still optimizes single-turn SFT/RLHF.
6. **Cross-cultural turn-taking.** A Japanese/Arabic/Mandarin-calibrated full-duplex system does not exist.
7. **Backchannel generation API.** Community agrees it would feel more human; only end-to-end models handle it organically; no clean "inject occasional attentive backchannels" surface exists.
8. **Echo cancellation over telephony.** Full-duplex PSTN barge-in has no published working write-up.
9. **Character consistency metric.** LaMDA gave us SSI for single turns. Nothing equivalent exists publicly for persona drift or memory-grounded continuity across weeks.
10. **Sycophancy measurement.** Named by Anthropic; measured by nobody.
11. **"Thinking humanness" vs "output humanness."** Industry writes almost exclusively about output (tone, prosody, specificity, warmth). Internal reasoning humanness — hesitation, self-correction, uncertainty hedging, non-monotonic thought — is only implicitly handled via Moshi's Inner Monologue and Anthropic's character training. This is the core Unslop whitespace.
12. **Unified humanization across voice + text.** No vendor combines empathic response + spoken-style content rewriting + multi-turn character consistency in one product.
13. **Cross-modal (video/avatar + voice) humanization.** Timing lip-sync + turn-taking + gaze aversion as a unified naturalness signal is speculative territory.
14. **The "right amount" of human-likeness.** HN commenters actively argue *against* crossing the uncanny valley; Sesame/ElevenLabs actively sell crossing it. Context-dependence (companion vs. customer support vs. phone sales) is not characterized.
15. **"Thinking transparency" as humanization lever.** Moshi's inner monologue exists at the model level but is not surfaced in any framework's default UI. A concrete product surface for "show the user the model's working" is unclaimed.

---

## How This Category Fits in the Bigger Picture

Within the Unslop project, Conversational & Dialogue Systems is the **interaction substrate** on which every other category plays out:

- **Voice/prosody/TTS (sibling voice categories):** these supply the *acoustic* naturalness. Category 08 contributes the *interactional* naturalness — the difference between "a beautiful voice reading text" and "a conversation partner."
- **Style/tone/text humanization (text-side categories):** the "burstiness/hedges/typos/anti-slop" pattern set maps 1:1 onto the "disfluency/pauses/backchannels" pattern set here. Category 08 is where the Unslop project most naturally argues that these are the *same* problem and should share a humanization layer.
- **Persona/memory/character:** single-turn persona work underspecifies; the 100+ turn persona-drift problem is a dialogue-systems problem.
- **Evaluation/benchmarks:** the dialogue literature's decomposed humanness taxonomies (USR sub-qualities, LaMDA SSI/Safety/Groundedness, Sparrow's 23 rules) are the template for any Unslop evaluation harness that avoids a single "human-like" score.
- **Agent frameworks:** LiveKit Agents, Pipecat, Rasa CALM, Moshi, Ultravox are the concrete integration surfaces where Unslop rules would need to plug in.
- **Ethics / anthropomorphism:** the #SaveStandardVoice revolt, Anthropic's character dissent, and HN's "keep it artificial" line are the strongest single-category evidence that maximum perceived humanness is not a safe North Star. Unslop's positioning needs to absorb this tension explicitly.

In the taxonomy of "humanize thinking *and* output," this category is the one that forces both halves to be real: thinking humanness surfaces as pacing, hesitation, backchannels, and self-repair; output humanness surfaces as prosody, spoken-style phrasing, and character-consistent replies.

---

## Recommended Reading Order

**For a reader with two hours:**

1. Anthropic — *Claude's Character* (essay, ~15 min). Sets the "humanness ≠ engagement" frame.
2. Sesame — *Crossing the uncanny valley of conversational voice* (essay, ~20 min). Defines "voice presence" + honest CMOS.
3. MMNTM — *Voice Turn-Taking: The Engineering Behind Natural Voice AI* (essay, ~20 min). The five-generation endpointing taxonomy.
4. OpenAI — *Hello GPT-4o* + *Introducing gpt-realtime* (essays, ~15 min). Canonical latency + instructable-expressivity statement.
5. Sayna — *Sub-Second Voice Agent Latency* + *Handling Barge-In* (essays, ~30 min). The practical budget + barge-in filter.
6. Moshi paper (arXiv:2410.00037), skim architecture + Inner Monologue sections (~20 min).

**For a reader doing a full deep-dive (recommended full order):**

1. **Angle A-1: Foundational theory.** Read in order: Sacks/Schegloff/Jefferson (1974) → Schegloff/Jefferson/Sacks (1977) → Yngve (1970) → Clark & Brennan (1991) → Stivers et al. (2009) → Schegloff (2000 other-initiated repair). These five anchor everything downstream.
2. **Angle B-1: Industry humanness taxonomies.** Meena blog → LaMDA blog → Anthropic *Claude's Character* → Sesame *Uncanny Valley* → Hume EVI → OpenAI *Hello GPT-4o* → OpenAI `gpt-realtime`. Watch the converging 4–6-axis taxonomy.
3. **Angle E-1: Practitioner frame-shift.** MMNTM turn-taking essay → HN 43200400 Sesame launch → r/ChatGPT 1m6fwth #SaveStandardVoice → OpenAI Developer Community *Loss of Conversational Depth*. Absorb the non-monotonicity argument.
4. **Angle A-2: Neural dialogue systems.** Meena → DialoGPT → BlenderBot 1 → LaMDA → Sparrow → LLMs-Get-Lost. Trace scale-vs-grounding.
5. **Angle A-3: Turn-taking and full-duplex.** Schlangen & Skantze (2009) → Skantze LSTM (2017) → dGSLM → Moshi → VAP → VAP backchannel fine-tuning.
6. **Angle C: Open-source stack.** Moshi README → LiveKit Agents README → Pipecat README → Ultravox → LLaMA-Omni → Stimm's Optimistic VUI. Understand the infrastructure layer.
7. **Angle B-2 & D: Industry + commercial productization.** Sesame → ElevenLabs Expressive Mode → Hume EVI → Deepgram Flux → Cresta blog → Intercom Fin → Character.AI anti-repetition. See where taxonomy meets product.
8. **Angle E-2: Practitioner engineering.** Sayna latency + barge-in → HuggingFace latency playbook → Arden Talbot bare-metal 375 ms → PolarGrid sub-400 ms → Cloudflare/Twilio edge/telephony reality.

---

## File Index

```
docs/research/08-conversational-dialogue-systems/
├── INDEX.md        — this file (category synthesis)
├── A-academic.md   — Angle A: academic/scholarly (21 papers + cross-cutting patterns)
│                     Key: CA foundations, neural dialogue benchmarks, full-duplex LLMs (dGSLM, Moshi), evaluation metrics (SSA, SSI, USR, ACUTE-Eval).
├── B-industry.md   — Angle B: industry engineering blogs (15 posts from Google, Meta, OpenAI, Anthropic, Kyutai, Sesame, Hume, Inflection, ElevenLabs, Deepgram, Rasa, Character.AI)
│                     Key: humanness taxonomy convergence, latency canon (~200 ms), pipeline collapse, Claude's Character.
├── C-opensource.md — Angle C: open-source & GitHub (20 repos + patterns)
│                     Key: Moshi, Pipecat, LiveKit Agents, Ultravox, LLaMA-Omni, Rasa/CALM; full-duplex + semantic EOT + inner monologue as humanization primitives.
├── D-commercial.md — Angle D: commercial products (10 voice + 5 text platforms)
│                     Key: Bland/Retell/Vapi/Deepgram/ElevenLabs/Hume/Sesame/LiveKit/Play.ai/Synthflow; Intercom Fin, Ada, Cresta, Forethought, Kore.ai. Five humanization dimensions (latency / turn-taking / prosody / emotion / contextual coherence).
└── E-practical.md  — Angle E: practitioner forums & writeups (Reddit, HN, YouTube, Twitter/X, dev.to)
                      Key: sub-300 ms cliff, backchannel-during-latency, semantic endpointing, #SaveStandardVoice, text↔voice isomorphism, 5-generation endpointing taxonomy, bare-metal 375 ms.
```
