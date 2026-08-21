# Agent #06 — Binoculars (Cross-Perplexity Zero-Shot Detection)

**Focus:** Paper, GitHub, mechanism, benchmarks, paraphrase robustness, vs DetectGPT/Fast-DetectGPT/DivEye, community debate, evasion, unslop `detector.py` integration.  
**Date:** 2026-08-19  
**Scope:** Full internet research + read of `unslop/scripts/detector.py`.

---

## 1. Executive summary

**Binoculars** (Hans et al., **ICML 2024** — not ICLR; [arXiv:2401.12070](https://arxiv.org/abs/2401.12070)) is a **zero-shot, training-free** AI-text detector that scores passages via the ratio of **log-perplexity** to **log-cross-perplexity** across a pair of closely related LMs ("observer" and "performer"). Machine text tends to sit at **lower** Binoculars scores than human text; the default global threshold is **0.901** (Falcon-7B pair, accuracy mode) or **0.854** (low-FPR mode).

**Headline claims hold in clean English, same-domain settings:** >90% of ChatGPT samples detected at **0.01% FPR** on Ghostbuster news/creative/essay corpora; beats ChatGPT-tuned Ghostbuster and GPTZero despite zero ChatGPT training data. ESL essays show **99.67%** accuracy on both grammar-corrected and uncorrected versions — a sharp contrast to Liang et al. (2023) commercial-detector bias.

**The 2024–2026 reality is harsher.** Binoculars is the **canonical academic zero-shot baseline** but collapses under the evasion vectors unslop cares about: **humanizer paraphrase** (DAMAGE: **94.15% → 28.23%** TPR@FPR=5%), **synonym swap** (RAID: **−36.1 pp**), **RL paraphrase** (StealthRL: **TPR@1%FPR ≈ 0.002**), and **cross-model rewrite**. Newer signals — **DivEye** surprisal variance (+14.4 pp AUROC on RAID), **AdaDetectGPT** formal FPR bounds — supersede Binoculars on robust benchmarks while sharing the same fundamental vulnerability to structural paraphrase.

**unslop verdict:** Binoculars is the right **academic reference target** for anti-detector mode but the **wrong default backend** for `detector.py`. TMR stays primary; optional `--detector binoculars` for benchmark/ablation only (~14GB RAM for Falcon-7B pair).

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (arXiv HTML v3)** | https://arxiv.org/html/2401.12070v3 | Full mechanism + appendix |
| **Paper (PDF)** | https://arxiv.org/pdf/2401.12070 | |
| **ICML 2024 proceedings** | https://proceedings.mlr.press/v235/hans24a.html | PMLR v235 |
| **OpenReview** | https://openreview.net/forum?id=iARAKITHTH | TL;DR: "training-free and accurate" |
| **Official GitHub** | https://github.com/ahans30/Binoculars | ~406 stars, BSD-3-Clause, Aug 2026 |
| **HF Gradio demo** | https://huggingface.co/spaces/tomg-group-umd/Binoculars | Two threshold modes shipped |
| **Parent lineage: DetectGPT** | https://arxiv.org/abs/2301.11305 | Mitchell et al., ICML 2023 |
| **Parent lineage: Fast-DetectGPT** | https://arxiv.org/abs/2310.05130 | Bao et al., ICLR 2024 |
| **Successor peer: DivEye** | https://arxiv.org/abs/2509.18880 | TMLR 2026; beats Binoculars on RAID |
| **Successor peer: AdaDetectGPT** | https://arxiv.org/abs/2510.01268 | NeurIPS 2025; bundles Binoculars in zoo |
| **RAID benchmark** | https://raid-bench.xyz/ | Leaderboard includes Binoculars |
| **DAMAGE humanizer audit** | https://arxiv.org/abs/2501.03437 | COLING 2025 GenAIDetect workshop |
| **NAACL 2025 practical eval** | https://aclanthology.org/2025.findings-naacl.271/ | TPR@FPR study across 7 detectors |
| **NAACL SRW paraphrase resilience** | https://doi.org/10.18653/v1/2025.naacl-srw.46 | Binoculars F1 −19.6 pp under GPTinf |
| **StealthRL evasion** | https://arxiv.org/abs/2602.08934 | Held-out Binoculars transfer |
| **unslop detector module** | `unslop/scripts/detector.py` | TMR + Desklib only today |
| **unslop anti-detector skill** | `skills/unslop/SKILL.md` | Names Binoculars as target |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | ICML 2024 (41st International Conference on Machine Learning) |
| **Authors** | Abhimanyu Hans, Avi Schwarzschild, Valeriia Cherepanova, Hamid Kazemi, Aniruddha Saha, Micah Goldblum, Jonas Geiping, Tom Goldstein |
| **Affiliation** | University of Maryland (Tom Goldstein group) |
| **License** | BSD-3-Clause (code); arXiv CC BY 4.0 |
| **Compute** | Falcon-7B + Falcon-7B-Instruct at bfloat16; ~27 GB RAM unquantized, ~11 GB 4-bit |

---

## 3. Mechanism — how Binoculars works

### 3.1 Core intuition

Raw **perplexity** fails when prompts induce high-perplexity completions regardless of author — the paper's **"capybara problem"** (GPT-4 writing about an astrophysicist capybara scores PPL 2.20, above human/machine means; DetectGPT misclassifies as human). Binoculars normalizes observed perplexity against **cross-perplexity**: how surprising the performer's next-token predictions are to the observer on the **same token sequence**.

Human writers diverge from \(\mathcal{M}_1\) more than \(\mathcal{M}_2\) diverges from \(\mathcal{M}_1\), when both LMs are similar to each other but both differ from humans.

### 3.2 Score definition

For text string \(s\), observer \(\mathcal{M}_1\), performer \(\mathcal{M}_2\):

\[
B_{\mathcal{M}_1,\mathcal{M}_2}(s) = \frac{\log \mathrm{PPL}_{\mathcal{M}_1}(s)}{\log \mathrm{xPPL}_{\mathcal{M}_1,\mathcal{M}_2}(s)}
\]

- **Numerator:** standard causal LM perplexity under \(\mathcal{M}_1\) (teacher-forced on observed tokens).
- **Denominator (cross-perplexity):** average per-token cross-entropy between \(\mathcal{M}_1\)'s distribution and \(\mathcal{M}_2\)'s argmax/next-token predictions on the same prefix.

**Classification rule (official implementation):** score **< threshold → AI-generated**; score **≥ threshold → human**. Default thresholds (Falcon-7B pair, bfloat16):
- **Accuracy mode:** 0.9015310749276843 (F1-optimized on validation mix)
- **Low-FPR mode:** 0.8536432310785527 (targets <0.01% FPR on validation)

### 3.3 Default model pairing

Paper body and GitHub default:

| Role | Model | Used for |
|------|-------|----------|
| Observer (PPL numerator) | `tiiuae/falcon-7b-instruct` | Perplexity of observed text |
| Performer | `tiiuae/falcon-7b-instruct` | Next-token predictions |
| Cross-PPL denominator | `tiiuae/falcon-7b` + instruct pair | Cross-perplexity term |

Appendix Table 3 sweeps other pairings (Mistral-7B, LLaMA-2-7B, etc.); **two models must be close in capability** — contrastive decoding uses weak+strong pairs; Binoculars needs **similar** pairs.

### 3.4 Relation to DetectGPT family

| Method | Signal | Passes needed | Key weakness |
|--------|--------|---------------|--------------|
| **DetectGPT** (ICML 2023) | Negative log-prob curvature under mask-fill perturbations | Many (perturbation sampling) | Slow; paraphrase-sensitive; capybara-class failures |
| **Fast-DetectGPT** (ICLR 2024) | Conditional probability curvature, closed-form | 1–2 | Same logits family; TempParaphraser collapse (Agent #24) |
| **Binoculars** (ICML 2024) | PPL / cross-PPL ratio | 2 forward passes | Paraphrase/humanizer collapse; GPT-4 FNR 58% |
| **DivEye** (TMLR 2026) | Surprisal variance + XGBoost | 1 + classifier | Needs labeled training; stronger on RAID |
| **AdaDetectGPT** (NeurIPS 2025) | Learned witness on log-probs + MCLT threshold | 1 + witness fit | Same paraphrase fragility; formal FPR bounds |

Binoculars occupies the **paired-LM zero-shot** niche — no training data from target generator, no perturbation loop. It is the **strongest pure ratio method** in 2024 papers but shares the **logits/perplexity surface** that paraphrase attacks flatten.

### 3.5 Code architecture (`ahans30/Binoculars`)

```python
from binoculars import Binoculars
bino = Binoculars()  # Falcon-7B defaults
score = bino.compute_score(text)   # float; lower = more AI-like
label = bino.predict(text)         # "Most likely AI-Generated" if score < threshold
```

- **406 GitHub stars**, 62 forks, 4 open issues (Aug 2026)
- Batch scoring supported (`list[str]` input)
- `mode="low-fpr"` vs `mode="accuracy"` switchable at runtime
- Custom observer/performer paths accepted; **threshold is fixed for Falcon pair** — retune if models change
- README warns: English-biased; academic use only; never deploy without human oversight
- Optional local Gradio demo via repo scripts

**Reproduction status:** Widely forked; integrated into MAGE, RAID, AdaDetectGPT, StealthRL, DAMAGE, and DivEye comparison tables. Independent replication confirms threshold and score direction. Quantization (~4-bit) costs ~2% F1 per NAACL SRW replication — marginal vs 2× carbon footprint.

---

## 4. Benchmark results (verified numbers)

### 4.1 Paper-native evaluations (Hans et al., ICML 2024)

| Setting | Metric | Result | Notes |
|---------|--------|--------|-------|
| ChatGPT on Ghostbuster datasets (news, creative, essay) | TPR @ 0.01% FPR | **>90%** | Zero-shot; beats ChatGPT-tuned Ghostbuster + GPTZero |
| News documents, 512 tokens | TPR @ 0.01% FPR | **~95%** | OpenReview abstract figure |
| LLaMA-2-13B generations | TPR @ low FPR | **Highest among baselines** | Ghostbuster fails on non-ChatGPT LLMs |
| GPT-3 (Open Orca) | Accuracy (machine-only set) | **92%** | Global OOD threshold |
| GPT-4 (Open Orca, n=129) | Accuracy | **41.86%** | **58.13% false negative rate** |
| Gemini-1.0-pro (Open Orca) | Accuracy | **96.89%** | 3.10% FNR |
| ESL essays (EssayForum) | Accuracy | **99.67%** both corrected & uncorrected | vs Liang commercial bias |
| M4 multilingual (ChatGPT) | Precision/recall | Strong vs RoBERTa/GLTR/Stylistic | Low recall on Urdu/Bulgarian/Arabic |
| Stylistic prompts (pirate voice, etc.) | FNR delta | **≤1 pp** | Robust to prompt style |
| Capybara GPT-4 example | Binoculars score | **0.73** (< 0.901 ✓) | DetectGPT wrong; GPTZero 49.7% |

**Paper's preferred metric:** TPR @ low FPR (0.01%), **not AUROC alone** — authors argue AUC misleads when FPR < 1% (Table 4 in appendix).

### 4.2 RAID (Dugan et al., ACL 2024)

Aggregated detection accuracy across 11 detectors, 8 domains, 12 models, 11 attack types:

| Attack / setting | Binoculars accuracy | Δ from baseline |
|------------------|---------------------|-----------------|
| **None (baseline)** | **79.6%** | — |
| Paraphrase (T5-11B) | 80.3% | +0.7 |
| **Synonym swap** | **43.5%** | **−36.1** |
| Homoglyph / whitespace / etc. | 37.7–78.0% | varies |

DivEye paper RAID AUROC row: Binoculars **0.844** vs leader e5-small-lora **0.986** (−14.4 pp); TPR@FPR=5% **79.0%** vs DivEye **93.63%**.

RAID Finding 6: metric-based detectors including Binoculars **degrade up to 36.1%** on synonym swap; adversarially trained RADAR more robust.

### 4.3 DAMAGE humanizer audit (Masrour et al., COLING 2025)

Academic text, TPR @ FPR=5%:

| Detector | Raw AI | After 19-tool humanization |
|----------|--------|---------------------------|
| GPTZero | 99.73% | 60.04% |
| **Binoculars** | **94.15% ± 0.88%** | **28.23% ± 1.62%** |
| RADAR | 3.33% | 5.05% |
| DAMAGE (proposed) | 100% | 98.26% |

RAID attack subsets (DAMAGE Table 4):

| Attack | Binoculars TPR |
|--------|----------------|
| Paraphrase | 80.3% |
| Synonym | 43.5% |

Educational text domain (DAMAGE appendix): Binoculars **94.40% → 29.73%** after humanization.

### 4.4 NAACL 2025 — Practical Examination (Dugan et al., Findings)

Seven detectors, seven tasks, four languages; emphasizes **TPR@FPR**:

| Detector | TPR@0.01 | TPR@0.05 | TPR@0.10 | AUROC |
|----------|----------|----------|----------|-------|
| **Binoculars** | **0.58** | **0.67** | **0.72** | **0.8485** |
| Fast-DetectGPT | 0.49 | 0.61 | 0.68 | 0.8405 |
| LogRank | 0.09 | 0.40 | 0.50 | 0.7763 |
| RADAR | 0.05 | 0.15 | 0.27 | 0.6009 |

Binoculars **wins the zero-shot panel** on TPR@0.01 but **rewrite prompting** drops average TPR sharply. GPT-4o generations: Binoculars TPR@0.01 as low as **0.02–0.05** on some tasks (Table 5).

### 4.5 NAACL SRW 2025 — Paraphrase resilience (Perkins et al.)

GPTinf paraphrase on 201 AI + 201 human samples (COLING GenAIDetect devtest):

| Method | Pre-attack F1 | Post-attack F1 | Degradation |
|--------|---------------|----------------|-------------|
| **Binoculars alone** | 0.7497 | 0.5533 | **−0.1964** |
| RoBERTa alone | 0.7586 | 0.6594 | −0.0992 |
| Text Features alone | 0.7207 | 0.6682 | −0.0526 |
| TF + RoBERTa + Binoculars ensemble | 0.8061 | 0.6716 | −0.1345 |

**Dichotomy:** highest standalone accuracy, **worst paraphrase fragility** among tested modules.

### 4.6 StealthRL (Feb 2026) — held-out transfer

GRPO-trained Qwen3-4B paraphrase policy; Binoculars **held out of training** (uses gpt2-medium + gpt2-large in their config):

| Method | Binoculars TPR@1%FPR | Binoculars AUROC |
|--------|---------------------|------------------|
| M0 (no attack) | 0.367 | 0.705 |
| **M2 StealthRL** | **0.002** | **0.055** |

Mean panel AUROC: 0.789 → 0.432 under attack.

### 4.7 vs Fast-DetectGPT / DetectGPT / DivEye

On **authors' own corpora** (white-box, 5-model generations):

| Method | 5-model AUROC | ChatGPT/GPT-4 AUROC | Speed |
|--------|---------------|---------------------|-------|
| DetectGPT | 0.9554 | 0.7225 | 1× |
| Fast-DetectGPT | **0.9887** | **0.9338** | **340×** |
| Binoculars | competitive on TPR@0.01% | **GPT-4 weak (58% FNR)** | ~2× Falcon forwards |

DivEye (TMLR 2026) beats Binoculars by **14.4 pp AUROC on RAID** (0.844 → 0.984) and on most MAGE testbeds. **Trade-off:** Fast-DetectGPT wins average AUROC on source-model text; Binoculars wins **low-FPR precision** on ChatGPT in Ghostbuster setting and handles capybara-class prompts better than DetectGPT. None survive 2025–2026 humanizer/RL paraphrase.

---

## 5. Community & academic debate

### 5.1 Supporters / positive signals

| Source | Position | Evidence |
|--------|----------|----------|
| **ICML 2024 acceptance** | Peer-reviewed SOTA zero-shot | PMLR proceedings, OpenReview |
| **Paper authors** | Capybara fix + ESL fairness | 99.67% ESL; Table 1 worked example |
| **RAID authors** | Strong clean-domain baseline | 79.6% pre-attack; best metric-method on some slices |
| **NAACL 2025 Practical Exam** | Best TPR@0.01 among 7 detectors tested | 0.58 vs Fast-DetectGPT 0.49 |
| **DAMAGE paper** | "Even more effective recent approach" for raw AI | Before humanization only |
| **AdaDetectGPT repo** | Bundled baseline in unified detector zoo | Still compared in NeurIPS 2025 |
| **unslop docs** | Named anti-detector target | `RESEARCH_AND_TECH.md`, Cat 05 synthesis |

Authors explicitly engage impossibility literature (Sadasivan, Varshney, Helm) but argue **current** LLMs remain detectable — constructive evidence, not proof of durable detection.

### 5.2 Critics / limitations

| Source | Concern | Binoculars impact |
|--------|---------|-------------------|
| **DAMAGE (2025)** | Humanizers break perplexity methods | **−66 pp** TPR on humanized text |
| **RAID Finding 6** | Synonym swap | **−36.1 pp** |
| **StealthRL (2026)** | RL paraphrase transfer | **TPR ≈ 0** at 1% FPR |
| **Perkins NAACL SRW** | GPTinf paraphrase | **−19.6 pp** F1 |
| **Paper Appendix A.10** | GPT-4 API text | **58% missed** at global threshold |
| **Paper §5 multilingual** | Low-resource languages | High precision, **low recall** |
| **NAACL Practical Exam** | Rewrite prompting | TPR collapses toward 0 on some tasks |
| **DivEye (2026)** | Surprisal variance strictly better | −14.4 pp AUROC on RAID |
| **Nicks et al. (ICLR 2024)** | Cited in `detector.py` | "Advise against continued reliance on LLM-generated text detectors" |
| **Pangram / practitioner blogs** | Perplexity ≠ production detector | Binoculars is smarter perplexity, same attack surface |

**Overhyped vs genuinely novel:**

- **Novel:** Cross-perplexity ratio; zero-shot cross-model transfer; ESL fairness vs commercial tools.
- **Overhyped:** 0.01% FPR headline does not survive humanizers; GPT-4 58% FNR (March 2024).

### 5.3 Social footprint

No major HN threads (Aug 2026). Heavy academic citation chain (RAID, MAGE, DAMAGE, AdaDetectGPT, StealthRL, DivEye). GitHub: 406 stars, 4 open issues.

---

## 6. Humanization angle — evading Binoculars-class detectors

Binoculars detects text that **looks like it was sampled from an LM similar to Falcon-7B**. Evasion = push cross-perplexity ratio toward the human band (scores ≥ 0.901).

### 6.1 What works (research-backed)

| Lever | Mechanism | Evidence |
|-------|-----------|----------|
| **Cross-model paraphrase** | Different model family rewrites token-surprise fingerprint | unslop SKILL.md; TempParaphraser 82.5% avg detector reduction (Agent #24) |
| **Structural paraphrase** | Changes sentence boundaries, not just synonyms | RAID: synonym swap kills Binoculars; paraphrase alone less effective |
| **Humanizer tools** | Multi-pass rewrite targeting detector scores | DAMAGE: 94% → 28% |
| **RL-optimized paraphrase** | StealthRL reward includes detector evasion | TPR@1%FPR → 0.002 |
| **Burstiness / variance injection** | Flat LM surprisal → human-like dispersion | DivEye motivation; unslop `structural.py` + sentence-length σ |
| **Grammar correction paradox** | Binoculars **insensitive** to ESL correction | Don't rely on "errors" for evasion — unlike GPTZero bias |

### 6.2 What unslop deterministic passes likely do

| Pass | Binoculars effect | Confidence |
|------|-------------------|------------|
| Stock vocab / hedging removal | Minimal — not perplexity-targeted | High |
| Em-dash / tricolon cleanup | Low | Medium |
| `structural.py` (sentence variance) | **Moderate positive** — increases local unpredictability | Medium |
| `soul.py` (contractions) | Tokenization shift; small PPL surface change | Low |
| `--surprisal-variance` telemetry | Measures related signal; **not optimized** in loop | High |

**Not measured yet:** no published Binoculars scores on unslop output. Highest-value experiment: run `benchmarks/detector_bench.py` with optional Binoculars backend on before/after corpus.

### 6.3 What not to do

- **Synonym-only paraphrase** — RAID shows Binoculars survives T5 paraphrase (+0.7 pp) but **dies on synonym swap**; QuillBot-class tools may hit the wrong attack axis.
- **Uniform smoothing** — lowers variance; keeps text in LM manifold.
- **Assume threshold 0.901 is universal** — model pair, quantization, and language all require recalibration.

---

## 7. unslop integration plan

Current `detector.py` state (read Aug 2026):

| Component | Today | Notes |
|-----------|-------|-------|
| Backends | `tmr`, `desklib` only | Supervised RoBERTa-style classifiers |
| Default | TMR (`Oxidane/tmr-ai-text-detector`) | 99.28% RAID AUROC claimed |
| Feedback loop | Escalates humanize ladder until TMR p_ai ≤ target | Recommends cross-model paraphrase on exhaustion |
| Binoculars | **Not integrated** | Named in module docstring via Nicks et al.; anti-detector skill only |

### 7.1 Why TMR stays default

1. **Size:** ~500MB vs ~14GB+ for Falcon-7B pair.
2. **Speed:** Single 125M forward pass vs dual 7B forwards.
3. **Robustness:** Supervised RAID training includes attack exposure; Binoculars raw score collapses under humanizers.
4. **Design fit:** `detector.py` lazy-import + offline HF cache pattern maps cleanly to classifiers, not dual-LM inference.
5. **Paraphrase guidance already correct:** `feedback_loop()` exhaustion message points to cross-model paraphrase — the lever that actually moves Binoculars scores.

### 7.2 Recommended additions

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P1** | Add `DetectorName = "binoculars"` optional backend behind `--detector binoculars` | Academic benchmark parity; anti-detector users want explicit score |
| **P1** | Map Binoculars score → `[0,1]` AI probability via calibrated sigmoid on `(threshold - score)` | Keeps `feedback_loop` interface stable; document non-linear mapping |
| **P2** | Extend `fetch_detectors.py` to prefetch Falcon-7B + instruct | Match TMR bootstrap pattern |
| **P2** | `benchmarks/detector_bench.py` row for Binoculars vs TMR vs Desklib | Close "no multi-detector eval harness" gap (Cat 16) |
| **P3** | Anti-detector dual threshold (TMR + Binoculars) | Disagreement ⇒ needs structural paraphrase |
| **P3** | Document Falcon/GPT-4 staleness | 2023 scoring models under-detect 2025+ generators |

Optional backend: wrap `binoculars.Binoculars(mode="low-fpr")`, map `(threshold - score) / threshold` into `[0,1]` for `feedback_loop` compatibility, chunk at 512 tokens. **Do not** add to default `DEFAULT_LADDER` — too slow and paraphrase-fragile for CI.

---

## 8. Open questions

1. **Does unslop structural+soul pass move Binoculars scores?** Needs local bench.
2. **Threshold mode:** low-FPR (0.854) vs accuracy (0.901) for anti-detector targets?
3. **GPT-4.1 / Claude 4 FNR:** Paper's 58% GPT-4 FNR (March 2024) — unreplicated on 2026 APIs.
4. **Ensemble disagreement:** TMR human + Binoculars AI — humanized text or ESL false positive?
5. **Legal/ethical:** Same as `detector.py` Nicks et al. warning — signal, not gate.

---

*Agent #06 complete. Cross-refs: Agent #01 (DivEye), Agent #04 (AdaDetectGPT), Agent #05 (Fast-DetectGPT), Agent #12 (DAMAGE), Agent #17 (Sadasivan), Agent #24 (TempParaphraser), Agent #26 (StealthRL), Agent #35 (cross-model paraphrase).*
