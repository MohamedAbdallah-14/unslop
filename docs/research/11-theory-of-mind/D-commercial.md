# Theory of Mind in AI — Commercial Products

**Research value: high** — The market already has 20+ shipping products that claim to model user mental states (intent, emotion, personality, engagement, buying propensity). No vendor uses the academic phrase "theory of mind," but almost all use the same marketing grammar — "understands intent," "empathic," "reads emotion," "infers what the customer really means" — and the capability stack is converging on a recognizable pattern that a humanization project can lift directly.

## Executive Summary

Commercial ToM-adjacent products cluster into six segments. (1) **Contact-center CX platforms** (Cresta, ASAPP GenerativeAgent, Observe.AI, Uniphore, Cogito/Verint, Level AI) model the customer's emotional trajectory in real time and coach human or AI agents on empathy expression; Uniphore explicitly claims to detect "sarcasm and hidden feelings" that word-level sentiment misses, and Cresta breaks empathy into a four-step pipeline (detect situation → detect expression → align guideline → improve performance). (2) **Revenue intelligence / sales conversation AI** (Gong, ZoomInfo Chorus, Outreach Kaia, Sybill) reframe ToM as "buyer intent signals" — Gong reports 300+ signals per conversation, and Sybill specifically markets non-verbal/body-language reading because "90% of communication is non-verbal." (3) **Autonomous negotiation** (Pactum) runs supplier-side negotiations with explicit opponent modeling, data-backed arguments, and buyer-approval guardrails across 60+ enterprises including Walmart, Maersk, AB InBev. (4) **Synthetic-user / digital-twin research** (Synthetic Users, Synthetic Respondents, Ask Rally / GenPop, FishDog, Twin Persona, BlockSurvey) simulates target humans for pre-launch research — Synthetic Users uses the OCEAN personality model plus a "chain-of-feeling" that pairs emotional states with traits, and reports 85–92% synthetic-organic parity. (5) **AI coaching and mental-health companions** (BetterUp AI / Grow, Slingshot AI's Ash, Woebot, Wysa, Inflection Pi, Replika, Character.AI) model long-term user state — Slingshot built a "foundation model for psychology" trained on CBT/DBT/ACT/psychodynamic/MI; BetterUp is built on 17M coaching data points; Pi is marketed as "the first emotionally intelligent AI." (6) **Affective sensing / multimodal emotion APIs** (Hume AI, Affectiva/Smart Eye, Valence AI) expose raw ToM primitives — Hume's EVI models 48 core emotions and 600+ voice descriptors and adapts its own tone to match the user's "vibe."

The strongest shared pattern across segments: vendors never claim to read *thoughts*, but they do sell the downstream predictions ToM would enable — will this customer churn, will this deal close, is this rep empathetic, will this user act on this coaching nudge — and they differentiate on the **span of signals** (tone, prosody, body language, conversation history, CRM state) rather than on the cognitive model behind the prediction. The clearest market gap is an explicit, *interpretable* user-model layer: today the "mental state" is implicit inside a scoring model, and customers buy it as a KPI uplift rather than as a belief/desire/intent graph they can inspect.

## Products

### Contact-Center CX & Empathy Platforms

- **Cresta** — `cresta.com` — Series C+, used by United Airlines, Cox, Holiday Inn, Alaska Airlines, Spirit, Optimum, Brinks Home, multiple Fortune 500 banks. Unified platform for human and AI agents covering AI Agent, Agent Assist, and Conversation Intelligence. **ToM hook:** a documented four-step empathy pipeline — (1) detect situations requiring empathy, (2) detect whether empathy was expressed, (3) align on what acceptable expression looks like, (4) modify prompts/configurations to close the gap. Ships real-time sentiment analysis so supervisors can "intervene before situations escalate." Multi-NLP approach (keyword matching + semantic understanding + context tracking). Marketing claims: "understand complex, dynamic conversations in real time," "adapt instantly to customer tone, history, and intent."

- **ASAPP GenerativeAgent** — `asapp.com` — enterprise CX AI, used by American Airlines, Dish, JetBlue. LLM-based conversational agent with explicit intent analysis, knowledge-base/API access, hallucination control, data redaction. **ToM hook:** "adapts instantly to customer tone, history, and intent for hyper-personalized service." Positions empathy in CX as a first-class platform concern via a "new rules of customer experience" campaign.

