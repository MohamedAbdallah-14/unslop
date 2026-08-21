# Agent #61 — Undetectable.ai / Ryter Pro / Walter Writes

**Topic:** Commercial humanizer ecosystem — product features, pricing, detector evasion claims, independent audits, user debate, unslop positioning  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop SKILL.md / README landscape refresh

---

## Executive summary

Three products anchor the **2025–2026 commercial humanizer tier** that unslop users ask about most: **Undetectable.ai** (category incumbent), **Ryter Pro** (budget Turnitin challenger), and **Walter Writes** (TikTok-viral quality-first humanizer). All three share the same product shape: paste-box web app, built-in “all green” detector panel, REST API on paid tiers, and marketing that promises Turnitin/GPTZero/Originality bypass.

**What independent measurement actually shows:**

| Tool | DAMAGE fluency tier | Pangram catch rate (Aug 2025) | Turnitin (independent, post–Aug 2025) | Built-in detector honesty |
|------|---------------------|-------------------------------|---------------------------------------|---------------------------|
| **Undetectable.ai** | **L3** (worst quality) | **90.3%** caught — best *evader* in Pangram table, still ~9/10 fail | **54–67% bypass** [I]; **no conflict-free Turnitin test** published | Panel omits Turnitin; dashboard can show all-green while Turnitin flags |
| **Ryter Pro** | Not in DAMAGE Table 9 | No Pangram row | **42% AI remaining** (AuraWrite, Mar 2026) — institutional fail | Claims 99.9% / 94% Turnitin [V]; one competitor test contradicts |
| **Walter Writes** | Not in DAMAGE Table 9 | No Pangram row | **79.7% bypass rate** [I] pre-update; **~38% AI flagged** post-update [I] — ~1 in 5 submissions still fail | Internal detector reports 100% human while GPTZero/Copyleaks flag same text [I] |

**Ecosystem pattern:** These tools optimize **detector-score minimization**, not editorial voice. DAMAGE (COLING 2025) classifies Undetectable.ai as L3 — elementary-school output with injected typos — while Pangram still catches it 90.3% of the time. Turnitin’s **27 August 2025 bypasser-detection launch** and **February 2026 retrain** collapsed stable bypass rates for signature-trained humanizers. Vendor “99.8% undetectable” claims diverge from peer-reviewed and independent panels by **20–100 percentage points**.

**unslop positioning:** Do not compete on bypass. unslop is an **in-editor subtractive polish layer** (hooks, regex preservation, voice-match, documented ESL false-positive defense). The honest comparison is not “unslop vs Undetectable.ai.” It is **“unslop + cross-model second pass + manual edit”** vs **“$8–15/mo paste-box with opaque rewrite.”** Independent work consistently shows cross-model paraphrase beats single-pass SaaS humanizers — without L3 quality degradation or monthly credit roulette.

**Highest-value unslop doc actions:**

1. **Name the three tools explicitly** in anti-detector / landscape sections — users search for them by brand.
2. **Separate bypass rate from AI-score reduction** — vendors conflate “79.7% bypass” with “0% AI on Turnitin.”
3. **Cite DAMAGE L3 for Undetectable.ai** when comparing fluency — evasion and readability decouple.
4. **Warn on built-in detector conflict of interest** — all three sell detector + humanizer; internal scores are not external ground truth.
5. **Keep anti-detector boundaries** — ESL/resume defense, not “cheaper Undetectable.ai.”

---

## Primary sources (URLs)

### Product & pricing

| Resource | URL |
|----------|-----|
| **Undetectable.ai homepage** | https://undetectable.ai/ |
| **Undetectable.ai pricing** | https://undetectable.ai/pricing |
| **Undetectable.ai API docs** | https://help.undetectable.ai/en/article/developer-api-1fvasec/ |
| **Undetectable.ai blog (founding narrative)** | https://undetectable.ai/blog/what-is-undetectable-ai/ |
| **Undetectable.ai vs Turnitin (vendor SEO)** | https://undetectable.ai/blog/undetectable-ai-vs-turnitin |
| **Ryter Pro homepage** | https://www.ryter.pro/ |
| **Ryter Pro pricing** | https://www.ryter.pro/pricing |
| **Ryter Pro terms (credits, no refunds)** | https://www.ryter.pro/terms |
| **Walter Writes homepage** | https://walterwrites.ai/ |
| **Walter Writes pricing** | https://walterwrites.ai/pricing |
| **Walter Writes Turnitin SEO guide** | https://walterwrites.ai/bypass-turnitin-ai-detection/ |

