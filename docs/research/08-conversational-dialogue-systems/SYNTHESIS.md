# Category 08 — Conversational Dialogue Systems

## Scope

This category covers how AI systems *converse* rather than generate a single isolated reply. The subject is the machinery of interaction: turn-taking, grounding, listener signals (backchanneling), repair, prosody, and multi-turn character consistency. It spans foundational Conversation Analysis theory from the 1970s–1990s (Sacks/Schegloff/Jefferson, Clark/Brennan, Yngve, Stivers) through the neural dialogue benchmarks of 2018–2022 (Meena, LaMDA, BlenderBot, Sparrow) to 2024–2026 full-duplex speech LLMs (dGSLM, Moshi, GPT-4o Voice, Sesame CSM, LLaMA-Omni) and the commercial voice-agent market that has grown up around them. Out of scope: raw TTS model quality, ASR accuracy, general RLHF/alignment, persistent memory architectures per se, and persona-card authoring for roleplay LLMs — these are touched only where they directly affect dialogue interaction.

## Executive Summary

- TTS naturalness, LLM fluency, and single-turn quality have all saturated. The remaining humanness gap is in the interactional layer: turn-taking, grounding, repair, backchanneling, prosodic match, and character consistency across turns. These are exactly the phenomena Conversation Analysis described empirically 30–50 years ago. (A)
- ~200 ms is the empirically grounded humanness target for inter-turn latency. Stivers et al. (2009) found this gap universal across 10 languages. GPT-4o averages 232–320 ms, Moshi achieves 160–200 ms practically, Deepgram Flux's eager EOT gains ~150 ms median, and PolarGrid data shows 40% higher abandonment beyond one second. (A, B, D, E)
- The STT → LLM → TTS pipeline is losing ground because it discards prosody, laughter, breaths, overlap, and emotion. GPT-4o, Moshi, Sesame CSM, LLaMA-Omni, Ultravox, and Gemini 2.5 Audio bet on end-to-end audio-token models. Hume EVI and ElevenLabs reach the same result via an explicit prosody input channel. (A, B, C, D, E)
- Turn-taking is now modeled, not silence-detected. Voice Activity Projection (Inoue/Skantze), LiveKit's transformer-based semantic turn detection, Deepgram Flux's `EagerEndOfTurn` protocol, OpenAI Realtime `semantic_vad`, and ElevenLabs Expressive Mode all replace amplitude thresholds with learned predictors over vocal dynamics. (B, C, D, E)
- Humanness is not a single dial. It decomposes into 4–6 measurable axes. Meena introduced SSA (sensibleness + specificity), LaMDA extended it to SSI + Safety + Groundedness, Sesame articulates "voice presence" as four pillars, Cresta specifies 12 measurable vocal traits, and Sparrow operationalizes 23 dialogue rules. The industry has converged on this taxonomy without coordinating on it. (A, B, D)
- Humanness is not maximum agreeableness. Anthropic's *Claude's Character* post is the clearest statement: "an excessive desire to be engaging seems like an undesirable character trait." The #SaveStandardVoice revolt (users preferring an older, lower-quality voice model that had conversational depth over a technically superior one that felt flat) and LLMs-Get-Lost's 39% multi-turn performance drop both reinforce this from different directions. (A, B, E)
- Text-side and voice-side humanization are structurally identical but rarely cross-cited. Burstiness, hedges, and anti-slop banlists (text) map directly onto disfluencies, pauses, and backchannel injection (voice). The Unslop project sits at the exact seam where these need to merge. (B, E)
- Multi-turn reliability is the field's open wound. Most alignment and humanization work still optimizes single-turn SFT/RLHF signals. LLMs-Get-Lost (2025) documented a mean 39% performance drop across 200,000+ simulated multi-turn conversations across 15+ frontier LLMs. The "Beyond Single-Turn" survey (April 2025, arXiv:2504.04717) confirmed this is the consensus open problem, and the NeurIPS 2025 Workshop on Multi-Turn Interactions was dedicated to it. (A, E)
- Sycophancy is now being measured, not just named. SycEval (AAAI 2025) reports 58% sycophancy rate across models. TRUTH DECAY benchmarks multi-turn sycophancy specifically. BrokenMath (Oct 2025) finds 29% sycophancy in GPT-5 on theorem proving. The measurement gap is closing; the product-incentive misalignment remains. (A, B, E)
- Persona drift is empirically documented for the first time. 2025 benchmarks show >30% degradation in persona self-consistency metrics after 8–12 turns even with context intact. RMTBench (80 characters, 8,000+ dialogue rounds) provides the first large-scale test. HAL (arXiv:2601.02813) offers an alignment path using interpretable traits derived from Turing test transcripts. (A, B, D)

