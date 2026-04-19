# 16 · GitHub Tools & Libraries — A. Academic (Research-Grade OSS Humanizers)

**Scope:** Open-source projects on GitHub whose code ships alongside published academic work on *humanizing* AI-generated text — i.e. paraphrase / rewrite / style-transfer systems whose stated goal is to make machine-generated output pass for human, or equivalently to evade AI-text detectors while preserving meaning. Adjacent academic primitives (authorship obfuscation, detector-robustness benchmarks, watermark-stealing) are included where the core mechanism is a humanization operator or a standardized humanization evaluation harness.

**Research value: high.** A dense, fast-moving literature from 2023–2025 with ~18 directly relevant GitHub repos, clear lineage (DIPPER → HMGC → HUMPA → StealthRL/AuthorMist), and a dedicated benchmark (TH-Bench) that already compares the main attack families. Findings should weight heavily in any technical plan.

---

## Standard field legend

For each project: **Repo · Paper/Venue · Year · Mechanism · Target detectors · License / artifacts · Notes.** Star counts are directional (fetched April 2026 or reported in sources); treat as order-of-magnitude.

---

## Prior Art — Core Humanization / Detector-Evasion Repos

### Foundational paraphraser (the one everyone else benchmarks against)

1. **DIPPER — `martiansideofthemoon/ai-detection-paraphrases`**
   - Paper: Krishna et al., *"Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense"*, **NeurIPS 2023** (arXiv 2303.13408).
   - Mechanism: 11B-parameter T5-XXL paraphraser trained on PAR3 aligned paragraph-level translations. Two scalar knobs — **lexical diversity** and **content reordering** — let an attacker dial in the *minimum* edit needed to flip a detector.
   - Targets broken: DetectGPT (70.3% → 4.6% AUROC), GPTZero, OpenAI classifier, KGW watermarks.
   - Artifacts: `kalpeshk2011/dipper-paraphraser-xxl` on HF; code on GitHub (~195★) and in `google-research/google-research/dipper`. Apache-2.0-style.
   - Role in the field: de-facto **baseline paraphrase attack**; every subsequent paper reports numbers against DIPPER.

### Humanization-specific attack repos (explicitly frame the goal as "humanize")

2. **HMGC — `zhouying20/HMGC`**
   - Paper: Zhou, He, Sun, *"Humanizing Machine-Generated Content: Evading AI-Text Detection through Adversarial Attack"*, **COLING 2024** (arXiv 2404.01907).
   - Mechanism: white/black-box adversarial framework combining paraphrase + minor token perturbations under surrogate-model gradient signals. Misclassifies MGT within ~10 s of attack budget.
   - License: Apache-2.0. Python. Ships detector eval scripts + surrogate training.

3. **HUMPA — "Humanizing the Machine: Proxy Attacks to Mislead LLM Detectors"**
   - Paper: Wang et al., **ICLR 2025** (arXiv 2410.19230; OpenReview `PIpGN5Ko3v`).
   - Mechanism: RL-fine-tuned small LM acts as a **decoding-time proxy** in front of a frontier LLM (Llama2-13B, Llama3-70B, Mixtral-8x7B), biasing token selection toward human-like distributions.
   - Results: –70.4% average AUROC, –95.0% max; –90.9% cross-discipline; –91.3% cross-language, with generation quality preserved.
   - Code: released with the paper (link from ICLR/OpenReview); best-in-class for the "small humanizer head" pattern.

4. **RAFT — `JamesLWang/RAFT`**
   - Paper: *"RAFT: Realistic Attacks to Fool Text Detectors"*, arXiv 2410.03658 (2024).
   - Mechanism: **word-level**, grammar-preserving perturbations chosen greedily via an auxiliary embedding; black-box. Up to 99% success vs DetectGPT, Ghostbuster, RoBERTa-based detectors on XSum/SQuAD/Abstract.
   - Notable: keeps text error-free (human eval indistinguishable from human prose), unlike most paraphrase attacks that leak stylistic tells.

5. **StealthRL — `suraj-ranganath/StealthRL`**
   - Paper: *"StealthRL: Reinforcement Learning Paraphrase Attacks for Multi-Detector Evasion"*, arXiv 2602.08934 (2026).
   - Mechanism: **GRPO** on Qwen3-4B with LoRA, rewarded by the *joint* loss across RoBERTa, Fast-DetectGPT, Binoculars, MAGE. 97.6% ASR; mean AUROC 0.79 → 0.43. Transfers to **held-out detectors** — strong evidence of shared detector vulnerabilities.
   - Artifacts: training code, detector wrappers, MAGE eval pipeline, HF model checkpoints.

