# Agent #17 — Sadasivan Impossibility Bound

**Topic:** Sadasivan et al., *Can AI-Generated Text be Reliably Detected?* (arXiv:2303.11156)  
**Prepared:** August 19, 2026  
**Scope:** TV-distance bound, paraphrase attacks, recursive DIPPER, debate with later detectors (DivEye, Chakraborty), educator/policy impact, unslop framing  
**Status:** complete

---

## Executive summary

Sadasivan et al. (2023–2025 revisions) is the foundational **impossibility** paper in AI-text detection. Its core claim is distributional, not architectural: for any detector \(D\), AUROC is capped by how far machine text distribution \(\mathcal{M}\) sits from human distribution \(\mathcal{H}\) in total variation (TV). As TV(\(\mathcal{M},\mathcal{H}\)) → 0, even the **best possible** detector approaches a coin flip (AUROC → 0.5).

Empirically, the paper shows this is not merely asymptotic. Lightweight paraphrasers (T5 222M, PEGASUS 568M) — models **2–6× smaller** than the generator — collapse watermark detectors (97% → 57–80%), zero-shot detectors (DetectGPT AUROC 96.5% → 25.2%), and trained classifiers (RoBERTa-Large TPR 100% → 60% at 1% FPR). **Recursive DIPPER** with detector-guided selection drops DetectGPT AUROC from 82% → 18% and breaks Krishna et al.'s retrieval defense from 100% → 25% after five rounds.

The paper does **not** say detection is always useless. It says: (a) paraphrase is near-optimal because \(|P(s)| \gg |L(s)|\) for most sentences; (b) high-stakes thresholds (90% TPR at 1% FPR) are **impossible** when distributions overlap more than ~11%; (c) watermarking raises TV but paraphrase redefines \(\mathcal{M}\) as the paraphraser output distribution, re-applying the same bound.

Later work reframes the debate without overturning the bound:

| Paper | Relationship to Sadasivan |
|-------|---------------------------|
| **Chakraborty et al. (ICML 2024)** | Possibility counter: multi-sample detection raises effective TV exponentially; single-pass bound is "too conservative" for bot/account-level detection |
| **DivEye (TMLR 2026)** | New feature axis (surprisal variance) that survives paraphrase better than perplexity; still subject to TV bound if adversary widens variance |
| **Adversarial Paraphrasing / StealthRL / TempParaphraser** | Operationalize Sadasivan's paraphrase intuition at scale |
| **Christ–Gunn–Zamir (COLT 2024)** | Cryptographic watermarks can be distributionally undetectable — side-channel, not refutation of TV for unwatermarked text |

**Unslop framing:** Sadasivan licenses **distribution-shaping** (reduce TV by removing AI-isms, injecting burstiness, widening surprisal variance) over **single-detector score chasing** (optimize one commercial API until green). The anti-detector mode in `skills/unslop/SKILL.md` is architecturally aligned: burstiness band, structural variation, contractions, specificity, rough edges — all TV-reduction moves. The `--detector-feedback` ladder in `unslop/scripts/detector.py` is explicitly a secondary, non-durable layer that recommends cross-model paraphrase when exhausted.

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | Can AI-Generated Text be Reliably Detected? |
| **Authors** | Vinu Sankar Sadasivan, Aounon Kumar, Sriram Balasubramanian, Wenxiao Wang, Soheil Feizi |
| **First posted** | March 2023 |
| **Revisions** | Through 2024–2025 (v4+ adds pseudorandom-generator extension, tightness proof) |
| **arXiv** | https://arxiv.org/abs/2303.11156 |
| **HTML** | https://arxiv.org/html/2303.11156v4 |
| **HuggingFace** | https://huggingface.co/papers/2303.11156 |

**One-line contribution:** Empirically breaks watermark, zero-shot, trained, and retrieval-based detectors via paraphrase; theoretically proves AUROC ceiling from TV distance; demonstrates watermark spoofing and retrieval poisoning.

---

## 2. The TV-distance impossibility bound

### 2.1 Setup

- \(\Omega\) = set of all text sequences
- \(\mathcal{H}\) = human text distribution; \(\mathcal{M}\) = machine text distribution (or any two distributions — the bound is general)
- Detector \(D: \Omega \rightarrow \mathbb{R}\); threshold \(\gamma\) yields ROC from TPR/FPR
- TV(\(\mathcal{M},\mathcal{H}\)) = total variation distance between the two distributions

