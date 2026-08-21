# Agent #74 — Kirchenbauer KGW Watermark

**Topic:** Kirchenbauer et al., *A Watermark for Large Language Models* (ICML 2023) — the foundational green-list / red-list LLM watermark; implementations, detection, removal attacks, regulatory role  
**Prepared:** August 19, 2026  
**Scope:** Original paper + ICLR 2024 reliability follow-up, official code, benchmark lineage (MarkLLM, WaterPark), attack catalog (Sadasivan → SIRA/BIRA), EU AI Act Art. 50, unslop boundary  
**Status:** complete

---

## Executive summary

**KGW** (Kirchenbauer–Geiping–Wen et al., University of Maryland, ICML 2023) is the canonical **distribution-shift** text watermark. At each generation step, a keyed pseudo-random function partitions the vocabulary into a **green list** (fraction γ) and **red list**; green-token logits get a bias δ before sampling. Detection is key-only: count green tokens and run a one-sided **z-test** — no model weights, no API access. Default settings (γ=0.25, δ=2) detect watermarked OPT-6.7B output from ~25 tokens at p≈10⁻¹⁴ with negligible perplexity cost on high-entropy spans.

The paper spawned an entire research family. Benchmarks label it **TGRL** (text-dependent green/red list). MarkLLM, WaterPark, SIRA, and TempParaphraser all treat KGW as the baseline scheme. SynthID-Text (Google, Nature 2024) generalizes the green-list idea to tournament sampling and ships on Gemini; Aaronson–Kirchner (OpenAI, 2022) is a parallel **distribution-transform** lineage that OpenAI **did not deploy** on ChatGPT (Aug 2024 WSJ/Verge reporting).

**Robustness arc (2023→2026):** Kirchenbauer ICLR 2024 argues watermarks beat post-hoc detectors and remain detectable after human paraphrase at ~800 tokens (FPR 10⁻⁵). That optimism collides with unified 2025 benchmarks: WaterPark DP-40 cuts TGRL TPR from 0.993 → **0.485**; copy-paste dilution (10% watermarked) → **TPR ≈ 0**. SIRA (ICML 2025) and BIRA (2025) report **~100% / >99%** evasion on KGW at $0.88/M tokens with no watermark key. The field now treats KGW as the **reference implementation**, not a production-grade mark.

**Regulatory role (Aug 2026):** EU AI Act **Article 50(2)** requires machine-readable marking of generative outputs (effective **2 Aug 2026** for disclosure; **2 Dec 2026** grace for marking on systems already on market). The law does not name KGW, but Commission Guidelines and the Code of Practice cite watermarking as one technique; free-form text >200 tokens needs an **imperceptible in-content watermark** (metadata alone insufficient). KGW is the academic and open-source default cited in compliance guidance — while red-team results show **paraphrase/humanization breaks it**.

**Unslop verdict:** KGW is upstream provenance, not a post-hoc AI detector. unslop's rewrite passes (cross-model paraphrase, burstiness injection) **statistically scrub green-list bias** as a side effect — same mechanism as DIPPER/SIRA attacks, different intent. Policy: no watermark-stripping mode; anti-detector targets ESL/resume false positives, not Art. 50 compliance. If users need provenance, mark **after** humanization or accept mark loss.

---

## 1. Paper identity

### 1.1 Primary paper — ICML 2023

| Field | Value |
|-------|-------|
| **Title** | A Watermark for Large Language Models |
| **Authors** | John Kirchenbauer*, Jonas Geiping*, Yuxin Wen, Jonathan Katz, Ian Miers, Tom Goldstein (*equal contribution) |
| **Affiliation** | University of Maryland |
| **Venue** | ICML 2023, Honolulu; PMLR 202:17061–17084 |
| **First posted** | 24 Jan 2023 |
| **arXiv** | https://arxiv.org/abs/2301.10226 |
| **PMLR** | https://proceedings.mlr.press/v202/kirchenbauer23a.html |
| **Code** | https://github.com/jwkirchenbauer/lm-watermarking |

