# Agent #43 — Catch Me If You Can (EMNLP 2025)

**Topic:** Personal implicit-style detection & imitation — mechanism, benchmarks, GitHub, critics, unslop `voice-match` relevance  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**Catch Me If You Can? Not Yet** (Wang et al., EMNLP 2025 Findings, arXiv 2509.14543) is the largest peer-reviewed measurement of whether **frontier LLMs can imitate an everyday author's implicit writing style from few-shot in-context examples alone**. It is an **evaluation paper**, not a humanizer. The authors prompt six models (GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3, Llama-4-Maverick) with five author samples + a content summary, then score ~40,000 generations per model across 400+ authors in four genres.

**Verdict:** Prompt-only personalization **partially works in structured genres** (news, email) and **fails in informal ones** (blogs, forums). Authorship verification on Blog drops to **~17–21%** for 5-shot LLM output vs **91.4%** for real human pairs. GPTZero flags most GPT-family outputs as AI (<1% "human" on blogs). More demonstrations (2→10) barely help.

For **unslop**, this paper is the **ceiling citation for `/unslop voice-match`**: it proves prompt + samples won't pass stylometric attribution on informal personal writing. unslop's extract-then-apply architecture (`stylometry.py` + `style_memory.py` → numeric targets in the LLM prompt) is the right *direction* but still prompt-bound — one layer short of TinyStyler/PEFT fine-tuning.

**Internal audit flag:** unslop currently cites Catch Me If You Can for the **23.5× few-shot gain** and **"fine-tuning wins decisively"** in `skills/unslop/SKILL.md`. The 23.5× figure is from **Jemama et al.** (arXiv 2509.24930, IEEE UEMCON 2025), not Wang et al. Catch Me If You Can reports ~**2–3×** few-shot gains on Blog AV/AA, not 23.5×. Wang et al. **does not run fine-tuning experiments** — that claim is inferred from adjacent work (Liu et al. 2024 INLG, Tan et al. 2024 EMNLP, TinyStyler EMNLP 2024). Split the citations in SKILL.md.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **arXiv preprint** | https://arxiv.org/abs/2509.14543 |
| **arXiv HTML** | https://arxiv.org/html/2509.14543 |
| **ACL Anthology (EMNLP 2025 Findings)** | https://aclanthology.org/2025.findings-emnlp.532/ |
| **ACL PDF** | https://aclanthology.org/2025.findings-emnlp.532.pdf |
| **DOI** | https://doi.org/10.18653/v1/2025.findings-emnlp.532 |
| **arXiv DOI redirect** | https://doi.org/10.48550/arxiv.2509.14543 |
| **Author project page** | https://www.zhengxiang-wang.me/papers/implicit-writing-styles/ |
| **GitHub (data + code)** | https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation |
| **Main experiment data (Google Drive)** | https://drive.google.com/file/d/1zzlnY_OTr6Mtnt19DQBtYF5LttF6DOt2/view?usp=sharing |
| **Follow-up data (Google Drive)** | https://drive.google.com/file/d/1fxkoClxjfkrUpzqy9rfPZk7tcCobkQG1/view?usp=sharing |
| **GPTZero (detector used)** | https://gptzero.me/ |
| **LiteLLM (generation API wrapper)** | https://github.com/BerriAI/litellm |

### Related / tension papers

