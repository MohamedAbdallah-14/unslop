# Memory & Personalization — Angle D: Commercial Landscape

**Research value: high** — Memory-as-a-Service is now a crowded, well-funded category (20+ vendors since mid-2025) with clear sub-segments (infra memory layers, personalization APIs, writing assistants, enterprise CRM memory) and active convergence on hybrid vector+graph + temporal architectures.

**Scope.** Commercial products that persist user/customer/author knowledge across sessions so an AI can respond in a way that feels continuous, "mine", and human — directly adjacent to the Unslop goal of humanizing AI output. Ordered by sub-segment.

---

## Sub-segment 1: Memory-as-a-Service infrastructure

These vendors sell a drop-in "memory layer" API that sits between an agent and its LLM, extracting facts from conversations/data and re-injecting them on subsequent calls.

### 1. Mem0 ([mem0.ai](https://mem0.ai))
- **Tagline:** "AI Agents Forget. Mem0 Remembers." / "The Memory Layer for your AI Apps."
- **Architecture:** Hybrid vector + knowledge graph, multi-level memory (user/session/agent). LoCoMo-style two-phase pipeline (extract salient facts → intelligently merge).
- **Pricing:** Free Hobby (10k memories) → Starter $19/mo → Pro $249/mo (unlimited memories, Graph Memory gated here) → Enterprise custom.
- **Traction:** ~50k GitHub stars, 186M+ monthly API calls, $24M raised (YC), 100k+ developers claimed.
- **Enterprise:** SOC 2, HIPAA, BYOK, Kubernetes/air-gapped/private-cloud deploys.
- **Headline claim:** "Cuts prompt tokens by up to 80%… 91% faster responses, 26% accuracy lift over baseline memory."
- **Humanizer relevance:** Explicitly frames itself as enabling "personalised AI experiences" and "personality" ("Give your AI a memory and personality"). Case studies (Sunflower Sober, OpenNote) are all about relational/personalized behavior, not retrieval accuracy.

### 2. Zep / Graphiti ([getzep.com](https://www.getzep.com))
- **Tagline:** "Context Engineering — assembles the right context from chat history, business data, and user behavior."
- **Architecture:** Temporal knowledge graph (Graphiti, open source). Stores facts as entity-relation triplets with valid-from/valid-to timestamps. When facts change (e.g., user switches from Adidas → Nike), old facts are *invalidated* rather than overwritten, preserving provenance.
- **Pricing:** Free 1k credits/mo → Flex $25/mo (20k credits) → Flex Plus $475/mo (300k credits) → Enterprise custom. Billed per "Episode" (1 data object = 1 credit).
- **Traction:** ~24k GitHub stars (Graphiti), 94.8% Deep Memory Retrieval benchmark, 80.32% LoCoMo at 189ms single-shot.
- **Enterprise:** SOC 2 Type II, HIPAA BAA, BYOK/BYOM/BYOC.
- **Headline claim:** "200ms P95 retrieval… three lines of code… 100%+ accuracy improvements through personalized context."
- **Humanizer relevance:** Unique selling point is that memory *evolves over time* — the agent knows not just what the user likes, but how their taste changed. That temporal shape is exactly what makes responses feel "you knew me back when".

### 3. Letta ([letta.com](https://www.letta.com)) — formerly MemGPT
- **Tagline:** "The memory-first agent." / "Persistent agents instead of stateless sessions."
- **Architecture:** OS-inspired three-tier — core memory (always in-context), recall memory (searchable history), archival memory (cold). LLM edits its own memory via tool calls ("Memory as Runtime").
- **Pricing:** Free tier → Pro $20/mo (20 agents, $20 credits) → Max $200/mo (50+ agents) → API Plan $20/mo + $0.10/active agent/mo → Enterprise custom with SAML/OIDC.
- **Traction:** ~22k GitHub stars, $10M raised.
- **Differentiator:** Agents are portable — memory can be moved across LLM providers and devices. "View your agent's memory in the memory palace."
- **Humanizer relevance:** Only vendor treating *persona* as a first-class object ("each with their own unique experiences and persona, designed to evolve with you"). Closest existing prior art to a writing-style-owning memory.

