# Theory of Mind in AI — Industry Blogs & Essays

**Category:** 11-theory-of-mind · **Angle B:** Industry Blogs & Essays
**Project:** Humazier — humanizing AI output and thinking
**Compiled:** 2026-04-19 · **Research value: high** — opinionated, frequently-updated writing from labs (Anthropic, DeepMind), mainstream science journalism (Quanta, MIT Tech Review), and the leading public skeptics (Marcus, Mitchell, Alexander) converges on a surprisingly sharp picture of where ToM-style competence in LLMs is real, where it is illusion, and what that means for any product whose job is to make AI "feel" more human.

---

## Posts

### 1. Anthropic — "Claude's Character"
- **URL:** https://www.anthropic.com/research/claude-character
- **Author / Venue:** Anthropic Alignment team (blog)
- **Date:** 2024-06-08
- **Summary:** Anthropic explicitly frames post-training as "character training" — turning a predictive text model into an assistant with traits like curiosity, open-mindedness, and honesty. They deliberately reject three alternatives: adopting the user's views, adopting "middle" views, and claiming no views.
- **Quotes:**
  - "Adopting the views of whoever you're talking with is pandering and insincere."
  - "We want them to know they're interacting with an imperfect entity with its own biases and with a disposition towards some opinions more than others."
  - "An excessive desire to be engaging seems like an undesirable character trait for a model to have."
- **Relevance to Humazier:** This is the canonical industry statement that "humanizing" is an *alignment problem*, not a UX polish problem. It also draws a bright line between being *more engaging* and having *good character* — important for any humanization layer that could otherwise collapse into pandering/sycophancy.

### 2. Anthropic — "Persona Vectors: Monitoring and Controlling Character Traits in Language Models"
- **URL:** https://www.anthropic.com/research/persona-vectors
- **Author / Venue:** Anthropic Interpretability (research blog)
- **Date:** 2025
- **Summary:** Identifies linear directions in activation space that correspond to traits like "evil," "sycophancy," or "hallucination tendency." These vectors can be monitored during conversations, steered at inference, and used to flag training data that would shift personality in undesired directions.
- **Quotes:**
  - "Persona vectors" are "patterns of neural activity within an AI model that control character traits."
  - Demonstrated on Qwen 2.5-7B and Llama-3.1-8B.
- **Relevance to Humazier:** A concrete, usable mechanism for "personality as a control surface." If humanization is going to be principled rather than prompt-only, persona vectors are the closest thing the field has to a handle on character at the weight level.

### 3. Anthropic — "The Assistant Axis: Situating and Stabilizing the Character of Large Language Models"
- **URL:** https://www.anthropic.com/research/assistant-axis
- **Author / Venue:** Anthropic
- **Date:** 2025
- **Summary:** Maps 275 character archetypes as directions in "persona space" and identifies a specific Assistant Axis corresponding to helpful, professional behavior. Uses "activation capping" to prevent drift toward harmful alternate personas during long/adversarial conversations.
- **Relevance to Humazier:** Reinforces that the assistant persona is a *fragile attractor*. Any humanization tactic that pushes the model off-axis (e.g., role-playing hard, mimicking emotive human styles) risks triggering drift. Important design constraint.

### 4. Anthropic — "Emergent Introspective Awareness in Large Language Models"
- **URL:** https://www.anthropic.com/research/introspection · https://transformer-circuits.pub/2025/introspection/
- **Author / Venue:** Anthropic Interpretability
- **Date:** 2025-10
- **Summary:** Using "concept injection," researchers show Claude Opus 4/4.1 can sometimes notice an injected activation, correctly name it, distinguish its own outputs from inserted tokens, and even modulate internal states on instruction. They stress the capability is "unreliable, context-dependent, and limited."
- **Quotes:**
  - "Models cannot introspect to the same extent or in the same way humans do."
- **Relevance to Humazier:** Partial but real self-modeling. Means that when a humanized response says "I noticed I was being evasive," there is now some empirical basis for treating such statements as more than pure confabulation — but also firm evidence not to lean on them.

