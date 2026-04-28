# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file covers the **whole repo** — the multi-IDE plugin, the hooks, and the
`unslop` Python package. The Python package also ships [`unslop/CHANGELOG.md`](./unslop/CHANGELOG.md)
inside its wheel; both files are kept in sync. Edit this one.

## [Unreleased]

## [0.6.2] — 2026-04-29

Docs and presentation release. No code changes; tests still 555 passed,
3 skipped.

### Added

- `docs/RESEARCH_AND_TECH.md` — public reference compendium covering 38
  verified citations across 20 research categories, full tech-stack
  inventory, and design differentiators with file:line evidence.
- README **Engineering & research** section above Architecture: links to
  `RESEARCH_AND_TECH.md`, embedded research-depth constellation visual,
  inspirations table (blader/humanizer, Antislop ICLR 2026, Adversarial
  Paraphrasing NeurIPS 2025, DivEye TMLR 2026, Liang et al. 2023), and a
  "What we deliberately don't do" list.
- README **Who this is for** 3-persona strip (Engineers / Writers /
  Researchers).
- README author byline near the footer.
- Five new PNG visual assets: `assets/hero-refresh.png`,
  `assets/research-depth.png`, `assets/social-preview.png`,
  `assets/demo.png`, `assets/statusline.png`.

### Changed

- README hero image swapped to `hero-refresh.png`; subtitle simplified.
- README jump-link bar reordered (Demo first, Research added) and TOC
  updated to match.
- README feature grid trimmed from 9 cells to 6; surprisal-variance,
  reasoning-trace sanitizer, and mode gating moved into a collapsed
  **Power-user features** details block.
- README voice-match feature card rewritten in plain English; dropped
  "stylometric" / "sycophancy-memory vector" jargon.
- README demo and statusline assets switched from SVG to PNG.

### Fixed

- README: AI-ism reduction stat corrected from `89.1 %` to `92.1 %`
  (9-fixture suite, 2026-04-28 latest run).
- README: "Six modes, one command" → "Five modes, one command" (subtle,
  balanced, full, voice-match, anti-detector).
- README: skills table no longer claims `/commit` or `/review` triggers
  the commit/review sub-skills — only `/unslop-commit` and `/unslop-review`
  match the hook regex.
- `skills/unslop/SKILL.md`: subtle-mode description aligned with
  deterministic code path. Sycophancy and hedging stacks need at least
  balanced; subtle is stock-vocab-only.
- `unslop/scripts/validate.py` + `soul.py`: removed broken arXiv
  `2604.11687` / "Kalemaj et al." citation. The ID resolves to an
  unrelated paper. Threshold kept; comment marked empirical pending
  re-verification.
- `unslop/scripts/surprisal.py`: added missing arXiv ID for the
  Chakraborty et al. ICML 2024 reference.
- `tests/unslop/test_humanize.py`: renamed shadowed `TestHumanizeFileEx`
  edge-case class to `TestHumanizeFileExEdgeCases`. The four main-path
  tests in the first class were silently dead due to Python class
  shadowing; they run again.
- 14 ruff F401/F811/F841 hits across `tests/` and `evals/measure.py`
  cleaned up.

### Removed

- `requirements-optional.txt`: dropped `scipy` (zero imports across the
  repo).
- 30+ stale benchmark result dumps (`benchmarks/results/20260421T*.json`,
  `20260426T*.json`, `llm-mode-baseline.json`) and the
  `evals/snapshots/20260419T220738Z/` snapshot. Current Apr 28 runs and
  the `baselines/` / `humanness/` subtrees remain.
- Orphan SVG assets `hero.svg`, `demo.svg`, `statusline.svg`, and
  `social-preview.svg`. PNG replacements take over.

## [0.6.1] — 2026-04-28

Tier 1 gap-fill release. Closes the four pattern families that the 0.6.0 sweep
left behind: full promotional copula avoidance, canonical negative parallelism,
extended promotional register, and outline-like conclusion detection.

### Added

- `humanize.py` `STOCK_VOCAB`: `nestled`, `(rich|deep) heritage`, and
  `steeped in (tradition|history|heritage)`.
- `humanize.py` `COPULA_AVOIDANCE`: promotional `serves/served/serve as`,
  `boasts/boasted/boasting/boast`, and `features` followed by promotional
  adjectives. Each pattern guards on the surrounding noun phrase so legit
  uses (`function serves as a callback`, `features include …`) survive.
- `humanize.py` `NEGATIVE_PARALLELISM`: canonical `Not just/only X, but Y`
  and `It's not X — it's Y` / `It's not X. It's Y.` forms (full intensity).
- `validate.py` `_count_outline_conclusions` + `outline_conclusions`
  field: detects "Despite X, Y faces (significant) challenges" closers
  and surfaces a warning.
