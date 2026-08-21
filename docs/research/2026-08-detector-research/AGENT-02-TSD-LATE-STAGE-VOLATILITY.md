# Agent #02 — TSD: Late-Stage Volatility Decay

**Focus:** Sun et al., *When AI Settles Down* (arXiv:2601.04833) — mechanism, benchmarks, debate, humanization, unslop integration  
**Date:** 2026-08-19  
**Scope:** Exhaustive web research on TSD / Late-Stage Volatility Decay (LSVD). Cross-read: `unslop/scripts/structural.py`, `docs/RESEARCH_AND_TECH.md`.

---

## Executive summary

TSD (Temporal Stability Detection) is a zero-shot AI-text detector from Westlake University (Jan 2026) that exploits **Late-Stage Volatility Decay**: as autoregressive models accumulate context, token surprisal fluctuations shrink faster than in human writing. The gap peaks in the **second half** of a passage (24–32% lower derivative and local volatility for AI on EvoBench/MAGE).

The method is deliberately minimal. A surrogate LM (Llama-3-8B-Instruct in the paper) computes per-token surprisal \(s_i = -\log P(t_i \mid t_{<i})\). Two features are extracted **only from positions after the midpoint**:

1. **Derivative Dispersion (DD)** — std of absolute first differences \(|s_i - s_{i-1}|\)
2. **Local Volatility (LV)** — mean of sliding-window (w=20) std of surprisal

Score: \(S_{\text{TSD}} = -(\text{DD} + \text{LV})\). Higher → more likely AI. No training, no perturbation sampling, no source-model access.

On academic benchmarks TSD reaches **83.36% AUROC (EvoBench avg)** and **71.56% (MAGE avg)**, beating Fast-DetectGPT, DivEye, Lastde, and DetectGPT-style baselines in the paper's unified table. Fusion with Fast-DetectGPT (TSD+) pushes to **85.37% / 75.20%**. The paper does **not** evaluate GPTZero, Turnitin, or other commercial APIs.

**Community footprint is thin.** One trade press write-up (Unite.AI, Jan 26 2026). No dedicated Hacker News front-page thread found. No official GitHub repo — only the related [baoguangsheng/fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt) from the same lab.

**Humanization implication:** unslop's current stack widens **global** burstiness (sentence-length σ in `structural.py`, global surprisal stdev in `surprisal.py`) but does **not** shape **where** volatility lives. TSD specifically penalizes texts whose **back half** settles down. Anti-detector work must inject sustained lexical surprise in the latter half — not just front-load spikes or inflate document-wide σ.

**unslop gap:** `surprisal.py` computes DivEye's global Δ statistics including `delta_surprisal_stdev`, but never splits at \(\lfloor n/2 \rfloor\), never computes LV, and never feeds position-aware targets into `detector.feedback_loop()`. `structural.py` targets a different axis (sentence-length variance). Both are necessary; neither closes the TSD hole alone.

---

## Primary URLs

| Resource | URL |
|----------|-----|
| **Paper (arXiv abstract)** | https://arxiv.org/abs/2601.04833 |
| **Paper (HTML v1)** | https://arxiv.org/html/2601.04833v1 |
| **Paper (PDF)** | https://arxiv.org/pdf/2601.04833 |
| **DOI** | https://doi.org/10.48550/arxiv.2601.04833 |
| **Trade press (Unite.AI, Jan 26 2026)** | https://www.unite.ai/ai-generated-writing-never-tires-and-thus-reveals-itself/ |
| **alphaXiv replicate CLI** | https://www.alphaxiv.org/replicate/2601.04833 |
| **Fast-DetectGPT (same lab, fusion partner)** | https://github.com/baoguangsheng/fast-detect-gpt |
| **Fast-DetectGPT paper** | https://arxiv.org/abs/2310.05130 |
| **DivEye (TSD baseline)** | https://arxiv.org/abs/2509.18880 |
| **EvoBench (eval set)** | https://arxiv.org/abs/2505.05239 |
| **MAGE (eval set)** | https://arxiv.org/abs/2305.14902 |
| **Guangsheng Bao (co-author homepage)** | https://baoguangsheng.github.io/ |
| **Semantic Scholar entry** | https://www.semanticscholar.org/paper/When-AI-Settles-Down%3A-Late-Stage-Stability-as-a-of-Sun-Bao/29f3d308f712120a5256d9db581708a19904991c |
| **unslop surprisal module** | `unslop/scripts/surprisal.py` |
| **unslop structural module** | `unslop/scripts/structural.py` |
| **unslop detector loop** | `unslop/scripts/detector.py` |
| **Related agent memo (dynamics stack)** | `docs/research/2026-08-detector-research/AGENT-55-SURPRISAL-DYNAMICS-BEYOND-DIVEYE.md` |

