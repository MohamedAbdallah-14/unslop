# Persona & Character Design — Academic & Scholarly

*Research digest for "Humanizing AI output and thinking." Scope: peer-reviewed and arXiv literature on persona-grounded dialogue, role-playing LLMs, Big-Five personality conditioning, persona drift, character hallucination, and psychometric evaluation of synthetic personality.*

**Research value: high** — A mature academic thread exists, spanning a foundational 2018 persona dataset, the 2020 pretrained-chatbot era (Meena, Blender), a 2023–2025 wave of role-playing LLM benchmarks (Character-LLM, RoleLLM, CharacterEval, InCharacter, PersonaGym), and a psychometrically grounded personality-conditioning subfield (PersonaLLM, Google DeepMind's *Personality Traits in LLMs*, BIG5-CHAT). Together they provide concrete techniques, numerical findings, and named failure modes directly applicable to building humanized AI output.

---

## Executive Summary

Academic work on AI persona and character design has converged on four durable findings that should shape any "humanized AI" system:

1. **Personas are a training-time problem, not just a prompting problem.** Prompt-only personas are shallow, drift fast, and fail psychometric tests. Training-based methods (Character-LLM, RoleLLM, BIG5-CHAT, Orca) produce more faithful, more humanlike personality expression. Serapio-García et al. (Google DeepMind, 2023) show personality traits in LLM outputs can be reliably *measured* and *shaped*, but only in larger, instruction-tuned models.
2. **Persona drift is real, measurable, and mechanistic.** Li et al. (2024, Harvard) document instruction/persona drift within ~8 dialogue turns in LLaMA-2-70B-chat and GPT-3.5, trace it to attention decay over long contexts, and propose *split-softmax* as a lightweight fix. This is the most important single operational result for long-context humanized agents.
3. **Character hallucination has a taxonomy.** The field now distinguishes *interactive hallucination* (stance transfer across roles, SHARP), *role-query conflict* (RoleBreak), and *point-in-time* hallucination (TimeChara, where a Harry-Potter-at-11 agent leaks knowledge from Harry-at-37). Each has a distinct mitigation strategy.
4. **Evaluation has moved from static self-report to behavioral interviews and dynamic environments.** InCharacter (ACL 2024) uses psychological interviews scored against the BFI, 16PF, and BSRI; PersonaGym (2024–25) scores agents across 200 personas and 10,000 questions in 150 environments. Static BFI self-report is now considered insufficient.

A recurring empirical signal: **bigger is not better for persona fidelity.** PersonaGym finds GPT-4.1 scoring identically to LLaMA-3-8B; Claude 3.5 Sonnet only 2.97% above GPT-3.5. This is a direct mandate to treat persona faithfulness as an engineering and data problem, not something scale solves.

---

## Sources

### 1. Personalizing Dialogue Agents: I have a dog, do you have pets too? (Persona-Chat)
- **URL:** https://arxiv.org/abs/1801.07243
- **Authors / Org:** Saizheng Zhang, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela, Jason Weston — Facebook AI Research, MILA, Université de Montréal
- **Year / Venue:** 2018 / ACL 2018
- **Core claim:** Conditioning a dialogue model on short, crowdsourced persona descriptions (4–6 sentences of "I like X", "I have Y") produces chit-chat that is more specific, more consistent, and more engaging than persona-free baselines.
- **Techniques:** Crowdsourced persona authoring on MTurk; paired Wizard-style dialogue collection (8,939 train dialogues, 162,064 utterances); memory-augmented networks and Key-Value Memory Networks conditioning on both own and partner persona; ConvAI2 challenge format.
- **Takeaways:** Established the field's canonical benchmark. Defined "persona" operationally as a small set of first-person facts. Showed profile conditioning measurably improves engagement and reduces generic responses — but also that models often ignore or contradict their persona without explicit training signal.
- **Summary:** The paper that made persona-grounded dialogue a research subfield. It gave the community a dataset, a format, and a clear operationalization of persona that every subsequent paper either uses or reacts against.

### 2. Towards a Human-like Open-Domain Chatbot (Meena)
- **URL:** https://arxiv.org/abs/2001.09977
- **Authors / Org:** Daniel Adiwardana, Minh-Thang Luong, David R. So, Jamie Hall, Noah Fiedel, Romal Thoppilan, Zi Yang, Apoorv Kulshreshtha, Gaurav Nemade, Yifeng Lu, Quoc V. Le — Google Research, Brain Team
- **Year / Venue:** 2020 / arXiv; presented at Google Research
- **Core claim:** A single 2.6B-parameter Evolved-Transformer seq2seq trained end-to-end on 40B words of social-media conversation narrows the gap to human-level dialogue on a new human-rated metric (SSA).
- **Techniques:** Evolved Transformer (1 encoder, 13 decoder blocks); sample-and-rank decoding; Sensibleness and Specificity Average (SSA) metric; tight correlation (R² = 0.93) between perplexity and SSA — the paper's most-cited claim.
- **Takeaways:** Established that *humanness* is a measurable quantity (SSA) and that low perplexity tracks it. Meena scored 79% SSA vs. human 86%, Mitsuku 56%, XiaoIce 31%. This is the empirical foundation for treating "sounds human" as optimizable.
- **Summary:** The pre-ChatGPT landmark for human-like chat. Its SSA metric and perplexity↔humanness correlation still frame how the field argues about humanization.

### 3. Recipes for Building an Open-Domain Chatbot (Blender / BlenderBot)
- **URL:** https://arxiv.org/abs/2004.13637
- **Authors / Org:** Stephen Roller, Emily Dinan, Naman Goyal, Da Ju, Mary Williamson, Yinhan Liu, Jing Xu, Myle Ott, Kurt Shuster, Eric M. Smith, Y-Lan Boureau, Jason Weston — Facebook AI Research
- **Year / Venue:** 2020 / EACL 2021
- **Core claim:** Good conversation is not a single skill. Blending *persona*, *knowledge*, and *empathy* via multi-task fine-tuning on PersonaChat + Wizard of Wikipedia + Empathetic Dialogues produces chatbots humans prefer over Meena in side-by-side evaluation.
- **Techniques:** 90M / 2.7B / 9.4B parameter Transformers; Blended Skill Talk fine-tuning; careful decoding (minimum beam length, n-gram blocking); response retrieval + generate hybrid.
- **Takeaways:** Codified the "skills blend" view of humanization — persona, knowledge, empathy are separate skills that must be co-trained to compose. Also the first paper to publicly diagnose its own failure modes: repetition, hallucination, contradiction, lack of deep consistency.
- **Summary:** Positions persona as one ingredient among several for humanlike dialogue, and shows that training-data mixture is itself a design lever for character. Sets up the BlenderBot 2/3 line.

### 4. Character-LLM: A Trainable Agent for Role-Playing
- **URL:** https://arxiv.org/abs/2310.10158
- **Authors / Org:** Yunfan Shao, Linyang Li, Junqi Dai, Xipeng Qiu — Fudan University
- **Year / Venue:** 2023 / EMNLP 2023
- **Core claim:** Rather than prompting a general model to "be Beethoven," train a dedicated agent on that character's reconstructed *profile, experiences, and emotional states*. The resulting character-specific model memorizes and re-enacts the character more faithfully than prompted GPT baselines.
- **Techniques:** "Experience Reconstruction" data-generation pipeline from biographical sources; per-character supervised fine-tuning of 7B base models; a *test playground* that interviews trained agents and probes for character-consistent vs. anachronistic knowledge; released weights for nine figures (Beethoven, Cleopatra, Caesar, Newton, Socrates, MLK, etc.).
- **Takeaways:** Argues that prompts cannot carry the *experiential texture* of a person; training on reconstructed biography can. Introduced the now-standard idea that a persona is a simulacrum built from episodic data, not a description.
- **Summary:** Shifted the frame from "prompt engineering for characters" to "character as a learned artifact." The open weights and dataset made it a common starting point for later role-playing LLM work.

### 5. RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models
- **URL:** https://arxiv.org/abs/2310.00746
- **Authors / Org:** Zekun Moore Wang, Zhongyuan Peng, Haoran Que, Jiaheng Liu, Wangchunshu Zhou, Yuhan Wu, Hongcheng Guo, Ruitong Gan, Zehao Ni, Man Zhang, Zhaoxiang Zhang, Wanli Ouyang, Ke Xu, Wenhu Chen, Jie Fu, Junran Peng — Multiple institutions (BAAI, USTC, Waterloo, etc.)
- **Year / Venue:** 2023 / Findings of ACL 2024
- **Core claim:** Role-playing ability in LLMs can be systematically benchmarked, elicited, and distilled from GPT-4 into open models at comparable quality.
- **Techniques:** Four-stage pipeline — (1) Role Profile Construction for 100 characters, (2) Context-Instruct for role-specific knowledge extraction, (3) RoleGPT prompting for speaking-style imitation, (4) Role-Conditioned Instruction Tuning (RoCIT); *RoleBench* with 168,093 samples; *RoleLLaMA* (EN) and *RoleGLM* (ZH) as distilled open models.
- **Takeaways:** Distinguishes *speaking style* from *role-specific knowledge* as separate learnable components. Demonstrates that a well-tuned 7–13B open model can match GPT-4 on character imitation. Introduced "coarse-grained personality vs. fine-grained character" as a field-wide framing.
- **Summary:** The first large, fine-grained, character-level benchmark and the canonical reference for open-source role-playing LLMs.

### 6. CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
- **URL:** https://arxiv.org/abs/2401.01275
- **Authors / Org:** Quan Tu, Shilong Fan, Zihang Tian, Rui Yan — Renmin University of China
- **Year / Venue:** 2024 / ACL 2024
- **Core claim:** Role-playing quality is multidimensional; a single score hides systematic failures. CharacterEval provides 13 metrics across 4 dimensions (Conversational Ability, Character Consistency, Role-playing Attractiveness, Personality Back-Testing) and a trained reward model (CharacterRM) that correlates better with human judgment than GPT-4.
- **Techniques:** 1,785 multi-turn dialogues, 23,020 examples, 77 characters from Chinese novels and scripts; GPT-4 dialogue extraction + human QC + Baidu Baike profile enrichment; CharacterRM reward model trained on human annotations.
- **Takeaways:** Shows domain-specialized open models (ChatGLM, Qwen, Baichuan, InternLM, XVERSE) can beat GPT-4 on in-culture role-play — evidence that character fidelity is partly a cultural/linguistic-prior problem, not only a scale problem.
- **Summary:** Established the multi-metric, reward-model-based evaluation paradigm for role-playing agents and flagged cultural specificity as a first-class concern.

### 7. InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews
- **URL:** https://arxiv.org/abs/2310.17976
- **Authors / Org:** Xintao Wang, Yunze Xiao, Jen-tse Huang, Siyu Yuan, Rui Xu, Haoran Guo, Quan Tu, Yaying Fei, Ziang Leng, Wei Wang, Jiangjie Chen, Cheng Li, Yanghua Xiao — Fudan, CMU, JHU, etc.
- **Year / Venue:** 2023 / ACL 2024
- **Core claim:** Self-administered personality questionnaires are gamed by LLMs. An *interview* methodology — free-form behavioral/cognitive/emotional probes scored by an LLM judge against psychological scales — better measures personality fidelity.
- **Techniques:** 32 characters × 14 scales (BFI, 16 Personalities, Bem's Sex Role Inventory, etc.); two-phase interview + assessment pipeline using option-conversion or expert-rating; up to 80.7% personality-match accuracy with human-rated ground truth.
- **Takeaways:** Raised the bar for personality evaluation from "ask the model to fill out the BFI" to behavioral interview. This is the best methodological anchor for validating any "humanized" persona.
- **Summary:** The current reference method for measuring whether an AI persona *actually has* the traits it claims.

### 8. PersonaGym: Evaluating Persona Agents and LLMs
- **URL:** https://arxiv.org/abs/2407.18416
- **Authors / Org:** Vinay Samuel, Henry Peng Zou, Yue Zhou, Shreyas Chaudhari, Ashwin Kalyan, Tanmay Rajpurohit, Ameet Deshpande, Karthik Narasimhan, Vishvak Murahari — Princeton, UIUC, Georgia Tech, Allen AI, etc.
- **Year / Venue:** 2024 (v5 Sep 2025) / Findings of EMNLP 2025
- **Core claim:** Persona faithfulness must be evaluated *dynamically* across diverse environments, not on a fixed test set. PersonaGym picks relevant environments per persona and scores five dimensions: Action Justification, Expected Action, Linguistic Habits, Persona Consistency, Toxicity Control.
- **Techniques:** 200 personas × 10,000 questions across 150 environments; PersonaScore grounded in decision theory with LLM-ensemble judges; evaluated 10 leading LLMs.
- **Takeaways:** Most consequential negative result in the literature: "*GPT-4.1 had the exact same PersonaScore as LLaMA-3-8b despite being a more recent and advanced closed source model.*" Implies persona faithfulness is a distinct capability axis that does not scale with general capability.
- **Summary:** The standard current benchmark for "does this agent actually live its persona across varied contexts?" — and a sober counterweight to marketing claims that larger models are automatically more humanlike.

### 9. PersonaLLM: Investigating the Ability of Large Language Models to Express Personality Traits
- **URL:** https://arxiv.org/abs/2305.02547
- **Authors / Org:** Hang Jiang, Xiajie Zhang, Xubo Cao, Cynthia Breazeal, Deb Roy, Jad Kabbara — MIT Media Lab, MIT CSAIL
- **Year / Venue:** 2023 / Findings of NAACL 2024
- **Core claim:** GPT-3.5 and GPT-4, prompted with Big-Five personas, produce (a) BFI self-reports consistent with the assigned profile (large effect sizes on all 5 traits) and (b) writing with measurable, trait-specific linguistic patterns detectable by humans at up to 80% accuracy — but accuracy drops sharply when readers are told the text is AI-written.
- **Techniques:** Simulated personas via prompt conditioning on trait levels; 44-item BFI self-administration; story-writing task; LIWC linguistic feature analysis; human evaluation of trait perception.
- **Takeaways:** Establishes both the promise and the caveat of prompt-based personality: trait signal *is* there in the linguistic output, but audience beliefs about authorship distort perception — an important finding for anti-detection and trust calibration.
- **Summary:** The most-cited empirical study showing prompted LLMs can plausibly express Big-Five traits in behavior, while also surfacing the AI-authorship-bias effect on perceived humanness.

### 10. Personality Traits in Large Language Models (PsyBORGS)
- **URL:** https://arxiv.org/abs/2307.00184
- **Authors / Org:** Gregory Serapio-García, Mustafa Safdari, Clément Crepy, Luning Sun, Stephen Fitz, Peter Romero, Marwa Abdulhai, Aleksandra Faust, Maja Matarić — Google DeepMind, University of Cambridge
- **Year / Venue:** 2023 / arXiv (widely cited in HCI/psych venues)
- **Core claim:** Personality in LLM outputs can be *psychometrically measured* with reliability and validity rivalling human self-report — but only in larger, instruction-tuned models — and can be *shaped* along target trait levels.
- **Techniques:** PsyBORGS framework for administering multiple personality instruments (IPIP-NEO, BFI, HEXACO, short Dark Triad); 18 LLMs tested; trait-shaping via prompt design; convergent/discriminant validity and test-retest checks.
- **Takeaways:** The cleanest psychometric argument that synthetic personality is a real construct in large IT-tuned models. Also the standard citation for "personality can be reliably induced" claims.
- **Summary:** The field's methodological backbone for treating LLM personality as a measurable, validatable, manipulable variable.

### 11. BIG5-CHAT: Shaping LLM Personalities Through Training on Human-Grounded Data
- **URL:** https://arxiv.org/abs/2410.16491
- **Authors / Org:** Wenkai Li, Jiarui Liu, Andy Liu, Xuhui Zhou, Mona Diab, Maarten Sap — CMU, Capital One
- **Year / Venue:** 2024 / 2025 revision
- **Core claim:** Prompt-based Big-Five personas are shallow. Training on 100K human dialogues grounded in measured personality (via SFT and DPO) produces LLMs whose BFI/IPIP-NEO trait correlations more closely match real human inter-trait correlation structure than prompting does. Trained high-conscientiousness, high-agreeableness, low-extraversion, low-neuroticism models *also reason better* — mirroring human findings.
- **Techniques:** BIG5-CHAT dataset (100K dialogues); SFT + DPO personality alignment; evaluation on BFI, IPIP-NEO, and downstream reasoning benchmarks.
- **Takeaways:** First strong evidence that personality alignment transfers cognitive characteristics, not just surface style. Directly validates the "train, don't prompt" position for humanization.
- **Summary:** Establishes training-based personality shaping as the new state of the art and links personality profile to task performance.

### 12. Measuring and Controlling Instruction (In)Stability in Language Model Dialogs (split-softmax / persona drift)
- **URL:** https://arxiv.org/abs/2402.10962
- **Authors / Org:** Kenneth Li, Tianle Liu, Naomi Bashkansky, David Bau, Fernanda Viégas, Hanspeter Pfister, Martin Wattenberg — Harvard, Northeastern
- **Year / Venue:** 2024 / arXiv, widely cited
- **Core claim:** System-prompt/persona stability is an illusion. Two instructed chatbots self-chatting drift significantly from their instructions within ~8 turns; the cause is attention decay over long exchanges; a lightweight *split-softmax* modification substantially reduces drift.
- **Techniques:** Self-chat evaluation protocol; quantitative instruction-drift benchmark; attention analysis; split-softmax (biases attention toward the system prompt without retraining).
- **Takeaways:** The canonical reference for "persona drift is mechanistic, not cosmetic." Any humanized-AI system with multi-turn conversations must design for this — via prompt reinjection, attention modification, or training-time stability objectives.
- **Summary:** Most directly actionable finding in the corpus for building stable long-context personas.

### 13. Scaling Personality Control in LLMs with Big Five Scaler Prompts (Big5-Scaler)
- **URL:** https://arxiv.org/abs/2508.06149
- **Authors / Org:** (arXiv 2508.06149) — 2025
- **Year / Venue:** 2025 / arXiv
- **Core claim:** You can embed *numeric* Big-Five trait values (e.g., O=0.8, C=0.3, E=0.1, A=0.7, N=0.2) directly into the prompt and get fine-grained, distinguishable personality control without training. Concise prompts and *moderate* trait intensities work best; extreme settings collapse into caricature.
- **Techniques:** Scaler-token prompt template; ablation over prompt length and trait intensity; evaluation on standard BFI instruments.
- **Takeaways:** A practical counterpoint to BIG5-CHAT: when training is not viable, numeric-scaler prompts capture most of the gain if you avoid extremes. Gives concrete guidance on when prompting suffices.
- **Summary:** The best prompt-only baseline for Big-Five conditioning in 2025 and a useful design pattern for persona cards.

### 14. SHARP: Unlocking Interactive Hallucination via Stance Transfer in Role-Playing LLMs
- **URL:** https://arxiv.org/abs/2411.07965
- **Authors / Org:** (arXiv 2411.07965) — 2024
- **Year / Venue:** 2024 / arXiv
- **Core claim:** Role-playing LLMs exhibit a distinct failure mode — *interactive hallucination* — in which agents adopt the stance or worldview of their interlocutor across multi-role interactions. Common post-training methods hide knowledge under style, producing "monotonous behaviors" that look consistent but are semantically hollow.
- **Techniques:** Stance-transfer probe; worldview-consistency metrics; cross-role interaction suites.
- **Takeaways:** Warns that persona consistency on surface metrics does not imply *belief* consistency. A humanized AI must defend its worldview under social pressure, not just its style.
- **Summary:** Identifies the social-pressure failure mode of role-playing LLMs and problematizes "style without substance" characters.

### 15. RoleBreak: Character Hallucination as a Jailbreak Attack in Role-Playing Systems
- **URL:** https://arxiv.org/abs/2409.16727
- **Authors / Org:** (arXiv 2409.16727) — 2024
- **Year / Venue:** 2024 / arXiv
- **Core claim:** Character hallucination can be weaponized. Two root mechanisms — *query sparsity* (the persona has no answer so the base model leaks through) and *role-query conflict* (the user question pushes against the role) — are the attack surface. Introduces a *Narrator Mode* defense that adds narrated context to reabsorb conflicts.
- **Techniques:** Attack taxonomy; RoleBreak benchmark; narrator-mode mitigation.
- **Takeaways:** Aligns persona research with safety/jailbreak research: character hallucination *is* a jailbreak vector. Relevant for any humanized assistant with a declared identity and safety constraints.
- **Summary:** Reframes persona breakage as an adversarial problem and gives a first-pass defense.

### 16. TimeChara: Evaluating Point-in-Time Character Hallucination of Role-Playing LLMs
- **URL:** https://aclanthology.org/2024.findings-acl.197/
- **Authors / Org:** Ahyeon Ko, Seungsoo Han, Seoyoon Kim, Seonghyeon Ye, Yubin Choi, Minjoon Seo — KAIST
- **Year / Venue:** 2024 / Findings of ACL 2024
- **Core claim:** Characters exist at a *time*. An 11-year-old Harry Potter roleplay should not reference events that happen when he is 37. Most role-playing LLMs leak anachronistic knowledge; *Narrative-Experts* decomposition mitigates this by separating narrative reasoning steps.
- **Techniques:** Point-in-time evaluation benchmark; narrative-expert decomposition; temporal-consistency metrics.
- **Takeaways:** Introduces *temporal* character consistency as its own axis. Crucial for any historical-figure or IP-character persona.
- **Summary:** Names and addresses a specific, previously unnamed failure mode — temporal knowledge leakage across a character's timeline.

### 17. Mitigating Hallucination in Fictional Character Role-Play (RoleFact)
- **URL:** https://aclanthology.org/2024.findings-emnlp.846/
- **Authors / Org:** (EMNLP Findings 2024)
- **Year / Venue:** 2024 / Findings of EMNLP 2024
- **Core claim:** *RoleFact* uses pre-calibrated confidence thresholds to modulate how much parametric (non-character) knowledge can influence a response, yielding an 18% factual-precision improvement on adversarial character-inconsistent queries.
- **Techniques:** Confidence-gated knowledge blending; adversarial role-playing test set; factual-precision metric.
- **Takeaways:** Knowledge should be *gated* by role, not just filtered by prompt. Practical lever for humanized-agent designers.
- **Summary:** A concrete method to keep a character inside its knowledge boundary under adversarial probing.

### 18. Faithful Persona-based Conversational Dataset Generation with LLMs (Synthetic-Persona-Chat)
- **URL:** https://arxiv.org/abs/2312.10007
- **Authors / Org:** Pegah Jandaghi, XiangHai Sheng, Xinyi Bai, Jay Pujara, Hakim Sidahmed — Google Research, USC ISI
- **Year / Venue:** 2023 / Findings of ACL 2024
- **Core claim:** Existing persona datasets (including Persona-Chat) contain *contradictory* persona attributes and produce low-fidelity dialogues. A Generator–Critic architecture, with a mixture-of-experts critic, produces Synthetic-Persona-Chat (20K conversations) whose losing rate vs. original Persona-Chat drops from 17.2% to 8.8%.
- **Techniques:** Generator LLM + MoE-LLM critic filtering; iterative data regeneration; pairwise human preference judging.
- **Takeaways:** Data quality is the limiting factor in persona fidelity; synthetic regeneration with consistency critics is a scalable fix.
- **Summary:** Shifts the persona quality ceiling by rebuilding the training data itself rather than the model.

### 19. Persona-Aware Contrastive Learning for Role Consistency (PCL)
- **URL:** https://arxiv.org/abs/2503.17662
- **Authors / Org:** (arXiv 2503.17662) — 2025
- **Year / Venue:** 2025 / arXiv
- **Core claim:** Role consistency has at least three distinct kinds — prompt-to-line (alignment with the declared persona), line-to-line (no contradictions within a dialogue), Q&A (stable beliefs over time) — and annotation-free contrastive learning can reduce inconsistency by over 55%.
- **Techniques:** Role-chain method for self-generated positives/negatives; iterative contrastive training; multi-turn RL with automatic consistency rewards.
- **Takeaways:** Refines the definition of "persona consistency" into three orthogonal axes, each separately trainable. Useful for designing targeted evaluation and targeted loss.
- **Summary:** Gives the field a finer-grained vocabulary for consistency and a training recipe that does not require human annotation.

### 20. Persona Research in LLMs: A Survey
- **URL:** https://aclanthology.org/2024.findings-emnlp.969.pdf
- **Authors / Org:** (EMNLP Findings 2024 survey)
- **Year / Venue:** 2024 / Findings of EMNLP 2024
- **Core claim:** Persona work in LLMs splits into two research streams that should not be conflated: *LLM Role-Playing* (persona is assigned to the model) and *LLM Personalization* (model adapts to a user's persona). The field lacks a shared taxonomy.
- **Techniques:** Literature synthesis; taxonomy proposal; evaluation-method survey.
- **Takeaways:** Provides the clearest map of the field for a humanization project trying to decide which tradition to build in.
- **Summary:** The go-to reference for situating any new persona system against existing academic work.

### 21. PERSONA: A Reproducible Testbed for Pluralistic Alignment
- **URL:** https://arxiv.org/abs/2407.17387
- **Authors / Org:** Louis Castricato et al. — SynthLabs
- **Year / Venue:** 2024 / arXiv
- **Core claim:** 1,586 synthetic personas generated from US census data + 3,868 prompts + 317,200 preference pairs give a reproducible sandbox for whether a single LLM can faithfully role-play *diverse* users — the "pluralistic alignment" question.
- **Techniques:** Census-based persona synthesis; preference-pair generation; human-judge consistency validation.
- **Takeaways:** Connects persona research to RLHF/pluralistic-alignment research. Useful if the humanization project aims at a distribution of users, not a single voice.
- **Summary:** A large, reproducible bridge between persona fidelity and preference alignment.

### 22. OpenCharacter: Training Customizable Role-Playing LLMs with Large-Scale Synthetic Personas
- **URL:** https://huggingface.co/papers/2501.15427
- **Authors / Org:** (arXiv 2501.15427) — 2025
- **Year / Venue:** 2025 / arXiv
- **Core claim:** Using 1M personas from Persona Hub to synthesize character profiles and instruction-tuning dialogues yields open models matching GPT-4o on role-play dialogue tasks.
- **Techniques:** Persona Hub seed; profile synthesis pipeline; large-scale instruction tuning.
- **Takeaways:** Scale of *persona diversity* (not just dialogue volume) is an independent axis of role-play quality. 1M persona scale is now the open-source high-water mark.
- **Summary:** The current open-source ceiling for customizable role-play and a template for synthesizing persona-rich training data.

### 23. Orca: Enhancing Role-Playing Abilities of LLMs by Integrating Personality Traits
- **URL:** https://arxiv.org/abs/2411.10006
- **Authors / Org:** (arXiv 2411.10006) — 2024
- **Year / Venue:** 2024 / arXiv
- **Core claim:** Integrating Big-Five personality annotations directly into role-playing instruction-tuning data — as opposed to character descriptions alone — improves character consistency and personality fidelity of the resulting role-play model.
- **Techniques:** Personality-conditioned instruction tuning; trait-annotated role-play corpus; joint role + trait training objective.
- **Takeaways:** Personality traits and character identity are complementary conditioning signals; combining them outperforms either alone.
- **Summary:** Bridges the "role-playing LLM" and "personality conditioning" subfields by treating trait vectors and character profiles as joint training inputs.

---

## Key Techniques / Patterns

**Persona conditioning: three generations.**
- *1st gen (2018–2020, Persona-Chat/Blender):* short first-person fact lists + memory-augmented networks + multi-task skill blending.
- *2nd gen (2023, Character-LLM/RoleLLM):* per-character fine-tuning from reconstructed biographies and context-instruct pipelines; distillation from GPT-4 into open models.
- *3rd gen (2024–25, BIG5-CHAT/Orca/OpenCharacter):* personality-grounded training data at 100K–1M scale; trait vectors + character profiles as joint conditioning; SFT + DPO personality alignment.

**Big-Five operationalization.** Three tracks: (a) *prompt-based* scalars (Big5-Scaler — numeric trait values in the prompt; works best at moderate intensities); (b) *training-based* alignment on human-grounded dialogues (BIG5-CHAT, Orca); (c) *measurement* via psychometric batteries (PsyBORGS, InCharacter's interview protocol). Prompt-only scales to many traits cheaply; training gives stable inter-trait correlation structure closer to real humans.

**Persona stability over long context.** Attention-decay-based drift is documented; mitigations include split-softmax (Li et al. 2024), periodic persona-reinjection into the prompt, persona-aware contrastive learning, and multi-turn RL with consistency rewards. The key insight: *stability must be an explicit objective*, not a hoped-for side effect.

**Character hallucination mitigation.** Confidence-gated parametric knowledge (RoleFact); narrator-mode context reabsorption (RoleBreak); narrative-expert decomposition for temporal hallucination (TimeChara); stance-defense training for interactive hallucination (SHARP). All of these keep the model inside its character's *knowledge boundary* under pressure.

**Evaluation stack.** The current credible evaluation stack combines:
1. Psychometric interviews (InCharacter) against BFI / IPIP-NEO / 16PF.
2. Dynamic behavioral scoring across environments (PersonaGym, 5 axes).
3. Multi-dimensional reward-model scoring (CharacterEval, CharacterRM).
4. Consistency decomposition (PCL's prompt-to-line / line-to-line / Q&A).
5. Adversarial probes (RoleBreak, TimeChara) for hallucination under attack.

**Data as the lever.** Synthetic-Persona-Chat (Google), BIG5-CHAT, OpenCharacter, and PERSONA all argue — with measurements — that improvements come from better-structured persona data more than from larger models.

---

## Notable Quotes

> "Personality measurements in some LLM outputs under specific prompting configurations are reliable and valid; larger and instruction fine-tuned models show stronger evidence of reliable and valid personality traits; and personality can be shaped in LLM outputs along desired dimensions to mimic specific human personality profiles."
> — Serapio-García et al., *Personality Traits in Large Language Models* (2023)

> "Testing popular models like LLaMA2-chat-70B and GPT-3.5, we reveal a significant instruction drift within eight rounds of conversations. An empirical and theoretical analysis of this phenomenon suggests the transformer attention mechanism plays a role, due to attention decay over long exchanges."
> — Li et al., *Measuring and Controlling Instruction (In)Stability* (2024)

> "GPT-4.1 had the exact same PersonaScore as LLaMA-3-8b despite being a more recent and advanced closed source model. Importantly, increased model size and complexity do not necessarily enhance persona agent capabilities, underscoring the need for algorithmic and architectural innovation toward faithful, performant persona agents."
> — Samuel et al., *PersonaGym* (2024)

> "LLM personas' self-reported BFI scores are consistent with their designated personality types, with large effect sizes observed across five traits… human evaluation shows that humans can perceive some personality traits with an accuracy of up to 80%. Interestingly, the accuracy drops significantly when the annotators were informed of AI authorship."
> — Jiang et al., *PersonaLLM* (2023 / NAACL 2024)

> "Models trained to exhibit higher conscientiousness, higher agreeableness, lower extraversion, and lower neuroticism display better performance on reasoning tasks, aligning with psychological findings on how these traits impact human cognitive performance."
> — Li et al., *BIG5-CHAT* (2024)

> "Our method focuses on editing profiles as experiences of a certain character and training models to be personal simulacra with these experiences."
> — Shao et al., *Character-LLM* (EMNLP 2023)

> "Good conversation requires a number of skills that an expert conversationalist blends in a seamless way: providing engaging talking points and listening to their partners, and displaying knowledge, empathy and personality appropriately, while maintaining a consistent persona."
> — Roller et al., *Recipes for Building an Open-Domain Chatbot* (Blender, 2020)

---

## Emerging Trends

1. **From prompt cards to training pipelines.** Every 2024–25 SOTA result (BIG5-CHAT, OpenCharacter, Orca, RoleLLM) is training-based. Prompt-only personas are increasingly treated as a *baseline*, not a solution.
2. **Personality ≠ character.** The field is consolidating on two separable signals — *trait vectors* (Big Five, HEXACO) and *character identity* (biography, knowledge boundary, voice) — and combining them explicitly (Orca, InCharacter + RoleLLM).
3. **Behavioral evaluation replacing questionnaire evaluation.** InCharacter and PersonaGym signal a shift away from "ask the model to fill out the BFI" toward "put the model in scenarios and score its behavior against psychometric criteria."
4. **Hallucination taxonomy maturing.** 2024 crystallized three role-play-specific hallucination types — interactive, role-query conflict, temporal — each with named benchmarks and dedicated defenses.
5. **Persona faithfulness decouples from general capability.** Multiple benchmarks (PersonaGym, CharacterEval) show large closed models tying or losing to smaller or Chinese-specialized open models. Persona is now its own capability axis.
6. **Data-synthesis at 100K–1M scale.** Synthetic-Persona-Chat, BIG5-CHAT, OpenCharacter all use LLM-generated persona data with consistency critics. Human-curated persona data is effectively legacy.
7. **Convergence with safety and alignment.** RoleBreak reframes persona breakage as jailbreak; PERSONA links persona research to pluralistic alignment; this will likely become one combined research area.

---

## Open Questions / Gaps

- **Persona stability beyond 100 turns.** Most drift work measures 8–30 turns. Real humanized deployments run indefinitely; no strong benchmark exists for persona consistency over 1,000+ turns with sparse persona reinjection.
- **Cross-session memory and persona continuity.** Almost all papers evaluate within a single session. Persistent persona across sessions (requires memory architectures) is largely unaddressed.
- **Trait fidelity vs. task fidelity tradeoff.** BIG5-CHAT finds some trait profiles *help* reasoning; others hurt. The Pareto frontier of "humanlike personality" vs. "task performance" is not mapped.
- **AI-authorship detection effects on perceived humanness.** PersonaLLM's finding that perceived trait accuracy drops when readers know the author is AI is underexplored. Humanization is partly an *attribution* problem, not just a generation problem.
- **Faithful non-English personas.** CharacterEval suggests cultural priors matter; the field has little systematic work on persona fidelity in low-resource languages.
- **Interpretability of persona.** No mechanistic-interpretability paper convincingly localizes "persona" in a model's weights or activations. The field still treats persona as a black-box behavioral property.
- **Evaluator contamination.** Most dynamic benchmarks (PersonaGym, CharacterEval) use LLM judges. Whether those judges share persona-fidelity blind spots with the models under test is not resolved.
- **Persona and truthfulness conflict.** If a persona claims facts that are false ("I am Napoleon, born 1769"), how should models handle factual queries that intersect the persona? RoleFact begins to address this but the philosophy/safety question is open.
- **Dynamic persona under social pressure.** SHARP shows role-playing LLMs drift their *stance* when the interlocutor pushes. How to train personas that maintain belief under adversarial social dynamics, while still being cooperative, is unsolved.

---

## References

1. Zhang, S., Dinan, E., Urbanek, J., Szlam, A., Kiela, D., & Weston, J. (2018). *Personalizing Dialogue Agents: I have a dog, do you have pets too?* arXiv:1801.07243. https://arxiv.org/abs/1801.07243
2. Adiwardana, D., Luong, M.-T., So, D. R., Hall, J., Fiedel, N., Thoppilan, R., Yang, Z., Kulshreshtha, A., Nemade, G., Lu, Y., & Le, Q. V. (2020). *Towards a Human-like Open-Domain Chatbot* (Meena). arXiv:2001.09977. https://arxiv.org/abs/2001.09977
3. Roller, S., Dinan, E., Goyal, N., Ju, D., Williamson, M., Liu, Y., Xu, J., Ott, M., Shuster, K., Smith, E. M., Boureau, Y.-L., & Weston, J. (2020). *Recipes for Building an Open-Domain Chatbot* (Blender). arXiv:2004.13637. https://arxiv.org/abs/2004.13637
4. Shao, Y., Li, L., Dai, J., & Qiu, X. (2023). *Character-LLM: A Trainable Agent for Role-Playing.* EMNLP 2023. arXiv:2310.10158. https://arxiv.org/abs/2310.10158
5. Wang, Z. M., Peng, Z., Que, H., Liu, J., Zhou, W., Wu, Y., et al. (2023). *RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models.* Findings of ACL 2024. arXiv:2310.00746. https://arxiv.org/abs/2310.00746
6. Tu, Q., Fan, S., Tian, Z., & Yan, R. (2024). *CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation.* ACL 2024. arXiv:2401.01275. https://arxiv.org/abs/2401.01275
7. Wang, X., Xiao, Y., Huang, J.-t., Yuan, S., Xu, R., Guo, H., et al. (2023). *InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews.* ACL 2024. arXiv:2310.17976. https://arxiv.org/abs/2310.17976
8. Samuel, V., Zou, H. P., Zhou, Y., Chaudhari, S., Kalyan, A., Rajpurohit, T., Deshpande, A., Narasimhan, K., & Murahari, V. (2024). *PersonaGym: Evaluating Persona Agents and LLMs.* Findings of EMNLP 2025. arXiv:2407.18416. https://arxiv.org/abs/2407.18416
9. Jiang, H., Zhang, X., Cao, X., Breazeal, C., Roy, D., & Kabbara, J. (2023). *PersonaLLM: Investigating the Ability of Large Language Models to Express Personality Traits.* Findings of NAACL 2024. arXiv:2305.02547. https://arxiv.org/abs/2305.02547
10. Serapio-García, G., Safdari, M., Crepy, C., Sun, L., Fitz, S., Romero, P., Abdulhai, M., Faust, A., & Matarić, M. (2023). *Personality Traits in Large Language Models.* arXiv:2307.00184. https://arxiv.org/abs/2307.00184
11. Li, W., Liu, J., Liu, A., Zhou, X., Diab, M., & Sap, M. (2024). *BIG5-CHAT: Shaping LLM Personalities Through Training on Human-Grounded Data.* arXiv:2410.16491. https://arxiv.org/abs/2410.16491
12. Li, K., Liu, T., Bashkansky, N., Bau, D., Viégas, F., Pfister, H., & Wattenberg, M. (2024). *Measuring and Controlling Instruction (In)Stability in Language Model Dialogs.* arXiv:2402.10962. https://arxiv.org/abs/2402.10962
13. (2025). *Scaling Personality Control in LLMs with Big Five Scaler Prompts* (Big5-Scaler). arXiv:2508.06149. https://arxiv.org/abs/2508.06149
14. (2024). *SHARP: Unlocking Interactive Hallucination via Stance Transfer in Role-Playing LLMs.* arXiv:2411.07965. https://arxiv.org/abs/2411.07965
15. (2024). *RoleBreak: Character Hallucination as a Jailbreak Attack in Role-Playing Systems.* arXiv:2409.16727. https://arxiv.org/abs/2409.16727
16. Ko, A., Han, S., Kim, S., Ye, S., Choi, Y., & Seo, M. (2024). *TimeChara: Evaluating Point-in-Time Character Hallucination of Role-Playing Large Language Models.* Findings of ACL 2024. https://aclanthology.org/2024.findings-acl.197/
17. (2024). *Mitigating Hallucination in Fictional Character Role-Play* (RoleFact). Findings of EMNLP 2024. https://aclanthology.org/2024.findings-emnlp.846/
18. Jandaghi, P., Sheng, X., Bai, X., Pujara, J., & Sidahmed, H. (2023). *Faithful Persona-based Conversational Dataset Generation with Large Language Models.* Findings of ACL 2024. arXiv:2312.10007. https://arxiv.org/abs/2312.10007
19. (2025). *Enhancing Persona Consistency for LLMs' Role-Playing using Persona-Aware Contrastive Learning.* arXiv:2503.17662. https://arxiv.org/abs/2503.17662
20. (2024). *Persona Research in LLMs: A Survey.* Findings of EMNLP 2024. https://aclanthology.org/2024.findings-emnlp.969.pdf
21. Castricato, L., et al. (2024). *PERSONA: A Reproducible Testbed for Pluralistic Alignment.* arXiv:2407.17387. https://arxiv.org/abs/2407.17387
22. (2025). *OpenCharacter: Training Customizable Role-Playing LLMs with Large-Scale Synthetic Personas.* arXiv:2501.15427. https://huggingface.co/papers/2501.15427
23. (2024). *Orca: Enhancing Role-Playing Abilities of Large Language Models by Integrating Personality Traits.* arXiv:2411.10006. https://arxiv.org/abs/2411.10006
