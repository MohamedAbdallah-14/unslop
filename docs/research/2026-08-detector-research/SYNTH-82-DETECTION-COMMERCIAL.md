# SYNTH-82 — Commercial Detection Landscape (August 2026)

**Synthesis agent:** #82  
**Inputs:** Agent memos #56–60, #62–70, #67 (commercial detection category)  
**Prepared:** August 19, 2026  
**Status:** Category synthesis for unslop detector refresh, README honesty pass, bench protocol  
**Cross-refs:** [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md), [AGENT-67-MARKETING-VS-AUDIT.md](./AGENT-67-MARKETING-VS-AUDIT.md), [AGENT-62-CHICAGO-BOOTH-2026.md](./AGENT-62-CHICAGO-BOOTH-2026.md)

---

## Executive summary

Commercial AI-text detection in August 2026 is a **patchwork of moving targets**, not a single accuracy leaderboard. Vendors sell clean-corpus separability ("99% accurate"); independent audits test deployment reality — humanizers, paraphrase, stubs, ESL prose, mixed authorship. The gap is typically **15–47 percentage points** and often **exceeds the spread between top vendors on raw AI text**.

Three structural shifts define the year:

1. **Humanizer arms race.** Turnitin (Aug 2025 bypasser layer, Feb 2026 retrain), GPTZero (15 model releases in 2025, humanizer red-team in arXiv:2602.13042), Originality (Turbo 3.0.2 Sep 2025), Pangram (DAMAGE-line humanizer training). Static bypass numbers decay in weeks.

2. **Ranking inverts under stress.** Jabarian & Imas (Chicago Booth / BFI WP 2025-116): on clean medium-to-long English, Pangram leads policy-cap metrics; after **StealthGPT** humanization, GPTZero FNR **44–77%** while Pangram stays **0–5%**. GPTZero's Jan 2026 rebuttal re-runs clean text only — humanizer arm unaddressed.

3. **Institutional retreat + generator exit.** OpenAI killed its public classifier Jul 2023 (26% TPR, 9% FPR); 60+ universities disabled Turnitin AI detection (2023–26); FTC sanctioned 98.3% claims → 53.2% measured (Content at Scale, Aug 2025). Integrity offices pivot to **process provenance** (Authorship, Replay, draft history) while classifiers remain advisory at best.

**For unslop users:** No single detector is authoritative. Education users hit **Turnitin + GPTZero** most; admissions and agencies hit **Pangram + Originality**; enterprise LMS bundles add **Copyleaks**. Lexical cleanup alone fails 2026 GPTZero/Originality; cross-model second pass is the strongest user lever unslop can recommend. Anti-detector mode stays **ESL false-positive defense and register restoration** — not Turnitin bypass.

---

## 1. Vendor landscape 2026

### 1.1 Tier map — who unslop users actually encounter

| Tier | Detector | Primary channel | Aug 2026 posture | unslop user exposure |
|------|----------|-----------------|-------------------|----------------------|
| **T1 — LMS default** | **Turnitin** | University LMS, iThenticate | Bypasser layer (Aug 2025); unified blue UI (Jul 2026); 1–19% scores suppressed as `*%` | **Highest** for coursework |
| **T1 — Consumer/education** | **GPTZero** | Web, Chrome, LMS plugins; **Superhuman** (Jun 2026 acquisition) | Deep-learning + humanizer red-team; predictability-cone generation; Writing Replay | **Highest** for direct checks |
| **T1 — Agency/publisher** | **Originality.ai** | SEO, enterprise, Moodle | Turbo 3.0.2 (hardest binary); **AI Allowance** (Jul 2026) for hybrid policy | Freelancers, content teams |
| **T1 — Admissions/integrity** | **Pangram** | API, admissions offices | Humanizer-adapted classifier; Booth policy-cap winner on clean + StealthGPT | Growing in high-stakes admissions |
| **T2 — Enterprise bundle** | **Copyleaks** | LMS + plagiarism fusion | V9/V10 ensemble + AI Logic (phrase heatmap, AI Source Match) | Multilingual enterprise |
| **T2 — Suite incumbent** | **Grammarly/Superhuman** | 40M+ DAU; Authorship in Docs | Dual detector (Grammarly + GPTZero); humanizer framed as clarity, not bypass | Comparison anchor, not bench target |
| **T3 — Defunct public** | **OpenAI classifier** | — | **Withdrawn Jul 2023**; text watermark unreleased | FAQ confusion only |
| **T3 — RoBERTa baseline** | OpenAI HF weights (2019) | Research papers | GPT-2 era; not ChatGPT-calibrated | Historical baseline only |