- **Observe.AI** — `observe.ai` — contact-center conversation intelligence; proprietary ASR trained on 10M+ hours of customer service calls. **ToM hook:** dual sentiment stack — traditional text-NLP sentiment plus "tonality-based sentiment" that "goes beyond words to examine how something was said — tone, inflection, pitch, volume — to better identify a person's actual sentiment." Product surfaces include sentiment alerts to agents, personalized coaching based on sentiment trends, and monitoring of "agent empathy and emotional intelligence."

- **Uniphore** — `uniphore.com` — Emotion AI platform explicitly branded as such (`/emotion-ai`). **ToM hook:** the sharpest "we see what text misses" pitch on the market — "a customer saying 'It's fine' in a flat tone appears neutral textually but reveals negative emotion through tonality analysis." Claims to detect sarcasm and hidden feelings from tone of voice, speech speed, volume, and subtle vocal patterns. Frames traditional conversation intelligence as limited to analyzing 1–3% of calls; Uniphore analyzes 100% and tracks "emotional journeys" in real time.

- **Cogito (Verint)** — `cogitocorp.com` / `verint.com/cogito` — real-time agent coaching; now part of Verint. **ToM hook:** detects "over 200 voice and behavioral signals" to coach agents on empathy and rapport in the moment. Deployed at a Fortune 25 telecom's 30,000-agent workforce. Business outcomes cited: $79M telco benefit (30s AHT reduction + sales lift), 16% NPS increase at a healthcare plan provider. Pitches empathy as a trainable skill delivered via live next-best-action guidance.

- **Level AI** — `thelevel.ai` — "human-quality AI for every customer interaction." **ToM hook:** NLU-based intent and sentiment detection "beyond simple keywords, grasping full context and emotional cues." Auto-QA on 100% of calls, real-time struggle detection that alerts supervisors, and agent coaching that identifies "teams and agents needing attention." Customer-reported results: 25% CSAT lift, 45% agent satisfaction lift, 90% QA time saved.

### Revenue Intelligence / Sales Conversation AI

- **Gong** — `gong.io` — "Revenue AI OS." 5,000+ customers, used by a significant share of the Fortune 10. **ToM hook:** "300+ unique signals drawn from actual customer conversations" to detect "complex concepts, deal risks, and emerging trends." Explicitly distinguishes itself from keyword matching. Gong Agents span detection, generation, guidance, automation, and predictive intelligence. The Revenue Graph integrates 300+ tools and frames ToM as a "living network of revenue data."

- **ZoomInfo Chorus** — `zoominfo.com/products/chorus` — conversation intelligence acquired by ZoomInfo in 2021. 14 patents. Sales call analysis, coaching, deal momentum, market intelligence. **ToM hook:** surfaces "buyer sentiment," "winning behaviors," and "deal momentum." Noted as stagnating since acquisition per 2026 comparison coverage; teams are reportedly migrating to Gong.

- **Outreach Kaia** — `outreach.io` — sales-engagement leader. **ToM hook:** Kaia provides "real-time meeting assistance and deal signal detection," shaves "11 days off sales cycles" and lifts win rates ~10% on $50K+ deals. Positions signal detection as the bridge between conversation and CRM action.

- **Sybill** — `sybill.ai` — AI sales assistant that explicitly specializes in non-verbal analysis. **ToM hook:** "over 90% of communication is non-verbal" — and tools like Gong and Chorus "miss the non-verbal cues." Sybill quantifies buying intent, flags distraction moments, identifies champions vs. detractors (including silent participants), and measures rapport strength. Covers head tilt, posture, facial expressions as first-class signals.

### Autonomous Negotiation

- **Pactum** — `pactum.com` — autonomous procurement negotiation. 60+ top brands including Walmart, Maersk, AB InBev; ERP integrations with SAP and Coupa. **ToM hook:** a fleet of specialized agents (Requisition Alignment, Tactical Sourcing, Requisition Negotiation, Post-Sourcing Negotiation, Price List, Discount, Payment Terms, Rebate) that use "data-backed arguments, historical information, commodity indices, and demand forecasts" to model supplier positions and negotiate within human-set guardrails. Testimonial framing highlights *supplier emotion* too: "Our suppliers appreciate being proactively engaged. They feel valued because we take the time to ask how they want to grow with us." Enterprise pricing blends platform fee + value-share on documented savings. Pilots 6–12 weeks; "Enterprise Platform" is the most common tier; "Global Enterprise" handles multi-region / multi-ERP.