**One-line contribution:** Inference-time logit biasing toward a context-dependent green list; open detection via z-score; information-theoretic sensitivity bounds (spike entropy); negligible quality impact when entropy is high.

### 1.2 Follow-up — ICLR 2024 reliability

| Field | Value |
|-------|-------|
| **Title** | On the Reliability of Watermarks for Large Language Models |
| **Authors** | Kirchenbauer, Geiping, Wen, Shu, Saifullah, Kong, Fernando, Saha, Goldblum, Goldstein |
| **Venue** | ICLR 2024, Vienna |
| **arXiv** | https://arxiv.org/abs/2306.04634 |
| **OpenReview** | https://openreview.net/forum?id=DEJIDCmWOz |
| **Code** | Same repo (`lm-watermarking`) |

**One-line contribution:** Watermark reliability as a function of **text length**; human + GPT-3.5 + Dipper paraphrase dilute but do not erase marks; ~800 tokens needed after strong human rewrite at FPR 10⁻⁵; span-detection for copy-paste; watermarks more robust than DetectGPT-class post-hoc detectors.

### 1.3 Naming in the wild

| Label | Where used | Meaning |
|-------|------------|---------|
| **KGW** | Papers, attacks (SIRA, BIRA), practitioner docs | Kirchenbauer green-list watermark |
| **TGRL** | WaterPark, MarkLLM tables | Text-dependent green/red list (KGW default) |
| **Maryland watermark** | vLLM-Watermark docs | Same algorithm, UMD origin |
| **Green-list scheme** | EU guidelines, textbooks | Generic class; KGW is the reference instance |

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (arXiv)** | https://arxiv.org/abs/2301.10226 | 113+ citations; definitive algorithm spec |
| **Paper (PMLR PDF)** | https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf | ICML camera-ready |
| **Reliability (arXiv)** | https://arxiv.org/abs/2306.04634 | ICLR 2024 robustness study |
| **Official GitHub** | https://github.com/jwkirchenbauer/lm-watermarking | `WatermarkLogitsProcessor`, `WatermarkDetector` |
| **MarkLLM toolkit** | https://arxiv.org/abs/2405.10051 · https://github.com/THU-BPM/MarkLLM | 9+ schemes; KGW is family anchor |
| **WaterPark benchmark** | https://arxiv.org/abs/2411.13425 · https://github.com/JACKPURCELL/WaterPark | TGRL = KGW baseline |
| **vLLM-Watermark** | https://vermaapurv.com/vLLM-Watermark/algorithms/maryland.html | Production-style HF integration |
| **Aaronson EXP (OpenAI lineage)** | Aaronson & Kirchner 2022 (cited in SIRA/BIRA evals) | Dist.-transform variant; not shipped on ChatGPT |
| **SynthID-Text (successor prod.)** | https://www.nature.com/articles/s41586-024-08025-4 | Gemini-scale deployment |
| **Sadasivan (attacks KGW)** | https://arxiv.org/abs/2303.11156 | First paraphrase break; spoofing |
| **SIRA attack** | https://arxiv.org/abs/2505.05190 | ICML 2025; ~100% ASR on KGW |
| **BIRA attack** | https://arxiv.org/abs/2509.23019 | >99% evasion; improves on SIRA |
| **EU Art. 50 Guidelines** | https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations | Finalized Jul 2026 |
| **OpenAI watermark non-deployment** | https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool | Aug 2024 |
| **Sibling agent: WaterPark** | `docs/research/2026-08-detector-research/AGENT-20-WATERPARK-BENCHMARK.md` | TGRL numbers |
| **Sibling agent: Sadasivan** | `docs/research/2026-08-detector-research/AGENT-17-SADASIVAN-IMPOSSIBILITY.md` | TV bound + KGW paraphrase |
| **Sibling agent: DIPPER** | `docs/research/2026-08-detector-research/AGENT-31-DIPPER.md` | Primary paraphrase attack |