6. **AuthorMist — `authormist/authormist-originality` (HF) + associated code**
   - Paper: *"AuthorMist: Evading AI Text Detectors with Reinforcement Learning"*, arXiv 2503.08716 (2025).
   - Mechanism: 3B LM fine-tuned with **GRPO** where the reward is a **commercial detector API** (GPTZero, WinstonAI, Originality.ai). Pioneered the *API-as-reward* pattern that several 2025 follow-ups copy.
   - Results: 78.6–96.2% ASR; semantic similarity ≥ 0.94.

7. **GradEscape — Zenodo (doi:10.5281/zenodo.15586856)**
   - Paper: Meng et al., **USENIX Security 2025**, arXiv 2506.08188.
   - Mechanism: first **gradient-based** evader. Builds weighted embeddings over the discrete token space and differentiates through the detector. Handles tokenizer mismatches (tokenizer-inference + model extraction) for query-only access.
   - Results: outperforms 4 SOTA evaders across 4 datasets × 3 LMs with only **139M parameters** (vs 11B DIPPER). Tested in the wild against **Sapling** and **Scribbr**.
   - Bonus: paper also proposes an "active paraphrase" defense.

8. **SICO — `ColinLu50/Evade-GPT-Detector`**
   - Paper: Lu et al., *"Large Language Models can be Guided to Evade AI-generated Text Detection"*, **TMLR 2024** (arXiv 2305.10847).
   - Mechanism: **Substitution-based In-Context Optimization** — searches for a prompt prefix (≤40 human examples needed) that makes the generator itself emit detector-evading text. No fine-tuning.
   - Targets: GPTZero, OpenAI detector, ChatGPT detector, GPT-2 detector, DetectGPT, Log-Rank. Avg ΔAUC –0.5 across six detectors.
   - Importance: cheapest humanization recipe — "prompt engineering is a valid attack vector."

9. **Adversarial-Paraphrasing — `chengez/Adversarial-Paraphrasing`**
   - Paper: *"Adversarial Paraphrasing: A Universal Attack"*, **NeurIPS 2025** (arXiv 2506.07001).
   - Mechanism: **training-free**; an instruction-following LLM paraphrases under live feedback from a detector. Claims the attack is *universal* because detectors converge on the same "human distribution."
   - Results: vs simple paraphrase, TPR@1%FPR drops **64.5% on RADAR, 98.96% on Fast-DetectGPT, 87.9% avg** across neural, watermark, and zero-shot detectors.

10. **CoPA — `ffhibnese/CoPA_Contrastive_Paraphrase_Attacks`**
    - Paper: *"Contrastive Paraphrase Attacks"*, **EMNLP 2025**.
    - Mechanism: training-free **contrastive decoding** — subtracts an "auxiliary machine-like distribution" from the paraphraser's logits to push outputs away from detectable patterns.
    - Strength: no detector query budget needed at attack time (pure decoding-time).

11. **LLM-Detector-Robustness — `shizhouxing/LLM-Detector-Robustness`**
    - Paper: Shi et al., *"Red Teaming Language Model Detectors with Language Models"*, **TACL 2024** (arXiv 2305.19713).
    - Mechanism: two attacks — (a) context-aware synonym substitution via an auxiliary LLM, (b) automatic prompt search for style-altering instructions. Evaluated vs DetectGPT + watermark detectors with a DIPPER + genetic-search attacker.
    - BSD-3-Clause; small repo but widely cited as an early red-team reference.

### Watermark-focused humanization (still humanization in mechanism)

12. **Revisiting Watermark Robustness — `codeboy5/revisiting-watermark-robustness`**
    - Paper: EMNLP 2024 (arXiv 2411.05277).
    - Mechanism: reverse-engineers the watermark green-list with limited queries, then paraphrases *specifically* around watermarked tokens. Undoes "paraphrase-robust" schemes (KGW, Unigram).

13. **Watermark Stealing — `eth-sri/watermark-stealing`**
    - Paper: Jovanović et al., **ICML 2024**.
    - Mechanism: three-step — query → learn internal watermark rules → scrub/spoof. Enables *spoofing* (making human text look watermarked) and *scrubbing* (humanization of watermarked output). MIT-licensed.

### Authorship-obfuscation repos (same operator, adjacent framing)