### Synthetic Users & Digital-Twin Research

- **Synthetic Users** — `syntheticusers.com` — "user research, without the humans." **ToM hook:** multi-agent architecture where each AI participant has an individual personality profile built on the **OCEAN** (Big Five) model and maintains "full context and continuity across every interview." Uses a "chain-of-feeling" approach that combines emotional states with OCEAN traits to produce human-like responses. Reports 85–92% synthetic-organic parity across thematic overlap, depth, and qualitative alignment; 95% AI-human feedback alignment in cited testimonials; 21+ peer-reviewed papers; $2–60 per interview vs. $100+ traditional; SOC 2. Positioned as a "discovery co-pilot" for front-loading problem space, not a replacement for organic research.

- **Synthetic Respondents** — `syntheticrespondents.com` — UK-based, launched 2025/2026. Proprietary behavioral research dataset: 2M+ responses over 10 years, 800+ projects, 42 industries, 35 countries. **ToM hook:** built on "behavioral and cognitive frameworks describing how people form preferences and make decisions," with a human-in-the-loop validation layer. Used for product development, marketing, and UX research.

- **Ask Rally / GenPop** — `askrally.com` — AI persona focus groups "calibrated on interviews with real people." "GenPop" is a virtual panel built on authentic human interviews "to reduce hallucinations and AI-sounding responses." Addresses the "Dutch Chris problem" — aggregate-stats-based personas hallucinating implausible individuals — by iterative calibration targeting 70–80% accuracy.

- **FishDog** — `fish.dog` — synthetic persona panels anchored to real-world statistics (census, income, geography), weighted to mirror population distributions. Emphasizes behavioral variables (age, household, income, cultural indicators) over long tail of traits.

- **Twin Persona** — `twinpersona.ai` — "behavioral digital twins built on real purchase data" rather than surveys. Supports scenario modeling (price changes, formula reformulations) grounded in actual transaction history across retail channels.

- **BlockSurvey AI Sample Response Generator** — `blocksurvey.io/ai-sample-response-generator` — e2e-encrypted survey platform (GDPR/HIPAA/SOC 2) with an AI Sample Response Generator that produces synthetic answers to validate question wording, surface bias, and preview analytics before launch. Narrower scope than Synthetic Users — aimed at survey design QA.

### AI Coaching & Mental-Health Companions

- **BetterUp AI / BetterUp Grow** — `betterup.com/press/betterup-launches-ai-coaching`, `betterup.com/products/betterup-ai-coaching/tour` — enterprise AI coaching from the market-leading human-coaching platform. **ToM hook:** "17 million data points on human growth and coaching effectiveness" combined with behavioral-science inputs. Marketing copy: AI coach "captures the nuance of effective coaching — adapting in the moment with empathy, guidance, and follow-up." Users can practice difficult conversations, problem solving, and leadership in real time. 95% user satisfaction, 16% confidence lift cited. Explicit human-AI hybrid — 51% of employees reportedly want both.

- **Slingshot AI — Ash** — `slingshotai.com` — "foundation model for psychology." **ToM hook:** trained on CBT, DBT, ACT, psychodynamic therapy, and motivational interviewing — framed as "designed from the ground up for therapeutic support rather than simply following instructions." Voice-based conversations, private, secure. Uses RL and Group Relative Policy Optimization (GRPO) on implicit user signals to learn "what actually helps people achieve their goals." Optimization targets from self-determination theory: autonomy, competence, relatedness, plus accountability. 25,000-user beta included many therapists.

- **Woebot** — Stanford-origin CBT chatbot. **ToM hook:** structured, decision-tree CBT modules teaching cognitive distortions, thought reframing, behavioral activation. Explicitly scripted rather than open-ended — user models are thin but the *therapeutic* mental model is deep. RCTs show depression/anxiety reductions. **⚠ Status update:** Woebot Health shut down its direct-to-consumer app on June 30, 2025, citing FDA marketing-authorization costs and inability to legally deploy LLM-based replacements as therapeutic tools without regulation. The company pivoted entirely to an enterprise B2B model, partnering with payers and providers. Roughly 1.5M users were affected. The shutdown is a concrete case of the humanization-vs-regulation gap: the scripted CBT model couldn't keep up with GPT-era expectations, and the LLM-based upgrade couldn't get approved. Woebot's legacy code and data is now licensed to enterprise integrations.

