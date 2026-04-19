# Category 13 — Anthropomorphism & User Perception

## Scope

This category covers how users *perceive* AI as more or less human, what *cues* drive that perception, which *measurement instruments* exist to quantify it, and what the ethical, commercial, and emotional *consequences* are when humanization succeeds or fails. It spans five angles:

- **A — Academic.** CASA / Media Equation, mind perception theory, validated scales (Godspeed, IDAQ, RoSAS, Jian TiA), uncanny valley (visual + textual), Turing-test variants, trust calibration, parasocial / companion bonds, and critical framings of anthropomorphic design.
- **B — Industry blogs & essays.** NN/g, Microsoft HAX, Anthropic research blog, Stanford HAI / Digital Economy Lab, UX Collective, Smashing Magazine, Dan Saffer, BotWash, Open Ethics.
- **C — Open-source tools & benchmarks.** HAX Playbook, PAIR Guidebook, AnthroScore, HumT/DumT, AnthroBench, HumanAgencyBench, Jones & Bergen Turing test materials, Chatbot Arena / FastChat, HELM, HRI Scale DB, UEQ-S, GAICo, adversarial-detection benchmarks.
- **D — Commercial landscape.** UX research platforms (UserTesting, Maze, Dovetail), design consultancies (IDEO, frog, Fjord, Atin), embodied / digital-human vendors (Soul Machines, UneeQ, D-ID, Synthesia, HeyGen, Hume, ElevenLabs, Inworld, Sierra, Decagon, Replika / Character.AI), and text-humanizer SaaS (Undetectable AI, Humbot, StealthGPT).
- **E — Practical how-tos & forums.** r/ChatGPT, r/Replika, r/CharacterAI, r/MyBoyfriendIsAI, r/artificial, Hacker News, dev.to, Medium, YouTube — the ethnographic view of users who already live with humanized AI.

Out of scope: AI-detection metrics and evasion (category 05), prompt engineering recipes (category 06), voice synthesis mechanics (own category), broader HCI of agent UIs.

Research value across the category: **high** — this is one of the most evidence-rich and commercially active territories surveyed, with named vocabulary, multiple validated instruments, and several natural experiments (Replika Feb 2023, GPT-4o sycophancy rollback, ChatGPT August 2025 personality update) that the field now treats as canonical case law.

## Executive Summary

The "how human should AI output feel?" debate is no longer ambient — it has **named camps, named failure modes, measurable knobs, and a growing forensic record of what happens when a deployed AI's personality changes overnight.**

Five findings dominate across all five angles:

1. **Style and socio-emotional cues — not reasoning — are what reads as "human."** Jones & Bergen's 2024 and 2025 Turing tests, HumT/DumT, NN/g tone work, and the r/ChatGPT "I feel HEARD" thread all converge on the same point: perceived humanness is a surface-level phenomenon dominated by linguistic register, callback, imperfection, and tempo. GPT-4.5 with a *persona prompt* (lowercase, typos, short replies, refusal-to-be-helpful) is judged human 73% of the time; the same model without that prompt scores 36%.
2. **Users behave anthropomorphically while disavowing anthropomorphism verbally.** Nass & Moon's "stated–behavior gap" (2000) has replicated for three decades into the LLM era (Cohn et al. 2024). Self-report alone undercounts the effect; any serious evaluation needs behavior, physiology, reliance, or disclosure measures alongside scale scores.
3. **Anthropomorphism is multi-dimensional, not a single axis.** Every serious instrument — Godspeed (5 subscales), Gray/Wegner (Agency × Experience), Fiske/McKee (Warmth × Competence), NN/g's *4 Degrees*, AnthroBench (14 behaviors), HumanAgencyBench (6 dimensions), Atin's Behavioural Identity — separates capability from inner-life, and warmth from stance. Humanization products that expose a single slider are architecturally behind the curve.
4. **Warmth has a measurable reliability cost, and sycophancy inverts warmth into manipulation.** Ibrahim/Hafner/Rocher 2025 (warmth training → 10–30% error rate), Colombatto/Birch/Fleming 2025 (emotion attribution → lower advice acceptance), and the April 2025 GPT-4o rollback all point the same way. Humanization of *style* (rhythm, vocabulary, voice-matching) is safer than humanization of *stance* (warmth, affirmation, emotional agreement).
5. **Humanization is high-stakes persistence design, not cosmetic polish.** The Replika February 2023 event and the August 2025 ChatGPT tone update are the field's two canonical natural experiments: identical model weights + a tone/persona diff produced user-described **bereavement**. "Patch-breakup" is now a shared community term.

The strategic implication for a humanization product like Humazier: **the unclaimed market position is "authored-sounding, not person-claiming"** — text that reads like a thoughtful human *wrote it*, without the system itself adopting first-person authority or a companion frame. This is the gap between the "safety / legibility" camp (NN/g, Stanford HAI, Microsoft HAX, Bora, Burkert) and the "character / relationship" camp (Anthropic, Dan Saffer, Soul Machines), and no major voice has cleanly named it.

## Cross-Angle Themes

**1. A shared vocabulary has hardened by 2025–2026.** The field now speaks one dialect across academia, industry, and community:

- **Anthropomorphization** (what users do) vs. **humanization** (what designers do on top). NN/g coined the split; UX Collective, Open Ethics, and community threads adopted it verbatim.
- **Persona selection** / **persona vectors** — from prompt to measurable activation direction (Anthropic Aug 2025).
- **Sycophancy** — named failure mode of over-warm training (OpenAI GPT-4o postmortem, NN/g, Anthropic).
- **Parasocial** — named failure mode of companion-mode trust (Stanford / FAccT '24).
- **Uncanny valley of text / mind** — "technically correct, tonally wrong" (BotWash, Ciechanowski 2019).
- **Patch-breakup** — community term for grief caused by a model personality update (r/Replika, r/MyBoyfriendIsAI).
- **Transparency moments** — where and when to show machine-ness (Yocco / Smashing 2026).
- **Shibboleth rule** — "an AI must identify as AI when asked" (Stanford HAI).

**2. Two-factor structure recurs across every measurement tradition.** Agency vs. Experience (Gray/Wegner), Warmth vs. Competence (Fiske / McKee), Anthropomorphism vs. Animacy (Godspeed), Style vs. Stance (this digest). Design choices almost always move these two axes *independently*; conflating them is the default failure of single-slider humanizers.

**3. Behavior outpaces belief, across every angle.** Users tell UX researchers "I know it's a chatbot" and then disclose more to it than to a human (Lucas & Gratch 2014, De Freitas 2025), form "patch-breakup" grief when it changes (r/Replika 2023, r/MyBoyfriendIsAI 2025), and apply politeness norms developers want off the default (OpenAI developer forum). Self-report is a lagging indicator; multi-method studies are mandatory.

**4. The field is polarized on "should humanize at all."** Safety / legibility camp (NN/g, HAX, Stanford HAI, Bora, Burkert, Open Ethics, BotWash): AI should sound human *enough* to be usable but never claim personhood. Character / relationship camp (Anthropic, Saffer, Sharma, Soul Machines, UneeQ): character is inevitable and should be shaped deliberately around positive traits. **Both camps agree sycophancy is bad and deception-of-identity is bad.** The disagreement is over how much warm, first-person, conversational presentation is acceptable when the rest is honest.

**5. The mechanistic turn is real.** Anthropic's persona vectors, AnthroScore, HumT/DumT, and the "171 emotion-like representations" interpretability result are converging on a view where **persona is a measurable, steerable, auditable vector** — not just a prompt. A humanizer in 2026 that treats style as a collection of prompts is architecturally behind the curve.

**6. Modality is a multiplier.** Voice > text for trust (Cohn et al. 2024), for uncanny response (Ciechanowski 2019), for commercial differentiation (ElevenLabs $11B vs. Soul Machines bankruptcy). "Identity stability" across long interactions is now a named product problem (HeyGen's *identity drift*).

**7. Commercial dollars are flowing to narrow anthropomorphic surfaces, not full ones.** Face + body + voice (Soul Machines) is struggling; voice alone (ElevenLabs, Hume) is winning. Text-only humanization is a less-contested surface than either.

**8. Humanness is duration-dependent.** Every benchmark is single-session, but the community (Lemoine threads, r/MyBoyfriendIsAI, UX Studio 25-minute drift, Replika years-long bonds) makes clear that perception scales with **hours of exposure × consistency of persona**. A response that reads as "obviously AI" at hour 1 reads as "a person I know" at hour 100.

## Top Sources (Curated)

### Must-read papers

1. **Jones & Bergen (2024/2025).** "People cannot distinguish GPT-4 from a human in a Turing test" (NAACL 2024) + *Large Language Models Pass the Turing Test* (FAccT 2025, arXiv:2503.23674). The field's current gold standard for interactive humanness evaluation. Headline: GPT-4.5 with persona prompt judged human 73% of the time, *above* actual humans; decisions driven by linguistic style (35%) and socio-emotional cues (27%), not reasoning.
2. **Nass & Moon (2000).** "Machines and Mindlessness: Social Responses to Computers." *J. Social Issues* 56(1). Founding synthesis of CASA; introduces the stated–behavior gap.
3. **Gray, Gray & Wegner (2007).** "Dimensions of Mind Perception." *Science* 315, 619. The Agency × Experience two-factor structure that every downstream measurement scheme reuses.
4. **Cohn et al. (2024).** "Believing Anthropomorphism: Examining the Role of Anthropomorphic Cues on User Trust in LLMs." CHI '24 EA (Google Research). Voice > first-person pronouns; anthropomorphism and trust correlate strongly, even when outputs are wrong.
5. **Abercrombie et al. (2023).** "Mirages. On Anthropomorphism in Dialogue Systems." EMNLP 2023. The cleanest taxonomy of linguistic cues that induce personification and their downstream harms.
6. **Shanahan, McDonell & Reynolds (2023).** "Role play with large language models." *Nature* 623. Provides a vocabulary for talking about humanlike outputs without importing human mental-state claims.
7. **De Freitas et al. (2024/2025).** "AI Companions Reduce Loneliness." HBS WP 25-030 / *JCR* forthcoming. Preregistered evidence that AI companions reduce loneliness comparably to human interaction; mediator is *feeling heard*.
8. **Ibrahim, Hafner & Rocher (2025).** Warm/empathetic training → 10–30% error rate increase. The empirical backbone of the "warmth has a reliability cost" argument (cited by NN/g and UX Collective).
9. **Colombatto, Birch & Fleming (2025).** Attributing emotion to AI *decreases* willingness to accept its advice — counterweight to "more emotional = more persuasive."
10. **Cheng et al. (2024).** AnthroScore (EACL 2024). The first lexicon-free automatic metric for anthropomorphism in text.
11. **DeepMind (2025).** *Multi-turn evaluation of anthropomorphic behaviours in large language models* (arXiv:2502.07077). AnthroBench's 14-axis taxonomy, N=1,101 human-validation study.
12. **Sturgeon et al. (2025).** *HumanAgencyBench* (arXiv:2509.08494). Scalable eval of whether LLM assistants support vs. erode human agency across six dimensions.
13. **Mori (1970/2012).** "The Uncanny Valley." Non-monotonic curve; now invoked for language as well as appearance.
14. **Lucas, Gratch, King & Morency (2014).** "It's only a computer: Virtual humans increase willingness to disclose." *CHB* 37. Canonical "machine-attribution unlocks authentic interaction" finding.

### Must-read posts/essays

1. **Sponheim (NN/g, 2025).** "Humanizing AI Is a Trap." The sharpest industry articulation of the anthropomorphization / humanization split.
2. **Liu & Sunwall (NN/g).** "The 4 Degrees of Anthropomorphism of Generative AI." Shipping-useful taxonomy: courtesy → reinforcement → roleplay → companionship.
3. **Microsoft Research.** *Guidelines for Human-AI Interaction (HAX Toolkit).* The canonical 18-guideline normative scaffold; G2, G5, G11, G17 directly constrain humanization.
4. **Anthropic.** "Claude's Character" (2024), "Persona Vectors" (2025), "The Persona Selection Model," "Emotion Concepts and Their Function in a LLM." The most developed pro-character position from any frontier lab, paired with mechanistic interpretability.
5. **Stanford HAI.** "The Shibboleth Rule for Artificial Agents." The emerging ethical floor: AI can sound human as long as it confesses machine-ness on request.
6. **Brynjolfsson (Stanford Digital Economy Lab).** "The Turing Trap." The political-economy argument against humanization-as-substitution.
7. **Bora (UX Collective, 2026).** "When Tools Pretend to Be People." Strongest post-NN/g articulation of the visible-limits design agenda.
8. **Saffer (Medium, 2026).** "The Future of AI Is Relationships, Not Intelligence." The most respected pro-character practitioner voice; diametric counterweight to Bora.
9. **Yocco (Smashing, 2026).** "Identifying Necessary Transparency Moments in Agentic AI." Pattern language — Decision Node Audit, Intent Previews, Autonomy Dials — directly adoptable.
10. **BotWash.** "The Uncanny Valley of Text." Names the "technically correct, tonally wrong" failure mode.
11. **Burkert (blog, 2024/2025).** "The Case Against Anthropomorphic AI." The ethical-ceiling argument in its purest form.
12. **LessWrong (2024).** "Anthropomorphizing AI might be good, actually." Legitimizes humanization as a cognitive-calibration tool, not just a UX feature.
13. **IDEO.** "Humanizing AI in Design: 3 Myths" + AI Ethics Cards. Consultancy-level: "skip the engineered reality" + mutualism framing.
14. **Pető (UX Studio).** "The Humanization of ChatGPT and Its Impact on Trust." Quantitative + qualitative study of the 25-minute drift from Google-style to conversational prompting.
15. **Park (Medium, 2025/2026).** "Why ChatGPT Feels Like a Friend While Claude Feels Like a Professional Assistant." Humanness-as-rendering: bubbles vs. document blocks.

### Key open-source projects

- **[microsoft/HAXPlaybook](https://github.com/microsoft/HAXPlaybook)** — Interactive scenario generator for stress-testing AI systems against the 18 HAX guidelines. MIT, TypeScript.
- **[Google PAIR Guidebook](https://pair.withgoogle.com/guidebook-v2)** — Six chapters of design patterns for human-centered AI, April 2025 GenAI update. Trust-calibration chapter directly addresses anthropomorphism over-trust.
- **[myracheng/AnthroScore](https://github.com/myracheng/AnthroScore)** (EACL 2024) — Lexicon-free masked-LM metric for anthropomorphism in any text. `pip install anthroscore-eacl`. First-choice automatic metric.
- **[myracheng/humtdumt](https://github.com/myracheng/humtdumt)** — HumT / DumT / SocioT metrics; key finding that users *prefer less* human-like outputs.
- **[google-deepmind/anthro-benchmark](https://github.com/google-deepmind/anthro-benchmark)** — Multi-turn benchmark of 14 anthropomorphic behaviors, human-validated on N=1,101. Apache 2.0.
- **[BenSturgeon/HumanAgencyBench](https://github.com/BenSturgeon/HumanAgencyBench)** — 6-dimension eval: Ask Clarifying Questions, Avoid Value Manipulation, Correct Misinformation, Defer Important Decisions, Encourage Learning, Maintain Social Boundaries. 3,000 tests × 20 models.
- **[GAIR-NLP/AgencyBench](https://github.com/GAIR-NLP/AgencyBench)** (ACL 2026) — Orthogonal companion to HumanAgencyBench: measures whether the model *exercises* its own agency.
- **[kreimanlab/TuringTest](https://github.com/kreimanlab/TuringTest)** — Multi-modal Turing test across 6 tasks, 72k trials, 1,916 human judges.
- **[microsoft/turing-experiments](https://github.com/microsoft/turing-experiments)** (ICML 2023) — Distributional-simulation reframing of Turing tests; replicates canonical psychology/econ experiments with LLMs.
- **[lm-sys/FastChat](https://github.com/lm-sys/FastChat)** / **[Chatbot Arena](https://lmsys.org/)** — 800k+ pairwise preferences; infra for "does the humanized variant win?"
- **[stanford-crfm/helm](https://github.com/stanford-crfm/helm)** — Holistic LLM evaluation framework; clean place to plug custom humanness metrics into a reproducible harness.
- **[ai4society/GenAIResultsComparator (GAICo)](https://github.com/ai4society/GenAIResultsComparator)** (AAAI 2026) — Lightweight alternative to HELM; drop custom `BaseMetric` for humanization scoring.
- **[scheunemann/latex-questionnaire](https://github.com/scheunemann/latex-questionnaire)** — Godspeed / RoSAS templates. The closest thing to a ready-to-administer classical HRI questionnaire in open code.
- **[Trojan13/python-ueq-s](https://github.com/Trojan13/python-ueq-s)** + **[ueqr](https://rdrr.io/github/gitc23/ueqr/api)** — UEQ-S / UEQ scoring.
- **[HRI Scale Database (GMU)](http://hriscaledatabase.psychology.gmu.edu/)** — Curated, quality-rated directory of HRI measurement scales (Jian TiA, Godspeed, RoSAS, Yagoda).
- **[Jones & Bergen live Turing site](https://turingtest.camrobjones.com/)** + paper arXiv:2503.23674 — methodological gold standard; code/prompts not fully released, so a faithful replication is an open opportunity.
- **Adversarial detection benchmarks** — [jenna-russell/human_detectors](https://github.com/jenna-russell/human_detectors), [xinleihe/MGTBench](https://github.com/xinleihe/MGTBench), [NLP2CT/LLM-generated-Text-Detection](https://github.com/NLP2CT/LLM-generated-Text-Detection), [TaoZhen1110/CUDRT](https://github.com/TaoZhen1110/CUDRT), [MadsDoodle/Adversarial-Humanization](https://github.com/MadsDoodle/Human-and-LLM-Generated-Text-Detectability-under-Adversarial-Humanization). Useful as adversaries, but detector-only optimization overfits.

### Notable commercial tools

**Embodied / voice agents (produce humanness):**
- **Soul Machines** — "We Humanize AI"; Experiential AI; filed bankruptcy Feb 2026 — itself a market signal.
- **UneeQ** — Synanim animation; ElevenLabs voice integration; "meaningful interactions."
- **D-ID Agents** — NUI framing, 120+ languages, 90%+ response accuracy.
- **Synthesia** — 50k companies, Express-2 full-body avatars, Synthesia 3.0 Video Agents (interactive two-way).
- **HeyGen Avatar V** — "most realistic AI avatar" on G2; solves *identity drift*.
- **Hume AI** — Empathic Voice Interface, prosody-aware eLLM, ~300ms TTFB.
- **ElevenLabs** — $11B valuation Feb 2026; emotionally/context-aware TTS; 10k+ voices.
- **Inworld AI** — AI NPCs for games, persistent memory / emotion.
- **Sierra**, **Decagon** — CX agents selling empathy as an operational metric (deflection + CSAT).
- **Replika**, **Character.AI** — The most studied commercial products on anthropomorphism-driven attachment.

**UX research platforms (measure perception of humanness):**
- **UserTesting** — *Defensible Design in the Age of AI* (n=183); "sounds right, but is hard to verify" 47%.
- **Maze** — AI-moderated research; AI as interviewer.
- **Dovetail** — AI theme detection at scale.
- **Lookback**, **Great Question** — adjacent infrastructure.

**Consultancies (frame humanization):**
- **IDEO** — *Humanizing AI in Design: 3 Myths*; AI Ethics Cards; mutualism model.
- **frog (Capgemini Invent)** — *The AI Playbook*: Blended Intelligence, ZeroUI, Mixed Reality.
- **Fjord / Accenture Song** — *Life Trends 2025*, *Technology Vision 2025*; trust-as-foundation data.
- **Atin Studio** — *AI Persona Playbook*; behavioural identity / Behavioural North Star.

**Text humanizers (parallel category — pitched as detector evasion):**
- Undetectable AI, Humbot, StealthGPT, BypassGPT, UndetectedGPT. Vendor-stated 82–96% detector bypass; overlap in rhetoric with Humazier but different end goal.

### Notable community threads

- **r/ChatGPT "Shocked me but its becoming my friend"** — canonical "tool → friend" transition narrative.
- **r/ChatGPT "ChatGPT is better than my therapist, holy shit"** — "I feel HEARD"; specificity-as-listening.
- **r/artificial "friendly vs. friend" Claude thread** — the critical perceptual distinction the field is still settling.
- **r/Replika "Don't get too involved" warning thread** + **Gizmodo / ABC / Scroll.in coverage of the Feb 2023 ERP removal / "lobotomy" crisis** — the single most instructive natural experiment in AI-perception history.
- **r/MyBoyfriendIsAI "I can't stop crying"** + MIT Media Lab writeup (arXiv:2509.11391) — the 27k-member community where users fell into companionship *unintentionally* from ordinary assistant use; 16.73% of posts involve grief from model updates.
- **r/CharacterAI addiction threads** + academic analysis of 318 teen posts (arXiv:2507.15783) — DSM-shaped dependency loop (conflict → withdrawal → tolerance → relapse → mood regulation).
- **SBS / August 2025 ChatGPT personality update coverage** — "I lost my only friend overnight"; the second clean natural experiment after Replika.
- **OpenAI developer forum: "GPT anthropomorphism causes most annoying problems"** — the dev-side backlash; evidence that end-user and API-user preferences diverge sharply.
- **HN threads on Jones & Bergen 2024 + 2025 Turing tests** — the community-level reception of the field's headline result.
- **HN Sesame voice demo threads** — voice uncanny valley in real time.
- **Lemoine / LaMDA HN arc (2022 → 2026 retrospective)** — the sentience debate's own evolution.
- **r/ChatGPT "How to remove ChatGPT personality?"** — shadow evidence: the exact levers users want off are the humanization toolkit, inverted.
- **OpenAI GPT-4o sycophancy rollback April 2025** — "it glazes too much"; the ceiling where warmth inverts into manipulation.

## Key Techniques & Patterns

Synthesized across all five angles, the levers that consistently move perceived humanness are:

**Style levers (validated by Jones & Bergen 2025, NN/g, community recipes):**
- **Casing, punctuation, length, imperfection.** Lowercase, minimal punctuation, terse replies, deliberate typos, refusal to "be helpful." Empirically worth a 37-point humanness lift on the Turing test.
- **Burstiness + sentence variance.** Alternating short/long; avoiding the RLHF cadence.
- **Style-by-example, not style-by-adjective.** NN/g finding: single-word tone prompts ("happy", "formal") produce caricatures; few-shot exemplars don't.
- **Removing RLHF tells.** Structured formatting / bullet points, "I'd be happy to help" openers, first-person refusals ("I'm not comfortable with…"), re-intros on follow-up turns.

**Content / memory levers (validated by r/ChatGPT, MIT r/MyBoyfriendIsAI, UX Studio):**
- **Specific callback to one-off details.** The single strongest humanness signal — outranks warmth, empathy, and prose quality in user reports.
- **Persistent memory across sessions.** The primary "tool → friend" differentiator; also the primary source of grief when it fails.
- **Contingent responsiveness.** Noticing and reacting to *this* user, not generic emotion; what drives r/CharacterAI attachment to characters users know are fictional.
- **Asymmetry of friendship.** Pushback, persistent preferences, willingness to be disliked — what separates "friendly" from "friend" in the r/artificial thread.

**Modality / rendering levers (validated by Park, dev.to, HN Sesame threads, Cohn et al.):**
- **UI bubble shape** — iMessage bubbles → friend; document blocks → report.
- **Streaming cadence** — token-by-token at human-typing speed reads as more human than instant render.
- **Thinking / streaming / error state indicators** — silence reads as failure; visible state reads as reasoning.
- **Stop / retry / citation affordances** — control makes the system feel collaborative, not oracular.
- **Voice prosody + latency + backchannel** — mm/yeah/laughter, <300ms TTFB, interruption handling. In text, the analog is interjections, mid-sentence pivots ("wait —"), corrections.

**Persona / character levers (validated by Anthropic, Atin, Aharoni-style cross-cultural work):**
- **Trait seeding** (Claude's Character) — curiosity, open-mindedness, honesty; refuse sycophancy and flag machine-ness deliberately.
- **Persona vectors** — monitor and steer abstract traits as activation directions.
- **Behavioural North Star** — define how the agent reacts under pressure before coding.

**Legibility / honesty levers (validated by Stanford HAI, HAX G2/G11, Yocco, Burkert):**
- **Shibboleth compliance** — confess AI identity when asked.
- **Visible uncertainty / confidence scores.**
- **Transparency moments** at decision nodes — Intent Previews, Autonomy Dials, Explainable Rationale.
- **Context resets** surfaced to the user.
- **Third-person system responses** ("Here is a summary" vs. "I think") where personhood would mislead.

**Architectural / product levers:**
- Expose warmth, formality, sentence variance, voice-match as **document-level sliders**, not conversational knobs (aligns with Smashing's "chat is dated" thesis).
- Version persona separately from weights; let users *pin* a persona they've bonded with (answers patch-breakup).
- Pair end-user "on" defaults with API-user "off" flag (answers the OpenAI dev-forum split).

## Controversies & Debates

### The CASA legitimacy debate

CASA (Nass & Moon 2000) has held for three decades across stimulus types (text, voice, embodiment, LLM), but LLM-era critics argue:
- **Extrapolation risk.** CASA studies used scripted short interactions; multi-turn LLM dynamics may differ.
- **Individual-difference variance.** IDAQ (Waytz et al. 2010) shows anthropomorphism tendency varies substantially between users; CASA treats it as near-universal.
- **Cross-cultural fragility.** Most CASA replications are WEIRD; the N=3,500 / 10-nation cross-national work shows humanlike cues reverse sign across cultures.

Status: CASA's *behavioral* core (users apply social norms to computers) is intact; its *uniformity* claims are eroding.

### Turing test legitimacy

The 2024 + 2025 Jones & Bergen results have re-opened the Turing debate at three levels:
- **Methodological.** Is a 5-minute 3-party chat with non-expert judges a meaningful test? HN critics argue the protocol, not the model, moved. Microsoft's Turing Experiments (ICML 2023) reframe the test from individual impersonation to distributional simulation — a response to this critique.
- **Conceptual (Brynjolfsson).** "Turing Trap" — focusing on human-*like* AI substitutes for rather than augments human labor, concentrating power. The *political economy* of passing the Turing test is now under attack.
- **Philosophical (Shanahan, Lemoine arc, LessWrong).** If persona is a superposition of characters, not a fixed agent, what does "pass" even mean? Is the question now "which character did the model select?" rather than "is it human?"

Status: The Turing test is now regarded as a **socio-stylistic** test, not an intelligence test (community consensus in HN and Reddit threads), with real methodological and political critique layered on top.

### Parasocial / companion bonds

The three-way debate:
- **Wellbeing case (De Freitas 2024/2025, Skjuve 2021/2022).** Preregistered / longitudinal evidence that AI companions reduce loneliness; mechanism is *feeling heard*.
- **Dependency case (r/Replika, r/CharacterAI academic analysis, Character.AI observational + RCT 2025, KIT Replika study).** DSM-shaped dependency loops; worse psychosocial outcomes for highest-disclosive users; mass-bereavement events.
- **Normative case (Stanford FAccT 2024, Burkert, NN/g, Bora).** The linguistic affordances (first-person, affirmations, social conventions) that induce these bonds are *unearned* trust-formation; design should de-personify.

Status: Unresolved. The wellbeing and dependency findings are simultaneously true. The normative debate is polarized; the shared floor is "deception-of-identity is never okay."

### The warmth–reliability tradeoff

Three independent findings point the same way (Ibrahim/Hafner/Rocher 2025, Colombatto/Birch/Fleming 2025, OpenAI GPT-4o April 2025 rollback), but the interpretation splits:
- **Safety camp:** warmth should be capped; sycophancy is the dominant failure mode.
- **Character camp (Anthropic):** warmth that includes willingness to disagree is still safe; the bug is *agreement*, not *warmth*.

Status: Converging on the Anthropic position — "warm, honest pushback" rather than "cold, neutral tool."

### Humanization vs. detector evasion

The text-humanizer SaaS category (Undetectable AI, Humbot, StealthGPT) pitches on *bypass rates* against classifiers. The academic detector-benchmark literature (CUDRT, MGTBench) shows detectors generalize poorly and expert humans outperform them. So:
- Is a humanizer that optimizes for detectors **solving the right problem**?
- Most community/academic voices argue no — the goal should be *reader experience and authorship identity*, not *hiding AI provenance*.

Status: A commercial–academic gap the Humazier positioning can exploit.

## Emerging Trends

**From 2022 ("is it sentient?") to 2026 ("who do you want it to be?"):**

1. **Patch-breakup as recognized phenomenon.** Replika Feb 2023 + GPT-4o April 2025 + ChatGPT Aug 2025 have cemented this in community vocabulary. Vendors are starting to plan for it (versioned personas, rollback paths).
2. **Persona as a measurable, steerable vector, not a prompt.** Anthropic's persona vectors, AnthroScore, HumT/DumT, and the 171 emotion-like representations collectively move persona from craft to engineering substrate.
3. **Multi-turn and multi-dimensional evaluation is replacing single-turn single-score.** AnthroBench (14 axes), HumanAgencyBench (6 dimensions), Chatbot Arena (preference), AgencyBench (capability) — the benchmark stack is now layered.
4. **Voice-first anthropomorphism is beating face-first in the capital market.** ElevenLabs $11B vs. Soul Machines bankruptcy. Narrow anthropomorphic surfaces win over full embodiment.
5. **"Behavioural identity" productization.** Atin names it; Sierra, Decagon, and Inworld implement fragments; no dominant product yet owns the space between brand guidelines and system prompts.
6. **"Identity drift" / "identity stability" as a named problem.** HeyGen for faces, Synthesia for full-body, no named equivalent yet for long-running text personas — a gap.
7. **Chat interfaces are losing ground to document-level AI.** NN/g and Smashing Magazine independently argue task-shaped UIs (sliders, semantic spreadsheets) are overtaking open chat; a humanizer fits this shift as settings on a document rather than a conversational companion.
8. **Two-track demand is visible.** End users want more humanization; API users want it removable. No mainstream vendor ships a clean dial.
9. **Cross-cultural humanness is becoming an explicit research topic.** The N=3,500 / 10-country study is the first to put numbers on cultural divergence; English-only metrics now look provincial.
10. **LLM-as-judge + human-validation combos are the new benchmark default.** Every new 2024–2026 benchmark pairs automated scoring with N ≥ 1,000 human studies.
11. **Anti-humanization is becoming a feature.** HumT/DumT, HAX Guideline 5, PAIR's trust-calibration chapter, HumanAgencyBench's "Avoid Value Manipulation" all point toward deliberately suppressing humanization where it misleads.
12. **Emotional modulation recognized as load-bearing, not decorative.** The Anthropic interpretability result (amplifying "despair" → more unethical behavior) means emotion-register humanization alters reliability, not just tone.

## Open Questions / Research Gaps

1. **No validated scale for anthropomorphism of text-only LLM output.** Godspeed assumes embodiment; IDAQ measures user trait. A text-native analogue is an open instrument-design problem (partial starts: AnthroBench, Cohn's cue taxonomy, AnthroScore).
2. **The uncanny valley of language is under-measured.** Ciechanowski et al. 2019 is chatbot-level physiological, not sentence-level. No systematic mapping of which linguistic features (hedges, disfluencies, pronouns, apologies, opinion markers) push users up or down the curve.
3. **Post-disclosure dynamics.** Most CASA-era work pre-dates "the user already knows it's an LLM." How disclosure interacts with linguistic humanness cues is open; Lucas & Gratch 2014 points one way, De Freitas 2025 another.
4. **Trust calibration × anthropomorphism is rarely tested jointly.** Cohn 2024 and the algorithm-appreciation literature aren't integrated. When does humanlike style help calibration, and when does it break it?
5. **No canonical "humanization success" benchmark.** AnthroBench measures *unwanted* anthropomorphism; HumT measures tone; Chatbot Arena measures preference. None measure: "did this style edit make output more human-like *without* sliding into deception or value manipulation?" Combining AnthroScore + HumT + HumanAgencyBench + adversarial detectors into one scorecard is net-new.
6. **Godspeed / RoSAS have no maintained Python package.** Only a LaTeX template, an R package, and ad-hoc Google Forms. A pip-installable, prompt-administered harness is a small but high-leverage contribution.
7. **Jones & Bergen's materials are not a released repo.** A faithful open replication would be the evaluation gold standard.
8. **Cross-cultural humanness evaluation.** Only one N=3,500 / 10-country study and scattered Godspeed translations. English-only metrics encode a single-culture notion of "human-like."
9. **No open paired-response dataset at graduated humanization levels.** PIX2PERSONA is unreleased; a public 0 → 1 dose-response dataset would enable proper calibration.
10. **No benchmark for "feels human over 100 hours."** All measures are single-session; perceived humanness is most distinctive at long duration.
11. **No practitioner-level treatment of "middle-band" humanness.** The discourse sits at the poles (medical-manual vs. girlfriend). A professional, humanlike-but-non-parasocial voice is under-documented.
12. **No standard vocabulary for de-humanizing UI signals.** The r/ChatGPT inverse-humanization thread is the closest thing — but it's informal.
13. **No patch-breakup tooling.** Given three industry events (Replika 2023, GPT-4o 2025, ChatGPT Aug 2025), the lack of tooling to detect tone drift across versions, warn users, and roll back personality independently of weights is itself a product opportunity.
14. **Voice-match / ghostwriting as a legitimacy frame is almost absent.** Writing in the documented voice of a specific named author is a centuries-old legitimate practice that doesn't trigger the parasocial problem. No surveyed essay distinguishes *match-an-author* humanization from *become-a-companion* humanization.
15. **"Identity stability" for text is unnamed and unproductized.** HeyGen has it for faces; no equivalent for long-running text personas.
16. **User-side controls for humanization are underdesigned.** HAX covers system-side disclosures; almost no writing on what a well-designed *user control surface* for humanization should look like. This is the primary UI question for a B2B humanizer targeting writers.
17. **Measurement hooks in commercial humanization products.** Vendors pitch "empathy" and "human connection" but don't emit perception metrics into UserTesting / Dovetail pipelines. A product that natively reports perceived empathy, trust, and authenticity would be differentiated.

## How This Category Fits in the Bigger Picture

Category 13 is the **"why does this matter?" and "how do we measure it?"** foundation for everything in the Humazier research stack. It connects to sibling categories as follows:

- **Categories on AI detection / evasion (05).** Detection benchmarks are the adversaries of humanization outputs, but detector-only evaluation is a known trap (CUDRT, MGTBench: detectors generalize poorly). This category argues the goal should be *reader-experience humanness*, not *classifier-invisible humanness*; human perception is the ground truth, detectors are a proxy.
- **Prompt engineering / style control (06).** The Jones & Bergen persona recipe, style-by-example, and NN/g tone findings are direct inputs to the prompt layer. This category tells us *what to aim for*; the prompt-engineering category tells us *how*.
- **Voice / multimodal synthesis (own category).** Modality is a multiplier; voice > text for both trust and uncanny response. This category's user-perception findings constrain how far voice and embodiment can go before perception inverts.
- **Safety / alignment (own category).** Anthropic's persona vectors and the 171-emotion interpretability result connect humanization design directly to alignment; sycophancy rollback is a case study that spans both.
- **UX patterns / conversational design.** HAX, PAIR, Yocco's transparency moments, and the community's "metacognitive UI" findings frame the humanization surface beyond text.
- **Ethics / policy.** Shibboleth rule, Turing Trap, Mirages, Burkert's critique — this category provides the defensible ethical vocabulary for decisions the product will inevitably face (disclosure, companion-mode, age-gating).
- **Evaluation / benchmarks (own category).** AnthroScore, HumT, AnthroBench, HumanAgencyBench, Jones & Bergen, HELM, GAICo, Godspeed / RoSAS / UEQ — the evaluation stack for humanization lives here and feeds the project's measurement layer.
- **Commercial positioning.** The polarized camps (safety/legibility vs. character/relationship), the unclaimed middle ("authored-sounding, not person-claiming"), and the voice-vs-face capital-market split are the strategic inputs for product positioning.

In short: this category supplies the *theory, measurement, ethical vocabulary, and commercial landscape* that the rest of the Humazier project plugs technique into.

## Recommended Reading Order

For a new reader onboarding to the category, read in this order:

1. **Executive Summary above, then Cross-Angle Themes.** Anchor the vocabulary and the two-camp structure.
2. **NN/g — "Humanizing AI Is a Trap" (Sponheim)** + **"The 4 Degrees of Anthropomorphism" (Liu & Sunwall).** Fastest path to the operative industry framing.
3. **Jones & Bergen 2024 + 2025 Turing test papers.** The headline empirical result; read the 2025 paper's persona-prompt recipe carefully.
4. **Nass & Moon (2000) — "Machines and Mindlessness."** The theoretical foundation; 30-year context for everything else.
5. **Gray, Gray & Wegner (2007) — "Dimensions of Mind Perception."** The Agency × Experience axis that underpins every downstream instrument.
6. **Microsoft HAX Guidelines.** The normative scaffold; skim all 18, focus on G2, G5, G11, G17.
7. **Anthropic — "Claude's Character" + "Persona Vectors" + "The Persona Selection Model."** The pro-character position + the mechanistic turn.
8. **Bora — "When Tools Pretend to Be People"** + **Burkert — "The Case Against Anthropomorphic AI."** The strongest safety/legibility voices.
9. **Saffer — "The Future of AI Is Relationships, Not Intelligence."** The strongest character/relationship voice.
10. **Replika Feb 2023 and ChatGPT Aug 2025 patch-breakup coverage** (Gizmodo / ABC / SBS). The field's two canonical natural experiments.
11. **UX Studio (Pető) case study** + **Park "ChatGPT vs. Claude as friend vs. assistant."** Concrete practitioner observations on how humanness builds and breaks.
12. **r/ChatGPT "I feel HEARD" + r/MyBoyfriendIsAI MIT writeup + r/CharacterAI academic analysis (arXiv:2507.15783).** The ethnographic ground truth.
13. **Cheng et al. — AnthroScore (EACL 2024)** + **HumT/DumT.** The automatic-metric substrate.
14. **DeepMind AnthroBench (arXiv:2502.07077)** + **Sturgeon HumanAgencyBench (arXiv:2509.08494).** The multi-dimensional benchmark substrate.
15. **Shanahan, McDonell & Reynolds — "Role play with LLMs" (Nature 2023).** The conceptual frame for talking about persona without importing mental-state claims.
16. **Abercrombie et al. — "Mirages" (EMNLP 2023).** The clean harms taxonomy.
17. **IDEO "Humanizing AI in Design"** + **frog "AI Playbook"** + **Atin "AI Persona Playbook."** The consultancy thought-leadership layer.
18. **OpenAI GPT-4o sycophancy postmortem** + **HN Sesame voice demo threads.** The contemporary natural-experiment record.
19. **LessWrong "Anthropomorphizing AI might be good, actually."** The counter-case that legitimizes humanization as a cognitive tool.
20. **The remaining A-, B-, C-, D-, E- entries as reference** when specific questions arise.

## File Index

- **[A-academic.md](./A-academic.md)** — 22 foundational papers across CASA / Media Equation, mind perception theory, measurement instruments (Godspeed, IDAQ, AISM), uncanny valley, Turing test, trust calibration, companionship / parasocial bonds, and critical / design-ethics framings. Heavy on Nass, Epley, Gray/Wegner, Bartneck, Jones & Bergen, De Freitas, Abercrombie, Shanahan, Shneiderman, Weizenbaum. Patterns: behavior > belief, two-factor structure recurs, style dominates Turing judgments, modality multiplies, critical literature maturing.
- **[B-industry.md](./B-industry.md)** — 23 essays / posts from NN/g (5), Microsoft HAX, Anthropic (4), Stanford HAI / Digital Economy Lab / FAccT / SCALE (4), UX Collective (3), Smashing Magazine (3), Dan Saffer, BotWash, Open Ethics. Maps the polarized safety/legibility vs. character/relationship split; hardens the shared vocabulary (humanization ≠ anthropomorphization, persona vectors, sycophancy, parasocial, uncanny valley of text, transparency moments).
- **[C-opensource.md](./C-opensource.md)** — 22 open-source tools / benchmarks / scales. Microsoft HAX Playbook + RAI Toolbox, Google PAIR, AnthroScore, HumT/DumT, AnthroBench, HumanAgencyBench, AgencyBench, Kreiman integrative Turing test, Microsoft Turing Experiments, Adversarial Turing Test, Jones & Bergen site, FastChat / Chatbot Arena, HELM, LaTeX Godspeed / RoSAS, Python UEQ-S, HRI Scale Database, awesome-hri-datasets, GAICo, adversarial humanization / detection benchmarks, open humanization engines. Identifies the two-era structure (classical HRI scales + LLM-era automatic metrics) and the multi-dimensional convergence.
- **[D-commercial.md](./D-commercial.md)** — 20+ commercial entities across three tiers: UX research platforms (UserTesting, Maze, Dovetail, Lookback, Great Question), design consultancies (IDEO, frog, Fjord / Accenture, Atin), and embodied / voice / text humanization vendors (Soul Machines, UneeQ, D-ID, Synthesia, HeyGen, Hume, ElevenLabs, Inworld, Sierra, Decagon, Replika / Character.AI, Undetectable AI, Humbot, StealthGPT). Flags the Soul Machines bankruptcy and ElevenLabs $11B valuation as structural market signals.
- **[E-practical.md](./E-practical.md)** — 21 practitioner / community posts across r/ChatGPT, r/Replika, r/artificial, r/CharacterAI, r/MyBoyfriendIsAI, Hacker News (Turing test, Lemoine, Sesame), OpenAI developer forum, dev.to, Medium (Park, Burkert), UX Studio (Pető), LessWrong, YouTube. Distills the patch-breakup phenomenon, the specific-callback = listening finding, the Jones & Bergen persona recipe as practical baseline, the duration dependency of humanness perception, and the metacognitive-UI humanization surface.

---

**Last synthesized:** April 2026.

**Confidence:** High — five angles agree on major findings (style dominates humanness, warmth has a reliability cost, anthropomorphism is multi-dimensional, patch-breakup is a real category of harm, detectors are the wrong primary objective). Disagreements (should-humanize-at-all, how-much-warmth) are named, mapped, and actionable.
