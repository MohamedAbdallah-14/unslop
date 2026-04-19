# D — Commercial SaaS, Self-Hostable APIs & OSS Alternatives to Undetectable.ai

**Research value: high** — The "humanizer API" space has a clear commercial layer (WriteHuman, StealthGPT, Undetectable.ai, HumanizerPro, BypassGPT, HIX, Humbot, Phrasly, Humaniser, Stealthly, etc.) and a visible but thin OSS layer (TextHumanize, StealthHumanizer, humanizer-x, Humanize-AI, unmask-ai, ai-humanizer-api, RasaHQ/paraphraser, Parrot). Strong pricing signal, weak "libraries offered as managed services" signal — most commercial players are black-box SaaS, not hosted wrappers of named OSS libs.

Scope: Angle D of the GitHub Tools & Libraries research — commercial SaaS that could be positioned against OSS humanizers, self-hostable humanizer APIs, and libraries offered as managed services.

---

## 1. Commercial SaaS / Managed-Service APIs

Black-box humanizer APIs with hosted infrastructure, API keys, rate limits, and per-word/per-month billing. None of these publicly credit an OSS library under the hood — they are either proprietary pipelines or wrap frontier LLMs plus custom post-processing.

### 1.1 Undetectable.ai — Humanization API v2

- **Posture:** Market incumbent; closed-source SaaS.
- **Pricing:** Consumer $9.99–$49.99/mo (10K–50K words, ~$0.20–$1.00 / 1K words); API access bundled in higher tiers. Cited as "$9.99/month" in comparison reviews.
- **API surface:** `v2`, `v11`, `v11sr` model versions. Parameters include readability levels (High School → Journalist) and strength (Quality / Balanced / More Human).
- **Claim:** "86% average detection reduction" in independent tests.
- **Relevance to D:** This is the thing OSS players explicitly position against — most OSS READMEs name it as the target to match.

### 1.2 WriteHuman API (writehuman.ai/api)

- **Posture:** Developer-facing REST API on top of a consumer app.
- **Pricing:** Standard $29/mo (125K words, 2,000 words/call, 10 req/min), Premium $69/mo (400K words, 4,000 words/call, 60 req/min, "Best of 3" scored outputs). Top-up: $25 / 125K words, non-expiring. ~$0.17/1K words at Premium.
- **API surface:** `POST /v1/humanize` with bearer auth; tone parameter; ~1.2 s avg response; 40+ languages; built-in AI detection on Premium.
- **Marketing quote:** *"Humanize AI text with a single API call… Simple REST API with production-ready reliability. Starting at $0.17 per 1K words."*
- **Relevance to D:** Clearest example of the "managed humanizer API" productization pattern — pricing, SLA, key rotation, usage dashboard all standard.

### 1.3 StealthGPT API (stealthgpt.ai/stealthapi)

- **Posture:** Commercial API with generate-or-rephrase endpoint.
- **Pricing:** `$0.20 / 1K words` (Stealth Pro), `$2.00 / 1K words` (Stealth Business), custom Enterprise. Consumer plan from $9.99/mo (~74% detection drop).
- **API surface:** `/api/stealthify` — tone (`Standard`, `HighSchool`, `College`, `PhD`), quality/speed modes, max 3,000 words/req, auto language detection, returns a 0–100 detection score.
- **Relevance to D:** The "student-facing" flavor of the managed service — the tone ladder (HS→PhD) is a copyable UX primitive.

### 1.4 HumanizerAI (humanizerai.com)

- **Posture:** SaaS with documented developer API.
- **Pricing:** $14.99/mo consumer. API gated to Pro/Business; credit-based billing per word, 10K words per request.
- **API surface:** `/humanize` and `/detect` endpoints, bearer auth; intensity levels `light` / `medium` / `aggressive`.
- **Claim:** "Highest bypass rates at 80% average across GPTZero, Turnitin, and Originality.ai" in one independent test.
- **Relevance to D:** Intensity-ladder UX (light/medium/aggressive) is the second dominant primitive after tone ladders.

### 1.5 HumanizerPro API (humanizerpro.ai/humanizer-api)

