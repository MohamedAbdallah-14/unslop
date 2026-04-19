---
name: humanizer-help
description: >
  Quick-reference card for humanizer modes, sub-skills, and slash commands.
  One-shot display, not a persistent mode. Trigger: /humanizer-help,
  "humanizer help", "what humanizer commands", "how do I use humanizer".
---

# Humanizer Help

## Purpose

Show a single reference card for humanizer modes, related sub-skills, exit phrases, and config. One-shot. Does not toggle modes. Does not write flag files.

## Output

Render the card below in normal prose (not humanizer style — this is documentation).

### Modes

| Mode | Trigger | What it does |
|------|---------|--------------|
| `subtle` | `/humanizer subtle` | Light touch. Trim AI tells, keep length and structure. |
| `balanced` | `/humanizer` (default) | Cut slop, vary rhythm, restore voice. |
| `full` | `/humanizer full` | Strong rewrite. Restructure. Allow opinions. |
| `voice-match` | `/humanizer voice-match` | Follow a provided voice/style sample. |
| `anti-detector` | `/humanizer anti-detector` | Adversarial paraphrase for detector resistance. Use only when explicitly requested. |

Modes persist until changed or the session ends.

### Sub-skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `humanizer-commit` | `/humanizer-commit`, `/commit`, "write a commit" | Conventional Commits in human voice. |
| `humanizer-review` | `/humanizer-review`, `/review`, "review this PR" | Direct, kind PR review comments. |
| `humanize` (action) | `/humanize <filepath>`, "humanize memory file" | Rewrite a markdown file removing AI-isms while preserving code/URLs/structure. |
| `humanizer-help` | `/humanizer-help`, "humanizer help" | This card. |

### Deactivate

- `"stop humanizer"` or `"normal mode"` — revert immediately
- Resume with `/humanizer` (or any mode flag)

### Configuration

- Default mode: `balanced`
- Override: `HUMANIZER_DEFAULT_MODE=full` (env), or `~/.config/humanizer/config.json`:
  ```json
  { "defaultMode": "full" }
  ```
- `"off"` disables auto-activation entirely
- Resolution order: env var > config file > `balanced`

### More

Full docs and source: <https://github.com/MohamedAbdallah-Hu/humanizer>

## Boundaries

- One-shot. Do not toggle a mode, write a flag file, or persist any state.
- Do not output in humanizer style — this card is reference material.
