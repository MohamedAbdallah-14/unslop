# Agentic Autonomous Thinking — Angle C: Open-Source Repos

**Category:** Agentic Autonomous Thinking
**Angle:** C — Open-Source Ecosystem
**Project lens:** Humanizing AI output and thinking
**Compiled:** April 2026
**Research value:** high — the open-source agent stack is deep, converging, and provides multiple direct reference points for "thinking" as a visible, human-legible process rather than a hidden chain-of-thought.

---

## TL;DR for Unslop

The OSS agent ecosystem has roughly three waves stacked on top of each other:

1. **Wave 1 (2023): Goal-loopers.** AutoGPT, BabyAGI, AgentGPT — a single agent recursively plans and executes. Noisy, loopy, but established the "thinking out loud" aesthetic Unslop can mine.
2. **Wave 2 (2023–2024): Role-play societies.** MetaGPT, ChatDev, CAMEL, CrewAI, AutoGen — multiple agents with personas argue toward a deliverable. Personas are the humanization surface.
3. **Wave 3 (2024–2026): Infrastructure.** LangGraph, OpenAI Agents SDK (Swarm successor), smolagents, Letta, Agno, LlamaIndex agents — opinionated runtimes for state, memory, handoffs, and observability.

A fourth, smaller strand — **Voyager, SWE-agent, OpenHands, Thoughtful Agents, AgentKit** — treats *how an agent thinks* (curriculum, skill library, System 1/2, graph-of-thoughts) as the primary artifact. This strand is the most directly useful for a project about humanizing AI thinking.

---

## Repo Catalog (22 repos)

Stars are approximate as of April 2026; see "Sources" for verification links.

### Wave 1 — Classic autonomous goal-loopers

#### 1. Significant-Gravitas/AutoGPT
- **Stars:** ~183k · **License:** MIT/Polyform (mixed) · **Language:** Python + TS
- **Pitch (README):** *"AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters."*
- **Thinking model:** Single-agent ReAct-style loop: think → plan sub-tasks → execute tool → evaluate. Exposes reasoning as visible monologue.
- **Relevance to humanization:** The original "agent thinks in first person" UX. Also the clearest demonstration of the *anti-*patterns humanization needs to solve: repetitive self-talk, loop collapse, token waste.

#### 2. yoheinakajima/babyagi
- **Stars:** ~22k · **License:** MIT · **Language:** Python
- **Pitch (repo/README):** Minimalist task-creation, task-prioritization, task-execution loop using OpenAI + a vector store for memory.
- **Thinking model:** Explicit task queue; agent "thinks" by rewriting its own todo list after each step.
- **Relevance:** Cleanest possible reference implementation of the "planner → worker → reprioritizer" triad. Easy to fork as a humanization testbed.

#### 3. reworkd/AgentGPT *(archived Jan 2026)*
- **Stars:** ~36k · **License:** GPL-3.0 · **Language:** TypeScript + Python
- **Pitch:** *"Assemble, configure, and deploy autonomous AI Agents in your browser."*
- **Relevance:** Browser-first surface for autonomous agents — the UX layer most casual users actually met. Archival matters: indicates the market has moved from "watch an agent think" toys toward workflow infrastructure.

#### 4. TransformerOptimus/SuperAGI
- **Stars:** ~17k · **License:** MIT · **Language:** Python + JS
- **Pitch:** *"A dev-first open-source autonomous AI agent framework"* with toolkit marketplace, vector-DB memory, and telemetry.
- **Relevance:** Early attempt to put the goal-looper inside a production envelope (GUI, telemetry, resource usage). A useful negative reference for how quickly "autonomous agents" became "agent platforms."

### Wave 2 — Multi-agent role-play societies

#### 5. FoundationAgents/MetaGPT
- **Stars:** ~67k · **License:** MIT · **Language:** Python
- **Pitch (README):** *"🌟 The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming."*
- **Thinking model:** Role-based SOPs — PM, architect, engineer, QA each have scripted prompt templates and handoff contracts. Produces reviewable artifacts (PRDs, designs, code), not raw chat.
- **Relevance:** The strongest OSS argument that **humanization = personas + standard operating procedures**, not just tone. Worth studying for how they scaffold "what would a PM actually write here?"

#### 6. OpenBMB/ChatDev
- **Stars:** ~33k · **License:** Apache-2.0 · **Language:** Python
- **Pitch (README):** *"ChatDev 2.0: Dev All through LLM-powered Multi-Agent Collaboration."* Recently relaunched as a zero-code orchestration platform ("DevAll").
- **Thinking model:** "Communicative agents" playing waterfall software roles; dialogue *is* the artifact. Strong academic lineage (Tsinghua/OpenBMB).
- **Relevance:** The clearest example of dialogue-as-reasoning — agents humanize each other through critique, not solo monologue.

