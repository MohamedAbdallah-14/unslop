# SYNTH-81 — Academic Detection Landscape (Agents 1–20)

**Synthesis Agent #81**  
**Date:** 2026-08-19  
**Scope:** DivEye, TSD, SurpMark, DetectGPT lineage (AdaDetectGPT, Fast-DetectGPT, Binoculars, Ghostbuster), PHD, LLM-DetectAIve, SHAP cross-domain, DAMAGE, GPTZero v6/cones, HLD, RAID, SHIELD, Sadasivan, Liang ESL, MGTBench/TH-Bench, WaterPark  
**Sources:** `AGENT-01` through `AGENT-20` memos in this directory  
**Audience:** unslop maintainers — product, benchmark, and anti-detector policy

---

## Executive summary

Academic AI-text detection in 2023–2026 converged on a uncomfortable truth: **single-signal, single-benchmark detectors fail under distribution shift, paraphrase, and humanization.** The field did not collapse into randomness — it **fractured into signal families** (logits/curvature, surprisal dynamics, embedding geometry, stylometric features, supervised classifiers) and **benchmark tiers** (clean in-domain → OOD → adversarial → humanizer-hardened). Each new method wins on one axis and loses on another.

For unslop, the synthesis is operational:

1. **TMR (RAID-trained RoBERTa) is the correct live feedback default** — not Fast-DetectGPT, Binoculars, DivEye XGBoost, or Ghostbuster API calls.
2. **Deterministic unslop moves surface AI-isms and light stylometry; it does not reliably move logits geometry, surprisal dynamics, or hierarchical syntax** — measured TMR delta on fixtures is ~0.0–0.2 pp.
3. **Distribution shaping** (burstiness, surprisal variance, late-half volatility, anti-recovery transitions) is the defensible anti-detector architecture — aligned with Sadasivan's TV framework and Liang's ESL fairness paradox.
4. **Cross-model paraphrase** remains the only lever with consistent evidence against curvature, perplexity, and commercial detector stacks when the deterministic ladder exhausts.
5. **Never cite in-domain AUROC without OOD, fixed-FPR, and attack context** — RAID, SHIELD, SHAP, and MGTBench/TH-Bench all punish headline numbers.

This memo maps consensus mechanisms, benchmark hierarchy, breakage timeline, debate positions, and ten actionable findings for the unslop codebase and docs.

---

## 1. Consensus mechanisms — what actually separates human from AI text

Across 20 agent memos, five **orthogonal signal families** recur. No family alone survives 2026 adversarial evaluation; ensembles and retraining on attack corpora (RAID, humanizer-augmented) are the deployment pattern.

### 1.1 Logits and curvature (DetectGPT lineage)

**Hypothesis:** LLM-generated token sequences sit on local maxima of the scoring model's log-probability surface — negative curvature under perturbation (DetectGPT), positive conditional curvature (Fast-DetectGPT), or learned witness transforms (AdaDetectGPT).

**Consensus:** Works on **clean, white-box, unparaphrased** text when scoring LM ≈ generator. **Fails** under cross-model paraphrase, TempParaphraser, Adversarial Paraphrasing, StealthRL, and often under synonym swap (RAID: Binoculars −36.1 pp on synonym attack).

