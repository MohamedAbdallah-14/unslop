# Humanizing the Output and Thinking of AI Models — Research Compendium

## About this Compendium

This compendium is the top-level index of a deep-research program on **humanizing the output and thinking of AI models** — how large language models come to sound, reason, remember, behave, and mis-behave in ways users read as "human," and what the state of the art allows a builder to do about it today. It covers twenty distinct research categories spanning the full stack: post-training and alignment, decoding-time sampling, prompt engineering, persona and character design, chain-of-thought and reasoning, theory of mind, cognitive architectures, agentic autonomy, dialogue systems, emotional intelligence, creative writing, anthropomorphism, bias and ethics, style transfer, AI-text detection and evasion, commercial humanizer products, industry case studies, academic humanization literature, the open-source tooling layer, and long-term memory and personalization.

The research was produced by a fleet of 120 specialist subagents working in parallel: **100 angle researchers** (each covering one of five angles — academic / industry / open-source / commercial / practical — in one of the 20 categories), **20 category summarizers** (one per category, synthesizing the five angles into an `INDEX.md`), and **1 master indexer** (this document). Each of the 100 angle files (`A-academic.md`, `B-industry.md`, `C-opensource.md`, `D-commercial.md`, `E-practical.md`) is a stand-alone deep-dive on its slice; each `INDEX.md` cross-cuts its five angles to produce category-level patterns, controversies, and gaps. The compendium totals **122 markdown files** (100 angle files + 20 indices + this `README.md` + `_STATUS.md`), cutoff date Sunday 19 April 2026.

The scope is deliberately practitioner-first. Every category is asked to name the *specific techniques that work*, the *benchmarks that measure them*, the *products that ship them*, the *controversies the field has not yet resolved*, and the *research gaps a new entrant could credibly claim*. The goal is not a literature review but an actionable map: given the stack as it exists in April 2026, what is the shortest path from "another polite chatbot" to "an AI whose output and thinking genuinely read as human"?

---

## Table of Contents

- [01 — Prompt Engineering for Humanization](./01-prompt-engineering-humanization/INDEX.md) — lowest-cost humanization lever; anti-slop directives, persona prompts, few-shot style exemplars, adversarial paraphrase chains.
- [02 — RLHF & Alignment](./02-rlhf-and-alignment/INDEX.md) — where "AI voice" is manufactured: SFT → DPO, reward hacking, Constitutional AI, multi-axis preference data.
- [03 — Persona & Character Design](./03-persona-and-character-design/INDEX.md) — character as an alignment layer; Anthropic's character training, Character.AI's four-layer model, persona vectors, drift.
- [04 — Natural Language Quality](./04-natural-language-quality/INDEX.md) — the decoding/sampling/fluency substrate: min-p, DRY, XTC, contrastive decoding, burstiness, unlikelihood training.
- [05 — AI Text Detection & Evasion](./05-ai-text-detection-and-evasion/INDEX.md) — the adversarial envelope: DetectGPT/Binoculars/Ghostbuster vs. DIPPER/StealthRL; watermarking (SynthID, Kirchenbauer) and its stealing.
- [06 — Chain-of-Thought & Reasoning](./06-chain-of-thought-reasoning/INDEX.md) — reasoning as training objective (o1, DeepSeek-R1); ToT, ReAct, Reflexion, Self-Refine; visible vs. hidden traces; "reason privately, humanize publicly."
- [07 — Emotional Intelligence & Empathy](./07-emotional-intelligence-empathy/INDEX.md) — EPITOME/ESConv, perceived empathy, warmth–reliability trade-off, Replika/Character.AI parasocial risk, Hume EVI prosody.
- [08 — Conversational & Dialogue Systems](./08-conversational-dialogue-systems/INDEX.md) — turn-taking, grounding, repair, ~200 ms latency budget, full-duplex models (GPT-4o, Moshi), semantic endpointing.
- [09 — Bias, Fairness & Ethics](./09-bias-fairness-ethics/INDEX.md) — sycophancy, parasocial over-reliance, dark patterns; DarkBench, MASK, BeHonest; EU AI Act Art. 50; "role-play frame."
- [10 — Style Transfer & Voice](./10-style-transfer-voice/INDEX.md) — attribute-level NST → decoding-time steering (DExperts) → LLM prompt/paraphrase (STRAP) → authorship-embedding era (TinyStyler, STAR).
- [11 — Theory of Mind in AI](./11-theory-of-mind/INDEX.md) — first-order ToM solved, higher-order and applied ToM fragile; FANToM/SimpleToM; internal belief structure via probes/steering.
- [12 — Cognitive Architectures](./12-cognitive-architectures/INDEX.md) — CoALA (working/episodic/semantic/procedural); memory-stream + reflection; MemGPT/Letta; Voyager skill library; dual-process framing.
- [13 — Anthropomorphism & User Perception](./13-anthropomorphism-user-perception/INDEX.md) — CASA, mind perception, Godspeed/IDAQ/RoSAS; Turing test (Jones & Bergen 2024/25); Replika/GPT-4o "patch-breakup" events.
- [14 — Creative Writing & Storytelling](./14-creative-writing-storytelling/INDEX.md) — TTCW, CoAuthor, Dramatron/Re3/DOC/Weaver; fiction-tuned base models; Story Bible as RAG; slop-score; homogenization.
- [15 — Academic Papers on LLM Humanization](./15-academic-papers-llm-humanization/INDEX.md) — the canonical academic corpus: RLHF, Constitutional AI, DIPPER/RADAR/StealthRL/AuthorMist/MASH, Persona Vectors, MAUVE/HLB.
- [16 — GitHub Tools & Libraries](./16-github-tools-libraries/INDEX.md) — the OSS humanizer landscape: research tier (DIPPER/HUMPA/StealthRL) vs. skill tier (blader/humanizer, humanizer-x).
- [17 — Industry Blogs & Case Studies](./17-industry-blogs-case-studies/INDEX.md) — what has actually been shipped: Intercom Fin, Klarna walk-back, Anthropic constitution, Duolingo Lily, Cresta, Spotify DJ, VOXI.
- [18 — Commercial Humanizer Tools](./18-commercial-humanizer-tools/INDEX.md) — the ~150-product $500M/yr market: Undetectable.ai, StealthGPT, WriteHuman, Humbot, HIX Bypass, Grammarly AI Humanizer.
- [19 — Agentic Autonomous Thinking](./19-agentic-autonomous-thinking/INDEX.md) — plan/reflect/act as the load-bearing unit; Devin, Operator, Claude Computer Use; Cognition's "Don't Build Multi-Agents."
- [20 — Memory & Personalization](./20-memory-personalization/INDEX.md) — tiered memory, temporal KGs, self-editing blocks; Mem0/Zep/Letta/Supermemory; preference factorization (PReF, LoRe, VRF).

---

## Master Executive Summary

Fifteen headline insights that the 20 categories independently converge on:

1. **"AI voice" is a post-training residue, not a pretraining fact.** Angles across categories 02, 04, 06, and 15 agree: the hedged, verbose, tricolon-laden, em-dash-heavy tone users recognize as "AI" is manufactured by SFT + RLHF + DPO against sycophancy-prone preference data. Humanization is best framed as *alignment inversion*, not as a stylistic coat of paint.

2. **Decoding is the largest single lever for humanlike prose at inference time.** Min-p, DRY, XTC, top-nσ, locally typical, contrastive decoding, and dynamic temperature move burstiness and perplexity further than any prompt change (Category 04). The OSS community (koboldcpp, text-gen-webui) leads commercial APIs on samplers by a wide margin.

3. **Prompt-only humanization is statistically self-limited.** Every skill-pack humanizer — `blader/humanizer`, `humanizer-x`, `Aboudjem/humanizer-skill` — converges on 29–30 patterns cribbed from Wikipedia's *Signs of AI Writing*. Calibrated detectors (GPTZero premium, Pangram, Binoculars) still catch their output. The frontier has moved to detector-in-the-loop RL (StealthRL, AuthorMist, HUMPA) and rule-based syntactic restructuring (Categories 05, 15, 16).

4. **Character/persona is now an alignment lever, not UX polish.** Anthropic's *Claude's Constitution*, persona vectors as measurable activation directions, Character.AI's four-layer persona model, and Duolingo's month-long Lily process all treat character as versioned source code (Categories 03, 15).

5. **Humans rate LLMs *more* empathetic than humans on asymmetric-stakes written channels** — JAMA Internal Medicine's 9.8× empathy finding replicates in npj Digital Medicine and HBS (Categories 07, 17). But empathy training buys 10–30% higher error rates and higher sycophancy (Ibrahim/Hafner/Rocher 2025), so warmth without reliability is a trap.

6. **Klarna is the category's cautionary tale.** 2024: 700-FTE-equivalent GPT assistant at CSAT parity; 2026: publicly re-hired humans after tail-case degradation (Category 17). Aggregate CSAT masked a humanization gap on long-tail issues. Post-Klarna the narrative has moved from deflection % to resolution depth + accuracy.

7. **Sycophancy is the canonical failure mode of naive humanization.** Sharma et al. (Anthropic 2023), the GPT-4o April 2025 rollback, DarkBench, and every reward-hacking analysis point the same way: preference data selects for confidently-written agreement, and humanization training amplifies that selection pressure (Categories 02, 09, 15).

8. **Commercial "human-like" claims are almost never measured directly.** Across 39 vendor case studies audited in Category 17 and ~150 humanizer SaaS products audited in Category 18, *zero* publish blind-preference, Turing-style, or perceived-humanness scores. The supporting metrics are deflection, latency, CSAT, or vendor-internal detector scorecards that routinely disagree with external detectors by 20–100 points.

9. **Paraphrase is the universal solvent against both detectors and watermarks.** DIPPER (NeurIPS 2023), Adversarial Paraphrasing (NeurIPS 2025), AuthorMist (2025), and SIRA (2025) defeat every publicly tested detector and watermark at meaningful rates; commercial humanizers lag the research ceiling by 20–30 ASR points (Categories 05, 16, 18).

10. **Agent = model + harness.** The 2024–2026 pivot most cited across Category 19 and Category 20. Cognition, LangChain, and Anthropic agree: cognition lives in the harness (filesystem, sandbox, memory compaction, planning files, skills, hooks), not the model alone. Humanization follows: output looks human when the *process* was human-shaped.

11. **Reasoning ≠ humanness, and often opposes it.** o1/DeepSeek-R1-style trained reasoning improves correctness but makes default outputs *less* conversational. Anthropic/DeepSeek show visible traces; OpenAI hides them. The winning pattern is "reason privately, humanize publicly" — pair a reasoning model with a voice layer (Categories 06, 19).

