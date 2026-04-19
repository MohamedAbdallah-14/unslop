# humanizer — statusline badge script for Claude Code (Windows)
# Reads the humanizer mode flag file and outputs a colored badge.

$ErrorActionPreference = 'SilentlyContinue'

$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$flag = Join-Path $claudeDir '.humanizer-active'

# Refuse symlinks
$item = Get-Item $flag -Force 2>$null
if (-not $item) { return }
if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { return }

# Read with size cap (64 bytes)
$bytes = [System.IO.File]::ReadAllBytes($flag)
if ($bytes.Length -gt 64) { return }

$mode = [System.Text.Encoding]::UTF8.GetString($bytes).Trim().ToLower()
$mode = $mode -replace '[^a-z0-9\-]', ''

# Whitelist
$validModes = @('off', 'subtle', 'balanced', 'full', 'voice-match', 'anti-detector', 'commit', 'review')
if ($mode -notin $validModes) { return }

$esc = [char]27
$green = "$esc[38;5;108m"
$reset = "$esc[0m"

if ($mode -eq 'balanced' -or [string]::IsNullOrEmpty($mode)) {
  Write-Host -NoNewline "$green[humanizer]$reset"
} else {
  $suffix = $mode.ToUpper()
  Write-Host -NoNewline "$green[humanizer:$suffix]$reset"
}
