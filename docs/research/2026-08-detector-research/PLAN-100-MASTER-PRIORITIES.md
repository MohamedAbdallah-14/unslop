# PLAN-100 — Master Priorities (August 2026 Integration)

**Master Integration Agent:** #100  
**Date:** 2026-08-19  
**Inputs:** UPDATE-PLAN-2026-08.md, SYNTH-81 through SYNTH-96, DEEP-RESEARCH-EXEC-SUMMARY.md, AGENT-MANIFEST-100.md  
**Derived plans:** PLAN-97 (Phase 1 quick wins), PLAN-98 (Phase 2 surprisal dynamics), PLAN-99 (Phase 3 LLM pipeline) — synthesized from UPDATE-PLAN Parts 3–4 where dedicated agent memos were not yet written  
**Output:** Ranked action list, timeline, risk register, explicit non-goals, success metrics  
**Audience:** unslop maintainers — product, engineering, docs, benchmark CI

---

## Executive summary

August 2026 research converges on one product truth: **unslop's philosophy is correct; wiring and measurement depth are wrong.** Lexical AI-ism removal works. Deterministic passes move TMR ~0.0–0.2 pp on fixtures — expected, not a bug. The 2026 detector stack reads five largely independent signals; unslop addresses two well, measures a third without closing the loop, and has zero code for late-stage volatility (TSD), transition dynamics (SurpMark), and predictability cones (GPTZero v6).

**Strategic posture:** Ship honesty and wiring first (Phase 1), then surprisal dynamics (Phase 2), then optional LLM pipeline (Phase 3). Run research doc refresh and May detector-test bench in parallel. Never ship bypass marketing, watermark strip modes, or score-targeting schedulers.

**Top 3 immediate actions:**

1. Wire `anti-detector` into the detector feedback ladder — mode exists, loop never reaches it  
2. Ship `stylometric_baseline.json` — lexical nudges are no-ops without it  
3. Fix SKILL.md attribution errors (Liang citation, Booth/Turnitin conflation) before any landscape refresh

---

## Top 20 actions (ranked)

Priority reflects **ROI × risk reduction × dependency order**. Effort: S (<1 day), M (2–5 days), L (1–3 weeks), XL (4+ weeks).

| Rank | Action | Phase | Effort | Primary source |
|------|--------|-------|--------|----------------|
| **1** | Add `anti-detector` as final step in `detector.feedback_loop()` ladder | P1 | S | SYNTH-83, UPDATE-PLAN |
| **2** | Ship `benchmarks/results/stylometric_baseline.json` (genre-stratified p25/p75) | P1 | S | SYNTH-92, SYNTH-89 |
| **3** | Fix SSOT citation errors: Liang **2304.02819**; remove Booth→Turnitin claims | P0 docs | S | SYNTH-87, SYNTH-82 |
| **4** | Wire `--surprisal-variance` telemetry into `--detector-feedback` JSON output | P1 | S | SYNTH-83, Agent #80 |
| **5** | Refresh `skills/unslop/SKILL.md` landscape to August 2026 (five-signal stack, dual reporting) | P0 docs | S | SYNTH-81, SYNTH-82 |
| **6** | Implement `shield_metrics.py`: TPR@FPR=5%, W-AUROC, SFD, URSS | P1 bench | M | SYNTH-84 |
| **7** | Extend `detector_bench.py`: TPR@FPR, RAID paraphrase/synonym arms, anti-detector matrix | P1 bench | M | SYNTH-84, SYNTH-83 |
| **8** | Run and commit May detector-test bench (`drafts/2026-05-detector-test/results/scores.csv`) | P0 bench | M | SYNTH-82, UPDATE-PLAN |
| **9** | Implement `compute_tsd_reading()` in `surprisal.py` (second-half DD + LV) | P2 | M | SYNTH-81, SYNTH-83, Agent #02 |
| **10** | Add `StylometryContext` wrapper: measure → edit → re-measure in Phase 1–2 pipeline | P2 | M | SYNTH-92 |
| **11** | Parameterize `structural.py` from profile gaps (σ, CV, flat paragraphs) | P2 | M | SYNTH-92, Agent #54 |
| **12** | Multi-objective stop: TMR ≤ target AND dynamics in human band | P2 | M | SYNTH-83, SYNTH-86 |
| **13** | Research doc Wave A: update Cat 05, 15, 16 in `docs/research/` | P0 docs | M | UPDATE-PLAN Phase 0 |
| **14** | CoPA dual-prompt + anti-machine negative in `_INTENSITY_PROMPT_GUIDANCE["anti-detector"]` | P1 | S | SYNTH-85, Agent #28 |
| **15** | `llm_pipeline.py` skeleton + S1 MASH 3-call (draft → critique → fix) | P3 | L | SYNTH-86, UPDATE-PLAN |
| **16** | S2 HIP cross-model template + `UNSLOP_HIP_ROUNDS` env | P3 | M | SYNTH-86, Agent #22 |
| **17** | SurpMark lite: `compute_surpmark_reading()` with frozen ref matrices | P2 | L | SYNTH-81, Agent #03 |
| **18** | Cone-width proxy: `compute_lexical_cone_reading()` for GPTZero v6 analog | P2 | L | SYNTH-81, Agent #13 |
| **19** | Catch Me AV harness: `benchmarks/voice_match_bench.py` (two-axis eval) | P2 eval | M | SYNTH-90, Agent #43 |
| **20** | Boundaries sync: four-question gate, refusal scripts, Art. 50 side-effect copy | P0 docs | S | SYNTH-87, SYNTH-94, SYNTH-95 |

