# Agent #35 — Cross-Model Paraphrase as Practitioner Technique

**Topic:** GPT → Claude → Gemini rewrite chains (and variants) as the dominant practitioner humanization workflow  
**Scope:** Academic evidence (TempParaphraser, Adversarial Paraphrasing, DAMAGE, DIPPER, HIP, Sadasivan), practitioner blogs/HN, why cross-model beats single-model humanization, limits, unslop `detector.py` ladder-exhaustion message  
**Status:** Complete  
**Date:** 2026-08-19

---

## Executive summary

Cross-model paraphrase — running AI text through one or more LLMs from **different families** (e.g. GPT → Claude → Gemini) — is the strongest **practitioner-accessible** lever for shifting detector scores. It is not a hack unique to bypass forums; it is the operational form of a line of peer-reviewed work showing that **paraphrase reshapes the output distribution** away from generator-specific fingerprints.

Single-model humanization (same-family polish, regex strips, SaaS humanizers) mostly edits **surface tokens** while leaving **distributional geometry** intact. TempParaphraser (EMNLP 2025) reports **82.5% average reduction in detector accuracy** via multi-sample sentence paraphrase. Adversarial Paraphrasing (NeurIPS 2025) reports **87.88% average T@1%F reduction** across eight detectors when paraphrase is detector-guided — and notes that naive paraphrase can *increase* detection on modern detectors. DAMAGE (GenAIDetect / COLING 2025) audited **19 commercial humanizers** and showed GPTZero TPR collapsing **99.73% → 60.04%** on humanized academic text; individual tools varied by 20–100 points on the same input.

unslop encodes this honestly: deterministic passes (`balanced` → `full` → `full + structural + soul`) move TMR by ~**0.0–0.2 pp** on fixtures. When the `--detector-feedback` ladder exhausts, `detector.py` prints a **structured cross-model recommendation** naming TempParaphraser and Adversarial Paraphrasing — the single strongest documented next step the product cannot execute inside one session.

**Bottom line for unslop:** Items 2–5 (burstiness, structure, contractions, specificity) are prep work. Item 1 (cross-model rewrite) is the capstone. Document both; never imply regex alone defeats RAID-grade detectors.

---

## 1. What practitioners mean by “cross-model paraphrase”

### 1.1 Canonical workflow

| Step | Action | Rationale |
|------|--------|-----------|
| 0 | Generate with Model A (often GPT or Claude) | Initial draft carries Model A's instruction-tuning artifacts |
| 1 | Rewrite with Model B from a **different family** | Breaks tokenizer + RLHF + stylistic priors of A |
| 2 (optional) | Second rewrite with Model C | Further TV reduction; chain length 2–3 is common in forums |
| 3 | Manual pass | Restore numbers, names, citations paraphrase mangled |
| 4 (optional) | Run unslop anti-detector locally | Burstiness / contractions after structural rewrite |

**Family boundaries that matter:** OpenAI (GPT) ↔ Anthropic (Claude) ↔ Google (Gemini) ↔ Meta (Llama). Same-family “polish” (GPT-4 → GPT-4 with a humanize prompt) removes vocabulary tells but **preserves family-level perplexity curvature** — exactly what Binoculars, Fast-DetectGPT, and DivEye read.

### 1.2 Related practitioner patterns

- **Chain-of-models:** GPT draft → Claude rewrite → Gemini final pass (order varies; principle is family diversity).
- **Human-in-the-loop editor:** One model for analysis, another for prose (common in HN “personal editor” comments).
- **SaaS humanizer as single hop:** Undetectable.ai, StealthGPT, etc. — functionally a black-box cross-model or fine-tuned paraphraser, but with opaque quality and month-to-month detector drift (DAMAGE, Chicago Booth 2025/2026).
- **Detector-guided rewrite:** Paste into tool that scores each variant (Adversarial Paraphrasing formalizes this; practitioners approximate by regenerating until GPTZero turns green).

### 1.3 What it is *not*

- Synonym swap / QuillBot light mode alone (Adversarial Paraphrasing: can **raise** T@1%F on RADAR/Fast-DetectGPT).
- Stock-vocab stripping without structural change (HLD-Detector: lexical layer breaks under paraphrase; POS/dep/semantic layers hold).
- Watermark removal (EU AI Act Art. 50 — unslop explicitly prohibits recommending this in ladder message).

