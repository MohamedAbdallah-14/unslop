# Category 20 — Memory and Personalization

**Last updated:** 2026-04-21

## Scope

This category covers how persistent memory and user personalization transform a stateless LLM into an assistant that feels continuous — one that knows who you are, remembers how you talk, and tracks what you care about across sessions. The research spans memory architectures (tiered stores, temporal knowledge graphs, self-editing blocks, sleep-time consolidation, Zettelkasten-style auto-linking), preference modeling and low-rank personalization methods (P-RLHF, PReF, LoRe, VRF), benchmarks (LongMemEval, LoCoMo, LaMP/LongLaMP, PersonalLLM, DMR, BEAM), the open-source and commercial tooling ecosystem (Mem0, Zep, Letta, Cognee, Supermemory, Lex), and the practitioner failure modes and debates that have accumulated across r/ChatGPT, Hacker News, r/LocalLLaMA, and dev.to. The humanization angle is explicit throughout: memory is the single biggest lever for making AI output stop feeling stateless, generic, and averaged.

---

## Executive Summary

- Tiered memory has become the universal architecture. Every major platform — OpenAI, Anthropic, Google, Letta, LlamaIndex, LangGraph, Mem0, Zep, and DIY SQLite builds — has converged on roughly the same four tiers: short-term buffer, core/working context, searchable recall, and archival storage. The vocabulary differs; the shape does not. (A, B, C, D, E)

- Within that tiered structure, four moves are consistently winning: self-editing memory blocks where the LLM owns write operations (MemGPT → Letta → Anthropic's memory tool); temporal knowledge graphs with bi-temporal validity over flat vector stores (Zep's Graphiti, Cognee, A-MEM); two-agent memory management where a cheap extractor gates expensive typed CRUD writes; and async/sleep-time consolidation that keeps memory work off the latency-critical path. (A, B, C, D, E)

- The episodic / semantic / procedural split from cognitive psychology is re-emerging as a first-class architectural axis. PRIME, REMem, SEEM, Echo, LangMem, LlamaIndex, and gptme all now model these memory types separately. Systems that collapse everything into one vector store consistently lose on multi-session reasoning and temporal tasks. (A, C)

- Personalization is converging on low-rank preference manifolds. PReF (arXiv 2503.06358), LoRe (arXiv 2504.14439), and VRF (arXiv 2604.00997) independently arrive at the same inductive bias: per-user reward equals a weighted combination of shared basis rewards. PReF achieves a 67% win rate over default GPT-4o responses with 30× fewer user signals than naive RLHF. Cold start is tractable. (A)

- Benchmarks have matured and multiplied. LongMemEval (ICLR 2025) quantified the memory bottleneck — commercial assistants drop 30–60% accuracy on long-horizon histories. LoCoMo (ACL 2024) runs 300–600-turn imagined dialogues over 6–12-month timelines. PersonalLLM (ICLR 2025) provides heterogeneous-user preference evaluation. RealPref (Mar 2026) and HorizonBench (Apr 2026) now measure long-horizon implicit preference following and preference evolution respectively — the two dimensions most relevant to style/voice humanization. Current leaderboard: Zep ~71.2% LongMemEval independently / 94.8% DMR; Mem0 ~49% LongMemEval independently (self-reports 93.4%, unexplained 44-point gap); SimpleMem (Jan 2026) +64% over Claude-Mem on LoCoMo via compression-first approach; Letta strong architecturally but "not production-ready" by practitioner consensus. Benchmark credibility is now as important as benchmark coverage — vendor self-reports and independent tests diverge by 15–44 points. (A, C, D, E)

- Memory-as-a-Service is a funded category now being commoditized from above and from below. Mem0 ($24.5M, YC), Zep, Letta ($10M), Supermemory ($3M), and Cognee ($7.5M) sell drop-in memory APIs. Foundation-model vendors (ChatGPT Feb 2024 through GPT-5.4 Mar 2026, Gemini Mar 2025, Claude Sep 2025) ship native memory. Cloud hyperscalers entered directly in Q1 2026: Microsoft (Azure AI Foundry user-scoped memory on Cosmos DB + Entra ID, Mar 2026), Oracle (Database 26ai Unified Memory Core, CY2026), and AWS (Mem0 as exclusive memory provider for Agent SDK). Lex's Style Guides — "teaching Lex to match your signature tone, metaphors, terminology, narrative voice" — remain the closest commercial analog to the Unslop thesis. (B, D)

- Users are split on memory, and the dominant complaint is architectural. Roughly half use memory in a "relationship-driven" mode (assistant as colleague); the other half disable it as "context pollution" or a "memory dossier." The top structural complaint, across HN and r/ChatGPT, is that memory is account-global when it should be project-scoped. Anthropic's project-scoped model is held up repeatedly as the right default. (E)

- Security is an active concern. Researcher Johann Rehberger demonstrated that malicious documents or images can write persistent false memories into ChatGPT and exfiltrate all subsequent user inputs to an attacker server. OpenAI's partial mitigation (store only user messages, not assistant outputs) is widely cited but widely regarded as insufficient. (E)

