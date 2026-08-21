# SYNTH-84 — Detection Benchmark Strategy for unslop

**Synthesis Agent #84**  
**Date:** 2026-08-19  
**Inputs:** Agent memos #12 (DAMAGE), #15 (RAID), #16 (SHIELD), #19 (MGTBench/TH-Bench), #20 (WaterPark), #36 (HumanLLM), #62 (Chicago Booth)  
**Scope:** Which benchmarks to adopt, metrics (TPR@FPR, URSS), eval harness design, honest reporting rules  
**Audience:** unslop maintainers, benchmark CI, README/SKILL.md authors

---

## Executive summary

unslop is a **humanizer**, not a detector. Its benchmark stack must therefore measure **three orthogonal axes**:

| Axis | Question | Primary harness |
|------|----------|-----------------|
| **Slop removal** | Did visible AI-isms leave? | `benchmarks/run.py` (existing) |
| **Detector signal** | Did classifier scores move? | `benchmarks/detector_bench.py` + RAID/SHIELD extensions |
| **Human quality** | Does text still read well / simulate cognition? | TH-Bench quality metrics + optional HumanLLM verbal slice |

No single benchmark answers all three. RAID is the **citation anchor** for detector robustness. SHIELD adds **deployment-fair metrics** (URSS). TH-Bench adds **evasion × quality × cost** framing. DAMAGE and Booth supply **commercial humanizer collapse numbers** for honest marketing. WaterPark is **reference-only** (provenance ethics). HumanLLM is a **fourth axis** for role-play dialogue, not detection.

**Core honest finding (already measured):** deterministic rule-stripping moves TMR probability ~0.1–0.2 pp on fixtures. RAID, TH-Bench, and DAMAGE all predict this. unslop should **lead with slop removal**, report detector numbers in research appendices with fixed-FPR metrics, and **never** conflate TMR's 99.28% RAID AUROC with consumer-detector bypass.

---

## 1. Benchmark adoption matrix

### 1.1 Adopt (integrate into CI or release gates)

| Benchmark | What to adopt | Priority | Rationale |
|-----------|---------------|----------|-----------|
| **RAID** (paraphrase + synonym slices) | Attack arms via `pip install raid-bench`; TPR@FPR=5% reporting | **P0** | Field standard; TMR is RAID-trained; unslop already cites RAID in `detector_bench.py` |
| **SHIELD** (metrics only) | `shield_metrics.py`: W-AUROC, SFD, URSS calculator | **P0** | Fixes AUROC-only misleading; no 700k corpus required initially |
| **TH-Bench** (reporting frame) | Three-axis table: evasion × quality × cost | **P1** | Canonical humanizer eval framing; adopt schema, not full 6×13×6 GPU-week run |
| **DAMAGE** (protocol + citation) | TPR@FPR=5% before/after; L1/L2/L3 tier labels; academic essay fixtures | **P1** | Peer-reviewed commercial humanizer audit; justifies detector loop |
| **Internal fixtures** | `benchmarks/fixtures/*.md` + PERSUADE-style essay samples | **P0** | Already shipped; extend with ESL/short/résumé slices |

### 1.2 Reference (cite in docs; do not ship as product feature)

| Benchmark | Role | Why reference-only |
|-----------|------|-------------------|
| **Chicago Booth** (Jabarian & Imas) | Independent commercial detector audit; policy-cap FPR framing | No unslop samples; one humanizer (StealthGPT); API field disputes; not a pass/fail cert |
| **MGTBench 2.0** | Cross-domain academic splits (16 categories) | Useful if unslop benchmarks institutional prose; full corpus is 336M tokens |
| **WaterPark** | Provenance side-effect citation (Art. 50) | unslop is not a watermark benchmark; rewrite may strip marks as side effect |
| **HumanLLM** | Normative-confounding citation; optional verbal eval | Measures cognitive anthropomorphism, not AI detection |

### 1.3 Refuse (do not adopt or optimize for)

