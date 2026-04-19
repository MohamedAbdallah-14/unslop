# Memory & Personalization for Humanization — Academic Literature

**Project:** Humanizing AI output and thinking
**Category:** Memory & Personalization (long-term memory, episodic memory, user adaptation)
**Angle:** A — Academic
**Compiled:** 2026-04-19
**Scope:** 20+ papers on LLM memory systems, episodic/semantic memory for agents, personalization (P-RLHF, PersonalLLM), continual learning for dialogue, long-term user modeling. Primary venues: ACL/NAACL/EMNLP, NeurIPS, ICLR, RecSys, CIKM, UMAP, AAAI, ICML, UIST.

---

## 1. Memory Architectures for LLM Agents

### 1.1 MemGPT: Towards LLMs as Operating Systems
- **Authors:** C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, J. E. Gonzalez (UC Berkeley Sky Lab)
- **Venue:** arXiv 2310.08560 (2023); productized as the Letta framework (2024)
- **Core idea:** OS-inspired *virtual context management*. A two-tier hierarchy (main context ↔ external context) and function-calling paging let an agent self-manage what enters its finite window.
- **Relevance to humanization:** Foundational for self-editing "persona" and "human" memory blocks that persist across sessions — the substrate most downstream humanization work now assumes.

### 1.2 A-MEM: Agentic Memory for LLM Agents
- **Authors:** W. Xu et al. (Rutgers, AIOS Foundation)
- **Venue:** arXiv 2502.12110; accepted NeurIPS 2025
- **Core idea:** A Zettelkasten-inspired memory that auto-generates structured notes (contextual descriptions, keywords, tags), discovers links to prior notes, and *evolves* existing memories when new information arrives — moving beyond fixed write/read operations.
- **Relevance:** Gives agents the kind of associative, drift-over-time memory graph humans exhibit; explicitly addresses the rigidity critique of MemGPT-style stores.

### 1.3 Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- **Authors:** P. Rasmussen, P. Paliychuk, T. Beauvais, J. Ryan, D. Chalef
- **Venue:** arXiv 2501.13956 (2025)
- **Core idea:** Graphiti engine — a bi-temporal, hierarchical knowledge graph that fuses unstructured dialogue with structured records while preserving both "valid time" and "ingestion time."
- **Results:** 94.8% on Deep Memory Retrieval (vs. MemGPT 93.4%); up to +18.5% and −90% latency vs. baselines on LongMemEval.
- **Relevance:** Explicit temporal reasoning is critical for "this is still true of the user" vs. "this used to be true of the user" — a common failure mode of naive vector-store memory.

### 1.4 HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs
- **Authors:** B. J. Gutiérrez, Y. Shu, Y. Gu, M. Yasunaga, Y. Su
- **Venue:** NeurIPS 2024 (OSU-NLP); HippoRAG 2 at ICML 2025
- **Core idea:** Combines LLMs, KGs, and Personalized PageRank to emulate the hippocampus/neocortex division of labor — retrieval as graph traversal over extracted triples, not only dense similarity.
- **Results:** +20% on multi-hop QA; 10–20× cheaper and 6–13× faster than iterative retrieval.
- **Relevance:** Biologically grounded motivation is directly on-point for "humanization"; offers a retrieval substrate that supports single-hop latency budgets while retaining multi-hop capability.

### 1.5 Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- **Authors:** P. Chhikara, D. Khant, S. Aryan, T. Singh, D. Yadav
- **Venue:** arXiv 2504.19413 (2025)
- **Core idea:** Single-pass ADD-only extraction and multi-signal retrieval (semantic + keyword + entity) with an optional graph variant. Designed for p95 latency and cost, not just recall.
- **Results:** +26% LLM-as-judge vs. OpenAI memory; −91% p95 latency vs. full context; >90% token savings. Graph variant +~2% over base on LOCOMO.
- **Relevance:** Only one of the production-oriented systems to jointly report quality *and* deployment cost — the metric frame most relevant to shipping a humanization layer.

### 1.6 MemoryLLM: Towards Self-Updatable Large Language Models
- **Authors:** Y. Wang, Y. Gao, X. Chen, H. Jiang, S. Li, J. Yang, Q. Yin, Z. Li, X. Li, B. Yin, J. Shang, J. McAuley
- **Venue:** arXiv 2402.04624 (2024); ICML 2024
- **Core idea:** Fixed-size memory pool of hidden vectors *inside* each transformer layer; new knowledge injected via sliding-window update, with exponential decay as controlled forgetting.
- **Relevance:** A parametric (rather than retrieval) take on long-term memory — robust through ~1M updates without degradation; a candidate when retrieval hops cost too much latency.

