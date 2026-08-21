# Agent #52 — Voice-Match Stylometric Limits

**Topic:** When matching user voice fails detectors or helps ESL writers  
**Prepared:** 2026-08-19  
**Agent:** unslop deep research sub-agent #52  
**Status:** Complete research memo for voice-match / anti-detector boundary work  
**Code anchors:** `unslop/scripts/stylometry.py`, `unslop/scripts/style_memory.py`, `unslop/scripts/humanize.py::_format_voice_targets`, `skills/unslop/SKILL.md` voice-match + anti-detector procedures

---

## Executive summary

Voice-match and anti-detector are **partially orthogonal objectives** that unslop currently exposes as separate modes but does not always disambiguate for ESL users.

**Voice-match** (`/unslop voice-match`, `--voice-sample`, persisted `style-memory.json`) optimizes **stylometric fidelity** to a user-provided sample: sentence-length μ/σ, contraction rate, punctuation tics, Latinate ratio, pronoun rates, DivEye proxies (`sentence_length_cv`, `word_length_stdev`). `stylometry.py` measures; the LLM prompt applies. Success means the rewrite **looks like the sample**, not that it **passes GPTZero**.

**Anti-detector** optimizes **statistical naturalness** against classifier fingerprints: burstiness band (target σ ≥ 6), contraction injection, surprisal variance, cross-model second pass. Success means **lower detector probability**, not authorship attribution to the real user.

The 2025–2026 literature now treats these as **separable axes**:

| Axis | Question | Primary metrics | unslop mode |
|------|----------|-----------------|-------------|
| Style fidelity | Does it sound like *this* author? | Authorship attribution, STAR/TinyStyler distance, `StyleProfile.delta()` | voice-match |
| Statistical naturalness | Does it look machine-generated to a classifier? | Perplexity, burstiness σ, DivEye surprisal variance, contraction rate | anti-detector |

**Jemama et al. (2025)** showed completion prompting can reach **99.9% style-matching agreement** while human essays average **perplexity 29.5** vs matched LLM outputs at **15.2** — high fidelity, still detectable. **Catch Me If You Can? (EMNLP 2025)** showed six frontier models fail implicit personal-style imitation on blogs/forums even when style-matching improves with more shots.

**ESL implications are asymmetric:**

