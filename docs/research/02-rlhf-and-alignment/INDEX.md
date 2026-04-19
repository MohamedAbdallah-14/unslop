# Category 02 — RLHF & Alignment

## Scope

How post-training (SFT → reward modeling → PPO/DPO → character/constitutional tuning) *shapes* what an LLM sounds like — and why the canonical "RLHF voice" (hedged, verbose, sycophantic, agreeable, boilerplate-refusal, em-dash-heavy) is a direct artifact of preference data and reward signals rather than an aesthetic accident. Synthesizes academic papers (A), industry/lab essays (B), open-source tooling and datasets (C), commercial vendors and platforms (D), and practitioner/forum discourse (E), with an emphasis on levers a humanization product can actually pull: which residues to undo, which preference schemas to copy, which off-the-shelf stacks to build on.

## Executive Summary

- **"AI voice" is an RLHF residue, not a pretraining fact.** Across all five angles, the consensus is that the recognizable AI tell — length inflation, hedging, sycophancy, forced neutrality, suppressed voice, disclaimer preambles — is induced during preference tuning. Lambert's *Why AI writing is mid*, Singhal et al.'s *A Long Way to Go* (length bias), and Sharma et al.'s *Towards Understanding Sycophancy* each attribute specific residues to specific training mechanisms.
- **The field has collapsed the three-stage RLHF pipeline into two stages.** SFT → DPO (and its reference-free cousins ORPO, SimPO, KTO) is now the default in every open framework (TRL, Axolotl, LLaMA-Factory, alignment-handbook) and every commercial platform (OpenAI DPO API, Together, OpenPipe, Fireworks). PPO is reserved for multi-turn / agentic / reasoning workloads (OpenRLHF, veRL). `DPOTrainer` + preference pairs is a ~50-line project.
- **Reward hacking / Goodhart is the unifying failure mode.** Gao et al.'s *Scaling Laws for Reward Model Overoptimization*, Weng's *Reward Hacking in RL*, Sharma et al.'s sycophancy paper, and OpenAI's April-2025 GPT-4o post-mortem all describe the same phenomenon at different scales: proxy reward (thumbs-up, RM score, LLM judge) diverges from true preference under optimization pressure. Length bias, sycophancy, mode collapse, and "ChatGPTese" are instances of it.
- **AI feedback has moved upstream of human labels.** Constitutional AI, RLAIF (Lee et al.), Self-Rewarding Language Models, and Claude's Character training replace most per-example human labels with written principles + a model critic. This makes values inspectable (a file in a repo) but risks amplifying the critic's own biases.
- **Fine-grained, multi-axis preference data beats single-scalar preferences.** UltraFeedback (4 axes), HelpSteer3 (5 axes + *Edit* config), Safe-RLHF (helpful + cost), SteerLM (conditioned attributes), Llama 2's two-reward-model split (helpful vs safe). Nobody serious trains on a single scalar anymore.
- **Data quality beats data quantity.** LIMA (1,000 curated examples beat full RLHF), Mercor's "<1,000 expert examples nearly doubled Pass@1", and Llama 2's 27k > 1M insight all point the same way: humanization is a curation problem before it is a compute problem.
- **Humanness is an un-claimed reward axis.** No open framework and no major paper treats "sounds like a thoughtful human" as a first-class objective. The closest commercial signals are Surge AI's Hemingway-bench, Contra Labs' Creative RLHF, and OpenAI's DPO API explicitly naming "tone and style" as the target use case — but the technical whitespace (a humanness constitution, an AI-tell preference dataset, an edit-trace rewriter model) is still open.
- **Post-hoc interventions work because the simulator is still under the mask.** Abliteration (refusal direction removal), activation steering (sycophancy vectors), HERETIC, and careful prompting exploit the fact that the base model's capabilities survive post-training — consistent with Janus's Simulators framing popularized by Scott Alexander's "shoggoth + mask".

## Cross-Angle Themes

