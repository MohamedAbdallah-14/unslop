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

# ---- 1. Main unslop skill mirrors ----
# (Note: no top-level `unslop/SKILL.md` mirror — that path is the Python
# package's file-rewriter skill, not the main activation skill.)
SRC=skills/unslop/SKILL.md
for DEST in \
  plugins/unslop/skills/unslop/SKILL.md \
  .cursor/skills/unslop/SKILL.md \
  .windsurf/skills/unslop/SKILL.md
do
  mkdir -p "$(dirname "$DEST")"
  cp "$SRC" "$DEST"
done

# ---- 2. Sub-skills to plugin bundle ----
for sub in unslop-commit unslop-review unslop-help; do
  S="skills/$sub/SKILL.md"
  D="plugins/unslop/skills/$sub/SKILL.md"
  mkdir -p "$(dirname "$D")"
  cp "$S" "$D"
done

# ---- 3. unslop skill + scripts to plugin bundle and skills/unslop-file ----
mkdir -p plugins/unslop/skills/unslop-file/scripts
cp unslop/SKILL.md plugins/unslop/skills/unslop-file/SKILL.md
cp -R unslop/scripts/. plugins/unslop/skills/unslop-file/scripts/

mkdir -p skills/unslop-file/scripts
cp unslop/SKILL.md skills/unslop-file/SKILL.md
cp -R unslop/scripts/. skills/unslop-file/scripts/

# ---- 4. Activation rule -> IDE rule files (with platform frontmatter) ----
BODY_FILE=rules/unslop-activate.md
mkdir -p .cursor/rules .windsurf/rules .clinerules .github

# Cursor
{
  printf '%s\n' '---'
  printf 'description: Humanize assistant output. Drop AI-isms, engineer burstiness, preserve technical accuracy.\n'
  printf 'alwaysApply: true\n'
  printf '%s\n\n' '---'
  cat "$BODY_FILE"
} > .cursor/rules/unslop.mdc

# Windsurf
{
  printf '%s\n' '---'
  printf 'description: Humanize assistant output. Drop AI-isms, engineer burstiness, preserve technical accuracy.\n'
  printf 'always_on: true\n'
  printf '%s\n\n' '---'
  cat "$BODY_FILE"
} > .windsurf/rules/unslop.md

# Cline
{
  printf '# Unslop Rule (Cline)\n\n'
  cat "$BODY_FILE"
} > .clinerules/unslop.md

# Copilot
{
  printf '# Copilot Instructions — unslop\n\n'
  printf 'When generating chat replies, code comments, or commit messages in this repository:\n\n'
  cat "$BODY_FILE"
} > .github/copilot-instructions.md

echo "sync-mirrors: done."
