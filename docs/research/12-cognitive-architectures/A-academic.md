# Cognitive Architectures — Academic & Scholarly

**Research value: high** — Dense, well-organized academic literature: a canonical LLM-era framework (CoALA) already unifies the field, classical architectures (Soar, ACT-R, CLARION, Sigma, OpenCog, LIDA) are mature and documented, and 2024–2026 work on hybrid LLM+symbolic systems and dual-process LLMs is converging on structures highly relevant to "humanizing" AI thinking (separating fast generation from deliberate reasoning, episodic/semantic/procedural memory, metacognition).

## Executive Summary

Academic work on cognitive architectures for AI now splits into four layers. (1) **Classical symbolic architectures** — Soar, ACT-R, CLARION, Sigma, OpenCog, LIDA — provide >40 years of scaffolding for memory typologies (working / declarative / procedural / episodic), decision cycles, metacognition, and skill chunking; Laird–Lebiere–Rosenbloom (2017) distilled this into a *Standard Model of the Mind* (a.k.a. Common Model of Cognition, CMC). (2) **CoALA** (Sumers, Yao, Narasimhan, Griffiths, TMLR 2024) is the de facto bridge, reinterpreting LLM agents through cognitive-science primitives: working memory + long-term (episodic, semantic, procedural), internal vs. external actions, and a planning-execution cycle. (3) **Language-agent instantiations** — ReAct, Reflexion, Voyager, Tree-of-Thoughts, Generative Agents, MemGPT — each implements a different subset of CoALA's slots (episodic memory buffers, procedural skill libraries, deliberative System-2 search). (4) **LLM↔cognitive-architecture hybrids** — LLM-ACTR, NL2GenSym (Soar+LLM), CogRec, Structured Cognitive Loop, CLARION-inspired neurosymbolic stacks — inject LLMs into symbolic loops or vice versa, explicitly targeting hallucination, interpretability, and human-likeness. In parallel, *LLMs-as-cognitive-models* (Binz & Schulz, ICLR 2024; Nature Rev. Psych. 2025) finetune LLMs on human behavioral data to predict individual human choice, and a growing **dual-process** literature (Dualformer, ACPO, Reasoning-on-a-Spectrum) argues that single-mode LLMs "overthink" and need adaptive System-1/System-2 switching.

The single most important cross-cutting insight for a humanization project: **human-like AI behavior emerges from *architectural* choices — distinct memory stores, reflection passes, skill accumulation, and System 1/System 2 arbitration — not from prompting alone.** Monolithic LLMs lack exactly the structures that classical cognitive science spent decades validating.

## Sources

### Foundational Frameworks

- **Sumers, Yao, Narasimhan, Griffiths — "Cognitive Architectures for Language Agents" (CoALA)** — arXiv:2309.02427 (Sep 2023, rev. Mar 2024); TMLR Feb 2024; OpenReview `1i6ZCvflQJ`. Princeton. *The canonical organizing framework*. Proposes: (a) modular memory — working + long-term **episodic / semantic / procedural**; (b) action space split into **internal** (reasoning, retrieval, learning) and **external** (grounding via tools/APIs/robots); (c) a generalized **planning → execution** decision cycle. Used to retrospectively classify 300+ language-agent papers (companion repo `ysymyth/awesome-language-agents`). This paper is the single most cited bridge between symbolic-AI history and current LLM agent practice.

- **Laird, Lebiere, Rosenbloom — "A Standard Model of the Mind"** — AI Magazine 38(4), Winter 2017, DOI `10.1609/aimag.v38i4.2744`. A consensus distillation across Soar/ACT-R/Sigma: long-term declarative + procedural memory, a working-memory control interface, and a ~50 ms cognitive cycle — proposed as physics-style shared reference for AI, cognitive science, neuroscience, robotics. Later rebranded *Common Model of Cognition* (CMC).