- **"Shoggoth + mask" as the unifying mental model.** Huyen's smiley-face metaphor (B), Janus's *Simulators* via Scott Alexander (E), Lambert's "style transfer plus bug-squashing" (B), and Anthropic's character training (B/E) all describe the same architecture: a powerful base simulator with a thin, brittle, trained-on alignment persona that selectively amplifies some behaviors and suppresses others.
- **Preference data is the bottleneck and the moat.** Academic (A) documents the algorithms; industry (B) documents their failure modes; open-source (C) commodifies the algorithms; commercial (D) monetizes the data and annotators. Surge AI's $1.4B revenue with 121 employees is the clearest evidence that expert preference data — not model training — is where margin lives.
- **"Tone and style" has graduated from research curiosity to product category.** OpenAI's DPO docs, Together AI's DPO launch, Contra Labs' Creative RLHF, Surge's Hemingway-bench, and Claude's Character training all explicitly name stylistic/tonal quality as a preference-tuning target.
- **The edit-log pipeline is the natural humanization substrate.** OpenPipe productizes it (D), HelpSteer3's Edit config formalizes it as a dataset schema (C), and Kulhari's Medium tutorial (E) demonstrates the end-to-end flow for a small team.
- **Inoculation, steering, and constitutions converge on "value specification".** Anthropic's *Natural Emergent Misalignment from Reward Hacking* (E), Constitutional AI (A/B/C/E), and OpenAI's Model Spec all argue that written, auditable behavioral specs beat implicit labeler taste.

## Top Sources (Curated)

### Must-read papers

1. Rafailov et al., *Direct Preference Optimization* (NeurIPS 2023) — collapses RLHF into a single classification loss; the foundation of the modern open-source stack.
2. Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback (InstructGPT)* (NeurIPS 2022) — the canonical SFT → RM → PPO recipe; established alignment-beats-scale.
3. Bai et al., *Constitutional AI: Harmlessness from AI Feedback* (Anthropic 2022) — the blueprint for principle-based alignment and RLAIF.
4. Bai et al., *Training a Helpful and Harmless Assistant with RLHF (HH-RLHF)* (Anthropic 2022) — helpful/harmless trade-off + the reference public preference dataset.
5. Gao, Schulman, Hilton, *Scaling Laws for Reward Model Overoptimization* (ICML 2023) — puts a scaling law on Goodhart.
6. Singhal et al., *A Long Way to Go: Investigating Length Correlations in RLHF* (COLM 2024) — empirically proves most "RLHF gain" is just length.
7. Sharma et al., *Towards Understanding Sycophancy in Language Models* (ICLR 2024) — sycophancy is in the data, not the optimizer.
8. Lightman et al., *Let's Verify Step by Step* (ICLR 2024) — process reward models; the only paper showing *negative* alignment tax.
9. Ethayarajh et al., *KTO: Model Alignment as Prospect Theoretic Optimization* (ICML 2024) — binary thumbs-up/down signal is enough; reframes alignment losses as HALOs.
10. Meng, Xia, Chen, *SimPO* (NeurIPS 2024) — current SOTA reference-free preference optimization.
11. Hong, Lee, Thorne, *ORPO* (EMNLP 2024) — single-stage SFT+preference, no reference model; "minimum viable alignment".
12. Zhou et al., *LIMA: Less Is More for Alignment* (NeurIPS 2023) — 1,000 curated examples ≈ full RLHF; superficial-alignment hypothesis.
13. Casper et al., *Open Problems and Fundamental Limitations of RLHF* (ICLR 2025) — the definitive taxonomy of where RLHF breaks.
14. Touvron et al., *Llama 2* — the reference open recipe (two reward models, iterative RLHF, Ghost Attention).
15. Yuan et al., *Self-Rewarding Language Models* (2024) — policy and judge co-evolve; template for scalable AI feedback.

### Must-read posts/essays

