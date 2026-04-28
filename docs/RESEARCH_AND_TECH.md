# Unslop — Research, Tech, and What Makes It Different

A public reference for the research, tech stack, and design choices behind this project.

Last refreshed 2026-04-28 from a five-agent audit of the codebase. Every citation in the "live" tables below has a verified arXiv URL or DOI, was confirmed against the paper's abstract, and informs at least one shipping rule, threshold, algorithm, or configuration value. Decorative or rationale-only citations are listed separately.

---

## What unslop is

A multi-platform plugin that humanizes LLM output without breaking it. It strips AI-isms — sycophancy openers, stock vocabulary (`delve`, `tapestry`, `testament`), hedging stacks (`it's important to note that`), em-dash pileups, performative balance, tricolon padding, copula avoidance, negative parallelisms — and restores the things that read human: contractions, sentence-length variance, concrete nouns, calibrated uncertainty.

Code, URLs, paths, headings, tables, and quoted examples come out byte-identical. That preservation contract is the load-bearing engineering choice.

The same skill ships across Claude Code, Cursor, Windsurf, Cline, Codex, Copilot, and Gemini through a single SSOT propagated by `scripts/sync-mirrors.sh`.

---

## What makes it different

Six anchors. None is unique on its own; the combination is.

### 1. Subtract, don't add

