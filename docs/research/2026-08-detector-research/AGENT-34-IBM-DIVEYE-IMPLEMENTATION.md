# Agent #34 — IBM DivEye Implementation Deep Research

**Focus:** Practical deployment, reproduction, community feedback, code quality — not theory.  
**Date:** 2026-08-19  
**Scope:** `IBM/diveye`, HF Space, PAN 2025 notebook, `unslop/scripts/surprisal.py` alignment audit.

---

## Executive summary

IBM's public DivEye stack is **minimal and research-grade**, not production-ready. The GitHub repo ships ~130 lines of feature math plus an XGBoost training loop; no sample data, no pinned deps file, no tests, no pretrained classifier weights. The **real deployable artifact** is the Hugging Face Space (`pinyuchen/Diveye_AI_text_detector`), which bundles a 307 KB `model.json` XGBoost head over DivEye + BiScope + zlib compression features, running Falcon-7B + Gemma-2B on ZeroGPU.

**Reproduction of feature vectors is straightforward** once `torch` + `transformers` are installed. unslop's `surprisal.py` **numerically matches IBM `diveye_utils.py` bit-for-bit** on GPT-2 (max relative error < 3×10⁻⁶ across 9 fixture texts; see `benchmarks/results/diveye_comparison.json`). Default scorer mismatch remains: unslop defaults to `distilgpt2`, paper/PAN notebook use `gpt2`, HF demo uses `tiiuae/falcon-7b`.

**Paper vs code vs demo diverge** on feature dimensionality (paper Eq. 6 = 9 features; code = 10; HF Space = 11 + 72 BiScope features), on second-order derivative source (paper defines Δ² on surprisal; code computes Δ² on log-likelihood — equivalent up to sign for variance/entropy/autocorr), and on PAN 2025 claims ("outperforms all baselines" vs TF-IDF SVM AUROC 0.996 vs their 0.997).

---

## Primary URLs

| Resource | URL |
|----------|-----|
| Official GitHub repo | https://github.com/IBM/diveye |
| TMLR paper (arXiv) | https://arxiv.org/abs/2509.18880 |
| TMLR HTML v3 | https://arxiv.org/html/2509.18880v3 |
| ICML DIG-BUG OpenReview | https://openreview.net/forum?id=QuDDXJ47nq |
| HF Space (live demo) | https://huggingface.co/spaces/pinyuchen/Diveye_AI_text_detector |
| HF Space `app.py` | https://huggingface.co/spaces/pinyuchen/Diveye_AI_text_detector/blob/main/app.py |
| Demo website (static, not real inference) | https://diveye.vercel.app/ |
| PAN 2025 notebook (CEUR) | https://ceur-ws.org/Vol-4038/paper_282.pdf |
| PAN 2025 notebook (Webis mirror) | https://downloads.webis.de/pan/publications/papers/basani_2025.pdf |
| IBM Research publication page | https://research.ibm.com/publications/diveye-at-pan-2025-diversity-boosts-ai-generated-text-detection |
| PAN 2025 task overview | https://pan.webis.de/clef25/pan25-web/generated-content-analysis.html |
| PAN 2025 data/code repo | https://github.com/pan-webis-de/pan25-generative-ai-authorship-verification |
| unslop comparison benchmark | `benchmarks/diveye_comparison/run.py` |
| unslop surprisal module | `unslop/scripts/surprisal.py` |

---

## 1. Repository anatomy (`IBM/diveye`)

**Created:** 2025-05-30. **Stars:** ~17 (Aug 2026). **License:** CC BY-NC-SA 4.0 (non-commercial). **Files:** 4 source files only — `diveye.py`, `diveye_utils.py`, `README.md`, `LICENSE`. No `requirements.txt`, no sample CSVs, no tests, no CI beyond an IBM Mend bot PR.

### 1.1 Installation (README)

