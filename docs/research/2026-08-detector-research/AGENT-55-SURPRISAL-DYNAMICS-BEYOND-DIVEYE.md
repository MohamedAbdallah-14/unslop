# Agent #55 — Surprisal Dynamics Humanization Beyond DivEye

**Focus:** TSD, SurpMark, late-stage signals — 2026 dynamics stack vs `unslop/scripts/surprisal.py` gaps  
**Date:** 2026-08-19  
**Scope:** Detection theory, humanization targets, implementation audit. Not DivEye reproduction (see Agent #34).

---

## Executive summary

The 2026 detector frontier moved from **"how surprising is this text on average?"** to **"how does surprise move through the text?"** Three papers define the stack:

1. **DivEye** (Basani & Chen, TMLR 2026) — global distributional + first/second-order surprisal statistics over the **full sequence**. unslop ships a numerically aligned 10-feature extractor; it does **not** classify or humanize against those features in the feedback loop.
2. **TSD** (Sun et al., arXiv Jan 2026) — **late-stage volatility decay**: AI surprisal stabilizes faster in the **second half** (24–32% lower derivative/local volatility). unslop computes some related quantities globally but **never conditions on position**.
3. **SurpMark** (Chen & Khisti, ICML 2026) — discretized surprisal **state transitions** scored via generalized Jensen–Shannon gap vs human/machine reference corpora. unslop has **zero** transition-matrix or recovery-pattern machinery.

**unslop verdict:** `surprisal.py` is a solid DivEye **measurement** module (bit-matched to IBM code on GPT-2). It is not a 2026 dynamics stack. Anti-detector mode still optimizes lexical burstiness and TMR; surprisal_stdev is optional telemetry in `detector.feedback_loop()`, not a stop condition. Closing the gap means **position-aware** and **transition-aware** targets — not widening global σ alone.

---

## Primary URLs

| Resource | URL |
|----------|-----|
| DivEye paper (TMLR 2026) | https://arxiv.org/abs/2509.18880 |
| DivEye HTML | https://arxiv.org/html/2509.18880v3 |
| IBM DivEye GitHub | https://github.com/IBM/diveye |
| HF Space (deployed classifier) | https://huggingface.co/spaces/pinyuchen/Diveye_AI_text_detector |
| TSD: When AI Settles Down | https://arxiv.org/abs/2601.04833 |
| TSD HTML | https://arxiv.org/html/2601.04833v1 |
| TSD DOI | https://doi.org/10.48550/arxiv.2601.04833 |
| SurpMark paper | https://arxiv.org/abs/2510.07500 |
| SurpMark HTML | https://arxiv.org/html/2510.07500v3 |
| SurpMark OpenReview (ICLR submission) | https://openreview.net/forum?id=eDJsc3KXZC |
| SurpMark GitHub | https://github.com/shuangyichen/SurpMark |
| Lastde / Lastde++ (ICLR 2025) | https://arxiv.org/abs/2410.06072 |
| Lastde code | https://github.com/TrustMedia-zju/Lastde_Detector |
| Fast-DetectGPT (TSD fusion baseline) | https://arxiv.org/abs/2310.05130 |
| EvoBench (TSD eval) | https://arxiv.org/abs/2505.05239 |
| MAGE benchmark | https://arxiv.org/abs/2305.14902 |
| unslop surprisal module | `unslop/scripts/surprisal.py` |
| unslop DivEye alignment bench | `benchmarks/diveye_comparison/run.py` |
| unslop dynamics update plan | `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md` |

---

## 1. The 2026 surprisal dynamics stack

Detectors now treat token surprisal \(s_t = -\log P(x_t \mid x_{<t})\) as a **time series**, not a bag of numbers. Methods differ by *which* summary they take.

### 1.1 Layer map

```
Token surprisal sequence s₁…sₙ  (one forward pass, proxy LM)
        │
        ├─ GLOBAL distributional     DivEye: μ, σ, σ², γ₁, γ₂
        ├─ GLOBAL temporal (full seq) DivEye: Δμ, Δσ; Δ² variance, H, ρ
        ├─ POSITION-SPLIT temporal    TSD: DD + LV on second half only
        ├─ DISCRETE Markov dynamics   SurpMark: k-state transitions → ΔGJS
        └─ LOCAL multiscale entropy   Lastde++: MDE windows + log-likelihood
```

These layers are **largely orthogonal**. TSD paper ablations: second-half TSD beats full-sequence aggregation by **6+ AUROC points** on EvoBench (83.36% vs 77.00%). DivEye ablations: second-order features contribute **~39%** of XGBoost importance — but computed over the **whole** document, diluting late-stage signal. SurpMark explicitly targets the **recovery pattern**: after a "highly surprising" token, LLM text snaps back to predictable states faster than human text.

### 1.2 DivEye (baseline — shipped in unslop)

**Paper:** Basani & Chen, *Diversity Boosts AI-Generated Text Detection*, TMLR 2026.  
**URL:** https://arxiv.org/abs/2509.18880

**Core claim:** LLM text has **narrower intra-document surprisal variance** than human text — the opposite of early perplexity-only detectors. Paraphrase attacks preserve mean perplexity but compress rhythmic variance.

**Feature vector (paper Eq. 6 — 9 dims):**

\[
\mathcal{D} = \{\underbrace{\mu_s, \sigma_s^2, \gamma_1, \gamma_2}_{\text{distribution}} \oplus \underbrace{\Delta\mu, \Delta\sigma^2}_{\text{1st-order}} \oplus \underbrace{\sigma^2_{\Delta^2}, H_{\Delta^2}, \rho_{\Delta^2}}_{\text{2nd-order}}\}
\]

**Shipped IBM code / unslop:** 10 dims — adds σ alongside σ²; first-order block uses std not variance. unslop `to_diveye_vector()` tracks **code**, not paper Eq. 6 (Agent #34 audit).

**Detection:** Features alone are not a detector — XGBoost (or HF Space ensemble with BiScope + compression ratio) required.

**Reported robustness:** AUROC ~0.87–0.99 on MAGE depending on testbed; ~0.87 under RAID paraphrase (vs Binoculars N/A on paraphrase category).

### 1.3 TSD — Temporal Stability Detection (gap)

**Paper:** Sun, Bao, Cui, Zhang — *When AI Settles Down: Late-Stage Stability as a Signature of AI-Generated Text Detection*, Jan 2026.  
**URL:** https://arxiv.org/abs/2601.04833

**Phenomenon — Late-Stage Volatility Decay (LSVD):** Both human and AI surprisal volatility falls as context grows. AI decays **1.8–2.6× faster**. Gap peaks in positions 50–100% of sequence:

| Dataset | 2nd-half derivative gap (AI vs human) | 2nd-half local-σ gap |
|---------|----------------------------------------|----------------------|
| EvoBench | −32% | −31% |
| MAGE | −24% | −25% |

**Features (second half only, \( \mathcal{H}_2 = \{i \mid i > \lfloor n/2 \rfloor\} \)):**

1. **Derivative Dispersion (DD):** \(\text{Std}(\{|s_i - s_{i-1}|\}_{i \in \mathcal{H}_2})\)
2. **Local Volatility (LV):** Mean of sliding-window std of surprisal, window \(w=20\), over \(\mathcal{H}_2\)

**Score:** \(S_{\text{TSD}} = -(\text{DD} + \text{LV})\). Higher → more likely AI.

**Benchmarks (Llama-3-8B-Instruct surrogate, max 512 tokens):**

| Method | EvoBench AUROC | MAGE AUROC |
|--------|----------------|------------|
| TSD (standalone) | **83.36%** | **71.56%** |
| Fast-DetectGPT | ~73–77% (per paper table) | lower |
| DivEye | 74.40% (TSD paper baseline row) | varies |
| Lastde | 76.66% | — |
| TSD+ (TSD + Fast-DetectGPT) | **85.37%** | **75.20%** |

**Key ablations:**

- Second half only: **83.36%** vs full sequence **77.00%** vs first half **63.59%** (EvoBench).
- Optimal start position: relative **50%** midpoint; 90% start collapses MAGE to 63%.
- Length sensitivity: TSD weak below ~100 tokens; strong above 150. FLAN-T5 short outputs are a known failure mode (35% → 56% with fusion).

**Relation to DivEye:** Complementary. DivEye aggregates global σ and Δ² statistics; TSD asks whether volatility **collapsed too fast** in the back half. TSD paper cites DivEye as capturing "rhythmic diversity" but not targeting LSVD explicitly.

**Code:** No official GitHub as of Aug 2026. Method is ~20 lines on an existing surprisal tensor.

### 1.4 SurpMark (gap)

**Paper:** Chen & Khisti — *Black-Box Detection of LLM-Generated Text Using Generalized Jensen–Shannon Divergence*, ICML 2026.  
**URL:** https://arxiv.org/abs/2510.07500  
**Code:** https://github.com/shuangyichen/SurpMark

**Core idea:** Likelihood-free hypothesis test on **surprisal dynamics**, not scalar perplexity.

**Pipeline:**

1. Proxy LM → token surprisal sequence (single forward pass).
2. **k-means** discretize surprisals into k states (e.g. Predictable / Slightly / Significantly / Highly Surprising).
3. Estimate first-order **transition matrix** \(\hat{M}_T\) for test text.
4. Offline: build reference matrices \(\hat{M}_P\) (machine), \(\hat{M}_Q\) (human) from corpora.
5. Score: \(\Delta\text{GJS}_n = \text{GJS}(\hat{M}_P, \hat{M}_T, \alpha) - \text{GJS}(\hat{M}_Q, \hat{M}_T, \alpha)\).

**Recovery phenomenon:** LLM text shows stronger transition **into** predictable states immediately after a high-surprisal token (perplexity-minimization snap-back). Human text maintains messier transition structure.

**Theory:** \(\Delta\text{GJS}_n\) equals normalized generalized log-likelihood ratio (Prop 3.4). Optimal bin count scales \(k^* = \Theta(N^{1/5})\).

**Benchmarks (avg AUROC across XSum, WritingPrompts, SQuAD, 9 OSS models):**

| Method | Avg AUROC |
|--------|-----------|
| SurpMark\(_{k=6}\) | **91.23%** |
| Lastde++ | 90.04% |
| Fast-DetectGPT | 88.01% |
| Binoculars | 86.19% |
| DivEye | not in SurpMark table |

**Practical constraints for unslop:**

- Requires **reference corpora** (human + machine) to build \(\hat{M}_P, \hat{M}_Q\) and shared quantizer \(q_k\).
- Black-box friendly: no perturbation sampling, no source-model access.
- Higher-order Markov **hurts** (state-space explosion) — first-order only.

### 1.5 Adjacent temporal methods (context, not shipped)

| Method | URL | Signal | vs unslop |
|--------|-----|--------|-----------|
| **Lastde++** | https://arxiv.org/abs/2410.06072 | Multiscale diversity entropy on probability sequences + log-likelihood | Local windows; not position-split LSVD |
| **Fast-DetectGPT** | https://arxiv.org/abs/2310.05130 | Sampling discrepancy (global) | Fused with TSD as TSD+ |
| **FourierGPT / Spectrum** | Xu et al. 2024 | Frequency-domain likelihood | TSD paper: near-random alone |
| **UCE (Hou et al. 2025)** | cited in TSD related work | Uncertainty contraction over prefixes | Theoretical sibling to LSVD; text UCE distinct from AAAI 2026 time-series UCE (https://arxiv.org/abs/2511.07104) |

---

## 2. unslop `surprisal.py` — what it actually does

**File:** `unslop/scripts/surprisal.py`  
**Entry:** `compute_surprisal_variance(text, model="distilgpt2", max_tokens=1024)`

### 2.1 Implemented signals

| Output field | DivEye index | TSD analog | SurpMark analog |
|--------------|-------------|------------|-----------------|
| `-mean_log_prob` | 0 (mean surprisal) | — | — |
| `surprisal_stdev` | 1 | — | — |
| `surprisal_variance` | 2 | — | — |
| `surprisal_skewness` | 3 | — | — |
| `surprisal_kurtosis` | 4 | — | — |
| `delta_surprisal_mean` | 5 | partial (global Δ mean, not \|Δ\|) | — |
| `delta_surprisal_stdev` | 6 | **DD uses Std(\|Δ\|) on H₂** | — |
| `delta2_surprisal_variance` | 7 | — | — |
| `delta2_surprisal_entropy` | 8 | — | — |
| `delta2_surprisal_autocorr` | 9 | — | — |
| `surprisal_cv` | extra | — | — |

**Alignment:** IBM `diveye_utils.py` match on GPT-2, max relative error < 3×10⁻⁶ (`benchmarks/results/diveye_comparison.json`, Agent #34).

### 2.2 Design choices

- **Default LM:** `distilgpt2` (82M) — fast, offline-friendly. Paper/PAN use `gpt2`; HF demo uses `tiiuae/falcon-7b`. Absolute stdev bands differ; rank order usually preserved (not fully benchmarked distil vs gpt2 on humanize before/after).
- **Truncation:** 1024 tokens post-encode. TSD eval uses 512; late-half features need ≥~100 tokens to stabilize.
- **Aggregation:** All statistics are **document-global**. No percentile normalization, no \(\mathcal{H}_2\) split, no sliding-window LV.
- **Role:** Voice-match telemetry and `--surprisal-variance` CLI JSON dump. **Not** wired as humanization objective.

### 2.3 Integration status elsewhere in unslop

| Consumer | Uses surprisal? | How |
|----------|----------------|-----|
| `detector.feedback_loop()` | Optional log only | `surprisal_fn` → records `surprisal_stdev` per iteration; **not** stop criterion |
| `humanize.py` | Proxy only | `word_length_stdev` labeled "DivEye-style proxy" in voice-match prompt |
| `stylometry.py` | Proxies | `sentence_length_cv`, `word_length_stdev` — no LM |
| `skills/unslop/SKILL.md` anti-detector | Mention | "Vary surprisal across the document" — prose, not computed |
| Anti-detector deterministic pass | No | Targets lexical/structural, not LM dynamics |
| `benchmark.py` | No dual-oracle row | Agent #50 gap: stylometry + surprisal not co-reported |

**Bottom line:** DivEye measurement exists; DivEye **humanization loop** does not.

---

## 3. Gap matrix — 2026 stack vs unslop

| Capability | DivEye | TSD | SurpMark | unslop today |
|------------|--------|-----|----------|--------------|
| Token surprisal sequence | ✅ | ✅ | ✅ | ✅ (internal) |
| Global σ, variance, skew, kurt | ✅ | — | — | ✅ |
| Global Δ / Δ² statistics | ✅ | — | — | ✅ |
| Second-half-only features | — | ✅ | — | ❌ |
| Sliding-window local volatility | — | ✅ | — | ❌ |
| \|Δ\| dispersion (DD) | partial | ✅ | — | ❌ (signed Δ only) |
| Position-normalized curves | — | ✅ | — | ❌ |
| Surprisal discretization (k-means) | — | — | ✅ | ❌ |
| Transition matrix | — | — | ✅ | ❌ |
| Reference corpora + ΔGJS | — | — | ✅ | ❌ |
| Recovery-pattern targeting | — | — | ✅ | ❌ |
| XGBoost / classifier head | external | threshold | threshold | ❌ (by design) |
| BiScope + compression (HF Space) | external | — | — | ❌ |
| Feedback loop stop on dynamics | — | — | — | ❌ |
| Deterministic late-half injection | — | — | — | ❌ |

### 3.1 What global DivEye widening misses

Widening **global** `surprisal_stdev` (anti-detector intuition) does not guarantee:

1. **Higher second-half DD/LV** — you can add front-loaded spikes and leave the back half smooth (TSD still flags AI).
2. **Human-like transition structure** — random spikes followed by immediate predictability mimic LLM recovery; SurpMark may still score machine-like.
3. **Length adequacy** — short paragraphs never manifest LSVD; TSD is weak <100 tokens.

Humanization must **shape the trajectory**, not just inflate variance.

### 3.2 Partial overlaps (do not double-count)

- `delta_surprisal_stdev` correlates with DD but differs: global std of **signed** differences vs second-half std of **absolute** differences.
- `delta2_*` features capture acceleration of surprisal; TSD LV captures **local** regime stability — related but not redundant.
- DivEye second-order block (39% importance) ≠ TSD late-half block (6+ AUROC points over full-seq TSD).

---

## 4. Humanization implications (defensive use only)

Per unslop Boundaries: anti-detector mode is for ESL false positives and legitimate voice repair — not academic misconduct.

### 4.1 Target profile (human band — qualitative)

From papers, human text tends to show:

- **Higher global surprisal variance** (DivEye)
- **Sustained volatility in positions 50–100%** (TSD: higher DD and LV)
- **Less predictable snap-back** after surprising tokens (SurpMark: weaker P(high→low) recovery)
- **Irregular Δ² clustering** (DivEye ρ, H on Δ²)

AI slop tends toward: flat global σ, collapsing back-half, recovery transitions, uniform smoothing.

### 4.2 Deterministic levers (Phase 2 — `dynamics_targets.py` per UPDATE-PLAN)

| Lever | Addresses | Mechanism |
|-------|-----------|-----------|
| **Back-half entropy injection** | TSD DD/LV | Reserve 1–2 lexical surprises, structural breaks, or register shifts for final 40% of paragraph |
| **Anti-recovery edits** | SurpMark | After an unusual word choice, *avoid* immediate generic glue ("Furthermore," "In conclusion"); follow with another low-probability but coherent choice |
| **Position-aware burstiness** | TSD + DivEye | Don't front-load all variation; `structural.py` sentence-length CV should not collapse in late sentences |
| **Cone-widen swaps** (separate signal) | GPTZero v6 | High-surprisal ≠ high top-k mass — need out-of-cone synonyms |

### 4.3 LLM levers (Phase 3)

- **Cross-model second pass** — changes transition structure, not just vocabulary (Agent #35).
- **TempParaphraser-style multi-sample** on high-surprisal sentences — targets local dynamics.
- **Adversarial paraphrasing** against ensemble including dynamics scorers — not TMR alone.

### 4.4 What not to do

- Uniform synonym noise → may raise global σ while **lowering** DD in second half (models settle after perturbation).
- Perfectly smooth anti-detector output → fails DivEye *and* TSD.
- Optimizing TMR alone → StealthRL/Binoculars axis; orthogonal to SurpMark transitions.

---

## 5. Recommended implementation (priority order)

Aligned with `UPDATE-PLAN-2026-08.md` Phase 1–2.

### P0 — Wire existing measurement (days)

1. **`--detector-surprisal` in CLI feedback** — log full `SurprisalReading.to_dict()`, not just stdev.
2. **Extend `detector_bench`** — before/after humanize: DivEye vector + TSD + SurpMark on fixture corpus.
3. **Document default model** — `--surprisal-model gpt2` for paper replication; keep distilgpt2 as speed default.

### P1 — TSD in `surprisal.py` (1–2 weeks)

```python
@dataclass
class TSDReading:
    derivative_dispersion: float  # DD on H2
    local_volatility: float       # LV on H2, w=20
    tsd_score: float              # -(DD + LV)
    token_count_second_half: int
    start_position: int           # floor(n/2)

def compute_tsd_reading(text, *, model=..., max_tokens=512, window=20) -> TSDReading
```

Reuse existing surprisal tensor from `compute_surprisal_variance` internals — avoid second forward pass.

**Acceptance:** On `benchmarks/` fixtures, anti-detector pass increases DD on ≥7/9 long samples without collapsing semantic validators.

### P2 — SurpMark lite (2–3 weeks)

- Ship frozen reference matrices from public human/machine slices (SQuAD/XSum-style, k=6, GPT-2-large proxy per paper default).
- `compute_surpmark_reading(text) -> {delta_gjs, transition_matrix, k}`.
- Store references under `benchmarks/fixtures/surpmark_refs/` (NC license check for DivEye training data — SurpMark refs are separate corpora).

**Acceptance:** Human fixtures closer to \(\hat{M}_Q\) than machine fixtures on held-out bench split.

### P3 — Unified dynamics API

```python
def compute_surprisal_dynamics(text) -> SurprisalDynamicsReading:
    """DivEye vector + TSD + SurpMark + optional cone proxy."""
```

Feed `dynamics_targets.gap_vs_human(reading)` for anti-detector LLM prompts.

### P4 — Multi-objective feedback loop

Extend `detector.feedback_loop()`:

```
stop when: TMR ≤ target
       AND surprisal_stdev ∈ [p25, p75]_human
       AND tsd_score ≤ human_p75  (lower AI likelihood)
       AND delta_gjs ≥ τ_human
```

---

## 6. Evasion / arms-race notes

| Attack | DivEye | TSD | SurpMark |
|--------|--------|-----|----------|
| Synonym swap | Moderate resistance | Moderate | **High** (transitions change) |
| DIPPER paraphrase | Partially survives | Unknown | Unknown |
| Adversarial Paraphrasing (detector-guided) | Vulnerable | Vulnerable | Vulnerable if surrogate in loop |
| StealthRL (RL ensemble) | **Not evaluated** | **Not evaluated** | **Not evaluated** |
| Cross-model paraphrase | Best practical lever | Likely helps back-half | Likely helps transitions |

**Sadasivan TV bound** still applies: sufficiently strong paraphrase can close any single scalar signal. Dynamics stack raises bar from "swap words" to "reshape generative trajectory."

---

## 7. Benchmarks unslop should run (no invented numbers)

1. **Fixture sweep:** `surprisal_stdev`, DD, LV, ΔGJS before/after each intensity mode on `benchmarks/fixtures/*.md`.
2. **distilgpt2 vs gpt2 vs falcon-7b** rank correlation on humanize outputs.
3. **Length stratification:** TSD readings vs token_count (expect cliff <100 tokens).
4. **Dual-oracle row** (Agent #50): stylometry delta + dynamics delta on same rewrite.
5. **StealthRL / AdvPara stress** — when open weights available; document as open gap.

---

## 8. Confidence & open questions

| Finding | Confidence |
|---------|------------|
| unslop implements DivEye **code** vector, not paper Eq. 6 | **High** (Agent #34 empirical) |
| TSD orthogonality to global DivEye | **High** (TSD ablations + DivEye ablations) |
| SurpMark recovery pattern as LLM tell | **High** (ICML 2026 paper + code) |
| Deterministic unslop passes move TSD DD materially | **Low** — **not measured** |
| distilgpt2 preserves humanize before/after ordering vs gpt2 | **Medium** |
| Text UCE (Hou 2025) separate from AAAI time-series UCE | **Medium** — TSD cites Hou 2025 for contraction; verify text preprint if wiring UCE |

---

## 9. Key code references

unslop DivEye export (`unslop/scripts/surprisal.py:107-119`):

```python
def to_diveye_vector(self) -> list[float]:
    return [
        -self.mean_log_prob, self.surprisal_stdev, self.surprisal_variance,
        self.surprisal_skewness, self.surprisal_kurtosis,
        self.delta_surprisal_mean, self.delta_surprisal_stdev,
        self.delta2_surprisal_variance, self.delta2_surprisal_entropy,
        self.delta2_surprisal_autocorr,
    ]
```

TSD score (paper Eq. 5):

\[
S_{\text{TSD}} = -(\text{DD} + \text{LV}), \quad \text{DD} = \text{Std}(\{|s_i - s_{i-1}|\}_{i \in \mathcal{H}_2}), \quad \text{LV} = \text{Mean}(\{\ell_i\}_{i \in \mathcal{H}_2})
\]

SurpMark decision (paper Eq. 2):

\[
\Delta\text{GJS}_n = \text{GJS}(\hat{M}_P, \hat{M}_T, \alpha) - \text{GJS}(\hat{M}_Q, \hat{M}_T, \alpha)
\]

---

## 10. Non-overlap with sibling agents

| Agent | Scope |
|-------|-------|
| **#1 / #34** | DivEye theory vs IBM implementation audit |
| **#50** | Jemama fidelity vs PPL dual-oracle |
| **#09** | PHD embedding geometry (orthogonal axis) |
| **#55 (this memo)** | TSD + SurpMark + late-stage stack vs `surprisal.py` |

**One-line takeaway:** unslop solved DivEye **measurement**. The 2026 detector arms race runs on **where** and **how** surprisal moves — TSD (when) and SurpMark (what state comes next). Until `surprisal.py` grows position- and transition-aware readings and the feedback loop stops on them, anti-detector mode is structurally blind to half the dynamics stack.

---

*Agent #55 complete.*
