# Agent #45 — Humanizing Machines Four-Cue Taxonomy (EMNLP 2025)

**Topic:** Xiao et al. *Humanizing Machines* — four-cue anthropomorphism framework, benchmarks, risk-vs-design debate, unslop `humanize.py` pass mapping  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**Humanizing Machines is a design-framework paper, not a humanizer benchmark and not an empirical evaluation study.** Xiao, Ng, Liu & Diab (CMU; EMNLP 2025) propose that anthropomorphism in LLM artifacts is a **reciprocal interaction**: designers embed cues; interpreters project mental states onto those cues. Cues fall into four dimensions — **perceptual, linguistic, behavioral, cognitive** — each on a low→high continuum. Aggregate intensity is a tunable parameter **α** that should match system competence, context, and cultural norms.

The paper's main contribution is vocabulary and design guidance, not numbers. It **did not run user studies or automated cue quantification at scale** (stated explicitly in Limitations). For measurement it **imports** Cheng et al.'s **AnthroScore** and **HumT** for the linguistic dimension only; behavioral and cognitive cue metrics are flagged as **open research**.

For **unslop**, the taxonomy is the best academic checklist for *which layer* a humanization pass operates on. unslop is **strong on linguistic cues** (lexical scrub + structural burstiness + contraction lift), **partial on behavioral and cognitive** (sycophancy/hedging/signposting removal; optional reasoning-trace strip), and **mostly out of scope on perceptual** (no avatar/UI layer). Critically, unslop's default job is **lowering α on fake-human slop** — sycophancy, performative empathy, visible chain-of-thought — while **raising authentic linguistic humanness** (contractions, sentence-length variance). That matches the paper's "capability-expectation alignment" principle better than blind "make it sound human" humanizers.

**Debate axis:** Cheng/Blodgett/Olteanu (*Dehumanizing Machines*, ACL 2025 Best Paper) = mitigate anthropomorphism when harmful. Xiao/Diab (*Humanizing Machines*) = treat anthropomorphism as intentional design dial. Same authors cross-cite; not contradictory if α is context-calibrated.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **arXiv abstract** | https://arxiv.org/abs/2508.17573 |
| **arXiv HTML (v2)** | https://arxiv.org/html/2508.17573v2 |
| **arXiv HTML (v1)** | https://arxiv.org/html/2508.17573v1 |
| **ACL Anthology (EMNLP 2025 main)** | https://aclanthology.org/2025.emnlp-main.164/ |
| **ACL PDF** | https://aclanthology.org/2025.emnlp-main.164.pdf |
| **DOI (arXiv)** | https://doi.org/10.48550/arxiv.2508.17573 |
| **ACL DOI** | https://doi.org/10.18653/v1/2025.emnlp-main.164 |

**Authors:** Yunze Xiao, Lynnette Hui Xian Ng (equal first), Jiarui Liu, Mona T. Diab — Carnegie Mellon University. Pages 3331–3350, EMNLP 2025, Suzhou.

---

## The four-cue taxonomy

### Core model

Anthropomorphism = **designers embed cues** + **interpreters project responses**. Four cue types, each varying in **intensity** (low = minimal human-like signal; high = sophisticated cognitive/emotional response). Combined intensity = **α**, a dial designers should match to **actual system competence**.

Aligned with **Wellman Theory of Mind** (Table 1 in paper):

| Cue dimension | ToM component | What it signals |
|---------------|---------------|-----------------|
| **Perceptual** | Perceiving | Physical/visual human-likeness |
| **Linguistic** | Feeling + Desiring | Word choice, syntax, tone, pronouns, hedges |
| **Behavioral** | Choosing | Actions, turn-taking, proactivity, adaptation |
| **Cognitive** | Thinking | Reasoning, reflection, uncertainty, planning |

### 3.1 Perceptual cues

**Definition:** Physical or visual features conveying human-likeness — avatars, embodiment, typing indicators, friendly greetings, robot faces.

**Spectrum:**
- Low: abstract symbolism (two dots as eyes), generic avatar
- High: personalized/realistic representation (Geminoid-F), anatomically detailed faces

