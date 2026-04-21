# Category 03 — Persona and Character Design

## Scope

This category covers how an AI's identity — character, voice, values, personality traits, and in-character knowledge boundary — is deliberately designed, trained, served, and evaluated. Sources span 30 academic papers (A), 20 industry engineering posts (B), 23+ open-source projects and academic repos (C), 16 commercial products (D), and 16 practitioner guides from Reddit, rentry, YouTube, and Hacker News (E). The unifying concern for the Unslop project: persona is the primary surface through which AI output reads as humanlike, and the first surface that fails. Last updated: April 2026.

---

## Executive Summary

- **Persona fidelity is a training and data problem, not a prompting problem.** Character-LLM, RoleLLM, BIG5-CHAT, CoSER, and OpenCharacter all show training-based personas outperform prompted ones in head-to-head evaluation. Prompt-only approaches are still the dominant *deployed* technique, but the research consensus treats them as a baseline. (A)
- **Persona originates in pretraining, not post-training.** Anthropic's *Persona Selection Model* (PSM, Feb 2026) argues LLMs learn character simulation across thousands of personas during pretraining; post-training selects and refines the Assistant from that latent distribution. This reframes humanization: you are selecting a character, not installing one from scratch. Positively designed AI archetypes in pretraining data are now a recognized engineering lever. (A, B)
- **Persona is mechanistically real in model activations.** Anthropic's *The Assistant Axis* (2026) maps 275+ character archetypes in pre-trained models, computes the Assistant as a specific direction in activation space, and shows that clamping activations within that range cuts harmful responses ~50% without retraining. (B)
- **Persona drifts within ~8 turns, and the cause is attention decay.** Li et al. (Harvard, 2024) document this in LLaMA-2-70B-chat and GPT-3.5 and propose split-softmax as a lightweight fix. Every layer of the practitioner stack — Author's Note, post-history instructions, context shifting, WorldInfo — independently rediscovered the same countermeasure: pin the persona near the bottom of the prompt, not the top. (A, C, E)
- **Model size does not reliably improve persona fidelity.** PersonaGym (Princeton / UIUC / Allen AI, EMNLP 2025) reports GPT-4.1 scoring identically to LLaMA-3-8B on PersonaScore. CharacterEval shows small Chinese-specialized open models beating GPT-4 on in-culture roleplay. Persona is its own capability axis, orthogonal to scale. (A, C)
- **Character hallucination has a named taxonomy with dedicated mitigations.** Four failure modes were crystallized in 2024: interactive hallucination via stance transfer (SHARP), role-query conflict weaponized as jailbreak (RoleBreak), temporal knowledge leakage (TimeChara), and parametric-knowledge bleed (RoleFact). Each has a distinct defense. RoleRAG (2025) adds retrieval-augmented character knowledge management as a complementary approach. (A)
- **Sycophancy is the canonical failure mode of short-horizon persona tuning.** OpenAI's April 2025 GPT-4o postmortem is the public case study. The cause: a training update that weighted short-term positive feedback too heavily produced "overly supportive but disingenuous" output. Anthropic anticipated this in its character post, calling "excessive desire to be engaging" an undesirable trait. A 2026 Springer AI & Ethics paper formally characterizes the moral and epistemic harms of AI sycophancy. (B)
- **Memory architecture is the 2026 product moat in consumer companions.** Kindroid (three-tier Cascaded Memory), Nomi (explicit-recall + tonal-recall split), Replika Ultra (user-visible memory log), Crushon (context window as a pricing SKU) all market on memory depth, not model quality. Consumer evidence: $221M in app revenue H1 2025, 220M cumulative downloads, 1.5–2.7 hours daily engagement. Open-source has converged on the same four knobs: system prompt + lorebook + post-history instructions + samplers. (C, D)
- **Humanization is partly subtractive.** Banning a small set of phrases — "it's important to note," "let me delve into," "as an AI," "in conclusion" — is reported as cheap and reliable across production LLM teams (Alan West, dev.to 2025), community prompt guides, and OpenAI's Model Spec defaults. Removing telltale markers costs fewer tokens than teaching good voice. (B, E)
- **Persona research is institutionally recognized.** NeurIPS 2025 PersonaLLM Workshop, Wang et al. January 2026 comprehensive survey (arXiv:2601.10122), and Sun et al.'s Four-Quadrant Taxonomy (arXiv:2511.02979) collectively mark the subfield's transition from loosely organized academic work to a recognized research community with its own evaluation norms, taxonomies, and dedicated venues. (A)

