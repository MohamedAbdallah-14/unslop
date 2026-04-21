# Cognitive Architectures — Commercial Landscape

**Research value: high** — The commercial "cognitive architecture" space in 2026 is unusually legible: two distinct camps (reasoning-first coding/agent labs vs. emotion-first companion/NPC platforms) with a thin middle of enterprise neuro-symbolic vendors, and an emerging third camp (LeCun/Extropic/Symbolica) betting that the whole post-transformer substrate needs replacing. For a humanizing-AI project, the competitive map is well covered but the *intersection* of "deep reasoning" and "humanlike tone/affect" is a clear gap.

**Last updated: April 2026. Covers April 2025–April 2026.**

## Executive Summary

Companies that frame themselves around "thinking" architectures cluster into five commercial camps.

1. **Reasoning-first agent labs** — Imbue, Cognition (Devin), Reflection AI, Adept (pre-Amazon). Pitch: "AI that reasons, plans, and acts," almost always instantiated as autonomous coding agents. The cognitive architecture language is used to justify *long-horizon task execution*, not empathy or tone.
2. **Post-transformer structural bets** — Symbolica (category theory), Extropic (thermodynamic p-bits), Sakana AI (evolutionary model merging), AMI Labs (LeCun, JEPA / world models). Pitch: "pattern matching is a dead end; real reasoning needs a new architecture." Mostly R&D, little productized surface today.
3. **Emotion- and persona-first platforms** — Inflection Pi, Hume AI (EVI), Character.AI, Replika, Soul Machines. Pitch: "emotionally intelligent," "empathic," "human-centered." These are the only commercial actors that explicitly frame their architecture around making AI *feel human*.
4. **Game / NPC character engines** — Inworld AI, Convai. Pitch: a full "Character Engine" / "character brain" combining LLM reasoning with memory, goals, perception, autonomous motivations, and emotional state — the most complete mass-market instantiation of a classical cognitive architecture (SOAR/ACT-R-like) on top of modern LLMs.
5. **Enterprise neuro-symbolic / orchestration platforms** — OneReach.ai, Adverant Nexus, Growth Protocol, Kortexya/ReasoningLayer, Weave.AI, AI21 Maestro, CognitionHub HiveOS, C3 AI's C3 Code, SingularityNET's OpenCog Hyperon/PRIMUS. Pitch: "cognitive layer" / "enterprise reasoning platform" with memory, orchestration, knowledge graphs, and auditability — positioned against raw LLMs.

The strongest cross-cutting insight for a humanization project: *almost every vendor that markets "thinking" optimizes for task-correctness (benchmarks, tool-calling, codebases), while everyone marketing "humanlike" optimizes for affect (prosody, memory, empathy). Very few cognitive-architecture products sit in the middle — a reasoning engine whose visible thinking is itself humanlike.* Anthropic's "visible extended thinking" is the closest incumbent position; the AI21 Maestro pitch (conceptualization → formulation → articulation, explicitly modeled on human language production) is the closest framing fit but is sold as enterprise orchestration rather than humanization.

## Products

### Reasoning-first agent labs

- **Imbue** — `imbue.com`. Founded by Kanjun Qiu; ~$200M raised; ~10K H100 cluster. Trains >100B-parameter reasoning-optimized foundation models and ships agent tooling on top: **Sculptor** ("the missing UI for parallel coding agents," Sep 2025), **Keystone** ("building self-configuring agents," open-source, Mar 2026), plus Vet, Offload, and Latchkey. Published Feb 2026 work on beating ARC-AGI-2 via "code evolution" that lifts cheaper models 2–3× and reaches 95% with Gemini 3.1 Pro. Explicit framing: "robust reasoning — handling uncertainty, gathering information, playing out scenarios, and adapting approaches — is the primary blocker to practical AI agents."

- **Cognition Labs — Devin** — `cognition.ai`. Self-described "AI lab focused on reasoning" that built Devin, "the first AI software engineer … a tireless, skilled teammate." Cognitive-architecture claim is long-horizon autonomy: Devin can "plan and execute complex engineering tasks requiring thousands of decisions" (learning tech, end-to-end deploys, autonomous bug-finding, fine-tuning models, production PRs, freelance jobs). SWE-bench jump from 1.96% SOTA to 13.86% at launch. Devin 2.0 ($20 entry plan, Apr 2025) added parallel Devins, interactive planning, codebase search, automated code review. Devin 2.2 (Feb 2026) added end-to-end testing with desktop computer use, self-verification, and auto-fix. Cognition merged 659 Devin PRs in one week in Feb 2026 ("Devin builds Devin").