Removal is the design principle. Warmth, pleasantries, "I'd be happy to help" framing are deleted, not paraphrased. The reasoning is empirical: Ibrahim, Hafner & Rocher 2025 ([arXiv:2507.21919](https://arxiv.org/abs/2507.21919)) found warmth-trained models had **+11pp** higher error rate when users held false beliefs and **+12.1pp** when emotion accompanied false beliefs (avg +7.43pp across factual tasks). Adding warmth measurably lowers reliability.

### 2. Style and stance separate

Style (cadence, register, vocabulary) and stance (sycophancy, agreement, confidence) are independent axes. A humanized voice preserves disagreement, refusals, and uncertainty unchanged. SKILL.md Principle #2 makes this explicit.

### 3. Byte-exact preservation

Fenced code, indented code, YAML frontmatter, tables, blockquotes, headings, inline code, URLs, markdown links, and quoted use/mention examples are swapped to opaque placeholders before any regex touches text. Restoration is in reverse insertion order so nested structures unwrap cleanly. The validator compares each protected category byte-by-byte; any mutation is a hard error. See `unslop/scripts/humanize.py::_protect`/`_restore` and `validate.py::validate`.

This is why unslop can run on `CLAUDE.md`, source with prose comments, or technical markdown without breaking them. Commercial paraphrasers don't make this guarantee.

### 4. Detector feedback loop with an honest exit

`detector.py` loads a local AI-text detector (TMR — 125M-param RoBERTa, 99.28% AUROC on RAID), scores the rewrite, and re-humanizes with escalating intensity until probability drops below a target or the ladder exhausts. When exhausted, the module recommends cross-model paraphrase by name, citing TempParaphraser (EMNLP 2025) and Adversarial Paraphrasing (NeurIPS 2025) — and explicitly refuses to recommend watermark removal, citing EU AI Act Article 50.

### 5. DivEye as the surprisal signal

`surprisal.py` computes the canonical 10-feature DivEye signal vector (Basani, Chen et al., [arXiv:2509.18880](https://arxiv.org/abs/2509.18880), TMLR 2026): per-token surprisal mean, variance, skewness, kurtosis, ΔS mean+variance, Δ²S variance + 20-bin entropy + lag-1 autocorrelation. Default base LM is `distilgpt2` (82M params, lazy-imported). Outperforms zero-shot detectors by up to 33.2% in the original paper, robust to paraphrasing.

Two deterministic proxies (`sentence_length_cv`, `word_length_stdev`) fall back when the LM isn't loaded.

### 6. Honest limitations, in writing

`SKILL.md` states the failure modes explicitly:

- Voice-match is prompt-based, not stylometric-attribution-resistant. Catch Me If You Can? ([arXiv:2509.14543](https://arxiv.org/abs/2509.14543), EMNLP 2025) showed all six tested frontier models fail personal-style imitation; few-shot beats zero-shot 23.5×, fine-tuning wins decisively.
- Detector evasion isn't durable when the verifier has source-DB access. Krishna et al. (DIPPER, [arXiv:2303.13408](https://arxiv.org/abs/2303.13408), NeurIPS 2023): retrieval-defense recovers 80–97% of paraphrased outputs.
- All commercial humanizer bypass numbers from before August 2025 are stale. Turnitin shipped explicit "AI bypasser" detection then, retrained February 2026, FP held below 1%.

---

## What unslop deliberately doesn't do

| Thing | Who does it | Why we refuse |
|---|---|---|
| Claim "100% undetectable" | Undetectable.ai, StealthGPT, BypassGPT | DAMAGE ([arXiv:2501.03437](https://arxiv.org/abs/2501.03437), COLING 2025) measured independent bypass at 45–88% across the same tools. Marketing this creates EU AI Act Art. 50 compliance exposure. |
| Synonym-swap paraphrase | QuillBot, Spinbot | Independent audits show synonym swap is largely ineffective vs. modern detectors. |
| Invent biographical detail | Some "voice restorers" | SKILL.md Principle #4 — role-play frame, not personhood. Never invent memory or experience. |
| Ship watermark removal as a feature | Several | Side effect is acknowledged in Boundaries. EU AI Act Article 50 (effective August 2026) prohibits watermark removal as a deliberate act. |
| Help with academic misconduct | Several commercial tools' marketing | SKILL.md Boundaries: decline. Legitimate framing is ESL false-positive defense (Liang et al. 2023, [arXiv:2304.02819](https://arxiv.org/abs/2304.02819) — >50% of TOEFL essays were flagged as AI). |

---

## Research the codebase actually uses

This is the set of papers whose findings or algorithms are encoded in shipping code, a rule, or a config value. Verified URLs and abstracts. Not a complete bibliography; for the wider research compendium see `docs/research/`.

### AI text detection

| Citation | arXiv | Used for |
|---|---|---|
| **DivEye** — Basani, Chen et al. (TMLR 2026) | [2509.18880](https://arxiv.org/abs/2509.18880) | 10-feature surprisal vector in `surprisal.py`; proxies in `stylometry.py`; reference for `--surprisal-variance` |
| **Adversarial Paraphrasing** — Cheng et al. (NeurIPS 2025) | [2506.07001](https://arxiv.org/abs/2506.07001) | Ladder-exhaustion recommendation in `detector.py`; reference impl at github.com/chengez/Adversarial-Paraphrasing |
| **TempParaphraser** (EMNLP 2025, ACL Anthology 2025.emnlp-main.1607) | — | Cross-model paraphrase recommendation cited verbatim in `detector.py:393` |
| **DAMAGE** — Tulchinskii et al. (COLING 2025) | [2501.03437](https://arxiv.org/abs/2501.03437) | Justification for live detector loop in `detector.py`. The 19-tool audit. |
| **Binoculars** — Hans et al. (ICML 2024) | [2401.12070](https://arxiv.org/abs/2401.12070) | Anti-detector mode targets Binoculars-style cross-perplexity ratio |
| **Sadasivan et al.** (2023) | [2303.11156](https://arxiv.org/abs/2303.11156) | Anti-detector framing — detection degrades as LLM distributions approach human text |
| **Nicks et al.** (ICLR 2024) | — | `surprisal.py` and `detector.py` warnings: detector reading is voice-match target, not gate |
| **Chakraborty et al.** (ICML 2024) | [2304.04736](https://arxiv.org/abs/2304.04736) | Counter to Sadasivan — sample-complexity bounds for reliable detection |
| **DIPPER / Krishna et al.** (NeurIPS 2023) | [2303.13408](https://arxiv.org/abs/2303.13408) | Retrieval-defense caveat in SKILL.md — detector evasion isn't durable |
| **Liang et al.** (Patterns 2023) | [2304.02819](https://arxiv.org/abs/2304.02819) | ESL false-positive defense framing — >50% TOEFL essays flagged. The defensive wedge. |
| **AdaDetectGPT** — Zhou, Zhu, Su et al. (NeurIPS 2025) | [2510.01268](https://arxiv.org/abs/2510.01268) | First zero-shot detector with provable FPR control; named target in anti-detector mode |

### Sycophancy and warmth

| Citation | arXiv | Used for |
|---|---|---|
| **Ibrahim, Hafner & Rocher** (2025) | [2507.21919](https://arxiv.org/abs/2507.21919) | SKILL.md Principle #3 warmth-reliability tradeoff. +11pp / +12.1pp / +7.43pp deltas |
| **Sharma et al.** (Anthropic, ICLR 2024) | [2310.13548](https://arxiv.org/abs/2310.13548) | `humanize.py` SYCOPHANCY regex list; sycophancy as canonical RLHF failure mode |
| **SycEval** (AIES 2025) | [2502.08177](https://arxiv.org/abs/2502.08177) | 58.19% sycophantic agreement rate cited in SKILL.md |
| **Shapira, Benadé & Procaccia** ("How RLHF Amplifies Sycophancy", 2026) | [2602.01002](https://arxiv.org/abs/2602.01002) | Formal causal account; informs `style_memory.py` constraint to never store free-text preference strings |

### Voice, style, blandification

| Citation | arXiv | Used for |
|---|---|---|
| **Catch Me If You Can?** (EMNLP 2025) | [2509.14543](https://arxiv.org/abs/2509.14543) | voice-match Known Limitation in SKILL.md — six frontier models all fail personal-style imitation |
| **Linguistic verbal uncertainty** (2025) | [2505.23854](https://arxiv.org/abs/2505.23854) | "I think / probably / seems" rule. LVU outperforms numeric confidence by ~10% AUROC and ECE |
| **LLM revision blandification** (2026) | [2603.18161](https://arxiv.org/abs/2603.18161) | ANTI-BLANDIFICATION block in `humanize.py` LLM-mode prompt — ~70% voice neutralization under LLM revision |

### Reasoning traces

| Citation | arXiv | Used for |
|---|---|---|
| **Turpin et al.** ("LLMs Don't Always Say What They Think", NeurIPS 2023) | [2305.04388](https://arxiv.org/abs/2305.04388) | `reasoning.py` justification — published CoT can diverge from internal computation |
| **s1 / Muennighoff et al.** (EMNLP 2025) | [2501.19393](https://arxiv.org/abs/2501.19393) | Reasoning-trace stripper basis — budget forcing makes reasoning visible in the token stream |

### LLM-as-judge bias

| Citation | arXiv | Used for |
|---|---|---|
| **A Survey on LLM-as-Judge** | [2411.15594](https://arxiv.org/abs/2411.15594) | `evals/perceived_humanness.py` A/B order randomization, multi-model jury (~40% position inconsistency, ~15% verbosity inflation) |
| **CALM** (LLM Judge Order Bias) | [2410.02736](https://arxiv.org/abs/2410.02736) | Order-randomization rationale |

### Watermarking landscape

| Citation | arXiv | Used for |
|---|---|---|
| **Kirchenbauer et al.** (ICML 2023) | [2301.10226](https://arxiv.org/abs/2301.10226) | Reference watermark scheme. Rationale for noting unslop degrades watermarks as side effect, not feature |
| **SynthID** (Nature 2024, Google DeepMind) | — | Production watermarking reference; informs Boundaries note |
| **SIRA** (ICML 2025) | [2505.05190](https://arxiv.org/abs/2505.05190) | $0.88/M-token watermark removal. Cited in SKILL.md as evidence watermarking is no longer a reliable provenance defense |

### Generation diversity

| Citation | arXiv | Used for |
|---|---|---|
| **Holtzman et al.** (Nucleus sampling, ICLR 2020) | [1904.09751](https://arxiv.org/abs/1904.09751) | Burstiness-signal foundation. Likelihood maximization → bland repetitive text |
| **Antislop / Paech** (ICLR 2026) | [2510.15061](https://arxiv.org/abs/2510.15061) | Per-rule counts in `Replacement`/`HumanizeReport` as training-data signal; auto-antislop pipeline parallel |

### Memory and persona drift

| Citation | arXiv | Used for |
|---|---|---|
| **HorizonBench** — Li et al. ("Long-Horizon Personalization with Evolving Preferences", 2026) | [2604.17283](https://arxiv.org/abs/2604.17283) | Drift-check banner cadence in `hooks/unslop-mode-tracker.js` (turns 8/16/24/32) |
| **Memory Security Survey** (2026) | [2604.16548](https://arxiv.org/abs/2604.16548) | Symlink refusal, O_EXCL writes, 0o600 perms, schema validation in `style_memory.py` |
| **OWASP Top 10 for Agentic Applications** (2026) | — | Persistent-memory threat class for `style_memory.py` |
| **CHI 2026 — Condensed user profiles drive sycophancy** (Barcelona, MIT/Penn State) | — | `style_memory.py` design constraint — store only numeric signals, never free-text preferences |

### Regulatory

| Source | Used for |
|---|---|
| **EU AI Act Article 50** (Dec 2025 Code of Practice; effective Aug 2026) | SKILL.md Boundaries — watermark-removal refusal; anti-detector scoped to false-positive defense |
| **California SB 243** (effective Jan 2026) | Companion-chatbot safety context in SKILL.md regulatory note |

### Decorative citations (kept as design rationale, no concrete code artifact)

These are cited to explain *why* a design choice was made (or why a feature was excluded) but don't drive a numeric threshold or shipped algorithm:

- **TH-Bench** ([2503.08708](https://arxiv.org/abs/2503.08708)) — first systematic humanization benchmark; informs eval design
- **StealthRL** ([2602.08934](https://arxiv.org/abs/2602.08934)) — RL-based humanization against detector ensembles; transferability informs anti-detector design
- **Reinhart et al.** ("Do LLMs Write Like Humans?", PNAS 2025) — stylometric axes a humanizer should target
- **Rallapalli et al.** ([2604.14111](https://arxiv.org/abs/2604.14111)) — decoder temperature as stylistic signal; out-of-scope decoder-level lever

### Citations referenced by name without a public ID in the codebase

Listed for transparency. If you have a public link for any of these, a PR is welcome.

- **TempParaphraser** (EMNLP 2025) — ACL Anthology entry exists; arXiv preprint ID not recorded in code
- **RMTBench** — cited as a 2025 benchmark; no paper link in code
- **Epaphras & Mtenzi 2026** — verified at Aga Khan University eCommons (DOI [10.37284/ijar.9.1.4683](https://doi.org/10.37284/ijar.9.1.4683)); not on arXiv
- **CHI 2026 sycophancy-memory paper** — cited as MIT/Penn State CHI 2026 (Barcelona); arXiv ID not in code

---

## Tech stack

### Python core

- **Python**: 3.10+; CI matrix runs 3.10, 3.11, 3.12, 3.13
- **Build**: setuptools + wheel; sdist + wheel via PyPI Trusted Publisher (OIDC)
- **Runtime deps for the deterministic path**: stdlib only
- **Optional deps**:
  - `anthropic` SDK — LLM mode (lazy-imported in `humanize.py`)
  - `torch` + `transformers` + `huggingface_hub` + `safetensors` — surprisal LM, AI detectors (lazy-imported)

### Quality tooling

- **mypy** — strict mode, `python_version=3.10`, strict_optional, warn_redundant_casts, check_untyped_defs
- **ruff** — line-length 100, target-version py310, rules E/F/I/UP/B/SIM
- **pytest** + **pytest-cov** — 558 tests collected; 555 pass + 3 LLM-mode opt-in (gated on `UNSLOP_RUN_LLM_TESTS=1`)
- **TestPreservation** — the contract suite. Byte-compares each protected category between input and output. Hard-errors on any mutation.
- **`tests/verify_repo.py`** — repo integrity verifier, runs as a CI step

### Distribution

| Channel | Manifest |
|---|---|
| PyPI | `unslop` package via OIDC trusted publisher |
| Claude Code marketplace | `.claude-plugin/marketplace.json` |
| Claude Code Agents marketplace | `.agents/plugins/marketplace.json` |
| Codex CLI plugin | `plugins/unslop/.codex-plugin/plugin.json` |
| Gemini CLI extension | `gemini-extension.json` |
| Cursor IDE | `.cursor/rules/unslop.mdc` (mirror) |
| Windsurf IDE | `.windsurf/rules/unslop.md` (mirror) |
| Cline | `.clinerules/unslop.md` (mirror) |
| GitHub Copilot Chat | `.github/copilot-instructions.md` (mirror) |

### IDE integration model

Three SSOT files (`skills/unslop/SKILL.md`, `unslop/SKILL.md`, `rules/unslop-activate.md`) are propagated to ~14 mirror locations by `scripts/sync-mirrors.sh`, run by `.github/workflows/sync.yml` on push. Hand-editing a mirror is silently overwritten on next sync.

### Hooks

Four hook files in `hooks/`. CommonJS via `require()`. Communicate through a flag file at `$CLAUDE_CONFIG_DIR/.unslop-active` (falls back to `~/.claude/.unslop-active`). `hooks/package.json` pins `{"type":"commonjs"}` so hooks resolve `require()` even when an ancestor `package.json` declares `"type":"module"`.

| Hook | Role |
|---|---|
| `unslop-activate.js` | SessionStart — write flag, emit ruleset, check settings.json for statusline config |
| `unslop-mode-tracker.js` | UserPromptSubmit — slash-command + NL activation, per-turn drift reinforcement |
| `unslop-statusline.sh` / `.ps1` | Statusline badge across CLI |
| `unslop-config.js` | Shared `getDefaultMode`, `safeWriteFlag` (symlink-safe, atomic, 0600 perms), `readFlag` |

All hooks honor `CLAUDE_CONFIG_DIR`. Flag writes are symlink-safe (refuse if flag path or its immediate parent is a symlink), atomic (temp + rename), 0600.

### Sub-skills

| Skill | Trigger | Role |
|---|---|---|
| `unslop` | `/unslop` | Main humanization |
| `unslop-commit` | `/unslop-commit` | Commit messages |
| `unslop-review` | `/unslop-review` | PR review comments |
| `unslop-help` | `/unslop-help` | Quick reference card |
| `unslop-reasoning` | `/unslop-reasoning` | Strip AI-slop from reasoning traces |
| `unslop-file` | `/unslop-file <file>` | Rewrite memory/doc files preserving code/URLs/headings |

### CI

| Workflow | Trigger | Purpose |
|---|---|---|
| `ci.yml` | push/PR to main | Lint, type-check, tests on Python 3.10–3.13 matrix, Codecov upload, repo integrity verifier |
| `sync.yml` | push to main on SSOT paths | Propagate SSOT to mirrors, commit as github-actions[bot] |
| `publish.yml` | tag `unslop-v*` | Build + publish to PyPI via OIDC |
| `weekly-detector-bench.yml` | cron Mon 09:00 UTC | TMR detector regression + perceived-humanness eval; 90-day artifact retention |
| `dependabot-auto-merge.yml` | Dependabot PRs | Auto-merge patch/minor; flag majors |

### External services

| Service | Purpose |
|---|---|
| Anthropic API (`anthropic>=0.34`) | LLM mode rewriting; default `claude-sonnet-4-5`, override via `UNSLOP_MODEL` |
| Claude CLI (`claude --print`) | LLM-mode fallback when no API key. `subprocess.run`, `shell=False`, fixed argument list. |
| HuggingFace `Oxidane/tmr-ai-text-detector` | Default AI-text detector (125M RoBERTa, MIT) |
| HuggingFace `desklib/ai-text-detector-v1.01` | Optional detector (RAID top entry) |
| HuggingFace `distilgpt2` | Default surprisal/burstiness scoring LM (82M params) |
| Codecov | Coverage reporting |

### Benchmarks + evals

- `benchmarks/run.py` + `benchmarks/check_regression.py` — quality + regression
- `benchmarks/detector_bench.py` — TMR + Desklib detector resistance
- `benchmarks/diveye_comparison/` — surprisal sanity vs IBM/diveye reference impl
- `benchmarks/adversarial_paraphrasing_comparison/` — vs chengez reference impl
- `benchmarks/stylometric_baseline.py` — corpus-derived stylometric targets
- `evals/perceived_humanness.py` — LLM-judge eval, A/B randomized, multi-model jury

---

## Key engineering numbers

| Metric | Value | Source |
|---|---|---|
| AI-ism reduction (rule-counted) | **92.1%** | `benchmarks/results/latest.json` (9-fixture suite, 2026-04-28) |
| Tests | 558 collected, 555 pass + 3 LLM-mode opt-in | `pytest tests/unslop/` |
| Detector backbone (default) | TMR — 125M-param RoBERTa, **99.28% AUROC on RAID** | `unslop/scripts/detector.py:9` |
| Detector ladder | 3-step default; 5-step aggressive variant | `unslop/scripts/detector.py` |
| Em-dash hard cap | 2 per paragraph; list items treated separately | `humanize.py::_cap_em_dashes_per_paragraph` |
| Contraction-rate baseline | human ~17/1000 words; AI often 0 (empirical) | `validate.py::_contraction_rate` |
| Burstiness target σ | ≥ 6 in anti-detector mode | SKILL.md anti-detector procedure |
| Sentence-length σ reference | human mean ~8.2; GPT-4o ~4.1 | `stylometry.py:29` |
| AI_ISMS regex inventory | ~100 named patterns | `validate.py` |
| File-size cap | 500 KB | `unslop/scripts/detect.py` |

---

## Verification methodology

This document is the result of a five-agent audit run on 2026-04-28. Three audit agents collected data in parallel, then I spot-checked the highest-stakes citations directly:

- **arXiv 2509.18880 (DivEye)** — verified, matches paper title and authors.
- **arXiv 2506.07001 (Adversarial Paraphrasing)** — verified, NeurIPS 2025.
- **arXiv 2507.21919 (Ibrahim/Hafner/Rocher)** — verified, exact deltas (+11pp / +12.1pp / +7.43pp avg).
- **arXiv 2604.17283 (HorizonBench)** — verified, "Long-Horizon Personalization with Evolving Preferences."
- **arXiv 2602.01002 (Shapira/Benadé/Procaccia, "How RLHF Amplifies Sycophancy")** — verified.
- **arXiv 2510.01268 (AdaDetectGPT)** — verified, Zhou, Zhu, Su et al.
- **DOI 10.37284/ijar.9.1.4683 (Epaphras & Mtenzi)** — verified at Aga Khan University eCommons.

One previously-cited arXiv ID (2604.11687, attributed to "Kalemaj et al." for the contraction-rate threshold) was found broken — the ID resolves to an unrelated paper by Utsav Paneru. That citation was removed from `validate.py` and `soul.py`; the empirical threshold was kept with a `pending re-verification` note.

If you spot a citation that doesn't resolve, a PR is welcome.

---

## Acknowledgments

Two external sources anchor a chunk of unslop's pattern coverage:

- **Wikipedia: Signs of AI writing** ([en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)) — canonical taxonomy maintained by WikiProject AI Cleanup. The vocab clusters by year (2023-mid24, mid24-mid25, mid25+), the negative-parallelism families, the copula-avoidance rule, the promotional-register list, the outline-like-conclusion detector — all trace back to this taxonomy.
- **blader/humanizer** ([github.com/blader/humanizer](https://github.com/blader/humanizer), MIT) — peer Claude Code skill catalogs 29 patterns. The two-pass audit methodology unslop uses in LLM mode (`"What makes this obviously AI generated?"` followed by `"Now make it not obviously AI generated."`) is ported from blader's design.

The detector-loop architecture follows DAMAGE (COLING 2025) — the audit that established commercial humanizer self-reported numbers diverge from independent measurement by 20–100 points.

The deterministic-first, byte-exact-preservation architecture is unslop's own choice, not adopted from any prior tool.

---

For the wider research compendium (per-category academic + commercial summaries, gap analysis, implementation traces), see `docs/research/`.
