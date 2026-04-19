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

## Patterns, Trends, and Gaps

### Patterns

1. **Two-axis consensus on what "empathy" is.** Nearly every model-side paper from CEM onward splits empathy into **affective** (feeling *with*) and **cognitive** (inferring situation/cause) components, and nearly every evaluation paper from 2021 onward uses Sharma et al.'s three mechanisms (Emotional Reactions / Interpretations / Explorations). This convergence is unusual for NLG and should be leveraged rather than re-invented.
2. **Emotion labels → emotion *causes* → emotion *strategies*.** The datasets grew from sentence-level emotion labels (EmpatheticDialogues), to cause-span annotations (EmoCause), to turn-level support strategies (ESConv, ESD-CoT, Psych8k). Each shift enlarged what "empathy" supervision encodes.
3. **LLMs beat humans on perceived empathy, at least on asynchronous text.** Multiple independent studies (Ayers 2023; Welivita & Pu 2024; GPT-4 vs ChatGPT 2024) replicate the finding that tuned LLM responses are rated more empathetic than time-pressured experts or peer supporters — consistent across clinician raters, crowd raters, and LLM judges.
4. **Augmentation beats pure AI.** HAILEY (Sharma et al., *Nature Machine Intelligence* 2023) is the field's strongest signal that **empathy is a human-AI team sport**: AI-suggested rewrites raised peer-to-peer empathy by ~20%, especially for struggling supporters, without hollowing out human authorship.
5. **The recipe is now instruction/alignment, not architecture.** From 2023 onward (EmPO, ESCoT, ChatCounselor, "Empathy by Design" DPO), progress comes from preference data and CoT-style process supervision over a base LLM, not from specialized encoders like MoEL/MIME/CEM.

### Trends

- **Interpretability pivot:** ESCoT, PEARL-CoT, and "Empathy by Design" demand that the model surface *why* a given strategy was chosen — a direct response to CHI-side critiques about performative empathy.
- **Strategy-first data:** New datasets increasingly label support strategies (Hill's Helping Skills, MI techniques) rather than emotions alone. Expect 2025+ benchmarks to grade on *strategy appropriateness*, not just emotion mimicry.
- **Clinical-grade evaluation arriving late:** Outside JMIR/JAMA venues, peer-reviewed ACL/EMNLP empathy work still leans on crowdsourced ratings of single turns; multi-session, outcome-tied evaluation is rare.

### Gaps

- **Process-vs-outcome disconnect.** Strong process evidence (higher EPITOME scores, higher human preference) does not yet translate into outcome evidence (PHQ-9 / GAD-7 reductions) for *LLM-based* systems. Woebot/Wysa have RCTs; GPT-4-class counselors largely do not.
- **Safety vs. empathy tradeoff is unresolved.** The 2026 *"Empathy Is Not What Changed"* result suggests newer models may trade advice-safety for perceived warmth — a critical blind spot for product teams chasing empathy metrics.
- **Long-horizon and multi-session empathy.** Almost all benchmarks are single or few-turn; memory-aware empathy across sessions (and the personalization it enables) remains open — connects directly to category 20 (Memory & Personalization).
- **Language and cultural coverage.** PsyQA (Chinese) is the main non-English counseling corpus at scale; Arabic, Hindi, Swahili, Spanish, etc. are severely under-represented, yet mental-health access gaps are largest in those languages.
- **Deceptive-empathy risk.** CHI 2024 ("Illusion of Empathy") reframes highly empathetic LLM output as potentially manipulative. There is no accepted disclosure or calibration standard analogous to medical informed-consent.
- **Cognitive over affective asymmetry.** Current LLMs score well on *Interpretation/Explanation* (cognitive empathy) but CHI user studies show users still perceive them as weaker on *Exploration* — the very behavior that drives therapeutic rapport.

### What this means for "humanizing AI output"

- The strongest humanization lever in this category is **empathy as process, not tone**: identifying emotion + cause + appropriate strategy, not just softer wording.
- Rating rubrics (EPITOME; Hill's strategies) are directly reusable as **RLHF/DPO reward signals** (as PARTNER and EmPO already demonstrate).
- There is robust empirical ground to prefer **human-in-the-loop** empathy augmentation over fully autonomous emotional-support agents — both for outcomes and for safety.

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