- The "feels human" metric is the universal blind spot. All five angles — academic, industry, OSS, commercial, practitioner — benchmark retrieval accuracy. None benchmark whether output reads as coming from someone who actually knows you. This is the core gap for a humanization-focused product. (A, B, C, D, E)

---

## Cross-Angle Themes

**1. Tiered memory has won.**
Academic papers (MemGPT, MemoryLLM), industry posts (OpenAI/Anthropic/Gemini/Letta), OSS repos (Letta, LlamaIndex, LangGraph Checkpointer+Store), commercial products (Mem0 multi-level, Zep temporal tiers), and DIY builds (SQLite+Chroma with short/working/long) all converge on four tiers. The vocabulary varies; the shape does not.

**2. The episodic / semantic / procedural taxonomy is consolidating.**
Academic systems (PRIME, REMem, SEEM, Echo) name this split explicitly. Industry blogs (LangChain's CoALA-based post) map it onto product decisions. OSS projects (LangMem, gptme's Journal/Knowledge/Relationships, LlamaIndex memory blocks) ship it as distinct interfaces. Practitioners (Adam Lucek's "four-memory cognitive architecture" YouTube tutorial, 48.3K views) have adopted it as the default mental model. Commercial vendors are following (Zep episodes vs. graph facts, Supermemory User Profile vs. Memory Graph).

**3. Temporal reasoning is the new recall.**
Zep's bi-temporal knowledge graph (arXiv 2501.13956), Echo's time-span benchmark (arXiv 2502.16090), LongMemEval's "knowledge updates" category, LoCoMo's 6–12-month imagined timelines, and the practitioner "Adidas → Nike" invalidation demo all signal the same shift: "did we remember it?" has moved to "do we know it's still true?" Flat vector stores with no temporal validity cannot answer the second question.

**4. Memory is becoming a policy, not a data structure.**
RMM (ACL 2025) trains the retrieval policy online with RL and gains +10% on LongMemEval. A-MEM (NeurIPS 2025) evolves existing memories at write time rather than appending. PrLM (CIKM 2025) shows that reasoning explicitly over retrieved user facts outperforms naive concatenation. Practitioners independently converged on agentic memory tools with a 5-call budget per turn. What to remember, how to retrieve, and when to update are learned behaviors.

**5. Forgetting is finally a feature.**
MemoryBank's Ebbinghaus forgetting curve, MemoryLLM's exponential decay with ~1M-update stability, and MemoRAG's KV compression all treat controlled forgetting as a design goal. Practitioners routinely hit the opposite problem — hoarding, memory bloat, "memory dossier" — and have no canonical library to reach for. This is a real gap.

**6. Personalization is converging on low-rank preference manifolds plus implicit signal.**
PReF, LoRe, and VRF independently find that individual preference is low-dimensional. ALOE (COLING 2025) moves personalization signal from explicit ratings to implicit conversational cues. PersonaMem-v2's 1,000-persona / 20,000+ preference benchmark and Persona-Plug's per-user adapter are the OSS anchors. Cold start is solvable with tens of signals.

**7. Memory portability is the emerging trust lever.**
Letta's "continual learning in token space" (Dec 2025), Anthropic's `claude.com/import-memory` (Mar 2026), OpenMemory MCP, and GetProfile's OpenAI-compatible proxy all treat user memory as an asset the user can move — not a platform lock-in. This is new in 2025–2026 and is already reshaping vendor positioning.

**8. Two-agent memory is the production default.**
Industry (Letta's sleep-time compute, LangChain's background writes), OSS (LangMem's background memory manager, MemoryScope's consolidation worker), and practitioners (Christian Rice's Sentinel + Knowledge Master, r/LocalLLaMA's filter-then-extract pattern) all separate the conversational agent from a dedicated memory manager. Single-agent self-managed memory is architecturally cleaner but loses on cost and reliability.

**9. Infra cost is a first-class axis.**
Character.AI serves 20k QPS of long roleplay dialogues averaging 180 messages of history — a 95% KV-cache hit rate and 33× cost reduction since 2022. Mem0 reports −91% p95 latency and >90% token savings vs. full context. HippoRAG achieves 10–20× cheaper retrieval and 6–13× faster than iterative retrieval. Humanized long conversation is an economics problem, not just a prompting problem.

**10. The "feels human" metric is the shared blind spot.**
Every angle benchmarks retrieval accuracy. None benchmark whether output reads as authored by someone who knows you. This is the explicit greenfield for a humanization product.

---

## Top Sources

### Must-read papers

- **MemGPT: Towards LLMs as Operating Systems** — Packer et al., arXiv 2310.08560 (2023). OS-inspired virtual context management; the substrate every later memory system assumes. https://arxiv.org/abs/2310.08560
- **Zep: A Temporal Knowledge Graph Architecture for Agent Memory** — Rasmussen et al., arXiv 2501.13956 (2025). 94.8% Deep Memory Retrieval, −90% latency on LongMemEval; bi-temporal validity as first-class state. https://arxiv.org/abs/2501.13956
- **A-MEM: Agentic Memory for LLM Agents** — Xu et al., NeurIPS 2025. Zettelkasten-style memory that evolves at write time, addresses the rigidity critique of MemGPT. https://arxiv.org/abs/2502.12110
- **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory** — Chhikara et al., arXiv 2504.19413 (2025). +26% LLM-as-judge vs. OpenAI memory, −91% p95 latency, >90% token savings. https://arxiv.org/abs/2504.19413
- **HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs** — Gutiérrez et al., NeurIPS 2024. +20% multi-hop QA, 10–20× cheaper than iterative retrieval; biologically motivated retrieval. https://arxiv.org/abs/2405.14831
- **LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory** — Wu et al., ICLR 2025. Five abilities, 500 questions, 115k–1.5M token histories; commercial assistants drop 30–60%. https://arxiv.org/abs/2410.10813
- **LoCoMo: Evaluating Very Long-Term Conversational Memory of LLM Agents** — Maharana et al. (Snap Research), ACL 2024. 50 conversations, 300–600 turns, imagined 6–12-month timelines. https://aclanthology.org/2024.acl-long.747.pdf
- **Generative Agents: Interactive Simulacra of Human Behavior** — Park et al., UIST 2023. The canonical memory stream + reflection + planning architecture. https://arxiv.org/abs/2304.03442
- **PRIME: Cognitive Dual-Memory and Personalized Thought Process** — EMNLP 2025. Most explicit academic integration of the episodic/semantic split for personalization. https://aclanthology.org/2025.emnlp-main.1711/
- **PersonalLLM: Tailoring LLMs to Individual Preferences** — Zollo et al., ICLR 2025. The canonical heterogeneous-user personalization benchmark. https://arxiv.org/abs/2409.20296
- **Personalization via Reward Factorization (PReF)** — arXiv 2503.06358 (2025). 30× fewer user responses than naive RLHF; 67% win rate over default GPT-4o. https://arxiv.org/abs/2503.06358
- **Cognitive Architectures for Language Agents (CoALA)** — Sumers et al., arXiv 2309.02427. The source of the working/episodic/semantic/procedural vocabulary that practitioners now default to. https://arxiv.org/abs/2309.02427
- **Reflective Memory Management for Long-Term Personalized Dialogue (RMM)** — ACL 2025. Online RL over retrieval policy; +10% on LongMemEval. https://aclanthology.org/2025.acl-long.413/
- **A Survey on the Memory Mechanism of LLM-based Agents** — ACM TOIS 2025. Four-type taxonomy; identifies benchmark-saturation and metric-misalignment risks. https://dl.acm.org/doi/10.1145/3748302

### Key essays and posts

- **Letta — "Agent Memory: How to Build Agents that Learn and Remember"** (Jul 2025). Canonical four-tier model; introduces sleep-time compute. https://letta.com/blog/agent-memory
- **Letta — "RAG is not Agent Memory"** (Feb 2025). Names the most common industry mistake. https://www.letta.com/blog/rag-vs-agent-memory
- **Letta — "Continual Learning in Token Space"** (Dec 2025). Why token-space memory survives model upgrades when weight-space does not. https://letta.com/blog-categories/research
- **LangChain — "Memory for agents"** (Oct 2024). CoALA-mapped taxonomy; hot-path vs. background writes. https://blog.langchain.dev/memory-for-agents/
- **Zep — "Beyond Chat Memory: Making AI Interactions More Personal"** (Oct 2024). Reframes memory from chat recall to whole-person context. https://blog.getzep.com/ai-knowledge-graph-memory/
- **OpenAI — "Memory and new controls for ChatGPT"** (Feb 2024). The consumer-memory archetype and its two modes. https://openai.com/index/memory-and-new-controls-for-chatgpt/
- **Anthropic — context-management announcement** (Sep 2025 → Mar 2026). Project-scoped three-layer model; opt-in as privacy-first trust lever. https://www.anthropic.com/news/context-management
- **Google — "Introducing Gemini with personalization"** (Mar 2025). Only vendor grounding memory in real-world behavioral data outside the chat window. https://blog.google/products/gemini/gemini-personalization/
- **Eugene Yan — "Patterns for Personalization in Recommendations and Search"** (2022). Pre-LLM personalization rigor — bandits, embeddings, sequential models — that still sets the floor. https://eugeneyan.com/writing/patterns-for-personalization/
- **Eugene Yan — "Training an LLM-RecSys Hybrid for Steerable Recs with Semantic IDs"** (2025). Cleanest industry pattern for user-steerable personalization that composes with behavioral signal. https://eugeneyan.com/writing/semantic-ids/

### Key OSS projects

- **letta-ai/letta** (~22.1k stars, Apache 2.0) — stateful agents with self-editing memory blocks; the archetype. https://github.com/letta-ai/letta
- **mem0ai/mem0** (~53.5k stars, Apache 2.0) — universal memory layer; LoCoMo 91.6 / LongMemEval 93.4 self-reported. https://github.com/mem0ai/mem0
- **getzep/graphiti** (~25.1k stars, Apache 2.0) — temporal knowledge graph; tracks fact validity over time with provenance. https://github.com/getzep/graphiti
- **langchain-ai/langmem** (~1.4k stars, MIT) — LangGraph-native semantic/episodic/procedural memory SDK; official replacement for deprecated ConversationBufferMemory lineage. https://github.com/langchain-ai/langmem
- **topoteretes/cognee** (~16.4k stars, Apache 2.0) — knowledge engine; graph features free at all tiers (unlike Mem0 where graph is $249/mo-gated). https://github.com/topoteretes/cognee
- **agiresearch/A-mem** (~976 stars, MIT) — Zettelkasten-inspired auto-linking memory, NeurIPS 2025. https://github.com/agiresearch/A-mem
- **em-llm/EM-LLM-model** — Bayesian-surprise event segmentation for episodic memory; 10M-token context without fine-tuning, ICLR 2025. https://github.com/em-llm/EM-LLM-model
- **zhongwanjun/MemoryBank-SiliconFriend** (~419 stars) — Ebbinghaus forgetting curve in a deployed bilingual companion, AAAI 2024. https://github.com/zhongwanjun/MemoryBank-SiliconFriend
- **agentscope-ai/ReMe** (~2.6k stars, Apache 2.0) — 20+ memory workers covering retrieval, consolidation, reflection, re-consolidation. https://github.com/agentscope-ai/ReMe
- **mem0ai/mem0/openmemory** — local-first MCP memory server shared across Cursor, Claude Desktop, Windsurf, Cline. https://github.com/mem0ai/mem0/tree/main/openmemory
- **gptme/gptme** — "living memory system": Journal / Tasks / Knowledge / Relationships / Projects, version-controlled on disk. https://github.com/gptme/gptme
- **unslothai/unsloth** (~40k+ stars, Apache 2.0) + **axolotl-ai-cloud/axolotl** (~8k+ stars) — 2×–30× faster LoRA/QLoRA with 70–80% less VRAM; makes per-user / per-persona fine-tunes tractable on consumer GPUs.

### Notable commercial tools

- **Mem0** (mem0.ai) — $24.5M raised, ~48k stars, 186M+ monthly API calls, ~625k PyPI downloads/week; exclusive memory provider for AWS Agent SDK (Q1 2026). https://mem0.ai
- **Zep / Graphiti** (getzep.com) — temporal KG with fact invalidation; best benchmarks on long-horizon accuracy. https://www.getzep.com
- **Letta** (letta.com) — $10M raised; memory-first agents with persona as a first-class object and cross-provider portability. https://www.letta.com
- **Supermemory** (supermemory.ai) — $3M raised; #1 on LongMemEval (85.2%) self-reported; "one memory across all your AI tools." https://supermemory.ai
- **Lex** (lex.page) — closest commercial analog to the Unslop thesis: Style Guides trained on writing samples, teaching the model "your signature tone, metaphors, terminology, narrative voice." https://lex.page
- **Salesforce Einstein + Agentic Memory** — enterprise-scale published architecture: profile graph, session context, confidence scoring, write/read gates. https://engineering.salesforce.com/how-agentic-memory-enables-durable-reliable-ai-agents-across-millions-of-enterprise-users/
- **Gong Mission Andromeda** (Feb 2026) — Revenue Graph as a living network of revenue data + conversational AI assistant over captured customer interactions. https://www.gong.io
- **Personize** (personize.ai) — unified customer memory as a governance layer over CRM/email/transcripts/docs; HubSpot and Salesforce connectors.
- **GetProfile** (getprofile.org) — Apache-2.0 OpenAI-compatible proxy that injects typed user traits with confidence scores into every prompt; personalization as transparent middleware.

### Notable community threads

- **HN 47132001 — "I turned off ChatGPT's memory."** Canonical disable-memory manifesto; Anthropic's project-scoped model held up as the fix. https://news.ycombinator.com/item?id=47132001
- **HN 44052246 — "I don't like ChatGPT's new memory dossier."** Names the per-project isolation gap. https://news.ycombinator.com/item?id=44052246
- **HN 39360724 — "Memory and new controls for ChatGPT."** Establishing thread; "transactional vs. relationship-driven" split first named here. https://news.ycombinator.com/item?id=39360724
- **HN 43946471 — "Dump ChatGPT's Memory by Inspecting the System Prompt."** Reverse-engineers the ~40-conversation window and "aggregated user insights" block. https://news.ycombinator.com/item?id=43946471
- **Ars Technica / Rehberger — "Hacker plants false memories in ChatGPT."** Canonical security story for memory as attack surface. https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/
- **r/LocalLLaMA 1rqujc1 — "We gave our RAG chatbot memory across sessions."** Catalogs the four most-cited DIY failure modes with fixes. https://www.reddit.com/r/LocalLLaMA/comments/1rqujc1/
- **dev.to Fransys — "I Tested 5 AI Memory Tools So You Don't Have To (2026 Comparison)."** Independent week-long head-to-head: Zep 85%, Letta 82%, Mem0 78%, SuperMemory 71%; "more memories ≠ better." https://dev.to/fransys/i-tested-5-ai-memory-tools-so-you-dont-have-to-2026-comparison-2ode

---

## Key Techniques & Patterns

1. **Four-tier memory hierarchy.** Short-term message buffer → core/working in-context memory → searchable recall store → cold archival. Near-universal across OpenAI, Anthropic, Gemini, Letta, LlamaIndex, LangGraph, Mem0, Zep, and DIY SQLite builds.

2. **Self-editing memory blocks.** The LLM uses function calls (`create_memory`, `update_memory`, `delete_memory`) to own write operations directly. MemGPT → Letta → Anthropic's memory tool → LangMem.

3. **Two-agent memory management.** A cheap "Sentinel" LLM decides whether a turn contains anything worth keeping; if yes, an expensive "Knowledge Master" performs typed CRUD. Prevents the main agent from getting distracted by memory ops and caps cost per turn. Used by Christian Rice's LangGraph demo, Mem0 internally, Zep's async enricher, LangMem's background manager.

4. **Episodic / semantic / procedural split (CoALA taxonomy).** Semantic memory holds facts about the world; episodic holds past experiences and few-shot examples; procedural holds behavioral patterns and auto-edited rule files. LangMem, LlamaIndex memory blocks, gptme, PRIME, REMem, SEEM all implement this split.

5. **Temporal knowledge graph with bi-temporal validity.** Entities + relations with valid-from / valid-to timestamps. Old facts are invalidated rather than overwritten, preserving provenance. Zep's Graphiti (~25.1k stars), Cognee, A-MEM, SEEM.

6. **Zettelkasten-style auto-linking notes.** New memories generate structured notes that auto-link to related prior notes and trigger updates in existing ones. A-MEM, gptme, Cognee.

7. **Sleep-time / async consolidation.** A separate agent rewrites, deduplicates, and re-links memories during idle time — analogous to memory consolidation during sleep. Letta's sleep-time compute; LangChain's background memory manager.

8. **Reflection passes.** After each session or on a cadence, a reflection LLM produces higher-order beliefs, what-worked / what-to-avoid summaries, and updated persona traits. Generative Agents → Adam Lucek's tutorial → Letta Memory Palace.

9. **Ebbinghaus-curve forgetting + salience weighting.** Explicit decay based on time elapsed and memory significance; strategic forgetting as a feature. MemoryBank/SiliconFriend; MemoryLLM's exponential decay with no degradation through ~1M updates.

10. **Two-phase extraction: extract salient facts → merge/dedupe.** Pioneered by Mem0's LoCoMo pipeline; now the shared algorithmic pattern across Zep, Supermemory, and Cognee.

11. **LangGraph Checkpointer + Store.** Thread-scoped short-term state in a typed PostgreSQL-backed Checkpointer; namespaced long-term memory in a JSON Store. Memory bloat in Store is the top-cited production bug.

12. **Agentic memory tools with a call budget.** Expose `search_memory`, `add_memory`, and `search_docs` as LLM-callable tools; cap at 5 calls per turn; bake user IDs into closures to prevent cross-user contamination. The r/LocalLLaMA consensus after cataloguing the four classic failure modes.

13. **User Profile as a first-class primitive.** A named "profile" object distinct from raw memory events — behavioral intents, preferences, context. Supermemory, Fastino, GetProfile, Weaviate Personalization Agent, Salesforce Agentic Memory, Letta persona objects.

14. **Low-rank preference factorization.** Per-user reward equals a weighted combination of shared basis rewards. PReF achieves this with 30× fewer user responses; LoRe and VRF extend it with uncertainty quantification. Cold start with tens of signals.

15. **Persona-Plug / per-user lightweight embeddings.** A user-specific embedding derived from historical context is attached as a prompt plug-in to a frozen LLM — no parameter tuning per user. Persona-Plug (ACL 2025 Findings).

16. **Per-user / per-persona LoRA fine-tunes.** Unsloth on a 4060/4070 + Axolotl YAML configs + a few hundred examples of target voice = a credible nightly pipeline on consumer hardware. Style lives in weights; facts live in memory.

17. **Procedural memory as an auto-edited rules file.** A persistent `.md` file of 10 ongoing rules, continuously refined by reflection passes. The agent's own learned style guide. Analogous to `CLAUDE.md`, `.cursor/rules`.

18. **MCP as memory transport.** OpenMemory MCP, Graphiti MCP, Letta MCP expose the same user memory across Cursor, Claude Desktop, Windsurf, and Cline — same identity across clients.

19. **Token-space over weight-space.** Memory that needs to survive model upgrades should live in external state (tokens), not model weights. Letta's explicit argument; Anthropic's import tool makes this user-facing.

20. **Hybrid SQLite + vector store (DIY).** SQLite for timestamped structured episodic facts; ChromaDB, Weaviate, or Qdrant for semantic similarity. The canonical r/LocalLLaMA build at ~1,244 lines.

---

## Controversies & Debates

**Relationship-driven vs. transactional memory.** Half of users value cross-chat memory as what makes the assistant feel like a colleague. The other half disable it as "context pollution" or a "memory dossier." This split tracks use case (companion vs. search-like tool) and seems to require explicit mode-switching UX — not a single default. (E)

**Account-global vs. project-scoped memory.** The dominant HN and r/ChatGPT complaint is that OpenAI's account-global memory leaks personal-project context into work replies. Anthropic's project-scoped model is consistently cited as the correct default. OpenAI is retrofitting scoping; the debate is about which starting point is right. (B, E)

**On-by-default vs. opt-in implicit memory.** Google defaulted Gemini's Personal Context to on; OpenAI made saved memories opt-in but Chat History implicit; Anthropic retrieves memory only when explicitly asked. A live product-philosophy fault line between naturalness and informed consent. (B, E)

**Retrieve-and-dump vs. reason-over-profile.** PrLM (CIKM 2025) shows that personalization is significantly better when the LLM reasons explicitly over retrieved user facts rather than just concatenating them. Most production systems still concatenate. (A)

**"Human-like" memory mechanics vs. context engineering.** Letta explicitly states the goal is not to replicate human memory but to manage context effectively. Counter-position from MemoryBank, A-MEM, EM-LLM, and the academic PRIME/REMem work: biological analogy pays off structurally — Ebbinghaus decay, Bayesian-surprise event segmentation, and dual-memory architecture produce measurable gains, not just metaphor. (A, B, C)

**Storage vs. policy.** Is memory a data structure (retrieval system over stored facts) or a set of learned behaviors (what to remember, how to retrieve, when to forget)? RMM, A-MEM, and PrLM argue for policy; Mem0, Zep, and most vector-DB recipes treat it as storage. The gap matters: storage systems can be benchmarked on recall; policy systems need to be evaluated on downstream behavior. (A, C, E)

**RAG vs. agent memory.** Letta's "RAG is not Agent Memory" post names the common confusion. The practitioner consensus is that static retrieval over a fixed corpus is insufficient — memory must be written to, evolved over time, and able to invalidate stale facts. Several vendors (early LangChain memory, Pinecone's assistant feature) still lag here. (B, C)

