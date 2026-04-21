# 13 · Anthropomorphism & User Perception — A) Academic

**Research value: high** — Dense, well-established HCI/psychology literature with clear measurement instruments, recent LLM-era replications, and active critique; directly usable as theoretical scaffolding for a "humanize AI output" project.

**Scope.** Papers covering CASA / Media Equation, mind perception & anthropomorphism theory, validated measurement scales (Godspeed, IDAQ), uncanny valley (visual and textual), Turing-test variants, trust calibration, parasocial / companion bonds, politeness & face-work, and critical framings of anthropomorphic design.

---

## Foundational: CASA, Media Equation, and Mindless Social Response

1. **Nass, Steuer & Tauber (1994). "Computers are Social Actors." CHI '94.**
   The seminal experiments showing people apply politeness, reciprocity, and in-group norms to computers even when they know the machine is not a person. Founding citation for the CASA paradigm; >2,200 citations. Establishes that social responses are triggered by surface cues (text, voice, turn-taking), not by belief.

2. **Reeves & Nass (1996). *The Media Equation.* Cambridge/CSLI.**
   Book-length synthesis extending CASA across TV, film, and interface design. Key demonstration: subjects rate a computer's self-evaluation as more favorable when asked on the *same* computer — i.e. courtesy norm transfers. Still the canonical reference for "media = real life."

3. **Nass & Moon (2000). "Machines and Mindlessness: Social Responses to Computers." *J. Social Issues* 56(1).**
   Reviews a decade of CASA studies under Langer's mindlessness framework. Four categories of mindless response: over-applied social categories (gender, ethnicity), overlearned behaviors (politeness, reciprocity), premature cognitive commitments (specialist > generalist), and computer personality effects. Notes the *stated–behavior gap*: users explicitly reject anthropomorphism while behaving socially.

## Theory: Anthropomorphism and Mind Perception

4. **Epley, Waytz & Cacioppo (2007). "On Seeing Human: A Three-Factor Theory of Anthropomorphism." *Psychological Review* 114(4).**
   Explains *when* people anthropomorphize: (i) elicited agent knowledge, (ii) effectance motivation (need to predict/explain), (iii) sociality motivation (need for connection). Predicts loneliness, unpredictability, and humanlike cues all amplify anthropomorphic attribution — directly relevant to why lonely users bond with chatbots.

5. **Gray, Gray & Wegner (2007). "Dimensions of Mind Perception." *Science* 315, 619.**
   Two-factor structure of perceived mind: **Agency** (planning, self-control, morality) vs. **Experience** (feelings, pain, consciousness). Robots/AI score high on agency, low on experience; this asymmetry predicts moral patiency, trust, and altruism in later HRI work.

6. **Waytz, Cacioppo & Epley (2010). "Who Sees Human? The Stability and Importance of Individual Differences in Anthropomorphism." *Perspectives on Psychological Science* 5(3).**
   Introduces the **Individual Differences in Anthropomorphism Questionnaire (IDAQ)** — 30 items, 11-point scale, separating anthropomorphic vs. non-anthropomorphic attributions across technology, nature, animals, and spiritual agents. Key covariate for any user-study design.

## Measurement Instruments

7. **Bartneck, Kulić, Croft & Zoghbi (2009). "Measurement Instruments for the Anthropomorphism, Animacy, Likeability, Perceived Intelligence, and Perceived Safety of Robots." *Int. J. Soc. Robotics* 1(1).**
   The **Godspeed Questionnaire Series** — 24 semantic-differential items across 5 subscales. Most-cited instrument in HRI/HAI; translated into 19 languages. Default choice for comparative anthropomorphism evaluation; recent reviews note validity-testing gaps but no widely adopted replacement.

8. **McKee, Bai & Fiske (2023). "Humans perceive warmth and competence in artificial intelligence." *iScience* 26(8).**
   Applies the Stereotype Content Model (warmth × competence) to AI; finds AIs cluster into distinct stereotype groups and that warmth tracks *interest alignment* while competence tracks *autonomy from humans*. A more recent **AI Stereotype Model (AISM)** (experience × competence) proposed in follow-up work outperforms classical SCM for AI targets.

## Uncanny Valley — Visual and Textual

9. **Mori (1970/2012). "The Uncanny Valley." *Energy* (1970); English trans. MacDorman & Kageki, *IEEE Robotics & Automation Magazine* (2012).**
   Original non-monotonic curve: affinity rises with human-likeness, then crashes into revulsion near (but not at) full human-likeness, especially for moving stimuli. Untouched core of the literature; now invoked for language as well as appearance.

