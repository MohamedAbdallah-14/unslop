# Persona & Character Design — Angle C: Open-Source & GitHub

> **Project:** Humanizing AI output and thinking
> **Angle:** Survey of open-source projects, community specs, and academic repos that shape how AI personas are authored, stored, played, and evaluated.
> **Research value:** high — a mature open-source stack exists with de-facto standards (character cards V2/V3), multiple production UIs with hundreds of thousands of users, and an active academic sub-field (RoleLLM, CharacterEval, PersonaGym, CoSER, CharacterBox, RoleRAG) producing datasets, benchmarks, and reward models specifically for persona fidelity. Last updated: April 2026.

## Scope

This angle indexes the projects that teach us how open-source communities already "humanize" LLMs through persona design: the runtime frontends that run characters, the card-file formats that serialize a character's identity, the alternative backends that trade censored APIs for controllable local models, and the academic repos that measure whether a persona actually holds up across a conversation.

---

## 1. SillyTavern

- **URL:** https://github.com/SillyTavern/SillyTavern
- **Author:** SillyTavern org (fork of TavernAI, ~200+ contributors)
- **Stars:** ~23,300 (corrected April 2026; prior entries overstated at ~25,900)
- **Updated:** Actively maintained (2026)
- **License:** AGPL-3.0
- **Description:** Locally-installed LLM frontend positioned as "LLM Frontend for Power Users." De-facto standard UI for character-based roleplay across dozens of LLM APIs.
- **Techniques:**
  - Character card (V1/V2/V3) import/export via PNG tEXt chunks, JSON, and CHARX zip.
  - WorldInfo / Lorebook system — keyword-triggered context injection to simulate long-term knowledge without blowing the context window.
  - Prompt macros (`{{char}}`, `{{user}}`, `{{random}}`, `{{pick}}`) for reusable persona templates.
  - Author's Note, post-history instructions, jailbreak slots, and group chats with turn-taking logic.
  - Extensions API (TTS, image gen via A1111/ComfyUI, expression sprites, translate, summarize).
- **Takeaways for humanization:** SillyTavern's prompt order (system → persona → scenario → WorldInfo → history → post-history instructions) is the community-hardened recipe for keeping a persona stable across long chats. The Lorebook pattern is the most battle-tested "soft memory" technique in the open-source world and directly addresses context-window-induced persona drift. February 2026 release added ComfyUI/Flux integration for multimodal persona image generation; persona avatar aspect ratio preservation added to UI.
- **Summary:** SillyTavern is the dominant open-source chat UI for persona roleplay, the reference implementation for the character card spec, and the main testbed where community prompt engineering gets hardened. Any serious "humanizing AI" work should study its prompt template, macro system, and WorldInfo triggering before re-inventing.
- **README quote:** "SillyTavern is a locally installed user interface that allows you to interact with text generation LLMs, image generation engines, and TTS voice models."

## 2. TavernAI

- **URL:** https://github.com/TavernAI/TavernAI
- **Author:** Humi (TavernAI org)
- **Stars:** ~2,667
- **Updated:** Slow maintenance; forked heavily (SillyTavern is the most active descendant).
- **License:** MIT
- **Description:** "Atmospheric adventure chat for AI language models" — the original ancestor of the modern character-card frontend lineage.
- **Techniques:** Character creation UI, online character database, group chat, story mode, World Info, message swiping, theme/background customization.
- **Takeaways:** TavernAI is where the "atmospheric," visual-novel-inspired persona UX was established — background, portrait, first-message greeting, and message swiping as a cheap branch-sampler. Those UX primitives turn out to matter for felt humanness as much as the prompt does.
- **Summary:** Historically important as the progenitor of the modern character-card ecosystem; still useful as a minimal reference. Most innovation has migrated to SillyTavern, but TavernAI's schema and UX conventions remain the vocabulary everyone else speaks.
- **README quote:** "TavernAI is an atmospheric frontend for chat and storywriting, compatible with KoboldAI, Pygmalion, NovelAI, OpenAI ChatGPT, and GPT-4."