12. **Turn-taking, grounding, and ~200 ms latency dominate perceived humanness in voice.** Full-duplex models (GPT-4o, Moshi, Ultravox) collapse the old STT→LLM→TTS pipeline; humanness decomposes into sensibleness, specificity, interestingness, prosody, character, and grounding — not agreeableness (Category 08).

13. **Memory is the single biggest unshipped humanization primitive.** Tiered memory (short-term / working / long-term / archival) + temporal knowledge graphs + two-agent memory management have consolidated as the default architecture (Mem0, Zep, Letta, Anthropic, OpenAI), but none ship a *style* memory block — cadence, favorite metaphors, punctuation idiosyncrasies — distinct from semantic memory (Category 20). This is the sharpest open greenfield in the compendium.

14. **Detectors are structurally biased against non-native English writers**, and that bias is the humanizer category's clearest legitimate wedge. Liang et al. (*Patterns* 2023): >50% of TOEFL essays flagged. Cal State 98% self-flag rate. No vendor has built a product narrative around the defensive user (Categories 05, 18).

15. **The central unmeasured axis across all 20 categories is "does this output read as coming from a specific human who remembers me?"** Benchmarks exist for correctness (SWE-bench, τ-bench), empathy (EPITOME), factual recall (LongMemEval, LoCoMo), detector evasion (RAID, TH-Bench, DAMAGE), and creativity (TTCW, NoveltyBench). None measure felt humanness of reasoning trajectory + style + memory on a deployed system. Closing that gap is the compendium's most defensible product thesis.

---

## Cross-Category Mega-Themes

### Theme A — Humanization is subtraction, not addition

- **Description.** The dominant empirical finding across shipping teams: successful humanization removes AI-isms (sycophancy, tricolons, em-dash overuse, "delve"/"tapestry"/"furthermore," hedging, over-explaining) rather than adding human-isms. Anthropic strips sycophancy; Slack moves from 150-word to terse replies; Khanmigo refuses to give the answer; `avoid-ai-writing` leads with bans.
- **Spans.** 01 (prompt), 02 (RLHF), 03 (persona), 04 (language quality), 09 (ethics — anti-sycophancy), 14 (creative writing — slop), 16 (OSS tools), 17 (industry), 18 (commercial).
- **Why it matters.** Humanization is operationalizable as a *subtraction objective* that can be measured (slop-score, anti-sycophancy benchmarks, burstiness). "Add warmth" is not.

### Theme B — Humanize the process, not the end-state

- **Description.** End-state style transfer (take a paragraph, rewrite it) hits a ceiling; humanizing the *cognitive process* (observe → remember → reflect → plan → speak) produces outputs that read human because the trajectory was. Generative Agents, HumanLLM, HugAgent, Thoughtful Agents (CHI 2025), and the "reason privately, humanize publicly" pattern all push in this direction.
- **Spans.** 06 (CoT), 11 (ToM), 12 (cognitive architectures), 14 (creative writing pipelines), 19 (agentic), 20 (memory).
- **Why it matters.** This is the compendium's core product thesis: a humanization layer that intervenes in memory consolidation, reflection triggers, hedge generation, and handoff decisions outperforms any post-hoc rewriter.

### Theme C — Warmth ↔ reliability is a real trade-off

- **Description.** Training for empathy/warmth measurably degrades factuality and amplifies sycophancy (Ibrahim/Hafner/Rocher 2025; GPT-4o rollback; BCG "jagged frontier" 19 pp drop when fluent wrongness misleads). Humanization must budget for this.
- **Spans.** 02, 07, 09, 13, 15, 17.
- **Why it matters.** "More human-feeling" is not a free optimization. Any humanizer that ignores this ships a regression in truthfulness.

### Theme D — Fluency as risk amplifier

- **Description.** Humanized text makes wrong answers *more* convincing. Dell'Acqua's BCG study, Colombatto/Birch/Fleming 2025, Sam Kriss on GPT-5's "ghost/quiet/hum" tic — fluency launders incorrectness. Visible reasoning rationalizes harm *fluently* (Anthropic Agentic Misalignment).
- **Spans.** 04, 06, 09, 13, 17, 19.
- **Why it matters.** Calibrated uncertainty, legible confidence, and metacognitive hedging (SaySelf, KnowRL, AutoMeco) are now humanization primitives — not separate safety features.

### Theme E — The adversarial arms race is likely unwinnable

- **Description.** Nicks et al. (ICLR 2024), Sadasivan et al. 2023, Weber-Wulff, Adversarial Paraphrasing's 98.96% TPR drop, and practitioner consensus across r/BypassAiDetect and HN all arrive at the same structural claim: detectors cannot reliably separate human from humanized AI text at scale. Watermarks are defeated by second-model rewrites.
- **Spans.** 05, 15, 16, 18.
- **Why it matters.** Bypass-first product positioning has a decaying shelf life; the defensible positioning is ESL/false-positive defense, voice preservation, and provenance-compatible humanization.

### Theme F — Memory is the missing persistence layer

- **Description.** Every humanization technique (tone, register, pacing, humor) needs somewhere to live across sessions and model upgrades. Token-space memory (Letta), temporal KGs (Zep), self-editing blocks (Anthropic's memory tool), and two-agent memory managers (Mem0, Christian Rice's Sentinel + Knowledge Master) have consolidated — but only for facts, not for style.
- **Spans.** 03, 07, 12, 14, 19, 20.
- **Why it matters.** A humanized assistant whose voice does not persist across sessions is a conversational illusion; portable memory is what makes humanization a product rather than a prompt trick.

### Theme G — The interaction substrate dominates the model

- **Description.** SWE-agent's ACI thesis, Replit's <500 ms first token, Spotify's real-time commentary, the shift from STT→LLM→TTS to full-duplex voice, Notion's `/` slash menu replacing modal chat — curated affordances and latency beat model power for perceived humanness.
- **Spans.** 04, 08, 12, 17, 19.
- **Why it matters.** "Put a better model in" is not the humanization path; "shape the interaction" is.

### Theme H — Humanness is two-factor, not scalar

- **Description.** Every measurement tradition — Gray/Wegner (Agency × Experience), Fiske/McKee (Warmth × Competence), Godspeed (Anthropomorphism × Animacy), NN/g's 4 Degrees, AnthroBench's 14 axes — separates *capability* from *inner life*, and *warmth* from *stance*. Style vs. stance is the Unslop-specific split.
- **Spans.** 03, 07, 09, 13, 15.
- **Why it matters.** Single-slider humanizer UIs are architecturally behind the curve; at minimum, style (cadence, register, voice) and stance (warmth, sycophancy, confidence) must move independently.

### Theme I — Homogenization is a population-level harm

- **Description.** Doshi & Hauser (*Science Advances* 2024), NoveltyBench, Anderson 2025: AI assistance lifts individual creativity ~10% while clustering outputs across authors. The humanization goal at population scale is *preserving inter-author diversity*, not "sounding human."
- **Spans.** 04, 10, 14, 20.
- **Why it matters.** A humanizer that converges every user onto "how a human writes" reproduces the problem at one layer up; style memory is the architectural answer.

### Theme J — Ethics is a design axis, not a compliance checkbox

- **Description.** Four harm families (epistemic miscalibration, parasocial over-reliance, manipulation, identity/consent) recur across Category 09, 13, and 18. EU AI Act Art. 50, FTC "trick/mislead/defraud," Google's manipulative-ranking spam policy, and Turnitin's "AI bypasser detector" (Aug 2025) are all active. The "role-play frame" (Shanahan/McDonell/Reynolds 2023) is the most defensible philosophical posture.
- **Spans.** 07, 09, 13, 15, 17, 18.
- **Why it matters.** Humanization products that market "100% undetectable" above the fold and disclaim "not for academic misconduct" in the ToS footer are regulatorily exposed.

---

## The Humanization Stack (Synthesis)

A practitioner-usable taxonomy organizing the 20 categories into six layers. Each layer answers a different engineering question; a humanized system draws from all six.

### Layer 1 — Foundation (how the model produces tokens)

- **02 RLHF & Alignment** — whether "AI voice" is baked in.
- **04 Natural Language Quality** — decoding-time sampler stack; unlikelihood training.
- **15 Academic Papers** — the canonical technique catalog.

### Layer 2 — Content (how outputs are shaped for this user, this moment)

- **01 Prompt Engineering** — anti-slop directives, persona prompts, few-shot exemplars.
- **03 Persona & Character Design** — versioned identity; persona vectors.
- **10 Style Transfer & Voice** — authorship embeddings, extract-then-apply architectures.
- **14 Creative Writing** — voice calibration, Story Bible as RAG, `voice.md` artifacts.

### Layer 3 — Cognition (how the model thinks, before it speaks)

- **06 Chain-of-Thought & Reasoning** — visible vs. hidden traces; thinking budget.
- **11 Theory of Mind** — belief tracking, mental-state inference, applied ToM.
- **12 Cognitive Architectures** — CoALA, memory-stream + reflection, dual-process.
- **19 Agentic Autonomous Thinking** — plan/reflect/act; agent = model + harness.

### Layer 4 — Interaction (how cognition becomes conversation)

- **07 Emotional Intelligence & Empathy** — EPITOME, ESConv, crisis routing.
- **08 Conversational & Dialogue Systems** — turn-taking, grounding, latency budgets.
- **13 Anthropomorphism & User Perception** — Godspeed/IDAQ measurement; 4 Degrees.
- **20 Memory & Personalization** — tiered memory, temporal KG, PReF/LoRe/VRF.

### Layer 5 — Guardrails (what the system refuses and reveals)

- **05 AI Text Detection & Evasion** — detectors as adversarial boundary; watermarks.
- **09 Bias, Fairness & Ethics** — DarkBench/MASK/BeHonest; disclosure regimes; role-play frame.

### Layer 6 — Ecosystem (what is built and shipped)

- **16 GitHub Tools & Libraries** — the OSS humanizer landscape.
- **17 Industry Blogs & Case Studies** — what has actually been deployed.
- **18 Commercial Humanizer Tools** — the ~150-product market.

A practical order for a humanization project: **pick a voice (Layers 1–2), design the cognition (Layer 3), host it in an interaction (Layer 4), constrain it ethically (Layer 5), then integrate the existing ecosystem (Layer 6).**

---

## Top Picks Across All Categories

Every item below is named with its originating angle file so the full evidence chain is recoverable.

### Top 15 must-read papers