- 25 new tests across `TestCopulaAvoidance`, `TestPromotionalRegister`,
  `TestOutlineConclusionValidator`, and `TestNegativeParallelismCanonical`.

### Changed

- `validate.py` `AI_ISMS` mirrors every new humanize.py rule so the
  residual check refuses LLM rewrites that reintroduce them.
- All public version manifests aligned at `0.6.1`.

## [0.6.0] — 2026-04-28

Feature release for the core humanization pipeline.

### Added

- Pattern coverage for curly quotes, knowledge-cutoff disclaimers, vague
  attributions, generic-positive conclusions, title-case headings, and
  repeated inline-header bullet lists.
- `anti-detector` intensity, `--no-audit`, `--detector-loop-aggressive`,
  and `--report-stylometric-gaps`.
- `unslop.scripts.lexical_targets` for deterministic stylometric target
  nudges without inventing first-person claims.
- Canonical 10-field DivEye vector output from `SurprisalReading`.
- Stylometric baseline and external comparison benchmark harnesses.

### Changed

- Expanded the stock-vocabulary table with the 2024–2026 Wikipedia /
  blader gap list.
- Detector feedback now has a five-step aggressive ladder and can record
  surprisal stdev per iteration.
- Citation and boundary notes now use the verified Ibrahim, SycEval, LVU,
  Krishna, Liang, and watermarking references.
- Public plugin/package version signals are aligned at `0.6.0`.

## [0.5.6] — 2026-04-26

Patch release for deterministic safety, CLI output correctness, and release
readiness.

### Fixed

- Prevented invalid `--stdin --diff` output from printing corrupted humanized
  text when validation fails.
- Restored `--stdin --json --quiet` machine output so quiet mode only suppresses
  chatter, not requested JSON.
- Fixed nested placeholder restoration for inline code inside protected quoted
  prose.
- Made pronoun-copula contractions more conservative so clause-final phrases
  like "Here they are" and coordinated phrases like "who I am and..." stay
  grammatical.
- Preserved closing em-dashes in parenthetical pairs before copulas, avoiding
  comma-splice output such as `, is the point`.

### Added

- Added a content guard that refuses secret-like text in LLM mode and points
  users to `--deterministic` for local-only rewrites.
- Added regression coverage for stdin diff suppression, stdin JSON output,
  nested placeholders, unsafe contractions, secret-like content, and em-dash
  parenthetical pairs.

### Changed

- Gitignored `*.reasoning.md` sidecars.
- Aligned public plugin/package version signals at `0.5.6`.
- Updated PyPI metadata to the modern SPDX license field.
- Tightened README and getting-started copy around install paths, detector
  limits, statusline state, and the `unslop-file` skill name.

## [0.5.5] — 2026-04-22

Docs-only release. No behavior change in the Python package or any of the
platform adapters. All 474 tests still pass; the benchmark and humanness
results from 0.5.4 carry over unchanged.

### Changed

- **README.md** rebuilt around a two-line Claude Code install. Other
  platforms (Cursor, Windsurf, Cline, Gemini CLI, Codex, manual hooks,
  standalone CLI) moved behind a single `<details>` block so the landing
  view stays short. Follows the structure patterns from
  `matiassingers/awesome-readme`.
- **Badge rows** reworked to the `alexandresanlim/Badges4-README.md-Profile`
  convention — `for-the-badge` style, consistent `labelColor=0B1410` and
  `color=7C9885`, brand logos on every platform badge.
- **New sections**: comparison table against Anthropic Custom Styles and
  commercial humanizer SaaS, an eight-entry FAQ covering the common
  questions (detector behavior, safety for code/legal/medical, API-key
  requirements, telemetry, origin of the name), a Mermaid architecture
  diagram, and a roadmap through v1.0.
- **GitHub alerts** (`> [!TIP]`, `> [!NOTE]`, `> [!WARNING]`) used at the
  three points where a reader most needs them: the non-technical on-ramp,
  the humanness-vs-detector disclaimer, and the warmth-reliability warning.

### Added

- **`assets/hero.svg`** — 1280×440 hero banner. Logo tile, gradient
  wordmark, three achievement pills, terminal card with before/after
  cover-letter snippet, install-command strip. XML-valid; renders as a
  static image on GitHub.
- **`assets/demo.svg`** — 1200×680 product demo. Simulated CLI run with
  pass-stamp output, counts of what got stripped, plus side-by-side
  `BEFORE` / `AFTER` panels with inline strikethrough on slop words.
- **`assets/statusline.svg`** — 1080×220 Claude Code statusline mockup
  showing the `[unslop:BALANCED]` badge in context.
- **`assets/social-preview.svg`** — 1280×640 GitHub social card at the
  OpenGraph recommended size. Upload via repo Settings → Social preview
  to replace the default star-count card.

## [0.5.4] — 2026-04-21

