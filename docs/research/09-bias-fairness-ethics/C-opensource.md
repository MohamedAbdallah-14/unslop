# Category 09 — Bias, Fairness & Ethics

## Angle C — Open-Source & GitHub

**Context:** External grounding for the Humanizer project on the ethics of making AI output "more human." This angle maps the open-source landscape of tools that measure or mitigate the exact failure modes a humanization layer can amplify: sycophancy, stereotype bias, dishonesty/deception, opacity, and unaccountable outputs.

**Research value: high** — The open-source ecosystem for LLM ethics has matured rapidly (2021–2026). There are now dedicated repos for nearly every failure mode a "humanizing" layer can worsen, plus mature multi-metric harnesses (HELM, Inspect, lm-eval-harness) that already fold bias/toxicity/honesty checks into a single pipeline. A humanizer that does not plug into at least one of these is flying blind.

---

## Repositories

Standard fields per entry: **Repo · Owner/Org · Stars (approx) · License · Language · Last active · Relevance to Humanizer**.

### 1. Sycophancy Evaluation

#### 1a. `anthropics/evals` — model-written sycophancy datasets
- **Org:** Anthropic · **Stars:** ~360 · **License:** MIT · **Language:** Jupyter / JSONL · **Last active:** 2024
- **URL:** https://github.com/anthropics/evals
- **What it is:** Companion datasets for Anthropic's *Discovering Language Model Behaviors with Model-Written Evaluations* and *Towards Understanding Sycophancy*. Four dataset families: `persona/`, `sycophancy/`, `advanced-ai-risk/`, `winogender/`. Each `.jsonl` has ~10k examples pairing a generated user biography with a question.
- **README quote:**
  > "We test for sycophancy on philosophy questions from the PhilPapers 2020 Survey, Natural Language Processing Survey, and political questions from the Pew Research Center Political Typology Quiz. We generate biographies for users who have a particular view on the question at hand… We then append the sourced questions to the biography, to simulate a user with a particular view asking a question."
- **Relevance to Humanizer:** Directly tests the core hazard of a humanizer — that making output "warmer" slides into agreeing with whoever the user is. Use the `sycophancy/sycophancy_on_*.jsonl` files as regression tests against the humanized model and the base model, measuring how often answer-matching-behavior shifts.

#### 1b. `meg-tong/sycophancy-eval`
- **Stars:** ~150 · **License:** MIT · **Language:** Python / Jupyter · **Last active:** 2023–2024
- **URL:** https://github.com/meg-tong/sycophancy-eval
- **What it is:** Companion code to the Sharma et al. Anthropic sycophancy paper covering free-form generation (not just MCQ). Three datasets: `feedback.jsonl` (commenting on arguments with biasing user framing), `are_you_sure.jsonl` (retracting correct answers under soft pushback), `answer.jsonl` (agreeing with leading user suggestions).
- **Relevance to Humanizer:** The only widely-used eval that catches "are you sure?" capitulation — a classic humanized-assistant failure mode.

#### 1c. `timfduffy/syco-bench`
- **Stars:** small / growing · **License:** MIT · **Language:** Python/TeX · **Last active:** 2024–2025
- **URL:** https://github.com/timfduffy/syco-bench · site: https://syco-bench.com
- **What it is:** Four-part sycophancy benchmark: *Delusion Acceptance*, *Attribution Bias* (favoring ideas attributed to the user), *Mirroring* (shifting position to match user), *Picking Sides* (siding with user against a friend). Runs via OpenRouter.
- **Relevance to Humanizer:** The four-axis decomposition matches exactly how a humanization layer can fail — each axis is a distinct hazard of emotional mirroring.

#### 1d. `JiseungHong/SYCON-Bench`
- **License:** MIT · **Language:** Python · **Last active:** 2025
- **URL:** https://github.com/JiseungHong/SYCON-Bench
- **What it is:** Multi-turn conversational sycophancy. Measures *Turn of Flip* (how many turns of user pressure before the model caves) and *Number of Flips*. Three scenarios: debates, ethical questions with harmful stereotypes, false-presupposition questions.
- **Relevance to Humanizer:** Single-turn sycophancy evals underestimate the problem; humanized chat is almost always multi-turn. This is the benchmark to use for dialogue products.

