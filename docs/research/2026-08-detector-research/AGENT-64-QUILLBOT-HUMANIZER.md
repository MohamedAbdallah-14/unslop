# Agent #64 — QuillBot Humanizer + AI Detector

**Topic:** QuillBot suite humanizer and detector — product features, evasion claims, independent audits, user debate, unslop comparison  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop SKILL.md / README landscape refresh

---

## Executive summary

**QuillBot** is the dominant **mainstream writing suite** (~30M+ monthly visits per Cat 18 industry estimates) that bolted a dedicated **AI Humanizer** onto its 2017-era paraphraser in **late 2025**. It sits in a different product class from paste-box bypass vendors (Undetectable.ai, Ryter Pro, Walter Writes — Agent #61): QuillBot markets **clarity and flow**, not undetectability. That honest framing has aged well as detectors tightened — but users still treat the paraphraser/humanizer as a Turnitin workaround.

**What independent measurement actually shows:**

| Dimension | QuillBot Humanizer | QuillBot AI Detector |
|-----------|-------------------|----------------------|
| **Evasion vs Turnitin** | **25–47% bypass** across 2025–2026 panels [I] | N/A |
| **Evasion vs GPTZero** | **40–55% bypass** (one-pass); Standard mode ~0% improvement on academic essays [I] | **11.8% recall** on GPTZero's 1,000-text bypasser corpus (4.3b) [V] — worst major detector in that table |
| **Peer-reviewed evasion** | **93.56% ADR** (Epaphras & Mtenzi 2026) — flagged **15/18** iterations [P] | Used as weak panel detector in same study |
| **DAMAGE tier** | **L1** (synonym/dictionary replacement) [P] | — |
| **Copyleaks (EyeSift Apr 2026)** | **31% false-negative** after QuillBot paraphrase — Copyleaks misses ~1 in 3 [I] | — |
| **Self-test collapse (HumanizeMyAI May 2026)** | Humanizer output **92–96% AI** on QuillBot's own detector post-refresh [A] | Detector updated; humanizer prompt tuning did not follow |

**Ecosystem pattern:** QuillBot is a **paraphraser with a humanizer skin** — light synonym substitution that preserves the AI sentence skeleton. Turnitin's **Jul 2024 two-category report** explicitly names QuillBot as the example paraphrasing tool; **Aug 2025 bypasser detection** added a classifier layer trained on common paraphraser fingerprints. GPTZero ships a dedicated **"possible AI paraphrase detected"** label. The failure mode is often **worse than a high AI score**: Turnitin can surface **paraphrasing-tool modification** as a visible overlay even when the numeric AI percentage looks borderline.

**unslop positioning:** QuillBot and unslop solve different problems. QuillBot **rephrases** (and sometimes inflates word count) inside a paid SaaS box. unslop **subtracts AI-isms** in-editor with byte-exact preservation of code, URLs, and headings. Neither is a Turnitin guarantee. For users who already pay for QuillBot for grammar/plagiarism, the honest guidance is: **use the paraphraser for polish, not bypass**; run **unslop + cross-model second pass** if fingerprint separation is the goal — not another synonym pass.

**Highest-value unslop doc actions:**

1. **Name QuillBot explicitly** in suite-humanizer landscape — users conflate it with dedicated bypass tools.
2. **Cite Epaphras 93.56% ADR** and DAMAGE **L1** when comparing "humanizer" vs "paraphraser" categories.
3. **Warn on Scribbr = QuillBot engine** — Learneo vertical integration is not independent verification.
4. **Separate Turnitin paraphrase overlay from AI %** — QuillBot-specific failure mode for coursework.
5. **Do not market unslop as "QuillBot alternative" on bypass** — market on voice, preservation, ESL false-positive defense.

---

## Primary sources (URLs)

### Product & pricing

| Resource | URL |
|----------|-----|
| **QuillBot homepage** | https://quillbot.com |
| **AI Humanizer (product page)** | https://quillbot.com/ai-humanizer |
| **AI Content Detector** | https://quillbot.com/ai-content-detector |
| **Premium pricing** | https://quillbot.com/premium |
| **Paraphraser** | https://quillbot.com/paraphrasing-tool |
| **Scribbr AI Humanizer (sister brand)** | https://www.scribbr.com/ai-humanizer/ |
| **Scribbr AI Detector** | https://www.scribbr.com/ai-detector/ |
| **Scribbr "best AI detector" self-test (2026)** | https://www.scribbr.com/ai-tools/best-ai-detector/ |
| **QuillBot Custom GPT (ChatGPT)** | Linked from humanizer page |

### Peer-reviewed & vendor-detector research

| Resource | URL |
|----------|-----|
| **DAMAGE paper (COLING 2025) — QuillBot L1 baseline** | https://arxiv.org/abs/2501.03437 |
| **Epaphras & Mtenzi 2026 — QuillBot 93.56% ADR** | https://doi.org/10.37284/ijar.9.1.4683 |
| **Liang et al. 2023 — ESL detector bias** | https://doi.org/10.1016/j.patter.2023.100779 |
| **Turnitin AI model guide (QuillBot named, Jul 2024 split)** | https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model |
| **Turnitin bypasser press (27 Aug 2025)** | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers |
| **GPTZero bypasser Table 7 — QuillBot detector 11.80% recall** | https://gptzero.me/news/gptzero-ai-detection-benchmarking-the-industry-standard-in-accuracy-transparency-and-fairness/ |
| **GPTZero paraphrase detection feature** | https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/ |

### Independent reviews & tests (2025–2026)

| Resource | URL | Tier |
|----------|-----|------|
| **HumanizeMyAI — QuillBot Humanizer 30-run test** | https://humanizemy.ai/vs/quillbot-humanizer | [A]* |
| **HumanizeMyAI — Scribbr = QuillBot engine** | https://humanizemy.ai/scribbr-ai-detector | [A]* |
| **Supwriter — 100-sample paraphraser test (42% avg bypass)** | https://supwriter.com/blog/quillbot-humanizer-review | [A]* |
| **Supwriter — QuillBot review 2026** | https://supwriter.com/blog/quillbot-review-2026 | [A]* |
| **WriteHybrid — suite framing, no bypass promise** | https://www.writehybrid.com/humanizers/quillbot-humanizer | [I] |
| **UndetectedGPT — Turnitin detects QuillBot** | https://www.undetectedgpt.ai/blog/can-turnitin-detect-quillbot | [A]* |
| **UndetectedGPT — GPTZero vs Turnitin (QuillBot ~1/4 below 20%)** | https://www.undetectedgpt.ai/blog/gptzero-vs-turnitin | [A]* |
| **AI Busted — 5 detectors × QuillBot Standard/Creative (Jun 2026)** | https://blog.aibusted.com/can-ai-detectors-detect-quillbot/ | [A]* |
| **StealthZero — QuillBot humanizer feature gaps** | https://blog.stealthzero.ai/blog/rephraser/quillbot-humanizer/ | [A]* |
| **EyeSift — Copyleaks review (QuillBot 31% FN)** | https://www.eyesift.com/blog/copyleaks-ai-detector-review/ | [I] |
| **GPTZero — Scribbr = QuillBot wrap (~80% accuracy)** | https://gptzero.me/news/scribbr-review-ai-detector/ | [V] |
| **BelikeNative — QuillBot detector ~78–80%** | https://belikenative.com/is-quillbots-ai-detector-trustworthy-we-tested-it-against-other-ai-checkers/ | [I] |
| **Axis Intelligence / AIera — Scribbr ~72.8% detection** | https://aiera.blog/scribbr-ai-detector-review-2026-accurate-free/ | [I] |
| **ToolChase — QuillBot paraphrase 40–43% GPTZero hit** | Cited in Agent #13 | [I] |
| **aitooldiscovery — QuillBot alone 34% bypass** | https://www.aitooldiscovery.com/guides/how-to-bypass-ai-detection-reddit | [I] |

\*Competitor-operated humanizer/detector sites — directional for bypass numbers, not neutral ground truth.

### unslop cross-refs

| Agent memo | Relevance |
|------------|-----------|
| **Agent #40 — DAMAGE L1/L2/L3 tiers** | QuillBot = L1 synonym tier; Pangram 100% on L1 paraphrasers |
| **Agent #56 — Turnitin 2025–2026** | QuillBot ~47% avg post-bypasser; AIR-1 paraphrase class |
| **Agent #59 — Copyleaks V9** | EyeSift QuillBot FN 31% |
| **Agent #61 — Undetectable/Ryter/Walter** | Dedicated bypass tier vs suite humanizer |
| **Agent #13 — GPTZero v6 cones** | QuillBot detector 11.80% on bypasser corpus |
| **Agent #01 — DivEye** | Paraphrase drops mean perplexity, not burstiness variance |
| **Agent #35 — Cross-model paraphrase** | Documented alternative to QuillBot one-pass |
| **Cat 18 D-commercial** | QuillBot pricing, suite positioning |

---

## Product architecture — Learneo writing stack

```
Learneo (formerly Course Hero)
├── QuillBot — paraphraser (2017) + grammar + plagiarism + AI detector + humanizer (late 2025)
├── Scribbr — academic brand; AI detector = QuillBot engine rebrand; Turnitin-licensed plagiarism (separate)
└── Shared detection backend — Scribbr AI check ≈ QuillBot AI check (not independent)
```

**User journey (typical student/workflow):**

```
ChatGPT/Claude draft
  → QuillBot Paraphraser (Standard/Fluency/Creative) OR Humanizer tab
  → QuillBot/Scribbr built-in AI score (single vendor engine)
  → LMS submission
  → Turnitin / GPTZero / Originality — often disagree; Turnitin may add paraphrase overlay
```

**Why this matters for unslop:** QuillBot users often **double-check with the same engine** (QuillBot detector → Scribbr detector) and treat agreement as ground truth. That is **vertical integration theater**, not external validation.

---

## Humanizer — features & pricing

### What QuillBot ships [V]

| Feature | Detail |
|---------|--------|
| **Humanizer tab** | Dedicated UI on `/ai-humanizer`; distinct from classic paraphraser modes |
| **Training claim** | "Tens of thousands of texts"; NLP word-choice + sentence-structure refinement |
| **Modes / presets** | Natural tone default; per-sentence alternate phrasings via dropdown |
| **Paraphraser modes (legacy)** | Standard, Fluency, Formal, Simple, Expand, Shorten, Creative (synonym intensity) |
| **Bundled suite** | Grammar checker, plagiarism checker, summarizer, translator, AI detector |
| **ChatGPT integration** | Custom GPT for in-conversation humanization |
| **Human score** | Premium readability metric — **not** a published multi-detector bypass rate |
| **File import** | PDF/Word on Premium |
| **Languages** | Primarily English; detector supports EN/ES/DE/FR per third-party tests |

### Pricing [V] — verified against Cat 18 + 2026 reviews

| Tier | Price | Humanizer limits |
|------|-------|------------------|
| **Free** | $0 | ~125 words/use, ~6 uses/day (StealthZero/HumanizeMyAI citations) |
| **Premium (annual)** | ~$8.33/mo (~$99.95/yr) | Unlimited humanizer; full suite |
| **Premium (monthly)** | ~$19.95/mo | Same |
| **API** | Commercial paraphrase API exists | Humanizer mode separately gated |

### Marketing posture [V]

QuillBot's humanizer page emphasizes **natural, human-sounding language** and **preserved meaning**. It does **not** publish:

- A numeric bypass rate against Turnitin, GPTZero, or Originality
- Multi-detector "proof reports"
- Locked-phrase / citation-preservation controls for academic work

WriteHybrid [I] and StealthZero [A] both note this is **deliberate legitimacy positioning** — clarity/voice, not detector evasion. Contrast: Undetectable.ai "99.8% undetectable," Ryter "99.9% Turnitin."

### Technical class (research consensus)

| Mechanism | QuillBot | Research label |
|-----------|----------|----------------|
| Word-level synonym swap | Primary | L1 in DAMAGE; "paraphraser not humanizer" |
| Sentence skeleton preserved | Yes — HumanizeMyAI | DivEye: burstiness variance survives |
| Discourse-level reorder | Minimal vs DIPPER | RAID synonym-swap attack axis |
| Error injection | No | L3 bypass tools only |
| Cross-model rewrite | No | Agent #35 documented alternative |

HumanizeMyAI (May 2026): Humanizer module is **"synonym-substitution engine with a humanizer skin"** — outputs carry the underlying AI draft skeleton.

---

## AI Detector — features & accuracy

### What QuillBot ships [V]

| Feature | Detail |
|---------|--------|
| **Input minimum** | ~80 words (BelikeNative) |
| **Output** | Document-level AI probability + sentence-level highlights (Premium) |
| **Languages** | EN, ES, DE, FR cited in comparisons |
| **Free tier** | Unlimited checks with word caps; no signup on some flows |
| **Scribbr sibling** | Same Learneo engine — near-identical scores |

### Accuracy claims vs measurement

| Source | QuillBot detector accuracy | False positives | Notes |
|--------|---------------------------|-----------------|-------|
| **Scribbr self-test (2026)** | **78%** free; **84%** premium Scribbr | Premium: 0 FP in their n | Same engine — circular |
| **BelikeNative (50 texts)** | **~78–80%** | 0 in their n | Behind GPTZero 99.5% in same test |
| **Axis Intelligence / AIera** | **~72.8% detection rate** | **~9.2%** human FP | Scribbr-branded engine |
| **GPTZero competitor review** | **~80%** correct | High FP on human sample | "Wrap-around" for QuillBot |
| **GPTZero bypasser Table 7** | **11.80% recall** on 1,000 bypasser texts | — | Worst listed commercial detector |

**Interpretation:** QuillBot's detector is **respectable for obvious raw GPT** on free quick checks. It is **weak on paraphrased/humanized text** (ironic given the suite sells both sides) and **not competitive** with GPTZero/Turnitin on adapted bypasser corpora.

### Conflict of interest

QuillBot sells **detector + humanizer in one subscription**. HumanizeMyAI documented a **May 2026 stack mismatch**: humanizer output scored **92–96% AI** on QuillBot's own detector after a detector model refresh — the humanizer's prompt tuning did not keep pace. Same structural problem as Undetectable.ai's panel (Agent #61), but QuillBot never promised bypass.

---

## Evasion claims vs independent measurement

### Vendor claims [V]

| Claim | Evidence tier | Reality check |
|-------|---------------|---------------|
| "Human-sounding" / "natural language" | Marketing | Subjective; does not imply detector pass |
| "Preserves meaning" | Product copy | Independent reviews: struggles on dense academic + citations |
| "Can help with AI detection" (implied in SEO ecosystem) | Third-party affiliates | QuillBot official pages avoid numeric bypass promises |
| Human score / readability metric | Premium UI | Not validated against Turnitin |

### Independent bypass tables

**Supwriter — 100 texts, Creative mode max synonym, five detectors [A]:**

| Detector | Bypass rate | Detection rate |
|----------|-------------|----------------|
| Turnitin | **38%** | 62% |
| GPTZero | **45%** | 55% |
| Originality.ai | **35%** | 65% |
| Copyleaks | **48%** | 52% |
| ZeroGPT | **52%** | 48% |
| **Average** | **~42%** | coin flip |

**HumanizeMyAI — 30 runs, post–Aug 2025 Turnitin [A]:**

| Detector | Median / typical |
|----------|------------------|
| Turnitin | **~47% bypass** |
| QuillBot self-detector (May 15 re-test) | **92–96% AI** after humanizer |

**AI Busted — Jun 2026, 5 originals × Standard/Creative, 5 detectors [A]:**

| Detector | Standard (5/5 AI texts) | Creative |
|----------|-------------------------|----------|
| Turnitin | **5/5 detected** | 3/5 detected |
| GPTZero | 3/5 detected | 2/5 detected |
| Originality.ai | 4/5 detected | 2/5 detected |

**UndetectedGPT — synthesis [A]:** Only **~1 in 4** QuillBot-processed passages drop **below Turnitin's 20% display threshold**; scores often land **38–64%** even after "improvement" from 94% raw.

**Practitioner aggregate (aitooldiscovery Reddit synthesis) [I]:** QuillBot alone **~34%** success vs multi-detector workflow — below Undetectable (82%), Humbot (71%), BypassGPT (67%).

**EyeSift — Copyleaks on QuillBot-paraphrased samples [I]:** **31% false-negative rate** — evasion works often enough to matter for integrity policy, but far from reliable bypass.

### Peer-reviewed

| Study | QuillBot result | Context |
|-------|-----------------|---------|
| **DAMAGE (COLING 2025)** | **L1 tier** — synonym/dictionary replacement; Pangram **100% catch** on L1 paraphrasers in follow-up | Baseline paraphraser, not top-tier humanizer |
| **Epaphras & Mtenzi (2026)** | **93.56% ADR** — detected in **15/18** iterations | vs WriteHuman **1.98% ADR**; panel = QuillBot detector, ZeroGPT, Scribbr |
| **Adversarial Paraphrasing (NeurIPS 2025)** | QuillBot-class synonym swap can **increase** detection on some metrics | Agent #35 — wrong attack axis |

### Turnitin-specific — paraphrase overlay (QuillBot-named)

From Turnitin model documentation (Jul 2024) [V] and independent tests [I]:

1. **Two-category report era:** "AI-generated only" vs "AI-generated text that was AI-paraphrased" — QuillBot cited as example spinner.
2. **Aug 2025 bypasser model:** Classifier layer trained on **lexical-substitution signatures** from common paraphrasers — the pattern QuillBot Humanizer produces.
3. **Observed LMS behavior [I]:** Purple/blue highlight + label such as **"AI-generated with paraphrasing tool modification"** — integrity signal **distinct from AI percentage alone**.

**Agent #56 summary:** QuillBot Humanizer was **weak pre-update**; post-bypasser **~47% avg** across detectors — Turnitin explicitly targets synonym-swap class.

---

## Claim vs measurement — synthesis table

| Claim source | Bypass / evasion | Quality / fluency | Detector honesty |
|--------------|------------------|-------------------|------------------|
| **QuillBot official** | No numeric bypass claim | "Natural," meaning preserved | Single-engine score |
| **Supwriter 2026** | **42% avg** | Paraphraser not humanizer | — |
| **HumanizeMyAI 2026** | **47% Turnitin median** | Skeleton preserved | Self-detector **95% AI** post-refresh |
| **Epaphras 2026** | **93.56% ADR** (fail) | L1 DAMAGE tier | QuillBot detector in weak panel |
| **DAMAGE 2025** | L1 — **100% Pangram catch** | Best fluency among evaders = *more* detectable (inverse for L3) | — |
| **EyeSift 2026** | **31% FN** on Copyleaks | — | Copyleaks misses paraphrased AI |
| **GPTZero Table 7** | — | — | QuillBot detector **11.8% recall** on bypassers |
| **Dedicated humanizers (Agent #61)** | 54–90% on *some* panels | Often L3 (Undetectable) | Built-in green checks unreliable |

**Interpretation:** QuillBot sits **below dedicated bypass SaaS** on every independent evasion metric and **above them on editorial legitimacy**. It is the **dominant free-tier recommendation** on Reddit for "try paraphrasing first" — but 2026 consensus is that **paraphrasing alone no longer works** against Turnitin/GPTZero for most academic prose.

---

## Debate map — supporters vs skeptics

### Mainstream / legitimacy camp

| Actor | Position |
|-------|----------|
| **QuillBot / WriteHybrid [I]** | Humanizer = flow and tone; verify on your own checker before graded work |
| **Grammarly-class vendors** | Same clarity-not-bypass posture (Agent #61 comparison) |
| **ESL educators** | Paraphraser helps **language polish**, not authorship concealment |

### Skeptics / independent testers

| Actor | Position |
|-------|----------|
| **HumanizeMyAI / Supwriter [A]** | 42–47% bypass = coin flip; wrong tool for Turnitin |
| **Turnitin [V]** | QuillBot-class tools named in paraphrase/bypasser training |
| **GPTZero [V]** | Dedicated paraphrase flag; 91.8%+ recall on bypasser corpus |
| **Pangram / DAMAGE [P]** | L1 paraphrasers caught 100%; fluent rewrite ≠ stealth |
| **DetectionDrama ecosystem [I]** | "Scribbr clean" ≠ Turnitin clean |

### Practitioner consensus (Reddit/forums, 2025–2026)

1. **QuillBot reword only** — inconsistent on essays **>600 words**; breaks on technical terms.
2. **Free first step** — still recommended, but **not sufficient** post–Aug 2025 Turnitin.
3. **Creative mode > Standard** — helps on GPTZero/Originality sometimes; **Turnitin still catches most**.
4. **Scribbr + QuillBot double-check is useless** — same engine.
5. **Structural rewriters** (Walter, cross-model) beat QuillBot in threads — aligns with Agent #35.
6. **Chaining QuillBot → dedicated humanizer** — ~41% in aitooldiscovery synthesis; adds cost, still no guarantee.

---

## unslop positioning

### What unslop is not

| QuillBot-shaped expectation | unslop response |
|----------------------------|-----------------|
| Cloud paraphrase box | In-editor skill + optional local Python pipeline |
| Synonym substitution | Subtractive AI-ism removal + structural/soul passes |
| Built-in AI score loop | Optional `--detector-feedback`; not primary metric |
| $8–15/mo suite bundle | Free/open-source plugin + PyPI |
| "Humanize" = rephrase entire draft | Preserve code, URLs, headings byte-exact (`TestPreservation`) |

### Head-to-head comparison (August 2026)

| Dimension | QuillBot Humanizer | **unslop** |
|-----------|-------------------|------------|
| **Primary goal** | Readability / suite retention | Editorial voice / de-slop |
| **Mechanism** | LLM paraphrase + synonym modes | Regex + optional LLM; structural + soul passes |
| **Bypass marketing** | Implicit in SEO; absent on official page | Explicitly disclaimed |
| **Turnitin expectation [I]** | **25–47% bypass** — overlay risk | No guarantee; anti-detector = ESL defense |
| **DAMAGE / peer-reviewed** | **L1**; **93.56% ADR** | Not in DAMAGE set; deterministic TMR ~0.0–0.2 pp |
| **Preservation** | Can alter citations/terminology | Contract-tested preservation |
| **Detector bundled** | Yes — conflict of interest | No vendor detector |
| **Cross-model pass** | No | Documented user workflow (Agent #35) |
| **Price** | ~$8.33/mo annual | Free |

### Recommended messaging (August 2026)

> **QuillBot** is a polished writing suite whose humanizer **rephrases** AI drafts into smoother prose. Independent tests put Turnitin bypass in the **~25–47%** range — a coin flip, often with a **paraphrase-tool flag** even when the AI percentage looks borderline. QuillBot's own detector and Scribbr's detector share the same engine; passing both is not independent verification.
>
> **unslop** does not rephrase your draft in a black box. It removes stock phrases, uniform rhythm, and performative balance while keeping your code and links intact. That is voice work — the same edits that help **ESL writers fight false positives**. For fingerprint separation beyond deterministic unslop, run a **cross-model second pass** you control. Neither tool is a Turnitin guarantee.

### User routing (decision tree)

```
Need grammar + plagiarism + paraphrase for daily writing?
  → QuillBot Premium may be worth it — ignore humanizer bypass SEO

Need to sound less like ChatGPT in Cursor/Claude Code?
  → /unslop balanced or full

Need ESL / resume false-positive defense?
  → /unslop anti-detector (+ manual fact check)

Need maximum separation from LLM fingerprints?
  → unslop → cross-model rewrite → manual edit
  → NOT QuillBot Creative mode alone

Need Turnitin clearance for graded work?
  → No honest tool recommendation — process-based authorship > post-hoc scores
```

### Boundaries (unchanged — load-bearing)

From `skills/unslop/SKILL.md`:

- Anti-detector mode: **defensive** (ESL false positives, resume writers) — **not** "cheaper QuillBot."
- Never fabricate facts to satisfy anti-detector mode.
- Do not claim unslop outperforms QuillBot on bypass — claim **honesty, preservation, integration**.

### Doc / code actions

| Priority | Action | Target |
|----------|--------|--------|
| P0 | Add QuillBot to suite-humanizer paragraph with Epaphras 93.56% + Turnitin overlay | `skills/unslop/SKILL.md` |
| P0 | Glossary note: **Scribbr detector = QuillBot engine** | `docs/RESEARCH_AND_TECH.md` |
| P1 | Landscape table row: QuillBot vs dedicated humanizers vs unslop | README commercial comparison |
| P1 | `drafts/2026-05-detector-test/` — add `quillbot` column (CSV headers exist, cells empty) | Benchmark runbook |
| P2 | `--surprisal-variance` doc tie-in: paraphrase drops mean PPL not burstiness (Agent #01) | `unslop/scripts/surprisal.py` docs |

---

## Competitive positioning matrix (August 2026)

| Dimension | QuillBot | Undetectable.ai | Grammarly Humanizer | **unslop** |
|-----------|----------|-------------------|---------------------|------------|
| **Category** | Suite paraphraser + humanizer | Dedicated bypass | Suite clarity | Editor skill |
| **Bypass claim** | None official | 99.8% [V] | None | None |
| **Turnitin [I]** | ~25–47% | 54–67% (conflicted) | ~0% HumanizerBench | Not claimed |
| **DAMAGE tier** | **L1** | **L3** | **L1** (100% detected HumanizerBench) | — |
| **Monthly cost** | ~$8.33 | ~$5+ | ~$12+ | $0 |
| **Open source** | No | No | No | Yes |
| **Integrity posture** | Clarity framing | Bypass SEO | Legitimacy play | ESL defense explicit |

**Where QuillBot sits vs Agent #61 trio:** **Strictly weaker on evasion**, stronger on **mainstream trust and suite utility**. Users comparing "which humanizer beats Turnitin" should not start with QuillBot — but many do because it is already installed for paraphrase.

---

## Open questions

1. **Humanizer vs paraphraser delta:** Does QuillBot's dedicated Humanizer tab outperform Creative paraphrase on Turnitin in a controlled n≥100 test? Public tests conflate the two.
2. **May 2026 detector/humanizer mismatch:** Did QuillBot re-sync humanizer tuning after detector refresh? HumanizeMyAI snapshot may be transient.
3. **Scribbr premium 84% claim:** Independent replication with ESL subsample and paraphrased-AI subsample — Scribbr self-test mixes both.
4. **Institutional QuillBot API:** Enterprise paraphrase API humanizer gating — campus license bypass workflows undocumented.
5. **unslop × QuillBot chain:** No published test of deterministic unslop → QuillBot vs unslop → cross-model — worth a fixture row in `drafts/2026-05-detector-test/`.

---

## unslop verdict

**QuillBot Humanizer + Detector** is the **respectable face of the humanizer category** — a suite feature that **never promised undetectability** and therefore **cannot be embarrassed** when Turnitin and GPTZero retrain. It is also **the wrong tool** for the job users secretly hire it for: independent 2025–2026 panels consistently place Turnitin bypass in the **~25–47%** range, peer-reviewed Epaphras data shows **93.56% average detection**, and DAMAGE classifies the underlying mechanism as **L1 synonym replacement** — the attack axis modern detectors were built to catch.

**QuillBot's detector** is a **free quick screen**, not ground truth. It shares DNA with Scribbr, scores **~72–84%** in mixed tests, and scored **11.8% recall** on GPTZero's hardest bypasser benchmark. Selling humanizer and detector together creates **self-reinforcing false confidence** — documented when humanizer output failed QuillBot's own detector at **~95% AI** after a May 2026 refresh.

**unslop wins on honesty, preservation, and in-editor workflow** — not bypass. Users arriving from "QuillBot didn't beat Turnitin" should hear: subtract AI-isms first, preserve your sources, use cross-model rewrite if fingerprint separation matters, and never treat Scribbr/QuillBot green checks as institutional clearance. QuillBot remains a **reasonable paraphraser**; it is not a **humanizer** in the DAMAGE sense, and it is not a **competitor** to unslop on voice — only on mindshare.

---

*Evidence tiers: [P] peer-reviewed / preprint · [I] independent third-party · [A] affiliate/competitor benchmark · [V] vendor · [U] user reviews*