Quality + feature pass. Adds two closed-loop capabilities the research trace
previously listed as "partial" or "convention-enforced": a programmatic
reasoning-trace sanitizer (Cat 06 / 19) and a real DivEye surprisal-variance
reading against a small local LM (Cat 15). Also fills a hole the test suite
had been carrying since v0.5.0 — the CLI itself had no direct test coverage.
All 474 tests pass; 92.0% AI-ism reduction benchmark holds.

### Added

- **`unslop/scripts/reasoning.py`** — strips agent reasoning traces before
  humanization. Six named shapes: `<thinking>` / `<think>` / `<analysis>` /
  `<reasoning>` / `<scratchpad>` / `<plan>` XML wrappers, plus markdown
  `## Reasoning` / `## Thought Process` / `## Plan` sections. Returns a
  `ReasoningReport` with audit detail. Idempotent; empty-input safe.
- **`--strip-reasoning` CLI flag** (default off). On file mode, stripped
  content is written to `<stem>.reasoning.md` as an audit sidecar. On
  stdin, content is discarded. Humanize-file report now carries a
  `reasoning` field. Research: "reason privately, humanize publicly"
  (Turpin et al. on CoT faithfulness; s1 budget-forcing EMNLP 2025;
  Anthropic `<thinking>` convention; DeepSeek-R1 `<think>` tags).
- **`unslop/scripts/surprisal.py`** — real DivEye reading via an optional
  small causal LM (distilgpt2 by default, ~330MB). Computes per-token
  surprisal and reports mean log-prob, stdev, coefficient-of-variation,
  token count. Heavy deps (`torch`, `transformers`) import lazily;
  `SurprisalUnavailable` raised on missing deps or failed load. Cached
  per-process so second call is ~1s on CPU.
- **`--surprisal-variance` one-shot CLI command** with `--surprisal-model`
  override. Reads stdin (or a file), prints JSON, exits. `UNSLOP_SKIP_SURPRISAL=1`
  forces the unavailable path (for CI).
- **`tests/unslop/test_reasoning.py`** — 19 tests: XML wrappers, markdown
  sections, idempotency, multi-block concatenation, empty/whitespace
  safety, inline-use preservation.
- **`tests/unslop/test_surprisal.py`** — 9 unit tests + 2 end-to-end
  tests (guarded by `UNSLOP_RUN_REAL_SURPRISAL=1`). Exercises the full
  pipeline against a patched fake LM and, when opted in, verifies the
  DivEye claim (bursty prose produces higher stdev than flat prose)
  against real distilgpt2.
- **`tests/unslop/test_cli.py`** — 21 tests covering the CLI end-to-end:
  version/help, stdin deterministic mode, JSON output, diff mode,
  --strip-reasoning on stdin and file (sidecar written), --surprisal-variance
  JSON shape, file mode with/without backup, --dry-run, --output single-file
  constraint, --report requires --deterministic, missing-file handling.
  The CLI previously had zero direct coverage.
- **`tests/unslop/test_detect.py`** — 30 tests for the safety gate:
  sensitive-path detection (`.env`, SSH keys, `.pem`), extension routing,
  extensionless sniffing (shebang, null bytes, symbol density), size and
  backup-file guards. First tests for `detect.py`.

### Changed

- `humanize.HumanizeReport` now carries a `reasoning: ReasoningReport`
  field, `to_dict()` reports it under `reasoning`.
- `humanize_deterministic` and `humanize_deterministic_with_report` gain
  a `strip_reasoning: bool = False` kwarg.
- `humanize_file_ex` gains `strip_reasoning` and, when enabled with a
  non-empty result, writes the `<stem>.reasoning.md` sidecar.
- `README.md` documents both new features in the Use section.
- `CLAUDE.md` package module map now enumerates every module in
  `unslop/scripts/`, not just the original five.
- `docs/research/IMPLEMENTATION_TRACE.md` gains two new rows (real DivEye
  reading; programmatic reasoning-trace stripping). The "What research we
  are NOT using yet" section is updated: Cat 15 moves from "partial" to
  "implemented"; Cat 06 / 19 moves from "convention-enforced" to
  "partial — programmatic stripper ships; latent-CoT analysis and
  inference-time reasoning-budget control stay out of scope".

## [0.5.3] — 2026-04-21

DivEye-proxy release. Closes the Category 15 research gap from
`docs/research/IMPLEMENTATION_TRACE.md` — the project's "What research
we are NOT using yet" section previously admitted no surprisal-variance
signal. Two deterministic, LM-free proxies now ship in stylometry and
surface in the voice-match LLM prompt. No behavioral break; benchmark
holds at 92.0% AI-ism reduction.

### Added

- **`sentence_length_cv`** in `unslop/scripts/stylometry.py` `StyleProfile`:
  coefficient of variation (σ/μ) of sentence word-counts. Scale-invariant
  burstiness — a ~0.3 reading is AI-flat; 0.5–0.8 is typical human academic.