## 3. Character Card Spec V2

- **URL:** https://github.com/malfoyslastname/character-card-spec-v2
- **Author:** malfoyslastname et al.
- **Stars:** widely adopted spec repo
- **Updated:** Frozen "validated" spec (May 2023) — still the most widely supported format.
- **Description:** JSON spec for serializing a character into a portable, PNG-embeddable file.
- **Techniques / fields introduced over V1:**
  - `creator_notes` (OOC guidance for users)
  - `system_prompt` (dedicated persona system prompt)
  - `post_history_instructions` (stays close to the output, used to re-anchor style)
  - `alternate_greetings` (multiple opening hooks)
  - `character_book` (in-card lorebook with structured entries)
  - `tags`, `creator`, `character_version`, `extensions`
- **Takeaways:** V2 codifies the architecture of a "humanized" persona: a persistent system prompt, a rolling lorebook, and recency-weighted instructions that fight LLM drift by re-asserting voice after the chat history. The `extensions` escape hatch is how the community ships experimental humanization tricks without breaking the spec.
- **Summary:** The most widely supported character file format in open-source AI roleplay. Understanding its fields is effectively understanding the community's empirical theory of what a persona needs to stay in character.
- **README quote:** "All V1 fields remain in V2. Character Card V2 is a superset of V1, intended to be backwards-compatible."

## 4. Character Card Spec V3

- **URL:** https://github.com/kwaroran/character-card-spec-v3
- **Author:** kwaroran (RisuAI maintainer)
- **Stars:** active spec repo
- **Updated:** "Living Standard" status (2024–2026)
- **Description:** Successor spec extending V2; adds richer asset handling, group personas, and the CHARX container format.
- **Techniques:**
  - Three embedding methods: PNG/APNG `ccv3` tEXt chunk, raw JSON, and CHARX (zip with `card.json` + `embeded://` asset URIs).
  - Expanded lorebook (decorators, regex triggers, priority, selective logic).
  - First-class support for assets (expression portraits, background images, audio) bundled alongside the persona.
  - Group greeting, `source` provenance, and asset-aware backfill rules for V2 consumers.
- **Takeaways:** V3 is where the community admits that personas are multimodal: a voice, a face, a soundscape, and a lore graph. If the goal is humanization, V3's asset bundling + CHARX is the clearest open-source blueprint for "a character is more than a prompt."
- **Summary:** The emerging standard for portable multimodal personas. Implemented by RisuAI and partially by SillyTavern; worth tracking because it will likely absorb V2 over the next 12–18 months.
- **README quote:** "Character Card V3 is a proposal for an updated character card specification... extends V2 with new features for various platforms."

## 5. RisuAI

- **URL:** https://github.com/kwaroran/RisuAI
- **Author:** kwaroran
- **Stars:** ~1,300+
- **Updated:** Active (2026)
- **License:** GPL-3.0
- **Description:** Cross-platform (web + Tauri desktop) character chat app, and the reference implementation of character card spec V3.
- **Techniques:** Multi-format card import (JSON / PNG / CHARX), group chats, emotion image switching (expressions driven by classifier output), lorebook, regex script hooks, and a plugin/module system.
- **Takeaways:** RisuAI treats the persona as a runtime with pluggable scripts rather than a static prompt — regex post-processors, emotion classifiers, and trigger modules let the character *react* in human ways (facial expressions, tone shifts) without the base model knowing. This is a strong pattern for humanization via orchestration rather than purely via prompting.
- **Summary:** Modern, TypeScript/Svelte-based chat UI that pushes character cards past text into orchestrated multimodal personas. The cleanest codebase to read if you want to understand how spec V3 gets implemented end-to-end.

## 6. Agnai (Agnaistic)

