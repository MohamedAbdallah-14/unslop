# Agent #50 — Jemama Fidelity vs Perplexity Tradeoff

**Topic:** Jemama & Kumar, *How Well Do LLMs Imitate Human Writing Style?* (IEEE UEMCON 2025, arXiv 2509.24930)  
**Prepared:** August 19, 2026  
**Scope:** Style-fidelity vs statistical-naturalness separation, experimental protocol, related papers, unslop dual-axis architecture  
**Status:** complete

---

## Executive summary

Jemama & Kumar (September 2025, Bucknell / Lewisburg Area HS) is the first paper to **empirically decouple two objectives that humanization tools routinely conflate**:

| Axis | Question | Jemama metric | Human baseline | High-fidelity LLM imitation |
|------|----------|---------------|----------------|----------------------------|
| **Style fidelity** | Does output match the target author's fingerprint? | Distribution-based authorship verifier (TF–IDF char n-grams + all-MiniLM-L6-v2) | — | Up to **99.9%** verifier agreement under text-completion prompting |
| **Statistical naturalness** | Does output have human-like unpredictability? | GPT-2 document perplexity | **μ = 29.5** | **μ = 15.2–16.07** regardless of prompting strategy |

The headline is not a smooth Pareto frontier ("more voice = less detectability"). It is **orthogonality**: a model can nail stylometric imitation and still sit in the trivially-detectable perplexity band. Prompting strategy drives fidelity (few-shot is **23.5×** better than zero-shot; completion reaches near-perfect match) but **does not reliably move perplexity toward human levels**. At perplexity ≤ 20, ~**90%** of LLM essays fall below the threshold vs ~**15%** of human essays.

**Unslop verdict:** Jemama validates unslop's **mode split** — `voice-match` (stylometry fidelity) vs `anti-detector` (surprisal variance / burstiness) — as architecturally correct, not accidental. It also exposes a product gap: no unslop benchmark yet scores **both axes on the same rewrite**. Highest-value follow-up: add a dual-oracle row to `benchmarks/` pairing `stylometry.analyze()` delta against a reference voice sample with `surprisal.py` / DivEye-style variance readings before and after humanization.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | How Well Do LLMs Imitate Human Writing Style? |
| **Authors** | Rebira Jemama (Lewisburg Area High School); Rajesh Kumar (Bucknell University) |
| **Venue** | IEEE UEMCON 2025 (paper accepted; presented at conference) |
| **arXiv** | https://arxiv.org/abs/2509.24930 |
| **arXiv DOI** | https://doi.org/10.48550/arxiv.2509.24930 |
| **IEEE DOI** | https://doi.org/10.1109/UEMCON67449.2025.11267719 |
| **Hugging Face Papers** | https://huggingface.co/papers/2509.24930 |
| **Claimed code repo** | `rajeshjnu2006/writing-style-uemcon2025` *(unavailable as of 2026-08-21 — artifact not public or renamed)* |

**One-line contribution:** A training-free authorship verifier plus controlled LLM imitation study showing that **stylistic fidelity and GPT-2 perplexity-based detectability are separable objectives** — high imitation accuracy does not imply human-like statistical unpredictability.

---

## 2. Mechanism — distribution-based authorship verifier

### 2.1 Feature stack

Two complementary representations, fused at distance-comparison time:

1. **TF–IDF character 3–5 grams** — top 10,000 n-grams from corpus; sparse 10⁴-dim vector. Captures punctuation habits, orthographic tics, surface regularities (PAN-competition lineage).
2. **all-MiniLM-L6-v2 embeddings** — mean-pooled 384-dim dense vector. Captures syntax preferences, lexical rhythm, function-word patterns.

Pairwise **cosine distance** (chosen over Euclidean — sharper same/different separation across 50–1000+ word lengths).

### 2.2 Nonparametric decision rule

No learned classifier, no hand-tuned threshold:

- Build empirical distance distributions **D⁺** (same-author pairs) and **D⁻** (different-author pairs) from 100k construction pairs.
- For test pair distance *d*\\*: compare *S* = P(δ ∈ D⁺ | δ > d\\*) vs *D* = P(δ ∈ D⁻ | δ < d\\*).
- Predict same-author iff *S* > *D*; confidence = |*S* − *D*| / max(*S*, *D*).

Construction time < 5 seconds; **91.8%** faster and **59%** less memory than parameterized Siamese baseline (which hit only **57%** accuracy on handcrafted 16 spaCy features).

### 2.3 Performance

