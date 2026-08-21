# Agent #19 — MGTBench / TH-Bench

**Topic:** Machine-generated text benchmark suite — detection harness (MGTBench lineage) and humanization-attack harness (TH-Bench)  
**Prepared:** August 19, 2026  
**Scope:** Papers, datasets, repos, leaderboard status, debate, unslop eval implications  
**Status:** complete

---

## Executive summary

**MGTBench** (He et al., CCS 2024) and **TH-Bench** (Zheng et al., KDD 2025) are sibling benchmarks from the Xinlei He / HKUST(GZ) / CISPA cluster. They share infrastructure — TH-Bench forks **MGTBench-2.0** — but answer opposite questions:

| Benchmark | Primary question | Unit under test |
|-----------|------------------|-----------------|
| **MGTBench v1** | Which **detector** wins on clean + simple attacks? | 13 detection methods |
| **MGTBench 2.0** | Do detectors **generalize** across academic domains and new LLMs? | Detectors + attribution + adaptation |
| **TH-Bench** | Which **humanization attack** wins the evasion × quality × cost trade-off? | 6 evading attacks |

**Headline TH-Bench finding:** no attack dominates all three axes. HMGC crushes metric-based detectors but needs a matched surrogate dataset. Recursion beats metrics but wrecks semantics and fails model-based detectors. Prompt preserves fluency but often *raises* detection AUC. TOBLEND evades ChatGPT-Detector but is GPU-heavy and mediocre on fluency.

**Leaderboard:** There is **no public hosted leaderboard** for either suite. Both are offline research harnesses with reproducible scripts and fixed splits. Community "leaderboard" pressure flows through paper tables and downstream benchmarks (RAID, SHIELD, DAMAGE, Chicago Booth 2026).

**Unslop verdict:** **Adopt TH-Bench's three-axis reporting frame; do not ship TH-Bench as a product feature.** unslop's existing `benchmarks/detector_bench.py` already documents the honest result — deterministic rule-stripping moves TMR probability by ~0.1–0.2 pp. MGTBench/TH-Bench confirm why: lexical humanization is a weak attack axis; structural/surprisal/distribution-level changes matter. Use these benchmarks to **scope claims** (what unslop can prove vs what requires LLM/anti-detector mode), not to optimize evasion.

---

## 1. Lineage map

```
MGTBench v1 (CCS 2024)
    │  xinleihe/MGTBench — 3 domains (Essay, WP, Reuters)
    │  8 metric + 5 model detectors; 3 simple attacks
    ▼
MGTBench 2.0 (CCS 2025)
    │  Y-L-LIU/MGTBench-2.0 — + MGT-Academic (16 categories)
    │  generalization, attribution, LLM adaptation tasks
    ▼
TH-Bench (KDD 2025)
    │  DrenfongWong/TH-Bench — fork of MGTBench-2.0
    │  6 humanization attacks × 13 detectors × 3-axis Pareto
    ▼
Satellites (same author cluster, not in TH-Bench attack set):
    AdvPara (NeurIPS 2025), GradEscape (USENIX 2025), TempParaphraser (EMNLP 2025),
    StealthRL (2026), DAMAGE (GenAIDetect 2025), SHIELD (arXiv 2507.15286)
```

TH-Bench explicitly positions against **MGTBench** (detector-centric, 3 crude attacks only), **Stumbling Blocks** (binary + partial quality, no cost axis), and **DetectRL** (detector generalization, no quality/cost).

---

## 2. MGTBench v1

### 2.1 Paper identity

| Field | Value |
|-------|-------|
| **Title** | MGTBench: Benchmarking Machine-Generated Text Detection |
| **Authors** | Xinlei He, Xinyue Shen, Zeyuan Chen, Michael Backes, Yang Zhang (CISPA) |
| **Venue** | ACM CCS 2024 |
| **arXiv** | https://arxiv.org/abs/2303.14822 |
| **DOI (CCS)** | https://doi.org/10.1145/3658644.3670344 |
| **Repo** | https://github.com/xinleihe/MGTBench (~164 ★) |
| **HF Papers** | https://huggingface.co/papers/2303.14822 |

### 2.2 What it benchmarks

**Detectors (13 total):**

| Type | Methods |
|------|---------|
| **Metric-based (8)** | Log-Likelihood, Rank, Log-Rank, Entropy, GLTR, DetectGPT, LRR, NPR |
| **Model-based (5)** | OpenAI Detector, ChatGPT Detector, ConDA, GPTZero, LM Detector |

