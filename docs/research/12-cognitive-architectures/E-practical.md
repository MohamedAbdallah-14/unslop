# Cognitive Architectures — Angle E: Practical How-Tos & Forums

**Project:** Humanizing AI output and thinking
**Category:** 12 — Cognitive Architectures
**Angle:** E — Practical How-Tos & Forums (Reddit, HN, Twitter/X, LessWrong, YouTube)
**Research date:** 2026-04-21 (updated April 2026; covers April 2025–April 2026)
**Research value: high** — Dense practitioner signal across Reddit, HN, LessWrong, and YouTube on memory, dual-process reasoning, metacognition, and agent loops. Multiple independent sources converge on a small set of architectural patterns directly usable for humanizing AI output and "thinking."

---

## How to read this digest

Each post has the same fields:

- **Source / Platform** — where it lives
- **Title / URL** — direct link
- **Approx. date** — when it was posted (best-effort; forum threads evolve)
- **Author / Community** — who's speaking
- **Summary** — what the post actually says
- **Pattern / Mechanism** — the reusable idea
- **Relevance to humanizing AI** — why it matters for this project

Posts are grouped by theme (memory, dual-process, metacognition, agent loops, humanization-of-output). Trends and gaps follow at the end.

---

## 1. Memory architectures — the practitioner baseline

### Post 1 — "Finally got my local agent to remember stuff between sessions"

- **Source:** Reddit — r/LocalLLaMA
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1r25chl/finally_got_my_local_agent_to_remember_stuff/
- **Date:** 2025 (late)
- **Community:** Local-LLM hobbyists / solo builders
- **Summary:** OP implements a three-tier memory system (short-term, working, long-term with selective consolidation) inspired by human cognition. Adds ~50 ms latency but removes the 10k+ token re-priming problem per session.
- **Pattern:** Hierarchical, human-inspired memory tiers with consolidation rules ("what's worth remembering vs. what should fade").
- **Relevance:** For "thinking-like" output, the model needs to reference prior context the way humans do — not by dumping raw history but via consolidated, summarized episodes. This is the base layer for voice consistency across sessions.

### Post 2 — "We gave our RAG chatbot memory across sessions — here's what broke first"

- **Source:** Reddit — r/LocalLLaMA
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1rqujc1/we_gave_our_rag_chatbot_memory_across_sessions/
- **Date:** 2025 Q4
- **Community:** Production RAG builders
- **Summary:** Team moved to an agentic-memory model with three tools (`search_docs`, `search_memory`, `add_memory`). Failure modes: tool loops (models call search repeatedly with tiny variations), user-ID confusion, and the model storing garbage without explicit "what's worth keeping" prompting.
- **Pattern:** Agentic/tool-driven memory beats passive vector stuffing, but requires strict caps (e.g., "max 5 tool calls per turn") and explicit consolidation heuristics.
- **Relevance:** Directly relevant — human-like thinking includes *deciding what to remember.* Passive vector recall produces the uncanny "perfect recall, wrong selection" feel that makes AI output feel non-human.

### Post 3 — "How are you handling persistent memory across local Ollama sessions?"

- **Source:** Reddit — r/LocalLLaMA
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1rokrsm/how_are_you_handling_persistent_memory_across/
- **Date:** 2025 Q4
- **Community:** Local-LLM operators
- **Summary:** Meta-thread surveying Mem0, Letta, Zep, plain SQLite, and custom JSON blobs. Consensus: most production pain is *project scoping* — separating memory per-context — not raw storage.
- **Pattern:** Context partitioning > storage tech. Cross-context bleed is the dominant failure.
- **Relevance:** Humans don't mix "what my friend said last week" with "what my boss said last week." Scoped memory maps to human persona/context switching.
- **2026 update:** By early 2026, practitioner discussion has shifted from "which storage tech" to "vector or graph?" — the question of whether to store facts with embeddings only or as graph edges with relational/temporal connections. Consensus forming around graph memory for long-horizon agents, vector memory for fast lookup. Mem0 and Zep now both ship graph memory as production features.

### Post 4 — "A three-layer memory architecture for long-running agents"