### Peer-reviewed & vendor-detector research

| Resource | URL |
|----------|-----|
| **DAMAGE paper (COLING 2025)** | https://arxiv.org/abs/2501.03437 |
| **Pangram humanizer table (Aug 2025)** | https://www.pangram.com/blog/humanizers-aug-25 |
| **Ghostbuster — Undetectable.ai 62% recall** | https://arxiv.org/abs/2305.15047 |
| **Turnitin bypasser press (27 Aug 2025)** | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers |
| **Copyleaks vendor test of humanizers** | https://copyleaks.com/blog/undetectable-ai-tools-are-they-worth-it |
| **EyeSift Copyleaks review (QuillBot/Undetectable)** | https://www.eyesift.com/blog/copyleaks-ai-detector-review/ |

### Independent reviews & tests (2025–2026)

| Resource | URL | Tier |
|----------|-----|------|
| **DetectionDrama — Undetectable vs Turnitin evidence gap** | https://detectiondrama.com/does-undetectable-ai-bypass-turnitin/ | [I] |
| **DetectionDrama — Undetectable vs Pangram (100% caught)** | https://detectiondrama.com/does-undetectable-ai-bypass-pangram/ | [I] |
| **DetectionDrama — Ryter Pro review** | https://detectiondrama.com/ryter-pro-review/ | [I] |
| **DetectionDrama — Walter Writes review** | https://detectiondrama.com/walter-writes-review/ | [I] |
| **Anangsha Alammyan — humanizer bypass test 2026** | https://www.anangsha.me/best-ai-humanizer-for-ai-detector-bypass-in-2026/ | [I] |
| **AIToolBlaze — Undetectable EyeSift synthesis** | https://aitoolblaze.com/blog/undetectable-ai-review-2026 | [I] |
| **TextSight — Undetectable honest take** | https://www.textsight.ai/blog/undetectable-ai-review-2026/ | [I] |
| **AuraWrite — Walter Writes test (38% Turnitin AI)** | https://aurawriteai.com/walterwrites-ai-review | [A]* |
| **AuraWrite — Ryter Pro test (42% Turnitin AI)** | cited in DetectionDrama Ryter review | [A]* |
| **HumanizeMyAI — Walter 100-sample benchmark** | https://humanizemy.ai/vs/walter-writes | [A]* |
| **Word Spinner — Walter bypass table** | https://word-spinner.com/blog/walter-writer-ai-humanizer/ | [A] |
| **Lynote — Walter multi-detector mixed results** | https://lynote.ai/blog/walterwrites-ai-humanizer-review | [I] |
| **TestedByHuman — Walter paragraph workflow (0% claim)** | https://testedbyhuman.com/2026/02/05/how-to-bypass-turnitin/ | [I] |
| **WriteHuman — Walter comparison / HumanizerBench** | https://writehuman.ai/compare/walter-writes-alternative | [A]* |
| **HumanizerBench Aug 2026 cycle** | https://humanizerbench.com/ | [A]* |
| **Trustpilot — Walter Writes** | https://www.trustpilot.com/review/walterwrites.ai | [U] user reviews |

\*Competitor-operated benchmarks — directional, not neutral. Treat numbers as **lower bounds on skepticism**, not gospel.

### Company / market

| Resource | URL |
|----------|-----|
| **Reuters — Undetectable 15M users (Feb 2025 press)** | https://www.reuters.com/press-releases/undetectable-ai-surpasses-15-million-users-2025-02-06/ |
| **Latka — Undetectable revenue (~$3.7M ARR, ~34 employees)** | https://getlatka.com/companies/undetectable.ai |
| **Wikipedia — Undetectable.ai** | https://en.wikipedia.org/wiki/Undetectable.ai |
| **unslop Cat 18 commercial catalog** | `docs/research/18-commercial-humanizer-tools/D-commercial.md` |
| **unslop Cat 18 industry synthesis** | `docs/research/18-commercial-humanizer-tools/B-industry.md` |

### unslop cross-refs

