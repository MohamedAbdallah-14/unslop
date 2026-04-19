<div align="center">

# unslop

**Your CLAUDE.md sounds like ChatGPT wrote it. Stop that.**

</div>

A bundled unslop skill that rewrites memory files (CLAUDE.md, AGENTS.md, todos, preferences, docs) to remove AI slop while preserving every code block, URL, path, and heading exactly.

## What It Do

Slash command: `/unslop-file <filepath>`

Drops sycophancy, stock vocab (`delve`, `tapestry`, `testament`, `leverage`, `robust`, `holistic`), hedging stacks, tricolon padding, em-dash pileups, and tidy five-paragraph essay shapes. Engineers burstiness. Restores voice. Keeps every fenced code block byte-identical.

Backup: `FILE.original.md` (the human-readable original — re-run if you edit it).

## Two Modes

### Deterministic (fast, no API)

```bash
cd unslop && python3 -m scripts --deterministic <absolute_filepath>
```

Pure regex. No API key. Strips canonical AI-isms and tightens tricolons. Best for batch / CI. ~50ms per file.

### LLM (default, calls Claude)

```bash
cd unslop && python3 -m scripts <absolute_filepath>
```

Calls Anthropic API (if `ANTHROPIC_API_KEY` set) or `claude --print` CLI. Better quality: rewrites for burstiness, restructures performative paragraphs, matches voice when sample provided.

## Benchmarks

Sample memory files, before/after AI-ism count and word count (deterministic mode):

| File | Original words | Humanized words | AI-isms removed |
|------|----------------|-----------------|-----------------|
| `claude-md-preferences.md` | 706 | 624 | 18 |
| `claude-md-project.md` | 1,512 | 1,310 | 24 |
| `mixed-with-code.md` | 950 | 838 | 11 |
| `project-notes.md` | 1,180 | 1,022 | 19 |
| `todo-list.md` | 845 | 763 | 14 |

LLM mode produces stronger rewrites (typically 60–75% AI-ism removal and noticeable burstiness improvement) but takes ~5–15s per file and costs API tokens.

## Security

`unslop` calls a subprocess (the `claude` CLI) when `ANTHROPIC_API_KEY` is unset. Snyk may flag this as High Risk because of the `subprocess.run` + file I/O combination. See [SECURITY.md](./SECURITY.md) for the full rationale.

The deterministic mode does no subprocess and no network — use it if your security context requires that.

## Install

Bundled with the `unslop` plugin. Skill path: `unslop/`.

Standalone: `cd unslop && python3 -m scripts <filepath>` (Python 3.10+).

## Usage

```bash
# Deterministic, no API
python3 -m scripts --deterministic /Users/me/proj/CLAUDE.md

# LLM, default
ANTHROPIC_API_KEY=... python3 -m scripts /Users/me/proj/CLAUDE.md

# LLM via Claude CLI fallback
python3 -m scripts /Users/me/proj/CLAUDE.md
```

## What Files Work

| Type | Action |
|------|--------|
| `.md`, `.markdown`, `.txt`, `.rst` | Humanize (prose) |
| `.py`, `.js`, `.ts`, `.json`, `.yaml`, etc. | Skip (code/config) |
| `*.original.md` | Skip (already a backup) |
| Mixed prose + code | Humanize prose; leave fenced code untouched |
| Sensitive paths (`.env`, `*.pem`, `~/.ssh/`) | Refuse |

## How It Work

```
detect file type ──▶ write .original.md backup ──▶ humanize (deterministic or LLM)
                                                              │
                                                              ▼
                                                         validate
                                          (preserve code/URLs/paths + AI-ism residual)
                                                              │
                                                       ┌──────┴──────┐
                                                    pass            fail
                                                       │              │
                                                  write & done   targeted fix
                                                                      │
                                                              retry (max 2)
                                                                      │
                                                              ┌───────┴───────┐
                                                           pass             fail
                                                              │               │
                                                         write & done    restore original
```

## What Is Preserved

- Fenced code blocks (every byte)
- Indented code blocks
- Inline backticks
- URLs and markdown links
- File paths and commands
- Technical terms, proper nouns, API names
- Dates, version numbers, numerics
- Headings (exact text)
- Tables (structure; cells humanized)
- YAML frontmatter

## Why This Matter

Project memory files (CLAUDE.md, AGENTS.md) get loaded into every agent session. If they're in AI-template English, you pay tokens for slop and you teach the model to mirror that voice back at you. Humanizing the memory file is the cheapest possible voice intervention.

## Part of the Unslop Plugin

| Skill | What it does |
|-------|--------------|
| `unslop` | Active humanization mode for live responses |
| `unslop-commit` | Commit messages without AI tone |
| `unslop-review` | Direct, human-voice PR comments |
| `unslop` | This: rewrite memory files |
| `unslop-help` | Quick-reference card |

## License

MIT — same as the parent unslop plugin.
