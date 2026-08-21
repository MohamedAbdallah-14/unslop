# Agent #24 — TempParaphraser

**Topic:** Huang et al., *TempParaphraser: "Heating Up" Text to Evade AI-Text Detection through Paraphrasing* (EMNLP 2025)  
**Prepared:** August 19, 2026  
**Scope:** Temperature-simulation paraphrase, 82.5% claim, Fast-DetectGPT/Binoculars comparison, reproductions, critics, unslop `detector.py` integration  
**Status:** complete

---

## Executive summary

TempParaphraser (Huang, Zhang, Su, Chen; Xiamen University) is an EMNLP 2025 attack framework that **simulates high-temperature LLM sampling** without actually decoding at high temperature. The trick: generate **N independent sentence paraphrases at normal temperature**, then **select the candidate with the lowest detector score** per sentence. Jensen's inequality argument: averaging N sharp distributions yields higher ensemble entropy than any single sample — approximating the distributional flattening that makes raw high-temperature text hard to detect.

The headline **"82.5% detector accuracy reduction"** is an **absolute drop in average detection accuracy on HC3** (96.1% → 13.6% across four primary detectors), not a relative 82.5% decrease. On **Fast-DetectGPT** specifically, accuracy falls from **98.9% → 2.6%** (N=7). A separate RAID cross-model/domain figure reports **92.3% average relative reduction** — a different metric on a different benchmark.

**Binoculars is not evaluated in the paper.** TempParaphraser tests SA, RADAR, Fast-DetectGPT, TOCSIN (+ DetectGPT, OpenAI GPT-2, HC3 in appendix). For Binoculars, the closest independent data is NAACL SRW 2025 (Perkins et al.), which finds Binoculars the **most paraphrase-vulnerable** zero-shot detector (F1 drop ~0.196 under generic paraphrase) — consistent with TempParaphraser's mechanism but not a direct replication.

**Unslop already cites TempParaphraser** in `unslop/scripts/detector.py` (feedback-loop exhaustion message), `skills/unslop/SKILL.md` (anti-detector step 6), README, and `docs/RESEARCH_AND_TECH.md`. The integration is **recommendation-only**: when the deterministic `--detector-feedback` ladder exhausts, unslop tells the user to paraphrase through a **different model family** — the practitioner analog of TempParaphraser's cross-distributional rewrite, without shipping the fine-tuned 1B paraphraser or multi-sample selection loop.