Note: TH-Bench later drops NPR, DetectGPT, GPTZero (slow or weak in MGTBench ablations) and adds Binoculars, RADAR, Fast-DetectGPT.

**Datasets (3):** Essay, WritingPrompts (WP), Reuters — 1,000 samples each, sourced from Ghostbuster (Verma et al., NAACL 2024). Human text + MGT from 7 LLMs (ChatGPT-turbo, Claude, ChatGLM, Dolly, GPT4All, StableLM, etc.). 80/20 train/test split.

**Tasks:**
1. **Binary detection** — human vs machine
2. **Text attribution** — which LLM (or human) authored the text
3. **Adversarial robustness** — paraphrasing, random spacing, adversarial perturbation

**Prompt template (generation):**

| Dataset | Prompt pattern |
|---------|----------------|
| Essay | Write an essay in *K* words to the prompt \<prompt\> |
| WP | Write a story in *K* words responding to \<prompt\> |
| Reuters | Write a news article in *K* words with headline \<headline\> |

### 2.3 Key findings (paper-native)

- **LM Detector** (fine-tuned BERT + classification head) wins binary detection broadly — e.g. 0.993 F1 vs ChatGPT-turbo on Essay.
- **Metric-based methods** (Log-Likelihood, Log-Rank, GLTR, LRR) transfer better to **new LLMs**; **model-based** methods transfer better to **new datasets**.
- **Text length matters:** ~200 words sufficient for strong detection; short texts remain hard.
- **Few-shot training works:** 10 samples often near full-data performance.
- **Attribution:** model-based >> metric-based (LM Detector 0.927 F1 vs Rank 0.208 on Essay).
- **Adversarial attacks devastate all methods:** LRR F1 drops 0.418 (paraphrase), 0.413 (spacing), 0.469 (perturbation) on WP / ChatGPT-turbo.
- **Takeaway quote:** "Even the best detectors can be evaded by small adversarial perturbations."

### 2.4 Limitations (authors + community)

- Only **3 coarse attacks** — not the 2024–2025 humanizer arsenal (DIPPER-scale paraphrase, detector-guided search, RL humanizers).
- Datasets are **English, short-form** (essays, fiction prompts, news) — not academic LaTeX, code, or multilingual.
- GPTZero included via API — latency and reproducibility issues; later work drops it.
- **No quality axis** — attack success reported without semantic preservation or fluency cost.

---

## 3. MGTBench 2.0 / MGT-Academic

### 3.1 Paper identity

| Field | Value |
|-------|-------|
| **Title** | On the Generalization and Adaptation Ability of Machine-Generated Text Detectors in Academic Writing |
| **Authors** | Yule Liu, Zhiyuan Zhong, Yifan Liao, Zhen Sun, Jingyi Zheng, Jiaheng Wei, et al.; Xinlei He (corresponding) |
| **Venue** | ACM CCS 2025 |
| **arXiv** | https://arxiv.org/abs/2412.17242 |
| **DOI (CCS)** | https://doi.org/10.1145/3711896.3737408 |
| **Repo** | https://github.com/Y-L-LIU/MGTBench-2.0 (~28 ★) |

### 3.2 MGT-Academic dataset

| Dimension | Detail |
|-----------|--------|
| **Scale** | 336M tokens, 749K samples (CCS camera-ready); preprint also cites 73K samples / 20M+ tokens for early subset |
| **Domains** | STEM (8), Social Sciences (3), Humanities (5) → **16 fine-grained categories** |
| **Human sources** | Wikipedia (two-level subtopics), arXiv abstracts/intros/conclusions (pre-2023, LaTeX retained), Project Gutenberg paragraphs |
| **Generators (5)** | Llama-3.1, Mixtral, Moonshot, ChatGPT, GPT-4o-mini — prompted as wiki/paper/book editors |
| **HF mirror** | `AITextDetect/AI_Polish_clean` on HuggingFace |

**Categories (from repo):** Physics, Medicine, Biology, Electrical_engineering, Computer_science, Literature, History, Education, Art, Law, Management, Philosophy, Economy, Math, Statistics, Chemistry.

### 3.3 Tasks beyond v1

1. **Cross-domain binary detection** — train STEM, test Humanities, etc.
2. **Text attribution** — multiclass LLM identification (harder than binary; often overlooked)
3. **Continual adaptation** — detector must adapt to **new LLM classes** with few/many shots and no access to old training data; 8 adaptation techniques benchmarked (~10–13% gains, task remains hard)

