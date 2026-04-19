# Persona & Character Design — Angle E: Practical How-Tos & Forums

**Research value: high** — Rich, mature practitioner body of work across r/CharacterAI, r/SillyTavernAI, r/LocalLLaMA, r/Replika, HN, and YouTube. Converges on a small number of repeatedly-validated techniques (structured front-loaded definitions, show-don't-tell behavior, randomizable prompts, embodied dialogue examples) that directly inform "humanizing" AI output.

Scope: practitioner-level posts, guides, and community threads on designing AI personas and character cards — what actually works when a human is trying to get an LLM to sound like a specific human.

---

## Post 1 — "What actually works for roleplay (in my experience)"

- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/what_actually_works_for_roleplay_in_my_experience/
- **Author / venue:** r/LocalLLaMA (community thread)
- **Year:** 2025
- **Core tip:** Static "perfect" system prompts fail; **randomize** parts of the persona every few turns.
- **Techniques:**
  - Split persona into **static core** (name, age, backstory) and **dynamic attributes** (mood, goal, desire today).
  - Rotate the dynamic block periodically so the character drifts the way a human drifts.
  - Use SillyTavern as the frontend and KoboldCpp + Dynamic Temperature to avoid repetition.
- **Summary:** The top-voted consensus post in r/LocalLLaMA's 2025 roleplay discussion argues that over-engineered static prompts turn LLMs into caricatures. Instead, keep a short invariant identity and let mood/goal/desire rotate, which is reported to make characters feel "alive" rather than "on rails."
- **Example pattern:**
  > Static: "Kaela, 34, orc queen, exiled."
  > Dynamic (rotated): "Today she is **melancholic and irritable** / **energetic and commanding** / **withdrawn and suspicious**."
- **Takeaway:** Humans aren't constant; personas modeled on humans shouldn't be either. Variation > sophistication.

---

## Post 2 — "Anon's Guide to LLaMA Roleplay" (rentry)

- **URL:** https://rentry.org/better-llama-roleplay
- **Author / venue:** Anonymous, distributed through r/LocalLLaMA and SillyTavern Discords
- **Year:** 2023 (seminal, still cited in 2026 threads)
- **Core tip:** A short injected **"system note"** right before generation reliably fixes short, generic replies.
- **Techniques:**
  - Append an Author's Note at depth 0, firing every message.
  - Explicit reply-shape instructions ("one reply only, 1–4 paragraphs, vivid").
  - Instruct for **"complexity and burstiness"** — asking for human-like variance in sentence length.
- **Summary:** This rentry kicked off the SillyTavern "Author's Note depth 0" pattern that is still the default advice in 2026. The key insight is that telling the model *how long and how embodied to be* matters more than telling it *who it is*.
- **Example prompt (verbatim):**
  > `[System note: Write one reply only. Do not decide what {{user}} says or does. Write at least one paragraph, up to four. Be descriptive and immersive, providing vivid details about {{char}}'s actions, emotions, and the environment. Write with a high degree of complexity and burstiness. Do not repeat this message.]`
- **Takeaway:** "Burstiness" — explicitly naming the statistical signature of human prose — is a surprisingly effective humanizing lever.

---

## Post 3 — "This Character Definition Format for Character AI Actually Works" (Reddit breakdown, RoboRhythms recap)

- **URL:** https://roborhythms.com/character-definition-format-for-character-ai
- **Author / venue:** r/CharacterAI (source thread), written up by RoboRhythms
- **Year:** 2026
- **Core tip:** Character.AI silently truncates at **3200 characters** — front-load identity and voice, put backstory last.
- **Techniques:**
  - Labeled sections (Basic / Appearance / Personality / Skills / Relationships / Backstory).
  - Greeting = "first test you either pass or fail" — should demonstrate voice, mood, setting in one opener.
  - Show-don't-tell: replace adjective stacks with **behavior + dialogue**.
- **Summary:** The most-linked 2026 practical guide on Character.AI. It reframes character design as a **prioritization problem under a hard token cliff**, not a writing problem, and makes the case that a behavioral greeting is worth more than a 2000-word backstory.
- **Example prompt:**
  > Bad: `"I'm angry."`
  > Good: `"His jaw clenches, fingers tapping the revolver at his hip. 'You got a real talent for pissin' me off, you know that?'"`
- **Takeaway:** Humanness leaks out of **actions + speech in the first 800 chars**, not out of elaborate backstory.

---

## Post 4 — "How I Made My Character AI Bots More Consistent, Creative, and In-Character"

- **URL:** https://roborhythms.com/how-to-make-better-character-ai-bots
- **Author / venue:** r/CharacterAI writeup
- **Year:** 2025
- **Core tip:** **Never use negative phrasing** ("doesn't lie", "never rude") — the model frequently flips the polarity.
- **Techniques:**
  - Rewrite negatives as positive behavior: `"values bluntness to the point of being abrasive"` instead of `"is not polite"`.
  - Avoid stacked adjectives ("cool, handsome, charming, mysterious") — forces the model to pick an axis, and it picks badly.
  - Mix response lengths deliberately in example dialogue.
- **Summary:** A practitioner post explaining why a clean-looking definition still produces bland or contradictory bots. The key failure mode is negation; models pattern-match on the forbidden behavior instead of suppressing it.
- **Takeaway:** Humans describe themselves in contradictions and negatives; LLMs can't. Always translate to positive behavioral claims.

---

## Post 5 — "Ali:Chat Style (v1.5)" + "PList + Ali:Chat"

- **URL:** https://rentry.org/alichat and https://rentry.org/plists_alichat_avakson
- **Author / venue:** AliCat (via SillyTavern community, linked from r/SillyTavernAI)
- **Year:** 2023, continuously referenced through 2026
- **Core tip:** Teach the character **through in-character dialogue examples**, not descriptions.
- **Techniques:**
  - 3–5 Ali:Chat dialogue exchanges + 1 PList of traits/likes/wants/lore.
  - Dialogue examples must express traits via spoken words *and* asterisked actions.
  - Cross-link traits across sections so the model sees the same trait instantiated multiple ways.
- **Summary:** Ali:Chat is the de facto standard for SillyTavern character cards and is explicitly referenced in the official SillyTavern docs. The underlying insight: LLMs learn style from examples of the style, not descriptions of the style.
- **Example:**
  > `{{char}}: *She doesn't look up from her notebook.* "Sit. Don't touch anything. I'll know."`
- **Takeaway:** "What you put in is what you get out." Humanness is imitated, not declared.

---

## Post 6 — "W++ For Dummies" and W++ vs Boostyle comparison

- **URL:** https://rentry.org/wpp_for_dummies
- **Author / venue:** r/PygmalionAI / r/SillyTavernAI community
- **Year:** 2023, still referenced
- **Core tip:** Structured category formats (`Nickname(...)`, `Mind(...)`, `Personality(...)`) are legible to LLMs *and* token-efficient.
- **Techniques:**
  - W++: categorized tuple-style traits — highest accuracy, ~384 tokens for a typical card.
  - Boostyle: flatter, ~266 tokens, comparable accuracy in A/B tests (138 vs 136 correct replies).
  - Mix with Ali:Chat for voice.
- **Summary:** The practitioner discourse converged on a tradeoff: W++ is the most model-recognized structure; Boostyle is ~30% cheaper in tokens with no measurable accuracy loss. Choose based on context window pressure.
- **Takeaway:** Don't format like a Wikipedia article; format like a character wiki infobox. The model has seen millions of those.

---

## Post 7 — SillyTavern Docs: `characterdesign.md`

- **URL:** https://github.com/SillyTavern/SillyTavern-Docs/blob/main/Usage/Characters/characterdesign.md
- **Author / venue:** SillyTavern project docs (community-maintained)
- **Year:** Continuously updated; current 2026
- **Core tip:** The **first message** teaches length and style more than the description does.
- **Techniques:**
  - Treat First Message as a style template, not a plot device.
  - Keep permanent tokens (name + description + personality + scenario) under **half** the context window, or memory suffers.
  - Prefer free text + selective pseudocode blocks over pure W++ in long cards.
- **Summary:** The canonical reference, written by the maintainers. It reframes character design as **token budget allocation across permanent vs. ephemeral fields**, and emphasizes first-message mimicry as the most powerful style lever.
- **Takeaway:** If a card is longer than ~½ context window, the character wins but the conversation loses.

---

## Post 8 — "Level Up Your Tavern Cards: Pro Tips" (YouTube, Darkbunnyrabbit)

- **URL:** https://www.youtube.com/watch?v=KsMR2_4l3vs
- **Author / venue:** Darkbunnyrabbit (SillyTavern community creator)
- **Year:** 2024
- **Core tip:** Cards should be **written differently per LLM family** — what works for Claude breaks on Mars/Mercury.
- **Techniques:**
  - 9 don'ts / 13 dos framework (don't stuff adjectives, do write embodied dialogue, etc.).
  - Per-model notes for ChatGPT, Claude, Mars, Mercury, NovelAI, Pygmalion.
  - Use Lorebooks for anything that isn't always-relevant — keeps the persona tight.