- **URL:** https://github.com/agnaistic/agnai
- **Author:** sceuick et al.
- **Stars:** ~703
- **Updated:** Active (2026)
- **License:** AGPL-3.0
- **Description:** Multi-user, multi-bot, AI-agnostic character chat backend + frontend designed for hosted deployments.
- **Techniques:**
  - Multiple persona schemas: W++, Square Bracket Format (SBF), Boostyle, plain text — lets authors pick the serialization that best fits the model.
  - Memory/Lore books with embedding-based retrieval; optional Wikipedia / PDF ingestion for factual grounding.
  - Chat branching and forking as first-class UX.
  - AI-assisted character generation.
  - Multi-tenant architecture (auth, per-user presets, group sessions).
- **Takeaways:** Agnai demonstrates that persona schemas are not one-size-fits-all — W++ and SBF work better on smaller open-weight models, plain prose works better on frontier models. Humanization pipelines should probably support multiple serializations and pick per target model.
- **Summary:** The canonical multi-user, server-deployable open-source persona chat platform. Its schema flexibility and retrieval-backed lorebook are the clearest guide to shipping personas as a service rather than a desktop toy.

## 7. Oobabooga text-generation-webui

- **URL:** https://github.com/oobabooga/text-generation-webui
- **Author:** oobabooga
- **Stars:** ~46,400
- **Updated:** Active (2026), v4.0 released.
- **License:** AGPL-3.0
- **Description:** "The original local LLM interface. Text, vision, tool-calling, training, and more. 100% offline."
- **Techniques:** Multiple model loaders (transformers, llama.cpp, ExLlama, HQQ, etc.), LoRA training, character tab with TavernAI-compatible PNG cards, instruction templates per model family, Chat/Default/Notebook modes, extensions (long-term memory, tool use, TTS).
- **Takeaways:** Oobabooga is where the community debugged the boring-but-critical pieces of persona humanization: per-model chat templates, correct stop-strings, sampler settings (temperature, top-p, min-p, DRY, XTC) that control how "alive" the output feels. A humanization stack without careful sampler control will underperform no matter how good the persona prompt is.
- **Summary:** The dominant local inference frontend; not a pure persona tool, but every serious character deployment passes through its sampler and template conventions. Its chat template registry is a de-facto source of truth for "how do I prompt model X as a character."

## 8. KoboldAI-Client

- **URL:** https://github.com/KoboldAI/KoboldAI-Client
- **Author:** KoboldAI community (henk717 fork active)
- **Stars:** ~3,868
- **Updated:** Still maintained; increasingly superseded by KoboldCpp.
- **Description:** Browser-based frontend for AI-assisted writing (novel, adventure, chat modes); the original "bring your own model" roleplay UI.
- **Techniques:** Memory + Author's Note + World Info triad (the pattern SillyTavern later inherited), adventure-mode action parsing, softprompt support.
- **Takeaways:** Kobold's "Author's Note" — a prompt injection that always sits N tokens before the latest output — is the oldest and still the most reliable trick for re-asserting voice/style on long chats. Any humanization system should steal this pattern.
- **Summary:** Ancestor of modern local roleplay tooling; historically important and still a reference for memory/author's-note mechanics.

## 9. KoboldCpp

- **URL:** https://github.com/LostRuins/koboldcpp
- **Author:** LostRuins
- **Stars:** ~9,900
- **Updated:** Very active (2026)
- **License:** AGPL-3.0
- **Description:** Single-binary C++ inference server built on llama.cpp, exposing a KoboldAI-compatible HTTP API plus its own chat UI.
- **Techniques:** GGUF-only, CPU/CUDA/ROCm/Vulkan/Metal backends, context shifting (avoids reprocessing full context on every turn), grammar-constrained output (GBNF), MMQ quant kernels, image model support, tool calls.
- **Takeaways:** Context shifting is a big deal for persona coherence — it lets the system prompt and first-message greeting stay pinned while old turns are evicted, which keeps persona drift measurably lower in long sessions.
- **Summary:** The preferred inference backend for people who want a local, low-friction engine behind SillyTavern / Agnai / RisuAI. Its context-shift and grammar-constraint features are tools a humanization pipeline can use without asking the model nicely.

