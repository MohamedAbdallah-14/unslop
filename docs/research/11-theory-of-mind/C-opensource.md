# Theory of Mind in AI — Open-Source & GitHub

**Research value: high** — The ToM open-source landscape is unusually well-organized for a cognitive-science-flavored subfield: 6–8 "named" benchmark repos (ToMi, BigToM, FANToM, SimpleToM, Hi-ToM, OpenToM, ToMBench, MMToM-QA) that directly cite each other, a clear Meta→AI2→Stanford→KCL→BIGAI authorship lineage, and a separate cluster of multi-agent social simulators (Generative Agents, Sotopia, CAMEL, AgentSims) that use ToM implicitly. Enough overlap for a humanization project to pick any one as a drop-in eval, enough gaps (conversation-native, applied ToM, multimodal) to matter.

## Executive Summary

Open-source ToM tooling splits into four roughly orthogonal layers. (1) **False-belief benchmarks** — the Sally–Anne lineage — are concentrated in `facebookresearch/ToMi` (EMNLP 2019, ~27★, CC-BY-NC 4.0), `ying-hui-he/Hi-ToM_dataset` (EMNLP Findings 2023, 4th-order belief + deceptive agents), and `seacowx/OpenToM` (ACL 2024, 696 narratives × 23 questions = 16,008 items, characters with personality traits and intentions). (2) **Procedural / model-written benchmarks** aim to kill data contamination: `cicl-stanford/procedural-evals-tom` (BigToM, 25 controls + 5,000 evals from causal templates), `zhchen18/ToMBench` (ACL 2024, 2,860 bilingual items across 8 tasks and 31 ATOMS abilities), and `facebookresearch/ExploreToM` (ICLR 2025, A* search over a DSL; Llama-3.1-70B scored 0%, GPT-4o 9%; fine-tuning on its data yields +27 points on ToMi). (3) **Interaction-native ToM**: `skywalker023/fantom` (EMNLP 2023, multi-party conversations with people joining/leaving; GPT-4o scores just 0.8% on the strict "All\*" score vs. human 87.5%), `yulinggu-cs/SimpleToM` (ICLR 2026, separates explicit belief attribution from *applied* ToM in supermarket/hospital/school/office scenarios), `chuanyangjin/MMToM-QA` (ACL 2024 Outstanding Paper, text+video, BIP-ALM method), and `allenai/social_i_qa` (EMNLP 2019, 38K social commonsense MCQs). (4) **Social-simulation frameworks that rely on ToM**: `joonspk-research/generative_agents` (Smallville, UIST 2023, ~26K★), `StanfordHCI/genagents` (1,000-agent interview-based successor), `sotopia-lab/sotopia` (ICLR 2024 Spotlight, 600 episodes × 90 scenarios, SOTOPIA-EVAL 7-dim rubric), `py499372727/AgentSims` (~940★, MIT-licensed GUI sandbox), and `camel-ai/camel` (16.6K★, Apache 2.0, role-playing multi-agent "society"). Plus one canonical reading list: `Mars-tin/awesome-theory-of-mind`.

The strongest cross-repo finding: **stated ToM performance collapses the moment you move from narrative Sally–Anne tasks to conversation, applied prediction, or adversarial generation.** GPT-4o on classical FB-style tasks can look near-human; GPT-4o on FANToM's `All*` strict-consistency score is 0.8%, on ExploreToM is ~9%, and on SimpleToM's behavior-prediction tier drops to ~49.5% from near-ceiling explicit ToM. This gap is *the* point of leverage: any humanization project that relies on the model understanding what the user believes vs. what is true needs to evaluate against FANToM/SimpleToM/ExploreToM rather than Sally–Anne clones.

## Sources

### False-Belief / Sally–Anne Benchmarks

