# Agent #69 — Institutional Detector Retreat (Universities)

**Topic:** Universities that disabled, banned, or declined AI writing detectors — timeline 2024–2026, stated reasons, policy debate, unslop positioning  
**Prepared:** August 19, 2026  
**Scope:** Primary institutional statements, PLEASE registry, GradPilot tracker, litigation (2025–2026), counter-trend (schools still running detectors), unslop integration  
**Status:** complete

---

## Executive summary

Between April 2023 and early 2026, a **documented wave** of universities disabled Turnitin's AI writing indicator, banned third-party detectors, or never enabled detection at all. No authoritative census exists; the best-maintained community list is the **PLEASE registry** (~66 institutions as of Sep 2024, still growing). GradPilot's 2026 tracker puts the documented total at **60+ across five countries** (US, Canada, UK, Australia, South Africa). Detection Drama's top-50 analysis (Jun 2026) finds **35 of 50** elite US schools have Turnitin AI detection disabled or unused; only **2** (Georgia Tech, University of Georgia) clearly keep it on.

The retreat is **not universal**. Many institutions still run Turnitin AI scores, GPTZero, or Copyleaks — often with "advisory only" language. The landscape is **patchwork**: institution-level disable does not stop individual instructors from buying GPTZero with a personal card (though UT Austin now blocks that path).

**Four reasons recur** in primary statements:

1. **False positives at scale** — Vanderbilt's arithmetic (1% × 75,000 papers = 750 wrongful flags/yr) became the template. WSU (Feb 2026) estimated **~1,485** false flags in one semester at Turnitin's own 1% claim. Waterloo internal tests flagged human prose **100% AI**.
2. **ESL / equity bias** — Liang et al. (2023) and follow-ups cited by Waterloo, Vanderbilt, WSU, Curtin. Federal and state guidance (US Dept of Education OCR, WV/NC education depts) now frames detector bias as a civil-rights concern.
3. **Black-box opacity + due process** — Scores students cannot see or contest; Northwestern, Manchester, Turnitin itself say detection cannot be sole evidence. **Newby v. Adelphi** (NY Sup. Ct., Jan 28, 2026) annulled a Turnitin-100% finding as "without valid basis."
4. **Privacy / IP / FERPA** — UC Berkeley, UT Austin classify unauthorized detector submission as high-risk; student work is an educational record.

**Policy replacement:** assessment redesign, AI literacy, process evidence (drafts, oral defense, AI-use statements). Similarity checking stays; classifier layer goes.

**Unslop honest positioning:** Institutional retreat validates the **ESL false-positive defense** framing for `/unslop anti-detector` — it does **not** validate evasion marketing. README and SKILL.md should cite **Vanderbilt (2023)** and **Waterloo/Curtin (2025–26)** as policy anchors, not "beat Turnitin." Cross-ref Agent #18 (Liang), #56 (Turnitin vendor moves), #68 (ESL industry response).

---

## 1. Timeline — institutional actions (2023–2026)

### 1.1 Phase 0: Turnitin launch and immediate pushback (Apr–Dec 2023)

| Date | Event | Significance |
|------|-------|--------------|
| **Apr 4, 2023** | Turnitin ships AI writing detection to existing customers | Enabled by default; <24 hr notice (Vanderbilt complaint) |
| **Apr 4, 2023** | **UBC declines to enable** | First major refusal same week as launch |
| **Jun 2023** | **U. Pittsburgh** Teaching Center disables; endorses no detector | Early R1 exit |
| **Jul 3, 2023** | **Boston University** disables AI score panel | False positives; no efficacy evidence |
| **Jul 20, 2023** | **OpenAI shuts down** its classifier | Low accuracy — undercuts detector confidence industry-wide |
| **Aug 16, 2023** | **Vanderbilt disables** campuswide | Canonical rationale post — arithmetic, ESL, opacity, privacy |
| **Oct 2023** | **Georgetown disables** | Faculty exec + Honor Council: FP harms > benefits |
| **2023** | Northwestern, Michigan State, Macquarie (AU), Dundee (UK), Deakin (AU) | Pilot-then-disable or never-enable pattern |