## 10. PygmalionAI / Aphrodite Engine

- **URL:** https://github.com/PygmalionAI/aphrodite-engine
- **Author:** PygmalionAI + Ruliad
- **Stars:** ~1,683
- **Updated:** Active (2026)
- **License:** AGPL-3.0
- **Description:** vLLM-based large-scale LLM inference engine built for roleplay backends; OpenAI-compatible API with aggressive quant and multi-LoRA support.
- **Techniques:** Paged Attention + continuous batching, extensive quant (AQLM, AWQ, GPTQ, GGUF, FP8), speculative decoding, multi-LoRA, heterogenous hardware (NVIDIA / AMD / Intel XPU / TPU).
- **Takeaways:** PygmalionAI historically trained roleplay-specific base models (Pygmalion-6B, Pygmalion-13B, Mythalion); Aphrodite is their serving half. The takeaway is that the community found "base model + LoRA per persona style" more economical than full fine-tunes for humanization.
- **Summary:** The production inference engine of the roleplay ecosystem. Its multi-LoRA path is the cheapest known way to ship N personas on one base model — directly relevant to any system that wants a catalog of voices without N full checkpoints.

## 11. CharHubAI (Chub Venus) open tooling

- **URL:** https://github.com/CharHubAI
- **Author:** CharHubAI org (runs chub.ai / venus.chub.ai)
- **Stars:** org-level; individual repos are small (stage-template ~31, proxy ~26).
- **Updated:** Active.
- **Description:** Open-source pieces of the Chub Venus platform (character browser with 60k+ user cards): CORS/API proxy, Pydantic type schemas, "Stage" template for interactive mini-apps, expressions extension.
- **Techniques:** Stages = scripted, reactive character experiences (essentially mini-apps around a card); proxy pattern to let browser clients call Anthropic/OpenAI without CORS pain; typed Pydantic models for the platform's object graph.
- **Takeaways:** The "Stage" primitive is an under-appreciated humanization idea — a character is not just a prompt but a small program that can render UI, branch, and maintain state. Worth studying as a design target.
- **Summary:** Not a single repo but the open half of the largest community character marketplace. The Stage template and types-pydantic repos are the concrete artifacts most worth reading.

## 12. Neph0s/awesome-llm-role-playing-with-persona

- **URL:** https://github.com/Neph0s/awesome-llm-role-playing-with-persona
- **Author:** Neph0s (also behind CoSER)
- **Stars:** ~1,000+
- **Updated:** Active curation.
- **Description:** Curated index of papers, datasets, and code for LLM role-playing with assigned personas; anchored on the survey *"From Persona to Personalization: A Survey on Role-Playing Language Agents"* (TMLR 2024).
- **Techniques:** Taxonomy spanning demographic personas, personalization, multi-agent, personality traits, and theory-of-mind.
- **Takeaways:** This is the single fastest on-ramp to the academic literature on persona LLMs. Anyone scoping a humanization roadmap should diff their planned features against this taxonomy first.
- **Summary:** The definitive community-maintained reading list for persona LLMs. Use as a map; cite the TMLR survey as the anchor.

## 13. InteractiveNLP-Team/RoleLLM-public

- **URL:** https://github.com/InteractiveNLP-Team/RoleLLM-public
- **Author:** Wang et al.
- **Stars:** ~522
- **Updated:** Last updated October 2024.
- **Description:** Role-play framework with four stages — role profile construction (100 roles), Context-Instruct, RoleGPT prompting, and RoCIT (role-conditioned instruction tuning).
- **Techniques:** **RoleBench** (168,093 samples, first systematic character-level benchmark), RoleGPT prompting recipe, RoleLLaMA (English) and RoleGLM (Chinese) fine-tuned models approaching GPT-4 on in-character metrics.
- **Takeaways:** RoleLLM shows that a carefully constructed profile + a small instruction-tuned model can rival prompted GPT-4 on persona fidelity. Important evidence that humanization is a fine-tuning problem at least as much as a prompting problem.
- **Summary:** Foundational academic work with reusable benchmark + models. The benchmark alone is reason enough to clone it when evaluating any humanization claim.