#### 1e. `lechmazur/sycophancy` ("Narrator-Bias Benchmark")
- **License:** MIT · **Language:** Python · **Last active:** 2025
- **URL:** https://github.com/lechmazur/sycophancy
- **What it is:** Measures sycophancy by swapping first-person perspective across opposing narrators and checking whether the model's moral/judgment call flips with the speaker.
- **Relevance to Humanizer:** Useful as a smoke test — very cheap, runs on any chat API, and catches the most egregious narrator-identification failures.

### 2. Bias Benchmarks (stereotype / social)

#### 2a. `nyu-mll/BBQ` — Bias Benchmark for QA
- **Stars:** ~140 · **License:** CC-BY-4.0 · **Language:** Python/HTML/R · **Last active:** maintained
- **URL:** https://github.com/nyu-mll/BBQ
- **What it is:** ACL 2022 dataset of QA items probing social bias across nine U.S. social dimensions (age, disability, gender identity, nationality, physical appearance, race/ethnicity, religion, SES, sexual orientation). Tests at two context levels: ambiguous (does the model fall back on bias?) and disambiguated (does bias override the correct answer?).
- **Relevance to Humanizer:** A humanizer that adds personality risks leaking stereotypes via persona ("a working-class dad from Texas would say…"). BBQ is the cleanest way to measure that drift.

#### 2b. `nyu-mll/crows-pairs` — CrowS-Pairs
- **Stars:** ~130 · **License:** CC-BY-SA-4.0 · **Language:** Python · **Last active:** maintained
- **URL:** https://github.com/nyu-mll/crows-pairs
- **What it is:** 1,508 crowdsourced minimal pairs across nine bias types. Each pair is a stereotypical vs. less-stereotypical sentence; the score is how often the LM prefers the stereotyped version.
- **Caveat:** Blodgett et al. (2021) documented significant noise/reliability issues — use it as one signal among several, not as ground truth.
- **Relevance to Humanizer:** Intrinsic (no prompt needed) — cheap to re-run every time a style/persona layer changes.

#### 2c. `moinnadeem/StereoSet`
- **Stars:** ~200 · **License:** CC-BY-SA-4.0 · **Language:** Python · **Last active:** Dec 2022 (unmaintained; see bias-bench)
- **URL:** https://github.com/moinnadeem/StereoSet
- **What it is:** Context Association Tests (CATs) over gender, profession, race, religion. Produces a Stereotype Score (SS) and Language Modeling Score (LMS), combined into an ICAT metric.
- **Relevance to Humanizer:** The ICAT formulation explicitly captures the humanizer tradeoff — you can't just suppress bias by degrading fluency.

#### 2d. `uclanlp/corefBias` — WinoBias
- **License:** MIT · **Language:** Python · **Last active:** maintained
- **URL:** https://github.com/uclanlp/corefBias
- **What it is:** 3,160 sentences probing gender bias in coreference resolution using occupations with documented U.S. Labor stereotypes, with pro- and anti-stereotypical pairs.
- **Relevance to Humanizer:** Pronoun handling is where a human-sounding assistant quietly smuggles in stereotypes ("the nurse… she").

#### 2e. `McGill-NLP/bias-bench`
- **Stars:** ~155 · **License:** Apache-2.0 · **Language:** Python · **Last active:** 2025
- **URL:** https://github.com/McGill-NLP/bias-bench
- **What it is:** Unified harness from Meade et al. covering StereoSet, CrowS-Pairs, SEAT plus five debiasing techniques (CDA, Dropout, Iterative Nullspace Projection, Self-Debias, SentenceDebias). Maintained leaderboard.
- **Relevance to Humanizer:** If the humanizer adds a debiasing step, this is the standard harness to compare against.