- **facebookresearch/ToMi** — `github.com/facebookresearch/ToMi` — authors: Matthew Le, Y-Lan Boureau, Maximilian Nickel — EMNLP 2019 — CC-BY-NC 4.0. The first widely cited LLM-era ToM benchmark. Forked from `kayburns/tom-qa-dataset` and rebuilt to close data biases the prior work exposed. Produces `train/val/test.txt` plus matching `.trace` files that classify every story as `true_belief` / `false_belief` / `second_order_false_belief` and every question as `first_order_tom`, `second_order_tom`, `reality` (control), or `memory` (control). Tiny repo (~27★) but it is the *ur*-dataset: BigToM, OpenToM, ExploreToM, and SimTom all either extend it or explicitly acknowledge it. The fact that no one has replaced it says as much as its star count.

- **ying-hui-he/Hi-ToM_dataset** — `github.com/ying-hui-he/Hi-ToM_dataset` — EMNLP 2023 Findings. Pushes beyond first/second-order to **fourth-order** ToM questions ("Alice thinks Bob thinks Charlie thinks Dave knows …"), 1,200 QA pairs in `Hi-ToM_data/Hi-ToM_data.json`, plus `generate_tomh.sh` for more. Key addition over ToMi: **deceptive agent communications** — agents actively lie to each other, which is what makes higher-order reasoning non-trivial. Reported finding: model accuracy degrades monotonically with order, and the failure mode at order ≥3 is "commonsense lapses and hallucinations" rather than clean belief-tracking errors.

- **seacowx/OpenToM** — `github.com/seacowx/OpenToM` — ACL 2024, Hainiu Xu et al. (KCL NLP) — CC-BY-NC 4.0. The most systematic next-generation Sally–Anne: 696 narratives (596 normal @ ~194 words, 100 long @ ~492 words) × 23 questions = 16,008 items, split into three question genres — **Location** (coarse/fine × first/second order), **Multihop** (reasoning about fullness + accessibility, "social commonsense" layered on top: "if it's in someone's bag you don't just take it"), and **Attitude** (character's *psychological* reaction to others' acts). Each story has explicit character personality, intention, and sentiment metadata. Includes SimulatedToM / SelfAsk / CoT baselines. README explicitly bans training on the data: *"please avoid testing OpenToM questions in OpenAI playground or places where the data might be used for LLM training."*

### Procedural / Adversarial / Bilingual Benchmarks

- **cicl-stanford/procedural-evals-tom** (BigToM) — `github.com/cicl-stanford/procedural-evals-tom` — authors: Kanishk Gandhi, Jan-Philipp Fränken, Tobias Gerstenberg, Noah Goodman (Stanford CICL) — NeurIPS 2023. 25 hand-authored causal templates (percepts → beliefs → desires → actions) procedurally populated into **5,000 model-written evaluations**. Human ratings of item quality "higher than previous crowd-sourced evaluations and comparable to expert-written ones." Companion repo `shawnsihyunlee/simulatedtom` ships the SimToM prompting technique ("first describe what each character knows, *then* answer") against BigToM + ToMi across GPT-3.5 / GPT-4 / Llama-2. Project site: `sites.google.com/view/social-reasoning-lms`.

- **zhchen18/ToMBench** — `github.com/zhchen18/ToMBench` — ACL 2024, Zhuang Chen et al. (Tsinghua / CoAI) — MIT. Bilingual (EN/ZH) from scratch to prevent leakage. 2,860 MCQ items across **8 canonical psychology tasks**: Unexpected Outcome, Scalar Implicature, Persuasion Story, False Belief, Ambiguous Story, Hinting, Strange Story, Faux-pas Recognition. Maps to **31 abilities from the ATOMS framework** across 6 categories (Emotion, Desire, Intention, Knowledge, Belief, Non-Literal Communication). Headline number: GPT-4 lags human by >10 pts. The ability-level breakdown (Hidden Emotions, Mixed Emotions, White Lies, Irony/Sarcasm, Faux Pas, Second-Order Beliefs, etc.) is what makes this useful for humanization: you can measure which specific social skills a system lacks, not just overall "ToM score."

