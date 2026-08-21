# Agent #60 — Pangram vs GPTZero on Paraphrase / Humanized Text

**Topic:** Head-to-head commercial detector divergence under paraphrase, humanizer SaaS, and StealthGPT — DAMAGE authors (Pangram Labs) vs independent Chicago Booth audit vs GPTZero rebuttal  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh  
**Cross-refs:** Agent #40 (DAMAGE tiers), Agent #35 (cross-model paraphrase), Agent #22 (HIP), UPDATE-PLAN-2026-08.md § Phase 4 dual reporting

---

## Executive summary

On **raw AI text**, Pangram and GPTZero both score well in independent work. Under **paraphrase and commercial humanization**, they diverge sharply — and the gap is now one of the most cited facts in the 2025–2026 detector arms race.

Three independent lines of evidence converge:

1. **DAMAGE** (Masrour, Emi & Spero, COLING 2025 — Pangram Labs): GPTZero TPR @ FPR=5% drops **99.73% → 60.04%** on humanized academic essays across 19 tools; Pangram's production model (post-humanizer training) holds **~97%** on humanized text vs **~46%** for GPTZero in the Russell et al. panel cited on Pangram's blog.
2. **Chicago Booth** (Jabarian & Imas, NBER w34223, Sept 2025): StealthGPT (DAMAGE L1 humanizer) pushes GPTZero FNR to **~50%+** across genres; Pangram FNR stays low. Only Pangram meets a **0.5% FPR policy cap** without sacrificing recall.
3. **GPTZero rebuttal** (Jan 2026): Booth used `average_generated_prob` instead of `class_probabilities` / `predicted_class`; GPTZero claims **99.3% recall** and **99.5% accuracy** on a corrected re-run of the same corpus — but does **not** re-litigate the StealthGPT humanizer arm or Pangram's humanizer-trained variant.

**unslop takeaway:** A green GPTZero check after cross-model paraphrase is **not** equivalent to a green Pangram check. unslop's `detector.py` uses TMR (GPTZero-family signal) as one input, not a gate. Any benchmark or README claim must follow **dual reporting**: consumer detector screenshots *and* academic ensemble metrics. Never cite single-detector "100% pass."

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **DAMAGE paper (arXiv)** | https://arxiv.org/abs/2501.03437 |
| **DAMAGE paper (ACL Anthology)** | https://aclanthology.org/2025.genaidetect-1.9/ |
| **DAMAGE paper (HTML)** | https://arxiv.org/html/2501.03437v1 |
| **Pangram technical report (Jan 2025)** | https://arxiv.org/abs/2402.14873 |
| **Pangram humanizer update (Aug 2025)** | https://www.pangram.com/blog/humanizers-aug-25 |
| **Pangram 4 technical report (2026)** | https://arxiv.org/html/2607.27183 |
| **Russell et al. — Human Detectors (ACL 2025)** | https://arxiv.org/abs/2501.15654 |
| **Russell et al. — ACL Anthology PDF** | https://aclanthology.org/2025.acl-long.267.pdf |
| **Russell dataset + detector outputs (GitHub)** | https://github.com/jenna-russell/human_detectors |
| **Jabarian & Imas — NBER w34223** | https://doi.org/10.3386/w34223 |
| **Jabarian & Imas — BFI working paper PDF** | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| **Chicago Booth Review lay summary** | https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust |
| **BFI insight page** | https://bfi.uchicago.edu/insights/artificial-writing-and-automated-detection/ |
| **GPTZero Booth rebuttal (Jan 2026)** | https://gptzero.me/news/chicago-booth-2026/ |
| **GPTZero vs Pangram v3.2 live bench** | https://gptzero.me/news/how-does-gptzero-compare-to-pangram-v3-2-latest-benchmark-results/ |
| **GPTZero API interpretation docs** | https://support.gptzero.me/articles/8947054519-how-do-i-use-and-interpret-the-results-from-your-api |
| **Adversarial Paraphrasing (NeurIPS 2025)** | https://arxiv.org/abs/2506.07001 |
| **DIPPER paraphrase attack (NeurIPS 2023)** | https://arxiv.org/abs/2303.13408 |
| **HIP — base models look human (2026)** | https://arxiv.org/abs/2605.19516 |
| **TempParaphraser (EMNLP 2025)** | https://aclanthology.org/2025.emnlp-main.1607/ |
| **RAID benchmark leaderboard** | https://raid-bench.xyz/leaderboard |

