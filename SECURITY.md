# Security Policy

Thanks for helping keep `unslop` secure.

## Supported versions

Only the latest minor release line on `main` receives security fixes. The
project is pre-1.0 — pin to a specific version if you need stability.

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | ✅                 |
| < 0.4   | ❌                 |

## Reporting a vulnerability

**Do not open a public GitHub issue for a security problem.** Use one of these
private channels:

1. **Preferred — GitHub Security Advisory.**
   [Open a private advisory](https://github.com/MohamedAbdallah-14/unslop/security/advisories/new)
   on this repo. GitHub notifies the maintainer privately and gives us a
   workspace to coordinate a fix and a CVE if needed.
2. **Email.** If GitHub Advisories are not an option, email the maintainer
   listed in the repo profile with subject line
   `SECURITY: unslop vulnerability report`.

### What to include

- Affected version (`unslop --version`) and install method (PyPI, Claude Code
  plugin, hooks install script, Docker, source).
- Exact reproduction steps. Minimal proof-of-concept if you have one.
- The impact: what an attacker can read, write, execute, or escalate.
- Your environment: OS, Python version, whether `ANTHROPIC_API_KEY` is set,
  whether the `claude` CLI is on `PATH`.
- Whether you intend to publicly disclose, and your timeline.

### Response targets

- **Acknowledgement:** within 3 business days.
- **Triage + severity assessment:** within 7 business days.
- **Fix or mitigation:** depends on severity. Critical issues get an out-of-band
  release. Lower severity rolls into the next normal release with a note in
  `CHANGELOG.md`.

We will coordinate disclosure with you. Credit goes in the advisory unless you
ask to stay anonymous.

## What is in scope

- The `unslop` Python package (`unslop/scripts/**`).
- The hook scripts under `hooks/**` (Node + Bash + PowerShell).
- The install/uninstall scripts under `hooks/install.{sh,ps1}` and
  `hooks/uninstall.{sh,ps1}`.
- The skill manifests and rules under `skills/`, `rules/`,
  `.claude-plugin/`, mirrored locations under `.cursor/`, `.windsurf/`,
  `.codex/`, `.clinerules/`, `.github/copilot-instructions.md`,
  `gemini-extension.json`.
- The `Dockerfile` and CI/sync workflows under `.github/workflows/**`.

## What is out of scope

- Vulnerabilities in upstream dependencies (Anthropic SDK, Python stdlib,
  Node, etc.). Report those upstream. We will pick up patched versions via
  `dependabot.yml`.
- Issues that require an attacker to already have arbitrary code execution as
  the user running the tool.
- Bugs in third-party AI-detector models referenced from `benchmarks/`.
- Reports that the LLM produced insecure prose. `unslop` rewrites style, not
  semantics.

## Hardening notes (what `unslop` already does)

The Python core and the hooks are written defensively. Highlights:

- **Sensitive paths refused.** `unslop/scripts/detect.py::is_sensitive_path()`
  rejects `.env*`, `*.pem`, `*.key`, `*.crt`, `id_rsa*`, `~/.ssh/`,
  `~/.aws/`, `~/.gnupg/`, `~/.kube/`, `~/.docker/`, `secret*`, `credential*`,
  `password*`, `token*` **before** any read or API call.
- **No shell interpolation.** Subprocess calls (LLM-mode fallback to the
  `claude` CLI) always use `shell=False` and a fixed argument vector. User
  content goes via stdin.
- **File size cap.** Files larger than **500 KB** are refused before any API
  call. Caps per-call cost and per-call risk.
- **Symlink-safe flag writes.** `hooks/unslop-config.js::safeWriteFlag()`
  refuses if the flag target or its immediate parent is a symlink, opens with
  `O_NOFOLLOW`, writes atomically (temp + rename), and creates with `0600`.
  Protects against local attackers replacing the predictable flag path with a
  symlink to clobber files writable by the user.
- **Statusline reader is whitelist-validated.** `hooks/unslop-statusline.sh`
  caps reads at 64 bytes, strips non-alphanumerics, and validates the mode
  against a fixed allowlist before injecting it into the statusline.
- **Auth surface is explicit.** `ANTHROPIC_API_KEY` set → SDK only.
  Unset → `claude` CLI fallback. `--deterministic` → no subprocess and no
  network at all.

For a deeper rationale (including why scanners may flag subprocess use as
high-risk and why that rating is not actionable here), see
[`unslop/SECURITY.md`](./unslop/SECURITY.md).

## Disclosure history

None reported yet. This section will track resolved advisories with CVE IDs
when applicable.