### 1.2 Product timeline (2025–2026 highlights)

| Date | Vendor | Change | Detection implication |
|------|--------|--------|----------------------|
| Aug 27, 2025 | Turnitin | Bypasser detection integrated (English) | Humanizer outputs merge into "AI-generated only"; no sub-label |
| Sep 2025 | Originality | Lite 1.0.2 / Turbo 3.0.2 / Academic 0.0.5 | Explicit humanizer retraining; pre-Sep bypass stats stale |
| Oct 14, 2025 | Turnitin | Model refresh; L2 tuning claimed | ESL narrative load-bearing; no public post-update matrix |
| Jan 2026 | GPTZero | "v6" generation; arXiv:2602.13042 | Paraphrase-resistant features; synonym swap insufficient |
| Feb 12, 2026 | Turnitin | English recall bump | Not retroactive; resubmit required |
| Feb 2026 | GPTZero | Booth rebuttal; model `2025-12-18-base` | Clean-text ranking dispute; humanizer arm not re-run |
| Jul 2026 | Originality | AI Allowance (0–40% thresholds) | Hybrid workflows; same text, opposite verdict by threshold |
| Jul 20, 2026 | Turnitin | Single blue highlight | UI de-escalation; detection logic unchanged |
| Jun 2026 | Superhuman | Acquires GPTZero (~$30M ARR) | Authenticity layer: Authorship + Replay + dual detectors |

### 1.3 Corporate consolidation

**Superhuman** (formerly Grammarly parent) now bundles: Grammarly writing + Coda/Docs + Superhuman Mail + **GPTZero** + Authorship provenance. Strategic bet: **process transparency where possible, classifier ensemble where not** — same tension as Turnitin (Clarity drafts, Authorship keystrokes) while de-emphasizing UI certainty.

unslop is **not** competing on distribution or provenance capture. It competes on editor-native polish, byte-exact preservation, and honest non-bypass positioning.

### 1.4 Evasion difficulty ranking (practitioner consensus, Aug 2026)

Independent humanizer tests and bypass surveys converge on a rough ordering — **not** identical to clean-text Booth ranking:

```
Originality Turbo 3.0.2  ≳  GPTZero (2026)  ≳  Turnitin (post-bypasser)  ≳  Copyleaks  ≫  free tools
```

**Paraphrase/humanized axis diverges:**

| Detector | Clean English (Booth-class) | Humanized / StealthGPT | Notes |
|----------|----------------------------|------------------------|-------|
| Pangram | Policy-cap leader | **Robust** (FNR ~0–5%) | Booth + DAMAGE; vendor-adjacent on 19-tool pool |
| GPTZero | Strong; #1 disputed on API field | **Fragile** (FNR 44–77% Booth; 60% TPR DAMAGE) | 2026 retrain may narrow gap — not independently replicated on 19 tools |
| Originality Turbo | 81.3% recall Booth clean | Moderate; aidetector.ac −24 pp humanized | Hardest single commercial check on raw SaaS humanizer output |
| Turnitin | Not in Booth | Blommerde 0–72% by tool; vendor metrics unpublished | Institutional default despite retreat wave |
| Copyleaks V9/V10 | ~90.7% adjacent studies | 40–71% post-humanization; sometimes **better than GPTZero** on paraphrase | Weaker clean recall; stronger on some edited-AI studies |

**Critical rule:** A green **GPTZero** after paraphrase is **not** a green **Pangram** or **Turnitin**. Dual reporting required.

---

## 2. Claim vs audit gaps

### 2.1 The pattern (Agent #67)

| Claim type | Marketing condition | Audit condition | Typical gap |
|------------|--------------------|-----------------|-------------|
| Overall accuracy | Raw AI vs clean human, long text | Humanized, mixed, stubs | 15–47 pp |
| False-positive rate | Native English, vendor threshold | ESL TOEFL, short form | 0.5% claimed → 5–61% measured (era-dependent) |
| Humanizer resistance | Named tools on retrained model | 19-tool pool, StealthGPT | GPTZero 99.7% → 60% (DAMAGE) |
| Benchmark rank | RAID clean slice | RAID adversarial grid | "99% TPR" → 20–50% under paraphrase |
| Regulatory accuracy | Headline % | FTC independent retest | 98.3% → 53.2% (Content at Scale) |