**Code status:** No official TSD repository as of Aug 2026. The paper states zero-shot detection with deterministic inference; authors note AI assistants helped with "code refinement" but release no repo link. Implementing TSD is ~20 lines on an existing surprisal tensor. alphaXiv offers a `/reproduce-paper 2601.04833` CLI wrapper — unverified third-party tooling.

---

## Mechanism

### Late-Stage Volatility Decay (LSVD)

Autoregressive generation sharpens the prediction distribution as context grows. Token surprise \(s_t = -\log P(x_t \mid x_{<t})\) becomes less volatile toward the end of AI text. Human writers keep introducing unexpected lexical choices throughout; their surprisal trajectory does not collapse as fast.

The paper analyzes 120k+ samples from EvoBench and MAGE using Llama-3-8B-Instruct (plus GPT-J-6B and Falcon-7B in appendices). Key quantitative findings:

| Metric | EvoBench 2nd-half gap (AI − human) | AI decay rate vs human |
|--------|-------------------------------------|-------------------------|
| \|Δ surprisal\| (derivative) | −32% | 2.4× faster AI decay |
| Local std of surprisal | −31% | 2.6× faster AI decay |
| MAGE (both features) | −24% to −25% | ~1.9× faster AI decay |

Both human and AI volatility fall over the sequence (context constraint). AI falls **much** faster. Discriminability concentrates at normalized positions 50–100%.

### TSD feature definitions

Given text tokens \(t_1 \ldots t_n\), surrogate LM probabilities \(p_i = P(t_i \mid t_{<i})\), surprisal \(s_i = -\log p_i\), and second-half index set \(\mathcal{H}_2 = \{i \mid i > \lfloor n/2 \rfloor\}\):

**Derivative Dispersion (DD):**
\[
d_i = |s_i - s_{i-1}|,\quad \text{DD} = \text{Std}(\{d_i\}_{i \in \mathcal{H}_2})
\]

**Local Volatility (LV):** sliding window \(w=20\),
\[
\ell_i = \text{Std}(s_{i-w/2}, \ldots, s_{i+w/2}),\quad \text{LV} = \text{Mean}(\{\ell_i\}_{i \in \mathcal{H}_2})
\]

**TSD score:**
\[
S_{\text{TSD}} = -(\text{DD} + \text{LV})
\]

Classification: threshold \(\tau\) on validation data. **TSD+** fuses additively with Fast-DetectGPT's global sampling-discrepancy score: \(S_{\text{fusion}} = S_{\text{TSD}} + S_{\text{global}}\).

### Implementation constants (paper)

- Surrogate: **Llama-3-8B-Instruct**
- Max sequence: **512 tokens** (truncated)
- Second-half start: **relative 50%** (not fixed token offset — ablation shows 50% beats 10–90% alternatives)
- LV window: **w = 20 tokens**
- Base metric: **log-probability / surprisal** (entropy, raw probability, top-k concentration near-random as TSD bases)

### How TSD differs from DivEye, burstiness, and perplexity

