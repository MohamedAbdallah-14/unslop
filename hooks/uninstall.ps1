# unslop — uninstall hook files and remove settings.json entries
# Usage: pwsh hooks/uninstall.ps1

$ErrorActionPreference = 'Stop'

$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$HooksDir  = Join-Path $ClaudeDir 'hooks'
$Settings  = Join-Path $ClaudeDir 'settings.json'
$Flag      = Join-Path $ClaudeDir '.unslop-active'

$HookFiles = @('package.json', 'unslop-config.js', 'unslop-activate.js', 'unslop-mode-tracker.js', 'unslop-statusline.ps1')

Write-Host "Uninstalling unslop hooks..."

foreach ($hook in $HookFiles) {
  $target = Join-Path $HooksDir $hook
  if (Test-Path $target) {
    Remove-Item $target -Force
    Write-Host "  Removed: $target"
  }
}

if (Test-Path $Flag) {
  Remove-Item $Flag -Force
  Write-Host "  Removed flag file: $Flag"
}

if ((Test-Path $Settings) -and (Get-Command node -ErrorAction SilentlyContinue)) {
  Copy-Item $Settings "$Settings.bak"

  $env:UNSLOP_SETTINGS = $Settings
  node -e @"
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
"@
} else {
  Write-Host "  Skipped settings.json cleanup (node not found or settings.json missing)."
}

Write-Host ""
Write-Host "Done. Restart Claude Code to complete removal."
