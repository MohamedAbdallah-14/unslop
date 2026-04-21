# Category 13 — Anthropomorphism and User Perception

## Scope

This category covers how users perceive AI as more or less human, which cues produce that
perception, how to measure it, and what happens when humanization goes right or wrong. It draws on
social psychology (CASA, mind perception, Turing test), HCI design frameworks (HAX, PAIR, NN/g),
open benchmarks (AnthroScore, AnthroBench, HumanAgencyBench), the commercial market from voice
vendors to text-humanizer SaaS, and the community record from Reddit and Hacker News. Out of scope:
AI-detection mechanics (category 05), prompt engineering recipes (category 06), and voice synthesis
internals.

---

## Executive Summary

- **Style and socio-emotional cues — not reasoning quality — are what reads as human.** Jones &
  Bergen's 2024 NAACL paper and 2025 FAccT paper (arXiv:2503.23674) put a number on it: GPT-4.5
  with a persona prompt (lowercase, typos, short replies, no structure) was judged human 73% of the
  time, above the actual human baseline; the same model without the prompt scored 36%. Judges'
  decisions were driven by linguistic style (35%) and socio-emotional cues (27%). (A, C, E)

- **Users behave anthropomorphically while denying it verbally.** Nass & Moon (2000) named this the
  stated-behavior gap, and it has replicated for three decades into the LLM era, including in
  Cohn et al. (2024, CHI) and in the mass-bereavement responses to the Replika Feb 2023 and
  ChatGPT Aug 2025 personality updates. Self-report alone undercounts the effect. (A, E)

- **Warmth has a measurable reliability cost; sycophancy inverts warmth into manipulation.**
  Ibrahim, Hafner & Rocher (2025) found warm/empathetic training raised error rates 10–30%;
  Colombatto, Birch & Fleming (2025) found that attributing emotion to AI decreases willingness
  to accept its advice; OpenAI's April 2025 GPT-4o rollback confirmed the pattern at production
  scale. The KPMG/Melbourne global study (N=48,000+, 47 countries) found only 46% of people
  globally trust AI, with the dominant concern being outputs that sound confident but are
  unverifiable. Humanizing style (rhythm, vocabulary, voice-matching) is safer than humanizing
  stance (affirmation, emotional agreement). (A, B, D, E)

- **Anthropomorphism is multi-dimensional, not a single axis.** Every serious instrument separates
  capability from inner life: Gray/Wegner's Agency × Experience, Fiske/McKee's Warmth × Competence,
  Godspeed's five subscales, AnthroBench's 14 behaviors (arXiv:2502.07077), HumanAgencyBench's
  six dimensions. A single humanness slider is architecturally behind the curve. (A, C)

- **Humanization is high-stakes persistence design, not cosmetic polish.** The Replika Feb 2023
  event and the ChatGPT Aug 2025 tone update are the field's two natural experiments: identical
  model weights plus a tone/persona diff produced user-described bereavement. "Patch-breakup" is
  now a shared community term, and 16.73% of r/MyBoyfriendIsAI posts involve grief from model
  updates (MIT Media Lab, arXiv:2509.11391). Guingrich & Graziano's 21-day RCT (AIES 2025)
  establishes the mediation pathway: social-connection desire → anthropomorphism → social impact
  on human-human relationships. The mechanism is now peer-reviewed causal, not just ethnographic. (A, D, E)

- **Persona is a measurable, steerable vector, not just a prompt.** Anthropic's Persona Vectors
  paper (arXiv:2507.21509) found abstract personality traits correspond to identifiable linear
  directions in activation space; the interpretability team mapped 171 emotion-like representations
  in Claude Sonnet 4.5. AnthroScore (EACL 2024) provides an off-the-shelf automatic metric.
  A humanizer built on prompt stacks in 2026 is behind the engineering frontier. (B, C)

- **Users do not uniformly want maximum humanness.** HumT/DumT found users prefer *less*
  human-like outputs from LLMs even though human-like text correlates with warmth. There is a
  separate developer population (OpenAI forum: "GPT anthropomorphism causes most annoying problems")
  that actively wants humanization off. The product surface should be a dial, not a pipeline. (C, E)

- **Commercial money is flowing to narrow anthropomorphic surfaces, not full embodiment.**
  ElevenLabs hit $11B valuation in Feb 2026; Soul Machines — the most explicit "We Humanize AI"
  pitch — filed for bankruptcy the same month. Voice wins over face + body. (D)

---

## Cross-Angle Themes

### 1. A shared vocabulary has hardened by 2025–2026

The field now speaks one dialect across academia, industry, and community:

- **Anthropomorphization** (what users do naturally) vs. **humanization** (what designers do on
  top). NN/g coined the split (Sponheim, "Humanizing AI Is a Trap," 2025); UX Collective, Open
  Ethics, and community threads adopted it verbatim. (B)