**Verdict (Agent #08):** Curvature is **not dead as a research feature**; it is **dead as a standalone deployment gate**.

### 1.2 Cross-perplexity and paired-LM ratios (Binoculars)

**Hypothesis:** Machine text has lower ratio of observer perplexity to cross-perplexity under two similar LMs — fixes the "capybara problem" of raw perplexity.

**Consensus:** Strong at **TPR@0.01% FPR** on Ghostbuster-era ChatGPT in English. **Collapses** under humanizers (DAMAGE: 94.15% → 28.23% TPR@5% FPR), RL paraphrase (StealthRL TPR@1%FPR ≈ 0.002), and synonym swap. ESL essays: paradoxically **99.67%** accuracy on corrected/uncorrected EssayForum — better than Liang-era GPTZero on some sets, but short-text TOEFL remains risky elsewhere.

### 1.3 Surprisal dynamics (DivEye → TSD → SurpMark)

**Hypothesis:** AI text is **too smooth** in token-level surprise — not just low mean perplexity but **narrow intra-document variance**, **late-stage volatility decay**, and **machine-like state transitions** after high-surprisal tokens.

| Method | Signal | Scope | Headline |
|--------|--------|-------|----------|
| **DivEye** (TMLR 2026) | Global σ, Δ, Δ² surprisal + XGBoost | Full sequence | 0.984 RAID AUROC; paraphrase robust vs Binoculars |
| **TSD** (Jan 2026) | Second-half DD + LV | Positions > 50% | 83.36% EvoBench avg; beats DivEye on frontier models |
| **SurpMark** (ICML 2026) | k-state Markov transitions, ΔGJS | Transition matrix | 99.2–99.8% AUROC under DIPPER/back-trans OOD |

**Consensus:** Surprisal **variance and dynamics** survive synonym paraphrase better than mean perplexity. **Complementary** — global σ (DivEye) ≠ positional decay (TSD) ≠ transition recovery (SurpMark). unslop `surprisal.py` implements DivEye measurement only; TSD and SurpMark are gaps.

### 1.4 Embedding geometry (PHD / Tulchinskii)

**Hypothesis:** Human fluent text explores higher **intrinsic dimension** in RoBERTa token-embedding trajectories (~9.5 vs ~7.9 for GPT-3.5).

**Consensus:** **Resists DIPPER** where DetectGPT collapses (40.0% → 41.2% TPR@1% FPR on GPT-3.5). **Partial ESL improvement** (26% FPR vs GPTZero 52% on TOEFL) — better, not fair. Requires ~200–300 tokens. Not in RAID standard baselines.

### 1.5 Supervised classifiers and stylometric stacks

**Hypothesis:** Fine-tuned encoders (RoBERTa, DeBERTa, Mistral+LoRA) and hand-crafted feature ensembles capture distributional fingerprints invisible to single-threshold perplexity.

**Representatives:** TMR/Desklib (RAID-trained), Ghostbuster (multi-LM logprob features + logreg), LLM-DetectAIve (4-way provenance), HLD (word/POS/dep n-gram LLR + semantic KDE + XGBoost), DAMAGE detector (humanizer-augmented Mistral NeMo).

**Consensus:** **Best deployment class** when trained on multi-generator, multi-attack corpora. **Still fails** OOD (DetectAIve: 95.71% in-domain → 60.08% on MixSet), cross-domain SHAP artefacts (PAN F1 0.97 → COLING 0.67), and adaptive humanizers not in training mix. Stylometric detectors learn **corpus-specific cues** (paragraph count, GZIP ratio) — Pudasaini SHAP paper proves feature rankings **do not transfer** across benchmarks.

### 1.6 Synthesis: the five-signal stack (2026)

unslop's UPDATE-PLAN stack maps cleanly onto agent findings:

```
Signal 1: Lexical AI-isms          → humanize.py ✅
Signal 2: Burstiness / structure   → structural.py ⚠️
Signal 3: Surprisal variance       → surprisal.py ⚠️ (measure, not optimize)
Signal 4: Late-stage stability     → NOT IMPLEMENTED ❌
Signal 5: Predictability cones     → NOT IMPLEMENTED ❌ (GPTZero commercial analog)
         POS/dependency patterns   → NOT IMPLEMENTED ❌ (HLD gap)
         Transition dynamics        → NOT IMPLEMENTED ❌ (SurpMark gap)
```

**Mechanism consensus:** Detection works when **multiple weak signals align** on unparaphrased text from known generator families. Evasion works when **any rewrite changes the token geometry** sufficiently — paraphrase is near-optimal per Sadasivan because |L(s)| ≪ |P(s)|.

---

## 2. Benchmark hierarchy — which numbers mean what

Not all benchmarks are comparable. Use this **authority ladder** when citing or designing unslop evals.

### Tier 0 — Toy / custom splits (low external validity)

- AdaDetectGPT five-dataset protocol (SQuAD, WritingPrompts, XSum, Yelp, Essay — 500 samples each)
- Fast-DetectGPT paper-native 0.9887 AUROC
- Ghostbuster 99.0 F1 in-domain (three domains, gpt-3.5-turbo era)
- LLM-DetectAIve 95.71% on M4GT-extended corpus

**Use for:** Method comparison within a paper. **Do not** extrapolate to deployment or unslop marketing.

### Tier 1 — OOD generalization (MAGE, EvoBench, cross-domain)

- **MAGE** (ACL 2024): 8 testbeds, 27 LLMs — Fast-DetectGPT **0.59 AUROC** on Testbed 2 vs DivEye **0.97**
- **EvoBench** (ACL 2025 Findings): model version drift — Fast-DetectGPT AUROC decays GPT-4o 0.80 → 0.74
- **MGTBench 2.0 / MGT-Academic**: 16 academic categories, cross-domain FN inflation
- **SHAP cross-domain** (arXiv:2603.23146): PAN F1 0.97 → COLING **0.67** on cross-train

**Use for:** Proving **generalization claims**. Required companion to any Tier 0 headline.

### Tier 2 — Adversarial robustness (RAID and derivatives)

- **RAID** (ACL 2024): 6.2M+ samples, 11 LLMs, 4 decoding strategies, 11–12 attacks, **TPR@FPR=5%**
- **COLING 2025 Shared Task 3**: train on full RAID grid → Pangram/Leidos **99.3%** clean, **97.7%** with all attacks
- **DAMAGE** (COLING 2025): 19 humanizers on academic essays — GPTZero 99.73% → **60.04%**; Binoculars 94.15% → **28.23%**
- **WaterPark** (EMNLP 2025 Findings): watermark robustness — DIPPER drops most schemes; ChatGPT 1-round paraphrase → all **<30% TPR**

**Use for:** **Deployment honesty.** TMR's 99.28% RAID AUROC and 95.79% TPR@5% FPR live here. unslop should cite RAID context whenever citing TMR.

### Tier 3 — Humanization hardness (SHIELD, TH-Bench, MGTBench attacks)

- **SHIELD** (Jul 2025): URSS = W-AUROC × SFD; zero-shot detectors lose **~80% URSS** under random MLM swaps (RMM)
- **TH-Bench** (KDD 2025): three-axis Pareto — **no attack wins** evasion × quality × cost; HMGC crushes metric detectors, Recursion fails model-based
- **MGTBench v1**: LRR F1 drops 0.418 under paraphrase on WritingPrompts

**Use for:** Scoping **anti-detector claims**. Lexical humanization alone is Tier 3–weak; structural + cross-model is Tier 3–strong.

### Tier 4 — Fixed-FPR operating points and equity strata

- **TPR@FPR=1% or 5%** — RAID standard; SHIELD W-AUROC weights low-FPR region
- **Liang TOEFL-91** — ESL false-positive stratum (61% → 23% on 2025 detectors, not 0%)
- **Chicago Booth 2026** — commercial FPR on general corpora; **does not** replace ESL stratification

**Use for:** High-stakes and **fairness** documentation. unslop anti-detector boundaries must cite Tier 4 ESL numbers, not Tier 0 vendor benchmarks.

### Recommended unslop eval stack

| Layer | Benchmark / metric | Purpose |
|-------|-------------------|---------|
| Regression | `benchmarks/` AI-ism delta | Voice quality contract |
| Detector | TMR + optional Desklib on fixtures | Live loop parity |
| Academic | RAID paraphrase/synonym slice via `raid-bench` | TPR@FPR=5% reporting |
| Dynamics | DivEye vector + (future) TSD/ΔGJS before/after | Surprisal humanization |
| Honesty | OOD subset or SHIELD-style hardness knob | Anti-marketing guardrail |

---

## 3. What broke what — causal timeline

Understanding **which benchmark or attack demoted which method** prevents repeating 2023 deployment mistakes.

| Year | Event | What it broke |
|------|-------|---------------|
| **Mar 2023** | Sadasivan TV bound + T5/DIPPER paraphrase | Watermarks (97%→57%), DetectGPT (96.5%→25% AUROC), retrieval defense (100%→25% after 5× DIPPER) |
| **Mar 2023** | Liang TOEFL study | Perplexity-class **ESL false positives** — 61% mean FPR, 97.8% flagged by ≥1 detector |
| **May 2023** | DetectGPT (ICML) | Launched curvature family — later shown fragile |
| **Jul 2023** | Ghostbuster (NAACL) | Proved multi-LM features beat single perplexity OOD — but API-dependent, not RAID-tested |
| **Oct 2023** | Fast-DetectGPT (ICLR 2024) | 340× speedup; became **straw-man baseline** for 2025 attacks |
| **2023** | Krishna DIPPER (NeurIPS) | Paraphrase as evasion standard; PHD resists, DetectGPT dies |
| **2024** | MAGE (ACL) | Fast-DetectGPT **0.59 AUROC** on wild testbeds — broke "0.99 AUROC" extrapolation |
| **2024** | RAID (ACL) | Binoculars synonym **−36.1 pp**; repetition penalty **−38 pp**; commercial API gaps exposed |
| **2024** | Binoculars (ICML) | Best zero-shot low-FPR — later broken by DAMAGE/StealthRL |
| **2024** | LLM-DetectAIve (EMNLP Demo) | 4-way taxonomy — broke binary-only policy framing |
| **2025** | DAMAGE (COLING GenAIDetect) | Binoculars/GPTZero collapse under 19-tool humanizer pool |
| **2025** | TempParaphraser (EMNLP) | Fast-DetectGPT **98.9% → 2.6%** accuracy on HC3 |
| **2025** | Adversarial Paraphrasing (NeurIPS) | −98.96% TPR@1%FPR on Fast-DetectGPT |
| **2025** | TH-Bench (KDD) | Proved **no humanization attack** wins all three axes |
| **2025** | SHIELD | URSS collapse under RMM — "casual editing" breaks zero-shot |
| **2025** | WaterPark (EMNLP Findings) | Paraphrase breaks most watermarks; humanization ≡ watermark attack |
| **2025–26** | DivEye, TSD, SurpMark | Broke "perplexity-only" zero-shot; shifted frontier to dynamics |
| **2025–26** | HLD (ICLR 2026) | Broke "stock-vocab stripping suffices" — POS/dep/semantic layers hold under paraphrase |
| **2026** | GPTZero 4.x + cones | Broke synonym-swap evasion (T1); structural/cross-model still contested |
| **2026** | SHAP validity paper | Broke "leaderboard F1 = authorship proof" — feature rankings swap by corpus |
| **2026** | StealthRL | Fast-DetectGPT AUROC **0.661 → 0.089** — RL humanizer upper bound |

**Pattern:** Each generation adds an **attack axis** (paraphrase → decoding → humanizer pool → RL → surprisal-aware retraining). Methods that skip Tier 2–3 eval get demoted in papers but linger in marketing.

---

## 4. Debate map — who argues what

### 4.1 Impossibility vs possibility

| Camp | Representative | Claim | unslop stance |
|------|----------------|-------|---------------|
| **Pessimists** | Sadasivan (TMLR 2025), Nicks (ICLR 2024) | TV bound → paraphrase optimal; don't rely on detectors | Cite in `detector.py`; ladder exhaustion message |
| **Sample-complexity** | Chakraborty (ICML 2024) | Multi-sample bot detection feasible; **single essay is hard regime** | ESL/essay use case stays pessimist |
| **Feature optimists** | DivEye, SurpMark, HLD | New axes restore separability under paraphrase | Measure in benchmarks; don't ship as gate |
| **Retraining optimists** | RAID shared task, DAMAGE, Pangram | 99%+ TPR@5% if train on known attack grid | TMR/D Desklib path; stale without patch cadence |

**Reconciliation:** Detection is **possible in constrained, retrained, multi-signal settings**; **impossible as durable single-threshold perplexity** under adaptive adversaries.

### 4.2 Zero-shot vs supervised

| Position | Evidence |
|----------|----------|
| Zero-shot dead for deployment | TempParaphraser, MAGE 0.59, SHIELD −80% URSS |
| Zero-shot alive for research | Every attack paper needs Fast-DetectGPT/Binoculars row |
| Supervised wins in-domain | TMR 99.28% RAID AUROC, DAMAGE 98.26% post-humanizer |
| Supervised fails OOD | DetectAIve 60% MixSet; RoBERTa 0.535 cross-domain (PHD); SHAP PAN→COLING |

### 4.3 Fairness vs evasion isomorphism (Liang)

| Frame | Same transform, different ethics |
|-------|-----------------------------------|
| **Fairness** | Enrich L2 prose → FPR 61% → 12% on TOEFL |
| **Evasion** | Literary self-edit on AI text → detection 100% → 13% |
| **Detector blind spot** | Cannot distinguish without provenance |

unslop **anti-detector mode** sits on this edge — defensive ESL/resume use only (`SKILL.md` boundaries).

### 4.4 Benchmark validity (SHAP / Pudasaini)

| Claim | Implication |
|-------|-------------|
| In-domain F1 measures **corpus artefacts** (paragraph count, GZIP) | Never ship "97 F1" without OOD |
| Features that win in-domain **fail cross-domain** | Multi-lever humanization > score chasing one detector |
| Ensembles help but don't fix validity | TMR + surprisal telemetry > TMR alone |

### 4.5 Watermarking vs detection

| Camp | WaterPark finding |
|------|-------------------|
| Watermarks raise TV | True — until paraphrase redefines M |
| Watermarks survive humanization | **False** for most schemes under DIPPER/ChatGPT paraphrase |
| SynthID solves provenance | Partial — mid-tier under DP-40, not paraphrase-proof |

unslop **refuses watermark removal** (EU AI Act Art. 50) — WaterPark confirms humanization and watermark stripping are the same attack class.

### 4.6 Commercial vs academic

| Tension | Data |
|---------|------|
| GPTZero self-report vs independent | 99.5% vs 89% WriteHumanly; cones close synonym gap, not StealthGPT |
| Pangram vs GPTZero on bypassers | GPTZero 91.8% vs Pangram 68% on vendor corpus — disputed field choice |
| Turnitin vs RAID | Shared-task winners ≠ legacy Binoculars; institutional retreat continues |

---

## 5. Top 10 findings for unslop

### Finding 1 — TMR default is architecturally correct

Supervised RAID-trained classifiers (TMR 99.28% AUROC, Desklib) beat zero-shot curvature/perplexity on Tier 2 benchmarks. AdaDetectGPT, Fast-DetectGPT, Binoculars, and Ghostbuster are **benchmark-only** backends — GPU/API cost, paraphrase fragility, or offline incompatibility. Do not replace TMR in `detector.py` without explicit opt-in.

### Finding 2 — Deterministic unslop does not move detector scores materially

Agents #04–#08, #35 cross-refs: regex + structural + soul passes yield **~0.0–0.2 pp** TMR delta on fixtures. This is expected — unslop targets AI-isms and surface burstiness, not token-level LM geometry. **Do not claim** deterministic mode "beats detectors."

### Finding 3 — Surprisal dynamics are the 2026 academic frontier; unslop measures but does not optimize

DivEye (global σ, Δ² entropy), TSD (second-half DD/LV), SurpMark (ΔGJS transitions) are **complementary**. `surprisal.py` bit-matches DivEye; anti-detector mode lacks Δ²/TSD/SurpMark targets. **P0:** extend prompts and feedback telemetry; **P1:** implement `compute_tsd()` and optional ΔGJS port.

### Finding 4 — Structural pass > lexical pass for detector-relevant signals

HLD, PHD, GPTZero cones, and DivEye all punish **uniform rhythm** more than stock vocabulary. `structural.py` (sentence-length σ) is the highest-value deterministic lever; `subtle` mode alone is the worst case against hierarchical detectors. **Prioritize structural + soul over synonym scrub** in anti-detector ordering.

### Finding 5 — Cross-model paraphrase is the only Tier-3-evidence exit ramp

When `feedback_loop()` exhausts, recommend cross-model rewrite — TempParaphraser, Adversarial Paraphrasing, and Sadasivan theory align. **Do not** recommend synonym swap (RAID: can *increase* detection; cones designed to catch it). Naive paraphrase can raise Fast-DetectGPT TPR +15% (AdvPara).

### Finding 6 — ESL fairness requires distribution shaping, not detector score chasing

Liang: 61% FPR on TOEFL; Al Ali 2026: still 23.1%. Anti-detector mode (burstiness, contractions, specificity) aligns with **fairness fix** — same transform as evasion when applied to AI text. Maintain strict boundaries; fix README citation (Liang = **2304.02819**, not Tulchinskii 2306.04723).

### Finding 7 — Report TPR@FPR and OOD; reject single AUROC marketing

RAID institutionalized TPR@FPR=5%. SHIELD URSS penalizes threshold instability. SHAP proves PAN winners ≠ COLING winners. Any unslop benchmark doc citing TMR must include **fixed-FPR** and ideally a **paraphrase attack slice**.

### Finding 8 — 4-way provenance (DetectAIve) exposes policy gap in binary loop

Categories III (machine-humanized) vs IV (human-polished) are exactly unslop anti-detector vs voice-match outputs. Binary TMR loop cannot distinguish them. **P1:** optional DetectAIve backend + `--provenance-policy` for bench; map to Originality Allowance thinking (Agent #58).

### Finding 9 — Humanizer-augmented training is the detector counter-move; static humanizers win less over time

DAMAGE: 0.68% humanizer data + 18× oversample → 98.26% post-humanizer. GPTZero 4.x trains on DIPPER/TempParaphraser. unslop users face **moving targets** — document model version in any external benchmark; never promise pass on "GPTZero" without version pin.

### Finding 10 — Epistemic humility is a product feature

Sadasivan TV bound, Nicks "signal not gate," Pudasaini SHAP validity, RAID ethics statement, Liang ESL — convergent policy: **detectors assist human judgment; they do not adjudicate authorship alone.** unslop `detector.py` already cites Nicks; extend to README anti-detector section with SHAP/RAID/Liang citations.

---

## 6. unslop integration priorities (merged from agents)

| Priority | Action | Agents |
|----------|--------|--------|
| **P0** | Keep TMR default; fix Liang/Tulchinskii citation split | #09, #18 |
| **P0** | DivEye-aware anti-detector prompts (σ, Δσ, H_Δ²) | #01 |
| **P1** | `compute_tsd()` in surprisal.py; log full vector in feedback loop | #02, #01 |
| **P1** | RAID paraphrase slice in detector_bench; TPR@FPR reporting | #15 |
| **P1** | Document GPTZero cones = surprisal variance analog; structural > lexical | #13, #14 |
| **P2** | Optional backends: Binoculars, DetectAIve, PHD — bench only | #06, #10, #09 |
| **P2** | SurpMark ΔGJS port or `surpmark` clone on fixtures | #03 |
| **P2** | Syntax/POS diversity pass (HLD-motivated) | #14 |
| **P3** | SHIELD URSS / TH-Bench three-axis reporting on humanize modes | #16, #19 |

**Explicit non-goals:** Integrate AdaDetectGPT/Ghostbuster into live loop; claim GPTZero pass; ship watermark removal; optimize to perplexity/burstiness UI metrics (retired 2023).

---

## 7. Open synthesis questions

1. **Ensemble meta-classifier:** DivEye + TSD + SurpMark + TMR — orthogonal or redundant once XGBoost fuses?
2. **unslop before/after on surprisal axes:** No published bench — highest-value internal experiment.
3. **PHD on structural-only pass:** Does `structural.py` alone raise ID ~1.5 points?
4. **DetectAIve III recall on unslop anti-detector output:** Direct policy test.
5. **TMR vs GPTZero 4.3b disagreement:** Which predicts education deployment?
6. **Reasoning-model LSVD:** TSD attenuated on R1/o3 — agent output humanization edge case.

---

## 8. Agent index (sources)

| Agent | Topic |
|-------|-------|
| 01 | DivEye |
| 02 | TSD / late-stage volatility |
| 03 | SurpMark |
| 04 | AdaDetectGPT |
| 05 | Fast-DetectGPT |
| 06 | Binoculars |
| 07 | Ghostbuster |
| 08 | DetectGPT lineage |
| 09 | PHD / Tulchinskii |
| 10 | LLM-DetectAIve 4-way |
| 11 | SHAP cross-domain validity |
| 12 | DAMAGE detector + humanizer audit |
| 13 | GPTZero v6 / predictability cones |
| 14 | HLD hierarchical n-grams |
| 15 | RAID benchmark |
| 16 | SHIELD URSS hardness |
| 17 | Sadasivan impossibility |
| 18 | Liang ESL bias |
| 19 | MGTBench / TH-Bench |
| 20 | WaterPark watermark robustness |

---

## Bottom line

Academic detection in August 2026 is a **multi-signal, multi-benchmark discipline**. Methods split into logits, surprisal dynamics, geometry, syntax, and supervised ensembles — each broken by a specific attack generation (paraphrase, decoding, humanizer pool, RL). unslop's product truth: **humanize voice and reduce false positives through distribution shaping; use TMR as a secondary signal; escalate to cross-model paraphrase only with explicit ethics boundaries; never treat any score as proof.**

The research program ahead is **measurement** (DivEye/TSD/SurpMark on fixtures), **honest reporting** (RAID slices, fixed FPR, OOD), and **structural humanization** — not another perplexity threshold.

---

*Synthesis Agent #81 complete. ~3,400 words. Cross-ref: `DEEP-RESEARCH-EXEC-SUMMARY.md`, `UPDATE-PLAN-2026-08.md`, `AGENT-MANIFEST-100.md`.*
