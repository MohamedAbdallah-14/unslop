# Agent #41 — Contraction-Rate Stylometry for AI Text Detection

**Topic:** Contraction frequency as a stylometric fingerprint; unslop Phase 5 (`soul.py`) integration  
**Primary empirical source:** Paneru (2026), *Please Make it Sound like Human* — arXiv:2604.11687  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

Contraction rate is one of the cleanest **single-feature** gaps between default LLM prose and human reference text in recent stylometric work. On Paneru's 25,140-pair AI↔human corpus, AI inputs average **0.00 contractions per chunk**; human references average **0.17 per chunk** — labeled "Very Strong" signal strength in Table 1, stronger than lexical diversity or comma density on that dataset.

**Citation correction (critical):** unslop internal docs and several SSOT mirrors still say **"Kalemaj et al. 2026"** and link arXiv:2604.11687. That ID resolves to **Utsav Paneru** (Kathmandu Engineering College), not anyone named Kalemaj. No published AI-detection paper by a Kalemaj author on contraction stylometry was found. Iden Kalemaj (Meta, differential privacy) and Ilir Kalemaj (political science) are unrelated. unslop already removed the broken citation from `validate.py` / `soul.py` per CHANGELOG; **`skills/unslop/SKILL.md` and mirrors still carry "Kalemaj et al."** and should be updated to Paneru (2026) or a neutral "empirical baseline, pending re-verification" note.

**unslop verdict:** Contraction injection in `soul.py` is **architecturally correct** — it targets a real distributional tell that lexical-only scrubbing cannot fix. It is **not sufficient** for detector evasion. unslop's own TMR benchmark shows deterministic passes including soul move RAID-grade scores by **0.0–0.2 percentage points** while `p_ai` stays above 0.98. Contraction lift is item **#4** in the anti-detector lever ordering (after cross-model paraphrase, burstiness, and user-specific specificity). Treat it as register restoration and ESL false-positive defense, not a bypass.

---

## Primary sources (full URLs)

| Resource | URL | Role |
|----------|-----|------|
| **Paneru — AI-to-human style transfer (contraction gap Table 1)** | https://arxiv.org/abs/2604.11687 | Canonical 0.00 vs 0.17/chunk finding |
| **Paneru — HTML v1** | https://arxiv.org/html/2604.11687v1 | Full marker-shift / overshoot analysis |
| **Paneru — PDF** | https://arxiv.org/pdf/2604.11687 | Same paper |
| **HuggingFace Papers page** | https://huggingface.co/papers/2604.11687 | Community indexing |
| **Rallapalli et al. — Biber stylometry across genres/models** | https://arxiv.org/abs/2604.14111 | Genre > model for stylistic features |
| **"Detecting the Machine" — XGBoost stylometric hybrid** | https://arxiv.org/pdf/2603.17522 | `contraction ratio` in 22-feature set; AUROC 0.9996 in-distribution |
| **StyloAI — ContractionCount feature** | https://arxiv.org/pdf/2405.10129 | RF classifier; 81–98% accuracy on multi-domain sets |
| **Beyond "AI Language" — idiolect / contraction variance** | https://arxiv.org/abs/2608.06589 | Model-level contraction profiles diverge wildly (120–30,000 per million words) |
| **Can Humans Detect AI? — contraction as judge heuristic** | https://arxiv.org/abs/2604.23471 | Humans use contractions as "human" cue; feature overlap between groups |
| **Human heuristics for AI language are flawed** | https://par.nsf.gov/biblio/10463192-human-heuristics-ai-generated-language-flawed | Jakesch et al.; contractions associated with "human" in self-presentation |
| **Liang et al. — GPT detector ESL bias** | https://arxiv.org/abs/2304.02819 | Formal/no-contraction ESL prose shares AI perplexity profile |
| **Sadasivan et al. — detection impossibility under paraphrase** | https://arxiv.org/abs/2305.18226 | TV bound; surface feature patching is bounded |
| **Adversarial Paraphrasing (NeurIPS 2025)** | https://arxiv.org/abs/2506.07001 | Simple paraphrase *increases* detector TPR; structural signal survives |
| **TMR detector (unslop benchmark model)** | https://huggingface.co/Oxidane/tmr-ai-text-detector | 99.28% AUROC on RAID; unslop fixture scores barely move |
| **RAID benchmark** | https://raid-bench.xyz/leaderboard | Stress test for detector / humanizer claims |
| **TH-Bench humanization eval** | https://arxiv.org/abs/2503.08708 | No attack wins all axes |

---

## Mechanism: why contractions matter