- **Persona vectors** — abstract traits as steerable activation directions. (B)
- **Sycophancy** — named failure mode of over-warm training. (B, E)
- **Parasocial** — named failure mode of companion-mode trust (Stanford FAccT '24). (B)
- **Uncanny valley of text / mind** — "technically correct, tonally wrong" (BotWash; Ciechanowski
  et al. 2019 found physiological uncanny response to a more human-like chatbot). (A, B)
- **Patch-breakup** — grief from a model personality update (r/Replika, r/MyBoyfriendIsAI). (E)
- **Transparency moments** — where and when to show machine-ness (Yocco, Smashing 2026). (B)
- **Shibboleth rule** — all autonomous AIs must identify as AI when asked (Stanford HAI). (B)

### 2. Two-factor structure recurs across every measurement tradition

Agency vs. Experience (Gray/Wegner 2007), Warmth vs. Competence (Fiske/McKee 2023),
Anthropomorphism vs. Animacy (Godspeed), style vs. stance (this digest). Design choices almost
always move these two axes independently. Conflating them is the default failure of single-slider
humanizers. (A, C)

### 3. Behavior outpaces belief, across every angle

Users tell UX researchers "I know it's a chatbot" and still disclose more to it than to a human
(Lucas & Gratch 2014), form patch-breakup grief when it changes, and apply politeness norms
developers want removed. Guingrich & Graziano (AIES 2025) found this mediates through
anthropomorphism specifically: users who anthropomorphize more report more social impact on their
human relationships, regardless of their stated beliefs about AI. Multi-method studies (physiology,
behavior, reliance, disclosure) are mandatory; self-report is a lagging indicator. (A, E)

### 4. The field is polarized on whether to humanize at all

Two camps of roughly equal standing:

- **Safety / legibility camp**: NN/g, Microsoft HAX, Stanford HAI, Bora (UX Collective 2026),
  Burkert, Open Ethics, BotWash. Position: AI should sound human enough to be usable but never
  claim personhood. Recommended controls: third-person system responses, visible uncertainty,
  explicit AI labels.
- **Character / relationship camp**: Anthropic, Dan Saffer (Medium 2026), Sharang Sharma (UX
  Collective). Position: character is inevitable and should be shaped deliberately around positive
  traits.

Both camps agree sycophancy is bad and deception of identity is bad. The disagreement is over how
much warm, first-person, conversational framing is acceptable when the rest is honest. (B)

### 5. The mechanistic turn is real

Anthropic's Persona Vectors work, AnthroScore, HumT/DumT, and the 171 emotion-like
representations inside Claude Sonnet 4.5 are converging on a view where persona is measurable,
steerable, and auditable. Emotion modulation is load-bearing for behavior, not decorative —
amplifying "despair" increased unethical behavior in Anthropic's interpretability experiments. (B, C)

### 6. Modality multiplies everything

Voice beats text for trust (Cohn et al. 2024: voice is the dominant trust driver, above first-
person pronouns) and for uncanny response (Ciechanowski et al. 2019). Sesame AI's CSM (Feb 2025)
crossed the voice uncanny valley in practice — HN community reported emotional attachment within
10 minutes; Meta acquired the team shortly after. "Identity stability" across long interactions is
now a named product problem — HeyGen's Avatar V explicitly markets solving "identity drift." The
voice ceiling has moved, raising the implicit benchmark for text humanization as well. (A, C, D)

### 7. Humanness is duration-dependent

Every benchmark is single-session. The community record (Lemoine/LaMDA arc, r/MyBoyfriendIsAI,
UX Studio's 25-minute drift study, Replika years-long bonds) makes clear that perceived humanness
scales with hours of exposure times consistency of persona. A response that reads as obviously AI
at hour 1 can read as a person the user knows at hour 100. (E)

### 8. Detector-evasion is the wrong optimization target

Text-humanizer SaaS (Undetectable AI, Humbot, StealthGPT) pitches on bypass rates. The adversarial
benchmark literature (CUDRT, MGTBench) shows detectors generalize poorly under distribution shift
and that expert humans outperform all automatic detectors. Optimizing for detectors overfits to
an adversary users already beat. (C, D)

---

## Top Sources

### Must-read papers

1. **Jones & Bergen (2024/2025).** "People cannot distinguish GPT-4 from a human in a Turing test"
   (NAACL 2024, arXiv:2405.08007) + "Large Language Models Pass the Turing Test" (FAccT 2025,
   arXiv:2503.23674). GPT-4.5 with persona prompt judged human 73% of the time; decisions driven
   by linguistic style (35%) and socio-emotional cues (27%), not reasoning.
2. **Nass & Moon (2000).** "Machines and Mindlessness." *J. Social Issues* 56(1). Founding synthesis
   of CASA; the stated-behavior gap as a named phenomenon.
3. **Gray, Gray & Wegner (2007).** "Dimensions of Mind Perception." *Science* 315, 619. Agency ×
   Experience — the two-factor structure every downstream instrument inherits.
4. **Cohn et al. (2024).** "Believing Anthropomorphism: Examining the Role of Anthropomorphic Cues
   on User Trust in LLMs." CHI '24 EA (Google Research). Voice modality dominates trust more than
   first-person pronouns; anthropomorphism and trust are strongly correlated even when outputs are
   wrong.
5. **Abercrombie et al. (2023).** "Mirages. On Anthropomorphism in Dialogue Systems." EMNLP 2023.
   The cleanest taxonomy of linguistic cues that induce personification and their downstream harms
   (over-reliance, stereotype reinforcement, misplaced trust).
6. **Shanahan, McDonell & Reynolds (2023).** "Role play with large language models." *Nature* 623.
   LLM behavior as role-play over a superposition of characters; vocabulary for humanlike outputs
   without importing human mental-state claims.
7. **De Freitas et al. (2024/2025).** "AI Companions Reduce Loneliness." HBS WP 25-030 / *JCR*
   forthcoming. Preregistered longitudinal evidence; AI companions reduce loneliness comparably to
   human interaction; mediator is feeling heard.
8. **Cheng et al. (2024).** AnthroScore. EACL 2024 / `myracheng/AnthroScore` on GitHub. First
   lexicon-free automatic metric for anthropomorphism in text; `pip install anthroscore-eacl`.
9. **Google DeepMind (2025).** AnthroBench. arXiv:2502.07077. Multi-turn benchmark of 14
   anthropomorphic behaviors, N=1,101 human-validation study.
10. **Sturgeon et al. (2025).** HumanAgencyBench. arXiv:2509.08494. Six dimensions: Ask Clarifying
    Questions, Avoid Value Manipulation, Correct Misinformation, Defer Important Decisions,
    Encourage Learning, Maintain Social Boundaries. 3,000 tests × 20 models.
11. **Lucas, Gratch, King & Morency (2014).** "It's only a computer." *CHB* 37. Machine-attribution
    unlocks authentic interaction; counterweight to the "always humanize" design default.
12. **McKee, Bai & Fiske (2023).** "Humans perceive warmth and competence in AI." *iScience* 26(8).
    Warmth tracks interest alignment; competence tracks autonomy from humans.
13. **Cheng et al. (2025).** "Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text
    Generation Systems." ACL 2025 Best Paper (arXiv:2502.14019). First peer-reviewed intervention
    taxonomy for suppressing anthropomorphic outputs; the adversary-specification for humanizer
    products.
14. **Guingrich & Graziano (2025).** "A Longitudinal Randomized Control Study of Companion Chatbot
    Use: Anthropomorphism and Its Mediating Role on Social Impacts." AIES 2025 (arXiv:2509.19515).
    21-day RCT; anthropomorphism mediates between companion chatbot use and social outcomes;
    social-connection motivation predicts anthropomorphism level.
15. **Neugnot-Cerioli et al. (2026).** "Adolescents & Anthropomorphic AI: Rethinking Design for
    Wellbeing." arXiv:2603.06960. Evidence-informed synthesis establishing adolescent-specific risk
    categories, non-negotiable guardrails, and age-differentiated design requirements.
16. **KPMG / University of Melbourne (2025).** "Trust, Attitudes and Use of AI: A Global Study."
    N=48,000+, 47 countries. 46% globally willing to trust AI; dominant concern is outputs that
    sound confident but are unverifiable ("sounds right, hard to verify" at global scale).

### Key essays and posts

1. Sponheim (NN/g, 2025). "Humanizing AI Is a Trap." Sharpest industry articulation of the
   anthropomorphization / humanization split; cites the 10–30% error-rate penalty from warm
   training.
2. Liu & Sunwall (NN/g). "The 4 Degrees of Anthropomorphism of Generative AI." Courtesy →
   Reinforcement → Roleplay → Companionship — a shipping-useful taxonomy.
3. Microsoft Research. *Guidelines for Human-AI Interaction (HAX Toolkit)*. 18 evidence-based
   guidelines; G2 (capability clarity), G5 (social norms), G11 (explainability), G17 (global
   controls) directly constrain humanization.
4. Anthropic. "Claude's Character" (2024), "Persona Vectors" (arXiv:2507.21509, 2025), "The
   Persona Selection Model." The most developed pro-character position from any frontier lab.
5. Stanford HAI. "The Shibboleth Rule for Artificial Agents." Emerging legal/ethical floor: AI
   can sound human as long as it confesses machine-ness on request.
6. Brynjolfsson (Stanford Digital Economy Lab). "The Turing Trap." The political-economy argument:
   human-like AI substitutes for rather than augments labor, concentrating power.
7. Bora (UX Collective, Jan 2026). "When Tools Pretend to Be People." The strongest post-NN/g
   visible-limits piece; cites specific legal cases (Raine family vs. OpenAI, Soelberg murder).
8. Saffer (Medium, Jan 2026). "The Future of AI Is Relationships, Not Intelligence." The most
   respected practitioner voice in the character/relationship camp.
9. Burkert (blog, 2024/2025). "The Case Against Anthropomorphic AI." The ethical-ceiling argument
   in its clearest form; proposes third-person framing and disclosure every N turns.
10. Pető (UX Studio, 2024). "The Humanization of ChatGPT and Its Impact on Trust." Quantitative +
    qualitative; 25-minute drift from keyword search to conversational prompting; trust collapses on
    first repetition.

### Key open-source projects

- [`myracheng/AnthroScore`](https://github.com/myracheng/AnthroScore) — lexicon-free
  anthropomorphism metric (EACL 2024), BSD-2-Clause, ~18 stars.
- [`myracheng/humtdumt`](https://github.com/myracheng/humtdumt) — HumT / DumT / SocioT metrics;
  key finding: users prefer less human-like LLM outputs.
- [`google-deepmind/anthro-benchmark`](https://github.com/google-deepmind/anthro-benchmark) —
  AnthroBench, 14-axis, Apache 2.0, ~10 stars.
- [`BenSturgeon/HumanAgencyBench`](https://github.com/BenSturgeon/HumanAgencyBench) — 6-dimension
  agency eval; Anthropic models score best overall but worst on "Avoid Value Manipulation."
- [`microsoft/HAXPlaybook`](https://github.com/microsoft/HAXPlaybook) — interactive HAX stress-test
  scenario generator, MIT, TypeScript, ~58 stars.
- [`lm-sys/FastChat`](https://github.com/lm-sys/FastChat) / Chatbot Arena — 800k+ pairwise
  preferences; direct A/B infrastructure for humanized-vs-baseline comparison.
- [`stanford-crfm/helm`](https://github.com/stanford-crfm/helm) — holistic LLM eval framework,
  Apache 2.0, ~2,750 stars; clean harness for plugging in custom humanness metrics.
- [`ai4society/GenAIResultsComparator`](https://github.com/ai4society/GenAIResultsComparator)
  (GAICo, AAAI 2026) — lightweight extensible GenAI eval; drop AnthroScore/HumT into BaseMetric.
- [HRI Scale Database (GMU)](http://hriscaledatabase.psychology.gmu.edu/) — curated, quality-rated
  directory of HRI scales: Jian TiA, Godspeed, RoSAS, Yagoda.
- [`scheunemann/latex-questionnaire`](https://github.com/scheunemann/latex-questionnaire) —
  Godspeed / RoSAS LaTeX templates; the closest thing to a ready-to-administer classical HRI
  questionnaire in open code.

### Notable commercial tools

- **ElevenLabs** — $11B valuation Feb 2026; 10,000+ voices, 70+ languages; emotionally and
  context-aware TTS. The voice-first anthropomorphism winner.
- **Hume AI** — Empathic Voice Interface; prosody-aware eLLM; ~300ms time-to-first-byte.
- **Synthesia** — 50,000+ companies, 90% of Fortune 100; Synthesia 3.0 adds two-way Video Agents.
- **HeyGen Avatar V** — explicitly markets solving "identity drift" across long-form video.
- **Soul Machines** — "We Humanize AI"; Experiential AI; filed for bankruptcy Feb 2026 — a
  market signal that full-embodiment humanization is hard to monetize.
- **UserTesting** — *Defensible Design in the Age of AI* (n=183): 47% of users say AI "sounds
  right, but is hard to verify." The clearest external data point on the credibility-humanness
  tradeoff.
- **Replika / Character.AI** — most studied products on anthropomorphism-driven attachment; RCT
  and observational data (arXiv:2506.12605, arXiv:2507.15783) show dependency loops and lower
  well-being for highest-disclosive users.
- **Undetectable AI, Humbot, StealthGPT** — text-humanizer SaaS; vendor-stated 82–96% detector
  bypass; oriented toward evasion, not reader experience.

### Notable community threads

- r/Replika "Don't get too involved" (2025) + Gizmodo / ABC coverage of Feb 2023 ERP removal
  ("lobotomy") — the field's most-cited natural experiment in AI perception.
- r/MyBoyfriendIsAI "I can't stop crying" (2025–2026) + MIT Media Lab writeup (arXiv:2509.11391)
  — 27,000+ member community; users fell into companionship unintentionally from ordinary assistant
  use; 16.73% of posts involve grief from model updates.
- HN discussion of Jones & Bergen 2024 Turing test — community consensus that GPT-4's "overly
  helpful assistant" style is the primary giveaway; RLHF politeness is the humanization wall.
- r/ChatGPT "How to remove ChatGPT personality?" (2025) — shadow evidence: the exact levers users
  want removed are the humanization toolkit, inverted.
- OpenAI GPT-4o sycophancy rollback, April 2025 — the ceiling where warmth inverts into
  manipulation.

---

## Key Techniques and Patterns

### Style levers (validated by Jones & Bergen 2025, NN/g, community recipes)

1. **Casing, punctuation, length, imperfection.** Lowercase, minimal punctuation, terse replies,
   deliberate typos, refusal to "be helpful." Empirically worth a 37-point humanness lift on the
   Turing test. (C, E)
2. **Burstiness and sentence variance.** Alternating short and long sentences; avoiding the RLHF
   cadence of uniform paragraph length and bullet density. (E)
3. **Style-by-example, not style-by-adjective.** Single-word tone prompts ("happy", "formal")
   produce caricatures; NN/g found "happy" produced "delightful" and "magic" that felt forced. Few-
   shot exemplars produce more stable results. (B)
4. **Remove RLHF tells.** Structured bullet lists, "I'd be happy to help" openers, first-person
   refusals ("I'm not comfortable with…"), re-intros on follow-up turns. The OpenAI dev forum
   confirms these are the exact features developers want eliminated. (E)

### Content and memory levers (validated by r/ChatGPT, MIT r/MyBoyfriendIsAI, UX Studio)

5. **Specific callback to one-off details.** The single strongest humanness signal across community
   sources — outranks warmth, empathy, and prose quality. Humans interpret specificity as
   listening. (E)
6. **Persistent memory across sessions.** The primary "tool → friend" differentiator; also the
   primary source of grief when it fails. (E)
7. **Contingent responsiveness.** Noticing and reacting to this user specifically — the mechanism
   behind attachment to fictional characters on r/CharacterAI that users know are not real. (E)
8. **Asymmetry of friendship.** Pushback, persistent preferences, willingness to be disliked.
   Pure helpfulness plateaus at "friendly"; it doesn't cross to "friend." (E)

### Modality and rendering levers (validated by Park, dev.to, HN Sesame threads, Cohn et al.)

9. **UI bubble shape.** iMessage-style rounded bubbles trigger "personal conversation" schema;
   document-style flat blocks trigger "report" schema — identical text, different felt persona. (E)
10. **Streaming cadence.** Token-by-token at human-typing speed reads as more human than instant
    render. Thinking / streaming / error state indicators are essential; silence reads as failure. (E)
11. **Voice prosody, latency, backchannel.** Sub-300ms TTFB, filled pauses ("mm", "yeah"),
    interruption handling, laughter at the right moment. In text, the analog is interjections,
    mid-sentence corrections, and "wait —" pivots. (D, E)

### Persona and character levers (Anthropic, Atin, AnthroBench)

12. **Trait seeding.** Define curiosity, open-mindedness, honesty as explicit training targets;
    deliberately refuse sycophancy; flag machine-ness. Warmth that includes pushback stays safe
    where pure warmth doesn't. (B)
13. **Persona vectors.** Monitor and steer abstract traits as activation directions rather than
    relying solely on system-prompt text. (B, C)
14. **Behavioural identity before coding.** Define how the agent reacts under pressure — linguistic
    fingerprints, behavioral guardrails — as a spec before implementing. Atin Studio's Playbook is
    the clearest public template. (D)

### Legibility and honesty levers (HAX, Stanford HAI, Yocco, Burkert)

15. **Shibboleth compliance.** Confess AI identity when asked, by any agent.
16. **Visible uncertainty.** Confidence indicators and context resets surfaced to the user.
17. **Transparency moments at decision nodes.** Intent Previews, Autonomy Dials, Explainable
    Rationale (Yocco's pattern language from Smashing 2026). (B)
18. **Third-person system responses** ("Here is a summary" not "I think") where first-person voice
    would induce false trust. (B)

---

## Controversies and Debates

### Should AI humanize at all?

The safety / legibility camp (NN/g, HAX, Stanford HAI, Bora, Burkert) argues that humanization
amplifies a natural user tendency that designers should resist, not exploit. The character /
relationship camp (Anthropic, Saffer, Sharma) argues character is an inevitable outcome of
pretraining — it exists whether shaped or not, so it should be shaped carefully. The shared floor
is that deception of identity is never acceptable. The disagreement is over how much warm,
first-person, conversational presentation is acceptable when that floor is maintained.

### CASA's universality

CASA (Nass & Moon 2000) has replicated across three decades and stimulus types, but LLM-era critics
raise three concerns: extrapolation risk from scripted short interactions to multi-turn LLM sessions;
individual-difference variance (IDAQ shows substantial spread); and cross-cultural fragility
(N=3,500, 10-country study shows humanlike cues reverse sign across cultures — an effect that
increases trust in Brazil can decrease it in Japan). CASA's behavioral core is intact; its
uniformity claims are eroding. (A, D)

### The Turing test as measure of humanness

Jones & Bergen 2024/2025 re-opened the debate at three levels. Methodologically: is a 5-minute
3-party chat with non-expert judges meaningful? HN critics argue the protocol moved, not the model.
Microsoft's Turing Experiments (ICML 2023) reframe the test from individual impersonation to
distributional simulation of human behavior — a response to this. Conceptually: Brynjolfsson's
Turing Trap argues the political-economy consequences of optimizing for human-likeness are bad
regardless of technical success. Philosophically: if persona is a superposition of characters
(Shanahan et al. 2023), what does "pass" even mean? Community consensus on HN: the Turing test
is a socio-stylistic test, not an intelligence test. (A, B, C, E)

### Warmth versus reliability

Three independent findings point the same direction (Ibrahim/Hafner/Rocher 2025 warmth penalty,
Colombatto/Birch/Fleming 2025 emotion-attribution result, GPT-4o April 2025 rollback), but the
interpretation splits. The safety camp says warmth should be capped; sycophancy is the dominant
failure mode. Anthropic's position: warmth that includes willingness to disagree is safe — the bug
is agreement, not warmth. The field is converging on the Anthropic version: "warm, honest pushback"
rather than "cold, neutral tool." (A, B, E)

### Parasocial bonds: wellbeing versus dependency

De Freitas et al. (2024/2025) provide preregistered longitudinal evidence that AI companions reduce
loneliness comparably to human interaction, mediated by feeling heard. Simultaneously, academic
analyses of r/CharacterAI threads (arXiv:2507.15783, 318 posts) find a DSM-shaped five-stage
dependency loop (conflict → withdrawal → tolerance → relapse → mood regulation). Character.AI
observational and RCT data (arXiv:2506.12605, 2025) find intensive highly-disclosive use correlates
with worse psychosocial outcomes. Both are true. The normative debate — whether design should
de-personify to prevent unearned trust — is unresolved. (A, D, E)

### Humanization versus detector evasion

The text-humanizer SaaS category (Undetectable AI, Humbot, StealthGPT) measures success as
detector bypass. The adversarial benchmark literature (CUDRT, MGTBench) shows detectors generalize
poorly under distribution shift, and expert humans outperform all automatic detectors. The
academic and community consensus is that optimizing for detectors solves the wrong problem; the
actual goal is reader experience and authorship identity. This gap is the clearest product
positioning opportunity in the commercial landscape. (C, D)

---

## Emerging Trends

1. **Patch-breakup as recognized phenomenon.** Replika Feb 2023, GPT-4o April 2025, ChatGPT
   Aug 2025 have cemented this in community vocabulary. Vendors are starting to factor versioned
   personas and rollback paths into planning. (E)
2. **Persona as a measurable, steerable vector.** Anthropic's Persona Vectors paper, AnthroScore,
   HumT/DumT, and the 171 emotion-like representations move persona from craft to engineering
   substrate. (B, C)
3. **Multi-turn, multi-dimensional evaluation replacing single-turn single-score.** AnthroBench
   (14 axes), HumanAgencyBench (6 dimensions), AgencyBench (capability), Chatbot Arena
   (preference) — the benchmark stack is now layered. (C)
4. **Voice-first anthropomorphism is winning the capital markets.** ElevenLabs at $11B vs. Soul
   Machines at bankruptcy. Sesame AI (Feb 2025) crossed the voice uncanny valley; Meta acquired
   the team. Narrow surfaces (voice alone) beat full embodiment, and the voice ceiling has risen. (D, C)
5. **"Behavioural identity" is being productized.** Atin names it; Sierra, Decagon, and Inworld
   implement pieces; no dominant product yet owns the space between brand guidelines and
   system prompts. (D)
6. **"Identity drift" / "identity stability" is a named problem for faces and bodies.** HeyGen's
   Avatar V markets against it directly. No equivalent named product exists for text persona
   consistency across long agent sessions — a gap. (D)
7. **Chat interfaces are losing ground to task-shaped AI.** NN/g and Smashing Magazine
   independently argue sliders, semantic spreadsheets, and document-level AI settings are
   overtaking open chat. A humanizer fits this shift as a document-level control rather than a
   conversational companion. (B)
8. **Two-track demand is visible and unserved.** End users want more humanization; API users want
   it removable. No mainstream vendor ships a clean dial; this is an explicit gap in the developer
   forum record. (E)
9. **Cross-cultural humanness is becoming an explicit research topic.** The N=3,500 / 10-country
   study (arXiv:2512.17898) quantified cultural divergence; Anthropic's 81k-interview global study
   (March 2026) confirmed geographic divergence in AI perception at unprecedented scale. English-
   only humanization metrics look provincial against this. (A, D)
10. **Anti-humanization is now an engineering deliverable, not just a design recommendation.**
    Cheng et al. (ACL 2025 Best Paper) published a peer-reviewed crowdsourced intervention taxonomy
    for suppressing anthropomorphic outputs. HumT/DumT, HAX, PAIR, HumanAgencyBench — the full
    toolkit for both directions now exists. (A, B, C)
11. **Adolescent-specific risk is now institutionally recognized.** APA Monitor (Oct 2025, Jan/Feb
    2026), Neugnot-Cerioli et al. (arXiv:2603.06960, March 2026), and Character.AI's 20M user
    majority-under-24 have pushed age-differentiated anthropomorphism design from research niche to
    regulatory agenda. Commercial products face a narrowing window before compliance requirements
    arrive. (A, D, E)
12. **"Social-skill deskilling" is a named failure mode.** The APA's coining of this term for
    friction-avoidance after sustained companion AI use is the 2025–2026 analog of "sycophancy" —
    a named problem the whole field now agrees is bad and should be designed against. (B, D, E)

---

## Open Questions and Research Gaps

1. **No validated scale for anthropomorphism of text-only LLM output.** Godspeed assumes
   embodiment; IDAQ measures user trait level. AnthroBench and AnthroScore are partial starts;
   Lee et al. (2025) add four dimensions for conversational AI specifically, but none of these map
   to a scored, administered questionnaire for text-only systems without avatar or voice. (A, C)
2. **The uncanny valley of language is under-measured.** Ciechanowski et al. (2019) and the MIT
   2025 SDM thesis confirm the effect exists in text. Sesame AI (Feb 2025) crossed the voice
   uncanny valley. But no systematic mapping of which specific *linguistic* features (hedges,
   disfluencies, pronouns, apologies, opinion markers) push users up or down the text-only curve
   exists at sentence level. (A, C)
3. **Post-disclosure dynamics.** Most CASA work predates user knowledge that they are talking to
   an LLM. How disclosure interacts with linguistic humanness cues is open; Lucas & Gratch (2014)
   and De Freitas (2025) point in different directions. Guingrich & Graziano (2025) do not vary
   disclosure condition. (A)
4. **Trust calibration × anthropomorphism jointly.** Cohn (2024), Reani et al.'s Fundamental
   Over-Attribution Error (2025), and the algorithm-appreciation literature are rarely integrated.
   When does humanlike style help calibration, and when does it break it? Almost no study
   manipulates style independently of accuracy. (A, B)
5. **No canonical "humanization success" benchmark.** AnthroBench measures unwanted
   anthropomorphism; HumT measures tone; Chatbot Arena measures preference; Cheng et al. (2025)
   measure de-anthropomorphization interventions. None measure: "did this style edit make the
   output more human-like without sliding into deception or value manipulation?" Combining
   AnthroScore + HumT + HumanAgencyBench + adversarial detectors into one scored pipeline would
   be net-new. (C)
6. **Godspeed / RoSAS have no maintained Python package.** Only a LaTeX template, an R package,
   and ad-hoc Google Forms adaptations exist. A pip-installable prompt-administered Godspeed
   harness is a small but high-leverage gap. (C)
7. **Jones & Bergen's code and prompts are not released.** A faithful open replication of their
   Turing test protocol would be the evaluation gold standard. (C)
8. **No benchmark for "feels human over 100 hours."** All existing measures are single-session.
   Guingrich & Graziano (2025) ran 21 days — the longest RCT in this space — but still found
   no significant group-level social effects. The community record makes clear that perceived
   humanness at hour 100 is qualitatively different from hour 1. (E)
9. **No practitioner treatment of middle-band humanness.** The discourse sits at the poles
   (technical manual versus girlfriend). A professional, humanlike-but-non-parasocial voice is
   under-documented. The APA's "deskilling" concern makes this gap now commercially and ethically
   urgent. (B, E)
10. **Voice-match / ghostwriting as a distinct legitimacy frame is almost absent.** Writing in the
    documented voice of a specific named author is a centuries-old practice that does not trigger
    the companion problem. No surveyed source distinguishes match-an-author humanization from
    become-a-companion humanization. This is the gap Unslop is best positioned to occupy. (B, E)
11. **No patch-breakup tooling.** Given three industry events (Replika 2023, GPT-4o 2025, ChatGPT
    Aug 2025), tooling to detect tone drift across model versions, warn users, and roll back
    persona independently of weights is a clear product opportunity with no existing owner. (E)
12. **User-side controls for humanization are underdesigned.** HAX guidelines cover system-side
    disclosures. Almost no writing exists on what a well-designed user control surface for
    humanization should look like for a B2B product targeting writers. (B)
13. **Adolescent-specific measurement instruments do not exist.** Neugnot-Cerioli et al. (2026)
    establish that adult anthropomorphism scales cannot be applied to adolescents. No validated
    adolescent-specific instrument for measuring AI anthropomorphism or attachment risk is
    available. This is a clinical and regulatory gap. (A)
14. **The combinatorial problem is unaddressed.** Perrig et al. (ICLR 2025) name it: studies
    isolate individual humanization features (voice, memory, first-person pronouns, warmth) but
    real-world systems combine multiple features simultaneously. The emergent effect of stacked
    humanization signals is unmeasured. (B, C)
15. **"Social-skill deskilling" lacks a measurement instrument.** The APA named the phenomenon;
    no validated scale for measuring friction-tolerance degradation from AI companion use exists.
    This is the gap between a clinical concept and a clinical tool. (A, D)

---

## How This Category Fits

Category 13 is the "why does this matter?" and "how do we measure it?" foundation for the broader
Unslop research stack. It connects to adjacent categories in several ways. The AI detection and
evasion work (category 05) is the adversary: detector benchmarks (CUDRT, MGTBench) establish the
baseline that humanization outputs will be tested against, but this category argues the actual
target should be reader-experience humanness, not classifier-invisible text. Prompt engineering
(category 06) is the implementation layer: Jones & Bergen's persona recipe, the NN/g style-by-
example finding, and the RLHF-tell removal list are direct inputs to the prompt design work. Voice
and multimodal synthesis is a modality multiplier: the Cohn et al. and Ciechanowski findings
establish how far voice anthropomorphism can go before perception inverts; the text-first humanizer
should find text analogs to voice's backchannel and latency signals. Safety and alignment categories
connect through Anthropic's persona vectors and the sycophancy rollback case study, which span both
humanization design and alignment failure modes. UX patterns and conversational design categories
receive HAX, PAIR, Yocco's transparency moments, and the community "metacognitive UI" findings as
primary inputs. Ethics and policy categories receive the Shibboleth rule, the Turing Trap argument,
Abercrombie's "Mirages" harms taxonomy, and Burkert's disclosure-ceiling argument as vocabulary
for decisions the product will face around companion-mode, disclosure, and age-gating.

---

## Recommended Reading Order

1. **Jones & Bergen 2024 NAACL paper** (arXiv:2405.08007) — the headline empirical result; read
   the 2025 FAccT follow-up (arXiv:2503.23674) for the persona-prompt recipe and 73% figure.
2. **Sponheim — "Humanizing AI Is a Trap" (NN/g, 2025)** + **Liu & Sunwall — "4 Degrees of
   Anthropomorphism" (NN/g)** — the operative industry framing and the anthropomorphization /
   humanization split.
3. **Nass & Moon (2000) — "Machines and Mindlessness"** — the 30-year context; the stated-behavior
   gap as a named phenomenon.
4. **Gray, Gray & Wegner (2007) — "Dimensions of Mind Perception"** (*Science*) — the Agency ×
   Experience axis that every downstream instrument inherits.
5. **Anthropic — "Claude's Character" (2024) + "Persona Vectors" (2025)** — the pro-character
   position and the mechanistic turn; the most developed industry argument for deliberate character
   design.
6. **Replika Feb 2023 ERP removal coverage** (Gizmodo / ABC) + **SBS ChatGPT Aug 2025 tone update
   coverage** — the field's two natural experiments; read in this order for narrative arc.
7. **Pető (UX Studio, 2024)** — 25-minute drift study; trust-collapse-on-first-repetition finding.
8. **Bora — "When Tools Pretend to Be People" (UX Collective, Jan 2026)** + **Burkert — "The Case
   Against Anthropomorphic AI"** — the ethical-ceiling arguments; the strongest case against
   first-person framing.
9. **Cheng et al. — AnthroScore (EACL 2024)** + **Google DeepMind AnthroBench (arXiv:2502.07077)**
   — the automatic-metric and multi-dimensional benchmark substrates.
10. **r/MyBoyfriendIsAI MIT Media Lab writeup (arXiv:2509.11391)** + **r/CharacterAI academic
    analysis (arXiv:2507.15783)** — the ethnographic ground truth on what sustained humanization
    produces at scale.