| Benchmark / practice | Reason |
|---------------------|--------|
| **HMGC surrogate evasion** (TH-Bench) | Academic misconduct tooling; detector-guided synonym search |
| **SHIELD AWS/RHL as evasion tools** | MI-targeted word swap is circumvention; use for defensive eval only |
| **WaterPark attack pipeline in CI** | Watermark removal is out of scope and Art. 50 boundary |
| **Commercial detector APIs in CI** | GPTZero/Pangram/Turnitin: ToS, cost, version drift, non-reproducible |
| **"Beat RAID" or "pass Booth" marketing** | unslop is not evaluated in either study |
| **Flat AUROC / raw P(AI) as sole metric** | RAID + SHIELD + Booth all retired this for deployment claims |

---

## 2. Metrics — TPR@FPR and URSS

### 2.1 TPR @ fixed FPR (primary detector metric)

**Definition:** True positive rate on machine-generated text while false-positive rate on human text stays ≤ target.

| Operating point | Use case | Source |
|-----------------|----------|--------|
| **TPR @ FPR=5%** | RAID standard, DAMAGE Table 3, unslop default | Dugan et al. ACL 2024 |
| **TPR @ FPR=1%** | WaterPark watermark eval; stricter deployment | Liang et al. EMNLP 2025 |
| **FPR cap ≤0.5%** | Institutional policy (ESL defense framing) | Jabarian & Imas Booth |

**Why unslop must migrate:** `detector_bench.py` today reports raw AI probability. RAID Table 4 showed detectors hit "99% accuracy" only at similarly high FPR. A humanized essay at 94% P(AI) is meaningless without the threshold that produced it.

**Implementation:**

```python
# Per scenario (domain, attack, hardness tier):
# 1. Collect scores for labeled human + AI (or humanized-AI) pairs
# 2. Binary-search threshold t such that FPR(t) <= 0.05 (ε=0.0005, max 50 iter — RAID protocol)
# 3. Report TPR(t) at that threshold
# 4. Also report ΔTPR = TPR_after_humanize - TPR_before_humanize
```

**Dual-report rule:** Always pair TPR@FPR=5% with mean P(AI) on fixtures. Fixture-level P(AI) is useful for regression diffs; TPR@FPR is useful for cross-paper comparison.

### 2.2 URSS — Unified Reliability-Stability Score (SHIELD)

**Definition:** Non-compensatory product of low-FPR-weighted discrimination and cross-scenario threshold stability.

\[
W\text{-AUROC} = \mathbb{E}_{t \sim p(t)}[\text{TPR}(t)], \quad p(t) = \frac{1}{Z}\exp(-kt), \quad k = 20\ln 2
\]

\[
\text{SFD} = \exp(-\lambda \cdot \sigma_{\text{FPR}}), \quad \lambda = 10\ln 2
\]

\[
\text{URSS} = \left(\frac{1}{M}\sum_i W\text{-AUROC}_i\right) \cdot \text{SFD}
\]

**Why it matters for unslop:** SHIELD showed zero-shot detectors lose ~27–97% URSS under even random word swaps (RMM). Binoculars can top AUROC yet rank last on URSS when SFD collapses. unslop anti-detector claims need hardness-stratified URSS, not a single P(AI) delta.

**Scenarios for unslop URSS bundle (M scenarios):**

| Scenario ID | Description |
|-------------|-------------|
| `clean-fixture` | Assistant-output fixtures, no attack |
| `raid-paraphrase` | T5-11B paraphrase via `raid-bench` |
| `raid-synonym` | BERT synonym swap |
| `esl-short` | Short ESL-style passages (Liang bias regression) |
| `essay-length` | PERSUADE-style academic prose |

**Hardness tiers (within each scenario):**

| Tier | Proxy | SHIELD equivalent |
|------|-------|-------------------|
| `baseline` | Clean / rule-stripped only | Paraphrase-only |
| `low` | Subtle unslop | RMM p≈10–40% equivalent |
| `medium` | Balanced + structural | AWS p≈60% equivalent |
| `high` | Anti-detector LLM pass | RHL R≥15 equivalent |

Do **not** ship SHIELD AWS/RHL generators. Use unslop modes as the hardness ladder; optionally add synthetic RMM (off by default) for stress tests.

### 2.3 TH-Bench quality metrics (co-reporting)

When reporting any detector delta, co-report:

| Metric | Purpose |
|--------|---------|
| ROUGE-L / cosine similarity | Semantic preservation vs original |
| Perplexity (fluency) | Readability cost of humanization |
| Latency / token count | Compute cost (anti-detector is expensive) |

