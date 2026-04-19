# Cognitive Architectures — Open-Source & GitHub

**Research value: high** — Two coexisting generations of open-source cognitive architectures are directly relevant to "humanizing" AI: (a) the classical symbolic arches (Soar, ACT-R, OpenCog Hyperon) that encode decades of psychology-grounded models of memory, attention, and rationality, and (b) a fast-moving LLM-era cluster (Generative Agents, Voyager, MemGPT/Letta, MetaGPT, CAMEL, ChatDev, Agent-S, AutoGen, BabyAGI, AutoGPT) that operationalizes CoALA-style working/episodic/semantic/procedural memory on top of language models. The LLM cluster is where most "sounds like a person" behavior gets produced today, but the classical arches are the source of the vocabulary (memory types, decision cycles, chunking, production rules) the LLM repos now use.

## Executive Summary

The field splits into five layers. (1) **Classical symbolic arches** — `SoarGroup/Soar` (416★, BSD, U-Michigan, Laird's *The Soar Cognitive Architecture* is the canonical reference) and `jakdot/pyactr` (179★, GPL-3) / `CarletonCognitiveModelingLab/python_actr` (37★, MIT) / official Common-Lisp ACT-R from CMU — provide production-rule / working-memory / declarative-memory machinery with quantitative latency predictions. (2) **Hybrid/neurosymbolic AGI arches** — `trueagi-io/hyperon-experimental` (250★, MeTTa "Atomese 2" in Rust/Python) and `opencog/atomspace` (962★, hypergraph DB) chase human-like reasoning via metagraph rewriting. (3) **Simulacra / believable-agent systems** — `joonspk-research/generative_agents` (21.1K★, Stanford Smallville) introduced the memory-stream + reflection + planning triple that is now the de facto template for "believable human behavior"; the `StanfordHCI/genagents` follow-up simulates 1,000 real people from interview data. (4) **Long-horizon, stateful-memory agents** — `letta-ai/letta` (22.2K★, formerly MemGPT), `MineDojo/Voyager` (6.8K★, lifelong-learning skill library), and `simular-ai/Agent-S` (10.8K★, first to beat humans on OSWorld at 72.6%). (5) **Role/SOP-based multi-agent societies** — `Significant-Gravitas/AutoGPT` (183.5K★), `yoheinakajima/babyagi` (22.2K★, archived but foundational), `FoundationAgents/MetaGPT` (66.7K★), `OpenBMB/ChatDev` (32.5K★, now ChatDev 2.0 zero-code platform), `camel-ai/camel` (16.6K★), `microsoft/autogen` (57.2K★, maintenance mode, merging into Microsoft Agent Framework). (6) **Theory scaffolding** — `ysymyth/awesome-language-agents` (1.2K★) curates the CoALA bibliography (300+ citations) and is the closest thing the LLM-agent field has to a shared cognitive vocabulary.

The strongest shared insight across repos: human-feeling output comes not from prompt style but from architecture — a working/long-term memory split, an explicit reflection step that condenses experience into higher-order generalizations, a skill/procedure store that grows over time, and a decision-making cycle separating deliberation from action. Voice tricks without these structures revert to formulaic output within a few turns.

## Sources

### Classical Symbolic Architectures

- **SoarGroup/Soar** — `github.com/SoarGroup/Soar` — ~416★ — BSD License — stable 9.6.4, workshop #45 held May 2025. General cognitive architecture from the Newell/Laird lineage; C/C++ core with Python, Java, JavaScript SWIG bindings. Encodes production rules, working memory, chunking, subgoaling, episodic memory, and reinforcement-learning modules. Companion `SoarGroup/Engineers-Guide-to-Soar` (14-part course) and `THA-Embedded-Systems-Lab/soar_ros` (ROS2 integration, 2025) extend it into robotics. *The longest-running open cognitive architecture, 40+ years of theory.*

- **jakdot/pyactr** — `github.com/jakdot/pyactr` — ~179★ — GPL-3 — v0.3.2 (Feb 2024). Python implementation of ACT-R with both symbolic and subsymbolic processes; supports features "not often implemented outside the official Lisp ACT-R software." Requires numpy, simpy, pyparsing. Paired with the Springer open-access book *Computational Cognitive Modeling and Linguistic Theory*.

- **CarletonCognitiveModelingLab/python_actr** — `github.com/CarletonCognitiveModelingLab/python_actr` — ~37★ — MIT. Python port from Carleton's cognitive modeling lab. Caveat: "Does not run on Python 3.12 or higher." Fork `asmaloney/python_actr` (pip: `actr`) is more actively maintained.

- **Official ACT-R (Common Lisp)** — `act-r.psy.cmu.edu` — Anderson & Lebiere, CMU. Current version ACT-R 7. Remains the reference for declarative/procedural memory, buffer architecture, and latency/accuracy predictions. Influential on nearly all CoALA memory-type distinctions.

### Neurosymbolic / AGI-Oriented Architectures

- **trueagi-io/hyperon-experimental** — `github.com/trueagi-io/hyperon-experimental` — ~250★ — pre-alpha. Rust (75.7%) + Python (15.3%) implementation of **MeTTa** (Meta Type Talk, "Atomese 2"), successor to OpenCog Classic's Atomese. Installable via `pip install hyperon` or `docker run trueagi/hyperon:latest`. Grounded in metagraph rewriting and "cognitive algorithms as Galois connections" (Goertzel et al.).

- **opencog/atomspace** — `github.com/opencog/atomspace` — ~962★. In-RAM hypergraph/metagraph knowledge database with query engine and graph-rewriting, the central representation layer of OpenCog Classic. Mature with dozens of modules (storage, network shell, embeddings, sensorimotor, language learning).

### Simulacra and Believable Agents

- **joonspk-research/generative_agents** — `github.com/joonspk-research/generative_agents` — ~21,149★ — UIST '23. Park et al.'s Smallville sandbox with 25 agents running GPT-3.5-turbo + a Phaser/Django frontend. Three-part architecture: **memory stream** (natural-language observations with recency/importance/relevance scoring), **reflection** (periodic synthesis of memories into higher-level inferences), **planning** (recursively decomposed schedules). *The canonical reference implementation for humanlike agent behavior.*

- **StanfordHCI/genagents** — `github.com/StanfordHCI/genagents` — 2024 follow-up. 3,000+ agents built from 2,000 hours of qualitative interviews with real people, replicating their General Social Survey responses. Tiered API (aggregated open, individual restricted).

### Long-Horizon Memory and Lifelong Learning

- **letta-ai/letta** (formerly MemGPT) — `github.com/letta-ai/letta` — ~22,157★ — Apache 2.0 — v0.16.7. "The platform for building stateful agents: AI with advanced memory that can learn and self-improve over time." Originated as UC Berkeley's MemGPT (OS-inspired virtual-context paging for LLMs). Ships **memory blocks** (structured editable context), Python/TypeScript SDKs, CLI (`npm i -g @letta-ai/letta-code`), skills and subagents. Model-agnostic; recommends Claude Opus 4.5 / GPT-5.2.

- **MineDojo/Voyager** — `github.com/MineDojo/Voyager` — ~6,834★ — MIT — NVIDIA/Caltech/UT Austin/Stanford/ASU. Three components: "(1) an automatic curriculum that maximizes exploration, (2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and (3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification." 3.3× more unique Minecraft items, 15.3× faster tech-tree milestones vs prior SOTA. Skills are "temporally extended, interpretable, and compositional."

- **simular-ai/Agent-S** — `github.com/simular-ai/Agent-S` — ~10,790★ — Apache 2.0 — v0.3.2. GUI agent framework; **Agent S3 (Oct 2025) is the first system to surpass human performance on OSWorld at 72.60%**. ICLR 2025 Best Paper Award (Agentic AI for Science Workshop). Cross-platform Linux/macOS/Windows, pluggable grounding models (UI-TARS-1.5-7B), explicit reflection agent.

### Multi-Agent Role Societies & SOPs

- **Significant-Gravitas/AutoGPT** — `github.com/Significant-Gravitas/AutoGPT` — ~183,558★ — last updated Apr 18 2026. "The vision of accessible AI for everyone." Self-hosted + cloud beta; 100 releases; 430 contributors. Pioneered the autonomous-loop pattern (plan → critique → execute → update memory) that most later frameworks refined.

- **yoheinakajima/babyagi** — `github.com/yoheinakajima/babyagi` — ~22,215★ — MIT — original archived Sep 2024 as `babyagi_archive`; current repo is an experimental "functionz" framework for a self-building autonomous agent. "The optimal way to build a general autonomous agent is to build the simplest thing that can build itself." Graph-based function store with dependency tracking, logging, dashboard.

- **FoundationAgents/MetaGPT** — `github.com/FoundationAgents/MetaGPT` — ~66.7K★. "Assign different roles to GPTs to form a collaborative entity for complex tasks." Software company as multi-agent system: product managers, architects, project managers, engineers. Core slogan: `Code = SOP(Team)`. AFlow paper accepted to ICLR 2025 oral (top 1.8%). Productized as `mgx.dev` ("the world's first AI agent development team," #1 Product Hunt Feb 2025).

- **OpenBMB/ChatDev** — `github.com/OpenBMB/ChatDev` — ~32,554★ — Apache 2.0 — v2.2.0. "ChatDev has evolved from a specialized software development multi-agent system into a comprehensive multi-agent orchestration platform." ChatDev 2.0 "DevAll" released Jan 7 2026 as zero-code multi-agent platform; ChatDev 1.0 (CEO/CTO/Programmer roles) moved to `chatdev1.0` branch. Companion research: MacNet (DAG topologies scaling to 1000+ agents), Puppeteer RL orchestration (NeurIPS 2025), Iterative Experience Refinement, Experiential Co-Learning.

- **camel-ai/camel** — `github.com/camel-ai/camel` — ~16,653★. "Open-source, modular framework for building intelligent multi-agent systems" with primitives for Agents, Societies, Interpreters, Memory & Storage, plus OASIS (social simulation) and CRAB benchmark. One of the earliest role-playing agent-society frameworks (NeurIPS 2023).

- **microsoft/autogen** — `github.com/microsoft/autogen` — ~57,201★ — CC-BY-4.0 — now in maintenance mode. "A programming framework for agentic AI" — pioneered multi-agent conversation (v0.4+ async messaging, distributed agent networks, Python+.NET). October 2025: merging with Semantic Kernel into **Microsoft Agent Framework**.

### Theory & CoALA Scaffolding

- **ysymyth/awesome-language-agents** — `github.com/ysymyth/awesome-language-agents` — ~1,198★ — MIT. Official companion to Sumers, Yao, Narasimhan, Griffiths, *Cognitive Architectures for Language Agents* (arXiv:2309.02427). CoALA defines the action space as external (**grounding**) vs internal (**reasoning**, **retrieval**, **learning**) and posits working memory + optional long-term memories (**episodic**, **semantic**, **procedural**). 300+ citations in `CoALA.bib`, papers tagged by action-space type.

- **IBM/SPIRAL** — `github.com/IBM/SPIRAL` — AAAI 2026. Tri-agent cognitive architecture embedded in an MCTS loop for grounded, reflective planning with LLMs. WatsonX + Hugging Face implementations.

- **ReCAP-Stanford/ReCAP** — `github.com/ReCAP-Stanford/ReCAP` — NeurIPS 2025. Recursive Context-Aware Reasoning and Planning: plan-ahead task decomposition, structured context re-injection, sliding-window scalability; beats sequential/hierarchical baselines on Robotouille, ALFWorld, FEVER, SWE-bench.

- **bdambrosio/Cognitive_workbench** — Research framework with incremental planning, FAISS semantic-memory search, reflective QC, 24 built-in tools, OODA-loop (Observe-Orient-Decide-Act) structure.

## Key Techniques / Patterns

1. **CoALA memory-type taxonomy.** Working memory + episodic (experience) + semantic (knowledge) + procedural (skills/code). Letta, Voyager, Generative Agents, MetaGPT, and CAMEL all map onto this four-way split; divergence is in *which* long-term store they emphasize. Humanization-relevant: episodic memory produces "I remember when…" coherence; procedural memory produces competence that compounds instead of drifting.

2. **Memory stream + reflection.** The Park et al. pattern: append raw natural-language observations to a stream, score each by recency × importance × relevance at retrieval, and periodically "reflect" (LLM-summarize) into higher-level beliefs. Reflection is what prevents agents from sounding like lookup tables.

3. **Virtual-context / OS-paging metaphor (MemGPT).** Treat limited context window as RAM and durable memory as disk, with the LLM explicitly issuing read/write calls to its own memory blocks. Directly addresses the "flat, contextless" feel of vanilla chat.

4. **Lifelong skill libraries (Voyager).** Successful behaviors are stored as executable code with natural-language descriptions, indexed for retrieval. Each new task re-uses prior skills; failure triggers iterative self-verification and program repair. Produces compounding competence — a key humanlike property.

5. **SOP / role-based multi-agent societies.** MetaGPT's `Code = SOP(Team)`, ChatDev's CEO/CTO/Programmer seminars, CAMEL's role-playing pairs, AutoGen's conversable agents. Persona-driven role splitting yields diverse voices, structured disagreement, and specialization — behaviorally more humanlike than a single chain-of-thought.

6. **Reflection / self-critique (Reflexion, Agent-S, SPIRAL).** Actor–Evaluator–Reflector triples that turn failure into stored "lessons." Carnival9's ActiveMemory and ChatDev's Iterative Experience Refinement push this further: extract small, prunable lessons rather than raw transcripts.

7. **Classical production-rule cognition as ground truth.** Soar and ACT-R encode decades of human-subject data on latency, forgetting, interference, chunking. LLM-era repos increasingly borrow the vocabulary (working memory, declarative/procedural split, decision cycles) but rarely the underlying dynamics — a genuine grounding gap.

8. **Metagraph / neurosymbolic substrate (Hyperon, AtomSpace).** A first-class relational/hypergraph representation under the LLM layer, motivated by "Atomese"-style uniform knowledge representation. Still pre-alpha but the most serious open attempt at combining logic, probability, and neural methods for humanlike general reasoning.

9. **Self-building / self-modifying systems (BabyAGI "functionz", AutoGPT, Letta self-improve).** Agents that add to their own function/skill library autonomously. Aligns with a humanlike property — learning as a side-effect of problem-solving rather than explicit training.

10. **Interview-grounded agents (StanfordHCI/genagents).** Rather than inventing personas, derive them from transcribed interviews with real people. Empirically closer to "what a specific human would say" than any prompt template.

## Notable Quotes

- From `ysymyth/awesome-language-agents` README, paraphrasing the CoALA paper: *"A language agent has a short-term working memory and several (optional) long-term memories (episodic for experience, semantic for knowledge, procedural for code/LLM). Reasoning = update working memory (with LLM); Retrieval = read long-term memory; Learning = write long-term memory."* — attribution: Sumers, Yao, Narasimhan, Griffiths (2023), curated by Shunyu Yao.

- From `MineDojo/Voyager` README: *"Voyager consists of three key components: 1) an automatic curriculum that maximizes exploration, 2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and 3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification. … The skills developed by Voyager are temporally extended, interpretable, and compositional, which compounds the agent's abilities rapidly and alleviates catastrophic forgetting."* — attribution: Wang et al. (arXiv 2305.16291), NVIDIA.

- From `letta-ai/letta` README: *"Letta (formerly MemGPT). Build AI with advanced memory that can learn and self-improve over time. … Letta Code supports skills and subagents, and bundles pre-built skills/subagents for advanced memory and continual learning."* — attribution: Letta AI team (originally UC Berkeley MemGPT authors Packer et al.).

- From `FoundationAgents/MetaGPT` README: *"Assign different roles to GPTs to form a collaborative entity for complex tasks. … Internally, MetaGPT includes product managers / architects / project managers / engineers. It provides the entire process of a software company along with carefully orchestrated SOPs. `Code = SOP(Team)` is the core philosophy. We materialize SOP and apply it to teams composed of LLMs."* — attribution: Hong, Zhuge, Chen et al. (ICLR 2024), DeepWisdom.

- From `OpenBMB/ChatDev` README: *"ChatDev has evolved from a specialized software development multi-agent system into a comprehensive multi-agent orchestration platform. … ChatDev 1.0 (Legacy) operates as a Virtual Software Company. It utilizes various intelligent agents (e.g., CEO, CTO, Programmer) participating in specialized functional seminars to automate the entire software development life cycle."* — attribution: Qian et al., Tsinghua / OpenBMB.

- From `yoheinakajima/babyagi` README: *"The optimal way to build a general autonomous agent is to build the simplest thing that can build itself."* — attribution: Yohei Nakajima.

- From `trueagi-io/hyperon-experimental` README: *"OpenCog Hyperon is a substantially revised, novel version of OpenCog — which is currently at an active pre-alpha stage of development and experimentation. … What we have landed on is an 'Atomese 2' language called MeTTa (Meta Type Talk)."* — attribution: TrueAGI / OpenCog Foundation, Goertzel et al.

- From `Significant-Gravitas/AutoGPT` repository tagline: *"AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters."* — attribution: Toran Bruce Richards / Significant Gravitas.

- From `simular-ai/Agent-S` README: *"Agent S3: First to Surpass Human Performance on OSWorld (72.60%). … Welcome to Agent S, an open-source framework designed to enable autonomous interaction with computers through Agent-Computer Interface. Our mission is to build intelligent GUI agents that can learn from past experiences and perform complex tasks autonomously on your computer."* — attribution: Agashe, Gonzalez-Pumariega et al., Simular AI.

## Emerging Trends

- **Convergence on CoALA vocabulary.** Papers and READMEs from 2024–2026 (Letta, MetaGPT, ChatDev, Agent-S, SPIRAL, ReCAP) increasingly adopt working/episodic/semantic/procedural memory language and grounding/reasoning/retrieval/learning action taxonomy. CoALA is becoming the shared interface spec the field lacked.

- **From chat frameworks to stateful-agent platforms.** Letta's rebrand (MemGPT → Letta) and ChatDev 2.0's pivot to a "zero-code multi-agent platform" mark a shift from single-session prompt engineering to persistent, multi-user, multi-agent infrastructure.

- **Consolidation in multi-agent frameworks.** AutoGen is merging into Microsoft Agent Framework; BabyAGI is archived; AutoGPT is still dominant by stars but development has slowed relative to MetaGPT / Letta / Agent-S. The 2023 Cambrian explosion is compressing into a few production-grade platforms.

- **Learned orchestration over hand-written SOPs.** ChatDev's Puppeteer paper (NeurIPS 2025) and MetaGPT's AFlow (ICLR 2025 oral) replace fixed workflows with RL-optimized central orchestrators — agents that *learn* when and how to activate sub-agents.

- **Grounded computer-use agents surpass humans.** Agent-S3 on OSWorld (72.60%) and related work on WindowsAgentArena / AndroidWorld show that cognitive-architecture-plus-LLM hybrids are now crossing human baselines on realistic tasks. The humanization question is shifting from "can it talk like a person" to "can it act like a person over long horizons."

- **Neurosymbolic revival through Hyperon.** MeTTa + AtomSpace are positioned as the general substrate under which LLMs, logic, and probabilistic reasoning can cohabit — the most active non-LLM AGI architecture in open source.

- **Interview-grounded simulacra.** StanfordHCI/genagents (1,000 real people, 2,000 interview hours) signals a move away from fictional "Isabella in Smallville" toward agents anchored in actual human data.

## Open Questions / Gaps

1. **Classical–LLM bridge is thin.** Almost no open-source project seriously runs Soar or ACT-R in the loop with an LLM. The 2023 paper *Synergistic Integration of Large Language Models and Cognitive Architectures* (in CoALA.bib) proposed this, but no popular repo implements it. The dynamics (forgetting curves, activation spread, chunking latencies) of classical arches are not being used to constrain LLM output.

2. **No shared humanization benchmark across architectures.** Generative Agents reports internal evaluations; Voyager reports Minecraft metrics; Agent-S reports OSWorld. No cross-architecture benchmark measures "how human does this agent feel" (believability, memory consistency, personality stability over long horizons).

3. **Reflection is the least rigorous stage.** Every repo has one, but quality varies wildly and is rarely evaluated. How much reflection? How often? What does reflection drift look like after 10,000 turns?

4. **Memory drift and contradiction handling.** Letta, Generative Agents, MemGPT all accumulate memory — but handling contradictions, outdated beliefs, and emotional-state consistency is under-specified. Humans forget gracefully; most agents either keep everything or purge arbitrarily.

5. **Procedural memory ≈ skill library, but compositionality is weak.** Voyager's skill library is the most cited example, yet composition between skills is still mostly LLM-prompted rather than formally structured (unlike Soar's chunking).

6. **Persona/identity persistence.** MetaGPT's role personas, Generative Agents' backstories, and Letta's memory blocks all approximate identity, but none provide a stable "this is who I am across every session" invariant the way classical arches' goal/impasse structure does.

7. **Hyperon is theoretically ambitious but pre-alpha.** 250 stars vs 22K for Letta. Neurosymbolic cognition for humanization remains aspirational; no humanizer toolchain uses MeTTa today.

8. **Licensing fragmentation.** MIT (Voyager, Letta, genagents), Apache-2 (Agent-S, ChatDev, MetaGPT), GPL-3 (pyactr), BSD (Soar), CC-BY-4.0 (AutoGen), and custom/research licenses for classical ACT-R. Composing a humanization stack across these is non-trivial.

9. **Evaluation bias toward task completion.** OSWorld/WebArena/SWE-bench measure doing-the-job; there is no equivalent benchmark for "did this agent's reasoning, tone, memory, and personality stay coherent and humanlike over hours of use." A project called *Unslop* could plausibly invent this.

## References

- `github.com/SoarGroup/Soar` — general cognitive architecture, Soar 9.6.4.
- `github.com/jakdot/pyactr` — Python ACT-R with subsymbolic support.
- `github.com/CarletonCognitiveModelingLab/python_actr` — Carleton Python ACT-R.
- `act-r.psy.cmu.edu` — official Common-Lisp ACT-R 7 at CMU.
- `github.com/trueagi-io/hyperon-experimental` — OpenCog Hyperon / MeTTa.
- `github.com/opencog/atomspace` — OpenCog Classic hypergraph DB.
- `github.com/joonspk-research/generative_agents` — Stanford Smallville (UIST '23).
- `github.com/StanfordHCI/genagents` — 1,000-person interview-grounded agents.
- `github.com/MineDojo/Voyager` — lifelong-learning Minecraft agent.
- `github.com/letta-ai/letta` — stateful-agent platform (formerly MemGPT).
- `github.com/simular-ai/Agent-S` — GUI agent, >72% OSWorld.
- `github.com/Significant-Gravitas/AutoGPT` — pioneering autonomous-loop platform.
- `github.com/yoheinakajima/babyagi` — self-building functionz framework.
- `github.com/FoundationAgents/MetaGPT` — SOP-driven software-company multi-agents.
- `github.com/OpenBMB/ChatDev` — DevAll zero-code multi-agent platform.
- `github.com/camel-ai/camel` — role-playing multi-agent framework.
- `github.com/microsoft/autogen` — Microsoft multi-agent conversation framework (maintenance).
- `github.com/ysymyth/awesome-language-agents` — CoALA bibliography and taxonomy.
- `github.com/IBM/SPIRAL` — tri-agent MCTS cognitive architecture (AAAI 2026).
- `github.com/ReCAP-Stanford/ReCAP` — recursive context-aware planning (NeurIPS 2025).
- `github.com/bdambrosio/Cognitive_workbench` — OODA-loop research framework.
- `arxiv.org/abs/2309.02427` — Sumers et al., *Cognitive Architectures for Language Agents* (CoALA).
- `arxiv.org/abs/2304.03442` — Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*.
- `arxiv.org/abs/2305.16291` — Wang et al., *Voyager*.
- `arxiv.org/abs/2310.08560` — Packer et al., *MemGPT*.
- `arxiv.org/abs/2308.00352` — Hong et al., *MetaGPT*.
- `arxiv.org/abs/2307.07924` — Qian et al., *ChatDev / Communicative Agents*.
- `soar.eecs.umich.edu` — Soar homepage and 45th workshop (2025).
