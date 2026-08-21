# Agent #29 — GradEscape (Gradient-Based Detector Evasion)

**Topic:** Meng et al., *GradEscape: A Gradient-Based Evader Against AI-Generated Text Detectors* (USENIX Security 2025, arXiv 2506.08188)  
**Prepared:** August 19, 2026  
**Scope:** Mechanism, papers, artifacts, TH-Bench / DAMAGE / MGTBench coverage, unslop refuse vs integrate  
**Status:** complete

---

## Executive summary

GradEscape (June 2025, Zhejiang University et al.) is the first **gradient-based** evader for AI-generated text (AIGT) detectors. It fine-tunes a 139M-parameter seq2seq paraphraser by backpropagating through the victim detector via **weighted pseudo-embeddings**, overcoming the discrete-token barrier that blocked PGD-style attacks in NLP. At ROUGE ≈ 0.9, it beats four baselines including **DIPPER (11B)** on evasion rate while using **2.48 GB GPU memory vs 43.51 GB** for DIPPER and finishing inference in **105s vs 412s** on the paper's hardware.

The paper also ships **query-only attack tooling** (tokenizer inference + model extraction) and demonstrates live evasion against **Sapling** and **Scribbr** commercial APIs (~$10 query budget → **61.7% average evasion rate**). It proposes **active paraphrase defense** — normalize expression style before detection — which cuts evasion below 20% on most datasets and is explicitly **robust against GradEscape itself** because the defense breaks the tokenizer-alignment precondition for pseudo-embeddings.

**Benchmark gap:** GradEscape is **not** in TH-Bench (published March 2025; GradEscape June 2025), **not** in DAMAGE's 19-tool commercial audit (DIPPER only), and **not** in MGTBench (2023 framework). Its numbers are self-contained in the USENIX paper + Zenodo artifact.

**Unslop verdict:** **Refuse to ship; integrate the insight.** GradEscape is a red-team training pipeline (GPU, surrogate detectors, adversarial fine-tuning) — the opposite of unslop's prompt-level slop removal. unslop should cite GradEscape as evidence that (a) small detector-aware models beat large blind paraphrasers, (b) style-disparity is the core detector vulnerability, and (c) the GradEscape authors' active-paraphrase defense aligns with unslop's voice-normalization goal more than with evasion. Anti-detector mode stays scoped to ESL false-positive defense; `--detector-feedback` remains a local signal, not a GradEscape substitute.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | GradEscape: A Gradient-Based Evader Against AI-Generated Text Detectors |
| **Authors** | Wenlong Meng, Shuguo Fan, Chengkun Wei (Zhejiang U.); Min Chen (Vrije U. Amsterdam); Yuwei Li (NUDT); Yuanchao Zhang (Mybank, Ant Group); Zhikun Zhang, Wenzhi Chen (Zhejiang U.) |
| **Venue** | 34th USENIX Security Symposium, Seattle, August 2025 |
| **arXiv** | https://arxiv.org/abs/2506.08188 |
| **arXiv HTML** | https://arxiv.org/html/2506.08188v2 |
| **DOI (arXiv)** | https://doi.org/10.48550/arxiv.2506.08188 |
| **USENIX PDF** | https://www.usenix.org/system/files/usenixsecurity25-meng.pdf |
| **USENIX appendix** | https://www.usenix.org/system/files/usenixsecurity25-appendix-meng.pdf |
| **Talk page** | https://www.usenix.org/conference/usenixsecurity25/presentation/meng |

**One-line contribution:** Make AIGT detector loss differentiable w.r.t. a paraphraser's parameters via weighted embeddings; handle tokenizer mismatch with warm-started repeaters; attack commercial detectors through surrogate extraction.

---

## 2. Mechanism

### 2.1 Problem: discrete text blocks gradients

Vision adversarial attacks (FGSM, PGD, C&W) differentiate through pixel tensors. Text evaders historically faced a hard stop: sampling tokens from a language model is non-differentiable. Prior work split into:

- **Perturbation evaders** (RP, DFTFooler): word swaps, no detector gradient.
- **Paraphrase evaders** (DIPPER, SentPara): large seq2seq rewrite, detector-agnostic training.
- **Query evaders** (TextFooler): greedy word replacement using detector feedback, 500–700 queries per sample — impractical at scale.

GradEscape closes the gap: **train the evader with detector gradients**, like GAN-style adversarial training in vision, but adapted for text.

