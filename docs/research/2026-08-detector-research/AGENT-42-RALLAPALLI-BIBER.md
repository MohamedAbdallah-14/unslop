# Agent #42 — Rallapalli Biber Stylometry / RLHF Homogenization

**Topic:** Register-level stylometry for AI detection; instruction-tuning homogenization  
**Primary paper:** Rallapalli et al., *Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies* (arXiv:2604.14111, April 2026)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Rallapalli et al. (CMU SEI / Statistics) apply Douglas Biber's **67 lexicogrammatical register features** to the RAID benchmark — 11 LLMs, 8 genres, 4 decoding strategies, ~468k non-adversarial samples. The headline hierarchy is:

**genre > model identity > decoding strategy > prompt nudging**

Instruction-tuned "Chat" models cluster together in stylometric space, *away* from both base models and human text. Chat outputs skew **information-dense and noun-heavy**: nominalizations, that-clauses as subjects, past-participial postmodifiers. Base models often cluster closer to humans. These patterns survive zero-shot RAID generation (no style-mimic prompt, no human prefix) — they are not artifacts of a single lab setup.

For unslop, this paper is the strongest 2026 argument that **detection and humanization must move below the word list**. Stock-vocab stripping hits Signal 1 (lexical AI-isms). Biber features capture **how** language is packaged: clause types, subordination depth, stance markers, nominal density. RLHF/DPO **homogenization** (Alignment Tax, arXiv:2603.24124) explains *why* chat models share a sedimented register — alignment collapses response diversity at the semantic level while preserving much token-level entropy. Rallapalli shows the stylistic fingerprint of that collapse.

**unslop verdict:** Architecture is directionally right (`structural.py`, `soul.py`, `stylometry.py`) but operates on **~15 surface proxies**, not Biber's 67 POS/register features. Critical irony: Rallapalli lists **contractions as overused by LLMs** (`f_59_contractions`); unslop's `soul.py` *injects* contractions because Paneru's corpus-specific markers and token-distribution nudges say humans contract more. Both can be true (chat models over-contract in aggregate RAID genres while still under-contract vs human Reddit/conversation). unslop needs genre-conditioned baselines, not one global contraction target. Highest-value gap: optional spaCy/pybiber register audit; no hard dependency.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Rallapalli et al. (2026) — arXiv abstract** | https://arxiv.org/abs/2604.14111 |
| **Rallapalli et al. — HTML full text** | https://arxiv.org/html/2604.14111 |
| **Reinhart et al. (2025) — PNAS** | https://www.pnas.org/doi/10.1073/pnas.2422455122 |
| **Reinhart et al. — DOI** | https://doi.org/10.1073/pnas.2422455122 |
| **Markey et al. (2024) — Dense and Disconnected** | https://doi.org/10.1177/07410883241263528 |
| **Alignment Tax / RLHF homogenization** | https://arxiv.org/abs/2603.24124 |
| **Alignment Tax PDF** | https://arxiv.org/pdf/2603.24124v2 |
| **RAID benchmark paper (ACL 2024)** | https://aclanthology.org/2024.acl-long.674/ |
| **RAID dataset / leaderboard** | https://github.com/liamdugan/raid |
| **RAID shared task** | https://raid-bench.xyz/shared-task |
| **pseudobibeR (feature extractor used by Rallapalli)** | https://github.com/browndw/pseudobibeR |
| **pybiber (Python Biber toolkit)** | https://github.com/browndw/pybiber |
| **Neurobiber (fast Biber extraction, 2025)** | https://arxiv.org/abs/2502.18590 |
| **Neurobiber PDF** | https://arxiv.org/pdf/2502.18590 |
| **Zanotto & Aroyehun — RAID linguistic profiling (EMNLP 2025)** | https://arxiv.org/abs/2412.03025 |
| **Tercon & Dobrovoljc — AI text linguistic survey** | https://arxiv.org/abs/2510.05136 |
| **Biber register ID on open web (2016)** | https://doi.org/10.1558/jrds.v2i1.27637 |
| **UCBD / Alignment Tax code** | https://github.com/DigitLion/ucbd-experiment |

---

## The Biber register framework (what Rallapalli actually measures)

Douglas Biber's Multidimensional Analysis (MDA) treats style as **functional distribution of grammatical resources**, not topic or sentiment. The 67 features in pseudobibeR/pybiber span:

