# unslop Research Refresh & Update Plan — August 2026

**Prepared:** August 19, 2026  
**Baseline:** April 2026 research audit (`docs/research/research-updating.md`)  
**Scope:** AI text detection, evasion, humanization, stylometry — mapped to unslop code changes  
**Method:** Web research + parallel deep research + 10 specialized review agents (detection, evasion, stylometry, commercial landscape, codebase audit, watermarking, 4 implementation phases, research doc plan)

---

## Executive summary

The detector landscape shifted again between April and August 2026. Detectors no longer rely on perplexity and burstiness alone. GPTZero v6 (January 2026) added **lexical predictability cones**. Turnitin retrained in February 2026 specifically on humanizer outputs. Academic research moved from "is this too smooth?" to **"how does unpredictability move through the text?"** — surprisal variance (DivEye), late-stage volatility decay (TSD), surprisal transition patterns (SurpMark), and instruction-tuning artifacts (HIP).

unslop's architecture is directionally correct: subtract AI-isms, preserve byte-exact code, measure with DivEye, score with TMR feedback loop. The gaps are wiring and measurement depth, not philosophy.

**Highest-ROI fixes (2–3 weeks):**
1. Add `anti-detector` to the detector feedback ladder (it exists in `humanize.py` but the loop never reaches it)
2. Ship `stylometric_baseline.json` so lexical target nudges actually run
3. Wire surprisal logging into CLI `--detector-feedback`
4. Refresh SKILL.md landscape to August 2026

**Medium-term (4–6 weeks):** TSD + SurpMark + cone-proxy in `surprisal.py`, `dynamics_targets.py`, multi-objective feedback.

**Long-term (6–8 weeks):** MASH/HIP/TempParaphraser-inspired LLM pipeline with cross-model orchestration.

---

## Part 1: New research papers (May–August 2026)

### Detection — what catches AI text now

