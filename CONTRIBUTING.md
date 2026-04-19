# Contributing

Welcome. Few rules, all practical.

## Before you change anything

Read [`CLAUDE.md`](./CLAUDE.md). It names the SSOT files and explains which directories are mirrored. Editing a mirror gets your work overwritten on the next sync.

## What goes where

| You want to change... | Edit this |
|-----------------------|-----------|
| Main humanizer behavior | `skills/humanizer/SKILL.md` |
| Always-on activation text | `rules/humanizer-activate.md` |
| File-rewriter behavior | `humanizer-humanize/SKILL.md` and `humanizer-humanize/scripts/*.py` |
| Commit message rules | `skills/humanizer-commit/SKILL.md` |
| PR review rules | `skills/humanizer-review/SKILL.md` |
| Slash command behavior | `commands/<name>.toml` |
| Hook behavior | `hooks/<name>.{js,sh,ps1}` |
| Plugin manifests | `.claude-plugin/`, `gemini-extension.json`, `plugins/humanizer/.codex-plugin/plugin.json` |

## Add an AI-ism

1. Add a regex to the right list in `humanizer-humanize/scripts/humanize.py` (`STOCK_VOCAB`, `HEDGING_OPENERS`, or `SYCOPHANCY`).
2. Add the same regex to `AI_ISMS` in `humanizer-humanize/scripts/validate.py` so the validator catches it.
3. Add a test in `tests/humanizer-humanize/test_humanize.py`.
4. Add the phrase to the "Drop" lists in `skills/humanizer/SKILL.md` and `rules/humanizer-activate.md`.

## Tests

```bash
python3 -m pytest tests/humanizer-humanize/
```

Must pass before any merge. Add coverage for any new behavior.

## Commit messages

Use the humanizer-commit voice: Conventional Commits, subject ≤72 chars (aim ≤50), imperative mood, body only when "why" isn't obvious. See `skills/humanizer-commit/SKILL.md`.

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
