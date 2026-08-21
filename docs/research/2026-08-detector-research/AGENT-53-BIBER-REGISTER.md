# Agent #53 — Biber Register Analysis for Generation Conditioning and Detection

**Topic:** Douglas Biber's Multidimensional Analysis (MDA) as an interpretable bridge between style transfer, AI-text detection, and unslop voice-match  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**Biber register analysis is the most mature theory-grounded interface between "how text sounds" and "what we can measure."** Douglas Biber's Multidimensional Analysis (MDA) counts 67–96 lexico-grammatical features per text (contractions, nominalizations, that-clauses, wh-relatives, stance markers), then reduces them via factor analysis into interpretable dimensions such as *Involved vs. Informational Production* and *Narrative vs. Non-narrative Concerns*. Stylometry and register analysis identify the same underlying variation patterns — Grieve (2023) showed this on newspaper columnists — but register descriptors are auditable in ways function-word frequency tables are not.

Three 2025–2026 research threads make Biber features operationally relevant for unslop:

1. **Generation conditioning.** Yang & Carpuat (2025) prompt LLMs to produce structured Biber register analyses of style exemplars before rewriting. The register descriptor becomes an intermediate representation for example-based style transfer. Result: comparable or better style transfer than STYLL-style open-vocabulary descriptors, with a **large gain in meaning preservation** — the content-drift failure mode that plagues humanizers.

2. **Detection fingerprinting.** Reinhart et al. (*PNAS* 2025) and Rallapalli et al. (2026) show instruction-tuned LLMs systematically overuse information-dense constructions (nominalizations 1.5–2× human rate, present participial clauses 2–5×, that-clauses as subjects) and underuse complex rare constructions (pied-piping relatives, concessive *though*, discourse particles). Chat/instruction-tuned models **cluster together in Biber space regardless of base model family** — the "AI voice" is an RLHF attractor, not a vendor-specific quirk. Genre dominates source (human vs. model) in PCA projections.

3. **Tooling maturity.** NeuroBiber / BiberPlus (2025) delivers 96-feature tagging at ~56× the speed of legacy MAT taggers, with a HuggingFace demo and Python API. unslop's `stylometry.py` already implements cheap proxies (TTR, contraction rate, latinate ratio) but not full Biber counts.

**For unslop:** Biber is not a detector replacement — it is an **interpretable evaluation and conditioning layer**. Recommended path: (a) add optional BiberPlus/NeuroBiber fingerprint delta to voice-match and anti-detector eval; (b) experiment with RG-style register prompting in LLM humanize mode; (c) map known AI-slop tells (nominalization inflation, participial pileups) to specific Biber feature IDs for deterministic pre-pass targets. Do not claim "human" from Biber distance alone — Jemama (2025) showed style fidelity and statistical undetectability are separable objectives.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Biber (1988)** — *Variation Across Speech and Writing* | https://www.cambridge.org/core/books/variation-across-speech-and-writing/ |
| **Biber (1995)** — methodological reply (Watson) | https://jan.ucc.nau.edu/biber/Biber/Biber%20(1995).pdf |
| **Grieve (2023)** — register explains stylometry | https://doi.org/10.1515/cllt-2022-0040 |
| **Reinhart et al. (2025)** — *PNAS* LLM vs human Biber features | https://doi.org/10.1073/pnas.2422455122 |
| **Reinhart OSF preprint** | https://doi.org/10.17605/osf.io/7mrqn |
| **Rallapalli et al. (2026)** — RAID × Biber × genres × decoding | https://arxiv.org/abs/2604.14111 |
| **Rallapalli HTML** | https://arxiv.org/html/2604.14111 |
| **Yang & Carpuat (2025)** — register-conditioned style transfer | https://arxiv.org/abs/2505.00679 |
| **Yang & Carpuat HTML** | https://arxiv.org/html/2505.00679v1 |
| **Milička et al. (2025)** — LLM stylistic benchmark (AI-Brown) | https://arxiv.org/abs/2509.10179 |
| **NeuroBiber paper** | https://arxiv.org/abs/2502.18590 |
| **BiberPlus GitHub** | https://github.com/davidjurgens/biberplus |
| **NeuroBiber HuggingFace model** | https://huggingface.co/Blablablab/neurobiber |
| **NeuroBiber live demo** | https://huggingface.co/spaces/Blablablab/neurobiber-demo |
| **MAT tagger (Nini 2019)** | https://sites.google.com/site/multidimensionaltagger |
| **MAT GitHub mirror** | https://github.com/andreanini/multidimensionalanalysistagger |
| **pseudobibeR (Reinhart/Rallapalli toolchain)** | https://github.com/browndw/pseudobibeR |
| **mda.biber R package (Reinhart)** | https://doi.org/10.32614/cran.package.mda.biber |
| **RAID benchmark** | https://arxiv.org/abs/2405.07926 |
| **STYLL (Patel et al. 2024)** — baseline Yang & Carpuat beat on meaning | https://arxiv.org/abs/2402.04983 |
| **Jemama (2025)** — style match ≠ undetectability | https://arxiv.org/abs/2509.24930 |
| **Catch Me If You Can (EMNLP 2025)** — prompt imitation ceiling | https://arxiv.org/abs/2509.14543 |