**Design principle:** Realism sets interpreter expectations. Uncanny valley when appearance exceeds capability. Even masked sensors/gestures can trigger social responses.

**unslop relevance:** **Out of scope** for a text rewriter. Tangential touchpoints: markdown structure (bullet-soup merge changes visual density), em-dash cap (typographic "AI slop" tell). Cursor/Windsurf statusline badge `[unslop]` is a perceptual cue in the IDE — signals "humanized mode" to the user, not to readers of rewritten prose.

### 3.2 Linguistic cues

**Definition:** Language choices signaling humanness — vocabulary, syntax, tone, pronouns, formality, emotional expression, hedges, politeness.

**Spectrum:**
- Low: superficial social markers ("I", "maybe", "please")
- High: complex discourse — justification, inference, conversational management (surface-level agency without true cognition)

**Quantification (cited, not built by Xiao et al.):**
- **AnthroScore** — Cheng et al. 2024, EACL: https://aclanthology.org/2024.eacl-long.47/ · https://arxiv.org/abs/2402.17227
- **HumT / DumT** — Cheng, Yu & Jurafsky 2025: https://arxiv.org/abs/2502.13259

**Risk:** Same cues that build trust backfire on failure (Crolic et al. "Blame the bot"). Cultural moderation: "maybe" = polite (US) vs evasive (Korea).

**unslop relevance:** **Primary intervention surface.** See pass mapping below.

### 3.3 Behavioral cues

**Definition:** Actions and interaction patterns — contingent responses, proactive goal pursuit, adaptive personalization, turn-taking, unsolicited recommendations.

**Spectrum:**
- Low: functionally contingent digital actions (API calls, code completion)
- High: embodied gestures, spatial coordination, emotional adaptability (companions)

**Risk:** Over-proactivity reads as intrusive; norm-adaptive behavior can embed cultural bias.

**unslop relevance:** **Partial.** Text-only behavioral cues in assistant output: sycophancy stacks, signposting, knowledge-cutoff disclaimers, vague attribution, performative balance. unslop **removes** many of these (lowering fake proactivity). Does not implement turn-taking latency, tool-use choreography, or companion-style emotional adaptation.

### 3.4 Cognitive cues

**Definition:** Reasoning capabilities — designer-embedded (planning, reflection) and interpreter-perceived (self-correction, uncertainty, adaptive responses).

**Spectrum:**
- Low: token expressions of reasoning/uncertainty
- High: empathy display, sophisticated logic, multi-turn negotiation

**Risk:** High empathy without grounding misleads vulnerable users; shallow empathy reads insincere.

**unslop relevance:** **Partial, mostly subtractive.** `--strip-reasoning` removes visible CoT/reasoning traces (`<thinking>`, `## Reasoning` sections) — lowers **high-level cognitive cue intensity** on published output ("reason privately, humanize publicly"). Hedging-opener removal reduces fake-uncertainty performance. unslop does **not** add genuine reasoning transparency; it removes **simulated** reasoning theater.

---

## Three alignment factors (Section 4)

Effectiveness depends on:

1. **Capability–expectation alignment** — cues must not promise more than the system delivers
2. **Context–purpose alignment** — cue intensity matches task stakes (Table 2)
3. **Cultural–norm alignment** — cues respect local interaction norms

**Table 2 (context-dependent applications):**

| Cue | Beneficial when | Minimize when |
|-----|-----------------|---------------|
| Cognitive | Mental health (empathy, reasoning) | Search engines |
| Linguistic | Education (conversational) | Finance (transaction seriousness) |
| Behavioral | Social AI (rapport) | Legal bots (false authority) |
| Perceptual | Children's learning (friendly avatar) | Government (official identity) |

**unslop implication:** Default `balanced` mode is tuned for **professional prose** (docs, commits, articles) — lowers linguistic slop and fake cognitive/behavioral cues without pushing companion-level α. `anti-detector` adds stylometric nudges; still not companion/chatbot α.

---

## Benchmarks and evaluation landscape

### What Humanizing Machines does NOT provide

From Limitations (Section after Conclusion):

