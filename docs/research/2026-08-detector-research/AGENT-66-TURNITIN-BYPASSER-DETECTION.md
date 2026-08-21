# Agent #66 — Turnitin Bypasser Detection Category

**Topic:** Turnitin's "AI bypasser" detection category — taxonomy, LLM-DetectAIve Class III mapping, vendor claims vs independent reality, unslop positioning  
**Prepared:** August 19, 2026  
**Scope:** Turnitin press/docs (Aug 2025–Jul 2026), LLM-DetectAIve (EMNLP 2024), independent humanizer tests, academic provenance literature  
**Status:** complete  
**Cross-ref:** [Agent #56](./AGENT-56-TURNITIN-2025-2026.md) (product timeline), [Agent #10](./AGENT-10-LLM-DETECTAIVE.md) (4-way taxonomy), [Agent #12](./AGENT-12-DAMAGE-DETECTOR.md) (humanizer audit), [Agent #62](./AGENT-62-CHICAGO-BOOTH-2026.md) (Booth attribution fix)

---

## Executive summary

Turnitin's **bypasser detection category** is the commercial name for what academic literature calls **machine-written → machine-humanized (M→MH) text** — LLM-DetectAIve **Class III**. Turnitin shipped it **August 27, 2025** as an integrated layer inside existing AI writing detection, not a separate product. English only. No published bypasser recall, no published bypasser FPR, no training-tool list.

The category sits in a three-layer commercial stack:

| Layer | Turnitin label (pre-Jul 2026 UI) | Academic analog | Target pipeline |
|-------|----------------------------------|-----------------|-----------------|
| Raw LLM output | "AI-generated only" (blue) | DetectAIve **Class II** (MG) | Prompt → LLM, no edit |
| Paraphrase / spinner | "AI-generated text that was AI-paraphrased" (purple) | MixSet "rewrite"; QuillBot-class | LLM → synonym/order swap |
| **Bypasser / humanizer** | Merged into "AI-generated only" (Aug 2025+); unified blue (Jul 2026) | DetectAIve **Class III** (M→MH) | LLM → LLM "make human" |

**Vendor claims vs reality:** Turnitin claims integration with "leading bypassers," CPO framing of humanizer vendors as "cheating providers," and document-level FP <1% on scores ≥20%. Reality: Blommerde (Northumbria, Sept 2025) — StealthGPT 0%→72%, Groby 0%→67%, Easy Essay still 0%; all flags labeled generic "AI generated" with no bypasser sub-label. Booth (2025) **did not test Turnitin**. No peer-reviewed bypasser benchmark exists. The absence of vendor metrics **is** the finding.

**LLM-DetectAIve Class III:** EMNLP 2024 demo; 95.71% in-domain accuracy on synthetic M→MH (LLM-on-LLM humanize prompts); **60–67% OOD** on IELTS ESL / MixSet. Class III training prompts ("Rewrite this text to make it sound more natural and human-written") match commercial humanizer behavior but **exclude** cross-model paraphrase, TempParaphraser, commercial SaaS tools, and unslop structural passes. Turnitin's bypasser layer is best read as **production Class III detection** trained on adversary corpora — same arms-race pattern as Originality Turbo 3.0.2 (Agent #58) and GPTZero humanizer layer (Jan 2026).

**Unslop honest positioning:** Anti-detector mode on AI-origin text produces **Class III-shaped output** — the exact evasion category both Turnitin and DetectAIve target. Do not market as "beat Turnitin." Cross-model second pass remains the strongest lever the skill can recommend; `--surprisal-variance` is the DivEye-aligned measurement hook. Fix SKILL.md: Booth did not test Turnitin; the "60–85% at Booth" line is unsupported.

---

## 1. Category definition — what "bypasser" means

### 1.1 Turnitin vendor definition

From the [Aug 27, 2025 press release](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers):

> AI bypasser tools, or "humanizers," which allow students to disguise AI-generated text as human-written, evading detection by both teachers and AI tools.

Operational rule (release notes): the report category **"AI-generated only"** now includes text that **may have been modified by an AI bypasser tool** — i.e., bypasser hits are not a separate UI class; they merge into the raw-AI bucket.

Key vendor constraints:

- **English only** for bypasser detection (Spanish/Japanese get LLM detection without bypasser/paraphrase layers as of May 2026).
- **No separate integration** — bundled in Turnitin Originality / iThenticate 2.0 AI add-on.
- **No adversary list published** — "leading bypassers" only.

### 1.2 How bypasser differs from paraphrase (Turnitin taxonomy)

Turnitin had already split raw vs paraphrased before bypasser shipped:

| Date | Category split | Example vendor named |
|------|----------------|----------------------|
| Jul 16, 2024 | "AI-generated only" vs "AI-generated text that was AI-paraphrased" | QuillBot (word spinner) |
| Aug 27, 2025 | Bypasser text → **folded into** "AI-generated only" | Humanizer SaaS (StealthGPT-class) |
| Jul 20, 2026 | Single blue highlight for all AI signal | Raw + paraphrased + bypassed unified |

**Conceptual distinction (inferred from product evolution):**

- **Paraphrase (AIR-1):** lexical/order perturbation on AI text — synonym swap, sentence reorder. QuillBot, DIPPER-light.
- **Bypasser:** full rewrite pass whose **stated goal** is detector evasion — "humanize," "undetectable," "bypass Turnitin." Often adds burstiness injection, typo noise, contraction forcing.

Turnitin treats both as AI-origin signal but historically separated paraphrase (purple) from raw (blue) until the Jul 2026 UI simplification. Bypasser was never given its own color — it entered through the raw-AI channel.

### 1.3 Industry "bypasser" as product category

Gray-market humanizers share a product shape (Agent #61, #12):

- Paste-box web app + built-in "all green" detector panel
- Marketing: "99% undetectable," "bypass Turnitin/GPTZero/Originality"
- Rewrite policy: minimize detector score, not editorial quality
- DAMAGE L1/L2/L3 fluency tiers — bypass rate and quality are **inversely correlated**

Turnitin's CPO Annie Chechitelli explicitly frames these vendors as **"a new category of cheating providers"** — parallel to essay mills, but AI-native and subscription-priced ($8–15/mo).

---

## 2. LLM-DetectAIve Class III — academic formalization

### 2.1 The four-class provenance ladder

[LLM-DetectAIve](https://arxiv.org/abs/2408.04284) (Abassy et al., EMNLP 2024 Demo) defines:

| Class | Label | Pipeline | Policy stance |
|-------|-------|----------|---------------|
| **I** | Human-Written (HW) | Human only | Always allowed |
| **II** | Machine-Generated (MG) | Prompt → LLM | Prohibited in education |
| **III** | Machine-Written → Machine-Humanized (M→MH) | LLM draft → LLM obfuscation pass | **Bypasser category** — adversarial |
| **IV** | Human-Written → Machine-Polished (H→MP) | Human draft → LLM grammar/style | Context-dependent (OK in journals; banned in zero-tolerance K–12) |

Class III is defined explicitly as detecting **"attempts to obfuscate the fact that a text was machine-generated."** That is the academic name for Turnitin's bypasser category.

### 2.2 Class III training data (paper §2.3)

103,852 M→MH examples generated with prompts including:

- *"Rewrite this text to make it sound more natural and human-written"*
- *"Rephrase this text to be easy to understand and personable"*

Generators: GPT-4o, Llama3-8B/70B, Mixtral-8x7B, Gemma-7B/2-9B, Gemini-1.5, Mistral-7B. Same-model humanization — **not** cross-model paraphrase.

Post-processing strips LLM preamble artifacts ("Sure!", "Here is the paraphrased text:") to avoid trivial class leakage.

### 2.3 DetectAIve performance on Class III

| Condition | Accuracy | Macro-F1 | Notes |
|-----------|----------|----------|-------|
| In-domain (M4GT-style) | **95.71%** | **95.72%** | DeBERTa-base universal model |
| IELTS ESL essays (OOD) | **66.91%** | 66.55% | ESL equity risk |
| MixSet mixtext (OOD) | **60.08%** | 54.95% | Subtle humanization near-random |

Primary confusion pair: **III ↔ IV** — obfuscated AI vs polished human. The humanizer arms race lives at this boundary.

### 2.4 Mapping table: Turnitin ↔ DetectAIve ↔ MixSet ↔ unslop

| Workflow | Turnitin (Aug 2025+) | DetectAIve | MixSet operation | unslop mode |
|----------|---------------------|------------|------------------|-------------|
| ChatGPT essay, submit raw | AI signal (blue) | **II** | `complete` / raw gen | N/A (input) |
| ChatGPT → QuillBot synonym swap | AI signal (was purple) | II or III (ambiguous) | `rewrite` (lexical) | N/A |
| ChatGPT → StealthGPT humanize | AI signal ("AI-generated only") | **III** | `humanize` | `anti-detector` on AI text → **III** |
| Student draft → Grammarly polish | May score low / `*%` band | **IV** | `polish` | `balanced`/`full` on human text → **IV** |
| Student draft → unslop subtle (regex only) | Likely **I** | **I** | N/A | `subtle` |
| AI draft → unslop → cross-model GPT pass | AI signal (Turnitin target) | **III** (stronger evasion) | N/A | anti-detector + user second pass |

**Critical unslop insight:** Binary detector loops (`detector.py` TMR/Desklib) optimize "AI probability" without naming the class. A text can pass TMR at 40% AI but still classify as DetectAIve **III** — policy-relevant for institutions that care about *provenance*, not just score.

---

## 3. Turnitin detection architecture (bypasser layer)

### 3.1 Published stack (evidence tier)

| Component | Role | Evidence |
|-----------|------|----------|
| **AIW-2** | Core LLM-output classifier | Turnitin whitepaper (Sep 2024) |
| **AIR-1** | Paraphrase / word-spinner detection | Whitepaper; Jul 2024 two-color report |
| **Bypasser layer (Aug 2025+)** | Humanizer-output signatures | Press release + release notes **[F]** |
| **Ensemble (inferred)** | Three-model + dedicated bypasser classifier | Secondary industry writeups **[V]** — not vendor-confirmed |

Turnitin's Aug 2025 move is **DAMAGE-class defense** (Agent #12): retrain on adversary outputs, not a new theoretical detector. Same pattern as Originality's ~monthly humanizer-corpus retraining (Agent #58).

### 3.2 Hypothesized bypasser signals (not vendor-confirmed)

| Signal | Rationale | Source tier |
|--------|-----------|-------------|
| **Humanizer rewrite fingerprint** | Training on StealthGPT/Groby-class outputs | Blommerde hit pattern **[I]** |
| **Burstiness injection artifacts** | Humanizers force sentence-length variance | HumanizeMy.ai analysis **[V]** |
| **Lexical AI-ism clusters post-rewrite** | Synonym-swap leaves co-occurrence tells | Cat 04 slop research |
| **Uniform list/bullet structure** | SaaS humanizers flatten syntax | SKILL.md anti-detector rule #2 |
| **Low intra-doc surprisal variance** | Even after rewrite, token distribution persists | DivEye (Agent #01) |
| **Typo/noise injection (L3 humanizers)** | DAMAGE L3 tools add garbage tokens | Agent #12 Table 9 |

Blommerde's results support **signature detection on trained tools** (StealthGPT, Groby hit hard) vs **distribution miss on untrained tools** (Easy Essay 0%). That is not "perfect detection" — it is incomplete adversary coverage.

---

## 4. Vendor claims catalog

### 4.1 Turnitin first-party claims

| Claim | Stated where | Caveats Turnitin admits |
|-------|--------------|-------------------------|
| Detects "leading AI bypasser modifications" | Press release Aug 2025 | No tool list; English only |
| Integrated — no extra setup | Press + release notes | Requires Originality / iThenticate AI license |
| Document FP **<1%** | Model guide | Applies to scores **≥20%** only |
| Catches **~85%** of fully AI-generated text | Internal testing cited in guides | By design misses ~15% to hold FP down |
| 1–19% band shown as `*%` | Oct 2025 formalization | Higher FP incidence acknowledged in this band |
| Score **not sole basis** for adverse action | Model guide disclaimers | Institutional policy varies |
| Feb 2026: improved recall, FP held low | 2026 release notes | Not retroactive; no magnitude published |
| Jul 2026: unified blue — detection unchanged | Product updates | Presentation only |

### 4.2 What Turnitin does **not** publish (the gap)

| Metric | Status |
|--------|--------|
| Bypasser detection rate (recall on humanized text) | **Not published** |
| Bypasser false-positive rate | **Not published** |
| Per-humanizer breakdown | **Not published** |
| Training corpus / consent / provenance | **Not published** |
| Benchmark dataset for bypasser layer | **Not published** |
| Class III vs Class IV disambiguation accuracy | **Not applicable** — no sub-labels |

Bassett (Charles Sturt) publicly demanded API access, versioned technical reports, and independent benchmark replication ([ETIH, Sept 2025](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers)). None delivered as of Aug 2026.

### 4.3 Humanizer vendor counter-claims (pre-Aug 2025, mostly stale)

| Vendor claim | Typical figure | Post-bypasser reality |
|--------------|----------------|----------------------|
| "99.8% undetectable on Turnitin" | Marketing sitewide | StealthGPT: 72% flagged (Blommerde) **[I]** |
| "Bypass Turnitin guaranteed" | Ryter Pro, Walter Writes SEO | Single-academic tests; no conflict-free replication |
| "0% AI on Turnitin" demo screenshots | YouTube/TikTok | Pre-Aug 2025 model; resubmit invalidates |
| Built-in "all green" detector panel | Undetectable.ai, StealthGPT | Omits Turnitin; internal conflict of interest **[I]** |

Humanizer marketing **conflates** bypass rate with AI-score reduction and **predates** the bypasser layer. Any pre-Aug 2025 Turnitin number is stale; post-Aug 2025 numbers are stale after each model refresh (Oct 2025, Feb 2026).

---

## 5. Independent evidence — claims vs reality

### 5.1 Blommerde (Northumbria University) — best public bypasser test

Source: [ETIH Sept 2025](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers); [DetectionDrama synthesis](https://detectiondrama.com/humanizers-that-beat-turnitin-bypasser-detection/)

| Tool | Pre-update | Post-bypasser (Sept 2025) | Interpretation |
|------|------------|---------------------------|----------------|
| **StealthGPT** | 0% | **72%** | Signature-trained; biggest swing |
| **Groby** | 0% | **67%** | Same |
| **GPT Human** | — | **31%** | Partial catch; grey-zone risk |
| **StealthWriter** | — | 1–19% (`*%` band) | Ambiguous suppression |
| **Refrazy** | — | 1–19% (`*%` band) | Same |
| **Easy Essay** | 0% | **0%** | Possible training miss |

Methodology: YouTube test, six tools, small sample, **not peer-reviewed**. Turnitin labels all flags "AI generated" — **no bypasser sub-label** exposed to instructors.

Blommerde conclusion: *"The new AI bypasser detector is an improvement, but it's not perfect… Totally accurate AI detection is a myth."*

### 5.2 Academic benchmarks — what did **not** test Turnitin bypasser

| Study | Turnitin tested? | Relevant finding |
|-------|------------------|------------------|
| **Jabarian & Imas (Booth/NBER 2025)** | **No** | StealthGPT breaks GPTZero; Pangram robust |
| **LLM-DetectAIve (EMNLP 2024)** | **No** | Class III 95.71% in-domain; 60% OOD |
| **DAMAGE (COLING 2025)** | **No** | 19 humanizers break legacy detectors; Pangram-trained DAMAGE holds |
| **Liang et al. (2023)** | **No** | ESL FP bias — equity load-bearing |
| **EFL study (Springer 2026)** | Turnitin accuracy **0.61** vs Originality **0.69** | Hybrid text; poor on mixed provenance |
| **Working Educators (2025–26)** | FP study | 15% overall FP; **31% ESL** vs 12% native |

**Attribution fix:** unslop `skills/unslop/SKILL.md` line "Turnitin drops to 60–85% accuracy on humanized text" at "Chicago Booth 2026" is **wrong**. Booth did not evaluate Turnitin. Remove or cite Blommerde / Cat 18 tier **[I]** instead.

### 5.3 Commercial humanizer tier results (unslop Cat 18)

From [docs/research/18-commercial-humanizer-tools/B-industry.md](../../docs/research/18-commercial-humanizer-tools/B-industry.md):

| Tool | Pre-Aug 2025 Turnitin bypass | Post-Aug 2025 |
|------|------------------------------|---------------|
| StealthGPT | ~79.7% bypass **[I]** | ~62%; Blommerde 72% flagged |
| QuillBot Humanizer | Weak already | ~47% avg; Turnitin targets synonym-swap |
| Undetectable.ai | Market leader claims | **No conflict-free Turnitin bypasser test** |
| Easy Essay | N/A | 0% Blommerde — single test, small n |

### 5.4 Claims vs reality summary matrix

| Stakeholder | Claim | Reality check (Aug 2026) | Tier |
|-------------|-------|--------------------------|------|
| Turnitin | Catches leading bypassers | Partial; tool-dependent; no public recall | **[F]** vs **[I]** |
| Turnitin | FP <1% | Document-level ≥20% only; ESL worse in independent tests | **[F]** vs **[I]** |
| StealthGPT | Turnitin-proof | 72% flagged post-update | **[I]** |
| Undetectable.ai | 99%+ undetectable | No bypasser-layer Turnitin test; Pangram catches 90.3% | **[V]** vs **[A]** |
| Humanizer blogs | "Bypass still works 2026" | Affiliate content; Easy Essay n=1 public pass | **[V]** |
| DetectAIve authors | 95.71% on Class III | In-domain LLM-on-LLM only; 60% OOD | **[A]** |
| Blommerde | Detection is whack-a-mole | Consistent with Sadasivan TV bound (Agent #17) | **[I]** |

---

## 6. UI evolution and instructor-facing category collapse

Understanding what instructors **see** vs what the model **detects**:

```
Jul 2024 ────────────────── Aug 2025 ────────────────── Jul 2026
  │                            │                            │
  ├─ Blue: raw LLM             ├─ Blue: raw + BYPASSER      ├─ Blue: ALL AI signal
  ├─ Purple: paraphrased       ├─ Purple: paraphrased       └─ (purple removed)
  └─ Two interactive cats      └─ Bypasser invisible in UI
```

**Jul 2026 unified blue** ([product updates](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates)): vendor rationale — instructors over-read purple-vs-blue as proof of workflow. Detection logic unchanged; **presentation de-escalates certainty** while **models escalate aggression** (bypasser training + Feb 2026 recall bump).

Policy implication: an instructor can no longer distinguish Class II vs III vs paraphrase from the report UI. They get a single "likely AI" signal — closer to binary detection, further from DetectAIve's policy-aware granularity.

---

## 7. Arms-race dynamics

### 7.1 Retrain cadence

| Date | Event | Humanizer impact |
|------|-------|------------------|
| Aug 27, 2025 | Bypasser layer launch | StealthGPT-class bypass rates collapse |
| Oct 14, 2025 | Model refresh + `*%` formalization | Non-native speaker tuning claimed |
| Feb 12, 2026 | Recall bump, FP held | Second post-bypasser refresh; resubmit required |
| May 2026 | Spanish LLM refresh | Bypasser still English-only |
| Jul 20, 2026 | Unified UI | No detection change |

Vendor pattern: **several English model updates per year**, each shifting the boundary without announcing training data changes. Humanizer vendors claim 35–40% detection increase post-Aug 2025 ([HumanLike blog](https://humanlike.pro/blog/turnitin-august-2025-bypass-detector-update) — **[V]** tier).

### 7.2 Evasion techniques vs bypasser layer

| Technique | vs pre-Aug 2025 Turnitin | vs bypasser layer | DetectAIve Class III |
|-----------|--------------------------|-------------------|----------------------|
| Same-model LLM humanize prompt | Often 0% | **Caught** (StealthGPT) | In-domain trained |
| Cross-model second pass | Unknown | **Likely stronger** — not in training | **Not in training** |
| TempParaphraser (no LLM) | Partial bypass | Unknown | Not tested |
| Light polish on human draft | Low signal | Low signal | **IV** — policy gray zone |
| Manual edit after humanizer | Unknown | Unknown | Proposed Class V (future) |
| unslop `subtle` (regex only) | N/A | Stays Class I/II | No LLM pass |

Cross-model paraphrase (Agent #35) is the evasion path **least represented** in both Turnitin training (inferred) and DetectAIve Class III corpus — and the path unslop's anti-detector procedure recommends as step 6.

### 7.3 Sadasivan impossibility bound (Agent #17)

If humanizer reduces total variation distance between human and machine text below detector resolution, **no stable classifier exists**. Turnitin's bypasser layer raises the bar for **signature-matched** humanizers but does not resolve the impossibility result — it shifts the equilibrium, monthly.

---

## 8. Institutional and academic response to the category

| Actor | Position | Source |
|-------|----------|--------|
| **Turnitin CPO** | Humanizers = "cheating providers"; bypasser detection = integrity duty | Press release **[F]** |
| **Bassett (Charles Sturt)** | Welcome transparency; demand public benchmarks + API | ETIH **[P]** |
| **Blommerde (Northumbria)** | Skeptical of raw/paraphrase/humanize trichotomy; binary label loses nuance | ETIH **[I]** |
| **Curtin University** | **Disabled AI detection Jan 1, 2026**; originality check remains | Institutional **[F]** |
| **Turnitin docs** | Score ≠ proof; human judgment essential | Model guide **[F]** |

The bypasser category **did not** reverse institutional skepticism. Curtin exit postdates the Aug 2025 launch — suggesting institutions weigh FP/equity over incremental bypasser recall.

---

## 9. unslop honest positioning

### 9.1 What bypasser detection changes for unslop

| unslop claim | Still valid? | Notes |
|--------------|--------------|-------|
| Subtract AI-isms, add burstiness/contractions | **Yes** | TV-reduction; reduces II→III detectability |
| Anti-detector for ESL false positives | **Yes** | Liang + Working Educators support **IV/I** defense, not III evasion |
| "Beat Turnitin" / stable bypass | **No** | Bypasser layer + Feb 2026 retrain = month-scale decay |
| Optimize one detector score | **Weak** | `--detector-feedback` binary; no Class III/IV distinction |
| Booth proves Turnitin 60–85% drop | **No — fix copy** | Booth didn't test Turnitin |

### 9.2 DetectAIve-aware anti-detector framing

When unslop runs `anti-detector` on **AI-origin** text, the output target is **Class III** (M→MH). Institutions adopting DetectAIve-style policy (or Turnitin's bypasser layer) care about this distinction.

When unslop runs on **human-origin** text (ESL false-positive defense), the target is stay **Class I** or at most **Class IV** — not drift into III.

Recommended SKILL.md addition (conceptual):

> Turnitin's bypasser category = DetectAIve Class III. Anti-detector on AI text is obfuscation-class output. For ESL defense on human drafts, prefer `voice-match` + `subtle` over heavy LLM rewrite.

### 9.3 Recommended messaging (August 2026)

> Turnitin retrained in August 2025 on humanizer outputs — the "bypasser" category — then again in February 2026. They publish no bypasser accuracy numbers. The report shows one blue highlight, not a tool-specific verdict. The score still isn't proof.
>
> unslop removes statistical signatures that make LLM text detectably non-human: stock phrases, uniform rhythm, zero contractions. That's voice work — the same edits that reduce false positives for ESL writers. It is not a Turnitin guarantee.
>
> Anti-detector mode exists for **false-positive defense** and **register restoration**. Maximum separation from detector fingerprints: **cross-model second pass** after unslop.

### 9.4 Code / doc actions

1. **SKILL.md:** Remove Booth attribution for Turnitin 60–85%. Add DetectAIve Class III mapping sentence.
2. **P1 `detector.py`:** Optional DetectAIve DeBERTa backend; log Class III vs IV softmax (Agent #10 §9).
3. **Bench protocol:** Map fixtures to 4-class labels; note Turnitin model version date on any Turnitin row.
4. **README:** Name bypasser category explicitly; link Curtin disable as institutional counter-signal.

---

## 10. Open questions

1. **Which humanizers are in Turnitin's bypasser training set?** Vendor silent. Blommerde hit/miss split suggests incomplete coverage (Easy Essay 0%).
2. **Does Turnitin distinguish Class III from Class II internally?** UI says no; inference pipeline unknown.
3. **Feb 2026 recall bump magnitude on bypasser specifically?** No public A/B.
4. **DetectAIve Class III recall on unslop anti-detector outputs?** Not benchmarked; P0 for May 2026 bench.
5. **Cross-model paraphrase vs bypasser layer?** Best hypothesized evasion path; zero public Turnitin tests.
6. **IV false-positive rate on ESL human polished text?** DetectAIve confusion III↔IV + Liang ESL bias = compounded equity risk.
7. **Authorship / Clarity pivot:** Turnitin investing in process provenance while collapsing classifier UI certainty — long-term bypasser category may matter less than draft history.

---

## 11. URL index

### Turnitin official

- [Press: AI bypasser detection (Aug 27, 2025)](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers)
- [AI writing detection model + release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model)
- [Turnitin release notes](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes)
- [Product updates (Jul 2026 unified UI)](https://guides.turnitin.com/hc/en-us/articles/29645383597965-Turnitin-product-updates)
- [Blog: Simplifying AI detection](https://www.turnitin.com/blog/how-turnitin-is-simplifying-ai-detection-for-educators-and-publishers)
- [AIW-2 / AIR-1 whitepaper](https://www.scribd.com/document/988214788/TII-AI-HE-AIWritingDetectionModel-Whitepaper-US-0924-1)

### LLM-DetectAIve / academic taxonomy

- [arXiv 2408.04284](https://arxiv.org/abs/2408.04284)
- [ACL Anthology EMNLP 2024 Demo](https://aclanthology.org/2024.emnlp-demo.35/)
- [HF model: DeBERTa 4-class](https://huggingface.co/raj-tomar001/LLM-DetectAIve_deberta-base)
- [MixSet (OOD eval)](https://arxiv.org/abs/2401.05952)
- [DAMAGE humanizer audit](https://arxiv.org/abs/2501.03437)
- [Jabarian & Imas BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)

### Independent tests

- [Blommerde / ETIH coverage](https://www.edtechinnovationhub.com/news/turnitins-new-ai-bypasser-detection-draws-scrutiny-from-academics-and-early-testers)
- [DetectionDrama — humanizer test table](https://detectiondrama.com/humanizers-that-beat-turnitin-bypasser-detection/)
- [DetectionDrama — Undetectable.ai evidence gap](https://detectiondrama.com/does-undetectable-ai-bypass-turnitin/)
- [Working Educators FP test](https://workingeducators.org/turnitin)
- [EFL detector study 2026](https://link.springer.com/article/10.1007/s40979-026-00213-1)

### Institutional

- [Curtin — disable AI detection (Jan 2026)](https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/)

### unslop internal

- [Agent #56 — Turnitin timeline](./AGENT-56-TURNITIN-2025-2026.md)
- [Agent #10 — LLM-DetectAIve](./AGENT-10-LLM-DETECTAIVE.md)
- [Agent #12 — DAMAGE](./AGENT-12-DAMAGE-DETECTOR.md)
- [Agent #58 — Originality Turbo 3.0.2](./AGENT-58-ORIGINALITY-AI-ALLOWANCE.md)
- [Cat 18 — commercial humanizer benchmarks](../../docs/research/18-commercial-humanizer-tools/B-industry.md)

---

## 12. Evidence tier key

| Tier | Meaning |
|------|---------|
| **[F]** | Turnitin first-party (press, guides, release notes) |
| **[A]** | Peer-reviewed / EMNLP / working paper |
| **[I]** | Independent test with named methodology |
| **[V]** | Vendor or vendor-adjacent |
| **[P]** | Press / aggregator |

---

*Agent #66 complete. Primary contribution vs Agent #56: bypasser-as-category taxonomy, DetectAIve Class III mapping, claims-vs-reality matrix, unslop III/IV policy distinction.*