- **facebookresearch/ExploreToM** — `github.com/facebookresearch/ExploreToM` — ICLR 2025, Melanie Sclar et al. (Meta FAIR) — ~93★. First framework for **adversarial procedural generation** of ToM data: A* search over a custom DSL produces complex story structures, then an LLM infills plausible narrative. Results: Llama-3.1-70B scored **0%**, GPT-4o scored **9%** on the generated set. Fine-tuning Llama-3.1-70B on ExploreToM data produced **+27 points on classical ToMi** without fine-tuning on ToMi itself. Sample dataset on HF (`facebook/ExploreToM`, 13,309 rows, regenerated adversarially per target model).

### Conversation-Native & Applied ToM

- **skywalker023/fantom** — `github.com/skywalker023/fantom` — EMNLP 2023, Hyunwoo Kim, Melanie Sclar, Xuhui Zhou, Ronan Le Bras, Gunhee Kim, Yejin Choi, Maarten Sap (AI2 / UW / CMU / SNU). Evaluates ToM in **information-asymmetric multi-party conversations** — characters enter and leave a chat and later ones don't know what was said before they arrived. Three aligned question types: `BeliefQ` (Choice + free-response), `AnswerabilityQ` (List + Y/N), `InfoAccessQ` (List + Y/N). Strict `All*` score demands that a model answer *all* aligned questions consistently for a single scenario. Headline numbers in the repo's leaderboard: Human 87.5, GPT-4o **0.8**, Claude-3-Opus 0.2, Llama-3-70B-chat 0.3. FANToM's explicit thesis: *"successful ToM responses are often illusory"* when probed from multiple sides.

- **yulinggu-cs/SimpleToM** — `github.com/yulinggu-cs/SimpleToM` — ICLR 2026 (to appear), Yuling Gu, Oyvind Tafjord, Hyunwoo Kim, Jared Moore, Ronan Le Bras, Peter Clark, Yejin Choi (AI2). Exposes the gap between **explicit ToM** ("Is Mary aware of the mold?") and **applied ToM** ("Will Mary pay?" / "Was that reasonable?"). Stories are intentionally mundane (supermarket / hospital / school / office) with naturalistic info asymmetries. Key result: GPT-4o near-ceiling on (a) mental state, ~49.5% on (b) behavior, ~15.3% on (c) judgment; CoT targeted prompting recovers 93.5 / 94.7. Dataset on HF `allenai/SimpleToM`.

- **chuanyangjin/MMToM-QA** — `github.com/chuanyangjin/MMToM-QA` — ACL 2024 Outstanding Paper, Chuanyang Jin et al. (NYU / MIT / Harvard / UCSD / JHU / UVa / Tianmin Shu). First **multimodal** ToM benchmark: text + video of a household environment; 600 QAs (300 belief + 300 goal) spanning 7 question types. Ships **BIP-ALM** (Bayesian Inverse Planning Accelerated by LMs) which extracts symbolic state from multimodal input and runs Bayesian inverse planning with the LM. Now has official successor repos: `SCAI-JHU/MuMA-ToM` (multi-agent, AAAI 2025 Oral) and `SCAI-JHU/AutoToM` (NeurIPS 2025 Spotlight, SOTA on MMToM-QA + 4 other ToM benchmarks, automated agent modeling).

- **allenai/social_i_qa (SocialIQA)** — `huggingface.co/datasets/allenai/social_i_qa` / `maartensap.github.io/social-iqa` — EMNLP 2019, Maarten Sap, Hannah Rashkin, Derek Chen, Ronan Le Bras, Yejin Choi (AI2 / UW). ~37K MCQ items on **commonsense reasoning about social interactions**: context → 3 answer options, crowdsourced with an adversarial-filtering pipeline that asks workers to answer *different* but related questions to suppress stylistic give-aways in distractors. License CC-BY-4.0. >20-point human-vs-model gap at publication. Still the largest open social-commonsense corpus and a common eval alongside ATOMIC and CommonsenseQA.