---

## 1. Why Pangram and GPTZero are the right pair

Both vendors sit at the center of the paraphrase debate for different reasons:

| Actor | Role in this memo |
|-------|-------------------|
| **Masrour, Emi, Spero (DAMAGE authors)** | Only peer-reviewed audit naming **19 humanizers**; built Pangram's humanizer-augmented training pipeline; published per-tool detection table Aug 2025 |
| **Jabarian & Imas (Chicago Booth)** | Independent academic audit — **no vendor stake**; tests StealthGPT on 1,992-passage corpus; introduces **policy-cap** framework institutions now cite |
| **GPTZero (Tian & Cui)** | Most-installed consumer detector; perplexity/predictability-cone lineage; actively disputes Booth methodology |

The comparison is not "which vendor wins marketing." It is whether **detector-specific paraphrase robustness** exists — which directly affects unslop users who run `--detector-feedback`, ESL false-positive defense workflows, and cross-model second passes.

---

## 2. DAMAGE (Pangram authors) — legacy GPTZero collapse

DAMAGE ([arXiv:2501.03437](https://arxiv.org/abs/2501.03437)) audited 19 humanizers/paraphrasers on academic essays. Table 3 reports TPR @ FPR=5% (bootstrap 1000 iterations):

| Detector | Raw AI text | Humanized AI text | Δ (pp) |
|----------|-------------|-------------------|--------|
| **GPTZero** | 99.73% ± 0.19 | **60.04% ± 1.80** | **−39.7** |
| Binoculars | 94.15% ± 0.88 | 28.23% ± 1.62 | −65.9 |
| LLM baseline | 100.00% | 95.74% ± 0.71 | −4.3 |
| **DAMAGE detector** | 100.00% | **98.26% ± 0.47** | −1.7 |

At **default thresholds** (Table 7): GPTZero humanized TPR collapses to **34.53%**; DAMAGE holds **97.47%**.

On **RAID paraphrase attacks** (Table in §5): GPTZero **64.0%** TPR vs DAMAGE **93.0%**.

**Interpretive notes:**

- DAMAGE tiers (Table 9) rank **fluency**, not bypass. StealthGPT is L1 quality but not the hardest evader once Pangram retrains ([Agent #40](AGENT-40-DAMAGE-HUMANIZER-TIERS.md)).
- DAMAGE trained on **L1 humanizer outputs only** (~0.68% of training set, 18× oversampled). Adversarial GPT-4o humanizer optimized against DAMAGE still detected at **93.2%** — paraphrase leaves residual generator fingerprints.
- Pangram's commercial product inherits this research line; GPTZero in Table 3 is the **pre-humanizer-adaptation** era baseline that Booth and Russell also stress-test.

---

## 3. Russell et al. (ACL 2025) — controlled humanization configs

Russell, Karpinska & Iyyer ([arXiv:2501.15654](https://arxiv.org/abs/2501.15654)) evaluate 300 non-fiction articles across GPT-4o, Claude 3.5 Sonnet, O1-PRO, with **paraphrase** and **prompt-based humanization** arms. Table 2 reports TPR (FPR) per configuration.

**Overall averages (Table 2, middle rows):**

| Detector | Overall TPR (FPR) | Notes |
|----------|-------------------|-------|
| Expert human majority vote | **99.3% (0%)** | 1/300 misclassified |
| **Pangram Humanizers** variant | **99.3% (2.7%)** | Only automatic detector matching experts |
| Pangram base | 96.7% (10%) | |
| **GPTZero** | **85.3% (0.7%)** | Struggles on O1-PRO arms |
| Fast-DetectGPT | ~23% TPR under 5% FPR calibration | Open-source collapse |
| Binoculars | ~7% | |

**O1-PRO HUMANIZED column (hardest config):** expert majority **100%** TPR; Pangram Humanizers **96.7%** (10% FPR on that column); **GPTZero 46.7%** (3.3% FPR). This is the origin of Pangram blog's **97% vs 46%** headline — aggregated across humanized conditions, not a single StealthGPT run.

Russell explicitly compares **Pangram base vs Pangram Humanizers** (trained with DAMAGE-line augmentation). GPTZero has no published equivalent humanizer-specialized public model name, though v6+ adds predictability cones and bypasser categories.

---

## 4. Chicago Booth — StealthGPT stress test (independent)

Jabarian & Imas ([NBER w34223](https://doi.org/10.3386/w34223), [BFI PDF](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)) evaluate Pangram, GPTZero, Originality.ai, and RoBERTa on **1,992 human + 1,992 AI passages** across 6 genres and 4 frontier LLMs (GPT-4.1, Claude Opus 4, Claude Sonnet 4, Gemini 2.0 Flash).

### 4.1 Baseline (no humanizer)

On medium-to-long text, all three commercial detectors achieve low FPR (≤1%) and low FNR. Pangram leads on AUROC (often 1.0000) and policy-cap compliance.

### 4.2 Section 4.2 — StealthGPT arm

Every AI passage fed through **StealthGPT default rewrite endpoint**, then rescored. Prose summary (§4.2):

- **Pangram:** FNR stays low; ~100% detection on longer passages; modest FNR increase on shorter text.
- **Originality.ai:** FNR ~0.05 long, up to **~0.21** short (genre/LLM dependent).
- **GPTZero:** "**largely loses its capacity to detect**" — FNR **~0.50+** across most genres and LLM models.
- **RoBERTa:** High FNR throughout (unsuitable for high-stakes use).

**Table B.4 (StealthGPT FNR by genre/model, selected):**

| Source LLM | Genre | GPTZero FNR | Pangram FNR |
|------------|-------|-------------|-------------|
| GPT-4.1 | blog | 0.445 | 0.023 |
| GPT-4.1 | novel | 0.447 | 0.024 |
| Claude Opus 4 | blog | 0.585 | 0.041 |
| Claude Opus 4 | novel | 0.773 | 0.029 |
| Gemini 2.0 Flash | blog | 0.525 | 0.030 |
| Gemini 2.0 Flash | novel | 0.437 | 0.037 |

StealthGPT is DAMAGE **L1** (quality-preserving). Booth uses **one** humanizer, not twelve — do not conflate with HumanizerBench ([Agent #40 attribution correction](AGENT-40-DAMAGE-HUMANIZER-TIERS.md)).

### 4.3 Policy-cap framework

Institutions set FPR cap (e.g. ≤0.5%). Pangram is the **only** detector meeting FPR ≤ 0.005 without sacrificing AI recall. GPTZero favors low FPR on **human** text but degrades on **humanized AI** — the cap table (Appendix C) widens GPTZero/Originality FNR under stringent caps.

### 4.4 API field dispute (GPTZero Jan 2026)

GPTZero ([chicago-booth-2026](https://gptzero.me/news/chicago-booth-2026/)) argues Booth used `average_generated_prob` (sentence-level mean) instead of `class_probabilities` / `predicted_class` for document classification. On corrected re-run of the **non-humanizer** corpus:

| Detector | FPR | Recall | Accuracy |
|----------|-----|--------|----------|
| GPTZero | 0.05% | **99.3%** | **99.5%** |
| Pangram | 0.05% | 98.9% | 99.1% |
| Originality | 0.11% | 81.3% | 85.0% |

**What the dispute does and does not cover:**

| Claim | Status |
|-------|--------|
| GPTZero recall on **raw** Booth corpus may be underreported | Plausible — API field mismatch is documented in Booth appendix |
| Pangram FPR advantage on human text | **Not** disputed by GPTZero rebuttal |
| StealthGPT / humanizer robustness | **Not** re-run in GPTZero Jan 2026 post — Booth §4.2 stands unaddressed |
| Pangram Humanizers vs GPTZero on Russell configs | Separate benchmark; GPTZero live bench ([v3.2 comparison](https://gptzero.me/news/how-does-gptzero-compare-to-pangram-v3-2-latest-benchmark-results/)) shows GPTZero leading on **Bypassers** category (95.70% vs Pangram 83.64%) using GPTZero-operated test harness |

**Honest read:** Two truths coexist. Booth may understate GPTZero on clean AI text if the wrong API field was used. Independent humanizer arms (Booth StealthGPT, Russell O1-PRO HUMANIZED, DAMAGE 19-tool) still show **GPTZero paraphrase fragility relative to Pangram humanizer-trained models** at the time of those studies. Model versions move monthly — treat all numbers as dated.

---

## 5. Pangram August 2025 — per-humanizer commercial table

Pangram blog ([humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25)) publishes **detection accuracy** (% caught) on 20 tools post-retraining:

| Humanizer | Pangram detection % | DAMAGE tier |
|-----------|---------------------|-------------|
| Grammarly, Quillbot, Semihuman AI, humanizeai.pro | 100.0% | L1 |
| StealthGPT | 95.6% | L1 |
| DIPPER (research paraphraser) | 97.6% | L1 |
| **Undetectable AI** | **90.3%** | L3 (best evader; still ~9/10 caught) |

Cross-detector citation (Russell et al. panel): Pangram **~97%** vs GPTZero **~46%** vs Fast-DetectGPT **~23%** vs Binoculars **~7%** on humanized text.

**Pangram design tradeoff (CTO Bradley Emi, co-author DAMAGE):** Internal models achieve near-perfect humanizer recall but higher ESL/human FPR — not shipped. Extremely garbled L3 output descoped intentionally (visible to humans; algorithmically ambiguous).

---

## 6. Pangram 4 (2026) — updated head-to-head

Pangram 4 ([arXiv HTML 2607.27183](https://arxiv.org/html/2607.27183)) on UChicago splits — TPR@1%FPR: **Humanizer full length** Pangram 4 **98.93%** vs GPTZero **44.32%**; humanizer stubs Pangram **73.32%** vs GPTZero **0.00%**. Vendors share evaluation substrate; interpret results by model version date.

---

## 7. Mechanism — why paraphrase splits them

| Signal class | GPTZero (historical) | Pangram (humanizer-adapted) |
|--------------|---------------------|----------------------------|
| **Primary features** | Perplexity / predictability cones, sentence-level AI probability | Transformer classifier + hard-negative mining on humanized synthetic data |
| **Paraphrase effect** | Surface token swap breaks perplexity signature → score drops toward human | Generator-family residual patterns persist after fluent rewrite → still classified AI |
| **DIPPER / synonym attack** | Large TPR drop (DAMAGE −40 pp) | 97.6% catch in Aug 2025 table |
| **Cross-model paraphrase** | HIP: base-model continuations score 96.7% human on GPTZero ([Agent #22](AGENT-22-HIP.md)) | Pangram Humanizers trained on diverse humanizer outputs |

**Practitioner implication:** GPTZero greens after paraphrase more often because its consumer score tracks different features than Pangram's humanizer-augmented classifier. Neither equals "human wrote this." Open-source detectors collapse harder still — consumer green ≠ ensemble pass.

---

## 8. unslop dual-reporting policy

Per [UPDATE-PLAN-2026-08.md § Phase 4](UPDATE-PLAN-2026-08.md): unslop never cites a single commercial detector as proof of evasion or detection. Every claim about paraphrase/humanization effects must report **both**:

### 8.1 Consumer layer (what users screenshot)

| Field | Purpose |
|-------|---------|
| GPTZero `predicted_class` / dashboard badge | What students and writers actually see |
| Pangram `prediction` label (Unlikely / Possibly / Likely / Highly Likely AI) | Admissions and integrity offices increasingly default here |
| Turnitin AI + bypasser category (if applicable) | Institutional ground truth for education |

**Rules:**

- Report **before/after** on the **same passage** and **same detector version** (GPTZero model date, Pangram 3.3 vs 4).
- StealthGPT / Undetectable.ai runs must name the **tool and tier** (DAMAGE L1/L2/L3).
- If only GPTZero is green post-paraphrase, say so explicitly — do not imply Pangram/Turnitin pass.

### 8.2 Academic ensemble layer (what maintainers trust)

| Signal | Module / source | What it catches |
|--------|-----------------|-----------------|
| Fast-DetectGPT | Academic baseline | Curvature / probability gap — collapses on naive paraphrase but useful as one axis |
| DivEye | `surprisal.py` | Surprisal variance dynamics — orthogonal to lexical swap |
| TSD | Planned Phase 2 | Late-stage generation volatility |
| DAMAGE TPR@FPR | Citation only | Humanizer collapse benchmarks; not live in `detector.py` today |
| TMR loop | `detector.py` | GPTZero-family feedback — **signal not gate** |

**Rules:**

- README / SKILL benchmark numbers come from `benchmarks/` and `evals/` runs — never vendor marketing.
- Adversarial Paraphrasing (~87.88% average detector TPR drop) and TempParaphraser (~82.5% accuracy reduction) cite **paper numbers**, not unslop deterministic pass (~0.0–0.2 pp TMR).
- Phase 4 acceptance: pipeline beats legacy LLM humanize by ≥5 pp TMR on ≥3 fixtures **plus** ensemble movement on ≥2 academic signals.

### 8.3 Example dual-report (template)

> **Fixture:** 800-word blog post → unslop full + cross-model second pass.  
> **Consumer:** GPTZero Human (was AI_ONLY); Pangram Likely AI (unchanged).  
> **Ensemble:** TMR 0.91 → 0.84; Fast-DetectGPT flag persists.  
> **Conclusion:** Partial consumer relief; not robust under adapted detector or ensemble.

---

## 9. Debate summary

| Camp | Claim | Best source |
|------|-------|-------------|
| **Pangram / DAMAGE authors** | Humanizer-adapted training closes paraphrase gap; fluent L1 rewrites *more* detectable | [DAMAGE](https://arxiv.org/abs/2501.03437), [humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25) |
| **Chicago Booth (independent)** | Pangram only policy-grade detector; GPTZero fails StealthGPT arm | [w34223](https://doi.org/10.3386/w34223) |
| **GPTZero** | Booth API misuse; corrected raw-corpus recall beats Pangram; live bypasser bench leads | [chicago-booth-2026](https://gptzero.me/news/chicago-booth-2026/) |
| **Russell et al. (academic)** | Only Pangram Humanizers matches expert humans under humanization | [ACL 2025](https://arxiv.org/abs/2501.15654) |
| **Detection pessimists** | Detector-guided paraphrase breaks all static classifiers eventually | [AdvPara NeurIPS 2025](https://arxiv.org/abs/2506.07001), Sadasivan bound |
| **unslop** | Cross-model second pass is strongest user lever; report consumer + ensemble; ESL defense not misconduct | `detector.py` ladder exhaustion message, SKILL Boundaries |

---

## 10. Implications for unslop

1. **`detector.py` TMR loop** optimizes a GPTZero-family signal. Ladder exhaustion correctly points to cross-model paraphrase — it cannot simulate Pangram/Turnitin outcomes.
2. **Anti-detector mode** framing stays ESL false-positive defense ([Liang et al. 2023](https://arxiv.org/abs/2304.02819)), not "beat Pangram."
3. **Do not cite** Booth "~6 pp median humanizer drop" — figure not in Jabarian & Imas; likely conflated with HumanizerBench ([Agent #40](AGENT-40-DAMAGE-HUMANIZER-TIERS.md)).
4. **Do cite** StealthGPT divergence: GPTZero FNR ~50%+ vs Pangram robust — with Booth URL and StealthGPT = DAMAGE L1 context.
5. **Refresh quarterly:** Pangram model version (3.3 May 2026, 4 Aug 2026), GPTZero model date strings, Turnitin bypasser release notes.

---

## 11. Open questions

- [ ] Re-run Booth StealthGPT arm with GPTZero `class_probabilities` on 2026 model — does FNR ~50%+ persist?
- [ ] In-repo dual-report bench: same fixtures through Pangram API + GPTZero API + TMR/DivEye ensemble.
- [ ] Retract or source README "median ~6 points" humanizer claim ([Agent #40](AGENT-40-DAMAGE-HUMANIZER-TIERS.md)).

---

*Agent #60 complete. Manifest row 60 → done.*
