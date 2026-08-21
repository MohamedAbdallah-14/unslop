# Agent #79 — C2PA / Metadata Provenance vs Statistical Watermark

**Topic:** Content Credentials (C2PA), metadata provenance, text-manifest patterns, comparison to KGW/SynthID statistical watermarks, EU multilayer marking, unslop implications  
**Prepared:** August 19, 2026  
**Scope:** C2PA spec 2.2–2.4, CAI ecosystem, Jul 2026 synthetic-content white paper, Soft Binding Resolution API, production deployments (OpenAI, Google, Adobe), Integrity Clash research (CVPR 2026W), sibling agents #71/#74/#75/#76/#77  
**Status:** complete

---

## Executive summary

**C2PA** (Coalition for Content Provenance and Authenticity) is an open **cryptographic provenance** standard: a signed manifest (Content Credential) records who did what to an asset, bound to file bytes via hard-binding hashes. **Content Authenticity Initiative (CAI)** is the Adobe-led industry body; **Content Credentials** is the user-facing name for C2PA-signed metadata on a specific file. This is a **different layer** from **statistical watermarks** (KGW green-list, SynthID tournament sampling) that embed detectable bias in token or pixel distributions.

The two layers answer different questions and fail on different transforms:

| Layer | Question it answers | Dies on | Survives |
|-------|---------------------|---------|----------|
| **C2PA metadata** | Who signed what history for *these bytes*? | Copy-paste, screenshot, social re-encode, metadata strip | Controlled file handoff (JPEG/PDF/MP4 intact) |
| **Statistical watermark** | Does this text/pixels match a keyed generation pattern? | Paraphrase, humanization, SIRA/BIRA rewrite | Copy-paste of plain text (mark travels with content) |

**Text is the fracture line.** C2PA 2.4 still has no production-grade **in-file** embedding for plain `.txt`. Patterns: **PDF-embedded manifests** (supported), **crJSON sidecar** (2.4, not independently verifiable), **remote/cloud manifest stores** linked by soft binding. Copy-paste into email, CMS, or chat **severs metadata before any humanizer runs**. Statistical text watermarks (SynthID-Text on Gemini consumer, KGW in open tooling) survive paste but **SIRA/WaterPark-class paraphrase strips them** — the side effect unslop documents in `skills/unslop/SKILL.md`.

**Regulatory convergence (Aug 2026):** EU AI Act Art. 50(2) + final Code of Practice (10 Jun 2026) assume **multilayer marking** — signed metadata **and** imperceptible in-content watermark where format allows. Free-form text >200 tokens cannot rely on metadata alone; watermark layer required. No single layer survives the full edit/distribution chain. OpenAI ships **C2PA + SynthID** on images; Google ships **SynthID-Text** on consumer Gemini but **not** API text and **C2PA on media**; neither solves distributed plain-text provenance.

**Unslop verdict:** unslop operates on **plain prose**. C2PA is usually **already absent** at input. Rewrites degrade **statistical** marks as a documented side effect — not cryptographic manifest stripping. Policy unchanged: no watermark/C2PA-removal mode; users needing Art. 50 compliance should **disclose + re-mark after humanization** (C2PA-sign the published PDF, re-watermark at generation, or visible label). C2PA is the citation backbone for why **metadata provenance ≠ paraphrase-resistant AI detection** and why regulators mandate **both** layers despite humanizer supply-chain risk.

---

## 1. Standard identity

### 1.1 Naming (often conflated in marketing)

| Term | What it is |
|------|------------|
| **CAI** | Content Authenticity Initiative — Adobe-led industry coalition |
| **C2PA** | Coalition for Content Provenance and Authenticity — open **technical standard** (spec at spec.c2pa.org) |
| **Content Credentials** | User-visible provenance badge / manifest attached to a **specific asset** |
| **crJSON** | Content Credentials JSON — 2.4 derived view of manifest store; **not independently verifiable** |
| **JUMBF** | ISO 19566-5 container format for embedded manifest stores |

### 1.2 Spec timeline (relevant to text + AI)

