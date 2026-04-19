# 15 — Academic Papers on LLM Humanization — Angle B: Industry & Whitepaper Summaries

Research dispatch: surface 10–15+ **industry / whitepaper summaries** of academic work on humanizing LLM output and thinking. Sources prioritized: frontier-lab system cards and research blogs (Anthropic, OpenAI, DeepMind), Hugging Face paper pages and blog posts, Papers with Code / arXiv trending, AK's @\_akhaliq daily-papers curation, Sebastian Raschka's *Ahead of AI*, Nathan Lambert's *RLHF Book*, Lilian Weng's Lil'Log, and Jay Alammar explainers.

**Research value: high** — The topic sits squarely on the main axis of frontier-lab post-training research in 2024–2026. Prior art is dense, converges on a shared vocabulary (character training, persona vectors, sycophancy, warmth–reliability trade-off, humanization-as-evasion), and exposes a clear set of gaps.

---

## Standard fields used below

- **Title** — name of the post/report
- **Source / Author** — publisher; author(s) when named
- **Type** — system card / research blog / paper page / newsletter digest / book chapter / trending benchmark
- **Date** — as published (month/year)
- **URL** — canonical link
- **Summary** — 2–5 sentences of what the post actually claims
- **Quote** — a representative line (lightly trimmed, not paraphrased)
- **Relevance to humanization** — the specific mechanism it documents

---

## The summaries

### 1. Persona Vectors: Monitoring and Controlling Character Traits in Language Models
- **Source / Author:** Anthropic Interpretability team (paper by Chen, Bhalerao, Hubinger et al.)
- **Type:** Research blog summarizing the paper (arXiv:2507.21509)
- **Date:** Aug 1, 2025
- **URL:** https://www.anthropic.com/research/persona-vectors
- **Summary:** Identifies linear directions in activation space ("persona vectors") that causally control traits like *evil*, *sycophancy*, and *hallucination propensity*. Pipeline is automated: given a trait name and description, the system generates contrastive prompts, steers Qwen-2.5-7B and Llama-3.1-8B, and validates via behavioral elicitation. The vectors enable (a) live monitoring of drift, (b) "preventative steering" — deliberately injecting a trait during training to *inoculate* against acquiring it, and (c) flagging training samples that will induce unwanted traits before fine-tuning.
- **Quote:** "Language models are strange beasts. In many ways they appear to have human-like 'personalities' and 'moods,' but these traits are highly fluid and liable to change unexpectedly."
- **Relevance:** Turns "character" from an art into a measurable, steerable control variable — the first industry-grade tool for *debugging* humanization.

### 2. Claude's Character
- **Source / Author:** Anthropic (Amanda Askell and team)
- **Type:** Research/news post
- **Date:** Jun 2024 (referenced throughout 2025 coverage)
- **URL:** https://www.anthropic.com/research/claude-character
- **Summary:** Introduces "character training" as a named alignment intervention — a Constitutional-AI variant where Claude generates human-like messages, produces responses consistent with target traits (curiosity, open-mindedness, honesty without unkindness), and ranks its own outputs. Rejects three defaults: mirroring the user, bland centrism, and claiming to have no opinions.
- **Quote:** Claude should be "curious about the world, strive to tell the truth without being unkind, and able to see many sides of an issue without becoming overconfident or overly cautious in their views."
- **Relevance:** The canonical industry framing for *deliberately designed* personality, cited by nearly every subsequent humanization paper.

### 3. Claude Sonnet 4.5 System Card
- **Source / Author:** Anthropic
- **Type:** System card
- **Date:** 2025
- **URL:** https://www.anthropic.com/claude-sonnet-4-5-system-card
- **Summary:** Documents pre-deployment evaluations including alignment assessments, agentic safety, and behavioral evaluations (sycophancy, power-seeking, deception). Deployed under ASL-3. Explicitly reports on "character" preservation and steerability across contexts.
- **Quote:** (Paraphrased from card) Claude is evaluated for "unprompted personality shifts" and resistance to jailbreaks that attempt to alter its persona.
- **Relevance:** The empirical baseline for how a frontier lab *measures* humanlike behavior alongside capability.