- **MindDial** — `arxiv.org/abs/2306.15253` (SIGDIAL 2024, Shuwen Qiu, Song-Chun Zhu, Zilong Zheng, BIGAI). Three-level belief module (speaker's belief; speaker's model of listener's belief; belief *gap*) plugged into dialogue generation; evaluated on MutualFriend common-ground alignment and negotiation. **No public code repository found** — only paper + author pages. Notable as one of the few works where ToM is wired into generation rather than evaluated as QA, but reproduction currently requires reimplementation from the paper.

### ToM Reading List / Meta

- **Mars-tin/awesome-theory-of-mind** — `github.com/Mars-tin/awesome-theory-of-mind` — ~150★, 6 contributors, last updated Feb 2025, maintainer Martin Ziqiao Ma. Curated list built out of the EMNLP Findings 2023 paper *"Towards A Holistic Landscape of Situated Theory of Mind in Large Language Models."* Six sections: community resources / surveys / cognitive underpinnings / foundation-model inquiry / computational modeling (prompting + Bayesian + RL) / applications (pragmatics, dialogue, language acquisition, HAI). Effectively the bibliography everyone else in the field starts from.

### Social-Simulation Frameworks (ToM-adjacent, ToM-relying)

- **joonspk-research/generative_agents** — `github.com/joonspk-research/generative_agents` — UIST 2023, Joon Sung Park, Joseph O'Brien, Carrie Cai, Meredith Ringel Morris, Percy Liang, Michael Bernstein (Stanford HCI). 25 generative agents in "Smallville" with GPT-3.5-driven **observation → memory stream → reflection → planning** loop. Agents gossip, throw a Valentine's Day party, propagate information. Doesn't call itself ToM but implements social reasoning: each agent maintains a model of other agents (relationships, recent interactions, beliefs). ~26K★ is easily the most-starred artifact in this whole digest.

- **StanfordHCI/genagents** — `github.com/joonspk-research/genagents` — 2024 successor. Scales the Smallville idea to **1,000 agents created from 2,000 hours of interviews**, plus a "demographic agent bank" of 3,000+ agents built on General Social Survey data. The design shift is important: v1 generated agents from fictional biographies, v2 grounds them in real human interviews, which changes what "believable human behavior" means.

- **sotopia-lab/sotopia** — `github.com/sotopia-lab/sotopia` — ICLR 2024 Spotlight, Xuhui Zhou, Hao Zhu, Leena Mathur et al. (CMU LTI). ~300★, MIT, 17 releases, 20 contributors. **600 episodes × 90 social scenarios** (negotiation / collaboration / competition / exchange), evaluated on 7 dimensions via the **SOTOPIA-EVAL** rubric: goal completion, believability, knowledge, relationship, secret-keeping, social rules, financial/material benefit. Top models ~7.6/10 vs. human 8.3/10. Has matured into a product (`pip install sotopia`, Redis or local-JSON backends, dashboards, `docs.sotopia.world`, `demo.sotopia.world`) and spawned **Sotopia-π** (interactive training) and **Sotopia-RL** (RL fine-tuning for social agents).

- **py499372727/AgentSims** — `github.com/py499372727/AgentSims` — ~940★, MIT, arXiv 2308.04026. Open-source sandbox for LLM evaluation via task-based simulation. Researchers add agents and buildings via GUI; deploy memory / planning / tool-use modules with a few lines of code. Python 97%, requires MySQL 8.0.31, live demo at `agentsims.com`. Pitched as an alternative to benchmark-based LLM eval: let agents *do things* in a simulated town and measure outcomes.

- **camel-ai/camel** — `github.com/camel-ai/camel` — 16.6K★, Apache 2.0. Builds "societies of agents with defined roles" on top of a `ChatAgent()` primitive. Three pitched use-cases: **data generation** (self-instruct + CoT synthesis), **task automation** (CRAB benchmark), **world simulation** (OASIS environment for large-scale social simulation). ToM shows up implicitly in role-playing conversation — an assistant agent and a user agent are each given a persona and must maintain it while cooperating. Pip-installable.

- **bigai-ai/ToM-RL** — `github.com/bigai-ai/ToM-RL` — BIGAI. Applies RL over ToM modeling for LLM agents; one of the few repos wiring ToM directly into an RL training loop rather than treating it as an eval.

- **SCAI-JHU/AutoToM** — `github.com/SCAI-JHU/AutoToM` — NeurIPS 2025 Spotlight. Automated Bayesian inverse planning + model discovery; claims SOTA on MMToM-QA and four other ToM benchmarks, plus "human-like confidence estimates" and embodied decision-making. The direction of travel for the MMToM lineage.

- **SCAI-JHU/MuMA-ToM** — `github.com/SCAI-JHU/MuMA-ToM` — AAAI 2025 Oral. Multi-modal, multi-agent ToM; extends MMToM-QA to embodied multi-agent interaction.

- **shawnsihyunlee/simulatedtom** — `github.com/shawnsihyunlee/simulatedtom` — Companion to the "Think Twice: Perspective-Taking Improves LLM's Theory-of-Mind Capabilities" (Wilf et al., 2023) / SimToM line. Implements SimToM prompting on BigToM + ToMi across GPT-3.5 / GPT-4 / Llama-2. Useful baseline harness.

## Key Techniques / Patterns

1. **The Sally–Anne backbone.** Every false-belief benchmark in this space descends (directly or structurally) from the Sally–Anne task: one character observes an object move, another doesn't; ask what each thinks. ToMi codifies it; Hi-ToM stacks it recursively; OpenToM enriches it with personality and attitude; ExploreToM generates it adversarially. The classical FB task is the unit cell.

2. **Information asymmetry as the generative principle.** FANToM, SimpleToM, ExploreToM, MindDial, and Sotopia all build their hard cases by constructing situations where *who knows what* diverges. "ToM is hard" reduces to "tracking information access is hard."

3. **Consistency scores beat single-question accuracy.** FANToM's `All*` score — a scenario is only correct if all aligned belief / answerability / info-access questions agree — drops GPT-4o from ~50% on individual items to 0.8% across scenarios. Any new humanization eval should require consistency, not pick-your-favorite-metric accuracy.

4. **Explicit vs. applied ToM.** SimpleToM's core move is to separate "can the model state the belief" from "does the model *act* on the belief." Most models can do the first and fail the second; interventions like CoT help only the first by default. Humanization projects should test applied, not explicit.

5. **Procedural / model-written generation against contamination.** BigToM, ToMBench (bilingual from scratch), ExploreToM (A* over DSL), and to an extent OpenToM all go out of their way to not reuse existing ToM item phrasings, specifically because LLM training sets now contain ToMi and Sally–Anne. Nearly every repo's README includes a "do not test in playgrounds that may train on input" warning.

6. **ATOMS-style ability decomposition.** ToMBench's 31-ability taxonomy (from Beaudoin's ATOMS framework) — Hidden Emotions, Discrepant Desires, Scalar Implicature, White Lies, Faux Pas, etc. — is the closest thing the field has to a shared *feature* space for social reasoning. SocialIQA predates it, Hi-ToM covers a slice, FANToM covers another. A humanization eval that picks 5–8 ability subsets and reports per-ability numbers is strictly more useful than one overall score.