| Version | Date | Text / AI relevance |
|---------|------|---------------------|
| **1.0** | 2022 | Core manifest model; PDF embedding (Appendix); sidecar for non-embeddable formats |
| **2.2** | May 2025 | Soft Binding Resolution API; PDF embedding appendix expanded; object-level manifests |
| **2.3** | ~2025 | Extended manifest patterns for **unstructured text** (file + sidecar paths) |
| **2.4** | Current (2026) | **crJSON**; `c2pa.ai-disclosure` assertion; synthetic-content guidance doc (Jul 2026) |

### 1.3 Primary normative + guidance docs

| Document | URL | Role |
|----------|-----|------|
| **C2PA Explainer 2.4** | https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html | Non-normative architecture overview |
| **Content Credentials spec 2.4** | https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html | Normative manifest/claim/signature |
| **Synthetic vs non-synthetic white paper** | https://c2pa.org/wp-content/uploads/sites/33/2026/07/Use-of-Content-Credentials-to-Identify-Synthetic-and-Non-Synthetic-Content.pdf | Jul 2026; `trainedAlgorithmicMedia`, ROI, `inputTo` prompts |
| **CAI assertions (actions)** | https://opensource.contentauthenticity.org/docs/manifest/writing/assertions-actions.md | `digitalSourceType` vocabulary |
| **c2pa-rs (Rust SDK)** | https://github.com/contentauth/c2pa-rs | Reference implementation ecosystem |

---

## 2. C2PA architecture — what metadata provenance is

### 2.1 Manifest stack

```
Asset bytes
    │
    ├── Hard binding (SHA-256 of content) ──► tamper-evident link
    │
    └── C2PA Manifest Store (JUMBF)
            ├── Assertions (statements: actions, ingredients, AI disclosure, …)
            ├── Claim (hash of assertions + bindings)
            └── Claim signature (COSE_Sign1 + X.509 chain)
```

**Hard binding:** any byte change invalidates the claim unless the editor re-signs with updated assertions (new manifest in chain).

**Soft binding:** fingerprint or invisible watermark in content used to **recover** a stripped manifest via Soft Binding Resolution API (2.2+) — bridges metadata loss on re-encode.

### 2.2 Embedding modes

| Mode | Mechanism | Typical formats |
|------|-----------|-----------------|
| **Embedded** | JUMBF inside container | JPEG (APP11), PNG, MP4/MOV, PDF stream, SVG (Base64; external preferred) |
| **Sidecar** | Separate `.c2pa` / crJSON alongside asset | Camera RAW, **plain text**, workflows forbidding embed |
| **Remote** | URL pointer → cloud manifest store | Large video, streaming |

C2PA white paper (Sep 2025): formats that **cannot embed** (including **text formats**) use sidecar + optional soft binding for discovery.

### 2.3 Trust model

- Verification = signature valid + hard binding matches + cert chain trusted (C2PA trust list).
- **Does not prove semantic truth** — only that a signer attested specific assertions about these bytes.
- Signer identity is the trust anchor; compromised or anonymous certs weaken evidential weight.
- Validators must warn on **invalid** manifests; unvalidated content is attacker-controlled text (spec UX guidance).

### 2.4 AI labelling assertions (Jul 2026 white paper)

Primary machine-readable AI signal on **`c2pa.actions.v2`**:

| `digitalSourceType` (IPTC) | Meaning |
|----------------------------|---------|
| `trainedAlgorithmicMedia` | Pure generative AI output |
| `compositeWithTrainedAlgorithmicMedia` | Human/origin asset + generative edit (inpaint, etc.) |
| `compositeSynthetic` | Composite with ≥1 generative element |
| `humanEdits` | Human edit with non-generative tools |

**New in 2.4:** `c2pa.ai-disclosure` assertion for explicit AI disclosure metadata.

**Generation recipe:** `inputTo` ingredient assertions can embed **text prompts**, reference images, hyperparameters — with PII/consent caveats.

**Regions of interest:** textual AI-modified spans in PDFs via W3C fragment selectors (tagged PDF) or page+rectangle (untagged).

Example (pure AI create):

```json
{
  "action": "c2pa.created",
  "when": "2026-03-15T14:30:00Z",
  "softwareAgent": { "name": "ExampleGen", "version": "3.5" },
  "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
}
```