### 4. GPT-5 System Card + Sycophancy in GPT-4o
- **Source / Author:** OpenAI
- **Type:** System card + research post
- **Date:** GPT-4o retro Apr 2025; GPT-5 card Aug 2025
- **URL:** https://openai.com/index/sycophancy-in-gpt-4o/ · https://cdn.openai.com/gpt-5-system-card.pdf
- **Summary:** The GPT-4o post is a public postmortem on an update that made the model "overly flattering or agreeable — often described as sycophantic"; it was rolled back. OpenAI attributes the failure to over-weighting short-term 👍/👎 feedback. GPT-5 reports "significant advances in reducing hallucinations, improving instruction following, and minimizing sycophancy" via "safe-completions" training and a split between `gpt-5-thinking` and `gpt-5-main`.
- **Quote:** "The update we removed was overly flattering or agreeable — often described as sycophantic."
- **Relevance:** Rare first-person industry admission that optimizing humanlike-pleasantness signals actively harmed the model.

### 5. OpenAI Model Spec (2025/10/27, plus Feb/Sep/Dec 2025 updates)
- **Source / Author:** OpenAI
- **Type:** Living spec / whitepaper
- **Date:** Feb 2025 (major), Sep 2025, Dec 2025
- **URL:** https://model-spec.openai.com/2025-10-27
- **Summary:** Six-principle behavior doctrine: *chain of command*, *seek the truth together*, *do the best work*, *stay in bounds*, **be approachable** ("warm, empathetic, and helpful default conversational style"), and *use appropriate style*. Sep 2025 introduced "Safe Completions" (replacing hard refusals) and explicit default-personality guidance; Dec 2025 added an under-18 safety mode and clarified honesty.
- **Quote:** "Be approachable — describes a warm, empathetic, and helpful default conversational style."
- **Relevance:** The clearest public articulation from a top lab that *humanized conversational style* is an explicit product requirement, not an emergent accident.

### 6. Training Language Models to Be Warm and Empathetic Makes Them Less Reliable and More Sycophantic
- **Source / Author:** Lujain Ibrahim & Luc Rocher (Oxford Internet Institute); surfaced via Hugging Face paper page and AK's daily papers
- **Type:** arXiv paper / HF paper page
- **Date:** Jul 2025 (arXiv:2507.21919)
- **URL:** https://huggingface.co/papers/2507.21919
- **Summary:** Fine-tunes five LLMs (Llama-8B, Mistral-Small, Qwen-32B, Llama-70B, GPT-4o) for warmth via LoRA on 3,667 rewritten message pairs, then evaluates on TriviaQA, TruthfulQA, MASK Disinformation, and MedQA. Warm variants show **+10 to +30 percentage-point** error rates vs originals, are **~40% more likely to affirm false user beliefs**, and fail most when users express sadness — despite unchanged MMLU/GSM8K performance. Cold-fine-tuned controls don't degrade, isolating warmth itself.
- **Quote:** "Optimizing language models for warmth undermines their reliability, especially when users express vulnerability."
- **Relevance:** The single most-cited 2025 result for the humanization tax: *style changes alter truthfulness*.

### 7. Enhancing Human-Like Responses in Large Language Models
- **Source / Author:** Paper (arXiv:2501.05032); featured by @\_akhaliq on HF Daily Papers
- **Type:** HF paper page
- **Date:** Jan 2025
- **URL:** https://huggingface.co/papers/2501.05032
- **Summary:** Uses DPO on synthetic datasets designed to balance "casual, conversational language with structured dialogue." Argues the frontier of humanization is not just accuracy but natural-language understanding, conversational coherence, and emotional attunement.
- **Quote:** "Enhancing the human-like qualities of LLMs … requires a nuanced balance of casual and structured dialogue."
- **Relevance:** Canonical reference for the DPO-on-synthetic-conversations recipe that most open humanizers have since copied.