### 2.2 Theorem 1 (core bound)

\[
\text{AUROC}(D) \leq \frac{1}{2} + \text{TV}(\mathcal{M},\mathcal{H}) - \frac{\text{TV}(\mathcal{M},\mathcal{H})^2}{2}
\]

**Interpretation:**

| TV(\(\mathcal{M},\mathcal{H}\)) | Max AUROC (best detector) | Practical reading |
|----------------------------------|---------------------------|-------------------|
| 0.0 | 0.50 | Random classifier |
| 0.1 | 0.595 | Chakraborty uses this as "hard" single-sample case |
| 0.2 | 0.68 | "Unreliable" per authors |
| 0.5 | 0.875 | Need TV > 0.5 for AUROC ≥ 0.9 |
| 1.0 | 1.00 | Perfect separation (tight bound) |

The bound is **tight**: Appendix A constructs \(\mathcal{M}\), \(\mathcal{H}\), and \(D\) achieving equality.

### 2.3 High-stakes deployment constraint

Authors note that for **90% TPR at 1% FPR** — the bar academic integrity tools claim — detection fails when distribution overlap exceeds **~11%** (TV < 0.89). This is stronger than "AUROC looks okay": operating-point constraints bite earlier than area-under-curve summaries suggest.

### 2.4 Extensions in later revisions

1. **Pseudorandom generators:** For polynomial-time detectors, bound holds with negligible correction \(\epsilon\) when true randomness is replaced by PRGs.
2. **Paraphraser-as-distribution:** For watermarked output \(s\), redefine \(\mathcal{M}\) = paraphraser outputs similar to \(s\), \(\mathcal{H}\) = human outputs similar to \(s\). Paraphrase **shrinks effective TV** between post-paraphrase machine text and human paraphrase space — watermarking does not escape the framework.
3. **Style-specific instantiation:** \(\mathcal{H}\) can be one author's distribution; \(\mathcal{M}\) an adversary mimicking that author. Bound applies per register, not only "all human text."

### 2.5 Empirical TV estimates (§4)

Figure 8 in the paper plots TV estimates between WebText and GPT-2 (small/medium/large/XL) outputs at sequence lengths 25–100. **Trend:** larger GPT-2 variants → lower TV vs human text. This connects the abstract bound to model scaling: better LMs → smaller distributional gap → lower detection ceiling.

---

## 3. Paraphrase as attack — mechanism and numbers

### 3.1 Intuition (the \(|L(s)|\) vs \(|P(s)|\) argument)

For sentence \(s\):

- \(P(s)\) = set of human-meaningful paraphrases of \(s\)
- \(L(s)\) = subset the source LLM would actually generate with same meaning

If \(|L(s)| \ll |P(s)|\): random paraphrase likely lands outside LLM's typical output manifold → evades detector (low FPR preserved).  
If \(|L(s)| \approx |P(s)|\): detector cannot achieve low FPR and low FNR simultaneously.

Paraphrase is not an implementation bug. It exploits a **measure-theoretic** gap between "what the model writes" and "what humans could write with the same meaning."

### 3.2 Watermark attacks (Kirchenbauer green-list, OPT-1.3B)

100 XSum passages; sentence-level paraphrase.

| Condition | Green-list token % | Detector accuracy | Perplexity |
|-----------|-------------------|-------------------|------------|
| Watermarked LLM output | ~58% | **97%** | 6.7 |
| PEGASUS paraphrase | ~44% | **80%** | 10.2 (+3.5 PPL) |
| T5 paraphrase | — | **64%** | 16.7 |
| T5 paraphrase (alt setting) | — | **57%** | 18.7 |

Recursive paraphrasing (Figure 3): accuracy degrades further with each round \(pp_i\).

### 3.3 Non-watermark detectors (GPT-2 Medium, 200 XSum passages, T5 222M paraphraser)

| Detector | Before | After single paraphrase |
|----------|--------|-------------------------|
| DetectGPT AUROC | 96.5% | 59.8% (→ 25.2% in abstract) |
| Other zero-shot (entropy, likelihood, rank) | ~99%+ | Near chance |
| OpenAI RoBERTa-Large TPR @ 1% FPR | 100% | ~80% (→ 60% with multi-query) |