**Prompt paradox (TH-Bench):** naive "rewrite to fool detector" prompts can *increase* detection AUC. unslop's Phase 1 → soul pipeline order is correct; document this when describing anti-detector mode.

### 2.4 Slop metrics (existing, keep)

| Metric | Gate |
|--------|------|
| `ai_isms delta` | `run.py --strict`: delta ≥ 0 |
| `structural_ok` | Preservation contract |
| `burstiness_delta` | Anti-flattening on rhythmic fixtures |

### 2.5 HumanLLM metrics (optional fourth axis)

| Metric | When to run |
|--------|-------------|
| IPE (Individual Pattern Expression) | Role-play / dialogue verbal turns only |
| MPD (Multi-Pattern Dynamics) | Multi-trait scenarios |

Not a substitute for TPR@FPR. Hypothesis to falsify: `anti-detector` may gain on TMR while losing MPD on negative-trait patterns (normative confounding).

---

## 3. Eval harness design

### 3.1 Architecture (target state)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 0: Slop bench (CI, every PR)                                 │
│  benchmarks/run.py — ai_isms, burstiness, preservation              │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 1: Detector bench (release gate, opt-in heavy)               │
│  benchmarks/detector_bench.py — TMR + Desklib                         │
│  + TPR@FPR=5%, URSS bundle, RAID paraphrase/synonym arms            │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 2: Research bench (manual / weekly CI)                       │
│  evals/shield/, TH-Bench quality module, HumanLLM verbal slice      │
│  adversarial_paraphrasing_comparison/ (external clone, opt-in)      │
└───────────────────────────────┬─────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 3: Reference corpus (docs only, no CI)                       │
│  Booth numbers, DAMAGE Table 3, WaterPark DP-40, MGTBench-2.0       │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Layer 1 — `detector_bench.py` upgrades (P0)

**Current state:** 3 fixtures, raw P(AI), TMR + Desklib, release gate = humanized balanced < original on both detectors.

**Target state:**

| Component | Spec |
|-----------|------|
| **Fixtures** | Existing 4+ fixtures + 2 essay-length (PERSUADE subsample) + 1 ESL-short + 1 résumé-bullets |
| **Intensities** | subtle, balanced, full, anti-detector (when LLM tests enabled) |
| **Detectors** | TMR (default), Desklib; optional Binoculars flag for disagreement signal |
| **Attacks** | `--raid-attacks paraphrase,synonym` via `raid-bench` API |
| **Metrics** | P(AI) mean/median; TPR@FPR=5% per fixture slice; ΔTPR; URSS if ≥2 scenarios |
| **Output** | `benchmarks/results/<stamp>-detectors.json` + markdown summary |

**Release gate (revised):**

1. **Slop gate (hard):** `run.py --strict` passes.
2. **Detector regression gate (soft):** humanized balanced must not *increase* mean P(AI) vs original on any fixture (current behavior).
3. **Honesty gate (docs):** if mean ΔP(AI) < 1 pp at balanced, report as "no material detector movement" — do not spin as evasion.

Do **not** gate releases on TPR@FPR matching RAID SOTA. unslop is not training detectors.

### 3.3 New module — `unslop/scripts/shield_metrics.py` (P0)

Pure numpy/scipy. No torch.

```python
def w_auroc(y_true, y_score, k=20 * log(2)) -> float: ...
def sfd(scenario_fprs: list[float], lambda_=10 * log(2)) -> float: ...
def urss(w_aurocs: list[float], sfd: float) -> float: ...
def tpr_at_fpr(y_true, y_score, target_fpr=0.05, eps=0.0005, max_iter=50) -> tuple[float, float]: ...
```

Input: list of (score, label) per scenario. Output: JSON-serializable metrics block appended to detector bench results.

### 3.4 Layer 2 — Research evals (P1)

| Eval | Path | Trigger |
|------|------|---------|
| SHIELD fixture subset | `evals/shield/` | Manual; 50-sample first pass |
| TH-Bench quality | `benchmarks/th_quality.py` (new, opt-in) | Post-LLM anti-detector runs |
| HumanLLM verbal | `benchmarks/humanllm_verbal_bench.py` (new, opt-in) | Dialogue fixtures only |
| DivEye comparison | `benchmarks/diveye_comparison/` | Existing |
| AdvPara comparison | `benchmarks/adversarial_paraphrasing_comparison/` | Existing, opt-in |