### 1.7 MemoryBank / SiliconFriend
- **Authors:** W. Zhong, L. Guo, Q. Gao, H. Ye, Y. Wang
- **Venue:** AAAI 2024
- **Core idea:** Memory updater based on the Ebbinghaus forgetting curve — time-and-salience-weighted reinforcement/forgetting. Operationalized in SiliconFriend, a bilingual companion chatbot fine-tuned with 38k psychological dialogues via LoRA.
- **Relevance:** Rare example of explicitly psychologically motivated memory dynamics in a deployed companion agent — directly relevant to humanization through affect-aware recall.

### 1.8 Generative Agents: Interactive Simulacra of Human Behavior
- **Authors:** J. S. Park et al. (Stanford, Google)
- **Venue:** UIST 2023
- **Core idea:** Memory stream + reflection + planning. Reflection synthesizes low-level observations into higher-order beliefs; retrieval uses recency, importance, and relevance jointly.
- **Relevance:** The canonical architecture for "believable" agent behavior — reflection is the mechanism most humanization work imports when it wants an agent to have *opinions* about the user rather than just records.

### 1.9 REMem: Reasoning with Episodic Memory in Language Agents
- **Venue:** ICLR 2026 (OpenReview)
- **Core idea:** Two-phase design — (1) index experiences into a hybrid memory graph with time-aware gists and facts; (2) agentic inference with iterative retrieval tools.
- **Results:** +3.4% episodic recollection and +13.4% episodic reasoning over Mem0 and HippoRAG 2.
- **Relevance:** Explicitly frames the episodic-vs-semantic split that most agent memory work elides.

### 1.10 Echo: A Large Language Model with Temporal Episodic Memory
- **Venue:** arXiv 2502.16090 (2025)
- **Core idea:** Multi-agent data generation + EM-Test benchmark targeting recall across varying time spans.
- **Relevance:** Rare focus on *temporal* episodic recall specifically (yesterday vs. six months ago), rather than collapsing everything into one flat store.

---

## 2. Personalization & Preference Modeling

### 2.1 PersonalLLM: Tailoring LLMs to Individual Preferences
- **Authors:** T. P. Zollo et al.
- **Venue:** ICLR 2025
- **Core idea:** Benchmark + dataset of open-ended prompts with multiple high-quality answers curated to elicit *heterogeneous* user preferences. Uses pretrained reward models to simulate diverse users and explores ICL / meta-learning baselines that leverage similar-user history under sparsity.
- **Relevance:** The canonical reference dataset for evaluating any personalization claim at ICLR-grade rigor; removes the "but you just trained one reward model" critique.

### 2.2 Personalized RLHF (P-RLHF)
- **Venue:** NeurIPS 2024 (OpenReview xxBoca28oG)
- **Core idea:** Lightweight user model jointly captures *explicit* preferences (from profile) and *implicit* preferences (from feedback), trained alongside the policy. Scales sub-linearly in number of users.
- **Relevance:** Foundational framing for personalization that does not require every user to articulate preferences upfront — matches realistic UX.

### 2.3 Personalization via Reward Factorization (PReF)
- **Venue:** arXiv 2503.06358 (2025)
- **Core idea:** Each user's reward = linear combination of a small number of shared *basis* reward functions. Preference manifold is low-dimensional.
- **Results:** 30× fewer user responses than naive RLHF; 67% win rate over default GPT-4o responses.
- **Relevance:** Practical cold-start story for personalization — only a handful of comparisons needed to locate a user in preference space.

### 2.4 Many Preferences, Few Policies (PALM)
- **Venue:** arXiv 2604.04144
- **Core idea:** Rather than one model per user, maintain a *portfolio* of aligned LLMs covering representative preference modes (safety, humor, brevity, etc.).
- **Relevance:** Deployment-efficient alternative when per-user parameter updates are infeasible; natural fit for a "style" layer on top of a base humanization model.

### 2.5 Low-Rank Reward Modeling (LoRe)
- **Venue:** arXiv 2504.14439 (2025)
- **Core idea:** Represent individual preferences as weighted combinations of shared basis rewards — scalable few-shot adaptation without explicit user clusters.
- **Relevance:** Closely related to PReF; makes the low-rank assumption the central inductive bias.

