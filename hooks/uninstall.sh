#!/bin/bash
# unslop — uninstall hook files and remove settings.json entries
# Usage: bash hooks/uninstall.sh
set -e

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
HOOKS_DIR="$CLAUDE_DIR/hooks"
SETTINGS="$CLAUDE_DIR/settings.json"
FLAG="$CLAUDE_DIR/.unslop-active"

HOOK_FILES=("package.json" "unslop-config.js" "unslop-activate.js" "unslop-mode-tracker.js" "unslop-statusline.sh")

echo "Uninstalling unslop hooks..."

for hook in "${HOOK_FILES[@]}"; do
  target="$HOOKS_DIR/$hook"
  if [ -f "$target" ]; then
    rm "$target"
    echo "  Removed: $target"
  fi
done

if [ -f "$FLAG" ]; then
  rm "$FLAG"
  echo "  Removed flag file: $FLAG"
fi

if [ -f "$SETTINGS" ] && command -v node >/dev/null 2>&1; then
  cp "$SETTINGS" "$SETTINGS.bak"

  UNSLOP_SETTINGS="$SETTINGS" node -e "
    const fs = require('fs');
    const settingsPath = process.env.UNSLOP_SETTINGS;
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));

    if (settings.hooks) {
      for (const event of ['SessionStart', 'UserPromptSubmit']) {
        if (Array.isArray(settings.hooks[event])) {
          settings.hooks[event] = settings.hooks[event].filter(e =>
            !(e.hooks && e.hooks.some(h => h.command && h.command.includes('unslop')))
          );
          if (settings.hooks[event].length === 0) delete settings.hooks[event];
        }
      }
      if (Object.keys(settings.hooks).length === 0) delete settings.hooks;
    }

    if (settings.statusLine) {
      const cmd = typeof settings.statusLine === 'string'
        ? settings.statusLine
        : (settings.statusLine.command || '');
      if (cmd.includes('unslop-statusline')) {
        delete settings.statusLine;
        console.log('  Removed statusline config.');
      }
    }

    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    console.log('  Cleaned settings.json');
  "
else
  echo "  Skipped settings.json cleanup (node not found or settings.json missing)."
fi

echo ""
echo "Done. Restart Claude Code to complete removal."
