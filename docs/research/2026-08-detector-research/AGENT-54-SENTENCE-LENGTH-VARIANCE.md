# AGENT-54 — Sentence-Length Variance Restoration

**Topic:** Academic and practical work on restoring human-like sentence-length distribution in AI text — mapped to `unslop/scripts/structural.py`  
**Prepared:** 2026-08-19  
**Scope:** Detection literature (σ, CV, consecutive Δ), humanization/restoration methods, unslop implementation audit, gaps  
**Status:** Complete research memo  
**Related agents:** AGENT-49 (burstiness vs surprisal), AGENT-25 (Adversarial Paraphrasing), AGENT-50 (Jemama fidelity/perplexity), AGENT-45 (linguistic cues)

---

## Executive summary

LLM prose is **structurally flat**: sentences cluster in a narrow band (often 15–28 words) with low within-paragraph standard deviation. Human prose **oscillates** — short emphatic fragments beside long analytical clauses. Detectors exploit this gap even when mean sentence length is indistinguishable.

| Signal | Human (typical) | AI (typical) | Primary sources |
|--------|-----------------|--------------|-----------------|
| σ(sentence word count), paragraph | ~6–8+ (academic); ~8.2 (practitioner GPT-4o contrast) | ~2–4; GPT-4o ~4.1 | Desaire 2023 (#8); r/WritingWithAI 2026 |
| CV (σ/μ) | ~0.55–0.75 (commercial humanizer targets) | <0.25–0.35 flagged | Joseph et al. 2025; BurstInjector marketing |
| Consecutive-sentence Δ | High median word-count delta | Low | Desaire 2023 (#9) |
| Fragment rate (<11 words) | Present | Rare | Desaire 2023 (#10) |
| Long sentences (>34 words) | Present | Rare | Desaire 2023 (#11) |

**Restoration** means moving a document's sentence-length distribution toward human shape **without changing claims**. Three families:

1. **Generative (decode-time)** — samplers that avoid mode collapse (Holtzman nucleus, Meister typical, min-p, Mirostat). Fixes the problem at source; unavailable to post-hoc rewriters.
2. **Learned paraphrase** — DIPPER, MASH, TempParaphraser reshape structure implicitly via trained models. High evasion; risk of semantic drift; needs GPU or API.
3. **Deterministic structural edit** — split long sentences, merge parallel bullets, inject fragments. Cheap, auditable, preservation-safe. **This is `structural.py`.**

**unslop verdict:** `structural.py` implements a **conservative, one-sided variance restorer** — it **splits** overlong sentences in flat paragraphs and **merges** bullet-soup monotony. It does **not** inject short sentences or merge adjacent short clauses (the other half of the human distribution). That asymmetry is intentional: splitting is low false-positive risk; fragment injection and aggressive merging are high. Anti-detector LLM mode (`skills/unslop/SKILL.md` step 1) carries the short-sentence/fragment half. Deterministic pass alone lifts σ but rarely reaches the σ ≥ 6 band the skill targets.

**Critical interaction:** Adversarial Paraphrasing (NeurIPS 2025) showed **lexical-only** rewriting **increases** detector TPR (+8.57% RADAR, +15.03% Fast-DetectGPT). Sentence-length restoration must run **after** lexical scrubbing, not instead of structural work. `structural.py` docstring cites this directly.

---

## 1. Why sentence-length variance is a detection signal

### 1.1 Mean vs variance

Desaire et al. (2023) — the canonical stylometric detection paper for academic science writing — found:

- **Average sentence length does not separate** human vs ChatGPT paragraphs.
- **Standard deviation of sentence length within a paragraph does** (feature #8 in their 20-feature XGBoost model, >99% in-domain accuracy).
- **Median consecutive-sentence length difference** also discriminates (#9).
- **Presence of very short (<11 word) and very long (>34 word) sentences** favors human (#10–11).

The model's insight: AI text is not "short" or "long" on average — it is **uniform**. Humans modulate length for emphasis, qualification, and rhythm.

**URLs:** [Cell Reports Physical Science / arXiv:2303.16352](https://doi.org/10.48550/arxiv.2303.16352) · [PMC10328544](https://pmc.ncbi.nlm.nih.gov/articles/PMC10328544/) · [DOI 10.1016/j.xcrp.2023.101426](https://doi.org/10.1016/j.xcrp.2023.101426)

### 1.2 Coefficient of variation (scale-invariant burstiness)

CV = σ/μ removes document-length bias. Feature-engineering studies (Joseph et al. 2025, SSRN) rank sentence-length CV among top stylometric discriminators — sometimes above raw perplexity in Random Forest importance. Commercial humanizers (BurstInjector, Humanit Ultra) target CV bands (~0.55–0.75 human vs <0.35 AI).

unslop exposes CV as `sentence_length_cv` in `stylometry.py` for voice-match prompting; `structural.py` optimizes raw σ per paragraph, not CV.

**URL:** [SSRN 5833302](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5833302)

### 1.3 Cross-model confirmation

| Study | Finding | URL |
|-------|---------|-----|
| Muñoz-Ortiz et al. (2025) | stddev sentence length as RF feature in paraphrase-resilience eval | [arXiv HTML 2605.14240](https://arxiv.org/html/2605.14240v1) |
| Contrasting Linguistic Patterns (Springer 2024) | LLM news text concentrates 10–30 tokens; humans wider tail | [DOI 10.1007/s10462-024-10903-2](https://link.springer.com/article/10.1007/s10462-024-10903-2) |
| EMNLP 2025 linguistic profiling | Sentence length mean + variability in LLM vs human profiles | [ACL 2025.emnlp-main.1163](https://aclanthology.org/2025.emnlp-main.1163.pdf) |
| Trace Is In Sentences (2025) | Inter-sentence structure survives word-level paraphrase (PSP) | [arXiv HTML 2509.18535](https://arxiv.org/html/2509.18535) |
| CT² / AI Detectability Index (2023) | Sentence-wise variety lower in AI; gap narrows for GPT-3.5+ | [arXiv:2310.05030](https://doi.org/10.48550/arxiv.2310.05030) |
| Tarım & Onan (2025) | Burstiness = CV of sentence lengths; diffusion LMs mimic human band | [arXiv:2507.10475](https://arxiv.org/html/2507.10475) |

### 1.4 Practitioner anchor (unslop Cat 14)

r/WritingWithAI structural thesis (2026): robotic writing = uniform sentence lengths + smooth transitions + tidy paragraph closures. Community measurement cited in unslop docs: human σ ~**8.2**, GPT-4o ~**4.1** (field heuristic, not peer-reviewed controlled study).

**URL:** [Reddit 1r9r6gk](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/)

### 1.5 Orthogonal to perplexity (Jemama split)

Jemama & Kumar (IEEE UEMCON 2025) decouples **style fidelity** (authorship verifier up to 99.9%) from **statistical naturalness** (GPT-2 perplexity). A rewrite can match voice and still sit at μ=15 perplexity vs human μ=29.5.

Sentence-length σ is a **third axis** — syntactic rhythm visible without an LM. unslop treats it separately from both voice-match and surprisal (`AGENT-50`).

**URL:** [arXiv:2509.24930](https://arxiv.org/abs/2509.24930)

---

## 2. Restoration techniques — academic and practical

### 2.1 Generation-side (prevent flatness)

These restore variance **before** the rewriter sees text. Post-hoc tools like unslop cannot invoke them on closed APIs.

| Method | Mechanism | Effect on length distribution |
|--------|-----------|-------------------------------|
| Nucleus sampling (Holtzman et al., ICLR 2020) | Truncate by cumulative probability mass | Reduces mode collapse; more clausal variety | [arXiv:1904.09751](https://arxiv.org/abs/1904.09751) |
| Locally typical sampling (Meister, TACL 2023) | Sample near conditional entropy | Human-like token unpredictability → varied clause boundaries | [arXiv:2202.00666](https://arxiv.org/abs/2202.00666) |
| Mirostat (Basu, ICLR 2021) | Perplexity feedback loop | Holds entropy in human-preferred band | [arXiv:2007.14966](https://arxiv.org/abs/2007.14966) |
| Min-p (Nguyen, ICLR 2025 Oral) | Adaptive truncation floor | Creative outputs with less uniform rhythm | [arXiv:2407.01082](https://arxiv.org/abs/2407.01082) |
| XTC (p-e-w, 2024) | Drop top-probability tokens | Breaks structural clichés | llama.cpp PR #9742 |
| Antislop backtracking (Paech, ICLR 2026) | Reject slop n-grams at decode | Phrase-level; indirect length effect | [arXiv:2510.15061](https://arxiv.org/abs/2510.15061) |

**Takeaway for unslop:** README and Cat 04 correctly position decoding as the largest lever. File rewriter compensates for API users who never touch samplers.

### 2.2 Learned structural paraphrase

| System | Structural lever | Sentence-length effect |
|--------|------------------|------------------------|
| **DIPPER** (Krishna et al., NeurIPS 2023) | Paragraph paraphrase with lexical + order diversity knobs | Implicit reshaping; crushes DetectGPT TPR 70.3% → 4.6% | [arXiv:2303.13408](https://arxiv.org/abs/2303.13408) |
| **MASH** (Gu et al., ACL Findings 2026) | Style-SFT BART: AI→human transfer + DPO vs detector | 92% ASR; trained on human rhythm, not explicit σ target | [arXiv:2601.08564](https://arxiv.org/abs/2601.08564) |
| **TempParaphraser** (EMNLP 2025) | Temperature-simulated entropy in paraphrase | Token-level; structural side effect | [ACL 2025.emnlp-main.1607](https://aclanthology.org/2025.emnlp-main.1607/) |
| **Adversarial Paraphrasing** (Cheng, NeurIPS 2025) | Detector-guided token edits | **Simple** paraphrase **worsens** detection; adversarial path needed | [arXiv:2506.07001](https://arxiv.org/abs/2506.07001) |
| **StyleShield** (2025) | Continuous embedding flow | Raises output PPL above human ref — injects variability | See AGENT-23 |

Learned methods can hit both tails of the distribution (fragments + long sentences) but require training data, GPU, or detector oracle access. unslop's `detector.py` references AdvPara as escalation when deterministic ladder exhausts.

### 2.3 Rule-based / prompt-based restoration

OSS and commercial stack converges on a **3–5 stage pipeline** (Cat 17): vocab scrub → structural scrub → texture injection → optional statistical tuning. Sentence-length work sits in stages 2–3.

| Technique | Operation | Examples |
|-----------|-----------|----------|
| **Split long sentences** | Break at safe clausal boundaries | unslop `split_long_sentences`; Microsoft Copilot humanize guide; Leap AI manual advice |
| **Merge short parallel units** | Collapse repetitive bullets/clauses | unslop `merge_bullet_soup`; BurstInjector "merge adjacent short sentences" |
| **Inject short sentences / fragments** | Add ≤8-word emphasis lines | anti-detector SKILL step 1; r/WritingWithAI craft advice |
| **Combine short + long pairs** | Deliberate burst pattern | BurstInjector gamma-distribution target model |
| **Prompt-only** | "Mix sentence lengths; include one fragment per paragraph" | blader/humanizer, West dev.to playbook, Humanit Ultra clause-level rewrite |

**BurstInjector** (commercial, 2026) is the most explicit σ-restoration product: measure CV → fit gamma distribution to human corpora → split/merge to hit target → re-measure. unslop's deterministic pass is a **subset** of this pipeline (split + bullet merge only; no gamma fit, no short-sentence injection, no adjacent-short merge).

**URL:** [texthumanize.link/methods/burstinjector](https://texthumanize.link/methods/burstinjector)

### 2.4 What naive paraphrase does (negative result)

Adversarial Paraphrasing baseline = strong LLM synonym swap **without** structural targeting:

- RADAR TPR **+8.57%**
- Fast-DetectGPT TPR **+15.03%**

Hypothesis: paraphrase models homogenize clausal boundaries while changing tokens — **lowering** syntactic σ and **smoothing** surprisal curvature. Structural restoration is damage control after lexical passes, not optional polish.

unslop pipeline order: lexical (`humanize.py`) → structural (`structural.py`) → soul/contractions (`soul.py`) → optional LLM anti-detector.

---

## 3. unslop `structural.py` — implementation map

**File:** `unslop/scripts/structural.py`  
**Phase:** 1 (deterministic, runs on `_protect()`-placeholder text)  
**CLI:** `--structural` (default on `balanced`/`full`; off on `subtle`)  
**Tests:** `tests/unslop/test_structural.py` — correctness guards + σ non-regression contract

### 3.1 Design philosophy

From module docstring:

```6:9:unslop/scripts/structural.py
Adversarial Paraphrasing (NeurIPS 2025) showed that synonym-swap rewriting without
structural work actually raises detector TPR by 8-15% — a lexical-only pipeline is
not neutral, it is a regression against modern detectors. This module is the
structural layer: it re-introduces sentence-length variance after lexical scrubbing.
```

Conservative by design:
- At most **one split per sentence per pass** (no cascade choppiness)
- **No split** in already-varied paragraphs (σ ≥ `target_sigma`)
- **Risky connectors excluded** (`, which`, `, because`, `, if`)
- Bullet merge prefers **false negatives** over destroying meaning

### 3.2 Pass 1: `split_long_sentences`

**Goal:** Increase paragraph-level σ by turning one long sentence into two shorter ones.

| Parameter | Default | Role |
|-----------|---------|------|
| `min_words` | 30 | Split floor when paragraph is not flat |
| `flat_min_words` | 20 | Split floor when paragraph σ < `target_sigma` |
| `target_sigma` | **5.0** | Flat if σ < 5 (AI band ~4; human ~8) |
| `min_half` | 8 | Both split halves must have ≥8 words |

**Flat-paragraph detection** (`_paragraph_sigma`):

```164:171:unslop/scripts/structural.py
def _paragraph_sigma(sentences: list[str]) -> float:
    """Sentence-length stddev across a paragraph. Short paragraphs return 0."""
    lengths = [_count_words(s) for s in sentences]
    if len(lengths) < 2:
        return 0.0
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    return variance**0.5
```

**Split boundary priority** (`_SPLIT_CANDIDATES`):

1. `;` — always safe (semicolon marks boundary)
2. `, however,` → `. However,`
3. `, but` → `. But`
4. `, and then` → `. Then`
5. `, so` → `. So`
6. `, while` → `. While`
7. ` — ` / ` – ` (em-dash) — balance check catches appositives

Maps to Desaire's human signals: more sentences per paragraph, higher consecutive Δ, eventual presence of sub-11-word clauses **if** the split creates a short half.

**Skips:** pure-list paragraphs, single-sentence paragraphs (no σ to measure), paragraphs already at σ ≥ 5.

### 3.3 Pass 2: `merge_bullet_soup`

**Goal:** Remove **parallel short-bullet monotony** — a structural tell distinct from low σ but correlated (every bullet ~same word count).

| Guard | Value |
|-------|-------|
| `min_run` | ≥3 consecutive bullets |
| Same first word | case-insensitive |
| `max_bullet_words` | ≤10 each |
| `max_total_words` | ≤40 across run |

Merging **increases** average sentence length but **removes** repetitive micro-units — net σ effect depends on context. Primary win: breaks Turnitin/GPTZero "uniform bullet syntax" pattern (`skills/unslop/SKILL.md` step 2).

### 3.4 Orchestration: `humanize_structural`

```361:375:unslop/scripts/structural.py
def humanize_structural(
    text: str,
    *,
    report: StructuralReport | None = None,
) -> str:
    """Apply all structural passes in order. Operates on protected text.

    Order matters: split before merge. Splitting a long sentence can change
    neighbouring bullets (none, in practice — sentences don't live inside bullet
    lines), but merging bullets can remove sentence candidates for the next pass.
    Running splits first lets us catch any long sentences that happen to live
    above or below a mergeable list without losing them to an overeager merge."""
    text = split_long_sentences(text, report=report)
    text = merge_bullet_soup(text, report=report)
    return text
```

Hooked in `humanize.py` Phase 1 after lexical regex passes, before `soul.py`.

### 3.5 Measurement alignment (`validate.py`, `stylometry.py`)

| Module | Metric | Threshold / use |
|--------|--------|-----------------|
| `validate.py` `_burstiness()` | Document-wide σ | Warning if σ < **4** on ≥8 sentences |
| `validate.py` `_count_flat_paragraphs()` | Per-paragraph σ | Flat if σ < **3.0** with ≥3 sentences |
| `stylometry.py` | `sentence_length_mean`, `sentence_length_stdev`, `sentence_length_cv` | Voice-match targets |
| `benchmarks/run.py` | Strict burstiness gate | Fails if human-like fixture flattened below floor |
| `skills/unslop/SKILL.md` anti-detector | Target band | σ ≥ **6**; ≥1 sentence ≤8 words and ≥1 ≥20 words per paragraph |

**Design note:** Structural pass uses **per-paragraph** σ (correct — document-wide σ hides flat paragraphs). Validator reports both.

Sentence boundary regex is shared between `structural.py` and `validate.py` (`_SENTENCE_SPLIT_RE` / `_SENTENCE_SPLIT`) so measurement and rewrite stay aligned.

---

## 4. Coverage matrix — what restoration requires vs what unslop ships

| Restoration move | Detection feature addressed | unslop deterministic | unslop LLM anti-detector |
|------------------|----------------------------|----------------------|--------------------------|
| Split 30+ word sentences | ↑ σ, ↑ sentence count, ↑ consecutive Δ | ✅ `split_long_sentences` | — |
| Split 20–29 word in flat para | Same, for "medium uniform" AI band | ✅ `flat_min_words` regime | — |
| Merge parallel short bullets | Break uniform list cadence | ✅ `merge_bullet_soup` | Step 2 (vary bullet syntax) |
| Inject ≤8-word fragment | Desaire #10, CV lower tail | ❌ not deterministic | ✅ Step 1, 3 |
| Merge two short sentences → one long | CV upper tail, long-sentence presence | ❌ | Prompt-only |
| Start sentence with And/But | Opener variety | ❌ | ✅ Step 3 |
| Gamma/CV-targeted reshaping | Commercial detector rhythm bands | ❌ | — |
| Cross-model second pass | Breaks templated clausal rhythm | ❌ | ✅ Step 6 |

**Asymmetry is the main gap:** `structural.py` only ** subdivides**; it never **creates** the short tail that Desaire features #10 and anti-detector step 1 require. A paragraph of five 22-word sentences stays flat if no sentence hits 30 words and no semicolon/but boundary exists — the flat_min_words path still needs a splittable connector.

---

## 5. Evidence-ordered restoration playbook

For unslop maintainers and anti-detector mode:

1. **Measure before edit** — `stylometry.analyze()` or validator burstiness on draft; note per-paragraph flat counts.
2. **Lexical scrub first** — stock vocab, hedging, sycophancy (`humanize.py`). Do not skip.
3. **Run structural pass** — `--structural` on balanced+; inspect `StructuralReport` (`sentences_split`, `bullet_groups_merged`).
4. **Re-measure σ and flat paragraphs** — if σ still < 5 or flat paragraphs remain, escalate to LLM anti-detector (fragments, short sentences, And/But openers).
5. **Soul pass** — contractions lift register (`soul.py`); Paneru 2026: human contraction rate ~0.17 vs AI ~0.00.
6. **Optional surprisal read** — `--surprisal-variance` for token-level rhythm (orthogonal axis; `AGENT-49`).
7. **Do not claim detector-proof output** — Turnitin Aug 2025 bypasser model trains on humanizer signatures; σ restoration is necessary, not sufficient.

---

## 6. Open questions

1. **Ablation:** No published study isolates "deterministic sentence split only" vs DivEye / Fast-DetectGPT TPR shift. unslop should benchmark σ before/after on `benchmarks/` fixtures with optional detector loop.
2. **σ=5 threshold:** Practitioner 8.2/4.1 gap; Desaire used paragraph-internal σ in chemistry abstracts only. Genre-aware floors (news vs academic vs creative) under-studied.
3. **Split-without-connector deadlock:** Uniform 24-word sentences with no safe boundary — structural pass no-ops; only LLM or manual edit breaks deadlock.
4. **CV vs σ:** Should `target_sigma` become CV-aware (short documents bias σ down)? `stylometry.py` already exports CV for voice-match.
5. **Merge vs split interaction:** Merging bullets reduces sentence count — can lower σ in edge cases. Current ordering (split first) mitigates; no quantitative study in repo.
6. **Diffusion LMs:** Tarım 2025 — sentence-length CV heuristics can misclassify diffusion outputs that mimic human burstiness without human authorship.

---

## 7. Recommendations for unslop

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P1** | Add benchmark row: σ, CV, flat_paragraphs before/after structural-only pass | Close ablation gap; cite in README only with real runs |
| **P2** | Document deadlock case in `structural.py` docstring + SKILL | Set expectations: deterministic pass is half the restoration problem |
| **P3** | Consider opt-in `merge_short_sentences` (adjacent ≤12-word clauses → compound) | Addresses upper-tail variance; high false-positive risk — gate tightly |
| **P4** | Wire flat-paragraph count from validator into LLM rewrite prompt | Give model explicit "paragraph 3 is flat (σ=2.1)" signal |
| **P5** | Do **not** add gamma-fit targeting without preservation tests | BurstInjector-style reshaping can drift meaning; `TestPreservation` is the contract |

---

## 8. Bibliography (URLs)

### Detection — sentence-length variance as feature
- Desaire et al. (2023): https://doi.org/10.48550/arxiv.2303.16352 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10328544/
- Joseph et al. feature-based detection (2025): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5833302
- Muñoz-Ortiz paraphrase resilience: https://arxiv.org/html/2605.14240v1
- Contrasting linguistic patterns (news): https://link.springer.com/article/10.1007/s10462-024-10903-2
- EMNLP 2025 linguistic profiling: https://aclanthology.org/2025.emnlp-main.1163.pdf
- Trace Is In Sentences: https://arxiv.org/html/2509.18535
- CT² AI Detectability Index: https://doi.org/10.48550/arxiv.2310.05030
- Tarım & Onan diffusion detection: https://arxiv.org/html/2507.10475
- Explainable detection failures (Sentence Length Variation): https://arxiv.org/html/2603.23146v1

### Humanization / restoration
- Adversarial Paraphrasing (NeurIPS 2025): https://arxiv.org/abs/2506.07001
- DIPPER (NeurIPS 2023): https://arxiv.org/abs/2303.13408
- MASH (ACL Findings 2026): https://arxiv.org/abs/2601.08564
- TempParaphraser (EMNLP 2025): https://aclanthology.org/2025.emnlp-main.1607/
- Jemama fidelity vs perplexity: https://arxiv.org/abs/2509.24930
- Holtzman nucleus sampling: https://arxiv.org/abs/1904.09751
- Meister locally typical sampling: https://arxiv.org/abs/2202.00666
- Min-p sampling: https://arxiv.org/abs/2407.01082

### Practitioner / craft
- r/WritingWithAI structural thesis: https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/
- Microsoft Copilot humanize guide: https://www.microsoft.com/en-us/microsoft-copilot/copilot-101/humanize-ai-text
- Cat 14 SYNTHESIS (structure-first humanization): `docs/research/14-creative-writing-storytelling/SYNTHESIS.md`
- Cat 04 SYNTHESIS (decoding vs post-hoc): `docs/research/04-natural-language-quality/SYNTHESIS.md`

### unslop implementation
- `unslop/scripts/structural.py`
- `unslop/scripts/validate.py` — `_burstiness`, `_count_flat_paragraphs`
- `unslop/scripts/stylometry.py` — `sentence_length_*`
- `tests/unslop/test_structural.py`
- `skills/unslop/SKILL.md` — anti-detector burstiness band (step 1)

---

## 9. One-paragraph distillation

Sentence-length variance restoration is the post-hoc fix for a generation-time failure: LLMs produce clausally uniform prose that detectors read via σ, CV, consecutive Δ, and fragment/long-sentence presence — even when mean length matches human writing (Desaire 2023). unslop's `structural.py` restores variance conservatively by splitting overlong sentences in flat paragraphs (σ < 5, default) at safe boundaries and merging parallel bullet soup; it runs after lexical scrub because naive paraphrase alone worsens modern detector scores (Adversarial Paraphrasing 2025). The module covers the **split half** of human rhythm; short-sentence and fragment injection remain in anti-detector LLM mode. Deterministic restoration is auditable and preservation-safe but cannot alone hit the σ ≥ 6 target band — full defense requires LLM texture passes, contractions, and optionally surprisal-variance work on the orthogonal token axis.
