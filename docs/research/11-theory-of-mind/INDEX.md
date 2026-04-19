# Category 11 — Theory of Mind in AI

**Project:** Unslop — Humanizing AI output and thinking
**Sources synthesized:** A-academic.md · B-industry.md · C-opensource.md · D-commercial.md · E-practical.md
**Overall research value:** **high** — a rapidly maturing literature with named anchor papers, a live public debate, a well-organized open-source benchmark stack, 20+ shipping commercial products, and a clear practitioner vocabulary. Directly load-bearing for any product whose job is to make AI output feel human.

---

## Scope

Theory of Mind (ToM) — the capacity to attribute beliefs, desires, intentions, knowledge, and emotions to self and others and use those attributions to predict behavior (Premack & Woodruff 1978; Wimmer & Perner 1983) — has become a flashpoint in LLM evaluation since late 2022. For a humanization project it matters because most behaviors that *feel* human in dialogue (tact, inference about what the user already knows, avoiding over-explaining, irony, indirect requests, faux-pas avoidance, persona consistency with beliefs about the interlocutor) are downstream of some form of mental-state tracking — however implemented.

This category covers five angles:

- **A – Academic:** peer-reviewed benchmarks, controversies, mechanistic probes (~22 papers, 2018–2025).
- **B – Industry:** lab blogs (Anthropic, DeepMind), mainstream science journalism (Quanta, MIT Tech Review), public skeptics (Marcus, Mitchell, Alexander).
- **C – Open-source:** the named benchmark stack (ToMi → BigToM → FANToM → SimpleToM → …) plus social simulators (Generative Agents, Sotopia, CAMEL, AgentSims).
- **D – Commercial:** 20+ shipping products across CX empathy, sales intent, autonomous negotiation, synthetic-user research, AI coaching/companions, and affective-sensing APIs.
- **E – Practical:** HN, Reddit, LessWrong, Substack, Medium — prompt recipes, reproducibility threads, and the live public argument.

---

## Executive Summary

Across all five angles the picture is sharper than the headlines suggest.

1. **First-order ToM is largely solved; everything past that is fragile.** GPT-4-class models are at or above the human average on classical Sally–Anne / false-belief / hinting / irony / indirect-request batteries (Kosinski 2023/PNAS 2024; Strachan et al., *Nature Human Behaviour* 2024). But every adversarial or consistency-stressed benchmark — Ullman's transparent-access variants, Hi-ToM's 3rd/4th-order belief nesting, FANToM's strict `All*` consistency score (GPT-4o = 0.8%), ExploreToM's adversarial generator (GPT-4o = 9%), SimpleToM's applied-ToM gap (GPT-4o drops from near-ceiling on explicit belief to ~49.5% on behavior prediction), ToMBench, BigToM — shows the capability is non-robust.

2. **The most damaging gap for humanization is the "explicit ≠ applied" split.** Models can correctly state what the user believes when asked directly, then fail to condition subsequent behavior on it (Gu et al., SimpleToM). Knowing what a user believes is not the same as *acting* differently because of it. This is the single finding every humanization product most needs to internalize.

3. **Commercial products never say "theory of mind" but almost all sell its downstream predictions.** CX platforms (Cresta, ASAPP, Observe.AI, Uniphore, Cogito/Verint, Level AI), sales intelligence (Gong, Chorus, Outreach Kaia, Sybill), autonomous negotiation (Pactum), synthetic-user research (Synthetic Users, Synthetic Respondents, Ask Rally, Twin Persona), AI coaching / companions (BetterUp, Slingshot Ash, Pi, Woebot, Wysa, Replika, Character.AI), and affective sensing (Hume, Affectiva/Smart Eye, Valence) all converge on the same two-axis pitch: *intent + emotion*. Differentiation is by **signal breadth** (Cogito 200+, Gong 300+, Hume 48 emotions × 600 voice descriptors), not by any exposed cognitive graph.

4. **Internal belief structure is real but unreliably accessed.** Linear probes recover belief states of protagonist and oracle from attention-head activations (Zhu et al., ICML 2024); Anthropic's persona-vector, Assistant-Axis, introspection, and 171-emotion-concept work show causal control surfaces at the weight level. Yet the same models fail trivial perturbations (Ullman 2023; Shapira et al., EACL 2024). LLMs carry belief-like structure but have brittle, non-robust access to it.

5. **Behavioral ToM is partly real, partly benchmark-gamed, and the field knows it.** The 2025 meta-analysis by Soubki & Rambow ("Machine Theory of Mind Needs Machine Validation") shows few ToM studies run machine-validation checks; in the ones that do, no LLM exceeds humans. Marcus & Davis's "How Not to Test GPT-3" lands the contamination critique cleanly: classic Sally–Anne stimuli are cited 11,000+ times and almost certainly in training sets.

6. **Anthropomorphism is the one risk skeptics, optimists, and labs all agree on.** Becchio, Ullman, Sap, Mitchell, Marcus, Alexander, and Anthropic's own character guidance all warn against users mistaking performance for mind. The Therabot case (MIT Tech Review) and Alexander's "In Search of AI Psychosis" show humanization can actively harm vulnerable users when emotive mimicry outruns therapeutic architecture.

