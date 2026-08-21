# Agent #36 — HumanLLM Benchmark (arXiv 2601.10198)

**Topic:** HumanLLM anthropomorphism benchmark — what it measures, eval design, community adoption, unslop integration  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**HumanLLM is not an AI-text detector benchmark and not a humanizer evasion benchmark.** It evaluates **psychological anthropomorphism** in Role-Playing Language Agents (RPLAs): whether a model expresses 244 documented cognitive patterns (100 Big Five personality traits + 144 social-cognitive mechanisms) with fidelity, including when 2–5 patterns reinforce, conflict, or modulate each other in situ.

The paper’s main eval contribution is **dual-level checklist scoring** — Individual Pattern Expression (IPE) and Multi-Pattern Dynamics (MPD) — which achieves **r ≈ 0.90** agreement with human psychology experts, while holistic “anthropomorphism” rubrics (CoSER) show **normative confounding** (r ≈ 0.43–0.61): LLM judges reward prosocial behavior and punish psychologically accurate but socially undesirable traits.

For **unslop**, HumanLLM is a **complementary upstream axis**, not a drop-in replacement for `detector_bench.py`. unslop optimizes **surface register** (slop removal, burstiness, voice-match, optional TMR/Desklib feedback). HumanLLM optimizes **cognitive-process simulation** (inner thoughts, embodied actions, multi-pattern dialogue). The papers align philosophically — cognitive modeling beats behavioral mimicry — but measure different layers. Recommended integration: add a **HumanLLM-verbal slice** eval that humanizes scenario dialogue turns and scores IPE/MPD delta, plus cite HumanLLM’s normative-confounding result in anti-detector ethics docs.

**Adoption is early:** ACL 2026 long paper, public GitHub release, ~7 stars, no mainstream HuggingFace weights yet, no HN/Reddit traction found.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **arXiv preprint** | https://arxiv.org/abs/2601.10198 |
| **arXiv HTML (v4)** | https://arxiv.org/html/2601.10198v4 |
| **ACL Anthology (2026.acl-long.1783)** | https://aclanthology.org/2026.acl-long.1783/ |
| **ACL PDF** | https://aclanthology.org/2026.acl-long.1783.pdf |
| **DOI** | https://doi.org/10.18653/v1/2026.acl-long.1783 |
| **GitHub (dataset + code)** | https://github.com/YJGoodbye2024/HumanLLM |
| **Paper Notes (ACL 2026 summary)** | https://en.papernotes.org/ACL2026/llm_evaluation/humanllm_benchmarking_and_improving_llm_anthropomorphism_via_human_cognitive_pat/ |
| **alphaXiv mirror** | https://www.alphaxiv.org/abs/2601.10198 |
| **Sibling paper (personalization, different work)** | https://arxiv.org/abs/2601.15793 |

### Related eval benchmarks (detector / humanizer axis — *not* HumanLLM)

| Benchmark | URL | What it measures |
|-----------|-----|------------------|
| **BUST** (NAACL 2024) | https://aclanthology.org/2024.naacl-long.444/ | Detector systems on 25K human vs 7-LLM texts across 10 tasks |
| **RAID** | https://arxiv.org/abs/2405.07926 | Robustness of AI-text detectors under paraphrase attacks |
| **MGTBench / TH-Bench** | https://arxiv.org/abs/2310.05172 | Humanizer attack success vs detectors |
| **HLB** (Human-Likeness Benchmark) | https://arxiv.org/abs/2409.15890 | 10 psycholinguistic experiments, capability ≠ humanlikeness |
| **HumT / DumT** | https://arxiv.org/abs/2502.13259 | Token-probability human-tone metric; warmth/status tradeoff |
| **CoSER** (external eval in HumanLLM) | https://arxiv.org/abs/2506.06639 | Holistic Anthropomorphism + Character Fidelity (critiqued by HumanLLM) |
| **LifeChoice** | https://arxiv.org/abs/2406.07249 | Persona-driven life decisions |
| **CroSS-MR** | https://arxiv.org/abs/2407.01835 | Character motivation recognition |

### unslop internal references