- **Source:** Hacker News
- **URL:** https://news.ycombinator.com/item?id=46097759
- **Date:** 2025
- **Community:** HN front page, engineer commentary
- **Summary:** Separates **semantic memory** (what are we building), **structured task storage** (Jira-for-AI), and **git-style versioning** for long-running agents. Argues that mixing these creates cognitive load.
- **Pattern:** Separation of concerns across memory axes — identity/understanding vs. action tracking vs. history/versioning.
- **Relevance:** A humanized agent needs a stable "identity/project understanding" layer distinct from episodic task history. Mixing them produces incoherent voice.

### Post 5 — "Show HN: Mnemo — Shareable typed agentic memory with Bayesian belief updating"

- **Source:** Hacker News
- **URL:** https://news.ycombinator.com/item?id=47691109
- **Date:** 2025–2026
- **Community:** HN Show HN
- **Summary:** Uses Tulving's typed memory model (episodic / procedural / semantic). Each memory is broken into *atoms* with Beta-distribution confidence scores, updated via Bayes when new info confirms/contradicts, with contradictions preserved as graph edges.
- **Pattern:** Typed memory + explicit uncertainty + preserved contradictions (not overwrites).
- **Relevance:** Humans hold contradictory beliefs and update confidence gradually. This is a concrete mechanism for non-overconfident, human-feeling revision.

### Post 6 — "Show HN: DeltaMemory — Persistent cognitive memory for production AI agents"

- **Source:** Hacker News
- **URL:** https://news.ycombinator.com/item?id=47161647
- **Date:** 2025
- **Community:** HN Show HN
- **Summary:** Automatic fact extraction + temporal reasoning. Claims 89% on long-conversation benchmarks, 50 ms retrieval, 97% cost reduction vs. raw token replay.
- **Pattern:** Temporal-aware fact extraction as a first-class memory primitive.
- **Relevance:** Temporal reasoning ("I told you this *last week*, not today") is a major tell when absent. Humans anchor memories in time.

### Post 3b — "State of AI Agent Memory 2026" (Mem0 blog)

- **Source:** Mem0 blog
- **URL:** https://mem0.ai/blog/state-of-ai-agent-memory-2026
- **Date:** Early 2026
- **Community:** Practitioners / production AI teams
- **Summary:** Industry-level synthesis. Key empirical result from ECAI 2025 Mem0 paper: full-context achieves 72.9% accuracy but requires ~26K tokens and 17.12 s p95 latency (not production-viable); Mem0 vector achieves 66.9% at 1.44 s p95 with ~1.8K tokens; Mem0 graph achieves 68.4% at 2.59 s. Graph memory adds ~1.5 pp accuracy over vector and handles contradiction detection and temporal reasoning that vectors cannot. VentureBeat prediction: graph memory will surpass RAG in usage for adaptive AI workflows in 2026.
- **Pattern:** Production-viable agent memory = selective retrieval + graph structure. Full-context replay is a research baseline, not an architecture.
- **Relevance:** The most rigorous head-to-head benchmark available for choosing a memory approach. Directly informs the Unslop memory layer decision.

---

## 2. Dual-process reasoning — System 1 vs System 2 in LLMs

### Post 7 — "Approaches to add logical reasoning into LLMs [D]"

- **Source:** Reddit — r/MachineLearning
- **URL:** https://old.reddit.com/r/MachineLearning/comments/123nczy/approaches_to_add_logical_reasoning_into_llms_d/
- **Community:** ML research readers
- **Summary:** Long thread debating whether LLMs are "stuck in System 1." Converges on CoT, self-consistency, Tree-of-Thoughts, Reflexion, and SELF-REFINE as proto-System-2 mechanisms. Skeptics note current LLMs exhibit non-human biases (hallucination) that differ from human System-1 biases.
- **Pattern:** Current LLMs default to pattern-completion (System 1). System-2 emerges only via explicit scaffolding — search, reflection, verification.
- **Relevance:** "Humanized thinking" is *not* just fast output — it's the interplay. Producing only System-1 output feels glib; producing only System-2 feels robotic. The human feel is in the hand-off.

### Post 8 — "Progress happens in a weird way: my thoughts on the Turing test"

