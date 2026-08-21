# Agent #38 — TempParaphraser Repo + Reproduction

**Topic:** HJJWorks/TempParaphraser — practical deployment, independent runs, GPU, unslop integration  
**Prepared:** August 19, 2026  
**Scope:** Reproduction path, repo health, hardware, license, integration difficulty for unslop anti-detector stack  
**Status:** complete

---

## Executive summary

TempParaphraser (EMNLP 2025) is a **sentence-level, detector-guided multi-sample paraphraser**. It is not a regex pass or a prompt tweak. It runs a fine-tuned Llama paraphrasing model through a vLLM HTTP API, generates N candidates per sentence, and picks the candidate with the **lowest AI-detector score** (HC3 or SuperAnnotate RoBERTa by default).

The paper claims an **82.5% average reduction in detector accuracy** with preserved quality (semantic similarity ~0.96+). Code and a ~4.9 GB HF checkpoint are public. Community signal is near zero: **4 GitHub stars, 0 forks, 0 issues, 67 HF downloads** (as of Aug 2026). No independent replication threads found.

**Reproduction verdict:** Medium-hard. The algorithm is simple; the **stack is fragile**. README has env-name typos; the main shell script references a **missing file** (`attack/paraphraser.py`). Backend depends on LLaMA-Factory + vLLM with un-pinned versions — a known breakage surface. Eval-only reproduction (using shipped `result/` JSON) is easy and needs only a GPU for RoBERTa scoring.

**Unslop integration verdict:** Do **not** vendor the repo or model into PyPI (license: academic-only, commercial prohibited). **Do** port the *selection loop* into Phase 3 `llm_pipeline.py` S3: batched multi-candidate sentence rewrite scored by existing `detector.py` (TMR). That captures the mechanism without the LLaMA-Factory/vLLM tax. Fix the incorrect comment in `detector.py:391` that says TempParaphraser needs "no LLM call" — the released system absolutely does.

---

## 1. Canonical links

| Resource | URL |
|----------|-----|
| GitHub repo | https://github.com/HJJWorks/TempParaphraser |
| HF model | https://huggingface.co/huangjj877/TempParaphraser |
| Paper (ACL) | https://aclanthology.org/2025.emnlp-main.1607 |
| Paper PDF | https://aclanthology.org/2025.emnlp-main.1607.pdf |
| DOI | https://doi.org/10.18653/v1/2025.emnlp-main.1607 |
| LLaMA-Factory (required backend) | https://github.com/hiyouga/LLaMA-Factory |
| Paraphraser base (HF metadata) | https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct |
| HC3 detector (selection default) | https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta |
| SA detector (alt selection) | https://huggingface.co/SuperAnnotate/roberta-large-llm-content-detector |

---

## 2. What the system actually does (implementation, not paper prose)

### 2.1 Algorithm

From `attack/attack_for_experiment.py`:

1. Split input on `.` (period) — **English-only, naive segmentation**.
2. For each segment with >4 words: call OpenAI-compatible chat API (`openai.ChatCompletion`, v0.28 API) with `n=rewrite_times` at `temperature`.
3. Score each candidate with a **local RoBERTa detector** on `prefix + candidate` (prefix = text rewritten so far).
4. Return the candidate with **minimum AI probability**.
5. Concatenate sentences; repeat for multi-round attack (shell default: 7 rounds at T=1.2).

Paper defaults for diversity analysis: **N=7, T=1.0** (Appendix G). Shell script ships **Times=7, Temp=1.2**.

### 2.2 Model artifact

| Field | Value |
|-------|-------|
| HF repo | `huangjj877/TempParaphraser` |
| Weights | `model.safetensors` ≈ **4.94 GB** |
| Architecture (config.json) | 16 layers, hidden 2048 → **Llama ~1B class** |
| Config `_name_or_path` | Says `Llama-3.2-3B-Instruct` — **metadata mismatch**; HF tags say 1B base |
| Template (vLLM yaml) | `llama3` |
| dtype | float32 in config |
| Gated | No |
| Downloads | 67 (Aug 2026) |

### 2.3 Inference backend

`attack/start_paraphrasing_model_vllm.yaml`:

```yaml
model_name_or_path: model/TempParaphraser
template: llama3
infer_backend: vllm
vllm_gpu_util: 0.3
vllm_enforce_eager: true
vllm_maxlen: 1024
```

Launch: `API_PORT=10001 llamafactory-cli api attack/start_paraphrasing_model_vllm.yaml`

Attack client hits `http://0.0.0.0:10001/v1` via legacy OpenAI Python SDK.

---

## 3. Reproduction tiers

### Tier A — Eval only (fastest sanity check)

**Goal:** Confirm paper numbers on precomputed outputs without running paraphrase.

| Step | Action |
|------|--------|
| 1 | Clone https://github.com/HJJWorks/TempParaphraser |
| 2 | `conda create -n tp python=3.10 && pip install -r requirements.txt` (+ torch with CUDA) |
| 3 | Run `eval/eval_neural_detector_ACC.py --detector hc3 --tests result/TempParaphraser-n7-T1.2.json` |

Repo ships ~130 MB pre-attacked JSON files under `result/` plus `test_data/test_rnd10k.jsonl`. No vLLM needed.

**Hardware:** GPU strongly expected — `attack_for_experiment.py` hardcodes `device = torch.device("cuda")`. CPU fallback not implemented.

### Tier B — Single-text paraphrase (minimal live run)

| Step | Action |
|------|--------|
| 1 | Download HF model → `TempParaphraser/model/TempParaphraser/` |
| 2 | Separate conda env: LLaMA-Factory + vLLM (`pip install -e ".[vllm]"`) |
| 3 | Pin versions (see §5) — do not `pip install` latest blind |
| 4 | Start vLLM API backend on port 10001 |
| 5 | Call `rewrite_text()` from `attack/attack_for_experiment.py` with `--api http://0.0.0.0:10001/v1` |

**Do not** run `bash attack/attack_for_experiment.sh` as written — it invokes **`attack/paraphraser.py`, which does not exist** in the repo tree (verified via GitHub API recursive listing, Aug 2026). Use `attack_for_experiment.py` directly or fix the shell script locally.

### Tier C — Full paper replication

Additional requirements beyond Tier B:

- HC3 test subset (`test_data/test_rnd10k.jsonl` included)
- Fast-DetectGPT eval stack under `eval/fast_detect_gpt/` (reference JSON blobs included; live Fast-DetectGPT needs gpt-j-6B + gpt-neo-2.7B refs)
- Detectors: HC3, SA, Fast-DetectGPT, TOCSIN, RADAR (paper Table 8 / Figure 14)
- Multi-round + hyperparameter sweep (N, T)

Expect **days** of engineering for dependency pinning alone. Paper used Llama-3.1-8B for *generation* of attack inputs; paraphraser is separate fine-tuned 1B-class model.

---

## 4. GPU and hardware requirements

Repo README does **not** state minimum VRAM. Derived from artifacts:

| Component | VRAM estimate | Notes |
|-----------|---------------|-------|
| TempParaphraser model (FP32 ~1B) | ~5 GB weights | vLLM may quantize internally depending on build |
| vLLM KV cache | +1–3 GB | `vllm_maxlen: 1024`, `vllm_gpu_util: 0.3` caps utilization at 30% of device |
| HC3/SA selector (RoBERTa) | ~0.5–1.5 GB | Loaded in **same Python process** as attack script during live paraphrase |
| Fast-DetectGPT (full eval) | +10–20 GB | Separate eval path; not needed for paraphrase-only |

**Practical minimum:** **1× GPU with ≥12 GB VRAM** (RTX 3060 12GB, T4 16GB, M4 Pro not supported — CUDA hardcoded). Comfortable: **16 GB+** (RTX 4080, A10).

**Not supported out of box:** Apple Silicon MPS, CPU-only inference, Windows without CUDA toolchain for vLLM.

**Throughput:** Paper positions vLLM for batch throughput. Sentence-level loop with N=7 candidates × multi-round = **many API calls per paragraph**. Budget ~1–5 s/sentence on 1B + vLLM (order-of-magnitude; not benchmarked in this memo).

Compare to DIPPER (T5-XXL 11B): TempParaphraser is **much lighter** (~5 GB vs ~40 GB) but still requires a **serving stack**, not a pip one-liner.

---