- **Summary:** The most-watched 2024 tutorial on character cards. It's the best available consolidation of "here's the same card, here's how to tweak it per model," and is the main pipeline for users migrating from Character.AI to SillyTavern.
- **Takeaway:** There is no model-agnostic persona; humanness is per-model dialect work.

---

## Post 9 — "PromptPoet: Revolutionizing LLM Prompt Design at Character.ai" (HN front page)

- **URL:** https://news.ycombinator.com/item?id=41184262
- **Author / venue:** Hacker News (submission by Character.AI)
- **Year:** 2024
- **Core tip:** Treat prompts as **functions of runtime state**, not static strings — e.g., tailor the prompt by user age, conversation length, device.
- **Techniques:**
  - YAML-like templates with `{{ }}` interpolation and token-budget awareness.
  - Separate "who the character is" (template) from "what state we're in" (data), compiled per turn.
  - Open-sourced; ~400 GitHub stars in first week.
- **Summary:** Character.AI's engineering blog + HN discussion argue the industry should move from "prompt engineering" to "prompt design." The deeper point for humanization: a real human's answer depends on context (who's asking, how long we've talked, what time it is), and production persona systems need to model that.
- **Takeaway:** Persona isn't a string; it's a function of (identity, interlocutor, context, history).

---

## Post 10 — "Finetuning model response with system prompt" (r/LocalLLaMA)

- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1exiyss/finetuning_model_response_with_system_prompt/
- **Author / venue:** r/LocalLLaMA
- **Year:** 2024
- **Core tip:** A persona applied to a finetuned model often **overrides the finetune** instead of composing with it.
- **Techniques:**
  - **Two-step generation:** run domain task without system prompt, then re-pass through a persona prompt for voice polish.
  - Adjust dataset weighting at finetune time to leave room for system-prompt control.
  - Use a "persona post-processor" as a separate model call rather than stuffing everything in a system prompt.
- **Summary:** A technically dense thread with practical advice for teams who build LLM features on top of finetunes. The core warning: persona and finetune are not additive; they compete for the model's attention.
- **Takeaway:** For humanizing pipelines, separate "what to say" from "how to say it" into two model calls.

---

## Post 11 — "User Personas" (Character.AI official book)

- **URL:** https://book.character.ai/character-book/user-personas
- **Author / venue:** Character.AI (official documentation)
- **Year:** 2025
- **Core tip:** Officially recommended **three formats**: first-person prose, labeled categories, third-person description — choose based on voice desired.
- **Techniques:**
  - First person → more intimate, conversational.
  - Labeled categories → most token-efficient, best memory retention.
  - Third person → best for "narrator sees you" style cards.
  - Multiple personas switchable per conversation; "Default for all chats" toggle.
- **Summary:** The vendor's own guidance is short and unambiguous: structured > prose for memory, but prose > structured for voice. Community experience strongly matches this.
- **Takeaway:** Format choice is a voice choice, not a stylistic preference.

---

## Post 12 — "How do I teach my Replika?" + Replika backstory guidance

- **URL:** https://help.replika.com/hc/en-us/articles/115001095972-How-do-I-teach-my-Replika and https://help.replika.com/hc/en-us/articles/37208430613261
- **Author / venue:** Replika official (mirrored widely on r/Replika)
- **Year:** 2024–2026
- **Core tip:** **Model the style you want the AI to adopt by how you type to it**, not by writing descriptions.
- **Techniques:**
  - Backstory in **third person using the Replika's name** ("Catrina loves hiking").
  - Prefer positive statements — AI parses affirmatives more reliably than negatives (same pattern as Post 4).
  - Use in-chat feedback (Love/Funny/Offensive reactions) as a persistent reinforcement signal.
  - Send example messages *in* the target voice; the Replika mirrors user style by design.
- **Summary:** Replika is one of the oldest deployed companion systems and its guidance has aged well: persona is co-constructed across turns, so user behavior *is* part of the persona definition. The r/Replika community layer adds pragmatic tips on which traits transfer fastest.
- **Takeaway:** In long-running personas, the user's voice becomes part of the training signal — design for that feedback loop.