---

## 3. Algorithm — generation

### 3.1 Hard vs soft watermark

**Algorithm 1 (hard red list):** Sample **only** from green list; red tokens forbidden. Detection trivial (any red-list violation → machine). Breaks low-entropy sequences ("Barack" → "Obama" blocked).

**Algorithm 2 (soft red list — deployed default):** Add δ to green logits, then softmax + sample. Red tokens remain possible but disfavored. Low-entropy tokens (p≈1) unchanged; high-entropy choices skew green.

### 3.2 Hyperparameters

| Symbol | Role | Typical values | Trade-off |
|--------|------|----------------|-----------|
| **γ** | Green-list fraction \|G\|/|V| | 0.25 (paper fig. 1), 0.5 common | Higher γ → easier detect, more distortion |
| **δ** | Logit bias on green tokens | 2.0 (default), ln(2)≈0.7 in theory | Higher δ → stronger mark, higher perplexity on medium-entropy tokens |
| **h** | Context width for PRF seed | 1 (LeftHash), 4+ (SelfHash/minhash) | h=1 simpler; wider context resists some attacks, hurts robustness per SIRA KGW-k ablation |
| **seeding_scheme** | PRF construction | `selfhash`, `ff-anchored_minhash_prf-4-True-*` | Must match between generator and detector |
| **z_threshold** | Detection cutoff | 4.0 → one-sided p≈3×10⁻⁵ | Lower → more sensitive, more FPR |

### 3.3 Seeding schemes (implementation detail)

Official repo (`extended_watermark_processor.py`):

- **LeftHash:** Hash prior token(s) → PRNG seed → partition V.
- **SelfHash:** MinHash over n-gram context; more entropy in partition, different robustness profile (ICLR 2024 Fig. 2 compares SelfHash vs LeftHash under Dipper/GPT attacks).

WaterPark/SIRA often use **KGW-1** (single left token) as the canonical weak-but-standard setting.

### 3.4 Low-entropy caveat (§1.2)

Memorized or deterministic completions (code, fixed phrases) are **hard to watermark without quality loss**. KGW's fix: wrap low-entropy spans inside a longer high-entropy passage; detection aggregates over T tokens. Failure mode in paper Table 1: near-copy regurgitation → z≈0, undetectable.

### 3.5 Information-theoretic sensitivity (Theorem 4.2)

Expected green count scales with **spike entropy** S(p, z) of the raw LM distribution. High-entropy steps → more green tokens → faster detection. OPT-1.3B on C4: mean spike entropy S≈0.807 → E[|s|_G]≥142.2 empirically 159.5 over 200 tokens; 98.4% detect at z=4 with multinomial sampling.

---

## 4. Algorithm — detection

### 4.1 Null hypothesis

H₀: Text produced with **no knowledge** of green-list rule (human or unwatermarked LM).

### 4.2 Z-statistic

For general γ:

\[
z = \frac{|s|_G - \gamma T}{\sqrt{T \gamma (1-\gamma)}}
\]

Reject H₀ (watermark detected) if z > z_threshold (default 4).

| Setting | Interpretation |
|---------|----------------|
| γ=0.5, hard list | z = 2(\|s\|_G − T/2)/√T |
| z > 4 | One-sided p ≈ 3×10⁻⁵ |
| ~25 tokens, γ=0.25, δ=2 | Example in Fig. 1: 28 green vs 9 expected → p≈6×10⁻¹⁴ |

### 4.3 Detection properties (design goals)

- **Public algorithm:** Detector can be open-sourced while model stays proprietary.
- **Key-only:** Needs shared secret (hash key + γ, δ, h); not the LM weights.
- **Contiguous span:** Works on a slice embedded in a longer doc (span detectors in ICLR 2024).
- **Private API mode:** Key hidden behind rate-limited API (§5 original paper); prevents unlimited spoofing queries.

### 4.4 Private vs public watermarking