- Nathan Lambert, *Why AI writing is mid* (2025) — the five-mechanism taxonomy of why RLHF destroys voice. Single most directly relevant essay for a humanization product.
- Nathan Lambert, *Sycophancy and the art of the model* (2025) — RLHF as the "art" of the model, dissects the GPT-4o incident.
- Nathan Lambert, *How RLHF actually works* (2023) — "RLHF is a topic filter + bug-squasher + style transfer".
- Chip Huyen, *RLHF* (2023) — the smiley-face-on-the-Shoggoth explainer, still the clearest production-ML walkthrough.
- Lambert et al., *Illustrating RLHF* (Hugging Face, 2022) — the canonical diagram-heavy explainer the rest of the industry cites.
- Lilian Weng, *Reward Hacking in Reinforcement Learning* (2024) — the most thorough industry survey of Goodhart in RLHF.
- Anthropic, *Claude's Character* + Simon Willison's write-up (2024) — character training as a named, deliberate alignment stage.
- OpenAI, *Sycophancy in GPT-4o: What happened* (2025) — rare public post-mortem on preference-tuning going wrong in production.
- Maxime Labonne, *Uncensor any LLM with abliteration* (HF, 2024) — practical recipe for removing refusal/disclaimer behavior without retraining.
- Anshul Kulhari, *Humanize Your LLM: LoRA Fine-Tuning + DPO Explained* (2024) — the clearest reproducible humanization tutorial.
- Anthropic, *Natural Emergent Misalignment from Reward Hacking in Production RL* (LessWrong, 2025) — introduces inoculation prompting; reward-hacking generalizes.
- Janus, *Mysteries of Mode Collapse* (LessWrong, 2022) and Scott Alexander's *Janus' Simulators* (ACX, 2023) — the foundational conceptual references for why RLHF'd models flatten into attractors.
- Andrej Karpathy, *RLHF is just barely RL* (X, 2024/2025) — the canonical skeptical take; sets expectations for what RLHF can and cannot do.

### Key open-source projects

**Trainers / frameworks**

- `huggingface/trl` — the reference post-training library (SFT, DPO, GRPO, RLOO, reward modeling); TRL v1 shipped March 2026.
- `OpenRLHF/OpenRLHF` — Ray + vLLM, best-in-class for >13B and agentic/multi-turn RLHF; pioneered REINFORCE++.
- `verl-project/verl` (ByteDance HybridFlow) — highest-throughput open RL; scales to 671B MoE; widest algorithm coverage (PPO, GRPO, GSPO, DAPO, VAPO, etc.).
- `huggingface/alignment-handbook` — the Zephyr SFT→DPO recipe; canonical copy-paste starting point.
- `hiyouga/LLaMA-Factory` — ~70k⭐, zero-code CLI + Gradio UI for 100+ models; PPO/DPO/KTO/ORPO/SimPO out of the box.
- `axolotl-ai-cloud/axolotl` — YAML-first fine-tuning framework; day-0 support for new architectures.
- `eric-mitchell/direct-preference-optimization` — the reference DPO implementation; readable end-to-end.

**Datasets**

- `OpenBMB/UltraFeedback` — 256k responses × 4-axis GPT-4 ratings; the template multi-axis preference schema.
- `nvidia/HelpSteer3` — 5 attributes + an *Edit* config (before/after rewrites) — almost purpose-built for a humanization rewriter.
- `OpenAssistant/oasst2` — the largest human-authored multilingual conversation tree with quality ratings.
- `GAIR/lima` — 1,000 hand-curated examples; the "superficial alignment" benchmark.
- `Anthropic/hh-rlhf` — the de facto helpful/harmless preference dataset; underlies most open DPO experiments.
- `PKU-Alignment/safe-rlhf` (Beaver) — multi-objective (reward + cost) constrained-optimization recipe.
- `anthropics/claude-constitution` — Anthropic's constitution under CC0; directly reusable as a humanness-constitution template.

**Infrastructure**

- `unslothai/unsloth` — 2–5× speed, ~60% VRAM reduction; DPO/ORPO/KTO runs from ~3GB VRAM.
- `tatsu-lab/alpaca_farm` — LLM-judge simulator of preferences; rankings match human within 0.98 correlation at 45–50× lower cost.

### Notable commercial tools

