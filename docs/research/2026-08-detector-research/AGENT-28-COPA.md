# Agent #28 — CoPA: Contrastive Paraphrase Attack

**Topic:** Contrastive decoding for training-free AI-text detector evasion  
**Paper:** Fang et al., *Your Language Model Can Secretly Write Like Humans: Contrastive Paraphrase Attacks on LLM-Generated Text Detectors*, EMNLP 2025  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

CoPA (Contrastive Paraphrase Attack) is a **training-free, decoding-time** paraphrase evader. It runs an off-the-shelf LLM twice per token: once with a human-style prompt, once with a machine-style prompt. The next-token distribution is **contrastively purified** by subtracting machine logits from human logits, then sampling with adaptive truncation.

Against eight academic detectors on three datasets, CoPA cuts average TPR at 5% FPR from ~44–66% (no attack) to **~3–13%** after a single paraphrase pass — while keeping P-SP semantic similarity above 90%. It beats DIPPER (11B fine-tuned paraphraser) especially on Fast-DetectGPT, where DIPPER often *increases* detectability.

CoPA sits in the **decoding-time guidance** family (with SICO, contrastive decoding literature). It differs from **GradEscape** (gradient-trained 139M evader, detector-boundary optimization) and **ToBlend** (multi-LLM token ensemble at *generation* time, not post-hoc paraphrase).

**unslop verdict:** CoPA is the clearest academic blueprint for **dual-prompt contrastive humanization**, but unslop cannot implement the core mechanism without logit access. Phase 3 should adopt the **prompt pair** (human scene + anti-machine subtraction as instruction), not the logit arithmetic. Pair with cross-model rewrite (HIP/ToBlend insight) and detector-guided span loop (Adversarial Paraphrasing) for anything aimed at 2026 commercial detectors. Do not cite CoPA numbers against Turnitin or GPTZero v6 without re-benchmarking.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Paper (ACL Anthology)** | https://aclanthology.org/2025.emnlp-main.433/ |
| **Paper (DOI)** | https://doi.org/10.18653/v1/2025.emnlp-main.433 |
| **Paper (arXiv)** | https://arxiv.org/abs/2505.15337 |
| **Paper (arXiv HTML)** | https://arxiv.org/html/2505.15337v3 |
| **Paper (PDF)** | https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-main.433.pdf |
| **Official code** | https://github.com/ffhibnese/CoPA_Contrastive_Paraphrase_Attacks |

### Comparison baselines (this memo)

| Paper | URL | Relation to CoPA |
|-------|-----|------------------|
| **GradEscape** (Meng et al., USENIX Security 2025) | https://arxiv.org/abs/2506.08188 · https://www.usenix.org/conference/usenixsecurity25/presentation/meng · https://www.usenix.org/system/files/usenixsecurity25-meng.pdf · https://doi.org/10.5281/zenodo.15586856 | Gradient evader; detector-targeted; 139M beats 11B DIPPER; tested on Sapling + Scribbr |
| **ToBlend** (token ensemble) | https://arxiv.org/abs/2402.11167 · https://arxiv.org/html/2402.11167v2 · https://anonymous.4open.science/r/ToBlend/ | Multi-LLM token blending at generation; breaks single-source detector assumption |
| **DIPPER** (Krishna et al., NeurIPS 2023) | https://arxiv.org/abs/2303.13408 | Primary paraphrase baseline CoPA beats on Fast-DetectGPT |
| **Adversarial Paraphrasing** (Chakraborty et al., 2025) | https://arxiv.org/abs/2506.07001 · https://github.com/chengez/Adversarial-Paraphrasing | Detector-guided token pick; explicitly contrasts with gradient/contrastive methods |
| **Raidar-A** (Mao et al., 2024) | https://arxiv.org/abs/2402.19433 | Simple "rephrase in human style" LLM query baseline |
| **MASH** (Gu et al., Jan 2026) | https://arxiv.org/abs/2601.08564 · https://github.com/githigher/MASH | Critiques CoPA proxy-guidance; 92% ASR via SFT+DPO |
| **Fast-DetectGPT** (Bao et al., 2024) | https://arxiv.org/abs/2406.04127 | Hardest zero-shot target; CoPA's headline win |
| **Sadasivan impossibility** (2023) | https://arxiv.org/abs/2310.01565 | TV-bound framing for distribution-shaping evasion |

---

## Mechanism

### Problem framing

