# Chain-of-Thought & Reasoning — Angle C: Open-Source & GitHub

> **Project context:** Humanizing the output and thinking of AI models.
> **Angle scope:** Open-source repositories that expose, shape, train, or critique how LLMs *reason* — agent frameworks, thought-search algorithms, reflective / self-corrective loops, and RL recipes that elicit human-like deliberation traces (long CoT, "aha moments", self-verification, multi-path exploration).

**Research value: high** — The open-source CoT/reasoning stack is unusually mature: canonical paper repos (ToT, ReAct, Reflexion), industrial agent frameworks (LangGraph, LlamaIndex, DSPy, CrewAI, AutoGen, OpenAgents), and a fresh 2025 wave of R1-style reasoning-RL reproductions (Open-R1, TinyZero, SimpleRL-Zoo, Open-Reasoner-Zero, PRIME) — all directly relevant to making AI "think" in more humanlike ways.

---

## 1. Selection criteria

Repos were chosen against the brief's explicit list (LangChain/LangGraph, LlamaIndex, DSPy, CrewAI, AutoGen, OpenAgents, Reflexion, Tree-of-Thoughts, ReAct, DeepSeek-R1, Open-R1, process reward models) and expanded to adjacent high-signal projects that fill obvious gaps (Graph-of-Thoughts, SimpleRL-Zoo, Open-Reasoner-Zero, PRIME, TinyZero). Every entry is either (a) the canonical reference implementation of a named reasoning technique or (b) a widely adopted production framework whose "reasoning" abstraction is the actual API users consume.

Standard fields per repo: **URL · Stars · License · Primary language · Last notable release · One-liner · Reasoning mechanism · Humanization relevance · README quote.**

---

## 2. Repositories

### 2.1 princeton-nlp/tree-of-thought-llm — Tree of Thoughts (ToT), canonical

- **URL:** https://github.com/princeton-nlp/tree-of-thought-llm
- **Stars / forks:** ~5.9k / ~606
- **License:** MIT · **Language:** Python (~79%), notebooks
- **Last release:** v0.1.0 (Jul 2023); paper-era repo, low activity since
- **One-liner:** Official NeurIPS 2023 implementation of deliberate problem solving by searching over a tree of intermediate "thoughts".
- **Reasoning mechanism:** BFS/DFS over generated thoughts with `method_generate ∈ {sample, propose}` and `method_evaluate ∈ {value, vote}`; backtracking + self-evaluation.
- **Humanization relevance:** Replaces left-to-right token decoding with *explore → self-evaluate → backtrack* — the same shape as human deliberate reasoning ("System 2"). Game-of-24 went from 4% (CoT) → 74% (ToT).
- **README quote:** *"The very simple `run.py` implements the ToT + BFS algorithm, as well as the naive IO/CoT sampling. Some key arguments: `--method_generate` (choices=[sample, propose]): thought generator, whether to sample independent thoughts (used in Creative Writing) or propose sequential thoughts (used in Game of 24); `--method_evaluate` (choices=[value, vote]): state evaluator, whether to use the value states independently (used in Game of 24) or vote on states together (used in Creative Writing)."*

### 2.2 kyegomez/tree-of-thoughts — ToT, pip-installable community impl.

- **URL:** https://github.com/kyegomez/tree-of-thoughts
- **Stars / forks:** ~4.6k / ~374
- **License:** Apache-2.0 · **Language:** Python · `pip install tree-of-thoughts`
- **One-liner:** "Plug in and Play" ToT wrapper that claims "Elevates Model Reasoning by atleast 70%".
- **Reasoning mechanism:** `TotAgent` + `ToTDFSAgent(threshold=..., max_loops=...)`; DFS/BFS variants.
- **Humanization relevance:** Lowers activation energy to swap linear CoT for branching deliberation in any LLM app; widely used as a reference by downstream agent repos.
- **Caveat:** Community fork, hype-y README; the princeton-nlp repo is the authoritative source — cite kyegomez primarily for *adoption signal*, not correctness.

### 2.3 spcl/graph-of-thoughts — Graph of Thoughts (GoT)