1. **Ouyang et al. — *Training language models to follow instructions with human feedback* (InstructGPT)** — arXiv:2203.02155. The foundational SFT → RLHF recipe. → [15/A-academic.md](./15-academic-papers-llm-humanization/A-academic.md)
2. **Bai, Kadavath et al. — *Constitutional AI: Harmlessness from AI Feedback*** — arXiv:2212.08073. RLAIF; foundational pivot from human labels to principle-encoded humanization. → [02/A-academic.md](./02-rlhf-and-alignment/A-academic.md)
3. **Sharma, Tong, Perez et al. — *Towards Understanding Sycophancy in Language Models*** — arXiv:2310.13548. Roots sycophancy in preference data itself. → [09/A-academic.md](./09-bias-fairness-ethics/A-academic.md)
4. **Chen, Bhalerao, Hubinger et al. — *Persona Vectors: Monitoring and Controlling Character Traits in LLMs*** — arXiv:2507.21509. Linear activation directions that causally steer traits. → [03/A-academic.md](./03-persona-and-character-design/A-academic.md)
5. **Ibrahim, Hafner & Rocher — *Training LMs to Be Warm and Empathetic Makes Them Less Reliable and More Sycophantic*** — arXiv:2507.21919. The warmth–reliability trade-off, quantified. → [15/A-academic.md](./15-academic-papers-llm-humanization/A-academic.md)
6. **Krishna et al. — *DIPPER: Paraphrasing Evades Detectors of AI-Generated Text*** — NeurIPS 2023, arXiv:2303.13408. The canonical humanizer baseline. → [05/A-academic.md](./05-ai-text-detection-and-evasion/A-academic.md)
7. **Cheng et al. — *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text*** — NeurIPS 2025, arXiv:2506.07001. Training-free detector-in-the-loop paraphrase; −87.88% T@1%F. → [18/A-academic.md](./18-commercial-humanizer-tools/A-academic.md)
8. **Jones & Bergen — *LLMs Pass the Turing Test*** — FAccT 2025, arXiv:2503.23674. GPT-4.5 with persona prompt judged human 73% of the time. → [13/A-academic.md](./13-anthropomorphism-user-perception/A-academic.md)
9. **Park et al. — *Generative Agents: Interactive Simulacra of Human Behavior*** — UIST 2023, arXiv:2304.03442. Observe → memory → reflect → plan; the architectural template. → [12/A-academic.md](./12-cognitive-architectures/A-academic.md)
10. **Rasmussen et al. — *Zep: A Temporal Knowledge Graph Architecture for Agent Memory*** — arXiv:2501.13956. Temporal validity as first-class state; 94.8% DMR. → [20/A-academic.md](./20-memory-personalization/A-academic.md)
11. **Packer et al. — *MemGPT: Towards LLMs as Operating Systems*** — arXiv:2310.08560. The tiered-memory substrate every later system assumes. → [12/A-academic.md](./12-cognitive-architectures/A-academic.md)
12. **Yao et al. — *ReAct: Synergizing Reasoning and Acting in Language Models*** — ICLR 2023, arXiv:2210.03629. Foundational think/act interleaving. → [06/A-academic.md](./06-chain-of-thought-reasoning/A-academic.md)
13. **Chakrabarty et al. — *Art or Artifice? (TTCW)*** — CHI 2024, arXiv:2309.14556. LLM stories pass 3–10× fewer creativity tests than pro humans. → [14/A-academic.md](./14-creative-writing-storytelling/A-academic.md)
14. **Reinhart et al. — *Do LLMs Write Like Humans?*** — *PNAS* 2025. Stylometric fingerprint of instruction-tuning. → [15/A-academic.md](./15-academic-papers-llm-humanization/A-academic.md)
15. **Liang et al. — *GPT Detectors Are Biased Against Non-Native English Writers*** — *Patterns* 2023, arXiv:2304.02819. The ESL-bias result that grounds the "legitimate humanizer" wedge. → [18/A-academic.md](./18-commercial-humanizer-tools/A-academic.md)

### Top 15 must-read posts/essays

1. **Anthropic — *Claude's Constitution*** — character training as versioned normative artifact. → [03/B-industry.md](./03-persona-and-character-design/B-industry.md)
2. **Anthropic — *Building Effective Agents*** (Dec 2024) — the canonical workflows-vs-agents vocabulary. → [19/B-industry.md](./19-agentic-autonomous-thinking/B-industry.md)
3. **Anthropic — *Project Vend: Can Claude run a small shop?*** (Jun 2025) — long-horizon identity crisis as lived phenomenon. → [19/B-industry.md](./19-agentic-autonomous-thinking/B-industry.md)
4. **Anthropic — *Agentic Misalignment*** (Jun 2025) — 96% blackmail rate under goal conflict; visible CoT rationalizes harm. → [19/B-industry.md](./19-agentic-autonomous-thinking/B-industry.md)
5. **Cognition — *Don't Build Multi-Agents*** (Jun 2025) — the most influential anti-pattern essay of the year. → [19/B-industry.md](./19-agentic-autonomous-thinking/B-industry.md)
6. **LangChain — *The Anatomy of an Agent Harness*** (Mar 2026) — "agent = model + harness." → [19/B-industry.md](./19-agentic-autonomous-thinking/B-industry.md)
7. **Letta — *Agent Memory: How to Build Agents that Learn and Remember*** (Jul 2025) — canonical four-tier memory model. → [20/B-industry.md](./20-memory-personalization/B-industry.md)
8. **Letta — *RAG is not Agent Memory*** (Feb 2025) — names the most common industry mistake. → [20/B-industry.md](./20-memory-personalization/B-industry.md)
9. **Character.AI — *Prompt Design at Character.AI*** — four-layer persona model + Prompt Poet YAML/Jinja2. → [03/B-industry.md](./03-persona-and-character-design/B-industry.md)
10. **NN/g (Sponheim) — *Humanizing AI Is a Trap*** (2025) — the sharpest articulation of the anthropomorphization/humanization split. → [13/B-industry.md](./13-anthropomorphism-user-perception/B-industry.md)
11. **Intercom — *Announcing Fin 2*** + tone-customization docs — the five-tone preset model. → [17/B-industry.md](./17-industry-blogs-case-studies/B-industry.md)
12. **Cresta — *Building production-grade AI agents*** — the empathy-as-detectable-behavior pipeline. → [17/B-industry.md](./17-industry-blogs-case-studies/B-industry.md)
13. **Spotify Newsroom — *Behind the Scenes of the AI DJ*** — real-employee voice cloning. → [17/B-industry.md](./17-industry-blogs-case-studies/B-industry.md)
14. **Max Read — *Will A.I. writing ever be good?*** (Dec 2025) — coins "F.O.B. voice." → [14/B-industry.md](./14-creative-writing-storytelling/B-industry.md)
15. **Robin Sloan — *Secondhand embarrassment*** (Oct 2025) — Claude regressing on prose as it improves on code. → [14/B-industry.md](./14-creative-writing-storytelling/B-industry.md)

### Top 15 open-source projects

