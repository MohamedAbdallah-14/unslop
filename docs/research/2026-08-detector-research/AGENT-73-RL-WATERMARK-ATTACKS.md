# Agent #73 — RLCracker / RLSpoofer Watermark Attacks

**Topic:** Hanbo Huang et al. (Shiyu Liang lab, SJTU) — GRPO-based RL watermark **removal** (RLCracker) and **spoofing** (RLSpoofer)  
**Prepared:** August 19, 2026  
**Scope:** Papers, code, benchmarks, SIRA/B⁴/WaterPark debate, unslop ethics + README implications  
**Status:** complete

---

## Executive summary

**RLCracker** and **RLSpoofer** are a paired attack family from the same research group. Both use **GRPO + 100 training pairs + zero detector access**, framing watermark robustness as **KL-divergence distributional optimization** rather than fixed-paraphrase red-teaming. They are mirror-image objectives:

| Attack | Direction | Headline result | Venue |
|--------|-----------|-----------------|-------|
| **RLCracker** | Shift paraphrase **away from** watermarked distribution → human-like | **98.5% ESR** on 1,500-token Unigram (Qwen2.5-3B); 10 schemes | ICML 2026 (accepted) |
| **RLSpoofer** | Shift paraphrase **toward** watermarked distribution | **62.0% SSR** on PF-Watermark (Qwen3-4B); 6 schemes | arXiv Apr 2026 (preprint) |

Together they close the loop on the watermark threat model: an adversary can both **strip** provenance from real AI text and **forge** provenance onto human text — with **100 samples**, not B⁴'s 100k distillation corpus.

