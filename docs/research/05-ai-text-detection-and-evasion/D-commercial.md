# Commercial Products & Services — AI Text Detection & Evasion

**Research value: high** — The detector ↔ humanizer market is a mature, fast-moving arms race with a clear price band, converging technique stack, and measurable performance gaps that directly inform positioning for a new humanizer product.

Scope: 9 detectors + 9 humanizers = **18 products** profiled. Pricing and claims are as of Q1–Q2 2026 per vendor pages and independent 2026 reviews; figures older than 12 months were re-verified where possible.

---

## AI Text Detectors

### 1. GPTZero
- **Positioning / Origin**: Built Dec 2022 by Princeton undergrad Edward Tian as a senior thesis; the one major detector whose "built for educators" framing is original, not retrofit. ~$20M ARR mid-2025, 380K+ teacher users. [3][15]
- **Pricing**: Free tier 10K words/mo; paid from ~$10/mo (annual) up through classroom/institution tiers. [1][3]
- **Claimed performance**: Version 4.1b: 99.39% overall accuracy, 98.78% recall, 0.00% FPR on own 2026 benchmark (1,000 human + 1,000 AI texts). Chicago Booth 2026 (third-party): 99.3% recall at 0.1% FPR — now the most-cited external benchmark replacing Scribbr's 2024 ranking. Independent real-world testing (MPG ONE, 2026): 88–95% on raw AI text, drops to 60–80% on paraphrased/edited content. [1][21]
- **Underlying technique**: Perplexity + burstiness as baseline, now layered with fine-tuned classifiers, writing-process replay, and a humanizer-awareness layer that maintains a greylist of known bypass methods and patches within days. [1][15][17][23]
- **Marketing frame**: "#1 AI detector for teachers" and "most accurate commercial AI detector" per Chicago Booth 2026. Humanizer-aware detection is now an explicit product line (Jan 2026 post). Shifted post-2025 toward "responsible classroom AI use" rather than pure catch-the-cheater. [15]

### 2. Originality.ai
- **Positioning**: Built for SEO agencies / publishers; no free tier, sells on enterprise credibility. [2]
- **Pricing**: Pro $12.95/mo annual ($14.95 monthly), 2,000 credits (1 credit = 100 words); Enterprise $136.58/mo; pay-as-you-go $30 for 3,000 credits. [2]
- **Claimed performance**: Three model variants as of early 2026: Lite (fastest, 0.5% claimed FP), Turbo (97% on humanized AI at 1.5% FP), Academic (92% accuracy, <1% FP). November 2025 independent study: 96% accuracy, lowest FP of all commercial tools tested. January 2026 study: 100% across ChatGPT, DeepSeek, Gemini, Grok, and human texts. Consistently the detector humanizers fail against most often — referenced as the "benchmark to beat" by multiple humanizer products. [1][2][5]
- **Underlying technique**: Fine-tuned transformer classifiers, explicitly retrained monthly against humanizer corpora. Lite 1.0.1 (June 2025) added humanizer-resistance capabilities; Lite 1.0.2 / Turbo 3.0.2 / Academic 0.0.5 (September 2025) further tightened against latest humanizer tools. Bundled plagiarism, readability, fact-check, and now also an AI humanizer tool on the same platform. [2][5]
- **Marketing frame**: "99% accuracy in detecting AI" and "most accurate on RAID adversarial benchmark." Ranked #1 in UPenn/CMU RAID study, winning 9 of 11 adversarial attack tests. [2]

### 3. Copyleaks
- **Positioning**: Multilingual + code plagiarism incumbent; sells the combined AI+plagiarism+code report as one product. [4]
- **Pricing**: Personal $13.99/mo annual (~$16.99 monthly); Pro $74.99/mo annual; Enterprise custom; 10-page free trial. API priced separately. [4]
- **Claimed performance**: "99%+ accuracy across mixed content, 1–2% FP"; 93% on English, falling to 74–84% on Chinese/Japanese/Arabic. Overall multilingual 91%, 7.2% English FP in independent tests. [4][1]
- **Underlying technique**: "AI Logic" — classifier with explanation layer that surfaces specific flagged phrases; mixed-content segmentation; "text manipulation" detection targeting humanizers. [4]
- **Marketing frame**: "Catches AI text manipulation" — explicit anti-humanizer positioning. [4]