| Signal | What it measures | Temporal scope | TSD relationship |
|--------|------------------|----------------|------------------|
| **Perplexity / likelihood** | Mean model confidence | Global aggregate | TSD paper: slope ratio ~1.0 for raw token probability — weak temporal signal |
| **Burstiness (Holtzman et al.)** | Sentence/word-length variance, repetition | Surface structure | Orthogonal. `structural.py` targets σ of **sentence lengths** (~8 human vs ~4 GPT-4o). TSD targets σ of **token surprisal derivatives** in the back half. A text can have high sentence-length σ and still show LSVD. |
| **DivEye** | Global distributional + Δ/Δ² surprisal stats | Full sequence | TSD paper lists Diveye at 74.40% EvoBench avg vs TSD 83.36%. DivEye captures "rhythmic diversity" globally; TSD asks whether diversity **decayed too fast** late. Complementary — DivEye ablations show temporal features help, but computed over whole doc. |
| **DetectGPT / Fast-DetectGPT** | Probability curvature / sampling discrepancy | Global (with local sampling) | Fast-DetectGPT strong globally; weaker on GPT-4o in paper. TSD excels on fluent frontier models where global anomalies shrink. TSD+ combines both. |
| **Global surprisal stdev** | Document-wide token surprise spread | Global | Insufficient. TSD ablation: full-sequence TSD **77.00%** vs second-half **83.36%** on EvoBench — late-half conditioning adds **6+ AUROC points**. |

**Conceptual distinction:** Perplexity asks "how surprising on average?" Burstiness asks "how varied is structure?" DivEye asks "how diverse is the surprisal distribution?" TSD asks "did surprisal **stop jumping around** too early in the back half?"

---

## Benchmarks

All numbers from Table 3 (paper §4.2). Metric: **AUROC %**. Surrogate: Llama-3-8B-Instruct. Sequences capped at 512 tokens.

### EvoBench (avg across 7 model families)

| Category | Method | AUROC |
|----------|--------|-------|
| Global | Likelihood | 77.44 |
| Global | Log-Rank (DetectGPT family) | 75.37 |
| Global | **Fast-DetectGPT** | 79.85 |
| Global | LLR (DetectLLM) | 59.86 |
| Temporal | Lastde | 76.66 |
| Temporal | **DivEye** | 74.40 |
| Temporal | FourierGPT | 58.74 |
| Temporal | UCE | 64.57 |
| **Ours** | DD alone | 80.73 |
| **Ours** | LV alone | 83.22 |
| **Ours** | **TSD (DD+LV)** | **83.36** |
| **Ours** | **TSD+ (fusion)** | **85.37** |

Per-source highlights: TSD beats Fast-DetectGPT on **GPT-4o by +9.66 pp** and **GPT-4 by +7.35 pp** — frontier models produce fewer global distributional tells but still exhibit LSVD.

### MAGE (avg across 8 generator families)

| Method | AUROC |
|--------|-------|
| Fast-DetectGPT | 69.69 |
| DivEye | 69.60 |
| Lastde | 70.71 |
| **TSD** | **71.56** |
| **TSD+** | **75.20** |

**Failure modes:** FLAN-T5 (short encoder–decoder outputs): TSD **35.17%** alone; TSD+ recovers to **55.92%** via Fast-DetectGPT. Human-paraphrased AI (Human-Para): TSD+ **72.03%** vs Fast-DetectGPT **61.92%** (+10 pp) — human edits dilute global cues but may leave residual late-stage machine smoothness.

### Position ablation (EvoBench / MAGE)

| Region used | TSD AUROC (Evo) | TSD AUROC (MAGE) |
|-------------|-----------------|------------------|
| First half only | 63.59 | 68.02 |
| Full sequence | 77.00 | 70.49 |
| **Second half only** | **83.36** | **71.56** |

### Length sensitivity

- Pearson **r = 0.54** (EvoBench), **r = 0.66** (MAGE) between avg token length and TSD AUROC.
- **>150 tokens:** TSD typically **>82%** AUROC.
- **<100 tokens:** most sub-70% cases.
- Starting position at **90%** of sequence drops MAGE to **63.01%** — too few tokens for stable estimation.

### GPTZero / commercial detectors

