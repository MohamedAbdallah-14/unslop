# Agent #71 — SIRA Universal Watermark Removal

**Focus:** Paper, attack mechanism, benchmarks, debate vs prior work, unslop ethics note.  
**Date:** 2026-08-19  
**Scope:** ICML 2025 proceedings + arXiv HTML + GitHub repo + sibling agent cross-refs (WaterPark #20, Sadasivan #17, DIPPER #31).

---

## 1. Executive summary

**SIRA** (Self-Information Rewrite Attack) is a black-box paraphrasing attack that strips statistical watermarks from LLM text by targeting high–self-information tokens — the same positions where KGW-family schemes embed green-list bias. The paper is *Revealing Weaknesses in Text Watermarking Through Self-Information Rewrite Attacks* (Cheng et al., **ICML 2025**, PMLR 267:9982–10009; [arXiv:2505.05190](https://arxiv.org/abs/2505.05190)). Code: [github.com/Allencheng97/Self-information-Rewrite-Attack](https://github.com/Allencheng97/Self-information-Rewrite-Attack).

**Headline finding:** SIRA-Large (Llama-3 70B Instruct) achieves **100% or near-100% attack success rate (ASR)** on all seven tested watermarking schemes under a strict black-box threat model — no access to watermark algorithm, secret key, or detector. Cost: **$0.88 per million tokens** (SIRA-Small on AWS Bedrock). Even SIRA-Tiny (Llama-3 3B) beats DIPPER-2 on every scheme in the main C4 table. The attack is training-free, model-agnostic, and runs on consumer-grade hardware (~7 GB VRAM for Tiny).

**Mechanism in one sentence:** Compute per-token self-information with an attack LM → mask tokens above the ε-percentile threshold → paraphrase the original into a reference text → fill-in-the-blank reconstruct the masked template using the reference, destroying green-list statistics while preserving semantics.

**unslop verdict:** SIRA is the strongest open citation for why **watermarking is provenance metadata, not proof** — and why any humanizer rewrite pass can accidentally strip embedded marks. unslop does not implement SIRA and must not add watermark-removal features (EU AI Act Art. 50). The paper supports the existing Boundaries language in `skills/unslop/SKILL.md`: users who need provenance should **watermark after unslop**, not before. SIRA also explains why OpenAI withheld its 99.9% internal ChatGPT watermark (AGENT-70): paraphrase circumvention is now commodity-cheap, not a lab-only threat.

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (arXiv)** | https://arxiv.org/abs/2505.05190 | v2 HTML; submitted May 2025 |
| **ICML 2025 proceedings** | https://proceedings.mlr.press/v267/cheng25c.html | PMLR 267, pp. 9982–10009 |
| **OpenReview** | https://openreview.net/forum?id=fE3kgW7kMp | ICML 2025 poster; CC BY 4.0 |
| **DOI** | https://doi.org/10.48550/arxiv.2505.05190 | |
| **GitHub (official)** | https://github.com/Allencheng97/Self-information-Rewrite-Attack | ICML 2025 release |
| **Author PDF (UBC)** | https://www.cs.ubc.ca/~lsigal/Publications/cheng2025icml.pdf | Camera-ready |
| **KGW watermark (baseline)** | https://arxiv.org/abs/2301.10226 | Kirchenbauer et al. 2023 |
| **DIPPER (primary baseline)** | https://arxiv.org/abs/2303.13408 | Krishna et al. NeurIPS 2023 |
| **WaterPark benchmark** | https://arxiv.org/abs/2411.13425 | SIRA **not** in attack catalog (Agent #20) |
| **Christ undetectable watermarks** | https://arxiv.org/abs/2306.09194 | COLT 2024; different threat model |
| **RLCracker (follow-up)** | https://arxiv.org/abs/2509.20924 | Uses SIRA as baseline; Sep 2025 |
| **MarkLLM toolkit** | https://arxiv.org/abs/2405.10051 | Default hyperparams for watermark eval |
| **EU AI Act Art. 50** | Dec 2025 Code of Practice | Prohibits deliberate watermark removal |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | ICML 2025 (42nd International Conference on Machine Learning); poster |
| **Authors** | Yixin Cheng, Hongcheng Guo, Yangming Li, Leonid Sigal |
| **Affiliations** | UBC (Cheng, Sigal); additional affiliations in paper header (Guo, Li) |
| **License** | CC BY 4.0 (OpenReview) |
| **Code release** | GitHub; Impact Statement frames release as robustness red-teaming |

---

## 3. Threat model and attack mechanism

### 3.1 Threat model (black-box paraphrasing)

SIRA formalizes the **model-based paraphrasing** threat class — distinct from:

| Attack class | Assumption | SIRA comparison |
|--------------|------------|-----------------|
| **Text manipulation** (delete, synonym, emoji) | Surface edits only | SIRA outperforms; Table 1 |
| **Informed / white-box** (watermark stealing, random walk with detector feedback) | Query access to watermarked LLM and/or detector | **Excluded** — different threat model; authors argue unrealistic for real adversaries |
| **Model-based paraphrasing** (DIPPER, GPT rewrite) | Watermarked text only; attack LM separate from generator | **SIRA's class** |

Formal assumptions (§3.1):

- Attacker knows **neither** watermark algorithm `W`, secret key `k`, **nor** detector `D`.
- Attacker has only the watermarked output `y_w` and a separate attack LM `M_attack`.
- Goal: minimize `D(W_k, P(y_w))` subject to semantic similarity ≥ ε.

This is weaker than WaterPark's threat model in one dimension (WaterPark gives the adversary paired watermarked/non-watermarked samples) but **stronger in attack sophistication** than WaterPark's default DIPPER settings.

### 3.2 Why high-entropy embedding is the vulnerability

KGW-family watermarks embed bias in **high-entropy positions** — tokens where the model is uncertain — because boosting a green token there minimally hurts quality. SIRA's insight: those positions also have **high self-information** (surprisal) under any competent LM:

```
I(y_t) = -log P(y_t | y_{0..t-1}; M_attack)
```

Watermark logit bias **reduces** self-information at green positions (probability mass shifted toward the chosen token). SIRA masks tokens whose self-information exceeds the **ε-percentile** of the sequence (default ε = 0.30), treating them as probable green-list carriers.

Self-information beats raw entropy as a mask signal (Appendix G): entropy alone misses watermark-induced probability shifts.

### 3.3 Three-step pipeline (Figure 1)

```
Watermarked text y
       │
       ├─► M_attack: compute I(y_t) per token
       │         mask tokens where I > Percentile(I, ε)
       │         → masked template y_mask
       │
       ├─► M_attack: paraphrase y → reference text y′
       │         (NOT the original — LLM shortcuts if y_mask ≈ y)
       │
       └─► M_attack: fill-in-the-blank
                 input: y_mask + y′ + instruction
                 output: y_p (de-watermarked)
                 decoding: greedy
```

**Why two generations:** Reference text alone achieves only ~64% ASR on Unigram (Table 4); fill-in-the-blank on self-information-masked template reaches ~94%. Simple paraphrase preserves n-grams that detectors still catch.

**Why placeholders, not deletion:** Placeholders preserve length/structure cues for reconstruction (§3.2).

### 3.4 SIRA model tiers

| Variant | Attack LM | VRAM (bf16) | Time/attack (~230 tok) | C4 ASR range |
|---------|-----------|-------------|------------------------|--------------|
| **SIRA-Tiny** | Llama-3 3B Instruct | ~7 GB | ~5.3 s | 75–100% |
| **SIRA-Small** | Llama-3 8B Instruct | ~18 GB | ~10.3 s | 83–100% |
| **SIRA-Large** | Llama-3 70B Instruct | ~139 GB | ~37.2 s | 98–100% |

Cost anchor (Appendix B): SIRA-Small @ AWS Bedrock = **$0.22/M tok × 2 (in+out) × 2 (two passes) = $0.88/M tokens**. GPT-4o paraphraser estimated at **$20/M tokens** (10-iteration assumption).

---

## 4. Watermark targets (seven schemes)

Evaluated on **Opt-1.3B** as watermark generator; 500 C4 prompts; 230-token generations; hyperparams from MarkLLM defaults.

| Code | Method | Family | SIRA-Large ASR |
|------|--------|--------|----------------|
| **KGW-1** | Kirchenbauer et al. 2023 (k=1 hash) | KGW / dist.-shift | **100%** |
| **Unigram** | Zhao et al. 2023 | KGW / context-free | **100%** |
| **UPV** | Liu et al. 2023 | KGW / model-based detect | **99.6%** |
| **EWD** | Lu et al. 2024 | KGW / entropy-based | **100%** |
| **DIP** | DiPmark (Wu et al. 2024) | KGW / stealth embed | **100%** |
| **SIR** | Semantic invariant (Liu et al. 2024) | KGW / semantic reweight | **98.8%** |
| **EXP** | Aaronson & Kirchner 2022 | Christ / sampling modify | **99.8%** |

**Not evaluated:** SynthID-Text, GO (Aaronson–Kirchner dist.-transform), RDF/Edit (Kuditipudi dist.-transform), CTWL, MPAC — the schemes WaterPark (#20) shows survive paraphrase best. SIRA appendix adds **Adaptive Watermark** (98.2% ASR) and **Waterfall Watermark** (90.8% ASR) on 200-sample subsets.

---

## 5. Benchmark results

### 5.1 Table 1 — Attack success rate on C4 (primary)

ASR = fraction of attacked texts classified as **non-watermarked** by the scheme's detector.

| Attack | KGW-1 | Unigram | UPV | EWD | DIP | SIR | EXP |
|--------|-------|---------|-----|-----|-----|-----|-----|
| Word delete | 22.4% | 1.6% | 6.6% | 22.8% | 57.4% | 44.0% | 9.4% |
| Synonym | 83.2% | 17.4% | 65.2% | 76.2% | 99.6% | 82.0% | 51.0% |
| GPT-4o Paraphraser | 100% | 63.9% | 71.9% | 90.8% | 99.8% | 58.8% | 72.2% |
| DIPPER-1 (lex 60) | 82.4% | 37.0% | 58.6% | 82.2% | 99.6% | 61.2% | 73.6% |
| DIPPER-2 (+order 40) | 95.8% | 45.6% | 61.8% | 89.0% | 99.8% | 63.6% | 82.2% |
| **SIRA-Tiny** | 96.4% | 87.6% | 84.4% | 97.8% | 99.8% | 75.0% | 90.6% |
| **SIRA-Small** | 100% | 93.8% | 93.0% | 100% | 99.8% | 83.4% | 93.4% |
| **SIRA-Large** | **100%** | **100%** | **99.6%** | **100%** | **100%** | **98.8%** | **99.8%** |

**Takeaways:**

- DIPPER-2 — WaterPark's primary paraphrase proxy — tops out at 95.8% on KGW-1 and **fails below 64% on SIR**. SIRA clears 75% even at Tiny scale.
- GPT-4o paraphraser hits 100% on KGW-1 but only 58.8% on SIR — untargeted rewrite leaves semantic watermarks intact.
- SIRA-Large is the first attack in the literature to near-saturate all seven schemes simultaneously under black-box constraints.

### 5.2 Threshold-adjusted detection (Figure 2 / Appendix C)

Following Liu et al. 2024 / Zhao et al. 2023, detectors' z-thresholds are tuned to hit FPR = 1% and 10% before measuring TPR on attacked text. SIRA achieves lowest TPR and best-attacker F1 in most cells — the ASR headline survives conservative threshold calibration.

### 5.3 Quality preservation (Figure 3)

- **PPL:** SIRA paraphrased output often **lower** perplexity than original watermarked text (model-based methods benefit from stronger LMs).
- **s-BERT:** Semantic similarity preserved; ablation on UPV shows ε ∈ [0.2, 0.3] balances ASR vs meaning (Table 2).
- **ChatGPT judge** (Appendix F): confirms semantic preservation vs baselines.

### 5.4 Ablations

| Experiment | Finding |
|------------|---------|
| **Self-info vs random mask** (Table 3) | Self-information masking dominates random at every mask ratio; rules out "double paraphrase alone" explanation |
| **Reference-only vs full SIRA** (Table 4) | Reference paraphrase: 64% ASR, z=3.75; full attack: 94% ASR, z=1.85 (human baseline z≈0.12) |
| **ε sweep on UPV** (Table 2) | ASR drops from 96% @ ε=0.25 to 32% @ ε=0.70; recommended ε ∈ [0.2, 0.3] |
| **OpenGen dataset** (Table 9, Appendix J) | SIRA-Small still best; DIPPER improves on OpenGen (training distribution match) but loses to SIRA |
| **Adaptive + Waterfall** (Table 10) | 98.2% and 90.8% ASR respectively — newer schemes also broken |

### 5.5 Compute comparison (Appendix B)

| Method | Time (s) | VRAM (GB) |
|--------|----------|-----------|
| GPT Paraphraser | 12.8 | N/A (API) |
| DIPPER | 14.7 | 44.56 |
| SIRA-Tiny | 5.3 | 7.06 |
| SIRA-Small | 10.3 | 18.20 |
| SIRA-Large | 37.2 | 138.60 |

SIRA-Tiny is faster than DIPPER, uses **~6× less VRAM**, and beats DIPPER on ASR.

---

## 6. Debate and positioning vs prior work

### 6.1 SIRA vs WaterPark (Agent #20)

| Dimension | WaterPark | SIRA |
|-----------|-----------|------|
| **Scope** | 12 watermarkers × 12 attacks | 7 watermarkers × 1 novel attack (+ baselines) |
| **Primary metric** | TPR @ 1% FPR (detector survival) | ASR (detector failure rate) |
| **Paraphrase attack** | DIPPER DP-l-o grid | SIRA + DIPPER + GPT-4o |
| **SynthID** | Included; DP-40 → 0.498 TPR | **Not tested** |
| **Dist.-transform (RDF, GO)** | Best paraphrase survival tier | **Not tested** |
| **SIRA in catalog?** | **No** — published after WaterPark revision |

**Synthesis:** WaterPark proved paraphrase is the default failure mode for dist.-**shift** schemes. SIRA proves an **untargeted** paraphrase (DIPPER) is suboptimal — a **targeted** self-information mask + fill-in-the-blank saturates the same family. The open question is whether distribution-**transform** schemes (WaterPark's RDF @ 0.738 TPR after DP-40, SynthID @ 0.498) resist SIRA; no public replication yet.

### 6.2 SIRA vs DIPPER (Agent #31)

DIPPER is unslop's humanizer proxy in detector research. SIRA does not replace DIPPER as a humanizer — it is a **watermark-specific** attack template. But the overlap matters:

- Both use paraphrase to break statistical signals.
- SIRA's fill-in-the-blank step is **more destructive** to green-list statistics than DIPPER's lexical/order diversity knobs.
- unslop's cross-model rewrite ladder (detector.py exhaustion message) is closer to DIPPER/GPT-paraphrase than to SIRA — but **side effects on watermarks may be SIRA-class** if the rewrite targets high-surprisal tokens implicitly.

### 6.3 SIRA vs Christ–Gunn–Zamir undetectable watermarks (Agent #17)

Christ et al. (COLT 2024) prove **cryptographically undetectable** watermarks exist under computational assumptions — watermarks indistinguishable from unwatermarked text to any efficient adversary **without the key**.

SIRA operates in the **statistical detectability** regime where KGW/EXP embed detectable green-list bias. It does not break cryptographic watermarks; it shows the **deployed** watermark stack (KGW variants, Aaronson EXP) is strip-able at scale. The regulatory implication: EU Art. 50 "marking" based on KGW-style schemes needs to assume **stripping is trivial**, not exotic.

### 6.4 SIRA vs OpenAI watermark non-release (Agent #70)

OpenAI surveyed users (Apr 2023): ~30% would use ChatGPT less if outputs were watermarked; internal watermark reported 99.9% detectability. Withheld because **paraphrase and translation bypass** it trivially. SIRA quantifies "trivial": **$0.88/M tokens**, 3B-model capable, no API access to the watermarked model. OpenAI's decision looks empirically justified.

### 6.5 Post-SIRA attacks (RLCracker, Agent #73 preview)

**RLCracker** (arXiv:2509.20924, Sep 2025) treats SIRA as a baseline, adopts ε=0.30 from the official repo, and argues SIRA/DIPPER/GPT attacks **under-estimate worst-case vulnerability on long texts (≥500 tokens)**. RL-trained adaptive attacks push ASR further. Direction of travel: SIRA is the floor, not the ceiling.

### 6.6 Author impact statement vs misuse risk

Authors frame release as **responsible disclosure** — analogous to adversarial ML tradition (Madry et al.; Wei et al. jailbreaks). Counterargument: SIRA lowers the skill floor for watermark stripping below fine-tuning DIPPER or running WaterPark. The mitigating fact for policy: **DIPPER and GPT-paraphrase already worked** on KGW; SIRA mainly closes the gap on SIR/UPV and cuts cost 20×.

### 6.7 Known limitations (paper + external)

1. **Generator model:** Opt-1.3B only — production watermarks on GPT-4/Claude/Gemini may use different entropy profiles.
2. **Missing production schemes:** No SynthID, no Google/Gemini-scale tuning.
3. **Missing dist.-transform tier:** RDF/GO — WaterPark's most paraphrase-resilient family — untested.
4. **Text length:** ~230 tokens per sample; RLCracker flags degradation questions at 500+.
5. **Multilingual:** English C4/OpenGen only.
6. **Semantic constraint:** ε threshold trades ASR vs preservation; aggressive masking can lose detail.
7. **Informed attacks excluded:** Watermark-stealing may succeed with fewer tokens when API access exists — orthogonal threat.

---

## 7. unslop ethics note

### 7.1 What SIRA means for unslop

SIRA and unslop operate on the **same surface** — rewriting token sequences — with opposite intent:

| | SIRA | unslop |
|---|------|--------|
| **Goal** | Remove watermark detectability | Remove AI-isms; sound human |
| **Target signal** | Green-list / self-information tokens | Stock vocab, surprisal uniformity, register |
| **Success metric** | ASR → detector says "human" | Lower TMR / residual AI-isms |
| **Overlap** | High-surprisal token rewrite destroys **both** watermark statistics **and** detector features | Same pass, different user intent |

From `skills/unslop/SKILL.md` (already shipped):

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real. Users who need provenance should watermark after unslop, not before.

SIRA **quantifies** that side effect for KGW-family marks at commodity cost. It is the citation backbone for the anti-detector landscape paragraph already in SKILL.md.

### 7.2 Policy boundaries (non-negotiable)

1. **No SIRA implementation.** Do not port self-information masking, fill-in-the-blank de-watering prompts, or ASR optimization into unslop Python or skills.
2. **No watermark-stripping mode.** Anti-detector targets ESL false positives and resume polish — not EU disclosure compliance or academic provenance evasion.
3. **Detector ladder boundary.** `unslop/scripts/detector.py` already refuses watermark removal at ladder exhaustion (lines 396–407); keep that language; do not cite SIRA as a recommended next step.
4. **Honest user guidance.** If user needs machine-readable provenance: generate → unslop → **then** apply watermark/markup. Pre-generation marks won't survive rewrite.
5. **Research citation discipline.** Cite SIRA for "statistical watermarks are strip-able at $0.88/M tok" — not as instruction. Pair with WaterPark (#20) for SynthID DP-40 numbers where SIRA has no data.

### 7.3 Regulatory context (Aug 2026)

- **EU AI Act Art. 50** — transparency for AI-generated content; in force August 2026.
- **Dec 2025 Code of Practice** — multilayered marking; **explicit prohibition on deliberate watermark removal**.
- **SIRA implication for compliance officers:** Ex-ante KGW watermarking without post-hoc ensemble detection fails SIRA red-team. Humanizer tools in the supply chain are a **provenance risk**, not just an academic-integrity risk.
- **California SB 243** (Jan 2026) — companion-chatbot safety; commercial "100% undetectable" marketing faces exposure (see Agent #63, #67).

### 7.4 Relationship to anti-detector mode

Anti-detector mode (`/unslop anti-detector`) is documented for **defensive** use: ESL false positives, resume writers, legitimate AI-assisted drafts. SIRA does not expand that remit. If a user's goal is stripping SynthID/KGW for misconduct, unslop refuses — same as Art. 50 boundary in Agents #35, #38, #08.

The **technical irony:** anti-detector rewriting may produce SIRA-like side effects on embedded watermarks even when watermark removal isn't the user's goal. Disclosure > prohibition theater: SKILL.md already warns; no additional feature needed.

### 7.5 Bench integration (optional future)

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P2** | Keep SIRA in SKILL.md landscape + Boundaries | Already present; verify numbers match Table 1 |
| **P3** | Cross-link in `docs/research/SYNTHESIS.md` | "$0.88/M tok" claim needs ICML primary source |
| **P3** | Do **not** add SIRA fixtures to `detector_bench.py` | Out of scope; legal boundary |
| **P4** | WaterPark + SIRA joint replication on SynthID | Research gap; neither paper alone covers full matrix |

---

## 8. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| Venue | ICML 2025, PMLR 267:9982–10009 | proceedings.mlr.press |
| Watermark schemes tested (main) | 7 (KGW-1, Unigram, UPV, EWD, DIP, SIR, EXP) | §4.1 |
| C4 prompts | 500 | §4.1 |
| Generation length | ~230 tokens | §4.1 |
| Watermark generator | Opt-1.3B | §4.1 |
| Default ε threshold | 0.30 (30th percentile) | §4.1 |
| SIRA-Large max ASR | 100% on 5/7 schemes; 98.8–99.8% on SIR/UPV | Table 1 |
| SIRA-Tiny vs DIPPER-2 (KGW-1) | 96.4% vs 95.8% | Table 1 |
| DIPPER-2 on SIR | 63.6% ASR | Table 1 |
| Cost (SIRA-Small, Bedrock) | **$0.88 / M tokens** | Appendix B |
| GPT-4o paraphrase cost estimate | $20 / M tokens | Appendix B |
| SIRA-Tiny VRAM | ~7 GB | Table 5 |
| DIPPER VRAM | ~45 GB | Table 5 |
| Reference-only ASR (Unigram) | 64% | Table 4 |
| Full SIRA ASR (Unigram) | 94% | Table 4 |
| Adaptive Watermark ASR (SIRA-Small) | 98.2% | Table 10 |
| Waterfall Watermark ASR (SIRA-Small) | 90.8% | Table 10 |

---

## 9. Open questions

1. **SIRA on SynthID?** No published replication. WaterPark DP-40 → 0.498 TPR; SIRA may or may not saturate — highest-impact missing experiment.
2. **SIRA on dist.-transform (RDF, GO)?** WaterPark's robust tier; SIRA's self-information heuristic may fail if watermark isn't logit-bias-based.
3. **SIRA × WaterPark harness?** Agent #20 flagged this; would unify 2024–2025 attack catalogs.
4. **Long-text ASR?** RLCracker claims SIRA underestimates at ≥500 tokens; verify independently.
5. **Production-scale generators?** Opt-1.3B → GPT-4/Claude watermark survival unknown.
6. **Does unslop's deterministic pass approximate SIRA?** No self-information mask today; stylometry/surprisal modules (`surprisal.py`, `stylometry.py`) are detection-side, not attack-side — but worth monitoring for accidental convergence.
7. **Regulatory response?** Will EU Code of Practice reference academic stripping attacks, or assume marking = compliance?

---

## 10. Cross-references (sibling agents)

| Agent | Relevance |
|-------|-----------|
| #17 Sadasivan | Paraphrase impossibility; Christ undetectable watermarks vs SIRA empirical strip |
| #20 WaterPark | Parallel benchmark; DIPPER baseline; SynthID/RDF gaps SIRA shares |
| #31 DIPPER | Primary paraphrase baseline SIRA beats |
| #35 Cross-model paraphrase | Art. 50 refusal; watermark side effect |
| #70 OpenAI classifier shutdown | Why 99.9% watermark wasn't shipped; SIRA validates paraphrase bypass |
| #73 RLCracker | Post-SIRA adaptive attacks; SIRA as floor baseline |
| #74 KGW | Primary watermark family SIRA saturates |
| #75 SynthID | Production watermark **not** in SIRA eval — critical gap |
| #76 EU AI Act Art. 50 | Legal prohibition unslop cites |
| #77 Watermark side effect ethics | Direct policy companion |
| #79 C2PA vs statistical | Multilayer provenance response to SIRA-class attacks |

---

## 11. Citations

```bibtex
@inproceedings{cheng2025sira,
  title={Revealing Weaknesses in Text Watermarking Through Self-Information Rewrite Attacks},
  author={Cheng, Yixin and Guo, Hongcheng and Li, Yangming and Sigal, Leonid},
  booktitle={Proceedings of the 42nd International Conference on Machine Learning},
  pages={9982--10009},
  volume={267},
  year={2025},
  publisher={PMLR},
  url={https://proceedings.mlr.press/v267/cheng25c.html}
}
```

```bibtex
@article{kirchenbauer2023watermark,
  title={A Watermark for Large Language Models},
  author={Kirchenbauer, John and Geiping, Jonas and Wen, Yuxin and Katz, Jonathan and Miers, Ian and Goldstein, Tom},
  journal={arXiv preprint arXiv:2301.10226},
  year={2023}
}
```

```bibtex
@inproceedings{krishna2023dipper,
  title={Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense},
  author={Krishna, Kalpesh and Song, Yixiao and Karpinska, Marzena and Wieting, John and Iyyer, Mohit},
  booktitle={NeurIPS 2023},
  year={2023}
}
```

---

**Status:** Complete — ready for manifest update (#71 → complete) and synthesis pass (Agents 81–84 Cat 05 Detection).
