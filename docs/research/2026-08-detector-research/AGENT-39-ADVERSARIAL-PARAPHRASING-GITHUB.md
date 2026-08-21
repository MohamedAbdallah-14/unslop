# Agent #39 — Adversarial Paraphrasing GitHub Implementation

**Topic:** Code availability, reproduction, compute cost, ethical use boundaries  
**Paper:** Cheng et al., *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text*, NeurIPS 2025  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

The official implementation lives at **https://github.com/chengez/Adversarial-Paraphrasing** — Apache 2.0, ~46 stars, 7 forks, last pushed June 2025, zero open issues. It is **complete enough to run the core attack** (detector-guided token selection in `utils.py`), but **not turnkey**: SLURM scripts assume UMD cluster paths, `requirements.txt` pins a full Jupyter stack, and several paper ablations (notably guidance-frequency `N>1`) are **described in the paper but not exposed as CLI flags**.

Reproduction needs **two CUDA GPUs** (paper: 2× RTX A6000), **LLaMA-3-8B-Instruct** (~16 GB FP16) plus a guidance detector (100–350M params), and Hugging Face downloads for MAGE/RADAR/OpenAI-RoBERTa weights. Per-sample latency: **7.2 s** (simple paraphrase) → **8.6–16.7 s** (adversarial), on ~100-word MAGE samples; full 2000-sample sweep is a **multi-hour GPU job**, not a laptop demo.

**Ethical framing:** Authors position the release as **red-team / robustness research** — generating adversarial training data, stress-testing detectors at low FPR. The attack is explicitly optimized to defeat academic-integrity and watermarking systems. Unslop should **not** port AdvPara token-level search into production; the architectural lesson (distribution-shaping beats single-detector chasing) already lives in `detector.py`'s "cross-model paraphrase" escape hatch and anti-detector mode boundaries.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Official GitHub repo** | https://github.com/chengez/Adversarial-Paraphrasing |
| **Core algorithm (`utils.py`)** | https://github.com/chengez/Adversarial-Paraphrasing/blob/main/utils.py |
| **Main entry script** | https://github.com/chengez/Adversarial-Paraphrasing/blob/main/paraphrase_and_detect.py |
| **SLURM launch template** | https://github.com/chengez/Adversarial-Paraphrasing/blob/main/scripts/transfer_test.sbatch |
| **Precomputed outputs** | https://github.com/chengez/Adversarial-Paraphrasing/tree/main/outputs |
| **Paper (arXiv)** | https://arxiv.org/abs/2506.07001 |
| **Paper (HTML)** | https://arxiv.org/html/2506.07001v2 |
| **NeurIPS proceedings PDF** | https://proceedings.neurips.cc/paper_files/paper/2025/file/443f314cd420ce621b6e748fd1194ed8-Paper-Conference.pdf |
| **NeurIPS abstract page** | https://proceedings.neurips.cc/paper_files/paper/2025/hash/443f314cd420ce621b6e748fd1194ed8-Abstract-Conference.html |
| **Papers With Code entry** | https://paperswithcode.com/paper/adversarial-paraphrasing-a-universal-attack |

### Related lineage (context, not AdvPara code)

