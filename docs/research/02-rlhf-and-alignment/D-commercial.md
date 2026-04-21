# RLHF & Alignment — Commercial

> Research category: **RLHF & Alignment**
> Angle: **D — Commercial Products & Services**
> Project context: **Humanizing AI output and thinking**
> Compiled: April 2026

## Executive Summary

The commercial RLHF/alignment stack has bifurcated into two main layers plus an emerging third:

1. **Preference data vendors** — a small set of frontier-focused firms (Scale AI, Surge AI, Labelbox/Alignerr, Mercor, Invisible Technologies) now compete to supply the top ~12 AI labs with "domain expert" preference data. Surge AI reportedly overtook Scale on revenue in 2024 (~$1.2B vs ~$870M) while still bootstrapped, signaling that the RLHF data market is a very large, margin-rich business.
2. **Fine-tuning platforms that expose DPO/RLHF** — Together AI, OpenPipe, Fireworks, Anyscale, Lamini, Predibase, plus first-party offerings from OpenAI (DPO API). These turn preference data into aligned model weights without owning the humans.
3. **Alignment-as-a-service** — A newer, thinner layer (Alignx, Alinia, Defined.ai, Snorkel AI, QASource, Contra Labs) that bundles evaluation, guardrails, RLHF/DPO, and policy-tuning into managed offerings for enterprises that do not want to run their own pipeline.

For the "humanizing AI output" project the most directly relevant commercial signal is: (a) **Contra Labs** and **Surge's Hemingway-bench** are explicitly targeting "creative taste," "brand fit," and nuanced writing quality as RLHF reward signals, not just helpfulness/harmlessness; (b) consumer-grade "humanizer" products (e.g., HumanTone) exist but are thin wrappers, while the deep leverage is in preference-tuned models trained on expert writer rankings.

**Research value: high** — dense commercial landscape with named players, public pricing, and clear technique adoption patterns directly applicable to a humanization product.

---

## Sources

### Preference data / labeling vendors

#### 1. Scale AI — GenAI Platform / RLHF
- **URL:** https://scale.ai/ · https://scale.ai/comparison
- **Vendor:** Scale AI (CEO: Jason Droege as of June 2025; founder Alexandr Wang joined Meta as Chief AI Officer)
- **Pricing tier:** Enterprise ~$93K/yr typical, up to $400K+; self-serve Data Engine pay-as-you-go with 1,000 free labeling units
- **Year:** Founded 2016; GenAI Platform / RLHF offering matured 2022–2025
- **Core feature:** End-to-end RLHF data, SFT data, red teaming, evaluation; tightly integrated with enterprise sales motion and frontier labs. Meta acquired a 49% non-voting stake in June 2025 for ~$14.3B (valuing Scale at ~$29B).
- **Claims / techniques:** "Quality RLHF data for natural language generation and large language models"; hybrid expert + crowd model; reward signal generation. SEAL (Safety, Evaluation, and Alignment Lab) frameworks now provide Meta with privileged access.
- **2-3 sentence summary:** The Scale AI / Meta deal (June 2025) was the largest transaction in the RLHF data market to date but triggered immediate customer defection: Google, OpenAI, and xAI severed ties rather than share proprietary training data with a Meta-affiliated vendor. Founder Alexandr Wang stepped down as CEO to become Meta's Chief AI Officer. Scale maintains nominal independence but Meta has priority scheduling access to its workforce.
- **Takeaways:** The Meta deal is a structural market event: Scale is now effectively unavailable to Meta's main competitors, creating a vacuum that Surge AI and Mercor are positioned to fill. Any RLHF data procurement decision in 2025–2026 must account for this conflict-of-interest risk.

#### 2. Surge AI — RLHF platform + domain experts
- **URL:** https://www.surgehq.ai/
- **Vendor:** Surge AI (Edwin Chen)
- **Pricing tier:** Enterprise only, no public rates; contractor annotators paid ~$0.30–$0.40/working minute (premium vs. crowdsourcing)
- **Year:** Founded 2020; platform scaled 2022–2026
- **Core feature:** ~50,000 vetted domain-expert "Surgers"; proprietary quality-control tech; Hemingway-bench (writing), AdvancedIF (instruction following), EnterpriseBench (agentic)
- **Claims / techniques:** "Rich human feedback"; red teaming; human-crafted reward rubrics yielding "13% gain" on instruction-following via Meta Superintelligence Labs partnership
- **2-3 sentence summary:** Surge AI grew from $1.2B (2024 revenue) to seeking a $1B capital raise at a $15–25B valuation in July 2025 — its first external financing after bootstrapping to this scale. The Scale AI / Meta deal sent major customers to Surge as the now-unaffiliated alternative; Google, OpenAI, and xAI are cited as newly uncontested Surge opportunities. Hemingway-bench (writing quality), AdvancedIF (instruction following) remain the most relevant benchmarks for humanization alignment.
- **Takeaways:** Post Scale/Meta deal, Surge is the leading unaffiliated frontier-lab RLHF vendor. The $15–25B valuation range in mid-2025 reflects the market's pricing of expert preference data as a strategic asset, not a commodity.