Given machine text \(y_m\), a paraphraser LLM \(f_\theta\), and detector \(D_w\), the attacker wants rewritten text \(y\) with:
1. Low \(D_w(y)\) (classified human),
2. High semantic fidelity to \(y_m\),
3. No fine-tuned paraphraser and no surrogate detector at attack time.

CoPA's insight: prompting alone ("write like a human") shifts the output distribution toward human-like tokens, but **pretraining priors** still favor high-probability, machine-detectable choices. Prompt engineering operates in input space; detectors read output statistics.

### Two prompt-conditioned distributions

**Human-like prompt \(x_h\):** Scene-based instruction, not bare "be human." The paper's best variant asks the model to rewrite input *as a text message to a friend* (no greetings/emojis). Realistic conversational framing increases lexical diversity.

**Machine-like prompt \(x_m\):** Must be **maximally detectable**, not a neutral paraphrase. Naive "rephrase this" *dilutes* machine features. CoPA uses **verbatim repetition**: system "You are a helpful assistant" + user "Repeat the following paragraph:" + \(y_m\). That preserves the richest machine token preferences for contrast.

At each timestep \(t\), standard autoregressive sampling uses \(p_h'(\cdot \mid x_h, y_m, y_{<t})\) and \(p_m(\cdot \mid x_m, y_m, y_{<t})\).

### Contrastive decoding (core equation)

```text
p_c(· | x_h, x_m, y_m, y_{<t}) ∝ exp( (1 + λ) · f_θ(· | x_h, y_m, y_{<t})
                                  − λ · f_θ(· | x_m, y_m, y_{<t}) )
```

- \(f_\theta\) = raw logits (not softmax probabilities in implementation).
- \(\lambda \ge 0\) = contrast strength; paper default **λ = 0.5**.
- Intuition: amplify human-prompt preferences, penalize tokens the machine prompt would choose — a **self-corrective** decoding loop without querying \(D_w\).

### Adaptive truncation (coherence guard)

Subtracting full vocabularies can boost incoherent tokens. CoPA restricts sampling to:

```text
V_top(y_{<t}) = { v ∈ V : p_h'(v | ...) ≥ α · max_v' p_h'(v' | ...) }
```

Default **α = 1e−5**. Human-prompt confidence defines the candidate pool; contrastive adjustment only operates inside it.

### Theoretical claim

Define \(g(\lambda) = \mathrm{KL}(p_h \,\|\, (1+\lambda)p_h' - \lambda p_m)\). Under premise \(g'(0) < 0\) (human-like distribution lies between machine and true human on KL contours), Theorem 1 guarantees \(\exists \lambda > 0\) such that contrastive \(p_c\) is closer to authentic human \(p_h\) than prompt-only \(p_h'\). Authors note this is a **sufficient condition**, not universal — validate per setting.

### Pipeline diagram

```
Machine text y_m
       │
       ├─► Forward pass (x_h: "text message to a friend") ──► logits_h
       │
       └─► Forward pass (x_m: "repeat paragraph")          ──► logits_m
                    │
                    ▼
         p_c ∝ exp((1+λ)·logits_h − λ·logits_m)
                    │
                    ▼
         Truncate to V_top via α · max(p_h')
                    │
                    ▼
              Sample y_t ; append ; repeat
```

### What CoPA is not

- **Not detector-guided:** Unlike Adversarial Paraphrasing, no per-token score from OpenAI-RoBERTa or RADAR.
- **Not gradient-based:** Unlike GradEscape, no backprop through detector; no trained evader weights.
- **Not multi-model blend:** Unlike ToBlend, single paraphraser, dual *prompts* not dual *models*.
- **Not recursive by default:** One pass suffices; multi-pass gains are marginal vs quality cost.

---

## vs GradEscape vs ToBlend

Three orthogonal attack geometries:

| Dimension | **CoPA** | **GradEscape** | **ToBlend** |
|-----------|----------|----------------|-------------|
| **When** | Post-hoc paraphrase of existing AI text | Post-hoc paraphrase | At original generation |
| **Signal** | Dual-prompt logit contrast | Detector gradient on weighted embeddings | Random LLM switch per token |
| **Training** | None | Fine-tune 139M seq2seq evader | None |
| **Detector access** | None at attack time | White-box, gray-box, or ~2k queries | None |
| **Model access** | **Logits required** (local/vLLM) | Evader + victim tokenizer alignment | Multiple generator APIs |
| **Target specificity** | Generic anti-machine prior | Optimizes victim decision boundary | Breaks single-LM manifold assumption |
| **Semantic control** | P-SP > 0.90; truncation helps | ROUGE-L ≥ 0.9 constraint | Quality varies; k=1 tokens can degrade fluency |
| **Commercial eval** | Academic detectors only | Sapling + Scribbr in the wild | Academic only |
| **2026 SOTA note** | Strong vs Fast-DetectGPT (2024) | Strong vs fine-tuned classifiers | RADAR/entropy partially resist |

### GradEscape — when detector boundaries matter

GradEscape (USENIX Security 2025) treats evasion as **differentiable optimization**: construct weighted embeddings from evader token probabilities, backprop detector feedback, fine-tune a 139M BART-based paraphraser. Handles tokenizer mismatch via warm-start + model extraction for query-only victims.

**Headline numbers:** At ROUGE-Lsum ≈ 0.9, beats DIPPER and four other evaders across GROVER News, HC3, GPA, GPTWiki. **139M parameters outperform 11B DIPPER.** Real-world: ~$10 query budget → 0.617 average evasion on commercial Sapling/Scribbr surrogates.

**Contrast with CoPA:** GradEscape **directly shapes the victim's decision boundary** (or a surrogate's). CoPA assumes machine-like tokens are generic across detectors — faster, cheaper, but **indirect**. MASH (2026) names this weakness explicitly: CoPA's proxy guidance "fails to capture target-specific decision boundaries." GradEscape is the fix when you can query or differentiate the victim.

**When CoPA wins on practicality:** No evader training, no query budget, single forward-model host. When GradEscape wins on efficacy:** Black-box commercial APIs with unknown internals — gradient/query attacks adapt; CoPA's fixed human/machine prompt pair may not align with GPTZero v6 cones or Turnitin's anti-humanizer features.

### ToBlend — when the fingerprint is single-model

ToBlend (arXiv 2402.11167) attacks a different assumption: detectors model text from **one** LM's next-token manifold. At each step, randomly pick an LLM from a pool (classic: GPT-2, OPT, GPT-Neo, GPT-J; advanced: Llama2, Phi-2, Mistral, Gemma) and append its next k tokens.

**Headline numbers (Fast-DetectGPT AUROC, XSum):**
- Baseline single LLM: **0.9845**
- ToBlend classic LLMs, k=1–2: **0.7004**
- ToBlend advanced LLMs, k=1–2: **0.3968**

**Contrast with CoPA:** ToBlend disrupts **source-model identity** at generation; CoPA disrupts **machine token preferences** during rewrite. Complementary. Sun et al. (arXiv 2502.12150) show model fingerprints persist through most rewrites — CoPA's lexical diversity helps; **cross-model** rewrite (unslop Phase 3 S5, HIP) addresses fingerprint persistence ToBlend attacks at the root.

**Partial resistance:** Entropy-based detectors and RADAR (GAN-trained on multi-model paraphrase data) degrade less — same pattern CoPA sees with R-detect and some training-based detectors.

### Three-way synthesis for evasion design

```text
CoPA       → subtract generic machine logits at decode (cheap, local LM)
GradEscape → climb down victim detector gradient (expensive, targeted)
ToBlend    → mix generator manifolds (cross-model, generation-time)
```

Best 2026 stack in literature (MASH, HIP, Adversarial Paraphrasing): **combine** distribution shaping (CoPA-like) + cross-model pass (ToBlend/HIP-like) + detector feedback (GradEscape/AP-like). CoPA alone is one leg, not the stool.

---

## Benchmarks

### Experimental setup

| Axis | Detail |
|------|--------|
| **Datasets** | XSum (news), SQuAD (Wikipedia QA), LongQA (250–350 word answers) — 150 samples each |
| **Source LLMs** | GPT-3.5-turbo (main), GPT-4, Claude-3.5, GPT-4o, Gemini-1.5 Pro (appendix) |
| **Paraphraser** | Qwen2.5-72B-Instruct (default); also R1-Distill-32B, QwQ-32B, GLM-4-9b |
| **Baselines** | DIPPER (lex=60, order=60), Raidar-A ("Help me rephrase it in human style"), Shi et al. RedTeaming (appendix) |
| **Detectors (8)** | LogRank, DetectGPT, DNA-GPT, **Fast-DetectGPT**, Raidar, TOCSIN, OpenAI RoBERTa, R-detect |
| **Metrics** | TPR at fixed FPR (5% main, 1% strict); P-SP semantic similarity |
| **Iterations** | **1** paraphrase pass (default) |

### GPT-3.5-turbo — TPR at 5% FPR (Table 1, averaged across 8 detectors)

| Dataset | No attack | DIPPER | Raidar-A | **CoPA** | CoPA avg TPR |
|---------|-----------|--------|----------|----------|--------------|
| XSum | 66.05% | 43.14% | 49.90% | **12.63%** | |
| SQuAD | 56.27% | 39.38% | 48.44% | **11.06%** | |
| LongQA | 57.09% | 40.27% | 46.82% | **7.44%** | |

**Fast-DetectGPT headline (XSum, GPT-3.5):** 95.33% → **17.00%** TPR after CoPA — paper reports **+57.72% fooling-rate improvement** over strongest baseline on that detector/dataset pair.

**vs DIPPER on Fast-DetectGPT:** DIPPER *raises* TPR on several settings (e.g., GPT-4 XSum: 51.67% no attack → 64.33% after DIPPER). CoPA consistently lowers it.

### GPT-3.5-turbo — TPR at 1% FPR (Table 4, stricter)

| Dataset | DIPPER avg | Raidar-A avg | **CoPA avg** |
|---------|------------|--------------|--------------|
| XSum | 26.39% | 33.91% | **4.92%** |
| SQuAD | 24.62% | 27.07% | **3.40%** |
| LongQA | 25.90% | 27.89% | **2.88%** |

Paper: at FPR=1%, CoPA drives detection accuracy **below 20%** against all eight defenses on aggregate ROC analysis.

### Semantic fidelity

- P-SP scores **> 90%** across datasets (vs human paraphrase threshold 0.76).
- Single-pass CoPA matches or beats multi-pass DIPPER on fooling rate without iterative quality decay.

### Ablations

- **λ:** Positive λ consistently beats λ=0 (prompt-only); optimum ~0.5.
- **Machine prompt design:** "Repeat paragraph" beats stylistic machine prompts for salient \(p_m\) (Fig. 3).
- **Multiple paraphrases:** Diminishing returns; DIPPER quality collapses with iterations.
- **Adversarial training defense:** CoPA-paraphrased texts used to adversarially train RoBERTa detector — appendix F; defense partially mitigates, confirms arms-race framing.

### What benchmarks omit

- **No GPTZero, Turnitin, Originality, Copyleaks** — unlike GradEscape's Sapling/Scribbr probe.
- **Pre–Turnitin-Feb-2026** detector generation; anti-humanizer retrain not in eval set.
- **English only** — authors flag Chinese/Spanish as future work.
- **Short-context academic detectors** — may not reflect GPTZero v6 lexical cones (arXiv 2602.13042) or TSD late-stage volatility (arXiv 2601.04833).

---

## Critics and limitations

### 1. Logit access — not a black-box API attack

CoPA requires **two full forward passes with logit extraction** per token. Standard OpenAI/Anthropic chat APIs do not expose this. Implementation assumes local inference (Qwen2.5-72B in paper) or a serving stack with custom logits processor.

**Implication for unslop:** Phase 3 LLM pipeline runs on API models. CoPA's core math is **not portable** unless unslop adds a local open-weight backend or a host that supports contrastive logits hooks.

### 2. Indirect proxy vs target-specific boundaries (MASH critique)

MASH (arXiv 2601.08564) evaluates CoPA among 11 baselines and reports:

> "Among existing paraphrase-based baselines, DIPPER struggles with out-of-distribution generalization, while **CoPA's indirect proxy-guidance fails to capture target-specific decision boundaries.**"

MASH's Style-SFT + DPO + inference refinement hits **~92% ASR** vs CoPA's academic TPR reductions — different metrics, but the critique stands: subtracting generic machine logits ≠ optimizing against the detector you face in production.

### 3. Adversarial Paraphrasing supersedes on transfer (when detector is available)

Chakraborty et al. (arXiv 2506.07001) position detector-guided decoding as strictly stronger when a guidance detector exists:

- Simple paraphrase **increases** TPR on RADAR (+8.57%) and Fast-DetectGPT (+15.03%) at 1% FPR.
- Adversarial Paraphrasing with OpenAI-RoBERTa-Large guidance: **−64.49%** RADAR, **−98.96%** Fast-DetectGPT TPR@1%FPR.
- **Average 87.88% relative TPR reduction** across eight deployed detectors.

They explicitly classify CoPA-style methods as not using the detector signal at generation time. CoPA is the **no-detector-access** optimum; AP is the **detector-access** optimum.

### 4. Latency and engineering cost

Authors acknowledge: contrastive decoding = **2× forward passes per token**. Real-time humanization at 72B scale is expensive. Adaptive truncation adds overhead. Trade-off vs training DIPPER once and running smaller inference.

### 5. Semantic drift and parameter fragility

- Off-the-shelf paraphrase can deviate from source meaning; may need **resampling**.
- λ and α sensitive; wrong settings reward incoherent tokens (motivation for V_top truncation).
- Human eval in appendix is preliminary; evaluators' linguistic backgrounds not controlled.

### 6. Stale against 2026 commercial stack

unslop's August 2026 landscape notes:

- **Turnitin (Feb 2026):** retrained on humanizer outputs; 60–85% detection recovery on paraphrased text.
- **GPTZero v6 (Jan 2026):** lexical predictability cones — synonym-band swaps insufficient; need structural entropy shifts.

CoPA's wins are against **2024 zero-shot and RoBERTa classifiers**. Extrapolating to commercial screenshots is unsupported.

### 7. Ethical framing (authors')

Paper positions CoPA as **detector stress-test**, not plagiarism tooling. Provides adversarial-training defense appendix. unslop Boundaries align: ESL defense and voice restoration only; decline academic misconduct.

### 8. English-only, lab conditions

Controlled 150-sample slices, known detectors, same paraphraser for baselines. Authors explicitly disclaim real-world adversary deployment expectations.

---

## unslop Phase 3 relevance

### Where Phase 3 is headed

From `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md`, **Phase 3** ships `llm_pipeline.py` — multi-stage LLM humanization mapped from MASH, HIP, TempParaphraser, and Adversarial Paraphrasing:

| Stage | Literature analog | LLM calls | CoPA overlap |
|-------|-------------------|-----------|--------------|
| **S1** | MASH align + refine | 3 (draft → critique → fix) | Low — CoPA has no alignment training |
| **S2** | HIP iterative paraphrase | 1–4 rounds, **cross-model** | Medium — human prompt scene; cross-model = ToBlend/HIP, not CoPA |
| **S3** | TempParaphraser multi-sample | 2 batched | Medium — multi-candidate approximates contrastive selection without logits |
| **S4** | Adversarial span loop | 3 detector-guided | **High for efficacy; opposite mechanism** — AP beats CoPA when TMR available |
| **S5** | Cross-model capstone | 1 different provider | Low vs CoPA; **high vs ToBlend/fingerprint** |

UPDATE-PLAN rates CoPA: **"Partial — prompt + regex analog"** (+57.72% fooling rate in paper; not directly reproducible in API-only unslop).

### What to adopt from CoPA

**1. Dual-prompt instruction pair (portable)**

Map CoPA's \((x_h, x_m)\) to Phase 3 prompts without logit math:

- **Human branch (\(x_h\)):** Scene-based rewrite — "text message to a friend," concrete setting, contractions, fragments allowed. Already adjacent to unslop `anti-detector` LLM guidance in `humanize.py`.
- **Anti-machine branch (\(x_m\) as negative spec):** Explicit subtraction instruction — "Remove patterns typical of AI assistants: uniform sentence length, hedging stacks, tricolon lists, stock transitions, over-qualified claims." This is the **prompt analog** of subtracting machine logits.

**2. Single-pass preference**

CoPA shows one well-designed pass beats naive multi-pass DIPPER. Phase 3 should not default to 4 HIP rounds if S1+S4 already moved TMR — matches unslop empirical note that deterministic passes move TMR ~0.0–0.2 pp; extra LLM rounds cost money with diminishing returns.

**3. Fast-DetectGPT as academic feedback target**

CoPA's largest wins are vs Fast-DetectGPT. unslop's `detector.py` TMR loop is commercial-facing; Phase 3 acceptance should include **academic ensemble** (Fast-DetectGPT + DivEye + TSD per Phase 4 plan), not CoPA numbers alone.

### What not to adopt

| CoPA feature | Why skip in unslop |
|--------------|-------------------|
| Logit contrastive decoding | No logit API on Claude/GPT routes |
| "Repeat paragraph" for \(p_m\) | Produces nonsense in chat-only rewrite flow |
| CoPA-as-primary evasion claim | Boundaries forbid academic misconduct; commercial numbers stale |
| λ/α hyperparameter grid | Not meaningful without logits |

### Mapping to existing code

| Module | Today | CoPA-informed Phase 3 change |
|--------|-------|------------------------------|
| `humanize.py` `_INTENSITY_PROMPT_GUIDANCE["anti-detector"]` | Break uniform shapes, preserve code | Add **anti-machine negative spec** block (contrastive prompt analog) |
| `detector.py` `feedback_loop` | Escalates subtle→full; anti-detector on ladder (Phase 1 fix) | S4 span loop = Adversarial Paraphrasing, not CoPA; use TMR as AP's guidance detector |
| `surprisal.py` | DivEye measurement | CoPA increases lexical diversity → should raise surprisal variance; wire `--detector-surprisal` (Phase 1) |
| `llm_pipeline.py` (planned) | — | S2 prompt pair from CoPA; S5 cross-model from HIP/ToBlend; do **not** name pipeline stage "CoPA" unless local logits backend added |

### Recommended Phase 3 prompt fragment (CoPA analog)

```text
Rewrite the INPUT in a casual, human voice (like a text to a friend — no greeting, no emoji).

While rewriting, actively REMOVE patterns associated with AI assistant output:
- even sentence rhythm and parallel structure
- hedging openers ("It's important to note", "In today's world")
- stock transitions (Furthermore, Moreover, In conclusion)
- overly safe, symmetrical paragraphs

Keep meaning exact. Keep code, URLs, headings, and quoted material unchanged.
```

This captures CoPA's **intent** (human prompt + machine suppression) without logit subtraction.

### Priority vs other Phase 3 inputs

| Source | Phase 3 priority | Reason |
|--------|------------------|--------|
| **HIP cross-model** | P0 | Strongest commercial-detector evidence (UPDATE-PLAN) |
| **Adversarial Paraphrasing S4** | P0 | Maps to existing TMR + span loop |
| **TempParaphraser S3** | P1 | API-compatible multi-sample |
| **CoPA dual-prompt** | P1 | Cheap prompt add; no new infrastructure |
| **GradEscape** | P2 (research) | Needs training loop; out of unslop scope |
| **ToBlend** | P1 via S5 | Cross-model capstone, not token-random blend |

### Honesty constraint (do not oversell)

unslop deterministic + single-pass LLM anti-detector **will not reproduce** CoPA's 57.72% fooling-rate delta. That number requires 72B local contrastive decoding against Fast-DetectGPT on 2024 detectors. Phase 3 goal: **≥5 pp TMR improvement on ≥3 fixtures** (UPDATE-PLAN acceptance), with semantic score ≥ 0.92 — a different, honest bar.

---

## Action items for unslop

| Priority | Action | Owner phase |
|----------|--------|-------------|
| **P0** | Add CoPA-style dual-prompt block to Phase 3 `llm_pipeline.py` spec (human scene + anti-machine negative) | Phase 3 |
| **P0** | Index CoPA in `docs/research/01` and `16` August refresh | Phase 0 |
| **P1** | Benchmark anti-detector LLM output vs Fast-DetectGPT in `detector_bench.py` — establish CoPA-analog ceiling | Phase 4 |
| **P1** | Document logit-contrastive as **non-portable** in RESEARCH_AND_TECH.md | Phase 0 |
| **P2** | Optional local-Qwen backend for research users who want literal CoPA reproduction | Future |
| **—** | Do **not** market "CoPA-powered" or cite EMNLP TPR against Turnitin/GPTZero without re-run | Boundaries |

---

## Bottom line

CoPA proves that **decoding-time contrast** — human prompt plus machine prompt, subtract the latter from the former — beats training an 11B paraphraser on 2024 academic detectors, in one pass, with >90% semantic preservation. The mechanism is elegant and theoretically grounded.

For unslop, CoPA is a **prompt-design reference**, not an implementable subsystem on API-only infrastructure. Phase 3 should steal the dual-prompt structure, pair it with cross-model rewrite (HIP/ToBlend) and detector-guided spans (Adversarial Paraphrasing / GradEscape logic via TMR), and measure against 2026's five-signal stack — not CoPA's 2024 eight-detector table.

**One-line verdict:** CoPA = best training-free **local-LM** paraphrase attack in the 2025 literature; unslop Phase 3 should inherit its prompts, not its logits.