| Category | Example features | Register function |
|----------|------------------|-------------------|
| **Tense / aspect** | present perfect, past perfect, progressive | narrative vs informational stance |
| **Pronouns** | first/second/third person, demonstratives | involved vs impersonal production |
| **Clause types** | that-clauses (subject/object), WH relatives, pied-piping relatives | information packaging density |
| **Nominal modification** | nominalizations, attributive adjectives, pre/post modifiers | "compressed" academic/news style |
| **Subordination** | concessive (`though`), conditional, purpose clauses | rhetorical complexity |
| **Coordination** | phrasal vs clausal coordination | additive vs elaborative structure |
| **Stance / interaction** | downtoners, amplifiers, discourse particles (`well`, `anyway`) | dialogic openness |
| **Passives & be-verbs** | agentless passive, `be` as main verb | impersonal / descriptive register |
| **Lexical diversity** | type-token ratio (feature 43) | vocabulary richness |

Features are counted **per 1,000 words**. MDA then reduces correlated features to interpretable dimensions (e.g., "informational vs involved production"). Rallapalli uses raw features + PCA + Random Forest + SHAP — not full MDA dimension scores — but the interpretability comes from the same feature vocabulary corpus linguists have used since the 1980s.

**POS/register link:** Biber features are **not raw POS tag sequences** (contrast HLD-Detector's POS n-grams, Agent #14). They are **POS-informed functional categories** — e.g., `f_32_wh_obj` counts WH-relative clauses functioning as objects, which requires parse-level or pattern-level grammar, not a unigram POS tag. This sits between unslop's regex heuristics and full dependency parsing.

Extractors: **pseudobibeR** (R, used in paper), **pybiber** (Python/spaCy), **Neurobiber** (https://arxiv.org/abs/2502.18590, GPU batch).

---

## Rallapalli et al. (2026) — method and findings

### Dataset and design

- **Corpus:** RAID subset excluding adversarial attacks → **467,985 texts** from 12 sources (1 human + 11 LLMs).
- **Genres:** Abstracts, Books, News, Poetry, Recipes, Reddit, Reviews, Wikipedia.
- **Decoding:** Greedy vs sampling × repetition penalty on/off (4 configs).
- **Generation:** Zero-shot prompts; chat models get instruction templates, base models get prefix continuation. **No** "write in human style" nudge; **no** human prefix to mimic.
- **Contrast with Reinhart (2025):** Reinhart conditions on 500 tokens of human text and explicitly prompts style continuation. Rallapalli tests "realistic" deployment where the model picks its own register.

### Classification sanity check

Random Forest on 67 Biber features achieves **AUC ≈ 0.9775** (down-sampled MGT:HWT = 4:1). Top discriminators (permutation importance + SHAP interactions):

1. **`f_43_type_token`** — TTR; humans show **narrow, predictable** TTR band; LLMs more dispersed. Important via **interactions**, not mean shift alone.
2. Overused LLM features (aggregate): **`f_29_that_subj`**, **`f_59_contractions`**, **`f_27_past_participle_whiz`**, **`f_14_nominalizations`**, **`f_34_sentence_relatives`**.
3. Underused LLM features: **`f_32_wh_obj`**, **`f_33_pied_piping`**, **`f_36_though`**, **`f_66_neg_synthetic`**, **`f_50_discourse_particles`**.

The overuse bundle = **dense, elaborated, noun-phrasal prose**. The underuse bundle = **rare, syntactically intricate, dialogically open** constructions humans use sparingly but detectors (and readers) associate with " lived-in" writing.

### Four structural results

1. **Genre dominates source.** PCA on genre×source mean feature vectors: ellipses cluster by genre (News with News, Poetry with Poetry) regardless of human vs GPT-4 vs Mistral. LLMs **adapt register to genre** without explicit prompting — mimicking human situational variation at the macro level while retaining machine micro-signatures.

2. **Instruction tuning separates chat models.** Hierarchical clustering (per genre, Ward linkage, PCA to 95% variance): human text groups with **base** models; **Chat** variants cluster together and away from humans. Conclusion text: "instruction tuning and reinforcement learning push models toward similar stylistic tendencies."

3. **Model > decoding.** Within-genre PCA colored by model vs decoding marker: same model clusters regardless of greedy/sampling/repetition penalty, with exceptions for GPT-2, MPT, Mistral where decoding matters more.

4. **Prompt/decoding nudging is weak.** Key differentiators "robust to generation conditions" — including RAID's lack of style-mimic prompts. Reinhart's style-conditioned setup **still** finds the same overuse patterns; Rallapalli confirms they persist when those crutches are removed.

### Implications for detection

- **Genre-stratified detectors** (or genre-aware thresholds) are mandatory. A single global "human band" across Abstracts and Reddit will false-positive or false-negative by genre shift alone.
- **Feature interactions matter.** Optimizing TTR alone misses the SHAP story — TTR modulates how other features classify.
- **Chat-model homogenization is a detectable prior.** If all major assistants converge on the same Biber cluster post-RLHF, stylometric detectors get a **shared negative class** that survives vendor updates better than perplexity thresholds.

---

## RLHF homogenization — connecting alignment tax to Biber clustering

Three papers form a causal chain Rallapalli observes but does not fully mechanize:

### 1. Reinhart et al. (PNAS 2025)

Parallel corpora (Llama 3 + GPT-4o variants). Biber tagset (~66 features). Findings:

- Instruction-tuned models diverge **more** from humans than base models.
- Systematic overuse: present participial clauses, that-subject clauses, nominalizations, phrasal coordination.
- Built a Biber-feature classifier that "recognizes machine-generated text with relative ease."

**URL:** https://www.pnas.org/doi/10.1073/pnas.2422455122

### 2. Markey et al. (2024) — *Dense and Disconnected*

Qualitative + quantitative analysis of ChatGPT academic prose. "Sedimented style": informationally dense, dialogically closed, simultaneously empty and fluffy. Nominalization overreliance is a central explanatory feature — aligns with Rallapalli's `f_14_nominalizations` overuse.

**URL:** https://doi.org/10.1177/07410883241263528

### 3. Alignment Tax (arXiv:2603.24124, March 2026)

Different measurement (semantic response clusters, not Biber), same phenomenon:

- RLHF-aligned models: **40–79%** of TruthfulQA questions yield a **single semantic cluster** across 10 samples (Single-Cluster Rate, SCR).
- Base Qwen3-14B: **1.0% SCR** vs instruct **28.5%** (p < 10⁻⁶).
- Stage ablation: Base 0.0% → SFT 1.5% → **DPO 4.0%+** SCR — **DPO drives collapse**, not SFT.
- Token entropy decouples: DPO retains ~66% token entropy while killing response diversity.

**Bridge to Rallapalli:** DPO/RLHF narrows the **semantically acceptable phrasing manifold**. Biber clustering shows the **linguistic surface expression** of that manifold — chat models don't just say the same thing; they say different things **the same way** (nominal density, that-clauses, suppressed discourse particles).

**Decoding cannot undo alignment tax.** Rallapalli shows decoding < model; Alignment Tax shows sampling temperature doesn't restore diversity on affected prompts. unslop's subtractive humanization is therefore **necessary but not sufficient** — you cannot temperature your way out of sedimented register.

---

## Debate, limitations, and open disagreements

### Genre confound vs genuine detection signal

**Skeptic position:** If genre explains most variance, detectors are measuring "did the model write an abstract or a Reddit post?" not "is this machine-generated?" Rallapalli's own PCA supports this — genre ellipses overlap across sources.

**Counter:** Within-genre clustering still separates Chat from human (Section 4.3 dendrograms). Practical detection domains (student essays, cover letters) are **genre-bounded**. The relevant question is human vs machine **within the declared genre**, not across all RAID domains at once.

### Contradiction: LLMs overuse contractions (Rallapalli) vs underuse (Paneru / unslop soul)

Rallapalli: `f_59_contractions` **overused** in aggregate RAID LLM output. Paneru (arXiv:2604.11687): humans ~0.17 contractions/chunk, AI ~0.00. unslop `soul.py` injects contractions.

**Resolution:** Genre conditioning. RAID aggregates span formal genres (Abstracts, Wikipedia, News) where chat models may over-use conversational contractions in inappropriate registers, while human Reddit/dialogue corpora under-contract in Paneru's chunk sample. unslop's global contraction injection helps **formal AI slop** but could **push away from human** in genres where humans rarely contract. Need genre-specific baselines in `stylometric_baseline.json`.

### TTR: overused or distinctive distribution?

Rallapalli notes TTR is **not** uniformly over/underused by LLMs — humans have **tighter** TTR distribution. unslop's `type_token_ratio` in `stylometry.py` measures point value, not **distribution tightness**. A rewriter that widens vocabulary without matching human band shape may not help.

### Paraphrase, ESL, causality

Rallapalli excludes RAID adversarial splits; Biber syntax features may survive synonym swap but not DIPPER (Zanotto & Aroyehun: https://arxiv.org/abs/2412.03025). HLD (Agent #14) POS/dep layers hold better under paraphrase — Biber alone is partial defense.

Biber encodes formal register; ESL writers may share nominal density / low discourse-particle rates without being LLMs — neither Rallapalli nor Reinhart reports ESL-stratified FPR. Closing Biber gaps for anti-detector can push ESL prose toward native-academic register (authenticity risk).

RLHF-as-cause is supported by Alignment Tax stage ablations + Rallapalli chat clustering, but RAID bundles opaque vendor alignment stacks — not a clean SFT→DPO ablation on one base model.

---

## unslop structural / soul / stylometry gaps (mapped to Biber)

Current pipeline (verified in `unslop/scripts/`):

| unslop module | What it measures/changes | Nearest Biber features | Coverage |
|---------------|-------------------------|------------------------|----------|
| `humanize.py` | Stock vocab, hedging, sycophancy | Stance amplifiers, performative openers (partial) | ~5/67 |
| `structural.py` | Sentence-length split/merge, bullet soup | Indirect: clausal boundaries, coordination | ~2/67 |
| `soul.py` | Contraction injection | **`f_59_contractions`** (genre-dependent direction) | 1/67 |
| `stylometry.py` | TTR, latinate ratio, passive approx, sentence σ/CV | **`f_43`**, **`f_14`**, passives, **`f_46` downtoners** (partial) | ~8/67 proxies |
| `lexical_targets.py` | Baseline band nudges | Blocked: **`stylometric_baseline.json` missing** → no-ops | 0 effective |

### Gap 1 — No register/POS feature extraction

unslop has **zero** that-clause, WH-relative, pied-piping, or discourse-particle counters. `latinate_ratio` regex approximates nominalization pressure but misses **`f_27_past_participle_whiz`**, **`f_29_that_subj`**, **`f_34_sentence_relatives`** — four of Rallapalli's top-five LLM overuse features.

**Fix direction:** Optional `register.py` using pybiber or lazy spaCy patterns; expose `biber_overuse_score` vs genre baseline. Match `surprisal.py` optional-dep pattern — no hard spaCy pin.

### Gap 2 — Genre-blind baselines

Rallapalli: genre > source. unslop: single global human band (when baseline file exists). A Reddit post and an arXiv abstract share one contraction target — wrong per both Rallapalli and Paneru.

**Fix direction:** `stylometric_baseline.json` keyed by `detect.py` genre heuristic (email, essay, docs, code-adjacent prose).

### Gap 3 — Structural pass doesn't touch syntactic templates

`structural.py` varies **length**, not **clause skeleton**. Rallapalli/Reinhart implicate **syntactic choice** (that-subject vs WH-object relatives). Splitting at `;` and `, but` doesn't reduce **`f_29_that_subj`** density.

**Fix direction (Agent #14 overlap):** POS-trigram entropy audit; flag paragraphs where >60% sentences open `DT-NN-VBZ` or repeat `that`-clause subjects. Safe rewrites: break one that-clause into two sentences; front concessive (`though`) where underused.

### Gaps 4–6 — Soul, anti-detector, feedback

`soul.py` moves TMR ~0.0–0.2 pp on fixtures via contractions alone; Rallapalli classifies on **multi-feature SHAP interactions**. Contraction injection without nominal-density reduction may worsen academic-genre Biber scores. Underused LLM features (`f_33_pied_piping`, `f_36_though`, `f_50_discourse_particles`) have no unslop lever; anti-detector optimizes RoBERTa/surprisal, not register gaps. `stylometry.py` profiles aren't wired to `detector.py` feedback (same orphan problem as DivEye in UPDATE-PLAN-2026-08).

---

## Recommended unslop actions (priority order)

1. **Ship `benchmarks/results/stylometric_baseline.json`** — genre-stratified p25/p75 for existing `stylometry.py` fields; unblocks `lexical_targets.py`.
2. **Benchmark unslop output on pybiber features** — before/after each mode on RAID genre slices; quantify whether `full` moves **`f_14_nominalizations`** down and **`f_36_though`** up.
3. **Optional `register.py`** — pybiber lazy import; 10-feature "Rallapalli subset" for CLI `--register-audit`.
4. **Revise contraction policy** — genre-conditioned: inject in formal AI slop; skip or reduce in genres where Rallapalli shows human underuse.
5. **Cite Rallapalli + Reinhart in RESEARCH_AND_TECH.md** — justify why word-list humanization plateaus; link Alignment Tax as generative cause of chat clustering.
6. **Do not claim Biber-evasion** — paraphrase and cross-genre transfer remain open; ESL fairness unvalidated.

---

## Bottom line

Rallapalli et al. make stylometric detection **interpretable and genre-aware**: LLMs aren't flagged for word choice alone but for a **sedimented register** — nominal-heavy, that-clause subject-heavy, discourse-particle-poor — that RLHF homogenization pushes chat models toward collectively. unslop already attacks the surface symptoms (slop vocabulary, flat rhythm, zero contractions) but not the **Biber skeleton**. Closing that gap requires optional register measurement, genre-stratified baselines, and syntactic diversity beyond sentence-length splitting — without breaking the byte-preservation contract that makes unslop trustworthy.

**Detection era shift:** 2023 perplexity → 2025 surprisal dynamics → 2026 **register geometry + temporal signals**. Biber is the interpretable layer explaining *why* GPTZero v6 cones and DivEye variance fire. unslop should measure it, not just mimic its side effects.

---

**Related memos:** Agent #14 (HLD POS/dep), #17 (Sadasivan TV-reduction), #25 (structural σ), UPDATE-PLAN-2026-08.
