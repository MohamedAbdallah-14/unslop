# Contributing

Welcome. Few rules, all practical.

## Before you change anything

Read [`CLAUDE.md`](./CLAUDE.md). It names the SSOT files and explains which directories are mirrored. Editing a mirror gets your work overwritten on the next sync.

## What goes where

| You want to change... | Edit this |
|-----------------------|-----------|
| Main unslop behavior | `skills/unslop/SKILL.md` |
| Always-on activation text | `rules/unslop-activate.md` |
| File-rewriter behavior | `unslop/SKILL.md` and `unslop/scripts/*.py` |
| Commit message rules | `skills/unslop-commit/SKILL.md` |
| PR review rules | `skills/unslop-review/SKILL.md` |
| Slash command behavior | `commands/<name>.toml` |
| Hook behavior | `hooks/<name>.{js,sh,ps1}` |
| Plugin manifests | `.claude-plugin/`, `.cursor-plugin/`, `.agents/`, `.codex/`, `gemini-extension.json`, `plugins/unslop/.codex-plugin/plugin.json` |
| Release notes | Root `CHANGELOG.md` only; `unslop/CHANGELOG.md` is generated |

## Add an AI-ism

1. Add a regex to the right list in `unslop/scripts/humanize.py` (`STOCK_VOCAB`, `HEDGING_OPENERS`, `SYCOPHANCY`, `PERFORMATIVE`, or `TRANSITION_TICS`).
2. Add the same regex to `AI_ISMS` in `unslop/scripts/validate.py` so the validator catches it.
3. Add a test in `tests/unslop/test_humanize.py`.
4. Add the phrase to the "Drop" lists in `skills/unslop/SKILL.md` and `rules/unslop-activate.md`.

## Tests

```bash
python3 -m pytest tests/unslop/                 # Python package contract
python3 -m pytest tests/                        # Package + hook integration
python3 tests/verify_repo.py                    # Mirrors, manifests, syntax, versions
python3 benchmarks/run.py --strict              # Offline quality gate
python3 benchmarks/run.py --all-intensities --strict
```

Python 3.10–3.14 and Node 24 are required in CI. Run the affected local gates before opening a PR and add coverage for new behavior. The full release checklist lives in [`docs/RELEASING.md`](./docs/RELEASING.md).

## Commit messages

Use the unslop-commit voice: Conventional Commits, subject ≤72 chars (aim ≤50), imperative mood, body only when "why" isn't obvious. See `skills/unslop-commit/SKILL.md`.

```
fix(humanize): protect heading lines from word substitution

The deterministic pass was replacing "delve" inside `## Delve into the topic`
even though the spec promised headings stay byte-identical. Added
HEADING_LINE to _protect() so heading text becomes an opaque placeholder.

Closes #N
```

## PR descriptions

Same voice. Direct on what changed and why. No "comprehensive solution" or "robust implementation".

## Code style

Python: 4-space indent, type hints on public functions, no unused imports. Keep regexes commented when intent isn't obvious. Avoid one-letter variable names except `m` for `re.Match`.

JS hooks: vanilla Node (no deps), 2-space indent, `"use strict"`, error handling that never breaks the session.

Bash: `set -euo pipefail`, quote every variable, `command -v` checks for required tools.

## Voice in the docs

We eat our own dog food. If you find a stock phrase or sycophancy opener in any doc in this repo, fix it in the same PR.

## License

By contributing you agree your work is licensed MIT.