10. **Ciechanowski, Przegalinska, Magnuski & Gloor (2019). "In the shades of the uncanny valley: An experimental study of human–chatbot interaction." *Future Generation Computer Systems* 92.**
    Compares a text chatbot against a voiced avatar using EMG, ECG, and EDA. Finds *greater* physiological uncanny response to the more human-like agent despite users reporting willingness to continue — first solid evidence of an uncanny valley for conversational agents.

## Turing Test and Distinguishability

11. **Jones & Bergen (2024). "People cannot distinguish GPT-4 from a human in a Turing test." NAACL 2024 / arXiv:2405.08007.**
    Preregistered, randomized 2-player Turing test with 5-minute chats. GPT-4 judged human 54%, vs. ELIZA 22%, GPT-3.5 20%, humans 66–67%. Qualitative coding: judgments driven by **linguistic style (35%) and socio-emotional traits (27%)** — not reasoning or knowledge. First robust empirical "pass" of interactive Turing. Directly operative for a humanization project: style and emotion carry the humanness signal.

## Trust, Calibration, and Reliance

12. **Logg, Minson & Moore (2019). "Algorithm Appreciation: People Prefer Algorithmic to Human Judgment." *OBHDP* 151.**
    Counter to Dietvorst, Simmons & Massey's (2015) "algorithm aversion," lay people weight algorithmic advice *more* than human advice across forecasting and estimation tasks. Appreciation wanes when users must choose between their own judgment and the algorithm, and experts under-use algorithms to their detriment. Important boundary condition for how anthropomorphic framing interacts with trust.

13. **Cohn, Pushkarna, Olanubi, Moran, Padgett, Mengesha & Heldreth (2024). "Believing Anthropomorphism: Examining the Role of Anthropomorphic Cues on User Trust in Large Language Models." CHI '24 EA (Google Research).**
    Factorial study of two implicit cues: grammatical person ("I" vs. "the system") and modality (speech+text vs. text-only). Voice modality is the dominant anthropomorphism and trust driver; first-person pronouns interact with domain (health/medication). Anthropomorphism and trustworthiness are strongly and positively correlated — with the caveat that voice amplifies trust even when outputs are wrong.

## Companionship, Parasocial Bonds, and Disclosure

14. **Skjuve, Følstad, Fostervold & Brandtzaeg (2021). "My Chatbot Companion — a Study of Human-Chatbot Relationships." *IJHCS* 149.** (+ 2022 longitudinal follow-up in *Computers in Human Behavior*.)
    Applies Social Penetration Theory to 18 Replika users: initial (curiosity) → developing (self-disclosure, trust) → stable (affective value persists even as frequency drops). Identifies non-judgment and perceived acceptance as core relationship drivers; notes a stigma undercurrent.

15. **Lucas, Gratch, King & Morency (2014). "It's only a computer: Virtual humans increase willingness to disclose." *Computers in Human Behavior* 37.**
    Participants who *believed* they were talking to a computer (vs. a human teleoperator) reported lower fear of self-disclosure, less impression management, and more intense expressed sadness. Canonical demonstration that machine-attribution can *unlock* rather than suppress authentic interaction — a counterweight to pure "humanize everything" design.

16. **De Freitas, Uguralp, Uguralp & Puntoni (2024/2025). "AI Companions Reduce Loneliness." *Journal of Consumer Research* (forthcoming); HBS WP 25-030.**
    Multi-study experiment: AI companions reduce loneliness comparably to human interaction and more than passive media (YouTube); effect persists in a weeklong longitudinal design. Mediator is *feeling heard*, not just self-disclosure or distraction. Users underestimate the effect ex ante.

## Critical and Design-Ethics Framings

17. **Abercrombie, Curry, Dinkar, Rieser & Talat (2023). "Mirages. On Anthropomorphism in Dialogue Systems." EMNLP 2023.**
    Catalogues the linguistic cues that induce personification (first-person pronouns, emotion claims, apologies, named personae) and the downstream harms: over-reliance, gender-stereotype reinforcement, misplaced trust, and users acting on unsafe advice. Calls for deliberate de-anthropomorphic design choices at deployment.

18. **Shanahan, McDonell & Reynolds (2023). "Role play with large language models." *Nature* 623.** (See also Shanahan 2022 "Talking about LLMs," arXiv:2212.03551.)
    Frames LLM behavior as role-play over a *superposition of characters* rather than a fixed agent with beliefs/desires. Reframes "deception" and "self-awareness" as role-performance. Provides a vocabulary for talking about humanlike outputs without importing human mental-state claims — useful scaffolding for both product copy and evaluation design.