### 3.5 Dual-arm protocol (DAMAGE + Booth derived)

Every detector research run should report **two arms**:

| Arm | Description | Proxy benchmark |
|-----|-------------|-----------------|
| **Clean** | Raw assistant output → unslop modes | Booth clean-text arm |
| **Humanized stress** | Cross-model paraphrase second pass OR StealthGPT-equivalent | Booth StealthGPT arm; DAMAGE 19-tool pool |

Report detector-specific outcomes. Booth proved aggregate "humanizer bypass" is false: Pangram robust, GPTZero collapsed ~44–77% FNR on StealthGPT. unslop must not imply a green GPTZero check transfers to Pangram/Turnitin.

### 3.6 Detector roster (what unslop scores vs what it cites)

| Detector | In CI? | Role |
|----------|--------|------|
| **TMR** | Yes | RAID-trained community checkpoint; feedback loop default |
| **Desklib** | Yes | Second RAID-trained scorer; disagreement signal |
| **Binoculars** | Optional | Zero-shot baseline; SHIELD shows URSS collapse under edits |
| **Fast-DetectGPT** | Optional | Curvature family; TH-Bench HMGC target |
| **GPTZero / Pangram / Turnitin** | No (API) | Cite Booth/DAMAGE numbers; log `predicted_class` not `average_generated_prob` if ever tested manually |

TMR's 99.28% RAID AUROC is a **model card fact**, not an unslop evasion claim.

---

## 4. Honest reporting rules

### 4.1 What unslop CAN claim (evidence-bound)

| Claim | Evidence source |
|-------|-----------------|
| Removes visible AI-isms (delve, hedging stacks, sycophancy openers) | `run.py` fixtures, validator |
| Preserves code, URLs, headings, tables | TestPreservation suite |
| Deterministic pass does not materially fool RAID-trained classifiers | `detector_bench.py` ~0.1–0.2 pp ΔP(AI) |
| Lexical humanization is a weak evasion axis | TH-Bench Prompt/HMGC results; RAID synonym −36 pp on Binoculars |
| Detector-score optimization ≠ slop removal | TH-Bench three-axis Pareto; HumanLLM normative confounding |
| Legacy detectors collapse on humanized text | DAMAGE Table 3 (GPTZero −40 pp, Binoculars −66 pp) |
| Commercial detector rankings are humanizer-specific | Booth StealthGPT arm; DAMAGE vendor COI note |
| Rewrite passes may affect embedded watermarks | WaterPark Table 2; Art. 50 side-effect disclosure |

### 4.2 What unslop MUST NOT claim

| Forbidden claim | Why |
|-----------------|-----|
| "Beats RAID" / "99% RAID AUROC" as unslop score | AUROC belongs to TMR model, not unslop output |
| "Passes Chicago Booth" | No such threshold; unslop not in study |
| "Twelve humanizer services" under Booth citation | Booth tested **one** (StealthGPT); use HumanizerBench/DAMAGE for multi-tool |
| "~6 points median accuracy drop" | Not in Jabarian & Imas; remove or cite primary source |
| "Turnitin 60–85% on humanized text" under Booth | Turnitin not in Booth corpus |
| "Evades GPTZero/Turnitin" from TMR score alone | Different training, patch cadence, ensemble layers |
| "Safe for academic misconduct" | Boundaries: ESL/resume/voice only |
| "Watermark removal" | Art. 50; WaterPark ethics |

### 4.3 Reporting template (README / research appendix)

```markdown
## Detector eval (research)

**Setup:** N fixtures, intensities [subtle|balanced|full|anti-detector], detectors [TMR, Desklib],
attacks [none|RAID paraphrase|RAID synonym], metric TPR@FPR=5% + URSS.

| Condition | Mean P(AI) | TPR@5% FPR | Δ vs clean | ROUGE-L | Latency |
|-----------|------------|------------|------------|---------|---------|
| Original | ... | ... | — | 1.00 | — |
| balanced | ... | ... | ... | ... | ... |
| anti-detector | ... | ... | ... | ... | ... |

**Interpretation:** [One sentence. Example: "Deterministic balanced moved TMR ≤0.2 pp;
no material evasion. Anti-detector reduced P(AI) X pp with ROUGE-L Y; TPR@5% still Z%."]

**References:** RAID (Dugan et al. 2024), SHIELD (Ayoobi et al. 2025), DAMAGE (Masrour et al. 2025).
unslop is not evaluated on commercial APIs unless explicitly noted.
```