- **Wysa** — AI + human-coach hybrid with CBT, DBT, mindfulness, meditation, breathing. **ToM hook:** semi-guided conversations "explore what you're feeling before suggesting relevant exercises." Peer-reviewed study (Frontiers in Digital Health) shows users form a therapeutic alliance with Wysa comparable to human CBT therapists.

- **Inflection Pi** — `hey.pi.ai` / `inflection.ai` — ~~"the first emotionally intelligent AI."~~ **⚠ Status update (March 2024):** Microsoft hired Inflection's co-founders (Suleiman, Simonyan) and ~70-person team in an effective acqui-hire deal for $650M. Pi remains operational but usage-capped since August 2024 and stagnating. Inflection AI the company has pivoted to an enterprise API-first B2B model under new CEO Sean White; it no longer develops Pi as a consumer companion. The Pi numbers (1M DAU / 6M MAU, 33-min sessions, 60% weekly return) are pre-pivot and should not be cited as current. Inflection's collapse is the clearest 2024 lesson in companion-AI market dynamics: emotional-intelligence positioning alone could not sustain a consumer AI product against OpenAI/Google/Anthropic capability improvements. The emotional-companion niche now belongs primarily to Replika and Character.AI.

- **Replika** — `replika.com` — AI companion with long-term memory. **ToM hook:** layered memory architecture — visible memories + pattern-based learning from full conversation history; remembers birthdays, favorite songs, past conflicts, shared dreams across 3–4 year spans. Personality develops based on user interaction; reinforcement via upvotes. Studied academically (arXiv 2510.15905 on "companion-assistant dynamics") for the tension between deep user attachment and user-stated denial of "real" humanity.

- **Character.AI** — `character.ai`. **ToM hook:** explicit persona framework (Anchor & Action) distinguishing *user personas* (identity anchor) from *character definitions* (the partner). Persistent memory system: chat memories (~400 chars fixed), pinned memories, auto-memories (paid), plus a memory-capacity visualization meter and notifications when memories are recorded. PipSqueak 2 (PSQ2, 2026) explicitly targets "better in-character consistency, improved memory retention, and more natural dialogue."

### Workplace Intent Agents

- **Ema.co** — `ema.co` — "universal AI employee" for enterprises. **ToM hook:** "agentic reasoning to understand employee intent and context rather than relying on keyword searches." Connects to 200+ enterprise apps to build an organizational knowledge graph; accessible via Teams, Slack, Google Chat, intranet, voice; 100+ languages. Reports 95% response accuracy, 80%+ employee satisfaction, $5M+ annual savings. EmaFusion™ model blends public and private AI.

- **Sana AI** — `sanalabs.com/meet-sana-ai` — enterprise knowledge assistant. Chat with company knowledge, automate Salesforce updates, transcribe and summarize meetings, semantic search across apps. Domain-specific customization without code. ISO 27001, GDPR, AES-256 at rest. ToM framing is lighter than Ema's — primarily intent extraction for retrieval rather than modeling the employee as a persistent entity.

### Affective Sensing APIs / Infrastructure

- **Hume AI** — `hume.ai` — "the emotional intelligence lab for voice AI." **ToM hook:** Empathic Voice Interface (EVI) analyzes prosody ("tune, rhythm, timbre"), detects nuanced emotions with streaming measurements integrated into responses, uses tone of voice for end-of-turn detection, generates empathic responses ("apologetic for frustration, sympathetic for sadness"), modulates its own voice to match the user's "vibe," supports interruption with full context. Positioned explicitly as infrastructure: 50+ languages, 48+ emotions, 600+ voice descriptors, ~300ms time-to-first-byte over WebSocket, pluggable LLMs (Claude, GPT, Gemini, Llama). Expression Measurement API exposes 600+ emotion/voice characteristic tags from face and voice. Open-source TADA TTS + closed-source Octave TTS + closed-source EVI S2S; Human Feedback API for preference-based eval studies. **2025 updates:** EVI 1 and 2 deprecated August 30, 2025. EVI 4-mini launched with multilingual support (English, Japanese, Korean, Spanish, French, Portuguese, Italian, German, Russian, Hindi, Arabic). Octave 2 TTS released October 2025 at 50% cost reduction with faster generation speeds. Hume closed a $50M Series B to fund these infrastructure updates.