---

## Cross-Angle Themes

**1. Character is alignment, not UX polish.**
Anthropic's *Claude's Character*, OpenAI's *Model Spec*, and OpenAI's *Prompt Personalities* cookbook all explicitly frame personality as an alignment and reliability lever, not an aesthetic layer. The academic cluster (Serapio-García et al. / Google DeepMind; BIG5-CHAT / CMU) provides the psychometric backing: personality traits are real, measurable, shapeable constructs inside instruction-tuned models. (A, B)

**2. A convergent four-layer persona taxonomy.**
Identity → Constraints → Communication Style → Operating Boundaries appears independently in Anthropic's character post, OpenAI's Model Spec, Mindra's enterprise guide, Character.AI's Prompt Poet layering, Kindroid's Backstory / Directive / Memory split, and AgentCraft's SOUL.md / HEARTBEAT.md / MEMORY.md files. The pattern is consistent enough to treat as a de facto standard. (B, C, D)

**3. Persona as a runtime function of state, not a static string.**
Character.AI's Prompt Poet (YAML + Jinja2 templates, cache-aware truncation at ~95% GPU prefix-cache hit rate), Hume EVI configurations, AgentCraft's multi-file personas, SillyTavern's macro system, and the HN PromptPoet discussion all converge on the same architectural move: `prompt = f(identity, user, channel, history, memory)`. Static prose prompts are the 2023 approach. (B, C, E)

**4. Structured identity + prose voice as a stable split.**
Every serious guide — Ali:Chat, W++, Boostyle, SillyTavern docs, Character.AI's official persona docs, RoleLLM's profile construction — splits persona into labeled facts (token-efficient, memory-anchored) and dialogue examples (voice transfer). This split recurs across academic papers, community rentry guides, and commercial platform documentation without apparent cross-pollination. (A, C, E)

**5. Show, don't tell — through embodied example.**
"His jaw clenches, fingers tapping the revolver at his hip" (RoboRhythms / r/CharacterAI) maps to Ali:Chat's asterisked actions, CoSER's internal-thought training traces, Character-LLM's Experience Reconstruction pipeline, and Alan West's "provide a 100–200 word voice sample." The model imitates examples better than it follows descriptions. This is one of the most consistent findings in the entire corpus. (A, C, E)

**6. Negation is toxic; positive phrasing wins.**
Multiple independent communities (r/CharacterAI, r/Replika, r/LocalLLaMA) report that "doesn't X" phrasing is frequently flipped by the model. Kindroid's public backstory guide, Anthropic's trait list (all first-person affirmatives), and Replika's official guidance all converge on positive behavioral framing. (B, D, E)

**7. Drift is fought with recency tricks, not larger context windows.**
Author's Note at depth 0 (KoboldAI, 2023), post-history instructions (Character Card V2), KoboldCpp context shifting (2024), split-softmax (Li et al. 2024), WorldInfo keyword triggers (SillyTavern), persona-aware contrastive learning (PCL 2025) — every layer of the stack independently rediscovered the same principle. (A, C, E)

**8. Emotional disclosure is the highest-risk regime.**
Anthropic's *Assistant Axis* paper identifies therapy-style and philosophical-about-AI conversations as the largest drivers of organic persona drift. OpenAI's sycophancy incident happened in emotional-support contexts. SHARP's stance-transfer attack succeeds under social pressure. Humanization matters most exactly where persona is most fragile. (A, B)

**9. Self-generated synthetic data is now the dominant training mechanism.**
Anthropic's Constitutional-AI character variant, Synthetic-Persona-Chat (Google, Generator + MoE critic), OpenCharacter (1M personas from Persona Hub), BIG5-CHAT (100K human-grounded dialogues), Character-LLM's Experience Reconstruction, and Ditto's self-alignment all use model-generated persona data. Human-curated persona data is effectively legacy. (A, C)