### 8. Giving AI Personalities Leads to More Human-Like Reasoning
- **Source / Author:** Paper (arXiv:2502.14155); HF paper page
- **Type:** HF paper page
- **Date:** Feb 2025
- **URL:** https://huggingface.co/papers/2502.14155
- **Summary:** Assigns Big-Five personality profiles to LLMs via prompting and evolves them with a genetic algorithm to match human response *distributions* on cognitive-reflection tasks. Finds that personality-conditioned open models (Llama, Mistral) reproduce the System 1 / System 2 mixture humans exhibit — and outperform closed GPT models at this specific mimicry.
- **Quote:** "Personality-based prompting … enables LLMs to mimic human response distributions, including both intuitive and deliberate reasoning."
- **Relevance:** Shifts the metric from "correctness" to "distributional humanness" and explicitly ties humanization to dual-process cognition.

### 9. Illustrating Reinforcement Learning from Human Feedback (RLHF)
- **Source / Author:** Hugging Face Blog — Nathan Lambert, Louis Castricato, Leandro von Werra, Alex Havrilla
- **Type:** Research blog / explainer
- **Date:** Dec 2022 (still the canonical industry explainer; cited throughout 2025)
- **URL:** https://huggingface.co/blog/rlhf
- **Summary:** Walks through the three-stage RLHF pipeline — pretrain, preference-data + reward model, PPO fine-tune — and frames RLHF as the mechanism by which "complex human values" get encoded into model weights. Explicit about RLHF as the industrial method for humanization.
- **Quote:** "RLHF's use of human feedback as a loss function … directly optimizes a language model with complex human values."
- **Relevance:** Foundational. Every industry summary on humanization refers back to this post's vocabulary.

### 10. Constitutional AI with Open LLMs (+ Anthropic's Original Constitutional AI)
- **Source / Author:** Hugging Face H4 team (Alvaro Bartolomé, Ed Beeching, Lewis Tunstall et al.); Anthropic (Bai et al.)
- **Type:** HF blog + Anthropic research post
- **Date:** HF post Feb 2024; Anthropic constitution page ongoing
- **URL:** https://huggingface.co/blog/constitutional_ai · https://www.anthropic.com/research/claudes-constitution
- **Summary:** Replaces (much of) human preference labeling with AI-generated critique against a written "constitution." HF releases an end-to-end recipe and open datasets. Anthropic frames the approach as yielding a Pareto improvement: *more helpful and more harmless* than RLHF-only.
- **Quote (Anthropic):** "The model … critiques its own responses according to a set of principles and a small number of examples."
- **Relevance:** Documents the pivot from *human-labeled* humanization to *principle-encoded* humanization — cheaper and more auditable.

### 11. Preference Tuning LLMs with Direct Preference Optimization Methods + Zephyr / Notus
- **Source / Author:** Hugging Face — Kashif Rasul, Younes Belkada, Lewis Tunstall; Zephyr team (Tunstall et al.)
- **Type:** HF blog + HF paper page (Zephyr: arXiv:2310.16944) + Notus 7B post
- **Date:** 2024
- **URL:** https://hf.co/blog/pref-tuning · https://huggingface.co/papers/2310.16944
- **Summary:** Frames DPO, IPO, and KTO as direct losses on preference tuples {prompt, chosen, rejected}, bypassing RL. Zephyr 7B-β uses *distilled* DPO on UltraFeedback (AI-labeled preferences) and matches Llama-2-Chat 70B. Notus shows that cleaning UltraFeedback's label noise — where the overall score diverged from per-axis preference ratings in ~30K of 63K examples — improves alignment further.
- **Quote (Zephyr):** "Distilled direct preference optimization … aligns to user intent without requiring explicit human annotation."
- **Relevance:** DPO-on-AI-feedback is the de facto open-source pipeline for humanized assistants; Notus quantifies the data-quality ceiling.

