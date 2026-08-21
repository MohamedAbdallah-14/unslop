# Agent #05 — Fast-DetectGPT Deep Research

**Focus:** Zero-shot conditional probability curvature detector (ICLR 2024): mechanism, benchmarks, evasion, Westlake lab lineage, unslop `detector.py` comparison.  
**Date:** 2026-08-19  
**Scope:** Exhaustive internet research + read of `unslop/scripts/detector.py`.

---

## Executive summary

**Fast-DetectGPT** (Bao et al., ICLR 2024; [arXiv:2310.05130](https://arxiv.org/abs/2310.05130)) is a **zero-shot, training-free** detector that replaces DetectGPT's expensive perturbation loop with a **single-pass conditional probability curvature** statistic. For each token, it compares the observed token's log-probability under a scoring LM against the expected log-probability over alternative tokens sampled from a (possibly different) sampling LM. Machine text shows positive curvature — the model's chosen token sits on a probability peak; human text clusters near zero curvature.

The headline numbers from the paper: **0.9887 average AUROC** on five open-source generators (white-box), **0.9338** on ChatGPT/GPT-4 (black-box with GPT-J/Neo-2.7 surrogates), and **340× speedup** vs DetectGPT on XSum/A100. At strict operating points the authors report **87% recall at 1% FPR** on ChatGPT and **89% recall at 10% FPR** on GPT-4. The repo ([baoguangsheng/fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt), ~419 stars, MIT) ships experiment scripts, GPT-3/ChatGPT/GPT-4 generation data, a local CLI, and a hosted demo at [fastdetect.net](https://fastdetect.net/) with API access.

**Venue correction:** Published at **ICLR 2024**, not NeurIPS. The paper was submitted to arXiv October 2023; final v3 December 2024. NeurIPS 2025's **AdaDetectGPT** (Zhou et al.) explicitly builds on and forks this codebase.

**Benchmark reality check:** Fast-DetectGPT dominates the paper's custom five-dataset protocol (SQuAD, WritingPrompts, XSum, Yelp, Essay) but **underperforms on harder out-of-distribution suites**. On **MAGE** Testbed 2 (arbitrary domains, GPT-J), DivEye reports FastDetectGPT at **0.59 AUROC** vs DivEye **0.97** (Agent #01). TSD (same Westlake lab, Jan 2026) reports **69.69% MAGE avg** and **79.85% EvoBench avg** — beat by TSD's temporal features (71.56% / 83.36%) and TSD+ fusion (75.20% / 85.37%). **EvoBench** (ACL 2025 Findings) shows Fast-DetectGPT's AUROC **declines across model version updates** (e.g., GPT-4o-05-13 → GPT-4o-latest: 0.8003 → 0.7422) with low **EMG** (Evolving Model Generalization) scores. A partial **RAID** submission exists (PR #52, release date 2023-10-08) but lacks aggregate leaderboard score — incomplete domain/model/attack coverage.

**Evasion is the story for unslop:** The paper's own T5 sentence paraphrase attack drops Fast-DetectGPT from **0.964 → 0.872 AUROC** — smallest relative downgrade among baselines, but still a 9-point hit. Modern attacks are far harsher: **TempParaphraser** (EMNLP 2025) drives Fast-DetectGPT from **98.9% → 2.6%** accuracy on HC3; **Adversarial Paraphrasing** (NeurIPS 2025) cuts T@1%F by **98.96%** relative while *naive* paraphrase paradoxically **increases** detection (+15.03% T@1%F). **CoPA** and **ToBlend** also report severe collapse. Fast-DetectGPT's curvature signal is exactly what temperature-simulation and detector-guided paraphrase attacks target.

**unslop integration verdict:** `detector.py` correctly defaults to **TMR** (125M RoBERTa classifier, 99.28% RAID AUROC) — not Fast-DetectGPT. Fast-DetectGPT requires loading 2.7B–8B+ LMs, GPU inference, surrogate-model choice, and chunking heuristics; it is incompatible with the CLI's lazy-import, offline-first, ~500MB design. **Recommendation:** keep TMR as the live feedback-loop scorer; optionally add Fast-DetectGPT as an **academic secondary axis** in `benchmarks/` for curvature-family comparison. Do **not** replace TMR. The module's exhaustion message already cites TempParaphraser and Adversarial Paraphrasing — the right escalation when deterministic humanization fails against *any* detector, including Fast-DetectGPT.

---

## Primary URLs

| Resource | URL |
|----------|-----|
| **Paper (arXiv HTML v3)** | https://arxiv.org/html/2310.05130v3 |
| **Paper (PDF)** | https://arxiv.org/pdf/2310.05130 |
| **ICLR 2024 proceedings** | https://proceedings.iclr.cc/paper_files/paper/2024/file/6b8c6f846c3575e1d1ad496abea28826-Paper-Conference.pdf |
| **ICLR virtual poster** | https://iclr.cc/virtual/2024/poster/19201 |
| **OpenReview** | https://openreview.net/forum?id=Bpcgcr8E8Z |
| **Official GitHub** | https://github.com/baoguangsheng/fast-detect-gpt |
| **Online demo + API** | https://fastdetect.net/ |
| **WestlakeNLP product page** | https://westlakenlp.com/work.html |
| **Parent: DetectGPT** | https://github.com/eric-mitchell/detect-gpt · [arXiv:2301.11305](https://arxiv.org/abs/2301.11305) |
| **Child: AdaDetectGPT** | https://github.com/Mamba413/AdaDetectGPT · [arXiv:2510.01268](https://arxiv.org/abs/2510.01268) |
| **Sibling: MAGE benchmark** | https://github.com/yafuly/MAGE · [ACL 2024](https://aclanthology.org/2024.acl-long.3/) |
| **Sibling: TSD detector** | https://arxiv.org/html/2601.04833v1 |
| **MAGE online detector** | https://detect.westlake.edu.cn/ |
| **RAID benchmark** | https://raid-bench.xyz/ |
| **RAID partial submission** | https://github.com/liamdugan/raid/pull/52 |
| **EvoBench** | https://github.com/happy-Moer/EvoBench · [ACL 2025 Findings](https://aclanthology.org/2025.findings-acl.754/) |
| **TempParaphraser attack** | https://aclanthology.org/2025.emnlp-main.1607/ |
| **Adversarial Paraphrasing attack** | https://arxiv.org/abs/2506.07001 |
| **NAACL 2025 practical audit** | https://aclanthology.org/2025.findings-naacl.271/ |
| **unslop detector module** | `unslop/scripts/detector.py` |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | ICLR 2024 (Twelfth International Conference on Learning Representations) |
| **Authors** | Guangsheng Bao, Yanbin Zhao, Zhiyang Teng, Linyi Yang, Yue Zhang† |
| **Affiliations** | Westlake University (corresponding: Yue Zhang); Zhejiang Univ.; Shanghai Polytechnic; NTU Singapore |
| **License** | MIT (code) |
| **GitHub stats (Aug 2026)** | ~419 stars, ~82 forks, 18 open issues; active through Jan 2026 (Llama3-8B demo upgrade) |

---

## Mechanism

### Lineage: DetectGPT → Fast-DetectGPT → AdaDetectGPT / TSD+

**DetectGPT** (Mitchell et al., ICML 2023) detects machine text via **probability curvature**: LLM-generated passages sit on local maxima of the model's log-probability surface. Implementation requires ~100 T5 perturbations per passage, each scored by the source LM — prohibitive for production.

**Fast-DetectGPT** reframes curvature using **conditional probability** \(p_\theta(\tilde{x}_t \mid x)\): given the full observed passage \(x\), how probable is token \(\tilde{x}_t\) at position \(t\)? Machine tokens score higher than the conditional expectation over alternative tokens drawn from a sampling distribution \(s_t\). Human tokens sit near the expectation (zero curvature).

Three-step pipeline (Figure 2 in paper):

1. **Sample:** For each token position, draw alternative tokens from sampling model \(q\) (often same family as scorer, or GPT-J for black-box).
2. **Score:** Single forward pass of scoring model \(p\) evaluates conditional log-probs for observed + sampled tokens.
3. **Aggregate:** Normalized sampling discrepancy across tokens:

\[
d(x) = \frac{\sum_t \left[\log p(x_t \mid x) - \mathbb{E}_{\tilde{x}_t \sim s_t}\log p(\tilde{x}_t \mid x)\right]}{\sqrt{\sum_t \mathrm{Var}_{\tilde{x}_t \sim s_t}(\log p(\tilde{x}_t \mid x))}}
\]

Classify as machine-generated if \(d(x) > \epsilon\). Threshold \(\epsilon\) balances FPR/TPR; paper uses validation-set calibration.

**Settings:** White-box uses the source LLM for both sampling and scoring. Black-box defaults to GPT-J-6B sampling + Neo-2.7B scoring for ChatGPT/GPT-4. Jan 2026 demo upgrade uses Llama3-8B-Instruct for both (better on reasoning-model text). One scoring forward pass per passage vs ~100 for DetectGPT (340× speedup on XSum/A100), but still requires 2.7B–8B LM weights — not a lightweight classifier.

### Westlake lab lineage (TSD, MAGE, AdaDetectGPT)

Fast-DetectGPT is the **anchor zero-shot method** in the Westlake NLP detection stack:

| Work | Authors overlap | Relationship |
|------|----------------|--------------|
| **MAGE** (Li et al., ACL 2024) | Linyi Yang, Yue Zhang | Benchmark + Longformer supervised detector; same lab ecosystem |
| **TSD** (Sun et al., arXiv Jan 2026) | Guangsheng Bao, Yue Zhang | **Temporal complement** — late-stage volatility decay in log-prob derivatives; fuses additively with Fast-DetectGPT (TSD+) |
| **T-Detect** (Westlake, arXiv 2025) | Yue Zhang | Replaces Fast-DetectGPT's Gaussian normalization with Student's t-distribution for adversarial heavy tails |
| **AdaDetectGPT** (Zhou et al., NeurIPS 2025) | Forks Fast-DetectGPT repo | Learns witness function \(w(\log q_t)\) over Fast-DetectGPT's statistic; formal FNR/TNR bounds |

TSD explicitly treats Fast-DetectGPT's **sampling discrepancy** as a global signal and adds **second-half-sequence temporal features** (Derivative Dispersion + Local Volatility). Fusion formula: \(S_{\text{fusion}} = S_{\text{TSD}} + S_{\text{global}}\). On EvoBench, TSD beats Fast-DetectGPT by **+9.66 pp on GPT-4o** and **+7.35 pp on GPT-4** — frontier models produce fewer global curvature tells but still exhibit late-stage stabilization.

TSD = **Temporal Stability Detection** (not spectral). SpecDetect and WAVEDETECT are independent spectral approaches from other groups.

---

## Benchmarks

### Paper-native evaluation (NOT MAGE/RAID/EvoBench)

Five completion datasets (SQuAD, WritingPrompts, XSum, Yelp, Essay): 500 human paragraphs each, LLM completes from first 120 tokens. Source models: GPT-2, Neo-2.7B, GPT-J-6B, NeoX-20B, OPT-13B.

| Method | 5-Model AUROC | ChatGPT/GPT-4 AUROC | Speedup |
|--------|--------------|---------------------|---------|
| DetectGPT | 0.9554 | 0.7225 | 1× |
| **Fast-DetectGPT** | **0.9887** | **0.9338** | **340×** |

vs supervised (black-box): beats RoBERTa-base/large on average; mixed vs GPTZero (GPTZero wins news, loses stories/technical). Decoding robustness strong (95–99% relative gain over DetectGPT on top-p/k/temperature) — but TempParaphraser exploits exactly the temperature-entropy vulnerability this implies.

### MAGE (Li et al., ACL 2024)

MAGE is a **same-lab benchmark** (co-author Linyi Yang) with 27 LLMs, 8 testbeds, increasing "wildness." Fast-DetectGPT is **not the MAGE paper's primary focus** but appears as a zero-shot baseline in follow-on work.

| Source | Setting | Fast-DetectGPT | Best competitor |
|--------|---------|---------------|-----------------|
| DivEye paper (Agent #01) | MAGE Testbed 2 (GPT-J, arbitrary domains) | **0.59 AUROC**, 56.4% AvgAcc | DivEye **0.97** |
| TSD paper (Jan 2026) | MAGE average (7 families) | **69.69%** | TSD **71.56%**, TSD+ **75.20%** |

**Interpretation:** Fast-DetectGPT's global curvature signal **breaks under domain shift and diverse generators** — exactly the "in the wild" scenario MAGE targets. The 0.59 vs 0.97 gap on Testbed 2 is catastrophic for deployment claims extrapolated from the paper's in-domain 0.99 AUROC.

MAGE's supervised Longformer (`yaful/MAGE` on HuggingFace) remains the lab's recommended production detector for wild settings; online demo at [detect.westlake.edu.cn](https://detect.westlake.edu.cn/).

### RAID (Dugan et al., ACL 2024)

RAID: 11 LLMs × 11 genres × 4 decoding strategies × 12 adversarial attacks; >10M documents. The canonical stress test for 2026 detector evaluation.

**Fast-DetectGPT RAID status:** Partial submission in [raid PR #52](https://github.com/liamdugan/raid/pull/52) (FastDetectGPT, release 2023-10-08). GitHub bot warning: **no aggregate leaderboard score** — incomplete coverage of domains/models/decoding/attacks. Per-split results only.

Cross-reference from sibling agents: TMR (`Oxidane/tmr-ai-text-detector`) reports **99.28% RAID AUROC**; DivEye **0.984** vs Binoculars **0.844**. Fast-DetectGPT has **no published full RAID number** competitive with these supervised detectors. TempParaphraser reports **92.3% average relative reduction** in Fast-DetectGPT detection accuracy across 5 LLMs × 6 RAID domains.

### EvoBench (Yu et al., ACL 2025 Findings)

EvoBench tests **generalization across evolving LLMs** — 7 families, 29 versions, two evolution pathways (publisher updates + developer fine-tunes/prunes). Introduces **EMG** (Evolving Model Generalization) metric alongside AUROC.

Key Fast-DetectGPT findings:

- **High per-version AUROC, low EMG:** Can score 0.91 AUROC on individual models while failing to generalize across version updates.
- **GPT-4o decay:** 0.8003 (GPT-4o-05-13) → 0.7422 (GPT-4o-latest).
- **EvoBench average (TSD paper Table 3):** Fast-Detect **79.85%** vs TSD **83.36%** vs TSD+ **85.37%**.
- **Mitigation tested:** Pruning scoring model to Sheared-LLaMA extracts shared features; improves zero-shot family including Fast-DetectGPT on LLaMA-2 development variants.

**Takeaway:** Static benchmark numbers (including Fast-DetectGPT's 0.99) **overestimate real-world durability** as models update monthly.

### Attack benchmarks (2025–2026)

| Attack | Fast-DetectGPT result |
|--------|----------------------|
| TempParaphraser (HC3) | 98.9% → **2.6%** accuracy |
| Adversarial Paraphrasing | T@1%F **−98.96%** relative; naive paraphrase **+15%** |
| CoPA / ToBlend / DIPPER | TPR@5%F → ~3–13%; AUC 0.98→0.40; 72.9% remaining |
| NAACL 2025 audit (Tufts et al.) | TPR@0.01F as low as **0%** OOD |
| SurpMark OOD paraphrase | 83–98% AUROC vs SurpMark 99.2–99.8% |

---

## Debate

### What proponents claim

1. **SOTA zero-shot speed/accuracy tradeoff (2023–2024 window):** 340× faster than DetectGPT with ~75% relative AUROC gain. Establishes conditional curvature as the efficient successor to perturbation-based detection.
2. **Black-box viability:** Surrogate GPT-J/Neo-2.7B beats DetectGPT white-box on average; 80% ChatGPT recall at 1% FPR in paper Figure 4.
3. **Beats GPTZero on consistency** across domains in paper's GPT-3/4 evaluation (though GPTZero wins on news).
4. **Production path exists:** [fastdetect.net](https://fastdetect.net/) demo, API, Jan 2026 Llama3-8B upgrade for reasoning-model text. WestlakeNLP markets free API keys.
5. **Paraphrase resilience (within paper's attack model):** Smallest relative AUROC drop under T5 sentence paraphrase (0.964 → 0.872) among baselines; authors argue decoherence drives the drop, not paraphrase per se.

### What critics and follow-on work show

1. **Sadasivan et al. (2023) paraphrase impossibility:** Fast-DetectGPT inherits the fundamental limit — paraphrase breaks likelihood-based detection. Paper's T5 attack is mild; 2025 attacks are not.
2. **Nicks et al. / ICLR 2024 "advise against reliance":** `detector.py` already cites this. Fast-DetectGPT does not escape the structural critique.
3. **Liang et al. ESL bias:** Paper §5 acknowledges LLM detectors may **elevate false positives on non-native English** — same concern as GPTZero-era audits.
4. **MAGE/EvoBench OOD collapse:** 0.59 AUROC on wild testbeds; EMG degradation across model versions. Static paper numbers mislead.
5. **Naive paraphrase can *help* detectors:** Adversarial Paraphrasing shows simple LLM paraphrase **increases** Fast-DetectGPT T@1%F by +15.03% — coherence disruption creates detectable artifacts. unslop's regex-only humanization may share this failure mode on curvature detectors.
6. **Surrogate-model dependency:** Black-box detection quality depends on sampling/scoring model pairing. Wrong surrogate → wrong curvature baseline. Closed API text from GPT-4o scored with Neo-2.7B is a guess, not ground truth.
7. **Community reproduction gap:** 419 stars but attack papers (TempParaphraser, AdvPara) treat it as a **straw-man baseline** to demolish. Independent full RAID reproduction absent.

**Community footprint:** ~419 GitHub stars, active through Jan 2026 (Llama3 demo, API). Default zero-shot baseline in 2025–2026 attack papers — cited to be beaten. Venue is **ICLR 2024**, not NeurIPS (AdaDetectGPT at NeurIPS 2025 is the direct extension).

---

## Humanization

### Attack taxonomy vs Fast-DetectGPT

| Attack | Effect |
|--------|--------|
| T5 paraphrase (paper) | AUROC 0.964 → 0.872 |
| TempParaphraser | **98.9% → 2.6%** (HC3) |
| Adversarial Paraphrasing | −98.96% T@1%F; naive paraphrase **+15%** |
| Cross-model rewrite | Strongest lever — already in `detector.py` exhaustion message |

unslop's regex/structural/soul pipeline reshapes lexicon and syntax, not token-level curvature. Cross-model paraphrase is the exit ramp. **Do not rely on synonym swaps** — can increase Fast-DetectGPT scores (AdvPara finding).

---

## unslop integration

### Current `detector.py` architecture

```python
DetectorName = Literal["tmr", "desklib"]
DEFAULT_DETECTOR: DetectorName = "tmr"
```

| Aspect | TMR (current default) | Fast-DetectGPT (not integrated) |
|--------|----------------------|--------------------------------|
| **Type** | Supervised RoBERTa classifier | Zero-shot LM curvature |
| **Size** | ~125M params (~500MB) | 2.7B–8B+ (~5–16GB) |
| **Inference** | Single forward pass, chunked | Full sequence + sampling stats |
| **Deps** | torch, transformers | + specific LM weights, GPU strongly recommended |
| **Offline** | Yes (HF cache) | Yes but impractical on laptop |
| **RAID AUROC** | 99.28% (claimed) | No full leaderboard entry |
| **API shape** | `score_ai_probability(text) -> float [0,1]` | Raw discrepancy → sigmoid/threshold mapping needed |

`feedback_loop()` escalates: balanced → full → full+structural+soul, scoring after each pass. On exhaustion, recommends cross-model paraphrase citing TempParaphraser and Adversarial Paraphrasing — **correct for Fast-DetectGPT evasion**.

Not wired as a `DetectorName`. Integration would need LM pair loading, z-score→probability mapping, sequence-level chunking, and `fetch_detectors` bootstrap — high cost, low production value. Use as **benchmark-only research axis**; keep TMR in production, Desklib as optional release gate.

---

## P0 / P1 / P2 actions

### P0 — Do now

| # | Action | Owner | Done when |
|---|--------|-------|-----------|
| 1 | **Confirm TMR remains default** — no Fast-DetectGPT in live `feedback_loop` without explicit opt-in | eng | Architecture decision documented |
| 2 | **Add Fast-DetectGPT to detector research index** (`AGENT-MANIFEST-100.md` → complete) | docs | Manifest row updated |
| 3 | **Fix venue in any user-facing copy** — ICLR 2024, not NeurIPS | docs | Grep clean |

### P1 — Next sprint

| # | Action | Owner | Done when |
|---|--------|-------|-----------|
| 4 | **Benchmark script:** score 10 `drafts/2026-05-detector-test/test-texts/` samples with TMR vs local Fast-DetectGPT (Neo-2.7B/GPT-J) pre/post unslop | research | CSV with delta columns |
| 5 | **Document naive-paraphrase regression** in anti-detector skill — AdvPara +15% T@1%F on Fast-DetectGPT | docs | Skill.md warning block |
| 6 | **Track TSD+ fusion code release** from Westlake — may supersede standalone Fast-DetectGPT | research | Watch baoguangsheng GitHub |

### P2 — Backlog

| # | Action | Owner | Done when |
|---|--------|-------|-----------|
| 7 | **Submit Fast-DetectGPT (Llama3-8B pair) to RAID** via `raid-bench` CLI for ground-truth vs TMR | research | Leaderboard entry |
| 8 | **Optional `--detector fastdetect`** behind env flag `UNSLOP_ENABLE_FASTDETECT=1` | eng | PR with lazy import + tests |
| 9 | **Replicate TempParaphraser attack on unslop output** — measure whether ladder + cross-model recommendation actually reaches <5% Fast-DetectGPT accuracy | research | Memo with numbers |
| 10 | **Evaluate AdaDetectGPT** (NeurIPS 2025 child) as academic upgrade path — same integration cost, marginal paraphrase gain | research | Agent #04 cross-ref validated |

---

## Open questions

1. **Llama3-8B demo vs paper Neo-2.7B:** Do Jan 2026 model choices change attack-surface numbers?
2. **Chunking curvature:** Correct aggregation for long docs (max vs mean discrepancy)?
3. **unslop vs Fast-DetectGPT:** Does structural+soul raise or lower curvature? AdvPara suggests naive edits can increase detection.
4. **TMR vs Fast-DetectGPT disagreement:** Which predicts commercial detectors on RAID?
5. **AdaDetectGPT / TSD+ release:** Will Westlake ship drop-in upgrades that survive TempParaphraser?
6. **ESL false positives:** Paper cites Liang et al. but provides no ESL-specific eval — critical for unslop's defensive use case.

---

*Agent #05 complete. Cross-refs: Agent #01 (DivEye/MAGE), Agent #02 (TSD), Agent #04 (AdaDetectGPT), Agent #24 (TempParaphraser), Agent #25 (Adversarial Paraphrasing).*