### unslop internal references

| Resource | Path |
|----------|------|
| Style-transfer synthesis (Cat 10) | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |
| Yang & Carpuat entry | `docs/research/10-style-transfer-voice/A-academic.md` §9.4 |
| Reinhart / RLHF homogenization | `docs/research/10-style-transfer-voice/A-academic.md` §9.5 |
| Voice-match stylometry (partial proxies) | `unslop/scripts/stylometry.py` |
| UPDATE-PLAN Biber row | `docs/research/2026-08-detector-research/UPDATE-PLAN-2026-08.md` |

---

## Theoretical foundation: what Biber MDA actually measures

**Register ≠ dialect.** In corpus linguistics, *register* is linguistic variation tied to situational context and communicative purpose (academic prose vs. personal letter vs. news report). *Style* in the authorship sense is an individual's habitual choices within that context. Biber's MDA operationalizes register by counting co-occurring feature bundles and extracting latent dimensions via factor analysis.

The canonical English model (Biber 1988) defines **six dimensions** from 67 lexico-grammatical features:

| Dimension | Pole labels (simplified) | Example feature bundles |
|-----------|--------------------------|-------------------------|
| D1 | Involved ↔ Informational | 1st/2nd person pronouns, contractions, private verbs vs. nouns, prepositions, attributive adjectives |
| D2 | Narrative ↔ Non-narrative | Past tense, 3rd-person pronouns, perfect aspect vs. present tense, attributive adjectives |
| D3 | Situation-dependent ↔ Elaborated reference | Time/place adverbs, demonstratives vs. wh-relative clauses, pied-piping |
| D4 | Overt persuasion | Modals, infinitives, suasive verbs, necessity modals |
| D5 | Abstract ↔ Non-abstract information | Conjuncts, passives, past participial clauses, nominalizations |
| D6 | On-line informational elaboration | That-clauses, demonstratives, final prepositions |

**Why this matters for NLP:** These dimensions are *functional*, not lexical. You can shift D5 (information density) without changing topic. That is exactly the failure mode of LLM prose — and exactly what a humanizer needs to steer.

Grieve (2023) ran parallel stylometric and MDA analyses on two newspaper columnists. Both methods distinguished the authors and recovered **the same underlying variation structure**. His conclusion: stylometric authorship attribution works because authors write in subtly different *registers*, not because each author has a private dialect. For forensic and product use cases, register descriptors beat opaque function-word vectors because you can explain *why* two texts differ ("more nominalization, fewer wh-object relatives") instead of "cosine distance 0.73."

---

## Generation conditioning: Yang & Carpuat (2025)

**Problem.** Example-based arbitrary style transfer: given input text *x* and a style exemplar *s*, rewrite *x* to match *s*'s style while preserving meaning. STYLL (Patel et al. 2024) asks the LLM to infer open-vocabulary descriptors ("clear, concise, persuasive") from exemplars. Those descriptors drift into content and produce weak style fidelity.

**Method — RG and RG-Contrastive.** Three-step prompting on Llama-3.2-3B-Instruct (and Llama-3.1-8B for authorship imitation):

1. LLM analyzes the target exemplar using Biber's MDA framework → structured register descriptor.
2. *(RG-Contrastive only)* LLM contrasts input and target register profiles.
3. LLM rewrites input under register guidance.

**Evaluation.** Style transfer strength measured by "Towards" score in Biber MDA embedding space and StyleCAV authorship embeddings. Meaning preservation via MIS (mutual entailment), SBERT, METEOR. Tasks: Reddit authorship imitation (MUD), GYAFC formality, Cochrane medical simplification.

**Key results.**

- **Meaning preservation:** RG variants dominate STYLL on MIS across tasks. On MUD, RG sits on the Pareto frontier for style-vs-meaning tradeoffs; STYLL is consistently suboptimal — comparable or weaker style transfer with much worse meaning retention.
- **Style transfer:** Mixed by task direction. RG-Contrastive wins I2F formality; plain RG wins F2I. Authorship imitation favors RG without contrast on most MUD splits.
- **Target copying trap:** Naive "rewrite like this example" baselines achieve high style scores by copying target content (ROUGE overlap 3–5× higher than RG). Register prompting resists this — important for humanizers that must preserve user's factual claims.
- **Model size:** Benefits appear even on 3B instruct models — no 175B requirement (contrast Reif et al. 2022).

