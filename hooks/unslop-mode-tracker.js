#!/usr/bin/env node
// unslop — UserPromptSubmit hook to track which unslop mode is active
// Inspects user input for /unslop commands and natural language activation,
// writes mode to flag file, and emits per-turn style reinforcement.

const fs = require('fs');
const path = require('path');
const os = require('os');
const { getDefaultMode, safeWriteFlag, readFlag, getFlagPath } = require('./unslop-config');

const flagPath = getFlagPath();

let input = '';
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const prompt = (data.prompt || '').trim();
    const promptLower = prompt.toLowerCase();

    // Natural language activation (e.g. "activate unslop", "turn on unslop mode",
    // "make this sound human", "humanize this").
    if (/\b(activate|enable|turn on|start)\b.*\bunslop\b/i.test(prompt) ||
        /\bunslop\b.*\b(mode|activate|enable|turn on|start)\b/i.test(prompt) ||
        /\b(humanize|de-?slop|make.*sound human|less robotic)\b/i.test(prompt)) {
      if (!/\b(stop|disable|turn off|deactivate)\b/i.test(prompt)) {
        const mode = getDefaultMode();
        if (mode !== 'off') {
          safeWriteFlag(flagPath, mode);
        }
      }
    }

    // Match /unslop slash commands
    if (promptLower.startsWith('/unslop')) {
      const parts = promptLower.split(/\s+/);
      const cmd = parts[0];
      const arg = parts[1] || '';

      let mode = null;

      if (cmd === '/unslop-commit') {
        mode = 'commit';
      } else if (cmd === '/unslop-review') {
        mode = 'review';
      } else if (cmd === '/unslop' || cmd === '/unslop:unslop') {
        if (arg === 'subtle') mode = 'subtle';
        else if (arg === 'balanced') mode = 'balanced';
        else if (arg === 'full') mode = 'full';
        else if (arg === 'voice-match') mode = 'voice-match';
        else if (arg === 'anti-detector') mode = 'anti-detector';
        else mode = getDefaultMode();
      }

      if (mode && mode !== 'off') {
        safeWriteFlag(flagPath, mode);
      } else if (mode === 'off') {
        try { fs.unlinkSync(flagPath); } catch (e) {}
      }
    }

    // Also match /unslop-file (the file-rewriter command) — set mode to current default
    if (promptLower.startsWith('/humanize') && !promptLower.startsWith('/unslop')) {
      const mode = getDefaultMode();
      if (mode !== 'off') {
        safeWriteFlag(flagPath, mode);
      }
    }

    // Detect deactivation — natural language and explicit stop phrases
    if (/\b(stop|disable|deactivate|turn off)\b.*\bunslop\b/i.test(prompt) ||
        /\bunslop\b.*\b(stop|disable|deactivate|turn off)\b/i.test(prompt) ||
        /\bnormal mode\b/i.test(prompt) ||
        /\brobotic mode\b/i.test(prompt)) {
      try { fs.unlinkSync(flagPath); } catch (e) {}
    }

    // Per-turn reinforcement: emit a structured reminder when unslop is active.
    // The SessionStart hook injects the full ruleset once, but models lose it
    // when other plugins inject competing style instructions every turn.
    // Skip independent modes (commit, review) — they have their own skill behavior.
    const INDEPENDENT_MODES = new Set(['commit', 'review']);
    const activeMode = readFlag(flagPath);
    if (activeMode && !INDEPENDENT_MODES.has(activeMode)) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "UserPromptSubmit",
          additionalContext: "UNSLOP MODE ACTIVE (" + activeMode + "). " +
            "Drop sycophancy/stock-vocab/hedging-stacks/tricolons/em-dash-pileups. " +
            "Engineer burstiness. Code/commits/security: write normal."
        }
      }));
    }
  } catch (e) {
    // Silent fail
  }
});