#### 3. Labelbox — Alignerr Connect / Expert Network
- **URL:** https://labelbox.com/ · https://labelbox.com/services/alignerr-connect/ · https://www.alignerr.com/
- **Vendor:** Labelbox
- **Pricing tier:** Platform subscription + expert hourly rates; experts earn $80–$150/hr
- **Year:** Labelbox founded 2018; Alignerr network scaled 2024–2025
- **Core feature:** "Data factory" platform combined with 1.5M+ vetted knowledge workers, 50K+ PhDs, 200+ domains, 40+ countries; "top 3% acceptance rate" via Zara AI interviewer
- **Claims / techniques:** Partners with "80%+ of leading US AI labs"; reward signals, rubric-based scoring for coding/science/finance/long-horizon tasks
- **2-3 sentence summary:** Labelbox pivoted from a general annotation platform to a frontier AI data factory, with Alignerr as the expert network brand. Their pitch is that filtered PhD-tier talent + platform tooling beats generic crowd labor for modern RLHF. Public hourly rates ($80–150/hr) give one of the few public floors for expert RLHF labor cost.
- **Takeaways:** Cleanest example of "marketplace + platform" RLHF economics; useful if humanization work needs domain-expert writers.

#### 4. Mercor — Expert data for frontier labs
- **URL:** https://www.mercor.com/ · https://mercor.com/research/
- **Vendor:** Mercor
- **Pricing tier:** Enterprise only; expert contractor pay varies
- **Year:** Founded 2022; scaled with frontier labs 2024–2026
- **Core feature:** Deep subject-matter experts (Nobel, Emmy, Rhodes, FAANG, IMO medalists); APEX benchmarks for productivity; RLHF environment design
- **Claims / techniques:** "Fewer than 1,000 expert-labeled data points nearly doubled Pass@1" in partnership with Applied Compute; reasoning, long-horizon planning, tool use, safe behavior
- **2-3 sentence summary:** Mercor represents the "ultra-premium expert" segment — a small set of very high-tier annotators producing small-volume, high-leverage data rather than millions of cheap comparisons. Reports "top 5 AI labs and 6 of the Magnificent Seven" as customers. Their thesis — that hundreds of expert examples beat tens of thousands of generic ones — is particularly relevant for nuanced preferences like writing style.
- **Takeaways:** Strong fit for expert-writer-driven humanization data; signals the "small data, high expertise" trend.

#### 5. Invisible Technologies — AI data trainers
- **URL:** https://www.invisible.co/ · https://invisibletech.ai/
- **Vendor:** Invisible Technologies
- **Pricing tier:** Enterprise engagements; internal estimates of ~$60K per 600 high-quality RLHF annotations (~$100/sample)
- **Year:** Founded 2015; AI-training pivot 2022+
- **Core feature:** Trainer workforce that ranks multiple AI-generated responses and provides chain-of-thought justifications, not binary labels; specialized in legal, medical, creative
- **Claims / techniques:** Known OpenAI partner for ChatGPT/InstructGPT-era RLHF; "chain-of-thought rationales" behind preferences
- **2-3 sentence summary:** Invisible has been one of the less-publicized but central suppliers of RLHF data to OpenAI, with a workforce model that emphasizes expertise and written reasoning for each ranking. Their published cost structure ($0.50–$5 per RLHF sample, with full-quality at ~$100) is one of the few public anchors on what human preference data actually costs. Their creative-domain expertise is directly relevant to writing-style alignment.
- **Takeaways:** Public cost anchor + creative domain workforce make it a likely benchmark partner for a humanization pipeline.

#### 6. Toloka AI — Platform + tiered expert network
- **URL:** https://toloka.ai/
- **Vendor:** Toloka AI (originally Yandex, now independent)
- **Pricing tier:** Tiered by expertise (Domain Experts / AI Tutors / General Annotators); "no minimums, no long-term contracts"
- **Year:** Founded 2014 (as Yandex Toloka); re-launched independent platform 2022+
- **Core feature:** RLHF & preference data, instruction tuning, side-by-side evaluation, synthetic data validation; AI-assisted project setup auto-configures QA
- **Claims / techniques:** 90+ domain specializations; "AI Tutors" trained specifically on RLHF guidelines
- **2-3 sentence summary:** Toloka is positioning between traditional crowd labeling (its origin) and premium expert networks, with the explicit "AI Tutor" tier for RLHF workflows. Tiered pricing lets teams buy only the expertise level each step needs. Strong European footprint and GDPR posture make it a fit for brand-safe humanization pipelines.
- **Takeaways:** Most flexible price/quality curve of the major vendors.