**Benchmark context:** WaterPark (Agent #20) and MarkLLM still benchmark DIPPER/GPT paraphrase, not adaptive RL. SIRA (Agent #71) reports ~100% removal but RLCracker argues SIRA **fails semantic-preserving ESR** (88% raw removal, P-SP 0.47). RL attacks are the **2025–2026 worst-case bar** for EU AI Act Art. 50 watermark assumptions.

**Unslop verdict:** RLCracker/RLSpoofer are **not** unslop competitors — they target statistical watermarks, not AI-text detectors. But they **quantify the side effect** already in `skills/unslop/SKILL.md`: any humanization pass that preserves meaning can scrub KGW/SynthID/PF signals. unslop must **not** ship RL watermark-stripping modes, **must** cite this work in provenance/ethics docs, and should update the landscape paragraph: SIRA is no longer the only sample-efficient RL-class attack; RLCracker generalizes across long-form text with semantic fidelity.

---

## 1. Research lineage — same lab, opposite gradients

| Field | RLCracker | RLSpoofer |
|-------|-----------|-----------|
| **Title** | Evaluating the Worst-Case Vulnerability of LLM Watermarks with Adaptive RL Attacks | A Lightweight Evaluator for LLM Watermark Spoofing Resilience |
| **arXiv** | [2509.20924](https://arxiv.org/abs/2509.20924) (Sep 2025; v2 revised) | [2604.11546](https://arxiv.org/abs/2604.11546) (Apr 2026) |
| **Venue** | **ICML 2026** ([poster 63933](https://icml.cc/virtual/2026/poster/63933)) | Preprint (no venue at research time) |
| **Authors** | Hanbo Huang, Yiran Zhang, Hao Zheng, Xuan Gong, Yihan Li, Lin Liu, Shiyu Liang | Hanbo Huang, Xuan Gong, Yiran Zhang, Hao Zheng, Shiyu Liang |
| **Affiliation** | SJTU (+ collaborators on RLCracker) | Shanghai Jiao Tong University |
| **Code** | [github.com/OTTO-OTO/RLCracker](https://github.com/OTTO-OTO/RLCracker) (released) | **Withheld during review**; acceptance-conditional release per Appendix C.10 |
| **Shared toolkit** | MarkLLM for watermark gen/detect | MarkLLM + PMark official repo |

**Conceptual pair:** Both papers argue prior watermark evals test **average-case fixed paraphrasers** (DIPPER, GPT-4o, SIRA templates) while a real adversary optimizes **policy + prompt context**. Both introduce a **KL-based theoretical certificate** (adaptive robustness radius vs local capacity bottleneck) and train a **3–4B GRPO policy** to approximate worst-case distributional shift.

**Not the same as B⁴:** B⁴ (Baizhou Huang, NAACL 2025, [2411.01222](https://arxiv.org/abs/2411.01222)) is a **distillation** scrubber needing **~100k** watermarked samples. RLCracker cites B⁴ as data-hungry; Hanbo Huang's RL line replaces distillation with **100-pair GRPO**. Same surname, different authors and method family.

---

## 2. RLCracker — watermark removal

### 2.1 One-line contribution

Introduce **adaptive robustness radius** (certified semantic margin under adaptive paraphrase) and **RLCracker**, a detector-free GRPO attack that maximizes token-wise \(D_{\mathrm{KL}}(Q \| P_{wm}) - D_{\mathrm{KL}}(Q \| P_h)\) using only **(question, watermarked-response)** pairs.

### 2.2 Threat model

| Dimension | Specification |
|-----------|---------------|
| **Objective** | Paraphrase watermarked text \(X \to X'\) with detector score below threshold |
| **Knowledge** | No secret key, no detector API, no watermark algorithm internals |
| **Capability** | Query watermarked generator; collect pairs; tune paraphraser \(\pi_\theta\) and system prompt |
| **Success (ESR)** | Fraction rephrased as **unwatermarked** with **P-SP > 0.7** (semantic fidelity gate) |

ESR is stricter than raw **removal rate (Rem.)** — the metric SIRA optimizes.

### 2.3 Method sketch

1. **Theory (§4.1):** Instance-level worst-case radius \(r^\star(\mathbf{X})\) is intractable → relax to **KL adaptive radius** over local paraphrase distributions. Sub-Gaussian detector scores yield computable lower bound \(\rho^\*\) correlating with removal rate (Pearson −0.77, Spearman < −0.9 on green-list schemes).
2. **Pass@k insight:** Multi-sample paraphrase succeeds without detector (Pass@20 → 89% on EWD); RL goal is **Pass@1 ≈ Pass@k** without oracle reranking.
3. **RLCracker (§4.2):** GRPO on Qwen3 family; token KL reward steers away from \(P_{wm}\) (reference model conditioned on watermarked text) toward \(P_h\) (reference conditioned on original question). Semantic reward = normalized P-SP with sigmoid scaling. Training: **100 × 500-token pairs**, batch 48, group size 12, ~1.5 h on 4× A100 for Qwen3-4B.

### 2.4 Experimental setup

| Component | Detail |
|-----------|--------|
| **Victim LLMs** | Llama-3.1-8B-Instruct, Qwen2.5-1.5B/32B-Instruct |
| **Attackers** | Qwen3-0.6B / 1.7B / 4B / 8B; Qwen2.5-3B-Instruct |
| **Watermarks (10)** | EWD, KGW, KGW_selfhash, UPV, SWEET, Unigram, SIR, X-SIR, SynthID-Text, PF-Watermark — all via MarkLLM defaults |
| **Text lengths** | 250, 500, **1500** tokens |
| **Training data** | 100 prompt–watermarked pairs from WritingPrompts |
| **Eval data** | WritingPrompts, LFQA, MMW BookReport/FakeNews |
| **Baselines** | Base, Think, SysP, Think+SysP, SIRA, DIPPER, GPT-4o |

### 2.5 Headline results

**Canonical benchmark (Table 5):** Qwen2.5-3B-Instruct RLCracker on **1500-token Unigram**:

| Method | ESR (%) | Rem. (%) | P-SP |
|--------|---------|----------|------|
| Base | 3.50 | 20.5 | 0.85 |
| GPT-4o | 6.75 | — | — |
| SIRA | 0.50 | **88.0** | **0.47** |
| **RLCracker** | **98.5** | **100.** | **0.92** |

**RLCracker vs SIRA debate (central):** SIRA's ICML 2025 claim (~100% ASR, $0.88/M tokens) uses a **weaker fidelity gate**. RLCracker shows SIRA **destroys semantics** on long text: high Rem., near-zero ESR. RLCracker is the **semantic-preserving** worst-case reference.

**Cross-scheme ESR (Qwen2.5-3B, 1500 tokens, Table 1 excerpt):**

| Scheme | ESR |
|--------|-----|
| Unigram | **98.5** |
| KGW | 78.0 |
| EWD | 71.5 |
| SWEET | 66.5 |
| PF-Watermark | 77.8 |
| KGW_selfhash | 58.0 |

**Hardest targets:** PF and Unigram at 500 tokens still see 76.8% / 67.0% ESR (Qwen3-0.6B) — distortion-free schemes resist more but do not survive RL.

**Sample efficiency (Table 3):** 50 pairs → 82.5% ESR on EWD (Qwen3-0.6B); gains plateau at **100 pairs**.

**OOD generalization (Table 2):** Policy trained on Llama-3.1-8B watermarks transfers to Qwen2.5-32B outputs at **96–98% ESR** on EWD.

**Prompt/reasoning ablations:** System prompt alone lifts Base ESR ~15 pp; Think (chain-of-thought paraphrase) adds ~40 pp on long KGW_selfhash. RLCracker bakes both in via RL.

**Impact statement:** Authors position RLCracker as **diagnostic stress-test** for designers; warn of misuse; recommend responsible access controls.

---

## 3. RLSpoofer — watermark spoofing

### 3.1 One-line contribution

Introduce **local capacity bottleneck** (token-level probability mass reallocatable under KL-bounded semantic-preserving updates) and **RLSpoofer**, a GRPO attack that shifts human text paraphrases **toward** \(P_{wm}\) and away from \(P_h\) — forging watermark detection on unwatermarked content.

### 3.2 Threat model (dual of RLCracker)

| Dimension | Specification |
|-----------|---------------|
| **Objective** | Paraphrase **human** text so detector flags it watermarked |
| **Training pairs** | (human text \(X\), watermarked rewrite \(X'_{wm}\) from victim LLM) |
| **Success (SSR)** | Spoof success rate: semantically faithful + detector triggered |
| **Knowledge** | Black-box; no key, no detector API |

Surrogate objective: \(\max_\theta D_{\mathrm{KL}}(P_\theta \| P_h) - D_{\mathrm{KL}}(P_\theta \| P_{wm})\) — **sign flip** vs RLCracker.

### 3.3 Method sketch

1. **Local capacity mass** \(c_t = 1 - \max_x P_h(x \mid h_t)\): positions with low human-token concentration allow more redistribution → capacity-aware token reward \(r_t = c_t \log \frac{P_{wm}}{P_h}\).
2. **Sequence reward:** conservative min(P-SP vs human, P-SP vs watermarked rewrite).
3. **CE anchor:** cross-entropy to watermarked reference stabilizes optimization (removing anchor drops SSR 23–36 pp).
4. **Reference approximations:** same lightweight \(\pi_{\mathrm{ref}}\) — human path conditions on \(X\), watermark path on \(X'_{wm}\).

### 3.4 Experimental setup

| Component | Detail |
|-----------|--------|
| **Victim** | Llama-3.1-8B-Instruct (watermarked rewrites) |
| **Attackers** | Qwen3-0.6B / 1.7B / 4B, Qwen2.5-3B-Instruct, Llama-3.2-3B |
| **Watermarks (6)** | EWD, SWEET, KGW, Unigram, PF-Watermark, PMark |
| **Length** | 500 tokens (train + test) |
| **Training** | **100** human–watermarked pairs per scheme (C4-RealNewslike) |
| **Baselines** | Distill (10k pairs), DITTO, DPO |

### 3.5 Headline results

**Qwen3-4B SSR (Table 1):**

| Scheme | Distill (10k) | RLSpoofer (100) |
|--------|---------------|-----------------|
| EWD | 51.3 | **56.5** |
| SWEET | 45.5 | **52.3** |
| KGW | 56.3 | **58.0** |
| Unigram | 26.0 | **54.8** |
| **PF** | **6.00** | **62.0** |
| PMark | 23.3 | **36.3** |

**Key finding:** Logit-based schemes (EWD/SWEET/KGW) were already spoofable by Distill at 10k pairs. **PF distortion-free** resisted all baselines (<9% SR) until RLSpoofer — **62% SSR** breaks the "distortion-free = spoof-resistant" narrative at modest sample cost.

**Cross-watermark transfer (Table 17):** EWD ↔ SWEET ~50% SSR zero-shot; PF → EWD 52.5% but PF → SWEET 0.25% — asymmetric vulnerability overlap.

**Limitations (authors, C.9):** Optimizes **surrogate** not true detector objective; sensitive to reference model and reward weights; no detector-agnostic guarantee.

**Release policy:** Code withheld during review; conditional post-acceptance release with misuse mitigation — unlike RLCracker's public repo.

---

## 4. Attack landscape — where RL-C/S sit

### 4.1 Removal attacks compared

| Method | Train data | Detector access | Long-form (≥500 tok) | Semantic gate | Code |
|--------|------------|-----------------|----------------------|---------------|------|
| DIPPER | — | No | Poor (Table 1: 4.5% Unigram @1500) | Moderate | Open |
| GPT-4o | — | No | Poor (6.75% Unigram @1500) | Moderate | API |
| SIRA | — | No | High Rem., **low ESR** | Weak (P-SP 0.47) | Open |
| B⁴ | ~100k pairs | No | Strong (NAACL) | Constrained opt. | Check repo |
| WaterPark Dipper | — | No | DP-40 → TPR collapse | N/A | [WaterPark](https://github.com/JACKPURCELL/WaterPark) |
| **RLCracker** | **100 pairs** | **No** | **98.5% ESR @1500 Unigram** | **P-SP > 0.7** | **Open** |

### 4.2 Spoofing attacks compared

| Method | Train data | PF-Watermark SSR (Qwen3-4B) |
|--------|------------|----------------------------|
| Distill | 10,000 | 6.0% |
| DITTO | 10,000 | 3.5% |
| DPO | prefs | 5.25% |
| **RLSpoofer** | **100** | **62.0%** |

### 4.3 WaterPark / MarkLLM gap

WaterPark (Agent #20) attack catalog: DIPPER, ChatGPT paraphrase, GBDA, typo/swap — **no GRPO adaptive policies**. RL-C/S belong in a **post-WaterPark tier** alongside SIRA and Adversarial Paraphrasing (Agent #25). Recommended synthesis action (Agent #97–100): add RLCracker as attack #13 in WaterPark fork or cite as external worst-case bound.

---

## 5. Supporters, critics, and open debate

### 5.1 Supporters (watermark pessimists / red-teamers)

- **Adaptive eval is necessary:** Fixed DIPPER/GPT prompts **overstate** robustness; SysP + Think ablations alone reach 60–90% ESR without RL — average-case benchmarks are misleading.
- **Sample efficiency matters for policy:** 100-pair RL beats 10k-pair distillation (RLSpoofer) and 100k-pair B⁴ (RLCracker narrative) — lowers bar for real adversaries.
- **Dual-metric discipline:** ESR/SSR with P-SP exposes SIRA-style **semantic destruction** attacks that inflate raw removal rates.
- **Designer utility:** \(\rho^\*\) correlates with removal — watermark authors can pre-compute certificates without running full RL.
- **Regulatory realism:** EU Art. 50 (Aug 2026) assumes machine-readable marks; RL-C/S show **both directions** of failure (strip + forge).

### 5.2 Critics and caveats

| Objection | Detail |
|-----------|--------|
| **Surrogate ≠ detector** | Both methods optimize reference-model KL proxies; true black-box detector success is indirect (RLSpoofer admits this explicitly). |
| **MarkLLM default settings** | All evals use toolkit defaults — production SynthID/KGW params may differ (same WaterPark critique). |
| **Victim model scope** | Llama-3.1-8B / Qwen2.5 victims; no multi-vendor production API sweep. |
| **SIRA metric dispute** | SIRA authors optimize different success definition; community has not fully reconciled Rem. vs ESR reporting. |
| **PF still hardest on removal** | RLCracker PF ESR ~62–78% vs Unigram 98.5% — distortion-free not solved but heavily degraded. |
| **Compute for RL training** | 4× A100 × 1.5 h per scheme — not free, though cheap vs 100k-sample distillation cost. |
| **Spoofing ≠ humanizer threat** | RLSpoofer forges marks on human text; unslop users typically start from AI text (removal direction). Different misuse profile. |
| **Code asymmetry** | RLSpoofer withheld — reproducibility lag vs RLCracker. |

### 5.3 Synthesis

The debate is no longer "can paraphrase remove watermarks?" (settled: yes, WaterPark 2025). It is **"how little data and how much fidelity preservation?"** RLCracker answers: **100 pairs, P-SP 0.92, 1500 tokens**. RLSpoofer adds: **spoofing is also sample-efficient**, especially breaking PF resistance. Watermarking survives only in **multilayer** deployments (statistical mark + C2PA + independent detector + rate limits on queries) — aligns with Agent #79 and OpenAI's 2024 decision not to ship a 99.9% watermark.

---

## 6. Relation to unslop stack

### 6.1 What unslop does vs RL-C/S

| | unslop | RLCracker | RLSpoofer |
|---|--------|-----------|-----------|
| **Target signal** | AI-isms, detector features, voice | Watermark z-score / green-list stats | Forge watermark stats |
| **Mechanism** | Regex + optional LLM ladder | GRPO policy fine-tune | GRPO policy fine-tune |
| **Train cost** | None (inference-only) | 100 pairs + GPU hours | 100 pairs + GPU hours |
| **Intent** | Sound human | Red-team removal | Red-team spoofing |

unslop **does not** implement KL watermark rewards. But **any** semantic-preserving rewrite — including unslop's paraphrase ladder — moves text in the same **direction as RLCracker** (toward human-like token statistics). Magnitude is unknown without running RLCracker adapter on unslop outputs; expect **weaker** than dedicated RL but **non-zero** (WaterPark DP-40 already shows paraphrase halving SynthID TPR).

### 6.2 StealthRL parallel (Agent #26)

StealthRL optimizes **detector ensemble** evasion with GRPO; RL-C/S optimize **watermark distributional** evasion/spoofing. Same algorithm family (GRPO + small LoRA/full FT), different reward. A **combined adversary** (StealthRL + RLCracker) is plausible but unpublished — upper bound on dual-use humanizer research.

### 6.3 README / SKILL.md updates (recommended)

| Priority | Action |
|----------|--------|
| **P2** | Extend landscape paragraph: cite RLCracker ICML 2026 alongside SIRA — "100-sample RL removes marks with P-SP 0.92 on 1500-token Unigram" |
| **P2** | Note spoofing axis (RLSpoofer): human text can be marked falsely — relevant to **detector** false positives, not unslop core |
| **P3** | Cross-link Agent #20 WaterPark, #71 SIRA, #74 KGW, #75 SynthID, #77 side-effect ethics |
| **Do not** | Add `--watermark-strip` or RL-C/S integration to `humanize.py` |

---

## 7. unslop ethics note

### 7.1 Side-effect alignment (already in SKILL.md)

From `skills/unslop/SKILL.md`:

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real.

RLCracker **proves the side effect can be optimized to near-completion** with 100 training pairs. RLSpoofer proves the **inverse** — marks can be forged. Together they undermine **watermark-only provenance** for compliance.

### 7.2 Policy boundaries (non-negotiable)

1. **No watermark-stripping mode.** Do not add prompts, flags, or docs targeting KGW/SynthID/PF removal. RL-C/S are **citations for honesty**, not feature specs.
2. **Anti-detector ≠ anti-watermark.** Anti-detector mode = ESL/resume false-positive defense. It must not be marketed as Art. 50 circumvention.
3. **Provenance ordering.** Docs: **watermark after unslop**, not before. RLCracker shows pre-generation marks won't survive optimized paraphrase; RLSpoofer shows post-hoc marking of human text isn't trivially safe either.
4. **Research citation discipline.** Cite RLCracker ESR (semantic-gated), not SIRA Rem. alone, when arguing long-form watermark fragility.
5. **No RL attack weights in product.** Same boundary as StealthRL (Agent #26) — dual-use GRPO checkpoints stay out of the plugin.

### 7.3 Regulatory context (Aug 2026)

- **EU AI Act Art. 50** — transparency marking in force; Code of Practice prohibits deliberate watermark removal.
- **RL-C/S implication for compliance officers:** Query-limited, multilayer provenance required; humanizer tools in supply chain are **provenance risk** even when users don't intend stripping.
- **unslop positioning:** Defensive humanization + explicit misconduct boundary. Cite RL-C/S to **warn**, not to enable.

### 7.4 Bench integration (optional)

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P3** | Add RLCracker numbers to `docs/research/SYNTHESIS.md` | Strongest semantic-preserving removal cite |
| **Do not** | Watermark-removal fixtures in `detector_bench.py` | Legal/scope boundary |
| **P2** | Anti-detector exhaustion copy: note rewrite may affect embedded provenance | Informed consent |

---

## 8. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| RLCracker train pairs | 100 × 500 tok | §5.1 |
| RLCracker headline ESR | **98.5%** Unigram @1500 tok | Table 5 |
| RLCracker P-SP @ headline | 0.92 | Table 5 |
| GPT-4o ESR same setting | 6.75% | Table 1 / 5 |
| SIRA ESR / Rem. / P-SP | 0.5% / 88% / 0.47 | Table 5 |
| RLSpoofer PF SSR | **62.0%** (100 pairs) | Table 1 / 3 |
| Distill PF SSR (10k) | 6.0% | Table 3 |
| Schemes tested | 10 (RLC) / 6 (RLS) | §5.1 / §4.1 |
| ESR semantic threshold | P-SP > 0.7 | §5.1 |
| \(\rho^\*\) vs removal correlation | Pearson −0.77 | §5.2 / Table 12 |
| RLSpoofer code | Withheld pre-acceptance | Appendix C.10 |

---

## 9. Open questions

1. **Will RLSpoofer code release?** Acceptance + responsible-release policy pending.
2. **WaterPark + RLCracker replication?** Unified harness would settle production-scheme numbers.
3. **RLCracker on SynthID production params?** MarkLLM defaults may under/over-state vs Google deployment.
4. **Combined StealthRL + RLCracker?** Unpublished dual evasion (detector + watermark).
5. **Defense:** Watermark robust RL training (adversarial min-max) — no mature open implementation as of Aug 2026.
6. **Metric reconciliation with SIRA authors** — community standard for semantic-gated ASR vs raw Rem.

---

## 10. Cross-references (sibling agents)

| Agent | Relevance |
|-------|-----------|
| #20 WaterPark | Dipper paraphrase baseline; no RL attacks in catalog |
| #26 StealthRL | GRPO paraphrase vs detectors — parallel method family |
| #71 SIRA | Removal baseline; ESR debate |
| #72 BIRA | Bias inversion attack — complementary watermark threat |
| #74 KGW | Primary logit watermark in both papers |
| #75 SynthID | Evaluated in RLCracker (MarkLLM); long-form ESR in appendix tables |
| #77 Watermark side-effect ethics | Direct policy companion |
| #79 C2PA vs statistical | Multilayer response to RL-C/S |
| #76 EU AI Act Art. 50 | Regulatory frame |

---

## 11. Citations

```bibtex
@inproceedings{huang2026rlcracker,
  title={{RLCracker}: Evaluating the Worst-Case Vulnerability of {LLM} Watermarks with Adaptive {RL} Attacks},
  author={Huang, Hanbo and Zhang, Yiran and Zheng, Hao and Gong, Xuan and Li, Yihan and Liu, Lin and Liang, Shiyu},
  booktitle={International Conference on Machine Learning (ICML)},
  year={2026},
  eprint={2509.20924},
  archivePrefix={arXiv},
  primaryClass={cs.CR},
  url={https://arxiv.org/abs/2509.20924}
}

@article{huang2026rlspoofer,
  title={{RLSpoofer}: A Lightweight Evaluator for {LLM} Watermark Spoofing Resilience},
  author={Huang, Hanbo and Gong, Xuan and Zhang, Yiran and Zheng, Hao and Liang, Shiyu},
  journal={arXiv preprint arXiv:2604.11546},
  year={2026},
  url={https://arxiv.org/abs/2604.11546}
}

@inproceedings{huang2025b4,
  title={B4: A Black-Box Scrubbing Attack on {LLM} Watermarks},
  author={Huang, Baizhou and Pu, Xiao and Wan, Xiaojun},
  booktitle={NAACL},
  pages={9113--9126},
  year={2025},
  url={https://aclanthology.org/2025.naacl-long.460/}
}

@inproceedings{cheng2025sira,
  title={Revealing Weaknesses in Text Watermarking through Self-Information Rewrite Attacks},
  author={Cheng, Yiming and others},
  booktitle={ICML},
  year={2025},
  eprint={2505.05190},
  archivePrefix={arXiv}
}

@inproceedings{liang2025waterpark,
  title={Watermark under Fire: A Robustness Evaluation of {LLM} Watermarking},
  author={Liang, Jiacheng and Wang, Zian and Hong, Spencer and Ji, Shouling and Wang, Ting},
  booktitle={Findings of EMNLP},
  year={2025},
  url={https://arxiv.org/abs/2411.13425}
}
```

---

## 12. Primary URLs

| Resource | URL |
|----------|-----|
| RLCracker arXiv | https://arxiv.org/abs/2509.20924 |
| RLCracker HTML v2 | https://arxiv.org/html/2509.20924v2 |
| RLCracker GitHub | https://github.com/OTTO-OTO/RLCracker |
| ICML 2026 poster | https://icml.cc/virtual/2026/poster/63933 |
| RLSpoofer arXiv | https://arxiv.org/abs/2604.11546 |
| RLSpoofer HTML | https://arxiv.org/html/2604.11546 |
| MarkLLM toolkit | https://github.com/THU-BPM/MarkLLM |
| B⁴ (prior scrubber) | https://arxiv.org/abs/2411.01222 |
| SIRA | https://arxiv.org/abs/2505.05190 |
| WaterPark | https://github.com/JACKPURCELL/WaterPark |
