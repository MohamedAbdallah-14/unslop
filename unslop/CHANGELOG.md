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