- **Source:** Reddit — r/singularity
- **URL:** https://www.reddit.com/r/singularity/comments/1opau1i/progress_happens_in_a_weird_way_my_thoughts_on/
- **Date:** 2025 Q4
- **Community:** r/singularity / futurists
- **Summary:** Argues Turing test effectively passed — modern LLMs convince ~99.9% of casual users they're human. "Thinking" as a term for LLM CoT is now normalized discourse.
- **Pattern:** Public vocabulary has absorbed "thinking" for LLMs; the interesting frontier has shifted from *fooling* humans to producing output that is *coherent over long horizons* like a human mind.
- **Relevance:** Branding / positioning signal — "humanize" now means something more than Turing-passing; it means sustained coherent persona, voice, and reasoning over time.

### Post 9 — "OpenAI o1 / reasoning models" meta-discussion

- **Source:** Reddit — r/singularity (multiple threads) + OpenAI blog
- **URL (primary):** https://www.openai.com/index/learning-to-reason-with-llms/
- **Date:** 2024–2026
- **Community:** Singularity / AI-watcher
- **Summary:** Reasoning models generate *reasoning tokens* before answering, RL-trained for CoT effectiveness. Longer "thinking" → better results. Cited limits of prior LLMs: one-step-at-a-time, no mid-answer revision.
- **Pattern:** Test-time compute + RL-on-reasoning = closest production analogue to deliberate System-2 thinking.
- **Relevance:** For humanization, the hidden reasoning trace is exactly where "thinking" should live — not in the user-facing text. The user sees the considered output, not the scratchpad.

### Post 9b — "Stop Overthinking" — TMLR 2025 Survey

- **Source:** arXiv + GitHub `Eclipsess/Awesome-Efficient-Reasoning-LLMs`
- **URL:** https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs
- **Date:** Mar 2025 (TMLR 2025)
- **Community:** ML researchers
- **Summary:** First dedicated survey on efficient reasoning for LLMs. Documents that large reasoning models (LRMs) systematically overthink — generating redundant chain-of-thought regardless of task difficulty. Catalogs difficulty-adaptive strategies, dynamic system-switching methods (ACPO, Dualformer, DiffAdapt), and the monotonic accuracy–efficiency trade-off from Reasoning on a Spectrum. ACPO (NeurIPS 2025 poster) is confirmed as the most principled RL-based solution.
- **Pattern:** Overthinking is now a named, measured failure mode with a dedicated literature. Adaptive System-1/2 switching is the accepted solution.
- **Relevance:** Overthinking produces output that reads as AI-ish — verbose, hedging, over-justified. Humanization and efficiency are aligned goals: fix overthinking, fix tone.

### Post 9c — SOFAI-LM (coordination of fast LLM + slow LRM via metacognition)

- **Source:** npj Artificial Intelligence + Thinking Fast and Slow AI website (sites.google.com/view/sofai)
- **Date:** 2025
- **Community:** Research / architecture practitioners
- **Summary:** SOFAI-v2 extends the SOFAI architecture to coordinate a fast LLM (System 1) with a slower LRM (System 2) through a real-time metacognitive governance layer. The metacognitive module decides which system to invoke based on task difficulty — without a pre-set budget — and reflects on outcomes to improve future selections. Demonstrates higher decision quality with less compute than either system alone.
- **Pattern:** Metacognitive arbitration > fixed-mode reasoning. The metacognitive module is a distinct, modular component — not an implicit property of a long context.
- **Relevance:** The cleanest current architectural template for "think when it matters, don't overthink when it doesn't." The metacognitive layer is exactly where a humanization-first design should focus.

---

## 3. Metacognition & self-reflection architectures

### Post 10 — "Capabilities and alignment of LLM cognitive architectures"

- **Source:** LessWrong / AI Alignment Forum
- **URL:** https://www.lesswrong.com/posts/ogHr8SvGqg9pW5wsT/capabilities-and-alignment-of-llm-cognitive-architectures
- **Author:** Seth Herd
- **Community:** LessWrong / alignment researchers
- **Summary:** Defines *Language Model Cognitive Architectures* (LMCAs): base LLMs scaffolded with executive function, episodic memory, and goal-directed agency (à la AutoGPT, Reflexion, HuggingGPT, BabyAGI). Argues their key property is that they think in natural language, enabling "natural language alignment."
- **Pattern:** The LLM is a *component,* not the whole agent. Humanlike behavior comes from what surrounds it.
- **Relevance:** Core framing for this project — humanizing AI is an *architecture* problem, not a prompt problem.

