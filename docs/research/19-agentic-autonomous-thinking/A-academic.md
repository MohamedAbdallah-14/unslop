# Agentic Autonomous Thinking — Academic & Scholarly

*Research angle A of category 19: peer-reviewed and pre-print literature on LLM agents that plan, reflect, self-evaluate, and pursue goals with human-like autonomy. Selected for its relevance to Unslop's goal of making AI output and thinking feel more human — that is, deliberative, self-correcting, and goal-directed rather than one-shot and reactive.*

---

## Executive Summary

- **"Agentic autonomous thinking" in the academic literature resolves into five overlapping threads**: (1) *reasoning-and-acting loops* that interleave thought with tool/environment actions (ReAct — Yao et al. ICLR 2023; Toolformer — Schick et al. NeurIPS 2023); (2) *self-reflection and verbal reinforcement* that let an agent critique and improve its own trajectories (Reflexion — Shinn et al. NeurIPS 2023; Self-Refine — Madaan et al. NeurIPS 2023); (3) *search-over-thoughts / deliberation* that replaces greedy decoding with branching, evaluation, and backtracking (Tree of Thoughts — Yao et al. NeurIPS 2023; Self-Consistency — Wang et al. ICLR 2023; Plan-and-Solve — Wang et al. ACL 2023); (4) *social/simulacra agents* that plan days, form opinions, and coordinate with other agents (Generative Agents — Park et al. UIST 2023; Generative Agent Simulations of 1,000 People — Park et al. 2024; CAMEL — Li et al. NeurIPS 2023); and (5) *production-style multi-agent and software engineering systems* that encode human workflows as agent roles (MetaGPT — Hong et al. ICLR 2024; ChatDev — Qian et al. ACL 2024; AutoGen — Wu et al. 2023; SWE-agent — Yang et al. NeurIPS 2024; OpenHands — Wang et al. 2024).
- **The dominant architectural pattern that has emerged by 2025 is a four-module cognitive stack — profile / plan / memory / action — layered on top of a frontier LLM.** Multiple surveys converge on this decomposition: Wang et al. (arXiv 2308.11432, Renmin) organize the field around *construction framework → application → evaluation*; Xi et al. (arXiv 2309.07864, Fudan) use a *brain / perception / action* frame; and recent "foundation agents" surveys (arXiv 2504.01990; Agentic AI survey arXiv 2510.25445) add *self-enhancement / evolution* as a fifth module. Huang et al.'s planning-specific survey (arXiv 2402.02716) sub-categorizes planning into decomposition, multi-plan selection, external modules, reflection, and memory.
- **Deliberation and reflection reliably improve reasoning quality, but with non-trivial caveats.** Self-Consistency yields +6–18 points on math/QA (Wang et al. 2023). Tree of Thoughts raises Game-of-24 from 4% (CoT) to 74% (Yao et al. 2023). Reflexion reaches 91% pass@1 on HumanEval vs. GPT-4's 80% baseline (Shinn et al. 2023). Self-Refine averages ~20% improvement across seven diverse tasks (Madaan et al. 2023). However, 2024–2025 follow-ups show these gains depend heavily on (a) having a reliable external signal for the reflection step, (b) sufficient model scale, and (c) task structure — unreflective over-use of self-critique can *degrade* performance when the evaluator itself is miscalibrated.
- **Metacognition in LLMs is real but selective.** LLMs match or exceed humans on aggregate metacognitive metrics, especially in reduced overconfidence (Steyvers-style studies, 2024); GPT-4 reaches adult-level on higher-order theory-of-mind tasks and surpasses humans on 6th-order inferences (arXiv 2405.18870). At the same time, frontier models fail at *self-modeling* tasks without explicit scratchpads (arXiv 2603.26089), and misjudge their own competence in >20% of cases (KnowRL, arXiv 2510.11407). Training-based methods — ReflectEvo (arXiv 2505.16475), SaySelf (EMNLP 2024), KnowRL (2025) — are converging on "introspection as a learnable objective" rather than a prompting trick.
- **Agentic software-engineering benchmarks have reset the field's yardstick.** SWE-bench (Jimenez et al. ICLR 2024) exposed that frontier LLMs solve <2% of real GitHub issues out of the box; SWE-agent (Yang et al. NeurIPS 2024) lifted this to 12.5% by engineering an *agent-computer interface* (ACI); Devin (Cognition 2024) reported 13.86% end-to-end and, per its 2025 review, now ships production PRs for major banks; OpenHands (Wang et al. 2024) made the stack open. The lesson is architectural: autonomy gains come from environment design and interface ergonomics, not just from stronger base models.
- **The humanization implication (core to Unslop).** Agentic systems are the closest academic analog to how humans actually write and think: they *plan, draft, stop, reflect, revise, and defer.* Three research threads connect directly: (i) Generative Agents and HumanLLM show that cognitive-process simulation produces more believable, human-reading output than end-state style transfer; (ii) Self-Refine and Reflexion give mechanical templates for "think-before-you-send" behaviors (drafting, doubting, revising) that reduce the fluent-but-hollow quality of single-shot LLM text; (iii) HugAgent (arXiv 2510.15144) and the 1,000-Agents paper (Park et al. 2024) argue that authentic human-likeness requires *individualized* reasoning trajectories, not population-average voice — a direct parallel to Unslop's personal-voice goals.
- **Open gaps are acute.** No unified benchmark yet measures "human-likeness of agent reasoning" (as opposed to correctness); reflection amplifies both correct and incorrect intuitions without a reliable detector (Huang et al. 2024); long-horizon memory remains fragile (arXiv 2504.01990); multi-agent debate converges toward consensus that is often wrong (CAMEL and follow-ups note role-flipping, repetition, infinite loops); and the shift to *model-native* agentic reasoning via RL (arXiv 2504.09037; arXiv 2510.16720) risks internalizing failure modes that were previously debuggable as prompt-level pipelines.

---

## Sources

