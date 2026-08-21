# SYNTH-90 — Voice-Match Strategy for unslop

**Synthesis Agent #90**  
**Date:** 2026-08-19  
**Inputs:** Agent memos #43 (Catch Me If You Can), #47 (Profile-to-PEFT), #48 (ZeroStylus), #52 (Voice-Match Stylometric Limits), #53 (Biber Register)  
**Scope:** Strategy for `/unslop voice-match`, `stylometry.py`, `style_memory.py`, and the extract-then-apply pipeline  
**Audience:** unslop maintainers, SKILL.md authors, benchmark CI, product framing  
**Code anchors:** `unslop/scripts/stylometry.py`, `unslop/scripts/style_memory.py`, `unslop/scripts/humanize.py` (`_build_voice_block`, `_format_voice_targets`), `skills/unslop/SKILL.md` §voice-match

---

## Executive summary

unslop voice-match is a **best-effort, numerically anchored prompt layer** for idiolect alignment. It is not authorship cloning, not detector evasion, and not document-level discourse transfer — unless future phases ship with honest benchmarks.

Five memos converge on a single architecture story:

| Layer | What it does | unslop status | Evidence |
|-------|--------------|---------------|----------|
| **Micro stylometry** | Sentence σ/cv, contractions, punctuation tics, TTR, Latinate ratio | **Shipped** — `stylometry.py` (19 fields) + `style_memory.py` | Catch Me style model; Paneru contractions |
| **Register / Biber** | Nominalizations, that-subj, participials, involvement dimensions | **Partial proxies** — latinate ratio, contractions; no clausal features | Yang & Carpuat RG 2025; Reinhart/Rallapalli 2025–2026 |
| **Macro discourse** | Paragraph templates, argument flow, long-doc consistency | **Not implemented** | ZeroStylus Γ_p (Phase 9 blueprint) |
| **Parametric voice** | Profile → LoRA weights in model | **Not implemented** | StyleTunedLM 87.9% vs 69.3% 5-shot; P2P 0.57 s/user |
| **Evaluation oracle** | AA/AV/style-model/GPTZero battery | **Not integrated** | Catch Me harness (Blog AV ~19% vs human 91.4%) |