| Resource | Path |
|----------|------|
| Research synthesis (Cat 01) | `docs/research/01-prompt-engineering-humanization/A-academic.md` §20 |
| Agentic humanness (Cat 19) | `docs/research/19-agentic-autonomous-thinking/SYNTHESIS.md` |
| Detector bench harness | `benchmarks/detector_bench.py` |
| Live detector loop | `unslop/scripts/detector.py` |
| Anti-detector skill spec | `skills/unslop/SKILL.md` §anti-detector |

---

## What HumanLLM measures

### Problem framing

Existing persona/RPLA methods treat personality as **isolated label → behavior mappings** (“extroverted” → “talkative”). Real humans express **dynamic pattern interactions**: a talkative person goes quiet under spotlight effect; an assertive person yields under conformity pressure. HumanLLM models patterns as **interacting causal forces** (Lewin field theory), not static tags.

### Pattern taxonomy (244 total)

| Dimension | Count | Source |
|-----------|-------|--------|
| **Personality traits** | 100 | Goldberg’s unipolar Big Five markers (20 per dimension) |
| **Social-cognitive patterns** | 144 | Cognitive biases, social influence, evolutionary psych, motivation research (~12K papers total, ~50 per pattern) |

Each pattern has: **Definition**, **Core Mechanisms**, **Real-World Manifestations** (Figure 1 in paper).

### Dataset scale

| Statistic | Value |
|-----------|-------|
| Scenarios | 11,359 |
| Avg patterns per scenario | 3.5 (range 2–5) |
| Characters per scenario | 2–6 |
| Turns per conversation | 12–20 (mean 16.4) |
| Pattern-level checklist items | 12–15 per pattern |
| Scenario-level checklist items | 2–6 per target character |
| SFT samples (ShareGPT) | 30,543 from 10,265 train scenarios |
| Training mixture | 4:4:2 HumanLLM : OpenThoughts-114k : CoSER |

### Turn structure (what gets scored)

Each dialogue turn has three channels:

1. **Inner thoughts** — `[brackets]`
2. **Physical actions** — `(parentheses)`
3. **Verbal expressions** — plain dialogue

Evaluation targets **pattern expression across all three**, not final polished prose alone.

### Core metrics

#### IPE — Individual Pattern Expression

- Uses **pattern-level checklists** (12–15 value-neutral behavioral indicators per pattern).
- Question: “Does this character exhibit the documented mechanisms of pattern X?”
- Context-independent — applies whether the scene is a boardroom or a breakup.

#### MPD — Multi-Pattern Dynamics

- Uses **scenario-level checklists** (2–6 items per target character).
- Question: “When patterns A and B co-occur in this situation, does behavior reflect their interaction?”
- Example: assertive + spotlight effect → outward confidence with internal audience anxiety, not generic “confident speech.”

#### Scoring protocol

- **Judge:** GPT-5-mini (deliberately not Gemini, which generated training data).
- **Scale:** Ternary per checklist item: +1 satisfied / 0 not exhibited / −1 violated.
- **Aggregation:** Mean per sample → mean across samples → linear map [−1,+1] to [−100%,+100%].
- **Stability:** 3 independent judge runs; σ < 2.1% across models.

#### Human alignment validation (n=100 scenarios, 3 psychology experts)

| Metric family | Metric | Human vs LLM judge r | Systematic bias Δ |
|---------------|--------|----------------------|-------------------|
| Holistic (CoSER) | Anthropomorphism | 0.43 | −30.8 |
| Holistic (CoSER) | Character Fidelity | 0.61 | −17.7 |
| Checklist (HumanLLM) | IPE | **0.90** | −0.6 |
| Checklist (HumanLLM) | MPD | **0.88** | +3.7 |

**Normative confounding:** Holistic rubrics conflate “good anthropomorphism” with prosocial behavior. A character correctly exhibiting ultimate attribution error (blaming out-groups defensively) scores ~5/100 on holistic metrics but passes checklist items grounded in pattern definitions.

### Eval splits (generalization)

From GitHub `Dataset/split/`:

| Split | Purpose |
|-------|---------|
| `train.json` | SFT (10,265 scenarios) |
| `id_eval.json` | In-domain patterns |
| `ood_eval.json` | Out-of-domain unseen patterns |
| `mixed_eval.json` | Mixed generalization |

Reported main results average **ID + OOD + Mixed**.

### Main model results (Table 2, paper)