---

## 2. Academic evidence

### 2.1 TempParaphraser (EMNLP 2025) — temperature simulation via paraphrase

**Citation:** Huang, Zhang, Su & Chen, *TempParaphraser: "Heating Up" Text to Evade AI-Text Detection through Paraphrasing*, EMNLP 2025.

| Field | Detail |
|-------|--------|
| Core idea | High-temperature sampling flattens token entropy and breaks detectors; raw high-T hurts quality. TempParaphraser **simulates** high-T effects via **multiple normal-T paraphrase candidates** at sentence level (Jensen's inequality argument). |
| Headline result | **82.5% average reduction in detector accuracy** while preserving quality |
| Model independence | Framework operates **independently of the original generation model** — direct analog to “rewrite in a different model” |
| Paraphraser diversity | Table 9: multiple fine-tuned paraphrase backbones all reduce detection — **diverse paraphrasing models** evade effectively |

**URLs:**
- Paper (ACL): https://aclanthology.org/2025.emnlp-main.1607/
- PDF: https://aclanthology.org/2025.emnlp-main.1607.pdf
- DOI: https://doi.org/10.18653/v1/2025.emnlp-main.1607
- Code: https://github.com/HJJWorks/TempParaphraser

**unslop link:** Cited verbatim in `detector.py` ladder-exhaustion `reason_stopped` string and SKILL anti-detector step 6.

---

### 2.2 Adversarial Paraphrasing (NeurIPS 2025) — detector-guided paraphrase ceiling

**Citation:** Cheng, Chakraborty, Krishna & Jurafsky, *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text*, NeurIPS 2025.

| Field | Detail |
|-------|--------|
| Method | Training-free. Instruction LLM (e.g. LLaMA-3-8B-Instruct) paraphrases while a **detector scores each candidate token**; pick min-AI-score continuation. |
| vs naive paraphrase | Simple paraphrase **increases** T@1%F by **+8.57%** (RADAR) and **+15.03%** (Fast-DetectGPT) — modern detectors punish shallow rewrite |
| Guided results | OpenAI-RoBERTa-Large guidance: **−64.49%** T@1%F (RADAR), **−98.96%** (Fast-DetectGPT); **−87.88% average** across 8 detectors |
| Transferability | Attack transfers across detector families — strong detectors converge on similar human-text target |
| Quality tradeoff | Mostly slight degradation; attack success dominates |

**URLs:**
- arXiv: https://arxiv.org/abs/2506.07001
- NeurIPS PDF: https://proceedings.neurips.cc/paper_files/paper/2025/file/443f314cd420ce621b6e748fd1194ed8-Paper-Conference.pdf
- OpenReview: https://openreview.net/forum?id=fYjF9KIJd5
- Code: https://github.com/chengez/Adversarial-Paraphrasing

**Practitioner implication:** Cross-model rewrite **without** detector feedback is a blind version of this attack. Cross-model **with** regenerate-until-green is the manual approximation. unslop's deterministic ladder is explicitly **not** detector-guided at token level.

---

### 2.3 DAMAGE (GenAIDetect / COLING 2025) — commercial humanizer audit

**Citation:** Masrour, Emi & Spero, *DAMAGE: Detecting Adversarially Modified AI Generated Text*, GenAIDetect @ COLING 2025.

| Field | Detail |
|-------|--------|
| Scope | **19 AI humanizer / paraphrasing tools** qualitatively graded (L1/L2/L3 fluency taxonomy) |
| Detector collapse | GPTZero TPR @ 5% FPR: **99.73% → 60.04%** on humanized AI academic text; Binoculars **94.15% → 28.23%** |
| DAMAGE defender | Data-centric augmentation; **98.26%** TPR on humanized text @ 5% FPR; **93.0%** on RAID paraphrase attacks |
| Adaptive attack | GPT-4o fine-tuned humanizer optimized against DAMAGE still **93.2%** detected at default threshold — paraphrase leaves residual patterns |
| Industry scale | Documents that humanization-as-a-service is a real adversary class, not a niche |

**URLs:**
- ACL: https://aclanthology.org/2025.genaidetect-1.9/
- PDF: https://aclanthology.org/2025.genaidetect-1.9.pdf
- arXiv: https://arxiv.org/abs/2501.03437

**unslop link:** `detector.py` module docstring cites DAMAGE as justification for live `--detector-feedback` loop vs trusting SaaS marketing.

---

### 2.4 DIPPER (NeurIPS 2023) — paraphrase as universal solvent (lineage)

**Citation:** Krishna et al., *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense*, NeurIPS 2023.

| Result | Detail |
|--------|--------|
| DetectGPT | **70.3% → 4.6%** TPR @ 1% FPR after DIPPER |
| Targets | Watermarking, GPTZero, DetectGPT, OpenAI classifier |
| Recursive DIPPER | 5 rounds + detector-guided selection → DetectGPT AUROC **82% → 18%** |
| Defense | Provider-side retrieval of logged generations (97.3% recovery on some settings) |

**URLs:**
- arXiv: https://arxiv.org/abs/2303.13408
- NeurIPS PDF: https://proceedings.neurips.cc/paper_files/paper/2023/file/575c450013d0e99e4b0ecf82bd1afaa4-Paper-Conference.pdf
- Code: https://github.com/martiansideofthemoon/ai-detection-paraphrases
- Model: https://huggingface.co/kalpeshk2011/dipper-paraphraser-xxl

**Cross-model connection:** DIPPER is a **specialized paraphraser** (11B, task-tuned). Practitioner cross-model chains approximate DIPPER's distribution shift without hosting DIPPER — different foundation model = different paraphrase manifold.

---

### 2.5 HIP — Base Models Look Human (2026) — why family swap works on commercial detectors

**Citation:** *Base Models Look Human To AI Detectors* (HIP pipeline), arXiv:2605.19516.

| Finding | Detail |
|---------|--------|
| Commercial detectors | GPTZero/Pangram rate **base-model** continuations **96.7–98.8% human** vs **17–30% human** for instruct-tuned same backbone |
| Mechanism | Detectors track **instruction-tuning artifacts**, not invariant “machine-ness” |
| HIP | Iterative paraphrase via lightly fine-tuned base model; SOTA evasion/semantics tradeoff on **commercial** detectors |
| Implication | Rewriting through a **different generative prior** (another family, or base-style paraphrase) moves the instruct-tuning fingerprint |

**URLs:**
- arXiv: https://arxiv.org/abs/2605.19516
- HTML: https://arxiv.org/html/2605.19516

---

### 2.6 Sadasivan et al. (2023) — theoretical frame: paraphrase reduces TV distance

**Citation:** Sadasivan et al., *Can AI-Generated Text be Reliably Detected?*, arXiv:2303.11156.

| Claim | Detail |
|-------|--------|
| TV bound | Best detector AUROC bounded by **Total Variation** between human and machine distributions |
| Paraphrase | Light paraphrasers (T5 222M, PEGASUS 568M) break watermark and zero-shot detectors |
| High-stakes impossibility | TPR 90% @ FPR 1% impossible when distributions overlap > ~11% |
| Recursive paraphrase | Multi-round paraphrase + selection → retrieval defense drops to **25%** |

**URLs:**
- arXiv: https://arxiv.org/abs/2303.11156
- Code: https://github.com/vinusankars/Reliability-of-AI-text-detectors

**Cross-model framing:** Each model family defines a different machine distribution **M**. Paraphrase through family B maps **M_A → M_B**, shrinking effective TV vs **H** (human) along axes family-A detectors trained on.

---

## 3. Why cross-model beats single-model humanization

| Dimension | Single-model (same family / regex / SaaS) | Cross-model chain |
|-----------|-------------------------------------------|-------------------|
| **Signal targeted** | Stock vocab, em-dashes, bullet uniformity (Signal 1) | Token entropy, perplexity curvature, syntactic POS/dep, semantic KDE (Signals 2–4) |
| **Generator logits** | Preserved — DetectGPT/Binoculars still see A's manifold | New model re-samples from B's conditional distributions |
| **Instruction-tuning fingerprint** | Partially preserved (HIP: instruct text flags non-human) | Different RLHF/DPO steering stack |
| **Empirical ceiling** | Adversarial Paraphrasing: naive paraphrase **hurts** on RADAR/Fast-DetectGPT | TempParaphraser −82.5% avg accuracy; AdvPara −87.88% avg T@1%F |
| **unslop bench** | TMR moves **<0.5 pp** after full deterministic ladder | Documented as manual step; only path that moves consumer detector screenshots |
| **Cost** | Low (local regex) or subscription SaaS | Multiple API calls + human verification |
| **Meaning preservation** | Higher for light edits | Risk of fact drift; numbers/names need manual restore |

### 3.1 Mechanism stack (why one pass isn't enough)

1. **Lexical layer** — “delve”, tricolon, hedging (regex / subtle mode). Detectors trained post-2024 weight this least.
2. **Structural layer** — sentence-length σ, parallel bullets (structural.py). Moves some commercial scores; insufficient vs TMR/HLD semantic KDE.
3. **Distribution layer** — surprisal variance, cross-perplexity (DivEye, Binoculars). Requires **resampling**, not substitution.
4. **Cross-model capstone** — full semantic reconstruction through another family's autoregressive process. Closest manual equivalent to TempParaphraser + blind Adversarial Paraphrasing.

### 3.2 Why SaaS humanizers underperform chains

DAMAGE: 19 tools, **20–100 point spread** on same input vs GPTZero. Chicago Booth 2025/2026: StealthGPT humanization — GPTZero FNR **~50%+** (often fails to detect), but Pangram stays robust; median commercial humanizer effect **~6 pp** not **40+**. Practitioner chains with **explicit family swap + manual edit** outperform opaque SaaS because the user controls semantics and can iterate.

---

## 4. Practitioner sources (blogs, forums, industry)

### 4.1 Hacker News (selected threads)

| Thread | URL | Relevant claim |
|--------|-----|----------------|
| Ask HN: How detect LLM text? | https://news.ycombinator.com/item?id=47659807 | Detectors use word distributions; tells suppressible; pattern-matching fragile |
| AI detectors do not work | https://news.ycombinator.com/item?id=41901653 | RLHF style is design choice; open-source can mimic human; “battle is lost” for naive detection |
| How to Spot AI Writing | https://news.ycombinator.com/item?id=49134310 | Detect **re-written** AI, not just generated; AI-as-editor blurs line |
| Detecting LLM with classical ML | https://news.ycombinator.com/item?id=48936880 | Changing LLM pattern via prompting breaks classifiers; distillation footprints overlap |
| Show HN: BypassGPT | https://news.ycombinator.com/item?id=45011938 | Commercial humanizer = AI rewriting AI (irony noted) |

**Consensus shape:** Motivated users defeat detectors via **rewrite + edit**. HN rarely documents rigorous benchmarks; academic papers fill that gap.

### 4.2 Practitioner blogs / SEO humanizer sites

| Source | URL | Claim (treat as marketing unless replicated) |
|--------|-----|---------------------------------------------|
| HumanizeThisAI strategy post | https://humanizethisai.com/md/blog/pass-all-ai-detectors.md | Single-vector edits fail; “semantic reconstruction” needed; model-specific detectors (Originality tuned to humanizer output) |
| unslop README (honest version) | [README FAQ](../../../README.md#faq) | Ordered levers: cross-model > burstiness > specificity > contractions > structure |
| Chicago Booth Review | https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust | Policy-cap framework; humanizer arms race; Pangram vs GPTZero under StealthGPT |
| BFI working paper | https://doi.org/10.3386/w34223 | GPT-4.1, Claude Opus/Sonnet 4, Gemini 2.0 Flash corpus; humanizer robustness varies by detector |

### 4.3 Turnitin / vendor arms race (context)

- Turnitin **August 2025:** explicit anti-humanizer / “AI-paraphrased” category — pre-Aug 2025 bypass stats stale.
- Turnitin **February 2026:** recall update, FP <1% claimed.
- **Implication:** Cross-model chains remain effective but **detector-specific**; a chain that greens GPTZero may still flag Turnitin Originality.ai.

---

## 5. Limits and failure modes

| Limit | Detail |
|-------|--------|
| **Fact drift** | Each paraphrase hop can corrupt numbers, dates, citations. Manual restore mandatory for high-stakes text. |
| **Not durable vs retrieval** | Krishna et al.: provider logs + semantic retrieval recover provenance regardless of paraphrase. |
| **Detector-specific outcomes** | Chicago Booth: Pangram robust to StealthGPT; GPTZero FNR ~50%+. One green check ≠ universal pass. |
| **ESL false positives** | Liang et al. (Patterns 2023): >50% TOEFL essays flagged — cross-model rewrite is false-positive **defense**, not cheating tool (unslop boundary). |
| **Adaptive defenders** | DAMAGE detector, HLD semantic KDE, Turnitin anti-humanizer — paraphrase arms race continues; no permanent pass. |
| **Watermark ethics** | EU AI Act Art. 50 — ladder message explicitly says do NOT remove watermarks. |
| **Same-family polish ceiling** | HIP: instruct-tuned outputs remain machine-like to GPTZero; polishing in-family has low ceiling. |
| **Quality tax** | StealthRL / high-aggression paraphrase: quality Likert drops; PPL spikes. Cross-model chains need light prompts (“preserve meaning, vary syntax”). |
| **Length / genre** | Chicago Booth: ultra-short passages degrade all detectors; résumé bullets harder than long-form blog. |
| **unslop cannot orchestrate** | Agent skill boundary — user must run cross-model pass explicitly; product prints recommendation only. |

---

## 6. unslop integration: `detector.py` ladder exhaustion message

### 6.1 Escalation ladder (deterministic)

```278:281:unslop/scripts/detector.py
DEFAULT_LADDER: list[tuple[str, bool, bool]] = [
    ("balanced", False, False),
    ("full", False, False),
    ("full", True, True),
]
```

Aggressive ladder (`--detector-loop-aggressive`): 5 steps from `subtle` through `full + structural + soul`.

### 6.2 Exhaustion message (strongest product lever)

When all ladder steps fail to reach `target_probability`, `feedback_loop` returns:

```399:407:unslop/scripts/detector.py
    recommendation = (
        f"ladder exhausted after {len(iterations)} iteration(s); "
        f"target {target} not reached (final p_ai={final_prob:.3f}). "
        "Next step is outside this module: paraphrase the text through a "
        "different model family (e.g. if generated by GPT, rewrite via Claude "
        "or Gemini). TempParaphraser (EMNLP 2025) and Adversarial Paraphrasing "
        "(NeurIPS 2025) document this as the single most reliable detector-"
        "evasion lever. Do NOT attempt watermark removal — EU AI Act Article 50 "
        "prohibits it."
    )
```

### 6.3 CLI surfacing

`unslop --detector-feedback file.md` prints to stderr:

```
detector: 87.3% → 86.9% (ladder exhausted after 3 iteration(s); target 0.5 not reached ...)
```

JSON mode exposes full string in `detector_feedback.reason_stopped`.

### 6.4 SKILL alignment

`skills/unslop/SKILL.md` anti-detector step 6 mirrors the same recommendation — cross-family second pass, TempParaphraser 82.5% figure, notes skill **cannot execute alone**.

### 6.5 Why this message is the strongest lever

1. **Honesty as differentiation** — Admits deterministic humanization doesn't beat TMR; matches NeurIPS 2025 prediction for surface rewrite.
2. **Actionable next step** — Names concrete workflow (GPT→Claude/Gemini), not “buy Undetectable.ai.”
3. **Research-backed** — TempParaphraser + Adversarial Paraphrasing citations give users and auditors a paper trail.
4. **Boundary clarity** — Watermark removal explicitly out of scope (legal).
5. **Measurement hook** — User can re-run `--detector-feedback` after cross-model pass to see if TMR moved (expected: larger delta than ladder alone).

### 6.6 Known gaps (UPDATE-PLAN-2026-08)

- `anti-detector` mode **not yet in ladder** — loop stops at `full + structural + soul` only.
- No automated cross-model orchestration (Phase 3: `llm_pipeline.py` planned).
- TempParaphraser 82.5% is **average across detectors/datasets** — not a TMR guarantee.

---

## 7. Recommended practitioner protocol (unslop-aligned)

For users in `/unslop anti-detector` or post-ladder-exhaustion:

1. Run unslop deterministic passes (or `--detector-feedback`) — fixes slop, burstiness, contractions.
2. **Cross-model rewrite:** prompt Model B: *“Rewrite for clarity. Preserve all facts, numbers, names, citations verbatim. Vary sentence length and structure. No filler.”*
3. Optional Model C pass if detector still high on consumer tool that matters.
4. Manual fact check — restore any mangled specifics.
5. Re-score with target detector (and keep drafts for false-positive defense).

**Chain length:** Diminishing returns after 2–3 hops; meaning drift dominates.

---

## 8. Debate summary

| Camp | Argument | Best source |
|------|----------|-------------|
| **Detection pessimists** | Paraphrase + TV bound → detectors structurally fragile | Sadasivan 2023; Nicks ICLR 2024 |
| **Detection optimists** | Augmented defenders (DAMAGE, HLD, Pangram) survive paraphrase | DAMAGE 2025; Chicago Booth 2026 |
| **Practitioners** | Family swap + edit beats SaaS; cat-and-mouse continues | HN threads; DAMAGE 19-tool audit |
| **unslop position** | Polish layer + honest escalation; cross-model is user-orchestrated capstone | detector.py, README FAQ |

---

## 9. URL index (all cited)

### Papers
- TempParaphraser EMNLP 2025: https://aclanthology.org/2025.emnlp-main.1607/
- Adversarial Paraphrasing NeurIPS 2025: https://arxiv.org/abs/2506.07001
- DAMAGE GenAIDetect 2025: https://aclanthology.org/2025.genaidetect-1.9/
- DIPPER NeurIPS 2023: https://arxiv.org/abs/2303.13408
- Sadasivan impossibility 2023: https://arxiv.org/abs/2303.11156
- HIP / Base Models Look Human 2026: https://arxiv.org/abs/2605.19516
- Liang TOEFL false positives 2023: https://arxiv.org/abs/2304.02819
- DivEye surprisal variance TMLR 2026: https://arxiv.org/abs/2509.18880
- HLD-Detector ICLR 2026: (see AGENT-14-HLD.md in this folder)

### Code
- TempParaphraser: https://github.com/HJJWorks/TempParaphraser
- Adversarial Paraphrasing: https://github.com/chengez/Adversarial-Paraphrasing
- DIPPER: https://github.com/martiansideofthemoon/ai-detection-paraphrases
- Sadasivan: https://github.com/vinusankars/Reliability-of-AI-text-detectors

### Practitioner / industry
- Chicago Booth Review: https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust
- BFI WP 2025-116: https://doi.org/10.3386/w34223
- RAID benchmark leaderboard: https://raid-bench.xyz/leaderboard
- HN Ask detect LLM: https://news.ycombinator.com/item?id=47659807
- HN AI detectors do not work: https://news.ycombinator.com/item?id=41901653

### unslop internals
- `unslop/scripts/detector.py` — ladder + exhaustion message
- `skills/unslop/SKILL.md` — anti-detector step 6
- `README.md` FAQ “Will it hide my text from AI detectors”
- `drafts/2026-05-detector-test/ARTICLE.md` — TMR vs consumer detector honesty

---

## 10. unslop integration recommendations

| Priority | Action | Rationale |
|----------|--------|-----------|
| P0 | Keep ladder-exhaustion message verbatim in sync across SSOT + mirrors | Strongest honest conversion moment |
| P1 | Add `anti-detector` to feedback ladder (UPDATE-PLAN Phase 1) | Currently unreachable in loop |
| P2 | Post-cross-model re-score UX: `--detector-feedback` docs should show before/after workflow | Closes measurement loop |
| P3 | Phase 3 `llm_pipeline.py`: optional cross-model prompt templates (S5 capstone) | Automate what skill cannot |
| Doc | May detector-test article: cite cross-model as reason rule-only TMR delta ≈ 0 | Already drafted in ARTICLE.md |

---

*Agent #35 complete. Cross-model paraphrase is practitioner technique #1, academically licensed, product-honest via detector.py exhaustion message.*
