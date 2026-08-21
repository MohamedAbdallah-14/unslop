# Agent #16 — SHIELD (Hardness-Aware Detection Benchmark)

**Focus:** Evaluation framework, humanification hardness ladder, URSS metrics, field debate, unslop bench integration — not a detector method.  
**Date:** 2026-08-19  
**Authors (paper):** Navid Ayoobi, Sadat Shahriar, Arjun Mukherjee (University of Houston)

---

## 1. Executive summary

- **SHIELD** (*Beyond Easy Wins: A Text Hardness-Aware Benchmark for LLM-generated Text Detection*, [arXiv:2507.15286](https://arxiv.org/abs/2507.15286), **Jul 2025**) is an **evaluation benchmark**, not a detector. It argues that flat **AUROC** overstates real-world detector quality by overweighting easy samples and ignoring **threshold stability** across domains/generators.

- The benchmark ships three things: (1) a **700k-sample corpus** (87.5k human + 612.5k LLM paraphrases across 7 domains × 7 open models), (2) a **post-hoc humanification framework** with graded hardness knobs, and (3) a unified metric **URSS** (Unified Reliability-Stability Score) combining low-FPR-weighted AUROC (**W-AUROC**) with cross-scenario threshold stability (**SFD**).

- **Headline finding:** SOTA **zero-shot** detectors (Binoculars, Fast-DetectGPT, GLTR-class rank/log-likelihood methods) lose **~80% URSS on average** under even **Random Meaning-Preserving Mutation (RMM)** — random word swaps via MLM that approximate casual human editing. Targeted **AI-flagged word swap (AWS)** and **recursive humanification loop (RHL)** degrade them further. **Supervised RADAR** *improves* under humanification (paraphrase-robust by design).

- **AUROC vs URSS:** Identical AUROC can mask practical differences. Example from paper: on Reddit, **RADAR** has much higher AUROC than **Rank**, but **identical URSS** — practical equivalence at deployment FPR. Conversely, **Binoculars** can top AUROC yet rank last on URSS in a domain when **SFD** collapses (threshold instability).

- **Community footprint is thin** (Aug 2026): ~2 GitHub stars, no dedicated HN/Reddit threads, no venue acceptance yet (arXiv preprint only). Academic uptake is **indirect** — cited in the broader "AUROC is misleading" wave alongside TH-Bench, RAID, and *Why AI Detection Fails* (arXiv:2603.23146). No humanizer repo reports SHIELD-stratified results.

- **unslop implication:** SHIELD is the **evaluation harness unslop lacks**. Current `benchmark.py` tracks AI-ism/word-count deltas only; `detector.py` optimizes TMR probability, not W-AUROC/URSS at fixed FPR. Adopting hardness-stratified reporting would expose whether `/unslop anti-detector` wins on easy paraphrases but fails at AWS/RHL-equivalent hardness — the gap between marketing claims and deployment reality.

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| arXiv preprint | https://arxiv.org/abs/2507.15286 | v1 submitted 2025-07-21 |
| arXiv HTML | https://arxiv.org/html/2507.15286v1 | Full paper with tables/figures |
| DOI | https://doi.org/10.48550/arXiv.2507.15286 | |
| GitHub (data + code) | https://github.com/navid-aub/SHIELD-Benchmark | ~2 stars Aug 2026; sparse README |
| Lattice summary | https://www.layerthelatestinalattice.com/papers/c1189d5776adae833529ff0475970671d4770e41 | Third-party digest |
| Prior work (same lab) — ESPERANTO | https://arxiv.org/abs/2409.14285 | Ayoobi et al. 2024; back-translation evasion; different attack axis |
| TH-Bench (complementary) | https://arxiv.org/abs/2503.08708 | Humanizer × detector Pareto; SHIELD adds hardness as 4th axis |
| RAID (baseline corpus culture) | https://aclanthology.org/2024.acl-long.674/ | Dugan et al., ACL 2024 |
| Why AI Detection Fails | https://arxiv.org/abs/2603.23146 | Cross-domain failure analysis; aligns with SHIELD's AUROC skepticism |
| unslop benchmark | `unslop/scripts/benchmark.py` | AI-ism delta only; no hardness tiers |
| unslop detector loop | `unslop/scripts/detector.py` | TMR probability; no URSS/FPR calibration |
| Internal index | `docs/research/15-academic-papers-llm-humanization/A-academic.md` §2.0b | Already indexed Apr 2026 |
| Agent manifest | `docs/research/2026-08-detector-research/AGENT-MANIFEST-100.md` | Slot #16 |

---

## 3. Mechanism — how SHIELD works

SHIELD is **Scalable Hardness Informed Evaluation of LLM Detectors**. Three subsystems:

```
┌─────────────────────────────────────────────────────────────────┐
│  3.1 DATA CREATION                                              │
│  7 domains × 7 LLMs → paraphrased AI text + pre-2021 human refs │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  3.2 HUMANIFICATION (hardness ladder)                           │
│  RMM (random MLM swap) │ AWS (MI-targeted swap) │ RHL (recursive)│
│  knob: p% words      │ knob: p% AI-flagged   │ knob: R rounds  │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  3.3 EVALUATION METRICS                                         │
│  W-AUROC (low-FPR weighted) × SFD (threshold stability) = URSS │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 Dataset construction

| Property | Value |
|----------|-------|
| Human samples | **87.5k** (12.5k per domain) |
| LLM samples (pre-humanification) | **612.5k** (7 models × 7 domains × ~12.5k) |
| Domains (7) | Medium, News, Amazon reviews, Reddit ELI5, arXiv abstracts, pink slime journalism, Wikipedia |
| Generators (7) | Llama3.2-1b/3b, Llama3.1-8b, Mistral-7b, Qwen-7b (DeepSeek-R1-Distill), Gemma2-2b/9b |
| Human text cutoff | **Pre-2021** — excludes LLM-era contamination |
| Generation task | Each LLM **paraphrases** a human document in-domain voice (~matched word count) |
| MLM for humanification | **Longformer-base-4096** (Allen AI) |

SHIELD claims to be the **first** benchmark with (a) structured **hardness gradients** and (b) **fairness-oriented** deployment metrics — see Table 1 comparison vs RAID, MAGE, HC3, M4GT-Bench, DetectRL, etc.

### 3.2 Hardness-aware humanification

Core hypothesis: replace words that **strongly indicate AI authorship** with words characteristic of human writing, preserving semantics.

**Step 0 — Word-MI ranker:** For each word \(w_i\), compute mutual information with authorship label:

\[
MI_i = \sum_x P(x, w_i) \log \frac{P(x \mid w_i)}{P(x)}
\]

Build vocab subsets: **A** (AI-associated) and **H** (human-associated) from corpus frequencies.

**Three strategies (Figure 1):**

| Strategy | Mechanism | Hardness knob | Targets |
|----------|-----------|---------------|---------|
| **RMM** (Random Meaning-Preserving Mutation) | Random non-stopword subset → `<mask>` → MLM top-1 replacement (must differ) | **p%** of non-stopwords (10–100%) | Simulates naive user edits without MI knowledge |
| **AWS** (AI-flagged Word Swap) | Top **p%** words by \(MI_A\) → mask → replace with highest \(MI_H\) among MLM candidates | **p%** (10–100%) | Targets detector-exploitable AI tokens |
| **RHL** (Recursive Humanification Loop) | Repeat AWS with fixed **p₀=10%** for **R** rounds | **R** rounds (5–40) | Progressive hardness; each round re-scores remaining AI-flagged words |

**Hardness onset (Figure 3):** Meaningful degradation begins at **R≈15** (RHL), **p≈60%** (AWS), **p≈80%** (RMM). AWS/RHL hit harder than RMM at equal knob values because swaps are MI-targeted (high-entropy AI → high-entropy human words).

### 3.3 Fairness-oriented metrics

**Problem with AUROC:** Uniformly weights entire ROC curve including impractical high-FPR regions; hides threshold instability when deployed with a fixed cutoff.

**W-AUROC** — exponential weight on low FPR:

\[
W\text{-AUROC} = \mathbb{E}_{t \sim p(t)}[\text{TPR}(t)], \quad p(t) = \frac{1}{Z}\exp(-kt), \quad k = 20\ln 2
\]

Calibrated so weight decays to 50% at **FPR=0.05** (aligns with TPR@FPR≤5% reporting norm).

**SFD** (Stability under FPR Deviation) — per-scenario Youden threshold \(t^*_i = \arg\max_t [\text{TPR}_i(t) - \text{FPR}_i(t)]\); compute \(\sigma_{\text{FPR}}\) across scenarios; then:

\[
\text{SFD} = \exp(-\lambda \cdot \sigma_{\text{FPR}}), \quad \lambda = 10\ln 2
\]

(SFD=0.5 when \(\sigma_{\text{FPR}}=0.1\).)

**URSS** — non-compensatory product:

\[
\text{URSS} = \left(\frac{1}{M}\sum_i W\text{-AUROC}_i\right) \cdot \text{SFD}
\]

High W-AUROC cannot mask poor stability, and vice versa. *(Note: conclusion §5 typo says "USRR"; equations/tables use URSS.)*

---

## 4. Results — headline numbers

### 4.1 AUROC is not enough (§4.1, Figure 2)

On **un-humanified** paraphrased AI text across 7 writing styles:

- **Binoculars** often leads AUROC but can rank **last on URSS** (e.g., Reddit) due to catastrophic **SFD** despite strong discrimination.
- **RADAR vs Rank** on Reddit: large AUROC gap → **identical URSS** (practical tie).
- **Binoculars vs Fast-DetectGPT** on News/Wikipedia/Medium/Reviews: similar AUROC, divergent W-AUROC and SFD — URSS separates them.

**Takeaway:** Leaderboard AUROC picks can be wrong for deployment.

### 4.2 Humanification effectiveness (Table 2, §4.2)

Largest model per family (Gemma2-9b, Llama3.1-8b, Mistral-7b, Qwen-7b); metrics averaged across writing styles; values as **percentages**.

**Baseline (paraphrase only, no humanification) — sample URSS:**

| Detector | Gemma2-9b URSS | Llama3.1-8b URSS | Mistral-7b URSS | Qwen-7b URSS |
|----------|----------------|------------------|-----------------|--------------|
| Binoculars | 32.9 | 40.9 | 27.4 | 14.9 |
| Fast-DetectGPT | 45.3 | 48.6 | 38.6 | **61.8** |
| Log-Likelihood | 11.8 | 15.1 | 3.8 | 7.7 |
| LRR | 19.9 | 25.0 | 2.3 | 4.8 |
| RADAR (supervised) | 6.0 | 6.3 | 4.0 | 10.7 |

**Average URSS degradation under humanification (zero-shot detectors, paper §4.2):**

| Strategy | Binoculars | Fast-DetectGPT | Log-Likelihood | Log-Rank | LRR | Rank |
|----------|------------|----------------|----------------|----------|-----|------|
| RMM | −41% | −27% | −97% | −96% | −92% | −95% |
| AWS | −27% | −66% | −98% | −98% | −98% | −95% |
| RHL | −38% | −65% | −99% | −99% | −97% | −97% |

**RMM surprise:** Simple random swaps can match AWS/RHL damage for several detectors — "natural editing" is enough to break token-statistic detectors.

**RADAR inversion:** Supervised RADAR **gains** W-AUROC and SFD under humanification → URSS **increases**. Humanification makes AI text *more* detectable to paraphrase-hardened supervised models (likely because swaps expose artifacts RADAR learned).

**Extreme collapse examples (URSS → ~0):**

- Log-Likelihood under RMM on Mistral-7b: **0.1%** URSS (baseline 3.8%).
- Log-Rank under AWS on Gemma2-9b: **0.1%** URSS.
- Rank under RHL: consistently **≤0.4%** URSS across generators.

**Generator dependency:** Same attack, different URSS by source LLM — reinforces RAID-style "detector overfits to generator fingerprint" problem.

### 4.3 Hardness knob curves (Figure 3)

- All metrics (W-AUROC, SFD, URSS) fall **below baseline** at every tested knob value — ladder is monotonically adversarial.
- **Paradox at high hardness:** Some detectors show **rising SFD** when text becomes very human-like — thresholds converge because signal vanishes. URSS still penalizes because W-AUROC collapses. "Stable but useless."

### 4.4 Detectors evaluated

| Detector | Type | SHIELD role |
|----------|------|-------------|
| Binoculars | Zero-shot cross-perplexity | Primary SOTA zero-shot target |
| Fast-DetectGPT | Zero-shot curvature | Often beats Binoculars on URSS in some domains |
| Log-Likelihood, Log-Rank, Rank, LRR | GLTR-class statistics | Collapse hardest under humanification |
| RADAR | Supervised adversarial | Control — improves under attack |

**Not evaluated:** DivEye, GPTZero, commercial APIs, ChatGPT/Claude generations, fine-tuned RAID successors (TMR, Desklib).

---

## 5. Community & academic debate

### 5.1 Supporters / aligned literature

| Source | Position |
|--------|----------|
| **unslop Cat 15 synthesis** (`docs/research/15-academic-papers-llm-humanization/SYNTHESIS.md`) | SHIELD adds **4th evaluation axis** (hardness) atop TH-Bench's evasion × quality × compute |
| **TH-Bench culture** (Liu et al., arXiv:2503.08708) | Single-number wins discounted; multi-axis Pareto is norm |
| **Why AI Detection Fails** (Pudasaini et al., arXiv:2603.23146) | In-domain AUROC misleading; SHIELD's low-FPR weighting addresses same failure mode from metric side |
| **Agent #10 (LLM-DetectAIve memo)** | Cites SHIELD as evidence that TPR@FPR=1% reporting is under-standardized |
| **Lattice / BibSonomy indexing** | Paper discoverable; no critique |

Authors' ethical stance (§Ethical considerations): framework is for **detector validation**, explicitly **not** for circumvention — standard dual-use disclaimer.

### 5.2 Critics / limitations / open questions

| Concern | Detail |
|---------|--------|
| **No peer review yet** | arXiv-only Jul 2025; citation count still ~0 at fetch time |
| **Minimal code adoption** | GitHub ~2 stars, 0 forks; no known replications or leaderboard |
| **English-only** | Authors acknowledge in Limitations; no multilingual hardness ladder |
| **No closed-source LLMs** | Budget constraint; ChatGPT/Claude/GPT-4 excluded — largest deployment gap |
| **Humanification ≠ modern humanizers** | Word-level MLM swaps, not DIPPER/LLM rewrite/StealthRL — may **understate** evasion vs commercial tools OR **overstate** vs prose-level humanization |
| **RADAR anomaly unexplored** | Supervised gain under attack noted but not generalized — may not hold for TMR/Desklib |
| **URSS parameter choices** | k=20ln2, λ=10ln2 are author-calibrated; sensitivity analysis limited |
| **Human text pre-2021** | Domain drift vs 2025 writing styles; pink slime includes 2021 partisan content |
| **No DivEye-era detectors** | Paper predates DivEye TMLR 2026; surprisal-variance methods untested on SHIELD ladder |
| **Industry lag** | Cat 15 B-industry.md: commercial blogs still cite flat AUROC |

### 5.3 SHIELD vs TH-Bench vs RAID — evaluation stack map

| Framework | Primary question | Axes | Humanification |
|-----------|------------------|------|----------------|
| **RAID** | Robustness to decoding + attacks | Domain × generator × attack | 11 adversarial attacks (homoglyph, paraphrase, etc.) |
| **TH-Bench** | Humanizer Pareto | Evasion × quality × compute | 6 SOTA humanizer attacks |
| **SHIELD** | Deployment-fair detector ranking | Reliability (W-AUROC) × stability (SFD) × **hardness tier** | 3 post-hoc word-swap strategies with knobs |

**Complementary, not redundant.** unslop should treat SHIELD as the **metric layer** TH-Bench lacks, not a replacement for TH-Bench's humanizer quality scoring.

### 5.4 Relation to ESPERANTO (same first author)

Ayoobi et al. **ESPERANTO** (arXiv:2409.14285, 2024) — back-translation evasion for AI detection. SHIELD generalizes the lab's theme: **structured adversarial evaluation** rather than single-shot attacks. Different mechanism (translation loop vs MI word swap).

---

## 6. Humanization angle — what SHIELD teaches evaders and defenders

SHIELD's humanification is **word-level**, targeting token-statistic detectors (perplexity, rank, log-likelihood). Implications:

### 6.1 What breaks detectors (per SHIELD)

1. **Random edits (RMM)** — enough for ~40% URSS drop on Binoculars; no MI oracle needed.
2. **Targeted AI-token replacement (AWS)** — swaps words with highest AI MI score; harder at p≥60%.
3. **Iterative refinement (RHL)** — compounding; R≥15 is the knee.

### 6.2 What does *not* match unslop's approach

| SHIELD strategy | unslop equivalent | Gap |
|-----------------|-------------------|-----|
| RMM | Casual user edits / typo passes | unslop doesn't do random MLM word swap |
| AWS | Stock-vocab stripping (`humanize.py`) | unslop targets phrases, not per-token MI |
| RHL | Multi-pass `anti-detector` loop | unslop rewrites prose holistically via LLM |

unslop's LLM rewrite may achieve **harder** evasion (semantic coherence preserved) or **easier** detection (rewrite introduces new AI fingerprint) — **unknown without SHIELD-stratified measurement**.

### 6.3 Defensive use (ESL false positives, voice restoration)

SHIELD supports the unslop Boundaries case: if human text survives AWS at low p but AI text doesn't, detectors with high AUROC but low URSS are **unsafe for academic integrity** (FPR instability). Document this when users ask about detector trust.

---

## 7. unslop integration plan

Current state:

| Component | Today | SHIELD gap |
|-----------|-------|------------|
| `benchmark.py` | AI-ism count + word delta per file | No detector scores; no hardness tiers; no URSS |
| `detector.py` | TMR probability loop; optional `surprisal_stdev` log | Optimizes P(AI), not TPR@FPR=5% or URSS |
| `humanize.py` anti-detector | LLM prose rewrite + structural passes | No calibration against SHIELD hardness ladder |
| `evals/` / `benchmarks/` | DivEye bit-match, sample corpora | No SHIELD subset |
| Docs | Indexed in Cat 15 A-academic §2.0b | No implementation trace |

### 7.1 Evaluation harness (P0)

1. **Add `evals/shield/`** — download SHIELD-Benchmark subset (or reproduce RMM at p=10/40/80 on unslop fixture corpus).
2. **Implement URSS calculator** — standalone module `unslop/scripts/shield_metrics.py`:
   - Input: list of (score, label) per scenario
   - Output: W-AUROC, SFD, URSS per paper Eqs. 10–13
   - No torch dependency for metric math
3. **Report hardness-stratified table** in benchmark output:

   ```
   | hardness | TMR P(AI) mean | TPR@FPR=5% | W-AUROC | URSS |
   | baseline | ...            | ...        | ...     | ...  |
   | RMM p=40 | ...            | ...        | ...     | ...  |
   ```

### 7.2 Anti-detector calibration (P1)

- Run `/unslop anti-detector` on SHIELD paraphrase baselines at each hardness tier.
- Compare against SHIELD's published Binoculars/Fast-DetectGPT URSS drops — establishes unslop's **relative position** on the ladder.
- **Do not ship SHIELD AWS/RHL as evasion tools** — use for defensive eval only (matches paper ethics + unslop Boundaries).

### 7.3 Detector feedback loop (P1)

- Extend `detector.feedback_loop()` to log **TPR@FPR=5%-equivalent threshold** if score distribution allows calibration on a small labeled dev set.
- URSS requires multi-scenario evaluation — loop per-iteration URSS is meaningless; use **held-out scenario bundle** instead.

### 7.4 Docs & claims hygiene (P0)

- README benchmark numbers: if citing detection evasion, add footnote that flat AUROC is insufficient per SHIELD.
- Cross-link Agent #16 in `docs/research/15-academic-papers-llm-humanization/SYNTHESIS.md` action item #14 (hardness-stratified humanizer reporting).

### 7.5 Stretch (P2)

- **Synthetic RMM pass** for stress-testing only: optional `--shield-rmm p=0.2` in benchmark CLI using local MLM (Longformer) — heavy dep, off by default.
- Joint reporting with **TH-Bench** axes: evasion URSS@hardness × AI-ism residual × latency.
- Track DivEye + TMR ensemble URSS on SHIELD — tests whether surprisal-variance survives word-swap ladder better than perplexity methods (hypothesis: partial survival at low p, collapse at RHL R≥15).

---

## 8. Recommended actions

### P0 (do now)

1. **Create `shield_metrics.py`** with W-AUROC, SFD, URSS — pure numpy/scipy.
2. **Add SHIELD fixture eval** under `evals/shield/` using existing `benchmarks/` samples + TMR scoring.
3. **Document** in research memo index that unslop reports AI-ism delta but **not yet** hardness-stratified detector URSS.

### P1 (next sprint)

4. Run one-time **anti-detector vs baseline** URSS comparison on 50-sample fixture; publish in `benchmarks/results/shield_comparison.md`.
5. Add **TPR@FPR=5%** to detector benchmark output alongside raw P(AI).
6. Update `AGENT-MANIFEST-100.md` slot #16 → **complete**.

### P2 (backlog)

7. Full SHIELD corpus integration (700k samples — storage + compute budget).
8. Cross-benchmark dashboard: RAID subset + SHIELD hardness tiers + DivEye features.
9. Monitor for **venue acceptance** (ACL/EMNLP/NeurIPS D&B track) and citation uptake.

---

## 9. Key citations

```bibtex
@article{ayoobi2025shield,
  title={Beyond Easy Wins: A Text Hardness-Aware Benchmark for {LLM}-generated Text Detection},
  author={Ayoobi, Navid and Shahriar, Sadat and Mukherjee, Arjun},
  journal={arXiv preprint arXiv:2507.15286},
  year={2025},
  url={https://arxiv.org/abs/2507.15286}
}
```

Related:

- Liu et al., TH-Bench — arXiv:2503.08708  
- Dugan et al., RAID — ACL 2024  
- Pudasaini et al., Why AI Detection Fails — arXiv:2603.23146  
- Ayoobi et al., ESPERANTO — arXiv:2409.14285  

---

*Research conducted 2026-08-19 via arXiv HTML v1, GitHub repo inspection, unslop codebase audit (`benchmark.py`, `detector.py`, `humanize.py`), and cross-reference with unslop Cat 15 research compendium.*