### 1. Generative Agents: Interactive Simulacra of Human Behavior
- **URL**: https://arxiv.org/abs/2304.03442
- **Authors / Org**: Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein (Stanford HCI, Google Research, Google DeepMind)
- **Year / Venue**: UIST 2023 (ACM Symposium on User Interface Software and Technology), October 2023
- **Core claim**: Twenty-five LLM-driven agents equipped with **observation → memory → reflection → planning** produce believable, emergent social behavior in a Sims-style sandbox, including unprompted coordination (a Valentine's Day party spreading through invitations and RSVPs).
- **Techniques mentioned**: Natural-language memory stream with retrieval; periodic synthesis of memories into higher-level *reflections*; day-plan generation and decomposition; inter-agent dialogue via the same LLM.
- **Practical takeaways**: Ablations show **each of observation, planning, and reflection is necessary** for believability — removing any one produces flat or inconsistent behavior. Reflection is the single most important module for complex decision-making. Agents hallucinate embellishments, but plausibly so.
- **Summary**: The paper that operationalized "autonomous LLM agent with human-like daily life" and gave the field its canonical architecture. For Unslop, its deepest lesson is that *authenticity comes from remembering and reflecting*, not from style. A humanizer that simulates human *process* (observe → remember → reflect → plan → speak) will read more human than one that only rewrites end-text.

### 2. Generative Agent Simulations of 1,000 People
- **URL**: https://arxiv.org/abs/2411.10109
- **Authors / Org**: Joon Sung Park and collaborators (Stanford University)
- **Year / Venue**: arXiv, November 2024
- **Core claim**: Agents built from **two-hour qualitative interviews** with 1,052 real participants replicate those individuals' General Social Survey responses at **85% accuracy** — the same rate at which *the humans themselves* replicate their own answers two weeks later.
- **Techniques mentioned**: Interview-to-agent pipeline; prompt-conditioned simulation; Big Five and dictator-game / public-goods-game replications; demographic-only control baseline.
- **Practical takeaways**: Individualized interview data **reduces racial and ideological accuracy bias** relative to demographic-template prompting. This is the strongest empirical evidence to date that "human-like" LLM behavior is personalizable and not just stylistic.
- **Summary**: Directly relevant to any humanization product aiming at a single user's voice. The result — personal-interview conditioning beats demographic-persona prompting at predicting *actual* human reasoning — argues for a pipeline that ingests a user's writing/interview corpus and conditions generation on it, rather than picking a generic "friendly" tone.

### 3. Voyager: An Open-Ended Embodied Agent with Large Language Models
- **URL**: https://arxiv.org/abs/2305.16291
- **Authors / Org**: Guanzhi Wang, Yuke Zhu, Anima Anandkumar et al. (NVIDIA, Caltech, UT Austin, Stanford, UW-Madison)
- **Year / Venue**: arXiv 2023 (often cited as NeurIPS 2023 / TMLR)
- **Core claim**: A GPT-4-driven agent for Minecraft combines an **automatic curriculum**, an **ever-growing skill library of executable code**, and an **iterative prompting loop with self-verification** to achieve 3.3× more unique items discovered, 2.3× longer travel, and **15.3× faster tech-tree progress** than prior SOTA.
- **Techniques mentioned**: Curriculum generation; code-as-skill library with retrieval; environment-feedback self-refinement; blackbox LLM queries (no fine-tuning).
- **Practical takeaways**: Demonstrates that **continual learning without weight updates** is viable when skills are stored as retrievable code. Skills transfer to new worlds zero-shot.
- **Summary**: The canonical "lifelong learning agent" paper. Relevant to Unslop as a structural analog: humans accumulate writing habits as reusable micro-skills ("how I write an apology," "how I disagree politely"); Voyager's library-of-code pattern maps cleanly onto a personal library of stylistic/cognitive operators.

### 4. ReAct: Synergizing Reasoning and Acting in Language Models
- **URL**: https://arxiv.org/abs/2210.03629
- **Authors / Org**: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao (Princeton, Google Brain)
- **Year / Venue**: ICLR 2023 (oral, top 5%)
- **Core claim**: Interleaving **explicit natural-language reasoning traces with task-specific actions** beats either reasoning-only (CoT) or acting-only baselines, especially where external knowledge is needed.
- **Techniques mentioned**: Thought/Action/Observation traces; few-shot trajectories; Wikipedia API tool use; ALFWorld and WebShop environments.
- **Practical takeaways**: ReAct **reduces hallucination** on HotpotQA/Fever via grounded action, and outperforms imitation/RL baselines by **+34% (ALFWorld) and +10% (WebShop)** absolute success. Minimal finetuning required; format transfers across sizes.
- **Summary**: The foundational recipe for "think-act loops" in LLM agents. Its deeper insight — that verbalizing reasoning *in the same stream* as acting — underpins virtually every agentic framework since. For humanization, the ReAct trace format ("I think X. I will do Y. I observe Z. I now think...") is structurally similar to how humans narrate their own reasoning when writing.

### 5. Reflexion: Language Agents with Verbal Reinforcement Learning
- **URL**: https://arxiv.org/abs/2303.11366
- **Authors / Org**: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao (Northeastern, MIT, Princeton)
- **Year / Venue**: NeurIPS 2023
- **Core claim**: Agents can improve **without weight updates** by (a) executing a trajectory, (b) verbally reflecting on task feedback, and (c) storing reflections in an episodic memory buffer that conditions the next attempt. Reaches **91% pass@1 on HumanEval**, surpassing GPT-4's 80% baseline.
- **Techniques mentioned**: Actor–Evaluator–Self-Reflection–Memory decomposition; scalar and free-form feedback; internally-simulated feedback.
- **Practical takeaways**: **Verbal RL** is the dominant academic alternative to RLHF-style weight updates for agent improvement. Works across coding, decision-making, and language reasoning. Critical dependency: a *reliable signal* (unit tests, environment score) to reflect against — pure self-judgment collapses.
- **Summary**: The clearest formalization of "reflect to improve." For Unslop, Reflexion's Actor–Evaluator split is a template for a "draft → self-critique → revise" humanization loop where the evaluator checks specific anti-AI markers and the actor rewrites.

### 6. Self-Refine: Iterative Refinement with Self-Feedback
- **URL**: https://arxiv.org/abs/2303.17651
- **Authors / Org**: Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, Peter Clark (CMU, AI2, UW, NVIDIA, UCSD, Google Research)
- **Year / Venue**: NeurIPS 2023
- **Core claim**: A single LLM acting as **generator, critic, and refiner** iteratively improves its own outputs with **~20% average gain** across 7 tasks (dialog, math, code, sentiment reversal, acronym generation, constrained generation, stylistic rewriting) on GPT-3.5/GPT-4.
- **Techniques mentioned**: Feedback/Refine loop; no supervised data, no RL, no extra model; few-shot prompts for feedback-and-refine pairs.
- **Practical takeaways**: Works best on *stylistic* and *preference* tasks; works least on *math* where errors compound. Preferred by humans and automatic metrics over one-shot generation.
- **Summary**: The most direct template for humanization-by-iteration in the academic literature. The result that stylistic refinement benefits more than mathematical refinement is important: humanization is exactly the task class Self-Refine is strong on, and it validates the "redraft, don't regenerate" pattern.

### 7. Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **URL**: https://arxiv.org/abs/2305.10601
- **Authors / Org**: Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan (Princeton, Google DeepMind)
- **Year / Venue**: NeurIPS 2023
- **Core claim**: Replacing token-level greedy decoding with **search over coherent "thought" units** — with LLM self-evaluation of intermediate states and backtracking — raises Game-of-24 from **4% (CoT) to 74%** with GPT-4.
- **Techniques mentioned**: Thought decomposition; BFS/DFS search; LLM value/vote evaluators; pruning and backtracking; applied to Game of 24, Creative Writing, Mini Crosswords.
- **Practical takeaways**: Deliberation works when (a) a problem has discrete subgoals, (b) the LLM can reliably evaluate partial progress. Otherwise search overhead swamps gains.
- **Summary**: Establishes "search over thoughts" as a distinct regime from sampling (self-consistency) and critique (self-refine). Humanization doesn't need Game-of-24-scale search, but ToT's *evaluator-driven pruning of bad drafts* transfers: a humanizer can branch on stylistic options and prune those flagged as AI-coded.

### 8. Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **URL**: https://arxiv.org/abs/2203.11171
- **Authors / Org**: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou (Google Research, Brain Team)
- **Year / Venue**: ICLR 2023
- **Core claim**: Sampling **multiple diverse CoT trajectories** and taking a **majority vote over final answers** improves GPT-3/PaLM accuracy by **+17.9% on GSM8K, +11.0% on SVAMP, +12.2% on AQuA, +6.4% on StrategyQA**.
- **Techniques mentioned**: Temperature sampling; answer-marginalization voting; CoT prompting baseline.
- **Practical takeaways**: The simplest, most reliable reasoning-quality boost for any LLM. Cost scales linearly in samples. Benefits plateau after ~40 samples.
- **Summary**: The baseline every subsequent reasoning-loop paper must beat. Its conceptual contribution — *many plausible paths, one convergent answer* — is also how humans double-check their own reasoning, making it a candidate primitive for a "cognitive humanization" layer that narrates multiple hypotheses before committing.

### 9. Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models
- **URL**: https://arxiv.org/abs/2305.04091
- **Authors / Org**: Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim (SMU, SUTD, East China Normal)
- **Year / Venue**: ACL 2023
- **Core claim**: A two-stage zero-shot prompt — first **"devise a plan,"** then **"carry out the subtasks"** — beats "Let's think step by step" on all 10 tested reasoning datasets; PS+ (with explicit anti-calculation-error instructions) approaches 8-shot CoT performance.
- **Techniques mentioned**: Zero-shot plan generation; subtask execution; error-class-specific instruction augmentation (calculation, missing-step, semantic).
- **Practical takeaways**: Explicit planning is a cheap, consistent lift over implicit step-by-step. It compounds with self-consistency.
- **Summary**: The minimal example of "agentic" behavior inside a single prompt: *plan, then execute.* Relevant to humanization as a template for forcing the model to *commit to a rhetorical plan* before drafting, which tends to reduce the aimless discourse-marker padding typical of single-shot LLM text.

### 10. Toolformer: Language Models Can Teach Themselves to Use Tools
- **URL**: https://arxiv.org/abs/2302.04761
- **Authors / Org**: Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom (Meta AI Research, Universitat Pompeu Fabra)
- **Year / Venue**: NeurIPS 2023 (oral)
- **Core claim**: An LLM can **self-supervise its own tool-use training** by sampling API calls, keeping only those that reduce downstream loss — producing a model that autonomously decides when to call calculators, QA, search, translation, or calendars.
- **Techniques mentioned**: Self-supervised API-call filtering; token-level insertion; few demonstrations per API.
- **Practical takeaways**: Often matches far larger models without losing core LM ability. Establishes tool-use as a *capability of the base model*, not a pipeline around it.
- **Summary**: Foundational for the "tool-using agent" branch. Relevant to Unslop if humanization is reframed as a tool call (e.g., a "style-guard" tool the model learns to invoke when it drafts) rather than a post-processing step.

### 11. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
- **URL**: https://arxiv.org/abs/2405.15793
- **Authors / Org**: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press (Princeton NLP / PLI)
- **Year / Venue**: NeurIPS 2024
- **Core claim**: Designing a **custom agent-computer interface (ACI)** — LM-friendly commands for file viewing/editing, with guardrails and feedback — lifts SWE-bench pass@1 to **12.5%** and HumanEvalFix to **87.7%**, far above agents given raw shell access.
- **Techniques mentioned**: ACI design (file viewer, linter-aware editor, search); error feedback; command guardrails.
- **Practical takeaways**: Autonomy quality is **dominated by interface design**, not just the base model. Poorly designed tools cause catastrophic agent confusion even with GPT-4.
- **Summary**: The most important "environment engineering" paper of 2024. Its thesis — agents need curated affordances, not just tools — is directly transferable to humanization systems: give the model a small set of *well-shaped* editing tools (e.g., "soften," "add hedge," "break up sentence") rather than free rewriting.

### 12. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **URL**: https://arxiv.org/abs/2310.06770
- **Authors / Org**: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan (Princeton)
- **Year / Venue**: ICLR 2024
- **Core claim**: A benchmark of **2,294 real GitHub issues** from 12 popular Python repos evaluates whether LMs can produce a patch that passes the repo's *actual* unit tests. Best baseline (Claude 2): **1.96%**.
- **Techniques mentioned**: Issue + codebase + test pipeline; retrieval-augmented evaluation; SWE-Llama fine-tune.
- **Practical takeaways**: Reset the yardstick for "useful" LLM coding. Brutally exposed that HumanEval-level performance does not transfer to production engineering. Drove the subsequent wave of ACI / agentic engineering.
- **Summary**: Not an agent paper per se, but the evaluative foundation that made the agentic-software-engineering wave legible. Relevant to Unslop as a methodological template: benchmark humanization against *real human text + real detectors + real tasks*, not sanitized style-transfer suites.

### 13. OpenHands (née OpenDevin): An Open Platform for AI Software Developers as Generalist Agents
- **URL**: https://arxiv.org/abs/2407.16741
- **Authors / Org**: Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, et al. (UIUC, CMU, Yale, All Hands AI, others)
- **Year / Venue**: arXiv, July 2024 (ICLR 2025)
- **Core claim**: An **open, permissive-licensed platform** for building software-developer agents that write code, use CLIs, and browse the web, with sandboxed execution, multi-agent coordination, and 15 built-in evaluation tasks (incl. SWE-bench, WebArena).
- **Techniques mentioned**: Event-driven agent architecture; shared action/observation types; MCP-style tool integration; docker sandboxing.
- **Practical takeaways**: Provides the first *open* agent platform with production-grade evaluation harnesses. Broke the dependency on closed systems (Devin) for reproducible research.
- **Summary**: Infrastructure paper that made academic work on generalist coding agents tractable. For humanization, its lesson is organizational: design the humanizer as an *agent runtime* with events, tools, and sandboxes rather than a prompt.

### 14. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework
- **URL**: https://arxiv.org/abs/2308.00352
- **Authors / Org**: Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Jürgen Schmidhuber (DeepWisdom, KAUST, others)
- **Year / Venue**: ICLR 2024 (oral)
- **Core claim**: Encoding human **Standard Operating Procedures (SOPs)** as prompt sequences over specialized roles (PM, Architect, Engineer, QA) reduces cascading hallucinations in multi-agent LLM systems. Reports **85.9% HumanEval pass@1** (+28.2% over GPT-4 solo) and **87.7% MBPP**.
- **Techniques mentioned**: Role-specialized prompts; structured message schemas; publish-subscribe message pool; executable feedback loops.
- **Practical takeaways**: Structured workflows outperform free-form agent dialogue; **pub-sub messaging prevents redundant cross-talk**; executable feedback adds +4–5%. Human revision cost drops from 2.25 to 0.83 on average.
- **Summary**: The strongest argument in the literature for *procedural* (SOP-shaped) agent coordination over emergent dialogue. For humanization, MetaGPT's pattern — specialized "roles" (drafter, critic, voice-matcher) with schema-defined handoffs — is a concrete template for a multi-agent humanizer.

### 15. ChatDev: Communicative Agents for Software Development
- **URL**: https://arxiv.org/abs/2307.07924
- **Authors / Org**: Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, Maosong Sun (Tsinghua, BUPT, Brown, DRC AI Lab, BUAA)
- **Year / Venue**: ACL 2024 (Long Paper)
- **Core claim**: A **chat-chain** of role-playing agents covering design, coding, and testing, coordinated by **"communicative dehallucination,"** demonstrates that natural language alone can orchestrate end-to-end software production among agents.
- **Techniques mentioned**: Chat chain (phase-sequenced dialogues); communicative dehallucination (request-for-clarification protocol); unified language-as-interface across phases.
- **Practical takeaways**: Dialogue-driven orchestration is viable but requires explicit hallucination-mitigation protocols. Complements MetaGPT's SOP-driven view.
- **Summary**: Establishes language-as-unifying-medium for multi-agent workflows. Useful counterpoint to MetaGPT: where MetaGPT prescribes schema, ChatDev prescribes *conversational patterns*. For humanization, the communicative-dehallucination protocol is directly reusable as a "ask before committing" check in draft pipelines.

### 16. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **URL**: https://arxiv.org/abs/2308.08155
- **Authors / Org**: Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W. White, Doug Burger, Chi Wang (Microsoft Research, Penn State, UW)
- **Year / Venue**: arXiv 2023; ICLR 2024 LLM Agents Workshop **Best Paper**
- **Core claim**: A generic framework of **conversable, customizable agents** combining LLMs, humans, and tools supports flexible patterns (joint chat, hierarchical chat) and lets developers program behavior in natural language *and* code.
- **Techniques mentioned**: ConversableAgent abstraction; AssistantAgent / UserProxyAgent; function/code-execution integration; group chat manager.
- **Practical takeaways**: Effective across math, coding, QA, operations research, online decision-making, entertainment. Has become the most-adopted open agent framework in industry.
- **Summary**: The pragmatic, framework-level contribution that decoupled agent *capabilities* from agent *topology*. Key for Unslop as a build-time choice: AutoGen-style conversable agents let a humanizer combine a drafter, a detector, and a user-proxy in configurable topologies without hard-coding the workflow.

### 17. CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society
- **URL**: https://arxiv.org/abs/2303.17760
- **Authors / Org**: Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, Bernard Ghanem (KAUST)
- **Year / Venue**: NeurIPS 2023
- **Core claim**: **Inception prompting** and role-playing let two LLM agents autonomously cooperate on a task with minimal human input — and produce **large-scale conversational data** for studying multi-agent cognition.
- **Techniques mentioned**: Inception prompts (assistant/user role seeds); task specifier; conversational-data generation pipeline; catalogue of multi-agent failure modes (role flipping, instruction repetition, flake replies, infinite loops).
- **Practical takeaways**: First systematic study of *how agent societies fail*, and a source of training data for subsequent agent work.
- **Summary**: Laid the methodological groundwork for studying LLM agent *sociology*. Humanization relevance: its taxonomy of dialogue failure modes (role flipping, loops) is a useful checklist for any multi-agent humanization rig.

### 18. The Rise and Potential of Large Language Model Based Agents: A Survey
- **URL**: https://arxiv.org/abs/2309.07864
- **Authors / Org**: Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, Rui Zheng, Xiaoran Fan, Xijie Huang, Zhiyuan Zhang, Li Du, Zhi Zhou, Shihan Dou, Jun Zhao, Ruihao Gong, Hao Fu, Tao Gui, Qi Zhang, Xuanjing Huang (Fudan NLP, ByteDance)
- **Year / Venue**: arXiv 2023; Science China Information Sciences 2025; **>1,500 citations**
- **Core claim**: LLM agents are best described by a **Brain–Perception–Action** triad: brain = LLM (with memory, knowledge, reasoning, planning), perception = multimodal inputs, action = text / tool / embodied output.
- **Techniques mentioned**: Single-agent, multi-agent, and human-agent scenarios; case catalog (AutoGPT, HuggingGPT, WebGPT, Generative Agents, CAMEL, AgentVerse, Copilot).
- **Practical takeaways**: The most influential survey-level vocabulary in the field. Essential reading for any project classifying its own system within the literature.
- **Summary**: Canonical reference for the "agentic LLM" taxonomy. Its *brain/perception/action* decomposition is a durable design frame for any humanization-agent architecture.

### 19. A Survey on Large Language Model based Autonomous Agents
- **URL**: https://arxiv.org/abs/2308.11432
- **Authors / Org**: Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei, Ji-Rong Wen (Renmin University, Gaoling School of AI)
- **Year / Venue**: arXiv 2023; Frontiers of Computer Science 2024
- **Core claim**: LLM agents are analyzable by **construction framework → applications → evaluation**; a unified construction framework covers profile, memory, planning, and action modules across social-science, natural-science, and engineering deployments.
- **Techniques mentioned**: Profile / memory / planning / action taxonomy; agent-type catalog (tool, simulation, game, embodied, web, assistant).
- **Practical takeaways**: Most practically useful survey for "what module should I build next" questions. Tracks growth from 2021–2023.
- **Summary**: Complements Xi et al. with an engineering lens. Together, the two surveys define the field's shared vocabulary. Unslop architecture should explicitly map onto the profile/memory/planning/action frame.

### 20. Understanding the Planning of LLM Agents: A Survey
- **URL**: https://arxiv.org/abs/2402.02716
- **Authors / Org**: Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Han, Yasheng Wang, Defu Lian, Enhong Chen, Hongsen Wu, Hai Wang, Yanfei Jiang, Jianhang Shan, Feihong Han (USTC, Huawei Noah's Ark Lab)
- **Year / Venue**: arXiv, February 2024
- **Core claim**: LLM-agent planning subdivides into five categories: **task decomposition, multi-plan selection, external module integration, reflection, and memory**.
- **Techniques mentioned**: Decomposition-first vs interleaved decomposition; heuristic search over plans; PDDL-style external planners; reflection loops; retrieval-augmented memory.
- **Practical takeaways**: First dedicated planning taxonomy for LLM agents. Makes explicit that *reflection and memory are planning substrates*, not separate concerns.
- **Summary**: The reference for anyone designing the planning layer of an agent. Its five categories map almost 1-to-1 onto the design decisions Unslop faces (break the humanization task into steps? sample multiple drafts? call detectors? reflect on output? remember user style?).

### 21. A Survey of Frontiers in LLM Reasoning: Inference Scaling, Learning to Reason, and Agentic Systems
- **URL**: https://arxiv.org/abs/2504.09037
- **Authors / Org**: collaborative survey (multiple institutions; see arXiv)
- **Year / Venue**: arXiv, April 2025 (v2)
- **Core claim**: Reasoning progress in LLMs splits along two axes: **regime** (inference-time vs training-time) and **architecture** (standalone LLM vs agentic compound system). A **shift from pipeline orchestration to model-native agentic reasoning via RL** is the dominant 2024–2025 trend.
- **Techniques mentioned**: Inference scaling (self-consistency, best-of-N, ToT); verifier-augmented search; learning-to-reason via RL (o1-style); agentic compound systems with tools and multi-agent collaboration.
- **Practical takeaways**: Recommended synthesis for understanding how *pipeline* humanization pipelines may be subsumed by *model-native* ones as capabilities internalize.
- **Summary**: The clearest map of where the field is going. Tells a humanization product that bets heavily on external orchestration to also plan for a future where the orchestration collapses into model weights.

### 22. Advances and Challenges in Foundation Agents: From Brain-Inspired Intelligence to Evolutionary, Collaborative, and Safe Systems
- **URL**: https://arxiv.org/abs/2504.01990
- **Authors / Org**: multi-institution survey (see arXiv)
- **Year / Venue**: arXiv, March 2025 (v2)
- **Core claim**: A **brain-inspired modular agent architecture** — perception, cognition (memory, world model, reward, goals, emotion), action — subsumes current LLM-agent stacks and provides a principled frame for four open topics: modular foundation, self-enhancement, multi-agent systems, safety.
- **Techniques mentioned**: Multimodal encoders; hierarchical memory; hybrid symbolic-neural world models; automated capability refinement; collective intelligence.
- **Practical takeaways**: Extends earlier taxonomies by treating *self-enhancement* (autonomous capability refinement) as a first-class module.
- **Summary**: The 2025 "grand-unified-theory" survey for foundation agents. Relevant to Unslop as scaffolding for framing humanization as a *goal-and-emotion-module* problem rather than a pure language problem.

### 23. Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions
- **URL**: https://arxiv.org/abs/2510.25445
- **Authors / Org**: systematic review authors (see arXiv; also in *Artificial Intelligence Review*, Springer Nature, 2025)
- **Year / Venue**: arXiv, October 2025; *AI Review* 2025
- **Core claim**: Across 90 studies (2018–2025), agentic AI splits into **symbolic/classical** (algorithmic planning, persistent state, safety-critical domains) and **neural/generative** (stochastic generation, prompt orchestration, adaptive domains). Three intelligence dimensions: **internal** (long-horizon planning/reflection/memory), **external tool use**, **environment interaction**.
- **Techniques mentioned**: Dual-paradigm taxonomy; intelligence-dimension scoring; domain case studies (healthcare, finance).
- **Practical takeaways**: Names the dual paradigm explicitly and provides the first peer-reviewed (Springer) meta-analysis of the field.
- **Summary**: Useful for legitimating agentic-AI framing in academic or policy contexts; its emphasis on *internal intelligence* as including reflection and memory reinforces the humanization-relevant parts of the stack.

### 24. Large Language Models Have Intrinsic Meta-Cognition, but Need a Good Lens (AutoMeco)
- **URL**: https://arxiv.org/abs/2506.08410
- **Authors / Org**: AutoMeco authors (see arXiv)
- **Year / Venue**: arXiv 2025; EMNLP 2025 main
- **Core claim**: LLMs possess **intrinsic metacognition** — internal signals (perplexity, entropy, step-level confidence) that correlate with correctness — but require good *lenses* (measurement methods) to expose it. Proposes **AutoMeco** benchmark and **MIRA** (training-free step-level Markovian intrinsic-reward adjustment).
- **Techniques mentioned**: Lens benchmarking; step-level metacognitive signals; training-free reward-shaping.
- **Practical takeaways**: Provides evidence that self-evaluation is *already present* in base models and the job is to surface it, not to train from scratch.
- **Summary**: Rigorous empirical paper grounding the "models know when they're wrong" intuition. For humanization, suggests that base-model internals already carry "this phrasing feels off" signal that a humanizer can extract rather than brute-force rewrite.

### 25. ReflectEvo: Improving Meta Introspection of Small LLMs by Learning Self-Reflection
- **URL**: https://arxiv.org/abs/2505.16475
- **Authors / Org**: ReflectEvo authors (see arXiv)
- **Year / Venue**: arXiv, May 2025
- **Core claim**: A **self-evolving reflection-learning pipeline** using a 460k-entry self-generated reflection dataset raises Llama-3 on BIG-bench from 52.4% → **71.2%** and Mistral 44.4% → **71.1%** — *without* distillation from a larger model or fine-grained human annotation.
- **Techniques mentioned**: Iterative reflection generation; self-training; ReflectEvo-460k dataset.
- **Practical takeaways**: Shows metacognition can be *trained into* small open models via self-supervised reflection alone. Strong evidence that reflection is a transferable skill, not a frontier-scale emergent property.
- **Summary**: Important counterweight to "reflection only works on GPT-4-scale." For Unslop on-device or OSS deployments, this is the template for installing a reflection capability in a small model.

### 26. LLMs Achieve Adult Human Performance on Higher-Order Theory of Mind Tasks
- **URL**: https://arxiv.org/abs/2405.18870
- **Authors / Org**: Winnie Street, John Oliver Siy, Geoff Keeling, Adrien Baranes, Benjamin Barnett, Michael McKibben, Tatenda Kanyere, Alison Lentz, Robin I. M. Dunbar, Blaise Agüera y Arcas (Google DeepMind, Google Research, Oxford, University of Warwick, collaborators)
- **Year / Venue**: arXiv, May 2024
- **Core claim**: GPT-4 reaches **adult-level or better** on higher-order ToM (recursive "I think that you believe that she knows…" up to 6th order); Flan-PaLM reaches near-adult. Results depend on an interplay of model size and finetuning.
- **Techniques mentioned**: MoToMQA benchmark; 2nd–6th-order ToM problems; adult human baseline.
- **Practical takeaways**: Cognitive capability — not just stylistic mimicry — is within reach of frontier LLMs on ToM. A prerequisite for any "authentically human-reasoning" agent.
- **Summary**: The strongest empirical claim to date that LLMs can reason *about* minds at human level. Unslop relevance: human-like text increasingly requires modeling of the reader's likely beliefs and updates, which this paper shows is feasible.

### 27. HumanLLM: Benchmarking and Improving LLM Anthropomorphism via Human Cognitive Patterns
- **URL**: https://arxiv.org/abs/2601.10198
- **Authors / Org**: HumanLLM authors (see arXiv)
- **Year / Venue**: arXiv, January 2026
- **Core claim**: Authentic anthropomorphism requires **cognitive modeling**, not behavioral mimicry: HumanLLM constructs 244 interacting psychological patterns from ~12,000 papers, and **HumanLLM-8B outperforms Qwen3-32B** on multi-pattern dynamics.
- **Techniques mentioned**: Psychology-pattern taxonomy; causal-force simulation; small-model fine-tuning on pattern traces.
- **Practical takeaways**: Parameter count matters less than *proper cognitive alignment*. Cognitive process simulation beats output-style mimicry for anthropomorphic quality.
- **Summary**: Directly parallels Unslop's thesis. Argues against style-transfer-only humanization and in favor of simulating the *psychological processes* behind human output.

### 28. HugAgent: Benchmarking LLMs for Simulation of Individualized Human Reasoning
- **URL**: https://arxiv.org/abs/2510.15144
- **Authors / Org**: HugAgent authors (see arXiv)
- **Year / Venue**: arXiv, October 2025
- **Core claim**: Current LLM simulation of humans collapses into an **"average voice"** that erases individuality; HugAgent shifts evaluation from *population-level consensus* to **capturing how specific individuals reason and update beliefs in novel scenarios**.
- **Techniques mentioned**: Individualized-reasoning benchmark; belief-update traces; per-subject evaluation.
- **Practical takeaways**: Establishes "averaged vs individualized" as the new axis for human-likeness evaluation. Complements the Park 2024 1,000-agents result empirically.
- **Summary**: The clearest academic articulation of the gap between "sounds human" and "sounds like *this* human." Critical reference for Unslop's personal-voice direction.

### 29. KnowRL: Teaching Language Models to Know What They Know
- **URL**: https://arxiv.org/abs/2510.11407
- **Authors / Org**: KnowRL authors (see arXiv)
- **Year / Venue**: arXiv, October 2025
- **Core claim**: Even leading LLMs misjudge their competence in **>20% of instances**. A **reinforcement-learning introspection method** (classifying tasks as feasible/infeasible; rewarding stable self-assessments) yields up to **+28% accuracy / +12% F1** on LLaMA-3.1-8B and Qwen-2.5-7B.
- **Techniques mentioned**: Self-classification of task feasibility; consensus-based reward; self-generated training data.
- **Practical takeaways**: Self-knowledge is trainable and measurable. Moves metacognition out of prompt-level tricks into parameter-level capability.
- **Summary**: Canonical 2025 example of the "model-native self-evaluation" shift forecast in the reasoning-frontier survey (arXiv 2504.09037). For humanization, a KnowRL-style introspection head can gate rewrite attempts (don't revise when you already know it's fine; do revise when you suspect AI-coded slop).

### 30. SaySelf: Teaching LLMs to Express Confidence with Self-Reflective Rationales
- **URL**: https://aclanthology.org/2024.emnlp-main.343/
- **Authors / Org**: SaySelf authors (see ACL)
- **Year / Venue**: EMNLP 2024 (Main)
- **Core claim**: A training framework that makes LLMs express **fine-grained confidence** accompanied by **self-reflective rationales** (not just numbers), calibrated via RL reward functions that penalize overconfidence.
- **Techniques mentioned**: Confidence-elicitation prompting; rationale-aware reward; calibration metrics.
- **Practical takeaways**: Shows that expressed confidence is not only calibratable but can be *explained* in natural language — closer to how humans hedge and qualify in text.
- **Summary**: The most direct bridge between agent metacognition and humanized text. Hedging and explicit uncertainty are among the most-cited markers of authentically human writing; SaySelf operationalizes them as a training objective.

---

## Key Techniques / Patterns

The academic literature on agentic autonomous thinking converges on a reusable stack of cognitive operators:

1. **Reason–Act interleaving (ReAct).** Alternate explicit natural-language thoughts with tool or environment actions inside one decoding stream. The default backbone of most modern agents.
2. **Search over thoughts (Tree of Thoughts, Plan-and-Solve).** Branch on candidate plans/thoughts, evaluate partial progress, backtrack. Expensive but transformative on deliberation-heavy tasks.
3. **Sample-and-aggregate (Self-Consistency, Best-of-N).** Generate many independent reasoning paths, vote or verify. The cheapest reliable improvement available.
4. **Verbal reflection with episodic memory (Reflexion).** Execute → critique → store → retry. Requires a reliable feedback signal (tests, scores) to avoid collapse.
5. **Self-critique and iterative refine (Self-Refine).** Single LLM as generator + critic + reviser. Strongest on stylistic and preference tasks.
6. **Tool use as a first-class skill (Toolformer; ACI designs in SWE-agent).** Model learns *when* to call tools, guarded by a curated interface. Interface ergonomics dominate raw-tool-access in quality.
7. **Role-specialized multi-agent with SOPs (MetaGPT).** Pub-sub message pool; schema-typed handoffs; executable-feedback loops. Reduces cross-talk vs. free dialogue.
8. **Communicative multi-agent (ChatDev, CAMEL, AutoGen).** Dialogue-driven coordination with explicit anti-failure protocols (inception prompts, dehallucination requests). Flexible but failure-prone.
9. **Simulated human cognition (Generative Agents, HumanLLM, HugAgent).** Observation → memory → reflection → planning pipeline; cognitive-pattern simulation; interview-conditioned individualization.
10. **Skill libraries with continual learning (Voyager).** Store verified behaviors as retrievable code; accumulate across episodes; transfer across tasks/worlds.
11. **Metacognitive gating (AutoMeco, KnowRL, SaySelf).** Use intrinsic signals (perplexity, entropy, trained confidence heads) to decide when to act, reflect, or defer.
12. **Model-native agentic reasoning (o1-style, RL-trained loops).** Internalize plan/reflect/verify within weights rather than prompting. The 2024–2025 frontier trend per the Survey of Frontiers in LLM Reasoning.

---

## Notable Quotes

> "Our architecture remembers, reflects, and plans … ablating each of these components significantly degrades believability."
> — *Park et al., Generative Agents, UIST 2023*

> "Generative agents replicate participants' responses on the General Social Survey 85% as accurately as participants replicate their own answers two weeks apart."
> — *Park et al., Generative Agent Simulations of 1,000 People, arXiv 2411.10109 (Abstract)*

> "ReAct outperforms several state-of-the-art baselines … despite adding only one or two in-context examples."
> — *Yao et al., ReAct, ICLR 2023 (Abstract)*

> "Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials."
> — *Shinn et al., Reflexion, NeurIPS 2023 (Abstract)*

> "Game of 24 is a difficult mathematical reasoning task where GPT-4 with chain-of-thought prompting only solves 4% of tasks, whereas our method achieves a success rate of 74%."
> — *Yao et al., Tree of Thoughts, NeurIPS 2023 (Abstract)*

> "Iterative refinement allows large language models to improve their outputs by ~20% on average across seven tasks, without any supervised training data, reinforcement learning, or additional model."
> — *Madaan et al., Self-Refine, NeurIPS 2023 (Abstract)*

> "We design a simple ACI for the LM to view, edit, and execute code … SWE-agent achieves a 12.5% pass rate on SWE-bench, far above all prior LM baselines."
> — *Yang et al., SWE-agent, NeurIPS 2024 (Abstract)*

> "Standard Operating Procedures encoded into prompt sequences streamline workflows and enable agents with human-like domain expertise to verify intermediate results and mitigate errors."
> — *Hong et al., MetaGPT, ICLR 2024 (Abstract)*

> "Authentic anthropomorphism requires cognitive modeling — simulating not just what humans do, but the psychological processes generating those behaviors."
> — *HumanLLM, arXiv 2601.10198 (Abstract)*

> "LLMs tend to collapse into an 'average voice,' erasing the individuality of personal histories, beliefs, and reasoning styles."
> — *HugAgent, arXiv 2510.15144 (Introduction)*

> "Even leading LLMs misjudge their competence in more than one out of five instances … introspection via reinforcement improves self-knowledge by up to 28%."
> — *KnowRL, arXiv 2510.11407 (Abstract)*

---

## Emerging Trends

- **From pipelines to model-native agency.** The Survey of Frontiers in LLM Reasoning (arXiv 2504.09037) and *Agentic Reasoning for LLMs* (arXiv 2601.12538) document a shift from externally orchestrated plan/reflect/tool pipelines toward RL-trained, in-weights agentic reasoning (o1-family, DeepSeek-R1-family). Expect 2026+ benchmarks to distinguish *what the base model does alone* from *what the scaffold adds.*
- **Environment / interface engineering as the key quality lever.** SWE-agent, OpenHands, and Agent-S all demonstrate that well-shaped agent-computer interfaces beat raw tool access by double-digit points. The message is general: the next-generation humanizer will likely have a small set of curated editing affordances, not a free-form rewrite call.
- **Individualized vs averaged simulation.** Park et al. 2024 and HugAgent 2025 move the field from "simulate a persona" to "simulate *this specific person*." Interview-data conditioning and per-subject belief-update traces are the emerging standards.
- **Reflection as a trainable capability.** ReflectEvo, KnowRL, and SaySelf show that metacognition is not a frontier-scale emergent trait — it can be distilled/trained into 7B–8B models. OSS/on-device humanizers become viable.
- **Multi-agent SOPs winning over open dialogue.** MetaGPT's pub-sub + role-schema + executable-feedback architecture has begun to dominate free-form multi-agent dialogue (CAMEL, ChatDev) in production settings. Expect future frameworks (AutoGen, CrewAI, LangGraph) to standardize on typed handoffs.
- **Cognitive-architecture surveys consolidating vocabulary.** Wang 2023, Xi 2023, Huang 2024, Foundation Agents 2025, Agentic AI Survey 2025 now share a core decomposition — profile/memory/planning/action + perception — and two live debates: (a) is *emotion/goal* a first-class module? (b) is *self-enhancement* separable from planning?
- **Metacognition meets humanization.** SaySelf-style confidence rationales and AutoMeco-style intrinsic signals are bridging "agent self-knowledge" and "human-like hedging." This convergence will likely produce, by 2026–2027, humanizers that *decide when to hedge* rather than apply hedge templates globally.
- **Safety and alignment for agents.** The Foundation Agents survey and the Agentic AI Survey both flag safety-and-alignment as an underdeveloped fifth module. Expect a wave of red-teaming work on *agent* (not just LLM) behavior.

---

## Open Questions / Gaps

- **No benchmark for "human-likeness of agent reasoning."** SWE-bench measures task success; HumanEval measures code correctness; ToT/CoT benchmarks measure math. Nothing in the mainstream measures whether an agent's *trajectory* reads as something a human would plausibly produce — the central gap for Unslop-style products.
- **Reflection amplifies miscalibrated confidence.** Without a reliable external signal (tests, simulation, retrieval), self-critique can reinforce errors (Huang 2024; KnowRL 2025). Research on *when to reflect* is nascent.
- **Long-horizon memory remains brittle.** Generative Agents use a reflection-synthesis shortcut; OpenHands relies on scrollback; Voyager stores skills as code. No consensus architecture yet balances recall, compression, and drift.
- **Multi-agent consensus is biased toward consensus, not truth.** CAMEL, ChatDev, and subsequent work all note convergence to confident-but-wrong agreement. Debate-style rigs help sometimes but introduce their own dynamics.
- **Individualized-reasoning data is scarce.** Park et al. 2024 required 2-hour interviews; HugAgent hand-curates belief updates. No scalable source of authentic individualized reasoning traces exists at population scale.
- **Evaluation of metacognition is lens-dependent.** AutoMeco shows that different "lenses" on the same model give different metacognitive scores. The field lacks a canonical measurement.
- **Agent safety research trails agent capability research.** Most frameworks (AutoGen, OpenHands, MetaGPT) sandbox execution but do not model *goal-level* safety. Foundation Agents 2025 flags this as the largest open area.
- **Humanization × agent autonomy is under-theorized.** Only a handful of papers (HumanLLM, HugAgent, the 1,000-Agents paper, SaySelf-adjacent work) directly connect *agent cognitive architecture* to *authentically human output*. The synthesis that Unslop targets — an agent that *thinks* human, not one that *sounds* human — is a genuinely open research direction as of 2026.

---

## References

1. https://arxiv.org/abs/2304.03442 — Park et al., *Generative Agents: Interactive Simulacra of Human Behavior* (UIST 2023)
2. https://arxiv.org/abs/2411.10109 — Park et al., *Generative Agent Simulations of 1,000 People* (arXiv 2024)
3. https://arxiv.org/abs/2305.16291 — Wang et al., *Voyager: An Open-Ended Embodied Agent with Large Language Models* (arXiv 2023)
4. https://arxiv.org/abs/2210.03629 — Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (ICLR 2023)
5. https://arxiv.org/abs/2303.11366 — Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning* (NeurIPS 2023)
6. https://arxiv.org/abs/2303.17651 — Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback* (NeurIPS 2023)
7. https://arxiv.org/abs/2305.10601 — Yao et al., *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* (NeurIPS 2023)
8. https://arxiv.org/abs/2203.11171 — Wang et al., *Self-Consistency Improves Chain of Thought Reasoning in Language Models* (ICLR 2023)
9. https://arxiv.org/abs/2305.04091 — Wang et al., *Plan-and-Solve Prompting* (ACL 2023)
10. https://arxiv.org/abs/2302.04761 — Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools* (NeurIPS 2023, oral)
11. https://arxiv.org/abs/2405.15793 — Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* (NeurIPS 2024)
12. https://arxiv.org/abs/2310.06770 — Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (ICLR 2024)
13. https://arxiv.org/abs/2407.16741 — Wang et al., *OpenHands: An Open Platform for AI Software Developers as Generalist Agents* (arXiv 2024)
14. https://arxiv.org/abs/2308.00352 — Hong et al., *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (ICLR 2024, oral)
15. https://arxiv.org/abs/2307.07924 — Qian et al., *ChatDev: Communicative Agents for Software Development* (ACL 2024)
16. https://arxiv.org/abs/2308.08155 — Wu et al., *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation* (arXiv 2023)
17. https://arxiv.org/abs/2303.17760 — Li et al., *CAMEL: Communicative Agents for "Mind" Exploration of LLM Society* (NeurIPS 2023)
18. https://arxiv.org/abs/2309.07864 — Xi et al., *The Rise and Potential of Large Language Model Based Agents: A Survey* (arXiv 2023 / Sci China IS 2025)
19. https://arxiv.org/abs/2308.11432 — Wang et al., *A Survey on Large Language Model based Autonomous Agents* (arXiv 2023 / FCS 2024)
20. https://arxiv.org/abs/2402.02716 — Huang et al., *Understanding the Planning of LLM Agents: A Survey* (arXiv 2024)
21. https://arxiv.org/abs/2504.09037 — *A Survey of Frontiers in LLM Reasoning* (arXiv 2025)
22. https://arxiv.org/abs/2504.01990 — *Advances and Challenges in Foundation Agents* (arXiv 2025)
23. https://arxiv.org/abs/2510.25445 — *Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions* (arXiv 2025 / AI Review 2025)
24. https://arxiv.org/abs/2506.08410 — *AutoMeco: LLMs Have Intrinsic Meta-Cognition, but Need a Good Lens* (EMNLP 2025)
25. https://arxiv.org/abs/2505.16475 — *ReflectEvo: Improving Meta Introspection of Small LLMs by Learning Self-Reflection* (arXiv 2025)
26. https://arxiv.org/abs/2405.18870 — Street et al., *LLMs Achieve Adult Human Performance on Higher-Order Theory of Mind Tasks* (arXiv 2024)
27. https://arxiv.org/abs/2601.10198 — *HumanLLM: Benchmarking and Improving LLM Anthropomorphism via Human Cognitive Patterns* (arXiv 2026)
28. https://arxiv.org/abs/2510.15144 — *HugAgent: Benchmarking LLMs for Simulation of Individualized Human Reasoning* (arXiv 2025)
29. https://arxiv.org/abs/2510.11407 — *KnowRL: Teaching Language Models to Know What They Know* (arXiv 2025)
30. https://aclanthology.org/2024.emnlp-main.343/ — *SaySelf: Teaching LLMs to Express Confidence with Self-Reflective Rationales* (EMNLP 2024)