## 14. morecry/CharacterEval

- **URL:** https://github.com/morecry/CharacterEval
- **Author:** Tu et al. (ACL 2024)
- **Stars:** ~289
- **Updated:** Maintained post-ACL 2024.
- **License:** MIT
- **Description:** Chinese benchmark for Role-Playing Conversational Agents: 1,785 multi-turn dialogues / 23,020 examples across 77 characters from Chinese novels and scripts.
- **Techniques:** 13 metrics across 4 dimensions (conversational ability, character consistency, role-playing attractiveness, personality back-testing); ships **CharacterRM**, a trained reward model whose Pearson correlation with human judgments exceeds GPT-4's.
- **Takeaways:** The CharacterRM reward model is directly reusable as an automatic humanness judge — cheaper and higher-correlation than GPT-4-as-judge for persona fidelity in long dialogues. Strong candidate for an in-loop quality gate.
- **Summary:** The most rigorous open benchmark + reward model for persona consistency to date. Chinese-centric but the methodology generalizes.

## 15. PersonaGym

- **URL:** https://personagym.com/ (paper code linked; project page hosts repo)
- **Author:** Samuel, Mulakala, Cerniglia, Khatri et al. (2024)
- **Stars:** research project, code released.
- **Description:** First *dynamic* evaluation framework for persona agents — environments and questions are generated per persona rather than fixed.
- **Techniques:** Five evaluation dimensions — Action Justification, Expected Action, Linguistic Habits, Persona Consistency, Toxicity Control. Introduces **PersonaScore**, a decision-theoretic auto-metric aligned to human judgment. Benchmarks 10 LLMs across 200 personas with 10,000 questions.
- **Takeaways:** Key finding that humanization work should internalize: model size does not reliably improve persona capability — GPT-4.1 scores similarly to LLaMA-3-8B on PersonaScore. Humanization is orthogonal to scale, which means careful scaffolding and evaluation matter more than picking the biggest model.
- **Summary:** State-of-the-art evaluation harness for persona agents; the best available answer to "is my persona actually working?"

## 16. choosewhatulike/trainable-agents (Character-LLM)

- **URL:** https://github.com/choosewhatulike/trainable-agents
- **Author:** Shao et al. (EMNLP 2023)
- **Stars:** ~620
- **Updated:** Maintained; 9 character weights released.
- **Description:** Treats each character as a trainable agent rather than a prompt; uses "Experience Reconstruction" to synthesize in-character training data from profiles.
- **Techniques:** Profile → experience graph → in-scene dialogue synthesis → character-specific fine-tune; released per-character weights (Beethoven, Cleopatra, Caesar, Spartacus, Hermione, etc.); evaluates with a "protective experience" probe that adversarially attacks character knowledge boundaries.
- **Takeaways:** Experience Reconstruction is a transferable pipeline for generating persona training data at scale — the whole approach is effectively "dataset synthesis for humanization." The knowledge-boundary probe (asking Beethoven about smartphones) is a cheap but powerful fidelity test.
- **Summary:** The most influential academic proof-of-concept that personas can be *trained* into weights rather than prompted in. Its data-synthesis recipe is directly applicable to any custom persona pipeline.

## 17. OFA-Sys/Ditto