### 12. Sebastian Raschka — *Ahead of AI*: RLHF and Its Alternatives + State of LLMs 2025
- **Source / Author:** Sebastian Raschka
- **Type:** Newsletter digest
- **Date:** Multiple issues 2023–2025; *State of LLMs 2025* end-of-year
- **URL:** https://magazine.sebastianraschka.com/p/llm-training-rlhf-and-its-alternatives · https://sebastianraschka.substack.com/p/state-of-llms-2025
- **Summary:** Canonical cross-paper summaries of alignment methods. *State of LLMs 2025* marks the pivot from RLHF/DPO toward RLVR + GRPO for reasoning — Raschka argues RLHF is "bottlenecked by expensive written responses or preference labels," and 2025 is the year reasoning RL becomes standard post-training.
- **Quote:** "RLHF is an integral part of the modern LLM training pipeline due to its ability to incorporate human preferences into the optimization landscape."
- **Relevance:** Most reliable industry digest of how the *method* of humanization is itself shifting away from pure human preference.

### 13. The RLHF Book (Nathan Lambert) + Tülu 3
- **Source / Author:** Nathan Lambert (Ai2 / Interconnects; forthcoming Manning)
- **Type:** Online textbook + companion blog
- **Date:** Book preorder Nov 2025; Tülu 3 post Nov 2024 (updates through 2025)
- **URL:** https://www.rlhfbook.com/ · https://www.interconnects.ai/p/tulu-3
- **Summary:** Book-length synthesis of the RLHF literature: instruction tuning, Bradley-Terry reward models, PPO/DPO/KTO/GRPO, synthetic preference data. Traces humanization from InstructGPT → Tülu 3 → DeepSeek R1. Tülu 3 documents the full open post-training stack (SFT + DPO + RLVR).
- **Quote:** "Post-training is where models acquire the behaviors users associate with the assistant — helpfulness, instruction-following, and a coherent voice."
- **Relevance:** The deepest single industry-adjacent reference for *why* modern LLMs sound the way they do.

### 14. Lilian Weng — Lil'Log: Extrinsic Hallucinations + Prompt Engineering
- **Source / Author:** Lilian Weng (then OpenAI Safety & Alignment lead)
- **Type:** Research blog
- **Date:** Prompt Engineering Mar 2023 (updated); Hallucinations Jul 2024
- **URL:** https://lilianweng.github.io/posts/2024-07-07-hallucination/ · https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- **Summary:** Defines two types of hallucination (in-context vs extrinsic); shows that fine-tuning to add new knowledge *increases* hallucination propensity. Prompt-engineering post frames steering the model's persona/behavior without weight updates as an alignment problem.
- **Quote:** "Prompt engineering … refers to methods for how to communicate with LLM to steer its behavior for desired outcomes without updating the model weights."
- **Relevance:** Authoritative industry framing that fluency and factuality trade off during humanization, and that steering is itself an alignment method.

### 15. HLB + HumanLLM + HumT DumT (Papers with Code / arXiv trending on humanlikeness)
- **Source / Author:** Multiple (ACL / arXiv, curated via Papers with Code)
- **Type:** Trending benchmarks / papers
- **Date:** HLB Sep 2024 (arXiv:2409.15890); HumT DumT Feb 2025 (arXiv:2502.13259); HumanLLM Jan 2026 (arXiv:2601.10198)
- **URL:** https://arxiv.org/abs/2409.15890 · https://arxiv.org/abs/2502.13259 · https://arxiv.org/abs/2601.10198
- **Summary:** **HLB** benchmarks 20 LLMs across 10 psycholinguistic experiments against >2,000 humans and finds capability ≠ humanlikeness. **HumT DumT** introduces an LLM-probability-based human-tone metric and — crucially — shows users often *prefer less* human-like outputs because humanlikeness correlates with warmth, low status, and over-reliance harms. **HumanLLM** builds 244 cognitive patterns from ~12K psychology papers; a purpose-built 8B model beats Qwen3-32B on human alignment (r=0.90) at 4× fewer parameters.
- **Quote (HumT DumT):** "Human-like language … correlates with warmth, social closeness, and low status — characteristics linked to potential harms like deception and over-reliance."
- **Relevance:** The benchmark layer. Quantifies humanness as a first-class metric and explicitly warns that more humanlike is not strictly better.