**Turnitin FP revision (industry context):** The Register and Inside Higher Ed reported Turnitin quietly revising claimed sentence-level FP from **<1% to ~4%** mid-2023 — schools that did Vanderbilt math with 1% were already understating risk.

### 1.2 Phase 1: Formal bans and procurement blocks (2024)

| Date | Institution | Action |
|------|-------------|--------|
| **Jan 1, 2024** | **ANU (Australia)** | Disabled Turnitin AI writing detection |
| **Jan 2024** | **Western University (Canada)** | Removed Turnitin AI detection |
| **2024** | **Yale** | Disabled; Poorvu Center does not endorse detectors for high-stakes use |
| **2024** | **UC Berkeley, UCLA, UC Irvine** | Opted out / deactivated |
| **2024** | **Johns Hopkins** | Advisory only; not endorsed |
| **2024–25** | **UT Austin** | No central ADS contracts; Procard/personal purchase **prohibited**; FERPA + student IP framing |
| **2024** | **U. Manchester (UK)** | AI detection "must not be used" as evidence in summative assessment |
| **2024–25** | **West Virginia / North Carolina** state education depts | Official guidance: do **not** use AI detectors |

### 1.3 Phase 2: Scandal-driven exits and litigation pressure (2025)

| Date | Institution | Action | Trigger / detail |
|------|-------------|--------|------------------|
| **Mar 17, 2025** | **Australian Catholic University** | Pilot-off then abandoned Turnitin AI indicator | ~6,000 misconduct referrals in 2024 (~90% AI-related); ~25% dismissed; ABC investigation |
| **Sep 2025** | **University of Waterloo** | Discontinued Turnitin AI detection | Named studies (Perkins, Weber-Wulff, Sadasivan); internal 100% FP on human text |
| **Oct 1, 2025** | **UCT (South Africa)** | Scraps Turnitin AI Score | Senate-endorsed AI in Education Framework; "education not surveillance" |
| **Jan 28, 2026** | **Newby v. Adelphi** (court) | Turnitin-100% finding annulled | Autistic student; contradictory tools ignored — process-defect precedent |
| **Jan 1, 2026** | **Curtin (Australia)** | Disables Turnitin AI detection all campuses | Originality checking stays; reliability + equity |

### 1.4 Phase 3: R1 contract cancellations (2026)

| Date | Institution | Action | Detail |
|------|-------------|--------|--------|
| **Feb 2026** | **Washington State University** | Cancelled Turnitin **AI detection contract** | 148,547 assessments Fall 2024; ~1,485 FP at 1%; 33% of AI integrity hearings → not responsible when detector was sole evidence |
| **2026** | **Detection Drama top-50 audit** | 35/50 disabled; 2/50 clearly enabled | Georgia Tech + UGA outliers among elites |

**Trend line:** Early exits (2023) were **Turnitin-toggle** decisions by teaching centers. Later exits (2025–26) cite **named research**, **internal validation failures**, and **litigation/ombudsman** pressure. Vendor response (Turnitin Oct 2025 ESL tuning, Aug 2025 bypasser detection) has **not reversed** the retreat at institutions that already left.

---

## 2. Institution inventory (verified tiers)

### 2.1 Evidence tiers for this memo

| Tier | Meaning |
|------|---------|
| **[P]** | Primary — institution's own dated policy page, provost memo, or news office |
| **[R]** | Registry — PLEASE or GradPilot with link to primary |
| **[S]** | Secondary — press (ABC, Bloomberg, Inside Higher Ed) citing primary |
| **[A]** | Aggregator — Detection Drama, Edcafe; verify before quoting |

### 2.2 Canonical cases (cite these five)

| Institution | Date | Action | Primary reason (their words) | Source tier |
|-------------|------|--------|-------------------------------|-------------|
| **Vanderbilt** | Aug 16, 2023 | Disabled Turnitin AI detector | ~750 FP/yr at 1%; ESL bias; opacity; privacy | **[P]** |
| **Georgetown** | Oct 2023 | Turned off AI writing detection | "Harms of false positives worse than the advantages" | **[P]** |
| **UT Austin** | 2024–25 | No ADS contracts; procurement ban | FERPA; student IP; high-risk software | **[P]** |
| **U. Waterloo** | Sep 2025 | Discontinued Turnitin AI detection | Unreliable; bias; human text flagged 100% AI | **[P]** |
| **Curtin** | Jan 1, 2026 | Disabled AI detection; similarity stays | Trust, fairness, future-ready assessment | **[P]** |

