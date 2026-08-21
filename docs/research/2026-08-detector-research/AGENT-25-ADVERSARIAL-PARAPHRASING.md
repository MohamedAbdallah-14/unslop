# Agent #25 — Adversarial Paraphrasing (NeurIPS 2025)

**Topic:** Detector-guided token search for universal AI-text humanization  
**Paper:** Cheng et al., *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text*  
**Venue:** NeurIPS 2025 · arXiv:2506.07001  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Cheng et al. (UMD) introduce **Adversarial Paraphrasing (AdvPara)**: a **training-free**, **gradient-free** attack that humanizes AI text by steering an instruction-following LLM with live detector scores at **every autoregressive token step**. It is not "paraphrase harder." It is **depth-1 detector-guided beam search** over the paraphraser's top-*k* candidates.

Three numbers define the field:

| Metric | Simple (naive) paraphrase | AdvPara (RoBERTa-Large guidance) |
|--------|---------------------------|----------------------------------|
| **Fast-DetectGPT T@1%F change** | **+15.03%** (ironic increase — easier to detect) | **−98.96%** relative drop |
| **RADAR T@1%F change** | **+8.57%** (ironic increase) | **−64.49%** relative drop |
| **Average across 8 detectors** | ~30.27% relative drop (mixed; some detectors get worse) | **−87.88%** relative drop |

**unslop verdict:** AdvPara is the canonical proof that **lexical-only humanization is not neutral — on modern detectors it is often a regression**. The paper's simple-paraphrase baseline is synonym-level rewriting by a strong LLM; that *raises* detector TPR on RADAR and Fast-DetectGPT. unslop already cites this in `structural.py` and routes around it with Phase 1 structural passes (`split_long_sentences`, `merge_bullet_soup`) after lexical scrubbing. What unslop does **not** ship is the paper's token-level detector loop — that lives in `chengez/Adversarial-Paraphrasing` and is referenced from `detector.py` as the escalation path when the deterministic ladder exhausts.

**Author note:** Correct citation is **Cheng et al.** Some unslop docs still say "Chakraborty et al." — wrong paper, wrong authors.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv abstract + PDF)** | https://arxiv.org/abs/2506.07001 |
| **Paper (HTML v1)** | https://arxiv.org/html/2506.07001v1 |
| **OpenReview (NeurIPS 2025)** | https://openreview.net/forum?id=fYjF9KIJd5 |
| **Official code** | https://github.com/chengez/Adversarial-Paraphrasing |
| **Core algorithm** | https://github.com/chengez/Adversarial-Paraphrasing/blob/main/utils.py |
| **Entry script** | https://github.com/chengez/Adversarial-Paraphrasing/blob/main/paraphrase_and_detect.py |
| **HuggingFace Papers page** | https://huggingface.co/papers/2506.07001 |
| **Contact (authors)** | yzcheng@cs.umd.edu · vinu@cs.umd.edu |

### Detectors evaluated in paper (upstream repos)

| Detector | Paper | URL |
|----------|-------|-----|
| OpenAI-RoBERTa-Large / Base | Solaiman et al. 2019 | https://arxiv.org/abs/1905.12616 |
| MAGE | Li et al. 2023 | https://arxiv.org/abs/2305.14902 |
| RADAR | Hu et al. NeurIPS 2023 | https://arxiv.org/abs/2307.03838 |
| Fast-DetectGPT | Bao et al. 2023 | https://arxiv.org/abs/2310.05130 |
| GLTR | Gehrmann et al. 2019 | https://arxiv.org/abs/1906.04043 |
| KGW watermark | Kirchenbauer et al. 2023 | https://arxiv.org/abs/2301.10226 |
| Unigram watermark | Zhao et al. 2023 | https://arxiv.org/abs/2306.17439 |

### Lineage papers (direct predecessors)