### What is being measured

Stylometric contraction rate counts apostrophe-bound clitics (`don't`, `it's`, `we're`, etc.) normalized by text length. Paneru measures **contractions per chunk** (~50 words). unslop measures **contractions per 1,000 prose words** in `stylometry.py` and `validate.py`. Same family of signal, different units — do not conflate without conversion.

Paneru's corpus construction makes the AI side artificially contraction-free: the generation prompt explicitly instructs models to adopt "formal, structured AI-like phrasing and **avoiding contractions**, slang, and casual expressions." The 0.00 AI average is therefore partly **prompt-engineered** — but it matches what default ChatGPT/Claude assistant register produces in the wild without anti-slop instructions.

### Why detectors (and humans) read it

1. **Token distribution.** RoBERTa-family detectors (TMR, Desklib, Turnitin backends) ingest subword n-grams. Full forms (`do not`, `it is`, `will not`) vs contractions (`don't`, `it's`, `won't`) shift byte-level and BPE token sequences. Phase 3 unslop benchmark commentary in `soul.py` states the core issue: stripping lexical AI-isms moves TMR by ~0 pp because detectors read **distributional fingerprint**, not the offensive vocabulary list.

2. **Register coupling.** Contractions correlate with lower Flesch-Kincaid grade (Paneru: human 11.5 vs AI 17.8), shorter mean word length, and higher sentence-length variance. Contraction rate is not independent — it sits in a bundle of informal-human markers. Fixing one axis without burstiness or specificity leaves the rest.

3. **Human prior.** Jakesch et al. (PNAS Nexus) show lay judges associate first-person pronouns and **contractions** with human-written self-presentation — and that this heuristic is **gameable** ("more human than human"). The 2026 arXiv:2604.23471 study finds judges pick "human" more often when warned about detection, even when stylometric features (including contraction rate) **do not differ** between groups. Contractions affect **perceived** humanness more reliably than **classifier** scores.

### The overshoot problem (Paneru's second lesson)

Paneru introduces **marker shift magnitude vs. shift accuracy**. Mistral-7B QLoRA achieves high aggregate shift but **overshoots** human targets: contraction rate reaches **0.383/chunk** vs human **0.17** — more than double. Five of eleven markers hit the max overshoot cap (2.0). Naive contraction stuffing produces a new tell: uniform, aggressive colloquialization. unslop's `preserve_first_sentence=True` in `contract_copula()` directly addresses this — Phase 6 perceived-humanness benchmark found uniform 100% contraction reads as "single find-replace pass" to a sophisticated judge.

---

## Benchmarks and numbers

### Paneru (arXiv:2604.11687) — chunk-level markers (n=1,390 test)

| Metric | Human | AI | Signal strength |
|--------|-------|-----|-----------------|
| Contractions/chunk | **0.17** | **0.00** | Very Strong |
| Sentence length variance | 37.1 | 18.4 | Strong |
| Flesch-Kincaid grade | 11.5 | 17.8 | Very Strong |
| Lexical diversity | 0.783 | 0.853 | Moderate |

Style-transfer results: BART-large BERTScore F1 **0.924**, ROUGE-L **0.566**, chrF++ **55.92** — beats Mistral-7B on reference similarity despite 17× fewer parameters. Mistral overshoots contraction target.

**Unit note for unslop:** 0.17 contractions ÷ ~51 words/chunk ≈ **3.3 contractions per 1k words** on Paneru's corpus. unslop's validator warns below human baseline at **~17 per 1k words** — roughly **5× higher**. That 17/1k figure may come from a different corpus or a broader contraction regex (including possessives in some community tools). **Reconciliation needed** before treating 17/1k as Paneru-derived.

### "Detecting the Machine" (arXiv:2603.17522)

22 hand-crafted features include **`contraction ratio`** alongside burstiness, hedging density, and sentence-length entropy. XGBoost stylometric hybrid hits **AUROC 0.9996** in-distribution on HC3 — matching fine-tuned RoBERTa — with interpretable features. Cross-domain (ELI5 ↔ HC3) still degrades (e.g. 0.904 vs 0.634 for classical RF). Contraction ratio is **one feature among many**, not the top SHAP driver; sentence-level perplexity CV and AI-phrase density rank higher in extended sets.

### StyloAI (arXiv:2405.10129)

**ContractionCount** listed under syntactic complexity (31 features). Random Forest: **81%** accuracy on AuTexTification, **98%** on Education dataset. Top discriminators were lexical diversity metrics, not contractions alone — consistent with "bundle of tells" framing.

### Idiolect paper (arXiv:2608.06589)