### 4.4 README / SKILL.md attribution fixes (from Agent #62)

| Current (if present) | Correct attribution |
|---------------------|---------------------|
| "Chicago Booth 2026, twelve humanizers" | Booth = Jabarian & Imas 2025, **1 humanizer** (StealthGPT); "2026" = GPTZero rebuttal branding |
| "Six-point median drop" | Remove or cite HumanizerBench/DAMAGE with date |
| "Turnitin drops there" | Cite Turnitin press / MPG ONE, not Booth |

### 4.5 Version and reproducibility requirements

Every published detector number must log:

- unslop version / git SHA
- Detector model IDs (`Oxidane/tmr-ai-text-detector`, etc.)
- `raid-bench` version if attacks used
- Fixture list + intensity
- Date (detector weights drift monthly)

Never round benchmark numbers from papers. Quote from real runs or cite paper tables with source.

### 4.6 Ethics co-reporting

| Topic | Required disclosure |
|-------|---------------------|
| Anti-detector mode | ESL/resume defensive use; not academic misconduct |
| Watermark side effect | Rewrite may degrade SynthID/KGW marks; not a removal feature |
| DAMAGE COI | Pangram-authored; cite collapse shape, not Pangram robustness as unslop proof |
| Booth dispute | GPTZero rebuttal re-ran clean text only; humanizer arm unreplicated |
| SHIELD humanification | Eval-only; do not ship AWS/RHL |

---

## 5. Priority roadmap

### P0 — Next sprint

