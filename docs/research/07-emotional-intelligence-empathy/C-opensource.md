# Emotional Intelligence & Empathy in AI — Angle C: Open-Source & GitHub

**Research value: high** — The open-source ecosystem around empathetic AI is large, well-papered, and actively maintained, with clear patterns (support-strategy scaffolding, multi-turn empathy corpora, EI benchmarks) that can be lifted almost wholesale into a humanization pipeline.

**Scope:** 20 repositories covering empathetic LLM fine-tunes (EN + ZH), foundational empathy datasets, emotional-intelligence benchmarks, multimodal emotion models, and affective-computing libraries for text and voice. Emphasis on what each asset contributes to a system that tries to make AI output feel more human.

---

## 1. SmartFlowAI/EmoLLM — Mental-Health LLM, Multi-Base

- **URL:** https://github.com/SmartFlowAI/EmoLLM
- **Stars / License / Lang:** ~1,733 ⭐ · MIT · Python
- **Tagline (from repo):** *"心理健康大模型 (LLM x Mental Health), Pre & Post-training & Dataset & Evaluation & Deploy & RAG, with InternLM / Qwen / Baichuan / DeepSeek / Mixtral / LLaMA / GLM series models."*
- **What it gives you:** An end-to-end empathy-fine-tune cookbook — SFT data pipelines, RAG over counseling knowledge, evaluation harness, and deployment recipes across every major open base model. Training loop targets the "understand user → support user → help user" flow rather than classification.
- **2025 updates:** May 2025 — Caryou (AI psychological assistant, deep-thinking variant) merged into EmoLLM with RAG, web search, and TTS. February 2025 — first psychological health R1 distillation dataset released. March 2025 — full fine-tune on InternLM2.5-7B-chat (GGUF fp16) published.
- **Use for humanization:** Closest thing to a turnkey reference implementation if you want to port empathy behaviors onto any open base model. The evaluation harness is reusable even if you keep your own base model.

## 2. lzw108/EmoLLMs — Affective Analysis LLM Family

- **URL:** https://github.com/lzw108/EmoLLMs
- **Stars / License / Lang:** ~105 ⭐ · MIT · Python
- **What it gives you:** A family of instruction-tuned LLMs (Emollama-7B/13B, Emoopt-13B, Emobloom-7B, Emot5-large, Emobart-large) that handle *both* categorical emotion classification and continuous emotion-intensity regression — i.e., the model can say "sadness, 0.72" rather than just "sad."
- **Use for humanization:** Use as a **scorer / monitor** in a post-generation pipeline, not the generator. Lets you detect flat or mis-calibrated emotional tone in AI output before it ships.

## 3. scutcyr/SoulChat — Multi-Turn Empathy Fine-Tune (ZH)

- **URL:** https://github.com/scutcyr/SoulChat; SoulChat2.0: https://github.com/scutcyr/SoulChat2.0
- **Stars / License / Lang:** ~728 ⭐ · Apache-2.0 · Python
- **Tagline:** *"中文领域心理健康对话大模型 SoulChat"* (Chinese mental-health dialogue LLM).
- **What it gives you:** SoulChatCorpus — 258,354 multi-turn dialogues / 1,517,344 turns (open-sourced June 2024), plus a ChatGLM-6B SFT recipe explicitly tuned so the model stops rushing to advice and instead performs *questioning, comfort, affirmation, listening, trust-building.* Paper: Findings of EMNLP 2023. SoulChat2.0 launched as the "first digital twin LLM for psychological counselors."
- **Use for humanization:** The corpus is the most-cited artifact in the "LLMs jump to solutions too fast" critique. Fine-tuning signal here directly counteracts the "assistant voice" failure mode.

## 4. morecry/CharacterChat — MBTI-Matched Persona Support