#### 7. Appen — Legacy data + RLHF services
- **URL:** https://www.appen.com/
- **Vendor:** Appen (ASX-listed)
- **Pricing tier:** Enterprise; no public rates
- **Year:** Founded 1996; LLM/RLHF pivot 2022+
- **Core feature:** Global crowd workforce + managed services; added generative AI, RLHF, and model evaluation offerings
- **Claims / techniques:** Full-stack annotation + RLHF + red teaming; multilingual at scale
- **2-3 sentence summary:** Appen is the legacy giant now repositioning around generative AI, competing on scale and language breadth rather than expert depth. Financial performance has been weaker than Surge/Scale, reflecting the shift from classic labeling to expert RLHF. Still relevant for broad multilingual evaluation and lower-tier preference data.
- **Takeaways:** Default for multilingual scale but not the leader on quality-first RLHF.

#### 8. Prolific — Research-grade participants for AI alignment
- **URL:** https://www.prolific.com/ · https://www.prolific.com/alignment
- **Vendor:** Prolific
- **Pricing tier:** Pay-as-you-go platform; no monthly fees; managed services tier with custom pricing
- **Year:** Founded 2014; AI alignment product launched 2023–2024
- **Core feature:** 200,000+ verified participants across 38+ countries with 300+ prescreening attributes; API + AI Task Builder
- **Claims / techniques:** Preference pairs, reward model data, SFT demos, instruction-following evals; research-grade QA; "preference data within hours"
- **2-3 sentence summary:** Prolific is the academic-research panel repositioned as an alignment data source, with the strongest ability to slice evaluator populations by demographics, language, and cultural background. That demographic filtering is the distinctive feature — important for humanization where target audience voice matters. Pay-as-you-go removes procurement friction.
- **Takeaways:** Best fit when the humanization target is a specific audience segment; weakest for deep domain expertise.

#### 9. Rapidata — High-throughput preference collection
- **URL:** https://rapidata.ai/
- **Vendor:** Rapidata
- **Pricing tier:** API usage pricing (per-annotation)
- **Year:** Founded ~2023
- **Core feature:** Pairwise preference collection at very high volume via mobile/web micro-tasks; Python API
- **Claims / techniques:** Collected 1.5M+ annotations from 150K+ humans for T2I RLHF; "over 2 million preference responses in just days"; rich feedback (Likert, heatmaps, word-level misalignment)
- **2-3 sentence summary:** Rapidata is the speed/scale play — a Mechanical-Turk-alternative tuned specifically for pairwise preference data used in RLHF/DPO. Strongest for broad-population preference signals (text-to-image was their beachhead) rather than deep expertise. The speed claim (millions in days) is meaningful for iteration loops.
- **Takeaways:** Useful for humanization A/B preference collection at volume.

#### 10. Contra Labs — Creative RLHF
- **URL:** https://contra.com/creative-rlhf · https://contra.com/creative-human-data
- **Vendor:** Contra
- **Pricing tier:** Enterprise engagements with AI teams
- **Year:** Creative RLHF launched 2024
- **Core feature:** 1.5M+ vetted creative professionals (writers, designers, video/audio) ranking AI outputs for tone, brand fit, emotion, storytelling
- **Claims / techniques:** "Creative human data" for text/image/video/audio/multimodal; models "more human, brand-safe, and audience-ready"; Human Creativity Benchmark
- **2-3 sentence summary:** Contra Labs is the most on-nose vendor for a humanization product: they explicitly market RLHF for style, tone, creativity, and brand fit, not just helpfulness/harmlessness. Their reviewers are working creatives with real client experience, not generic annotators. This is close to a category-of-one in "taste-tuning" RLHF.
- **Takeaways:** Highest prior-art value for the humanization project.

### Fine-tuning platforms that expose DPO / RLHF

#### 11. OpenPipe — DPO + SFT fine-tuning
- **URL:** https://openpipe.ai/ · https://docs.openpipe.ai/features/dpo/quick-start
- **Vendor:** OpenPipe (YC W23)
- **Pricing tier:** Training $0.48/1M tokens (≤8B) up to $2.90/1M tokens (70B+); hosted inference from $0.30/$0.45 per 1M (Llama 3.1 8B)
- **Year:** Founded 2023; DPO added 2024
- **Core feature:** Production-oriented fine-tuning with DPO as a "drop-in" on preference data; tooling to convert overwritten responses into preference pairs
- **Claims / techniques:** DPO on Llama 3.1 8B; reward models (beta); "fine-tuning for production apps"
- **2-3 sentence summary:** OpenPipe is one of the few platforms with publicly listed, competitive per-token training pricing for preference-based fine-tuning. Its ergonomics — converting production-edit overrides into DPO pairs — are explicitly designed around the "capture human edits in the wild" pattern. Strong fit for humanization teams that already have edit logs.
- **Takeaways:** Best-priced, most transparent option for DPO at small model sizes.

