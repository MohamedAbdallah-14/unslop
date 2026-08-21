# SYNTH-88 — Practitioner Evasion Tools & Techniques (August 2026)

**Synthesis agent:** #88  
**Category:** Cat Evasion — tools quadrant (manifest agents 85–88)  
**Inputs:** Evasion memos (#21 MASH, #25/#39 Adversarial Paraphrasing, #35 cross-model, #38 TempParaphraser, #40 DAMAGE tiers) + commercial memos #61–65 (Undetectable/Ryter/Walter, Chicago Booth, Grammarly/Superhuman, QuillBot, Alammyan)  
**Prepared:** August 19, 2026  
**Cross-refs:** [SYNTH-81-DETECTION-ACADEMIC.md](./SYNTH-81-DETECTION-ACADEMIC.md), [SYNTH-82-DETECTION-COMMERCIAL.md](./SYNTH-82-DETECTION-COMMERCIAL.md), [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md)

---

## Executive summary

Practitioners who want lower AI-detector scores in 2026 use a **stacked toolkit**, not one product. The dominant pattern is:

```
Generate (Model A) → rewrite (Model B, different family) → optional SaaS humanizer → manual fact-check → re-score
```

Academic work licenses this: TempParaphraser (−82.5% avg detector accuracy), Adversarial Paraphrasing (−87.88% avg T@1%F), HIP (base-model paraphrase beats instruct fingerprints on commercial detectors). DAMAGE audited **19 commercial humanizers** and found **20–100 point spread** on the same input — opaque SaaS is a lottery, not a protocol.

Commercial paste-box tools (**Undetectable.ai**, **Ryter Pro**, **Walter Writes**) optimize detector-score minimization, often at **L3 fluency** (DAMAGE) while adapted detectors still catch **~90%+** (Pangram on Undetectable). **QuillBot** is the mainstream suite humanizer — **L1 synonym tier**, **25–47% Turnitin bypass**, often triggers **paraphrase-tool overlay** even when AI % looks borderline. **Grammarly/Superhuman** ships detection + humanization + **Authorship provenance** — the 2026 endgame is process transparency, not classifier evasion.

**unslop split:**

| Action | What |
|--------|------|
| **Document** | Cross-model workflow, commercial tool honest comparison, dual-detector reporting, DAMAGE L1/L2/L3, ladder exhaustion message, Alammyan n=1 caveats, Ryter Pro misattribution fix |
| **Integrate (Phase 1–2)** | `anti-detector` in feedback ladder, surprisal/TSD logging, stylometric baseline, TempParaphraser-style multi-candidate **selection loop** via existing TMR |
| **Integrate (Phase 3, optional)** | Cross-model prompt templates, MASH Stage-4 sentence polish with detector gate |
| **Refuse** | SaaS humanizer API wrappers, watermark removal, Turnitin bypass marketing, vendoring TempParaphraser weights (license) |

Anti-detector mode stays **ESL false-positive defense and register restoration** — not "cheaper Undetectable.ai."

---

## 1. Practitioner technique taxonomy

### 1.1 Tier map — what users actually run

| Tier | Technique | Examples | Signal layer targeted | Evidence tier |
|------|-----------|----------|----------------------|---------------|
| **T0 — Lexical strip** | Regex / stock-vocab removal | unslop `balanced`/`full`, blader skill | Signal 1 (AI-isms) | unslop fixtures ~0.0–0.2 pp TMR |
| **T1 — Suite paraphrase** | Synonym swap, fluency modes | QuillBot Standard/Creative, Grammarly paraphraser | Signal 1–2; fails Signals 3–5 | DAMAGE **L1**; Epaphras 93.56% ADR on QuillBot |
| **T2 — Dedicated humanizer** | Black-box multi-pass LLM + error injection | Undetectable.ai, Ryter Pro, Walter Writes, WriteHuman | Distribution shift (partial) | DAMAGE L3 (Undetectable); Pangram 90.3% catch |
| **T3 — Cross-model chain** | GPT → Claude → Gemini (2–3 hops) | Manual practitioner workflow | Instruction-tuning fingerprint, logits geometry | Agent #35; HIP 96.7–98.8% human on base vs 17–30% instruct |
| **T4 — Detector-guided rewrite** | Regenerate until green; token-level beam | AdvPara repo; TempParaphraser; Undetectable "detection-informed" marketing | Full stack when guided | AdvPara −87.88% avg; TempParaphraser −82.5% |
| **T5 — Trained humanizer** | SFT/DPO/RL on detector reward | MASH, StealthRL, StyleShield | Style transfer + distribution | MASH 92% ASR; not practitioner-accessible without GPU/training |

**Practitioner consensus (forums, Alammyan, Detection Drama):** T3 beats T2 on semantics control; T2 beats T1 on consumer detector screenshots; **none** reliably clears Turnitin + Pangram + Originality together post–Aug 2025 bypasser retrain.

### 1.2 Canonical cross-model workflow (Agent #35)

| Step | Action | Why |
|------|--------|-----|
| 0 | Draft with Model A (GPT/Claude) | Carries family A instruction-tuning artifacts |
| 1 | Rewrite with Model B (**different family**) | Breaks tokenizer + RLHF priors of A |
| 2 (opt.) | Model C pass | Diminishing returns; meaning drift dominates after 2–3 |
| 3 | Manual restore numbers, names, citations | Each hop corrupts facts |
| 4 (opt.) | unslop anti-detector locally | Burstiness, contractions after structural rewrite |
| 5 | Re-score on **target detector(s)** | One green ≠ universal pass |

**Family boundaries:** OpenAI ↔ Anthropic ↔ Google ↔ Meta. Same-family polish (GPT→GPT) preserves perplexity curvature — what Binoculars, DivEye, GPTZero v6 cones read.

**Prompt template (document in SKILL):** *"Rewrite for clarity. Preserve all facts, numbers, names, citations verbatim. Vary sentence length and structure. No filler."*

### 1.3 Manual detector-guided approximation

Practitioners without AdvPara/TempParaphraser approximate T4 by:

1. Paste into GPTZero / Originality / built-in panel
2. Regenerate humanizer output until score drops
3. Paragraph-level passes (Walter **Enhanced** workflow — TestedByHuman n=1)

This is blind Adversarial Paraphrasing — no token-level beam, but same intent. **WriteHuman** passed Pangram + Quetext on Alammyan's single-sample protocol [I]; Pangram's Aug 2025 table still catches many humanizers at 90%+ — treat WriteHuman as **anecdote**, not benchmark.

---

## 2. Commercial tools practitioners use

### 2.1 Dedicated bypass SaaS (Agent #61)

| Tool | Price floor | DAMAGE tier | Pangram catch | Turnitin [I] | Built-in panel honesty |
|------|-------------|-------------|---------------|--------------|------------------------|
| **Undetectable.ai** | ~$5/mo annual | **L3** (worst fluency) | **90.3%** caught | 54–67% bypass; no conflict-free public test | Omits Turnitin; all-green while Turnitin flags |
| **Ryter Pro** | ~$6/mo annual | Not in Table 9 | No public row | **42% AI remaining** (AuraWrite) vs vendor 94% bypass [V] | 99.9% claim uncited; no refunds |
| **Walter Writes** | ~$8/mo annual | Not in Table 9 | No public row | 79.7% bypass pre-update vs **38% flagged** post–Aug 2025 | Internal 100% vs external fail; Trustpilot ~2.4/5 |

**Shared product shape:** paste box → black-box rewrite → built-in multi-detector panel → submit to LMS. **Conflict of interest:** every vendor sells detector + humanizer.

**Practitioner debate:**

- Built-in green checks lie — verify externally (Alammyan, Detection Drama, Agent #61).
- Turnitin ≠ GPTZero — optimize one, fail the other routinely.
- Paragraph + Enhanced beats bulk paste — manual labor ads omit.
- Cross-model beats single-pass SaaS (forums; aligns with Agent #35).

### 2.2 QuillBot — suite humanizer (Agent #64)

| Dimension | Measurement | Source |
|-----------|-------------|--------|
| Mechanism | L1 synonym substitution; sentence skeleton preserved | DAMAGE; HumanizeMyAI |
| Turnitin bypass | **25–47%** (coin flip) | Supwriter, HumanizeMyAI, AI Busted |
| Peer-reviewed fail rate | **93.56% ADR** (15/18 iterations) | Epaphras & Mtenzi 2026 |
| Turnitin failure mode | **Paraphrase-tool overlay** — "AI-generated with paraphrasing tool modification" | Turnitin docs Jul 2024; Aug 2025 bypasser |
| Self-test collapse | Humanizer output **92–96% AI** on QuillBot detector post–May 2026 refresh | HumanizeMyAI |
| Scribbr detector | **Same Learneo engine** — not independent verification | GPTZero review; Agent #64 |

**User routing:** QuillBot for grammar/plagiarism/paraphrase polish — **not** bypass. Reddit still recommends "try QuillBot first" as free step; 2026 consensus: insufficient alone post-bypasser.

**vs dedicated humanizers:** Strictly **weaker on evasion**, stronger on mainstream trust. Users comparing "which humanizer beats Turnitin" often start here because it's already installed.

### 2.3 Grammarly / Superhuman stack (Agent #63)

Not a bypass tool — **legitimate incumbent** unslop users get compared against:

| Layer | Product | Evasion relevance |
|-------|---------|-------------------|
| Humanizer | Grammarly AI Humanizer | DAMAGE **L1**; HumanizerBench **0% bypass** |
| Detector | Grammarly + **GPTZero** (acquired Jun 2026) | RAID #1 on raw text; weak on paraphrase (Pangram 0/9 vs GPTZero 7/9 panel) |
| Provenance | **Authorship** in Docs (5M+ students, default-on Mar 2026) | Shifts integrity from post-hoc score to creation log |

**Market implication:** Classifier evasion window narrows; **process transparency** is Superhuman's 2026–2027 bet. unslop does not compete on Authorship capture.

### 2.4 Independent reviewer layer (Agent #65 — Alammyan)

| Safe to cite | Do not cite |
|--------------|-------------|
| WriteHuman 100% human Pangram + 96% Quetext (Jul 2026, n=1) | Ryter Pro 97% GPTZero / 94% Turnitin — **misattributed** in E-practical §20 |
| GPTHuman fails Pangram, passes Quetext — dual-detector split | "67–89% real bypass" — Detection Drama synthesis, not her table |
| Undetectable free tier 100% AI on Pangram | Turnitin ground truth — Aceessay claims only |
| Meaning-first framework (Feb 2026 pivot) | Aggregate "Alammyan says X bypasses" without protocol |

**Credibility tier:** **[I] anecdote** with screenshots — not reproducible benchmark. Her Feb 2026 "detector scores stopped mattering" aligns with unslop subtractive thesis; SEO titles still say "bypass."

### 2.5 Chicago Booth context (Agent #62)

Jabarian & Imas (BFI WP 2025-116) tested **one humanizer (StealthGPT)**, not twelve. Key practitioner lesson:

- **Clean text:** Pangram, GPTZero, Originality all work; ranking disputed after GPTZero Jan 2026 rebuttal.
- **StealthGPT stress:** Pangram FNR **0–5%**; GPTZero FNR **44–77%** — ranking **inverts**.
- **Do not cite Booth for multi-humanizer bypass rates** — use DAMAGE or HumanizerBench.

Median "~6 pp humanizer drop" in some unslop docs **does not appear in Booth** — likely HumanizerBench conflation. Fix in landscape refresh.

---

## 3. Academic tools practitioners approximate (not SaaS)

| Paper / repo | What practitioners copy | unslop can ship? | License / compute |
|--------------|-------------------------|------------------|-------------------|
| **TempParaphraser** (EMNLP 2025) | Multi-candidate sentence pick by detector score | **Selection loop yes**; vendored model **no** | Academic-only; vLLM + LLaMA-Factory fragile |
| **Adversarial Paraphrasing** (NeurIPS 2025) | Regenerate-until-green manual loop | **Document only**; token beam **no** | Apache 2.0 repo; 2× GPU, research framing |
| **DIPPER** (NeurIPS 2023) | Specialized 11B paraphraser | Optional HF integration Phase 3 | Open weights; hosting cost |
| **MASH** (ACL 2026) | Multi-stage polish + detector gate | Prompt analog Stage 4 only | Training pipeline out of scope |
| **HIP** (2026) | Base-model iterative paraphrase | Cross-model doc cites mechanism | Fine-tune required for full HIP |

**Critical AdvPara lesson for docs:** Naive paraphrase **increases** detection on RADAR (+8.57%) and Fast-DetectGPT (+15.03%). Synonym swap is not neutral — it can **worsen** scores. unslop's structural passes exist partly to avoid this regression after lexical scrub.

---

## 4. What unslop should **document** vs **integrate**

### 4.1 Document only (P0 — no code dependency)

| Topic | Content | Target file | Source memos |
|-------|---------|-------------|--------------|
| **Cross-model capstone** | GPT→Claude→Gemini workflow, prompt template, 2–3 hop limit, fact-restore step | `skills/unslop/SKILL.md` anti-detector §6; README FAQ | #35, #25 |
| **Commercial landscape** | Undetectable/Ryter/Walter + QuillBot + Superhuman honest comparison table | SKILL landscape; `docs/RESEARCH_AND_TECH.md` | #61, #64, #63 |
| **DAMAGE L1/L2/L3** | Fluency tier ≠ bypass; Undetectable L3 + Pangram 90.3% | README commercial section | #40, #61 |
| **Dual-detector rule** | Green GPTZero ≠ green Pangram/Turnitin; GPTHuman Pangram/Quetext split | Anti-detector boundaries | #60, #65, #62 |
| **Built-in panel theater** | Vendor sells detect + humanize; Scribbr = QuillBot engine | Glossary | #61, #64 |
| **Bypass rate vs residual AI %** | 79.7% bypass ≠ 0% Turnitin; name metric when citing | Glossary | #61 |
| **Alammyan attribution fix** | Remove Ryter Pro from Alammyan citations | E-practical §20, SYNTHESIS, Cat 18 | #65 |
| **Booth attribution fix** | One humanizer (StealthGPT); not "twelve humanizers" | README, SKILL | #62, #40 |
| **QuillBot overlay** | Turnitin paraphrase flag distinct from AI % | ESL/coursework guidance | #64, #56 |
| **Ladder exhaustion** | When `--detector-feedback` stops, print cross-model recommendation | Already in `detector.py`; keep SSOT sync | #35 |
| **SaaS vs chain comparison** | "unslop + cross-model + manual edit" vs "$8/mo paste-box" | README positioning | #61, #35 |
| **Meaning-first pivot** | Quote Alammyan 2026 framework where discussing human edit requirement | Anti-detector ethics | #65 |

### 4.2 Integrate — Phase 1 (2–3 weeks, UPDATE-PLAN)

| Feature | Rationale | Source |
|---------|-----------|--------|
| **`anti-detector` in feedback ladder** | Loop currently stops at `full + structural + soul`; mode exists but unreachable | #35 §6.6, UPDATE-PLAN |
| **`stylometric_baseline.json`** | Lexical nudges are no-ops without baseline | UPDATE-PLAN |
| **Surprisal wired to CLI `--detector-feedback`** | DivEye measurement orphaned from loop | #01, UPDATE-PLAN |
| **Fix TempParaphraser comment in detector.py** | Comment incorrectly says "no LLM call"; mechanism needs LLM | #38 |

### 4.3 Integrate — Phase 2 (4–6 weeks)

| Feature | Rationale | Source |
|---------|-----------|--------|
| **TempParaphraser-style selection loop** | N candidates per sentence, pick min TMR — port algorithm, not HF weights | #38, #25 |
| **TSD second-half volatility target** | 2026 detector signal unslop doesn't optimize | SYNTH-81, UPDATE-PLAN |
| **SurpMark transition proxy** | Recovery-pattern tells post-paraphrase | SYNTH-81 |
| **Cone-width proxy** | GPTZero v6 synonym-swap resistance | #13, UPDATE-PLAN |
| **Benchmark fixtures** | `quillbot`, `undetectable`, `cross-model` columns in `drafts/2026-05-detector-test/` | #64, #61, #65 |

### 4.4 Integrate — Phase 3 (6–8 weeks, optional LLM pipeline)

| Feature | Rationale | Source |
|---------|-----------|--------|
| **`llm_pipeline.py` cross-model templates** | Automate what skill cannot execute in-session | #35, UPDATE-PLAN |
| **MASH Stage-4 analog** | PPL-ordered sentence polish + TMR gate | #21 |
| **Post-cross-model re-score UX** | Before/after `--detector-feedback` workflow in docs + CLI hints | #35 |
| **DIPPER optional backend** | Practitioner alternative to manual cross-model | #35 §2.4 |

### 4.5 Refuse / out of scope (document why)

| Request | unslop response | Reason |
|---------|-----------------|--------|
| Undetectable.ai / QuillBot API wrapper | No | Bypass positioning; opaque quality; ToS |
| TempParaphraser weight bundle in PyPI | No | Academic-only license |
| AdvPara token-level beam in production | No | Academic integrity attack surface; 2× GPU |
| Watermark removal instructions | No | EU AI Act Art. 50; ladder message explicit |
| "Undetectable alternative" marketing | No | Boundaries in SKILL.md |
| Turnitin bypass guarantee | No | Sadasivan bound; institutional retreat |
| Built-in commercial detector panel | No | Conflict of interest unslop avoids |

---

## 5. Practitioner decision tree (for docs)

```
User asks: "Which humanizer beats Turnitin?"

├─ Graded coursework / thesis?
│   └─ No honest bypass tool. Process authorship > post-hoc scores.
│      Cite Turnitin bypasser Aug 2025, institutional Authorship pivot.
│
├─ Already pays for QuillBot/Grammarly?
│   └─ Use for clarity/grammar. Ignore bypass SEO.
│      Warn: paraphrase overlay on Turnitin; 25–47% bypass coin flip.
│
├─ Considering Undetectable / Ryter / Walter ($8–15/mo)?
│   └─ DAMAGE L3 fluency risk; Pangram ~90% catch; built-in panel unreliable.
│      Alternative: unslop in editor → cross-model second pass → manual edit.
│
├─ ESL false positive / resume polish?
│   └─ /unslop anti-detector + fact check. Liang 2023 cite.
│      NOT "cheaper humanizer subscription."
│
└─ Need maximum fingerprint separation?
    └─ unslop deterministic passes → cross-model chain (2 hops max)
       → manual restore → re-score on TARGET detector(s).
       Optional: TempParaphraser-style multi-candidate (Phase 2) if TMR available.
```

---

## 6. Evidence tiers for landscape citations

| Tier | Label | Examples in this synthesis |
|------|-------|---------------------------|
| Peer-reviewed | [P] | DAMAGE L1/L3; Epaphras 93.56%; TempParaphraser; AdvPara; Booth WP |
| Independent third-party | [I] | Detection Drama; EyeSift; Supwriter; Alammyan (protocol-specific) |
| Affiliate / competitor | [A] | HumanizeMyAI; AuraWrite; HumanizerBench; WriteHuman benchmarks |
| Vendor | [V] | Undetectable 99.8%; Ryter 99.9%; QuillBot marketing |
| User reviews | [U] | Trustpilot Walter; Medium comments |

**Rule:** Never rank humanizers from affiliate lists alone. Dual-report detector + version date. Competitor benchmarks are **directional skepticism**, not gospel.

---

## 7. Competitive positioning — unslop vs practitioner stack

| Dimension | Cross-model + unslop | QuillBot | Undetectable.ai | Superhuman |
|-----------|---------------------|----------|------------------|------------|
| **Primary goal** | Voice + ESL defense | Suite clarity | Detector evasion | Integrity platform |
| **Mechanism** | Subtract + family swap | L1 paraphrase | L3 black-box | L1 humanizer + Authorship |
| **Preservation** | Byte-exact code/URLs | Citations drift | Often breaks | Docs-native |
| **Turnitin honest expectation** | None claimed | ~25–47% [I] | Low–moderate [I] | Provenance > score |
| **Cost** | API calls user pays | ~$8/mo | ~$5–15/mo | ~$12+/mo |
| **Open source** | Yes | No | No | No |
| **Strongest honest lever** | Cross-model after ladder | Paraphrase polish | None reliable 2026 | Draft history |

**unslop wins:** honesty, preservation, in-editor integration, ESL framing, free.  
**unslop loses:** distribution, provenance capture, RAID-marketed detector depth, one-click paste-box UX.

---

## 8. Doc / code action checklist

| Pri | Action | Owner surface |
|-----|--------|---------------|
| **P0** | Add Undetectable/Ryter/Walter + QuillBot to commercial landscape with DAMAGE/Pangram cites | `skills/unslop/SKILL.md` |
| **P0** | Fix Ryter Pro → Alammyan misattribution | E-practical §20, Cat 18, SYNTHESIS |
| **P0** | Fix "Booth twelve humanizers" conflation | README, SKILL |
| **P0** | Glossary: bypass rate vs residual AI %; Scribbr = QuillBot engine | `docs/RESEARCH_AND_TECH.md` |
| **P1** | Practitioner cross-model protocol in anti-detector §6 (sync detector.py message) | SKILL SSOT + mirrors |
| **P1** | QuillBot Turnitin overlay warning for coursework users | SKILL Boundaries |
| **P1** | Add `anti-detector` to `DEFAULT_LADDER` | `unslop/scripts/detector.py` |
| **P1** | Alammyan Pangram 4-tool table with n=1 caveat | Landscape / RESEARCH_AND_TECH |
| **P2** | Benchmark CSV: quillbot, undetectable, cross-model columns | `drafts/2026-05-detector-test/` |
| **P2** | TempParaphraser selection loop (no vendored weights) | Phase 2 `llm_pipeline.py` |
| **P2** | Fix detector.py TempParaphraser "no LLM" comment | `detector.py` |
| **P3** | Cross-model prompt templates in LLM pipeline | Phase 3 |

---

## 9. Debate summary

| Camp | Claim | Best evidence |
|------|-------|---------------|
| **Bypass optimists** | Cross-model + SaaS beats detectors | Practitioner forums; TempParaphraser; pre-2025 Turnitin stats (**stale**) |
| **Detection optimists** | Adapted detectors survive (Pangram, Turnitin bypasser) | DAMAGE; Booth StealthGPT arm; Pangram Aug 2025 table |
| **Meaning-first (Alammyan 2026)** | Chasing scores produces thesaurus-bot; human edit required | Refunded $5K sponsor; framework post |
| **Provenance shift (Superhuman)** | Authorship beats post-hoc classifier | GPTZero acquisition; Docs default-on Mar 2026 |
| **unslop position** | Subtract in-editor; document cross-model capstone; refuse bypass marketing | detector.py ladder; SKILL boundaries |

---

## 10. Bottom line

Practitioners in 2026 stack **cross-model rewrite** (strongest accessible lever), **suite paraphrasers** (QuillBot — weak, ubiquitous), and **dedicated humanizers** (Undetectable tier — aggressive marketing, L3 quality, ~90% Pangram catch). Built-in detector panels are **vertical integration theater**. Chicago Booth and Alammyan add nuance: detector rankings **invert under humanization**; single-sample affiliate tests **disagree with adapted detectors**.

**unslop documents the stack honestly and integrates the defensible slices:** deterministic de-slop, anti-detector register restoration, ladder exhaustion → cross-model recommendation, and (Phase 2+) TempParaphraser-style TMR selection without shipping bypass SaaS or Turnitin guarantees. The product is **prep work + honest escalation**, not a paste-box competitor.

---

*SYNTH-88 complete. Inputs: evasion memos #21, #25, #35, #38, #39, #40; commercial memos #61–#65.*