14. **StyleRemix — `jfisher52/StyleRemix`**
    - Paper: *"StyleRemix: Interpretable Authorship Obfuscation…"*, arXiv 2408.15666 (EMNLP 2024 Findings).
    - Mechanism: **LoRA modules per style axis** (formality, length, function-word use, grade level, sarcasm, voice) composed at inference. Interpretable knobs — a planning-friendly property missing from most paraphrasers.
    - Artifacts: releases **AuthorMix** (30K) and **DiSC** (1.5K) datasets + HF demo.

15. **JamDec — `jfisher52/JAMDecoding`**
    - Paper: *"JAMDec: Unsupervised Authorship Obfuscation via Constrained Decoding"*, **NAACL 2024**.
    - Mechanism: inference-time only; keyword extraction → constrained diverse beam over GPT-2-XL → filtering. Competitive with GPT-3.5 obfuscation despite small-model backbone.

16. **TinyStyler — `zacharyhorvitz/TinyStyler`**
    - Paper: **EMNLP 2024 Findings**.
    - Mechanism: 800M model + **authorship embeddings**; few-shot target-style transfer trained via reconstruction-from-paraphrase. Not framed as evasion but is the cleanest open "write in a specific human's voice" primitive in 2024.

### Evaluation harnesses (the scaffolding the field now runs on)

17. **MGTBench / MGTBench-2.0 — `xinleihe/MGTBench`, `Y-L-LIU/MGTBench-2.0`**
    - Paper: **ACM CCS 2024** (arXiv 2303.14822).
    - Content: 11 metric-based + 5 model-based detectors (DetectGPT, Fast-DetectGPT, Binoculars, GLTR, GPTZero wrapper, ConDA, …). Ships paraphrase/spacing/perturbation attacks. 2.0 focuses on academic-writing generalization.

18. **TH-Bench — `DrenfongWong/TH-Bench`**
    - Paper: *"TH-Bench: Evaluating Evading Attacks via Humanizing AI Text"*, arXiv 2503.08708 (2025).
    - Content: **first benchmark explicitly for humanization attacks**. 6 attacks (DIPPER, Recursive DIPPER, Token Ensemble, RAFT, HMGC, Prompt-based) × 13 detectors × 6 datasets × 19 domains × 11 LLMs. Measures effectiveness, text quality, and compute cost.
    - Headline finding: **no single attack wins all three axes** — effectiveness ↔ quality ↔ cost trade-offs are real.
    - A fork of MGTBench-2.0, so operationally compatible.

---

## Adjacent Solutions (worth porting patterns from)

- **SemStamp / k-SemStamp — `abehou/SemStamp` (NAACL 2024, ACL 2024).** Sentence-level semantic watermark via LSH/k-means partitions. Relevant inverted: the paper defines a **bigram-paraphrase attack** that is one of the cleanest sentence-structure humanization recipes in the literature.
- **Ghostbuster — `vivek3141/ghostbuster` (NAACL 2024).** A *detector* (99.0 F1 on their benchmarks, beats GPTZero + DetectGPT by ~5.9 F1), but it's the reference benchmark that HMGC / RAFT / HUMPA measure themselves against. Useful to ship as an in-loop reward for any new humanizer.
- **Evasive Soft Prompts (Kumarage et al., EMNLP 2023 Findings, arXiv 2310.05095).** No public repo found, but the *transferable soft-prompt* idea is the precursor to SICO and HUMPA.
- **BART/Mistral AI→Human style-transfer corpus (arXiv 2604.11687).** Releases a 25,140-pair parallel corpus with 11 stylistic markers — reusable as training data for any humanizer regardless of architecture.

---

## Patterns, Trends, and Gaps

### Patterns that converged 2023 → 2026