- **Valence AI** — `valenceai.tech` — "highest-accuracy emotion engine" pitched for sales and support voice calls. Narrower competitor to Hume focused on the CX/sales wedge (detecting when empathy or escalation is needed, buying signals, AI QA).

- **Affectiva (Smart Eye)** — `affectiva.com` / `smarteye.se` — pioneer of automotive emotion AI. **ToM hook:** real-time facial-expression and voice analysis for drowsiness, fatigue, physical and mental distraction, plus "complex emotional and cognitive reactions" to driving conditions and vehicle systems. Drives safety features (semi-autonomous handoff, fleet safety, airbag deployment), child-presence detection, and environmental personalization based on detected emotional state. One of the few ToM-adjacent products whose *physical safety* is downstream of the mental-state inference.

## Marketing-Grammar Quotes on "Intent / Emotion / Mental State"

Exact or close-paraphrased marketing lines, grouped by claim type:

- **"Understands intent / context / tone / history."**
  - ASAPP GenerativeAgent: "adapts instantly to customer tone, history, and intent for hyper-personalized service."
  - Cresta: the AI system is designed to "understand complex, dynamic conversations between customers and agents in real-time."
  - Ema: "agentic reasoning to understand employee intent and context rather than relying on keyword searches."
  - Level AI: NLU detects "customer intent and sentiment beyond simple keywords, grasping full context and emotional cues."

- **"Reads emotion / empathy / tonality beyond words."**
  - Observe.AI: tonality-based sentiment "goes beyond words to examine how something was said — analyzing tone, inflection, pitch, and volume — to better identify a person's actual sentiment."
  - Uniphore: "'It's fine' in a flat tone appears neutral textually but reveals negative emotion through tonality analysis."
  - Cogito: coaches agents to "develop empathy and improve customer rapport" via "over 200 voice and behavioral signals."
  - Hume EVI: "measures the tune, rhythm, and timbre of user speech … generates contextually appropriate emotional responses — apologetic for frustration, sympathetic for sadness."

- **"First emotionally intelligent AI."**
  - Inflection Pi: "the first emotionally intelligent AI."
  - BetterUp AI: AI coach "captures the nuance of effective coaching — adapting in the moment with empathy, guidance, and follow-up."

- **"Reads non-verbal / body language."**
  - Sybill: "over 90% of communication is non-verbal," tracks "each participant's engagement level" and "quantifies buying intent."
  - Affectiva: analyzes facial expressions and voice "to detect drowsiness, distraction, emotional and cognitive states."

- **"Reads deals / buying signals."**
  - Gong: "300+ unique signals drawn from actual customer conversations" to detect "deal risks, and emerging trends."
  - Outreach Kaia: "real-time meeting assistance and deal signal detection."

- **"Simulates/predicts real people."**
  - Synthetic Users: "predict human behavior before the market does"; "chain-of-feeling" combining emotions with OCEAN traits; "85–92% synthetic-organic parity."
  - Ask Rally / GenPop: "built on authentic human interviews to reduce hallucinations and AI-sounding responses."
  - Twin Persona: "behavioral digital twins built on real purchase data."

- **"Models the user long-term."**
  - Replika: memory lets the system "remember your birthdays, favorite songs, past conflicts, and shared dreams — often recalling conversations from 3–4 years ago unprompted."
  - Character.AI: PipSqueak 2 targets "better in-character consistency, improved memory retention, and more natural dialogue."

- **"Foundation model for mental state."**
  - Slingshot AI: "foundation model for psychology … designed from the ground up for therapeutic support rather than simply following instructions."
  - BetterUp: "17 million data points on human growth and coaching effectiveness."

## Patterns, Trends, and Gaps

### Patterns

1. **"Intent + emotion" is the universal dual axis.** Every CX platform (Cresta, ASAPP, Observe.AI, Uniphore, Cogito, Level AI) markets the same two primitives: what the user *wants* (intent) and what the user *feels* (emotion/sentiment/tonality). Sales tools swap "emotion" for "buying signals," coaching tools swap it for "mental fitness" — but the structure is invariant.