| Mode | Pro | Con |
|------|-----|-----|
| **Public** | Third parties detect locally; transparent | Spoofing: infer green rules → inject false watermark (Sadasivan §spoofing) |
| **Private (API)** | Key secrecy | Query limits; centralization; adversary can still paraphrase |

---

## 5. Implementations

### 5.1 Official — `jwkirchenbauer/lm-watermarking`

| Component | File | Role |
|-----------|------|------|
| `WatermarkLogitsProcessor` | `extended_watermark_processor.py` | HuggingFace `LogitsProcessor` hook |
| `WatermarkDetector` | same | z-score over tokenized text |
| `WatermarkBase` | `watermark_processor.py` | Minimal reference |

**Integration pattern:**

```python
# Pseudocode — matches official README
processor = WatermarkLogitsProcessor(vocab, gamma=0.25, delta=2.0, seeding_scheme="selfhash")
detector = WatermarkDetector(vocab, gamma=0.25, seeding_scheme="selfhash", z_threshold=4.0)
# model.generate(..., logits_processor=[processor])
# detector.detect(text) → {z_score, p_value, prediction}
```

Requires **matching** γ, δ, seeding_scheme, and tokenizer between generation and detection.

### 5.2 Ecosystem integrations

| Project | URL / ref | KGW role |
|---------|-----------|----------|
| **MarkLLM** | THU-BPM/MarkLLM | Unified API for KGW + 8 variants; default eval harness |
| **WaterPark** | JACKPURCELL/WaterPark | TGRL slot in 12-scheme matrix |
| **vLLM-Watermark** | Maryland algo docs | `WatermarkingAlgorithm.MARYLAND`, `MARYLAND_Z` detector |
| **lm-watermarking demos** | HF Spaces linked from repo | Interactive detect/generate |
| **Adversarial Paraphrasing repo** | Agent #39 | KGW branch in watermark eval |

### 5.3 Not KGW but adjacent

| Scheme | Relation to KGW |
|--------|-----------------|
| **Unigram (Zhao 2023)** | Context-**free** green list; same z-test; WaterPark: *more* paraphrase-robust than TGRL |
| **EWD (Lu 2024)** | Entropy-gated δ; add-on to TGRL; typo TPR 0.222→0.472 in WaterPark |
| **Aaronson EXP** | OpenAI dist.-**transform**; evaluated alongside KGW in SIRA/BIRA |
| **SynthID-Text** | Tournament green-list generalization; production on Gemini |
| **RDF (Kuditipudi 2023)** | Index-dependent transform; beats TGRL on copy-paste, lower MAUVE |

---

## 6. Empirical results — original paper

### 6.1 Detection (OPT-1.3B, C4, γ=0.5, δ=2, z=4)

| Metric | Value |
|--------|-------|
| Type-I (human → flagged) | ~3×10⁻⁵ (by threshold design) |
| Type-II (watermarked → missed) | 1.6% multinomial; 0.4% 4-way beam |
| Low-entropy quartile failures | Memorization / near-copy rows |
| Perplexity impact | Minimal on high-entropy; bounded in supplement for medium entropy |

### 6.2 Removal cost (theoretical, §2)

Adversary with **full key knowledge** flipping 200/1000 tokens creates ≤400 red violations; ~600 greens remain → z≈6.3, still detected. Without key: each flip 50% red → ~200 violations → weaker but often sufficient at long T.

**Without key + paraphrase:** Sadasivan shows small T5/PEGASUS models break detection far below this analysis.

---

## 7. Robustness timeline — attacks on KGW

### 7.1 Attack taxonomy

