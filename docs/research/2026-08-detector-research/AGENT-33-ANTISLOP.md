# Agent #33 — ANTISLOP / auto-antislop / peakoss CI gate

**Topics:** Paech et al. ANTISLOP (ICLR 2026), `sam-paech/auto-antislop` pipeline, `peakoss/anti-slop` GitHub Action  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop positioning refresh

---

## Executive summary

Three different projects share the word "antislop." They solve different layers of the same problem — repetitive, recognizable AI output — and **do not compete with unslop**.

| Layer | Project | When it acts | Requires |
|-------|---------|--------------|----------|
| **Weights / sampler** | ANTISLOP (Paech et al., ICLR 2026) | During token generation or via FTPO fine-tune | Raw logits, self-hosted model, GPU |
| **Post-generation text** | **unslop** | After assistant/API output exists | Any host (Claude Code, Cursor, pip CLI) |
| **Contribution gate** | `peakoss/anti-slop` | On PR open (CI) | GitHub Actions, maintainer config |

**ANTISLOP** (arXiv [2510.15061](https://arxiv.org/abs/2510.15061), accepted **ICLR 2026 Poster**, Apr 24 2026) formalizes what the LocalLLaMA community built in `sam-paech/antislop-sampler`: detect statistically over-represented phrases ("slop"), suppress them at inference via **backtracking resample**, then optionally bake suppression into weights with **Final Token Preference Optimization (FTPO)**. Reported results: some patterns **>1,000×** more frequent in LLM vs human text; sampler handles **8,000+** banned strings where token banning breaks at **~2,000**; FTPO achieves **~90% slop reduction** with **<1%** writing-quality loss vs **6–15 point** degradation under DPO.

**auto-antislop** automates the full loop: profile model-specific slop fingerprints → generate FTPO preference pairs from sampler traces → fine-tune. Checkpoint example: [`sam-paech/gemma-3-27b-it-antislop`](https://huggingface.co/sam-paech/gemma-3-27b-it-antislop) on Hugging Face.

**peakoss/anti-slop** is a **maintainer CI gate**, not a text humanizer. It runs **34 heuristic checks** on PR metadata (branch names, title/description, template compliance, commit messages, file paths, contributor signals) and closes PRs that trip **`max-failures`** (default 4). Battle-tested on Coolify (~120 slop PRs/month). **762★** as of Aug 2026. AGPL-3.0.

**unslop verdict:** ANTISLOP owns **generation-time and weight-time** subtraction for self-hosted stacks. unslop owns **post-generation residue cleanup** for SaaS assistants where you never see logits. peakoss owns **repo hygiene** at the PR boundary. README already states this split correctly ([Antislop · Paech, ICLR 2026](https://arxiv.org/abs/2510.15061) in Inspirations table). Highest-value cross-pollination: export unslop `Replacement`/`HumanizeReport` per-rule counts as **training-data signal** for auto-antislop-style profiling; import ANTISLOP slop fingerprints into `anti-aiisms.md` curation.

---

## Primary sources (URLs)

### Academic ANTISLOP

| Resource | URL |
|----------|-----|
| **Paper (arXiv)** | https://arxiv.org/abs/2510.15061 |
| **Paper (PDF v1)** | https://arxiv.org/pdf/2510.15061v1 |
| **DOI** | https://doi.org/10.48550/arxiv.2510.15061 |
| **OpenReview (ICLR 2026)** | https://openreview.net/forum?id=gLcyM1khyp |
| **ICLR 2026 poster page** | https://iclr.cc/virtual/2026/poster/10008156 |
| **Hugging Face papers** | https://huggingface.co/papers/2510.15061 |
| **Emergent Mind summary** | https://www.emergentmind.com/topics/antislop-sampler |
| **Thoughtworks AI Labs explainer** | https://research.thoughtworks.com/library/anti-slopping-an-innovation-for-rectifying-llm-writing-cliches |
| **Allen Roush (co-author) LinkedIn post** | https://www.linkedin.com/posts/allen-roush-27721011b_after-years-of-llms-converging-on-the-same-activity-7387167851146756098-txV0 |

### Code & artifacts

| Resource | URL |
|----------|-----|
| **auto-antislop (full pipeline, MIT)** | https://github.com/sam-paech/auto-antislop |
| **antislop-sampler (inference, MIT)** | https://github.com/sam-paech/antislop-sampler |
| **antislop-vllm (OpenAI-compatible API)** | https://github.com/sam-paech/antislop-vllm |
| **Fine-tuned checkpoint** | https://huggingface.co/sam-paech/gemma-3-27b-it-antislop |
| **koboldcpp integration (v1.76+)** | https://github.com/LostRuins/koboldcpp/releases/tag/v1.76 |
| **koboldcpp antislop issue (closed, shipped)** | https://github.com/LostRuins/koboldcpp/issues/1141 |
| **koboldcpp regex bans (open)** | https://github.com/LostRuins/koboldcpp/issues/1233 |
| **llama.cpp SLOP discussion** | https://github.com/ggml-org/llama.cpp/discussions/9699 |

### peakoss CI gate

| Resource | URL |
|----------|-----|
| **Repository** | https://github.com/peakoss/anti-slop |
| **GitHub Marketplace action** | https://github.com/marketplace/actions/anti-slop |
| **action.yaml** | https://github.com/peakoss/anti-slop/blob/main/action.yaml |
| **Releases** | https://github.com/peakoss/anti-slop/releases |
| **CHANGELOG** | https://github.com/peakoss/anti-slop/blob/main/CHANGELOG.md |
| **Coolify (reference deployment)** | https://github.com/coollabsio/coolify |

### Practitioner / critique substrate

| Resource | URL |
|----------|-----|
| **Wikipedia Signs of AI Writing** | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing |
| **blader/humanizer (prompt-pack lineage)** | https://github.com/blader/humanizer |
| **blader/humanizer issue #82 (prompt-only critique)** | https://github.com/blader/humanizer/issues/82 |
| **Peggy Kang — post-processing > prompts** | https://dev.to/peggggykang/building-an-ai-humanizer-why-we-stopped-trying-to-fix-prompts-bi9 |
| **HN thread citing antislop paper** | https://news.ycombinator.com/item?id=47007098 |
| **unslop RESEARCH_AND_TECH** | https://github.com/MohamedAbdallah-14/unslop/blob/main/docs/RESEARCH_AND_TECH.md |
| **unslop Cat. 16 synthesis** | https://github.com/MohamedAbdallah-14/unslop/blob/main/docs/research/16-github-tools-libraries/SYNTHESIS.md |

---

## ANTISLOP mechanism (technical)

### Problem definition

"Slop" = repetitive lexical patterns that degrade quality and make LLM text instantly recognizable. Not generic "bad writing" — **statistically over-represented** n-grams relative to human baselines.

### Layer 1 — Forensic detection (`auto-antislop` profiling)

```
ρ(p) = f_LLM(p) / f_human(p)
```

- Generate ~2,000 creative-writing outputs per target model (Reddit prompts, Nitral-AI 2024 corpus).
- Compare word/bigram/trigram frequencies against:
  - **wordfreq** (Speer et al. 2018) for unigrams
  - Reddit creative writing + Project Gutenberg for n-grams
- Collate highest-ρ patterns into a **model-specific slop fingerprint**.

**Example overrepresentation (gemma-3-12b, Table 1):**

| Pattern | Ratio vs human |
|---------|----------------|
| "Elara" (character name fixation) | 85,513× |
| "heart hammered ribs" | 1,192× |
| "felt profound sense" | 550× |
| "It's not X, it's Y" construction | 6.3× |

Fingerprints **cluster within model families** but differ across families → banlists should be model-specific, not universal.

### Layer 2 — Antislop Sampler (inference-time)

**Key insight:** Per-token logit biasing fails for multi-token phrases ("tapestry" may split across tokens; banning "El" kills "elastic"). The sampler waits until the **full banned string appears in the decode trace**, then:

1. Backtrack to the pattern's first token
2. Multiply initiating token probability by `10^(-10s)` where `s ∈ [0,1]` is ban-strength
3. Resample with **min-p** filtering
4. Soft-ban: allow high-probability banned patterns through when prompt explicitly requests them (e.g. "Write about tapestries")

**Prior art note:** Paech originally claimed novelty; README now acknowledges **exllamav2 `banned_strings`** uses a similar approach.

**Throughput cost (Appendix B):** 69–96% reduction with vLLM at banlist sizes 1k–8k due to backtracking frequency. Production deployments should prefer FTPO-trained weights.

**Integrations:** koboldcpp 1.76+ (native), open-webui (via OpenAI-compatible antislop API), Transformers streaming.

### Layer 3 — auto-antislop pipeline + FTPO (weight-time)

**Pipeline:**

```
Model → profile slop (ρ ratios) → build banlist
     → run Antislop Sampler on prompts → capture inference traces
     → synthesize final-token preference pairs (rejected = slop token, chosen = coherent alternatives)
     → FTPO fine-tune (LoRA, last 5 layers + lm_head, r=128–512)
     → optional: ship checkpoint (no runtime sampler needed)
```

**FTPO vs DPO:** Both can train on final-token pairs, but FTPO adds:
- Multi-chosen-token updates per step
- Margin-based preference loss with automatic gradient shutoff when margin achieved
- Split MSE regularization: target logits get freedom; non-target vocab anchored to reference

**Main results (gemma-3-12b, 1k outputs, banlists 2k/4k/8k):**

| Method | Suppression | Writing quality (100-pt rubric) | Lexical diversity |
|--------|-------------|--------------------------------|-------------------|
| Antislop Sampler | 100% | **Improves** vs baseline | Maintained |
| FTPO | 83–92% | Within 1% of baseline | 95–102% of baseline |
| DPO | 80–82% | **−6 to −15 points** | 74–92% of baseline |
| Token banning (logit −100) | Partial | **Collapses to ~28** at 8k patterns | Severe |

Cross-domain evals: GSM8K, MMLU, EQ-Bench Creative Writing — FTPO within 1–3% of baseline on reasoning benchmarks.

**Training caveat:** Llama-3.3-70B required restricting LoRA to `lm_head` only to avoid repetition; suppression dropped to ~66%.

### Evaluation methodology (limitations to note)

- Writing quality judged by **GPT-5 / Sonnet-4 to a rubric** on long multi-turn story generation — not human rater replication (authors flag this as future work).
- Primary eval prompts overlap training corpus family (Reddit creative writing) though held-out subset.
- Paper's AI Usage Disclosure: LLMs assisted early drafting; results human-designed.

---

## peakoss/anti-slop — CI gate pattern

### What it is NOT

- Does **not** scan prose for "delve" or em-dash density
- Does **not** run an LLM or stylometric classifier on diff content
- Does **not** overlap with ANTISLOP's text-generation pipeline

### What it IS

A **GitHub Action** (`peakoss/anti-slop@v0`, AGPL-3.0, author peaklabs-dev) that scores pull requests against **34 configurable rules** across:

| Category | Example checks |
|----------|----------------|
| PR branch | Blocked target branches, branch naming patterns |
| PR size | `maxChangedFiles`, `maxChangedLines` |
| Title / description | Min length, blocked terms, template compliance |
| Commits | Conventional commit enforcement, author match, blocked authors |
| Files | Blocked paths (README, LICENSE, SECURITY), extension allowlists, final newline |
| User signals | Spam username patterns, account age, daily fork rate, profile completeness, `requirePublicProfile` |
| Contributor history | Min merged PRs, merge ratio thresholds |
| Honeypots | `blocked-terms` / `blocked-issue-numbers` as deliberate AI traps |

**Failure model:** Count failed checks; when failures ≥ `max-failures` (default **4**), trigger actions: comment, label, **close PR** (default), optionally lock.

**Design philosophy (from README):**
- "Anti-slop, **not anti-AI**" — good AI-assisted PRs pass if they follow process
- Owners/Members/Collaborators exempt by default
- Derived from **130+ manually reviewed slop PRs** across large OSS projects
- Tuned on **Coolify** maintenance (~50K★, ~120 slop PRs/month)
- Runs in **<15 seconds**; v0 pre-1.0, pin version for stability

**Honeypot pattern:** Maintainers add nonsense `blocked-terms` (e.g. `"PINEAPPLE"`) or fake blocked issue numbers. AI tools that hallucinate standard PR boilerplate or scrape issue lists trip the gate — a **behavioral** slop signal, not a lexical one.

### Relation to ANTISLOP naming

Same metaphor ("slop"), different substrate. peakoss filters **contribution process slop** (drive-by README edits, template-skipping bots, spam accounts). Paech filters **generative lexical slop**. unslop filters **assistant output residue**. All three are valid; conflating them causes category errors in product positioning.

---

## vs unslop subtractive approach

### Shared philosophy: subtraction beats addition

Both ANTISLOP and unslop reject the "inject warmth / human patterns" school. ANTISLOP surgically lowers logits for overused tokens; unslop strips stock vocab, hedging stacks, sycophancy openers, and performative balance from existing text. unslop repo synthesis ([Cat. 16](docs/research/SYNTHESIS.md)): **"Subtraction beats addition."**

### Where they diverge

| Dimension | ANTISLOP | unslop |
|-----------|----------|--------|
| **Insertion point** | Token stream / model weights | Completed assistant or file text |
| **Logit access** | Required (sampler) or owns weights (FTPO) | Not required |
| **SaaS assistants** | Cannot intercept Claude/GPT/Cursor APIs | Primary use case (hooks + skills + CLI) |
| **Mechanism** | Backtracking + preference optimization on final tokens | Deterministic regex + optional LLM rewrite (`humanize.py`) |
| **Structural tells** | Indirect (via slop phrase removal) | Explicit Phase 1 burstiness (`structural.py`), Phase 5 contractions (`soul.py`), stylometry |
| **Preservation contract** | N/A (generation) | Byte-identical code/URLs/headings (`TestPreservation`) |
| **Detector evasion** | Not primary goal (quality/friction) | Measured honestly: TMR moves 0.0–0.2 pp deterministic; recommends cross-model paraphrase |
| **Banlist curation** | Auto-generated ρ ratios (+ manual curation planned) | Curated tiers in `anti-aiisms.md` from Wikipedia + practitioner corpora |
| **Scope** | Creative writing / long-form fiction eval focus | General assistant output: docs, commits, resumes, code comments |

### The "auto-antislop" split (generation vs post-generation)

README states explicitly:

> Anthropic Custom Styles sets the ceiling at generation; unslop catches residue afterwards. The ICLR 2026 Antislop paper formalizes that split.

Three-tier stack for a user who controls everything:

```
1. Custom Styles / system prompt (vendor generation-time)
2. ANTISLOP sampler or FTPO checkpoint (self-hosted generation-time)
3. unslop hook or CLI (post-generation residue)
```

For typical unslop users (Claude Code, Cursor, no local weights): **only tier 3 applies**. ANTISLOP is upstream inspiration and eval benchmark, not a runtime dependency.

### Prompt-only humanization critique — both sides agree

Engineering consensus (Peggy Kang, `blader/humanizer` #82, unslop's own architecture):

> "Prompts don't fix distributions. Rewriting does."

ANTISLOP agrees at the **distribution** level — prompts alone cannot stop "Elara" at 85,513× overrepresentation; you need sampler or weight surgery. unslop agrees at the **assistant** level — system prompts drift (RMTBench/HorizonBench >30% persona degradation by turn 8–12); deterministic post-pass + hook reinforcement is the reliable layer.

**Disagreement surface:** Whether surface regex rewriting moves **detector** scores (Adversarial Paraphrasing, NeurIPS 2025: ~<1 pp for local rewrite). ANTISLOP doesn't optimize for detectors; unslop doesn't claim detector defeat. No actual conflict.

---

## Supporters

| Camp | Position | Representative sources |
|------|----------|-------------------------|
| **LocalLLaMA / self-hosters** | Sampler is the reference fix when you control inference; shipped in koboldcpp | [koboldcpp #1141](https://github.com/LostRuins/koboldcpp/issues/1141), r/LocalLLaMA antislop-sampler announcement |
| **Academic reviewers** | ICLR 2026 acceptance; rigorous FTPO ablations vs DPO/token ban | [OpenReview](https://openreview.net/forum?id=gLcyM1khyp) |
| **Industry research labs** | Thoughtworks AI Labs wrote explainer; frames 90% slop reduction | [Thoughtworks post](https://research.thoughtworks.com/library/anti-slopping-an-innovation-for-rectifying-llm-writing-cliches) |
| **Authors / practitioners** | Paech, Roush — open MIT code, HF checkpoints, LinkedIn outreach | [Allen Roush post](https://www.linkedin.com/posts/allen-roush-27721011b_after-years-of-llms-converging-on-the-same-activity-7387167851146756098-txV0) |
| **OSS maintainers** | peakoss/anti-slop — measurable relief on high-traffic repos | Coolify maintainer experience cited in [peakoss README](https://github.com/peakoss/anti-slop) |
| **unslop repo** | Lists Antislop as top-5 inspiration; documents complementary split | [README Inspirations](https://github.com/MohamedAbdallah-14/unslop/blob/main/README.md) |
| **Creative writing community** | SillyTavern anti-slop prompts, slop-score evaluators — same banlist philosophy | Cat. 14 research compendium |

---

## Critics and limitations

| Critique | Detail | Source |
|----------|--------|--------|
| **Throughput penalty** | 69–96% tok/s loss at 1k–8k banlist; impractical for latency-sensitive prod without FTPO | Paper §7; Thoughtworks |
| **Research-grade code** | Paech warns: bugs, not optimized, minimal API, no concurrency | [antislop-sampler README](https://github.com/sam-paech/antislop-sampler) |
| **Auto banlist quality** | Default `slop_phrase_prob_adjustments.json` "mostly auto-generated… not well optimised" — roll your own | antislop-sampler README |
| **Commercial API dead end** | Requires raw logits; OpenAI/Anthropic APIs unreachable | antislop-sampler disclaimers |
| **Novelty partial walkback** | exllamav2 `banned_strings` predates; similar implementation | antislop-sampler README edit history |
| **Eval automation bias** | GPT-5/Sonnet-4 rubric, not replicated human raters | Paper §6, §7 future work |
| **Domain narrowness** | Primary eval = creative fiction / Reddit prompts; code, legal, resume slop underexplored | Paper scope |
| **peakoss false positives** | Any heuristic gate can snag legitimate new contributors if `max-failures` too low | Inherent to CI-gate design; mitigated by threshold + exemptions |
| **peakoss v0 instability** | Breaking changes expected pre-1.0 | peakoss README IMPORTANT callout |
| **HN hostility to humanizer framing** | "Machines pretending to be human…" — market skepticism toward evasion tools | Cat. 16 E-practical; distinct from ANTISLOP quality framing |
| **Banlist arms race** | New model family → new slop fingerprint; static lists stale | Paper Appendix K family clustering |
| **Pink elephant / backfire** | Paper cites Castricato et al. 2024 — forbidden concepts can amplify | Paper §2 related work |

---

## unslop as complementary (not competitive)

### Positioning statement (recommended)

**unslop is the post-generation layer in a stack ANTISLOP defines.** Paech et al. fix the model; peakoss fixes the repo; unslop fixes the assistant output you actually paste into PRs, docs, and emails. Installing unslop does not require opposing ANTISLOP — it catches what generation-time tools miss when you don't control the model.

### Concrete integration opportunities

| Opportunity | Rationale | unslop artifact |
|-------------|-----------|-----------------|
| **Export `HumanizeReport` counts** | auto-antislop profiles slop via frequency ratios; unslop already logs per-rule `Replacement` events — usable as **human-in-the-loop validation** of banlist entries | `humanize.py` `Replacement`, `HumanizeReport` |
| **Sync banlist corpora** | `anti-aiisms.md` already cites antislop-sampler corpora + Wikipedia Signs | `.cursor/skills/unslop/anti-aiisms.md` |
| **Benchmark cross-pass** | No published study compares prompt + regex vs sampler vs FTPO on same fixtures — unslop `benchmarks/` could host | `benchmarks/run.py` |
| **Document three-layer stack** | README already mentions Custom Styles + Antislop split — add peakoss as **fourth layer for maintainers** | README Engineering section |
| **Detector honesty alignment** | Both projects avoid "99% undetectable" marketing; strengthens credibility vs SaaS humanizers | README "What I deliberately don't do" |
| **ESL / false-positive defense** | unslop `/unslop anti-detector` for defensive use; ANTISLOP doesn't address institutional detectors — orthogonal | `skills/unslop/SKILL.md` Boundaries |

### What unslop should NOT claim

- Do not imply unslop replaces FTPO or antislop-sampler for local fiction writers with koboldcpp.
- Do not conflate peakoss PR heuristics with text humanization — different buyer (maintainer vs writer).
- Do not cite ANTISLOP's 90% slop reduction as unslop's number — different mechanism, different eval.

### What unslop CAN claim (evidence-backed)

- Same **subtractive** design philosophy as ICLR 2026 Antislop (remove overused patterns, don't inject fake warmth).
- Occupies the **second half** of the generation/post-generation split the paper implies.
- **Composes** with Custom Styles (generation) and optionally with self-hosted ANTISLOP for users who run both.

---

## Ecosystem map (Aug 2026)

```
                    ┌─────────────────────────────────────┐
                    │  Vendor generation-time             │
                    │  (Anthropic Custom Styles, etc.)    │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │ self-hosted only       │                        │
          ▼                        ▼                        │
┌──────────────────┐    ┌──────────────────┐               │
│ Antislop Sampler │───▶│ auto-antislop    │               │
│ (inference)      │    │ → FTPO weights   │               │
└──────────────────┘    └──────────────────┘               │
          │                        │                        │
          └────────────┬───────────┘                        │
                       ▼                                    │
              Generated text ──────────────────────────────▶│
                       │                                    │
                       ▼                                    ▼
              ┌─────────────────────────────────────────────┐
              │ unslop (hooks / CLI / skills)               │
              │ post-generation subtractive rewrite         │
              └─────────────────────┬───────────────────────┘
                                    │
                                    ▼
              ┌─────────────────────────────────────────────┐
              │ peakoss/anti-slop (optional, maintainers)    │
              │ PR metadata CI gate — not text analysis     │
              └─────────────────────────────────────────────┘
```

---

## Key numbers (verified from paper / repos)

| Claim | Value | Source |
|-------|-------|--------|
| Slop pattern overrepresentation | Up to **85,513×** ("Elara", gemma-3-12b) | Table 1, arXiv 2510.15061 |
| Sampler banlist scale | **8,000+** patterns vs token ban unusable at **~2,000** | Abstract |
| FTPO slop reduction | **~90%** (83–92% across banlist sizes) | §6.2 |
| FTPO quality delta | **<1%** vs baseline writing rubric | §6.2 |
| DPO quality delta | **−6 to −15** points at 80–82% suppression | §6.2, Fig 3 |
| Sampler throughput hit | **69–96%** (1k–8k banlist, vLLM) | §7, Thoughtworks |
| peakoss check rules | **34** checks, **57** config options | peakoss README |
| peakoss stars | **762** (Aug 2026) | GitHub |
| antislop-sampler stars | **354** | GitHub |
| auto-antislop stars | **177** | GitHub |

---

## Open questions / research gaps

1. **No head-to-head:** unslop deterministic pass vs ANTISLOP sampler vs FTPO checkpoint on identical prompts + same downstream detectors (DivEye, PHD, GPTZero).
2. **Non-fiction slop:** Resume bullets, technical docs, commit messages — unslop's domain — underrepresented in ANTISLOP evals.
3. **Cross-vendor residue:** FTPO on gemma doesn't help Claude Code output; unslop's value prop is exactly this gap.
4. **peakoss + unslop maintainer story:** Could unslop-humanized PR descriptions reduce peakoss template-failure rate? Untested.
5. **Regex ban maturity:** koboldcpp #1233 still open; ANTISLOP paper demos regex suppression but production UX lagging.

---

## BibTeX

```bibtex
@inproceedings{paech2026antislop,
  title={Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models},
  author={Paech, Samuel and Roush, Allen and Goldfeder, Judah and Shwartz-Ziv, Ravid},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2026},
  url={https://arxiv.org/abs/2510.15061}
}
```

---

## Agent manifest update

| # | Topic | Status |
|---|-------|--------|
| 33 | auto-antislop / Antislop ICLR 2026 | **done → this file** |
| 37 | peakoss/anti-slop CI gate | **covered herein** (same memo — shared "antislop" namespace) |