#### 12. Together AI — Fine-Tuning Platform with DPO
- **URL:** https://together.ai/pricing · https://www.together.ai/blog/introducing-fine-tuning-platform
- **Vendor:** Together AI
- **Pricing tier:** Token-based; no minimum per job; varies by model size (<16B vs 16–69B) and method (LoRA vs full)
- **Year:** Founded 2022; DPO added April 2025
- **Core feature:** Managed fine-tuning with DPO, SFT, continued training, LoRA + full; large OSS model catalog
- **Claims / techniques:** DPO "stable and effective… does not require an additional reward model"; improves "helpfulness, tone, truthfulness, harmlessness, and instruction-following"
- **2-3 sentence summary:** Together AI added DPO in April 2025 as a formal part of their fine-tuning platform, pitching it as the commercial default for preference-based alignment. Pricing is purely token-based with no minimum, which is unusual. Their marketing explicitly names "tone" as a DPO lever, which maps directly to humanization.
- **Takeaways:** Broadest model support for DPO; "tone" called out as a target in public docs.

#### 13. Fireworks AI — Training API (RFT / GRPO / DAPO / ORPO / DPO)
- **URL:** https://fireworks.ai/ · https://docs.fireworks.ai/fine-tuning/training-api/introduction
- **Vendor:** Fireworks AI
- **Pricing tier:** RFT free for models <16B; Training API in private preview
- **Year:** Founded 2022; RL offerings 2024–2026
- **Core feature:** Full Python control over custom loss functions; RL objectives (GRPO, DAPO, DRO, GSPO, CISPO), DPO, ORPO, SFT; managed GPU infrastructure with BYOB option for sensitive data
- **Claims / techniques:** "Train frontier models like DeepSeek V3 and Kimi K2… without managing GPU infrastructure"; multi-turn remote-agent training
- **2-3 sentence summary:** Fireworks positions as the power-user platform for teams that want to write their own RL loop but not run their own cluster. Supports the widest set of preference/RL algorithms of any commercial offering and a true "bring your own bucket" for sensitive data. Free tier below 16B is aggressive and useful for humanization experiments.
- **Takeaways:** Best fit when humanization needs custom reward functions beyond vanilla DPO.

#### 14. Anyscale — Post-training on Ray
- **URL:** https://docs.anyscale.com/llm/fine-tuning
- **Vendor:** Anyscale (creators of Ray)
- **Pricing tier:** Compute-based (Ray cluster); enterprise
- **Year:** Founded 2019; LLM post-training product matured 2024–2025
- **Core feature:** SFT + preference tuning (DPO, KTO, ORPO), PPO-style RLHF, RLVR with GRPO/DAPO; LLaMA-Factory, SkyRL, and Ray Train frameworks; FSDP/DeepSpeed/Megatron
- **Claims / techniques:** "Preference tuning… refining model behavior based on human preferences for helpfulness, safety, politeness"; synthetic-data DPO cookbook
- **2-3 sentence summary:** Anyscale is the engineering-heavy option, best for teams comfortable running distributed training who want access to every modern post-training algorithm. Strong on monitoring/observability (W&B, MLflow, TensorBoard) which matters for iterative humanization experiments. Less managed than Together or Fireworks.
- **Takeaways:** Maximum flexibility; expects a real ML infra team.

#### 15. Lamini — Enterprise fine-tuning
- **URL:** https://www.lamini.ai/pricing
- **Vendor:** Lamini
- **Pricing tier:** $0.50/tuning step on-demand; $0.50/1M tokens inference; $300 free credit; Reserved plan for dedicated GPUs
- **Year:** Founded 2022
- **Core feature:** Managed tuning with memory-optimization (Mixture-of-Memory-Experts for hallucination reduction); enterprise support
- **Claims / techniques:** RLHF and preference tuning inside managed enterprise platform; LoRA + full tuning
- **2-3 sentence summary:** Lamini targets enterprises that want fine-tuning without infra, with a straightforward per-step price. Less focus on cutting-edge RL algorithms than Fireworks/Anyscale, more on stable managed delivery. Their on-prem/VPC option is a differentiator for regulated buyers.
- **Takeaways:** Conservative, managed option for enterprise humanization deployments.