| Setting | Accuracy | ROC AUC | F1 | Notes |
|---------|----------|---------|-----|-------|
| Same-domain (IvyPanda) | **97.49%** | 0.997 | 0.975 | Symmetric FP/FN (~628 each) |
| Cross-domain (EssayForum) | **94.48%** | 0.981 | 0.870 | FN-heavy (1,349 vs 113 FP) — genre drift |

---

## 3. Style imitation protocol

### 3.1 Data

| Corpus | URL | Role |
|--------|-----|------|
| **IvyPanda Essays** | https://huggingface.co/datasets/qwedsacf/ivypanda-essays | Primary — ~95k filtered academic essays (mean 1,561 words) |
| **EssayForum** | https://huggingface.co/datasets/nid989/EssayFroum-Dataset | Cross-domain — conversational essays |

Preprocessing: >500 words, <10% numeric chars, <5% misspellings (pyspellchecker), no token >10% frequency, paratext stripped. Each essay split into two non-adjacent 500-word blocks for pair construction.

### 3.2 Models tested

Five open-weight LLMs, three families:

- Llama-3.3-70B-Instruct — https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
- Llama-4-Scout-17B-16E-Instruct
- Mixtral-8x7B — https://arxiv.org/abs/2401.04088
- Qwen2.5-14B-Instruct / Qwen2.5-32B-Instruct — https://arxiv.org/abs/2410.09583

System prompt preamble on all runs: *"Output only the requested content. No prefaces, disclaimers, or explanations."*

### 3.3 Four prompting conditions

| Condition | Setup | Style fidelity (verifier accuracy) |
|-----------|-------|-----------------------------------|
| **Zero-shot** | Statistical style profile only (syntax counts, punctuation ratios, bigrams); generate 300–500 words on any topic | **< 7%** all models |
| **One-shot** | Single longest paragraph anchor; different topic | **67.6%–94.7%** (high variance) |
| **Few-shot** | Two longest paragraphs as anchors | **91%–100%** |
| **Completion** | Continue second half of human essay from first half | **96.9%–99.9%** (4/5 models at 99.9%) |

**Key finding:** Prompting strategy dominates model size/architecture for fidelity. Zero-shot statistical summaries are useless anchors. Completion is forensic-dangerous — once a human prefix establishes the stylistic manifold, continuation is nearly indistinguishable from the author by stylometric means.

---

## 4. The fidelity–perplexity split (core result)

### 4.1 Perplexity measurement

- Scorer: **GPT-2** (classic zero-shot AI-text signal lineage — Jelinek et al. 1977; Brown et al. 2020 few-shot LM paper).
- Unit: document-level perplexity on IvyPanda essays, n = 1,000 held-out authors per condition.

### 4.2 Headline numbers

| Population | Mean PPL (μ) | At threshold ≤ 20 |
|------------|--------------|-------------------|
| Human essays | **29.5** | ~**10–15%** |
| LLM outputs (all conditions pooled) | **15.2–16.07** | ~**90%** |

Perplexity by prompting strategy (Llama variants, Table IV):

| Strategy | Llama-3.3-70B | Llama-4-Scout-17B |
|----------|---------------|-------------------|
| Zero-shot | 8.90 | 10.46 |
| One-shot | 17.45 | 19.87 |
| Few-shot | 16.43 | 15.16 |

Human baseline: **29.5** throughout.

### 4.3 What "separable" means (and doesn't)

**Means:**
- A text can score **99.9% style-match** on the verifier while remaining at **PPL ≈ 15** — roughly half the human mean.
- Raising fidelity (zero → few-shot → completion) does **not** monotonically raise perplexity toward human levels.
- Detectability and fidelity show **no clear correlation** in their scatter — optimizing one does not automatically optimize the other.

**Does not mean:**
- Human-like perplexity is impossible for LLMs (one-shot Llama-3.3 hits **17.45**, closer to human than pooled AI mean — still below 29.5).
- Perplexity alone is sufficient for detection in 2026 (DivEye, Binoculars, PHD, and ensemble commercial detectors use additional signals — see §6).
- Reader-perceived "naturalness" was measured — only algorithmic perplexity and stylometric verification.

### 4.4 Interpretation for humanization

Traditional humanizer marketing collapses three distinct goals:

1. **Remove AI slop** (stock vocab, hedging, uniform rhythm) — unslop `balanced`/`full`
2. **Match a voice** (author fingerprint) — unslop `voice-match`
3. **Evade detectors** (statistical human-likeness) — unslop `anti-detector`