**Not evaluated.** The paper compares zero-shot academic methods only. No GPTZero, Originality.ai, Copyleaks, or Turnitin numbers exist in this work. Any mapping to commercial tools is speculative. TMR (unslop's default detector backbone) is also absent from the TSD evaluation suite.

### Reasoning-model generalization (Appendix E, MIRDGE)

LSVD persists on GPT-4o, Claude 3.7, Gemini 2.0, DeepSeek-V3, etc. **Reasoning models** (DeepSeek-R1, GPT-o3-mini, QwQ-Plus) show **attenuated** decay ratios (1.0–2.3 vs 1.8–3.0 for standard models) and smaller 2nd-half gaps (~13–18% vs ~24–32%). Extended chain-of-thought may mask LSVD.

---

## Debate

### Community reaction

**Sparse.** As of Aug 2026:

- **Unite.AI** (Martin Anderson, Jan 26 2026) — accessible summary of LSVD, DD/LV, benchmark table, fusion with Fast-DetectGPT. Raises editorial-process concern: heavily edited human prose may lose the "eccentricities" TSD keys on. URL above.
- **aispaper.com** — indexer entry; reported ~1 citation early (could not re-fetch; 401 on direct access).
- **HN / Reddit / academic Twitter:** No front-page Hacker News thread specifically for arXiv:2601.04833 found in search. Generic "AI settles down" HN hits refer to industry maturation, not this paper.
- **Peer review:** arXiv preprint only (submitted Jan 8, 2026). No venue acceptance confirmed in public sources.

### Critics and limitations (paper + press)

1. **Length dependency (authors, §Limitations):** TSD needs enough tokens in \(\mathcal{H}_2\) to estimate DD/LV. Very short texts (<100 tokens), tweets, bullet replies — weak signal. unslop often humanizes paragraphs of this size.

2. **Architectural mismatch:** Encoder–decoder (FLAN-T5) breaks the autoregressive-story LSVD assumes. TSD alone near-random on FLAN-T5 (35.17%).

3. **Surrogate sensitivity:** Primary results use Llama-3-8B. Appendices D/E show LSVD persists on GPT-J-6B and Falcon-7B with slightly weaker gaps (−19% to −22% vs −32%). unslop defaults to **distilgpt2** — gap magnitudes untested.

4. **False positives (authors, Appendix F):** "May produce false positives or negatives… should not be the sole basis for consequential decisions." No FPR table at fixed thresholds. ESL and edited institutional prose are plausible FP sources (Unite.AI editorial concern).

5. **Paraphrase robustness — mixed:** Human-Para category favors TSD+ (+10 pp over Fast-DetectGPT). But heavy paraphrase that re-smooths the entire surprisal trajectory could attack both DD and LV. DivEye's RAID paraphrase numbers (~87% AUROC) remain the stronger paraphrase benchmark in the broader literature; TSD has no RAID eval.

6. **Reasoning-model evasion:** Attenuated LSVD on R1/o3-mini/QwQ suggests CoT-heavy outputs may partially evade TSD.

7. **Simple fusion:** TSD+ uses unweighted score addition. No length-adaptive weighting despite known short-text failure.

8. **No code release:** Reproducibility depends on reimplementation. Same lab released Fast-DetectGPT code; TSD may follow later.

---

## Humanization angle

TSD defines a **positional** adversary. To evade LSVD (defensive use only — ESL false positives, resume polish; not academic misconduct):

### What to increase in the second half

1. **Sustained lexical surprise** — concrete nouns, domain terms, or idioms the surrogate LM did not expect given prior context. Not synonym swaps (Adversarial Paraphrasing showed lexical-only rewrites **raise** detector TPR 8–15%).

2. **Higher \|Δ surprisal\| dispersion late** — vary the *rate* of surprise changes in \(\mathcal{H}_2\). Avoid monotonic settling.

3. **Higher local volatility late** — within 20-token windows in the back half, keep surprisal swinging. Short punchy sentences mixed with longer ones help **structural** burstiness; TSD additionally wants **token-level** swing.

4. **Avoid "recovery snap-back"** — after a surprising token, don't immediately revert to predictable glue words (SurpMark's related failure mode; TSD LV captures the same smoothness).

