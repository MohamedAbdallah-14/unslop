"""Tests for unslop/scripts/style_memory.py."""

from __future__ import annotations

import json
import os

import pytest

from unslop.scripts.style_memory import (
    StyleMemoryError,
    clear_profile,
    format_summary,
    load_profile,
    save_profile,
)
from unslop.scripts.stylometry import StyleProfile

_SAMPLE = (
    "You'll find the config in /etc/platform/settings.yaml. It's not obvious — "
    "I missed it the first time. We use YAML because the legacy tooling can't "
    "parse JSON5. There's a migration underway but I wouldn't hold my breath. "
    "We'd prefer TOML honestly. But the migration cost is real and nobody has "
    "volunteered. So YAML it is. If you need to edit it, run the validator "
    "first. Don't skip it. Every on-call I've had started with a broken YAML "
    "edit. Seven times in the last quarter alone."
)


class TestSaveLoad:
    def test_roundtrip(self, tmp_path):
        target = tmp_path / "memory.json"
        save_profile(_SAMPLE, source="tests", path=target)
        profile = load_profile(target)
        assert profile is not None
        # The module's tokenizer (\b[A-Za-z']+\b) splits paths differently from
        # str.split; loose sanity check on order of magnitude.
        assert 70 < profile.total_words < 110
        assert profile.sentence_length_stdev >= 0.0
        assert profile.contraction_rate > 0.0

    def test_overwrite_replaces_not_merges(self, tmp_path):
        target = tmp_path / "memory.json"
        save_profile(_SAMPLE, path=target)
        # Save a different profile
        other = _SAMPLE + " Additional content to change the word count and signals."
        save_profile(other, path=target)
        p = load_profile(target)
        assert p is not None
        # The loaded profile should reflect the newer, longer sample.
        assert p.total_words > len(_SAMPLE.split()) * 0.9

    def test_file_mode_owner_only(self, tmp_path):
        target = tmp_path / "memory.json"
        save_profile(_SAMPLE, path=target)
        if os.name != "nt":
            mode = target.stat().st_mode & 0o777
            assert mode == 0o600

    def test_short_sample_rejected(self, tmp_path):
        target = tmp_path / "memory.json"
        with pytest.raises(StyleMemoryError, match="need ≥50"):
            save_profile("Too short.", path=target)

    def test_load_missing_returns_none(self, tmp_path):
        assert load_profile(tmp_path / "nope.json") is None


class TestClear:
    def test_clear_existing(self, tmp_path):
        target = tmp_path / "memory.json"
        save_profile(_SAMPLE, path=target)
        assert target.exists()
        assert clear_profile(target) is True
        assert not target.exists()

    def test_clear_nonexistent_returns_false(self, tmp_path):
        target = tmp_path / "not-here.json"
        assert clear_profile(target) is False


class TestSchemaValidation:
    def test_wrong_version_rejected(self, tmp_path):
        target = tmp_path / "memory.json"
        target.write_text(
            json.dumps({"version": 999, "profile": {"total_words": 100}}) + "\n"
        )
        with pytest.raises(StyleMemoryError, match="schema version"):
            load_profile(target)

    def test_missing_profile_rejected(self, tmp_path):
        target = tmp_path / "memory.json"
        target.write_text(json.dumps({"version": 1}) + "\n")
        with pytest.raises(StyleMemoryError, match="missing 'profile'"):
            load_profile(target)

    def test_malformed_json_rejected(self, tmp_path):
        target = tmp_path / "memory.json"
        target.write_text("{ not valid json")
        with pytest.raises(StyleMemoryError, match="Cannot read"):
            load_profile(target)

    def test_unknown_fields_ignored(self, tmp_path):
        target = tmp_path / "memory.json"
        # Save a valid profile, then add a stray field to the file.
        save_profile(_SAMPLE, path=target)
        data = json.loads(target.read_text())
        data["profile"]["unknown_future_field"] = "xyz"
        target.write_text(json.dumps(data))
        # Still loads cleanly.
        profile = load_profile(target)
        assert profile is not None


class TestSymlinkRefusal:
    @pytest.mark.skipif(os.name == "nt", reason="symlink handling differs on Windows")
    def test_save_refuses_symlink(self, tmp_path):
        real = tmp_path / "real.json"
        real.write_text("{}")
        link = tmp_path / "link.json"
        link.symlink_to(real)
        with pytest.raises(StyleMemoryError, match="symlink"):
            save_profile(_SAMPLE, path=link)

    @pytest.mark.skipif(os.name == "nt", reason="symlink handling differs on Windows")
    def test_load_refuses_symlink(self, tmp_path):
        real = tmp_path / "real.json"
        real.write_text("{}")
        link = tmp_path / "link.json"
        link.symlink_to(real)
        with pytest.raises(StyleMemoryError, match="symlink"):
            load_profile(link)

    @pytest.mark.skipif(os.name == "nt", reason="symlink handling differs on Windows")
    def test_clear_refuses_symlink(self, tmp_path):
        real = tmp_path / "real.json"
        real.write_text("{}")
        link = tmp_path / "link.json"
        link.symlink_to(real)
        with pytest.raises(StyleMemoryError, match="symlink"):
            clear_profile(link)


class TestFormatSummary:
    def test_none_summary(self):
        assert "No style memory" in format_summary(None)

    def test_profile_summary(self):
        p = StyleProfile(
            total_words=500,
            sentence_length_stdev=7.5,
            contraction_rate=40.0,
            second_person_rate=12.0,
        )
        out = format_summary(p)
        assert "500 words" in out
        assert "7.5" in out