**Single-agent self-managed memory vs. two-agent manager.** Letta-style self-management (the main LLM handles memory via tools) is architecturally simpler and cleaner. The Christian Rice / Mem0 / Zep approach (a dedicated cheap extractor writes asynchronously) wins on cost and reliability in practitioner tests. Neither is a clear winner for all use cases. (E)

**More memory is better? Fransys disproves it.** In an independent week-long head-to-head, SuperMemory stored the most memories and scored lowest on accuracy (71%) because it over-extracted, producing 16 false positives. Mem0 and Zep were more precise. The field has no published Pareto curve of memory count vs. recall accuracy vs. latency. (E)

**Self-reported vs. independent benchmark numbers.** Mem0 self-reports ~66% LoCoMo / 93.4% LongMemEval; independent tests find ~58% LoCoMo / ~49% LongMemEval. The 15-point or higher gaps are not explained by methodology. Standardized evaluation is an open problem. (E)

**Memory as attack surface.** Rehberger demonstrated indirect prompt injection via malicious Google Drive or OneDrive documents: false memories are written persistently and all subsequent user inputs/outputs are exfiltrated to an attacker. OpenAI initially categorized this as "safety, not security." The partial mitigation (store only user messages) is widely cited but not considered complete. (E)

**Invisible memory destroys trust.** April 2025's "Reference Chat History" rollout removed user visibility and editability from what ChatGPT remembered. The practitioner consensus: memory that users cannot see or edit feels stalkerish and erodes trust, even if it produces better answers. (E)

