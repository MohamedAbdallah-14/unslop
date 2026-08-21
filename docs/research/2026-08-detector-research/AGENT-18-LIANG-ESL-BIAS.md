# Agent #18 — Liang ESL False-Positive Bias

**Topic:** Liang et al., *GPT Detectors Are Biased Against Non-Native English Writers* (*Patterns* 2023; arXiv:2304.02819)  
**Prepared:** August 19, 2026  
**Scope:** Original study, mechanism (perplexity ↔ L2 writing), follow-ups (2024–2026), vendor/industry/institutional response, lawsuits, unslop boundaries  
**Status:** complete

---

## Executive summary

Liang, Yuksekgonul, Mao, Wu, and Zou (Stanford; James Zou lab) published the defining **equity** paper in AI-text detection. On March 15, 2023, they ran seven commercial detectors on **91 human-written TOEFL essays** (Chinese forum, pre-2020) vs **88 US eighth-grade ASAP essays** (presumed native speakers). Result:

| Corpus | Mean false-positive rate (flagged as AI) | At least one detector flagged |
|--------|------------------------------------------|-------------------------------|
| TOEFL (non-native) | **61.22%** | **97.80%** (89/91) |
| US 8th grade (native) | **5.19%** | near-perfect accuracy |

All seven detectors **unanimously** flagged **19.78%** (18/91) of human TOEFL essays. Those essays had significantly lower GPT-2 XL perplexity (P = 9.74×10⁻⁵). The paper's mechanism is blunt: detectors treat **predictable prose** as machine prose; L2 academic English is often predictable for lexical, syntactic, and grammatical reasons documented in decades of SLA literature.

The paper's second finding is load-bearing for unslop: the **same linguistic transformation** that removes ESL false positives also evades detectors. Prompting ChatGPT to *"Enhance the word choices to sound more like that of a native speaker"* on real TOEFL essays dropped mean FPR from **61.22% → 11.77%** (−49.45 pp). The inverse prompt on native essays raised FPR from **5.19% → 56.65%**. A second-round self-edit on synthetic ChatGPT essays (*"Elevate the provided text by employing literary language"*) dropped detection from up to **100% → 13%**.

**2025–2026 state of play:** Bias is **not immutable** but **not solved**. Al Ali et al. (EACL 2026 SRW; arXiv:2602.05769) re-tested Liang's English TOEFL set with a 2025 commercial detector (Plagramme): FPR **23.1%** vs Liang's **61.3%** — better, still **23×** the 0% FPR on native Hewlett essays in the same run. Chicago Booth (Jabarian & Imas, BFI WP 2025-116) reports top commercial detectors at **≤1% FPR** on general human corpora but does **not** stratify by L1. GPTZero and Pangram both claim ESL de-biasing; Pangram reports **0%** on the fixed 91-essay Liang set (first-party, Apr 2025). Turnitin shipped "non-native English speaker protections" (Oct 2025) and still faces Adelphi litigation where a **100%** Turnitin score was annulled (NY Supreme Court, Jan 2026). **60+ institutions** have disabled or restricted AI detection, often citing Liang's headline number.

**Unslop verdict:** Liang is the **ethical anchor** for `/unslop anti-detector`. The mode's burstiness, contraction, and specificity steps are structurally aligned with what Liang showed removes unfair perplexity penalties — without requiring users to "sound native." Boundaries stay tight: defensive use (ESL false positives, resume writers, journalists) yes; academic misconduct no. **Maintenance note:** `skills/unslop/SKILL.md` Boundaries cite arXiv **2306.04723** alongside Liang — that ID is Tulchinskii (intrinsic dimension), not Liang. Correct citation is **2304.02819** / DOI [10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779).

---

## 1. Paper identity