- **Laird — "An Analysis and Comparison of ACT-R and Soar"** — arXiv:2201.09305 (2022). Fine-grained comparison of memory structures, metadata handling, and decision mechanisms across the two dominant classical architectures. Notes ACT-R optimizes for *cognitive modeling of humans*, Soar for *general AI agents*; secondary goals converge. Essential background for anyone claiming "human-like" AI.

- **Lieto et al. — "Integrating LLMs with Cognitive Architectures" (AAAI Spring Symposium 2023, arXiv:2308.09830)**. Lays out three integration paradigms: **Modular** (CoT + CMC/simulation theory), **Agency** (Society-of-Mind / LIDA-style multi-agent), **Neuro-Symbolic** (CLARION-inspired — bottom-up extraction of symbols from LLMs + top-down symbolic-guided prompting). Useful taxonomy for choosing a humanization architecture.

### Classical Cognitive Architectures

- **Soar (Laird, Newell, Rosenbloom)** — Problem-Space Hypothesis; production rules + chunking; working, procedural, semantic, episodic memories; real-time decision cycle. Canonical survey: Laird, *The Soar Cognitive Architecture* (MIT Press, 2012). Wikipedia `Soar_(cognitive_architecture)` for concise overview.

- **ACT-R (Anderson, Lebiere)** — Buffer-based modular architecture tuned to fit human reaction-time and error data; declarative + procedural; subsymbolic activation equations. See ACT-R tutorials and Anderson, *How Can the Human Mind Occur in the Physical Universe?* (Oxford, 2007).

- **CLARION (Sun)** — Connectionist Learning with Adaptive Rule Induction On-line. *Dual representational structure*: top-level explicit/localist chunks + bottom-level implicit/distributed microfeatures, with top-down/bottom-up flow across four subsystems (action-centered, non-action-centered, motivational, meta-cognitive). Most psychologically faithful implementation of implicit/explicit cognition. Sun, *Anatomy of the Mind* (Oxford, 2016).

- **Sigma (Rosenbloom)** — Graphical-models-based unification: factor graphs + summary-product inference for a hybrid (discrete+continuous) and mixed (symbolic+probabilistic) system, targeting 50 ms/cycle biological real-time. Rosenbloom, Demski, Ustun, *The Sigma Cognitive Architecture and System*, J. AGI (2016); recent extension to neural nets in Springer *Artificial General Intelligence 2016*.

- **OpenCog / OpenCog Prime (Goertzel)** — AtomSpace hypergraph knowledge store + MindAgents + Cognitive Synergy Theory. Explicit AGI ambition; divides cognition into declarative/procedural/sensory/episodic/attentional/intentional units with designed synergies. See `opencog.org` and Goertzel, *Engineering General Intelligence* (Atlantis, 2014).

- **LIDA (Franklin)** — Implements Global Workspace Theory with ~10 Hz cognitive cycles, codelets, sparse distributed memory, and an explicit consciousness phase between understanding and action selection. Primary reference: Franklin et al., "LIDA: A Computational Model of Global Workspace Theory," AAAI FSS 2007; Baars & Franklin, *Global Workspace Theory, its LIDA Model and the Underlying Neuroscience* (2009).

### LLM + Classical Cognitive-Architecture Hybrids

- **Wu et al. — LLM-ACTR** — neurosymbolic framework that extracts ACT-R decision traces as latent representations and injects them into LLM adapter layers for Design-for-Manufacturing tasks; claims improved grounding and reduced hallucination vs. LLM-only. Neurosymbolic AI Journal (2024/25), `nai-paper-791.pdf`.

- **Language-model embeddings inside ACT-R** — Frontiers in Language Sciences (2026, DOI `10.3389/flang.2026.1721326`). Replaces ACT-R's hand-coded spreading-activation similarities with cosine similarities from Word2Vec/BERT embeddings; scales memory-retrieval models without breaking interpretability.

- **NL2GenSym (arXiv:2510.09355, 2025)** — Uses an LLM Generator–Critic loop to synthesize Soar production rules from natural language, executed and refined inside Soar; >86% rule-generation success; solves tasks at 1.98× optimal cycles. Addresses Soar's biggest practical bottleneck (manual rule authoring).