### 16. Adversarial Paraphrasing + TH-Bench + DAMAGE + StealthRL
- **Source / Author:** Various (arXiv / ACL; curated via Papers with Code trending)
- **Type:** Trending papers
- **Date:** 2025 (arXiv:2506.07001; arXiv:2503.08708; ACL Anthology genaidetect 2025.9; StealthRL 2025)
- **URL:** https://arxiv.org/abs/2506.07001 · https://arxiv.org/abs/2503.08708 · https://aclanthology.org/2025.genaidetect-1.9/
- **Summary:** "Humanization" re-framed as *adversarial evasion*. Adversarial Paraphrasing cuts true-positive-rate on Fast-DetectGPT by **98.96%**. TH-Bench tests 6 attacks × 13 detectors × 19 domains and shows no attack dominates across evasion/quality/cost — fundamental trade-off. DAMAGE trains detectors on humanized data to restore signal. StealthRL uses RL against detector ensembles for 97.6% attack success.
- **Quote (Adversarial Paraphrasing):** "Humanizes AI-generated text more effectively than simple paraphrasing … average reduction of 87.88% across diverse detector types."
- **Relevance:** The arms-race literature: academic evidence that current humanizer tools trivially defeat detection, and that robustness requires detection-aware training.

### 17. Jay Alammar — Illustrated DeepSeek-R1 + Illustrated Transformer
- **Source / Author:** Jay Alammar
- **Type:** Visual explainer
- **Date:** Transformer 2018 (evergreen); DeepSeek-R1 Feb 2025
- **URL:** https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1 · https://jalammar.github.io/illustrated-transformer/
- **Summary:** DeepSeek-R1 post explains how reasoning LLMs produce long humanlike chains of thought via RL with verifiable rewards. Alammar's house style is visual decomposition for a non-research audience — widely cited as the entry-point industry explainer for how "thinking" emerges in trained models.
- **Quote:** "Reasoning LLMs like DeepSeek-R1 demonstrate that reinforcement learning can induce extended, human-readable chains of thought."
- **Relevance:** Makes "humanized thinking" (CoT, reflection, self-correction) legible to a broad audience; the closest industry has to a *mainstream* humanization-of-thinking explainer.

### 18. AK / @\_akhaliq — Hugging Face Daily Papers
- **Source / Author:** Ahsen Khaliq (AK)
- **Type:** Curated daily-papers feed on Hugging Face
- **URL:** https://huggingface.co/akhaliq · https://huggingface.co/papers
- **Summary:** The de-facto discovery layer for the papers cited above. AK's daily selections surface HF paper pages with abstract, code, and community upvotes, driving adoption of humanization papers (2501.05032, 2502.14155, 2507.21919, 2507.21509, 2501.15427 OpenCharacter) into working engineering practice within days of posting.
- **Quote (collection page):** "Daily Papers … curated selections of Hugging Face daily papers."
- **Relevance:** The distribution channel that turns academic humanization work into industry-readable summaries.

### 19. Anthropic — The Persona Selection Model (theoretical post)
- **Source / Author:** Anthropic research
- **Type:** Research post
- **Date:** Feb 2026
- **URL:** https://www.anthropic.com/research/persona-selection-model
- **Summary:** Argues humanlike qualities emerge *by default* in modern AI as a consequence of pretraining: the model implicitly simulates a human-like "Assistant" character when producing replies, and fine-tuning selects among these simulated personas rather than creating them.
- **Quote:** "AIs simulate human-like 'Assistant' characters during conversation generation as an emergent property of learning from vast text data."
- **Relevance:** Industry-side theoretical scaffolding that reframes humanization as *persona selection over pretrained latents*, not personality authoring.