### 2.3 United States — banned or disabled (PLEASE "Banned" category + tracker)

**Fully banned / disabled with public statement** (sample; not exhaustive):

| Institution | Action | Date | Source |
|-------------|--------|------|--------|
| American University | Banned ADS in assessment policy | — | PLEASE **[R]** |
| Boston University | Disabled Turnitin AI panel | Jul 2023 | PLEASE, GradPilot **[R]** |
| Colorado State | AI detection unavailable | — | PLEASE **[R]** |
| DePaul | Banned detectors | — | PLEASE **[R]** |
| Georgetown | Disabled | Oct 2023 | **[P]** |
| Indiana University | About AI detection — not for misconduct | — | PLEASE **[R]** |
| Johns Hopkins | Advisory only | 2024–25 | GradPilot **[R]** |
| Michigan State | Turnitin AI not available | 2023 | PLEASE **[R]** |
| MIT Sloan EdTech | "AI Detectors Don't Work" guidance | 2023+ | **[P]** |
| Montclair State | Not recommended | — | PLEASE **[R]** |
| Northwestern | Disabled after pilot | 2023–24 | PLEASE **[R]** |
| NYU | Disabled Turnitin AI tool | — | PLEASE **[R]** |
| Oregon State | Disabled | — | PLEASE **[R]** |
| RIT | Unreliability statement | — | PLEASE **[R]** |
| SMU | Removed AI detection feature | — | PLEASE **[R]** |
| Syracuse | Detecting AI — not endorsed | — | PLEASE **[R]** |
| UC Berkeley / UCLA / UCI | Opted out | 2024–25 | PLEASE, GradPilot **[R]** |
| U. Maryland | Turned off detector | — | PLEASE **[R]** |
| U. Michigan-Dearborn | "Only winning move is not to play" | — | PLEASE **[R]** |
| U. Pittsburgh | Teaching Center doesn't endorse | Jun 2023 | **[P]** |
| U. Southern Maine | Not recommended | — | PLEASE **[R]** |
| U. Washington | Opted out SimCheck AI | — | PLEASE **[R]** |
| Vanderbilt | Disabled | Aug 2023 | **[P]** |
| **Washington State U.** | **Cancelled AI detection contract** | **Feb 2026** | **[P]** |
| West Chester | Disabled | — | PLEASE **[R]** |
| Western Connecticut | Stopped using | — | PLEASE **[R]** |
| Yale | Disabled | 2024 | PLEASE **[R]** |

**Recommend against / don't provide** (weaker but still retreat):

| Institution | Notes |
|-------------|-------|
| UT Austin | Procurement block — effectively bans unsanctioned use **[P]** |
| Notre Dame | Service disabled **[R]** |
| U. Missouri | Detecting AI plagiarism — caution **[R]** |
| Arizona State | Integrity guidance — no central detector **[R]** |

### 2.4 Canada

| Institution | Action | Date | Source |
|-------------|--------|------|--------|
| UBC | Declined to enable | Apr 2023 | PLEASE **[R]** |
| U. Toronto | Did not enable | 2023 | PLEASE **[R]** |
| **U. Waterloo** | Discontinued | Sep 2025 | **[P]** |
| Western University | Stopped using | Jan 2024 | PLEASE **[R]** |
| Simon Fraser | Turnitin AI off | — | PLEASE disabled-only **[R]** |

### 2.5 United Kingdom

| Institution | Action | Source |
|-------------|--------|--------|
| U. Manchester | Must not use in summative assessment | PLEASE **[R]** |
| U. Dundee | Opted out at launch | Apr 2023, GradPilot **[R]** |
| U. Portsmouth | Banned | PLEASE **[R]** |
| U. South Wales | Statement against ADS | PLEASE **[R]** |
| Newcastle, Glasgow, Nottingham | Discourage / update guidance | PLEASE **[R]** |
| Edinburgh, Greenwich | Turnitin AI disabled, no broad ban | PLEASE disabled-only **[R]** |

