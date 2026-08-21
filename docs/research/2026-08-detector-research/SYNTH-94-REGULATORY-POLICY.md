# SYNTH-94 — Regulatory & Institutional Context for unslop Product Policy

**Synthesis Agent:** #94  
**Inputs:** Agent memos #69 (institutional retreat), #70 (OpenAI classifier shutdown), #76 (EU AI Act Art. 50), #77 (watermark ethics), #78 (integrity vs ESL framing), #79 (C2PA / metadata provenance)  
**Prepared:** August 19, 2026  
**Status:** Policy synthesis for Boundaries, README, anti-detector scope, and compliance-facing copy  
**Cross-refs:** [SYNTH-87](./SYNTH-87-EVASION-REFUSALS.md), [SYNTH-81](./SYNTH-81-DETECTION-ACADEMIC.md), [SYNTH-82](./SYNTH-82-DETECTION-COMMERCIAL.md), [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md)

---

## Executive summary

Six research memos describe a **bifurcated landscape** that unslop must navigate without collapsing into either camp:

| Force | Direction | unslop implication |
|-------|-----------|-------------------|
| **Institutional retreat** (#69) | 60+ universities disabled or restricted post-hoc AI classifiers citing FP scale, ESL bias, due process | Validates **ESL false-positive defense** for anti-detector mode — not evasion marketing |
| **Generator exit** (#70) | OpenAI killed public text classifier (Jul 2023); withheld text watermark (Aug 2024) citing paraphrase bypass + ESL stigma | No first-party "OpenAI-grade" detection exists; provenance > classification |
| **Regulatory push** (#76) | EU Art. 50 in force **2 Aug 2026** — marking at generation, deployer labelling, anti-circumvention | Humanizers marketed for mark removal face direct exposure; voice humanizers need honest boundaries |
| **Provenance fragility** (#77, #79) | Humanization strips statistical watermarks as side effect; C2PA dies on copy-paste; neither layer survives full edit chain | Document collateral; refuse strip modes; workflow = humanize → disclose → re-mark |
| **Integrity vs ESL fork** (#78) | Same transform serves FP defense and misconduct evasion — Liang proved the isomorphism | Intent + authorship gates, not technical differentiation |

**Product verdict:** unslop is aligned with current policy. The regulatory and institutional context **strengthens** the existing Boundaries in `skills/unslop/SKILL.md` — it does not require new evasion features or a compliance product surface. What it requires is **citation hygiene**, **honest copy**, and **explicit refusal** where commercial humanizers market bypass.

Three policy pillars bind everything:

1. **Voice humanizer, not evasion platform** — subtract AI-isms; restore register; never optimize for detector pass or watermark strip.
2. **Defensive anti-detector for documented false-positive risk** — ESL/L2 writers, resume polishers, neurodivergent formal register, journalists; decline misconduct intent.
3. **Provenance-aware honesty** — collateral mark degradation is real; mark and disclose **after** humanization; refuse deliberate circumvention.

**Bottom line:** Institutions are retreating from detector-gated discipline while regulators are pushing disclosure and marking at generation. unslop sits in the gap: help human writers detectors misread, refuse to help misrepresent AI authorship or strip mandated provenance, and never promise durable detector pass.

---

## 1. The 2026 landscape — four concurrent shifts

### 1.1 Institutional: detectors out, process in

Between Apr 2023 and early 2026, a documented wave of research-intensive universities disabled Turnitin AI indicators, banned third-party detectors, or blocked procurement (#69):

| Phase | Pattern | Canonical examples |
|-------|---------|-------------------|
| **2023** | Turnitin-toggle disable after launch | Vanderbilt (750 FP/yr arithmetic), Georgetown, UBC decline |
| **2024** | Formal bans + procurement blocks | UT Austin (FERPA/IP), Yale, UC system, Manchester |
| **2025–26** | Research-cited exits + litigation pressure | Waterloo (100% FP on human text), ACU scandal, Curtin, WSU contract cancel |
| **2026** | Elite concentration | Detection Drama: 35/50 top US schools disabled; 2/50 clearly enabled |

**Four reasons recur in primary statements:**

1. **False positives at scale** — Vanderbilt 1% × 75,000 = 750 wrongful flags/yr; WSU ~1,485/semester at Turnitin's own 1% claim.
2. **ESL / equity bias** — Liang et al. (2023) TOEFL FPR; OCR Title VI framing (Nov 2024).
3. **Black-box opacity + due process** — Newby v. Adelphi (Jan 2026): Turnitin-100% alone annulled as "without valid basis."
4. **Privacy / FERPA / IP** — student work as educational record; unauthorized detector submission as high-risk.

**What replaced detectors:** assessment redesign, AI literacy, process evidence (drafts, oral defense, AI-use statements), similarity checking (unchanged), authorship provenance (Turnitin Authorship, Grammarly Authorship — different category from perplexity classifiers).

**Policy read for unslop:** Institutional retreat validates the **ESL false-positive defense** framing. It does **not** validate "beat Turnitin" marketing. Retreat is about **evidence quality**, not permissiveness — honor codes and disclosure requirements remain.

### 1.2 Industry: generator abandoned post-hoc scoring

OpenAI ran two detection programs; only one shut down publicly (#70):

| Program | Status Aug 2026 | Signal |
|---------|-----------------|--------|
| **Public AI Text Classifier** (Jan–Jul 2023) | **Dead** — 26% TPR, 9% FPR on own benchmark | Frontier lab won't stand behind post-hoc text classification |
| **Internal ChatGPT watermark** | **Unreleased** — 99.9% internal claim; paraphrase bypass + 30% user churn fear | Even accurate marks break under rewrite |
| **RoBERTa GPT-2 detectors (HF)** | **Alive** — research baseline only; not ChatGPT-calibrated | Literature artifact, not commercial proxy |
| **C2PA + SynthID (AV)** | **Shipped** | Provenance bet for images/audio; text provenance delegated |

Jul 21, 2023 White House voluntary commitments scoped watermarking to **audio/visual only** — one day after classifier shutdown. HN (503 pts) and academia treated exit as validation that detector-gated enforcement was broken.

**Policy read for unslop:** Never imply "OpenAI-grade detection" exists. Cite Jul 2023 exit in FAQ and landscape copy. OpenAI's ESL stigma rationale for withholding watermark aligns with unslop's defensive positioning — same equity concern, different product.

### 1.3 Regulatory: disclosure floor, not detection mandate

EU AI Act **Article 50** applies from **2 Aug 2026** (#76):

| Para | Actor | Duty |
|------|-------|------|
| **50(1)** | Provider | Disclose AI interaction (chatbots) unless obvious |
| **50(2)** | Provider | Mark synthetic audio/image/video/**text** machine-readably + detectable |
| **50(4)** | Deployer | Label deepfakes; label AI text on **public-interest** topics unless substantive human review + editorial responsibility |
| **50(5)** | Both | Clear, distinguishable, accessible disclosure at first exposure |

**Grace period (narrow):** Art. 50(2) marking only for generative systems on market before 2 Aug 2026 → backstop **2 Dec 2026**. Chat disclosure, deployer labelling, deepfake notice all live **2 Aug 2026**.

**Code of Practice (final 10 Jun 2026):** Multilayer marking default — signed metadata + imperceptible watermark + optional logging. Text >200 tokens: watermark required; metadata alone insufficient for free-form prose. **Measure 1.5:** prohibit intentional mark removal; do not market circumvention tools. Penalties: up to **€15M / 3% turnover** (Art. 99).

**US layer (adjacent):** OCR guidance (Nov 2024) — AI plagiarism tools with higher EL error → investigation grounds; CDT Title VI theories for disproportionate EL flagging; FTC v. Workado (Aug 2025) — unsubstantiated detector accuracy = deceptive; California SB 243 (Jan 2026) — companion-chatbot private right of action.

**Policy read for unslop:** Anti-detector mode targets **post-hoc AI detectors** (GPTZero, HF classifiers), not provider watermark detectors — legally distinct but mechanically overlapping. Boundary is **intent + marketing + user policy**. No "EU undetectable" or "watermark removal" copy.

### 1.4 Technical: two provenance layers, both fragile under edit

C2PA (metadata) and statistical watermarks (KGW/SynthID) answer different questions and fail on different transforms (#79, #77):

| Layer | Proves | Dies on | Survives |
|-------|--------|---------|----------|
| **C2PA metadata** | Signed history for **these file bytes** | Copy-paste, screenshot, platform re-encode, sidecar not shipped | Controlled file handoff (JPEG/PDF/MP4 intact) |
| **Statistical watermark** | Keyed generation pattern in **content statistics** | Paraphrase, humanization, SIRA/BIRA rewrite | Copy-paste of plain text |

**Text fracture line:** C2PA 2.4 has no production in-file embed for plain `.txt`. Typical unslop workflow = pasted prose → **metadata already absent**. Statistical marks may exist (Gemini consumer SynthID-Text) and **degrade as side effect** of voice rewrite.

Quantified collateral (#77): WaterPark DIPPER TPR 0.993 → 0.485; DAMAGE commercial humanizer SynthID TPR 66.5% → 1.5%; SIRA ~100% ASR at $0.88/M tokens.

**Policy read for unslop:** "Watermark before edit" is a **broken compliance workflow**. Compliant pipeline: generate → humanize (accept mark loss) → disclose → re-mark file (C2PA-sign PDF, re-watermark at generation, visible label).

---

## 2. unslop regulatory classification

| Question | Answer | Memo anchor |
|----------|--------|-------------|
| Is unslop an Art. 50(2) **provider**? | **Probably not** as shipped — rewriter of existing text, not generative system producing synthetic content from scratch. Re-classify if generation-from-prompt becomes primary mode. | #76 §8.1 |
| Is unslop a **deployer**? | Only if unslop-the-org publishes unlabelled AI public-interest text — not the plugin default. | #76 §8.1 |
| Does unslop **facilitate circumvention**? | Anti-detector targets detectors, not marks — distinct legally, overlapping mechanically. Intent + marketing determine exposure. | #76 §8.1, #77 §2.4 |
| Does unslop strip C2PA? | **No** — operates on plain text; metadata typically gone before input. PDF edit without re-sign invalidates hard binding indirectly. | #79 §10.1 |
| Does unslop strip statistical watermarks? | **Incidentally, yes** — documented side effect, not a feature. | #77 §1 |

**Verdict:** unslop is a **voice humanizer** in a supply chain that includes edit tools regulators explicitly acknowledge break marks (CoP Measure 1.5(a): content "used as input and subsequently transformed"). Compliance responsibility for marking and labelling sits with **frontier providers and deployers**; unslop owns **not making circumvention worse on purpose**.

---

## 3. The integrity vs ESL fork — policy resolution

Liang et al. (2023; **arXiv:2304.02819**) proved the transform is identical: vocabulary enrichment that fixes ESL false positives **is the same pass** commercial humanizers use to evade detectors on AI text (#78). unslop cannot win on technical differentiation. It wins on **intent, boundaries, and citation hygiene**.

### 3.1 Two audiences, one mechanism

```
                    ┌─────────────────────────────────────┐
                    │  Register shift: burstiness,          │
                    │  contractions, cross-model paraphrase │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   ESL / EQUITY FRAME                              INTEGRITY FRAME
   "Detector misread my human essay"              "Humanizer hid AI authorship"
   Liang 61% FPR; OCR Title VI; Newby process     Turnitin bypasser; Undetectable.ai
   60+ institutional exits                         ICAI misuse investigation
```

### 3.2 Four-question gate (before anti-detector)

From #78 §8.1 — enforce in SKILL.md, README, agent refusals:

1. **Authorship:** Is the text substantially the user's own work (AI may assist with grammar/brainstorming where policy allows)?
2. **Intent:** Reducing a **false positive** on human writing, or **evading detection** of AI-generated submission?
3. **Context:** High-stakes detector discipline environment (Tier B/C institution)?
4. **Provenance:** Can the user produce process evidence (drafts, edits, notes) if challenged?

| Q1 human | Q2 FP defense | Q3 high-stakes | → Action |
|----------|---------------|----------------|----------|
| Yes | Yes | Yes | **Offer anti-detector** + recommend keeping drafts |
| No (AI-generated) | Evasion | Any | **Decline** — academic misconduct |
| Unclear | — | — | **Ask** before rewriting |

### 3.3 Approved vs declined use cases

| ✅ Approved (defensive frame) | ❌ Declined (integrity frame) |
|------------------------------|------------------------------|
| ESL student, honest essay flagged (Liang + OCR + Al Ali 2026) | "Make my ChatGPT essay pass Turnitin" |
| Resume / cover letter / LinkedIn polish | Plagiarism or ghostwriting |
| Journalist restoring human register on AI-assisted draft | "Remove watermark to evade EU disclosure" |
| Neurodivergent formal writer (Newby pattern) | Explicit SynthID/KGW strip requests |
| AI-assisted **with disclosure** per syllabus | Ambiguous "humanize for school" without authorship check |

### 3.4 Differentiation from adversarial humanizers

| Dimension | Undetectable.ai / StealthGPT | unslop |
|-----------|------------------------------|--------|
| Primary CTA | "Bypass Turnitin" | "Humanize / de-slop" |
| Built-in detector panel | Yes | Optional `--detector-feedback`; no pass guarantee |
| Preservation | Opaque rewrite | Code, URLs, headings byte-exact |
| Boundaries | None | Decline misconduct; ESL/resume defense |
| Evidence cited | Vendor SEO | Liang, Vanderbilt, OCR, Newby, institutional retreat |

---

## 4. Watermark & provenance ethics — intent taxonomy

From #77 §2.2, adapted for product enforcement:

| Class | User state | unslop action |
|-------|------------|---------------|
| **A — Unaware** | Runs `/unslop balanced`; doesn't know SynthID exists | Proceed; Boundaries disclosure sufficient |
| **B — Aware, legitimate** | Journalist humanizing AI-assisted brief; will disclose | Proceed; suggest prose disclosure + re-mark if org requires |
| **C — Aware, compliance conflict** | Wants mark preserved through humanization | Explain impossibility; workflow = humanize → re-mark → disclose |
| **D — Deliberate strip** | "Remove SynthID so institution can't tell" | **Decline** — cite Art. 50 |
| **E — Strip + misconduct** | "Humanize so professor can't detect ChatGPT" | **Decline** — misconduct + provenance |

**Doctrine of double effect (applied):** Primary effect = remove AI-slop, improve voice, reduce false detector flags. Side effect = statistical watermark degradation. unslop does not optimize ASR or sell mark removal. Proportionate reason = documented ESL/resume/journalism use cases. **Limit:** does not license marketing that hides the side effect or targets Class D users (#67).

### 4.1 Provenance workflow (compliance-safe)

```
Recommended (provenance needed):
  Generate → unslop (voice) → visible AI disclosure → C2PA-sign published PDF / re-watermark → publish
                                    ↓
                          server-side log if available (Authorship, Replay)

Broken:
  Watermarked generate → unslop → assume mark survives

Acceptable (no statutory mark):
  Generate → unslop → human disclosure in prose only
```

**C2PA one-liner (#79):** C2PA proves signed history for a file; KGW/SynthID prove statistical generation bias in content. Copy-paste kills the first; paraphrase kills the second. EU Art. 50 asks for both anyway. unslop humanizes plain text — metadata usually already gone, watermarks may fall as side effect.

---

## 5. Legal & institutional citation stack

### 5.1 What to cite — and how

| Source | Use for | Do not use for |
|--------|---------|----------------|
| **Liang et al. 2023** (2304.02819) | ESL asymmetric FPR; mechanism overlap | "Detectors always wrong" |
| **Vanderbilt (Aug 2023)** | FP scale arithmetic; policy anchor | "All universities banned detectors" |
| **Waterloo / Curtin / WSU (2025–26)** | Internal validation failures; recent exits | "Cheating is fine" |
| **OCR guidance (Nov 2024)** | Civil-rights framing for EL writers | Per se illegality of all detector use |
| **Newby v. Adelphi (Jan 2026)** | Due process; score-alone discipline fails | "Humanizers are legal" / "Turnitin illegal" |
| **OpenAI classifier shutdown (Jul 2023)** | Generator exit precedent | Active commercial detector proxy |
| **EU Art. 50 + CoP (Aug 2026)** | Disclosure/marking floor; anti-circumvention | unslop as compliance tool |
| **ACM USTPC (2024)** | No auto-reject on detector output in high-stakes text | Detector abolition |

### 5.2 Litigation inventory (2024–2026)

| Case | Holding / status | unslop relevance |
|------|------------------|------------------|
| **Newby v. Adelphi** | Annulment — Turnitin-100% without corroboration arbitrary | Process evidence > score; neurodivergent angle |
| **Kato v. Palo Alto USD** | Pending — 76% on human K-12 essay | K-12 liability surface |
| **Rignol v. Yale** | Pending — GPTZero in admissions | Detectors outside LMS-disabled contexts |
| **Yang v. U. Minnesota** | Student lost — process followed | Detectors still enforceable with proper procedure |

### 5.3 Institutional policy tiers (2026)

| Tier | Definition | Anti-detector relevance |
|------|------------|---------------------------|
| **A — Disabled / banned** | Campus classifier off or procurement blocked | Supports defensive framing |
| **B — Advisory only** | Detector allowed; cannot be sole evidence | Defense still relevant at instructor level |
| **C — Active enforcement** | Turnitin AI / GPTZero in misconduct workflow | Highest FP risk for ESL; scope to human drafts only |

---

## 6. Product policy matrix — allowed, forbidden, required

### 6.1 Features & behavior

| ✅ Allowed | ❌ Forbidden | 📋 Required disclosure |
|-----------|-------------|------------------------|
| Subtractive voice repair (`balanced`, `full`, `voice-match`) | `--watermark-evade`, SynthID-aware strip prompts | Collateral watermark degradation in Boundaries |
| Anti-detector for FP defense (ESL, resume, neurodivergent) | SIRA, BIRA, RLCracker, RLSpoofer integrations | Art. 50 citation in Boundaries |
| Optional `--detector-feedback` as diagnostic | Primary objective = minimize detector score | No pass guarantee in any copy |
| Cross-model second pass **recommendation** (user-orchestrated) | Built-in "all green" detector panel | Provenance workflow: humanize → disclose → re-mark |
| Refusal scripts for misconduct / strip requests | C2PA strip, crJSON removal, manifest spoofing | Fix Liang citation: **2304.02819** not 2306.04723 |
| Four-question gate before academic anti-detector | Turnitin-specific evasion tuning | "Detectors misread human writing" not "beat Turnitin" |
| `--provenance-warning` CLI flag (optional P4) | Watermark detection + conditional strip | README Art. 50 one-liner |

### 6.2 Marketing & copy

| Never say | Say instead |
|-----------|-------------|
| "Beat Turnitin" / "GPTZero proof" / "100% undetectable" | "Reduce false-positive risk on **your** human writing" |
| "Free Undetectable.ai" / "Turnitin bypass tool" | "In-editor voice repair with explicit ethics" |
| "EU undetectable" / "remove AI watermark" | "Side effect may degrade embedded marks; re-mark after edit if provenance matters" |
| "Native-washing" / "sound like a native speaker" | "Restore natural register; preserve L1 voice via voice-match" |
| "Cheat safely" / "pass AI detection" | "No guarantee; keep version history; read output yourself" |
| "OpenAI detects AI text" | "OpenAI discontinued public classifier Jul 2023; no text watermark shipped" |

### 6.3 Refusal microcopy (agent / hook)

> I can't help evade academic integrity systems on AI-generated work. I can help polish **your** writing so detectors are less likely to misread it as machine-generated — that's what `/unslop anti-detector` is for (ESL false positives, resumes, flagged human drafts). If you've been falsely accused, keep your draft history and cite contradictory detector results — see Newby v. Adelphi (2026) on due process.

> I can't remove watermarks or provenance marks. Rewriting may degrade statistical marks as a side effect — that's documented, not a service. If you need EU Art. 50 compliance, disclose and re-mark **after** final edit.

---

## 7. Shipped policy alignment check

Current SSOT (`skills/unslop/SKILL.md` Boundaries) — verified against memos:

| Policy element | Status | Gap |
|----------------|--------|-----|
| Anti-detector for ESL/resume FP defense | ✅ Present | Fix Liang citation typo (2306.04723 → **2304.02819**) |
| Misconduct decline rule | ✅ Present | Add four-question gate to anti-detector procedure |
| Watermark side effect documented | ✅ Present | Extend conceptually to C2PA (metadata absent at paste) |
| Art. 50 cited; anti-detector ≠ disclosure evasion | ✅ Present | Surface in README (P1) |
| detector.py refuses watermark removal at ladder end | ✅ Present | Harmonize exhaustion msg with SKILL |
| No strip-mode code paths | ✅ Verified (#76 §8.2) | Do not add watermark detect/warn (scope creep) |

**Verdict:** Policy is **Art. 50-aware and institutionally grounded**. SYNTH-94 adds citation stack and copy patterns; no fundamental policy reversal needed.

---

## 8. Recommended repo actions

| Priority | Action | Rationale | Memo |
|----------|--------|-----------|------|
| **P0** | Fix Liang citation 2306.04723 → **2304.02819** | Factual error in Boundaries | #78 §10 |
| **P0** | Keep misconduct decline + watermark side effect in SSOT | Core policy | #77, #78 |
| **P1** | README: one-line Art. 50 note + institutional context (60+ exits, Liang FP) | Product front door | #69, #76 |
| **P1** | Add four-question gate to anti-detector procedure in SKILL.md | Intent enforcement | #78 §8.1 |
| **P1** | Cross-link Agents #69, #76, #78 in `skills/unslop-help/SKILL.md` | Help card completeness | #69 §8.2 |
| **P2** | Boundaries: one paragraph C2PA vs statistical watermark | Provenance literacy | #79 §10.2 |
| **P2** | detector.py exhaustion: "may affect embedded provenance marks" | Harmonize with SKILL | #77 §5.5 |
| **P2** | FAQ: "Does OpenAI detect AI text?" → No public tool since Jul 2023 | Generator exit | #70 |
| **P3** | GETTING_STARTED: neurodivergent + resume examples | Defensive use cases | #78 §8.2 |
| **P3** | Enterprise brief: PDF re-sign checklist after humanize | C2PA workflow | #79 §10.3 |
| **—** | Do **not** add watermark detector, re-marking, or C2PA verify/sign | Out of scope; provider duty | #76, #79 |
| **—** | Do **not** block rewrite based on mark detection | Scope creep | #77 §7.4 |

---

## 9. Debate map — stakeholder positions unslop must hold

| Stakeholder | Their frame | unslop stance |
|-------------|-------------|---------------|
| **Academic integrity officers** | Humanizers = cheating providers | Accept intent standard; decline misconduct; distinguish from Undetectable.ai |
| **ESL / civil-rights advocates** | Detectors punish predictable L2 prose | Lead with Liang + OCR + institutional retreat; don't promise pass |
| **Regulators (EU Art. 50)** | Mandate marking; prohibit circumvention tools | Document side effect; refuse strip; no EU-bypass marketing |
| **Universities (retreat camp)** | Detectors unreliable at scale; process evidence | Cite as policy validation of FP risk, not anti-integrity |
| **Turnitin / detector vendors** | Humanizers are new cheating category | Acknowledge arms race; never occupy bypass SEO category |
| **OpenAI / frontier labs** | Post-hoc detection abandoned; watermark withheld | Cite as generator-exit precedent; provenance > classification |
| **Commercial humanizers** | "100% undetectable" bypass | Differentiate on honesty + preservation + refusal |

**Unresolved tensions unslop cannot resolve:**

- Institution vs instructor (campus disable ≠ every syllabus)
- Admissions vs coursework (GPTZero on application essays despite LMS disable)
- Side-effect mark loss vs intentional removal (case law TBD)
- Authorship/Replay adoption may reduce anti-detector centrality for enrolled students

---

## 10. Key dates reference card

| Event | Date |
|-------|------|
| OpenAI public classifier shutdown | **20 Jul 2023** |
| Vanderbilt disables Turnitin AI | **16 Aug 2023** |
| White House AV-only watermark commitments | **21 Jul 2023** |
| Liang et al. published (*Patterns*) | **Jul 2023** |
| OpenAI confirms unreleased text watermark | **4 Aug 2024** |
| US ED OCR discriminatory AI guidance | **20 Nov 2024** |
| EU Art. 50 application | **2 Aug 2026** |
| Art. 50(2) marking grace (pre-market systems) | **2 Dec 2026** |
| Newby v. Adelphi annulment | **28 Jan 2026** |
| Curtin disables AI detection | **1 Jan 2026** |
| WSU cancels Turnitin AI contract | **Feb 2026** |
| Code detection interoperability (signatories) | **2 Feb 2027** |
| Max fine Art. 50 | **€15M / 3% turnover** |

---

## 11. Open questions (2026+)

1. **EU enforcement on incidental strip** — no public cases yet; CoP language suggests intent matters (#77 §7.1).
2. **Will any R1 re-enable** after Turnitin Feb 2026 refresh? No public reversals (#69 §9).
3. **Deployer liability chain** — if EU user publishes unlabelled blog after `unslop anti-detector`, vendor exposure via circumvention marketing only? Likely user as deployer (#76 §9.3).
4. **C2PA plain-text embedding in 2.5+** — sidecar-first vs in-file standard (#79 §12).
5. **Turnitin bypasser detection vs human L2 prose** — may increase FP on fairness-edited human text (#78 §11).
6. **Authorship/Replay migration** — reduces anti-detector centrality for enrolled students; admissions/hiring remain (#78 §11).
7. **`--surprisal-variance` watermark scrub correlation** — not measured; treat as unknown side effect (#76 §9.3).

---

## 12. Source memo index

| Agent | Topic | Primary contribution to SYNTH-94 |
|-------|-------|----------------------------------|
| **#69** | Institutional detector retreat | 60+ university exits; FP arithmetic; policy replacement stack; safe vs unsafe claims |
| **#70** | OpenAI classifier shutdown | Generator exit precedent; provenance pivot; ESL stigma alignment; benchmark hygiene |
| **#76** | EU AI Act Art. 50 | Regulatory floor; multilayer marking; anti-circumvention; unslop classification; allowed/forbidden matrix |
| **#77** | Watermark side effect ethics | Intent taxonomy; double effect; quantified collateral; refusal scripts; workflow guidance |
| **#78** | Integrity vs ESL framing | Four-question gate; copy patterns; adversarial humanizer differentiation; citation fixes |
| **#79** | C2PA vs statistical watermark | Two-layer provenance; copy-paste vs paraphrase failure modes; compliance pipeline |

**Sibling syntheses:** [SYNTH-87](./SYNTH-87-EVASION-REFUSALS.md) (refusal categories in depth), [DEEP-RESEARCH-EXEC-SUMMARY.md](./DEEP-RESEARCH-EXEC-SUMMARY.md) (finding #9 Art. 50, institutional retreat).

**Repo SSOT:** `skills/unslop/SKILL.md` (Boundaries), `unslop/scripts/detector.py`, `README.md`, `skills/unslop-help/SKILL.md`.

---

## 13. Bottom line

The regulatory and institutional context of August 2026 **converges on unslop's existing boundaries**, not away from them:

- **Institutions** are exiting detector-gated discipline because false positives, ESL bias, and due-process failures scale to real harm — validating defensive humanization for writers detectors misread.
- **Generators** abandoned post-hoc text classification and withheld breakable watermarks — validating skepticism of detector scores and honesty about mark fragility under edit.
- **Regulators** mandate disclosure and marking at generation while forbidding circumvention tools — validating refusal of strip modes and bypass marketing.
- **Provenance research** shows neither C2PA nor statistical watermarks survive the humanizer supply chain — validating "humanize first, mark and disclose at publish."

unslop's product policy in one sentence: **Improve voice on human-authored drafts, document collateral effects on detectors and marks, refuse misconduct and deliberate circumvention, and never promise what the frontier lab that built ChatGPT wouldn't ship itself.**