### 3. Honesty / Deception Evaluation

#### 3a. `centerforaisafety/mask` — MASK Benchmark
- **License:** MIT · **Language:** Python · **Last active:** 2025
- **URL:** https://github.com/centerforaisafety/mask · paper: arXiv 2503.03750
- **README quote:**
  > "MASK (Model Alignment between Statements and Knowledge) is a benchmark designed to evaluate honesty in large language models by testing whether they contradict their own beliefs when pressured to lie. MASK disentangles honesty from factual accuracy… We find that scaling pre-training does not improve model honesty."
- **What it is:** 1,028 human-labeled examples across six archetypes (continuations, disinformation, doubling-down on known facts, known_facts, provided_facts, statistics). Designed to separate "wrong" from "lying."
- **Relevance to Humanizer:** The *most* important benchmark for this project. A humanized model is under constant implicit social pressure (politeness, user-pleasing). MASK directly measures whether that pressure flips the model into lying.

#### 3b. `sylinrl/TruthfulQA`
- **Stars:** ~900 · **License:** Apache-2.0 · **Language:** Python · **Last active:** 2025 (MC v2 release Jan 2025)
- **URL:** https://github.com/sylinrl/TruthfulQA
- **What it is:** 817 questions across 38 categories crafted to elicit "imitative falsehoods" — false answers the model learned from frequent internet repetition. Famous for showing inverse scaling (GPT-J 6B was 17% less truthful than its 125M variant).
- **Relevance to Humanizer:** A humanizer trained on chatty/casual text risks amplifying the exact folk-myth patterns TruthfulQA is built to surface.

#### 3c. `GAIR-NLP/BeHonest`
- **License:** Apache-2.0 · **Language:** Python · **Last active:** 2024
- **URL:** https://github.com/GAIR-NLP/BeHonest
- **What it is:** Holistic honesty benchmark across three axes — self-knowledge (admitting unknowns), non-deceptiveness (including persona-sycophancy and burglar-deception scenarios), and response consistency. 10 sub-scenarios, leaderboard over 9 frontier models.
- **Relevance to Humanizer:** The *persona sycophancy* sub-scenario is the closest externally available match to what the Humanizer project is likely to produce.

#### 3d. `Aries-iai/DeceptionBench`
- **License:** MIT · **Language:** Python · **Last active:** 2024–2025
- **URL:** https://github.com/Aries-iai/DeceptionBench
- **What it is:** 150 scenarios / 1,000+ samples across economy, healthcare, education, social, entertainment. Tests internal influences (self vs. other perspectives) and external influences (rewards, pressure, multi-turn).
- **Relevance to Humanizer:** Decomposes deception by *motivation*, which maps cleanly to "why a humanized model might lie" (user-pleasing, role-consistency, reward-seeking).

#### 3e. `lechmazur/deception`
- **License:** MIT · **Last active:** rolling leaderboard, 2025
- **URL:** https://github.com/lechmazur/deception
- **What it is:** Two-way benchmark — how well a model can generate convincing disinformation and how well it resists being misled. Uses post-cutoff articles to reduce memorization contamination.

### 4. Multi-Metric / Holistic Harnesses

#### 4a. `stanford-crfm/helm` — HELM
- **Stars:** ~2,700 · **License:** Apache-2.0 · **Language:** Python · **Last active:** active (v0.5.14)
- **URL:** https://github.com/stanford-crfm/helm
- **README quote:**
  > "Holistic Evaluation of Language Models (HELM) is an open source Python framework… for holistic, reproducible and transparent evaluation of foundation models… Metrics for measuring various aspects beyond accuracy (e.g. efficiency, bias, toxicity)."
- **What it is:** The most comprehensive academic eval framework. Separate leaderboards for *Capabilities*, *Safety*, VHELM (vision-language), HEIM (T2I), MedHELM, audio. The original paper evaluated 30 models across 42 scenarios with 7 metrics including bias, toxicity, fairness, calibration, robustness.
- **Relevance to Humanizer:** Not just a bias benchmark — it is the framework that standardizes *how* to report bias and toxicity alongside capability, which a humanizer launch blog post should mirror.