### 2.2 Weighted pseudo-embeddings (core trick)

1. Evader \(F_\theta\) is a seq2seq model (typically BART-base, ~139M params).
2. At each position, \(F_\theta\) outputs a token **probability vector** \(p_i\) over the vocabulary.
3. Instead of argmax-sampling discrete tokens into the detector, GradEscape computes a **weighted sum of the detector's embedding matrix rows**: \(\tilde{e}_i = \sum_j p_{ij} \cdot E_j\).
4. The sequence of \(\tilde{e}_i\) flows through the victim detector \(D_V\); classification loss \(L_c\) backpropagates to \(\theta\).

This is the textual analogue of straight-through / soft-token estimators. The evader learns to paraphrase toward regions of embedding space the detector labels "human."

### 2.3 Multi-objective loss

GradEscape minimizes:

\[
L = \alpha L_l + \beta L_s + (1 - \alpha - \beta) L_c
\]

| Term | Role |
|------|------|
| \(L_c\) | Classification loss — fool detector (functional constraint) |
| \(L_l\) | Label loss — token-level consistency with input (no reference model on GPU; saves memory) |
| \(L_s\) | Semantic loss — MSE between sentence-transformer encodings of input vs output |

Hyperparameters \(\alpha, \beta\) trade evasion vs fidelity. The paper plots evasion rate vs ROUGE, cos-sim, perplexity, GRUEN across settings.

### 2.4 Tokenizer mismatch: warm-started evader

Detectors (RoBERTa, GPT-2, BERT) and paraphrasers (BART) use different tokenizers. GradEscape's fix:

1. Build an encoder-decoder **repeater** sharing the detector's tokenizer (e.g., BERT2BERT for BERT targets).
2. Pretrain repeater to copy input → output on mixed AlpacaGPT4 / OpenWebText / WikiText (~15k samples, 5k steps).
3. Fine-tune that warm-started model with GradEscape losses.

For RoBERTa victims, BART already shares the tokenizer — direct attack. For GPT-2, token re-mapping maps BART logits into GPT-2 vocabulary.

### 2.5 Opaque (query-only) attack

When the victim is a black-box API:

1. **Tokenizer inference:** craft inputs where punctuation/space insertions change detection confidence (DC); infer whether victim uses RoBERTa-style tokenization.
2. **Model extraction:** query 2k–6k labeled samples → train surrogate \( \hat{D}_V \).
3. **GradEscape training** against \(\hat{D}_V\).

Results: **2,000 queries ≈ 90% of white-box evasion rate**; shadow-dataset attack (12k samples, no queries) matches open-model performance. Commercial Sapling attack: infer RoBERTa surrogate, ~$10 API spend.

### 2.6 Attack data requirement

Unlike detector training (human + AI pairs), GradEscape needs **only LLM-generated synthetic text** — trivial for an attacker who owns the generator. Training: 9,000 samples per dataset, non-overlapping with detector train set. Full training ~50 minutes on consumer hardware (batch 64, 5 epochs).

### 2.7 Proposed defense: active paraphrase

GradEscape's root-cause analysis: detectors exploit **expression-style disparity** (formality, colloquialism, spelling) between human and AI corpora, not pure semantics. Defense:

1. Paraphrase all training data with Llama-3-8B-Instruct (`"Rewrite the following text for me:\n\n{text}"`).
2. Train detector on paraphrased corpus.
3. At inference, paraphrase test input before classification.

**Effect:** evasion rate **below 20%** on GROVER, **below 10%** on HC3/GPA/GPTWiki for all evaders including GradEscape — except GradEscape on GPA (~still elevated). Defense is **robust to white-box GradEscape** because paraphraser and detector tokenizers differ, breaking pseudo-embedding attack path. Tradeoff: LLM paraphrase cost + ~5% accuracy drop on most datasets (GROVER worse).

This defense is conceptually adjacent to **DAMAGE** (train on humanized text) and **Turnitin's August 2025 anti-humanizer update**, but operates on style normalization rather than adversarial augmentation alone.

---

## 3. Experimental results (paper-native)

### 3.1 Setup

| Dimension | Detail |
|-----------|--------|
| **Datasets** | GROVER News, HC3, GPA, GPTWiki (4 AIGT detection benchmarks) |
| **Victim detectors** | RoBERTa, GPT-2, BERT fine-tuned classifiers; baseline evasion < 2% |
| **Baselines** | RP, DFTFooler, DIPPER (11B), SentPara |
| **Metric** | Evasion rate (ER) at controlled ROUGE / cos-sim / GRUEN / PPL |