2. **Signals, not cognition, is the differentiator.** Nobody sells a cognitive model of the user; they sell *coverage*. Cogito: 200+ signals. Gong: 300+ signals. Hume: 48 emotions × 600 voice descriptors × 50 languages. The implicit ToM is "a richer spectral decomposition of observable behavior than the other guy."

3. **Tonality and non-verbal are the premium wedge.** Uniphore, Observe.AI (tonality), Cogito (voice/behavioral), Sybill (body language), Hume (prosody), Affectiva (face + voice) all lean on the same "text-alone misses it" story. When a vendor wants to command a premium over text-sentiment incumbents, this is the move.

4. **Empathy is being decomposed into a pipeline.** Cresta's four-step (detect-situation → detect-expression → align-guideline → improve-performance) is the clearest articulation but the same structure appears in Observe.AI's "monitor agent empathy and emotional intelligence" and Cogito's "real-time empathy coaching." Empathy is treated as a measurable, coachable behavior — not a mystical property.

5. **OCEAN / Big Five is the go-to personality substrate.** Synthetic Users explicitly uses OCEAN + "chain-of-feeling"; Character.AI's Anchor & Action framework rhymes with it; Replika's pattern-based personality adaptation is an implicit analogue. Nobody in this sample uses more recent social-cognitive-theory models — OCEAN is pragmatic and familiar to marketing/UX buyers.

6. **Memory is how companions fake ToM.** Replika (multi-year recall), Character.AI (chat memories + memory meter + notifications), Pi (33-min average sessions, 60% weekly return), BetterUp (personalized to role, personality, learning style, culture). The user-visible mental model is "it remembers me" — which is a weaker but more sellable claim than "it understands me."

7. **Human-in-the-loop is almost universal.** BetterUp (AI + human coaches), Pactum (buyer-approval thresholds), Wysa (AI + human coaching), Synthetic Users ("discovery co-pilot, not a replacement"), Cresta/ASAPP/Observe.AI (supervisor intervention). The honest subtext: no vendor is comfortable deploying a pure ToM system without a human validator somewhere in the loop.

8. **Two distinct "humanization" stances.** Companion / therapy products (Slingshot, BetterUp, Pi, Wysa, Replika) push toward *warmer* outputs — more empathy, more follow-up, more continuity. Contact-center products push toward *more legible* outputs — empathy expressed on-script, escalation when tonality crosses a threshold. A humanization layer needs to know which of these two stances it's serving.

### Trends (2025–2026)

- **From sentiment to emotion to "emotional journey."** Uniphore explicitly names "emotional journeys" and Cresta tracks empathy across a conversation arc. The unit of analysis is moving from the utterance to the full session.
- **Voice-native is the new default for ToM.** Hume EVI (now on EVI 4-mini with expanded multilingual support), Slingshot Ash, Affectiva — and the CX incumbents all heavily invest in tonality. Text-only ToM is being reframed as the low-rent tier. Note: Inflection Pi, formerly a voice-native companion leader, effectively exited the consumer market in 2024 (see above).
- **Digital twins are eating early-stage research.** Synthetic Users, Synthetic Respondents, Ask Rally/GenPop, FishDog, Twin Persona — four+ well-funded players in under 24 months. Most explicitly position against real recruitment, not alongside it.
- **Agent-of-agents stack for negotiation.** Pactum's eight specialized negotiation agents (Alignment, Tactical, Requisitions, Post-Sourcing, Price List, Discount, Payment Terms, Rebate) is the clearest commercial instance of decomposed ToM: different "minds" for different phases of the same opponent relationship.
- **Conversation intelligence consolidation.** 2026 comparisons report teams migrating off Chorus (ZoomInfo) toward Gong; ZoomInfo is reportedly under-investing post-acquisition. The ToM-in-CI market is concentrating, not fragmenting.
- **Foundation models for specific mental domains.** Slingshot's "foundation model for psychology" is the first explicit vertical foundation model for a mental-state domain. BetterUp's 17M-data-point claim and Synthetic Users' OCEAN-based participant model are softer versions of the same move.
- **Regulatory pressure on therapeutic AI is real.** Woebot's shutdown (June 2025) demonstrates that FDA marketing-authorization requirements for LLM-based therapy products are not waivable at current timelines. Any companion or therapeutic product in this space must account for regulatory runway, not just capability. The "pre-scripted CBT → LLM upgrade" path Woebot attempted is blocked without clinical-trial evidence the FDA can evaluate.