**Two-axis doctrine (Agent #52):** Voice-match optimizes *"does this read like the user's sample?"* Anti-detector optimizes *"does this escape classifier basins?"* Jemama (2025) proved these diverge: 99.9% style-matching agreement coexists with perplexity 15.2 vs human 29.5. For ESL users, faithful voice-match can **increase** detector false-positive risk (Liang 2023) because L2 formal English occupies the same low-σ, low-perplexity neighborhood as AI output.

**Strategic verdict:** Keep voice-match as Phase 1–2 (extract → persist → prompt). Extend upward with Biber eval/conditioning (Tier 1–3) and ZeroStylus-inspired discourse counters (Tier 2). Treat P2P/StyleTunedLM as Phase 3+ parametric upgrade. Close the eval gap with Catch Me's AV harness before any "sounds like me" product claim on informal writing.

---

## 1. What voice-match is for (and what it is not)

### 1.1 Legitimate goals

1. **Idiolect restoration** — User drafted with AI; slop removal pulled cadence toward RLHF mean. Voice-match pulls back toward *their* measured profile.
2. **Professional consistency** — Emails, cover letters, internal docs where the reader knows prior tone.
3. **Anti-blandification** — Counterweight to LLM homogenization (arXiv 2603.18161; Biber D5 information-density attractor).
4. **Cross-session anchor** — `style_memory.json` + hook re-reinforcement at turn 8/16 (HorizonBench drift).
5. **Human-reader alignment** — "Don't sound like ChatGPT to my manager" without claiming Turnitin clearance.

### 1.2 Explicit non-goals

| Do not claim | Why |
|--------------|-----|
| Stylometric-attribution-resistant output | Catch Me Blog AV ~17–21% vs human 91.4% |
| GPTZero / Turnitin pass from voice-match alone | Jemama separability; Catch Me GPT-4o ≈ 0% human on blogs |
| Blog/forum idiolect cloning from 5 samples | Wang: 2→10 shots flat; informal domain systematic failure |
| "Fine-tuning wins decisively" without citation split | Wang excludes PEFT; StyleTunedLM/TinyStyler prove PEFT path |
| More samples fixes the gap | Catch Me: diminishing returns 2→10 shots |
| Biber distance = human | Rallapalli AUC ~0.98 on Biber features alone |

### 1.3 Citation fix (P1 — SSOT `skills/unslop/SKILL.md`)

Current Known Limitation misattributes **23.5×** few-shot gain to Catch Me If You Can. Correct split:

- **Wang et al. (EMNLP 2025, arXiv 2509.14543)** — prompt-only ceiling; Blog AV ~2.4× gain 0-shot→5-shot, not 23.5×
- **Jemama et al. (UEMCON 2025, arXiv 2509.24930)** — 23.5× style-matching; 99.9% completion; perplexity/style split
- **Liu StyleTunedLM (INLG 2024)** — PEFT authorship classifier 87.9% vs 69.3% 5-shot
- **Tan P2P (ACL 2026)** — scalable profile→LoRA deployment (0.57 s/user vs OPPU 20.44 s)
- **TinyStyler (EMNLP 2024)** — 800M + authorship embeddings beats GPT-4 on transfer

Replace "Fine-tuning wins decisively" with: *"Specialized adaptation (StyleTunedLM, TinyStyler, P2P) beats prompting on authorship metrics; Catch Me If You Can shows prompt-only fails on informal personal style."*

---

## 2. Current architecture (Phase 1–2 — shipped)

### 2.1 Extract-then-apply pipeline

```
User sample (≥50 words) or persisted profile
        │
        ▼
  stylometry.analyze() → StyleProfile (19 numeric fields)
        │
        ├─► style_memory.save_profile() → ~/.config/unslop/style-memory.json
        │   (numeric-only, mode 0600, closed schema, 64 KB cap)
        │
        ▼
  humanize._format_voice_targets() → LLM prompt block
        │
        ▼
  Single-pass LLM rewrite (prompt-bound)
        │
        ▼
  Optional: StyleProfile.delta(sample, rewrite) → format_delta() feedback
```

**Design choices already correct:**

- **Measurement before generation** — Same architecture as Catch Me's style model (LIWC/WritePrint family) and TinyStyler extract-then-apply.
- **Numeric-only memory** — Avoids CHI 2026 sycophancy amplification from free-text preference strings; OWASP agentic memory poisoning defense.
- **No LM in default path** — Deterministic, auditable, offline-capable.
- **DivEye proxies** — `sentence_length_cv`, `word_length_stdev` as cheap burstiness/surprisal-variance surrogates (full DivEye requires `--surprisal-variance` opt-in).

**Known gap:** Wang evaluates whether output matches author centroids. unslop feeds numeric deltas **into** the prompt but never **closes the loop** with AA/AV verification.

### 2.2 StyleProfile field map

| Field group | Fields | Voice-match role | Anti-detector tension |
|-------------|--------|------------------|----------------------|
| Cadence | `sentence_length_mean/stdev/cv`, `fragment_rate`, `starts_with_and_but` | Primary cadence targets | Anti-detector may raise σ above sample |
| Lexical | `type_token_ratio`, `function_word_rate`, `latinate_ratio` | Register anchor | Anti-detector may Anglo-Saxon-ize |
| Punctuation | `em_dash/semicolon/colon/parenthetical_rate` | Idiolect tics | Sample overrides global cap (document in SKILL.md) |
| Persona | `first/second_person_rate`, `contraction_rate` | Involvement (Biber D1) | Paneru: AI ~0 contractions in its corpus; a user sample may also have 0 |
| Proxies | `word_length_stdev`, `passive_voice_approx` | DivEye/surprisal rhythm | Not in default detector axis |

### 2.3 Mode boundaries

| Mode | Optimizes | Voice-match interaction |
|------|-----------|-------------------------|
| subtle / balanced / full | Generic anti-slop | **Increases distance** from specific author (RLHF regression to mean) |
| **voice-match** | Stylometric fidelity to sample | Core mode |
| anti-detector | Classifier escape (σ ≥ 6, contractions, surprisal) | **Conflicts** with low-σ ESL samples — see §5 |

Voice-match is **LLM-mode only** today (`voice_sample` / `voice_profile` ignored in deterministic pass). Hooks activate `/unslop voice-match` at session level; CLI uses `--voice-sample` and auto-loads `style_memory.json`.

---

## 3. Research synthesis — five memos

### 3.1 Agent #43 — Catch Me If You Can (prompt ceiling)

**Verdict:** Largest peer-reviewed measurement of frontier LLM implicit-style imitation. Prompt-only **partially works** in structured genres (news AV ~95%, email ~96%) and **fails** on informal blogs (AV ~17–21% vs human 91.4%).

**Implications for unslop:**

- voice-match strongest on **email/docs**; weakest on **casual blog/social**
- Authorship match ≠ GPTZero pass (GPT-4o ≈ 0% human on blogs despite partial AA)
- +Snippet (author prefix seeding) and completion prompting (Jemama) are future flags, not shipped
- **P2 eval:** Adapt `deploy_AV_models.py` on unslop before/after Blog pairs

### 3.2 Agent #47 — Profile-to-PEFT (Phase 3+ parametric path)

**Verdict:** P2P maps NL profile → LoRA via hypernetwork in 0.57 s/user (33× vs OPPU). StyleTunedLM proves **voice objective** with PEFT (87.9% authorship classifier). P2P proves **deployment pattern** but uses preference tasks, not Catch Me's AA/AV battery.

**Phase roadmap:**

| Phase | Deliverable | Dependency |
|-------|-------------|------------|
| **1–2 (now)** | Prompt + numeric profile | Shipped |
| **2 (eval)** | Catch Me AV harness on unslop output | Wang repo + Blog subset |
| **3a (prototype)** | Single-user StyleTunedLM-style LoRA (qlora, local) | User consent, ~5k–10k words |
| **3b (scaled)** | Hypernetwork: NL summary + `StyleProfile` → LoRA | Offline training on multi-author corpus |
| **4 (product)** | Infer-only weights OR "bring your own LoRA" | One base model or documented external path |

**Input modality recommendation:** Hybrid — NL summary from samples (P2P ablation: summary dominates) + numeric `StyleProfile` side-channel for cues NL misses (contraction rate, σ).

### 3.3 Agent #48 — ZeroStylus (macro discourse layer)

**Verdict:** Document-level style transfer via sentence templates Γ_s + paragraph templates Γ_p. Modest absolute gain (+0.20 tri-axial) but solves **style drift on long inputs** — the problem unslop hits when micro-signals hold locally but discourse structure wanders.

**Layer stack:**

```
Document  (ZeroStylus Γ_p — discourse templates)     NOT IMPLEMENTED
Paragraph (structural.py — sentence σ, bullet merge)  PARTIAL
Sentence  (humanize.py — slop regex, em-dash cap)     SHIPPED
Token     (surprisal.py — DivEye proxies)             OPT-IN
```

**Tier 2 shortcut (no ZeroStylus reimplementation):** From `--voice-sample`, count rhetorical move frequencies (opener types, "However"/"We show" patterns) as closed-schema numeric fields in `style_memory.json` v2 — ~30% of Γ_s value at deterministic cost.

**Tier 3 (opt-in `--document-voice`):** Full template-guided chunked rewrite under voice-match, not default slop removal. 500 KB file cap limits reference corpus size.

### 3.4 Agent #52 — Two-axis limits (voice vs detector)

**Verdict:** Keep modes separate. Document conflict in SKILL.md. ESL false positives require **anti-detector**, not voice-match alone.

**Sequenced workflow (recommended, not yet single command):**

1. `analyze(user_sample)` + optional `analyze(draft)` baseline
2. **voice-match rewrite** — slop removal + register/cadence match
3. `StyleProfile.delta()` — if fidelity win, stop
4. **If user opts into detector defense** — anti-detector with **constrained bands**: `σ ≥ max(sample_σ, 6)`, contractions ≥ max(sample rate, human floor), preserve Latinate ±ε and first-person rate
5. Cross-model second pass (TempParaphraser / Adversarial Paraphrasing)
6. Re-measure: stylometric delta **and** detector probability if `--detector-feedback`

**ESL framing:** Liang 2023 — 61.3% FP on TOEFL essays; "enhance to native speaker" cuts FP to 11.6% by **destroying** original stylometric profile. Cite as anti-detector mitigation, never as voice-match.

### 3.5 Agent #53 — Biber register (auditable conditioning layer)

**Verdict:** Biber MDA closes the loop between subtraction (remove AI tells → f14/f27/f29 overuse) and voice-match (steer toward target register, not vibes checklist). Yang & Carpuat RG prompting improves **meaning preservation** during style transfer — critical for humanizers.

**AI fingerprint (Reinhart/Rallapalli):** Instruction-tuned LLMs overuse nominalizations (1.5–2×), present participials (2–5×), that-clauses-as-subject; underuse wh-relatives, discourse particles. Chat models **cluster together in Biber space** — RLHF homogenization, not vendor quirk.

**Contradiction to surface heuristics:** Aggregate benchmarks show LLM **contraction overuse** (f59); unslop `soul.py` often **adds** contractions. Resolution: **target-profile-relative steering**, not global "human mean."

---

## 4. Integrated voice-match strategy

### 4.1 Three-tier voice fidelity model

| Tier | Name | Mechanism | Target use case | Fidelity ceiling |
|------|------|-----------|-----------------|------------------|
| **T1** | Micro prompt-match | `StyleProfile` → LLM targets | Email, docs, short posts | Structured genres OK; Blog AV ~20% |
| **T2** | Register-aware match | T1 + Biber fingerprint delta + RG-style prompt | Academic/professional prose | Better meaning preservation; auditable |
| **T3** | Document-consistent match | T2 + discourse templates (ZeroStylus-inspired) | Essays, long memos, chapters | Reduces long-doc drift |
| **T4** | Parametric match | LoRA / hypernetwork (StyleTunedLM / P2P) | Production voice cloning | StyleTunedLM 87.9% classifier; not in plugin |

unslop ships **T1**. Roadmap targets **T2 eval → T2 prompt → T3 opt-in → T4 research**.

### 4.2 Apply order (generation procedure)

From SKILL.md six-signal checklist, unified with memo evidence:

1. **Register** — Latinate ratio, TTR, Biber D1/D5 (involvement vs information density). Match sample, not "human average."
2. **Cadence** — Sentence-length μ/σ/cv, fragment rate, And/But openers.
3. **Punctuation** — Em-dash, semicolon, parenthetical rates; sample overrides default em-dash cap when higher.
4. **Vocabulary touches** — Favorite phrases / rhetorical moves (LLM layer; future: Tier 2 closed-schema counters).
5. **Forbidden patterns** — What sample never does (LLM layer only; do not persist as free text in memory).
6. **Post-rewrite verify** — `StyleProfile.delta()` + optional Biber delta + optional AV score.

Do not invent biographical detail for named public voices.

### 4.3 Sample requirements

| Words | Behavior |
|-------|----------|
| <50 | `style_memory.save_profile()` rejects; `_build_voice_block` warns "rough tone guidance only" |
| 50–200 | Usable but high variance on σ, contraction_rate |
| 200–500 | Cold-start norm (Cat 10 synthesis) |
| 500+ | Stable idiolect signals; preferred for memory commit |
| Multi-doc reference | Future Tier 3; single sample today |

Warn when sample is AI-polished (encodes detectable stylometrics, not user idiolect).

---

## 5. Voice-match vs anti-detector — merge policy

### 5.1 Conflict matrix

| Sample property | voice-match | anti-detector |
|-----------------|-------------|---------------|
| σ = 3.5 (flat ESL academic) | Match σ 3.5 | Raise to σ ≥ 6 |
| contraction_rate = 5/1k | Match 5/1k | Inject toward ~170/1k scale |
| Low TTR, high Latinate | Match register | Fragments, Anglo-Saxon chunks |
| No em-dashes | Match 0/1k | May add for burstiness (cap 2/para) |

### 5.2 Recommended user guidance

| User goal | Mode |
|-----------|------|
| "Sound like my old emails" | voice-match + sample |
| "GPTZero flagged my human essay" | anti-detector (+ cross-model) |
| "AI draft → my voice, not flagged" | **Sequenced:** voice-match → optional anti-detector with register anchors |
| "Beat Turnitin for AI essay" | **Decline** (Boundaries) |

### 5.3 Future CLI flags

- `--voice-floor-σ` — `max(sample_σ, floor)` for merged ESL defense
- `--voice-seed-snippet` — Jemama/Catch Me +Snippet analog (author prefix continuation)
- `--document-voice` — Tier 3 ZeroStylus-inspired chunked rewrite

---

## 6. Implementation roadmap

### Phase A — Documentation & honesty (P0, now)

| Action | Owner | Memo |
|--------|-------|------|
| Fix 23.5× citation misattribution in SSOT `skills/unslop/SKILL.md` | Docs | #43 |
| Add "Voice-match vs anti-detector" subsection with Jemama two-axis paragraph | Docs | #52 |
| ESL callout linking Liang 2023; voice-match ≠ detector clearance | Docs | #52, #78 |
| Genre caveat: strongest email/docs, weakest informal blog | Docs | #43 |
| Sample em-dash override rule in SKILL.md | Docs | #52 |
| Add P2P + StyleTunedLM one-liner to Known Limitation | Docs | #47 |

### Phase B — Measurement extensions (P1)

| Action | Module | Memo |
|--------|--------|------|
| Optional `--biber-profile` eval (NeuroBiber/BiberPlus fingerprint delta) | `stylometry.py` or sibling | #53 |
| StyleProfile v2 optional rhetorical-move counters (closed schema) | `style_memory.py` v2 | #48 |
| `format_delta()` UX: warn when rewrite σ exceeds sample in voice-match-only | `stylometry.py` | #52 |
| Map f14/f27/f29 overuse to deterministic hints in LLM mode | `humanize.py` | #53 |
| RG-style register prompt block in `--mode llm` voice-match | `humanize.py` | #53 |

**Biber integration tiers (from #53):**

- **Tier 1 (eval):** `--biber-profile` reports per-feature delta; flag nominalization > 1.3× target
- **Tier 2 (deterministic hints):** Split stacked participials; that-subj opener diversification
- **Tier 3 (LLM conditioning):** Inject structured Biber register analysis before rewrite
- **Tier 4 (guardrail):** Never market Biber delta as detector evasion score

Keep opt-in: `pip install unslop[biber]` (torch/spaCy tier, same as DivEye).

### Phase C — Evaluation harness (P1)

| Action | Deliverable | Memo |
|--------|-------------|------|
| Wrapper: Catch Me `deploy_AV_models.py` on unslop before/after | `benchmarks/voice_match_bench.py` | #43 |
| Log `StyleProfile.delta()` alongside AV score | Telemetry | #43, #47 |
| Two-axis dashboard: style fidelity vs perplexity/burstiness | Benchmark report | #52 |
| Conflict test suite: samples with σ ∈ {3, 5, 8, 12} | Tests | #52 |
| Long-doc fixtures: style Δ + content keyword recall | Benchmark | #48 |
| Liang TOEFL slice (stylometric movement, not Turnitin API) | Research fixture | #52 |

**Honest benchmark targets (informal Blog):**

| Metric | Prompt-only LLM (Catch Me) | voice-match aspiration | Human ceiling |
|--------|---------------------------|------------------------|---------------|
| Blog AV | ~17–21% | Measure movement, not claim pass | 91.4% |
| GPTZero % human (GPT-4o, blogs) | ~0.47% | Do not optimize in voice-match | — |
| StyleTunedLM BERT classifier | — | Phase 3+ target ~88% | — |

### Phase D — Macro & parametric voice (P2–P3, research)

| Action | Phase | Memo |
|--------|-------|------|
| Rhetorical-move extraction from reference corpus | Tier 2 | #48 |
| Chunked template-guided rewrite (`--document-voice`) | Tier 3 | #48 |
| `--voice-seed-snippet` completion-style seeding | Tier 2 | #43, Jemama |
| Single-user StyleTunedLM qlora prototype | Phase 3a | #47 |
| Hypernetwork stylometric profile → LoRA | Phase 3b | #47 |
| Infer-only P2P checkpoint eval on Personal Reddit (research) | Phase 3 | #47 |

**Product boundaries for Phase D:**

- Never auto-train on user data without explicit consent
- Ephemeral LoRA in memory; optional encrypted cache (LoRA ≈ compressed profile)
- Anti-detector remains separate; no implied Turnitin evasion from voice LoRA
- Ship infer-only OR document external LoRA path

---

## 7. Architecture diagram (target state)

```
                    ┌─────────────────────────────────────┐
                    │         User writing samples         │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
   stylometry.analyze()      optional BiberPlus/          optional discourse
   → StyleProfile (T1)       NeuroBiber fingerprint        move counters (T2)
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      ▼
                         style_memory.save_profile()
                         (numeric-only, v1 → v2 schema)
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
           _format_voice_targets()              optional RG register
           + SKILL.md six-signal                  prompt block (T2)
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      ▼
                         LLM rewrite (voice-match intensity)
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
           StyleProfile.delta()                  optional Catch Me AV
           (+ Biber delta T2)                    (+ GPTZero axis, research)
                    │
                    ▼
           User feedback / benchmark CI

   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Phase 3+ (not shipped) ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                                      │
                         Hypernetwork / per-user LoRA (T4)
                                      ▼
                         Rewrite with plugged adapter
```

---

## 8. Claims matrix for README / SKILL.md

| Claim | Allowed? | Wording |
|-------|----------|---------|
| "Match register, cadence, punctuation tics" | Yes | Best-effort; structured genres stronger |
| "Numerically anchored to your sample" | Yes | 19-field StyleProfile |
| "Persists voice across sessions" | Yes | style_memory.json; re-verify with fresh analyze() |
| "Sounds exactly like you" | No | Blog AV ~20% prompt ceiling |
| "Passes AI detectors" | No | Use anti-detector; cite Jemama |
| "23.5× better with samples" | Fix citation | Jemama, not Catch Me |
| "Fine-tuning wins" | Qualify | StyleTunedLM/TinyStyler/P2P — not shipped |
| "Document-level consistency" | Not yet | ZeroStylus blueprint; track for Tier 3 |
| "Biber-verified register match" | After Tier 1 eval ships | With `--biber-profile` only |

---

## 9. Key numbers cheat sheet

| Metric | Value | Source | Memo |
|--------|-------|--------|------|
| Catch Me human Blog AV | 91.4% | Wang EMNLP 2025 | #43 |
| Catch Me 5-shot LLM Blog AV | ~17–21% | Wang EMNLP 2025 | #43 |
| Few-shot gain Blog AV (0→5 shot) | ~2.4× | Wang EMNLP 2025 | #43 |
| Jemama few-shot style gain | up to 23.5× | Jemama UEMCON 2025 | #52 |
| Jemama completion style match | 99.9% | Jemama 2025 | #52 |
| Human vs matched LLM perplexity | 29.5 vs 15.2 | Jemama 2025 | #52 |
| StyleTunedLM authorship classifier | 87.9% | Liu INLG 2024 | #47 |
| 5-shot authorship classifier | 69.3% | Liu INLG 2024 | #47 |
| P2P deployment time | 0.57 s/user | Tan ACL 2026 | #47 |
| ZeroStylus tri-axial gain | +0.20 vs DirectPrompt | Wu & Deng 2025 | #48 |
| Liang TOEFL FP rate | 61.3% | Liang Patterns 2023 | #52 |
| Liang "native enhance" FP drop | 61.3% → 11.6% | Liang 2023 | #52 |
| Rallapalli Biber RF AUC | ~0.98 | Rallapalli 2026 | #53 |
| unslop StyleProfile fields | 19 | stylometry.py | — |
| style_memory minimum sample | 50 words | style_memory.py | — |
| Recommended cold-start sample | 200–500 words | Cat 10 synthesis | #52 |

---

## 10. Bottom line

Voice-match is unslop's **preserve-stance** mode: subtract AI-slop without regressing to generic "humanized" baseline, anchored to measured idiolect rather than vibes. The five input memos agree on the ceiling (Catch Me informal failure), the upgrade path (StyleTunedLM → P2P parametric voice), the missing macro layer (ZeroStylus discourse templates), the product boundary (voice ≠ detector — Agent #52), and the auditable middle layer (Biber register — Agent #53).

**Ship today:** T1 micro stylometry + numeric memory + honest docs.  
**Measure next:** Catch Me AV harness + two-axis benchmark + optional Biber delta.  
**Build later:** Register prompting, discourse counters, document-voice, parametric LoRA — each gated on eval, not marketing.

Prompt-based voice-match with numeric anchors is **valuable for human readers**, **insufficient for stylometric attribution**, and **orthogonal to ESL false-positive defense** unless anti-detector constraints are applied as a documented second pass.

---

## References

| Memo | File |
|------|------|
| Agent #43 | `AGENT-43-CATCH-ME-IF-YOU-CAN.md` |
| Agent #47 | `AGENT-47-PROFILE-TO-PEFT.md` |
| Agent #48 | `AGENT-48-ZEROSTYLUS.md` |
| Agent #52 | `AGENT-52-VOICE-MATCH-STYLOMETRIC-LIMITS.md` |
| Agent #53 | `AGENT-53-BIBER-REGISTER.md` |

| Code | Path |
|------|------|
| Stylometry | `unslop/scripts/stylometry.py` |
| Style memory | `unslop/scripts/style_memory.py` |
| Voice prompt | `unslop/scripts/humanize.py` |
| Voice-match spec | `skills/unslop/SKILL.md` §voice-match |

| External (canonical) | URL |
|---------------------|-----|
| Catch Me If You Can | https://arxiv.org/abs/2509.14543 |
| Jemama style vs detectability | https://arxiv.org/abs/2509.24930 |
| Profile-to-PEFT | https://arxiv.org/abs/2510.16282 |
| StyleTunedLM | https://arxiv.org/abs/2409.04574 |
| ZeroStylus | https://arxiv.org/abs/2505.07888 |
| Yang & Carpuat register transfer | https://arxiv.org/abs/2505.00679 |
| Liang ESL detector bias | https://arxiv.org/abs/2304.02819 |
| Rallapalli Biber × RAID | https://arxiv.org/abs/2604.14111 |

---

*~2,400 words (body excluding tables). Synthesis Agent #90.*
