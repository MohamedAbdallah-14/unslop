# Humanizer hooks for Claude Code

Three small hook scripts that keep the humanizer persona active across a
session, without asking you to paste anything:

| File | Event | What it does |
|---|---|---|
| `humanizer-activate.js` | `SessionStart` | Emits the humanizer rules as hidden context and writes the active mode to `~/.claude/.humanizer-active`. |
| `humanizer-mode-tracker.js` | `UserPromptSubmit` | Watches your prompt for `/humanizer <mode>`, natural-language triggers (`"humanize this"`), and stop phrases (`"stop humanizer"`). Updates the flag file. |
| `humanizer-statusline.sh` / `.ps1` | `statusLine` | Prints a short `humanizer: <mode>` badge so you can see what's active. |

Everything under `hooks/` is plain JavaScript / Bash / PowerShell. No Claude
Code internals are touched — the installer only patches `settings.json`.

## Install (one command)

```bash
bash hooks/install.sh           # macOS / Linux / Git Bash
# or
powershell -File hooks\install.ps1   # Windows
```

The installer is idempotent. Run it again any time — it will skip any step
that's already done. To force a full reinstall:

```bash
bash hooks/install.sh --force
```

## Uninstall

```bash
bash hooks/uninstall.sh
```

Removes only the humanizer entries. Any existing `statusLine` or `hooks` you
had before we touched the file is preserved verbatim.

## Statusline integration

If you already have a custom statusline, the installer won't overwrite it.
To show the humanizer badge inside your existing statusline, append the
output of `humanizer-statusline.sh` to your own script:

```bash
# your-statusline.sh
bash ~/.claude/hooks/humanizer-statusline.sh
# ... the rest of your line ...
```

Windows: use `humanizer-statusline.ps1` the same way inside your own `.ps1`.

The badge is driven entirely by `~/.claude/.humanizer-active`. Any process
can read it. Any hook can overwrite it. The file is intentionally small and
boring so power users can script against it.

## Default mode

Precedence, highest first:

1. `HUMANIZER_DEFAULT_MODE` environment variable (`off`, `subtle`, `balanced`, `full`, `voice-match`, `anti-detector`)
2. `~/.config/humanizer/config.json` → `{ "defaultMode": "..." }`
3. Built-in default: `balanced`

Invalid values silently fall back to `balanced` so a typo never breaks the
flow.

## Security notes

- The flag file is written with `O_NOFOLLOW` and `0600` on Unix, and refuses
  to follow symlinks on Windows. An attacker who can drop a symlink into
  `~/.claude/` cannot redirect our writes into `/etc/passwd` or similar.
- The statusline script (`humanizer-statusline.sh`) refuses to read the
  flag file if it is a symlink. This is explicitly tested in
  `tests/test_hooks.py::test_statusline_refuses_symlink`.
- `CLAUDE_CONFIG_DIR` is honored everywhere. You can point every hook at a
  per-project directory if you don't want them touching `~/.claude`.

## Testing the hook scripts

```bash
python3 -m pytest tests/test_hooks.py -v
```

The test suite covers: fresh install, idempotent reinstall, custom
statusline preservation, uninstall cleanup, mode-flag writes, natural
language activation, stop phrases, and the symlink refusal.

## Troubleshooting

**"Nothing to do"** — the installer sees a valid humanizer install already.
Add `--force` if you want to overwrite.

**No banner on session start** — either `HUMANIZER_DEFAULT_MODE=off` is set,
or you set the flag file to `off`. Delete it:

```bash
rm ~/.claude/.humanizer-active
```

**Badge not showing** — the statusline is registered but another tool may
be stealing the slot. Run `bash hooks/humanizer-statusline.sh` manually;
if it prints, the hook is fine and the issue is elsewhere in your shell.