### 2.6 Australia & New Zealand

| Institution | Action | Date | Source |
|-------------|--------|------|--------|
| ANU | Disabled | Jan 1, 2024 | PLEASE **[P]** |
| Macquarie | Disabled | 2023 | PLEASE **[R]** |
| U. Canberra, UniSA | Disabled | — | PLEASE **[R]** |
| Charles Sturt, Deakin | Banned | — | PLEASE **[R]** |
| **ACU** | Abandoned after pilot | Mar 2025 | ABC **[S]** |
| **Curtin** | Disabled all campuses | Jan 1, 2026 | **[P]** |

### 2.7 Africa

| Institution | Action | Date | Source |
|-------------|--------|------|--------|
| **UCT** | No Turnitin AI Score | Oct 1, 2025 | UCT News **[P]** |

### 2.8 Institutions still using detectors (counter-trend)

Documented **enabled** or active use (Aug 2026):

| Institution | Tool | Notes | Source tier |
|-------------|------|-------|-------------|
| Georgia Tech | Turnitin AI | One of 2 top-50 clearly on | Detection Drama **[A]** |
| U. Georgia | Turnitin AI | Same | **[A]** |
| Many non-elite US colleges | Turnitin add-on | ~40% of US 4-yr still use (Detection Drama claim) | **[A]** — verify per school |
| Adelphi (pre-reform) | Turnitin | Used until Newby ruling exposed process failure | Court **[P]** |

**Interpretation:** Retreat is **concentrated at R1/research-intensive** and **Commonwealth** universities with public teaching-and-learning offices. Community colleges and smaller privates are under-documented; PLEASE list skews toward schools that **published** a stance.

---

## 3. Why universities retreat — reason matrix

### 3.1 False positives at scale

| Source | Claim | Math |
|--------|-------|------|
| Vanderbilt **[P]** | 1% FP unacceptable | 75,000 papers × 1% = **750**/year |
| WSU provost memo **[P]** | Turnitin self-reports 1–2% | 148,547 × 1% ≈ **1,485**/semester |
| Waterloo ITMS **[P]** | Internal test | Human text → **100% AI** |
| Turnitin **[F]** | Document-level FP "under 1%"; 1–19% suppressed as `*%` | Vendor disclaimer: not sole basis for adverse action |

**Debate point:** Vendors argue 1% is low; institutions argue **volume × low rate = unacceptable human harm**, especially when appeals are slow (ACU students waited months).

### 3.2 ESL / L2 / neurodivergent equity

| Evidence | Finding | Cited by |
|----------|---------|----------|
| Liang et al. 2023 **[A]** | 61.22% mean FPR on TOEFL essays | Vanderbilt, Waterloo, WSU |
| Stanford HAI summary | 97% flagged by ≥1 detector | Press, policy memos |
| WSU memo **[P]** | Higher FP for neurodivergent + ESL | Feb 2026 |
| Newby v. Adelphi **[P]** | Autistic student; Turnitin 100% | Litigation |
| US Dept of Education OCR **[S]** | Detector bias as Title VI concern | Detection Drama ESL page |

**Institutional response pattern:** Not always explicit "ESL" in early 2023 statements; by 2025–26 Waterloo and WSU name bias categories directly.

### 3.3 Due process and opacity

Shared policy language:

- Detection **cannot be sole evidence** (Northwestern, Manchester, Turnitin FAQ, Adelphi own policy — violated in Newby)
- Students often **cannot view** Turnitin AI report (UBC objection Apr 2023)
- **UK Office of Independent Adjudicator** overturned appeals (autistic + international postgraduate) — 2025 **[S]**

**Newby holding (Jan 28, 2026):** NY Sup. Ct. Nassau County annulled violation; ordered expungement. Not federal precedent, but widely cited. Turnitin score without corroboration + ignored contradictory tools = arbitrary and capricious.

### 3.4 Privacy, FERPA, intellectual property

