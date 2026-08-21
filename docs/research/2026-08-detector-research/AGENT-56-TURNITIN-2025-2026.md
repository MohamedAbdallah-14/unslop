# Agent #56 — Turnitin 2025–2026 Detector Updates

**Topic:** Turnitin AI writing detection — bypasser model (Aug 2025), February 2026 retrain, unified UI (Jul 2026), educator sentiment, unslop honest positioning  
**Prepared:** August 19, 2026  
**Scope:** Press releases, official release notes, independent tests, institutional policy, unslop framing  
**Status:** complete

---

## Executive summary

Turnitin spent 2025–2026 on three parallel tracks: **catch humanizers**, **hide low-confidence scores**, and **simplify what instructors see**.

The headline move is **AI bypasser detection**, shipped **August 27, 2025**. Turnitin folded detection of text run through "leading AI bypasser tools" into its existing English AI writing model. No separate product, no published detection rate, no published false-positive rate for the bypasser layer specifically. English only. Available via Turnitin Originality add-on and iThenticate 2.0 AI capabilities.

**February 12, 2026:** another English model refresh — "improve recall while maintaining a low false positive rate." No UI change. Not retroactive; resubmit to get new scores.

**July 20, 2026:** unified AI report UI — single blue highlight replaces the two-color system (blue = raw LLM, purple = AI-paraphrased/bypassed). Vendor rationale: instructors were over-reading color distinctions as proof of workflow. Detection logic unchanged; presentation simplified.

Independent testing is thin and noisy. The best public test is **Tadhg Blommerde (Northumbria University)**, Sept 2025: six humanizers, small sample. StealthGPT 0%→72%, Groby 0%→67%, GPT Human 31%, Easy Essay still 0%. Turnitin labels everything "AI generated" — no bypasser sub-label in the report. Blommerde: "an improvement, but not perfect"; "totally accurate AI detection is a myth."

Educator sentiment is split and hardening against high-stakes use. **Curtin University disabled Turnitin AI detection January 1, 2026** (originality checking stays). Vanderbilt, UT Austin, Northwestern disabled earlier (2023–2024). Turnitin's own docs say the score must not be sole basis for adverse action; 1–19% scores are suppressed as `*%`.

**Unslop honest positioning:** Do not market as "beat Turnitin." Vendor retrains on humanizer outputs; any single-score optimization decays in weeks. Anti-detector mode is for **ESL false-positive defense** and **register restoration** (TV-reduction: burstiness, contractions, specificity), not guaranteed evasion. Cross-model second pass is the strongest lever the skill can recommend; `--surprisal-variance` is the DivEye-aligned measurement hook. Correct a repo error: **Chicago Booth (Jabarian & Imas 2025) did not evaluate Turnitin** — it tested Pangram, Originality.ai, GPTZero, RoBERTa. The "Turnitin 60–85% at Booth" line in current SKILL.md is unsupported and should be removed or re-sourced.

---

## 1. Product timeline (verified)

