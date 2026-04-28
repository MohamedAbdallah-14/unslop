## Unreleased

## 0.6.2 — 2026-04-29

Docs and presentation release. No code changes; tests still 555 passed,
3 skipped.

### Fixed

- README and `skills/unslop/SKILL.md` corrections: AI-ism reduction stat
  (89.1 → 92.1), mode count ("Six" → "Five"), skills-table triggers
  (drop `/commit` and `/review`; only the `/unslop-*` forms match), and
  subtle-mode description alignment with deterministic code.
- `validate.py` + `soul.py`: removed broken `arXiv 2604.11687` /
  "Kalemaj et al." citation; the ID resolves to an unrelated paper.
  Empirical contraction-rate threshold kept.
- `surprisal.py`: added missing arXiv ID for the Chakraborty et al.
  ICML 2024 reference.
- `tests/unslop/test_humanize.py`: renamed shadowed `TestHumanizeFileEx`
  edge-case class. Four previously-dead main-path tests run again.
- 14 ruff F401/F811/F841 hits cleaned up across `tests/` and
  `evals/measure.py`.

### Removed

- `scipy` from `requirements-optional.txt` (zero imports).
- 30+ stale benchmark result dumps and the
  `evals/snapshots/20260419T220738Z/` snapshot.

## 0.6.1 — 2026-04-28

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

## 0.6.0 — 2026-04-28

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

## 0.5.6 — 2026-04-26

Patch release for deterministic safety, CLI output correctness, and release
readiness.

### Fixed

- Invalid `--stdin --diff` output no longer prints corrupted humanized text
  when validation fails.
- `--stdin --json --quiet` now still emits the requested JSON report.
- Inline code inside protected quoted prose restores correctly.
- Unsafe clause-final contractions stay full-form English.
- Parenthetical em-dash pairs before copulas no longer collapse into comma
  splices.

### Added

- LLM mode now refuses secret-like content and points users to
  `--deterministic` for local-only rewrites.
- Regression tests cover stdin output, nested placeholders, unsafe
  contractions, secret-like content, and em-dash parentheticals.

### Changed

- `*.reasoning.md` sidecars are gitignored.
- Public plugin/package version signals are aligned at `0.5.6`.
- PyPI metadata now uses the modern SPDX license field.

## 0.5.5 — 2026-04-22

Docs-only release. No behavior change in the Python package. Benchmark
and humanness numbers from 0.5.4 carry over; all 474 tests still pass.

### Changed

- Repo README rebuilt around a two-line Claude Code install, with other
  platforms collapsed. Badge rows now follow the Badges4-README
  convention. New sections: comparison table, FAQ, Mermaid architecture
  diagram, roadmap.

### Added

- `assets/hero.svg`, `assets/demo.svg`, `assets/statusline.svg`,
  `assets/social-preview.svg` — four XML-valid SVG assets that ship with
  the repo (not the wheel).

## 0.5.4 — 2026-04-21

Quality + feature pass. Closes two research gaps previously marked partial:
a reasoning-trace sanitizer (Cat 06 / 19) and a real DivEye surprisal-variance
reading against a small local LM (Cat 15). Fills the CLI test-coverage hole
carried since v0.5.0. All 474 tests pass; 92.0% AI-ism reduction holds.

### Added

- `unslop.scripts.reasoning.strip_reasoning_traces()` — strips six shapes
  of agent reasoning traces (`<thinking>`, `<think>`, `<analysis>`,
  `<reasoning>`, `<scratchpad>`, `<plan>`, plus markdown `## Reasoning`
  sections). Returns a `ReasoningReport` audit trail.
- `unslop --strip-reasoning` CLI flag (opt-in). File mode writes stripped
  content to `<stem>.reasoning.md`; stdin mode discards it.
- `unslop.scripts.surprisal.compute_surprisal_variance()` — real DivEye
  reading via an optional small causal LM (distilgpt2 default, ~330MB).
  Lazy deps (`torch`, `transformers`). `SurprisalUnavailable` on missing
  deps. Cached per-process.
- `unslop --surprisal-variance` one-shot CLI command with
  `--surprisal-model` override. `UNSLOP_SKIP_SURPRISAL=1` forces unavailable.
