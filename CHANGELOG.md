# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file covers the **whole repo** — the multi-IDE plugin, the hooks, and the
`unslop` Python package. The Python package also ships [`unslop/CHANGELOG.md`](./unslop/CHANGELOG.md)
inside its wheel; both files are kept in sync. Edit this one.

## [Unreleased]

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