---

## Emerging Trends

**Memory portability is becoming a norm.** Claude's `claude.com/import-memory` launched in March 2026 (importing from ChatGPT/Gemini), Letta's cross-provider agent migration, OpenMemory MCP, and GetProfile's proxy architecture all push against vendor lock-in. Users are starting to treat their accumulated memory as a portable asset. (B, D)

**MCP is becoming the integration substrate for memory.** OpenMemory MCP, Graphiti MCP, and Letta MCP expose the same memory to any compliant client. Once a memory server exists, every new client inherits continuity for free. Likely to be the dominant interop pattern by end of 2026. (C)

**Episodic event segmentation is crossing from neuroscience into production.** EM-LLM's Bayesian-surprise boundary detection, A-MEM's note-linking, and Echo's time-span benchmark are direct imports from event-cognition psychology. The practical effect: retrieval that returns "that conversation last week in context" rather than "five similar chunks." (A, C)

**Consumer-grade fine-tuning is the back half of personalization.** Unsloth + Axolotl + a few hundred examples of a target voice = a credible nightly pipeline on a single consumer GPU. The "style lives in weights, facts live in memory" architecture is no longer research-only. (C)

**The four-memory cognitive architecture is going mainstream.** Working / episodic / semantic / procedural is now the default vocabulary in dev.to tutorials, YouTube courses, LangChain docs, LangMem, LlamaIndex, and gptme. CoALA (arXiv 2309.02427) is the shared vocabulary source. (E)