- **`word_length_stdev`** in `StyleProfile`: per-sentence mean word-length,
  σ across the document. Zipf's abbreviation law gives word-length ≈
  inverse rarity, so variance in that quantity is a cheap surrogate for
  intra-document surprisal variance (DivEye, arXiv 2509.18880, TMLR 2026).
- Voice-match LLM prompt block (`_format_voice_targets` in
  `unslop/scripts/humanize.py`) now reports `cv` and `word_length_stdev`
  as DivEye-style targets, with explicit rewrite guidance: "Higher cv
  and word-length σ both indicate bursty human rhythm — mix short and
  long sentences, mix Anglo-Saxon fragments with longer Latinate clauses."
- Six new unit tests in `tests/unslop/test_stylometry.py::TestDivEyeProxies`
  covering uniform/bursty/scale-invariance/monotone/mixed-register/empty.

### Changed

- `docs/research/IMPLEMENTATION_TRACE.md`: new row mapping DivEye
  research → `sentence_length_cv` + `word_length_stdev` → tests; the
  Category 15 entry under "What research we are NOT using yet" now
  reads "partial" and names what is still out of scope (a real local-LM
  surprisal reading).

## [0.5.2] — 2026-04-21

CI hot-fix. No functional change; re-tag of 0.5.1 with a mypy config
correction so the Tests workflow stays green in matrix rows that do
not install the optional detector stack.

### Fixed

- `unslop/pyproject.toml`: `tool.mypy.overrides` now lists `torch`,
  `torch.nn`, `torch.nn.functional`, `transformers`, `huggingface_hub`,
  `safetensors`, `safetensors.torch` alongside `anthropic` under
  `ignore_missing_imports = true`. These are lazy-loaded runtime
  dependencies of `unslop/scripts/detector.py` and
  `unslop/scripts/fetch_detectors.py`; CI runners without the heavy
  detector stack were failing strict mypy with `import-not-found` on
  each of the four Python versions in the matrix.

## [0.5.1] — 2026-04-21

Research sync release. Follows the April 2026 update to
`docs/research/` (20 categories refreshed, 20 new synthesis files, 14
implementation-trace rows added) and ports the new findings into code,
rules, and documentation. No behavioral break: every previously working
CLI flag, hook, and skill still works identically. AI-ism reduction at
balanced moves from 89.1% to **92.0%** on the nine-fixture benchmark.

### Added

- **Persona-drift reinforcement** in `hooks/unslop-mode-tracker.js`. A
  per-session turn counter at `$CLAUDE_CONFIG_DIR/.unslop-turn-count`
  (symlink-safe, size-capped, whitelist-validated) fires an expanded
  drift-check banner at turns 8, 16, 24, 32, then every 16 turns
  thereafter. Calibrated against RMTBench (>30% persona degradation at
  turns 8–12) and HorizonBench (arXiv 2604.17283, Apr 2026).
  `hooks/unslop-activate.js` resets the counter on session start, and
  "stop unslop" also clears it. Three new integration tests in
  `tests/test_hooks.py` lock the turn-8 banner, the session-start reset,
  and the stop-phrase reset.
- **AI-ism vocabulary expansion** in `unslop/scripts/humanize.py`
  `STOCK_VOCAB` and `unslop/scripts/validate.py` `AI_ISMS`: `meticulous(ly)`,
  `bustling`, `paradigm shift`, `game-changer/changing`,
  `revolutionize(s/d/ing)`, `transformative`, `unprecedented` in
  connective-adjective contexts, `a myriad of` / `myriad`,
  `a plethora of`, `uncharted territory/waters/ground/area/domain`,
  `nuanced` as connective filler, `synergy/synergies/synergize(s/d/ing)`.
  Each has a corresponding validator pattern so a rewrite cannot silently
  reintroduce them. Six new tests cover the rewrites, including the
  factual-context guard for `unprecedented` (e.g. "unprecedented drought"
  survives; "unprecedented opportunity" does not).
- **LLM-as-judge bias mitigations** in `evals/perceived_humanness.py`.
  `--judges` accepts a comma-separated multi-model jury (Claude + OpenAI)
  to counter self-enhancement bias; `--counterbalance` (default on)
  runs each fixture in both A/B orientations to average out position bias
  (~40% position inconsistency baseline per arXiv 2411.15594);
  `length_delta_chars` is tracked and reported to surface verbosity
  inflation (~15% per arXiv 2410.02736); per-judge win rates are broken
  out in the summary. Four new tests cover counterbalancing, multi-judge
  juries, all-judges-unavailable, and bias-note reporting.