### 4. Turnitin
- **Positioning**: Institutional standard bundled into university LMS contracts; not sold per-seat to consumers. [1]
- **Pricing**: Institutional only; effectively "included" from the student's view. [1]
- **Claimed performance**: "98% accuracy, <1% FP on submissions >300 words." Independent 2025–2026 testing: 92–100% on raw AI text; drops to 60–85% on manually edited or paraphrased content; 70–80% on AI text with minor human edits (University of Chicago Booth data, late 2025). Stanford HAI study: non-native English misclassified 2–5× more often than native English, up to 32% of non-native essays flagged. [1][6]
- **Underlying technique**: Proprietary classifier fine-tuned on academic corpora; April 2025 update added Japanese-language detection. 2026 model targets "AI humanizer tool" outputs specifically. October 2025 update softened verdicts and hid 1–19% scores by default due to false-positive incidence. [1][6]
- **Marketing frame**: Quiet, institutional — rare public marketing quotes; trust comes from LMS integration. Roadmap for 2026 includes explicit humanizer-resistant detection layer.

### 5. Winston AI
- **Positioning**: Consumer-facing detector bundled with AI image/deepfake detection and plagiarism; pushes "HUMN-1" website certification badge. [5]
- **Pricing**: 14-day trial (2,000 credits); Essential $10–18/mo, Advanced $16–29/mo, Elite $26–49/mo. Credits: 1/word text, 2/word plagiarism, 200–500/image. [5]
- **Claimed performance**: "99.98% accuracy." Independent RAID benchmark (ACL 2024) shows 71% at 5% FP; third-party 2026 tests: 76.3% overall, 66% on Claude 3.5, 59% on creative writing, ~10% FP. [5]
- **Underlying technique**: Sentence-level classifier + OCR pipeline for scanned documents/handwriting. [5]
- **Marketing frame**: "99.98% accuracy" is the entire pitch — the single most aggressive accuracy claim in the market. [5]

### 6. Sapling
- **Positioning**: Developer-first; API-priced; lightweight consumer UI. [6]
- **Pricing**: Free 2,000 chars/scan; Pro $25/mo for 8,000 chars/scan; API $0.005 per 1,000 chars. [6]
- **Claimed performance**: "97%+ accuracy." Independent: 99.5% AI-detection but 35% FP; one peer-reviewed study found 90% FP on human text; Scribbr pegs it at 68% overall; 2.4★ Trustpilot. [6]
- **Underlying technique**: Classifier on top of Sapling's existing grammar/writing-assistant stack.
- **Marketing frame**: Positioned as "fast, API-first AI detection" — lighter marketing voice than Originality/Winston. [6]

### 7. ZeroGPT
- **Positioning**: Free-tier consumer tool; ad-supported web product with freemium upsell. [7]
- **Pricing**: Free; paid tiers exist for longer inputs and API.
- **Claimed performance**: 2026 benchmark across 150 samples, 8 detectors: 71% overall, 84% AI-detection, 74% human-detection, 26% FP, 52% on mixed text. [7]
- **Underlying technique**: Perplexity-based with a proprietary "DeepAnalyse" label; consistency high (87%) but mixed-content accuracy low. [7]
- **Marketing frame**: "Most advanced AI detector" — heavy on bold percentage claims with little supporting method detail. [7]

### 8. Writer.com detector
- **Positioning**: Bundled inside Writer's enterprise writing platform; detector is a free lead-magnet for the broader platform, not a standalone product. [8]
- **Pricing**: Free public tool; Writer platform pricing (Team/Enterprise) starts in the hundreds/month per seat.
- **Claimed performance**: Vendor marketing only ("built for enterprise content teams"); independent testing in 2026 has largely stopped including Writer's detector because accuracy lags peers by wide margin.
- **Underlying technique**: Classifier trained on Writer's content-ops corpus; effectively deprecated as a standalone.
- **Marketing frame**: De-emphasized — Writer pivoted messaging toward agentic enterprise writing workflows, leaving the detector as a residual funnel asset. [8]

### 9. Grammarly Authorship
- **Positioning**: Explicitly *not* a detector in 2026 — rebranded as "Authorship," a provenance/attribution tool. [9]
- **Pricing**: Included in Grammarly Premium / Business tiers.
- **Claimed performance**: Avoids accuracy claims; Grammarly publicly argues detection is "not conclusive" and can misfire on repetitive phrasing or non-native English. [9]
- **Underlying technique**: Real-time keystroke/paste tracking inside Google Docs + Word, color-coded sentence attribution, process replay, citation generation. Closer to Git blame for prose than classifier-based detection. [9]
- **Marketing frame**: "From AI detection to authorship" — the first major vendor to openly concede classifier-based detection is the wrong framing. [9]

