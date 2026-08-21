# Agent #46 — Alignment Tax / Response Homogenization (RLHF/DPO ↔ Detection)

**Topic:** How preference alignment collapses output diversity, why detectors exploit it, and what that means for unslop anti-detector mode  
**Anchor papers:** Liu et al. *The Alignment Tax: Response Homogenization…* (arXiv:2603.24124, Mar 2026); HIP *Base Models Look Human To AI Detectors* (arXiv:2605.19516, May 2026)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop anti-detector / Phase 3 integration

---

## Executive summary

"Alignment tax" names two related but distinct costs of post-training:

1. **Capability tax (classic).** InstructGPT (Ouyang et al., 2022) introduced the term for small benchmark regressions paid in exchange for instruction-following gains.
2. **Homogenization tax (2026 diagnostic).** Liu (arXiv:2603.24124) shows aligned models **collapse inter-sample semantic diversity**: on TruthfulQA, **40%** of questions yield a **single semantic cluster** across 10 i.i.d. samples (Jaccard bigram clustering); **79%** under embedding cosine clustering. Base Qwen3-14B: **1.0%** SCR vs instruct **28.5%** (Wilcoxon *p* < 10⁻⁶). Stage ablation localizes the jump to **DPO**, not SFT (Base 0.0% → SFT 1.5% → DPO 4.0% SCR on the paper's ablation chain). **Decoding cannot undo it** — the tax persists at *T* = 0.3–1.5 and under nucleus sampling (Exp. 15).

Parallel stylometric literature (Reinhart PNAS 2025, Rallapalli arXiv:2604.14111, Sardinha Nature HSS Comms 2025, Abdulhai "blandification" arXiv:2603.18161) shows the same phenomenon at the **register/feature** layer: instruction-tuned chat models cluster tightly in Biber space; humans spread wide; LLM edits push text toward a shared neutral semantic basin (~**70%** stance neutralization in the Abdulhai RCT).

**HIP connection (detection flip side):** Xu et al. (2605.19516) report commercial detectors (GPTZero, Pangram) score **base-model** continuations as overwhelmingly human (**96.7% / 98.8%** human prob on Llama-3-8B) while **instruct** continuations from the same family score as AI (**30.3% / 17.1%**). Detectors are partly **post-training sensors**, not generic "machine-text" oracles. Alignment tax homogenization is the distributional mechanism; HIP is the evasion strategy that **exits the instruct statistical regime** via base-model paraphrase.

**unslop verdict:** Anti-detector mode must treat homogenization as **weight-level, not prompt-level**. Temperature, synonym swap, and single-pass "make it human" prompts cannot restore diversity that DPO removed. unslop's defensible stack: (1) **subtractive** de-slop (regex + structural + soul) to break canonical RLHF surface patterns; (2) **anti-blandification** guard (already in `humanize.py`) so humanization does not trade detection relief for semantic neutralization; (3) **cross-model / HIP-inspired iterative paraphrase** (Phase 3 S2) to shift fingerprint families; (4) **voice-match** and DivEye/TSD targets to restore intra-document variance detectors now measure. Do not market "undetectable" — homogenization is recipe-dependent (Tulu-3 DPO+RLVR: 0.5% SCR vs Zephyr DPO: 4.0%) and vendors retrain on evasion outputs.

---

## Primary sources (full URLs)

### Anchor — response homogenization as alignment tax

| Resource | URL |
|----------|-----|
| **Liu — The Alignment Tax (arXiv abstract)** | https://arxiv.org/abs/2603.24124 |
| **Liu — HTML v2** | https://arxiv.org/html/2603.24124v2 |
| **Liu — DOI** | https://doi.org/10.48550/arxiv.2603.24124 |
| **Liu — alphaXiv overview** | https://www.alphaxiv.org/overview/2603.24124 |

### HIP — base vs instruct detection (direct detection link)

| Resource | URL |
|----------|-----|
| **HIP paper (arXiv)** | https://arxiv.org/abs/2605.19516 |
| **HIP HTML** | https://arxiv.org/html/2605.19516v1 |
| **HIP code** | https://github.com/YixuanEvenXu/humanization-by-iterative-paraphrasing |
| **Agent #22 memo** | `docs/research/2026-08-detector-research/AGENT-22-HIP.md` |

### Stylistic / semantic homogenization (RLHF/DPO lineage)

| Paper | URL | Core claim |
|-------|-----|------------|
| **InstructGPT** (Ouyang et al., NeurIPS 2022) — *classic* alignment tax | https://arxiv.org/abs/2203.02155 | SFT → RM → PPO; capability tradeoffs for intent-following |
| **Reinhart et al.** (PNAS 2025) — instruction tuning ≠ human register | https://arxiv.org/abs/2410.16107 · https://doi.org/10.1073/pnas.2422455122 | Noun-heavy, dense Biber profile; **instruct > base** divergence from human dispersion |
| **Abdulhai et al.** — blandification / semantic drift | https://arxiv.org/abs/2603.18161 | ~70% stance neutralization; LLM edits shift embeddings in a **common direction** |
| **Rallapalli et al.** (Apr 2026) — chat models cluster in Biber space | https://arxiv.org/abs/2604.14111 · https://doi.org/10.48550/arxiv.2604.14111 | Genre > source; **chat variants cluster together**; prompting/decoding weak levers |
| **Sardinha et al.** (Nature HSS Comms 2025) | https://doi.org/10.1057/s41599-025-05986-3 · https://www.nature.com/articles/s41599-025-05986-3 | Humans heterogeneous; LLM outputs **tight per-model clusters** |
| **Reinhart et al.** — embedding profiling (EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1163/ | Newer models similarly variable → **machine homogenization** trend |
| **Doshi & Hauser** (*Science Advances* 2024) — collective creativity tax | https://www.science.org/doi/10.1126/sciadv.adq1636 | Individual creativity ↑, collective diversity ↓ under AI assist |
| **Kirk et al.** (2024) — RLHF reduces diversity | https://arxiv.org/abs/2310.03716 (see also COLM Singhal length paper) | Preference optimization narrows output distribution |
| **ConLL 2026 — RLHF-induced uniformity** | https://aclanthology.org/2026.conll-main.43.pdf | RLHF **constrains UID variance** across texts; SFT-like steps show similar effects |
| **Where does output diversity collapse?** (Apr 2026) | https://arxiv.org/abs/2604.16027 · https://github.com/ckarouzos/where-diversity-collapses | Collapse is **training-data/recipe embedded**; inference tricks insufficient |
| **DivPO** — diversity-preserving DPO | https://arxiv.org/abs/2501.18101 | DPO collapses diversity; DivPO mitigates |
| **Verbalized Sampling** | https://arxiv.org/abs/2510.01171 | Inference-time diversity recovery partial (~66.8% of base diversity after DPO) |
| **Mode collapse attribution** (OpenReview) | https://openreview.net/pdf?id=3pDMYjpOxk | SFT drops token diversity; **reward/DPO step collapses output diversity** on creative prompts |
| **Sadasivan impossibility** | https://arxiv.org/abs/2303.11156 | Paraphrase shrinks TV distance — homogenized sources easier to erase *and* easier to re-homogenize |

### Classic RLHF pathology (feeds homogenized "ChatGPT voice")

| Paper | URL | Homogenization link |
|-------|-----|---------------------|
| **Singhal — length correlates with RLHF reward** | https://arxiv.org/abs/2310.03716 | Verbose, uniform sentence shapes |
| **Sharma — sycophancy** | https://arxiv.org/abs/2310.13548 | Agreement-biased canonical responses |
| **Gao — reward overoptimization** | https://arxiv.org/abs/2210.10760 | Goodhart → stereotyped high-reward modes |
| **Shapira — How RLHF Amplifies Sycophancy** (Feb 2026) | https://arxiv.org/abs/2602.01002 | Closed-form amplification toward premise-matching |

---

## Mechanism — three layers of homogenization

### Layer 1: Semantic response collapse (Liu 2603.24124)

**Metric:** Single-Cluster Rate (SCR) — fraction of prompts where *N* i.i.d. samples fall in one semantic cluster.

| Finding | Number | Implication |
|---------|--------|-------------|
| TruthfulQA SCR (Jaccard, aligned) | 40% (790q) | Same answer repeated even when wrong |
| TruthfulQA SCR (embedding cosine) | 79% | Conservative primary metric understates collapse |
| Qwen3-14B base vs instruct SCR | 1.0% vs 28.5% | Alignment **causes** collapse, not scale |
| Training stage ablation | Base 0.0% → SFT 1.5% → DPO 4.0% | **DPO** is the sharp lever |
| Token entropy vs response diversity | Base 1.175 → DPO 0.776 nats; DPO retains ~66% token entropy | **Token-level surprise ≠ semantic diversity** — explains why DivEye/TSD can survive while sampling-UQ dies |
| Decoding ablation | Persists T=0.3–1.5, nucleus p=0.9 | **Not a sampling bug** — learned distribution property |
| Recipe dependence | Tulu-3 DPO+RLVR 0.5% SCR vs Zephyr DPO 4.0% | Vendor/training choices matter |
| Cross-family SCR | Qwen3-14B 28.5%, LLaMA-3.2-3B 5.5%, Mistral-7B 1.0% | Family-specific severity |

**Downstream consequence (paper's main UQ angle):** On homogenized questions, sampling-based semantic entropy → AUROC **0.500** (chance). Single-pass token entropy retains signal (~0.603 on affected subset).

**Detection read:** If a model always lands in the same semantic phrasing bucket, **surface paraphrase** that preserves meaning may stay inside the same bucket — synonym swap insufficient (aligns with GPTZero v6 predictability cones in UPDATE-PLAN).

### Layer 2: Stylistic / register collapse (Reinhart, Rallapalli, Sardinha)

| Study | Homogenization signature |
|-------|-------------------------|
| **Reinhart PNAS 2025** | Instruction-tuned models overuse nominalizations, participial clauses, phrasal coordination; **base Llama ≈ human rates**, instruct diverges |
| **Rallapalli 2604.14111** | Chat-model outputs **cluster together** in Biber space regardless of prompt/decoding; genre dominates levers |
| **Sardinha Nature 2025** | Per-model tight clusters; human Burrows' Delta clouds are broad |
| **Abdulhai 2603.18161** | LLM edits shift all essays toward a **shared embedding region** no human essay occupied |

**Instruction tuning pushes models into a shared "assistant register"** — noun-dense, analytically neutral, emotionally flattened in stance even when lexically varied.

### Layer 3: Collective / meaning collapse (Abdulhai, Doshi & Hauser)

- **~70%** increase in neutral argumentative stance under heavy LLM use (Abdulhai RCT, *N*=100).
- AI-assisted stories **cluster more** than unassisted despite higher individual creativity scores (Doshi & Hauser).
- Risk for humanizers: "sounds human to detector" may mean **"sounds like median LLM-humanized prose"** — a new homogenized basin (Sadasivan + commercial humanizer audits).

---

## HIP connection — homogenization as what detectors measure

HIP and Alignment Tax are **inverse framings of the same post-training artifact**:

| Dimension | Alignment Tax (2603.24124) | HIP (2605.19516) |
|-----------|---------------------------|------------------|
| **Question** | Why do aligned models give the same answer repeatedly? | Why do detectors flag instruct but not base? |
| **Mechanism** | DPO compresses **inter-sample** semantic diversity | Instruction tuning imprints **detectable continuation statistics** |
| **Measurement** | SCR, clustering, token entropy decoupling | GPTZero/Pangram human probability on prefix continuations |
| **Mitigation axis** | H-DPO, DivPO, recipe design (training-time) | Base-model LoRA paraphrase + iteration (inference/training) |
| **Decoding fix?** | **No** (Exp. 15) | N/A — HIP exits instruct regime entirely |

**Synthesis chain for unslop:**

```
RLHF/DPO preference optimization
  → collapses high-reward response modes (Liu SCR)
  → concentrates Biber/register features (Reinhart, Rallapalli)
  → commercial detectors trained on instruct-tuned corpora fire (HIP Fig. 1)
  → lexical paraphrase stays in same mode (AdvPara regression on RADAR)
  → structural + cross-model + base-like paraphrase needed (unslop Phase 1–3)
```

HIP's **negative result** (OpenAI API fine-tune fails to recover base trade-off) reinforces Liu: **closed aligned stacks resist cheap un-homogenization**. unslop's API approximation (cross-provider S2) is a pragmatic hack, not guaranteed HIP equivalence.

**Head-to-head note:** Liu did not evaluate GPTZero; HIP did not measure SCR. Together they form the 2026 consensus: **detectors ≠ truth machines; they ≈ alignment-artifact sensors**.

---

## Debate — who agrees, who pushes back

### Aligns — homogenization is real, structural, partly DPO-driven

| Actor | Position |
|-------|----------|
| **Liu 2603.24124** | DPO-driven semantic SCR; decoding-independent; recipe-dependent |
| **HIP authors** | Detectors encode instruct-vs-base distinction; iterative base paraphrase evades |
| **Reinhart / Rallapalli / Sardinha** | Stylistic clustering of chat models; humans more dispersed |
| **Abdulhai et al.** | Semantic + stance homogenization from LLM editing; "blandification" |
| **karouzos 2604.16027** | Diversity collapse embedded at training; not fixable at inference alone |
| **DivPO / Verbalized Sampling authors** | DPO mode collapse documented; mitigations partial |
| **unslop UPDATE-PLAN** | Alignment Tax **4/5 relevance** — "justifies subtractive humanization" |
| **Detector vendors (implicitly)** | Retrain on humanizers / paraphrase — bet that homogenization fingerprints persist |

### Partial agreement — different emphasis or scope

| Actor | Position |
|-------|----------|
| **InstructGPT authors** | "Alignment tax" originally meant **NLP benchmark regressions**, not diversity — term overloaded in 2026 |
| **ConLL 2026 uniformity paper** | RLHF reduces **UID variance** but doesn't validate "more uniform = more human-like" — homogenization ≠ UID optimization |
| **OpenReview mode-collapse paper** | Attributes **output** collapse more to reward/DPO than token-level SFT effects — partially overlaps Liu, different experimental frame |
| **Verbalized Sampling** | **Inference-time** diversity recovery possible (~30% diversity vs ~11% direct prompt post-DPO on Tulu-3 poem task) — doesn't contradict Liu on **single-answer** factual QA |
| **Process supervision (Lightman PRM)** | **Negative alignment tax** in math reasoning — homogenization is not universal across tasks/objectives |
| **MASH / StealthRL line** | Can **re-target** homogenization toward detector decision boundaries — different optimization than un-slop |

### Pushes back or limits the claim

| Actor | Position |
|-------|----------|
| **"Just raise temperature" camp** | Liu Exp. 15: SCR still **38%** at *T*=1.5 — temperature helps marginally, not structurally |
| **"Prompt for varied style" camp** | Rallapalli: prompting/decoding **weaker than model+genre**; Reinhart: instruct models miss human dispersion even when prompted |
| **Quality-first alignment advocates** | Homogenization may be **feature** (consistent, safe, on-brand assistant) not bug — unslop is explicitly reversing a product choice |
| **Sadasivan + retrieval defenses** | Paraphrase evades lexical detectors but **multi-sample / account-level** detection raises bar — homogenization helps until it doesn't |
| **Humanizer marketing** | Claims "100% human" while producing **second-order homogenization** (DAMAGE audit) — different failure mode from RLHF homogenization |
| **ESL / non-native writers** | Detectors conflate **low-variance non-native prose** with AI homogenization (Liang line) — anti-detector must not assume all flagged text is RLHF slop |

---

## Detection implications — what homogenization enables

| Detector signal | Homogenization link | Paraphrase resistance |
|-----------------|---------------------|------------------------|
| **Lexical n-gram / RADAR** | Shared stock vocab + collocations from RLHF (Reinhart word rates: tapestry, intricate >> human) | Low — AdvPara shows synonym paraphrase can **hurt** |
| **GPTZero / Pangram commercial** | Trained on instruct-tuned web scale; HIP shows base/instruct split | Medium — cross-model + iterative base paraphrase |
| **DivEye surprisal variance** | Aligned text **lower intra-doc variance** (TMLR 2026) | High — needs structural burstiness restoration |
| **TSD late-stage volatility** | Homogenized generation **settles** — AI surprisal stabilizes in 2nd half | High — unslop gap (not yet weighted) |
| **Predictability cones (GPTZero v6)** | Homogenized modes = **high-probability lexical band** | High — synonym swap stays in cone |
| **PHD / intrinsic dimension** | Tulchinskii: paraphrase can **increase** PHD — orthogonal to homogenization story | Variable |

**Key insight:** Homogenization makes text **easier to detect in aggregate** (tight clusters) but also **harder to escape with shallow rewrite** (you stay in the cluster). Effective anti-detector work must **move the text to a different region** of stylistic/semantic space — voice-match, cross-model, HIP — not just de-templatize.

---

## unslop anti-detector implications

### What unslop already gets right

| Component | Homogenization response |
|-----------|-------------------------|
| **`humanize.py` anti-detector intensity** | Explicitly breaks **uniform sentence shapes** — targets Layer 2 surface regularity |
| **ANTI-BLANDIFICATION block** | Cites arXiv:2603.18161; forbids stance/voice sand-down — fights Abdulhai semantic collapse |
| **`structural.py`** | Sentence-length variance, bullet-soup merge — burstiness vs RLHF length bias (Singhal) |
| **`soul.py` contractions** | Restores human contraction rate (~0.17/chunk human vs ~0 AI — Paneru 2026) |
| **`stylometry.py` + voice-match** | Per-user dispersion targets vs global chat centroid |
| **`surprisal.py` DivEye proxies** | Directly targets **intra-doc variance** collapse from alignment |
| **Stock vocab / hedging removal** | Strikes Reinhart-overrepresented items (tapestry, intricate, "It's important to note") |

### Gaps (homogenization-aware)

| Gap | Why it matters | Priority |
|-----|----------------|----------|
| **Anti-detector not in `detector.feedback_loop()` ladder** | Can't iteratively de-homogenize toward TMR target | P0 (UPDATE-PLAN Phase 1) |
| **`stylometric_baseline.json` missing** | Lexical target nudges inert — can't steer away from chat centroid | P0 |
| **No TSD / SurpMark weighting** | Homogenization is **temporal** (late-stage settle), not just lexical | P1 |
| **No HIP S2 iterative cross-model stage** | Only way to approximate **regime change** without local base LoRA | P1 (Phase 3) |
| **Single-pass LLM humanize** | May **re-homogenize** toward editor-model basin (Abdulhai common-direction shift) | P1 — cap rounds, cross-model |
| **No SCR-style diversity self-check** | Can't detect when rewrite collapsed to canonical phrasing | P2 research spike |

### Recommended anti-detector doctrine (update SKILL / prompts)

1. **Subtract, don't re-author.** Alignment tax is paid at training; unslop removes slop markers — it does not ask the model to "write like a human from scratch" (which triggers blandification).

2. **Preserve stance and idiosyncrasy.** Homogenization neutralizes opinions; anti-detector must not confuse "non-AI" with "inoffensive median prose."

3. **Decoding is not a humanizer.** Do not document temperature/top-p as primary anti-detector levers — Liu + karouzos contradict.

4. **Cross-model when detector feedback exhausts.** Same-family rewrite stays in same instruct cluster (Rallapalli chat clustering); HIP mechanism = **different post-training artifact**.

5. **Measure dispersion, not just TMR.** Log DivEye proxy + sentence-length CV pre/post; target **variance restoration**, not single score.

6. **Honesty about second-order homogenization.** Aggressive evasion can produce **detectable humanizer-homogenized** class (Turnitin Feb 2026 retrain). unslop Boundaries unchanged.

### Proposed pipeline (homogenization-aware)

```
Input (instruct-tuned generator artifact)
  → deterministic de-slop (regex — kill shared RLHF vocabulary)
  → structural pass (sentence-length CV ↑, merge template bullets)
  → soul / contraction pass (Paneru axis)
  → surprisal nudge (DivEye proxy ↑ if measured low)
  → [optional S2] 1–4 round cross-model plain paraphrase (HIP analog)
  → validate.py + anti-blandification residual check
  → detector.feedback_loop (include anti-detector in ladder)
  → if exhausted: recommend different provider / voice-match sample
```

### Anti-patterns (homogenization edition)

| Anti-pattern | Why it fails |
|--------------|--------------|
| Synonym-only paraphrase | Stays in predictability cone + SCR cluster |
| "Rewrite to sound human" without source fidelity | Abdulhai semantic basin shift |
| Max temperature | Liu: SCR 38% at T=1.5; quality collapse |
| Same-model second pass | Same chat centroid (Rallapalli) |
| Score-chase until TMR=0 | Sadasivan arms race; humanizer-homogenized fingerprint |
| Neutralize strong voice for "safety" | Trades detection for blandification — ESL false-positive adjacency |

---

## Key numbers (quick reference)

| Metric | Value | Source |
|--------|-------|--------|
| TruthfulQA SCR (Jaccard, aligned) | 40% | Liu 2603.24124 |
| TruthfulQA SCR (embedding) | 79% | Liu Exp. 12 |
| Qwen3-14B base vs instruct SCR | 1.0% vs 28.5% | Liu Exp. 13 |
| DPO stage SCR ablation | 4.0% (vs SFT 1.5%, base 0.0%) | Liu Exp. 16 |
| GPTZero base vs instruct (Llama-3-8B) | 96.7% vs 30.3% human prob | HIP Fig. 1 |
| Pangram base vs instruct | 98.8% vs 17.1% | HIP Fig. 1 |
| Stance neutralization (heavy LLM use) | ~70% increase | Abdulhai 2603.18161 |
| Nominalization rate GPT-4o vs human | 2.1× (d=1.23) | Reinhart PNAS 2025 |
| VS diversity retained post-DPO vs direct prompt | ~66.8% vs ~23.8% of base | Verbalized Sampling 2510.01171 |
| Tulu-3 vs Zephyr SCR | 0.5% vs 4.0% | Liu Exp. 18 |

---

## Implementation priority for unslop

| Priority | Action |
|----------|--------|
| **P0** | Wire `anti-detector` into `detector.feedback_loop()` — homogenization recovery needs multi-pass |
| **P0** | Ship `stylometric_baseline.json` — steer away from chat-model Biber centroid |
| **P0** | Cite Liu 2603.24124 + HIP 2605.19516 together in SKILL.md anti-detector rationale |
| **P1** | Bench pre/post **sentence-length CV + DivEye proxy** on detector-test fixtures |
| **P1** | Phase 3 S2 cross-model iteration — explicit "regime change" step |
| **P2** | TSD second-half weighting — target late-stage volatility decay |
| **P2** | SCR-inspired self-check spike (embedding cluster count on multi-sample rewrite — research only) |

---

## Bottom line

RLHF/DPO does not merely make models "helpful" — it **compresses the space of things they say** at both semantic (Liu SCR) and stylistic (Reinhart/Rallapalli) levels. Decoding tricks cannot reopen that space. Commercial detectors partially measure this compression (HIP base/instruct split), which is why unslop's anti-detector path is **subtractive variance restoration + optional cross-model regime change**, not polish or synonym swap.

Alignment tax and HIP are the same coin: **training narrows; detection reads the narrow band; serious evasion exits the band.** unslop should humanize without pushing users into a **second** homogenized basin — the anti-blandification rule is load-bearing.

---

*Agent #46 complete. Cross-refs: AGENT-22-HIP (base/instruct detection), AGENT-25-ADVERSARIAL-PARAPHRASING (lexical regression), AGENT-17-SADASIVAN (paraphrase bounds), AGENT-42-RALLAPALLI (pending — Biber clustering), UPDATE-PLAN-2026-08 (Alignment Tax row), `docs/research/02-rlhf-and-alignment/A-academic.md`.*