| Date | Release | What changed | Source |
|------|---------|--------------|--------|
| Apr 2023 | AI writing detection launch | Document-level 0–100% score; instructor-only visibility | [Turnitin AI writing FAQ](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) |
| Dec 2023 | Paraphrase in score | AI-paraphrased text counted inside overall AI % | Secondary timelines; [WibbleAI chronology](https://www.wibbleai.com/blog/can-turnitin-detect-humanized-ai-text) |
| **Jul 16, 2024** | Two-category report | Split: "AI-generated only" vs "AI-generated text that was AI-paraphrased" (names QuillBot as example spinner) | [AI writing detection model guide](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) |
| Aug 2024 | Whitepaper | **AIW-2** (core LLM detection) + **AIR-1** (paraphrase detection) architecture published | [TII whitepaper (Sep 2024)](https://www.scribd.com/document/988214788/TII-AI-HE-AIWritingDetectionModel-Whitepaper-US-0924-1) |
| Jul 2024 | Low-score suppression | Scores 1–19% shown as asterisk to limit false-positive overreaction | [Model guide](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) |
| **Oct 14, 2025** | Model refresh | Improved recall; formalized `*%` for 1–19%; "non-native speaker" tuning claimed in vendor blog coverage | [Model guide](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model); [Turnitin.app blog](https://turnitin.app/blog/Turnitin-October-2025-AI-Detection-Updates.html) |
| **Aug 27, 2025** | **Bypasser detection** | "AI-generated only" category now includes bypasser-modified text; integrated, English-only | [Press release](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers); [PR Newswire](https://www.prnewswire.com/news-releases/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers-302539461.html); [Release notes Aug 27](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes) |
| **Feb 12, 2026** | English model refresh | Improved recall, FP held low; no UI change; not retroactive | [Model guide — 2026 release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) |
| May 2026 | Spanish model refresh | Better recall on newer LLMs (GPT-5 family, Gemini 2.5); bypasser/paraphrase still English-only | [Product updates](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates) |
| Jul 15, 2025 | Next Gen Feedback Studio | Consolidated inbox: similarity + AI scores in one workflow | [Blog](https://www.turnitin.com/blog/unlocking-insights-whats-new-in-turnitin-feedback-studio) |
| **Jul 20, 2026** | **Unified blue highlight** | Single blue for all likely AI (raw + paraphrased + bypassed); drops purple segment | [Product updates — Jul 20](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates); [Blog — simplifying AI detection](https://www.turnitin.com/blog/how-turnitin-is-simplifying-ai-detection-for-educators-and-publishers) |
| Jul 8, 2026 | Unified assignment creation | Single-screen assignment settings (Standard + Clarity) | [Product updates — Jul 8](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates) |

**Architecture note (secondary, not in press release):** Multiple industry writeups describe a **three-model ensemble plus a dedicated bypasser classifier** post-Aug 2025. Turnitin's official language is vaguer: "enhanced AI writing detection capabilities" and training on "leading AI bypasser tools." Treat ensemble details as **inferred**, not vendor-confirmed.

---

## 2. Bypasser model (August 27, 2025)

### 2.1 What Turnitin claims

From the [Aug 27, 2025 press release](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers):

- Bypasser detection is **integrated into existing AI writing detection** — no extra integration, no third-party API.
- Targets text "intentionally modified by AI humanizer tools" to evade detection.
- CPO Annie Chechitelli frames humanizer vendors as a **new cheating-provider category**.
- **English only** for bypasser detection.
- Licensed via **Turnitin Originality** add-on or **iThenticate 2.0** AI capabilities.

From [release notes](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes):

> In the AI writing report, the category **'AI-generated only'** will now include AI-generated text that may have been modified by an AI bypasser tool.

Important UX detail: bypasser hits are **not labeled separately** in the report. They merge into "AI-generated only" (until Jul 2026 unified UI, when even that distinction disappears from highlights).

### 2.2 What Turnitin does *not* publish

| Metric | Status |
|--------|--------|
| Bypasser detection rate (recall on humanized text) | **Not published** |
| Bypasser false-positive rate | **Not published** |
| Training tool list | **Not published** ("leading bypassers") |
| Benchmark dataset | **Not published** |

[DetectionDrama analysis (2026)](https://detectiondrama.com/does-undetectable-ai-bypass-turnitin/) is correct: **the absence of data is the finding.** Academics (Blommerde) publicly asked for benchmark transparency; none released.

### 2.3 Mechanism (best available evidence)

| Layer | Description | Evidence tier |
|-------|-------------|---------------|
| **AIW-2** | Core LLM-output classifier | Turnitin whitepaper (Aug 2024) |
| **AIR-1** | Paraphrase / word-spinner detection (QuillBot-class) | Whitepaper; Jul 2024 report split |
| **Bypasser layer (2025+)** | Trained on humanizer outputs; catches modification signatures | Press release + release notes; architecture details from secondary sources |
| **Signals (secondary)** | Burstiness, lexical AI-ism clusters, paraphraser-pattern classifier | [HumanizeMy.ai analysis](https://humanizemy.ai/bypass-turnitin) — vendor-adjacent, treat as hypothesis |

Turnitin's Aug 2025 move is best read as **DAMAGE-class defense**: retrain on adversary outputs (humanizer text), not a new theoretical detector. Same arms-race pattern unslop Cat 05 documents for Originality.ai (~30-day patch cadence).

---

## 3. February 2026 retrain

From [AI writing detection model — 2026 release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model):

**Date:** February 12, 2026  
**Change:** "Updated our AI writing detection model to improve recall while maintaining a low false positive rate."  
**UI:** None.  
**Settings:** None required.  
**Retroactivity:** None. Resubmit to regenerate reports.

This is the **second post-bypasser refresh** (after Oct 14, 2025). Vendor pattern: several English model updates per year, each shifting the detection boundary without announcing what training data changed.

**Practical implication for humanizers:** Pre-Aug 2025 bypass rates are stale. Post-Aug 2025 rates are stale after each refresh. [docs/research/18-commercial-humanizer-tools/B-industry.md](../../docs/research/18-commercial-humanizer-tools/B-industry.md) documents StealthGPT Turnitin bypass collapsing ~79.7% → ~62% after Aug 2025 (independent tier **[I]**).

---

## 4. Unified UI (July 2026)

Two "unified" changes — don't conflate them.

### 4.1 Next Gen Feedback Studio (July 15, 2025)

[Blog post](https://www.turnitin.com/blog/unlocking-insights-whats-new-in-turnitin-feedback-studio): consolidated inbox, similarity + AI scores together, redesigned Similarity Report, platform rebuild for faster add-on shipping. LTI 1.3 and turnitin.com users.

### 4.2 Single blue highlight (July 20, 2026)

[Product updates](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates) + [blog](https://www.turnitin.com/blog/how-turnitin-is-simplifying-ai-detection-for-educators-and-publishers):

| Before | After |
|--------|-------|
| Blue = likely raw LLM | Single blue = **all** likely AI |
| Purple = likely AI-paraphrased / bypassed | Purple removed from UI |
| Two interactive categories in report | One unified indicator |

**Vendor stated goals:**

1. Reduce overinterpretation of tool-specific colors.
2. Lower risk of misconduct reviews based on purple-vs-blue distinctions.
3. Focus instructors on **whether** AI signal exists, not **which** tool path.

**What did NOT change:** Detection still runs on paraphrased and bypassed text. English only for this UI change. Auto-applied for Originality / iThenticate AI customers. Old reports keep two-color view until resubmission.

**Interpretation:** Turnitin is **de-escalating UI certainty** while **escalating model aggression** (bypasser training + Feb 2026 recall bump). The product is moving toward "conversation starter" framing — consistent with institutional skepticism below.

---

## 5. Official accuracy claims vs. independent evidence

### 5.1 Turnitin vendor claims

| Claim | Caveats (Turnitin's own docs) |
|-------|-------------------------------|
| Document FP rate **<1%** | Applies to scores **≥20%** only |
| Catches **~85%** of fully AI-generated text (internal testing) | Misses up to ~15% by design to hold FP down |
| Sentence-level error ~**4%** | Cited in third-party reads of vendor materials |
| 1–19% band suppressed as `*%` | Vendor acknowledges higher FP incidence in this band |
| Not sole basis for adverse action | [Model guide disclaimers](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) |

### 5.2 Independent tests

| Study / test | Turnitin finding | Notes | URL |
|--------------|------------------|-------|-----|
| **Blommerde (Northumbria), Sept 2025** | StealthGPT 72%, Groby 67%, GPT Human 31%, Easy Essay 0%, StealthWriter/Refrazy 1–19% | 6 tools, YouTube test; **not peer-reviewed** | [ETIH](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers); [DetectionDrama](https://detectiondrama.com/humanizers-that-beat-turnitin-bypasser-detection/) |
| **Jabarian & Imas (Chicago Booth), Sep 2025** | **Turnitin not tested** | Pangram ≈ robust to StealthGPT; GPTZero FNR ~50%+ on humanized; Originality FNR up to ~21% on short text | [BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf); [NBER WP 34223](https://www.nber.org/system/files/working_papers/w34223/w34223.pdf) |
| **Liang et al. 2023** | Not Turnitin-specific; GPT detectors broadly | 61.3% of TOEFL essays flagged vs 5.1% native | [Patterns / DOI 10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779) |
| **Washington Post (pre-launch)** | >50% FP on small human sample | Turnitin later said tool "not always reliable" | Via [Diglot](https://diglot.ai/blog/is-turnitin-ai-detection-accurate) |
| **Working Educators, 2025–26** | 15% overall FP; **31% ESL** vs 12% native | 150 essays, Philadelphia area; methodology differs from vendor | [Working Educators](https://workingeducators.org/turnitin) |
| **Peer-reviewed EFL study, 2026** | Turnitin accuracy **0.61** vs Originality **0.69**; poor on hybrid text | 192 texts; academic integrity journal | [Springer — Educational Integrity](https://link.springer.com/article/10.1007/s40979-026-00213-1) |
| **Commercial humanizer benchmarks (unslop Cat 18)** | Pre-Aug 2025 bypass numbers obsolete; StealthGPT ~62% post-update | Tier **[I]** independent | [B-industry.md](../../docs/research/18-commercial-humanizer-tools/B-industry.md) |

### 5.3 Correction for unslop internal docs

Current `skills/unslop/SKILL.md` states:

> Incorrect former repo copy: "Chicago Booth 2026 is the current reference benchmark … Turnitin drops to 60–85% accuracy on humanized text there." Booth did not test Turnitin.

**This is incorrect.** Booth tested **Pangram, Originality.ai, GPTZero, RoBERTa** — not Turnitin. The 60–85% figure appears in unslop Cat 05/18 as a **secondary-market aggregate** for edited AI text across detectors, not a Booth Turnitin datapoint. **Action:** Remove Booth attribution for Turnitin or cite Blommerde / Cat 18 tier **[I]** tests instead.

---

## 6. Educator and institutional sentiment

### 6.1 Institutional exits and caution

| Institution | Action | Date | Source |
|-------------|--------|------|--------|
| **Vanderbilt** | Disabled Turnitin AI detector | Aug 2023 | [Inside Higher Ed](https://www.insidehighered.com/news/tech-innovation/artificial-intelligence/2024/02/09/professors-proceed-caution-using-ai) |
| **UT Austin, Northwestern** | Disabled / discouraged | 2023–2024 | Same |
| **Curtin University** | **Disabled AI detection**; originality check remains | **Jan 1, 2026** | [Curtin announcement](https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/); [student page](https://www.curtin.edu.au/students/study-support/genai-use-at-curtin/) |
| **University of Twente** | Do not treat score as proof without investigation | 2026 guidance | [Thesify guide](https://www.thesify.ai/blog/how-professors-detect-ai-writing-2026-guide) |

Curtin framing: "trust and clarity," assessments "fair and relevant." Student guild guidance (2026): even without the detector, **AI paraphrase of your own writing is still misconduct**; process evidence (drafts, file metadata) substitutes for detector scores.

### 6.2 Academic critics of bypasser launch

Blommerde ([ETIH](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers)): skeptical of Turnitin's claim to distinguish raw / paraphrased / humanized; binary "AI generated" label loses nuance.

Mark A. Bassett (Charles Sturt), on Curtin's disable: "joining the growing list of providers that are abandoning this deeply flawed technology" ([ETIH on Curtin](https://www.edtechinnovationhub.com/news/curtin-university-to-disable-turnitin-ai-detection-tool-in-2026-as-debate-over-reliability-continues)).

[CASRAI 2026 litigation roundup](https://casrai.org/news/ai-detector-false-positive-controversies-2026): courts and universities "catching up to accuracy limitations researchers had already flagged."

### 6.3 Sentiment summary

| Stakeholder | 2025 | 2026 |
|-------------|------|------|
| Turnitin | Aggressive model updates; humanizer as "cheating providers" | UI simplification; de-emphasize tool-path certainty |
| Early-adopter instructors | Purple/blue as smoking gun | Growing guidance: score = weak signal only |
| Integrity offices | Detector-led workflows | Shift to declarations, draft history, Authorship-style provenance |
| ESL / non-native students | Disproportionate FP risk (Liang) | Curtin exit; Turnitin hides 1–19%; equity narrative still load-bearing |
| Humanizer vendors | "99% undetectable" marketing | Bypass rates crumbled for signature-trained tools (StealthGPT-class) |

---

## 7. Impact on humanizer market

Documented in [docs/research/18-commercial-humanizer-tools/B-industry.md](../../docs/research/18-commercial-humanizer-tools/B-industry.md):

| Tool | Pre-Aug 2025 Turnitin bypass | Post-Aug 2025 (independent) |
|------|------------------------------|-----------------------------|
| StealthGPT | ~79.7% bypass **[I]** | ~62%; Blommerde: 72% flagged |
| QuillBot Humanizer | Weak already | ~47% avg across detectors; Turnitin targets synonym-swap |
| Undetectable.ai | Market leader claims | **No conflict-free Turnitin test published** |
| Ryter Pro / Walter Writes | N/A (2025 entrants) | Claim 94–97% Turnitin in **[I]** tests — verify near submission |
| Easy Essay | N/A | 0% in Blommerde test — **single academic, small n** |

**Pattern:** Tools with **stable paraphraser signatures** (StealthGPT, Groby) got hit hardest. Tools outside training distribution may still score 0–19%. That is signature detection behavior, not proof any humanizer is "Turnitin-proof."

---

## 8. unslop honest positioning

### 8.1 What Turnitin 2025–2026 changes for unslop

| unslop claim | Still valid? | Notes |
|--------------|--------------|-------|
| Subtract AI-isms, add burstiness/contractions | **Yes** | Reduces distributional TV; aligned with Sadasivan framing (Agent #17) |
| Anti-detector for ESL false positives | **Yes** | Liang + Working Educators ESL FP data support this use case |
| "Beat Turnitin" / stable bypass | **No** | Feb 2026 retrain + bypasser training = month-scale decay |
| Optimize one detector score | **Weak** | `--detector-feedback` is secondary; ladder should reach anti-detector + cross-model rec |
| Chicago Booth proves Turnitin 60–85% drop | **No — fix copy** | Booth didn't test Turnitin |

### 8.2 Recommended messaging (August 2026)

> Turnitin retrained in August 2025 specifically on humanizer outputs, then again in February 2026. They publish no bypasser accuracy numbers. Instructors increasingly see one blue highlight, not a tool-specific verdict — but the score still isn't proof.
>
> unslop removes the statistical signatures that make LLM text detectably non-human: stock phrases, uniform rhythm, zero contractions, performative balance. That's voice and quality work — the same edits that reduce false positives for ESL writers. It is not a Turnitin guarantee.
>
> Anti-detector mode exists for **false-positive defense** and **register restoration**. If you need maximum separation from detector fingerprints, run a **cross-model second pass** (Claude ↔ GPT ↔ Gemini) after unslop — the skill can't do that alone.

### 8.3 Boundaries (unchanged, now more load-bearing)

From `skills/unslop/SKILL.md`:

- Anti-detector mode: **defensive** (ESL false positives, resume writers) — **not academic misconduct tooling**.
- Never fabricate facts to satisfy anti-detector mode.
- Detector evasion is not durable if verifier has generation logs (retrieval defenses).

### 8.4 Code / doc actions for UPDATE-PLAN

1. **SKILL.md landscape paragraph:** Keep Aug 2025 bypasser + Feb 2026 refresh; **remove** "Turnitin drops to 60–85% at Chicago Booth." Replace with: "Booth (2025) did not test Turnitin; Blommerde (2025) and Cat 18 **[I]** benchmarks show tool-specific, unstable results post-bypasser."
2. **README anti-detector section:** Name Turnitin bypasser explicitly; link Curtin disable as institutional counter-signal.
3. **`--detector-feedback` ladder:** Wire `anti-detector` mode (per UPDATE-PLAN-2026-08).
4. **Benchmark honesty:** Any Turnitin row in `drafts/2026-05-detector-test/` must note model version date and resubmission requirement.

---

## 9. Open questions

1. **Which humanizers are in Turnitin's bypasser training set?** Vendor silent. Blommerde's hit/miss split suggests incomplete coverage.
2. **Feb 2026 recall bump magnitude?** No public A/B. Humanizer vendors claim 35–40% detection increase post-Aug 2025 ([HumanLike blog](https://humanlike.pro/blog/turnitin-august-2025-bypass-detector-update) — vendor-adjacent, **[V]** tier).
3. **Does unified UI precede policy softening?** Jul 2026 UI change correlates with Curtin-style exits — possible vendor response to institutional pushback.
4. **Multilingual gap:** Bypasser + paraphrase detection English-only; Spanish/Japanese get LLM detection only. ESL equity story persists for non-English submissions.
5. **Authorship / Clarity pivot:** Turnitin investing in **process provenance** (Clarity drafts, Authorship keystroke data) while de-emphasizing classifier certainty — long-term threat to pure humanizer market.

---

## 10. URL index

### Turnitin official

- [Press: AI bypasser detection (Aug 27, 2025)](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers)
- [PR Newswire mirror](https://www.prnewswire.com/news-releases/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers-302539461.html)
- [AI writing detection model + release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model)
- [Turnitin release notes (product changelog)](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes)
- [Product updates (Jul 2026 unified UI)](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates)
- [Blog: Simplifying AI detection (unified blue)](https://www.turnitin.com/blog/how-turnitin-is-simplifying-ai-detection-for-educators-and-publishers)
- [Blog: Next Gen Feedback Studio](https://www.turnitin.com/blog/unlocking-insights-whats-new-in-turnitin-feedback-studio)
- [Next Gen Feedback Studio resource center](https://guides.turnitin.com/hc/en-us/articles/34876874513421-Next-Generation-of-Turnitin-Feedback-Studio-Resource-Center)
- [AI writing detection whitepaper (AIW-2 / AIR-1)](https://www.scribd.com/document/988214788/TII-AI-HE-AIWritingDetectionModel-Whitepaper-US-0924-1)

### Independent tests and academic

- [Jabarian & Imas — BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)
- [NBER WP 34223](https://www.nber.org/system/files/working_papers/w34223/w34223.pdf)
- [Chicago Booth Review summary](https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust)
- [Liang et al. 2023 — GPT detectors biased against non-native writers](https://doi.org/10.1016/j.patter.2023.100779)
- [EFL detector study — Turnitin vs Originality (2026)](https://link.springer.com/article/10.1007/s40979-026-00213-1)
- [Blommerde / ETIH coverage](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers)
- [DetectionDrama — humanizer test table](https://detectiondrama.com/humanizers-that-beat-turnitin-bypasser-detection/)
- [DetectionDrama — Undetectable.ai evidence gap](https://detectiondrama.com/does-undetectable-ai-bypass-turnitin/)
- [Working Educators — Turnitin FP test](https://workingeducators.org/turnitin)
- [LogAI — false positives / vendor disclaimers](https://www.logai.com.au/blog/turnitin-ai-false-positives)
- [Diglot — accuracy research roundup](https://diglot.ai/blog/is-turnitin-ai-detection-accurate)
- [CASRAI — 2026 FP controversies / Curtin](https://casrai.org/news/ai-detector-false-positive-controversies-2026)

### Institutional policy

- [Curtin — disable AI detection (Jan 2026)](https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/)
- [Curtin — GenAI student guidance](https://www.curtin.edu.au/students/study-support/genai-use-at-curtin/)
- [Inside Higher Ed — professors proceed with caution](https://www.insidehighered.com/news/tech-innovation/artificial-intelligence/2024/02/09/professors-proceed-caution-using-ai)

### Industry / secondary (tier **[I]** or **[V]** — verify before citing as fact)

- [IT Brief — Aug 2025 bypasser launch](https://itbrief.news/story/turnitin-updates-tool-to-detect-ai-bypassers-humanised-text)
- [WibbleAI — Turnitin chronology](https://www.wibbleai.com/blog/can-turnitin-detect-humanized-ai-text)
- [HumanLike — post-Aug 2025 impact claims](https://humanlike.pro/blog/turnitin-august-2025-bypass-detector-update)
- [unslop Cat 18 — commercial humanizer benchmarks](../../docs/research/18-commercial-humanizer-tools/B-industry.md)

### unslop internal

- [Agent #17 — Sadasivan impossibility](./AGENT-17-SADASIVAN-IMPOSSIBILITY.md)
- [UPDATE-PLAN-2026-08](./UPDATE-PLAN-2026-08.md)
- [skills/unslop/SKILL.md](../../skills/unslop/SKILL.md) — anti-detector procedure
- [docs/research/05-ai-text-detection-and-evasion/SYNTHESIS.md](../../docs/research/05-ai-text-detection-and-evasion/SYNTHESIS.md)

---

## 11. Evidence tier key

| Tier | Meaning |
|------|---------|
| **[F]** | Turnitin first-party (press, guides, release notes) |
| **[A]** | Peer-reviewed / working paper (Booth, Liang, Springer 2026) |
| **[I]** | Independent test with named methodology (Blommerde, Working Educators, Cat 18) |
| **[V]** | Vendor or vendor-adjacent (HumanLike, humanizer blogs) |
| **[P]** | Press / aggregator (ETIH, IT Brief, DetectionDrama) |

---

*Agent #56 complete. Cross-ref: Agent #66 (Turnitin bypasser category deep-dive) pending; Agent #17 (Sadasivan TV bound) load-bearing for unslop positioning.*
