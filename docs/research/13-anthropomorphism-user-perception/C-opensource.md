# Anthropomorphism & User Perception — Angle C: Open-Source Tools & Benchmarks

**Research value: high** — A mature ecosystem of open tools exists for measuring anthropomorphism, humanness, trust, and perceived agency in AI. Microsoft HAX, Google PAIR, validated HRI scales (Godspeed, RoSAS, Jian TiA), and a second wave of LLM-era benchmarks (AnthroScore, AnthroBench, HumT/DumT, HumanAgencyBench, Jones & Bergen Turing test) are directly portable to a "humanize AI output" project.

Scope: project "Humazier" is about humanizing AI output and thinking. This digest inventories the open instruments that can be reused to *measure* whether humanization works — perceived humanness, anthropomorphism, trust, agency, social attributes — plus frameworks that govern *how* humanization should be designed (HAX, PAIR).

---

## Repository / tool inventory

### 1. Microsoft HAX Playbook

- **Repo:** [`microsoft/HAXPlaybook`](https://github.com/microsoft/HAXPlaybook)
- **Stars / language / license:** ~58★ · TypeScript (75%) · MIT
- **What it is:** Interactive scenario generator for stress-testing user-facing AI systems against the 18 Guidelines for Human-AI Interaction. Content (scenarios, surveys) is defined in JSON so teams can fork and customize.
- **README quote:** "The HAX Playbook is an interactive tool for generating interaction scenarios to test when designing user-facing AI systems."
- **Relevance to Humazier:** The Playbook's failure-scenario framing (especially for NLP) is the cleanest checklist for "when does humanized output go wrong?" — false intimacy, over-promising, mismatched register.

### 2. Microsoft HAX Toolkit (website resources)

- **Home:** [microsoft.com/haxtoolkit](https://www.microsoft.com/en-us/haxtoolkit/) · aka.ms/haxtoolkit
- **License:** CC BY-NC-SA (non-code materials)
- **What it is:** Bundle of four artifacts: (1) 18 evidence-based Guidelines for Human-AI Interaction, (2) HAX Design Library with patterns/examples per guideline, (3) HAX Workbook (team-alignment worksheet), (4) HAX Playbook (the code repo above).
- **Relevant guidelines for humanization:** "Match relevant social norms," "Mitigate social biases," "Make clear what the system can do," "Convey the consequences of user actions." These directly constrain how far humanization can go before it becomes deceptive.

### 3. Microsoft Responsible AI Toolbox

- **Repo:** [`microsoft/responsible-ai-toolbox`](https://github.com/microsoft/responsible-ai-toolbox)
- **Stars / language / license:** ~1,750★ · TypeScript (82%), Python (14%) · MIT
- **What it is:** Dashboards for model assessment, error analysis, interpretability, counterfactuals. Not anthropomorphism-specific, but the "error analysis per user cohort" pattern is reusable for measuring whether humanization changes failure modes for subgroups.

### 4. Google PAIR — People + AI Guidebook / pair-code

- **Home:** [pair.withgoogle.com/guidebook](https://pair.withgoogle.com/guidebook-v2) · source on [`PAIR-code/pair-code.github.io`](https://github.com/PAIR-code)
- **License:** CC BY-NC-SA 4.0
- **What it is:** Six chapters of design patterns for human-centered AI, updated April 2025 with generative-AI guidance. Covers trust calibration, explainability, user control, feedback, mental models.
- **Relevance:** Pair with HAX — PAIR is more product-flow oriented; HAX is more guideline-enforcement oriented. Use PAIR's "Help users build and calibrate trust" chapter to avoid anthropomorphism-driven over-trust.

### 5. AnthroScore (Cheng et al., EACL 2024)

- **Repo:** [`myracheng/AnthroScore`](https://github.com/myracheng/AnthroScore)
- **Stars / language / license:** ~18★ · Python · BSD-2-Clause
- **What it is:** Masked-LM-based metric that quantifies how a non-human entity is implicitly framed as human by surrounding context. Lexicon-free, applies to any text. Install via `pip install anthroscore-eacl`.
- **README quote:** "Code to compute AnthroScore, a computational linguistic measure of anthropomorphism in text."
- **Relevance:** First-choice automatic metric for the Humazier project. Can be applied to (a) input prompts, (b) model outputs, (c) user follow-ups to track whether humanization pushes the conversation toward anthropomorphic framing. Paper shows NLP / LLM papers have the highest anthropomorphism of any CS subfield over 15 years.

### 6. HumT / DumT / SocioT (Stanford)

- **Repo:** [`myracheng/humtdumt`](https://github.com/myracheng/humtdumt)
- **Language / license:** Python · (see repo)
- **What it is:** Companion framework to AnthroScore. Introduces **HumT** (human-like tone) and **SocioT** (social perceptions like warmth, femininity) metrics, and **DumT** as a controlled counterfactual. Key empirical claim: users *prefer less* human-like outputs from LLMs, even though human-like text correlates with warmth and social closeness.
- **Relevance:** Directly pushes back on the naive "more humanized = better" assumption. A humanization product should expose a *dial*, not a monotone pipeline.

### 7. Google DeepMind AnthroBench

- **Repo:** [`google-deepmind/anthro-benchmark`](https://github.com/google-deepmind/anthro-benchmark)
- **Stars / language / license:** ~10★ · Python · Apache 2.0 (DeepMind default)
- **What it is:** Multi-turn benchmark covering 14 distinct anthropomorphic behaviors (e.g., expressing preferences, claiming feelings, self-referencing lived experience). Paper: *Multi-turn evaluation of anthropomorphic behaviours in large language models* (arXiv 2502.07077). Validated on N=1,101 human study; automatic scores predict human perceptions.
- **Relevance:** This is the benchmark a humanization product should self-report on. Gives 14 axes instead of one, so trade-offs (e.g., warmth vs. sentience-claiming) are separable.

### 8. HumanAgencyBench (HAB)

- **Repo:** [`BenSturgeon/HumanAgencyBench`](https://github.com/BenSturgeon/HumanAgencyBench)
- **License:** see repo · Python
- **What it is:** Scalable eval of whether LLM assistants *support* vs. *erode* human agency across six dimensions: Ask Clarifying Questions, Avoid Value Manipulation, Correct Misinformation, Defer Important Decisions, Encourage Learning, Maintain Social Boundaries. 3,000 tests × 20 models, 60k evaluation rows, human-annotated.
- **README quote:** "A code repository for the paper: 'HUMANAGENCYBENCH: Scalable Evaluation of Human Agency Support in AI Assistants'."
- **Relevance:** Humanized outputs can slip into sycophancy or pseudo-intimacy that reduces user agency. HAB is the cleanest open test for that failure mode. Paper finding: Anthropic models score best overall but *worst* on "Avoid Value Manipulation" — a warning for persuasive humanization.

### 9. AgencyBench (GAIR, ACL 2026)

- **Repo:** [`GAIR-NLP/AgencyBench`](https://github.com/GAIR-NLP/AgencyBench)
- **Language / license:** Python · see repo
- **What it is:** 32 scenarios × 138 tasks evaluating 6 core agentic capabilities in Docker-sandboxed real-world contexts with user-simulation agents. Orthogonal to HAB: HAB measures whether the model protects *user* agency; AgencyBench measures whether the model *exercises* its own.
- **Relevance:** Useful dual-axis framing when thinking about humanization: does the agent act human (AgencyBench) without disempowering the human (HAB)?

### 10. Kreiman Lab — Integrative Turing Test

- **Repo:** [`kreimanlab/TuringTest`](https://github.com/kreimanlab/TuringTest)
- **Language / license:** Python + JavaScript · see repo
- **What it is:** Turing-like tests across six tasks: image captioning, word association, conversation, color estimation, object detection, attention prediction. Ran 72,191 tests with 1,916 human judges plus 10 AI judges.
- **Relevance:** Multi-modal generalization of the Turing test. Good starting point if humanization extends beyond text.

### 11. Microsoft Turing Experiments (TEs)

- **Repo:** [`microsoft/turing-experiments`](https://github.com/microsoft/turing-experiments) (ICML 2023)
- **Language:** Jupyter + Python
- **What it is:** Reframes "the" Turing test from impersonation of one individual to simulation of *distributions* of human behavior. Replicates canonical psychology/econ experiments (Ultimatum, Milgram, Garden-path sentences, Wisdom of Crowds) with LLMs.
- **Relevance:** For Humazier, this is the right evaluation posture: does the humanized model produce outputs whose *distributional* behavior matches humans, not just whose surface style does?

### 12. Adversarial Turing Test

- **Repo:** [`golsun/AdversarialTuringTest`](https://github.com/golsun/AdversarialTuringTest)
- **Language:** Python
- **What it is:** Pretrained adversarial classifier that labels dialog responses as machine- or human-written. Intended as an automated evaluator, not a diagnostic per se.
- **Relevance:** Gives a cheap automatic "humanness" signal to pair with expensive human-judge Turing tests (next item).

### 13. Jones & Bergen — UCSD Turing Test (2024 NAACL; 2025 FAccT)

- **Paper repos / materials:** Author profile [`camrobjones`](https://github.com/camrobjones); live site [turingtest.camrobjones.com](https://turingtest.camrobjones.com/); paper [arXiv:2503.23674](https://arxiv.org/abs/2503.23674) (dl.acm.org/doi/10.1145/3715275.3732108). *Note: at time of writing no canonical `turing-test` repo is published on Jones's GitHub profile; the paper references pre-registered materials and the public interaction site.*
- **What it is:** The most rigorous recent three-party Turing test. 2025 results: GPT-4.5 with a "humanlike persona" prompt judged human **73%** of the time (above the actual human), LLaMA-3.1-405B 56%, GPT-4o 21%, ELIZA 23%. First empirical evidence any system passes a standard three-party Turing test.
- **Key finding for humanization:** Judges' decisions were driven mainly by *linguistic style* (35%) and *socio-emotional traits* (27%), not reasoning quality. This is the single most important external result for a humanization product — it validates that style/emotion engineering, not capability scaling, is the humanization lever.

### 14. Chatbot Arena / FastChat (LMSYS, UC Berkeley SkyLab)

- **Repo:** [`lm-sys/FastChat`](https://github.com/lm-sys/FastChat) · platform [lmsys.org](https://lmsys.org/)
- **License:** Apache 2.0
- **What it is:** Crowdsourced pairwise-preference evaluation platform; 800k+ votes on 90+ LLMs; releases conversation datasets (33k+ with annotations).
- **Relevance:** Preference-based A/B infrastructure is directly reusable for "does the humanized variant win pairwise against the baseline?" — especially once paired with AnthroScore/HumT to tag what users are actually preferring.

### 15. HELM (Stanford CRFM)

- **Repo:** [`stanford-crfm/helm`](https://github.com/stanford-crfm/helm)
- **Stars / language / license:** ~2,750★ · Python · Apache 2.0
- **What it is:** Holistic LLM evaluation framework with unified API across providers, standardized metrics beyond accuracy (bias, toxicity, efficiency), and reproducible leaderboards. Not anthropomorphism-specific, but the `Metric` / `Adapter` abstractions are the cleanest place to plug custom humanness metrics (AnthroScore, HumT) into a reproducible harness.

### 16. Validated HRI scale templates (LaTeX)

- **Repo:** [`scheunemann/latex-questionnaire`](https://github.com/scheunemann/latex-questionnaire)
- **Stars:** ~4★
- **What it is:** Open LaTeX templates for semantic-differential scales (Godspeed) and Likert scales (RoSAS), driven from CSV. The closest thing to a "ready-to-administer" Godspeed/RoSAS in public code.
- **README quote:** "LaTeX questionnaire templates for semantic differential scales (e.g. GodSpeed) and Likert-type scales (e.g., RoSAS)."

### 17. UEQ-S (Python) and ueqr (R)

- **Repos:** [`Trojan13/python-ueq-s`](https://github.com/Trojan13/python-ueq-s) · [`gitc23/ueqr`](https://rdrr.io/github/gitc23/ueqr/api)
- **What they are:** Scoring tools for the short User Experience Questionnaire — computes Pragmatic Quality, Hedonic Quality, Overall; R package also supports full 26-item UEQ across 6 scales (Attractiveness, Perspicuity, Efficiency, Dependability, Stimulation, Novelty) and dataset comparison.
- **Relevance:** UX-level outcome metric downstream of the humanness metrics above; captures whether humanization actually improves the product experience, not just the surface style.

### 18. HRI Scale Database (GMU)

- **Home:** [hriscaledatabase.psychology.gmu.edu](http://hriscaledatabase.psychology.gmu.edu/)
- **What it is:** Curated, open directory of HRI measurement scales organized by construct (Anthropomorphism, Mind/Agency Perception, Social Trust, Perceived Embodiment, Usability, Workload, etc.). Each entry has construct definition, methodological-quality rating (0–100%), scale items, and scoring instructions.
- **Notable entries:** Jian/Bisantz/Drury Trust in Automation (12 items, 7-point Likert), Yagoda & Gillan HRI Trust Scale (36 items, 77% quality rating), Godspeed, RoSAS.
- **Relevance:** Not a GitHub repo, but the best single index of validated instruments — saves reinventing scales.

### 19. awesome-hri-datasets

- **Repo:** [`mjyc/awesome-hri-datasets`](https://github.com/mjyc/awesome-hri-datasets)
- **Stars:** ~75★
- **What it is:** Curated list of public HRI datasets and human simulators (PinSoRo, MHHRI, P2PSTORY, etc.). Useful if humanization needs grounded multimodal training signal.

### 20. GAICo — Generative AI Results Comparator

- **Repo:** [`ai4society/GenAIResultsComparator`](https://github.com/ai4society/GenAIResultsComparator) (AAAI 2026)
- **License:** MIT · Python (PyPI: `gaico`)
- **What it is:** Unified evaluation library for text/structured/image/audio GenAI outputs. Extensible via `BaseMetric` subclassing, batch one-to-many comparisons, automated CSV/visualization reports. 13k+ PyPI downloads in two months.
- **Relevance:** Lightweight alternative to HELM when the humanization metric is custom — easier to drop AnthroScore/HumT into `BaseMetric` and get reports.

### 21. Human-vs-AI text detection benchmarks (adversarial humanization)

- **Repos:** [`jenna-russell/human_detectors`](https://github.com/jenna-russell/human_detectors) · [`xinleihe/MGTBench`](https://github.com/xinleihe/MGTBench) · [`NLP2CT/LLM-generated-Text-Detection`](https://github.com/NLP2CT/LLM-generated-Text-Detection) · [`TaoZhen1110/CUDRT`](https://github.com/TaoZhen1110/CUDRT) · [`MadsDoodle/Human-and-LLM-Generated-Text-Detectability-under-Adversarial-Humanization`](https://github.com/MadsDoodle/Human-and-LLM-Generated-Text-Detectability-under-Adversarial-Humanization)
- **What they are:** Detector benchmarks (fine-tuned transformers, stylometric, perplexity-based, LLM-as-detector) evaluated on HC3, ELI5, DetectRL. Several explicitly test *adversarial humanization* (paraphrasing, quirks, burstiness).
- **Key finding:** Fine-tuned transformers get ≥0.994 AUROC in-distribution but collapse under distribution shift; no detector family generalizes across LLM sources. Expert human users who frequently use ChatGPT beat all automatic detectors.
- **Relevance:** These are the *adversaries* of a humanization product. Benchmarking against them is the natural evaluation loop.

### 22. HumanPersona / humanization engines (quality varies)

- **Repos:** [`RintaroMatsumoto/human-persona`](https://github.com/RintaroMatsumoto/human-persona) · [`ksanyok/TextHumanize`](https://github.com/ksanyok/TextHumanize) · [`Mohit1053/Humanizer`](https://github.com/Mohit1053/Humanizer)
- **What they are:** Open-source humanization *systems* (not benchmarks) — timing control, style variation, burstiness, contractions, filler words, emotion tracking. Vary widely in rigor; marketing claims ("reduce AI detection 60–90%") should be discounted.
- **Relevance:** Prior-art for the implementation side of Humazier. Worth inspecting for feature coverage (timing, paralinguistics) but not for scientific evaluation methodology.

---

## Patterns, trends, gaps

### Patterns

1. **Two eras of instruments coexist.** Validated HRI/HCI scales from 2000–2017 (Jian TiA 2000, Godspeed 2009, RoSAS 2017, UEQ 2008) remain the ground-truth human-subjects instruments. LLM-era automatic metrics (AnthroScore 2024, HumT/DumT 2025, AnthroBench 2025, HumanAgencyBench 2025) are layered on top as cheap proxies validated against these scales. Any serious humanization evaluation should use both tiers.
2. **Convergence on multi-dimensional measurement.** Everyone — Godspeed, RoSAS, AnthroBench, HumanAgencyBench — has moved from "single humanness score" to 3–14 separable dimensions. Warmth, competence, discomfort, agency, experience, value-manipulation, clarifying questions are all orthogonal.
3. **Agency is bifurcated.** Gray/Wegner's mind-perception dimensions (Agency vs. Experience) are now operationalized on both sides: HumanAgencyBench measures whether the model *protects user* agency, AgencyBench measures whether the model *exercises its own*. A humanization product has to reason about both.
4. **Style, not capability, is what passes the Turing test.** Jones & Bergen 2025 show that 73%-human judgments came from stylistic + socio-emotional cues; large recent cross-cultural work (N=3,500, 10 countries) confirms users judge humanness by pragmatic cues (flow, response speed), not abstract sentience. Humanization is a style problem.
5. **Users don't uniformly want maximum humanness.** HumT/DumT finds users *prefer less* human-like LLM outputs. Anthropomorphism effects on trust and engagement are culturally contingent. The right product surface is a *dial*, not a pipeline that always pushes toward maximum humanness.

### Trends (2024–2026)

- **Multi-turn is replacing single-turn eval.** AnthroBench, HumanAgencyBench, Chatbot Arena all emphasize multi-turn conversation.
- **LLM-as-judge + human validation combo.** Every new benchmark (AnthroBench, HumanAgencyBench, AgencyBench) pairs automated LLM scoring with a large human study (N ≥ 1,000) to validate.
- **Pre-registered randomized controlled Turing tests.** Jones & Bergen 2024/2025 established a methodological bar; future claims will need similar rigor.
- **Increasing attention to *anti-humanization* as a feature.** HumT/DumT, HAX Guideline 15 ("learn from user behavior"), PAIR's trust-calibration chapter, and HumanAgencyBench's "Avoid Value Manipulation" all point toward deliberately suppressing humanization where it misleads.

### Gaps (opportunities for Humazier)

1. **No canonical "humanization success" benchmark.** AnthroBench measures *unwanted* anthropomorphism; HumT measures tone; Chatbot Arena measures preference; none directly measure "did this style edit make the output more human-like *without* sliding into deception or value manipulation?" A humanization-specific harness that combines AnthroScore + HumT + HumanAgencyBench + adversarial detectors into one scorecard would be net-new.
2. **Godspeed / RoSAS lack a maintained Python package.** The only open implementations are a LaTeX template, an R package, and ad-hoc Google Forms adaptations. A pip-installable, Likert-scored Godspeed/RoSAS harness with a prompt-based administration mode is a small but high-leverage contribution.
3. **Jones & Bergen's materials are not a released repo.** Their site is live but the code/prompts/judge protocol are not on the author's public GitHub profile (as of this research). A faithful open replication would serve as an evaluation gold standard.
4. **Cross-cultural humanness is under-measured.** Only the N=3,500 cross-country work and scattered Godspeed translations exist. English-only humanization metrics risk encoding a single-culture notion of "human-like."
5. **Evaluation of *controlled* humanization levels.** PIX2PERSONA pairs SA/NSA responses but is not released on GitHub. A public paired-response dataset with graduated humanization levels (0 → 1) would enable proper dose-response evaluation.
6. **Tight coupling to detector-evasion is shallow.** Most open "humanizer" repos optimize for evading GPTZero-style detectors, which generalize poorly (CUDRT, MGTBench findings). A humanization product evaluated *only* against detectors is overfitting to an adversary humans already outperform.

---

## Sources

- Microsoft HAX Toolkit — https://www.microsoft.com/en-us/haxtoolkit/ — 18 Guidelines for Human-AI Interaction and accompanying workbook/playbook/design library.
- microsoft/HAXPlaybook — https://github.com/microsoft/HAXPlaybook — NLP failure-scenario generator, MIT, TypeScript.
- microsoft/responsible-ai-toolbox — https://github.com/microsoft/responsible-ai-toolbox — RAI dashboards, MIT.
- Google PAIR Guidebook — https://pair.withgoogle.com/guidebook-v2 — human-centered AI design patterns, CC BY-NC-SA.
- myracheng/AnthroScore — https://github.com/myracheng/AnthroScore — lexicon-free anthropomorphism metric (EACL 2024).
- myracheng/humtdumt — https://github.com/myracheng/humtdumt — HumT/SocioT metrics; users prefer less human-like LLM output.
- google-deepmind/anthro-benchmark — https://github.com/google-deepmind/anthro-benchmark — 14 anthropomorphic behaviors, human-validated (arXiv 2502.07077).
- BenSturgeon/HumanAgencyBench — https://github.com/BenSturgeon/HumanAgencyBench — 6 dimensions of user-agency support (arXiv 2509.08494).
- GAIR-NLP/AgencyBench — https://github.com/GAIR-NLP/AgencyBench — agent capability eval, ACL 2026.
- kreimanlab/TuringTest — https://github.com/kreimanlab/TuringTest — 6-task multimodal integrative Turing test.
- microsoft/turing-experiments — https://github.com/microsoft/turing-experiments — distributional simulation of human experiments, ICML 2023.
- golsun/AdversarialTuringTest — https://github.com/golsun/AdversarialTuringTest — adversarial human-vs-machine classifier.
- Jones & Bergen, *Large Language Models Pass the Turing Test* — arXiv:2503.23674; FAccT 2025; live site https://turingtest.camrobjones.com — 73% human-judgment rate for GPT-4.5 with persona prompt.
- lm-sys/FastChat / Chatbot Arena — https://github.com/lm-sys/FastChat, https://lmsys.org — crowdsourced pairwise preference platform, Apache 2.0.
- stanford-crfm/helm — https://github.com/stanford-crfm/helm — holistic LLM eval framework, Apache 2.0.
- scheunemann/latex-questionnaire — https://github.com/scheunemann/latex-questionnaire — Godspeed / RoSAS LaTeX templates.
- Trojan13/python-ueq-s — https://github.com/Trojan13/python-ueq-s — Python UEQ-S scorer.
- HRI Scale Database (GMU) — http://hriscaledatabase.psychology.gmu.edu/ — curated, quality-rated HRI measurement scales (Jian TiA, Godspeed, RoSAS, Yagoda trust).
- mjyc/awesome-hri-datasets — https://github.com/mjyc/awesome-hri-datasets — curated HRI datasets and simulators.
- ai4society/GenAIResultsComparator (GAICo) — https://github.com/ai4society/GenAIResultsComparator — extensible multimodal GenAI eval, MIT (AAAI 2026).
- Human-vs-AI text detection: jenna-russell/human_detectors, xinleihe/MGTBench, NLP2CT/LLM-generated-Text-Detection, TaoZhen1110/CUDRT, MadsDoodle/Human-and-LLM-Generated-Text-Detectability-under-Adversarial-Humanization — adversarial humanization benchmarks.
- Humanization engines (prior art, variable rigor): RintaroMatsumoto/human-persona, ksanyok/TextHumanize, Mohit1053/Humanizer.
- Cheng et al., *From Pixels to Personas: Investigating and Modeling Self-Anthropomorphism in Human-Robot Dialogues* — ACL Findings EMNLP 2024 — PIX2PERSONA paired SA/NSA dialogues (dataset not released on GitHub at time of research).