**Hypothesis (authors).** LLMs saw Biber register analyses in pretraining (education corpora, linguistics texts). Structured MDA descriptors are in-distribution in a way that adjective lists are not. Online text — a large pretraining slice — exhibits the same register variation Biber's corpora captured.

**Limits.** No detector-in-the-loop eval. No claim that Biber-matched output evades perplexity classifiers (cf. Jemama). Evaluation uses LLM-generated register analyses, not ground-truth NeuroBiber counts — circularity risk if the model hallucinates feature profiles.

---

## Detection: what Biber features reveal about LLM text

### Reinhart et al. (*PNAS* 2025)

Parallel corpora of human and LLM continuations (GPT-4o family, Llama 3 base + instruct). Instruction-tuned models prompted to continue in the same style as a 500-token human prefix.

**Systematic LLM overuse (vs. human):**

- Present participial clauses: **2–5×**
- Nominalizations: **1.5–2×**
- That-clauses as subject
- Phrasal coordination
- Lexical tells: *camaraderie, tapestry, palpable, intricate*

**Underuse:** Passive voice (~0.5× human rate in their setup).

**Scale invariance:** Differences persist from smaller to larger models. **Instruction tuning amplifies the gap** — base models sit closer to human Biber profiles than chat variants.

### Rallapalli et al. (2026) — RAID at scale

467,985 texts; 11 LLMs; 8 genres; 4 decoding strategies; 67 Biber features via pseudobibeR. No style-mimic prompt (unlike Reinhart) — zero-shot genre templates only.

**Classification signal.** Random forest on Biber features: AUC **0.9775** (downsampled) / 0.9755 (full). Top discriminators include f43_type_token (TTR) — not because LLMs always have low TTR, but because human TTR distribution is narrow and predictable; LLMs spread wider. SHAP interactions show TTR modulates many other features.

**Top 5 LLM overuses (aggregate):**

1. f29_that_subj — that-clauses as subject
2. f59_contractions — contractions *(note: contradicts "AI never contracts" folk wisdom; LLMs overuse contractions vs. human in this benchmark)*
3. f27_past_participle_whiz — postnominal participial clauses ("the solution produced by…")
4. f14_nominalizations
5. f34_sentence_relatives

**Top 5 underuses:** wh-object relatives, pied-piping relatives, concessive *though*, synthetic negation, sentence-initial discourse particles.

**Structural findings:**

- **Genre > source** in PCA: news-by-GPT-4 clusters with news-by-human, not with poetry-by-GPT-4.
- **Chat models cluster together** across genres — RLHF homogenization confirmed at feature level.
- **Model > decoding** within genre; temperature/repetition penalty matter less than model identity (exceptions: GPT-2, MPT, Mistral show decoding sensitivity).
- Signatures **robust** without style-mimic prompts — paraphrase/humanize must move specific constructions, not just vocabulary.

### Milička et al. (2025) — interpretable benchmark

AI-Brown corpus (LLM continuations of BE21 Brown-family texts) + Czech AI-Koditex replication. 16 frontier models ranked on Biber dimensions via MAT tagger. Framing: not detection-for-policing but **model quality** — does post-training flatten stylistic persona diversity?

Findings align with Reinhart/Rallapalli: instruction-tuned models shift toward information-dense, less narrative profiles. Czech shows larger stylistic drift than English — underrepresented languages expose attractor bias more clearly. Authors propose MDA as a standard LLM eval axis alongside coding benchmarks.

---

## Tooling landscape

| Tool | Features | Speed | Best for |
|------|----------|-------|----------|
| **MAT (Nini 2019)** | 67 (Biber 1988) | ~2.1k tok/s CPU | Ground-truth replication, dimension scoring |
| **pseudobibeR** | 67 | R-native | Reinhart/Rallapalli reproduction |
| **biberpy / profiling-UD** | 67+ | moderate | UD-pipeline integration |
| **BiberPlus** | 96 | ~4.6k tok/s CPU | Exact counts, PCA/factor analysis in-Python |
| **NeuroBiber** | 96 | ~117k tok/s GPU | Batch eval, real-time humanize feedback |

NeuroBiber macro-F1 **0.97** vs. rule tagger on validation; 56× faster than MAT baseline per authors. Tradeoff: neural approximation vs. rule exactness — use BiberPlus for audit, NeuroBiber for scale.

**Install path:** `pip install biberplus`; spaCy `en_core_web_sm`; optional GPU for NeuroBiber.

