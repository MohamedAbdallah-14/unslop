from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "unslop" / "SKILL.md"


def test_skill_md_no_8_to_13_percent():
    text = SKILL.read_text(encoding="utf-8")
    assert "8–13" not in text
    assert "8-13" not in text


def test_skill_md_cites_2507_21919():
    assert "2507.21919" in SKILL.read_text(encoding="utf-8")


def test_skill_md_cites_lvu():
    assert "2505.23854" in SKILL.read_text(encoding="utf-8")


def test_skill_md_cites_watermark_warning():
    assert "Watermark interaction" in SKILL.read_text(encoding="utf-8")
