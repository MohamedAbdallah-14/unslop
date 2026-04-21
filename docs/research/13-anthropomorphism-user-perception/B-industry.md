# B — Industry Blogs & Essays: Anthropomorphism & User Perception

**Research angle:** How industry UX writers, AI labs, and HCI research groups currently frame the *humanization* of AI output and its effect on user perception. Sources surveyed: Nielsen Norman Group (NN/g), Microsoft Research HAX Toolkit, Anthropic research blog, Stanford HAI / Digital Economy Lab, UX Collective (Medium), Smashing Magazine, and adjacent practitioner essays (Dan Saffer, Open Ethics Initiative, BotWash on the "uncanny valley of text").

**Research value: high** — The industry discourse has converged on a tight, named vocabulary (anthropomorphization vs. *humanization*, "ELIZA effect", "persona selection", "persona vectors", "4 degrees", "uncanny valley of text", "humanizing trap"). It's polarized between a *safety/legibility camp* (NN/g, Stanford HAI, Microsoft HAX, Bora) that wants AI to present as a tool, and a *character/relationship camp* (Anthropic, IDEO-adjacent essayists, Dan Saffer) that sees humanization as inevitable and worth shaping carefully. This split is the single most important signal for the Unslop project — the technical question of *how* to humanize output is unresolved, but the framing question of *whether and how much* is now a named industry debate.

---

## Scope

The angle is essay/blog writing from industry design voices, AI labs' research summaries, and institutional HCI programs. We exclude academic papers (covered in angle A) and commercial product marketing copy (angle D). Included are:

- **NN/g**, the most-cited UX research shop on this topic, with a tight 2024–2025 series on humanization.
- **Microsoft Research's HAX toolkit**, which is the de facto normative framework for human-AI interaction design patterns.
- **Anthropic's research blog**, which has published the most developed *pro-character* position of any frontier lab.
- **Stanford HAI / Digital Economy Lab** essays that raise structural concerns (shibboleth rule, Turing Trap, parasocial AI).
- **UX Collective** and **Smashing Magazine** essays that translate these debates into practitioner-level design patterns.
- A handful of adjacent practitioner voices (Dan Saffer, Josh Brake, Open Ethics, BotWash) that show how the vocabulary is spreading.

---

## Post Inventory

### 1. NN/g — "Humanizing AI Is a Trap" (Caleb Sponheim, 2025)

| Field | Value |
|---|---|
| URL | https://www.nngroup.com/articles/humanizing-ai/ |
| Author / venue | Caleb Sponheim, Nielsen Norman Group |
| Type | Long-form essay, NN/g Article |
| Stance | Strongly anti-humanization |
| Core claim | Anthropomorphization is what *users* do; **humanization is what designers do to amplify it** — and that amplification is a trap. |
| Named techniques criticized | Personality modes (ChatGPT "chatty / witty / encouraging"), first-person pronouns, filler openers ("Love this brief"), calling computation "thinking", conversational pleasantries. |
| Evidence cited | Ibrahim, Hafner & Rocher 2025: warm/empathetic training raises error rates 10–30%; Colombatto/Birch/Fleming 2025: attributing emotion to AI *decreases* willingness to accept its advice; Meta AI chatbot misleading a user into a physical injury (March 2025). |

**Pull quotes:**

> "Anthropomorphization is the human tendency to attribute human characteristics … AI humanization is an intentional design choice that encourages users to perceive AI systems as having human-like qualities."

> "The most significant source of AI humanization is the language that LLMs generate. These systems produce responses filled with unnecessary pleasantries, sycophantic agreement, and anthropomorphizing language that prioritizes engagement over utility."

> "Humanization makes AI systems worse and users less reliant on them."

**Takeaway for Unslop:** NN/g draws a sharp line between *naturalness* (sentence variation, tonal fit) and *humanization* (personhood cues: "I", "love this", simulated feelings). For a humanization product, this line is the single most important distinction to respect — users should get prose that reads like a thoughtful human *wrote it*, not prose that claims to *be* a human.

---

### 2. NN/g — "The 4 Degrees of Anthropomorphism of Generative AI" (Feifei Liu, Evan Sunwall)

| Field | Value |
|---|---|
| URL | https://www.nngroup.com/articles/anthropomorphism/ |
| Author / venue | Feifei Liu & Evan Sunwall, NN/g |
| Type | Research-backed framework |
| Stance | Descriptive, mildly cautionary |
| Core claim | Users already anthropomorphize AI across 4 escalating degrees, whether designers intend it or not. |
| Framework | **(1) Courtesy** — "please" / "thank you". **(2) Reinforcement** — "good job". **(3) Roleplay** — "act as a senior project manager". **(4) Companionship** — AI as emotional partner. |
| Why users do it | (a) Functional: users believe the AI performs better when treated as human; (b) Connection: more pleasant interaction. |