#### 16. Predibase — Reinforcement fine-tuning (GRPO)
- **URL:** https://predibase.com/ · https://docs.predibase.com/
- **Vendor:** Predibase (acquired by Rubrik in 2025)
- **Pricing tier:** Free tier for SFT; GRPO/reinforcement fine-tuning gated to Enterprise SaaS and VPC tiers
- **Year:** Founded 2021; GRPO support 2024–2025
- **Core feature:** LoRA-first fine-tuning on A100 80GB; Python SDK; reinforcement fine-tuning via GRPO with custom reward functions
- **Claims / techniques:** "Fastest, most cost-effective way to fine-tune and serve open-source AI"; reinforcement fine-tuning for reasoning/alignment
- **2-3 sentence summary:** Predibase emphasizes cost-efficient LoRA + serving, with GRPO-based reinforcement fine-tuning as the premium-tier alignment capability. Rubrik's acquisition pulls it toward regulated-enterprise positioning. A good fit when humanization needs custom reward functions but on managed infrastructure.
- **Takeaways:** GRPO behind enterprise paywall limits tire-kicking but fits serious buyers.

#### 17. OpenAI — Direct Preference Optimization API
- **URL:** https://platform.openai.com/docs/guides/direct-preference-optimization
- **Vendor:** OpenAI
- **Pricing tier:** Standard fine-tuning per-token rates (same as SFT)
- **Year:** DPO API launched 2024–2025
- **Core feature:** Native DPO fine-tuning on GPT-4.1 / 4.1-mini / 4.1-nano with preference pairs (JSONL), `beta` hyperparameter
- **Claims / techniques:** "Best for tasks like summarizing text and generating chat messages with specific tone and style"
- **2-3 sentence summary:** OpenAI's DPO API is the first-party preference-tuning path and explicitly calls out "tone and style" as the target use case — essentially an official endorsement of DPO for humanization-style work. Tradeoff is closed weights and lock-in. Currently limited to single-turn text.
- **Takeaways:** Default for teams already on GPT-4.1; useful "tone" messaging mirrors humanization goals.

### Alignment-as-a-service / guardrails

#### 18. Snorkel AI — Snorkel Flow programmatic preferences
- **URL:** https://snorkel.ai/
- **Vendor:** Snorkel AI
- **Pricing tier:** Enterprise
- **Year:** Snorkel Flow launched 2019; LLM alignment tutorials/products 2024–2025
- **Core feature:** Programmatic weak-supervision + active learning to scale SME preference labeling; RLHF + DPO training workflows
- **Claims / techniques:** "Build high-quality scoring models in as little as a day"; labeling functions that encode SME preferences programmatically
- **2-3 sentence summary:** Snorkel's wedge is that manual RLHF labeling is slow and expensive, so they convert expert judgment into labeling functions that generate preferences at scale. This maps well onto humanization, where a small number of expert editors can encode "good writing" rules. Strong evaluation infra is a byproduct.
- **Takeaways:** Best for teams wanting to leverage a small expert group to generate lots of preference data programmatically.

#### 19. Defined.ai — Ethical RLHF / DPO services
- **URL:** https://defined.ai/llm-fine-tuning
- **Vendor:** Defined.ai
- **Pricing tier:** Managed services; custom
- **Year:** Founded 2015
- **Core feature:** RLHF & DPO, RAG, red teaming, benchmarking, A/B(x) testing; GDPR / HIPAA / ISO 27001/27701 posture
- **Claims / techniques:** "Ethically sourced data"; full compliance story
- **2-3 sentence summary:** Defined.ai is the compliance-forward RLHF vendor, trading raw expert depth for ethical-sourcing claims and regulated-industry fit. Appropriate for humanization work in healthcare, legal, or regulated content.
- **Takeaways:** Go-to when procurement wants GDPR/HIPAA-level guarantees.

#### 20. Alignx — Enterprise alignment platform
- **URL:** https://alignx.ai/services/
- **Vendor:** Alignx
- **Pricing tier:** Enterprise engagement
- **Year:** 2024–2025
- **Core feature:** Fine-tuning to enterprise policies/tone/ethical standards; automated eval suites; human-in-the-loop testing; red teaming; multi-metric quality scoring
- **Claims / techniques:** "Accelerate enterprise AI adoption with real ROI"; policy-as-alignment framing
- **2-3 sentence summary:** Alignx packages alignment as a consulting+platform hybrid for non-lab enterprises, treating tone and policy as first-class tuning targets. Good match for corporate humanization deployments where brand voice must align with explicit policies.