### 3.4 Why small paraphrasers win

Attack models are **2.3×–5.8× smaller** than target LLM but fine-tuned specifically for paraphrase. Task specialization beats scale for signature removal — relevant to unslop's "cross-model second pass" recommendation (different family > same-family polish).

---

## 4. Recursive DIPPER results

Sadasivan uses Krishna et al.'s **DIPPER** (11B T5-XXL, NeurIPS 2023) for recursive attacks — the same model Krishna proposed as both attack and retrieval defense.

### 4.1 Protocol

1. Generate text with GPT-2 Medium.
2. Apply DIPPER recursively \(i\) times (\(pp_i\)).
3. With black-box detector access, **select the paraphrase with worst detection score** among \(i\) candidates.
4. Plot ROC / measure accuracy.

### 4.2 Key numbers

| Target | Metric | Before | After recursive DIPPER |
|--------|--------|--------|------------------------|
| DetectGPT | AUROC | 82% | **18%** |
| Watermark detector | Accuracy | 97% | Degrades per Figure 3 (recursive \(pp_i\)) |
| Krishna retrieval defense | Detection accuracy | 100% (1 round) | **25%** (5 rounds) |

**Retrieval defense postmortem:** Krishna et al. store provider-side generations; detection = semantic match above threshold. Single DIPPER pass: defense holds. Five recursive rounds with score-guided selection: semantic drift stays within human-readable band but escapes embedding match. Authors note retrieval also raises **privacy** concerns (storing all user–LLM conversations).

### 4.3 DIPPER as canonical follow-on

Krishna et al. (arXiv:2303.13408, NeurIPS 2023) published DIPPER separately but Sadasivan's recursive experiment is the definitive stress test of retrieval defense.

| DIPPER headline (Krishna) | Sadasivan recursive counter |
|---------------------------|----------------------------|
| DetectGPT 70.3% → 4.6% @ 1% FPR | DetectGPT AUROC 82% → 18% |
| Retrieval recovers 80–97% (single paraphrase) | 5× recursive → 25% accuracy |
| 11B paragraph paraphraser | Same model, used as multi-round TV reducer |

**Repo:** https://github.com/martiansideofthemoon/ai-detection-paraphrases  
**Model:** `kalpeshk2011/dipper-paraphraser-xxl` (HuggingFace)

---

## 5. Spoofing and watermark learning (§5)

Beyond evasion, Sadasivan documents **offensive** failures:

1. **Watermark spoofing:** Query soft-watermarked LLM repeatedly → infer green-list rules → inject watermark signature into human-written toxic text → falsely attributed to LLM provider.
2. **Retrieval poisoning:** Adversary paraphrases victim's human essay via LLM, registers paraphrase in database → original human essay flagged as AI (false positive on innocent work).

These are policy-relevant: detectors don't just miss AI text — they can **accuse the wrong party**.

---

## 6. Debate with later detectors

### 6.1 Sadasivan vs Chakraborty — same curve, different sample regime

| | Sadasivan (2303.11156) | Chakraborty (2304.04736, ICML 2024) |
|--|------------------------|-------------------------------------|
| **Claim** | Single-sample AUROC bounded by TV | Multi-sample detection feasible |
| **Mechanism** | TV(\(\mathcal{M},\mathcal{H}\)) small → bound ≈ 0.5 | TV(\(m^{\otimes n}, h^{\otimes n}\)) → 1 exponentially in \(n\) |
| **Use case** | Single essay, single email | Bot detection, account-level corpus |
| **Verdict** | Both correct | Essay-length plagiarism vs social-media bot |

Chakraborty's Figure 1 explicitly replots Sadasivan's bound at TV=0.1 (AUROC 0.6) and shows multi-sample ROC approaching 1. **Implication for educators:** one-shot essay detection is exactly the hard regime Sadasivan analyzes; Chakraborty does not rescue single-submission integrity tools.

**URL:** https://arxiv.org/abs/2304.04736

### 6.2 DivEye (TMLR 2026) — new axis, same bound

**Basani & Chen,** *Diversity Boosts AI-Generated Text Detection* (arXiv:2509.18880)

