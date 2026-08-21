# Agent #78 — Academic Integrity vs ESL Defense Framing

**Topic:** How to position `/unslop anti-detector` ethically — integrity enforcement vs false-positive defense, legal cases, university policies, public debate  
**Prepared:** August 19, 2026  
**Scope:** Messaging architecture, decline rules, litigation/policy anchors, critic/supporter debate — not detector mechanics (see Agents #18, #56, #68, #69)  
**Status:** complete  
**Cross-ref:** [Agent #18](./AGENT-18-LIANG-ESL-BIAS.md) (mechanism), [Agent #68](./AGENT-68-ESL-INDUSTRY-RESPONSE.md) (vendor response), [Agent #69](./AGENT-69-INSTITUTIONAL-RETREAT.md) (university exit wave), [Agent #61](./AGENT-61-UNDETECTABLE-RYTER-WALTER.md) (adversarial humanizers), [Agent #66](./AGENT-66-TURNITIN-BYPASSER-DETECTION.md) (bypasser category), [Agent #67](./AGENT-67-MARKETING-VS-AUDIT.md) (honest claims)

---

## Executive summary

Anti-detector mode sits at a **fork in framing**. Academic integrity professionals hear "humanizer" and map it to **misconduct tooling** — the same product category as Undetectable.ai and Turnitin's "AI bypasser" layer (Agent #66). ESL advocates, civil-rights lawyers, and a growing list of universities hear **false-positive harm** — Liang's 61% TOEFL FPR, Vanderbilt's 750-wrongful-flags arithmetic, OCR Title VI guidance, and courts annulling score-only discipline (Newby v. Adelphi, Jan 2026).

Both framings describe **the same transform**. Liang proved that vocabulary enrichment and register shift remove ESL false positives **and** evade detectors on real AI text. Vendors cannot claim unbiased detection without admitting evasion; humanizers cannot claim equity defense without admitting the technique overlaps cheating workflows. unslop resolves the fork with **intent-based boundaries**, not technical differentiation:

| Frame | Audience | unslop stance |
|-------|----------|---------------|
| **Integrity enforcement** | Conduct officers, Turnitin CPO, essay-mill critics | Decline plagiarism/grader deception; never "beat Turnitin"; no bypass marketing |
| **ESL / equity defense** | L2 writers, resume polishers, journalists, neurodivergent students falsely flagged | Offer anti-detector for documented false-positive risk; cite Liang + institutional retreat + due-process law |
| **Process integrity** | Vanderbilt, MIT Sloan, ICAI, ACM USTPC | Align with assessment redesign + process evidence — unslop polishes *human* drafts, not ghostwritten AI |

**2026 landscape:** 60+ universities disabled or restricted AI classifiers; US ED OCR (Nov 2024) treats disproportionate ESL flagging as potential **Title VI** exposure; Newby established that Turnitin-100% alone fails administrative review. Meanwhile Turnitin shipped bypasser detection (Aug 2025), commercial humanizers market "99% undetectable," and ICAI's 2026 webinar series still teaches **investigating misuse** — detection has not disappeared, it moved underground (personal GPTZero accounts, admissions workflows).

**Unslop verdict:** Anti-detector is **legitimate defensive tooling** when the user's stated goal is reducing false flags on **their own human-authored work**. It is **misconduct facilitation** when the goal is submitting AI-generated text as original scholarship. The product must **lead with equity and due-process citations**, **decline explicitly on misconduct intent**, and **never promise durable detector pass**. Fix the Boundaries citation typo: Liang is **arXiv:2304.02819**, not 2306.04723.

---

## 1. The framing fork — why one mode, two audiences

### 1.1 Same mechanism, opposite moral valence

```
                    ┌─────────────────────────────────────┐
                    │  Register shift: burstiness,        │
                    │  contractions, specificity,         │
                    │  cross-model paraphrase             │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   ┌──────────────────────┐                     ┌──────────────────────┐
   │ ESL DEFENSE FRAME    │                     │ INTEGRITY FRAME      │
   │                      │                     │                      │
   │ "My essay is mine;   │                     │ "Student used AI;    │
   │  detector is wrong"  │                     │  humanizer hid it"   │
   │                      │                     │                      │
   │ Liang 61% FPR        │                     │ Turnitin bypasser    │
   │ OCR Title VI         │                     │ ICAI misuse probe    │
   │ Newby annulment      │                     │ Undetectable.ai ads  │
   └──────────────────────┘                     └──────────────────────┘
```

Liang et al. (*Patterns*, July 2023; [arXiv:2304.02819](https://arxiv.org/abs/2304.02819)) made the isomorphism explicit: ChatGPT prompt *"Enhance word choices to sound more like a native speaker"* dropped mean FPR on human TOEFL essays from **61.22% → 11.77%**. The inverse prompt on native essays raised FPR from **5.19% → 56.65%**. The **detector cannot distinguish** fairness intervention from evasion without external provenance (drafts, keystroke logs, oral defense).

### 1.2 Who uses which frame

| Stakeholder | Default frame | What they need to hear from unslop |
|-------------|---------------|-----------------------------------|
| ESL / international student | Defense | "Detectors misread predictable L2 prose; here's how to reduce false flags on *your* writing" |
| Academic conduct officer | Enforcement | "Humanizers are evasion; we investigate process evidence, not scores alone" |
| University teaching center | Risk management | "Detectors unreliable at scale; redesign assessment; don't sole-source discipline" |
| Commercial humanizer vendor | Bypass | "100% undetectable" — **do not mirror this** |
| Civil-rights advocate (CDT, OCR) | Disparate impact | "Automated flagging + discipline on EL students = Title VI theories" |
| Resume / job seeker | Defense | "ATS and hiring tools run classifiers; polish without inventing facts" |
| Journalist / freelancer | Defense | "Editorial AI-assist flagged as bot; restore human register" |

unslop's Boundaries already encode the fork (`skills/unslop/SKILL.md` L145–146). This memo supplies the **evidence stack** and **copy patterns** to defend that boundary under scrutiny from both camps.

---

## 2. Academic integrity camp — arguments and limits

### 2.1 Core claims

**"Without automated triage, AI cheating scales faster than manual review."** Turnitin, Copyleaks, and integrity vendors argue that disabling detectors pushes misconduct underground and rewards essay-mill humanizers. Turnitin's Aug 2025 press release frames humanizer SaaS as **"a new category of cheating providers"** — parallel to contract cheating, subscription-priced at $8–15/mo (Agent #61, #66).

**"Humanizers exploit equity framing."** Critics note that Liang's ESL findings give moral cover to bypass tools. Undetectable.ai, Ryter Pro, and Walter Writes all sell detector panels + rewrite in one box; their SEO targets "bypass Turnitin" not "fix false positive." Academic integrity professionals (ICAI Summer 2026 webinar #3: *Investigating Misuse of AI*) teach conduct officers to treat contradictory detector results as a **process problem**, not proof of innocence — but still pursue misuse through version history and interviews.

**"Assessment redesign is slow; instructors need something now."** Pro-detection camp accepts detector imperfection but rejects total exit. Some K-12 districts and community colleges still purchase Copyleaks/GPTZero despite R1 retreat (Agent #69 §2.8). Georgia Tech and U. Georgia remain documented Turnitin-AI-enabled outliers among US top-50.

### 2.2 What the integrity camp gets right

1. **Intent matters.** A humanizer on AI-origin text is evasion regardless of ESL status.
2. **Process evidence beats post-hoc scoring.** ICAI conduct administrators recommend Google Docs version history, collaborator links, and student interviews over detector dueling (ICAI 2024 article, Agent #68 sources).
3. **Commercial bypass marketing is predatory.** FTC sanctioned Workado (Aug 2025) for misrepresented AI-detector accuracy; "98% accurate" claims without arm qualification are legally risky (Agent #67).
4. **Arms race is real.** Turnitin bypasser layer (Aug 2025), GPTZero humanizer-trained models (Jan 2026), DAMAGE showing humanizers break legacy detectors — evasion and detection co-evolve.

### 2.3 What the integrity camp overclaims

| Overclaim | Counter-evidence |
|-----------|------------------|
| "Detectors are good enough for high-stakes discipline" | OpenAI withdrew classifier Jul 2023; ACM USTPC: insufficient accuracy for automatic rejection in high-stakes text |
| "ESL bias is solved" | Al Ali 2026: **23.1%** FPR on Liang TOEFL-91 vs **0%** native; independent English gap persists |
| "Disabling detectors = enabling cheating" | Vanderbilt, Waterloo, WSU replaced detection with **process-based integrity** — not honor-code abolition |
| "All humanizers are equivalent" | unslop subtracts AI-isms with byte-preservation; Undetectable.ai is DAMAGE **L3** fluency with injected typos |

**unslop response:** Accept integrity camp's **intent standard** and **process-evidence preference**. Reject equating **ESL false-positive defense** with **Undetectable.ai bypass marketing**. Decline when user intent is misconduct; offer anti-detector when intent is polishing human-authored work at false-positive risk.

---

## 3. ESL / equity defense camp — arguments and limits

### 3.1 Core claims

**"Detectors punish predictable prose; L2 writers produce predictable prose for human reasons."** Liang mechanism: smaller productive vocabulary, formulaic scaffolding, exam-register templates → low perplexity → high AI score. ICLR abstract analysis extends to **non-native-country ML authors** at equal review ratings.

**"False positives scale to real harm."** Vanderbilt (Aug 2023): 75,000 papers × 1% claimed FP = **750 wrongful flags/year**. WSU (Feb 2026): ~**1,485** FPs/semester at Turnitin's own 1% claim. Bloomberg (Oct 2024), HEPI (Jul 2026), MIT Technology Review document accused students' stories — reputational damage even when charges are reversed.

**"Institutions are exiting because the tools fail, not because cheating stopped."** 60+ universities disabled or restricted AI classifiers (Agent #69). Pattern: keep **similarity checking**, drop **classifier layer**. Replacement stack: staged drafts, oral defense, AI-use statements, Authorship/Replay provenance.

**"Civil-rights law applies."** CDT brief (*Late Applications: Disproportionate Effects of Generative AI-Detectors on English Learners*, 2024): EL false flagging → **disparate treatment, disparate impact, hostile environment** theories under Title VI. US ED OCR (Nov 20, 2024): AI plagiarism tool with higher error on non-native essays → **investigation grounds** ([OCR resource PDF](https://www.ed.gov/media/document/avoiding-discriminatory-use-of-artificial-intelligence-112274.pdf)).

### 3.2 Populations beyond Liang TOEFL

| Population | Mechanism overlap | Documented misfire |
|------------|-------------------|-------------------|
| Chinese L1 TOEFL writers | Liang primary corpus | 61.22% mean FPR |
| International students (UK) | HEPI 2026 fairness crisis | OIA overturn cases Jul 2025 |
| Neurodivergent formal writers | Uniform/polished register | Newby (autism + Turnitin 100%); York SU reporting |
| Grammarly/tutor-assisted prose | Polished surface → low perplexity | Newby — tutoring support ignored |
| Careful native academics | High register | "Better writer = more AI" anecdote (Cal State, press) |
| Special-ed teachers' students | 76% of licensed SPED teachers use detectors (CDT) | Highest exposure × highest FP risk |

Liang did not test all groups; the **predictable-prose mechanism** predicts overlap.

### 3.3 What the ESL camp gets right

1. **Historical harm is documented and peer-reviewed** — not vendor FUD.
2. **Independent replication shows bias reduction ≠ elimination** (Al Ali 2026).
3. **Institutional policy converged** on "detector cannot be sole evidence" before unslop existed.
4. **OpenAI itself cited ESL stigma** when withholding ChatGPT watermark (Aug 2024 — Agent #70).

### 3.4 What the ESL camp overclaims

| Overclaim | Counter-evidence |
|-----------|------------------|
| "Any detector use is always discriminatory" | ETS in-house study: no bias when L2 represented in training (simplified; not commercial tools) |
| "Humanizers fix ESL bias with no tradeoffs" | Register enrichment may homogenize L1 voice; Liang used "native speaker" as **intervention**, not ethical recommendation |
| "All flagged ESL students are innocent" | ESL students may legitimately use ChatGPT for editing — true positives exist (Pangram ESL blog acknowledgment) |
| "Detector pass = justice" | Booth/DAMAGE: humanized AI still detectable; anti-detector is not permanent immunity |

**unslop response:** Lead with Liang + OCR + institutional retreat for **why** the mode exists. Do **not** promise pass. Do **not** force "native-washing." Preserve authentic L1-influenced voice (voice-match when identity matters; anti-detector when formal-register false flags are the problem).

---

## 4. Legal cases — what they establish (and don't)

### 4.1 Case inventory (2024–2026)

| Case | Court | Detector | Outcome | ESL/neuro | Establishes |
|------|-------|----------|---------|-----------|-------------|
| **Matter of Newby v. Adelphi** | NY Sup. Ct., Nassau (Article 78) | Turnitin **100%** | **Student won** — annulment + expungement (Jan 28–29, 2026) | Autistic; Bridges program; Grammarly tutoring | Score-alone discipline + ignored contradictory tools = arbitrary and capricious |
| **Kato v. Palo Alto USD** | Pending (2026) | Turnitin **76%** | Pending | K-12 human essay | Extends litigation to K-12 |
| **Rignol v. Yale** | Pending | GPTZero | Injunction denied so far | SOM admissions essay | Detectors still used outside LMS-disabled contexts |
| **Yang v. U. Minnesota** | Appeal lost | GPTZero + faculty | **Student lost** | PhD dissertation | Detectors still enforceable when process followed |
| **Harris v. Hingham** | D. Mass. | Teacher judgment | School won (injunction denied) | HS | Not all challenges succeed |

**Newby details (canonical):** Freshman Orion Newby submitted a World Civilizations essay with tutoring support through Adelphi's Bridges program (neurodevelopmental support). Professor Micah Oelze cited Turnitin **100% AI-generated**. Newby submitted Grammarly detector and ZeroGPT results showing **0% AI**. University found him responsible, required 3-hour integrity workshop, denied appeal. Judge Randy Sue Marber: finding **"without valid basis and devoid of reason"**; ordered record expungement ([2026 NY Slip Op 26021](https://law.justia.com/cases/new-york/other-courts/2026/2026-ny-slip-op-26021.html)).

**Critical legal nuance (often misreported):**

- Newby is **state administrative review**, not federal damages precedent.
- Holding is **process failure** (ignored exculpatory detector evidence, broken appeal), not "Turnitin is per se unreliable."
- **Neurodivergent** angle is load-bearing; ESL-specific precedent remains OCR guidance + Liang, not Newby alone.

### 4.2 Regulatory layer

| Source | Date | Relevance to unslop framing |
|--------|------|----------------------------|
| **CDT** — EL disproportionate impact brief | 2024 | Title VI theories for false-flag discipline |
| **US ED OCR** — Avoiding Discriminatory Use of AI | Nov 20, 2024 | AI plagiarism checker + higher EL error → investigation |
| **ACM USTPC** — GAI detection principles | 2024 | No automatic rejection of high-stakes text; human final arbiter; appeal required |
| **FTC v. Workado** | Aug 2025 | Unsubstantiated detector/humanizer accuracy = deceptive |
| **EU AI Act Art. 50** | In force Aug 2026 | Transparency for AI-generated content — shifts some contexts from detection to **disclosure** (Agent #76 scope) |

**For unslop copy:** Cite Newby for **due-process** ("institutions can't rely on one score"). Cite Liang + OCR for **equity** ("ESL writers face asymmetric false-positive risk"). Do **not** cite Newby as "humanizers are legal" or "Turnitin is illegal."

---

## 5. University policies — the patchwork (2026)

### 5.1 Three policy tiers

| Tier | Definition | Examples | Implication for anti-detector |
|------|------------|----------|-------------------------------|
| **A — Disabled / banned** | Campus AI classifier off or procurement blocked | Vanderbilt, Waterloo, Curtin, WSU, UT Austin, Yale, ANU | Institutional stance: post-hoc score unreliable — **supports defensive framing** |
| **B — Advisory only** | Detector allowed; cannot be sole evidence | Johns Hopkins, Northwestern (post-disable guidance), Turnitin FAQ | User may still face instructor-level flag — **defense still relevant** |
| **C — Active enforcement** | Turnitin AI / GPTZero in misconduct workflow | Georgia Tech, UGA; many undisclosed CCs; Adelphi pre-reform | **Highest false-positive risk** for ESL users; anti-detector ethically scoped to human drafts |

### 5.2 Canonical policy language (cite these)

**Vanderbilt (Aug 16, 2023)** — disabled Turnitin AI detector:

> ~750 potential false accusations per year at 1% FP × 75,000 papers; ESL bias (Stanford HAI); opacity; FERPA concerns.

[Primary guidance](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/)

**University of Waterloo (Sep 2025)** — discontinued Turnitin AI detection:

> Internal testing flagged human-written text as **100% AI-generated**; cited Liang lineage and peer-reviewed unreliability.

**Washington State University (Feb 2026)** — cancelled AI detection contract:

> 148,547 assessments; ~1,485 false positives at 1%; 33% of AI integrity hearings → not responsible when detector was sole evidence.

**Indiana Kelley School (2026 Faculty AI Playbook)** — prohibits AI detectors:

> "These services are highly unreliable… focus on designing assignments that encourage process, reasoning, and authentic engagement."

**MIT Sloan Teaching & Learning Technologies** — *AI Detectors Don't Work*:

> High error rates; false accusations; OpenAI shutdown; emphasize syllabus clarity and fair assessment design.

**HEPI (Jul 20, 2026)** — UK international-student fairness:

> UK universities still treat integrity as detection problem; OIA cases show cost; recommends suspend detection as primary evidence pending independent validation.

### 5.3 Policy replacement stack (integrity-positive, detection-skeptical)

Institutions that disabled classifiers did **not** abandon academic integrity. Replacement pattern:

1. **AI-resilient assessment** — in-class writing, oral defense, staged submissions
2. **Required AI-use disclosure** — process memos, reflection on tool use
3. **Traditional similarity checking** — unchanged
4. **Authorship provenance** — Turnitin Authorship, Grammarly Authorship, GPTZero Replay (keystroke/draft trail — **different category** from post-hoc perplexity classifiers)

**unslop alignment:** Position anti-detector as compatible with **process integrity** (polish *your* draft before submission) and incompatible with **output-only surveillance** (beat the score on AI ghostwriting).

---

## 6. Professional consensus — who says what

| Body | Position | Quote / paraphrase |
|------|----------|-------------------|
| **ACM US Public Policy Council (USTPC)** | No auto-reject on detector output in high-stakes text | Humans must be final arbiters; appeal process required |
| **ICAI (2024–2026)** | Shift from detection to assessment redesign + ethical AI literacy | Summer 2026 series: "Re-designing assessment," "Investigating misuse" — detection is investigative tool, not proof |
| **ICAI / York (2026)** | Neurodivergent + "academic language" → false flags | Disability double standard: encouraged register triggers detectors |
| **University of Pittsburgh Teaching Center** | Disabled Turnitin AI; do not endorse any detector | "Not reliable enough… substantial risk of false positives" |
| **Turnitin (vendor)** | Detection improves; bypasser layer Aug 2025; scores are conversation starters | Also: "must not be sole basis for adverse action" in model guide |
| **OpenAI** | Withdrew public classifier Jul 2023 | Insufficient accuracy for education |
| **Chicago Booth (Jabarian & Imas 2025)** | Commercial detectors work on clean medium-length English | **No ESL stratification** — limits use as equity rebuttal |

**Synthesis:** There is **no professional consensus that detectors are safe for sole-evidence discipline**. There **is** consensus that misconduct still matters and must be investigated through **process**. unslop sits in the gap: help human writers avoid **wrongful classification**, refuse to help **misrepresent AI authorship**.

---

## 7. The public debate — mapped arguments

### 7.1 Debate matrix

| Claim | Integrity side | ESL/equity side | unslop adjudication |
|-------|--------------|-----------------|---------------------|
| Detectors work | "≤1% FPR on general corpus" (Booth) | "23% on Liang TOEFL; 100% live failures" (Al Ali, Waterloo) | **Both true on different populations** — never cite Booth without ESL caveat |
| Humanizers | "Bypass tools = cheating providers" | "Same transform fixes false positives" | **Intent + authorship origin** determines ethics |
| Institutional retreat | "Abdication; cheating wins" | "Rational risk management" | Cite retreat as **policy validation of FP risk**, not anti-integrity |
| ESL "native enhancement" | "Encourages deception" | "Reduces bias" | unslop: **distribution shaping**, not native-washing |
| Neurodivergent writers | Emerging integrity concern | Same mechanism as ESL | Include in defensive use cases; cite Newby |
| EU / CA regulation | Disclosure required | False positive still harms | Anti-detector ≠ Art. 50 evasion; document watermark side effect |

### 7.2 Rhetorical traps to avoid

| Trap | Why it fails | unslop alternative |
|------|--------------|-------------------|
| "Beat Turnitin/GPTZero" | Collapses into Agent #61 adversarial category; FTC exposure | "Reduce false-positive risk on human writing" |
| "100% undetectable" | False; Sadasivan + monthly retraining | "Detectors are noisy; keep drafts; no guarantee" |
| "Detectors are always racist" | Overstates; weakens credibility with policy audiences | "Documented asymmetric FPR on L2 English (Liang 2023; Al Ali 2026)" |
| "Using anti-detector is always cheating" | Ignores Liang mechanism + 60+ institutional exits | "Decline when intent is misconduct; offer for FP defense" |
| "ESL bias is fixed in 2026" | Al Ali 23.1%; vendor 0% is first-party | "Bias reduced, not eliminated; verify per tool" |

### 7.3 Adversarial humanizer comparison (integrity optics)

| Dimension | Undetectable.ai / Ryter / Walter | unslop anti-detector |
|-----------|----------------------------------|----------------------|
| **Primary CTA** | "Bypass Turnitin" | "Humanize / de-slop" |
| **Built-in detector panel** | Yes (conflict of interest) | Optional `--detector-feedback`; no pass guarantee |
| **Preservation** | Opaque rewrite | Code, URLs, headings byte-exact |
| **Quality target** | Minimize detector score (DAMAGE L3) | Subtract AI-isms; burstiness, contractions |
| **Boundaries** | None | Decline misconduct; ESL/resume/journalism defense |
| **Evidence cited** | Vendor SEO | Liang, Vanderbilt, OCR, Newby process |

unslop must **never** be positioned as "free Undetectable.ai." Position as **"in-editor voice repair with explicit ethics — the cross-model pass you orchestrate, not a paste-box bypass subscription."**

---

## 8. Ethical positioning framework for unslop

### 8.1 The four-question gate (before enabling anti-detector)

Use in SKILL.md, README, and agent refusals:

1. **Authorship:** Is the text substantially the user's own work (possibly AI-*assisted* for grammar/brainstorming with disclosure), or generated by AI to be submitted as original?
2. **Intent:** Is the goal reducing a **false positive** on human writing, or **evading detection** of AI-generated submission?
3. **Context:** Is the institution/policy environment one where detector scores trigger discipline (Tier B/C above)?
4. **Provenance:** Can the user produce process evidence (drafts, edits, notes) if challenged?

| Q1 human-authored | Q2 FP defense | Q3 high-stakes | Q4 process exists | → Action |
|-------------------|---------------|----------------|-------------------|----------|
| Yes | Yes | Yes | Yes/No | **Offer anti-detector** + recommend keeping drafts |
| Yes | Yes | No | — | Offer; lower urgency |
| No (AI-generated) | Evasion | Yes | No | **Decline** — academic misconduct |
| No | Evasion | Any | — | **Decline** |
| Unclear | — | — | — | **Ask** before rewriting |

### 8.2 Approved use cases (defensive frame)

| Use case | Warrant | Copy hook |
|----------|---------|-----------|
| ESL student, honest essay flagged | Liang 2023; OCR 2024; Al Ali 2026 | "Detectors misread L2 academic register" |
| Resume / cover letter / LinkedIn | Hiring ATS + classifier noise; no institutional detector policy | "Polish without inventing experience" |
| Journalist / freelancer | Editorial AI-assist flagged | "Restore human register on reported facts" |
| Neurodivergent formal writer | Newby pattern; York/ICAI 2026 | "Polished academic register ≠ AI" |
| AI-assisted **with disclosure** | Process integrity; Grammarly-class assist | "De-slop the surface; disclose tool use per syllabus" |

### 8.3 Decline cases (integrity frame)

| Use case | Response template |
|----------|-------------------|
| "Make my ChatGPT essay pass Turnitin" | Decline. Same technique; misconduct intent. Suggest assignment help or disclose AI use per policy. |
| "I'm plagiarizing but need it undetectable" | Hard decline. |
| "Ghostwrite my dissertation" | Decline. |
| "Remove watermark to evade EU disclosure" | Decline (Art. 50 boundary — Agent #72, #76). |
| Ambiguous — "humanize for school" | Ask: own work? flagged? policy? before proceeding. |

### 8.4 Technical steps ↔ ethical labels

Map anti-detector procedure to **defensive** language (not bypass language):

| SKILL step | Bypass marketing says | unslop defensive says |
|------------|-------------------------|----------------------|
| Burstiness σ ≥ 6 | "Trick the AI checker" | "Restore natural sentence-length variation human writers have" |
| Contractions / fragments | "Fake human errors" | "Match human contraction rate (~0.17/chunk per Paneru 2026)" |
| Grounded specificity | "Add fake details" | "Use *your* real numbers and names — never invent" |
| Rough edges | "Insert typos" | "Don't over-polish into low-perplexity AI register" |
| Cross-model second pass | "Bypass cascade" | "Different model families have different fingerprints; optional final pass" |

---

## 9. Recommended copy — SSOT touchpoints

### 9.1 README — "When it matters" block (keep / refine)

**Say:**

- "AI detectors falsely flag real human writing — especially from non-native English speakers (Liang et al., *Patterns* 2023: >50% of TOEFL essays flagged)."
- "60+ universities disabled or restricted AI detectors citing unreliability and equity (Vanderbilt 2023, Waterloo 2025, Curtin 2026)."
- "`/unslop anti-detector` reduces AI-ism fingerprints and restores human register — for **your** drafts when a detector might misread them. Not for submitting AI-generated work as your own."
- "No tool guarantees a detector pass. Keep version history. Read the output yourself."

**Do not say:**

- "Beat Turnitin" / "GPTZero proof" / "100% undetectable"
- "Cheat safely" / "pass AI detection"

### 9.2 SKILL.md Boundaries — fix + expand

**Fix citation:** `arXiv:2304.02819` (Liang), not 2306.04723 (Tulchinskii).

**Add one paragraph:**

> When a user requests anti-detector mode for an essay or assignment, confirm the text is their own work (AI may assist with grammar or brainstorming only where policy allows). If the user wants to submit AI-generated text as original scholarship, decline and explain that the same techniques that reduce ESL false positives also evade detectors — offering them for evasion would violate unslop boundaries. Cite process-evidence alternatives: staged drafts, AI-use statements, oral defense.

### 9.3 GETTING_STARTED.md — already good

Existing line: "An ESL student whose honest essays keep getting falsely flagged" — **keep**. Add neurodivergent + resume examples from §8.2.

### 9.4 Refusal microcopy (agent / hook)

> I can't help evade academic integrity systems on AI-generated work. I can help polish **your** writing so detectors are less likely to misread it as machine-generated — that's what `/unslop anti-detector` is for (ESL false positives, resumes, flagged human drafts). If you've been falsely accused, keep your draft history and cite contradictory detector results — see Newby v. Adelphi (2026) on due process.

---

## 10. unslop integration checklist

| Priority | Action | Owner file |
|----------|--------|------------|
| **P0** | Fix Liang citation 2306.04723 → **2304.02819** | `skills/unslop/SKILL.md` SSOT |
| **P0** | Keep Boundaries decline rule on misconduct | `skills/unslop/SKILL.md` |
| **P1** | Add four-question gate to anti-detector procedure | `skills/unslop/SKILL.md` |
| **P1** | Cross-link Agent #18, #69, #78 in `skills/unslop-help/SKILL.md` | help card |
| **P2** | README: cite Newby (process) + OCR (equity) alongside Liang | `README.md` |
| **P2** | Bench corpus: ESL vs native FPR stratification | `drafts/2026-05-detector-test/` |
| **P3** | Optional `--intent=defense` CLI flag? | **Defer** — intent is conversational, not flag-gated |

---

## 11. Open questions (2026+)

1. **Will Newby spawn copycat Article 78 filings?** Early 2026 tracker shows K-12 (Kato) and admissions (Rignol) — process precedent may spread faster than ESL-specific rulings.
2. **Does Turnitin bypasser detection re-open integrity framing against register-shift tools?** Aug 2025 layer targets Class III humanized AI — may increase false positives on **human** L2 prose edited for fairness (Agent #66).
3. **Authorship/Replay adoption:** If institutions migrate to keystroke provenance, post-hoc anti-detector becomes less central for **enrolled** students but remains relevant for admissions, hiring, publishing.
4. **UK QAA/OIA joint guidance** — HEPI asked for suspension of detection as primary evidence; formal guidance pending could shift EU/UK copy.
5. **Humanizer homogenization harm** — equity fix that erases L1 voice (commercial tools optimize for native-like register) — unslop should track voice-match vs anti-detector split (Agent #18 §10.1).

---

## 12. Primary source table

| # | Source | Year | URL |
|---|--------|------|-----|
| 1 | Liang et al. — *Patterns* / arXiv:2304.02819 | 2023 | https://arxiv.org/abs/2304.02819 |
| 2 | Stanford HAI — ESL bias summary | 2023 | https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers |
| 3 | US ED OCR — Avoiding Discriminatory Use of AI | 2024 | https://www.ed.gov/media/document/avoiding-discriminatory-use-of-artificial-intelligence-112274.pdf |
| 4 | CDT — EL disproportionate impact brief | 2024 | https://www.einpresswire.com/article/675948844/brief-late-applications-disproportionate-effects-of-generative-ai-detectors-on-english-learners |
| 5 | Matter of Newby v. Adelphi | 2026 | https://law.justia.com/cases/new-york/other-courts/2026/2026-ny-slip-op-26021.html |
| 6 | Vanderbilt — disable Turnitin AI | 2023 | https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/ |
| 7 | MIT Sloan — AI Detectors Don't Work | 2023+ | https://mitsloanedtech.mit.edu/ai/teach/ai-detectors-dont-work/ |
| 8 | HEPI — international students fairness | 2026 | https://www.hepi.ac.uk/2026/07/20/catching-the-wrong-students-ai-detection-international-students-and-the-fairness-crisis-in-uk-universities/ |
| 9 | Inside Higher Ed — detectors out | 2026 | https://www.insidehighered.com/news/tech-innovation/artificial-intelligence/2026/08/05/ai-detectors-are-out-new-approaches-are |
| 10 | ACM USTPC — GAI detection principles | 2024 | https://prod-www.acm.bloomreach.cloud/binaries/content/assets/public-policy/ustpc-gai-detection.pdf |
| 11 | Al Ali et al. — EACL 2026 SRW | 2026 | https://arxiv.org/abs/2602.05769 |
| 12 | Turnitin — bypasser press release | 2025 | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers |
| 13 | GradPilot — AI cheating lawsuits tracker | 2026 | https://gradpilot.com/news/ai-cheating-lawsuits-tracker |
| 14 | ICAI — Investigating Misuse of AI (webinar series) | 2026 | https://associationdatabase.com/aws/ICAI/pt/sp/summer |

---

## 13. Unslop verdict (one paragraph)

The integrity vs ESL framing war is **not winnable on technical grounds** — Liang proved the transform is identical. unslop wins on **intent, boundaries, and citation hygiene**: lead with peer-reviewed ESL harm (2304.02819), institutional retreat (Vanderbilt, Waterloo, Curtin), civil-rights guidance (OCR, CDT), and due-process law (Newby); decline misconduct and bypass marketing; never promise detector pass; distinguish from Undetectable.ai by preservation, subtractive polish, and explicit refusal. Anti-detector mode is **defensive humanization for writers detectors misread**, not a cheaper cheating tool. Fix the Tulchinskii/Liang citation typo. When both camps attack — integrity says "humanizer," equity says "too weak to help" — the answer is the same: **whose text, what intent, what process evidence**.