| Agent memo | Relevance |
|------------|-----------|
| **Agent #40 — DAMAGE tiers** | Undetectable L3; Pangram 90.3%; fluency ≠ evasion |
| **Agent #56 — Turnitin 2025–2026** | Bypasser launch; Ryter/Walter post-update claims |
| **Agent #59 — Copyleaks V9** | Undetectable 23% FN in EyeSift panel |
| **Agent #35 — Cross-model paraphrase** | Documented alternative to SaaS humanizer |
| **Agent #44 — Blandification** | Walter 517% YoY; homogenization-as-service |

---

## Ecosystem architecture (shared product shape)

```
User pastes ChatGPT/Claude output
  → SaaS humanizer (black-box LLM paraphrase + heuristics)
  → Built-in multi-detector panel (often vendor-tuned)
  → User submits to institution / publisher
  → External detector (Turnitin, Pangram, Originality) — may disagree with panel
```

**Common feature bundle (all three):**

| Feature | Undetectable.ai | Ryter Pro | Walter Writes |
|---------|-----------------|-----------|---------------|
| AI humanizer | ✓ | ✓ | ✓ |
| Built-in AI detector | ✓ (multi-engine) | ✓ | ✓ |
| Chrome extension | ✓ | — | — |
| REST API | ✓ (annual+) | ✓ (Professional+) | MCP server (2026) |
| Readability / level matching | ✓ (`readability`, `purpose`, `strength`) | Mode selector | Simple / Standard / Enhanced |
| Per-detector targeting | Implicit via strength modes | Claimed universal | Enhanced for strict detectors |
| Languages | 50+ claimed | Multilingual claimed | 80+ claimed |
| Free tier | 250 words trial | 1×/day, 500 words | ~300 words trial |
| Academic positioning | Essay Writer, Job Applier | Plans labeled for students | University + Essay modes |
| Privacy claim | No sale of text; business retention controls | Delete after processing [V] | Varies by surface [V] |

**Technique patterns (inferred — none publish reproducible methods):**

1. **Multi-pass LLM paraphrase** with detector feedback loop (Undetectable explicitly markets detection-informed rewriting).
2. **Readability degradation** — shorter sentences, synonym swap, error injection (DAMAGE L3 signature for Undetectable).
3. **Structural rewrite at “Enhanced” tiers** — Walter Writes and Ryter Pro “Pro Algorithm” claim deeper restructuring vs surface paraphrase.
4. **Per-detector routing** — industry-wide pattern (Deceptioner documents it openly; these three imply it in marketing only).

---

## Product profiles

### 1. Undetectable.ai — category incumbent

**Identity:** Bootstrapped SaaS, launched **May 2023**. Co-founders **Christian Perry**, **Bars Juhasz** (Loughborough PhD; prior RAF AI-detection research marketed as model foundation), **Devan Leos**. ~**11M users** (G2/Tracxn 2026; down from “15M+” Feb 2025 Reuters press release). ~**$3.7M ARR**, ~**34 employees** (Latka, Sep 2025). Forbes “#1 AI Detector” badge on homepage [V].

**Product surface (2026):** Humanizer, multi-engine detector, AI image detector, fake PDF detector, AI audio detector, Chrome extension, Human Auto Typer, Essay Writer, SEO Writer, Job Application Bot, API (`readability`, `purpose`, `strength`, model variants v2/v11/v11sr).

**Pricing (Aug 2026 — verify at signup):**

| Plan | Monthly | Annual effective | Words/mo |
|------|---------|------------------|----------|
| 10K | $9.99 | ~$5.00/mo ($60/yr) | 10,000 |
| 20K | $19.00 | ~$9.50/mo | 20,000 |
| 35K | $31.00 | ~$15.75/mo | 35,000 |
| 50K | $42.50 | ~$21.25/mo | 50,000 |
| Business | Custom | Non-expiring credits, white-label, API | Custom |

Free trial: **250 words**. Money-back guarantee: **conditional** — must prove output scored **<75% human** on named detectors within **30 days**, with screenshots [V/TOS]. Not a satisfaction refund.

**Marketing claims [V]:**

- “99.8% success rate” / “passes AI detectors”
- “Watermark and future proof”
- “Making AI-generated content more human-like” (Forbes quote)
- Detection “99%+ accuracy”; cites PubMed Central comparison of free detectors

**Independent audit results:**