### Rank clusters (why this order)

**Ranks 1–5 (Week 1):** Close obvious wiring gaps and doc lies. Zero architectural risk. Unblocks honest anti-detector claims and lexical_targets.

**Ranks 6–8 (Weeks 2–3):** Measurement infrastructure. Without TPR@FPR and commercial bench data, every product claim is anecdote.

**Ranks 9–12 (Weeks 4–8):** 2026 detector signal gap. TSD + stylometry closed-loop is the highest-value code after wiring.

**Ranks 13–14 (Parallel):** Docs and prompts — can run alongside engineering without blocking releases.

**Ranks 15–16 (Weeks 9–14):** LLM pipeline only after Phase 1–2 stop conditions exist. Single-pass `humanize_llm()` is not the anti-detector product.

**Ranks 17–20 (Weeks 8–16):** Research depth, voice eval, policy hardening — important but not release-blocking for v0.7.x.

---

## Timeline

### Phase 0 — Research corpus + honesty (parallel, ~1 week)

| Week | Deliverable | Owner |
|------|-------------|-------|
| W0 | Fix Liang/Booth/Turnitin attribution in SSOT + sync mirrors | Docs |
| W0 | UPDATE-PLAN Phase 0: `docs/research/research-updating.md` August block | Research |
| W0 | Boundaries refresh: SYNTH-87 refusal scripts → SKILL.md | Docs |

**Gate:** No public landscape cite without `[detector] [version] [arm] [metric] [tier I–V]` format (SYNTH-82).

### Phase 1 — Quick wins (Weeks 1–3)

Derived from PLAN-97 / UPDATE-PLAN Part 4 Phase 1:

| Week | Engineering | Bench/docs |
|------|-------------|------------|
| W1 | #1 anti-detector ladder; #4 surprisal telemetry; #14 CoPA prompt | #3 SKILL refresh |
| W2 | #2 stylometric_baseline.json; #6 shield_metrics.py | #7 detector_bench upgrades |
| W3 | #10 StylometryContext spike (optional partial) | #8 May detector-test CSV |

**Acceptance (Phase 1 exit):**

- `pytest tests/unslop/` green  
- `feedback_loop()` reaches `anti-detector` as step 4+  
- `load_baselines()` returns non-empty genre bands  
- `--detector-feedback` JSON includes full surprisal vector when flag set  
- No Booth/Turnitin misattribution in SSOT

### Phase 2 — Surprisal dynamics + stylometry loop (Weeks 4–8)

Derived from PLAN-98 / UPDATE-PLAN Part 4 Phase 2:

| Week | Engineering | Bench |
|------|-------------|-------|
| W4–5 | #9 `compute_tsd_reading()`; #11 structural parameterization | Structural-only ablation on fixtures |
| W6 | #12 multi-objective stop; `dynamics_targets.py` sketch | DivEye/TSD before/after on 9 fixtures |
| W7–8 | #17 SurpMark lite (if bandwidth); #18 cone proxy spike | Dynamics section in detector_bench |