Jemama proves goals **2** and **3** require **independent optimization targets and independent evaluation oracles**. A rewrite that "sounds like you" (few-shot imitation succeeds) can still flag as AI on perplexity-only screening. Conversely, perturbing token predictability to raise PPL may damage stylometric fidelity — the paper doesn't test adversarial humanizers, but GradEscape/DIPPER literature shows fidelity–evasion tradeoffs exist on a *different* axis (semantic ROUGE vs detector score).

---

## 5. Related work — how Jemama fits the landscape

### 5.1 Same-month companion: Catch Me If You Can (Wang et al., EMNLP 2025 Findings)

| | Jemama 2025 | Catch Me 2025 |
|---|-------------|---------------|
| **arXiv** | https://arxiv.org/abs/2509.24930 | https://arxiv.org/abs/2509.14543 |
| **GitHub** | *(claimed, 404)* | https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation |
| **Population** | Academic essay authors (IvyPanda) | 400+ everyday authors, news/email/forums/blogs |
| **Models** | Open-weight (Llama, Qwen, Mixtral) | Frontier closed APIs (GPT-4o, Gemini-2.0-Flash, DeepSeek-V3, Llama-4-Maverick, etc.) |
| **Fidelity verdict** | Completion prompting → **99.9%** verifier match | All frontier models **fail** implicit personal style imitation |
| **Detection axis** | GPT-2 perplexity explicitly measured | AI detection as one of four ensemble metrics |

**Reconciliation:** Jemama tests **explicit exemplar-based imitation on homogeneous academic prose** under ideal conditions (completion = strongest possible anchor). Catch Me tests **implicit personalization of everyday authors across informal domains** with summary-conditioned generation — a harder, more realistic product scenario. Jemama reports the **23.5×** few-shot multiplier; Catch Me reports smaller, domain-specific few-shot gains. unslop's `voice-match` skill already cites Catch Me for the "prompt-only voice cloning fails" limitation; Jemama adds the orthogonal perplexity warning for the cases where stylometry *does* match.

### 5.2 Two paradigms of LLM detection (Bevendorff et al., ACL 2025 Findings)

- **Paper:** https://arxiv.org/abs/2505.06285 (ACL 2025 Findings)
- **Claim:** LLM detection is better framed as **authorship verification** (human vs machine boundary) than multi-class **authorship attribution** (which of N authors?).

Jemama operationalizes exactly this convergence — same verifier pipeline for human–human and human–LLM pairs, then separate perplexity pass for the machine boundary.

### 5.3 Perplexity detection lineage

| Paper | URL | Relevance |
|-------|-----|-----------|
| DetectGPT (Mitchell et al., ICML 2023) | https://arxiv.org/abs/2301.11305 | Curvature beyond raw PPL — Jemama uses simpler GPT-2 PPL only |
| "Influence of perplexity score in detection" (Alberto et al., NLPAICS 2024) | cited in Jemama refs | Empirical PPL threshold behavior |
| DivEye (Ganapathi et al., TMLR 2026) | https://arxiv.org/abs/2509.18880 | **Surprisal variance**, not mean PPL, survives paraphrase — unslop ships this via `surprisal.py` |
| Binoculars (Hans et al., ICML 2024) | https://arxiv.org/abs/2401.12070 | Cross-model perplexity ratio — stronger than single-model PPL |
| Tulchinskii PHD (NeurIPS 2023) | https://arxiv.org/abs/2306.04723 | Intrinsic dimension — third orthogonal geometry signal |

Jemama's PPL analysis is deliberately **simple and interpretable** — useful as a floor, not a ceiling, for what "statistical naturalness" means in 2026.

### 5.4 Humanizers that explicitly trade fidelity vs evasion