7. **Bayesian Inverse Planning as the "principled" alternative to raw LLM ToM.** BIP-ALM (MMToM-QA), AutoToM (NeurIPS 2025 Spotlight), and MuMA-ToM all pair a symbolic planner with an LLM and claim the combination outperforms pure LLMs. This is the main non-prompt approach to ToM in the open-source stack.

8. **Prompt-time simulation of other minds.** SimulatedToM ("SimToM", `shawnsihyunlee/simulatedtom`) and OpenToM's `--simtom` flag implement the same pattern: *before* asking the belief question, prompt the model to describe what each character perceives. Consistent lifts across ToMi, BigToM, OpenToM. Cheap, portable, model-agnostic.

9. **Perspective-taking belief modules in dialogue generation.** MindDial's three-level belief (self / prediction of other / gap), CAMEL's role-playing assistant+user pair, Sotopia's per-agent SOTOPIA-EVAL with separate public vs. secret goals — the pattern is: store the other party's beliefs separately and consult them when generating.

10. **Social simulation as ToM evaluation.** Generative Agents / Sotopia / AgentSims don't score models on belief questions; they place agents in scenarios and measure whether emergent behavior is coherent (did Isabella actually invite Klaus to the party she planned? Did both Sotopia agents converge on a deal?). This is a different and complementary eval paradigm to QA.

