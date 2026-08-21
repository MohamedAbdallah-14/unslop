# Agent #31 — DIPPER Paraphrase Attack

**Topic:** DIPPER (Discourse Paraphraser) as the canonical AI-text evasion attack  
**Paper:** Krishna et al., *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense*, NeurIPS 2023  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Krishna et al. trained **DIPPER** — an **11B-parameter T5-XXL** seq2seq model fine-tuned on **6.3M discourse-level paraphrase pairs** — to stress-test 2023-era AI-text detectors. Two inference knobs control attack intensity: **lexical diversity (L)** and **order diversity (O)**, each on a 0–100 scale in multiples of 20. At the paper's standard setting **L=60, O=60**, a single DIPPER pass on GPT-2-XL open-ended generations drops **DetectGPT true-positive rate from 70.3% → 4.6%** at **1% FPR**, while P-SP semantic similarity stays **0.94** (above the 0.76 human-paraphrase median).

DIPPER is the **de-facto baseline paraphrase attack** in every subsequent humanization/evasion paper. It is **not** a synonym swapper: it paraphrases **paragraph-length spans in discourse context** (prompt + surrounding sentences), iterates in **3-sentence windows**, and can **reorder sentences** — the design choice that separates it from sentence-level paraphrasers (Sadasivan's T5-222M loop, QuillBot-style tools).

The same paper proposes the strongest countermeasure: **provider-side retrieval**. Store every API generation; query candidate text against the corpus with **BM25** or **P-SP**. Paraphrase preserves semantics, so provenance survives surface rewrite. At L60/O60 on long-form QA, BM25 retrieval detects **97.8%** (GPT-2-XL), **97.3%** (OPT-13B), **96.2%** (GPT-3.5) vs DetectGPT's **7.6% / 1.5% / 0.0%**. At **15M-generation scale**, PG19 BM25 holds **97.3%** on paraphrases; Wikipedia drops to **80.4%**.

**2026 staleness warning:** DIPPER numbers target **2023 detectors** (DetectGPT, GPTZero v1-era, Kirchenbauer watermark, OpenAI classifier since shut down). TH-Bench (2025) finds DIPPER **fails to dominate** the modern Pareto — it preserves semantics but **can increase AUC on Binoculars** and struggles vs model-based detectors. Turnitin's August 2025 "AI bypasser" category explicitly trains on humanizer outputs. Treat DIPPER as the **historical floor**, not current commercial bypass performance.

**unslop analog:** DIPPER ≈ **trained, controllable, discourse-aware paraphrase**. unslop's closest operational equivalent is **anti-detector step 6: cross-model second pass** (Claude ↔ GPT ↔ Gemini) — same mechanism (different model family rewrites surface statistics) without the 11B GPU cost. Deterministic unslop passes (regex, burstiness, contractions) target **lexical L** only; they do **not** replicate discourse reordering (O) or cross-model fingerprint shift. HIP (arXiv 2605.19516) formalizes the cross-model lever DIPPER approximates with a dedicated paraphraser.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Paper (arXiv)** | https://arxiv.org/abs/2303.13408 |
| **Paper (PDF)** | https://arxiv.org/pdf/2303.13408 |
| **NeurIPS proceedings** | https://proceedings.neurips.cc/paper_files/paper/2023/hash/575c450013d0e99e4b0ecf82bd1afaa4-Abstract.html |
| **OpenReview** | https://openreview.net/forum?id=WbFhFvjjKj |
| **Official code** | https://github.com/martiansideofthemoon/ai-detection-paraphrases |
| **HuggingFace weights** | https://huggingface.co/kalpeshk2011/dipper-paraphraser-xxl |
| **Google Research mirror (T5X/Jax)** | https://github.com/google-research/google-research/tree/master/dipper |
| **Minimal inference script** | https://github.com/martiansideofthemoon/ai-detection-paraphrases/blob/main/dipper_paraphrases/paraphrase_minimal.py |
| **Retrieval defense script** | https://github.com/martiansideofthemoon/ai-detection-paraphrases/blob/main/dipper_paraphrases/detect_retrieval.py |

### Related papers (lineage)

| Paper | URL | Relation |
|-------|-----|----------|
| **Sadasivan impossibility** (arXiv 2303.11156) | https://arxiv.org/abs/2303.11156 | Concurrent; recursive sentence paraphrase; no retrieval defense |
| **DetectGPT** (Mitchell et al.) | https://arxiv.org/abs/2301.11305 | Primary victim; curvature destroyed by paraphrase |
| **Kirchenbauer watermark** | https://arxiv.org/abs/2301.10226 | Most resilient 2023 detector to DIPPER |
| **Tulchinskii PHD** (NeurIPS 2023) | https://arxiv.org/abs/2306.04723 | Rare detector that *resists* DIPPER on some generators |
| **TH-Bench** (2025) | https://arxiv.org/abs/2503.08708 · https://github.com/DrenfongWong/TH-Bench | Modern 6×13 benchmark; DIPPER is one of six attacks |
| **RAID** (ACL 2024) | https://arxiv.org/abs/2405.07940 · https://github.com/liamdugan/raid · https://raid-bench.xyz | Adversarial robustness benchmark; `paraphrase` attack split |
| **WaterPark** (EMNLP 2025 Findings) | https://arxiv.org/abs/2411.13425 · https://doi.org/10.18653/v1/2025.findings-emnlp.1148 | 10 watermarkers × 12 attacks; DIPPER as DP-l-o |
| **TempParaphraser** (EMNLP 2025) | https://github.com/HJJWorks/TempParaphraser | Post-DIPPER multi-round baseline |
| **HIP cross-model** (2026) | https://arxiv.org/abs/2605.19516 | Practitioner cross-model pass formalized |
| **DivEye** (TMLR 2026) | https://arxiv.org/abs/2509.18880 | Surprisal-variance survives paraphrase |

---

## DIPPER mechanism

### Architecture

```
Base: google/t5-v1_1-xxl (11B)
Fine-tune data: 6.3M paragraph-level paraphrase pairs
Training signal: Two English translations of French novels (The Nun, etc.)
  → sentence alignment (Needleman-Wunsch + Wieting 2019 similarity)
  → subset selection + random sentence shuffle
  → control codes (L, O) computed from overlap / Kendall-Tau
Inference: T5 conditional generation, greedy or top-p
Hardware: ≥40 GB GPU (per repo README)
```

**Name:** **D**iscourse **IPPER** (Discourse Paraphraser).

### Inference format

Paper notation:

```
lexical = L, order = O prompt <p> generated-text </p>
```

**Repo reality (two footnotes):**

1. Tags are `<sent> … </sent>` in the shipped model, not `<p>`.
2. Control codes encode **similarity**, not diversity: use **`100 − X`** for diversity X. Paper **L60-O60** → **`lex=40, order=40`** in code.

Minimal API (`paraphrase_minimal.py`):

- `lex_diversity`, `order_diversity` ∈ {0, 20, 40, 60, 80, 100}
- Long inputs: sliding window of **`sent_interval=3`** sentences; prior context kept in prefix
- Mark target span with `<sent> … </sent>`

### L and O knobs

| Knob | Training definition | Intuition |
|------|---------------------|-----------|
| **L (lexical)** | Unigram token-overlap F1 between source and target span; binned to {0,20,…,100} | L=20 ≈ 20% lexical change |
| **O (order)** | Kendall-Tau on overlapping tokens after sentence shuffle | O=60 = substantial reordering |

**Attack sweep in paper:** L ∈ {20, 40, 60}, O ∈ {0, 60}. Main headline uses **L60 + O60**.

**DetectGPT on GPT-2-XL (Wiki open-ended, 1% FPR):**

| Setting | Sim (P-SP) | Watermark | DetectGPT | GPTZero | RankGen |
|---------|------------|-----------|-----------|---------|---------|
| Clean | — | 100.0 | **70.3** | 13.9 | 13.5 |
| +20L | 99.2 | 97.1 | 28.7 | 9.1 | 15.8 |
| +40L | 98.4 | 85.8 | 15.4 | 7.3 | 18.0 |
| +60L | 96.9 | 68.9 | 8.7 | 7.1 | 19.8 |
| **+60L,60O** | **94.3** | **57.2** | **4.6** | **1.2** | 28.5 |

Lexical change drives DetectGPT collapse; adding **O=60** finishes the job (70.3→8.7→4.6). Watermark is the **most resilient** 2023 detector (still 57.2% at L60/O60).

### Discourse-level vs sentence-level

**Discourse-level (DIPPER default):**

- Trained on multi-sentence spans with **document context** (sentences before/after the paraphrase window)
- Prompt passed as prefix: `lexical = L, order = O {prompt} <sent> window </sent>`
- Supports **content reordering** within the window
- Iterates 3 sentences at a time for long generations

**Sentence-level (ablation / alternatives):**

- Non-contextual DIPPER variant (Appendix C): lower quality, worse prompt compatibility
- Sadasivan recursive T5-222M / LLaMA-2-7B-Chat: sentence-by-sentence, no diversity knobs
- QuillBot / Parrot / Pegasus: practitioner default; no L/O control

Paper §4.4: sentence-level paraphrasers **can** evade (Sadasivan) but lack fine-grained diversity control and multi-sentence support — attackers want **minimum edit** to flip a detector on long responses.

**Field consensus (Cat 17, TH-Bench):** Paragraph-scoped paraphrase is the **quality floor** for cohesion. Sentence-by-sentence humanizers underperform on discourse coherence.

---

## Attack experimental setup

| Dimension | Value |
|-----------|-------|
| **Generators** | GPT-2-XL (1.5B), OPT-13B, GPT-3.5 text-davinci-003 (175B) |
| **Tasks** | WikiText-103 open-ended (300 tokens); long-form QA (300 words) |
| **Detectors** | Kirchenbauer watermark, DetectGPT, GPTZero, OpenAI classifier, RankGen |
| **Metric** | TPR at **1% FPR** (authors argue ROC-AUC hides false-positive cost) |
| **Semantic check** | P-SP ≥ 0.76 threshold; 88–99% of paraphrases pass |
| **Attack policy** | **Single** DIPPER sample (no detector-guided resampling) |

Long-form QA DetectGPT (GPT-2-XL): **74.9% → 7.6%** at L60/O60 (OpenAI classifier: 59.2% → 32.7%).

---

## Retrieval defense

### Mechanism

1. API provider stores every `(prompt, response)` pair.
2. Candidate text `y′` embedded via **BM25** or **P-SP**.
3. Score = max similarity to corpus; flag if score > threshold T.
4. Paraphrase preserves meaning → near-duplicate retrieval still hits.

### Headline numbers (long-form QA, L60/O60, BM25, 3K corpus)

| Generator | DetectGPT (pp) | **Retrieval BM25 (pp)** |
|-----------|----------------|-------------------------|
| GPT-2-XL | 7.6% | **97.8%** |
| OPT-13B | 1.5% | **97.3%** |
| GPT-3.5 | 0.0% | **96.2%** |

**15M-scale (RankGen training corpus, 2K paraphrased subset):**

- PG19 BM25: **97.3%** detection on paraphrases at 1% FPR
- Wikipedia BM25: **80.4%** (corpus growth hurts more on wiki than PG19)
- Degradation 1M→15M on PG19: only **~1%** absolute

**Limitations (Appendix A):** Requires provider log access; FPR grows with corpus size (human text that resembles prior API output gets flagged); not available to third-party detectors (Turnitin, GPTZero); Sadasivan argues recursive paraphrase can eventually beat retrieval — Krishna disagrees when semantic preservation holds.

**unslop SKILL.md cites this correctly:** anti-detector mode is a **false-positive defense**, not durable evasion when verifier has source DB.

---

## Benchmark usage: RAID / WaterPark / TH-Bench

### RAID (ACL 2024)

- **What:** 10M+ docs, 11 LLMs, 12 adversarial attacks including **`paraphrase`**
- **DIPPER link:** RAID's `paraphrase` split is the standard robustness test; practitioners often use DIPPER or Pegasus-class models via `raid-bench` attack API
- **Repo:** `pip install raid-bench` → `generation/adversarial` → `get_attack("paraphrase")`
- **Gap:** RAID does **not** ship DIPPER weights; attack implementation is separate from Krishna repo. DIPPER headline numbers are **not** RAID leaderboard entries — different detectors, different era.
- **unslop relevance:** `benchmarks/detector_bench.py` / Desklib RAID fixtures; rule-only passes barely move TMR — consistent with DIPPER showing lexical-only edits insufficient vs modern metric detectors.

### WaterPark (EMNLP 2025 Findings)

- **What:** Unified watermark robustness platform — **10 watermarkers × 12 attacks × 8 metrics**
- **DIPPER encoding:** **`DP-l-o`** — lexical change **l%**, order change **o%** (e.g. DP-40, DP-60, DP-40-20)
- **Findings:**
  - **UPV, UB:** TPR → ~0 under DP-40 (highly vulnerable)
  - **RDF, UG:** Most robust (index-dependent / context-free designs)
  - **TGRL, SIR, GO:** Intermediate; context-dependent schemes break when token order/surface shifts
  - **SynthID-Text:** Resilience similar to TGRL baseline under paraphrase class
- **Contrast with Krishna 2023:** Watermark was *most resilient* in Krishna's DetectGPT-era eval; WaterPark shows **scheme-dependent** fracture under systematic DP sweeps.
- **Gap noted in Cat 05:** WaterPark covers **watermark** attacks, not humanizer-vs-commercial-detector — different measurement surface.

### TH-Bench (arXiv 2503.08708, 2025)

- **What:** First humanization benchmark — **6 attacks × 13 detectors × 6 datasets × 19 domains × 11 LLMs**
- **DIPPER role:** One of six attacks alongside **Recursive DIPPER**, Token Ensemble (TOBLEND), RAFT, HMGC, Prompt-based
- **Implementation:** Precomputed `clean_${model}_dipper.csv`; HF model `kalpeshk2011/dipper-paraphraser-xxl`
- **Headline TH-Bench verdict on DIPPER:**
  - **High semantic similarity**, moderate compute (11B GPU)
  - **Mixed evasion:** Strong vs some metric detectors (Log-Likelihood AUC drops) but **can increase AUC on Binoculars** vs clean text on some splits
  - **Does not win Pareto:** No attack dominates effectiveness + quality + cost
  - **Recursive DIPPER** often beats single-pass on metric detectors but **destroys** text quality (worst semantic similarity)
- **Multi-class attribution:** DIPPER + Prompt perform **better** against LM-D source attribution than in binary detection — paraphrase shifts stylistic fingerprints across models.

---

## Concurrent work: Sadasivan vs Krishna

| | **Sadasivan (2303.11156)** | **Krishna / DIPPER (2303.13408)** |
|--|---------------------------|-----------------------------------|
| **Attack** | Recursive sentence paraphrase (T5-222M, etc.) | Single-pass discourse paraphrase with L/O knobs |
| **Theory** | TV-distance bound → detection approaches random | Empirical + **retrieval defense** |
| **Defense** | Claims retrieval also defeated by enough recursion | BM25 80–97% on paraphrases at 15M scale |
| **unslop stance** | Impossibility frames regulatory debate | Retrieval caveat in SKILL.md — provenance > surface stats |

Both papers posted March 2023; Krishna explicitly contrasts in §2.

---

## unslop cross-model pass analog

### Mechanism mapping

| DIPPER capability | unslop equivalent | Gap |
|-------------------|-------------------|-----|
| Lexical diversity (L) | Regex stock-vocab scrub, `lexical_targets.py`, contractions (`soul.py`) | ✅ partial — vocabulary only |
| Order diversity (O) | `structural.py` sentence split/merge, bullet-shape breaking (anti-detector step 2) | ⚠️ weak — Tulchinskii shows O=60 barely moves PHD |
| Discourse context | Paragraph-aware LLM pass (`--llm`) | ⚠️ single-model unless user runs step 6 |
| Cross-model fingerprint | **Anti-detector step 6:** Claude ↔ GPT ↔ Gemini second pass | ✅ strongest analog; manual |
| Controllable edit budget | L/O knobs | ❌ no continuous diversity control in unslop |
| Detector feedback loop | `detector.py` TMR ladder | ⚠️ ladder historically stopped at `full`; `anti-detector` exists in code |

### Why cross-model ≈ DIPPER in practice

- DIPPER must be a **different model family** from the generator to evade watermarks (paper §3) — same reason cross-model pass works: ** shifts token-distribution fingerprint**
- HIP (2026): iterative base-model paraphrase beats commercial detectors; cross-model is the practitioner version without 11B fine-tune
- TempParaphraser (EMNLP 2025): temperature-simulation multi-round; **82.5% avg detector accuracy reduction** — formalizes what step 6 describes informally
- Internal benchmark constraint (`UPDATE-PLAN-2026-08.md`): deterministic passes move TMR **~0.0–0.2 pp**; **cross-model structural rewrite** required for consumer detector screenshots

### Recommended unslop integration

1. **Document honestly:** DIPPER 70.3→4.6% is DetectGPT@2023, not Turnitin@2026.
2. **Anti-detector step 6 is the DIPPER analog** — keep recommending it; consider `--detector-feedback` exhaustion message citing Krishna retrieval caveat.
3. **Do not ship DIPPER inference** in unslop CLI (40 GB GPU, adversarial misuse surface) — cite as research baseline.
4. **Benchmark hook:** Add optional `dipper` column to `detector_bench.py` only if HF weights available; otherwise proxy with **cross-model LLM pass** in LLM test tier.
5. **Phase 3 pipeline (UPDATE-PLAN):** MASH/HIP/TempParaphraser-inspired multi-stage + cross-model capstone = operational unslop without 11B paraphraser.
6. **Defense-aware copy:** Any anti-detector marketing must mention retrieval/provenance (Grammarly Authorship, API logging) — DIPPER's own conclusion.

---

## 2026 detector landscape vs DIPPER era

| Detector class | DIPPER-era fate (2023) | 2026 notes |
|----------------|------------------------|------------|
| DetectGPT / curvature | Collapses (70.3→4.6%) | Largely superseded by Fast-DetectGPT, Binoculars |
| GPTZero | Weak baseline even pre-paraphrase | v6 adds predictability cones; patched bypasses in days |
| Watermark (KGW) | Most resilient (100→57%) | WaterPark: scheme-dependent; SIRA ~100% removal $0.88/M tok |
| PHD / intrinsic dimension | **Improves** on some generators post-DIPPER | Rare geometry signal |
| DivEye / surprisal variance | N/A (2026) | **Survives** paraphrase — orthogonal to DIPPER |
| Turnitin | N/A | Aug 2025 "AI bypasser" category; pre-Aug bypass rates stale |
| Commercial ensemble | N/A | Chicago Booth 2026: 60–85% on humanized content |

**Bottom line:** DIPPER proved **statistical detectors are brittle to paraphrase**. It did **not** prove evasion is durable against retrieval, geometry detectors (PHD), surprisal dynamics (DivEye), or adversarially retrained commercial ensembles (DAMAGE, Turnitin bypasser).

---

## Reproduction checklist

```bash
# Clone + env (needs ~40GB GPU)
git clone https://github.com/martiansideofthemoon/ai-detection-paraphrases
pip install transformers torch sentencepiece
# Model auto-downloads from kalpeshk2011/dipper-paraphraser-xxl

# Minimal paraphrase (L60/O60 → lex=40, order=40)
python dipper_paraphrases/paraphrase_minimal.py

# Full paper replication: Google Drive benchmark bundle (see README)
python dipper_paraphrases/detect_detectgpt.py --output_file ...jsonl_pp
python dipper_paraphrases/detect_retrieval.py --technique bm25 --retrieval_corpus pooled
```

---

## Key citations

```bibtex
@inproceedings{krishna2023paraphrasing,
  title={Paraphrasing evades detectors of {AI}-generated text, but retrieval is an effective defense},
  author={Krishna, Kalpesh and Song, Yekyung and Karpinska, Marzena and Wieting, John and Iyyer, Mohit},
  booktitle={NeurIPS},
  year={2023},
  url={https://arxiv.org/abs/2303.13408}
}
```

---

## Open questions for unslop

1. **Measure unslop output under DIPPER** — does full + cross-model pass recover DetectGPT-era evasion on 2026 Binoculars/Fast-DetectGPT?
2. **PHD + DivEye under DIPPER-analog passes** — does cross-model move both ID and surprisal variance?
3. **Retrieval simulation** — can Desklib/RAID fixtures proxy provider-side defense for honest anti-detector docs?
4. **Distilled DIPPER** — GradEscape (139M) and MASH (0.1B) beat 11B on some axes; should unslop reference them instead of raw DIPPER in research docs?

---

*Agent #31 complete. Manifest row 31 → done.*
