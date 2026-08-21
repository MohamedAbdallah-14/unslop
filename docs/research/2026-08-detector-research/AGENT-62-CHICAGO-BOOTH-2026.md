# Agent #62 — Chicago Booth 2026 Benchmark (Jabarian & Imas)

**Topic:** Independent academic audit of commercial AI detectors and humanizer robustness — the benchmark unslop docs call "Chicago Booth 2026"  
**Primary paper:** Jabarian & Imas, *Artificial Writing and Automated Detection*, BFI WP 2025-116 / NBER w34223 (Aug 26, 2025)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

"Chicago Booth 2026" is **community shorthand**, not a separate 2026 study. The underlying audit is **Jabarian & Imas (August 2025)**: 1,992 human passages × four frontier LLMs, four detectors, two stress tests (ultra-short stubs, StealthGPT humanizer). The Booth Review lay summary shipped **December 2, 2025**. GPTZero's **January 2026 rebuttal** re-ran the *clean-text* corpus with corrected API fields and branded the result "Chicago Booth 2026" — which is why unslop SKILL.md and README cite it that way.

Three findings survive scrutiny:

1. **Clean, medium-to-long text:** All three commercial detectors (Pangram, GPTZero, Originality.ai) work well. Pangram leads on policy-cap metrics (FPR ≤ 0.5% without sacrificing recall). RoBERTa is unusable (30–69% FPR).
2. **Humanizer stress test (StealthGPT only):** The ranking **inverts**. Pangram stays robust (FNR mostly 0–5%). GPTZero **collapses** (FNR ~44–77% by genre/model in Table B.4). This arm was **not** re-run in GPTZero's rebuttal.
3. **Ranking dispute on clean text:** GPTZero claims Booth used the wrong API field (`average_generated_prob` vs `predicted_class`). Plausible methodological objection. GPTZero's re-run (model `2025-12-18-base`) puts itself first on recall; Booth puts Pangram first. Both agree commercial >> open-source.