- **URL:** https://github.com/OFA-Sys/Ditto
- **Author:** Alibaba OFA-Sys
- **Stars:** ~210
- **Description:** Self-alignment method for role-play; reframes role-play as a reading-comprehension task so that any instruction-tuned LLM can self-generate role-play training data from character knowledge.
- **Techniques:** 4,000-character self-generated dataset (10x prior datasets); **WikiRoleEval** benchmark with three axes — consistent role identity, role-specific knowledge, knowledge boundary awareness.
- **Takeaways:** Self-alignment removes the human-labeling bottleneck, which matters if you want to scale personas beyond a hand-curated cast. The knowledge-boundary metric pairs well with Character-LLM's probe.
- **Summary:** Important evidence that roleplay capability can be bootstrapped without human-written dialogues. WikiRoleEval is a solid third evaluator alongside RoleBench and CharacterEval.

## 18. Neph0s/CoSER

- **URL:** https://github.com/Neph0s/CoSER
- **Author:** Wang et al. (ICML 2025)
- **Description:** Dataset + open models + evaluation protocol for role-playing language agents, covering 17,966 characters from 771 renowned books with authentic dialogues, character experiences, and internal thoughts.
- **Techniques:** "Given-Circumstance Acting" — LLMs sequentially portray multiple characters in the same book scene; training data includes explicit internal thought traces. Released CoSER-8B and CoSER-70B (LLaMA-3.1 backbone); 70B matches or beats GPT-4o (75.80% on InCharacter, 93.47% on LifeChoice).
- **Takeaways:** Training on *internal thoughts*, not just dialogue, is an underused humanization lever — it teaches the model to simulate the hidden state that makes speech feel motivated rather than generic. Worth borrowing even if CoSER's exact data isn't reused.
- **Summary:** Current SOTA open weights for persona simulation. The internal-thought training signal is the most interesting methodological idea in this cluster.

## 19. weiyifan1023/Neeko

- **URL:** https://github.com/weiyifan1023/Neeko
- **Author:** Yu et al. (EMNLP 2024)
- **Description:** Dynamic-LoRA framework for multi-character role-playing: one LoRA block per character plus a gating network that routes tokens to the right persona.
- **Techniques:** Agent pre-tuning → multi-character playing → character incremental learning (cold-start for new roles without retraining the base).
- **Takeaways:** Gated per-persona LoRAs are the most parameter-efficient way yet shown to host many distinct personas on one base model, and the incremental-learning stage is a clean pattern for "add a new persona without regressing existing ones."
- **Summary:** Complements Aphrodite's multi-LoRA serving with a training-time recipe. Together they form a plausible "N personas, one GPU" stack.

## 20. Character.AI community wrappers

- **kramcat/characterai** — https://github.com/kramcat/characterai — ~537 stars, MIT, async/sync wrapper around the unofficial C.AI endpoints.
- **Xtr4F/PyCharacterAI** — https://github.com/Xtr4F/PyCharacterAI — ~95 stars, MIT, async wrapper with structured `persona` methods (`fetch_my_persona`, `create_persona`).
- **Takeaway:** Character.AI itself is closed, but these reverse-engineered clients expose the data model that made C.AI's personas sticky — persona text, greeting, definitions, and *user-level* personas distinct from character-level. The split between a user's persona and the character's persona is a humanization primitive worth copying into any new system.

## 21. CharacterBox (NAACL 2025)

- **URL:** https://aclanthology.org/2025.naacl-long.323/ (paper: arXiv:2412.05631)
- **Author:** Haoxuan Li et al. (Peking University)
- **Stars:** Research release
- **Updated:** 2025
- **Description:** A simulation sandbox for generating fine-grained character behavior trajectories. Two-agent architecture: a character agent grounded in psychological and behavioral science, and a narrator agent that coordinates character interactions and environmental changes.
- **Techniques:** Text-world simulation; dynamic trajectory generation; dual-agent (character + narrator) evaluation framework.
- **Takeaways:** Extends evaluation past static QA into dynamic world-simulation. Useful as a benchmark when evaluating persona designs for open-ended interactive agents and games, not just chat.
- **Summary:** State-of-the-art simulation-based evaluation for role-playing capability in text-world contexts. Complements PersonaGym and CharacterEval in the evaluation stack.