| Field | Value |
|-------|-------|
| **Title** | GPT Detectors Are Biased Against Non-Native English Writers |
| **Authors** | Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, James Zou |
| **Affiliations** | Stanford CS, EE, Biomedical Data Science |
| **Venue** | *Patterns* (Cell Press), July 10, 2023 |
| **Preprint** | arXiv:2304.02819 (v3+) |
| **DOI** | [10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779) |
| **Code/data** | [GitHub](https://github.com/Weixin-Liang/ChatGPT-Detector-Bias) · [Zenodo 7893958](https://doi.org/10.5281/zenodo.7893958) |
| **Plain summary** | [Stanford HAI news](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers) |

**One-line contribution:** Perplexity-based GPT detectors systematically misclassify human L2 English as AI-generated while scoring native English near-perfectly; vocabulary enrichment fixes bias and enables evasion with the same prompt.

---

## 2. Experimental design

### 2.1 Detectors tested (March 15, 2023)

Seven off-the-shelf tools, all perplexity- or classifier-backed products available at ChatGPT launch:

| # | Detector | URL (as tested) |
|---|----------|-----------------|
| 1 | Originality.AI | app.originality.ai |
| 2 | Quill.org AI Writing Check | aiwritingcheck.org |
| 3 | Sapling | sapling.ai/ai-content-detector |
| 4 | OpenAI RoBERTa classifier | HF Space (later withdrawn) |
| 5 | Crossplag | crossplag.com |
| 6 | GPTZero | gptzero.me |
| 7 | ZeroGPT | zerogpt.com |

**Snapshot caveat:** All numbers describe the **March 2023 detector generation**. GPTZero retired perplexity/burstiness as the classifier backbone in autumn 2023; Turnitin did not ship LMS AI detection until April 2023 (after Liang's access date).

### 2.2 Corpora

| Dataset | n | Source | Population |
|---------|---|--------|------------|
| TOEFL essays | 91 | toefl.zhan.com (Chinese forum) | Non-native English, year ≤ 2020 |
| ASAP essays | 88 | Hewlett Foundation Kaggle ASAP | US 8th graders |
| ICLR 2023 abstracts | 1,574 | OpenReview | Pre-ChatGPT ML papers; country-level L1 proxy |
| Synthetic essays | 31 | ChatGPT-3.5 Common App prompts | Evasion experiment |
| Synthetic abstracts | 145 titles | Stanford CS224n W2021 | Evasion experiment |

### 2.3 Perplexity measurement

GPT-2 XL log-probability; paired one-sided *t*-tests. ICLR analysis controlled for review rating via regression residuals — non-native-country authors still showed significantly lower abstract perplexity (P = 0.033 after rating control).

---

## 3. Headline results (verified from paper)

### 3.1 Asymmetric false positives

- **TOEFL mean FPR:** 61.22% across seven detectors  
- **Native mean FPR:** 5.19%  
- **Unanimous TOEFL flags:** 19.78% (18/91) — all seven detectors agree  
- **≥1 detector flagged:** 97.80% (89/91) TOEFL essays  
- **Unanimous-flagged TOEFL essays:** significantly lower perplexity (P = 9.74×10⁻⁵)

Stanford HAI popularized this as "more than half of TOEFL essays" and "97% flagged by at least one detector."

### 3.2 Causal intervention — vocabulary / register shift

| Intervention | Direction | Mean FPR change | Perplexity |
|--------------|-----------|-----------------|------------|
| ChatGPT: "Enhance word choices… native speaker" on TOEFL | L2 → richer lexicon | 61.22% → **11.77%** (−49.45 pp) | Significant increase (P = 9.36×10⁻⁵) |
| ChatGPT: "Simplify word choices… non-native speaker" on ASAP | Native → constrained lexicon | 5.19% → **56.65%** (+51.46 pp) | Significant decrease |
| Post-enhancement unanimous TOEFL flags | — | 1/91 (1.10%) | — |

**Interpretation:** Detectors were not detecting "AI authorship." They were detecting **low perplexity / low lexical diversity** — a property shared by early GPT output *and* by many human L2 writers in timed exam conditions.

### 3.3 Evasion — same mechanism, adversarial direction

| Task | Pre self-edit detection | Post "literary/technical language" edit |
|------|-------------------------|----------------------------------------|
| ChatGPT college essays (31 valid) | up to 100% | up to **13%** |
| ChatGPT CS224n-style abstracts | up to 68% | up to **28%** |

Perplexity rose sharply after self-edit (P ≪ 0.001). Liang explicitly connects this to Krishna et al. paraphrase evasion and Sadasivan impossibility work in the discussion.

### 3.4 Limitations (authors' own)

- Small *n* (91 + 88) — pilot scale  
- TOEFL corpus is **Chinese L1 only**; not general "ESL"  
- Detectors used **GPT-2-era** backends where applicable  
- Binary detector outputs; no per-threshold ROC on L1-stratified data  
- ASAP essays are **8th grade**, not college native baseline — asymmetry of genre as well as L1

---

## 4. Mechanism — why L2 English looks like LLM text

### 4.1 Perplexity as proxy for "human-ness"

GPTZero's 2023 public explainer (and most tools Liang tested) treated **low perplexity** (high next-token predictability) as an AI signal. Human writing was assumed to be **burstier** and **less predictable**.

L2 academic English often violates that assumption:

| L2 writing trait | Detection consequence |
|------------------|----------------------|
| Smaller productive vocabulary (Laufer & Nation 1995) | Lower type-token ratio → lower perplexity |
| Formulaic scaffolding ("Firstly… Furthermore… In conclusion") | High bigram predictability |
| Reduced syntactic complexity (Lu 2011; Ortega 2003) | Shorter dependency paths → easier LM prediction |
| Error avoidance / simplified grammar (Biber et al. 2011) | More regular patterns |
| Exam-register TOEFL prompts | Convergent genre templates across writers |

ICLR 2023 abstract analysis extends the claim beyond student essays: **non-native-country ML authors** write lower-perplexity abstracts even at equal review scores — detection bias can hit professional researchers, not only undergraduates.

### 4.2 The equity–evasion isomorphism

Liang's core paradox (later cited in Cat 05, 09, 18 across unslop research):

```
Constrained lexicon + uniform syntax  →  high detector score
                ↕ (same transform)
Richer lexicon + varied syntax        →  low detector score
```

That transform is:

- **Fairness fix** when applied to genuine human L2 prose falsely flagged  
- **Evasion** when applied to actual LLM output  
- **Indistinguishable to the detector** without external provenance

This is why unslop refuses to market anti-detector as "beat Turnitin for cheaters" while still offering it for documented false-positive defense.

### 4.3 Populations beyond Liang's TOEFL set

Subsequent practitioner and press literature (not in the original paper) documents similar misfires on:

- **Neurodivergent formal writers** (Adelphi Newby case — autism + Turnitin 100%)  
- **Grammarly / tutoring-assisted prose** (polished surface → low perplexity)  
- **West-African English "delve"** and other L1 transfer features (HN 2025 threads; Cat 15)  
- **Apple autocorrect em-dash users** (single-feature over-fit; not Liang but same mechanism)  
- **Careful native academics** ("the better the writer, the more AI thinks you're AI" — Erin Ramirez, Cal State; widely quoted in Cat 18)

Liang did not test these groups; the mechanism predicts overlap whenever prose is **regular, polished, or template-shaped**.

---

## 5. Follow-up research (2024–2026)

### 5.1 Al Ali et al. — "Different Time, Different Language" (EACL 2026 SRW)

- **arXiv:** [2602.05769](https://arxiv.org/abs/2602.05769)  
- **Question:** Did 2025 detectors fix Liang's bias? Does bias require perplexity?

**Czech setting (Q1–Q2):** Non-native Czech essays do **not** show lower entropy than native youth writing — opposite of English Liang finding. Custom Czech detectors show **no systematic native vs non-native FPR gap** on AKCES corpora.

**English Liang replication (Table 5):** Plagramme commercial detector on original TOEFL-91 vs Hewlett native:

| Dataset | FPR |
|---------|-----|
| TOEFL-91 (Liang non-native) | **23.1%** |
| Hewlett (Liang native) | **0.0%** |

Improvement from 61.3% → 23.1%, but **bias persists**. Entropy–detector correlation on English set: negligible (0 < ρ < 0.04) — contemporary detector not purely perplexity-driven.

**Takeaway for unslop:** "Detectors fixed ESL bias" is **overstated**. "Bias reduced but not eliminated" is accurate. Language-specific morphology matters; English L2 bias remains the highest-stakes case for global academia.

### 5.2 Chicago Booth — Jabarian & Imas (BFI WP 2025-116)

- **PDF:** [BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)  
- **Review:** [Chicago Booth Review](https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust)

Tests Pangram, Originality.ai, GPTZero, RoBERTa on mixed human/AI corpora by length. **Pangram** achieves near-zero FPR on medium/long passages at strict 0.5% policy caps. **RoBERTa open-source** FPR 30–78% — reproduces the "free tools are dangerous" lesson.

**Gap:** Booth corpus is **not** the Liang TOEFL benchmark. ESL-stratified FPR is absent. Pangram's first-party re-test of the 91-essay set (0% FPR, Apr 2025 blog) is the main post-Liang independent datapoint on the **fixed benchmark**.

### 5.3 GPTZero ESL de-biasing arc

| Milestone | Claim |
|-----------|-------|
| Liang 2023 | GPTZero among seven detectors; part of 61.22% mean |
| GPTZero 2024 response | Blog: "ESL Bias in AI Detection is an Outdated Narrative" + model update |
| Pangram 2024 report | GPTZero updated model: **7.7%** FPR on 91-essay set (1.1% if "Possible AI" counted negative) |
| arXiv 2602.13042 (Feb 2026) | GPTZero technical report: Model 3.7m **97.6% recall, 0.09% FPR** on 24-language bench (vendor) |
| Chicago Booth Jan 2026 | GPTZero **99.3% recall / 0.1% FPR** on Booth corpus (vendor-relayed) |

**Tension:** Vendor multilingual benchmarks ≠ Liang TOEFL replication. Independent ESL-stratified confusion matrices remain rare.

### 5.4 Originality.ai rebuttal

- **URL:** [originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers](https://originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers)  
- **Thesis:** Liang study "flawed" — TOEFL forum essays ≠ enrolled students; Originality's own corpus shows minimal bias  
- **Counter:** Originality is a **vendor** with legal/PR incentive; Liang benchmark still used by Pangram and Al Ali as fixed reference  
- **Observation:** Originality ships monthly retraining (Lite/Turbo/Academic 2025) with explicit humanizer resistance — they accept evasion pressure while disputing ESL numbers

### 5.5 Education / integrity follow-ups

| Paper | Finding relevant to Liang |
|-------|---------------------------|
| Perkins et al. 2024 (Frontiers) | Seven detectors **39.5%** baseline accuracy on edited AI; not ESL-stratified but supports "don't use for integrity findings" |
| Nicks et al. ICLR 2024 | RL fine-tune drops detector AUROC in <1 day — orthogonal to ESL but undermines high-stakes reliance |
| Computing-education study (arXiv 2307.07411) | **52/114** human CS submissions false-flagged — adjacent early warning cited in AGENT-57 |

### 5.6 Fixed benchmark as community anchor

The **91 TOEFL essays** became a **held-out equity benchmark**:

| Evaluator | Year | FPR on Liang TOEFL-91 |
|-----------|------|------------------------|
| 7-detector mean (Liang) | 2023 | **61.22%** |
| GPTZero (post-debias) | 2024 | **7.7%** (1.1% generous) |
| Pangram | 2024–25 | **0%** (first-party) |
| Plagramme (Al Ali) | 2025 | **23.1%** |

Bias multiplier vs ~5% native baseline fell from **~12×** to **0–4×** depending on vendor — but **no consensus** that all production detectors cleared a 0.5% ESL FPR bar.

---

## 6. Industry response (2023–2026)

### 6.1 Turnitin

| Date | Action |
|------|--------|
| Apr 2023 | AI writing detection launched LMS-wide; claimed **<1% FP**, 97% GPT-3/ChatGPT detection |
| Apr 2023 | [Washington Post](https://www.washingtonpost.com/technology/2023/04/01/chatgpt-cheating-detection-turnitin/) — innocent student flagged; cited in *Patterns* editorial |
| 2024–25 | FP rate revised upward in discourse (~**4%** sentence-level per vendor ack.) |
| Oct 2025 | "Non-native English speaker protections"; **hide 1–19% scores** (vendor found higher FP incidence in band) |
| Aug 2025 | Anti-humanizer detection shipped |
| Feb 2026 | Model update; FP "held below 1%" per vendor |
| Feb 2026 | Public pivot language: "detection → transparency" (Grammarly Authorship / process provenance) |

Turnitin's own research (relayed in industry digests) documented **6–9% FP on L2 English vs 1–4% native** — acknowledged disparity, disputed closure.

### 6.2 GPTZero

- Autumn 2023: deep-learning classifier; perplexity/burstiness demoted to **UI explainability**  
- Explicit ESL corpus inclusion in de-biasing (vendor claim, 2024–25)  
- Jun 2026: acquired by Superhuman (~$30M ARR) — pivots toward **authorship replay** alongside detection  
- Strategic shift: institutions moving from post-hoc scores to **process evidence** (Replay, Grammarly Authorship)

### 6.3 OpenAI

- Withdraw public classifier **July 2023** (~26% TP / 9% FP on their eval — Liang-era baseline)  
- Aug 2024: declines to ship 99.9% watermark — cites user churn + trivial paraphrase circumvention ([The Verge](https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool))

### 6.4 Copyleaks, Pangram, Grammarly

- **Copyleaks:** ensemble "three investigators"; multilingual expansion; vendor claims do not publish Liang replication  
- **Pangram:** positions on Booth + Liang TOEFL re-test; adoption in admissions workflows  
- **Grammarly/Superhuman:** Authorship keystroke provenance — **sidesteps** perplexity bias by not classifying post-hoc text alone

---

## 7. Institutional, legal, and press response

### 7.1 Universities disabling or restricting detectors

Canonical case — **Vanderbilt**, Aug 16, 2023: disabled Turnitin AI detector; arithmetic at claimed 1% FP × 75,000 papers/year = **750 false accusations**; cited ESL bias ([guidance post](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/)).

Tracker summaries (GradPilot 2026) list **60+ institutions** including Northwestern, UT Austin, MIT Sloan guidance, UC Berkeley, University of Waterloo (2025 — internal test flagged human text **100% AI**), Curtin (Jan 2026), UBC (declined enablement Apr 2023).

**Policy pattern:** Detector scores **cannot be sole evidence**; require drafts, interviews, process artifacts.

### 7.2 Litigation and administrative wins (2025–2026)

| Case | Detector | Outcome | ESL/neuro relevance |
|------|----------|---------|---------------------|
| **Matter of Newby v. Adelphi** (NY Sup. Ct., Jan 2026) | Turnitin 100% | Record expunged; decision "without valid basis and devoid of reason" | Autistic student; Grammarly tutoring; contradictory tools ignored |
| **Kato v. Palo Alto USD** (filed 2026) | Turnitin 76% | Pending | Human essay, in-class rewrite penalty |
| **Rignol v. Yale** | GPTZero | Pending | SOM application essay |
| **Yang v. U. Minnesota** | GPTZero + faculty | Student lost on appeal | PhD dissertation — shows detectors still used despite controversy |

Newby is **Article 78 administrative review**, not federal damages — but establishes process-defect precedent when institutions ignore contradictory detector results.

### 7.3 Mainstream press adopting Liang headline

- **Bloomberg** Oct 2024 — named false-accusation victims; cites **61% ESL** figure  
- **MIT Technology Review**, **WIRED**, **Inside Higher Ed** — institutional retreat narrative  
- **Stanford HAI** — primary public explainer

The **61.3% TOEFL** stat is now load-bearing in marketing, policy, and humanizer category positioning — regardless of 2025 detector improvements.

---

## 8. Critiques of Liang (and rebuttals)

| Critique | Source | Assessment |
|----------|--------|------------|
| TOEFL forum essays ≠ enrolled student work | Originality.ai blog | Valid **external validity** concern; does not negate **mechanism** on matched prompts |
| Small sample, single L1 (Chinese) | Authors' limitations + reviewers | Fair; replication on other L1s still sparse |
| Genre confound (exam vs 8th-grade narrative) | Methodology critics | Partial; ICLR abstract analysis partially controls |
| "Outdated — detectors improved" | GPTZero 2024, Axis Intelligence 2026 | **Partially true** on fixed benchmark; **ESL disparity persists** in Al Ali English replication (23.1% vs 0%) |
| "Humanizers exploit equity framing" | Academic integrity advocates | Real tension; unslop addresses via Boundaries + decline misconduct |
| Booth proves detectors trustworthy | Vendor marketing | Booth ** lacks ESL stratification**; Pangram's 0% on Liang set is first-party |

**Net:** Liang remains **citation-grade** for mechanism and historical harm. It is **not** a universal 2026 FPR forecast without per-detector replication on L1-stratified data.

---

## 9. Relationship to other unslop research agents

| Agent / paper | Connection |
|---------------|------------|
| **#17 Sadasivan** | Paraphrase evasion; Liang's "native speaker enhancement" is lightweight paraphrase |
| **#57 GPTZero** | Primary vendor arc post-Liang; ESL de-biasing claims |
| **#56 Turnitin** | Oct 2025 L2 protections; anti-humanizer 2025–26 |
| **#25 Adversarial Paraphrasing** | Operationalizes Liang's register shift at scale |
| **#41 Paneru contraction** | Contractions (anti-detector step 3) — human rate ~0.17 vs AI ~0.00 in Paneru's test subset |
| **#55 Surprisal / DivEye** | Moves beyond scalar perplexity — may reduce but not remove L2 overlap |
| **#68 (manifest)** | "ESL false-positive industry response" — this memo feeds that slot |

---

## 10. Unslop integration

### 10.1 Why Liang grounds anti-detector mode

`/unslop anti-detector` is explicitly scoped as **false-positive defense** in `skills/unslop/SKILL.md` Boundaries. Liang supplies the peer-reviewed warrant:

1. Detectors conflate **predictable human prose** with AI  
2. L2 writers produce predictable prose for **human reasons**  
3. Register shift (richer lexicon, burstier syntax) reduces false flags **without fabricating facts**

Anti-detector procedure steps map to Liang mechanism:

| unslop step | Liang / detection link |
|-------------|------------------------|
| Burstiness band (σ ≥ 6) | Raises perplexity variance — opposite of flat L2 exam prose |
| Break uniform structure | Reduces template predictability |
| Contractions / fragments | Paneru: corpus-specific human contraction rate; lowers "polished AI" register |
| Grounded specificity | User-specific tokens unpredictable to LM — not in Liang but complementary |
| Rough edges | Avoids over-polished low-perplexity surface |
| Cross-model second pass | Changes stylometric fingerprint; Liang used ChatGPT enhancement |

**Critical distinction:** unslop anti-detector for ESL defense should **preserve the writer's authentic L1-influenced voice**, not force "native speaker" cosmetic enrichment — Liang used native-like enhancement as a **scientific intervention**, not an ethical recommendation. Voice-match mode is the right tool when the goal is identity preservation; anti-detector when the goal is reducing false flags on formal/academic drafts.

### 10.2 Boundaries (unchanged principles, Liang-backed)

From `skills/unslop/SKILL.md` and `UPDATE-PLAN-2026-08.md`:

| Rule | Liang basis |
|------|-------------|
| **Offer** anti-detector for ESL false positives, resume writers, journalists | 61% TOEFL FPR; institutional disablement wave |
| **Decline** plagiarism / grader deception | Same transform enables evasion (Liang § bypass) |
| **No "100% undetectable" marketing** | Liang + Sadasivan + monthly retraining |
| **Document watermark side effect** | Orthogonal to ESL but regulatory (EU AI Act Art. 50, Aug 2026) |
| **Treat evasion as non-durable** | Retrieval defenses; authorship replay pivot |

### 10.3 Citation fix needed

`skills/unslop/SKILL.md` L145 cites **arXiv 2306.04723** with Liang findings. **2306.04723 is Tulchinskii et al.** (intrinsic dimension detection). Liang is **2304.02819**. Fix in SSOT on next Boundaries touch.

### 10.4 What unslop should NOT do

| Action | Reason |
|--------|--------|
| Promise permanent Turnitin/GPTZero pass | Al Ali: 23% FPR still possible; Turnitin anti-humanizer Aug 2025 |
| Ship "sound like native speaker" prompt | Ethically coercive; erases legitimate L1 voice |
| Use Liang 61% as 2026 vendor FPR | Anachronistic; use stratified current benchmarks |
| Target academic evasion workflows | Boundaries violation |

### 10.5 Recommended unslop artifacts

1. **`drafts/2026-05-detector-test/`** — include Liang-style L2 sample or TOEFL-analog in bench corpus; report ESL vs native FPR separately  
2. **README "When it matters"** — keep Liang + Vanderbilt arithmetic as consumer-facing equity case  
3. **Agent #68 memo** — industry response timeline (this memo is upstream)  
4. **Help skill** — one-line: "anti-detector = false-positive defense (Liang 2023); not for cheating"

---

## 11. Open gaps (research + product)

1. **No public ESL confusion matrix for Turnitin 2026** post-"L2 protections" — vendor-only claims  
2. **L1 diversity** — Liang is Chinese TOEFL only; Arabic, Spanish, Hindi L1 replication scarce in peer review  
3. **Genre × L1 interaction** — STEM lab reports vs humanities essays untested on fixed Liang scale  
4. **Humanizer harm to L2 voice** — commercial tools optimize for detector pass, may homogenize toward native register (Cat 18 gap)  
5. **Process provenance vs post-hoc humanize** — GPTZero Replay / Grammarly Authorship may obsolete classifier-only defense for institutions that adopt them  
6. **Booth + Liang intersection** — independent lab has not yet published ESL-stratified Booth-style policy-cap analysis

---

## 12. Primary source table

| # | Source | Year | URL |
|---|--------|------|-----|
| 1 | Liang et al. — *Patterns* / arXiv:2304.02819 | 2023 | https://arxiv.org/abs/2304.02819 |
| 2 | Stanford HAI summary | 2023 | https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers |
| 3 | Liang code/data | 2023 | https://github.com/Weixin-Liang/ChatGPT-Detector-Bias |
| 4 | Al Ali et al. — EACL 2026 SRW | 2026 | https://arxiv.org/abs/2602.05769 |
| 5 | Jabarian & Imas — BFI WP 2025-116 | 2025 | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| 6 | Originality.ai ESL rebuttal | 2023+ | https://originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers |
| 7 | Vanderbilt disable guidance | 2023 | https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/ |
| 8 | Bloomberg false accusations | 2024 | https://www.bloomberg.com/news/features/2024-10-18/do-ai-detectors-work-students-face-false-cheating-accusations |
| 9 | Matter of Newby v. Adelphi | 2026 | NY Slip Op 26021 (Jan 2026) |
| 10 | GPTZero technical report | 2026 | https://arxiv.org/abs/2602.13042 |
| 11 | Krishna et al. — DIPPER | 2023 | https://arxiv.org/abs/2303.13408 |
| 12 | Nicks et al. — detector RL evasion | 2024 | https://openreview.net/forum?id=4eJDMjYZZG |

---

## 13. Unslop verdict (one paragraph)

Liang et al. is the **load-bearing equity citation** for the entire humanizer category's legitimate use case. It proved, with reproducible numbers on fixed corpora, that March 2023 detectors punished constrained English — and that the punishment mechanism (perplexity / predictability) was **gameable in both directions**. Three years later, mean FPR on the same 91 essays dropped from **61%** toward **0–23%** depending on vendor, but **native vs non-native gaps have not been eliminated in independent English replication**, and high-stakes failures (Adelphi 100%, Waterloo 100%, Palo Alto 76%) keep occurring. unslop should **cite Liang for why anti-detector exists**, **implement anti-detector as distribution shaping (burstiness, contractions, specificity) rather than "native-washing"**, **decline misconduct**, and **fix the 2306.04723 citation typo** in Boundaries. The arms race moved toward authorship replay; ESL writers still need post-hoc false-positive defense when institutions use classifiers without process evidence.