> "We did not conduct empirical evaluations, user studies, or automated cue quantification at scale."

No new benchmark dataset. No α-scoring tool shipped. Recommendations call for **future metrics** on behavioral and cognitive dimensions.

### Metrics the paper cites for linguistic α

| Metric | Paper | URL | What it measures |
|--------|-------|-----|------------------|
| **AnthroScore** | Cheng et al. EACL 2024 | https://arxiv.org/abs/2402.17227 · https://aclanthology.org/2024.eacl-long.47/ | Computational linguistic anthropomorphism score |
| **HumT / DumT** | Cheng, Yu & Jurafsky 2025 | https://arxiv.org/abs/2502.13259 | Human-like language tone; warmth/status tradeoff |
| **DeVrio et al. linguistic taxonomy** | CHI 2025 | https://doi.org/10.1145/3706598.3713307 | Taxonomy of linguistic expressions contributing to anthropomorphism |

### Adjacent benchmarks (not in Humanizing Machines, relevant to unslop)

| Benchmark | URL | Axis |
|-----------|-----|------|
| **HumanLLM** | https://arxiv.org/abs/2601.10198 · https://aclanthology.org/2026.acl-long.1783/ | Cognitive-pattern fidelity in role-play (244 patterns) |
| **HLB (Human-Likeness Benchmark)** | https://arxiv.org/abs/2409.15890 | Psycholinguistic human-likeness vs capability |
| **Psychobench** | https://arxiv.org/abs/2310.01386 | LLM psychological portrayal |
| **InCharacter** | https://aclanthology.org/2024.acl-long.108/ | Personality fidelity in RP agents |
| **BUST** | https://aclanthology.org/2024.naacl-long.444/ | AI-text detection (25K texts, 7 LLMs) |
| **RAID** | https://arxiv.org/abs/2405.07926 | Detector robustness under attack |
| **MGTBench / TH-Bench** | https://arxiv.org/abs/2310.05172 | Humanizer vs detector Pareto frontier |
| **DivEye** | https://arxiv.org/abs/2509.18880 | Intra-document surprisal variance detection |

### unslop internal evals (four-cue mapping)

| unslop eval | Path | Cue dimensions touched |
|-------------|------|------------------------|
| **Phase 6 perceived humanness** | `evals/perceived_humanness.py` | Primarily **linguistic** (blind LLM-judge preference) |
| **Detector bench** | `benchmarks/detector_bench.py` | Meta-signal; correlates with **linguistic** distributional cues |
| **Stylometric baseline** | `benchmarks/results/stylometric_baseline.json` | **Linguistic** (burstiness, contractions, TTR) |
| **Preservation suite** | `tests/unslop/test_humanize.py` | Non-cue (integrity constraint) |

**Gap vs Humanizing Machines agenda:** unslop has no **behavioral** or **cognitive** cue scorer; no **perceptual** layer. Phase 6 measures holistic preference, not α per dimension.

---

## Debate: risk-centric vs design-centric anthropomorphism

### Risk-centric camp (mitigate anthropomorphism)

| Work | URL | Position |
|------|-----|----------|
| **Dehumanizing Machines** (Cheng et al., ACL 2025 Best Paper) | https://aclanthology.org/2025.acl-long.1259/ · https://arxiv.org/abs/2502.14019 | 28 intervention types from literature + crowdsourced edits; framework for *reducing* anthropomorphic behaviors when harmful |
| **AnthroScore** | https://arxiv.org/abs/2402.17227 | Measure anthropomorphism to *control* it |
| **HumT / DumT** | https://arxiv.org/abs/2502.13259 | Measure and control human-like language |
| **AI Automatons** (Olteanu et al. 2025) | https://arxiv.org/abs/2503.02250 | Systems intended to imitate humans — ethical framing |
| **Mirages** (Abercrombie et al. EMNLP 2023) | https://aclanthology.org/2023.emnlp-main.288/ | Anthropomorphism as dialogue-system risk |
| **Mapping anthropomorphic AI risk** (Akbulut et al. AIES 2024) | https://doi.org/10.1609/aies.v7i1.31613 | Risk mapping and mitigation |