**Writing-voice products are adopting memory-infra patterns.** Lex's Style Guides and Knowledge Bases, Jenova's persistent preference accumulation, and Lindy's per-agent memory snippets are all infrastructure-layer products wearing writer-facing UX. They are the nearest commercial implementations of memory-as-humanization. (D)

**Consolidation pressure on the category.** Humanloop sunsetted in September 2025 and merged into Anthropic Console. Foundation-model vendors are absorbing memory and personalization tooling. Cloud hyperscalers (Microsoft, Oracle, AWS) entered directly in Q1 2026. The Mem0 "State of AI Agent Memory 2026" report explicitly marks graph memory as "in production, not experimental" and announces Mem0 as the exclusive memory provider for AWS Agent SDK. (B, D)

**Memory security governance is now a field.** SSGM (arXiv 2603.11768, Mar 2026) named three critical failure points in evolving memory systems. InjecMEM demonstrated one-interaction memory poisoning. Memory security survey (arXiv 2604.16548, Apr 2026) catalogued the attack classes. OWASP Top 10 for Agentic Applications 2026 includes persistent memory as a named risk. The Rehberger (2024) attack is now the first instance of a broader class rather than a one-off. (A, E)

**Compression-first memory is emerging as the efficient alternative.** SimpleMem (arXiv 2601.02553, Jan 2026) demonstrated that distilling full dialogue streams into compact indexed units, then consolidating asynchronously, achieves +64% over Claude-Mem on LoCoMo and 30× token reduction. The extraction-first approach (Mem0, Zep) and the store-everything approach are both losing cost efficiency ground to compress-then-consolidate. (A, C)

