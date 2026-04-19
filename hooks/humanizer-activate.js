#!/usr/bin/env node
// humanizer — Claude Code SessionStart activation hook
//
// Runs on every session start:
//   1. Writes flag file at $CLAUDE_CONFIG_DIR/.humanizer-active (statusline reads this)
//   2. Emits humanizer ruleset as hidden SessionStart context
//   3. Detects missing statusline config and emits setup nudge

const fs = require('fs');
const path = require('path');
const os = require('os');
const { getDefaultMode, safeWriteFlag, getFlagPath } = require('./humanizer-config');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = getFlagPath();
const settingsPath = path.join(claudeDir, 'settings.json');

const mode = getDefaultMode();

if (mode === 'off') {
  try { fs.unlinkSync(flagPath); } catch (e) {}
  process.stdout.write('OK');
  process.exit(0);
}

safeWriteFlag(flagPath, mode);

// Independent modes have their own skill files — don't emit the full ruleset.
const INDEPENDENT_MODES = new Set(['commit', 'review']);

if (INDEPENDENT_MODES.has(mode)) {
  process.stdout.write('HUMANIZER MODE ACTIVE — level: ' + mode + '. Behavior defined by /humanizer-' + mode + ' skill.');
  process.exit(0);
}

// Read SKILL.md — the single source of truth for humanizer behavior.
// Plugin installs: __dirname = <plugin_root>/hooks/, SKILL.md at <plugin_root>/skills/humanizer/SKILL.md
// Standalone installs: __dirname = $CLAUDE_CONFIG_DIR/hooks/, SKILL.md won't exist — falls back to activation rule then hardcoded rules.
let skillContent = '';
try {
  skillContent = fs.readFileSync(
    path.join(__dirname, '..', 'skills', 'humanizer', 'SKILL.md'), 'utf8'
  );
} catch (e) { /* try activation rule next */ }

// Fallback: try the activation rule file (lighter weight than full SKILL.md)
let activationRule = '';
if (!skillContent) {
  try {
    activationRule = fs.readFileSync(
      path.join(__dirname, '..', 'rules', 'humanizer-activate.md'), 'utf8'
    ).trim();
  } catch (e) { /* will use hardcoded fallback */ }
}

let output;

if (skillContent) {
  const body = skillContent.replace(/^---[\s\S]*?---\s*/, '');

  // Filter intensity table and examples to the active level
  const filtered = body.split('\n').reduce((acc, line) => {
    const tableRowMatch = line.match(/^\|\s*\*\*(\S+?)\*\*\s*\|/);
    if (tableRowMatch) {
      if (tableRowMatch[1] === mode) {
        acc.push(line);
      }
      return acc;
    }

    const exampleMatch = line.match(/^- (\S+?):\s/);
    if (exampleMatch) {
      if (exampleMatch[1] === mode) {
        acc.push(line);
      }
      return acc;
    }

    acc.push(line);
    return acc;
  }, []);

  output = 'HUMANIZER MODE ACTIVE — level: ' + mode + '\n\n' + filtered.join('\n');
} else if (activationRule) {
  output = 'HUMANIZER MODE ACTIVE — level: ' + mode + '\n\n' + activationRule;
} else {
  output =
    'HUMANIZER MODE ACTIVE — level: ' + mode + '\n\n' +
    'Write like a careful human. All technical substance stays exact. Only AI-slop dies.\n\n' +
    '## Persistence\n\n' +
    'ACTIVE EVERY RESPONSE. No revert after many turns. No drift back into AI-template English.\n' +
    'Off only: "stop humanizer" / "normal mode".\n\n' +
    'Current level: **' + mode + '**. Switch: `/humanizer subtle|balanced|full|voice-match|anti-detector`.\n\n' +
    '## Rules\n\n' +
    'Drop: sycophancy ("great question", "I\'d be happy to"), stock vocab (delve/tapestry/testament/seamless/holistic/leverage-as-filler), ' +
    'hedging stacks ("it\'s important to note that"), tricolon padding, em-dash pileups, performative balance, tidy five-paragraph shapes.\n\n' +
    'Keep: technical terms exact, code unchanged, real uncertainty when honest.\n' +
    'Engineer burstiness: mix short and long sentences deliberately.\n\n' +
    'Pattern: [concrete observation]. [why]. [what to do next].\n\n' +
    '## Auto-Clarity\n\n' +
    'Drop humanizer style for: security warnings, irreversible actions, legal/medical/financial precision, user confused. Resume after.\n\n' +
    '## Boundaries\n\n' +
    'Code/commits/PRs: write normal. "stop humanizer" or "normal mode": revert. Level persists until changed or session ends.';
}

// Detect missing statusline config — nudge Claude to help set it up
try {
  let hasStatusline = false;
  if (fs.existsSync(settingsPath)) {
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    if (settings.statusLine) {
      hasStatusline = true;
    }
  }

  if (!hasStatusline) {
    const isWindows = process.platform === 'win32';
    const scriptName = isWindows ? 'humanizer-statusline.ps1' : 'humanizer-statusline.sh';
    const scriptPath = path.join(__dirname, scriptName);
    const command = isWindows
      ? `powershell -ExecutionPolicy Bypass -File "${scriptPath}"`
      : `bash "${scriptPath}"`;
    const statusLineSnippet =
      '"statusLine": { "type": "command", "command": ' + JSON.stringify(command) + ' }';
    output += "\n\n" +
      "STATUSLINE SETUP NEEDED: The humanizer plugin includes a statusline badge showing active mode " +
      "(e.g. [humanizer], [humanizer:full]). It is not configured yet. " +
      "To enable, add this to " + path.join(claudeDir, 'settings.json') + ": " +
      statusLineSnippet + " " +
      "Proactively offer to set this up for the user on first interaction.";
  }
} catch (e) {
  // Silent fail — don't block session start over statusline detection
}

process.stdout.write(output);