**Structural causes:** metric laundering (AUROC vs TPR@FPR=5%), condition cherry-picking, self-benchmarking, auto-updating SaaS (numbers age in weeks), Sadasivan impossibility under paraphrase.

### 2.2 Per-vendor gap map

#### Turnitin

| Marketing | Audit reality | Gap |
|-----------|---------------|-----|
| 98% accurate, <1% FPR | Conditional on scores **≥20%**; CPO ~**85% recall** admission | Accuracy describes flagged subset |
| Bypasser detection (Aug 2025) | Blommerde: StealthGPT 0%→72%; **no vendor benchmark** | Unpublished |
| ESL protections (Oct 2025) | Liang lineage; Working Educators 31% ESL vs 12% native; Waterloo 100% FP internal | Equity unresolved |
| "Not sole basis for action" | Newby v. Adelphi (Jan 2026): Turnitin 100% annulled | Policy ≠ practice |

**Attribution fix:** Booth **did not test Turnitin**. Remove "Turnitin 60–85% at Booth" from SKILL.md; cite Blommerde / independent tier **[I]** tests.

#### GPTZero

| Marketing | Audit reality | Gap |
|-----------|---------------|-----|
| 99.3% recall, 0.05% FPR (Booth rebuttal) | Clean text only; StealthGPT arm **not re-run** | ~40 pp under humanization (Booth/DAMAGE) |
| Humanizer-resistant (Model 3.15b+) | DAMAGE on pre-retrain API; Booth StealthGPT collapse | Post-retrain unverified on 19-tool pool |
| ESL de-biased | Liang 2023: part of 61% mean; Al Ali 2026: 23.1% still on TOEFL-91 | Equity improved, not closed |

**Nuance:** API field dispute (`average_generated_prob` vs `predicted_class`) is **legitimate for clean-text ranking** — does not refute humanizer arm.

#### Pangram

| Marketing | Audit reality | Gap |
|-----------|---------------|-----|
| 0.004% FPR | Booth ~0.1% class; sample too small to confirm 0.004% | Extraordinary precision unconfirmed |
| Booth #1 / policy-cap | **Confirmed independent** on clean + StealthGPT | Strongest validated commercial story |
| 99.3% on humanizers | DAMAGE/Russell: **self-authored** | Conflict-of-interest tier |

#### Originality.ai

| Marketing | Audit reality | Gap |
|-----------|---------------|-----|
| Turbo 99%+ raw | Booth clean: **81.3% recall** | Threshold/model sensitive |
| 97% on humanizers | aidetector.ac: **91% → 67%** humanized | ~24–30 pp |
| AI Allowance 99.4% @ 15% | Threshold aligned to binary V6 labels | Peak at marketed setting |

**Paradox:** Marketing **understates** raw difficulty (hardest to evade in practitioner surveys); **overstates** consistency on humanized text.

#### Copyleaks

| Marketing | Audit reality | Gap |
|-----------|---------------|-----|
| 99.12% V9/V10 | Scribbr **66%**; mixed studies 77–96% | Up to 33 pp |
| "Three investigators" ensemble | arXiv:2503.01659 is **4-class LLM attribution**, not binary spec | Category error |
| Best on paraphrase (some studies) | Absolute recall still **40–71%**; 0% on fully humanized in controlled reviews | Not integrity-grade |

#### OpenAI (historical)

| Marketing | Audit reality | Lesson |
|-----------|---------------|--------|
| 26% TPR / 9% FPR (Jan 2023) | Withdrawn Jul 2023 — "low rate of accuracy" | Generator abandoned post-hoc text scoring |
| Internal watermark 99.9% | Never shipped — ESL stigma, bypass, user churn | Provenance > classification at frontier labs |

### 2.3 Chicago Booth — the independent anchor

"Chicago Booth 2026" = **Jabarian & Imas (Aug 2025)** + **GPTZero clean-text rebuttal (Jan 2026)** — not a separate 2026 study.

**Survives scrutiny:**