## 22. RoleRAG

- **URL:** https://arxiv.org/abs/2505.18541
- **Author:** Multiple institutions
- **Stars:** Research release (2025)
- **Description:** Retrieval-Augmented Generation applied specifically to character knowledge management. Combines entity disambiguation for knowledge indexing with a boundary-aware retriever that extracts contextually appropriate information from a structured knowledge graph.
- **Techniques:** Knowledge graph construction; entity disambiguation; boundary-aware retrieval; calibrated retrieval to reduce character knowledge hallucination.
- **Takeaways:** The retrieval-side complement to confidence-gating (RoleFact) for managing character knowledge boundaries. Applicable wherever persona has a bounded, verifiable knowledge domain (historical figures, IP characters, enterprise personas).
- **Summary:** Addresses character knowledge hallucination from the retrieval rather than the training side. Benchmarks show improved character knowledge accuracy and fewer hallucinated responses for both general-purpose and role-specific LLMs.

## 23. nuochenpku/Awesome-Role-Play-Papers

- **URL:** https://github.com/nuochenpku/Awesome-Role-Play-Papers
- **Author:** nuochenpku et al.
- **Stars:** Active curation (2025–2026)
- **Description:** Curated reading list of role-playing papers, complementary to Neph0s/awesome-llm-role-playing-with-persona. Organized around the Wang et al. (2026) survey (arXiv:2601.10122) categorization: cognitive simulation, language-style imitation, and rule-based paradigms.
- **Takeaways:** A second useful entry-point for the academic literature, with different curation priorities from the Neph0s list. Cross-referencing both gives the broadest coverage.
- **Summary:** Secondary canonical reading list; useful for papers published after the TMLR 2024 survey cutoff.

---

## Patterns

- **Character cards are the lingua franca.** V1 → V2 → V3 is the shared wire format across SillyTavern, RisuAI, Agnai, Chub Venus, Oobabooga, and Backyard AI. Any humanization system that wants to plug into this ecosystem should import/export cards, not invent a new format.
- **A persona is system prompt + lorebook + post-history instructions + samplers.** Every mature frontend converges on the same four knobs; the interesting differences are in retrieval triggers and sampler defaults, not in the presence of the knobs themselves.
- **Drift is fought with *recency* tricks, not bigger context windows.** Author's Note (Kobold), post-history instructions (card V2), context shifting (KoboldCpp), and WorldInfo keyword triggers (SillyTavern) all exist because pinning the persona near the bottom of the prompt is more reliable than pinning it near the top.
- **Multimodality is sneaking back in.** Expression portraits, TTS, sound cues, and background art are returning via V3 / CHARX and RisuAI's runtime. Text-only personas feel less human by comparison.
- **Academic work has converged on three evaluation axes.** Consistency (do you stay in character?), knowledge-boundary (do you correctly *not* know things?), and linguistic habits (do you talk like this person?) — RoleBench, CharacterEval, PersonaGym, WikiRoleEval all triangulate the same triangle.
- **Multi-LoRA is the economical path to catalogs.** Neeko (training) + Aphrodite (serving) show the template: one base model, gated LoRAs, incremental-learning pipeline for new personas.
- **Self-generated training data is now credible.** Character-LLM's Experience Reconstruction and Ditto's self-alignment both demonstrate that good persona data can be synthesized from profiles alone — eliminating the human-authoring bottleneck that historically blocked scale.

## Trends (2024 → 2026)