### Post 11 — "Simulators" (janus)

- **Source:** LessWrong
- **URL:** https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators
- **Author:** janus
- **Community:** LessWrong / alignment
- **Summary:** Reframes GPT-style LLMs as *simulators* — Bayes-optimal text completers, not agents/oracles/genies. A prompted LLM isn't answering a question; it's simulating text *about* a question being answered. Asking "how would a smart AI answer?" produces smarter text because it simulates that frame.
- **Pattern:** LLM outputs = conditional simulations. Persona and "thinking style" are *summoned,* not intrinsic.
- **Relevance:** Massive implication for humanization — the right move isn't "make the model human," it's *condition it to simulate a specific human-shaped cognitive process.* The cognitive architecture is the conditioning scaffold.

### Post 12 — "An LLM-based 'exemplary actor'" (Roman Leventov)

- **Source:** LessWrong
- **URL:** https://www.lesswrong.com/posts/4ztqncYBakD6DWuXC/an-llm-based-exemplary-actor
- **Community:** LessWrong / alignment
- **Summary:** Proposes an LLM equipped with textbooks on epistemology, rationality, and ethics, plus tools, that iteratively critiques and refines its own plans/predictions until convergence.
- **Pattern:** Internalized critic + curriculum of reasoning references + iterate-to-convergence.
- **Relevance:** This is a concrete recipe for a "thoughtful" persona — it's not the base LLM, it's the loop with a curated self-critique corpus.

### Post 13 — "Meta-cognitive AI architectures" cluster (MultiMind v2 / Think² / MIRROR)

- **Source:** Medium / arXiv / research blogs (cited widely on Twitter/X)
- **URLs:**
  - MultiMind v2: https://medium.com/@federicogiampietro/multimind-v2-an-advanced-deliberative-inference-framework-d96bd271a503
  - Think²: https://arxiv.org/abs/2602.18806v1
  - MIRROR: https://arxiv.org/html/2506.00430v1
- **Date:** 2025–2026
- **Summary:** Three converging lines of work. **MultiMind v2:** Supervisor orchestrating analytical/creative sub-models for "multi-voiced" output. **Think²:** grounds CoT in Ann Brown's Planning–Monitoring–Evaluation regulatory cycle; 3× self-correction improvement, 84% human preference for trustworthiness. **MIRROR:** parallel cognitive threads (goals/reasoning/memory) running *between turns,* reduces sycophancy and constraint-drop; up to 156% improvement on safety-critical tasks.
- **Pattern:** Explicit, named metacognitive stages (monitor / control / reflect) dramatically outperform implicit CoT — and *humans rate them as more trustworthy.*
- **Relevance:** This is the most direct evidence in the digest that *structured metacognition* is a humanization technique per-se — humans prefer it subjectively. Between-turn inner monologue (MIRROR) is particularly interesting for long conversations.

### Post 13b — "Language Models Coupled with Metacognition Can Outperform Reasoning Models" (arXiv 2025)

- **Source:** arXiv:2508.17959
- **Date:** August 2025
- **Community:** ML researchers
- **Summary:** Proposes a dual-loop reflection method — extrospection (LLM critiques its own reasoning against human reference responses) + introspection (uses that critique to update reasoning). Outperforms standard reasoning models on several benchmarks at lower cost. Key finding: a small metacognitive scaffold on a standard LLM can beat a larger, specialized reasoning model.
- **Pattern:** Metacognition is a cost-effective alternative to scaling reasoning. The metacognitive loop provides capability gains without the overthinking failure mode.
- **Relevance:** Directly relevant for a humanization project: structured metacognition produces better results AND avoids the verbose reasoning-token output that reads as AI-ish.

### Post 13c — "Truly Self-Improving Agents Require Intrinsic Metacognitive Learning" (ICML 2025)

- **Source:** arXiv:2506.05109; ICML 2025
- **Date:** 2025
- **Community:** ML researchers / alignment
- **Summary:** Position paper arguing that genuine self-improvement requires three distinct metacognitive components: metacognitive knowledge (what can I do?), metacognitive planning (what should I learn?), and metacognitive evaluation (did that learning work?). Current LLM agents, even with reflection loops, lack intrinsic metacognitive learning — they improve within a task but don't modify their learning process itself.
- **Pattern:** Metacognition has three layers: knowledge, planning, evaluation. Most reflection loops only implement the evaluation layer.
- **Relevance:** Defines the ceiling for "feels like a learning entity." A humanized AI that seems to grow requires all three metacognitive layers, not just post-hoc self-critique.