1. **Mechanism stack.** Four families dominate: (a) **paragraph paraphrase** (DIPPER and descendants), (b) **word-level perturbation** (RAFT, Shi et al.), (c) **detector-in-the-loop RL** (AuthorMist, StealthRL, HUMPA), (d) **decoding-time guidance** (SICO, CoPA, HUMPA's proxy).
2. **API-as-reward is the new normal.** Starting with AuthorMist (early 2025), treating commercial detectors as opaque reward functions has become standard — it sidesteps the need for gradient access and aligns training with the exact surface the user will face in production.
3. **Convergence theorem is empirical.** Multiple 2025 papers (Adversarial-Paraphrasing, StealthRL) report that attacks **transfer** to unseen detectors. The implicit claim — detectors learn the same human-text manifold — is now strongly supported and is the strongest argument for why humanization is tractable *as a general problem* rather than a cat-and-mouse per-detector game.
4. **Small models beat big ones.** GradEscape (139M) and AuthorMist (3B) outperform DIPPER (11B). The frontier moved from scale to **signal quality in the training loop**.
5. **Benchmarks caught up.** Before TH-Bench (mid-2025) every paper reported on its own detector/dataset mix. TH-Bench + MGTBench-2.0 now let any new humanizer plug in and produce comparable numbers — an implementation can rely on this scaffolding rather than reinvent it.

### Gaps worth exploiting

1. **No open "production-grade" humanizer.** Commercial Originality/WinstonAI/Undetectable are closed; research repos are demos. A well-engineered OSS humanizer with the StealthRL training recipe + StyleRemix's per-axis knobs + TH-Bench-scored eval is an empty niche.
2. **Quality metrics are still weak.** Most papers report BERTScore / semantic similarity. Almost no repo reports **fluency-by-human-eval at scale** or downstream task utility (does the humanized essay still argue the same thesis?). Anyone who invests in honest quality measurement differentiates immediately.
3. **Interpretable controls under-explored outside obfuscation.** StyleRemix's per-style LoRAs are a near-perfect fit for a *user-facing* humanizer ("rewrite at grade 10, more informal, less hedging"), but no humanization repo has generalized that UX.
4. **Multilingual is almost absent.** HUMPA shows cross-language gains incidentally; only TextHumanize (non-academic, listed in sibling research docs) explicitly supports 25 languages. Gap for a research-grade multilingual humanizer.
5. **Defense-aware humanization.** Most attacks are evaluated against static detectors. Almost nothing targets **adaptive/active defenses** (Raidar, Binoculars retrained). This is where the arms race will move in 2026.
6. **No standard "humanness" benchmark.** TH-Bench measures *evasion*, not *humanness*. There is room for a benchmark whose ground truth is human preference rankings, not detector scores — a cleaner training signal than API reward.

### Cross-domain analogies (earned)

- **Adversarial examples in vision.** The DIPPER→RAFT→GradEscape arc parallels FGSM→PGD→C&W in vision — same progression from black-box to gradient-based, same eventual finding that attacks transfer because models learn overlapping manifolds. Treat the detector-evasion literature as the textual PGD.
- **Malware polymorphism.** The "humanize a known-bad artifact just enough to pass a classifier" loop is structurally identical to malware packers vs AV. That field's lessons — defenders eventually win with behavioral signals, not static ones — suggests watermark-style + semantic-behavioral detectors (Raidar) will outlive pure stylometric ones, and therefore humanizers that only beat stylometry have a short shelf life.

---

## Sources

- `martiansideofthemoon/ai-detection-paraphrases` — DIPPER repo (NeurIPS 2023).
- `zhouying20/HMGC` — HMGC (COLING 2024).
- arXiv 2410.19230 + ICLR 2025 poster — HUMPA.
- `JamesLWang/RAFT` + arXiv 2410.03658 — RAFT.
- `suraj-ranganath/StealthRL` + arXiv 2602.08934 — StealthRL.
- HF `authormist/authormist-originality` + arXiv 2503.08716 — AuthorMist.
- arXiv 2506.08188 + Zenodo 15586856 — GradEscape (USENIX Security 2025).
- `ColinLu50/Evade-GPT-Detector` + arXiv 2305.10847 — SICO (TMLR 2024).
- `chengez/Adversarial-Paraphrasing` + arXiv 2506.07001 — Adversarial Paraphrasing (NeurIPS 2025).
- `ffhibnese/CoPA_Contrastive_Paraphrase_Attacks` — CoPA (EMNLP 2025).
- `shizhouxing/LLM-Detector-Robustness` + arXiv 2305.19713 — TACL 2024 red-team.
- `codeboy5/revisiting-watermark-robustness` — EMNLP 2024.
- `eth-sri/watermark-stealing` — ICML 2024.
- `jfisher52/StyleRemix` + arXiv 2408.15666 — StyleRemix.
- `jfisher52/JAMDecoding` — JamDec (NAACL 2024).
- `zacharyhorvitz/TinyStyler` — EMNLP 2024 Findings.
- `xinleihe/MGTBench`, `Y-L-LIU/MGTBench-2.0` — MGTBench (CCS 2024).
- `DrenfongWong/TH-Bench` + arXiv 2503.08708 — TH-Bench.
- `abehou/SemStamp` — SemStamp (NAACL 2024).
- `vivek3141/ghostbuster` — Ghostbuster (NAACL 2024), cited as evaluation target.
- arXiv 2310.05095 — Evasive Soft Prompts (EMNLP Findings 2023).
- arXiv 2604.11687 — BART/Mistral AI-to-Human style-transfer corpus.
