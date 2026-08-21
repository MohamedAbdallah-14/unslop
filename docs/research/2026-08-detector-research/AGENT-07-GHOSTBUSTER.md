# Agent #07 — Ghostbuster Deep Research

**Focus:** Ghostbuster (NAACL 2024): feature-based multi-weak-LM detector, benchmarks, paraphrase robustness, community reception, unslop `detector.py` comparison.  
**Date:** 2026-08-19  
**Scope:** Full internet research + read of `unslop/scripts/detector.py`.

---

## Executive summary

**Ghostbuster** (Verma, Fleisig, Tomlin, Klein — UC Berkeley; [NAACL 2024](https://aclanthology.org/2024.naacl-long.95/); arXiv [2305.15047](https://arxiv.org/abs/2305.15047)) is a **feature-engineering detector**, not a fine-tuned neural classifier. It runs each document through a **bank of weaker language models** (unigram, trigram, GPT-3 `ada`, GPT-3 `davinci`), performs a **structured search** over vector/scalar combinations of their token probabilities, and trains a **logistic regression** head on the selected features. Crucially, it does **not** need token probabilities from the **target** generator — so it works on black-box ChatGPT/Claude output.

Headline numbers from the paper: **99.0 F1** in-domain across three custom domains (student essays, news, creative writing); **97.0 F1** averaged out-of-domain; **+7.5 F1** cross-domain vs GPTZero; **+2.1 F1** cross-prompt; **+4.4 F1** cross-model; **92.2 F1** on Claude-generated text without Claude training data. It beats DetectGPT by **23.7 F1** on average and GPTZero by **5.9 F1**.

The design thesis: perplexity-only is too brittle (worse than random on some OOD domains); RoBERTa-large is too expressive (up to **21.3 F1** catastrophic OOD drop). Ghostbuster takes the **middle path** — more capacity than a single threshold, less overfitting than a large transformer.

**Critical gaps for unslop:** Ghostbuster is **not on the RAID leaderboard** (RAID ACL 2024 benchmarks 12 other detectors; Ghostbuster is cited but not evaluated). Its paraphrase tests use **PEGASUS** (`tuner007/pegasus_paraphrase`) and **Undetectable.ai** — not DIPPER, cross-model paraphrase, TempParaphraser, or Adversarial Paraphrasing. **SilverSpeak** homoglyphs collapse Ghostbuster's MCC from **0.64 to −0.01** (Creo & Pudasaini 2025). Inference requires **OpenAI API calls** for ada/davinci logprobs — incompatible with unslop's offline, lazy-import `detector.py` design.

**unslop uses TMR** (`Oxidane/tmr-ai-text-detector`, 125M RoBERTa, 99.28% RAID AUROC) — a **supervised text classifier** in the same family as Ghostbuster's RoBERTa baseline, but RAID-adversarial-trained. Ghostbuster occupies a **different detection family** (multi-LM probability features + linear head). **Recommendation:** keep TMR as the live feedback-loop default; add Ghostbuster only as an **offline academic benchmark** in `benchmarks/` if OpenAI API access is acceptable. Do **not** integrate into `detector.py` without a dedicated `--detector ghostbuster` opt-in that documents API dependency, cost, and privacy (inputs are sent to OpenAI per the repo README).

---

## Primary URLs

| Resource | URL |
|----------|-----|
| **Paper (ACL Anthology / NAACL 2024)** | https://aclanthology.org/2024.naacl-long.95/ |
| **Paper (PDF)** | https://aclanthology.org/2024.naacl-long.95.pdf |
| **Paper (arXiv)** | https://arxiv.org/abs/2305.15047 |
| **DOI** | https://doi.org/10.18653/v1/2024.naacl-long.95 |
| **Official GitHub** | https://github.com/vivek3141/ghostbuster |
| **Datasets (HF/GitHub)** | https://github.com/vivek3141/ghostbuster-data |
| **Live demo** | https://ghostbuster.app |
| **Human baseline experiment** | https://ghostbuster.app/experiment |
| **BAIR blog post** | https://bair.berkeley.edu/blog/2023/11/14/ghostbuster/ |
| **unslop detector module** | `unslop/scripts/detector.py` |
| **unslop TMR model** | https://huggingface.co/Oxidane/tmr-ai-text-detector |
| **RAID benchmark** | https://raid-bench.xyz/ |

### Authors and venue

| Field | Value |
|-------|-------|
| **Venue** | NAACL 2024 — *not* ACL 2024. Long papers, Volume 1, pages 1702–1717, Mexico City |
| **Authors** | Vivek Verma, Eve Fleisig, Nicholas Tomlin, Dan Klein |
| **Affiliation** | Computer Science Division, UC Berkeley |
| **First posted** | arXiv May 2023; camera-ready NAACL June 2024 |
| **Funding** | Open Philanthropy, DARPA SemaFor, Bakar Spark |
| **License** | GitHub lists **"Other"** (not MIT). Check repo before redistribution |

---

## Mechanism

### Three-stage pipeline

```
Document → [unigram, trigram, ada, davinci] token log-probs
         → structured search over feature combinations (depth ≤ 3)
         → logistic regression (L2, C=1) + 7 handcrafted features
         → P(AI-generated)
```

**Stage 1 — Probability vectors:** Each token position gets log-probabilities under four models. Unigram/trigram are Kneser-Ney smoothed on the Brown Corpus, vocabulary aligned to GPT-3 tokenizer.

**Stage 2 — Structured feature search:** A combinatorial search over vector functions (`+`, `−`, `×`, `÷`, `>`, comparisons across model pairs) and scalar functions (`max`, `min`, `avg`, `avg-top25`, `len`). Forward feature selection picks the best subset per domain. At depth 3: **2,534** candidate features; depth 2: **322**. Example selected features (Figure 5 in paper):

- `avg(ada > davinci / trigram)`
- `var(trigram > davinci)`
- `max(ada / unigram + ada)`

**Stage 3 — Classifier:** Logistic regression on selected features plus handcrafted heuristics (outlier token counts, top-25 probability gaps between ada/davinci, average word length in tokens). Interpretable, low capacity — deliberately avoids full neural overfitting.

### Design rationale (from paper + BAIR blog)

| Approach | In-domain | OOD problem |
|----------|-----------|-------------|
| **Perplexity-only (davinci)** | 81.5 F1 | 49.0 F1 creative writing OOD; **worse than random** on some non-native English |
| **DetectGPT (GPT-2 XL scorer)** | 57.4 F1 | Fails when scorer ≠ generator; unsuitable for ChatGPT/Claude |
| **GPTZero (commercial)** | 93.1 F1 | Static across domains (unsupervised); oracle-thresholded in paper |
| **RoBERTa-large + logreg head** | 98.1 F1 | **71.4 F1** student essays OOD; catastrophic domain shift |
| **Ghostbuster (full)** | **99.0 F1** | **97.0 F1** averaged OOD; best except creative-writing OOD (95.3 F1) |

Ghostbuster's insight: AI text sits on a **different point of the multi-model likelihood manifold** than human text. ChatGPT documents are more predictable under weak LMs, with the gap **widening toward document end** (entropy-rate analysis, Figure 6). A linear classifier over **ratios and variances** across models captures this without memorizing surface n-grams.

### Black-box property

Unlike DetectGPT/Fast-DetectGPT/Binoculars, Ghostbuster never queries the **source** LLM. It only needs probabilities from **fixed weaker models** (ada, davinci via OpenAI API at training and inference time). This makes it applicable when the generator is ChatGPT, Claude, or an unknown API — as long as the text's statistical signature differs from human text under the weak-LM bank.

**Caveat:** Weak models are **GPT-3 era** (ada, davinci). As frontier models improve and human/AI perplexity gaps narrow, the ada/davinci feature space may stale — no 2025–2026 refresh paper exists.

---

## Benchmarks and datasets

### Ghostbuster's own benchmarks (released)

Three paired human/AI datasets, **7,000 documents each**, training on gpt-3.5-turbo:

| Domain | Human source | Median words (human / ChatGPT) | Split |
|--------|-------------|-------------------------------|-------|
| **Student essays** | IvyPanda | 529 / 559 | 1k train+val+test same-prompt; 4k generalization prompts |
| **News** | Reuters 50-50 | 498 / 510 | Headline generated by ChatGPT, then article from headline |
| **Creative writing** | r/WritingPrompts (pre-Nov 2022) | 455 / 512 | Ground-truth prompts available |

Evaluation extras (held out from training):

- **5 prompt variants** per domain (high-school style, short sentences, casual "Hi! I'm trying to write…", etc.)
- **Claude-generated** parallel corpus
- **Non-native English:** TOEFL-11 (1k), Lang8 (1k), Liang et al. 91 TOEFL essays

Data + precomputed ada/davinci logprobs: `vivek3141/ghostbuster-data`. Old dataset pre-Nov 14 2023 at commit `604d85c`.

### In-domain results (Table 2, F1)

| Model | All domains | News | Creative | Student |
|-------|------------|------|----------|---------|
| Perplexity-only | 81.5 | 82.2 | 84.1 | 92.1 |
| DetectGPT | 57.4 | 56.6 | 48.2 | 67.3 |
| GPTZero | 93.1 | 91.5 | 93.1 | 83.9 |
| RoBERTa-large | 98.1 | 99.4 | 97.6 | 97.4 |
| **Ghostbuster** | **99.0** | **99.5** | **98.4** | **99.5** |

### Out-of-domain results (train 2 domains, test 1)

| Model | Avg OOD | vs GPTZero margin |
|-------|---------|-------------------|
| Ghostbuster | **97.0** | +7.5 F1 |
| RoBERTa | 83.2 | — |
| GPTZero | 89.5 | — |
| DetectGPT | 57.4 | — |

### Generalization (Table 3)

| Condition | Ghostbuster | RoBERTa | GPTZero | DetectGPT |
|-----------|------------|---------|---------|-----------|
| Prompt variants | **99.5** | 97.4 | 96.1 | 70.8 |
| Claude text | **92.2** | 87.8 | 75.6 | 64.2 |
| TOEFL-11 (acc) | 95.5 | 98.6 | 99.2 | 98.6 |
| Lang8 (acc) | 95.5 | 98.6 | 99.2 | 98.6 |
| Liang 91 TOEFL (acc) | **74.7** | 96.7 | 92.3 | 63.7 |

**Human baseline:** Annotators achieve **58.1 ± 11.1%** accuracy (max 82%, min 39.7%) on 50-doc sets — task is hard for humans.

### What Ghostbuster was NOT evaluated on

| Benchmark | Status |
|-----------|--------|
| **RAID** (ACL 2024, 6M+ samples, 11 attacks) | **Not included** in RAID's 12-detector panel (RoBERTa×4, RADAR, GLTR, Binoculars, Fast-DetectGPT, LLMDet, GPTZero, Originality, Winston, ZeroGPT) |
| **MAGE / MGTBench / M4** | Not reported in Ghostbuster paper |
| **Adversarial Paraphrasing** (NeurIPS 2025) | **Not evaluated** — AdvPara tests 8 detectors; Ghostbuster absent |
| **DIPPER paraphrase** (NeurIPS 2023) | Not tested (Ghostbuster uses PEGASUS, a weaker paraphraser) |
| **TempParaphraser** (EMNLP 2025) | Not tested |
| **Modern models** (GPT-4o, Claude 3.5, Gemini 2.5, Llama 3) | Only gpt-3.5-turbo (train) + Claude (eval) |

Ghostbuster's 99 F1 numbers are **real but narrow** — three English prose domains, gpt-3.5-turbo era, document-level classification, no RAID-style adversarial suite.

---

## Strengths

1. **Black-box without target-model access.** Works when you can't get ChatGPT/Claude logits — the normal deployment case.

2. **Strong cross-domain generalization for its era.** +7.5 F1 OOD vs GPTZero; beats RoBERTa OOD by 13.8 F1 on average. Linear head + multi-LM features generalize better than a fine-tuned transformer on domain shift.

3. **Prompt-robust.** 99.5 F1 across five stylistic prompt variants including "write like a high-school student" — directly relevant to evasion-via-prompting.

4. **Interpretable features.** Selected features are human-readable ratios of model probabilities — useful for research, not just deployment.

5. **Released artifacts.** Code, three benchmark datasets, precomputed logprobs, live demo, human evaluation interface. High reproducibility *if* you have OpenAI API access.

6. **Honest ethics section.** Paper and README explicitly warn against automated student penalization; list failure modes (short text, ESL, paraphrased AI, non-English).

7. **Middle-capacity sweet spot.** Ablations show structured search is **crucial** (+15–22 F1 vs handcrafted-only); ada+davinci neural LM probs are **essential** for OOD (+10–28 F1 vs n-gram only).

8. **Academic reference standard.** Cited as evaluation target in HMGC, RAFT, TH-Bench, and unslop's own research compendium (`docs/research/05-ai-text-detection-and-evasion/`). ~186 GitHub stars; stable citation count.

---

## Weaknesses

1. **OpenAI API dependency at inference.** `classify.py` requires `--openai_key`; all inputs go to OpenAI API. README warns inputs are saved internally. **No offline path** after feature-cache generation. Conflicts with unslop's offline-first detector design.

2. **Stale weak-LM bank.** ada and davinci are legacy GPT-3 models. No published update for GPT-4-era generators or open-weight Llama/Mistral as weak scorers.

3. **Short-text unreliability.** Paper: "unreliable for documents with ≤ 100 tokens." Liang 91 TOEFL essays (median 104 words) → **74.7%** accuracy. Paragraph-level detection explicitly deferred to future work.

4. **Paraphrase vulnerability (moderate, not solved).** See next section — better than DetectGPT/GLTR on light edits, worse than ideal against dedicated evaders.

5. **Homoglyph collapse.** SilverSpeak (2025): Ghostbuster MCC **0.64 → −0.01** — detector becomes random or inverted. Trivial character substitution breaks subword tokenization that probability features depend on.

6. **Not RAID-hardened.** RAID shows detectors drop 36+ points on synonym swap, repetition-penalty decoding, unseen models. Ghostbuster never ran this suite — its 99 F1 is not comparable to TMR's 99.28% RAID AUROC.

7. **Heavy setup for reproduction.** README: symbolic feature generation takes **hours**; Python 3.10 + pickled artifacts; conda env recommended. 8 open GitHub issues (incl. HuggingFace Llama access for some experiment configs).

8. **License ambiguity.** "Other" license on GitHub — not clearly MIT/Apache. Blocks bundling into unslop PyPI wheel without legal review.

9. **Privacy / cost.** Per-document OpenAI logprob calls on ada + davinci for every classification. Not suitable for high-volume CLI humanization loops.

10. **RoBERTa can beat Ghostbuster in-domain.** 98.1 vs 99.0 F1 — the gain is in **generalization**, not peak same-domain performance. Supervised RAID-trained classifiers (TMR, Desklib) may match or exceed Ghostbuster on modern benchmarks with better deployment ergonomics.

---

## Paraphrase and evasion attacks

### Attacks tested in the Ghostbuster paper (Section 7.2)

**Local perturbations** (character/word level — Figure 3 left):

| Attack | Effect |
|--------|--------|
| Flip/add/delete characters | Smooth F1 degradation; many edits needed for evasion |
| Random space/newline | Smooth degradation |
| Capitalize/lowercase | Smooth degradation |
| Swap adjacent words | Smooth degradation |
| Synonym swap (WordNet) | Smooth degradation |

**Global perturbations** (Figure 3 right):

| Attack | Effect |
|--------|--------|
| Swap adjacent sentences | **Negligible** F1 drop |
| Swap adjacent paragraphs | **Negligible** |
| Sentence paraphrase (PEGASUS) | Degrades with **repeated** paraphrase calls |
| Paragraph paraphrase (PEGASUS) | Stronger degradation than sentence-level |

**Commercial evader:**

| Attack | Recall |
|--------|--------|
| Clean AI text | **99%** |
| Undetectable.ai (balanced, domain-specific settings) | **62%** |

Paper quote: "sites like Undetectable AI still fool our model **less than half** of the time" — framing 38% evasion as partial robustness. For unslop anti-detector mode, **62% recall means 38% escape rate** — not a gate you'd ship.

Paraphrase model: `tuner007/pegasus_paraphrase` (HuggingFace). Weaker than DIPPER-11B or cross-model LLM paraphrase.

### Attacks NOT tested but relevant to unslop

| Attack | Expected effect on Ghostbuster | Evidence |
|--------|-------------------------------|----------|
| **DIPPER** (NeurIPS 2023) | Likely strong evasion | DetectGPT 70.3% → 4.6% at 1% FPR; Ghostbuster shares probability-feature family |
| **Cross-model paraphrase** (GPT→Claude) | Unknown; likely moderate–strong | unslop `detector.py` recommends this when ladder exhausts |
| **TempParaphraser** (EMNLP 2025) | Unknown | Fast-DetectGPT 98.9% → 2.6% on HC3 |
| **Adversarial Paraphrasing** (NeurIPS 2025) | **Not evaluated** | Would likely work via transfer from RoBERTa guidance |
| **SilverSpeak homoglyphs** | **Broken** | MCC → −0.01 |
| **Recursive paraphrase** (Sadasivan) | Not tested | Theoretical upper bound on any detector |
| **"Enhance word choices to sound native"** (Liang 2023) | Partially related | Ghostbuster 74.7% on short TOEFL essays |

### Paraphrase robustness vs other detectors (qualitative)

Ghostbuster is **more robust than DetectGPT/GLTR** on light edits and single-pass PEGASUS, **less robust than RADAR** (adversarially trained paraphraser loop), and **unknown vs Binoculars/Fast-DetectGPT** on RAID attacks. Its multi-model feature space means **lexical-only humanization** (synonym swap, AI-ism removal) probably **does not evade** — but **structural paraphrase through a different model family** likely does, matching the pattern unslop already documents in `detector.py` lines 384–407.

---

## Community reception

### Academic uptake

- **NAACL 2024 long paper** — primary venue, not a workshop poster. Standard citation format in detection surveys.
- **Benchmark anchor:** Ghostbuster's three datasets reused by RAID (as comparison datasets, not RAID's main corpus), MGTBench lineage, and multiple humanization papers (RAFT, HMGC) as the detector to beat.
- **Theoretical context:** Paper cites Sadasivan impossibility but focuses on document-level full-generation setting; explicitly leaves adversarial paraphrase as "future work" — honest scope limit.
- **Successor detectors** (Binoculars ICML 2024, Fast-DetectGPT ICLR 2024, AdaDetectGPT NeurIPS 2025, RAIDAR ICLR 2024) treat Ghostbuster as the **feature-engineering branch** baseline, distinct from curvature-ratio (Binoculars) and supervised-RoBERTa (TMR/RADAR) branches.

### Practitioner / open-source

| Signal | Value (Aug 2026) |
|--------|------------------|
| GitHub stars | ~186 |
| Forks | ~26 |
| Open issues | 8 |
| License | Other (not OSI-standard) |
| Demo traffic | Public at ghostbuster.app since 2023 |
| README disclaimer | Explicit: do not auto-penalize students; paraphrased AI is a failure mode |

Community friction: Issue #12 — users blocked by HuggingFace Llama access for some replication configs. OpenAI API key required for `classify.py` blocks casual adopters.

### Industry / media

- **BAIR blog** (Nov 2023): accessible explainer, emphasizes generalization and ethics.
- **Not deployed commercially** as a product — research artifact + demo. GPTZero and Turnitin remain the consumer-facing detectors Ghostbuster compared against.
- **2025 human-detector study** ([arXiv:2501.15654](https://arxiv.org/abs/2501.15654)): cites Ghostbuster as automatic baseline; finds frequent ChatGPT users outperform many detectors — indirect critique of automated detection trust.

### unslop repo internal references

- `docs/research/05-ai-text-detection-and-evasion/A-academic.md` — canonical summary
- `docs/research/05-ai-text-detection-and-evasion/C-opensource.md` — notes README failure-mode list includes human-paraphrased AI
- `docs/research/04-natural-language-quality/SYNTHESIS.md` — "multi-model probability features beat single-LM perplexity by ~6 F1"
- `detector.py` does **not** mention Ghostbuster — TMR/Desklib only

---

## Humanization implications for unslop

### What Ghostbuster detects (signal map)

Ghostbuster is sensitive to **token-level predictability under weak LMs**, especially:

- Cross-model probability **ratios** (ada vs davinci vs n-gram)
- **Variance** structures across the document
- **End-of-document** predictability gap (ChatGPT more predictable at tail)
- Document **length** and **outlier** high-probability tokens

It is **not** primarily an AI-ism / stock-vocab detector. unslop's deterministic passes (drop "delve", cap em-dashes, structural burstiness) may **help marginally** by changing token sequences, but they do **not** directly optimize the multi-LM probability manifold Ghostbuster reads.

### Mapping unslop modes to Ghostbuster

| unslop mode / pass | Ghostbuster effect | Confidence |
|-------------------|-------------------|------------|
| **subtle/balanced** (AI-ism scrub) | Low–moderate | Synonym-level edits need volume to move F1 (paper Figure 3) |
| **full** (+ filler removal, ing-pattern) | Low–moderate | Surface lexical; doesn't re-sample token probabilities |
| **structural** (sentence split/merge) | Moderate | Sentence reorder alone negligible; splits change token boundaries |
| **soul** (contractions) | Moderate | Tokenization change (`do not` → `don't`) shifts probability vectors |
| **voice-match** | Unknown | Stylometric; may or may not align weak-LM features |
| **anti-detector** | Insufficient alone | Needs cross-model paraphrase per `detector.py` escalation |
| **surprisal-variance (DivEye)** | Orthogonal signal | DivEye targets surprisal dynamics; Ghostbuster uses raw probs — partial overlap |
| **feedback_loop (TMR)** | TMR ≠ Ghostbuster | Optimizing TMR score may not minimize Ghostbuster score |

### Anti-detector mode guidance

Ghostbuster's own README lists **"AI-generated text that has been edited or paraphrased by a human"** as a known failure case. For ESL false-positive defense (Liang 2023 use case), Ghostbuster is **worse than GPTZero on the Liang 91 TOEFL essays**: 74.7% human-only accuracy (25.3% false-positive rate) vs GPTZero's 92.3% (7.7% FP). RoBERTa hits 96.7% on the same set. The paper attributes Ghostbuster's drop largely to **short document length** (median 104 words); at comparable lengths elsewhere, OOD F1 ranges 75.6–93.1.

For unslop's stated anti-detector use case (ESL false positives): Ghostbuster is **not** an equity win. Short human text remains a problem. Length ≥ 350 words (Ghostbuster training median) is more reliable.

### What would evade Ghostbuster (ranked)

1. **Cross-model paraphrase** — different LM family rewrites token probability structure (unslop's recommended escalation)
2. **Dedicated commercial humanizer** (Undetectable.ai) — 38% evasion in paper
3. **Repeated neural paraphrase** (PEGASUS/DIPPER multi-pass)
4. **Homoglyph attacks** (SilverSpeak) — trivial but detectable to human readers
5. **Prompt-level** ("write like a confused ESL student") — partially tested; Ghostbuster still 99.5 F1 on prompt variants for **AI-generated** text, but ESL **human** text remains risky

---

## unslop integration

### Current `detector.py` design

```44:49:unslop/scripts/detector.py
DetectorName = Literal["tmr", "desklib"]
DEFAULT_DETECTOR: DetectorName = "tmr"

_MODEL_IDS = {
    "tmr": "Oxidane/tmr-ai-text-detector",
    "desklib": "desklib/ai-text-detector-v1.01",
```

| Dimension | TMR (current default) | Ghostbuster |
|-----------|----------------------|-------------|
| **Family** | Supervised RoBERTa classifier | Multi-weak-LM features + logistic regression |
| **Input** | Raw text | Raw text + OpenAI ada/davinci logprobs |
| **Output** | P(AI) ∈ [0,1] via softmax | Binary + confidence via logreg |
| **Model size** | ~125M params (~500MB) | Precomputed feature cache + tiny logreg |
| **Inference cost** | Single 512-token forward pass | 2× OpenAI logprob API calls per token × doc length |
| **Training** | Pre-trained on RAID (50k samples) | Per-domain feature selection on Ghostbuster datasets |
| **Offline** | Yes (HF cache) | **No** — requires OpenAI API |
| **RAID AUROC** | 99.28% (leaderboard) | Not reported |
| **Paraphrase tests** | RAID-adversarial (DIPPER, homoglyph, etc.) | PEGASUS + Undetectable.ai only |
| **ESL equity** | RAID includes diverse domains | 25% FP on short Liang TOEFL essays |
| **License** | MIT (TMR model card) | Other (repo) |

### Architectural fit assessment

**Poor fit for live feedback loop:**

- OpenAI API required — violates offline-first, `ANTHROPIC_UNSLOP_SKIP_DETECTOR` philosophy
- Privacy: README states inputs are sent to OpenAI and saved
- Cost: token-wise logprobs on full documents at humanize-loop frequency
- No native `score_ai_probability(text) -> float` without wrapping `classify.py` + API key
- Feature cache is domain-specific (news/essays/creative); arbitrary user prose is OOD

**Possible fit for offline benchmark harness:**

- Add to `benchmarks/detector_bench/` as `--detector ghostbuster` with `OPENAI_API_KEY` env gate
- Compare unslop humanization delta on Ghostbuster's three released datasets
- Report ensemble disagreement: TMR says human, Ghostbuster says AI → text still carries weak-LM signature
- Pair with DivEye surprisal for three-family panel (supervised / probability-features / surprisal-dynamics)

**Do NOT ship as default or PyPI dependency** without license clarification and API cost disclosure.

### Comparison to Ghostbuster's RoBERTa baseline

TMR and Desklib are **same architectural family** as Ghostbuster's RoBERTa-large baseline — but **RAID-trained** with adversarial exposure. Ghostbuster's value proposition over RoBERTa is **OOD generalization** (+13.8 F1 OOD). TMR's value proposition is **RAID robustness** (99.28% AUROC on paraphrase/homoglyph/decoding-shift attacks). For unslop's feedback loop, **RAID-hardened supervised > Ghostbuster-style features** unless the user specifically needs black-box-logits-free detection without fine-tuning.

---

## Actions

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P0** | **Do not integrate Ghostbuster into default `detector.py` loop** | OpenAI API, privacy, cost, license, offline conflict |
| **P1** | **Run Ghostbuster on 3–5 unslop benchmark fixtures** via `classify.py` pre/post humanize | Establish probability-feature-family baseline; compare delta to TMR |
| **P1** | **Test cross-model paraphrase against Ghostbuster** on same fixtures | Confirm `detector.py` escalation path works against this detector family |
| **P2** | **Submit TMR + Ghostbuster (if API available) side-by-side** in `drafts/2026-05-detector-test/` | Document where deterministic unslop helps vs doesn't for multi-LM features |
| **P2** | **Fix stale citation in `docs/research/04-natural-language-quality/A-academic.md`** | Claims AdvPara evaluated Ghostbuster — it did not (8 detectors only) |
| **P3** | **Optional `--detector ghostbuster` backend** behind `OPENAI_API_KEY` + `--detector ghostbuster` flag | For academic users with API access; map logreg output to [0,1] |
| **P3** | **Watch for Ghostbuster v2** with open-weight weak LMs (Llama-3-8B, Mistral) | Would remove API dependency and improve reproducibility |

---

## Open questions

1. **Ghostbuster vs TMR on identical RAID slices?** Ghostbuster never ran RAID. A direct comparison on RAID's news domain would ground-truth the 99 F1 vs 99.28% AUROC claims.

2. **Does unslop structural+soul pass move Ghostbuster scores?** Contractions and sentence splits change tokenization — may shift ada/davinci vectors more than AI-ism removal alone. No data.

3. **Cross-model paraphrase evasion rate against Ghostbuster?** The paper's strongest relevant test is Undetectable.ai (38% evasion). Claude/GPT cross-paraphrase is the unslop-recommended path — untested.

4. **Feature staleness with GPT-4o/Claude 3.5 text.** Training data is gpt-3.5-turbo. Modern model outputs may sit closer to human weak-LM signatures.

5. **Ensemble stopping criterion.** If TMR ≤ 0.5 but Ghostbuster > 0.5, should anti-detector mode continue? Multi-family disagreement is unexplored in unslop.

6. **Open-weight Ghostbuster replication.** Could unslop ship a Ghostbuster-like feature extractor using local LMs (GPT-2 XL + Llama-3-8B-base) without OpenAI API? Research project, not a weekend patch.

7. **Paragraph-level detection.** Ghostbuster defers mixed human/AI documents to future work — common in real student essays.

---

*Agent #07 complete. Cross-refs: Agent #04 (AdaDetectGPT), Agent #17 (Sadasivan impossibility), Agent #25 (Adversarial Paraphrasing), Agent #31 (DIPPER), Agent #35 (cross-model paraphrase), Agent #40 (DAMAGE humanizer tiers), Agent #49 (burstiness/surprisal), Agent #04 (Fast-DetectGPT family).*