- **URL:** https://github.com/spcl/graph-of-thoughts
- **License:** BSD-style · **Language:** Python · `pip install graph_of_thoughts`
- **One-liner:** Official ETH/SPCL implementation of reasoning as an arbitrary DAG, not just a chain or tree.
- **Reasoning mechanism:** Thoughts are vertices; edges are dependencies. Supports *merging/aggregation, splitting/generation, refinement* — including feedback loops impossible in a tree.
- **Humanization relevance:** Closer to how humans actually combine ideas (merge two half-plans, refine one branch with evidence from another) than CoT or ToT.
- **Paper quote (arXiv:2308.09687):** *"GoT enables combining arbitrary LLM thoughts into synergistic outcomes, distilling whole networks of thoughts, or enhancing thoughts using feedback loops"* — with ~62% quality gain over ToT on sorting at >31% lower cost.

### 2.4 ysymyth/ReAct — canonical ReAct prompting

- **URL:** https://github.com/ysymyth/ReAct
- **License:** MIT · **Language:** Python (Jupyter notebooks per task)
- **One-liner:** ICLR 2023 reference code for interleaving **Rea**soning traces and **Act**ions.
- **Reasoning mechanism:** Thought → Action → Observation loop, so reasoning and tool use co-evolve in the same sequence.
- **Humanization relevance:** ReAct is the proto-pattern behind essentially every modern agent framework; it models reasoning as narrated intent plus grounded action, matching how humans "think out loud while doing".
- **README quote:** *"GPT-3 prompting code for ICLR 2023 paper ReAct: Synergizing Reasoning and Acting in Language Models. … To use ReAct for more tasks, consider trying LangChain's zero-shot ReAct Agent."* Results table reports HotpotQA 30.4 EM, AlfWorld 78.4%, WebShop 35.8% with GPT-3.

### 2.5 noahshinn/reflexion — self-reflective agents

- **URL:** https://github.com/noahshinn/reflexion
- **Stars / forks:** ~3.1k / ~300
- **License:** MIT · **Language:** Python
- **One-liner:** NeurIPS 2023 verbal reinforcement learning: agents critique their own past attempts in natural language and retry.
- **Reasoning mechanism:** Three modules — **Actor**, **Evaluator**, **Self-Reflection** — with configurable strategies (`NONE`, `LAST_ATTEMPT`, `REFLEXION`, `LAST_ATTEMPT_AND_REFLEXION`).
- **Humanization relevance:** Directly encodes self-criticism, a signature human cognitive move; produces visible "reflection" text that reads like an internal monologue.
- **README quote:** *"`ReflexionStrategy.REFLEXION` — The agent is given its self-reflection on the last attempt as context. `ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION` — The agent is given both its reasoning trace and self-reflection on the last attempt as context."*

### 2.6 stanfordnlp/dspy — programming (not prompting) reasoning modules

- **URL:** https://github.com/stanfordnlp/dspy
- **License:** MIT · **Language:** Python
- **One-liner:** Declarative framework where `dspy.ChainOfThought`, `dspy.ReAct`, etc. are first-class, optimizable modules.
- **Reasoning mechanism:** `ChainOfThought` prepends a `reasoning` field to any signature: `classify = dspy.ChainOfThought('question -> answer'); response.reasoning / response.answer`. Optimizers (MIPROv2, GEPA, BootstrapFewShot) *learn* better prompts and rationales from data.
- **Humanization relevance:** Makes reasoning traces a programmable, inspectable, improvable artifact — you can *measure* whether the "thinking" is more human and tune it.
- **README quote:** *"DSPy is the framework for programming—rather than prompting—language models. It allows you to iterate fast on building modular AI systems and offers algorithms for optimizing their prompts and weights, whether you're building simple classifiers, sophisticated RAG pipelines, or Agent loops."*

### 2.7 langchain-ai/langgraph — stateful agent graphs