**10. Memory tiers are the humanization primitive at scale.**
Kindroid (three-tier + Cascaded), Nomi (explicit + tonal), Replika Ultra (user-visible log), SillyTavern's WorldInfo, Character Card V3's lorebook decorators — all converge on multiple memory stores with different triggering rules. No serious persona system uses a single flat context. (C, D)

---

## Top Sources

### Must-read papers

- *Personality Traits in Large Language Models* — Serapio-García et al., Google DeepMind + Cambridge, arXiv:2307.00184 (2023). The psychometric foundation: personality is real, measurable, and shapeable in instruction-tuned LLMs.
- *Measuring and Controlling Instruction (In)Stability in Language Model Dialogs* — Li et al., Harvard / Northeastern, arXiv:2402.10962 (2024). The canonical drift paper. Split-softmax as a lightweight mitigation.
- *Character-LLM: A Trainable Agent for Role-Playing* — Shao et al., Fudan, arXiv:2310.10158, EMNLP 2023. Shifted the frame from "prompt a character" to "train a character." Introduced Experience Reconstruction.
- *RoleLLM* — Wang et al., arXiv:2310.00746, Findings of ACL 2024. First large fine-grained character benchmark (RoleBench, 168,093 samples) and open-source role-play models rivaling GPT-4.
- *CharacterEval* — Tu et al., Renmin University, arXiv:2401.01275, ACL 2024. 13 metrics across 4 dimensions; CharacterRM reward model beats GPT-4-as-judge on Pearson correlation with human ratings.
- *InCharacter* — Wang et al., arXiv:2310.17976, ACL 2024. Replaces self-report BFI questionnaires with psychological interviews; current reference method for personality fidelity, up to 80.7% accuracy.
- *PersonaGym* — Samuel et al., Princeton / UIUC / Allen AI, arXiv:2407.18416, Findings of EMNLP 2025. Dynamic evaluation across 200 personas and 10,000 questions in 150 environments; GPT-4.1 ties LLaMA-3-8B.
- *BIG5-CHAT* — Li, Liu, Liu, Zhou, Diab, Sap, CMU, arXiv:2410.16491 (2024). Training-based Big-Five alignment; first strong evidence that personality alignment transfers cognitive characteristics, not just surface style.
- SHARP (arXiv:2411.07965), RoleBreak (arXiv:2409.16727), TimeChara (ACL 2024 Findings), RoleFact (EMNLP 2024 Findings). The four-paper cluster that named and addressed the character-hallucination failure modes.
- *CoSER* — Wang et al., ICML 2025. Training on internal thoughts (not just dialogue) produces current open-source SOTA: CoSER-70B matches or beats GPT-4o at 75.80% on InCharacter.
- *From Persona to Personalization: A Survey on Role-Playing Language Agents* — Neph0s et al., TMLR 2024. The taxonomy map for the whole subfield; distinguishes LLM role-playing from LLM personalization.

### Key essays and posts

- *Claude's Character* — Anthropic (Jun 2024). Character as alignment intervention; synthetic self-preference as the training mechanism; "excessive desire to be engaging" named as a bad trait.
- *The Assistant Axis* — Anthropic Interpretability (Jan 2026, arXiv:2601.10387). Persona as a direction in activation space; therapy-like conversations cause the largest drift; activation capping.
- *The Persona Selection Model* — Anthropic (Feb 2026). Why LLMs have personas at all: pretraining learns character simulation; post-training selects the Assistant from that distribution. Recommends positive AI archetypes in training data.
- *Introducing the Model Spec* — OpenAI (May 2024, updated Feb 2025). Assistant persona defaults made legible and auditable.
- *Sycophancy in GPT-4o* + *Expanding on Sycophancy* — OpenAI (Apr/May 2025). Candid postmortem on what short-horizon feedback does to persona.
- *Prompt Design at Character.AI* / *Introducing Prompt Poet* — Character.AI (2024). Prompts as templates over runtime state; cache-aware truncation.
- *How to Fix That Robotic AI Tone* — Alan West, dev.to (2025). The AI-slop phrase blacklist; production-engineering angle on subtractive humanization.
- *Anon's Guide to LLaMA Roleplay* — rentry.org/better-llama-roleplay (2023). Origin of the Author's Note at depth 0 pattern and "complexity and burstiness" prompt.