Contradicts a universal "AI = zero contractions" rule. Within 2026 model cohort, contraction frequency ranges **1,200–30,000 per million words** depending on model. GPT-3.5 ≈ **120/million**; Claude-Haiku-4-5 ≈ **30,000/million**. Negation contractions (`'t`) show ~**32:1** generational shift (2024 vs 2026 cohort means). **Model idiolect dominates a single global contraction threshold.**

### unslop internal (TMR on fixtures)

README and `soul.py` header: deterministic lexical + structural + soul moves TMR **`p_ai` by 0.0–0.2 pp** on four AI fixtures. Soul is necessary for voice; insufficient for TMR evasion. Coherent with Adversarial Paraphrasing finding that shallow rewriting can **worsen** detector scores.

---

## Supporters, critics, and fault lines

### Supporters (contraction rate is a real signal)

| Actor | Position | Evidence |
|-------|----------|----------|
| **Paneru (2026)** | Strongest single marker on 11-feature analysis | 0.00 vs 0.17/chunk |
| **StyloAI authors** | ContractionCount in production stylometry stack | Multi-domain RF gains |
| **"Detecting the Machine" authors** | Contraction ratio in interpretable hybrid | Near-perfect in-distribution AUROC |
| **Jakesch et al.** | Humans use contraction presence as authorship heuristic | Manipulable but real |
| **unslop `soul.py` design** | Deterministic injection after subtractive passes | Safe, preservation-tested |
| **ESL-advocacy / anti-detector community** | Adding contractions + burstiness helps formal L2 writers flagged as AI | Liang TOEFL 61% FP; formulaic L2 ≈ low perplexity |

### Critics and caveats (contraction rate is fragile or misleading)

| Actor | Position | Evidence |
|-------|----------|----------|
| **Paneru (same paper)** | Blind contraction lift overshoots; wrong-direction markers possible | Mistral 0.383 vs target 0.17 |
| **Idiolect authors (2026)** | Contraction frequency is model-specific, not "AI vs human" | 120 vs 30,000/million within LLMs |
| **Rallapalli et al. (2604.14111)** | **Genre > model > decoding** for Biber features | Prompting cannot nudge LLM style much |
| **arXiv:2604.23471** | Stylometric contraction rate **does not separate** human-AI-assisted groups | Judges still prefer "warned" group |
| **Liang et al. (2023)** | ESL formal prose = low perplexity = AI flag; contractions help but don't fix root bias | 61.22% TOEFL misclassified |
| **Sadasivan et al.** | Paraphrase drives TV toward human; single-feature arms race bounded | Recursive paraphrase breaks detectors |
| **AdvPara (NeurIPS 2025)** | Lexical/surface rewrite insufficient; can backfire | +15% TPR on Fast-DetectGPT for naive paraphrase |
| **TMR / RAID-grade encoders** | Token-sequence models absorb surface edits | unslop 0.0–0.2 pp movement |

**Synthesis:** Contraction rate is a **high-precision register marker** for *default-assistant* LLM text and a **low-precision detector feature** in isolation — genre, model vintage, and prompt design collapse the binary gap. It remains valuable for **humanization quality** and **false-positive defense** when applied conservatively.

---

## Community and tooling landscape

- **HuggingFace Papers** indexes 2604.11687 with the contraction finding in the abstract snippet — primary discovery path for practitioners.
- **Stylometry feature libraries:** TextDescriptives (NEULIF, arXiv:2511.21744), StyloMetrix (Argasiński et al., ESWA 2025), StyloAI's 31-feature set — contractions appear in syntactic/discourse buckets, rarely as sole classifier input.
- **Commercial detectors** (GPTZero, Turnitin, Originality) do not publish contraction-specific weights; behavior is proprietary. Turnitin's 2025–2026 "AI bypasser" models explicitly target **humanizer output patterns**, which may include mechanical contraction density.
- **Humanizer tier lists** (DAMAGE audit, blader/humanizer) treat contraction injection as **Tier 1** surface edit — same tier as stock-vocab scrubbing. Research tier humanizers (DIPPER, AdvPara, GradEscape) operate at discourse/surprisal layers where contraction rate is emergent, not regex-injected.
- **Forensic linguistics / authorship attribution** tradition treats contractions as author-specific (expand vs retain in preprocessing affects PAN shared-task systems, arXiv:2401.06752) — opposite direction from AI detection (inject rather than strip).

---

## unslop `soul.py` integration (Phase 5)

### Pipeline position