---

## 4. Agent loops, planning, and the "perceive-plan-execute" frame

### Post 14 — "Show HN: Cogency — Cognitive Architecture for AI Agents"

- **Source:** Hacker News
- **URL:** https://news.ycombinator.com/item?id=44542163
- **Date:** 2025
- **Community:** HN Show HN
- **Summary:** Open-source framework packaging CoALA-style cognitive architecture (modular memory, structured action space, decision loop) as a usable library.
- **Pattern:** CoALA (Cognitive Architectures for Language Agents, Sumers/Yao/Narasimhan/Griffiths 2023) is now the canonical reference frame for practitioners. Threads repeatedly cite it as the "grown-up" organization of agents.
- **Relevance:** If we're building a humanized thinking layer, CoALA's vocabulary (working memory / episodic / semantic / procedural + internal vs external actions) is the lingua franca. Pick sides explicitly.

### Post 15 — "Does anyone have an understanding — or intuition — of what the agentic loop looks like?"

- **Source:** Hacker News (comment thread on Claude-Code-style agents)
- **URL:** https://news.ycombinator.com/item?id=45841522
- **Date:** 2025
- **Community:** HN devs
- **Summary:** Top-voted takeaway — the loop itself is trivially `while True: call_llm(system, state)`. Complexity lives in token/context management, memory, and tool selection, *not* in loop structure.
- **Pattern:** Structure is easy; the hard part is *what goes into context each turn.* This dovetails with the context-engineering discourse.
- **Relevance:** For humanizing output, the loop is table-stakes. The real work is curating per-turn context so the model simulates the right "person" consistently.

### Post 16 — "Context engineering" cluster (r/LocalLLaMA + Karpathy)

- **Source:** Reddit r/LocalLLaMA thread on 44 agent frameworks + Karpathy coinage
- **URLs:**
  - https://www.reddit.com/r/LocalLLaMA/comments/1r84o6p/i_did_an_analysis_of_44_ai_agent_frameworks/
  - Karpathy originating tweets (2024)
- **Date:** 2024–2026
- **Community:** r/LocalLLaMA + Twitter/X AI-dev
- **Summary:** Practitioners have shifted vocabulary from *prompt* engineering to *context* engineering — "the art of filling the context window usefully." Four named failure modes surfaced: **context poisoning** (hallucinations treated as fact), **context distraction** (overload), **context confusion** (irrelevant noise), **context clash** (contradictory content). Context quality degrades around 25% window fill, not at the limit.
- **Pattern:** Humanlike coherence emerges from clean, well-curated context — not bigger windows.
- **Relevance:** Practical anchor. Whatever cognitive architecture we pick, the humanization work lives in *what we choose to put into each turn's context,* and what we deliberately evict.

---

## 5. Humanizing AI output — the applied-writing angle

### Post 17 — "How to humanize AI text" community synthesis

- **Source:** Reddit — r/OpenAI, r/SEO, r/freelancewriters (aggregated across multiple threads)
- **URL:** https://thehumanizeai.pro/articles/how-to-humanize-ai-text-reddit (secondary aggregator; see also r/OpenAI threads on "AI writing tells")
- **Community:** Writers / SEOs / prompters
- **Summary:** Concrete, repeated community diagnoses of why AI text reads as AI:
  - Uniform sentence lengths (low burstiness)
  - Transition-word tics ("moreover," "furthermore," "additionally")
  - Hedging ("it is important to note")
  - Overused vocabulary ("delve," "tapestry," "plays a crucial role")
  - Forced neatness — no contradictions, no tangents, no mid-paragraph mind-changes
  
  Recommended techniques: "Frankenstein" prompting (feed your own writing samples), deliberate imperfection (em-dashes, starting sentences with "And"/"But"), varying sentence length, the "read aloud" test.