**Cheng crowdsourced study:** participants edited AI outputs to be **less** human-like — directly parallel to unslop's subtractive passes (sycophancy, hedging, performative empathy removal).

### Design-centric camp (calibrate anthropomorphism)

| Work | URL | Position |
|------|-----|----------|
| **Humanizing Machines** (Xiao et al., EMNLP 2025) | https://arxiv.org/abs/2508.17573 | Anthropomorphism as tunable design parameter α; function-oriented evaluation |
| **Humanizing LLMs survey** (Dong et al. 2025) | https://arxiv.org/abs/2505.00049 | Psychological measurement for persona design |
| **From Persona to Personalization** (Chen et al. 2024) | https://arxiv.org/abs/2404.18231 | Role-playing agent design survey |

### Synthesis (not a clean fight)

Xiao et al. **explicitly cite** Cheng et al. as the risk-centric paradigm they move beyond — not as wrong, but as **incomplete**:

> "Instead of treating anthropomorphism solely as a linguistic attribution… we contend that anthropomorphism should be treated as a multidimensional reciprocal interaction process."

Cheng's **Dehumanizing Machines** and Xiao's **Humanizing Machines** are **title-inverted complements**:
- Cheng: *when* and *how* to **de**-humanize output (inventory of 28 interventions)
- Xiao: *when* and *how* to **calibrate** human-like cues across four dimensions

unslop sits in the **intersection**: it **de**-humanizes slop (Cheng-aligned subtractive rules) while **re**-humanizing register (contractions, burstiness — Xiao linguistic α tuned to "competent human writer" not "empathetic companion").

**Dual-use note (from Xiao Limitations):** taxonomy can inform manipulative systems. unslop's `anti-detector` mode is explicitly bounded in skill docs — ESL false positives, resume polish; not academic misconduct.

---

## unslop → four-cue → `humanize.py` pass mapping

### Pipeline overview

```
[Optional Phase 0] strip_reasoning     → cognitive ↓
[Phase 2 lexical]  regex rule families → linguistic ↓/↑, behavioral ↓, cognitive ↓
[Phase 1]          structural.py       → linguistic ↑ (burstiness)
[Phase 3]          lexical_targets     → linguistic ↑ (anti-detector only)
[Phase 5]          soul.py             → linguistic ↑ (contractions)
[Phase 4]          stylometry.py       → measure linguistic (voice-match)
[Phase 3 det]      detector.py         → eval loop, not a cue pass
[LLM mode]         humanize_llm        → all dimensions (prompt-driven)
[Phase 8]          style_memory.py     → linguistic personalization
[Phase 6 eval]     perceived_humanness → holistic linguistic preference
```

### Detailed mapping table