- **Reflection AI** — `reflection.ai`. Tagline: "Building Frontier Open Intelligence." Founded 2024 in Brooklyn by ex-DeepMind AlphaGo researchers Misha Laskin (CEO) and Ioannis Antonoglou (CTO). Raised $2.13B cumulative; $2B Series B Oct 2025 led by Nvidia ($800M) at an $8B valuation (15× up from $545M in Mar 2025); reportedly seeking an additional $2.5B at $25B as of Mar 2026. Product: **Asimov**, a code-research agent for understanding large codebases. Thesis: solving autonomous coding is a stepping stone to general superintelligence because the required capabilities (advanced reasoning + iterative self-improvement) generalize.

- **Adept AI** — `adept.ai`. Positioned "AI that powers the workforce." Built ACT-1 (2022), an Action Transformer controlling web browsers and desktop apps via natural-language instructions — one of the earliest commercial bets on a cognitive architecture for computer-use agents. In 2024 Amazon executed a $350M+ "reverse-acquihire" for co-founders David Luan and Ashish Vaswani plus key staff and the foundational research, leaving Adept operating as an enterprise automation company (~$415M cumulative funding; financial services and healthcare customers) with a technology that is "brittle and fail[s] on unseen, complex workflows." Cautionary tale for action-transformer-as-cognitive-architecture.

- **xAI — Grok 4.20 Beta (multi-agent reasoning variant)** — `x.ai`. Feb 17 2026 release with three API variants (Non-Reasoning, Reasoning Preview, Multi-Agent Beta). The multi-agent flagship is explicitly a named four-agent cognitive architecture: **Grok** (coordinator), **Harper** (research/web grounding), **Benjamin** (logic/code), **Lucas** ("deliberately positioned to disagree with others" — creative/divergent). Shared ~3T-parameter MoE backbone, ~500B active, shared KV cache/context. Up to 16 agents for deep research. Claims ~65% hallucination reduction on multi-step reasoning. Interesting for humanization because the agents are *named and given personas with epistemic roles*, including a dissenter.

- **Anthropic — Claude with extended thinking** — `anthropic.com`. Not a cognitive-architecture startup per se but the most widely deployed "visible thinking" product. Extended thinking (introduced with Claude 3.7 Sonnet, Feb 2025) exposes step-by-step reasoning and a user-settable "thinking budget." Claude Opus 4.7 (Apr 2026) replaced the manual toggle with *adaptive thinking* driven by an effort parameter. Marketing framing via Constitutional AI (RLAIF) emphasizes principled, self-reflective output — "thoughtful without being evasive" — which is the closest incumbent framing to humanizable reasoning.

### Post-transformer structural bets

