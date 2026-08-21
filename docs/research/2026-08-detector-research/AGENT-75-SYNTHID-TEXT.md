# Agent #75 — SynthID-Text Production Watermark

**Topic:** Google DeepMind SynthID-Text — tournament-sampling generative watermark, Gemini deployment, detection stack, attack surface, EU AI Act Art. 50 status  
**Prepared:** August 19, 2026  
**Scope:** Nature 2024 paper + supplementary text, DeepMind/HF open-source stack, SRI Lab red-team (2024–2025), WaterPark/DAMAGE/SynGuard benchmarks, Gemini API vs consumer split, sibling agents #20/#71/#74/#72  
**Status:** complete

---

## Executive summary

**SynthID-Text** (Dathathri et al., *Nature* 634:818–823, Oct 2024) is the first **production-scale** generative text watermark. Google DeepMind embeds imperceptible statistical marks at sampling time via **Tournament sampling** — a multi-layer knockout tournament over candidate tokens scored by pseudorandom **g-functions** — layered on a **LeftHash** sliding-window seed generator (H=4) and **repeated context masking** (caching). Non-distortionary configuration preserves text quality; a live A/B study over **~20 million Gemini chatbot responses** showed negligible user-perceived quality loss before full production rollout.

**Deployment split (Aug 2026):** SynthID-Text watermarks **Gemini App and Web** (consumer). It does **not** watermark text from the **Gemini API** — Google staff confirmed on the AI Developers Forum (2026): no machine-readable provenance signal in API responses; native API text watermarking "not planned at the moment." Images, audio, and video from Gemini carry SynthID; text detection via the public SynthID Detector portal is **not** offered for text (image/video/audio only). Developers can self-deploy SynthID via Hugging Face Transformers v4.46.0+ or the reference repo.

**Detection:** Key-only, no LLM access required. **Weighted mean g-value** detector (no training) or **Bayesian detector** (trained per watermark config; three-state output: watermarked / not watermarked / uncertain). Google has described fully-private, semi-private (API), and public detector release tiers; production Gemini uses the Bayesian path per open-source docs.

**Robustness arc:** SynthID beats Gumbel and Soft Red List baselines on clean detectability and resists **spoofing** better than KGW (SRI Lab: 4% spoof success at FPR 10⁻³ vs 80%+ on LeftHash h=3). It is **more scrubbable** than KGW under paraphrase — SRI Lab reports **>90% scrubbing success** without watermark stealing, **~100%** with stealing-assisted scrubbing (FNR*@10⁻³). Unified benchmarks align: WaterPark DP-40 cuts TPR from 0.998 → **0.498**; DAMAGE DIPPER on Gemma-2B-IT drops TPR from 66.5% → **1.5%** @ FPR 1%; ChatGPT one-round paraphrase drops all WaterPark watermarkers below **30% TPR**. SynGuard (Aug 2025) hybrid semantic+token marking improves avg F1 by **11.1%** — partial patch, not a paraphrase cure.

**Regulatory (Aug 2026):** EU AI Act **Article 50(2)** requires machine-readable marking of AI-generated text (effective **2 Aug 2026**; **2 Dec 2026** grace for systems already on market). Commission Guidelines (C(2026) 5054, point 74) allow deployers to rely on the **provider's marking** when available — but Gemini **API** users in the EU cannot rely on Google for text marks. Consumer Gemini text is marked; API text is not. Deliberate watermark removal remains prohibited under the Dec 2025 Code of Practice.

**Unslop verdict:** SynthID is **upstream provenance metadata**, not a post-hoc AI detector. unslop's semantic-preserving rewrites scrub tournament g-value patterns as a **documented side effect** — same failure mode as DIPPER/SIRA/BIRA, different user intent. Policy unchanged: no watermark-stripping mode; users who need Art. 50 compliance should mark **after** unslop or use provider-marked output that survives their workflow (consumer Gemini copy-paste may retain marks; API output + unslop = no mark). SynthID's production deployment is the strongest citation that watermarking **can ship at scale** — and the SRI/WaterPark corpus is the strongest citation that it **cannot survive humanization**.

---

## 1. Paper identity

### 1.1 Primary paper — Nature 2024

