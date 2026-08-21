# Agent #68 — ESL False-Positive Industry + Academic Response

**Topic:** How Turnitin, GPTZero, Pangram, peer reviewers, and universities responded to Liang et al. ESL bias findings (2023–2026)  
**Prepared:** August 19, 2026  
**Scope:** Vendor statements, product changes, institutional policy, follow-up research, litigation, civil-rights framing — not a re-derivation of Liang mechanism (see Agent #18)  
**Status:** complete

---

## Executive summary

Liang et al. (*Patterns*, July 2023; arXiv:2304.02819) did not just publish numbers — it forced a **four-year accountability arc** across vendors, campuses, courts, and regulators. The headline **61.22% mean false-positive rate** on 91 human TOEFL essays (vs **5.19%** on US 8th-grade native essays) became the equity anchor every stakeholder had to address.

Industry responses sorted into four modes:

| Mode | Who | Example |
|------|-----|---------|
| **Deny / rebut** | Originality.ai | "Flawed Stanford study"; swap TOEFL for IELTS corpus |
| **"Outdated narrative"** | GPTZero | Oct 2023 blog: 1.1% FPR on same 91 essays post-debias |
| **Benchmark arms race** | Pangram | 0% on Liang TOEFL set; 25k-essay ESL eval (Apr 2025) |
| **Acknowledge + tune** | Turnitin | Oct 2025 L2 protections; own ELL eval blog; hide 1–19% band |

Universities largely **exited or restricted** high-stakes detector use — Vanderbilt (Aug 2023), UBC (declined enablement Apr 2023), Waterloo (disabled Sep 2025), Curtin (Jan 2026). **60+ institutions** in tracker summaries cite unreliability and/or ESL equity. Academic follow-ups are mixed: Al Ali et al. (EACL 2026 SRW) finds **23.1%** FPR on Liang TOEFL with a 2025 detector (down from 61%, still **23×** native baseline); Chicago Booth (2025) shows ≤1% FPR on general corpora but **does not stratify by L1**. Civil society (CDT) and ED OCR (Nov 2024) framed disproportionate ESL flagging as potential **Title VI** exposure.

**2026 verdict:** Vendors claim closure; independent English replication and live failures (Adelphi Turnitin 100%, Waterloo internal 100%) say otherwise. The **91-essay Liang set** is now a fixed community benchmark — not because it is perfect, but because everyone re-runs it. unslop should cite Liang for **why anti-detector exists**, treat vendor 0% claims as first-party until independently replicated, and never promise permanent detector pass.

---

## 1. The trigger (brief — full analysis in Agent #18)

| Event | Date | What happened |
|-------|------|---------------|
| Preprint | Apr 2023 | arXiv:2304.02819 posted |
| Turnitin AI launch | Apr 2023 | LMS detection ships; WaPo pre-launch FP story cited in *Patterns* editorial |
| *Patterns* Opinion | Jul 10, 2023 | Peer-reviewed editorial; DOI [10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779) |
| Stanford HAI | Jul 2023 | Public explainer; Zou: avoid detectors in ESL-heavy settings |
| Fixed benchmark born | Jul 2023+ | 91 TOEFL essays become held-out equity set |

**Load-bearing numbers (unchanged in discourse):**

- TOEFL mean FPR: **61.22%** (7 detectors, Mar 15, 2023 snapshot)
- ≥1 detector flagged: **97.80%** (89/91)
- Unanimous false flags: **19.78%** (18/91)
- Native ASAP baseline: **5.19%**

Turnitin was **not** in Liang's seven-detector panel (launched after access date; 300-word minimum excludes most TOEFL essays). GPTZero **was** — part of the 61% mean.

---

## 2. Response taxonomy

Understanding vendor and institutional moves requires separating **rhetoric** from **product change**:

```
Liang publication
       │
       ├─ DENY ─────────── Originality: methodology flawed; different corpus
       │
       ├─ REFRAME ──────── GPTZero: "outdated narrative"; we fixed it first
       │
       ├─ OUTPERFORM ───── Pangram: hold out Liang set; publish 0% + larger ESL evals
       │
       ├─ ACKNOWLEDGE ──── Turnitin: L2 tuning, score suppression, ELL blog study
       │
       ├─ EXIT ─────────── OpenAI: withdraw public classifier Jul 2023
       │
       └─ INSTITUTIONAL ── Disable / restrict; require process evidence; litigation
```

**Equity–evasion isomorphism** (Liang § intervention) constrains every "fix": vocabulary enrichment that removes ESL false positives is the same transform that evades detectors on real AI text. Vendors cannot claim full ESL closure without admitting their own historical harm; institutions cannot rely on scores without accepting asymmetric risk on L2 writers.

---

## 3. Chronological timeline (2023–2026)

| Date | Actor | Response |
|------|-------|----------|
| **Apr 2023** | Turnitin | AI writing detection launches; claims <1% FP, 97% GPT-3 detection |
| **Apr 2023** | Washington Post | Pre-launch test: innocent student flagged; Turnitin later said tool "not always reliable" |
| **Jul 2023** | Liang / *Patterns* / HAI | 61% TOEFL FPR published; Zou calls for curtailment in education |
| **Jul 2023** | OpenAI | Public classifier withdrawn (~26% TP / 9% FP on their eval) |
| **Aug 16, 2023** | **Vanderbilt** | **Disables Turnitin AI detector**; cites 750 potential FPs/year at 1% × 75k papers + ESL bias (Myers/HAI) |
| **Aug–Sep 2023** | Northwestern, UT Austin, others | Disable or discourage (Inside Higher Ed Feb 2024 roundup) |
| **Apr 4, 2023** | **UBC** | Declines to enable Turnitin AI feature — insufficient vetting |
| **Oct 19, 2023** | **GPTZero** | Blog: "ESL Bias in AI Detection is an Outdated Narrative"; 1/91 TOEFL essays flagged AI |
| **Oct 2023** | Pangram technical report | Re-runs Liang 91-essay set: **0% FPR**; notes GPTZero still **7.7%** (1.1% generous) |
| **2023–24** | Originality.ai | Rebuttal blog: flawed sample, IELTS comparison, v1.4 "100% on AI sets" |
| **Autumn 2023** | GPTZero | Deep-learning pivot; perplexity demoted to explainability UI |
| **2024** | GPTZero Substack | "Million Teacher Question": de-biased model, 1% ESL FPR target, AFT partnership |
| **2024** | Turnitin | 1–19% score suppression as `*%`; sentence-level FP revised upward in discourse (~4%) |
| **Aug 2024** | Turnitin whitepaper | AIW-2 + AIR-1 architecture published |
| **Aug 2024** | ETS (GRE study) | ~2k non-native samples; in-house detectors show no bias when L2 represented in training (simplified setting; no commercial tools) |
| **Apr 2025** | Pangram ESL blog | 25,021-essay ESL eval; 0% on Liang TOEFL; L2 0.02% vs Turnitin L2 1.4% (same datasets) |
| **Sep 2025** | Jabarian & Imas (Booth) | Independent audit: ≤1% FPR on general human corpus; **no L1 stratification** |
| **Sep 2025** | **University of Waterloo** | **Discontinues Turnitin AI detection**; cites Liang lineage + internal test flagging human text **100% AI** |
| **Oct 14, 2025** | Turnitin | Model refresh; "non-native English speaker protections"; formalized `*%` for 1–19% |
| **Nov 2024** | US ED OCR | AI discrimination resource: plagiarism AI on non-native essays → potential **Title VI** investigation |
| **2024–25** | CDT | Legal brief: disproportionate ESL flagging + discipline = civil-rights concern |
| **Jan 2026** | GPTZero | Chicago Booth rebuttal; arXiv:2602.13042 technical report (multilingual bench) |
| **Jan 2026** | **Curtin University** | **Disables Turnitin AI detection** (effective Jan 1, 2026); originality check remains |
| **Jan 2026** | **Matter of Newby v. Adelphi** | Turnitin 100% annulled; neurodivergent student; contradictory tools ignored |
| **Feb 2026** | Turnitin | English model refresh; FP "held below 1%" per vendor |
| **EACL 2026** | Al Ali et al. | English Liang replication: Plagramme **23.1%** FPR on TOEFL-91 vs **0%** native Hewlett |

---

## 4. Vendor responses (deep dive)

### 4.1 Turnitin

Turnitin was absent from Liang's original panel but became the **default LMS detector** and the primary litigation target post-2023.

| Phase | Action | Evidence tier |
|-------|--------|---------------|
| Launch (Apr 2023) | <1% document FP (scores ≥20%); instructor-only visibility | [F] vendor |
| Pre-Liang context | WaPo innocent-student flag; cited in *Patterns* editorial | [P] press |
| 300-word minimum | Won't score Liang-length TOEFL essays (~150 words) | [F] model guide |
| Jul 2024 | Suppress 1–19% as `*%` — higher FP incidence acknowledged in band | [F] |
| **ELL blog study** | L1 vs L2 FPR on PELIC/ICNALE/ASAP samples; **no significant L2 bias** at ≥300 words; short docs worse | [F] [blog](https://www.turnitin.com/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners) |
| Critique of Liang | TOEFL essays too short; Turnitin excluded by design | [F] same blog |
| **Oct 14, 2025** | "Non-native English speaker protections"; improved recall; L2 tuning claimed | [F] release notes + secondary blog |
| Aug 2025 | Anti-humanizer detection (English) — raises new FP risk for register-edited L2 prose | [F] |
| Feb 2026 | Model refresh | [F] |

**Turnitin rhetorical pattern:** (1) Liang corpus is wrong test (too short, not in product scope); (2) our own ELL eval shows parity at ≥300 words; (3) we tuned for L2 in Oct 2025; (4) scores are conversation starters, not proof.

**Counter-evidence:**

- Pangram first-party comparison on Turnitin's own ELL datasets: L2 FPR **1.4%** vs Pangram **0.02%** ([Pangram ESL blog](https://www.pangram.com/blog/how-accurate-is-pangram-ai-detection-on-esl), Apr 2025) — **[V]** tier (competitor-run).
- Working Educators (Philadelphia): **31% ESL FP vs 12% native** on Turnitin (150 essays) — **[I]** independent, different methodology.
- Waterloo internal test: human text flagged **100% AI** — **[F-inst]** primary.
- Newby: Turnitin **100%** on human essay; other tools disagreed; record expunged — **[L]** legal.

**Gap:** No public post-Oct-2025 ESL confusion matrix from Turnitin. "No statistically significant bias" ≠ zero harm at institutional scale.

### 4.2 GPTZero

GPTZero was in Liang's seven-detector mean and moved fastest on **"we fixed it"** messaging.

| Phase | Action | Claim on Liang TOEFL-91 |
|-------|--------|-------------------------|
| Mar 2023 (Liang snapshot) | Perplexity-era detector | Part of **61.22%** mean |
| Oct 19, 2023 | ["ESL Bias… Outdated Narrative"](https://gptzero.me/news/esl-and-ai-detection/) | **1.1%** AI; **6.6%** "possible AI" |
| Autumn 2023 | Deep-learning classifier; ESL corpus in training | Architecture change |
| 2024 Substack | First vendor to "directly address" ESL bias; 1% FPR target | [V] |
| arXiv:2602.13042 (Feb 2026) | Model 3.7m: 97.6% recall, **0.09% FPR** on 24-language vendor bench | [V] |
| Jan 2026 Booth rebuttal | 99.3% recall / 0.05% FPR on **non-ESL-stratified** Booth corpus | [V] |

**De-biasing methods disclosed (Oct 2023 blog):**

1. Education/ESL parameter tagging (CNN layer)
2. Pre-classification of likely ESL text before scoring
3. Representative dataset insertion (TOEFL, Medium 180k, Persuade 31k, Hewlett 12k)
4. Sentence-level training for short texts

**GPTZero rhetorical pattern:** Liang is six months old in AI time; we re-ran their code; n=91 is too small; our larger ESL eval shows <2% FPR.

**Counter-evidence:**

- Pangram technical report (Oct 2023): updated GPTZero still **7.7%** on same set — competitor measurement.
- Booth StealthGPT arm: GPTZero FNR **~50%+** — orthogonal to ESL but undermines "trustworthy at scale" framing (Agent #60).
- Liang intervention: "native speaker enhancement" drops FPR **61% → 12%** — same transform as evasion.

**Strategic pivot (2024–2026):** Writing Replay, Docs, Superhuman acquisition — **process provenance** alongside classification. Tian: "human conversations" over default adversarial use. ESL de-biasing remains marketing load-bearing for education sales.

### 4.3 Pangram

Pangram launched after Liang and was **never in the original seven-detector panel**. Response strategy: **own the benchmark**.

| Milestone | Action |
|-----------|--------|
| arXiv:2402.14873 (Jan 2024) | Hold out 91 TOEFL essays from training; report **0% FPR** on Liang set |
| Oct 2023 | Cites GPTZero "outdated narrative" post; reports GPTZero at 7.7% on same data |
| ICNALE eval | **0.09%** FPR on 5,600 Asian-learner essays |
| **Apr 2025 ESL blog** | Four public ESL corpora, n=25,021; overall **0.012%**; Liang TOEFL **0%** |
| vs Turnitin | Same datasets Turnitin used: L2 **0.02%** vs Turnitin **1.4%** (300+ words) |
| vs GPTZero | GPTZero self-reports 1.1% + 6.6% "possible AI" on Liang set |
| May 2026 | Pangram 3.3 update; ESL section refreshed |

**Mitigation strategies published:**

- Broad training distribution (not essays-only)
- Multilingual training → less English-native overfit
- Active learning / hard-negative mining on human text resembling AI
- Prompt diversity including "write like a nonnative English speaker"
- Large-n eval (millions of examples for sub-0.01% FPR claims)

**Pangram rhetorical pattern:** Bias is a **training-data representation** problem; perplexity detectors (historical GPTZero) fail; we solved it on the exact dataset that exposed the harm.

**Honest limits (Pangram's own words):**

- Liang n=91 is coarse; one error = 1.1% — why they need 25k+ ESL eval
- Detector fairness ≠ process fairness — educators may **selectively** scan ESL submissions
- ESL students may legitimately use ChatGPT for editing → true positives, not bias

**Independent check:** Al Ali 2026 finds **23.1%** on Liang TOEFL with Plagramme — shows "ESL solved" is **not industry-wide**, even if Pangram claims 0%.

### 4.4 Originality.ai

Originality was in Liang's panel. Response: **deny + replace corpus**.

| Claim | Originality position |
|-------|---------------------|
| Sample size | 91 TOEFL forum essays too small |
| Genre confound | TOEFL vs 8th-grade US — unfair comparison |
| GPT-4 polish label | Stanford misclassified enhanced text as human |
| Stale detector | Liang used v1.1; v1.4+ fixes everything |
| Own eval | 1,500+ IELTS essays; **5.04% FPR** vs Stanford's 61.3% |

**Notable tension:** Blog simultaneously argues (a) no ESL bias in IELTS eval and (b) **"Originality.AI is not for academic use"** — trained on web/SEO content, not student essays. Academic ESL false positives framed as out-of-distribution, not equity failure.

**2025–26:** Monthly retraining (Lite/Turbo/Academic); humanizer resistance marketing. ESL rebuttal remains static rebuttal, not a published Liang replication with version pinning.

### 4.5 OpenAI, Copyleaks, others

| Vendor | ESL-specific response |
|--------|----------------------|
| **OpenAI** | Withdrew public classifier Jul 2023; no ESL de-bias program — exited |
| **Copyleaks** | Multilingual expansion; no published Liang replication |
| **ZeroGPT / Sapling / Crossplag** | Named in Liang; no major public ESL response tracked |
| **Grammarly/Superhuman** | **Authorship** keystroke provenance — sidesteps post-hoc ESL classification |

---

## 5. Academic and research response

### 5.1 Immediate amplification (2023)

| Outlet | Role |
|--------|------|
| *Patterns* (Cell Press) | Opinion piece; legitimizes equity frame for citation |
| Stanford HAI | 61% headline enters policy discourse |
| Times Higher Education | "Inherently discriminate" framing for UK/EU readers |
| Washington Post / Rolling Stone / Bloomberg 2024 | False-accusation human stories |

### 5.2 Replication and extension (2024–2026)

| Study | ESL-relevant finding | vs Liang |
|-------|---------------------|----------|
| **Al Ali et al.** (EACL 2026 SRW; [arXiv:2602.05769](https://arxiv.org/abs/2602.05769)) | Plagramme on Liang TOEFL-91: **23.1% FPR**; Hewlett native: **0%** | Improved, bias persists |
| Al Ali — Czech | No native/non-native gap (different language mechanics) | English-specific |
| Al Ali — entropy correlation | Negligible on English set (ρ < 0.04) | Detectors less perplexity-pure |
| **Jabarian & Imas** (BFI WP 2025-116) | Commercial ≤1% FPR on mixed human corpus | **No L1 stratification** |
| **ETS GRE study** (Aug 2024) | No bias when L2 in training (in-house, simplified) | Does not test commercial tools |
| **Working Educators** | Turnitin 31% ESL vs 12% native FP | Live institutional data |
| **Pindrop ACL 2026** (secondary) | 16 detectors; non-White ELL flagged more; no uniform fairness | Extends equity beyond Liang L1 |

### 5.3 What academia did *not* do

- No multi-vendor **independent** Liang replication with 2026 model version strings at scale (Pangram/GPTZero numbers remain mostly first-party or competitor-measured).
- Booth — the most-cited 2025 audit — ** omitted ESL stratification** despite Liang being the reason institutions cite FP risk.
- Peer review has not produced a consensus "ESL FPR bar" (e.g., ≤0.5% on L1-stratified data) binding on vendors.

---

## 6. University and institutional response

### 6.1 Policy patterns

Three recurring moves:

1. **Disable detector feature** (keep similarity/originality)
2. **Advisory-only** — score starts conversation, cannot be sole evidence
3. **Process evidence** — drafts, Authorship/Replay, in-class writing, interviews

### 6.2 Canonical cases

| Institution | Date | Action | Liang / ESL cited? |
|-------------|------|--------|-------------------|
| **Vanderbilt** | Aug 16, 2023 | Disable Turnitin AI | Yes — HAI/Myers; arithmetic 750 FPs/yr |
| **UBC** | Apr 4, 2023 | Never enabled AI feature | Accuracy/vetting; not sole Liang cite |
| **Northwestern, UT Austin** | 2023–24 | Disabled / discouraged | Via IHE roundup |
| **Yale** (Poorvu) | 2025–26 | Cannot cite detector scores in formal complaints | FP rates vs burden of proof |
| **Johns Hopkins** | 2025–26 | Advisory only | — |
| **University of Waterloo** | Sep 2025 | **Discontinue** Turnitin AI | Yes — Leong/Rafiq/Liang lineage + 100% internal FP |
| **Curtin** | Jan 1, 2026 | **Disable** AI detection | Equity/trust framing; student guild notes paraphrase still misconduct |
| **University of Twente** | 2026 | No proof without investigation | — |

**Vanderbilt arithmetic** (most cited institutional logic):

> 75,000 papers × 1% claimed FP = **750 false accusations/year**

ESL bias cited as **additional** equity layer, not the only reason.

**Waterloo** (strongest 2025 primary):

> Internal testing flagged human-written text as **100% AI-generated** — plus peer-reviewed unreliability and ESL bias literature.

Tracker aggregators (GradPilot, DetectionDrama) list **60+** institutions — treat as **[S]** secondary unless primary URL verified.

### 6.3 What most institutions did *not* do

- Mandate vendor ESL audits before purchase
- Require L1-stratified FP reporting in RFPs
- Uniform policy — 2026 landscape is patchwork (some departments still use GPTZero directly)

---

## 7. Legal, regulatory, and civil-society response

| Actor | Date | Response |
|-------|------|----------|
| **CDT** | 2024–25 | Legal brief: disproportionate ESL flagging → Title VI theories (disparate impact, hostile environment) |
| **US ED OCR** | Nov 20, 2024 | [Avoiding Discriminatory Use of AI](https://www.ed.gov/media/document/avoiding-discriminatory-use-of-artificial-intelligence-112274.pdf): AI plagiarism tool with higher error on non-native essays → investigation grounds under **Title VI** |
| **Matter of Newby v. Adelphi** | Jan 2026 | Turnitin 100%; disabilities ignored; annulment — process defect, not ESL-specific but same black-box pattern |
| **Kato v. Palo Alto USD** | filed 2026 | Turnitin 76%; pending |
| **Rignol v. Yale** | pending | GPTZero on SOM application |
| **Yang v. U. Minnesota** | appeal lost | GPTZero + faculty on dissertation — detectors still used despite controversy |

**Regulatory takeaway:** Liang supplies the **scientific predicate** for civil-rights framing; OCR supplies the **enforcement hook**. Institutions using detectors as sole evidence on ESL-heavy cohorts carry legal exposure independent of vendor "<1%" marketing.

---

## 8. Fixed benchmark evolution (the arms race on Liang TOEFL-91)

| Evaluator | Year | FPR on 91 essays | Source tier |
|-----------|------|------------------|-------------|
| 7-detector mean (Liang) | 2023 | **61.22%** | [A] peer-reviewed |
| GPTZero (post-debias) | Oct 2023 | **1.1%** (+ 6.6% "possible") | [V] first-party |
| Pangram | 2024 | **0%** | [V] first-party |
| GPTZero (Pangram-measured) | 2024 | **7.7%** | [V] competitor |
| Plagramme (Al Ali) | 2025 | **23.1%** | [A] independent |
| Pangram (Apr 2025 blog) | 2025 | **0%** | [V] first-party |

**Bias multiplier vs ~5% native baseline:** ~12× (2023) → **0–4×** (2024–25 vendor claims) → **~23×** still (Al Ali Plagramme vs 0% native).

The benchmark is **stale by design** (fixed essays, Chinese L1 only, exam register) — but it is the **only cross-vendor equity ruler** the industry agreed to fight over.

---

## 9. What changed vs what did not (August 2026)

### Changed

- Vendors **cannot ignore** ESL equity in marketing; all major players publish de-bias or ELL eval language
- Mean FPR on Liang set dropped from **61%** toward **0–23%** depending on vendor/year
- **60+ institutions** restricted or disabled LMS AI detection
- **Process provenance** (Replay, Authorship, Clarity) pivots partially **because** classifiers failed equity tests
- OCR/CDT elevated FP from "accuracy debate" to **civil-rights compliance**

### Did not change

- **No vendor** publishes independent ESL confusion matrices with version-pinned 2026 models under adversarial conditions (humanizer + L2)
- **High-stakes failures continue** (100% scores, annulled only after litigation)
- Booth and most 2025 audits still **ignore L1 stratification**
- Liang **equity–evasion isomorphism** unresolved — fairer detectors remain evadable
- Humanizers market using the same Liang stats defenders use

---

## 10. unslop integration

### 10.1 Why this memo matters for unslop

Agent #68 is the **stakeholder response layer** atop Agent #18 (mechanism). It documents:

- **Legitimate use case warrant:** institutions and courts still harm L2 writers when detectors misfire
- **Marketing hazard:** vendor "0% ESL" ≠ user's detector at submission time
- **Boundary enforcement:** same register shifts that fix bias enable evasion — `/unslop anti-detector` stays defensive

### 10.2 Recommended messaging (Aug 2026)

> Liang (2023) proved 2023-era detectors punished predictable L2 prose. Vendors say they fixed it; Al Ali (2026) still finds 23% FPR on the same 91 essays with at least one 2025 tool. Vanderbilt, Waterloo, and Curtin disabled Turnitin AI anyway.
>
> unslop anti-detector mode reduces false-positive risk via burstiness, contractions, and specificity — not "sound native." It is not a guarantee against Turnitin, GPTZero, or Pangram.

### 10.3 Doc actions (cross-ref UPDATE-PLAN-2026-08)

| Item | Action |
|------|--------|
| SKILL.md Boundaries | Cite Liang as **2304.02819** (not 2306.04723) |
| README equity case | Keep Vanderbilt arithmetic + Liang 61% as historical harm |
| Bench corpus | Add L1-stratified reporting in `drafts/2026-05-detector-test/` |
| Vendor claims | Never cite Pangram 0% or GPTZero 1.1% without "first-party, fixed benchmark" caveat |

### 10.4 What unslop should NOT do

| Action | Why |
|--------|-----|
| "Beat Turnitin after Oct 2025 L2 protections" | No public ESL matrix; anti-humanizer layer |
| "Pangram-proof" | Competitor-measured; admissions offices use Pangram precisely because GPTZero greens |
| "ESL bias solved in 2026" | Al Ali 23.1%; live 100% failures |
| Native-washing prompts | Liang used as scientific intervention; ethically coercive as product default |

---

## 11. Cross-references (unslop research agents)

| Agent | Connection |
|-------|------------|
| **#18** | Liang mechanism, intervention, evasion isomorphism — upstream |
| **#56** | Turnitin Oct 2025 L2 protections; Curtin disable |
| **#57** | GPTZero ESL de-bias arc; Superhuman pivot |
| **#60** | Booth/GPTZero/Pangram — paraphrase axis orthogonal to ESL |
| **#62** | Booth lacks ESL stratification — attribution fix |
| **#58** | Originality allowance / rebuttal lineage |

---

## 12. Open gaps

1. Independent 2026 multi-vendor Liang replication with API version strings (GPTZero `2025-12-18-base`, Pangram 4, Turnitin post-Feb 2026)
2. Turnitin post-Oct-2025 ESL FPR — vendor-only claims
3. L1 diversity beyond Chinese TOEFL (Arabic, Spanish, Hindi) in peer-reviewed vendor evals
4. Intersection: ESL × neurodivergent × tutoring-assisted (Newby pattern)
5. Booth + Liang intersection — policy-cap analysis on L1-stratified subsample
6. Whether institutional **exit wave** accelerates after Newby (Jan 2026) — early signal only

---

## 13. Primary source table

| # | Source | Year | URL |
|---|--------|------|-----|
| 1 | Liang et al. — *Patterns* | 2023 | https://doi.org/10.1016/j.patter.2023.100779 |
| 2 | Stanford HAI summary | 2023 | https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers |
| 3 | Vanderbilt disable guidance | 2023 | https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/ |
| 4 | GPTZero "Outdated Narrative" | 2023 | https://gptzero.me/news/esl-and-ai-detection/ |
| 5 | Pangram technical report (ESL §) | 2024 | https://arxiv.org/abs/2402.14873 |
| 6 | Pangram ESL blog | 2025 | https://www.pangram.com/blog/how-accurate-is-pangram-ai-detection-on-esl |
| 7 | Turnitin ELL bias blog | 2024+ | https://www.turnitin.com/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners |
| 8 | Turnitin AI model guide | 2025–26 | https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model |
| 9 | Originality.ai rebuttal | 2023+ | https://originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers |
| 10 | Waterloo discontinue | 2025 | https://uwaterloo.ca/associate-vice-president-academic/discontinuing-use-ai-detection-functionality-turnitin |
| 11 | Curtin disable | 2026 | https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/ |
| 12 | Al Ali et al. — EACL 2026 SRW | 2026 | https://arxiv.org/abs/2602.05769 |
| 13 | Jabarian & Imas — Booth | 2025 | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| 14 | US ED OCR AI guidance | 2024 | https://www.ed.gov/media/document/avoiding-discriminatory-use-of-artificial-intelligence-112274.pdf |
| 15 | CDT ESL brief | 2024–25 | https://www.einpresswire.com/article/675948844/brief-late-applications-disproportionate-effects-of-generative-ai-detectors-on-english-learners |
| 16 | Washington Post pre-launch | 2023 | https://www.washingtonpost.com/technology/2023/04/01/chatgpt-cheating-detection-turnitin/ |
| 17 | Times Higher Education | 2023 | https://www.timeshighereducation.com/news/ai-text-detectors-biased-against-non-native-english-speakers |
| 18 | GPTZero technical report | 2026 | https://arxiv.org/abs/2602.13042 |
| 19 | Bloomberg false accusations | 2024 | https://www.bloomberg.com/news/features/2024-10-18/do-ai-detectors-work-students-face-false-cheating-accusations |

---

## 14. Evidence tier key

| Tier | Meaning |
|------|---------|
| **[A]** | Peer-reviewed / working paper |
| **[F]** | Vendor first-party |
| **[F-inst]** | Institution first-party |
| **[I]** | Independent test (named methodology) |
| **[L]** | Legal record |
| **[P]** | Press |
| **[S]** | Secondary aggregator (verify primary) |
| **[V]** | Vendor or competitor-measured benchmark |

---

## 15. Unslop verdict (one paragraph)

Liang did not end the detector industry — it forced every player to pick a response script. Turnitin acknowledged L2 risk while disputing the test corpus; GPTZero declared bias "outdated" and re-ran the 91 essays; Pangram built its credibility by reporting **0%** on that exact set; Originality called the study flawed; universities from Vanderbilt to Curtin **turned the feature off** anyway; OCR and CDT reframed false positives as civil-rights risk. By 2026, headline FPR on the fixed benchmark fell from **61%** to **0–23%** depending on who measures — but independent English replication still shows gap, Booth ignores L1, and 100% Turnitin scores keep reaching courts. unslop cites this arc to justify **anti-detector as false-positive defense**, not vendor defeat, and treats every "ESL solved" claim as dated until stratified, version-pinned, independently replicated.

---

*Agent #68 complete. Upstream: Agent #18 (Liang mechanism). Downstream: README equity copy, SKILL Boundaries citation fix, bench L1 reporting.*