| Paper | URL | Relationship |
|-------|-----|--------------|
| **Jemama et al. — How Well Do LLMs Imitate Human Writing Style?** (IEEE UEMCON 2025) | https://arxiv.org/abs/2509.24930 · https://doi.org/10.1109/uemcon67449.2025.11267719 · claimed repo `rajeshjnu2006/writing-style-uemcon2025` unavailable as of 2026-08-21 | Same month, different setup: academic essays, completion prompting hits 99.9% AV agreement; source of **23.5×** few-shot claim |
| **TinyStyler** (EMNLP 2024 Findings) | https://aclanthology.org/2024.findings-emnlp.781/ | ~800M model + authorship embeddings beats GPT-4 on style transfer — supports fine-tune/small-expert path |
| **Liu et al. — Customizing LLM generation style via PEFT** (INLG 2024) | https://aclanthology.org/2024.inlg-main.412/ | Cited by Wang as practical fine-tune alternative they deliberately exclude |
| **Tan et al. — Personalized PEFT** (EMNLP 2024) | https://aclanthology.org/2024.emnlp-main.6476/ | Democratizing per-user LoRA; cited as scalability counterpoint |
| **Bhandarkar et al. — Emulating author style feasibility** (PERSONALIZE 2024) | https://aclanthology.org/2024.personalize-1.6/ | Snippet-seeding precursor; Wang's **+Snippet** ablation |
| **Cho et al. — Trial-Error-Explain ICL** (NAACL 2025) | https://aclanthology.org/2025.naacl-long.5864/ | Multi-turn prompting Wang excludes as impractical for chat UI |
| **Padmakumar & He — LLMs reduce content diversity** (ICLR 2024) | https://openreview.net/forum?id=FN7XJ5kZvc | Motivation: generic RLHF style strips personal voice |
| **Huang et al. — Authorship Attribution survey** (SIGKDD 2025) | https://arxiv.org/abs/2408.08946 | Canonical AA/AV taxonomy |
| **Foreverse synthesis blog** (practitioner) | https://foreverse.app/blog/can-ai-imitate-an-authors-style | Reconciles Jemama completion results with Wang everyday-author pessimism |

### unslop internal references

| Resource | Path |
|----------|------|
| voice-match skill spec + Known Limitation | `skills/unslop/SKILL.md` §voice-match |
| Stylometry extraction (Phase 4) | `unslop/scripts/stylometry.py` |
| Numeric style memory (Phase 8) | `unslop/scripts/style_memory.py` |
| Voice targets in LLM prompt | `unslop/scripts/humanize.py` (`_build_voice_block`, `_format_voice_targets`) |
| Cat 10 synthesis | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |
| Implementation trace | `docs/research/IMPLEMENTATION_TRACE.md` |

---

## Mechanism

### Problem definition

**Implicit personalized writing imitation:** Given author *a*, few-shot samples from *a*'s prior writing, and a **content summary** of a held-out test piece, can LLM *L* generate text *tₐᴸ* that matches *a*'s style without explicit stylistic instructions?

This mirrors real chat-UI usage: paste a few emails/posts, ask for a new draft on a topic. No fine-tuning, no multi-turn refinement, **one API call**, temperature **0**.

```
Train split Tₐᵗʳ  ──sample 5 examples──▶  Prompt
Test summary S(tₐ)  ──────────────────▶  Prompt  ──▶  LLM  ──▶  tₐᴸ
                                              │
                                              ▼
                                    4-metric evaluation ensemble
```

### Four-metric evaluation ensemble

Wang et al. reject LLM-as-judge (subjective, self-preference bias per Panickssery et al. 2024) and ROUGE/METEOR (content overlap, not style). Instead:

| Metric | Model / tool | Question answered | Training |
|--------|--------------|-------------------|----------|
| **AA** — Authorship Attribution | Longformer-base-4096 + ModernBERT-base | Does *tₐᴸ* get attributed to author *a* (top-5)? | Fine-tuned on human train splits per dataset |
| **AV** — Authorship Verification | Same encoders, pair classifier | Do (*tₐᴸ*, *tₐ*) look same-author? | Balanced pos:neg = 4:6 pairs from human data |
| **Style model** | LIWC-22 + WritePrint features → Mahalanobis distance to per-author centroid | Is *tₐᴸ* closer to *a*'s distributional style than other authors? | Unsupervised feature extraction per author |
| **AI detection** | GPTZero (off-the-shelf) | Does output pass as human-written? | None (commercial API) |

**Design rationale:** AA conflates content + style (Sari et al. 2018) — explains non-trivial zero-shot AA from topical overlap alone. AV is the strictest pairwise test. Style model gives explicit stylometric grounding (same feature families unslop proxies in `stylometry.py`). GPTZero adds human-likeness axis separate from authorship match.

### Datasets (400 authors, 4 genres)

