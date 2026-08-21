# Agent #40 — Commercial Humanizer DAMAGE Tier Results

**Topic:** DAMAGE Table 9 L1/L2/L3 tiers, 2025–2026 independent verification, vendor responses, unslop vs L1 humanizers  
**Primary paper:** Masrour, Emi & Spero, *DAMAGE: Detecting Adversarially Modified AI Generated Text*, COLING 2025  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

DAMAGE ([arXiv:2501.03437](https://arxiv.org/abs/2501.03437)) is still the only peer-reviewed audit that **names 19 humanizers**, **segments them by output quality** (Table 9), and **measures detector collapse** on humanized academic text (Table 3). The tier labels (L1/L2/L3) rank **fluency and faithfulness**, not bypass success. The paper says so explicitly.

Post-DAMAGE, the landscape shifted in three ways that matter for unslop:

1. **Adapted detectors win.** Pangram's August 2025 humanizer table catches 90.3–100% of named tools. Jabarian & Imas (Chicago Booth, Sept 2025) find Pangram stays robust when text passes through StealthGPT (an L1 tool); GPTZero's false-negative rate jumps to ~50%+.
2. **Turnitin entered the arms race.** AI bypasser detection shipped **27 August 2025** ([press release](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers)). Pre-August bypass numbers are stale.
3. **Vendor marketing diverged from measurement.** Epaphras & Mtenzi (2026) find WriteHuman at 1.98% ADR on weak detectors (ZeroGPT/Scribbr); HumanizerBench (Aug 2026, WriteHuman-operated) ranks WriteHuman #1 at 89.1% bypass on five commercial detectors. Pangram still catches Undetectable AI ~90% of the time. Same tool class, incompatible headlines.

**unslop positioning vs L1 humanizers:** L1 SaaS tools (StealthGPT, Quillbot, Grammarly, HumanizeAI.pro, etc.) are **cloud paste-box rewriters** optimized for detector evasion. unslop is an **in-editor polish layer** that subtracts AI-isms, preserves code/URLs byte-exact, and documents that deterministic rewriting moves TMR scores ~0.0–0.2 pp. The honest comparison isn't "unslop vs Undetectable.ai." It's "unslop vs a cross-model second pass + manual edit" — which independent work consistently beats single-pass SaaS humanizers.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **DAMAGE paper (arXiv)** | https://arxiv.org/abs/2501.03437 |
| **DAMAGE paper (HTML)** | https://arxiv.org/html/2501.03437 |
| **Pangram humanizer update (Aug 2025)** | https://www.pangram.com/blog/humanizers-aug-25 |
| **Pangram technical report (Jan 2025)** | https://arxiv.org/abs/2402.14873 |
| **Jabarian & Imas — working paper PDF** | https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf |
| **Jabarian & Imas — NBER DOI** | https://doi.org/10.3386/w34223 |
| **Chicago Booth Review summary** | https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust |
| **Turnitin bypasser press (27 Aug 2025)** | https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers |
| **Turnitin AI writing model docs** | https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model |
| **Turnitin release notes** | https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes |
| **Epaphras & Mtenzi (2026) — DOI** | https://doi.org/10.37284/ijar.9.1.4683 |
| **Epaphras & Mtenzi — AKU eCommons PDF** | https://ecommons.aku.edu/cgi/viewcontent.cgi?article=1258&context=eastafrica_ied |
| **HumanizerBench (Aug 2026 cycle)** | https://humanizerbench.com/ |
| **Poignant Guide 2025 bypass survey** | https://poignantguide.net/research/ |
| **Adversarial Paraphrasing (NeurIPS 2025)** | https://arxiv.org/abs/2506.07001 |
| **DIPPER / Krishna et al. (NeurIPS 2023)** | https://arxiv.org/abs/2303.13408 |

---

## DAMAGE Table 9 — full tier inventory

Table 9 lives in Appendix E of DAMAGE. Tiers reflect **qualitative fluency audit** + GPT-4o Fluency Win Rate (25 samples per tool). **Not** bypass rate.

### Tier definitions (§4.5–4.6)

| Tier | Quality profile | Avg Fluency Win Rate* |
|------|-----------------|----------------------|
| **L1** | Preserves tone, vocabulary level, complexity; subtle rewrites | 26.0% |
| **L2** | Degraded quality; intent preserved; occasional word misuse | 14.67% |
| **L3** | Nonsense phrases, citations hallucinated, meaning distorted | 2.67% |

*Win rate = fraction of times GPT-4o preferred humanized text over original. Lower = humanizer degraded quality more.

### Table 9 — per-tool assignments

| Name | Tier | DAMAGE qualitative note |
|------|------|-------------------------|
| **DIPPER** | L1 | Sparing changes; sentences often unchanged; occasional grammar issues |
| **GPTInf** | L1 | High quality; few spelling/punctuation/vocabulary issues |
| **Grammarly** | L1 | High quality; varied punctuation; occasional odd edits |
| **HumanizeAI.pro** | L1 | Good grammar, advanced vocabulary, punctuation |
| **Quillbot** | L1 | Flowery but fluent; high vocabulary, slightly imprecise |
| **Semihuman AI** | L1 | Good quality; sometimes adds personal pronouns |
| **StealthGPT** | L1 | Output closely matches original style |
| **Twixify** | L1 | Good overall; occasional dictionary-lookup word misuse |
| **AIHumanizer.com** | L2 | Downgrades university → middle-school level |
| **BypassGPT** | L2 | Dictionary lookup per sentence; words used out of context |
| **StealthWriter.AI** | L2 | Grammar/punctuation/capitalization issues ~1/paragraph |
| **Surfer SEO** | L2 | Middle-school-level output |
| **Ghost AI** | L3 | Splits every sentence into single-clause statements |
| **HIX Bypass** | L3 | Mostly OK; dense pockets of nonsense |
| **HumanizeAI.io** | L3 | Fictional citations, `??????`, punctuation errors |
| **Humbot AI** | L3 | Uninterpretable sentences; random additions |
| **Phrasly** | L3 | Poor sentences; high variance across texts |
| **Undetectable AI** | L3 | Elementary-school level; introduces typos |
| **WriteHuman.ai** | L3 | Elementary-school level; incomplete sentences |

**Table 1 tool count:** 3 paraphrasers (DIPPER, Grammarly, Quillbot) + 16 humanizers = 19 tools audited.

### Critical interpretive note

DAMAGE trained its robust detector on **L1 humanizer outputs only** (§5.4) because L1 rewrites are the hardest adversarial case that still reads fluently. L3 tools degrade text so badly that Pangram later **chooses not to optimize for them** — garbled output is visible to humans but hard to classify without raising false positives on ESL writers ([Pangram blog](https://www.pangram.com/blog/humanizers-aug-25)).

**Fluency tier ≠ evasion tier.** StealthGPT is L1 (quality) but only the **15th-best evader** in Pangram's August 2025 table (95.6% detected). Undetectable AI is L3 (quality) but the **best evader** in that same table (90.3% detected — still not a bypass).

---

## DAMAGE detector-collapse results (Table 3)

Academic essay benchmark, TPR @ FPR=5%, bootstrap 1000 iterations:

| Detector | Raw AI text | Humanized AI text | Δ (pp) |
|----------|-------------|-------------------|--------|
| GPTZero | 99.73% ± 0.19 | 60.04% ± 1.80 | **−39.7** |
| Binoculars | 94.15% ± 0.88 | 28.23% ± 1.62 | **−65.9** |
| RADAR | 3.33% ± 0.65 | 5.05% ± 0.81 | +1.7 |
| LLM baseline (no humanizer training) | 100.00% | 95.74% ± 0.71 | −4.3 |
| **DAMAGE detector** | 100.00% | **98.26% ± 0.47** | **−1.7** |

At default thresholds (Table 7): GPTZero humanized TPR collapses to **34.53%**; DAMAGE holds **97.47%**.

**Marketing gap:** Vendors routinely claim "99.8% undetectable." DAMAGE shows **20–100 pp** divergence between self-reported and independently measured bypass on legacy detectors — and even legacy GPTZero still catches ~60% of humanized academic text.

---

## Pangram August 2025 — per-tool detection accuracy

Pangram (DAMAGE authors' commercial detector) published an expanded 20-tool table. Metric is **detection accuracy** (% of humanizer outputs caught), not fluency tier.

| Humanizer | Pangram detection % | DAMAGE tier | Notes |
|-----------|----------------------|-------------|-------|
| Grammarly, Quillbot, Semihuman AI, humanizeai.pro, Smodin, Surfer SEO, Ghost AI, Ahrefs, aihumanizer.com | 100.0% | Mixed L1–L3 | Zero evasion in this test |
| Bypass GPT | 99.7% | L2 | |
| Scribbr | 99.0% | — | Not in DAMAGE Table 9 |
| Writesonic AI | 98.1% | — | Not in DAMAGE Table 9 |
| DIPPER | 97.6% | L1 | Research paraphraser baseline |
| GPTinf | 99.2% | L1 | |
| StealthGPT | 95.6% | **L1** | Quality ≠ evasion |
| humanizeai.io | 93.8% | L3 | |
| Just Done | 93.5% | — | |
| TwainGPT | 92.7% | — | |
| **Undetectable AI** | **90.3%** | **L3** | Best evader; still ~9/10 caught |

Pangram's stated design tradeoff: internal models exist with near-perfect humanizer recall but higher FPR on human/ESL text. They ship the conservative model.

Cross-detector comparison on humanized text (Pangram blog, citing Russell et al.): Pangram ~97% vs GPTZero ~46%, FastDetectGPT ~23%, Binoculars ~7%.

---

## Independent verification 2025–2026

### 1. DAMAGE / Pangram (Jan–Aug 2025)

- **What:** 19-tool qualitative audit + detector robustness via humanizer-augmented training (~0.68% of training set, 18× oversampled).
- **Humanizer for adversarial fine-tune test:** GPT-4o fine-tuned on L1 false negatives; DAMAGE still detects 93.2% at default threshold (Table 5).
- **Watermark:** DIPPER drops SynthID TPR @ FPR=1% from 66.5% → 1.5% (Table 2).
- **URLs:** [2501.03437](https://arxiv.org/abs/2501.03437), [humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25)

### 2. Jabarian & Imas — Chicago Booth / NBER (September 2025)

- **What:** 1,992-passage corpus, 6 genres, 4 frontier LLMs (GPT-4.1, Claude Opus 4, Claude Sonnet 4, Gemini 2.0 Flash). Four detectors tested.
- **Humanizer tested:** **StealthGPT only** (DAMAGE L1).
- **Key finding:** Pangram FNR stays low on humanized text; GPTZero FNR ~50%+ across genres; Originality.ai FNR 5–21% depending on length/genre.
- **Policy framework:** Institutions set FPR cap (e.g. ≤0.5%); compare detectors under that cap.
- **URLs:** [BFI PDF](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf), [NBER w34223](https://doi.org/10.3386/w34223), [Booth Review](https://www.chicagobooth.edu/review/do-ai-detectors-work-well-enough-trust)

**Attribution correction for unslop docs:** README cites "Chicago Booth 2026 audit of twelve humanizer services" with "~6 points median accuracy drop." The Booth paper **does not audit twelve humanizers** — it uses one (StealthGPT). The **12-humanizer monthly benchmark** is [HumanizerBench](https://humanizerbench.com/) (August 2026 cycle), operated by WriteHuman. The "~6 points" figure does not appear in Jabarian & Imas; treat as **unverified / likely conflated** until a primary source is found.

### 3. Turnitin AI bypasser detection (27 August 2025 → 2026)

- **Launch:** Bypasser detection integrated into AI writing report; "AI-generated only" category now includes text modified by bypasser tools.
- **Scope:** English only (Spanish/Japanese have separate models without bypasser layer per release notes).
- **July 2026 UI change:** Two-color report (blue AI / purple AI-paraphrased) unified; detection capability retained including bypasser-modified text.
- **Vendor claim:** Trained/tested on "leading" bypassers; CPO Annie Chechitelli names humanizer companies as "cheating providers."
- **URLs:** [Press release](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers), [Model docs](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model), [Release notes](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes)

**SKILL.md note:** "Retrained February 2026" — no dedicated February 2026 bypasser-model release appears in Turnitin release notes as of this memo. Closest 2026 AI-model update: Spanish model (May 2026). Flag for verification.

### 4. Epaphras & Mtenzi (2026)

- **What:** Three humanizers × ChatGPT/Gemini outputs × 3 detectors (QuillBot AI detector, ZeroGPT, Scribbr), multi-iteration design.
- **Results (ADR = average detection rate — lower = better evasion):**

| Tool | ADR | DAMAGE tier |
|------|-----|-------------|
| WriteHuman | **1.98%** | L3 |
| Writesonic | 64.39% | — |
| QuillBot | **93.56%** | L1 |

- **Limitation:** Consumer-grade detectors only; no Turnitin, Pangram, or Originality.ai. WriteHuman's strong score **conflicts with L3 fluency rating** — suggests detector panel weakness, not proof of durable bypass.
- **URL:** [DOI 10.37284/ijar.9.1.4683](https://doi.org/10.37284/ijar.9.1.4683)

### 5. HumanizerBench (August 2026 cycle)

- **What:** 12 humanizers, 33 samples each, 5 detectors (GPTZero, ZeroGPT, Copyleaks, Winston AI, Originality.ai). Methodology v1.2.0.
- **Conflict:** Operated by WriteHuman; WriteHuman ranks #1.
- **Selected results:**

| Rank | Humanizer | Bypass rate | DAMAGE tier |
|------|-----------|-------------|-------------|
| 1 | WriteHuman | 89.1% | L3 |
| 2 | HumanizeAI.pro | 83.5% | L1 |
| 4 | HIX Bypass | 75.2% | L3 |
| 8 | Undetectable.ai | 86.0% bypass / heavy penalties | L3 |
| 11 | Grammarly | **0.0%** | L1 |
| 12 | StealthGPT | **27.5%** | L1 |

- **Takeaway:** L1 tools split wildly on bypass (0–83.5%). Grammarly detected 100% of the time; HumanizeAI.pro leads. StealthGPT — DAMAGE L1, Jabarian test subject — finishes last on this panel.
- **URL:** [humanizerbench.com](https://humanizerbench.com/)

### 6. Poignant Guide 2025 Annual Survey

- **What:** 14 humanizers × 6 detectors × 4,200 samples. Independent, published data.
- **Finding:** 21–33 pp accuracy drop on humanized text; perplexity-based detectors (GPTZero, Sapling) most vulnerable; no detector robust to all humanizers.
- **URL:** [poignantguide.net/research](https://poignantguide.net/research/)

### 7. Adversarial Paraphrasing (NeurIPS 2025) — structural context

- Optimized paraphrase drops tested detector TPR by ~87% on average.
- Supports unslop README finding: surface synonym rewriting (deterministic unslop) moves TMR ~0.0–0.2 pp; structural/adversarial paraphrase is a different class.
- **URL:** [2506.07001](https://arxiv.org/abs/2506.07001)

---

## Vendor responses (2025–2026)

No humanizer vendor published a formal rebuttal to DAMAGE Table 9 tier assignments. Response pattern is **counter-benchmark marketing**, not engagement with the paper.

| Actor | Response type | Claim | Primary URL |
|-------|---------------|-------|-------------|
| **Pangram / DAMAGE authors** | Research follow-up | >90% detection on all tested humanizers; fluent L1 output *more* detectable | [humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25) |
| **Turnitin** | Product counter-move | Bypasser detection shipped; names humanizer industry as integrity threat | [Press 2025-08-27](https://www.turnitin.com/press/turnitin-expands-capabilities-amid-rising-threats-posed-by-ai-bypassers) |
| **StealthGPT** | Counter-benchmark blog | "Only perfect score" in independent 25-tool Medium test vs Originality/Winston/GPTZero/ZeroGPT | [stealthgpt.ai/blog](https://www.stealthgpt.ai/blog/ai-humanizer-test-stealthgpt-perfect-score) |
| **WriteHuman** | Self-operated benchmark | #1 on HumanizerBench Aug 2026; 89.1% bypass | [writehuman.ai/blog](https://writehuman.ai/blog/ai-humanizer-rankings-august-2026) |
| **Undetectable.ai** | SEO content | 85–95% bypass vs Turnitin; 12–14% detection on "professional" rewrites | [undetectable.ai/blog](https://undetectable.ai/blog/undetectable-ai-vs-turnitin) |
| **Originality.ai** | Competitive review | StealthGPT flagged 100% AI in controlled test | [originality.ai/blog/stealthgpt](https://originality.ai/blog/stealthgpt-ai-review) |

**Silence:** Undetectable.ai, WriteHuman, HIX Bypass, Phrasly — none address their **L3 fluency classification** in DAMAGE. Marketing instead emphasizes detector scores on panels that exclude Pangram and Turnitin.

**Detector-side arms-race quote:** Pangram CTO Bradley Emi (DAMAGE co-author) — internal high-recall models exist but aren't shipped to protect ESL/human FPR ([Aug 2025 blog](https://www.pangram.com/blog/humanizers-aug-25)).

---

## L1 humanizers — what they actually do

From DAMAGE §3–4 and Pangram follow-up:

| Mechanism | Examples | Detector interaction |
|-----------|----------|---------------------|
| Fine-tuned LLM paraphrase | StealthGPT, HumanizeAI.pro, Semihuman AI | Preserves fluency → **more detectable** by adapted classifiers |
| Synonym / dictionary replacement | Quillbot, BypassGPT, Twixify | "Tortured phrases"; 100% caught by Pangram on L1 paraphrasers |
| Error injection (spacing, Unicode) | L3 tools, some HIX/Humbot modes | Evades tokenizers briefly; gibberish visible to humans; Pangram descopes |
| Jailbreakable system prompts | Several LLM humanizers | DAMAGE Appendix A — prompts exposed via jailbreak |

L1 tools share DNA with unslop's **LLM mode** (rewrite to sound human) but differ on:

- **Goal:** L1 SaaS optimizes detector scores; unslop optimizes voice/subtraction.
- **Preservation:** unslop `_protect()` contract; SaaS often breaks code, URLs, citations.
- **Auditability:** unslop emits per-rule `HumanizeReport`; SaaS is black-box.
- **Honesty:** unslop documents detector limits; SaaS claims "100% undetectable."

---

## unslop positioning vs L1 humanizers

### What unslop is not

- Not a paste-box bypass service.
- Not competing on "beat Turnitin" marketing.
- Not claiming durable detector evasion (`SKILL.md` Boundaries, README FAQ).

### What unslop is

| Dimension | L1 commercial humanizer | unslop |
|-----------|------------------------|--------|
| **Deployment** | Web SaaS, copy-paste | IDE/agent plugin, inline |
| **Core move** | Paraphrase / synonym swap / error injection | Subtract AI-isms; optional structural + soul passes |
| **Detector claim** | "99.8% undetectable" | Deterministic pass: ~0.0–0.2 pp on TMR; LLM judge 21/21 human-read wins |
| **Code/URL safety** | Often breaks | Validated preservation suite |
| **Strongest evasion lever** | Black-box rewrite | **Cross-model second pass** (user-orchestrated; TempParaphraser ~82.5% detector reduction) |
| **Anti-detector mode** | Entire product | Explicit opt-in; ESL false-positive defense framing |
| **Cost** | $10–30/mo | Free / MIT |

### Strategic narrative (defensible)

1. **Quality tier inversion:** DAMAGE L3 tools (Undetectable, WriteHuman) sometimes score *better* on weak detectors than L1 tools (Grammarly 0% bypass on HumanizerBench). Fluency and evasion decouple once detectors adapt.

2. **Adapted detector wins:** Any humanizer recommendation keyed to pre-August-2025 GPTZero scores is stale. Turnitin bypasser layer + Pangram humanizer training shift the boundary.

3. **unslop's wedge isn't bypass — it's honest polish:** Strip sycophancy, cap em-dashes, restore burstiness, preserve technical content. For users who need detector relief (ESL false positives), anti-detector mode + cross-model pass is the documented path — same lever that beats L1 SaaS in independent work, without "$30/mo undetectable" lies.

4. **`detector.py` alignment:** Live TMR feedback loop implements DAMAGE's core lesson — don't trust humanizer self-reports; measure. But Nicks et al. (ICLR 2024) warning stands: detector score is a signal, not a gate.

### Recommended doc fixes (repo hygiene)

| Location | Issue | Fix |
|----------|-------|-----|
| `README.md` L610 | "Chicago Booth 2026 audit of twelve humanizer services" | Split: Booth = Jabarian & Imas (1 humanizer, 4 detectors); HumanizerBench = 12 humanizers (WriteHuman-operated) |
| `README.md` L610 | "median ~6 points accuracy drop" | Cite primary source or remove; Booth paper shows GPTZero FNR → ~50%+, not 6 pp |
| `skills/unslop/SKILL.md` L88 | "Retrained February 2026" | Verify against Turnitin release notes; cite specific release if confirmed |

---

## 2026 synthesis table — where truth lives

| Evidence type | Trust level | Best for |
|---------------|-------------|----------|
| DAMAGE Table 9 tiers | High (peer-reviewed) | Fluency/faithfulness ranking |
| DAMAGE Table 3 | High | Legacy detector collapse vs augmented detector |
| Pangram Aug 2025 table | Medium-high (vendor, reproducible methodology) | Per-tool detection on adapted classifier |
| Jabarian & Imas 2025 | High (academic, no vendor stake) | StealthGPT vs 4 detectors; policy framework |
| Turnitin Aug 2025+ | High (product ground truth for education) | Institutional bypasser detection |
| Epaphras & Mtenzi 2026 | Medium (weak detector panel) | Relative ranking WriteHuman vs QuillBot |
| HumanizerBench 2026 | Low-medium (operator conflict) | Trend signal only; verify raw GitHub data |
| Vendor blogs (StealthGPT, Undetectable) | Low | Marketing; contradict peer-reviewed results |

---

## Implications for unslop anti-detector mode

1. **Do not cite L1 tier as "better humanizer."** StealthGPT is L1 and gets caught 95.6% (Pangram) or ranks #12/12 (HumanizerBench).

2. **Do cite fluency–detection paradox** when users ask about commercial tools: the humanizers that read best are often the easiest for adapted detectors to fingerprint.

3. **Keep recommending cross-model second pass** over SaaS subscription — strongest independent lever; unslop handles items 2–5 (burstiness, contractions, structure break).

4. **ESL defense remains the legitimate wedge** (Liang et al. 2023) — not "beat Turnitin for AI-generated essays."

5. **Refresh landscape paragraph quarterly** — HumanizerBench monthly cycles, Turnitin release notes, Pangram model versions (Pangram 3.3 May 2026, Pangram 4 Aug 2026 per their blog index).

---

## Open questions / next research

- [ ] Measure unslop output (deterministic + LLM + structural + soul) against Pangram API on L1-style fixtures — no in-repo data yet.
- [ ] Reconcile WriteHuman: L3 in DAMAGE, 1.98% ADR in Epaphras, 89.1% bypass in HumanizerBench — panel sensitivity analysis.
- [ ] Track Turnitin bypasser model version strings when exported in AI writing CSV (Nov 2025 export feature).
- [ ] Primary source for README "~6 points median drop" claim — may need retraction.

---

*Agent #40 complete. Cross-refs: Agent #9 (PHD/Tulchinskii), Agent #17 (Sadasivan), UPDATE-PLAN-2026-08.md § commercial humanizers.*