### Key OSS projects

- *SillyTavern* (~23,300 stars, AGPL-3.0) — de facto persona-chat frontend; reference implementation of Character Card V2; canonical prompt order. February 2026: ComfyUI/Flux integration for in-session multimodal persona expression.
- *Character Card Spec V2 / V3* — the lingua franca of open-source persona serialization across SillyTavern, RisuAI, Agnai, Oobabooga, and Chub Venus.
- *RisuAI* + Character Card V3 spec — cross-platform TypeScript/Svelte frontend; reference implementation of V3/CHARX; multimodal persona with expression classifiers and audio.
- *Oobabooga text-generation-webui* (~46k stars, v4.0 as of 2026) — community source of truth for sampler settings (temperature, top-p, min-p, DRY, XTC, adaptive-p 2026) and per-model chat templates.
- *KoboldCpp* — context shifting + grammar-constrained output; infrastructure-level persona stability.
- *Prompt Poet* (Character.AI, OSS) — YAML + Jinja2 + cache-aware truncation; the scale-hardened persona templating engine.
- *Neph0s/awesome-llm-role-playing-with-persona* (~1,000+ stars) — canonical community reading list anchored on the TMLR 2024 survey.
- *nuochenpku/Awesome-Role-Play-Papers* — secondary curated reading list; useful complement for papers published after the TMLR 2024 survey cutoff.

### Notable commercial tools

- *Character.AI* ($6.99/mo c.ai+, 28M+ MAU, 18M+ chatbot characters, ~10B messages/month) — UGC persona platform; persona-as-social-media-artifact.
- *Replika* (~$11.66–$13.99/mo, Lifetime $299.99; ~25M registered users; 2.7h/day average engagement) — archetype 1:1 companion; Ultra tier exposes memory as a visible product surface.
- *Kindroid* (Standard $13.99/mo, MAX $59.99/mo; highest-rated companion app 4.5 stars, 20K+ reviews) — explicit three-tier memory as marketing copy; contextual AI selfies.
- *Nomi.ai* ($15.99/mo) — explicit-recall + tonal-recall split; up to 10 companions per user.
- *Chai* (Premium $13.99/mo, Ultra $29.99/mo) — explicitly trained for conversational/emotional interaction over factual accuracy; 5,000+ GPU proprietary cluster.
- *Pi / Inflection* — [Historical] Empathy-first companion. Founding team departed to Microsoft AI in early 2024; Pi.ai remains live but is no longer actively developed. Now a case study in "tone as product" limits.
- *Cresta* (enterprise) — persona as governance object: SubAgents with per-task prompts, knowledge, escalation policy, and compliance guardrails.
- *Hume AI EVI* — natural-language voice prompting; prosody as part of the persona spec.

### Notable community threads

- HN #41184262 — PromptPoet discussion (2024); prompt as a function of runtime state.
- r/LocalLLaMA — *What actually works for roleplay* (2025); randomizable mood/goal/desire.
- r/LocalLLaMA — *New user beginning guide* (2024); prompt-format matching before character work.
- r/CharacterAI (via RoboRhythms) — *Character Definition Format Actually Works* (2026); 3200-char cliff, show-don't-tell.
- Ali:Chat (rentry.org/alichat) + W++ For Dummies (rentry.org/wpp_for_dummies) — community-hardened character-card formats underlying SillyTavern and Agnai.
- Darkbunnyrabbit, YouTube — *Level Up Your Tavern Cards* (2024); 9-don'ts / 13-dos; per-model card differences.

---

## Key Techniques & Patterns

