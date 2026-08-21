#!/usr/bin/env python3
"""Repo integrity verifier for the unslop plugin.

Run locally before releasing:

    python3 tests/verify_repo.py

Checks (each failure is fatal):

  1. SSOT mirrors are byte-identical to their sources after running sync-mirrors.sh.
  2. All JSON manifests parse cleanly (plugin.json, marketplace.json, etc).
  3. All JS hooks pass `node --check` (syntax-valid).
  4. All shell scripts pass `bash -n` (syntax-valid).
  5. Install / uninstall scripts reference every required hook file.
  6. Windows install paths statically wire the PowerShell statusline.
  7. unslop modules import without errors.
  8. humanize_deterministic round-trips every fixture pair and the result
     matches the committed `.md` output (detects accidental regex drift).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckFailure(RuntimeError):
    pass


def section(title: str) -> None:
    print(f"\n== {title} ==")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(
    args: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        args,
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise CheckFailure(
            f"Command failed ({result.returncode}): {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def read_json(path: Path) -> object:
    return json.loads(path.read_text())


def verify_synced_mirrors() -> None:
    section("Synced Mirrors")
    # Run sync-mirrors.sh first — that's what CI does.
    run(["bash", "scripts/sync-mirrors.sh"])

    skill_source = ROOT / "skills/unslop/SKILL.md"
    rule_source = ROOT / "rules/unslop-activate.md"

    skill_copies = [
        ROOT / "plugins/unslop/skills/unslop/SKILL.md",
        ROOT / ".cursor/skills/unslop/SKILL.md",
        ROOT / ".windsurf/skills/unslop/SKILL.md",
    ]
    for copy in skill_copies:
        ensure(copy.exists(), f"Missing skill mirror: {copy}")
        ensure(
            copy.read_text() == skill_source.read_text(),
            f"Skill mirror drifted: {copy}",
        )

    # Activation rule has per-platform headers, so we substring-match the body.
    rule_body = rule_source.read_text().strip()
    for copy in [
        ROOT / ".clinerules/unslop.md",
        ROOT / ".github/copilot-instructions.md",
        ROOT / ".cursor/rules/unslop.mdc",
        ROOT / ".windsurf/rules/unslop.md",
    ]:
        ensure(copy.exists(), f"Missing rule mirror: {copy}")
        ensure(
            rule_body in copy.read_text(),
            f"Rule mirror missing body of {rule_source.name}: {copy}",
        )

    # File-rewriter package must be mirrored to the plugin bundle and skills/unslop-file.
    pkg_src = ROOT / "unslop"
    for mirror in [
        ROOT / "plugins/unslop/skills/unslop-file",
        ROOT / "skills/unslop-file",
    ]:
        ensure(
            (mirror / "SKILL.md").read_text()
            == (pkg_src / "SKILL.md").read_text(),
            f"unslop-file SKILL.md drift: {mirror}",
        )
        for py in (pkg_src / "scripts").glob("*.py"):
            target = mirror / "scripts" / py.name
            ensure(target.exists(), f"Missing script mirror: {target}")
            ensure(
                target.read_text() == py.read_text(),
                f"Script mirror drifted: {target}",
            )

    print("Skill, rule, and humanize-package mirrors OK")


def verify_sync_workflow_triggers() -> None:
    section("Sync workflow triggers")
    workflow = (ROOT / ".github/workflows/sync.yml").read_text()
    authoritative_paths = (
        "skills/unslop/SKILL.md",
        "skills/unslop-commit/SKILL.md",
        "skills/unslop-review/SKILL.md",
        "skills/unslop-help/SKILL.md",
        "skills/unslop-reasoning/SKILL.md",
        "rules/unslop-activate.md",
        "unslop/SKILL.md",
        "unslop/scripts/**",
        "CHANGELOG.md",
        "scripts/sync-mirrors.sh",
    )
    for path in authoritative_paths:
        ensure(path in workflow, f"sync.yml missing SSOT trigger: {path}")
    print("Every mirrored SSOT path triggers sync.yml")


def verify_manifests_and_syntax() -> None:
    section("Manifests and Syntax")

    manifests = [
        ROOT / ".claude-plugin/plugin.json",
        ROOT / ".claude-plugin/marketplace.json",
        ROOT / ".cursor-plugin/plugin.json",
        ROOT / "gemini-extension.json",
        ROOT / "plugins/unslop/.codex-plugin/plugin.json",
    ]
    # Optional manifests — some may not yet exist
    optional = [
        ROOT / ".agents/plugins/marketplace.json",
        ROOT / ".codex/hooks.json",
    ]
    for m in manifests:
        ensure(m.exists(), f"Missing required manifest: {m}")
        read_json(m)
    for m in optional:
        if m.exists():
            read_json(m)

    for js in [
        "hooks/unslop-config.js",
        "hooks/unslop-activate.js",
        "hooks/unslop-mode-tracker.js",
    ]:
        run(["node", "--check", js])

    for sh in [
        "hooks/install.sh",
        "hooks/uninstall.sh",
        "hooks/unslop-statusline.sh",
        "scripts/sync-mirrors.sh",
    ]:
        run(["bash", "-n", sh])

    install_sh = (ROOT / "hooks/install.sh").read_text()
    uninstall_sh = (ROOT / "hooks/uninstall.sh").read_text()
    for needed in (
        "unslop-config.js",
        "unslop-activate.js",
        "unslop-mode-tracker.js",
        "unslop-statusline.sh",
    ):
        ensure(needed in install_sh, f"install.sh missing {needed}")
        ensure(needed in uninstall_sh, f"uninstall.sh missing {needed}")

    print("JSON manifests parse; JS + bash syntax clean")


def verify_powershell_static() -> None:
    section("PowerShell (static)")
    install_ps1 = (ROOT / "hooks/install.ps1").read_text()
    uninstall_ps1 = (ROOT / "hooks/uninstall.ps1").read_text()
    statusline_ps1 = (ROOT / "hooks/unslop-statusline.ps1").read_text()

    for needed in (
        "unslop-config.js",
        "unslop-activate.js",
        "unslop-mode-tracker.js",
        "unslop-statusline.ps1",
    ):
        ensure(needed in install_ps1, f"install.ps1 missing {needed}")
        ensure(needed in uninstall_ps1, f"uninstall.ps1 missing {needed}")

    ensure("-AsHashtable" not in install_ps1, "install.ps1 must stay PS 5.1 compatible")
    ensure(
        "powershell -ExecutionPolicy Bypass -File" in install_ps1,
        "install.ps1 missing PS statusline wiring",
    )
    ensure("unslop" in statusline_ps1.lower(), "statusline.ps1 must emit unslop badge")

    print("Windows install path statically wired")


def verify_humanize_modules_importable() -> None:
    section("humanize package importable")
    sys.path.insert(0, str(ROOT / "unslop"))
    try:
        import scripts.benchmark  # noqa: F401
        import scripts.cli as cli  # noqa: F401
        import scripts.detect as detect
        import scripts.humanize as humanize
        import scripts.validate as validate
    except Exception as exc:
        raise CheckFailure(f"humanize package import failed: {exc}")
    # Smoke: the core surface has the expected callables.
    for name in ("humanize_deterministic", "humanize_file"):
        ensure(hasattr(humanize, name), f"humanize.{name} missing")
    for name in ("validate", "format_report"):
        ensure(hasattr(validate, name), f"validate.{name} missing")
    for name in ("detect_file_type", "should_compress", "is_sensitive_path"):
        ensure(hasattr(detect, name), f"detect.{name} missing")
    print("Core Python API surface present")


def verify_fixture_pairs() -> None:
    section("Fixture pairs")
    sys.path.insert(0, str(ROOT / "unslop"))
    from scripts.humanize import humanize_deterministic
    from scripts.validate import validate

    fixtures_dir = ROOT / "tests/unslop/fixtures"
    if not fixtures_dir.exists():
        print("  (no fixtures/ dir — skipping)")
        return

    pairs = sorted(fixtures_dir.glob("*.original.md"))
    ensure(pairs, f"No fixture pairs in {fixtures_dir}")

    errors: list[str] = []
    for original in pairs:
        expected = original.with_name(original.name.replace(".original.md", ".md"))
        if not expected.exists():
            errors.append(f"missing expected output for {original.name}")
            continue
        actual = humanize_deterministic(original.read_text())
        if actual != expected.read_text():
            errors.append(
                f"{original.name}: humanize_deterministic output drifted "
                f"from committed {expected.name}"
            )
        result = validate(original.read_text(), expected.read_text())
        if not result.ok:
            errors.append(f"{expected.name}: committed output fails validator: {result.errors}")

    ensure(not errors, "Fixture failures:\n  " + "\n  ".join(errors))
    print(f"Validated {len(pairs)} fixture pair(s) — no drift")


def verify_commands_wired() -> None:
    section("Commands and plugin manifest")
    plugin = read_json(ROOT / ".claude-plugin/plugin.json")
    ensure(plugin.get("name") == "unslop", "plugin.json name mismatch")
    hooks_block = plugin.get("hooks", {})
    ensure("SessionStart" in hooks_block, "plugin.json missing SessionStart")
    ensure("UserPromptSubmit" in hooks_block, "plugin.json missing UserPromptSubmit")

    commands_dir = ROOT / "commands"
    toml_files = list(commands_dir.glob("*.toml"))
    ensure(toml_files, "no slash command TOMLs found")

    mkt = read_json(ROOT / ".claude-plugin/marketplace.json")
    ensure(mkt.get("plugins"), "marketplace.json missing plugins array")
    ensure("displayName" not in mkt, "marketplace root displayName is not supported")

    print("Plugin + marketplace wired")


def verify_cursor_plugin() -> None:
    section("Cursor plugin")
    manifest_path = ROOT / ".cursor-plugin/plugin.json"
    manifest = read_json(manifest_path)

    ensure(manifest.get("name") == "unslop", "Cursor plugin name mismatch")
    ensure(isinstance(manifest.get("version"), str), "Cursor plugin version missing")
    ensure("commands" not in manifest, "Cursor plugin must not expose TOML commands")

    for field in ("skills", "rules", "logo"):
        value = manifest.get(field)
        ensure(isinstance(value, str) and value, f"Cursor plugin {field} path missing")
        relative = Path(value)
        ensure(not relative.is_absolute(), f"Cursor plugin {field} path must be relative")
        ensure(".." not in relative.parts, f"Cursor plugin {field} path must not contain '..'")
        ensure((ROOT / relative).exists(), f"Cursor plugin {field} path missing: {value}")

    skills_dir = ROOT / manifest["skills"]
    ensure(
        any(skills_dir.glob("*/SKILL.md")),
        "Cursor plugin skills path contains no skills",
    )
    rules_dir = ROOT / manifest["rules"]
    ensure(any(rules_dir.glob("*.mdc")), "Cursor plugin rules path contains no .mdc files")
    ensure(Path(manifest["logo"]).suffix == ".svg", "Cursor plugin logo must be SVG")

    print("Cursor plugin manifest and component paths wired")


def verify_codex_plugin() -> None:
    section("Codex plugin")
    plugin_root = ROOT / "plugins/unslop"
    manifest = read_json(plugin_root / ".codex-plugin/plugin.json")
    ensure(manifest.get("name") == plugin_root.name, "Codex plugin folder/name mismatch")
    ensure(isinstance(manifest.get("author"), dict), "Codex author must be an object")
    ensure("displayName" not in manifest, "Codex displayName belongs under interface")
    ensure("ui" not in manifest, "Codex uses interface, not ui")
    ensure("defaultPrompt" not in manifest, "Codex defaultPrompt belongs under interface")
    interface = manifest.get("interface")
    ensure(isinstance(interface, dict), "Codex interface metadata missing")
    for field in ("displayName", "shortDescription", "longDescription", "developerName"):
        ensure(interface.get(field), f"Codex interface.{field} missing")
    skills_path = manifest.get("skills")
    ensure(
        isinstance(skills_path, str) and skills_path.startswith("./"),
        "Codex skills path invalid",
    )
    ensure((plugin_root / skills_path).exists(), f"Codex skills path missing: {skills_path}")
    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        ensure(isinstance(value, str) and value.startswith("./"), f"Codex {field} path invalid")
        ensure((plugin_root / value).is_file(), f"Codex {field} path missing: {value}")

    marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
    ensure(isinstance(marketplace.get("interface"), dict), "Agents marketplace interface missing")
    ensure(marketplace.get("plugins"), "Agents marketplace plugins missing")
    entry = marketplace["plugins"][0]
    ensure(entry.get("name") == manifest["name"], "Agents marketplace plugin name mismatch")
    ensure(
        entry.get("source") == {"source": "local", "path": "./plugins/unslop"},
        "Agents marketplace source metadata invalid",
    )
    ensure(
        entry.get("policy")
        == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "Agents marketplace policy metadata invalid",
    )
    ensure(entry.get("category"), "Agents marketplace category missing")
    print("Codex plugin and repo marketplace use the current schema")


def verify_gemini_extension() -> None:
    section("Gemini extension")
    manifest = read_json(ROOT / "gemini-extension.json")
    ensure("contextFiles" not in manifest, "Gemini ignores the contextFiles field")
    context_files = manifest.get("contextFileName")
    ensure(isinstance(context_files, list) and context_files, "Gemini context list missing")
    for relative in context_files:
        ensure(isinstance(relative, str), "Gemini context path must be a string")
        path = Path(relative)
        ensure(not path.is_absolute() and ".." not in path.parts, "Gemini context path invalid")
        ensure((ROOT / relative).is_file(), f"Gemini context path missing: {relative}")
    print("Gemini context files use the supported manifest field")


def verify_version_alignment() -> None:
    section("Version alignment")
    sys.path.insert(0, str(ROOT / "unslop"))
    from scripts import __version__

    expected = __version__
    version_sources = {
        "unslop/scripts/__init__.py": expected,
        ".claude-plugin/plugin.json": read_json(ROOT / ".claude-plugin/plugin.json").get(
            "version"
        ),
        ".claude-plugin/marketplace.json": read_json(ROOT / ".claude-plugin/marketplace.json")[
            "plugins"
        ][0]["version"],
        "gemini-extension.json": read_json(ROOT / "gemini-extension.json")["version"],
        "plugins/unslop/.codex-plugin/plugin.json": read_json(
            ROOT / "plugins/unslop/.codex-plugin/plugin.json"
        )["version"],
        ".codex/hooks.json": read_json(ROOT / ".codex/hooks.json")["version"],
        ".cursor-plugin/plugin.json": read_json(ROOT / ".cursor-plugin/plugin.json")[
            "version"
        ],
    }

    for label, version in version_sources.items():
        ensure(version == expected, f"{label} version {version!r} != {expected!r}")

    cli_version = run(
        [sys.executable, "-m", "scripts.cli", "--version"],
        cwd=ROOT / "unslop",
    ).stdout.strip()
    ensure(cli_version == f"unslop {expected}", f"CLI version mismatch: {cli_version!r}")

    root_changelog = (ROOT / "CHANGELOG.md").read_text()
    package_changelog = (ROOT / "unslop/CHANGELOG.md").read_text()
    ensure(
        re.search(rf"^## \[{re.escape(expected)}\] ", root_changelog, re.MULTILINE)
        is not None,
        "root CHANGELOG latest version heading missing",
    )
    ensure(
        re.search(rf"^## {re.escape(expected)} ", package_changelog, re.MULTILINE) is not None,
        "package CHANGELOG latest version heading missing",
    )

    print(f"All public version signals match {expected}")


def verify_package_metadata() -> None:
    section("Package metadata")
    pyproject = (ROOT / "unslop/pyproject.toml").read_text()
    ensure(
        'surprisal = ["torch", "transformers"]' in pyproject,
        "surprisal extra must contain only its imported dependencies",
    )
    ensure(
        'detector = ["torch", "transformers", "huggingface_hub", "safetensors"]'
        in pyproject,
        "detector extra missing detector runtime dependencies",
    )
    ensure("scipy" not in pyproject, "unused scipy dependency must not ship")
    print("Optional dependency groups match runtime imports")


def main() -> int:
    checks = [
        verify_synced_mirrors,
        verify_sync_workflow_triggers,
        verify_manifests_and_syntax,
        verify_powershell_static,
        verify_humanize_modules_importable,
        verify_fixture_pairs,
        verify_commands_wired,
        verify_cursor_plugin,
        verify_codex_plugin,
        verify_gemini_extension,
        verify_version_alignment,
        verify_package_metadata,
    ]
    try:
        for check in checks:
            check()
    except CheckFailure as exc:
        print(f"\nFAIL: {exc}", file=sys.stderr)
        return 1

    print("\nAll repo verification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