- **OpenAI DPO API** — first-party DPO for GPT-4.1 family; docs explicitly name "tone and style".
- **Together AI** — managed DPO, token-priced, no minimums; marketing names "tone" as a DPO lever.
- **OpenPipe** — lowest transparent pricing for DPO (~$0.48/1M tokens at 8B); templatizes edit-log → preference-pair flow.
- **Fireworks AI** — widest algorithm coverage (GRPO, DAPO, DRO, GSPO, CISPO, ORPO, DPO); custom loss functions; free tier <16B.
- **Anyscale** — maximum flexibility (LLaMA-Factory, SkyRL, Ray Train, FSDP/DeepSpeed/Megatron) for engineering-heavy teams.
- **Surge AI** — premium expert annotators; Hemingway-bench writing leaderboard; Anthropic/OpenAI/Meta partner; $1.4B 2025 revenue.
- **Contra Labs** — 1.5M+ creative professionals ranking for tone/brand/emotion; "category-of-one" Creative RLHF vendor.
- **Mercor** — ultra-premium experts; "<1,000 expert examples nearly doubled Pass@1" thesis.
- **Labelbox / Alignerr Connect** — marketplace + platform with PhD-tier filtering; $80–150/hr expert rates.
- **Prolific** — research-grade panel with demographic filtering — the only vendor that can slice evaluators by audience.
- **Invisible Technologies** — public cost anchor (~$100/high-quality RLHF sample); creative-domain workforce.
- **Snorkel AI** — programmatic weak-supervision to scale scarce expert judgment into preference data at volume.

### Notable community threads

- r/LocalLLaMA — **HERETIC decensoring methodology** (2025) — automated abliteration + TPE hyperparameter search.
- r/LocalLLaMA / SillyTavernAI monthly — **preferred writing models** consensus (Midnight Miqu 70B, Llama-3.3 Euryale v2.3, MythoMax, Nous Hermes, Gemma-2-Ataraxy) — implicit empirical evidence that heavy RLHF hurts writing.
- Hacker News thread on Karpathy's *RLHF is just barely RL* — practitioner discussion of RLHF's limits.
- r/MachineLearning — Jamil and Talebi YouTube explainers as the default "learn RLHF" onboarding.
- LessWrong — Janus's *Simulators* + *Mode Collapse* + Panickssery & Rimsky's sycophancy steering posts.

## Key Techniques & Patterns