| Model | IPE (%) | MPD (%) |
|-------|---------|---------|
| Gemini 3 Pro | 41.3 | 85.1 |
| Claude Sonnet 4.5 | 34.8 | 79.5 |
| GPT-5 | 15.5 | 43.4 |
| Qwen3-32B | 26.0 | 65.8 |
| Qwen3-235B | 34.3 | 72.5 |
| DeepSeek-R1 | 23.3 | 69.0 |
| **HumanLLM-8B** | 25.7 | **70.3** |
| **HumanLLM-32B** | 32.8 | 73.6 |

**Headline finding:** HumanLLM-8B beats Qwen3-32B on MPD (+4.5 pp) at 4× fewer parameters — psychological training data matters more than scale for multi-pattern dynamics.

**GPT-5 underperforms:** Strong instruction-following → literal, shallow role-play; “helpful assistant” behaviors conflict with cognitively biased characters.

### External benchmarks (modest gains)

| Model | LifeChoice | CroSS-MR |
|-------|------------|----------|
| GPT-5 | 85.53 | 62.25 |
| HumanLLM-32B | 50.64 | 64.27 |
| Qwen3-32B | 47.71 | 63.37 |

HumanLLM’s large IPE/MPD gains **do not fully transfer** to outcome-based role-play benchmarks (decisions, motivation ID). Paper argues those benchmarks miss cognitive-process fidelity.

### Ablations (negative transfer)

Training Qwen3-8B on OpenThoughts + CoSER **without** HumanLLM data **hurts** both metrics vs base (IPE 18.6→9.1, MPD 54.4→31.3). Generic instruction-following and conventional role-play data suppress latent psychological simulation. HumanLLM data acts as an **anchor** against prosocial collapse.

---

## Detector / humanizer eval design — how HumanLLM fits (and doesn’t)

### Critical distinction

| Axis | Question | Example benchmarks | HumanLLM? |
|------|----------|-------------------|-----------|
| **Detection** | Is this text machine-generated? | BUST, RAID, GPTZero, TMR, Desklib | **No** |
| **Humanizer attack** | Does rewriting fool detectors? | MGTBench, MASH ASR, DAMAGE audit | **No** |
| **Surface humanlikeness** | Does text read naturally? | HumT/DumT, HLB, stylometry | **Partial overlap** |
| **Cognitive anthropomorphism** | Does agent simulate psychological processes? | **HumanLLM (IPE/MPD)**, ToM benches | **Yes** |

HumanLLM evaluates **whether the model thinks like a human under specified psychology**, not whether a classifier assigns low AI probability.

### Eval design innovations relevant to unslop

1. **Decomposed checklists beat holistic scores.** Same lesson as unslop’s split between `validate.py` AI-ism residuals vs subjective “sounds human.” Holistic LLM-judge anthropomorphism is unreliable (r=0.43).

2. **Value-neutral indicators.** Checklist items describe observable behavior without moral judgment. unslop’s anti-detector mode should not conflate “human” with “nice” — HumanLLM proves judges do exactly that.

3. **Multi-pattern dynamics as hard case.** Single-trait prompts are easy; interacting patterns are where surface humanizers fail. unslop’s regex/skill layer has **no representation** of pattern interaction.

4. **Synthetic training data with expert validation.** Pattern summaries validated by 3 psychology annotators (Krippendorff α 0.58–0.76). Generation via Gemini 2.5 Pro + Claude Sonnet 4.5; judge via GPT-5-mini to avoid generator-evaluator overlap.

5. **Three-channel output (thought / action / speech).** Closest academic formalization of unslop’s “reason privately, humanize publicly” — but HumanLLM **trains** all three; unslop only humanizes the public channel.

### What a detector-centric eval of HumanLLM-trained text would show (hypothesis)

Not reported in paper. Speculative based on architecture:

- **Verbal expressions** from HumanLLM-8B may carry **lower detector scores** than base Qwen3-8B if cognitive grounding increases burstiness and reduces template prosocial phrasing.
- **Inner thoughts / actions** are unlikely to appear in typical detector inputs (essays, emails).
- **Negative-transfer finding** implies generic humanizers that push “helpful assistant” tone may **decrease** IPE/MPD even if detectors improve — optimization conflict.