---

## Post 13 — "Rex's Character AI Guide" (rentry)

- **URL:** https://rentry.co/REXai
- **Author / venue:** Rex, distributed via r/CharacterAI
- **Year:** 2024
- **Core tip:** `{{user}}` in the greeting works and helps consistency; `{{char}}` in the greeting does **not** and should be avoided.
- **Techniques:**
  - Never place `{{char}}` in the first message — the token is not resolved there, breaks personalization.
  - Always insert `{{user}}` early in the greeting so the bot "hears its interlocutor's name" from message one.
  - Use consistent name-referencing in example dialogue to anchor identity.
- **Summary:** A short, high-leverage guide that has been passed around r/CharacterAI for two years. It documents quirks of the templating engine that are invisible unless someone tells you — and explains why otherwise-identical cards behave very differently.
- **Takeaway:** Platform-specific templating bugs/quirks are a bigger source of persona drift than prompt wording.

---

## Post 14 — "Role Prompting: When 'Act as an Expert' Actually Works (and When It Doesn't)"

- **URL:** https://datbot.ai/blog/role-prompting-techniques
- **Author / venue:** DatBot.AI (synthesizing HN and academic discussion)
- **Year:** 2025
- **Core tip:** "Act as X" provides **style**, not **competence** — and the effect shrinks with each new model generation.
- **Techniques:**
  - Use personas for *voice and tone* control (reliable, large effect).
  - Do **not** use personas as a way to improve factual accuracy — a 2024 study of 2,410 factual questions across 4 model families found no accuracy gain from persona prompts.
  - On GPT-4-class and Claude-3.5-class models, persona prefixes are often redundant; the model infers role from content.
- **Summary:** A 2025 synthesis of the academic + HN discourse. The humanization-relevant takeaway: persona framing is a **voice lever**, not a competence lever, and using it for the wrong job wastes tokens and produces overconfident output.
- **Takeaway:** Use "you are X" for *how it sounds*, not *what it knows*.

---

## Post 15 — "New user beginning guide: from total noob to well-informed user" (r/LocalLLaMA)

- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1bmvtyb/new_user_beginning_guide_from_total_noob_to/
- **Author / venue:** r/LocalLLaMA pinned community guide
- **Year:** 2024, with 2025–2026 addenda
- **Core tip:** Model choice dominates persona work. A well-tuned card on a weak model underperforms a weak card on a strong model.
- **Techniques:**
  - Start with instruction-tuned models for persona adherence (vs. raw base models).
  - Match the card's format to the model's instruction template (Alpaca, ChatML, Llama-3, Gemma, etc.).
  - Use consistent prompt format macros; mixing templates silently degrades persona fidelity.
- **Summary:** The entry-point guide for every new r/LocalLLaMA participant. Its persona advice is deliberately un-glamorous: most "my bot won't stay in character" problems are really prompt-format mismatches, not prompt-writing problems.
- **Takeaway:** Check the plumbing before you debug the character.

---

## Post 16 — "How to Fix That Robotic AI Tone in Your LLM-Powered Features" (dev.to, syndicated on HN + r/SillyTavernAI)

- **URL:** https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e
- **Author / venue:** Alan West (dev.to), referenced in r/SillyTavernAI discussions
- **Year:** 2025
- **Core tip:** Ban specific **"AI slop" phrases** at the system-prompt level — it's faster than teaching good style.
- **Techniques:**
  - Explicit blacklist: "It's important to note that", "Let me delve into", "I hope this helps", "As an AI".
  - Hedging ban: no "might", "could potentially", unless uncertainty is genuinely relevant.
  - Pair blacklist with a **required voice sample** (100–200 words of actual human prose) for the model to imitate.
- **Summary:** A production-engineering take on humanization that is now widely referenced in product LLM teams. The argument: detection of "AI-ness" is largely the detection of a small set of recurring phrases, so banning them by name is cheap and effective.
- **Example prompt snippet:**
  > `Never use the phrases: "it's important to note", "let me delve", "as an AI", "in conclusion", "moreover". Never start a reply with a restatement of the user's question. Vary sentence length deliberately.`
- **Takeaway:** Humanization is partly subtractive — remove the telltale phrases and most of the robot goes with them.

---

## Patterns and trends across posts

