# Agent #76 — EU AI Act Article 50 (Aug 2026 in force)

**Topic:** Article 50 transparency obligations — AI marking, disclosure, GPAI interplay, grace periods, unslop compliance boundaries  
**Prepared:** August 19, 2026  
**Scope:** Regulation (EU) 2024/1689 Art. 50; AI Omnibus grandfathering; Commission Guidelines (Jul 2026); final Code of Practice on Transparency of AI-generated Content (Jun 2026); GPAI Code (Arts 53/55); commercial humanizer / humanization-tool implications  
**Status:** complete

---

## Executive summary

**Article 50** is the EU AI Act's **limited-risk transparency chapter**. It applies from **2 August 2026** to providers and deployers of in-scope AI systems whose outputs reach the EU — regardless of where the provider is headquartered.

Four distinct duties, split by role:

| Para | Who | Duty |
|------|-----|------|
| **50(1)** | Provider | Disclose when users interact with AI (chatbots, agents, avatars) unless obvious |
| **50(2)** | Provider | Mark synthetic audio/image/video/**text** in machine-readable format + ensure detectability |
| **50(3)** | Deployer | Inform people exposed to emotion-recognition or biometric-categorisation systems |
| **50(4)** | Deployer | Label deepfakes; label AI text on **public-interest** topics unless substantive human review + editorial responsibility |
| **50(5)** | Both | Detection/disclosure info must be clear, distinguishable, accessible at first exposure |

**Grace periods are narrow.** Almost everything bites **2 Aug 2026**. The only grandfathering is **Art. 50(2) marking/detection** for generative systems **already on market before 2 Aug 2026** → backstop **2 Dec 2026** (AI Omnibus). Hybrid systems still need **50(1) chat disclosure on 2 Aug**. Content generated before 2 Aug need not be retro-marked; content **published** after 2 Aug must be labelled even if generated earlier.

**GPAI split:** Art. 50 applies to **AI systems** (including GPAI systems). Art. 53/55 apply to **GPAI model providers** (documentation, copyright policy, training-data summary; systemic-risk extras). Two Codes of Practice — GPAI (model-level) and AI-content transparency (system/output-level) — are complementary. Downstream integrators are **not** GPAI providers; they inherit marking via upstream models and must classify their own product under Art. 50.

**Code of Practice (final, 10 Jun 2026):** Voluntary sign-up (~190 orgs by Jul 2026) but **legal obligations stand regardless**. No single technique meets the four statutory tests (effective, interoperable, robust, reliable) → **multilayer marking** default: signed metadata + imperceptible watermark + optional fingerprint/logging. Text exceptions: free-form prose cannot carry metadata → watermark-only layer; **<200 tokens** exempt from watermarking; closed physical products may use single layer. **Measure 1.2 / 1.5:** providers must **prohibit intentional mark removal** in ToS and must not market tools whose purpose is to **circumvent** machine-readable markings. Detection APIs required; expert-restricted access for short-text watermarks; cross-vendor interoperability target **2 Feb 2027**.

**Technical tension:** Academic and red-team literature (WaterPark, SIRA, BIRA, KGW reliability paper) shows paraphrase and humanization **statistically scrub** KGW/SynthID-class marks — the same rewrite passes unslop uses for voice. Regulators assume marking at generation; practitioners should assume **mark-after-edit** or accept mark loss. The law targets **deliberate removal**, not incidental side effects — but products marketed as "undetectable" or "watermark removal" sit in direct Art. 50 / Code crosshairs.

**Unslop verdict:** unslop is a **voice humanizer**, not a disclosure system and not a watermark stripper. Existing boundaries in `skills/unslop/SKILL.md` and `detector.py` align with Art. 50: anti-detector mode for ESL/resume false-positive defense; explicit refusal of watermark-removal workflows; advise provenance marking **after** humanization. **No new product surface needed** for compliance — but P1 doc actions: surface Art. 50 date in README compliance note; ensure no marketing language implies EU disclosure evasion.

---

## 1. Legal text — Article 50 structure

**Source:** Regulation (EU) 2024/1689, Article 50; consolidated at [artificialintelligenceact.eu/article/50](https://artificialintelligenceact.eu/article/50/)

### 1.1 Provider obligations

**Art. 50(1) — Interaction disclosure**

Providers of AI systems that **directly interact** with natural persons must design systems so users know they are interacting with AI, **unless obvious** to a reasonably well-informed, circumspect, observant person. Four cumulative criteria (Commission Guidelines §3): qualifies as AI system; genuine two-way exchange; direct communication (no human intermediary); with natural persons. Background / M2M systems out of scope. Notification from **first interaction**, clear and distinguishable, accessibility-compliant.

**Art. 50(2) — Machine-readable marking + detection**

> Providers of AI systems, **including general-purpose AI systems**, generating synthetic audio, image, video or **text** content, shall ensure that the outputs of the AI system are **marked in a machine-readable format** and **detectable as artificially generated or manipulated**.

Technical solutions must be **effective, interoperable, robust and reliable** as far as technically feasible, accounting for content type, cost, and state of the art. **Two linked elements** — marking without detection does not comply (Guidelines §4.2).

**Exemptions (Art. 50(2) second sentence + Guidelines):**

- Assistive function for **standard editing** that does not substantially alter deployer input or semantics
- Law-enforcement authorised use
- Out-of-scope outputs: very short symbol/number sequences; **source code**; M2M-only outputs; closed-loop industrial dev (unless final published output)
- Narrow **B2B/industrial** carve-out when conditions in Guidelines met
- **Very short text** (<200 tokens per final Code) — watermarking reliability insufficient

**Art. 50(5)** — information from (1)–(4) provided clearly at first interaction/exposure; accessibility requirements apply.

### 1.2 Deployer obligations

**Art. 50(3)** — notify people exposed to emotion-recognition or biometric-categorisation (real-time or ex-post).

**Art. 50(4) — Deepfakes and public-interest text**

- **Deepfakes** (Art. 3(60)): AI image/audio/video resembling existing persons/objects/events that would **falsely appear authentic**. Deployers must disclose at first exposure in human-perceptible form — **cannot rely on provider machine-readable marks alone**.
- **Public-interest text:** deployers must label AI-generated/manipulated **published** text intended to inform the public on politics, public admin, justice, fundamental rights, public health, environment, consumer safety, economic/financial/political/scientific/cultural debate topics.
- **Editorial exemption:** text with **substantive human review** (peer review, professional validation) + **editorial responsibility** (editor-in-chief authority) exempt. Spell-check / grammar-only does **not** qualify.

**Art. 50(6)** — law-enforcement carve-outs mirror provider side.

### 1.3 Penalties

**Art. 99** — up to **€15M** or **3% worldwide turnover** (whichever higher) for Art. 50 violations. SMEs/SMCs: lower of cap or percentage. EU institutions: up to €750k. Code signatory compliance may be **mitigating factor** in fine calculation (Guidelines §8.3).

---

## 2. Timeline and grace periods

| Date | What applies |
|------|----------------|
| **1 Aug 2024** | AI Act enters into force |
| **2 Feb 2025** | Prohibited AI practices (Art. 5) |
| **2 Aug 2025** | GPAI model obligations (Arts 53–55) |
| **2 Aug 2026** | **Article 50 fully applicable** — chat disclosure (50(1)), deployer labelling (50(3)(4)), marking for **new** generative systems (50(2)) |
| **2 Dec 2026** | **Grandfathering backstop** — Art. 50(2) marking/detection only for generative systems **placed on market before 2 Aug 2026** (AI Omnibus / Art. 111 amendment) |
| **2 Feb 2027** | Code signatories: cross-provider detection **interoperability** deadline |

### 2.1 What the grace period is NOT

- **Not** a general deferral of Art. 50 — deployer deepfake labelling, chatbot disclosure, emotion/biometric notice all apply **2 Aug 2026** even for legacy systems.
- **Not** retroactive marking — outputs generated before 2 Aug 2026 need not be marked; encouraged but not required.
- **Not** a publish-date escape — deepfakes/text **published on or after 2 Aug 2026** must be labelled even if generated earlier.
- **Not** extra-territorial immunity — non-EU providers subject when output used in EU (Art. 2; Guidelines §2).

### 2.2 Extraterritorial reach

Providers outside the EU fall under the Act when they **place AI on the EU market** or when **output is used in the EU** (Commission FAQ, Jul 2026). Humanizer tools consumed by EU users editing EU-facing content create indirect exposure for deployers; tool vendors marketing "bypass EU marking" to EU customers face direct provider/deployer-adjacent liability if they operate as generative systems or facilitate circumvention.

---

## 3. GPAI interplay — Articles 53, 55 vs Article 50

### 3.1 Role split

| Layer | Legal hook | Primary actor | Focus |
|-------|------------|---------------|-------|
| **GPAI model** | Arts 53, 55 | OpenAI, Google, Anthropic, Mistral, etc. | Technical documentation, copyright policy, training-data summary (Annex XII to downstream); systemic-risk mitigation if ≥10²⁵ FLOPs |
| **GPAI / generative system** | Art. 50 | Same or downstream integrator | User-facing transparency: interaction notice, output marking, deployer labelling support |
| **Downstream product** | Art. 50 (+ maybe Art. 6 high-risk) | App builder using GPT/Claude API | Classify **system** by use; obtain Annex XII package; implement or inherit marking |

**Key clarification (Guidelines §2.6):** Art. 50 does **not explicitly apply to GPAI models alone** — it applies to **AI systems**. Model providers are **encouraged** (and for systemic-risk models, may be required under Art. 55(1)(b)) to implement model-level marking to help downstream system providers comply. Downstream providers remain **responsible** for demonstrating Art. 50(2) compliance even when relying on upstream marks.

### 3.2 Two Codes of Practice

| Code | Finalised | Covers | Presumption |
|------|-----------|--------|-------------|
| **GPAI Code of Practice** | Jul 2025 | Arts 53, 55 — docs, copyright, safety for systemic-risk models | Adequate for GPAI provider obligations |
| **Transparency of AI-generated Content** | 10 Jun 2026 | Art. 50(2), (4), (5) — marking, labelling, detection | Adequate for marking/labelling obligations |

Commission FAQ: GPAI Code addresses **training-data transparency to authorities/downstream**; AI-content Code addresses **output marking toward exposed persons**. Model-level marking techniques in GPAI Code **facilitate** but do not replace system-level Art. 50 duties.

### 3.3 Open-source GPAI

Art. 53 documentation duties partially exempt open-source models unless systemic-risk tier. Art. 50(2) **still applies** when those models are integrated into generative systems placed on the EU market. Final Code Measure 1.2(b): open-source providers may document non-removal best practice in docs rather than enforce via license — but **downstream system provider** retains Art. 50 liability.

---

## 4. Code of Practice — marking architecture (Jun 2026 final)

**Sources:** [Code landing page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content); final PDF via same; Freshfields/Paul Weiss client memos (Jun 2026)

### 4.1 Multilayer default

Recital (b): *"no single active marking technique suffices… to meet effectiveness, interoperability, robustness and reliability"* → **Commitment 1: multi-layered marking**.

| Layer | Modality | Technique |
|-------|----------|-------------|
| **1.1.1 Metadata** | Image, video, document files | Digitally signed, time-stamped provenance in file metadata; ToS prohibits user stripping |
| **1.1.2 Watermark** | All; text >200 tokens | Imperceptible in-content watermark interwoven with content |
| **1.1.3 Fingerprint/logging** | Where 1.1.1–2 insufficient | Perceptual hash, prompt/output logs (proportionate; not general prompt retention mandate) |
| **1.2.1 Provenance certificate** | Free-form text (no metadata slot) | Signed manifest linking output to generating system |
| **1.2.2 Multimodal sync** | Cross-modal outputs | Marks survive single-modality swap |

**Single-layer exceptions:**

1. **Free-form text** — cannot embed metadata; watermark layer only (plus certificate)
2. **Closed physical product** — output technically confined inside device, not shareable online

### 4.2 Text-specific rules

- **>200 tokens:** watermark required; may have lower reliability → detection access restricted to **verified experts** (authorities, researchers, media) per Sub-measure 2.1.2
- **<200 tokens ("very short"):** watermark exempt — threshold expected to fall as tech improves
- **Source code:** Guidelines exclude from 50(2) scope (treated as distinct output class)

### 4.3 Non-removal and anti-circumvention (Measure 1.2 / 1.5)

Providers must:

- Retain upstream metadata marks when transforming input → output (good-faith processing excepted)
- **Prohibit intentional removal/tampering** in AUP/ToS/documentation
- **Neither market nor promote tools** whose purpose is to **circumvent** machine-readable markings

This is the direct regulatory hook for **Undetectable.ai-class "watermark remover"** SKUs and for humanizers explicitly marketed to **defeat provenance**, distinct from voice editing.

### 4.4 Detection obligations (Commitment 2)

- Free detector API/UI for marked content verification
- Human-readable detection results (Art. 50(5))
- Legacy detector handover if provider exits market
- **Measure 2.3:** forensic detectors for **unmarked** synthetic content encouraged for GPAI model providers — acknowledges watermark fragility
- **Interoperability by 2 Feb 2027:** industry-standard query routing so third parties need not run N vendor detectors

### 4.5 Deployer section (Commitment — Section 2)

- Standardised **EU icons** for labelling deepfakes and public-interest text
- Deepfake labels: perceptible at first exposure; artistic/satirical works — disclose without spoiling enjoyment
- Public-interest text: editorial-chain documentation if claiming exemption

### 4.6 Signatory advantage

Signatories (~190 by Jul 2026): presumption of conformity for covered measures, reduced admin burden, collaborative taskforces. Non-signatories: gap analysis vs Code, higher information-request risk from market surveillance authorities.

---

## 5. Commission Guidelines (20 Jul 2026)

**Source:** C(2026) 5054 final — [PDF](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf); FAQ updated 24 Jul 2026

### 5.1 Technical solution requirements (§4.2.3)

| Term | Meaning |
|------|---------|
| **Effective** | Enables distinguishing AI content; supports information-ecosystem integrity |
| **Reliable** | Accurate under nominal conditions across provider's output variety |
| **Robust** | Survives common alterations **and adversarial attacks** |
| **Interoperable** | Works across systems/actors; cross-vendor detection |

Providers may combine techniques (Recital 133 examples: watermarks, metadata, cryptography, logging, fingerprints). Marking may occur at **model, inference, or post-hoc system** stage; may rely on upstream/third-party solutions — **system provider remains liable**.

### 5.2 Standard editing vs generative (§4.3)

Assistive editing exempt when it does **not substantially alter** deployer semantics. Guidelines give practical examples: grammar/style correction in vs object removal / face swap / full rewrite out. **Humanizers that fully rewrite AI drafts are generative transformation, not "standard editing"** — output marking duty stays with the **original generative provider**; a humanizer that **generates new text** may itself become an Art. 50(2) provider if it places a generative system on the market.

### 5.3 Enforcement architecture (§8)

- **National market surveillance authorities** — primary enforcers
- **AI Office** — GPAI-integrated systems where same entity provides model + system; limited deployer role unless also deployer
- **EDPS** — EU institutions
- Complaint right for any affected person (Art. 85)

---

## 6. Technical reality — marking vs humanization

### 6.1 Known fragility (research consensus)

| Attack / process | Effect on KGW/SynthID-class marks | Source |
|------------------|-----------------------------------|--------|
| Cross-model paraphrase | Near-complete mark loss | SIRA (ICML 2025), BIRA (>99% ASR) |
| Human paraphrase | Detectable @ ~800 tokens (ICLR 2024) — not zero | Kirchenbauer reliability |
| Copy-paste 10% watermarked into human doc | TPR ≈ 0 | WaterPark DP-40 |
| unslop-style rewrite (burstiness, AI-ism strip, voice-match) | Statistical scrub — same mechanism, different intent | Agent #72, #74 |

**Regulatory assumption vs engineering reality:** Art. 50 and Code assume **robust** marks; field evidence says **paraphrase breaks statistical watermarks** at scale. Code Measure 2.3 (forensic detection) and expert-restricted short-text detectors are implicit admissions. Compliance officers should plan **provenance chain** (C2PA manifest + post-edit re-mark) not **generate-once-trust-forever**.

### 6.2 Metadata vs watermark for text

- **Metadata/C2PA:** survives until copy-paste into plain text; stripped on export to `.txt`, email body, most CMS paste
- **In-content watermark:** survives copy-paste; dies under rewrite
- **Final Code:** both layers where format allows; text gets watermark + provenance certificate

unslop operates on **plain prose** — metadata layer already gone before humanization; watermark layer is what side-effect rewrite degrades.

### 6.3 "Removal" vs "side effect"

| Scenario | Art. 50 / Code posture |
|----------|------------------------|
| Tool marketed to **strip SynthID/KGW/C2PA** | Prohibited circumvention product (Measure 1.2) |
| User runs humanizer to **sound human**, mark degrades incidentally | Not clearly prohibited — intent and product design matter |
| User runs anti-detector to **evade institutional disclosure** | Deployer-side Art. 50(4) violation if publishing unlabelled public-interest text |
| Provider ships humanizer **without** non-removal ToS clause | Provider-side gap if they also operate generative system |

EU law is **intent-sensitive** for circumvention products; **strict** for deployers publishing unlabelled synthetic public-interest content.

---

## 7. Commercial humanizer market — regulatory exposure

### 7.1 Category map (Aug 2026)

| Segment | Art. 50 exposure | Examples |
|---------|------------------|----------|
| **Detector-bypass humanizers** | High — marketing contradicts Code anti-circumvention; may facilitate deployer 50(4) violations | Undetectable.ai, HIX Bypass, StealthGPT |
| **Watermark-removal APIs** | Direct — Code forbids marketing circumvention tools | Smodin `watermark_removal` flag (cited Agent #72) |
| **Grammar/style humanizers** | Medium — if generative rewrite, may be Art. 50(2) provider; if editing-only, closer to standard-editing exemption | Grammarly, QuillBot |
| **Defensive ESL/resume tools** | Lower — legitimate false-positive use (Liang TOEFL bias) if not marketed for misconduct | unslop positioning |
| **Frontier model providers** | Provider 50(1)(2) — Gemini (SynthID shipped), OpenAI (no public text watermark Aug 2026), Anthropic | Agent #74, #75 |

### 7.2 Marketing vs ToS divergence

Industry audits (Cat. 18 research): most commercial humanizers say "100% undetectable" in headers while ToS disclaim academic misuse. Post–2 Aug 2026, EU-facing **"undetectable" + "remove AI traces"** copy is enforceable deception risk under Art. 50 + Unfair Commercial Practices Directive interaction (not modelled here in depth).

### 7.3 Turnitin / institutional layer

Turnitin shipped **AI bypasser detection** (Aug 2025); July 2026 product change retained paraphrase/bypasser signals (Agent #56). Art. 50 adds **regulatory** pressure on top of **institutional** arms race — universities may retreat from punitive detector use (Agent #69) while regulators require **disclosure**, not detection scores.

---

## 8. unslop compliance boundaries

### 8.1 What unslop is (regulatory classification)

| Question | Answer |
|----------|--------|
| Is unslop an Art. 50(2) **provider**? | **Probably not** as shipped — deterministic + optional LLM **rewriter** of existing text, not a generative system placed on market producing synthetic content from scratch. Re-classify if product adds **generation-from-prompt** as primary mode. |
| Is unslop a **deployer**? | Only if unslop-the-org publishes AI public-interest text without labelling — not the plugin's default use. |
| Does unslop **facilitate circumvention**? | **Anti-detector mode** targets post-hoc AI **detectors** (GPTZero, HF classifiers), not provider watermark detectors — legally distinct but mechanically overlapping. Boundary is **intent + marketing + user policy**. |

### 8.2 Current policy alignment (verified in repo)

From `skills/unslop/SKILL.md` Boundaries:

- AI-detector evasion for **ESL/resume false positives** — allowed with misconduct refusal
- **Watermark side effect documented** — rewrite may degrade SynthID/KGW; not a watermark remover
- **Art. 50 cited** — anti-detector not for circumventing disclosure obligations
- Dec 2025 Code multilayer marking + watermark-removal prohibition referenced

From `skills/unslop-file/scripts/detector.py` (lines 396–407):

- Feedback ladder exhaustion recommends **cross-model paraphrase** for detector evasion
- Explicit **"Do NOT attempt watermark removal — EU AI Act Article 50 prohibits it"**

From `unslop/CHANGELOG.md`:

- Documents Art. 50 refusal for watermark removal in detector feedback

**Verdict:** Policy is **already Art. 50-aware**. No code path implements watermark stripping; no BIRA/SIRA integration (Agent #72).

### 8.3 Allowed vs forbidden (Art. 50 lens)

| ✅ Allowed | ❌ Forbidden |
|-----------|-------------|
| Remove AI-isms, improve burstiness, voice-match | `--watermark-evade`, SynthID-aware stripping prompts |
| Anti-detector for ESL/resume **false-positive defense** | Marketing "EU undetectable" / "remove AI watermark" |
| Cross-model rewrite when detector ladder exhausts | Prompting rewrite **to defeat provenance checks** |
| Document incidental mark degradation honestly | Advising watermark-before-humanize for provenance chains |
| Refuse academic misconduct requests | Implementing circumvention tool marketplace |
| Cite Art. 50 in Boundaries / research | Silent degradation while claiming provenance preservation |

### 8.4 User guidance (compliance-safe)

1. **Need EU-disclosable public-interest content?** — Human review + editorial responsibility may exempt Art. 50(4); if not exempt, **label** regardless of detector score.
2. **Need technical provenance?** — Mark **after** final humanization (upstream model mark will not survive rewrite).
3. **Hit detector false positive?** — Anti-detector mode is defensible; still not a substitute for disclosure where law requires labelling.
4. **Academic submission?** — Decline; Art. 50 does not replace institutional honour codes.

### 8.5 Recommended repo actions

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P1** | README: one-line Art. 50 note + link to Boundaries | Product front door; non-programmer visibility |
| **P1** | Keep anti-detector marketing clear of "watermark" / "EU bypass" language | Code Measure 1.2 anti-circumvention |
| **P2** | `detector.py` exhaustion msg: add "may affect embedded provenance marks" | Already partially there; harmonize with SKILL |
| **P2** | Research synthesis cross-link this memo + Agent #74/#79 | C2PA vs statistical watermark split |
| **—** | Do **not** add watermark detector or re-marking feature | Out of scope; provider duty |
| **—** | Do **not** block rewrite based on mark detection | Would require mark detection = scope creep |

---

## 9. Debate and open questions

### 9.1 Supporter frame (regulatory)

- First binding **transparency floor** for synthetic content at scale
- Multilayer + interoperability timeline forces vendor coordination
- Editorial exemption preserves legitimate AI-assisted journalism with human gatekeeping
- Code signatory path reduces fragmentation across 27 member states

### 9.2 Critic frame (industry + research)

- **Robustness gap:** Code demands adversarial robustness; literature shows paraphrase breaks all deployed statistical schemes
- **200-token threshold:** Arbitrary; evasion via chunked generation
- **Enforcement asymmetry:** Frontier labs sign Code while shipping weak/no text marks (OpenAI, Anthropic)
- **False-positive mirror:** Expert-only short-text detection admits unreliability — same reliability problem as GPTZero on ESL writers (Agent #18)
- **Humanizer liability unsettled:** Side-effect mark loss vs intentional removal — case law TBD

### 9.3 Open questions for unslop

1. If EU user publishes unlabelled blog post after `unslop anti-detector`, who is deployer — user only, or also tool vendor? (Likely **user** as deployer; vendor exposure via circumvention marketing if any.)
2. Does `--surprisal-variance` (DivEye proxy tuning) increase watermark scrub correlation? Not measured — treat as unknown side effect.
3. Will harmonised EN standards subsume Code before 2027 interoperability deadline? CEN/CENELEC GPAI standards still pending (Art. 56 bridge).

---

## 10. Key dates reference card

| Event | Date |
|-------|------|
| Art. 50 application | **2 Aug 2026** |
| 50(2) marking grace (pre-market systems) | **2 Dec 2026** |
| Detection interoperability (Code signatories) | **2 Feb 2027** |
| First draft AI-content Code | 17 Dec 2025 |
| Final AI-content Code | 10 Jun 2026 |
| Commission Art. 50 Guidelines | 20 Jul 2026 |
| ~190 Code signatories | Jul 2026 |
| Max fine Art. 50 | €15M / 3% turnover |

---

## 11. Primary sources

| # | Resource | URL |
|---|----------|-----|
| 1 | Regulation (EU) 2024/1689 — Art. 50 | https://artificialintelligenceact.eu/article/50/ |
| 2 | Commission FAQ — Art. 50 | https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act |
| 3 | Guidelines on Art. 50 (Jul 2026 PDF) | https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf |
| 4 | Code of Practice — AI-generated content | https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content |
| 5 | First draft Code (Dec 2025) | https://digital-strategy.ec.europa.eu/en/library/first-draft-code-practice-transparency-ai-generated-content |
| 6 | EU icons for labelling | https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content (linked) |
| 7 | Art. 53 GPAI obligations | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53 |
| 8 | GPAI Code introduction | https://artificialintelligenceact.eu/introduction-to-code-of-practice/ |
| 9 | Freshfields — final Code analysis | https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-33-the-final-code-of-practice-on-transparency-of-ai-generate-102n4yx |
| 10 | Paul Weiss — final Code memo | https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content |
| 11 | Cooley — 2 Aug 2026 effective | https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026 |
| 12 | AI Act Service Desk — Art. 50 | https://ai-act-service-desk.ec.europa.eu/ |

---

## 12. Sibling agents and repo cross-refs

| Agent | Link |
|-------|------|
| **#74 KGW watermark** | Regulatory role §9; paraphrase fragility |
| **#72 BIRA attack** | unslop ethics boundary; mark scrub mechanism |
| **#71 SIRA** | Universal paraphrase attack on marks |
| **#75 SynthID-Text** | Production marking vs humanization |
| **#77 Watermark side effect** | Ethics deep-dive (pending) |
| **#79 C2PA / metadata** | Provenance layer vs statistical watermark (pending) |
| **#18 Liang ESL bias** | Anti-detector legitimacy frame |
| **#56 Turnitin 2025–26** | Institutional bypasser detection |
| **#69 Institutional retreat** | Detector retreat vs regulatory disclosure push |
| **#58 Originality.ai** | Commercial detector context |

**Repo files:** `skills/unslop/SKILL.md` (Boundaries); `skills/unslop-file/scripts/detector.py`; `docs/research/04-natural-language-quality/B-industry.md` §1.19; `docs/research/05-ai-text-detection-and-evasion/B-industry.md`; `docs/research/SYNTHESIS.md` finding #12; `docs/research/2026-08-detector-research/DEEP-RESEARCH-EXEC-SUMMARY.md` finding #9.

---

## 13. Bottom line

Article 50 is **in force now** (2 Aug 2026). It separates **provider marking** (machine-readable, detectable synthetic outputs) from **deployer labelling** (human-visible deepfakes and public-interest text). GPAI model rules (53/55) feed upstream; Art. 50 binds at the **system/output** layer. Grace until **2 Dec 2026** applies only to **50(2) marking** on generative systems already on market — everything else is live.

The Code of Practice makes explicit what the research already showed: **marks and humanization collide**. Products whose purpose is circumvention are directly targeted; humanizers whose purpose is **voice** must not cross into provenance stripping — documented side effects, honest boundaries, no EU-bypass marketing.

**unslop is aligned.** Stay a humanizer. Refuse misconduct. Refuse watermark removal. Tell users to mark after edit if provenance matters. Let frontier providers and deployers own Art. 50(2)/(4) compliance — unslop owns not making it worse on purpose.