### 4. Supermemory ([supermemory.ai](https://supermemory.ai))
- **Tagline:** "The memory layer for AI agents." Bundles five layers: User Profiles, Memory Graph, Retrieval, Extractors, Connectors.
- **Pricing:** Free (1M tokens/mo) → Pro $19/mo (3M tokens) → Scale $399/mo (80M tokens) → Enterprise.
- **Traction:** $3M raised Oct 2025, ~17k GitHub stars, 10k+ power users on consumer app, #1 on LongMemEval (85.2%), LoCoMo, ConvoMem.
- **Differentiator:** Has a consumer app (`app.supermemory.ai`) + plugins for Cursor, Claude Code, Windsurf, Chrome. "One memory across all your AI tools."
- **Humanizer relevance:** Explicit "User Profiles" primitive — builds behavioral profiles of intent/preferences/context, not just message logs.

### 5. Cognee ([cognee.ai](https://www.cognee.ai))
- **Architecture:** KG + vector + cognitive-science concepts, ingests 30+ data sources (docs, images, audio, Slack). ~13k stars, $7.5M seed, adopted by 70+ companies. Graph features free at all tiers (differentiator vs Mem0 where graph is $249/mo-gated).

### 6. Memobase / Memori / Personize / GetProfile
- **Memobase** ([memobase.io](https://www.memobase.io)) — "AI Memory for LLMs, Build Personalized Agents."
- **Memori** — SQL-native alternative (~12k stars), rejects vector-first framing.
- **Personize** ([personize.ai](https://personize.ai)) — **Enterprise angle**: "Unified Customer Memory for AI Agents" across CRM/emails/transcripts/docs. Positions itself as a governance layer so every authorized agent reads the same context. HubSpot + Salesforce connectors.
- **GetProfile** ([getprofile.org](https://www.getprofile.org)) — Apache-2.0 OpenAI-compatible *proxy* that auto-injects typed user traits with confidence scores into every prompt. Interesting mechanism: personalization as a transparent middleware.

### 7. Fastino Personalization API
- Positions as "market leader in agent personalization." Unified API for user-level memory, retrieval, deterministic summarization, GDPR. Integrates with LangChain, LlamaIndex, Claude Tools, OpenAI Realtime.

### 8. LangChain / LangSmith / LangGraph memory
- Not a product per se — LangGraph's state checkpointer (Postgres default, Mongo optional) + LangSmith's memory store is the "default" memory primitive for devs already on the stack. PostgreSQL is the actual persistence layer; Redis is ephemeral only. Memory is a *feature* of the agent framework, not a differentiated product — in contrast to Mem0/Zep, which compete specifically on memory quality.

### 9. Pinecone / Weaviate — memory-as-positioning on top of vector DBs
- **Pinecone Assistant:** document-grounded chat; notably has *no* native user-profile/long-term personalization primitive — a gap competitors like Mem0 explicitly fill on top of vector DBs like Pinecone.
- **Weaviate Personalization Agent** (preview, Weaviate Cloud): dedicated "personas" collection + persona-interaction logs; combines LLMs and classic ranking ML to return tailored recommendations with natural-language explanations. Most explicit "personalization" productization among vector-DB incumbents.

---

## Sub-segment 2: Personalized writing assistants (directly adjacent to Unslop)

These are the closest commercial analogs to "humanize my AI output" — they explicitly sell *voice ownership*.

### 10. Lex ([lex.page](https://lex.page))
- **Positioning:** "Collaborative documents, with powerful AI editing tools" — Google Docs replacement with AI. 300k+ writers.
- **Memory primitives:** **Style Guides** (trained on your writing samples — "AI can clearly interpret writing descriptions for other AI systems") + **Knowledge Bases** (persistent background across sessions) + **Prompt Library**.
- **Framing quote (marketing):** "Generic AI trained on the internet speaks in averages and optimizes for what's most likely, stripping unique voice from writing. Style Guides solve this by teaching Lex to match your signature tone, metaphors, terminology, narrative voice, and storytelling approach." This is *exactly* the humanization pitch.
- **Pricing:** Pro $12–18/mo, Team $5–8/user/mo. Premium models (GPT-5, Claude 4.1 Opus). Enterprise API privacy — writing not used for training.

### 11. Athena / Iris by Athena ([iris.theathenaai.com](https://iris.theathenaai.com))
- Voice-first personal assistant; "remembers past conversations to provide contextual, personalized responses." Lighter-weight and more assistant-shaped than Lex. Less writing-focused.

### 12. Jenova AI Writing Assistant
- "Adaptive voice matching" — analyzes writing samples to reproduce tone, sentence structure, vocabulary. Persistent session memory that tracks style, instructions, draft progress; standing preferences accumulate from user feedback across sessions. Same shape as Lex, more automatic.

### 13. Lindy ([lindy.ai](https://www.lindy.ai))
- Agent builder, not writer, but **memory model is illustrative**: persistent "memories" snippets auto-injected into every agent call (e.g., "Customer prefers email over phone," "User timezone: PST"). CRUD tool surface exposed to the agent (read/create/update/delete memory). Memory can be user-defined, pre-configured, or agent-written during execution.

### 14. ChatGPT / Claude consumer memory (context for what "default" feels like)
- **ChatGPT Memory**: dual automatic + manual extraction, capped memories, unlimited chat history. Plus/Pro subscribers.
- **Claude Memory** (GA March 2026, including free tier): automatic learning on ~24h cadence, extracts role/skills/work style/communication preferences. **Key 2026 development:** memory *import* from ChatGPT/Gemini — a nascent portability norm Claude is pushing, implicitly commoditizing vendor-specific lock-in.

---

## Sub-segment 3: Enterprise CRM / revenue-intelligence memory

This is where memory meets customer profile at scale; "humanization" here means agents that sound like a rep who knows the account.

### 15. Salesforce Einstein + Agentic Memory
- Salesforce Engineering publicly published an architecture for **"Agentic Memory"**: persistent memory layer tied to a profile graph, spanning sessions and channels, with confidence scoring, write/read gates, and hybrid semantic validation. Short-term session context + long-term profile-linked memory.
- **Einstein Conversation Insights Spring '26**: Generative ECI (unified call summaries with sentiment + next steps), up to 8 custom insights per call, 2,000 ECI standard licenses for Enterprise Edition.

### 16. Gong — Mission Andromeda (Feb 2026)
- Launched **Revenue Graph** — "a living network of your revenue data that automatically captures and connects every interaction across your business." **Gong Assistant** provides conversational Q&A grounded in real customer conversations. **Gong Enable / AI Trainer** uses simulations drawn from successful conversations across the org — memory as coaching corpus, not just retrieval.

### 17. HubSpot Breeze / Microsoft Copilot (context-only mention)
- Both ship customer-context memory tied to CRM objects; competitive baseline that forces Mem0/Zep/Personize to differentiate on portability, openness, and writing-quality control.

---

## Patterns, trends, gaps

### Patterns
1. **Hybrid vector + graph has won** for production agents (Mem0, Zep, Cognee, Supermemory all converge here). Pure-vector memory is now table stakes; the premium is paid for *relational + temporal* structure.
2. **Temporal fact invalidation** (Zep's "Robbie switched from Adidas to Nike" example) is emerging as the differentiator over "append-only log" memory.
3. **Two-phase extraction** (salient-fact extraction → intelligent merge/dedupe) is the shared algorithmic pattern, pioneered by Mem0's LoCoMo pipeline and mimicked across the stack.
4. **Pricing floor is ~$19–25/mo** for the first paid tier across Mem0, Zep, Supermemory, Letta — suggests a market-tested willingness-to-pay for individual/indie devs.
5. **"Three lines of code" / "single-line install"** has become the mandatory onboarding pitch (Mem0, Zep, Supermemory, Letta all claim this).
6. **User Profile as a first-class primitive** is new in 2025–26 — Supermemory, Fastino, GetProfile, and Weaviate Personalization Agent all ship a named "profile" object, separate from raw memory events.

### Trends
1. **Memory portability is becoming a norm** — Claude's March 2026 import from ChatGPT/Gemini memories, Letta's cross-model agent migration, and GetProfile's proxy architecture all push against vendor lock-in. Users increasingly expect to *own* their memory artifact.
2. **Writing-voice products are adopting memory-infra patterns**: Lex's Style Guides + Knowledge Bases, Jenova's persistent preference accumulation. They are infra-layer products wearing writer-facing UX.
3. **Consolidation pressure**: Humanloop sunsetted Sep 2025 and merged into Anthropic Console. Expect more personalization/eval tools to get absorbed into foundation-model vendors.
4. **Enterprise CRM incumbents moving fast**: Salesforce's published Agentic Memory architecture (May/June 2026) and Gong's Mission Andromeda (Feb 2026) compress the window for startup wedges in enterprise customer memory.

### Gaps (opportunity space for a humanization-focused product)
1. **No vendor owns "writing voice memory" as a portable artifact.** Lex owns it *inside* its editor; Mem0/Supermemory own it *inside* their API. Nobody sells a portable "voice profile" you attach to any LLM surface (Claude, Cursor, email client).
2. **Style contradictions are unsolved.** Temporal fact invalidation handles "Adidas → Nike" well; nobody has published the equivalent for "voice last March vs. voice now" where the author legitimately evolves. This is a humanization-native problem.
3. **Humanization as an outcome metric is missing.** Every memory vendor benchmarks LoCoMo/LongMemEval (retrieval accuracy). None benchmark "does output read as human/authored-by-me." There is no commercial "humanness score" SLA.
4. **Author/reader asymmetry.** All products model one user's preferences. None model the reader/audience as a co-memory object — though writing humanness depends heavily on audience context.
5. **Emotional/affect memory barely exists commercially.** Mem0 cites healthcare/therapy case studies but the primitive is still "fact + timestamp." No vendor ships affective/mood memory as an explicit type.

---

## Sources

- [Mem0](https://mem0.ai/) — homepage, pricing, positioning, case studies
- [Zep / Graphiti](https://www.getzep.com/) — homepage, temporal knowledge graph, LoCoMo benchmarks
- [Letta](https://www.letta.com/) — homepage, persistent agents, memory portability
- [Supermemory](https://supermemory.ai/) — llms.txt product summary, pricing, benchmark claims
- [Lex.page](https://lex.page/) — homepage, FAQ; plus [Style Guides read](https://lex.page/read/3492a59e-ea19-4733-964a-3adc25b5f3e0) and [pricing](https://lex.page/pricing)
- [widemem.ai 2026 memory landscape](https://widemem.ai/blog/memory-landscape) — market-wide survey of 20+ vendors
- [HydraDB Mem0 vs Zep vs Letta](https://hydradb.com/blog/mem0-vs-zep-vs-letta) — architecture-level comparison
- [Vectorize.io memory system comparison](https://vectorize.io/articles/best-ai-agent-memory-systems) — framework comparison table
- [Salesforce Engineering — Agentic Memory](https://engineering.salesforce.com/how-agentic-memory-enables-durable-reliable-ai-agents-across-millions-of-enterprise-users/) — primary architecture doc
- [Gong — Mission Andromeda press release](https://www.gong.io/press/gong-launches-mission-andromeda-expanding-its-revenue-ai-os-to-enablement-and-account-management)
- [Salesforce Break — Einstein Conversation Insights Spring '26](https://salesforcebreak.com/2026/02/26/einstein-conversation-insights-spring-26/)
- [Lindy docs — Memory fundamentals](https://docs.lindy.ai/fundamentals/lindy-101/memory)
- [Weaviate Personalization Agent](https://weaviate.io/product/personalization-agent)
- [Claude Lab — Claude Memory for all users](https://claudelab.net/en/articles/claude-ai/claude-memory-chat-history) and [PrimeTimer — memory import](https://www.primetimer.com/features/anthropic-opens-gate-for-importing-memories-from-chatgpt-gemini-and-more-to-claude-in-a-new-gamechanger-update)
- [AI Tools Atlas — Humanloop sunset / Anthropic migration](https://aitoolsatlas.ai/tools/humanloop/pricing)
- [Personize](https://personize.ai/) — unified customer memory for enterprise agents
- [GetProfile](https://www.getprofile.org/) — OpenAI-compatible personalization proxy