- **Posture:** B2B-positioned API, 30+ languages.
- **Pricing:** $37–$1,100+/mo based on word volume.
- **API surface:** Humanize endpoint plus companion services (AI detector, plagiarism, fact-check) — i.e., bundling humanize + detect + plagiarism in one contract.
- **Relevance to D:** The "agency bundle" pattern — detector + humanizer + plagiarism under a single API key, competing on scope rather than pure per-word price.

### 1.6 AI Humanizer API (aihumanizerapi.com)

- **Posture:** Pure-API product with explicit usage-based tiers.
- **Pricing:**
  - Free: 10K words/mo, 10 req/min
  - Starter: $29/mo — 100K words/mo, 60 req/min
  - Professional: $99/mo — 500K words/mo, 300 req/min, batch processing
  - Enterprise: Custom — unlimited words, SSO, VPC/Private endpoint, 99.99% SLA
- **API surface:** 50+ languages, batch processing, SSE streaming, tone preservation, confidence scoring; 20% annual discount; SOC 2 Type II on paid tiers.
- **Marketing quote:** *"Simple, transparent pricing. Start free, scale as you grow. No hidden fees, cancel anytime."*
- **Relevance to D:** Cleanest "enterprise humanizer" pricing grid — SSO, VPC, SLA tiers explicitly on the page.

### 1.7 Humaniser (humaniser.com)

- **Posture:** Privacy-positioned consumer app with a developer preview API.
- **Pricing:** Free tier; premium from $19/mo.
- **API surface:** JS + Python SDKs, tiers from 10K to 2M+ words/mo, "zero data retention" claim, tuned against GPTZero/Turnitin/Originality.ai/Copyleaks.
- **Claim:** "93% average detection reduction", "no signup required" on consumer side; 9.4/10 composite in self-cited comparisons.
- **Relevance to D:** Only mainstream vendor leading with **privacy + zero retention** as the differentiator — this is the angle most competitors ignore.

### 1.8 Humanize-AI-Text (humanize-ai-text.ai)

- **Posture:** Developer portal with direct API.
- **API surface:** `/v1/humanize`, bearer auth, 100 req/min, JS/Python/Java code samples.
- **Relevance to D:** Unremarkable on features; confirms the `/v1/humanize` single-endpoint shape is the de-facto convention.

### 1.9 BypassGPT

- **Posture:** Consumer SaaS with developer API (less-documented than peers).
- **Pricing:** From ~$8/mo freemium; up to 3,000 words/request on premium.
- **Relevance to D:** Price-floor competitor to Undetectable.ai at the consumer end.

### 1.10 HIX Bypass (bypass.hix.ai)

- **Pricing:** $11.99/mo.
- **Performance:** 74% bypass rate, 5–7 s latency, API available.
- **Relevance to D:** Part of a larger HIX writing suite — bundled distribution, not a pure API play.

### 1.11 Humbot

- **Pricing:** $14.99/mo.
- **Performance:** 65% overall bypass, 61% Turnitin / 68% GPTZero; 5–7 s latency.
- **Relevance to D:** Sits in the mid-tier consumer bracket alongside HIX and StealthWriter.

### 1.12 Phrasly

- **Pricing:** $4.99–$12.99/mo; **no public API** despite B2B messaging.
- **Performance:** 76% average bypass across five detectors; 15–25 s latency.
- **Relevance to D:** Data point that "B2B / team" positioning does not imply a real API — a gap a challenger can hit.

### 1.13 Smodin AI Detection Remover

- **Pricing:** $10/mo.
- **Performance:** 0% detection across most detectors in Smodin's own tests; 4–6 s latency; file upload support; API available.
- **Relevance to D:** Differentiates on **file ingestion** (not just copy-paste) — a UX gap most humanizer APIs ignore.

### 1.14 StealthWriter

- **Pricing:** $14.99/mo (30K words, ~$0.50 / 1K words). API positioning inconsistent across sources.
- **Relevance to D:** The older "ninja" brand; now outpaced on price and API maturity by WriteHuman and StealthGPT.

### 1.15 Stealthly

- **Pricing:** Free 300 words/mo → Basic $11–17/mo (20K) → Pro $20–30/mo (50K) → Premium up to $49/mo (300K). API only at higher tiers.
- **Relevance to D:** API-gated-behind-premium is the common anti-pattern — treats the API as an upsell rather than a product.

