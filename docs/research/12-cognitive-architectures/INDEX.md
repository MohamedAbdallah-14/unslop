# Category 12 — Cognitive Architectures

## Scope

This category covers **how AI systems are structured to think** — the architectural scaffolding around (or instead of) a raw LLM call. It spans four decades of classical symbolic architectures (Soar, ACT-R, CLARION, Sigma, OpenCog, LIDA), the LLM-era cluster of language agents (ReAct, Reflexion, Voyager, Generative Agents, MemGPT/Letta), the canonical bridge between them (Princeton's **CoALA**), and commercial instantiations from reasoning-first agent labs, emotion-first companion platforms, game/NPC character engines, and enterprise neuro-symbolic middleware. It also pulls in post-transformer substrate bets (Symbolica, Extropic, AMI Labs/JEPA, Sakana) and practitioner discourse from Reddit, Hacker News, LessWrong, and YouTube.

For the Unslop project, "cognitive architectures" is the *structural* counterpart to stylistic humanization: it answers **"what must be around the LLM for its thinking and output to feel human across long horizons?"** — memory, reflection, planning, dual-process arbitration, affect, persona persistence — rather than "how should each sentence read?"

## Executive Summary

Across academia, industry, open source, commercial vendors, and practitioner forums, the field has converged on a shared thesis: **human-like AI behavior is an architectural property, not a prompt property.** Five findings recur with unusual consistency.

1. **A canonical framework exists.** Princeton's **CoALA** (Sumers, Yao, Narasimhan, Griffiths — TMLR 2024, arXiv:2309.02427) is cited across all five angles as the organizing frame: working memory + long-term **episodic / semantic / procedural** stores, **internal** (reasoning, retrieval, learning) vs **external** (grounding) actions, and a planning–execution decision cycle. The 2017 Laird–Lebiere–Rosenbloom *Standard Model of the Mind* is its pre-LLM parent.

2. **Memory is the dominant frontier.** Bigger context windows are not considered a substitute for structured, typed, self-editing memory. MemGPT/Letta's OS-style virtual context, Voyager's procedural skill library, Generative Agents' memory stream + reflection, Mem0/Zep/Mnemo/DeltaMemory on the practitioner side, Hume's long-term companion memory, and Inworld's NPC memory all implement different subsets of the CoALA slots.

3. **Dual-process framing is now default.** System 1 / System 2 (Kahneman) has been absorbed into LangChain's reflection agents, Tree of Thoughts, Dualformer, ACPO, OpenAI o-series reasoning, and Anthropic's adaptive extended thinking. **Over-reasoning** is a named failure mode; adaptive switching beats always-on CoT.

4. **Metacognition/reflection is load-bearing and *feels* human.** CLARION's metacognitive subsystem, LIDA's consciousness phase, Reflexion's verbal RL, Generative Agents' reflection tree, Think² (Planning–Monitoring–Evaluation), and MIRROR (between-turn parallel cognitive threads) all report step-change gains — with Think² measuring 84% human preference for trustworthiness and MIRROR up to 156% improvement on safety-critical tasks. Users subjectively rate structured metacognition as more human.

5. **The market bifurcates almost completely.** Reasoning-first labs (Imbue, Cognition/Devin, Reflection AI, xAI Grok, Anthropic) brag SWE-bench and ARC-AGI-2 but ship flat output. Emotion-first platforms (Hume, Replika, Inflection Pi, Character.AI, Soul Machines) brag 48 emotions × 600+ voice descriptors but don't publish reasoning benchmarks. Game/NPC engines (Inworld, Convai) are the only commercial actors shipping full classical-cog-arch stacks (memory + goals + motivation + emotion + perception + *"state-of-mind ≠ dialogue"* split). **The intersection of deep reasoning and humanlike tone/affect is a white-space opportunity.**

Across all angles, a single strategic implication stands out: a humanization stack should treat the LLM as one component inside a CoALA-shaped architecture (explicit typed memory, reflection, adaptive System-1/2, persona grounded in real interview data), *and* bridge to output-surface craft (burstiness, voice, controlled imperfection) — two literatures that currently do not talk to each other.

## Cross-Angle Themes

**T1 — CoALA as lingua franca.** All five angles back-reference CoALA. Academic (A) cites it as the canonical bridge; industry blogs (B) operationalize it (LangChain's Agent Builder memory is openly CoALA-based); open source (C) tags repos against it via `awesome-language-agents`; commercial (D) uses its vocabulary even when not citing it; practitioners (E) treat it as the adult organization of agents. **If Unslop picks any vocabulary, picking CoALA's is a free compatibility win.**

**T2 — Memory typology convergence.** Working + episodic + semantic + procedural is independently named by ACT-R (1990s), Soar (2008+), CoALA (2023), MemGPT (2023), Mnemo/DeltaMemory (2025), Adam Lucek's brain-like memory video (E), and LangChain's production memory system. Divergence is only in *which* long-term store each emphasizes.

**T3 — Reflection and metacognition as the quality lever.** Reflexion, Generative Agents' reflection tree, CLARION's metacognitive subsystem, Think²'s Planning–Monitoring–Evaluation, MIRROR's between-turn parallel threads, LangChain's Basic Reflection / Reflexion / LATS trio, Agent-S's reflection agent, IBM's SPIRAL (actor–evaluator–reflector) — same pattern across the stack.

**T4 — Dual-process is the frame for "think longer when it matters."** Tree of Thoughts (NeurIPS 2023), Dualformer (2024), ACPO (2025), Reasoning on a Spectrum (NeurIPS 2025), OpenAI o1/o3, Anthropic adaptive thinking, LangChain's Reflection Agents post — all pitch System-1/2 arbitration as the target, with overthinking flagged as a failure mode.

**T5 — Self-editing / agent-authored memory beats passive RAG.** Letta's *RAG is not Agent Memory* (Feb 2025), Anthropic's memory tool, MetaGPT/ChatDev role memory, Mnemo's Bayesian atoms, Reddit consensus on agentic-memory tools (`search_memory` / `add_memory`) over passive vector stuffing — convergent rejection of retrieval-only approaches.

**T6 — Critic camp: no amount of style fixes the absence of a world model.** Marcus (world models), Hawkins/Numenta (Thousand Brains, sensorimotor grounding), LeCun/AMI Labs (JEPA), Laird (cognitive-architecture hypothesis). All argue the substrate is the problem. For humanization: persona-prompt humanization is fragile if the agent cannot hold a stable model of the interlocutor and the world.

**T7 — Classical vocabulary has been absorbed into gaming and enterprise, not frontier labs.** Inworld's Configurable Reasoning + Long-Term Memory + Autonomous Goals + Emotional Fluidity + Spatial Perception reads like ACT-R-with-dialogue. OpenCog Hyperon is the only frontier-adjacent lab still openly classical. Frontier labs borrow the *results* of classical thinking without the *vocabulary*.

**T8 — Named personas with epistemic roles are moving from papers to products.** xAI Grok 4.20 ships Grok/Harper/Benjamin/**Lucas (the dissenter)**, Inworld ships "state-of-mind ≠ dialogue," MetaGPT ships CEO/CTO/Programmer/PM, ChatDev ships multi-role seminars. Multi-agent is the *architecture* of 2026, not a prompt pattern.

**T9 — Context engineering has replaced prompt engineering.** Letta and Anthropic independently rebrand within 2025; r/LocalLLaMA's four named failure modes (*context poisoning, distraction, confusion, clash*) give practitioners a shared diagnostic vocabulary; Karpathy coined the term. The unit of design is the whole context window's structure and lifecycle.

**T10 — Sleep/consolidation/offline compute is re-emerging.** Letta's *Sleep-time Compute* (Apr 2025), *Continual Learning in Token Space* (Dec 2025), and Sakana's Continuous Thought Machines (neuron-level timing, May 2025) bring neuroscience metaphors back into the transformer era after years of exile.

**T11 — Interview-grounded agents > persona-prompted agents.** Stanford's *Generative Agent Simulations of 1,000 People* (arXiv:2411.10109) replicates real-person GSS responses at 85% of test–retest reliability and reduces demographic-stereotype bias vs persona prompts. *Supply data, not adjectives.*

**T12 — Architectural humanization and output-surface humanization are separate problems.** The cognitive-architecture literature (A/B/C/D) barely touches burstiness, hedging, or voice; the writing-craft literature (the r/OpenAI / r/SEO "AI tells" canon in E) barely touches memory or metacognition. Unslop sits precisely in this bridge.

## Top Sources (Curated)

### Must-read papers

- **Sumers, Yao, Narasimhan, Griffiths — Cognitive Architectures for Language Agents (CoALA)** — arXiv:2309.02427, TMLR 2024. The canonical framework. [Angle A, C, E]
- **Laird, Lebiere, Rosenbloom — A Standard Model of the Mind** — AI Magazine 38(4), 2017, DOI `10.1609/aimag.v38i4.2744`. Pre-LLM consensus distillation of Soar/ACT-R/Sigma. [Angle A]
- **Park et al. — Generative Agents: Interactive Simulacra of Human Behavior** — UIST '23, arXiv:2304.03442. Smallville. Memory stream + reflection + planning = believability. [Angle A, B, C]
- **Park et al. — Generative Agent Simulations of 1,000 People** — arXiv:2411.10109 (Nov 2024). 85% of test–retest reliability on GSS. Empirical case for interview-grounded persona. [Angle A, C]
- **Shinn et al. — Reflexion: Language Agents with Verbal Reinforcement Learning** — arXiv:2303.11366, NeurIPS 2023. Metacognition + episodic memory buffer. [Angle A, B, E]
- **Yao et al. — Tree of Thoughts** — arXiv:2305.10601, NeurIPS 2023. Explicit System-1 → System-2 augmentation. [Angle A, B, E]
- **Wang et al. — Voyager** — TMLR 2024, arXiv:2305.16291. Canonical procedural-memory / skill-library instantiation. [Angle A, C]
- **Packer et al. — MemGPT: Towards LLMs as Operating Systems** — arXiv:2310.08560. OS-style virtual context. [Angle A, B, C]
- **Binz & Schulz — Turning Large Language Models into Cognitive Models** — arXiv:2306.03917, ICLR 2024. LLMs as models of human cognition. [Angle A]
- **Nature Reviews Psychology — Dual-Process Theory and Decision-Making in LLMs** — 2025, DOI `10.1038/s44159-025-00506-1`. [Angle A]
- **Dualformer / ACPO / Reasoning on a Spectrum** — arXiv:2410.09918, 2505.16315, OpenReview `DQuWpKLNwd`. Adaptive System-1/2 switching. [Angle A]
- **Zhang et al. — Survey on the Memory Mechanism of LLM-Based Agents** — arXiv:2404.13501. Six memory operations. [Angle A]
- **Lieto et al. — Integrating LLMs with Cognitive Architectures** — arXiv:2308.09830. Modular / Agency / Neuro-Symbolic taxonomy. [Angle A]

### Must-read posts/essays

- **Stanford HAI — Computational Agents Exhibit Believable Humanlike Behavior** (Sep 2023). Companion framing for Generative Agents; reframes "humanlike" as architectural. [Angle B]
- **LangChain — Reflection Agents** (Feb 21, 2024). The industry standard-bearer for dual-process framing in production. [Angle B]
- **Letta — Anatomy of a Context Window: A Guide to Context Engineering** (Jul 3, 2025). Kernel/user split for LLM OS. [Angle B]
- **Letta — Stateful Agents: The Missing Link in LLM Intelligence** (Feb 6, 2025) and **Sleep-time Compute** (Apr 21, 2025). [Angle B]
- **Anthropic — Effective Context Engineering for AI Agents** (2025). Context rot, compaction, tool-result clearing, memory tool. [Angle B]
- **Sakana AI — Introducing Continuous Thought Machines** (May 2025). Neuron-level timing and synchronization. [Angle B]
- **Jeff Hawkins / Numenta — For Truly Intelligent AI, We Need to Mimic the Brain's Sensorimotor Principles** (Nov 15, 2024) and **The Thousand Brains Theory of Intelligence** (Jan 16, 2019). The strongest substrate-critic voice. [Angle B]
- **Gary Marcus — Generative AI's Crippling and Widespread Failure to Induce Robust Models of the World** (Jun 28, 2025) and **How o3 and Grok 4 Accidentally Vindicated Neurosymbolic AI** (2025). [Angle B]
- **janus — Simulators** (LessWrong). GPT-style LLMs as Bayes-optimal text simulators; persona is *summoned*, not intrinsic. [Angle E]
- **Seth Herd — Capabilities and Alignment of LLM Cognitive Architectures** (LessWrong). Defines LMCAs. [Angle E]
- **MIRROR / Think² / MultiMind v2 cluster** (arXiv/Medium, 2025–2026). Structured metacognition with measured trust gains. [Angle E]
- **Voicebot.ai — Does ChatGPT Mark the End of the Voice Assistant Era?** (Bret Kinsella, Oct 2023). Cognitive trust vs. affective trust. [Angle B]

### Key open-source projects

- **`joonspk-research/generative_agents`** — 21.1K★ — Stanford Smallville reference implementation. Memory stream + reflection + planning. [Angle C]
- **`StanfordHCI/genagents`** — 1,000-person interview-grounded agents (2024). [Angle C]
- **`letta-ai/letta`** (formerly MemGPT) — 22.2K★, Apache 2.0 — stateful agents with memory blocks, skills, subagents. [Angle C]
- **`MineDojo/Voyager`** — 6.8K★, MIT — lifelong-learning skill library. [Angle C]
- **`simular-ai/Agent-S`** — 10.8K★, Apache 2.0 — first to surpass human on OSWorld (72.6%). [Angle C]
- **`SoarGroup/Soar`** — 416★, BSD — classical production-rule cognitive architecture, 40+ years. [Angle C]
- **`jakdot/pyactr` / `CarletonCognitiveModelingLab/python_actr`** — Python ACT-R implementations. [Angle C]
- **`trueagi-io/hyperon-experimental`** — 250★, pre-alpha — MeTTa / OpenCog Hyperon. [Angle C]
- **`opencog/atomspace`** — 962★ — hypergraph knowledge DB. [Angle C]
- **`FoundationAgents/MetaGPT`** — 66.7K★ — `Code = SOP(Team)` software-company multi-agents. [Angle C]
- **`OpenBMB/ChatDev`** — 32.5K★ — CEO/CTO/Programmer multi-agent, now zero-code DevAll platform. [Angle C]
- **`camel-ai/camel`** — 16.6K★ — role-playing multi-agent framework (NeurIPS 2023). [Angle C]
- **`Significant-Gravitas/AutoGPT`** — 183.5K★ — pioneering autonomous-loop platform. [Angle C]
- **`microsoft/autogen`** — 57.2K★ (maintenance, merging into Microsoft Agent Framework). [Angle C]
- **`IBM/SPIRAL`** (AAAI 2026) and **`ReCAP-Stanford/ReCAP`** (NeurIPS 2025). [Angle C]
- **`ysymyth/awesome-language-agents`** — 1.2K★ — CoALA companion bibliography. [Angle C]

### Notable commercial tools

- **Reasoning-first agent labs:** Imbue (Sculptor, Keystone), Cognition Labs (Devin), Reflection AI (Asimov, $2B Series B at $8B from Nvidia), Adept (ACT-1, now Amazon acquihire), xAI Grok 4.20 Beta Multi-Agent (Grok/Harper/Benjamin/Lucas), Anthropic Claude with adaptive extended thinking. [Angle D]
- **Post-transformer substrate bets:** Symbolica (category theory, 85.3% on ARC-AGI-2 with Agentica), Extropic (thermodynamic TSUs, Z1 chip), AMI Labs (LeCun, $1.03B seed, JEPA), Sakana AI (evolutionary model merging, M2N2), SingularityNET OpenCog Hyperon / PRIMUS. [Angle D]
- **Emotion-first platforms:** Hume AI (EVI, 48 emotions × 600+ voice descriptors × 10-dim Voice Control, Octave, TADA), Inflection Pi, Character.AI (PipSqueak), Replika (Smarter Memory, 2026), Soul Machines (Digital Brain™, Experiential AI). [Angle D]
- **Game/NPC engines:** **Inworld AI Character Engine** (Configurable Reasoning + Long-Term Memory + Autonomous Goals + Emotional Fluidity + Spatial Perception + *state-of-mind ≠ dialogue* split; Ubisoft NEO NPCs). Convai (NVIDIA ACE integration, 500+ voices, 65+ languages). [Angle D]
- **Enterprise neuro-symbolic / orchestration:** AI21 Maestro (+ Jamba Reasoning — conceptualization/formulation/articulation framing), OneReach.ai (explicit "Cognitive Architecture" product line), Adverant Nexus, Growth Protocol, Kortexya ReasoningLayer, Weave.AI, CognitionHub HiveOS, C3 AI's C3 Code, Arcee Trinity Large Thinking, Cloudflare Project Think. [Angle D]

### Notable community threads

- **r/LocalLLaMA memory threads** — *Finally got my local agent to remember stuff*, *We gave our RAG chatbot memory*, *How are you handling persistent memory across local Ollama sessions*, *I did an analysis of 44 AI agent frameworks*. Practitioner consensus on Mem0/Letta/Zep and on context partitioning as the hard part. [Angle E]
- **HN Show HN cluster** — Mnemo (Bayesian typed memory), DeltaMemory (temporal fact extraction), Cogency (CoALA-as-library), *A three-layer memory architecture for long-running agents*, *Does anyone have an understanding of what the agentic loop looks like?* [Angle E]
- **LessWrong architecture essays** — janus *Simulators*, Seth Herd on LMCAs, Leventov's *LLM-based exemplary actor*. [Angle E]
- **r/MachineLearning — Approaches to add logical reasoning into LLMs.** Long thread on System-1 default and System-2 scaffolding. [Angle E]
- **r/OpenAI / r/SEO / r/freelancewriters "humanize AI text" community canon** — burstiness, transition-word tics, hedging, "delve/tapestry" vocabulary, Frankenstein prompting, controlled imperfection. [Angle E]
- **r/PhilosophyofMind — treating LLMs as extended cognition.** Cognitive amplifier framing. [Angle E]
- **AI and You Podcast Ep. 228 — John Laird, Cognitive Architect (Part 2).** The cognitive-architecture hypothesis from its original champion. [Angle B]
- **YouTube — Adam Lucek, *Building Brain-Like Memory for AI* (43:31, 47K views).** Canonical four-memory-type walkthrough. [Angle E]

## Key Techniques & Patterns

1. **CoALA memory typology (working / episodic / semantic / procedural).** Expose each as a distinct store with its own policy, not as a single context window. Episodic memory produces "I remember when…" coherence; procedural memory produces competence that compounds rather than drifts. [A, B, C, E]

2. **Memory stream + reflection (Park et al.).** Append raw natural-language observations; score on recency × importance × relevance at retrieval; periodically LLM-summarize into higher-level beliefs. The reflection pass is what prevents lookup-table affect. [A, C]

3. **Virtual-context / OS-paging (MemGPT/Letta).** Treat context window as RAM and durable memory as disk with the LLM explicitly issuing read/write calls. Memory blocks have size caps, labels, and read-only flags — cognitive slots with policy, not raw text. [A, B, C]

4. **Lifelong skill libraries (Voyager).** Successful behaviors stored as executable code with NL descriptions, indexed for retrieval; self-verification and program repair on failure. Compounding competence is a key humanlike property. [A, C]

5. **Reflexion-style verbal RL.** Verbally reflect on failures; store reflections in an episodic buffer. 91% pass@1 on HumanEval vs GPT-4's 80%. [A, B, E]

6. **Tree of Thoughts / deliberate search.** Explicit System-1 → System-2 augmentation over "thoughts" with self-evaluation + backtracking. Game-of-24: 4% (CoT) → 74% (ToT). [A, B, E]

7. **Dual-process adaptive switching (Dualformer, ACPO, Reasoning on a Spectrum).** RL-select System-1 vs System-2 based on estimated task difficulty; combats overthinking. [A]

8. **Structured metacognition — Planning–Monitoring–Evaluation (Think²) and between-turn parallel threads (MIRROR).** Explicit named metacognitive stages outperform implicit CoT and are subjectively preferred by users. [E]

9. **Multi-agent role societies / SOPs.** `Code = SOP(Team)` (MetaGPT), CEO/CTO/Programmer seminars (ChatDev), role-playing pairs (CAMEL), conversable agents (AutoGen), named epistemic roles including a dissenter (xAI Grok's Lucas). Persona-split multi-agent yields diverse voices and structured disagreement. [A, C, D]

10. **Self-editing agent-authored memory (over passive RAG).** `search_memory`/`add_memory` as first-class tools, Bayesian belief updating with preserved contradictions (Mnemo), temporal fact extraction (DeltaMemory). [B, E]

11. **Sleep-time / offline consolidation.** Background processes rewrite memory blocks and form connections between user turns — human-sleep analogue. [B]

12. **Context engineering discipline.** Four named failure modes (*poisoning, distraction, confusion, clash*); quality degrades at ~25% window fill; compaction + tool-result clearing + persistent memory as named strategies. [B, E]

13. **Interview-grounded persona.** Ground personas in 2,000 hours of real qualitative interviews (Park 2024) rather than persona adjectives — 85% of test–retest reliability, reduced demographic-stereotype bias. [A, C]

14. **"State of mind ≠ dialogue" split (Inworld).** Internal thought differs from spoken output — the single most humanization-relevant architectural choice in the commercial market, currently only in game-NPC products. [D]

15. **Neuron-level timing & synchronization (Sakana CTM).** Neurons with access to their own history; variable "ticks" let the model think longer on harder problems. Human-like trajectories (e.g., maze-tracing) emerge without being designed in. [B]

16. **Symbolic governance layer (Structured Cognitive Loop, CLARION-inspired stacks).** Wrap LLM calls in a 5-phase R-CCAM loop (Retrieval, Cognition, Control, Action, Memory) for zero-policy-violation runs. [A]

17. **Output-surface humanization.** Sentence-length burstiness, deliberate imperfection (em-dashes, sentence-initial *And*/*But*), controlled self-contradiction and tangents, avoidance of "delve/tapestry/plays a crucial role" vocabulary, Frankenstein prompting with user's own samples. [E]

## Controversies & Debates

**C1 — Can scaling alone produce human-like cognition, or is the architecture the bottleneck?**
The **scaling camp** (Altman; implicit in frontier-lab practice) bets that more parameters + more reasoning RL will close the gap. The **architectural camp** (Marcus, Hawkins/Numenta, LeCun/AMI Labs, Laird, CoALA authors) argues that without world models, sensorimotor grounding, typed memory, and metacognition, no amount of scale fixes the failure modes (hallucination, brittle world-modeling, losing at Atari 2600 chess). Marcus's "o3 and Grok 4 accidentally vindicated neurosymbolic AI" essay claims the scaling camp has been smuggling symbolic machinery back in. [B, A, D]

**C2 — Extended/explicit thinking vs hidden reasoning.**
Anthropic's visible extended thinking and OpenAI's o-series bet that showing the reasoning trace is a product surface; practitioners (E, Post 9) argue the user should see *considered output, not the scratchpad*, and that leaked scratchpad language ("I need to consider…") is precisely what makes AI output feel AI-ish. Open question: should metacognition be *exposed* (Anthropic) or *hidden* (practitioner preference)? [B, D, E]

**C3 — Affective vs cognitive trust (which to lead with).**
Voicebot/Kinsella's thesis — Alexa failed because it led with affective trust; ChatGPT succeeded because it led with cognitive trust — cuts directly against emotion-first platforms (Hume, Replika, Inflection Pi). Reasoning-first labs treat affect as an afterthought. Unslop must decide which to lead with. [B, D]

**C4 — RAG vs agent-authored memory.**
Letta's *RAG is not Agent Memory* (Feb 2025) and the r/LocalLLaMA / HN consensus reject passive vector retrieval as a memory substitute. Mem0, Zep, and most production RAG stacks still operate in the passive paradigm. Convergence is underway but not settled. [B, E]

**C5 — Transformer as substrate vs post-transformer substrates.**
Symbolica (category theory), Extropic (thermodynamic p-bits), AMI Labs (JEPA), Sakana (evolutionary populations), OpenCog Hyperon (metagraph rewriting). Capital is now flowing toward *not-a-transformer* bets in 2026. Whether any of these ship at scale is open. [D]

**C6 — Persona prompts vs interview-grounded persona.**
Park 2024 empirically beats persona prompts with 2,000 hours of real interviews. Character.AI and Replika scale via prompt-only personas. Inworld uses richer character sheets. No consensus yet on the minimum viable grounding data. [A, C, D]

**C7 — Classical cog-arch vocabulary: dead, dormant, or foundational?**
Laird's view (Ep. 228) is that the cognitive-architecture hypothesis (a fixed set of computational building blocks + knowledge) is still the right frame and LLMs are one component. Most of the LLM-agent field uses CoALA terms (which originated in this tradition) without ever citing Soar/ACT-R. Inworld/SingularityNET fly the classical flag; frontier labs don't. [A, B, C, D]

**C8 — Multi-agent societies vs single powerful model.**
xAI Grok 4.20's four-agent flagship, MetaGPT, ChatDev, AutoGen, SPIRAL, MultiMind v2 bet that the *team* is the architecture. OpenAI and (historically) Anthropic bet on a single reasoner. Convergence seems to favor multi-agent for long-horizon tasks, but coordination costs and output coherence remain contested. [A, C, D, E]

**C9 — Reflection as quality improvement vs reflection as humanization.**
LangChain's reflection agents pitch it for "knowledge-intensive tasks." Think²/MIRROR show it *also* improves subjective trustworthiness. No one has yet reframed reflection primarily as a humanization technique (the quiet pause, the hedge, the self-correction). [B, E]

**C10 — Overthinking.**
ACPO, Dualformer, and Reasoning on a Spectrum explicitly name *over-reasoning* as a failure mode. Frontier "reasoning" models often burn tokens on trivial inputs; adaptive arbitration is the proposed fix but not yet default. [A]

## Emerging Trends

- **"Extended thinking" → "adaptive thinking."** Manual toggles (Claude 3.7) give way to adaptive difficulty detection (Claude Opus 4.7, Grok auto-reasoning). [D]
- **Multi-agent as the default architecture for reasoning.** The cognitive architecture of 2026 is a *team*, not a single model. [D]
- **Context engineering supersedes prompt engineering** as the discipline's name. [B, E]
- **Stateful agents / learning in token space.** Letta's thesis — agents that improve via memory edits rather than weight updates and that carry their memories across model generations. [B]
- **Sleep-time / offline compute** re-emerges with explicit neuroscience framing. [B]
- **Post-transformer substrate money arrives.** Reflection AI $2B Series B, AMI Labs $1.03B seed, Extropic Z1, Symbolica Series A. [D]
- **Named agent personas with epistemic roles** (including deliberate dissenters) shipping in products. [D]
- **Classical cognitive-architecture vocabulary revives inside gaming and enterprise**, not frontier labs. [D]
- **Grounded computer-use agents crossing human baselines.** Agent-S3 on OSWorld (72.6%) marks the shift from "can it talk like a person" to "can it act like a person over long horizons." [C]
- **Interview-grounded simulacra** (StanfordHCI/genagents, 2,000 hours) as the next step past fictional personas. [A, C]
- **Metacognition measurably improves perceived trustworthiness.** Think² (84% preference), MIRROR (+156% on safety-critical). Structured metacognition is being recognized as a *humanization* lever, not just a capability lever. [E]
- **Consolidation in open-source multi-agent frameworks.** AutoGen merging into Microsoft Agent Framework; BabyAGI archived; the 2023 Cambrian explosion is compressing to MetaGPT / Letta / Agent-S / ChatDev 2.0. [C]
- **Neurosymbolic revival.** Hyperon/MeTTa, Marcus's "vindication" essay, Kortexya/Growth Protocol/Weave selling neuro-symbolic to enterprise. [A, B, C, D]

## Open Questions / Research Gaps

1. **No standard benchmark for "human-likeness" at the cognitive-architecture level.** Generative Agents uses believability Turing tests; Voyager uses Minecraft; Agent-S uses OSWorld; Park 2024 uses GSS replication. None measure voice/memory/personality stability over long horizons. **Unslop likely needs its own eval.** [A, C, E]

2. **Bridge between architectural humanization and output-surface humanization is empty.** Cognitive-architecture work stops at the output boundary; writing-craft work starts there. No one has published how metacognitive structure should (or should not) leak into user-facing voice. [A, B, C, E]

3. **Voice/persona consistency under episodic retrieval.** Lots of work on *storing* episodic memory; little on *retrieving it in a stylistically consistent way* so the agent doesn't break voice when surfacing old memories. [E]

4. **Deliberate imperfection as an architectural feature.** The writing community knows hedging/tangents/self-contradiction humanize output; the cog-arch community never treats them as design variables. [E]

5. **Affective / motivational subsystems of CLARION and LIDA have no mainstream LLM analog.** Emotional modeling remains fragmented and prompt-level, not architectural. Hume modulates voice but doesn't reason over tasks; reasoning labs render output flat. The **reasoning ↔ affect integration gap** is the clearest white-space. [A, D, E]

6. **"State of mind ≠ dialogue" exists only in game-NPC products.** Under-exploited in assistants, writing tools, and companions. [D]

7. **Time-aware identity / evolving persona.** No practitioner pattern for "the agent's beliefs/style have evolved over our relationship." DeltaMemory handles time for facts, not for self. [E]

8. **Forgetting is theorized but rarely implemented** beyond ad-hoc context truncation. Zhang 2024 survey names six memory operations; forgetting is usually stubbed. [A]

9. **Persona/identity persistence across long sessions.** MetaGPT's role personas, Generative Agents' backstories, Letta's memory blocks approximate identity, but none provide a stable "this is who I am across every session" invariant comparable to Soar's goal/impasse structure. [C]

10. **Classical–LLM bridge is thin in practice.** Almost no open-source project runs Soar/ACT-R in the loop with an LLM despite academic papers (LLM-ACTR, NL2GenSym, CogRec) arguing for it. Forgetting curves, activation spread, chunking latencies are not constraining LLM output. [A, C]

11. **Reflection quality varies wildly and is rarely evaluated.** How much reflection? How often? What does reflection drift look like after 10,000 turns? [C]

12. **Memory drift and contradiction handling.** Most systems either keep everything or purge arbitrarily. Humans forget gracefully. Mnemo's contradiction-preserving graph is one of the few serious attempts. [C, E]

13. **Procedural-memory compositionality is weak.** Voyager's skill library composes via LLM prompting rather than formal structure (unlike Soar's chunking). [C]