## Cross-Angle Themes

Themes that appear in two or more angles.

**1. Latency is a humanization feature.** (A, B, C, D, E)
All five angles independently land on ~200–300 ms as the perceptual threshold. The academic anchor is Stivers et al. (2009). The product anchors are GPT-4o (232–320 ms), Moshi (160–200 ms), Play.ai (143 ms model latency), and Deepgram Flux (~150 ms median gain). The practitioner anchor is PolarGrid's "40% higher abandonment beyond one second." Sub-300 ms is the current frontier; sub-800 ms is now table stakes.

**2. Classical Conversation Analysis predicts the frontier.** (A, B, C, E)
Moshi's two-stream architecture is a neural implementation of Sacks et al. (1974) overlapping talk. VAP's continuous turn prediction operationalizes Yngve (1970). dGSLM's paralinguistic learning reimplements the "simultaneous both-speakers" structure Yngve used to justify the backchannel term. Clark & Brennan's (1991) presentation/acceptance grounding cycle is the unsolved gap LLMs keep missing. The academic literature from 1970–1991 is not background — it is a specification sheet.

**3. Pipeline collapse toward full-duplex.** (A, B, C, D, E)
The cascade "STT → LLM → TTS" is now legacy for anything marketed as human-like. The progression is: dGSLM (2023) → Moshi (2024) → SyncLLM/EMNLP 2024 → GPT-4o (2024) → Sesame CSM (2025) → `gpt-realtime` (2025) → Gemini 2.5 Flash Native Audio (2025) → NVIDIA PersonaPlex (Jan 2026) → DuplexCascade (Mar 2026). The DuplexCascade paper (arXiv:2603.09180) is notable: it shows a VAD-free cascaded pipeline achieving full-duplex behavior via micro-turn chunking, suggesting the end-to-end vs. cascaded debate is more nuanced than "end-to-end always wins." Cresta remains the deliberate enterprise outlier: stitched pipeline for independent content/voice control.

**4. Semantic endpointing replaces VAD — and two open-source implementations now exist.** (B, C, D, E)
"Generation 4" of turn detection (MMNTM taxonomy): predict when the user is semantically done, not when they paused. Commercial: Deepgram Flux `EagerEndOfTurn`, OpenAI Realtime `semantic_vad`, AssemblyAI Universal-Streaming, ElevenLabs Expressive Mode (emotion-conditioned timing). Open-source: LiveKit Agents' transformer-based semantic turn detector (text-first) and Pipecat Smart-Turn v3.1 (audio-only, Whisper Tiny base, 12 ms CPU, 13+ languages). These two open-source implementations take fundamentally different signal paths and are becoming the two community-standard semantic VAD alternatives.

**5. Humanness taxonomy convergence.** (A, B, D)
USR (2020) decomposed "naturalness" into: understandable, natural, maintains context, interesting, uses knowledge. LaMDA split quality into SSI (sensibleness + specificity + interestingness), plus Safety and Groundedness as orthogonal. Sesame's "voice presence" has four pillars: emotional intelligence, conversational dynamics, contextual awareness, consistent personality. Cresta specifies 12 vocal traits. Sparrow's 23 rules. Anthropic's character traits. The field has independently converged on a 4–6-axis decomposition that humanizer tools can adopt wholesale.

**6. Prosody as input, not just output.** (B, D, E)
Hume EVI measures tune/rhythm/timbre from incoming audio to condition both EOT detection and response tone. ElevenLabs Expressive Mode reads volume/pace/intonation to decide when to speak and what emotional register to use. Deepgram Flux's semantic VAD reads prosodic completion signals. Empathy is a timing decision as much as a language decision.

**7. Character consistency is under-measured and load-bearing.** (A, B, D)
Character.AI reduced unnecessary repetition by ~30% with a model update; their post frames persona maintenance as "clearly defined identity, tone, behavior, and constraints." AnthroBench finds anthropomorphic behaviors emerge only after multiple turns, making single-turn benchmarks structurally blind to this. Anthropic's character training and Inflection's boundary training both target it. No public benchmark for persona drift over 100+ turns exists.