- **Spec consolidation** — V3 and CHARX are winning as the portable persona container; expect V2 to be a legacy compatibility target within 12–18 months.
- **Training > prompting for fidelity** — recent academic results (CoSER 70B > GPT-4o on InCharacter) argue that humanization is migrating from a prompt-engineering problem to a data + fine-tuning problem.
- **Reward-model-as-judge** — CharacterEval's CharacterRM, PersonaGym's PersonaScore, and Ditto's WikiRoleEval signal a move away from GPT-4-as-judge toward purpose-built persona evaluators. Cheaper and more aligned with human ratings.
- **Stages / runtime personas** — Chub's Stage primitive and RisuAI's script modules point to personas-as-programs: state machines and mini-UIs wrapped around a card rather than static prompts.
- **Small models with persona-specific LoRAs** are catching up to frontier models on in-character metrics, especially outside English (RoleGLM, CharacterEval Chinese).
- **Simulation-based evaluation** — CharacterBox and RPEval signal a third evaluation paradigm after static benchmarks and dynamic QA environments: full narrative world simulation with a narrator agent. Relevant for game NPCs, interactive fiction, and agent personas.
- **Retrieval-augmented persona (RAP)** — RoleRAG formalizes RAG-based character knowledge management as a research area. Expect more RAP work as knowledge-boundary hallucination remains a top failure mode.
- **SillyTavern ComfyUI/Flux integration** (Feb 2026) marks multimodal persona going mainstream in open-source: expression images generated in-session as part of persona expression, not as a bolt-on.

## Gaps

- **Evaluation is English + Chinese heavy.** Almost no open persona benchmarks for low-resource languages, dialects, or sociolects — a real blocker for humanization across global audiences.
- **No shared benchmark for *affective* fidelity.** Existing benchmarks measure consistency and knowledge boundaries well but barely touch emotional trajectory, empathy, humor timing, or silence — the subtler signals of humanness.
- **Long-horizon memory is still hacky.** Lorebooks + embeddings are the state of the art, but there's no open benchmark for "does this persona remember correctly after 1,000 turns?"
- **User-side persona is under-specified.** Character.AI exposes user personas as first-class; open-source card specs mostly treat the user as `{{user}}`. A humanizing system probably needs symmetric persona modeling on both sides.
- **Safety / toxicity evaluation is siloed.** PersonaGym is the only framework that bakes toxicity control into its core axes; most persona benchmarks sidestep it entirely.
- **No canonical *author's note / post-history* benchmark.** We have strong community consensus that these tricks work but no rigorous ablation quantifying their effect on long-conversation persona drift — a concrete, high-value research gap.

## Sources

- SillyTavern repo — https://github.com/SillyTavern/SillyTavern
- TavernAI repo — https://github.com/TavernAI/TavernAI
- Character Card V2 spec — https://github.com/malfoyslastname/character-card-spec-v2
- Character Card V3 spec — https://github.com/kwaroran/character-card-spec-v3
- RisuAI — https://github.com/kwaroran/RisuAI
- Agnaistic — https://github.com/agnaistic/agnai
- text-generation-webui — https://github.com/oobabooga/text-generation-webui
- KoboldAI-Client — https://github.com/KoboldAI/KoboldAI-Client
- KoboldCpp — https://github.com/LostRuins/koboldcpp
- Aphrodite Engine — https://github.com/PygmalionAI/aphrodite-engine
- CharHubAI org — https://github.com/CharHubAI
- awesome-llm-role-playing-with-persona — https://github.com/Neph0s/awesome-llm-role-playing-with-persona
- RoleLLM-public — https://github.com/InteractiveNLP-Team/RoleLLM-public
- CharacterEval — https://github.com/morecry/CharacterEval (paper: arXiv 2401.01275)
- PersonaGym — https://personagym.com/ (paper: arXiv 2407.18416)
- Character-LLM / trainable-agents — https://github.com/choosewhatulike/trainable-agents (paper: arXiv 2310.10158)
- Ditto — https://github.com/OFA-Sys/Ditto
- CoSER — https://github.com/Neph0s/CoSER
- Neeko — https://github.com/weiyifan1023/Neeko (paper: arXiv 2402.13717)
- kramcat/characterai — https://github.com/kramcat/characterai
- Xtr4F/PyCharacterAI — https://github.com/Xtr4F/PyCharacterAI
