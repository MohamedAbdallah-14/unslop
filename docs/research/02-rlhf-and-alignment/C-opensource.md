# RLHF & Alignment — Open-Source & GitHub

> Research dossier for the **Unslop** project ("Humanizing AI output and thinking").
> Scope: Category 02 · Angle **C — Open-Source Tooling & GitHub**. Covers libraries, frameworks, and open datasets that the community uses to steer large language models toward human-preferred output via RLHF, DPO, Constitutional AI, and related post-training recipes.
> Date of sweep: April 2026.

---

## Executive Summary

Open-source RLHF tooling has matured from a handful of research forks in 2022–2023 into a stratified ecosystem in 2025–2026. Three clear layers have emerged:

1. **Trainer libraries** — Hugging Face's **TRL** is now the de facto post-training toolbox (SFT/DPO/GRPO/reward modeling, plus a TRL v1 release in March 2026). It is complemented by **OpenRLHF** (Ray + vLLM, high-throughput agentic RL), ByteDance's **veRL / HybridFlow** (SOTA throughput with 3D-HybridEngine, scales to 671B MoE), **NVIDIA NeMo-Aligner** (superseded by NeMo RL in May 2025), **DeepSpeed-Chat** (the original three-stage pipeline, now largely historical), and **CarperAI trlx** (archived but still cited).
2. **Wrapper / recipe frameworks** — **LLaMA-Factory** (~70k stars, 100+ models, CLI + Web UI), **Axolotl** (11.5k stars, YAML-driven fine-tuning), and HF's **alignment-handbook** (reproducible Zephyr and ORPO recipes) lower the barrier to running the same pipelines TRL/veRL expose.
3. **Preference data and safety scaffolding** — Community-built preference corpora (**UltraFeedback**, **HelpSteer3**, **HH-RLHF**, **OpenAssistant/oasst2**, **PKU-SafeRLHF**) and simulation frameworks (**AlpacaFarm**, Anthropic's Constitutional AI / RLAIF recipe) replace expensive human labeling and make it feasible to train "humane" behaviors (helpful, honest, harmless, non-robotic) without an in-house annotation team.

**What matters for humanizing AI output:** The biggest signal for this project is the decisive shift from PPO-style RLHF toward **direct preference methods** (DPO, IPO, KTO, ORPO, SimPO, GRPO) plus **fine-grained preference data with rubric-level labels** (honesty, truthfulness, verbalized calibration, edit quality, multilingual naturalness). LIMA's "1,000 curated examples beat massive RLHF" result reframes humanization as a **data-curation problem** rather than a compute problem, and Constitutional AI demonstrates how to bake style/tone principles ("don't use meta-commentary", "sound like a thoughtful human", etc.) into a self-critique loop without human labels.

**Key gap:** Almost every framework optimizes helpfulness, harmlessness, or reasoning accuracy. **None explicitly target "human-sounding" output** as a named alignment objective — this is an open whitespace Unslop can fill with a custom reward/principle set on top of TRL or OpenRLHF.

---

## Sources

### 1. TRL — Transformers Reinforcement Learning
- **Repo:** [huggingface/trl](https://github.com/huggingface/trl)
- **Author/Org:** Hugging Face (von Werra, Belkada, Tunstall, Beeching, Lambert, et al.)
- **Stars / Updated:** ~17.9k · actively maintained (TRL v1 released March 27, 2026)
- **License:** Apache-2.0
- **What it does:** Full-stack post-training library integrated with 🤗 Transformers, Accelerate, PEFT, and DeepSpeed. Exposes `SFTTrainer`, `DPOTrainer`, `GRPOTrainer`, `RewardTrainer`, `RLOOTrainer`, plus a `trl` CLI.
- **Techniques:** SFT, DPO, GRPO (the algorithm used to train DeepSeek-R1), PPO, RLOO, reward modeling, reasoning reward functions, vision-language alignment, Liger kernels, Unsloth integration, co-located vLLM for GPU efficiency, OpenEnv integration for agentic RL, Open-R1 reproduction.
- **Takeaways for Unslop:** Easiest on-ramp for DPO/GRPO on preference pairs. `DPOTrainer` + a UltraFeedback-style "humanness" dataset is a ~50-line project. TRL v1 explicitly positions itself as "a post-training library that holds when the field invalidates its own assumptions" — i.e., algorithm-agnostic.
- **Summary (2–3 sentences):** TRL is the reference post-training stack for the Hugging Face ecosystem, covering every major preference-optimization algorithm behind a uniform trainer API. It scales from single-GPU QLoRA to multi-node DeepSpeed/FSDP and is the library most third-party humanization work builds on top of.

### 2. trlx
- **Repo:** [CarperAI/trlx](https://github.com/CarperAI/trlx)
- **Author/Org:** CarperAI (Stability-adjacent community)
- **Stars / Updated:** 4,743 · last release v0.7.0 (June 2023), last commit January 2024 (effectively archived)
- **License:** MIT
- **What it does:** Distributed RLHF training for models up to 20B (Accelerate) and beyond (NeMo-Megatron). Implements PPO and **Implicit Language Q-Learning (ILQL)**.
- **Techniques:** PPO, ILQL (an offline RL alternative to PPO), reward-labeled datasets, prompt-completion datasets, Accelerate + NeMo-Megatron backends.
- **Takeaways for Unslop:** Historically important (one of the first open PPO-for-LLM libs), but no longer actively maintained. Its ILQL implementation is still a useful reference for offline methods if DPO is deemed insufficient.
- **Summary:** trlx was the community's first serious distributed RLHF framework and is still the canonical open-source reference for ILQL. It has been overtaken by TRL and OpenRLHF but the repo remains widely cited in 2023–2024 RLHF papers.

### 3. OpenRLHF
- **Repo:** [OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)
- **Author/Org:** OpenRLHF community (originally `hijkzzz`)
- **Stars / Updated:** ~20k+ · highly active (v0.10 in April 2026 with multi-turn VLM RL)
- **License:** Apache-2.0
- **What it does:** High-performance RLHF framework built on **Ray + vLLM + DeepSpeed** with an agent-based execution paradigm. Separates Actor / Reward / Reference / Critic across GPUs with hybrid-engine scheduling.
- **Techniques:** PPO, REINFORCE++, REINFORCE++-baseline, GRPO, RLOO, DPO, iterative DPO, IPO, cDPO, KTO, rejection sampling; LoRA RL; async agent RLHF; multi-turn VLM RLHF; reward-model ensembling; vLLM-accelerated generation (claims 2×+ vs. DeepSpeed-Chat).
- **Takeaways for Unslop:** Best-in-class when training >13B humanization models or when multi-turn/agentic rollouts are needed (e.g., scoring human-likeness after a whole conversation). The agent-based execution model is unusually clean for custom reward functions.
- **Summary:** OpenRLHF is the most production-ready open RLHF stack for Ray + vLLM deployments, and arguably the highest-throughput open framework that is still approachable. It pioneered REINFORCE++ and now supports agentic and VLM RL out of the box.

### 4. DeepSpeed-Chat
- **Repo:** [deepspeedai/DeepSpeedExamples/applications/DeepSpeed-Chat](https://github.com/microsoft/DeepSpeedExamples/blob/master/applications/DeepSpeed-Chat/README.md)
- **Author/Org:** Microsoft / DeepSpeed team
- **Stars / Updated:** parent repo ~6.8k · last major RLHF updates Aug 2023 (Llama 2 support); largely superseded
- **License:** Apache-2.0 / MIT
- **What it does:** End-to-end three-stage RLHF pipeline (SFT → Reward Model → PPO) implemented on top of DeepSpeed ZeRO. Single-script `e2e_rlhf.py` runs all three stages; `DeepSpeedRLHFEngine` and `DeepSpeedPPOTrainer` handle the actor/critic/reward/reference orchestration.
- **Techniques:** Classic three-stage RLHF, ZeRO-2/3 offload, Hybrid Engine (shared weights between training and generation), EMA checkpoint, PPO-ptx with SFT loss mixing, support for 125M→66B models.
- **Takeaways for Unslop:** Still the clearest pedagogical reference for the full RLHF pipeline. Most modern frameworks (OpenRLHF, veRL) explicitly benchmark against it. Not recommended for new work.
- **Summary:** DeepSpeed-Chat is the canonical open-source recreation of InstructGPT's three-stage RLHF pipeline, and it is what most people mean when they say "standard RLHF." Active development has largely moved to newer frameworks, but it remains the most readable pipeline for learning.

### 5. Axolotl
- **Repo:** [axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl) (originally OpenAccess AI Collective)
- **Author/Org:** Axolotl AI Cloud / OpenAccess AI Collective
- **Stars / Updated:** 11,568 · highly active (weekly releases; MoE LoRA, ScatterMoE, GDPO, EAFT added in early 2026)
- **License:** Apache-2.0
- **What it does:** YAML-driven fine-tuning framework wrapping TRL and custom kernels. Supports SFT, DPO, KTO, ORPO, GRPO, plus MoE expert training, multi-modal, and distributed (FSDP2, ND parallelism, Distributed Muon).
- **Techniques:** LoRA/QLoRA, DoRA, ScatterMoE LoRA, GDPO (Generalized DPO), EAFT (Entropy-Aware Focal Training), sample packing, Liger kernels, SageAttention, long-context (Scalable Softmax).
- **Takeaways for Unslop:** Best path from "I have a jsonl of preferred vs. rejected humanized responses" to a trained DPO model with minimal code. Config-first means reproducibility is trivial.
- **Summary:** Axolotl is the community's favorite config-first fine-tuning framework, sitting above TRL and offering working recipes for almost every modern open model. Its cadence of day-0 support for new architectures makes it the most pragmatic choice for iteration-heavy humanization work.

### 6. LLaMA-Factory
- **Repo:** [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
- **Author/Org:** Yaowei Zheng et al. (ACL 2024)
- **Stars / Updated:** ~70k · v0.9.4 released Dec 31 2025; active April 2026. Used by Amazon, NVIDIA, Aliyun.
- **License:** Apache-2.0
- **What it does:** Unified fine-tuning framework for 100+ LLMs and VLMs with **zero-code CLI and Gradio Web UI** (LLaMA Board).
- **Techniques:** Pre-training, SFT, reward modeling, **PPO, DPO, KTO, ORPO, SimPO**, GaLore, BAdam, APOLLO, Muon, OFT, DoRA, LongLoRA, LLaMA Pro, Mixture-of-Depths, LoRA+, PiSSA, FlashAttention-2, Unsloth, Liger Kernel, KTransformers (1T-param training on 2×4090), NEFTune, rsLoRA, FSDP+QLoRA.
- **Takeaways for Unslop:** The most approachable end-to-end trainer. Non-ML-engineer stakeholders can retrain a humanization LoRA in the browser via LLaMA Board. Ships preference datasets (UltraFeedback-binarized, HH-RLHF, DPO-En-Zh-20k) out of the box.
- **Summary:** LLaMA-Factory is the most widely adopted open fine-tuning framework and the one most non-researchers actually use. Its integration of 8+ preference-learning algorithms, a web UI, and dataset bundling makes it a strong default front-end for a humanization product.

### 7. veRL (Volcano Engine RL)
- **Repo:** [verl-project/verl](https://github.com/verl-project/verl) (formerly volcengine/verl)
- **Author/Org:** ByteDance Seed team → verl-project community
- **Stars / Updated:** 20k+ · extremely active (PyTorch Conference EU 2026, NVIDIA GTC 2026)
- **License:** Apache-2.0
- **What it does:** Flexible, efficient, production-ready RL training library for LLMs. Open-source implementation of the **HybridFlow** paper (EuroSys 2025).
- **Techniques:** PPO, GRPO, GSPO, ReMax, REINFORCE++, RLOO, PRIME, DAPO, DrGRPO, KL_Cov & Clip_Cov, SPPO, PF-PPO, VAPO; FSDP/FSDP2, Megatron-LM, vLLM, SGLang; 3D-HybridEngine for actor resharding; multi-turn tool calling; VLM RL; scales to 671B MoE and trillion-parameter LoRA RL; expert parallelism.
- **Takeaways for Unslop:** If humanization ever needs agentic / multi-turn / tool-using RL (e.g., a judge agent evaluating humanness), veRL is the state of the art. DAPO and VAPO achieve SOTA reasoning without losing naturalness.
- **Summary:** veRL is the fastest and most algorithmically diverse open RL framework for LLMs in 2026, powering ByteDance's Doubao and Seed-Thinking as well as multiple frontier research papers. It is heavier to operate than TRL but essential for frontier-scale humanization research.

### 8. NVIDIA NeMo-Aligner
- **Repo:** [NVIDIA/NeMo-Aligner](https://github.com/NVIDIA/NeMo-Aligner/)
- **Author/Org:** NVIDIA
- **Stars / Updated:** 851 · **No longer actively maintained as of May 15, 2025** (succeeded by NeMo RL)
- **License:** Apache-2.0
- **What it does:** Scalable alignment toolkit on top of NeMo with tensor/data/pipeline parallelism across thousands of GPUs and TensorRT-LLM-accelerated generation.
- **Techniques:** SFT, Reward Model training, PPO, **REINFORCE**, DPO (with sequence packing), **SteerLM** (attribute-conditioned SFT as an RLHF alternative), Nemotron-4-340B recipes.
- **Takeaways for Unslop:** SteerLM is interesting prior art — conditioning on attribute labels (helpfulness, correctness, coherence, complexity, verbosity) as an alternative to RLHF. Could map directly to "humanness" as a conditioning attribute.
- **Summary:** NeMo-Aligner was NVIDIA's large-scale alignment toolkit and shipped Nemotron-4-340B's full post-training recipe. While deprecated in favor of NeMo RL, its SteerLM technique remains a useful pattern for conditional alignment.

### 9. Hugging Face alignment-handbook
- **Repo:** [huggingface/alignment-handbook](https://github.com/huggingface/alignment-handbook)
- **Author/Org:** Hugging Face H4 team (Tunstall, Beeching, et al.)
- **Stars / Updated:** 5,554 · last major release with Zephyr-141B-A35B (April 2024); occasional updates
- **License:** Apache-2.0
- **What it does:** Reproducible recipes for aligning models with human and AI preferences. Produced **Zephyr-7B-β** (the reference SFT→DPO recipe) and **Zephyr-141B-A35B** (ORPO on Mixtral 8x22B).
- **Techniques:** SFT on filtered UltraChat → DPO on UltraFeedback; ORPO; QLoRA variants (sft-full, sft-qlora, dpo-full, dpo-qlora); accelerate configs for DeepSpeed ZeRO-3 and FSDP.
- **Takeaways for Unslop:** The Zephyr recipe is the single most copied alignment recipe in the community. For a humanization model, the pattern is: SFT on filtered high-quality human-like corpus + DPO on humanness-preference pairs, exactly mirroring the Zephyr flow.
- **Summary:** The alignment-handbook is Hugging Face's "canonical recipe" companion to TRL, with working YAML configs for the Zephyr line of models. It is the fastest way to stand up a publishable SFT+DPO pipeline.

### 10. Direct Preference Optimization (reference implementation)
- **Repo:** [eric-mitchell/direct-preference-optimization](https://github.com/eric-mitchell/direct-preference-optimization)
- **Author/Org:** Eric Mitchell (Stanford)
- **Stars / Updated:** 2,882 · last commit August 2024
- **License:** Apache-2.0
- **What it does:** Reference implementation of the DPO paper ("Your Language Model is Secretly a Reward Model", NeurIPS 2023). Supports any causal Hugging Face model, DPO + **conservative DPO** (label smoothing) + **IPO**.
- **Techniques:** DPO loss, cDPO label smoothing, IPO variant, two-stage pipeline (SFT → preference learning).
- **Takeaways for Unslop:** Clean single-file trainer, useful as a reading companion even though production training should use TRL's `DPOTrainer`.
- **Summary:** This is the historical reference DPO implementation cited by virtually every DPO paper since. It is small enough to read end-to-end in an hour and includes cDPO/IPO variants that the TRL wrapper now exposes.

### 11. Safe-RLHF / PKU Beaver
- **Repo:** [PKU-Alignment/safe-rlhf](https://github.com/PKU-Alignment/safe-rlhf)
- **Author/Org:** PKU-Alignment, Peking University (ICLR 2024 Spotlight)
- **Stars / Updated:** ~1.5k · Beaver-v1/v2/v3 released; PKU-SafeRLHF dataset v1.0 (June 2024, 300k+ labeled pairs, updated toward 1M)
- **License:** Apache-2.0
- **What it does:** Constrained-optimization RLHF that jointly maximizes helpfulness subject to safety constraints via a separate **Reward Model + Cost Model**. Full SFT → RM → Cost Model → Safe-PPO pipeline.
- **Techniques:** Safe-PPO with a Lagrangian for the safety constraint, helpful/harmless decomposition, multi-scale evaluation (BIG-bench, GPT-4 judge).
- **Takeaways for Unslop:** The decomposition of a single "preferred" signal into **separate reward dimensions** (helpfulness, safety, etc.) maps directly onto a humanization need: separate "correctness" and "human-soundingness" rewards so that the model doesn't sacrifice accuracy to sound casual.
- **Summary:** Safe-RLHF pioneered explicit multi-objective alignment with a constrained-optimization framing rather than a single scalar reward. The approach of training separate reward heads is directly portable to humanization (style reward + task reward).

### 12. Constitutional AI — open implementations
- **Repos:**
  - [anthropics/claude-constitution](https://github.com/anthropics/claude-constitution) (the constitution document itself, CC0-1.0)
  - [Azazel5/Constituitional-AI](https://github.com/Azazel5/Constituitional-AI) (community reimplementation)
  - Hugging Face `constitutional-ai` recipes inside `alignment-handbook`
- **Author/Org:** Anthropic (original paper) + community reimplementations
- **Stars / Updated:** community repos small (tens–hundreds), active in 2024–2025
- **What it does:** Two-phase alignment: (1) **Supervised CAI** — model critiques and revises its own responses against a set of natural-language principles; (2) **RLAIF** — reinforcement learning from AI-generated preference labels rather than human ones.
- **Techniques:** Self-critique with principle sampling, revise-in-context, AI preference labeling, reward model distillation from AI judgments.
- **Takeaways for Unslop:** **The most directly applicable pattern for humanization.** The constitution can be literally a list of humanness principles: "Don't use meta-commentary," "Vary sentence length," "Avoid stock LLM phrases ('As an AI language model'), "Sound like a thoughtful human writer." RLAIF removes the need for human preference labels at scale. One community repo noted prompt-engineering improvements including "eliminating meta-commentary in revision responses" — exactly a humanization concern.
- **Summary:** Constitutional AI / RLAIF is the most scalable way to inject stylistic and tonal principles into a model without human labels. Anthropic released the Claude Constitution under CC0 and multiple community reimplementations exist — these are the ideal starting points for a principle-based humanness trainer.

### 13. AlpacaFarm
- **Repo:** [tatsu-lab/alpaca_farm](https://github.com/tatsu-lab/alpaca_farm)
- **Author/Org:** Tatsunori Hashimoto's lab, Stanford (arXiv 2305.14387)
- **Stars / Updated:** ~800 · v0.2.0 (Feb 2024); text-davinci-003 annotator deprecated, switched to GPT-4
- **License:** Apache-2.0 (code), CC-BY-NC-4.0 (dataset)
- **What it does:** Simulation framework for RLHF research. Simulates pairwise preference feedback with LLM annotators, provides automated evaluation, and ships reference implementations of PPO, DPO, best-of-n, and expert iteration.
- **Techniques:** LLM-as-annotator (claims 45–50× cheaper than humans, high human agreement), automated win-rate evaluation, baseline RLHF methods. End-to-end validated: rankings on AlpacaFarm match rankings trained on real human data.
- **Takeaways for Unslop:** The simulator is nearly purpose-built for the humanization use case — it lets you iterate on humanness-reward models without ever running a human study. Their reference PPO achieves +10% win-rate vs. davinci003, a useful sanity baseline.
- **Summary:** AlpacaFarm is the most rigorous open simulation framework for RLHF experimentation without human labels. For a humanization product, its architecture (LLM judge → simulated preferences → standard RL pipeline) is directly reusable with a swapped-in "humanness" judge prompt.

### 14. UltraFeedback
- **Repo:** [OpenBMB/UltraFeedback](https://github.com/OpenBMB/UltraFeedback) · **Dataset:** [openbmb/UltraFeedback on HF](https://huggingface.co/datasets/openbmb/UltraFeedback)
- **Author/Org:** OpenBMB (THUNLP)
- **Size:** 64k prompts × 4 completions = **256k responses**, 380k annotations (potentially ~1M comparison pairs).
- **License:** MIT (dataset)
- **What it does:** Large-scale **fine-grained preference dataset** with GPT-4 annotations across four aspects: instruction-following, truthfulness, honesty, helpfulness. Responses from 17 different models spanning LLaMA/Falcon/MPT/StarChat/Pythia families.
- **Techniques:** Principle-sampled prompting (Helpfulness, Truthfulness, Honesty, **Verbalized Calibration**, Harmless), per-axis scoring, rationales. Powers **UltraRM** (92.3% win-rate vs. davinci003 on AlpacaEval) and **UltraCM**.
- **Takeaways for Unslop:** The fine-grained schema is a proven template for multi-dimensional reward modeling. A humanization dataset could use the same four-axis format, substituting "naturalness / authenticity / register-match / low-AI-tell" for the UltraFeedback axes. Note the December 2023 fix of ~2,628 mis-scored completions — a reminder that LLM-judged data requires careful auditing.
- **Summary:** UltraFeedback is the most influential open preference dataset of the post-ChatGPT era and the training data behind Zephyr. Its multi-axis rubric is the template any serious humanization reward model should copy.

### 15. OpenAssistant (oasst / oasst2)
- **Repo:** [LAION-AI/Open-Assistant](https://github.com/LAION-AI/Open-Assistant) · **Dataset:** [OpenAssistant/oasst2](https://huggingface.co/datasets/OpenAssistant/oasst2)
- **Author/Org:** LAION + open community (thousands of volunteers)
- **Stars / Updated:** 37.4k · **Project completed April 2024**; oasst2 is the final dataset.
- **License:** Apache-2.0 (code), Apache-2.0 (data)
- **What it does:** Crowdsourced multi-turn conversation tree dataset with human-written prompts and human-ranked responses across 35+ languages. Full-stack chat platform for collecting the data.
- **Techniques:** Message-tree data model (conversations as DAGs), ranking + quality labels + category tags, multilingual, both SFT and RM training splits.
- **Takeaways for Unslop:** oasst/oasst2 is the largest **human-authored** conversational corpus with quality ratings. For a humanization model, it is training data that is human by construction — an excellent SFT base before DPO.
- **Summary:** OpenAssistant is the community answer to "where do you get human conversation data if you don't have an annotation budget?" The project is now archived but its two dataset releases (oasst1, oasst2) are still core SFT ingredients for open chat models.

### 16. LIMA
- **Paper / Dataset:** [arXiv 2305.11206](https://arxiv.org/abs/2305.11206) · [GAIR/lima on HF](https://huggingface.co/datasets/GAIR/lima)
- **Author/Org:** Meta AI (Zhou et al., NeurIPS 2023)
- **Size:** 1,000 curated prompt–response pairs (~750k tokens) from Stack Exchange, wikiHow, Reddit WritingPrompts, Natural Instructions, and 200 hand-written examples.
- **License:** CC-BY-NC (dataset)
- **What it does:** Demonstrates that **1,000 carefully curated examples, with no RLHF and no human preference modeling**, can fine-tune a 65B LLaMA to match or beat GPT-4 in 43% of comparisons and beat DaVinci003 in 65%.
- **Techniques:** Hand-curation for style/format diversity, extreme data minimalism, no RL at all.
- **Takeaways for Unslop:** The most important single data point in this dossier. For humanization, it suggests that **a few thousand hand-curated "human-sounding" responses** may beat industrial-scale DPO/RLHF. Consider LIMA-style curation as the v1 strategy before any RL.
- **Summary:** LIMA's "superficial alignment hypothesis" claims that alignment teaches style and format on top of knowledge already learned in pretraining. If true, humanization is primarily a curation problem, and LIMA is the blueprint.

### 17. HelpSteer / HelpSteer3
- **Dataset:** [nvidia/HelpSteer3 on HF](https://huggingface.co/datasets/nvidia/HelpSteer3) · Paper [arXiv 2505.11475](https://arxiv.org/abs/2505.11475)
- **Author/Org:** NVIDIA
- **Size:** 40k+ human-annotated samples across STEM, coding, and 12 languages; multiple configs (Preference, Feedback, Edit, Edit-Quality, Principle).
- **License:** CC-BY-4.0
- **What it does:** Open human-annotated preference dataset with **multi-attribute ratings** (helpfulness, correctness, coherence, complexity, verbosity) and a novel **Edit** config where annotators rewrite responses to improve them.
- **Techniques:** Multi-attribute rating (precursor to SteerLM), edit-based supervision, multilingual preferences, ITS (Inference-Time Scaling) configs.
- **Takeaways for Unslop:** The **Edit** configuration is gold — it captures not just "A is better than B" but *how* a human would rewrite an AI response to be better. This is almost exactly the training signal for a humanization/rewriter model.
- **Summary:** HelpSteer3 is the most carefully constructed open human-preference dataset in 2025–2026, and its Edit config gives before/after pairs that directly encode "what an LLM response is missing to sound human." Models trained on it hit 85.5% on RM-Bench and 93.4% on Arena Hard.

---

## Key Techniques / Patterns

Patterns consistently observed across the 17 projects above:

1. **DPO is the default; PPO is for scale.** Every 2024+ framework ships DPO (often plus KTO, ORPO, SimPO) as the first-class preference method. PPO is reserved for multi-turn / agentic / reasoning settings (OpenRLHF, veRL).
2. **GRPO is the new PPO for reasoning.** TRL, OpenRLHF, and veRL all added GRPO in 2024–2025; DeepSeek-R1 made it mainstream. For stylistic/humanization goals, GRPO's group-relative advantage is overkill but works fine.
3. **Three-stage → two-stage collapse.** The DeepSpeed-Chat pattern (SFT → RM → PPO) has been largely collapsed to **SFT → DPO** because DPO dispenses with the separate reward model. The Zephyr recipe is the canonical two-stage pipeline.
4. **Multi-axis reward / preference schemas.** UltraFeedback (4 axes), HelpSteer3 (5 axes), Safe-RLHF (helpfulness + cost), SteerLM (conditioned attributes). The community has abandoned single-scalar preferences.
5. **LLM-as-judge everywhere.** AlpacaFarm, UltraFeedback, and most 2024+ preference datasets use GPT-4-class judges. Humans are used for validation, not primary labeling.
6. **Ray + vLLM as the RL runtime standard.** OpenRLHF and veRL both built on Ray + vLLM; TRL added co-located vLLM in June 2025. Generation is ~80% of RL wall time, so vLLM integration is now table stakes.
7. **YAML-driven config layers over Python trainers.** Axolotl, LLaMA-Factory, alignment-handbook all converge on config-first UX. Unslop should ship a config layer, not expose TRL directly.
8. **Self-critique / RLAIF as a label-free alternative.** Constitutional AI's two-phase recipe (revise-under-principles → RLAIF) removes the human-labeling bottleneck entirely.
9. **Minimal-data alignment (LIMA).** The alternative narrative: don't scale data, curate it. Tiny datasets (1k) with extreme quality control can match RLHF.
10. **Edit-based supervision (HelpSteer3 Edit).** Rewrite-and-rate beats pure rating for teaching a model *how* to be better, not just which of two options is better. Directly applicable to humanization.

---

## Notable Quotes

From the READMEs and papers surveyed:

> "TRL is a cutting-edge library designed for post-training foundation models using advanced techniques like Supervised Fine-Tuning (SFT), Group Relative Policy Optimization (GRPO), and Direct Preference Optimization (DPO)." — **huggingface/trl** README

> "TRL v1 — a Post-Training Library That Holds When the Field Invalidates Its Own Assumptions." — **TRL v1 release blog**, March 2026

> "OpenRLHF is **the first** high-performance, production-ready open-source RLHF framework that combines **Ray + vLLM distributed architecture** with a **unified agent-based design paradigm**." — **OpenRLHF** README

> "RLHF training spends **80% of the time on sample generation**." — **OpenRLHF** README (on why vLLM integration is load-bearing)

> "verl is a flexible, efficient and production-ready RL training library for large language models (LLMs). verl is the open-source version of **HybridFlow: A Flexible and Efficient RLHF Framework** paper." — **verl-project/verl** README

> "Efficient actor model resharding with 3D-HybridEngine: Eliminates memory redundancy and significantly reduces communication overhead during transitions between training and generation phases." — **verl** README

> "A fast, affordable, scalable and open system framework for enabling end-to-end Reinforcement Learning Human Feedback (RLHF) training experience to generate high-quality ChatGPT-style models at all scales." — **DeepSpeed-Chat** README

> "Easily fine-tune 100+ large language models with zero-code CLI and Web UI." — **LLaMA-Factory** README

> "Go ahead and axolotl questions." — **Axolotl** tagline (the project's literal slogan)

> "Robust recipes to continue pretraining and to align language models with human and AI preferences." — **alignment-handbook** README

> "We measure that AlpacaFarm is faithful to human feedback (simulated reference methods match the human rankings with 0.98 correlation) and 45–50× cheaper." — **AlpacaFarm** paper

> "Developed to improve the alignment of general language models through scalable and diverse preference data." — **UltraFeedback** README, on the motivation for multi-axis preference annotation

> "We define a superficial alignment hypothesis: A model's knowledge and capabilities are learnt almost entirely during pretraining, while alignment teaches it which subdistribution of formats should be used when interacting with users." — **LIMA** paper

> "Constitutional AI: Harmlessness from AI Feedback… we train a non-evasive and relatively harmless AI assistant using a combination of supervised learning from AI feedback (SL-CAI) and reinforcement learning from AI feedback (RL-CAI)." — **Anthropic Constitutional AI** paper (cited in community implementations)

> "Claude's Constitution, released under Creative Commons Zero (CC0-1.0) for transparency into how Claude is trained." — **anthropics/claude-constitution** README

> "Beaver is the first framework to support RLHF for constrained reward maximization in language models, guaranteeing safety via cost constraints." — **PKU-Alignment/safe-rlhf** (Beaver) project page

> "OpenAssistant is a chat-based assistant that understands tasks, can interact with third-party systems, and retrieve information dynamically to do so… **The project is completed.** The final published oasst2 dataset can be found on HuggingFace." — **LAION-AI/Open-Assistant** README

> "HelpSteer3-Preference can be used to train Reward Models (RMs) with Llama 3.3 models, achieving **85.5% on RM-Bench and 78.6% on JudgeBench**." — **HelpSteer3** dataset card

---

## Emerging Trends

1. **DPO-and-variants as commodity.** Between 2023 (release of DPO) and 2026, every major framework shipped DPO plus 3–5 variants (IPO, cDPO, KTO, ORPO, SimPO, GDPO). A March 2025 survey (arXiv 2503.11701) taxonomizes over a dozen named variants including MinMax-DPO, MallowsPO, ODPO, MPO, and GaPO. The algorithm is no longer a competitive moat; the data and reward function are.
2. **GRPO, REINFORCE++, and value-free RL.** Driven by DeepSeek-R1's success (January 2025), 2025 saw a wave of value-function-free on-policy methods (GRPO, REINFORCE++, RLOO, ReMax, DAPO, VAPO). DAPO (arXiv 2503.14476) adds asymmetric clipping and dynamic sampling; VAPO (arXiv 2504.05118) achieves 60.4 on AIME 2024. TRL v1 shipped asynchronous GRPO and VESPO in April 2026.
3. **Agentic and multi-turn RLHF.** OpenRLHF 0.8 (async agent RLHF), veRL (multi-turn tool-calling), TRL (OpenEnv integration) all shipped in 2025–2026. The frontier is no longer single-turn preference pairs but whole trajectories under tool use.
4. **VLM alignment catching up to text.** OpenRLHF 0.10, TRL VLM trainer, veRL VLM RL, and LLaVA-style datasets in LLaMA-Factory all arrived in 2025–2026. Expect multimodal humanization (image captioning tone, etc.) to be a 2026 axis.
5. **Fine-grained and multi-attribute preference data.** UltraFeedback (4-axis), HelpSteer3 (5-axis + Edit), SteerLM (conditioning attributes), Safe-RLHF (helpfulness + safety). Nobody trains on single-scalar preferences anymore if they can avoid it.
6. **Label-free scaling via RLAIF.** Constitutional AI + GPT-4-judged datasets are now standard for teams without a labeling budget. AlpacaFarm formalized the simulator approach; everyone else uses ad-hoc variants. Anthropic's updated 2026 constitution now explicitly describes Claude generating its own synthetic training data from the constitution.
7. **Ray + vLLM as the RL runtime.** Three of the top five libraries (OpenRLHF, veRL, and TRL via co-located vLLM) converged here. TRL v1's asynchronous GRPO offloads rollouts to an external vLLM server, eliminating idle GPU time during training.
8. **Deprecation wave.** trlx (archived January 2024), NeMo-Aligner (superseded by NeMo RL in May 2025), DeepSpeed-Chat (stagnant since Aug 2023), OpenAssistant (project completed April 2024). The first generation of RLHF tooling is being retired.
9. **LIMA-style minimalism re-emerging.** With frontier base models now extremely capable, "small hand-curated SFT + tiny DPO" is winning mindshare again for style/tone tasks (Sky-T1 used this; WeClone too).
10. **Config-first UX is the norm.** LLaMA-Factory, Axolotl, alignment-handbook — all YAML-first. Unslop should ship a config layer rather than expose raw trainer code.
11. **Subliminal learning risk for synthetic data pipelines.** Anthropic's 2025 research found student models acquire teacher behavioral traits from model-generated training data even when the data is unrelated to those traits. This affects any RLAIF or synthetic-data preference pipeline — including Constitutional AI variants used for humanization.

---

## Open Questions / Gaps

Gaps in the open-source ecosystem that are directly relevant to a humanization product:

1. **No "humanness" alignment objective.** Every framework optimizes helpfulness, harmlessness, correctness, calibration, or reasoning. None has a named "sound-like-a-human" objective or dataset. This is genuine whitespace.
2. **No open "AI-tell" preference dataset.** Datasets like "remove the 'As an AI language model' preamble," "avoid hedging boilerplate," "vary sentence rhythm" do not exist at scale. HelpSteer3's Edit config is the closest but is general-purpose.
3. **No Constitutional-style humanness principles.** Anthropic's constitution is about ethics and safety, not style. A public "humanness constitution" (list of natural-language principles specifying what makes writing sound human) would be a novel contribution.
4. **AI-text-detection feedback loops are unexplored.** Nothing in the open ecosystem trains against a GPTZero / DetectGPT reward. This is a live question with ethical wrinkles but technically straightforward using OpenRLHF or TRL.
5. **Register / voice conditioning is ad-hoc.** SteerLM gave us conditioned attributes (verbosity, complexity), but register (casual vs. academic), voice (first-person vs. neutral), and persona are not first-class attributes in any open dataset.
6. **Multilingual humanization data is thin.** HelpSteer3 covers 12 languages; everything else skews heavily English. Localization of "natural-sounding" is an open problem.
7. **Edit-based rewards are under-used.** HelpSteer3's Edit config is rare. Most frameworks consume (chosen, rejected) pairs but do not train on the *edit trace* that would teach a rewriter model.
8. **Evaluation of humanness has no accepted benchmark.** MT-Bench, Arena Hard, AlpacaEval measure helpfulness/correctness. There is no open "human-or-AI" evaluation suite.
9. **Training-time tradeoff between accuracy and naturalness is not studied.** When you DPO toward human-sounding output, do you lose factual accuracy? Safe-RLHF's constrained-optimization framing is the closest precedent, but humanization-specific studies are missing.
10. **RLAIF for style rather than safety is rare.** Almost all Constitutional AI work targets harmlessness. A community implementation of CAI-for-style (revise this response to sound more human) would be a 100-line project and, apparently, nobody has published it.

---

## References

**Trainer libraries and frameworks:**
- huggingface/trl — https://github.com/huggingface/trl
- CarperAI/trlx — https://github.com/CarperAI/trlx
- OpenRLHF/OpenRLHF — https://github.com/OpenRLHF/OpenRLHF
- deepspeedai/DeepSpeedExamples (DeepSpeed-Chat) — https://github.com/microsoft/DeepSpeedExamples/tree/master/applications/DeepSpeed-Chat
- axolotl-ai-cloud/axolotl — https://github.com/axolotl-ai-cloud/axolotl
- hiyouga/LLaMA-Factory — https://github.com/hiyouga/LLaMA-Factory
- verl-project/verl — https://github.com/verl-project/verl
- NVIDIA/NeMo-Aligner — https://github.com/NVIDIA/NeMo-Aligner
- huggingface/alignment-handbook — https://github.com/huggingface/alignment-handbook
- eric-mitchell/direct-preference-optimization — https://github.com/eric-mitchell/direct-preference-optimization
- PKU-Alignment/safe-rlhf — https://github.com/PKU-Alignment/safe-rlhf

**Constitutional AI / RLAIF:**
- anthropics/claude-constitution — https://github.com/anthropics/claude-constitution
- Azazel5/Constitutional-AI (community RLAIF reimplementation) — https://github.com/Azazel5/Constituitional-AI
- Bai et al., "Constitutional AI: Harmlessness from AI Feedback" — https://arxiv.org/abs/2212.08073

**Preference datasets / simulators:**
- tatsu-lab/alpaca_farm — https://github.com/tatsu-lab/alpaca_farm
- OpenBMB/UltraFeedback — https://github.com/OpenBMB/UltraFeedback · https://huggingface.co/datasets/openbmb/UltraFeedback
- LAION-AI/Open-Assistant — https://github.com/LAION-AI/Open-Assistant · https://huggingface.co/datasets/OpenAssistant/oasst2
- GAIR/lima (LIMA: Less Is More for Alignment) — https://huggingface.co/datasets/GAIR/lima · https://arxiv.org/abs/2305.11206
- nvidia/HelpSteer3 — https://huggingface.co/datasets/nvidia/HelpSteer3 · https://arxiv.org/abs/2505.11475
- Anthropic/hh-rlhf (referenced throughout) — https://huggingface.co/datasets/Anthropic/hh-rlhf

**Key papers cited above:**
- Rafailov et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" — https://arxiv.org/abs/2305.18290
- Zhou et al., "LIMA: Less Is More for Alignment" — https://arxiv.org/abs/2305.11206
- Dubois et al., "AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback" — https://arxiv.org/abs/2305.14387
- Cui et al., "UltraFeedback: Boosting Language Models with Scaled AI Feedback" — https://arxiv.org/abs/2310.01377
- Dai et al., "Safe RLHF: Safe Reinforcement Learning from Human Feedback" (ICLR 2024 Spotlight) — https://arxiv.org/abs/2310.12773
- Sheng et al., "HybridFlow: A Flexible and Efficient RLHF Framework" (EuroSys 2025) — https://arxiv.org/abs/2409.19256
- Wang et al., "HelpSteer3-Preference: Open Human-Annotated Preference Data across Diverse Tasks and Languages" — https://arxiv.org/abs/2505.11475
- Zheng et al., "LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models" (ACL 2024) — https://arxiv.org/abs/2403.13372