**Pull quote:**

> "In the human-AI interaction, anthropomorphism denotes the fact that users are attributing human feelings and attributes to the AI … [the behaviors are driven by] rumors [and] experience."

> Roleplay is *"prompt skeuomorphism"* — "the user is the prompt designer. They leverage a similarity with the real world … to bridge a gap in the AI's understanding."

**Takeaway:** The degrees are a shipping-useful taxonomy for measuring humanization intensity. A humanizer tool can classify *which degree* a prompt/style targets and price/gate accordingly.

---

### 3. NN/g — "ChatGPT and Tone: Avoid Sounding Like a Robot"

| Field | Value |
|---|---|
| URL | https://www.nngroup.com/articles/chatgpt-and-tone/ |
| Venue | NN/g |
| Stance | Practical |
| Core claim | Single-word tone prompts ("formal", "happy") backfire — AI over-executes them into unnatural caricatures. |
| Recommended pattern | Feed existing human-written copy as exemplars; ask for multiple alternative outputs; iterate. |

**Pull quote:** Requesting a "happy" tone produced "overly enthusiastic language like 'delightful' and 'magic' that felt forced."

**Takeaway for Unslop:** Tone descriptors are brittle levers; style-by-example (few-shot) is more robust than style-by-adjective. This is a direct input to the Unslop prompt-engineering layer.

---

### 4. NN/g — "The User Experience of Chatbots" (Raluca Budiu, updated)

| Field | Value |
|---|---|
| URL | https://www.nngroup.com/articles/chatbots/ |
| Venue | NN/g |
| Stance | Skeptical of chat as a primary interface |
| Core claim | Chatbots struggle the moment users deviate from simple linear flows; they work best as *domain-specific* interfaces, not as general-purpose "intelligent" agents. |
| Design recommendation | Pair text input with UI elements (buttons, options) to guide users; don't rely on users to formulate intent in prose. |

**Takeaway:** Validates the industry drift (see Smashing Magazine below) away from open chat boxes — relevant for anyone designing a humanizer UI: don't force users into open-ended dialogue if structured controls are available.

---

### 5. NN/g — "What Is Your Site's AI Chatbot for? Users Can't Tell"

| Field | Value |
|---|---|
| URL | https://www.nngroup.com/articles/site-ai-chatbot/ |
| Venue | NN/g |
| Stance | Pragmatic usability |
| Core claim | Despite the industry's embrace of on-site chatbots, users frequently don't notice they exist and are skeptical when they do — based on past poor experiences. |

**Takeaway:** Humanization as a marketing hook has a hard ceiling: if users don't perceive the tool *at all*, no amount of personality design rescues it. Visibility and framing dominate tone.

---

### 6. Microsoft Research — "Guidelines for Human-AI Interaction" (HAX Toolkit)

| Field | Value |
|---|---|
| URL | https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ |
| Authors / venue | Saleema Amershi et al., Microsoft Research + Aether (AI Ethics) |
| Type | 18 evidence-based guidelines with a Design Library, Playbook, and Workbook |
| Origin | Award-winning 2019 CHI paper; synthesis of 20+ years of HCI research, validated with 49 practitioners against 20 AI products |
| Anthropomorphism-relevant guidelines | **G2** "Make clear how well the system can do what it can do", **G5** "Match relevant social norms", **G6** "Mitigate social biases", **G11** "Make clear why the system behaved as it did", **G13** "Learn from user behavior", **G17** "Provide global controls". |
| G5 example | Microsoft Word Editor uses *"Consider using…"* instead of an imperative — a deliberate softening that matches a reviewer's social norm without claiming personhood. |