- **Pattern:** Humanness = variance + voice + controlled imperfection + willingness to self-contradict.
- **Relevance:** This is the *output-surface* counterpart to the cognitive-architecture work. The architecture produces the reasoning; these techniques govern how the reasoning gets verbalized. Both are needed.

### Post 18 — "Framework: treating AI/LLMs as part of extended cognition"

- **Source:** Reddit — r/PhilosophyofMind
- **URL:** https://www.reddit.com/r/PhilosophyofMind/comments/1p4puhp/framework_treating_aillms_as_part_of_the_extended/
- **Community:** Philosophy of mind
- **Summary:** Positions LLMs as *cognitive amplifiers* for humans — iterative reflection, knowledge accumulation, cross-domain reinforcement — rather than autonomous minds. Emphasizes reducing "cognitive drift."
- **Pattern:** Reframe from "AI pretends to be human" to "AI augments human thinking, and therefore needs to think in compatible patterns."
- **Relevance:** Strong product-positioning frame for "Unslop." A humanized AI isn't impersonating a person — it's thinking in a way a human can co-think with.

---

## 6. YouTube lectures and primary references

### Post 19 — "Building Brain-Like Memory for AI | LLM Agent Memory Systems" (Adam Lucek)

- **Source:** YouTube
- **URL:** https://www.youtube.com/watch?v=VKPngyO0iKg
- **Length / reach:** 43:31, ~47.6K views
- **Summary:** Walks through implementing four psychological memory types in an LLM agent: **working, episodic, semantic, procedural.** Explicitly frames it around the statelessness problem — humans bring prior experience, LLMs don't.
- **Pattern:** Canonical practitioner reference for the four-memory-type taxonomy (Tulving-adjacent).
- **Relevance:** The clearest "starter kit" lecture for replicating human memory structure.

### Post 20 — "Everything about LLM Agents — CoT, Reflection, Tool Use, Memory, Multi-Agent"

- **Source:** YouTube
- **URL:** https://www.youtube.com/watch?v=Ll7lRBaP378
- **Summary:** Broad survey lecture — tours CoT, Reflexion, tool-use patterns, memory, multi-agent orchestration. Community-cited introductory reference.
- **Relevance:** Orientation material — useful for onboarding contributors before diving into specific components.

### Post 21 — Cognitive Architectures for Language Agents (CoALA) — primary paper

- **Source:** arXiv (referenced constantly across all above threads)
- **URL:** https://arxiv.org/abs/2309.02427
- **Authors:** Sumers, Yao, Narasimhan, Griffiths (Princeton)
- **Date:** Sept 2023 (still the canonical reference)
- **Summary:** Three pillars: (1) modular memory (working + episodic/semantic/procedural), (2) structured action space (internal reasoning + external tool use), (3) a plan–execute decision cycle.
- **Relevance:** The paper that HN, Reddit, and LessWrong all back-reference. Adopt its vocabulary for internal docs to stay compatible with the broader ecosystem.

---

## Patterns & trends (cross-source synthesis)

1. **Memory is the frontier, not the context window.** Every community (r/LocalLLaMA, HN, LessWrong, YouTube) has converged on "statelessness is the core problem" and on typed-memory solutions (working / episodic / semantic / procedural). Bigger context windows are *not* considered a substitute.

2. **Graph memory is the 2025–2026 frontier within memory.** By early 2026, practitioners have moved past "vector or no vector" to "vector or graph." The Mem0 ECAI 2025 benchmark gives the concrete numbers: graph adds ~1.5 pp accuracy over vector and is the only approach that handles contradictions and temporal reasoning. Production stacks now choose per use case: vector for fast lookup, graph for long-horizon relational reasoning.

3. **Cognitive science vocabulary has been absorbed.** Tulving's memory taxonomy, Kahneman's dual-process, Nelson–Narens metacognitive monitoring/control — all are now routine terms in practitioner threads. The field has picked sides: human cognitive science is the scaffold.

4. **"Thinking" as a first-class stage is normalized.** OpenAI o1-style reasoning tokens, CoT, ToT, Reflexion, MIRROR-style between-turn monologues — across sources, the consensus is that humanlike output requires an *explicit separate reasoning stage* that the user does not directly see.

5. **Overthinking is now a named, measured failure mode.** The TMLR 2025 "Stop Overthinking" survey makes this formal. The corollary for humanization: always-on chain-of-thought produces verbose, AI-ish output. Adaptive switching (ACPO, Dualformer, SOFAI-LM) is the fix, and the fix happens to also reduce the AI-ish surface.