---

## Humanizers / Evasion Tools

### 10. Undetectable.ai
- **Pricing**: $19/mo for 10K words → $199.50/mo for 1M words; 250-word free trial. [10]
- **Claimed performance**: 96% AI → human against GPTZero in 2026 head-to-head, beating WriteHuman, BypassGPT, StealthGPT (all scored 100% AI in same test). Independent 2026 testing: 87–88% average bypass rate across Turnitin, GPTZero, Copyleaks, Originality.ai — strong but fails to consistently pass all detectors simultaneously. 22M+ users as of 2026 (up from 15M in Feb 2025 per Reuters). [10]
- **Underlying technique**: NLP pipeline that restructures sentences, adjusts vocabulary, calibrates tone by selectable mode (University, Journalist, Marketing, etc.); three stealth-intensity levels; bundled TruthScan detector; 50+ languages; Chrome + Zapier + API. [10]
- **Marketing frame**: "Undetectable by *any* AI detector" — positions as category leader and prices accordingly. The 22M user milestone makes it the most widely used humanizer by a significant margin.

### 11. Humanize AI Pro / Humanize AI
- **Pricing**: Core web tool **$0/mo, unlimited, no signup** (ad + upsell model). Sister product `humanizeai.io` runs $4/mo intro → $20/mo annual for 600K words/yr. [11][13]
- **Claimed performance**: "99.8% bypass rate" across Turnitin, GPTZero, Originality, Copyleaks, Winston, Sapling, ZeroGPT. [11]
- **Underlying technique**: Rewriter with intensity levels; leverages the category-standard sentence-restructure + vocabulary-swap + burstiness injection stack.
- **Marketing frame**: "Free forever, highest bypass rate" — disrupts the $10–20/mo band by giving the core product away.

### 12. StealthGPT
- **Pricing**: $32/mo (billed weekly) or $40/mo; optional "Samurai Engine" +$4.99/mo. [12]
- **Claimed performance**: 2026 tests: strong against Turnitin (22% AI), GPTZero (18%), ZeroGPT (15%); **fails against Originality.ai (35% AI, still flagged)**. [12]
- **Underlying technique**: Multiple "engines" — standard (speed) vs. quality-optimized; Chrome extension for in-place rewriting; built-in checker. [12]
- **Marketing frame**: "Military-grade stealth" + "Samurai Engine" — leans hard on branded mode names rather than technical detail.

### 13. BypassGPT
- **Pricing**: ~$7.99/mo entry; 300-word free sample; ~$0.80 per 1K words. [11][10]
- **Claimed performance**: Vendor claims broad bypass; independent 2026 head-to-head vs Undetectable.ai: only 17% detector-pass rate (1/6), vs Undetectable's 83%. [10]
- **Underlying technique**: Three modes (Fast, Creative, Enhanced); 50+ languages; built-in 7-detector dashboard (lets users pre-check before submitting). [10]
- **Marketing frame**: "Bypass any AI detector" — aggressive naming, middling independent results.

### 14. Phrasly
- **Pricing**: Free (550 humanizer words + 6K generator); "Unlimited" paid plan w/ 45% annual discount. [13]
- **Claimed performance**: "99.7% average human score across 100,000+ documents." [13]
- **Underlying technique**: **Claims proprietary models trained on 1M+ pages of human writing** — explicit differentiation from competitors reselling third-party LLMs. Three intensity levels (Easy, Medium, Aggressive) + content generator with live citation verification. [13]
- **Marketing frame**: "Our own models, not a wrapper" — the only humanizer that markets on training-data provenance. 2M+ users, 4M projects cited.