```
humanize_deterministic()
  → Phase 0: _protect() placeholders
  → Phases 1–4: lexical + structural + stylometry measurement
  → Phase 5: humanize_soul()  ← contraction injection
  → Phase 3 (optional): detector feedback loop
  → _unprotect() + validate.py preservation + AI-ism residual check
```

Gating (`humanize.py` `_resolve_toggles`):

| Intensity | `soul` default |
|-----------|----------------|
| `subtle` | **off** |
| `balanced` | **on** |
| `full` | **on** |
| `anti-detector` | **on** (via balanced/full path + LLM procedure in SKILL.md) |

CLI: `--no-soul` disables Phase 5. `--soul` forces on regardless of intensity.

### Two passes inside `humanize_soul()`

**1. `contract_negations`** — 14 auxiliary–negation patterns (`do not`→`don't`, `cannot`→`can't`, etc.). Case-preserving via backreference. Always safe for truth value; runs on full protected text including all paragraphs.

**2. `contract_copula`** — 12 conservative copula/pronoun patterns with **allow-listed followers** (e.g. `it is`→`it's` only before `the`, `not`, `clear`, …; skips possessive-ambiguous contexts). **`preserve_first_sentence=True` (default):** first sentence of each multi-sentence paragraph stays uncontracted — register ramp mimics human prose (formal opener, relaxed body).

Both passes respect `_protect()` — code blocks, URLs, headings, tables, YAML untouched. `TestPreservation` + `TestSoul` in `tests/unslop/` enforce the contract.

### Measurement hooks

| Module | Function | Baseline |
|--------|----------|----------|
| `stylometry.py` | `StyleProfile.contraction_rate` | Per 1k words; voice-match delta |
| `validate.py` | `_contraction_rate()` | Warns if post-humanize rate still low; reports before/after in validation dict |
| `style_memory.py` | Persists numeric profile | Contraction rate in voice-match cache |
| `skills/unslop/SKILL.md` | Anti-detector item 3 | Targets ~0.17/chunk (misattributed to Kalemaj) |

`soul.py` does **not** target a numeric rate — it applies all safe patterns until exhaustion. Rate is an **outcome metric**, not a loop target (contrast: burstiness σ≥6 in anti-detector LLM mode).

### Design alignment with research

| Research finding | unslop response |
|------------------|-----------------|
| Contraction gap is strongest single marker (Paneru) | Phase 5 exists; negation + copula split |
| Overshoot reads as mechanical (Paneru Mistral; Phase 6 humanness) | First-sentence preservation; conservative copula allow-lists |
| Detectors need distributional shift, not vocab scrub | Soul runs **after** subtractive passes; additive injection |
| Contraction alone doesn't move TMR | Documented in README; cross-model pass recommended |
| ESL formal prose lacks contractions | Soul helps register; paired with burstiness in anti-detector mode |
| Broken Kalemaj citation | Removed from `validate.py`; **still in SKILL.md mirrors** |

### Gaps and recommended follow-ups

1. **Fix attribution everywhere:** Replace "Kalemaj et al." with **Paneru (2026), arXiv:2604.11687** or drop author until SSOT sync.
2. **Reconcile 17/1k vs 0.17/chunk baselines** — run `stylometry.analyze()` on Paneru-style human chunks if corpus becomes public; adjust validator threshold or document dual baselines (casual blog vs edited multi-style corpus).
3. **Optional rate cap:** If post-soul contraction_rate > ~30/1k on formal inputs, skip remaining copula patterns — guard against Mistral-style overshoot without LLM.
4. **Benchmark soul isolation:** Extend `benchmarks/detector_bench.py` with `--no-soul` vs `--soul` delta column; publish contraction_rate_before/after alongside `p_ai`.
5. **Do not imply detector bypass** in user-facing copy — contractions are item 4 of 5 local levers; item 1 remains cross-model paraphrase.

---

## Bottom line

Contraction-rate stylometry identifies a **real, measurable, token-level gap** between prompt-formalized AI prose and human reference text. Paneru (2026) quantifies it cleanly; parallel work embeds contraction ratio in hybrid detectors; idiolect research shows the gap is **not universal across models or genres**. unslop's `soul.py` implements the research-backed intervention — deterministic, preservation-safe, conservatively gated — in the correct pipeline slot. It improves voice and may reduce shallow stylometric flags; it does **not** defeat RAID-grade encoders. The "Kalemaj" label in unslop docs is a **wrong-author artifact**; the empirical finding belongs to **Paneru, arXiv:2604.11687**. Fix the citation, reconcile unit baselines, keep soul — and keep cross-model paraphrase as the documented ceiling for detector resistance.
