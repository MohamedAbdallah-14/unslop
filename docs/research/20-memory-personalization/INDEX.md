# Category 20 — Memory & Personalization

**Project:** Unslop — Humanizing AI output and thinking
**Compiled:** 2026-04-19
**Angles:** A (Academic) · B (Industry) · C (Open-Source) · D (Commercial) · E (Practical/Forums)

---

## Scope

How persistent memory and user personalization turn a stateless LLM into an assistant that feels *continuous* — one that "knows who I am, remembers how I talk, and notices what I care about." Spans:

- **Memory architectures:** episodic / semantic / procedural memory, tiered stores, self-editing blocks, temporal knowledge graphs, and sleep-time consolidation.
- **Personalization:** preference modeling (P-RLHF, PReF/LoRe/VRF), style adaptation, lightweight per-user fine-tunes (LoRA/QLoRA), and user-profile primitives.
- **Benchmarks & evaluation:** LongMemEval, LoCoMo, LaMP/LongLaMP, PersonalLLM, DMR, BEAM — plus the measurable gap between factual recall and "felt humanness."
- **Productization:** Memory-as-a-Service vendors (Mem0, Zep, Letta, Supermemory, Cognee) and the consumer-facing memory UX wars across ChatGPT, Claude, and Gemini.
- **Practitioner reality:** what breaks (context pollution, memory bloat, prompt-injection via memory), what works (two-agent memory managers, Checkpointer + Store), and what users actually want (project-scoped, editable, portable memory).

Humanization relevance is explicit throughout: memory is the single biggest lever for making AI outputs stop feeling stateless, generic, and "averaged."

---

## Executive Summary

Memory and personalization have become **the** architectural frontier of the agent era, and the field has consolidated around a surprisingly consistent picture in the 18 months from late 2024 to April 2026.

**Architecturally, everyone is converging.** Tiered memory (short-term buffer → core/working → recall → archival) is now table stakes — OpenAI, Anthropic, Google, Letta, LlamaIndex, LangGraph, Mem0 and Zep have all shipped variants. Within that tiering, four structural moves are winning:

1. **Self-editing memory blocks** (MemGPT → Letta → Anthropic's memory tool) — the LLM owns write operations.
2. **Temporal knowledge graphs over flat vector stores** (Zep's Graphiti, Cognee, A-MEM) — because humans know "Alice got married *last year*" supersedes "Alice is single," and naive RAG cannot.
3. **Two-agent memory management** (Christian Rice's Sentinel + Knowledge Master, Mem0's extractor, Zep's async enricher) — a cheap filter gates an expensive, typed, CRUD-shaped extractor. Single-agent "let the LLM manage its own memory" is losing on cost and reliability.
4. **Asynchronous / sleep-time consolidation** (Letta, LangChain's "writing in the background") — memory work happens off the critical path so latency budgets survive.

**Personalization is collapsing onto low-rank preference manifolds.** PReF, LoRe, and VRF (2025–2026) independently arrive at the same inductive bias — per-user reward = weighted combination of a small set of shared basis rewards — which makes cold start tractable. Below the prompt layer, Unsloth + Axolotl have made per-user LoRA fine-tunes affordable on consumer GPUs, opening the door to "style lives in weights, facts live in memory."

**The episodic / semantic / procedural split is re-emerging as a first-class axis.** PRIME, REMem, SEEM, Echo, LangMem, LlamaIndex and gptme all now model these memory types separately — the same taxonomy psychologists use for human autobiographical memory. Systems that collapse everything into one vector store consistently lose on multi-session reasoning.

**Benchmarks have caught up with ambition.** LongMemEval, LoCoMo, PersonalLLM, LongLaMP and ALOE give the field measurable ground truth for long-horizon recall, temporal reasoning, preference heterogeneity, and implicit-preference inference. Current leaderboard shape: Zep ~63.8% LongMemEval / 94.8% DMR, Mem0 ~49% LongMemEval but far cheaper/faster, Letta strong on architecture but "not production-ready."

**Commercially, memory is now its own category.** Mem0 ($24M, YC), Zep, Letta ($10M), Supermemory ($3M), Cognee ($7.5M), Personize, Fastino, and GetProfile all ship "drop-in memory layer" APIs — and are starting to be commoditized by foundation-model vendors shipping native memory (ChatGPT, Claude, Gemini). Writing-voice products (Lex, Jenova) are the closest commercial analogs to the Unslop thesis and explicitly sell "your signature tone, metaphors, terminology, narrative voice."

**Users are split.** Half want "relationship-driven" memory that makes the assistant feel like a colleague; the other half disable memory as "context pollution" or a "memory dossier." The dominant usability complaint — across r/ChatGPT, HN, and r/LangChain — is that memory is *account-global* when it should be *project-scoped*, and *invisible* when it should be editable. Anthropic's project-scoped approach is held up as the model to beat.

**Security and UX gaps are real.** Rehberger's indirect-prompt-injection-to-memory attack is now the canonical threat model; no one has a clean defense. Memory editing UX is underdeveloped; forgetting is treated as a bug, not a feature; portability across vendors barely exists; and — most pointedly for this project — no benchmark measures whether memory makes an assistant *feel more like a person who knows you*.

That last gap is the core Unslop opportunity: to treat memory not just as retrieval infrastructure, but as a humanization mechanism whose quality metric is *"does this reply sound like it came from someone who remembers me?"*

---

## Cross-Angle Themes

1. **Tiered memory has won — every angle confirms it.** Academic (MemGPT, MemoryLLM), industry (OpenAI/Anthropic/Gemini/Letta), OSS (Letta, LlamaIndex blocks, LangGraph Checkpointer+Store), commercial (Mem0 multi-level, Zep temporal tiers), practitioner (DIY SQLite+Chroma with short/working/long). The vocabulary varies, the shape does not.

2. **Episodic ↔ semantic ↔ procedural is the shared taxonomy.** Academic (PRIME, REMem, SEEM, Echo), industry (LangChain's CoALA-based post), OSS (LangMem, gptme's Journal/Knowledge/Relationships, LlamaIndex), practitioner (Adam Lucek's "four-memory cognitive architecture"). Commercial vendors are starting to ship this distinction too (Zep episodes vs. graph facts, Supermemory User Profile vs. Memory Graph).

3. **Temporal reasoning is the new recall.** Academic (Zep paper, Echo, LongMemEval's "knowledge updates" category), industry (Zep Graphiti, Anthropic project-scoping), OSS (Graphiti, MemoryBank's Ebbinghaus decay), commercial (Zep's "Robbie switched from Adidas to Nike" fact-invalidation demo). "Did we remember it?" has shifted to "do we know it's still true?"

4. **Memory is moving from storage to policy.** Academic (RMM learns retrieval online; A-MEM evolves memories at write time; PrLM trains reasoning over retrieved profiles). OSS (MemoryScope/ReMe's consolidation/reflection stages; Mem0's single-pass ADD-only extraction). Practitioner (agentic memory tools: `search_memory`, `add_memory`, with a 5-call budget). What to remember, how to retrieve, when to update are all *learned behaviors*, not fixed pipelines.

5. **Forgetting is finally a feature.** MemoryBank's Ebbinghaus curve, MemoryLLM's exponential decay, MemoRAG's KV compression, and the TOIS survey's explicit "forgetting" operation treat controlled forgetting as a design goal. Practitioners routinely hit the opposite problem — hoarding, bloat, "memory dossier" — and have no canonical library to reach for.

6. **Personalization is converging on low-rank preference manifolds + implicit signal.** Academic (PReF, LoRe, VRF, ALOE). Commercial (Supermemory/Fastino/GetProfile's "User Profile" primitive). OSS (PersonaMem-v2's 1,000-persona / 20k-preference benchmark, Persona-Plug as a per-user adapter). Cold start is solvable with tens, not thousands, of signals.

7. **Memory portability is the emerging trust lever.** Letta's "continual learning in token space," Anthropic's `claude.com/import-memory`, OpenMemory MCP, agent-file formats, GetProfile as an OpenAI-compatible proxy. Users are starting to expect their memory to be *an asset they can move*, not a platform lock-in — and vendors are positioning around it.

8. **Two-agent memory is the new default.** Industry (Letta's sleep-time compute), OSS (LangMem background memory manager, MemoryScope's consolidation worker), practitioner (Christian Rice's Sentinel + Knowledge Master, Mem0's extractor, Zep's async enricher). The main conversational agent does *not* manage its own memory inline.

9. **Infra cost is a first-class axis.** Character.AI's KV-cache engineering (95% hit on 180-message-average chats), Mem0's p95 latency + 80% token reduction, HippoRAG's 10–20× cost wins. Humanized long dialogues have an economics problem, not just a prompting problem.

10. **The "feels human" metric is the shared blind spot.** All angles — academic, industry, OSS, commercial, practitioner — benchmark retrieval accuracy. None benchmark "does this output read as authored by someone who knows me." This is the explicit greenfield for a humanization-focused product.

---

## Top Sources (Curated)

### Must-read papers

1. **MemGPT: Towards LLMs as Operating Systems** — Packer et al., arXiv 2310.08560 (2023). The substrate every later system assumes. https://arxiv.org/abs/2310.08560
2. **Zep: A Temporal Knowledge Graph Architecture for Agent Memory** — Rasmussen et al., arXiv 2501.13956 (2025). 94.8% DMR, −90% latency; temporal validity as first-class state. https://arxiv.org/abs/2501.13956
3. **A-MEM: Agentic Memory for LLM Agents** — Xu et al., NeurIPS 2025. Zettelkasten-style memory that evolves at write time. https://arxiv.org/abs/2502.12110
4. **Mem0: Production-Ready Long-Term Memory** — Chhikara et al., arXiv 2504.19413 (2025). +26% vs. OpenAI memory, −91% p95 latency, >90% token savings. https://arxiv.org/abs/2504.19413
5. **HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs** — Gutiérrez et al., NeurIPS 2024. Biological motivation + 10–20× cost wins on multi-hop QA. https://arxiv.org/abs/2405.14831
6. **LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory** — Wu et al., ICLR 2025. The benchmark that made the memory bottleneck measurable. https://arxiv.org/abs/2410.10813
7. **LoCoMo: Evaluating Very Long-Term Conversational Memory** — Maharana et al., ACL 2024. 300–600-turn imagined 6–12-month dialogues. https://aclanthology.org/2024.acl-long.747.pdf
8. **Generative Agents: Interactive Simulacra of Human Behavior** — Park et al., UIST 2023. The canonical memory-stream + reflection architecture. https://arxiv.org/abs/2304.03442
9. **PRIME: Cognitive Dual-Memory and Personalized Thought Process** — EMNLP 2025. Most explicit integration of episodic/semantic split *for personalization*. https://aclanthology.org/2025.emnlp-main.1711/
10. **PersonalLLM: Tailoring LLMs to Individual Preferences** — Zollo et al., ICLR 2025. Canonical personalization benchmark with heterogeneous users. https://arxiv.org/abs/2409.20296
11. **Personalization via Reward Factorization (PReF)** — arXiv 2503.06358 (2025). 30× fewer user responses; 67% win-rate over GPT-4o. https://arxiv.org/abs/2503.06358
12. **Cognitive Architectures for Language Agents (CoALA)** — Sumers et al., arXiv 2309.02427. Source of the working/episodic/semantic/procedural vocabulary practitioners now default to. https://arxiv.org/abs/2309.02427
13. **Reflective Memory Management for Long-Term Personalized Dialogue** — ACL 2025. Online-RL over retrieval policy; +10% LongMemEval. https://aclanthology.org/2025.acl-long.413/
14. **A Survey on the Memory Mechanism of LLM-based Agents** — ACM TOIS 2025. Best current orientation map. https://dl.acm.org/doi/10.1145/3748302
15. **EM-LLM** — ICLR 2025. Bayesian-surprise event segmentation; 10M-token context with no fine-tuning. https://arxiv.org/abs/2407.09450

### Must-read posts/essays

1. **Letta — "Agent Memory: How to Build Agents that Learn and Remember"** (Jul 2025). Canonical four-tier model + sleep-time compute. https://letta.com/blog/agent-memory
2. **Letta — "RAG is not Agent Memory"** (Feb 2025). Names the most common industry mistake. https://www.letta.com/blog/rag-vs-agent-memory
3. **Letta — "Continual Learning in Token Space"** (Dec 2025). Why token-space memory survives model upgrades. https://letta.com
4. **LangChain — "Memory for agents"** (Oct 2024). CoALA-mapped taxonomy; hot-path vs. background writes. https://blog.langchain.dev/memory-for-agents/
5. **Zep — "Beyond Chat Memory: Making AI Interactions More Personal"** (Oct 2024). Reframes memory from chat recall to whole-person context. https://blog.getzep.com/ai-knowledge-graph-memory/
6. **OpenAI — "Memory and new controls for ChatGPT"** (Feb 2024). The consumer-memory archetype. https://openai.com/index/memory-and-new-controls-for-chatgpt/
7. **Anthropic — "Context management" / project-scoped memory** (Sep 2025 → Mar 2026). The privacy-first counter-position. https://www.anthropic.com/news/context-management
8. **Google — "Introducing Gemini with personalization"** (Mar 2025). The only vendor grounding memory in real-world behavior outside chat. https://blog.google/products/gemini/gemini-personalization/
9. **Eugene Yan — "Patterns for Personalization in Recommendations and Search"** (2022). Pre-LLM personalization rigor that still sets the floor. https://eugeneyan.com/writing/patterns-for-personalization/
10. **Eugene Yan — "Training an LLM-RecSys Hybrid for Steerable Recs with Semantic IDs"** (2025). Cleanest pattern for steerable personalization. https://eugeneyan.com/writing/semantic-ids/
11. **Character.AI — "Optimizing AI Inference"** (2024). Humanized long dialogues have an infra-cost problem. https://blog.character.ai/optimizing-ai-inference-at-character-ai-2/
12. **Salesforce Engineering — "Agentic Memory"** (2026). Reference architecture for enterprise customer memory. https://engineering.salesforce.com/how-agentic-memory-enables-durable-reliable-ai-agents-across-millions-of-enterprise-users/

### Key open-source projects

1. **Letta (ex-MemGPT)** — `letta-ai/letta`. Stateful agents with self-editing memory blocks. The archetype. https://github.com/letta-ai/letta
2. **Mem0** — `mem0ai/mem0`. ~53.5k stars. Universal memory layer; LoCoMo 91.6 / LongMemEval 93.4 self-reported. https://github.com/mem0ai/mem0
3. **Graphiti (Zep)** — `getzep/graphiti`. Temporal knowledge graph; tracks fact validity over time. https://github.com/getzep/graphiti
4. **LangMem** — `langchain-ai/langmem`. LangGraph-native semantic/episodic/procedural memory SDK. https://github.com/langchain-ai/langmem
5. **Cognee** — `topoteretes/cognee`. Knowledge engine + ontology grounding + multi-tenant isolation. https://github.com/topoteretes/cognee
6. **A-MEM** — `agiresearch/A-mem`. Zettelkasten-inspired auto-linking memory. https://github.com/agiresearch/A-mem
7. **EM-LLM** — `em-llm/EM-LLM-model`. Bayesian-surprise event segmentation for episodic memory. https://github.com/em-llm/EM-LLM-model
8. **MemoryBank / SiliconFriend** — `zhongwanjun/MemoryBank-SiliconFriend`. Ebbinghaus-curve forgetting in a deployed companion. https://github.com/zhongwanjun/MemoryBank-SiliconFriend
9. **MemoryScope / ReMe** — `agentscope-ai/ReMe`. 20+ memory workers across retrieve/consolidate/reflect. https://github.com/agentscope-ai/ReMe
10. **OpenMemory MCP** — `mem0ai/mem0/openmemory`. Local-first, MCP-shared memory across Cursor / Claude / Windsurf. https://github.com/mem0ai/mem0/tree/main/openmemory
11. **gptme** — `gptme/gptme`. "Living memory systems": Journal / Tasks / Knowledge / Relationships / Projects. https://github.com/gptme/gptme
12. **Unsloth** + **Axolotl** — `unslothai/unsloth` / `axolotl-ai-cloud/axolotl`. Make per-user / per-persona LoRA fine-tunes tractable on consumer GPUs. https://github.com/unslothai/unsloth

### Notable commercial tools

1. **Mem0** (mem0.ai) — $24M raised, ~50k stars, 186M+ monthly API calls. The category leader on setup speed and ecosystem. https://mem0.ai
2. **Zep / Graphiti** (getzep.com) — Temporal KG + fact invalidation; best benchmarks on long-horizon accuracy. https://www.getzep.com
3. **Letta** (letta.com) — Memory-first agents, cross-provider portable memory, persona as first-class object. https://www.letta.com
4. **Supermemory** (supermemory.ai) — "One memory across all your AI tools" + consumer app. https://supermemory.ai
5. **Cognee** (cognee.ai) — KG + vector + ontology; graph features free at all tiers. https://www.cognee.ai
6. **Lex** (lex.page) — **Closest commercial analog to Unslop.** Style Guides trained on your writing samples: "teaching Lex to match your signature tone, metaphors, terminology, narrative voice." https://lex.page
7. **Salesforce Einstein + Agentic Memory** — Enterprise-scale published architecture for profile-graph-linked memory. https://engineering.salesforce.com
8. **Gong Mission Andromeda** (Feb 2026) — Revenue Graph + conversational AI Assistant over captured customer interactions. https://www.gong.io
9. **Personize** (personize.ai) — Unified customer memory as a governance layer over CRM / email / docs. https://personize.ai
10. **GetProfile** (getprofile.org) — Apache-2.0 OpenAI-compatible proxy that injects typed user traits with confidence scores. https://www.getprofile.org
11. **Weaviate Personalization Agent** — Vector-DB-native "personas" + interaction logs with NL explanations. https://weaviate.io/product/personalization-agent
12. **ChatGPT / Claude / Gemini native memory** — The consumer baseline every startup is measured against.

### Notable community threads

1. **HN 47132001 — "I turned off ChatGPT's memory."** Canonical disable-memory manifesto; Anthropic project-scoping held up as the fix. https://news.ycombinator.com/item?id=47132001
2. **HN 44052246 — "I don't like ChatGPT's new memory dossier."** Names the per-project isolation gap. https://news.ycombinator.com/item?id=44052246
3. **HN 39360724 — "Memory and new controls for ChatGPT."** Establishing thread; the "transactional vs. relationship-driven" split was named here first. https://news.ycombinator.com/item?id=39360724
4. **HN 43946471 — "Dump ChatGPT's Memory and Chat History by Inspecting the System Prompt."** Reverse-engineers the ~40-conversation window + "aggregated user insights" block. https://news.ycombinator.com/item?id=43946471
5. **Ars Technica / Rehberger — "Hacker plants false memories in ChatGPT."** Canonical security story for memory-as-attack-surface. https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/
6. **r/LocalLLaMA 1rqujc1 — "We gave our RAG chatbot memory across sessions — here's what broke first."** The four most-cited DIY failure modes, with fixes. https://www.reddit.com/r/LocalLLaMA/comments/1rqujc1/
7. **r/LangChain 1rpnxmx — "how you guys are dealing with the long running agents??"** Consensus Checkpointer + Store pattern. https://www.reddit.com/r/LangChain/comments/1rpnxmx/
8. **dev.to Fransys — "I Tested 5 AI Memory Tools So You Don't Have To (2026 Comparison)."** Independent head-to-head: Zep 85%, Letta 82%, Mem0 78%, SuperMemory 71% — with the canonical "more memories ≠ better" finding. https://dev.to/fransys/i-tested-5-ai-memory-tools-so-you-dont-have-to-2026-comparison-2ode
9. **YouTube — Christian Rice, "Build an Agent with Long-Term, Personalized Memory."** The reference two-agent (Sentinel + Knowledge Master) LangGraph implementation. https://www.youtube.com/watch?v=oPCKB9MUP6c
10. **YouTube — Adam Lucek, "Building Brain-Like Memory for AI."** The four-memory cognitive-architecture tutorial that brought CoALA into mainstream practice. https://www.youtube.com/watch?v=VKPngyO0iKg

---

## Key Techniques & Patterns

- **Tiered memory (short-term / working / long-term / archival).** Universal across OpenAI, Anthropic, Gemini, Letta, LlamaIndex, LangGraph, Mem0, Zep, and DIY SQLite+Chroma builds. The vocabulary varies; the four-tier shape is near-universal.
- **Self-editing memory blocks.** LLM uses function calls (`create_memory`, `update_memory`, `delete_memory`) to own write operations. MemGPT → Letta → Anthropic's memory tool → LangMem.
- **Two-agent memory management.** Cheap "Sentinel" LLM gates an expensive, typed extractor that performs CRUD on memory. Used by Christian Rice's LangGraph demo, Mem0 internally, Zep's async enrichment, LangMem's background manager, MemoryScope/ReMe.
- **Episodic ↔ semantic ↔ procedural split (CoALA taxonomy).** Facts about the world in semantic memory; past experiences / few-shots in episodic; behavioral patterns / auto-edited rule files in procedural. LangMem, LlamaIndex, gptme, PRIME, REMem, SEEM all ship this split.
- **Temporal knowledge graph with bi-temporal validity.** Entities + relations + valid-from / valid-to timestamps. Old facts are invalidated, not overwritten. Zep's Graphiti, Cognee, A-MEM, SEEM.
- **Zettelkasten-style auto-linking notes.** New memories generate structured notes and auto-link to related prior notes, triggering updates in the old ones. A-MEM, gptme, Cognee.
- **Sleep-time / async consolidation.** A separate agent rewrites, deduplicates, and re-links memory during idle time. Letta's sleep-time compute; LangChain's "writing in the background."
- **Reflection passes.** After each session (or on a cadence), a reflection LLM produces higher-order beliefs, "what worked / what to avoid," updated persona traits. Generative Agents → Adam Lucek's tutorial → Letta's Memory Palace.
- **Ebbinghaus-curve forgetting + salience weighting.** Explicit decay based on time + importance; strategic forgetting as a feature. MemoryBank/SiliconFriend; MemoryLLM's exponential decay.
- **LangGraph Checkpointer + Store.** Thread-scoped short-term state (typed schema, PostgreSQL) + namespaced long-term memory (JSON). The production default for LangGraph agents.
- **Agentic memory tools with a call budget.** Expose `search_memory` / `add_memory` / `search_docs` as tools; cap at 5 calls/turn; bake user-IDs into closures. The r/LocalLLaMA consensus.
- **Two-phase extraction: extract → merge/dedupe.** Pioneered by Mem0's LoCoMo pipeline; now the shared algorithmic pattern across Zep, Supermemory, Cognee.
- **User Profile as a first-class primitive.** Distinct from raw memory events. Supermemory, Fastino, GetProfile, Weaviate Personalization Agent, Salesforce Agentic Memory, Letta persona objects.
- **Low-rank preference factorization.** Per-user reward = weighted combination of shared basis rewards. PReF, LoRe, VRF. Tens of user signals sufficient.
- **Persona-Plug / per-user embeddings.** Lightweight user-specific embedding from history, attached to a frozen LLM — cheapest plausible personalization.
- **Per-user / per-persona LoRA fine-tunes.** Unsloth + Axolotl + a few hundred examples of target voice = nightly pipeline on consumer GPUs.
- **Hybrid: SQLite for structured episodic facts + vector DB for semantic similarity.** The canonical r/LocalLLaMA DIY architecture.
- **Explicit `bio` / "Remember that…" triggers.** User-visible primitive for writing memory; more reliable than hoping extractor catches it implicitly.
- **Custom Instructions vs. Memory division of labor.** Permanent identity in Custom Instructions (~1,500-word cap); evolving detail in Memory. Community-tested pattern.
- **Temporary / project-scoped chat as escape hatch.** No memory read/write for sensitive queries; ChatGPT's Temporary Chat, Anthropic's Projects.
- **Procedural memory as an auto-edited rules file.** `CLAUDE.md` / `.cursor/rules`-style persistent `.md` with 10 ongoing rules, refined by reflection passes.
- **Human-in-the-loop memory writes.** `interrupt()` before persistent memory-writes; user confirms; resume from checkpoint.
- **MCP as memory transport.** OpenMemory MCP, Graphiti MCP, Letta MCP. Same user memory across Cursor / Claude Desktop / Windsurf / Cline.
- **Token-space over weight-space.** Memory that survives model upgrades must live in tokens/external state, not weights. Letta's explicit argument; Anthropic's import tool.
- **Semantic IDs.** Hybrid LLM + recsys IDs for steerable personalization — users articulate taste in natural language that composes with behavioral signal.

---

## Controversies & Debates

1. **Relationship-driven vs. transactional memory.** Roughly half of users love cross-chat memory as "colleague feeling"; the other half disable it as "context pollution" or a "memory dossier." The split tracks intent (companion vs. tool) and is not resolved — likely needs explicit mode-switching UX.

2. **Account-global vs. project-scoped memory.** The dominant HN / r/ChatGPT complaint against OpenAI's approach. Anthropic's project-scoped model is held up as correct. OpenAI is retrofitting scoping; the war is over which default is right.

3. **On-by-default vs. opt-in implicit memory.** Google (on-by-default), OpenAI (opt-in saved / implicit chat history), Anthropic ("only when user asks"). A live product-philosophy fault line — natural UX vs. informed consent.

4. **Retrieve-and-dump vs. reason-over-profile.** PrLM (CIKM 2025) shows that personalization benefits from *explicit reasoning over* retrieved user facts, not just concatenation. Most production systems still concatenate.

5. **"Human-like" memory vs. "context engineering."** Letta's official stance: *"The goal isn't to replicate human memory mechanics but to create memory systems that enable agents to be genuinely helpful."* Counter-position from MemoryBank, A-MEM, EM-LLM, and academic PRIME/REMem: biological analogy pays off structurally (Ebbinghaus decay, event segmentation, dual-memory). The Unslop project has to pick a stance.

6. **Storage vs. policy.** Is memory a data structure (retrieval system) or a learned behavior (what to remember, how to retrieve, when to forget)? RMM, A-MEM, PrLM argue policy; Mem0, Zep, vector-DB recipes argue storage.

7. **RAG vs. agent memory.** Letta's "RAG is not Agent Memory" post names the common confusion. Consensus in the practitioner literature is now that static retrieval over a fixed corpus is insufficient; memory must be written to, evolved, and able to invalidate old facts. Some vendors (Pinecone, early LangChain memory) lag.

8. **Single-agent self-managed memory vs. two-agent manager.** Letta-style ("the main LLM manages its own memory via tools") vs. Christian Rice / Mem0 / Zep ("separate cheap extractor agent writes memory asynchronously"). Two-agent is winning on cost and reliability but single-agent is architecturally cleaner.

9. **More memory = better? (Fransys disproves it.)** SuperMemory stored the most memories and got the lowest accuracy. The field has no published Pareto curve of memory count vs. recall accuracy vs. latency.

10. **Self-reported vs. independent benchmarks.** Mem0 self-reports ~66% LoCoMo / 93.4% LongMemEval; independent tests show ~58% / 49%. The field's credibility hinges on standardizing evaluation.

11. **Memory as attack surface.** Rehberger's indirect-prompt-injection-to-memory attack persists across sessions and exfiltrates user data. OpenAI's "user messages only, not assistant outputs" is a partial mitigation. No one has published a full defense.

12. **Memory dossier vs. legibility.** April 2025's "Reference Chat History" rollout removed user visibility into what was remembered. The practitioner consensus is that *invisible memory destroys trust*, yet OpenAI chose it for UX simplicity.

---

## Emerging Trends

1. **Memory portability (2025 → 2026).** Claude's March 2026 `claude.com/import-memory` (from ChatGPT/Gemini), Letta's cross-provider agent migration, OpenMemory MCP, GetProfile's OpenAI-compatible proxy, agent file formats. Users expect to *own* their memory artifact.

2. **MCP as the integration substrate for memory.** Once a user's memory is exposed as an MCP server, every compliant client inherits it (Cursor, Claude Desktop, Windsurf, Cline). Expected to be the dominant interop pattern by end of 2026.

3. **Episodic event segmentation crossing from neuroscience into production.** EM-LLM's Bayesian surprise, A-MEM's note-linking, Echo's time-span benchmark. "Oh yeah, that conversation last week" instead of "here are 5 similar chunks."

4. **Consumer-grade fine-tuning as the back half of personalization.** Unsloth on a 4060/4070 + Axolotl YAML + a few hundred examples = credible nightly pipeline. Style lives in weights; facts live in memory.

5. **The four-memory cognitive architecture going mainstream.** Working / episodic / semantic / procedural is now the default vocabulary in dev.to, YouTube, LangChain docs, LangMem, LlamaIndex, gptme.

6. **Two-agent memory as default.** Cheap Sentinel + expensive Knowledge Master; user-facing agent never manages its own memory inline.

7. **Year-in-review as forced memory audit.** "Your Year with ChatGPT" (Dec 2025) became the most effective memory-audit UX the space has produced — users finally *saw* their aggregated insights. Expect more vendors to ship similar "memory wrapped."

8. **Writing-voice products adopting memory-infra patterns.** Lex's Style Guides + Knowledge Bases, Jenova's persistent preference accumulation. They are infra-layer products wearing writer-facing UX.

9. **Consolidation pressure on the category.** Humanloop sunsetted Sep 2025 and merged into Anthropic Console. Expect more personalization / eval tools to get absorbed into foundation-model vendors.

10. **Enterprise CRM incumbents moving fast.** Salesforce's published Agentic Memory architecture (mid-2026) + Gong Mission Andromeda (Feb 2026) compress the window for startup wedges in enterprise customer memory.

11. **Benchmark stratification.** LoCoMo, LongMemEval, PersonalLLM, LongLaMP, DMR, BEAM, ALOE are becoming the standard evaluation axes. "Does it work?" has shifted to "what does 85% accuracy mean for my use case?"

12. **Agentic / procedural memory via auto-edited rules files.** `CLAUDE.md`, `.cursor/rules`, gptme's Knowledge folder. The system's *own* learned style guide.

---

## Open Questions / Research Gaps

1. **"Does this output sound like me?" has no benchmark.** Every memory system benchmarks retrieval accuracy; none benchmark felt humanness or voice fidelity. This is the core Unslop wedge.

2. **Tone / style memory is missing as an architectural primitive.** Systems store *what* the user said (facts, preferences), not *how they say it* (cadence, favorite metaphors, punctuation idiosyncrasies, reading level). A dedicated **style memory block** — distinct from semantic memory — is greenfield.

3. **Memory and personalization are still two separate stacks.** PersonaMem-v2 advances weights-side personalization; Mem0/Zep/Letta advance tokens-side memory. **No open-source framework jointly trains a LoRA on user style AND writes structured memories from the same conversational stream.** Closing that loop is the highest-leverage white space.

4. **Cold start beyond VRF.** When is it worse than nothing to personalize? Most systems assume more user data is always better; VRF addresses uncertainty but the field lacks principled guidance.

5. **Style contradictions / voice drift.** Temporal fact invalidation handles "Adidas → Nike." Nobody has the equivalent for "voice last March vs. voice now" where the author legitimately evolves.

6. **Emotional / affective memory.** Outside MemoryBank/SiliconFriend, very few academic systems — and essentially no commercial ones — explicitly track affect, sentiment trajectories, or relationship state. Arguably the most distinctively human aspect of long-term memory.

7. **Principled forgetting.** Only MemoryBank implements decay seriously, and it is a research artifact. A pluggable forgetting-curve / salience-weighted pruning layer is an obvious missing dependency.

8. **Privacy / editability / right-to-forget.** Almost no academic paper addresses per-memory access control, auditable provenance, or deletion guarantees. Most OSS recipes assume a single-tenant store with no PII redaction.

9. **Cross-model / cross-vendor portability in practice.** Graph memories are model-agnostic in theory, but embeddings and schema choices bind stores to a specific LLM family. Migrating OpenAI-embedded Zep to locally-hosted Cognee is painful.

10. **Memory editing UX.** Every vendor claims the user is "in control," but there is no widely adopted pattern for **user-visible memory editing** ("here's what I remember — correct me"). That visibility is precisely what makes memory feel trustworthy rather than stalkerish.

11. **Multi-user / shared memory models.** Couple / team / family agents with shared + private memory are thin — Letta's Conversations API (Jan 2026) is an early signal.

12. **Memory-hallucination trade-off.** When the agent misremembers, is that worse or better than making it up fresh? Essentially unstudied.

13. **Sycophancy × memory.** If the agent remembers "user likes feature X," does that increase sycophantic agreement? Unstudied.

14. **Cross-session identity drift of the agent itself.** Generative Agents' reflection gives agents opinions; no work asks how those should evolve coherently across months. Humans have narrative identity; current agents have memory without biography.

15. **Multilingual / multicultural personalization.** SiliconFriend is bilingual; almost everything else is English-only. Unsolved academic problem with immediate product consequences.

16. **How much memory is the right amount?** Fransys' "more memories ≠ better" is widely cited but there is no published Pareto curve of memory count vs. accuracy vs. latency.

17. **Defenses against memory-as-attack-surface.** Rehberger's indirect-prompt-injection-to-memory has no published canonical defense.

18. **Reader/audience memory.** All products model one user. None model the reader / audience as a co-memory object — though writing humanness depends heavily on audience context.

19. **Interaction between memory and alignment.** If memory stores dispreferred behaviors (e.g., the user's tolerance for spicy humor), does it override base-model safety tuning? How?

20. **Prompt-engineering for the memory extractor itself.** The "Sentinel prompt" and category schema are load-bearing in production — but tutorials treat them as one-off engineering, not a reusable artifact.

---

## How This Category Fits in the Bigger Picture

Memory and personalization are the **single biggest lever** between "an LLM that sounds like every other LLM" and "an LLM that sounds like a specific human talking to a specific human they know." For the Unslop thesis that category matters for these reasons:

- **Generic = averaged.** As Lex puts it: *"Generic AI trained on the internet speaks in averages and optimizes for what's most likely, stripping unique voice."* Without memory + personalization, humanization collapses to prompt tricks that wash out within a session. With them, every output gets to stand on a cumulative relationship.

- **Memory is the substrate humanization techniques (tone, register, humor, pacing) live on.** Prompting for voice is necessary but insufficient — it has nowhere to persist, no way to evolve, and no way to survive model upgrades. Token-space memory (Letta) is what makes a humanized assistant's *identity* portable across model generations.

- **Personalization is the cold-start bridge.** PReF / LoRe / VRF make it tractable to locate a new user in preference space with tens — not thousands — of signals. Combined with Persona-Plug-style per-user adapters or consumer-grade LoRA fine-tunes, this is the path from "humanized defaults" to "humanized *for you*" without per-user training cost.

- **Temporal reasoning is where AI most often fails to feel human.** Knowing "Alice got married *last year*" supersedes "Alice is single" is table stakes for human-feeling recall. Zep's bi-temporal KG and LongMemEval's "knowledge updates" category make this measurable.

- **The humanization blind spot in memory evaluation is the Unslop wedge.** All five angles converge on the same observation: current benchmarks measure factual recall, not whether the output *reads* as coming from someone who knows you. That gap is precisely what this project can fill — and where it can differentiate from Mem0 / Zep / Letta / Supermemory, all of whom compete on benchmark numbers the Unslop target audience doesn't care about.

- **Style memory is the unshipped primitive.** Every vendor has a semantic memory block. None has a first-class *style* memory block — cadence, favorite metaphors, running jokes, punctuation idiosyncrasies. This is both a product opportunity and the cleanest humanization-native research contribution.

- **Humanization connects to other Unslop categories through memory.** Anti-sycophancy work becomes harder and more important when memory stores past agreement signals. Detection-evasion humanization needs style memory to evolve so outputs don't become trivially clusterable over time. Long-horizon agentic workflows (coding, research) need procedural memory to preserve hard-won context.

---

## Recommended Reading Order

**If you have 30 minutes (orientation):**
1. Letta — "Agent Memory" (canonical four-tier model) — https://letta.com/blog/agent-memory
2. LangChain — "Memory for agents" (CoALA-based taxonomy) — https://blog.langchain.dev/memory-for-agents/
3. HN 39360724 thread (transactional vs. relationship-driven split) — https://news.ycombinator.com/item?id=39360724

**If you have 2 hours (architectural depth):**
4. Zep / Graphiti paper (temporal knowledge graph) — https://arxiv.org/abs/2501.13956
5. Mem0 paper (production metrics + two-phase extraction) — https://arxiv.org/abs/2504.19413
6. Generative Agents paper (reflection + memory stream) — https://arxiv.org/abs/2304.03442
7. LongMemEval paper (what the memory bottleneck actually looks like) — https://arxiv.org/abs/2410.10813
8. Letta — "RAG is not Agent Memory" — https://www.letta.com/blog/rag-vs-agent-memory

**If you have a day (full field map):**
9. **Angle A — Academic** (this folder, `A-academic.md`). Covers the field in 8 sections + selected-sources table.
10. **Angle D — Commercial** (this folder, `D-commercial.md`). 17 vendors across 3 sub-segments + gaps framed as product opportunities.
11. CoALA paper — Sumers et al., arXiv 2309.02427 (vocabulary foundation)
12. PersonalLLM + PReF / LoRe / VRF sequence (personalization evaluation + low-rank preferences)
13. Eugene Yan — "Patterns for Personalization" + "Semantic IDs" (pre-LLM rigor + hybrid)

**If you have a week (full practitioner fluency):**
14. **Angle C — Open-Source** (this folder, `C-opensource.md`). Build a minimal memory system following A-MEM + Mem0 patterns.
15. **Angle E — Practical/Forums** (this folder, `E-practical.md`). Read the top 10 cited practitioner threads and build the Christian Rice two-agent LangGraph demo.
16. **Angle B — Industry** (this folder, `B-industry.md`). Map each vendor's public claims against your implementation.
17. Benchmarks: run LoCoMo + LongMemEval against your system; report numbers the same way Mem0 / Zep do.

**If you only have 10 minutes and want the Unslop punchline:**
Read the final two sections of this document — "Open Questions / Research Gaps" and "How This Category Fits in the Bigger Picture" — then skim the Lex and Zep summaries in `D-commercial.md`. The wedge is: *style memory as a portable, user-editable primitive + a humanness benchmark that measures "sounds like you" rather than "recalled the fact."*

---

## File Index

| File | Angle | Scope |
|---|---|---|
| [`A-academic.md`](./A-academic.md) | Academic literature | 30+ papers across ACL/NAACL/EMNLP, NeurIPS, ICLR, ICML, UIST, AAAI, COLING, IEEE TASLP, CIKM, ACM TOIS. Covers memory architectures, preference modeling, long-term dialogue & benchmarks, continual learning, surveys, patterns & gaps. |
| [`B-industry.md`](./B-industry.md) | Industry blogs | 17 posts (Feb 2024 – Apr 2026) from OpenAI, Anthropic, Google, Character.AI, Letta, Zep, LangChain, Eugene Yan. Covers tiered memory, self-editing, async consolidation, portability, long-dialogue infra. |
| [`C-opensource.md`](./C-opensource.md) | Open-source & GitHub | 20 repos with star counts, licenses, quotes. Letta/MemGPT, Mem0, Graphiti, A-MEM, LangMem, Cognee, MemoRAG, EM-LLM, MemoryBank, MemoryScope/ReMe, PersonaMem-v2, LlamaIndex memory, gptme, Motorhead, Chroma, OpenMemory MCP, Embedchain, Axolotl, Unsloth. |
| [`D-commercial.md`](./D-commercial.md) | Commercial landscape | 17 vendors across 3 sub-segments: (1) Memory-as-a-Service infra (Mem0, Zep, Letta, Supermemory, Cognee, Memobase, Personize, GetProfile, Fastino, LangChain, Pinecone, Weaviate); (2) Personalized writing assistants (Lex, Iris, Jenova, Lindy, ChatGPT/Claude consumer memory); (3) Enterprise CRM / revenue memory (Salesforce, Gong, HubSpot, Microsoft). |
| [`E-practical.md`](./E-practical.md) | Practical & forums | Reddit (r/ChatGPT, r/LocalLLaMA, r/LangChain), HN, dev.to, YouTube, engineering blogs, press. Three sub-communities, 40+ cited threads, 13 techniques/patterns, notable quotes, failure modes, security (Rehberger), cross-vendor benchmarks. |
| `INDEX.md` | This document | Category-level synthesis across all five angles. |