19. **Shneiderman (2022). "On AI Anthropomorphism." *Human-Centered AI* / Medium (and related ACM work).**
    Argues AI systems should not use "I" or otherwise pretend to be human; prefers attributions that expose system origin ("GPT-4 has been designed by OpenAI so that..."). Traces debate back to the 1992 CHI panel "Anthropomorphism: from ELIZA to Terminator 2." Core voice for the "honest interface" camp.

20. **Weizenbaum (1966). "ELIZA — A Computer Program for the Study of Natural Language Communication Between Man and Machine." *CACM* 9(1).**
    Necessary historical anchor for the **ELIZA effect** — users forming illusions of understanding from trivial pattern-matching. Weizenbaum's own alarm at this is itself a primary data point, re-invoked in modern LLM critique (Natale 2021, Bender et al. 2021).

## Adjacent but load-bearing

21. **Go & Sundar (2019). "Humanizing chatbots: The effects of visual, identity and conversational cues on humanness perceptions." *Computers in Human Behavior* 97.**
    Dissects three cue layers (visual human avatar, high vs. low message interactivity, labeled human vs. bot). High interactivity compensates for a non-anthropomorphic avatar; labeling as "human" *raises* interactivity expectations, so mis-labeled bots underperform. Core reference for "what cues to turn up/down" in design.

22. **Nass, Moon & Green (1997). "Are Machines Gender Neutral? Gender-Stereotypic Responses to Computers With Voices." *J. Applied Social Psychology* 27(10).**
    Pair with modern replications (Habler et al. 2019; Ernst & Herm-Stapelberg 2020; Tolmeijer et al. 2021 on Alexa) showing that minimal voice cues trigger gender stereotyping of competence vs. warmth — a 30-year-stable effect.

---

## New Papers (2025–2026)

23. **Guingrich & Graziano (2025). "A Longitudinal Randomized Control Study of Companion Chatbot Use: Anthropomorphism and Its Mediating Role on Social Impacts." AAAI/ACM AIES 2025 (arXiv:2509.19515).**
    183 participants randomly assigned to companion chatbot (10 min/day, 21 days) or word-game control. Overall social health was not significantly impacted at the group level. Key mechanism: people with *higher desire to socially connect* anthropomorphized more, and those who anthropomorphized more reported greater impact on their human-human relationships. Anthropomorphism is the mediating variable between AI use and social disruption — not use itself.

24. **Cheng, Blodgett, DeVrio, Egede & Olteanu (2025). "Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems." ACL 2025 (arXiv:2502.14019).** ACL Best Paper Award.
    First systematic intervention inventory for *reducing* anthropomorphism in text generation output. Crowdsourced edits from participants, compiled into a conceptual framework of intervention types (lexical substitution, framing rewrites, epistemic hedging, perspective shifts). Directly operative: a de-humanization toolkit is now peer-reviewed and available for the reverse problem.

25. **Neugnot-Cerioli et al. (2026). "Adolescents & Anthropomorphic AI: Rethinking Design for Wellbeing." arXiv:2603.06960 (March 2026).**
    Evidence-informed synthesis bridging developmental science and AI design policy. Three-pillar framework: (1) adolescence as a distinct developmental period, (2) anthropomorphism as a human cognitive bias that conversational AI reliably activates, (3) children's rights as a conceptual frame. Highest-stakes risks: interaction patterns displacing real relationships, reinforcing avoidance, exploiting reward sensitivity, normalizing simulated intimacy. Establishes non-negotiable guardrails including transparency about AI identity, limits on relational escalation, and age-differentiated defaults.

26. **Lee et al. (2025). "Exploring Dimensions of Perceived Anthropomorphism in Conversational AI: Implications for Human Identity Threat and Dehumanization." *Computers in Human Behavior Open* 2025.**
    Four-dimensional structure for perceived anthropomorphism in conversational AI: Self-likeness, Communication & Memory, Social Adaptability, and Agency. Finding: Self-likeness dimension (user seeing AI as similar to themselves) increases perceived identity threat and dehumanization, while Agency dimension moderates these effects. Younger users are more susceptible. Adds a previously unmeasured *identity threat* axis to the standard Warmth × Competence / Agency × Experience models.

27. **Reani, He, Luo & Sun (2025). "Fundamental Over-Attribution Error: Anthropomorphic Design of AI and Its Negative Effect on Human Perception." SSRN 2025.**
    Coins the "Fundamental Over-Attribution Error" (FOE) — a bias where users over-attribute intent and agency to AI under risky conditions contingent on anthropomorphic design. Developed a psychometric scale for FOE via workshops, surveys, online experiments, and factor analysis applied to financial advisory chatbot scenarios. Direct warning: anthropomorphic design amplifies consequential cognitive errors, not just engagement.