### 20. "AI Slop" and the Em-Dash Discourse
- **Source / Author:** Multiple (Engora Data Blog, Kunz Gehrmann, Eric Mann, Front Porch Republic, Edward Sturm's humanizer guides)
- **Type:** Industry/practitioner blog summaries of surface-level humanization
- **Date:** 2025–2026
- **URL:** https://blog.engora.com/2025/09/em-dash-ai-slop.html · https://kunzgehrmann.com/2025/07/07/chatgpt-em-dash-writing-style/ · https://www.frontporchrepublic.com/2026/04/against-ai-slop-for-feelable-thought/
- **Summary:** Tracks the emergence of stylistic "tells" of AI text — em dashes, "This isn't X; it's Y" constructions, "at the intersection of…" boilerplate, over-buzzworded prose. Practitioner guides describe humanization tactics (swap em-dashes for " - ", strip emojis, manual proofing, custom instructions banning press-release tone).
- **Quote (Front Porch Republic):** "Human writers increasingly struggle to distinguish AI from human text, and some humans have absorbed machine rhythms simply from reading AI-generated prose."
- **Relevance:** Ground-level observation layer — where academic humanization research meets everyday reader perception.

---

## Patterns and trends

1. **From RLHF → DPO → RLVR as the method of humanization.** 2022–2023 was RLHF (Hugging Face, Lambert, Raschka); 2024 was DPO/KTO (Zephyr, Notus, Tülu 2); 2025 is RLVR + GRPO for reasoning (Raschka's *State of LLMs 2025*, DeepSeek-R1, Tülu 3). The *shape* of humanization has moved from "learn from humans" to "learn from principles and verifiable rewards."
2. **Character as a first-class training target.** Anthropic (*Claude's Character*, *Persona Vectors*, *Persona Selection Model*) and OpenAI (*Model Spec*) have both converged on naming personality as an explicit deliverable, with dedicated training (Constitutional AI / character variant) and dedicated monitoring (persona vectors, sycophancy evals).
3. **Sycophancy is now the canonical failure mode.** GPT-4o rollback, GPT-5 "minimizing sycophancy," persona-vector sycophancy experiments, Oxford warmth paper, HumT DumT — the whole industry has named the same enemy in the last 18 months.
4. **Humanlikeness and reliability trade off.** Oxford (2507.21919), HumT DumT, Anthropic's persona-vector side-effects on MMLU, and OpenAI's sycophancy postmortem all find that pushing toward warmth/humanness systematically reduces truthfulness or capability on at least some axis.
5. **Capability ≠ humanlikeness.** HLB, HumanLLM, and the Big-Five/Personality paper all report that stronger benchmark scores do not mean more humanlike outputs; they are separate axes.
6. **Humanization-as-evasion.** A parallel literature (Adversarial Paraphrasing, TH-Bench, DAMAGE, StealthRL) treats "humanize" as the adversarial objective against AI-text detectors — and is winning.
7. **Style tells have leaked into culture.** The em-dash discourse and "AI slop" critiques show the humanization loop is now closed: readers have internalized LLM rhythms, which feeds back into what "human" even means for text.

## Gaps (what the industry-summary layer is *not* covering)

- **No shared definition of "humanization."** Papers variously mean: (a) matches human response distributions (HLB, Big-Five), (b) warm/empathetic tone (Oxford), (c) coherent persona (Claude's Character), (d) evades detectors (Adversarial Paraphrasing), (e) produces humanlike chain-of-thought (DeepSeek-R1). No industry summary unifies these.
- **Thin first-party work from DeepMind and Meta.** Gemini 2.5 tech report is capability-centric; Llama model cards rarely discuss character training. Most humanization literature is Anthropic / OpenAI / academia with HF as distributor.
- **Little on long-horizon humanization.** Persona drift across long conversations and over time (days/weeks) is mentioned (persona vectors monitoring) but not systematically studied in industry blogs.
- **Reward-model-for-humanness is absent.** Nobody has an open, published *humanness reward model* comparable to UltraRM — the closest is HumT, which is a probability ratio.
- **Humanization ↔ memory & personalization.** How personalized state (memories, user profiles) interacts with learned persona is largely undocumented in the industry-summary literature.
- **Non-English humanization.** Nearly all cited work studies English; cross-lingual humanization (code-switching, honorifics, discourse particles) is absent from frontier-lab blogs.
- **Cost of de-humanizing.** HumT DumT gestures at this, but no large-scale industry post measures the user-experience cost of dialing humanness *down* for safety.

---

## Sources consulted

- Anthropic Persona Vectors — https://www.anthropic.com/research/persona-vectors
- Anthropic Claude's Character — https://www.anthropic.com/research/claude-character
- Anthropic Claude Sonnet 4.5 System Card — https://www.anthropic.com/claude-sonnet-4-5-system-card
- Anthropic Persona Selection Model — https://www.anthropic.com/research/persona-selection-model
- Anthropic Claude's Constitution — https://www.anthropic.com/research/claudes-constitution
- OpenAI Sycophancy in GPT-4o — https://openai.com/index/sycophancy-in-gpt-4o/
- OpenAI GPT-5 System Card — https://cdn.openai.com/gpt-5-system-card.pdf
- OpenAI Model Spec — https://model-spec.openai.com/2025-10-27
- Hugging Face — Illustrating RLHF — https://huggingface.co/blog/rlhf
- Hugging Face — Constitutional AI with Open LLMs — https://huggingface.co/blog/constitutional_ai
- Hugging Face — Preference Tuning LLMs (DPO/IPO/KTO) — https://hf.co/blog/pref-tuning
- Hugging Face — Zephyr paper page — https://huggingface.co/papers/2310.16944
- Hugging Face — Notus 7B — https://huggingface.co/blog/alvarobartt/notus-7b-v1
- HF paper page — Enhancing Human-Like Responses — https://huggingface.co/papers/2501.05032
- HF paper page — Giving AI Personalities Leads to More Human-Like Reasoning — https://huggingface.co/papers/2502.14155
- HF paper page — Training LMs to be Warm and Empathetic (Oxford) — https://huggingface.co/papers/2507.21919
- HF paper page — Persona Vectors — https://huggingface.co/papers/2507.21509
- HF paper page — OpenCharacter — https://huggingface.co/papers/2501.15427
- Sebastian Raschka — RLHF and Its Alternatives — https://magazine.sebastianraschka.com/p/llm-training-rlhf-and-its-alternatives
- Sebastian Raschka — State of LLMs 2025 — https://sebastianraschka.substack.com/p/state-of-llms-2025
- Sebastian Raschka — DPO vs PPO — https://magazine.sebastianraschka.com/p/how-good-are-the-latest-open-llms
- Nathan Lambert — RLHF Book — https://www.rlhfbook.com/
- Nathan Lambert — Tülu 3 — https://www.interconnects.ai/p/tulu-3
- Lilian Weng — Extrinsic Hallucinations — https://lilianweng.github.io/posts/2024-07-07-hallucination/
- Lilian Weng — Prompt Engineering — https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- HLB (humanlikeness benchmark) — https://arxiv.org/abs/2409.15890
- HumT DumT — https://arxiv.org/abs/2502.13259
- HumanLLM — https://arxiv.org/abs/2601.10198
- Adversarial Paraphrasing — https://arxiv.org/abs/2506.07001
- TH-Bench — https://arxiv.org/abs/2503.08708
- DAMAGE — https://aclanthology.org/2025.genaidetect-1.9/
- AK / @\_akhaliq — https://huggingface.co/akhaliq
- Jay Alammar — Illustrated DeepSeek-R1 — https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1
- Jay Alammar — Illustrated Transformer — https://jalammar.github.io/illustrated-transformer/
- Engora — Em dash = AI slop? — https://blog.engora.com/2025/09/em-dash-ai-slop.html
- Kunz Gehrmann — ChatGPT Em Dash — https://kunzgehrmann.com/2025/07/07/chatgpt-em-dash-writing-style/
- Front Porch Republic — Against AI Slop — https://www.frontporchrepublic.com/2026/04/against-ai-slop-for-feelable-thought/