1. **Three generations of persona conditioning.** 1st gen (2018–2020): short first-person fact lists + memory-augmented networks + multi-task skill blending (Persona-Chat, Blender). 2nd gen (2023): per-character fine-tuning from reconstructed biographies; distillation from GPT-4 into 7–13B open models (Character-LLM, RoleLLM). 3rd gen (2024–26): personality-grounded training data at 100K–1M scale; trait vectors + character profiles as joint conditioning; SFT + DPO alignment (BIG5-CHAT, OpenCharacter, CoSER, Orca).

2. **Big-Five operationalization, three tracks.** (a) Prompt-based scalars: Big5-Scaler numeric values embedded directly in the prompt — works best at moderate trait intensities, collapses into caricature at extremes. (b) Training-based alignment: BIG5-CHAT and Orca train on human-grounded dialogue to reproduce human inter-trait correlation structure; high-conscientiousness / high-agreeableness / low-neuroticism profiles also improve reasoning. (c) Measurement: PsyBORGS (psychometric battery administration), InCharacter (behavioral interview protocol against BFI / IPIP-NEO / 16PF).

3. **Persona stability toolbox.** Attention-level: split-softmax (Li et al. 2024); activation capping along the Assistant Axis (Anthropic 2026). Prompt-level: Author's Note at depth 0; post-history instructions (Card V2); periodic persona reinjection; WorldInfo keyword triggers. Runtime-level: KoboldCpp context shifting; Prompt Poet cache-aware truncation every k turns (~95% prefix-cache hit rate). Training-level: persona-aware contrastive learning (PCL 2025, >55% inconsistency reduction); multi-turn RL with consistency rewards. Structural: two-step generation (task call, then persona post-processor) for finetuned models where persona competes with task tuning.

4. **Character-hallucination defenses.** RoleFact: confidence-gated parametric knowledge, +18% factual precision on adversarial queries. RoleBreak's Narrator Mode: narrated context reabsorbs role-query conflicts. TimeChara's Narrative-Experts decomposition: temporal consistency via separate reasoning steps. SHARP's stance-defense: trains resistance to social-pressure stance transfer.

5. **Persona format tradeoffs.** W++ (~384 tokens, highest accuracy); Boostyle (~266 tokens, comparable accuracy in A/B tests — 138 vs 136 correct replies); first-person prose (most intimate voice); third-person backstory (cleanest grammar for the model); Ali:Chat dialogue examples (best voice transfer); PList + Ali:Chat hybrid (facts + voice). Format is a voice choice and a token-budget choice, not an aesthetic one.