### 15. HIX Bypass
- **Pricing**: Standard $14.99/mo ($9.99 annual) 5K words; Premium $29.99/mo ($14.99 annual) 50K; Unlimited $59.99/mo ($39.99 annual). 300-word free tier with 125-word per-request cap. [14]
- **Claimed performance**: Third-party 89.3% bypass rate; vendor claims higher. [11]
- **Underlying technique**: Four modes — **Fast, Balanced, Aggressive, and "Latest" (explicitly tuned against Originality 3.0 and Turnitin's newest models)**; document upload (DOC/DOCX/PDF/TXT); 50+ languages. [14]
- **Marketing frame**: "Bypass any AI detector" — but uniquely advertises detector-version-specific tuning, signalling fast iteration cycles.

### 16. Surfer (AI Humanizer)
- **Positioning**: Humanizer as a **feature inside the Surfer SEO suite**, not a standalone; aimed at SEO teams worried about Google's "scaled content abuse" policy. [16]
- **Pricing**: Free tool tier; paid tier with 50K words + unlimited AI detection bundled into Surfer subscription.
- **Claimed performance**: Vendor-only claims; no independent benchmark in the 2026 head-to-heads.
- **Underlying technique**: Rewriter + **custom-voice training** (teach the humanizer your style) + humanizer/detector API for workflow automation; Zapier integration. [16]
- **Marketing frame**: "Humanize for Google, not just for detectors" — only major humanizer explicitly tying value to SEO ranking, not cheating.

### 17. WriteHuman
- **Pricing**: From $12/mo; 200 words/check free tier; ~$0.80 per 1K words. [11]
- **Claimed performance**: Third-party 86.8% bypass rate; loses head-to-heads to Undetectable.ai. [11]
- **Underlying technique**: Standard rewrite-and-reshape pipeline; simple consumer UX.
- **Marketing frame**: "Remove AI detection, retain your voice" — consumer-friendly rather than adversarial tone.

### 18. AIHumanize (aihumanize.com) / aihumanize.co
- **Pricing**: Basic 5K words/mo, 500-word per-request cap; Premium/Unlimited required to pass Turnitin; API on higher tiers. Sister `aihumanize.co` offers instant free tool w/ upsell. [14]
- **Claimed performance**: **99.8% pass rate vs Turnitin**, 1.28B words/month processed, 2.8M+ users, **credit-back guarantee if flagged as AI**. [14]
- **Underlying technique**: Rewriter + seven-detector pre-check; grammar/flow + SEO polish bolted on. [14]
- **Marketing frame**: The only tool in the set offering an explicit **money-back-if-detected guarantee** — converts the detection risk into a vendor problem.

---

## Patterns, Trends, Gaps

**1. Converging technique stack.** Detectors all layer (a) perplexity + burstiness, (b) stylometric features (lexical diversity, readability), and (c) a fine-tuned transformer classifier. [17] Humanizers all layer (a) sentence-structure reshuffling, (b) vocabulary substitution, (c) deliberate burstiness injection, and (d) tone/persona modes. Technical differentiation is narrowing fast — the real differentiation now lives in brand trust, pricing, and integrations.

**2. "99%" is a marketing primitive, not a fact.** Every detector and most humanizers cluster around a 97–99.8% claim. Independent 2026 benchmarks show: GPTZero 88–95% (raw), 60–80% (humanized); Originality 96% (most consistent); Turnitin 92–100% (raw), 60–85% (edited). Humanizer bypass rates: Undetectable.ai 87–88%; BypassGPT 67%; QuillBot alone 34%. Claims cluster at 99% regardless of actual measured performance. [1][5][6][7][11][21]

**3. Detector vendors are the #1 use-case for humanizer vendors.** Multiple humanizers (Undetectable.ai, Phrasly, BypassGPT, HIX Bypass, AIHumanize) **ship their own built-in detector dashboards** so users can pre-check against 6–7 detectors before submitting. The arms race is now co-located inside each humanizer's UI.

**4. Originality.ai is the benchmark to beat.** Across independent humanizer tests, Originality.ai is the detector humanizers most consistently fail against (StealthGPT 35% AI, multiple tools flagged). HIX Bypass's "Latest Mode" advertises explicit tuning against "Originality 3.0." This makes Originality the *de facto* reference adversary in the market.

**5. Pricing has bifurcated into three tiers.**
   - **Free / $0** — Humanize AI Pro, Surfer's free tier, ZeroGPT, Grammarly Authorship (bundled).
   - **$10–20/mo consumer** — GPTZero, Originality Pro, Copyleaks Personal, Winston Essential, BypassGPT, WriteHuman, HIX Standard, Phrasly Unlimited, Humanize AI.
   - **$40–200/mo pro / enterprise** — Undetectable.ai scale tiers, Originality Enterprise, Copyleaks Pro, HIX Unlimited, StealthGPT.
   The $20–40/mo band is conspicuously thin — products either disrupt below or scale above.

**6. The "authorship" pivot.** Grammarly's 2025–2026 rebrand from "AI detector" to "Authorship" (provenance via keystroke tracking) is the first major vendor to concede classifier-based detection is a losing long-term bet. This is the clearest strategic signal that the detection side of the arms race is structurally weakening.

**7. EU regulatory watermarking deadline is an unpriced event.** The EU AI Act Article 50 transparency obligations become binding in August 2026 for all generative AI providers, requiring machine-readable marking of AI-generated text. No commercial detector or humanizer has updated positioning to account for a mandatory-watermarking landscape. This is the most significant structural change to the market in 2026.

**8. Under-served gaps.**
   - **Multilingual humanization quality** — detectors publicly admit 74–84% accuracy on non-English; Turnitin added Japanese detection in April 2025 but humanizers claim 50+ languages while publishing no non-English quality benchmarks.
   - **Long-form coherence after humanization** — every independent reviewer flags meaning drift, fact corruption, and awkward phrasing; no tool markets "we preserve semantics" as a headline claim.
   - **Auditability / provenance for the writer's side** — Grammarly Authorship is the only product in this space. The symmetric opportunity (a tool that *proves* human authorship to a reader/grader, decoupled from detection) is effectively uncontested.
   - **Academic-aware humanization** — Originality launched an "Academic" detector model (September 2025); no humanizer has launched a matched "Academic" mode trained to preserve citation integrity and disciplinary tone.
   - **Enterprise/compliance angle** — almost all humanizer marketing is consumer/student-facing; none have built a B2B narrative around compliance-friendly "voice normalization" (e.g. legal, medical) even though the underlying tech fits.
   - **SIRA-capable SynthID bypass** — SIRA's ~100% watermark removal at commodity cost is publicly available (ICML 2025, GitHub). No commercial humanizer has incorporated it, creating a first-mover opportunity in a market where Gemini is the dominant consumer AI output source.

**8. Guarantee-as-marketing is emerging.** AIHumanize's "credit-back if detected" is the clearest sign humanizers are commoditizing and must compete on risk-transfer rather than raw performance. Expect this to spread.

---

## Sources

1. Axis Intelligence, *Best AI Detectors 2026: 10 Tools Tested* — cross-detector accuracy/FP benchmark.
2. Originality.ai — pricing page and "99% Accuracy" benchmark post (Turbo 3.0.2 / Lite / Academic models).
3. GPTZero.me + Business Insider — origin story, Princeton/Tian, educator focus.
4. Copyleaks — pricing, API docs, multilingual accuracy breakdown.
5. gowinston.ai + RAID (ACL 2024) + SupWriter 2026 review — Winston claimed vs. measured accuracy.
6. Sapling — pricing + Scribbr / peer-reviewed FP studies.
7. SupWriter, *Are AI Detectors Accurate? 8 Tools Tested* — ZeroGPT benchmark.
8. Writer.com — public AI detector tool (residual funnel asset).
9. Grammarly — "From AI Detection to Authorship" + Authorship product page.
10. UndetectedGPT + AIXRadar — Undetectable.ai vs. StealthGPT vs. BypassGPT head-to-heads.
11. TheHumanizeAI.pro — 2026 humanizer pricing/bypass-rate comparison table.
12. UndetectedGPT, *StealthGPT Review 2026*.
13. Phrasly.ai — pricing + custom-model claim; independent review.
14. HIX Bypass pricing + aihumanize.com feature pages.
15. Observer, *GPTZero Shifts Focus to Responsible Classroom A.I.* (Aug 2025) + GPTZero educators page.
16. surferseo.com/ai-humanizer + changelog (custom voice, API).
17. dev.to / Stack Junkie / UndetectedGPT — explainers on perplexity, burstiness, stylometry, watermarking, DetectGPT.
18. Cybernews, *Undetectable AI review April 2026* — https://cybernews.com/ai-tools/undetectable-ai-review/
19. GPTZero, *GPTZero Tops Accuracy on Chicago Booth Benchmark in 2026* — https://gptzero.me/news/chicago-booth-2026/
20. MPG ONE, *Is GPTZero Accurate? Our 2026 Test Results* — https://mpgone.com/is-gptzero-accurate-our-2025-test-results-here/
21. BestHumanize, *Are AI Detectors Accurate in 2026? Independent Data* — https://besthumanize.com/blog/are-ai-detectors-accurate-in-2026-independent-data
22. Turnitin, *AI Detector Roadmap: Features Coming in 2026* — https://turnitin.app/blog/Turnitin-AI-Detector-Roadmap-Features-Coming-in-2026.html
23. GPTZero, *Detecting AI-Humanized Text: How GPTZero Stays Ahead* (Jan 2026) — https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/
