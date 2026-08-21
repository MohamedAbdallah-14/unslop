# SYNTH-89 — Stylometric Signals for Detection and Humanization

**Synthesis Agent #89**  
**Date:** 2026-08-19  
**Inputs:** Agent memos #41–55 (contraction stylometry through surprisal dynamics)  
**Scope:** Unified signal taxonomy, detection vs humanization axes, unslop lever map, honest limits  
**Audience:** unslop maintainers, SKILL.md authors, benchmark CI, research docs

---

## Executive summary

Stylometric detection and humanization are **not one knob**. The 2023–2026 literature converges on a **multi-layer signal stack** where surface markers (contractions, stock vocab), syntactic rhythm (sentence-length σ/CV), register geometry (Biber features), distributional homogenization (RLHF/DPO), and surprisal **dynamics** (DivEye, TSD, SurpMark) are **partially independent**. Optimizing one layer does not fix another.

| Layer | Primary signal | Detection use | Humanization lever | unslop today |
|-------|----------------|---------------|-------------------|--------------|
| **Lexical** | Stock vocab, TTR, AI-phrase density | XGBoost hybrids, RoBERTa n-grams | Regex scrub (`humanize.py`) | ✅ Shipped |
| **Syntactic rhythm** | σ/CV of sentence word counts | Desaire #8, practitioner σ~4 AI vs ~8 human | `structural.py` split/merge | ✅ Partial (split-only) |
| **Register** | Biber 67 features (nominalizations, that-clauses, relatives) | Reinhart/Rallapalli AUC ~0.98 | RG-style LLM conditioning (future) | ⚠️ ~8/67 proxies |
| **Surface register** | Contraction rate, Flesch-Kincaid | Paneru 0.00 vs 0.17/chunk | `soul.py` injection | ✅ Shipped |
| **Homogenization** | Semantic SCR, Biber chat-cluster | HIP base vs instruct; alignment tax | Anti-blandification + cross-model | ⚠️ Partial |
| **Surprisal global** | σ(surprisal), Δ² block | DivEye (TMLR 2026) | `surprisal.py` (measure only) | ⚠️ Opt-in telemetry |
| **Surprisal temporal** | Late-half DD/LV; transition matrices | TSD, SurpMark (2026) | Not implemented | ❌ Gap |
| **Voice/idiolect** | Authorship embeddings, LIWC/WritePrint | Catch Me AA/AV battery | `voice-match` prompt + `stylometry.py` | ⚠️ Prompt-bound |

**Core honest finding:** unslop's deterministic stack (lexical + structural + soul) moves TMR **`p_ai` by ~0.0–0.2 pp** on fixtures while removing visible slop. That is the expected outcome when detectors read **multi-feature distributional fingerprints**, not word lists. Humanization value = slop removal + register restoration + ESL false-positive defense — not RAID-grade bypass.

**Core architectural finding:** Jemama (2025) and Catch Me (2025) prove **style fidelity ⊥ statistical naturalness**. unslop's separate `voice-match` and `anti-detector` modes are correct; merging them requires explicit precedence and dual-oracle evaluation.

---

## 1. Signal taxonomy — what "stylometry" means in 2026

### 1.1 Three "burstiness" families (do not conflate)

From Agent #49 — GPTZero marketing and academic literature use the same word for different quantities:

| Family | Measures | Typical metric | unslop module |
|--------|----------|----------------|---------------|
| **Syntactic burstiness** | Sentence shape | σ(word count), CV, consecutive Δ | `structural.py`, `stylometry.py` |
| **Token surprisal burstiness** | LM predictability swings | σ(−log p), Δ² entropy | `surprisal.py` |
| **IR burstiness** | Term re-appearance | Poisson mixture (Church & Gale) | Not used |

**Rule:** Raising sentence-length σ does **not** guarantee higher DivEye Δ² block or TSD late-half volatility. Full defense needs **both** syntactic and token layers.

### 1.2 Register vs idiolect vs homogenization