| Study | Finding | Notes |
|-------|---------|-------|
| **DAMAGE Table 9** | **L3 tier** — “elementary school level,” introduces typos | Fluency audit, not bypass |
| **DAMAGE Table 3** | GPTZero TPR on humanized text: **60%** (down from 99.7% raw) | Legacy detector; still majority caught |
| **Pangram Aug 2025** | **90.3% detection** — best evader in 20-tool table | Still ~9/10 caught |
| **Ghostbuster (ICML 2023)** | **62% recall** on Undetectable-balanced output | 38% escape rate |
| **HumanizerBench Aug 2026** | **86.0% bypass** on 5-detector panel | WriteHuman-operated [A] |
| **EyeSift Mar–Apr 2026** | GPTZero **82–87%** bypass; Turnitin **54–67%**; Originality **54–63%**; **23% rescan failure** within 30 min | [I] |
| **Anangsha 2026** | **100% AI** on Pangram; **72% AI** on Quetext | Free tier test [I] |
| **DetectionDrama Jul 2026** | **100% AI** on Pangram; Quetext 72% | [I] |
| **Copyleaks vendor blog** | Still flagged “humanized” whale article | Detector vendor [V] |
| **Turnitin** | **No published Undetectable-specific test** | Evidence gap is the finding |

**User debate:**

- **Pro:** All-in-one detect→rewrite→recheck loop; cheapest annual entry (~$5/mo); API ecosystem; refund exists (if you document everything).
- **Con:** L3 output quality; inconsistent across detectors; conditional refund “homework assignment” (Kismac forum); monthly price rose ($9.99→$14.99 on some tiers per Cat 18); built-in panel omits Turnitin; demographic data collection noted in forum reviews.
- **Forum sentiment:** “Lowers scores but not plug-and-play safe for school” — aligns with DAMAGE L3 + Pangram 90.3%.

---

### 2. Ryter Pro — budget challenger (NOT Rytr)

**Identity:** Separate product from **Rytr** (rytr.me). Domain **ryter.pro**, launched **2025**. Homepage: “🏆 #1 Ranked AI Humanizer,” **50,000+ users**, **99.9% success rate**, **1.5M+ texts processed** [V]. Trustpilot **4.9** cited on site [V]. Student-first pricing copy.

**Product surface:** Paste-in humanizer, built-in detector, REST API (Professional+), credit-based billing. “Pro Algorithm and New Model” on paid tiers [V]. Claims **>5,000 words/minute** processing in Cat 18 synthesis [I].

**Pricing (Aug 2026):**

| Plan | Monthly | Annual effective | Credits/mo | Per-run limit |
|------|---------|------------------|------------|---------------|
| Basic | $9.99 | **$6/mo** | 100 | 5,000 chars |
| Professional | $19.99 | **$12/mo** | 500 | 10,000 chars |
| Enterprise | $29.99 | **$18/mo** | 1,000 | Unlimited chars |

**Credit economics:** Humanizer ≈ **2 credits**; basic detection ≈ **1**; **Turnitin check ≈ 10 credits** [V]. Free: **1 humanization/day, 500 words**. **All sales final — no refunds** [TOS]; GPU provisioned immediately; 14-day withdrawal waived.

**Marketing claims [V]:**

- “99.9% success rate against all major AI detection tools including Turnitin, GPTZero, Originality.ai”
- “Bypass all major AI detection tools including Turnitin”
- Homepage demo: 100% AI → 1% AI (curated)

**Independent audit results:**

| Study | Finding | Notes |
|-------|---------|-------|
| **AuraWrite Mar 2026** | Turnitin **42% AI**; Originality **55% AI**; GPTZero **20% AI**; ZeroGPT **12% AI** | Competitor test [A] — institutional fail on Turnitin |
| **DetectionDrama Jun 2026** | Verdict **6.5/10** — “crushes lightweight detectors, Turnitin unproven” | Synthesizes AuraWrite + vendor claims |
| **AI Natural Write Apr 2026** | **94% Turnitin bypass**, 97% GPTZero [I] cited in Cat 18 | Conflicts with AuraWrite — methodology unknown |
| **DAMAGE / Pangram** | Not in Table 9 | No peer-reviewed fluency tier |
| **Turnitin** | No published test | Same evidence gap as Undetectable |

**Pattern:** Strong on **ZeroGPT/GPTZero**, weak on **Turnitin/Originality** in the only detailed independent test. Directionally matches industry norm: consumer detectors easier than institutional stacks.

**User debate:**