14. **Neurosymbolic humanization is undefined.** Marcus argues neurosymbolic is where reliability comes from; no one has written what a *neurosymbolic approach to humanization* (explicit tone/persona rules + LLM generation conditioned on them) would look like. [B]

15. **Sleep/consolidation/offline processing** is nearly unexplored outside Letta. Most humans feel coherent partly because of overnight consolidation; no current humanization stack simulates that. [B]

16. **Licensing fragmentation.** MIT (Voyager, Letta, genagents), Apache-2 (Agent-S, ChatDev, MetaGPT), GPL-3 (pyactr), BSD (Soar), CC-BY-4.0 (AutoGen), research licenses for classical ACT-R. Composing a humanization stack across these is non-trivial. [C]

17. **Voice-AI industry writing barely touches LLM memory architectures**, and vice versa. Voicebot/Kinsella frames via trust/interface; Letta/LangChain barely touch voice. The voice + cognitive-architecture intersection is under-written. [B]

## How This Category Fits in the Bigger Picture

For the *Humanizing AI output and thinking* project, Category 12 is the **structural backbone**. Where other categories handle what to say and how to say it (tone, register, copywriting, rhetorical craft), Cognitive Architectures handles **what is doing the saying** — the memory, reflection, planning, persona state, affect, and arbitration structures around the LLM call.