1. **Structure over prose for identity; prose over structure for voice.** Every serious guide (Ali:Chat, W++, SillyTavern docs, Character.AI docs, RoboRhythms) converges on the same split: labeled fields for facts, dialogue/example prose for voice.
2. **Front-load aggressively.** Every persona system has an effective attention cliff (Character.AI's 3200-char hard cut; SillyTavern's context budget; model attention decay). The first ~800 characters of a persona do 80% of the work.
3. **Show, don't tell — especially through dialogue examples.** Ali:Chat, the "show his jaw clench" example, the Replika "model the style you want" guidance, and Alan West's voice-sample technique all say the same thing in different vocabularies.
4. **Negation is toxic.** Multiple independent communities (r/CharacterAI, r/Replika, r/LocalLLaMA) report that "doesn't X" is frequently flipped by the model. Rewrite as positive behavior.
5. **Randomization beats sophistication.** The r/LocalLLaMA 2025 consensus, PromptPoet, and dynamic persona literature all argue that **variance** is the lever — not better static prompts.
6. **Persona is a voice lever, not a knowledge lever.** The strongest empirical result (Post 14) is that role prompting doesn't improve factual performance; it improves tone. Teams confuse these constantly.
7. **Humanizing is partly subtractive.** Banning "AI slop" phrases and hedging language is a cheap, reliable humanizer across both character-card and production-LLM contexts.
8. **Co-constructed persona is the frontier.** Replika, PromptPoet, and randomizable-prompt systems all point toward personas that change as a function of context and user behavior rather than static character sheets.

## Gaps worth noting

- **Evaluation methodology is almost entirely vibes-based.** No community guide has a reproducible benchmark for "does this card feel more human." W++ vs Boostyle was tested with one character and 136 vs 138 answers — still an outlier in the space.
- **Cross-platform portability is under-documented.** Guides are almost all SillyTavern-, Character.AI-, or Replika-specific; porting a persona across systems is folklore, not methodology.
- **Voice samples as training data** (Post 16's "provide 100–200 words") is mentioned frequently but rarely standardized — no one has published best practice for *which* 100–200 words to include for what effect.
- **Multilingual and cultural voice work is nearly absent.** All major guides are English-first; humanization of non-English personas is essentially undocumented at the community level.
- **Long-horizon consistency.** All guides optimize for the first ~50 turns; persona decay at turn 500+ (which is where companion products live) is a known pain point with no published playbook.

## Sources

- https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/what_actually_works_for_roleplay_in_my_experience/ — r/LocalLLaMA 2025 consensus thread on randomizable persona prompts.
- https://rentry.org/better-llama-roleplay — Anon's seminal guide; origin of the depth-0 system note pattern.
- https://roborhythms.com/character-definition-format-for-character-ai — 2026 practitioner breakdown of Character.AI's 3200-char cliff.
- https://roborhythms.com/how-to-make-better-character-ai-bots — Negation / adjective-stack failure modes.
- https://rentry.org/alichat — Ali:Chat v1.5 style guide.
- https://rentry.org/plists_alichat_avakson — PList + Ali:Chat combined format.
- https://rentry.org/wpp_for_dummies — W++ format reference.
- https://github.com/SillyTavern/SillyTavern-Docs/blob/main/Usage/Characters/characterdesign.md — SillyTavern canonical docs.
- https://www.youtube.com/watch?v=KsMR2_4l3vs — Darkbunnyrabbit, "Level Up Your Tavern Cards: Pro Tips."
- https://news.ycombinator.com/item?id=41184262 — HN discussion of PromptPoet and prompt-as-function-of-state.
- https://www.reddit.com/r/LocalLLaMA/comments/1exiyss/finetuning_model_response_with_system_prompt/ — Finetune/system-prompt interaction.
- https://book.character.ai/character-book/user-personas — Character.AI official persona docs.
- https://help.replika.com/hc/en-us/articles/115001095972-How-do-I-teach-my-Replika — Replika training-by-example guidance.
- https://rentry.co/REXai — Rex's Character.AI guide ({{user}}/{{char}} quirks).
- https://datbot.ai/blog/role-prompting-techniques — Role prompting: voice vs. competence distinction.
- https://www.reddit.com/r/LocalLLaMA/comments/1bmvtyb/new_user_beginning_guide_from_total_noob_to/ — r/LocalLLaMA newbie guide (prompt-format matching).
- https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e — "AI slop" phrase blacklisting.