- **Pro:** Cheapest paid humanizer ($6/mo annual); clean UX; free daily test; API on Pro tier.
- **Con:** 99.9% claim uncited; Turnitin unproven; no refund policy; credit model opaque; name collision with Rytr confuses buyers; thin third-party review corpus outside competitor tests.

---

### 3. Walter Writes — TikTok-viral quality humanizer

**Identity:** **walterwrites.ai**, emerged **2024–2025**, mainstream awareness via **TikTok** (early 2026). Search interest surged **~517% YoY** (Cat 18 / Agent #44 internal notes). Claims **100,000+ users** [V]. Added **MCP server** access on paid plans (2026 pricing page) — positions in agent-tooling adjacency.

**Product surface:** Humanizer with **Simple / Standard / Enhanced** levels; built-in detector; **University + Essay** modes; ChatGPT watermark removal claim; mobile app; SEO landing pages for students/academics/business.

**Pricing (Aug 2026 — annual rates shown on site):**

| Plan | Annual effective | Words/mo | Words/request |
|------|------------------|----------|---------------|
| Starter | **$8/mo** ($96/yr) | 30,000 | 750 |
| Pro | **$13/mo** ($156/yr) | 70,000 | 1,500 |
| Elite | **$26/mo** ($312/yr) | 200,000 | 2,000 |
| Teams | **$99/mo** ($1,188/yr) | 500,000 | 2,000 (10 seats) |

Free trial: **~300 words**. Site FAQ: “incorporates contextual nuances, minor errors, or informal language” — explicit error-injection admission [V].

**Marketing claims [V]:**

- “Make AI Text Feel Like You Wrote It”
- Passes Turnitin including “August 2025 bypasser detection update” (student landing pages)
- Built-in detector shows authenticity score instantly
- **Disclaimer on homepage:** “We are not affiliated with other detection services” — yet marketing cites Turnitin/GPTZero by name on SEO pages

**Independent audit results:**

| Study | Finding | Notes |
|-------|---------|-------|
| **The Humanize AI — 100 samples, Apr 2026** | Bypass rates: Turnitin **79.7%**, GPTZero **89.3%**, Copyleaks **87.0%**, Originality **84.2%**, ZeroGPT **93.8%** — avg **87.6%** | Rival vendor benchmark [A] |
| **Blog/marketing content** | **92.8%** bypass on blog/marketing genres | Same study — genre matters |
| **AuraWrite 2026** | Turnitin **38% AI flagged**; Originality **45% AI**; GPTZero **15% AI** | Post–Aug 2025 update narrative |
| **WriteHuman comparison** | **38%** still flagged Turnitin; HumanizerBench **60.83** vs WriteHuman **76.69** | Competitor [A] |
| **Lynote 2026** | Mixed: Originality **98% original** on one sample; GPTZero/Copyleaks **100% AI** on same workflow | Single-sample variance |
| **TestedByHuman Feb 2026** | **0% AI** Turnitin with **paragraph-by-paragraph Enhanced** workflow | Pro-instructor account; n=1 essay |
| **DetectionDrama** | **~87% avg** bypass; “not 100%”; refund complaints | [I] |
| **Trustpilot** | **~2.4/5** — billing, refund denials, credit inflation, internal 100% vs external detectors | [U] |

**Post–Turnitin August 2025 narrative:** Pre-update Turnitin bypass ~**79.7%** [I]. After bypasser-detection shipping, independent tests report **~38% of content still flagged** [I] — roughly **1 in 5 submissions fail** at the bypass-rate framing, or **38% AI score** at the residual-score framing. Both metrics are cited in the wild; unslop docs should **name which metric** when comparing.

**User debate:**

- **Pro:** Strong on marketing/blog copy; Enhanced mode structurally rewrites; free trial; MCP integration for agent users; paragraph workflow can yield low scores (TestedByHuman).
- **Con:** TikTok “beats Turnitin” hype exceeds academic reliability; Trustpilot billing/refund pattern; internal detector optimism vs external failure; adds **25–40% word count** (AuraWrite); credits expire monthly; technical content meaning drift reported.
- **Reddit:** Limited indexed threads — reputation grew on TikTok, not sustained forum debate (HumanizeMyAI observation, Jul 2026).

---

## Claim vs measurement — synthesis table

| Claim source | Undetectable.ai | Ryter Pro | Walter Writes |
|--------------|-----------------|-----------|---------------|
| **Vendor headline** | 99.8% undetectable [V] | 99.9% success [V] | Detector-safe / beats Turnitin [V] |
| **Peer-reviewed fluency** | DAMAGE **L3** [P] | — | — |
| **Adapted detector (Pangram)** | **90.3% caught** [P/V] | — | — |
| **Institutional (Turnitin)** | 54–67% bypass [I]; no clean public test | 42% AI left [A] vs 94% bypass [I] — conflict | 79.7% bypass [A] vs 38% flagged [I] |
| **Consumer (GPTZero)** | 82–87% bypass [I]; Anangsha 0% pass Pangram | 20% AI [A] | 89.3% bypass [A] |
| **Originality.ai** | 54–63% bypass [I] | 55% AI [A] | 84.2% bypass [A] vs 45% flagged [I] |
| **Score stability** | 23% fail on rescan @ 30 min [I] | — | High run-to-run variance [I] |

**Interpretation:** Vendor panels optimize for **weak detectors and curated samples**. Pangram (DAMAGE authors) and Turnitin (bypasser-trained) represent the **2026 ceiling**. No commercial humanizer in this trio achieves durable institutional bypass under adapted measurement — consistent with Sadasivan impossibility framing (Agent #17) and StealthRL fine-tune threat (Agent #26).

---

## Debate map — supporters vs skeptics

### Industry / academic skeptics

| Actor | Position | Citation |
|-------|----------|----------|
| **Pangram / DAMAGE authors** | >90% catch on named humanizers; L1 fluent rewrites *more* detectable | [humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25) |
| **Turnitin** | Bypasser detection shipped; humanizer vendors = “cheating providers”; **no bypass accuracy published** | Aug 2025 press |
| **DetectionDrama** | Turnitin bypass percentages often **don’t exist**; evidence gap is the finding | 2026 Undetectable/Turnitin memo |
| **Liang ESL bias** | Detectors already harm non-native writers; humanizer arms race worsens equity | Agent #18 |
| **Institutions (Curtin 2026)** | Disabling Turnitin AI detection — detector-led workflow retreat | Agent #56 |

### Vendor / affiliate supporters

| Actor | Position | Conflict |
|-------|----------|----------|
| **Undetectable.ai** | Forbes #1; conditional refund; 8M+ users | Sells both detector + humanizer |
| **Ryter Pro** | #1 ranked; 99.9%; student pricing | No refunds; self-reported stats |
| **Walter Writes** | TikTok demos; Enhanced structural rewrite | Trustpilot 2.4/5; competitor tests mixed |
| **WriteHuman / AuraWrite / HumanizeMyAI** | Publish benchmarks favoring themselves | Direct competitors |
| **HumanizerBench (WriteHuman)** | Undetectable 86% bypass; Walter ~61% composite | Operator = ranked #1 vendor |

### Practitioner consensus (forums, 2025–2026)

1. **Test your exact detector** before paying — free tiers exist for this.
2. **Built-in green checks lie** — always verify externally.
3. **Turnitin ≠ GPTZero** — optimizing one fails the other routinely.
4. **Paragraph-level + Enhanced** beats bulk paste (Walter workflow) — manual labor vendors omit from ads.
5. **Cross-model rewrite** (GPT→Claude→Gemini) beats single-pass humanizer in practitioner threads — aligns with Agent #35.

---

## unslop positioning

### What unslop is not

| SaaS humanizer promise | unslop response |
|------------------------|-----------------|
| “99.8% undetectable” | Documented ~0.0–0.2 pp TMR shift on deterministic pass; no bypass guarantee |
| Paste-box rewrite | In-editor skill + optional Python pipeline |
| Built-in detector loop | Optional `--detector-feedback`; not primary success metric |
| L3 error injection | Subtractive de-slop; preserve code/URLs byte-exact |
| $8–15/mo credit roulette | Free/open-source plugin + PyPI |

### What unslop offers instead

| User need | unslop path | Research basis |
|-----------|-------------|----------------|
| “Sounds like AI wrote this” | `balanced` / `full` modes — drop stock vocab, cap em-dashes, burstiness | Wikipedia taxonomy; blader/humanizer (#32) |
| ESL false positive | `anti-detector` — register restoration, contraction pass | Liang 2023; Working Educators |
| Voice preservation | `voice-match` + style memory | Agent #52 limits |
| Maximum fingerprint separation | Document **cross-model second pass** after unslop | Agent #35; Adversarial Paraphrasing |
| Honest detector expectations | Sadasivan bound; Turnitin bypasser Aug 2025; Pangram 90.3% | Agents #17, #56, #40 |

### Recommended messaging (August 2026)

> **Undetectable.ai, Ryter Pro, and Walter Writes** are cloud rewriters that trade readability (sometimes severely) for lower detector scores on **some** panels. Independent tests show **none** reliably beat Turnitin, Pangram, and Originality together after 2025–2026 retrains. **unslop** removes AI-isms and restores human rhythm in your editor — it does not sell bypass. For false-positive defense (ESL writers, resumes), use `anti-detector` mode and optionally a **cross-model rewrite you control**, not a black-box subscription.

### Boundaries (unchanged — now load-bearing)

From `skills/unslop/SKILL.md`:

- Anti-detector mode: **defensive** — not academic misconduct tooling.
- Never fabricate facts to satisfy anti-detector mode.
- Do not market “Undetectable.ai alternative” on bypass claims — market on **honest voice**.

### Doc / code actions

| Priority | Action | Target |
|----------|--------|--------|
| P0 | Add trio to commercial landscape paragraph with DAMAGE/Pangram citations | `skills/unslop/SKILL.md` |
| P0 | Fix “Chicago Booth twelve humanizers” conflation | README / SKILL (per Agent #40) |
| P1 | Glossary: **bypass rate** vs **residual AI %** | `docs/RESEARCH_AND_TECH.md` |
| P1 | Benchmark template: name detector version date + humanizer tier | `drafts/2026-05-detector-test/` |
| P2 | Optional `--detector-feedback` ladder note: SaaS humanizers = opaque Tier-3 paraphrase | `unslop/scripts/detector.py` docs |

---

## Competitive positioning matrix (August 2026)

| Dimension | Undetectable.ai | Ryter Pro | Walter Writes | **unslop** |
|-----------|-----------------|-----------|---------------|------------|
| **Primary goal** | Detector evasion | Detector evasion | Quality + evasion | Editorial voice |
| **Price floor** | ~$5/mo annual | ~$6/mo annual | ~$8/mo annual | Free |
| **Output quality (DAMAGE)** | L3 | Unknown | Unknown | N/A (subtract-first) |
| **Preservation** | Breaks code/citations often | Unknown | Word inflation | Byte-exact contract |
| **Turnitin honest expectation** | Low–moderate | Low | Low–moderate | None claimed |
| **Refund** | Conditional | None | Complaints [U] | N/A |
| **Open source** | No | No | No | Yes |
| **Agent integration** | Chrome ext | API | MCP server | Hooks + skills |

---

## Open questions for follow-up agents

1. **Agent #64 (QuillBot):** Suite humanizer vs dedicated — where does QuillBot sit vs this trio on post-bypasser Turnitin?
2. **Agent #65 (Anangsha 2026):** Full methodology for Pangram 100% fail on Undetectable — sample size, mode, premium tier?
3. **Agent #67 (marketing vs audit):** Build evidence-tier template for README citations ([P]/[I]/[A]/[V]/[U]).
4. **Ryter Pro Pangram test:** No public data — worth a fixture in `drafts/2026-05-detector-test/`?
5. **Walter MCP server:** Technical integration patterns for agent harnesses — competitor analysis for unslop distribution?

---

## unslop verdict

**Undetectable.ai, Ryter Pro, and Walter Writes** are the **visible commercial layer** of the detector-evasion economy — polished UX, aggressive SEO, built-in detector theater, and pricing that undercuts enterprise API tiers. They are **not** voice tools. DAMAGE proves the category leader (Undetectable) sacrifices fluency to L3 while Pangram still catches **90.3%**. New entrants (Ryter, Walter) fight on **Turnitin marketing** with **conflicting independent numbers** and **competitor-operated benchmarks**.

**unslop wins on honesty, preservation, and integration** — not bypass. Users arriving from TikTok or Reddit asking “which humanizer beats Turnitin” should be routed to: (1) subtract AI-isms in-editor, (2) cross-model pass if fingerprint separation is needed, (3) never trust a built-in green check, (4) read Liang on ESL false positives before chasing lower scores.

---

*Agent #61 complete. Manifest row 61 → done.*