- `HumanizeReport.reasoning` field and `strip_reasoning` kwarg on
  `humanize_deterministic`, `humanize_deterministic_with_report`, and
  `humanize_file_ex`.
- First direct CLI tests (`tests/unslop/test_cli.py`, 21 cases).
- First tests for `detect.py` (`tests/unslop/test_detect.py`, 30 cases).
- Reasoning-trace and surprisal tests (19 + 9).

### Changed

- `README.md` documents both new features in the Use section.
- `CLAUDE.md` module map enumerates every module in `unslop/scripts/`.
- `docs/research/IMPLEMENTATION_TRACE.md` gains two new rows; Cat 15
  moves from "partial" to "implemented"; Cat 06 / 19 moves from
  "convention-enforced" to "partial".

## 0.5.3 — 2026-04-21

DivEye-proxy release. Two deterministic, LM-free proxies for
intra-document surprisal variance — `sentence_length_cv` (coefficient
of variation) and `word_length_stdev` (per-sentence mean word-length σ)
— now ship in `unslop.scripts.stylometry.StyleProfile` and surface in
the voice-match LLM prompt. Closes the Category 15 gap in
`docs/research/IMPLEMENTATION_TRACE.md`. No behavioral break; six new
unit tests; 92.0% AI-ism reduction on the nine-fixture benchmark holds.

## 0.5.2 — 2026-04-21

CI hot-fix. No functional change; re-tag of 0.5.1 with a mypy config
correction. `tool.mypy.overrides` in `unslop/pyproject.toml` now covers
the lazy-loaded detector stack (`torch`, `transformers`, `huggingface_hub`,
`safetensors`) so strict mypy passes in CI matrix rows that do not install
those optional dependencies.

## 0.5.1 — 2026-04-21

Research-sync release. Ports the April 2026 update of `docs/research/`
(20 categories) into code, rules, and docs. No behavioral break. AI-ism
reduction at balanced moves from 89.1% to **92.0%** on the nine-fixture
benchmark.

### Added

- Persona-drift reinforcement hook (`hooks/unslop-mode-tracker.js`): per-session
  turn counter fires an expanded drift-check banner at turns 8, 16, 24, 32,
  then every 16 turns thereafter. Calibrated against RMTBench and
  HorizonBench (arXiv 2604.17283). Counter resets on session start and on
  "stop unslop". Three new integration tests.
- AI-ism vocabulary expansion in `STOCK_VOCAB` + `AI_ISMS`: `meticulous(ly)`,
  `bustling`, `paradigm shift`, `game-changer/changing`, `revolutionize`,
  `transformative`, `unprecedented` (connective-adjective context only),
  `myriad`, `plethora`, `uncharted territory/waters/ground/area/domain`,
  `nuanced` (as connective filler), `synergy/synergies/synergize`. Six new
  tests including a factual-context guard for `unprecedented`.
- LLM-as-judge bias mitigations in `evals/perceived_humanness.py`:
  `--judges` comma-separated multi-model jury (Claude + OpenAI),
  `--counterbalance` flag (default on) for position-bias averaging,
  `length_delta_chars` tracking for verbosity-bias audit, per-judge win
  rates in summary. Four new tests.
- Detector-feedback ladder exhaustion now prints a structured cross-model
  paraphrase recommendation naming TempParaphraser (EMNLP 2025) and
  Adversarial Paraphrasing (NeurIPS 2025), with an explicit warning
  against watermark removal (EU AI Act Article 50).
- Style-memory security hardening: 64 KB file-size cap on load, expanded
  docstring documenting the OWASP Top 10 for Agentic Applications 2026
  memory-risk class and the MIT/Penn State CHI 2026 sycophancy × memory
  finding.

### Fixed

- Static-typing failures in `structural.py` (`Callable` annotation) and
  `detector.py` (explicit `str()` on `tokenizer.decode()` results).

### Changed

- `--judge-model` deprecated in favor of `--judges` (backward compatible
  through the 0.5.x line).

For the full repo-level changelog (hooks, skill, docs, benchmarks,
IMPLEMENTATION_TRACE rows, commercial-humanizer landscape, etc.) see
[`/CHANGELOG.md`](../CHANGELOG.md) at the repo root.