#### 21. Alinia — Safety/compliance API
- **URL:** https://alinia.ai/offerings/
- **Vendor:** Alinia
- **Pricing tier:** Basic API access through enterprise custom regulatory agents
- **Year:** 2024+
- **Core feature:** Model-agnostic safety/compliance layer: evaluation, guardrails, monitoring
- **Claims / techniques:** Runtime alignment layer sitting in front of any LLM
- **2-3 sentence summary:** Alinia is a guardrails/monitoring API rather than a training service — closer to Guardrails AI / Protect AI than to Surge/Scale. Useful downstream of a humanization pipeline to enforce runtime brand-safety and compliance.
- **Takeaways:** Complement, not substitute, for preference-tuning vendors.

#### 22. QASource — LLM alignment & optimization services
- **URL:** https://www.qasource.com/llm-model-alignment-and-optimization
- **Vendor:** QASource (large QA/outsourcing firm)
- **Pricing tier:** Managed services; custom
- **Year:** LLM offering 2023+
- **Core feature:** SFT, iterative RLHF, hyperspecific evaluation dataset generation, evaluation frameworks
- **2-3 sentence summary:** QASource is a traditional QA outsourcing firm applying its workforce to RLHF + evaluation work. Lower-cost than frontier specialists but less depth. Fit for humanization when evaluation volume matters more than expert ranking nuance.

#### 23. HumanTone — Consumer AI humanizer (adjacent)
- **URL:** https://humantone.io/
- **Vendor:** HumanTone
- **Pricing tier:** $10–$40/month; 1,000 free words
- **Year:** 2023+
- **Core feature:** Rewrites AI-generated content to sound human-written with custom tone/audience/purpose instructions; 60+ languages; built-in AI detection
- **Claims / techniques:** "20,000+ content professionals"; post-hoc rewriting rather than RLHF
- **2-3 sentence summary:** HumanTone is included as an adjacent consumer-tier offering that shows market demand for humanization but uses prompt-engineering + rewrites rather than RLHF/DPO. It establishes a price ceiling for thin humanizer wrappers and implicitly frames the opportunity for a deeper, preference-tuned alternative.
- **Takeaways:** Demonstrates market pull; a serious humanization product can likely out-quality these by going after preference-tuned model weights instead of post-hoc rewrites.

---

## Key Techniques / Patterns

- **Expert networks eat generic crowd labeling.** Every top-tier 2024–2026 RLHF vendor has explicitly moved away from generic crowd workers toward vetted domain experts (Surgers, Alignerrs, Mercor experts, Invisible trainers, Contra creatives). Crowd sources like Mechanical Turk are now a cost floor, not a quality option, for preference data.
- **DPO is the commercial default for preference tuning, not PPO.** Every fine-tuning platform (Together, OpenPipe, Fireworks, Anyscale, Predibase, Lamini, OpenAI) now exposes DPO first, with PPO-style RLHF reserved for teams with sophisticated reward-model pipelines. The marketing reason: no separate reward model, simpler data format.
- **GRPO / DAPO / RLVR are the emerging premium.** Fireworks, Anyscale, and Predibase all expose group-relative RL methods (GRPO, DAPO, DRO) and reinforcement learning from verifiable rewards. These are positioned as the path to reasoning/agentic gains, not raw preference tuning.
- **Edit-logs-as-preference-data is a productization pattern.** OpenPipe (in particular) has templatized the workflow of turning human edits of LLM outputs into preference pairs for DPO. This is the most practical pipeline for a humanization product with an edit surface.
- **"Tone and style" has moved into official platform marketing.** OpenAI's DPO docs and Together's DPO launch explicitly name tone and style as DPO use cases — preference tuning is no longer just helpfulness/harmlessness.
- **Small-expert-data beats large-generic-data.** Mercor's "fewer than 1,000 expert examples nearly doubled Pass@1" and Surge's "13% gain from human-crafted rubrics as RL rewards" both argue for quality-over-quantity. This makes expert-driven humanization economically viable at small scales.
- **Programmatic preference generation is emerging as a cost-reducer.** Snorkel AI's weak-supervision-of-preferences and Anyscale's synthetic-DPO cookbooks show a consistent industry move to amplify scarce expert judgment through automation.
- **Compliance/guardrails is a separate, smaller layer.** Alinia, Alignx, Defined.ai treat alignment as runtime/compliance enforcement rather than model training, suggesting the market is splitting into "train-time alignment" and "run-time alignment" as distinct line items.

---

## Notable Quotes