| Paper | URL | Relation |
|-------|-----|----------|
| Sadasivan et al. — *Can AI-Generated Text be Reliably Detected?* | https://arxiv.org/abs/2305.18226 | Paraphrase breaks detectors; TV bound; recursive paraphrase baseline |
| Krishna et al. — DIPPER (NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Strong T5 paraphraser baseline; DetectGPT 70.3% → 4.6% |
| BEAST (jailbreak beam search) | NeurIPS 2024 | Closest prior: gradient-free beam guidance, different objective |
| PPLM / InstructCTG | https://arxiv.org/abs/1912.02164 · https://arxiv.org/abs/2308.15459 | Controlled generation lineage; AdvPara is gradient-free + off-the-shelf |

### Benchmark / audit papers that cite AdvPara

| Paper | URL | Relation |
|-------|-----|----------|
| TH-Bench | https://arxiv.org/abs/2503.08708 | 6 attacks × 13 detectors × 19 domains; no attack wins all axes |
| DAMAGE (COLING 2025) | https://arxiv.org/abs/2501.03437 | Audits 19 commercial humanizers; AdvPara is academic ceiling |
| StealthRL (2026) | https://arxiv.org/abs/2602.08934 | RL-trained paraphraser; 97.6% ASR; confirms transferability thesis |

---

## Mechanism: detector-guided token search

### Algorithm (training-free, depth-1 beam)

At each autoregressive step of paraphrase generation:

```
1. Paraphraser P (LLaMA-3-8B-Instruct + system prompt) → next-token logits p(·|context)
2. Filter: top-p (p=0.99) ∘ top-k (k=50) → candidate set C
3. Decode each candidate token in C to text fragment
4. For each c ∈ C: score D(y_so_far ⊕ c) with guidance detector D
5. Append argmin_c D(·) — token with lowest "AI score"
6. Repeat until <EOS>
```

**Guidance detector** ≠ **deployed detector**. The attack uses one trained classifier (e.g. OpenAI-RoBERTa-Large) to steer token choice, then evaluates transfer to eight held-out detectors including zero-shot (Fast-DetectGPT, GLTR), watermark (KGW, Unigram), and adversarially trained RADAR.

### Paraphraser setup

System prompt configures any instruction-tuned LLM as a rephraser: must change style, not just swap a few words, preserve meaning, wrap output in tags. Paper uses **LLaMA-3-8B-Instruct**. Simple baseline uses the same model with standard sampling (no detector guidance).

### Transferability intuition (paper's core claim)

High-performing detectors converge on a shared estimate of the human-text distribution (minimize FPR). Steering away from one well-trained detector's "AI region" pushes text toward that shared human manifold — so evasion **transfers** to unseen detectors, watermarks, and zero-shot methods. Figure 4 in the paper plots the full guidance×deployed T@1%F drop matrix; all 4×4 neural guidance choices yield >80% average relative drops.

### Efficiency

Per-sample runtime (100 samples, batch=1): simple paraphrase **7.18±0.13 s**; AdvPara with RoBERTa-Large guidance **10.20±0.18 s** (~42% overhead). Detectors are 100–350M params vs 8B paraphraser — detector adds <5% FLOPs. MAGE guidance is slowest (LongFormer, 16.71 s) due to architecture, not algorithm.

### Quality tradeoff

| Metric | Simple paraphrase | AdvPara (RoBERTa-Large) | Human (MAGE) |
|--------|-------------------|-------------------------|--------------|
| Perplexity (LLaMA-3.1-8B) | **9.28±3.86** (too smooth) | **14.26±4.97** (human-like band) | 15.02±7.71 |
| SBERT cosine vs original | 0.8601±0.0880 | 0.8082±0.1006 | — |
| GPT-4o quality rating | 4.75±0.54 | 4.48±0.77 | — |

Simple paraphrase **oversmooths** — lower perplexity than original AI text. AdvPara lands near human perplexity. Semantic similarity drops slightly; GPT-4o head-to-head win rate shows simple paraphrase wins <50% of comparisons in most configs — quality cost is small relative to evasion gain.

---

## Headline results (Table 2, RoBERTa-Large guidance)

**Deployed detector T@1%F (true positive rate at 1% false positive rate):**

| Detector | No attack | Simple paraphrase | AdvPara | Relative drop (AdvPara) |
|----------|-----------|-------------------|---------|-------------------------|
| OpenAI-RoBERTa-Large | 0.163 | 0.096 | **0.000** | ~100% |
| OpenAI-RoBERTa-Base | 0.182 | 0.119 | **0.000** | ~100% |
| MAGE | 0.768 | 0.616 | **0.142** | ~81.5% |
| RADAR | 0.124 | **0.140** ↑ | **0.044** | ~64.5% |
| KGW watermark | 1.000 | 0.295 | **0.131** | ~86.9% |
| Unigram watermark | 0.999 | 0.609 | **0.294** | ~70.6% |
| **Fast-DetectGPT** | 0.323 | **0.326** ↑ | **0.003** | **~98.96%** |
| GLTR | 0.174 | 0.049 | **0.001** | ~99.4% |

**The ironic finding:** On RADAR and Fast-DetectGPT, **simple paraphrase increases T@1%F** relative to unattacked AI text (+8.57% and +15.03% respectively, per abstract). Naive rewriting makes detection *easier*, not harder. RADAR was adversarially trained against paraphrase — it learns paraphrase artifacts. Fast-DetectGPT reads curvature; a fluent LLaMA-3 rewrite can sharpen the very statistical regularities zero-shot detectors target.

**Average relative T@1%F drop** across all guidance×deployed pairs when using RoBERTa-Large guidance: **87.88%**.

---

## Why lexical-only is regression (`structural.py` citation)

### What the paper shows

1. **Simple paraphrase = lexical/surface rewrite** by a capable LLM. It changes words and light syntax but preserves the **macro-statistical envelope** — and often tightens it (perplexity 14.94 → 9.28).
2. **Modern detectors don't only read vocabulary.** Fast-DetectGPT uses conditional probability curvature; RADAR was trained on paraphrased AI text; GLTR reads rank histograms. Surface synonym swap without distributional reshaping can **amplify** detectable signals.
3. **AdvPara succeeds by moving the full generative trajectory** — each token chosen to minimize detector score, producing human-band perplexity and cross-detector transfer.

### What unslop cites in code

```6:9:unslop/scripts/structural.py
Adversarial Paraphrasing (NeurIPS 2025) showed that synonym-swap rewriting without
structural work actually raises detector TPR by 8-15% — a lexical-only pipeline is
not neutral, it is a regression against modern detectors. This module is the
structural layer: it re-introduces sentence-length variance after lexical scrubbing.
```

The 8–15% band maps to the paper's **+8.57% RADAR** and **+15.03% Fast-DetectGPT** ironic increases on naive paraphrase.

### unslop pipeline implication

| Pass | What it fixes | AdvPara signal addressed |
|------|---------------|--------------------------|
| Lexical (`humanize.py`) | Stock vocab, hedging, sycophancy | Partial — GPTZero cones still catch synonym-band rewrites |
| **Structural (`structural.py`)** | Sentence-length σ, bullet soup, flat paragraphs | Burstiness / shape — the axis naive paraphrase ignores |
| Soul (`soul.py`) | Contraction rate, register | Paneru-informed human markers |
| Surprisal (`surprisal.py`) | DivEye variance rhythm | Curvature-adjacent; measure-only today |
| Detector loop (`detector.py`) | Iterative score check | Document-level analog of AdvPara; no token-level search |

**`subtle` intensity is lexical-only** — appropriate for slop removal, **wrong default for anti-detector**. `balanced`/`full` enable structural + soul. That matches the paper: lexical pass alone ≈ simple paraphrase baseline.

---

## GitHub & reproducibility

**Repo:** https://github.com/chengez/Adversarial-Paraphrasing (~46★, Apache-style LICENSE, 0 forks as of Aug 2026)

| Path | Role |
|------|------|
| `utils.py` | Core AdvPara loop (detector-scored token selection) |
| `paraphrase_and_detect.py` | End-to-end paraphrase + score (used by unslop benchmark) |
| `scripts/transfer_test.sbatch` | SLURM/local batch runner; `adversarial=1` toggles guidance |
| `detect_existing_paraphrased_text.py` | Re-score saved outputs against new detectors |
| `quality_judge_utils.py` | GPT-4o quality prompts |
| `kgw_wm/`, `uni_wm/` | Watermarked MAGE subsets (HF format) |
| `zs_detectors/` | Fast-DetectGPT, GLTR implementations |
| `outputs/` | Saved paraphrases + ROC inputs |

**Requirements:** Python ≥3.10, CUDA strongly recommended; SLURM scripts assume cluster. Not pip-installable as a library — research code, not a product SDK.

**unslop benchmark hook:** `benchmarks/adversarial_paraphrasing_comparison/run.py` subprocesses `paraphrase_and_detect.py` from a cloned repo (default `/tmp/chengez-adv`) and compares TMR scores against unslop's `feedback_loop`.

---

## Community reception

| Venue | URL | Signal |
|-------|-----|--------|
| **HuggingFace Papers** | https://huggingface.co/papers/2506.07001 | Paper discovery; linked from r/MachineLearning threads |
| **OpenReview** | https://openreview.net/forum?id=fYjF9KIJd5 | NeurIPS 2025 acceptance record |
| **r/MachineLearning cluster** | https://www.reddit.com/r/MachineLearning/ (threads anchor HF + genaidetect 2025) | AdvPara grouped with DAMAGE + AuthorMist as "serious academic humanization" |
| **TH-Bench / genaidetect workshop** | https://aclanthology.org/2025.genaidetect-1.9/ | Evasion benchmark ecosystem |
| **HN detection discourse** | e.g. https://news.ycombinator.com/item?id=47202864 | Practitioners treat detection as "lost battle"; AdvPara is the formal capstone |

**Recurring community tension:** Pangram/DAMAGE findings that *more fluent* commercial humanizers can be *more* detectable — AdvPara explains part of the mechanism (oversmoothing). Polished synonym swap ≠ human distributional shift.

**Sadasivan connection:** Second author Vinu Sankar Sadasivan links AdvPara to the TV-bound / paraphrase-fragility line (arXiv:2305.18226). AdvPara operationalizes "recursive paraphrase" with detector feedback instead of blind resampling.

---

## Integration plan for unslop

### Current state (already wired)

| Component | Status | AdvPara relationship |
|-----------|--------|---------------------|
| `structural.py` | ✅ Shipped (`--structural`, default on balanced+) | Direct citation; fixes lexical-only regression |
| `detector.py` feedback ladder | ✅ Shipped | Exhaust message recommends cross-model + TempParaphraser/AdvPara pattern |
| `skills/unslop/SKILL.md` anti-detector mode | ✅ Shipped | 6-step structural/burstiness guidance; step 6 = different-model rewrite |
| `.cursor/skills/unslop/prompt-templates.md` Template 4 | ✅ Shipped | Document-level detector-in-loop prompt (not token-level) |
| `benchmarks/adversarial_paraphrasing_comparison/` | ✅ Scaffold | Compare unslop ladder vs external AdvPara repo |

### Phase 1 — Honest defaults (1 week)

1. **Document `subtle` ≠ anti-detector** in SKILL.md help card — cite AdvPara +8–15% ironic TPR on naive paraphrase.
2. **Fix author typos** — replace "Chakraborty et al." with Cheng et al. in `docs/research/01-prompt-engineering-humanization/SYNTHESIS.md` and anywhere else.
3. **Run comparison benchmark** — clone `chengez/Adversarial-Paraphrasing`, execute `benchmarks/adversarial_paraphrasing_comparison/run.py` on fixtures, publish gap in `benchmarks/results/`.

### Phase 2 — Structural deepening (2–3 weeks, deterministic)

AdvPara moves **per-token** detector scores; unslop's deterministic analog is **per-sentence structural edits**:

1. Wire **surprisal variance nudges** into feedback loop when TMR plateaus (DivEye proxy for curvature).
2. Add **TSD second-half volatility** target (arXiv:2601.04833) — AdvPara doesn't address temporal dynamics; unslop can differentiate here.
3. Expand `structural.py` flat-paragraph detection using measured σ from `stylometry.py` (human ~8.2, GPT-4o ~4.1).

### Phase 3 — External AdvPara bridge (optional, opt-in)

Do **not** bundle 8B CUDA inference into the pip wheel. Instead:

1. CLI flag `--adv-paraphrase /path/to/chengez-clone` → subprocess `paraphrase_and_detect.py` after deterministic passes fail target.
2. Gate behind explicit ethics prompt (same as Template 4 — no academic fraud).
3. Pass **already structurally humanized** text as input — paper shows quality holds; unslop front-loads the pass AdvPara assumes.

### Phase 4 — In-process token guidance (long-term, research)

Full AdvPara inside unslop requires:

- Local HF paraphraser + guidance classifier (~8GB+ VRAM)
- Token-level hook in LLM mode (not regex)
- Multi-detector ensemble guidance (StealthRL pattern)

MASH/HIP/StealthRL outperform training-free AdvPara on commercial detectors by 2026 — token-level AdvPara is the **floor**, not the ceiling. unslop's defensible product path: **deterministic structural + optional cross-model LLM**, with AdvPara repo as external reference implementation.

### Anti-patterns (do not ship)

- Lexical-only `--intensity subtle` marketed as detector evasion
- Synonym-swap "humanizer" mode without structural pass
- Watermark-targeted guidance (EU AI Act Art. 50 — already in `detector.py`)
- Claiming unslop replicates 98.96% Fast-DetectGPT drop without running AdvPara benchmark

---

## Comparison to adjacent unslop research memos

| Method | Training | Guidance | Fast-DetectGPT outcome | unslop adoptability |
|--------|----------|----------|------------------------|---------------------|
| **AdvPara** | None | Token-level detector | −98.96% TPR | External subprocess / prompt analog |
| DIPPER | T5-XXL fine-tune | Lexical diversity knobs | Strong vs old detectors | Different-model rewrite recommendation |
| TempParaphraser | None | Multi-sample sentence | −82.5% avg accuracy | Sentence-level candidate pick (partial) |
| StealthRL | GRPO LoRA | Multi-detector reward | 97.6% ASR | Not deterministic |
| unslop deterministic ladder | None | TMR score at document level | ~0.0–0.2 pp on fixtures | Shipped; honest about limits |

---

## Key quotes (verbatim from paper)

> "Compared to simple paraphrasing attack—which, ironically, increases the true positive at 1% false positive (T@1%F) by 8.57% on RADAR and 15.03% on Fast-DetectGPT—adversarial paraphrasing, guided by OpenAI-RoBERTa-Large, reduces T@1%F by 64.49% on RADAR and a striking 98.96% on Fast-DetectGPT."

> "Our approach leverages an off-the-shelf instruction-following LLM to paraphrase AI-generated content under the guidance of an AI text detector, producing adversarial examples that are specifically optimized to bypass detection."

---

## Open questions for unslop bench

1. Does unslop `humanize_structural` alone move Fast-DetectGPT / TMR scores on fixtures, or only AI-ism regex counts?
2. Does **lexical-only subtle → structural** ordering beat **structural-only** on RADAR-proxy detectors?
3. After unslop deterministic passes, does external AdvPara add marginal gain — or did structural pass already capture most distributional shift?
4. Turnitin Feb 2026 anti-humanizer retrain — does AdvPara transfer hold against production black boxes? (Paper evaluates OSS detectors only.)

---

## BibTeX

```bibtex
@misc{cheng2025adversarialparaphrasinguniversalattack,
  title={Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text},
  author={Yize Cheng and Vinu Sankar Sadasivan and Mehrdad Saberi and Shoumik Saha and Soheil Feizi},
  year={2025},
  eprint={2506.07001},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2506.07001},
}
```

---

*Agent #25 complete. Cross-ref: Agent #17 (Sadasivan), Agent #39 (AdvPara GitHub deep-dive), UPDATE-PLAN-2026-08 Part 1 evasion table.*