Three specific load-bearing roles:

1. **Provides the vocabulary.** CoALA's memory typology (working/episodic/semantic/procedural) and action taxonomy (internal reasoning/retrieval/learning vs external grounding) give the project a shared language with the broader research and practitioner ecosystems. Using it buys free compatibility.

2. **Explains why prompt-only humanization fails.** The critic camp (Marcus, Hawkins, LeCun, Laird) supplies rigorous arguments for why a stylistic layer on a stateless LLM will always produce the uncanny "perfect recall, wrong selection," contradictory-persona, amnesiac-friend feel that users register as AI-ish. Unslop's differentiation story rests on this structural argument.

3. **Marks the white-space.** The market bifurcation (reasoning-first labs ship flat output; emotion-first platforms don't reason; game NPCs have the right architecture but ship in games) is the clearest positioning opportunity in the entire landscape. A product that makes a *persona* reason well — with adaptive System-1/2, typed memory, sleep-time consolidation, interview-grounded persona, and a metacognitive layer that *feels* human without leaking scratchpad — would collapse the bifurcation.

Interfaces to other categories:

- **→ Voice / tone / register categories:** output-surface craft (burstiness, imperfection, voice) is the other half of the bridge; Category 12 supplies the reasoning that the tone layer articulates.
- **→ Persona / identity categories:** interview-grounded persona (Park 2024) is the empirically-strongest base; classical architectures supply the stability invariants (goals, impasse, chunking).
- **→ Memory / continuity categories:** the memory typology and context-engineering discipline live here; any continuity feature plugs into CoALA's slots.
- **→ Trust / reliability / safety categories:** dual-process arbitration, symbolic governance (SCL), and visible-vs-hidden thinking debates are shared with trust framings.
- **→ Evaluation categories:** the open gap on human-likeness benchmarks is a Unslop-owned opportunity.

## Recommended Reading Order

**First pass — orient (≈2–3 hours).**

1. **CoALA — Sumers et al., arXiv:2309.02427** (A). The canonical scaffolding; everything else slots into this vocabulary.
2. **Stanford HAI post + Generative Agents (UIST '23, arXiv:2304.03442)** (B, A, C). Canonical "architecture → believability" demonstration.
3. **Adam Lucek — *Building Brain-Like Memory for AI* (YouTube, 43:31)** (E). Clearest introduction to the four-memory-type taxonomy for builders.
4. **LangChain — *Reflection Agents* (Feb 2024)** (B). Production-side dual-process framing.
5. **Letta — *Anatomy of a Context Window* (Jul 2025) + *Stateful Agents* (Feb 2025)** (B). OS metaphor and the stateful-agent thesis.
6. **Anthropic — *Effective Context Engineering for AI Agents*** (B). Context rot, compaction, memory tool.

**Second pass — deep dive (≈6–10 hours).**

7. **Reflexion (arXiv:2303.11366)** and **Tree of Thoughts (arXiv:2305.10601)** (A). Metacognition + deliberate search.
8. **Voyager (TMLR 2024, arXiv:2305.16291)** (A, C). Procedural-memory canon.
9. **MemGPT (arXiv:2310.08560)** (A, C). Virtual-context paging.
10. **Park et al. — *Generative Agent Simulations of 1,000 People* (arXiv:2411.10109)** (A, C). Interview-grounded persona.
11. **Laird–Lebiere–Rosenbloom — *A Standard Model of the Mind* (2017)** (A). Pre-LLM distillation.
12. **Laird — *ACT-R vs Soar* (arXiv:2201.09305)** (A). Classical-architecture orientation.
13. **Lieto et al. — *Integrating LLMs with Cognitive Architectures* (arXiv:2308.09830)** (A). Integration taxonomy (Modular / Agency / Neuro-Symbolic).
14. **Zhang et al. — *Survey on the Memory Mechanism of LLM-Based Agents* (arXiv:2404.13501)** (A). Memory-operations taxonomy.
15. **Dualformer / ACPO / Reasoning on a Spectrum** (A). Adaptive System-1/2.
16. **MIRROR (arXiv:2506.00430) + Think² (arXiv:2602.18806)** (E). Structured metacognition with user-trust metrics.
17. **janus — *Simulators* (LessWrong)** + **Seth Herd — *LMCAs* (LessWrong)** (E). Conceptual framings.
18. **Marcus — *Crippling … Failure to Induce Robust Models of the World* (Jun 2025) + Hawkins — *Thousand Brains* posts** (B). Strong contrarian voices.

**Third pass — competitive landscape and practice (≈6–8 hours).**

19. **Angle D (Commercial)** top-to-bottom. Especially the reasoning-first / emotion-first / game-NPC / enterprise split and the "gaps" section.
20. **Inworld AI Character Engine docs** (`inworld.ai/ai-npc-development`, *Configurable Reasoning* blog) (D). The single most reusable commercial blueprint.
21. **AI21 — *Modular Intelligence* post + Maestro docs** (D). Closest framing fit for humanization.
22. **Hume AI EVI + Voice Control docs** (D). Affect commoditized.
23. **xAI Grok 4.20 Multi-Agent write-ups** (D). Named epistemic roles + dissenter.
24. **r/LocalLLaMA memory thread cluster + HN Cogency/Mnemo/DeltaMemory** (E). Practitioner reality check.
25. **Angle C open-source tour** — clone and skim Generative Agents, Letta, Voyager, Agent-S, MetaGPT.

**Fourth pass — speculative substrate (optional, ≈3–4 hours).**

26. **Sakana — Continuous Thought Machines (May 2025)** + **Sakana evolutionary model merge (Nature MI 2025)** (B, D).
27. **Symbolica, Extropic, AMI Labs, OpenCog Hyperon** (D). Post-transformer substrates.

## File Index

- `A-academic.md` — Academic & scholarly framing: CoALA, Standard Model of the Mind, classical architectures (Soar, ACT-R, CLARION, Sigma, OpenCog, LIDA), LLM+cog-arch hybrids (LLM-ACTR, NL2GenSym, CogRec, SCL), language-agent instantiations (ReAct, Reflexion, ToT, Voyager, Generative Agents, MemGPT), LLMs-as-cognitive-models, dual-process for LLMs, and 2024–2026 surveys. **Research value: high.**
- `B-industry.md` — Industry blogs and essays: Stanford HAI, LangChain (Reflection Agents, Agent Builder memory), Letta (context engineering, stateful agents, sleep-time compute, MemGPT), Sakana (Continuous Thought Machines, evolutionary model merge), Numenta/Hawkins (Thousand Brains, sensorimotor), Gary Marcus (world models, neurosymbolic vindication), Anthropic (context engineering), AI and You podcast with Laird, Voicebot/Kinsella (cognitive vs affective trust). **Research value: high.**
- `C-opensource.md` — Open-source and GitHub: classical (Soar, pyactr, python_actr, Hyperon, AtomSpace), simulacra (generative_agents, genagents), long-horizon memory (Letta, Voyager, Agent-S), multi-agent societies (AutoGPT, BabyAGI, MetaGPT, ChatDev, CAMEL, AutoGen), theory scaffolding (awesome-language-agents, SPIRAL, ReCAP, Cognitive_workbench). **Research value: high.**
- `D-commercial.md` — Commercial landscape: reasoning-first labs (Imbue, Cognition/Devin, Reflection AI, Adept, xAI Grok, Anthropic), post-transformer substrate bets (Sakana, Symbolica, Extropic, AMI Labs/LeCun, SingularityNET Hyperon), emotion-first (Inflection Pi, Hume EVI, Character.AI, Replika, Soul Machines), game/NPC engines (Inworld, Convai), enterprise neuro-symbolic/orchestration (AI21 Maestro, OneReach, Adverant, Growth Protocol, Kortexya, Weave, CognitionHub, C3 AI, Arcee Trinity, Cloudflare Project Think). **Research value: high.**
- `E-practical.md` — Practitioner forums and how-tos: r/LocalLLaMA memory threads, r/MachineLearning / r/singularity dual-process and reasoning discussions, LessWrong architectural essays (janus *Simulators*, Seth Herd LMCAs, Leventov exemplary actor), HN Show HN cluster (Cogency, Mnemo, DeltaMemory), metacognition papers (MultiMind v2, Think², MIRROR), context-engineering consensus, r/OpenAI / r/SEO humanize-AI writing canon, YouTube primers (Adam Lucek, LLM-agent survey), CoALA as primary reference. **Research value: high.**
