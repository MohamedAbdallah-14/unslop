# SYNTH-93 — 2026 Commercial Humanizer / Detector Market Landscape

**Synthesis agent:** #93  
**Inputs:** Agent memos #56–67 (detectors: 56–60, 62, 66–67; humanizers: 61, 63–65; cross-cutting: 62, 67)  
**Prepared:** August 19, 2026  
**Status:** Market landscape + unslop positioning synthesis  
**Cross-refs:** [SYNTH-82-DETECTION-COMMERCIAL.md](./SYNTH-82-DETECTION-COMMERCIAL.md), [AGENT-67-MARKETING-VS-AUDIT.md](./AGENT-67-MARKETING-VS-AUDIT.md), [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md)

---

## Executive summary

August 2026 commercial AI-text integrity is a **two-sided arms race** between retraining detectors and subscription humanizers — with a widening **legitimacy schism** between mainstream suite vendors (Superhuman/Grammarly, Turnitin) and gray-market bypass SaaS (Undetectable.ai, Ryter Pro, Walter Writes).

**Detectors** sell clean-corpus separability ("99% accurate"). **Independent audits** test deployment reality: humanizers, paraphrase, stubs, ESL prose, mixed authorship. The marketing-vs-audit gap is typically **15–47 percentage points** — often larger than the spread between top vendors on raw AI text.

**Humanizers** sell detector-score minimization. **Independent measurement** shows no tool reliably beats Turnitin, Pangram, and Originality together after 2025–2026 retrains. Bypass rates are **tool-specific, unstable, and decay in weeks** as vendors retrain on adversary outputs.

Three structural shifts define the year:

1. **Detector humanizer arms race.** Turnitin bypasser layer (Aug 2025), GPTZero 15 model releases in 2025 + arXiv:2602.13042, Originality Turbo 3.0.2 (Sep 2025), Pangram DAMAGE-line training. Static bypass numbers are stale within weeks.

2. **Ranking inverts under stress.** Jabarian & Imas (Chicago Booth / BFI WP 2025-116): on clean medium-to-long English, Pangram leads policy-cap metrics; after StealthGPT humanization, GPTZero FNR **44–77%** while Pangram stays **0–5%**. GPTZero's Jan 2026 rebuttal re-runs clean text only — humanizer arm unaddressed.

3. **Platform consolidation + provenance pivot.** Superhuman (formerly Grammarly) acquired GPTZero (~$30M ARR, Jun 2026), shipping detection + humanization + Authorship in one bundle. Turnitin de-escalates UI certainty (unified blue, Jul 2026) while escalating model aggression. Institutions retreat from high-stakes classifiers (Curtin disabled Jan 2026) toward process provenance.

**For unslop:** The market splits into **evasion SaaS** (paste-box, built-in green checks, $5–15/mo) and **integrity suites** (Superhuman, Turnitin LMS). unslop is neither — it is an **editor-native voice polish layer** with byte-exact preservation, open source, and explicit non-bypass posture. Win on honesty, integration, ESL false-positive defense, and structural de-slop — not detector leaderboards or Authorship provenance.

---

## 1. Market map — who users actually hit

### 1.1 Detector tiers (August 2026)

| Tier | Product | Channel | 2026 posture | unslop user exposure |
|------|---------|---------|--------------|----------------------|
| **T1 — LMS default** | Turnitin | University LMS, iThenticate | Bypasser layer (Aug 2025); unified blue UI (Jul 2026); 1–19% scores suppressed as `*%` | **Highest** for coursework |
| **T1 — Consumer/education** | GPTZero (+ Superhuman Go) | Web, Chrome, LMS; acquired Jun 2026 | Deep-learning + humanizer red-team; predictability-cone generation; Writing Replay | **Highest** for direct checks |
| **T1 — Agency/publisher** | Originality.ai | SEO, enterprise, Moodle | Turbo 3.0.2 (hardest binary); **AI Allowance** (Jul 2026) for hybrid policy | Freelancers, content teams |
| **T1 — Admissions/integrity** | Pangram | API, admissions offices | Humanizer-adapted classifier; Booth policy-cap winner on clean + StealthGPT | Growing in high-stakes admissions |
| **T2 — Enterprise bundle** | Copyleaks | LMS + plagiarism fusion | V9/V10 ensemble + AI Logic (phrase heatmap, AI Source Match) | Multilingual enterprise |
| **T2 — Suite incumbent** | Grammarly/Superhuman | 40M+ DAU; Authorship in Docs | Dual detector (Grammarly + GPTZero); Humanizer framed as clarity, not bypass | Comparison anchor, not bench target |
| **T3 — Defunct / discredited** | OpenAI classifier, Content at Scale | — | Withdrawn Jul 2023; FTC 98.3% → 53.2% (Aug 2025) | FAQ confusion only |