### 2.6 Uncertainty-Aware Variational Reward Factorization (VRF)
- **Venue:** arXiv 2604.00997 (2026)
- **Core idea:** Treat per-user preference weights as *distributions*, not points; infer via a variational encoder and match to shared bases with Wasserstein loss; downweight uncertain users via variance-attenuated loss.
- **Relevance:** Directly addresses the "new user with 3 ratings" overconfidence failure that breaks most personalization pipelines.

### 2.7 Aligning LLMs with Individual Preferences via Interaction
- **Venue:** COLING 2025 (ALOE benchmark)
- **Core idea:** Train LLMs to infer unspoken preferences through multi-turn conversation; 3,310+ personas and 3k+ multi-turn preference dialogues.
- **Relevance:** Moves personalization signal from explicit ratings to *implicit signal in conversation* — the only practical source for most humanization deployments.

### 2.8 A Survey on Personalized Alignment
- **Venue:** arXiv 2503.17003 (2025)
- **Core idea:** Organizes the field around three pillars: preference memory management, personalized generation/rewarding, feedback-based alignment. Proposes a 90-dimensional preference space synthesizing psychological models and alignment dimensions.
- **Relevance:** Map of the space; useful taxonomy for positioning a humanization product's personalization story.

### 2.9 LaMP: When Large Language Models Meet Personalization
- **Authors:** A. Salemi et al.
- **Venue:** ACL 2024
- **Core idea:** Seven-task personalization benchmark spanning classification and generation, with retrieval-augmented personalization baselines (BM25, Contriever, recency).
- **Relevance:** De facto evaluation for any personalized generation claim; widely replicated.

### 2.10 LongLaMP: A Benchmark for Personalized Long-form Text Generation
- **Venue:** arXiv 2407.11016 (2024)
- **Core idea:** Extends LaMP to long-form tasks (emails, reviews) where style drift matters more than label match.
- **Relevance:** The matching benchmark if the humanization product outputs long-form text — short-form LaMP does not discriminate style fidelity well.

### 2.11 Persona-Plug (PPlug): One PLUG for All Users
- **Venue:** ACL 2025 (Findings)
- **Core idea:** Lightweight user-specific embedding from historical context, attached as a prompt/plug-in to a frozen LLM — no parameter tuning per user.
- **Relevance:** Cheapest plausible personalization route for humanization; aligns with the "adapter per user" product pattern.

### 2.12 PRIME: Cognitive Dual-Memory and Personalized Thought Process
- **Venue:** EMNLP 2025
- **Core idea:** Episodic memory mirrors historical engagements; semantic memory mirrors long-term evolving beliefs; adds a "slow thinking" personalized reasoning step. Evaluated on a new Change-My-View (CMV) long-context personalization dataset from Reddit.
- **Relevance:** Most explicit academic adoption of the episodic/semantic split for *personalization* rather than just memory; closely mirrors how humanization must operate.

### 2.13 PrLM: Explicit Reasoning for Personalized RAG via Contrastive Reward Optimization
- **Venue:** CIKM 2025
- **Core idea:** RL-trains the LLM to reason over retrieved user profiles, guided by a contrastively trained personalization reward model; robust to varying profile count and retriever.
- **Relevance:** Shows that personalization benefits from *explicit reasoning over* retrieved user facts, not just concatenation — useful signal against the "dump memory into context and pray" approach.

---

## 3. Long-Term Dialogue, User Modeling & Benchmarks

### 3.1 LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
- **Authors:** D. Wu et al.
- **Venue:** ICLR 2025
- **Core idea:** 500 curated questions over scalable chat histories (115k and 1.5M token variants) targeting five abilities — information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention.
- **Result:** Commercial assistants drop 30–60% accuracy on the small variant — a quantified "long-term memory bottleneck."
- **Relevance:** The benchmark that makes the memory bottleneck *measurable* and thus actionable for a humanization product roadmap.

### 3.2 LoCoMo: Evaluating Very Long-Term Conversational Memory of LLM Agents
- **Authors:** A. Maharana et al. (Snap Research)
- **Venue:** ACL 2024
- **Core idea:** 50 machine-human-hybrid conversations of 300–600 turns over imagined 6–12 month timelines, with temporal event graphs and multimodal turns. Three eval tasks: QA, event summarization, multimodal dialog generation.
- **Relevance:** The "scale and time horizon" benchmark — complementary to LongMemEval; required reading for any long-term memory claim.