6. **Metacognition as a distinct architectural layer — not just a loop.** SOFAI, "Language Models Coupled with Metacognition" (Aug 2025), and "Truly Self-Improving Agents" (ICML 2025) converge on treating the metacognitive module as a first-class component. Practitioners are beginning to implement this explicitly rather than relying on a single reflection prompt.

7. **Context engineering > prompt engineering.** Unanimous across HN + r/LocalLLaMA + Karpathy. The interesting craft is curating what enters the context window per turn — including evictions, summaries, and retrievals — not writing cleverer prompts.

8. **Structured metacognition measurably improves perceived trustworthiness.** Think² reported 84% human preference; MIRROR reported 156% relative improvement on safety-critical tasks; "Language Models Coupled with Metacognition" (Aug 2025) shows metacognition outperforms larger reasoning models on some benchmarks. Metacognitive scaffolding isn't just a capability lift — *users feel* the output is more human.

9. **Preserve contradictions, don't overwrite.** Mnemo (HN) and Reddit threads on long-running memory agree: humanlike belief update is *Bayesian and contradiction-preserving,* not replace-on-write. Graph memory (Mem0 graph, MAGMA) now provides the infrastructure for this — graph edges can represent contradictions explicitly, which vector embeddings cannot.

10. **Output-surface humanization and architectural humanization are separate problems.** Reddit writing threads (burstiness, voice, controlled imperfection) and cognitive-architecture threads (memory, metacognition) rarely overlap, but both are necessary. Unslop's advantage is in *bridging* them.

11. **Simulators frame (janus) is the deepest lens.** The LLM doesn't "become" human — it *simulates* a specified human-shaped process. This changes the design goal from "train a human" to "specify, scaffold, and condition a simulation of human-like thinking."

---

## Gaps — where practitioner discourse is thin

- **Voice/persona consistency across episodic memory.** Lots of work on *storing* episodic memory, very little on *retrieving it in a stylistically consistent way.* If a user's past exchanges informed "Unslop's voice," how does the architecture keep voice stable under retrieval? Open.

- **Deliberate imperfection as an architectural feature.** The writing community knows imperfection humanizes output; the cognitive-architecture community never treats it as a design variable. No posts found that *architecturally* model hedging, self-contradiction, or tangents as emergent properties.

- **Metacognition → output style.** Think²/MIRROR show metacognition improves reasoning *quality* and *perceived* trust, but do not address how the metacognitive trace should (or should not) leak into the user-facing voice.

- **Emotion / affect as a cognitive layer.** Cognitive-architecture threads mostly omit affect. A few r/artificial / r/PhilosophyofMind posts mention it, but no production architecture integrates affective state as a memory or control variable.

- **Time-aware identity.** Temporal reasoning (DeltaMemory) exists for facts, not for *self.* There's no practitioner pattern for "the agent's beliefs/style have evolved over our relationship" — a real human trait.

- **Evaluation for humanness.** No standard benchmark for "humanized thinking." LoCoMo and similar test recall, not voice, not metacognitive trust. Unslop will likely need its own eval.

---

## Sources actually consulted in synthesis

- Reddit r/LocalLLaMA memory threads (Posts 1, 2, 3, 16)
- Reddit r/MachineLearning dual-process thread (Post 7)
- Reddit r/singularity Turing-test + o1 threads (Posts 8, 9)
- Reddit r/PhilosophyofMind extended-cognition framework (Post 18)
- Reddit humanize-AI community synthesis across r/OpenAI / r/SEO / r/freelancewriters (Post 17)
- Hacker News: Cogency, Mnemo, DeltaMemory, three-layer memory, agentic-loop thread (Posts 4, 5, 6, 14, 15)
- LessWrong: Seth Herd (LMCAs), janus (Simulators), Leventov (exemplary actor) (Posts 10, 11, 12)
- Medium / arXiv metacognition cluster: MultiMind v2, Think², MIRROR (Post 13)
- YouTube: Adam Lucek, broad LLM-agents survey (Posts 19, 20)
- Primary paper: CoALA — Sumers et al., arXiv:2309.02427 (Post 21)