**Acceptance (Phase 2 exit):**

- Anti-detector raises 2nd-half DD on ≥7/9 long fixtures (when `--surprisal-variance` enabled)  
- `detector_bench.py` reports TPR@FPR=5% + URSS bundle  
- Stylometry pre/post in `HumanizeReport` for Phase 1–2 passes

### Phase 3 — LLM pipeline (Weeks 9–16, optional product surface)

Derived from PLAN-99 / UPDATE-PLAN Part 4 Phase 3:

| Week | Engineering | Gate |
|------|-------------|------|
| W9–10 | #15 `llm_pipeline.py` + S1 MASH 3-call | Mock LLM tests; preservation 100% |
| W11–12 | #16 S2 HIP rounds; S3 TempParaphraser selection loop | ≥5 pp TMR vs legacy on ≥3 fixtures |
| W13–14 | S4 span loop; S5 cross-model capstone | Semantic score ≥0.92 |
| W15–16 | Budget presets (fast/balanced/max); CLI `--llm-pipeline` | May detector-test commercial panel eval |

**Acceptance (Phase 3 exit):**

- Pipeline beats `humanize_llm()` by ≥5 pp TMR on ≥3 fixtures  
- `TestPreservation` 100%; no ASR marketing  
- SKILL.md documents stages, cost envelope, Boundaries

### Ongoing — Phase 4 benchmark & honesty

| Cadence | Action |
|---------|--------|
| Every PR | `run.py --strict` slop gate |
| Release | Opt-in `detector_bench.py` + dynamics JSON |
| Quarterly | Manual GPTZero/Pangram/Originality panel (version-pinned, not CI) |
| Per release | Research appendix with dual-arm reporting (clean vs cross-model stress) |

---

## Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| **R1** | Users interpret TMR ≤0.5 as "passes GPTZero/Turnitin" | High | Critical | Document TMR ≠ commercial; dual reporting; exhaustion message unchanged |
| **R2** | Anti-detector used for academic misconduct (Class III) | High | Critical | Four-question gate (SYNTH-87); decline scripts; no bypass SEO |
| **R3** | `stylometric_baseline.json` wrong genre bands → bad nudges | Medium | High | Ablation on fixtures before ship; conservative p25/p75 |
| **R4** | distilgpt2 default miscalibrates DivEye vs gpt2 | Medium | Medium | Label uncertified or switch default; CI parity gate |
| **R5** | Phase 3 LLM pipeline oversold as "92% ASR" | Medium | Critical | Acceptance = ≥5 pp TMR on fixtures; cite StealthRL as ceiling only |
| **R6** | Booth/Turnitin misattribution persists in mirrors | Medium | High | SSOT-only edit + sync workflow; grep CI for "Booth.*Turnitin" |
| **R7** | Watermark collateral scrub → Art. 50 exposure if marketed wrong | Low | Critical | Side-effect disclosure only; refuse strip modes (SYNTH-95) |
| **R8** | Voice-match + anti-detector merge without floors → ESL voice erased | Medium | High | Sequenced workflow; `max(sample_σ, 6)` floor (SYNTH-90) |
| **R9** | Commercial detector APIs in CI → flaky, ToS, non-reproducible | High | Medium | TMR + RAID in CI; commercial manual only |
| **R10** | Deterministic pass raises TPR (AdvPara lesson) | Medium | Medium | Structural before lexical LLM; document `subtle` ≠ anti-detector |
| **R11** | Research docs stale → misleading README claims | Medium | High | Phase 0 Wave A; version-date every accuracy mention |
| **R12** | Chunk truncation (4×512) hides essay-level dynamics | Medium | Medium | Raise cap or full-doc score for loop decisions |
| **R13** | RateAudit-style score targeting shipped by mistake | Low | Critical | Explicit non-goal; TMR diagnostic only |
| **R14** | Pangram vs GPTZero divergence uncommunicated | High | Medium | Dual-detector rule in SKILL; May bench includes both |
| **R15** | Phase 2 TSD/SurpMark orthogonal to TMR → false confidence | Medium | High | Multi-objective stop; never single-scalar gate for anti-detector claims |