### 1.16 StealthBypass

- **Pricing:** Free → Pro $7.99/mo → Max $19.99/mo (API access).
- **Relevance to D:** Lowest advertised API price point in the scan; signals a commoditization floor around ~$8/mo for basic API access.

### 1.17 Deceptioner API

- **API surface:** v2, task-based architecture, multi-detector profiles (Turnitin, GPTZero, Winston AI, Originality.ai), 10K char/request cap.
- **Relevance to D:** "Detector profile" as a first-class API parameter is an unusually honest design — makes the tuning explicit instead of hiding behind "aggressiveness".

### 1.18 Apify AI Text Humanizer (apify.com)

- **Posture:** Third-party Actor on Apify's marketplace, not a standalone SaaS.
- **Pricing:** $0.003 per text, sub-500 ms processing.
- **API surface:** 12-pass transformation — phrase replacement, contractions, sentence variation; fully deterministic, **no external LLM dependency**.
- **Relevance to D:** The closest thing in this scan to "OSS-style rules engine packaged as a managed service" — and by far the cheapest per-call price observed.

---

## 2. Open-Source / Self-Hostable Humanizers

The OSS side of Angle D. Most are recent (post-2024), small (often <20 stars), MIT-licensed, and explicitly market themselves against Undetectable.ai / WriteHuman / StealthWriter.

### 2.1 ksanyok/TextHumanize

- **License:** Dual — free for non-commercial, paid commercial (Indie $199/yr, Startup $499/yr, Business $1,499/yr, Enterprise custom with on-prem + SLA).
- **Stack:** Python (primary), PHP, TypeScript — claims 235K+ LoC, 2,073 tests, 38-stage pipeline, PHANTOM™ / ASH™ / SentenceValidator™ proprietary components.
- **Capabilities:** 100% offline, zero dependencies, 25 languages, claimed 60–90% detection reduction.
- **Hosted demo:** texthumanize.link.
- **Relevance to D:** The only OSS project in this scan that formalizes **commercial licensing on top of an open-source codebase** — closest to the "library offered as managed service" pattern.

### 2.2 itsjwill/humanizer-x (HUMANIZER X)

- **License:** MIT.
- **Form factor:** Claude Code skill (4-pass engine).
- **Capabilities:** Removes 30 AI writing patterns; manipulates perplexity / burstiness / entropy; voice-agent humanization mode.
- **Marketing quote:** *"Free alternative to Undetectable AI, WriteHuman, and StealthWriter."* — explicit.
- **Relevance to D:** Strong example of the "skill/plugin-as-humanizer" distribution model bypassing SaaS pricing entirely.

### 2.3 rudra496/StealthHumanizer

- **License:** MIT; TypeScript/HTML.
- **Capabilities:** 13 AI providers, 4 rewrite levels, 13 tone presets, 12-metric AI detection engine, 16 languages, client-side with a 5-pass "Ninja mode" auto-loop. No login, Vercel-deployable.
- **Marketing quote (README tagline):** *"Free, open-source AI text humanizer. 13 providers, 4 rewrite levels, multi-pass ninja mode. No login required."*
- **Relevance to D:** Copies the Undetectable.ai UX (levels + tones + multi-pass) 1:1 in client-side JS.

### 2.4 OrbitWebTools/Humanize-AI

- **License:** MIT; HTML/JS, client-side only, PWA.
- **Capabilities:** Unlimited word count, no backend, targets Turnitin/ZeroGPT/Originality.ai, ChatGPT/DeepSeek/Claude/Gemini-aware.
- **Relevance to D:** Demonstrates that for a wide class of user cases, a **serverless client-side tool** is already sufficient — pressure on the bottom tier of SaaS pricing.

### 2.5 unknownman1244/ai-humanizer-api

- **License:** MIT.
- **Form factor:** JSON API.
- **Capabilities:** Simple REST surface, pitched at bypassing Turnitin / GPTZero.
- **Relevance to D:** A literal "self-host the WriteHuman shape" starter — the drop-in OSS replacement pattern.

### 2.6 imsv1301/unmask-ai

