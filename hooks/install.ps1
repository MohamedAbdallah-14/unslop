# Install unslop hooks into Claude Code's user settings on Windows.
#
# Copies hook scripts into $CLAUDE_CONFIG_DIR/hooks/ (or ~/.claude/hooks/)
# and registers SessionStart + UserPromptSubmit hooks in settings.json.
# Also wires the statusline so the [unslop] badge shows when active.
#
# Supports: -Force to overwrite existing hooks.
# Requires: PowerShell 5.1+, Node.js

param([switch]$Force)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$HooksDir  = Join-Path $ClaudeDir 'hooks'
$Settings  = Join-Path $ClaudeDir 'settings.json'

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Error "Error: 'node' not found on PATH. Install Node.js from https://nodejs.org"
  exit 1
}

$HookFiles = @('package.json', 'unslop-config.js', 'unslop-activate.js', 'unslop-mode-tracker.js', 'unslop-statusline.ps1')

# Check if already installed (unless -Force)
if (-not $Force) {
  $allPresent = $true
  foreach ($hook in $HookFiles) {
    if (-not (Test-Path (Join-Path $HooksDir $hook))) {
      $allPresent = $false
      break
    }
  }
  if ($allPresent -and (Test-Path $Settings)) {
    Write-Host "Unslop hooks already installed in $HooksDir"
    Write-Host "  Re-run with -Force to overwrite."
    exit 0
  }
}

if ($Force -and (Test-Path (Join-Path $HooksDir 'unslop-activate.js'))) {
  Write-Host "Reinstalling unslop hooks (-Force)..."
} else {
  Write-Host "Installing unslop hooks..."
}

New-Item -ItemType Directory -Force -Path $HooksDir | Out-Null

foreach ($hook in $HookFiles) {
  $src = Join-Path $ScriptDir $hook
  $dst = Join-Path $HooksDir $hook
  if (Test-Path $src) {
    Copy-Item -Force $src $dst
  } else {
    $url = "https://raw.githubusercontent.com/MohamedAbdallah-Hu/unslop/main/hooks/$hook"
    Invoke-WebRequest -Uri $url -OutFile $dst
  }
  Write-Host "  Installed: $dst"
}

if (-not (Test-Path $Settings)) { '{}' | Out-File -Encoding utf8 $Settings }

# Back up settings before modifying
Copy-Item $Settings "$Settings.bak"

$env:UNSLOP_SETTINGS = $Settings
$env:UNSLOP_HOOKS_DIR = $HooksDir

node -e @"
  const fs = require('fs');
  const settingsPath = process.env.UNSLOP_SETTINGS;
  const hooksDir = process.env.UNSLOP_HOOKS_DIR;
  const managedStatusLinePath = hooksDir + '/unslop-statusline.ps1';
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  if (!settings.hooks) settings.hooks = {};

  if (!settings.hooks.SessionStart) settings.hooks.SessionStart = [];
  const hasStart = settings.hooks.SessionStart.some(e =>
    e.hooks && e.hooks.some(h => h.command && h.command.includes('unslop'))
  );
  if (!hasStart) {
    settings.hooks.SessionStart.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/unslop-activate.js\"',
        timeout: 5,
        statusMessage: 'Loading unslop mode...'
      }]
    });
  }

  if (!settings.hooks.UserPromptSubmit) settings.hooks.UserPromptSubmit = [];
  const hasPrompt = settings.hooks.UserPromptSubmit.some(e =>
    e.hooks && e.hooks.some(h => h.command && h.command.includes('unslop'))
  );
  if (!hasPrompt) {
    settings.hooks.UserPromptSubmit.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/unslop-mode-tracker.js\"',
        timeout: 5,
        statusMessage: 'Tracking unslop mode...'
      }]
    });
  }

  if (!settings.statusLine) {
    settings.statusLine = {
      type: 'command',
      command: 'powershell -ExecutionPolicy Bypass -File \"' + managedStatusLinePath + '\"'
    };
    console.log('  Statusline badge configured.');
  } else {
    const cmd = typeof settings.statusLine === 'string'
      ? settings.statusLine
      : (settings.statusLine.command || '');
    if (cmd.includes(managedStatusLinePath)) {
      console.log('  Statusline badge already configured.');
    } else {
      console.log('  NOTE: Existing statusline detected - unslop badge NOT added.');
    }
  }

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
  console.log('  Hooks wired in settings.json');
"@

Write-Host ""
Write-Host "Done! Restart Claude Code to activate."
Write-Host ""
Write-Host "What's installed:"
Write-Host "  - SessionStart hook: auto-loads unslop rules every session"
Write-Host "  - Mode tracker hook: updates statusline badge when you switch modes"
Write-Host "  - Statusline badge: shows [unslop] or [unslop:FULL] etc."