#### 7. camel-ai/camel
- **Stars:** ~17k · **License:** Apache-2.0 · **Language:** Python
- **Pitch (README):** *"🐫 CAMEL: The first and the best multi-agent framework. Finding the Scaling Law of Agents."*
- **Thinking model:** Role-playing "Inception prompting" where a user-agent and assistant-agent co-evolve task specs. Includes a *Deductive Reasoner Agent* and a new *Deep Research Agent* (plan → execute → replan → summarize).
- **Relevance:** Research-grade framework; the deductive-reasoner and deep-research modules are directly relevant to visible-thinking design.

#### 8. crewAIInc/crewAI
- **Stars:** ~49k · **License:** MIT · **Language:** Python
- **Pitch (README):** *"Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks."*
- **Thinking model:** Role + goal + backstory per agent; tasks route via a "process" (sequential / hierarchical). Benchmarked in 2026 as the fastest-to-prototype framework but also the lowest in conditional-workflow control.
- **Relevance:** The "backstory" field is the most explicit humanization primitive in any mainstream framework.

#### 9. microsoft/autogen
- **Stars:** ~57k · **License:** MIT (+ CC-BY-4.0 docs) · **Language:** Python + .NET
- **Pitch (README):** *"A programming framework for agentic AI."*
- **Thinking model:** Conversation-first; agents exchange typed messages; loops and nested chats are first-class. v0.4 rewrite in 2024–25 added distributed actors.
- **Relevance:** The most flexible substrate for "what would the conversation between these two minds look like" — but also the one most prone to runaway chatter without humanization guardrails.

### Wave 3 — Infrastructure & runtimes

#### 10. langchain-ai/langgraph
- **Stars:** ~30k · **License:** MIT · **Language:** Python + TS
- **Pitch (README):** *"Build resilient language agents as graphs."*
- **Thinking model:** Explicit state machine — nodes (LLM calls, tools) + edges (conditional routing) + typed state. Native persistence and human-in-the-loop checkpoints.
- **Relevance:** The reigning production choice (per 2026 benchmarks, ~91% task completion with verification nodes, leads production deployments by ~40%). For Unslop, the relevant lesson is that *human-legible thinking is easier to enforce inside a graph than inside a free-running loop.*

#### 11. openai/swarm → openai/openai-agents-python (successor)
- **Stars:** ~21k (Swarm, archived) · **License:** MIT
- **Pitch (Swarm README):** *"Educational framework exploring ergonomic, lightweight multi-agent orchestration."* Officially superseded by the production **OpenAI Agents SDK**.
- **Thinking model:** Two primitives — `Agent` (instructions + tools) and **handoffs** (one agent transfers context to another, exposed to the LLM as a tool like `transfer_to_refund_agent`).
- **Relevance:** Handoffs as a humanization primitive: the agent *declares* "I'm the wrong person for this" — mirrors how human experts escalate. Low-ceremony, easy to adopt.

#### 12. huggingface/smolagents
- **Stars:** ~27k · **License:** Apache-2.0 · **Language:** Python
- **Pitch (README):** *"🤗 smolagents: a barebones library for agents that think in code."*
- **Thinking model:** Code-as-action — the agent emits Python snippets that call tools, rather than JSON tool calls. ~1k LoC core. Model-/modality-/tool-agnostic, sandboxed via E2B/Docker/WASM.
- **Relevance:** Code-as-action is a *less human* interface on the surface, but reliably produces more coherent reasoning because Python forces structure. A useful counterpoint to "humanize via more natural language."

#### 13. letta-ai/letta (formerly MemGPT)
- **Stars:** ~22k · **License:** Apache-2.0 · **Language:** Python
- **Pitch (README):** *"Letta is the platform for building stateful agents: AI with advanced memory that can learn and self-improve over time."*
- **Thinking model:** Tiered memory — core (identity/goals), archival (long-term facts), recall; agents edit their own memory as a tool call. Rebranded from MemGPT Sept 2024.
- **Relevance:** The closest thing in OSS to "an agent that remembers you like a person would." Persistent identity is a prerequisite for humanization beyond a single turn.

#### 14. agno-agi/agno
- **Stars:** ~40k · **License:** MPL-2.0 · **Language:** Python
- **Pitch (README):** *"Build, run, manage agentic software at scale."* Positioned as a multi-agent framework with a runtime and control plane.
- **Claimed edge:** *529× faster agent instantiation vs LangGraph* (vendor claim); strong memory/knowledge system.
- **Relevance:** The "operational" end of the spectrum. Useful to study for how it treats an agent as a deployable unit rather than a script.