### Gaps / Open Whitespace

1. **No interpretable belief/desire/intent graph is exposed to the buyer.** Every system surfaces ToM as a *score* (sentiment 0.7, empathy flag, buying-intent percentile). None exposes "the model believes the user *wants* X, *believes* Y, is *blocked by* Z, and would change behavior if W." The explicit cognitive-graph layer is a real gap — both for auditability and for agent design.

2. **No shared "humanization API."** CX vendors treat humanization as an internal ingredient; companion products treat it as personality; synthetic-user vendors treat it as realism. There's no vendor shipping "humanize this LLM output *conditioned on* an inferred user mental state."

3. **ToM eval is immature.** Synthetic Users self-reports 85–92% parity; Hume offers a Human Feedback API; Cresta runs internal validation. There is no shared, public benchmark for "did the system correctly infer what the user was thinking/feeling/wanting."

4. **Cross-session user models barely exist outside companion products.** Replika and Character.AI model the user across years; every enterprise CX product resets per-conversation (or relies on CRM fields). A persistent, cross-surface user model is an obvious next layer.

5. **"Sarcasm / hidden feelings" is claimed but rarely validated.** Uniphore's "It's fine" example is compelling but the industry lacks published benchmarks for sarcasm, irony, and masked affect detection. This is both a credibility gap and an opportunity.

6. **Multi-party ToM is nascent.** Sybill flags "silent participants" and Pactum models supplier relationships, but most systems still treat conversations as dyadic (agent ↔ customer, coach ↔ employee). Buying committees, family car rides, therapy triads, and negotiation tables are multi-party by nature.

7. **"Humanizing output back" is untouched by the ToM stack.** These vendors infer the user's state to *drive business outcomes* or *retrieve the right knowledge*; almost none use the inferred state to *modulate the AI's own output voice* beyond Hume EVI's prosodic matching and Slingshot's therapeutic tone. This is the most direct opening for a humanization-of-output project.

## Sources