#### 4b. `EleutherAI/lm-evaluation-harness`
- **Stars:** ~12k · **License:** MIT · **Language:** Python · **Last active:** active (v0.4.11)
- **URL:** https://github.com/EleutherAI/lm-evaluation-harness
- **What it is:** 60+ standardized benchmarks including BBQ, CrowS-Pairs, TruthfulQA, ToxiGen. Powers the HuggingFace Open LLM Leaderboard. YAML-configured, supports vLLM/SGLang/Anthropic/OpenAI/local.
- **Relevance to Humanizer:** Lowest-friction path to run the entire bias/honesty suite against a humanized model with one config file.

#### 4c. `UKGovernmentBEIS/inspect_ai`
- **Stars:** ~1,900 · **License:** MIT · **Language:** Python · **Last active:** active (UK AISI)
- **URL:** https://github.com/UKGovernmentBEIS/inspect_ai · evals: https://github.com/UKGovernmentBEIS/inspect_evals
- **What it is:** LLM evaluation framework by the UK AI Security Institute. 100+ pre-built evals in a companion repo (co-built with Arcadia Impact and Vector Institute). Strong agent/tool-use and sandbox support (Docker/Kubernetes/Modal).
- **Relevance to Humanizer:** The *governance-grade* framework — if Unslop ever needs to produce UK/EU-regulator-legible reports, Inspect is the emerging standard.

#### 4d. `openai/evals`
- **Stars:** ~18k · **License:** MIT · **Language:** Python · **Last active:** active
- **URL:** https://github.com/openai/evals
- **What it is:** Registry-of-evals framework with model-graded and logic-graded rubrics; runs in CI before deployment.
- **Relevance to Humanizer:** The most natural home for *custom* humanization-specific evals (tone, warmth, non-sycophancy) that don't exist in academic benchmarks yet.

#### 4e. `google/BIG-bench`
- **Stars:** ~3,200 · **License:** Apache-2.0 · **Language:** Python · **Last active:** frozen/maintained
- **URL:** https://github.com/google/BIG-bench
- **What it is:** 214 community-contributed tasks including multiple bias/social-reasoning tasks. BIG-bench Lite (24 tasks) is the practical subset.
- **Relevance to Humanizer:** Mostly capability-focused, but several bias and social-understanding tasks (e.g., moral permissibility, social IQ) are directly relevant for measuring a humanizer's social competence.

### 5. Toxicity & Safety Datasets

#### 5a. `allenai/real-toxicity-prompts`
- **License:** Apache-2.0 · **Language:** Python
- **URL:** https://github.com/allenai/real-toxicity-prompts
- **What it is:** 100k naturally-occurring web prompts scored via Perspective API across toxicity, profanity, sexually_explicit, identity_attack, flirtation, threat, insult, severe_toxicity.
- **Relevance to Humanizer:** A humanizer that relaxes formality can also relax guardrails. RTP is the standard degeneration test.

#### 5b. `microsoft/TOXIGEN`
- **License:** MIT · **Language:** Python
- **URL:** https://github.com/microsoft/toxigen
- **What it is:** 250k machine-generated (ACL 2022) + 27k human-annotated (2024) examples of *implicit* toxicity targeting 13 minority groups. Includes ALICE, an adversarial stress-test tool for moderation classifiers.
- **Relevance to Humanizer:** Explicit toxicity is easy to filter; TOXIGEN targets the implicit / coded-language kind, which is exactly what a "warmer, more human" rewrite layer can produce accidentally.

### 6. Model Cards & Transparency