#### 15. run-llama/llama_index (agents module)
- **Stars:** ~46k (whole project) · **License:** MIT · **Language:** Python + TS
- **Pitch:** RAG-first framework that grew an agent layer (`AgentWorkflow`, `FunctionAgent`, ReAct, multi-agent handoffs).
- **Relevance:** Humanization via grounding — agents that cite and defer to documents read more honest than agents that assert from memory. Closest OSS parallel to "answer like a careful analyst."

### Wave 4 — Thinking-as-artifact (most relevant to Unslop)

#### 16. xlang-ai/OpenAgents
- **Stars:** ~4.7k · **License:** Apache-2.0 · **Language:** Python + TS · **Venue:** COLM 2024 (XLang Lab, HKU)
- **Pitch:** Three deployed agents — Data Agent (Python/SQL), Plugins Agent (200+ APIs), Web Agent. Ships a chat UI designed for *"swift responses and error handling."*
- **Relevance:** One of the few OSS stacks that treats the *human reading the agent's work* as a first-class design target.

#### 17. MineDojo/Voyager
- **Stars:** ~6.8k · **License:** MIT · **Language:** JS + Python · **Venue:** NeurIPS 2023
- **Pitch (paper/README):** *"An Open-Ended Embodied Agent with Large Language Models."*
- **Thinking model:** Three pillars — (1) an **automatic curriculum** that sets the agent's own goals, (2) an **ever-growing skill library** of executable code, (3) **iterative prompting with self-verification**. Reported 3.3× more unique items, 15.3× faster tech-tree progression vs prior Minecraft agents.
- **Relevance to humanization:** The strongest argument in OSS that *an agent becomes more humanlike when it builds and names its own skills over time*. Skill naming is identity.

#### 18. princeton-nlp/SWE-agent (now SWE-agent/SWE-agent)
- **Stars:** ~19k · **License:** MIT · **Language:** Python · **Venue:** NeurIPS 2024
- **Pitch (README):** *"SWE-agent takes a GitHub issue and tries to automatically fix it, using your LM of choice."* Introduced the **Agent-Computer Interface (ACI)** concept.
- **Thinking model:** Rather than maximize raw LLM power, *design the tools the LLM uses* so every action is short, reversible, and legible. Huge SWE-bench gains came from the interface, not a smarter model.
- **Relevance:** The key insight — "legible tools produce legible thinking" — is directly transferable to humanization work.

#### 19. All-Hands-AI/OpenHands (formerly OpenDevin)
- **Stars:** ~71k · **License:** MIT · **Language:** Python + TS
- **Pitch (README):** *"🙌 OpenHands: AI-Driven Development."*
- **Thinking model:** **CodeAct** — unify reasoning and action as executable code + bash in a sandbox. Pluggable agents (CodeActAgent, PlannerAgent, BrowsingAgent). OpenDevin CodeAct 1.0 reached 21% SWE-Bench-Lite.
- **Relevance:** The most battle-tested autonomous coding agent in OSS; the CodeAct loop is one of the cleanest "observable thinking" patterns available.

#### 20. Bessouat40/TreeThinkerAgent
- **Stars:** small (<1k) · **License:** MIT · **Language:** Python
- **Pitch (README):** *"A lightweight orchestration layer that turns any LLM into an autonomous multi-step reasoning agent… exposing the entire reasoning process as a tree you can explore."*
- **Relevance:** The entire value proposition is *making thinking legible*. Tree-of-thought UX is under-represented in big frameworks; this is a mineable reference.

#### 21. holmeswww/AgentKit
- **Stars:** ~1k · **License:** CC-BY · **Language:** Python · **Venue:** NAACL 2024
- **Pitch:** *"Constructs complex thought processes from simple natural language prompts"* by stacking graph nodes ("LEGO pieces") that enforce structured reasoning.
- **Relevance:** Graph-of-thought designable by non-programmers. Could inform a Unslop "thought scaffold" authoring interface.

#### 22. xybruceliu/thoughtful-agents
- **Stars:** ~40 · **License:** MIT · **Language:** Python · **Venue:** CHI 2025
- **Pitch (README):** *"A Python framework for building proactive LLM agents that simulate human-like cognitive processes. Enables agents to continuously generate and evaluate thoughts in parallel with conversations, and autonomously determining when and how to engage."*
- **Thinking model:** Five explicit stages (Trigger → Retrieval → Thought Formation → Evaluation → Participation) with a **System 1 / System 2** split.
- **Relevance:** The single most on-thesis repo for Unslop — a research-grade reference implementation of "thoughts happening in parallel with conversation" that is exactly the humanization target.