### 3.3 Reflective Memory Management (RMM) for Long-Term Personalized Dialogue
- **Venue:** ACL 2025 (long papers)
- **Core idea:** Prospective Reflection continuously summarizes interactions at multiple granularities into a personalized memory bank; Retrospective Reflection refines retrieval via online RL from cited evidence.
- **Result:** +10% accuracy on LongMemEval over non-memory baselines.
- **Relevance:** One of the first long-term personalized dialogue systems that treats *retrieval policy itself* as something to learn online.

### 3.4 LD-Agent: Hello Again! LLM-powered Personalized Agent for Long-term Dialogue
- **Venue:** NAACL 2025
- **Core idea:** Model-agnostic framework with event perception, persona extraction, and response generation modules; separate long/short-term memory banks; topic-based retrieval; dynamic persona modeling for both user and agent.
- **Relevance:** Blueprint for a modular humanization agent where each humanization subcomponent (persona, events, reply style) can be swapped.

### 3.5 PLATO-LTM: Long-Term Memory Mechanism for Dialogue
- **Venue:** Findings of ACL 2022
- **Core idea:** Real-time persona bank for both user and bot without requiring multi-session training data.
- **Relevance:** An early canonical reference for the "online persona extraction" pattern that modern systems assume.

### 3.6 Faithful Persona-based Conversational Dataset Generation with LLMs
- **Venue:** ACL 2024 Findings
- **Core idea:** Generator-Critic pipeline (mixture-of-experts critic) that expands PersonaChat into Synthetic-Persona-Chat (20k conversations) with measurable quality improvements.
- **Relevance:** Data supply-chain paper — persona-consistent training data is the bottleneck for humanization fine-tunes.

### 3.7 SEEM: Structured Episodic Event Memory
- **Venue:** arXiv 2601.06411 (2026)
- **Core idea:** Hierarchical framework — graph memory for relational facts + dynamic episodic memory for narrative progression; Episodic Event Frames anchored by provenance pointers; Reverse Provenance Expansion reconstructs narrative context.
- **Relevance:** Explicit narrative-progression memory is rare and directly serves human-style recall (which is story-shaped, not table-shaped).

---

## 4. Continual Learning for Dialogue & User Modeling

### 4.1 Continual Learning in Task-Oriented Dialogue Systems
- **Authors:** A. Madotto, Z. Lin, Z. Zhou, S. Moon, P. Crook, B. Liu, Z. Yu, E. Cho, Z. Wang
- **Venue:** EMNLP 2021
- **Core idea:** First 37-domain CL benchmark for TOD; residual adapter method + replay strategy. Performance ≈ multitask while learning new domains 20× faster.
- **Relevance:** Still the standard reference for continual learning in dialogue; the residual-adapter pattern reappears in every "add a new user domain without forgetting" design.

### 4.2 Lifelong and Continual Learning Dialogue Systems (LINC)
- **Authors:** B. Liu, S. Mazumder
- **Venue:** AAAI 2021 (Senior Member Track)
- **Core idea:** Self-supervised lifelong learning during deployment — new world knowledge, new language expressions grounded to actions, new conversational skills.
- **Relevance:** Philosophical grounding for any system that claims to "get to know the user over time"; defines three distinct knowledge types rather than collapsing everything into "memory."

### 4.3 Acquiring New Knowledge Without Losing Old Ones for Effective Continual Dialogue Policy Learning
- **Venue:** IEEE TASLP (2024)
- **Core idea:** Continual dialogue *policy* learning (not just memory), with explicit anti-forgetting objectives.
- **Relevance:** Reminder that continual learning targets include *how the agent acts*, not only *what it knows*.

---

## 5. Surveys & Position Papers

### 5.1 A Survey on the Memory Mechanism of Large Language Model-based Agents
- **Venue:** ACM TOIS (2025), dl.acm.org/doi/10.1145/3748302
- **Taxonomy:** Four structures — Lightweight Semantic, Entity-Centric/Personalized, Episodic/Reflective, Structured/Hierarchical. Identifies benchmark-saturation and metric-misalignment as methodological risks.
- **Relevance:** Best current orientation map for the agent memory subfield.

### 5.2 LLM Agent Memory: A Unified Representation–Management Perspective
- **Venue:** Preprints.org 202603.0359 (2026)
- **Taxonomy:** Memory represented as tokens, intermediate representations, or parameters; operations categorized as consolidation, updating, indexing, forgetting, retrieval, condensation.
- **Relevance:** Useful engineering vocabulary — frames a humanization design space by *operation* rather than *architecture*.