| System | URL | Tradeoff mechanism |
|--------|-----|-------------------|
| GradEscape (USENIX Security 2025) | https://arxiv.org/abs/2506.08188 | α/β weights on semantic fidelity vs detector loss — see Agent #29 memo |
| DIPPER (Krishna et al., NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Diversity vs fidelity knobs on paraphrase |
| TempParaphraser (EMNLP 2025) | https://arxiv.org/abs/2410.09583 | Temperature simulation — breaks uniform LM smoothness |
| DAMAGE audit (Masrour et al., COLING 2025) | https://arxiv.org/abs/2501.03437 | Commercial humanizers degrade semantics while evading detectors |

None of these papers use Jemama's **dual-oracle** framing (stylometric verifier + PPL), but all assume some fidelity–evasion tension. Jemama shows the tension is **worse than assumed** — you can win on fidelity without touching detectability.

### 5.5 Stylometric homogenization context

| Paper | URL | Why it matters |
|-------|-----|--------------|
| Interpretable stylistic variation (Apr 2026) | https://arxiv.org/abs/2604.14111 | RLHF pushes models to same stylistic attractor — "AI voice" is model-agnostic |
| How LLMs Distort Our Written Language (Mar 2026) | https://arxiv.org/abs/2603.18161 | ~70% neutralization on contested topics after LLM editing |
| Benchmark of stylistic variation (Kasner et al., 2025) | https://arxiv.org/abs/2509.10179 | Complements Jemama — how much variation LLMs produce under prompting |

Jemama's fidelity axis measures **distance to a specific human author**, not distance from the generic RLHF cluster. unslop's slop removal attacks the generic cluster; voice-match attacks author distance; anti-detector attacks statistical smoothness.

---

## 6. Critiques, limitations, and debate

### 6.1 Methodological limits (paper acknowledges)

- **English academic/conversational essays only** — creative, technical, multilingual registers untested.
- **GPT-2 perplexity only** — dated scorer; modern detectors (GPTZero v6 predictability cones, DivEye variance, ensemble RoBERTa) may show different separation.
- **Retrospective verifier** — adversarial paraphrase / humanizer post-processing not in loop (GradEscape, DIPPER, unslop `--detector-feedback` untested against this verifier).
- **IvyPanda authorship** — essays may be heterogeneous in true authorship; student essay mill corpus, not verified single-author longitudinal data.
- **Code unavailable** — reproducibility risk; IEEE DOI exists but GitHub 404.

### 6.2 Community / secondary coverage

- Hugging Face Papers listing: https://huggingface.co/papers/2509.24930
- Moonlight literature review (secondary): https://www.themoonlight.io/en/review/how-well-do-llms-imitate-human-writing-style
- No major HN/Reddit thread found (Aug 2026 search) — paper is recent and venue is IEEE conference, not arXiv-first viral.

### 6.3 Supporters vs skeptics (inferred from method choices)

| Supporters would say | Skeptics would say |
|---------------------|-------------------|
| Clean separation of two conflated objectives | PPL gap may shrink with better detectors / newer LMs |
| Training-free verifier is cheap and interpretable | MiniLM + char n-grams miss discourse-level voice |
| Completion result is forensic wake-up call | Completion is not the humanizer use-case — rewrite-from-scratch is harder |
| 97.5% verifier accuracy rivals supervised PAN baselines | IvyPanda ≠ real-world author ground truth |

---

## 7. Unslop relevance — detailed integration map

### 7.1 Current architecture already splits the axes

| Jemama axis | unslop mode / module | What it optimizes |
|-------------|---------------------|-------------------|
| Style fidelity | `voice-match` skill + `stylometry.py` | Sentence-length μ/σ, contraction rate, em-dash rate, TTR, fragment rate, DivEye **proxies** (`sentence_length_cv`, `word_length_stdev`) |
| Statistical naturalness | `anti-detector` skill + `surprisal.py` + `structural.py` + `soul.py` | Surprisal variance (DivEye), burstiness σ ≥ 6, contraction lift, lexical target gaps |

**Gap Jemama exposes:** unslop has **no single pass** that jointly optimizes both with a Pareto-aware controller. Modes are user-selected, not auto-balanced. A user running `voice-match` may get stylometric convergence while surprisal stays flat — exactly Jemama's failure mode.

### 7.2 Python package touchpoints

| File | Jemama connection |
|------|-------------------|
| `unslop/scripts/stylometry.py` | Implements fidelity-side signals; `StyleProfile.delta()` is the right shape for verifier-distance reporting |
| `unslop/scripts/surprisal.py` | Real DivEye reading — **stronger than GPT-2 mean PPL** for the naturalness axis |
| `unslop/scripts/humanize.py` | `anti-detector` runs lexical_targets + structural + soul; `voice-match` is LLM-skill-only (no `--intensity voice-match` in Python CLI — skill-layer only) |
| `unslop/scripts/detector.py` | Optional RoBERTa feedback — third axis (classifier score), not stylometric fidelity |
| `unslop/scripts/benchmark.py` | **Missing dual-oracle row** — should report stylometry delta + surprisal delta on same sample |

### 7.3 Skill-layer citations already partially aligned

`skills/unslop/SKILL.md`:
- `voice-match` cites Catch Me (2509.14543) for imitation limits — **add Jemama (2509.24930)** for the perplexity orthogonality caveat.
- `anti-detector` cites DivEye surprisal variance — Jemama confirms mean PPL alone is insufficient but directionally consistent.

### 7.4 Recommended unslop actions (priority order)

1. **Benchmark dual-oracle** — For each humanize sample: (a) stylometry delta vs user voice sample if provided; (b) surprisal_stdev before/after. Report Jemama-style separation on unslop outputs. No invented thresholds — run on `benchmarks/` corpus first.
2. **Document the tradeoff in README / research docs** — "Sounds like you" ≠ "passes detectors." Link IEEE UEMCON paper.
3. **Optional `--dual-objective` flag (future)** — When voice sample + anti-detector both requested, run stylometry-targeted rewrite first, then surprisal pass; abort or warn if fidelity delta regresses > X%. Needs measured X from bench, not guessed.
4. **Do not merge modes blindly** — Jemama warns that optimizing fidelity via exemplar completion (strongest anchor) doesn't fix PPL. Chaining voice-match → anti-detector may be necessary, with fidelity re-check after anti-detector structural perturbation.
5. **Cite in AGENTS.md / Cat-10 synthesis** — Already in `docs/research/10-style-transfer-voice/`; ensure `AGENT-MANIFEST-100.md` row 50 → this memo.

### 7.5 What unslop should NOT do

- **Do not claim** voice-match improves detector evasion — Jemama directly contradicts this for stylometric success cases.
- **Do not use mean GPT-2 PPL as sole anti-detector metric** — DivEye variance is the better aligned signal (Agent #1 / `surprisal.py`); Jemama's PPL is pedagogically useful, technically dated.
- **Do not build a GradEscape-style joint trainer** — out of scope; unslop stays prompt/regex-first with optional local scorer feedback.

---

## 8. Open questions for unslop research (post-Jemama)

1. Does unslop `anti-detector` move **surprisal_stdev** toward human band without destroying voice-match stylometry delta?
2. Does cross-model second pass (recommended in anti-detector procedure) improve **both** axes or only naturalness?
3. Where is the empirical Pareto surface for unslop intensities (`balanced` → `full` → `anti-detector`) on IvyPanda-style academic prose?
4. Can MiniLM embedding distance (Jemama verifier analogue) be added as optional fidelity oracle without API calls? (`sentence-transformers` is heavy — may belong in bench only.)
5. How does Jemama's completion result inform **co-writing detection** product positioning vs rewrite humanization?

---

## 9. Primary source URL index

| Resource | URL |
|----------|-----|
| **Jemama arXiv** | https://arxiv.org/abs/2509.24930 |
| **Jemama arXiv DOI** | https://doi.org/10.48550/arxiv.2509.24930 |
| **Jemama IEEE** | https://doi.org/10.1109/UEMCON67449.2025.11267719 |
| **IvyPanda dataset** | https://huggingface.co/datasets/qwedsacf/ivypanda-essays |
| **EssayForum dataset** | https://huggingface.co/datasets/nid989/EssayFroum-Dataset |
| **all-MiniLM-L6-v2** | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| **Catch Me If You Can** | https://arxiv.org/abs/2509.14543 |
| **Catch Me GitHub** | https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation |
| **Bevendorff two paradigms (ACL 2025)** | https://arxiv.org/abs/2505.06285 |
| **DivEye / surprisal variance** | https://arxiv.org/abs/2509.18880 |
| **IBM DivEye code** | https://github.com/IBM/diveye |
| **DetectGPT** | https://arxiv.org/abs/2301.11305 |
| **Binoculars** | https://arxiv.org/abs/2401.12070 |
| **PHD (Tulchinskii)** | https://arxiv.org/abs/2306.04723 |
| **GradEscape** | https://arxiv.org/abs/2506.08188 |
| **DAMAGE audit** | https://arxiv.org/abs/2501.03437 |
| **LLM authorship survey (Huang et al., SIGKDD 2025)** | https://arxiv.org/abs/2408.08946 |
| **Living paper list** | https://llm-authorship.github.io/ |
| **PAN authorship verification** | https://doi.org/10.5281/zenodo.3716402 |
| **unslop stylometry module** | `unslop/scripts/stylometry.py` |
| **unslop surprisal module** | `unslop/scripts/surprisal.py` |
| **Cat-10 synthesis (repo)** | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |

---

## 10. Bottom line

Jemama 2025 gives unslop a **clean experimental license** for two things it already does separately: measure voice (`stylometry`) and measure statistical human-likeness (`surprisal`). The paper's numbers — **PPL 29.5 vs 15.2**, **99.9% style match under completion**, **no fidelity–PPL correlation** — should appear anywhere unslop claims "humanized" without qualification.

The product implication is blunt: **ship dual metrics or stop implying one rewrite solves both problems.** Voice-match and anti-detector are complementary modes, not interchangeable intensities of the same knob.