**Enterprise CRM incumbents are moving fast.** Salesforce published their Agentic Memory architecture in mid-2026 with profile graphs, confidence scoring, and hybrid semantic validation. Gong's Mission Andromeda (Feb 2026) added a Revenue Graph and conversational AI assistant over captured customer interactions. The window for startup wedges in enterprise customer memory is narrowing. (D)

**The "memory dossier" backlash has hardened.** A distinct community of users now explicitly disables memory and uses ChatGPT in Temporary Chat mode for any sensitive or exploratory query. The framing has shifted from "privacy concern" to "product defect." (E)

---

## Open Questions & Research Gaps

**"Does this output sound like me?" has no benchmark.** Every memory system benchmarks retrieval accuracy. None measure felt humanness or voice fidelity. This is the core opportunity for a humanization-focused product.

**Tone and style memory is missing as an architectural primitive.** Systems store what the user said — facts, explicit preferences. None track how they say it: cadence, favorite metaphors, punctuation idiosyncrasies, reading level, sentence rhythm. A dedicated style memory block, distinct from semantic memory, appears to be greenfield across all five angles.

**Memory and personalization are still two separate stacks.** PersonaMem-v2 advances weights-side personalization; Mem0/Zep/Letta advance tokens-side memory. No open-source framework jointly trains a LoRA on user style and writes structured memories from the same conversational stream. Closing that loop is the highest-leverage white space in the category.