- **Detector-feedback ladder exhaustion recommendation** in
  `unslop/scripts/detector.py`. When the escalation ladder (balanced →
  full → full+structural+soul) can't reach the target AI probability,
  `reason_stopped` now prints a structured cross-model-paraphrase
  recommendation, names TempParaphraser (EMNLP 2025) and Adversarial
  Paraphrasing (NeurIPS 2025) as the research basis, and explicitly warns
  against watermark removal (EU AI Act Article 50).
- **Style-memory security hardening** in `unslop/scripts/style_memory.py`.
  File-size cap at 64 KB on load (StyleProfile JSON is ~1 KB; anything
  larger is either corrupt or adversarial). Expanded module docstring
  documents the OWASP Top 10 for Agentic Applications 2026 memory-risk
  class (InjecMEM, memory control flow, semantic drift), and cites MIT /
  Penn State CHI 2026 for the sycophancy × memory link that drives the
  design constraint of persisting only numerically measured signals (no
  free-text preferences).
- **Commercial humanizer tool coverage** in README's detector section:
  names Ryter Pro, Walter Writes AI, and GPTHuman.ai alongside the
  existing list; cites Turnitin's August 2025 anti-humanizer update and
  Chicago Booth 2026's audit of twelve services (median ~6-point drop
  vs. claimed 40+). README also positions Anthropic Custom Styles (Nov
  2025) and OpenAI's style-steering as the real first-party comparison,
  and references Antislop (ICLR 2026) as the learned per-pattern framework
  this repo implements.
- **SKILL anti-detector step 7**: "re-anchor after long contexts". Cites
  RMTBench and HorizonBench directly and lists the re-anchor checklist
  so agents that miss the hook output still self-correct.
- **IMPLEMENTATION_TRACE.md rows** for every change above, each linking
  the research file, the code location, and (where applicable) the tests.
- **Benchmark baseline** `benchmarks/results/baselines/post-v050-vocab-expansion-20260421.json`
  pinned at 92.0% reduction.

### Fixed