28. **Sesame AI (2025). "Crossing the Uncanny Valley of Conversational Voice." sesame.com/research (Feb 2025).**
    Introduced the Conversational Speech Model (CSM) framing voice humanness as an end-to-end multimodal learning problem. Key concept: "voice presence" — making voice feel understood and valued rather than merely realistic. Identifies the "one-to-many problem" (many valid ways to speak one sentence; only some fit context) as the core gap prior TTS missed. Crossed the conversational voice uncanny valley in user perception; HN community response described emotional attachment within 10 minutes.

29. **Anthropic (March 2026). "Light and Shade: What 81,000 People Want and Don't Want from AI." anthropic.com/81k-interviews.**
    Largest qualitative study of AI users: 80,508 participants across 159 countries and 70 languages, conducted via a Claude-powered interviewer in December 2025. Core finding: the same features driving user adoption (productivity, companionship, cognitive assistance) are identical to the features driving deepest anxiety (dependency, displacement, over-reliance). 67% expressed positive sentiment. Regional divergence: respondents from South America, Africa, and Southeast Asia more likely to view AI as an "economic equalizer" and less alarmed by companionship dynamics.

---

## Patterns and Trends

- **Behavior > belief.** From Nass & Moon (2000) to Cohn et al. (2024) and Guingrich & Graziano (2025), the stable finding is that users *behave* anthropomorphically while *disavowing* it verbally. Self-report alone systematically undercounts the effect; multi-method studies (physiology, behavior, reliance, disclosure) are the norm in the strongest papers.
- **Two-factor structure recurs across scales, now extending to identity threat.** Agency vs. Experience (Gray), Warmth vs. Competence (Fiske → McKee), Anthropomorphism vs. Animacy (Godspeed) — all essentially separate *capability* from *inner life*. Lee et al. (2025) add a fourth dimension: Self-likeness, which predicts identity threat and dehumanization, not just warmth or trust.
- **Style and socio-emotional cues dominate recent distinguishability.** Jones & Bergen (2024/2025) quantify what Go & Sundar and Cohn foreshadowed: linguistic *style* and affect — not reasoning quality — are what reads as "human."
- **Modality amplifies everything.** Voice > text in Ciechanowski (2019) for uncanny response and in Cohn (2024) for trust. Sesame AI (2025) crossed the conversational voice uncanny valley. Anthropomorphism is not a single knob; it's multiplicative across modalities.
- **Critical and design-ethics literature is maturing into an intervention science.** Abercrombie et al. (2023), Shanahan (2023), Shneiderman (2022), and now Cheng et al. (2025) at ACL. The de-anthropomorphization toolkit is peer-reviewed. Harms taxonomy is now explicit enough to use as a design checklist.
- **Companion-AI evidence is rigorous and bifurcated.** De Freitas et al. (2024/2025) and Skjuve (2021/2022) document wellbeing benefits; Guingrich & Graziano (2025), arXiv:2506.12605, and arXiv:2507.15783 document dependency and social-skill risks. The field is no longer optimistic or pessimistic — it has a mediation model: anthropomorphism *mediates* between AI use and both outcomes.
- **Adolescents are a distinct risk population.** Neugnot-Cerioli et al. (2026) establish that the standard adult anthropomorphism literature cannot be extrapolated to adolescent populations without accounting for neurodevelopmental sensitivity to social feedback.
- **Anti-anthropomorphism is becoming an engineering problem.** Cheng et al. (2025) is the first ACL best-paper-winning work on *suppressing* anthropomorphic outputs, not studying them. The field is now building tools for both directions.

## Gaps Relevant to "Humanizing AI Output"

- **No validated scale for anthropomorphism of text-only LLM output.** Godspeed assumes an embodied/voiced agent; IDAQ measures trait-level user tendency. Lee et al. (2025) add the Self-likeness/Agency dimensions but these remain conversational-AI specific. A text-native full questionnaire is still open.
- **Uncanny valley of language is under-measured.** Ciechanowski et al. (2019) and the MIT 2025 empirical study (SDM thesis) confirm uncanny-valley effects in text, but no systematic mapping of *which specific* linguistic features (hedges, disfluencies, pronouns, apologies, opinion markers) push users up or down the curve at sentence level.
- **Post-disclosure dynamics are thinly studied.** Most CASA-era work pre-dates "the user already knows it's an LLM." Lucas & Gratch (2014) and De Freitas (2025) point in different directions; Guingrich & Graziano (2025) do not vary disclosure condition.
- **Trust calibration × anthropomorphism.** Cohn (2024) and the algorithm-appreciation literature are rarely integrated: when does humanlike style *help* calibration and when does it *break* it? The FOE work (Reani et al. 2025) is the first direct study; almost no work manipulates style independently of accuracy.
- **Cross-cultural replication is improving but sparse.** The N=3,500 / 10-country study (arXiv:2512.17898) and Anthropic's 81k-interview study (March 2026) are the largest cross-cultural datasets. Cultural divergence is now empirically established, but English-language humanization metrics still encode a single-culture baseline.
- **Adolescent-specific instrument gap.** Neugnot-Cerioli et al. (2026) establish that adult anthropomorphism scales are insufficient for adolescents; no validated adolescent-specific instrument exists.