- **Signal:** Intra-document **surprisal variance** and temporal dynamics — not mean perplexity.
- **Claim:** +33.2% vs zero-shot baselines; robust to paraphrase on MAGE/RAID; +18.7% when stacked on Fast-DetectGPT, Binoculars, RADAR.
- **Relation to Sadasivan:** DivEye explicitly cites Sadasivan's impossibility (§2, §3.1). It shifts **where** separability lives (variance trajectory) but does not repeal TV: an adversary that widens surprisal variance (burstiness, sentence-length swings) moves \(\mathcal{M}\) toward \(\mathcal{H}\) on that axis too.

**Debate summary:**

| Detector generation | Primary signal | Paraphrase survival | TV-bound status |
|--------------------|----------------|---------------------|-----------------|
| DetectGPT / Fast-DetectGPT | Log-prob curvature | Poor (Sadasivan T5/DIPPER) | Collapses first |
| Binoculars / Ghostbuster | Cross-model perplexity | Moderate | Still paraphrasable |
| DivEye | Surprisal variance rhythm | Better (author claim) | Reducible via structural humanization |
| Turnitin Aug 2025+ | Humanizer-output training | Retrained on bypass tools | Arms race, not proof |

**URLs:**
- Paper: https://arxiv.org/abs/2509.18880
- TMLR: https://mlanthology.org/tmlr/2026/basani2026tmlr-diversity/
- Code: https://github.com/IBM/diveye

### 6.3 Post-2025 evasion stack (operational Sadasivan)

These papers implement the paraphrase/TV-reduction strategy at higher sophistication:

| Paper | arXiv | Headline | Sadasivan connection |
|-------|-------|----------|----------------------|
| Adversarial Paraphrasing | 2506.07001 | 87.88% avg TPR drop; 98.96% vs Fast-DetectGPT | Detector-guided \(|P(s)|\) search |
| TempParaphraser | EMNLP 2025 | 82.5% avg accuracy reduction | Sampling diversity as paraphrase |
| StealthRL | 2602.08934 | 97.6% ASR, AUROC 0.79→0.43 | RL learns TV-reducing edits |
| GradEscape | 2506.08188 | 139M beats 11B DIPPER | Gradient paraphrase |
| DAMAGE | COLING 2025 | 19 commercial humanizers audited | Industry scale of paraphrase evasion |

### 6.4 Watermark cryptography (partial escape hatch)

Christ, Gunn & Zamir (COLT 2024, arXiv:2306.09194): computationally undetectable watermarks exist under cryptographic assumptions. **Not** a refutation of Sadasivan for unwatermarked text. SIRA (ICML 2025, arXiv:2505.05190) then shows ~100% watermark removal via high-entropy token rewrite at $0.88/M tokens — re-grounding the empirical attack surface.

---

## 7. Educator and policy impact

### 7.1 What Sadasivan changed in the discourse

Before Sadasivan: detectors treated as engineering problems ("train a better classifier"). After: **adversarial paraphrase + TV bound** became the default citation for "detectors are fragile." OpenAI withdrew its public classifier July 2023. Vanderbilt disabled Turnitin AI detection Aug 2023 citing false-positive risk.

### 7.2 Institutional responses (2023–2026)

| Institution / source | Action | Sadasivan relevance |
|---------------------|--------|---------------------|
| Vanderbilt (Aug 2023) | Disabled Turnitin AI detector | Cites unreliable detection + equity |
| Weber-Wulff et al. (IJETHE 2024) | Bypass techniques + inclusive education | Cites Sadasivan among limitation papers |
| CASRAI / USD Legal guides (2024–2026) | Score = inquiry prompt, not proof | Cites Sadasivan impossibility |
| Springer *Educational Integrity* (2026) | Threshold bands 0–20/21–79/80+ | Acknowledges detector unreliability |
| Turnitin (2024–2026) | Holds FP < 1%; accepts ~15% FN | Explicit tradeoff: won't flag ambiguous human text |
| EU AI Act Art. 50 (effective Aug 2026) | Mandatory marking for GenAI | Shifts burden to provenance/watermark — Sadasivan's paraphrase corollary applies |

### 7.3 Equity coupling (Liang + Sadasivan)

Liang et al. (Patterns 2023, arXiv:2304.02819): >61% FPR on TOEFL essays. The **same** "enhance word choices" prompt that fixes ESL false positives also evades detectors — Sadasivan's TV reduction via register shift. Policy implication: detectors punish constrained registers **and** are bypassed by register elevation. Humanizers that polish ESL prose occupy an ethically ambiguous zone unslop documents in Boundaries.