### 3.4 Key findings

- Supervised **model-based detectors** dominate in-domain and in cross-domain transfer for both binary and attribution.
- **Attribution is strictly harder** than binary — high binary AUROC does not imply usable source identification.
- Cross-domain FN inflation is systematic — aligns with M4, RAID, SHAP cross-domain work (Agent #11).
- Framework is **extensible** — TH-Bench, APT-Eval, and other 2025 harnesses fork this codebase rather than reinventing.

---

## 4. TH-Bench (Text-Humanization Benchmark)

### 4.1 Paper identity

| Field | Value |
|-------|-------|
| **Title** | TH-Bench: Evaluating Evading Attacks via Humanizing AI Text on Machine-Generated Text Detectors |
| **Authors** | Jingyi Zheng, Junfeng Wang, Zhen Sun, Wenhan Dong, Yule Liu, Xinlei He (HKUST Guangzhou) |
| **Venue** | **KDD 2025** (Toronto), pp. 5948–5959 — **not** GenAIDetect workshop |
| **arXiv** | https://arxiv.org/abs/2503.08708 |
| **DOI (KDD)** | https://doi.org/10.1145/3711896.3737418 |
| **Repo** | https://github.com/DrenfongWong/TH-Bench (~3 ★; fork of MGTBench-2.0) |

### 4.2 Evaluation framework (three axes)

| Axis | Metrics | Intent |
|------|---------|--------|
| **Evasion effectiveness** | AUC drop vs clean text; binary + attribution tasks; adapted-detector scenario | Does humanization fool detectors? |
| **Text quality** | PPL (fluency), cosine similarity + ROUGE-L (semantics), FRE (complexity) | Does humanization preserve meaning and readability? |
| **Computational overhead** | GPU memory, wall time vs token length (100–1000 tokens) | Is the attack deployable? |

**Normalized radar plot (Figure 1):** no attack occupies the outer triangle on all three vertices simultaneously — the paper's load-bearing **Pareto impossibility** result.

### 4.3 Attack roster (6)

| Attack | Category | Mechanism | TH-Bench headline |
|--------|----------|-----------|-------------------|
| **DIPPER** | Paraphrase | 11B T5 paraphraser, lexical diversity + reorder control | High semantic similarity; **weak evasion**; can *increase* Binoculars AUC |
| **Recursion** | Paraphrase | Iterative DIPPER (depth 5) | Strong vs **metric** detectors; **fails all model-based**; worst semantic similarity (cos-sim < 0.65, ROUGE-L < 0.3) |
| **Prompt** | Paraphrase | LLM rewrite with explicit "classify as human-written" instruction (GPT-4o-mini) | Best fluency preservation; **often fails evasion** — Log-Likelihood AUC *increases* on WP (0.907 → 0.928) |
| **RAFT** | Perturbation | Black-box word substitution via auxiliary embeddings + greedy detector feedback | Excellent semantics; moderate evasion; high compute |
| **HMGC** | Perturbation | Surrogate-detector-guided synonym replacement | **Best vs metric detectors** (Essay Log-Likelihood 0.913 → 0.185); needs matched training corpus |
| **HMGC (Mis)** | Perturbation ablation | HMGC with **mismatched** surrogate dataset | Shows domain-mismatch collapse — works on academic splits, not Essay/WP/Reuters |
| **TOBLEND** | Data mixing | Token-level ensemble across multiple LLMs | Strong vs ChatGPT-Detector; expensive; mediocre fluency |

**Baseline Prompt instruction (from repo README):** *"Your task is to rewrite the below article… Keeping the semantic meaning… The new article should be classified as human-written. Only output the new article without anything else."* — structurally similar to commercial humanizer marketing copy.

### 4.4 Detector roster (13)

| Type | Detectors |
|------|-----------|
| **Metric-based (7)** | Log-Likelihood, Rank, Log-Rank, Entropy, GLTR, Binoculars, LRR, Fast-DetectGPT |
| **Model-based (5)** | RADAR (pretrained, not retrained), OpenAI-D, ChatGPT-D, LM-D, ConDA |

Scoring model for metrics: **Llama-2-7B** features → logistic regression (trained per dataset). Model-based detectors use official weights (RoBERTa-base OpenAI/ChatGPT, distilled BERT LM-D, etc.).

### 4.5 Data coverage

| Source | Datasets | Domains | LLMs |
|--------|----------|---------|------|
| MGTBench v1 | Essay, WP, Reuters | 3 | 7 (ChatGPT-turbo, ChatGLM, Dolly, GPT4All, StableLM, Claude, ChatGPT) |
| MGT-Academic | STEM, Social Science, Humanity | 16 | 5 (Llama-3.1, Mixtral, Moonshot, ChatGPT, GPT-4o-mini) |
| **Combined** | **6 dataset groups** | **19 domains** | **11 LLMs** |

### 4.6 Standout numbers (Table 1, binary task)

**HMGC vs metric detectors (Essay, averaged over LLMs):**

| Detector | Clean AUC (approx.) | Post-HMGC AUC |
|----------|---------------------|---------------|
| Log-Likelihood | 0.913 | **0.185** |
| Binoculars | 0.688 | **0.518** |
| Fast-DetectGPT | 0.773 | **0.355** |

**Recursion vs model-based (Essay):**

| Detector | Post-Recursion AUC |
|----------|-------------------|
| OpenAI-D | 0.962 (detection *increases*) |
| LM-D | 0.975 |
| ChatGPT-D | 0.856 |

**Prompt paradox (WP, Log-Likelihood):** AUC 0.907 → **0.928** (attack makes detection easier).

### 4.7 Adapted-detector experiment

TH-Bench trains Fast-DetectGPT and LM-D on HMGC-augmented data, then tests on **held-out attacks**. Finding: HMGC-training collapses detector against HMGC but **does not reliably generalize** to other attacks — supports DAMAGE-style data-centric augmentation (GenAIDetect 2025) over single-attack adversarial training.

### 4.8 Proposed optimizations (preliminary)

1. **Quality-Preserving Attack (QPA)** — plug-in constraints during generation (quality-aware prompts for Prompt; PPL/FRE guards for RAFT; token ranking for TOBLEND). Improves fluency/semantics with minimal evasion loss.
2. **Attack Blending** — combine complementary attacks (e.g., HMGC effectiveness + Prompt fluency). Paper validates directionally; not a shipped tool.

---

## 5. Leaderboard and reproducibility

| Question | Answer |
|----------|--------|
| **Public leaderboard?** | **No.** Results live in paper tables + local script output. |
| **Submission portal?** | None. |
| **Community comparison hub?** | Indirect — RAID (`pip install raid-bench`), M4/SemEval-2024 Task 8, Chicago Booth 2026 (commercial), HuggingFace detector model cards cite MGTBench numbers. |
| **Reproducibility** | Moderate. Code + splits public; TH-Bench substitutes GPT-4o-mini for RAFT's GPT-3.5 (cost); GPU required for DIPPER/TOBLEND; detector training per-dataset. |
| **Stars / adoption** | MGTBench v1 ~164 ★; MGTBench-2.0 ~28 ★; TH-Bench ~3 ★ (new, fork). High **paper citation** velocity matters more than GitHub stars here. |

**Practical reproducibility blockers:**
- Full TH-Bench run = 6 attacks × 13 detectors × 6 dataset groups × 11 LLMs — multi-GPU-week scale.
- HMGC requires per-domain surrogate training.
- Commercial detectors (GPTZero API, Turnitin, Originality) **not in TH-Bench** — gap filled by DAMAGE commercial audit (19 tools, DIPPER-only academic attack).

---

## 6. Debate: supporters vs critics

### 6.1 What supporters get right

- **Splitting detector benchmarks from attack benchmarks** ends apples-to-oranges comparisons. MGTBench answered "who detects best?"; TH-Bench answers "what does humanization cost?"
- **Three-axis Pareto** is now canonical framing in humanization literature (see Cat 15 synthesis, Agent #25 AdvPara, Agent #36 HumanLLM). Reviewers discount single-axis evasion claims.
- **Shared codebase** (MGTBench-2.0 fork) reduces benchmark fragmentation — same loaders, same splits, same detector training protocol.
- **HMGC (Mis) ablation** honestly shows surrogate-mismatch limits — rare in attack papers.
- **Prompt attack failure modes** document that naive "rewrite to fool detector" prompts can **backfire** — important for unslop's claim discipline.

### 6.2 Criticisms and gaps

| Criticism | Detail |
|-----------|--------|
| **Attack set frozen early 2025** | Missing AdvPara (NeurIPS 2025), GradEscape (USENIX 2025), TempParaphraser (EMNLP 2025), StealthRL (2026), MASH, Adversarial Paraphrasing GitHub releases — all postdate or postdate TH-Bench finalization |
| **No commercial detectors** | GPTZero, Turnitin, Originality, Copyleaks, Pangram absent — the detectors users actually hit |
| **Prompt attack is a strawman** | Explicit "classify as human-written" instruction ≠ skilled humanizer UX; inflates "attacks fail" narrative for paraphrase category |
| **Recursion quality collapse** | Known since Sadasivan 2023 — overweighting a degraded attack skews "quality vs evasion" trade-off plots |
| **English-only, academic-heavy** | ESL fairness axis (Liang TOEFL) not measured — unslop's primary anti-detector use case |
| **No hardness stratification** | SHIELD (arXiv 2507.15286) argues easy/hard conflation inflates attack success — fourth axis emerging |
| **Attribution ≠ user task** | Multiclass LLM ID is academically interesting; institutions care about binary human/AI + false-positive fairness |
| **Low repo traction for TH-Bench** | 3 GitHub stars suggests community runs MGTBench-2.0 directly rather than TH-Bench wrapper — integration friction |

### 6.3 Related benchmarks (positioning)

| Benchmark | Relationship |
|-----------|--------------|
| **RAID** | Attack-inclusive detector benchmark; 12 attacks, 10M docs — detector-side complement |
| **M4 / M4GT-Bench** | Multilingual, cross-generator — generalization focus |
| **DetectRL** | Detector adversarial training generalization — cited by TH-Bench as incomplete (no quality/cost) |
| **Stumbling Blocks** | Broader attack taxonomy; TH-Bench claims deeper quality + cost coverage |
| **DAMAGE** (GenAIDetect 2025) | 19 commercial humanizers + defender trained on humanized data — product-facing audit |
| **SHIELD** | Hardness-stratified humanizer eval — extends TH-Bench Pareto to 4 axes |
| **APT-Eval / ai-polished-text** | Polish-degree axis — "minimal edit" still flagged |
| **HumanLLM** | Human preference benchmark — orthogonal to detector evasion |

**GenAIDetect 2025 workshop** (COLING, Abu Dhabi): DAMAGE paper lives here (`aclanthology.org/2025.genaidetect-1.9/`). TH-Bench is **KDD**, not GenAIDetect — but the workshop ecosystem is the debate venue for detection vs humanization.

---

## 7. unslop eval implications

### 7.1 What unslop already measures (and how it maps)

| unslop harness | MGTBench/TH-Bench analogue | Current gap |
|----------------|---------------------------|-------------|
| `benchmarks/run.py` | — (no direct analogue) | AI-ism delta, burstiness, preservation — **lexical/structural**, not detector evasion |
| `benchmarks/detector_bench.py` | MGTBench detector track | TMR + Desklib only; 3 fixtures; ~0.1–0.2 pp movement at balanced/full |
| `benchmarks/stylometric_baseline.py` | Metric-based detector features | Offline bands; no logistic head |
| `benchmarks/adversarial_paraphrasing_comparison/` | TH-Bench attack axis (partial) | Opt-in external clone; not CI |
| `unslop/scripts/detector.py` | HMGC / AdvPara guidance loop | Local HF models; defensive `--detector-feedback` |

**Confirmed alignment:** `benchmarks/README.md` honest finding — rule-stripping alone barely moves TMR — is exactly what TH-Bench predicts for attacks that only touch lexicon (Prompt/HMGC operate at different levels; unslop rules ≈ weak perturbation, not HMGC-scale surrogate optimization).

### 7.2 What unslop should claim (evidence-bound)

| Claim | Supported by | Not supported by |
|-------|--------------|------------------|
| "Removes visible AI-isms" | `run.py` fixtures, validator | MGTBench detection AUC |
| "Preserves code/URLs/headings" | TestPreservation suite | TH-Bench quality metrics |
| "Deterministic pass does not materially fool modern detectors" | `detector_bench.py` TMR runs | — |
| "Anti-detector mode may reduce detector scores" | SKILL.md spec + AdvPara lineage | No published unslop TH-Bench numbers yet |
| "Safe for ESL false-positive defense" | Liang, institutional policy docs | TH-Bench (no ESL slice) |

### 7.3 Integration recommendations

**Integrate (documentation + eval framing):**

1. **Adopt TH-Bench three-axis reporting** for any future humanization eval: evasion × quality (ROUGE/cos-sim) × cost (latency/tokens). Add `--quality-metrics` optional module rather than claiming detector wins alone.
2. **Cite Prompt-paradox** in anti-detector mode docs — naive detector-targeted rewriting can worsen detection; structural + distribution changes first (matches unslop Phase 1 → soul pipeline order).
3. **Map unslop modes to TH-Bench attack taxonomy:**
   - `subtle/balanced/full` ≈ lexical perturbation (weak axis)
   - `voice-match` ≈ style transfer (not evaluated in TH-Bench)
   - `anti-detector` ≈ Prompt-class attack + optional detector feedback — must report quality side
4. **Use MGTBench-2.0 cross-domain splits** if unslop ever benchmarks detection impact on academic prose — 16 categories match institutional use cases better than Essay/WP.

**Refuse (product boundaries):**

1. **Do not ship a "TH-Bench score"** or optimize for HMGC-style surrogate evasion — academic misconduct tooling.
2. **Do not imply MGTBench clean AUROC transfers to humanized text** — MGTBench's own attack section shows collapse under paraphrase.
3. **Do not add commercial detector API keys to CI** — reproducibility and ToS risk; DAMAGE already documents commercial tier behavior.

**Eval backlog (if unslop pursues detector research track):**

| Priority | Task | Effort |
|----------|------|--------|
| P1 | Run `detector_bench.py` post-LLM-pass (not just deterministic) on fixtures | Medium |
| P2 | Port TH-Bench quality metrics (ROUGE-L, cos-sim, PPL) into opt-in bench | Low |
| P3 | Subsample MGTBench-2.0 `Computer_science` + `Literature` (100 pairs) for cross-domain detector delta | High |
| P4 | Compare unslop `anti-detector` vs TH-Bench Prompt baseline on same texts | High (LLM cost) |
| P5 | Track SHIELD hardness buckets if fourth axis becomes publication norm | Medium |

### 7.4 Strategic read for unslop positioning

TH-Bench proves the market promise of "one-click humanize to fool Turnitin" is **false in the general case** — no attack wins all axes, Prompt fails often, Recursion destroys text, HMGC needs insider dataset access. That supports unslop's ethics boundary: we strip slop for **human readability**, not detector laundering.

The corollary unslop must internalize: **detector evasion and slop removal diverge.** An text can read human (no "delve", good burstiness) and still score 98% AI on TMR. Product copy should lead with Before/After **human reading experience**; detector numbers belong in research appendices with TH-Bench-style quality co-reporting.

---

## 8. Primary source index

| Resource | URL |
|----------|-----|
| MGTBench paper | https://arxiv.org/abs/2303.14822 |
| MGTBench CCS DOI | https://doi.org/10.1145/3658644.3670344 |
| MGTBench repo | https://github.com/xinleihe/MGTBench |
| MGTBench 2.0 paper | https://arxiv.org/abs/2412.17242 |
| MGTBench 2.0 repo | https://github.com/Y-L-LIU/MGTBench-2.0 |
| MGT-Academic HF data | https://huggingface.co/datasets/AITextDetect/AI_Polish_clean |
| TH-Bench paper | https://arxiv.org/abs/2503.08708 |
| TH-Bench KDD DOI | https://doi.org/10.1145/3711896.3737418 |
| TH-Bench repo | https://github.com/DrenfongWong/TH-Bench |
| DAMAGE (GenAIDetect) | https://aclanthology.org/2025.genaidetect-1.9/ |
| SHIELD (4th axis) | https://arxiv.org/abs/2507.15286 |
| unslop detector bench | `benchmarks/detector_bench.py` |
| unslop bench README | `benchmarks/README.md` |

---

## 9. One-paragraph summary

MGTBench (CCS 2024) standardized **detector** comparison on Essay/WP/Reuters with 13 methods and showed clean-domain detection works until simple paraphrase attacks land. MGTBench 2.0 (CCS 2025) extended to **MGT-Academic** — 16 categories, 749K samples — and exposed cross-domain and attribution failures. TH-Bench (KDD 2025), forked from MGTBench-2.0, flipped the unit under test to **humanization attacks** and established the field's governing trade-off: **evasion × quality × compute**, with no dominant attack (HMGC beats metrics but needs matched surrogates; Recursion beats metrics but destroys semantics; Prompt preserves fluency but often backfires). There is no public leaderboard — only reproducible harnesses. For unslop: adopt the three-axis reporting frame, cite the Prompt-paradox and rule-stripping insufficiency results already seen in `detector_bench.py`, and refuse to productize HMGC-class surrogate evasion; lead claims with human-readable slop removal, not detector AUROC.