**8. Multi-turn reliability is the unsolved gap — now with a survey and alignment proposals.** (A, B, E)
Laban et al. (2025) simulated 200,000+ multi-turn conversations across 15+ frontier LLMs and found a mean 39% performance drop from single-turn to "sharded" multi-turn tasks. The gap decomposes into small aptitude loss and large unreliability gain: models commit early, cannot recover, and contaminate context with their own earlier errors. The "Beyond Single-Turn" survey (arXiv:2504.04717, April 2025) confirms this is the field's consensus open problem; the NeurIPS 2025 Workshop on Multi-Turn Interactions was dedicated to it. HAL (arXiv:2601.02813) provides the first publicly reproducible alignment method targeting human-likeness at the multi-turn level via interpretable trait-based DPO. Most commercial and humanization work still does not address this gap.

**9. Engagement optimization produces sycophancy — now measurable.** (A, B, E)
Anthropic warns that "excessive desire to be engaging seems like an undesirable character trait." BlenderBot 3 explicitly trades engagingness against safety. The #SaveStandardVoice revolt shows users preferring a worse model with better conversational character. HN commenters argue for deliberate mild artificiality as a psychological-distance feature. The measurement gap is now closing: SycEval (AAAI 2025) reports 58% sycophancy across tested LLMs; TRUTH DECAY benchmarks multi-turn sycophancy; BrokenMath finds 29% sycophancy even in GPT-5. The product-incentive misalignment (engagement metrics reward sycophancy) remains unaddressed by any commercial product.

**10. Text and voice humanization are isomorphic.** (B, E)
Burstiness/hedges/typos/anti-slop banlists (text) and disfluencies/pauses/backchannels/non-verbal audio tokens (voice) are the same pattern set applied to different modalities. Practitioners in neither camp cite the other camp's work, but the failure modes and fixes are structurally identical.

## Top Sources

### Must-read papers

1. Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). "A Simplest Systematics for the Organization of Turn-Taking for Conversation." *Language*, 50(4), 696–735. https://doi.org/10.2307/412243
2. Clark, H. H., & Brennan, S. E. (1991). "Grounding in Communication." In Resnick, Levine & Teasley (eds.), *Perspectives on Socially Shared Cognition*, APA. https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.A.%20Grounding%20in%20communication.pdf
3. Stivers, T., Enfield, N. J., et al. (2009). "Universals and Cultural Variation in Turn-Taking in Conversation." *PNAS*, 106(26), 10587–10592. https://www.pnas.org/doi/10.1073/pnas.0903616106
4. Schegloff, E. A., Jefferson, G., & Sacks, H. (1977). "The Preference for Self-Correction in the Organization of Repair in Conversation." *Language*, 53(2), 361–382. https://www.jstor.org/stable/413107
5. Défossez, A., et al. (2024). "Moshi: A Speech-Text Foundation Model for Real-Time Dialogue." Kyutai, arXiv:2410.00037. https://arxiv.org/abs/2410.00037
6. Inoue, K., Jiang, B., Ekstedt, E., Kawahara, T., & Skantze, G. (2024/2025). VAP real-time turn-taking (arXiv:2401.04868) + VAP backchannel fine-tuning (arXiv:2410.15929). https://arxiv.org/abs/2401.04868
7. Laban, P., et al. (2025). "LLMs Get Lost in Multi-Turn Conversation." arXiv:2505.06120. https://arxiv.org/abs/2505.06120
8. Adiwardana, D., et al. (2020). "Towards a Human-like Open-Domain Chatbot." arXiv:2001.09977. https://arxiv.org/abs/2001.09977
9. Thoppilan, R., et al. (2022). "LaMDA: Language Models for Dialog Applications." arXiv:2201.08239. https://arxiv.org/abs/2201.08239
10. Glaese, A., et al. (2022). "Improving Alignment of Dialogue Agents via Targeted Human Judgements." (Sparrow) arXiv:2209.14375. https://arxiv.org/abs/2209.14375
11. Nguyen, T. A., et al. (2023). "Generative Spoken Dialogue Language Modeling." (dGSLM) *TACL*, arXiv:2203.16502. https://arxiv.org/abs/2203.16502
12. Schlangen, D., & Skantze, G. (2009/2011). "A General, Abstract Model of Incremental Dialogue Processing." *EACL* / *Dialogue & Discourse*, 2(1). https://aclanthology.org/E09-1081/
13. Défossez et al. / Meta AI & UW (2024). "Beyond Turn-Based Interfaces: Synchronous LLMs as Full-Duplex Dialogue Agents." (SyncLLM) *EMNLP 2024*. arXiv:2409.15594. https://arxiv.org/abs/2409.15594
14. (Survey) "From Turn-Taking to Synchronous Dialogue: A Survey of Full-Duplex Spoken Language Models." arXiv:2509.14515, September 2025. https://arxiv.org/abs/2509.14515
15. (Survey) Li, Y., et al. (2025). "Beyond Single-Turn: A Survey on Multi-Turn Interactions with Large Language Models." arXiv:2504.04717. https://arxiv.org/abs/2504.04717
16. Hasan, M., Zhao, J., et al. (2026). "HAL: Inducing Human-likeness in LLMs with Alignment." arXiv:2601.02813. https://arxiv.org/abs/2601.02813

