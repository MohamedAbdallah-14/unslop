# unslop CLI

Humanize Markdown and text files from the command line. `unslop` removes common AI tells, varies rhythm, and preserves code, URLs, headings, tables, blockquotes, and YAML frontmatter.

Use it for docs, memory files, posts, bios, cover letters, and other prose where voice matters. Do not use it for secrets, legal text, medical advice, runbooks, or anything where exact wording matters more than readability.

## Install

```bash
pipx install unslop
# or
uv tool install unslop
```

For a one-off local checkout:

```bash
cd unslop
python3 -m scripts.cli --deterministic README.md
```

## Quick Start

```bash
unslop --deterministic doc.md
```

Deterministic mode is local-only. No API key, no subprocess, no network call.

```bash
unslop doc.md
```

LLM mode uses `ANTHROPIC_API_KEY` when set, otherwise falls back to `claude --print` if the Claude CLI is installed. Before any LLM call, the CLI refuses secret-like content such as private keys and common API token shapes. Use `--deterministic` for sensitive local files.

## Common Commands

```bash
unslop --deterministic --diff doc.md          # preview changes
unslop --deterministic --dry-run --json doc.md
unslop --deterministic --report audit.json doc.md
unslop --mode full doc.md
unslop --no-structural --no-soul doc.md       # extra conservative
cat draft.md | unslop --stdin --deterministic
```

## What Files Work

| Type | Action |
|------|--------|
| `.md`, `.markdown`, `.txt`, `.rst` | Humanize prose |
| `.py`, `.js`, `.ts`, `.json`, `.yaml`, etc. | Skip as code/config |
| `*.original.md`, `*.original.txt` | Skip as backups |
| Mixed prose + code | Humanize prose; preserve protected regions |
| Sensitive paths (`.env`, `*.pem`, `~/.ssh/`) | Refuse |

## What Stays Exact

- Fenced code blocks
- Indented code blocks
- Inline backticks
- URLs and markdown links
- Headings
- Markdown tables
- Blockquotes
- YAML frontmatter

Deterministic mode validates these after rewriting. If preservation fails, the command exits non-zero and does not overwrite the file.

## Backups And Sidecars

In file mode, `unslop` writes `FILE.original.md` before overwriting the target. If `--strip-reasoning` removes hidden reasoning traces, the stripped content is written to `FILE.reasoning.md`; those sidecars are gitignored by the repo template because they can contain process notes you did not mean to publish.

## Why This Exists

Project memory files, READMEs, resumes, and draft posts often get polished by assistants until they all sound the same. `unslop` is a cleanup pass: remove the stock phrases, keep the facts, keep the code, and make the text readable again.

## Part Of The Unslop Plugin

| Skill | What it does |
|-------|--------------|
| `unslop` | Live assistant-output humanization |
| `unslop-file` | File rewrite command |
| `unslop-commit` | Commit messages without AI tone |
| `unslop-review` | Direct PR review comments |
| `unslop-help` | Quick reference |

## License

MIT.