## 0.4.1 — 2026-04-20

Pure infrastructure / packaging release. No runtime changes — all behavior
identical to 0.4.0.

### Fixed
- `pyproject.toml` URLs (Homepage, Issues, Source, Changelog) now point to
  the live `MohamedAbdallah-14/unslop` repo (was `MohamedAbdallah-Hu`).
- `[[tool.mypy.overrides]]` for the optional `anthropic` import — type
  checking no longer requires the SDK to be installed.

### Changed
- Dev extra floors: `pytest>=9`, `pytest-cov>=7`, `ruff>=0.15`, `mypy>=1.20`.
- New `pytest-cov` dependency in the dev extra (CI now reports coverage).

For the full repo-level changelog (CI, docs, hooks, eval baseline,
caveman-parity polish, etc.) see [`/CHANGELOG.md`](../CHANGELOG.md) at the
repo root.

## 0.4.0 — 2026-04-19

Major release driven by a comparative study against `humanizr/Unslop` (Unslop.Net, a .NET inflection/formatting library) and `blader/unslop` (a Claude-Code humanization skill). The goal: out-humanize both by importing what each does well.

### Added

#### New AI-ism pattern categories

- **Expanded stock vocab** (`STOCK_VOCAB`): `interplay`, `intricate`, `vibrant`, figurative `underscore(s)/d/ing`, `crucial`, `vital` (role/importance/part), `ever-evolving`, `ever-changing`, `in today's (digital) world/age/landscape/era`, `dynamic landscape`. Sourced from `blader/unslop` #5 and `Wikipedia:Signs_of_AI_writing`.
- **Authority tropes** (`AUTHORITY_TROPES`): persuasive framings like `At its core`, `In reality`, `Fundamentally`, `What really matters is`, `The heart of the matter is`, `At the heart of X is/lies`. Stripped only at sentence start where the tell is strongest.
- **Signposting announcements** (`SIGNPOSTING`): meta-commentary that announces the writing instead of doing it: `Let's dive in(to ...)`, `Let's break this down`, `Here's what you need to know`, `Without further ado`, `In this article, I'll ...`, `Buckle up`.
- **Filler phrases** (`FILLER_PHRASES`, `full` intensity only): `in order to`, `due to the fact that`, `in spite of the fact that`, `a wide variety of`, `a significant/substantial amount of`, `at this point in time`, `for all intents and purposes`, `in the event that`, `with regard to`, `prior to`, `subsequent to`, `the fact that`.
- **Negative-parallelism tricolons** (`NEGATIVE_PARALLELISM`, `full` intensity only): rhetorical tricolons like `No guesswork, no bloat, no surprises.`

#### Intensity levels (subtle / balanced / full)

- Explicit `intensity` parameter on `humanize_deterministic` and `humanize_deterministic_with_report`. Previously every rule ran every time; now the rule set is gated per intensity.
  - `subtle` — stock vocab only.
  - `balanced` (default) — sycophancy, hedging openers, transition tics, stock vocab, authority tropes, signposting, performative balance, em-dash cap.
  - `full` — balanced + filler phrases + negative-parallelism knockouts.
- LLM mode also branches prompt guidance by intensity (see `_INTENSITY_PROMPT_GUIDANCE`).

#### Audit trail

- New `Replacement` and `HumanizeReport` dataclasses. Every deterministic edit is recorded as `(rule, pattern, before, after)`.
- `humanize_deterministic_with_report(text, *, intensity) -> (str, HumanizeReport)` returns both the humanized text and the audit trail.
- `HumanizeReport.counts_by_rule` + `HumanizeReport.to_dict()` for machine-readable reporting.
- Tracks `em_dashes_before` / `em_dashes_after` to surface paragraph-cap effectiveness.

#### CLI (rewritten with `argparse`)