1. **Voice-match helps ESL** when the goal is *authenticity to the writer's own prior prose* (emails, cover letters, forum posts) — restoring idiolect after AI slop removal, not beating Turnitin.
2. **Voice-match fails detectors for ESL** when the user's natural profile overlaps the "AI-like" region detectors read: low TTR, low burstiness, low perplexity, sparse contractions — the same profile Liang et al. (2023) flagged on TOEFL essays.
3. **Anti-detector helps ESL false positives** by pushing text *away* from that region (Liang's ChatGPT "enhance to native speaker" intervention cut average FP from **61.3% → 11.6%**) — but that move **destroys voice-match fidelity** to the original ESL sample.

**unslop verdict:** Keep the modes separate. Document the conflict explicitly in `SKILL.md`. Do not promise voice-match clears detectors. For ESL users hit by false positives, recommend **anti-detector + cross-model pass**, optionally **after** a voice sample establishes register — not voice-match alone. Consider a future **`voice-match + anti-detector`** merge path that treats the sample as a **ceiling/floor band** (match register, but enforce minimum σ and contraction floor when user opts into detector defense).

---

## The two-objective problem (research basis)

### Style fidelity ≠ statistical naturalness

**Jemama & Kumar — "How Well Do LLMs Imitate Human Writing Style?"** (arXiv:2509.24930, UEMCON 2025)

- URL: https://arxiv.org/abs/2509.24930  
- DOI (IEEE): https://doi.org/10.1109/uemcon67449.2025.11267719  

Key numbers:

- Few-shot prompting: up to **23.5×** higher style-matching accuracy vs zero-shot.
- Completion prompting: up to **99.9%** agreement with original author style.
- Human essay mean perplexity: **29.5**; stylistically matched LLM outputs: **15.2** (paper also reports ~15.1–16.1 in places).

**Implication for unslop:** `_format_voice_targets()` can drive the LLM to nail numeric deltas on all 19 `StyleProfile` fields while the document remains in the low-perplexity basin detectors flag. Voice-match telemetry (`StyleDelta.largest_gaps()`) is not a detector score.

### Prompt-only voice cloning has a hard ceiling

**Wang et al. — "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors"** (EMNLP 2025 Findings)

- arXiv: https://arxiv.org/abs/2509.14543  
- ACL Anthology: https://aclanthology.org/2025.findings-emnlp.532/  
- DOI: https://doi.org/10.18653/v1/2025.findings-emnlp.532  
- Eval harness: https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation  
- Author page: https://www.zhengxiang-wang.me/papers/implicit-writing-styles/

Four-metric evaluation battery: authorship attribution, authorship verification, style matching, **AI detection** — the same decomposition unslop should use internally.

Findings:

- **40,000+ generations per model**, 400+ real authors, domains: news, email, forums, blogs.
- Structured formats (news, email): approximate imitation possible.
- Informal blogs/forums: **systematic failure**; outputs regress to generic LLM tone.
- More demonstrations help but plateau; outputs remain detectable as AI.

**Implication for unslop:** `SKILL.md` Known Limitation (already cites this paper) should stay. `stylometry.py` + 50-word minimum sample is **best-effort prompt conditioning**, not TinyStyler-class authorship embedding (https://github.com/zacharyhorvitz/tinystyler).

### Stylometric fidelity alone does not beat modern detectors

**Guo et al. — HLD: Approximate Hierarchical Linguistic Distribution Modeling** (ICLR 2026 poster)

- OpenReview: https://openreview.net/forum?id=[search ICLR 2026 HLD]  
- Stub repo: https://github.com/nefugr/HLD-Detector  

HLD stacks word n-gram LLR, POS n-gram LLR, dependency n-gram LLR, and semantic KDE — four features into XGBoost. Lexical-only humanization (stock-vocab stripping) is explicitly the attack surface; syntactic and semantic layers survive paraphrase.

**Synergizing Stylometrics with Semantics (SSLA)** (ACL 2026 Findings)

- PDF: https://aclanthology.org/2026.findings-acl.1855.pdf  

Stylometric fingerprints (syntactic rigidity, function-word usage) dominate when semantic homogeneity is high — exactly the Wikipedia-editor neutral prose voice-match can converge to if the sample is short or generic.

**Detecting the Machine benchmark** (arXiv:2603.17522)

- PDF: https://arxiv.org/pdf/2603.17522  

XGBoost on extended stylometric features (sentence-level perplexity CV, connector density, AI-phrase density) reaches **AUROC 0.9996** in-distribution. unslop's 19-field profile covers a **subset** of this feature space — no POS/dependency sequences, no semantic KDE.

---

## What `stylometry.py` measures (and what it cannot)

### Shipped signals (Phase 4)

From module docstring and `StyleProfile`:

| Field | Unit | Role |
|-------|------|------|
| `sentence_length_mean` / `sentence_length_stdev` | words | Burstiness primary; anti-detector targets σ ≥ 6 |
| `sentence_length_cv` | σ/μ | DivEye proxy — scale-invariant burstiness; flat AI ~0.3, human academic ~0.5–0.8 |
| `word_length_stdev` | chars | DivEye proxy — per-sentence mean word-length variance |
| `fragment_rate` | fraction | Human burstiness / casual register |
| `contraction_rate` | per 1k words | Paneru marker: AI ~0.00/chunk, human ~0.17/chunk |
| `em_dash_rate`, `semicolon_rate`, `colon_rate`, `parenthetical_rate` | per 1k | Punctuation idiolect |
| `type_token_ratio`, `function_word_rate` | ratio | Lexical diversity — ESL + AI both skew low TTR |
| `latinate_ratio` | ratio | Register (Anglo-Saxon vs Latinate) |
| `first_person_rate`, `second_person_rate` | per 1k | Persona / directness |
| `passive_voice_approx` | per 1k | Formal register proxy (noisy) |
| `starts_with_and_but` | fraction | Human burstiness tic |

Pipeline: strip code/YAML/tables/blockquotes (same prose contract as validator) → sentence split → regex counts. **No LM. No POS tagger. No embedding retrieval.**

### Integration path

```
User sample (≥50 words)
  → stylometry.analyze() → StyleProfile
  → optional style_memory.save_profile() → ~/.config/unslop/style-memory.json (numeric only, mode 0600)
  → humanize._format_voice_targets() → LLM prompt block
  → post-rewrite: StyleProfile.delta(sample, rewrite) → format_delta() for user feedback
```

Optional deeper reading: `surprisal.py` with `--surprisal-variance` (distilgpt2, DivEye 10-feature vector per https://arxiv.org/abs/2509.18880). Documented as **voice-match telemetry, not a gate** — same caution as Nicks et al. (ICML 2024) on detector scores.

### Known measurement gaps

1. **No perplexity / surprisal in the default profile** — the main detector axis for ESL bias (Liang et al.).
2. **No syntactic n-grams** — HLD's POS/dependency layers untouched by voice-match deltas.
3. **No authorship embedding distance** — cannot score STAR/TinyStyler-class fidelity (https://arxiv.org/abs/2310.11081, https://arxiv.org/abs/2312.17242).
4. **No semantic preservation check under stylization** — Yang & Carpuat 2025 register prompting shows meaning drift is a separate failure mode.
5. **Approximate passive voice** — labeled `_approx` in code; not suitable for high-stakes claims.
6. **50-word floor** — `style_memory.py` rejects shorter samples; signals remain noisy until ~200–500 words (vendor cold-start norms in Cat 10 synthesis).

---

## Voice-match procedure: what it optimizes

### SKILL.md six-signal checklist (LLM layer)

1. Average sentence length and variance  
2. Contraction rate  
3. Punctuation tics (em-dash, semicolon, parenthetical, fragments, And/But openers)  
4. Vocabulary register (Latinate vs Anglo-Saxon)  
5. Favorite phrases / rhetorical moves  
6. Forbidden patterns ("never uses exclamation marks", etc.)

Apply order: **register → cadence → punctuation → vocabulary**. Do not invent biographical detail for named public voices.

### Deterministic layer (numeric)

`_format_voice_targets()` injects measured values:

```text
VOICE SAMPLE TARGETS (measured — match these):
- Sentence-length mean: X words (σ Y, cv Z)
- Contractions per 1k words: ...
...
Higher cv and word-length σ both indicate bursty human rhythm
```

The LLM is told to **match the profile**, including **low σ** if the sample is flat — which is correct for voice fidelity and wrong for detector evasion.

### Style memory design constraint

`style_memory.py` persists **numeric-only** profiles — no free-text "user prefers warm tone" keys. Rationale: MIT/Penn State CHI 2026 sycophancy-memory finding (condensed preference strings amplify sycophancy). OWASP Agentic Applications 2026 memory-poisoning class. Schema closed; symlink refusal; 64 KB cap.

---

## Anti-detector procedure: what it optimizes (and conflicts)

From `skills/unslop/SKILL.md` anti-detector procedure:

1. **Burstiness band** — 4–35 words per sentence within paragraphs; **σ ≥ 6** (human academic ~8.2 vs GPT-4o ~4.1 per Cat 14 practitioner measurement and IMPLEMENTATION_TRACE.md).  
2. Break predictable structure (Turnitin anti-humanizer targets uniform bullet syntax).  
3. Contractions + fragments (Paneru 2026: human ~0.17 contractions/chunk vs AI ~0.00).  
4. User-supplied specificity (numbers, file names — cannot be faked).  
5. Rough edges (imperfect smoothness).  
6. Cross-model second pass (TempParaphraser EMNLP 2025, Adversarial Paraphrasing NeurIPS 2025).  
7. Re-anchor after turn 8/16 (HorizonBench / RMTBench drift).

**Direct conflict with voice-match:**

| Sample property | Voice-match instruction | Anti-detector instruction |
|---------------|-------------------------|---------------------------|
| σ = 3.5 (flat ESL academic) | Match σ 3.5 | Raise to σ ≥ 6 |
| contraction_rate = 5/1k | Match 5/1k | Inject toward human ~170/1k scale (skill: "don't", "won't", "it's") |
| Low TTR, high Latinate | Match register | Add fragments, Anglo-Saxon chunks, rough edges |
| No em-dashes | Match 0/1k | May add if burstiness needs (unslop caps 2/para globally in deterministic mode) |

unslop does **not** currently define precedence when both modes are requested. blader/humanizer resolves one tic conflict: voice sample **overrides em-dash ban**. unslop caps em-dashes at 2/paragraph but does not document sample-rate override in `SKILL.md` — gap.

---

## ESL: when voice-match helps vs when it fails detectors

### Why ESL writing gets flagged (mechanism)

**Liang, Yuksekgonul, Mao, Wu & Zou — "GPT detectors are biased against non-native English writers"** (Patterns, 2023)

- Journal: https://doi.org/10.1016/j.patter.2023.100779  
- arXiv: https://arxiv.org/abs/2304.02819  
- Stanford HAI summary: https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers  

Numbers on 91 TOEFL essays vs 88 US 8th-grade ASAP essays, seven detectors:

- TOEFL false-positive rate: **61.3%** average (61.22% in arXiv text).  
- Unanimous FP (all 7 detectors): **19.8%** of TOEFL essays.  
- At least one detector flagged: **97.8%** of TOEFL essays.  
- US essays: near-perfect correct classification.  
- Mechanism: flagged essays had **significantly lower perplexity** — limited lexical/syntactic range reads as "model-predictable."

Practitioner synthesis: https://www.enago.com/responsible-ai-movement/resources/writing-looks-like-ai-non-native-english-researchers/

Institutional response example: Vanderbilt disabled Turnitin AI detection (Aug 2023), citing FP rate × volume (Enago cites ~750 papers/year at claimed 1% FP).

**TextSight fingerprint table** (practitioner, useful for overlap mapping): https://www.textsight.ai/blog/ai-writing-fingerprint/

| Passage type | Typical perplexity | Burstiness (sentence SD) |
|--------------|-------------------|--------------------------|
| GPT-4o default | 12–22 | Low (~4–6 words) |
| Academic journal (human) | 28–45 | Low (~4–7 words) |
| **ESL student essay (human)** | **20–35** | **Low (~4–8 words)** |
| Blog/journalism (human) | 40–70 | High (~9–15 words) |

ESL human writing occupies **the same stylometric neighborhood as AI** on burstiness and often perplexity — not because it is AI, but because formal L2 production converges on predictable, grammatically safe patterns.

### Liang intervention paradox (critical for product framing)

Same paper, ChatGPT prompt: *"Enhance the word choices to sound more like that of a native speaker."*

- Average FP: **61.3% → 11.6%** (−49.7 percentage points).  
- Perplexity increased significantly (P ≈ 9.36×10⁻⁵).  
- Reverse experiment: simplify native 8th-grade essays → FP rose **5.19% → 56.65%**.

This is **anti-detector behavior**, not voice preservation. It explicitly **diverges from the author's original stylometric profile** to escape detector basins.

**Product ethics:** Offering ESL users voice-match alone implies "sound like you" but leaves them flagged. Offering only anti-detector implies "sound more native/statistically human" — legitimate false-positive defense per unslop Boundaries, but **not** "match my voice."

### When voice-match **helps** ESL writers

Legitimate use cases (aligned with `SKILL.md` Boundaries — not academic misconduct):

1. **Idiolect restoration after AI drafting** — User wrote prior emails/posts in their natural L2 English; AI rewrite added slop (`delve`, hedging stacks, uniform σ). Voice-match strips slop **and** pulls cadence back toward *their* established profile, not Wikipedia-neutral "humanized" baseline.

2. **Professional consistency** — Cover letters, LinkedIn, internal docs where the reader knows the author's prior tone. Stylometric delta feedback (`format_delta()`) gives actionable "your σ is 2.1 below sample" without claiming detector clearance.

3. **Anti-blandification** — arXiv:2603.18161 ("How LLMs Distort Our Written Language") documents ~70% shift toward argumentative neutrality under LLM assist. Voice-match is the **preserve-stance** counterweight; anti-detector alone can further neutralize.

4. **Numeric memory without sycophancy drift** — `style_memory.json` gives cross-session anchor (complements hook re-reinforcement at turn 8/16 per HorizonBench arXiv:2604.17283).

5. **Detector-agnostic authenticity** — Catch Me If You Can's four metrics include AI detection, but the user's goal may be "don't sound like ChatGPT" to a **human manager**, not "pass Turnitin." Voice-match targets human reader alignment.

### When voice-match **fails** (or worsens) detector outcomes

1. **Faithful replication of low-variance ESL profile** — If sample σ = 4.0, cv ≈ 0.25, TTR low, contractions sparse, voice-match **instructs the model to stay there** — maximizing fidelity, maximizing FP risk on perplexity/burstiness detectors.

2. **Short or generic samples** — <50 words: warning-only path in `_build_voice_block`. 50–200 words: high variance on σ and contraction_rate; LLM may "average toward RLHF mean" anyway (EACL 2024 PERSONALIZE feasibility study: https://aclanthology.org/2024.personalize-1.6/).

3. **AI-polished sample as "voice"** — If user pastes ChatGPT output as their sample, profile encodes **AI stylometrics**; voice-match locks in detectable fingerprints (Jemama separability applies in reverse).

4. **Informal domain** — Catch Me If You Can: blogs/forums fail even with six frontier models; voice-match six-signal checklist is strictly weaker.

5. **Post-paraphrase detectors** — DivEye (https://arxiv.org/abs/2509.18880, TMLR 2026): intra-document **surprisal variance** survives synonym swap. Matching sentence-length cv alone does not reproduce DivEye's per-token variance pattern without `--surprisal-variance` LM pass.

6. **Turnitin anti-humanizer (Aug 2025+)** — Trained on humanizer outputs; uniform-structure tells. Voice-match that preserves user's parallel bullet habit may remain flagged even if σ improves slightly.

7. **blader/humanizer parallel** — Editorial humanization can **increase** GPTZero scores (https://github.com/blader/humanizer/issues/2). Voice-match without anti-detector moves is in the same risk class when the target is classifier score, not reader quality.

### Paneru contraction marker (shared AI + voice-match lever)

**Paneru — "Please Make it Sound like Human: Encoder-Decoder vs. Decoder-Only Transformers for AI-to-Human Text Style Transfer"** (arXiv:2604.11687, April 2026)

- URL: https://arxiv.org/abs/2604.11687  

AI inputs: **0.00** contractions/chunk; human references: **0.17**/chunk. Also: human text ~4 grade levels lower Flesch-Kincaid, shorter words, greater sentence-length variance.

unslop encodes this in anti-detector + optional `soul.py` contraction pass. Voice-match **matches sample contraction_rate** — if ESL sample has 0 contractions (formal L2 habit), voice-match preserves 0; anti-detector injects them. **Another explicit conflict.**

---

## Mode interaction matrix (recommended user guidance)

| User goal | Recommended mode | Why |
|-----------|------------------|-----|
| "Sound like my old emails" | voice-match + sample | Fidelity axis; ignore detector |
| "GPTZero flagged my human essay" | anti-detector (+ cross-model pass) | Statistical naturalness; cite Liang FP bias |
| "AI draft → my voice, not flagged" | **Both, sequenced** | See workflow below |
| "Sound like Paul Graham" | voice-match (public style only) | No bio invention; still won't pass authorship test |
| "Beat Turnitin for AI essay" | **Decline** | Boundaries |

### Proposed sequenced workflow (not yet shipped as single command)

1. **Measure baseline** — `analyze(user_sample)` + optional `analyze(draft)`.  
2. **voice-match rewrite** — Remove slop; match register/cadence.  
3. **Check delta** — `StyleProfile.delta()`; if largest gaps are σ/cv/contractions *below* sample, stop (fidelity win).  
4. **If detector FP persists and user opts in** — anti-detector pass with **constrained bands**: e.g. raise σ toward max(sample σ, 6), raise contractions toward max(sample rate, human floor), preserve Latinate ratio ±ε and first-person rate (register anchor).  
5. **Cross-model second pass** — different provider (TempParaphraser / Adversarial Paraphrasing citation in `detector.py`).  
6. **Re-measure** — Report both stylometric delta **and** detector probability if `--detector-feedback` enabled.

This is the honest merge of Jemama's two axes without pretending one mode serves both masters equally.

---

## Evaluation gaps (what unslop should not claim)

| Claim | Verdict |
|-------|---------|
| "Voice-match passes GPTZero" | **False** — Jemama, Catch Me If You Can, blader #2 |
| "Voice-match equals authorship cloning" | **False** — EMNLP 2025; fine-tuning wins (TinyStyler) |
| "Stylometric delta → 0 implies human" | **False** — LLM can match counts with wrong POS/semantic trajectory (HLD) |
| "ESL users should use voice-match for Turnitin" | **Misleading** — use anti-detector FP defense framing or decline misconduct |
| "50-word sample is enough for stable σ" | **Weak** — style_memory enforces ≥50; Cat 10 norms 200–500+ for cold start |

Suggested eval additions (research-only, not shipping blockers):

1. **Liang TOEFL slice** — Run deterministic + voice-match + anti-detector on public TOEFL excerpts; report TMR/Desklib/GPTZero if licensed, at minimum stylometric profile movement.  
2. **Two-axis dashboard** — Style fidelity (embedding distance or EMNLP harness) vs perplexity/burstiness (DivEye features).  
3. **Conflict test suite** — Samples with σ ∈ {3, 5, 8, 12}; verify voice-match preserves, anti-detector raises, merged policy respects floors.

---

## Primary sources (full URLs)

### Core two-axis / voice-match limits

| Paper | URL |
|-------|-----|
| Jemama & Kumar 2025 — style vs detectability | https://arxiv.org/abs/2509.24930 |
| Wang et al. 2025 — Catch Me If You Can? (EMNLP) | https://arxiv.org/abs/2509.14543 |
| ACL Anthology EMNLP 2025 | https://aclanthology.org/2025.findings-emnlp.532/ |
| Eval harness | https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation |
| Patel et al. 2024 — author embeddings | https://arxiv.org/abs/2312.17242 |
| TinyStyler repo | https://github.com/zacharyhorvitz/tinystyler |
| EACL 2024 prompt stylization ceiling | https://aclanthology.org/2024.personalize-1.6/ |
| Blandification measurement | https://arxiv.org/abs/2603.18161 |
| RLHF homogenization (Biber features) | https://arxiv.org/abs/2604.14111 |

### ESL / detector false positives

| Paper / resource | URL |
|------------------|-----|
| Liang et al. 2023 (Patterns) | https://doi.org/10.1016/j.patter.2023.100779 |
| Liang et al. 2023 (arXiv) | https://arxiv.org/abs/2304.02819 |
| Stanford HAI news | https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers |
| Enago practitioner summary | https://www.enago.com/responsible-ai-movement/resources/writing-looks-like-ai-non-native-english-researchers/ |
| Gonzaga faculty guide (burstiness + perplexity) | https://researchguides.gonzaga.edu/GenerativeAIforFaculty/AIDetectors |
| TextSight fingerprint table | https://www.textsight.ai/blog/ai-writing-fingerprint/ |
| Pangram ESL/FPR tradeoff (DAMAGE co-author) | https://www.pangram.com/blog/humanizers-aug-25 |

### Detection / stylometry (anti-detector axis)

| Paper | URL |
|-------|-----|
| DivEye (TMLR 2026) | https://arxiv.org/abs/2509.18880 |
| Paneru 2026 — contractions + variance | https://arxiv.org/abs/2604.11687 |
| DAMAGE audit | https://arxiv.org/abs/2501.03437 |
| Adversarial Paraphrasing (NeurIPS 2025) | https://arxiv.org/abs/2506.07001 |
| TempParaphraser (EMNLP 2025) | https://aclanthology.org/2025.emnlp-main.1607/ |
| SSLA stylometric-semantics (ACL 2026) | https://aclanthology.org/2026.findings-acl.1855.pdf |
| Detector benchmark 2026 | https://arxiv.org/pdf/2603.17522 |
| Beyond "AI Language" — LLM idiolect | https://arxiv.org/pdf/2608.06589 |

### unslop internal / related memos

| Resource | URL |
|----------|-----|
| Cat 10 Style Transfer synthesis | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |
| IMPLEMENTATION_TRACE (σ 8.2 vs 4.1, previously misattributed to Kalemaj) | `docs/research/IMPLEMENTATION_TRACE.md` |
| RESEARCH_AND_TECH | https://github.com/MohamedAbdallah-14/unslop/blob/main/docs/RESEARCH_AND_TECH.md |
| Agent #32 blader/humanizer voice calibration | `docs/research/2026-08-detector-research/AGENT-32-BLADER-HUMANIZER.md` |
| Agent #14 HLD syntactic layers | `docs/research/2026-08-detector-research/AGENT-14-HLD.md` |

---

## Recommendations for unslop (actionable)

### SKILL.md / docs (high priority)

1. **Add "Voice-match vs anti-detector" subsection** under voice-match procedure — state Jemama separability in one paragraph with arXiv link.  
2. **ESL callout** — Link Liang et al.; explain that faithful voice-match may **not** reduce detector scores; point to anti-detector for FP defense.  
3. **Sample override rule** — Document: if sample `em_dash_rate` exceeds default cap, sample wins (parity with blader/humanizer).  
4. **Conflict precedence** — When user requests both: default **voice-match first, anti-detector second with register anchors**; never silently overwrite sample Latinate/first-person targets.  
5. **Do not cite Liang "native enhancement" as voice-match** — it is the anti-pattern for authenticity; cite as detector-FP mitigation only.

### Code (medium priority)

1. **`format_delta()` UX** — When `sentence_length_stdev` gap is negative (rewrite exceeds sample σ) and user is in voice-match-only mode, surface: "Rewrite is burstier than your sample — good for detectors, may diverge from your voice."  
2. **Optional `--voice-floor-σ`** — CLI flag: `max(sample_σ, floor)` for merged ESL defense path.  
3. **Eval hook** — Benchmark fixture: ESL-like low-σ sample + AI draft; track two-axis movement.

### Research / eval (lower priority)

1. Port EMNLP 2025 harness metrics on unslop outputs (attribution + detection), not just internal AI-ism residual check.  
2. Compare `--surprisal-variance` reading before/after voice-match — expect minimal movement if only surface counts changed.

---

## Bottom line

**Voice-match** answers: *"Does this read like the user's sample?"*  
**Anti-detector** answers: *"Does this escape classifier basins?"*  

For ESL writers, those questions diverge because **L2 formal English is statistically AI-like** to perplexity/burstiness detectors (Liang 2023). Matching the user's authentic low-variance profile is the **right** outcome for voice restoration and the **wrong** outcome for detector clearance. unslop's architecture (`stylometry.py` + separate modes) already encodes the right split; the product gap is **explicit user guidance and merge policy**, not more stylometric fields.

Fine-tuning on author corpus (Catch Me If You Can?, TinyStyler) remains the only path to production authorship cloning. Prompt-based voice-match with numeric anchors is **best-effort idiolect alignment** — valuable for human readers, insufficient for stylometric attribution tests, and **orthogonal to ESL false-positive defense** unless anti-detector constraints are applied as a second pass with documented tradeoffs.