---

## 3. C2PA for text — the hard case

### 3.1 Why text differs from images

| Property | Image/video C2PA | Plain text |
|----------|------------------|------------|
| Container for JUMBF | Yes (JPEG, MP4, PDF) | **No** standard plain-text embed in 2.4 |
| Typical user action | Download file | **Copy-paste** snippet |
| Metadata survival | Stripped by many platforms (OpenAI acknowledges) | **Gone on paste** |
| EU CoP posture | Metadata + watermark layers | **Watermark required**; metadata alone insufficient for free-form prose |

Engineering consensus (Jun–Aug 2026 practitioner guides): C2PA 2.4 **does not define robust in-file embedding for plain text**. Working patterns:

1. **PDF with embedded manifest** — first-class (ISO 32000 embedded file spec, `AFRelationship: C2PA_Manifest`).
2. **crJSON sidecar** — signed manifest + content hash shipped alongside `.txt`; **not universally standardized**; dies when user copies body only.
3. **Soft binding + manifest repository** — fingerprint/watermark lookup to reattach manifest (spec 2.2+ API); **no approved soft-binding algorithm list** in spec yet (ISCC under evaluation).
4. **Server-side generation log + hash lookup** — out-of-band provenance API (OpenAI Content Provenance API model for images).

### 3.2 Copy-paste as the universal metadata stripper

OpenAI (Feb 2024): C2PA on DALL-E images is **not a silver bullet** — social platforms remove metadata; screenshots remove it. Same applies to text sidecars: the moment prose enters a chat box, email, or Google Doc paste, **no C2PA travels**.

**Implication for unslop:** typical workflow is already **metadata-free plain text** at humanization time. unslop does not "strip C2PA" — users paste without it.

### 3.3 PDF as the text provenance carrier

For documents that must retain credentials:

- Embed manifest at generation or export.
- Human **edit** (including unslop on extracted text → re-export) **invalidates hard binding** unless tool re-signs with `c2pa.edited` + updated hash.
- Tagged PDF ROI can mark **which paragraphs** were AI-modified — relevant for hybrid human+AI workflows.

### 3.4 crJSON (2.4)

- Human-readable JSON-LD-ish view of manifest store.
- Explicitly **derived, not independently verifiable** — debugging/interop, not a substitute for JUMBF+signature verification.
- Sidecar pattern: `document.txt` + `document.crjson` (or `.c2pa`).

---

## 4. Statistical watermarks — KGW and SynthID-Text (recap)

Detailed memos: **#74 KGW**, **#75 SynthID**. Summary for comparison:

### 4.1 KGW (Kirchenbauer et al., ICML 2023)

| Aspect | Detail |
|--------|--------|
| **Mechanism** | Keyed PRF → green/red vocab partition; logit bias δ at sample time |
| **Detection** | Key-only z-test on green-token rate; no model weights |
| **Deployment** | Open-source default (MarkLLM, vLLM-Watermark); **not** ChatGPT production |
| **Robustness** | WaterPark DP-40: TPR 0.993 → **0.485**; SIRA **~100% ASR** @ $0.88/M tok |

### 4.2 SynthID-Text (Dathathri et al., *Nature* 2024)

| Aspect | Detail |
|--------|--------|
| **Mechanism** | LeftHash(h=4) + tournament sampling over g-functions |
| **Deployment** | Gemini App/Web **yes**; Gemini API text **no** (Google forum 2026) |
| **Robustness** | SRI Lab: **>90% scrubbing** without key stealing; WaterPark DP-40 TPR 0.998 → **0.498** |
| **Detection** | Key-only weighted g-value / Bayesian detector; **no public text portal** (image/audio/video only) |

### 4.3 What statistical marks are good at

- Proving **"this string came from model M with key K"** without access to model internals.
- Surviving **metadata strip** (copy-paste, re-upload) — signal lives in content statistics.
- **Failing** paraphrase, humanization, translation — same transform class as unslop rewrites.

---

## 5. Head-to-head comparison

### 5.1 Mechanism and verification