- Jared Kaplan, Anthropic co-founder: *"The team at Surge AI understands the unique challenges of training large language models… Their human data labeling platform is tailored to provide the unique, high-quality feedback needed for cutting-edge AI work. Surge AI is an excellent partner to us in supporting our technical AI alignment research."*
- Surge AI (on Hemingway-bench, their writing benchmark): *"Stop rewarding slop. Hemingway-bench is an AI writing leaderboard that takes real-world writing tasks and puts them in front of master wordsmiths. Our goal: to push AI writing from two-second vibes to genuine nuance and impact."*
- Labelbox: *"The data factory for AI teams… partnered with over 80% of leading US AI labs."*
- Contra Labs: *"Creative human data to fine-tune your AI for style, tone, and brand fit… so your models feel more human, brand-safe, and audience-ready."*
- Together AI (DPO launch): *"Direct Preference Optimization is stable and effective… does not require an additional reward model… improves helpfulness, tone, truthfulness, harmlessness, and instruction-following."*
- OpenAI (DPO guide): *"DPO works best for tasks like summarizing text and generating chat messages with specific tone and style."*
- Mercor: *"Fewer than 1,000 high-quality expert-labeled data points nearly doubled a model's Pass@1 and mean scores on the APEX-Agents benchmark."*
- Invisible Technologies: *"Producing 600 quality RLHF annotations costs approximately $60,000, roughly 167x more than the compute expense for training itself."*

---

## Emerging Trends

1. **Preference data as a $1B+/vendor business — with consolidation.** Surge AI ($1.2B+ revenue) and Scale AI (~$870M 2024 revenue) are now the two poles, but the Meta/Scale deal restructured the competitive landscape: Google, OpenAI, and xAI have reallocated budgets away from Scale toward Surge and Mercor. The annotation market is projected at $17–29B by 2030–2032.
2. **Scale/Meta deal is the defining market event of 2025.** Meta's $14.3B (49% non-voting stake) at ~$29B valuation closed June 2025. It simultaneously elevated Scale AI's valuation and made it effectively off-limits to Scale's existing top-tier AI lab customers. The strategic lesson: RLHF data is treated as a strategic moat, not a commodity service.
3. **"Taste" and "creativity" enter the RL reward stack.** Contra Labs (creative RLHF) and Surge's Hemingway-bench both productize the idea that aesthetic/tonal quality is a legitimate reward signal. This is the key trend for humanization.
4. **Verticalized evaluation benchmarks become a GTM wedge.** AdvancedIF (instruction-following), Hemingway-bench (writing), EnterpriseBench/CoreCraft (agentic), APEX (general) — vendors are building and owning the benchmarks their customers measure against, which also generates demand for their labeling services.
5. **Self-serve DPO pricing is converging around ~$0.50–$3/1M training tokens.** OpenPipe, Together, and Lamini are close enough in pricing that selection is now driven by ergonomics and model support, not raw cost.
6. **Reinforcement fine-tuning (GRPO/DAPO) is drifting down-market.** Fireworks, Anyscale, and Predibase already expose GRPO-style RL to enterprise customers. Expected to become commodity-priced the way DPO did in 2024–2025.
7. **Safety/guardrails is separating from training-time alignment.** Alinia, Alignx-style runtime layers are forming a distinct category, implying that a humanization stack will likely compose a fine-tuning vendor + a runtime guardrail vendor.
8. **Synthetic + programmatic preference amplification is a cost lever.** Snorkel Flow, Anyscale synthetic-DPO, and vendor "AI-assisted QA" (Toloka) all point to the same compression of expert hours into scaled preference signal.
9. **Expert data at small volume is the new hotspot.** Mercor's "fewer than 1,000 expert examples nearly doubled Pass@1" thesis gained credibility in 2025. The LIMA-style minimalism trend reinforces this: tiny, high-quality expert datasets outperform large generic ones for style/voice alignment specifically.
10. **Anti-sycophancy enters commercial specifications.** OpenAI's December 2025 Model Spec explicitly names sycophancy as a behavior to suppress. Expect commercial fine-tuning platforms to add anti-sycophancy objectives as a named checkbox in their DPO/RLHF pipelines by 2026.

---

## Open Questions / Gaps