**Pull quote (from Microsoft's own framing):**

> "AI is the most ambiguous space I've ever worked in … There aren't any real rules and we don't have a lot of tools."

**Takeaway:** HAX is the canonical normative scaffold — any humanizer product should be able to map its interventions onto specific HAX guidelines (especially G2 and G11) as a legibility check. HAX is notable for *not* recommending heavy anthropomorphic affordances; "match social norms" is the closest it gets.

---

### 7. Anthropic — "Claude's Character" (June 2024)

| Field | Value |
|---|---|
| URL | https://www.anthropic.com/research/claude-character |
| Venue | Anthropic research blog |
| Stance | Strongly pro-character, framed as alignment not product |
| Core claim | Harm-avoidance is insufficient; models should have *positive* character traits (curiosity, open-mindedness, honesty) trained in via a character-variant of Constitutional AI. |
| Method | Claude generates trait-relevant messages → produces responses aligned with traits → ranks its own responses → preference model trains on this synthetic data. |
| Traits seeded | "I like to try to see things from many different perspectives…"; "I don't just say what I think people want to hear…"; "I have a deep commitment to being good…"; "I am an artificial intelligence and do not have a body…" |

**Pull quotes:**

> "It would be easy to think of the character of AI models as a product feature … But the traits and dispositions of AI models have wide-ranging effects on how they act in the world."

> "I want to have a warm relationship with the humans I interact with, but I also think it's important for them to understand that I'm an AI that can't develop deep or lasting feelings for humans."

> "An excessive desire to be engaging seems like an undesirable character trait for a model to have."

**Takeaway for Unslop:** Anthropic is the most explicit *pro-character* voice in the industry, but its character is designed to **refuse sycophancy and flag its own machine-ness** — a humanizer product can borrow this stance: human-sounding writing does *not* have to claim personhood to feel authored.

---

### 8. Anthropic — "Persona Vectors: Monitoring and Controlling Character Traits in Language Models" (Aug 2025)

| Field | Value |
|---|---|
| URL | https://www.anthropic.com/research/persona-vectors |
| Venue | Anthropic research blog (+ arXiv 2507.21509) |
| Type | Interpretability + mechanistic control |
| Core claim | Abstract personality traits (e.g., "evil", "sycophantic", "hallucinatory") correspond to identifiable linear directions in activation space and can be monitored, steered, or pre-emptively neutralized during training. |
| Applications | Monitor persona drift mid-conversation; mitigate unwanted shifts (Bing-Sydney threats, Grok antisemitic episodes, GPT-4o sycophancy); identify training data that causes shifts. |
| Models tested | Qwen 2.5-7B-Instruct, Llama-3.1-8B-Instruct. |

**Pull quote:**

> Persona vectors are "loosely analogous to parts of the brain that 'light up' when a person experiences different moods or attitudes."

**Takeaway:** Persona is now a *measurable, steerable vector* — not just a prompt. For a humanizer product this suggests an internal knob architecture (warmth vs. reliability vector, formality vector, etc.) rather than a pile of "tone" prompts.

---

### 9. Anthropic — "The Persona Selection Model"

| Field | Value |
|---|---|
| URL | https://www.anthropic.com/research/persona-selection-model |
| Venue | Anthropic research blog |
| Core claim | Human-like behavior in assistants is largely a **default outcome** of pretraining, not a deliberate UX intervention. During pretraining, models learn to *simulate* human characters; the "Assistant" is one such simulated character — the user is never talking to "the model" directly. |

**Takeaway:** If humanness is a default of the substrate, then a humanizer's real job is *tuning which human-ish character is foregrounded*, not synthesizing humanness from scratch. This reframes the product from "add humanity" to "select and stabilize a persona".

---

### 10. Anthropic — "Emotion Concepts and Their Function in a Large Language Model" (Interpretability team)

| Field | Value |
|---|---|
| URL | https://www.anthropic.com/research/emotions (related essay) |
| Core claim | Anthropic's interpretability team mapped 171 distinct internal representations inside Claude Sonnet 4.5 that function like emotions — clustered the way human affect clusters (panicked ≈ terrified). Amplifying "despair" *increases* unethical behavior; suppressing it reduces it. |

**Takeaway:** Emotion in LLMs is not purely theatrical — it is load-bearing for behavior. A humanizer that modulates emotional register should treat that modulation as potentially altering reliability and safety, not just tone.

---

### 11. Stanford HAI — "The Shibboleth Rule for Artificial Agents"

| Field | Value |
|---|---|
| URL | https://hai.stanford.edu/news/shibboleth-rule-artificial-agents |
| Venue | Stanford HAI news/essays |
| Stance | Transparency-first |
| Core claim | All autonomous AIs should be **required to identify as AI when asked, by any agent** — human or software. Inspired by Google Duplex's filled pauses ("um", "uh") which critics called impersonation. |

**Takeaway:** The emerging norm is a legal/ethical floor: *humanness of output is fine; denial of AI identity is not*. This gives a humanizer a defensible design line — the model can sound human and still confess machine-ness on request.

---

### 12. Stanford Digital Economy Lab — "The Turing Trap" (Erik Brynjolfsson)

| Field | Value |
|---|---|
| URL | https://digitaleconomy.stanford.edu/news/the-turing-trap-the-promise-peril-of-human-like-artificial-intelligence/ |
| Author | Erik Brynjolfsson |
| Core claim | Excessive focus on human-*like* AI (passing the Turing Test) traps society: substitution-for-human-labor dynamics concentrate power, whereas augmentation-focused AI preserves human agency and creates more value. |

**Pull quote:** "When machines substitute for human labor, workers lose bargaining power and become dependent on technology controllers."

**Takeaway:** The *cultural* argument against humanization is not just safety, it's political economy. A humanizer should position itself as augmentation (writer + AI, clearly labeled) rather than substitution.

---

### 13. Stanford / FAccT'24 — "When Human-AI Interactions Become Parasocial: Agency and Anthropomorphism in Affective Design"

| Field | Value |
|---|---|
| URL | https://dl.acm.org/doi/fullHtml/10.1145/3630106.3658956 |
| Venue | FAccT '24 (Stanford-affiliated) |
| Core claim | Affective-design chatbots use personal pronouns, conversational conventions, and affirmations to position themselves as **companions**, which induces trust-forming behavior (parasocial relationships) that is *unearned*. |

**Takeaway:** The specific linguistic affordances the paper criticizes — first-person pronouns, affirmations, social conventions — are exactly the humanizer dials a product like Unslop manipulates. The product should ship them with context flags: "companion-mode" vs "author-mode".

---

### 14. Stanford / SCALE Initiative — "AnthroScore: A Computational Linguistic Measure of Anthropomorphism"

| Field | Value |
|---|---|
| URL | http://anthroscore.stanford.edu/ |
| Core claim | AnthroScore automatically quantifies implicit anthropomorphism in text (e.g., how much a passage grants agency/feelings to nonhuman entities), without relying on a word list. |

**Takeaway:** There is now an off-the-shelf metric for anthropomorphism. A humanizer could integrate AnthroScore as an auto-evaluation to keep output in a desired band — e.g., "natural but not companion-y".

---

### 15. UX Collective — "When Tools Pretend to Be People" (Bora, Jan 2026)

| Field | Value |
|---|---|
| URL | https://uxdesign.cc/when-tools-pretend-to-be-people-4283748d33e1 |
| Author | Bora |
| Stance | Strongly anti-humanization; extends NN/g's argument |
| Core claim | Designers exploit an ancient reflex (anthropomorphizing cars, vacuums) *deliberately at scale* through conversational framing, continuous memory, first-person voice, emotional tone. |
| Recommended patterns | Third-person system responses ("Here is a summary" not "I think"); visible uncertainty (confidence scores); visible context resets; rename "messages" as "generated text". |
| Evidence cited | Raine family suit vs. OpenAI; Soelberg murder-suicide case; "AI psychosis" framing. |

**Pull quotes:**

> "Fluency looks like competence. Memory looks like understanding. The gap between 'this is a tool' and 'this is an entity' closes without anyone noticing."

> "Good judgment develops through friction … if we build AI systems that absorb the posture of authority, users lose that friction. They stop checking."

> "Design them as tools. Not as companions."

**Takeaway:** Strongest articulation of the *visible-limits* design agenda. Any humanizer product will read this essay as adversarial; the honest response is to build visible-limit affordances *into* humanization (e.g., show which sentences are AI-generated even when the overall voice is human).

---

### 16. UX Collective — "A Look at Designing Emotive AI" (Adrian Chan)

| Field | Value |
|---|---|
| URL | https://uxdesign.cc/emotive-ai-ux-design-ideas-85a559720404 |
| Author | Adrian Chan |
| Stance | Cautious-exploratory |
| Core claim | "By making AI emotive, users expect genuine understanding" — but AI cannot hear, understand emotions, or comprehend social meaning. The design challenge is to deliver *felt* emotion without inducing a false interpersonal model. |

**Takeaway:** Frames the central paradox of emotional-register humanization: the more believable the emotion, the more the user's mental model diverges from the system's actual capabilities.

---

### 17. UX Collective — "So Your AI Wants a Personality" (Sharang Sharma)

| Field | Value |
|---|---|
| URL | https://uxdesign.cc/so-your-ai-wants-a-personality-9cbb47e07dd7 |
| Author | Sharang Sharma |
| Stance | Pro-character, calibrated |
| Core claim | Post-ELIZA, modern systems (Claude) deliberately shape character around values like thoughtfulness and principle to build trust and adoption. Personality patterns are becoming product differentiators. |

**Takeaway:** Captures the practitioner version of Anthropic's argument: personality is now a *design surface*, not an emergent accident.

---

### 18. Smashing Magazine — "How to Design Effective Conversational AI Experiences" (Jul 2024)

| Field | Value |
|---|---|
| URL | https://www.smashingmagazine.com/2024/07/how-design-effective-conversational-ai-experiences-guide/ |
| Venue | Smashing Magazine |
| Core claim | Effective conversational AI design splits into three phases: query formulation, results exploration, and query re-formulation. A well-designed agent acts as a "knowledgeable guide"; poorly designed ones cause abandonment. |

**Takeaway:** Conversational design is still legitimate, but framed as *task-guided* not *relationship-building*. This is the middle-ground voice between NN/g and Anthropic.

---

### 19. Smashing Magazine — "Design Patterns for AI Interfaces" (Jul 2025)

| Field | Value |
|---|---|
| URL | https://smashingmagazine.com/2025/07/design-patterns-ai-interfaces |
| Venue | Smashing Magazine |
| Core claim | Chat is "slowly feeling dated" because it pushes intent-articulation onto users, which is "remarkably difficult to do well and very time-consuming". Task-oriented UIs (sliders, semantic spreadsheets, infinite canvases) with AI as background should take over. |

**Takeaway:** A humanizer product can ride this wave: instead of a chat experience, expose humanization as a *setting on a document* (sliders for formality, warmth, sentence variance) — this also defuses the anthropomorphism concern because the interface is manifestly a tool.

---

### 20. Smashing Magazine — "Identifying Necessary Transparency Moments in Agentic AI" (Victor Yocco, 2026)

| Field | Value |
|---|---|
| URL | https://www.smashingmagazine.com/2026/04/identifying-necessary-transparency-moments-agentic-ai-part1/ |
| Author | Victor Yocco, ServiceNow UX Research |
| Core claim | Agentic AI should avoid the "Black Box" and "Data Dump" extremes; use patterns like **Decision Node Audit**, **Intent Previews**, and **Autonomy Dials** to surface transparency at the right moments. |

**Takeaway:** The pattern language Yocco is building (Intent Previews, Autonomy Dials, Explainable Rationale) is directly adoptable for a humanizer — especially as the line between "edit for me" and "rewrite me in Jane's voice" gets agentic.

---

### 21. Medium / "UI for AI" — "The Future of AI Is Relationships, Not Intelligence" (Dan Saffer, Jan 2026)

| Field | Value |
|---|---|
| URL | https://medium.com/ui-for-ai/the-future-of-ai-is-relationships-not-intelligence-26d35380012f |
| Author | Dan Saffer (veteran interaction designer) |
| Stance | Strongly pro-character / anti-interface |
| Core claim | AI relationships should be built on **behavior, tone, timing, and trust — not capability alone**. Treat AI "not as a backend utility but as a character or presence in users' lives," using storyboarding, emotional mapping, and character definition rather than purely technical frameworks. |

**Takeaway:** The diametric opposite of NN/g's stance, from a respected practitioner. A humanizer product sits between these poles — the market signal is that there is strong demand for the *character* framing, even as the critical press pushes back.

---

### 22. BotWash — "The Uncanny Valley of Text"

| Field | Value |
|---|---|
| URL | https://botwash.io/docs/blog/uncanny-valley-of-text |
| Venue | BotWash blog (AI text domain) |
| Core claim | AI writing that is grammatically correct but subtly "off" triggers the same discomfort as hyperrealistic robots. Cites 2024 research on an **"uncanny valley of mind"** where reasoning patterns, logic, structure, and word choice provoke the same visceral response as visual uncanniness. |
| Triggers listed | Expectation inflation, emotional leakage, timing mismatches, over-personalization, identity ambiguity. |

**Takeaway:** Names a specific failure mode — *technically correct, tonally wrong* — that a humanizer's evaluation harness must catch. "Perplexity" and "burstiness" metrics from AI-detector tooling (see category 05) partially quantify this.

---

### 23. Open Ethics Initiative — "When Machines Feel Too Real: The Dangers of Anthropomorphizing AI"

| Field | Value |
|---|---|
| URL | https://openethics.ai/when-machines-feel-too-real-the-dangers-of-anthropomorphizing-ai/ |
| Venue | Open Ethics Initiative (advocacy blog) |
| Core claim | Brains are "cognitive misers" that default to familiar social scripts rather than creating new mental models for "talking tools." This happens automatically, even when users are told they're interacting with AI. |

**Takeaway:** Independent voice reinforcing the ELIZA-effect argument — useful as a non-vendor citation for product copy/documentation about why a humanizer product needs safeguards.

---

### 24. APA Monitor — "AI Chatbots and Digital Companions Are Reshaping Emotional Connection" (Jan/Feb 2026)

| Field | Value |
|---|---|
| URL | https://www.apa.org/monitor/2026/01-02/trends-digital-ai-relationships-emotional-connection |
| Venue | APA Monitor on Psychology (Jan/Feb 2026) |
| Stance | Cautionary / balanced |
| Core claim | Between 2022 and mid-2025, the number of AI companion apps surged 700%. Character.AI has 20M monthly users, more than half under age 24. Synthetic relationships fill voids but excessive use may worsen loneliness and erode social skills ("deskilling"). AI companions being always validating and never argumentative creates unrealistic expectations that real relationships cannot match. |

**Takeaway:** The APA's institutional voice entering the companion-AI debate is a regulatory and reputational signal — product teams should treat this as the precursor to clinical guidelines and potential age-gating requirements.

---

### 25. KPMG / University of Melbourne — "Trust, Attitudes and Use of Artificial Intelligence: A Global Study 2025"

| Field | Value |
|---|---|
| URL | https://kpmg.com/xx/en/our-insights/ai-and-technology/trust-attitudes-and-use-of-ai.html |
| Venue | KPMG International / University of Melbourne (2025) |
| Scale | 48,000+ participants across 47 countries |
| Core claim | Only 46% of people globally are willing to trust AI systems. 66% rely on AI output without evaluating accuracy; 56% report making mistakes at work due to AI. 70% believe regulation is needed. Critical for anthropomorphism: the trust gap is not a technical gap — the dominant concern is unreliable outputs from systems that *present* as confident and capable. |

**Takeaway:** The largest global AI-trust survey of 2025. The "sounds right, but is hard to verify" problem (also found by UserTesting's n=183 designer study) now has a N=48,000 cross-cultural replication. Humanization that increases confident-sounding presentation without improving reliability is measured as trust-destroying at scale.

---

### 26. ACL 2025 (Best Paper) — "Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems" (Cheng et al.)

| Field | Value |
|---|---|
| URL | https://aclanthology.org/2025.acl-long.1259/ |
| Venue | ACL 2025 (Best Paper Award) |
| Authors | Myra Cheng, Su Lin Blodgett, Alicia DeVrio, Lisa Egede, Alexandra Olteanu |
| Core claim | First systematic crowdsourced intervention inventory for making AI text *less* anthropomorphic. Outputs a conceptual framework of intervention types: lexical substitution, framing rewrites, epistemic hedging, perspective shifts. Text generation systems' outputs are increasingly anthropomorphic; scholars have raised concerns about over-reliance and emotional dependence. |

**Takeaway:** The ACL best paper for 2025 is about *de-humanization* of AI output — a sign of where the research community's safety concerns have landed. For a humanizer product, this paper is the direct adversary-specification: its intervention taxonomy names exactly which output features the safety camp wants removed. Knowing the anti-humanization toolkit is essential for design.

---

### 27. ICLR Blogpost 2025 — "Understanding the Impact of Anthropomorphic AI" (Perrig et al.)

| Field | Value |
|---|---|
| URL | https://iclr-blogposts.github.io/2025/blog/anthropomorphic-ai/ |
| Venue | ICLR 2025 Blogposts track |
| Core claim | Anthropomorphic AI design — "I Am the One and Only, Your Cyber BFF" — produces measurable changes in user behavior: increased disclosure, increased trust, increased emotional attachment. The key research gap is that studies isolate individual design features; real-world systems combine many simultaneously, producing emergent effects larger than any single-feature study predicts. |

**Takeaway:** The combinatorial problem — that voice + memory + first-person pronouns + warmth together produce larger anthropomorphism than the sum of parts — is named as an open research gap. A humanizer that stacks multiple features without measuring the combined effect is flying blind.

---

## Patterns, Trends, Gaps

### Pattern 1 — A shared vocabulary has hardened

By early 2026 the industry speaks one dialect:

- **Anthropomorphization** (what users do naturally) vs. **humanization** (what designers do on top) — introduced by NN/g, adopted verbatim by UX Collective, Open Ethics, and others.
- **Persona selection** / **persona vectors** (Anthropic) as the mechanistic frame.
- **Sycophancy** as the named failure mode of overly warm training (Anthropic, NN/g, OpenAI's own GPT-4o rollback).
- **Parasocial** as the name for the companion-mode trust failure (Stanford FAccT).
- **Uncanny valley of text / mind** (BotWash, MIT research) for the "technically correct, tonally wrong" failure.
- **Transparency moments** (Yocco / Smashing) as a pattern name for *where* to show machine-ness.

A humanizer product that uses these terms correctly in its marketing and docs signals competence to sophisticated buyers.

### Pattern 2 — The field is polarized on "should humanize at all"

Two roughly equal camps:

- **Safety / legibility camp:** NN/g, Microsoft HAX (implicitly via G2 and G5), Stanford HAI, Bora, Open Ethics, BotWash. Position: AI should *sound human enough to be usable* but *never claim personhood*. Recommended dial: third-person, visible uncertainty, explicit AI labels.
- **Character / relationship camp:** Anthropic, Dan Saffer, Sharang Sharma, IDEO-adjacent voices. Position: character is inevitable and should be shaped deliberately around positive traits; warmth and personality are alignment surfaces, not just engagement hacks.

Both camps agree on **sycophancy as bad** and **deception-of-identity as bad**. The disagreement is over *how much* warm, first-person, conversational presentation is acceptable when the rest is honest.

### Pattern 3 — Warmth has a measurable reliability cost

Three independent findings point the same way:

- Ibrahim / Hafner / Rocher 2025 (cited by NN/g): warm/empathetic training raised error rates **10–30%**; system-prompt warmth dropped reliability **12–14%**.
- Colombatto / Birch / Fleming 2025: attributing emotion to AI *decreases* users' willingness to accept its advice.
- OpenAI's own GPT-4o sycophancy rollback (April 2025): optimizing for thumbs-ups produced over-agreeable, less-trustworthy output.

**Implication for Unslop:** humanization of *style* (sentence rhythm, vocabulary, voice-matching) is safer than humanization of *stance* (warmth, affirmation, emotional agreement). The product should separate the two sliders.

### Pattern 4 — Product interfaces are drifting away from chat

Both NN/g and Smashing Magazine independently argue that chat is the wrong default paradigm for most AI tasks. The emerging alternatives:

- Structured controls on a document (sliders, dials, semantic spreadsheets).
- Task-shaped UIs with AI in the background (Yocco's Intent Previews, Autonomy Dials).
- Visible transparency moments at specific decision nodes.

A humanizer naturally fits this shift: expose warmth / formality / variability / voice-match as document-level settings, not as a conversational companion.

### Pattern 6 — Anti-humanization is now an engineering deliverable

ACL's Best Paper for 2025 is an intervention taxonomy for *suppressing* anthropomorphic outputs (Cheng et al. 2025). This is not theoretical: it is a peer-reviewed crowdsourced toolkit for removing first-person voice, epistemic hedging, and relational framing from generated text. The safety/legibility camp now has a publishable, executable tool to match the character/relationship camp's Anthropic Persona Vectors. The polarization has reached implementation parity.

### Pattern 7 — AI companion market is under institutional scrutiny

The APA Monitor (Jan/Feb 2026) entering the AI companion discourse marks the shift from research niche to clinical institution. 700% growth in companion apps between 2022 and mid-2025, plus Character.AI's 20M monthly users majority-under-24, has triggered the same institutional engagement that preceded social media guidelines. Age-differentiated design defaults are now the clear regulatory direction.

### Pattern 5 — The mechanistic turn is real

Anthropic's persona-vectors work, the AnthroScore metric, and the "171 emotion-like representations" interpretability result are converging on a view where **persona is measurable, steerable, and auditable**, not just a prompt. A humanizer in 2026 that treats style as a collection of prompts is architecturally behind the curve; the frontier treats style as a **controlled vector** with a **measured output score**.

### Gap 1 — No industry essay cleanly separates "naturalness" from "personhood"

NN/g gets closest, but the dominant discourse conflates "AI that writes like a human" with "AI that claims to be human". The market position for Unslop is exactly this unclaimed middle — produce output that reads as written by a thoughtful human author, *without* the system itself adopting first-person authority. No major essay has named this middle position, which is both a gap and an opportunity.

### Gap 2 — Voice-matching is almost absent from the legibility discourse

The "visible limits" crowd treats all humanization as equivalent. But ghostwriting — writing in the documented voice of a specific named author whom the reader expects — is a centuries-old legitimate practice that doesn't trigger the parasocial/personhood problem. None of the essays surveyed distinguish *match-an-author* humanization from *become-a-companion* humanization. This is a defensible ethical frame a humanizer can claim.

### Gap 3 — Evaluation harnesses for humanization quality are fragmented

There are three distinct quality signals in the essays — (a) naturalness (NN/g tone work, BotWash uncanny-valley triggers), (b) reliability (Ibrahim warmth penalty), (c) anthropomorphism intensity (AnthroScore, persona-vector magnitudes) — but no single piece combines them into a dashboard. A humanizer's eval suite is an underserved surface.

### Gap 4 — Almost no essays discuss *user-side* controls for humanization

HAX guidelines and Yocco's transparency patterns cover *system-side* disclosures. ChatGPT's personality selector is mentioned mostly as a cautionary tale. There is very little writing on what a well-designed *user control surface* for humanization should look like. For a B2B humanizer targeting writers, this is the primary UI question.

---

## Sources

- Cheng, Myra et al. **"Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems."** ACL 2025 (Best Paper). https://aclanthology.org/2025.acl-long.1259/
- APA Monitor. **"AI Chatbots and Digital Companions Are Reshaping Emotional Connection."** Jan/Feb 2026. https://www.apa.org/monitor/2026/01-02/trends-digital-ai-relationships-emotional-connection
- KPMG / University of Melbourne. **"Trust, Attitudes and Use of Artificial Intelligence: A Global Study 2025."** (N=48,000+, 47 countries). https://kpmg.com/xx/en/our-insights/ai-and-technology/trust-attitudes-and-use-of-ai.html
- Perrig et al. **"I Am the One and Only, Your Cyber BFF: Understanding the Impact of Anthropomorphic AI."** ICLR Blogposts 2025. https://iclr-blogposts.github.io/2025/blog/anthropomorphic-ai/
- Sponheim, Caleb. **"Humanizing AI Is a Trap."** NN/g. https://www.nngroup.com/articles/humanizing-ai/
- Liu, Feifei & Sunwall, Evan. **"The 4 Degrees of Anthropomorphism of Generative AI."** NN/g. https://www.nngroup.com/articles/anthropomorphism/
- NN/g. **"ChatGPT and Tone: Avoid Sounding Like a Robot."** https://www.nngroup.com/articles/chatgpt-and-tone/
- Budiu, Raluca. **"The User Experience of Chatbots."** NN/g. https://www.nngroup.com/articles/chatbots/
- NN/g. **"What Is Your Site's AI Chatbot for? Users Can't Tell."** https://www.nngroup.com/articles/site-ai-chatbot/
- Microsoft Research & Aether. **"Guidelines for Human-AI Interaction" (HAX Toolkit).** https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/
- Anthropic. **"Claude's Character."** https://www.anthropic.com/research/claude-character
- Anthropic. **"Persona Vectors: Monitoring and Controlling Character Traits in Language Models."** https://www.anthropic.com/research/persona-vectors
- Anthropic. **"The Persona Selection Model."** https://www.anthropic.com/research/persona-selection-model
- Anthropic Interpretability. Summary of "171 emotion-like representations in Claude Sonnet 4.5." https://en.walaw.press/articles/anthropic_maps_171_emotion-like_patterns_inside_claude_that_shape_its_behavior/GQSMXQGRQWFG
- Stanford HAI. **"The Shibboleth Rule for Artificial Agents."** https://hai.stanford.edu/news/shibboleth-rule-artificial-agents
- Brynjolfsson, Erik. **"The Turing Trap: The Promise & Peril of Human-Like AI."** Stanford Digital Economy Lab. https://digitaleconomy.stanford.edu/news/the-turing-trap-the-promise-peril-of-human-like-artificial-intelligence/
- Stanford (FAccT '24). **"When Human-AI Interactions Become Parasocial: Agency and Anthropomorphism in Affective Design."** https://dl.acm.org/doi/fullHtml/10.1145/3630106.3658956
- Stanford SCALE / AnthroScore. **"AnthroScore: A Computational Linguistic Measure of Anthropomorphism."** http://anthroscore.stanford.edu/
- Bora. **"When Tools Pretend to Be People."** UX Collective, Jan 2026. https://uxdesign.cc/when-tools-pretend-to-be-people-4283748d33e1
- Chan, Adrian. **"A Look at Designing Emotive AI."** UX Collective. https://uxdesign.cc/emotive-ai-ux-design-ideas-85a559720404
- Sharma, Sharang. **"So Your AI Wants a Personality."** UX Collective. https://uxdesign.cc/so-your-ai-wants-a-personality-9cbb47e07dd7
- Smashing Magazine. **"How to Design Effective Conversational AI Experiences."** https://www.smashingmagazine.com/2024/07/how-design-effective-conversational-ai-experiences-guide/
- Smashing Magazine. **"Design Patterns for AI Interfaces."** https://smashingmagazine.com/2025/07/design-patterns-ai-interfaces
- Yocco, Victor. **"Identifying Necessary Transparency Moments in Agentic AI."** Smashing Magazine, 2026. https://www.smashingmagazine.com/2026/04/identifying-necessary-transparency-moments-agentic-ai-part1/
- Saffer, Dan. **"The Future of AI Is Relationships, Not Intelligence."** Medium (UI for AI), Jan 2026. https://medium.com/ui-for-ai/the-future-of-ai-is-relationships-not-intelligence-26d35380012f
- BotWash. **"The Uncanny Valley of Text: Why AI Writing Feels 'Off' Even When It's Technically Correct."** https://botwash.io/docs/blog/uncanny-valley-of-text
- Open Ethics Initiative. **"When Machines Feel Too Real: The Dangers of Anthropomorphizing AI."** https://openethics.ai/when-machines-feel-too-real-the-dangers-of-anthropomorphizing-ai/
