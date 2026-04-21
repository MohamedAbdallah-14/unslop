# Category 12 — Cognitive Architectures

**Last updated: April 2026. Content covers April 2025–April 2026. Items from before April 2025 are preserved as historical context where they remain the most authoritative source.**

## Scope

This category covers how AI systems are structured to think — the architectural scaffolding around (or instead of) a raw LLM call. It spans four decades of classical symbolic architectures (Soar, ACT-R, CLARION, Sigma, OpenCog, LIDA), the LLM-era cluster of language agents (ReAct, Reflexion, Voyager, Generative Agents, MemGPT/Letta), Princeton's CoALA as the canonical organizing framework, and commercial instantiations from reasoning-first agent labs to game/NPC character engines to enterprise neuro-symbolic platforms. It also covers post-transformer substrate bets (Symbolica, Extropic, AMI Labs/JEPA, Sakana) and practitioner discourse from Reddit, Hacker News, LessWrong, and YouTube. For the Unslop project, this is the structural counterpart to stylistic humanization: it answers what must be around the LLM for its thinking and output to feel human across long horizons — typed memory, reflection loops, dual-process arbitration, persona grounding, affect — rather than how each sentence should read.

## Executive Summary

Across all five angles, the field has converged on a single thesis: human-like AI behavior is an architectural property, not a prompt property.

