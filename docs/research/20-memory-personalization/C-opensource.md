# Category 20 — Memory & Personalization

**Angle C — Open-Source & GitHub**

**Project:** Unslop (humanizing AI output and thinking)
**Research date:** 2026-04-19
**Last updated:** 2026-04-21
**Scope:** The open-source stack for persistent LLM memory, user personalization, and lightweight fine-tuning that enables an assistant to "remember who I am, how I talk, and what I care about" across sessions — MemGPT/Letta, mem0, Zep/Graphiti, LangMem, LlamaIndex memory blocks, A-MEM, MemoryBank, MemoRAG, EM-LLM, Cognee, MemoryScope/ReMe, Motorhead, gptme, ChromaDB memory recipes, plus personalized fine-tuning tooling (Axolotl, Unsloth, PersonaMem-v2).

---

## Research value: high

Memory is the single most active sub-ecosystem in open-source agent tooling in 2025–2026. Two factors make it especially fertile for a humanization project: (1) every serious memory framework now distinguishes **semantic / episodic / procedural** memory types — the same taxonomy used by psychologists describing human autobiographical memory; and (2) the field has bifurcated into "retrieval-style" memory (mem0, Chroma recipes, Motorhead) and "self-organizing" memory (A-MEM, MemoryBank, Cognee, Graphiti) that more explicitly models *how* a mind updates its own notes. For making an AI feel like it actually knows the user, the second camp is where the leverage is.

---

## Repository Matrix