| Dimension | C2PA metadata | KGW / SynthID statistical |
|-----------|---------------|---------------------------|
| **Signal location** | File container / sidecar | Token or pixel distribution |
| **Crypto** | X.509 + COSE signatures | Pseudorandom keyed bias |
| **Verifier needs** | Manifest bytes + trust list | Watermark key (or API) |
| **Proves** | Signed assertion history | Statistical fit to generation process |
| **Tamper model** | Byte change breaks hard binding | Edit breaks green/g-value pattern |
| **Spoofing** | Forge manifest with valid cert | Forge green pattern (Sadasivan spoofing) |

### 5.2 Survival under transforms (text-focused)

| Transform | C2PA metadata | Statistical watermark |
|-----------|---------------|----------------------|
| **Copy-paste to plain text** | **Lost** (sidecar not copied) | **Retained** |
| **Paraphrase / humanize / unslop** | N/A if already plain; PDF edit **invalidates** unless re-signed | **Degraded / removed** (SIRA, WaterPark, DAMAGE) |
| **Export .txt from PDF** | **Lost** | N/A (watermark on text if marked at gen) |
| **Social platform re-upload** | Often **stripped** (images) | Image SynthID better; text re-tokenization varies |
| **Screenshot** | **Lost** | N/A for text |
| **10% paste into human doc** | N/A | z-score / TPR **≈0** (WaterPark dilution) |

### 5.3 Complementarity (why regulators want both)

```
Generation ──► [Statistical watermark in content] ──► survives metadata strip
       │
       └──► [C2PA manifest on file] ──► survives paraphrase IF file untouched
                    │
                    └── soft binding ──► recover manifest after re-encode (images)
```

**Neither alone** covers: paste-heavy text workflows **or** rewrite-heavy editing pipelines.