- **URL:** https://github.com/morecry/CharacterChat
- **Stars / License / Lang:** open-source · Python · arXiv 2308.10278
- **What it gives you:** Two-part system — (a) a LLaMA-based conversational model with per-character persona + memory, and (b) an *interpersonal matching* plugin that picks one of 1,024 MBTI-decomposed virtual supporters for the user. Built on a new S2Conv (Social Support Conversation) dataset.
- **Use for humanization:** Non-obvious contribution — they explicitly reject the "one-size-fits-all emotional support" assumption and argue empathy needs *personality compatibility* between speaker and listener. Directly relevant if your humanization system varies voice per user.

## 5. ZebangCheng/Emotion-LLaMA — Multimodal Emotion Reasoning

- **URL:** https://github.com/ZebangCheng/Emotion-LLaMA
- **Stars / Venue:** NeurIPS 2024 · Python · HuggingFace demo available
- **What it gives you:** A LLaMA variant with emotion-specific encoders (HuBERT for audio; MAE / VideoMAE / EVA for facial analysis) aligned into a shared semantic space via instruction tuning. Ships the MERR dataset (28,618 coarse + 4,487 fine-grained multimodal samples). SOTA on MER2023 (F1 0.9036), won MER2024 Noise track.
- **Use for humanization:** If your pipeline ever ingests voice or video (e.g., voice-mode humanization), this is the current best open reference for cross-modal emotion grounding.

## 6. facebookresearch/EmpatheticDialogues — Foundational Benchmark

- **URL:** https://github.com/facebookresearch/EmpatheticDialogues
- **Status:** Archived Oct 2023 (read-only) · CC-BY-NC-4.0
- **What it gives you:** The canonical 25K-conversation dataset (76,673 / 12,030 / 10,943 train/val/test) grounded in 32 emotion labels, plus PyTorch Transformer + BERT-retrieval baselines. Still the most-cited empathy benchmark in the field.
- **Use for humanization:** Required read for any empathy-eval story. Use as held-out test set even if you don't train on it, so your claims are comparable to published work.

## 7. thu-coai/Emotional-Support-Conversation (ESConv)

- **URL:** https://github.com/thu-coai/Emotional-Support-Conversation
- **Stars / Venue:** ~317 ⭐ · ACL 2021
- **What it gives you:** 1,300 long support dialogues across 10 problem topics (depression, breakup, job crisis, academic pressure, etc.) annotated with an 8-category *support strategy* taxonomy (Questions, Providing Suggestions, Affirmation and Reassurance, Self-disclosure, Reflection of Feelings, Information, Restatement/Paraphrasing, Other). May 2024 added `FailedESConv.json` with 196 *negative* examples — support attempts that failed.
- **Use for humanization:** The strategy taxonomy is the most portable artifact here. Condition generation on a predicted strategy label instead of hoping the model "is empathetic."

## 8. thu-coai/PsyQA — Long-Form Chinese Counseling Dataset

- **URL:** https://github.com/thu-coai/PsyQA
- **Venue:** ACL 2021 Findings · access gated behind user agreement
- **What it gives you:** 22K questions → 56K long structured answers from a Chinese mental-health platform, annotated with counseling-theory-grounded support strategies. Long-form (counseling letter length), not turn-by-turn.
- **Use for humanization:** Covers a regime most empathy datasets miss — *extended, narrative* supportive response rather than short chat turns.

## 9. EmoCareAI/ChatPsychiatrist (ChatCounselor)

- **URL:** https://github.com/EmoCareAI/ChatPsychiatrist
- **License / Venue:** Apache-2.0 · Python · PGAI CIKM 2023 (arXiv 2309.15461)
- **What it gives you:** Psych8K — an 8K instruction-tuning dataset built from real counseling dialogues using GPT-4 as extractor + filter. Full LLaMA-7B instruct-tune recipe plus domain-tailored evaluation metrics.
- **Use for humanization:** Good template for "GPT-4 as a distillation oracle over real human transcripts" — a pattern worth copying for any expert-behavior SFT set.

## 10. SteveKGYang/MentalLLaMA — Interpretable Mental-Health Analysis

