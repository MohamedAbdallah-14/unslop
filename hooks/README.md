# Unslop hooks for Claude Code

Three small hook scripts that keep the unslop persona active across a
session, without asking you to paste anything:

| File | Event | What it does |
|---|---|---|
| `unslop-activate.js` | `SessionStart` | Emits the unslop rules as hidden context and writes the active mode to `~/.claude/.unslop-active`. |
| `unslop-mode-tracker.js` | `UserPromptSubmit` | Watches your prompt for `/unslop <mode>`, natural-language triggers (`"humanize this"`), and stop phrases (`"stop unslop"`). Updates the flag file. |
| `unslop-statusline.sh` / `.ps1` | `statusLine` | Prints a short `unslop: <mode>` badge so you can see what's active. |

Everything under `hooks/` is plain JavaScript / Bash / PowerShell. No Claude
Code internals are touched — the installer only patches `settings.json`.

## How it works

```
SessionStart hook ──writes mode──▶ $CLAUDE_CONFIG_DIR/.unslop-active ◀──writes mode── UserPromptSubmit hook
                                              │
                                           reads
                                              ▼
                                    Statusline script
                                  [unslop] / [unslop:FULL] / ...
```

`SessionStart` stdout is injected as hidden context — Claude sees it, the
user does not. The statusline runs as a separate process that reads the flag
file. The flag file is the bridge between the two write hooks and the
statusline reader.

`unslop-config.js` is not itself a hook — it's a shared module imported by
the two write hooks. It owns `safeWriteFlag` (symlink-refusing, atomic,
`O_NOFOLLOW`, `0600`) and `readFlag` (size-capped, whitelist-validated). Any
new hook that touches the flag file must go through these helpers.

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

Removes only the unslop entries. Any existing `statusLine` or `hooks` you
had before we touched the file is preserved verbatim.

## Statusline integration

If you already have a custom statusline, the installer won't overwrite it.
To show the unslop badge inside your existing statusline, append the
output of `unslop-statusline.sh` to your own script:

```bash
# your-statusline.sh
bash ~/.claude/hooks/unslop-statusline.sh
# ... the rest of your line ...
```

Windows: use `unslop-statusline.ps1` the same way inside your own `.ps1`.

The badge is driven entirely by `~/.claude/.unslop-active`. Any process
can read it. Any hook can overwrite it. The file is intentionally small and
boring so power users can script against it.

## Default mode

Precedence, highest first:

1. `UNSLOP_DEFAULT_MODE` environment variable (`off`, `subtle`, `balanced`, `full`, `voice-match`, `anti-detector`)
2. `~/.config/unslop/config.json` → `{ "defaultMode": "..." }`
3. Built-in default: `balanced`

Invalid values silently fall back to `balanced` so a typo never breaks the
flow.

## Security notes

- The flag file is written with `O_NOFOLLOW` and `0600` on Unix, and refuses
  to follow symlinks on Windows. An attacker who can drop a symlink into
  `~/.claude/` cannot redirect our writes into `/etc/passwd` or similar.
- The statusline script (`unslop-statusline.sh`) refuses to read the
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

**"Nothing to do"** — the installer sees a valid unslop install already.
Add `--force` if you want to overwrite.

**No banner on session start** — either `UNSLOP_DEFAULT_MODE=off` is set,
or you set the flag file to `off`. Delete it:

```bash
rm ~/.claude/.unslop-active
```

**Badge not showing** — the statusline is registered but another tool may
be stealing the slot. Run `bash hooks/unslop-statusline.sh` manually;
if it prints, the hook is fine and the issue is elsewhere in your shell.