- Commercial >> open-source RoBERTa on matched corpus
- Short text degrades all tools
- **Policy caps** (FPR ≤ 0.5%) — Pangram only strict-cap winner on clean text
- **StealthGPT arm:** ranking inverts; GPTZero FNR ~50%+; Pangram robust

**Does not support:**

- Turnitin numbers (not tested)
- Twelve-humanizer median drop (Booth = **one** humanizer; twelve = HumanizerBench)
- "~6 points median accuracy drop" in README (not in Jabarian & Imas)

**Attribution hygiene:** Split Booth (1 humanizer) from HumanizerBench (12) from DAMAGE (19).

### 2.4 ESL response — equity gap persists

Liang (2023): **61.22%** mean FPR on 91 human TOEFL essays. Industry responses:

| Mode | Who | 2026 status |
|------|-----|-------------|
| Deny | Originality | Static rebuttal; "not for academic use" |
| "Outdated" | GPTZero | Claims 1.1% on same 91 essays (first-party) |
| Outperform | Pangram | 0% on Liang set (first-party); 25k ESL eval |
| Acknowledge + tune | Turnitin | Oct 2025 L2 protections; 1–19% suppression |
| Exit | OpenAI | Classifier withdrawn Jul 2023 |

**Independent check:** Al Ali (EACL 2026): Plagramme **23.1%** FPR on Liang TOEFL-91 vs **0%** native — bias **not industry-wide solved**. Booth **does not stratify by L1**.

**Institutional response:** Vanderbilt (750 FP/yr arithmetic), Waterloo (100% internal FP), Curtin (Jan 2026 disable), WSU (Feb 2026 contract cancel). OCR Title VI framing (Nov 2024).

**unslop implication:** Liang + institutional retreat **validate** anti-detector as false-positive defense. Vendor "0% ESL" ≠ user's detector at submission time.

### 2.5 Institutional retreat — policy landscape

**Documented minimum:** 60+ institutions across US, Canada, UK, Australia, South Africa disabled or banned AI writing detectors (2023–26). Elite US: ~35/50 disabled per Detection Drama (Jun 2026); Georgia Tech + UGA outliers still on.

**Four recurring reasons:**