- **URL:** https://github.com/langchain-ai/langgraph
- **Stars:** ~28.7k
- **License:** MIT · **Language:** Python (+ JS twin at langgraphjs)
- **One-liner:** Low-level orchestration framework for long-running, stateful agents as explicit graphs.
- **Reasoning mechanism:** Agents are graphs of nodes (LLM calls, tools, subgraphs) with persistent state, interrupts, and durable execution — enabling *plan → act → observe → replan* loops that survive crashes and human interventions.
- **Humanization relevance:** Persistent memory + human-in-the-loop interrupts = agents that "remember yesterday's conversation" and let a human course-correct mid-thought, both crucial for non-robotic interactions.
- **README quote:** *"LangGraph provides low-level supporting infrastructure for any long-running, stateful workflow or agent: Durable execution — build agents that persist through failures and can run for extended periods, automatically resuming from exactly where they left off. Human-in-the-loop — seamlessly incorporate human oversight by inspecting and modifying agent state at any point during execution. Comprehensive memory — create truly stateful agents with both short-term working memory for ongoing reasoning and long-term persistent memory across sessions."*

### 2.8 run-llama/llama_index — ReActAgent & AgentWorkflow

- **URL:** https://github.com/run-llama/llama_index  (see `docs/examples/agent/react_agent.ipynb`, `docs/examples/workflow/react_agent.ipynb`)
- **License:** MIT · **Language:** Python
- **One-liner:** RAG-first framework whose `ReActAgent` and workflow engine expose stepwise thought/action traces.
- **Reasoning mechanism:** `ReActAgent(tools=[...], llm=llm)` runs Thought→Action→Observation cycles; works even with LLMs that lack native function calling. A refactor (PR #9584) split execution into `AgentEngine` + `BaseAgentStepEngine` so custom step-policies (ReAct, OpenAI-FC, etc.) plug in.
- **Humanization relevance:** Streams full reasoning including tool calls — i.e., the agent "narrates" each step, which is exactly the trace a user reads to trust the system.

### 2.9 microsoft/autogen — multi-agent conversation framework

- **URL:** https://github.com/microsoft/autogen
- **License:** CC-BY-4.0 (docs) / MIT (code) · **Language:** Python + .NET
- **Status:** **Maintenance mode** — Microsoft now recommends *Microsoft Agent Framework* (MAF) for new projects.
- **One-liner:** Conversable-agent framework: specialized agents (`AssistantAgent`, `UserProxyAgent`) chat with each other, optionally with humans, to solve tasks.
- **Reasoning mechanism:** Multi-agent dialogue as the reasoning substrate — e.g., a `math_expert` + `chemistry_expert` + general assistant negotiate answers via `AgentTool`; MagenticOne adds planning+browser+code-exec teams.
- **Humanization relevance:** Reasoning rendered as a *group conversation* is one of the most humanlike paradigms — specialization, disagreement, delegation.
- **README quote:** *"Pioneered in Microsoft Research, AutoGen opened the door to experimental multi-agent orchestration patterns that inspired the community. … AutoGen is now in maintenance mode. For new projects, we recommend Microsoft Agent Framework."*

### 2.10 crewAIInc/crewAI — role-playing agent crews

- **URL:** https://github.com/crewAIInc/crewAI (canonical; `joaomdmoura/crewAI` redirects)
- **Stars:** ~48k+ · **License:** MIT · **Language:** Python (98.6%)
- **One-liner:** Framework for orchestrating role-playing autonomous agents — *Crews* (autonomy) + *Flows* (event-driven production control).
- **Reasoning mechanism:** Each agent has `role`, `goal`, `backstory`; tasks get assigned; the crew reasons collaboratively. Built from scratch, independent of LangChain.
- **Humanization relevance:** Personality-first framing ("you are a senior researcher with 10 years of experience…") produces reasoning in a consistent *voice*, directly adjacent to the humanization goal. ~5.4M PyPI downloads/month signals real adoption.

### 2.11 xlang-ai/OpenAgents — an open ChatGPT-Plus-like platform

- **URL:** https://github.com/xlang-ai/OpenAgents
- **Stars:** ~4.7k+ · **License:** Apache-2.0 · **Language:** Python + TypeScript
- **One-liner:** COLM 2024 open platform hosting three production agents: Data Agent, Plugins Agent (200+ tools), Web Agent.
- **Reasoning mechanism:** Each real agent mixes ReAct-style tool loops with app-specific adapters (stream parsing, memory, callbacks); Plugins Agent supports *Auto Plugin Selection*.
- **Humanization relevance:** Focus on non-expert end-user UX, chat-web UI, and realistic daily tasks — i.e., reasoning traces have to be *legible to normal users*, not just devs.
- **README quote:** *"Current language agent frameworks aim to facilitate the construction of proof-of-concept language agents while neglecting the non-expert user access to agents and paying little attention to application-level designs. We built OpenAgents, an open platform for using and hosting language agents in the wild of everyday life."*

### 2.12 deepseek-ai/DeepSeek-R1 — open-weights reasoning model

- **URL:** https://github.com/deepseek-ai/DeepSeek-R1
- **Stars / forks:** ~92k / ~11.7k · **License:** MIT (weights included)
- **One-liner:** First-generation reasoning models (R1-Zero via pure RL; R1 via cold-start + 2-stage RL + 2 SFT) at 671B MoE with 37B active, plus 6 distilled checkpoints (1.5B→70B on Qwen/Llama).
- **Reasoning mechanism:** RL on a verifier-style reward elicits long CoT, *self-verification*, *reflection*, and the now-famous **"aha moment"** — all without SFT in R1-Zero. R1 refines this with cold-start data for readability.
- **Humanization relevance:** Operational proof that very long, reflective, mid-stream-course-correcting CoT can be *trained into* a model — the reference humans and every downstream project now copy.
- **README quote:** *"DeepSeek-R1-Zero … demonstrates capabilities such as self-verification, reflection, and generating long CoTs, marking a significant milestone for the research community. Notably, it is the first open research to validate that reasoning capabilities of LLMs can be incentivized purely through RL, without the need for SFT."*
- **Usage note (from README):** *"Avoid adding a system prompt; all instructions should be contained within the user prompt. … To ensure that the model engages in thorough reasoning, we recommend enforcing the model to initiate its response with `<think>\n` at the beginning of every output."*

### 2.13 huggingface/open-r1 — fully open R1 reproduction

- **URL:** https://github.com/huggingface/open-r1
- **Stars:** ~26k+ · **License:** Apache-2.0 · **Language:** Python
- **One-liner:** HF's open reproduction pipeline for DeepSeek-R1: SFT, GRPO, synthetic-reasoning generation, evals.
- **Reasoning mechanism:** `src/open_r1/{grpo.py, sft.py, generate.py}` + a `Makefile` covering the three-step plan (distill → RL-Zero → full multi-stage). Ships *Mixture-of-Thoughts* (350k reasoning traces) and *OpenR1-Distill-7B*.
- **Humanization relevance:** Fills the gaps left by DeepSeek's release — especially *data curation for reasoning traces*, which is exactly where "humanlike thinking" is shaped.
- **Project goals (README):** Reproduce R1-Distill models, replicate the R1-Zero pure-RL pipeline, and demonstrate multi-stage training from base → RL-tuned.

### 2.13b simplescaling/s1 — budget-forced test-time scaling

- **URL:** https://github.com/simplescaling/s1
- **License:** Apache-2.0 · **Language:** Python
- **Paper:** [arXiv:2501.19393](https://arxiv.org/abs/2501.19393) · EMNLP 2025 / ICLR 2025 workshop (Stanford et al.)
- **One-liner:** SFT Qwen2.5-32B on 1,000 curated reasoning traces (s1K) then **budget force** at inference to control thinking depth.
- **Reasoning mechanism:** Budget forcing appends "Wait" tokens when the model tries to close its thinking block early (extending thought) or hard-truncates (shortening thought). s1-32B beats o1-preview by up to 27% on MATH and AIME24.
- **Humanization relevance:** "Wait" as a budget-extension signal is the naturalistic hesitation token that humans produce mid-deliberation. The paper formalizes a phenomenon practitioners already observed with llama.cpp `--reasoning-budget-message`. Budget forcing is now a first-class inference-time humanization lever.

### 2.13c MoonshotAI/Kimi-K2 / Kimi-K2-Thinking — open-weights trillion-parameter reasoning

- **URL:** https://huggingface.co/moonshotai/Kimi-K2-Thinking · https://github.com/MoonshotAI/Kimi-K2.5
- **License:** Modified MIT · **Language:** Python (inference); weights on HuggingFace
- **Release:** November 2025
- **One-liner:** 1-trillion-parameter MoE reasoning model (32B active per pass) with native tool-calling fused into the thinking pass; transparent `<think>` blocks.
- **Reasoning mechanism:** Kimi K2 Thinking fuses tool invocations directly into the reasoning trace rather than deferring tool use to after thinking completes — enabling 200–300 sequential tool calls with coherent mid-reasoning grounding. Sets SOTA on Humanity's Last Exam (HLE) and BrowseComp.
- **Humanization relevance:** Tool-calling-in-thinking is the most humanlike agent architecture yet — humans interrupt their deliberation to look things up, not just at the end. The transparent `<think>` blocks are accessible for styling. r/LocalLLaMA threads note that Kimi K2's CoT "voice" is among the most natural-sounding of the open-weights class (not just the "Wait… Hmm…" loops of R1 distills).

### 2.13d facebookresearch/coconut — reasoning in continuous latent space

- **URL:** https://github.com/facebookresearch/coconut
- **License:** CC-BY-NC · **Language:** Python (PyTorch)
- **Paper:** [arXiv:2412.06769](https://arxiv.org/abs/2412.06769) · ICLR 2025
- **One-liner:** Replace discrete token-level reasoning steps with continuous hidden-state feedback loops — "Chain of Continuous Thought."
- **Reasoning mechanism:** Last hidden state is fed back as next input embedding; no token decoding between reasoning steps. Enables BFS-style multi-path exploration in latent space. Multi-stage curriculum progressively replaces language steps with latent steps.
- **Humanization relevance:** Coconut makes explicit what the Unslop project assumes implicitly: the visible trace is a *rendering* of something deeper. If reasoning migrates fully to latent space, the surface CoT becomes a wholly synthetic product — the same design space Unslop operates in. Interpretability trade-off: better reasoning, zero trace to read.

### 2.14 Jiayi-Pan/TinyZero — minimal R1-Zero reproduction

- **URL:** https://github.com/Jiayi-Pan/TinyZero
- **Stars:** ~13k · **License:** Apache-2.0 · **Language:** Python
- **Status:** Deprecated — use [veRL](https://github.com/volcengine/verl) directly; kept as an explainer.
- **One-liner:** 3B base LM develops self-verification + search on countdown/multiplication for <$30.
- **Reasoning mechanism:** PPO via veRL on rule-based rewards; Qwen2.5-3B base emerges with reflective behavior.
- **Humanization relevance:** Cheapest proof that the "aha moment" is not a scale artifact of 671B models — making humanlike reflective reasoning trainable by small labs.
- **README quote:** *"Through RL, the 3B base LM develops self-verification and search abilities all on its own. You can experience the Aha moment yourself for < $30."*

### 2.15 hkust-nlp/simpleRL-reason (SimpleRL-Zoo)

- **URL:** https://github.com/hkust-nlp/simpleRL-reason
- **Stars / forks:** ~3.8k / ~289 · **License:** MIT · **Language:** Python
- **One-liner:** "Simple" RL recipe (rule-based reward, 8K MATH, PPO, no SFT, no RM) applied to **10 diverse base models** (Llama3-8B, Mistral-7B/24B, DeepSeekMath, Qwen2.5 0.5B→32B).
- **Reasoning mechanism:** Builds on OpenRLHF + vLLM + Ray; GRPO-free baseline; Qwen2.5-Math-7B goes 30.2 → 48.8 avg across MATH/AIME/AMC benchmarks.
- **Humanization relevance:** Paper explicitly studies how *different base families* produce different reasoning behaviors under zero-RL — first observation of the "aha moment" in small non-Qwen models. Important caveat for humanization: *response length alone doesn't correlate with cognitive behaviors like self-verification*.
- **README quote:** *"It is simple because only rule-based reward is used, the recipe is almost the same as the one used in DeepSeek-R1, except that the code currently uses PPO rather than GRPO. … No SFT, no reward model, just 8K MATH examples for verification."*

### 2.16 Open-Reasoner-Zero/Open-Reasoner-Zero

- **URL:** https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero
- **Stars / forks:** ~2.1k / ~119 · **License:** MIT · **Language:** Python
- **One-liner:** Minimalist vanilla-PPO + GAE(λ=1, γ=1) + rule-based rewards, no KL regularization — matches DeepSeek-R1-Zero-Qwen-32B quality at ~10× fewer training steps.
- **Reasoning mechanism:** Claims that removing KL + picking simple RL is enough at scale; ships 0.5B/1.5B/7B/32B checkpoints + 129k curated reasoning data.
- **Humanization relevance:** A counter-hypothesis to PRMs and complex RL — argues that the "humanlike" CoT patterns emerge without process supervision if you just scale the basics correctly.

### 2.17 openai/prm800k — process reward supervision dataset

- **URL:** https://github.com/openai/prm800k
- **License:** MIT · **Language:** Python (data + grading)
- **One-liner:** 800K step-level correctness labels for model-generated MATH solutions, companion to "Let's Verify Step by Step".
- **Reasoning mechanism:** Each step in a solution is labeled −1/0/+1 by humans; PRM trained on this outperforms outcome-only reward models on MATH best-of-N (~78% vs lower baselines).
- **Humanization relevance:** This is the dataset that operationalizes "reward *how* you think, not just *what* you output" — the substrate for reasoning that follows human-endorsed chains rather than reaching the right answer via wrong logic.
- **README quote:** *"PRM800K is a process supervision dataset containing 800,000 step-level correctness labels for model-generated solutions to problems from the MATH dataset."*
- **Label schema excerpt (README):** each step holds multiple `completions` with `rating ∈ {−1, 0, +1}` and `flagged`; labelers terminate with `finish_reason ∈ {found_error, solution, bad_problem, give_up}` — a machine-readable record of what "good human reasoning" looks like.

### 2.18 PRIME-RL/PRIME — implicit process rewards without step labels

- **URL:** https://github.com/PRIME-RL/PRIME
- **Stars:** ~1.8k+ (Dec 2024 launch) · **Paper:** arXiv:2502.01456
- **One-liner:** Online RL with **implicit** process rewards — derives dense per-step signals from an outcome reward model, skipping the need for PRM800K-style manual step annotation.
- **Reasoning mechanism:** Implicit PRM is trained as an ORM, then *interpreted* as a PRM at inference and during RL; rollout-level outcome + step-level implicit process rewards are combined for policy updates. Ships Eurus-2-7B-PRIME (started from Eurus-2-7B-SFT).
- **Humanization relevance:** Makes step-level "was this line of thinking good?" feedback scalable — the bottleneck that previously prevented most teams from doing PRM-style humanlike-reasoning RL.

---

## 3. Patterns

1. **Thought structure has been generalized from *chain* → *tree* → *graph* → *latent*.** CoT (linear) → ToT (branch + backtrack) → GoT (merge + refine + loop) → Coconut/latent-space BFS (no surface tokens at all). Each jump maps to a more humanlike mode of deliberation, but with decreasing interpretability.
2. **Self-critique is now a reusable primitive.** Reflexion's *Actor / Evaluator / Self-Reflection* split shows up (renamed) in LangGraph subgraphs, DSPy `Refine`, CrewAI manager agents, and the "reflection + self-verification" behavior emergent in DeepSeek-R1. The humanization-relevant insight is that *visible* self-criticism text increases user trust.
3. **Reasoning has moved from prompt-time to train-time.** 2023 was dominated by prompting tricks (ToT, ReAct, Reflexion). 2025 is dominated by RL recipes (DeepSeek-R1, Open-R1, TinyZero, SimpleRL-Zoo, Open-Reasoner-Zero, PRIME). The "long humanlike CoT with aha moments" can now be *trained into* a model, not just elicited.
4. **Process rewards are converging on "implicit" variants.** PRM800K proved step-level supervision works; PRIME removed the human-annotation bottleneck; SimpleRL-Zoo and Open-Reasoner-Zero then asked whether you even need a PRM. The field is actively triangulating.
5. **Agent frameworks have consolidated around ReAct + persistent state + human-in-the-loop.** LangGraph, LlamaIndex workflows, AutoGen/MAF, CrewAI, and OpenAgents all converge on the same mental model: a stateful graph of specialized, tool-using agents with explicit interrupt points. ReAct is the shared core.
6. **Open-weights reasoning is the new normal.** DeepSeek-R1 (MIT, 671B + 6 distilled sizes), Open-Reasoner-Zero, SimpleRL, HF Open-R1, and now Kimi K2 Thinking (1T-parameter MoE, Modified MIT) mean that by 2026 any serious team can self-host a reasoning model; licensing is no longer the blocker for humanization research.
7. **Budget forcing is now a standard inference primitive.** s1 (simplescaling) formalized the "Wait" token trick into a reproducible method. The naturalness of the budget stop signal matters — "Wait" outperforms hard truncation, confirming practitioner findings from llama.cpp.

## 4. Trends

- **Visible "thinking" as a product feature.** `<think>...</think>` style tags (DeepSeek-R1, Kimi K2) and streamed ReAct traces (LlamaIndex, LangGraph) are turning internal monologue into part of the UX — the humanization frontier.
- **Tool use fused into the reasoning trace.** Kimi K2 Thinking (and Claude 4's interleaved thinking) merge tool calls into the CoT pass rather than deferring them. This produces reasoning traces that read like a researcher browsing sources mid-thought — more humanlike than the two-phase (think → act) pattern.
- **Role/persona-first agent design.** CrewAI's `role/goal/backstory` pattern and AutoGen's named experts make *voice* a first-class attribute alongside capability.
- **Programmable reasoning.** DSPy's `ChainOfThought` module + optimizers (MIPROv2, GEPA) mean reasoning style can be *learned* rather than hand-prompted — the missing link between humanization evals and training.
- **Reasoning distillation down-market.** DeepSeek-R1-Distill-Qwen-1.5B/7B, OpenR1-Distill-7B, and Qwen3 MoE series bring humanlike CoT behavior to edge/consumer-scale models. Qwen3-30B-A3B activates only 3B parameters per pass.
- **Convergence on GRPO/PPO with rule-based rewards.** The 2025 recipes are converging on the same backbone (verifier-style reward, PPO/GRPO, vLLM rollout, Ray cluster). Implementation fragmentation is decreasing.
- **Framework-level re-consolidation.** AutoGen's move to maintenance mode (→ Microsoft Agent Framework) signals the category is compressing around state graphs + tools + A2A/MCP interop. LangGraph is increasingly the default stateful graph layer.
- **Latent reasoning as the next leap.** Coconut (ICLR 2025), Heima (single-token CoT compression), and the Latent CoT Survey (arXiv 2505.16782) point toward reasoning that produces no surface trace. Humanization work will need to address a world where the CoT to style doesn't exist.

## 5. Gaps (directly relevant to "humanizing AI thinking")

1. **Humanization-specific reasoning benchmarks are missing.** All the major repos benchmark against MATH, AIME, GPQA, SWE-bench — logical correctness. There is no widely adopted open eval for *how humanlike* the reasoning trace reads (variability, hedging, self-talk, emotional reasoning, tangents).
2. **Persona × reasoning is under-explored.** CrewAI gives you persona; DSPy gives you optimizable reasoning. Nobody has published a clean, benchmarked combination where persona *shapes* CoT style (instead of just the final answer voice).
3. **Non-math/code domains lack reasoning-RL recipes.** Almost every R1 reproduction trains on math + code because the verifier is cheap. Dialogue, empathetic reasoning, creative planning, and advice-giving — the humanization core — have no equivalent open recipe. PRIME's implicit PRM is the most promising generalizable primitive, but almost nobody has tried it on conversational data publicly.
4. **"Aha moments" are not controllable.** Repos report observing them (TinyZero, SimpleRL-Zoo) but do not offer knobs to elicit or suppress them. From a UX perspective, humans *sometimes* want the visible reflection and *sometimes* want a confident, concise answer.
5. **Memory-meets-reasoning is fragmented.** LangGraph has long-term memory; none of the R1-style RL repos train with long-term memory in the loop. Humanlike thinking in multi-session conversations is currently a framework-side hack, not a model-side property.
6. **AutoGen → MAF migration creates a docs gap.** A huge amount of tutorial/blog content still targets AutoGen 0.2 API shapes that no longer receive features; downstream humanization projects relying on AutoGen need to plan migration.

---

## 6. Quick-reference table

| # | Repo | Category | Stars (approx.) | License |
|---|---|---|---|---|
| 1 | princeton-nlp/tree-of-thought-llm | Thought search (canonical) | 5.9k | MIT |
| 2 | kyegomez/tree-of-thoughts | Thought search (community) | 4.6k | Apache-2.0 |
| 3 | spcl/graph-of-thoughts | Thought search (graph) | — | BSD |
| 4 | ysymyth/ReAct | Prompting pattern | — | MIT |
| 5 | noahshinn/reflexion | Self-reflective agents | 3.1k | MIT |
| 6 | stanfordnlp/dspy | Programmable reasoning | — | MIT |
| 7 | langchain-ai/langgraph | Agent framework | 28.7k+ | MIT |
| 8 | run-llama/llama_index | Agent framework (RAG-first) | — | MIT |
| 9 | microsoft/autogen (maintenance) | Agent framework | — | MIT / CC-BY |
| 10 | crewAIInc/crewAI | Agent framework (personas) | 48k+ | MIT |
| 11 | xlang-ai/OpenAgents | Agent platform (end-user) | 4.7k+ | Apache-2.0 |
| 12 | deepseek-ai/DeepSeek-R1 | Reasoning model weights | 92k+ | MIT |
| 13 | huggingface/open-r1 | Reasoning-RL reproduction | 26k+ | Apache-2.0 |
| 13b | simplescaling/s1 | Budget-forced test-time scaling | — | Apache-2.0 |
| 13c | MoonshotAI/Kimi-K2-Thinking | Reasoning model (1T MoE, tool-fused) | — | Modified MIT |
| 13d | facebookresearch/coconut | Latent continuous reasoning | — | CC-BY-NC |
| 14 | Jiayi-Pan/TinyZero (deprecated) | Reasoning-RL reproduction | 13k | Apache-2.0 |
| 15 | hkust-nlp/simpleRL-reason | Reasoning-RL reproduction | 3.8k | MIT |
| 16 | Open-Reasoner-Zero/Open-Reasoner-Zero | Reasoning-RL reproduction | 2.1k | MIT |
| 17 | openai/prm800k | Process supervision dataset | — | MIT |
| 18 | PRIME-RL/PRIME | Implicit process rewards | 1.8k+ | (see repo) |

*Star counts are snapshots from public search/README signals and will drift; treat them as order-of-magnitude.*

---

## 7. Sources

- LangGraph README — https://github.com/langchain-ai/langgraph
- Tree of Thoughts (Princeton) README — https://github.com/princeton-nlp/tree-of-thought-llm
- Tree of Thoughts (kyegomez) — https://github.com/kyegomez/tree-of-thoughts
- Graph of Thoughts — https://github.com/spcl/graph-of-thoughts (paper: arXiv:2308.09687)
- ReAct — https://github.com/ysymyth/ReAct (paper: arXiv:2210.03629)
- Reflexion — https://github.com/noahshinn/reflexion (paper: arXiv:2303.11366)
- DSPy — https://github.com/stanfordnlp/dspy (docs: https://dspy.ai)
- LlamaIndex ReAct agent examples — https://github.com/run-llama/llama_index (docs/examples/agent/react_agent.ipynb)
- AutoGen — https://github.com/microsoft/autogen (successor: https://github.com/microsoft/agent-framework)
- CrewAI — https://github.com/crewAIInc/crewAI
- OpenAgents — https://github.com/xlang-ai/OpenAgents (paper: arXiv:2310.10634)
- DeepSeek-R1 — https://github.com/deepseek-ai/DeepSeek-R1 (paper: arXiv:2501.12948)
- Open-R1 — https://github.com/huggingface/open-r1 (HF blog: https://huggingface.co/blog/open-r1)
- TinyZero — https://github.com/Jiayi-Pan/TinyZero
- SimpleRL-Zoo — https://github.com/hkust-nlp/simpleRL-reason (paper: arXiv:2503.18892)
- Open-Reasoner-Zero — https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero (paper: arXiv:2503.24290)
- PRM800K — https://github.com/openai/prm800k (paper: arXiv:2305.20050, "Let's Verify Step by Step")
- PRIME — https://github.com/PRIME-RL/PRIME (paper: arXiv:2502.01456)
- s1 (simplescaling) — https://github.com/simplescaling/s1 (paper: arXiv:2501.19393)
- Kimi K2 Thinking — https://huggingface.co/moonshotai/Kimi-K2-Thinking · https://github.com/MoonshotAI/Kimi-K2.5
- Coconut — https://github.com/facebookresearch/coconut (paper: arXiv:2412.06769)