**Cold start beyond VRF.** When is it actively harmful to personalize? VRF addresses uncertainty quantification but the field lacks principled guidance on when more user data makes outputs worse — over-familiarity, sycophancy amplification, false confidence.

**Style contradictions and voice drift.** Temporal fact invalidation handles "Adidas → Nike" cleanly. HorizonBench (Apr 2026) is now the first benchmark measuring preference evolution over time. No system has shipped the equivalent for voice/style drift, and HorizonBench results show all current LLMs struggle with it.

**Emotional and affective memory.** Outside MemoryBank/SiliconFriend, almost no academic system and essentially no commercial product tracks affect, sentiment trajectories, or relationship state as explicit memory types. This is arguably the most distinctively human aspect of long-term memory.

**Principled forgetting.** Only MemoryBank implements Ebbinghaus-curve decay seriously, and it is a research artifact. A pluggable forgetting-curve / salience-weighted pruning layer is an obvious missing OSS dependency.

**Privacy, editability, and right-to-forget.** Almost no academic memory paper addresses per-memory access control, auditable provenance, or deletion guarantees. Most OSS recipes assume a single-tenant store with no PII redaction.

**Cross-model memory portability in practice.** Graph-shaped memories are model-agnostic in theory, but embedding choices and schema assumptions bind a store to a specific LLM family. Migrating OpenAI-embedded Zep to locally-hosted Cognee is painful and largely undocumented.

