# Agent #22 — HIP (Humanization by Iterative Paraphrasing)

**Topic:** Iterative base-model paraphrase for detector evasion  
**Paper:** Xu et al., *Base Models Look Human To AI Detectors* (arXiv:2605.19516, May 2026)  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop Phase 3 / anti-detector integration

---

## Executive summary

HIP (Humanization by Iterative Paraphrasing) is a **detector-agnostic** evasion pipeline from CMU (Xu, Zhong, Raghunathan, Fang, Kolter). The paper's headline finding is empirical, not architectural: **commercial detectors (GPTZero, Pangram) classify raw base-model continuations as overwhelmingly human**, while instruction-tuned continuations from the same family score as AI. On Llama-3-8B with human-written prefixes, GPTZero assigns **96.7%** human probability to base continuations vs **30.3%** for instruct; Pangram shows **98.8%** vs **17.1%**.

HIP exploits this by (1) building AI→human rewrite pairs, (2) **minimally fine-tuning a base model** (LoRA rank 128, one epoch) into a paraphraser that maps AI-style text back toward human prose while preserving base-model "low distortion," and (3) applying that paraphraser **iteratively** (N=10 rounds in the paper) so local context drifts from AI-origin statistics toward human-like continuation behavior. On GPTZero and Pangram, HIP on Llama-3-8B traces a **stronger semantic-preservation vs evasion Pareto frontier** than the baselines the authors actually ran: Simple Paraphrase, DIPPER, SilverSpeak, and StealthRL. **MASH and TempParaphraser are cited in related work but not head-to-head baselines.**

**unslop verdict:** HIP is the strongest 2026 evidence for **cross-model + iterative plain-text paraphrase** against commercial detectors — but it requires a locally hosted base-model + LoRA stack unslop does not ship today. Phase 3 should implement **S2: HIP-inspired iterative LLM paraphrase** (1–4 rounds, cross-provider, plain `<source>/<target>` prompt) as an **optional** step after deterministic anti-detector passes and before detector feedback. Do not fine-tune LoRA inside unslop v1; approximate the mechanism with API models chosen for "base-like" statistical behavior (or a different provider than the generator). Boundaries unchanged: ESL false-positive defense and resume polish — not academic misconduct.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv abstract)** | https://arxiv.org/abs/2605.19516 |
| **Paper (HTML v1)** | https://arxiv.org/html/2605.19516v1 |
| **DOI** | https://doi.org/10.48550/arxiv.2605.19516 |
| **alphaXiv mirror** | https://www.alphaxiv.org/abs/2605.19516 |
| **HuggingFace paper page** | https://huggingface.co/papers/2605.19516 |
| **Official code (GitHub)** | https://github.com/YixuanEvenXu/humanization-by-iterative-paraphrasing |
| **LoRA adapters + data (HF collection)** | https://huggingface.co/collections/YixuanEvenXu/humanization-by-iterative-paraphrasing |

### Comparison papers (MASH, TempParaphraser, shared lineage)