### 5.3 A Survey on Personalized Alignment (see §2.8)

---

## 6. Patterns & Trends

1. **Episodic ↔ semantic split is re-emerging as a first-class architectural axis.** PRIME, REMem, SEEM, Echo, and the TOIS survey all explicitly separate story-shaped personal experiences from time-invariant beliefs. Systems that collapse both into a single vector store (early MemGPT, naive RAG chat) consistently lose on multi-session reasoning.

2. **Memory is moving from storage to *policy*.** RMM (online RL over retrieval), PrLM (contrastive reward for reasoning-over-profile), and A-MEM (memory *evolution* at write time) treat what to remember, how to retrieve, and how to update as learned behaviors — not fixed pipelines.

3. **Personalization is converging on low-rank preference manifolds.** PReF, LoRe, and VRF independently arrive at the same inductive bias: individual rewards = weighted combination of shared basis rewards. This lets personalization work with tens, not thousands, of user signals — critical for cold start in any humanization product.

4. **Temporal reasoning is the new recall.** Zep's bi-temporal KG, LongMemEval's explicit "knowledge updates" category, LoCoMo's 6–12 month timelines, and Echo's time-span benchmark all signal that "did we remember this?" has shifted to "do we know this is still true?" — a much harder and more human-like task.

5. **Forgetting is being taken seriously.** MemoryBank's Ebbinghaus curve, MemoryLLM's exponential decay, and the TOIS survey's explicit "forgetting" operation treat controlled forgetting as a *feature*, not a bug. This aligns with the humanization objective: humans selectively forget, and agents that never do feel uncanny.

6. **Latency/cost metrics are entering memory evaluation.** Mem0 (p95 latency), Zep (−90% latency), and HippoRAG (10–20× cheaper) all co-report quality *and* deployment cost. Academic memory systems that ignore this axis increasingly look impractical.

7. **Benchmarks have matured in 18 months.** Where 2023 papers leaned on recall over five-session dialogues, 2024–2025 work (LongMemEval, LoCoMo, LongLaMP, PersonalLLM, ALOE) provides multi-session, temporal, multimodal, and preference-heterogeneity evaluations. Any new humanization claim now needs to land on at least one of these.

---

## 7. Gaps & Open Questions

1. **Memory + personalization are still mostly studied in isolation.** PRIME is the most integrated example; almost all others are either a memory system benchmarked on neutral recall or a personalization system tested on short contexts. A humanization product needs both *and* the interaction between them (e.g., updating persona beliefs as episodic memory accumulates).

2. **Emotional and affective memory are under-modeled.** Outside of MemoryBank/SiliconFriend, very few academic systems explicitly track affect, sentiment trajectories, or relationship state — arguably the most distinctively human aspect of long-term memory.

3. **Evaluation of *style* fidelity, not just factual recall, is immature.** LongLaMP gestures at this but most benchmarks still reward factual hits. For humanization, "would this user recognize their own voice?" is the harder metric and is essentially absent from public benchmarks.

4. **Privacy and editability are treated as afterthoughts.** Almost no academic memory paper addresses right-to-forget, per-memory access control, or auditable provenance. Zep's bi-temporal graph is the closest; production humanization systems will need more.

5. **Cold start for personalization remains brittle.** VRF addresses uncertainty but the field still lacks principled guidance on when it is worse than nothing to personalize — most systems assume more user data is always better.

6. **Cross-session *identity drift* of the agent itself.** Generative Agents' reflection mechanism gives the agent opinions, but almost no work asks how those opinions should evolve coherently across months. Humans have narrative identity; current agents have memory without biography.

7. **Multilingual / multicultural personalization.** SiliconFriend is bilingual, but almost all other cited work is English-only. Humanization across languages and cultural norms is an unsolved academic problem with immediate product consequences.

---

## 8. Selected Sources

