"""Phase 8 style memory: persist a StyleProfile per user.

Phase 4 shipped stylometric measurement; Phase 4-wire made it usable via
`--voice-sample PATH`. That still requires the sample on every invocation.
This module persists the measured profile so voice-match auto-loads.

Storage: $UNSLOP_STYLE_MEMORY, then $XDG_CONFIG_HOME/unslop/style-memory.json,
then ~/.config/unslop/style-memory.json (Linux/macOS) / %APPDATA%/unslop/
style-memory.json (Windows). First one set or existing wins.

Schema:
  {
    "version": 1,
    "profile": {StyleProfile.to_dict()},
    "sample_words": int,
    "saved_at": iso-8601 string,
    "source": str | null    # original file path or "stdin" when provided
  }

Security posture:
  - No PII collected. Profile is purely numeric — rates, ratios, counts.
  - File is created with mode 0600 (owner-only).
  - Symlink refused on both read and write (mirrors the hook flag-file
    pattern in hooks/unslop-config.js).
  - Schema validated on load; unknown fields ignored, missing required
    fields fail clean.

Not a hook. Pure CLI-driven save/load. Not linked to any session-level
state. Works offline.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path

from .stylometry import StyleProfile, analyze

_SCHEMA_VERSION = 1


class StyleMemoryError(RuntimeError):
    """Raised when the memory file is present but unreadable / malformed."""


def _default_path() -> Path:
    env = os.environ.get("UNSLOP_STYLE_MEMORY")
    if env:
        return Path(env).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg).expanduser() / "unslop" / "style-memory.json"
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "unslop" / "style-memory.json"
    return Path.home() / ".config" / "unslop" / "style-memory.json"


def _refuse_symlink(path: Path) -> None:
    """If `path` exists and is a symlink, refuse. Same reasoning as the
    flag-file pattern in hooks/unslop-config.js: predictable user-owned
    paths are a local-attack surface for symlink-clobber tricks."""
    if path.is_symlink():
        raise StyleMemoryError(
            f"Refusing to touch symlink at {path}. "
            "Remove or replace with a regular file."
        )


def save_profile(
    sample_text: str,
    *,
    source: str | None = None,
    path: Path | None = None,
) -> Path:
    """Measure the sample's profile and persist it. Returns the path written.

    Overwrites any existing memory. The profile replaces, it does not merge —
    a new sample is the new voice. Profiles under 50 words raise
    StyleMemoryError because their signals are too noisy to commit."""
    profile = analyze(sample_text)
    if profile.total_words < 50:
        raise StyleMemoryError(
            f"Sample is {profile.total_words} words; need ≥50 for stable "
            "signals. Use a larger sample."
        )

    target = path or _default_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    _refuse_symlink(target)

    payload = {
        "version": _SCHEMA_VERSION,
        "profile": profile.to_dict(),
        "sample_words": profile.total_words,
        "saved_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
    }

    # Atomic write: temp file in same directory, then rename.
    fd, tmp_path = tempfile.mkstemp(
        prefix="style-memory-", suffix=".json.tmp", dir=str(target.parent)
    )
    os.close(fd)
    tmp = Path(tmp_path)
    try:
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
    return target


def load_profile(path: Path | None = None) -> StyleProfile | None:
    """Read the persisted profile. Returns None if no file; raises
    StyleMemoryError on a malformed file or symlink."""
    target = path or _default_path()
    if not target.exists():
        return None
    _refuse_symlink(target)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StyleMemoryError(f"Cannot read {target}: {exc}") from exc

    if not isinstance(data, dict):
        raise StyleMemoryError(f"{target}: expected a JSON object, got {type(data).__name__}")

    version = data.get("version")
    if version != _SCHEMA_VERSION:
        raise StyleMemoryError(
            f"{target}: schema version {version!r}, expected {_SCHEMA_VERSION}. "
            "Clear and re-save the profile."
        )

    profile_data = data.get("profile")
    if not isinstance(profile_data, dict):
        raise StyleMemoryError(f"{target}: missing 'profile' object")

    # Filter to known StyleProfile fields so extra keys don't crash construction.
    known_fields = set(asdict(StyleProfile()).keys())
    kwargs = {k: v for k, v in profile_data.items() if k in known_fields}
    try:
        return StyleProfile(**kwargs)
    except TypeError as exc:
        raise StyleMemoryError(f"{target}: cannot reconstruct profile: {exc}") from exc


def clear_profile(path: Path | None = None) -> bool:
    """Delete the persisted profile. Returns True if a file was removed,
    False if nothing was there. Symlinks are refused."""
    target = path or _default_path()
    if not target.exists():
        return False
    _refuse_symlink(target)
    target.unlink()
    return True


def format_summary(profile: StyleProfile | None) -> str:
    """Short, user-facing description of the current memory state."""
    if profile is None:
        return "No style memory on file."
    return (
        f"Style memory: {profile.total_words} words of sample measured. "
        f"Sentence σ={profile.sentence_length_stdev}; "
        f"contractions/1k={profile.contraction_rate}; "
        f"second-person/1k={profile.second_person_rate}."
    )