| Flag               | Behavior                                                             |
| ------------------ | -------------------------------------------------------------------- |
| `--version`        | Print `unslop <version>` from the single-source `__version__`.     |
| `-m / --mode`      | Choose intensity: `subtle`, `balanced`, `full`. Default `balanced`.  |
| `--stdin`          | Read from stdin, write to stdout. Forces `--no-backup`.              |
| `-o / --output`    | Write humanized text to a named file instead of overwriting input.   |
| `--diff`           | Print unified diff to stdout; implies `--dry-run`.                   |
| `--dry-run`        | Validate and report but do not write to disk.                        |
| `--no-backup`      | Skip the `<stem>.original.md` backup.                                |
| `--json`           | Emit machine-readable JSON per file.                                 |
| `--report PATH`    | Write full replacement audit trail as JSON (requires deterministic). |
| `-q / --quiet`     | Suppress progress lines.                                             |
| Multi-file / batch | `unslop a.md b.md c.md` is supported.                              |

Exit codes: `0` success, `1` usage / file-not-found / sensitive path, `2` validation failure, `3` partial-success batch.

#### Packaging / typing / distribution

- `scripts/py.typed` marker so downstream type-checkers see the package as typed.
- `[tool.mypy]` strict config in `pyproject.toml`, enforced in CI.
- `[tool.ruff]` config (`E`, `F`, `I`, `UP`, `B`, `SIM`), enforced in CI.
- `[project.optional-dependencies]` `dev = [pytest, ruff, mypy]` and `llm = [anthropic]`.
- Single-source version: `__version__` in `scripts/__init__.py`, read dynamically by `pyproject.toml` (`dynamic = ["version"]`).
- Classifier `Typing :: Typed` added.
- Python support window bumped to `>= 3.10` (previously inconsistent).
- `Dockerfile` (two-stage, non-root user, optional `INSTALL_LLM=1` build arg).
- `.github/workflows/publish.yml` — PyPI trusted-publisher workflow on `unslop-v*` tag with version/tag consistency check.
- `.github/release.yml` — GitHub auto-generated release notes categories (Breaking / Features / Pattern rules / CLI / Validation + benchmarks / Bug fixes / Docs / Internal).

#### Benchmarks + detector eval

- `benchmarks/run.py --all-intensities --strict` — runs the full matrix and enforces monotonicity (`subtle ≤ balanced ≤ full`). Current baseline on 4 fixtures, 148 AI-isms:
  | intensity | after | % reduction |
  | --------- | ----- | ----------- |
  | subtle    | 55    | 62.8%       |
  | balanced  | 18    | 87.8%       |
  | full      | 13    | 91.2%       |
- New fixtures `ai-slop-new-categories.md` and `ai-slop-expanded-categories.md` exercise authority tropes, signposting, filler phrases, negative-parallelism tricolons, and the expanded stock vocab. Without them the benchmarks could not prove the new rules did anything measurable.
- `benchmarks/detector_bench.py` — opt-in AI-detector harness running TMR (`Oxidane/tmr-ai-text-detector`, 99.28% AUROC on RAID) and Desklib v1.01 (`desklib/ai-text-detector-v1.01`, DeBERTa-v3-large). Scores every fixture at every intensity. Surfaces the honest finding that deterministic rule-stripping alone moves the TMR probability by 0.1–0.2 pp, which matches Cat 05 research on adversarial paraphrasing and keeps the project from overclaiming detector evasion. See `benchmarks/README.md`.

#### CI

- `.github/workflows/ci.yml` now runs ruff, mypy (strict), pytest, `verify_repo.py`, and both benchmark gates (default + monotonicity matrix) across Python 3.10 / 3.11 / 3.12 / 3.13.

#### Validator

- `ValidationResult.to_dict()` for JSON emission.
- New `AI_ISMS` patterns mirror every new category above so validation scores stay honest.

### Changed

- `humanize_file` now delegates to `humanize_file_ex`, which returns a `HumanizeOutcome` carrying `(ok, original, humanized, validation, report, attempts, error)`. Back-compat is preserved: the legacy signature still returns a `bool`.
- `_build_humanize_prompt` accepts `intensity` and injects category-specific guidance.
- CLI `--report` now refuses non-deterministic mode (LLM mode cannot produce byte-level audit trails).

### Reference

- Full study + gap analysis: `docs/research/IMPLEMENTATION_TRACE.md`.
- Wikipedia: *Signs of AI writing* — the canonical public taxonomy we cross-referenced.
- `blader/unslop` — the Claude-Code humanize skill whose "30 tells" list inspired several new categories.

---

## 0.3.0 and earlier

See git history. No formal changelog before 0.4.0.
