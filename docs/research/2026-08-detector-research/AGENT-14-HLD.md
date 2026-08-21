# Agent #14 — HLD: Approximate Hierarchical Linguistic Distribution Modeling

**Prepared:** 2026-08-19  
**Agent:** unslop deep research sub-agent #14  
**Topic:** ICLR 2026 poster — 4-level n-gram + semantic KDE detector vs stock-vocab humanization  
**Status:** Complete

---

## Executive summary

HLD-Detector (Guo et al., ICLR 2026) is a supervised-but-interpretable detector that stacks **four Bayesian log-likelihood-ratio features** — word n-grams, POS n-grams, dependency n-grams, and semantic KDE retrieval — then aggregates them with XGBoost. On DetectRL it reports **99.12% / 99.60% AUROC** (multi-LLM / multi-domain) and **97.04% AUROC under paraphrase attacks** (DIPPER, back-translation, LLM polish), while zero-shot baselines collapse.

For unslop, HLD is the clearest 2026 proof that **stock-vocab stripping is Signal 1 only**. Paraphrase defeats shallow lexical swaps; HLD's syntactic and semantic layers keep scoring. unslop has no POS/dependency modeling anywhere in `humanize.py` — only regex lexical rules, coarse structural passes (`structural.py`), and contraction injection (`soul.py`). That is exactly the attack surface HLD is built to read.

**Code status:** GitHub repo exists but is a **stub** (README title only, 0 stars, no implementation as of 2026-08-19). Treat numbers as paper-reported until code ships.

---

## Paper identity

| Field | Value |
|-------|-------|
| Title | HLD: Approximate Hierarchical Linguistic Distribution Modeling for LLM-Generated Text Detection |
| Venue | ICLR 2026 (Poster) |
| Poster session | Thu, Apr 23, 2026, 11:15 AM – 1:45 PM PDT |
| Authors | Rui Guo, Weibin Zeng, Fuzhang Wu, Yan Kong, Sicheng Shen, Yanjun Wu, Weiming Dong |
| Affiliation | Northeast Forestry University (inferred from `nefugr` GitHub org) |
| License | CC BY 4.0 (OpenReview) |

---

## Method — four layers, one pipeline

HLD replaces proxy-LLM zero-shot detectors (DetectGPT, Fast-DetectGPT, Binoculars) with **offline n-gram libraries** estimated from small human vs machine corpora. No LLM calls at inference.

### Architecture

```
Input text X
  ├─ φ_word      → z_word     (word n-gram LLR)
  ├─ φ_pos       → z_pos      (POS-tag n-gram LLR)
  ├─ φ_dep       → z_dep      (dependency-label n-gram LLR)
  └─ φ_semantic  → z_semantic (KDE retrieval LLR on embedding pairs)
         ↓
    Z = [z_word, z_pos, z_dep, z_semantic]  ∈ ℝ⁴
         ↓
    XGBoost f_θ(Z) → P(MGT | Z)
```

### 1. Bayesian likelihood ratio + Markov truncation

Detection framed as comparing human-written (HWT) vs machine-generated (MGT) conditional distributions. Full chain rule is intractable; HLD truncates context to length **k** (Markov assumption):

\[
P(f_i \mid Y, f_{<i}) \approx P(f_i \mid Y, f_{i-k:i-1})
\]

Per-token normalized log-likelihood ratio:

\[
z = \frac{1}{n}\sum_{i=1}^{n}\log\frac{\hat P_{\text{HWT}}(f_i \mid f_{i-k:i-1})}{\hat P_{\text{MGT}}(f_i \mid f_{i-k:i-1})}
\]

**Why it matters:** Distributional comparison without needing the source LLM's logits. Cheap lookup vs expensive proxy-model forward passes.

### 2. Lexical + syntactic n-grams

- **Word level:** Standard n-gram LM with additive smoothing and backoff when context counts are zero (Fast-DetectGPT insight — humans and LLMs diverge in word preference given context — but estimated statistically, not via a live proxy model).
- **Syntactic level:** Text mapped to **spaCy POS sequences** and **dependency-label sequences**; same n-gram + smoothing machinery applied.
- **Ablation signal:** Removing the word layer hurts **cross-domain generalization most** (Review domain AUROC 91.45% → 84.43%). POS, dependency, and semantic layers also drop performance when removed — all four are load-bearing.

### 3. Semantic KDE (paraphrase defense)

Lexical and syntactic features break under synonym swap and paraphrase. Semantic layer adapts **Dipper-style retrieval** to continuous space:

1. Pre-trained encoder builds **context-embedding → target-embedding** pairs.
2. Offline libraries `D_HWT^semantic`, `D_MGT^semantic`.
3. At detection: retrieve **M nearest context neighbors**, interpolate target probability via law of total probability.
4. Neighbor weights from cosine similarity through softmax kernel (τ_ctx = 0.1).

Surface words can change; **semantic trajectory** in embedding space stays machine-like. This is the mechanism behind paraphrase robustness.

### 4. XGBoost aggregation

Four LLRs are **not** naively summed. XGBoost learns scenario-dependent weighting (e.g., syntactic/semantic layers weighted higher in cross-domain settings).

### External dependencies (paper)

| Component | Tool |
|-----------|------|
| POS / dependency | spaCy |
| Semantic embeddings | Pre-trained encoder (paper does not name a single checkpoint in public summaries) |
| Classifier | XGBoost |
| Benchmark | DetectRL |

---

## Results on DetectRL

**DetectRL** ([Wu et al., 2024](https://arxiv.org/abs/2410.23746)) — multi-LLM, multi-domain, adversarial attacks (prompt, paraphrase, perturbation, data mixing). Code: [NLP2CT/DetectRL](https://github.com/NLP2CT/DetectRL).

### Main AUROC (%, DetectRL)

| Detector | Multi-LLM avg | Multi-domain avg | Type |
|----------|---------------|------------------|------|
| Binoculars* | 83.31 | 86.45 | Zero-shot |
| RADAR | 91.91 | 90.95 | Supervised |
| RAIDAR | 88.48 | 92.61 | Supervised |
| DPIC | 96.75 | 97.54 | Supervised |
| RoBERTa-base | 98.24 | 98.94 | Supervised |
| **HLD (Ours)** | **99.12** | **99.60** | Hierarchical LLR + XGBoost |

*Zero-shot baselines average ~60% with heavy per-model variance (e.g., DetectGPT on PaLM-2 reported ~26.72% in paper note).

### Robustness (AUROC %)

| Scenario | Second-best | HLD |
|----------|-------------|-----|
| Cross-domain (train Arxiv → avg) | 81.38 (RoBERTa) | **86.61** |
| Cross-model (train GPT-3.5 → avg) | 91.93 (RoBERTa) | **92.46** |
| Adversarial attack avg | 93.03 (DPIC) | **97.85** |
| **Paraphrase attack** | Significant drop (all baselines) | **97.04** |

**Paraphrase attack setup (DetectRL):** DIPPER paraphraser, Google Translate back-translation, LLM polishing — meaning-preserving rewrites. DetectRL itself reports zero-shot detectors lose ~15.67% AUROC average under paraphrase; HLD's 97.04% is the headline robustness number.

### Ablation (train Arxiv, test Review)

| Config | Review AUROC |
|--------|--------------|
| Full HLD | 91.45% |
| − Word | 84.43% |
| − POS / − Dep / − Semantic | Each decreases (exact deltas in paper PDF) |

---

## HLD vs stock-vocab stripping (unslop's core pass)

### What unslop does today

| Layer | Module | What it touches | HLD equivalent |
|-------|--------|-----------------|----------------|
| Lexical AI-isms | `humanize.py` `STOCK_VOCAB`, sycophancy, hedging, etc. | ~100 regex families, synonym-level swaps | **z_word** — partially addressed |
| Sentence-length variance | `structural.py` | Split/merge by word count | Surface structure only; **not POS/dep n-grams** |
| Contraction injection | `soul.py` | Shifts token n-grams (`don't` vs `do not`) | Narrow **z_word** lever |
| Stylometric proxies | `stylometry.py` | σ sentence length, TTR, latinate ratio, passive approx | Weak proxies; **no spaCy sequences** |
| Surprisal dynamics | `surprisal.py` | DivEye-style variance (optional LM) | Partial overlap with **z_semantic** intent |
| Detector feedback | `detector.py` | TMR / Desklib RoBERTa scorers | Different family from HLD |

### Asymmetry table

| Evasion move | Stock-vocab strip | HLD response |
|--------------|-------------------|--------------|
| Replace "delve" → "explore" | ✅ Fixed | Word n-gram may shift slightly |
| DIPPER paraphrase (lexical diversity) | ⚠️ Rules may miss new phrasing | Word layer weakens; **POS/dep/semantic hold** |
| Synonym swap preserving syntax | ❌ No structural change | Syntactic n-grams unchanged → still flagged |
| LLM polish (same meaning, new surface) | ❌ | Semantic KDE still matches MGT library |
| Contraction injection only | ⚠️ ~0.0–0.2 pp TMR on fixtures (documented) | Shifts word n-grams; **does not rewrite POS/dep patterns** |

### Key quote from unslop's own codebase

`soul.py` already states the problem HLD exploits:

> Token-level detectors read the distributional fingerprint, not the offensive vocabulary list.

HLD makes that fingerprint **explicit and hierarchical**: word preference + syntactic habit + semantic neighborhood.

### Relation to UPDATE-PLAN five-signal stack

HLD maps cleanly onto the August 2026 stack:

```
Signal 1: Lexical AI-isms        → z_word      → unslop ✅ (humanize.py)
Signal 2: Burstiness             → partial z_word / structural → unslop ⚠️
Signal 3: Surprisal variance     → related to z_semantic → unslop ⚠️ (measure only)
Signal 4: Late-stage stability   → not HLD's focus → unslop ❌
Signal 5: Predictability cones   → not HLD's focus → unslop ❌
         POS/dependency patterns → z_pos, z_dep  → unslop ❌ (THE GAP)
```

HLD proves that **Signals 1 alone lose under paraphrase**; unslop's `subtle` mode (stock vocab only) is the worst-case evasion target for a hierarchical detector.

---

## unslop integration — POS/syntax layer gap

### Current state (verified in repo)

- **No spaCy, no POS tagging, no dependency parsing** in `unslop/scripts/`.
- `grep POS|spacy|dependency` across `unslop/scripts/` hits only `_GENERIC_POSITIVE_*` regex names in `validate.py` — not part-of-speech tagging.
- `structural.py` splits long sentences at punctuation boundaries; it does **not** vary syntactic templates (e.g., breaking repeated `NN-VBZ-NP` openers).
- `stylometry.py` `passive_voice_approx` is a regex heuristic, not a dep-parse passive detector.

### What HLD implies unslop should add (deterministic, preservation-safe)

**Phase 2.5 — Syntactic diversity pass (new module, e.g. `syntax.py`):**

1. **POS bigram/trigram entropy audit** — flag paragraphs where >60% sentences share the same POS-initial pattern (e.g., `DT-NN-VBZ` "The X is…").
2. **Dependency-openers diversity** — detect repeated `nsubj → ROOT → dobj` skeletons in bullet lists; merge or restructure (extends `structural.py` logic with parse trees).
3. **Safe rewrite operators** (preservation contract):
   - Fronted adverbial ↔ end placement
   - Active ↔ passive where `_protect` blocks aren't involved
   - Subordinate clause reordering at safe boundaries (extend `_SPLIT_CANDIDATES`)
4. **Measurement hook** — `stylometry.py` gains optional `pos_trigram_entropy`, `dep_bigram_jsd_vs_baseline` when spaCy available; falls back gracefully (match `surprisal.py` lazy-import pattern).

**Anti-detector feedback:**

- Add HLD to `detector_bench.py` ensemble **when code releases** (alongside TMR, Desklib).
- Until then, use **POS n-gram distance to human baseline** as a cheap proxy target in `lexical_targets.py` / new `syntax_targets.py`.

**LLM mode prompt additions:**

- Explicit instruction: "Vary syntactic openers — do not start three consecutive sentences with the same POS pattern."
- Cross-model paraphrase remains the strongest lever for semantic KDE (HLD's deepest layer).

### What NOT to do

- Do not claim deterministic regex can fully evade HLD — paper's whole point is hierarchical stacking beats single-layer humanization.
- Do not add spaCy as a hard dependency for core CLI — optional, like torch in `surprisal.py`.
- Do not optimize solely against TMR; HLD represents a **different feature family** (interpretable n-grams vs RoBERTa hidden states).

---

## Community & code status

### GitHub: [nefugr/HLD-Detector](https://github.com/nefugr/HLD-Detector)

| Metric | Value (2026-08-19) |
|--------|---------------------|
| Stars | 0 |
| Forks | 0 |
| Created | 2026-02-09 |
| Last push | 2026-02-09 |
| Contents | `README.md` only (`# HLD-Detector`) |
| Commits | 1 ("Initial commit") |
| License | None declared |
| Issues / PRs | 0 |
| CI / tests | None |

**Assessment:** Placeholder repo. No reproducible implementation, no DetectRL eval script, no model weights. Paper note ([papernotes.org](https://en.papernotes.org/ICLR2026/aigc_detection/hld_approximate_hierarchical_linguistic_distribution_modeling_for_llm-generated_/)) is currently the best public method summary besides OpenReview abstract.

### Community uptake

- ICLR 2026 poster acceptance — academic visibility, not product deployment.
- No HN/Reddit threads found in search (Aug 2026).
- No PyPI package, no HuggingFace model card.
- Related concurrent work: DMAP (ICLR 2026), Learn-to-Distance (ICLR 2026), KatFishNet (ACL 2025 — linguistic features for Korean).

### Critic / supporter framing

**Supporters would say:** Interpretable features, no proxy LLM at inference, SOTA on DetectRL, paraphrase robustness validates hierarchical design.

**Skeptics would say:** Single benchmark (DetectRL), offline corpus representativeness, spaCy/encoder toolchain dependency, Markov truncation loses long-range structure, stub repo prevents verification, XGBoost reintroduces a supervised black box on top of interpretable LLRs.

---

## Limitations (paper + our read)

1. **DetectRL-only evaluation** in public summaries — cross-benchmark (RAID, MGTBench, TH-Bench) not yet shown.
2. **Corpus drift** — libraries built from specific HWT/MGT mixes; new models (GPT-5, DeepSeek-R1/V3, Claude-3.5 mentioned in paper note) may shift distributions.
3. **Toolchain propagation** — spaCy parse errors and encoder choice affect z_pos, z_dep, z_semantic.
4. **Markov order k** — trades compute for long-range dependency capture; adversarial long-range consistency evasion possible.
5. **Non-reproducible today** — stub GitHub.

---

## Recommended unslop actions

| Priority | Action | Effort |
|----------|--------|--------|
| P0 | Document HLD in `docs/research/05-ai-text-detection-and-evasion/` — hierarchical n-gram + KDE as 2026 SOTA on DetectRL | S |
| P0 | Add POS/dep gap to `UPDATE-PLAN-2026-08.md` five-signal stack (explicit z_pos, z_dep row) | S |
| P1 | Spike `syntax.py` with optional spaCy — POS trigram entropy + safe opener diversification | M |
| P1 | Watch `nefugr/HLD-Detector` for code drop; add to `fetch_detectors.py` / `detector_bench.py` | S |
| P2 | Human POS/dep baseline corpus in `benchmarks/fixtures/` for n-gram distance targets | M |
| P2 | LLM anti-detector prompt: syntactic diversity + cross-model (semantic KDE evasion) | S |

---

## URL reference

| Resource | URL |
|----------|-----|
| OpenReview | https://openreview.net/forum?id=l9mqzHROGu |
| ICLR 2026 poster page | https://iclr.cc/virtual/2026/poster/10007709 |
| ML Anthology | https://mlanthology.org/iclr/2026/guo2026iclr-hld/ |
| GitHub (stub) | https://github.com/nefugr/HLD-Detector |
| Paper note (method detail) | https://en.papernotes.org/ICLR2026/aigc_detection/hld_approximate_hierarchical_linguistic_distribution_modeling_for_llm-generated_/ |
| DetectRL benchmark paper | https://arxiv.org/abs/2410.23746 |
| DetectRL code | https://github.com/NLP2CT/DetectRL |
| DetectRL OpenReview | https://openreview.net/forum?id=ZGMkOikEyv |
| DIPPER (semantic retrieval lineage) | https://arxiv.org/abs/2303.13408 |
| Fast-DetectGPT (word-preference lineage) | https://arxiv.org/abs/2305.18440 |

---

## BibTeX

```bibtex
@inproceedings{guo2026hld,
  title     = {{HLD: Approximate Hierarchical Linguistic Distribution Modeling for LLM-Generated Text Detection}},
  author    = {Guo, Rui and Zeng, Weibin and Wu, Fuzhang and Kong, Yan and Shen, Sicheng and Wu, Yanjun and Dong, Weiming},
  booktitle = {International Conference on Learning Representations},
  year      = {2026},
  url       = {https://openreview.net/forum?id=l9mqzHROGu}
}

@inproceedings{wu2024detectrl,
  title     = {{DetectRL: Benchmarking LLM-Generated Text Detection in Real-World Scenarios}},
  author    = {Wu, Junchao and others},
  booktitle = {NeurIPS Datasets and Benchmarks Track},
  year      = {2024},
  url       = {https://arxiv.org/abs/2410.23746}
}
```

---

## Agent manifest update

| # | Topic | Status |
|---|-------|--------|
| 14 | HLD hierarchical n-gram detector | **complete** → this memo |

---

*Sub-agent #14 deliverable. Feeds `UPDATE-PLAN-2026-08.md` Part 1 (detection papers) and Part 3 (POS/syntax gap).*