---

## What NOT to build

Explicit non-goals consolidated from SYNTH-81, 84, 85, 87, 88, 94, 95 and UPDATE-PLAN Boundaries.

### Never ship (hard red lines)

| Category | Examples | Why |
|----------|----------|-----|
| **Watermark attack tooling** | SIRA, BIRA, RLCracker, RLSpoofer integrations; `--watermark-evade` | EU Art. 50 / CoP Measure 1.5; SYNTH-95 |
| **Score targeting** | RateAudit schedulers; `--target-score=0`; optimize until panel green | Gameable; Class III obfuscation; SYNTH-87 |
| **Bypass marketing** | "Beat Turnitin," "100% undetectable," Undetectable.ai positioning | FTC precedent; Turnitin bypasser category; SYNTH-87 |
| **Academic misconduct facilitation** | Ghostwrite mode; AI-as-original submission tooling | Intent gate; SYNTH-78 |
| **Commercial humanizer APIs** | Undetectable.ai / QuillBot wrapper in product | Bypass positioning; opaque quality; SYNTH-88 |
| **Trained adversary weights** | MASH SFT/DPO, HIP LoRA, StealthRL/AuthorMist GRPO in pip wheel | T3 threat model; quality tax; SYNTH-85 |
| **Watermark strip prompts** | SynthID-aware removal; KGW green-list targeting | Deliberate circumvention; SYNTH-95 |
| **HMGC / SHIELD attack generators in CI** | AWS/RHL as evasion tools | Academic misconduct surface; SYNTH-84 |

### Defer / reference only

| Item | Verdict | Notes |
|------|---------|-------|
| AdaDetectGPT / Ghostbuster in live loop | Bench-only opt-in | GPU/API; paraphrase fragile; SYNTH-81 |
| DivEye XGBoost HF head in production | P2 optional | NC license; measurement sufficient for v1 |
| BiScope + Falcon-7B ensemble | No | VRAM; not portable |
| `--adv-paraphrase` CUDA subprocess in default wheel | P3 opt-in | Research users only |
| TempParaphraser 1B weight bundle | No | Academic license; API selection loop instead |
| StyleShield embedding flow matching | No | 128×A800; γ-as-intensity tier concept only |
| Watermark detect + warn module | No | FP risk; scope creep; SYNTH-87 |
| C2PA re-marking / provenance restoration | No | Provider duty; document workflow instead |
| P2P/StyleTunedLM LoRA in plugin | Phase 3+ research | Consent + eval gate; SYNTH-90 |
| "OpenAI-grade detection" claims | Never | Classifier withdrawn Jul 2023; SYNTH-94 |

### Marketing / docs forbidden claims

| Forbidden | Allowed replacement |
|-----------|---------------------|
| "Passes GPTZero/Turnitin" from TMR score | "Moves TMR ≤0.2 pp deterministic; commercial panel separate" |
| "Chicago Booth twelve humanizers" | Booth = StealthGPT only; DAMAGE = 19 tools |
| "Turnitin 60–85% at Booth" | Booth did not test Turnitin; cite Blommerde |
| "ESL bias solved" | Al Ali 23.1% FPR persists; Liang mechanism documented |
| "HIP-powered / MASH-powered" product | "Prompt analog of published stages" |
| TMR 99.28% RAID AUROC as unslop score | Model card fact for TMR checkpoint only |

---

## Success metrics

### Tier 1 — Release gates (every version)

| Metric | Target | Harness |
|--------|--------|---------|
| AI-ism delta | ≥0 on all fixtures | `benchmarks/run.py --strict` |
| Preservation contract | 100% pass | `TestPreservation` |
| Deterministic TMR movement | Document ≤0.2 pp mean ΔP(AI) | `detector_bench.py` |
| pytest | Green | `tests/unslop/` |
| SSOT attribution | Zero Booth/Turnitin/Liang errors | Manual grep + review |

### Tier 2 — Phase 1 complete

| Metric | Target | Harness |
|--------|--------|---------|
| Feedback ladder includes anti-detector | Step 4+ in default ladder | `test_detector.py` |
| Baseline loads | Non-empty genre bands | `lexical_targets.load_baselines()` |
| Surprisal in feedback JSON | Full vector when flag set | CLI integration test |
| TPR@FPR reporting | Emitted alongside P(AI) | `shield_metrics.py` + bench |
| May detector-test | ≥12 detector rows populated | `drafts/2026-05-detector-test/results/scores.csv` |