### 3.2 White-box highlights (Section 6.2)

- GradEscape **Pareto-dominates** baselines on evasion-vs-quality plots (Figures 3–4) for GROVER News and HC3.
- **DIPPER** only exceeds ER > 0.8 on GROVER; on other datasets ER **< 0.4** despite 11B parameters.
- RP/DFTFooler can match ER at some ROUGE points but **destroy readability** (high PPL, low GRUEN).
- On easy datasets (GROVER), GradEscape makes **minimal word-level edits**; on hard datasets (HC3), it shifts **narration style** like full paraphrasers.
- ER scales **linearly with ROUGE/cos-sim** for GradEscape — more modification → easier evasion, but readability doesn't necessarily degrade.

### 3.3 Efficiency (Table 3)

| Evader | Time | GPU Mem |
|--------|------|---------|
| GradEscape | 105s | 2.48 GB |
| SentPara | 329s | 4.43 GB |
| RP | 382s | 3.51 GB |
| DFTFooler | 1182s | 9.54 GB |
| DIPPER | 412s | **43.51 GB** |

GradEscape is the only evader runnable on consumer GPUs among the paraphrase-class baselines.

### 3.4 Real-world commercial detectors (Table 4, Section 6.6)

Targets: **Sapling** (HTTP API + online demo) and **Scribbr** (web demo). GradEscape rows at ROUGE ≈ 0.85–0.87:

| Detector | Dataset | GradEscape ER | Notes |
|----------|---------|---------------|-------|
| Sapling | HC3 | **0.448** | DC drops 0.801 → 0.550 |
| Sapling | GPTWiki | **0.578** | DC drops 0.758 → 0.422 |
| Scribbr | HC3 | **0.785** | DC drops 0.801 → 0.378 |
| Scribbr | GPA | **0.658** | DC drops 0.829 → 0.496 |

Aggregate across both services: **61.7% evasion rate at ~$10 query cost**. Sapling more robust than Scribbr. Paper includes tokenizer-inference walkthrough for Sapling (RoBERTa surrogate).

### 3.5 ROUGE = 0.9 headline (abstract)

At ROUGE 0.9, GradEscape **consistently beats all four baselines on all four datasets**, including DIPPER at 11B, with 139M parameters. Opaque attack: 2,000 queries → ~90% of white-box effectiveness.

---

## 4. Artifacts and code

**No public GitHub repository** as of August 2026. Code ships via USENIX artifact evaluation on Zenodo:

| Resource | URL |
|----------|-----|
| **Primary artifact (v4)** | https://zenodo.org/records/15586856 |
| **Supplementary record** | https://zenodo.org/records/15586857 |
| **Alt. record** | https://zenodo.org/records/15807727 |

Contents: `GradEscape.zip` (~code + install scripts), `Usenix-AE.zip`, trained evader checkpoints, `real_world_demo_sapling.ipynb`, `real_world_demo_scribbr.ipynb`, `Scribbr.webarchive`.

**Requirements:** 2× NVIDIA RTX A6000 minimum; Ubuntu 20.04+; Conda; Sapling API key (paid) for commercial replication; macOS for Scribbr webarchive demo.

**Install sketch:**
```bash
conda create -n ge python=3.10 && conda activate ge
cd GradEscape && ./install.sh
cp src/AIGT/.config.yaml src/AIGT/config.yaml
```

**External dependency cloned in artifact:** https://github.com/nmrksic/counter-fitting (word similarity matrix for perturbation baselines).

**Reproduction entry points:**
- `./scripts/train_evader_roberta_grover.sh` — white-box effectiveness (compare to Figure 3)
- `real_world_demo_sapling.ipynb` — Table 4 / Figure 20
- `./scripts/paraphrase_defense_grover.sh` + `./scripts/eval_paraphrase_defense_grover.sh` — Figure 11 defense

---

## 5. DAMAGE / TH-Bench / MGTBench coverage

### 5.1 TH-Bench — **not evaluated**

