# Agent #48 — ZeroStylus Document-Level Style Transfer (arXiv 2505.07888)

**Topic:** ZeroStylus hierarchical long-text style transfer — method, evaluation, gaps, unslop integration  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**ZeroStylus is not an AI-text detector and not a slop stripper.** It is a zero-shot **long-text style transfer** framework: given source prose and reference documents in a target style, it rewrites paragraph-by-paragraph while preserving content and aligning rhetorical structure. The core claim: sentence-level transfer alone causes **style drift** and **content leakage** on long inputs; paragraph-level template matching fixes both.

The method builds two dynamic repositories from reference texts — **Γ_s** (sentence templates via DBSCAN on encoder embeddings) and **Γ_p** (paragraph structure templates via hierarchical aggregation) — then rewrites each source sentence conditioned on matched sentence + paragraph templates, followed by a paragraph coherence refinement pass. No fine-tuning, no parallel corpora. Evaluated on academic paragraphs from ArxivPapers / Arxiv 10 with GPT-4o and DeepSeek-R1.

Results are **real but modest**: full StructuredRewritten averages **6.90** on a tri-axial score vs **6.70** for DirectPrompt (+0.20). The win is **content preservation at stylization strength** — TemplateOnly gets higher style scores but wrecks semantics; DirectPrompt preserves content but stylizes only opening paragraphs. Adversarial pairwise tests show StructuredRewritten beats sentence-only ablations on content preservation (~57% win rate) while tying on expression quality.

For **unslop**, ZeroStylus occupies the **macro-structure layer** voice-match currently lacks. `stylometry.py` + `style_memory.py` capture micro-signals; `structural.py` rebalances sentence length locally. ZeroStylus models **discourse templates** — how paragraphs develop arguments. Treat it as a **Phase 9 blueprint** for document-level voice consistency, not a drop-in for deterministic anti-slop. **No public code** as of August 2026.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **arXiv abstract** | https://arxiv.org/abs/2505.07888 |
| **arXiv HTML (v1)** | https://arxiv.org/html/2505.07888v1 |
| **arXiv PDF** | https://arxiv.org/pdf/2505.07888 |
| **DOI** | https://doi.org/10.48550/arxiv.2505.07888 |
| **OpenReview** | https://openreview.net/forum?id=NoeyaHgrFX |
| **OpenReview PDF** | https://openreview.net/pdf?id=NoeyaHgrFX |

**Authors:** Yusen Wu, Xiaotie Deng. **Code:** none linked from arXiv or OpenReview — reimplementation requires reproducing DBSCAN clustering, Γ_p threshold ε, and Phase 2 prompts not fully specified in the PDF.

### Key related work

| Work | URL | Relationship |
|------|-----|--------------|
| Roy ConvTransfer (baseline) | https://arxiv.org/abs/2302.08362 | Sentence-level dialogue TST |
| Syed StyleLM / DirectPrompt analogue | https://arxiv.org/abs/1909.09962 | Non-parallel author rewrite |
| Tao CAT-LLM | https://arxiv.org/abs/2401.05707 | Document-level (Chinese, parallel data) |
| Chen & Moscholios 2024 | https://arxiv.org/abs/2410.03848 | ICL author imitation (short text) |
| Riley TextSETTR | https://arxiv.org/abs/2010.03802 | Few-shot style extraction |
| Jin TST survey | https://arxiv.org/abs/2011.00416 | Problem framing |
| Jemama 2025 | https://arxiv.org/abs/2505.00679 | Style fidelity ≠ detector evasion |
| Interpretable Stylistic Variation 2026 | https://arxiv.org/abs/2604.14111 | RLHF homogenization |
| How LLMs Distort Our Written Language 2026 | https://arxiv.org/abs/2603.18161 | Voice loss at scale |
| Profile-to-PEFT | https://arxiv.org/abs/2510.16282 · https://github.com/TamSiuhin/P2P | Trained hypernetwork LoRA (not zero-shot) |
| Kardas ArxivPapers (eval corpus) | https://arxiv.org/abs/2004.14356 | ZeroStylus test data |