| Paper | URL | Relation to HIP |
|-------|-----|-----------------|
| **MASH** (Gu et al., ACL Findings 2026) | https://arxiv.org/abs/2601.08564 · https://aclanthology.org/2026.findings-acl.1487.pdf · https://github.com/githigher/MASH | Detector-aware style humanization; cited §2, not in HIP baseline table |
| **TempParaphraser** (Huang et al., EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1607/ · https://doi.org/10.18653/v1/2025.emnlp-main.1607 · https://github.com/HJJWorks/TempParaphraser · https://huggingface.co/huangjj877/TempParaphraser | Temperature-sampling vulnerability; multi-round sentence paraphrase; cited §2 |
| **DIPPER** (Krishna et al., NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Strongest HIP baseline; 11B paraphraser |
| **StealthRL** (Ranganath & Ramesh, 2026) | https://arxiv.org/abs/2602.08934 | RL detector-evasion baseline; weak on commercial detectors in HIP eval |
| **Sadasivan impossibility** | https://arxiv.org/abs/2303.11156 | Theoretical frame: paraphrase shrinks TV distance |
| **PADBen** (paraphrase robustness bench) | https://arxiv.org/abs/2511.00416 | Iterative paraphrase as attack class |
| **DAMAGE** (humanizer audit) | https://arxiv.org/abs/2501.03437 | Commercial humanizer honesty; motivates detector-in-loop |
| **RAID / MAGE** (eval corpora) | https://arxiv.org/abs/2405.07940 · https://arxiv.org/abs/2404.09764 | HIP training/eval subsets |

**Citation note:** The correct arXiv ID is **2605.19516** (May 2026). Title on arXiv is *Base Models Look Human To AI Detectors*; the method acronym **HIP** = Humanization by Iterative Paraphrasing.

---

## HIP mechanism (three stages)

### Stage 1 — Data collection (inverse pairing)

HIP trains **AI → human**, not human → AI. For each high-quality human passage \(h_i\) from RAID/MAGE domains (abstracts, books, news, wiki, xsum, cnn, tldr, squad):

1. Filter corpus (provenance, length, dedup, text-quality screen).
2. An external AI paraphraser (GPT-5-nano in the paper) rewrites \(h_i \rightarrow a_i\) (AI-style).
3. Reject/resample pairs that fail anomaly or semantic-preservation checks (bounded retry budget K).

Result: **11,757 training pairs** \(\mathcal{D} = \{(a_i, h_i)\}\). The direction matters: the model learns to **undo** AI paraphrase back to human targets, not to produce chatty assistant prose.

### Stage 2 — Minimal fine-tuning (preserve base-model distortion)

Starting from **base** checkpoints (Llama-3, Qwen-3; 0.6B–70B), HIP applies supervised fine-tuning with **LoRA** (rank 128, one epoch, lr 5e-5, effective batch 16, seq len 2048). QLoRA for 70B. Critical design choices:

- **No chat template.** Plain continuation format:

  ```
  <source_text>
  {AI paraphrase a}
  </source_text>
  <target_text>
  {human passage h}
  </target_text>
  ```

- Loss only on the completion span (human target + closing tag).
- Goal: add paraphrase capability **without** full instruction-tuning distortion — keep outputs in the statistical regime commercial detectors already call "human."

Ablation A.4 shows **output-layer-only adaptation fails**; representation-path changes are required. Ablation A.3 shows native chat templates on instruct models produce **modest** frontier shifts — the effect is not template-dependent.

### Stage 3 — Iterative paraphrasing (build human context)

At inference, the trained \(\mathcal{M}_{\text{para}}\) rewrites input \(x^{(0)}\) for **N rounds** (N=10 default; temperature 1.0, top-p 0.95; vLLM serving):

\[
x^{(t)} = \mathcal{M}_{\text{para}}(\text{FormatAsPrompt}(x^{(t-1)}))
\]

**Why iterate?** Single-pass paraphrase leaves AI-origin local context; repeated self-conditioning progressively replaces that context with the paraphraser's preferred human-like continuation regime. Trade-off is explicit: detector human-probability rises round-over-round while GPT-5-nano semantic scores gradually fall. Qualitative example (Llama-3-8B, MAGE/xsum): GPTZero 0% → 8.2% (R1) → 20.9% (R2) → 100% (R10); Pangram 0% → 0% (R1) → 100% (R2) → 100% (R10); semantic score stays 8–9/10 through R10.

**Two intuitions from §1** (the paper's explanatory frame):

1. **Low distortion** — outputs closer to base-model continuation behavior look human to GPTZero/Pangram.
2. **Human context** — conditioning on human-like prefix text shifts continuations toward higher human scores; iterative rewriting manufactures that context inside the passage.

---

## HIP vs MASH vs TempParaphraser

All three are iterative or multi-stage paraphrase attacks. They differ in **training objective**, **detector coupling**, and **what signal they manipulate**.

| Dimension | **HIP** (2605.19516) | **MASH** (2601.08564) | **TempParaphraser** (EMNLP 2025) |
|-----------|----------------------|------------------------|----------------------------------|
| **Core idea** | Recover base-model human-likeness via minimal SFT + iteration | Style transfer: machine → human style vectors | Simulate high-temperature sampling via multi-pass normal-temp paraphrase |
| **Detector-aware training?** | **No** — explicitly detector-agnostic | **Yes** — DPO with detector confidence as implicit reward | **No** — exploits statistical detector weakness |
| **Training pipeline** | AI→human pairs + LoRA on base model | Inverse corpus → Style-SFT → DPO → inference refinement | Synthetic paraphrase data; 1B model via LLaMA-Factory |
| **Iteration** | Document-level, same paraphraser, N=10 | Sentence-level refinement (PPL-ordered) at inference | Sentence-level multi-round |
| **Model scale** | 0.6B–70B (base/instruct) | ~0.1B rewriter | 1B paraphraser |
| **Primary evaluators** | **GPTZero, Pangram** (commercial) | 5 black-box detectors, 6 datasets | Open detectors; **82.5% avg accuracy drop** claimed |
| **Semantic control** | GPT-5-nano judge 0–10 | Linguistic quality metrics + refinement gate | Quality preserved vs raw high-temp sampling |
| **Head-to-head in HIP paper?** | — | Cited only | Cited only |
| **Code** | https://github.com/YixuanEvenXu/humanization-by-iterative-paraphrasing | https://github.com/githigher/MASH | https://github.com/HJJWorks/TempParaphraser |

### Mechanistic contrast (what each method "believes" detectors measure)

- **HIP:** Detectors mostly flag **instruction-tuning artifacts** and **AI-origin local context**, not a platonic "machine text" property. Fix: move text into **base-model continuation statistics** through human-targeted paraphrase, iterated to overwrite context.

- **MASH:** Detectors respond to **style distribution shift** (semantic + statistical features). Fix: explicit style injection, then **align to detector decision boundaries** via DPO, then polish low-fluency sentences while preserving evasion.

- **TempParaphraser:** Detectors rely on **low-entropy / high-temperature-sensitive token patterns**. Fix: multiple paraphrase passes at normal temperature approximate the entropy widening of high-temperature generation **without** the quality collapse of actually raising temperature.

### Empirical positioning (no direct three-way table exists)

HIP's Fig. 4 baseline comparison is the most relevant anchor for unslop:

- **DIPPER** — only non-HIP method with a non-trivial semantic–evasion trade-off on GPTZero/Pangram; still dominated by HIP on Llama-3-8B (smaller backbone than DIPPER's 11B).
- **StealthRL** — meaningful trade-off **not** achieved on commercial detectors (despite RL optimization against open detectors).
- **Simple Paraphrase / SilverSpeak** — weak (SilverSpeak bumps Pangram slightly; negligible GPTZero effect).

MASH reports **92% average ASR** across 5 detectors — a different metric suite; authors claim +24% over strongest prior evaders. TempParaphraser reports **82.5% average detector accuracy reduction** — strong on academic/open detectors, not the same commercial panel as HIP.

**Practitioner synthesis (unslop research compendium):** MASH wins when you can **train against the target detector family** and accept a multi-stage pipeline. TempParaphraser wins as a **lightweight sentence rewriter** benchmark. HIP wins when the deployment target is **2026 commercial classifiers** and you can host a **base-model paraphraser** without detector API training loops. For API-only tools (unslop today), HIP's *mechanism* is approximated by **cross-model iterative plain paraphrase**, not by LoRA fine-tune.

---

## Who agrees, who pushes back

### Aligns with HIP / reinforces the thesis

| Actor | Position |
|-------|----------|
| **Sadasivan et al. (2023)** | Paraphrase is near-optimal TV-reduction; detectors break under rewrite — HIP is a scaled, base-model-specific instance. |
| **Krishna / DIPPER line** | Paraphrase evades detectors; retrieval defense helps detectors but recursive paraphrase breaks it — HIP iterates harder with a different training objective (human restoration vs diversity controls). |
| **Post-training artifact literature** (Casper, Singhal length bias, Sharma sycophancy, Movva Markdown preference) | Instruction tuning leaves statistical fingerprints — HIP explicitly reads detectors as post-training sensors. |
| **PADBen / TH-Bench** | Iterative paraphrase is a standard attack class; robustness requires explicit paraphrase-aware training. |
| **HIP authors → detector researchers** | Call for detectors that model **base vs instruct behavior** and **local prefix context** explicitly (diagnostic contribution). |
| **unslop UPDATE-PLAN Phase 3** | Lists HIP as primary evidence for cross-model S2 stage. |

### Partial agreement / different emphasis

| Actor | Position |
|-------|----------|
| **MASH authors** | Agree style transfer evades black-box detectors; disagree that detector-agnostic base-model recovery is enough — **DPO against detector scores** is necessary for SOTA ASR. |
| **TempParaphraser authors** | Agree multi-round paraphrase evades detectors; attribute vulnerability to **temperature/entropy statistics**, not instruction-tuning alone. |
| **DAMAGE / commercial audit line** | Agree evasion is easy; emphasize **marketing dishonesty** and need for independent measurement — HIP's GPTZero/Pangram numbers are research-credit evals, not consumer guarantees. |
| **DivEye / TSD / SurpMark (2025–2026 detection)** | New axes (surprisal variance, late-stage volatility, transitions) may survive surface paraphrase — **HIP did not evaluate** these signals; unslop already ships DivEye proxies in stylometry/surprisal. |
| **Tulchinskii PHD (NeurIPS 2023)** | Geometry-based ID can **improve** after DIPPER paraphrase — HIP's lexical/context shift may not move PHD as easily; unknown without measurement. |

### Disagrees or limits the claim

| Actor | Position |
|-------|----------|
| **Detector vendors (GPTZero, Pangram)** | Implicitly disagree with "detectors only see instruction tuning" — both funded/partnered on the study but sell general AI detection; will retrain on HIP-style outputs (HIP §5 limitation). |
| **Chakraborty et al. (ICML 2024)** | Multi-sample / account-level detection raises effective TV — single-pass HIP success does not imply undetectability at scale. |
| **HIP Appendix A.2 (OpenAI API fine-tune)** | **Negative result:** HIP on GPT-4.1-nano via OpenAI fine-tuning API does **not** achieve the open-weight trade-off — closed alignment stack may block low-distortion recovery. Bad news for "HIP via API fine-tune"; good news for unslop's cross-model prompt approximation. |
| **Nicks et al. / ICLR 2024 detector guidance** | Warn against relying on LLM-generated-text detectors — unslop `detector.py` treats TMR as signal, not gate. |
| **Academic integrity policy community** | Any evasion method is adversarial to proctoring — unslop Boundaries restrict use cases regardless of HIP efficacy. |

---

## GitHub and artifact availability

**HIP repo:** https://github.com/YixuanEvenXu/humanization-by-iterative-paraphrasing

Shipped (per README, April 2026):

- LoRA training on AI→human pairs
- Iterative inference with released adapters
- Evaluation utilities (GPT-5-nano semantic judge, GPTZero, Pangram scoring)
- Example configs: smoke test, 8B representative, 70B QLoRA

**Dependencies:** vLLM inference, standard HF training stack, commercial detector API keys for reproduction.

**HuggingFace collection:** https://huggingface.co/collections/YixuanEvenXu/humanization-by-iterative-paraphrasing — training/eval data + LoRA adapters for Llama-3 and Qwen-3 sizes.

**Maturity:** Early — ~5 GitHub stars at fetch time; CMU authorship + full artifact release is the credibility signal. Repro cost is non-trivial (~300 GPU-hours + ~$11k equivalent commercial detector eval per paper §4.1).

**TempParaphraser:** https://github.com/HJJWorks/TempParaphraser — LLaMA-Factory + vLLM; model at https://huggingface.co/huangjj877/TempParaphraser (1B, research-only license).

**MASH:** https://github.com/githigher/MASH — Python, ACL Findings 2026.

---

## unslop integration — optional LLM pipeline step (anti-detector mode)

### Current state (August 2026 codebase)

| Component | HIP relevance |
|-----------|---------------|
| `humanize.py` `anti-detector` intensity | Deterministic + single-pass LLM; prompt breaks uniform sentence shapes — **does not iterate** |
| `humanize_llm()` | One pass (+ optional audit pass at full/anti-detector) |
| `detector.feedback_loop()` | Escalates **deterministic** ladder (subtle → anti-detector + structural + soul); max 3 iterations; TMR scorer — **not** HIP-style paraphrase |
| `surprisal.py` / `stylometry.py` | Orthogonal signals HIP never measured |
| Phase 3 plan (`UPDATE-PLAN-2026-08.md`) | **`llm_pipeline.py` S2 = HIP analog** — 1–4 rounds, cross-model |

HIP is **not** wired in today. Closest operational analog in unslop docs: **cross-model second pass** (DIPPER agent memo) — same fingerprint-shift mechanism without 11B local paraphraser.

### Recommended integration architecture

Place HIP-inspired iteration as **optional Stage S2** inside a future `llm_pipeline.py`, gated by `--llm-pipeline` or `UNSLOP_HIP_ROUNDS=N` when intensity is `anti-detector`:

```
Input text
  → [existing] deterministic anti-detector (regex, structural, soul, surprisal targets)
  → [optional S1] MASH-style draft/critique/fix (3 calls)
  → [optional S2] HIP iterative paraphrase ← THIS MEMO
  → [optional S3] TempParaphraser multi-sample on flagged sentences
  → [optional S4] detector-guided span rewrite (Adversarial Paraphrasing pattern)
  → [optional S5] cross-model capstone (different provider than S2)
  → validate.py preservation + AI-ism residual check
  → [optional] detector.feedback_loop if TMR still above target
```

### S2 prompt spec (API approximation of HIP Stage 3)

Do **not** ship LoRA training in unslop. Approximate \(\mathcal{M}_{\text{para}}\) with:

1. **Cross-model rewriter** — if text was Claude-generated, S2 uses GPT or Gemini (implements "low distortion" via different post-training artifacts without target detector training).
2. **Plain HIP format** — no assistant persona; use source/target tags or minimal "rewrite toward natural human prose, preserve meaning" instruction matching §3.2.
3. **Round count 1–4** (not 10) — diminishing returns + semantic drift; CoPA agent memo: stop when TMR moves enough.
4. **Stop rules** — semantic preservation via unchanged facts/names/numbers; `validate.py` byte contract; optional TMR ≤ target from `detector.py`.

Example env surface:

```bash
UNSLOP_LLM_PIPELINE=balanced          # fast | balanced | max
UNSLOP_HIP_ROUNDS=2                   # 0 = skip S2
UNSLOP_HIP_MODEL=...                  # provider/model for paraphrase pass
python3 -m unslop.scripts.cli humanize doc.md --intensity anti-detector --llm-pipeline
```

### Why optional, not default

1. **Cost** — each HIP round is a full-document LLM call; 4 rounds × 1K words adds ~$0.10–0.40 on API pricing (UPDATE-PLAN budget table).
2. **Semantic drift** — HIP trades meaning for evasion after ~2–4 rounds on some samples; unslop preservation contract may reject output.
3. **Closed-model gap** — HIP fails on OpenAI API fine-tune path; API paraphrase approximations need empirical TMR/GPTZero bench, not paper numbers.
4. **Boundaries** — iterative evasion is powerful; keep behind explicit flag and anti-detector intensity; document ESL/resume use only in SKILL.md.
5. **Honesty** — DAMAGE gap applies; never market "HIP-powered undetectable."

### Acceptance criteria (from UPDATE-PLAN Phase 3)

- Pipeline beats legacy `humanize_llm()` by **≥5pp TMR** on ≥3 fixtures.
- Semantic score **≥0.92** (external judge or embedding similarity).
- Preservation suite **100% pass** on code/URL/heading fixtures.
- Document that commercial detector pass rates are **benchmark snapshots**, not warranties.

### Interaction with detector feedback loop

Today `feedback_loop()` re-runs deterministic humanization. After S2 exists:

- Run HIP rounds **before** feedback loop (distribution shaping first — Sadasivan-aligned).
- Use feedback loop only for **residual** AI-ism / TMR cleanup.
- If loop exhausts ladder, recommend user increase `UNSLOP_HIP_ROUNDS` or enable S5 cross-model — mirrors `detector.py` escalation docstring intent.

---

## Implementation priority for unslop

| Priority | Action |
|----------|--------|
| **P0** | Add S2 prompt template + `--hip-rounds` to Phase 3 `llm_pipeline.py` spike |
| **P0** | Bench S2 against TMR + `drafts/2026-05-detector-test/` commercial panel |
| **P1** | Measure DivEye/TSD proxies pre/post HIP rounds — test if iteration moves **all five** 2026 signals |
| **P2** | Optional local HIP backend (vLLM + HF LoRA adapter) for power users — separate extra, not core pip package |
| **P3** | Do not train custom LoRA inside unslop; point to upstream GitHub for reproducibility |

---

## Key numbers (quick reference)

| Metric | Value | Source |
|--------|-------|--------|
| Base vs instruct GPTZero (Llama-3-8B, human prefix) | 96.7% vs 30.3% human prob | Fig. 1 |
| Base vs instruct Pangram | 98.8% vs 17.1% | Fig. 1 |
| Training pairs | 11,757 | §4.1 |
| Default inference rounds | N=10 | §4.1 |
| LoRA rank | 128 | §4.1 |
| Eval set | 256 AI passages | §4.1 |
| GPU-hours (authors) | ~300 | §4.1 |
| MASH avg ASR | 92% | MASH paper |
| TempParaphraser avg detector accuracy drop | 82.5% | EMNLP 2025 |

---

## Bottom line

HIP reframes the 2026 evasion arms race: **the cheapest move is not to attack the detector but to leave the instruction-tuned statistical regime** — base models already look human to GPTZero and Pangram, and a lightly fine-tuned base paraphraser iterated 10 times pushes AI-generated sources along the same path while keeping semantic scores high through mid-rounds. MASH and TempParaphraser share the iterative paraphrase shape but optimize different levers (detector-aligned style transfer vs entropy simulation). None of the three replaces unslop's deterministic anti-AI-ism core; they sit **above** it as optional LLM stages for users who need commercial detector relief without score-gaming a single API.

For unslop: implement HIP as **cross-model iterative plain paraphrase (S2)**, optional under `anti-detector`, 1–4 rounds, stopped by preservation + TMR, benchmarked honestly, bounded by existing misuse policy.

---

*Agent #22 complete. Cross-refs: AGENT-31-DIPPER (cross-model analog), AGENT-28-COPA (prompt vs logit), AGENT-17-SADASIVAN (TV frame), AGENT-25-ADVERSARIAL-PARAPHRASING (S4 span loop), UPDATE-PLAN-2026-08 Phase 3.*