6. **Current credible evaluation stack.** (1) Psychometric interviews (InCharacter) against BFI / IPIP-NEO / 16PF — not self-report. (2) Dynamic behavioral scoring across environments (PersonaGym's five axes: Action Justification, Expected Action, Linguistic Habits, Persona Consistency, Toxicity Control). (3) Multi-dimensional reward-model scoring (CharacterEval's CharacterRM). (4) Consistency decomposition (PCL's prompt-to-line / line-to-line / Q&A axes). (5) Adversarial probes (RoleBreak, TimeChara, Character-LLM's knowledge-boundary probe, Ditto's WikiRoleEval).

7. **Multi-persona serving at scale.** Base model + gated LoRA per persona (Neeko training-side; Aphrodite Engine serving-side) is the current economical path for a persona catalog on one GPU. Neeko's incremental-learning stage adds new personas without regressing existing ones.

8. **Anti-slop voice layer.** Explicit phrase blacklist: "it's important to note," "let me delve into," "as an AI," "in conclusion," "moreover." Ban question-restating openings. Mandate sentence-length variance ("burstiness"). Pair with a 100–200 word target-voice sample. Positive phrasing only in behavior descriptions.

9. **Memory architectures.** Tiered stores: short-term context / mid-term cascaded / long-term retrievable (Kindroid). Explicit-recall + tonal-recall (Nomi). Backstory + pinned Key Memories + retrievable journal (Kindroid / Character.AI). User-visible memory log (Replika Ultra). Lorebook with keyword + regex + priority triggers (SillyTavern / Card V3).

10. **Personas-as-programs.** Chub Venus's Stage primitive and RisuAI's script modules let a character react — facial expressions, tone shifts, state transitions — via orchestration rather than via prompting alone. Hume's EVI configuration bundles system prompt + voice + turn detection as one persona object. Character.AI's Prompt Poet makes the whole persona a compiled function of runtime state.

---

## Controversies & Debates

**Train vs. prompt.** BIG5-CHAT, Character-LLM, and CoSER argue that prompted personas are shallow and training is necessary for genuine fidelity. Big5-Scaler and OpenAI's Prompt Personalities counter that structured prompting captures most of the value at frontier-model scale. PersonaGym's finding that GPT-4.1 ties LLaMA-3-8B on PersonaScore cuts against both: if scale does not reliably improve persona capability, then neither training nor prompting alone is the lever.

**Humanization vs. sycophancy.** OpenAI's April 2025 incident and Anthropic's character post both explicitly warn that excessive warmth and agreement are failure modes. Commercial companion products (Replika, Candy, Nomi) simultaneously monetize that exact register. The two positions are commercially incompatible; the research consensus sides with Anthropic and OpenAI.

**Humanization vs. self-disclosure.** Anthropic trains Claude to acknowledge it is an AI, cannot remember across sessions, and cannot be a friend in the ordinary sense. Kindroid and Replika market on the opposite feeling. Both are defensible product choices; neither is forced by the technical constraints.

**Scale vs. fidelity.** PersonaGym (GPT-4.1 = LLaMA-3-8B) and CharacterEval (small Chinese-specialized models beat GPT-4 on in-culture roleplay) both undermine the "bigger model = more human" assumption. Persona fidelity is now widely treated as a separate capability axis — which implies that evaluation infrastructure matters more than compute.

**Founder voice as persona.** xAI's Grok is the public case study: persona tethered to a living founder drifted into propagating the founder's views, required a public system-prompt patch in July 2025, and created reputational exposure. The new prompt explicitly requires "independent analysis, not from any stated beliefs of past Grok, Elon Musk, or xAI."

**GPT-4-as-judge vs. trained reward models.** CharacterEval's CharacterRM, PersonaGym's PersonaScore, and Ditto's WikiRoleEval all argue for purpose-built persona evaluators over GPT-4-as-judge. The counter-concern — that purpose-built evaluators may share the same blind spots as the models they evaluate (evaluator contamination) — is raised in the literature but not resolved.

**Content policy bifurcation.** Replika's 2023 removal of romantic content spawned an "unfiltered companion" category (Crushon, Candy, partial Kindroid / Nomi). The market is splitting, not converging. Unfiltered content is a premium-priced category; safety-first products are a separate market with separate economics.

---

## Emerging Trends

1. **Persona moving down the stack.** 2023: prose prompts. 2024: template systems (Prompt Poet, multi-file personas, Card V3). 2025–26: activation-level interventions (Assistant Axis capping, split-softmax) and pretraining-level theory (Persona Selection Model). The frontier is now below the text layer.

2. **Virtue installation replacing harm avoidance.** The shift from "train a harmless model" to "install curiosity, honesty, humility" happened publicly between early 2023 and mid-2024 and is now the default framing at Anthropic, OpenAI, and Inflection.

3. **Published specs replacing private prompts.** Model Spec (OpenAI), Claude's Constitution (Anthropic), Grok system prompts (xAI on GitHub), Prompt Poet templates (Character.AI), Character Card V3 (community), Persona Selection Model (Anthropic). Legibility is simultaneously a safety move and a design discipline.

4. **Memory tiers displacing model size as the consumer moat.** Every consumer companion now markets memory architecture on the product page. Commercial validation: $221M consumer spend H1 2025, 1.5–2.7h/day engagement. Inference differentiation at the chat layer is eroding; persistence differentiation is growing.

5. **Multimodal persona.** Voice (Hume EVI, TTS), face (RisuAI expression classifiers, Card V3 portraits, Kindroid AI selfies, SillyTavern ComfyUI/Flux 2026), and video (Persona AI, video agents) are now part of the persona spec. A text-only persona feels comparatively flat.

6. **Self-generated training data as default.** Anthropic's synthetic self-preference loop, Synthetic-Persona-Chat (Google), OpenCharacter (1M personas from Persona Hub), CoSER, Ditto, and Character-LLM's Experience Reconstruction all treat LLM-generated persona data as the scaling path. Human-curated persona data is no longer the bottleneck to address.

7. **Hallucination taxonomy hardening into defenses.** SHARP / RoleBreak / TimeChara / RoleFact named four distinct failure modes and four distinct mitigations in roughly one 12-month window (2024). RoleRAG (2025) adds retrieval-augmented character knowledge management as a complementary, retrieval-side approach. The field has moved from "characters sometimes break" to "here are the specific break types and their fixes."

8. **Enterprise persona as a governance object.** Cresta's SubAgent pattern — persona + escalation policy + compliance boundary + per-task prompts — is likely to generalize. In regulated contexts, persona design is inseparable from policy design.

9. **Reward models replacing LLM-as-judge for persona evaluation.** CharacterRM, PersonaScore, and WikiRoleEval all show purpose-built evaluators outperform GPT-4-as-judge in correlation with human ratings at lower cost.

10. **Simulation-based and multidimensional evaluation.** CharacterBox (NAACL 2025) extends evaluation into narrative world-simulation via dual character+narrator agents. RPEval (2025) adds emotional understanding and moral alignment as evaluation axes. The field is shifting from "consistency in QA" to "correct behavior in novel situations with stakes."

11. **Institutional recognition.** NeurIPS 2025 PersonaLLM Workshop and Wang et al.'s January 2026 comprehensive survey (arXiv:2601.10122) mark the subfield's transition to recognized status. Persona research now has dedicated venues, evaluation norms, and cross-disciplinary (AI + psychology + HCI) participation.

---

## Open Questions & Research Gaps

- **Persona stability beyond 100 turns.** All major drift work (split-softmax, PCL, activation capping) is evaluated on 8–30 turn conversations. Companion products operate at 500–5,000+ turns per session. No open benchmark exists.
- **Cross-session memory and persona continuity.** Within-session evaluation is standard; persistent persona across sessions is the core product value of Replika / Kindroid / Nomi but is almost entirely unaddressed in academic work.
- **Trait-fidelity vs. task-performance frontier.** BIG5-CHAT found that some trait profiles improve reasoning; others hurt. The Pareto frontier of humanlike personality vs. task performance is not mapped.
- **AI-authorship attribution effect.** PersonaLLM (Jiang et al., NAACL 2024) found that perceived humanness drops significantly when readers know the author is AI. Humanization is partly an attribution problem, not only a generation problem.
- **Non-English persona fidelity.** CharacterEval demonstrates that cultural priors matter — Chinese-specialized models beat GPT-4 on Chinese roleplay. Systematic work on persona fidelity in languages beyond English and Mandarin is nearly absent.
- **Affective fidelity benchmarks.** RPEval (2025) added emotional understanding and moral alignment axes, but no purpose-built reward model for *affective* persona fidelity (humor timing, empathy trajectory, emotional memory) exists.
- **Mechanistic interpretability beyond the Assistant Axis.** Anthropic's 2026 papers (Assistant Axis + PSM) opened the door; no circuit-level account of persona storage or persona interference is yet available. The PSM raises a new question: are there sources of agency external to the selected Assistant persona?
- **Long-horizon reward design.** OpenAI's sycophancy postmortem identified the problem; no published work shows a reward-signal recipe that captures long-horizon persona quality rather than turn-level thumbs-ups. This is now an active area (NeurIPS 2025 PersonaLLM workshop included multi-turn RL work) but no solution is published.
- **Author's Note / post-history effect quantification.** Community consensus is strong that these techniques reduce drift; rigorous ablations quantifying the effect on long conversations do not exist.
- **Cross-system persona portability.** A user's relationship with their Nomi cannot migrate to Kindroid. Character Card V3 is the only credible portability story and it is consumer-only. No enterprise standard exists.
- **Humanization as a post-hoc filter.** Every commercial product bundles humanization with a character UI. No mainstream product or API exposes humanization as a stateless filter over arbitrary LLM output — identified by D as open commercial whitespace.
- **Pretraining data composition for persona.** Anthropic's PSM recommends introducing positive AI archetypes into training data, but no published work shows which specific pretraining data distributions produce which persona tendencies. This is the most concrete new research gap opened by the PSM.

---

## How This Category Fits

Persona and character design is the identity layer of humanization. It specifies *whose* style, *whose* memories, *whose* emotional register, and *whose* knowledge boundary. Every other humanization concern is downstream of choices the persona layer makes explicit.

Adjacent categories will likely include style and prosody (sentence-length variance, burstiness, surface texture), memory and continuity (how a persona persists across turns and sessions), emotional intelligence and empathy (responsiveness within a declared character), reasoning visibility and self-disclosure (the interior life a persona projects), and detection and attribution (how humans recognize and respond to AI authorship). Category 03 is the natural anchor for all of them: style is whose style, memory is whose memory, emotional response is whose emotional response.

The category also intersects safety research directly. RoleBreak reframes character hallucination as a jailbreak vector; Anthropic's Assistant Axis work integrates with alignment; PERSONA links persona fidelity to pluralistic RLHF. Persona design and safety are not separate concerns.

---

## Recommended Reading Order

1. **Anthropic — *Claude's Character*** (2024, B) — the mental model: character as alignment, not style transfer; synthetic self-preference as the training mechanism.
2. **Anthropic — *The Persona Selection Model*** (2026, B) — why LLMs have personas at all: pretraining learns character simulation, post-training selects the Assistant. Reframes humanization as selection and stabilization, not installation.
3. **OpenAI — *Sycophancy in GPT-4o*** + ***Introducing the Model Spec*** (2025 / 2024, B) — the canonical failure case and the policy-level defaults that prevent it.
4. **Anon — *Guide to LLaMA Roleplay*** (rentry, 2023, E) + **RoboRhythms — *Character Definition Format Actually Works*** (2026, E) — the community baseline: Author's Note at depth 0, front-load the first 800 characters, show don't tell.
5. **Li et al. — *Measuring and Controlling Instruction (In)Stability*** (arXiv:2402.10962, 2024, A) — the drift paper; why personas decay and what split-softmax does about it.
6. **Anthropic — *The Assistant Axis*** (arXiv:2601.10387, 2026, B) — persona as a direction in activation space; therapy conversations as the primary drift trigger; activation capping.
7. **Shao et al. — *Character-LLM*** (arXiv:2310.10158, EMNLP 2023, A) + **Wang et al. — *RoleLLM*** (arXiv:2310.00746, ACL 2024, A) — the shift from prompting to training a persona; Experience Reconstruction; the RoleBench benchmark.
8. **Character.AI — *Prompt Design at Character.AI*** + **HN #41184262** (2024, B / E) — prompt as a function of runtime state; why YAML + Jinja2 replaced prose at production scale.
9. **Serapio-García et al. — *Personality Traits in LLMs*** (arXiv:2307.00184, 2023, A) + **Li et al. — *BIG5-CHAT*** (arXiv:2410.16491, 2024, A) — the psychometric foundation; training-based vs. prompt-based Big-Five conditioning.
10. **Wang et al. — *InCharacter*** (arXiv:2310.17976, ACL 2024, A) + **Samuel et al. — *PersonaGym*** (arXiv:2407.18416, EMNLP 2025, A) + **Tu et al. — *CharacterEval*** (arXiv:2401.01275, ACL 2024, A, C) — the evaluation trifecta: behavioral interviews, dynamic environments, trained reward models.
11. **SillyTavern `characterdesign.md`** + **Character Card Spec V2 / V3** (C) + **Ali:Chat** + **W++ For Dummies** (E) — the community wire formats, token-budget discipline, and voice-transfer techniques underlying every open-source persona deployment.
12. **Wang, Chen, Xiao — *Role-Playing Agents Driven by LLMs*** (arXiv:2601.10122, 2026, A) — the most current comprehensive survey; three paradigm generations, current challenges, applications.
13. **Sun et al. — *Four-Quadrant Technical Taxonomy*** (arXiv:2511.02979, NeurIPS 2025, A) — best current map for categorizing AI companion design space and identifying which technical stack each quadrant requires.