### unslop internal references

| Resource | Path |
|----------|------|
| Style transfer synthesis | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |
| Academic survey §9.7 | `docs/research/10-style-transfer-voice/A-academic.md` |
| Voice-match spec | `skills/unslop/SKILL.md` |
| Stylometry | `unslop/scripts/stylometry.py` |
| Style memory | `unslop/scripts/style_memory.py` |
| Structural pass | `unslop/scripts/structural.py` |
| Humanize pipeline | `unslop/scripts/humanize.py` |

---

## Problem and method

### Why sentence-level transfer fails

Two failure modes on multi-paragraph inputs:

1. **Premature stylization termination.** DirectPrompt (whole doc + "rewrite in style of X") heavily edits early paragraphs and leaves later ones near-original — same drift seen in multi-turn dialogue TST.

2. **Structural incoherence under per-sentence transfer.** TemplateOnly improves stylization coverage but breaks inter-sentential logic (progression, parallelism, referential chains) because style is treated as local surface, not discourse structure.

ZeroStylus thesis: **style lives at sentence and paragraph granularities.** Long-text transfer needs both encoded explicitly.

### Architecture (two phases)

**Inputs:** source text T_s, reference papers {R_1…R_n}, style intensity α ∈ [0,1] (mentioned; limited ablation in PDF).

**Phase 1 — Template acquisition**

- Sentences embedded via π_enc; DBSCAN clusters → sentence templates τ_s ∈ Γ_s.
- Paragraph embedding e_p = π_enc([e_1,…,e_m]); Γ_p grows only when ||e_p − τ_p|| > ε for all existing τ_p.
- Decoupled repos allow partial reference updates without reprocessing full corpus.

**Phase 2 — Template-guided generation**

For each source paragraph:

1. Match each sentence to nearest τ_s; match paragraph to nearest τ_p*.
2. Transform: s'_j = π_gen(s_j, τ_s^j, τ_p*) — sentence template + paragraph template + original semantics.
3. Refine: p^out = π_refine([s'_1,…], τ_p*) — transitions, discourse markers, referential consistency.

**Engineering:** length-constrained chunked rewriting within bounded context windows; GPT-4o and DeepSeek-R1 used as unified π in experiments.

**What it is not:** stylometry/detection, adversarial paraphrase, deterministic regex humanization, or per-user fine-tuning.

---

## Evaluation

- **N = 500** test paragraphs from ArxivPapers and Arxiv 10; 1–5 reference papers per author; reference length ~3× source.
- **Tri-axial metric** v = [x, y, z]: style consistency (paragraph embedding similarity), content preservation (BLEURT + keyword recall), expression quality (human + LLM preference).

| Method | Style (X) | Content (Y) | Expression (Z) | Average |
|--------|-----------|-------------|----------------|---------|
| DirectPrompt | 6.42 | 7.34 | 6.34 | **6.70** |
| ConvTransfer | 7.45 | 6.22 | 6.08 | 6.58 |
| TemplateOnly (no Γ_p) | 7.62 | 5.91 | 6.32 | 6.62 |
| **StructuredRewritten** | 7.39 | 7.04 | 6.26 | **6.90** |

Full method trades ~0.2 style points vs TemplateOnly for **+1.1 content points**. Adversarial ablations: pre-extracted sentence templates beat raw reference matching (~57%); paragraph templates add ~14pp content win rate over sentence-only with expression quality unchanged (~50%).

Evaluators: GPT-4o, DeepSeek-R1, Llama-4 with position-bias mitigation.

---

## Limitations

Authors acknowledge: no systematic long-form benchmark; naive period-based sentence splitting; domain-specific template needs; two-layer ceiling (section types, inter-paragraph roles unexplored).

**Detection angle (non-overlap):** ZeroStylus optimizes alignment to a reference author, not AI-vs-human classification. High tri-axial scores do not imply detector evasion — Jemama 2025 showed perplexity-matched style remains classifier-visible. unslop anti-detector optimizes classifier scores without requiring reference corpora. Shared enemy: **voice drift** over long generations — ZeroStylus via Γ_p templates; unslop via session hooks and persisted `StyleProfile` anchors. Both partial.

**Adoption (Aug 2026):** arXiv May 2025; OpenReview submission active; no GitHub, no HuggingFace weights, no vendor integration visible. Research reference, not production dependency.

---

## unslop integration

### Layer map

```
Document level  (ZeroStylus Γ_p — discourse templates)     NOT IMPLEMENTED
Paragraph level (structural.py — sentence σ, bullet merge)  PARTIAL
Sentence level  (humanize.py — slop regex, em-dash cap)     SHIPPED
Token level     (surprisal.py — DivEye proxies)             OPT-IN
```

unslop humanizes bottom-up. ZeroStylus is top-down: extract macro patterns from reference docs, rewrite chunks under those constraints.

| ZeroStylus concept | unslop module | Fit |
|--------------------|---------------|-----|
| Sentence templates Γ_s | `stylometry.analyze()` | Partial — stats, not rhetorical clusters |
| Paragraph templates Γ_p | `structural.py` | Weak — no argument-flow modeling |
| Reference corpus | `--voice-sample` / `style_memory.py` | Partial — numeric profile, not template repo |
| Style intensity α | subtle→full modes | Analogous, not continuous |
| Content preservation | `validate.py` | Strong — code/URL/heading contract |
| Tri-axial eval | `benchmark.py` | Missing long-doc style/content/fluency split |

### Recommended tiers

**Tier 0 (now):** Cite in Cat 10 docs; note micro-vs-macro voice distinction in voice-match skill; anti-detector ethics: author transfer ≠ detector evasion.

**Tier 1 (eval):** Long-doc fixtures with `StyleProfile.delta()` before/after; optional paragraph-embedding cosine vs reference; report style Δ + content keyword recall + residual AI-ism count. No ZeroStylus reimplementation needed.

**Tier 2 (lightweight):** From `--voice-sample`, count rhetorical move frequencies (opener types, fragment rate, "However"/"We show" patterns) as closed-schema numeric fields in `style_memory.json` — consistent with OWASP memory posture. Inject alongside stylometry deltas in LLM prompt. ~30% of Γ_s value at deterministic cost.

**Tier 3 (opt-in `--document-voice`):** Full pipeline — embed reference corpus, cluster Γ_s/Γ_p, chunked template-guided rewrite, `validate.py` gate per chunk, final transition-refine pass. LLM-cost heavy; 500 KB file cap limits reference size; belongs under voice-match, not default slop removal.

**Do not:** ship as anti-detector escalation; store raw reference paragraphs in style memory (poisoning surface); claim document-level consistency without held-out benchmark.

### Mode matrix

| Mode | ZeroStylus relevance |
|------|---------------------|
| subtle / balanced / full | Low — slop removal ≠ author imitation |
| voice-match | **High** — macro templates extend micro stylometry |
| anti-detector | Low–Medium — structural entropy helps; author templates don't |

Sudowrite claims 80K-word POV consistency without published methodology. ZeroStylus is the first peer-reviewed architectural articulation of document-level consistency — unslop can cite it when explaining why session-level voice-match isn't enough for book-length work.

---

## Bottom line

ZeroStylus names the problem unslop voice-match hits on long documents: **micro-signals drift while discourse structure goes untemplated.** Contribution is architectural (dual repositories, chunked constrained rewrite), not a large absolute jump (+0.20). No code ships. unslop should **learn the hierarchy**, **extend stylometry upward**, **build eval before implementation**. Orthogonal to slop removal and anti-detector; directly relevant to "make this 3,000-word draft sound like my previous essays."

**Maintainer actions:** add tri-axial eval design to long-form benchmark RFC; track OpenReview for code release; extend StyleProfile v2 with optional rhetorical-move counters; do not merge ZeroStylus numbers into README until in-repo runs exist.