### What not to do

- **Front-load all surprise** — first-half-only features score ~64% AUROC; detectors using full+late fusion still see smooth back halves.
- **Inflate global σ alone** — DivEye global widening ≠ second-half DD/LV increase.
- **Uniform sentence splitting** — `structural.py` `split_long_sentences` helps sentence-length σ but does not touch token surprisal dynamics.
- **Rely on perplexity spikes** — mean perplexity is weak; TSD uses dynamics, not level.

### Practical rewrite heuristics (anti-detector mode extension)

For passages **>150 tokens** (where TSD is strongest):

- Last 40–50%: inject 1–2 concrete specifics, a hedged aside ("I think", "probably"), or a register shift per paragraph.
- Avoid repeating sentence openers in the closing section (reduces LM predictability).
- If using LLM rewrite pass: explicit instruction — *"Keep the ending lexically uneven; don't converge to summary-register smoothness."*

Short texts (<100 tokens): TSD is a weak threat; prioritize TMR/commercial detectors and structural σ instead.

---

## unslop integration

Cross-read against `docs/RESEARCH_AND_TECH.md`, `structural.py`, `surprisal.py`, `detector.py`.

### `structural.py` — Layer 2, surface burstiness

Operates on **sentence-length variance**, not token surprisal:

- `_paragraph_sigma()` — stddev of sentence word counts; flat paragraphs (σ < 5.0) trigger splits at 20-word cutoff.
- Research basis cited: human σ ~8.2, GPT-4o ~4.1.
- **TSD overlap:** Low. Sentence-length rebalancing changes how humans *read* rhythm; TSD reads surrogate-LM token surprise dynamics. Both fight "AI smoothness" on different axes. A structurally varied paragraph can still LSVD-fail if the back half token stream settles.

**Integration note:** Structural pass runs **before** or alongside lexical scrubbing in the pipeline. It does not know about \(\mathcal{H}_2\). Consider a **late-paragraph structural perturbation** pass (split or merge in final 50% only) as a cheap proxy — unproven against TSD, low priority vs surprisal work.

### `surprisal.py` — DivEye measurement, partial TSD overlap

Ships 10-feature DivEye vector via `distilgpt2` (default). Relevant fields:

| Field | TSD analog | Gap |
|-------|-----------|-----|
| `delta_surprisal_stdev` | DD (partial) | Global std of **signed** Δ, not second-half std of **\|Δ\|** |
| (none) | LV | No sliding-window local std |
| (none) | Position split | All stats over full sequence |

`compute_surprisal_variance()` truncates at **1024 tokens**; TSD eval uses **512**. Implementation is a straightforward extension: compute surprisal list, slice `surprisals[n//2:]`, derive DD and LV, return `tsd_score = -(dd + lv)`.

**Not wired today:** `--surprisal-variance` dumps global JSON. Anti-detector SKILL.md mentions "vary surprisal across the document" as prose — not computed or enforced.

### `detector.py` — TMR feedback loop

Default backbone: **TMR RoBERTa** (99.28% AUROC on RAID per `RESEARCH_AND_TECH.md`). Loop:

1. Humanize → `score_ai_probability()` → escalate intensity until below target or ladder exhausts.
2. Optional `surprisal_fn` logs `surprisal_stdev` per iteration — **not a stop criterion**.