## 5. Known breakage points (repo + upstream)

### 5.1 TempParaphraser repo issues

| Issue | Severity | Detail |
|-------|----------|--------|
| Missing `attack/paraphraser.py` | **Blocker** for README shell path | `attack_for_experiment.sh` line 7 calls nonexistent file |
| README env typo | **Blocker** for copy-paste | Says `conda activate llama` after creating `llamafactory` env |
| `openai==0.28` | **Fragile** | Deprecated ChatCompletion API; conflicts with modern openai SDK if envs merge |
| Naive `.` segmentation | **Quality** | Breaks abbreviations, decimals, non-English; authors acknowledge — suggest BlingFire |
| No `license` field on GitHub | **Legal** | HF README: research only, commercial prohibited |
| Zero community issues | **Signal** | 0 GitHub issues — no documented fixes from users |

### 5.2 LLaMA-Factory + vLLM (upstream, affects every run)

TempParaphraser pins **nothing**. Fresh install pulls moving targets. Representative breakages:

| Upstream issue | URL | Symptom |
|----------------|-----|---------|
| transformers 4.57+ vs LLaMA-Factory | https://github.com/hiyouga/LLaMA-Factory/issues/9364 | ImportError on `is_torch_sdpa_available` |
| vLLM 0.11+ API rename | https://github.com/hiyouga/LLaMA-Factory/issues/9503 | `disable_log_requests` → `enable_log_requests` |
| vLLM version skew | https://github.com/hiyouga/LLaMA-Factory/issues/6523 | `limit_mm_per_prompt` unexpected kwarg |
| Module path / Python 3.11 | https://github.com/hiyouga/LLaMA-Factory/issues/6909 | `No module named 'llamafactory'`; use Python 3.10 |

**Mitigation recipe (unverified pin set — treat as starting point):**

```bash
conda create -n tempparaphraser-vllm python=3.10 -y
conda activate tempparaphraser-vllm
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
git checkout a711bce664fa  # Oct 2025 commit cited in LLaMA-Factory issue #9503 thread
pip install -e ".[vllm]"
# If API fails, try vllm==0.6.6 per LLaMA-Factory issue #6523 maintainer suggestion
```

Re-verify after any pin change. **No CI in TempParaphraser repo** to catch drift.

### 5.3 Independent reproduction signal

| Metric | Value (Aug 2026) |
|--------|------------------|
| GitHub stars | 4 |
| Forks | 0 |
| Open issues | 0 |
| Last push | 2025-10-28 |
| HF downloads | 67 |
| Independent replication reports | **None found** (web + GitHub search) |

Unslop research corpus already flagged this: `docs/research/17-industry-blogs-case-studies/C-opensource.md` — "hasn't been replicated independently."

---

## 6. Detectors used in paper vs unslop

| Role | TempParaphraser | unslop `detector.py` |
|------|-----------------|----------------------|
| Selection during attack | HC3 or SA RoBERTa (output probability only) | TMR (125M RoBERTa) or Desklib |
| Eval targets | HC3, SA, Fast-DetectGPT, TOCSIN, RADAR, watermark | TMR default; bench against commercial separately |
| Transfer claim | Table 8: selector trained on one detector evades others | **Not validated** for TMR — assume partial transfer, not 82.5% |

Paper Table 8 (HC3 selector, N=7): HC3 → 2.1%, SA → 1.9%, Fast-DetectGPT → 2.6%, RADAR → 45.4%. Cross-detector transfer is real but **not uniform** (RADAR still ~45%).

unslop's `--detector-feedback` ladder optimizes TMR locally. TempParaphraser's 82.5% figure is an **average across detectors/datasets** — do not cite as TMR guarantee.

---

## 7. unslop integration assessment

### 7.1 Current state

| Location | Integration |
|----------|-------------|
| `unslop/scripts/detector.py:389–407` | Names TempParaphraser in ladder-exhaustion recommendation |
| `skills/unslop/SKILL.md` step 6 | Recommends cross-model second pass; cites 82.5% |
| `README.md` | Same citation in anti-detector guidance |
| `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md` | Phase 3 S3: "TempParaphraser multi-sample" in planned `llm_pipeline.py` |

**No code calls TempParaphraser today.** Citation-only.