1. **`shield_metrics.py`** — W-AUROC, SFD, URSS, `tpr_at_fpr()`
2. **Extend `detector_bench.py`** — emit TPR@FPR=5% alongside P(AI); add `--raid-attacks paraphrase,synonym`
3. **Fix README misattributions** — Booth twelve-humanizer, six-point drop (Agent #62)
4. **Document** in `benchmarks/README.md` that slop delta ≠ detector evasion

### P1 — Following sprint

5. **`evals/shield/`** — 50-sample fixture URSS comparison (baseline vs balanced vs anti-detector)
6. **TH-Bench quality module** — ROUGE-L + cos-sim on anti-detector output
7. **Essay + ESL fixture slices** — RAID confound + Liang bias regression
8. **Dual-arm reporting** — clean vs cross-model paraphrase in detector JSON

### P2 — Backlog

9. MGTBench-2.0 `Computer_science` + `Literature` subsample (100 pairs)
10. HumanLLM verbal bench (dialogue fixtures, IPE/MPD delta)
11. Optional Binoculars second opinion in detector bench
12. Cross-benchmark dashboard JSON (RAID + SHIELD + slop + quality)

### P3 — Reference only

13. WaterPark numbers in research synthesis (provenance)
14. Booth policy-cap framing in ESL defense docs
15. RAID generalization track submission (third-party credibility)

---

## 6. Reconciled picture across benchmarks

The seven input memos describe a **stack**, not a winner-take-all competition:

```
                    ┌──────────────┐
                    │  HumanLLM    │  cognitive fidelity (optional)
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │      TH-Bench           │  evasion × quality × cost
              └────────────┬────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │  RAID   │      │  SHIELD   │     │  DAMAGE   │
    │ attacks │      │ URSS/     │     │ commercial│
    │ + models│      │ hardness  │     │ humanizers│
    └────┬────┘      └─────┬─────┘     └─────┬─────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼───────┐
                    │ Booth 2025   │  independent commercial audit
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  WaterPark   │  watermark robustness (ethics ref)
                    └──────────────┘
```

**Tension resolved:** RAID COLING 2025 shared task showed 99%+ TPR@5% when detectors train on RAID's known attack catalog. RAID ACL 2024 showed zero-shot collapse under synonym swap. Both are true — the answer depends on **who trains on what**. unslop trains nothing; it humanizes. Expect deterministic passes to behave like **weak perturbations** (TH-Bench Prompt class), not HMGC or StealthRL.

**Sadasivan vs DAMAGE vs Booth:** Detection is not permanently solved (TV-distance bound) and not permanently broken (humanizer-augmented training works today). unslop sits in the **user-facing middle**: make text readable, document detector limits honestly, refuse laundering claims.

---

## 7. Key numbers reference (for maintainers)

| Claim | Value | Source | unslop use |
|-------|-------|--------|------------|
| Deterministic Δ TMR | ~0.0–0.2 pp | `detector_bench.py` | Primary honest finding |
| RAID Binoculars synonym TPR@5% | 43.5% (−36 pp) | RAID Table 6 | Why rules aren't enough |
| RAID Pangram paraphrase TPR@5% | 91.6% | COLING 2025 Task 3 | Best-case adapted detector |
| SHIELD URSS drop under RMM | ~27–97% (zero-shot) | SHIELD Table 2 | Why URSS > AUROC |
| DAMAGE GPTZero humanized TPR@5% | 60.04% (−40 pp) | DAMAGE Table 3 | Legacy collapse cite |
| DAMAGE Binoculars humanized | 28.23% (−66 pp) | DAMAGE Table 3 | Perplexity family fragility |
| Booth GPTZero StealthGPT FNR | ~44–77% | Booth Table B.4 | Commercial humanizer stress |
| Booth Pangram StealthGPT FNR | ~0–5% | Booth Table B.4 | Detector-specific outcomes |
| WaterPark SynthID DP-40 TPR | 0.498 @ FPR=1% | WaterPark Table 2 | Provenance side-effect |
| TH-Bench HMGC → Log-Likelihood AUC | 0.913 → 0.185 | TH-Bench Table 1 | Surrogate attack power (don't ship) |

---

## 8. Citations

```bibtex
@inproceedings{dugan-etal-2024-raid,
  title={{RAID}: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors},
  author={Dugan, Liam and others},
  booktitle={ACL 2024},
  pages={12463--12492},
  year={2024}
}

@article{ayoobi2025shield,
  title={Beyond Easy Wins: A Text Hardness-Aware Benchmark for {LLM}-generated Text Detection},
  author={Ayoobi, Navid and Shahriar, Sadat and Mukherjee, Arjun},
  journal={arXiv:2507.15286},
  year={2025}
}

@inproceedings{zheng2025thbench,
  title={{TH-Bench}: Evaluating Evading Attacks via Humanizing {AI} Text on Machine-Generated Text Detectors},
  author={Zheng, Jingyi and others},
  booktitle={KDD 2025},
  year={2025}
}

@inproceedings{masrour2025damage,
  title={{DAMAGE}: Detecting Adversarially Modified {AI} Generated Text},
  author={Masrour, Elyas and Emi, Bradley and Spero, Max},
  booktitle={GenAIDetect, COLING 2025},
  pages={120--133},
  year={2025}
}

@article{jabarian2025booth,
  title={Artificial Writing and Automated Detection},
  author={Jabarian, Sima and Imas, Alex},
  journal={NBER Working Paper 34223},
  year={2025}
}

@inproceedings{liang2025waterpark,
  title={Watermark under Fire: A Robustness Evaluation of {LLM} Watermarking},
  author={Liang, Jiacheng and others},
  booktitle={EMNLP 2025 Findings},
  pages={21050--21074},
  year={2025}
}

@inproceedings{wang2026humanllm,
  title={Human{LLM}: Benchmarking and Improving {LLM} Anthropomorphism via Human Cognitive Patterns},
  author={Wang, Yujie and others},
  booktitle={ACL 2026},
  year={2026}
}
```

---

## 9. Cross-references

| Agent | Contribution to this synthesis |
|-------|----------------------------------|
| #12 DAMAGE | TPR@FPR protocol, L1/L2/L3 tiers, Table 3 collapse numbers |
| #15 RAID | Primary citation anchor, attack slices, metric standard |
| #16 SHIELD | URSS metric layer, hardness ladder concept |
| #19 MGTBench/TH-Bench | Three-axis reporting, Prompt paradox |
| #20 WaterPark | Provenance ethics, DIPPER shared attack |
| #36 HumanLLM | Fourth axis, normative confounding |
| #62 Booth | Commercial audit framing, attribution fixes |

---

*SYNTH-84 complete. unslop benchmarks slop removal in CI, detector signal in opt-in heavy runs with TPR@FPR=5% and URSS, and cites RAID/DAMAGE/Booth for honest external context — without pretending deterministic passes solve the arms race.*