**TSD gap:** TMR and TSD measure different things. Optimizing TMR does not monotonically optimize TSD (or vice versa). A dual-oracle loop — TMR for commercial proxy, TSD for temporal dynamics — would match the 2026 detector stack direction (see Agent #55).

### `RESEARCH_AND_TECH.md` status

TSD is **not** in the "live citations" table (papers encoded in shipping code). DivEye is (surprisal.py). Adding TSD requires either implementing `compute_tsd()` or documenting as decorative until shipped.

---

## P0 / P1 / P2 actions

### P0 — Measure before optimizing

1. **Implement `compute_tsd()` in `surprisal.py`** (or sibling `tsd.py`) — DD + LV on second half, default w=20, return `{dd, lv, tsd_score, half_token_count}`.
2. **Benchmark hook** — extend `benchmarks/diveye_comparison/` or new `benchmarks/tsd_probe/` — before/after unslop on 9-fixture suite; report TSD score delta per mode (`balanced`, `full`, `anti-detector`).
3. **Correlate TSD vs TMR** on same texts — if uncorrelated, dual-oracle rationale is confirmed.

### P1 — Close the humanization gap

4. **Anti-detector late-half prompt block** — LLM mode instruction for final 50%: sustained lexical unevenness, no summary-register convergence. Gate on `token_count > 150`.
5. **Optional TSD telemetry in `detector.feedback_loop()`** — log `tsd_score` alongside `surprisal_stdev`; still not sole stop criterion (Nicks et al. warning stands).
6. **Document in `RESEARCH_AND_TECH.md`** — add TSD row to live or decorative table once code lands.

### P2 — Research / eval depth

7. **distilgpt2 vs Llama-3-8B TSD calibration** — paper surrogate ≠ unslop default; quantify rank-order preservation.
8. **Short-text policy** — explicit skip/warn when `token_count < 100` for TSD-based advice.
9. **RAID / paraphrase eval** — TSD paper lacks this; run TSD probe on unslop's existing adversarial paraphrasing comparison fixtures.
10. **Watch for official code** from baoguangsheng — same lab shipped Fast-DetectGPT within months of paper.

---

## Open questions

1. **Does unslop's deterministic path increase or decrease second-half DD/LV?** Lexical scrubbing may smooth surprisal; structural splits may fragment it. Empirical only.

2. **Is sentence-length σ a useful proxy for LV?** Both measure "variance," different domains. Correlation on unslop fixture suite unknown.

3. **Human-edited AI (Human-Para):** TSD+ beats Fast-DetectGPT — does humanization that mimics heavy editing leave residual LSVD? Implication for "voice-match" vs "anti-detector."

4. **Cross-model paraphrase (TempParaphraser, Adversarial Paraphrasing):** Recommended at detector-ladder exhaustion — do they restore late-half volatility or just shift global curvature?

5. **Reasoning traces:** If `--strip-reasoning` removes CoT, does remaining prose still LSVD-fail? Relevant for agent output humanization.

6. **Commercial detector adoption:** Will GPTZero/Turnitin ship TSD-like features in 2026? Turnitin Feb 2026 retrain already targets bypassers; no public LSVD confirmation.

7. **Threshold calibration:** Paper uses validation-set τ. What τ gives 1% FPR on ESL essays (Liang et al. TOEFL cohort)? Unknown — critical for defensive framing.

8. **Fusion with DivEye features:** TSD paper fuses with Fast-DetectGPT only. DivEye + TSD XGBoost stack unexplored in either paper.

---

## Authors and lineage

| Author | Affiliation | Notes |
|--------|-------------|-------|
| **Ke Sun** | Visiting student, Westlake University | Lead; LSVD analysis |
| **Guangsheng Bao** | Westlake → Fuyao Univ. of Science and Technology | Fast-DetectGPT, Glimpse co-author |
| **Han Cui** | Westlake University | |
| **Yue Zhang** | Westlake University (corresponding) | MAGE benchmark co-author |

Institution: **School of Engineering, Westlake University, Hangzhou, China**. Submitted **2026-01-08**. Same research lineage as Fast-DetectGPT (ICLR 2024) and MAGE (ACL 2024) — TSD is the temporal complement to Bao et al.'s global curvature work.

**Citations:** Early — preprint age ~7 months at research time. Semantic Scholar entry exists; independent replication count low.

---

*Agent #02 complete. Cross-reference: Agent #55 (dynamics stack), Agent #34 (DivEye implementation), Agent #50 (perplexity/fidelity).*