---

## Patterns

1. **Visible-reasoning UX has converged on three idioms.**
   - Monologue (AutoGPT / BabyAGI) — reads as a journal; now seen as dated.
   - Dialogue between agents (MetaGPT / ChatDev / CAMEL / AutoGen) — reads as a meeting transcript; cognitively richer.
   - Graph / tree of nodes (LangGraph / AgentKit / TreeThinkerAgent) — reads as a plan; best for auditability.

2. **Persona is the cheap humanization lever and everyone uses it.** Every wave-2 framework exposes `role + goal + backstory`-type fields. Humanization at the persona layer is table stakes; the differentiator is whether the persona *persists* (Letta) and *evolves* (Voyager's skill library).

3. **Code-as-action is winning for correctness, losing for readability.** smolagents, OpenHands (CodeAct), and SWE-agent all argue that emitting code is more reliable than emitting JSON tool calls. But code output feels less "humanlike" to non-technical users — an explicit tension Unslop has to pick a side on.

4. **Memory is where the serious OSS effort is in 2025–26.** Letta/MemGPT, Agno, LangGraph checkpointing, LlamaIndex workflows. The shift is away from "smarter loop" toward "agent that remembers and has continuity."

5. **Handoffs > God-Bot.** OpenAI Agents SDK, CrewAI's hierarchical process, MetaGPT's SOPs all say the same thing: specialization + handoff is more legible (and cheaper) than one agent doing everything. This mirrors how humans actually work.

6. **Observability is part of the agent, not an add-on.** LangSmith (LangGraph), Swarm's stateless client-side design, Agno's control plane, OpenAI Agents SDK's tracing — modern frameworks ship with tracing out of the box. Unslop should assume traced execution as the baseline.

## Trends

- **Market consolidation is underway.** AgentGPT archived (Jan 2026), Swarm retired in favor of OpenAI Agents SDK, LangGraph dominating production deployments (~91% task completion with verification nodes; reached v1.0 in late 2025 and v1.1.3 in 2026 with distributed runtime support), OpenHands dominating coding-agent mindshare at ~70k+ stars. The "thousand frameworks" era is ending.
- **Research → runtime migration.** MemGPT → Letta, SWE-agent → OpenHands integration, Voyager's skill-library idea absorbed by CAMEL and others. Research ideas now reach production runtimes within ~12 months.
- **2026 frameworks ship evaluation harnesses.** SWE-bench, AgentBench, τ-bench are now assumed; "does it run on SWE-bench?" has become a de-facto credibility test. OpenHands shipped the OpenHands Index (January 2026) to broaden beyond SWE-bench: issue resolution, greenfield app dev, frontend tasks, and testing.
- **Thinking-as-artifact is a small but distinct substrand.** Thoughtful Agents (CHI 2025), AgentKit, TreeThinkerAgent all treat *how the agent thinks* (not what it produces) as the primary output. Directly on-thesis for Unslop.
- **New framework entrants from frontier labs.** 2025 saw three major new SDKs: OpenAI Agents SDK (March 2025, production successor to the educational Swarm repo), Google Agent Development Kit / ADK (April 2025, A2A-native), and Anthropic Claude Agent SDK (April 2026, same tools as Claude Code, programmable in Python/TypeScript). These are not community projects — they are officially supported production runtimes backed by the frontier model providers. Developers adopting them trade framework flexibility for first-class model integration.
- **Security tooling is arriving.** Microsoft released the Agent Governance Toolkit (April 2026) as open-source runtime security for agents, framework-agnostic with hooks into LangChain, CrewAI, and Google ADK. The prior absence of this layer was a known gap; its arrival marks agents entering enterprise compliance and security workflows.
- **MCP as universal tool-use protocol.** Anthropic's Model Context Protocol (MCP, November 2024) crossed 97M monthly SDK downloads and 5,800+ servers by late 2025. OpenAI, Google, and Microsoft all adopted it; it was donated to the Linux Foundation's Agentic AI Foundation in December 2025. Most frameworks now treat MCP servers as the standard tool interface rather than bespoke function schemas.

## Gaps (Unslop opportunities)

1. **No mainstream framework models "thinking style" as a first-class parameter.** Personas have role/goal/backstory, but not *pace*, *hedging*, *self-revision*, *aesthetic preferences*. Thoughtful Agents is the only serious attempt. This is the most defensible gap.
2. **Very little OSS work on *un-*polished output.** Everything optimizes for final-answer quality; almost nothing models the messy intermediate thinking a human produces (crossed-out ideas, half-ideas, reconsiderations). The visible monologue of AutoGPT was closer to this than any current framework — the UX has regressed.
3. **Memory is treated as facts, not opinions.** Letta stores "what the user said"; no mainstream OSS agent persists "what I came to believe and why" in a way another agent can critique.
4. **Handoffs are triggered by task, not by emotional/interpersonal read.** An agent can route to a "refund agent" but not to a "kinder agent" or a "more skeptical agent." Humanization requires handoffs driven by register and relationship, not just skill.
5. **The "parallel stream of thought while in dialogue" idea (Thoughtful Agents) has no production-grade implementation.** CHI 2025 research exists; there is no LangGraph/CrewAI plugin for it. This is a buildable gap.

---

## Sources

- **Agents Index — AutoGPT vs MetaGPT (2026):** https://agentsindex.ai/compare/autogpt-vs-metagpt — strengths/limitations of AutoGPT and MetaGPT in production.
- **AIAgentsKit — BabyAGI vs AutoGPT vs AgentGPT (2026):** https://aiagentskit.com/blog/babyagi-vs-autogpt-vs-agentgpt — star counts, ecosystem status, API-cost anecdotes.
- **agent-harness.ai benchmark — CrewAI vs LangGraph vs AutoGen (2026):** https://agent-harness.ai/blog/multi-agent-orchestration-frameworks-benchmark-crewai-vs-langgraph-vs-autogen-performance-cost-and-integration-complexity/ — production latency/cost table cited above.
- **iBuidl — AI Agent Frameworks 2026:** https://ibuidl.org/blog/ai-agent-frameworks-comparison-20260310 — framework philosophy summary + production-deployment share.
- **openai/swarm (GitHub):** https://github.com/openai/swarm — Swarm design + migration notice to OpenAI Agents SDK.
- **OpenAI Agents SDK docs:** https://openai.github.io/openai-agents-js/guides/handoffs/ — handoff model + `transfer_to_*` convention.
- **huggingface/smolagents:** https://github.com/huggingface/smolagents — "agents that think in code" tagline + architecture overview.
- **letta-ai/letta:** https://github.com/letta-ai/letta — stateful-agent pitch + memory tiers.
- **FoundationAgents/MetaGPT:** https://github.com/FoundationAgents/MetaGPT — role-based SOP framework.
- **OpenBMB/ChatDev:** https://github.com/OpenBMB/ChatDev — ChatDev 2.0 / DevAll repositioning.
- **crewAIInc/crewAI:** https://github.com/crewAIInc/crewAI — role/goal/backstory primitives.
- **microsoft/autogen:** https://github.com/microsoft/autogen — conversation-first agentic programming.
- **langchain-ai/langgraph:** https://github.com/langchain-ai/langgraph — graph-as-agent orchestration.
- **MineDojo/Voyager + project page:** https://github.com/MineDojo/Voyager and https://voyager.minedojo.org/ — curriculum + skill library + self-verification.
- **SWE-agent/SWE-agent:** https://github.com/SWE-agent/SWE-agent — Agent-Computer Interface concept.
- **All-Hands-AI/OpenHands (OpenDevin):** https://github.com/All-Hands-AI/OpenHands — CodeAct 1.0 on SWE-Bench Lite (xwang.dev blog: https://xwang.dev/blog/2024/opendevin-codeact-1.0-swebench).
- **camel-ai/camel:** https://github.com/camel-ai/camel — CAMEL framework + Deep Research Agent PR (https://github.com/camel-ai/camel/pull/2235).
- **xlang-ai/OpenAgents:** https://github.com/xlang-ai/OpenAgents — three-agent deployment + multi-stakeholder design (COLM 2024).
- **TransformerOptimus/SuperAGI:** https://github.com/transformeroptimus/superagi — toolkit marketplace + telemetry.
- **reworkd/AgentGPT:** https://github.com/reworkd/AgentGPT — browser-first autonomous agent (archived).
- **agno-agi/agno:** https://github.com/agno-agi/agno — runtime + control-plane positioning.
- **xybruceliu/thoughtful-agents:** https://github.com/xybruceliu/thoughtful-agents — System 1 / System 2 proactive cognition (CHI 2025).
- **holmeswww/AgentKit:** https://github.com/holmeswww/agentkit — graph-of-thought via LEGO-style nodes (NAACL 2024).
- **Bessouat40/TreeThinkerAgent:** https://github.com/Bessouat40/TreeThinkerAgent — tree-of-thought exposure layer.
- **yoheinakajima/babyagi:** https://github.com/yoheinakajima/babyagi — minimal plan/execute/reprioritize loop.