- **Form factor:** Claude Sonnet 4 wrapper with 3-pass pipeline (perplexity injection + burstiness variation).
- **Cost model:** Bring-your-own Anthropic key (min $5 credit); ~$0.07 / 1K words amortized.
- **Relevance to D:** Cleanest example of the "BYO-LLM-key humanizer" — 3× cheaper than StealthGPT Pro without any SaaS layer.

### 2.7 ZAYUVALYA/AI-Text-Humanizer

- **Form factor:** Browser-based, private-by-default.
- **Capabilities:** Context-aware paraphrasing, proper-noun detection, live counters. Explicitly described as early-stage.
- **Relevance to D:** Confirms the long tail — many early-stage OSS humanizers are browser-only, thin, and rarely maintained.

### 2.8 abdibrokhim/humanaize

- **Form factor:** Tutorial/starter project (Next.js + Tailwind + Clerk + Vercel + AI/ML API).
- **Relevance to D:** Illustrative of the "copy-paste a humanizer SaaS in a weekend" trend — 46 stars on a tutorial repo is meaningful signal about how easy it is to clone the product surface.

### 2.9 RasaHQ/paraphraser

- **License:** MIT.
- **Stack:** Transformer-based NLG, 30 languages, Docker CPU/GPU, interactive + bulk modes.
- **Origin:** Built for Rasa NLU data augmentation, not AI-detection bypass.
- **Relevance to D:** A credible **OSS paraphrasing engine** that a commercial humanizer could wrap as a managed service. Not a humanizer itself; a building block.

### 2.10 PrithivirajDamodaran/Parrot_Paraphraser

- **License:** Permissive OSS; ~915 stars.
- **Capabilities:** Syntactic and phrasal diversity controls, NLU augmentation.
- **Relevance to D:** The other canonical OSS paraphraser with enough maturity to be commercialized. Again, not a humanizer out of the box — it needs a detection-aware wrapper on top.

---

## 3. Patterns, Trends, Gaps

### Pricing structure

- **Consumer floor:** $8–$15/mo for 20–50K words. Commoditized.
- **Mid-API tier:** $29/mo for ~100–125K words (AI Humanizer API, WriteHuman Standard) — the de-facto "$29 / 100K words" anchor.
- **Per-1K floor:** ~$0.17 (WriteHuman Premium) on the mainstream side; ~$0.003 (Apify) on the rules-engine side; ~$0.07 (unmask-ai BYO-key) on the self-hosted side. **Two orders of magnitude of spread** — SaaS margins are defensible only through UX and detection-tuning, not compute.
- **Enterprise tier:** Custom pricing consistently gates SSO, VPC, 99.99% SLA — nobody publishes enterprise numbers.

### Product surface conventions

- `POST /v1/humanize` with bearer auth is the default shape. WriteHuman, Humanize-AI-Text, AI Humanizer API, HumanizerAI all converge on it.
- **Intensity ladder** (light / medium / aggressive) and **tone ladder** (HighSchool → PhD / Journalist) are the two dominant parameter conventions.
- Detection score in the response (0–100) is becoming table stakes — StealthGPT, Deceptioner, HumanizerAI all return it.
- Latency: 1–7 s is the working band. Phrasly's 15–25 s is a clear outlier and a competitive gap.

### OSS vs commercial — real gap

- OSS projects are small (<20 stars typical), MIT-licensed, and usually client-side or single-developer. TextHumanize is the most production-shaped with a dual-license model, but still at 12 stars.
- **No widely-adopted OSS humanizer library has emerged** the way LangChain did for LLM orchestration. The mature OSS paraphrasers (RasaHQ/paraphraser, Parrot) are **not detection-tuned** — they were built for data augmentation.
- This means: the commercial SaaS layer is not actually wrapping named OSS libraries. It is wrapping frontier LLMs + proprietary post-processing. The "libraries offered as managed services" thesis is, at present, **mostly aspirational** in this space.

### Gaps / leverage points