| Class | Examples | Mechanism vs KGW |
|-------|----------|------------------|
| **Lexical edit** | Typo, synonym, swap | Breaks LeftHash context chain; WaterPark typo TPR 0.222 |
| **Paraphrase (LM)** | T5, PEGASUS, Dipper, GPT-3.5/4 | Resample tokens → reset green/red assignments |
| **Copy-paste dilution** | 10% watermarked in human doc | z-score diluted; TGRL CP1-10 TPR **0.000** |
| **Translation / round-trip** | Seamless M4T | Surface token change; TGRL Trans TPR 0.222 |
| **Human rewrite** | Adversarial paraphrase study | ICLR 2024: detectable @ ~800 tokens |
| **Self-information targeted** | SIRA, BIRA | Mask high-surprisal (proxy green) tokens → rewrite |
| **Gradient adaptive** | GBDA + surrogate detector | WaterPark: most schemes <10% TPR |
| **Spoofing** | Sadasivan | Query watermarked LM → forge green signature on human toxic text |

### 7.2 Key numbers by source

| Source | Attack | KGW / TGRL result | Notes |
|--------|--------|-------------------|-------|
| **Sadasivan 2023** | PEGASUS paraphrase | Acc 97% → **80%**; green ~58% → ~44% | OPT-1.3B, 100 XSum |
| **Sadasivan 2023** | T5 paraphrase | Acc → **57–64%** | Recursive rounds worse |
| **ICLR 2024 reliability** | Dipper full rewrite | AUC @ T=200: −0.05–0.15; recovers >0.9 @ 600 tokens | Llama-7B watermarked |
| **ICLR 2024 reliability** | GPT-3.5 paraphrase | AUC >0.85 @ T=200; >0.9 @ T=600 | Stronger than 2023 T5 threat model |
| **ICLR 2024 reliability** | Human adversarial | Detectable @ **~800 tokens** avg, FPR 10⁻⁵ | 14 graduate writers |
| **WaterPark 2025** | Clean | TPR **0.993** @ 1% FPR | Qwen2.5-14B generator |
| **WaterPark 2025** | Dipper DP-40 | TPR **0.485** | Primary humanizer proxy |
| **WaterPark 2025** | Copy-paste 10% | TPR **≈0.000** | Provenance dilution |
| **WaterPark 2025** | ChatGPT 1-round | TPR **<0.30** | All 12 schemes |
| **TempParaphraser** | Single pass | Detection **56% → 1.7%** | Agent #24 |
| **Adversarial Paraphrasing** | Guided rewrite | Score **1.000 → 0.131** | Agent #25 |
| **SIRA ICML 2025** | Self-info rewrite | **~100% ASR** | 7 schemes incl. KGW-1; $0.88/M tok |
| **BIRA 2025** | Bias inversion | **>99% evasion** | Beats SIRA on fidelity + ASR |

### 7.3 Debate — optimists vs pessimists

**Optimists (Kirchenbauer 2024, regulatory briefs):**

- Watermarks beat post-hoc detectors under same paraphrase budget.
- Reliability scales with **length**; long documents remain auditable.
- Public detection enables platform-scale moderation without model access.

**Pessimists (WaterPark, SIRA, BIRA, Sadasivan):**

- Paraphrase is not an edge case — it is default editing and every humanizer pipeline.
- Short-form text (tweets, email, cover letters) sits below reliable T; EU exempts <200 tokens anyway.
- Unified 2025 evals: one Dipper pass halved TGRL TPR; SIRA/BIRA near-total removal at commodity cost.
- OpenAI **chose not to ship** Aaronson watermark (99.9% on clean text) citing trivial paraphrase bypass + ~30% user churn (Aug 2024).

**Synthesis for unslop:** Both sides agree on mechanism; they disagree on **operating point**. KGW works on clean, long, unedited model output. It fails the humanizer threat model that unslop implicitly implements when users run `/unslop anti-detector` or cross-model rewrite.

---

## 8. KGW variant family (post-2023)

MarkLLM / WaterPark treat these as KGW **derivatives** (distribution-shift cluster):