### 7.4 Recommended policy posture (aligned with paper's own conclusion)

Sadasivan's closing argument: deploying unreliable detectors causes **more harm than good** when FPR is socially concentrated. Consensus emerging:

1. Never sole evidence for misconduct
2. Human review mandatory
3. Disclose detector version and language
4. Prefer process integrity (drafts, oral defense) over post-hoc classification
5. Treat paraphrase-capable LLMs as assumed attacker capability

**URLs:**
- Weber-Wulff bypass paper: https://link.springer.com/article/10.1186/s41239-024-00487-w
- Liang ESL bias: https://arxiv.org/abs/2304.02819
- CASRAI accuracy guide: https://casrai.org/guides/ai-detection-accuracy-higher-education
- Educational Integrity 2026 eval: https://link.springer.com/article/10.1007/s40979-026-00213-1

---

## 8. Unslop framing: TV-reduction vs single-detector score chasing

### 8.1 The distinction

| Strategy | Mechanism | Durability | Ethical posture |
|----------|-----------|------------|-----------------|
| **TV-reduction** | Remove AI-isms, inject human register variance, widen surprisal rhythm, add user-specific anchors | Moves \(\mathcal{M} \rightarrow \mathcal{H}\) on multiple axes; survives detector updates better | Defensible for ESL false-positive defense, voice restoration, slop removal |
| **Score chasing** | Iteratively rewrite until GPTZero/TMR/Originality score drops | Arms race; overfits one detector version; may homogenize text oddly | Indistinguishable from bypass tools; stale after vendor retrain |

Sadasivan proves score chasing has a **ceiling** set by TV. Chasing one API optimizes a lagging indicator. TV-reduction attacks the distribution directly.

### 8.2 How unslop already implements TV-reduction

| unslop component | TV-reduction mechanism | Sadasivan / follow-on basis |
|------------------|------------------------|----------------------------|
| `humanize.py` deterministic pass | Strip stock vocab, hedging, sycophancy, em-dash pileups | Removes high-probability LLM register markers |
| `anti-detector` mode (`SKILL.md` §84–98) | Burstiness σ≥6, structural variation, contractions, specificity, rough edges | DivEye surprisal variance; Paneru contraction rate |
| `stylometry.py` | `sentence_length_cv`, `word_length_stdev` | DivEye proxies |
| `surprisal.py` (`--surprisal-variance`) | Real per-token surprisal stdev via distilgpt2 | DivEye target metric |
| `detector.py` feedback ladder | Deterministic passes first; cross-model paraphrase recommendation when exhausted | TempParaphraser, Adversarial Paraphrasing, DIPPER pattern |
| Boundaries in SKILL.md | Anti-detector for false-positive defense; not academic misconduct | Matches Sadasivan "unreliable detector" warning |

### 8.3 What unslop should **not** do (per Sadasivan + policy)

1. **Market as "beat Turnitin"** — vendor retrains on humanizer outputs (Aug 2025); single-score optimization is stale on arrival.
2. **Treat TMR probability as success metric alone** — benchmark README already notes deterministic pass moves TMR by 0.1–0.2pp; aligns with Sadasivan (surface edits ≠ distributional shift).
3. **Skip retrieval caveat** — Krishna retrieval defense recovers provenance regardless of paraphrase if provider logs exist.
4. **Watermark removal** — EU AI Act Art. 50; Sadasivan paraphrase corollary applies but deliberate scrubbing is separate legal/ethical violation.

### 8.4 Recommended unslop messaging (August 2026)

> unslop removes the statistical signatures that make LLM text **detectably non-human** — stock phrases, uniform rhythm, zero contractions, performative balance. That is TV-reduction: sound like yourself, not like a detector's inverse. Optimizing one detector score is a bypass arms race Sadasivan proved is bounded. unslop's primary job is **quality and voice**, not evasion. Anti-detector mode exists for ESL false-positive defense and register restoration, with `--surprisal-variance` as the DivEye-aligned measurement hook.

### 8.5 Code touchpoints for UPDATE-PLAN

From `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md`:

- Wire `anti-detector` into detector feedback ladder (currently reaches deterministic passes only)
- Log surprisal CV alongside TMR in `--detector-feedback` runs
- Refresh SKILL.md landscape paragraph (already cites DivEye, Turnitin Aug 2025, SIRA)
- Dual benchmark: in-domain TMR + surprisal variance delta (TV proxy), not TMR alone