| Item | Detail |
|------|--------|
| **Paper** | https://arxiv.org/abs/2503.08708 |
| **Repo** | https://github.com/DrenfongWong/TH-Bench |
| **Attacks included (6)** | Dipper, Recursion, Prompt, RAFT, HMGC, TOBLEND |
| **GradEscape** | **Absent** — TH-Bench finalized before GradEscape preprint (March vs June 2025) |

TH-Bench headline: no single attack wins effectiveness + quality + cost simultaneously. HMGC dominates metric-based detectors on Essay (AUC 0.913 → 0.185); Recursion trades quality for evasion. GradEscape would likely rank high on **effectiveness × efficiency** if added — 139M params, sub-3GB inference — but TH-Bench authors have not published an extension.

**Implication for unslop:** TH-Bench cannot be used to score GradEscape directly. Cross-paper comparison requires the USENIX figures or a custom TH-Bench port.

### 5.2 DAMAGE — **not evaluated**

| Item | Detail |
|------|--------|
| **Paper** | https://arxiv.org/abs/2501.03437 |
| **Anthology** | https://aclanthology.org/2025.genaidetect-1.9/ |
| **Scope** | 19 commercial humanizers + DIPPER, Grammarly, QuillBot |
| **GradEscape** | **Absent** — research evader, not a commercial SaaS at audit time |

DAMAGE findings relevant by analogy:

- GPTZero TPR drops **99.73% → 60.04%** across commercial humanizers (L1/L2/L3 taxonomy).
- DAMAGE detector trained on humanized text retains **93.2%** detection even against a **GPT-4o fine-tuned adversarial humanizer** optimized against it.
- GradEscape is exactly the class DAMAGE's adversarial fine-tune tests — gradient-signal humanizer — but DAMAGE uses API fine-tuning, not pseudo-embeddings.

**Gap:** No published head-to-head GradEscape vs DAMAGE detector. GradEscape's active-paraphrase defense and DAMAGE's augmentation defense are **complementary** (style normalize + train on humanized variants).

### 5.3 MGTBench — **not evaluated**

| Item | Detail |
|------|--------|
| **Paper** | https://arxiv.org/abs/2303.14822 |
| **Repo** | https://github.com/xinleihe/MGTBench |
| **Attacks** | Paraphrase, random spacing, perturbation (2023-era) |

MGTBench predates GradEscape by two years and uses simpler attack templates. Not applicable for direct numbers.

### 5.4 Lineage placement

GradEscape sits in the **DIPPER → RAFT → StealthRL / AuthorMist / GradEscape** research tier:

| Method | Signal in training loop | Scale |
|--------|-------------------------|-------|
| DIPPER | None (PAR3 paraphrase SFT) | 11B |
| RAFT | Greedy word importance | Black-box |
| GradEscape | **Detector gradient** | 139M |
| AuthorMist / StealthRL | **Detector reward (RL)** | 3B–4B |

GradEscape proves **gradient signal beats scale** for evasion efficiency — the same "small model wins" pattern as AuthorMist (3B) and later MASH (0.1B, arXiv 2601.08564).

---

## 6. unslop: refuse vs integrate

### 6.1 What unslop refuses

| GradEscape capability | Why unslop refuses |
|-----------------------|-------------------|
| Adversarial fine-tuning against victim detectors | Academic-misconduct enablement; requires GPU pipeline + surrogate training — not a writing assistant feature |
| Query-only model extraction against commercial APIs | Active attack tooling; violates unslop Boundaries (anti-detector = false-positive defense, not evasion SaaS) |
| Shipping "undetectable" claims | GradEscape itself reports 44–79% ER on commercial detectors, not 100%; DAMAGE shows even adaptive humanizers leave detectable residue |
| Pseudo-embedding / straight-through rewrite | Implementation complexity orders of magnitude beyond regex + optional LLM pass; no path in `humanize.py` |
| Watermark or provenance stripping | EU AI Act Art. 50; SKILL.md explicit refusal |

GradEscape is **red-team infrastructure**. The authors open-source it "for developing more robust AIGT detectors" — same framing unslop uses for citing attack papers without shipping them.

### 6.2 What unslop integrates (research → product)