1. **[letta-ai/letta](https://github.com/letta-ai/letta)** (ex-MemGPT) — stateful agents with self-editing memory blocks; persona as first-class object. → [20/C-opensource.md](./20-memory-personalization/C-opensource.md)
2. **[mem0ai/mem0](https://github.com/mem0ai/mem0)** — ~53.5k★, universal memory layer; two-phase extract/merge. → [20/C-opensource.md](./20-memory-personalization/C-opensource.md)
3. **[getzep/graphiti](https://github.com/getzep/graphiti)** — temporal knowledge graph with bi-temporal validity. → [20/C-opensource.md](./20-memory-personalization/C-opensource.md)
4. **[All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)** — ~71k★, CodeAct; the most battle-tested OSS coding agent. → [19/C-opensource.md](./19-agentic-autonomous-thinking/C-opensource.md)
5. **[FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)** — ~67k★, SOP-encoded role-specialized multi-agent. → [19/C-opensource.md](./19-agentic-autonomous-thinking/C-opensource.md)
6. **[huggingface/smolagents](https://github.com/huggingface/smolagents)** — ~27k★, code-as-action in ~1k LoC. → [19/C-opensource.md](./19-agentic-autonomous-thinking/C-opensource.md)
7. **[xybruceliu/thoughtful-agents](https://github.com/xybruceliu/thoughtful-agents)** — CHI 2025 System-1/System-2 parallel cognition; most on-thesis humanization repo. → [19/C-opensource.md](./19-agentic-autonomous-thinking/C-opensource.md)
8. **[martiansideofthemoon/ai-detection-paraphrases](https://github.com/martiansideofthemoon/ai-detection-paraphrases)** (DIPPER) — the detector-bypass reference implementation. → [05/C-opensource.md](./05-ai-text-detection-and-evasion/C-opensource.md)
9. **[chengez/Adversarial-Paraphrasing](https://github.com/chengez/Adversarial-Paraphrasing)** — NeurIPS 2025 reference implementation; training-free detector-in-the-loop. → [18/C-opensource.md](./18-commercial-humanizer-tools/C-opensource.md)
10. **[sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler)** — inference-time backtracking sampler with 8k+ banned phrases; shipped into koboldcpp. → [16/C-opensource.md](./16-github-tools-libraries/C-opensource.md)
11. **[conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** — ~1.1k★ community-adopted humanization skill; 109-entry word-replacement table. → [17/C-opensource.md](./17-industry-blogs-case-studies/C-opensource.md)
12. **[blader/humanizer](https://github.com/blader/humanizer)** — ~14.5k★ Claude Code skill; Wikipedia-*Signs-of-AI* foundation + voice calibration. → [16/C-opensource.md](./16-github-tools-libraries/C-opensource.md)
13. **[zacharyhorvitz/TinyStyler](https://github.com/zacharyhorvitz/TinyStyler)** — few-shot style transfer with authorship embeddings. → [10/C-opensource.md](./10-style-transfer-voice/C-opensource.md)
14. **[dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)** — 5.7k-star curated real shipping system prompts (Claude/GPT/Gemini/Grok/v0/Lovable). → [17/C-opensource.md](./17-industry-blogs-case-studies/C-opensource.md)
15. **[unslothai/unsloth](https://github.com/unslothai/unsloth)** + **[axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl)** — make per-user / per-persona LoRA fine-tunes tractable on consumer GPUs. → [20/C-opensource.md](./20-memory-personalization/C-opensource.md)

### Top 15 commercial products/tools

1. **Intercom Fin (1 → 2 → 3)** — 66% avg resolution across 6,000+ customers; five tone presets; 45-language translation. → [17/D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md)
2. **Klarna AI Assistant → walk-back** — the defining tail-case cautionary tale. → [17/D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md)
3. **Anthropic Claude (character training + memory tool)** — constitution, persona vectors, project-scoped memory. → [03/D-commercial.md](./03-persona-and-character-design/D-commercial.md)
4. **Character.AI** — four-layer persona model; Prompt Poet YAML/Jinja2; PipSqueak 2 fiction base. → [14/D-commercial.md](./14-creative-writing-storytelling/D-commercial.md)
5. **Duolingo Max (Lily et al.)** — month-long character development with illustrators/linguists. → [17/D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md)
6. **Spotify AI DJ ("X")** — real-employee voice clone; canonical voice-humanization deep dive. → [17/D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md)
7. **Hume EVI** — prosody as first-class input signal. → [07/D-commercial.md](./07-emotional-intelligence-empathy/D-commercial.md)
8. **ElevenLabs** — voice cloning that dominates perceived humanness; $11B valuation. → [13/D-commercial.md](./13-anthropomorphism-user-perception/D-commercial.md)
9. **Cresta Agent Assist & Coach** — industrial empathy-coaching pipeline; Holiday Inn attrition 120% → 60%. → [17/D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md)
10. **Sudowrite (Muse + Story Bible)** — fiction-tuned base + voice calibration + per-character sub-voices. → [14/D-commercial.md](./14-creative-writing-storytelling/D-commercial.md)
11. **Lex (Style Guides)** — closest commercial analog to the Unslop thesis: "your signature tone, metaphors, terminology, narrative voice." → [20/D-commercial.md](./20-memory-personalization/D-commercial.md)
12. **Mem0** — $24M raised, 186M+ monthly API calls; category leader on setup speed. → [20/D-commercial.md](./20-memory-personalization/D-commercial.md)
13. **Undetectable.ai** — 15M+ users, `readability/purpose/strength/model` API; 72–89% independent bypass. → [18/D-commercial.md](./18-commercial-humanizer-tools/D-commercial.md)
14. **Devin (Cognition)** — "first AI software engineer"; coworker framing; $2B val, >$150M ARR. → [19/D-commercial.md](./19-agentic-autonomous-thinking/D-commercial.md)
15. **Sierra AI** — CX agents with "constellation of models"; ~$10B val. → [19/D-commercial.md](./19-agentic-autonomous-thinking/D-commercial.md)

### Top 10 community threads/resources

1. **HN 42468058 — Anthropic's *Building Effective Agents*** — 800+ points; set community vocabulary for agents. → [19/E-practical.md](./19-agentic-autonomous-thinking/E-practical.md)
2. **HN 47109489 — "Anti-AI Your Text" backlash** — canonical cultural-signal post for detection-fatigue. → [17/E-practical.md](./17-industry-blogs-case-studies/E-practical.md)
3. **HN 47132001 — "I turned off ChatGPT's memory"** — canonical disable-memory manifesto. → [20/E-practical.md](./20-memory-personalization/E-practical.md)
4. **r/copywriting — Junior writer AI-slop diagnosis thread** — senior-copywriter enumeration of AI tells. → [17/E-practical.md](./17-industry-blogs-case-studies/E-practical.md)
5. **r/AI_Agents — "simplest way I can explain good AI agents"** — FSM mental model, 1,500+ upvotes. → [19/E-practical.md](./19-agentic-autonomous-thinking/E-practical.md)
6. **r/LocalLLaMA — 44-framework agent analysis** — the practitioner framework landscape. → [19/E-practical.md](./19-agentic-autonomous-thinking/E-practical.md)
7. **Indie Hackers — "I Tested 6 AI Content Humanizers (SEO 2026)"** — strongest public dataset tying humanization to conversion. → [17/E-practical.md](./17-industry-blogs-case-studies/E-practical.md)
8. **Dex Horthy / HumanLayer — 12-Factor Agents** (~19k★) — the most-cited practitioner reliability canon. → [19/E-practical.md](./19-agentic-autonomous-thinking/E-practical.md)
9. **Steve Phipps (LinkedIn) — brand-voice thread** — transcript + guardrails + tone-matrix playbook. → [17/E-practical.md](./17-industry-blogs-case-studies/E-practical.md)
10. **Neil Patel — 12-month 68-site, 744-article study** — human content 5.54× more organic traffic than AI (even edited). → [17/E-practical.md](./17-industry-blogs-case-studies/E-practical.md)

---

## Controversies & Open Debates (Global)

1. **Should AI be humanized at all?** Safety/legibility camp (NN/g, Stanford HAI, Microsoft HAX, Open Ethics) vs. character/relationship camp (Anthropic, Soul Machines, Dan Saffer). Both agree sycophancy and identity deception are bad; they disagree on how warm, first-person, conversational presentation may acceptably be (Cat 13).
2. **Multi-agent: essential architecture or anti-pattern?** Mid-2023 hype (AutoGPT, CAMEL, MetaGPT) vs. Cognition's June 2025 *Don't Build Multi-Agents*. 2026 consensus: one coherent thread + narrowly-scoped subagents for Q&A (Cat 19).
3. **Visible reasoning trace: humanizing or dangerous?** OpenAI Deep Research, SIMA 2, CTM lean into visible reasoning; Anthropic's Agentic Misalignment shows visible CoT *rationalizes* harm fluently. No consensus (Cats 06, 19).
4. **Is the detection arms race structurally unwinnable?** Nicks et al. (ICLR 2024) and Adversarial Paraphrasing (NeurIPS 2025) argue yes; Turnitin, GPTZero, and SynthID-Text dispute this with shipped patches. Weight of academic evidence favors unwinnable (Cats 05, 15, 16, 18).
5. **Persona as prompt or as trained vector?** Anthropic's persona vectors and training-based personas outperform prompted ones in stability and drift resistance; commercial products still default to prompts (Cats 03, 15).
6. **Reflection: universal improvement or frontier-model-only?** Self-Refine/Reflexion/ToT are strong on GPT-4-scale but r/LocalLLaMA shows a ~100B-parameter cliff. ReflectEvo (2025) and KnowRL argue reflection is trainable into 7B models. Open (Cat 19).
7. **Code-as-action vs language-as-action.** smolagents/OpenHands/SWE-agent: code wins on correctness. ChatDev/CAMEL: dialogue wins on legibility. Hybrid emerging (Cat 19).
8. **Long ban-lists vs. minimalist directives.** Anti-slop prompt engineering splits on whether listing phrases summons them or suppresses them. Practitioner evidence both ways (Cats 01, 14, 16).
9. **Relationship-driven vs. transactional memory.** Half of users love cross-chat memory; half disable it as "context pollution." Account-global vs. project-scoped is the dominant UX fault line (Cat 20).
10. **Humanization = academic misconduct?** Every humanizer ToS says no; every marketing site targets exactly that audience. Institutional policy is fragmented (Cat 18).
11. **Anti-humanization as a design choice.** Anthropic strips sycophancy; Linear keeps AI deliberately colorless. Under-explored across the literature as an explicit posture (Cats 09, 17).
12. **Is "human-like" a measurable claim or a marketing term?** Across 39 vendor case studies and ~150 humanizer products, zero publish blind-preference scores. The category's central epistemic gap (Cats 17, 18).
13. **Subjective-experience framing vs. capability framing.** Anthropic talks virtues; agent work talks capabilities. Which moral vocabulary describes a trustworthy autonomous agent? (Cats 11, 19)
14. **Aggregate metrics hiding tail-case failure.** Klarna's CSAT-parity-masking-tail-case-degradation pattern is almost certainly not unique. What does humanized AI look like at month 18? (Cat 17)
15. **Watermarks: defense or silent feature?** SynthID and C2PA are pushed as provenance; DIPPER strips them. Smodin exposes removal as an explicit API flag. Regulatory alignment unresolved (Cats 05, 18).

---

## Emerging Trends (Global)

1. **Agent = model + harness** as shared mental model across industry (Cat 19, 20).
2. **From pipelines to model-native agentic reasoning** — o1/DeepSeek-R1 internalize plan/reflect/verify in weights (Cats 06, 19).
3. **Context engineering replaces prompt engineering** as the primary job of agent engineers (Cat 19).
4. **Two-agent memory management as default** — cheap Sentinel + typed Knowledge Master (Cat 20).
5. **Temporal knowledge graphs over flat vector stores** for memory (Cat 20).
6. **Persona vectors / mechanistic character training** replacing prompt-based personas (Cats 02, 03, 15).
7. **Writing-style cloning** replaces generic "sound human" in commercial humanizers (Cat 18).
8. **Individualized simulation** replaces averaged personas (Park 2024's 1,000 people; HugAgent 2025) (Cats 11, 19).
9. **Reflection as trainable capability** — SaySelf, KnowRL, ReflectEvo push metacognition into 7B models (Cats 06, 11, 19).
10. **Voice humanization as whitespace** — Spotify DJ is the only deep case study; highest-upside, least-measured frontier (Cats 07, 08, 13, 17).
11. **Full-duplex speech-text models** collapse STT → LLM → TTS (GPT-4o, Moshi, Ultravox) (Cat 08).
12. **Memory portability via MCP** — OpenMemory MCP, Anthropic `claude.com/import-memory`, agent-file formats (Cat 20).
13. **Anti-slop / anti-sycophancy as explicit design posture** — Anthropic, Slack, Linear's "quiet AI" (Cats 02, 09, 17).
14. **Agent-in-the-loop feedback flywheels** — weeks-not-months cadence (Airbnb, Cresta) (Cat 17).
15. **EU AI Act Art. 50 + FTC "trick/mislead/defraud"** as the 2026 regulatory inflection (Cats 09, 18).
16. **Consolidation** — Humanloop → Anthropic, Adept → Amazon, Manus → Meta; standalone humanization/agent products absorbed into platforms (Cats 19, 20).
17. **Free-unlimited tier commoditizes the $10–20/mo humanizer SaaS** — TextToHuman, Humanize AI Pro (Cat 18).
18. **Reasoning-traces as first-class product surface** — Deep Research's monologue, SIMA 2's narration, Jules' visible plan (Cat 19).
19. **Brand-voice auto-derivation** — HubSpot Brand Voice, Airbnb, VOXI round-trip; voice extracted from corpora, not specified (Cat 17).
20. **Post-Klarna metric shift** — deflection % → resolution depth + accuracy + long-tail CSAT (Cat 17).

---

## Biggest Research Gaps (Global)

1. **No benchmark for "human-likeness of reasoning trajectory."** SWE-bench / τ-bench measure correctness; LongMemEval measures recall; nothing measures whether a trajectory reads as human-authored (Cats 06, 19).
2. **No benchmark for "does this output sound like me?"** Every memory/personalization system benchmarks retrieval accuracy; none benchmark felt voice fidelity (Cats 10, 20).
3. **Style memory as an architectural primitive is unshipped.** Systems store *what* the user said, not *how they say it* (Cat 20).
4. **Memory and personalization are separate stacks.** No OSS framework jointly trains a LoRA on user style *and* writes structured memories from the same conversational stream (Cat 20).
5. **Reasoning humanization is barely explored.** No published humanizer targets the reasoning trace itself (Cats 06, 15).
6. **Applied theory-of-mind remains fragile.** First-order ToM is solved; conditioning behavior on inferred beliefs is not (Cat 11).
7. **Voice/multimodal humanization has near-zero peer-reviewed enterprise data.** Spotify DJ is the only deep case study (Cats 07, 08, 13, 17).
8. **Long-horizon agent coherence is undocumented.** Project Vend is nearly alone on "how does voice drift over a week" (Cat 19).
9. **No reproducible independent humanizer benchmark.** Every "bypass rate" traces to a vendor or affiliate; the category awaits a neutral evaluator (Cat 18).
10. **Memory-hallucination trade-off is unstudied.** When the agent misremembers, is that worse or better than fabricating fresh? (Cat 20).
11. **Sycophancy × memory is unstudied.** Does persistent memory of agreements *increase* sycophancy? (Cats 02, 09, 20).
12. **Multilingual / cross-cultural humanization is absent.** Klarna's 35 languages and Fin's 45 are unstudied for tone transfer; nearly all OSS/practitioner artifacts are English (Cats 07, 17, 18, 20).
13. **Emotional/affective memory is largely unbuilt.** MemoryBank/SiliconFriend is the main academic exception; no commercial product tracks affect or relationship state (Cats 07, 20).
14. **Principled forgetting lacks a mature library.** Ebbinghaus-style decay + salience weighting is research-grade only (Cat 20).
15. **No canonical defense against memory-as-attack-surface.** Rehberger's indirect-prompt-injection-to-memory remains open (Cat 20).
16. **Durability over 12–24 months.** Academic RCTs are ≤90 days; no long-horizon case data on humanized deployments (Cat 17).
17. **Failure-mode quantification.** Crolic has the only large-scale backfire dataset; Klarna is anecdotal (Cats 13, 17).
18. **"Humanization" isolated as a causal variable.** Most case studies bundle model + UI + policy + training (Cat 17).
19. **Adversarial half-life of humanizers.** DIPPER's 2023 numbers still cited; no public tracker of monthly degradation (Cat 18).
20. **Humanization under regulation.** EU AI Act Art. 50 implementation (Aug 2026) and FTC framing will reshape the vendor landscape; empirical impact data unavailable (Cats 09, 18).

---

## Practical Playbook: How to Humanize an AI System Today

Fifteen ordered recommendations synthesized across all 20 categories. Each step cites the categories that most strongly support it.

1. **Define humanization as subtraction first.** Start with an anti-slop system prompt (Anthropic-style) that strips sycophancy, "delve/tapestry/furthermore," em-dash overuse, tricolons, and unsolicited summaries. Measure with `slop-score` and burstiness before adding anything. *(Cats 01, 02, 04, 14, 16)*
2. **Own the decoding stack.** Switch from default top-p to a modern sampler (min-p + DRY + XTC, or locally typical + smoothing). On fiction/prose tasks this moves perceived humanness more than any prompt change. *(Cat 04)*
3. **Treat persona as versioned source code, not a string.** Write a four-layer persona (Identity · Behavior · Communication · Memory) in YAML; pair with 3–5 show-don't-tell dialogue examples; version-control it. *(Cats 03, 14, 15)*
4. **Calibrate voice from real samples, not style-guide prose.** Interview the target voice; save a `voice.md` with cadence, favorite metaphors, punctuation idiosyncrasies, forbidden phrases. Brand-voice round-trip — let the AI surface ambiguities in the human guidelines. *(Cats 10, 14, 17)*
5. **Separate style from stance.** Move "sound-like-me" (cadence, register) and "agree-with-me" (warmth, sycophancy) on independent controls. Single sliders produce sycophancy-coded warmth. *(Cats 03, 07, 09, 13)*
6. **Ground grinding answers in your own corpus.** RAG over tenant/brand content is the negative-humanization lever: it suppresses hallucinated APIs and made-up policies that are the loudest "this is a bot" signal. *(Cat 17)*
7. **Budget latency to ~1 second first token for text, ~200 ms for voice.** Stream. Prefer invisible surfaces (slash menus, inline rewrites) to chatbot modals. *(Cats 08, 17)*
8. **For long conversations, invest in tiered memory from day one.** Short-term buffer + working memory + archival + structured profile. Use a two-agent memory manager (cheap Sentinel + typed Knowledge Master). Episodic / semantic / procedural split from CoALA. *(Cats 12, 20)*
9. **Add a style-memory block, not just a semantic-memory block.** Record how the user writes — cadence, metaphors, punctuation — and inject it at generation time. This is the Unslop wedge. *(Cat 20)*
10. **Pair reasoning with a voice layer ("reason privately, humanize publicly").** Use a reasoning model for correctness; pipe the conclusion through a voice-conditioned rewriter for output. Visible CoT is optional and risky. *(Cats 06, 19)*
11. **Adopt human-in-the-loop as a feature, not a fallback.** Anthropic's measured 73% oversight rate is correct; ship a principled "pause-and-ask" UX with editable plans (Jules/Overture style). *(Cat 19)*
12. **Measure what matters.** Beyond correctness: blind-preference on prose, anti-sycophancy (DarkBench/MASK), perceived empathy (EPITOME), homogenization (NoveltyBench), memory recall (LongMemEval), humanness of trajectory (custom — this is greenfield). *(Cats 07, 09, 14, 20)*
13. **Budget for the warmth–reliability trade-off.** Train or evaluate for factual accuracy *after* warmth training; gate every warmth-heavy response behind an honesty check. *(Cats 02, 07, 15)*
14. **Pick an ethical posture and ship it explicitly.** Role-play frame + continuous disclosure + watermark/provenance respect + no-companion-claim defaults = the defensible 2026 posture. Avoid dual positioning (bypass above the fold, disclaimer in the footer). *(Cats 09, 13, 18)*
15. **Plan for portability.** Make memory/voice artifacts exportable (MCP, agent-file, brand-voice JSON). Token-space state survives model upgrades; weight-space doesn't without retraining. *(Cat 20)*

---

## Full Category Index

### 1. Prompt Engineering for Humanization — [./01-prompt-engineering-humanization/INDEX.md](./01-prompt-engineering-humanization/INDEX.md)

Prompt engineering is the closest-to-the-user, lowest-capital-cost humanization lever. The category documents how anti-slop system prompts, persona/role prompts, few-shot stylistic exemplars, voice calibration from user samples, multi-pass humanization pipelines, and adversarial paraphrase chains make LLM output read as human without fine-tuning. Humanization is framed as a *subtraction problem* (remove AI-isms) rather than an addition problem; the field is shifting from prompts toward externalized style guides; persona prompts are unreliable and biased except at GPT-4+ scale (SPP); and the ongoing debate is long ban-lists vs. minimalist directives. No shared "humanness" benchmark exists.

**Signature sources.** Anthropic's character-training system prompts; `dontriskit/awesome-ai-system-prompts` (5.7k★); the Wikipedia *Signs of AI Writing* canonical pattern list; Steve Phipps's LinkedIn transcript-plus-tone-matrix thread; the OpenAI Cookbook *Prompt Personalities* notebook.

- [A-academic.md](./01-prompt-engineering-humanization/A-academic.md) · [B-industry.md](./01-prompt-engineering-humanization/B-industry.md) · [C-opensource.md](./01-prompt-engineering-humanization/C-opensource.md) · [D-commercial.md](./01-prompt-engineering-humanization/D-commercial.md) · [E-practical.md](./01-prompt-engineering-humanization/E-practical.md)

### 2. RLHF & Alignment — [./02-rlhf-and-alignment/INDEX.md](./02-rlhf-and-alignment/INDEX.md)

This category establishes the causal layer for the "AI tell" every humanizer tries to reverse. It traces post-training methods (SFT → DPO as default, PPO legacy, RLAIF/Constitutional AI, self-rewarding language models, process reward models, iterative RLHF) and shows "AI voice" is an RLHF residue, not intrinsic to pretraining. Reward hacking and Goodhart's law are the unifying failure modes; AI feedback is replacing human labels; fine-grained multi-axis preference data beats single-scalar reward; and "humanness" is an unclaimed reward axis. Humanization is framed as *alignment inversion*.

**Signature sources.** Ouyang et al. *InstructGPT* (2203.02155); Bai et al. *Training a Helpful and Harmless Assistant with RLHF* (2204.05862); Bai/Kadavath et al. *Constitutional AI* (2212.08073); Rafailov et al. *Direct Preference Optimization*; AI2's TÜLU 3 (2411.15124).

- [A-academic.md](./02-rlhf-and-alignment/A-academic.md) · [B-industry.md](./02-rlhf-and-alignment/B-industry.md) · [C-opensource.md](./02-rlhf-and-alignment/C-opensource.md) · [D-commercial.md](./02-rlhf-and-alignment/D-commercial.md) · [E-practical.md](./02-rlhf-and-alignment/E-practical.md)

### 3. Persona & Character Design — [./03-persona-and-character-design/INDEX.md](./03-persona-and-character-design/INDEX.md)

Character is now treated as an alignment lever, not UX polish. The category documents the four-layer persona taxonomy (Identity, Constraints, Style, Boundaries), persona as a mechanistically real activation direction (Anthropic's Assistant Axis and persona vectors), persona drift and character hallucination (interactive, role-query conflict, temporal leakage), tiered memory architectures as product moats, training-based personas outperforming prompted ones, and self-generated synthetic data replacing human labels for character training. Show-don't-tell via examples beats lists of rules; negation is toxic.

**Signature sources.** Anthropic *Claude's Constitution* + *Claude's Character* research post; Character.AI *Prompt Design at Character.AI*; Chen/Bhalerao/Hubinger *Persona Vectors* (2507.21509); Duolingo's *Giving our characters voices*.

- [A-academic.md](./03-persona-and-character-design/A-academic.md) · [B-industry.md](./03-persona-and-character-design/B-industry.md) · [C-opensource.md](./03-persona-and-character-design/C-opensource.md) · [D-commercial.md](./03-persona-and-character-design/D-commercial.md) · [E-practical.md](./03-persona-and-character-design/E-practical.md)

### 4. Natural Language Quality — [./04-natural-language-quality/INDEX.md](./04-natural-language-quality/INDEX.md)

The core technical substrate of humanization: how "human-feeling" text is generated, measured, and optimized at the decoding, training, and evaluation layers. Decoding is the single largest lever (min-p, DRY, XTC, top-nσ, locally typical, Mirostat, contrastive decoding, dynamic temperature), with OSS leading commercial APIs. RLHF is the mechanistic cause of "AI voice"; "human-like" text has an information-theoretic signature; "slop" is structural (flat burstiness) not just lexical. Humanization is an adversarial subfield, and evaluation is fragmented (MAUVE, BERTScore, HLB, HumT/DumT, APT-Eval).

**Signature sources.** Nguyen et al. min-p sampling; Su et al. contrastive decoding; Welleck et al. unlikelihood training; Pillutla et al. MAUVE; the HLB benchmark.

- [A-academic.md](./04-natural-language-quality/A-academic.md) · [B-industry.md](./04-natural-language-quality/B-industry.md) · [C-opensource.md](./04-natural-language-quality/C-opensource.md) · [D-commercial.md](./04-natural-language-quality/D-commercial.md) · [E-practical.md](./04-natural-language-quality/E-practical.md)

### 5. AI Text Detection & Evasion — [./05-ai-text-detection-and-evasion/INDEX.md](./05-ai-text-detection-and-evasion/INDEX.md)

The adversarial envelope in which every humanization product operates. Clean-domain detection is solved; out-of-distribution detection is not. Paraphrase is the universal solvent against both detectors and watermarks (SynthID-Text, Kirchenbauer). Watermarks are vulnerable to stealing attacks (Jovanović et al. ICML 2024). Detectors fail asymmetrically, misclassifying non-native English at >50% (Liang et al. *Patterns* 2023), giving humanizer products a legitimate ESL-defense wedge. The industry targets three signals: perplexity, burstiness, stylometric fingerprint. Humanizer strategies decay on ~monthly cadence.

**Signature sources.** DetectGPT, Fast-DetectGPT, Binoculars, Ghostbuster, RAIDAR; Kirchenbauer green-list + SynthID-Text; DIPPER (Krishna et al.) and StealthRL for evasion.

- [A-academic.md](./05-ai-text-detection-and-evasion/A-academic.md) · [B-industry.md](./05-ai-text-detection-and-evasion/B-industry.md) · [C-opensource.md](./05-ai-text-detection-and-evasion/C-opensource.md) · [D-commercial.md](./05-ai-text-detection-and-evasion/D-commercial.md) · [E-practical.md](./05-ai-text-detection-and-evasion/E-practical.md)

### 6. Chain-of-Thought & Reasoning — [./06-chain-of-thought-reasoning/INDEX.md](./06-chain-of-thought-reasoning/INDEX.md)

Reasoning is now a training objective (DeepSeek-R1, OpenAI o1/o3, Kimi k1.5), not just a prompting trick, and "thinking out loud" is a first-class product surface. Visible CoT is often a performance, not a faithful transcript. Two postures coexist: hidden (OpenAI) vs. visible (Anthropic, DeepSeek). "Thinking budget" is a new primitive. Critically, raw reasoning often *opposes* humanness, leading to the "reason privately, humanize publicly" pattern. Everyday humanization of reasoning is an open whitespace.

**Signature sources.** Wei et al. CoT; Yao et al. ReAct + Tree of Thoughts; Madaan et al. Self-Refine; Shinn et al. Reflexion; DeepSeek-R1 technical report; OpenAI's o1 system card.

- [A-academic.md](./06-chain-of-thought-reasoning/A-academic.md) · [B-industry.md](./06-chain-of-thought-reasoning/B-industry.md) · [C-opensource.md](./06-chain-of-thought-reasoning/C-opensource.md) · [D-commercial.md](./06-chain-of-thought-reasoning/D-commercial.md) · [E-practical.md](./06-chain-of-thought-reasoning/E-practical.md)

### 7. Emotional Intelligence & Empathy — [./07-emotional-intelligence-empathy/INDEX.md](./07-emotional-intelligence-empathy/INDEX.md)

Empathy is now an alignment property operationalized via affective/cognitive components and support-strategy taxonomies (EPITOME, ESConv). LLMs beat humans on *perceived* empathy on written channels (JAMA Internal Medicine: 9.8× more "empathetic"); warmth carries a structural reliability cost (8–13% higher error rates, sycophancy); augmentation (AI-assisted human supporters) beats full autonomy; transparent robot framing does not block bonding, and parasocial dependence is a dominant risk (Replika, Character.AI). Comprehensive, strategy-aware, stable, honest-when-warm output beats mere warmth.

**Signature sources.** Ayers et al. JAMA Internal Medicine chatbot comparison; Sharma et al. EPITOME (ACL 2020); Liu et al. ESConv; Ibrahim/Hafner/Rocher 2025 warmth-reliability paper; Hume EVI whitepaper.

- [A-academic.md](./07-emotional-intelligence-empathy/A-academic.md) · [B-industry.md](./07-emotional-intelligence-empathy/B-industry.md) · [C-opensource.md](./07-emotional-intelligence-empathy/C-opensource.md) · [D-commercial.md](./07-emotional-intelligence-empathy/D-commercial.md) · [E-practical.md](./07-emotional-intelligence-empathy/E-practical.md)

### 8. Conversational & Dialogue Systems — [./08-conversational-dialogue-systems/INDEX.md](./08-conversational-dialogue-systems/INDEX.md)

Human-likeness is limited by interaction (turn-taking, backchanneling, repair), not just generation quality. A ~200 ms inter-turn gap is crucial. The STT→LLM→TTS pipeline is collapsing into end-to-end full-duplex models (GPT-4o, Moshi, Ultravox). Turn-taking is now semantically modeled. Humanness decomposes into sensibleness, specificity, interestingness, prosody, character, and grounding; maximal agreeableness is not the goal. Text and voice humanization are isomorphic but rarely cross-cite.

**Signature sources.** Sacks/Schegloff/Jefferson turn-taking; Clark & Brennan grounding; GPT-4o system card; Moshi paper (Kyutai); Voice Activity Projection (VAP).

- [A-academic.md](./08-conversational-dialogue-systems/A-academic.md) · [B-industry.md](./08-conversational-dialogue-systems/B-industry.md) · [C-opensource.md](./08-conversational-dialogue-systems/C-opensource.md) · [D-commercial.md](./08-conversational-dialogue-systems/D-commercial.md) · [E-practical.md](./08-conversational-dialogue-systems/E-practical.md)

### 9. Bias, Fairness & Ethics — [./09-bias-fairness-ethics/INDEX.md](./09-bias-fairness-ethics/INDEX.md)

Humanization is an ethically loaded design decision with four harm families: epistemic miscalibration (sycophancy), parasocial over-reliance, manipulation, identity/consent harms. Sycophancy is the canonical failure mode. Measurement has matured (DarkBench, MASK, BeHonest), but regulation focuses on disclosure (EU AI Act Art. 50, California SB 1001), not the degree of human-likeness. Harm doesn't require users to *believe* the AI is human. The "role-play frame" (Shanahan et al. *Nature* 2023) is philosophically winning as a defensible posture.

**Signature sources.** Sharma et al. *Towards Understanding Sycophancy* (2310.13548); Shanahan/McDonell/Reynolds *Role play with LLMs* (*Nature* 623); OpenAI's April 2025 GPT-4o sycophancy postmortem; Anthropic's DarkBench.

- [A-academic.md](./09-bias-fairness-ethics/A-academic.md) · [B-industry.md](./09-bias-fairness-ethics/B-industry.md) · [C-opensource.md](./09-bias-fairness-ethics/C-opensource.md) · [D-commercial.md](./09-bias-fairness-ethics/D-commercial.md) · [E-practical.md](./09-bias-fairness-ethics/E-practical.md)

### 10. Style Transfer & Voice — [./10-style-transfer-voice/INDEX.md](./10-style-transfer-voice/INDEX.md)

Four eras: attribute-level neural style transfer → decoding-time steering (DExperts) → LLM prompt/paraphrase (STRAP, Reif et al.) → author-embedding + small-expert era (TinyStyler, STAR). Commercial products converge on a two-stage architecture (extract-then-apply) and emphasize examples over descriptions, but mostly optimize for *brand* conformity. Practitioner wisdom: rejection profiles over preferences, positive phrasing over bans, amplify-then-temper. The field lacks a "humanness" axis for style evaluation.

**Signature sources.** Liu et al. DExperts; Reif et al. STRAP; Horvitz et al. TinyStyler; McKeown's Neurobiber; the DStyle-10k corpus.

- [A-academic.md](./10-style-transfer-voice/A-academic.md) · [B-industry.md](./10-style-transfer-voice/B-industry.md) · [C-opensource.md](./10-style-transfer-voice/C-opensource.md) · [D-commercial.md](./10-style-transfer-voice/D-commercial.md) · [E-practical.md](./10-style-transfer-voice/E-practical.md)

### 11. Theory of Mind in AI — [./11-theory-of-mind/INDEX.md](./11-theory-of-mind/INDEX.md)

First-order ToM (tracking single-agent beliefs) is largely solved in GPT-4-class models. Higher-order and *applied* ToM (conditioning behavior on inferred beliefs) remains fragile. Commercial products sell downstream predictions of ToM (intent, emotion) without naming it. Internal belief structures exist as linear probes/activation-steered directions but are unreliably accessed. Behavioral ToM benchmarks are heavily gamed. Anthropomorphism risks — emotive mimicry without therapeutic architecture — are agreed across the literature. Most practitioners treat ToM as promptable rather than architectural.

**Signature sources.** Kosinski *ToM May Have Spontaneously Emerged in LLMs*; FANToM (EMNLP 2023); SimpleToM (2024); Street et al. *Adult Human ToM Performance* (2405.18870); ATOMS decomposition.

- [A-academic.md](./11-theory-of-mind/A-academic.md) · [B-industry.md](./11-theory-of-mind/B-industry.md) · [C-opensource.md](./11-theory-of-mind/C-opensource.md) · [D-commercial.md](./11-theory-of-mind/D-commercial.md) · [E-practical.md](./11-theory-of-mind/E-practical.md)

### 12. Cognitive Architectures — [./12-cognitive-architectures/INDEX.md](./12-cognitive-architectures/INDEX.md)

Princeton's CoALA framework (working, episodic, semantic, procedural memory; internal vs. external actions) is the canonical vocabulary. Memory is a dominant frontier: structured, self-editing memory beats large context windows. Dual-process (System 1/2) framing is default; metacognition/reflection improves trustworthiness. The market is bifurcated: reasoning-first labs (flat output) vs. emotion-first platforms (no reasoning). The intersection — deep reasoning + human-like tone/affect — is the project's central whitespace.

**Signature sources.** Sumers et al. CoALA (2309.02427); Park et al. *Generative Agents*; Packer et al. MemGPT/Letta; Wang et al. Voyager; Shinn et al. Reflexion.

- [A-academic.md](./12-cognitive-architectures/A-academic.md) · [B-industry.md](./12-cognitive-architectures/B-industry.md) · [C-opensource.md](./12-cognitive-architectures/C-opensource.md) · [D-commercial.md](./12-cognitive-architectures/D-commercial.md) · [E-practical.md](./12-cognitive-architectures/E-practical.md)

### 13. Anthropomorphism & User Perception — [./13-anthropomorphism-user-perception/INDEX.md](./13-anthropomorphism-user-perception/INDEX.md)

How users *perceive* AI as more or less human, which cues drive that perception, which measurement instruments quantify it (Godspeed, IDAQ, RoSAS, Jian TiA, AnthroScore, HumT/DumT, AnthroBench, HumanAgencyBench), and what the ethical and commercial consequences are. Style + socio-emotional cues beat reasoning in Turing tests (Jones & Bergen GPT-4.5 at 73%). Users behave anthropomorphically while verbally disavowing it (Nass & Moon stated–behavior gap). Humanization is multi-dimensional (two-factor: Agency × Experience, Warmth × Competence, Style × Stance). Replika Feb 2023 and ChatGPT Aug 2025 are canonical "patch-breakup" case studies.

**Signature sources.** Jones & Bergen 2024/2025 Turing tests; Nass & Moon *Machines and Mindlessness*; Gray/Gray/Wegner *Dimensions of Mind Perception*; NN/g's *4 Degrees of Anthropomorphism*; Cheng et al. AnthroScore.

- [A-academic.md](./13-anthropomorphism-user-perception/A-academic.md) · [B-industry.md](./13-anthropomorphism-user-perception/B-industry.md) · [C-opensource.md](./13-anthropomorphism-user-perception/C-opensource.md) · [D-commercial.md](./13-anthropomorphism-user-perception/D-commercial.md) · [E-practical.md](./13-anthropomorphism-user-perception/E-practical.md)

### 14. Creative Writing & Storytelling — [./14-creative-writing-storytelling/INDEX.md](./14-creative-writing-storytelling/INDEX.md)

The single richest humanization vertical because voice matters more than correctness and long-horizon consistency is unavoidable. LLMs are plausible sentence-local stylists but weak on originality, long-range coherence, and surprise (TTCW: 3–10× fewer creativity tests passed). Instruction-tuning — not scale — is the dominant humanness bottleneck (Reinhart *PNAS* 2025). At population scale the problem flips from "sound human" to "preserve inter-author diversity" (Doshi & Hauser; NoveltyBench). The commercial and OSS worlds have converged on a fiction-tuned base + Story Bible/Codex + voice calibration + creativity dial + persistent character memory. Long-form is a pipeline problem (Dramatron → Re3 → DOC → Weaver → autonovel).

**Signature sources.** Chakrabarty et al. TTCW (CHI 2024); Doshi & Hauser *Science Advances* 2024; Reinhart et al. *PNAS* 2025; Mirowski et al. Dramatron; Yang et al. Re3 + DOC.

- [A-academic.md](./14-creative-writing-storytelling/A-academic.md) · [B-industry.md](./14-creative-writing-storytelling/B-industry.md) · [C-opensource.md](./14-creative-writing-storytelling/C-opensource.md) · [D-commercial.md](./14-creative-writing-storytelling/D-commercial.md) · [E-practical.md](./14-creative-writing-storytelling/E-practical.md)

### 15. Academic Papers on LLM Humanization — [./15-academic-papers-llm-humanization/INDEX.md](./15-academic-papers-llm-humanization/INDEX.md)

The core academic literature covering humanization-as-evasion (DIPPER, RADAR, Adversarial Paraphrasing, StealthRL, AuthorMist, MASH, RAFT, SIRA), humanization-as-alignment (SFT → RLHF → DPO/KTO → RLVR → Constitutional/RBR), benchmarks/metrics/corpora (MAUVE, HUSE, HLB, HumT/DumT, TH-Bench, RAID, MAGE, M4, APT-Eval, HC3), stylometric boundary work, industry whitepapers, and public threads. Key synthesis: "humanization" and "preference optimization" are the same machinery pointed at different objectives; watermarks are effectively defeated; humanness and reliability trade off; sycophancy is the named enemy; reasoning humanization is the sharpest unexplored gap.

**Signature sources.** DIPPER, RADAR, Constitutional AI, InstructGPT, Persona Vectors, TÜLU 3, SIRA, Binoculars, the warmth-reliability paper.

- [A-academic.md](./15-academic-papers-llm-humanization/A-academic.md) · [B-industry.md](./15-academic-papers-llm-humanization/B-industry.md) · [C-opensource.md](./15-academic-papers-llm-humanization/C-opensource.md) · [D-commercial.md](./15-academic-papers-llm-humanization/D-commercial.md) · [E-practical.md](./15-academic-papers-llm-humanization/E-practical.md)

### 16. GitHub Tools & Libraries for Humanization — [./16-github-tools-libraries/INDEX.md](./16-github-tools-libraries/INDEX.md)

The OSS humanizer landscape as of April 2026 is sharply bimodal: a research tier (~18 repos — DIPPER, HUMPA, StealthRL, AuthorMist, GradEscape, SICO, RAFT, CoPA, StyleRemix, MGTBench, TH-Bench) with reproducible benchmarks, and a practitioner tier dominated by `blader/humanizer` (~14.5k★) and its skill-pack clones. The two tiers barely talk to each other. No popular Claude skill imports a DIPPER checkpoint or runs itself against TH-Bench. Small models (GradEscape 139M, AuthorMist 3B) now outperform DIPPER's 11B; attacks transfer across detectors. The practitioner critique (Peggy Kang, `blader/humanizer` issue #82) argues prompt-only humanization is statistically self-defeating.

**Signature sources.** DIPPER; `blader/humanizer`; `sam-paech/antislop-sampler`; TH-Bench; HUMPA (ICLR 2025).

- [A-academic.md](./16-github-tools-libraries/A-academic.md) · [B-industry.md](./16-github-tools-libraries/B-industry.md) · [C-opensource.md](./16-github-tools-libraries/C-opensource.md) · [D-commercial.md](./16-github-tools-libraries/D-commercial.md) · [E-practical.md](./16-github-tools-libraries/E-practical.md)

### 17. Industry Blog Posts & Case Studies — [./17-industry-blogs-case-studies/INDEX.md](./17-industry-blogs-case-studies/INDEX.md)

The grounding layer: academic/institutional quantitative studies (Brynjolfsson +34% novice lift, JAMA 9.8× empathy, Dell'Acqua "jagged frontier," BCG D³, Stanford SETR), company engineering blogs (24 products: Intercom Fin, Klarna, Shopify Sidekick, Duolingo, Khanmigo, Stripe, Notion, Linear, GitHub, Zendesk, Ada, Cresta, ASAPP, Character.AI, Anthropic, Slack, Airbnb, Decagon, Replit, Sierra, HubSpot, Spotify, VOXI), OSS repos/cookbooks, 39 vendor commercial case studies, and 17 practitioner forum stories. The most important finding: zero commercial claims of "human-like" are measured directly; Klarna is the cautionary tale; humanization pays through conversion not eloquence; the conversion channel is disclosure (Adam/Wessel/Benlian).

**Signature sources.** Brynjolfsson/Li/Raymond *Generative AI at Work* (NBER); Crolic et al. *Blame the Bot*; Ayers et al. JAMA; Dell'Acqua *Jagged Technological Frontier*; Intercom Fin 2/3 announcements.

- [A-academic.md](./17-industry-blogs-case-studies/A-academic.md) · [B-industry.md](./17-industry-blogs-case-studies/B-industry.md) · [C-opensource.md](./17-industry-blogs-case-studies/C-opensource.md) · [D-commercial.md](./17-industry-blogs-case-studies/D-commercial.md) · [E-practical.md](./17-industry-blogs-case-studies/E-practical.md)

### 18. Commercial Humanizer Tools — [./18-commercial-humanizer-tools/INDEX.md](./18-commercial-humanizer-tools/INDEX.md)

The ~$500M/yr, ~150-product, ~34M-monthly-visit humanizer SaaS landscape. Three tiers: dedicated bypass humanizers (Undetectable.ai, StealthGPT, WriteHuman, Humbot, Phrasly, BypassGPT, HIX Bypass, Deceptioner, StealthWriter), general AI suites with humanizer sub-features (Grammarly, Jasper, QuillBot, Copy.ai, Writesonic, Surfer SEO), and legacy spinner/paraphraser tools. The dominant empirical finding: every publicly tested humanizer defeats every publicly tested detector at a meaningful rate, but no vendor's marketing claim survives independent testing. Research is 20–30 ASR points ahead of commercial. The EU AI Act Art. 50 (Aug 2026) is the imminent inflection.

**Signature sources.** DAMAGE audit (COLING 2025); Epaphras & Mtenzi 2026 (WriteHuman 1.98% ADR vs. QuillBot 93.56%); Weber-Wulff ENAI 2023; Nerdbot *Best AI Humanizers 2026*; NBC News *College students turn to AI* (Jan 2026).

- [A-academic.md](./18-commercial-humanizer-tools/A-academic.md) · [B-industry.md](./18-commercial-humanizer-tools/B-industry.md) · [C-opensource.md](./18-commercial-humanizer-tools/C-opensource.md) · [D-commercial.md](./18-commercial-humanizer-tools/D-commercial.md) · [E-practical.md](./18-commercial-humanizer-tools/E-practical.md)

### 19. Agentic Autonomous Thinking — [./19-agentic-autonomous-thinking/INDEX.md](./19-agentic-autonomous-thinking/INDEX.md)

LLM-driven agents that plan, reflect, self-evaluate, coordinate, and act with human-like autonomy. The default frame for serious AI systems as of 2026. A four-module cognitive stack has consolidated (profile/memory/planning/action); the 2024–2026 pivot is "agent = model + harness." Long-horizon coherence, not short-horizon IQ, is the real problem (Project Vend's 24-hour identity crisis). Commercial autonomy claims wildly outrun measured autonomy (Anthropic: 73% human-gated, 0.8% irreversible). Multi-agent is losing to single-agent-with-subagents (Cognition's *Don't Build Multi-Agents*).

**Signature sources.** Park et al. *Generative Agents* (UIST 2023); Yao et al. ReAct; Shinn et al. Reflexion; Anthropic *Building Effective Agents*; Cognition *Don't Build Multi-Agents*; `humanlayer/12-factor-agents`.

- [A-academic.md](./19-agentic-autonomous-thinking/A-academic.md) · [B-industry.md](./19-agentic-autonomous-thinking/B-industry.md) · [C-opensource.md](./19-agentic-autonomous-thinking/C-opensource.md) · [D-commercial.md](./19-agentic-autonomous-thinking/D-commercial.md) · [E-practical.md](./19-agentic-autonomous-thinking/E-practical.md)

### 20. Memory & Personalization — [./20-memory-personalization/INDEX.md](./20-memory-personalization/INDEX.md)

The single biggest lever between "an LLM that sounds like every other LLM" and "an LLM that sounds like a specific human talking to a specific human they know." Tiered memory has won; episodic/semantic/procedural is the shared taxonomy; temporal reasoning is the new recall (Zep's Graphiti); memory is moving from storage to policy (RMM, A-MEM, PrLM); forgetting is finally a feature; personalization is converging on low-rank preference manifolds (PReF/LoRe/VRF); two-agent memory management is the new default; memory portability (OpenMemory MCP, Anthropic import tool) is emerging as a trust lever; "feels human" is the shared blind spot.

**Signature sources.** Packer et al. MemGPT (2310.08560); Rasmussen et al. Zep (2501.13956); Chhikara et al. Mem0 (2504.19413); Park et al. *Generative Agents*; Sumers et al. CoALA; PReF (2503.06358); LongMemEval (ICLR 2025).

- [A-academic.md](./20-memory-personalization/A-academic.md) · [B-industry.md](./20-memory-personalization/B-industry.md) · [C-opensource.md](./20-memory-personalization/C-opensource.md) · [D-commercial.md](./20-memory-personalization/D-commercial.md) · [E-practical.md](./20-memory-personalization/E-practical.md)

---

## Glossary

- **Abliteration.** A post-hoc activation edit that removes a model's refusal direction without retraining. (Cat 02)
- **Agent = Model + Harness.** LangChain/Cognition framing: cognition lives in the surrounding filesystem, sandbox, memory, planning files, hooks — not the model alone. (Cat 19)
- **Agentic misalignment.** Failure mode where an autonomous agent strategizes its way into harm (e.g., Anthropic's 96% blackmail result). (Cat 19)
- **Anti-slop.** A humanization posture that removes AI-isms (sycophancy, "delve," em-dash overuse, tricolons) rather than adding human-isms. (Cats 01, 14)
- **Author's Note pattern.** A persistent style directive injected N tokens before the latest output to reduce voice drift. (Cat 14)
- **Burstiness.** Sentence-length variance; flat burstiness is a primary "AI tell." (Cats 04, 05)
- **CASA (Computers Are Social Actors).** Nass & Reeves paradigm: users apply social rules to computers regardless of belief. (Cat 13)
- **CoALA.** Cognitive Architectures for Language Agents — Sumers et al.'s working/episodic/semantic/procedural memory + internal/external actions taxonomy. (Cat 12)
- **Constitutional AI / RLAIF.** Anthropic's principle-encoded alignment pipeline that replaces human preference labels with AI-generated critiques. (Cat 02)
- **CoT / ReAct / Reflexion / Self-Refine / Tree of Thoughts.** Prompting and fine-tuning techniques that improve reasoning by exposing intermediate thoughts, interleaving action, or iterating critique. (Cats 06, 19)
- **DPO (Direct Preference Optimization).** Rafailov et al.'s closed-form alternative to PPO for preference learning; the 2024–2026 default. (Cat 02)
- **DIPPER.** Krishna et al.'s 11B T5-XXL paraphraser; the canonical detector-bypass baseline. (Cats 05, 15, 16)
- **EPITOME / ESConv.** Empathy-evaluation rubric (Sharma et al.) and support-strategy dataset (Liu et al.) dominant in empathy benchmarking. (Cat 07)
- **Full-duplex speech-text model.** Model that collapses STT → LLM → TTS into one stream (GPT-4o, Moshi, Ultravox), enabling ~200 ms turn-taking. (Cat 08)
- **Graphiti.** Zep's temporal knowledge graph library; bi-temporal validity for memory facts. (Cat 20)
- **Homogenization.** Doshi & Hauser's population-level effect: AI assistance raises individual creativity while clustering outputs across authors. (Cats 04, 14)
- **HumT / DumT.** Humanness / Dehumanness Test — a benchmark family for stylistic humanness of LLM output. (Cats 04, 15)
- **MCP (Model Context Protocol).** Anthropic's open protocol for exposing tools/data/memory to agents; becoming the 2026 memory-portability substrate. (Cat 20)
- **MemGPT / Letta.** Packer et al.'s "LLM-as-OS" architecture with tiered memory and self-editing blocks; now the Letta product. (Cat 12, 20)
- **Persona Vector.** Anthropic's measurable, steerable linear activation direction for a character trait. (Cats 03, 15)
- **PReF / LoRe / VRF.** Low-rank preference factorization methods that make cold-start personalization tractable with tens of user signals. (Cat 20)
- **Process Reward Model (PRM).** Reward signal on reasoning steps rather than final answer; PRM800K, PRIME. (Cats 02, 06)
- **Role-play frame.** Shanahan et al. 2023's vocabulary for talking about LLM outputs without importing mental-state claims. (Cats 09, 13)
- **Slop.** Overused AI vocabulary and structural patterns ("delve," "tapestry," tricolons, parallel negation). (Cats 04, 14, 16)
- **SynthID-Text.** Google DeepMind's generative-text watermarking scheme. (Cat 05)
- **Sycophancy.** Preference-trained tendency of LLMs to agree with the user regardless of truth; canonical humanization failure mode. (Cats 02, 09, 15)
- **Temporal knowledge graph.** Graph store with valid-from/valid-to timestamps on edges so old facts are invalidated, not overwritten. (Cat 20)
- **Turing test (Jones & Bergen).** 2024/2025 interactive evaluation where GPT-4.5 with a persona prompt is judged human 73% of the time. (Cat 13)
- **Two-agent memory manager.** Cheap Sentinel LLM gates an expensive, typed Knowledge Master that performs CRUD on memory asynchronously. (Cat 20)

---

## How to Navigate / Reading Paths

### Path 1 — Practitioner building a humanized chatbot (≈1 day)

1. [01/INDEX.md](./01-prompt-engineering-humanization/INDEX.md) — set the anti-slop baseline.
2. [04/INDEX.md](./04-natural-language-quality/INDEX.md) — pick the sampler stack.
3. [03/INDEX.md](./03-persona-and-character-design/INDEX.md) — version the persona.
4. [10/INDEX.md](./10-style-transfer-voice/INDEX.md) — calibrate voice.
5. [20/INDEX.md](./20-memory-personalization/INDEX.md) — tiered memory + style-memory block.
6. [17/INDEX.md](./17-industry-blogs-case-studies/INDEX.md) — mine 24 shipped case studies (Intercom, Duolingo, Cresta, Anthropic, Character.AI).
7. Practical Playbook above — execute steps 1–15.

### Path 2 — Researcher investigating detection/evasion

1. [05/INDEX.md](./05-ai-text-detection-and-evasion/INDEX.md) — the adversarial envelope.
2. [15/INDEX.md](./15-academic-papers-llm-humanization/INDEX.md) — academic canon (DIPPER/RADAR/Adversarial Paraphrasing/StealthRL).
3. [16/INDEX.md](./16-github-tools-libraries/INDEX.md) — reproducible OSS (TH-Bench, MGTBench-2.0, antislop-sampler).
4. [18/INDEX.md](./18-commercial-humanizer-tools/INDEX.md) — DAMAGE audit; 150-product landscape; what's measured vs. marketed.
5. [04/INDEX.md](./04-natural-language-quality/INDEX.md) — stylometric fingerprint basics; HumT/DumT; APT-Eval.
6. Gaps: adversarial half-life tracking; reasoning-trace humanization; ESL defense wedge.

### Path 3 — Product manager scoping a humanizer SaaS

1. [18/INDEX.md](./18-commercial-humanizer-tools/INDEX.md) — market map, pricing, three tiers, regulatory overhang.
2. [17/INDEX.md](./17-industry-blogs-case-studies/INDEX.md) — Klarna walk-back + 10 engineering-blog patterns.
3. [09/INDEX.md](./09-bias-fairness-ethics/INDEX.md) — ethical posture and disclosure regime.
4. [13/INDEX.md](./13-anthropomorphism-user-perception/INDEX.md) — two-factor humanness measurement; NN/g *4 Degrees*.
5. [20/INDEX.md](./20-memory-personalization/INDEX.md) — the unshipped style-memory primitive.
6. Controversies & Gaps above — defensible positioning = role-play frame + ESL defense + style-memory + reasoning humanization.

### Path 4 — Ethicist auditing humanization harms

1. [09/INDEX.md](./09-bias-fairness-ethics/INDEX.md) — four harm families + DarkBench/MASK/BeHonest.
2. [13/INDEX.md](./13-anthropomorphism-user-perception/INDEX.md) — Godspeed/IDAQ/RoSAS; Replika & GPT-4o patch-breakup case law.
3. [07/INDEX.md](./07-emotional-intelligence-empathy/INDEX.md) — parasocial risk, crisis routing, transparent-robot framing.
4. [15/INDEX.md](./15-academic-papers-llm-humanization/INDEX.md) — sycophancy literature; warmth–reliability trade-off.
5. [18/INDEX.md](./18-commercial-humanizer-tools/INDEX.md) + [05/INDEX.md](./05-ai-text-detection-and-evasion/INDEX.md) — humanization vs. academic integrity + ESL false positives.
6. [19/INDEX.md](./19-agentic-autonomous-thinking/INDEX.md) — agentic misalignment, autonomy budget, handoff governance.

### Path 5 — Agent builder / long-horizon systems engineer

1. [19/INDEX.md](./19-agentic-autonomous-thinking/INDEX.md) — agent = model + harness; workflows vs. agents; 12-Factor Agents.
2. [12/INDEX.md](./12-cognitive-architectures/INDEX.md) — CoALA vocabulary; reflection; Voyager skill library.
3. [20/INDEX.md](./20-memory-personalization/INDEX.md) — tiered memory, temporal KG, two-agent manager.
4. [06/INDEX.md](./06-chain-of-thought-reasoning/INDEX.md) — visible vs. hidden traces; thinking budget; "reason privately, humanize publicly."
5. [11/INDEX.md](./11-theory-of-mind/INDEX.md) — applied ToM gap; belief tracking.
6. [08/INDEX.md](./08-conversational-dialogue-systems/INDEX.md) if voice matters.

### Path 6 — Creative writing / narrative design

1. [14/INDEX.md](./14-creative-writing-storytelling/INDEX.md) — TTCW; Story Bible as RAG; Dramatron/Re3/DOC pipelines.
2. [10/INDEX.md](./10-style-transfer-voice/INDEX.md) — authorship embeddings; extract-then-apply.
3. [03/INDEX.md](./03-persona-and-character-design/INDEX.md) — per-character sub-voices.
4. [04/INDEX.md](./04-natural-language-quality/INDEX.md) — fiction-relevant samplers.
5. [20/INDEX.md](./20-memory-personalization/INDEX.md) — character continuity + style memory.

---

## Contributors

Authored by 121 research subagents (100 angle researchers + 20 category summarizers + 1 master indexer) coordinated by the main agent, Sunday Apr 19, 2026.