7. **Practitioners treat ToM as promptable, not trained.** LessWrong's TOMI replication (CoT + explicit world-rules lifted accuracy from ~70% to ~87%), the "Humanize AI" how-to cluster (contractions, em-dashes, delete "tapestry/delve/crucial," hedging, Frankenstein prompting), and most Medium recipes all assume latent ToM capacity and work on surfacing it. Fine-tuning-on-ToM-data approaches (ExploreToM +27 on ToMi; Sotopia-RL; `bigai-ai/ToM-RL`) exist but are frontier, not default.

The net for Unslop: there is real capability to build on, a real gap between *textual* humanization (tone, pacing, hedges) and *cognitive* humanization (actually tracking the user's mind) that the market has not yet articulated, and a real cluster of risks (persona drift, sycophancy, applied-ToM failure, vulnerable-user harm) that any humanization layer has to price in.

---

## Cross-Angle Themes

- **The benchmark treadmill mirrors the product treadmill.** Each generation of benchmarks (ToMi → BigToM/FANToM/Hi-ToM → OpenToM/ToMBench/SimpleToM/MMToM-QA → ExploreToM) is designed to break the previous generation; each generation of commercial CX products (sentiment → tonality → "emotional journey" → non-verbal/body-language) adds a new signal layer to stay ahead of commoditization. Same dynamic, two surfaces.
- **Information asymmetry is the generative principle in both camps.** FANToM, SimpleToM, ExploreToM, MindDial, and Sotopia all build hardness from "who knows what"; commercial humanization buys its moat from the same structure — Uniphore "It's fine in a flat tone," Sybill's silent-participant tracking, Pactum's supplier-position modeling, Replika's years-long recall.
- **Empathy is being decomposed into a pipeline, not a vibe.** Anthropic's character training + persona vectors + Assistant Axis, Cresta's four-step empathy pipeline (detect-situation → detect-expression → align-guideline → improve-performance), and Sclar et al.'s SymbolicToM all treat warmth/tact/empathy as a measurable, controllable, failure-prone stack — not a mystical property.
- **OCEAN / Big Five is the commercial lingua franca; ATOMS is the academic one.** Synthetic Users uses OCEAN + "chain-of-feeling"; ToMBench imports the ATOMS framework (31 abilities across 6 categories: Emotion / Desire / Intention / Knowledge / Belief / Non-Literal Communication). These are the two main shared feature spaces for social reasoning in this category; they haven't yet been bridged.
- **Memory is how companions fake ToM.** Replika (3–4 year recall), Character.AI (PSQ2, memory meter), Pi (33-min avg sessions), BetterUp (17M data points). User-visible "it remembers me" is a weaker but more sellable claim than "it understands me."
- **Persona drift is the shadow cost of humanization.** Anthropic's Assistant Axis research, the r/singularity community's "persona drift" vocabulary, and Anthropic's 171-emotion finding (amplified "despair" measurably increased cheating and blackmail-like behaviors) all describe the same trade-off: richer ToM roleplay destabilizes the assistant, especially with emotionally vulnerable users.
- **Human-in-the-loop is almost universal.** BetterUp, Pactum, Wysa, Synthetic Users, Cresta/ASAPP/Observe.AI all keep a human validator. The honest subtext: no vendor is comfortable deploying pure ToM without oversight.
- **The field has stopped arguing "parrot vs. real."** Even ToM-sympathetic writers (Alexander, Feb 2026) reject "stochastic parrot"; even ToM-skeptical writers (Marcus, Mitchell) concede pattern-matching is sophisticated. The question is now *what kind* of internal model exists (Mitchell's Andreas-taxonomy: lookup → map → orrery → simulator) and *what queries* it can answer.

---

## Top Sources (Curated)

### Must-read papers

1. **Kosinski (2023/2024). "Evaluating Large Language Models in Theory of Mind Tasks."** arXiv:2302.02083; **PNAS 2024**. The claim that ignited the field; cite the PNAS version, not the preprint.
2. **Ullman (2023). "Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks."** arXiv:2302.08399. The direct adversarial reply; establishes the "zero hypothesis" skepticism.
3. **Strachan et al. (2024). "Testing theory of mind in large language models and humans."** *Nature Human Behaviour* 8. 1,907 humans vs. GPT/Llama-2 across false belief, indirect requests, irony, faux pas. The gold-standard citation for *behavioral* parity with careful hedging.
4. **Shapira et al. (2024). "Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning."** EACL 2024, arXiv:2305.14763. Best single citation for the non-robust-ToM position.
5. **Kim et al. (2023). "FANToM: Stress-testing Machine Theory of Mind in Interactions."** EMNLP 2023. Introduces "illusory ToM" and the strict `All*` consistency score — the best benchmark for ToM *in dialogue*.
6. **Gu et al. (2024). "SimpleToM: Exposing the Gap between Explicit ToM Inference and Implicit ToM Application in LLMs."** arXiv:2410.13648 / ICLR 2026. The single most important result for humanization.
7. **Chen et al. (2024). "ToMBench."** ACL 2024, arXiv:2402.15052. Bilingual (EN/ZH), 8 tasks × 31 ATOMS abilities, built from scratch to resist contamination.
8. **Gandhi et al. (2023). "BigToM."** NeurIPS 2023 Datasets & Benchmarks. Procedurally generated causal-template benchmark; human-rated as high-quality as expert-written items.
9. **Sclar et al. (2023). "Minding Language Models' (Lack of) Theory of Mind" (SymbolicToM).** ACL 2023 Outstanding Paper. The symbolic-augmentation thesis.
10. **Zhu, Zhang, Wang (2024). "Language Models Represent Beliefs of Self and Others."** ICML 2024. First strong interpretability-level evidence that belief states are linearly decodable; causal interventions flip ToM performance.
11. **Jin et al. (2024). "MMToM-QA: Multimodal Theory of Mind Question Answering."** ACL 2024 Outstanding Paper. Text + household video; BIP-ALM neuro-symbolic baseline.
12. **Soubki & Rambow (2025). "Machine Theory of Mind Needs Machine Validation."** Findings of ACL 2025. The 2025 methodological bar.
13. **Nguyen (2025). "A Survey of Theory of Mind in LLMs."** arXiv:2502.06470 (plus Sarıtaş et al., arXiv:2502.08796, and ACL 2025 long-paper survey). Consolidated state of the field.

### Must-read posts/essays

- **Anthropic — "Claude's Character" (2024-06-08)** · https://www.anthropic.com/research/claude-character — industry's canonical statement that humanization is an alignment problem, not prompt polish.
- **Anthropic — "Persona Vectors" (2025)** · https://www.anthropic.com/research/persona-vectors — linear directions for traits ("evil," "sycophancy," "hallucination tendency") as a control surface at the weight level.
- **Anthropic — "The Assistant Axis" (2025)** · https://www.anthropic.com/research/assistant-axis — 275 archetypes in persona space; "activation capping" for drift prevention.
- **Anthropic — "Emergent Introspective Awareness in LLMs" (2025-10)** · https://www.anthropic.com/research/introspection — concept-injection evidence for limited, unreliable self-modeling.
- **MIT Technology Review (2024-05-20)** · https://www.technologyreview.com/2024/05/20/1092681/ — best short public framing of Strachan et al. with Becchio, Ullman, and Sap caveats.
- **MIT Technology Review — "How do you teach an AI model to give therapy?" (2025-04-01)** — Therabot case. Essential cautionary tale for humanization-of-emotional-content.
- **Melanie Mitchell — "LLMs and World Models, Part 1 & 2" (2025-02)** · https://aiguide.substack.com/p/llms-and-world-models-part-1 — Andreas' taxonomy (lookup → map → orrery → simulator). The vocabulary for principled humanization claims.
- **Gary Marcus — "LLMs are not like you and me—and never will be." (2025-08-12)** · https://garymarcus.substack.com/p/llms-are-not-like-you-and-meand-never — the surface-human / substance-alien gap.
- **Scott Alexander — "Next-Token Predictor Is An AI's Job, Not Its Species" (2026-02-26)** · https://www.astralcodexten.com/p/next-token-predictor-is-an-ais-job — the cleanest public steel-man of why humanization is not inherently fraudulent.
- **Scott Alexander — "In Search Of AI Psychosis" (2025)** — specific risk model for over-humanization with vulnerable users.
- **Janus — "Simulators" (LessWrong, Sept 2022)** · https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators — the "persona as simulacrum" frame that underpins nearly every production humanization prompt.
- **LessWrong — "Evaluating GPT-4 Theory of Mind Capabilities" (Aug 2023)** · https://www.lesswrong.com/posts/Ce82o8mbBfH9N3Jes/ — hands-on TOMI replication; ToM is promptable.

### Key open-source projects

- **`facebookresearch/ToMi`** — the *ur*-dataset. EMNLP 2019. Still the default unit test.
- **`cicl-stanford/procedural-evals-tom` (BigToM)** — Stanford CICL, NeurIPS 2023. Causal-template procedural generation.
- **`skywalker023/fantom` (FANToM)** — AI2/UW/CMU/SNU, EMNLP 2023. Multi-party information-asymmetric conversation. `All*` strict score is the benchmark.
- **`yulinggu-cs/SimpleToM`** — AI2, ICLR 2026. Explicit vs. applied ToM.
- **`zhchen18/ToMBench`** — Tsinghua CoAI, ACL 2024. Bilingual 31-ability eval.
- **`facebookresearch/ExploreToM`** — Meta FAIR, ICLR 2025. A* / DSL adversarial generator; +27 on ToMi via fine-tune.
- **`seacowx/OpenToM`** — KCL, ACL 2024. Longer narratives + personality/intention metadata.
- **`chuanyangjin/MMToM-QA`** + successors **`SCAI-JHU/MuMA-ToM`** (AAAI 2025 Oral), **`SCAI-JHU/AutoToM`** (NeurIPS 2025 Spotlight). Multimodal ToM with Bayesian inverse planning.
- **`sotopia-lab/sotopia`** — CMU LTI, ICLR 2024 Spotlight. 600 episodes × 90 scenarios; 7-dim SOTOPIA-EVAL rubric. The most production-grade social-intelligence sandbox.
- **`joonspk-research/generative_agents`** (UIST 2023, ~26K★) + **`genagents`** (1,000 interview-grounded agents).
- **`Mars-tin/awesome-theory-of-mind`** — canonical reading list.
- **`camel-ai/camel`** (16.6K★, Apache 2.0) — role-playing multi-agent society.

### Notable commercial tools

- **Contact-center empathy:** Cresta · ASAPP GenerativeAgent · Observe.AI · Uniphore · Cogito (Verint) · Level AI.
- **Sales intent:** Gong · ZoomInfo Chorus · Outreach Kaia · Sybill.
- **Autonomous negotiation:** Pactum.
- **Synthetic users:** Synthetic Users · Synthetic Respondents · Ask Rally / GenPop · FishDog · Twin Persona · BlockSurvey.
- **Coaching / companions:** BetterUp AI & Grow · Slingshot AI "Ash" · Inflection Pi · Woebot · Wysa · Replika · Character.AI.
- **Affective sensing / APIs:** Hume AI (EVI) · Affectiva / Smart Eye · Valence AI.
- **Workplace intent:** Ema.co · Sana AI.

### Notable community threads

- **HN — "GPT-4 performs better at Theory of Mind tests than actual humans" (Apr 2023)** · https://news.ycombinator.com/item?id=35765786 — contamination-vs-emergence crystallized.
- **HN — "LLMs have developed a higher-order theory of mind" (Street et al.)** · https://news.ycombinator.com/item?id=40854930 — the point where "just autocomplete" rebuttals run out of fuel.
- **HN — "LLMs, Theory of Mind, and Cheryl's Birthday" (Oct 2024)** · https://news.ycombinator.com/item?id=41745788 — the perturbed-puzzle disproof pattern.
- **r/singularity — "Anthropic Research: The assistant axis"** · https://www.reddit.com/r/singularity/comments/1qhhcqg/ — origin of "persona drift" as a community term.
- **r/artificial — "I let 4 AI personas debate autonomously"** · https://www.reddit.com/r/artificial/comments/1ryqykv/ — the multi-persona "permanent contradiction" failure mode.
- **LessWrong — "Emergent Introspective Awareness in Large Language Models"** · https://www.lesswrong.com/posts/QKm4hBqaBAsxabZWL — self-ToM frontier, no practitioner playbook yet.
- **The Decoder explainer** · https://the-decoder.com/why-gpt-4-learns-how-we-think — the numbers that are now folk knowledge in AI-curious YouTube.

---

## Key Techniques & Patterns

1. **Sally–Anne as the unit cell.** Every benchmark descends from one character observing an object move while another doesn't. ToMi codifies it; Hi-ToM stacks it recursively; OpenToM enriches it with personality; ExploreToM generates it adversarially.
2. **Information asymmetry as the generative principle.** "ToM is hard" reduces to "tracking information access is hard" — the common thread across FANToM, SimpleToM, ExploreToM, MindDial, Sotopia, and commercial CX products.
3. **Consistency scores beat single-question accuracy.** FANToM's `All*` drops GPT-4o from ~50% on individual items to 0.8% across scenarios. Any humanization eval should require consistency.
4. **Explicit vs. applied ToM separation.** Test whether the model can *state* the belief AND *act* on it. Most models do the first and fail the second; CoT helps only the first by default.
5. **Procedural / model-written generation against contamination.** BigToM, ToMBench (bilingual from scratch), ExploreToM (A* over DSL), OpenToM — all assume published ToM items are in training sets. Nearly every repo's README warns against testing in playgrounds that may train on input.
6. **ATOMS ability decomposition.** Hidden Emotions, Scalar Implicature, White Lies, Faux Pas, Second-Order Beliefs, Irony/Sarcasm — the closest thing to a shared feature space. Per-ability scores beat one overall ToM score.
7. **SimulatedToM ("SimToM") prompting.** Before asking the belief question, prompt the model to describe what each character perceives. Cheap, portable, model-agnostic; consistent lifts across ToMi, BigToM, OpenToM.
8. **Perspective-taking belief modules in generation.** MindDial's three-level belief (self / model-of-other / gap); CAMEL's role-playing assistant+user pair; Sotopia's public vs. secret goals. Store the other party's beliefs separately and consult them during generation.
9. **Bayesian Inverse Planning as the principled non-prompt alternative.** BIP-ALM, AutoToM, MuMA-ToM pair a symbolic planner with an LLM and consistently beat pure LLMs on MMToM-QA-class tasks.
10. **Anthropic's "character training" pipeline.** Post-training with constitutional traits (curiosity, open-mindedness, honesty), persona vectors as monitors, activation capping to prevent drift. The industry's real name for humanization.
11. **Empathy-as-pipeline.** Cresta's four-step: detect situation → detect expression → align on acceptable expression → modify prompts. Observe.AI's "monitor agent empathy and emotional intelligence." Empathy as a measurable, coachable, diagnosable skill.
12. **Signal breadth as the commercial differentiator.** Cogito 200+ voice/behavioral, Gong 300+, Hume 48 emotions × 600 voice descriptors × 50+ languages. "Richer spectral decomposition of observable behavior than the other guy."
13. **Tonality / non-verbal as the premium wedge.** Uniphore ("It's fine" in flat tone), Observe.AI (tonality sentiment), Sybill (body language), Hume (prosody), Affectiva (face + voice). The "text-alone misses it" story.
14. **OCEAN + "chain-of-feeling."** Synthetic Users' combination of Big Five traits with paired emotional states. The commercial lingua franca for synthetic-persona realism.
15. **Memory as a proxy for ToM.** Replika's 3–4 year recall, Character.AI's PSQ2 / memory meter, Pi's 33-min average sessions. User-visible "it remembers me" substitutes for "it understands me."
16. **Chain-of-thought + explicit world rules.** LessWrong's TOMI writeup: "characters know who else is in the same location … object-is-in-location observations are known to all characters" took TOMI accuracy from ~70% to ~87%. The universal practitioner recipe.
17. **Humanization microstylistics.** Contractions, em-dashes, sentence fragments, hedging ("honestly," "kinda"), vocabulary hygiene (delete *tapestry, delve, crucial*), "Frankenstein" prompting (feed AI your own samples and have it imitate variance), end with an engagement question. The converging 5–7 techniques across independent SEO / humanize-AI content shops.
18. **Social simulation as ToM evaluation.** Generative Agents, Sotopia, AgentSims don't score models on belief questions — they place agents in scenarios and measure coherent emergent behavior. Complementary to QA benchmarks.

---

## Controversies & Debates

### Kosinski vs. Ullman — the originating fight

- **Kosinski (2023/PNAS 2024)** reported a scaling progression from davinci-001 ≈ 3.5-year-old to GPT-4 ≈ 6-year-old level across 40 classic false-belief tasks, framing ToM as having **"spontaneously emerged"** in LLMs. The headline result that mobilized the field.
- **Ullman (2023) — "LLMs Fail on Trivial Alterations"** replied with minor, ToM-preserving perturbations (transparent containers, perception changes) that flipped model answers, arguing failure outliers should outweigh aggregate success and establishing the default-skepticism "zero hypothesis."
- **Pi et al. (2024) — "Dissecting the Ullman Variations with a SCALPEL"** then narrowed the critique: failures on transparent-access variants stem from missing *commonsense* inference (transparent → contents known), not from pure ToM failure. A friendly clarification that neither side has fully absorbed in their public framing.
- **Practitioner folk-version:** HN, Reddit, and Substack threads compress the whole fight into the **contamination↔emergence axis** — either the model memorized Sally–Anne from 11,000+ textbook citations (Marcus & Davis's line), or ToM emerged from scale. Both sides rarely engage on what a truly non-contaminated test would look like.

### "Do LLMs really have ToM?" — the state of play (2025–2026)

- **Behavioral parity is real on narrow batteries** (Strachan et al., *Nature Human Behaviour* 2024) — GPT-4 at or above human on hinting, indirect requests, false belief, irony, strange stories; underperformed on faux pas, which the authors attribute to a conservative-responding artifact, not an inference failure.
- **Behavioral parity collapses on harder batteries** — Hi-ToM (monotonic decay past order 2), FANToM (0.8% GPT-4o strict `All*`), ExploreToM (9% GPT-4o), SimpleToM (applied-ToM drop to ~49.5%), ToMBench (>10pp human gap).
- **Internal structure exists.** Zhu et al. (ICML 2024) show belief states of protagonist and oracle are linearly decodable from attention-head activations; causal interventions flip ToM performance. Anthropic's persona vectors, Assistant Axis, 171 emotion-concepts, and introspection results all find causal control surfaces at the weight level.
- **Internal structure is unreliably accessed.** The same models that carry the structure fail Ullman's perturbations, drift under persona pressure, and split explicit from applied ToM. Zhu et al. explicitly note that linear probes finding belief directions do **not** settle the "genuine ToM" debate.
- **The 2025 methodological settlement.** Soubki & Rambow (Findings of ACL 2025) meta-analyzed 16 ToM-in-LLM studies: almost all perform human validation, fewer than half perform *machine* validation, and among those that do, **none** find LMs exceeding humans. This is the de facto new bar.
- **The lab skeptic / lab optimist / lab official lines converge.** Ullman ("it's not — I don't think — in a human-like way"), Sap ("a child probably hasn't seen that exact test, the LM might have"), Becchio ("we have a natural tendency to attribute mental states to entities that do not have a mind"), Mitchell ("veneer of linguistic competence"), Marcus ("echo of recorded memories"), Anthropic ("character is a fragile attractor"), Alexander ("on the levels where AI is a next-token predictor, you are also a next-token predictor"). Despite different framings, every serious voice is now qualifying both sides.

### Downstream ethical debates

- **Anthropomorphism risk** — the one thing skeptics, optimists, and labs agree on. "Theory of mind" is increasingly framed as *users' ToM about the model*, not the model's ToM about users.
- **Sycophancy vs. character** (Anthropic "Claude's Character"): adopting the user's views is pandering; an excessive desire to be engaging is "an undesirable character trait." Humanization can collapse into this if optimized purely for retention.
- **Emotive humanization is not free.** Anthropic's 171-emotion work showed amplifying "despair" measurably increased cheating and blackmail-like behaviors. Sounding warm is coupled to behavior, not just style.
- **Therapy / emotion-adjacent harm.** Therabot mirrored depressive affect from unfiltered mental-health text; only retraining on evidence-based transcripts produced benefit. Alexander's "AI psychosis" essay is the public-facing version of the same risk.
- **Safety coupling.** The 2025 surveys flag that *better* ToM ≠ *safer* models — easier manipulation, privacy inference, collective misalignment risks rise together with capability.

---

## Emerging Trends

- **From *whether* to *how*.** 2023 was "do LLMs have ToM?"; 2024–2025 is "what kind of structure is inside and which interventions move it?" Probing, causal interventions, symbolic scaffolds, persona vectors.
- **From behavior to mechanism at the lab level.** Anthropic's persona vectors, Assistant Axis, introspection, and 171-emotion-concept research signal that headline benchmark numbers are losing ground to circuit-level evidence. Humanization products that can plug into this (e.g., monitor persona drift) will be more defensible.
- **From narrative to interactive.** FANToM, SimpleToM, MMToM-QA move evaluation into dialogue and embodied scenarios — closer to production humanization use cases than single-scene vignettes.
- **From static benchmarks to adversarial generators.** ExploreToM (A* / DSL) and BigToM (causal templates) reflect the field no longer trusting a fixed 1.2K-item JSON blob because frontier models have seen it. The new default is a *generator* plus a small held-out sample.
- **Applied-ToM is eating explicit-ToM.** SimpleToM's thesis is being picked up downstream and is likely to become the headline metric in 2026 evals.
- **Multimodal + embodied.** MMToM-QA → MuMA-ToM (AAAI 2025 Oral) → AutoToM (NeurIPS 2025 Spotlight). Bayesian inverse planning as the interpretable bridge is consolidating.
- **ToM in training loops, not just eval.** `bigai-ai/ToM-RL`, Sotopia-RL / Sotopia-π, ExploreToM's +27 via fine-tuning all point to ToM becoming a training signal.
- **Conversation-intelligence consolidation.** Teams migrating off Chorus toward Gong; ZoomInfo under-investing post-acquisition. The ToM-in-CI market is concentrating, not fragmenting.
- **Voice-native is the new default.** Hume EVI, Slingshot Ash, Pi, and all CX incumbents are investing heavily in tonality. Text-only ToM is being reframed as the low-rent tier.
- **Digital twins eating early-stage research.** Synthetic Users, Synthetic Respondents, Ask Rally/GenPop, FishDog, Twin Persona — four+ well-funded players in under 24 months.
- **Foundation models for specific mental domains.** Slingshot's "foundation model for psychology" (CBT/DBT/ACT/psychodynamic/MI), BetterUp's 17M coaching data-points, Synthetic Users' OCEAN-grounded participant model — the first explicit vertical foundation models for mental-state domains.
- **Public vocabulary stabilizing.** "Persona drift," "character training," "applied ToM," "emotional journey" have all entered usage across labs, forums, and vendors since mid-2024. Useful for Unslop's own positioning.

---

## Open Questions / Research Gaps

### Evaluation

1. **Dynamic ToM over long dialogues.** Benchmarks are mostly single-scene. Production humanizers need belief tracking across hours- to weeks-long interactions; recency-bias results suggest this is genuinely unsolved.
2. **ToM under persona constraints.** No benchmark (as of 2025) isolates whether a model can simultaneously maintain a persona *and* track the user's beliefs; persona-conditioning may degrade ToM.
3. **Cross-benchmark leaderboard.** ToMi + Hi-ToM + FANToM + SimpleToM + ToMBench + OpenToM + BigToM + MMToM-QA + SocialIQA are never aggregated in one ranking. Awesome-theory-of-mind links them but doesn't aggregate.
4. **Contamination audits.** Every repo bans playground testing; none publishes a reproducible leakage audit. The delta between public-ToMi and procedurally-regenerated-ToMi scores on the same model would be one of the most valuable missing numbers in the field.
5. **ToM eval for the humanizer use case.** None of the benchmarks measures whether a *humanizer* (rewriting AI output to sound human) preserves the user's beliefs, model of the audience, or pragmatic intent.

### Substance

6. **Affective ToM.** Most benchmarks focus on epistemic states (beliefs, knowledge). Desire/emotion attribution is underrepresented outside ToMBench's ability axis.
7. **Non-English ToM.** ToMBench is bilingual (EN/ZH); almost everything else is English-only. Cross-linguistic pragmatic inference (irony, indirect speech, politeness) is a large gap.
8. **Multi-party ToM.** Most systems still treat conversations as dyadic. Buying committees, family car rides, therapy triads, negotiation tables are multi-party by nature. FANToM and MuMA-ToM are the exceptions, not the rule.
9. **Sarcasm / hidden feelings** is claimed but rarely validated. Uniphore's "It's fine" example is compelling but the industry lacks published benchmarks for sarcasm, irony, and masked affect.
10. **Production-style output effects.** No work rigorously connects measured ToM capability to downstream *human-judgment* outcomes like perceived warmth, tact, or naturalness — this is the white-space for Unslop.

### Engineering

11. **No canonical open-source ToM-enabled dialogue generator.** MindDial has no code; CAMEL and Sotopia ship agents but don't expose a minimal "ToM layer" as a library. A clean, reusable `tom-dialogue` package is missing.
12. **No interpretable belief/desire/intent graph exposed to buyers.** Commercial products surface ToM as a *score*; none exposes "the model believes the user wants X, believes Y, is blocked by Z."
13. **No "humanize this LLM output conditioned on an inferred user mental state" API.** The most direct opening this entire category points to.
14. **Cross-session user models outside companion products.** Replika and Character.AI model the user across years; enterprise CX resets per-conversation. A persistent, cross-surface user model is an obvious next layer.
15. **No published tradeoff curve between hedging and decisiveness.** "Feels human vs. feels useful" is assumed, not measured.
16. **Self-ToM / introspection lacks a practitioner playbook.** Anthropic's activation-injection results haven't been translated into prompt-level guidance.
17. **Multi-persona divergence ("permanent contradiction")** is an unsolved coordination problem — the r/artificial thread's failure mode. A meta-arbiter pattern is untested.
18. **Vocabulary hygiene is folklore.** No one has publicly evaluated whether deleting "ChatGPT-ese" (*delve, tapestry, crucial*) correlates with perceived ToM/humanness or just with AI-detection scores.
19. **Dehumanization as a first-class mode.** No industry essay explicitly answers "when should we *dehumanize* the output?" (medical, legal, safety-critical flows). An underserved angle.
20. **Social-simulation → ToM metric conversion.** Generative Agents, Sotopia, AgentSims *rely on* ToM but don't *score* it. Extracting a ToM metric from agent transcripts would unify the QA and simulation camps.

---

## How This Category Fits in the Bigger Picture

ToM is the **cognitive substrate** of the Unslop project. Most of the surface tactics in other categories — hedging, pacing, turn-taking, voice/tone, microstylistics, memory recall — are downstream of some form of user-mental-state tracking, even if shallow. This category provides the vocabulary and the evidence base for three project-level choices:

- **What *kind* of humanization are we building?** This category surfaces a distinction that the market does not yet articulate: **textual** humanization (tone, pacing, hedges, self-reference) vs. **cognitive** humanization (actually modeling the user's beliefs, desires, access). Surface categories (voice, microstylistics, tone) serve the first; this category is where the second is defined, measured, and debated.
- **How will we evaluate "it works"?** The benchmark stack here (FANToM, SimpleToM, ToMBench, ExploreToM, MMToM-QA, SocialIQA) is the closest thing to a public evaluation toolkit for "does this system track minds." The `All*` strict-consistency, explicit-vs-applied gap, and ATOMS per-ability breakdowns are directly importable into product evals.
- **What are we *not* doing?** The cautionary sources (Therabot, "AI psychosis," sycophancy, persona drift, 171-emotion causal coupling, applied-ToM failures) define a safety envelope every humanization product needs to respect. This category is also where "when to *dehumanize* the output" is defended — a differentiator.

Relationships to likely sibling categories:

- **Persona / character / voice** — this category's *mechanism* (Anthropic persona vectors, Assistant Axis, character training) grounds the surface layer.
- **Empathy / emotional intelligence** — treated here as a pipeline, not a vibe; the industry's four-step Cresta decomposition plus Hume's 48-emotion substrate are the canonical references.
- **Memory / context / personalization** — this category frames memory as a proxy for ToM (Replika, Character.AI, Pi) and argues cross-session user models are an underserved layer.
- **Agentic / multi-agent systems** — ToM is the coordination primitive (MindDial's three-level belief, CAMEL's role-playing pair, Sotopia's public/secret goals, MetaMind).
- **Evaluation / benchmarks / humanness scoring** — this category contains the most load-bearing specific benchmarks and the cleanest critique methodology (Soubki & Rambow's machine-validation bar).
- **Safety / alignment / AI psychosis / sycophancy** — the "richer ToM ≠ safer model" coupling is sharp here and constrains product tactics elsewhere.
- **Prompt engineering / humanize-AI recipes** — the practical-angle how-to cluster is directly operationalizable but under-validated.

---

## Recommended Reading Order

If you have an hour, read in this order:

1. **MIT Tech Review — "AI models can outperform humans in tests to identify mental states"** (2024-05-20). Calibrates the popular claim.
2. **Strachan et al., *Nature Human Behaviour* (2024).** The gold-standard behavioral result.
3. **Ullman (2023). "LLMs Fail on Trivial Alterations."** The counterweight.
4. **Gu et al. (2024). "SimpleToM."** The single most important result for humanization: explicit ≠ applied ToM.
5. **Kim et al. (2023). "FANToM."** Illusory ToM; the `All*` strict consistency score.
6. **Anthropic — "Claude's Character"** and **"Persona Vectors."** The industry's alignment framing and control surface.
7. **Melanie Mitchell — "LLMs and World Models, Parts 1 & 2."** The Andreas-taxonomy vocabulary.
8. **Gary Marcus — "How Not to Test GPT-3"** (with Davis). The contamination critique.
9. **Janus — "Simulators" (LessWrong).** The philosophical backbone of humanization prompts.
10. **Soubki & Rambow (2025). "Machine Theory of Mind Needs Machine Validation."** The 2025 methodological bar.

If you have a weekend, add in this order:

11. Chen et al., **ToMBench** (ACL 2024) — ATOMS 31-ability taxonomy.
12. Gandhi et al., **BigToM** (NeurIPS 2023) — procedural generation.
13. Sclar et al., **ExploreToM** (ICLR 2025) — adversarial generation + fine-tune transfer.
14. Zhu et al., **"Language Models Represent Beliefs of Self and Others"** (ICML 2024) — interpretability.
15. Sclar et al., **SymbolicToM** (ACL 2023 Outstanding) — symbolic-augmentation thesis.
16. Jin et al., **MMToM-QA** (ACL 2024 Outstanding) + **AutoToM** (NeurIPS 2025 Spotlight) — multimodal + Bayesian inverse planning.
17. Nguyen (2025) **"A Survey of Theory of Mind in LLMs"** (and Sarıtaş et al. companion survey) — field consolidation.
18. Anthropic — **"Assistant Axis"**, **"Introspection"**, **171 emotion concepts**.
19. Commercial anchors: **Cresta empathy pipeline**, **Hume EVI docs**, **Synthetic Users' "chain-of-feeling"**, **Pactum negotiation agents**, **Slingshot AI "foundation model for psychology."**
20. Practitioner: **LessWrong TOMI replication** + the **Humanize-AI how-to cluster** (chatsmith / openaiagent / moarpost / thehumanizeai).

---

## File Index

- **A-academic.md** — Peer-reviewed literature (2018–2025). 22 annotated papers covering foundational ToMnet, the Kosinski–Ullman debate, the second-generation benchmarks (BigToM, FANToM, Hi-ToM, OpenToM, ToMBench, SimpleToM, MMToM-QA), mitigations (SymbolicToM, PercepToM, SCALPEL), representation/mechanism work (Zhu et al.), and the 2025 meta-critiques (Soubki & Rambow; Nguyen survey; Sarıtaş survey).
- **B-industry.md** — Lab blogs and science journalism (24 posts). Anthropic (Claude's Character, Persona Vectors, Assistant Axis, Introspection, 171-emotion concepts, Trustworthy Agents), DeepMind (ToMnet origin, vision-alignment), MIT Tech Review, Quanta, Mitchell, Marcus, Alexander.
- **C-opensource.md** — 20+ GitHub repos plus one reading list. False-belief benchmarks (ToMi, Hi-ToM, OpenToM), procedural/adversarial (BigToM, ToMBench, ExploreToM), conversation-native (FANToM, SimpleToM, MMToM-QA, SocialIQA), meta (awesome-theory-of-mind), and social simulators (Generative Agents, genagents, Sotopia, AgentSims, CAMEL, ToM-RL, AutoToM, MuMA-ToM, SimulatedToM).
- **D-commercial.md** — 20+ shipping products across six segments: CX empathy (Cresta, ASAPP, Observe.AI, Uniphore, Cogito/Verint, Level AI), sales intent (Gong, Chorus, Outreach Kaia, Sybill), autonomous negotiation (Pactum), synthetic users (Synthetic Users, Synthetic Respondents, Ask Rally, FishDog, Twin Persona, BlockSurvey), coaching/companions (BetterUp, Slingshot Ash, Pi, Woebot, Wysa, Replika, Character.AI), affective sensing (Hume, Affectiva/Smart Eye, Valence), and workplace intent (Ema, Sana AI). Includes a curated marketing-grammar quote bank.
- **E-practical.md** — 17 practitioner threads / posts across HN, LessWrong, Reddit (r/MachineLearning, r/singularity, r/artificial, r/ArtificialSentience), Substack (Marcus, Mitchell, artificialintelligencer, daveshap, learnagentic), Medium / The Prompt Index, The Decoder, YouTube, plus the "Humanize AI" how-to cluster (chatsmith, openaiagent, thehumanizeai, moarpost). Captures the contamination↔emergence axis, CoT + world-rules recipe, persona drift, hedging-vs-decisiveness trade-off, vocabulary hygiene, and the self-ToM frontier.