unslop should **not** claim HumanLLM validation without running IPE/MPD; detector-only scores are an insufficient proxy.

---

## Community adoption (August 2026)

| Signal | Status |
|--------|--------|
| **Venue** | ACL 2026 long paper, San Diego, July 2026; pp. 38486–38517 |
| **arXiv** | Posted Jan 2026; v4 available |
| **GitHub** | https://github.com/YJGoodbye2024/HumanLLM — public dataset layout documented; **~7 stars, 0 forks** (early) |
| **HuggingFace weights** | **Not found** for HumanLLM-8B/32B under YJGoodbye2024 (paper says “model” released; may be in repo README not yet mirrored to HF) |
| **Name collision** | `HumanLLMs` HF org (https://huggingface.co/HumanLLMs) is **unrelated** — “Human-Like-Llama3” from arXiv 2501.05032 |
| **Blog / community** | Paper Notes ACL 2026 entry; no HN front-page or major Reddit threads found |
| **Citations** | Too early for meaningful count; listed in unslop research compendium (Cats 01, 15, 19) |
| **Industry** | Hello Group + Fudan + JHU (Jen-tse Huang) authorship; companion AI / social simulation use case |

**Assessment:** Credible ACL venue + full artifact release, but **pre-adoption** in practitioner humanizer/detector ecosystem. Expect 6–12 months before downstream tools reference IPE/MPD.

### Related sibling work (do not conflate)

| Paper | arXiv | Focus |
|-------|-------|-------|
| **HumanLLM (this memo)** | 2601.10198 | Cognitive pattern benchmark + HumanLLM-8B/32B |
| **HumanLLM: Towards Personalized Understanding** | 2601.15793 | 5.5M user-log Cognitive Genome; personalized voice/behavior |
| **Humanizing LLMs survey** | 2505.00049 | Psychological measurement landscape |

unslop’s `A-academic.md` §20 accidentally merges 2601.10198 with Cognitive Genome claims — **fix in separate doc PR**; they are distinct papers from overlapping author networks.

---

## unslop as eval target — integration plan

### Alignment (why HumanLLM matters to unslop)

| HumanLLM thesis | unslop expression |
|-----------------|-------------------|
| Cognitive modeling > behavioral mimicry | “Reason privately, humanize publicly”; agentic humanness research thread |
| Surface role-play fails on pattern dynamics | unslop removes surface slop but doesn’t model psychology |
| Generic “helpful assistant” training hurts fidelity | Subtract-don’t-add; anti-sycophancy rules |
| Holistic humanlikeness ≠ accurate simulation | Anti-detector ≠ “sounds nice”; `[VERIFY]` over fluent wrongness |
| Multi-turn anchor (12–20 turns) | Mode-tracker drift checks at turns 8–16 |

HumanLLM is the **closest peer-reviewed formalization** of unslop’s long-term thesis (Cat 19): humanize the **process**, not just the paragraph.

### Misalignment (what unslop cannot claim today)

- unslop is a **post-hoc rewriter**, not an RPLA with memory/planning/reflection.
- No IPE/MPD checklist infrastructure.
- `anti-detector` optimizes classifier scores + stylometry, which HumanLLM **does not measure** and may **anti-correlate** with negative-trait pattern expression.
- Deterministic regex pass targets **AI-isms**, not spotlight effect vs assertive tension.

### Proposed eval protocol: `humanllm_verbal_bench.py`

**Goal:** Measure whether unslop improves or harms **verbal-expression humanlikeness** on psychologically grounded dialogue — without claiming full IPE/MPD certification.

```
Pipeline:
1. Sample N scenarios from id_eval.json / ood_eval.json (start N=50).
2. Extract target character verbal turns (strip [thoughts] and (actions)).
3. Baseline: score with GPT-5-mini checklist judge (reuse HumanLLM prompt from Appendix F.1).
4. Generate "slopified" variant: add AI-ism template (delve, tricolon, hedging) — simulates pre-unslop assistant output.
5. Run unslop modes: subtle, balanced, full, anti-detector on slopified text.
6. Re-score IPE/MPD on rewritten verbal layer only (thought/action held fixed or omitted).
7. Report: ΔIPE, ΔMPD per mode; preservation failures; detector P(AI) from TMR/Desklib parallel track.
```

**Success criteria (hypothesis to falsify):**

- `balanced` / `full` **recover** IPE lost to slop injection without MPD collapse.
- `anti-detector` may **gain** on TMR while **losing** MPD on negative-trait scenarios (normative confounding stress test).
- `subtle` insufficient for multi-pattern scenes.

**Effort:** ~2–3 days engineering (JSON loader + judge API wrapper + report JSON). Judge cost: ~100 scenarios × ~15 checklist items × 3 runs.

### Skill / docs integration (low effort)

1. **`skills/unslop/SKILL.md`** — Add HumanLLM citation under Principles: holistic “humanlikeness” scores conflate prosocial bias with simulation accuracy (arXiv 2601.10198 §5.5). Supports anti-detector ethics boundary.

2. **`benchmarks/README.md`** — Third axis table: Detection | Slop removal | Cognitive anthropomorphism (HumanLLM).

3. **`docs/research/01-prompt-engineering-humanization/A-academic.md` §20** — Split 2601.10198 from 2601.15793; remove erroneous “Reddit/Twitter logs” claim from §20.

4. **Anti-detector warning** — If user humanizes role-play dialogue with negative cognitive patterns (defensiveness, bias), detector-optimal rewrite may **destroy** psychological fidelity HumanLLM would score highly.

### Not recommended

- Marketing unslop as “HumanLLM SOTA” without running IPE/MPD.
- Replacing `detector_bench.py` with HumanLLM judge (orthogonal metrics).
- Fine-tuning on HumanLLM SFT data for unslop plugin (scope creep; safety/ethics concerns in paper §Ethical Statement).

---

## Limitations & ethics (from paper — relevant to unslop)

| Limitation | Implication for unslop eval |
|------------|----------------------------|
| WEIRD psychology corpus | Voice-match for non-Western users may not align with HumanLLM patterns |
| Synthetic conversations | IPE/MPD on human-written text may behave differently |
| 12–20 turn horizon | unslop session-long drift untested on HumanLLM scale |
| LLM-as-judge (GPT-5-mini) | Same class of risk as using LLM to grade “humanized” prose |
| Safety–fidelity tension | Training/evaluating negative traits; unslop should not amplify manipulation patterns in anti-detector mode |
| Social engineering patterns modeled | Authority bias, conformity, reciprocity — do not optimize unslop for persuasion exploit scenarios |

---

## Key quotes (verbatim from paper)

> “Holistic metrics conflate simulation accuracy with social desirability.”

> “Authentic anthropomorphism requires cognitive modeling—simulating not just what humans do, but the psychological processes generating those behaviors.”

> “Generic instruction-following data may inadvertently suppress the base model’s latent ability to simulate psychological patterns.”

---

## Bottom line for unslop maintainers

| Question | Answer |
|----------|--------|
| Is HumanLLM a detector benchmark? | **No.** |
| Should unslop cite it in anti-detector docs? | **Yes** — for normative confounding and “human ≠ nice.” |
| Should unslop run IPE/MPD evals? | **Optional but high value** as a third benchmark axis alongside slop residuals + detector bench. |
| Does HumanLLM validate unslop today? | **No empirical run yet.** Philosophically aligned; empirically untested. |
| Community maturity | **ACL accepted, artifacts live, adoption nascent.** |

---

## URL index (flat)

- https://arxiv.org/abs/2601.10198
- https://arxiv.org/html/2601.10198v4
- https://aclanthology.org/2026.acl-long.1783/
- https://aclanthology.org/2026.acl-long.1783.pdf
- https://doi.org/10.18653/v1/2026.acl-long.1783
- https://github.com/YJGoodbye2024/HumanLLM
- https://en.papernotes.org/ACL2026/llm_evaluation/humanllm_benchmarking_and_improving_llm_anthropomorphism_via_human_cognitive_pat/
- https://www.alphaxiv.org/abs/2601.10198
- https://arxiv.org/abs/2601.15793
- https://arxiv.org/abs/2505.00049
- https://arxiv.org/abs/2409.15890
- https://arxiv.org/abs/2502.13259
- https://aclanthology.org/2024.naacl-long.444/
- https://arxiv.org/abs/2405.07926
- https://arxiv.org/abs/2506.06639
