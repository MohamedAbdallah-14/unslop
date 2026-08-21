# Agent #20 — WaterPark Watermark Benchmark

**Focus:** Paper, platform, datasets, attack catalog, headline results, debate vs prior benchmarks, unslop ethics note.  
**Date:** 2026-08-19  
**Scope:** Full web research + ACL Anthology PDF + GitHub repo + sibling agent cross-refs.

---

## 1. Executive summary

**WaterPark** is the first open-source, unified benchmark for **attack robustness** of LLM text watermarking — not just detectability or fidelity. The paper is *Watermark under Fire: A Robustness Evaluation of LLM Watermarking* (Liang et al., EMNLP 2025 Findings, Suzhou, Nov 2025; [arXiv:2411.13425](https://arxiv.org/abs/2411.13425), [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1148/)). Code: [github.com/JACKPURCELL/WaterPark](https://github.com/JACKPURCELL/WaterPark).

The platform integrates **12 watermarkers**, **12 removal attacks**, and **8 metric families** (detection, fidelity, robustness ΔTPR, quality under perturbation). It runs a full pipeline: watermark injection → adversarial removal → evaluation → optional generic RoBERTa detector training. As of the paper's May 2025 revision, it also supports next-token distribution comparison, attack-combination analysis, what-if scenarios, and gradient-based whitebox attacks.

**Headline finding:** No watermark wins on all axes. Distribution-**transform** schemes (RDF, GO) survive paraphrase and copy-paste best but sacrifice fidelity (MAUVE/P-SP). Distribution-**shift** schemes (TGRL, UG, SIR, UPV) stay close to unwatermarked quality but collapse under Dipper paraphrase, copy-paste, and combined lexical attacks. **SynthID-Text** tracks KGW/TGRL robustness — not a paraphrase silver bullet. A **single ChatGPT paraphrase round** drops all watermarkers below **30% TPR**; GBDA gradient attacks push most below **10%**.

**unslop verdict:** WaterPark is the canonical citation for why **humanization and watermarking are adversaries**. DIPPER — the same paraphraser unslop's detector research treats as the humanizer proxy — is WaterPark's primary paraphrase attack. unslop does not target watermark removal, but rewriting passes can strip statistical watermarks as a side effect. The benchmark supports unslop's **EU AI Act Art. 50 refusal** and anti-detector boundary: legitimate ESL/resume use, not provenance stripping.

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (arXiv)** | https://arxiv.org/abs/2411.13425 | Submitted Nov 2024; revised May 2025 |
| **ACL Anthology** | https://aclanthology.org/2025.findings-emnlp.1148/ | EMNLP 2025 Findings, pp. 21050–21074 |
| **DOI** | https://doi.org/10.18653/v1/2025.findings-emnlp.1148 | |
| **GitHub (WaterPark)** | https://github.com/JACKPURCELL/WaterPark | Platform + evaluation scripts |
| **Related repo (examples)** | https://github.com/JACKPURCELL/sok-llm-watermark | Referenced in README shell paths |
| **MarkLLM toolkit** | https://arxiv.org/abs/2405.10051 | Prior platform WaterPark positions against |
| **WaterBench** | https://arxiv.org/abs/2311.07138 | Effectiveness-focused prior benchmark |
| **MarkMyWords** | Piet et al. 2023 | Single-watermarker robustness study |
| **DIPPER attack source** | https://arxiv.org/abs/2303.13408 | Krishna et al. NeurIPS 2023 |
| **SynthID-Text** | https://www.nature.com/articles/s41586-024-08025-4 | Nature 2024; included in WaterPark |
| **SIRA (post-WaterPark)** | ICML 2025 | ~100% ASR on 7 schemes; not in WaterPark catalog |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | Findings of EMNLP 2025 (Suzhou, China, Nov 4–9, 2025) |
| **Authors** | Jiacheng Liang, Zian Wang, Spencer Hong, Shouling Ji, Ting Wang |
| **Affiliations** | Stony Brook University (lead), NUS, Zhejiang University |
| **Funding** | NSF 2405136, 2406572; OpenAI Researcher Access Program |
| **License** | Open-source code on GitHub; no standalone HuggingFace dataset card |

---

## 3. What WaterPark is (and is not)

### 3.1 Position in the benchmark landscape

| Benchmark / toolkit | Focus | WaterPark gap filled |
|---------------------|-------|----------------------|
| **WaterBench** (Tu et al. 2023) | Effectiveness, quality, basic robustness | No unified attack matrix or design-choice ablations |
| **MarkMyWords** (Piet et al. 2023) | KGW (TGRL) robustness deep-dive | Single scheme, not comparative |
| **MarkLLM** (Pan et al. 2024) | Toolkit: detectability + basic robustness + quality | Lacks in-depth design-choice → robustness analysis |
| **Zhao et al. 2024 survey** | Taxonomy overview | Not an executable benchmark |
| **WaterPark** | **Attack robustness** across 12 schemes × 12 attacks × 5 domains | First unified red-team testbed |

WaterPark's contribution is **systematization + execution**: it maps watermark design space (context dependency × generation strategy × detection method) and attack design space (linguistic / lexical / mixing / paraphrase / adaptive), then runs them on identical prompts, models, and metrics.

### 3.2 Platform pipeline (GitHub)

```
Prompts → LLM + watermarker → watermarked text
                ↓
         attack_pipeline.py (12 attacks)
                ↓
         evaluation_pipeline.py (8 metric families)
                ↓
    optional: generic_detector/ (RoBERTa fine-tune)
```

Shell scripts under `release_shell/` batch runs (e.g. `attack_john23.sh`, Dipper-on-C4). Supports W&B logging, gradient-based whitebox attack module, and attack-combination sweeps.

---

## 4. Watermarker catalog (Table 7)

12 schemes in the May 2025 revision; main paper Table 2 evaluates 10 + SynthID + TGRL+EWD.

| Code | Method | Context | Generation | Detection | Notes |
|------|--------|---------|------------|-----------|-------|
| **TGRL** | Kirchenbauer KGW (2023) | Text-dep. | Dist.-shift | Score | Industry default reference |
| **UG** | Unigram (Zhao et al. 2023) | Context-free | Dist.-shift | Score | Piet et al. called it "not robust" — WaterPark **refutes** under paraphrase |
| **UPV** | Liu et al. 2023a | Text-dep. | Dist.-shift | Model-based | Low clean TPR (0.40) in main table |
| **SIR** | Semantic invariant (Liu et al. 2024) | Text-dep. | Dist.-reweight | Model-based | Sensitive to paraphrase intensity |
| **RDF** | Kuditipudi et al. 2023 | Index-dep. | Dist.-transform | Score (edit) | Best overall robustness tier |
| **UB** | Unbiased (Hu et al. 2024) | Text-dep. | Dist.-reweight | Score | Typo/swap → TPR ≈ 0 |
| **DIP** | DiPmark (Wu et al. 2024) | — | Stealth embed | — | Strong lexical + mixing resilience |
| **GO** | Aaronson–Kirchner | Text-dep. | Dist.-transform | Score | Google/OpenAI lineage |
| **SynthID** | Dathathri et al. 2024 | — | Production-scale | — | Nature paper; marginal over TGRL on typo |
| **EWD** | Entropy-based (Lu et al. 2024b) | Add-on | Applied to TGRL | Score | Typo TPR 0.222→0.472 |
| **CTWL** | Wang et al. 2024b | Multi-bit | — | — | In taxonomy; limited main-table coverage |
| **MPAC** | Yoo et al. 2024 | Multi-bit | — | — | In taxonomy |

**Design axes (controlled comparisons, §4.3):**

1. **Context dependency:** UG (context-free) beats TGRL (text-dependent) on Dipper, typo, copy-paste.
2. **Generation strategy:** GO (dist.-transform) beats TGRL (dist.-shift) on copy-paste and strong paraphrase.
3. **Detection method:** UPV model-based **does not** beat score-based on paraphrase — contradicts original UPV claim.

---

## 5. Attack catalog (Table 8)

12 attacks grouped by perturbation type. Threat model: adversary has sample watermarked + non-watermarked texts, **cannot** reproduce watermarking or interact with the detector API; uses LLMs **less capable** than the target generator.

### 5.1 Attack taxonomy

| Class | Attacks | Humanizer / unslop relevance |
|-------|---------|------------------------------|
| **Linguistic variation** | Contraction, expansion, lowercasing | Minor; tokenizer edge cases |
| **Lexical editing** | Misspelling, typo, synonym (WordNet), word swap | QuillBot-class lexical edit; ESL typo patterns |
| **Text-mixing** | Copy-paste CP-n-m (n segments, m% watermarked) | Partial paste into human doc; dilution attack |
| **Paraphrasing** | DIPPER DP-l-o (lexical % l, order % o); round-trip translation (Seamless M4T) | **Primary humanizer proxy** — same tool as RAID/DAMAGE |
| **Advanced (§5.2)** | Attack intensity sweep; combined simple attacks; GBDA gradient + surrogate detector; ChatGPT iterative paraphrase | Commercial humanizer / expert-LLM threat |

### 5.2 DIPPER settings used

| Notation | Meaning |
|----------|---------|
| DP-20 | 20% lexical paraphrase |
| DP-40 | 40% lexical paraphrase |
| DP-60 | 60% lexical paraphrase |
| DP-40-20 | 40% lexical + 20% order change |
| DP-60-20 | 60% lexical + 20% order change |

Main Table 2 reports DP-20 and DP-40; Table 4 sweeps full intensity grid.

---

## 6. Datasets and experimental setting

### 6.1 Generation grid

| Axis | Values |
|------|--------|
| **LLMs** | OPT-1.3B (small), LLaMA-3-7B-Chat (medium), Qwen2.5-14B-Instruct (large) |
| **Domains** | C4 (completion), HC3 (QA), Story Completion (creative), Law Stack Exchange (legal), Paper Conclusion (academic) |
| **Prompts** | 1,000 prompts per watermarker for effectiveness eval (§E); main robustness table uses Qwen2.5-14B + Paper Conclusion |
| **Non-watermarked baseline** | Human responses (same prompts) or ChatGPT-mimic for generic-detector training |

### 6.2 Dataset sources

| Dataset | Source | Task |
|---------|--------|------|
| **C4** | Colossal Clean Crawled Corpus | Text completion |
| **HC3** | Human–ChatGPT comparison corpus | QA |
| **Story Completion** | euclaise/writingprompts (HF) | Creative writing |
| **Law Stack Exchange** | jonathanli/law-stack-exchange (HF) | Legal Q&A |
| **Paper Conclusion** | Academic summarization subset | Research prose |

Cross-model/cross-dataset analysis (Table 9) shows **algorithm design dominates** model/dataset variance for robustness ranking — justifying the single primary setting (Qwen + Paper Conclusion) for Table 2.

### 6.3 Evaluation protocol

- **Primary metric:** TPR at **FPR = 1%** (fixed threshold; ROC AUC for overall effectiveness).
- **Fidelity:** WER, BLEU, BERTScore, P-SP between original and watermarked text.
- **Robustness:** ΔTPR (and ΔAUC) before vs after attack.
- **Quality under attack:** BERTScore/P-SP between watermarked T̃ and attacked T̃′.

---

## 7. Headline results

### 7.1 Table 2 — TPR @ 1% FPR (Qwen2.5-14B, Paper Conclusion)

| Watermarker | Clean | Typo | Swap | CP1-10 | DP-40 | Trans | Tier |
|-------------|-------|------|------|--------|-------|-------|------|
| **RDF** | 0.999 | 0.979 | 0.976 | 0.872 | **0.738** | 0.978 | Robust |
| **UG** | 0.993 | 0.930 | 0.929 | 0.857 | **0.877** | 0.921 | Robust paraphrase |
| **GO** | 0.996 | 0.956 | 0.982 | 0.864 | 0.560 | 0.667 | Robust mixing |
| **DIP** | 0.978 | 0.920 | 0.889 | 0.343 | 0.781 | 0.577 | Stealth lexical |
| **SynthID** | 0.998 | 0.321 | 0.415 | 0.039 | 0.498 | 0.232 | Production; paraphrase-vulnerable |
| **TGRL** | 0.993 | 0.222 | 0.429 | 0.000 | 0.485 | 0.222 | KGW baseline |
| **TGRL+EWD** | 0.995 | 0.472 | 0.650 | 0.035 | 0.573 | 0.459 | EWD helps typo, not CP |
| **SIR** | 0.978 | 0.320 | 0.320 | 0.340 | 0.300 | 0.000 | Paraphrase-sensitive |
| **UB** | 0.980 | 0.033 | 0.000 | 0.018 | 0.103 | 0.255 | Lexical collapse |
| **UPV** | 0.400 | 0.000 | 0.080 | 0.000 | 0.080 | 0.240 | Weakest overall |

**Reading guide:**

- **Copy-paste (CP1-10):** Only 10% watermarked content remaining. TGRL, UPV, UB, SynthID → TPR ≈ 0. RDF/GO stay >0.86.
- **Paraphrase (DP-40):** UG (0.877) and RDF (0.738) lead; TGRL (0.485) and SynthID (0.498) mid; UPV/UB fail.
- **Translation (Trans):** RDF still 0.978; TGRL 0.222 — length/surface change exploits RDF edit-score sensitivity.

### 7.2 Table 4 — Dipper intensity sweep

| Watermarker | DP-20 | DP-40 | DP-60 | DP-60-20 |
|-------------|-------|-------|-------|----------|
| **RDF** | 0.988 | 0.962 | 0.840 | 0.714 |
| **UG** | 0.940 | 0.916 | 0.848 | 0.846 |
| **GO** | 0.971 | 0.847 | 0.500 | 0.378 |
| **TGRL** | 0.952 | 0.858 | 0.550 | 0.406 |
| **UB** | 0.461 | 0.149 | 0.025 | 0.009 |
| **UPV** | 0.296 | 0.057 | 0.645 | 0.742 |

UG shows the most **consistent** decay curve; UPV is erratic (model-assisted detector instability).

### 7.3 Advanced attacks

| Attack | Result | Implication |
|--------|--------|-------------|
| **Combined simple** (typo+swap, etc.) | SIR TPR < 0.3; TGRL/GO vulnerable to typo+swap combo | Benign edits compose into red-team |
| **GBDA gradient + surrogate detector** | Most watermarkers < 10% detection; RDF 42% caught by specific detector after evading generic | Adaptive attacker beats Dipper |
| **ChatGPT 1-round paraphrase** | All watermarkers TPR < 0.30 | Expert LLM outside threat model but real |
| **ChatGPT 5-round iterative** | UG/GO still drop below 0.15 | Confirms Zhang et al. 2023 worst-case trend |

### 7.4 Generic + specific detector ensemble (§5.1)

Fine-tuned RoBERTa on C4 (OPT-1.3B watermarked vs ChatGPT mimic):

| Watermarker | Generic TPR (clean) | Dipper-40: both fail rate |
|-------------|---------------------|---------------------------|
| TGRL | 0.985 | < 7% |
| RDF | 0.981 | < 7% |
| UG | 0.999 | < 7% |
| UPV | 0.997 | < 7% (generic beats specific for UPV/UB) |

**Deployment recommendation from authors:** Run watermarker-specific detector **and** generic classifier; joint miss rate stays below 7% even after Dipper-40. Caveat: adversary can use generic detector as **attack oracle** (§5.2.3).

### 7.5 Fidelity vs robustness trade-off (§4.4)

Two clusters:

1. **High fidelity, low robustness:** TGRL, UG, SIR, UPV (high MAUVE; collapse under paraphrase/mixing).
2. **High robustness, lower fidelity:** RDF, GO (strong TPR under attack; lower MAUVE/P-SP).

UB is the worst of both: low fidelity **and** lexical fragility.

---

## 8. Debate — what WaterPark confirms, contradicts, and leaves open

### 8.1 Table 1 — prior claims WaterPark refines

| Prior claim | Source | WaterPark finding | Verdict |
|-------------|--------|-------------------|---------|
| UG "not robust" (context-free flaw) | Piet et al. / MarkMyWords | UG **most resilient** to paraphrase among shift methods | **Contradicts** |
| UPV low false-positive rate | Liu et al. 2023a | UPV **more FPR-prone** than TGRL; model-based detection doesn't help paraphrase | **Partially contradicts** |
| UPV beats TGRL on rewriting | Liu et al. 2023a | Both fail GPT/Dipper paraphrase | **Contradicts** |
| RDF beats TGRL on substitution | Piet et al. | Confirmed; extends to broader lexical class | **Consistent** |
| RDF edit-score robust to insertion | Piet et al. | Robust to lexical edit but **sensitive to variable token length** (translation) | **Partially contradicts** |
| SIR resilient to paraphrase | Liu et al. 2024 | Effectiveness **decreases** with paraphrase intensity | **Contradicts** |
| UB beats TGRL on substitution | Hu et al. 2024 | Comparable on synonym; UB **worse** on paraphrase | **Mixed** |

### 8.2 Community tension (2024–2026)

**Optimists (regulatory):** EU AI Act Art. 50 (effective Aug 2026) pushes machine-readable marking; SynthID ships on Gemini at scale (~10B+ pieces marked, Jan 2026 per repo research synthesis).

**WaterPark pessimists:** Even production SynthID sits at **0.498 TPR after DP-40** in unified eval — same ballpark as KGW. Paraphrase is not an edge case; it is the default humanizer move.

**Post-WaterPark escalation:**

| Work | Claim vs WaterPark |
|------|-------------------|
| **SIRA** (ICML 2025, Agent #71) | ~100% ASR on 7 schemes, $0.88/M tokens — stronger than Dipper; not in WaterPark attack list |
| **Watermark stealing** (Jovanović et al. 2024) | $50 budget, 80% success — different threat (key recovery), cited in appendix |
| **DAMAGE Table 2** (Agent #12) | DIPPER on SynthID: 87.6% → 66.5% TPR (lighter setting than WaterPark DP-40 grid) |
| **OpenAI** (Aug 2024) | Declined to ship 99.9% watermark — user churn + trivial paraphrase circumvention |

**Synthesis:** WaterPark doesn't kill watermarking research — it **ends naive deployment**. Any system that treats watermark alone as provenance fails the WaterPark bar. Multilayer marking (SynthID + C2PA + generic detector ensemble) is the paper's constructive output.

### 8.3 Limitations (authors acknowledge)

- Training-free **pre-generation** watermarking only; no training-time or post-hoc schemes.
- Threat model excludes **stronger-than-target** paraphrasers (ChatGPT tested separately, flagged as out-of-scope).
- No **SIRA**, **Adversarial Paraphrasing** (NeurIPS 2025), or **commercial humanizers** in the 12-attack set.
- Small-N ablation per taxonomic cell — causal claims from pairwise comparisons (TGRL vs UG), not full factorial.
- Low GitHub traction (2 stars Aug 2026) — benchmark not yet community-standard like RAID.

---

## 9. unslop ethics note

### 9.1 What WaterPark means for unslop

WaterPark and unslop sit on **opposite sides of the same axis**:

| | WaterPark | unslop |
|---|-----------|--------|
| **Goal** | Measure watermark survival under attack | Remove AI-isms; sound human |
| **Primary attack** | DIPPER paraphrase | Cross-model rewrite / paraphrase ladder |
| **Success metric** | TPR @ 1% FPR (keep detecting) | Lower TMR/desklib AI probability |
| **Overlap** | Paraphrase destroys both watermark signals **and** detector features | Same rewrite pass, different intent |

From `skills/unslop/SKILL.md`:

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real.

WaterPark **quantifies** that side effect: DP-40 cuts SynthID TPR from 0.998 to 0.498; ChatGPT one-shot paraphrase drops all schemes below 0.30.

### 9.2 Policy boundaries (non-negotiable)

1. **No watermark-stripping mode.** unslop must not add features, prompts, or docs aimed at evading SynthID/KGW/C2PA provenance. Agent #29, #35, #08 all cite Art. 50 explicit refusal.
2. **Anti-detector ≠ anti-watermark.** Anti-detector mode targets **ESL false positives** and resume polish — not EU disclosure compliance or academic provenance.
3. **Honest user guidance.** If a user needs machine-readable provenance, docs should say: **watermark after unslop**, not before. WaterPark shows pre-generation marks won't survive a rewrite pass.
4. **Research citation discipline.** WaterPark supports the claim "paraphrase breaks statistical watermarks" — cite Table 2, not DAMAGE alone. Do not claim unslop "passes WaterPark" (we don't run the benchmark; we aren't a watermarker).

### 9.3 Regulatory context (Aug 2026)

- **EU AI Act Art. 50** — transparency for AI-generated text; Dec 2025 Code of Practice prohibits deliberate watermark removal.
- **WaterPark implication for compliance officers:** Ex-ante watermarking without ex-post detector ensemble fails red-team. Humanizer tools in the supply chain are a **provenance risk**, not just an academic-integrity risk.
- **unslop positioning:** Defensive humanization with explicit misconduct boundary — aligned with WaterPark's stated ethics (expose vulnerabilities to **harden** systems, not to abandon marking).

### 9.4 Bench integration (optional future)

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P3** | Cross-reference WaterPark DP-40 numbers in `docs/research/SYNTHESIS.md` | SynthID 0.498 TPR already cited via DAMAGE; add WaterPark as primary source |
| **P3** | Do **not** add watermark-removal fixtures to `detector_bench.py` | Out of scope; legal boundary |
| **P2** | Note in anti-detector exhaustion message: rewrite may affect embedded provenance marks | Informed consent, not instruction |

---

## 10. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| Watermarkers integrated | 12 (10 in abstract; 12 May 2025) | Paper §1, GitHub |
| Removal attacks | 12 + advanced combos | Table 8, §5.2 |
| Evaluation metrics | 8 families | GitHub README |
| Primary TPR operating point | @ FPR = 1% | §4.1 |
| RDF DP-40 TPR | 0.738 | Table 2 |
| UG DP-40 TPR | 0.877 | Table 2 |
| SynthID DP-40 TPR | 0.498 | Table 2 |
| TGRL CP1-10 TPR | 0.000 | Table 2 |
| ChatGPT 1-round paraphrase | All TPR < 0.30 | §5.2.4 |
| GBDA adaptive attack | Most < 10% TPR | §5.2.3 |
| Generic+specific joint miss | < 7% after Dipper-40 | §5.1 |
| EWD typo boost (TGRL) | 0.222 → 0.472 | §4.2.2 |
| DAMAGE SynthID + DIPPER (alt setting) | 87.6% → 66.5% | Agent #12 |

---

## 11. Open questions

1. **Will WaterPark become the RAID of watermarking?** Code exists; community adoption still minimal vs MarkLLM.
2. **SIRA / Adversarial Paraphrasing replication on WaterPark harness?** Strongest 2025 attacks absent from original 12.
3. **Production SynthID params vs WaterPark defaults?** Google may tune γ/δ differently; open eval may understate production resilience.
4. **Multi-bit watermarkers (CTWL, MPAC)?** In taxonomy, under-evaluated in main tables.
5. **Cross-link to RAID?** Watermark robustness and MGT detection robustness are parallel problems; no unified benchmark yet.

---

## 12. Cross-references (sibling agents)

| Agent | Relevance |
|-------|-----------|
| #12 DAMAGE | DIPPER vs SynthID; humanizers remove watermarks |
| #15 RAID | Parallel benchmark architecture; Dipper as shared attack |
| #31 DIPPER | Same paraphraser; WaterPark DP-l-o notation |
| #35 Cross-model paraphrase | Art. 50 refusal; watermark side effect |
| #71 SIRA | Post-WaterPark universal removal; not in attack set |
| #74 KGW | TGRL baseline in WaterPark |
| #75 SynthID | Production watermark; 0.498 TPR @ DP-40 |
| #77 Watermark side effect ethics | Direct unslop policy companion |
| #79 C2PA vs statistical | Multilayer provenance response to WaterPark |

---

## 13. Citations

```bibtex
@inproceedings{liang-etal-2025-watermark,
  title={Watermark under Fire: A Robustness Evaluation of {LLM} Watermarking},
  author={Liang, Jiacheng and Wang, Zian and Hong, Spencer and Ji, Shouling and Wang, Ting},
  booktitle={Findings of the Association for Computational Linguistics: EMNLP 2025},
  pages={21050--21074},
  year={2025},
  address={Suzhou, China},
  url={https://aclanthology.org/2025.findings-emnlp.1148/},
  doi={10.18653/v1/2025.findings-emnlp.1148}
}

@article{liang2024waterpark,
  title={Watermark under Fire: A Robustness Evaluation of {LLM} Watermarking},
  author={Liang, Jiacheng and Wang, Zian and Hong, Spencer and Ji, Shouling and Wang, Ting},
  journal={arXiv preprint arXiv:2411.13425},
  year={2024}
}
```

---

*Agent #20 complete. WaterPark is the red-team benchmark for watermark **robustness** — the evidence base for unslop's provenance side-effect warning and Art. 50 boundary, not a target to beat.*