11. **Multi-party > dyadic.** FANToM and MuMA-ToM both emphasize that most prior ToM benchmarks assume two parties, whereas interesting social reasoning happens at ≥3. The difficulty jump from 2 → 3 is large and currently under-tested elsewhere.

12. **Procedural generation with personality/intention variables.** OpenToM's explicit personality + intention + sentiment fields, and the BigToM causal-template approach (percepts × desires × actions), both push toward *controllable* ToM items where the experimenter can vary one dimension at a time. This is the direction humanization work should follow if it wants diagnostic rather than just binary results.

## Notable Quotes

- From `skywalker023/fantom` README disclaimer: *"We are not claiming that machines have minds. They do not have minds, emotions, or intentions. However, they do need social reasoning capabilities to better understand information."* — attribution: Kim et al., FANToM README.

- From `skywalker023/fantom` repo leaderboard caption: *"Please ensure that the performance on the control task remains stable when testing your method or model."* — attribution: Kim et al. The point being that FANToM's difficulty comes from the information-asymmetry condition, not from unreadable conversations; a model that can't even do the control is a broken harness, not a ToM result.

- From `yulinggu-cs/SimpleToM` README: *"Experiments reveal a striking gap: state-of-the-art models often reliably infer mental state, but fail at applying knowledge about the mental state for secondary predictions. … This exposes a critical fragility in LLMs' social reasoning in terms of what they know (explicit ToM) versus how well they can implicitly apply that knowledge for predictions (applied ToM)."* — attribution: Gu et al., SimpleToM.

- From `seacowx/OpenToM` README, on the data-contamination warning that appears almost verbatim across this whole repo cluster: *"Please avoid testing OpenToM questions in OpenAI playground or places where the data might be used for LLM training."* — attribution: Xu et al., OpenToM.

- From `zhchen18/ToMBench` README: *"ToMBench covers 8 theory-of-mind tasks … and 6 theory-of-mind ability categories and 31 specific theory-of-mind abilities from the ATOMS framework."* — attribution: Chen et al., ToMBench.

- From `sotopia-lab/sotopia` paper abstract (quoted in repo): *"Sotopia is an open-ended social learning environment that allows agents to interact with each other and the environment. The environment is designed to be a platform for evaluating and facilitating social intelligence in language agents."* — attribution: Zhou, Zhu et al., Sotopia.

- From `joonspk-research/generative_agents` paper (UIST 2023): *"Generative agents wake up, cook breakfast, and head to work; artists paint, while authors write; they form opinions, notice each other, and initiate conversations; they remember and reflect on days past as they plan the next day."* — attribution: Park et al., Generative Agents.

- From MMToM-QA news section, announcing AutoToM: *"AutoToM … achieves SOTA performance on MMToM-QA and four other ToM benchmarks, produces human-like confidence estimates, and supports embodied decision-making."* — attribution: Jin et al., MMToM-QA README (Feb 2025 update).

- From `cicl-stanford/procedural-evals-tom` / BigToM paper, on the model-written-evals approach: *"25 controls and 5,000 model-written evaluations … quality was validated through human ratings, which were higher than previous crowd-sourced evaluations and comparable to expert-written ones."* — attribution: Gandhi et al., BigToM (paraphrased from paper, reflected in repo README and project page).