| Resource | URL | Relation |
|----------|-----|----------|
| **Krishna DIPPER paraphrase attack** (NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Baseline "simple paraphrase"; official repo https://github.com/martiansideofthemoon/ai-detection-paraphrases |
| **Sadasivan impossibility** (ICML 2023) | https://arxiv.org/abs/2305.04226 | Co-author lineage; paraphrase as fundamental detector limit |
| **RADAR detector** (robust to basic paraphrase) | https://arxiv.org/abs/2307.03898 | AdvPara still breaks it (−64.49% T@1%FPR) |
| **Fast-DetectGPT** | https://arxiv.org/abs/2305.17303 | Largest single-target drop (−98.96% T@1%FPR) |
| **MAGE dataset/detector** | https://huggingface.co/datasets/yaful/MAGE | Default eval corpus |
| **KGW watermark** | https://arxiv.org/abs/2301.10226 | Watermark eval branch in repo |
| **Unigram watermark** | https://arxiv.org/abs/2306.17439 | Second watermark eval branch |

---

## What the repo ships

### Repository metadata (Aug 2026)

- **License:** Apache 2.0 — https://github.com/chengez/Adversarial-Paraphrasing/blob/main/LICENSE  
- **Language:** Python; repo size ~16 MB (excluding LFS blobs in `outputs/`)  
- **Activity:** Created 2025-06-04; main branch last pushed 2025-06-10; 46 stars, 7 forks, 0 open issues  
- **Issues:** Two closed — #1 (dataset/output layout clarification, answered by author), #2 (contact request in Chinese)

### File map (what works out of the box)

| Path | Role |
|------|------|
| `utils.py` | **Core AdvPara loop** — `Paraphraser` class with detector-guided token selection; `MAGEDetector`, `OpenAIRoberta`, `RADAR` wrappers |
| `paraphrase_and_detect.py` | End-to-end: load MAGE/watermarked data → paraphrase → score with deploy detector → print pairs |
| `detect_existing_paraphrased_text.py` | Re-score saved paraphrases against other detectors (transfer eval without re-paraphrasing) |
| `parseNsave_paraphrased_output.py` | Parse SLURM logs → HuggingFace dataset |
| `quality_judge_utils.py` | GPT-4o judge prompts (needs `OPENAI_API_KEY`) |
| `kgw_wm/`, `uni_wm/` | Watermark detector + dataset creation code |
| `zs_detectors/` | Fast-DetectGPT and GLTR wrappers |
| `MAGE/` | MAGE deployment helpers (submodule-style copy) |
| `outputs/` | **Precomputed attack outputs** — human score baselines, guided generations per detector combo; enables ROC replot without re-running attack |
| `scripts/*.sbatch` | SLURM batch templates for attack, watermark creation, detection |

### What is *not* in the repo

1. **No pip package or CLI wrapper** — you run raw Python against cluster paths.  
2. **No guidance-frequency ablation (`N`)** — paper Table 10 varies applying detector guidance every N tokens; `utils.py` applies guidance **every step** when `adversarial=1`. No `--guidance_interval` flag.  
3. **No Docker/Colab notebook** — reproduction assumes you bring CUDA + HF cache.  
4. **No unit tests** — correctness is "matches paper numbers if you rerun our sbatch."  
5. **Hardcoded UMD paths** in sbatch: `/fs/cml-scratch/yzcheng/...`, `/fs/nexus-scratch/yzcheng/anaconda3/...`, default `hf_cache_dir=/fs/cml-scratch/yzcheng/cache2`.  
6. **LLaMA-3 weights** — not bundled; gated on Hugging Face (Meta license acceptance).  
7. **Commercial detectors** (GPTZero, Turnitin, Originality.ai) — not included; only open research detectors.

---

## Algorithm (implementation-level)

AdvPara is **gradient-free controlled generation**: at each autoregressive step, the paraphraser (LLaMA-3-8B-Instruct + fixed system prompt) proposes up to **k=50** top-p-filtered candidate next tokens (`p=0.99`). For each candidate, the code **appends the partial continuation**, runs the **guidance detector** on the decoded prefix, and picks the token minimizing the detector's "AI" score (`np.argmin(adv_scores)` when `deterministic=1`).

This is depth-1 beam search with a surrogate objective — closer to Plug-and-Play / InstructCTG than to gradient-based attacks (PPLM, CAT-Gen). The paper explicitly contrasts with gradient perturbation methods.

**Transferability claim:** Guidance pushes text toward the shared "human" manifold all detectors approximate → attack evades detectors never seen during optimization. Empirically: 4 guidance × 8 deploy detector matrix, avg **87.88% relative T@1%FPR drop** under OpenAI-RoBERTa-Large guidance.

**Quality tradeoff:** GPT-4o auto-ratings show adversarial outputs score slightly lower than simple paraphrase, but **87% still rate 4–5/5**; pairwise win rate favors simple paraphrase <50% of the time — meaning AdvPara wins on evasion with acceptable quality loss.

---

## Reproduction guide

### Minimum hardware

| Component | Paper spec | Practical minimum |
|-----------|------------|-------------------|
| GPUs | 2× NVIDIA RTX A6000 (48 GB each) | 1× 24 GB GPU *may* work with `device_map="auto"` + smaller batch; 2 GPUs preferred (paraphraser + detector colocated) |
| RAM | 16 GB (sbatch `--mem=16gb`) | 32 GB safer once HF models cache |
| Disk | ~30–50 GB | LLaMA-3-8B (~16 GB) + 4 detectors + MAGE dataset + watermark LLaMA-3.1-8B for wm eval |
| CUDA | Required | CPU-only path not implemented |

### Software setup

```bash
git clone https://github.com/chengez/Adversarial-Paraphrasing.git
cd Adversarial-Paraphrasing
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # heavy: torch 2.5.1, transformers 4.51.3, full Jupyter stack
huggingface-cli login               # for gated LLaMA-3
```

**Dependency note:** `requirements.txt` is a **frozen lab environment** (Jupyter, comet-ml, wandb, kagglehub). For a minimal repro, you likely need only: `torch`, `transformers`, `accelerate`, `datasets`, `tqdm`, `numpy`, plus detector-specific deps in subdirs. The full pin file is overkill and may conflict on Apple Silicon or older CUDA.

### Running a minimal attack

Edit hardcoded paths, then:

```bash
python paraphrase_and_detect.py \
  --dataset mage \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --guidance_classifier openai_roberta_large \
  --deploy_classifier fastdetectgpt \
  --num_samples 10 \
  --batch_size 1 \
  --top_p 0.99 \
  --adversarial 1 \
  --deterministic 1 \
  --hf_cache_dir ~/.cache/huggingface/hub
```

**Dataset selection (`--dataset`):**

- `mage` — pulls `yaful/MAGE` test split, filters AI-labeled rows (`label==0`), ~100–200 words  
- `kgwwm_mage` / `uniwm_mage` — local HuggingFace-on-disk under `kgw_wm/wm_mage` and `uni_wm/wm_mage` (included in repo or regenerate via `scripts/create_wm_mage.sbatch`)

**Detectors available:**

| Role | Choices |
|------|---------|
| Guidance (`--guidance_classifier`) | `mage`, `openai_roberta_base`, `openai_roberta_large`, `radar` |
| Deploy (`--deploy_classifier`) | above + `kgw_wm`, `uni_wm`, `fastdetectgpt`, `gltr` |

### Reproducing paper numbers without re-attacking

The `outputs/` tree contains precomputed paraphrase runs and human-text score baselines (see GitHub issue #1 for layout). Workflow:

1. Inspect `outputs/guided_generations_mage/adv/<guidance_detector>/` for adversarial texts  
2. Run `detect_existing_paraphrased_text.sbatch` against alternate deploy detectors  
3. Compare T@1%FPR against `outputs/human_text_scores/`

This is the **fastest path** to validate claims if you lack 2× A6000 for a full 2000-sample sweep.

### Known reproduction friction

| Issue | Mitigation |
|-------|------------|
| SLURM-only docs | Run `paraphrase_and_detect.py` directly; ignore sbatch `#SBATCH` headers or strip them |
| Watermark eval needs LLaMA-3.1-8B | Download separately; set `--hf_cache_dir` |
| MAGE LongFormer guidance is slowest | Use `openai_roberta_large` for faster iteration |
| Output goes to stdout | Redirect to log file; parse with `parseNsave_paraphrased_output.py` |
| No progress persistence | Crash mid-batch loses work; reduce `--num_samples` for dev |
| RADAR model is Vicuna-7B-based classifier | Extra ~14 GB download |

---

## Compute cost analysis

### Per-sample latency (paper Table 3)

Measured on 100 MAGE samples, batch size 1, 5 trials each:

| Method | Mean time (seconds) |
|--------|---------------------|
| Simple paraphrase | 7.18 ± 0.13 |
| AdvPara (OpenAI-RoBERTa-Large guidance) | 10.20 ± 0.18 |
| AdvPara (OpenAI-RoBERTa-Base guidance) | 8.64 ± 0.11 |
| AdvPara (MAGE guidance) | 16.71 ± 0.74 |
| AdvPara (RADAR guidance) | 9.69 ± 0.20 |

**Interpretation:** Adversarial overhead is **~20–130%** over simple paraphrase, dominated by guidance detector architecture (MAGE's LongFormer is the bottleneck, not the 8B LLM). Paper notes detectors are <5% of paraphraser param count but run **once per candidate token per step** — up to 50 forward passes per generated token.

### Scaling estimates

| Workload | Approximate GPU time |
|----------|---------------------|
| 1 essay (~500 words, ~700 tokens) | ~70–120 s adversarial (RoBERTa-L guidance) |
| 10-sample smoke test | ~2–3 min |
| Paper main eval (2000 samples × ~150 tokens) | **~5.7 h** (RoBERTa-L) to **~9.3 h** (MAGE guidance), batch_size=5 reduces wall time |
| Full transfer matrix (4 guidance × 8 deploy × 2000) | **Multi-day** on 2× A6000; use precomputed `outputs/` |
| GPT-4o quality eval (optional) | API cost: 2000 samples × 2 paraphrase types × judge calls ≈ **$20–80** depending on length (not reported in paper) |

### Cloud cost ballpark (Aug 2026)

- **Lambda / RunPod A6000:** ~$0.80–1.10/hr → full 2000-sample RoBERTa-L run ≈ **$5–12**  
- **Single A100 40GB:** feasible with sequential loading; ~$1.50/hr → similar total  
- **No-GPU path:** not supported; API-based paraphrase + detector would be a reimplementation, not a repro

### Memory footprint

- LLaMA-3-8B FP16: ~16 GB  
- OpenAI-RoBERTa-Large: ~1.4 GB  
- MAGE (LongFormer-large): ~1.5 GB  
- RADAR (Vicuna-7B backbone for classifier): ~14 GB — **largest guidance option**  
- **2× GPU setup** lets paraphraser and detector sit on separate devices without serial offload latency

### Efficiency ablation not wired in code

Paper Table 10: applying guidance every **N** tokens (N=5 still beats simple paraphrase) reduces latency with graceful effectiveness decay. Repo hardcodes N=1. A fork wanting production speed should add `--guidance_interval N` to `Paraphraser.paraphrase()`.

---

## Ethical use boundaries

### Authors' stated intent

The paper opens with misuse concerns (plagiarism, social engineering) and closes by recommending AdvPara for **adversarial dataset generation to improve detector robustness**. NeurIPS release under Apache 2.0 is standard for red-team research — no gated access, no click-through ethics module.

### Offensive capability (what this code actually enables)

1. **Universal detector evasion** at the operating point institutions care about (T@1%FPR, not AUC headline numbers).  
2. **Watermark breaking** without stealing the key — outperforms watermark-stealing in low-FPR regime per paper Appendix A.  
3. **Transferable attack** — user need not know which detector Turnitin/GPTZero/Canvas uses; OpenAI-RoBERTa-L guidance suffices.  
4. **Post-hoc humanization** — works on *already generated* AI text; no model access needed.  
5. **Quality-preserving** — output remains readable; not gibberish adversarial noise.

This is strictly stronger than DIPPER/simple paraphrase for evasion, with comparable readability.

### Defensive / legitimate uses

| Use case | Legitimate? | Notes |
|----------|-------------|-------|
| Detector robustness benchmarking | Yes | Primary stated purpose; aligns with RAID/SHIELD eval culture |
| Red-teaming watermark schemes | Yes | KGW/Unigram eval code included |
| Academic integrity enforcement tuning | Yes | Institutions need to know detectors fail |
| ESL false-positive testing | Partial | MAGE corpus is general web text; not Liang TOEFL protocol |
| Personal resume/portfolio polish | Gray | Same ethical space as unslop anti-detector mode |
| Submitting paraphrased AI work as human-authored | **No** | Academic misconduct; AdvPara is optimized for this |
| Disinformation / social engineering at scale | **No** | Paper explicitly lists this threat model |
| Commercial "humanizer" product backend | **No** | License permits it (Apache 2.0), but violates platform ToS at downstream services |

### unslop integration policy (recommended)

**Do not implement AdvPara-style token-level detector search in unslop.** Reasons:

1. **Architectural mismatch** — unslop is deterministic regex + optional LLM rewrite; AdvPara requires loaded 8B LM + detector in a tight generation loop.  
2. **Ethical guardrails** — `skills/unslop/SKILL.md` anti-detector mode is for ESL false positives and voice recovery, **not** academic misconduct. AdvPara is single-purpose evasion.  
3. **Existing escape hatch** — `detector.py` `feedback_loop()` already escalates intensity then recommends **cross-model paraphrase** when deterministic passes exhaust — same *family* of move without shipping the attack.  
4. **Sadasivan framing** — distribution-shaping (burstiness, surprisal variance, AI-ism removal) is more durable than optimizing one surrogate detector; see `AGENT-17-SADASIVAN-IMPOSSIBILITY.md`.

**Do use AdvPara repo for:**

- Benchmarking unslop output against precomputed `outputs/` adversarial texts  
- Calibrating `--detector-feedback` thresholds (if TMR/Desklib scores remain high after unslop, user is in AdvPara-vulnerable territory)  
- Informing README honesty about detector fragility with **cited numbers** (87.88% avg T@1%FPR drop — from real paper, not marketing)

### Regulatory / platform context

- **EU AI Act Art. 50** (transparency for AI-generated content) — AdvPara undermines technical enforcement; policy must not rely on detectors alone.  
- **OpenAI classifier withdrawal (July 2023)** — precedent that vendors exit when evasion + FP risk exceeds value.  
- **Turnitin AI detection disabled at Vanderbilt (Aug 2023)** — institutional retreat from detector-gated enforcement.

---

## Comparison to adjacent GitHub implementations

| Repo | URL | vs AdvPara |
|------|-----|------------|
| DIPPER paraphrase attack | https://github.com/martiansideofthemoon/ai-detection-paraphrases | Separate 11B paraphraser model; one-shot rewrite; **ironically increases** detection on RADAR/Fast-DetectGPT |
| TempParaphraser | (Agent #38 scope) | Temperature-based sampling; lighter but less universal |
| StealthRL | (Agent #26 scope) | RL-trained humanizer; training required vs AdvPara training-free |
| blader/humanizer | Claude skill ecosystem | LLM prompt humanization; no detector-in-loop guarantee |

AdvPara is the **most detector-aware open-source evasion repo** as of Aug 2026 — not the only paraphrase attack, but the one with NeurIPS-grade transfer eval and shipped precomputed outputs.

---

## unslop verdict

| Question | Answer |
|----------|--------|
| Is code available? | **Yes** — full attack loop, detectors, watermarks, precomputed outputs |
| Can we reproduce? | **Yes with friction** — 2× GPU, HF gated models, path editing, heavy requirements.txt |
| Compute cost? | **~10 s/sample** adversarial; **~$5–15** cloud for main table; days for full matrix |
| Should unslop ship this? | **No** — benchmark against it; keep deterministic + voice-match primary |
| Highest-value action | Add optional bench target: score unslop output vs AdvPara precomputed texts in `outputs/`; cite 87.88% / 98.96% numbers in detector-frailty docs with live URLs |

---

## Citation

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
