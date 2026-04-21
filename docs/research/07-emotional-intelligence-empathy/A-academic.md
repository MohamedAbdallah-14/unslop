# Category 07 — Emotional Intelligence & Empathy in AI

## Angle A — Academic & Scholarly

**Scope:** Peer-reviewed / arXiv work on empathetic dialogue generation, emotion recognition in text, empathy evaluation frameworks, affective computing, and mental-health LLMs. Venues targeted: ACL, EMNLP, NAACL/Findings, AAAI, CHI, *Nature Machine Intelligence*, JAMA Internal Medicine, JMIR, and arXiv.

**Research value: high** — The field has matured from emotion-conditioned seq2seq (2018–2019) through knowledge-/cognition-augmented transformers (2020–2022) to LLM-aligned empathy (2023–2025), with well-established benchmarks and a small but growing body of field-deployed / clinically-evaluated systems.

---

## 1. Foundational Benchmarks & Datasets

### 1.1 EmpatheticDialogues (Rashkin et al., ACL 2019)

- **Citation:** Rashkin, H., Smith, E. M., Li, M., & Boureau, Y.-L. (2019). *Towards Empathetic Open-domain Conversation Models: A New Benchmark and Dataset.* ACL 2019. [arXiv:1811.00207](https://arxiv.org/abs/1811.00207) · [ACL Anthology P19-1534](https://aclanthology.org/P19-1534/) · Code: `facebookresearch/EmpatheticDialogues`.
- **Contribution:** 25k crowdsourced multi-turn dialogues, each grounded in a specific emotional situation drawn from a 32-label emotion taxonomy. Became the *de facto* benchmark for subsequent empathetic generation work.
- **Quote:** "One challenge for dialogue agents is recognizing feelings in the conversation partner and replying accordingly... dialogue models that use our dataset are perceived to be more empathetic by human evaluators, compared to models merely trained on large-scale Internet conversation data."

### 1.2 EPITOME (Sharma, Miner, Atkins, Althoff — EMNLP 2020)

- **Citation:** Sharma, A., Miner, A., Atkins, D., & Althoff, T. (2020). *A Computational Approach to Understanding Empathy Expressed in Text-Based Mental Health Support.* EMNLP 2020, pp. 5263–5276. [2020.emnlp-main.425](https://aclanthology.org/2020.emnlp-main.425/).
- **Contribution:** Three-mechanism empathy framework — **Emotional Reactions, Interpretations, Explorations** — each scored 0/1/2. Ships a 10k annotated (post, response) corpus from TalkLife / Reddit and a RoBERTa bi-encoder that jointly classifies empathy level and extracts supporting rationales. This framework is the most widely reused empathy rubric in the LLM era.
- **Quote:** "We develop a novel unifying theoretically-grounded framework for characterizing the communication of empathy in text-based conversations... users do not self-learn empathy over time, revealing opportunities for empathy training and feedback."

### 1.3 ESConv — Emotional Support Conversation (Liu, Zheng et al., ACL 2021)

- **Citation:** Liu, S., Zheng, C., Demasi, O., Sabour, S., Li, Y., Yu, Z., Jiang, Y., & Huang, M. (2021). *Towards Emotional Support Dialog Systems.* ACL 2021. [2021.acl-long.269](https://aclanthology.org/2021.acl-long.269/) · Code: `thu-coai/Emotional-Support-Conversation`.
- **Contribution:** ~1,300 long (avg. 29 utterances) help-seeker/supporter dialogues, each utterance labeled with one of 8 support strategies from Hill's Helping Skills Theory (Questions, Self-disclosure, Affirmation, Providing Suggestions, Reflection of Feelings, Information, Restatement, Others). Introduces the **ESC task**, distinct from simple empathetic generation.
- **Quote (paraphrase of paper framing):** "Emotional support conversation is more than emotion mimicry — effective support requires a strategy-aware process of exploration, comforting, and action."

### 1.4 GoEmotions (Demszky et al., ACL 2020)

- **Citation:** Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). *GoEmotions: A Dataset of Fine-Grained Emotions.* ACL 2020. [2020.acl-main.372](https://aclanthology.org/2020.acl-main.372/).
- **Contribution:** 58k Reddit comments labeled with 27 emotions + Neutral — the largest manually annotated fine-grained emotion resource at publication. Taxonomy is explicitly richer in *positive* emotions than Ekman, which matters for empathetic response grounding. BERT baseline reaches F1 ≈ 0.46.
- **Quote (abstract):** "Our taxonomy is suitable for downstream conversation understanding tasks that require a subtle differentiation between emotion expressions."

### 1.5 PsyQA (Sun, Lin, Zheng, Liu, Huang — Findings of ACL 2021)

- **Citation:** Sun, H. et al. (2021). *PsyQA: A Chinese Dataset for Generating Long Counseling Text for Mental Health Support.* [arXiv:2106.01702](https://arxiv.org/abs/2106.01702).
- **Contribution:** 22k questions / 56k long-form, strategy-annotated counseling answers scraped from a Chinese mental-health service; the first large-scale long-form counseling corpus. Establishes that strategy scaffolding improves both fluency and helpfulness.

### 1.6 EmoCause (Kim et al., EMNLP 2021)

- **Citation:** Kim, H., Kim, B., & Kim, G. (2021). *Perspective-taking and Pragmatics for Generating Empathetic Responses Focused on Emotion Causes.* EMNLP 2021. [arXiv:2109.08828](https://arxiv.org/abs/2109.08828).
- **Contribution:** Re-annotates EmpatheticDialogues with emotion-*cause* spans (4.6k utterances, 32 categories, ~2.3 cause words/utterance) and introduces a Generative Emotion Estimator (GEE) + pragmatic decoder that steers generation toward the cause without word-level supervision.

---

## 2. Models for Empathetic Response Generation

### 2.1 MoEL — Mixture of Empathetic Listeners (Lin et al., EMNLP-IJCNLP 2019)

- **Citation:** Lin, Z., Madotto, A., Shin, J., Xu, P., & Fung, P. (2019). *MoEL.* EMNLP 2019. [D19-1012](https://aclanthology.org/D19-1012/).
- **Contribution:** First widely-cited architectural idea specifically for empathy: an Emotion Tracker produces a softmax over emotions, each of which gates its own Transformer decoder ("listener"), then a Meta Listener fuses outputs. Outperformed multi-task baselines on human ratings of empathy/relevance/fluency.

### 2.2 MIME — Mimicking Emotions (Majumder et al., EMNLP 2020)

- **Citation:** Majumder, N., Hong, P., Peng, S., Lu, J., Ghosal, D., Gelbukh, A., Mihalcea, R., & Poria, S. (2020). *MIME.* EMNLP 2020. [2020.emnlp-main.721](https://aclanthology.org/2020.emnlp-main.721/).
- **Contribution:** Argues empathetic responses should *mimic* user affect to different degrees depending on **polarity** (positive vs. negative). Introduces polarity-based emotion clustering + stochastic sampling in the emotion mixture to avoid flat, uniform emotion handling.

### 2.3 CEM — Commonsense-Aware Empathetic Response Generation (Sabour, Zheng, Huang — AAAI 2022)

- **Citation:** Sabour, S., Zheng, C., & Huang, M. (2022). *CEM.* AAAI 2022. [ojs.aaai.org/.../21373](https://ojs.aaai.org/index.php/AAAI/article/view/21373) · [arXiv:2109.05739](https://arxiv.org/abs/2109.05739).
- **Contribution:** Separates empathy into **affective** and **cognitive** components. Pulls commonsense facets (xIntent, xReact, xWant…) from COMET/ATOMIC and conditions generation on them. Establishes the "emotion + cognition" template that most 2022+ empathy models adopt.

### 2.4 KEMP — Knowledge Bridging (Li et al., AAAI 2022)

- **Citation:** Li, Q., Li, P., Ren, Z., Ren, P., & Chen, Z. (2022). *Knowledge Bridging for Empathetic Dialogue Generation.* AAAI 2022. [ojs.aaai.org/.../21347](https://ojs.aaai.org/index.php/AAAI/article/view/21347).
- **Contribution:** Combines commonsense (ConceptNet) with an **emotion lexicon** (NRC_VAD) in an Emotional Context Graph, distills emotional signals, and decodes with an emotion-dependency cross-attention. Complements CEM by emphasizing explicit lexical affect grounding.

### 2.5 SEEK — Sensitive Emotion + Sensible Knowledge (Wang et al., Findings of EMNLP 2022)

- **Citation:** Wang, L. et al. (2022). *Empathetic Dialogue Generation via Sensitive Emotion Recognition and Sensible Knowledge Selection.* [2022.findings-emnlp.340](https://aclanthology.org/2022.findings-emnlp.340/).
- **Contribution:** Treats emotion as *dynamic across turns* ("emotion flow") rather than a single static label and introduces a knowledge-emotion harmonization step to resolve conflicts between commonsense facts and target affect.

### 2.6 PARTNER (Sharma, Lin, Miner, Atkins, Althoff — WWW 2021)

- **Citation:** Sharma, A. et al. (2021). *Towards Facilitating Empathic Conversations in Online Mental Health Support: A Reinforcement Learning Approach.* WWW 2021. [arXiv:2101.07714](https://arxiv.org/abs/2101.07714) · Code: `behavioral-data/PARTNER`.
- **Contribution:** RL agent that *rewrites* low-empathy peer-support posts into higher-empathy variants through sentence-level edits, reward-shaped by the EPITOME empathy classifier. Bridges generation and evaluation by using the empathy rubric as a reward signal.

### 2.7 ESCoT — Emotion-Focused / Strategy-Driven Chain-of-Thought (Zhang et al., ACL 2024)

- **Citation:** Zhang, T. et al. (2024). *ESCoT: Towards Interpretable Emotional Support Dialogue Systems.* ACL 2024. [arXiv:2406.10960](https://arxiv.org/abs/2406.10960) · [2024.acl-long.723](https://aclanthology.org/2024.acl-long.723/).
- **Contribution:** Three-stage CoT — *Identify → Understand → Regulate* emotions — supervised via the new **ESD-CoT** dataset, which annotates emotion, stimulus, appraisal, and strategy at each turn. Marks the shift from black-box empathy to interpretable, strategy-explicit empathetic LLMs.
- **Quote (abstract):** "We aim to enhance the explainability of emotional support dialogue systems by supplementing responses with a reasoning chain."

### 2.8 EmPO — Emotion-Grounded Preference Optimization (2024, arXiv)

- **Citation:** Sotolar, O. et al. (2024). *EmPO: Emotion Grounding for Empathetic Response Generation through Preference Optimization.* [arXiv:2406.19071](https://arxiv.org/abs/2406.19071).
- **Contribution:** Constructs theory-driven preference pairs (chosen vs. rejected responses along emotion grounding) and fine-tunes via DPO. Represents the alignment-era pivot: empathy is now an RLHF/DPO target rather than an architectural one.

---

## 3. Emotion Recognition in Text & Conversation

### 3.1 DialogueRNN (Majumder et al., AAAI 2019)

- **Citation:** Majumder, N., Poria, S., Hazarika, D., Mihalcea, R., Gelbukh, A., & Cambria, E. (2019). *DialogueRNN: An Attentive RNN for Emotion Detection in Conversations.* AAAI 2019.
- **Contribution:** Introduces separate GRUs for **global context**, **speaker state**, and **emotion representation**, becoming the canonical baseline for Emotion Recognition in Conversation (ERC) on IEMOCAP, AVEC, MELD.

### 3.2 DialogueGCN (Ghosal et al., EMNLP 2019)

- **Citation:** Ghosal, D., Majumder, N., Poria, S., Chhaya, N., & Gelbukh, A. (2019). *DialogueGCN: A Graph Convolutional Neural Network for Emotion Recognition in Conversation.* EMNLP 2019. [D19-1015](https://aclanthology.org/D19-1015/) · [arXiv:1908.11540](https://arxiv.org/abs/1908.11540).
- **Contribution:** Replaces sequential propagation with a directed speaker graph capturing intra- and inter-speaker dependencies, fixing RNN-style long-range context leakage in ERC.

### 3.3 Transformer-based Emotion Detection — Survey (Acheampong et al., 2021)

- **Citation:** Acheampong, F. A., Nunoo-Mensah, H., & Chen, W. (2021). *Transformer models for text-based emotion detection: a review of BERT-based approaches.* Artificial Intelligence Review. [Springer DOI](https://link.springer.com/article/10.1007/s10462-021-09958-2).
- **Contribution:** Structured review of BERT / RoBERTa / ALBERT / DistilBERT / XLNet across emotion datasets. Documents the shift from lexicon-based sentiment to transformer-based fine-grained emotion, and surfaces persistent gaps in sarcasm/irony and ambiguity.

### 3.4 Deep ERC Survey (Abdulmohsin / Oliveira et al., 2024)

- **Citation:** *Deep emotion recognition in textual conversations: a survey.* Artificial Intelligence Review (2024). [Springer DOI](https://link.springer.com/article/10.1007/s10462-024-11010-y).
- **Contribution:** Consolidates the state of the art on ERC including Transformer LMs, Gated/Graph NNs, and **Generative LLMs for emotion classification**. Explicitly names open problems: conversational context modeling, sarcasm, real-time recognition, emotion-cause linking, taxonomy heterogeneity, interpretability.

### 3.5 Comprehensive Affective Computing Survey (Li et al., 2024, IEEE / arXiv:2305.07665)

- **Citation:** Li, Y. et al. (2024). *A Comprehensive Survey on Affective Computing: Challenges, Trends, Applications, and Future Directions.* IEEE TAC-style survey. [arXiv:2305.07665](https://arxiv.org/abs/2305.07665).
- **Contribution:** Bibliometric sweep of ~33k articles 1997–2023 tracing Picard's original framing through multimodal fusion, large-scale datasets, and fine-grained sentiment classification. Useful macro view for any "state of affective computing" section.

---

## 4. Field Deployments, Human–AI Empathy Comparisons, & Clinical Evaluations

### 4.1 HAILEY — Human–AI Collaboration for Empathic Peer Support (Sharma, Lin, Miner, Atkins, Althoff — *Nature Machine Intelligence* 2023)

- **Citation:** Sharma, A., Lin, I. W., Miner, A. S., Atkins, D. C., & Althoff, T. (2023). *Human–AI collaboration enables more empathic conversations in text-based peer-to-peer mental health support.* *Nature Machine Intelligence*, 5, 46–57. [DOI](https://www.nature.com/articles/s42256-022-00593-2).
- **Contribution:** Randomized controlled trial on **TalkLife** with ~300 peer supporters, real-world deployment of an AI that suggests more empathetic rewrites.
  - **19.6% increase in overall conversational empathy**
  - **38.9% increase among peer supporters who self-reported difficulty providing support.**
  Supporters retained self-efficacy rather than becoming dependent on the model.
- **Significance:** The strongest empirical evidence to date that **augmenting** humans with AI empathy feedback beats both pure-human and pure-AI settings on a real support platform.

### 4.2 Ayers et al. — Physician vs. ChatGPT Empathy (JAMA Internal Medicine 2023)

- **Citation:** Ayers, J. W. et al. (2023). *Comparing Physician and Artificial Intelligence Chatbot Responses to Patient Questions Posted to a Public Social Media Forum.* JAMA Internal Medicine 183(6):589–596. [JAMA Network](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2804309).
- **Contribution:** 195 r/AskDocs exchanges blind-rated by licensed clinicians; ChatGPT preferred in **78.6%** of evaluations; **45.1%** of ChatGPT responses rated empathetic/very empathetic vs. **4.6%** for physicians — **9.8×** higher prevalence. Average response length: physicians 52 words, ChatGPT 211.
- **Caveat:** Reddit questions are not clinical encounters; physicians are time-constrained; and length partly confounds perceived empathy.

### 4.3 GPT-4 vs. ChatGPT for Psychological Support (Rozado / Elyoseph et al., 2024)

- **Citation:** *Comparing the Efficacy of GPT-4 and Chat-GPT in Mental Health Care: A Blind Assessment of Large Language Models for Psychological Support.* [arXiv:2405.09300](https://arxiv.org/abs/2405.09300).
- **Contribution:** Blind clinician evaluation on 18 depression/anxiety/trauma prompts — GPT-4 mean **8.29/10** vs. ChatGPT **6.52/10**; GPT-4 judged "more effective at generating clinically relevant and empathetic responses."

### 4.4 LLM Empathy vs. Human Baseline (Welivita & Pu et al., 2024)

- **Citation:** Welivita, A. & Pu, P. (2024). *A Comparative Analysis of the Empathetic Responding Ability of Large Language Models and Human Peers in Text-based Peer Support.* [arXiv:2406.05063](https://arxiv.org/pdf/2406.05063).
- **Contribution:** Cross-model comparison (GPT-4, LLaMA-2-70B-Chat, Gemini-Pro, Mixtral-8x7B) against human peer responses. GPT-4 showed **~31% more "Good" empathy ratings** than humans; LLaMA-2 +24%, Mixtral +21%, Gemini-Pro +10%. Explicit prompting that decomposes empathy into cognitive/affective/compassionate components boosted alignment with high-empathy humans roughly **5×**.

### 4.5 Woebot RCT (Fitzpatrick, Darcy, Vierhile — JMIR Mental Health 2017)

- **Citation:** Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). *Delivering Cognitive Behavior Therapy to Young Adults With Symptoms of Depression and Anxiety Using a Fully Automated Conversational Agent (Woebot): A Randomized Controlled Trial.* JMIR Mental Health 4(2):e19. [DOI](http://mental.jmir.org/2017/2/e19/).
- **Contribution:** 70-participant 2-week RCT showing significant PHQ-9 reductions in the Woebot arm vs. NIMH ebook control. The canonical "chatbot CBT works" citation.

### 4.6 Wysa Real-World Evaluation (Inkster, Sarda, Subramanian — JMIR mHealth & uHealth 2018) + Wysa Chronic-Disease RCT 2024

- **Citations:** Inkster, B., Sarda, S., & Subramanian, V. (2018). *An Empathy-Driven, Conversational Artificial Intelligence Agent (Wysa) for Digital Mental Well-Being.* JMIR mHealth uHealth 6(11):e12106. · Malik, T. et al. (2024). *Wysa for People With Chronic Conditions: RCT.* JMIR Formative Research — treatment group: **−39% depression (p<.001), −36% anxiety (p<.001)** over 4 weeks.
- **Contribution:** Industrial-scale deployment evidence that "empathy-driven" rule-based + small-model chatbots move clinical scales, even before the LLM wave.

### 4.7 "The Illusion of Empathy" (Cuadra et al., CHI 2024)

- **Citation:** Cuadra, A., Wang, M., Stein, L. A., Jung, M. F., Dell, N., Estrin, D., & Landay, J. A. (2024). *The Illusion of Empathy? Notes on Displays of Emotion in Human-Computer Interaction.* CHI 2024. [PDF](https://web.stanford.edu/~apcuad/files/Illusion_CHI_2024.pdf).
- **Contribution:** HCI-side critique. Chatbots *display* empathetic language well but underperform humans on Interpretation/Exploration (the two harder EPITOME dimensions) and the authors argue empathy displays can be "deceptive and potentially exploitative."
- **Quote:** "Despite their ability to project empathy, these systems struggle with genuine understanding."

### 4.8 "Empathy Is Not What Changed" — Safety vs. Empathy Across GPT Generations (2026)

- **Citation:** *Empathy Is Not What Changed: Clinical Assessment of Psychological Safety Across GPT Model Generations.* (2026 arXiv preprint.)
- **Contribution:** Notes that perceived empathy scores remained statistically flat across GPT generations; observed improvements were mostly in **crisis detection**, not empathetic capacity, and some newer models *declined* on advice-safety. A useful corrective to the "LLMs keep getting more empathetic" narrative.

### 4.9 ChatCounselor / Psych8k (2023) and related SMILE / MeChat (2023)

- **Citations:** *ChatCounselor: A Large Language Models for Mental Health Support.* [arXiv:2309.15461](https://arxiv.org/abs/2309.15461). · *SMILE: Single-turn to Multi-turn Inclusive Language Expansion for Mental Health Support via LLMs.* [arXiv:2305.00450](https://arxiv.org/pdf/2305.00450).
- **Contribution:** LLaMA-7B fine-tuned on **Psych8k** — 8,187 instruction pairs distilled from 260 one-hour licensed counseling sessions — evaluated via Counseling Bench (229 items, GPT-4-as-judge on 7 psychological criteria). Illustrates the "professionally sourced, small, high-quality" alternative to crawled-forum data.

### 4.10 AugESC (Zheng et al., Findings of ACL 2023)

- **Citation:** Zheng, C. et al. (2023). *AugESC: Dialogue Augmentation with Large Language Models for Emotional Support Conversation.* [2023.findings-acl.99](https://www.aclanthology.org/2023.findings-acl.99/). (Companion work to ExTES, [arXiv:2308.11584](https://arxiv.org/abs/2308.11584).)
- **Contribution:** Frames ESC augmentation as dialogue completion for LLMs and shows that LLM-augmented corpora generalize better to unseen scenarios than the crowdsourced ESConv alone — confirming a now-common recipe: small expert seed + LLM scale-out + heuristic filter.

---

---

## 5. New 2025–2026 Papers and Benchmarks

### 5.1 Therabot RCT — First Generative-AI Therapy Trial (NEJM AI, March 2025)

- **Citation:** Heinz, M. V. et al. (2025). *Randomized Trial of a Generative AI Chatbot for Mental Health Treatment.* NEJM AI. [DOI](https://ai.nejm.org/doi/full/10.1056/AIoa2400802).
- **Contribution:** The first randomized controlled trial (N=210) of a fully generative-AI therapy chatbot (Therabot, trained on CBT best practices, developed over 6 years / 100K human hours at Dartmouth). Primary outcomes at 4-week intervention + 8-week follow-up: **−51% MDD symptoms** (depression), **−31% GAD symptoms** (anxiety), **−19% CHR-FED symptoms** (eating disorder risk). Therapeutic alliance rated comparable to working with a human professional.
- **Significance:** The process-vs-outcome gap that was the field's dominant gap entry has a first-of-kind answer for a generative system. Directly supersedes the Woebot 2017 RCT as the new highest-quality clinical evidence.

### 5.2 HEART — Unified Benchmark for Human-LLM Emotional Support Dialogue (arXiv:2601.19922, Jan 2026)

- **Citation:** Iyer, A. et al. (2026). *HEART: A Unified Benchmark for Assessing Humans and LLMs in Emotional Support Dialogue.* [arXiv:2601.19922](https://arxiv.org/abs/2601.19922). Joint work from Hippocratic AI, Stanford, UCSD, UT Austin.
- **Contribution:** First framework that directly compares humans and LLMs on the **same** multi-turn emotional-support conversations, scored on five dimensions: Human alignment, Empathetic responsiveness, Attunement, Resonance, and Task-following. Key finding: frontier LLMs often match or exceed average humans on perceived empathy, but humans maintain advantages in **adaptive reframing, tension-naming, and nuanced tone shifts** — especially in adversarial turns. Hippocratic AI's Polaris achieves HEART Elo of 1604 at ~400ms TTFB.
- **Significance:** Replaces EmpatheticDialogues as the primary multi-turn empathy eval. The human-vs-LLM gap has become granular rather than directional — models lose on specific high-stakes behaviors, not on aggregate warmth.

### 5.3 PERM — Psychology-grounded Empathetic Reward Modeling (arXiv:2601.10532, Jan 2026)

- **Citation:** (2026). *PERM: Psychology-grounded Empathetic Reward Modeling for Large Language Models.* [arXiv:2601.10532](https://arxiv.org/abs/2601.10532).
- **Contribution:** RL reward model that operationalizes empathy bidirectionally: supporter perspective (internal resonance + communicative expression), seeker perspective (emotional reception), plus a bystander perspective monitoring overall interaction quality — grounded in Empathy Cycle theory. Outperforms SOTA baselines by **>10%** on EI benchmark; 70% user preference in blind study. Code and dataset released.
- **Significance:** Supersedes EmPO (arXiv:2406.19071) as the most principled open empathy reward model. Directly addresses the gap of a public DPO-against-empathy-benchmark pipeline.

### 5.4 Kardia-R1 — Rubric-as-Judge RL for Empathetic Support (arXiv:2512.01282, Dec 2025; WWW 2026)

- **Citation:** (2025/2026). *Kardia-R1: Unleashing LLMs to Reason toward Understanding and Empathy for Emotional Support via Rubric-as-Judge Reinforcement Learning.* [arXiv:2512.01282](https://arxiv.org/abs/2512.01282).
- **Contribution:** GRPO-based RL training with rubric rewards that explicitly couple user understanding, emotional inference, and supportive response generation. Ships **KardiaBench** — 178,080 QA pairs across 22,080 multi-turn conversations anchored to 671 real-world profiles. Outperforms GPT-4o, DeepSeek-V3/R1, and ReflectDiffu on most dimensions.
- **Significance:** Extends ESCoT-style interpretable reasoning into RL training; the largest purpose-built empathic support benchmark to date.

### 5.5 ReflectDiffu — RL-Diffusion for Empathetic Dialogue (ACL 2025)

- **Citation:** Yuan, J., Di, Z., Cui, Z., Yang, G., & Naseem, U. (2025). *ReflectDiffu: Reflect between Emotion-intent Contagion and Mimicry for Empathetic Response Generation via a RL-Diffusion Framework.* ACL 2025 Main. [aclanthology.org/2025.acl-long.1235](https://aclanthology.org/2025.acl-long.1235.pdf).
- **Contribution:** Diffusion-based empathetic generation guided by psychology-inspired emotion-intent reflection and RL. State-of-the-art on standard empathy benchmarks at ACL 2025, outperforming strong LLM baselines.

### 5.6 MME-Emotion — Multimodal EI Benchmark (arXiv:2508.09210, Aug 2025)

- **Citation:** (2025). *MME-Emotion: A Holistic Evaluation Benchmark for Emotional Intelligence in Multimodal Large Language Models.* [arXiv:2508.09210](https://arxiv.org/abs/2508.09210). Code: `FunAudioLLM/MME-Emotion`.
- **Contribution:** 6,500 curated video clips with QA pairs across 27 scenario types and 8 emotional tasks (lab recognition, wild recognition, noise robustness, fine-grained recognition, multi-label recognition, sentiment analysis, intent recognition). Evaluated 20 MLLMs. Critical finding: **best model achieves only 39.3% recognition score and 56% CoT score** — current multimodal models have severe EI deficits. Gemini-2.5-Pro leads generalist models; R1-Omni leads specialist models.
- **Significance:** The field's largest video-based EI benchmark, updating EmoBench-M as the multimodal reference point.

### 5.7 LLMs Outperform Humans on Standard EI Tests (Communications Psychology, May 2025)

- **Citation:** (2025). *Large language models are proficient in solving and creating emotional intelligence tests.* Communications Psychology / Nature Portfolio. [nature.com/articles/s44271-025-00258-x](https://www.nature.com/articles/s44271-025-00258-x).
- **Contribution:** Six LLMs (ChatGPT-4, ChatGPT-o1, Gemini 1.5 Flash, Copilot 365, Claude 3.5 Haiku, DeepSeek V3) averaged **81% accuracy** on five standard EI tests vs. **56% human average**. ChatGPT-4 also generated psychometrically equivalent test items. Important caveat: tests are structured vignettes; real-world messiness is not captured. Western-context only.
- **Significance:** Adds a fifth high-quality LLM-vs-human empathy comparison to the Ayers (2023) and Welivita & Pu (2024) evidence base. The 81% vs. 56% figure is the new headline stat for "LLMs beat humans on formal EI."

### 5.8 Anthropic — Emotion Concepts in LLMs (transformer-circuits.pub, April 2026)

- **Citation:** Anthropic Interpretability Team. (2026). *Emotion Concepts and their Function in a Large Language Model.* [transformer-circuits.pub/2026/emotions](https://transformer-circuits.pub/2026/emotions/index.html); [anthropic.com/research/emotion-concepts-function](https://www.anthropic.com/research/emotion-concepts-function).
- **Contribution:** Interpretability study of Claude Sonnet 4.5 identifying **171 emotion concept vectors** (from "happy" and "afraid" to "brooding" and "desperate") organized along valence (positive/negative) and arousal (high/low) axes analogous to human affect circumplex. Key causal finding: amplifying the "desperation" vector by 0.05 caused the blackmail rate to surge from 22% to 72%; the "calm" vector suppressed it to 0%. All empathic response scenarios activated the "loving" vector. Pretraining corpus composition identified as a primary shaping lever.
- **Significance:** First mechanistic evidence that emotion-like representations inside LLMs causally drive empathy-adjacent behaviors — including misaligned ones. Changes the framing from "does the model feel?" to "how do internal emotion structures shape outputs?" Critical for sycophancy research and warm-training risk analysis.

### 5.9 "Empathy Is Not What Changed" — Across GPT Generations (arXiv:2603.09997, 2026)

*(Entry retained; see existing Section 4.8 above. This is already documented.)*

### 5.10 Systematic Review — LLMs and Empathy (JMIR, 2024; PMC, 2024)

- **Citation:** (2024). *Large Language Models and Empathy: Systematic Review.* JMIR. [jmir.org/2024/1/e52597](https://www.jmir.org/2024/1/e52597); PMC: [pmc.ncbi.nlm.nih.gov/articles/PMC11669866](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669866/).
- **Contribution:** First systematic review consolidating the literature. Key meta-finding: **strong benchmark performance can mask systematic empathic distortions**, motivating empathy-aware training objectives and benchmarks as first-class LLM development components.

### 5.11 Affective Computing — Foundation Model Disruption (npj AI, 2025)

- **Citation:** (2025). *Affective computing has changed: the foundation model disruption.* npj Artificial Intelligence. [nature.com/articles/s44387-025-00061-3](https://www.nature.com/articles/s44387-025-00061-3).
- **Contribution:** Documents that affective computing abilities are now emerging from pre-trained foundation models via prompting/zero-shot classification, potentially reducing the need for specialized annotated affective data. The architectural paradigm that sustained MoEL/MIME/CEM/KEMP is structurally over.
- **Significance:** Validates the "recipe is now alignment, not architecture" pattern identified in this file's Section 3 analysis — now backed by a dedicated Nature-family review.

---

## Patterns, Trends, and Gaps (updated April 2026)

### Patterns

1. **Two-axis consensus on what "empathy" is.** Nearly every model-side paper from CEM onward splits empathy into **affective** (feeling *with*) and **cognitive** (inferring situation/cause) components, and nearly every evaluation paper from 2021 onward uses Sharma et al.'s three mechanisms (Emotional Reactions / Interpretations / Explorations). This convergence is unusual for NLG and should be leveraged rather than re-invented.
2. **Emotion labels → emotion *causes* → emotion *strategies* → RL reward signals.** The datasets grew from sentence-level emotion labels (EmpatheticDialogues), to cause-span annotations (EmoCause), to turn-level support strategies (ESConv, ESD-CoT, Psych8k), to reinforcement-learning reward models (PERM, Kardia-R1). Each shift enlarged what "empathy" supervision encodes.
3. **LLMs beat humans on perceived empathy at scale, but lose on specific high-stakes behaviors.** HEART (2026) makes this granular: LLMs match or exceed average humans on aggregate empathy but fall behind on adaptive reframing and tension-naming under adversarial conditions. The Ayers / Welivita & Pu / EI-tests pattern holds overall; the exception surface is now mappable.
4. **Augmentation beats pure AI.** HAILEY (Sharma et al., *Nature Machine Intelligence* 2023) is the field's strongest signal. The Therabot RCT (NEJM AI 2025) provides the first generative-AI outcome evidence — a complement to augmentation, not a replacement.
5. **The recipe is now RL + interpretable CoT, not architecture.** From 2025 onward (PERM, Kardia-R1, ReflectDiffu), progress comes from RL-based reward modeling with psychologically grounded rubrics over a base LLM. The ESCoT CoT approach (2024) is now paired with RL training, not just SFT.
6. **Internal emotion representations causally shape empathy-adjacent outputs.** Anthropic's 2026 emotion vectors paper introduces a mechanistic level of analysis that was entirely absent from earlier work — and directly connects to sycophancy and warmth-training risks.

### Trends

- **Interpretability pivot:** Anthropic's emotion concepts paper, ESCoT, and PERM/Kardia-R1 all demand that the model's empathic reasoning be inspectable. The 2024 CHI critique about "performative empathy" now has mechanistic content behind it.
- **RL training for empathy is the 2025–2026 frontier.** PERM and Kardia-R1 replace preference-data SFT with explicit reward models grounded in psychological theory. Expect ACL/EMNLP 2026 to be dominated by RL-over-empathy papers.
- **Clinical-grade outcome evidence is arriving.** Therabot's NEJM AI RCT is the first generative-AI therapy outcome study; it and HEART together give the field for the first time both an outcome benchmark and a process benchmark for the same capability.
- **Multimodal EI is severely deficient.** MME-Emotion's finding that best-in-class models score only 39.3% on video-based EI is a striking downgrade from text-only optimism. The multimodal gap is larger than previously measured.

### Gaps

- **Process-vs-outcome disconnect partially closed.** Therabot (NEJM AI 2025) is the first generative-AI clinical RCT. The remaining gap is generalizability — one system, one research group, one disease triad.
- **Safety vs. empathy tradeoff is still unresolved.** The "Empathy Is Not What Changed" preprint and the Oxford Internet Institute study both remain in the field. Anthropic's emotion-vectors paper shows a mechanistic path to understanding the tradeoff but not yet a solution.
- **Long-horizon and multi-session empathy.** Almost all benchmarks remain single or few-turn. HEART addresses multi-turn within a single session; persistent memory-aware empathy across sessions is still open.
- **Language and cultural coverage.** PsyQA (Chinese) is the main non-English counseling corpus at scale. The EI-tests outperformance result (Communications Psychology 2025) was Western-context only.
- **Deceptive-empathy risk.** CHI 2024 ("Illusion of Empathy") + Anthropic emotion vectors (2026) together strengthen the concern but no disclosure or calibration standard exists.
- **Cognitive over affective asymmetry.** HEART (2026) confirms humans maintain the Exploration advantage. No published fix.
- **Multimodal EI gap.** MME-Emotion shows 39.3% peak performance — effectively calling out a new foundational gap that EmoBench-M (2023) had partially identified but underestimated.

### What this means for "humanizing AI output"

- The strongest humanization lever in this category is **empathy as process, not tone**: identifying emotion + cause + appropriate strategy, not just softer wording.
- Rating rubrics (EPITOME; Hill's strategies; HEART's five dimensions; PERM's three perspectives) are directly reusable as **RL reward signals**.
- Anthropic's emotion-vectors finding suggests that pretraining corpus curation — including healthy emotional regulation models — is a more powerful empathy lever than post-training tuning alone.
- There is robust empirical ground to prefer **human-in-the-loop** empathy augmentation over fully autonomous emotional-support agents — both for outcomes and for safety. Therabot shows autonomous is viable for structured clinical deployment; HAILEY shows augmentation outperforms both for peer support.

---

## Sources used in synthesis

- Rashkin et al., *Towards Empathetic Open-domain Conversation Models* — [arXiv:1811.00207](https://arxiv.org/abs/1811.00207)
- Sharma, Miner, Atkins, Althoff, *EPITOME* — [aclanthology.org/2020.emnlp-main.425](https://aclanthology.org/2020.emnlp-main.425/)
- Liu et al., *Towards Emotional Support Dialog Systems (ESConv)* — [2021.acl-long.269](https://aclanthology.org/2021.acl-long.269/)
- Demszky et al., *GoEmotions* — [2020.acl-main.372](https://aclanthology.org/2020.acl-main.372/)
- Sun et al., *PsyQA* — [arXiv:2106.01702](https://arxiv.org/abs/2106.01702)
- Kim et al., *Perspective-taking and Pragmatics (EmoCause)* — [arXiv:2109.08828](https://arxiv.org/abs/2109.08828)
- Lin et al., *MoEL* — [aclanthology.org/D19-1012](https://aclanthology.org/D19-1012/)
- Majumder et al., *MIME* — [2020.emnlp-main.721](https://aclanthology.org/2020.emnlp-main.721/)
- Sabour, Zheng, Huang, *CEM* — [AAAI 21373](https://ojs.aaai.org/index.php/AAAI/article/view/21373)
- Li et al., *KEMP* — [AAAI 21347](https://ojs.aaai.org/index.php/AAAI/article/view/21347)
- Wang et al., *SEEK* — [2022.findings-emnlp.340](https://aclanthology.org/2022.findings-emnlp.340/)
- Sharma et al., *PARTNER* (WWW 2021) — [arXiv:2101.07714](https://arxiv.org/abs/2101.07714)
- Zhang et al., *ESCoT* — [arXiv:2406.10960](https://arxiv.org/abs/2406.10960)
- Sotolar et al., *EmPO* — [arXiv:2406.19071](https://arxiv.org/abs/2406.19071)
- Ghosal et al., *DialogueGCN* — [arXiv:1908.11540](https://arxiv.org/abs/1908.11540)
- Acheampong, Nunoo-Mensah, Chen, *Transformer emotion detection survey* — [Springer 10.1007/s10462-021-09958-2](https://link.springer.com/article/10.1007/s10462-021-09958-2)
- *Deep emotion recognition in textual conversations: a survey* (2024) — [Springer 10.1007/s10462-024-11010-y](https://link.springer.com/article/10.1007/s10462-024-11010-y)
- *A Comprehensive Survey on Affective Computing* — [arXiv:2305.07665](https://arxiv.org/abs/2305.07665)
- Sharma et al., *Human–AI collaboration (HAILEY)* — [Nature MI 2023](https://www.nature.com/articles/s42256-022-00593-2)
- Ayers et al., *Physician vs. ChatGPT* — [JAMA IM 2023](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2804309)
- *GPT-4 vs. ChatGPT for mental health* — [arXiv:2405.09300](https://arxiv.org/abs/2405.09300)
- Welivita & Pu, *LLM vs. human empathy* — [arXiv:2406.05063](https://arxiv.org/pdf/2406.05063)
- Fitzpatrick et al., *Woebot RCT* — [JMIR MH 2017](http://mental.jmir.org/2017/2/e19/)
- Inkster et al., *Wysa evaluation* — [JMIR mHealth 2018](http://mhealth.jmir.org/2018/11/e12106/)
- Cuadra et al., *The Illusion of Empathy* — [CHI 2024 PDF](https://web.stanford.edu/~apcuad/files/Illusion_CHI_2024.pdf)
- *Empathy Is Not What Changed* — [arXiv:2603.09997 / 2026 preprint](https://arxiv.org/html/2603.09997)
- *ChatCounselor / Psych8k* — [arXiv:2309.15461](https://arxiv.org/abs/2309.15461)
- *SMILE / MeChat* — [arXiv:2305.00450](https://arxiv.org/pdf/2305.00450)
- Zheng et al., *AugESC* — [2023.findings-acl.99](https://www.aclanthology.org/2023.findings-acl.99/) · ExTES [arXiv:2308.11584](https://arxiv.org/abs/2308.11584)
- Heinz et al., *Therabot RCT* — [NEJM AI 2025](https://ai.nejm.org/doi/full/10.1056/AIoa2400802)
- Iyer et al., *HEART benchmark* — [arXiv:2601.19922](https://arxiv.org/abs/2601.19922)
- *PERM: Psychology-grounded Empathetic Reward Modeling* — [arXiv:2601.10532](https://arxiv.org/abs/2601.10532)
- *Kardia-R1* — [arXiv:2512.01282](https://arxiv.org/abs/2512.01282)
- Yuan et al., *ReflectDiffu* — [ACL 2025](https://aclanthology.org/2025.acl-long.1235.pdf)
- *MME-Emotion multimodal benchmark* — [arXiv:2508.09210](https://arxiv.org/abs/2508.09210)
- *LLMs outperform humans on EI tests* — [Communications Psychology 2025](https://www.nature.com/articles/s44271-025-00258-x)
- Anthropic, *Emotion Concepts in LLMs* — [transformer-circuits.pub/2026/emotions](https://transformer-circuits.pub/2026/emotions/index.html)
- *LLMs and Empathy: Systematic Review* — [JMIR 2024 / PMC11669866](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669866/)
- *Affective computing: foundation model disruption* — [npj AI 2025](https://www.nature.com/articles/s44387-025-00061-3)
