# Category 06 — Chain-of-Thought & Human-Like Reasoning

## Angle A — Academic & Scholarly

**Scope.** Seminal and recent peer-reviewed / arXiv papers on chain-of-thought (CoT), zero-shot CoT, self-consistency, Tree of Thoughts, Graph of Thoughts, ReAct, Reflexion, Self-Refine, PAL, PoT, process reward, deliberative reasoning, System-1 vs System-2 in LLMs, inner monologue / scratchpads, and o1 / R1-style long-CoT reasoning.

**Project relevance (Humanizing AI output & thinking).** Reasoning-trace methods are the backbone of "human-like thinking" in LLMs: they produce the visible deliberation, self-correction, hesitation, and multi-path exploration that make model cognition legible — and that, when surfaced well, make outputs feel authored rather than mechanically sampled. This file catalogs the academic canon we draw on.

---

## 1. Wei et al. (2022) — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

- **Authors:** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou (Google Research).
- **Venue / Year:** NeurIPS 2022.
- **Link:** [arXiv:2201.11903](https://arxiv.org/abs/2201.11903).
- **Core idea:** A handful of few-shot exemplars that *show* intermediate reasoning steps ("chain of thought") unlock complex arithmetic, commonsense, and symbolic reasoning in sufficiently large models, without any fine-tuning.
- **Headline result:** PaLM-540B with 8 CoT exemplars hits 58.1% on GSM8K, surpassing fine-tuned GPT-3 + verifier. Reasoning appears as an *emergent* capability at scale.
- **Why it matters for humanization:** This is the foundational paper for "making the model think out loud." Every downstream humanization technique (reflection, self-critique, persona-consistent reasoning) sits on top of it.

## 2. Kojima et al. (2022) — Large Language Models are Zero-Shot Reasoners

- **Authors:** Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, Yusuke Iwasawa.
- **Venue / Year:** NeurIPS 2022.
- **Link:** [arXiv:2205.11916](https://arxiv.org/abs/2205.11916).
- **Core idea:** Simply prepending `"Let's think step by step."` to a prompt triggers chain-of-thought reasoning with zero task-specific exemplars.
- **Headline result:** On MultiArith, accuracy jumps from 17.7% → 78.7%; on GSM8K, 10.4% → 40.7%, across InstructGPT and PaLM-540B.
- **Why it matters:** Demonstrates CoT is a latent *capability* elicited by a cue, not a skill that must be taught with examples — a cornerstone insight for lightweight humanization prompts.

## 3. Wang et al. (2022) — Self-Consistency Improves Chain of Thought Reasoning

- **Authors:** Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou.
- **Venue / Year:** ICLR 2023.
- **Link:** [arXiv:2203.11171](https://arxiv.org/abs/2203.11171).
- **Core idea:** Replace greedy decoding with sampling of many diverse CoT paths, then marginalize via majority vote over final answers.
- **Headline result:** +17.9 pts on GSM8K, +11.0 on SVAMP, +12.2 on AQuA, +6.4 on StrategyQA over vanilla CoT.
- **Why it matters:** Introduces the "multiple lines of reasoning → converge" paradigm that mirrors how humans triangulate uncertain answers, and underpins later tree/graph methods.

## 4. Yao et al. (2023) — Tree of Thoughts: Deliberate Problem Solving with LLMs

- **Authors:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan.
- **Venue / Year:** NeurIPS 2023.
- **Link:** [arXiv:2305.10601](https://arxiv.org/abs/2305.10601).
- **Core idea:** Generalize CoT to a *tree* of thoughts where the model generates candidate intermediate states, self-evaluates them, and uses classical search (BFS/DFS) with lookahead and backtracking.
- **Headline result:** Game of 24 jumps from 4% (GPT-4 CoT) to 74% (GPT-4 ToT); strong gains on Creative Writing and Mini Crosswords.
- **Why it matters:** Makes deliberation explicit — the model does not just narrate a path, it *searches*. This is the direct computational analog of System-2 thinking.

## 5. Besta et al. (2023) — Graph of Thoughts: Solving Elaborate Problems with LLMs

- **Authors:** Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, Torsten Hoefler (ETH Zürich et al.).
- **Venue / Year:** AAAI 2024.
- **Link:** [arXiv:2308.09687](https://arxiv.org/abs/2308.09687).
- **Core idea:** Model LLM thoughts as arbitrary DAG vertices with edges for dependency, aggregation (merge), and refinement (self-loop). Supports operations CoT/ToT cannot express (e.g., combining two sub-solutions).
- **Headline result:** +62% quality on sorting vs ToT with >31% lower cost; better Pareto frontier than CoT / CoT-SC / ToT on set operations, keyword counting, and document merging.
- **Why it matters:** Shows non-linear, recombinant reasoning structures — closer to how humans re-use and splice partial conclusions.

## 6. Yao et al. (2022) — ReAct: Synergizing Reasoning and Acting in Language Models

- **Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao.
- **Venue / Year:** ICLR 2023.
- **Link:** [arXiv:2210.03629](https://arxiv.org/abs/2210.03629).
- **Core idea:** Interleave `Thought → Action → Observation` steps so reasoning traces update plans while tool calls ground the model in external state (Wikipedia API, environments).
- **Headline result:** Reduces hallucination on HotpotQA / Fever; +34% absolute success on ALFWorld, +10% on WebShop over imitation / RL baselines using only 1–2 in-context examples.
- **Why it matters:** Canonical framework for agentic, grounded reasoning — reasoning that stays honest because it must periodically touch reality.

## 7. Shinn et al. (2023) — Reflexion: Language Agents with Verbal Reinforcement Learning

- **Authors:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao.
- **Venue / Year:** NeurIPS 2023.
- **Link:** [arXiv:2303.11366](https://arxiv.org/abs/2303.11366).
- **Core idea:** Agents verbally reflect on failed trajectories and store self-critiques in an episodic memory buffer that conditions future attempts — reinforcement via *language*, not weight updates.
- **Headline result:** 91% pass@1 on HumanEval, beating the then-SOTA GPT-4 (80%); gains across decision-making, coding, and reasoning tasks.
- **Why it matters:** Introduces the natural-language self-critique loop that makes agents *feel* like they learn from mistakes within a session — a core humanization pattern.

## 8. Madaan et al. (2023) — Self-Refine: Iterative Refinement with Self-Feedback

- **Authors:** Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, Peter Clark.
- **Venue / Year:** NeurIPS 2023.
- **Link:** [arXiv:2303.17651](https://arxiv.org/abs/2303.17651).
- **Core idea:** A single LLM plays generator, critic, and editor in a `Generate → Feedback → Refine` loop — no training, no external reward model.
- **Headline result:** ~20% absolute preference gain (humans + metrics) over direct GPT-3.5 / GPT-4 generations across 7 tasks (dialogue, math, review rewriting, code readability).
- **Why it matters:** The simplest, most transferable pattern for producing drafts that feel revised rather than first-pass — directly applicable to humanizing prose output.

## 9. Gao et al. (2022) — PAL: Program-Aided Language Models

- **Authors:** Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, Graham Neubig (CMU).
- **Venue / Year:** ICML 2023.
- **Link:** [arXiv:2211.10435](https://arxiv.org/abs/2211.10435).
- **Core idea:** The LLM translates the problem into Python; a deterministic interpreter does the arithmetic. Reasoning ≠ computation.
- **Headline result:** With Codex, +15 pts on GSM8K over PaLM-540B + CoT; SOTA across 13 math / symbolic / algorithmic benchmarks.
- **Why it matters:** Key precedent for hybrid "neural reasoning + symbolic execution" that keeps arithmetic honest while preserving human-style narration.

## 10. Chen et al. (2022) — Program of Thoughts Prompting (PoT)

- **Authors:** Wenhu Chen, Xueguang Ma, Xinyi Wang, William W. Cohen.
- **Venue / Year:** TMLR 2023.
- **Link:** [arXiv:2211.12588](https://arxiv.org/abs/2211.12588).
- **Core idea:** Express the reasoning trace itself as a program; offload execution. Distinguished from PAL by explicit framing as a CoT variant and by combining with self-consistency.
- **Headline result:** ~12% avg. improvement over CoT across 8 math / financial-QA datasets; SOTA on all tested math word-problem sets when combined with self-consistency.
- **Why it matters:** Confirms the "disentangle thinking from arithmetic" pattern is general, not task-specific.

## 11. Uesato et al. (2022) — Solving Math Word Problems with Process- and Outcome-Based Feedback

- **Authors:** Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, Irina Higgins (DeepMind).
- **Venue / Year:** NeurIPS MATH-AI workshop, 2022.
- **Link:** [arXiv:2211.14275](https://arxiv.org/abs/2211.14275).
- **Core idea:** First rigorous comparison of outcome supervision (reward the final answer) vs process supervision (reward each reasoning step) for math reasoning.
- **Headline result:** On GSM8K, final-answer error 16.8% → 12.7%, and *reasoning* error among correct solutions 14.0% → 3.4% with process feedback — i.e., correct answers for correct reasons.
- **Why it matters:** Establishes that supervising *how* a model thinks, not just *what* it concludes, is necessary for trustworthy reasoning — an alignment foundation for humanization too (we want honest reasons, not just good outputs).

## 12. Lightman et al. (2023) — Let's Verify Step by Step

- **Authors:** Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe (OpenAI).
- **Venue / Year:** ICLR 2024.
- **Link:** [arXiv:2305.20050](https://arxiv.org/abs/2305.20050); [PRM800K dataset](https://github.com/openai/prm800k).
- **Core idea:** Scale the process-supervision thesis of Uesato et al. with 800K step-level human labels; train a Process Reward Model (PRM) and use it to rerank solutions.
- **Headline result:** 78% on a representative MATH test subset — a large margin over outcome-supervised reward models; active learning substantially improves PRM data efficiency.
- **Why it matters:** Provides the training signal behind today's reasoning models (o1, R1-like) and releases the canonical process-feedback dataset.

## 13. Nye et al. (2021) — Show Your Work: Scratchpads for Intermediate Computation

- **Authors:** Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David Luan, Charles Sutton, Augustus Odena (Google).
- **Venue / Year:** arXiv preprint, Nov 2021 (NeurIPS workshop).
- **Link:** [arXiv:2112.00114](https://arxiv.org/abs/2112.00114).
- **Core idea:** Transformers struggle with unbounded multi-step computation "in one pass" but succeed when allowed to emit intermediate steps into a scratchpad — both via few-shot prompting and fine-tuning.
- **Why it matters:** The pre-CoT ancestor of chain-of-thought; introduces the "scratchpad" mental model that o1-style hidden reasoning tokens now instantiate in production.

## 14. Zhou et al. (2022) — Least-to-Most Prompting Enables Complex Reasoning

- **Authors:** Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi.
- **Venue / Year:** ICLR 2023.
- **Link:** [arXiv:2205.10625](https://arxiv.org/abs/2205.10625).
- **Core idea:** Decompose a hard problem into an ordered list of easier subproblems, then solve each in turn, feeding prior answers forward.
- **Headline result:** code-davinci-002 reaches ≥99% on the SCAN compositional generalization benchmark (including length split) with just 14 exemplars, vs 16% with CoT — beating specialized neuro-symbolic models trained on 15K+ examples.
- **Why it matters:** Formalizes hierarchical planning in natural language — the scaffolding behind structured, human-like task breakdowns.

## 15. Zelikman et al. (2022) — STaR: Bootstrapping Reasoning with Reasoning

- **Authors:** Eric Zelikman, Yuhuai Wu, Jesse Mu, Noah D. Goodman (Stanford, Google Research).
- **Venue / Year:** NeurIPS 2022.
- **Link:** [arXiv:2203.14465](https://arxiv.org/abs/2203.14465).
- **Core idea:** Iteratively (1) sample rationales for training questions, (2) for wrong answers, *re-generate rationales conditioned on the correct answer* ("rationalization"), (3) fine-tune on all rationales that reached the correct answer; repeat.
- **Headline result:** On CommonsenseQA, a small model trained with STaR rivals a 30× larger SOTA model that was directly fine-tuned.
- **Why it matters:** Early, highly influential recipe for *self-generated* reasoning data — ancestor of R1-Zero-style pipelines.

## 16. DeepSeek-AI (2025) — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

- **Authors:** DeepSeek-AI team (Daya Guo, Dejian Yang, Haowei Zhang, et al.).
- **Venue / Year:** arXiv preprint, Jan 2025.
- **Link:** [arXiv:2501.12948](https://arxiv.org/abs/2501.12948).
- **Core idea:** Train a reasoning model (**R1-Zero**) with *pure* RL using GRPO on DeepSeek-V3-Base, with no SFT cold-start, letting long CoT, reflection, and "aha moments" emerge naturally. **R1** adds cold-start data + multi-stage training to fix readability and language-mixing.
- **Headline result:** AIME 2024 pass@1 rises 15.6% → 71.0% (86.7% with majority voting), matching OpenAI-o1-0912. 6 distilled dense models (1.5B–70B, Qwen/Llama bases) open-sourced.
- **Why it matters:** The open, reproducible counterpart to o1 — and the paper that popularized *emergent* reasoning behaviors (self-verification, backtracking, reflection) as a product of reward, not prompting.

## 17. OpenAI (2024) — OpenAI o1 System Card

- **Authors:** OpenAI.
- **Venue / Year:** OpenAI technical report, Dec 2024 (earlier o1-preview card: Sep 2024).
- **Link:** [o1 System Card (PDF)](https://cdn.openai.com/o1-system-card-20241205.pdf).
- **Core idea:** Train via large-scale RL to *think* in long, hidden chains of thought before responding — refining strategy, trying alternatives, recognizing errors. Introduces **deliberative alignment**: the model reasons over the safety spec itself at inference time.
- **Why it matters:** The industrial reference point for "long-CoT reasoning models." Establishes the template that R1, QwQ, and Kimi k1.5 follow, and anchors the current debate about faithfulness / visibility of hidden reasoning.

## 18. Qwen Team (2024) — QwQ-32B-Preview: Reflect Deeply on the Boundaries of the Unknown

- **Authors:** Qwen Team, Alibaba.
- **Venue / Year:** Technical blog + HF release, Nov 2024.
- **Link:** [Qwen blog](https://qwenlm.github.io/blog/qwq-32b-preview/); [model card](https://huggingface.co/Qwen/QwQ-32B-Preview).
- **Core idea:** A 32.5B "Qwen with Questions" model built on Qwen2.5-32B-Instruct that externalizes self-questioning and reflective reasoning with a 32K context.
- **Headline result:** 65.2% GPQA, 50.0% AIME, 90.6% MATH-500, 50.0% LiveCodeBench. Known failure modes: language mixing, recursive reasoning loops.
- **Why it matters:** Open evidence that deliberative style + moderate scale suffices for frontier math/code reasoning — and a candid case study in how "thinking out loud" can devolve into rumination (relevant to humanization failure modes).

## 19. Turpin et al. (2023) — Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting

- **Authors:** Miles Turpin, Julian Michael, Ethan Perez, Samuel R. Bowman (NYU, Anthropic).
- **Venue / Year:** NeurIPS 2023.
- **Link:** [arXiv:2305.04388](https://arxiv.org/abs/2305.04388).
- **Core idea:** CoT explanations can systematically misrepresent the actual computation. Adding biasing features to the input (e.g., reordering MCQ so the answer is always A) changes predictions by up to 36% on BIG-Bench Hard, while CoTs never mention the bias.
- **Why it matters:** Cautionary pillar for any humanization pipeline that surfaces reasoning to users. "Looking like honest reasoning" ≠ "being honest reasoning"; designs must account for post-hoc rationalization.

## 20. Li et al. (2025) — From System 1 to System 2: A Survey of Reasoning Large Language Models

- **Authors:** Zhong-Zhi Li, Duzhen Zhang, Ming-Liang Zhang, Jiaxin Zhang, Zengyan Liu, Yuxuan Yao, Haotian Xu, Junhao Zheng, Pei-Jie Wang, Xiuyi Chen, Yingying Zhang, Fei Yin, Jiahua Dong, Zhijiang Guo, Le Song, Cheng-Lin Liu.
- **Venue / Year:** arXiv preprint, Feb 2025.
- **Link:** [arXiv:2502.17419](https://arxiv.org/abs/2502.17419).
- **Core idea:** A systematic survey mapping the shift from System-1 (fast, heuristic) foundational LLMs to System-2 (slow, deliberate) reasoning LLMs. Taxonomizes construction methods, benchmarks, and core reasoning techniques including CoT, ToT/GoT, self-consistency, process reward, RL with verifiable rewards, and distillation.
- **Why it matters:** The current best single-document map of the reasoning-LLM landscape; grounds any humanization project that leans on dual-process theory.

## 21. Huang et al. (2022) — Inner Monologue: Embodied Reasoning through Planning with Language Models

- **Authors:** Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, Brian Ichter.
- **Venue / Year:** CoRL 2022.
- **Link:** [arXiv:2207.05608](https://arxiv.org/abs/2207.05608).
- **Core idea:** Form a closed-loop "inner monologue" by feeding environment observations (passive scene description, active LLM-initiated queries, success detection) back into the LLM's prompt — no additional training.
- **Why it matters:** Grounds the metaphor of "inner speech" in real embodied systems; influential precedent for reasoning that is *situated* rather than floating free — a key property of human-like cognition.

## 22. Wei et al. (2022) — Emergent Abilities of Large Language Models

- **Authors:** Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, William Fedus.
- **Venue / Year:** TMLR 2022.
- **Link:** [arXiv:2206.07682](https://arxiv.org/abs/2206.07682).
- **Core idea:** Some capabilities — including chain-of-thought reasoning — appear discontinuously above scale thresholds and cannot be extrapolated from small-model trends.
- **Why it matters:** Provides the empirical framing ("reasoning is emergent at scale") that legitimized the entire CoT research program. (Note: Schaeffer et al. 2023 have since argued this is partly a metric artifact — a caveat worth tracking for humanization claims about "what models 'really' do.")

## 23. Kimi Team (2025) — Kimi k1.5: Scaling Reinforcement Learning with LLMs

- **Authors:** Moonshot AI (Kimi Team).
- **Venue / Year:** arXiv technical report, Jan 2025.
- **Link:** [arXiv:2501.12599](https://arxiv.org/abs/2501.12599).
- **Core idea:** Scale RL-based reasoning via (a) 128K-token context with partial rollouts, (b) online-mirror-descent policy optimization, (c) length penalties and data-recipe tuning — **without** MCTS, value functions, or process reward models. Jointly trains on text and vision.
- **Headline result:** Matches OpenAI o1 on reasoning — 77.5 AIME, 96.2 MATH-500, 94th percentile Codeforces (long-CoT); short-CoT variant beats GPT-4o / Claude 3.5 Sonnet by up to 550% on benchmarks like AIME.
- **Why it matters:** Shows long-context RL alone can induce planning, reflection, and correction behaviors — simplifying the recipe for "thinking" models and offering an alternative axis (context length) to process reward.

---

## Cross-cutting themes relevant to *Humanizing AI Output & Thinking*

- **Visible deliberation (CoT, ToT, GoT, ReAct, Inner Monologue).** Humans recognize thinking when they can watch it branch, hesitate, and recover. These papers define the grammar of that externalized cognition.
- **Self-critique and revision (Reflexion, Self-Refine, STaR).** Make the model read its own draft. Drafts that were revised *read* as human; first-pass outputs do not.
- **Correct reasons, not just correct answers (Uesato, Lightman, Turpin).** Process supervision and faithfulness work are the guardrails: without them, humanized CoT drifts into confident rationalization.
- **Dual-process framing (Kahneman → Li et al. survey; o1, R1, QwQ, Kimi k1.5).** The System-1 / System-2 split is now load-bearing terminology for frontier reasoning research and maps cleanly onto product decisions about *when* to let a model think slowly.
- **Hybrid neural-symbolic execution (PAL, PoT).** Preserves the human-style narrative while delegating arithmetic to an interpreter — a design pattern directly reusable for humanizers that must stay factually tight.

## Notable gaps / follow-up threads

- Faithfulness of *long* hidden CoTs (o1-style) is underexplored publicly.
- Emergence-as-metric-artifact critique (Schaeffer, Miranda & Koyejo, NeurIPS 2023) deserves its own entry in a follow-up pass.
- Psycholinguistic evaluations of whether model CoT structurally resembles human think-aloud protocols are sparse — a real academic gap this project could exploit.