| unslop pass / module | Intensity gate | Cue dim | Direction | Mechanism |
|---------------------|----------------|---------|-----------|-----------|
| `strip_reasoning` (`reasoning.py`) | opt-in CLI | **Cognitive** | ↓ high-level | Removes `<thinking>`, `## Reasoning` — simulated deliberation |
| `sycophancy` rules | balanced+ | **Linguistic**, **Behavioral** | ↓ | "Great question!", "I'd be happy to" — fake warmth |
| `hedging_opener` | balanced+ | **Linguistic**, **Cognitive** | ↓ | "It's important to note" — performative uncertainty |
| `transition_tic` | balanced+ | **Linguistic** | ↓ | "Furthermore", "Moreover" — essay-register |
| `authority_trope` | balanced+ | **Linguistic**, **Behavioral** | ↓ | False expert positioning |
| `signposting` | balanced+ | **Linguistic**, **Cognitive** | ↓ | "Let me explain", "In this section" — meta-narration |
| `knowledge_cutoff` | balanced+ | **Linguistic**, **Cognitive** | ↓ | "As of my last training" — assistant behavioral script |
| `vague_attribution` | balanced+ | **Linguistic** | ↓ | "Experts say" — fake epistemic grounding |
| `stock_vocab` | all (incl. subtle) | **Linguistic** | ↓ | delve/tapestry/leverage slop |
| `significance_inflation` | balanced+ | **Linguistic** | ↓ | "pivotal moment", "testament to" |
| `notability_namedropping` | balanced+ | **Linguistic** | ↓ | Wikipedia-tone |
| `copula_avoidance` | balanced+ | **Linguistic** | ↓ | "serves as" → "is" |
| `performative` | balanced+ | **Linguistic**, **Behavioral** | ↓ | False balance, both-sidesism |
| `filler_phrase` | full+ | **Linguistic** | ↓ | Padding |
| `negative_parallelism` | full+ | **Linguistic** | ↓ | "Not X but Y" AI construction |
| `superficial_ing` | full+ | **Linguistic** | ↓ | "-ing" nominalizations |
| `_cap_em_dashes_per_paragraph` | balanced+ | **Linguistic** | ↓ | Typographic AI tell |
| `humanize_structural` (`structural.py`) | balanced+ default | **Linguistic** | ↑ authentic | Sentence-length variance, bullet merge |
| `apply_targeted_pass` (`lexical_targets.py`) | anti-detector | **Linguistic** | ↑ measured | Stylometric gap closure vs human baselines |
| `humanize_soul` (`soul.py`) | balanced+ default | **Linguistic** | ↑ authentic | Contraction rate toward human distribution |
| `analyze` (`stylometry.py`) | voice-match | **Linguistic** | measure | 20+ signals incl. DivEye proxies |
| `humanize_llm` + audit | LLM mode | **All** | mixed | Rewrite + second-pass audit |
| `feedback_loop` (`detector.py`) | anti-detector CLI | meta | n/a | Escalates intensity until detector score drops |
| Hooks (`unslop-mode-tracker.js`) | session | **Behavioral** (IDE) | mode switch | User-facing unslop activation |

### Intensity modes as α presets

| Mode | Approx. α profile | Cue focus |
|------|-------------------|-----------|
| `subtle` | Low linguistic edit | Stock vocab only; preserves most assistant register |
| `balanced` | Medium-low fake α, medium authentic linguistic | Default: strip slop + structural + soul |
| `full` | Lower fake α, higher authentic linguistic | + filler, negative parallelism, superficial -ing |
| `anti-detector` | Lowest detectable AI fingerprint | full + lexical_targets + detector loop |
| `voice-match` | Match user α | Phase 4 stylometry → LLM prompt |

### Coverage scorecard (honest)

| Cue dimension | unslop coverage | Gap |
|---------------|-----------------|-----|
| **Perceptual** | ~0% (text tool) | No avatar/UI/typing-indicator control |
| **Linguistic** | ~85% | No AnthroScore/HumT integration; no cultural hedge calibration |
| **Behavioral** | ~30% | Removes fake proactivity; no turn-taking/proactivity design |
| **Cognitive** | ~40% | Strips fake reasoning; doesn't add calibrated uncertainty or genuine transparency |

**Key insight from repo synthesis (`docs/research/15-academic-papers-llm-humanization/A-academic.md` §5.6):** "Most open humanizers cover only linguistic." unslop is above average because of reasoning-strip + behavioral-adjacent rule families, but still fundamentally a **linguistic-register humanizer**.

---

## Integration recommendations for unslop

### Short term (documentation / eval framing)

1. **Map existing rules to four cues** in `docs/research/IMPLEMENTATION_TRACE.md` — use this memo's table as SSOT.
2. **Cite Xiao et al. in anti-detector boundaries:** calibrate α to artifact competence; unslop lowers *misleading* cues, not all human-like language.
3. **Phase 6 eval report:** tag which cue dimension shifted (manual rubric extension — even 4 checkboxes per fixture).

### Medium term (optional metrics)

4. **AnthroScore/HumT read-only probe** on before/after text — linguistic α delta without making them optimization targets (HumT warmth/status tradeoff may conflict with "direct engineer voice").
5. **Cognitive cue lint:** flag remaining signposting/reasoning preludes not caught by regex ("Let me think step by step" — currently explicitly NOT stripped by `reasoning.py`).

### Long term (out of scope unless product expands)