| Dataset | Genre | Authors | Samples | Avg words | Human AV acc. | Human AA top-5 | Human style acc. |
|---------|-------|---------|---------|-----------|---------------|----------------|------------------|
| **CCAT50** | News (Reuters) | 50 | 2,500 | 584 | 89.2% | 94.9% | 69.1% |
| **Enron** | Email | 150 | 3,884 | 309 | 88.9% | 79.8% | 79.4% |
| **Reddit** | Forum posts | 100 | 8,451 | 333 | 87.7% | 89.7% | 73.8% |
| **Blog** | Personal blogs | 100 | 25,224 | 319 | **91.4%** | 95.5% | 81.9% |

Preprocessing: 100–1500 words per sample, top-N authors by volume, 50/50 train/test, Reddit stratified by subreddit. Summaries generated by **GPT-4.1** (semantic control so evaluation isolates style).

### Models & prompting

- **6 LLMs:** GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3, Llama-4-Maverick
- **Default:** 5 random train samples per test item (same samples across models)
- **Baseline:** 0-shot (summary only) on 4 models
- **Follow-ups (§6):** content-similar exemplars (+Sim), length-matched (+Len), opening snippet (+Snippet), 2/4/6/8/10 shot count

### What the paper deliberately excludes

- **Fine-tuning / LoRA / RAG** — cited as better but impractical for chat-UI users with few samples
- **Multi-turn prompting** (Cho et al. 2025, Bhandarkar et al. 2024 iterative) — latency/API cost
- **Cross-genre transfer** — exemplar genre = generation genre only
- **Human perceptual eval at scale** — acknowledged limitation

---

## Benchmarks (headline numbers)

### Main result — Authorship Verification (5-shot, Table 3)

Higher = generated text verified as same-author with human reference.

| Dataset | GPT-4o | GPT-4o-mini | Gemini-2.0-Flash | Gemma-3-27B | DeepSeek-V3 | Llama-4-Mav |
|---------|--------|-------------|------------------|-------------|-------------|-------------|
| **CCAT50** (news) | 95.28 | 95.16 | 97.44 | 97.34 | 97.46 | 94.68 |
| **Enron** (email) | 96.15 | 96.64 | 96.44 | 96.17 | 96.30 | 95.65 |
| **Reddit** (forum) | 63.65 | 60.23 | 65.88 | 55.54 | 49.97 | 65.10 |
| **Blog** (informal) | **19.37** | **17.93** | **21.25** | **16.72** | **20.77** | **17.61** |

**Human Blog AV ceiling: 91.4%.** Best LLM Blog AV ≈ **21%** — roughly **coin-flip against a 4:6 balanced AV training prior**, far below human pairs.

### Few-shot vs zero-shot (Blog AV, GPT-4o)

| Setting | Blog AV | Blog AA top-5 |
|---------|---------|---------------|
| 5-shot | 19.37% | 39.39% |
| 0-shot | 8.15% | 17.22% |
| **Ratio** | **~2.4×** | **~2.3×** |

These are the **actual** few-shot gains in Catch Me If You Can on the hardest domain. Not 23.5×.

### Authorship Attribution top-5 (5-shot, Table 2 — selected)

| Dataset | GPT-4o | Gemini-2.0-Flash | Gemma-3-27B |
|---------|--------|------------------|-------------|
| CCAT50 | 86.64 | 92.17 | 93.30 |
| Enron | 59.65 | 59.56 | 62.38 |
| Reddit | 27.12 | 35.59 | 30.53 |
| Blog | 39.39 | 44.34 | 39.38 |

AA looks better than AV on blogs because top-5 gives partial credit and topic overlap helps — still far below human 95.5% Blog AA.

### GPTZero "% detected as human" (5-shot, Table 4)

| Model | CCAT50 | Enron | Reddit | Blog |
|-------|--------|-------|--------|------|
| GPT-4o | 0.08 | 16.86 | 0.67 | 0.47 |
| GPT-4o-mini | 0.00 | 13.76 | 0.12 | 0.35 |
| Gemini-2.0-Flash | 20.49 | 54.25 | 20.77 | 18.74 |
| Gemma-3-27B | 31.36 | 43.63 | 16.09 | 7.58 |