- **URL:** https://github.com/SteveKGYang/MentalLLaMA
- **Venue / Base:** WWW 2024 · LLaMA2 (+33B LoRA variant)
- **What it gives you:** IMHI dataset — 105K samples across 8 mental-health analysis tasks from 10 social-media sources, with ChatGPT-generated *explanations* audited under human + automatic quality gates. Focus: classification + human-readable rationale, not chat.
- **Use for humanization:** Useful as the "explainability layer" — when the humanization system detects distress, use MentalLLaMA-style reasoning to justify why, rather than raw classifier scores.

## 11. Sahandfer/EmoBench — EI Benchmark for Text LLMs

- **URL:** https://github.com/Sahandfer/EmoBench
- **Stars / Venue:** ~114 ⭐ · ACL 2024
- **What it gives you:** 400 hand-crafted scenarios (EN + ZH) grounded in psychological EI theory, split into two capabilities: **Emotional Understanding** (recognize emotions and their causes) and **Emotional Application** (recommend an effective response in an emotionally charged dilemma). High inter-annotator agreement (Fleiss' κ = 0.852).
- **Use for humanization:** Compact, rigorous, theory-grounded eval set. Better signal per $$$ than ad-hoc LLM-judge evals on EmpatheticDialogues.

## 12. Emo-gml/EmoBench-M — Multimodal EI Benchmark

- **URL:** https://github.com/Emo-gml/EmoBench-M
- **Stars:** ~133 ⭐
- **What it gives you:** 5,000+ video + audio + text samples across 13 scenarios, evaluated over three dimensions: Foundational Emotion Recognition (FER), Conversational Emotion Understanding (CEU), Socially Complex Emotion Analysis (SCEA). Headline finding: current MLLMs significantly lag humans on CEU and SCEA.
- **Use for humanization:** Use to ground claims like "our multimodal voice agent is more socially competent" in a reproducible number rather than cherry-picked demos.

## 13. CUHK-ARISE/EmotionBench — Empathy Response Evaluation

- **URL:** https://github.com/CUHK-ARISE/EmotionBench
- **Venue:** NeurIPS 2024
- **What it gives you:** 8 emotion types × 36 factors × 428 situations × 1,266 human references. Ships a 3-stage CLI: `emotionbench_run.py` → `emotionbench_eval.py` → `emotionbench_analyze.py`.
- **Use for humanization:** Most operationally complete empathy-eval harness — lets you plug in a model endpoint and get comparable numbers in one pass.

## 14. PennShenLab/MentalChat16K — Hybrid Real+Synthetic Dataset

- **URL:** https://github.com/PennShenLab/MentalChat16K
- **What it gives you:** 16,113 Q&A pairs: 6,338 from anonymized PISCES clinical-trial transcripts (behavioral-health coaches ↔ caregivers in palliative/hospice care) + 9,775 GPT-3.5-synthesized pairs over 33 mental-health topics. Evaluation uses GPT + Gemini as judges.
- **Use for humanization:** Rare example of *real clinical* empathy data at scale; particularly valuable for grief, caregiver-burnout, and end-of-life tones that synthetic data struggles with.

## 15. qiuhuachuan/smile (MeChat / SmileChat)

- **URL:** https://github.com/qiuhuachuan/smile
- **Stars / Venue:** ~526 ⭐ · EMNLP 2024 Findings · CC0-1.0
- **What it gives you:** The **SMILE** technique — use ChatGPT to *expand* single-turn Q&A into multi-turn dialogue, yielding ~55K multi-turn Chinese mental-health conversations. MeChat is the ChatGLM2-6B + LoRA fine-tune trained on it, grounded in CBT, motivational interviewing, and problem-solving.
- **Use for humanization:** SMILE is the most cost-effective trick in this list: if you have single-turn labeled empathy data, you can bootstrap multi-turn data without new human labels.

## 16. qiuhuachuan/PsyChat — Client-Centric Dialogue

- **URL:** https://github.com/qiuhuachuan/PsyChat
- **Stars / Venue:** ~62 ⭐ · CSCWD 2024 · MIT
- **What it gives you:** Dialogue system organized around *client-centric* techniques (CBT, motivational interviewing, solution-focused short-term therapy) rather than advisor-style responses. Inference code + HF model weights.
- **Use for humanization:** Worth reading alongside SoulChat/MeChat to see three different authoring teams converge on the same taxonomy of humane response moves.

## 17. X-D-Lab/MindChat — Four-Dimension Psychological LLM

- **URL:** https://github.com/X-D-Lab/MindChat
- **Stars / License:** ~707 ⭐ · GPL-3.0
- **Tagline:** *"MindChat (漫谈) — 心理大模型: 漫谈人生路, 笑对风霜途."*
- **What it gives you:** Covers 4 dimensions — counseling, assessment, diagnosis, treatment — across 0.5B–14B parameter variants on multiple bases (Baichuan-13B, ChatGLM2-6B, InternLM, Qwen). Includes MBTI classification and psychometric evaluation modules. Mobile / private-cloud / API deployment recipes.
- **Use for humanization:** The only repo in the list that ships genuinely small (0.5B) variants — useful if humanization has to run on-device or at low latency.

## 18. audeering/opensmile — Affective Audio Features

- **URL:** https://github.com/audeering/opensmile
- **Stars / License / Lang:** ~795 ⭐ · C++ · Python wrapper available
- **What it gives you:** The reference toolkit for low-level + mid-level speech affect features (eGeMAPS, ComParE, INTERSPEECH 2009–2013 affect-challenge feature sets). Runs real-time on Linux / Windows / macOS / Android / iOS / Raspberry Pi.
- **Use for humanization:** If humanization extends to voice output, use openSMILE on your TTS render to *measure* its prosodic affect and confirm it matches the intended emotional label.

## 19. tyiannak/pyAudioAnalysis — Python Audio Classification

- **URL:** https://github.com/tyiannak/pyAudioAnalysis
- **Stars / License:** ~6,236 ⭐ · Apache-2.0 · Python
- **What it gives you:** Feature extraction (MFCC, spectrogram, chromagram), supervised/unsupervised segmentation, classifiers (kNN/SVM/RF/extra-trees/gradient boosting), and regression. Published in PLoS One, widely used for speech emotion recognition and depression classification.
- **Use for humanization:** Lower-friction Python entry point than openSMILE for basic emotion classifiers on voice data.

## 20. speechbrain/speechbrain — Speech Toolkit with Emotion Recipes

- **URL:** https://github.com/speechbrain/speechbrain
- **Stars / License:** ~11,400 ⭐ · Apache-2.0 · PyTorch
- **What it gives you:** 200+ training recipes across 40+ datasets including `recipes/IEMOCAP/emotion_recognition`. Ships a wav2vec2-IEMOCAP checkpoint at 78.7% acc on HF (`speechbrain/emotion-recognition-wav2vec2-IEMOCAP`).
- **Use for humanization:** Best-maintained PyTorch path for training your own voice-emotion head on domain audio rather than shipping a generic classifier.

## 21. j-hartmann/emotion-english-distilroberta-base — The Default HF Classifier

- **URL:** https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
- **Stats:** 40M+ all-time downloads · 485 likes
- **What it gives you:** DistilRoBERTa fine-tune over 6 datasets (~20K balanced samples from Twitter, Reddit, student self-reports, TV dialogue) predicting Ekman-6 + neutral. Three-line `transformers` pipeline usage.
- **Use for humanization:** Lingua franca of text-emotion tagging — safe choice for a *monitor* on AI output. Pair with NRCLex for redundant labels when precision matters.

## 22. DemetersSon83/NRCLex — Lexicon-Based Text Emotion

- **URL:** https://github.com/DemetersSon83/NRCLex
- **What it gives you:** 10-emotion lexicon (anger, anticipation, disgust, fear, joy, sadness, surprise, trust, positive, negative) over ~27K words built on NRC + NLTK WordNet, wrapped on TextBlob. Exposes `top_emotions`, `affect_dict`, `affect_frequencies`.
- **Use for humanization:** Useful as a *deterministic* sanity check alongside neural classifiers — when model-based and lexicon-based disagree strongly, that itself is signal.

## 23. CUHK-ARISE / related — EmotionBench (see #13) + psychometric LLM evals

Grouped here: a thread of papers from CUHK-ARISE and collaborators (EmotionBench, PsyChat cross-evals, ACM IUI 2025 "LLMs and Emotional Intelligence" via psychometric tools) treat empathy as a *measurable psychometric construct* rather than a judge-style vibes check. Not a single repo, but a pattern worth tracking.

## 24. anuradha1992/llm-empathy-evaluation

- **URL:** https://github.com/anuradha1992/llm-empathy-evaluation
- **What it gives you:** Replication data + code for studies comparing expert vs crowdworker vs LLM (GPT-4o, Gemini 2.5 Pro, Claude 3.7 Sonnet) annotation of empathic communication — Cohen's Kappa (quadratic-weighted) + F1 across 21 empathy dimensions using EPITOME, EmpatheticDialogues, Perceived Empathy, Lend an Ear.
- **Use for humanization:** Directly answers "can we use an LLM to judge empathy?" — rare concrete agreement numbers rather than assertion.

## 25. passing2961/EmpGPT-3

- **URL:** https://github.com/passing2961/EmpGPT-3
- **What it gives you:** In-context empathetic dialogue generation with GPT-3, evaluated with EPITOME + EmoAcc + IntentAcc metrics. Includes EPITOME checkpoint setup.
- **Use for humanization:** Shows the *prompting-only* baseline — useful lower bound before you commit to fine-tuning anything.

## 26. FunAudioLLM/MME-Emotion — Multimodal EI Benchmark (Aug 2025)

- **URL:** https://github.com/FunAudioLLM/MME-Emotion; paper: [arXiv:2508.09210](https://arxiv.org/abs/2508.09210)
- **Stars / Venue:** Arxiv Aug 2025, updated Feb 2026 · Python
- **What it gives you:** 6,500 video clips with QA pairs across 27 scenario types and 8 emotional tasks. Evaluated 20 frontier MLLMs. Best model scores only 39.3% recognition / 56% CoT — the hardest open multimodal EI eval in the field. Generalist models (Gemini-2.5-Pro) and specialist models (R1-Omni) are profiled.
- **Use for humanization:** New standard for multimodal empathy evaluation, replacing EmoBench-M as the quantitative reference for claims about voice/video empathy capability.

## 27. JhCircle/Awesome-LLM-Empathy — Living Paper Registry (2025–2026)

- **URL:** https://github.com/JhCircle/Awesome-LLM-Empathy
- **What it gives you:** A curated, maintained list of papers on empathy in LMs covering theory, modeling, systems, emotion, and evaluation. Includes Kardia-R1 (WWW 2026), ReflectDiffu (ACL 2025), and HEART (2026). The fastest way to track new work without running a manual arXiv search.
- **Use for humanization:** Reference index to keep A-academic.md current. Check monthly.

## 28. NEU-DataMining/awesome-affective-computing — Affective Computing in the LLM Era (2025)

- **URL:** https://github.com/NEU-DataMining/awesome-affective-computing
- **What it gives you:** Overview of affective computing research as it intersects with LLMs — a bridge between the traditional sensing-focused affective computing literature and the new generation alignment-focused literature.
- **Use for humanization:** Useful background for any team trying to connect the openSMILE/SpeechBrain sensing stack with LLM-based empathy generation.

## 29. PERM (arXiv:2601.10532) — Psychology-grounded Empathetic Reward Model (Jan 2026)

- **URL:** https://arxiv.org/abs/2601.10532; code and dataset released via the paper
- **What it gives you:** An open RL reward model for empathy grounded in Empathy Cycle theory. Evaluates from three perspectives (supporter / seeker / bystander). Outperforms SOTA baselines by >10%; 70% preference in blind user study. Code and dataset publicly released.
- **Use for humanization:** Directly addresses the "no open DPO-against-empathy-benchmark pipeline" gap. First open resource to couple an empathy classifier with RL training for a generator in a principled way.

## 30. Kardia-R1 / KardiaBench (arXiv:2512.01282, WWW 2026)

- **URL:** https://arxiv.org/abs/2512.01282
- **What it gives you:** Rubric-as-Judge RL training framework for empathic dialogue, plus KardiaBench — 178,080 QA pairs across 22,080 multi-turn conversations anchored to 671 real user profiles. The largest purpose-built empathic support benchmark.
- **Use for humanization:** KardiaBench is currently the largest open multi-turn empathy eval. GRPO-based rubric reward approach is the 2025 replacement for EmPO/DPO SFT approaches.

---

## Patterns & Trends (updated April 2026)

1. **Chinese-language repos lead on volume, depth, and active maintenance.** SmartFlowAI/EmoLLM, SoulChat, MeChat/SMILE, PsyChat, MindChat, PsyQA, ChatPsychiatrist — the Chinese mental-health-LLM community has shipped more real fine-tunes, bigger corpora, and more variants than the English-language side. Any serious empathy work should mine these even if the target language is English.

2. **The dominant failure mode everyone names is the same:** LLMs rush to advice-giving, "universal suggestions," or solution-mode before listening. SoulChat, PsyChat, MeChat, CharacterChat, and ChatPsychiatrist all motivate their contributions in these terms, which is exactly the *humanization* failure mode.

3. **"Support strategy" is the most portable abstraction.** ESConv's 8-category strategy taxonomy (Questions, Affirmation, Self-disclosure, Reflection, Restatement, Providing Suggestions, Information, Other) reappears, with variants, in PsyQA, PsyChat, MeChat, and ChatPsychiatrist. Conditioning generation on a predicted strategy is the most repeated pattern across teams.

4. **Persona + memory + matching is the next frontier.** CharacterChat (MBTI-1024 + dispatcher), MindChat (MBTI module), and the psychometric-eval thread (EmotionBench, SECEU references) all converge on the idea that empathy is *relational*, not absolute — you need the right supporter for this user, not a maximally empathetic bot.

5. **Data bootstrapping via GPT/ChatGPT expansion is mainstream.** SMILE (single-turn → multi-turn), ChatPsychiatrist (GPT-4 extractor/filter), MentalLLaMA (ChatGPT explanations), MentalChat16K (GPT-3.5 synthetic). Pure human-labeled empathy corpora are rare; hybrid real+synthetic is the norm. Budget for an eval step that catches GPT's own mannerisms leaking into your data.

6. **Eval is fragmenting productively.** EmoBench (text-psychometric), EmoBench-M (multimodal-psychometric), EmotionBench (empathy-response), EPITOME (expressed empathy in replies), llm-empathy-evaluation (human↔LLM-judge agreement) — no single benchmark dominates, but together they let you triangulate.

7. **Voice affect is underused in LLM humanization.** openSMILE, pyAudioAnalysis, SpeechBrain, Emotion-LLaMA are mature, but almost no "humanizer" products pipe through them. Open whitespace.

## Gaps (updated April 2026)

- **Open DPO-against-empathy pipeline now exists, but is RL-only.** PERM (arXiv:2601.10532) and Kardia-R1 (arXiv:2512.01282) both publish open reward models for RL training. A pure DPO pipeline against EmoBench remains unpublished, but the RL path is now well-trodden.
- **Underserved tones.** Caregiver burnout and grief are covered only by MentalChat16K; anger/rage, awkwardness, embarrassment, and joy-without-sycophancy are largely absent from the empathy corpora — they're all tuned for distress support.
- **Strategy taxonomy drift.** ESConv, PsyQA, PsyChat, MeChat all use *slightly different* strategy labels. No crosswalk has been published. HEART (2026) introduces five new dimensions (H/E/A/R/T) that partially overlap with ESConv's 8-strategy taxonomy without aligning them.
- **No open repo explicitly targets "make generic assistant output sound more human."** All the empathy repos target mental-health support as the application. For a humanization product, the correct move is to borrow the *corpora and strategies* but build your own smaller, broader tone dataset.
- **Evaluation trust gap.** llm-empathy-evaluation shows LLM judges partly agree with humans on empathy but diverge on subtler dimensions — implying "GPT-4 as judge" evals should always be paired with at least one deterministic anchor. MME-Emotion adds a new finding: multimodal LLMs are far weaker than text-only models at EI in video contexts (best = 39.3%), so multimodal claims require specifically multimodal eval.
- **Multimodal empathy gap.** Emotion-LLaMA (NeurIPS 2024) was the best open reference for multimodal emotion grounding. MME-Emotion (Aug 2025) shows that even frontier models score poorly on video-based EI. The gap between text empathy and multimodal empathy in open models is large and largely unaddressed.

## Sources

- https://github.com/SmartFlowAI/EmoLLM — EmoLLM repo and README.
- https://github.com/lzw108/EmoLLMs — EmoLLMs affective analysis LLM family.
- https://github.com/scutcyr/SoulChat — SoulChat ZH empathetic dialogue LLM (EMNLP 2023 Findings).
- https://github.com/morecry/CharacterChat — MBTI-1024 personalized social support (arXiv 2308.10278).
- https://github.com/ZebangCheng/Emotion-LLaMA — Multimodal emotion-reasoning LLaMA (NeurIPS 2024).
- https://github.com/facebookresearch/EmpatheticDialogues — Foundational 25K empathy dataset (archived 2023).
- https://github.com/thu-coai/Emotional-Support-Conversation — ESConv, support-strategy taxonomy (ACL 2021).
- https://github.com/thu-coai/PsyQA — ZH long-form counseling dataset (ACL 2021 Findings).
- https://github.com/EmoCareAI/ChatPsychiatrist — ChatCounselor + Psych8K (CIKM 2023).
- https://github.com/SteveKGYang/MentalLLaMA — Interpretable mental-health analysis (WWW 2024).
- https://github.com/Sahandfer/EmoBench — Text EI benchmark (ACL 2024).
- https://github.com/Emo-gml/EmoBench-M — Multimodal EI benchmark.
- https://github.com/CUHK-ARISE/EmotionBench — Empathy response benchmark (NeurIPS 2024).
- https://github.com/PennShenLab/MentalChat16K — Real+synthetic mental-health corpus.
- https://github.com/qiuhuachuan/smile — SMILE single→multi-turn expansion + MeChat.
- https://github.com/qiuhuachuan/PsyChat — Client-centric dialogue system (CSCWD 2024).
- https://github.com/X-D-Lab/MindChat — 4-dimension psychological LLM, 0.5B–14B variants.
- https://github.com/audeering/opensmile — C++ speech affect feature toolkit.
- https://github.com/tyiannak/pyAudioAnalysis — Python audio analysis + classifiers (PLoS One).
- https://github.com/speechbrain/speechbrain — PyTorch speech toolkit incl. IEMOCAP emotion recipes.
- https://huggingface.co/j-hartmann/emotion-english-distilroberta-base — HF default text-emotion classifier.
- https://github.com/DemetersSon83/NRCLex — NRC-lexicon Python emotion scorer.
- https://github.com/anuradha1992/llm-empathy-evaluation — Human↔LLM empathy-annotation agreement study.
- https://github.com/passing2961/EmpGPT-3 — In-context empathetic dialogue baseline w/ EPITOME.
- https://github.com/FunAudioLLM/MME-Emotion — Multimodal EI benchmark, 6,500 clips, 8 tasks (arXiv:2508.09210).
- https://github.com/JhCircle/Awesome-LLM-Empathy — Living registry of empathy-in-LMs papers.
- https://github.com/NEU-DataMining/awesome-affective-computing — Affective computing in the LLM era overview.
- https://arxiv.org/abs/2601.10532 — PERM: Psychology-grounded Empathetic Reward Modeling.
- https://arxiv.org/abs/2512.01282 — Kardia-R1 + KardiaBench, RL-based empathic support framework (WWW 2026).
- https://github.com/scutcyr/SoulChat2.0 — SoulChat2.0: digital twin for psychological counselors.