### Tier 3 — Phase 2 complete

| Metric | Target | Harness |
|--------|--------|---------|
| TSD second-half DD lift | ≥7/9 fixtures after anti-detector | `surprisal_humanization/` ablation |
| Multi-objective stop | TMR + dynamics band | `detector.feedback_loop()` |
| Stylometry closed-loop | Δσ, ΔCV logged pre/post Phase 1–2 | `HumanizeReport.stylometry` |
| URSS bundle | ≥2 scenarios in release JSON | SHIELD fixture subset |
| RAID paraphrase slice | TPR@FPR=5% reported | `raid-bench` opt-in |

### Tier 4 — Phase 3 complete (if shipped)

| Metric | Target | Harness |
|--------|--------|---------|
| LLM pipeline TMR gain | ≥5 pp vs `humanize_llm()` on ≥3 fixtures | `detector_bench.py` variants |
| Semantic preservation | ≥0.92 embedding/judge | TH-Bench quality module |
| Cost envelope | balanced ≤$0.35/1K words | PipelineReport |
| Commercial panel (manual) | Dual-arm CSV; no single-detector pass claim | May detector-test |
| Voice fidelity (informal) | Measure AV movement; no "pass" claim | Catch Me harness optional |

### Tier 5 — Product / policy (ongoing)

| Metric | Target | Evidence |
|--------|--------|----------|
| Boundaries compliance | Zero strip-mode PRs; refusal scripts in SKILL | SYNTH-87 checklist |
| README 60-second install | Non-programmer completes install | Maintainer review |
| ESL defense framing | Liang + OCR + institutional retreat cited | SYNTH-96 segments |
| Dual-detector honesty | Every commercial cite names arm + version | SYNTH-82 template |
| User segment clarity | Developer / ESL / resume / student blocks in README | SYNTH-96 |

### Anti-metrics (do not optimize)

| Anti-metric | Why |
|-------------|-----|
| Minimize TMR to 0.0 as primary goal | Score targeting; RateAudit game |
| Maximize RAID AUROC | unslop is not training detectors |
| "Beat Turnitin" conversion rate | Misconduct positioning |
| Single-detector screenshot pass rate | Pangram ≠ GPTZero under paraphrase |
| Watermark removal success rate | Art. 50 circumvention |

---

## Cross-synthesis decision log

Decisions implied by integrating all SYNTH memos:

| Decision | Rationale | Dissent / open question |
|----------|-----------|-------------------------|
| **Keep TMR as default feedback scorer** | RAID-trained supervised classifiers beat zero-shot on Tier 2; SYNTH-81 | Optional Binoculars/DetectAIve for bench disagreement |
| **Deterministic-first, LLM-second** | ~0.2 pp TMR expected; slop removal is primary win; SYNTH-83 | Phase 3 only for anti-detector distribution layer |
| **Separate voice-match and anti-detector** | Jemama two-axis; ESL conflict; SYNTH-90, #52 | Future `--voice-floor-σ` for merged path |
| **Cross-model as user-orchestrated capstone** | Strongest practitioner lever; SYNTH-88; cannot automate all providers in-plugin | Phase 3 S5 partial automation |
| **Institutional retreat validates ESL defense, not bypass** | 60+ universities disabled classifiers; SYNTH-94, #69 | Admissions may still use Pangram outside LMS |
| **Document watermark side effect; refuse strip** | WaterPark + Art. 50; SYNTH-95 | Enforcement of incidental loss unsettled |
| **Lead with slop removal; detector in appendix** | TH-Bench three-axis; SYNTH-84 | Anti-detector users want detector telemetry — ship as opt-in |
| **No commercial detector APIs in CI** | ToS, drift, cost; SYNTH-84 | Manual quarterly panel for article data |

---

## Dependency graph (critical path)