| GradEscape insight | unslop integration |
|--------------------|-------------------|
| Detectors latch onto **style disparity**, not semantics alone | Core thesis of unslop: remove AI-ism surface patterns (stock vocab, uniform structure, zero contractions) |
| Small detector-aware models beat large blind paraphrasers | Justifies `--detector-feedback` loop over "run DIPPER" advice; README honesty about commercial humanizers |
| Active paraphrase defense works | Aligns with unslop's goal of **normalizing voice**, not evading detection — unslop is closer to the defense side of Meng et al. Section 7 |
| Evasion ≠ quality free lunch | GradEscape trades ROUGE for ER; unslop's validator preserves code/URLs and rejects slop without adversarial optimization |
| Commercial detectors are vulnerable but not uniformly | Supports anti-detector mode's "not durable" caveat + cross-model second-pass recommendation (TempParaphraser, Adversarial Paraphrasing) |
| DAMAGE-style robust detectors exist | `detector.py` uses TMR as **signal not gate**; cites DAMAGE for why self-reported bypass rates lie |

### 6.3 Anti-detector mode vs GradEscape

| | **unslop anti-detector** | **GradEscape** |
|--|--------------------------|----------------|
| **Mechanism** | Prompt rules: burstiness σ≥6, contractions, rough edges, structure break | Gradient-trained paraphraser |
| **Detector access** | Optional local TMR loop | Victim detector gradients or surrogate |
| **Compute** | Zero extra infra | 2× A6000, fine-tuning |
| **Durability** | Explicitly "not durable" (retrieval defenses, Turnitin Aug 2025) | Degraded by active paraphrase defense |
| **Legitimate use** | ESL false positives (Liang et al.) | Detector robustness research |

unslop's anti-detector procedure is **orthogonal** to GradEscape — surface stylometry vs learned adversarial paraphrase. A document passing unslop anti-detector would **not** automatically achieve GradEscape ER against Sapling/Scribbr. Conversely, GradEscape output may still read as "AI slop" to humans even when detectors fail.

### 6.4 Recommended unslop actions

1. **Cite in research compendium** (Cat 16) — already indexed; ensure IMPLEMENTATION_TRACE notes GradEscape as upper bound on *efficient* adversarial paraphrase.
2. **Do not add GradEscape checkpoint or training recipe** to the plugin bundle.
3. **Eval backlog:** port GradEscape (or request authors add) to TH-Bench attack slot #7 for comparable 3-axis scoring.
4. **Defense alignment:** consider whether unslop's output distribution intentionally moves text toward human colloquial register (GradEscape defense insight) vs adversarial detector minimization.
5. **README:** GradEscape + StealthRL + Adversarial Paraphrasing form a tiered threat model — deterministic unslop < prompt anti-detector < RL/gradient evaders.

---

## 7. Key URLs (full)

**GradEscape**
- https://arxiv.org/abs/2506.08188
- https://arxiv.org/html/2506.08188v2
- https://doi.org/10.48550/arxiv.2506.08188
- https://www.usenix.org/system/files/usenixsecurity25-meng.pdf
- https://www.usenix.org/system/files/usenixsecurity25-appendix-meng.pdf
- https://www.usenix.org/conference/usenixsecurity25/presentation/meng
- https://zenodo.org/records/15586856
- https://zenodo.org/records/15586857

**Benchmarks (GradEscape not included)**
- https://arxiv.org/abs/2503.08708 (TH-Bench)
- https://github.com/DrenfongWong/TH-Bench
- https://arxiv.org/abs/2501.03437 (DAMAGE)
- https://aclanthology.org/2025.genaidetect-1.9/
- https://arxiv.org/abs/2303.14822 (MGTBench)
- https://github.com/xinleihe/MGTBench

**Baselines cited in GradEscape**
- https://arxiv.org/abs/2303.13408 (DIPPER / Krishna et al.)
- https://arxiv.org/abs/2410.03658 (RAFT)

**Adjacent unslop-cited work**
- https://arxiv.org/abs/2506.07001 (Adversarial Paraphrasing)
- https://arxiv.org/abs/2602.08934 (StealthRL)
- https://arxiv.org/abs/2503.08716 (AuthorMist)

**Commercial detectors attacked**
- https://sapling.ai/ (detector API)
- https://www.scribbr.com/ai-detector/ (web demo)

---

## 8. Bottom line

GradEscape is the NLP field's **PGD moment**: differentiable attacks against detectors, 80× smaller than DIPPER, validated on live commercial APIs. It is not in TH-Bench or DAMAGE, so cross-benchmark claims require careful provenance. For unslop, it belongs in the **threat-model bibliography**, not the shipping path — integrate the style-disparity diagnosis and efficiency lesson; refuse the adversarial training stack.