- Type-check failures in `unslop/scripts/structural.py` (`_SplitCandidate`
  now uses `collections.abc.Callable` instead of a string literal) and
  `unslop/scripts/detector.py` (explicit `str()` cast on `tokenizer.decode()`
  results to satisfy mypy's inferred `str | list[str]` union).
- Lint failures (ruff) across `unslop/scripts` and `benchmarks` from
  earlier mixed-ordering imports and redundant `__future__` annotations.
  `ruff check unslop/scripts benchmarks` and `mypy --config-file unslop/pyproject.toml unslop/scripts` both clean.

### Changed

- `evals/perceived_humanness.py` `--judge-model` is deprecated in favor
  of `--judges`. Backward compatibility is retained for the duration of
  the 0.5.x line; a deprecation warning points to the new flag.
- `tests/unslop/test_perceived_humanness.py` migrated to the new API;
  tests that assert exact vote counts now pass `counterbalance=False`
  to keep the prior one-vote-per-fixture accounting.

## [0.5.0] — 2026-04-21

Humanizer overhaul. Nine-phase plan from the "best open source humanizer"
goal shipped. Headline: **100% blind LLM-judge humanness win rate** on a
7-fixture benchmark (Claude Sonnet 4.5 compares unslop rewrite vs original,
no side metadata). AI-ism reduction at balanced is 89.1% (was 88.0%).

Honest note on detector resistance: deterministic surface rewriting moves
TMR detector scores by <0.5 pp across all tested fixtures. unslop is a
polish tool, not a detector-defeat tool. Cross-model paraphrase remains the
only strong lever and must be executed by the user. See README.

### Added

- **Phase 1 structural rewriter** (`unslop/scripts/structural.py`). Shape-aware
  sentence-length rebalancer: splits overlong sentences at safe boundaries
  (`;`, `, but `, `, and then `, `, so `, `, while `, `, however, `, em-dash)
  when the paragraph's sentence-length σ sits below 5. Flat paragraphs use
  a 20-word cutoff; varied paragraphs use 30. Parallel-bullet-soup merger
  collapses ≥3 short bullets sharing a first word into one sentence. Gated
  behind a new `--structural` flag. 23 new tests.
- **Phase 2 six new lexical families** (mirrored into `validate.py` AI_ISMS):
  SIGNIFICANCE_INFLATION, NOTABILITY_NAMEDROPPING, SUPERFICIAL_ING (full
  only), COPULA_AVOIDANCE, plus validator-only FALSE_RANGES and
  SYNONYM_CYCLING. Source taxonomy: Wikipedia "Signs of AI writing" +
  blader/humanizer. 24 new tests.
- **Phase 3 live detector feedback loop** (`unslop/scripts/detector.py`).
  Lazy-loads TMR (default, ~500MB) or Desklib (~1.5GB) from HuggingFace.
  `feedback_loop(text, ...)` escalates humanize settings until the detector
  score drops below target or the ladder is exhausted.
  `--detector-feedback` CLI flag. `unslop/scripts/fetch_detectors.py`
  bootstrap. 12 new tests.
- **Phase 4 stylometry module** (`unslop/scripts/stylometry.py`).
  Deterministic 17-signal profile: sentence-length μ/σ, fragment rate,
  contraction rate, em-dash / semicolon / colon / parenthetical rates,
  type-token ratio, comma-per-sentence, Latinate ratio, first- and
  second-person rates, approximate passive-voice rate, And/But-opener
  rate. `StyleProfile.delta(other)` for voice-match deltas. 22 new tests.
- **Phase 5 soul injection** (`unslop/scripts/soul.py`). 18 auxiliary-
  negation contractions + 12 copula contractions with allow-listed
  follow-ons to avoid possessive-fronting ambiguity. `--soul` CLI flag.
  23 new tests.
- **Phase 6 perceived-humanness benchmark** (`evals/perceived_humanness.py`).
  Blind LLM-as-judge preference harness. Claude Sonnet 4.5 compares each
  unslop rewrite against the original without side metadata; randomized
  A/B; aggregates win rate. First-pass result: 100% (7/7) humanized wins.
  11 new tests (judge calls mocked).
- **`benchmarks/check_regression.py`** — compares latest run against pinned
  baseline; fails on >2pp drop in AI-ism reduction, >+2 flat-paragraph rise,
  or preservation break.
- **`.github/workflows/weekly-detector-bench.yml`** — cron-Monday-09:00
  detector + humanness regression; artifacts uploaded; nothing auto-committed.

### Changed

- `balanced` and `full` intensities now include Phase 1 structural and
  Phase 5 soul passes by default. Old behavior available via
  `--no-structural` and `--no-soul`. `subtle` unchanged (lexical only).
  Motivation: Phase 6 benchmark showed 100% blind-judge win rate with the
  new defaults.
- `HumanizeReport` gains `structural: StructuralReport` and
  `soul: SoulReport` sub-dataclasses with per-pass counts.
- `ValidationResult` gains `flat_paragraphs_before/after`,
  `false_ranges_before/after`, `synonym_cycling_before/after`.
- CLI `--structural` and `--soul` are now `BooleanOptionalAction`
  (supports `--no-structural` / `--no-soul`).
- README updated to lead with the 100% humanness result, flag the
  detector-resistance limits (deterministic rewriting moves TMR by
  <0.5pp across all tested fixtures), and document the new mode gating.

### Fixed

- `merge_bullet_soup` treated protected-region placeholders (inline code,
  URLs, quoted prose) as a shared first word. A 4-bullet list of inline-code
  entries was collapsing to one line. Breaks run-scan on placeholder prefix
  now; the fixed empty-run advance guarantees every line gets emitted.

### Added (continued)

- **Phase 4 wire-in**: voice-match mode now accepts `--voice-sample PATH`.
  The LLM prompt receives explicit numeric targets extracted from the
  sample: sentence-length μ/σ, fragment rate, contraction rate, em-dash /
  semicolon / colon / parenthetical rates, first/second-person rates, And/
  But-opener fraction, Latinate-suffix ratio. Short samples (<50 words)
  get rough guidance instead.
- **Phase 7 `unslop-reasoning` sub-skill** (`skills/unslop-reasoning/
  SKILL.md`). Catalogs six AI-slop reasoning patterns absent from the
  prose-focused catalog: restating the question, over-hedging the plan,
  over-decomposing, infinite-loop rationalization, performative
  exhaustiveness, unmotivated confidence-then-retraction. Targets chain-
  of-thought / extended-thinking output, not final answers. Added to
  `scripts/sync-mirrors.sh` and the help card.
- **Phase 8 style memory** (`unslop/scripts/style_memory.py`). Persists
  a measured StyleProfile so voice-match stops requiring the sample on
  every invocation. Storage: `$UNSLOP_STYLE_MEMORY` → `$XDG_CONFIG_HOME/
  unslop/style-memory.json` → platform default. Mode 0600, symlink-
  refused, atomic write, schema-versioned. CLI:
  `--save-voice-profile PATH`, `--clear-voice-profile`, `--voice-memory`.
  16 new tests.
- `humanize_llm` / `humanize_file_ex` / `_build_humanize_prompt` accept
  `voice_profile: StyleProfile` alongside `voice_sample: str`. Profile-
  only is the memory-driven path; sample-text takes precedence.

## [0.4.1] — 2026-04-20

### Added
- Root-level `CHANGELOG.md`, `SECURITY.md`, `.github/dependabot.yml`,
  `.github/PULL_REQUEST_TEMPLATE.md`, `.github/FUNDING.yml`. Brings the repo
  in line with conventional GitHub project layout used by
  `davila7/claude-code-templates`, `obra/superpowers`, `cline/cline`,
  and `anthropics/claude-code`.
- Status badges in `README.md` (CI, Codecov, PyPI, Python versions, license).
- `evals/snapshots/<timestamp>/` baseline (3 prompts, sonnet-4-5 via local
  CLI fallback) so future PRs can be diffed against a real reference.
- `evals/plot.py` — grouped bar chart of AI-isms per prompt × condition
  (optional `plotly` + `kaleido` deps).
- `hooks/README.md` data-flow diagram (SessionStart → flag file →
  statusline reader).
- `CLAUDE.md` "README is a product artifact" section codifying README
  maintenance rules.
- Codecov upload step in CI with explicit token.
- Dependabot auto-merge workflow for patch + minor updates (major bumps
  still require manual review).

### Fixed
- All repo URL references corrected to `MohamedAbdallah-14/unslop` across
  13 files (was a mix of `juliusbrussee`, `MohamedAbdallah-Hu`, `MAbdallah14`).
- mypy now finds the strict config + `[[tool.mypy.overrides]]` for the
  optional `anthropic` dep — CI was running mypy with defaults from repo
  root and failing on missing-stub errors.
- `tests/ai_detector_test.py` uses `pytest.importorskip` for its heavy ML
  deps so CI without `torch`/`transformers` skips cleanly instead of failing
  collection.

### Changed
- All GitHub Actions bumped to v6 (`actions/checkout`, `actions/setup-python`,
  `actions/setup-node`, `codecov/codecov-action`). Silences the Node.js 20
  deprecation warning.
- Dev dep floors bumped to current latest: `pytest>=9`, `pytest-cov>=7`,
  `ruff>=0.15`, `mypy>=1.20`.
- `Dockerfile` default `PYTHON_VERSION` bumped from 3.12 to 3.13 (matches
  the highest version in the CI matrix).

## [0.4.0] — 2026-04-19

Major release driven by a comparative study against `humanizr/Unslop` (Unslop.Net,
a .NET inflection/formatting library) and `blader/unslop` (a Claude-Code
humanization skill). Goal: out-humanize both by importing what each does well.

### Added

#### New AI-ism pattern categories

- **Expanded stock vocab** (`STOCK_VOCAB`): `interplay`, `intricate`, `vibrant`,
  figurative `underscore(s)/d/ing`, `crucial`, `vital` (role/importance/part),
  `ever-evolving`, `ever-changing`, `in today's (digital) world/age/landscape/era`,
  `dynamic landscape`. Sourced from `blader/unslop` #5 and
  `Wikipedia:Signs_of_AI_writing`.
- **Authority tropes** (`AUTHORITY_TROPES`): persuasive framings like
  `At its core`, `In reality`, `Fundamentally`, `What really matters is`,
  `The heart of the matter is`, `At the heart of X is/lies`. Stripped only at
  sentence start where the tell is strongest.
- **Signposting announcements** (`SIGNPOSTING`): meta-commentary that announces
  the writing instead of doing it: `Let's dive in(to ...)`, `Let's break this
  down`, `Here's what you need to know`, `Without further ado`, `In this
  article, I'll ...`, `Buckle up`.
- **Filler phrases** (`FILLER_PHRASES`, `full` intensity only): `in order to`,
  `due to the fact that`, `in spite of the fact that`, `a wide variety of`,
  `a significant/substantial amount of`, `at this point in time`,
  `for all intents and purposes`, `in the event that`, `with regard to`,
  `prior to`, `subsequent to`, `the fact that`.
- **Negative-parallelism tricolons** (`NEGATIVE_PARALLELISM`, `full` intensity
  only): rhetorical tricolons like `No guesswork, no bloat, no surprises.`

#### Intensity levels (subtle / balanced / full)

- Explicit `intensity` parameter on `humanize_deterministic` and
  `humanize_deterministic_with_report`. Previously every rule ran every time;
  now the rule set is gated per intensity.
  - `subtle` — stock vocab only.
  - `balanced` (default) — sycophancy, hedging openers, transition tics, stock
    vocab, authority tropes, signposting, performative balance, em-dash cap.
  - `full` — balanced + filler phrases + negative-parallelism knockouts.
- LLM mode also branches prompt guidance by intensity (see
  `_INTENSITY_PROMPT_GUIDANCE`).

#### Audit trail

- New `Replacement` and `HumanizeReport` dataclasses. Every deterministic edit
  is recorded as `(rule, pattern, before, after)`.
- `humanize_deterministic_with_report(text, *, intensity) -> (str, HumanizeReport)`
  returns both the humanized text and the audit trail.
- `HumanizeReport.counts_by_rule` + `HumanizeReport.to_dict()` for
  machine-readable reporting.
- Tracks `em_dashes_before` / `em_dashes_after` to surface paragraph-cap
  effectiveness.

#### CLI (rewritten with `argparse`)

| Flag               | Behavior                                                             |
| ------------------ | -------------------------------------------------------------------- |
| `--version`        | Print `unslop <version>` from the single-source `__version__`.       |
| `-m / --mode`      | Choose intensity: `subtle`, `balanced`, `full`. Default `balanced`.  |
| `--stdin`          | Read from stdin, write to stdout. Forces `--no-backup`.              |
| `-o / --output`    | Write humanized text to a named file instead of overwriting input.   |
| `--diff`           | Print unified diff to stdout; implies `--dry-run`.                   |
| `--dry-run`        | Validate and report but do not write to disk.                        |
| `--no-backup`      | Skip the `<stem>.original.md` backup.                                |
| `--json`           | Emit machine-readable JSON per file.                                 |
| `--report PATH`    | Write full replacement audit trail as JSON (requires deterministic). |
| `-q / --quiet`     | Suppress progress lines.                                             |
| Multi-file / batch | `unslop a.md b.md c.md` is supported.                                |

Exit codes: `0` success, `1` usage / file-not-found / sensitive path,
`2` validation failure, `3` partial-success batch.

#### Packaging / typing / distribution

- `scripts/py.typed` marker so downstream type-checkers see the package as typed.
- `[tool.mypy]` strict config in `pyproject.toml`, enforced in CI.
- `[tool.ruff]` config (`E`, `F`, `I`, `UP`, `B`, `SIM`), enforced in CI.
- `[project.optional-dependencies]` `dev = [pytest, ruff, mypy]` and
  `llm = [anthropic]`.
- Single-source version: `__version__` in `scripts/__init__.py`, read
  dynamically by `pyproject.toml` (`dynamic = ["version"]`).
- Classifier `Typing :: Typed` added.
- Python support window bumped to `>= 3.10` (previously inconsistent).
- `Dockerfile` (two-stage, non-root user, optional `INSTALL_LLM=1` build arg).
- `.github/workflows/publish.yml` — PyPI trusted-publisher workflow on
  `unslop-v*` tag with version/tag consistency check.
- `.github/release.yml` — GitHub auto-generated release notes categories
  (Breaking / Features / Pattern rules / CLI / Validation + benchmarks /
  Bug fixes / Docs / Internal).

#### Benchmarks + detector eval

- `benchmarks/run.py --all-intensities --strict` — runs the full matrix and
  enforces monotonicity (`subtle ≤ balanced ≤ full`). Current baseline on
  4 fixtures, 148 AI-isms:

  | intensity | after | % reduction |
  | --------- | ----- | ----------- |
  | subtle    | 55    | 62.8%       |
  | balanced  | 18    | 87.8%       |
  | full      | 13    | 91.2%       |

- New fixtures `ai-slop-new-categories.md` and `ai-slop-expanded-categories.md`
  exercise authority tropes, signposting, filler phrases, negative-parallelism
  tricolons, and the expanded stock vocab.
- `benchmarks/detector_bench.py` — opt-in AI-detector harness running TMR
  (`Oxidane/tmr-ai-text-detector`, 99.28% AUROC on RAID) and Desklib v1.01
  (`desklib/ai-text-detector-v1.01`, DeBERTa-v3-large). Surfaces the honest
  finding that deterministic rule-stripping alone moves the TMR probability by
  0.1–0.2 pp. See `benchmarks/README.md`.

#### CI

- `.github/workflows/ci.yml` runs ruff, mypy (strict), pytest, `verify_repo.py`,
  and both benchmark gates (default + monotonicity matrix) across Python 3.10 /
  3.11 / 3.12 / 3.13.

#### Validator

- `ValidationResult.to_dict()` for JSON emission.
- New `AI_ISMS` patterns mirror every new category above so validation scores
  stay honest.

### Changed

- `humanize_file` now delegates to `humanize_file_ex`, which returns a
  `HumanizeOutcome` carrying `(ok, original, humanized, validation, report,
  attempts, error)`. Back-compat is preserved: the legacy signature still
  returns a `bool`.
- `_build_humanize_prompt` accepts `intensity` and injects category-specific
  guidance.
- CLI `--report` now refuses non-deterministic mode (LLM mode cannot produce
  byte-level audit trails).

### Reference

- Full study + gap analysis: `docs/research/IMPLEMENTATION_TRACE.md`.
- Wikipedia: *Signs of AI writing* — the canonical public taxonomy we
  cross-referenced.
- `blader/unslop` — the Claude-Code humanize skill whose "30 tells" list
  inspired several new categories.

## [0.3.0] and earlier

See git history. No formal changelog before 0.4.0.

[Unreleased]: https://github.com/MohamedAbdallah-14/unslop/compare/unslop-v0.4.0...HEAD
[0.4.0]: https://github.com/MohamedAbdallah-14/unslop/releases/tag/unslop-v0.4.0
