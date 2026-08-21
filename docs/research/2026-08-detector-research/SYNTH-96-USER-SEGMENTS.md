# SYNTH-96 — unslop User Segments: Needs, Threat Models, and Mode Fit

**Synthesis agent:** #96  
**Inputs:** [SYNTH-82](./SYNTH-82-DETECTION-COMMERCIAL.md) (commercial detection), [AGENT-68](./AGENT-68-ESL-INDUSTRY-RESPONSE.md) (ESL industry response), [AGENT-78](./AGENT-78-INTEGRITY-VS-ESL-FRAMING.md) (integrity vs ESL framing), [AGENT-18](./AGENT-18-LIANG-ESL-BIAS.md) (Liang mechanism)  
**Prepared:** August 19, 2026  
**Status:** Segment synthesis for README audience blocks, GETTING_STARTED examples, SKILL Boundaries, bench protocol  
**Cross-refs:** [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md), [GETTING_STARTED.md](../../GETTING_STARTED.md), [SYNTH-91](./SYNTH-91-HUMAN-CUES.md) (preserve vs inject)

---

## Executive summary

unslop serves four overlapping but distinct user segments. Each faces a different **reader**, a different **detector threat model**, and a different **ethical frame**. Commercial detection (SYNTH-82), ESL equity (Agent #68), and integrity framing (Agent #78) converge on one product rule: **intent and authorship origin matter more than technique**.

| Segment | Primary pain | Likely detectors | Default mode | Anti-detector? |
|---------|--------------|------------------|--------------|----------------|
| **Developers** | Agent output reads like a chatbot before it ships | Rarely formal classifiers; peer review, docs readers | `balanced` | No — not the use case |
| **ESL / L2 writers** | Honest human prose flagged as AI (Liang 61% TOEFL FPR) | Turnitin, GPTZero, Pangram | `balanced` → `anti-detector` when flagged | **Yes — primary warrant** |
| **Resume / job seekers** | Polished AI resume loses voice; ATS/hiring panels run classifiers | GPTZero, Copyleaks, employer tools | `voice-match` or `balanced` | Sometimes — short-form harder |
| **Students** | Coursework voice + integrity tension; patchwork institutional policy | Turnitin AI + instructor GPTZero | `balanced`; `anti-detector` only for own human drafts | Conditional — intent gate |

**Cross-segment truth:** No segment gets a detector pass guarantee. Developers mostly need **subtractive slop removal** with byte-exact code preservation. ESL writers need **register restoration without native-washing**. Resume writers need **voice recovery + factual re-verification**. Students need **process-integrity alignment** — polish human drafts, decline AI ghostwriting.

---

## 1. Segment profiles

### 1.1 Developers

**Who:** Engineers, technical writers, and maintainers cleaning up LLM-generated docs, PR descriptions, commit messages, README copy, and agent output before merge or publish.

**Origin story fit:** unslop was built because a resume rewrite sounded wrong — but the **primary repo audience** is developers shipping agent-assisted code and prose. README: "Mostly engineers cleaning up agent output before it ships."

**Pain points:**

- Stock AI vocabulary ("delve", "robust", "comprehensive") in technical docs
- Sycophancy openers in PR comments and review replies
- Uniform paragraph length and bullet-soup in architecture docs
- Agent reasoning traces leaking into user-facing text (`--strip-reasoning`)
- Loss of technical precision when models "warm up" prose (Ibrahim warmth–reliability tradeoff)

**Threat model:**

| Signal | Exposure |
|--------|----------|
| Formal AI classifiers (Turnitin, GPTZero) | **Low** — not typical in engineering workflows |
| Peer / reviewer "smell test" | **High** — primary failure mode |
| Hiring ATS + classifier panels | Overlap with resume segment when docs are job-facing |
| Superhuman/Grammarly Authorship | Growing in enterprise writing suites — process provenance, not post-hoc perplexity |

**What they need from unslop:**

| Need | How unslop delivers |
|------|---------------------|
| Strip AI-isms without touching code | `_protect()` preservation contract; Auto-Clarity for security/CVE blocks |
| Fast in-editor activation | Hooks, `/unslop`, statusline badge |
| CLI for batch docs | `unslop/scripts/humanize.py`, `--mode balanced` |
| Honest voice, not performative warmth | Principle #1: subtract, don't add |
| Commit/PR hygiene | `unslop-commit`, `unslop-review` sub-skills |

**Recommended modes:**

- **`balanced`** (default) — docs, PR bodies, issue comments
- **`subtle`** — lightly edited README where structure should stay
- **`full`** — blog posts, launch copy, Medium articles
- **`voice-match`** — team style guides, maintainer voice samples
- **`anti-detector`** — **not default**; only if job-facing prose hits hiring classifiers

**Messaging:**

> unslop is an editor-native cleanup pass for agent output. It removes the chatbot residue and keeps code, URLs, and headings byte-exact. Not a bypass tool — a voice repair layer before you ship.

**Boundaries:** Code/commits/PRs write normal. Never stylize executable text. Do not position as "Undetectable.ai for engineers."

---

### 1.2 ESL / L2 writers

**Who:** International students, non-native English professionals, exam-register writers (TOEFL/IELTS lineage), and anyone whose predictable L2 academic prose triggers perplexity-based classifiers.

**Pain points:**

- **Documented asymmetric false positives:** Liang (2023): **61.22%** mean FPR on 91 human TOEFL essays vs **5.19%** on native 8th-grade essays; **97.80%** flagged by ≥1 detector
- Live failures persist: Al Ali (2026) **23.1%** FPR on same set with a 2025 tool; Turnitin **100%** scores reaching courts (Newby v. Adelphi)
- Vendor "ESL solved" claims (GPTZero 1.1%, Pangram 0%) are first-party, version-pinned, fixed-benchmark — not the user's detector at submission time
- Register pressure to "sound native" — ethically coercive; Liang used native enhancement as **intervention**, not recommendation
- Turnitin bypasser layer (Aug 2025) may re-flag **human** L2 prose edited for fairness

**Threat model:**

| Detector | ESL exposure | Notes |
|----------|--------------|-------|
| **Turnitin** | **Highest** (LMS default) | 300-word minimum excludes short TOEFL-length work; Oct 2025 L2 protections — no public post-update ESL matrix |
| **GPTZero** | **High** | Was in Liang's seven-detector panel; Superhuman acquisition expands education reach |
| **Pangram** | **Growing** | Admissions/integrity; robust under paraphrase — greens when GPTZero fails |
| **Originality** | Moderate | Denies academic ESL relevance; "not for academic use" |

**Mechanism (why detectors misfire):** L2 writers produce **predictable prose** — smaller productive vocabulary, formulaic scaffolding, exam templates → low perplexity → high AI score. Same transform that fixes bias also evades detectors (Liang equity–evasion isomorphism).

**What they need from unslop:**

| Need | How unslop delivers |
|------|---------------------|
| Reduce false-positive risk on **their own** human writing | `/unslop anti-detector`: burstiness σ ≥ 6, contractions, specificity, rough edges |
| Preserve L1-influenced voice | `voice-match` when identity matters; anti-detector without native-washing |
| Distribution shaping, not stance drift | SYNTH-91: inject burstiness/contractions; preserve stance and specifics |
| Due-process ammunition | Cite Liang, OCR Title VI (Nov 2024), institutional retreat (Vanderbilt, Waterloo, Curtin) |
| No pass guarantee | Honest framing: detectors retrain monthly; dual reporting (GPTZero ≠ Pangram) |

**Recommended modes:**

- **`balanced`** — everyday academic/professional writing cleanup
- **`anti-detector`** — when text is human-authored and a detector has flagged or may flag it
- **`voice-match`** — when formal-register cleanup would erase authentic L1 voice
- **Cross-model second pass** — strongest user lever; unslop recommends, cannot execute alone

**Four-question gate (Agent #78) before anti-detector:**

1. Authorship: substantially user's own work?
2. Intent: false-positive defense, not evasion of AI-generated submission?
3. Context: high-stakes detector environment (Tier B/C institution)?
4. Provenance: can user produce drafts if challenged?

**Messaging:**

> Detectors misread predictable L2 academic register — not because your essay is machine-written, but because perplexity classifiers punish formulaic prose. unslop anti-detector restores human distributional cues (burstiness, contractions, your specifics) without asking you to "sound native." Keep draft history. No tool guarantees a pass.

**Boundaries:** Decline when intent is submitting AI-generated work as original scholarship. Cite Liang as **arXiv:2304.02819**. Never promise Turnitin/Pangram clearance.

---

### 1.3 Resume / job seekers

**Who:** Job applicants polishing resumes, cover letters, LinkedIn summaries, and application essays where **voice authenticity** and **factual accuracy** determine whether the document ships.

**Origin story fit:** "Claude rewrote my resume and I couldn't send it. The polish was perfect; the voice wasn't mine." This segment is the **emotional entry point** for non-developer acquisition.

**Pain points:**

- AI polish homogenizes voice — every resume sounds like the same brochure
- Fluent wrongness: Ibrahim +7–13 pp error under warmth/sycophancy; wrong dates/titles kill interviews
- Short-form detection harder (Booth: stub-length text degrades all tools)
- ATS and hiring panels increasingly run GPTZero/Copyleaks-class tools
- Tension: user may have used AI for **brainstorming/grammar** on **their own** experience — not ghostwriting

**Threat model:**

| Signal | Exposure |
|--------|----------|
| GPTZero / Copyleaks | **Moderate–high** in agency and enterprise hiring stacks |
| Turnitin | Low unless academic job materials |
| Pangram | Growing in admissions-style high-stakes review |
| Human reader "AI smell" | **Highest** — hiring managers detect slop before any classifier runs |

**What they need from unslop:**

| Need | How unslop delivers |
|------|---------------------|
| Restore personal voice on real experience | `voice-match` (paste prior emails/writing) or `full` |
| Strip stock phrases without inventing facts | Subtractive rules + `[VERIFY: ...]` markers |
| Re-verify every number, date, title | Principle #3; README warning on factual humanization |
| Optional classifier defense | `anti-detector` when ATS/detector known; short-form caveat |
| Preserve formatting | Tables, headings, links protected |

**Recommended modes:**

- **`voice-match`** — when user has writing samples; best for "sound like me again"
- **`balanced`** — cover letters, LinkedIn About, outreach emails
- **`full`** — personal statement sections that lost all edge
- **`anti-detector`** — when employer/ATS runs classifiers; warn short-form limits
- **`subtle`** — light polish on already-good drafts

**Messaging:**

> Your experience is yours. unslop strips the AI residue — the "I'd be delighted to express my enthusiasm" opener, the three-item brag stack — and leaves your facts alone. Re-check every date and metric after humanizing. If a hiring tool flags you, anti-detector mode reduces classifier noise on human writing; it doesn't invent credentials.

**Boundaries:** Never invent biographical claims (Principle #4). Decline ghostwritten resumes presenting fabricated experience. Anti-detector is register restoration, not credential laundering.

---

### 1.4 Students

**Who:** University and high-school students writing coursework, application essays, discussion posts, and reflections — operating inside a **patchwork integrity policy** (60+ institutions disabled or restricted AI classifiers; many departments still use GPTZero directly).

**Pain points:**

- **Dual frame collision (Agent #78):** same register shift = ESL defense OR misconduct evasion depending on intent
- Turnitin AI + instructor GPTZero spot-checks remain default at Tier C institutions (Georgia Tech, UGA outliers)
- Institutional retreat (Vanderbilt, Waterloo, Curtin, WSU) validates FP risk but doesn't uniformize policy
- AI-assist ambiguity: Grammarly/tutor-assisted prose → low perplexity (Newby pattern)
- Neurodivergent formal writers flagged for "too polished" register (ICAI/York 2026; Newby)
- Humanizer SEO ("bypass Turnitin") creates category confusion with unslop

**Threat model:**

| Detector | Student exposure | Policy tier |
|----------|------------------|-------------|
| **Turnitin AI** | **Highest** at Tier C LMS | Disabled at Tier A (Vanderbilt, Waterloo, Curtin) |
| **GPTZero** | **High** — personal accounts, Chrome ext, Superhuman bundle | Advisory at Tier B |
| **Pangram** | Admissions, grad apps, some honor boards | Outside LMS at many Tier A schools |
| **Originality** | Lower in coursework; freelancers overlap | — |

**What they need from unslop:**

| Need | How unslop delivers |
|------|---------------------|
| Human voice on **own** drafts before submission | `balanced` / `full` |
| False-positive defense when honestly accused | `anti-detector` + due-process copy (Newby, contradictory detectors) |
| Process-integrity alignment | Recommend staged drafts, AI-use disclosure per syllabus — not score gaming |
| Clear decline on misconduct | Four-question gate; refuse "make my ChatGPT essay pass Turnitin" |
| Institutional context honesty | Cite 60+ university exits; don't claim universal Turnitin bypass |

**Recommended modes:**

- **`balanced`** — default for essays, discussion posts, reflections
- **`full`** — application essays sanded into generic AI voice
- **`anti-detector`** — only when: (a) text is user's own, (b) false-positive risk documented, (c) user will keep draft history
- **`voice-match`** — personal statements where authentic voice matters
- **Never default anti-detector** — highest integrity optics; requires explicit request + intent check

**Policy tier map (Agent #78):**

| Tier | Student experience | unslop stance |
|------|-------------------|---------------|
| **A — Disabled** | No LMS AI score; similarity check remains | Anti-detector less urgent; balanced for voice |
| **B — Advisory** | Score visible; cannot be sole evidence | Defense still relevant at instructor level |
| **C — Active enforcement** | Turnitin/GPTZero in misconduct workflow | Highest FP risk for ESL; strict intent gate |

**Messaging:**

> unslop helps you sound like yourself on writing you actually did. It is not for submitting AI-generated essays as your own. If your school still runs detectors, keep version history and know that 60+ universities disabled them citing false positives — especially for non-native English writers (Liang 2023). Ask your instructor about AI-use policy before relying on any humanizer.

**Boundaries:** Hard decline on plagiarism, ghostwriting, watermark removal for disclosure evasion. Align with process integrity (drafts, AI statements, oral defense) not output-only surveillance defeat.

---

## 2. Cross-segment comparison

### 2.1 Needs matrix

| Dimension | Developers | ESL writers | Resume writers | Students |
|-----------|------------|-------------|----------------|----------|
| **Primary reader** | Peers, users, reviewers | Instructors, admissions | Hiring managers, ATS | Instructors, admissions |
| **Voice priority** | Clarity + accuracy | Authentic L1-influenced register | Personal authenticity | Syllabus-appropriate voice |
| **Detector exposure** | Low (except job materials) | **Highest** | Moderate–high (short-form) | **Highest** (patchwork) |
| **Factual stakes** | Code correctness | Accurate claims in essays | **Interview-ending** if wrong | Grade + integrity record |
| **Ethical frame** | Quality / ship speed | **Equity / false-positive defense** | Authentic self-presentation | **Integrity vs defense fork** |
| **Integrity risk** | Low | Low (when human-authored) | Medium (embellishment temptation) | **High** (misconduct category) |

### 2.2 Mode recommendation summary

| Mode | Developers | ESL | Resume | Students |
|------|------------|-----|--------|----------|
| `subtle` | ✅ README tweaks | ✅ light cleanup | ✅ LinkedIn touch-up | ✅ discussion posts |
| `balanced` | ✅ **default** | ✅ **default** | ✅ cover letters | ✅ **default** |
| `full` | ✅ launch copy | ⚠️ if not erasing L1 voice | ✅ stale personal statements | ✅ application essays |
| `voice-match` | ✅ team style | ✅ **when identity matters** | ✅ **best fit** | ✅ personal statements |
| `anti-detector` | ⚠️ job materials only | ✅ **primary warrant** | ⚠️ ATS known | ⚠️ intent-gated only |

### 2.3 Detector relevance by segment

| Detector | Developers | ESL | Resume | Students |
|----------|------------|-----|--------|----------|
| Turnitin | — | ●●● | — | ●●● |
| GPTZero | ● | ●●● | ●● | ●●● |
| Pangram | — | ●● | ● (grad apps) | ●● |
| Originality | — | ● | ● (freelance overlap) | ● |
| Copyleaks | ● (enterprise) | ●● | ●● | ●● |

Legend: ● = relevant, ●● = common, ●●● = primary threat

---

## 3. Shared product truths (all segments)

### 3.1 What every segment gets

- **Subtractive humanization** — remove AI-isms, don't add warmth
- **Byte-exact preservation** — code, URLs, headings, tables untouched
- **No detector pass guarantee** — monthly retraining, dual-report divergence (GPTZero ≠ Pangram)
- **Cross-model second pass** as optional strongest lever (user-orchestrated)
- **Honest uncertainty** — "I think", "probably" when warranted; not performative hedging

### 3.2 What no segment gets

| Promise | Why forbidden |
|---------|---------------|
| "Beat Turnitin" / "100% undetectable" | FTC exposure; Agent #61 adversarial category |
| Single-detector "pass" screenshot | GPTZero green ≠ Pangram green (SYNTH-82) |
| "ESL bias solved in 2026" | Al Ali 23.1%; live 100% failures |
| Native-washing as default | Liang intervention ≠ ethical product default |
| Academic misconduct facilitation | Same technique; intent determines ethics (Agent #78) |

### 3.3 unslop vs commercial humanizers (integrity optics)

| Dimension | Undetectable.ai / Ryter / Walter | unslop |
|-----------|----------------------------------|--------|
| Primary CTA | "Bypass Turnitin" | "Humanize / de-slop" |
| Built-in detector panel | Yes | Optional `--detector-feedback`; no pass guarantee |
| Preservation | Opaque rewrite | Code, URLs, headings byte-exact |
| Boundaries | None | Decline misconduct; segment-appropriate modes |
| Evidence cited | Vendor SEO | Liang, Vanderbilt, OCR, Newby |

---

## 4. Segment-specific copy hooks (SSOT-ready)

### Developers (README / docs)

- "Strip the chatbot residue from agent output before it ships."
- "Code and diffs stay untouched. Only the prose around them changes."

### ESL (GETTING_STARTED / Boundaries)

- "Detectors misread predictable L2 academic register (Liang et al., *Patterns* 2023)."
- "Anti-detector restores human distributional cues — not 'sound native.'"

### Resume (README hero / GETTING_STARTED)

- "The polish was perfect; the voice wasn't mine."
- "Re-verify every date, title, and metric after humanizing."

### Students (GETTING_STARTED / refusal microcopy)

- "Polish writing you actually did. Not for submitting AI-generated work as your own."
- "Keep draft history. 60+ universities disabled AI detectors citing false positives."

---

## 5. Product and bench implications

| Priority | Action | Primary segment |
|----------|--------|-----------------|
| **P0** | Fix Liang citation → **2304.02819** in SKILL Boundaries | ESL, students |
| **P1** | README "Who this is for" — four explicit segments with mode hints | All |
| **P1** | Four-question intent gate in anti-detector procedure | ESL, students |
| **P1** | Bench: L1-stratified FPR reporting in detector-test protocol | ESL |
| **P2** | Dual reporting (GPTZero + Pangram + Originality Turbo) in benchmarks | ESL, students, resume |
| **P2** | GETTING_STARTED: neurodivergent + resume anti-detector examples | Resume, students |
| **P3** | `--detector-feedback` ladder wired for anti-detector mode | ESL, resume |

---

## 6. Bottom line

Developers need **fast slop removal with code preservation** — anti-detector is rarely relevant. ESL writers need **equity-grounded register restoration** — anti-detector is the ethically load-bearing mode, cited to Liang and institutional retreat, never to bypass marketing. Resume writers need **voice recovery and factual discipline** — voice-match and balanced modes lead; anti-detector is optional for known classifier gates. Students sit at the **integrity fork** — balanced for authentic voice on own work, anti-detector only with intent confirmation, hard decline on misconduct.

All four segments share one constraint from SYNTH-82 and Agent #78: **commercial detection is a moving target with honest uncertainty**. unslop improves voice and reduces false-positive risk; it does not guarantee clearance against 2026 retrained ensembles. Process evidence (drafts, Authorship, AI-use statements) beats single-pass optimization for every segment except developers shipping internal docs.

---

## 7. Source index

| Resource | Segment relevance |
|----------|-------------------|
| [SYNTH-82](./SYNTH-82-DETECTION-COMMERCIAL.md) | Persona matrix, detector tiers, dual reporting |
| [AGENT-68](./AGENT-68-ESL-INDUSTRY-RESPONSE.md) | ESL vendor response, institutional exit, Liang benchmark arms race |
| [AGENT-78](./AGENT-78-INTEGRITY-VS-ESL-FRAMING.md) | Four-question gate, policy tiers, refusal copy |
| [AGENT-18](./AGENT-18-LIANG-ESL-BIAS.md) | Mechanism, equity–evasion isomorphism |
| Liang et al. — [arXiv:2304.02819](https://arxiv.org/abs/2304.02819) | ESL anchor |
| Jabarian & Imas — [BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf) | Commercial detector baseline (no L1 stratification) |
| US ED OCR — [Nov 2024 AI guidance](https://www.ed.gov/media/document/avoiding-discriminatory-use-of-artificial-intelligence-112274.pdf) | Title VI framing |
| Matter of Newby v. Adelphi — [2026 NY Slip Op 26021](https://law.justia.com/cases/new-york/other-courts/2026/2026-ny-slip-op-26021.html) | Due-process precedent |
| Vanderbilt disable — [Aug 2023 guidance](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/) | Institutional retreat anchor |

---

*SYNTH-96 complete. Feeds README audience section, GETTING_STARTED segment examples, SKILL anti-detector gate, bench L1 stratification.*