| Ref | Paper | Venue | URL |
|-----|-------|-------|-----|
| 1.1 | MemGPT | arXiv 2023 / Letta 2024 | https://arxiv.org/abs/2310.08560 |
| 1.2 | A-MEM | NeurIPS 2025 | https://arxiv.org/abs/2502.12110 |
| 1.3 | Zep / Graphiti | arXiv 2025 | https://arxiv.org/abs/2501.13956 |
| 1.4 | HippoRAG | NeurIPS 2024 | https://papers.nips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html |
| 1.5 | Mem0 | arXiv 2025 | https://arxiv.org/abs/2504.19413 |
| 1.6 | MemoryLLM | ICML 2024 | https://arxiv.org/abs/2402.04624 |
| 1.7 | MemoryBank / SiliconFriend | AAAI 2024 | https://arxiv.org/abs/2305.10250 |
| 1.8 | Generative Agents | UIST 2023 | https://arxiv.org/abs/2304.03442 |
| 1.9 | REMem | ICLR 2026 (OpenReview) | https://openreview.net/pdf?id=fugnQxbvMm |
| 1.10 | Echo (Temporal Episodic Memory) | arXiv 2025 | https://arxiv.org/abs/2502.16090 |
| 2.1 | PersonalLLM | ICLR 2025 | https://arxiv.org/abs/2409.20296 |
| 2.2 | P-RLHF | NeurIPS 2024 | https://openreview.net/pdf?id=xxBoca28oG |
| 2.3 | PReF | arXiv 2025 | https://arxiv.org/abs/2503.06358 |
| 2.4 | PALM (Many Preferences, Few Policies) | arXiv 2026 | https://arxiv.org/abs/2604.04144 |
| 2.5 | LoRe | arXiv 2025 | https://arxiv.org/abs/2504.14439 |
| 2.6 | VRF | arXiv 2026 | https://arxiv.org/abs/2604.00997 |
| 2.7 | Aligning via Interaction (ALOE) | COLING 2025 | https://aclanthology.org/2025.coling-main.511/ |
| 2.8 | Personalized Alignment Survey | arXiv 2025 | https://arxiv.org/abs/2503.17003 |
| 2.9 | LaMP | ACL 2024 | https://github.com/lamp-benchmark/lamp |
| 2.10 | LongLaMP | arXiv 2024 | https://arxiv.org/abs/2407.11016 |
| 2.11 | Persona-Plug (PPlug) | ACL 2025 Findings | https://aclanthology.org/2025.acl-long.461.pdf |
| 2.12 | PRIME | EMNLP 2025 | https://aclanthology.org/2025.emnlp-main.1711/ |
| 2.13 | PrLM | CIKM 2025 | https://arxiv.org/abs/2508.07342 |
| 3.1 | LongMemEval | ICLR 2025 | https://arxiv.org/abs/2410.10813 |
| 3.2 | LoCoMo | ACL 2024 | https://aclanthology.org/2024.acl-long.747.pdf |
| 3.3 | Reflective Memory Management | ACL 2025 | https://aclanthology.org/2025.acl-long.413/ |
| 3.4 | LD-Agent | NAACL 2025 | https://aclanthology.org/2025.naacl-long.272/ |
| 3.5 | PLATO-LTM | Findings ACL 2022 | https://aclanthology.org/2022.findings-acl.207.pdf |
| 3.6 | Faithful Persona Dataset Generation | ACL 2024 Findings | https://aclanthology.org/2024.findings-acl.904/ |
| 3.7 | SEEM | arXiv 2026 | https://arxiv.org/abs/2601.06411 |
| 4.1 | Continual Learning in TOD | EMNLP 2021 | https://aclanthology.org/2021.emnlp-main.590/ |
| 4.2 | LINC (Lifelong Dialogue) | AAAI 2021 | https://cdn.aaai.org/ojs/17768/17768-13-21262-1-2-20210518.pdf |
| 4.3 | Continual Dialogue Policy | IEEE TASLP 2024 | https://ieeexplore.ieee.org/document/10366832 |
| 5.1 | Agent Memory Survey (TOIS) | ACM TOIS 2025 | https://dl.acm.org/doi/10.1145/3748302 |
| 5.2 | Unified Representation–Management Survey | Preprints.org 2026 | https://www.preprints.org/manuscript/202603.0359/v2 |

---

**Coverage check:** 30+ papers across ACL, NAACL, EMNLP, Findings, NeurIPS, ICLR, ICML, UIST, AAAI, COLING, IEEE TASLP, CIKM, and ACM TOIS, with RecSys- and UMAP-adjacent personalization work (LaMP, LongLaMP, PPlug, PrLM, Persona-Plug) included. No single cited source is more than ~18 months old for claims about current capability; foundational references (MemGPT, Generative Agents, Madotto 2021, LINC) are included for lineage.