| Field | Value |
|-------|-------|
| **Title** | Scalable watermarking for identifying large language model outputs |
| **Authors** | Sumanth Dathathri, Abigail See, Sumedh Ghaisas, Po-Sen Huang, Rob McAdam, Johannes Welbl, Vandana Bachani, Alex Kaskasoli, Robert Stanforth, Tatiana Matejovicova, Jamie Hayes, Nidhi Vyas, Majd Al Merey, Jonah Brown-Cohen, Rudy Bunel, Borja Balle, Ali Taylan Cemgil, Zahra S. Ahmed, Kitty Stacpoole, Ilia Shumailov, Ciprian Băetu, Sven Gowal, Demis Hassabis, Pushmeet Kohli (corresponding) |
| **Affiliation** | Google DeepMind |
| **Venue** | *Nature* 634, 818–823 (2024) |
| **Published** | 23 October 2024 |
| **DOI** | https://doi.org/10.1038/s41586-024-08025-4 |
| **Nature URL** | https://www.nature.com/articles/s41586-024-08025-4 |

**One-line contribution:** Tournament sampling generative watermark with configurable non-distortionary/distortionary modes; speculative-sampling integration for production latency; live Gemini quality validation at ~20M-response scale; open-sourced for developer adoption.

### 1.2 Naming in the wild

| Label | Where used | Meaning |
|-------|------------|---------|
| **SynthID-Text** | Nature paper, HF Transformers, MarkLLM/WaterPark | Text modality of SynthID family |
| **SynthID Text** | Google developer docs, HF blog | Same; spacing variant |
| **Tournament sampling** | Paper Algorithm 2 | Core sampling innovation |
| **LeftHash h=4** | SRI decomposition, supplementary | Sliding-window seed = hash of last H=4 tokens + key |
| **Non-distortionary SynthID** | Production Gemini config | Single-sequence non-distortion; quality-preserving default |

### 1.3 Timeline