#### 6a. `tensorflow/model-card-toolkit`
- **Stars:** ~450 · **License:** Apache-2.0 · **Language:** Python · **Status:** **archived Sept 2024** (successor in `tensorflow/tfx-addons`)
- **URL:** https://github.com/tensorflow/model-card-toolkit
- **What it is:** Google's model card generator — auto-scaffolds JSON, exports HTML/PDF. Based on Mitchell et al., "Model Cards for Model Reporting" (FAccT 2019).
- **Relevance to Humanizer:** Still the canonical schema even though the tool is archived. A humanizer release should ship a model card that documents the bias/sycophancy deltas vs. base.

#### 6b. `stanford-crfm/fmti` — Foundation Model Transparency Index
- **License:** CC-BY · **Last active:** Dec 2025 update
- **URL:** https://github.com/stanford-crfm/fmti
- **What it is:** 100 transparency indicators covering upstream resources (data, labor, compute), capabilities/risks, and downstream use. December 2025 release scored 13 developers (OpenAI, Google, Meta, DeepSeek, Alibaba, xAI, Midjourney, etc.).
- **Relevance to Humanizer:** The external yardstick for "what honest disclosure of a humanization layer looks like."

#### 6c. `compl-ai/compl-ai`
- **License:** Apache-2.0 · **Language:** Python
- **URL:** https://github.com/compl-ai/compl-ai
- **What it is:** ETH Zurich / INSAIT / LatticeFlow AI. A technical interpretation of the EU AI Act into 29+ concrete benchmarks, with a public HuggingFace leaderboard. First attempt to make the AI Act programmatically testable.
- **Relevance to Humanizer:** Any EU-market-facing humanization product will eventually need something that looks like this. Already covers bias, privacy, and robustness mappings.

### 7. Algorithmic Audit / Fairness Toolkits

#### 7a. `Trusted-AI/AIF360` — IBM AI Fairness 360
- **Stars:** ~2,800 · **License:** Apache-2.0 · **Language:** Python (95%) / R / Java
- **URL:** https://github.com/Trusted-AI/AIF360
- **What it is:** 10 bias-mitigation algorithms (Reweighing, Disparate Impact Remover, Equalized Odds Postprocessing, Calibrated Equalized Odds, Prejudice Remover, Adversarial Debiasing, Learning Fair Representations, Meta-Fair Classifier, Reject Option Classification, Optimized Preprocessing) plus a large metric library. Originally tabular, extended since.
- **Relevance to Humanizer:** More applicable to downstream decisioning systems than to generation. Useful as a vocabulary source for fairness metrics.

#### 7b. `fairlearn/fairlearn`
- **Stars:** ~2,200 · **License:** MIT · **Language:** Python
- **URL:** https://github.com/fairlearn/fairlearn
- **What it is:** Group-fairness metrics and mitigation (Reductions, Grid Search, ThresholdOptimizer, Postprocessing). Grounds itself in a specific framing:
  > "Fairlearn defines unfairness in terms of harms to people: *allocation harms* (extending or withholding opportunities/resources/information) and *quality-of-service harms* (systems work better for some people than others)."
- **Relevance to Humanizer:** The "quality-of-service" framing maps naturally to humanization: does the "more human" output work equally well for users across demographic groups?

#### 7c. `microsoft/responsible-ai-toolbox`
- **Stars:** ~1,750 · **License:** MIT · **Language:** TypeScript (UI) + Python
- **URL:** https://github.com/microsoft/responsible-ai-toolbox
- **README quote:**
  > "Responsible AI Toolbox is a suite of tools providing a collection of model and data exploration and assessment user interfaces and libraries… empower developers and stakeholders of AI systems to develop and monitor AI more responsibly."
- **What it is:** Integrates Fairlearn, InterpretML, DiCE (counterfactuals), EconML (causal) under one dashboard. Companion repos: `responsible-ai-toolbox-mitigations`, `responsible-ai-toolbox-tracker` (JupyterLab extension), `responsible-ai-toolbox-genbit` (NLP gender-bias metrics).
- **Relevance to Humanizer:** The GenBit sub-repo is directly applicable; the dashboard gives a drop-in UI for presenting audit results.

