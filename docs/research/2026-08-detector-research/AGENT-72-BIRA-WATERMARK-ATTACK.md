# Agent #72 — BIRA Bias-Inversion Watermark Attack

**Topic:** Query-free LLM watermark evasion via negative logit bias on high-surprisal tokens  
**Paper:** Hwang, Park & Ok, *LLM Watermark Evasion via Bias Inversion*  
**Venue:** ICML 2026 poster · arXiv:2509.23019 (v4, Sep 2025)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Hwang et al. (POSTECH) introduce **BIRA** (Bias-Inversion Rewriting Attack): a **query-free**, **scheme-agnostic** watermark remover that paraphrases watermarked text while applying a **negative logit bias** to a proxy set of high-surprisal tokens. Watermarking embeds signal by biasing generation toward "green" tokens; BIRA inverts that bias during rewrite — without knowing the secret key, green list, or watermark algorithm.

Three numbers define the threat model:

| Metric | Vanilla paraphrase | SIRA (prior SOTA query-free) | BIRA (Llama-3.1-8B) |
|--------|-------------------|------------------------------|---------------------|
| **Average ASR across 7 schemes** | ~49–74% (model-dependent) | ~72–99% | **>99%** on all three rewriter LMs |
| **SIR watermark ASR (GPT-4o-mini)** | 23.6% | 57.6% | **99.4%** |
| **Long-text TPR @ FPR=1% (600 tok, SIR)** | — | 20.8% | **4.0%** (LLM judge 4.14 vs SIRA 1.33) |

The theoretical hook: if a rewriter keeps the average conditional probability of sampling green tokens **δ below the detector threshold**, detection probability decays as **exp(−Nδ²/2)** (Theorem 4.2). BIRA operationalizes this with surprisal-ranked token suppression — the same distributional lever unslop's rewrite passes touch incidentally, but BIRA targets it **deliberately**.

**unslop verdict:** BIRA is the strongest published proof that **effective humanization and watermark stripping are structurally coupled**. unslop must **document the side effect**, **refuse deliberate removal**, and **never ship BIRA-style negative logit guidance**. Cross-ref Agent #20 (WaterPark), #31 (DIPPER), #71 (SIRA), #12 (DAMAGE SynthID table), and `skills/unslop/SKILL.md` Boundaries.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv abstract + PDF)** | https://arxiv.org/abs/2509.23019 |
| **Paper (HTML v4)** | https://arxiv.org/html/2509.23019v4 |
| **OpenReview** | https://openreview.net/forum?id=dZY5t9ZrUB |
| **ICML 2026 poster** | https://icml.cc/virtual/2026/poster/61021 |
| **Project page** | https://oppurity12.github.io/project_pages/bira/ |
| **Official code** | https://github.com/ml-postech/LLM-Watermark-Evasion-via-Bias-Inversion |
| **HuggingFace Papers** | https://huggingface.co/papers/2509.23019 |

### Watermark schemes evaluated (MarkLLM toolkit)

| Scheme | Original paper | Relation to BIRA |
|--------|----------------|------------------|
| **KGW** | Kirchenbauer et al. 2023 | Green-red list + positive γ bias; canonical baseline |
| **Unigram** | Zhao et al. 2023 | Fixed green fraction per token |
| **UPV** | Liu et al. 2023a | Publicly verifiable watermark |
| **EWD** | Lu et al. 2024 | Entropy-based detection |
| **DIP** | Wu et al. 2023 | Distribution-preserving watermark |
| **SIR** | Liu et al. 2024 | Semantic invariant robust — strongest pre-BIRA baseline |
| **EXP** | Aaronson & Kirchner 2022 | Sampling-based (non green-red) — BIRA still effective |

Appendix E.2 also tests **sentence-level** watermarks (SemStamp, SimMark, PMark) and localized detectors — BIRA remains effective via sentence merge/split during document paraphrase.

### Lineage and adjacent attacks

