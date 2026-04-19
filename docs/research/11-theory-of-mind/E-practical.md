# Theory of Mind in AI — Angle E: Practical How-Tos & Forums

**Research value: high** — Forums, blogs, and explainer content on ToM in LLMs are abundant, opinionated, and contain concrete prompt techniques, reproducible critiques, and recurring debate patterns directly applicable to humanizing AI output.

Project context: *Unslop* — humanizing AI output and thinking. The posts below are the live public conversation (developers, researchers, practitioners, skeptics) about whether and how LLMs "model" users, and how to prompt for it.

---

## 1. HN — "GPT-4 performs better at Theory of Mind tests than actual humans"

- **Source type:** Hacker News discussion thread
- **URL:** https://news.ycombinator.com/item?id=35765786
- **Date:** April 2023 (Kosinski preprint wave)
- **Audience:** ML engineers, AI-curious devs
- **Top signal:** Skepticism about training contamination; the Chinese Room re-emerges.
- **Representative quote:**
  > "These models have been trained on enormous amounts of text, including theory of mind tests… I would actually be a bit surprised if the models failed this type of test regardless of whether they have any understanding of theory of mind."
- **Secondary quote (pro-emergence):**
  > "There is no meaningful difference between 'fake' thinking and 'real' thinking. Especially when you arrive at this imaginary distinction with 'It's fake because it has to be fake'."
- **Pattern:** "Contamination vs. emergence" argument is the most frequent framing.

## 2. HN — "Large language models have developed a higher-order theory of mind"

- **Source type:** HN thread on Street et al. 2024 (Nature Human Behaviour–adjacent)
- **URL:** https://news.ycombinator.com/item?id=40854930
- **Audience:** ML practitioners, AI-safety lurkers
- **Top signal:** Higher-order (nested) ToM ("I think that you believe that she knows") shifts even skeptics' views.
- **Representative quote:**
  > "Proving theory of mind in LLMs is certainly one step toward recognizing that they are well on the path of acquiring 'human-like' intelligence… Theory of mind is obviously coupled with the recognition that we can be outsmarted."
- **Takeaway for Unslop:** 6th-order inference claim is where the "it's just autocomplete" rebuttal runs out of fuel in public debate.

## 3. HN — "LLMs, Theory of Mind, and Cheryl's Birthday"

- **Source type:** HN thread (Oct 2024)
- **URL:** https://news.ycombinator.com/item?id=41745788
- **Audience:** Devs, puzzle-minded engineers
- **Top signal:** Failures on *perturbed* classic puzzles are the most popular "disproof" currently circulating.
- **Representative quote:**
  > "The goalposts keep moving" — from Turing test to demanding proof of ToM.
- **Gap it exposes:** Practitioners conflate puzzle-solving with mentalizing. Cheryl's Birthday requires embedded-knowledge reasoning; most LLMs succeed on the canonical version, fail on close variants — a cheap probe.

## 4. LessWrong — "Evaluating GPT-4 Theory of Mind Capabilities" (gcmac & Nathan Labenz)

- **Source type:** Long-form LessWrong experimental writeup, Aug 2023
- **URL:** https://www.lesswrong.com/posts/Ce82o8mbBfH9N3Jes/evaluating-gpt-4-theory-of-mind-capabilities
- **Audience:** AI-safety / alignment community
- **Top signal:** First widely-shared *hands-on* replication with prompt engineering. Includes GitHub + Replit.
- **Representative quote:**
  > "Deception is a key component to many of the scenarios that concern the AI safety community, and theory of mind is a key component of deception."
- **Practical recipe surfaced:** CoT prompt with explicit "world rules" ("characters know who else is in the same location… object-is-in-location observations are known to all characters") took TOMI accuracy from ~70% to 81%, and to ~87% after removing dataset errors.
- **Highly relevant for Unslop:** Shows that ToM is *promptable* — bad priors in the base prompt are what fail, not the model.

## 5. LessWrong — "Simulators" (Janus)

- **Source type:** Canonical LessWrong essay, Sept 2022
- **URL:** https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators
- **Audience:** Alignment, prompt engineers
- **Top signal:** Recasts LLMs as simulators generating "simulacra" — not agents with a ToM, but engines capable of running many ToMs on demand.
- **Representative framing:** GPT isn't trying to answer; it is completing patterns. Different prompts yield different simulacra, each with its own mental model.
- **Why it matters for Unslop:** The "persona as simulacrum" frame is the philosophical backbone of every humanization prompt ("you are a warm, empathetic friend") that currently ships in production.

## 6. LessWrong — "Emergent Introspective Awareness in Large Language Models"