| # | Repo | Stars (approx) | License | Language | Status | Relevance to humanization |
|---|---|---|---|---|---|---|
| 1 | [letta-ai/letta](https://github.com/letta-ai/letta) (ex-MemGPT) | ~22.1k | Apache 2.0 | Python | Active (v0.16.7, Mar 2026) | Stateful agents with persistent **memory blocks**; self-editing context — originator of the "OS for LLMs" metaphor |
| 2 | [mem0ai/mem0](https://github.com/mem0ai/mem0) | ~48k | Apache 2.0 | Python / TS | Active (v2.x, Apr 2026); AWS Agent SDK exclusive provider | Universal memory layer: User/Session/Agent levels; LoCoMo 66.9% (independent), LongMemEval self-reported 93.4 |
| 3 | [getzep/graphiti](https://github.com/getzep/graphiti) | ~25.1k | Apache 2.0 | Python | Active (v0.28.2, Mar 2026) | Temporal knowledge graph memory; tracks how facts **change over time** with provenance |
| 4 | [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | ~976 | MIT | Python | Active (NeurIPS 2025) | **Zettelkasten-inspired** agentic memory — notes auto-link and evolve as new memories arrive |
| 5 | [langchain-ai/langmem](https://github.com/langchain-ai/langmem) | ~1.4k | MIT | Python | Active (v0.0.30) | LangGraph-native semantic / episodic / procedural memory SDK — official replacement for deprecated `ConversationBufferMemory` lineage |
| 6 | [topoteretes/cognee](https://github.com/topoteretes/cognee) | ~16.4k | Apache 2.0 | Python (93%) | Active (v0.5.7) | "Knowledge engine for AI agent memory in 6 lines" — graph + vector + ontology grounding, multi-tenant isolation |
| 7 | [qhjqhj00/MemoRAG](https://github.com/qhjqhj00/MemoRAG) | — | Apache 2.0 | Python | Active (WWW 2025) | Dual-system RAG: cheap global-memory drafter + expensive retriever; KV-compressed memory reinforced via RLGF |
| 8 | [em-llm/EM-LLM-model](https://github.com/em-llm/EM-LLM-model) | — | OSS | Python | ICLR 2025 | **Episodic memory** for LLMs: Bayesian-surprise event segmentation; scales to 10M tokens with no fine-tuning |
| 9 | [zhongwanjun/MemoryBank-SiliconFriend](https://github.com/zhongwanjun/MemoryBank-SiliconFriend) | ~419 | OSS | Python | AAAI 2024 | Applies **Ebbinghaus forgetting curve** — memories decay or reinforce by time + significance. "SiliconFriend" companion bot |
| 10 | [modelscope/MemoryScope](https://github.com/modelscope/MemoryScope) → [agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe) | ~2.6k | Apache 2.0 | Python | Active (v0.3.1.8) | 20+ memory workers: retrieval, **consolidation**, reflection, re-consolidation — explicit cognitive stages |
| 11 | [bowen-upenn/PersonaMem-v2](https://github.com/bowen-upenn/PersonaMem-v2) | — | OSS | Python | Active (Mar 2026) | 1,000 personas × 20k preferences benchmark; GRPO over long-context training recipe for implicit personalization |
| 12 | [run-llama/llama_index](https://github.com/run-llama/llama_index) (memory module) | ~44k+ | MIT | Python | Active | Memory class with pluggable blocks: `ChatMemoryBuffer`, `VectorMemoryBlock`, `FactExtractionMemoryBlock` |
| 13 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) (memory) | ~100k | MIT | Python / TS | Memory module **deprecated**; migrate to LangGraph Checkpointer / LangMem | Historical vocabulary: ConversationBuffer/Summary/EntityMemory |
| 14 | [gptme/gptme](https://github.com/gptme/gptme) | — | MIT | Python | Active (v0.30+) | "Living memory systems": Journal / Tasks / Knowledge / Relationships / Projects, with version-controlled agent profiles |
| 15 | [getmetal/motorhead](https://github.com/getmetal/motorhead) | — | Apache 2.0 | Rust | **Deprecated** (v3.0.2 Dec 2023) | Early Redis-backed memory server with rolling summaries + VSS retrieval |
| 16 | [chroma-core/chroma](https://github.com/chroma-core/chroma) | ~19k+ | Apache 2.0 | Python / Rust | Active | Default vector store under most memory recipes (A-MEM, AutoGen's `ChromaDBVectorMemory`, countless RAG stacks) |
| 17 | [mem0ai/mem0 /openmemory](https://github.com/mem0ai/mem0/tree/main/openmemory) | (part of mem0) | Apache 2.0 | Python | Active | **OpenMemory MCP**: local-first memory server shared across Cursor / Claude Desktop / Windsurf / Cline via MCP |
| 18 | [mem0ai/mem0 /embedchain](https://github.com/mem0ai/mem0/tree/main/embedchain) | (absorbed) | Apache 2.0 | Python | Maintained inside mem0 | Personalization-oriented RAG framework; predecessor of mem0's ingest layer |
| 19 | [axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl) | ~8k+ | Apache 2.0 | Python | Active (v0.16.1, Apr 2026) | YAML-driven LoRA/QLoRA/DPO/GDPO fine-tuning — produces **style-personalized** base models |
| 20 | [unslothai/unsloth](https://github.com/unslothai/unsloth) | ~40k+ | Apache 2.0 | Python / Triton | Active | 2×–30× faster LoRA/QLoRA with 70–80% less VRAM — makes per-user / per-persona fine-tunes tractable on consumer GPUs |
| 21 | [aiming-lab/SimpleMem](https://github.com/aiming-lab/SimpleMem) | — | OSS | Python | Active (Jan 2026); ICLR 2026 submission | Efficient lifelong memory via semantic lossless compression: 3-stage pipeline (compress → consolidate → retrieve); +26.4% mean F1, 30× token reduction, +64% over Claude-Mem on LoCoMo; multimodal |

---

## Representative README quotes

**Letta (ex-MemGPT) — `letta-ai/letta`:**
> "Letta is the platform for building stateful agents: AI with advanced memory that can learn and self-improve over time." Companion project `letta-code` frames its contribution as "a **memory-first coding agent**" with `/init` and `/remember` commands that let the agent reflect on and persist learned skills across sessions.

**Mem0 — `mem0ai/mem0`:**
> "Universal memory layer for AI Agents." Latest algorithm release claims "+26% accuracy over OpenAI Memory, 91% faster responses, 90% lower token usage," with "Multi-Level Memory: Retains User, Session, and Agent state with adaptive personalization" and "Multi-signal retrieval: Semantic, BM25 keyword, and entity matching scored in parallel and fused." LoCoMo 91.6, LongMemEval 93.4, BEAM (1M tokens) 64.1.

**Zep / Graphiti — `getzep/graphiti`:**
> "Build Real-Time Knowledge Graphs for AI Agents." From the associated paper: Graphiti "dynamically integrates unstructured conversational data and structured business data while maintaining historical relationships… [and] outperforms MemGPT on the Deep Memory Retrieval benchmark (94.8% vs 93.4%)" and "achieves up to 18.5% accuracy improvements while reducing response latency by 90%" on LongMemEval.

**A-MEM — `agiresearch/A-mem`:**
> "A-MEM: Agentic Memory for LLM Agents." Uses **Zettelkasten principles**: when a new memory is added, the system "generates comprehensive notes with structured attributes… analyzes historical memories for relevant connections… [and] new memories can trigger updates to existing memory attributes, allowing continuous refinement."

**LangMem — `langchain-ai/langmem`:**
> LangMem provides "a core memory API that works with any storage system… memory management tools that agents can use to record and search information during conversations… [and] a background memory manager that automatically extracts, consolidates, and updates agent knowledge." Supports three memory types: "**Semantic memory**: Facts and knowledge… **Episodic memory**: Past experiences and few-shot examples… **Procedural memory**: System behavior and response patterns."

**Cognee — `topoteretes/cognee`:**
> "Knowledge Engine for AI Agent Memory in **6 lines of code**." Three lines suffice for a working memory: `await cognee.add(...)`, `await cognee.cognify()`, `await cognee.search(...)`. Pitch is "persistent and learning agents [that] learn from feedback, manage context, and share knowledge across agents," with "agentic user/tenant isolation, traceability, OTEL collector, and audit trails."

**MemoryBank — `zhongwanjun/MemoryBank-SiliconFriend`:**
> Paper abstract: "MemoryBank enables the models to summon relevant memories, continually evolve through continuous memory updates, comprehend, and adapt to a user's personality over time by synthesizing information from previous interactions." Built explicitly on "the principles of the **Ebbinghaus Forgetting Curve** theory, allowing the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory."

**MemoryScope / ReMe — `agentscope-ai/ReMe`:**
> Framed around three cognitive stages: "memory **retrieval** (returning semantically related memory pieces), memory **consolidation** (extracting user information), and **reflection / re-consolidation** (forming insights at regular intervals)." ReMe adds "file-based memory… storing memories as readable Markdown files" alongside vector memory.

**EM-LLM — `em-llm/EM-LLM-model`:**
> "A novel approach that integrates key aspects of human episodic memory and event cognition into LLMs." Segments token streams into coherent events via "Bayesian surprise and graph-theoretic boundary refinement," then retrieves with a "two-stage memory retrieval combining similarity-based and temporally contiguous retrieval" — demonstrated across 10M-token contexts without fine-tuning.

**MemoRAG — `qhjqhj00/MemoRAG`:**
> "Empowering RAG with a memory-based data interface for all-purpose applications." Dual system: "a light but long-range LLM [that] forms the global memory of database" and generates draft clues, plus "an expensive but expressive LLM" that finalizes the answer against retrieved chunks; memorization is reinforced through Generation-quality Feedback (RLGF).

**gptme — `gptme/gptme`:**
> Describes its agent stack as a **"Living Memory System"**: "Journal records every decision and insight… Tasks tracks goals… Knowledge stores learned lessons… Relationships maintains collaboration history and social intelligence… Projects documents active work." Version-controlled on disk, with `/summarize`, `/context`, and `gptme-util chats search` surfacing past conversation state.

**LlamaIndex memory — `run-llama/llama_index`:**
> "The Memory class handles both short-term and long-term memory for agents. Short-term memory is represented as a FIFO queue of `ChatMessage` objects… When short-term memory exceeds its token limit, the oldest messages are either discarded or flushed to long-term memory blocks." Blocks include `VectorMemoryBlock`, `FactExtractionMemoryBlock`, and custom extractors.

**LangChain legacy memory — `langchain-ai/langchain`:**
> `ConversationBufferMemory` is now explicitly annotated: "Deprecated since version 0.3.1… will not be removed until langchain==1.0.0." LangChain.js has churned through three memory APIs in 18 months (ConversationBufferMemory → RunnableWithMessageHistory → LangGraph Checkpointer), each "tightly coupled to a specific abstraction layer."

**Motorhead — `getmetal/motorhead`:**
> "When the message window reaches its maximum size, Motorhead automatically summarizes the oldest messages and performs incremental summarization as conversations grow." Deprecated after v3.0.2 (Dec 2023) — historically important as one of the first Redis-backed chat-memory servers.

**OpenMemory MCP — `mem0ai/mem0/openmemory`:**
> "Local memory infrastructure powered by Mem0 that provides persistent memory across MCP-compatible AI tools." Exposes four MCP tools — `add_memories`, `search_memory`, `list_memories`, `delete_all_memories` — "unified memory UI dashboard… full local ownership and control of memory data… seamless context handoff across development, planning, and debugging environments."

**PersonaMem-v2 — `bowen-upenn/PersonaMem-v2`:**
> "Towards Personalized Intelligence via Learning Implicit User Personas and Agentic Memory." Benchmark covers "1,000 comprehensive user personas and 20,000+ preferences across 300+ scenarios, focusing on **implicit user preferences revealed through long-context conversations** rather than explicit statements." Ships GRPO-over-long-context training recipes built on the verl framework and adapted from MemAgent.

**Axolotl — `axolotl-ai-cloud/axolotl`:**
> Supports "full fine-tune, LoRA, QLoRA, ReLoRA, GPTQ… ScatterMoE LoRA, SageAttention, GDPO (Generalized DPO), EAFT (Entropy-Aware Focal Training)." Community guides report "fine-tuning a 7B model on domain data in an afternoon on consumer hardware (RTX 4070 Ti)." Standard stack is ChatML SFT → DPO for alignment.

**Unsloth — `unslothai/unsloth`:**
> "2× faster training and 70% less VRAM with zero accuracy loss… 10× faster than Flash Attention 2 on single GPUs, up to 30× on multi-GPU." Supports "full fine-tuning, LoRA, QLoRA, GRPO, PPO, vision, TTS, embeddings, multimodal" across 1B–405B models on NVIDIA/AMD/Intel GPUs. Practically: makes per-user style fine-tuning affordable.

**SimpleMem — `aiming-lab/SimpleMem`:**
> "SimpleMem proposes a three-stage pipeline: Semantic Structured Compression, which applies entropy-aware filtering to distill unstructured interactions into compact, multi-view indexed memory units; Recursive Memory Consolidation, an asynchronous process that integrates related units into higher-level abstract representations; and Adaptive Query-Aware Retrieval, which dynamically adjusts retrieval scope based on query complexity." Results: +26.4% mean F1 improvement, 30× inference-time token reduction, +64% over Claude-Mem on LoCoMo. Supports text and multimodal inputs.

---

## Patterns

1. **Three-tier memory typology is consolidating.** LangMem, LlamaIndex, gptme, and Letta all now explicitly model **semantic** (facts), **episodic** (experiences), and **procedural** (behavioral patterns) memory. This mirrors cognitive-psychology taxonomy and is the closest thing to a shared vocabulary in the space.
2. **Knowledge graphs beat flat vector stores for personalization.** Graphiti, Cognee, and A-MEM all move from "retrieve nearest embeddings" to "traverse a typed graph of entities and relations." The practical win is being able to answer questions like *"what has the user's opinion on X been over time?"* — which flat vector recall cannot do well.
3. **Memory is becoming its own service, shared across clients.** OpenMemory MCP, Letta server, and Zep-as-a-service all expose memory through a standard protocol (MCP or REST) so the same user identity persists across Cursor, Claude Desktop, and custom apps. Memory portability is quickly becoming table stakes.
4. **"Consolidation" and "reflection" are now first-class operations.** MemoryScope/ReMe, A-MEM, mem0's single-pass ADD-only extraction, and LangMem's background memory manager all run an asynchronous process that rewrites or re-links old memories — not just appending new ones. This is the structural move that turns a log into a mind.
5. **Self-organizing notes (Zettelkasten) are a recurring design.** A-MEM is the cleanest instance, but gptme's Journal/Knowledge/Relationships structure and Cognee's ontology grounding express the same intuition: memory should auto-link by topic, not just by recency.
6. **Forgetting is back in fashion.** MemoryBank's explicit Ebbinghaus-curve decay and MemoRAG's KV compression push back against the "store everything forever" default. For humanization, strategic forgetting is what keeps responses from sounding like a creepy surveillance archive.
7. **Personalization below the prompt layer.** PersonaMem-v2, SiliconFriend (LoRA on 38K empathic-dialogue pairs), Axolotl, and Unsloth make **per-persona / per-user lightweight fine-tunes** a realistic option. This is a distinct humanization surface from retrieval-based memory — style lives in weights, facts live in memory.
8. **Benchmarks now rank memory systems by *accuracy over time*.** LoCoMo, LongMemEval, DMR, and BEAM are becoming the standard evaluation axes; claims like "LongMemEval 93.4" (mem0) or "DMR 94.8% vs MemGPT 93.4%" (Zep) are starting to arrive in READMEs. The field is moving from demos to measurable claims.

## Trends

- **LangChain's memory modules are a cautionary tale** — three deprecations in 18 months have pushed the frontier into purpose-built projects (Letta, mem0, LangMem, Zep), not chain-coupled helpers. Any new dependency on a framework-bound memory API in 2026 is fragile.
- **MCP is becoming the integration substrate for memory.** OpenMemory MCP, Graphiti MCP, Letta MCP — once a user's memory is exposed as an MCP server, any compliant client inherits it. Expect this to be the dominant interop pattern by end of 2026. Mem0's MCP Plugin for AI Editors (launched Mar–Apr 2026) ships 9 MCP memory tools with lifecycle hooks and cloud MCP server support.
- **Episodic event segmentation is quietly crossing from neuroscience to production.** EM-LLM (Bayesian surprise) and A-MEM's note-linking are direct imports from event-boundary theories in cognitive psychology. For a humanization project that wants the AI's recall to feel like *"oh yeah, that conversation last week"* instead of *"here are 5 similar chunks,"* this is the right thread to pull.
- **Fast, consumer-grade fine-tuning has become the back half of personalization.** Unsloth on a 4060/4070 + Axolotl YAML configs + a few hundred examples of the target voice is now a credible nightly pipeline — no longer research-only.
- **Compression-first memory (SimpleMem, MemoRAG) is emerging as an alternative to extraction-first memory.** Rather than extracting salient facts and appending them, compression-first systems distill entire dialogue streams into compact indexed units, then consolidate asynchronously. +64% over Claude-Mem on LoCoMo and 30× token savings make this the highest-efficiency approach published as of Apr 2026.
- **Enterprise cloud vendors entered the architecture conversation directly.** Microsoft (Azure AI Foundry, Mar 2026), Oracle (Database 26ai, CY2026), and AWS (Mem0 as exclusive partner for Agent SDK) are all making architectural bets about where memory lives. The container-orchestration-in-2015 analogy: multiple competing architectures, no consensus yet.

## Gaps

1. **"Tone memory" is missing.** Almost every framework stores *what* the user said (facts, preferences) but not *how they say it* (cadence, favorite metaphors, punctuation idiosyncrasies, reading level). For a humanization project, a dedicated **style memory block** — distinct from semantic memory — appears to be greenfield.
2. **No canonical "forgetting policy" library.** Only MemoryBank implements decay seriously, and it is a research artifact, not a dependency you drop into Letta or mem0. A pluggable forgetting-curve / salience-weighted pruning layer is an obvious missing piece.
3. **Memory UX is underdeveloped.** OpenMemory has a dashboard and Cognee has a Next.js UI, but there is no widely adopted pattern for **user-visible memory editing** ("here's what I remember about you — correct me"). That visibility is precisely what makes memory feel trustworthy and human rather than stalkerish.
4. **Privacy boundaries are weakly enforced.** Cognee ships tenant isolation and OpenMemory is local-first, but most recipes (A-MEM, MemoRAG, LangMem examples) assume a single-tenant store with no PII redaction. A "humanization-safe" memory profile (what to never persist, what to hash, what to let the user purge) is a documentation and tooling gap.
5. **Personalization and memory are still two stacks.** PersonaMem-v2 advances the weights-side personalization benchmark, but there is no open-source framework that *jointly* trains a LoRA on user style **and** writes structured memories from the same conversational stream. Closing that loop is the highest-leverage white space for a humanization product.
6. **Cross-model memory portability is unsolved.** Graph-shaped memories (Graphiti, Cognee) are model-agnostic in theory, but in practice embeddings and schema choices bind a memory store to a particular embedding model and LLM family. Migrating a user's memory from, say, OpenAI-embedded Zep to a locally hosted Cognee is painful.
7. **Evaluation harnesses for "feeling known" don't exist.** LoCoMo and LongMemEval measure factual recall. There is no standard benchmark for whether a humanized agent's reply sounds like it comes from someone who genuinely remembers *you* — the dimension that matters most for this project.

---

## Sources

- <https://github.com/letta-ai/letta> — Letta (ex-MemGPT) stateful agent platform
- <https://github.com/letta-ai/letta-code> — Letta Code memory-first coding agent
- <https://github.com/mem0ai/mem0> — Mem0 universal memory layer (incl. LLM.md, benchmarks)
- <https://github.com/mem0ai/mem0/tree/main/openmemory> + <https://mem0.ai/blog/introducing-openmemory-mcp> — OpenMemory MCP
- <https://github.com/mem0ai/mem0/tree/main/embedchain> — Embedchain (absorbed into mem0)
- <https://github.com/getzep/graphiti> — Graphiti temporal knowledge graph for Zep
- <https://arxiv.org/html/2501.13956> — Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- <https://github.com/agiresearch/A-mem> — A-MEM agentic memory (NeurIPS 2025)
- <https://github.com/langchain-ai/langmem> + <https://langchain-ai.github.io/langmem/concepts/conceptual_guide/> — LangMem SDK
- <https://python.langchain.com/docs/versions/migrating_memory/> — LangChain memory deprecation/migration notes
- <https://github.com/topoteretes/cognee> — Cognee knowledge engine for agent memory
- <https://github.com/qhjqhj00/MemoRAG> + <https://arxiv.org/abs/2409.05591> — MemoRAG paper + repo
- <https://github.com/em-llm/EM-LLM-model> — EM-LLM episodic memory (ICLR 2025)
- <https://github.com/zhongwanjun/MemoryBank-SiliconFriend> — MemoryBank + SiliconFriend (AAAI 2024)
- <https://github.com/modelscope/MemoryScope> → <https://github.com/agentscope-ai/ReMe> — MemoryScope / ReMe
- <https://github.com/bowen-upenn/PersonaMem-v2> + <https://github.com/bowen-upenn/PersonaMem> — PersonaMem benchmarks
- <https://developers.llamaindex.ai/python/examples/memory/memory/> — LlamaIndex memory blocks
- <https://github.com/gptme/gptme> + <https://gptme.org/docs/agents.html> — gptme living memory systems
- <https://github.com/getmetal/motorhead> — Motorhead (deprecated)
- <https://github.com/chroma-core/chroma> + <https://github.com/microsoft/autogen/pull/5308> — ChromaDB + AutoGen `ChromaDBVectorMemory` reference
- <https://github.com/axolotl-ai-cloud/axolotl> — Axolotl fine-tuning framework
- <https://github.com/unslothai/unsloth> — Unsloth fast LoRA/QLoRA fine-tuning
