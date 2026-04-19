# Security

## Snyk High Risk Rating

`unslop` may show a High Risk rating in security scanners (Snyk, Bandit, etc.) because of two things: a subprocess invocation and file I/O on a user-provided path. Both are intentional and contained. This document explains exactly what the skill does and does not do.

### What triggers the rating

1. **Subprocess.** When `ANTHROPIC_API_KEY` is not set, the LLM-mode unslop calls the `claude` CLI via `subprocess.run()` to perform the rewrite.
   - Argument list is fixed (`["claude", "--print"]`).
   - No shell interpolation. `shell=False` always.
   - User file content is sent over **stdin**, not as a shell argument.
2. **File I/O.** The skill reads the user-specified path and writes two outputs back to disk: the humanized file (overwriting the original) and a `<stem>.original.md` backup alongside it.
   - No other paths are read or written.
   - `is_sensitive_path()` refuses paths matching `.env*`, `*.pem`, `*.key`, `*.crt`, `id_rsa*`, `~/.ssh/`, `~/.aws/`, `~/.gnupg/`, `~/.kube/`, `~/.docker/`, `secret*`, `credential*`, `password*`, `token*` before any read or API call.

### What the skill does NOT do

- Execute the user's file content as code.
- Make network calls except to the Anthropic API (via SDK or `claude` CLI).
- Access files outside the user-provided path.
- Use `shell=True` or string interpolation in `subprocess`.
- Collect or transmit anything beyond the file being humanized.

### Auth behavior

- `ANTHROPIC_API_KEY` set → uses the **Anthropic Python SDK**. No subprocess.
- `ANTHROPIC_API_KEY` unset → falls back to the **`claude` CLI** (relies on whatever desktop auth the user has configured for Claude Code).
- `--deterministic` flag → no subprocess and no network at all. Pure regex pass.

### File size limit

Files larger than **500 KB** are refused before any API call. This caps per-call cost and per-call risk.

### Reporting a vulnerability

Open a GitHub issue with the label `security`. For sensitive disclosures, prefer GitHub's private vulnerability reporting on the repo.