```bash
conda create -n diveye python=3.11
conda activate diveye
pip install transformers scikit-learn tqdm numpy pandas xgboost scipy
```

**Gap:** `torch` is not listed explicitly but required at runtime. No version pins. No GPU guidance (CPU works for GPT-2 feature extraction; training loop is CPU-viable).

### 1.2 Execution model

```bash
python3 diveye.py --model=gpt2 \
  --train_dataset=train.csv --test_dataset=test.csv
```

CSV schema: columns `text`, `label` (binary). The script:
1. Loads HF causal LM + tokenizer
2. Loops every row, calls `DivEyeUtils.diveye_compute(text)` → 10-float vector
3. Trains XGBoost (`max_depth=12`, `n_estimators=200`, etc.)
4. Evaluates on test split, writes `train.json` / `test.json` logs

**You must bring your own labeled CSVs.** MAGE/RAID/HC3/PAN splits are not bundled. Reproducing paper AUROC numbers from the repo alone is impossible without external dataset acquisition.

---

## 2. Code quality audit

### 2.1 `diveye_utils.py` — feature core (43 lines)

**Strengths:**
- Clear separation of log-likelihood extraction and surprisal stats
- Uses standard teacher-forcing shift: `logits[:, :-1]` vs `tokens[:, 1:]`
- Truncation at 1024 tokens (matches HF Space)
- 10-feature vector matches HF Space DivEye block (minus compression ratio)

**Defects:**

| Severity | Issue | Detail |
|----------|-------|--------|
| **Critical** | Infinite recursion on short text | `if len(surprisals) < 10`: `return self.diveye_compute(text)` — no base case, stack overflow |
| Medium | Double forward pass | `_surprisal()` calls `_log_likelihoods()`; `diveye_compute()` calls both again |
| Medium | Redundant `labels=tokens` in forward | Loss computed but discarded; manual gather used anyway |
| Low | No device-agnostic CPU fallback | `.to(self.model.device)` assumes model has device set |
| Low | NaN autocorr unguarded | `np.corrcoef` on constant sequences → NaN (HF Space handles with conditional) |

### 2.2 `diveye.py` — training wrapper (128 lines)

**Defects:**

| Severity | Issue | Detail |
|----------|-------|--------|
| **Critical** | `self.model` shadowing | Line 63: `self.model = xgb.XGBClassifier(...)` overwrites the HF LM loaded in `__init__`. `evaluate()` still calls `self.utils.diveye_compute()` which uses the LM inside `DivEyeUtils`, so evaluation works, but any code expecting `self.model` to remain the LM breaks. Naming collision, maintenance trap. |
| Medium | No train/test guard | `evaluate()` checks `if self.model == None` but after train it's an XGBoost object, never None |
| Medium | No model serialization | Trained XGBoost not saved to disk by default |
| Low | `--logging` typed as `bool` | argparse bool parsing is broken in Python (`type=bool` + `"False"` → True) |

### 2.3 What's missing for production

- Pretrained classifier weights (only on HF Space, not GitHub)
- Batch inference API / REST endpoint
- Error handling for OOM on large LMs
- Unit tests
- Docker / reproducible environment lockfile
- Interpretability hooks advertised in paper (token-level heatmaps) — **not in GitHub repo**

---

## 3. Hugging Face Space deployment

**Space:** https://huggingface.co/spaces/pinyuchen/Diveye_AI_text_detector  
**Runtime:** ZeroGPU (`@spaces.GPU`), Gradio 5.35.0  
**Models at load:** `tiiuae/falcon-7b` (DivEye features) + `google/gemma-1.1-2b-it` (BiScope features)  
**Classifier:** `model.json` (307 KB XGBoost) bundled in Space repo  
**Min input:** 15 words (hardcoded)

### 3.1 Feature pipeline (Space vs GitHub)

The Space **inlines** all logic in `app.py` (~370 lines) rather than importing `diveye_utils.py`. Feature vector:

```
[mean_s, std_s, var_s, skew_s, kurt_s,           # 5 distributional (paper has 4)
 mean_diff, std_diff,                              # 2 first-order (paper uses Δμ, Δσ²)
 var_2nd, entropy_2nd, autocorr_2nd,              # 3 second-order
 comp_ratio]                                       # +1 zlib compression ratio (NOT in paper/repo)
+ biscope_features (72 floats)                     # BiScope percentile losses
= 83 total features → XGBoost → P(AI)
```

**Deployment requirements:**
- CUDA mandatory (`loaded = False` if no CUDA — Space shows error)
- `HF_TOKEN` env var for gated models (Falcon, Gemma)
- ~16+ GB VRAM for dual-model load (falcon-7b on cuda:0, gemma on cuda:1)
- `requirements.txt`: unpinned `torch`, `transformers`, `xgboost`, etc.

### 3.2 Community fix history (16 merged PRs, Jul 2025)

All authored by first author `FloofCat` (Advik Basani). No external contributors. Fix themes:

| PR # | Title | Implied bug class |
|------|-------|-------------------|
| 6, 9 | pickling error | XGBoost / Gradio serialization on ZeroGPU |
| 8 | fix bugs, cuda | GPU device mapping |
| 7 | fix concurrency | Race on global model globals |
| 14–16 | fix bugs x3/x4, themes, xgb | Runtime stability, CUDA-XGBoost conflicts |
| 15 | fix, xgb | "potential cuda-xgb conflicts" |
| 3–5 | dependencies | Missing packages on Space builder |

**Takeaway:** The Space was **迭代-debugged in public** over ~10 days (Jul 5–14, 2025). No issue tracker on GitHub; HF Discussions served as de facto bug tracker. No user-reported reproduction threads found outside these author PRs.

### 3.3 Static demo site

https://diveye.vercel.app/ — explicitly labeled **"for representational purposes only"**. Hardcoded confidence (95.7%). Directs users to HF Space for real testing. Not a deployment path.

---

## 4. PAN 2025 notebook analysis

**Paper:** "DivEye at PAN 2025: Diversity Boosts AI-Generated Text Detection"  
**PDF:** https://ceur-ws.org/Vol-4038/paper_282.pdf  
**Authors:** Basani (BITS Goa), Chen (IBM Research)

### 4.1 Task context

PAN@CLEF 2025 Generative AI Authorship Verification (Voight-Kampff subtask 1): binary classification, human vs machine text, with style-mimic and obfuscation surprises in test set. Builder-breaker setup with ELOQUENT lab generating evasion methods.

### 4.2 Implementation details (notebook)

- **Scorer LM:** GPT-2 (default); also submitted Falcon-7B variant
- **Meta-classifier:** XGBoost on DivEye features alone, or concatenated with BiScope scores
- **Training data:** PAN organizer splits only (no MAGE/RAID in submission)
- **Evaluation:** TIRA platform — AUROC, c@1, F0.5, F1, Brier

### 4.3 Reported results (Table 1, validation split)

| Method | AUROC | c@1 | F1 |
|--------|-------|-----|-----|
| **DivEye [GPT-2] + BiScope** (tart-league) | **0.997** | 0.978 | 0.983 |
| DivEye [Falcon-7B] + BiScope | 0.997 | 0.912 | 0.897 |
| DivEye [GPT-2] standalone (weary-jersey) | 0.961 | 0.905 | 0.926 |
| **baseline-tf-idf (Linear SVM)** | **0.996** | **0.984** | **0.980** |
| baseline-binoculars-llama-3.1 | 0.918 | 0.843 | 0.873 |
| baseline-ppmd | 0.786 | 0.757 | 0.812 |

### 4.4 Claim vs number disagreements