6. **Behavioral cue controls** for agent plugins (response length caps, proactivity toggles) — belongs in hooks/skills, not `humanize.py`.
7. **Perceptual layer** — N/A for file rewriter.

### What NOT to do

- Do not treat Humanizing Machines as a detector-evasion paper — it doesn't benchmark humanizers.
- Do not optimize blindly for high linguistic α — paper Section 4.2 warns trust inflation + sharper backlash on failure.
- Do not conflate unslop with companion/chatbot humanization (high cognitive α) — default modes target professional prose.

---

## Key quotes (verified against arXiv v2)

> "Anthropomorphism should instead be treated as a concept of design that can be intentionally tuned to support user goals."

> "Cues are categorized into four dimensions: perceptive, linguistic, behavioral, and cognitive."

> "We treat the aggregate intensity of perceptual, linguistic, behavioral, and cognitive cues as a calibrated parameter α that designers can dial up or down to match the artifact's system competence."

> "Currently, indices such as HUMT quantify linguistic cues, but measures for behavioral and cognitive cues are still lacking for NLP researchers and form a crucial research avenue."

> "We did not conduct empirical evaluations, user studies, or automated cue quantification at scale."

---

## Cross-references in unslop repo

| Path | Content |
|------|---------|
| `docs/research/15-academic-papers-llm-humanization/A-academic.md` §5.6 | Four-cue checklist vs open humanizers |
| `docs/research/15-academic-papers-llm-humanization/B-industry.md` §20b | Industry summary |
| `docs/research/13-anthropomorphism-user-perception/` | Risk-centric literature cluster |
| `docs/research/research-updating.md` | Flagged as missing until April 2026 update |
| `unslop/scripts/humanize.py` | Phase 1/2/5 orchestration |
| `unslop/scripts/reasoning.py` | Cognitive cue strip |
| `skills/unslop/SKILL.md` | Mode definitions, anti-detector boundaries |

---

## Related papers (full URL index)

| Paper | URL |
|-------|-----|
| Dehumanizing Machines (Cheng et al., ACL 2025) | https://aclanthology.org/2025.acl-long.1259/ |
| AnthroScore (Cheng et al., EACL 2024) | https://arxiv.org/abs/2402.17227 |
| HumT / DumT (Cheng et al., 2025) | https://arxiv.org/abs/2502.13259 |
| Linguistic anthropomorphism taxonomy (DeVrio et al., CHI 2025) | https://doi.org/10.1145/3706598.3713307 |
| Humanizing LLMs survey (Dong et al., 2025) | https://arxiv.org/abs/2505.00049 |
| AI Automatons (Olteanu et al., 2025) | https://arxiv.org/abs/2503.02250 |
| InCharacter (Wang et al., ACL 2024) | https://aclanthology.org/2024.acl-long.108/ |
| Embracing Contradiction (Dai & Xiao, 2025) | https://arxiv.org/abs/2505.18139 |
| Mirages on anthropomorphism (Abercrombie et al., EMNLP 2023) | https://aclanthology.org/2023.emnlp-main.288/ |
| Blame the bot (Crolic et al., J Marketing 2022) | https://doi.org/10.1177/00222429211045687 |
| ELIZA effect (Weizenbaum, 1966) | foundational — cited in paper |
| Uncanny Valley (Mori et al., 2012) | https://doi.org/10.1109/MRA.2012.2192811 |

---

## Bottom line for unslop maintainers

Humanizing Machines gives unslop a **design vocabulary**, not a new benchmark to beat. The actionable mapping:

- **Linguistic:** already the core product (`humanize.py` Phase 2 + 1 + 5 + optional lexical_targets)
- **Behavioral:** partial via sycophancy/signposting/knowledge-cutoff removal
- **Cognitive:** partial via `--strip-reasoning` and hedging/signposting removal
- **Perceptual:** out of scope

unslop's philosophy aligns with **capability–expectation alignment**: strip cues that simulate competence/warmth the system doesn't have; add cues (contractions, burstiness) that match a competent human writer. That is **calibrated α**, not maximum anthropomorphism — and it sits cleanly between Cheng's dehumanization inventory and Xiao's four-cue design framework.