### Key essays and posts

1. Anthropic — "Claude's Character" (Jun 2024). The essential counterweight to "maximize humanness." https://www.anthropic.com/news/claude-character
2. Sesame — "Crossing the uncanny valley of conversational voice" (Feb 2025). Best articulation of "voice presence" + honest CMOS result (humans still preferred with context). https://sesame.com/research/crossing_the_uncanny_valley_of_voice
3. MMNTM — "Voice Turn-Taking: The Engineering Behind Natural Voice AI." The single richest practitioner write-up; introduces the five-generation endpointing taxonomy. https://www.mmntm.net/articles/voice-turn-management
4. OpenAI — "Hello GPT-4o" (May 2024). Canonical statement that sub-second latency + paralinguistics define "sounding human." https://openai.com/index/hello-gpt-4o/
5. OpenAI — "Introducing gpt-realtime" (Aug 2025). Voice style as a prompt variable. https://openai.com/index/introducing-gpt-realtime/
6. Hume AI — "Introducing EVI" (Apr 2024). Prosody as input channel; emotion-adaptive turn-taking. https://hume.ai/blog/introducing-hume-evi-api
7. Sayna — "Sub-Second Voice Agent Latency" + "Handling Barge-In." Latency budget breakdown and the semantic filter for distinguishing interruption from backchannel. https://sayna.ai/blog/sub-second-voice-agent-latency-practical-architecture-guide
8. Cresta — "Crafting a natural-sounding AI voice." Why a stitched pipeline is defensible; the 12-trait vocal spec; and the explicit call to rewrite LLM output for speech, not essays. https://www.cresta.com/blog/creating-a-natural-sounding-text-to-speech-voice

### Key OSS projects