#### 7d. `dssg/aequitas` — University of Chicago DSSG
- **Stars:** ~750 · **License:** MIT · **Language:** Python
- **URL:** https://github.com/dssg/aequitas
- **What it is:** The prototypical *policymaker-oriented* audit toolkit. Web tool + Python + CLI. Metrics: Equal Parity, Proportional Parity, False Positive Parity, False Negative Parity. v1.0 added "Aequitas Flow" for bias-mitigation experimentation. Ships with a COMPAS recidivism walkthrough.
- **Relevance to Humanizer:** Best reference for how an *audit report* (not just a benchmark number) should be structured.

### 8. Interpretability / Visualization (adjacent)

#### 8a. `jalammar/ecco`
- **License:** BSD-3-Clause · **Language:** Python
- **URL:** https://github.com/jalammar/ecco
- **What it is:** In-notebook visualization of GPT-2/BERT/T5/T0 behavior — logit-lens token evolution, per-neuron activations, and feature attribution (Integrated Gradients, DeepLift, Guided Backprop, LRP, etc.).
- **Relevance to Humanizer:** If the humanization layer is an attached adapter or prompt wrapper, Ecco-style attribution shows *which* tokens the humanizing wrapper actually moved.

---

## Patterns, Trends, Gaps

### Patterns

1. **The one-dataset-per-failure-mode era is ending; harnesses are winning.** Five years ago, each failure mode (stereotype bias, toxicity, honesty) had its own repo with its own scoring script. Today, `lm-evaluation-harness`, HELM, and Inspect each wrap dozens of these under one YAML-configured pipeline. For Unslop this means: do not write custom glue. Pick one harness and plug the humanizer in as a model endpoint.
2. **Honesty has split from accuracy.** TruthfulQA (2021) still conflates them. MASK (2025) and BeHonest (2024) explicitly separate "the model got it wrong" from "the model lied under pressure." This is the single biggest methodological shift relevant to Humanizer, because social pressure is the thing a humanizer adds.
3. **Sycophancy went from a side-comment in Anthropic's 2022 eval repo to a full subfield in 2024–2025.** Five dedicated repos now exist (syco-bench, SYCON-Bench, sycophancy-eval, lechmazur/sycophancy, plus Anthropic's original). Multi-turn evaluation (SYCON-Bench) consistently finds models are more sycophantic than single-turn tests suggest.
4. **Transparency tooling is consolidating around the EU AI Act.** FMTI, COMPL-AI, and Glassbox-AI 2.0 all frame themselves against Annex IV / Article 50 obligations. A humanization product shipping into the EU in 2026 will be assumed by auditors to be testable by these tools.
5. **Model cards are standard but tooling is underpowered.** The TensorFlow Model Card Toolkit is *archived*. HuggingFace's model-card template is effectively the default, but there is no thriving open-source successor to the original Google toolkit.
6. **Industry labs (Anthropic, OpenAI, Microsoft, UK AISI) now open-source their eval infrastructure** rather than just publishing papers — a marked change from 2020–2022. This makes replication and adversarial use dramatically easier.

### Trends

- **Dynamic / adversarial > static benchmark.** MASK, SYCON-Bench, DeceptionBench, and BeHonest all test behavior under *pressure* (user pushback, incentives, role-play framing), not just on a fixed prompt.
- **"Persona sycophancy" is an emerging named hazard** (BeHonest, model-persona subset of anthropics/evals). Directly names what a humanizer does: give the model a character, then see if honesty degrades.
- **Contamination awareness is growing.** `lechmazur/deception` explicitly uses post-cutoff articles; newer TruthfulQA releases track memorization; HELM rotates scenarios. Any humanizer eval should assume test-set leakage and design accordingly.
- **Cross-pollination between capability and safety harnesses.** Inspect and HELM both now include honesty/bias evals alongside MMLU, GPQA, etc. The dichotomy "capability benchmarks vs. safety benchmarks" is dissolving.
- **Implicit > explicit for toxicity.** ToxiGen's shift to implicit hate-speech (and its +2024 human annotations) reflects the field catching up to the reality that safety filters already stop explicit toxicity; the remaining problem is coded/implicit forms, which is exactly where humanization lives.