| Date | Event |
|------|-------|
| May 14, 2024 | DeepMind blog: SynthID text watermarking announced for Gemini app/web |
| Oct 23, 2024 | *Nature* publication |
| Oct 23, 2024 | HF Transformers v4.46.0 SynthID merge (PR #34350) |
| Oct 2024 | `google-deepmind/synthid-text` reference repo + PyPI package |
| 2024–2025 | SRI Lab adversarial evaluation blog posts |
| Aug 2025 | SynGuard robustness paper (Queen's University) |
| Aug 2, 2026 | EU AI Act Art. 50 transparency obligations in force |
| 2026 | Google forum: Gemini API text **not** SynthID-watermarked |

---

## 2. Primary URLs

| Resource | URL | Notes |
|----------|-----|-------|
| **Paper (Nature)** | https://www.nature.com/articles/s41586-024-08025-4 | Definitive algorithm + production eval |
| **DOI** | https://doi.org/10.1038/s41586-024-08025-4 | |
| **DeepMind blog (May 2024)** | https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/ | Launch announcement |
| **SynthID product page** | https://deepmind.google/models/synthid/ | Consumer detection via Gemini chat (image/video/audio); text watermark described for app/web |
| **Google developer docs** | https://ai.google.dev/responsible/docs/safeguards/synthid | HF integration, detector tiers, limitations |
| **HF blog (Oct 2024)** | https://huggingface.co/blog/synthid-text | Transformers launch |
| **HF Transformers PR** | https://github.com/huggingface/transformers/pull/34350 | Merged v4.46.0 |
| **Reference GitHub** | https://github.com/google-deepmind/synthid-text | Research reference; not production-grade |
| **PyPI package** | https://pypi.org/project/synthid-text/ | Colab + Gemma/GPT-2 demos |
| **HF Space** | https://huggingface.co/spaces/google/synthid-text | Interactive demo |
| **Gemini watermark settings** | https://support.google.com/gemini/answer/17405358 | Visible watermark toggle; SynthID invisible layer always on for media |
| **Gemini API watermark thread** | https://discuss.ai.google.dev/t/does-gemini-api-text-output-carry-synthid-watermarking/177241 | Official: API text NOT watermarked |
| **SRI Lab red-team** | https://www.sri.inf.ethz.ch/blog/probingsynthid | Spoofing/scrubbing/presence detection |
| **Watermark Stealing (ICML 2024)** | https://arxiv.org/abs/2402.19361 · https://watermark-stealing.org/ | Pre-SynthID; frames detector API threat model |
| **SynGuard defense** | https://arxiv.org/abs/2508.20228 · https://github.com/githshine/SynGuard | +11.1% F1 vs SynthID under 4 attacks |
| **reverse-SynthID-text** | https://github.com/aloshdenny/reverse-SynthID-text | Community attack toolkit (paraphrase 90–100%) |
| **EU Art. 50 guide** | https://artificialintelligenceact.eu/transparency-rules-article-50/ | Aug 2026 timeline |
| **Sibling: WaterPark #20** | `docs/research/2026-08-detector-research/AGENT-20-WATERPARK-BENCHMARK.md` | SynthID DP-40 TPR 0.498 |
| **Sibling: KGW #74** | `docs/research/2026-08-detector-research/AGENT-74-KGW-WATERMARK.md` | Lineage + regulatory framing |
| **Sibling: SIRA #71** | `docs/research/2026-08-detector-research/AGENT-71-SIRA-WATERMARK-REMOVAL.md` | Paraphrase strip side effect |
| **Sibling: DAMAGE #12** | `docs/research/2026-08-detector-research/AGENT-12-DAMAGE-DETECTOR.md` | DIPPER → 1.5% TPR |
| **Sibling: BIRA #72** | `docs/research/2026-08-detector-research/AGENT-72-BIRA-WATERMARK-ATTACK.md` | Mechanism transfer to distribution-shift marks |

---

## 3. Algorithm — generation

### 3.1 Architecture decomposition

SRI Lab (ETH) decomposes production SynthID-Text as:

```
SynthID-Text = LeftHash(h=4) + increased context size + Tournament sampling(m≈30) + caching (K=1)
```

| Component | Role |
|-----------|------|
| **LeftHash seed generator** | Hash of preceding H=4 tokens + watermark key → random seed r_t per step |
| **g-functions** | m independent pseudorandom scorers g_ℓ(x, r_t); primary distribution Bernoulli(0.5) |
| **Tournament sampling** | Sample M=2^m candidates from p_LM; m-layer knockout tournament; winner = x_t |
| **Repeated context masking** | Cache: if same context window repeats, skip re-watermarking (K=1 for single-sequence non-distortion) |
| **Logits processor (HF)** | Applied after Top-K/Top-P in `.generate()`; no training required for embedding |

### 3.2 Tournament sampling (Algorithm 2)

At each decoding step:

1. Random seed r_t from sliding window (H tokens + key).
2. Sample M candidate tokens from LLM distribution p_LM(·|x_{<t}).
3. Pair candidates; layer ℓ=1..m uses g_ℓ(·, r_t) to pick winners; ties broken randomly.
4. Final survivor becomes output token x_t.

**Hyperparameters (paper defaults):**

| Symbol | Typical | Effect |
|--------|---------|--------|
| **m** (tournament layers) | 30 | More layers → stronger mark, uses more entropy per token |
| **H** (context window) | 4 | Seed diversity; h=4 increases scrubbing vulnerability (SRI spoofing-scrubbing tradeoff) |
| **N** (competitors per match) | 2 (non-dist.) / >2 (dist.) | N=2 → single-token non-distortionary |
| **K** (cache repeats) | 1 (production) | K>1 harder to detect presence but weakens mark |

**Latency:** Gemma 7B-IT on 4× v5e TPUs: 15.527 ms/token → 15.615 ms/token with 30-layer tournament (**+0.57%**). Gumbel +0.26%, Soft Red List +0.28%.

### 3.3 Non-distortionary vs distortionary

| Mode | Quality | Detectability | Production use |
|------|---------|---------------|----------------|
| **Non-distortionary** | Preserved (20M Gemini A/B) | Good | **Gemini App/Web default** |
| **Distortionary** | Some quality cost | Stronger | High-detectability scenarios |

Non-distortionary uses N=2 competitors per match + repeated context masking for single-sequence non-distortion (Supplementary G).

### 3.4 Relation to KGW (#74)

SynthID generalizes **distribution-shift** watermarking:

- KGW: fixed green-list logit bias δ on high-entropy tokens.
- SynthID: tournament picks tokens that score high under random g-functions — effectively **variable logit biases** per context.
- Red-Green presence-detection tests still pass on SynthID (SRI): fixed-context bias consistency survives tournament generalization.
- WaterPark labels SynthID alongside **TGRL** (KGW family) for robustness — not distribution-transform (RDF/GO).

---

## 4. Detection

### 4.1 Scoring functions

| Detector | Training | Output | Use case |
|----------|----------|--------|----------|
| **Mean / Weighted mean g-value** | None | Score ∈ [0,1]; threshold at target FPR | Rigorous FPR control; supplementary A.3 |
| **Bayesian detector (BD)** | Required on watermarked + human corpus | 3-state: watermarked / uncertain / not watermarked | **Production Gemini path**; better detectability under speculative sampling |
| **Frequentist z-test analog** | — | KGW-style hypothesis test | Not primary for SynthID; g-value aggregation instead |

Detection formula (mean g-values):

```
score(x) = (1/T) Σ_t mean_ℓ g_ℓ(x_t, r_t)
```

Longer text → more evidence. Low-entropy (factual) responses → weaker marks (same fundamental limit as KGW).

### 4.2 Detector access tiers (Google docs)

| Tier | Detector exposure | Threat model note |
|------|-------------------|-------------------|
| **Fully private** | Not released | Watermark Stealing D0 setting |
| **Semi-private** | Binary API (watermarked / not) | Realistic for SynthID image/audio; text API not public for Gemini |
| **Public** | Downloadable weights | HF research path; enables offline verification |

**Practical gap:** No public text watermark detection API for end users checking arbitrary pasted Gemini text. Consumer verification routes: ask Gemini about uploaded **media**; SynthID Detector portal accepts image/video/audio only.

### 4.3 Developer detection workflow (HF)

1. Fix `SynthIDTextWatermarkingConfig` (keys, m, H, g-distribution).
2. Train `BayesianDetectorModel` on watermarked outputs from **your** model + human negatives.
3. Run `SynthIDTextWatermarkDetector` with upper/lower thresholds calibrated to target FPR/FNR (demo defaults ~0.95 / ~0.12 — must retune per deployment).
4. Models sharing a tokenizer can share watermark config + detector if training corpus covers all generators.

### 4.4 Known detection limitations (Google acknowledged)

- Less effective on **factual/low-entropy** responses (few high-entropy choice points).
- Confidence drops sharply under **thorough rewrite** or **translation**.
- Not designed to stop **motivated adversaries** — raises cost, not a cryptographic proof.

---

## 5. Production deployment — Gemini

### 5.1 What is watermarked

| Surface | Text SynthID | Other SynthID | C2PA |
|---------|--------------|---------------|------|
| **Gemini App / Web** | ✅ Yes (invisible) | ✅ Images, audio, video | ✅ Media provenance |
| **Gemini API** | ❌ **No** (Google confirmed 2026) | ✅ Generated media modalities | Varies |
| **Third-party HF self-deploy** | ✅ If developer enables logits processor | — | — |

Nature paper: "non-distortionary SynthID-Text has been productionized and is currently watermarking responses in **Gemini and Gemini Advanced**."

### 5.2 Quality validation at scale

- **~20 million** live Gemini response pairs in user feedback study.
- Human side-by-side ratings: negligible quality/utility difference vs unwatermarked.
- First systematic watermarking investigation inside a **large-scale production LLM system** (authors' claim).

### 5.3 Consumer vs developer implications

**For EU deployers (Art. 50):**

- Pasting consumer Gemini output → likely carries SynthID mark (if not edited).
- Building on **Gemini API** → **must implement own marking** (SynthID HF toolkit, C2PA metadata, visible labels, or hybrid). Cannot cite Google's provider marking for API text (Guidelines point 74 inapplicable for that path).

**For provenance auditors:**

- Detecting Gemini consumer text requires Google's private/semi-private detector or a self-trained Bayesian detector with guessed/config-matched parameters — not turnkey for third parties today.

---

## 6. Attacks and robustness

### 6.1 Threat model summary

| Attack | Mechanism | SynthID outcome | Primary source |
|--------|-----------|-----------------|----------------|
| **Paraphrase / scrubbing** | Regenerate token sequence; destroy g-value pattern | **>90% success** (SRI); TPR → 0.498 (WaterPark DP-40) | SRI blog, WaterPark #20 |
| **Assisted scrubbing** | Watermark stealing → informed paraphrase | **~100%** FNR*@10⁻³ | SRI blog |
| **DIPPER paraphrase** | Trained paraphraser | 66.5% → **1.5%** TPR @ FPR 1% | DAMAGE #12 |
| **Copy-paste dilution** | 10% watermarked content | TPR → **0.039** | WaterPark CP1-10 |
| **ChatGPT 1-round paraphrase** | Off-the-shelf LLM rewrite | All schemes **TPR < 0.30** | WaterPark §5.2.4 |
| **Synonym substitution** | Lexical swap | F1 → 0.884 (community repro) | lilting.ch / reverse-SynthID |
| **Back-translation** | Round-trip MT | Sharp confidence drop; quality-correlated | SynGuard |
| **Watermark stealing → spoof** | Query API, learn approximate rules | **4%** FPR*@10⁻³ default; **15%** with 3× query budget | SRI blog |
| **Spoofing clue detection** | Detect learning-based forgeries | High power on stolen spoofs | SRI "Discovering Clues" |
| **Presence detection** | Red-Green black-box test | Detectable (p≈0) if context size estimated | SRI "Black-Box Detection" |
| **SIRA / BIRA** | Self-information / bias inversion rewrite | **Not in SynthID eval tables**; mechanism should transfer to distribution-shift marks | Agents #71, #72 |

### 6.2 SRI Lab four-axis evaluation (2024–2025)

**1. Presence detectable:** Watermark deployment cannot be hidden — Red-Green test passes on local SynthID-Text (not on Gemini 1.5 API, matching Google's claims).

**2. Spoofing harder than KGW:**

| Scheme variant | Spoof FPR*@10⁻³ |
|----------------|-----------------|
| LeftHash h=3 (KGW-like) | >80% |
| + increased context | 15% |
| + tournament sampling | 9% |
| + caching (full SynthID) | **4%** |
| Full SynthID + 3× query budget | 15% |
| Full SynthID + Bayesian detector | **5%** |

Tournament sampling and caching **help spoof resistance**; context size h=4 **hurts scrub resistance**.

**3. Spoofing leaves clues:** Stealing-based spoofs detectable by clue detector at high power.

**4. Scrubbing easy:**

| Scheme | Baseline paraphrase scrub | + stealing assist |
|--------|---------------------------|-------------------|
| LeftHash h=3 | 2% | 90% |
| LeftHash h=4 | 26% | 85% |
| **Full SynthID-Text** | **>90%** | **~100%** |

Paper supplementary C.6 showed AUC → 0.7 at 1000 tokens under paraphrase but lacked quality metrics and assisted scrubbing — SRI closes that gap.

### 6.3 WaterPark unified benchmark (#20)

Qwen2.5-14B generator; TPR @ FPR 1%:

| Condition | SynthID TPR |
|-----------|-------------|
| Clean | 0.998 |
| Typo | 0.321 |
| Token swap | 0.415 |
| Copy-paste 10% (CP1-10) | 0.039 |
| **DP-40 paraphrase** | **0.498** |
| Translation | 0.232 |

SynthID tracks TGRL/KGW paraphrase vulnerability — **not** a paraphrase silver bullet despite production scale.

### 6.4 DAMAGE humanizer path (#12)

Gemma-2B-IT + SynthID; DIPPER paraphrase as humanizer proxy:

| Condition | TPR @ FPR 1% |
|-----------|--------------|
| Watermarked | 66.5% |
| After DIPPER | **1.5%** |

Confirms commercial humanizer category strips SynthID as **side effect**, not just attack-lab artifact.

### 6.5 SynGuard partial defense (Aug 2025)

Hybrid **SIR semantic alignment + SynthID token marking**:

- +**11.1%** average F1 vs SynthID across paraphrase, synonym, copy-paste, back-translation.
- Not evaluated against SIRA/BIRA/RLCracker.
- Adds LM overhead; trades diversity for robustness.

### 6.6 Open-source attack surface

Google open-sourced the **full algorithm** (Oct 2024) — attackers need not reverse-engineer carrier frequencies (contrast: image SynthID). Community repo `reverse-SynthID-text` documents paraphrase as 90–100% effective because marks live in **token sequence**, not semantics.

**SIRA/BIRA gap:** No published SIRA table row for SynthID-Text. WaterPark + SRI paraphrase results imply SIRA would likely achieve high ASR — highest-impact missing experiment (flagged in Agents #71, #74).

---

## 7. Regulatory status (August 2026)

### 7.1 EU AI Act Article 50

| Date | Obligation |
|------|------------|
| **2 Aug 2026** | Art. 50 transparency rules apply (marking + disclosure for AI-generated content) |
| **2 Dec 2026** | Grace period ends for generative systems already on market before Aug 2026 |
| **Jun 2026 (expected)** | Final Code of Practice on AI-generated content |

**Art. 50(2) technical marking:** Providers of AI generating text/image/audio/video must ensure outputs are **machine-readable marked** and **detectable as AI-generated**. Free-form text >200 tokens: imperceptible in-content watermark required (metadata alone insufficient per Commission draft guidance).

**Provider reliance (Guidelines C(2026) 5054, point 74):** Deployers may rely on the **model provider's marking** when the provider implements compliant marking — **if** the mark survives to the end user.

### 7.2 SynthID vs Art. 50 — gap analysis

| Scenario | Art. 50 posture |
|----------|-----------------|
| User copies unedited **Gemini App** text | Provider mark likely present; detectability depends on private detector access |
| **Gemini API** text in EU product | **No provider mark** → deployer must add own (HF SynthID, metadata, visible label) |
| User runs text through **humanizer/unslop** | Mark degraded/removed → deployer cannot rely on upstream mark; must re-mark after editing |
| Deliberate watermark removal | **Prohibited** under Code of Practice (Dec 2025) — applies to tools targeting provenance, not just user intent |
| SynthID + C2PA on Gemini **media** | Multilayer marking aligned with Code of Practice direction; text lacks C2PA equivalent at consumer scale |

### 7.3 US / other

- **California SB 243** (companion chatbots, Jan 2026): transparency pressure; SynthID cited in industry compliance discussions.
- **OpenAI ChatGPT:** Text watermark **not deployed** (Aug 2024); Google is the contrasting production case for text — but only on consumer Gemini, not API.

### 7.4 Compliance officer takeaway

SynthID proves watermarking **can** ship at billion-user scale without measurable quality loss. It does **not** prove watermarking **equals** compliance after normal editing workflows. Any supply chain with paraphrase/humanization breaks the mark — unslop included.

---

## 8. Debate map

| Camp | Claim | Evidence |
|------|-------|----------|
| **Google / Nature optimists** | Production-ready; quality-preserving; best-in-class detectability vs Gumbel/SRL | 20M Gemini study; Nature benchmarks; 0.57% latency |
| **SRI / WaterPark pessimists** | Scrubbing trivial; spoofing costly but feasible; presence cannot be hidden | >90% scrub; DP-40 TPR 0.498; Red-Green detection |
| **Regulatory pragmatists** | Marking required; multilayer provenance; provider marks help when intact | Art. 50; Gemini API gap forces deployer action |
| **Humanizer vendors** | "Undetectable" marketing | DAMAGE: SynthID 66.5% → 1.5%; same pass breaks detectors |
| **Defense researchers (SynGuard)** | Semantic+token hybrid improves robustness | +11.1% F1; not paraphrase-proof |

**Synthesis:** SynthID moved the frontier from "can watermarking work in theory?" to "does it survive the real world?" Answer: **yes for shipping; no for paraphrase-as-normal-editing.**

---

## 9. Unslop integration

### 9.1 Side-effect overlap

| | SynthID mark | unslop rewrite |
|---|-------------|----------------|
| **Signal locus** | g-value pattern over token n-grams | AI-isms, surprisal flatness, register |
| **Mechanism** | Tournament-biased token choices | Paraphrase, burstiness, contraction |
| **Destroying target** | Regenerate tokens → g-values uncorrelated | Remove stock vocab / uniform surprisal |
| **Overlap** | **High** — any semantic-preserving full paraphrase scrubs both | Same pass |

From `skills/unslop/SKILL.md` (shipped):

> Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real. Users who need provenance should watermark after unslop, not before.

SynthID is the **named production instance** of that warning.

### 9.2 Policy boundaries (non-negotiable)

1. **No SynthID-stripping mode.** Do not optimize ASR against Google's g-value detector; do not port `reverse-SynthID-text` or SRI scrubbing pipelines.
2. **Anti-detector scope unchanged.** ESL/resume false positives — not Art. 50 evasion or academic misconduct.
3. **Watermark after unslop.** For users needing machine-readable provenance: generate → humanize → **apply mark** (self-deployed SynthID, C2PA where applicable, visible disclosure).
4. **Honest landscape docs.** Cite SynthID as production proof + WaterPark/SRI/DAMAGE numbers for fragility — paired citation, not either/or.
5. **`detector.py` ladder.** Keep refusal to recommend watermark removal at exhaustion; SynthID is not a TMR target.

### 9.3 Bench integration (optional)

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P2** | Verify SKILL.md cites SynthID + DP-40 / DAMAGE numbers | Already partially present via sibling agents |
| **P3** | Cross-link in research synthesis | Production vs API split is new Aug 2026 fact |
| **P4** | Do **not** add SynthID detector fixtures to `detector_bench.py` | Requires trained BD + key material; legal boundary |
| **P4** | SIRA × SynthID replication | Open research gap; neither SIRA nor BIRA papers include SynthID row |

### 9.4 User workflow guidance

```
Need provenance?
  ├─ Consumer Gemini text, no edits → mark may survive (verify with provider tools if available)
  ├─ Gemini API text → no upstream mark; deployer must mark
  └─ Any unslop pass → assume mark dead; re-watermark or disclose manually
```

---

## 10. Key numbers reference card

| Claim | Value | Source |
|-------|-------|--------|
| Venue | *Nature* 634:818–823 (2024) | nature.com |
| Published | 23 Oct 2024 | Nature |
| Gemini live quality study | ~**20 million** response pairs | Nature main text |
| Tournament layers (default) | m = **30** | Nature + supplementary C.1 |
| Context window H | **4** | Nature Fig. 2; SRI decomposition |
| Latency overhead (Gemma 7B, 30-layer) | **+0.57%** | Nature evaluation |
| WaterPark SynthID clean TPR @ FPR 1% | **0.998** | Agent #20 Table 2 |
| WaterPark SynthID DP-40 TPR | **0.498** | Agent #20 Table 2 |
| WaterPark SynthID CP1-10 TPR | **0.039** | Agent #20 Table 2 |
| DAMAGE SynthID → DIPPER TPR @ FPR 1% | 66.5% → **1.5%** | Agent #12 Table 2 |
| SRI scrubbing (full SynthID, no steal) | **>90%** FNR*@10⁻³ | SRI blog §4 |
| SRI scrubbing (+ stealing) | **~100%** | SRI blog §4 |
| SRI spoofing (full SynthID) | **4%** FPR*@10⁻³ | SRI blog §2 |
| SynGuard F1 improvement | **+11.1%** avg vs SynthID | arXiv:2508.20228 |
| ChatGPT 1-round paraphrase | All watermarkers TPR **< 0.30** | WaterPark §5.2.4 |
| Gemini API text watermarked | **No** | Google forum 2026 |
| EU Art. 50 in force | **2 Aug 2026** | artificialintelligenceact.eu |
| Art. 50 grace (existing systems) | **2 Dec 2026** | AI Omnibus May 2026 |

---

## 11. Open questions

1. **SIRA/BIRA on production SynthID params?** MarkLLM defaults used in WaterPark; Gemini production m/H/key unknown. Highest-impact missing red-team.
2. **Does consumer Gemini still watermark all model tiers in Aug 2026?** Product page says app/web; model-specific exceptions undocumented.
3. **Will Google ship API text watermarking before Dec 2026 EU grace ends?** Forum answer "not planned" — deployers building on API need alternatives now.
4. **Public text detection API?** Semi-private tier exists for image/audio; text detection for third-party auditors remains closed.
5. **SynGuard vs SIRA?** No unified eval.
6. **Long-form scrubbing:** SRI tested ~1000-token Dolly prompts; RLCracker (Agent #73) claims short-text attacks underestimate long-form — replicate on SynthID.
7. **Factual/low-entropy content:** Both Google and attackers know marks are weak on deterministic outputs — how does Art. 50 handle "mostly factual" AI text?
8. **unslop deterministic pass alone:** Does regex-only unslop scrub SynthID materially, or only LLM paraphrase tiers? Unknown without paired BD eval.

---

## 12. Bottom line

SynthID-Text is the **reference production deployment** for generative text watermarking — the answer to "did anyone actually ship this?" is **yes**, on consumer Gemini, with a *Nature* paper and open-source stack to match. It is **not** the answer to "does watermarking survive editing?" Paraphrase, humanizers, and assisted scrubbing collapse detectability to coin-flip or worse in published benchmarks; the Gemini **API** gap means most B2B EU deployers cannot outsource marking to Google for text anyway.

For unslop: SynthID names the exact upstream signal our rewrites may destroy. Cite it paired with WaterPark DP-40 and SRI scrub rates. Do not build against it. Tell users to mark **after** humanization.

---

*Agent #75 · SynthID-Text production watermark · August 2026*