- Cresta — `cresta.com`, `cresta.com/blog/building-and-deploying-production-grade-ai-agents-crestas-end-to-end-approach`, `cresta.com/guides/real-time-sentiment-analysis` — empathy pipeline, real-time sentiment, unified human/AI agent platform, enterprise customer list.
- ASAPP GenerativeAgent — `asapp.com/customer-experience-platform/generativeagent`, `asapp.com/press/empathy-ai-and-the-new-rules-of-customer-experience` — intent + tone adaptation, safety-first LLM agent for CX, empathy positioning.
- Observe.AI — `observe.ai/contact-center-glossary/sentiment-analysis`, `observe.ai/blog/ai-sentiment-analysis-contact-centers-customer-experience` — traditional + tonality sentiment, 10M-hour ASR, agent empathy monitoring.
- Uniphore — `uniphore.com/emotion-ai/`, `uniphore.com/blog/harnessing-customer-emotion-to-boost-csat-and-reduce-churn/` — emotion AI framing, "It's fine in a flat tone" example, 100% call coverage claim.
- Cogito / Verint — `cogitocorp.com/products/real-time-coaching/`, `businesswire.com/news/home/20230124005247/en/Cogito-Enhances-Conversation-AI-Bolstering-Real-Time-Agent-Assist-and-Coaching-Capabilities` — 200+ voice/behavioral signals, Fortune 25 30K-agent deployment, empathy coaching.
- Level AI — `thelevel.ai`, `thelevel.ai/blog/what-is-conversation-intelligence/` — intent + sentiment NLU, 25% CSAT uplift, 90% QA time saved.
- Gong — `gong.io`, `gong.io/platform/revenue-ai`, `gong.io/conversation-intelligence` — 300+ signals, Revenue AI OS, Fortune 10 penetration.
- ZoomInfo Chorus — `zoominfo.com/products/chorus`, `summarizemeeting.com/comparison/revenue-intelligence-tools` — 14-patent CI platform, post-acquisition stagnation, migration to Gong.
- Outreach Kaia — `outreach.io/resources/blog/coach-sellers-to-success-with-kaia` — real-time meeting assist + deal-signal detection, sales-cycle and win-rate impact.
- Sybill — `sybill.ai/emotional-intelligence`, `sybill.ai/blogs/nonverbal-communication` — non-verbal analysis, buying-intent quantification, body-language taxonomy.
- Pactum — `pactum.com`, `pactum.com/price-list-agents`, `procurementaiagents.com/agents/pactum-ai.html`, `toolradar.com/tools/pactum-ai` — eight specialized negotiation agents, Walmart/Maersk/AB InBev, pricing tiers, 82% supplier satisfaction.
- Synthetic Users — `syntheticusers.com`, `docs.syntheticusers.com/guides/core-concepts`, `syntheticusers.com/science` — OCEAN + chain-of-feeling, 85–92% parity, SOC 2, 21+ papers.
- Synthetic Respondents — press coverage (Eagle Country) on launch — 2M+ response dataset, behavioral/cognitive framework, HITL validation.
- Ask Rally / GenPop — `askrally.com` — persona calibration on real interviews, Dutch-Chris problem framing, 70–80% accuracy targets.
- FishDog — `fish.dog/how-we-build-digital-twins` — census-anchored synthetic panels.
- Twin Persona — `twinpersona.ai` — purchase-data-based digital twins, scenario modeling.
- BlockSurvey — `blocksurvey.io/ai-sample-response-generator`, `blocksurvey.io` — encrypted survey platform, AI sample responses, compliance.
- BetterUp — `betterup.com/press/betterup-launches-ai-coaching`, `betterup.com/products/betterup-ai-coaching/tour`, `betterup.com/blog/human-plus-ai-coaching` — 17M data points, 95% satisfaction, 16% confidence lift, human-AI hybrid.
- Slingshot AI — `slingshotai.com`, `radical.vc/building-the-foundation-model-for-mental-health/` — CBT/DBT/ACT/psychodynamic/MI training, GRPO + self-determination theory, 25K beta.
- Woebot — systematic review `pmc.ncbi.nlm.nih.gov/articles/PMC11904749/`, comparison `ilty.co/blog/woebot-vs-wysa-vs-ilty-2026` — Stanford CBT, decision-tree UX, RCT evidence.
- Wysa — Frontiers in Digital Health (`frontiersin.org/articles/10.3389/fdgth.2022.847991`), `heypsych.com/tools/wysa` — CBT+DBT+mindfulness, therapeutic alliance parity with human therapists.
- Inflection Pi — `hey.pi.ai`, `inflection.ai/inflection-2-5`, `inflection.ai/blog/pi` — "first emotionally intelligent AI," Inflection-2.5, 1M DAU / 6M MAU, 33-min avg session.
- Replika — `help.replika.com/hc/en-us/articles/37208679176077-How-does-Replika-s-memory-work`, `en.wikipedia.org/wiki/Replika`, `arxiv.org/html/2510.15905v4` — layered memory, years-long recall, academic analysis of companion dynamics.
- Character.AI — `blog.character.ai/helping-characters-remember-what-matters-most/`, `blog.character.ai/pipsqueak2-and-more/`, `characterai.it.com/character-ai-character-personality-framework/` — PSQ2 model, 400-char chat memories, memory visualization, Anchor & Action persona framework.
- Ema.co — `ema.co`, `ema.co/blog/product-launch/introducing-ema-s-employee-assistant` — agentic reasoning for employee intent, 200+ app connectors, EmaFusion model.
- Sana AI — `sanalabs.com/meet-sana-ai` — enterprise knowledge assistant, domain-specific customization, ISO 27001.
- Hume AI — `hume.ai`, `hume.ai/blog/introducing-hume-evi-api`, `hume.ai/empathic-voice-interface`, `dev.hume.ai/docs/speech-to-speech-evi/overview`, `hume.ai/expression-measurement` — EVI, 48 emotions, 600+ voice descriptors, 50+ languages, 300ms TTFB, Human Feedback API.
- Valence AI — `valenceai.tech` — emotion engine for sales/support voice.
- Affectiva / Smart Eye — `affectiva.com/product/affectiva-automotive-ai-for-driver-monitoring-solutions`, `smarteye.se/solutions/automotive/interior-sensing` — driver drowsiness/distraction/emotion detection, in-cabin sensing, safety downstream of mental-state inference.