- **No mainstream vendor prices "humanization" explicitly.** Contra Labs is closest, but there is no established SKU for "train a model on expert-writer preferences about human-sounding prose." This is either a real product gap or an unformed category.
- **Public cost-per-RLHF-sample is sparse.** Only Invisible Technologies ($0.50–$5 generic, ~$100 high-quality) and Surge (via annotator pay rates) give meaningful anchors. Hard to budget a humanization RLHF pipeline precisely.
- **Unclear who owns "writing quality" evaluation.** Surge's Hemingway-bench is the clearest candidate but is vendor-owned. No independent writing-quality benchmark has emerged comparable to MMLU or IFEval.
- **Demographic/audience targeting in RLHF is underbuilt.** Prolific can filter by demographics, but no vendor has productized "train this model to sound like it is talking to audience X." This is a likely humanization-specific gap.
- **Edit-log → preference-pair tooling is thin outside OpenPipe.** A production humanization product generating edit logs has few off-the-shelf options to turn those into DPO-ready data at scale.
- **Trust/provenance of "human-sounding" claims.** Consumer humanizers (HumanTone) advertise "beats AI detection," but there is no vendor-neutral way to measure "human-ness" of AI writing — a potential benchmark gap worth filling.
- **Closed vs. open model trade-off is unresolved.** OpenAI's DPO API ties humanization to GPT-4.1 family; open-model DPO (Together/OpenPipe/Anyscale) is cheaper and more controllable but loses access to frontier base-model quality. No vendor bridges this cleanly.
- **Post-Scale/Meta landscape is still settling.** Google, OpenAI, and xAI defecting from Scale creates vendor fragmentation. How this resolves — whether Surge takes their share entirely, or new entrants emerge — will determine the commercial RLHF data market structure for 2026–2027. Procurement decisions made in the next 12 months may need to be revisited.
- **Antitrust scrutiny of Meta/Scale deal.** European regulators opened an inquiry into whether Meta's "privileged access" framework constitutes unfair competitive advantage in foundation model development. Outcome could force unwinding or behavioral remedies — a live variable for anyone relying on Scale infrastructure.

---

## References

1. Scale AI Pricing — https://www.scale.ai/pricing
2. "A practical guide to Scale AI pricing in 2025" (eesel.ai) — https://www.eesel.ai/en/blog/scale-ai-pricing
3. Surge AI — https://www.surgehq.ai/
4. "How Anthropic uses Surge AI to Train and Evaluate Claude" — https://www.surgehq.ai/blog/anthropic-surge-ai-rlhf-platform-train-llm-assistant-human-feedback
5. Surge AI revenue / funding (Reuters, Sacra, Wikipedia) — https://www.reuters.com/business/scale-ais-bigger-rival-surge-ai-seeks-up-1-billion-capital-raise-sources-say-2025-07-01/ · https://sacra.com/research/surge-ai
6. Surge "Hemingway-bench" writing leaderboard — https://www.surgehq.ai/blog/hemingway-bench-ai-writing-leaderboard
7. Labelbox — https://www.labelbox.com/ · Alignerr Connect — https://labelbox.com/services/alignerr-connect/ · Alignerr — https://www.alignerr.com/
8. Mercor Research — https://mercor.com/research/ · Blog — https://www.mercor.com/blog/expert-data-drives-model-performance
9. Invisible Technologies — https://www.invisible.co/blog/supervised-fine-tuning-vs-rlhf-how-to-choose-the-right-approach-to-train-your-llm · https://invisibletech.ai/
10. Toloka AI Platform & Pricing — https://toloka.ai/platform · https://toloka.ai/pricing/
11. Prolific AI Services & Alignment — https://www.prolific.com/ai-services · https://prolific.com/alignment
12. Rapidata — https://rapidata.ai/guides/preference-dataset-demo · https://rapidata.ai/blog/rich-human-feedback
13. Contra Labs — https://contra.com/creative-rlhf · https://contra.com/creative-human-data
14. OpenPipe Pricing & DPO docs — https://docs.openpipe.ai/pricing/pricing · https://docs.openpipe.ai/features/dpo/quick-start
15. Together AI — Fine-Tuning Platform DPO launch — https://www.together.ai/blog/introducing-fine-tuning-platform · Pricing — https://docs.together.ai/docs/fine-tuning-pricing
16. Fireworks AI — Reinforcement Fine-Tuning — https://docs.fireworks.ai/fine-tuning/reinforcement-fine-tuning-models · Training API — https://docs.fireworks.ai/fine-tuning/training-api/introduction
17. Anyscale — Post-training docs — https://docs.anyscale.com/llm/fine-tuning · DPO blog — https://anyscale.com/blog/direct-preference-optimization-with-synthetic-data
18. Lamini Pricing — https://www.lamini.ai/pricing
19. Predibase — Fine-Tuning Overview — https://docs.predibase.com/guides/fine-tuning/overview · Reinforcement Fine-Tuning — https://docs.predibase.com/fine-tuning/tasks/reinforcement
20. OpenAI DPO API — https://platform.openai.com/docs/guides/direct-preference-optimization · Cookbook — https://cookbook.openai.com/examples/fine_tuning_direct_preference_optimization_guide
21. Snorkel AI — Programmatic preferences — https://snorkel.ai/blog/scaling-human-preferences-in-ai-snorkel-s-programmatic-approach/
22. Defined.ai LLM Fine-Tuning — https://defined.ai/llm-fine-tuning
23. Alignx — https://alignx.ai/services/
24. Alinia — https://alinia.ai/offerings/
25. QASource — https://www.qasource.com/llm-model-alignment-and-optimization
26. HumanTone — https://humantone.io/