| Paper | arXiv | Relation |
|-------|-------|----------|
| **SIRA** (Self-Information Rewrite Attack) | [2505.05190](https://arxiv.org/abs/2505.05190) | Direct predecessor: masks high-entropy tokens, refills; BIRA replaces mask-and-refill with negative bias; shared MarkLLM eval infra |
| **DIPPER** (Krishna et al.) | [2303.13408](https://arxiv.org/abs/2303.13408) | Trained paraphraser baseline; DAMAGE SynthID 66.5% → 1.5% TPR |
| **DAMAGE** (Masrour et al.) | [2501.03437](https://arxiv.org/abs/2501.03437) | Commercial humanizer audit; Table 2 watermark removal |
| **WaterPark** (EMNLP 2025) | [2505.07940](https://arxiv.org/abs/2405.07940) | Unified robustness benchmark; DP-40 paraphrase cuts SynthID TPR to ~0.498 |
| **Jovanović watermark stealing** | [2402.19361](https://arxiv.org/abs/2402.19361) | Query-based ($50); different threat model |
| **SynGuard** (SynthID hardening) | [2508.20228](https://arxiv.org/abs/2508.20228) | Partial defense response; hybrid semantic + token marking |

---

## Mechanism: bias inversion on surprisal proxy set

### Threat model

- **Black-box:** adversary has watermarked text only — no access to watermark key, generator model, or scheme parameters.
- **Query-free:** no repeated API calls to the watermarked LLM (unlike Jovanović stealing or De-mark).
- **Objective:** produce rewritten text $\tilde{y}$ with $\mathcal{D}(\tilde{y}) = 0$ (undetected) while $\mathrm{sim}(\tilde{y}, \hat{y}) \geq \epsilon$.

### Theoretical core (Section 4.1)

For detectors whose statistic is a nondecreasing function of empirical green-token rate $\hat{p}$:

1. **Lemma 4.1:** Detection reduces to thresholding $\hat{p}(y) \geq p_\tau$.
2. **Theorem 4.2:** If the rewriter keeps average conditional green probability $\leq p_\tau - \delta$ across $N$ tokens, then  
   $\Pr[\mathcal{D}(\tilde{y}) = 1] \leq \exp(-N\delta^2/2)$.

**KGW numeric example (paper defaults):** $p_0 = 0.5$, $\tau = 4$, $N = 230$ → $p_\tau \approx 0.632$. Margin $\delta = 0.1$ → detection bound ≈ 0.316; $\delta = 0.2$ → ≈ 0.010.

Key insight: **perfect green-list identification is unnecessary** — consistent per-step suppression suffices.

### Algorithm (BIRA, Algorithm 1)

```
Phase 1 — Proxy suppression set Ĝ:
  For each token ŷ⁽ⁿ⁾ in watermarked input:
    I⁽ⁿ⁾ ← −log P_M(ŷ⁽ⁿ⁾ | ŷ⁰:ⁿ⁻¹)   # self-information under public LM M
  η ← q-th percentile of {I⁽ⁿ⁾}
  Ĝ ← { id(ŷ⁽ⁿ⁾) : I⁽ⁿ⁾ ≥ η }

Phase 2 — Bias-inversion rewrite:
  β ← β₀ < 0
  Autoregressively paraphrase with system prompt S:
    logits l ← M(ỹ_so_far, ŷ_full, S)
    l_u ← l_u + β · 1{u ∈ Ĝ}   for all u ∈ V
    sample next token from softmax(l)
  If distinct-1-gram ratio in last h tokens < ρ:
    β ← min(0, β + lr); restart   # adaptive anti-degeneration
  Return ỹ
```

**Design choices:**

| Parameter | Default | Role |
|-----------|---------|------|
| $q$ (percentile) | 0.5 | Top half of surprisal tokens enter $\widehat{\mathcal{G}}$ |
| $\beta_0$ | −4 (Llama-3.1), −11 (GPT-4o-mini) | Initial negative bias; calibrated on 50 C4 paraphrases |
| $\mathrm{lr}$ | 0.125 | Degeneration recovery step |
| $\rho$ | window distinct-1 threshold | Detects repetitive collapse |

**Why surprisal works:** Watermarks concentrate bias on **high-entropy positions** (SIRA observation). Low-entropy tokens (function words, code) carry less signal; suppressing them degrades quality without helping evasion.

**Relation to watermark embedding:** Generation adds **+γ** to green logits; BIRA adds **β < 0** to proxy "likely-watermarked" token types during rewrite — literal bias inversion (Figure 1).

---

## Headline results

### Table 1 — Attack Success Rate (ASR) by scheme and rewriter

ASR = fraction of attacked watermarked texts classified as **non-watermarked**.

| Attack | KGW | Unigram | UPV | EWD | DIP | SIR | EXP |
|--------|-----|---------|-----|-----|-----|-----|-----|
| Vanilla (Llama-3.1-8B) | 88.8% | 73.4% | 73.4% | 92.6% | 99.8% | 54.0% | 80.6% |
| SIRA (Llama-3.1-8B) | 98.8% | 95.0% | 87.6% | 99.8% | 99.6% | 72.8% | 95.2% |
| **BIRA (Llama-3.1-8B)** | **99.8%** | **99.4%** | **99.8%** | **100.0%** | **100.0%** | **99.6%** | **99.8%** |
| **BIRA (GPT-4o-mini)** | **99.4%** | **100.0%** | **100.0%** | **99.8%** | **99.8%** | **99.4%** | **98.2%** |

Setup: 500 C4 prompts → 230-token watermarked text from OPT-1.3B; seven MarkLLM schemes; thresholds calibrated on 500 human + 500 attacked texts at FPR 1% and 10%.

**Largest gain vs prior art:** SIR on GPT-4o-mini — vanilla 23.6% → SIRA 57.6% → **BIRA 99.4%**.

### Detector-calibrated metrics (Figure 2)

At FPR = 1% and 10%, BIRA yields the **lowest TPR and best F1** across all seven schemes — attacked text is statistically indistinguishable from human writing under standard z-test detectors.

### Semantic fidelity (Figure 3)

| Attack | LLM judgment (↑) | Self-BLEU (↓) | Notes |
|--------|------------------|---------------|-------|
| Vanilla | Highest (~4.76 at β=0) | Highest (~0.25) | Weak paraphrase → low ASR |
| DIPPER-2 | Mid | Low | Strong paraphrase, meaning drift |
| SIRA | Low on long text (1.33 @ 600 tok) | Low | Masking disrupts context |
| **BIRA** | **~4.24 @ β=−4** | **~0.07** | Best fidelity among high-ASR attacks |

Qualitative example (KGW): z-score **6.03 → 0.83** after BIRA (Llama-3.1-8B) with preserved factual content (names, numbers, structure).

### z-score suppression (Table 4)

| Watermark | Vanilla | SIRA | **BIRA** |
|-----------|---------|------|----------|
| SIR ($\tau=0.2$) | 0.19±0.10 | 0.14±0.11 | **−0.06±0.09** |
| Unigram ($\tau=4.0$) | 3.04±1.52 | 1.63±1.38 | **−0.34±1.61** |

BIRA drives statistics **below** detection threshold on average — not merely near the boundary.

### Long-text stress test (Table 3)

600-token SIR-watermarked text from **Qwen2.5-32B** (stronger generator):

| Attack | TPR @ FPR=1% | LLM Judge | PPL |
|--------|--------------|-----------|-----|
| SIRA | 20.8% | 1.33 | 7.19 |
| **BIRA** | **4.0%** | **4.14** | 8.90 |

SIRA collapses on length; BIRA holds — relevant for essays, reports, and humanizer product targets.

### Ablation highlights (Table 2)

- **β = 0** (vanilla paraphrase): ASR 54.2% on SIR — confirms bias inversion is the mechanism, not paraphrase alone.
- **β = −4, q = 0.5:** ASR 99.6%, LLM judge 4.24 — sweet spot.
- **q = 0.9** (suppress only top 10% surprisal): ASR drops to 77.2% — proxy set must be wide enough.
- Self-information beats **random token selection** at equal set size (Figure 6).

### Beyond green-red schemes

- **EXP** (sampling watermark): ASR >98% — traces also concentrate in high-entropy choices.
- **Sentence-level** (SemStamp, SimMark): BIRA merges/splits sentences, breaking segmentation assumptions.
- **Adaptive white-box attack** (Diaa et al. 2024, Appendix H): BIRA black-box still wins with slight quality tradeoff.

---

## BIRA vs SIRA vs ordinary humanization

| Dimension | Ordinary paraphrase | SIRA (ICML 2025) | BIRA (ICML 2026) |
|-----------|--------------------|--------------------|------------------|
| **Mechanism** | Resample tokens | Mask high-surprisal → refill | Negative logit bias on surprisal set |
| **Training** | None | None | None |
| **Scheme knowledge** | None | None | None |
| **Avg ASR (7 schemes)** | ~50–90% | ~85–99% | **>99%** |
| **Long-text quality** | OK | **Fails** (judge 1.33) | **Holds** (judge 4.14) |
| **Cost** | 1× rewrite pass | 1× rewrite + mask steps | 1× rewrite + logit hook |
| **Code dependency** | Any LLM | MarkLLM + SIRA repo | Fork of SIRA/MarkLLM stack |

**Paper's explicit remark (project page):** "BIRA replaces SIRA's mask-and-refill step with a controllable negative decoding bias, yielding stronger, more semantics-preserving evasion."

**Humanizer overlap:** Any tool that (a) paraphrases with an LLM and (b) preferentially avoids reusing high-surprisal token choices performs a **weak, unintentional BIRA**. unslop's deterministic passes don't apply logit bias — but cross-model LLM rewrite (recommended in `detector.py` after ladder exhaustion) will **incidentally** scrub statistical watermarks. BIRA proves that scrubbing can be **optimized to >99%** with one decoding hook.

---

## Debate — supporters, skeptics, and what changed

### 4.1 Authors' stated position (Impact Statement)

Hwang et al. frame BIRA as **adversarial red-teaming**, not a deployment recipe:

> "Transparently identifying vulnerabilities is a prerequisite for scientific progress… serving as a necessary form of adversarial red-teaming aiming to foster the development of more robust defenses."

They acknowledge release risk (misuse to hide AI-generated misinformation) and argue current watermark evals **overestimate robustness** because they stress-test insertion/deletion/substitution — not **semantic-preserving LLM rewrite**.

### 4.2 Watermark optimists (pre-BIRA)

| Actor | Claim | BIRA challenge |
|-------|-------|----------------|
| **Kirchenbauer et al. (ICLR 2024 reliability)** | Watermarks survive common edits | BIRA is not "common edit" — full generative rewrite with targeted bias |
| **Google SynthID-Text (Nature 2024)** | Production-scale provenance | WaterPark DP-40 → 0.498 TPR; BIRA >99% ASR on academic scheme grid; SynGuard (Aug 2025) is a partial patch |
| **EU AI Act Art. 50 (Aug 2026)** | Mandate machine-readable marking | Marking ≠ durable proof if rewrite strips signal; Code of Practice explicitly bans removal |
| **OpenAI (Jul 2024)** | Declined 99.9% text watermark — churn + paraphrase | BIRA validates the paraphrase objection with formal bounds |

### 4.3 Watermark pessimists (post-BIRA, aligned with paper)

| Actor | Claim | Evidence chain |
|-------|-------|----------------|
| **WaterPark authors** | No single scheme wins all axes; paraphrase is default failure mode | Agent #20; DP-40 grid |
| **SIRA authors (Cheng et al.)** | Query-free removal is commodity-cheap | BIRA extends same line with better ASR + fidelity |
| **DAMAGE authors** | Humanizers strip SynthID as side effect | Table 2: 66.5% → 1.5% TPR; BIRA generalizes mechanism |
| **Sadasivan TV bound** | Detection and evasion share a distribution gap | Watermark is orthogonal — statistical mark, not "AI-ness" |

**Synthesis:** BIRA does not refute watermark **existence** — it refutes watermark **reliability under rewrite** as a standalone compliance control. Multilayer provenance (C2PA metadata + watermark + retrieval + detector ensemble) is the surviving regulatory story.

### 4.4 Skeptical / limiting counters

| Counter | Source | Force |
|---------|--------|-------|
| **Eval uses OPT-1.3B watermarked text** | Paper §5.1 | Short, high-entropy generations favor rewrite attacks; production SynthID on Gemini may use different γ/δ |
| **MarkLLM scheme params ≠ production** | WaterPark limitation | Google/OpenAI may tune undiscclosed parameters |
| **No SynthID-Text in main table** | Paper scope | DAMAGE + SynGuard papers cover SynthID separately; BIRA mechanism (surprisal suppression) should transfer to distribution-shift marks |
| **Retrieval defense not tested** | Krishna et al. NeurIPS 2023 | Provider-side BM25/P-SP on API logs detects paraphrased **semantic duplicates** regardless of watermark — different threat model |
| **Degeneration at extreme β** | Table 2 | ASR saturates by β=−4; quality cliff after — attack has Pareto frontier, not free lunch |
| **Dual-use release** | Impact Statement | GitHub + ICML poster = reproducible removal; defenders wanted embargo debate (no public OpenReview thread found Aug 2026) |

### 4.5 Defense responses (post-BIRA landscape)

| Defense | Paper | Claim vs BIRA |
|---------|-------|---------------|
| **SynGuard** | arXiv:2508.20228 | Hybrid SIR + SynthID; +11.1% avg F1 vs SynthID under 4 attacks — **not evaluated against BIRA specifically** |
| **Paraphrase Inversion** | arXiv:2410.21637 | +22 AUROC vs humanized text for **detectors**, not watermark recovery |
| **Sentence-level watermarks** | SemStamp, SimMark | BIRA appendix claims effectiveness via segmentation break — arms race continues |
| **Stronger γ / localized detection** | Appendix E.2 | Raises evasion cost; paper shows BIRA still wins with quality tradeoff |

**Open problem:** No published benchmark yet unifies **BIRA + SIRA + commercial humanizers + SynthID production params** in one grid. WaterPark predates BIRA; RAID/SHIELD/WATERPARK don't list BIRA as standard attack.

---

## unslop ethics boundary

### 5.1 Structural coupling (why BIRA matters to unslop)

BIRA formalizes what unslop docs already admit:

| Layer | Watermark goal | Humanizer goal | BIRA insight |
|-------|----------------|----------------|--------------|
| Token distribution | Bias toward green / marked tokens | Reduce AI-smoothness, increase variance | Suppress high-surprisal tokens → both |
| Detection target | z-test on green rate | TMR / perplexity / DivEye | Different detectors, **same rewrite pass** |
| User intent | Prove provenance | Sound human / fix ESL false positive | Intent determines ethics, not mechanism |

From `skills/unslop/SKILL.md`:

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real. Users who need provenance should watermark **after** unslop, not before.

BIRA upgrades "side effect" from anecdote (DAMAGE Table 2) to **theorem + >99% ASR**.

### 5.2 Hard boundaries (non-negotiable)

| Rule | Rationale | Current unslop state |
|------|-----------|---------------------|
| **No BIRA implementation** | Deliberate provenance stripping; Art. 50 violation | Not in codebase ✅ |
| **No negative logit bias mode** | Core BIRA mechanism | unslop has no logit hooks ✅ |
| **No "watermark removal" marketing** | Smodin exposes `watermark_removal` API flag — regulatory liability | README/SKILL refuse ✅ |
| **No watermark-targeted prompts** | "Remove SynthID marks" = different product category | Anti-detector mode scoped to ESL/resume ✅ |
| **Document incidental degradation** | Honesty under EU transparency regime | SKILL Boundaries + README ✅ |
| **detector.py must not recommend watermark stripping** | Feedback ladder exhaustion message | Lines 396–407 explicitly prohibit ✅ |

### 5.3 What unslop may do (defensive scope)

| Allowed | Forbidden |
|---------|-----------|
| Remove AI-isms, improve burstiness, voice-match | Optimize ASR against KGW/SynthID/SIR detectors |
| Anti-detector mode for **ESL false-positive defense** | Anti-watermark mode for **EU disclosure evasion** |
| Cross-model rewrite when detector ladder exhausts | Cross-model rewrite **prompted to strip provenance** |
| Cite BIRA in research docs as structural vulnerability evidence | Ship BIRA repo as optional `--watermark-evade` flag |
| Advise: watermark **after** humanization if provenance required | Advise: run unslop **before** submission to defeat institutional watermark checks |

### 5.4 Regulatory context (August 2026)

- **EU AI Act Art. 50** — transparency obligations **in force** Aug 2026; Dec 2025 Code of Practice prohibits deliberate watermark removal.
- **California SB 243** — companion-chatbot safety; private right of action (parallel jurisdiction).
- **BIRA implication for compliance officers:** Any humanizer in the supply chain is a **provenance risk**. BIRA proves the risk is not vendor-specific — it's **mechanistic**.
- **unslop positioning:** Defensive humanization with explicit misconduct boundary — same ethical frame as BIRA authors' red-team argument, but **opposite implementation** (never optimize removal).

### 5.5 README / docs actions (from UPDATE-PLAN-2026-08)

| Action | Priority | Status |
|--------|----------|--------|
| Index BIRA in watermark synthesis (Cat 05) | P0 | Pending corpus refresh |
| Cite BIRA alongside SIRA/DAMAGE for side-effect claim | P1 | Partially in docs/research |
| Add BIRA to Boundaries evidence list in RESEARCH_AND_TECH.md | P1 | Pending |
| **Do not** add BIRA to detector feedback ladder | — | Correct — different objective |
| Optional bench: measure watermark z-score drop on unslop fixtures **for internal audit only** | P3 | Not shipped; publish aggregate only if run |

---

## Integration plan for unslop

### Current state

| Component | BIRA relationship |
|-----------|-------------------|
| `humanize.py` / `structural.py` | Incidental distributional shift; no logit bias |
| `surprisal.py` | Computes self-information — **same signal BIRA uses for $\widehat{\mathcal{G}}$**, but for DivEye measurement only |
| `detector.py` | TMR feedback; explicitly rejects watermark removal in exhaust message |
| `skills/unslop/SKILL.md` | Boundaries section covers watermark side effect + Art. 50 |

### Phase 0 — Documentation (no code)

1. Add BIRA row to `docs/research/05-ai-text-detection-and-evasion/A-academic.md` watermark attack table.
2. Cross-link Agent #72 from Agent #20 (WaterPark), #71 (SIRA when written), #12 (DAMAGE).
3. Update `UPDATE-PLAN-2026-08.md` Agent #72 status → complete.

### Phase 1 — Honest user guidance

1. README detector section: one sentence — "Research shows optimized rewrite (BIRA, ICML 2026) removes >99% of statistical watermarks; unslop may degrade marks incidentally."
2. GETTING_STARTED / Boundaries: **watermark after unslop** workflow for users who need C2PA/SynthID provenance.

### Anti-patterns (do not ship)

- `--strip-watermark` CLI flag or skill trigger
- Surprisal-guided **suppression** mode (using `surprisal.py` to down-weight tokens)
- Subprocess bridge to `ml-postech/LLM-Watermark-Evasion-via-Bias-Inversion`
- Marketing anti-detector mode as "undetectable by Google/Anthropic watermarks"
- Claiming unslop is "BIRA-safe" or "watermark-preserving" — rewrite passes are not provenance-neutral

---

## Comparison to adjacent unslop research memos

| Method | Training | Target | Watermark ASR | Semantic fidelity | unslop adoptability |
|--------|----------|--------|---------------|-------------------|---------------------|
| **BIRA** | None | Watermark z-score | **>99%** | High (LLM judge ~4.2) | **Refuse** — ethics boundary |
| **SIRA** | None | Watermark | ~85–99% | Medium; fails long text | Cite only |
| **DIPPER** | T5-XXL | Detector + watermark | High (DAMAGE SynthID) | Medium | Different-model rewrite analog |
| **WaterPark DP-40** | — | Benchmark paraphrase | ~0.498 TPR SynthID | N/A | Cite for side-effect magnitude |
| **unslop deterministic** | None | AI-isms / structure | Unknown (not measured) | Preservation contract | Shipped; incidental watermark effect |

---

## Key quotes (verbatim from paper)

> "We theoretically analyze rewriting-based evasion, demonstrating that reducing the average conditional probability of sampling green tokens by a small margin causes the detection probability to decay exponentially."

> "Empirically, BIRA achieves state-of-the-art evasion rates (>99%) across diverse watermarking schemes while preserving semantic fidelity substantially better than prior baselines."

> "These results suggest that many current watermarks can be removed with minimal effort, highlighting the need for more robust watermarking and evaluations beyond simple editing-based stress tests."

> "We acknowledge the potential risks associated with releasing a successful evasion method… we believe that transparently identifying vulnerabilities is a prerequisite for scientific progress."

---

## Open questions for unslop bench

1. Does unslop `humanize_structural` + cross-model LLM pass measurably drop KGW z-score on fixtures — and by how much vs BIRA?
2. Is incidental removal **correlated** with anti-detector TMR gains, or orthogonal (watermark vs neural detector)?
3. Will Anthropic's Aug 2026 default text watermark use params that survive surprisal suppression better than MarkLLM SIR?
4. Should unslop publish a **provenance checklist** (C2PA sign after edit) for enterprise users?

---

## BibTeX

```bibtex
@article{hwang2025llm,
  title={LLM Watermark Evasion via Bias Inversion},
  author={Hwang, Jeongyeon and Park, Sangdon and Ok, Jungseul},
  journal={arXiv preprint arXiv:2509.23019},
  year={2025},
  url={https://arxiv.org/abs/2509.23019},
  note={ICML 2026 poster}
}
```

---

*Agent #72 complete. Cross-ref: Agent #20 (WaterPark), #12 (DAMAGE SynthID), #31 (DIPPER), #71 (SIRA), UPDATE-PLAN-2026-08 watermark table, `skills/unslop/SKILL.md` Boundaries, `detector.py` L396–407.*