**Attribution fixes for unslop:** Booth tested **one** humanizer (StealthGPT), not twelve. The "~6 points median accuracy drop" in README **does not appear** in Jabarian & Imas — likely conflated with [HumanizerBench](https://humanizerbench.com/) (WriteHuman-operated, 12 tools). Turnitin's "60–85% on humanized text" comes from **other** independent tests (e.g. MPG ONE), not this paper — Turnitin wasn't evaluated.

**unslop verdict:** Booth is the best **independent, multi-genre, multi-model** reference for detector comparison. For unslop users, the actionable slice is §4.2 (humanizer arm): lexical SaaS rewrites break GPTZero but not Pangram. unslop is not a detector-defeat tool; Booth supports "cross-model second pass + manual edit" over single-pass humanizer SaaS — but cite DAMAGE or HumanizerBench for multi-humanizer numbers, not Booth.

---

## What "Chicago Booth 2026" actually is

| Layer | Date | What it is |
|-------|------|------------|
| **Working paper** | Aug 26, 2025 | Jabarian & Imas, BFI WP 2025-116, [NBER w34223](https://doi.org/10.3386/w34223) |
| **Lay summary** | Dec 2, 2025 | [Chicago Booth Review](https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust) |
| **GPTZero rebuttal** | Jan 2026 | [gptzero.me/news/chicago-booth-2026](https://gptzero.me/news/chicago-booth-2026/) — re-runs clean-text arm only |
| **"2026" label** | Jan 2026+ | Vendor/community branding after GPTZero post; paper itself is 2025 |

Not peer-reviewed. NBER working papers are circulated for discussion. Still the **strongest independent commercial-detector audit** as of August 2026 — no financial conflicts disclosed; authors thank Kevin Bryan; funded by Booth CAAI, BFI, Google Cloud Research Program.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Working paper PDF (BFI)** | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| **NBER DOI** | https://doi.org/10.3386/w34223 |
| **Chicago Booth Review summary** | https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust |
| **GPTZero rebuttal / re-run (Jan 2026)** | https://gptzero.me/news/chicago-booth-2026/ |
| **GPTZero predictions spreadsheet (linked from rebuttal)** | Referenced in rebuttal post; not independently verified here |
| **Replication package** | Paper Appendix D references code/logs; README in replication repo per paper |

### Related (NOT Booth, often conflated)

| Resource | URL | Note |
|----------|-----|------|
| **HumanizerBench (12 humanizers)** | https://humanizerbench.com/ | WriteHuman-operated; separate from Booth |
| **DAMAGE (19 humanizers)** | https://arxiv.org/abs/2501.03437 | Peer-reviewed; academic essays |
| **Turnitin bypasser update** | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers | Not in Booth corpus |

---

## Methodology

### Corpus construction

- **Human:** 1,992 unique pre-2020 passages across six genres — Amazon reviews (200), blogs (200), news (300), novel excerpts (1,000), restaurant reviews (100), résumés (192).
- **AI:** Matched 1,992 passages per source model via mimetic prompt (same substance/structure, different wording). Temperature 0.7; max 4,096 tokens; output capped at 2× input length.
- **LLMs:** GPT-4.1, Claude Opus 4, Claude Sonnet 4, Gemini 2.0 Flash. (GPT-3.5 replicated in appendix only.)
- **Length buckets:** Long (novel, résumé ~790–1,040 words), medium (news, blog ~200–460 words), short (reviews ~77–133 words), stubs (<50 words, 160 per model).

Human and AI matched on word count, lexical variety (TTR), readability (Flesch–Kincaid) to reduce confounds.

### Detectors evaluated

| Detector | API score field used by Booth | Type |
|----------|-------------------------------|------|
| **Pangram** | `prob_ai` | Commercial |
| **Originality.ai** | `probability_ai` | Commercial |
| **GPTZero** | `average_generated_prob` | Commercial |
| **RoBERTa-base** | Fine-tuned GPT-2 output classifier | Open-source baseline |

### Metrics

1. **FPR** — human text flagged as AI (Type I).
2. **FNR** — AI text missed (Type II).
3. **AUROC** — P(AI score > human score) for random pair.
4. **Δ-Mean** — E[score | AI] − E[score | human].
5. **Threshold strategy:** (a) Youden's J per genre (Table 1); (b) exogenous thresholds 0.1–0.9 (Tables 4–5); (c) **policy caps** — fix FPR ≤ x%, report resulting FNR (§5.2).

### Stress tests

1. **Stubs (<50 words):** 160 passages per model. Originality.ai rejects some stubs ("length filter") — excluded from stub analysis.
2. **Humanizer:** Every AI passage through **StealthGPT default rewrite endpoint**; re-scored. **Only one humanizer tested.**

### What Booth did NOT test

- Turnitin, Copyleaks, Winston AI, Grammarly Authorship, or other commercial tools.
- Multiple humanizers (only StealthGPT).
- Mixed human/AI documents, keystroke provenance, or process replay.
- ESL/non-native writer fairness (pre-2020 English corpus; no TOEFL-style stress test).
- unslop or any in-editor polish tool.

---

## Key numbers — clean (unhumanized) AI text

### False positive rates (human text misflagged)

Detector-optimized thresholds, by genre aggregate (Table 2):

| Detector | Short passages | Medium–long passages |
|----------|----------------|----------------------|
| **Pangram** | ≤ 0.75% | ~0% |
| **GPTZero** | ≤ 2.38% | ≤ 1.0% |
| **Originality.ai** | ≤ 2.18% | ≤ 0.26% |
| **RoBERTa** | 31–78% | 30–78% |

At exogenous threshold 0.5 (Table 4): Pangram FPR 0.0%; GPTZero 0.71%; Originality 0.11%; RoBERTa 95%.

### False negative rates (AI text missed)

Medium-to-long passages, detector-optimized thresholds (Table 3 summary):

| Detector | Typical FNR (medium–long) | Short passages |
|----------|---------------------------|----------------|
| **Pangram** | ~0% (max 1% on some cells) | ≤ 2% |
| **GPTZero** | ≤ 5% | ≤ 7% |
| **Originality.ai** | ≤ 2% | ≤ 5% |
| **RoBERTa** | 5–51% | Higher |

### AUROC (discrimination)

Pangram: 0.9979–1.0000 on most genre×model cells. GPTZero: 0.96–1.00 (lower on short Amazon/restaurant reviews). Originality: generally high but below Pangram. RoBERTa: often near 0.5 (random).

### Policy-cap headline

At **FPR cap ≤ 0.5% (0.005):** Pangram is the **only** detector that meets the cap without sacrificing AI detection across all four generative models (abstract + §5.2). Originality.ai "comes second, failing slightly short on higher policy caps." GPTZero and Originality degrade under the **most stringent** caps but recover when cap loosens to 1%.

### Cost economics (Table B.5–B.6)

Average per-passage API fee: Pangram $0.0228, Originality $0.0416, GPTZero $0.0575 per true positive. Pangram ~2× cheaper than Originality, ~3× cheaper than GPTZero.

---

## Key numbers — stubs (<50 words)

| Metric | Pangram | GPTZero | RoBERTa |
|--------|---------|---------|---------|
| FPR (by genre) | 0–2.5% | 0–3.3% | 29–49% |
| FNR (worst cells) | News stubs + Claude/Gemini: 11–22% | News + Claude Opus: **44%**; multiple cells 10–20% | Up to 44% |
| AUROC | 0.96–1.00 | 0.78–1.00 | 0.57–0.79 |

**Résumé bullets and social stubs are harder for everyone.** Pangram degrades least; GPTZero's stub FNR spikes on news genre.

---

## Key numbers — StealthGPT humanizer arm (Table B.4)

This is the **highest-value table for unslop**. FNR after StealthGPT rewrite:

| Detector | Long passages (novel, résumé) | Short passages (reviews) | Representative GPT-4.1 cells |
|----------|------------------------------|--------------------------|------------------------------|
| **Pangram** | ~0% | 1–5% | amazon 2.5%, blog 0%, news 2%, novel 0%, resume 0% |
| **Originality.ai** | ~2–10% | up to **21%** | amazon 8.9%, news 7.4%, restaurant 19% |
| **GPTZero** | **~44–77%** | **~53–68%** | amazon **67.8%**, blog 44.5%, news 50.7%, novel 44.7%, resume 63.5% |
| **RoBERTa** | High throughout | High | 15–94% depending on cell |

Paper prose (§4.2): *"GPTZero largely loses its capacity to detect AI-generated text, with FNR scores around 0.50 and above across most genres and LLM models."*

**Pangram's humanizer robustness is the paper's adversarial headline.** GPTZero's Jan 2026 rebuttal does **not** address this arm.

---

## GPTZero rebuttal (Jan 2026) — clean-text re-run

### Methodological dispute

Booth binarized GPTZero using `average_generated_prob` (sentence-level average). GPTZero argues document classification should use `predicted_class` / `class_probabilities` — the field dashboard users see.

Fair point: same numeric threshold on different fields is not apples-to-apples. Booth did not contact GPTZero before publication (GPTZero's claim; not independently verified).

### GPTZero re-run results (clean text only, model `2025-12-18-base`)

| Detector | FPR | Recall | Accuracy |
|----------|-----|--------|----------|
| **GPTZero** | 0.05% (1 error) | **99.3%** | **99.5%** |
| **Pangram** | 0.05% (1 error) | 98.9% | 99.1% |
| **Originality.ai** | 0.11% (2 errors) | 81.3% | 85.0% |

Binary collapse rules (GPTZero post):
- **GPTZero AI bucket:** AI, AI-paraphrased, Mixed, Lightly edited by AI
- **Pangram AI bucket:** Possibly/Likely/Highly Likely AI
- **Originality AI bucket:** AI only

Originality processed 6,879/9,960 predictions (length filter).

### What the rebuttal does NOT settle

1. **Humanizer arm** — no re-run published.
2. **Model version** — Booth API calls Aug 2025; re-run Dec 2025 (`2025-12-18-base`). GPTZero shipped 15 model releases in 2025 alone.
3. **Independent replication** — vendor re-run, not third-party.
4. **Multiclass → binary collapse** — counting Mixed and "Lightly edited by AI" as AI inflates recall vs strict "fully AI-generated" definitions institutions may want.

No formal Pangram response located as of this memo.

---

## Debate map

| Stakeholder | Position | Strength |
|-------------|----------|----------|
| **Jabarian & Imas** | Pangram only policy-grade detector; GPTZero good on clean text, fails humanizer test; policy-cap framework for institutions | Independent corpus; transparent methods; replication package promised |
| **GPTZero** | Booth used wrong API field; corrected run shows GPTZero #1 on recall/accuracy (clean text) | Plausible field mismatch; doesn't address humanizer collapse |
| **Pangram** | Implicitly aligned with Booth initial ranking; no public rebuttal found | Admissions market cites Booth; Aug 2025 humanizer table shows adapted Pangram catches 90–100% of named tools |
| **Skeptics (GradPilot, AIForesight360)** | Working paper ≠ settled science; all vendor numbers directional; benchmark gaming possible | Correct epistemic humility |
| **unslop README (current)** | "Twelve humanizer services," "~6 points median drop" | **Misattributed** — see Agent #40 correction |

### Consensus (low controversy)

- Commercial detectors beat open-source RoBERTa by a wide margin on this corpus.
- Short text degrades all tools.
- Detection is an arms race; routine audits needed (paper §6).
- Policy-cap framing is useful for institutional tradeoffs (false accusation vs missed AI).

### Open fights

- Clean-text ranking: Pangram vs GPTZero (field + model version sensitive).
- Whether StealthGPT results generalize to 2026 humanizer ecosystem (DAMAGE 19-tool, HumanizerBench 12-tool suggest **detector-specific** outcomes).
- ESL fairness — not in Booth; Liang 2023 still cited separately.

---

## Comparison to other benchmarks unslop tracks

| Benchmark | Scope | Humanizers | Detectors | Peer-reviewed |
|-----------|-------|------------|-----------|---------------|
| **Chicago Booth (Jabarian & Imas)** | 6 genres, 4 LLMs, matched length | **1** (StealthGPT) | 4 | No (working paper) |
| **DAMAGE (COLING 2025)** | Academic essays | **19** named | Pangram + others | Yes |
| **HumanizerBench (Aug 2026)** | 33 samples × 12 humanizers | **12** | 5 commercial | No (vendor-operated) |
| **RAID / SHIELD** | Research harnesses | Paraphrase arms | Many | Yes (research) |

**Use Booth for:** independent policy-cap framing, clean-vs-humanized split on a fixed corpus, genre/length sensitivity, cost-per-true-positive economics.

**Use DAMAGE/HumanizerBench for:** multi-humanizer bypass rates, tier comparisons.

**Do not use Booth for:** Turnitin accuracy, twelve-humanizer medians, or "~6 pp" marketing corrections.

---

## unslop implications

### Documentation corrections (high priority)

| Current claim (repo) | Booth actually says | Fix |
|---------------------|---------------------|-----|
| "Chicago Booth 2026 audit of **twelve** humanizer services" (README L610) | **One** humanizer: StealthGPT | Split: Booth = 1 humanizer; HumanizerBench = 12 |
| "median accuracy drop **~6 points**" (README L400, L610) | Not in Jabarian & Imas; GPTZero FNR → **~50%+** on humanized text | Cite primary source or remove |
| "Turnitin drops to 60–85% on humanized text **there**" (SKILL.md) | Turnitin not tested | Attribute to MPG ONE / other independent tests |

### Product / SKILL.md landscape

1. **Reference benchmark status confirmed.** Booth (plus GPTZero rebuttal) displaced Scribbr 2024 rankings as the community's external anchor for "does it pass independent eval?" — especially in education/admissions discourse.

2. **Detector-specific humanizer outcomes.** Booth proves aggregate "humanizer bypass" is wrong. Pangram robust; GPTZero fragile **under Booth's Aug 2025 API usage** on StealthGPT. unslop anti-detector mode should document that a green GPTZero check after SaaS humanizer pass is **not** transferable to Pangram or Turnitin 2026.

3. **Clean text vs edited text gap.** Even GPTZero's rebuttal shows 99.3% recall on **raw** AI pairs. Independent docs (MPG ONE, repo synthesis) cite 60–80% on paraphrased/edited content. unslop's honest frame: polish layer improves voice; **does not guarantee** detector clearance.

4. **Short-form / résumé users.** Booth includes résumé genre (192 passages) and stub analysis. Ultra-short writing hurts all detectors; aligns with unslop origin story (résumé bullets). Voice-match + structural entropy matter more than vocabulary deletion for short form.

5. **Policy-cap language for ESL defense.** Booth's FPR-cap framework supports unslop's documented use case: institutions with strict false-accusation tolerance (ESL writers) vs catch-rate optimization. unslop anti-detector mode is defensive — Booth gives vocabulary to argue detector thresholds, not evasion guarantees.

6. **Benchmark hygiene for unslop evals.** If running internal GPTZero tests, use `predicted_class` not `average_generated_prob` (Booth lesson). Log model version string (`2025-12-18-base` or later).

### What unslop should NOT claim

- "Beats Chicago Booth" — unslop isn't in the study.
- "Six-point detector drop" — unsourced vs Booth.
- "Passes Chicago Booth" — no such pass/fail threshold exists; paper reports continuous FPR/FNR.

### Recommended benchmark wiring

From [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md) + [AGENT-57](./AGENT-57-GPTZERO-EVOLUTION.md):

- Add Booth corpus metadata (or genre-matched unslop samples) to `benchmarks/detector_bench.py`.
- Report **two arms:** clean post-unslop vs StealthGPT-equivalent (cross-model paraphrase proxy).
- Track Pangram + GPTZero (`predicted_class`) + optional Turnitin separately.
- Publish Mixed/Polished/Paraphrased breakdown for GPTZero, not binary AI rate alone.

---

## Timeline

| Date | Event |
|------|-------|
| Aug 26, 2025 | Working paper v1 (BFI WP 2025-116) |
| Sep 2025 | NBER w34223 circulation |
| Dec 2, 2025 | Chicago Booth Review lay article |
| Jan 12, 2026 (approx.) | GPTZero rebuttal + clean-text re-run |
| Aug 2026 | Community adopts "Chicago Booth 2026" as shorthand; Scribbr rankings treated as stale |

---

## Bottom line

Chicago Booth 2026 = **Jabarian & Imas independent audit** + **GPTZero clean-text rebuttal**. For unslop, the durable lesson is not who wins on pristine AI essays — it's that **humanizer stress tests reorder detectors** (Pangram robust, GPTZero collapsed in the academic protocol) and that **short genre-matched text** remains hard. Fix README misattributions (twelve humanizers, six-point drop). Keep citing Booth for policy-cap framing and StealthGPT robustness splits; cite DAMAGE/HumanizerBench for multi-tool bypass tables; cite other sources for Turnitin.

---

## Cross-references

- [AGENT-40 — DAMAGE humanizer tiers](./AGENT-40-DAMAGE-HUMANIZER-TIERS.md) — attribution correction source
- [AGENT-57 — GPTZero evolution](./AGENT-57-GPTZERO-EVOLUTION.md) — rebuttal numbers, API field lesson
- [AGENT-56 — Turnitin 2025–2026](./AGENT-56-TURNITIN-2025-2026.md) — separate from Booth corpus
- [AGENT-15 — RAID benchmark](./AGENT-15-RAID-BENCHMARK.md) — research harness complement
- [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md) — wiring priorities

---

## Open items

- [ ] Independent third-party re-run of Booth corpus with `predicted_class` **and** StealthGPT arm on current model versions
- [ ] Pangram formal response to GPTZero rebuttal (if any)
- [ ] Primary source for README "~6 points median drop" or retraction ([AGENT-40](./AGENT-40-DAMAGE-HUMANIZER-TIERS.md))
- [ ] Verify GPTZero predictions spreadsheet from rebuttal post
- [ ] Peer-review status of NBER w34223 (still working paper as of Aug 2026)