**Interpretation:** Even when AA/AV partially pass, **detector human-likeness stays low** for OpenAI models. Authors warn GPTZero may be **vendor-biased** (optimized for GPT outputs) — treat cross-model detection rates cautiously.

### Semantic control sanity check (Table 5)

SBERT similarity ≥ 0.74–0.78 across settings — models follow the summary. Failures are **stylistic**, not instruction-following.

### Follow-up ablations (§6, 3-model average, Table 6)

| Trick | Blog AV | Blog % Human (GPTZero) | Notes |
|-------|---------|------------------------|-------|
| 5-shot baseline | 19.40 | 9.00 | — |
| +Len ctrl | 20.68 | 27.50 | Surface length match; style acc drops |
| +Sim ctrl | **10.33** | 8.60 | Topic-cluster exemplars **hurt** AV |
| +Snippet† | 15.04 | 21.70 | Seed with author's opening words; boosts detection, mixed AV |

**Exemplar count (Figure 5):** 2→10 shots — **flat curves** on AA/AV/style. Diminishing returns confirmed.

### Scale

- **>40,000 generations per model**
- **400+ authors** across four corpora
- Greedy decoding throughout (reproducibility)

---

## GitHub reproduction

**Repo:** https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation  
**Stars / forks (Aug 2026):** ~5 / 0 — early release, fully functional eval harness  
**License:** Not prominently stated in README; check repo root before commercial reuse

### Layout

```
llms-implicit-writing-styles-imitation/
├── README.md
├── requirements.txt
├── scripts/
│   ├── generate_llm_writing.py      # LiteLLM generation, settings 1–6
│   ├── train_and_eval_an_AA_model.py
│   ├── deploy_AA_models.py
│   ├── train_and_eval_an_AV_model.py
│   ├── deploy_AV_models.py
│   ├── create_stylometry_features.py  # LIWC + WritePrint style models
│   ├── create_AV_datasets.py
│   └── LIWC2007_English100131.dic
├── dataset_prepare/    # from Google Drive zip
└── dataset_followup/   # Section 6 subsets
```

### Reproduction path

1. `conda create -n PW python=3.12.9 && conda activate PW`
2. `pip install -r requirements.txt`
3. Download `dataset_prepare` + `dataset_followup` zips from Google Drive links in README
4. Generate: `python generate_llm_writing.py --training_df_fp=dataset_prepare/blog_train.csv --evaluation_df_fp=dataset_prepare/blog_test.csv --setting=1 --llm=openai/gpt-4o-mini-2024-07-18`
5. Train AA/AV: `train_and_eval_an_AA_model.py` / `train_and_eval_an_AV_model.py` with ModernBERT or Longformer
6. Deploy evaluators on LLM outputs: `deploy_AA_models.py`, `deploy_AV_models.py`
7. Stylometry: `create_stylometry_features.py`

### Setting codes

| Setting | Meaning |
|---------|---------|
| 1 | 5-shot random (main paper) |
| 2 | +Sim ctrl (same BERTopic cluster) |
| 3 | +Len ctrl (length-matched exemplars) |
| 4 | 0-shot baseline |
| 5 | +Snippet (author opening excerpt) |
| 6 | Variable shot count 2/4/6/8/10 |

### unslop eval gap

The harness tests **raw LLM generation**, not **humanizer pipeline output**. No public benchmark yet asks: "Does unslop voice-match + stylometry move Blog AV from 19% toward 91%?" Adapting `deploy_AV_models.py` on unslop before/after pairs would be the cleanest external oracle.

---

## Critics, limitations, and literature tension

### Stated limitations (paper §Limitations)

1. **No large-scale human evaluation** — automated metrics may miss perceptual "sounds like me"
2. **Within-genre only** — no cross-genre author consistency test
3. **English-only, four corpora** — demographic diversity bounded
4. **Small per-author training sets for AA/AV** — unstable for low-consistency authors
5. **GPTZero as black-box detector** — vendor bias, no open weights