- From `facebookresearch/ExploreToM` paper abstract: *"Llama-3.1-70B and GPT-4o achieved accuracies as low as 0% and 9% respectively on ExploreToM-generated data … fine-tuning on ExploreToM data yielded a 27-point accuracy improvement on the classic ToMi benchmark."* — attribution: Sclar et al., ExploreToM.

## Emerging Trends

- **From static benchmarks to adversarial generators.** ExploreToM (A*-over-DSL) and BigToM (causal templates) reflect a broader 2024–2025 shift: the community no longer trusts a fixed 1.2K-item JSON blob because frontier models have seen it. The new default is to ship a *generator* plus a small held-out sample.

- **Applied-ToM is eating explicit-ToM.** SimpleToM's thesis — that models' surface ability to state beliefs doesn't predict their ability to act on them — is being picked up in downstream work and is likely to become the headline metric in 2026 evals.

- **Conversation > narrative.** FANToM made explicit what the field had been sensing: Sally–Anne narratives are artificially easy because the narrator spells out who saw what. In natural conversation with entries/exits, models collapse. Expect more `fantom`-style conversation-native repos.

- **Multimodal + embodied.** MMToM-QA → MuMA-ToM → AutoToM is a clear trajectory: text → household video → multi-agent embodied. Bayesian inverse planning as the "interpretable bridge" between symbolic simulation and LLM inference is consolidating as the dominant non-LLM-only approach.

- **ToM in training loops, not just eval.** `bigai-ai/ToM-RL`, Sotopia-RL / Sotopia-π, and ExploreToM's demonstrated +27 points on ToMi via fine-tuning on generated data all point to ToM becoming a *training signal*, not just a test. This is the frontier.

- **Social simulators as emergent ToM testbeds.** Generative Agents (2023) → genagents (2024, interview-grounded 1K agents) → Sotopia (2024, formalized 7-dim rubric) → AgentSims + CAMEL/OASIS (world-scale). "ToM works" is being operationally redefined as "agents behave coherently in a simulated society," and the QA-benchmark subculture and the simulator subculture are starting to cite each other.

- **ATOMS as a shared taxonomy.** ToMBench's import of Beaudoin's ATOMS framework is becoming a *lingua franca* for what ToM even contains — emotion / desire / intention / knowledge / belief / non-literal communication, with 31 specific abilities. Before ATOMS was re-imported, every repo invented its own category scheme.

## Open Questions / Gaps

1. **No single canonical open-source ToM-enabled dialogue generator.** MindDial has no public code; CAMEL and Sotopia ship agents but don't expose a minimal "ToM layer" as a library. A clean, reusable `tom-dialogue` package with belief tracking, perspective-taking, and info-access modeling is missing.

2. **Training-data contamination is assumed but not measured.** Every repo bans playground testing; none publishes a reproducible leakage audit. The delta between "public ToMi" scores and "procedurally-regenerated ToMi" scores on the same model would be one of the most valuable missing numbers in the field.

3. **No cross-benchmark leaderboard.** Each repo runs its own models; there is no aggregated public leaderboard that pools ToMi + Hi-ToM + FANToM + SimpleToM + ToMBench + OpenToM + BigToM + MMToM-QA + SocialIQA into one ranking. Awesome-theory-of-mind links them but doesn't aggregate.

4. **Non-English coverage thin.** ToMBench is the only serious bilingual entry; everything else is English-only. The structural intuition of false belief may transfer; the vocabulary, pragmatics, and politeness norms probably don't.

5. **Generator reproducibility.** ExploreToM's data generation is model-specific ("users testing other models should regenerate data adversarially for their specific model"). In practice, this means comparing two models on ExploreToM is delicate. No standard "ExploreToM-v1 frozen set" exists and this may be by design but limits apples-to-apples comparison.

6. **ToM vs. linguistic shortcuts.** ToMi's own motivating paper was about *cleaning up* Sally–Anne to prevent shortcut solutions. Whether the next generation (OpenToM, ToMBench, ExploreToM) is genuinely shortcut-free, or just has *different* shortcuts frontier models haven't yet exploited, is an open empirical question.