### 1.2 Humanizer tiers (August 2026)

| Tier | Examples | Product shape | Posture | Typical Turnitin outcome [I] |
|------|----------|---------------|---------|------------------------------|
| **Gray-market bypass** | Undetectable.ai, Ryter Pro, Walter Writes | Paste-box + built-in detector panel + bypass SEO | "99% undetectable" | 38–72% flagged post-bypasser; conflicting panels |
| **Suite paraphraser** | QuillBot Humanizer, Grammarly Humanizer | Writing suite feature; clarity framing | No numeric bypass claim | ~25–47% bypass; paraphrase overlay risk |
| **Affiliate-reviewed** | WriteHuman, GPTHuman, Aceessay (Alammyan corpus) | Same paste-box shape; SEO reviews | Bypass headlines + 2026 meaning-first pivot | Single-sample; Pangram often catches |
| **Not a humanizer** | **unslop** | Editor skill + optional Python pipeline | Voice polish; ESL defense | No bypass claim; ~0.0–0.2 pp TMR deterministic |

### 1.3 Corporate consolidation — Superhuman platform (Agent #63)

The clearest consolidation event of 2026:

| Date | Event |
|------|-------|
| Jan 2025 | Grammarly acquires Coda |
| Jul 2025 | Grammarly acquires Superhuman Mail |
| Oct 2025 | Company rebrand to **Superhuman**; Superhuman Go launch |
| Jun 2026 | Superhuman acquires **GPTZero** (~$30M ARR, 19M users) |
| Mar 2026 | Authorship default-on in Docs; agent-specific attribution |