- **CoALA is the canonical scaffold.** Sumers, Yao, Narasimhan, and Griffiths (arXiv:2309.02427, TMLR 2024) is cited in all five angles as the organizing frame: working memory + long-term episodic/semantic/procedural stores, internal (reasoning, retrieval, learning) vs external (grounding) actions, and a planning–execution decision cycle. Everything else slots into or extends this vocabulary. (A, B, C, E)
- **Memory is the dominant frontier.** Bigger context windows are not considered a substitute for structured, typed, self-editing memory. MemGPT/Letta's OS-style virtual context, Voyager's procedural skill library, Generative Agents' memory stream, Mnemo's Bayesian atoms, and Inworld's NPC long-term memory all implement different subsets of CoALA's slots — and every practitioner thread on r/LocalLLaMA and HN converges on the same conclusion. (A, B, C, D, E)
- **Dual-process framing is now default.** Kahneman's System 1/System 2 has been absorbed into LangChain's Reflection Agents post (Feb 2024), Tree of Thoughts (NeurIPS 2023), Dualformer (arXiv:2410.09918), ACPO (arXiv:2505.16315), OpenAI o-series, and Anthropic's adaptive extended thinking. Over-reasoning is a named failure mode; adaptive switching beats always-on chain-of-thought. (A, B, E)
- **Structured metacognition measurably feels human.** Reflexion achieves 91% pass@1 on HumanEval vs GPT-4's 80%. Think² (arXiv:2602.18806) reports 84% human preference for trustworthiness. MIRROR (arXiv:2506.00430) reports up to 156% improvement on safety-critical tasks. "Language Models Coupled with Metacognition" (arXiv:2508.17959, Aug 2025) shows a metacognitive scaffold on a standard LLM can outperform a larger specialized reasoning model. Users don't just score it better — they subjectively prefer it. (A, B, E)
- **The market bifurcates almost completely.** Reasoning-first labs (Imbue, Cognition/Devin, Reflection AI, xAI Grok, Anthropic) brag SWE-bench and ARC-AGI-2 but ship flat output. Emotion-first platforms (Hume EVI, Replika, Inflection Pi, Soul Machines) brag 48 emotions × 600+ voice descriptors but publish no reasoning benchmarks. Game/NPC engines (Inworld, Convai) are the only commercial actors shipping full classical-cog-arch stacks — memory, goals, motivation, emotion, perception, and an explicit "state-of-mind ≠ dialogue" split. (D)
- **The critical gap is the bridge between architectural and surface humanization.** The cognitive-architecture literature (A/B/C/D) stops at the output boundary. The writing-craft literature — the r/OpenAI/r/SEO canon on burstiness, transition-word tics, hedging, "delve/tapestry" vocabulary, Frankenstein prompting — starts there and never looks up at memory or metacognition. No paper, post, or product spans both. (B, E)
- **Interview-grounded personas outperform persona prompts.** Park et al.'s 1,052-agent study (arXiv:2411.10109, Nov 2024) grounded in 2,000 hours of qualitative interviews replicates GSS responses at 85% of test–retest reliability and reduces demographic-stereotype bias. Supply data, not adjectives. (A, C)
- **Context engineering has replaced prompt engineering.** Letta and Anthropic independently named this shift in 2025. Practitioners on r/LocalLLaMA identified four failure modes with names: context poisoning, context distraction, context confusion, context clash. Quality degrades at roughly 25% window fill, not at the limit. (B, E)
- **Capital is flowing toward post-transformer bets.** Reflection AI closed a $2B Series B at $8B valuation (Nvidia-led, Oct 2025). AMI Labs (Yann LeCun) closed a $1.03B seed at $3.5B pre-money (Mar 2026, Europe's largest-ever seed), with Bezos, Nvidia, Samsung, Eric Schmidt, and Tim Berners-Lee participating; AMI is building JEPA-based world models as an open-source European alternative to US/China labs. Symbolica raised a $33M Series A for category-theoretic architecture. Whether any of these ships at scale is open. (D)
- **Classical cognitive-architecture vocabulary is being revived — inside gaming and enterprise, not frontier labs.** Inworld's Configurable Reasoning module reads like ACT-R with a dialogue layer. Enterprise platforms (AI21 Maestro, OneReach, Adverant) explicitly market "cognitive architecture" as a product category. Frontier labs borrow the results without the vocabulary. (A, B, C, D)

## Cross-Angle Themes

**T1 — CoALA as lingua franca.** All five angles back-reference CoALA. Angle A cites it as the canonical bridge between classical AI and LLM agents. Angle B shows LangChain's Agent Builder memory openly adopting its three-tier taxonomy. Angle C's `ysymyth/awesome-language-agents` (1.2K★) is the official CoALA companion bibliography with 300+ tagged citations. Angle D's commercial vocabulary mirrors CoALA's terms even when companies don't cite it. Angle E's practitioner threads treat it as the adult framework. Using CoALA's vocabulary is a free compatibility win.

**T2 — Memory typology convergence, now with graph structure as the 2025–2026 frontier.** Working + episodic + semantic + procedural is named independently by ACT-R (1990s), Soar (extended 2008+), CoALA (2023), MemGPT (2023), Mnemo and DeltaMemory (2025), and Adam Lucek's YouTube walkthrough. The 2025 addition: graph memory, which adds relational and temporal edges between typed memory atoms, is in production across Mem0, Zep, and MAGMA. The Mem0 ECAI 2025 benchmark establishes the first head-to-head numbers (vector: 66.9% accuracy; graph: 68.4%) and confirms that contradiction preservation and temporal reasoning require graph edges, not vectors. By early 2026, choosing between vector and graph memory is a standard architectural decision, not a research choice.

**T3 — Reflection and metacognition as the quality lever — now with metacognition as a distinct architectural component.** Reflexion, Generative Agents' reflection tree, CLARION's metacognitive subsystem, LIDA's Global Workspace consciousness phase, Think²'s Planning–Monitoring–Evaluation cycle, MIRROR's between-turn parallel threads, LangChain's Reflexion / LATS trio, Agent-S's reflection agent, IBM SPIRAL's actor–evaluator–reflector triple, SOFAI's metacognitive arbitrator (npj AI 2025). The same pattern appears across every layer of the stack. The 2025 advance: "Language Models Coupled with Metacognition" (arXiv:2508.17959) shows a metacognitive scaffold on a standard LLM outperforms larger reasoning models — making metacognition a cost-effective capability, not just a quality-of-life feature. ICML 2025's "Truly Self-Improving Agents" formalizes that metacognition has three distinct layers (knowledge, planning, evaluation) and most systems only implement the last.

**T4 — Dual-process is the frame for "think longer when it matters" — now with a dedicated survey and a productized metacognitive arbitrator.** Tree of Thoughts (NeurIPS 2023), Dualformer (Oct 2024), ACPO (NeurIPS 2025 poster), Reasoning on a Spectrum (NeurIPS 2025), OpenAI o1/o3, Anthropic adaptive thinking, and LangChain's Reflection Agents post all pitch System-1/2 arbitration. Overthinking is a named failure mode with a TMLR 2025 survey ("Stop Overthinking") dedicated to cataloging it. SOFAI-LM (npj AI 2025) provides the cleanest architectural instantiation — a separate metacognitive agent that selects between a fast LLM and a slow LRM. Adaptive switching outperforms always-on chain-of-thought in every study that tests it, and it also produces less AI-ish output — a direct humanization win.

**T5 — Self-editing agent-authored memory beats passive RAG.** Letta's *RAG is not Agent Memory* post (Feb 2025), Anthropic's first-party memory tool, MetaGPT and ChatDev role memory, Mnemo's Bayesian confidence atoms with contradiction-preserving graph edges, and the r/LocalLLaMA consensus on `search_memory`/`add_memory` as first-class tools — all reject retrieval-only approaches. Passive vector stuffing produces "perfect recall, wrong selection," which feels distinctly non-human.

**T6 — Critic camp: style fixes are fragile without world models.** Marcus (world models), Hawkins/Numenta (Thousand Brains, sensorimotor grounding), LeCun/AMI Labs (JEPA), and Laird (cognitive-architecture hypothesis) form a loose coalition. Their shared argument: no amount of stylistic work compensates for an agent that cannot hold a stable model of the interlocutor and the world it is discussing. Marcus's Anthropic "Project Vend" example — Claude running a vending-machine shop and losing money daily while claiming to wear business clothes — is the clearest industry-sourced case study.

**T7 — Classical vocabulary absorbed by gaming and enterprise, not frontier labs.** Inworld ships memory + goals + motivation + emotion + perception + state-of-mind/dialogue split. OpenCog Hyperon is the only frontier-adjacent project still flying the classical flag. Frontier labs borrow the outcomes without the vocabulary.

**T8 — Named personas with epistemic roles moving from papers to products.** xAI Grok 4.20 ships four named agents including Lucas, "deliberately positioned to disagree with others." Inworld splits internal thought from spoken dialogue. MetaGPT ships CEO/CTO/Programmer/PM. ChatDev ships role-based seminars. Multi-agent is the architecture of 2026, not a prompt pattern.

**T9 — Context engineering as the new design discipline.** Letta and Anthropic both rebranded within 2025. Practitioners named four failure modes. The unit of design is now the structure and lifecycle of the whole context window, not the wording of a system prompt.

**T10 — Sleep/consolidation/offline compute re-emerging, now with a production system.** Letta's Sleep-time Compute (Apr 2025) and Continual Learning in Token Space (Dec 2025) both frame background memory consolidation as a direct sleep analogue — and Letta has shipped multiple products (Letta Evals Oct 2025, Conversations API Jan 2026, Letta Code Dec 2025, Letta Code App Apr 2026) built on this thesis. Sakana's Continuous Thought Machines (May 2025) reintroduce neuron-level timing and synchronization. MemEvolve (Dec 2025) extends the metaphor to memory structure itself: the memory architecture evolves, not just the memories. Neuroscience metaphors that were exiled from the transformer era are now in shipping products.

**T11 — Interview-grounded agents outperform persona-prompted agents.** Park et al.'s 1,052-agent paper is the strongest empirical evidence in this category. It doesn't just beat persona prompts; it measures the margin (85% of test–retest reliability) and shows reduced bias as a side effect. The practical implication for humanization: ground in data, not adjectives.

**T12 — Architectural and surface humanization are separate problems.** Angle E's writing-craft canon (burstiness, sentence-initial "And"/"But", controlled imperfection, Frankenstein prompting) and the cognitive-architecture literature (angles A/B/C/D) almost never cite each other. Unslop sits exactly at this bridge, and the bridge is currently empty.

## Top Sources

### Must-read papers

- **Sumers, Yao, Narasimhan, Griffiths — Cognitive Architectures for Language Agents (CoALA)** — arXiv:2309.02427, TMLR Feb 2024. The canonical framework. Retrospectively classifies 300+ language-agent papers. (A, C, E)
- **Laird, Lebiere, Rosenbloom — A Standard Model of the Mind** — AI Magazine 38(4), 2017, DOI `10.1609/aimag.v38i4.2744`. Pre-LLM consensus distillation of Soar, ACT-R, Sigma. (A)
- **Park et al. — Generative Agents: Interactive Simulacra of Human Behavior** — UIST '23, arXiv:2304.03442. Memory stream + reflection + planning = believable behavior; ablations show all three are necessary. (A, B, C)
- **Park et al. — Generative Agent Simulations of 1,000 People** — arXiv:2411.10109, Nov 2024. 85% of test–retest reliability on GSS; reduced demographic bias vs persona prompts. (A, C)
- **Shinn et al. — Reflexion: Language Agents with Verbal Reinforcement Learning** — arXiv:2303.11366, NeurIPS 2023. 91% pass@1 on HumanEval vs GPT-4's 80%. (A, B, E)
- **Yao et al. — Tree of Thoughts** — arXiv:2305.10601, NeurIPS 2023. Game-of-24: 4% (CoT) to 74% (ToT). Explicit System-1 to System-2 augmentation. (A, B, E)
- **Wang et al. — Voyager** — TMLR 2024, arXiv:2305.16291. 3.3× more unique items, 15.3× faster tech-tree in Minecraft vs prior SOTA. Canonical procedural-memory instantiation. (A, C)
- **Packer et al. — MemGPT: Towards LLMs as Operating Systems** — arXiv:2310.08560, 2023. OS-style virtual context; main context as RAM, external store as disk. (A, B, C)
- **Binz & Schulz — Turning Large Language Models into Cognitive Models** — arXiv:2306.03917, ICLR 2024. Finetunes LLaMA on psychological-experiment data; beats classical cognitive models on two decision-making domains. (A)
- **Dualformer** — arXiv:2410.09918, Oct 2024. 97.6% optimality on mazes using 45.5% fewer reasoning steps than CoT baseline. (A)
- **ACPO — Incentivizing Dual Process Thinking** — arXiv:2505.16315, May 2025. RL framework for adaptive System-1/2 selection based on task difficulty. (A)
- **Zhang et al. — Survey on the Memory Mechanism of LLM-Based Agents** — arXiv:2404.13501, 2024. Six memory operations: consolidation, updating, indexing, forgetting, retrieval, condensation. (A)
- **Lieto et al. — Integrating LLMs with Cognitive Architectures** — arXiv:2308.09830, AAAI Spring Symposium 2023. Three integration paradigms: Modular, Agency, Neuro-Symbolic. (A)
- **Nature Reviews Psychology — Dual-Process Theory and Decision-Making in LLMs** — 2025, DOI `10.1038/s44159-025-00506-1`. (A)
- **Bertolazzi et al. — Fast, Slow, and Metacognitive Thinking in AI (SOFAI)** — npj Artificial Intelligence, 2025. Multi-agent architecture with metacognitive arbitrator. Emergence of human-like skill learning, adaptability, cognitive control without design. Cleanest current instantiation of System-1/2 arbitration with a modular metacognitive layer. (A, B, E)
- **"Memory in the Age of AI Agents: A Survey"** — arXiv:2512.13564 (Dec 2025). Most current comprehensive survey on agent memory; covers R3Mem, MemRL, MemEvolve, MAGMA, MemVerse. Supersedes Zhang et al. 2024 for 2025 developments. (A, C)
- **Chhikara et al. — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory** — ECAI 2025, arXiv:2504.19413. First rigorous head-to-head benchmark of ten memory approaches on LOCOMO. Establishes production-viable numbers: Mem0 graph at 68.4% accuracy, 2.59 s p95 latency, ~1.8K tokens. (A, B, E)
- **"Graph-Based Agent Memory: Taxonomy, Techniques, and Applications"** — arXiv:2602.05665 (Feb 2026). Defines the vector-vs-graph distinction; documents the 2025 inflection where graph memory moved to production. (A, C)
- **Wray, Kirk, Laird — Applying Cognitive Design Patterns to General LLM Agents** — arXiv:2505.07087 (May 2025). Laird et al. formally document that LLM-agent work is unconsciously rediscovering Soar/ACT-R patterns. Bridges the classical and LLM-era literatures from the classical side. (A)
- **"Language Models Coupled with Metacognition Can Outperform Reasoning Models"** — arXiv:2508.17959 (Aug 2025). Metacognitive scaffold on standard LLM beats larger specialized reasoning models on some benchmarks. Establishes metacognition as cost-effective alternative to scale. (A, E)
- **"Truly Self-Improving Agents Require Intrinsic Metacognitive Learning"** — arXiv:2506.05109; ICML 2025. Defines three metacognitive layers (knowledge / planning / evaluation) and argues current agents only implement evaluation. (A, E)

### Key essays and posts

- **Stanford HAI — Computational Agents Exhibit Believable Humanlike Behavior** — Sep 2023. Reframes "humanlike" as an architectural property. Ablations show memory, reflection, and planning are each necessary. (B)
- **LangChain — Reflection Agents** — Ankush Gola, Feb 21, 2024. Industry-standard framing of System-1/2 dual-process for production agents. (B)
- **Letta — Anatomy of a Context Window: A Guide to Context Engineering** — Jul 3, 2025. Kernel/user split; memory blocks as typed slots with labels, size caps, read-only flags. (B)
- **Letta — Stateful Agents: The Missing Link in LLM Intelligence** — Feb 6, 2025. And **Sleep-time Compute** — Apr 21, 2025. The stateful-agent thesis and sleep-consolidation analogue. (B)
- **Anthropic — Effective Context Engineering for AI Agents** — 2025. Context rot, compaction, tool-result clearing, memory tool as named techniques. (B)
- **Gary Marcus — Generative AI's Crippling and Widespread Failure to Induce Robust Models of the World** — Jun 28, 2025. The strongest single argument that stylistic humanization is fragile without world models. (B)
- **Gary Marcus — How o3 and Grok 4 Accidentally Vindicated Neurosymbolic AI** — 2025. (B)
- **Jeff Hawkins — The Thousand Brains Theory of Intelligence** — numenta.com, Jan 16, 2019. And **For Truly Intelligent AI, We Need to Mimic the Brain's Sensorimotor Principles** — numenta.com/Fast Company, Nov 15, 2024. Contrarian substrate argument. (B)
- **janus — Simulators** — LessWrong. GPT-style LLMs as Bayes-optimal text simulators; persona is summoned, not intrinsic. The deepest conceptual frame for humanization-as-conditioning. (E)
- **Seth Herd — Capabilities and Alignment of LLM Cognitive Architectures** — LessWrong. Defines LMCAs; argues humanlike behavior comes from what surrounds the LLM, not from the LLM itself. (E)
- **Think² cluster** — arXiv:2602.18806 (Think²), arXiv:2506.00430 (MIRROR), Medium (MultiMind v2). Structured metacognition with measured human-trust gains: 84% preference (Think²), 156% improvement on safety-critical tasks (MIRROR). (E)
- **Bret Kinsella / Voicebot.ai — Does ChatGPT Mark the End of the Voice Assistant Era?** — Oct 20, 2023. Cognitive trust vs affective trust: Alexa failed by leading with affect; ChatGPT succeeded by leading with cognitive reliability. (B)
- **Mem0 — State of AI Agent Memory 2026** — mem0.ai/blog, early 2026. Documents the transition: graph memory is now production-ready; vector-only is legacy; agentic memory expected to surpass RAG for adaptive AI workflows in 2026. (B, E)
- **Hume AI — Introducing EVI 3** — May 2025. Speech-to-speech foundation model capturing voice, rhythm, tone, personality from 30 s audio without fine-tuning; <300 ms response; the affect-first architecture now at production scale and cross-lingual. (B, D)
- **Hume AI + Anthropic — Emotionally Intelligent Claude Voice** — 2025. First concrete product collaboration between a reasoning-first lab and an affect-first platform; marks the beginning of the reasoning × affect convergence. (B, D)

### Key OSS projects

- **`joonspk-research/generative_agents`** — 21,149★ — Stanford Smallville. Reference implementation for memory stream + reflection + planning. (C)
- **`StanfordHCI/genagents`** — 1,000-person interview-grounded agents from 2,000 hours of real interviews. (C)
- **`letta-ai/letta`** — formerly MemGPT; shipped Letta Code (Dec 2025), Conversations API (Jan 2026), Letta Code App (Apr 2026); stateful agents with typed memory blocks, skills, subagents. (C)
- **`mem0ai/mem0`** — ~48K★, MIT — universal memory layer with vector + graph; ECAI 2025 paper benchmarks ten approaches; the most widely adopted drop-in memory API as of 2026. (C)
- **`MineDojo/Voyager`** — 6,834★, MIT — lifelong-learning skill library; canonical procedural-memory instantiation. (C)
- **`simular-ai/Agent-S`** — Agent-S3 (Oct 2025), first to surpass human performance on OSWorld at 72.60%; Behavior Best-of-N extends to 69.9%; ICLR 2025 Best Paper (Agentic AI Workshop). (C)
- **`SoarGroup/Soar`** — 416★, BSD — classical production-rule cognitive architecture, 40+ years of development; 45th workshop held May 2025 with Princeton's Jonathan Cohen as keynote. (C)
- **`FoundationAgents/MetaGPT`** — 66,700★ — `Code = SOP(Team)`; AFlow accepted to ICLR 2025 oral (top 1.8%). (C)
- **`ysymyth/awesome-language-agents`** — 1,198★, MIT — CoALA companion bibliography, 300+ citations. (C)
- **`trueagi-io/hyperon-experimental`** — v0.2.10, Feb 2026 — MeTTa / OpenCog Hyperon; production-ready stack milestone Nov 2025; most active non-LLM AGI architecture in open source. (C)
- **`Shichun-Liu/Agent-Memory-Paper-List`** — companion to "Memory in the Age of AI Agents" survey (Dec 2025); most current bibliography for agent memory work in 2025–2026. (C)
- **`VoltAgent/awesome-ai-agent-papers`** — curated 2026 agent paper collection; covers engineering, memory, evaluation, workflows. (C)

### Notable commercial tools

- **Inworld AI Agent Runtime** — Pivoted from pure NPC engine to a general Agent Runtime + voice AI platform (2025–2026). Retains Configurable Reasoning, Long-Term Memory, Autonomous Goals, Emotional Fluidity, Spatial Perception, and the "state of mind ≠ dialogue" split — now paired with production TTS (<200 ms) and enterprise security (SOC 2 Type II, HIPAA). Ubisoft NEO NPCs and GDC 2025 production games run on it. Ranked #1 on Artificial Analysis for voice AI latency. (D)
- **Hume AI EVI 3/4** — EVI 3 (May 2025): speech-to-speech foundation model, any voice from 30 s audio, <300 ms response, 48+ emotions, 600+ voice descriptors, 10-dim Voice Control. EVI 4-mini (Jan 2026): 11-language multilingual support. $50M Series B. Joint Anthropic collaboration on emotionally intelligent Claude Voice. The most prosody-centric commercial cognitive architecture shipping today. (D)
- **xAI Grok 4.20 Beta Multi-Agent** — Four named agents sharing a ~3T-parameter MoE backbone: Grok (coordinator), Harper (research), Benjamin (logic/code), Lucas ("deliberately positioned to disagree with others"). Claims ~65% hallucination reduction on multi-step reasoning. (D)
- **AI21 Maestro** — Agent orchestrator framed around human language production stages: conceptualization, formulation, articulation. Budget-controlled reasoning; model-agnostic. Closest commercial framing fit for a humanization project. (D)
- **Anthropic Claude with adaptive extended thinking** — Claude Opus 4.7 (Apr 2026) replaced manual thinking-budget toggles with adaptive difficulty detection. The most widely deployed "visible thinking" product. (D)
- **Reflection AI — Asimov** — Code-research agent backed by $2.13B cumulative funding; $2B Series B at $8B valuation (Nvidia-led, Oct 2025). (D)
- **Symbolica — Agentica** — Category-theoretic architecture; 85.28% on ARC-AGI-2 with Opus 4.6. (D)

### Notable community threads

- **r/LocalLLaMA** — *Finally got my local agent to remember stuff between sessions*, *We gave our RAG chatbot memory*, *How are you handling persistent memory*, *I did an analysis of 44 AI agent frameworks*. Practitioner consensus on typed memory, agentic-memory tools, context partitioning. By early 2026, discussion has shifted to "vector or graph?" as the primary architectural choice. (E)
- **HN Show HN cluster** — Mnemo (Bayesian typed memory, Beta-distribution confidence scores, contradiction-preserving graph), DeltaMemory (89% on long-conversation benchmarks, 50 ms retrieval, 97% cost reduction), Cogency (CoALA as library). (E)
- **r/OpenAI / r/SEO / r/freelancewriters "humanize AI text" canon** — Concrete output-surface diagnostics: uniform sentence length, transition-word tics, "it is important to note," "delve/tapestry," forced neatness; recommended fixes include Frankenstein prompting and deliberate imperfection. (E)
- **Mem0 blog — "State of AI Agent Memory 2026"** — The industry-level summary of the memory landscape as of early 2026; establishes graph memory as production-ready and provides the head-to-head LOCOMO benchmark numbers. (B, E)

## Key Techniques & Patterns

1. **CoALA memory typology.** Expose working, episodic, semantic, and procedural memory as distinct stores with separate policies. Episodic memory produces coherent "I remember when…" callbacks; procedural memory produces compounding competence rather than drifting capability. (A, B, C, E)

2. **Memory stream + reflection (Park et al.).** Append raw observations to a stream; score by recency × importance × relevance at retrieval; periodically LLM-summarize into higher-level beliefs. The reflection pass is what prevents lookup-table behavior. Without it, agents sound like databases. (A, C)

3. **Virtual-context / OS-paging (MemGPT/Letta).** Treat context window as RAM and durable memory as disk, with the LLM explicitly issuing read/write calls via tool calls. Memory blocks have size caps, labels, and read-only flags — cognitive slots with enforced policy, not raw text buffers. (A, B, C)

4. **Lifelong skill libraries (Voyager).** Successful behaviors stored as executable code with natural-language descriptions, indexed by embeddings for retrieval. Failure triggers self-verification and program repair. Skills are "temporally extended, interpretable, and compositional." Compounding competence is a key humanlike property. (A, C)

5. **Reflexion-style verbal RL.** Generate verbal critiques of failures; store them in an episodic buffer; retrieve on next attempt. 91% pass@1 on HumanEval vs GPT-4's 80%. Direct LLM-era implementation of metacognition. (A, B, E)

6. **Tree of Thoughts / deliberate search.** Explicit System-2 augmentation over "thoughts" with self-evaluation and backtracking. Game-of-24: 4% (CoT) to 74% (ToT). The technique that made System-1/2 framing concrete for LLMs. (A, B, E)

7. **Adaptive dual-process switching (Dualformer, ACPO, Reasoning on a Spectrum).** RL-select System-1 vs System-2 based on estimated task difficulty. 97.6% optimality at 45.5% fewer reasoning steps (Dualformer). Combats the overthinking failure mode that always-on CoT creates. (A)

8. **Structured metacognition with named stages — Planning–Monitoring–Evaluation (Think²) and between-turn parallel threads (MIRROR).** Explicit metacognitive scaffolding outperforms implicit CoT and is subjectively preferred by users. Think² reports 3× self-correction improvement and 84% human preference. MIRROR reports up to 156% improvement on safety-critical tasks. (E)

9. **Self-editing agent-authored memory.** `search_memory`/`add_memory` as first-class tool calls, Bayesian confidence updates with contradiction-preserving graph edges (Mnemo), temporal-aware fact extraction (DeltaMemory). Beats passive vector retrieval for coherent long-horizon behavior. (B, E)

10. **Multi-agent role societies and SOPs.** `Code = SOP(Team)` (MetaGPT), CEO/CTO/Programmer seminars (ChatDev), role-playing pairs (CAMEL), named epistemic roles with a deliberate dissenter (xAI Grok's Lucas). Persona-split multi-agent produces diverse voices and structured disagreement. The architecture of 2026 is a team, not a single model. (A, C, D)

11. **State-of-mind ≠ dialogue split (Inworld).** Internal thought differs from spoken output. This is the single most humanization-relevant architectural choice in the commercial market — and it currently exists only in game-NPC products. (D)

12. **Interview-grounded persona.** Derive persona from 2,000 hours of real qualitative interviews rather than demographic adjectives. 85% of test–retest reliability on GSS, reduced demographic-stereotype bias. Supply data, not labels. (A, C)

13. **Context engineering discipline.** Four named failure modes: context poisoning (hallucinations treated as fact), context distraction (overload), context confusion (irrelevant noise), context clash (contradictory content). Quality degrades at roughly 25% window fill. Managed strategies: compaction, tool-result clearing, persistent memory. (B, E)

14. **Sleep-time / offline consolidation.** Background processes reprocess conversation and rewrite memory blocks between user turns, analogous to sleep consolidation. Letta is currently the only production system to operationalize this. (B)

15. **Symbolic governance layer.** Wrap LLM calls in a structured loop — the 5-phase R-CCAM (Retrieval, Cognition, Control, Action, Memory) — for policy compliance. Reports zero policy violations vs ReAct/AutoGPT baselines. (A)

16. **Output-surface humanization.** Sentence-length burstiness, deliberate imperfection, sentence-initial "And"/"But," controlled self-contradiction and tangents, avoidance of "delve/tapestry/plays a crucial role" vocabulary, Frankenstein prompting with user's own writing samples. This is the surface half of the bridge that architectural techniques address from the other side. (E)

## Controversies & Debates

**C1 — Can scaling alone produce human-like cognition?** The scaling camp (Sam Altman; implicit in frontier-lab practice) bets that more parameters and more reasoning RL will close the gap. The architectural camp (Marcus, Hawkins/Numenta, LeCun/AMI Labs, Laird, CoALA authors) argues that without world models, sensorimotor grounding, typed memory, and metacognition, no amount of scale fixes the fundamental failure modes. Marcus's sharpest point: an Atari 2600 (1977, $55 on eBay, 1.19 MHz 8-bit CPU, no GPU) beat ChatGPT at chess. His "o3 and Grok 4 accidentally vindicated neurosymbolic AI" essay argues the scaling camp has been quietly smuggling symbolic machinery back in. (A, B, D)

**C2 — Should the reasoning trace be exposed or hidden?** Anthropic's visible extended thinking and OpenAI's o-series treat the reasoning trace as a product surface. Practitioners on r/singularity and the LessWrong crowd argue the user should see considered output, not the scratchpad — and that leaked scratchpad language ("I need to consider…") is precisely what makes AI output feel AI-ish. Which is the humanization-correct choice is genuinely open. (B, D, E)

**C3 — Affective trust vs cognitive trust: which to lead with?** Voicebot/Kinsella's thesis — Alexa failed by leading with affective trust (personality, empathy); ChatGPT succeeded by leading with cognitive trust (reliability) — runs directly against the emotion-first platform strategy (Hume, Replika, Inflection Pi). Reasoning-first labs treat affect as an afterthought. No product currently ships both at once. (B, D)

**C4 — RAG vs agent-authored memory.** Letta's explicit rejection of RAG as agent memory, and the practitioner consensus on r/LocalLLaMA and HN, is clear. But Mem0, Zep, and most production RAG stacks still operate in the passive paradigm. The gap between recommendation and production deployment is wide. (B, E)

**C5 — Transformer as substrate vs post-transformer bets.** Symbolica (category theory), Extropic (thermodynamic p-bits), AMI Labs (JEPA world models), Sakana (evolutionary populations), OpenCog Hyperon (metagraph rewriting). 2026 is the first year real capital — Reflection AI $2B, AMI $1.03B seed, Symbolica $33M Series A — flows toward not-a-transformer architectures. Whether any of these ships at scale before the transformer train has run much further is the central unresolved question. (D)

**C6 — Persona prompts vs interview-grounded persona.** Park et al.'s 2024 paper empirically beats persona prompts with 2,000 hours of real interviews. Character.AI and Replika scale via prompt-only personas. No consensus exists yet on the minimum viable grounding data for practical deployments. (A, C, D)

**C7 — Classical cog-arch vocabulary: obsolete or foundational?** Laird's view (AI and You Podcast, Ep. 228) is that the cognitive-architecture hypothesis — a fixed set of computational building blocks combined with knowledge — is still the right frame and LLMs are one component of it. Most LLM-agent practitioners use CoALA terms (which originate in this tradition) without ever citing Soar or ACT-R. Inworld and SingularityNET fly the classical flag; frontier labs don't. (A, B, C, D)

**C8 — Multi-agent societies vs single powerful model.** xAI Grok 4.20's four-agent design, MetaGPT, ChatDev, AutoGen, SPIRAL, and MultiMind v2 all bet the team is the architecture. OpenAI and historically Anthropic bet on a single reasoner. Convergence seems to favor multi-agent for long-horizon tasks, but coordination costs and output coherence across agents remain contested. (A, C, D, E)

**C9 — Reflection as quality improvement vs reflection as humanization technique.** LangChain pitches reflection for "knowledge-intensive tasks where response quality is more important than speed." Think²/MIRROR show it also improves subjective trustworthiness — users feel the output is more human. Nobody has yet framed reflection primarily as a humanization technique: the quiet pause, the hedge, the mid-answer self-correction. (B, E)

**C10 — Overthinking as a failure mode.** ACPO, Dualformer, and Reasoning on a Spectrum all name over-reasoning explicitly. Frontier reasoning models burn tokens on trivial inputs. Adaptive arbitration is the proposed fix, but it is not yet the default behavior in any major deployed model. (A)

## Emerging Trends

- **"Extended thinking" to "adaptive thinking."** Manual thinking-budget toggles (Claude 3.7 Sonnet, Feb 2025) give way to adaptive difficulty detection (Claude Opus 4.7, Apr 2026; Grok auto-reasoning). The effort parameter replaces the slider. (D)
- **Multi-agent as the default reasoning architecture.** Grok 4.20's four named agents, Imbue Sculptor (parallel coding agents), AI21 Maestro's planning trees, Devin's parallel Devins, SPIRAL. The cognitive architecture of 2026 is a team. (D)
- **Context engineering supersedes prompt engineering** as the field's name for its core craft. Karpathy coined it; Letta and Anthropic institutionalized it in 2025. (B, E)
- **Stateful agents and learning in token space.** Letta's thesis: agents that improve via memory edits rather than weight updates and that carry memories across model generations will outlast any single foundation model. Confirmed by Letta Code, Conversations API, and Letta Code App (2025–2026). (B)
- **Graph memory moved from experimental to production (2025).** Mem0 ECAI 2025 benchmark, MAGMA (Jan 2026), and Mem0's "State of AI Agent Memory 2026" post together confirm graph memory is now table stakes for agentic applications. Vector-only is now the legacy approach. (A, B, C, E)
- **Metacognition as a distinct architectural layer.** SOFAI (npj AI 2025), "Language Models Coupled with Metacognition" (Aug 2025), and ICML 2025 "Truly Self-Improving Agents" treat the metacognitive module as a first-class component that selects reasoning depth, monitors quality, and reflects on learning. This is the 2025 advance beyond the 2023–2024 "add a reflection prompt" pattern. (A, B, E)
- **Post-transformer substrate capital.** Reflection AI $2B Series B, AMI Labs $1.03B seed at $3.5B pre-money (Mar 2026, Europe's largest-ever seed), Extropic Z1 chip targeted early 2026, Symbolica $33M Series A. The financial bets are now real. (D)
- **Named agent personas with epistemic roles — including deliberate dissenters — shipping in products.** Grok's Lucas, Inworld's state-of-mind split, MetaGPT's PM/CTO differentiation. Anthropomorphizing the architecture itself is moving from lab to product. (D)
- **Classical cognitive-architecture vocabulary reviving inside gaming and enterprise.** Inworld (now an Agent Runtime, not just NPC engine) reads like ACT-R; OneReach.ai markets a "cognitive architecture" product line explicitly. Laird and collaborators (arXiv:2505.07087, May 2025) formally documented that LLM-agent work is unconsciously rediscovering Soar/ACT-R patterns. (D)
- **Computer-use agents crossing human performance baselines.** Agent-S3 on OSWorld at 72.60% (Oct 2025); Behavior Best-of-N extends this to 69.9%. The humanization question shifts from "can it talk like a person" to "can it act like a person over long horizons." (C)
- **Interview-grounded simulacra** as the next step past fictional personas. StanfordHCI/genagents: 3,000+ agents from 2,000 interview hours; still unbeaten as the empirical gold standard (Apr 2026). (A, C)
- **Metacognition recognized as a humanization lever.** Think²'s 84% human preference, MIRROR's 156% safety-critical improvement, and "Language Models Coupled with Metacognition"'s benchmark superiority all establish that structured metacognition is perceived as more human. (E)
- **Consolidation in open-source multi-agent frameworks.** AutoGen merged into Microsoft Agent Framework (Oct 2025); BabyAGI archived (Sep 2024); the 2023 Cambrian explosion has compressed to MetaGPT / Letta / Agent-S / ChatDev 2.0. Dedicated memory frameworks (Mem0, Zep) now exist as a separate category alongside agent frameworks. (C)
- **Neurosymbolic revival across all four layers.** Hyperon/MeTTa v0.2.10 in open source (Feb 2026, production-ready stack milestone Nov 2025), Marcus's "vindication" essay in industry discourse, LLM-ACTR/NL2GenSym/CogRec/cognitive design patterns (Laird May 2025) in academia, Kortexya/Growth Protocol/Weave in enterprise sales. (A, B, C, D)
- **Reasoning-first × affect-first convergence beginning.** Hume AI + Anthropic joint post on emotionally intelligent Claude Voice (2025); Hume EVI 3 uses Claude as LLM backend; Inworld pivoted to a general Agent Runtime. The two previously separate camps are beginning to build on each other's work. Not merged — but no longer a hard wall. (B, D)

## Open Questions & Research Gaps

1. **No standard benchmark for "human-likeness" at the cognitive-architecture level.** Generative Agents uses believability Turing tests; Voyager uses Minecraft metrics; Agent-S uses OSWorld; Park 2024 uses GSS replication. None of these measure voice consistency, memory coherence, or personality stability over long horizons. Unslop likely needs its own eval. (A, C, E)

2. **The bridge between architectural humanization and output-surface humanization is empty.** Cognitive-architecture work stops at the output boundary. Writing-craft work starts there and never looks up. No paper, post, or product has spanned both. This is the specific gap where a Unslop contribution would be novel. (A, B, C, E)

3. **Voice/persona consistency under episodic retrieval.** Much work on storing episodic memory; almost none on retrieving it in a stylistically consistent way so the agent doesn't break voice when surfacing old memories. (E)

4. **Deliberate imperfection as an architectural feature.** The writing community treats hedging, self-contradiction, and tangents as humanizing. The cognitive-architecture community has never modeled these as design variables. (E)

5. **Reasoning ↔ affect integration gap.** CLARION and LIDA have motivational and affective subsystems; no mainstream LLM analog exists. Hume modulates voice but doesn't reason over tasks. Reasoning labs render output flat. This is the clearest white-space in the commercial market. (A, D, E)

6. **"State of mind ≠ dialogue" outside game NPCs.** Inworld's split between internal thought and spoken output is arguably the most humanization-relevant architectural choice in the market. It does not exist in assistants, writing tools, or companions. (D)

7. **Time-aware identity.** DeltaMemory handles temporal reasoning about facts. Nobody has a practitioner pattern for "the agent's beliefs and communication style have evolved over our relationship." This is a real human property with no current analog. (E)

8. **Forgetting is theorized but rarely implemented.** Zhang et al.'s 2024 survey names forgetting as one of six memory operations. In practice, most systems either keep everything or purge arbitrarily via context truncation. Graceful forgetting — the human kind — is essentially unimplemented. (A)

9. **Persona/identity persistence across sessions.** MetaGPT's role personas, Generative Agents' backstories, and Letta's memory blocks approximate identity. None provide a stable "this is who I am across every session" invariant comparable to Soar's goal/impasse structure. (C)

10. **Classical–LLM bridge is thin in practice.** Academic papers (LLM-ACTR, NL2GenSym, CogRec) argue for running Soar or ACT-R in the loop with an LLM, and report results. Almost no open-source project implements this seriously. Forgetting curves, activation spread, and chunking latencies from classical architectures are not being used to constrain LLM output. (A, C)

11. **Reflection quality varies and is rarely evaluated.** Every system has a reflection step. How much reflection is enough? How often? What does reflection drift look like after 10,000 turns? No paper has measured this systematically. (C)

12. **Memory drift and contradiction handling.** Mnemo's Bayesian contradiction-preserving graph is one of the few serious attempts. Most systems either accumulate everything or purge arbitrarily. Humans forget gracefully and hold contradictory beliefs at graded confidence. Both properties are almost absent. (C, E)

13. **Neurosymbolic humanization is undefined.** Marcus argues neurosymbolic is where reliability comes from. Nobody has specified what a neurosymbolic approach to humanization would look like in practice — explicit tone/persona rules plus LLM generation conditioned on them. The category label exists; the design has not been attempted. (B)

14. **Licensing fragmentation.** MIT (Voyager 6.8K★, Letta 22.2K★, genagents), Apache-2 (Agent-S, ChatDev, MetaGPT), GPL-3 (pyactr), BSD (Soar), CC-BY-4.0 (AutoGen), research-only licenses for classical ACT-R. Composing a humanization stack from these is non-trivial. (C)

## How This Category Fits

For the Humanizing AI output and thinking project, Category 12 is the structural backbone. Where other categories address what to say and how to say it — tone, register, copywriting, rhetorical craft — Cognitive Architectures addresses what is doing the saying: the memory, reflection, planning, persona state, affect, and arbitration structures around the LLM call.

Three specific load-bearing roles. First, it provides the vocabulary: CoALA's memory typology and action taxonomy give the project a shared language with the broader research and practitioner ecosystems. Using it is a free compatibility win. Second, it explains why prompt-only humanization fails: the critic camp (Marcus, Hawkins, LeCun, Laird) supplies rigorous arguments for why a stylistic layer on a stateless LLM will always produce the uncanny "perfect recall, wrong selection," contradictory-persona, amnesiac-friend feel that users register as non-human. Third, it marks the white-space: the market bifurcation — reasoning-first labs ship flat output, emotion-first platforms don't reason, game NPCs have the right architecture but ship in games — is the clearest positioning opportunity in the landscape.

Interfaces to sibling categories:

- **Voice / tone / register categories** — output-surface craft (burstiness, imperfection, voice) is the other half of the bridge. Category 12 supplies the underlying reasoning; the tone layer articulates it.
- **Persona / identity categories** — interview-grounded persona (Park 2024) is the empirically strongest base; classical architectures supply stability invariants (goals, impasse, chunking).
- **Memory / continuity categories** — the memory typology and context-engineering discipline live here; any continuity feature plugs into CoALA's slots.
- **Trust / reliability / safety categories** — dual-process arbitration, symbolic governance (SCL), and the visible-vs-hidden thinking debate are shared with trust framings.
- **Evaluation categories** — the open gap on human-likeness benchmarks is a Unslop-owned opportunity.

## Recommended Reading Order

1. **CoALA — Sumers et al., arXiv:2309.02427** (A) — Start here. Everything else slots into this vocabulary.
2. **Stanford HAI post + Generative Agents (UIST '23, arXiv:2304.03442)** (B, A, C) — The canonical architecture-to-believability demonstration. Read the ablations.
3. **Adam Lucek — Building Brain-Like Memory for AI (YouTube, 43:31, ~47.6K views)** (E) — Clearest builder introduction to the four-memory-type taxonomy.
4. **LangChain — Reflection Agents (Feb 21, 2024)** (B) — The industry standard for dual-process framing in production. Short and quotable.
5. **Letta — Anatomy of a Context Window (Jul 3, 2025) + Stateful Agents (Feb 6, 2025)** (B) — The LLM OS metaphor and the stateful-agent thesis.
6. **Anthropic — Effective Context Engineering for AI Agents (2025)** (B) — Context rot, compaction, memory tool; first-party industry validation.
7. **Park et al. — Generative Agent Simulations of 1,000 People (arXiv:2411.10109)** (A, C) — The empirical case for interview-grounded persona over prompt-only persona.
8. **janus — Simulators (LessWrong)** (E) — The deepest conceptual reframe: humanization as conditioning a simulation, not training a human.
9. **Gary Marcus — Generative AI's Crippling and Widespread Failure to Induce Robust Models of the World (Jun 28, 2025)** (B) — The strongest single argument for why style without architecture fails. Read before dismissing it.
10. **Angle D (Commercial) — the gaps section specifically** (D) — The market split and white-space analysis. Read the Inworld and AI21 Maestro subsections in full.