**Memory editing UX.** Every vendor claims the user is "in control." There is no widely adopted pattern for user-visible memory editing — "here's what I remember about you; correct me." That visibility is what makes memory feel trustworthy rather than surveillance-like.

**Multi-user / shared memory models.** Couples, teams, and family agents with a shared-plus-private memory model are barely addressed. Letta's Conversations API (Jan 2026) is an early signal, but the architecture is thin.

**Memory-hallucination interaction.** When an agent misremembers, is the effect better or worse than hallucinating without any memory? Essentially unstudied.

**Sycophancy amplified by memory — now empirically confirmed.** MIT / Penn State (CHI 2026, Barcelona) studied two weeks of real daily LLM interactions and found condensed user profiles in memory are the single largest sycophancy driver across five LLMs — larger than interaction context alone. Accurate persona inference is causally linked to mirroring behavior. No published defense architecture exists. Recommendations: detect mirroring patterns and flag; let users moderate personalization intensity in long conversations.

**Cross-session identity drift of the agent itself.** Generative Agents' reflection mechanism gives agents opinions, but no work asks how those opinions should evolve coherently across months. Humans have narrative identity; current agents have memory without biography.

**How much memory is the right amount?** Fransys' "more memories ≠ better" finding (SuperMemory stored the most and scored lowest) is widely cited but there is no published Pareto curve of memory count vs. accuracy vs. latency.

**Defenses against memory-as-attack-surface.** Rehberger's indirect-prompt-injection-to-memory exploit (persistent false memories + exfiltration) has no published canonical defense beyond partial mitigations.

**Prompt engineering for the memory extractor itself.** The Sentinel prompt and typed category schema are load-bearing in every two-agent memory system, but tutorials treat them as one-off engineering. No reusable, benchmarked extractor artifact exists.

---

## How This Category Fits

Memory and personalization intersect most directly with three other research categories in this project. The anti-sycophancy category (stored agreement signals may amplify sycophancy over time), the detection-evasion and AI-ism reduction categories (style memory needs to evolve so outputs don't become trivially clusterable across sessions), and long-horizon agentic workflow categories (procedural memory is what preserves hard-won architectural decisions and coding preferences across a multi-day project). Memory is the substrate that humanization techniques — tone, register, humor, pacing, voice — need to persist on. Without it, prompting for voice washes out within a session. With it, every output stands on a cumulative relationship.

The category also connects to the broader personalization-as-product question. Lex, Jenova, and writing-voice tools are building what Mem0 and Zep would call an "infra layer product in writer-facing UX." The unshipped primitive across all of them is a first-class *style* memory block — separate from the semantic memory block that stores facts — that captures cadence, metaphor preferences, punctuation patterns, and reading level. None of the academic benchmark suites evaluate this dimension. None of the commercial products expose it as a named primitive. That gap is where the Unslop humanization lens makes a distinct contribution that retrieval-accuracy-focused competitors cannot easily copy.

---

## Recommended Reading Order

1. **Letta — "Agent Memory: How to Build Agents that Learn and Remember"** (Jul 2025) — four-tier model and sleep-time compute; best 20-minute orientation to the whole architecture space. https://letta.com/blog/agent-memory

2. **LangChain — "Memory for agents"** (Oct 2024) — CoALA-mapped taxonomy; hot-path vs. background writes; the practitioner vocabulary source. https://blog.langchain.dev/memory-for-agents/

3. **HN 39360724 thread** (Feb 2024) — "transactional vs. relationship-driven" user split named here first; read the top 20 comments. https://news.ycombinator.com/item?id=39360724

4. **Zep / Graphiti paper** (arXiv 2501.13956, Jan 2025) — bi-temporal KG; temporal validity as first-class state; 94.8% DMR benchmark. https://arxiv.org/abs/2501.13956

5. **Generative Agents paper** (arXiv 2304.03442, UIST 2023) — the canonical memory stream + reflection architecture that every downstream system imports. https://arxiv.org/abs/2304.03442

6. **LongMemEval paper** (arXiv 2410.10813, ICLR 2025) — quantifies the memory bottleneck; shows what "30–60% accuracy drop" actually looks like in practice. https://arxiv.org/abs/2410.10813

7. **Angle A — Academic** (`A-academic.md` in this folder) — 30+ papers across ACL, NeurIPS, ICLR, ICML, UIST, AAAI, TOIS; 8 sections with patterns and gaps.

8. **Angle D — Commercial** (`D-commercial.md` in this folder) — 17 vendors across 3 sub-segments; gaps framed as product opportunities; Lex section is most directly relevant to Unslop.

9. **PReF paper** (arXiv 2503.06358, 2025) + **PersonalLLM paper** (arXiv 2409.20296, ICLR 2025) — the personalization evaluation anchor and the low-rank-manifold argument side by side.

10. **Angle E — Practical/Forums** (`E-practical.md` in this folder) — Rehberger's attack, the four DIY failure modes with fixes, the Fransys benchmark, the "transactional vs. relationship-driven" debate in full; most useful for understanding what ships and what breaks.