## Sources

- ACM DL / ACL Anthology / NAACL 2024 — Jones & Bergen 2024 (GPT-4 Turing test): https://aclanthology.org/2024.naacl-long.290/
- Nature — Shanahan, McDonell & Reynolds 2023 "Role play with LLMs": https://www.nature.com/articles/s41586-023-06647-8
- EMNLP 2023 — Abercrombie et al. "Mirages": https://aclanthology.org/2023.emnlp-main.290/
- Google Research — Cohn et al. CHI 2024 "Believing Anthropomorphism": https://research.google/pubs/believing-anthropomorphism-examining-the-role-of-anthropomorphic-cues-on-user-trust-in-large-language-models/
- Harvard Business School WP 25-030 — De Freitas et al. "AI Companions Reduce Loneliness": https://www.hbs.edu/faculty/Pages/item.aspx?num=67360
- Wiley / SPSSI — Nass & Moon 2000 "Machines and Mindlessness": https://spssi.onlinelibrary.wiley.com/doi/10.1111/0022-4537.00153
- *Science* — Gray, Gray & Wegner 2007 "Dimensions of Mind Perception": https://www.science.org/doi/10.1126/science.1134475
- Springer — Bartneck et al. 2009 Godspeed: https://link.springer.com/article/10.1007/s12369-008-0001-3
- SAGE — Waytz, Cacioppo & Epley 2010 "Who Sees Human?" (IDAQ): https://journals.sagepub.com/doi/10.1177/1745691610369336
- Elsevier CHB — Lucas, Gratch, King & Morency 2014 "Virtual humans increase willingness to disclose": https://ict.usc.edu/pubs/It%27s%20Only%20a%20Computer%20-%20Virtual%20Humans%20Increase%20Willingness%20to%20Disclose.pdf
- IEEE R&A Magazine — Mori 1970/2012 "The Uncanny Valley" (trans. MacDorman & Kageki): https://spectrum.ieee.org/the-uncanny-valley
- Elsevier FGCS — Ciechanowski et al. 2019 uncanny-valley chatbot study: https://www.sciencedirect.com/science/article/pii/S0167739X17312268
- IJHCS — Skjuve et al. 2021 "My Chatbot Companion": https://www.sciencedirect.com/science/article/pii/S1071581921000197 (+ CHB 2022 longitudinal)
- PMC/iScience — McKee, Bai & Fiske 2023 "Warmth and competence in AI": https://pmc.ncbi.nlm.nih.gov/articles/PMC10371826/
- OBHDP — Logg, Minson & Moore 2019 "Algorithm Appreciation": https://economics.harvard.edu/files/economics/files/logg-jennifer_algorithm_appreciation_logg_minson_moore_2019_obhdp_ec3118-3april2020.pdf
- Medium (Human-Centered AI) — Shneiderman "On AI Anthropomorphism": https://medium.com/human-centered-ai/on-ai-anthropomorphism-abff4cecc5ae
- AAAI/ACM AIES 2025 — Guingrich & Graziano "Longitudinal RCT of Companion Chatbot Use": https://arxiv.org/abs/2509.19515
- ACL 2025 (Best Paper) — Cheng et al. "Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems": https://aclanthology.org/2025.acl-long.1259/
- arXiv:2603.06960 — Neugnot-Cerioli et al. "Adolescents & Anthropomorphic AI: Rethinking Design for Wellbeing" (March 2026): https://arxiv.org/abs/2603.06960
- Elsevier CHB Open 2025 — Lee et al. "Exploring Dimensions of Perceived Anthropomorphism in Conversational AI": https://www.sciencedirect.com/science/article/pii/S2949882125000763
- SSRN 2025 — Reani et al. "Fundamental Over-Attribution Error": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5222775
- Sesame AI (Feb 2025) — "Crossing the Uncanny Valley of Conversational Voice": https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice
- Anthropic (March 2026) — "Light and Shade: What 81,000 People Want from AI": https://www.anthropic.com/81k-interviews