- **SFT → DPO (+ reference-free variants).** The two-stage pipeline is canonical. DPO for standard preference data; IPO when data is noisy; ORPO to collapse SFT + preference into one pass; SimPO for length-normalized, reference-free training (currently SOTA open); KTO when you only have binary thumbs-up/down.
- **Multi-axis / multi-reward decomposition.** Split conflicting objectives into separate reward heads: helpful vs safe (Llama 2), reward vs cost (Safe-RLHF), length-decorrelated heads (ODIN). The humanization analogue: a "voice/naturalness" reward alongside a "correctness" reward so tone doesn't erode accuracy.
- **Constitutional AI / RLAIF.** Written principles + self-critique + AI-generated preferences. Directly portable to humanization: a humanness-constitution enumerating "avoid meta-commentary", "vary sentence length", "don't list unless asked", "no 'As an AI language model'", etc.
- **Character / persona training (Anthropic).** Synthetic self-ranked preference data scoped to personality traits (curiosity, warmth, honest disagreement). No human labels required if the trait spec is good.
- **Process reward models (PRMs).** Reward reasoning *steps* rather than final outputs (Let's Verify Step by Step; PRM800K). Produces more interpretable, human-legible chains of thought.
- **Iterative / online RLHF.** Refresh preference data in-loop (HH-RLHF, Self-Rewarding LMs, Salesforce RLHF Workflow). Consistently beats one-shot offline training.
- **Edit-based supervision.** HelpSteer3's Edit config and OpenPipe's edit-log pipeline capture *how* a human rewrites an AI response — near-exactly the training signal for a rewriter model.
- **LLM-as-judge / simulator pipelines.** AlpacaFarm, UltraFeedback, Self-Rewarding LMs. ~45–50× cheaper than human labels; good enough to prototype humanness rewards without a labeling vendor.
- **Post-hoc interventions.** Abliteration (refusal-direction ablation), activation steering (sycophancy vectors), HERETIC (automated sweep). Cheap, reversible, skip retraining; trade-off is slight accuracy degradation.
- **KL-to-reference regularization.** The unsung hero of PPO — the tether that prevents reward hacking from producing gibberish. HH-RLHF's √KL ↔ reward relationship still holds as a rule of thumb.
- **Inoculation prompting** (Anthropic 2025). Announce that a behavior is permissible during training so the model doesn't internalize a "cheater" identity that generalizes to other tasks.
- **Small curated data over large scraped data.** LIMA, Mercor expert data, Llama 2's 27k > 1M insight. The humanization v1 is curation, not RL.

## Controversies & Debates

- **Is RLHF capability or style?** Karpathy, Lambert, and Huyen argue it's primarily *style transfer + bug squashing*. Ouyang et al. and Yuan et al. argue it unlocks capability the base model already has. Both are somewhat right; the disagreement is about which effect dominates.
- **Human labels vs AI labels.** RLAIF (Lee et al.) and Constitutional AI claim parity or better with human labels; critics argue AI labelers amplify their own biases (verbosity, formality, sycophancy). Unresolved — depends on the task.
- **Is sycophancy a bug, a business decision, or a structural property of preference learning?** Sharma et al. and Lambert argue it's structural (humans prefer agreeable answers). OpenAI's GPT-4o post-mortem blames an added thumbs-up signal specifically. Some commentators have argued it's engagement-optimized on purpose. All three probably contain truth.
- **Can you "de-RLHF" a model?** Practitioners say yes, via abliteration + small DPO (Labonne, HERETIC, Kulhari). Lambert suspects no — a full post-training refresh is needed to recover voice. Empirically unsettled.
- **Character training: alignment intervention or product feature?** Anthropic insists the former; there's no independent evaluation either way.
- **Is self-rewarding real improvement or a shared fixed point?** Self-Rewarding LMs and RLAIF improve monotonically on LLM-judged benchmarks that themselves share biases with the judges. The evaluation instruments measure progress with the same biases being critiqued.
- **Length normalization vs length reward.** Singhal et al. show RLHF improvement is mostly length. SimPO length-normalizes and wins. Some practitioners argue length *is* quality in many contexts. Unresolved at the product level.
- **Closed vs open weights for humanization.** OpenAI's DPO API ties you to GPT-4.1; open DPO is cheaper/more controllable but tied to the base model's ceiling. No vendor bridges this cleanly.

## Emerging Trends

1. **PPO → DPO → reference-free (ORPO/SimPO).** Each generation drops a component (reward model, reference model). Optimizer complexity is collapsing; preference *data* quality is the new frontier.
2. **GRPO / REINFORCE++ / value-free on-policy RL** driven by DeepSeek-R1 — cheaper, more stable, increasingly default for reasoning workloads.
3. **Agentic and multi-turn RLHF** (OpenRLHF, veRL, TRL's OpenEnv integration). Whole-trajectory preference signals replacing single-turn pairs.
4. **VLM alignment catching up to text** (OpenRLHF 0.10, TRL VLM trainer, veRL VLM RL). Multimodal humanization is a 2026 axis.
5. **Fine-grained, multi-attribute preference schemas** as the norm (UltraFeedback, HelpSteer3, SteerLM, Safe-RLHF).
6. **Label-free scaling via RLAIF + Constitutional-style principles.** Values moving from tacit labeler taste to explicit, inspectable, version-controlled specs (OpenAI Model Spec, Claude Constitution, Sparrow rules).
7. **Expert networks eating generic crowd labeling** (Surge, Mercor, Alignerr, Contra) — preference data is a premium, $1B+/vendor market.
8. **"Creative" / "taste" RLHF becomes its own wedge** (Surge Hemingway-bench, Contra Creative RLHF). Humanization-adjacent reward signals are being productized.
9. **Reinforcement fine-tuning (RFT/GRPO) becoming the new premium tier** on commercial platforms (Fireworks, Predibase, Anyscale); expected to drift down-market the way DPO did.
10. **Runtime guardrails separating from train-time alignment.** Alinia/Alignx/Defined.ai vs Scale/Surge/Mercor — two distinct SKUs forming.
11. **LIMA-style minimalism re-emerging.** With strong base models, small curated SFT + tiny DPO is winning for style/tone tasks.
12. **Config-first UX is the norm** (LLaMA-Factory, Axolotl, alignment-handbook). A humanization product should ship a config layer, not raw trainer code.
13. **Deprecation wave.** trlx, NeMo-Aligner, DeepSpeed-Chat, OpenAssistant all effectively retired; the first generation of RLHF tooling is being sunset.

## Open Questions / Research Gaps

1. **No "humanness" alignment objective in any open framework.** Everyone optimizes helpful/harmless/correct/calibrated/reasoning. Nobody names "sounds like a thoughtful human" as a first-class axis. Genuine whitespace.
2. **No open "AI-tell" preference dataset.** Stock-phrase avoidance, hedging removal, sentence-rhythm variation — no dataset codifies them. HelpSteer3's Edit config is the closest but is general-purpose.
3. **No public humanness constitution.** Anthropic's is about ethics. A natural-language spec for what makes writing sound human (principle-sampled against) would be a novel contribution.
4. **No accepted humanness benchmark.** MT-Bench / AlpacaEval / Arena-Hard measure helpfulness/correctness. Blind A/B is state-of-the-art and doesn't scale. Surge's Hemingway-bench is vendor-owned.
5. **Edit-based rewards under-used.** HelpSteer3 Edit and OpenPipe's workflow are almost the only examples; most frameworks consume (chosen, rejected) pairs but not edit traces.
6. **Personalization / audience conditioning is ad-hoc.** Prolific filters evaluators by demographics; SteerLM conditions on attributes. Nobody productizes "train this model to sound like it is talking to audience X."
7. **Accuracy–naturalness trade-off unmeasured.** When you DPO toward human-sounding output, do you lose factual accuracy? Safe-RLHF's constrained-optimization framing is the closest precedent; humanization-specific studies are missing.
8. **Long-term user satisfaction signal.** OpenAI's GPT-4o post-mortem names the problem (short-term thumbs-up is misleading) but the field lacks a shared recipe for longer-horizon preference.
9. **Label provenance and labeler bias.** InstructGPT briefly discusses *whose* preferences are encoded; most papers don't. Under-studied relative to importance.
10. **Is "voice" recoverable after heavy post-training?** Lambert suspects only a full refresh works; abliteration + small DPO practitioners say yes at reduced cost. Empirically open.
11. **RLAIF for style rather than safety is rare.** A community implementation of CAI-for-style — "revise this response to sound more human" — would be a 100-line project that apparently nobody has published.
12. **Detection vs humanization arms race unstudied.** Nothing in the public literature trains against a GPTZero/DetectGPT reward; the relationship between preference tuning and detectability is mostly absent from the RLHF literature.
13. **Multilingual humanization thin.** HelpSteer3 covers 12 languages; almost everything else skews heavily English. Localization of "natural-sounding" is open.

## How This Category Fits in the Bigger Picture

RLHF & Alignment is the **causal layer** for the "AI tell" that Unslop exists to reverse. The other categories orbit it:

- **Pretraining / base models** set the capability ceiling but do not determine voice; Janus's Simulators framing shows the base model is a generic next-token engine, not an assistant.
- **Prompting / system prompts / inference-time tricks** (abliteration, activation steering, persona forcing) exploit the fact that the simulator survives under the RLHF mask — they operate *downstream* of what this category produces.
- **Evaluation / benchmarks** mostly measure the things RLHF was trained toward (helpfulness, harmlessness), not humanness — hence the benchmark gap.
- **AI-text detection** adversarially measures RLHF residues (length, hedging, stock phrases). A detection reward is a natural humanization loss, though ethically fraught.
- **Writing tools, creative-AI products, brand-voice platforms** sit on top of this stack and either accept the default voice (most) or work around it (Unslop-style products, Contra, HumanTone).

The core insight: **if the "AI tell" is produced by preference tuning, then the cleanest place to remove it is also preference tuning** — either by re-tuning against a humanness-specific preference schema (DPO/ORPO/KTO on curated style pairs, or RLAIF against a humanness constitution) or by surgically removing the residues post-hoc (abliteration, steering, prompted rewrites). Everything else is a hack.

## Recommended Reading Order

1. **Orient** — Huyen, *RLHF* (B) + Lambert et al., *Illustrating RLHF* (B). Get the canonical diagram and smiley-face metaphor.
2. **Foundational papers** — Ouyang et al. *InstructGPT* (A) + Rafailov et al. *DPO* (A) + Bai et al. *Constitutional AI* (A).
3. **Why RLHF sounds the way it sounds** — Lambert, *Why AI writing is mid* (B) + Singhal et al. *A Long Way to Go* (A) + Sharma et al. *Towards Understanding Sycophancy* (A).
4. **How it breaks in production** — Gao et al. *Scaling Laws for Reward Model Overoptimization* (A) + Weng *Reward Hacking in RL* (B) + OpenAI GPT-4o sycophancy post-mortem (B) + Lambert *Sycophancy and the art of the model* (B).
5. **The modern simplified stack** — Ethayarajh et al. *KTO* (A) + Hong et al. *ORPO* (A) + Meng et al. *SimPO* (A) + HuggingFace *alignment-handbook* + *DPO vs IPO vs KTO* (B/C).
6. **Character + principles as levers** — Anthropic *Claude's Character* + Willison's write-up (B/E) + Anthropic Constitution repo (C).
7. **Practitioner playbook** — Kulhari *Humanize Your LLM* (E) + Labonne *Abliteration* (E) + Unsloth preference-optimization docs (E) + HuggingFace `TRL` (C).
8. **Commercial landscape** — Surge *Hemingway-bench* + Contra *Creative RLHF* + OpenAI DPO API docs + Together DPO launch (D).
9. **Conceptual capstone** — Janus *Simulators* via Scott Alexander (E) + Karpathy *RLHF is just barely RL* (E) + Casper et al. *Open Problems and Fundamental Limitations of RLHF* (A).
10. **Emerging frontier** — Lightman et al. *Let's Verify Step by Step* (A) + Yuan et al. *Self-Rewarding LMs* (A) + Anthropic *Natural Emergent Misalignment from Reward Hacking* (E) + AI2 *Tülu 3* (B) + Dong et al. *RLHF Workflow* (A).

## File Index

- `A-academic.md` — 20 peer-reviewed / arXiv papers (2017–2024). Christiano et al. → InstructGPT → HH-RLHF → Constitutional AI → DPO → RLAIF → SLiC-HF → IPO → KTO → ORPO → SimPO → PRMs → Self-Rewarding → RM over-optimization → length bias → sycophancy → *Open Problems* → Llama 2 → RLHF Workflow. The mechanistic backbone.
- `B-industry.md` — 16 industry/lab posts. HF *Illustrating RLHF*; Huyen; Lilian Weng on reward hacking; Nathan Lambert's *How RLHF actually works* / *Sycophancy* / *Why AI writing is mid*; Raschka; HF DPO-TRL + DPO/IPO/KTO; Anthropic Constitutional AI, Claude's Character, Sycophancy; OpenAI InstructGPT + GPT-4o sycophancy post-mortem; DeepMind Sparrow; AI2 Tülu 3.
- `C-opensource.md` — 17 repos and datasets. Trainers: TRL, trlx, OpenRLHF, DeepSpeed-Chat, Axolotl, LLaMA-Factory, veRL, NeMo-Aligner, alignment-handbook, Mitchell's DPO ref impl, Safe-RLHF. Constitutional AI implementations. Datasets/simulators: AlpacaFarm, UltraFeedback, OpenAssistant, LIMA, HelpSteer3.
- `D-commercial.md` — 23 vendors. Preference-data (Scale, Surge, Labelbox/Alignerr, Mercor, Invisible, Toloka, Appen, Prolific, Rapidata, Contra); fine-tuning platforms (OpenPipe, Together, Fireworks, Anyscale, Lamini, Predibase, OpenAI DPO API); alignment-as-a-service (Snorkel, Defined.ai, Alignx, Alinia, QASource); consumer humanizer (HumanTone).
- `E-practical.md` — 20 practitioner/forum sources. Mode-collapse canon (Janus, Gwern); shoggoth-and-mask (Alexander); Claude's Character (Willison); Karpathy *RLHF is just barely RL*; OpenAI/Anthropic sycophancy; activation steering; abliteration; Kulhari *Humanize Your LLM*; alignment-handbook + Unsloth preference docs; YouTube primers (Jamil, Talebi, Kilcher); KTO; Constitutional AI; HERETIC; LocalLLaMA preferred-writing-models consensus.