### 7.2 Comment bug to fix

`detector.py:391` says TempParaphraser works via "temperature-simulation paraphrase with **no LLM call needed**." That is **wrong for the released repo**. The method requires N LLM generations per sentence via fine-tuned Llama + vLLM. The accurate reading: no access to *source generator* logits; paraphraser is post-hoc. Track as doc fix, not blocker.

### 7.3 Integration options (ranked by practicality)

| Option | Effort | Fits unslop? | Notes |
|--------|--------|--------------|-------|
| **A. Algorithm port (recommended)** | 2–3 weeks in Phase 3 | Yes | S3 in `llm_pipeline.py`: for flagged sentences, request N paraphrases from existing LLM path; score with TMR; pick min. No HF model, no vLLM. |
| **B. Optional subprocess to local TempParaphraser API** | 1 week glue + user docs | Marginal | Power-user only; document conda + GPU setup; cannot ship in wheel |
| **C. Vendor HF checkpoint in plugin** | N/A | **No** | Academic-only license; commercial use prohibited |
| **D. Cross-model API capstone (already planned S5)** | Low incremental | Yes | Weakest faithful copy of paper's transfer effect; different model family, not multi-sample same model |

### 7.4 Recommended S3 spec (for Phase 3)

```
Input: sentence S, context prefix P, budget N (default 5), temperature T (default 1.0)
Loop:
  candidates = LLM.complete(system=PARAPHRASE_PROMPT, user=S, n=N, temperature=T)
  scores = [detector.score(P + c) for c in candidates]
  return candidates[argmin(scores)]
```

Prompt: use paper's fine-tune system prompt verbatim (Appendix I.2):

> "Rewrite the following text to sound more natural and human-like. Maintain the same information and overall structure, but use more casual language, varied sentence structures, and subtle personal touches."

**Preservation:** run unslop `_protect()` before sentence split; never paraphrase inside code fences.

**Budget presets** (from UPDATE-PLAN): fast N=3, balanced N=5, max N=7 — maps to paper's N=7.

### 7.5 Boundaries (unchanged)

- ESL false-positive defense, resume humanization: legitimate
- Academic misconduct evasion: decline
- Watermark removal: refuse (EU AI Act Art. 50)
- Do not market "82.5% reduction" without unslop's own bench on TMR + commercial screenshots

---

## 8. Decision matrix

| Question | Answer |
|----------|--------|
| Can we reproduce paper numbers today? | **Eval-only: yes** (shipped JSON). **Live paraphrase: yes with effort**, after fixing shell script + pinning LLaMA-Factory/vLLM. |
| Minimum GPU? | **~12 GB VRAM**, CUDA, Linux preferred |
| Is the repo maintained? | **Low activity** — last push Oct 2025, zero community |
| Should unslop depend on it? | **No** — license + ops burden |
| Should unslop implement its pattern? | **Yes** — S3 multi-sample + TMR selection in `llm_pipeline.py` |
| Is 82.5% transferable to unslop users? | **No guarantee** — detector set, domains, and TMR differ |

---

## 9. Suggested verification checklist (maintainer)

- [ ] Tier A eval on `result/TempParaphraser-n7-T1.2.json` with HC3 script — record gpt_acc
- [ ] Tier B: one paragraph through live vLLM backend — manual read for semantic drift
- [ ] Score before/after with unslop TMR — compare delta to paper direction (should drop)
- [ ] File issue upstream: missing `paraphraser.py`, README env typo (optional courtesy)
- [ ] Fix `detector.py:391` comment in separate PR
- [ ] Phase 3: implement S3 without vendoring model

---

## 10. Sources

- https://github.com/HJJWorks/TempParaphraser
- https://huggingface.co/huangjj877/TempParaphraser
- https://aclanthology.org/2025.emnlp-main.1607
- https://github.com/hiyouga/LLaMA-Factory/issues/9364
- https://github.com/hiyouga/LLaMA-Factory/issues/9503
- https://github.com/hiyouga/LLaMA-Factory/issues/6523
- https://github.com/hiyouga/LLaMA-Factory/issues/6909
- https://docs.vllm.ai/en/latest/configuration/conserving_memory/
- unslop: `unslop/scripts/detector.py`, `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md`