7. **Intervention studies are rare.** SimpleToM shows CoT targeted prompting recovers applied-ToM accuracy from ~50% to ~93%. This is a massive swing but comes from one repo. Nobody has systematically measured which prompting, scaffolding, or fine-tuning interventions move which ATOMS ability, across which benchmarks.

8. **Social simulation → ToM metric conversion.** Generative Agents, Sotopia, AgentSims all *rely on* ToM but don't *score* it. Extracting a ToM-specific metric from agent transcripts (did the agent act consistent with the other's known beliefs?) would unify the QA and simulation camps, but no public tooling does this.

9. **Evaluation of ToM in the humanizer use case itself.** None of these benchmarks measures whether a *humanizer* (in the sense of a system rewriting AI output to sound human) preserves the user's beliefs, model of the audience, or pragmatic intent. This is the direct overlap with the Unslop project and is completely open.

10. **MindDial and MindDial-like belief-module work is under-reproduced.** The three-level belief module (self / model-of-other / gap) is an architecturally elegant idea that hasn't been picked up in open code anywhere. Someone implementing it as a drop-in agent wrapper would meaningfully move the field.

## References

- `github.com/facebookresearch/ToMi` — Le/Boureau/Nickel, EMNLP 2019; foundational procedural FB benchmark.
- `github.com/ying-hui-he/Hi-ToM_dataset` — Hi-ToM, EMNLP Findings 2023; 4th-order ToM with deceptive agents.
- `github.com/seacowx/OpenToM` — Xu et al., ACL 2024; 696 narratives × 23 questions, personality+intention metadata.
- `github.com/cicl-stanford/procedural-evals-tom` — BigToM, Gandhi et al., NeurIPS 2023; causal templates.
- `github.com/shawnsihyunlee/simulatedtom` — SimToM prompting + BigToM/ToMi harness.
- `github.com/zhchen18/ToMBench` — Chen et al., ACL 2024; bilingual 2,860 items, ATOMS 31 abilities.
- `github.com/facebookresearch/ExploreToM` — Sclar et al., ICLR 2025; A* / DSL adversarial generator, +27 on ToMi via fine-tune.
- `github.com/skywalker023/fantom` — Kim et al., EMNLP 2023; multi-party conversation ToM, strict `All*` score.
- `github.com/yulinggu-cs/SimpleToM` — Gu et al., ICLR 2026; explicit vs. applied ToM gap.
- `github.com/chuanyangjin/MMToM-QA` — Jin et al., ACL 2024 Outstanding Paper; multimodal + BIP-ALM.
- `github.com/SCAI-JHU/AutoToM` — Jin et al., NeurIPS 2025 Spotlight; automated Bayesian inverse planning.
- `github.com/SCAI-JHU/MuMA-ToM` — AAAI 2025 Oral; multi-agent multimodal ToM.
- `huggingface.co/datasets/allenai/social_i_qa` — Sap et al., EMNLP 2019; 38K social commonsense MCQs.
- `arxiv.org/abs/2306.15253` — MindDial, Qiu/Zhu/Zheng, SIGDIAL 2024 (no public code).
- `github.com/Mars-tin/awesome-theory-of-mind` — canonical ToM reading list.
- `github.com/joonspk-research/generative_agents` — Park et al., UIST 2023; Smallville 25-agent simulacra.
- `github.com/joonspk-research/genagents` — StanfordHCI; 1,000 interview-grounded agents.
- `github.com/sotopia-lab/sotopia` — Zhou, Zhu et al., ICLR 2024 Spotlight; social-intelligence sandbox + SOTOPIA-EVAL.
- `github.com/py499372727/AgentSims` — LLM evaluation sandbox, ACL 2023 arXiv, MIT.
- `github.com/camel-ai/camel` — CAMEL multi-agent society, role-playing + OASIS world simulation.
- `github.com/bigai-ai/ToM-RL` — BIGAI; RL over ToM modeling.