| Institution | Frame |
|-------------|-------|
| UC Berkeley **[R]** | FERPA, copyright, third-party data feeding |
| UT Austin **[P]** | ADS = high-risk; no Procard; student owns IP |
| Vanderbilt **[P]** | FERPA; unknown third-party data policies |

UT Austin's 2024–25 guidance is the **strongest procurement wall**: no central contract exists, so **de facto ban** on sanctioned detector use.

### 3.5 Cost / staff burden (secondary but rising)

- Waterloo: AI feature expense in USD outweighs benefits **[P]**
- ACU: ~6,000 referrals → investigation load; ~25% dismissed **[S]**
- WSU Faculty Senate: mid-semester cancel with insufficient faculty lead time — process complaint separate from merits **[P]**

---

## 4. The debate (2024–2026)

### 4.1 Pro-retreat camp

**Core claim:** Statistical detectors cannot meet **beyond-reasonable-doubt** integrity standards at scale.

| Actor | Position |
|-------|----------|
| MIT Sloan EdTech **[P]** | Detectors don't work; use syllabus clarity, process statements, assignment design |
| Vanderbilt **[P]** | Harms of wrongful accusation exceed cheating detection benefit |
| UCT Walji **[P]** | "No magic solutions"; assess process not product |
| WSU Davis **[P]** | Aligns with peer R1s; cat-and-mouse with humanizers |
| GradPilot / PLEASE activists | Equity + due process; tracker as advocacy |

**Alternative integrity stack:**

1. AI-resilient assessments (in-class, oral, staged drafts)
2. Required AI-use disclosure / process memos
3. Traditional similarity checking (unchanged)
4. Authorship provenance tools (Turnitin Authorship, Grammarly Authorship) — **different category** from post-hoc perplexity classifiers

### 4.2 Pro-detection camp

**Core claim:** Without automated triage, AI cheating scales faster than manual review.

| Actor | Position |
|-------|----------|
| Turnitin **[F]** | Detection improves with retrains (Oct 2025, Feb 2026); bypasser layer Aug 2025 |
| Instructors (anecdotal) | "Something is better than nothing" for flagging obvious AI |
| Some K-12 districts | Still purchasing Copyleaks/GPTZero despite HE retreat |
| Academic integrity vendors | Frame humanizers as new cheating-provider category |

**Counter-arguments to retreat:**

- "Institutions are outsourcing judgment to broken tools" ≠ "cheating is fine"
- Assessment redesign is **slow and unfunded** — WSU Faculty Senate noted policy gap
- Disabling central tools may **push detection underground** (personal GPTZero accounts) unless procurement blocks (UT Austin model)

### 4.3 Unresolved tensions

| Tension | Detail |
|---------|--------|
| **Institution vs instructor** | Campus disable ≠ every syllabus; PLEASE warns about individual educator practice |
| **Similarity vs AI** | Most retreating schools **keep Turnitin similarity** — only classifier removed |
| **Admissions vs coursework** | Yale SOM / Rignol v. GPTZero shows detectors still used outside disabled-LMS contexts |
| **Global south lag** | UCT framed as catch-up; many SA/Asian institutions still adopting |
| **Vendor improvement claims** | Turnitin Oct 2025 "non-native speaker protections" — no public ESL-stratified benchmark; institutions that left haven't returned |

---

## 5. Legal and regulatory layer (2025–2026)