---

## 9. Open problems (August 2026)

1. **Adaptive paraphrase vs DivEye:** No public benchmark of recursive DIPPER specifically against DivEye + XGBoost stack.
2. **TV estimation at scale:** Sadasivan's Figure 8 uses RoBERTa TV estimates on GPT-2 era models; no public TV tracker for GPT-4o/Claude/Gemini class outputs.
3. **Operating-point reporting:** Most post-Sadasivan papers report AUROC, not TPR@1%FPR — the metric Sadasivan argues matters for integrity.
4. **Humanizer-trained detectors:** Turnitin Aug 2025, DAMAGE augmentation — shifts \(\mathcal{H}\) detection boundary; TV between *humanizer output* and *human* is the new relevant gap.
5. **Regulatory vs academic threat models:** EU Art. 50 assumes watermark provenance; Sadasivan + SIRA assume paraphrase strips it.

---

## 10. Source index

### Primary

| Resource | URL |
|----------|-----|
| Sadasivan et al. (main) | https://arxiv.org/abs/2303.11156 |
| Sadasivan HTML v4 | https://arxiv.org/html/2303.11156v4 |
| Sadasivan appendix (tightness proof) | https://arxiv.org/html/2303.11156v4 (Appendix A) |

### Theoretical debate

| Resource | URL |
|----------|-----|
| Chakraborty et al. — possibility | https://arxiv.org/abs/2304.04736 |
| Christ–Gunn–Zamir — undetectable watermarks | https://arxiv.org/abs/2306.09194 |

### Paraphrase / DIPPER lineage

| Resource | URL |
|----------|-----|
| Krishna et al. — DIPPER | https://arxiv.org/abs/2303.13408 |
| DIPPER repo | https://github.com/martiansideofthemoon/ai-detection-paraphrases |
| Kirchenbauer watermark (attacked) | https://arxiv.org/abs/2301.10226 |
| DetectGPT (attacked) | https://arxiv.org/abs/2301.11305 |

### Later detectors (post-Sadasivan debate)

| Resource | URL |
|----------|-----|
| DivEye (TMLR 2026) | https://arxiv.org/abs/2509.18880 |
| DivEye code | https://github.com/IBM/diveye |
| Fast-DetectGPT | https://arxiv.org/abs/2310.05130 |
| Binoculars | https://arxiv.org/abs/2401.12070 |
| AdaDetectGPT | https://arxiv.org/abs/2510.01268 |
| Adversarial Paraphrasing | https://arxiv.org/abs/2506.07001 |
| TempParaphraser (EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1607 |
| StealthRL | https://arxiv.org/abs/2602.08934 |
| SIRA watermark attack | https://arxiv.org/abs/2505.05190 |

### Equity / policy

| Resource | URL |
|----------|-----|
| Liang ESL bias | https://arxiv.org/abs/2304.02819 |
| Weber-Wulff bypass + inclusion | https://link.springer.com/article/10.1186/s41239-024-00487-w |
| Educational Integrity detector eval 2026 | https://link.springer.com/article/10.1007/s40979-026-00213-1 |
| CASRAI false-positive evidence | https://casrai.org/guides/ai-detection-accuracy-higher-education |

### unslop internal

| Resource | Path |
|----------|------|
| Cat 05 synthesis | `docs/research/05-ai-text-detection-and-evasion/SYNTHESIS.md` |
| Cat 15 humanization survey | `docs/research/15-academic-papers-llm-humanization/A-academic.md` |
| Implementation trace | `docs/research/IMPLEMENTATION_TRACE.md` |
| anti-detector spec | `skills/unslop/SKILL.md` |
| surprisal module | `unslop/scripts/surprisal.py` |
| detector feedback | `unslop/scripts/detector.py` |

---

## 11. Verdict for manifest

**Agent #17 status:** ✅ complete  
**Confidence:** High on paper claims (primary source verified); medium on DivEye-vs-recursive-DIPPER gap (no direct ablation found)  
**Feeds:** `UPDATE-PLAN-2026-08.md` Part 1 (theoretical foundation row), SKILL.md anti-detector landscape, `benchmarks/README.md` TMR limitation framing
