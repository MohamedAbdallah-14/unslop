---
name: humanizer-humanize
description: >
  Humanize natural-language memory files (CLAUDE.md, todos, preferences, docs) by removing AI-isms
  and adding burstiness while preserving every code block, URL, path, command, and heading exactly.
  Two modes: --deterministic (fast, regex-based, no API) and LLM (default, calls Claude for rewrite).
  Humanized version overwrites the original file. Plain backup saved as FILE.original.md.
  Trigger: /humanize <filepath> or "humanize memory file"
---

# Humanizer Humanize

## Purpose

Rewrite natural-language memory files (CLAUDE.md, AGENTS.md, todos, preferences, docs) so they sound human-written: no sycophancy, no stock vocab, no five-paragraph essay shape, no tricolon padding. Everything technical stays exact: code blocks, inline code, URLs, file paths, commands, headings, tables.

Two modes:

- **`--deterministic`** — fast regex pass that strips canonical AI-isms and tightens tricolons. No API call, no `ANTHROPIC_API_KEY` needed. Best for batch processing and CI.
- **LLM mode (default)** — calls Claude (via Anthropic SDK or `claude --print` CLI fallback) to do a full rewrite that engineers burstiness, restructures performative paragraphs, and matches voice. Slower but better quality.

Humanized version overwrites the original. A `FILE.original.md` backup is written first. Re-run after editing the `.original.md` to regenerate.

## Trigger

`/humanize <filepath>`, `/humanizer:humanize <filepath>`, or "humanize memory file", "de-slop this doc", "strip AI tone from this file".

## Process

The scripts live in a `scripts/` directory adjacent to this SKILL.md.

Common layouts:
- Full repo: `humanizer-humanize/SKILL.md` + `humanizer-humanize/scripts/`
- Synced mirror: `skills/humanize/SKILL.md` + `skills/humanize/scripts/`
- Codex bundle: `plugins/humanizer/skills/humanize/SKILL.md` + sibling `scripts/`

Always prefer the `scripts/` sibling of the currently loaded SKILL file.

Steps:

1. Locate the directory containing this SKILL.md and its `scripts/` sibling.
2. Run from that directory: `python3 -m scripts <absolute_filepath>` (LLM mode), or add `--deterministic` for the regex pass.
3. CLI flow: detect file type → write `.original.md` backup → humanize → validate (preserve check + AI-ism residual check) → on validation error: targeted fix call (LLM mode) → retry up to 2 times.
4. On final failure: report errors, restore original, exit 2.
5. On success: report path of humanized file and `.original.md` backup, exit 0.
6. Return result to user.

## Humanization Rules

### Remove (canonical AI-isms)

- Sycophancy openers: "Great question!", "Certainly!", "Absolutely!", "Sure!", "I'd be happy to help", "What a fascinating..."
- Stock vocab: delve, tapestry, testament (when used as praise), navigate (figurative), embark, journey (figurative), realm, landscape (figurative), pivotal, paramount, seamless, holistic, leverage (as filler verb), robust (as filler), comprehensive (when "complete" works), cutting-edge, state-of-the-art (as filler)
- Hedging stacks: "It's important to note that", "It's worth mentioning", "Generally speaking", "In essence", "At its core", "It should be noted that", "It's also worth pointing out"
- Performative balance: "however" / "on the other hand" appended to every claim
- Em-dash pileups (more than two em-dashes per paragraph)

### Tighten

- Tricolons: "X, Y, and Z" stacks where two would suffice — keep two, drop the weakest
- Bullet soup: three bullets that say the same thing → merge into one sentence
- Five-paragraph essay shapes: vary paragraph length; don't write four paragraphs of identical length

### Preserve EXACTLY (never modify)

- Fenced code blocks (```...```) — every byte
- Indented code blocks (4-space)
- Inline code (`...`)
- URLs and markdown links
- File paths (`./src/`, `/etc/`, `C:\Users\...`)
- Commands (`npm install`, `git rebase`, `docker run`)
- Technical terms, proper nouns, API names
- Dates, version numbers, numerics
- Environment variables (`$HOME`, `${NODE_ENV}`)

### Preserve structure

- All markdown headings (text exact)
- Bullet hierarchy and nesting
- Numbered lists
- Tables (compress cells; keep structure)
- YAML frontmatter

### CRITICAL RULE

Everything inside ` ``` ... ``` ` is read-only. No comment changes, no whitespace changes, no line reordering. Inline backticks: same. Code is the substrate; humanization only operates on prose between code regions.

## Pattern (before → after)

### Before
> It's important to note that running tests prior to pushing changes is a comprehensive best practice that helps ensure code quality. Additionally, it's worth mentioning that this practice can prevent broken builds from being deployed to production environments.

### After
> Run tests before you push to main. Catches bugs early; keeps prod builds green.

### Before
> The application leverages a microservices architecture that comprises multiple discrete components which collectively deliver functionality to end users. The API gateway, which serves as the entry point for all incoming requests, handles routing to the appropriate downstream service.

### After
> We run microservices: a gateway routes traffic, auth owns sessions and JWTs, and orders does the heavy DB work.

## Boundaries

- Only operate on `.md`, `.txt`, `.markdown`, `.rst`, or extensionless natural language.
- Never modify `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.env`, `.lock`, `.css`, `.html`, `.xml`, `.sql`, `.sh`.
- Mixed prose-and-code files: humanize only the prose; leave fenced code untouched.
- If unsure whether a file is prose or code: leave unchanged.
- Backup `FILE.original.md` is written before overwrite. Never humanize a file already named `*.original.md`.
- Sensitive paths (anything matching `.env*`, `*.pem`, `*.key`, `~/.ssh/`, `~/.aws/`, etc.) are refused before any read or API call.
- Files larger than 500 KB are refused.