1. **Transparent "detector profile" APIs.** Only Deceptioner exposes per-detector tuning as a first-class parameter. Most competitors hide tuning under an opaque "aggressiveness" slider. Transparency is a differentiator.
2. **File ingestion.** Only Smodin supports file uploads. PDFs, DOCX, Google Docs ingestion is an underinvested UX surface.
3. **Privacy-first API.** Humaniser is the only mainstream vendor leading on zero retention. On the OSS side, this is the default — which means a commercial product built on a named OSS library with a zero-retention promise could credibly undercut Undetectable.ai on trust, not price.
4. **True OSS-as-managed-service.** No one is successfully running the "host RasaHQ/paraphraser or Parrot + a detection-aware re-ranker behind an API" play. TextHumanize's dual license is the closest attempt; nobody is attacking the market from a well-known OSS lineage.
5. **Rules-engine tier.** Apify's $0.003/text deterministic 12-pass transform is the only offering at that price point. There is room for a disclosed, open-source rules-based humanizer that runs without LLMs and costs ~$0.
6. **Batch + streaming.** Batch processing and SSE streaming appear only on the higher-priced tiers (AI Humanizer API Professional). Default at-all-tiers batch is still a differentiation lever.

### Counter-signal

- Review sites are heavily self-interested (humaniser.com, thehumanizeai.pro, phrasly.ai all publish "best-of" comparisons that rank their own product first). Treat any bypass-rate number not from an independent academic test as marketing.
- A large share of results point to thin content farms. The actually-durable sources are the vendor API docs themselves (WriteHuman, StealthGPT, Undetectable.ai, AI Humanizer API).

---

## Sources

- https://aihumanizerapi.com/pricing/ — AI Humanizer API public pricing grid (free/$29/$99/custom), SOC 2, VPC, SSE streaming.
- https://writehuman.ai/api — WriteHuman REST API shape, $29/$69 tiers, Best-of-3 feature, 40+ languages.
- https://stealthgpt.ai/stealthapi — StealthGPT API pricing ($0.20 / $2.00 per 1K words), `/api/stealthify` endpoint, tone ladder.
- https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n — Undetectable.ai v2/v11 model versions, readability + strength parameters.
- https://humanizerai.com/docs/api — HumanizerAI developer docs: `/detect` + `/humanize`, intensity levels, 10K word/request cap.
- https://humanizerpro.ai/blog/ai-humanizer-detector-api — HumanizerPro B2B bundle (detect + humanize + plagiarism), $37–$1,100+/mo.
- https://humaniser.com/developers/api — Humaniser developer preview, zero-retention positioning, JS/Python SDKs.
- https://humanize-ai-text.ai/docs — `/v1/humanize` reference implementation; confirms endpoint convention.
- https://stealthbypass.app/pricing, https://stealthly.ai/pricing, https://phrasly.ai/pricing, https://humanizeai.site/pricing/ — Consumer pricing floor and API-gating patterns.
- https://apify.com/george.the.developer/ai-text-humanizer-api/api/javascript — Apify deterministic 12-pass humanizer at $0.003/text, 500 ms SLO.
- https://docs.stealthgpt.ai/api-reference/endpoints/stealthify — StealthGPT `/stealthify` endpoint details.
- https://smodin.io/id/studi-kasus/smodin-ai-detection-remover-vs-competitors — Smodin's self-test claiming 0% detection; file upload support.
- https://github.com/ksanyok/TextHumanize — Dual-license OSS humanizer with paid commercial tiers and hosted demo.
- https://github.com/rudra496/StealthHumanizer — MIT client-side humanizer, 13 providers, 5-pass "Ninja mode".
- https://github.com/itsjwill/humanizer-x — MIT 4-pass Claude Code humanizer; explicit Undetectable/WriteHuman/StealthWriter counter-positioning.
- https://github.com/OrbitWebTools/Humanize-AI — Client-side PWA humanizer, MIT, no backend.
- https://github.com/unknownman1244/ai-humanizer-api — MIT JSON humanizer API starter.
- https://github.com/imsv1301/unmask-ai — 3-pass Claude-based humanizer, BYO-key, ~$0.07/1K words.
- https://github.com/ZAYUVALYA/AI-Text-Humanizer — Early-stage browser humanizer; context-aware paraphrasing.
- https://github.com/abdibrokhim/humanaize — Next.js humanizer tutorial with Clerk/Vercel/AI-ML API.
- https://github.com/RasaHQ/paraphraser — OSS transformer paraphraser, Docker, 30 languages — building block.
- https://github.com/PrithivirajDamodaran/Parrot_Paraphraser — OSS paraphraser, ~915 stars — building block.