| Variant | Paper | Change vs KGW | Robustness note (WaterPark) |
|---------|-------|---------------|----------------------------|
| **TGRL / KGW** | Kirchenbauer 2023 | Baseline text-dep. shift | DP-40 TPR 0.485 |
| **UG (Unigram)** | Zhao 2023 | Context-free partition | DP-40 TPR **0.877** — beats TGRL |
| **UPV** | Liu 2023a | Model-based detection | Low clean TPR 0.40; paraphrase fragile |
| **EWD** | Lu 2024 | Entropy-gated δ on TGRL | Helps typo, not copy-paste |
| **SWEET / AAR** | Lee, Takezawa et al. | Low-entropy skip | Quality↑, detect on high-S only |

Distribution-**transform** alternatives (RDF, Aaronson GO/EXP) trade fidelity for paraphrase survival — different design point, not KGW patches.

---

## 9. Regulatory role (EU AI Act, Aug 2026)

### 9.1 Legal hook

**Article 50(2)** — providers of generative AI must mark synthetic audio, image, video, or **text** in machine-readable format detectable as AI-generated.

| Date | Obligation |
|------|------------|
| **2 Aug 2026** | Art. 50 transparency (incl. user disclosure, deepfake labelling) |
| **2 Dec 2026** | Machine-readable **marking** for generative systems already on market (Digital Omnibus grace) |
| **2 Feb 2027** | Code of Practice signatories: cross-vendor detection interoperability |

### 9.2 How KGW fits

- **Not mandated by name.** Art. 50 requires marking that is "effective, interoperable, robust and reliable as far as technically feasible."
- **De facto reference.** Commission Guidelines (Jul 2026) list watermarks among techniques; academic and open-source compliance paths integrate **inference-time token bias** — KGW is the textbook algorithm (see LLM ethics modules, MarkLLM docs).
- **Code of Practice (text):** Free-form text >**200 tokens** → imperceptible **in-content watermark** required (metadata alone insufficient for flowing prose). Sub-200-token outputs exempt — matches KGW's short-text weakness.
- **Detection access:** Restricted to verified experts (authorities, researchers, media) given false-positive and robustness limits — realistic given KGW paraphrase fragility.

### 9.3 Production vs academic

| Provider | Marking approach | KGW relation |
|----------|------------------|--------------|
| **Google Gemini** | SynthID-Text (shipped) | KGW generalization; WaterPark DP-40 TPR 0.498 |
| **OpenAI ChatGPT** | No public token watermark (Aug 2026) | Aaronson prototype shelved; metadata exploration |
| **Anthropic Claude** | No public cryptographic text watermark (May 2026 surveys) | — |
| **Self-hosted / EU GPAI** | MarkLLM, lm-watermarking, vLLM-Watermark | Direct KGW integration path for Art. 50 |

### 9.4 Compliance implication

Regulators assume marking **at generation**. WaterPark + SIRA imply any downstream **humanization, paraphrase, or paste-into-human-doc** breaks KGW-class marks unless re-applied post-edit. Supply-chain docs must treat humanizers as **provenance risk**, not only academic-integrity risk.

---

## 10. unslop integration

### 10.1 Mechanism overlap

| unslop pass | Effect on KGW |
|-------------|---------------|
| Stock-vocab / AI-ism removal | Token substitutions → new green/red draws |
| Burstiness / sentence-length variance | Changes high-entropy token choices — where watermark lives |
| Cross-model paraphrase (`detector.py` ladder) | Same class as Dipper/SIRA; strips green bias |
| `--surprisal-variance` | Optimizes signals orthogonal to watermark but often co-occur with rewrites |
| Voice-match / anti-detector | Full rewrite → near-complete mark loss at short T |

unslop does **not** implement KGW detection or key-aware stripping. Side effect is statistical, not cryptographic.

### 10.2 Policy boundaries (from Agent #20, #77)