**Combined stack:** Grammarly writing + Superhuman Docs + Mail + Go + **dual detectors** (Grammarly RAID #1 claim + GPTZero) + Authorship + Replay + AI Vision.

**Strategic bet:** Process transparency where possible, classifier ensemble where not — same tension as Turnitin (Clarity drafts, Authorship keystrokes) while de-emphasizing UI certainty.

**Naming trap:** "Superhuman" = company (formerly Grammarly Inc.), Superhuman Mail (email app), Superhuman Go (cross-app assistant), and GPTZero (standalone brand). Do not conflate in docs.

---

## 2. Detector landscape — condensed findings

### 2.1 Evasion difficulty ranking (practitioner consensus)

```
Originality Turbo 3.0.2  ≳  GPTZero (2026)  ≳  Turnitin (post-bypasser)  ≳  Copyleaks  ≫  free tools
```

**Paraphrase/humanized axis diverges from clean-text ranking:**

| Detector | Clean English (Booth-class) | Humanized / StealthGPT | Notes |
|----------|----------------------------|------------------------|-------|
| Pangram | Policy-cap leader | **Robust** (FNR ~0–5%) | Booth + DAMAGE; best independent humanizer story |
| GPTZero | Strong; #1 disputed on API field | **Fragile** (FNR 44–77% Booth) | 2026 retrain may narrow — not replicated on 19-tool pool |
| Originality Turbo | 81.3% recall Booth clean | Moderate; aidetector.ac −24 pp humanized | Hardest single commercial check on raw SaaS humanizer output |
| Turnitin | Not in Booth | Blommerde 0–72% by tool; vendor metrics unpublished | Institutional default despite retreat wave |
| Copyleaks V9/V10 | ~90.7% adjacent studies | 40–71% post-humanization; sometimes better than GPTZero on paraphrase | Weaker clean recall; stronger on some edited-AI studies |
| Grammarly/Superhuman | RAID #1 claim (clean) | HumanizerBench **0% bypass**; Pangram 0/9 on panel | L1 paraphraser class; not Turnitin-tested in Booth |

**Critical rule:** A green **GPTZero** after paraphrase is **not** a green **Pangram** or **Turnitin**. Dual reporting required.

### 2.2 Turnitin bypasser category (Agents #56, #66)

Turnitin's **bypasser detection** (Aug 27, 2025) = academic **LLM-DetectAIve Class III** (machine-written → machine-humanized). Integrated into "AI-generated only"; English only; **no published bypasser recall or FPR**.

| Layer | Turnitin label (pre-Jul 2026) | Target |
|-------|--------------------------------|--------|
| Raw LLM | "AI-generated only" (blue) | Class II |
| Paraphrase / spinner | "AI-paraphrased" (purple, until Jul 2026) | QuillBot-class |
| **Bypasser / humanizer** | Merged into "AI-generated only" | StealthGPT-class |

**Jul 2026:** Single blue highlight for all AI signal — detection logic unchanged; UI de-escalates certainty.

**Blommerde (Sept 2025, best public test):** StealthGPT 0%→72%, Groby 0%→67%, Easy Essay still 0%. Pattern = signature detection on trained tools, not universal bypass-proof.

**Attribution fix:** Booth **did not test Turnitin**. Remove "Turnitin 60–85% at Booth" from SKILL.md.

### 2.3 Chicago Booth — independent anchor (Agent #62)

"Chicago Booth 2026" = **Jabarian & Imas (Aug 2025)** + **GPTZero clean-text rebuttal (Jan 2026)** — not a separate study.

| Finding | Detail |
|---------|--------|
| Clean text | Commercial detectors work; Pangram only strict FPR-cap (≤0.5%) winner |
| StealthGPT arm | **Ranking inverts** — Pangram FNR ~0–5%; GPTZero FNR **44–77%** |
| Humanizers tested | **One** (StealthGPT) — not twelve |
| Not tested | Turnitin, Copyleaks, Grammarly, unslop, ESL stratification |

**Misattributions to fix in unslop docs:**

| Wrong claim | Reality |
|-------------|---------|
| "Booth twelve humanizers" | Booth = 1; twelve = HumanizerBench |
| "~6 points median accuracy drop" | Not in Jabarian & Imas |
| "Turnitin 60–85% at Booth" | Turnitin not evaluated |

### 2.4 Marketing vs audit gap (Agent #67)

| Claim type | Marketing condition | Audit condition | Typical gap |
|------------|--------------------|-----------------|-------------|
| Overall accuracy | Raw AI, long English | Humanized, mixed, stubs | 15–47 pp |
| False-positive rate | Native English | ESL TOEFL, short form | 0.5% claimed → 5–61% measured |
| Humanizer resistance | Vendor-retrained model | DAMAGE 19-tool, Booth StealthGPT | GPTZero 99.7% → 60% TPR |
| Regulatory | 98.3% (Content at Scale) | FTC retest | **53.2%** non-academic |

**Citation rule for unslop docs:**

```
[Detector] [Model/version + date] · [Corpus] · [Arm: clean | humanizer | ESL] · [Metric] · [Tier: I | II | III | IV | V]
```

Never repeat vendor "99%" without arm qualification.

---

## 3. Humanizer landscape — condensed findings

### 3.1 Three product classes users conflate

| Class | Examples | DAMAGE tier | Pangram catch (Aug 2025) | Fluency |
|-------|----------|-------------|---------------------------|---------|
| **Gray-market bypass** | Undetectable.ai | **L3** (error injection) | **90.3%** — best evader, still ~9/10 fail | Elementary-school output |
| **Budget bypass** | Ryter Pro, Walter Writes | Not in DAMAGE | No Pangram row | Conflicting Turnitin tests |
| **Suite paraphraser** | QuillBot, Grammarly Humanizer | **L1** (synonym swap) | **100%** on L1 paraphrasers | High fluency; *more* detectable |
| **Editor polish** | **unslop** | N/A (subtractive) | Not benchmarked | Preservation contract |

**Key insight (DAMAGE):** Fluent L1 rewrites are **more detectable** than garbled L3 output once detectors retrain on humanizer corpora. Evasion and readability **decouple**.

### 3.2 Gray-market trio — Undetectable / Ryter / Walter (Agent #61)

| Tool | Vendor claim | Independent reality | Built-in panel |
|------|--------------|---------------------|----------------|
| **Undetectable.ai** | 99.8% undetectable | Pangram **90.3%** caught; Turnitin **54–67% bypass** [I]; no clean public Turnitin test | Omits Turnitin; all-green theater |
| **Ryter Pro** | 99.9% / 94% Turnitin | AuraWrite: **42% AI remaining** on Turnitin; conflicts with vendor SEO | Not in Booth/DAMAGE/Pangram tables |
| **Walter Writes** | Beats Aug 2025 bypasser | Pre-update **79.7% bypass** [A]; post-update **~38% flagged** [I]; Trustpilot ~2.4/5 | Internal 100% vs external fail |

**Ecosystem pattern:** Built-in detector panels optimize for **weak detectors and curated samples**. Pangram (DAMAGE authors) and Turnitin (bypasser-trained) represent the **2026 ceiling**.

**Ryter Pro misattribution:** Several unslop internal docs cite "Alammyan 2026" for Ryter Pro bypass rates — **her published 14-tool list does not include Ryter Pro** (Agent #65). Source is vendor SEO [V], not Alammyan [I].

### 3.3 QuillBot — suite humanizer (Agent #64)

Dominant mainstream paraphraser (~30M+ monthly visits). Humanizer tab (late 2025) = **synonym-substitution with a humanizer skin**.

| Metric | Result |
|--------|--------|
| Turnitin bypass [I] | **25–47%** — coin flip |
| Epaphras 2026 ADR | **93.56%** detected (15/18 iterations) |
| DAMAGE tier | **L1** — Pangram **100%** catch |
| Turnitin-specific failure | **Paraphrase overlay** — "AI-generated with paraphrasing tool modification" even when AI % looks borderline |
| Scribbr detector | **Same engine** as QuillBot — vertical integration theater |

QuillBot official pages **avoid numeric bypass claims** — deliberate legitimacy positioning. Users still hire it for Turnitin workarounds; 2026 consensus: **paraphrasing alone no longer works** for most academic prose.

### 3.4 Grammarly/Superhuman Humanizer (Agent #63)

**Positioning:** "Editor with emotional intelligence" — explicitly **not** detector bypass. Landing page directs users to transparency features (Authorship).

| Audit | Result |
|-------|--------|
| DAMAGE | **L1** paraphraser — high fluency, faith preserved |
| HumanizerBench | **0.0% bypass** (100% detected) |
| Pangram panel (Fast.io 2026) | Superhuman detector **0/9** caught where GPTZero got **7/9** |
| Chicago Booth | Not tested |

**Brittany Carr case:** Student dropped out chasing Grammarly detector scores on **her own** writing — canonical false-positive + humanizer loop. Superhuman's response: Authorship + conservative detector + rewrite agents = empowerment **within their ecosystem**.

**Conflict of interest:** Same subscription sells detector + humanizer + generative agents. Structurally identical to Undetectable.ai's vertical integration — but Superhuman discloses limits and pushes provenance instead of "100% human guaranteed."

### 3.5 Practitioner review layer — Alammyan (Agent #65)

Most-cited affiliate-layer reviewer (30+ tools screened, 14 retained). **Useful as [I] anecdote, not benchmark SSOT.**

**Strongest protocol (Jul 2026, n=1):** Same ChatGPT article through 4 tools × Pangram + Quetext:

| Tool | Pangram | Quetext |
|------|---------|---------|
| WriteHuman | 100% human | 96% human |
| GPTHuman | 100% AI | 80% human |
| Undetectable (free) | 100% AI | 72% AI |
| HumaLingo | 100% AI | 99% AI |

**2026 pivot:** Meaning-first framework — "detector scores stopped mattering." Aligns with unslop subtractive thesis; bypass SEO titles remain for ranking.

**Do not cite Alammyan for:** Ryter Pro, Walter Writes, aggregate "67–89% real bypass" (that's Detection Drama synthesis).

---

## 4. Arms race dynamics

### 4.1 Retrain cadence (2025–2026)

| Date | Vendor | Change | Humanizer impact |
|------|--------|--------|------------------|
| Aug 27, 2025 | Turnitin | Bypasser detection integrated | StealthGPT-class bypass rates collapse |
| Sep 2025 | Originality | Turbo 3.0.2 / Lite 1.0.2 humanizer retrain | Pre-Sep bypass stats stale |
| Jan 2026 | GPTZero | arXiv:2602.13042; "v6" generation | Synonym swap insufficient |
| Feb 12, 2026 | Turnitin | English recall bump | Resubmit required; magnitude unpublished |
| Jul 2026 | Originality | AI Allowance (0–40% thresholds) | Same text, opposite verdict by threshold |
| Jul 20, 2026 | Turnitin | Unified blue highlight | UI only; logic unchanged |
| Jun 2026 | Superhuman | Acquires GPTZero | Dual-detector + Authorship bundle |

**Pattern:** Monthly-ish retraining against humanizer corpora. Any single-score optimization decays in weeks.

### 4.2 What breaks vs what survives

| Attack | vs legacy detectors | vs 2026 adapted (Pangram, Turbo, bypasser Turnitin) |
|--------|--------------------|-------------------------------------------------------|
| Synonym swap / QuillBot L1 | Often sufficient (GPTZero pre-retrain) | **Caught** — explicit training target |
| Same-model LLM humanize (StealthGPT) | 0% Turnitin pre-Aug 2025 | **72% flagged** post-bypasser |
| Cross-model second pass (Claude↔GPT↔Gemini) | Strongest user lever | **Least represented in training** — unslop documents this |
| unslop deterministic pass | ~0.0–0.2 pp TMR | Lexical cleanup necessary but insufficient |
| Manual edit after any humanizer | All vendors concede evades | True human rewrite |
| Process provenance (Authorship, Replay) | Irrelevant to classifier | **Endgame** — post-hoc humanization insufficient |

### 4.3 Endgame shift — provenance beats classification

| Era | Institutional question |
|-----|------------------------|
| 2023–2024 | "What % AI is this document?" |
| 2025–2026 | "Show me how this document was made." |

Superhuman Authorship (5M+ students, default-on Mar 2026) + GPTZero Replay + Turnitin Clarity drafts = **process verification stack**. Classifier evasion is a narrowing window. unslop is **out of scope for provenance** — document honestly.

---

## 5. Legitimacy schism — two humanizer markets

```
                    LEGITIMATE                           GRAY-MARKET
                    ──────────                           ───────────
Posture             Clarity, voice, transparency          Bypass metrics, SEO
Examples            Grammarly Humanizer, QuillBot       Undetectable, Ryter, Walter
Detector bundled    Yes — disclosed conflict            Yes — omits Turnitin
Marketing           "Sound human" / Authorship          "99.8% undetectable"
DAMAGE tier         L1 (100% detected when adapted)     L3 (90% caught, unreadable)
Regulatory posture  EU AI Act durable                   Bypass vendors at risk
unslop alignment    Same anti-bypass ethics             Opposite — never compete here
```

**Superhuman** is the **respectable incumbent** unslop users get compared against: same audience (students, knowledge workers), opposite architecture (cloud suite vs editor plugin).

**Undetectable/Ryter/Walter** are the **visible commercial layer** users search for by brand when asking "which humanizer beats Turnitin" — route them away from bypass promises toward honest voice work.

---

## 6. unslop positioning

### 6.1 What unslop is not

| Market promise | unslop response |
|----------------|-----------------|
| "99.8% undetectable" | Documented ~0.0–0.2 pp TMR on deterministic pass; no bypass guarantee |
| Paste-box cloud rewrite | In-editor skill + optional Python pipeline |
| Built-in detector loop | Optional `--detector-feedback`; TMR is signal not gate |
| L3 error injection | Subtractive de-slop; byte-exact preservation |
| Authorship / provenance | Out of scope — different product category |
| $5–15/mo credit roulette | Free/open-source plugin + PyPI |

### 6.2 Competitive matrix (August 2026)

| Dimension | Superhuman | QuillBot | Undetectable | **unslop** |
|-----------|------------|----------|--------------|------------|
| **Primary goal** | Integrity suite + clarity | Suite paraphrase | Detector evasion | Editorial voice |
| **Detection** | Dual (Grammarly + GPTZero) | Bundled (weak on bypassers) | Built-in theater | None (optional TMR) |
| **Humanization** | L1 Humanizer agent | L1 Humanizer tab | L3 black-box | Subtractive regex + LLM |
| **Turnitin honest expectation** | Not Booth-tested; 0% HumanizerBench | ~25–47% bypass [I] | Low–moderate; conflicting | **None claimed** |
| **Preservation** | Holistic rewrite | Breaks citations often | Breaks code/citations | **Byte-exact contract** |
| **ESL defense narrative** | Authorship + conservative detector | Incidental | None | **Explicit anti-detector mode** |
| **Price** | ~$12+/mo suite | ~$8/mo | ~$5+/mo | **Free** |
| **Open source** | No | No | No | **Yes** |

### 6.3 Where unslop wins

| Wedge | Why it holds |
|-------|--------------|
| **Editor-native, zero context switch** | Superhuman/QuillBot require extension or paste-box; unslop lives in Cursor/Claude/Codex |
| **Byte-exact preservation** | Code, URLs, headings, tables protected — suite tools rewrite holistically |
| **Transparent non-bypass posture** | Credible to mainstream press; no "beat Turnitin" marketing |
| **Defensive ESL / false-positive narrative** | Liang 2023 + Working Educators; Superhuman owns detector side of same problem |
| **Open, auditable deterministic passes** | Regex + optional local DivEye; no black-box subscription |
| **Anti-slop without warmth injection** | Superhuman Humanizer adds "warmth" — same RLHF gradient unslop avoids |
| **Developer/agent output focus** | Superhuman optimizes email/essays; unslop optimizes agent markdown and codebase docs |
| **Cross-model second pass documentation** | Strongest practitioner lever against 2026 detectors — unslop recommends, doesn't sell |

### 6.4 Where unslop loses (document honestly)

| Gap | Response |
|-----|----------|
| 40M-user distribution | Stay plugin/open-source; no GTM arms race |
| Dual-detector ensemble | Don't claim detector bypass; cite independent audits |
| Authorship / Replay provenance | "When institutions require Authorship, unslop can't help — and shouldn't pretend to." |
| Custom voice from 200-word samples | `voice-match` + stylometry is lighter-weight; different job |
| RAID-marketed detector depth | Not unslop's category |

### 6.5 Recommended messaging (August 2026)

> **Detectors** retrain monthly on humanizer outputs. Vendor "99%" numbers describe raw English under vendor-friendly conditions. Independent audits show **15–47 pp drops** after paraphrase, and **detector-specific** outcomes — GPTZero greens after StealthGPT do not imply Pangram or Turnitin pass.
>
> **Humanizers** (Undetectable.ai, Ryter Pro, Walter Writes) trade readability for lower scores on **some** panels. None reliably beat Turnitin, Pangram, and Originality together after 2025–2026 retrains. **QuillBot** and **Grammarly Humanizer** are legitimate paraphrasers (DAMAGE L1) — not bypass tools; Turnitin explicitly names QuillBot-class spinners.
>
> **unslop** removes AI-isms and restores human rhythm in your editor — stock phrases, uniform sentence length, zero contractions, performative balance. That is voice work. The same edits reduce false positives for ESL writers. It is not a Turnitin guarantee.
>
> **Anti-detector mode** exists for **false-positive defense** and **register restoration** — not academic misconduct. Maximum fingerprint separation: **cross-model second pass** after unslop (Claude ↔ GPT ↔ Gemini), then manual edit. Never trust a built-in green check.

### 6.6 DetectAIve-aware framing (Turnitin bypasser = Class III)

When unslop runs `anti-detector` on **AI-origin** text, output targets **Class III** (M→MH) — the category Turnitin's bypasser layer and DetectAIve target.

When unslop runs on **human-origin** text (ESL false-positive defense), target stays **Class I** or at most **Class IV** — prefer `voice-match` + `subtle` over heavy LLM rewrite on human drafts.

---

## 7. User routing — decision tree

```
Graded coursework / Turnitin submission?
  → No honest bypass recommendation
  → Process-based authorship (drafts, Authorship) > post-hoc scores
  → unslop for voice polish only; not evasion

ESL writer / resume falsely flagged?
  → /unslop anti-detector (+ manual fact check)
  → Cite Liang; do not chase detector scores in a loop

Sounds like ChatGPT but isn't trying to cheat?
  → /unslop balanced or full

Already paying for QuillBot/Grammarly for grammar?
  → Keep suite for grammar; use unslop in IDE for agent output
  → Do not chain QuillBot humanizer expecting Turnitin clearance

Arriving from "which humanizer beats Turnitin" SEO?
  → Name Undetectable/Ryter/Walter honestly: conflicting numbers, built-in panel theater
  → Route to: subtract AI-isms → cross-model pass → manual edit
  → Never trust built-in green checks

Need maximum separation from LLM fingerprints?
  → unslop full/anti-detector → cross-model second pass → manual edit
  → NOT single-pass SaaS humanizer ($8–15/mo credit roulette)
```

---

## 8. Documentation corrections (P0)

Cross-agent attribution fixes consolidated:

| Location | Wrong claim | Fix |
|----------|-------------|-----|
| SKILL.md | "Turnitin 60–85% at Chicago Booth" | Booth didn't test Turnitin; cite Blommerde [I] |
| README | "Twelve humanizer services" at Booth | Booth = StealthGPT only; twelve = HumanizerBench |
| README | "~6 points median accuracy drop" | Not in Jabarian & Imas; remove or source |
| E-practical / Cat 18 | "Ryter Pro — Alammyan 2026" | Misattributed; vendor SEO [V] |
| Bench protocol | Single detector pass = success | Dual-report: GPTZero + Pangram + Turnitin where applicable |
| Any vendor "99%" | Unqualified | Add arm + metric + model date + tier |

### Bench protocol additions

Log for every commercial scan:

```csv
detector,model_version,scan_date,mode,text_id,variant,score,verdict,screenshot
originality,Turbo 3.0.2,2026-08-19,binary,01-flutter,unslop-full,87,Likely AI,...
originality,AI Allowance 15%,2026-08-19,threshold,01-flutter,unslop-full,12,Likely Original,...
gptzero,2025-12-18-base,2026-08-19,predicted_class,01-flutter,unslop-full,Mixed,,...
```

Minimum Tier 1 detectors for article credibility: **GPTZero** (`predicted_class`), **Originality Turbo 3.0.2**, **Pangram**, optional **Turnitin** (note model date + resubmit requirement).

---

## 9. Five-signal stack vs commercial detectors

| Signal | unslop coverage | Detector sensitivity (2026) |
|--------|-----------------|------------------------------|
| Lexical AI-isms | ✅ `humanize.py` | Caught; insufficient alone |
| Burstiness / sentence-length σ | ⚠️ `structural.py` | High — all major vendors train on this |
| Surprisal variance (DivEye) | ⚠️ measure-only `surprisal.py` | Orthogonal; classifiers absorb LM-surprisal proxies |
| Late-stage stability (TSD) | ❌ planned | Unknown public detail |
| Predictability cones (GPTZero v6) | ❌ | Synonym swap insufficient |

**TMR loop (`detector.py`)** optimizes GPTZero-family signal — **not** Pangram, Turnitin, or Originality. TMR green ≠ commercial green. Web bench is external validator.

---

## 10. Open questions (Q3 2026)

1. Independent third-party re-run of Booth StealthGPT arm with GPTZero `predicted_class` on 2026 model — does FNR ~50%+ persist?
2. Turnitin bypasser training set — vendor silent; Easy Essay 0% suggests incomplete coverage.
3. unslop fixtures vs live Copyleaks API (Extra Sensitive mode) — CSV rows empty.
4. Premium Undetectable Stealth vs Pangram — Alammyan explicitly untested.
5. Superhuman Go agent SDK — third-party voice plugin signals?
6. AI Allowance on Originality free tier — model picker availability?
7. Peer-review status of NBER w34223 (still working paper Aug 2026).

---

## 11. Bottom line

The 2026 commercial landscape is **not a leaderboard** — it is an arms race between retraining detectors and subscription humanizers, with a **legitimacy schism** splitting mainstream integrity suites from gray-market bypass SaaS, and a **provenance pivot** that may make post-hoc classifier evasion secondary to creation logs.

**Detectors:** Pangram leads independent clean + StealthGPT tests; Originality Turbo is hardest single commercial check on SaaS humanizer output; GPTZero is most-installed but paraphrase-fragile in Booth/DAMAGE; Turnitin is institutional default with unpublished bypasser metrics; Copyleaks is enterprise screening not integrity-grade alone.

**Humanizers:** No commercial tool reliably beats adapted detectors together. Gray-market vendors (Undetectable, Ryter, Walter) sell detector theater. Suite tools (QuillBot, Grammarly) sell clarity with L1 paraphrase mechanics Turnitin names explicitly. Affiliate reviews (Alammyan) are useful anecdotes, not benchmarks.

**unslop:** Editor-native voice polish with preservation, open source, and honest non-bypass positioning. Win the polish layer. Document everything else — Authorship, dual detectors, bypass SaaS — as someone else's product. Anti-detector mode stays **ESL false-positive defense and register restoration**, not Turnitin bypass.

---

## 12. Source index (agent memos)

| Agent | Topic |
|-------|-------|
| [#56](./AGENT-56-TURNITIN-2025-2026.md) | Turnitin 2025–2026 product timeline |
| [#57](./AGENT-57-GPTZERO-EVOLUTION.md) | GPTZero evolution + Superhuman acquisition |
| [#58](./AGENT-58-ORIGINALITY-AI-ALLOWANCE.md) | Originality Turbo 3.0.2 + AI Allowance |
| [#59](./AGENT-59-COPYLEAKS-V9.md) | Copyleaks V9 ensemble |
| [#60](./AGENT-60-PANGRAM-VS-GPTZERO-PARAPHRASE.md) | Pangram vs GPTZero paraphrase divergence |
| [#61](./AGENT-61-UNDETECTABLE-RYTER-WALTER.md) | Gray-market humanizer trio |
| [#62](./AGENT-62-CHICAGO-BOOTH-2026.md) | Chicago Booth independent audit |
| [#63](./AGENT-63-GRAMMARLY-SUPERHUMAN.md) | Superhuman platform consolidation |
| [#64](./AGENT-64-QUILLBOT-HUMANIZER.md) | QuillBot suite humanizer |
| [#65](./AGENT-65-ALAMMYAN-HUMANIZER-REVIEW.md) | Practitioner review layer |
| [#66](./AGENT-66-TURNITIN-BYPASSER-DETECTION.md) | Bypasser category + DetectAIve Class III |
| [#67](./AGENT-67-MARKETING-VS-AUDIT.md) | Marketing vs independent audit gap |

---

*SYNTH-93 complete. Feeds UPDATE-PLAN-2026-08 landscape refresh, SKILL.md commercial paragraph, README honesty pass, and `drafts/2026-05-detector-test/` protocol.*