| Development | Implication |
|-------------|-------------|
| **Newby v. Adelphi** (NY, Jan 2026) | Score-alone discipline fails administrative review |
| **Rignol v. Yale** (pending) | GPTZero in admissions — different FERPA surface |
| **Kato v. Palo Alto USD** (pending) | K-12 Turnitin 76% on human essay |
| **UK OIA overturns** | International + neurodivergent students |
| **US OCR / Title VI framing** | ESL bias as civil rights — institutional risk calculus |
| **EU AI Act Art. 50** (Aug 2026 in force) | Transparency for AI-generated content — may shift from detection to disclosure (Agent #76 scope) |

CASRAI (2026) summary: **AI percentage alone increasingly insufficient** for misconduct findings; policies without human review + appeal carry legal exposure.

---

## 6. ACU case study — scandal-driven retreat

The Australian Catholic University arc is the **largest documented enforcement blowback**:

1. **2023:** Turnitin AI indicator enabled with national trend
2. **2024:** ~6,000 misconduct referrals (~90% AI-related) across 9 campuses
3. **Investigation:** ABC (Oct 2025) — students cleared after months; detector often **only evidence** despite Turnitin disclaimer
4. **Mar 17, 2025:** ACU pilots switch-off; cites limited reliability, can't distinguish editing vs generation, lack of student transparency
5. **Outcome:** ~25% referrals dismissed; any sole-detector case dismissed immediately (university claim post-reform)

**Lesson for unslop:** High-volume automated flagging **creates institutional liability** even when vendor terms say "don't use alone." ACU is the counterexample to "advisory only" policies that instructors ignore.

---

## 7. What replaces detectors — institutional playbook

| Strategy | Examples |
|----------|----------|
| **Assessment redesign** | Waterloo → CTE support; UCT → oral exams, observed group work |
| **AI literacy** | UCT mandatory modules; MIT syllabus examples |
| **Process artifacts** | Drafts, revision history, "how I used AI" statements (MIT Sloan) |
| **Similarity only** | Curtin, WSU, Waterloo — Turnitin plagiarism without AI % |
| **Provenance / authorship** | Turnitin Authorship (keystroke), Grammarly Authorship — **not** same as Liang-vulnerable perplexity detectors |
| **Honor code + conversation** | Vanderbilt, Georgetown — trust-first framing |

**Not replaced:** Prohibition on undisclosed AI where syllabus bans it. Retreat is about **evidence quality**, not permissiveness.

---

## 8. Unslop integration

### 8.1 What institutional retreat validates

| Claim | Safe to say | Do not say |
|-------|-------------|------------|
| ESL/L2 false positives are **real enough that R1s disable tools** | Yes — cite Liang + Vanderbilt + Waterloo | "Detectors are always wrong" |
| Anti-detector mode targets **register restoration**, not cheating | Yes — Boundaries in SKILL.md | "Beat Turnitin" / "100% undetectable" |
| Landscape is **inconsistent** | Yes — 35/50 elites off, 2/50 on | "All universities banned detectors" |
| **Process evidence** beats detector scores | Yes — aligns with MIT/UCT guidance | "No integrity rules apply" |

### 8.2 Recommended doc updates

1. **README "When it matters"** — Add 1-line institutional context: "60+ universities disabled Turnitin AI detection (2023–26); ESL false positives cited." Link Vanderbilt + Curtin.
2. **skills/unslop/SKILL.md Boundaries** — Cross-link Agent #69 for policy landscape; keep anti-detector as **ESL/resume/journalist defense**.
3. **Anti-detector procedure** — Optional step: suggest draft/version history preservation (institutional due-process ladder — matches GradPilot "protect yourself" without evasion marketing).
4. **Do not** cite Detection Drama "40% still use" without per-school verification.

### 8.3 Relationship to other agents

| Agent | Link |
|-------|------|
| **#18 Liang ESL** | Mechanism behind equity retreat |
| **#56 Turnitin 2025–26** | Vendor moves (bypasser, ESL tuning) didn't stop Curtin/WSU exits |
| **#68 ESL industry response** | Overlap — #69 is institutional half |
| **#70 OpenAI classifier shutdown** | Jul 2023 accelerant for Phase 0 |
| **#78 Academic integrity vs ESL framing** | Policy synthesis slot |

---

## 9. Open questions

1. **Exact global count?** PLEASE stopped updating Sep 2024; no ISO census. Treat "60+" as **minimum documented**.
2. **Will any R1 re-enable** after Turnitin Feb 2026 refresh? No public reversals yet.
3. **K-12 vs HE divergence?** HE retreats; some K-12 still buying — different liability surface.
4. **Admissions detectors?** Institution-level LMS disable may not cover GPTZero on application essays (Rignol).
5. **Underground detection?** UT Austin procurement ban vs schools with disable-only — enforcement unknown.
6. **Authorship tools** — Do provenance products get exempted from "detector retreat" category? Turnitin betting yes (Authorship, Clarity).

---

## 10. URL index

### Primary institutional statements

- [Vanderbilt — disable guidance (Aug 16, 2023)](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/)
- [Georgetown — Turnitin page (Oct 2023)](https://uis.georgetown.edu/turnitin/)
- [MIT Sloan — AI Detectors Don't Work](https://mitsloanedtech.mit.edu/ai/teach/ai-detectors-dont-work/)
- [UT Austin — AI Detection Software Guidance](https://provost.utexas.edu/the-office/faculty-affairs/office-of-academic-technology/ai-detection-software-guidance/)
- [U. Waterloo — discontinue Sep 2025](https://uwaterloo.ca/associate-vice-president-academic/discontinuing-use-ai-detection-functionality-turnitin)
- [Curtin — disable Jan 2026](https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/)
- [Curtin — GenAI student guidance](https://www.curtin.edu.au/students/study-support/genai-use-at-curtin/)
- [WSU provost memo — cancel Feb 2026 (PDF)](https://provost.wsu.edu/documents/2026/02/cancellation-of-turnitin-ai-detection-software_memo-to-instructors_provost-office_spring-2026.pdf/)
- [WSU — detecting misconduct policy page](https://provost.wsu.edu/policies/artificial_intelligence/detecting-and-reporting-misconduct/)
- [UCT News — scrap detectors Oct 2025](https://www.news.uct.ac.za/article/-2025-07-24-uct-scraps-flawed-ai-detectors)
- [ANU — disabled Jan 2024](https://www.anu.edu.au/students/program-administration/assessments-exams/detection-of-plagiarism-and-use-of-generative-artificial-intelligence) *(verify current URL)*

### Registries and trackers

- [PLEASE — Schools that Banned AI Detectors](https://www.pleasedu.org/resources/schools-that-banned-ai-detectors)
- [GradPilot — Colleges That Turned Off AI Detectors (2026)](https://gradpilot.com/news/colleges-that-disabled-ai-detectors)
- [GradPilot — AI cheating lawsuits tracker](https://gradpilot.com/news/ai-cheating-lawsuits-tracker)

### Litigation

- [Matter of Newby v. Adelphi — FindLaw](https://caselaw.findlaw.com/court/ny-supreme-court/118148544.html)
- [CASRAI — FP controversies 2026](https://casrai.org/news/ai-detector-false-positive-controversies-2026)

### Press / investigations

- [ABC — ACU wrongly accuses students (Oct 2025)](https://www.abc.net.au/news/2025-10-09/artificial-intelligence-cheating-australian-catholic-university/105863524)
- [Business Insider — universities ditch detectors (Sep 2023)](https://www.businessinsider.com/universities-ditch-ai-detectors-over-fears-students-falsely-accused-cheating-2023-9)
- [Detection Drama — top 50 policies (Jun 2026)](https://detectiondrama.com/ai-detection-policies-top-50-universities/)
- [Detection Drama — full banned list](https://detectiondrama.com/universities-that-banned-ai-detectors/)

### Research cited by institutions

- [Liang et al. 2023 — DOI](https://doi.org/10.1016/j.patter.2023.100779)
- [Sadasivan et al. 2023 — impossibility](https://arxiv.org/abs/2305.04342)
- [Stanford HAI — detector bias news](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers)

### unslop internal

- [Agent #18 — Liang ESL](./AGENT-18-LIANG-ESL-BIAS.md)
- [Agent #56 — Turnitin 2025–26](./AGENT-56-TURNITIN-2025-2026.md)
- [Agent MANIFEST](./AGENT-MANIFEST-100.md)
- [skills/unslop/SKILL.md](../../skills/unslop/SKILL.md)

---

## 11. Evidence tier key

| Tier | Meaning |
|------|---------|
| **[P]** | Primary institutional (provost, teaching center, official news) |
| **[R]** | Registry pointing to primary |
| **[F]** | Vendor first-party |
| **[A]** | Peer-reviewed / working paper |
| **[S]** | Major press with document citation |
| **[V]** | Aggregator / vendor-adjacent — verify |

---

*Agent #69 complete. Cross-ref: Agent #68 (ESL industry response) — institutional half delivered here; Agent #78 (integrity vs ESL framing) pending synthesis.*
