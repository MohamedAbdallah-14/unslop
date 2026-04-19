#!/bin/bash
# unslop — statusline badge script for Claude Code
# Reads the unslop mode flag file and outputs a colored badge.
#
# Usage in ~/.claude/settings.json:
#   "statusLine": { "type": "command", "command": "bash /path/to/unslop-statusline.sh" }

FLAG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.unslop-active"

# Refuse symlinks — a local attacker could point the flag at a secret file and
# have the statusline render its bytes to the terminal every keystroke.
[ -L "$FLAG" ] && exit 0
[ ! -f "$FLAG" ] && exit 0

# Hard-cap the read at 64 bytes and strip anything outside [a-z0-9-]
MODE=$(head -c 64 "$FLAG" 2>/dev/null | tr -d '\n\r' | tr '[:upper:]' '[:lower:]')
MODE=$(printf '%s' "$MODE" | tr -cd 'a-z0-9-')

# Whitelist valid modes. Anything else → render nothing.
case "$MODE" in
  off|subtle|balanced|full|voice-match|anti-detector|commit|review) ;;
  *) exit 0 ;;
esac

GREEN='\033[38;5;108m'
RESET='\033[0m'

if [ -z "$MODE" ] || [ "$MODE" = "balanced" ]; then
  printf "${GREEN}[unslop]${RESET}"
else
  SUFFIX=$(printf '%s' "$MODE" | tr '[:lower:]' '[:upper:]')
  printf "${GREEN}[unslop:%s]${RESET}" "$SUFFIX"
fi
