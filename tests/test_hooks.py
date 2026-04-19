"""Integration tests for the unslop hook install/uninstall flow.

Run with:
    python3 -m pytest tests/test_hooks.py -v

These tests exercise the real install.sh / uninstall.sh / activate.js / mode-tracker.js
against a throwaway HOME directory. They catch regressions in:

- settings.json merge safety (does install clobber existing statusline/hooks?)
- idempotency (does a second install say "Nothing to do"?)
- uninstall cleanliness (does uninstall restore the prior state?)
- activate.js output (does it emit the UNSLOP MODE banner?)
- mode-tracker.js flag writes (does /unslop full set the flag to full?)
- natural-language activation ("humanize this" should set the flag)
- stop phrases ("stop unslop" should delete the flag)
- custom statusline detection (activate.js stays quiet if user has one)
- off-mode (UNSLOP_DEFAULT_MODE=off should skip activation)
- symlink attack refusal (safeWriteFlag must refuse symlink targets)

Node.js and bash are required. On Windows, the PowerShell counterparts are tested
via static assertions in `tests/verify_repo.py`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

HOOK_FILES = (
    "package.json",
    "unslop-config.js",
    "unslop-activate.js",
    "unslop-mode-tracker.js",
    "unslop-statusline.sh",
)


def _have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


@unittest.skipUnless(_have("node") and _have("bash"), "node and bash required")
class HookInstallFlow(unittest.TestCase):
    """End-to-end: install -> inspect -> activate -> uninstall -> inspect."""

    def _run(self, cmd, home, stdin: str | None = None, check: bool = True):
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env.pop("CLAUDE_CONFIG_DIR", None)
        return subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=check,
            input=stdin,
        )

    def test_fresh_install_wires_hooks_and_statusline(self):
        with tempfile.TemporaryDirectory(prefix="unslop-fresh-") as tmp:
            home = Path(tmp)
            self._run(["bash", "hooks/install.sh"], home)

            claude = home / ".claude"
            settings = json.loads((claude / "settings.json").read_text())

            for f in HOOK_FILES:
                self.assertTrue((claude / "hooks" / f).exists(), f"missing {f}")

            hooks = settings.get("hooks", {})
            self.assertIn("SessionStart", hooks)
            self.assertIn("UserPromptSubmit", hooks)
            self.assertIn("statusLine", settings)
            self.assertIn("unslop-statusline.sh", settings["statusLine"]["command"])

    def test_install_preserves_existing_custom_statusline(self):
        with tempfile.TemporaryDirectory(prefix="unslop-custom-") as tmp:
            home = Path(tmp)
            claude = home / ".claude"
            claude.mkdir(parents=True)
            existing = {
                "statusLine": {
                    "type": "command",
                    "command": "bash /tmp/user-statusline.sh",
                },
                "hooks": {
                    "Notification": [
                        {"hooks": [{"type": "command", "command": "echo keep-me"}]}
                    ]
                },
            }
            (claude / "settings.json").write_text(json.dumps(existing, indent=2) + "\n")

            self._run(["bash", "hooks/install.sh"], home)

            settings = json.loads((claude / "settings.json").read_text())
            self.assertEqual(
                settings["statusLine"]["command"],
                "bash /tmp/user-statusline.sh",
                "install.sh must not clobber existing statusline",
            )
            self.assertIn("Notification", settings["hooks"])

    def test_install_is_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="unslop-idem-") as tmp:
            home = Path(tmp)
            self._run(["bash", "hooks/install.sh"], home)
            second = self._run(["bash", "hooks/install.sh"], home)
            self.assertIn("Nothing to do", second.stdout)

    def test_activate_emits_banner_and_writes_flag(self):
        with tempfile.TemporaryDirectory(prefix="unslop-activate-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            result = self._run(["node", "hooks/unslop-activate.js"], home)
            self.assertIn("UNSLOP MODE ACTIVE", result.stdout)
            flag = home / ".claude" / ".unslop-active"
            self.assertTrue(flag.exists())
            self.assertEqual(flag.read_text().strip(), "balanced")

    def test_activate_respects_off_mode(self):
        with tempfile.TemporaryDirectory(prefix="unslop-off-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            env = os.environ.copy()
            env["HOME"] = str(home)
            env["UNSLOP_DEFAULT_MODE"] = "off"
            result = subprocess.run(
                ["node", "hooks/unslop-activate.js"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertNotIn("UNSLOP MODE ACTIVE", result.stdout)
            self.assertFalse((home / ".claude" / ".unslop-active").exists())

    def test_activate_quiet_when_user_has_statusline(self):
        with tempfile.TemporaryDirectory(prefix="unslop-have-sl-") as tmp:
            home = Path(tmp)
            claude = home / ".claude"
            claude.mkdir()
            (claude / "settings.json").write_text(
                json.dumps({"statusLine": {"type": "command", "command": "echo x"}})
            )
            result = self._run(["node", "hooks/unslop-activate.js"], home)
            self.assertNotIn("STATUSLINE SETUP NEEDED", result.stdout)

    def test_mode_tracker_slash_command(self):
        with tempfile.TemporaryDirectory(prefix="unslop-slash-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            self._run(
                ["node", "hooks/unslop-mode-tracker.js"],
                home,
                stdin='{"prompt":"/unslop full"}',
            )
            flag = home / ".claude" / ".unslop-active"
            self.assertTrue(flag.exists())
            self.assertEqual(flag.read_text().strip(), "full")

    def test_mode_tracker_natural_language_activate(self):
        with tempfile.TemporaryDirectory(prefix="unslop-nl-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            self._run(
                ["node", "hooks/unslop-mode-tracker.js"],
                home,
                stdin='{"prompt":"humanize this for me please"}',
            )
            flag = home / ".claude" / ".unslop-active"
            self.assertTrue(flag.exists())
            self.assertIn(flag.read_text().strip(), {"balanced", "subtle", "full"})

    def test_mode_tracker_stop_phrase_removes_flag(self):
        with tempfile.TemporaryDirectory(prefix="unslop-stop-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            flag = home / ".claude" / ".unslop-active"
            flag.write_text("full")
            self._run(
                ["node", "hooks/unslop-mode-tracker.js"],
                home,
                stdin='{"prompt":"stop unslop"}',
            )
            self.assertFalse(flag.exists())

    def test_statusline_outputs_badge(self):
        with tempfile.TemporaryDirectory(prefix="unslop-sl-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            (home / ".claude" / ".unslop-active").write_text("full")
            result = self._run(["bash", "hooks/unslop-statusline.sh"], home)
            self.assertIn("unslop", result.stdout.lower())
            self.assertIn("full", result.stdout.lower())

    def test_statusline_refuses_symlink(self):
        """Security: if flag is a symlink, statusline must not read it."""
        with tempfile.TemporaryDirectory(prefix="unslop-sym-") as tmp:
            home = Path(tmp)
            claude = home / ".claude"
            claude.mkdir()
            target = home / "secret.txt"
            target.write_text("SECRET_CONTENT")
            flag = claude / ".unslop-active"
            flag.symlink_to(target)
            result = self._run(["bash", "hooks/unslop-statusline.sh"], home)
            self.assertNotIn("SECRET_CONTENT", result.stdout)

    def test_uninstall_restores_prior_settings(self):
        with tempfile.TemporaryDirectory(prefix="unslop-unin-") as tmp:
            home = Path(tmp)
            claude = home / ".claude"
            claude.mkdir()
            prior = {
                "statusLine": {"type": "command", "command": "bash /tmp/mine.sh"},
                "hooks": {
                    "Notification": [
                        {"hooks": [{"type": "command", "command": "echo z"}]}
                    ]
                },
            }
            (claude / "settings.json").write_text(json.dumps(prior, indent=2) + "\n")
            self._run(["bash", "hooks/install.sh"], home)
            self._run(["bash", "hooks/uninstall.sh"], home)
            after = json.loads((claude / "settings.json").read_text())
            self.assertEqual(
                after["statusLine"]["command"],
                "bash /tmp/mine.sh",
                "uninstall must preserve user's custom statusline",
            )

    def test_claude_config_dir_env_var_honored(self):
        """CLAUDE_CONFIG_DIR should redirect flag file location."""
        with tempfile.TemporaryDirectory(prefix="unslop-env-") as tmp:
            custom = Path(tmp) / "custom-claude"
            custom.mkdir()
            env = os.environ.copy()
            env["CLAUDE_CONFIG_DIR"] = str(custom)
            env["HOME"] = tmp
            subprocess.run(
                ["node", "hooks/unslop-activate.js"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertTrue((custom / ".unslop-active").exists())


@unittest.skipUnless(_have("node"), "node required")
class ConfigResolution(unittest.TestCase):
    """Validate unslop-config.js mode resolution precedence."""

    def _probe(self, home: Path, extra_env: dict[str, str] | None = None) -> str:
        """Spawn node, call getDefaultMode(), print result."""
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env.pop("CLAUDE_CONFIG_DIR", None)
        env.pop("UNSLOP_DEFAULT_MODE", None)
        env.pop("XDG_CONFIG_HOME", None)
        if extra_env:
            env.update(extra_env)
        script = (
            "const c = require(process.cwd() + '/hooks/unslop-config.js');"
            "process.stdout.write(c.getDefaultMode());"
        )
        result = subprocess.run(
            ["node", "-e", script],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()

    def test_default_is_balanced(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._probe(Path(tmp)), "balanced")

    def test_env_var_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                self._probe(Path(tmp), {"UNSLOP_DEFAULT_MODE": "full"}),
                "full",
            )

    def test_config_file_used_when_env_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg_dir = home / ".config" / "unslop"
            cfg_dir.mkdir(parents=True)
            (cfg_dir / "config.json").write_text('{"defaultMode": "subtle"}')
            self.assertEqual(self._probe(home), "subtle")

    def test_invalid_mode_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg_dir = home / ".config" / "unslop"
            cfg_dir.mkdir(parents=True)
            (cfg_dir / "config.json").write_text('{"defaultMode": "notamode"}')
            self.assertEqual(
                self._probe(home, {"UNSLOP_DEFAULT_MODE": "alsobad"}),
                "balanced",
            )


if __name__ == "__main__":
    unittest.main()