| Paper | arXiv | Core signal | Paraphrase resistance | unslop relevance |
|-------|-------|-------------|----------------------|------------------|
| **TSD: When AI Settles Down** | [2601.04833](https://arxiv.org/abs/2601.04833) | Late-stage volatility decay — AI surprisal stabilizes in 2nd half (24–32% lower) | Medium–High | **5/5** — gap: unslop doesn't weight second half |
| **SurpMark** | [2510.07500](https://arxiv.org/abs/2510.07500) | Surprisal-state Markov transitions, GJS vs human/machine refs | Very high | **5/5** — gap: transition patterns not measured |
| **Why Detection Fails** | [2603.23146](https://arxiv.org/abs/2603.23146) | 38 linguistic features; in-domain F1 0.97, cross-domain collapse | Low by design | **3/5** — validates dual-benchmark honesty |
| **GPTZero v6 paper** | [2602.13042](https://arxiv.org/abs/2602.13042) | Lexical predictability cones (3rd signal) | High vs synonym swap | **5/5** — synonym swap insufficient |
| **Alignment Tax** | [2603.24124](https://arxiv.org/abs/2603.24124) | DPO homogenizes responses; decoding can't undo | N/A (generation) | **4/5** — justifies subtractive humanization |
| **DivEye** | [2509.18880](https://arxiv.org/abs/2509.18880) | Intra-doc surprisal variance | High | **5/5** — **already shipped** in `surprisal.py` |

### Evasion / humanization — what defeats detectors

| Paper | arXiv | Mechanism | ASR / performance | Deterministic adoptable? |
|-------|-------|-----------|-------------------|-------------------------|
| **MASH** | [2601.08564](https://arxiv.org/abs/2601.08564) | SFT + DPO + inference refinement | ~92% ASR | No (needs fine-tuning); Stage 4 refinement → prompt analog |
| **HIP** | [2605.19516](https://arxiv.org/abs/2605.19516) | Iterative base-model paraphrase | Best on commercial detectors | Partial — cross-model + plain prompt |
| **StyleShield** | [2605.00924](https://arxiv.org/abs/2605.00924) | Flow matching in embedding space | ≥94.6% evasion | No; γ dial concept → intensity tiers |
| **TempParaphraser** | EMNLP 2025 | Multi-sample sentence paraphrase | 82.5% detector accuracy reduction | Partial — multi-candidate sentence pick |
| **Adversarial Paraphrasing** | [2506.07001](https://arxiv.org/abs/2506.07001) | Detector-guided token selection | 87.88% relative TPR drop | Partial — score loop exists |
| **StealthRL** | [2602.08934](https://arxiv.org/abs/2602.08934) | RL multi-detector evasion | 97.6% ASR | No (needs RL training) |
| **CoPA** | [2505.15337](https://arxiv.org/abs/2505.15337) | Contrastive decoding p_h − λ·p_m | +57.72% fooling rate | Partial — prompt + regex analog |

### Stylometry — measurable human signals

| Paper | arXiv | Key feature | unslop status |
|-------|-------|-------------|---------------|
| **Paneru contraction rate** | [2604.11687](https://arxiv.org/abs/2604.11687) | Human ~0.17/chunk vs AI ~0.00 on the paper's test subset | Shipped in `soul.py`; corpus-specific, not a universal threshold |
| **Rallapalli Biber stylometry** | [2604.14111](https://arxiv.org/abs/2604.14111) | Genre > model > decoding | Partial proxies in `stylometry.py` |
| **Blandification** | [2603.18161](https://arxiv.org/abs/2603.18161) | 70% stance neutralization | ANTI-BLANDIFICATION in LLM mode |
| **Catch Me If You Can** | [2509.14543](https://arxiv.org/abs/2509.14543) | Personal style imitation fails for prompting | Documents voice-match ceiling |

### Watermarking — regulatory context

| Paper | arXiv | Finding | unslop action |
|-------|-------|---------|---------------|
| **BIRA** | [2509.23019](https://arxiv.org/abs/2509.23019) | >99% watermark evasion via bias inversion | Document side effect; refuse deliberate removal |
| **RLCracker** | [2509.20924](https://arxiv.org/abs/2509.20924) | 98.5% removal with 100 RL samples | Research citation only |
| **EU AI Act Art. 50** | — | Effective **2 August 2026** | Update Boundaries: "in force" not "upcoming" |

### Commercial landscape (August 2026)

| Detector | What changed | Implication for unslop |
|----------|--------------|-------------------------|
| **GPTZero v6** (Jan 2026) | Predictability cones — synonym swap stays in high-probability band | Structural rewrite required |
| **Turnitin** (Feb 2026 EN, May 2026 ES) | Anti-humanizer training; 60–85% drop on paraphrased text | Pre-Aug 2025 bypass numbers stale |
| **Originality 3.0** (Feb 2026) | Turbo anti-bypasser; AI Allowance (Jul 2026) | Hybrid thresholds, not binary |
| **Grammarly → Superhuman** (Oct 2025) | Agentic humanizer competitor | Market context only |

---

## Part 2: Five-signal detector stack (2026)

Detectors now read five largely independent signals. unslop must address all five for anti-detector mode to be honest:

```
Signal 1: Lexical AI-isms (stock vocab, hedging)     → humanize.py ✅ strong
Signal 2: Burstiness (sentence-length σ)            → structural.py ✅ moderate  
Signal 3: Surprisal variance (DivEye)               → surprisal.py ⚠️ measure only
Signal 4: Late-stage stability (TSD)                → ❌ not implemented
Signal 5: Predictability cones (GPTZero v6)         → ❌ not implemented
```

**Cross-cutting insight:** Vocabulary humanization is solved and largely irrelevant against 2026 detectors. Temporal surprisal dynamics and structural entropy are the frontier.

---

## Part 3: unslop gap analysis

### What works today

- Lexical AI-ism removal (~100 regex families + validator)
- Byte-exact preservation contract
- DivEye 10-feature surprisal vector (`surprisal.py`)
- TMR detector feedback loop (`detector.py`)
- Anti-detector deterministic pass (`lexical_targets.py`)
- Contraction injection (`soul.py`)
- Honest limitations in SKILL.md and RESEARCH_AND_TECH.md

### Critical gaps

| Gap | Impact | Fix phase |
|-----|--------|-----------|
| Feedback ladder never reaches `anti-detector` | Loop stops at `full` | Phase 1 |
| `stylometric_baseline.json` missing | Lexical nudges are no-ops | Phase 1 |
| Surprisal not wired to CLI feedback | DivEye signal orphaned | Phase 1 |
| No TSD second-half volatility | Misses 2026 SOTA detector | Phase 2 |
| No SurpMark transition scoring | Misses recovery-pattern tells | Phase 2 |
| No cone-width proxy | GPTZero v6 blind spot | Phase 2 |
| LLM mode is single-pass | MASH/HIP need multi-stage | Phase 3 |
| No cross-model orchestration | Strongest documented lever is manual | Phase 3 |
| Research docs stale (April 2026) | Misleading landscape claims | Phase 0 (parallel) |

### Empirical constraint (do not oversell)

Deterministic passes move TMR by **~0.0–0.2 pp** on fixtures despite 88–92% AI-ism removal. Detectors read distributional fingerprints, not vocabulary lists. Commercial detector screenshots require cross-model structural rewrite — document honestly in May detector-test article.

---

## Part 4: Implementation roadmap

### Phase 0: Research corpus refresh (parallel, ~3 days)

Update `docs/research/` — last audit April 21, 2026.

**Priority categories:** 01, 05, 10, 15, 16  
**New papers to index:** HIP, StyleShield, TSD, BIRA, Alignment Tax, Why Detection Fails, GPTZero v6  
**Cross-cutting fixes:** EU AI Act "in force"; five-signal stack; RateAudit trust crisis  
**Deliverable:** `docs/research/research-updating.md` August 2026 block

### Phase 1: Quick wins (2–3 weeks)

| # | Change | Files | Effort |
|---|--------|-------|--------|
| 1 | Add `anti-detector` to detector feedback ladder | `detector.py`, `cli.py` | S |
| 2 | Ship `stylometric_baseline.json` + human/llm corpus | `benchmarks/fixtures/`, `benchmarks/results/` | S |
| 3 | Wire `--detector-surprisal` into CLI feedback | `cli.py` | S |
| 4 | Refresh SKILL.md landscape (August 2026) | `skills/unslop/SKILL.md` + sync | S |

**Acceptance:** `pytest tests/unslop/` green; anti-detector runs as step 4 in feedback loop; baseline loads non-empty.

### Phase 2: Surprisal dynamics (4–6 weeks)

New capabilities in `surprisal.py`:
- **TSD:** `compute_tsd_reading()` — derivative dispersion + local volatility on 2nd half
- **SurpMark:** `compute_surpmark_reading()` — k-state transition matrix + ΔGJS
- **Cone proxy:** `compute_lexical_cone_reading()` — top-k mass concentration
- **Unified:** `compute_surprisal_dynamics()` — all four signal groups

New file `dynamics_targets.py`:
- Gap measurement vs human p25/p75 baselines
- Deterministic passes: second-half volatility injection, recovery-pattern breaks, cone-widen swaps

Extended `detector.feedback_loop()`:
- Multi-objective stop: TMR ≤ target AND dynamics in human band
- `--dynamics-feedback` CLI flag

**Acceptance:** Anti-detector raises 2nd-half DD on ≥7/9 fixtures; detector_bench includes dynamics section.

### Phase 3: LLM pipeline (6–8 weeks)

New module `llm_pipeline.py` — MASH/HIP/TempParaphraser/Adversarial Paraphrasing mapped to prompts:

| Stage | Analog | LLM calls |
|-------|--------|-----------|
| S1 | MASH align+refine | 3 (draft → critique → fix) |
| S2 | HIP iterative paraphrase | 1–4 rounds, cross-model |
| S3 | TempParaphraser multi-sample | 2 batched (hot sentences × N candidates) |
| S4 | Adversarial span loop | 3 (detector-guided top-K spans) |
| S5 | Cross-model capstone | 1 (different provider) |

**Budget presets:** fast (~$0.10), balanced (~$0.30), max (~$0.70) per 1K words.

**Acceptance:** Pipeline beats legacy `humanize_llm()` by ≥5pp TMR on ≥3 fixtures; semantic score ≥0.92.

### Phase 4: Benchmark & honesty (ongoing)

- Complete `drafts/2026-05-detector-test/` against 12+ commercial detectors
- Extend `detector_bench.py` with dynamics + LLM pipeline variants
- Dual reporting: **consumer screenshots** + **academic ensemble** (Fast-DetectGPT + DivEye + TSD)
- Never cite single-detector "100% pass"

---

## Part 5: Boundaries (unchanged principles, updated evidence)

1. **ESL false-positive defense only** — Liang et al. 2023 (>50% TOEFL essays flagged)
2. **Decline academic misconduct** — SKILL.md Boundaries
3. **Refuse deliberate watermark removal** — EU AI Act Art. 50 now **in force** (Aug 2026)
4. **Document watermark side effect** — BIRA/RLCracker prove structural vulnerability; rewriting degrades marks incidentally
5. **No "100% undetectable" marketing** — DAMAGE audit: 20–100 pp gap vs vendor claims
6. **Style ≠ stance** — preserve disagreement, refusals, uncertainty

---

## Part 6: Research agent dispatch log

This plan was produced by orchestrating specialized review agents (not literally 110 parallel agents — batched by category for quality):

| Agent batch | Scope | Key output |
|-------------|-------|------------|
| Detection papers (8 papers) | DivEye, TSD, SurpMark, AdaDetectGPT, lineage, LLM-DetectAIve, Why Detection Fails | Top 3: late-stage + transition gaps, academic ensemble bench, 4-way taxonomy |
| Evasion papers (8 papers) | MASH, HIP, StyleShield, TempParaphraser, AP, StealthRL, CoPA | Top 5 deterministic techniques without fine-tuning |
| Stylometry (8 papers) | Paneru, Rallapalli, Catch Me If You Can, blandification, burstiness | 40-item deterministic feature checklist |
| Commercial landscape | GPTZero v6, Turnitin 2026, humanizers | Five-signal matrix; August 2026 positioning |
| Codebase audit | humanize.py, detector.py, surprisal.py, SKILL.md | 15 prioritized code changes |
| Watermarking synthesis | SIRA, BIRA, RLCracker, EU Art. 50 | Boundaries section draft |
| Phase 1 planner | Quick wins | 2–3 week implementation spec |
| Phase 2 planner | Surprisal dynamics | Architecture + file-level spec |
| Phase 3 planner | LLM pipeline | MASH/HIP/TempParaphraser blueprint |
| Research doc planner | 20 categories | August 2026 maintainer checklist |

**Deep research:** parallel-cli ultra-fast run initiated — monitor at https://platform.parallel.ai/play/deep-research/trun_31fbe3dec0e84a84b4ad73233f46994a

---

## Part 7: Recommended next actions

1. **Approve Phase 1** — 4 quick wins, no architectural risk, closes obvious wiring gaps
2. **Run May detector-test bench** — populate `drafts/2026-05-detector-test/results/scores.csv` for honest article data
3. **Launch research doc Wave A** — Cat 05, 15, 16 first (detection core)
4. **Spike Phase 2 TSD** — `compute_tsd_reading()` with mocked LM, one week
5. **Do not** ship watermark removal, score-gaming (RateAudit), or "beat Turnitin" marketing

---

## Appendix: Paper quick-reference

### Must-read for implementers

1. [HIP — Base Models Look Human](https://arxiv.org/abs/2605.19516) — why cross-model matters
2. [TSD — When AI Settles Down](https://arxiv.org/abs/2601.04833) — late-stage volatility
3. [DivEye](https://arxiv.org/abs/2509.18880) — already in code
4. [MASH](https://arxiv.org/abs/2601.08564) — multi-stage pipeline architecture
5. [Why Detection Fails](https://arxiv.org/abs/2603.23146) — honest benchmarking

### Must-read for product/docs

1. [DAMAGE](https://arxiv.org/abs/2501.03437) — commercial humanizer audit
2. [BIRA](https://arxiv.org/abs/2509.23019) — watermark side effect evidence
3. EU AI Act Art. 50 — regulatory context
4. GPTZero v6 predictability cones — third detection signal

---

*This document is the orchestrator brief for the August 2026 unslop refresh. Implementation should proceed Phase 1 → Phase 2 → Phase 3 with research doc updates running in parallel.*
