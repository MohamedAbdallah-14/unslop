# Agent #58 — Originality.ai 3.0 + AI Allowance

**Topic:** Originality.ai Turbo 3.0.x model line, September 2025 humanizer-resistant retraining, and July 2026 AI Allowance threshold detection  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh and May 2026 bench protocol

---

## Executive summary

Originality.ai is the **de facto hardest commercial detector** in independent humanizer tests. HIX Bypass advertises explicit tuning against "Originality 3.0." Practitioner bypass surveys consistently rank **Originality > GPTZero ≈ Turnitin > Copyleaks** for evasion difficulty.

The product has two distinct detection modes as of mid-2026:

1. **Classic binary models** (Lite 1.0.2, Turbo 3.0.2, Academic 0.0.5) — "Is this AI or human?"
2. **AI Allowance** (July 2026) — "Does AI usage exceed my policy threshold?" at 0%, 5%, 15%, 25%, or 40%

**Turbo 3.0.2** is the humanizer-hunting variant: vendor claims 99%+ on raw flagship LLM output, up to **97% on humanizer/bypasser corpora**, 1.5% FPR. **Lite 1.0.2** trades recall for lower FPR (0.5%). **Academic 0.0.5** targets STEM/code/formula content with <1% FPR but only ~92% on humanizers.

**AI Allowance** reframes detection for hybrid workflows. It estimates *how much* of a document is AI-derived, then compares against a user-selected ceiling. Vendor claims **99.4% accuracy at 15% allowance** on a 456,872-sample Benchmark V6 slice — but that number peaks at 15% because V6 labels are binary ("any AI = AI"), not because 15% is objectively optimal. A separate **167,980-sample Threshold Benchmark** where labels flip by threshold shows **96.53% at 5% allowance**.

For unslop:

- **Tier 1 bench detector** — already in `drafts/2026-05-detector-test/PROTOCOL.md` as detector #2.
- **Anti-detector mode reference adversary** — lexical cleanup alone won't pass Turbo; cross-model second pass is the documented lever.
- **Bench must log model + mode** — "Originality 3.0.2 Turbo" vs "AI Allowance 15%" produce different verdicts on Grammarly-polished human text.
- **Honest partial-fail story** — aidetector.ac (2026) shows Originality drops from **91% → 67%** on humanized content; vendor's own humanizer table shows Undetectable.ai still evades Turbo **8% of the time**.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Product home / free checker** | https://originality.ai/ |
| **Free AI checker (2,000 words, 3 scans/day)** | https://originality.ai/ai-checker |
| **Accuracy study hub (model history, confusion matrices, third-party table)** | https://originality.ai/blog/ai-accuracy |
| **AI Allowance launch (July 2026)** | https://originality.ai/blog/introducing-ai-allowance |
| **Model selection guide (Lite vs Turbo vs Academic vs Multilingual)** | https://originality.ai/blog/which-ai-detection-model-to-use |
| **2025 year in review (Sep 2025 model launch recap)** | https://originality.ai/blog/year-in-review-2025 |
| **RAID benchmark blog (Originality #1, 96.7% paraphrase)** | https://originality.ai/blog/robust-ai-detection-study-raid |
| **RAID paper (ACL 2024)** | https://arxiv.org/abs/2405.07940 |
| **RAID dataset / code** | https://github.com/liamdugan/raid |
| **RAID benchmark site** | https://raid-bench.xyz |
| **PeerJ scholarly-publication study (Lite 98.61%, Turbo 97.69%)** | https://originality.ai/blog/ai-detection-scholarly-publications-study |
| **PeerJ paper (accuracy-bias trade-offs)** | https://peerj.com/articles/cs-1234/ *(verify DOI at publication)* |
| **Turnitin similarity study (40% AI Allowance closest match)** | https://originality.ai/blog/what-ai-detector-similar-turnitin |
| **Turnitin comparison review** | https://originality.ai/blog/turnitin-review-originality-comparison |
| **ESL bias response (Stanford 2023 rebuttal)** | https://originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers |
| **Pricing** | https://originality.ai/pricing |
| **Enterprise / API** | https://originality.ai/enterprise |
| **Credit mechanics** | https://help.originality.ai/en/article/how-many-words-does-a-credit-scan-1uwp6dq/ |
| **Patent / BERT architecture note** | https://originality.ai/blog/patented-breakthrough-technology *(U.S. Patent No. 12,253,988 cited on homepage)* |
| **Gemini 3.7 Flash detectability (Aug 2026 vendor test)** | https://originality.ai/blog/is-gemini-3-7-flash-detectable |

### Independent / adversarial sources

| Resource | URL |
|----------|-----|
| **aidetector.ac Q1 2026 benchmark (91% raw → 67% humanized)** | https://aidetector.ac/accuracy/ |
| **Plainview StealthWriter vs Turbo 3.0.2 test (Dec 2025–Jan 2026)** | https://plainviewblog.com/can-you-still-bypass-originality-ai-in-2026-testing-stealthwriter-vs-turbo-3-0 |
| **Liang et al. ESL false-positive study (GPTZero, Originality, Crossplag >50% TOEFL)** | https://arxiv.org/abs/2304.02819 |
| **DAMAGE humanizer audit (COLING 2025)** | https://arxiv.org/abs/2501.03437 |
| **Chicago Booth detector working paper** | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| **FTC Content at Scale / BrandWell 98% claim enforcement (2025)** | https://www.ftc.gov/news-events/news/press-releases/2025/03/ftc-takes-action-against-company-that-claimed-its-ai-detection-tool-was-98-percent-accurate |

---

## Model lineage: what "3.0" means

Originality uses version numbers per model family, not a single product semver. The "3.0" line refers to **Turbo**, the zero-tolerance / anti-bypasser tier.

| Model | Released | Claimed accuracy | Claimed FPR | Humanizer resistance | Primary use case |
|-------|----------|------------------|-------------|---------------------|------------------|
| **Lite 1.0.2** | Sep 2025 | 99% | 0.5% | Moderate (80–87% on named humanizers) | Light AI editing OK (Grammarly grammar/spelling) |
| **Turbo 3.0.2** | Sep 2025 | 99%+ | 1.5% | Strong (90–97% on named humanizers) | Zero-tolerance / bypasser hunting |
| **Academic 0.0.5** | Sep 2025 | 99%+ | <1% | Moderate (82–92% on named humanizers) | STEM, code, formulas, education |
| **Multilingual 2.0.0** | May 2025 | 97.8% | 2.4% | Not published per-humanizer | 30 languages |
| **AI Allowance** | Jul 2026 | Threshold-dependent (see below) | Threshold-dependent | Same underlying stack; policy-gated verdict | Hybrid human+AI workflows |

### Turbo version history (relevant to stale citations)

| Version | Date | Notes |
|---------|------|-------|
| 3.0 Turbo | Feb 2024 | 98.8% on toughest internal set; Grok, Mixtral, GPT-4 Turbo, Gemini, Claude 2 |
| 3.0.1 Turbo | Oct 2024 | 99%+ claimed; "extremely challenging to bypass" |
| **3.0.2 Turbo** | Sep 2025 | Current; explicit humanizer/bypasser retraining; 97% humanizer claim |

Pre-Sep 2025 bypass numbers are **stale**. Pre-Aug 2025 humanizer marketing against "Originality" often targeted 3.0.1 or earlier.

### Underlying technique (vendor-disclosed)

- **Fine-tuned transformer classifier** — homepage cites modified BERT within patented text-analysis system (U.S. Patent No. 12,253,988).
- **Supervised learning** on curated human vs AI corpora; vendor emphasizes **web/marketing content** training bias (explicitly *not* academic-paper optimized until Academic model).
- **Red team / blue team** internal loop — monthly-ish retraining against humanizer corpora (vendor blog cadence: Lite 1.0.1 Jun 2025 added humanizer resistance; 1.0.2 / 3.0.2 / Academic Sep 2025 tightened further).
- **Feature families mentioned in accuracy post:** burstiness, perplexity, frequency, readability, punctuation — but primary product is classifier-based, not pure perplexity like GPTZero/ZeroGPT.

---

## AI Allowance — mechanism and interpretation

### Problem statement

Binary "AI vs human" breaks down when:

- Writers use Grammarly/QuillBot for polish
- Agencies permit "AI-assisted" outlines or paragraph expansion
- Schools debate acceptable AI editing levels

AI Allowance shifts the question from **classification** to **policy compliance**.

### How it works (vendor model)

1. Model estimates **AI fraction** of document (continuous, not just binary).
2. User selects allowance threshold: **0%, 5%, 15%, 25%, 40%**.
3. Verdict: **Likely Original** if estimated AI ≤ threshold; **Likely AI** if above.

Example from vendor docs: 1,000-word human essay with 100 AI-generated words (10% AI):

- At **5% allowance** → Likely AI (10% > 5%)
- At **15% allowance** → Likely Original (10% ≤ 15%)

Same text, opposite labels. **Threshold is part of the measurement.**

### Threshold semantics (vendor table)

| Allowance | Label | Intended policy |
|-----------|-------|-----------------|
| 0% | Very Strict | Zero AI tolerance |
| 5% | Strict | Minimal AI |
| 15% | Moderate | Light editing (grammar/spelling) |
| 25% | Flexible | Mostly human, some hybrid |
| 40% | Generous | Hybrid permitted; not fully AI-generated |

**Default recommendation:** 15% for general use.

### Reported accuracy by threshold

**Benchmark V6** (456,872 samples, binary-labeled "any AI = AI"):

| Setting | Overall accuracy | Precision |
|---------|------------------|-----------|
| 5% | 98.0% | 91.1% |
| **15%** | **99.4%** | **98.5%** |
| 25% | 95.8% | 99.7% |
| 40% | 88.7% | 99.8% |

Peak at 15% reflects **label alignment with legacy binary datasets**, not universal optimality.

**Threshold Benchmark** (167,980 samples, labels flip by threshold): **96.53% at 5% boundary**.

**Classic baselines on same V6 slice:**

| Model | Accuracy | Precision |
|-------|----------|-----------|
| Lite 1.0.2 | 99.3% | 97.0% |
| Turbo 3.0.2 | 98.3% | 91.8% |

Turbo trades precision for recall on raw AI; AI Allowance at 15% beats both on V6 by vendor metrics.

### Turnitin alignment (vendor study, interpret carefully)

Originality tested **300 GEDE student essays** (100 human, 100 AI-polished human, 100 fully AI) against Turnitin, comparing all five allowance levels. Turnitin ≥50% treated as AI-positive (**study-defined boundary, not Turnitin guidance**).

| AI Allowance | Agreement with Turnitin |
|--------------|-------------------------|
| 0% | 45.3% |
| 5% | 45.7% |
| 15% | 46.7% |
| 25% | 55.3% |
| **40%** | **69.7%** |

When 40% Allowance marked a doc Original, Turnitin scored below 50% in **182/189 cases (96.3%)**. Still only **69.7% overall binary agreement** — detectors are not interchangeable.

**unslop implication:** For students comparing against Turnitin, Turbo 0% and AI Allowance 40% are different instruments. Log which mode was used in bench CSV.

---

## Humanizer resistance — vendor vs independent

### Vendor humanizer table (Sep 2025 launch, Turbo 3.0.2)

| Humanizer | Lite 1.0.2 | Turbo 3.0.2 | Academic 0.0.5 |
|-----------|------------|-------------|----------------|
| Undetectable.ai | 80.3% | **92%** | 82.4% |
| Phrasly.ai | 86.1% | 92% | 89% |
| Stealthwriter.ai | 87.1% | 94% | 89.1% |
| Netus.ai | 86.1% | **97%** | 92.1% |
| Humbot.ai | 81.2% | 90% | 83.3% |

"Accuracy" here = **detection rate** (% of humanizer outputs caught), not fluency tier.

### RAID (ACL 2024) — still cited, model now superseded

- **6.29M texts**, 12 detectors, 11 LLMs, 11 adversarial attacks, 8 domains.
- Originality **2.0 Standard** (pre-Turbo 3.0.2): **85% base**, **96.7% paraphrase** at 5% FPR threshold.
- Won **9/11** adversarial attack categories; weak on homoglyph and zero-width-space (vendor acknowledged, patched in later models).
- RAID paraphrase split remains the best open proxy for humanizer behavior (`pip install raid-bench`).

### Independent 2026 bypass findings

| Source | Finding |
|--------|---------|
| **aidetector.ac** | Originality **91% → 67%** after 14 humanizers; best resistance of 6 detectors tested |
| **Plainview blog** | 7 humanizers vs Turbo 3.0.2 (Jan 2026): **93% still detected**; WriteHuman/AIHumanizer **100% detected**; HIX Bypass best at ~12% evasion |
| **unslop docs (18-commercial-humanizer-tools)** | StealthGPT **35% AI** on Originality; HIX "Latest Mode" explicitly targets Originality 3.0 |
| **DAMAGE (COLING 2025)** | Legacy GPTZero TPR collapses 99.7% → 60% on humanized academic text; Originality positioned as harder than legacy detectors in practitioner rankings |

**Takeaway:** Turbo 3.0.2 catches most SaaS humanizer output most of the time. "Bypass" = lower score, not reliable clearance. No humanizer consistently beats GPTZero **and** Originality **and** Turnitin simultaneously.

---

## ESL / false-positive landscape

Three narratives collide:

1. **Liang et al. (2023)** — GPTZero, OriginalityAI, Crossplag flagged **>50% of TOEFL essays** as AI. https://arxiv.org/abs/2304.02819
2. **Originality rebuttal** — Stanford study used **v1.1**, small TOEFL sample (91), confounded comparison; Originality claims **5.04% FPR** on 1,500+ IELTS essays with v1.4+. https://originality.ai/blog/are-ai-checker-biased-against-non-native-english-speakers
3. **PeerJ 2025 extension** — Lite/Turbo **99.07% accuracy**, **0% FNR** on non-native speaker samples in scholarly abstract dataset. https://originality.ai/blog/ai-detection-scholarly-publications-study

**Vendor stance:** Originality historically said it was **built for publishers/SEO, not academia** — then launched Academic 0.0.5 and Moodle plugin anyway.

**unslop relevance:** README already cites Liang for ESL false-positive risk. Originality Turbo at 1.5% claimed FPR is still **15× Chicago Booth's 0.1% FPR bar for GPTZero** on clean text — hybrid/edited ESL prose is the high-risk zone for **both** Turbo strict mode and AI Allowance at 5%.

---

## Pricing, access, API

| Tier | Price | Credits | API | Notes |
|------|-------|---------|-----|-------|
| Free checker | $0 | 3 scans/day, 2,000 words | No | No AI Allowance model picker on free tier unclear — verify at scan time |
| Pro | $12.95/mo annual ($14.95 monthly) | 2,000/mo | No | 1 credit = 100 words (AI only) or 50 words (AI + plagiarism) |
| Enterprise | $136.58/mo annual ($179 monthly) | 15,000/mo | **Yes** | Team management, 365-day scan history |
| Pay-as-you-go | $30 one-time | 3,000 credits | No | 2-year expiry |

**Scan limits:** AI detection max **10,000 words** per scan (help docs, updated May 2026).

**Bench cost estimate:** 4 texts × ~1 scan each ≈ 4 credits on Pro if <100 words each; longer corpus texts need credit math before run.

---

## Bundled features affecting bench interpretation

| Feature | Relevance to unslop |
|---------|---------------------|
| **Deep Scan** | AI writing tutor — suggests edits to "sound human" (competes with humanizers; different from detection) |
| **Sentence-level highlighting** | Shows which spans flagged — useful for debugging unslop passes |
| **Chrome extension authorship replay** | Provenance, not classification — Grammarly pivot mirror |
| **Plagiarism / fact-check / readability** | Same credit burn; disable for pure AI bench |
| **Bulk Site Scan** | Agency workflow; not bench |

---

## unslop bench relevance

### Current protocol status

`drafts/2026-05-detector-test/PROTOCOL.md` lists Originality as **Tier 1 detector #2**. CSV template expects `detector_version` like `3.0.1`. **Update to log both model family and mode:**

```csv
originality,Turbo 3.0.2,01-flutter,raw,87,,Likely AI,,screenshots/originality_01-flutter_raw.png
originality,AI Allowance 15%,01-flutter,unslop,12,,Likely Original,,screenshots/originality_01-flutter_unslop.png
```

Recommended minimum for article credibility:

1. **Turbo 3.0.2** — hardest binary mode; matches humanizer-industry adversary
2. **AI Allowance 15%** — default hybrid policy; likely verdict for Grammarly-polished unslop output
3. Optional: **AI Allowance 40%** if comparing to Turnitin proxy

### vs unslop `detector.py` (TMR / Desklib)

| Layer | What it measures | Originality overlap |
|-------|------------------|---------------------|
| **TMR** (Oxidane/tmr-ai-text-detector) | RAID-trained 125M RoBERTa; AUROC 99.28% on RAID | Same benchmark family Originality won; **not** correlated 1:1 with Turbo 3.0.2 |
| **Desklib** | Optional release gate | Independent vendor signal |
| **Originality web** | Commercial retrained monthly on humanizer corpora | **Ground truth for "will a paying customer flag this?"** |

TMR green ≠ Originality green. unslop's `--detector-feedback` loop optimizes against **local HF model**, not Originality. For anti-detector mode honesty: **web bench is the external validator**.

### Five-signal stack (`UPDATE-PLAN-2026-08.md`)

Originality Turbo explicitly targets signals unslop partially addresses:

| Signal | unslop coverage | Originality sensitivity |
|--------|-----------------|-------------------------|
| Lexical AI-isms | ✅ `humanize.py` | Caught, but insufficient alone |
| Burstiness / sentence-length σ | ⚠️ `structural.py` | High — Turbo trained on humanizer burstiness shifts |
| Surprisal variance (DivEye) | ⚠️ measure-only `surprisal.py` | Likely high — classifiers absorb LM-surprisal proxies |
| Late-stage stability (TSD) | ❌ | Unknown public detail |
| Predictability cones (GPTZero v6) | ❌ | Originality has separate product line |

**Originality 3.0 + AI Allowance = hybrid thresholds, not binary** per UPDATE-PLAN. A paragraph that passes Turbo may fail AI Allowance 5% if a single sentence block reads AI-heavy.

### Anti-detector mode positioning

From `skills/unslop/SKILL.md`:

- Cross-model second pass (Claude ↔ GPT ↔ Gemini) is **strongest lever** — TempParaphraser reports ~82.5% detector accuracy reduction; still may not clear Turbo.
- Treat as **false-positive defense**, not durable evasion.
- Originality is the detector humanizers **most often fail** — passing Turbo is the highest bar in commercial space.

### Expected unslop outcomes (hypothesis, not measured)

| Text variant | Turbo 3.0.2 (predicted) | AI Allowance 15% (predicted) |
|--------------|-------------------------|------------------------------|
| Raw Claude/GPT prose | High AI score | Likely AI |
| unslop balanced/full | Lower; may still flag | Likely Original if edits are lexical+structural only |
| unslop anti-detector + cross-model pass | Best case for clearance | Depends on residual AI fraction |
| Human baseline (ESL, heavy Grammarly) | FP risk at Turbo sensitivity | 15% may pass; 5% may not |

**Publish partial fails.** Protocol already requires logging when unslop output flags.

### Quarterly re-run trigger

Originality model cadence: **~monthly retraining** against humanizer corpora. Bench rows should include **scan date + visible UI version**. Q3 2026 re-run likely needed if Lite/Turbo point release ships.

---

## Competitive context (one paragraph)

GPTZero owns the **Chicago Booth 2026** external benchmark on clean AI text (99.3% recall @ 0.1% FPR) and added a **humanizer-aware layer (Jan 2026)**. Originality owns the **humanizer-resistance** narrative (RAID paraphrase 96.7%, practitioner bypass failures, HIX explicit targeting). Turnitin owns **institutional deployment** but shows **60–85% drop on paraphrased content** in independent tests and hid 1–19% scores (Oct 2025). Copyleaks pushes multilingual ensemble. **No single detector is authoritative** — unslop's "detectors disagree" README framing is correct; Originality is the **hardest single commercial check**, not the only one.

---

## Gaps and open questions

1. **AI Allowance on free tier?** Homepage mentions "AI Allowance scans (new)" in feature list; confirm model picker availability without Pro login.
2. **API model parameter** — Enterprise API docs not fetched; unknown if API exposes Turbo vs Allowance vs threshold programmatically.
3. **PeerJ DOI** — verify exact DOI for scholarly-publication study before citing in README.
4. **Humanizer table replication** — vendor table lacks sample size, humanizer tier/version, prompt conditions.
5. **RAID recency** — RAID tested model 2.0 Standard; no public third-party RAID re-run on Turbo 3.0.2 found.
6. **aidetector.ac methodology** — independent but opaque; treat as directional, not canonical.

---

## Recommendations for unslop maintainers

1. **Run May bench with Turbo 3.0.2 + AI Allowance 15%** as two rows per text in `scores.csv`.
2. **Screenshot model selector** in every capture — UI version string is audit trail.
3. **Do not claim "beats Originality"** without dated Turbo scan; cite partial fails.
4. **Anti-detector docs:** name Originality Turbo as reference adversary; note AI Allowance for hybrid-policy users.
5. **Consider Enterprise API** for quarterly automated bench (~$136/mo) if manual 56-run protocol becomes recurring.
6. **Cross-reference TMR loop:** if TMR score drops but Originality Turbo still flags, document the gap in RESEARCH_AND_TECH.md — proves commercial retraining outpaces open RAID models.

---

## Key numbers cheat sheet

| Claim | Source | Trust level |
|-------|--------|-------------|
| Turbo 3.0.2 99%+ raw AI | Vendor V6 benchmark | Vendor; directionally consistent with independents |
| Turbo 97% on humanizers | Vendor Sep 2025 table | Vendor; aidetector.ac qualitatively confirms leadership |
| AI Allowance 99.4% @ 15% | Vendor V6 (456k samples) | Vendor; threshold aligned to binary labels |
| RAID 96.7% paraphrase | ACL 2024 / UPenn-CMU | Peer-reviewed; **stale model** |
| aidetector.ac 91% → 67% humanized | Independent 2026 | Directional |
| Turnitin agreement 69.7% @ 40% | Vendor GEDE study | Vendor; useful for mode selection only |
| Liang ESL >50% FP | arXiv 2304.02819 | Peer-reviewed; **old Originality version** |

---

*Agent #58 complete. Cross-ref: AGENT-40 (DAMAGE tiers), AGENT-56 (Turnitin 2025–26), AGENT-57 (GPTZero), UPDATE-PLAN-2026-08 (five-signal stack).*