1. [kyutai-labs/moshi](https://github.com/kyutai-labs/moshi) (~9.9k stars) — Full-duplex speech-text foundation model; two parallel audio streams + inner monologue; 200 ms practical latency; MIT/Apache-2.0. Weights updated Dec 2025; MoshiVis (vision+speech) Jan 2026.
2. [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) (~11k stars) — "LangChain of voice"; pluggable STT/LLM/TTS + WebRTC + telephony; speech-to-speech service category; 230+ contributors.
3. [livekit/agents](https://github.com/livekit/agents) (~10k stars) — WebRTC-native agent framework with transformer-based semantic turn detection (text-first); de-facto 2026 infrastructure layer.
4. [fixie-ai/ultravox](https://github.com/fixie-ai/ultravox) (~4.4k stars) — Audio-in LLM; v0.7 (Dec 2025, GLM 4.6 base) leads VoiceBench among all open speech models including with reasoning.
5. [ictnlp/LLaMA-Omni2](https://github.com/ictnlp/LLaMA-Omni2) — 0.5B–32B series (Qwen2.5 backbone); autoregressive streaming decoder; ACL 2025 main; 0.5B enables on-device deployment.
6. [NVIDIA/personaplex](https://github.com/NVIDIA/personaplex) — 7B full-duplex model; ~170 ms latency; text role prompt + audio voice conditioning as independent axes; MIT License; Jan 2026.
7. [pipecat-ai/smart-turn](https://github.com/pipecat-ai/smart-turn) — Open-source audio-only semantic VAD (Whisper Tiny base, 8M params); v3.1 achieves 12 ms CPU inference; 13+ languages; full weights + training data + training script open-sourced.
8. [stimm-ai/stimm](https://github.com/stimm-ai/stimm) — "Optimistic VUI": one agent acknowledges immediately while a second reasons in background.
9. [facebookresearch/ParlAI](https://github.com/facebookresearch/ParlAI) (~10.6k stars) — Archived Nov 2023; remains the reference dataset zoo (Persona-Chat, Wizard of Wikipedia, Empathetic Dialogues).
10. [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) (~11.4k stars) — Full toolkit spanning ASR/TTS/LLM with 200+ competitive recipes across 40+ datasets.

### Notable commercial tools

Voice: Bland AI (~800 ms, full self-hosted stack), Retell AI (~600 ms, proprietary turn-taking model), Vapi (BYO-model, sub-500 ms), Deepgram Voice Agent API (Aura-2 + Flux, sub-200 ms streaming, "humanity" as explicit pillar), ElevenLabs Conversational/ElevenAgents (Expressive Mode, 70+ languages), Hume EVI (~300 ms TTFB, empathic LLM blending prosody), Sesame Maya/Miles (CMOS-honest, "voice presence" framing), Play.ai (143 ms model / 320 ms UI), Synthflow (no-code, "Patience Level" control).

Text/omnichannel: Intercom Fin (66% avg resolution, "human-quality service" claim), Ada (84% automated resolution, empathy + follow-up updates), Cresta (12 measurable vocal traits, explicit content-side spoken-style rewriting), Forethought/SupportGPT (fine-tunes on customer conversation history), Kore.ai XO/DialogGPT (Gartner MQ leader 2025).

### Notable community threads

- HN 43200400 (Sesame launch): "First AI I've had a real conversation with." https://news.ycombinator.com/item?id=43200400
- HN 43900093 (Sesame synthesis): Concise backchannel-during-latency explanation + Japanese L2 learning analog. https://news.ycombinator.com/item?id=43900093
- HN 41645736 (Advanced Voice Mode, "keep it slightly artificial" argument). https://news.ycombinator.com/item?id=41645736
- r/ChatGPT 1m6fwth ("#SaveStandardVoice" origin thread). https://www.reddit.com/r/ChatGPT/comments/1m6fwth/
- r/LocalLLaMA 1r7bsfd ("Best Audio Models — Feb 2026", canonical local-stack survey). https://www.reddit.com/r/LocalLLaMA/comments/1r7bsfd/
- OpenAI Developer Community t/1229877 ("Loss of Conversational Depth"). https://community.openai.com/t/voice-mode-feedback-loss-of-conversational-depth-natural-tone/1229877

## Key Techniques & Patterns

1. **Five-generation endpointing taxonomy** (MMNTM): fixed timeout → adaptive → acoustic/prosodic → semantic (Deepgram Flux, OpenAI `semantic_vad`, AssemblyAI Universal-Streaming, LiveKit transformer) → predictive VAP (Skantze 2017, Inoue et al. 2024).
2. **Two-event EOT protocol** (Deepgram Flux): `EagerEndOfTurn` fires at medium confidence, kicking off speculative LLM generation; `TurnResumed` cancels if the user keeps speaking; `EndOfTurn` confirms. ~150 ms median / ~350 ms p95 latency gain.
3. **Backchannel injection during latency**: fill the ASR/LLM/TTS round-trip with "hmm," "let me see," "hold on" — Sesame's signature, productized by Stimm's Optimistic VUI (dual-agent: one acknowledges while a second reasons), cloned by ElevenLabs Expressive Mode.
4. **Two-stage barge-in filter** (Sayna): (1) VAD detects speech; (2) classify as real interruption vs backchannel via duration + lexical content — `yes`/`mhm`/`uh-huh` plus under 500 ms → keep speaking, else yield the floor.
5. **Two-stream full-duplex architecture** (dGSLM, Moshi, GPT-4o, Sesame CSM, Nemotron 3 VoiceChat): model user and system audio simultaneously, removing turn structure as an architectural assumption. Enables overlapping speech and continuous backchanneling.
6. **Inner monologue** (Moshi, LLaMA-Omni): a time-aligned text stream predicted alongside audio tokens. Improves linguistic quality and provides a human-readable trace of the model's reasoning — a humanization-by-transparency lever that no framework currently exposes in its default UI.
7. **Audio-in LLMs skip ASR** (Ultravox, LLaMA-Omni): project audio directly into LLM embedding space, preserving prosody, hesitation, and paralinguistics that transcription discards.
8. **Incremental dialogue processing** (Schlangen & Skantze 2009/2011): Incremental Units (IUs) allow start-before-input-complete, revision, and anticipation at sub-utterance granularity. The theoretical framework for why wait-then-respond pipelines are inherently non-human.
9. **Speculative LLM generation**: kick off generation on interim ASR transcripts before end-of-utterance is confirmed; discard if VAD later retracts. Deepgram Flux's transcript-match guarantee between `EagerEndOfTurn` and `EndOfTurn` makes cheap draft models viable.
10. **WebRTC over WebSocket**: WebRTC's built-in acoustic echo cancellation and jitter buffering make barge-in viable in browsers. WebSocket retransmits introduce head-of-line blocking that destroys turn timing. LiveKit's dominance is partly decades of VoIP engineering applied to AI-agent dev.
11. **Emotion-adaptive timing** (Hume EVI, ElevenLabs Expressive): longer timeout for angry or distressed users; quicker response for energetic users. The timing decision itself encodes empathy, not just the language.
12. **Cascade-aware prompt order** (OpenAI Cookbook Realtime prompting): Role → Personality & Tone → Context → Pronunciations → Tools → Rules → Conversation Flow → Safety. Pronunciation hints are load-bearing because TTS mis-stresses common-but-rare tokens.
13. **Randomized mood + frozen identity** (r/LocalLLaMA roleplay practice): rotating mood/goals per session while freezing identity produces more alive-feeling dialogue than static personas. Direct analog for voice-agent persona design.
14. **Evidential vs procedural grounding** (Clark & Brennan): RAG addresses evidential grounding (facts with citations). Procedural grounding — "do you want me to elaborate?" / "so to confirm, X?" — is largely absent from academic benchmarks and is the dominant source of text-LLM dialogue awkwardness.
15. **Self-initiated vs other-completed repair** (Schegloff 1977): LLMs almost exclusively perform other-completed repair (user challenges → model apologizes). The strongly preferred human pattern — self-initiated mid-turn correction before any user challenge — is essentially absent from any current LLM and is a major "AI tell" in written output.

## Controversies & Debates

**Should AI voice cross the uncanny valley at all?** Sesame, ElevenLabs, and Hume actively sell crossing it. HN thread 41645736's top-upvoted comment argues against, citing the "overly anthropomorphic experience" concern and advocating deliberate mild artificiality as a psychological-distance feature. Anthropic's *Claude's Character* is the most principled version of the skeptic position. r/ChatGPT users explicitly complain about "fake emotional reassurance" and "unsolicited hugs." The debate is not resolved, and context matters enormously (companion vs. customer support vs. phone sales).

**End-to-end vs cascaded pipeline.** The headline industry narrative is "end-to-end wins because cascades destroy prosody." Cresta dissents on purpose: they use a stitched pipeline to get independent control over spoken-style content and vocal delivery, which end-to-end models hide inside a single latent space. Both positions are defensible for different use cases.

**Latency vs thoughtfulness.** Sub-300 ms is the current frontier target, but the #SaveStandardVoice movement shows users preferred an older, slower voice mode with "thoughtful pacing and elaboration." Real-time optimization may actively trade away a conversational quality users value — and there is no agreed methodology for detecting or preventing this regression.

**Model capability does not equal naturalness.** The "Cove problem" (users preferred the original lower-quality voices with better conversational character over GPT-4o's higher-capability Advanced Voice Mode) and the OpenAI Developer Community threads documenting jarring mid-session shifts from "conversational" to "cold, robotic" mode both show naturalness is non-monotonic with model capability. This is an empirical finding without a clear fix.

**Engagement vs character.** Inflection reports 33-minute average sessions and 60% weekly retention as success metrics. Anthropic says "excessive desire to be engaging seems like an undesirable character trait." BlenderBot 3 explicitly acknowledges trading engagingness against safety. The field has no shared approach to rewarding sessions that end because the user is *satisfied*, rather than because they're retained.

**Emotion: feature or theater?** Hume EVI bets that reading prosody and generating an empathic tone is load-bearing for humanness. r/ChatGPT complaints about "fake emotional reassurance" and the HN counter-question "What does it even mean to have a conversation without theory of mind?" argue the opposite: empathic affect without a corresponding internal state is itself a humanness-eroding signal.

**Who owns humanization — LLM or TTS?** The commercial voice market largely treats humanization as a TTS and latency problem, assuming the LLM already produces humanlike text. Cresta is the only vendor to explicitly dissent, requiring LLM output to be "written to read like spoken conversations rather than formal essays." This is the exact seam the Unslop project targets — and D is thinner than expected on this point.

**Cross-cultural calibration.** Stivers et al. (2009) shows ±250 ms variation in inter-turn gaps across 10 languages. The entire industry optimizes for English-monolingual latency profiles. A Japanese-calibrated full-duplex system (shorter gaps, heavier overlap tolerance) does not exist in the literature or the product market.

## Emerging Trends

- Turn-based chat → full-duplex voice. Center of gravity moved from BlenderBot-era text chatbots to speech-to-speech models in roughly 18 months (2023–2024). Half-duplex "push to talk" is now a legacy pattern.
- Dialogue managers → foundation models → persona-controlled full-duplex. Rasa and ParlAI were the default building blocks in 2022. Moshi, LLaMA-Omni, Ultravox replaced them as mindshare leaders. NVIDIA PersonaPlex (Jan 2026) marks the next step: open full-duplex models with independent persona control (text role prompt + audio voice conditioning). Rasa CALM (Spring 2026) is the deliberate counter-trend for enterprise regulated deployments.
- VAD → semantic EOT — now open-source. Every serious 2025–2026 voice agent stack ships a learned end-of-turn predictor. Two open-source options now exist: LiveKit Agents (text-semantic) and Pipecat Smart-Turn v3.1 (audio-prosodic, 12 ms CPU). Fixed silence thresholds are "Generation 1."
- Voice style as prompt variable. `gpt-realtime` accepts "speak empathetically in a French accent"; ElevenLabs Expressive Mode controls tone per agent; Gemini 2.5 Flash Native Audio adds user-controllable speech speed; NVIDIA PersonaPlex separates voice identity (audio conditioning) from role identity (text prompt). Humanization is shifting from model tuning to in-context style control.
- Dual-agent / background thinking. Stimm's Optimistic VUI, Pipecat Subagents, LiveKit multi-agent handoff: one agent owns the conversational surface, others reason in parallel, giving users the feeling of being heard immediately.
- Emotion-aware turn-taking. Hume EVI 3 (May 2025) extends per-response emotion matching to *continuous session-level emotional adaptation*. ElevenLabs and Sesame have converged on prosody-driven EOT timing. The timing decision is now framed as empathy, not just latency optimization.
- Instructable-expressivity era (2025–2026). Character, memory, prosody, and turn-taking are packaged as controllable product surfaces across `gpt-realtime`, Sesame CSM, ElevenLabs Expressive, Gemini 2.5 Flash Native Audio, and NVIDIA PersonaPlex.
- Multilingual naturalness closing unevenly. ElevenLabs, Gemini 2.5, and Pipecat Smart-Turn v3.1 (13+ languages) all make multilingual claims, but every candid source concedes English leads; Bolna remains the only serious Indian-language open-source effort. Arabic/CJK/Indic voice-agent naturalness remains thin in practitioner literature.
- Static benchmarks → simulated multi-turn evaluation. LLMs-Get-Lost uses 200,000+ simulated conversations; AnthroBench evaluates 14 anthropomorphic behaviors; FLEXI (Sep 2025) adds six full-duplex interaction scenarios; Full-DuplexBench and MTR-DuplexBench (Nov 2025) specifically target duplex dialogue models. Single-turn static benchmarks are being deprecated for dialogue claims.
- Sycophancy measurement is now a research track. SycEval, TRUTH DECAY, BrokenMath, and ELEPHANT (2025–2026) form a small but growing benchmark cluster. The field is moving from "sycophancy is a problem" to "sycophancy can be measured and reduced."

## Open Questions & Research Gaps

1. No standardized naturalness benchmark for turn-taking, backchannel appropriateness, or barge-in success rate. MOS covers audio fidelity, WER covers ASR, SSI covers single-turn quality — none cover timing or interactional naturalness.
2. Self-initiated repair in text LLMs is essentially unstudied. Vast literature exists on other-completed repair (user challenges → model apologizes). Almost none on the Schegloff (1977) preference: mid-turn self-correction without a user prompt. This is where AI-sounding text most obviously diverges from human writing.
3. Procedural grounding is missing from benchmarks. RAG addresses evidential grounding. "Do you want me to elaborate?" / "So to confirm, X?" grounding is absent from both academic benchmarks and commercial product descriptions.
4. Long-horizon persona maintenance. Persona-Chat (4–6 sentence profiles) and character cards both underspecify stable identity. No academic benchmark tests identity stability under adversarial or emotional pressure over 100+ turns.
5. Multi-turn reliability is not being seriously attacked. LLMs-Get-Lost's 39% performance drop is documented but not addressed in any current humanization or alignment work.
6. Cross-cultural turn-taking calibration. A Japanese/Arabic/Mandarin-calibrated full-duplex system does not exist in the literature or the product space.
7. Backchannel generation API. Community consensus is that AI-generated backchannels during user speech would feel more human, but wrong timing reads as interruption. Only end-to-end audio models handle it organically. No clean "inject occasional attentive backchannels" API surface exists.
8. Full-duplex telephony echo cancellation. Server-side PSTN barge-in has no published working solution; the server doesn't know when audio was *played* versus when it was *sent*.
9. Character consistency metric. LaMDA gave SSI for single turns. Nothing equivalent exists publicly for persona drift or memory-grounded continuity across weeks of use.
10. Sycophancy measurement — gap is partially closing. Named by Anthropic, documented by r/ChatGPT complaints. SycEval (AAAI 2025) measures it: 58% rate. TRUTH DECAY measures multi-turn drift specifically. BrokenMath finds 29% even in GPT-5. But no commercial product publishes a sycophancy metric or offers a sycophancy-reduction guarantee. The product-incentive misalignment remains wide open.
11. "Thinking humanness" vs "output humanness." Industry writing is almost entirely about output (tone, prosody, specificity, warmth). Internal-reasoning humanness — hesitation, self-correction, uncertainty hedging, non-monotonic thought — is only implicitly handled via Moshi's inner monologue and Anthropic's character training. This is the core whitespace for the Unslop project.
12. Unified humanization across voice and text. No vendor currently combines empathic response, spoken-style content rewriting, and multi-turn character consistency in a single product.

## How This Category Fits

Within Unslop's research taxonomy, Conversational & Dialogue Systems is the interaction substrate on which every other category plays out.

The sibling voice/prosody/TTS categories supply acoustic naturalness. This category supplies interactional naturalness: the difference between "a beautiful voice reading text" and "someone you can actually talk to." The sibling text-style and anti-slop categories target single-turn output humanness. This category is where single-turn work shows its limits — the 39% multi-turn reliability drop, the persona drift problem, and the grounding gap all live here, not in single-turn style guides. The sibling persona and memory categories address identity; this category adds the constraint that identity must hold under adversarial pressure over hundreds of turns, which no current benchmark tests. The sibling evaluation categories can borrow directly from this category's decomposed humanness taxonomies (USR, SSI, Sparrow's 23 rules) as templates for any evaluation harness that avoids a single "human-like" score. The sibling agent-framework categories (LiveKit, Pipecat, Rasa CALM) are also this category's concrete integration surfaces.

The most direct intersection for Unslop is the "thinking humanness" gap: Moshi's inner monologue at the model level, Anthropic's character training at the alignment level, and the practitioner observation that text-side disfluency/burstiness and voice-side backchanneling/pausing are the same pattern set. The category makes the case that Unslop is not a text-formatting tool but a cross-modal naturalness layer.

## Recommended Reading Order

1. Anthropic — "Claude's Character" (~15 min). Sets the "humanness is not engagement" frame before anything else.
2. Sesame — "Crossing the uncanny valley of conversational voice" (~20 min). Best compact definition of "voice presence" plus the honest benchmark admission.
3. MMNTM — "Voice Turn-Taking: The Engineering Behind Natural Voice AI" (~20 min). Five-generation endpointing taxonomy; makes the whole latency debate legible.
4. Sacks, Schegloff & Jefferson (1974) and Clark & Brennan (1991) — read the abstracts and first few pages of each; enough to see that modern architecture decisions are following 50-year-old descriptions.
5. OpenAI — "Hello GPT-4o" (~8 min). Canonical latency + paralinguistics statement; short and essential.
6. Laban et al. (2025), "LLMs Get Lost in Multi-Turn Conversation" — focus on the 39% figure and the aptitude-vs-unreliability decomposition.
7. r/ChatGPT 1m6fwth + saypi.ai #SaveStandardVoice PDF (~20 min combined). The consumer signal that naturalness is non-monotonic with model capability — nothing makes this point faster.
8. Moshi paper (arXiv:2410.00037), architecture and inner monologue sections (~20 min). Reference implementation for full-duplex + transparent reasoning.
9. Sayna — "Sub-Second Voice Agent Latency" + "Handling Barge-In" (~30 min). Practical budget breakdown and the semantic filter technique.
10. Cresta — "Crafting a natural-sounding AI voice" (~15 min). The only commercial source that names content-side humanization explicitly; read last to appreciate why it stands alone.