- **Sakana AI** — `sakana.ai`, Tokyo. Mission: "transformative AI that will bring us into the next paradigm" via nature-inspired intelligence. Founded 2023 by ex-DeepMind David Ha and Llion Jones (Transformer co-author). ~$30M seed + ~$200M Series A. Core IP: evolutionary model merging. "Evolutionary Optimization of Model Merging Recipes" (Nature Machine Intelligence) produced a 7B Japanese Math LLM surpassing some 70Bs. Latest is **M2N2** (GECCO'25 best-paper runner-up): evolving merging boundaries ("like swapping variable-length segments of DNA"), diversity-through-competition for niche specialization, and attraction-based mate selection. Not a cognitive architecture in the classical sense — cognition emerges from the *population*, not from within a single model.

- **Symbolica** — `symbolica.ai`. Tagline: "Intelligence, Redefined — pioneering the application of category theory and type theory to build a symbolic reasoning engine." Founded 2022; $33M Series A + seed led by Khosla. Three architectural primitives: **Semantics** ("formal logic and semantics at the architectural level providing provable invariants"), **Reasoning** ("program execution, search, and synthesis all occur in the same architecture"), and **Categories** (unifying discrete types/programs with vector spaces and optimization). Product: **Agentica**, an open-source SDK agent-builder with code execution as a first-class primitive. Result: 85.28% on ARC-AGI-2 with Opus 4.6, 10–20 pp above baselines.

- **Extropic** — `extropic.ai`. Thermodynamic computing hardware startup (Guillaume Verdon / "Beff Jezos"). Builds **Thermodynamic Sampling Units (TSUs)** whose core primitive is the **p-bit** — a silicon element that samples between states with programmable probabilities, exploiting thermal electron fluctuations rather than forcing 1/0 binarization. Hardware timeline: **X0** prototype (Q1 2025), **XTR-0** dev platform shipped to partners (Q3 2025), **Z1** production chip with hundreds of thousands of p-bits targeted early 2026. Claims thousands-fold energy savings on probabilistic workloads vs. GPUs. Open-source Python simulator **THRML**. Positions itself as "probabilistic software, meet probabilistic hardware" — a cognitive-architecture pitch at the silicon layer.

- **AMI Labs (Yann LeCun)** — Paris. Founded late 2025 after LeCun left Meta; **$1.03B seed** at $3.5B pre-money in Mar 2026 (Europe's largest-ever seed), with Bezos, Nvidia, Samsung, Eric Schmidt, and Tim Berners-Lee participating. Thesis: LLMs are "a dead end" / "sophisticated pattern matchers" that lack causality, physics, and world-grounding. Builds **world models** based on **JEPA (Joint Embedding Predictive Architecture)** — "which futures are physically and causally compatible with this situation?" — positioned as an open-source European alternative to US/China labs. No near-term product; the pitch is research-first.

- **SingularityNET — OpenCog Hyperon / PRIMUS** — `singularitynet.io`. Classical AGI-aligned cognitive architecture. Core components: **Distributed Atomspace (DAS)** hypergraph knowledge repository; **MeTTa (Meta Type Talk)** programming language for self-modifying and introspective programs; **PRIMUS** cognitive architecture targeted at human-level AGI; plus PLN (probabilistic logic), ECAN (attention economics), MOSES (evolutionary program synthesis). Hyperon Alpha released May 2024; ongoing publications into early 2026. Distinctive because it is the only commercial vendor whose explicit *marketing* mentions "architectures resembling human cognition" at the data-structure level.

### Emotion- and persona-first platforms

- **Inflection AI — Pi** — `inflection.ai`, `pi.ai`. Homepage tagline: "We're empowering people and brands with human-centered, emotionally intelligent AI." Founded by Mustafa Suleyman (DeepMind) and Reid Hoffman. Pi is positioned as an "empathetic personal AI" built on counseling-psychology dialogue techniques, with cross-session memory, adaptive communication style, warm/curious tone, and free voice conversation on web/iOS/Android. Capability scope is deliberately narrow — no code, data, images, or file handling. Strategic cloud hanging over product: Microsoft hired the founding team in 2024, leaving Pi's future uncertain while the brand continues to sell the "human-centered, emotionally intelligent AI" thesis to enterprise.

- **Hume AI — EVI (Empathic Voice Interface)** — `hume.ai`. Tagline: "The Emotional Intelligence Lab for Voice AI." Positioning spans **50+ languages, 48+ emotions, 600+ voice descriptors**. EVI processes prosody (tune, rhythm, timbre) and responds with matched vibe (calm, interest, excitement). Trained on human reactions to optimize for well-being-aligned expressions. Ships **Voice Control** for precise manipulation of 10 voice dimensions (assertiveness, confidence, enthusiasm, relaxedness, smoothness…) without voice cloning, plus **Octave** (closed-source LLM TTS with voice design/modulation/cloning), **TADA** (open-source LLM TTS), and a **Human Feedback API** for survey-style human evals. **EVI 3** (May 2025) is a speech-to-speech foundation model that captures voice, rhythm, tone, and personality from 30 seconds of audio without fine-tuning, at <300 ms response time (1.2 s practical latency). **EVI 4-mini** (Jan 2026) adds multilingual support across 11 languages. Hume raised a $50M Series B. Notable convergence: published a joint blog with Anthropic on emotionally intelligent Claude Voice interactions, marking the first public collaboration between a reasoning-first lab and an affect-first platform. This is the most prosody-centric commercial cognitive architecture shipping today.

- **Character.AI** — `character.ai`. Creative/roleplay platform with millions of community-created characters. 2026 model is **PipSqueak**, tuned for better context and reduced repetition. $9.99/mo Premium; 30+ voices; group chats. Community-rated 3.6–4.2/5. Architecturally thin on long-term memory; architecturally deep on *persona diversity* — the largest commercial corpus of hand-crafted AI personas in production.

- **Replika** — `replika.ai`. Emotional companion positioned against Character.AI: one deep long-term relationship, not many shallow ones. $19.99/mo Pro. 2026 update ships **Smarter Memory** that recalls emotional states and adjusts tone accordingly; voice + AR in Pro. Pitched explicitly for "emotional support, companionship, self-reflection, and daily emotional check-ins."

- **Soul Machines** — `soulmachines.com`. Tagline: "Experiential AI™." Core IP: the **Digital Brain™**, a simulated set of human subsystems (sensory, motor, attention/perception, autonomic) that drives **autonomous facial animation** — digital humans that "spontaneously respond to stimuli rather than follow pre-programmed scripts." LLM-agnostic. Commercial surface: **Digital Workforce™** for customer service, HR benefits, clinical trial onboarding, sales engagement, with Salesforce and ServiceNow integrations. The only mass-market vendor explicitly marketing an embodied cognitive architecture whose *output modality* is a face.

### Game / NPC cognitive-architecture vendors

- **Inworld AI** — `inworld.ai`. Tagline (updated): **"Top-ranked voice AI for realtime applications."** — Inworld has pivoted from a pure NPC character engine to a broader **Agent Runtime and voice AI platform**, with Google, NVIDIA, Meta, Ubisoft, and Xbox as clients. The original NPC subsystems (Configurable Reasoning, Long-Term Memory, Autonomous Goals, Emotional Fluidity, Spatial Perception, state-of-mind/dialogue split) remain in the product and in Unreal/Unity SDKs. **2025–2026 additions:** **Unreal AI Runtime** (C++ orchestration, single low-latency API across hundreds of models), **TTS-1.5-Max** (<200 ms latency), SOC 2 Type II and GDPR certification, zero data retention option, HIPAA compliance. At GDC 2025, Inworld demonstrated production-deployed AI NPCs in shipping games. The company now ranks #1 on Artificial Analysis for voice AI latency. For a humanization project this remains the single most reusable commercial blueprint for "reasoning + memory + goals + emotion + perception" — and the "state of mind ≠ dialogue" split is still unique in the commercial market, now paired with production-grade TTS.

- **Convai** — `convai.com`. Tagline: "Conversational AI for Virtual Worlds." Competes head-on with Inworld. Features: real-time multimodal perception (vision + hearing), 500+ voices across 65+ languages, embodied animations with lip-sync and facial animation, personality traits + knowledge banks + narrative design + memory systems. No-code browser studio; Unreal/Unity/3JS SDKs; deployable to web, mobile, VR, AR, "physical world." Integrated into **NVIDIA's Avatar Cloud Engine (ACE) for Games** as the conversational layer. Narrower on cognitive subsystems than Inworld (no "state of mind" split), deeper on deployment breadth.

### Enterprise cognitive-architecture / neuro-symbolic platforms

- **AI21 Labs — Maestro (+ Jamba Reasoning)** — `ai21.com`. Maestro is sold as an "accurate AI agents for enterprise workflows" orchestrator, but the underlying pitch is explicitly humanlike: AI21's "Modular Intelligence" post frames it as mirroring *human language production stages — conceptualization, formulation, articulation* — by separating reasoning, planning, and execution into independently evaluable components. Features: dynamic planning tree of LLM and tool calls; budget-controlled reasoning (`low`/`medium`/`high`); model-agnostic across AI21 Jamba, OpenAI, Anthropic, Google; execution traces + structured validation reports. **Jamba Reasoning 3B** is a 256K-context (1M token max), 2–5× efficient open-source reasoning component. Best framing fit for a humanization project.

- **OneReach.ai — Cognitive Architecture platform** — `onereach.ai`. Positions itself under the exact phrase "cognitive architecture." Components: low-code/no-code studio, contextual memory system, cognitive orchestration engine, observability for agentic applications. One of the few vendors to anchor its marketing on the term itself rather than just "agents."

- **Adverant — Nexus** — `adverant.ai`. Tagline: "The Cognitive Layer for AI Infrastructure." **GraphRAG memory**, **unified LLM gateway** across 320+ models, autonomous orchestration, 67+ microservices, 240+ AI agents. Positions the "cognitive layer" as infrastructure middleware, not application.

- **Growth Protocol** — `growthprotocol.ai`. Tagline: "The Enterprise Reasoning Platform." Neuro-symbolic approach for high-stakes enterprise decisions. Public claims: deployed across 3 continents, $170M+ profitable growth delivered, 20× ROI average, SOC 2 Type II, NVIDIA Inception, WEF Davos 2026 presence. Customer name-drops: Nestlé, Unilever, P&G. Sectors: insurance, industrials, consumer.

- **Kortexya — ReasoningLayer** — `reasoninglayer.ai` / `kortexya.com`. Neuro-symbolic platform adding formal reasoning for auditability, determinism, and cost. Claim: up to **10× LLM token reduction** via symbolic pre-filtering; outputs validated against formal knowledge bases. Both managed SaaS and on-prem; pitches EU AI Act, GDPR/HIPAA/SOC 2 readiness as differentiators.

- **Weave.AI** — `weave.ai`. Neuro-symbolic for high-stakes decision-making and risk. Knowledge graphs for relationship mapping; SWOT, gap analysis, red-flag detection built in. Explainability-first pitch.

- **CognitionHub — HiveOS** — `cognitionhub.com`. "Operating system for the AI-native era." Agentic deployment in days; persistent agent memory; model flexibility across OpenAI/Claude/Gemini; multi-agent orchestration.

- **C3 AI — C3 Code** — announced April 2026. Not sold as a cognitive architecture but competes for the same "autonomous thinking + doing" enterprise buyer. Claimed 9.2/10 in an independent eval vs. Codex (6.0), Claude Code (5.2), Palantir (7.7), with a perfect 10 on "Domain Intelligence."

- **Arcee AI — Trinity Large Thinking** — 400B-parameter sparse MoE reasoning model (Apache 2.0, April 2026), 13B active per token, **SMEBU** MoE load balancing, interleaved attention, #2 on PinchBench for autonomous agent capability. Packaged as a component for long-horizon agentic apps.

- **Cloudflare — Project Think** — April 2026. Infrastructure primitives for long-running agents: durable execution, sub-agents, persistent sessions, sandboxed code execution. The "cognitive architecture as a platform primitive" approach — runtime, not model.

## Marketing Quotes (verbatim)

- **Imbue — Keystone**: *"Building self-configuring agents."*
- **Imbue — Sculptor**: *"The missing UI for coding agents."* / *"The missing UI for parallel coding agents."*
- **Cognition — Devin**: *"A tireless, skilled teammate."* / *"Devin can plan and execute complex engineering tasks requiring thousands of decisions."*
- **Reflection AI**: *"Building Frontier Open Intelligence — we're building frontier open intelligence and making it accessible to all."*
- **Adept**: *"AI that powers the workforce."*
- **Sakana AI**: *"Transformative AI that will bring us into the next paradigm."*
- **Symbolica**: *"Intelligence, Redefined."* / *"Unlike large language models, our category-theoretic architectures embed reasoning into the architecture itself."*
- **Extropic**: *"Probabilistic software, meet probabilistic hardware."*
- **AMI Labs / LeCun** (paraphrased, MIT Tech Review, Jan 2026): LLMs are *"a dead end"* and *"sophisticated pattern matchers"* rather than reasoning systems.
- **Inflection AI**: *"We're empowering people and brands with human-centered, emotionally intelligent AI."*
- **Hume AI**: *"The Emotional Intelligence Lab for Voice AI."*
- **Replika 2026 update**: *"Smarter Memory … recalls emotional states and adjusts tone accordingly."*
- **Soul Machines**: *"Experiential AI™"* — digital humans that *"see, listen, react, remember and even empathize."*
- **Inworld AI**: *"The most advanced Character Engine for AI NPCs."* Configurable Reasoning enables *"'state of mind' reasoning (where internal thoughts differ from spoken dialogue)."*
- **Convai**: *"Conversational AI for Virtual Worlds."*
- **AI21 Maestro / "Modular Intelligence"**: *"A human-like model for agent orchestration"* mirroring *"human language production stages — conceptualization, formulation, articulation."*
- **OneReach.ai**: Markets itself explicitly as a *"Cognitive Architecture"* with a *"cognitive orchestration engine."*
- **Adverant Nexus**: *"The Cognitive Layer for AI Infrastructure."*
- **Growth Protocol**: *"The Enterprise Reasoning Platform."*
- **Kortexya**: *"AI That Reasons."*
- **xAI — Grok Multi-Agent** (internal agent design): Lucas is *"deliberately positioned to disagree with others."*
- **Anthropic — Claude**: *"Thoughtful without being evasive"* (describing visible extended thinking design intent).

## Patterns, Trends, Gaps

### Patterns

1. **"Cognitive architecture" is marketing code for one of four things.** (a) Long-horizon reasoning for coding/action agents (Imbue, Cognition, Reflection, Adept, xAI, Anthropic). (b) A full NPC brain with memory + goals + emotion + perception (Inworld, Convai, Soul Machines). (c) Enterprise neuro-symbolic middleware with GraphRAG/formal validation/audit (Adverant, Growth Protocol, Kortexya, Weave, OneReach). (d) A post-transformer substrate bet (Symbolica, Extropic, AMI Labs, Sakana, Hyperon). Almost no vendor crosses between these quadrants.
2. **Visible thinking is becoming table stakes.** Anthropic exposes the chain; xAI exposes four named agents; AI21 exposes traces and validation reports; Symbolica embeds program execution in-architecture; Inworld splits *thought* from *speech*. The "thinking trace" is now a product surface, not an implementation detail.
3. **Named agent personas with epistemic roles are creeping in.** xAI Grok 4.20 (Harper/Benjamin/Lucas/Grok, including a deliberately disagreeing dissenter) and Inworld (goals + motivations + state of mind) both commercialize ideas that used to live in academic multi-agent papers. Anthropomorphizing *the architecture itself* is moving from lab to shipping product.
4. **Modular human-cognition analogies are a sales frame.** AI21's conceptualization/formulation/articulation, OneReach's "cognitive orchestration," Soul Machines' simulated human subsystems, and SingularityNET's PRIMUS all sell the architecture by mapping it onto human cognitive faculties — giving buyers a mental model, whether or not the internals justify it.
5. **The classical AGI cog-arch vocabulary (SOAR/ACT-R/LIDA) has been absorbed into gaming and enterprise, not AGI labs.** Inworld's architecture reads like ACT-R with a dialogue layer; OpenCog Hyperon is the only lab still flying the classical flag, and it lives adjacent to blockchain rather than frontier labs.
6. **Memory is the most contested subsystem.** Replika's "Smarter Memory," Pi's cross-session memory, Inworld's long-term memory, Adverant's GraphRAG, CognitionHub's persistent agent memory, Cloudflare Project Think's durable execution — almost every "cognitive" pitch in 2026 leads with memory because LLM context alone no longer feels like thinking.
7. **Reasoning-first labs rarely talk about tone or affect. Emotion-first platforms rarely publish reasoning benchmarks.** Imbue/Cognition/Reflection brag ARC-AGI-2 and SWE-bench; Hume/Replika/Inflection brag prosody dimensions and emotional categories. The vocabulary gap is almost total.
8. **Capital is bifurcating the substrate.** Frontier/reasoning bets attract mega-rounds (Reflection $2B, AMI $1.03B seed, Anthropic/xAI billions). Emotion/companion bets are smaller and more consumer-subscription-driven (Replika $19.99/mo, Character.AI $9.99/mo, Pi free). Enterprise neuro-symbolic is a third pool, sold by ROI not benchmarks (Growth Protocol's "20× ROI," "170M+ profitable growth").

### Trends

- **"Extended thinking" → "adaptive thinking."** Manual toggles (Claude 3.7) are giving way to adaptive difficulty detection (Claude Opus 4.7, Grok auto-reasoning).
- **Multi-agent as the default "architecture" for reasoning.** Grok 4.20's four-agent design, Maestro's planning trees, Imbue's Sculptor (parallel agents), Symbolica's Agentica multi-agent SDK, Devin's parallel Devins. The cognitive architecture of 2026 is *a team*, not a single model.
- **Emotion productized as a dimension grid.** Hume's EVI 3/4 — 48 emotions × 600+ voice descriptors × 10 voice-control dimensions × multilingual (EVI 4-mini, Jan 2026) — is the clearest sign that affect is being commoditized into sliders.
- **Post-transformer substrate money arrives.** Extropic's Z1 chip (early 2026), AMI Labs' $1.03B seed at $3.5B pre-money (Mar 2026, Europe's largest-ever seed), Symbolica's category-theoretic architecture, Sakana's evolutionary population — 2026 is the first year real capital flows toward *not-a-transformer* bets.
- **Classical cognitive-architecture vocabulary ("goals," "motivations," "state of mind," "perception," "autonomic systems") is being revived by game and digital-human vendors** precisely because LLM-only NPCs felt flat. The humanization insight the games industry reached first: you can't fake believable inner life with a system prompt.
- **Inworld's pivot from NPC engine to general Agent Runtime (2025–2026)** signals that the architectural patterns that made game NPCs believable (goal-driven behavior, state-of-mind/dialogue split, typed long-term memory) are now being repositioned as general-purpose agent infrastructure. The NPC use case was the proving ground; the target is now real-time assistants, voice AI, and enterprise agents.
- **Reasoning-first × affect-first convergence starting.** Hume AI + Anthropic published a joint post on emotionally intelligent Claude Voice interactions (2025). EVI 3 uses Claude as one of its LLM backends. This is the first concrete product collaboration between the two camps that previously had a total vocabulary gap.
- **Memory is now the leading sales argument for every "cognitive" product.** Replika's "Smarter Memory," Inworld's Long-Term Memory, Adverant's GraphRAG, Letta's memory blocks, CognitionHub's persistent agent memory — almost every "cognitive" pitch in 2026 leads with memory. Graph memory specifically is now appearing in enterprise neuro-symbolic pitches.

### Gaps (opportunities for a humanization project)

1. **No one owns "humanlike visible thinking."** Anthropic's extended thinking is clinical; xAI's multi-agent is engineering-flavored. There is no product whose *exposed reasoning trace* reads like how a thoughtful human actually thinks (hedging, dead-ends, side-tracks, self-correction). This is a white-space positioning specifically suited to a humanization-first company.
2. **Reasoning ↔ affect integration is empty.** Hume can modulate voice but doesn't reason over tasks; Imbue/Cognition can reason over tasks but render output flat. A product that makes reasoning *and its tonal register* co-vary with context would sit unopposed.
3. **"State of mind ≠ dialogue" is only commercialized in games.** Inworld's split between internal thought and spoken output is the single most humanization-relevant architectural choice in the market, and it exists only in the game-NPC segment. It is under-exploited in assistants, writing tools, and companions.
4. **Enterprise "cognitive architecture" platforms sell auditability, not voice.** Adverant/Growth Protocol/Kortexya/Weave pitch explainability, token reduction, and compliance. None differentiate on output humanness. A humanization layer that lives *on top of* these platforms has no incumbent.
5. **The persona libraries (Character.AI, Replika) don't own reasoning; the reasoning labs don't own persona.** Whoever ships a product that makes a *persona* reason well — not just converse well — will collapse the current split into a single offering.
6. **Memory is fragmented.** Every cognitive-architecture vendor invents its own memory subsystem (GraphRAG, Smarter Memory, Atomspace, DAS, long-term NPC memory). There is no canonical human-style autobiographical memory layer that a humanization product can plug into — which means one may need to be built.

## Sources

### Reasoning-first agent labs

- `imbue.com/company/introducing-imbue/` — Imbue's company/mission page and $200M funding rationale for reasoning-optimized foundation models.
- `imbue.com/product/keystone/` and `imbue.com/sculptor/` and `imbue.com/product/sculptor/` — Keystone and Sculptor product pages, official taglines, and feature descriptions.
- `imbue.com/research/2026-02-27-arc-agi-2-evolution/` — Feb 2026 ARC-AGI-2 results via code evolution.
- `cognition.ai/introducing-devin`, `cognition.ai/blog/devin-2`, `cognition.ai/blog/introducing-devin-2-2`, `cognition.ai/blog/how-cognition-uses-devin-to-build-devin` — Devin positioning, capabilities, Devin 2.0/2.2 updates, and the "Devin builds Devin" case study.
- `reflection.ai/` and `reflection.ai/blog/reflection-a-path-to-superintelligence/` — Reflection AI homepage, "Frontier Open Intelligence" tagline, and superintelligence thesis.
- `aifundingtracker.com/reflection-ai-2b-funding-autonomous-coding-agents/`, `sacra.com/c/reflection-ai/`, `cbinsights.com/company/reflection-ai` — Reflection AI funding timeline, Nvidia-led $2B Series B, valuation trajectory, and Asimov product.
- `adept.ai` and `adept.ai/act` and `adept.ai/blog/act-1/` — Adept positioning and ACT-1 action transformer.
- `aeo.sig.ai/brands/adept-ai` and `swotanalysis.com/adept-ai` — Adept's Amazon acquihire, $415M funding, and enterprise automation pivot.
- `medium.com/@SarangMahatwo/grok-4-20-beta-xais-native-4-agent-multi-agent-architecture-…` and `buildfastwithai.com/blogs/grok-4-20-beta-explained-2026` and `docs.x.ai/docs/guides/reasoning` and `awesomeagents.ai/models/grok-4-20/` — Grok 4.20 Beta multi-agent architecture, named agent roles, pricing, and benchmarks.
- `anthropic.com/news/claude-opus-4-7`, `anthropic.com/news/visible-extended-thinking`, `docs.anthropic.com/en/docs/about-claude/models/extended-thinking-models` — Claude extended/adaptive thinking product surface.

### Post-transformer structural bets

- `sakana.ai/`, `sakana.ai/seed-round`, `sakana.ai/series-a/`, `sakana.ai/m2n2/`, `sakana.ai/evolutionary-model-merge` — Sakana AI mission, funding, evolutionary model merge work, and M2N2.
- `symbolica.ai/` and `symbolica.ai/research` and `symbolica.ai/blog/arcgentica` and `symbolica.ai/blog/introducing-agentica` and `venturebeat.com/ai/move-over-deep-learning-symbolicas-structured-approach-could-transform-ai` — Symbolica positioning, category-theoretic thesis, Agentica launch, and ARC-AGI-2 result.
- `extropic.ai/` and `extropic.ai/hardware` and `extropic.ai/writing/thermodynamic-computing-from-zero-to-one` and `scalebytech.com/extropic-debuts-probabilistic-tsu-chip…` — Extropic's TSU, p-bit, hardware roadmap, and THRML open-source library.
- `technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/`, `toolhalla.ai/blog/yann-lecun-ami-labs-billion-dollar-world-models-2026`, `novaknown.com/2026/03/11/ami-labs/` — AMI Labs founding, $1.03B seed, JEPA/world-models thesis.
- `singularitynet.io/research/opencog-hyperon/`, `hyperon.opencog.org/`, `singularitynet.io/announcing-the-release-of-opencog-hyperon-alpha/` — OpenCog Hyperon, MeTTa, PRIMUS, DAS.

### Emotion- and persona-first platforms

- `inflection.ai/` and `inflection.ai/blog/pi` — Inflection tagline "human-centered, emotionally intelligent AI" and Pi positioning.
- `megaoneai.com/reviews/inflection-pi-review-2026-…`, `visionsparksolutions.com/reviews/pi-ai/` — Pi 2026 reviews and empathy framing.
- `hume.ai/`, `hume.ai/empathic-voice-interface`, `hume.ai/blog/introducing-hume-evi-api`, `hume.ai/blog/introducing-voice-control`, `dev.hume.ai/docs/speech-to-speech-evi/overview` — Hume EVI, Voice Control, 48 emotions / 600+ voice descriptors, Octave, TADA.
- `companiongeek.com/comparisons/character-ai-vs-replika`, `theaihunter.com/compare/replika-vs-character-ai/`, `aitoolbuds.com/character-ai-vs-replika/` — Character.AI vs Replika 2026 comparisons, PipSqueak model, Smarter Memory.
- `soulmachines.com/digital-workforce`, `soulmachines.com/experiential-ai`, `soulmachines.medium.com/not-all-digital-humans-are-created-equal-…` — Soul Machines Digital Brain™ and Digital Workforce™.

### Game / NPC cognitive-architecture vendors

- `inworld.ai/ai-npc-development`, `inworld.ai/blog/configurable-reasoning-ai-agents`, `inworld.ai/platform`, `docs.inworld.ai/guides/runtime-character`, `aitools-directory.com/tools/inworld-ai-npc-dialogue-behavior/` — Inworld Character Engine, Configurable Reasoning, "state of mind" split, Unreal AI Runtime, Ubisoft NEO NPCs.
- `home.convai.com/`, `home.convai.com/blog/elevating-conversational-npcs-nvidia-ace-for-games-…`, `docs.convai.com/api-docs/convai-playground/character-customization` — Convai platform, NVIDIA ACE integration, multimodal perception, knowledge banks.

### Enterprise cognitive-architecture / neuro-symbolic platforms

- `ai21.com/maestro/`, `docs.ai21.com/docs/maestro-overview`, `ai21.com/blog/modular-intelligence-agent-orchestration/`, `ai21.com/blog/introducing-jamba-reasoning-3b/` — AI21 Maestro, "Modular Intelligence" human-language-production framing, Jamba Reasoning 3B.
- `onereach.ai/cognitive-architecture/` — OneReach.ai "Cognitive Architecture" product page.
- `adverant.ai/en` and `adverant.ai/` — Adverant Nexus "Cognitive Layer for AI Infrastructure."
- `growthprotocol.ai/` and `growthprotocol.ai/about` — Growth Protocol "Enterprise Reasoning Platform."
- `reasoninglayer.ai/` and `kortexya.com/en` — Kortexya / ReasoningLayer neuro-symbolic pitch.
- `weave.ai/` — Weave.AI neuro-symbolic risk/decision platform.
- `cognitionhub.com/` — CognitionHub HiveOS.
- `businesswire.com/news/home/20260408810023/en/C3-AI-Announces-C3-Code-…` — C3 Code April 2026 launch and benchmark.
- `marktechpost.com/2026/04/02/arcee-ai-releases-trinity-large-thinking-…` — Arcee AI Trinity Large Thinking reasoning MoE.
- `blog.cloudflare.com/project-think/` — Cloudflare Project Think primitives for long-running agents.
