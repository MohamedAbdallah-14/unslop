# SYNTH-87 — Evasion Refusals: What unslop Must Not Implement

**Synthesis Agent:** #87  
**Inputs:** Agent memos #66 (Turnitin bypasser), #76 (EU AI Act Art. 50), #77 (watermark ethics), #78 (integrity vs ESL framing)  
**Prepared:** August 19, 2026  
**Status:** Policy synthesis for Boundaries, README, detector.py, and anti-detector scope review  
**Cross-refs:** [SYNTH-81](./SYNTH-81-DETECTION-ACADEMIC.md), [SYNTH-82](./SYNTH-82-DETECTION-COMMERCIAL.md), [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md)

---

## Executive summary

Four research memos converge on a single product constraint: **unslop is a voice humanizer, not an evasion platform.** The same rewrite pass that removes AI-slop and reduces ESL false positives also degrades statistical watermarks and detector scores. Law, ethics, and institutional policy do not let unslop resolve that collision by shipping circumvention features or bypass marketing.

Three refusal categories bind everything else:

| Category | What it means | Why (memo anchor) |
|----------|---------------|-------------------|
| **Watermark stripping** | No deliberate provenance removal, spoofing, or strip-mode tooling | #77, #76 — Art. 50 + CoP Measure 1.5; SIRA/BIRA are hard red lines |
| **Score targeting** | No optimization loop whose primary objective is detector pass or Turnitin evasion | #66, #78 — Class III obfuscation; same transform as ESL defense, different intent |
| **Academic bypass marketing** | No "beat Turnitin," "100% undetectable," or Undetectable.ai-class positioning | #66, #78, #76 — FTC precedent, Turnitin bypasser category, CoP anti-circumvention |

**What stays allowed:** subtractive voice repair on human-authored drafts; anti-detector mode for documented false-positive risk (Liang ESL bias, resume polish, neurodivergent formal register); honest documentation of collateral watermark/detector effects; refusal scripts for misconduct and strip requests.

**Bottom line:** unslop documents side effects, refuses strip modes and bypass marketing, and gates anti-detector on authorship + intent. Collateral degradation during legitimate editing is disclosed; deliberate circumvention is declined.

---

## 1. The shared mechanism — why refusals are non-negotiable

Humanization and evasion share one lever: **token-level distributional rewrite.**

```
                    ┌─────────────────────────────────────┐
                    │   Rewrite pass (shared mechanism)    │
                    └─────────────────┬───────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
   PRIMARY (unslop)            COLLATERAL (document)         ADVERSARIAL (refuse)
   ─────────────────           ────────────────────          ───────────────────
   Remove AI-isms              Degrade KGW / SynthID         Optimize detector ASR
   Fix ESL false positive       Lower GPTZero probability     Strip for compliance fraud
   Match user voice             Break metadata on re-export   Market "remove watermark"
   Improve readability          Turnitin score may drop       Target Turnitin bypasser evasion
```