### Methodological critiques

| Critique | Detail |
|----------|--------|
| **AA confounds topic and style** | Authors acknowledge; zero-shot AA > random on topic overlap alone. AV + style model partially mitigate. |
| **Summary intermediary** | GPT-4.1 summaries may homogenize content plans, adding RLHF genericness before style eval. |
| **Temperature 0** | Maximizes reproducibility but may suppress stylistic variance humans exhibit. |
| **GPTZero asymmetry** | GPT-4o ≈ 0% human on blogs while Gemini ≈ 19% — detector choice skews "human-likeness" axis. |
| **Blog = hardest, Blog = target use case** | Personal voice products (email assistants, LinkedIn, Medium) skew informal — worst domain is the commercial one. |

### Tension with Jemama et al. (arXiv 2509.24930)

Same research window, **opposite headline on prompting**:

| Dimension | Catch Me If You Can (Wang) | Jemama et al. |
|-----------|---------------------------|---------------|
| **Corpus** | Everyday authors, 4 genres | Academic essays |
| **Task** | Generate from summary + samples | Style match / continue text |
| **Best prompt** | 5-shot imitation | **Completion** (human prefix) → 99.9% AV |
| **Few-shot gain** | ~2–3× on Blog AV | Up to **23.5×** style-matching vs zero-shot |
| **Detectability** | GPTZero mostly fails | High style match **≠** human perplexity (29.5 vs 15.2) |

**Reconciliation:** Completion prompting anchors the model in the author's **lexical manifold** for continuation; **de novo generation from a summary** (Wang's task) is harder and closer to what writing assistants actually do. Jemama's 99.9% does **not** contradict Wang's Blog failure — different task geometry. unslop should cite **both**: Wang for voice-match ceiling on generative rewrite; Jemama for perplexity/style separability and completion-vs-description hierarchy.

### Fine-tuning "wins decisively" — provenance

Catch Me If You Can **does not benchmark fine-tuning**. The claim in unslop docs chains:

- Wang et al. → "prompt-only insufficient" (direct)
- Liu et al. 2024 INLG → PEFT style customization works (cited, not replicated)
- Tan et al. 2024 EMNLP → personalized LoRA at scale (cited)
- TinyStyler EMNLP 2024 → 800M + embeddings **beats GPT-4** on authorship transfer (strongest direct evidence)

**Accurate SKILL.md wording:** "Catch Me If You Can shows frontier prompt-only imitation fails on informal personal style; TinyStyler / PEFT lines show specialized adaptation beats prompting (see Liu 2024, Tan 2024, TinyStyler 2024)."

### Ethical considerations (paper §Ethical)

- Impersonation, academic dishonesty, phishing risk from style mimicry
- Style as quasi-biometric identifier — privacy even on "public" corpora
- English-only fairness gap
- Disclosure/transparency as LLM prose converges on human surface form

### Community reception