1. **"Outperforms all given baselines"** (Conclusion, p. 272): Misleading on AUROC — TF-IDF SVM hits 0.996 vs 0.997 for DivEye+BiScope (0.1 point). TF-IDF **wins** c@1 (0.984 vs 0.978) and is competitive on F1. Only fair reading: **DivEye+BiScope ensemble edges TF-IDF on AUROC/F0.5; standalone DivEye (0.961) is well below TF-IDF.**

2. **Paper Eq. 6 = 9 features; code = 10; Space = 11+72:** Notebook references "original paper [40]" for MAGE experiments but PAN submission uses the **10-feature code vector**, not the 9-feature equation. Distribution block in Eq. 6 is `{μ, σ², γ₁, γ₂}` (4); code adds σ alongside σ² and uses std (not variance) for first-order block.

3. **"~0.01 seconds per input"** (§4.2 efficiency claim): Applies to GPT-2 statistical features only. HF Space with Falcon-7B + Gemma-2B is orders of magnitude slower; ZeroGPU queue latency dominates.

4. **MAGE/RAID numbers cited but not in notebook:** Footnote 1 states MAGE models "were not submitted for PAN 2025; results reported solely to empirically validate." PAN notebook is not a full reproduction of TMLR paper benchmarks.

5. **No public reproduction attempts found:** Web/GitHub search turned up zero independent "I reproduced DivEye" posts, issues, or forks with fixes. Community signal = HF Space author self-PRs only.

---

## 5. Reproduction runbook

### 5.1 Feature extraction only (matches paper signal)

```bash
git clone https://github.com/IBM/diveye.git
pip install torch transformers scipy numpy
python3 -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
from diveye_utils import DivEyeUtils
lm = AutoModelForCausalLM.from_pretrained('gpt2')
tok = AutoTokenizer.from_pretrained('gpt2')
print(DivEyeUtils(lm, tok).diveye_compute('Your text here, at least fifteen words or so.'))
"
```

**Known failure modes:**
- Text < 10 tokens → infinite recursion (GitHub utils) or zeros (HF Space, but still computes)
- Missing `torch` → ImportError (README omits it)
- First HF download requires network; ~500 MB for GPT-2

### 5.2 Full detector (GitHub path)