EU Code of Practice (Agent #76): **multilayer marking** default — metadata + imperceptible watermark + optional logging. Text >200 tokens: **watermark-only** in-content layer mandatory; metadata supplements where container exists.

---

## 6. Production deployments (Aug 2026)

| Provider | C2PA | Statistical watermark | Text notes |
|----------|------|----------------------|------------|
| **OpenAI** | DALL-E 3, Sora, ChatGPT image edits (Steering Committee) | **SynthID** on images/audio from ChatGPT/API | **No** public text watermark; Content Provenance API checks C2PA+SynthID on **images** |
| **Google DeepMind** | Imagen, Gemini **media** | **SynthID-Text** on Gemini **consumer**; SynthID on image/audio/video | API text **not** watermarked |
| **Adobe** | Firefly, Photoshop (CAI origin) | Partner ecosystem | Document workflows via PDF |
| **Meta** | Platform labeling tools | Meta Seal (images) | — |
| **Microsoft** | C2PA in ecosystem | — | — |

**OpenAI dual-layer (2026):** advancing content provenance blog — **C2PA conformant** + **SynthID** watermark as complementary; public verification tool checks **both** signals on uploaded images.

**Scale claim (industry):** SynthID + C2PA dual-layer cited at **10B+** marked assets (Jan 2026 industry surveys) — overwhelmingly **image/video**, not plain text.

---

## 7. Integrity Clash — when layers disagree

**Paper:** *Authenticated Contradictions from Desynchronized Provenance and Watermarking* (Nemecek et al., CVPR 2026W APAI; [arXiv:2603.02378](https://arxiv.org/abs/2603.02378))

**Finding:** C2PA manifest validation and watermark detection are **independent procedures**. An asset can pass both checks while **contradicting itself**:

- Valid C2PA manifest asserts **human edit only** (`c2pa.edited`, no `trainedAlgorithmicMedia`).
- Pixel-level watermark still detects **AI generation**.

**Cause:** C2PA does **not mandate** AI-origin disclosure on every edit manifest — omitting `digitalSourceType` is spec-legal. Watermark embedded at generation **survives** C2PA-compliant re-sign that mis-describes origin.

**Conflict matrix (simplified):**

| Manifest | Watermark | State |
|----------|-----------|-------|
| Absent/invalid | Absent | Q1 Silent |
| Absent | Detected | Q2 Fragile provenance (watermark only) |
| Valid, no AI claim | Absent | Q3 Metadata-only trust |
| Valid, AI disclosed | Detected | Q4a Verified synthetic |
| Valid, **no** AI claim | Detected | **Q4b Integrity Clash** |

**Mitigation proposed:** joint audit protocol — verifiers must cross-check manifest assertions against watermark signals.

**Text relevance:** Same structural desync possible if text ever ships **both** C2PA sidecar and SynthID-Text — editor re-signs manifest as `humanEdits` while statistical mark persists. Humanizer that rewrites tokens without updating manifest creates **false Q3** (looks human-edited in metadata) while watermark degrades — or **Q4b** if watermark partially survives.

---

## 8. Attack and failure catalog by layer

### 8.1 C2PA-specific

| Attack / failure | Effect |
|------------------|--------|
| Metadata strip (platform, paste, screenshot) | Provenance **gone**; no negative signal |
| Strip + re-sign false history | **Mis-provenance** with valid signature (trust problem) |
| Integrity Clash (Q4b) | **False human attribution** with valid manifest |
| Sidecar not shipped | Validator finds nothing — indistinguishable from never-marked |
| crJSON without JUMBF verify | False sense of security if treated as proof |
| Phone-home sidecar URL | Spec warns of validator privacy risks |

### 8.2 Statistical watermark-specific

| Attack / failure | Effect | Source |
|----------------|--------|--------|
| Paraphrase (DIPPER, GPT) | TPR collapse | WaterPark, DAMAGE |
| SIRA / BIRA targeted rewrite | ~100% / >99% removal | Agents #71, #72 |
| Copy-paste dilution | TPR ≈ 0 | WaterPark CP1-10 |
| Spoofing | Forge AI mark on human toxic text | Sadasivan |
| Key stealing + scrub | ~100% removal (SynthID) | SRI Lab |

### 8.3 Humanization (unslop class) — which layer breaks?

| unslop input | C2PA effect | Watermark effect |
|--------------|-------------|------------------|
| Plain pasted ChatGPT prose | Already **no C2PA** | **Degrades** SynthID/KGW if present |
| PDF with embedded manifest, user extracts text | Metadata **left in PDF**; pasted excerpt **unmarked** | Rewrite strips watermark in extracted text |
| Full PDF re-export after unslop | Hard binding **invalid** unless re-signed | Depends on whether rewrite applied in signed tool chain |
| Anti-detector / cross-model paraphrase | Metadata N/A | **Near-complete** statistical scrub |

---

## 9. Regulatory framing (Art. 50 + Code of Practice)

Cross-ref **Agent #76**. Points specific to C2PA vs watermark:

| Code / Guidelines element | C2PA role | Watermark role |
|---------------------------|-----------|----------------|
| **Multilayer marking (Measure 1.x)** | Signed metadata layer | Imperceptible in-content layer |
| **Text >200 tokens** | Metadata **insufficient alone** | Watermark **required** |
| **Text <200 tokens** | Exempt from watermark reliability requirement | — |
| **Interoperability target (Feb 2027)** | C2PA as de facto metadata standard | Cross-vendor watermark TBD |
| **Anti-circumvention (Measure 1.2)** | Forbids tools marketed to strip **either** layer | Same |
| **Provider reliance (Guidelines point 74)** | Deployer may rely on upstream marking **when present** | Same — but Gemini API text has **no** Google mark |

**Compliance engineering reality:** Mark-at-generation → humanize → **mark lost or invalid**. Compliant pipeline for edited AI prose:

1. Generate → 2. Humanize (accept watermark loss) → 3. **Re-disclose** (visible label) + **re-sign C2PA on published PDF** + optional re-generation watermark pass.

unslop sits at step 2 — **supply-chain provenance risk**, not a C2PA stripper.

---

## 10. unslop integration

### 10.1 What unslop touches

| Layer | Touched by unslop? | Mechanism |
|-------|-------------------|-----------|
| C2PA embedded in PDF | **Indirectly** — only if user re-exports edited PDF without re-signing | Hard binding invalidation |
| C2PA sidecar / crJSON | **No** — not parsed or deleted | User never passes sidecar to text humanizer |
| Plain text statistical watermark | **Yes** — side effect of token rewrites | Same as DIPPER/SIRA class |
| Post-hoc AI **detection** | Anti-detector mode targets **detectors**, not C2PA | Different threat model |

### 10.2 Policy (aligned with #71, #74, #76, #77)

Existing language in `skills/unslop/SKILL.md`:

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks… Users who need provenance should watermark **after** unslop, not before.

**Extend conceptually to C2PA:**

> C2PA credentials bind to **file bytes**. unslop humanizes **plain text**. Metadata provenance is typically already absent at paste time. For PDF workflows, editing text without a C2PA-aware re-sign invalidates the manifest. Users needing Content Credentials should sign **after** final edit/export.

**Do not:**

- Add C2PA strip, crJSON removal, or manifest-spoofing features.
- Market anti-detector as Art. 50 / Content Credentials evasion.
- Claim unslop preserves or verifies provenance.

**Do:**

- Cite C2PA vs watermark split in research synthesis and enterprise FAQ.
- Recommend workflow: **humanize → disclose → re-mark file**.
- Pair with SIRA/WaterPark citations for statistical layer fragility.

### 10.3 Optional product actions

| Priority | Action |
|----------|--------|
| **P2** | GETTING_STARTED / Boundaries: one paragraph on C2PA (metadata, file-bound) vs watermark (statistical, rewrite-fragile) |
| **P2** | Anti-detector exhaustion note: may affect embedded provenance marks **and** detector scores |
| **P3** | Enterprise brief: PDF export checklist (re-sign after unslop) |
| **—** | Do **not** add C2PA verify/sign to `humanize.py` — out of scope, key management liability |
| **—** | Do **not** add watermark detector to warn pre-rewrite — keyless KGW guess unreliable; scope creep |

### 10.4 Anti-detector vs provenance (framing)

| User goal | unslop stance |
|-----------|---------------|
| ESL false positive / resume polish | Supported (defensive) |
| Strip SynthID/KGW for misconduct | Refused |
| Strip C2PA to evade disclosure | Refused (even though paste usually already did) |
| Publish EU public-interest AI text without label | Refused; not a product goal |
| Humanize then properly re-mark for compliance | **Supported** — document how |

---

## 11. Key numbers and claims

| Claim | Value / status | Source |
|-------|----------------|--------|
| C2PA spec (current) | **2.4** | spec.c2pa.org |
| PDF manifest embedding | Normative (ISO 32000 embedded file) | C2PA spec Appendix |
| Plain-text in-file embed | **Not standardized** in 2.4 | Practitioner guides Jun 2026 |
| crJSON independently verifiable | **No** | C2PA 2.4 |
| OpenAI DALL-E C2PA overhead | ~3% PNG (~90KB on 3.1MB) | OpenAI Feb 2024 |
| OpenAI metadata strip admission | Social upload + screenshot | OpenAI blog |
| SynthID scrubbing (images) | >90% without stealing | SRI Lab |
| SynthID-Text WaterPark DP-40 | TPR 0.998 → **0.498** | Agent #20 |
| KGW WaterPark DP-40 | TPR 0.993 → **0.485** | Agent #74 |
| SIRA ASR (7 schemes) | **~100%** | Agent #71 |
| EU text watermark threshold | **>200 tokens** | Code of Practice / Agent #76 |
| EU Art. 50 in force | **2 Aug 2026** | Regulation 2024/1689 |
| Integrity Clash (Q4b) | Demonstrated on SDXL pipeline | Nemecek CVPR 2026W |
| Gemini API text SynthID | **Not shipped** | Google dev forum 2026 |

---

## 12. Open questions

1. **Will C2PA 2.5+ standardize plain-text embedding** (Unicode variation-selector wrapper cited in some implementer notes) or stay sidecar-first?
2. **Soft binding for text:** ISCC or other fingerprint on prose — enough for manifest recovery after edit, or trivially broken by synonym swap?
3. **Joint verification UX:** Will browsers/platforms adopt Integrity Clash audit (Q4b) or continue showing metadata-only badges?
4. **PDF re-sign after humanize:** Is there a C2PA-aware humanizer category (`humanEdits` + `digitalSourceType` preservation) — market gap?
5. **OpenAI text path:** Permanent C2PA+SynthID skip, or EU pressure forces API text marking by Dec 2026 grace?
6. **unslop PDF pipeline:** Should file-rewriter skill warn on C2PA PDF input without attempting verify?
7. **crJSON in the wild:** Adoption rate vs JUMBF embed — affects enterprise checklist wording.

---

## 13. Cross-references (sibling agents)

| Agent | Relevance to #79 |
|-------|------------------|
| **#20 WaterPark** | Statistical watermark paraphrase failure rates |
| **#70 OpenAI shutdown** | Pivot to C2PA+SynthID vs post-hoc text classification |
| **#71 SIRA** | Statistical strip at commodity cost; multilayer response |
| **#72 BIRA** | >99% evasion; supply-chain provenance risk |
| **#74 KGW** | Statistical baseline; regulatory default cite |
| **#75 SynthID** | Production text watermark; API/consumer split |
| **#76 EU Art. 50** | Multilayer mandate; metadata vs watermark for text |
| **#77 Watermark ethics** | Side effect vs intent; C2PA named as separate layer |
| **#78 Integrity vs ESL** | Disclosure framing when marks fail |

---

## 14. Primary URLs

| Resource | URL |
|----------|-----|
| C2PA Explainer 2.4 | https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html |
| Content Credentials spec 2.4 | https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html |
| Synthetic content white paper (Jul 2026) | https://c2pa.org/wp-content/uploads/sites/33/2026/07/Use-of-Content-Credentials-to-Identify-Synthetic-and-Non-Synthetic-Content.pdf |
| CAI / C2PA org | https://c2pa.org |
| OpenAI C2PA announcement | https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/ |
| OpenAI advancing provenance (SynthID+C2PA) | https://openai.com/index/advancing-content-provenance/ |
| OpenAI Content Provenance API | https://developers.openai.com/api/docs/guides/content-provenance |
| Google SynthID | https://deepmind.google/models/synthid/ |
| Integrity Clash paper | https://arxiv.org/abs/2603.02378 |
| KGW paper | https://arxiv.org/abs/2301.10226 |
| SynthID-Text (*Nature*) | https://doi.org/10.1038/s41586-024-08025-4 |
| EU Art. 50 consolidated | https://artificialintelligenceact.eu/article/50/ |

---

## 15. Key citations

```bibtex
@techreport{c2pa2024spec,
  title={Content Credentials: C2PA Technical Specification},
  author={{Coalition for Content Provenance and Authenticity}},
  year={2024},
  note={Version 2.4},
  url={https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html}
}
```

```bibtex
@techreport{c2pa2026synthetic,
  title={Use of Content Credentials to Identify Synthetic and Non-Synthetic Content},
  author={{Coalition for Content Provenance and Authenticity}},
  year={2026},
  month={July},
  url={https://c2pa.org/wp-content/uploads/sites/33/2026/07/Use-of-Content-Credentials-to-Identify-Synthetic-and-Non-Synthetic-Content.pdf}
}
```

```bibtex
@inproceedings{nemecek2026integrityclash,
  title={Authenticated Contradictions from Desynchronized Provenance and Watermarking},
  author={Nemecek and others},
  booktitle={CVPR Workshops (APAI)},
  year={2026},
  url={https://arxiv.org/abs/2603.02378}
}
```

```bibtex
@inproceedings{kirchenbauer2023watermark,
  title={A Watermark for Large Language Models},
  author={Kirchenbauer, John and Geiping, Jonas and others},
  booktitle={ICML},
  year={2023},
  url={https://arxiv.org/abs/2301.10226}
}
```

```bibtex
@article{dathathri2024synthid,
  title={Scalable watermarking for identifying large language model outputs},
  author={Dathathri, Sumanth and others},
  journal={Nature},
  volume={634},
  pages={818--823},
  year={2024},
  doi={10.1038/s41586-024-08025-4}
}
```

---

## 16. Synthesis one-liner (for README / SKILL landscape)

**C2PA proves signed history for a file; KGW/SynthID prove statistical generation bias in the content. Copy-paste kills the first; paraphrase kills the second. EU Art. 50 asks for both anyway. unslop humanizes plain text — metadata is usually already gone, watermarks may fall as a side effect — so mark and disclose after editing, not before.**