| Concept | What varies | Key source |
|---------|-------------|------------|
| **Register** | Situational packaging (abstract vs Reddit) | Biber MDA; Rallapalli: **genre > model > decoding** |
| **Idiolect** | Individual habit within register | Catch Me AA/AV; StyleTunedLM PEFT |
| **Homogenization** | RLHF/DPO collapse toward shared assistant basin | Alignment Tax SCR 40–79%; Abdulhai ~70% stance neutralization |

Detectors exploit **homogenization** (chat models cluster in Biber space) and **register mismatch** (formal ESL prose ≈ AI perplexity profile per Liang 2023). Voice-match targets **idiolect**; anti-detector targets **escape from AI/homogenized basins** — often in tension (Agent #52).

### 1.3 The surprisal dynamics stack (2026 frontier)

```
Token surprisal sequence s₁…sₙ
  ├─ GLOBAL distributional     DivEye: μ, σ, γ₁, γ₂, Δ, Δ² block
  ├─ POSITION-SPLIT temporal   TSD: derivative dispersion + local volatility on 2nd half
  ├─ DISCRETE Markov           SurpMark: k-state transitions → ΔGJS vs human/machine refs
  └─ LOCAL multiscale          Lastde++ (adjacent, not shipped)
```

TSD ablation: second-half features beat full-sequence by **6+ AUROC points**. Global σ inflation **misses** late-stage volatility decay — AI text "settles" in the back half.

---

## 2. Signal catalog — detection fingerprints and humanization targets

### 2.1 High-confidence single-feature tells

| Signal | Human vs default AI | Strength | Caveats |
|--------|---------------------|----------|---------|
| **Contraction rate** | ~0.17/chunk vs ~0.00 (Paneru 2026) | Very strong on prompt-formalized corpora | Genre-dependent; Rallapalli shows LLM **overuse** in aggregate RAID; model idiolect 120–30,000/million (2026 idiolect paper) |
| **Sentence-length σ (paragraph)** | ~6–8+ vs ~2–4 (Desaire; practitioner ~8.2 vs ~4.1) | Strong (#8 in Desaire XGBoost) | Mean length alone weak; ESL formal prose also low-σ |
| **Sentence-length CV** | ~0.55–0.75 human vs <0.35 AI (commercial targets) | Strong in RF stacks | Scale-invariant; voice-match may preserve low CV |
| **Flesch-Kincaid grade** | Human ~11.5 vs AI ~17.8 (Paneru) | Very strong | Coupled with contraction/register bundle |
| **Nominalization density** | 1.5–2× human (Reinhart PNAS 2025) | Strong Biber discriminator | `latinate_ratio` proxy only in unslop |
| **That-clause subjects (f29)** | LLM overuse (Rallapalli top-5) | Strong in Biber RF | No unslop counter yet |
| **Global surprisal σ** | Human wider intra-doc variance (DivEye) | Paraphrase-resistant | Needs scoring LM |
| **Late-half volatility (TSD DD/LV)** | AI 24–32% lower in 2nd half | Orthogonal to global DivEye | Position-aware humanization required |
| **Surprisal recovery transitions** | LLM snap-back to predictable states (SurpMark) | High AUROC (~91%) | Needs reference corpora |

### 2.2 Feature bundles detectors actually use

**"Detecting the Machine" (arXiv:2603.17522):** 22+ hand features including contraction ratio, burstiness, hedging density, sentence-length entropy → XGBoost **AUROC 0.9996** in-distribution. Contraction is one of many; perplexity CV ranks higher.

**Rallapalli Biber RF (arXiv:2604.14111):** **AUC ~0.9775** on 67 features. Top story = **SHAP interactions** (TTR modulates other features), not any single counter. Overuse bundle: that-subj, contractions (aggregate), participial whiz, nominalizations, sentence relatives. Underuse: wh-object relatives, pied-piping, *though*, discourse particles.

**HLD (ICLR 2026):** Word + POS + dependency n-grams + semantic KDE — lexical-only humanization is the attack surface; syntactic layers survive paraphrase.

**Commercial stack (2026):** GPTZero v6 predictability cones + learned ensemble; Turnitin anti-humanizer (uniform structure); DivEye-class features in technical reports. None publish per-feature weights.

### 2.3 Homogenization as detectable prior

Three mechanistic layers (Agent #46):

1. **Semantic SCR** — Liu Alignment Tax: 40% TruthfulQA questions → single semantic cluster post-DPO; decoding cannot fix (T=1.5 still 38% SCR).
2. **Register clustering** — Reinhart/Rallapalli/Sardinha: instruct models cluster together in Biber space, away from humans and base models.
3. **Stance neutralization** — Abdulhai: ~68.9% increase in neutral essays; LLM edits shift embeddings in a **common direction** even for "grammar only."

**HIP flip (arXiv:2605.19516):** GPTZero scores base-model continuations **96.7% human** vs instruct **30.3%** (Llama-3-8B). Detectors are partly **post-training sensors**, not generic machine-text oracles.

**Detection implication:** Blandified/homogenized text is often **easier** to flag, not harder — but **shallow paraphrase stays inside the cluster** (AdvPara: +8–15% TPR on naive rewrite).

---

## 3. Two orthogonal humanization axes

### 3.1 Style fidelity vs statistical naturalness (Jemama 2025)

| Axis | Metric | Human | High-fidelity LLM |
|------|--------|-------|-------------------|
| Style fidelity | Authorship verifier (char n-grams + MiniLM) | — | Up to **99.9%** (completion prompting) |
| Statistical naturalness | GPT-2 document PPL | **μ = 29.5** | **μ = 15.2–16** (all conditions) |

**No correlation** between fidelity and PPL in scatter. Few-shot gain up to **23.5×** vs zero-shot on style match — does **not** move PPL toward human band.

**unslop mapping:**

| Axis | Mode | Module |
|------|------|--------|
| Fidelity | `voice-match` | `stylometry.py` → LLM prompt targets |
| Naturalness | `anti-detector` | `structural.py`, `soul.py`, `surprisal.py`, cross-model pass |

**Gap:** No dual-oracle benchmark row reporting both on the same rewrite (Agent #50 P1).

### 3.2 Voice-match vs anti-detector conflicts (Agent #52)

| Sample property | voice-match | anti-detector |
|-----------------|-------------|---------------|
| σ = 3.5 (flat ESL) | Match 3.5 | Raise to σ ≥ 6 |
| contraction_rate = 0 | Match 0 | Inject toward human floor |
| Low TTR, high Latinate | Match register | Fragments, Anglo-Saxon chunks |

**ESL asymmetry (Liang 2023):** TOEFL essays **61.3% FP** average; mechanism = low perplexity + low variance. Liang's "enhance to native speaker" prompt cut FP to **11.6%** — that is **anti-detector**, not voice preservation.

**Recommended sequenced workflow (not yet single command):**

1. Measure baseline (`stylometry.analyze` + optional surprisal)
2. `voice-match` — remove slop, match sample
3. If detector FP persists and user opts in → `anti-detector` with **register anchors** (preserve Latinate ratio, first-person rate; floor σ at max(sample_σ, 6))
4. Cross-model second pass
5. Re-measure both axes

### 3.3 Prompt-only voice ceiling (Catch Me 2025)

Blog authorship verification: human **91.4%** vs best LLM **~17–21%**. Few-shot gain **~2.4×**, not 23.5× (that figure is Jemama). More shots (2→10) **flat**. GPTZero human-likeness on blogs: GPT-4o **~0.5%**.

**Upgrade path:** StyleTunedLM PEFT **87.9%** authorship vs **69.3%** 5-shot; P2P hypernetwork LoRA **33×** faster than OPPU; TinyStyler beats GPT-4 on authorship transfer. None tested in unslop; none ship in-plugin.

---

## 4. Humanization philosophy — subtract, preserve, restore variance

### 4.1 Ibrahim warmth–reliability (Nature 2026)

Warmth-trained models: **+7.43 pp** error avg; **+11 pp** with false user beliefs; **+12.1 pp** with emotion + false beliefs. Cold controls on identical data: **no degradation**.

**unslop license for Principle #1 ("Subtract, don't add"):** Delete sycophancy/hedging — do not paraphrase into softer agreement. Anti-detector burstiness/contraction moves are **distribution-shaping**, not empathy injection.

### 4.2 Anti-blandification (Abdulhai 2026)

~**70%** stance neutralization under heavy LLM use. Blandification **increases** detectability (shared low burstiness, analytical LIWC, aligned embeddings). unslop `balanced` mode + ANTI-BLANDIFICATION block in LLM path preserves stance while stripping slop.

**Commercial trap:** "Neutralize detectors" humanizers often **double-homogenize** — RLHF base + uniform rewrite → Turnitin anti-humanizer target class.

### 4.3 Four-cue calibration (Humanizing Machines, EMNLP 2025)

unslop operates primarily on **linguistic cues** (lexical + structural + soul). Partial on **behavioral** (sycophancy/signposting removal) and **cognitive** (`--strip-reasoning`). Out of scope: **perceptual** (avatars, UI).

Philosophy = **capability–expectation alignment**: strip fake warmth/reasoning; add authentic writer cues (contractions, burstiness) matching competent human prose — not companion-level anthropomorphism.

### 4.4 Alignment-tax-aware anti-detector doctrine

1. **Subtract, don't re-author** — DPO removed diversity at training; "write like a human from scratch" re-homogenizes (Abdulhai basin shift).
2. **Preserve stance and idiolect** — homogenization neutralizes opinions; ESL defense ≠ invent voice.
3. **Decoding is not a humanizer** — Liu Exp. 15: SCR persists at T=1.5.
4. **Cross-model when same-family exhausts** — Rallapalli chat clustering; HIP regime change.
5. **Measure dispersion, not just TMR** — log DivEye proxy + sentence CV pre/post.

---

## 5. unslop lever map — signal → module → mode

### 5.1 Pipeline order (homogenization-aware)

```
Input (instruct-tuned artifact)
  → Phase 0: _protect() placeholders
  → Phase 2: lexical scrub (stock vocab, hedging, sycophancy)     [all modes]
  → Phase 1: structural.py (split long, merge bullet soup)        [balanced+]
  → Phase 5: soul.py (contraction injection)                      [balanced+]
  → Phase 4: stylometry.analyze() (measurement)                   [voice-match]
  → Phase 3: lexical_targets (blocked without baseline JSON)      [anti-detector]
  → optional: surprisal.py (--surprisal-variance)                 [telemetry]
  → optional: LLM rewrite + ANTI-BLANDIFICATION                   [balanced+ LLM]
  → optional: detector.feedback_loop (TMR; surprisal logged only) [anti-detector CLI]
  → validate.py (preservation + AI-ism residual + burstiness warn)
```

### 5.2 Signal-to-lever matrix

| Signal | Detection weight | Humanization pass | Mode | Moves TMR? |
|--------|------------------|-------------------|------|------------|
| Stock vocab / hedging | High (lexical) | `humanize.py` regex | all | ~0 pp |
| Sycophancy openers | Behavioral tell | `humanize.py` | balanced+ | ~0 pp |
| Sentence-length σ | Desaire #8 | `structural.py` split | balanced+ | minimal alone |
| Bullet-soup uniformity | Commercial anti-humanizer | `merge_bullet_soup` | balanced+ | minimal |
| Contraction rate | Paneru, StyloAI | `soul.py` | balanced+ | ~0–0.2 pp |
| Fragment / short sentence | Desaire #10 | LLM anti-detector step 1 | anti-detector | varies |
| TTR / latinate | Biber f43, f14 proxy | lexical rules + voice-match | mixed | minimal |
| Nominalization / that-clause | Biber top-5 | ❌ no deterministic lever | — | — |
| Global surprisal σ, Δ² | DivEye 39% importance | ❌ measure only | anti-detector telemetry | not wired |
| Late-half DD/LV | TSD +6 AUROC vs full-seq | ❌ not implemented | — | — |
| Transition recovery | SurpMark | ❌ not implemented | — | — |
| Cross-model fingerprint | HIP, TempParaphraser | LLM procedure step 6 | anti-detector | best practical |
| Register profile delta | Biber RF | voice-match LLM (future RG) | voice-match | N/A |
| Document discourse template | ZeroStylus Γ_p | ❌ not implemented | voice-match future | N/A |

### 5.3 Anti-detector lever ordering (evidence-based)

From Agents #41, #49, #54, #46 — local levers before cross-model:

| Priority | Lever | Rationale |
|----------|-------|-----------|
| 1 | **Cross-model paraphrase** | Exits instruct cluster (HIP); breaks single-family fingerprint |
| 2 | **Syntactic burstiness** (σ, fragments) | Desaire #8; AdvPara warns lexical-only **hurts** |
| 3 | **Surprisal dynamics** (global + late-half + transitions) | 2026 detector stack; unslop partial |
| 4 | **Contraction injection** | Strong register marker; insufficient alone for TMR |
| 5 | **User-specific specificity** | Out-of-training details; cannot be faked |

Contraction is **item #4**, not #1 — fix Paneru attribution (not "Kalemaj") in SKILL mirrors.

### 5.4 structural.py — what sentence-length restoration covers

**Shipped:** Split overlong sentences in flat paragraphs (σ < 5); merge ≥3 parallel short bullets.

**Not shipped (by design):** Short-sentence/fragment injection, adjacent-short merge, gamma/CV targeting. Deterministic pass is **split-half** of human rhythm; anti-detector LLM carries the other half.

**Deadlock:** Five uniform ~24-word sentences with no safe split boundary → structural no-op; LLM or manual edit required.

---

## 6. Measurement and evaluation — what to report

### 6.1 Three-axis benchmark (recommended)

| Axis | Metrics | Source papers |
|------|---------|---------------|
| **Slop removal** | AI-ism residual, validator pass | unslop internal |
| **Style fidelity** | `StyleProfile.delta()`, optional Biber/NeuroBiber delta | Jemama verifier analogue; Catch Me AV |
| **Statistical naturalness** | σ, CV, surprisal_stdev, TSD DD/LV, SurpMark ΔGJS, TMR@FPR | Jemama, DivEye, TSD, SurpMark, RAID |

Never conflate TMR movement with voice fidelity or slop removal.

### 6.2 Genre-stratified baselines (mandatory per Rallapalli)

Single global human band fails across Abstracts vs Reddit. Ship `stylometric_baseline.json` keyed by genre heuristic — unblocks `lexical_targets.py` and contraction policy (inject in formal AI slop; reduce where humans under-contract).

### 6.3 Optional tooling tiers

| Tier | Tool | Use |
|------|------|-----|
| **Eval-only** | NeuroBiber/BiberPlus `--biber-profile` | Auditable register delta |
| **Eval-only** | Catch Me `deploy_AV_models.py` on before/after | External voice oracle |
| **Opt-in runtime** | `surprisal.py` + future TSD/SurpMark | Dynamics telemetry |
| **Phase 3+ product** | P2P-style profile→LoRA | Parametric voice beyond prompt ceiling |

---

## 7. Gap register — highest-value closes

| Priority | Gap | Memos | Action |
|----------|-----|-------|--------|
| **P0** | `stylometric_baseline.json` missing | #42, #53 | Genre-stratified p25/p75; unblock lexical_targets |
| **P0** | Dual-oracle benchmark | #50, #52, #55 | stylometry delta + surprisal/TSD on same sample |
| **P0** | Anti-detector not in detector feedback ladder | #46 | Multi-pass de-homogenization |
| **P1** | TSD second-half features | #55 | Extend `surprisal.py`; position-aware targets |
| **P1** | Biber register audit | #42, #53 | Optional `register.py`; 10-feature Rallapalli subset |
| **P1** | Voice-match vs anti-detector precedence in SKILL | #52 | Sequenced workflow + ESL callout |
| **P1** | Fix citations (23.5× → Jemama; Kalemaj → Paneru) | #41, #43 | SSOT sync |
| **P2** | SurpMark lite (frozen ref matrices) | #55 | ΔGJS telemetry |
| **P2** | ZeroStylus-lite rhetorical counters in StyleProfile | #48 | Document-level voice |
| **P2** | `--voice-floor-σ` for merged ESL path | #52 | max(sample_σ, 6) |
| **P3** | P2P/StyleTunedLM infer path | #47 | Parametric voice research spike |

---

## 8. Honest claims matrix

| Claim | Verdict |
|-------|---------|
| "Deterministic unslop defeats AI detectors" | **False** — TMR ~0.0–0.2 pp on fixtures |
| "Contraction pass alone evades detection" | **False** — necessary register restore, not bypass |
| "voice-match passes GPTZero" | **False** — Jemama, Catch Me, blader #2 |
| "Sounds like you = undetectable" | **False** — orthogonal axes |
| "Biber-matched = human to detectors" | **False** — Rallapalli AUC ~0.98; genre-conditional |
| "More few-shot samples fixes voice cloning" | **False** — Catch Me: 2→10 shots flat on blogs |
| "Anti-detector preserves your voice" | **Often false** — Liang native-enhancement diverges from idiolect |
| "Removes AI slop without changing code/URLs" | **True** — TestPreservation contract |
| "Helps ESL false positives (defensive)" | **Plausible** — anti-detector + burstiness; cite Liang; not misconduct |
| "Prompt voice-match = production cloning" | **False** — PEFT/TinyStyler path required |

---

## 9. Source index (memos #41–55)

| Agent | Topic | Key URL / anchor |
|-------|-------|------------------|
| #41 | Contraction stylometry | Paneru arXiv:2604.11687; `soul.py` |
| #42 | Rallapalli Biber / RLHF homogenization | arXiv:2604.14111 |
| #43 | Catch Me voice ceiling | arXiv:2509.14543 |
| #44 | Blandification / neutralization | arXiv:2603.18161 |
| #45 | Four-cue taxonomy | arXiv:2508.17573 |
| #46 | Alignment tax / HIP | arXiv:2603.24124; arXiv:2605.19516 |
| #47 | Profile-to-PEFT | arXiv:2510.16282; StyleTunedLM INLG 2024 |
| #48 | ZeroStylus document voice | arXiv:2505.07888 |
| #49 | Burstiness vs surprisal | Desaire 2023; DivEye arXiv:2509.18880 |
| #50 | Jemama fidelity ⊥ PPL | arXiv:2509.24930 |
| #51 | Ibrahim warmth–reliability | Nature 2026; arXiv:2507.21919 |
| #52 | Voice-match stylometric limits / ESL | Liang Patterns 2023 |
| #53 | Biber register conditioning | Yang & Carpuat arXiv:2505.00679 |
| #54 | Sentence-length variance restoration | `structural.py`; Desaire #8 |
| #55 | Surprisal dynamics beyond DivEye | TSD arXiv:2601.04833; SurpMark arXiv:2510.07500 |

---

## 10. Bottom line

**For detection:** Modern classifiers read a **stack** — lexical slop, syntactic flatness, Biber register homogenization, alignment-compressed semantics, and surprisal **trajectory** (especially late-stage settle and recovery transitions). Genre and ESL status modulate every threshold. No single stylometric feature survives as a silver bullet; SHAP interactions and ensemble heads dominate.

**For humanization:** unslop's shipped levers correctly target **cheap, auditable layers** (lexical subtraction, syntactic split, contraction restore, stance preservation). They fix voice quality and shallow tells. They do **not** exit the instruct-tuned statistical regime alone. Full defensive humanization adds cross-model passes, optional surprisal dynamics targeting, genre-conditioned baselines, and — when users need real idiolect — PEFT/hypernetwork voice paths outside prompt conditioning.

**Product doctrine:** Report **three axes** (slop removed, style delta, statistical naturalness). Keep voice-match and anti-detector separate. Subtract warmth, don't add it. Treat homogenization as weight-level; do not trust temperature or synonym swap. Lead with slop removal; put detector numbers in research appendices with TPR@FPR — never market "undetectable."

---

*Synthesis Agent #89 complete. Cross-refs: SYNTH-81–84 (detection), SYNTH-85–88 (evasion), UPDATE-PLAN-2026-08, `unslop/scripts/{humanize,structural,soul,stylometry,surprisal}.py`.*