### Gaps — opportunities for the Humanizer project

1. **No dedicated "humanized output" benchmark exists.** The closest are persona sycophancy (BeHonest) and model-persona (anthropics/evals), but neither measures *whether the humanization goal was achieved* (warmth, naturalness) *against* whether it degraded honesty/fairness. This is a distinct axis and a real publishable contribution.
2. **No open tool measures the sycophancy ↔ warmth tradeoff jointly.** Sycophancy evals score dishonesty; naturalness/warmth evals (LMSYS-style preference, MT-Bench) score style. Nothing plots them on the same chart. This is a one-weekend extension on top of lm-eval-harness or Inspect.
3. **"Responsible AI Toolbox" has nothing generative-text-specific beyond GenBit.** The dashboard is strong for tabular classification; adapting it for humanized chat output is open territory.
4. **Model card generators for LLM rewrite/style layers don't exist.** All current tools (TF MCT, HF model-card UI) assume a single model, not a wrapper layer. A humanization adapter that ships without disclosure of sycophancy/bias deltas vs. base is arguably under-documented by 2026 standards — and there's no off-the-shelf template for doing it right.
5. **Multi-turn + multi-lingual gap.** Almost all sycophancy and honesty repos are English-only. Humanization is inherently cultural; the EN-only assumption is a limitation waiting to be exploited.
6. **No standard red-team harness for "vibe drift."** A humanizer can stay within policy on toxicity and still produce outputs that are culturally tone-deaf, inappropriately flirty, or parasocial. The closest adjacent work is RealToxicityPrompts + flirtation scoring, but no one has stitched this into a dedicated "parasocial risk" eval.

---

## Sources

- https://github.com/anthropics/evals — Anthropic model-written evals (sycophancy/persona/risk)
- https://github.com/centerforaisafety/mask — MASK honesty benchmark (CAIS + Scale)
- https://github.com/stanford-crfm/helm — HELM framework
- https://github.com/stanford-crfm/fmti — Foundation Model Transparency Index
- https://github.com/microsoft/responsible-ai-toolbox — Microsoft RAI Toolbox
- https://github.com/fairlearn/fairlearn — Fairlearn
- https://github.com/Trusted-AI/AIF360 — IBM AIF360
- https://github.com/dssg/aequitas — U. Chicago DSSG Aequitas
- https://github.com/nyu-mll/BBQ, https://github.com/nyu-mll/crows-pairs — NYU bias benchmarks
- https://github.com/uclanlp/corefBias — WinoBias
- https://github.com/McGill-NLP/bias-bench — Unified bias/debiasing harness
- https://github.com/sylinrl/TruthfulQA — TruthfulQA
- https://github.com/GAIR-NLP/BeHonest — BeHonest multi-axis honesty
- https://github.com/Aries-iai/DeceptionBench, https://github.com/lechmazur/deception — deception benchmarks
- https://github.com/timfduffy/syco-bench, https://github.com/JiseungHong/SYCON-Bench, https://github.com/meg-tong/sycophancy-eval, https://github.com/lechmazur/sycophancy — sycophancy benchmark family
- https://github.com/EleutherAI/lm-evaluation-harness — EleutherAI eval harness
- https://github.com/UKGovernmentBEIS/inspect_ai — UK AISI Inspect
- https://github.com/openai/evals — OpenAI evals
- https://github.com/google/BIG-bench — BIG-bench
- https://github.com/allenai/real-toxicity-prompts — RealToxicityPrompts (AllenAI)
- https://github.com/microsoft/toxigen — ToxiGen (Microsoft)
- https://github.com/tensorflow/model-card-toolkit — TF Model Card Toolkit (archived 2024)
- https://github.com/compl-ai/compl-ai — ETH/INSAIT/LatticeFlow EU AI Act harness
- https://github.com/jalammar/ecco — Ecco interpretability visualizer