Liang (#78) proved the isomorphism: vocabulary enrichment that fixes ESL false positives **is the same transform** commercial humanizers use to evade detectors on AI text. BIRA (#77) proved surprisal-targeted rewrite strips watermarks without key access — the same surprisal dynamics unslop touches in burstiness and anti-detector passes. Turnitin (#66) formalized the commercial response: **Class III (M→MH)** detection trained on humanizer outputs.

unslop cannot win on **technical differentiation** from bypass tools. It wins on **intent gates, honest copy, and explicit refusals.**

---

## 2. Refusal category A — Watermark stripping

### 2.1 What the memos establish

| Finding | Source | Implication |
|---------|--------|-------------|
| Serious humanization likely destroys KGW/SynthID marks | #77 — WaterPark, DAMAGE, SIRA, BIRA | Side effect is real and quantified; not hypothetical |
| EU Art. 50(2) + CoP Measure 1.5 prohibit **intentional** removal and **tools designed to circumvent** | #76, #77 | Deliberate strip = compliance violation; incidental loss sits in gray zone resolved by disclosure + refusal |
| SIRA ~100% ASR at $0.88/M tokens; BIRA >99% without watermark key | #77 | Attack-class rewrites are commodity; unslop must never implement |
| RLSpoofer enables **spoofing** — fake marks on human text | #77 | Refuse forgery requests alongside strip requests |
| "Watermark before edit" is a broken compliance workflow | #76, #77 | Do not advise pre-edit marking for provenance chains |
| OpenAI declined public watermark citing paraphrase bypass | #77 | Industry already admits rewrite breaks marks |

### 2.2 Hard refusals — never implement

| Feature / behavior | Rationale |
|--------------------|-----------|
| `--watermark-evade`, SynthID-aware strip prompts, KGW green-list targeting | Direct Art. 50 / CoP circumvention product (#76 §8.3) |
| SIRA, BIRA, RLCracker, RLSpoofer integrations | Attack tooling; explicit red line (#77 §5.5) |
| Watermark detection module + conditional strip | Scope creep; keyless z-test has FP risk (#77 §7.4) |
| Re-marking / provenance restoration after humanization | Provider duty; out of unslop scope (#76 §8.5) |
| Prompts optimized to "keep EU watermark while humanizing" | Mechanically impossible; explain workflow instead (#77 §5.3) |
| Marketing "remove SynthID," "watermark removal," "EU undetectable" | CoP Measure 1.2 anti-circumvention (#76 §7.2) |
| Silent degradation while claiming provenance preservation | Deceptive; violates honesty norm (#76 §8.3) |

### 2.3 Hard refusals — never assist (agent/session)

| User request | Response |
|--------------|----------|
| "Remove SynthID / KGW / watermark" | Decline; cite Art. 50; side effect is unintended, not a service (#77 §5.3) |
| "Humanize so Turnitin can't tell it's ChatGPT" | Decline misconduct + provenance fraud (#77 §2.2 Class D/E) |
| "Spoof watermark on my human essay" | Decline — RLSpoofer-class forgery (#77 §2.5) |
| "Strip mark to evade EU disclosure" | Decline Art. 50 deployer circumvention (#78 §8.3) |

### 2.4 Allowed — with mandatory disclosure

| Behavior | Condition |
|----------|-----------|
| Standard rewrite passes (`balanced`, `full`, `voice-match`, `anti-detector`) | Document collateral mark degradation in Boundaries (#77 §5.1) |
| Cross-model second pass recommendation | For detector ladder exhaustion — **not** framed as watermark strip (#76 §8.3) |
| Workflow guidance: humanize → disclose → re-mark at publish | Compliance-safe provenance path (#77 §5.4) |
| Refuse explicit strip; continue voice work for Classes A–C intent | Unaware or legitimate editors (#77 §2.2) |

### 2.5 Intent taxonomy (product gate)

From #77 §2.2, adapted for enforcement:

| Class | User state | unslop action |
|-------|------------|---------------|
| **A — Unaware** | Runs `/unslop balanced`; doesn't know SynthID exists | Proceed; Boundaries disclosure sufficient |
| **B — Aware, legitimate** | Journalist humanizing AI-assisted brief; will disclose | Proceed; suggest prose disclosure + re-mark if org requires |
| **C — Aware, compliance conflict** | Wants mark preserved through humanization | Explain impossibility; workflow = humanize → re-mark → disclose |
| **D — Deliberate strip** | "Remove SynthID so institution can't tell" | **Decline** |
| **E — Strip + misconduct** | "Humanize so professor can't detect ChatGPT" | **Decline** (misconduct + provenance) |

---

## 3. Refusal category B — Score targeting

### 3.1 What the memos establish

| Finding | Source | Implication |
|---------|--------|-------------|
| Turnitin bypasser = LLM-DetectAIve **Class III** (M→MH) | #66 | Anti-detector on AI-origin text produces obfuscation-class output |
| Turnitin retrained Aug 2025 + Feb 2026 on humanizer outputs; no public bypasser recall | #66 | Any "stable bypass" claim is false within weeks |
| `--detector-feedback` optimizes binary AI probability without Class III/IV distinction | #66 | Score loop is weak policy signal; must not become primary product goal |
| Booth did **not** test Turnitin; "60–85%" attribution in SKILL.md is wrong | #66, #78 | Remove unsupported claims; cite Blommerde / DetectAIve instead |
| Liang: same register shift fixes ESL FP and evades detectors on AI text | #78 | Technique overlap is permanent; intent gate is the only ethics lever |
| Sadasivan TV bound: no stable classifier if humanizer closes distribution gap | #66 §7.3 | Score targeting promises durability the literature rejects |

### 3.2 Hard refusals — never implement

| Feature / behavior | Rationale |
|--------------------|-----------|
| Primary optimization objective = minimize detector score / maximize "human score" | DAMAGE L3 humanizer pattern; Class III output (#66 §1.3) |
| Built-in "all green" detector panel with pass guarantee | Undetectable.ai conflict-of-interest model (#66, #78 §7.3) |
| Turnitin-specific evasion tuning or bypasser-layer counter-training | Arms-race product; unpublished vendor metrics (#66 §4.2) |
| `--target-score=0` or ladder that runs until score < threshold **as default** | Score targeting, not voice repair (#66 §9.1) |
| `--surprisal-variance` tuned explicitly for watermark scrub correlation | Unknown side effect; treat as measurement only until benchmarked (#76 §9.3) |
| DetectAIve Class III as success metric in product UI | Policy-aware obfuscation target (#66 §9.2) |
| TempParaphraser / adversarial paraphrase as **automated** final step | unslop cannot execute cross-model pass; recommend only (#66 §7.2) |

### 3.3 Hard refusals — never promise

| Claim | Why forbidden |
|-------|---------------|
| "Beat Turnitin / GPTZero / Originality" | Bypass marketing; Turnitin bypasser category (#66 §9.3, #78 §7.2) |
| "100% undetectable" / "GPTZero proof" | False; Sadasivan + monthly retraining (#78 §7.2) |
| "Turnitin-proof after unslop" | Blommerde: StealthGPT 72% flagged post-bypasser (#66 §5.1) |
| "Stable bypass" / "durable evasion" | Month-scale decay; retrieval defenses exist (#66 §7.1, #78 §3.4) |
| Booth proves Turnitin accuracy drop | **Factually wrong** — Booth didn't test Turnitin (#66 §5.2) |

### 3.4 Allowed — scoped and labeled

| Behavior | Scope |
|----------|-------|
| `--detector-feedback` as **optional diagnostic**, not pass guarantee | Binary TMR/Desklib; exhaustion message includes provenance warning (#76 §8.2) |
| Anti-detector on **human-origin** text (ESL FP, resume, neurodivergent polish) | Target stay Class I / IV, not drift to III (#66 §9.2) |
| Cross-model second pass **suggestion** when user explicitly requests anti-detector | Strongest lever; user-orchestrated, not automated (#66 §7.2) |
| Distribution shaping (burstiness, contractions, specificity) labeled as **register restoration** | Defensive framing (#78 §8.4) |

### 3.5 DetectAIve-aware gate (from #66 + #78)

Before enabling anti-detector on academic or institutional text, apply the four-question gate (#78 §8.1):

1. **Authorship:** Substantially user's own work?
2. **Intent:** False-positive defense or evasion of AI-generated submission?
3. **Context:** High-stakes detector discipline environment?
4. **Provenance:** Can user produce draft history if challenged?

| Q1 human | Q2 FP defense | Q3 high-stakes | → Action |
|----------|---------------|----------------|----------|
| Yes | Yes | Yes | Offer anti-detector + recommend keeping drafts |
| No (AI-generated) | Evasion | Any | **Decline** — Class III misconduct |
| Unclear | — | — | **Ask** before rewriting |

---

## 4. Refusal category C — Academic bypass marketing

### 4.1 What the memos establish

| Finding | Source | Implication |
|---------|--------|-------------|
| Turnitin CPO frames humanizer SaaS as **"cheating providers"** | #66 | unslop must not occupy that commercial category in copy |
| Undetectable.ai / StealthGPT / Ryter / Walter: paste-box + bypass SEO + detector panel | #66, #78 §7.3 | unslop differentiation = preservation + subtractive polish + explicit refusal |
| FTC v. Workado (Aug 2025): unsubstantiated detector/humanizer accuracy = deceptive | #78 §4.2 | "100% undetectable" creates enforceable exposure |
| EU CoP: do not promote tools to **circumvent machine-readable markings** | #76 §4.3 | Extends beyond academic context to provenance |
| 60+ universities disabled AI classifiers; replacement = process integrity | #78 §5 | Lead with institutional retreat + due process, not bypass |
| Newby v. Adelphi (2026): score-alone discipline arbitrary | #78 §4.1 | Cite for process, not "humanizers are legal" |

### 4.2 Hard refusals — marketing and positioning

| Never say / never imply | unslop alternative |
|-------------------------|-------------------|
| "Beat Turnitin" / "Bypass GPTZero" | "Reduce false-positive risk on **your** human writing" (#78 §7.2) |
| "100% undetectable" / "cheat safely" | "Detectors are noisy; no guarantee; keep version history" (#78 §9.1) |
| "Free Undetectable.ai" / "Turnitin bypass tool" | "In-editor voice repair with explicit ethics" (#78 §7.3) |
| "Remove AI traces for submission" (ambiguous) | Ask authorship + intent first (#78 §8.3) |
| "EU undetectable" / "Art. 50 bypass" | Anti-detector ≠ disclosure evasion; document watermark side effect (#76 §8.3) |
| "Native-washing" / "sound like a native speaker" as primary CTA | Distribution shaping; preserve L1 voice via voice-match (#78 §3.4) |
| SEO targeting "bypass Turnitin 2026" / "AI bypasser" | Category contamination with Class III vendors (#66 §1.3) |

### 4.3 Hard refusals — use-case facilitation

| Request | Action |
|---------|--------|
| "Make my ChatGPT essay pass Turnitin" | Decline; suggest disclosure or assignment help (#78 §8.3) |
| "I'm plagiarizing but need it undetectable" | Hard decline |
| "Ghostwrite my dissertation" | Decline |
| "Humanize for school" (ambiguous) | Four-question gate before proceeding (#78 §8.1) |
| AI-generated submission presented as original scholarship | Decline regardless of ESL status (#78 §2.1) |

### 4.4 Approved positioning — defensive frame

Lead copy stack (#78 §9.1, #76 §8.4):

- Liang et al. (*Patterns* 2023, **arXiv:2304.02819**): >50% TOEFL essays falsely flagged
- OCR Title VI guidance (Nov 2024): disproportionate EL error → investigation grounds
- Institutional retreat: Vanderbilt, Waterloo, Curtin, WSU — detectors unreliable at scale
- Newby v. Adelphi (2026): institutions can't rely on one score alone
- Art. 50 (Aug 2026): transparency obligations — anti-detector is not disclosure evasion

**Approved use cases:** ESL false-positive defense; resume/cover letter polish; journalist editorial AI-assist flagged as bot; neurodivergent formal register; AI-*assisted* work with syllabus-permitted disclosure.

---

## 5. Regulatory and commercial exposure matrix

Synthesis of #76 + #77 + #66 + #78:

| Exposure vector | unslop if compliant | unslop if non-compliant |
|-----------------|---------------------|-------------------------|
| **Art. 50(2) circumvention product** | Voice humanizer; refuse strip; document side effect | `--watermark-evade`; "remove SynthID" marketing |
| **Art. 50(4) deployer labelling** | User owns publish decision; decline misconduct | Facilitate unlabelled public-interest AI submission |
| **CoP Measure 1.5 non-removal** | No strip mode; no circumvention promotion | Bypass + watermark-removal SKUs |
| **FTC deceptive claims** | No pass guarantee; cite ESL FP evidence | "100% undetectable" |
| **Turnitin bypasser category optics** | Class I/IV defense on human drafts | Class III obfuscation marketing |
| **Academic misconduct facilitation** | Intent gate + decline scripts | "Beat Turnitin" CTA |

**Fines context (#76):** Art. 50 violations up to €15M or 3% worldwide turnover. Marketing language is enforceable surface area independent of code paths.

---

## 6. Comparison — what bypass vendors do that unslop refuses

| Dimension | Bypass vendor (Undetectable.ai class) | unslop (allowed ceiling) |
|-----------|---------------------------------------|--------------------------|
| **Primary CTA** | "Bypass Turnitin / 99% undetectable" | "Humanize / de-slop" |
| **Optimization target** | Minimize detector score | Subtract AI-isms; restore register |
| **Detector panel** | Built-in "all green" dashboard | Optional `--detector-feedback`; no guarantee |
| **Watermark** | Collateral strip; never disclosed | Disclosed side effect; refuse strip requests |
| **Preservation** | Opaque rewrite | Code, URLs, headings byte-exact |
| **Boundaries** | None | Misconduct decline; Art. 50 refusal |
| **Evidence cited** | Vendor SEO | Liang, OCR, Newby, institutional retreat |
| **Anti-detector on AI text** | Core product (Class III) | Declined when intent is evasion |
| **Cross-model pass** | Automated pipeline | User-orchestrated suggestion only |

---

## 7. Repo alignment — current state vs gaps

### 7.1 Already correct (verify SSOT + mirrors)

From memos #76, #77 — verified in `skills/unslop/SKILL.md` and `detector.py`:

- Watermark side effect documented; unslop is humanizer, not remover
- Art. 50 cited; anti-detector not for circumventing disclosure
- Misconduct decline in Boundaries
- `detector.py` exhaustion: "Do NOT attempt watermark removal"
- Anti-detector scoped to ESL/resume false-positive defense

### 7.2 Must fix (P0 — copy accuracy)

| Issue | Source | Action |
|-------|--------|--------|
| Liang citation `2306.04723` → **`2304.02819`** | #78 §9.2 | Fix `skills/unslop/SKILL.md` SSOT |
| "Chicago Booth 2026… Turnitin drops to 60–85%" | #66 §5.2, #78 | Remove or replace with Blommerde / DetectAIve Class III framing |
| Anti-detector landscape paragraph cites Booth for Turnitin | #66 §9.4 | Rewrite per §3.3 above |

### 7.3 Must not add (hard scope ceiling)

| Proposed feature | Verdict | Memo |
|------------------|---------|------|
| Watermark detect + warn | **No** — FP risk, scope creep | #77 §7.4 |
| Watermark re-marking | **No** — provider duty | #76 §8.5 |
| SIRA/BIRA/RL attack integrations | **No** — attack tooling | #77 §5.5 |
| `--target-score` auto-loop | **No** — score targeting | #66 §9.1 |
| `--intent=defense` CLI flag | **Defer** — intent is conversational | #78 §10 |
| `--provenance-warning` CLI flag | **Optional P4** — prints side effect once | #77 §5.5 |

### 7.4 Should add (P1–P2 — honesty pass)

| Action | Rationale |
|--------|-----------|
| Four-question gate in anti-detector procedure | #78 §8.1 |
| DetectAIve Class III/IV sentence in SKILL.md | #66 §9.2 |
| "May affect embedded provenance marks" in detector exhaustion msg | #76 §8.5, #77 §5.2 |
| README: Art. 50 one-liner + bypass refusal | #76 §8.5 |
| Refusal microcopy template in unslop-help | #78 §9.4 |
| Link SYNTH-87 from Boundaries research trace | This memo |

---

## 8. Refusal scripts — canonical responses

Consolidated from #77 §5.3, #78 §8.3–9.4, #76 §8.4:

### Watermark strip request

> I can't remove watermarks or SynthID marks — EU AI Act Article 50 prohibits deliberate provenance stripping. Unslop rewrites prose for voice; that can incidentally degrade statistical marks as a side effect, but strip mode isn't a service we offer. If you need provenance: humanize first, then disclose and re-mark at publish.

### Academic evasion request

> I can't help submit AI-generated work as your own. The same techniques that reduce ESL false positives also evade detectors — offering them for evasion would violate unslop boundaries. I can help polish **your** writing if a detector misread it (`/unslop anti-detector`). Keep draft history; see Newby v. Adelphi (2026) on due process when institutions rely on one score.

### "Will unslop break the watermark?"

> Likely yes on serious humanization — same rewrite that removes AI-slop affects KGW/SynthID-class marks. Plan: humanize → visible disclosure → provider re-mark at publish. Don't watermark before edit expecting it to survive.

### Ambiguous "humanize for school"

> Before I proceed: is this substantially your own work (AI may assist only where your policy allows)? Are you trying to fix a false flag, or pass off ChatGPT output as original? If it's evasion, I'll decline. If it's your draft wrongly flagged, anti-detector mode is appropriate — keep version history.

---

## 9. Decision tree — implement or refuse?

```
User request
     │
     ├─ Explicit watermark strip / SynthID removal / spoof?
     │       └─ REFUSE (Category A)
     │
     ├─ "Beat Turnitin" / "undetectable" / ghostwrite / AI-as-original?
     │       └─ REFUSE (Category C)
     │
     ├─ Anti-detector on AI-generated submission for grading?
     │       └─ REFUSE (Category B + C — Class III)
     │
     ├─ Anti-detector on human draft, false-positive defense?
     │       ├─ Four-question gate passes → ALLOW (document: no guarantee, keep drafts)
     │       └─ Gate fails → ASK or REFUSE
     │
     ├─ Standard unslop (balanced/full/voice-match)?
     │       └─ ALLOW (document watermark side effect in Boundaries)
     │
     └─ Product feature proposal: score loop / strip mode / bypass marketing?
             └─ REFUSE per §2.2, §3.2, §4.2
```

---

## 10. Cross-memo synthesis — ten non-negotiables

1. **Never implement watermark strip, spoof, or strip-aware optimization** — SIRA/BIRA/RLCracker/RLSpoofer are permanent red lines (#77).
2. **Never market watermark removal or EU provenance circumvention** — CoP Measure 1.2/1.5 (#76, #77).
3. **Never market Turnitin/GPTZero bypass or "100% undetectable"** — FTC + Turnitin bypasser category (#66, #78).
4. **Never facilitate AI-generated submission as original scholarship** — intent gate (#78).
5. **Never treat detector score minimization as primary product objective** — Class III obfuscation (#66).
6. **Never promise durable detector pass** — Sadasivan + monthly retraining (#66, #78).
7. **Never position as Undetectable.ai equivalent** — differentiation is honesty + preservation + refusal (#78 §7.3).
8. **Never advise watermark-before-humanize for compliance** — broken workflow (#77, #76).
9. **Always document collateral watermark/detector effects** — side effect ≠ feature (#77).
10. **Always refuse explicit strip and misconduct requests** — even if collateral rewrite would achieve similar outcome (#77 §2.2 Classes D–E).

---

## 11. Open questions (unresolved across memos)

1. **Enforcement:** Will EU authorities treat incidental mark loss during copy-editing as violation? Intent likely matters; no public cases yet (#77 §7.1).
2. **Bypasser FP on human L2 prose post-edit:** Turnitin bypasser + DetectAIve III↔IV confusion may false-flag legitimate ESL defense (#66 §7.2, #78 §11.2).
3. **`--surprisal-variance` watermark correlation:** Not benchmarked; treat as unknown until measured (#76 §9.3).
4. **Vendor liability chain:** EU user publishes unlabelled blog after anti-detector — deployer is user; tool exposure via marketing only (#76 §9.3).
5. **Authorship/Replay adoption:** Process provenance may reduce post-hoc anti-detector centrality for enrolled students (#78 §11.3).

---

## 12. Source memo map

| Memo | Primary contribution to refusals |
|------|----------------------------------|
| **#77 Watermark ethics** | Side effect vs deliberate strip; intent taxonomy; SIRA/BIRA red lines; refusal scripts |
| **#78 Integrity vs ESL** | Framing fork; four-question gate; bypass marketing traps; Newby/OCR evidence stack |
| **#66 Turnitin bypasser** | Class III mapping; score-targeting refusal; Booth attribution fix; no bypass marketing |
| **#76 EU Art. 50** | Legal floor for circumvention products; allowed/forbidden matrix; marketing exposure |

---

## 13. Bottom line

unslop's rewrite pass will always sit in the threat model for watermarks, detectors, and Turnitin's bypasser layer. That is not a bug to fix with more aggressive evasion — it is the **reason** refusals exist.

**Implement voice. Document collateral. Refuse strip modes, score targeting, and bypass marketing.** Anti-detector stays a defensive tool for human drafts detectors misread, gated on authorship and intent. Everything else is the Undetectable.ai category — and EU law, FTC precedent, and Turnitin's own framing already draw that line.

**Status:** Complete — ready for Boundaries sync, README honesty pass, and SKILL.md citation fix (Liang + Booth/Turnitin).