- **No dedicated HN front page** found for arXiv 2509.14543 specifically
- Findings circulate via research syntheses (Foreverse, Moonlight review: https://www.themoonlight.io/en/review/catch-me-if-you-can-not-yet-llms-still-struggle-to-imitate-the-implicit-writing-styles-of-everyday-authors)
- Practitioner HN threads on voice preservation align with the pessimistic informal-genre result (e.g. https://news.ycombinator.com/item?id=47346032 — LLM polish "doesn't sound like me")
- unslop Cat 10 E-practical claims HN/r/LocalLLaMA circulation validating "fine-tune not prompts" — **vendor narrative confirmation**, not independent replication of Wang's harness

---

## unslop `voice-match` mode relevance

### What voice-match claims vs what Catch Me If You Can proves

| voice-match claim | Catch Me If You Can evidence |
|-------------------|------------------------------|
| "Mimic a sample's register, cadence, punctuation" | Partial — structured genres yes, blogs/forums no |
| "Best-effort prompt approximation" | Consistent — paper tests exactly this regime |
| "Won't pass stylometric attribution" | **Confirmed** — Blog AV ~19% vs human 91% |
| "Fine-tune for production cloning" | **Not tested in paper** — infer from TinyStyler/PEFT |
| "23.5× few-shot better than zero-shot" | **Wrong paper** — use Jemama 2509.24930 or Wang's ~2.4× Blog AV |

### Architectural alignment (extract-then-apply)

Catch Me If You Can's style model uses **LIWC + WritePrint** — the same classical stylometry family unslop implements deterministically:

```1:30:unslop/scripts/stylometry.py
"""Phase 4 stylometry: deterministic style-signal extraction for voice-match.
...
analyze(text) -> StyleProfile returns a dataclass of measured signals:
  sentence_length_mean / sentence_length_stdev
  fragment_rate, contraction_rate, em_dash_rate, ...
```

```1249:1268:unslop/scripts/humanize.py
def _build_voice_block(sample_text: str | None, profile=None) -> str:
    ...
    profile = analyze(sample_text)
    ...
    return _format_voice_targets(profile)
```

**Gap:** Wang evaluates whether LLM output **matches author centroids**. unslop feeds numeric deltas **into** the LLM prompt but never **closes the loop** with AA/AV verification. Catch Me If You Can's harness is the oracle unslop lacks.

### Mode-by-mode positioning

| unslop mode | Catch Me If You Can implication |
|-------------|--------------------------------|
| **voice-match** | Legitimate for register/cadence steering on **structured** prose; must disclaim Blog/forum-grade idiolect cloning. Cite Wang for ceiling. |
| **anti-detector** | Orthogonal axis — Wang shows authorship match ≠ GPTZero pass; Jemama shows style match ≠ perplexity. voice-match ≠ detector evasion. |
| **balanced/full** | Generic anti-slop helps "average human" but **increases distance** from a specific author's implicit style (RLHF regression toward mean). |

### Recommended SKILL.md edits

1. **Split citations:** Wang 2509.14543 for attribution ceiling; Jemama 2509.24930 for 23.5× and perplexity/style split
2. **Replace "fine-tuning wins decisively"** with "specialized adaptation (TinyStyler, PEFT) beats prompting; Catch Me If You Can shows prompt-only fails on informal personal style"
3. **Add genre caveat:** voice-match strongest on email/docs; weakest on casual blog/social voice
4. **Optional honest upgrade path:** "For Blog-grade fidelity, completion-style seeding (+Snippet analog) or fine-tuned authorship embeddings — not yet in unslop CLI"

### Benchmark integration opportunities

| Priority | Action |
|----------|--------|
| **P1** | Fix misattributed 23.5× in SSOT `skills/unslop/SKILL.md` (mirrors sync via CI) |
| **P2** | Add `benchmarks/voice_match_bench.py` wrapper around Wang's Blog subset: unslop before/after → deploy AV model |
| **P3** | Report stylometric Mahalanobis distance (LIWC/WritePrint or unslop proxy) alongside AI-ism residual |
| **P4** | Track Jemama completion-prompting as future `--voice-seed-snippet` flag (author prefix continuation) |

### What unslop should **not** claim

- "Write in your voice" for informal personal blogging (Wang Blog AV ~19%)
- Stylometric-attribution-resistant output from prompt-only voice-match
- That more samples fixes the gap (Wang: 2→10 shots flat)
- That voice-match helps GPTZero (Wang: authorship ≠ detection; GPT-4o ≈ 0% human on blogs)

---

## Bottom line

**Catch Me If You Can** is the peer-reviewed **negative result** personal-voice products need: frontier LLMs + few-shot prompting **do not** reproduce everyday implicit style in the registers users care about most. The eval harness (AA + AV + LIWC/WritePrint + GPTZero) is the gold-standard **measurement stack**; the GitHub repo is reproducible but niche.

**unslop voice-match** sits correctly as a **best-effort, numerically anchored prompt layer** — better than "write like me" vibes, insufficient for stylometric cloning. Fix the **23.5× citation error**, cite Wang for the ceiling and Jemama/TinyStyler for the upgrade path, and treat Blog AV (~19% vs 91% human) as the honest benchmark target if unslop ever claims personal voice fidelity.