1. False positives at scale (Vanderbilt 750/yr; WSU ~1,485/semester at vendor's own 1%)
2. ESL / equity bias (Liang + live failures)
3. Black-box opacity + due process (Newby annulment)
4. FERPA / IP (UT Austin procurement ban)

**Replacement stack:** assessment redesign, AI-use declarations, draft history, **similarity checking retained**, Authorship/Replay provenance (different category from Liang-vulnerable classifiers).

**Retreat ≠ universal:** Patchwork persists; admissions may still use GPTZero/Pangram outside disabled-LMS contexts (Rignol v. Yale pending).

---

## 3. Which detectors matter for unslop users

### 3.1 Persona matrix

| User persona | Likely detectors | What "pass" means | unslop relevance |
|--------------|------------------|-------------------|------------------|
| **University student (US/Commonwealth)** | Turnitin AI + instructor GPTZero spot-check | LMS score + advisory conversation | Don't claim bypass; cite institutional retreat + ESL defense |
| **ESL / L2 writer** | Turnitin, GPTZero, Pangram | Avoid false accusation | **Primary** anti-detector legitimate use case |
| **Grad / professional school applicant** | Pangram, GPTZero (SOM etc.) | Admissions integrity | Dual reporting; Pangram ≠ GPTZero under paraphrase |
| **Freelancer / SEO writer** | Originality Turbo, GPTZero | Client/agency gate | Turbo = hardest bar; log AI Allowance threshold if hybrid policy |
| **Resume / job seeker** | GPTZero, Copyleaks, employer panels | Read-as-human for hiring | Origin story use case; short-form harder (Booth stubs) |
| **Enterprise LMS user** | Copyleaks + Turnitin bundle | Screening, not verdict | Copyleaks Extra Sensitive = explicit humanizer mode |
| **Journalist / editorial** | GPTZero, Pangram, in-house | Voice authenticity | balanced/full modes; not misconduct framing |

### 3.2 Signal stack vs unslop coverage

2026 detectors read five largely independent signals:

| Signal | unslop coverage | Leading vendor sensitivity |
|--------|-----------------|---------------------------|
| Lexical AI-isms | ✅ `humanize.py` | Necessary, insufficient alone |
| Burstiness / sentence-length σ | ⚠️ `structural.py` | Turnitin, Copyleaks, GPTZero |
| Surprisal variance (DivEye) | ⚠️ `surprisal.py` measure-only | Classifier proxies |
| Late-stage stability (TSD) | ❌ | Research frontier |
| Predictability cones (GPTZero v6) | ❌ | Synonym swap fails |

**TMR loop (`detector.py`)** optimizes GPTZero-family signal — **not** Pangram, Turnitin, or Originality. Web bench is external validator.

### 3.3 What unslop should measure in benchmarks

**Tier 1 (minimum credible article):**

1. GPTZero — `predicted_class`, version string (e.g. `2025-12-18-base`), Mixed/Polished/Paraphrased breakdown
2. Originality — Turbo 3.0.2 **and** AI Allowance 15%
3. Turnitin — if accessible; note model date + resubmission requirement

**Tier 2 (dual-report integrity):**

4. Pangram — admissions-relevant divergence from GPTZero
5. Copyleaks — Balanced vs Extra Sensitive

**Tier 3 (ensemble / research):**

6. TMR + DivEye + Fast-DetectGPT — academic signals; not consumer proxy

**Every row:** scan date, model ID, attack arm (clean | unslop | anti-detector | cross-model pass).

---

## 4. Recommendations

### 4.1 Documentation (high priority)

| Action | Rationale |
|--------|-----------|
| **Remove** "Turnitin 60–85% at Chicago Booth" from SKILL.md | Booth did not test Turnitin |
| **Split** "twelve humanizers at Booth" → Booth = StealthGPT only; HumanizerBench = 12 | Misattribution per Agent #62 |
| **Remove or source** "~6 points median accuracy drop" | Not in Jabarian & Imas |
| **Add** institutional context: 60+ universities disabled Turnitin AI (2023–26) | Validates ESL defense framing |
| **Cite OpenAI Jul 2023 exit** in FAQ/Boundaries | No first-party generator detector exists |
| **Dual reporting policy** (Agent #60): never single-detector "pass" | GPTZero green ≠ Pangram green |

**Citation format (every accuracy mention):**

```
[Detector] [model/version + date] · [corpus] · [arm: clean|humanizer|ESL] · [metric] · [tier: I–V]
```

Tier key: **I** independent academic (Booth, Liang, FTC); **II** open benchmark (RAID, SHIELD); **III** peer-reviewed vendor (DAMAGE); **IV** vendor self; **V** adversarial marketing (HumanizerBench, bypass ads).

### 4.2 Product / SKILL messaging

**Say:**

- Commercial detectors work on **raw, medium-length English**; independent audits show **large drops** after humanization (DAMAGE: GPTZero 99.7% → 60%; Booth: GPTZero FNR 44–77% after StealthGPT).
- Pangram leads **independent** clean + StealthGPT tests; not transferable from GPTZero clearance.
- unslop reduces AI-isms and restores human register — **Liang-aligned ESL defense**, not Turnitin guarantee.
- Cross-model second pass (Claude ↔ GPT ↔ Gemini) is strongest user lever; unslop cannot do it alone.
- Turnitin retrained Aug 2025 + Feb 2026 on humanizer outputs; publishes no bypasser accuracy.

**Do not say:**

- "Beat Turnitin" / "detector-proof" / "99% accurate"
- Booth numbers for Turnitin or twelve-humanizer medians
- Single screenshot as systematic bypass
- "ESL bias solved" (Al Ali 23.1%; live 100% failures)

### 4.3 Engineering / bench

| Action | Owner | Priority |
|--------|-------|----------|
| Fill `drafts/2026-05-detector-test/` Copyleaks + Pangram rows | bench | P1 |
| Log GPTZero `predicted_class` + model version in `detector_bench.py` | bench | P1 |
| Run Originality Turbo 3.0.2 + AI Allowance 15% as two rows per fixture | bench | P1 |
| Wire `anti-detector` in `--detector-feedback` ladder | code | P1 (UPDATE-PLAN) |
| Document TMR ≠ Originality gap when both run | docs | P2 |
| Optional: Originality Enterprise API for quarterly automation | ops | P3 |

### 4.4 Anti-detector boundaries (unchanged, now load-bearing)

From `skills/unslop/SKILL.md` — reinforced by Agent #67, #68, #69, #70:

- **Defensive use:** ESL false positives, resume writers, journalism register restoration
- **Not:** academic misconduct tooling, guaranteed evasion, native-washing
- **Ethical alignment:** OpenAI cited ESL stigma when withholding watermark; FTC sanctioned inflated detector claims; institutions disabled tools citing same equity harms Liang documented

### 4.5 Competitive context (Superhuman / QuillBot)

- **Superhuman/Grammarly:** detection + humanizer + Authorship in one bundle; RAID #1 marketing vs paraphrase reality gap; unslop wins on preservation + honest positioning, loses on distribution.
- **QuillBot:** L1 paraphraser; Turnitin names it explicitly; 25–47% bypass panels — **polish tool, not bypass**. unslop is not "QuillBot alternative on evasion."

---

## 5. Bottom line

August 2026 commercial detection is an **arms race with honest uncertainty**. Vendors retrain monthly on humanizer outputs; institutions retreat from high-stakes classifier use; the generator (OpenAI) abandoned post-hoc text scoring; independent audits show **detector-specific** outcomes under paraphrase — especially **GPTZero vs Pangram** divergence.

For unslop:

1. **Turnitin + GPTZero** = default education threat model; **Originality Turbo** = hardest single check; **Pangram** = admissions divergence watch.
2. **Marketing numbers are conditional truths** — always name arm, metric, model date.
3. **Anti-detector stays defensive** — institutional retreat and Liang supply the warrant; not bypass marketing.
4. **Fix attribution errors** before citing Booth anywhere Turnitin or twelve-humanizer claims appear.

Deterministic unslop improves voice and reduces false-positive risk; it does **not** guarantee clearance against 2026 retrained ensembles. Cross-model second pass + process evidence (drafts, Authorship) beat single-pass optimization.

---

## 6. Source index (primary)

| Resource | URL |
|----------|-----|
| Jabarian & Imas — Booth working paper | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| GPTZero Booth rebuttal | https://gptzero.me/news/chicago-booth-2026/ |
| GPTZero technical report | https://arxiv.org/abs/2602.13042 |
| DAMAGE (humanizer collapse) | https://arxiv.org/abs/2501.03437 |
| Liang ESL (*Patterns*) | https://doi.org/10.1016/j.patter.2023.100779 |
| Turnitin bypasser press release | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers |
| Originality AI Allowance | https://originality.ai/blog/introducing-ai-allowance |
| Copyleaks V10 methodology | https://copyleaks.com/ai-detector/testing-methodology |
| OpenAI classifier shutdown | https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ |
| FTC Content at Scale order | https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-approves-final-order-against-workado-llc-which-misrepresented-accuracy-its-artificial |
| Vanderbilt disable guidance | https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/ |
| Curtin disable (Jan 2026) | https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/ |
| Superhuman acquires GPTZero | https://blog.superhuman.com/superhuman-to-acquire-gptzero/ |

### Input memos

| Agent | Topic |
|-------|-------|
| [#56](./AGENT-56-TURNITIN-2025-2026.md) | Turnitin 2025–26 |
| [#57](./AGENT-57-GPTZERO-EVOLUTION.md) | GPTZero / Superhuman |
| [#58](./AGENT-58-ORIGINALITY-AI-ALLOWANCE.md) | Originality 3.0 + Allowance |
| [#59](./AGENT-59-COPYLEAKS-V9.md) | Copyleaks ensemble |
| [#60](./AGENT-60-PANGRAM-VS-GPTZERO-PARAPHRASE.md) | Pangram vs GPTZero paraphrase |
| [#62](./AGENT-62-CHICAGO-BOOTH-2026.md) | Booth benchmark |
| [#67](./AGENT-67-MARKETING-VS-AUDIT.md) | Marketing vs audit |
| [#68](./AGENT-68-ESL-INDUSTRY-RESPONSE.md) | ESL industry response |
| [#69](./AGENT-69-INSTITUTIONAL-RETREAT.md) | Institutional retreat |
| [#70](./AGENT-70-OPENAI-CLASSIFIER-SHUTDOWN.md) | OpenAI shutdown |

---

*SYNTH-82 complete. Feeds UPDATE-PLAN Phase 4 (dual reporting), README honesty pass, `drafts/2026-05-detector-test/` protocol.*
