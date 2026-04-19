#!/usr/bin/env bash
# sync-mirrors.sh
# Propagate SSOT files (skills + rules + scripts) to all mirrored locations.
# Run locally for testing; the GitHub Actions sync workflow invokes the same
# script so behavior is identical between CI and developer machines.
#
# Idempotent. Safe to run repeatedly.

set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$ROOT"

# ---- 1. Main humanizer skill mirrors ----
SRC=skills/humanizer/SKILL.md
for DEST in \
  humanizer/SKILL.md \
  plugins/humanizer/skills/humanizer/SKILL.md \
  .cursor/skills/humanizer/SKILL.md \
  .windsurf/skills/humanizer/SKILL.md
do
  mkdir -p "$(dirname "$DEST")"
  cp "$SRC" "$DEST"
done

# ---- 2. Sub-skills to plugin bundle ----
for sub in humanizer-commit humanizer-review humanizer-help; do
  S="skills/$sub/SKILL.md"
  D="plugins/humanizer/skills/$sub/SKILL.md"
  mkdir -p "$(dirname "$D")"
  cp "$S" "$D"
done

# ---- 3. humanizer-humanize skill + scripts to plugin bundle and skills/humanize ----
mkdir -p plugins/humanizer/skills/humanize/scripts
cp humanizer-humanize/SKILL.md plugins/humanizer/skills/humanize/SKILL.md
cp -R humanizer-humanize/scripts/. plugins/humanizer/skills/humanize/scripts/

mkdir -p skills/humanize/scripts
cp humanizer-humanize/SKILL.md skills/humanize/SKILL.md
cp -R humanizer-humanize/scripts/. skills/humanize/scripts/

# ---- 4. Activation rule -> IDE rule files (with platform frontmatter) ----
BODY_FILE=rules/humanizer-activate.md
mkdir -p .cursor/rules .windsurf/rules .clinerules .github

# Cursor
{
  printf '%s\n' '---'
  printf 'description: Humanize assistant output. Drop AI-isms, engineer burstiness, preserve technical accuracy.\n'
  printf 'alwaysApply: true\n'
  printf '%s\n\n' '---'
  cat "$BODY_FILE"
} > .cursor/rules/humanizer.mdc

# Windsurf
{
  printf '%s\n' '---'
  printf 'description: Humanize assistant output. Drop AI-isms, engineer burstiness, preserve technical accuracy.\n'
  printf 'always_on: true\n'
  printf '%s\n\n' '---'
  cat "$BODY_FILE"
} > .windsurf/rules/humanizer.md

# Cline
{
  printf '# Humanizer Rule (Cline)\n\n'
  cat "$BODY_FILE"
} > .clinerules/humanizer.md

# Copilot
{
  printf '# Copilot Instructions — humanizer\n\n'
  printf 'When generating chat replies, code comments, or commit messages in this repository:\n\n'
  cat "$BODY_FILE"
} > .github/copilot-instructions.md

echo "sync-mirrors: done."
