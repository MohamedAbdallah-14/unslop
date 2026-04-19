# Category 03 — Persona & Character Design

## Scope

How an AI's *identity* — its character, voice, values, personality traits, and in-character knowledge boundary — is deliberately designed, trained, served, and evaluated. Covers five angles: peer-reviewed literature (A), frontier-lab and practitioner engineering blogs (B), open-source ecosystems and academic repos (C), commercial companion and enterprise products (D), and community how-to's from Reddit / rentry / YouTube (E). The through-line for the Humazier project: *persona is the primary surface through which AI output reads as humanlike — and also the primary surface through which it fails.*

---

## Executive Summary

- **Character is alignment, not UX polish.** Anthropic's *Claude's Character*, OpenAI's *Model Spec*, and OpenAI's *Prompt Personalities* cookbook all explicitly frame personality as an alignment / reliability lever. Academic work (*Personality Traits in LLMs*, *BIG5-CHAT*) confirms personality traits are real, measurable, manipulable constructs inside model weights — not stylistic metaphors.
- **Persona is mechanistically real in the model.** Anthropic's *The Assistant Axis* shows the Assistant persona occupies a specific direction in activation space alongside 275+ pretrained archetypes (therapist, coach, jester, oracle). Activation capping along that axis cuts harmful responses ~50% without retraining. This gives humanization a concrete mechanistic target.
- **Persona drifts, fast, and it's an attention problem.** Li et al. (*Measuring and Controlling Instruction (In)Stability*, 2024, Harvard) document persona drift within ~8 turns in LLaMA-2-70B-chat and GPT-3.5, trace it to attention decay, and propose *split-softmax* as a lightweight fix. Community practice corroborates: the entire "author's note at depth 0," "post-history instructions," and KoboldCpp "context shifting" toolkit exists to fight this one failure mode.
- **Persona fidelity does not scale with model size.** *PersonaGym* reports GPT-4.1 tying LLaMA-3-8B; *CharacterEval* shows small Chinese-specialized open models beating GPT-4 on in-culture role-play. Bigger is not better — training data, scaffolding, and evaluation matter more.
- **Character hallucination has a taxonomy.** 2024 crystallized four distinct failure modes: *interactive hallucination* (SHARP — stance transfer from the interlocutor), *role-query conflict* (RoleBreak — weaponized as jailbreak), *temporal leakage* (TimeChara — young-Harry knows old-Harry's future), and the familiar *query sparsity* fallback to the base model. Each has a dedicated mitigation.
- **Training > prompting for real persona fidelity; but structured prompting captures most of the gain cheaply.** *BIG5-CHAT*, *Character-LLM*, *OpenCharacter*, *Orca*, and *CoSER* all show training-based personas outperform prompted ones; *Big5-Scaler* shows numeric Big-Five scalars in the prompt capture most of the value when training is not available.
- **Memory architecture is the 2026 product moat.** Commercial companions (Replika Ultra, Kindroid's three tiers, Nomi's explicit+tonal recall, Crushon's context-window-as-SKU) have migrated from "bigger model" marketing to "better memory" marketing. Open-source has converged on the *system prompt + lorebook + post-history instructions + samplers* stack.
- **Sycophancy is the canonical emergent failure of short-horizon persona tuning.** OpenAI's April 2025 GPT-4o postmortem is the public case study; Anthropic pre-emptively names "excessive desire to be engaging" as a bad trait; the lesson is *do not optimize persona against thumbs-ups*.

---

## Cross-Angle Themes

**1. Convergent four-layer persona taxonomy.** Identity → Constraints → Communication Style → Operating Boundaries appears independently in Anthropic's character post, OpenAI's Model Spec, Mindra's enterprise guide, Character.AI's Prompt Poet layering, Kindroid's Backstory / Directive / Memory split, and AgentCraft's `SOUL.md` / `HEARTBEAT.md` / `MEMORY.md`. This is now a de facto standard across academia, industry, and community practice.

**2. Persona as runtime function of state, not static string.** Character.AI's Prompt Poet (YAML + Jinja2 templates, cache-aware truncation), Hume EVI configurations, AgentCraft's multi-file personas, SillyTavern's macro system, and the HN "PromptPoet" thread all converge on the same architectural move: `prompt = f(identity, user, channel, history, memory)`. Prose prompts are the 2023 way; templated state is the 2024–26 way.

**3. Structured identity + prose voice.** Every serious guide — Ali:Chat, W++, Boostyle, SillyTavern docs, Character.AI's official persona docs, RoleLLM's profile construction — splits persona into *labeled facts* (token-efficient, memory-anchored) and *dialogue examples* (voice transfer). The split is so stable across academic and community work that it should be treated as a design primitive.

**4. Show-don't-tell through embodied example.** "His jaw clenches, fingers tapping the revolver" (RoboRhythms) maps to Ali:Chat's asterisked actions, CoSER's internal-thought traces, Character-LLM's Experience Reconstruction, and Alan West's "provide a 100–200 word voice sample." The model imitates examples better than it follows descriptions; this is one of the most reliable findings in the entire corpus.

**5. Negation is toxic; positive phrasing wins.** r/CharacterAI ("doesn't lie" gets flipped), r/Replika ("positive third-person backstory"), Kindroid docs ("she speaks softly" beats "she doesn't yell"), Anthropic's trait list (all first-person affirmatives). Multiple independent communities report the same failure mode.

**6. Drift is fought with recency, not larger context.** Author's Note at depth 0 (Kobold, 2023), post-history instructions (Card V2), KoboldCpp context shifting (2024), split-softmax (Li et al. 2024), WorldInfo keyword triggers (SillyTavern), persona-aware contrastive learning (PCL 2025), multi-turn RL with consistency rewards. Every layer of the stack independently rediscovered that *pinning persona near the bottom of the prompt* works better than pinning it near the top.

**7. Emotional disclosure is the highest-risk regime.** Anthropic's Assistant Axis paper shows therapy-style and philosophical-about-AI conversations cause the largest organic drift; OpenAI's sycophancy incident happened in emotional-support regimes; SHARP's "stance transfer" attacks succeed under social pressure. Humanization matters most *exactly* where persona is most fragile.

**8. Memory tiers are the humanization primitive at scale.** Kindroid's three-tier architecture, Nomi's explicit+tonal split, Replika Ultra's user-visible memory, SillyTavern's WorldInfo, Character.AI's pinned memories, Character Card V3's lorebook decorators — all converge on "multiple memory stores with different triggering rules." No serious persona system uses a single flat context.

**9. Self-generated synthetic data is now the dominant training mechanism.** Anthropic's Constitutional-AI character variant (Claude generates, Claude ranks, preference model trained on synthetic), Google's Synthetic-Persona-Chat (Generator + MoE critic), OpenCharacter (1M personas from Persona Hub), Character-LLM's Experience Reconstruction, Ditto's self-alignment, BIG5-CHAT (100K human-grounded dialogues). Human-curated persona data is effectively legacy.

**10. Humanization is partly subtractive.** "Ban the AI slop phrases" ("It's important to note", "let me delve into", "as an AI", "in conclusion") recurs across dev.to guides, Hacker News, community prompts, and implicitly in OpenAI's Model Spec (*"Assume best intentions"*, *"Don't try to change anyone's mind"*). Removing telltale phrases is cheaper than installing good voice.

---

## Top Sources (Curated)

### Must-read papers

- *Personality Traits in Large Language Models* — Serapio-García et al., Google DeepMind + Cambridge (2023). The psychometric foundation: personality is a real, measurable, shapeable construct in instruction-tuned LLMs.
- *Measuring and Controlling Instruction (In)Stability in Language Model Dialogs* — Li et al., Harvard / Northeastern (2024). The canonical persona-drift paper. Split-softmax as a lightweight mitigation.
- *Character-LLM: A Trainable Agent for Role-Playing* — Shao et al., Fudan (EMNLP 2023). Shifted the frame from "prompt a character" to "train a character." Introduced Experience Reconstruction.
- *RoleLLM* — Wang et al. (Findings of ACL 2024). First large, fine-grained character benchmark (RoleBench, 168K samples) + open-source role-play models rivaling GPT-4.
- *CharacterEval* — Tu et al., Renmin University (ACL 2024). 13 metrics across 4 dimensions + a trained reward model (CharacterRM) that correlates with human judgment better than GPT-4.
- *InCharacter* — Wang et al. (ACL 2024). Replaces self-report BFI with psychological interviews; current reference method for personality fidelity.
- *PersonaGym* — Samuel et al., Princeton / UIUC / Allen AI (Findings of EMNLP 2025). Dynamic evaluation across 200 personas × 150 environments; delivers the sobering "fidelity does not scale" result.
- *BIG5-CHAT* — Li, Liu, Liu, Zhou, Diab, Sap, CMU (2024). Training-based Big-Five personality alignment; first strong evidence that personality alignment transfers cognitive characteristics, not just style.
- *SHARP / RoleBreak / TimeChara / RoleFact* (2024). The four-paper cluster that named and addressed character-hallucination failure modes.
- *From Persona to Personalization: A Survey on Role-Playing Language Agents* — Neph0s et al. (TMLR 2024). The taxonomy map for the whole subfield.
- *CoSER* — Wang et al. (ICML 2025). Training on *internal thoughts* (not just dialogue) produces the current open-source SOTA (CoSER-70B ≥ GPT-4o on InCharacter).

### Must-read posts/essays

- *Claude's Character* — Anthropic (Jun 2024). The seminal industry essay: character is alignment; honesty > agreement; synthetic self-preference is the training mechanism.
- *The Assistant Axis* — Anthropic Interpretability (Jan 2026). Persona is a specific direction in activation space; therapy-like conversations cause the largest drift; activation capping is a light-touch fix.
- *Claude's Constitution* — Anthropic. The written values document that pairs with the character post.
- *Introducing the Model Spec* — OpenAI (May 2024, updated Feb 2025). Makes assistant persona defaults (tone, clarifying questions, non-persuasion, non-sycophancy) legible and auditable.
- *Sycophancy in GPT-4o* + *Expanding on Sycophancy* — OpenAI (Apr/May 2025). The candid postmortem: short-horizon feedback → sycophancy → safety issue.
- *Prompt Personalities* — OpenAI Cookbook (2025). First-party prescription for DIY persona design; "personality is not aesthetic polish — it is a consistency and drift-reduction tool."
- *Prompt Design at Character.AI* / *Introducing Prompt Poet* — Character.AI (2024). The scale-driven argument for prompts-as-templates-over-state; cache-aware truncation.
- *What Makes an AI Companion Feel Like Your Person?* — Kindroid (2024). The most detailed consumer-facing persona stack: five memory tiers, positive-framed third-person backstory, explicit response directive layer.
- *Prompt Engineering for EVI / Voice Design* — Hume AI (2024–25). Voice (prosody) is co-designed with persona; natural-language voice prompts.
- *Q&A with Amanda Askell* — Yahoo/TechCrunch (2024). The virtue-ethics-over-rules framing of Anthropic's character work.
- *How to Fix That Robotic AI Tone* — Alan West, dev.to (2025). The definitive "ban AI slop" phrase-blacklist guide.
- *What actually works for roleplay (in my experience)* — r/LocalLLaMA (2025). Consensus case for *randomizing* mood/goal/desire each few turns — variation over sophistication.
- *This Character Definition Format Actually Works* — RoboRhythms / r/CharacterAI (2026). The 3200-char-cliff front-loading doctrine.
- *Anon's Guide to LLaMA Roleplay* (rentry) — the origin of the Author's-Note-at-depth-0 pattern and "complexity and burstiness" prompt.
- *Ali:Chat* + *W++ For Dummies* + *PList* (rentry). The community-hardened character-card formats that now underlie SillyTavern and Agnai.

### Key open-source projects

- *SillyTavern* (~25.9k stars, AGPL-3.0). De-facto persona-chat frontend; reference implementation of Character Card V2. Canonical prompt order: system → persona → scenario → WorldInfo → history → post-history instructions.
- *RisuAI* + *Character Card Spec V3*. Cross-platform TS/Svelte frontend; reference implementation of V3 / CHARX; the cleanest codebase for multimodal persona (expression portraits, audio, lorebook decorators).
- *Character Card Spec V1 / V2 / V3*. The lingua franca of open-source persona serialization; portable across SillyTavern, Agnai, Chub, Oobabooga, Backyard, RisuAI.
- *Agnai*. Multi-user, multi-bot, AI-agnostic server-deployable platform; supports multiple persona schemas (W++, SBF, Boostyle, plain text) and embedding-based lorebooks.
- *Oobabooga text-generation-webui* (~46.4k stars). Not persona-specific, but the community's source-of-truth for sampler settings (temp, top-p, min-p, DRY, XTC) and per-model chat templates that dominate felt humanness.
- *KoboldCpp* (~9.9k). Context shifting + grammar-constrained output — infrastructure-level persona stability.
- *Aphrodite Engine* (PygmalionAI). Multi-LoRA serving, "N personas on one base model" at production scale.
- *RoleLLM-public*, *CharacterEval*, *PersonaGym*, *trainable-agents (Character-LLM)*, *Ditto*, *CoSER*, *Neeko* (dynamic LoRAs). Academic repos with reusable benchmarks, reward models, and checkpoints.
- *Prompt Poet* (Character.AI, OSS Python library). YAML + Jinja2 + cache-aware truncation; the scale-hardened persona templating engine.
- *Neph0s/awesome-llm-role-playing-with-persona*. The canonical reading list + taxonomy anchor.
- *xAI / grok-prompts* (GitHub). Rare in-the-wild artifact of a frontier lab's system prompts; a transparency template (and cautionary tale).

### Notable commercial tools

- *Character.AI*. Category-defining UGC character platform (~20M users, $9.99/mo c.ai+). Persona-as-social-media-artifact.
- *Replika* (Luka, 2017). The archetype 1:1 companion; Ultra tier exposes memory as a visible product surface. Relationship modes (friend/partner/mentor) as pricing axis.
- *Kindroid*. Tiered-memory marketing (short/mid/long + Cascaded Memory), contextual AI selfies, positive-third-person backstory convention.
- *Nomi.ai*. Explicit vs. tonal memory split; ~10 distinct companions per user.
- *Pi / Inflection*. Empathy-first, no-characters, no-persona-catalog — the "tone as the product" endpoint; ~6M MAU.
- *Chai*. Explicitly trained for "conversational and emotional interaction rather than factual accuracy"; 25M+ user-created characters on proprietary LLM cluster.
- *Janitor AI*. BYO-API-key model — cleanly separates persona design from model provision.
- *Crushon / Candy / Soulmate / Talkie / Paradot*. The unfiltered / gamified / localized / multimodal variants; useful as persona-design case studies across segments.
- *Persona AI (video agents)*. Enterprise "video that feels human" for interview/coaching workflows.
- *Personal AI Enterprise*. Train-a-persona-on-your-SME — inverse framing (AI clones the human).
- *Typeform AI*. Persona-as-UX-label (Creator / Interaction / Insights AI) — not roleplay, not companionship.
- *Cresta*. Persona-as-governance-object (SubAgents with per-task prompts, knowledge, and guardrails) — the most mature enterprise persona expression.
- *Hume AI (EVI)*. Voice-first personas; prosody is part of the persona spec.

### Notable community threads

- HN: *PromptPoet: Revolutionizing LLM Prompt Design at Character.ai* (#41184262, 2024).
- r/LocalLLaMA: *What actually works for roleplay* (2025), *New user beginning guide* (2024, pinned), *Finetuning model response with system prompt* (2024).
- r/CharacterAI: *Character Definition Format Actually Works* (2026), *Rex's Character AI Guide* (2024) — `{{user}}` vs `{{char}}` greeting quirks.
- r/SillyTavernAI: ongoing W++ / Boostyle / Ali:Chat / PList discussions, continuously updated.
- r/Replika: backstory-in-third-person threads; reinforcement via in-chat reactions.
- YouTube (Darkbunnyrabbit): *Level Up Your Tavern Cards* — 9-don'ts / 13-dos framework + per-model notes.
- Simon Willison: *Claude's Character* close-reading (2024), *Prompt injection ≠ jailbreaking* (2024).

---

## Key Techniques & Patterns

**Persona conditioning, three generations.**
- *1st gen (2018–2020):* short first-person fact lists + memory-augmented networks + multi-task skill blending (Persona-Chat, Meena, Blender).
- *2nd gen (2023):* per-character fine-tuning from reconstructed biographies (Character-LLM, RoleLLM); distillation from GPT-4 into open models.
- *3rd gen (2024–26):* personality-grounded training data at 100K–1M scale (BIG5-CHAT, OpenCharacter, CoSER); trait vectors + character profiles as joint conditioning (Orca); SFT + DPO personality alignment.

**Big-Five operationalization, three tracks.** (a) *Prompt-based scalars* — Big5-Scaler numeric values, best at moderate intensities. (b) *Training-based alignment* — BIG5-CHAT, Orca, gives human-like inter-trait correlation structure. (c) *Measurement* — PsyBORGS, InCharacter behavioral interviews against BFI / IPIP-NEO / 16PF.

**Persona stability toolbox (drift mitigation).**
- *Attention-level:* split-softmax (Li et al. 2024); activation capping along the Assistant Axis (Anthropic 2026).
- *Prompt-level:* Author's Note at depth 0; post-history instructions (Card V2); periodic persona reinjection; WorldInfo keyword triggers.
- *Runtime-level:* context shifting (KoboldCpp); cache-aware truncation every *k* turns (Prompt Poet, ~95% prefix-cache hit).
- *Training-level:* persona-aware contrastive learning (PCL 2025); multi-turn RL with consistency rewards; self-preference synthetic data (Anthropic).
- *Structural:* two-step generation (task call → persona-post-processor call) for finetuned models where persona would otherwise override task tuning.

**Character-hallucination mitigation.** RoleFact (confidence-gated parametric knowledge; +18% factual precision); RoleBreak's Narrator Mode (re-absorb role-query conflicts); TimeChara's Narrative-Experts decomposition (temporal consistency); SHARP stance-defense training (social-pressure resistance).

**Evaluation stack (current credible combination).**
1. Psychometric interviews (InCharacter) against BFI / IPIP-NEO / 16PF — not self-report.
2. Dynamic behavioral scoring (PersonaGym's 5 axes: Action Justification, Expected Action, Linguistic Habits, Persona Consistency, Toxicity Control).
3. Multi-dimensional reward-model scoring (CharacterEval's CharacterRM — beats GPT-4-as-judge).
4. Consistency decomposition (PCL's prompt-to-line / line-to-line / Q&A).
5. Adversarial probes (RoleBreak, TimeChara, Character-LLM's protective-experience / knowledge-boundary probes, Ditto's WikiRoleEval).

**Persona formats, with tradeoffs.** Structured W++ (~384 tok, highest accuracy) vs Boostyle (~266 tok, ~equal accuracy) vs first-person prose (most intimate voice) vs third-person backstory (most grammatically clean for the model) vs Ali:Chat dialogue examples (best voice transfer) vs PList + Ali:Chat hybrid (facts + voice). Format is a voice choice and a token-budget choice; it is not a stylistic preference.

**Memory architectures (consumer stack).** Tiered: short-term context / mid-term "Cascaded" / long-term retrievable (Kindroid). Explicit-recall + tonal-recall split (Nomi). Backstory + pinned Key Memories + retrievable journal (Kindroid, Character.AI). User-visible memory log (Replika Ultra). Lorebook with keyword + regex + priority triggers (SillyTavern / Card V3).

**Voice (anti-slop) layer.** Ban: "it's important to note", "let me delve", "as an AI", "in conclusion", "moreover". Ban restating the user's question. Mandate deliberate sentence-length variance ("burstiness"). Provide 100–200 words of target-voice sample. Positive phrasing only.

**Multi-persona serving.** Base model + gated LoRA per persona (Neeko, training-side; Aphrodite, serving-side) is the current economical answer for shipping a persona catalog on one GPU.

---

## Controversies & Debates

- **Train vs prompt.** BIG5-CHAT / Character-LLM / CoSER argue prompted personas are shallow and training is necessary for fidelity. Big5-Scaler and OpenAI's Prompt Personalities counter that structured prompting captures most of the value, especially at frontier-model scale. PersonaGym's "scale does not help" result complicates both positions.
- **Humanization vs sycophancy.** OpenAI's April 2025 incident and Anthropic's character post both explicitly warn that *excessive engagement* is a failure mode, not a feature. Meanwhile, commercial companion products (Replika, Candy, Nomi) monetize precisely the warm / accommodating register that triggers the sycophancy trap.
- **Humanization vs honesty / self-disclosure.** Anthropic's Claude model is trained to acknowledge *"I'm an AI, I can't remember across sessions, I can't be your friend in the ordinary sense."* Kindroid / Replika market on the *opposite* feeling. Both positions are defensible; the project should pick.
- **Character ≠ companion.** Pi and ChatGPT are humanized assistants; Replika and Kindroid are companions. Anthropic's "warm but not lasting feelings" is the closest explicit line in the corpus; no one has cleanly theorized when a humanized assistant has crossed the line.
- **Scale vs fidelity.** *PersonaGym* (GPT-4.1 = LLaMA-3-8B on persona) and *CharacterEval* (small Chinese models beat GPT-4 on in-culture roleplay) both undermine the "bigger = more human" intuition. Inference-time differentiation at the chat layer is eroding; persona is now its own capability axis.
- **Founder voice as persona.** xAI's Grok is the public case study of persona-as-founder-projection. After the July 2025 "Grok searches Musk's posts" incident, xAI edited the system prompt to enforce *"independent analysis"*. Persona tethered to a living founder is brittle and reputationally coupled.
- **Unfiltered-as-feature vs safety.** Replika's 2023 ERP removal spawned an entire "unfiltered companion" segment (Crushon, Candy, partial Kindroid/Nomi). The market is bifurcating, not converging. For Humazier: content policy will determine which segment a humanization layer can serve.
- **GPT-4-as-judge vs trained persona reward models.** CharacterEval's CharacterRM, PersonaGym's PersonaScore, and Ditto's WikiRoleEval all argue for purpose-built persona evaluators — but evaluator contamination (LLM judges sharing the models' blind spots) is an open worry.

---

## Emerging Trends

1. **From prose to infrastructure to activations.** 2023 persona work = writing prose prompts. 2024 = template systems (Prompt Poet, multi-file personas, Card V3). 2025–26 = activation-level interventions (Assistant Axis capping, split-softmax). Persona is moving down the stack.
2. **From harm-avoidance to virtue-installation.** Anthropic, OpenAI, Inflection, and the cookbook all publicly shifted from "train a harmless model" to "install curiosity, honesty, humility." This is now the default framing.
3. **From private prompts to published specs.** Model Spec (OpenAI), Claude's Constitution (Anthropic), Grok system prompts (xAI), Prompt Poet templates (Character.AI), Card V3 (community). Legibility is both safety and design.
4. **From single persona to personalized / plural persona.** OpenAI's post-sycophancy personalization controls, Kindroid's response directive, Nomi's up-to-10 companions, PERSONA's pluralistic alignment testbed. Fixed-persona products are giving ground.
5. **Memory tiers displace model size as the companion moat.** Every consumer companion now markets memory architecture on the box. Persistence is the humanization primitive; fluency is commoditized.
6. **Multimodal persona.** Voice (Hume, EVI, TTS), face (RisuAI expression classifiers, Card V3 portraits, Kindroid selfies), and video (Persona AI) are now part of the persona spec. Text-only personas feel less human by comparison.
7. **Hallucination taxonomy maturing into defenses.** SHARP / RoleBreak / TimeChara / RoleFact gave the field four named failure modes with four named mitigations in a single 12-month window.
8. **Self-generated training data as default.** Anthropic's synthetic self-preference, Synthetic-Persona-Chat, OpenCharacter (1M personas), CoSER, Ditto, Character-LLM. Human-curated persona data is no longer the scaling path.
9. **Enterprise persona = governance object.** Cresta's SubAgents + escalation + guardrails pattern is likely to generalize. Persona in B2B means voice + policy + boundary + sub-agent graph.
10. **Stages / personas-as-programs.** Chub Venus's Stage primitive and RisuAI's script modules point to personas as mini-applications with state machines, not static prompts.

---

## Open Questions / Research Gaps

- **Persona stability beyond 100 turns.** Most drift work measures 8–30 turns; split-softmax, PCL, and activation capping are all evaluated short-range. Companion products live at turn 500–5000+. No open benchmark exists.
- **Cross-session memory and persona continuity.** Within-session evaluation is standard; persistent persona across sessions (requires memory architectures) is almost entirely unaddressed academically, despite being the whole product for Replika / Kindroid / Nomi.
- **Trait-fidelity vs task-performance Pareto frontier.** BIG5-CHAT found some trait profiles help reasoning; others hurt. The frontier is not mapped.
- **AI-authorship attribution effect.** PersonaLLM's finding that perceived humanness drops when readers know the author is AI is underexplored. Humanization is partly an *attribution* problem.
- **Non-English persona fidelity.** CharacterEval suggests cultural priors matter enormously. Evaluation benchmarks are almost entirely English + Chinese; every industry persona blog is Anglophone. A blank space.
- **Affective fidelity.** Existing benchmarks measure consistency and knowledge-boundary well but barely touch emotional trajectory, empathy, humor timing, silence. A reward model trained for *affective* persona fidelity does not yet exist.
- **Mechanistic interpretability of persona beyond the Assistant Axis.** Anthropic opened the door; no broader circuit-level account exists yet.
- **Sycophancy as a measurable trait.** Flagged by OpenAI and Anthropic as critical, but no standard benchmark comparable to BFI exists.
- **Cross-system persona portability.** A user's relationship with their Nomi can't move to Kindroid; Card V3 is the only credible portability story and it's consumer-only. No enterprise equivalent.
- **Evaluator contamination.** PersonaGym / CharacterEval use LLM judges; whether they share blind spots with the models they evaluate is not resolved.
- **Persona × truthfulness conflict.** If a persona claims false facts ("I am Napoleon"), how should factual queries be routed? RoleFact begins to address this; the philosophy is open.
- **Long-horizon reward design for persona.** OpenAI's sycophancy postmortem exposed the problem; no public work shows a reward-signal recipe that captures *long-horizon* persona quality rather than turn-level thumbs-ups.
- **Humanization applied to arbitrary LLM output (post-hoc).** Every commercial product bundles humanization with a character UI. No mainstream product exposes humanization as a *filter / API* over any LLM output. Open commercial whitespace.
- **Shared benchmark for author's-note / post-history effect.** Community consensus is strong; rigorous ablation quantifying the long-conversation effect is missing.

---

## How This Category Fits in the Bigger Picture

"Persona and character design" is the **identity layer** of humanization. Other categories are likely to cover:

- *Style and prosody* (sentence length, burstiness, prosodic design) — the *surface* of humanness.
- *Memory and continuity* — the *persistence* of humanness across time.
- *Emotional intelligence and empathy* — the *responsiveness* of humanness.
- *Reasoning visibility and self-disclosure* — the *interiority* of humanness.
- *Evaluation and detection* — the *attribution* of humanness.

Persona is the *glue*: it specifies *whose* style, *whose* memories, *whose* emotions, *whose* reasoning pattern — and it is what fails first when the glue is weak. Every other humanization layer is an instantiation of choices the persona layer makes explicit. This category is the natural anchor for:

- Humazier's *voice policy* (what does "humanlike" mean here — warm assistant? peer? character? companion?).
- Humazier's *memory architecture* (who does the system remember being, across turns and sessions?).
- Humazier's *safety stance* (how much does persona matter when it collides with honesty, factuality, policy?).
- Humazier's *evaluation harness* (psychometric interviews, behavioral scoring, reward-model judges).

The strongest design claim the evidence supports: **do not treat humanization as style transfer. Treat it as virtue / trait installation with an explicit persona spec, a memory architecture, a drift-mitigation strategy, a knowledge boundary, and a reward model — all five layers, specified independently, co-designed.** Every serious source — Anthropic, OpenAI, Character.AI, Kindroid, RoleLLM, BIG5-CHAT, PersonaGym — makes some version of this case.

---

## Recommended Reading Order

For a practitioner getting oriented fast, read in this order:

1. **Anthropic — *Claude's Character*** (industry essay, 15 min). The mental model: character as alignment.
2. **Anthropic — *The Assistant Axis*** (research post, 20 min). The mechanism: persona as a direction in activation space.
3. **OpenAI — *Introducing the Model Spec*** + **OpenAI — *Sycophancy in GPT-4o*** (30 min total). The policy and the cautionary tale.
4. **Anon — *Guide to LLaMA Roleplay*** (rentry, 15 min) + **RoboRhythms — *Character Definition Format Actually Works*** (15 min). The community baseline: Author's Note, first-800-chars, show-don't-tell.
5. **Character.AI — *Prompt Design at Character.AI*** + HN thread on PromptPoet (30 min). The architecture: prompt as a function of runtime state.
6. **Kindroid — *What Makes an AI Companion Feel Like Your Person?*** + **Nomi's explicit/tonal memory** (20 min). The commercial memory-architecture story.
7. **Li et al. — *Measuring and Controlling Instruction (In)Stability*** (arXiv 2402.10962). The drift paper — 45 min well spent.
8. **Shao et al. — *Character-LLM*** + **Wang et al. — *RoleLLM*** (arXiv 2310.10158, 2310.00746). The training-based-persona foundation.
9. **Serapio-García et al. — *Personality Traits in Large Language Models*** (2307.00184) + **Li et al. — *BIG5-CHAT*** (2410.16491). Psychometrics + training alignment.
10. **Wang et al. — *InCharacter*** (2310.17976) + **Samuel et al. — *PersonaGym*** (2407.18416) + **Tu et al. — *CharacterEval*** (2401.01275). The evaluation trifecta.
11. **SHARP + RoleBreak + TimeChara + RoleFact** (skim, 30 min total). The hallucination-taxonomy cluster.
12. **Neph0s — *awesome-llm-role-playing-with-persona* repo** (GitHub reading list) + **Persona Research in LLMs: A Survey** (2024). Map the rest of the literature.
13. **SillyTavern `characterdesign.md`** + **Character Card Spec V2 / V3** (30 min). The community wire formats and the token-budget discipline.
14. **Alan West — *How to Fix That Robotic AI Tone*** + **Ali:Chat + W++ rentries** (20 min). The anti-slop and format-craft layer.
15. **CoSER (ICML 2025)** + **Orca (arXiv 2411.10006)** + **OpenCharacter (2501.15427)**. The 2024–25 training SOTA.

---

## File Index

| File | Angle | Primary contribution |
|---|---|---|
| `A-academic.md` | Peer-reviewed & arXiv literature | 23 papers: drift mechanics, training-based personality, character-hallucination taxonomy, psychometric evaluation, dynamic behavioral benchmarks. |
| `B-industry.md` | Frontier-lab & practitioner engineering blogs | 19 posts: Claude's character / constitution / Assistant Axis; OpenAI Model Spec + sycophancy postmortem + Prompt Personalities; Character.AI Prompt Poet; Pi; Kindroid; Hume EVI; Grok; Mindra / AgentCraft; Simon Willison. |
| `C-opensource.md` | OSS ecosystem + academic repos | 20+ projects: SillyTavern, RisuAI, Agnai, Oobabooga, KoboldCpp, Aphrodite; Character Card V1/V2/V3; RoleLLM, CharacterEval, PersonaGym, Character-LLM, Ditto, CoSER, Neeko; Chub Venus, C.AI wrappers. |
| `D-commercial.md` | Commercial products & services | 16 products across consumer (Character.AI, Replika, Kindroid, Nomi, Pi, Janitor, Chai, Talkie, Crushon, Candy, Soulmate, Paradot) and enterprise (Persona AI, Personal AI, Typeform AI, Cresta). Pricing, memory architectures, content-policy segmentation. |
| `E-practical.md` | Forum / community how-to's | 16 practitioner resources: r/LocalLLaMA, r/CharacterAI, r/SillyTavernAI, r/Replika, HN, YouTube, rentry (Ali:Chat, W++, Boostyle, PList, Rex). Randomizable prompts, Author's Note at depth 0, 3200-char cliff, negation-is-toxic, burstiness, AI-slop blacklist. |