1. **No watermark-stripping mode** — no prompts/docs targeting SynthID/KGW/C2PA removal.
2. **Anti-detector ≠ anti-watermark** — ESL/resume defence, not Art. 50 evasion.
3. **User honesty** — if provenance required, humanize first then mark (or don't humanize).
4. **Citation discipline** — cite WaterPark Table 2 / SIRA for "paraphrase breaks KGW"; don't claim unslop runs watermark evals.

### 10.3 Optional product actions

| Priority | Action |
|----------|--------|
| **P2** | Anti-detector exhaustion message: rewrite may affect embedded provenance marks |
| **P3** | Cross-link KGW/SynthID fragility in research synthesis (no bench fixtures) |
| **—** | Do **not** add KGW detector to `detector.py` — different problem (keyed provenance vs keyless AI-ism) |

---

## 11. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| Default γ, δ (Fig. 1) | 0.25, 2.0 | ICML 2023 |
| Detect from | ~25 tokens | Fig. 1 example (28 green, p≈6×10⁻¹⁴) |
| z threshold → FPR | 4 → ~3×10⁻⁵ | §3.1 |
| OPT-1.3B detect rate | 98.4% @ z=4, 200 tok | §4.1 |
| Sadasivan PEGASUS | 97% → 80% watermark acc | §3.2 Agent #17 |
| ICLR 2024 human paraphrase | Detect @ ~800 tokens | Abstract |
| WaterPark TGRL clean TPR | 0.993 @ 1% FPR | Table 2 |
| WaterPark TGRL DP-40 | 0.485 | Table 2 |
| WaterPark TGRL CP1-10 | ≈0.000 | Table 2 |
| SIRA ASR on KGW | ~100% | ICML 2025 |
| BIRA evasion | >99% | arXiv:2509.23019 |
| EU text marking threshold | >200 tokens | Code of Practice / Orrick Aug 2026 |
| OpenAI ship decision | Not deployed | Verge Aug 2024 |

---

## 12. Open questions

1. **Will EU enforcement accept KGW-class marks knowing SIRA breaks them?** Likely yes for "best effort" at generation, with detection restricted to experts — not proof-grade provenance.
2. **KGW-1 vs SelfHash in production?** Narrower context = simpler audit; SIRA ablation shows smaller k can mean *more* attack robustness in some settings — counterintuitive for deployers.
3. **Post-hoc re-watermarking after humanization?** Technically possible only with another generation pass; not equivalent to preserving original mark.
4. **OpenAI metadata path vs KGW?** C2PA-style signed metadata avoids statistical paraphrase break but dies on copy-paste — Art. 50 CoP mandates **two layers** for online content.
5. **unslop detector feedback vs watermark:** `--detector-feedback` optimizes commercial detector scores; watermark survival is unmonitored — should ethics docs mention both?

---

## 13. Cross-references (sibling agents)

| Agent | Relevance |
|-------|-----------|
| **#17 Sadasivan** | TV bound; first KGW paraphrase numbers; spoofing |
| **#20 WaterPark** | TGRL = KGW; unified attack matrix |
| **#24 TempParaphraser** | 56% → 1.7% watermark detection |
| **#25 Adversarial Paraphrasing** | KGW 1.0 → 0.131 |
| **#31 DIPPER** | Primary paraphrase attack on KGW |
| **#71 SIRA** | Universal removal successor |
| **#72 BIRA** | Bias inversion; >99% on KGW |
| **#75 SynthID** | Production KGW descendant |
| **#76 EU AI Act Art. 50** | Regulatory mandate context |
| **#77 Watermark side-effect ethics** | unslop policy companion |

---

## 14. Bottom line

KGW is the **foundational paper** for LLM text watermarking: green-list logit bias, public z-test detection, ICML 2023 + ICLR 2024 reliability study, official `lm-watermarking` code, TGRL baseline in every 2024–2026 benchmark. It is **not** a durable mark under paraphrase — the same rewrite passes unslop uses for humanization. Regulators cite watermarking generically; practitioners should assume **mark-at-publish after editing**, not mark-at-model-output, unless no rewrite occurs. unslop stays on the human-voice side of that axis with explicit Art. 50 refusal for deliberate provenance stripping.