1. Obtain labeled CSVs (PAN: https://github.com/pan-webis-de/pan25-generative-ai-authorship-verification)
2. Run `diveye.py` with `--model gpt2`
3. Inspect `test.json` for per-sample features + labels
4. **You still won't match PAN numbers** without BiScope features, compression ratio, and their exact XGBoost hyperparams + validation split

### 5.3 Full detector (HF Space path)

Use the hosted Space or clone Space repo + provision CUDA + HF_TOKEN + download Falcon-7B and Gemma-2B. Closest to PAN `tart-league` submission.

### 5.4 unslop one-shot reading

```bash
pip install torch transformers  # optional deps
echo "Your prose here..." | python3 -m unslop.scripts.cli --stdin --surprisal-variance
# or with paper scorer:
echo "..." | python3 -m unslop.scripts.cli --stdin --surprisal-variance --surprisal-model gpt2
```

Compare against IBM:
```bash
python3 benchmarks/diveye_comparison/run.py --ibm-repo /path/to/IBM/diveye --model gpt2
```

---

## 6. `surprisal.py` alignment audit

### 6.1 Verdict

**Feature vector: ALIGNED with IBM reference code** (not necessarily with paper Eq. 6).

Empirical check (2026-08-19, GPT-2, local run):
- 9 unslop fixture texts: max relative error **< 3×10⁻⁶** per feature
- Hand-checked varied vs flat prose: **0.0000** relative error all 10 dimensions
- Benchmark artifacts: `benchmarks/results/diveye_comparison.json`

### 6.2 Feature mapping

| Index | IBM `diveye_utils` | unslop `to_diveye_vector()` | Match |
|-------|-------------------|----------------------------|-------|
| 0 | `mean(surprisal)` | `-mean_log_prob` | ✅ |
| 1 | `std(surprisal)` | `surprisal_stdev` | ✅ |
| 2 | `var(surprisal)` | `surprisal_variance` | ✅ |
| 3 | `skew(surprisal)` | `surprisal_skewness` | ✅ |
| 4 | `kurtosis(surprisal)` (Fisher/excess) | `surprisal_kurtosis` (excess) | ✅ |
| 5 | `mean(diff(surprisal))` | `delta_surprisal_mean` | ✅ |
| 6 | `std(diff(surprisal))` | `delta_surprisal_stdev` | ✅ |
| 7 | `var(diff(diff(log_likelihood)))` | `delta2_surprisal_variance` | ✅ (equiv) |
| 8 | `entropy(hist(diff²(log_l), 20))` | `delta2_surprisal_entropy` | ✅ |
| 9 | `autocorr(diff²(log_l))` | `delta2_surprisal_autocorr` | ✅ |

### 6.3 Intentional unslop divergences (by design)

| Aspect | IBM / paper | unslop | Risk |
|--------|-------------|--------|------|
| Default LM | GPT-2 (paper/PAN) | `distilgpt2` | Different absolute stdev bands; rank order usually preserved |
| Classifier head | XGBoost required for detection | None — measurement only | unslop reads stdev/CV, doesn't classify AI/human |
| Extra outputs | 10-vector only | `surprisal_cv`, `mean_log_prob`, `to_dict()` | Harmless superset |
| Max tokens | 1024 (truncation in tokenizer) | 1024 (post-encode slice) | ✅ aligned |
| Second-order source | Δ² on log-likelihood | Δ² on surprisal sequence | Numerically identical for var/entropy/autocorr |
| HF Space extras | +compression +BiScope | Not implemented | Can't reproduce Space classifier from unslop alone |

### 6.4 Paper Eq. 6 vs unslop (theoretical gap)

Paper defines **9 features**:
- Distribution: μ, **σ²**, γ₁, γ₂
- 1st-order: **Δμ, Δσ²** (variance of first differences)
- 2nd-order: σ²_Δ², H_Δ², ρ_Δ²

IBM code / unslop use **10 features**: adds σ, uses **std** (not variance) for first-order block. unslop faithfully ports the **code**, not the equation. For detection, XGBoost trained on 10-dim code vectors won't match 9-dim paper ablations.

### 6.5 unslop gaps vs deployable DivEye

1. **No BiScope booster** — PAN best system is DivEye+BiScope, not standalone
2. **No compression ratio feature** — present in HF Space (11th DivEye dim)
3. **No XGBoost / pretrained weights** — `--surprisal-variance` is voice-match telemetry, not a detector
4. **Default distilgpt2** — docstring field readings (0.6–0.9 flat, >1.5 literary) are calibrated for distilgpt2, not gpt2/falcon
5. **`surprisal_cv` unexported in `to_diveye_vector()`** — correct; not part of DivEye vector

### 6.6 Recommended unslop fixes (implementation agent)

| Priority | Change | Rationale |
|----------|--------|-----------|
| P1 | Document that `to_diveye_vector()` tracks **IBM code**, not paper Eq. 6 | Prevents false confidence in 9-dim ablation claims |
| P2 | Add `--surprisal-model gpt2` to CLI docs as paper-faithful default | distilgpt2 is fine for local speed, wrong for PAN replication |
| P3 | Wire `benchmarks/diveye_comparison/run.py` into CI with `UNSLOP_RUN_REAL_SURPRISAL=1` | Regression guard (already written, not CI-gated) |
| P4 | Optional: `to_paper_diveye_vector()` returning 9 dims per Eq. 6 | For researchers comparing to Table 8 ablations |
| Low | Match IBM short-text guard (return zeros if < 10 tokens) | Avoids meaningless stats on tiny inputs |

---

## 7. Disagreements with paper claims (implementation lens)

| Claim | Implementation reality |
|-------|------------------------|
| "Zero-shot, no fine-tuning required" | Feature extraction is zero-shot; **detection requires training XGBoost** on labeled data. HF Space uses a pretrained `model.json`. |
| "Interpretable insights pointing to where text is flagged" | **Not implemented** in GitHub repo. No saliency, no token heatmap code shipped. |
| "Robust to paraphrasing and adversarial attacks" | RAID/MAGE adversarial numbers live in TMLR paper, **not reproducible from GitHub**. No attack code bundled. |
| "Outperforms zero-shot detectors by 33.2%" | Depends on baseline and testbed; GitHub repo provides no benchmark script. |
| "Processing in ~0.01s" | True for GPT-2 CPU features on short text; **false** for HF Space production stack. |
| "Model-agnostic" | True for feature extractor; **classifier is not** — XGBoost trained on specific feature distribution. Changing scorer LM (GPT-2 → Falcon) requires retraining (PAN notebook shows Falcon+BiScope c@1 drops 0.978→0.912). |
| NC license | **Blocks commercial deployment** without separate license from authors. |

---

## 8. Comparison to unslop agent #1 (theory) scope

Agent #1 covers surprisal variance **theory**, UID hypothesis, Sadasivan bounds, evasion implications. This memo (#34) covers:

- Exact code paths and bugs
- HF Space as the actual deployment surface
- PAN notebook numbers vs claims
- Numeric alignment proof for `surprisal.py`
- Practical runbook and missing artifacts

**Non-overlap conclusion:** Theory says *widening surprisal variance helps*. Implementation says *here's the exact 10-float vector, it's numerically matched in unslop, but the public detector also needs BiScope + XGBoost + GPU, and the GitHub repo alone won't get you there.*

---

## 9. Key code references

IBM feature core (`/tmp/ibm-diveye/diveye_utils.py` cloned 2026-08-19):

```python
# 10-feature return (note: paper Eq. 6 specifies 9)
return [mean_s, std_s, var_s, skew_s, kurt_s,
        mean_diff, std_diff, var_2nd, entropy_2nd, autocorr_2nd]
```

unslop vector export (`unslop/scripts/surprisal.py:107-119`):

```python
def to_diveye_vector(self) -> list[float]:
    return [
        -self.mean_log_prob, self.surprisal_stdev, self.surprisal_variance,
        self.surprisal_skewness, self.surprisal_kurtosis,
        self.delta_surprisal_mean, self.delta_surprisal_stdev,
        self.delta2_surprisal_variance, self.delta2_surprisal_entropy,
        self.delta2_surprisal_autocorr,
    ]
```

unslop comparison harness (`benchmarks/diveye_comparison/run.py`) — loads IBM utils via importlib, compares fixture markdown files, writes JSON + markdown report.

---

## 10. Confidence & gaps

| Finding | Confidence |
|---------|------------|
| surprisal.py ↔ diveye_utils.py numeric match (GPT-2) | **High** (empirical, 9 fixtures) |
| GitHub repo incomplete for full detector reproduction | **High** |
| HF Space = production deployment path | **High** |
| Paper Eq. 6 ≠ shipped 10-feature code | **High** (primary source) |
| PAN "beats all baselines" overstated | **High** (Table 1 in notebook) |
| No independent community reproduction | **Medium** (search may miss private attempts) |
| distilgpt2 vs gpt2 rank-order preservation on unslop fixtures | **Medium** (not tested this session) |

**Open benchmarks unslop should run:**
1. distilgpt2 vs gpt2 vs falcon-7b feature correlation on humanize before/after
2. Standalone DivEye XGBoost vs DivEye+BiScope on PAN data (if license permits NC use)
3. Short-text guard behavior (< 10 tokens) across IBM vs unslop

---

*Agent #34 complete. Overlap with Agent #1 noted; implementation focus per manifest.*