---

## unslop integration plan

### What we have today

`stylometry.py` extracts ~15 deterministic signals (sentence-length mean/stdev, TTR, contraction rate, latinate ratio, passive approx, DivEye proxies). These overlap partially with Biber — TTR ↔ f43, contractions ↔ f59, latinate/nominalization ↔ f14 family — but miss clausal architecture (that-subj, wh-relatives, participial whiz-deletion, discourse particles).

### Tier 1 — Eval-only (low risk, high audit value)

Add optional `--biber-profile` to voice-match / benchmark:

1. Extract NeuroBiber fingerprint for source sample + humanized output.
2. Report per-feature delta and dimension-score distance.
3. Flag regressions on known AI tells: nominalization ratio > 1.3× target, f29_that_subj spike, f27 participial pileup.

Output format mirrors existing `StyleProfile.delta()` — auditable, no API calls if NeuroBiber runs local.

### Tier 2 — Deterministic humanize hints

Map top overused Biber features to existing `humanize.py` passes:

| Biber feature | unslop lever |
|---------------|--------------|
| f14_nominalizations | Already targeted via latinate suffix + promotional register rules; extend with `-tion/-ment → verb` rewrite hints in LLM mode |
| f27/f34 participials & sentence relatives | Structural pass: split stacked postnominal clauses |
| f29 that-subj | Sentence opener diversification |
| f59 contractions | `soul.py` contraction pass — but **direction depends on target register**; do not blindly inflate |

Critical: Reinhart/Rallapalli disagree with folk "AI doesn't contract" — LLMs **overuse** contractions in aggregate benchmarks. Voice-match must steer *toward target*, not toward a generic "human mean."

### Tier 3 — LLM conditioning (RG-style)

In `--mode llm` / voice-match rewrite prompt, inject:

```
Before rewriting, analyze the target sample's register using Biber's multidimensional framework:
- Information density (nominalizations, prepositions, attributive adjectives)
- Involvement (pronouns, contractions, private verbs)
- Narrativity (past tense, third-person reference)
Contrast with the input. Rewrite preserving meaning; shift only register features that differ.
```

Pilot on benchmark samples; measure Biber Towards score + preservation validator pass rate. Cost: extra prompt tokens; benefit: Yang & Carpuat showed meaning preservation gains without fine-tuning.

### Tier 4 — Anti-detector ethics guardrail

Biber delta reports should **not** be marketed as "detector evasion scores." Use for:

- ESL false-positive defense ("your nominalization rate matches academic human baseline")
- Voice-match QA ("rewrite moved 80% toward target register on D1/D5")

Cite Rallapalli AUC ~0.98: feature manipulation alone won't beat modern detectors; genre-conditional evaluation is mandatory.

---

## Open questions and risks

1. **Circularity in RG prompting.** LLM-generated register analyses may not match NeuroBiber counts. Hybrid: compute ground-truth fingerprint externally, inject as structured JSON into rewrite prompt.

2. **Genre confound.** A humanizer that matches Biber profile in vacuum may still fail genre-appropriate detection — academic abstract vs. Reddit post need different dimension targets.

3. **Contradiction with surface heuristics.** Biber aggregate shows contraction *overuse*; unslop `soul.py` often *adds* contractions for human feel. Resolution: target-profile-relative steering, not global rules.

4. **Dependency weight.** NeuroBiber adds torch/transformers/spaCy — same tier as DivEye. Keep opt-in via extras: `pip install unslop[biber]`.

5. **Non-English.** Czech MDA exists (Cvrček et al. 2018); English-centric unslop should document limitation. Milička benchmark shows English LLM stylistic bias is *smaller* than Czech — ESL users face double penalty.

6. **Humanizer evasion arms race.** Adversarial paraphrase papers (NeurIPS 2025 AP, TempParaphraser) attack probability-based detectors. Biber features are more robust than perplexity but Rallapalli shows TTR+interactions still discriminate — paraphrase that preserves information density may remain detectable.

---

## Bottom line

Biber register analysis closes the loop between unslop's two halves: **subtraction** (remove AI-slop tells that map to f14/f27/f29 overuse) and **voice-match** (steer toward a target register profile, not a vibes checklist). Yang & Carpuat proved the same framework works as a **generation conditioner** without fine-tuning. Reinhart and Rallapalli proved the same features define a **durable detection fingerprint** biased by RLHF, not just vocabulary.

unslop should treat Biber as the auditable measurement layer sitting above regex passes and below LLM rewrite — the place where you can honestly say "this rewrite moved toward your register" with feature-level receipts. It is not a silver bullet for detector evasion, and it should not be sold as one.

---

## Word count

~2,150 words (body excluding tables).
