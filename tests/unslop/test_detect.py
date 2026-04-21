"""Tests for detect.py -- the safety gate that decides which files are humanizable.

This module has no existing tests, yet it's the first line of defense:
it's what stops us humanizing `.env`, SSH keys, binary files, and source
code. A false-positive here could corrupt a credentials file; a false-
negative just silently skips a markdown doc the user wanted processed."""

from __future__ import annotations

from pathlib import Path

from unslop.scripts.detect import (
    MAX_BYTES,
    detect_file_type,
    is_already_humanized_backup,
    is_sensitive_path,
    should_compress,
)


class TestSensitivePaths:
    """Anything that looks like a secret must be blocked."""

    def test_dotenv_blocked(self):
        assert is_sensitive_path(Path("/home/me/.env"))

    def test_dotenv_variants_blocked(self):
        assert is_sensitive_path(Path("/home/me/.env.local"))
        assert is_sensitive_path(Path("/home/me/.env.production"))
        assert is_sensitive_path(Path("/home/me/.env.staging"))

    def test_ssh_keys_blocked(self):
        assert is_sensitive_path(Path("/home/me/.ssh/id_rsa"))
        assert is_sensitive_path(Path("/home/me/.ssh/id_ed25519"))

    def test_pem_files_blocked(self):
        assert is_sensitive_path(Path("/etc/ssl/server.pem"))
        assert is_sensitive_path(Path("/etc/ssl/server.key"))

    def test_secret_in_name_blocked(self):
        assert is_sensitive_path(Path("/home/me/secret-notes.md"))
        assert is_sensitive_path(Path("/home/me/my-password.txt"))

    def test_ordinary_path_allowed(self):
        assert not is_sensitive_path(Path("/home/me/docs/readme.md"))


class TestDetectFileType:
    """Extension-based routing."""

    def test_markdown_is_natural_language(self):
        assert detect_file_type(Path("doc.md")) == "natural-language"
        assert detect_file_type(Path("README.markdown")) == "natural-language"

    def test_rst_and_txt(self):
        assert detect_file_type(Path("x.rst")) == "natural-language"
        assert detect_file_type(Path("notes.txt")) == "natural-language"

    def test_python_is_code(self):
        assert detect_file_type(Path("x.py")) == "code-or-config"

    def test_config_formats_are_code(self):
        for ext in ("yaml", "yml", "json", "toml", "ini"):
            assert detect_file_type(Path(f"x.{ext}")) == "code-or-config"

    def test_sensitive_takes_priority_over_extension(self):
        # An `.env.local.md` would match both an .md extension and the
        # sensitive check. Sensitive must win.
        assert detect_file_type(Path("/home/me/.env.local")) == "sensitive"

    def test_backup_files_detected(self):
        assert detect_file_type(Path("doc.original.md")) == "backup"
        assert detect_file_type(Path("notes.original.txt")) == "backup"

    def test_dotfile_without_extension_is_config(self):
        assert detect_file_type(Path("/home/me/.gitignore")) == "code-or-config"


class TestExtensionlessFiles:
    """The trickiest path: no extension, must sniff the content."""

    def test_known_natural_names(self, tmp_path):
        for name in ("README", "CHANGELOG", "LICENSE", "AUTHORS"):
            p = tmp_path / name
            p.write_text("Some prose here.\n", encoding="utf-8")
            assert detect_file_type(p) == "natural-language-extensionless", name

    def test_known_code_names(self, tmp_path):
        for name in ("Dockerfile", "Makefile", "Gemfile"):
            p = tmp_path / name
            p.write_text("FROM ubuntu\n", encoding="utf-8")
            assert detect_file_type(p) == "code-or-config", name

    def test_shebang_detected_as_code(self, tmp_path):
        p = tmp_path / "myscript"
        p.write_text("#!/usr/bin/env bash\necho hi\n", encoding="utf-8")
        assert detect_file_type(p) == "code-or-config"

    def test_binary_null_byte_detected(self, tmp_path):
        p = tmp_path / "payload"
        p.write_bytes(b"\x00\x01\x02binary data")
        assert detect_file_type(p) == "binary"

    def test_utf8_garbage_detected_as_binary(self, tmp_path):
        p = tmp_path / "blob"
        p.write_bytes(b"\xff\xfe\xfd\xfc")
        assert detect_file_type(p) == "binary"

    def test_prose_heuristic_accepts_english(self, tmp_path):
        p = tmp_path / "notes"
        p.write_text(
            "These are some written-out notes about the project. "
            "Most of the characters should be alphabetic, which is the "
            "signal the heuristic uses.\n",
            encoding="utf-8",
        )
        assert detect_file_type(p) == "natural-language-extensionless"

    def test_prose_heuristic_rejects_symbol_heavy(self, tmp_path):
        p = tmp_path / "weird"
        p.write_text(
            "{x:1}; [y]=(z); <a|b>={$c}; `|`;\\\\; ((1));",
            encoding="utf-8",
        )
        assert detect_file_type(p) == "unknown"


class TestShouldCompress:
    def test_markdown_allowed(self, tmp_path):
        p = tmp_path / "doc.md"
        p.write_text("Some prose.\n", encoding="utf-8")
        assert should_compress(p) is True

    def test_empty_file_rejected(self, tmp_path):
        p = tmp_path / "empty.md"
        p.write_text("", encoding="utf-8")
        assert should_compress(p) is False

    def test_oversize_file_rejected(self, tmp_path):
        p = tmp_path / "huge.md"
        p.write_text("x" * (MAX_BYTES + 1), encoding="utf-8")
        assert should_compress(p) is False

    def test_code_file_rejected(self, tmp_path):
        p = tmp_path / "x.py"
        p.write_text("print('hi')\n", encoding="utf-8")
        assert should_compress(p) is False

    def test_sensitive_path_rejected(self, tmp_path):
        p = tmp_path / ".env"
        p.write_text("SECRET=1\n", encoding="utf-8")
        assert should_compress(p) is False

    def test_backup_file_rejected(self, tmp_path):
        p = tmp_path / "doc.original.md"
        p.write_text("Some prose.\n", encoding="utf-8")
        assert should_compress(p) is False

    def test_missing_file_rejected(self, tmp_path):
        assert should_compress(tmp_path / "nope.md") is False


class TestHumanizedBackup:
    def test_original_md_suffix(self):
        assert is_already_humanized_backup(Path("doc.original.md"))

    def test_original_txt_suffix(self):
        assert is_already_humanized_backup(Path("notes.original.txt"))

    def test_ordinary_path_not_backup(self):
        assert not is_already_humanized_backup(Path("doc.md"))