**Reproduction grade: medium-high.** Code is public (`HJJWorks/TempParaphraser`), but community uptake is minimal (4 GitHub stars, 0 forks as of Aug 2026), no independent replication found, and the pipeline requires LLaMA-Factory + VLLM + GPU fine-tuning — not a drop-in script.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | TempParaphraser: "Heating Up" Text to Evade AI-Text Detection through Paraphrasing |
| **Authors** | Junjie Huang, Ruiquan Zhang, Jinsong Su, Yidong Chen (Xiamen University) |
| **Venue** | EMNLP 2025 Main, Suzhou, China (November 2025) |
| **Pages** | 31554–31573 |
| **Anthology ID** | 2025.emnlp-main.1607 |
| **DOI** | [10.18653/v1/2025.emnlp-main.1607](https://doi.org/10.18653/v1/2025.emnlp-main.1607) |
| **ACL Anthology** | https://aclanthology.org/2025.emnlp-main.1607/ |
| **PDF** | https://aclanthology.org/2025.emnlp-main.1607.pdf |
| **Checklist PDF** | https://aclanthology.org/2025.emnlp-main.1607.checklist.pdf |
| **Code** | https://github.com/HJJWorks/TempParaphraser |
| **arXiv** | Not indexed in unslop code; paper appears Anthology-only (no arXiv ID in ACL entry) |

**One-line contribution:** Exploit temperature vulnerability in statistical/neural detectors via multi-sample sentence paraphrase + detector-guided selection; dual-use as adversarial benchmark and detector training augmentation.

---

## 2. Mechanism — "heating up" without high temperature

### 2.1 Observed vulnerability

Preliminary experiment (Dolly 3K, Llama-3.1-8B-Instruct): as decoding **temperature rises**, both statistical and neural detectors assign **lower AI confidence**. High temperature increases conditional token entropy, collapsing the distributional gap detectors exploit:

\[
H(p_{\text{AI}}(\cdot \mid t_{<j})) < H(p_{\text{Human}}(\cdot \mid t_{<j}))
\]

**Problem:** raw high-temperature generation degrades readability (PPL spikes, Flesch drops — Appendix B).

### 2.2 TempParaphraser workaround

Instead of decoding at T=1.9, TempParaphraser:

1. **Segments** text into sentences (period-split; sentences <4 words skipped)
2. **Generates N paraphrase candidates** per sentence from a **fine-tuned 1–3B instruct model** at normal temperature (main experiments: **N=7, T=1.2**)
3. **Scores each candidate** with an open-source detector
4. **Selects lowest-score candidate** per sentence
5. **Reassembles** the document

Theoretical hook (Section 4.1): ensemble distribution \(p_{\text{avg}}\) over N independent normal-temperature samples has entropy ≥ average individual entropy (Jensen). Multi-sample selection increases the chance of landing on a low-detector-confidence trajectory — mimicking high-T evasion while keeping per-candidate quality controlled.

### 2.3 Paraphrasing model

| Component | Detail |
|-----------|--------|
| **Base model** | Llama-3.2-1B-Instruct (main); also tested Phi-2, Llama-3.2-3B, Qwen2.5-1.5B |
| **Training data** | 151,189 pairs from The Pile; Llama-3.1-8B synthetic paraphrase → human sentence as target |
| **Filtering** | SA detector score, Stella embedding cosine ≥0.6, n-gram diversity heuristic, rule filters |
| **Training** | LLaMA-Factory full fine-tune; lr 2e-5, batch 32, ~3h on NVIDIA L40 |
| **Inference backend** | VLLM via LLaMA-Factory (separate Conda env recommended) |

**Not training-free.** Despite some secondary unslop docs calling it a "cheap structural lever with no LLM call," the published method **requires a fine-tuned paraphraser + N× inference + detector scoring**. What is cheap relative to RL attacks (StealthRL, AuthorMist) is the **absence of adversarial fine-tuning against a specific detector API**.

---

## 3. The 82.5% claim — decoded

### 3.1 Primary result (HC3, Table 1, N=7)

Attack on 3,218 AI-generated ChatGPT answers from HC3 test subset. Detection accuracy = recall on AI-positive class (threshold 0.5).

| Detector | Origin accuracy | After TempParaphraser (N=7) | Absolute drop (pp) | Relative drop |
|----------|----------------:|----------------------------:|-------------------:|--------------:|
| **SA** (SuperAnnotate) | 99.8% | **1.9%** | 97.9 | 98.1% |
| **Fast-DetectGPT** | 98.9% | **2.6%** | 96.3 | 97.4% |
| **TOCSIN** | 95.5% | **4.5%** | 91.0 | 95.3% |
| **RADAR** | 90.0% | **45.4%** | 44.6 | 49.6% |
| **Average (4 detectors)** | **96.1%** | **13.6%** | **82.5** | 85.8% |

**The abstract's "82.5%" = 96.1 − 13.6 percentage points on average accuracy.** Not "detectors now operate at 17.5% of original accuracy."

### 3.2 Secondary result (RAID, Figure 6)

Across **5 LLMs × 6 domains** on RAID (500 samples per cell, Fast-DetectGPT heatmaps in main text): **92.3% average relative reduction** in detection accuracy. Appendix E.4 extends to HC3 and SA detectors.

### 3.3 Quality preservation (same table)

| Metric | TempParaphraser N=7 | Best baseline |
|--------|--------------------:|--------------|
| \|∆PPL\| vs human RAID benchmark | **2.532** | HMGC 3.629 |
| Flesch reading ease | **66.159** | Ours N=1 66.747 |
| Semantic similarity (Sim) | **0.958** | WordNet 0.974 |
| Human readability (1–5) | **3.78** | AI origin 4.47; human 3.89 |

Human eval: attacked text stays fluent (mean 3.78) and near human-written (3.89).

### 3.4 Baseline comparison highlights

TempParaphraser N=7 vs prior attacks on **average 4-detector accuracy**:

| Method | Avg accuracy after attack |
|--------|--------------------------:|
| Origin AI text | 96.1% |
| DIPPER | 72.1% |
| Recursive Paraphrase (Sadasivan-style) | 72.1% |
| HMGC | 27.2% |
| RAFT | 45.5% |
| **TempParaphraser N=7** | **13.6%** |

Notable: **BackTrans increases detectability** on RADAR (94.3% → more detectable). **WordNet/BERT** crush Fast-DetectGPT/TOCSIN but barely touch SA. TempParaphraser is the only method that hits all four primary detectors hard.

---

## 4. vs Fast-DetectGPT and Binoculars

### 4.1 Fast-DetectGPT — directly tested, severely degraded

**Fast-DetectGPT** (Bao et al., ICLR 2024; [arXiv:2310.05130](https://arxiv.org/abs/2310.05130); [github.com/baoguangsheng/fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt)) uses **conditional probability curvature** — a zero-shot statistical signal in the DetectGPT family, ~340× faster than DetectGPT.

TempParaphraser explicitly lists Fast-DetectGPT as a primary evaluation detector and borrows its codebase. Results:

| Setting | Fast-DetectGPT accuracy |
|---------|------------------------:|
| Origin AI (HC3) | 98.9% |
| WordNet attack | 46.5% |
| DIPPER | 72.9% |
| HMGC | 5.3% |
| **TempParaphraser N=7** | **2.6%** |
| TempParaphraser N=1 (ablation) | 8.5% |

Appendix Table 3 (7 detectors): Fast-DetectGPT origin 98.9% → TempParaphraser N=7 **2.6%**. ROC-AUC drops from 0.997 → 0.525.

**Mechanism fit:** Fast-DetectGPT assumes AI text sits in a low-curvature, high-confidence token band. Multi-sample paraphrase + lowest-score selection pushes text toward higher-entropy, human-like token choices — exactly the temperature vulnerability the paper theorizes.

TempParaphraser repo **depends on** Fast-Detect-GPT as a forked evaluation dependency ([github.com/baoguangsheng/fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt)).

### 4.2 Binoculars — not in paper; indirect evidence only

**Binoculars** (Hans et al., ICML 2024; [arXiv:2401.12070](https://arxiv.org/abs/2401.12070); [proceedings.mlr.press/v235/hans24a.html](https://proceedings.mlr.press/v235/hans24a.html); [github.com/ahans30/Binoculars](https://github.com/ahans30/Binoculars)) scores text via **log-perplexity / log-cross-perplexity** ratio between observer and performer LMs. SOTA zero-shot on ChatGPT at 0.01% FPR in original evaluation.

**TempParaphraser does not report Binoculars numbers.** Gap is notable because Binoculars is often grouped with Fast-DetectGPT as a 2024 zero-shot SOTA.

**Indirect paraphrase vulnerability** — Perkins et al., *Paraphrasing Attack Resilience of Various AI-Generated Text Detection Methods* (NAACL SRW 2025; [aclanthology.org/2025.naacl-srw.46](https://aclanthology.org/2025.naacl-srw.46); [arXiv:2605.14240](https://arxiv.org/html/2605.14240)):

| Detector | F1 before paraphrase | F1 after | Δ F1 |
|----------|---------------------:|---------:|-----:|
| RoBERTa | 0.7586 | 0.7586 | ~0 |
| Text Features | 0.7207 | 0.6682 | 0.0526 |
| **Binoculars** | 0.5765 | 0.3800 | **~0.196** |
| TF + RoBERTa + Binoculars ensemble | 0.8061 | 0.6716 | 0.1345 |

Binoculars' cross-perplexity ratio is **highly sensitive to structural rewording** — the attack class TempParaphraser formalizes. Expect TempParaphraser-style multi-sample selection to hit Binoculars at least as hard as generic paraphrase, but **this remains extrapolation until someone runs the experiment**.

### 4.3 Cross-detector selection generalization (Table 8)

TempParaphraser uses **one detector to pick candidates** but evades **others**:

| Selector → Target | HC3 | SA | Fast-DetectGPT | TOCSIN | RADAR |
|-------------------|----:|---:|---------------:|-------:|------:|
| HC3 selector | 2.1% | ~0% | 2.7% | 3.7% | 44.4% |
| SA selector | 19.2% | 1.9% | 0% | — | — |
| Fast-DetectGPT selector | 39.4% | 7.1% | 0% | 1.2% | 50.4% |

Key finding: **exploiting shared detection mechanism** — any single open detector as selector transfers to other detectors without white-box weight access.

---

## 5. Additional attack surfaces tested

| Target | Result |
|--------|--------|
| **Watermarks** (Kirchenbauer et al. 2023; Llama-3.1-8B) | Detection 56% → **1.7%** after TempParaphraser |
| **5 source LLMs × 6 RAID domains** | Consistent Fast-DetectGPT heatmap collapse (Figure 6) |
| **Detector-augmented training** | RoBERTa fine-tuned on 5% TempParaphraser-augmented HC3 resists high-T generation better (Figure 9) |

---

## 6. Reproductions and repo status

### 6.1 Official repo

| Item | Status |
|------|--------|
| **URL** | https://github.com/HJJWorks/TempParaphraser |
| **Stars / forks** | 4 / 0 (Aug 2026) |
| **License** | Not prominently listed in README fetch |
| **Stack** | LLaMA-Factory, VLLM, Fast-Detect-GPT fork, HMGC, SuperAnnotate detector, textstat |
| **Pipeline** | Data synthesis → fine-tune paraphraser → iterate GPT samples → sentence paraphrase → save attacked corpus |
| **Known limitation** | Period-based English sentence split; authors recommend [BlingFire](https://github.com/microsoft/BlingFire) upgrade |

### 6.2 Independent reproduction

**None found** as of Aug 2026. Unslop research corpus (`docs/research/17-industry-blogs-case-studies/C-opensource.md`): *"TempParaphraser (EMNLP 2025) benchmarks against updated detectors but hasn't been replicated independently."*

Repro hurdles:
- Fine-tune step (~3h L40, 151K pairs)
- Separate LLaMA-Factory Conda env
- Detector stack alignment (SA, Fast-DetectGPT checkpoints)
- HC3/RAID subset selection matching Zhou et al. 2024 protocol

**Internal repro grade:** `[Repro: high]` in `docs/research/15-academic-papers-llm-humanization/A-academic.md` refers to **code availability**, not community verification.

### 6.3 Related contemporaneous attacks (context, not reproductions)

| Paper | vs Fast-DetectGPT | Relation |
|-------|-------------------|----------|
| **CoPA** ([arXiv:2505.15337](https://arxiv.org/abs/2505.15337)) | +57.72% fooling rate (FPR=5%) | Contrastive decoding; prompt-based, no fine-tune |
| **Adversarial Paraphrasing** ([arXiv:2506.07001](https://arxiv.org/abs/2506.07001)) | 87.88% relative TPR drop | Detector-guided token selection; NeurIPS 2025 |
| **HMGC / RAFT** | TempParaphraser beats both on avg accuracy | Token-level adversarial baselines in same table |
| **DIPPER** ([NeurIPS 2023](https://arxiv.org/abs/2305.13439)) | 72.9% Fast-DetectGPT accuracy vs 2.6% | Prior paraphrase SOTA; TempParaphraser's explicit predecessor |

---

## 7. Critics, limitations, and misreadings

### 7.1 Authors' stated limitations

1. **Sentence-level only** — long-range coherence loss on complex documents; context not passed between sentences during paraphrase.
2. **English period splitter** — brittle on abbreviations, decimals, non-English.
3. **RADAR residual robustness** — still 45.4% accuracy post-attack (hardest detector; adversarially trained against paraphrase).
4. **Dual-use framing** — paper positions attack as robustness research + training augmentation, not evasion tooling (Ethical Considerations section).

### 7.2 External critique vectors

| Critique | Detail |
|----------|--------|
| **Benchmark staleness** | HC3 is ChatGPT-centric (2023). RAID helps but commercial detectors (GPTZero v6, Turnitin 2026 anti-humanizer training) moved since paper submission. |
| **No Binoculars / commercial eval** | Zero-shot SOTA most cited in 2026 practitioner workflows not in primary table. |
| **Detector-guided selection = oracle-ish** | Attacker uses detector scores at rewrite time. Strong for robustness eval; differs from black-box humanizer who lacks local TMR/RoBERTa. Unslop's user-facing recommendation (different-model rewrite) is **blind** to detector scores unless `--detector-feedback` is running. |
| **Headline metric ambiguity** | "82.5% reduction" reads as relative%; it is **82.5 pp average accuracy drop**. Marketing hazard. |
| **Low OSS adoption** | 4 stars suggests limited battle-testing outside authors' lab. |
| **"Training-free" mislabel** | Fine-tuned 1B paraphraser required; only the *temperature simulation insight* transfers without fine-tuning (multi-sample + pick-most-human-like heuristic). |

### 7.3 Documentation bug in unslop

`unslop/scripts/detector.py:390–392` comment says TempParaphraser achieves evasion **"with no LLM call needed."** That is **incorrect for TempParaphraser itself** (requires fine-tuned LLM inference). The intended meaning is likely: *after unslop's deterministic ladder exhausts, the remaining lever is an LLM paraphrase outside this module.* Worth a follow-up edit to separate **TempParaphraser the paper** from **cross-model rewrite the recommendation**.

Similarly, `docs/research/IMPLEMENTATION_TRACE.md` calls it "no LLM call needed on the attacker side" — wrong for the paper; right only if mapping to unslop's regex-only passes.

---

## 8. unslop integration — current state and recommended path

### 8.1 Where TempParaphraser is cited today

| Location | What it says |
|----------|--------------|
| `unslop/scripts/detector.py:389–407` | Ladder exhaustion → recommend cross-model paraphrase; cites TempParaphraser (EMNLP 2025) + Adversarial Paraphrasing (NeurIPS 2025); prohibits watermark removal (EU AI Act Art. 50) |
| `skills/unslop/SKILL.md` step 6 | Anti-detector mode: different-family second pass; 82.5% figure; `--detector-feedback` prints recommendation |
| `README.md` ~L603 | Same recommendation in anti-detector guidance |
| `docs/RESEARCH_AND_TECH.md` | Names ACL Anthology ID; notes arXiv not recorded |
| `CHANGELOG.md` / `unslop/CHANGELOG.md` | Cross-model paraphrase recommendation shipped |

### 8.2 What unslop does NOT implement

From `UPDATE-PLAN-2026-08.md`:

| TempParaphraser feature | unslop status |
|-------------------------|---------------|
| Multi-sample sentence paraphrase (N=7) | **Partial** — no N-candidate generation |
| Fine-tuned 1B paraphraser | **No** — no bundled model |
| Detector-guided per-sentence selection | **Partial** — `--detector-feedback` loop scores whole text, not per-sentence argmin |
| Temperature-simulation theory | **No** — not in deterministic passes |
| Phase 3 `llm_pipeline.py` S3 stage | **Planned** — "TempParaphraser multi-sample: 2 batched (hot sentences × N candidates)" |

### 8.3 Recommended integration (cross-model technique)

TempParaphraser's **transferable insight for unslop** is not the fine-tuned weights — it is the **procedure**:

```
For each high-surprisal or detector-flagged sentence:
  1. Generate N paraphrases via Model B (different family from Model A author)
  2. Score each with local detector (TMR / Fast-DetectGPT if wired)
  3. Keep lowest p_ai candidate that passes preservation validator
```

**Practitioner mapping (already shipped as recommendation):**

| TempParaphraser component | unslop equivalent |
|---------------------------|-------------------|
| Fine-tuned paraphraser | User runs Claude ↔ GPT ↔ Gemini rewrite |
| N samples at T=1.2 | User regenerates 2–3 variants (manual or `--llm` batch) |
| Detector argmin selection | `--detector-feedback` loop OR user picks lowest-scoring variant |
| Sentence segmentation | `structural.py` paragraph/sentence passes (upgrade to BlingFire optional) |

**Priority for Phase 3** (`UPDATE-PLAN-2026-08.md` §Phase 3): implement **S3 TempParaphraser multi-sample** as an LLM pipeline stage — batched hot-sentence rewrite with detector pick — without shipping HMGC/StealthRL fine-tuning.

**Boundary (keep):** Anti-detector mode remains defensive (ESL false positives, resume polish). Cite TempParaphraser as **research basis for cross-model paraphrase**, not as instruction to evade academic integrity systems.

---

## 9. Position in unslop research stack

| Layer | TempParaphraser role |
|-------|---------------------|
| **Sadasivan TV bound** (Agent #17) | TempParaphraser operationalizes paraphrase-as-TV-reduction at scale |
| **DivEye / surprisal variance** | Orthogonal signal; TempParaphraser raises entropy but may not widen surprisal σ — verify on TSD bench |
| **Adversarial Paraphrasing** | Complementary; detector-guided like TempParaphraser §4.2.3 but token-level and NeurIPS 2025 |
| **DIPPER** | Superseded as research baseline per `docs/research/17-industry-blogs-case-studies/SYNTHESIS.md` |
| **Commercial detectors** | Paper predates GPTZero v6 cones, Turnitin 2026 anti-humanizer — treat HC3 numbers as ceiling not floor |

---

## 10. Key numbers cheat sheet

| Metric | Value | Source |
|--------|------:|--------|
| Avg 4-detector accuracy drop | **82.5 pp** (96.1→13.6%) | Table 1, N=7 |
| Fast-DetectGPT after attack | **2.6%** (from 98.9%) | Table 1 |
| SA after attack | **1.9%** (from 99.8%) | Table 1 |
| RADAR after attack | **45.4%** (from 90.0%) | Table 1 |
| RAID cross-model avg relative drop | **92.3%** | §5.2 / Figure 6 |
| Watermark detection after attack | **1.7%** (from 56%) | Appendix E.5 |
| Main hyperparameters | **N=7, T=1.2** | §5, Appendix D |
| Training pairs | **151,189** | Appendix C |
| Human readability | **3.78 / 5** | Table 7 |

---

## 11. URL index

### Primary

- ACL Anthology entry: https://aclanthology.org/2025.emnlp-main.1607/
- PDF: https://aclanthology.org/2025.emnlp-main.1607.pdf
- DOI: https://doi.org/10.18653/v1/2025.emnlp-main.1607
- GitHub: https://github.com/HJJWorks/TempParaphraser

### Detectors discussed

- Fast-DetectGPT paper: https://arxiv.org/abs/2310.05130
- Fast-DetectGPT code: https://github.com/baoguangsheng/fast-detect-gpt
- Fast-DetectGPT demo: https://fastdetect.net
- Binoculars paper: https://arxiv.org/abs/2401.12070
- Binoculars proceedings: https://proceedings.mlr.press/v235/hans24a.html
- Binoculars code: https://github.com/ahans30/Binoculars
- DetectGPT: https://arxiv.org/abs/2301.11305
- RADAR: https://arxiv.org/abs/2307.03893
- TOCSIN (Ma & Wang 2024): cited in TempParaphraser refs
- SuperAnnotate detector: https://github.com/superannotateai/generated_text_detector

### Datasets

- HC3: https://arxiv.org/abs/2301.07554
- RAID: https://aclanthology.org/2024.acl-long.866/

### Related attacks / defenses

- DIPPER: https://arxiv.org/abs/2305.13439
- Sadasivan impossibility: https://arxiv.org/abs/2303.11156
- Adversarial Paraphrasing: https://arxiv.org/abs/2506.07001
- CoPA: https://arxiv.org/abs/2505.15337
- HMGC: https://github.com/zhouying20/HMGC
- Paraphrase resilience (Binoculars vulnerability): https://aclanthology.org/2025.naacl-srw.46
- Watermarking (Kirchenbauer): https://arxiv.org/abs/2301.10226

### unslop internals

- `unslop/scripts/detector.py` — feedback loop + recommendation
- `skills/unslop/SKILL.md` — anti-detector step 6
- `docs/RESEARCH_AND_TECH.md` — product-facing research summary
- `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md` — Phase 3 LLM pipeline plan

---

## 12. Bottom line for unslop maintainers

1. **Keep citing TempParaphraser** in ladder-exhaustion messaging — it is the best peer-reviewed anchor for "different model family rewrite" in 2025–2026 literature.
2. **Fix the "no LLM call" comment** in `detector.py` — TempParaphraser requires LLM inference; unslop's deterministic layer does not.
3. **Quote 82.5% correctly** — average **percentage-point** accuracy drop on four detectors, not relative percent.
4. **Do not claim Binoculars results** — not in paper; cite Perkins NAACL SRW 2025 for Binoculars paraphrase fragility separately.
5. **Phase 3 win:** per-sentence N-candidate LLM paraphrase + detector argmin is the faithful TempParaphraser implementation path; cross-model family satisfies the distributional shift the paper targets.
6. **Treat RADAR 45.4% as the honest floor** — paraphrase-hardened detectors remain partially effective; unslop should not imply universal evasion.

---

*Agent #24 complete. Cross-reference: Agent #17 (Sadasivan), Agent #38 (repo reproduction — pending), UPDATE-PLAN Phase 3 S3.*
