# Agent #63 — Grammarly / Superhuman Acquisition & AI Authenticity Stack

**Topic:** Grammarly's pivot to Superhuman (company), Superhuman Mail acquisition, AI writing agents, detection/humanization features 2025–2026, GPTZero acquisition, market implications, unslop positioning  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Grammarly is no longer a single-purpose writing assistant. Between January 2025 and June 2026 it executed a three-step platform play: **Coda** (workspace), **Superhuman Mail** (email surface), **GPTZero** (detection/authenticity), then rebranded the **parent company** as **Superhuman** while keeping the **Grammarly product name**. The result is the only mainstream vendor shipping **detection + humanization + process provenance** in one bundle — deliberately framed as academic integrity, not bypass.

Three facts matter for unslop:

1. **Dual "Superhuman" confusion is real.** July 2025: Grammarly acquired **Superhuman Mail** (Rahul Vohra's email app). October 2025: Grammarly **rebranded the company** to Superhuman. June 2026: Superhuman acquired **GPTZero**. The email product, the company, and the detection startup are three different entities that now share a brand.

2. **Detection marketing ≠ independent paraphrase reality.** Superhuman claims RAID **#1** quality (670k+ texts, Feb 2026 blog). Independent tests tell a split story: strong on **raw, unedited** frontier-model output; weak once text is paraphrased, blended, or humanized. Pangram Labs reported **0/9** detection on a current-generation panel where GPTZero caught **7/9**. DAMAGE ([arXiv:2501.03437](https://arxiv.org/abs/2501.03437)) classifies Grammarly's rewrite as **L1 paraphraser** — fluent, faith-preserving, **100% detected** on HumanizerBench. The Humanizer agent is architecturally a clarity/voice tool, not a StealthGPT-class bypass engine.

3. **The arms race is shifting to provenance.** Authorship (5M+ students on Google Docs/Word; default-on in docs March 2026) plus agent-specific attribution plus GPTZero Replay/AI Vision moves institutional evaluation from "does this score 80% AI?" to "show me the creation log." Classifier evasion is a narrowing window; **process transparency** is the 2026–2027 endgame Superhuman is betting on.

**unslop verdict:** Superhuman is the **legitimate incumbent** unslop users will be compared against — same audience (students, knowledge workers), opposite posture (integrated SaaS vs open plugin, detection stack vs voice polish). unslop wins on **editor-native polish, code/URL preservation, transparent non-bypass positioning, and defensive ESL use cases** Superhuman's Humanizer doesn't own narratively. unslop loses on distribution (40M DAU, institutional contracts), RAID-marketed detector depth, and Authorship provenance. Do not claim unslop "beats Grammarly's detector"; cite RAID/conservative-tuning limits and structural humanization gaps instead.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Coda acquisition + Mehrotra CEO** | https://www.grammarly.com/blog/company/grammarly-acquires-coda/ |
| **$1B General Catalyst financing (May 2025)** | https://www.businesswire.com/news/home/20250529436291/en/Grammarly-Announces-1-Billion-Growth-Financing-With-General-Catalyst |
| **Superhuman Mail acquisition (Jul 2025)** | https://www.grammarly.com/blog/company/grammarly-to-acquire-superhuman/ |
| **Company rebrand → Superhuman (Oct 2025)** | https://www.grammarly.com/blog/company/announcing-company-rebrand-to-superhuman/ |
| **Superhuman Go launch** | https://www.grammarly.com/blog/company/introducing-new-superhuman/ |
| **Eight AI agents launch (Aug 2025)** | https://www.grammarly.com/blog/company/grammarly-launches-ai-agents/ |
| **AI Detector (#1 RAID claim, Feb 2026)** | https://www.grammarly.com/blog/company/number-one-ai-detector/ |
| **Free AI Detector landing page** | https://www.grammarly.com/ai-detector |
| **AI Humanizer landing page** | https://www.grammarly.com/ai-humanizer |
| **Humanizer support guide** | https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide |
| **Paraphraser support guide** | https://support.grammarly.com/hc/en-us/articles/38552469933837-Paraphraser-agent-user-guide |
| **Authorship + agent-specific attribution (Mar 2026)** | https://www.grammarly.com/blog/company/superhuman-authorship-docs/ |
| **Authorship in docs (blog)** | https://blog.superhuman.com/authorship-launches-in-docs-with-agents/ |
| **GPTZero acquisition (Jun 2026)** | https://blog.superhuman.com/superhuman-gptzero-ai-authenticity-suite/ |
| **GPTZero acquisition (TechCrunch)** | https://techcrunch.com/2026/06/23/superhuman-acquires-ai-detection-startup-gptzero/ |
| **Superhuman Mail acquisition (Reuters)** | https://www.reuters.com/business/grammarly-acquires-email-startup-superhuman-ai-platform-push-2025-07-01/ |
| **Rebrand (TechCrunch)** | https://techcrunch.com/2025/10/29/grammarly-rebrands-to-superhuman-launches-a-new-ai-assistant/ |
| **RAID benchmark (paper)** | https://arxiv.org/abs/2405.07940 |
| **RAID leaderboard** | https://raid-bench.xyz |
| **DAMAGE humanizer audit** | https://arxiv.org/abs/2501.03437 |
| **Chicago Booth detector eval** | https://doi.org/10.3386/w34223 |
| **GPTZero evolution memo (sibling)** | [AGENT-57-GPTZERO-EVOLUTION.md](./AGENT-57-GPTZERO-EVOLUTION.md) |
| **RAID benchmark memo (sibling)** | [AGENT-15-RAID-BENCHMARK.md](./AGENT-15-RAID-BENCHMARK.md) |
| **DAMAGE memo (sibling)** | [AGENT-12-DAMAGE-DETECTOR.md](./AGENT-12-DAMAGE-DETECTOR.md) |

### Third-party / independent (use with caution)

| Resource | URL | Note |
|----------|-----|------|
| Fast.io Grammarly detector review 2026 | https://fast.io/resources/grammarly-ai-detector-review-2026/ | ~81% on raw GPT-4o; drops on paraphrase |
| Cripsywire conservative-tuning analysis | https://cripsywire.com/grammarly-ai-checker/ | Explains RAID #1 vs real-world paraphrase gap |
| HumanizerBench (Grammarly 0% bypass) | https://humanizerbench.com/ | WriteHuman-operated; 12-tool panel |
| Graphite "half the internet is AI" (cited by Superhuman) | Referenced in GPTZero acquisition blog | Primary study not independently verified here |

---

## Timeline: platform assembly

| Date | Event | Significance |
|------|-------|--------------|
| **Jan 2025** | Acquires **Coda**; Shishir Mehrotra becomes CEO | Workspace/agent orchestration layer; revenue reported >$700M post-deal |
| **May 29, 2025** | **$1B non-dilutive** financing from General Catalyst CVF | Explicitly earmarked for GTM + **strategic acquisitions**; revenue-linked repayment, no new equity |
| **Jul 1, 2025** | Acquires **Superhuman Mail** (email app) | Email = #1 professional use case; 50M+ emails/week via Grammarly; Vohra joins leadership |
| **Aug 18, 2025** | Launches **8 specialized AI agents** + **docs** writing surface | Agentic pivot: Paraphraser, AI Detector, Plagiarism, Citation Finder, Proofreader, Reader Reactions, AI Grader, Expert Review |
| **Sep 2025** | Dedicated **AI Humanizer** landing page + agent | Mainstream "humanizer" framed as clarity/voice; custom voice profiles |
| **Oct 29, 2025** | **Company rebrand** to Superhuman; launches **Superhuman Go** | Suite bundles Grammarly + Coda + Superhuman Mail + Go; Pro $12/mo, Business $33/mo (annual) |
| **Feb 1, 2026** | Superhuman Go features free through this date | Land-grab for connector/partner agent ecosystem |
| **Feb 10, 2026** | Blog: AI Detector **#1 on RAID** quality leaderboard | Marketing anchor for education sales |
| **Mar 10, 2026** | **Authorship** default-on in docs; **agent-specific attribution** | Process provenance beats post-hoc scan |
| **Jun 23, 2026** | Acquires **GPTZero** (~$30M ARR, 19M users) | Dual-detector authenticity layer; GPTZero stays standalone |
| **Aug 2026** | Coda → **Superhuman Docs** rebrand underway | Unified visual identity across suite |

**Naming cheat sheet:**

| Name | What it is |
|------|------------|
| **Superhuman** (company) | Parent; formerly Grammarly Inc. |
| **Grammarly** (product) | Writing assistant; browser extension + docs |
| **Superhuman Mail** | AI-native email client (acquired company/product) |
| **Superhuman Go** | Proactive cross-app AI assistant (connectors to Gmail, Jira, Drive, etc.) |
| **Superhuman Docs** | Coda workspace, rebranded |
| **GPTZero** | Standalone detection/authenticity brand; integrating into Go |

---

## Corporate architecture & distribution

### Scale (company claims, Oct 2025 rebrand)

- **40M+** people; **50,000** organizations; **3,000** educational institutions
- Integrations across **500k–1M** apps/sites (figures vary by press release; Go marketing uses 1M)
- **5M+ students** on Authorship (Google Docs + Word + docs)
- Post-Coda revenue **>$700M** (Vestbee/Crunchbase reporting, 2025)
- Last private valuation cited **$13B** (2021 round); Superhuman Mail last valued **$825M** (2021)

### Superhuman Suite (bundled subscription)

| Component | Role |
|-----------|------|
| **Grammarly** | Real-time writing: grammar, tone, generative rewrite, agents |
| **Superhuman Docs** | Team workspace; agents embedded in documents |
| **Superhuman Mail** | AI-native inbox; triage, scheduling, voice-matched replies |
| **Superhuman Go** | Cross-surface proactive assistant; connector + partner agents |

### Strategic thesis (Mehrotra)

Grammarly's "AI superhighway" — agents delivered **where users already work** rather than forcing context-switch to a chat tab. Email and docs become **multi-agent orchestration surfaces**: e.g., customer memo with grammar agent + sales-facts agent + support-context agent + marketing-positioning agent simultaneously.

General Catalyst's **$1B CVF** structure signals IPO-path ambition without immediate dilution: scale GTM, buy complementary products (Coda, Superhuman Mail, GPTZero), build agent platform before Anthropic/OpenAI absorb the category.

---

## AI writing stack (2025–2026)

### Layer 1 — GrammarlyGO / core generative (pre-agent)

- Context-aware prompts using user writing history
- Tone + formality controls
- **Notable self-disclosure (historical):** Grammarly acknowledged GrammarlyGO output *can be detected by AI detectors* without human editing — rare transparency among writing suites ([docs/research/04-natural-language-quality/D-commercial.md](../../docs/research/04-natural-language-quality/D-commercial.md))

### Layer 2 — Eight specialized agents (Aug 2025)

Rolling out in **docs** (`app.grammarly.com`) then extension; Free + Pro at launch; Enterprise/Education later 2025.

| Agent | Function |
|-------|----------|
| **Paraphraser** | Six presets: Humanize, Academic, Professional, Streamlined, Creative, Simple; custom voice |
| **AI Detector** | Pro-only at launch; sentence-level highlighting in paid tier |
| **Plagiarism Checker** | Pro-only at launch |
| **Citation Finder** | Source discovery |
| **Proofreader** | Grammar/clarity |
| **Reader Reactions** | Simulated audience feedback (professor/manager/client) |
| **AI Grader** | Rubric-aligned pre-submission feedback |
| **Expert Review** | Domain expert simulation |

Later additions: **AI Rewriter** (targeted clarity revisions with detector transparency), **Humanizer** (see below).

### Layer 3 — Superhuman Go (Oct 2025+)

- Proactive assistant in Chrome/Edge extension; Mac/Windows planned
- **Connector agents:** Gmail, Google Calendar, Google Drive, Jira, etc.
- **Partner agents:** Box, Gamma, Wayground (expanded ecosystem)
- **Agents SDK:** closed developer beta
- Agents shared across Go and docs; voice profiles portable between Paraphraser and Humanizer

### Voice / style capture

- **Custom voice:** 200+ word writing sample → profile shared across Paraphraser + Humanizer
- **Four preset voices** on Humanizer landing page
- **Six languages:** EN, ES, FR, DE, PT, IT
- Documents-vs-messages split (personal vs work tone) — likely template for enterprise

**Gap vs deep humanization:** Tone sliders and sample-based profiles are **recommendation engines on generated text**. They don't reproduce sentence-level idiosyncratic quirks (contraction rate, register mixing, late-stage surprisal volatility). Superhuman rebrand adds productivity layer; does not deepen stylometric fidelity beyond competitor Jasper Brand Voice / Claude Styles baseline.

---

## Detection capabilities

### Product surface

| Tier | Features |
|------|----------|
| **Free** | Paste/upload scan; aggregate **percentage AI score**; no per-scan word limit (marketing) |
| **Pro / docs agent** | Sentence-level highlighting; explanations; integrated rewrite suggestions |
| **Authorship (Education)** | Process tracking — typed vs pasted vs AI vs agent-assisted |

### Technical claims (vendor)

- Model trained on **tens of thousands** of pre-2021 human + AI texts
- Segments document; scores each section; outputs **percentage** estimate
- **Conservative tuning:** prefers missing AI over false-accusing humans (third-party analysis, Cripsywire 2026)
- **RAID #1 quality** (Feb 2026): tested on **670,000+** real-world texts across styles, models, evasion attempts

### RAID #1 — what it means and doesn't

RAID ([arXiv:2405.07940](https://arxiv.org/abs/2405.07940)) is the field's standard robustness benchmark ([AGENT-15](./AGENT-15-RAID-BENCHMARK.md)). Superhuman's claim is **quality leaderboard** under RAID's evaluation protocol — not "undefeatable in the wild."

**Supports the claim:**

- Fixed-FPR methodology; large multi-domain corpus
- COLING 2025 shared task showed **trained** detectors can hit 97%+ TPR@FPR=5% even with RAID attacks — when train and test share attack taxonomy

**Limits the claim:**

- RAID attacks (synonym swap, homoglyph, repetition penalty) ≠ commercial humanizers (StealthGPT, Undetectable, DIPPER)
- Shared-task authors warn results may not extend to unseen generators or prompt-based evasion
- **Conservative tuning** optimizes RAID's fairness metrics while sacrificing recall on paraphrased AI
- Independent panel: Pangram Labs **0/9** vs GPTZero **7/9** on current-gen outputs (Fast.io 2026, citing Pangram)
- **Chicago Booth** ([AGENT-62](./AGENT-62-CHICAGO-BOOTH-2026.md)) did **not** evaluate Grammarly detector

### Post-GPTZero acquisition: "two detectors are better than one"

June 2026 rationale (Superhuman blog):

- Superhuman detector: RAID #1, 40M-user behavioral data
- GPTZero: education-specialized patterns, Mixed/Polished/Paraphrased taxonomy, Replay, AI Vision, hallucination + citation verification
- Combined suite in Superhuman Go: detection + plagiarism + citation check + feed-level AI Vision + authorship tracking

**Interpretation:** Superhuman acknowledges single-detector limits. Cross-checking different training data and threshold philosophies is intellectually honest — and a moat against pure-play detectors (Pangram, Originality) that can't offer humanization + provenance in the same subscription.

---

## Humanization features

### Humanizer agent (Sep 2025+)

**Positioning:** "Editor with emotional intelligence" — eliminate robotic phrasing, add warmth, preserve meaning. **Explicitly not framed as detector bypass.**

Landing page language:

> "While an AI humanizer can be a helpful tool… the use of AI humanizers can be frowned upon in certain contexts. We suggest using Grammarly's AI humanizer alongside Grammarly's suite of **transparency features**."

**Mechanics:**

- NLP rewrite preserving semantics
- Preset voices + custom profile (200+ word sample)
- Actionable inline suggestions (hover bars in docs)
- Paired workflow: run **AI Detector first** → Humanizer on flagged spans
- Available: Free (limited), Pro/Plus, Go, docs; Enterprise/Education via admin agent-access controls

### Paraphraser "Humanize" preset

Functionally overlaps Humanizer — same voice profiles, six-style preset grid includes **Humanize** as one option. DAMAGE taxonomy treats Grammarly rewrite as **L1 paraphraser** (high fluency, faithfulness preserved) alongside QuillBot and DIPPER.

### AI Rewriter agent

Targeted revisions with **detector transparency** — shows how AI detectors assess text during rewrite. Positions humanization as iterative clarity improvement, not one-shot bypass.

### Independent audit results

| Study | Grammarly result | Context |
|-------|------------------|---------|
| **DAMAGE** ([AGENT-12](./AGENT-12-DAMAGE-DETECTOR.md)) | **L1** tier; GPTZero TPR drops from 99.73% → 60.04% *across all 19 tools pooled*; Grammarly individually in L1 paraphraser class | Academic essays |
| **DAMAGE Table 9** | High quality; varied punctuation; occasional odd edits | Qualitative tier |
| **HumanizerBench** | **0.0% bypass** (100% detected) | 12-tool panel; GPTZero scorer |
| **Epaphras & Mtenzi 2026** | QuillBot 93.56% ADR; Grammarly grouped with paraphrasers, not top humanizers | WriteHuman 1.98% ADR baseline |
| **Chicago Booth** | Not tested | — |

**Takeaway:** Grammarly Humanizer is a **legitimate-editing paraphraser**, not a gray-market bypass engine. Students using it to "clear" GPTZero after pasting ChatGPT output will often fail against adapted detectors (Pangram, Turnitin 2026 bypasser layer, GPTZero 3.15b+ humanizer training). Students using it to **fix false-positive phrasing** on their own writing is the vendor's intended narrative — and overlaps unslop's defensive use case, but inside a detection vendor's walled garden.

### Institutional friction

- **Notre Dame** classifies Grammarly itself as generative AI under institutional policy ([docs/research/18-commercial-humanizer-tools/SYNTHESIS.md](../../docs/research/18-commercial-humanizer-tools/SYNTHESIS.md))
- **Brittany Carr case** (Liberty University): student dropped out after chasing Grammarly detector scores on **her own** writing — canonical false-positive + humanizer loop ([E-practical.md](../../docs/research/18-commercial-humanizer-tools/E-practical.md))
- Superhuman's response: Authorship reports + conservative detector + rewrite agents = **empowerment loop** within their ecosystem, not exit to third-party polish tools

---

## Authorship & process provenance

### Grammarly Authorship (pre-docs)

- Tracks: typed text, AI-generated spans, paste events, revisions
- Shareable report; student controls disclosure to instructor
- **5M+ students** on Google Docs + Microsoft Word integrations

### Authorship in docs (Mar 2026)

- **Default-on** in Superhuman Docs for education
- **Agent-specific attribution:** which Superhuman agent touched which span (Citation Finder, Proofreader, Reader Reactions, Humanizer, etc.)
- Admin-configurable agent allowlists per institution
- Framed as false-positive **defense** ("protects students from false AI-detection flags") and instructor **visibility**

### Strategic shift

| Era | Question |
|-----|----------|
| 2023–2024 | "What % AI is this document?" |
| 2025–2026 | "Show me how this document was made." |

Authorship + GPTZero Replay + agent attribution = **process verification stack**. Post-hoc humanization (whether Grammarly Humanizer or unslop anti-detector mode) becomes insufficient when institutions require Authorship reports or keystroke replay.

Superhuman owns both sides: generate with agents → track with Authorship → scan with dual detectors → rewrite with Humanizer. **Vertical integration** unmatched among mainstream vendors.

---

## GPTZero acquisition (Jun 2026)

| Field | Value |
|-------|-------|
| **Announced** | June 23, 2026 |
| **Terms** | Undisclosed; PitchBook ~$88M valuation cited |
| **GPTZero scale** | 19M registered users; ~$30M ARR; 30 employees; profitable since 2024 |
| **Total raised (GPTZero)** | $13.5M (seed + Series A) |
| **Leadership** | Edward Tian + Alex Cui join Superhuman authenticity team |
| **Product status** | GPTZero standalone continues; features migrating to Superhuman Go |

**Why acquire a "competitor"?**

Superhuman already had an AI detector. GPTZero adds:

- Education brand trust and institutional LMS footprint
- **Mixed / Polished / Paraphrased** granular taxonomy
- Writing Replay, AI Vision (feed-level detection), hallucination + citation verification
- Adversarial humanizer red-team cadence (15 model releases in 2025 alone — [AGENT-57](./AGENT-57-GPTZERO-EVOLUTION.md))

**Combined authenticity suite (Superhuman marketing):**

1. AI detection (dual models)
2. Hallucination detection
3. Plagiarism checking
4. Citation verification
5. AI Vision (browser feed scanning)
6. Authorship / replay tracking

This is the clearest **platform consolidation signal** in the detection/humanization market: the writing assistant bought the detector, not the other way around.

---

## Market implications

### 1. Legitimacy schism widens

Superhuman/Grammarly humanization = **clarity + voice + transparency**. Undetectable.ai / StealthGPT / Ryter Pro = **bypass metrics**. Mainstream press (PCMag, etc.) covers Grammarly; ignores bypass category. EU AI Act Article 50 (Aug 2026) pressures watermark removal and opaque evasion — Superhuman's posture is regulatory-durable; bypass vendors are not.

### 2. Bundled authenticity kills point-solution detectors for education

Institutions already buying Grammarly for Education get: detector + humanizer + Authorship + agents. Standalone GPTZero had LMS traction; now it's suite-included. Pangram/Originality must compete on **API accuracy** and **humanizer-resistant models**, not distribution.

### 3. Dual-detector becomes table stakes

Superhuman explicitly markets ensemble detection. Expect Turnitin, Copyleaks, and LMS vendors to cite multi-model or multi-signal ensembles. Single-detector green checks (including unslop benchmark gates) lose institutional credibility.

### 4. Process provenance > classifier evasion

Authorship + Replay shifts assessment design: "submit your process log" replaces "must score <20% AI." Humanizer arms race becomes secondary to **verifiable creation trails**. unslop file-rewriter is out of scope for provenance — document honestly.

### 5. Agentic writing homogenization

Eight+ agents producing rubric-aligned, tone-normalized, reader-optimized text accelerates **alignment-tax homogenization** ([AGENT-46](./AGENT-46-ALIGNMENT-TAX-HOMOGENIZATION.md)). Superhuman optimizes for clarity and institutional acceptability — the same gradient that produces AI slop before unslop subtracts it.

### 6. Competitive set expands beyond writing tools

Superhuman Go competes with Notion AI, ClickUp, Google Workspace AI, Microsoft Copilot — not just QuillBot/Jasper. Detection/humanization is a **feature** inside a productivity platform, not the product.

### 7. Open question: conflict of interest

Superhuman sells detector + humanizer + generative agents in one subscription. Same structural conflict as ZeroGPT/Undetectable vertical integration — but Superhuman discloses limits and pushes Authorship instead of "100% human guaranteed." Independent audits still required; vendor scorecards non-credible.

---

## unslop positioning

### Where Superhuman is strong (don't fight here)

| Superhuman strength | unslop response |
|--------------------|-----------------|
| 40M-user distribution, institutional contracts | Stay plugin/open-source; no GTM arms race |
| RAID-marketed detector + GPTZero ensemble | Don't claim detector bypass; cite independent audits |
| Authorship / process provenance | Out of scope; note limitation in anti-detector docs |
| Custom voice profiles from samples | unslop `voice-match` + stylometry is lighter-weight; different job |
| Multi-agent workflow (cite, grade, react) | unslop is polish layer, not assignment workflow |

### Where unslop wins

| unslop advantage | Why it holds |
|------------------|--------------|
| **Editor-native, zero context switch** | Superhuman requires extension/docs; unslop lives in Cursor/Claude/Codex session |
| **Byte-exact preservation** | Code, URLs, headings, tables protected — Superhuman rewrites prose holistically |
| **Transparent non-bypass posture** | No "beat Turnitin" marketing; credible to mainstream press Superhuman also targets |
| **Defensive ESL / false-positive narrative** | Superhuman owns detector side of same problem; unslop owns **voice polish without detector loop dependency** |
| **Open, auditable deterministic passes** | Regex + optional local DivEye; no black-box cloud paste box |
| **Anti-slop without warmth injection** | Superhuman Humanizer adds "warmth and nuance" — same RLHF gradient unslop explicitly avoids |
| **Developer/agent output focus** | Superhuman optimizes email, essays, memos; unslop optimizes **agent/codebase markdown** |

### Messaging frames (recommended)

1. **"Superhuman polishes inside their garden; unslop polishes inside yours."** No Authorship report, no suite lock-in, works in engineering IDEs.

2. **"Grammarly Humanizer is L1 paraphrase (0% bypass on HumanizerBench); unslop targets AI-ism removal, not detector defeat."** Cite DAMAGE/HumanizerBench; honest benchmark hygiene.

3. **"When institutions require Authorship, unslop can't help — and shouldn't pretend to."** Process verification is the endgame; unslop is pre-submission voice, not provenance forgery.

4. **"False-positive victims don't need another detector score to chase."** Brittany Carr loop is Superhuman-ecosystem pathology; unslop never ships a detector.

5. **"Structural entropy > synonym swap."** Superhuman Paraphraser/Humanizer operates at paragraph rewrite level; unslop's roadmap (structural.py, surprisal variance) targets signals RAID-trained detectors still weight.

### Documentation / product actions

| Priority | Action |
|----------|--------|
| **High** | Add Superhuman/Grammarly to SKILL.md landscape table: detection + humanization + Authorship stack |
| **High** | Fix any repo claims equating "humanizer" with Grammarly-class tools and bypass-category tools |
| **Medium** | `benchmarks/detector_bench.py`: log Superhuman/GPTZero model version when testing anti-detector outputs |
| **Medium** | Cross-link AGENT-57 (GPTZero) + AGENT-63 in UPDATE-PLAN-2026-08.md |
| **Low** | Monitor Superhuman Go agent SDK for third-party voice plugins — partnership unlikely but signals market |

### What unslop should NOT claim

- "Beats Grammarly's RAID #1 detector" — unsourced; conservative tuning ≠ unslop's job
- "Replacement for Authorship" — different product category
- "Same as Grammarly Humanizer" — unslop doesn't cloud-rewrite full documents via voice presets
- "Institutionally compliant" — Notre Dame treats Grammarly as gen-AI; unslop has no compliance certification

---

## Competitive landscape snapshot (Aug 2026)

| Vendor | Detection | Humanization | Provenance | Distribution | Bypass posture |
|--------|-----------|--------------|------------|--------------|----------------|
| **Superhuman (Grammarly+GPTZero)** | Dual detector; RAID #1 claim | Humanizer + Paraphraser agents | Authorship + Replay | 40M DAU; edu contracts | **Anti-bypass** (legitimate use) |
| **Turnitin** | LMS-integrated; bypasser layer | None | Similarity + AI report | Institutional default | N/A (instructor tool) |
| **Pangram** | Humanizer-trained DAMAGE model | None | API | B2B / API | N/A |
| **QuillBot** | Basic | Humanizer mode (~47% bypass) | None | Consumer freemium | Gray (coin-flip bypass) |
| **Undetectable.ai** | Internal (non-credible) | Core product | None | SEO/marketing | **Pro-bypass** |
| **unslop** | Optional TMR feedback | Deterministic + LLM polish | None | Plugin/pip | **Anti-bypass** (voice/ESL defense) |

---

## Bottom line

Superhuman is the **platform consolidation event** the detection/humanization market was heading toward: writing assistant acquires workspace, email, then the leading edu detector, and ships detection + humanization + provenance as one **academic-integrity bundle**. The Grammarly Humanizer is a **mainstream L1 paraphraser** with explicit anti-bypass ethics — strong for clarity, weak for evasion, **0% bypass** on independent humanizer panels.

For unslop, Superhuman is the **respectable incumbent** to differentiate against: same anti-slop goal, opposite architecture (cloud suite vs editor plugin), opposite detector relationship (built-in vs none). The durable unslop wedge is **editor-native voice polish with preserved code, no detector score chase, and honest limits on provenance-era institutions** — not competing with RAID leaderboards or Authorship reports.

The arms race endpoint is visible: **process verification beats post-hoc classification.** unslop should win the polish layer and document everything else as someone else's product.

---

## Related unslop repo artifacts

| Artifact | Relevance |
|----------|-----------|
| [AGENT-57-GPTZERO-EVOLUTION.md](./AGENT-57-GPTZERO-EVOLUTION.md) | GPTZero acquisition deep dive |
| [AGENT-15-RAID-BENCHMARK.md](./AGENT-15-RAID-BENCHMARK.md) | RAID #1 claim context |
| [AGENT-12-DAMAGE-DETECTOR.md](./AGENT-12-DAMAGE-DETECTOR.md) | Grammarly L1 tier |
| [AGENT-40-DAMAGE-HUMANIZER-TIERS.md](./AGENT-40-DAMAGE-HUMANIZER-TIERS.md) | L1 paraphraser inventory |
| [AGENT-62-CHICAGO-BOOTH-2026.md](./AGENT-62-CHICAGO-BOOTH-2026.md) | Grammarly not in Booth corpus |
| [docs/research/10-style-transfer-voice/D-commercial.md](../../docs/research/10-style-transfer-voice/D-commercial.md) | Grammarly voice + Superhuman rebrand |
| [docs/research/18-commercial-humanizer-tools/SYNTHESIS.md](../../docs/research/18-commercial-humanizer-tools/SYNTHESIS.md) | Legitimacy schism; Notre Dame; Brittany Carr |