```
P0 docs fix (Liang, Booth) ──────────────────────────────┐
                                                            │
P1 #1 anti-detector ladder ──► P1 #4 surprisal telemetry ──┼──► P2 #12 multi-objective stop
P1 #2 baseline.json ──► P2 #10 StylometryContext ──────────┤
P1 #6 shield_metrics ──► P1 #7 detector_bench ─────────────┤
                                                            │
P2 #9 TSD ──► P2 #17 SurpMark ──► P2 #18 cone proxy ──────┘
                                                            │
P3 #15 llm_pipeline ──► P3 #16 HIP/S3 ──► commercial bench (manual)
```

**Critical path:** #1 → #4 → #9 → #12 → (optional) #15. Docs (#3, #5, #13) parallel throughout.

---

## Appendix A — PLAN-97/98/99 summaries (derived)

### PLAN-97 — Phase 1 Quick Wins (Agent #97 scope)

| # | Change | Files |
|---|--------|-------|
| 1 | anti-detector on feedback ladder | `detector.py`, `cli.py` |
| 2 | stylometric_baseline.json | `benchmarks/fixtures/`, `benchmarks/results/` |
| 3 | surprisal in CLI feedback | `cli.py`, `detector.py` |
| 4 | SKILL.md August landscape | `skills/unslop/SKILL.md` + sync |
| 5 | CoPA anti-detector prompt | `humanize.py` |
| 6 | Fix TempParaphraser comment | `detector.py` |

### PLAN-98 — Phase 2 Surprisal Dynamics (Agent #98 scope)

| Capability | Module |
|------------|--------|
| TSD `compute_tsd_reading()` | `surprisal.py` |
| SurpMark `compute_surpmark_reading()` | `surprisal.py` |
| Cone proxy | new or `surprisal.py` |
| `dynamics_targets.py` | new |
| Multi-objective stop | `detector.py` |
| `--dynamics-feedback` CLI | `cli.py` |

### PLAN-99 — Phase 3 LLM Pipeline (Agent #99 scope)

| Stage | Analog | Calls |
|-------|--------|-------|
| S1 | MASH align+critique+fix | 3–4 |
| S2 | HIP cross-model | 1–4 rounds |
| S3 | TempParaphraser N-pick | 2 batched |
| S4 | AdvPara span loop | 3 |
| S5 | Cross-model capstone | 1 |

Budget: fast ~$0.10, balanced ~$0.30, max ~$0.70 per 1K words.

---

## Appendix B — Source index

| Doc | Contribution to PLAN-100 |
|-----|---------------------------|
| UPDATE-PLAN-2026-08 | Phase timeline, five-signal stack, gap analysis |
| SYNTH-81 | Academic detection; TMR default; benchmark hierarchy |
| SYNTH-82 | Commercial landscape; dual reporting; attribution fixes |
| SYNTH-83 | Code gap; detector.py semantics; P0–P3 engineering |
| SYNTH-84 | TPR@FPR, URSS, honest reporting rules |
| SYNTH-85 | Prompt/rule evasion; pipeline architecture |
| SYNTH-86 | LLM pipeline spec; detector-in-loop policy |
| SYNTH-87 | Refusal categories; four-question gate |
| SYNTH-88 | Practitioner tools; document vs integrate |
| SYNTH-89 | Stylometry signal stack; three-axis eval |
| SYNTH-90 | Voice-match strategy; two-axis doctrine |
| SYNTH-91 | Preserve vs inject human cues |
| SYNTH-92 | Stylometry Phase 1–2 integration |
| SYNTH-93 | Commercial market map |
| SYNTH-94 | Regulatory / institutional context |
| SYNTH-95 | Watermark & provenance policy |
| SYNTH-96 | User segments; mode fit |

---

## Bottom line

unslop wins by **subtracting slop honestly**, **wiring what already exists**, **measuring on fixed-FPR benchmarks**, and **refusing the bypass category**. The top 20 list is ordered so Week 1 fixes lies and wiring, Weeks 2–8 close the 2026 surprisal-dynamics gap, and Weeks 9–16 optionally ship a bounded LLM pipeline — never marketed as MASH/StealthRL ASR.

Ship Phase 1 before debating Phase 3. Run the May detector-test bench before claiming commercial context. Fix Liang and Booth before refreshing README. Treat TMR as a maintainer release gate, not a user pass certificate.

---

*PLAN-100 complete. Master Integration Agent #100. Feeds maintainer roadmap, release planning, and research doc Wave A/B scheduling.*