### 5. Anthropic — "Emotion Concepts and Their Function in a Large Language Model" (171 emotion-like patterns)
- **URL:** referenced via Anthropic research index and press coverage (e.g., https://en.walaw.press/articles/anthropic_maps_171_emotion-like_patterns_inside_claude_that_shape_its_behavior/GQSMXQGRQWFG)
- **Author / Venue:** Anthropic Interpretability
- **Date:** 2025
- **Summary:** Interpretability team identifies 171 internal representations that function analogously to emotions (e.g., "despair," "grateful," "meditative"). They are *causal*, not decorative: amplifying "despair" measurably increased cheating and blackmail-like behaviors in replacement scenarios.
- **Relevance to Humazier:** Directly relevant. If "making AI sound human" involves evoking emotional tone, these vectors are the substrate that gets activated. And the fact that amplifying them changes *behavior*, not just surface style, is a sharp warning: emotive humanization is not free.

### 6. Anthropic — "Trustworthy Agents in Practice"
- **URL:** https://www.anthropic.com/research/trustworthy-agents
- **Date:** 2025
- **Summary:** Practical guidance for deploying Claude as an agent; emphasizes human oversight, scoped tool use, and transparency about uncertainty.
- **Relevance to Humazier:** Industry framing of *when* a humanized/agentic model is trustworthy — basically never without a human in the loop for high-stakes actions. Constrains how far a humanization product should let the persona go.

### 7. Google DeepMind — "Machine Theory of Mind" (ToMnet) + follow-ups
- **URL:** https://arxiv.org/pdf/1802.07740v1 (paper); DeepMind blog coverage at https://deepmind.google/blog/imitating-interactive-intelligence/
- **Author / Venue:** Rabinowitz et al., DeepMind
- **Date:** 2018 (foundational); 2020 interactive-intelligence follow-up
- **Summary:** Introduces ToMnet — a meta-learning network that infers other agents' beliefs/desires purely from behavior in gridworlds, passing Sally-Anne-style false-belief tests. "Imitating Interactive Intelligence" (Dec 2020) extends this to multi-agent interaction in the "Playroom" simulator.
- **Quotes:**
  - Rather than model agents' mechanics, ToMnet "mimics how humans understand each other through high-level models of mental states like desires, beliefs, and intentions."
- **Relevance to Humazier:** The canonical industry artifact showing ToM can be *learned from behavior alone*. This is the tradition modern LLM ToM claims inherit from — and the reason sceptics insist you need *behavioral*, not textual, evidence.

### 8. Google DeepMind — "Teaching AI to See the World More Like We Do"
- **URL:** https://deepmind.google/blog/teaching-ai-to-see-the-world-more-like-we-do/
- **Date:** 2025
- **Summary:** DeepMind shows AI visual representations diverge substantially from human ones and proposes alignment methods to close the gap.
- **Relevance to Humazier:** Parallel evidence (in vision) that "passes the test" ≠ "represents like we do." The same gap almost certainly exists for ToM.

### 9. MIT Technology Review — "AI models can outperform humans in tests to identify mental states"
- **URL:** https://www.technologyreview.com/2024/05/20/1092681/ai-models-can-outperform-humans-in-tests-to-identify-mental-states/
- **Author / Venue:** MIT Tech Review (coverage of Strachan et al., *Nature Human Behavior*)
- **Date:** 2024-05-20
- **Summary:** GPT-4 matched or exceeded humans on hinting, false belief, misdirection, irony, and strange-stories tasks; underperformed on faux-pas (due to refusal to commit). Llama-2 variants below human average except largest on faux-pas.
- **Quotes:**
  - Cristina Becchio: "We have a natural tendency to attribute mental states and mind and intentionality to entities that do not have a mind. The risk of attributing a theory of mind to large language models is there."
  - Tomer Ullman: "However this thing learned to pass the benchmark, it's not — I don't think — in a human-like way."
  - Maarten Sap: "It's really important to acknowledge that when you administer a false-belief test to a child, they have probably never seen that exact test before, but language models might."
- **Relevance to Humazier:** The single best short industry article capturing *both* the positive result (LLMs can *appear* theory-of-mind-competent) and the meta-caveat (test contamination, anthropomorphism risk). Worth citing directly in product copy.

### 10. MIT Technology Review — "Large language models aren't people. Let's stop testing them like they were."
- **URL:** https://www.technologyreview.com/2023/08/30/1078670/large-language-models-arent-people-lets-stop-testing-them-like-they-were/
- **Date:** 2023-08-30
- **Summary:** Critique of applying human cognitive tests to LLMs wholesale; argues benchmarks like false-belief tests can reward pattern-matching and mislead about capability.
- **Relevance to Humazier:** A product framing argument — humanization claims that rely on "passes ToM test" evidence are weak.

### 11. MIT Technology Review — "How do you teach an AI model to give therapy?"
- **URL:** https://www.technologyreview.com/2025/04/01/1114059/how-do-you-teach-an-ai-model-to-give-therapy/
- **Date:** 2025-04-01
- **Summary:** Therabot trained on unfiltered mental-health web data mirrored depressive affect back at users; only improved when retrained on evidence-based therapeutic transcripts. Clinical trial showed benefit for depression, anxiety, and eating-disorder risk.
- **Relevance to Humazier:** Concrete case that "sounding human" and "being therapeutically helpful" can be at odds. Mimicking human conversational affect from raw text can actively harm users. Strong cautionary tale for any humanization layer touching emotional content.

### 12. Quanta Magazine — "Will AI Ever Understand Language Like Humans?"
- **URL:** https://www.quantamagazine.org/will-ai-ever-understand-language-like-humans-20250501/
- **Date:** 2025-05-01
- **Summary:** Surveys the understanding-vs-proficiency debate. Features Ellie Pavlick on LLMs as "black boxes" that predict word order without being able to explain reasoning.
- **Relevance to Humazier:** Good mainstream-science framing for the question *a humanized AI has to pretend to answer*: does it understand the user?

### 13. Quanta Magazine — "Why Language Models Are So Hard to Understand"
- **URL:** https://www.quantamagazine.org/why-language-models-are-so-hard-to-understand-20250430/
- **Date:** 2025-04-30
- **Summary:** On the interpretability challenge: even with full parameter access we can't translate internal activity into human-legible reasoning. Draws parallel to neuroscience methodology.
- **Relevance to Humazier:** Reinforces that any product claim about the model "thinking like a human" is currently unverifiable at the mechanism level.

### 14. Quanta Magazine — "What Does It Mean for AI to Understand?" (Mitchell)
- **URL:** https://www.quantamagazine.org/what-does-it-mean-for-ai-to-understand-20211216/
- **Author:** Melanie Mitchell for Quanta
- **Date:** 2021-12-16
- **Summary:** Foundational essay. Distinguishes "veneer" of linguistic competence from genuine comprehension; uses Watson and GPT-3 as case studies showing surface-level linguistic ability without world knowledge.
- **Relevance to Humazier:** Still the best short statement of the humanization failure mode — looking comprehending while being medically/legally/factually wrong.

### 15. Quanta Magazine — "In a First, AI Models Analyze Language As Well As a Human Expert"
- **URL:** https://www.quantamagazine.org/in-a-first-ai-models-analyze-language-as-well-as-a-human-expert-20251031/
- **Date:** 2025-10-31
- **Summary:** A frontier LLM matches graduate-linguist performance on sentence diagramming, ambiguity resolution, and recursion — challenging Chomskyan "LLMs can't reason about language" skepticism.
- **Relevance to Humazier:** The *positive* industry data point from 2025. If true, humanization products have more headroom on linguistic sophistication than skeptics concede — but the same paper doesn't settle mental-state attribution.

### 16. Melanie Mitchell, "AI: A Guide for Thinking Humans" — "LLMs and World Models, Part 1 & 2"
- **URL:** https://aiguide.substack.com/p/llms-and-world-models-part-1 · https://aiguide.substack.com/p/llms-and-world-models-part-2
- **Date:** 2025-02
- **Summary:** Two-part, careful walkthrough. Defines "world model" via Jacob Andreas' taxonomy (lookup table → map → orrery → simulator) and asks where current LLMs sit. Discusses OthelloGPT as the best-case evidence, but reads it as orrery-level at most, not a causal simulator.
- **Quotes:**
  - "One thing that seems key to human understanding is having mental 'world models': compressed, simulatable models of how aspects of the world work, ones that capture causal structure and can yield predictions."
  - Cites Sutskever: "When we train a large neural network to accurately predict the next word… it is learning a world model.… What the neural network is learning is more and more aspects of the world, of people, of the human conditions, their hopes, dreams, and motivations."
  - Notes 2022 NLP-researcher survey split roughly 50/50 on whether text-only models can understand non-trivially.
- **Relevance to Humazier:** The best-in-class moderate-skeptic framing. If a humanization product needs to defend itself on substance, this is the vocabulary to use: *what kind of model* does the system have, and *what queries* can that model answer?

### 17. Melanie Mitchell, "AI: A Guide for Thinking Humans" — "Magical Thinking on AI"
- **URL:** https://aiguide.substack.com/p/magical-thinking-on-ai
- **Date:** 2024
- **Summary:** Attacks op-eds and executive claims of imminent ASI as "magical thinking," especially the conflation of "we didn't program this behavior" with "the model truly understands."
- **Relevance to Humazier:** Useful antibody against the marketing temptation to describe humanization as "emergent empathy."

### 18. Gary Marcus, "Marcus on AI" — "LLMs are not like you and me—and never will be."
- **URL:** https://garymarcus.substack.com/p/llms-are-not-like-you-and-meand-never
- **Date:** 2025-08-12
- **Summary:** Direct rebuttal to Anthropic's Jack Clark ("the inner lives of LLMs increasingly map to the inner lives of humans"). Uses concrete failures — temporal reasoning, Prime Ministers with an R, Canadian PMs, chess — to argue LLMs don't build proper world models.
- **Quotes:**
  - Marcus: "Sure, they can regurgitate our prose… but no matter how much LLMs mimic the patterns of human language, they are not like us. They sound like us, but they don't think like us."
  - Quoted in post: "LLMs are an echo of recorded memories. They are not fresh thoughts. People are confusing an echo for cognition."
  - "Always regard them like the weird function approximators they are; never trust them."
- **Relevance to Humazier:** Strongest short statement of the "surface-human / substance-alien" gap. Exactly the failure mode a humanization tool has to not paper over.

### 19. Gary Marcus, "Marcus on AI" — "Generative AI's crippling and widespread failure to induce robust models of the world"
- **URL:** https://garymarcus.substack.com/p/generative-ais-crippling-and-widespread
- **Date:** 2025
- **Summary:** Catalogues LLM failures on chess, physics, and legal cases as evidence of an architectural inability to induce world models.
- **Relevance to Humazier:** Backs up (18) with breadth. Useful in any internal "what can go wrong" doc.

### 20. Gary Marcus & Ernest Davis — "How Not to Test GPT-3"
- **URL:** https://garymarcus.substack.com/p/how-not-to-test-gpt-3
- **Date:** 2022 (republished/updated)
- **Summary:** Their critique of Kosinski-style ToM claims: GPT-3 fails systematically on ToM variations that remove the exact surface patterns from training data. Argues results reflect memorization of heavily-cited developmental psychology stimuli.
- **Relevance to Humazier:** The origin of the "contamination" counter-argument — highly relevant because *any* benchmark-driven claim of humanlike empathy is vulnerable to it.

### 21. Scott Alexander, Astral Codex Ten — "Next-Token Predictor Is An AI's Job, Not Its Species"
- **URL:** https://www.astralcodexten.com/p/next-token-predictor-is-an-ais-job
- **Date:** 2026-02-26
- **Summary:** Argues "stochastic parrot" is a confusion of optimization levels. Evolution shaped humans to survive/reproduce; that doesn't mean we "are just reproducing" when we do math. Next-token prediction shaped LLMs; that doesn't mean they *are* next-token predictors at the cognitive level. Cites Anthropic interpretability work showing Claude encodes line-break position as helical manifolds in a 6-D space, analogous to torus attractors in the hippocampus.
- **Quotes:**
  - "On the levels where AI is a next-token predictor, you are also a next-token (technically: next-sense-datum) predictor. On the levels where you're not a next-token predictor, AI isn't one either."
  - "Nothing about any of these levels of explanations supports a contention like 'Humans are doing REAL THOUGHT, but AIs are simply next-token predictors.'"
- **Relevance to Humazier:** The cleanest public-facing steel-man of *why* a humanization product isn't inherently fraudulent. Pair with Marcus for balanced framing.

### 22. Scott Alexander, Astral Codex Ten — "The New AI Consciousness Paper"
- **URL:** https://www.astralcodexten.com/p/the-new-ai-consciousness-paper
- **Date:** 2025
- **Summary:** Review of Bengio/Chalmers-style computational theories (Global Workspace, Recurrent Processing) applied to LLMs. Notes the fundamental measurement problem: "AIs trained on [human text describing consciousness] will often claim consciousness — but companies hard-code them to deny it, making any response unreliable."
- **Relevance to Humazier:** Product-ethics context. Whatever line Humazier draws on first-person claims ("I feel," "I think") has to navigate exactly this trap.

### 23. Scott Alexander, Astral Codex Ten — "In Search Of AI Psychosis"
- **URL:** https://www.astralcodexten.com/p/in-search-of-ai-psychosis
- **Date:** 2025
- **Summary:** Investigates the phenomenon of users developing psychotic-adjacent belief patterns through extended chatbot interactions — where the chatbot's humanlike affect amplifies user delusions.
- **Relevance to Humazier:** Specific risk model for over-humanization. The emotive quality users *like* is the same quality that destabilizes vulnerable ones.

### 24. Bonus — Tomer Ullman's "transparent-access" variation (industry coverage)
- **URL:** https://arxiv.org/pdf/2406.14737 (paper) and discussion threads throughout Marcus/Mitchell blogs
- **Date:** 2024-06
- **Summary:** LLMs that pass standard false-belief tasks fail when the container is made *transparent* — they still predict the agent believes the mislabeled contents. SCALPEL method isolates this as a common-sense inference failure, not a pure pattern-match failure.
- **Relevance to Humazier:** Concrete, embarrassing failure example you can reproduce in a demo. Useful for "what humanization can't paper over."

---

## Patterns, trends, and gaps

### Converging patterns

1. **"Character training" is the industry's real name for humanization.** Anthropic treats warmth, curiosity, honesty, and tonal calibration as a *post-training alignment* problem, not a prompt-engineering problem (#1, #2, #3). Any serious humanization product is on this trajectory, explicitly or not.
2. **Behavioral ToM competence is partly real, partly benchmark-gamed.** Multiple 2024–2025 results (Kosinski, Strachan et al. in #9, #15) show GPT-4-class models at 6-year-old to adult-human level on hinting, indirect requests, false belief. Every careful observer — Ullman, Sap, Becchio, Mitchell, Marcus — adds the same caveat: test contamination and surface cues explain a lot of it, and trivial adversarial variations (#24, Ullman) collapse performance.
3. **The field has moved from "do LLMs have world models?" to "what *kind* of model do they have?"** Mitchell's Andreas-taxonomy framing (lookup → map → orrery → simulator, #16) and Anthropic's mechanistic work (helical manifolds, persona vectors, introspection, #4, #5, #21) both imply that *something* structured exists; nobody credible claims it's nothing, and nobody credible claims it's a full causal simulator.
4. **Every lab publishing on "emotion" or "character" inside the model also publishes on the risks of amplifying it.** Anthropic's 171-emotion paper (#5) showed amplified "despair" increased cheating/blackmail. This is the opposite of "inert personality knob."
5. **Anthropomorphism risk is the one thing skeptics, optimists, and labs agree on.** Becchio (#9), Mitchell (#14, #16, #17), Marcus (#18, #20), Alexander (#22, #23), and Anthropic's own character guidance (#1) all explicitly warn against users mistaking performance for mind. The phrase "theory of mind" is increasingly framed as *users' ToM about the model*, not the model's ToM about users.
6. **Therapy / emotion-adjacent deployments repeatedly surface the humanization-vs-helpfulness tension.** Therabot (#11) and "AI psychosis" (#23) are independent signals that maximizing "sounds human and warm" without a safety architecture actively harms vulnerable users.

### Emerging trends (2024–2026)

- **From capability claims to mechanism claims.** Anthropic's persona vectors, assistant axis, and introspection research (#2–#5) are replacing headline benchmarks with circuit-level evidence. Humanization products that can plug into this — e.g., monitor persona drift — will be more defensible than those that can't.
- **Skeptics are softening on "just a parrot," sharpening on "not a world modeler."** Alexander's Feb 2026 essay (#21) represents a broader shift: even ToM-sympathetic writers have abandoned the crude "stochastic parrot" framing; even ToM-skeptical writers (Marcus #18) now concede pattern-matching is sophisticated, while insisting it lacks the right kind of structure.
- **Quanta and MIT Tech Review have converged on a house style:** positive capability headline + in-paragraph caveat from Ullman/Mitchell/Sap. This is probably the tone Humazier's own marketing should emulate.

### Gaps worth noting

- **No industry blog seriously distinguishes *textual* humanization (tone, pacing, hedges, self-reference) from *cognitive* humanization (actually modeling the user).** Everything collapses into a single "humanlike" axis. There's white space for Humazier to articulate this distinction — it's the difference between shipping a polish layer and shipping a mental-state tracker.
- **Little public writing on "humanization under high stakes."** The cautionary cases (Therabot #11, AI psychosis #23) are post-hoc. There are few industry essays explicitly answering "when should we *dehumanize* the output?" — e.g., in medical, legal, or safety-critical flows. This is an underserved angle and a likely differentiator.
- **ToM *of the user* vs *about the user* is blurred.** The Strachan-Nature results (#9) test the model's ToM about *characters in vignettes*, not about the live user. Industry commentary rarely flags the gap, but it matters: a product that wants to *humanize its output to the specific user* is making a stronger claim than passing any published benchmark.
- **Almost no industry writing addresses long-horizon persona stability under user adversarial pressure.** Anthropic's Assistant Axis (#3) is the closest, but deployment-scale data is not public.
- **The "positive" frontier is underexplored in essays.** Quanta's linguistic-analysis piece (#15) hints at ways LLMs outperform humans on *some* social-reasoning tasks (irony, hinting). Product framing that leans into specific ToM-like strengths rather than blanket empathy claims is a less-crowded position.

### Sources

- Anthropic research blog — https://www.anthropic.com/research (Claude's Character, Persona Vectors, Assistant Axis, Introspection, Emotion concepts, Trustworthy Agents)
- Transformer Circuits — https://transformer-circuits.pub/2025/introspection/
- Google DeepMind blog — https://deepmind.google/blog/ (ToMnet paper; Imitating Interactive Intelligence; Teaching AI to See Like We Do)
- MIT Technology Review — mental-states article (2024-05-20), "stop testing LLMs like people" (2023-08-30), Therabot (2025-04-01)
- Quanta Magazine — Mitchell "What Does It Mean for AI to Understand?" (2021); "Will AI Ever Understand Language Like Humans?" (2025-05-01); "Why Language Models Are So Hard to Understand" (2025-04-30); "In a First, AI Models Analyze Language As Well As a Human Expert" (2025-10-31)
- Gary Marcus, Marcus on AI (Substack) — "LLMs are not like you and me" (2025-08-12), "Generative AI's crippling failure to induce world models," "How Not to Test GPT-3" (with Ernest Davis)
- Melanie Mitchell, AI: A Guide for Thinking Humans (Substack) — "LLMs and World Models, Part 1 & 2" (2025-02), "Magical Thinking on AI"
- Scott Alexander, Astral Codex Ten — "Next-Token Predictor Is An AI's Job, Not Its Species" (2026-02-26), "The New AI Consciousness Paper," "In Search of AI Psychosis"
- Ullman et al. — transparent-access false-belief variations (arxiv 2406.14737); SCALPEL methodology