- **CogRec (arXiv:2512.24113, 2025)** — Cognitive recommender fusing Soar's Perception–Cognition–Action cycle with LLM-sourced knowledge; on impasse, LLM proposes a solution that Soar *chunks* into a new production rule — online symbolic learning driven by language.

- **Structured Cognitive Loop / Soft Symbolic Control (arXiv:2511.17673, 2025)** — 5-phase R-CCAM loop (Retrieval, Cognition, Control, Action, Memory) wrapping LLM calls in a symbolic governance layer; reports zero policy violations vs. ReAct/AutoGPT baselines.

### Language Agents (CoALA instantiations)

- **Yao et al. — ReAct** — arXiv:2210.03629; ICLR 2023. Interleaves reasoning traces and tool actions. On ALFWorld/WebShop: +34% / +10% absolute success over imitation/RL baselines. The prototype of CoALA's internal+external action split.

- **Shinn et al. — Reflexion: Language Agents with Verbal Reinforcement Learning** — arXiv:2303.11366; NeurIPS 2023. Agents verbally reflect on failures and store reflections in an **episodic memory buffer**; 91% pass@1 on HumanEval (vs. GPT-4's 80%). Direct LLM-era implementation of metacognition + episodic learning.

- **Yao et al. — Tree of Thoughts (ToT)** — arXiv:2305.10601; NeurIPS 2023. Deliberate search over "thoughts" with self-evaluation + backtracking. Game-of-24: 4% (CoT) → 74% (ToT). Explicitly framed as **System-1 → System-2** augmentation.

- **Wang et al. — Voyager: Open-Ended Embodied Agent with LLMs** — TMLR 2024; `voyager.minedojo.org`. Automatic curriculum + ever-growing **skill library** (executable code indexed by embeddings) + iterative self-verification. 3.3× items, 15.3× faster tech-tree than prior in Minecraft. Canonical example of CoALA's **procedural memory**.

- **Park et al. — Generative Agents: Interactive Simulacra of Human Behavior** — UIST '23; arXiv:2304.03442. 25 agents in "Smallville" with memory stream + **reflection** (higher-level summaries) + planning; emergent Valentine's Day party. First high-profile demonstration that memory + reflection + planning modules produce believable human-like behavior on top of GPT-3.5.

- **Park et al. — Generative Agent Simulations of 1,000 People** — arXiv:2411.10109 (Nov 2024). 1,052 agents grounded in 2,000 hrs of qualitative interviews; replicate GSS responses at 85% of test–retest reliability; reduce demographic-stereotype bias vs. persona-only prompts. Empirical evidence that *rich episodic grounding* beats *persona prompts* for human-likeness.

- **Packer et al. — MemGPT: Towards LLMs as Operating Systems** — arXiv:2310.08560 (2023). OS-style hierarchical memory (fast context + paged external store) with function-calling-based self-management. Operationalizes CoALA's long-term memory at systems level.

### LLMs as Cognitive Models

- **Binz & Schulz — "Turning Large Language Models into Cognitive Models"** — arXiv:2306.03917; ICLR 2024. Finetunes LLaMA on psychological-experiment data (CENTaUR); beats classical cognitive models on two decision-making domains and generalizes across tasks/individuals. Foundational for *LLMs-as-models-of-human-cognition* (distinct from *cognitive-architectures-for-LLMs*).

- **Nature Reviews Psychology — "Dual-Process Theory and Decision-Making in Large Language Models"** (2025, DOI `10.1038/s44159-025-00506-1`). Review arguing LLMs exhibit both System-1 heuristic and System-2 deliberate behavior, but with *non-human* biases (hallucinations) rooted in training-data patterns rather than cognitive mechanisms.

### Dual-Process / System 1 ↔ System 2 for LLMs

- **Dualformer** — arXiv:2410.09918 (Oct 2024). Single Transformer trained on *randomized* reasoning traces; runs in fast / slow / auto modes. 97.6% optimality on mazes using 45.5% fewer reasoning steps than CoT baseline.

- **Adaptive Cognition Policy Optimization (ACPO) — "Incentivizing Dual Process Thinking"** — arXiv:2505.16315 (May 2025). RL framework that makes a model choose System-1 vs. System-2 based on estimated task difficulty; directly addresses "overthinking."

- **Reasoning on a Spectrum** — NeurIPS 2025 submission (OpenReview `DQuWpKLNwd`). Curates a dataset with valid System-1 and System-2 responses; shows a monotonic accuracy–efficiency trade-off and that interpolation outperforms either extreme.

### Surveys & Recent Framing (2024–2026)

- **Zhang et al. — "A Survey on the Memory Mechanism of LLM-Based Agents"** — arXiv:2404.13501 (2024). Taxonomy of parametric vs. contextual, structured vs. unstructured memory, and six operations (consolidation, updating, indexing, forgetting, retrieval, condensation). Useful mapping to CoALA memory slots.

- **"Agentic AI: Architectures, Taxonomies, Evaluation of LLM Agents"** — arXiv:2601.12560 (2026). Unified six-component taxonomy (Perception, Brain, Planning, Action, Tool Use, Collaboration); traces the shift from fixed APIs to MCP / Native Computer Use.

- **The Auton Agentic AI Framework** — arXiv:2602.23720 (2026). Separates declarative *Cognitive Blueprint* from execution *Runtime Engine*; formalizes agent execution as an augmented POMDP with latent reasoning space and biologically-inspired hierarchical episodic consolidation.

## Patterns, Trends, Gaps

1. **Convergence on a shared memory typology.** Working, episodic, semantic, procedural — independently named by ACT-R (1990s), Soar (extended ~2008), CoALA (2023), MemGPT (2023), and the 2024 memory survey. Any serious "humanizing" system should expose these four stores explicitly, not collapse them into a single context window.

2. **Metacognition and reflection are load-bearing.** CLARION's metacognitive subsystem, LIDA's consciousness phase, Reflexion's verbal RL, and Generative Agents' reflection tree all report step-change gains. Human-likeness correlates with *an agent that re-reads and re-summarizes its own traces*.

3. **Dual-process framing has become the default.** From Tree of Thoughts (explicit System-1 → System-2 augmentation) through Dualformer and ACPO, the field is converging on **adaptive** System-1/2 switching rather than always-on CoT. Over-reasoning is now a named failure mode.

4. **Hybrid neurosymbolic stacks have moved from theory to benchmarks.** 2025 saw concrete speedups and safety gains from LLM-ACTR, NL2GenSym, CogRec, and SCL. The symbolic layer is no longer optional when interpretability or policy compliance matters.

5. **Grounding in human data beats persona prompting.** Park et al.'s 1,000-people paper directly shows that interview-grounded episodic memory outperforms demographic persona prompts — and reduces racial/ideological bias. Strong implication for humanization: supply *data*, not *adjectives*.

6. **Gaps.** (a) No standard benchmark for "human-likeness" at the cognitive-architecture level — papers use believability Turing tests, survey replication, or task accuracy, incomparably. (b) Classical architectures (Sigma, OpenCog, LIDA) remain almost untouched by the LLM-agent wave; most LLM+classical work focuses on Soar and ACT-R. (c) The **motivational / affective** subsystems of CLARION and LIDA have no mainstream LLM analog — emotional modeling remains fragmented and mostly prompt-level, not architectural. (d) **Forgetting** is theorized (Zhang 2024 survey) but rarely implemented beyond ad-hoc context truncation.

## Relevance to the Humanization Project

Treat humanization as an *architectural* problem: layer explicit episodic + semantic + procedural stores over the LLM; add a reflection/metacognition pass (Reflexion-style); arbitrate System-1/System-2 adaptively (Dualformer/ACPO); ground persona in real human interview data (Park 2024) rather than persona adjectives; and consider a symbolic governance layer (SCL, CLARION-inspired) for the traits — style invariance, consistent opinions, controlled hedging — that pure prompting cannot stabilize. CoALA is the right top-level scaffold to organize such a stack.