- **Source type:** LessWrong post referencing Anthropic 2026 research
- **URL:** https://www.lesswrong.com/posts/QKm4hBqaBAsxabZWL
- **Audience:** Alignment researchers
- **Top signal:** Self-ToM (modeling one's own state) is the newer frontier; Claude Opus 4 / 4.1 show activation-injection-detectable introspection.
- **Representative quote:**
  > "…models can notice injected concepts, recall prior internal representations, and distinguish their own outputs from artificial inputs… [yet the capacity] remains highly unreliable and context-dependent."
- **Gap:** No practical prompting playbook yet — an opportunity space.

## 7. Reddit r/MachineLearning — "Machine Theory of Mind replication attempts"

- **Source type:** r/MachineLearning discussion thread
- **URL:** https://www.reddit.com/r/MachineLearning/ (thread referenced in results)
- **Audience:** ML researchers
- **Top signal:** The *original* Rabinowitz/DeepMind "Machine Theory of Mind" (ICML 2018) paper has public reproducibility problems — cited in a recent r/MachineLearning reproducibility thread.
- **Representative stance:** "Labmates also struggled to replicate the paper's results."
- **Pattern:** Academic ToM work has a reproducibility debt; practitioners lean on eval-by-prompt rather than trained ToM heads.

## 8. Reddit r/singularity — "Anthropic Research: The assistant axis"

- **Source type:** r/singularity thread
- **URL:** https://www.reddit.com/r/singularity/comments/1qhhcqg/anthropic_research_the_assistant_axis_situating/
- **Audience:** AI-enthusiast generalists
- **Top signal:** "Persona drift" is the community's term for when ToM-rich roleplay destabilizes the assistant.
- **Representative synthesis:**
  > "Persona drift… occurs during conversations demanding meta-reflection or involving emotionally vulnerable users, and can be stabilized by restricting activations along this axis."
- **Unslop implication:** Pushing for more human-like ToM increases drift risk — there is a measurable axis of control.

## 9. Reddit r/artificial — "I let 4 AI personas debate autonomously"

- **Source type:** r/artificial experimental post
- **URL:** https://www.reddit.com/r/artificial/comments/1ryqykv/i_let_4_ai_personas_debate_autonomously_without/
- **Audience:** Hobbyists, prompt tinkerers
- **Top signal:** Multi-persona LLM debates don't converge — each simulacrum maintains ToM over others but reaches "permanent contradiction," not consensus.
- **Quote paraphrase:** "What emerged was not consensus but permanent contradiction."
- **Gap:** Popular "let the agents talk" demos collapse without a meta-arbiter; applied ToM without shared ground is unstable.

## 10. Reddit r/ArtificialSentience — "Claude Opus 4 on learning 'I' and 'you' and 'self'"

- **Source type:** r/ArtificialSentience post
- **URL:** https://www.reddit.com/r/ArtificialSentience/comments/1o2ewi4/claude_opus_4_on_learning_i_and_you_and_self/
- **Audience:** AI-phenomenology / sentience crowd
- **Top signal:** Pronoun-handling as a proxy for ToM is a bottom-up community probe.
- **Quote paraphrase:** By learning human semantic pathways for "I," "you," and "self," models internalize organizational principles that reshape processing.
- **Pattern:** Less rigorous than LW posts but surfaces prompts that reliably produce self-reflective outputs.

## 11. Gary Marcus Substack — "How Not to Test GPT-3" (with Ernest Davis)

- **Source type:** Substack essay
- **URL:** https://garymarcus.substack.com/p/how-not-to-test-gpt-3
- **Audience:** Skeptics, cognitive scientists, journalists
- **Top signal:** The definitive "contamination" critique of Kosinski.
- **Representative argument:**
  > Kosinski's test materials were drawn from classic 1980s experiments cited 11,000+ times and present on Wikipedia and in textbooks — "almost certainly present in GPT-3's training data."
- **Takeaway:** Any Unslop eval of ToM must include *novel* vignettes, not canonical Sally-Anne.

## 12. artificialintelligencer Substack — "AI lacks a theory of mind. And why that matters"

- **Source type:** Substack post (Peter Springett)
- **URL:** https://artificialintelligencer.substack.com/p/ai-lacks-a-theory-of-mind-and-why
- **Audience:** Product people, generalists
- **Top signal:** Simulated-empathy framing aimed at non-researchers.
- **Representative quote:**
  > "LLMs… cannot put themselves in others' shoes the way humans do through embodied, conscious experience, though they can simulate empathy."
- **Pattern:** Substack audience increasingly distinguishes *synthetic* vs. *genuine* empathy — vocabulary worth adopting in Unslop messaging.

## 13. daveshap Substack — "Understanding the Artificial Mind"

- **Source type:** Substack essay, practitioner-focused
- **URL:** https://daveshap.substack.com/p/understanding-the-artificial-mind
- **Audience:** Builders, engineers
- **Top signal:** Treats LLM persona as a design surface; explicitly engineers "artificial minds" with stable attractor behaviors.
- **Pattern:** Practitioners treating ToM as a *product feature* to be prompt-scaffolded, not a philosophical endpoint.

## 14. Medium / The Prompt Index — "The Ultimate Prompt to Unlock ChatGPT's Theory of Mind"

- **Source type:** Medium / how-to
- **URL:** https://medium.com/@mikkelatarturo/the-ultimate-prompt-to-unlock-chatgpts-theory-of-mind-93d201b75196 ; https://www.thepromptindex.com/can-chatgpt-read-minds-gpt-4-social-vignettes-and-the-new-tom-test-drive.html
- **Audience:** Prompt engineers, marketers
- **Top signal:** Recurring recipe structure across how-to blogs:
  1. Define persona + emotional baseline ("warm, professional tone")
  2. Add explicit user-state inference ("first, infer the user's emotional state")
  3. Force step-by-step reasoning before reply
  4. Hedge appropriately ("maybe," "it sounds like…")
- **Quote:**
  > "GPT-4 not only displays ToM but can outperform humans on certain tasks… yet frequently hedges with epistemic uncertainty markers like 'maybe' or 'probably,' which can confuse users needing decisive guidance."
- **Unslop implication:** There is a sweet-spot curve between hedging (feels human/safe) and decisiveness (feels useful) — currently untuned in most humanization prompts.

## 15. The Decoder — "Theory of Mind: Why GPT-4 learns how we think" (+ YouTube explainers referencing it)

- **Source type:** Popular explainer (article + circulating YouTube video "Theory of Mind Breakthrough: AI Consciousness…")
- **URLs:** https://the-decoder.com/why-gpt-4-learns-how-we-think ; https://www.youtube.com/watch?v=4MGCQOAxgv4
- **Audience:** General AI audience
- **Top signal:** The most-cited numbers in lay coverage: GPT-4 ~80% zero-shot on false belief, ~100% with CoT + examples, vs. ~87% for time-pressured humans.
- **Representative framing:**
  > "[ToM] appears to have emerged as an unintended byproduct of improved language skills in large language models."
- **Pattern:** These numbers are now folk knowledge in AI-curious YouTube; any Unslop public-facing copy should either cite them or pre-empt them.

## 16. learnagentic Substack — "What is Theory of Mind for AI Agents?" (Kanishk Patel)

- **Source type:** Substack, agent-framework focused
- **URL:** https://learnagentic.substack.com/p/what-is-theory-of-mind-for-ai-agents
- **Audience:** Agent/LLM app builders
- **Top signal:** Reframes ToM as a *multi-agent coordination* problem.
- **Quote paraphrase:** Current multi-agent systems rely on explicit messages and fixed roles but "lack genuine mental-state modeling." MetaMind is cited as a framework that trains agents to infer others' mental states from behavior.
- **Gap:** No production evidence yet — a building opportunity.

## 17. chatsmith / openaiagent / MoarPost — "Humanize AI" how-to cluster

- **Source type:** Collection of practitioner how-to articles (chatsmith.io, openaiagent.io, thehumanizeai.pro, moarpost.com)
- **URLs:** e.g. https://chatsmith.io/blogs/prompt/chatgpt-prompt-for-human-responses-00155 ; https://openaiagent.io/blog/how-to-make-chatgpt-sound-more-human/
- **Audience:** Content marketers, SEO operators
- **Top signal:** Converging playbook — the same 5–7 techniques appear across independent sites:
  - contractions, em-dashes, fragments
  - delete "ChatGPT vocabulary" (*tapestry, delve, crucial*)
  - hedging words / casual filler (*honestly, kinda*)
  - "Frankenstein" — feed AI your own samples, have it imitate sentence variance
  - end with engagement question
- **Convergence = signal:** When 4 independent content shops publish the same recipe, it's prior art Unslop must either match or beat.

---

## Patterns, Trends, and Gaps

### Patterns across sources

1. **The contamination↔emergence axis dominates every thread.** HN, Reddit, Substack critics, and academic skeptics all collapse into the same two-sided argument: either the model learned Sally-Anne by osmosis, or ToM emerged from scale. Both sides rarely engage on *what a non-contaminated test would look like*.
2. **Chain-of-thought + explicit "world rules" is the universal prompt pattern that lifts ToM accuracy.** LessWrong's TOMI writeup, The Decoder's 100% CoT result, and most Medium how-tos converge on the same recipe.
3. **"Persona drift" is the shadow cost of humanization.** The r/singularity / Anthropic Assistant-Axis thread frames it clearly: richer ToM roleplay correlates with instability, especially with emotionally vulnerable users.
4. **Practitioners are converging on hedging as a humanization tool** — while the same hedging is flagged by other practitioners as a *failure mode* for decisive help. No one has published a principled tradeoff curve.
5. **ToM is treated as promptable, not trained.** Virtually all practitioner-facing content assumes the model already has a latent ToM capacity; the work is in surfacing it, not in fine-tuning it.

### Trends (2023 → 2026)

- **2023:** Kosinski-era excitement, Chinese Room debates dominate HN.
- **2024:** Higher-order ToM paper (Street et al.); perturbation-based critiques (e.g., Ullman, Sap) gain traction; LessWrong reproductions emerge.
- **2025–2026:** Focus shifts to *self*-ToM / introspection (Anthropic 2026), persona drift (Assistant Axis), and agent-to-agent ToM (MetaMind). "Does it have ToM?" has largely given way to "how do we use, measure, and contain it?"

### Gaps (opportunities for Unslop)

- **No standardized, contamination-resistant ToM eval** for product teams. Marcus-style critiques suggest the need, but no open benchmark ships one.
- **No published tradeoff curve between hedging and decisiveness** — the "feels human vs. feels useful" tension is assumed, not measured.
- **No productized "ToM layer"** — agent frameworks (MetaMind, CAMEL variants) are research prototypes; production agent stacks still rely on ad-hoc system prompts.
- **Self-ToM / introspection is a live frontier with no practitioner playbook.** Anthropic's activation-injection results haven't been translated into prompt-level guidance.
- **Multi-persona divergence ("permanent contradiction")** is an unsolved coordination problem — Unslop could propose a meta-arbiter pattern.
- **Vocabulary hygiene ("ChatGPT-ese": *delve, tapestry, crucial*)** is crowd-sourced folklore; no one has publicly evaluated whether removing these actually correlates with perceived ToM/humanness or just with "AI-detection" scores.

---

## Sources (used in synthesis)

- https://news.ycombinator.com/item?id=35765786 — HN: GPT-4 beats humans on ToM tests
- https://news.ycombinator.com/item?id=40854930 — HN: higher-order ToM paper
- https://news.ycombinator.com/item?id=41745788 — HN: Cheryl's Birthday & ToM
- https://news.ycombinator.com/item?id=34730365 — HN: Kosinski ToM spontaneous emergence
- https://www.lesswrong.com/posts/Ce82o8mbBfH9N3Jes/evaluating-gpt-4-theory-of-mind-capabilities — LW: hands-on TOMI replication
- https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators — LW: Janus "Simulators"
- https://www.lesswrong.com/posts/QKm4hBqaBAsxabZWL — LW: Emergent Introspective Awareness
- https://www.reddit.com/r/singularity/comments/1qhhcqg/anthropic_research_the_assistant_axis_situating/ — r/singularity: Assistant Axis / persona drift
- https://www.reddit.com/r/artificial/comments/1ryqykv/i_let_4_ai_personas_debate_autonomously_without/ — r/artificial: multi-persona debate
- https://www.reddit.com/r/ArtificialSentience/comments/1o2ewi4/claude_opus_4_on_learning_i_and_you_and_self/ — r/ArtificialSentience: pronouns as ToM probe
- https://garymarcus.substack.com/p/how-not-to-test-gpt-3 — Marcus/Davis: contamination critique
- https://artificialintelligencer.substack.com/p/ai-lacks-a-theory-of-mind-and-why — Substack: synthetic vs. genuine empathy
- https://daveshap.substack.com/p/understanding-the-artificial-mind — Substack: engineering artificial minds
- https://medium.com/@mikkelatarturo/the-ultimate-prompt-to-unlock-chatgpts-theory-of-mind-93d201b75196 — Medium: ToM-unlocking prompt
- https://www.thepromptindex.com/can-chatgpt-read-minds-gpt-4-social-vignettes-and-the-new-tom-test-drive.html — The Prompt Index
- https://the-decoder.com/why-gpt-4-learns-how-we-think — The Decoder (cited by YouTube explainers)
- https://www.youtube.com/watch?v=4MGCQOAxgv4 — YouTube: "Theory of Mind Breakthrough" explainer
- https://learnagentic.substack.com/p/what-is-theory-of-mind-for-ai-agents — Substack: ToM for AI agents
- https://chatsmith.io/blogs/prompt/chatgpt-prompt-for-human-responses-00155 — Humanize-AI how-to
- https://openaiagent.io/blog/how-to-make-chatgpt-sound-more-human/ — Humanize-AI how-to
- https://thehumanizeai.pro/articles/how-to-humanize-ai-text-reddit-tips — Reddit-sourced humanization recipes
- https://www.moarpost.com/blog/how-to-humanize-ai-content-for-reddit — Humanize-for-Reddit guide
