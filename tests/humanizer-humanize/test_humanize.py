"""Tests for humanizer-humanize.

Run with: pytest tests/humanizer-humanize/

The deterministic mode is fully tested. LLM mode is smoke-tested only when
ANTHROPIC_API_KEY is present.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "humanizer-humanize"))

from scripts.detect import detect_file_type, is_sensitive_path, should_compress
from scripts.humanize import humanize_deterministic
from scripts.validate import validate


# ---------- detect.py ----------


class TestDetect:
    def test_markdown_is_natural_language(self, tmp_path: Path) -> None:
        f = tmp_path / "doc.md"
        f.write_text("hello")
        assert detect_file_type(f) == "natural-language"

    def test_python_is_code(self, tmp_path: Path) -> None:
        f = tmp_path / "script.py"
        f.write_text("print('hi')")
        assert detect_file_type(f) == "code-or-config"

    def test_extensionless_dockerfile_is_code(self, tmp_path: Path) -> None:
        f = tmp_path / "Dockerfile"
        f.write_text("FROM python:3.12\nRUN pip install -r requirements.txt\n")
        assert detect_file_type(f) == "code-or-config"
        assert not should_compress(f)

    def test_dotfile_is_code_or_config(self, tmp_path: Path) -> None:
        f = tmp_path / ".gitignore"
        f.write_text("*.pyc\n")
        assert detect_file_type(f) == "code-or-config"
        assert not should_compress(f)

    def test_extensionless_notes_is_natural_language(self, tmp_path: Path) -> None:
        f = tmp_path / "NOTES"
        f.write_text("Great question! It's important to note that this is prose.\n")
        assert detect_file_type(f) == "natural-language-extensionless"
        assert should_compress(f)

    def test_env_file_is_sensitive(self, tmp_path: Path) -> None:
        f = tmp_path / ".env"
        f.write_text("SECRET=x")
        assert is_sensitive_path(f)
        assert not should_compress(f)

    def test_pem_is_sensitive(self, tmp_path: Path) -> None:
        f = tmp_path / "id_rsa.pem"
        f.write_text("---")
        assert is_sensitive_path(f)

    def test_already_humanized_backup(self, tmp_path: Path) -> None:
        f = tmp_path / "notes.original.md"
        f.write_text("hi")
        assert detect_file_type(f) == "backup"
        assert not should_compress(f)

    def test_oversize_refused(self, tmp_path: Path) -> None:
        f = tmp_path / "big.md"
        f.write_text("a" * (600 * 1024))
        assert not should_compress(f)

    def test_empty_refused(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.md"
        f.write_text("")
        assert not should_compress(f)


# ---------- humanize.py: deterministic ----------


class TestDeterministicSycophancy:
    def test_strips_great_question(self) -> None:
        out = humanize_deterministic("Great question! Here is the answer.")
        assert not out.lower().startswith("great question")
        assert "Here is the answer" in out

    def test_strips_certainly(self) -> None:
        out = humanize_deterministic("Certainly! I will help.")
        assert "Certainly" not in out
        assert "I will help" in out

    def test_strips_stacked_openers(self) -> None:
        text = "Great question! I'd be happy to help with this. Here is the real content."
        out = humanize_deterministic(text)
        assert "Great question" not in out
        assert "happy to help" not in out.lower()
        assert "Here is the real content" in out


class TestDeterministicHedging:
    def test_strips_important_to_note(self) -> None:
        out = humanize_deterministic("It's important to note that tests should pass.")
        assert "important to note" not in out.lower()
        assert "Tests should pass" in out

    def test_strips_worth_mentioning(self) -> None:
        out = humanize_deterministic("It's worth mentioning that performance matters.")
        assert "worth mentioning" not in out.lower()
        assert "Performance matters" in out

    def test_strips_stacked_hedging(self) -> None:
        out = humanize_deterministic(
            "It's worth mentioning that, generally speaking, you should run tests."
        )
        assert "worth mentioning" not in out.lower()
        assert "generally speaking" not in out.lower()
        assert "You should run tests" in out


class TestDeterministicStockVocab:
    def test_strips_delve(self) -> None:
        out = humanize_deterministic("Let's delve into the topic.")
        assert "delve" not in out.lower()

    def test_strips_leverage_all_forms(self) -> None:
        out = humanize_deterministic(
            "We leverage caching. The system leverages it. We leveraged X. We are leveraging Y."
        )
        assert "leverag" not in out.lower()

    def test_strips_seamless(self) -> None:
        out = humanize_deterministic("The seamless integration works seamlessly.")
        assert "seamless" not in out.lower()
        assert "smooth" in out.lower()

    def test_navigate_kept_when_literal(self) -> None:
        out = humanize_deterministic("Use the keyboard to navigate to the next page.")
        assert "navigate" in out.lower()

    def test_navigate_replaced_when_figurative(self) -> None:
        out = humanize_deterministic("We navigate the complex regulatory landscape.")
        assert "navigate the" not in out.lower()


class TestDeterministicPerformative:
    def test_strips_however_at_sentence_start(self) -> None:
        out = humanize_deterministic("Tests pass. However, coverage is low.")
        assert "however" not in out.lower()
        assert "Coverage is low" in out

    def test_collapses_mid_sentence_however(self) -> None:
        out = humanize_deterministic("Tests pass, however, coverage is low.")
        assert "however" not in out.lower()


class TestDeterministicTransitionTics:
    def test_strips_furthermore_at_sentence_start(self) -> None:
        out = humanize_deterministic("Tests pass. Furthermore, coverage is good.")
        assert "furthermore" not in out.lower()
        assert "Coverage is good" in out

    def test_strips_moreover(self) -> None:
        out = humanize_deterministic("Tests pass. Moreover, the API is stable.")
        assert "moreover" not in out.lower()

    def test_strips_additionally(self) -> None:
        out = humanize_deterministic("Tests pass. Additionally, docs are updated.")
        assert "additionally" not in out.lower()

    def test_strips_in_conclusion(self) -> None:
        out = humanize_deterministic("We wrote tests. In conclusion, this is safe.")
        assert "in conclusion" not in out.lower()

    def test_keeps_furthermore_mid_sentence(self) -> None:
        # "Furthermore" can legitimately appear mid-sentence. Only strip at sentence start.
        out = humanize_deterministic("He looked at her and saw, furthermore, great sadness.")
        # Note: the regex requires ". " before to match, so this legitimately stays.
        assert "furthermore" in out.lower()


class TestDeterministicEmDashCap:
    def test_keeps_two_em_dashes_per_paragraph(self) -> None:
        text = "One thing — and another — stays."
        out = humanize_deterministic(text)
        assert out.count("—") == 2

    def test_replaces_third_em_dash_with_comma(self) -> None:
        text = "First — second — third — fourth — end."
        out = humanize_deterministic(text)
        assert out.count("—") == 2
        assert "third , fourth , end" in out or "third, fourth, end" in out.replace("  ", " ")

    def test_em_dash_count_resets_per_paragraph(self) -> None:
        text = "One — two — three — four.\n\nAnother — paragraph — here — too."
        out = humanize_deterministic(text)
        # Each paragraph keeps up to 2 em-dashes independently.
        assert out.count("—") == 4

    def test_each_bullet_gets_its_own_em_dash_budget(self) -> None:
        """Research: Cat 04 — list items are rhythmically separate."""
        text = (
            "- first bullet — has one dash\n"
            "- second bullet — has one dash\n"
            "- third bullet — has one dash\n"
            "- fourth bullet — has one dash"
        )
        out = humanize_deterministic(text)
        assert out.count("—") == 4, f"expected 4 em-dashes, got {out.count('—')}: {out!r}"

    def test_abbreviation_does_not_trigger_sentence_capitalize(self) -> None:
        """Regression: 'i.e. not' was becoming 'i.e. Not'.

        Common abbreviations (i.e., e.g., etc., et al., Dr., Mr., St., No.) end
        with a period but do not end a sentence. Capitalizing the next word is a
        humanizer bug."""
        cases = [
            "Use the flag (i.e. not the env var) for this case.",
            "For tools e.g. ripgrep, the syntax differs.",
            "Pens, pencils, etc. go in the drawer.",
            "See Smith et al. for the original experiment.",
            "Dr. smith reviewed the paper.",
            "The manager (Mr. jones) approved it.",
        ]
        for text in cases:
            out = humanize_deterministic(text)
            # Whatever else changes, the lowercase word after the abbreviation period stays lowercase.
            assert out == text, f"Unexpected change: {text!r} -> {out!r}"

    def test_intro_line_before_bullets_does_not_eat_budget(self) -> None:
        """Regression: 'Exports:\\n- a — b\\n- c — d' was collapsing bullets 3+ dashes.

        The intro line joined the bullets into one paragraph, which then shared
        a single budget of 2. Each bullet must have its own budget regardless of
        a leading prose line."""
        text = (
            "Exports:\n"
            "- `a()` — does thing one\n"
            "- `b()` — does thing two\n"
            "- `c()` — does thing three\n"
            "- `d()` — does thing four"
        )
        out = humanize_deterministic(text)
        assert out.count("—") == 4, f"expected 4 em-dashes, got {out.count('—')}: {out!r}"


class TestPreservation:
    def test_code_block_preserved_byte_for_byte(self) -> None:
        text = (
            "Great question! Here is the code:\n\n"
            "```python\n"
            "def delve():  # AI-ism here MUST stay\n"
            "    leverage = 'comprehensive'\n"
            "    return leverage\n"
            "```\n\n"
            "Done."
        )
        out = humanize_deterministic(text)
        assert "def delve():  # AI-ism here MUST stay" in out
        assert "leverage = 'comprehensive'" in out

    def test_inline_code_preserved(self) -> None:
        text = "Great question! Use `delve()` here."
        out = humanize_deterministic(text)
        assert "`delve()`" in out

    def test_indented_code_block_preserved_byte_for_byte(self) -> None:
        text = (
            "Great question! Here is code:\n\n"
            "    def delve():\n"
            "        leverage = 'comprehensive'\n"
            "        return leverage\n"
        )
        out = humanize_deterministic(text)
        assert "    def delve():" in out
        assert "        leverage = 'comprehensive'" in out

    def test_url_preserved(self) -> None:
        text = "Certainly! See https://example.com/delve for more."
        out = humanize_deterministic(text)
        assert "https://example.com/delve" in out

    def test_heading_preserved(self) -> None:
        text = "## Great question! delve into this\n\nGreat question! Body text."
        out = humanize_deterministic(text)
        assert "## Great question! delve into this" in out

    def test_empty_input_safe(self) -> None:
        assert humanize_deterministic("") == ""

    def test_no_change_when_clean(self) -> None:
        clean = "Run `npm install`, then start the server. Tests live in `./test/`."
        out = humanize_deterministic(clean)
        # May not be byte-identical (whitespace cleanup) but content is unchanged
        assert "npm install" in out
        assert "./test/" in out

    def test_yaml_frontmatter_preserved(self) -> None:
        text = (
            "---\n"
            "name: humanizer\n"
            "description: strip delve, leverage, comprehensive\n"
            "---\n\n"
            "Great question! The body gets humanized.\n"
        )
        out = humanize_deterministic(text)
        assert "---\nname: humanizer\ndescription: strip delve, leverage, comprehensive\n---" in out
        assert "Great question" not in out

    def test_blockquote_preserved_as_example(self) -> None:
        # Blockquotes are used in docs to hold verbatim "before/after" examples.
        # The humanizer must not rewrite them.
        text = (
            "Before:\n\n"
            "> Great question! It's important to note that we leverage caching.\n\n"
            "After rewrite text here.\n"
        )
        out = humanize_deterministic(text)
        assert "> Great question! It's important to note that we leverage caching." in out

    def test_multi_line_blockquote_preserved(self) -> None:
        text = (
            "Reference:\n\n"
            "> Line one has delve.\n"
            "> Line two has tapestry.\n"
            "> Line three has testament.\n\n"
            "Normal prose that mentions delve here.\n"
        )
        out = humanize_deterministic(text)
        assert "> Line one has delve.\n> Line two has tapestry.\n> Line three has testament." in out
        # The prose outside the blockquote still gets humanized.
        assert "normal prose that mentions delve here" not in out.lower() or "look at" in out.lower()

    def test_table_rows_preserved(self) -> None:
        # Tables carry glossary / reference content. Rewriting them destroys meaning.
        text = (
            "| Category | Examples |\n"
            "|----------|----------|\n"
            "| Stock vocab | delve, tapestry, testament, leverage, comprehensive |\n"
            "| Hedging | It's important to note that, generally speaking |\n\n"
            "Normal prose: we leverage caching.\n"
        )
        out = humanize_deterministic(text)
        assert "| Stock vocab | delve, tapestry, testament, leverage, comprehensive |" in out
        assert "| Hedging | It's important to note that, generally speaking |" in out
        # Prose outside the table still humanized.
        assert "we leverage caching" not in out.lower() or "use" in out.lower()

    def test_readme_before_example_survives(self) -> None:
        # Regression test: the "Before" example from the project's own README
        # used to be rewritten by the humanizer, which corrupted the doc.
        text = (
            "### Before\n\n"
            "> Great question! When optimizing React performance, it's important to note that "
            "there are several factors to consider. Firstly, you should leverage the `useMemo` "
            "hook to memoize expensive computations.\n\n"
            "### After\n\n"
            "Profile first. The bottleneck is almost never where you'd guess.\n"
        )
        out = humanize_deterministic(text)
        # Everything inside the blockquote stays byte-identical.
        assert "> Great question! When optimizing React performance, it's important to note that there are several factors to consider. Firstly, you should leverage the `useMemo` hook to memoize expensive computations." in out


# ---------- validate.py ----------


class TestValidate:
    def test_clean_humanization_passes(self) -> None:
        original = "Great question! Use `foo()`. See https://x.com."
        humanized = "Use `foo()`. See https://x.com."
        result = validate(original, humanized)
        assert result.ok
        assert result.ai_isms_after < result.ai_isms_before

    def test_dropped_url_fails(self) -> None:
        original = "See https://example.com/docs for more."
        humanized = "See the docs for more."
        result = validate(original, humanized)
        assert not result.ok
        assert any("URL" in e for e in result.errors)

    def test_dropped_inline_code_fails(self) -> None:
        original = "Run `npm install` first."
        humanized = "Run npm install first."
        result = validate(original, humanized)
        assert not result.ok
        assert any("Inline code" in e for e in result.errors)

    def test_changed_heading_fails(self) -> None:
        original = "## Setup\n\nbody"
        humanized = "## Installation\n\nbody"
        result = validate(original, humanized)
        assert not result.ok
        assert any("Heading" in e for e in result.errors)

    def test_added_ai_isms_fails(self) -> None:
        original = "Run tests."
        humanized = "Great question! It's important to note that you should run tests."
        result = validate(original, humanized)
        assert not result.ok
        assert any("AI-ism count increased" in e for e in result.errors)

    def test_modified_code_fails(self) -> None:
        original = "```\nfoo\n```"
        humanized = "```\nbar\n```"
        result = validate(original, humanized)
        assert not result.ok

    def test_reordered_code_blocks_fails(self) -> None:
        original = "```py\nprint('a')\n```\n\n```py\nprint('b')\n```"
        humanized = "```py\nprint('b')\n```\n\n```py\nprint('a')\n```"
        result = validate(original, humanized)
        assert not result.ok
        assert any("Code block" in e for e in result.errors)

    def test_added_code_block_fails(self) -> None:
        original = "```py\nprint('a')\n```"
        humanized = "```py\nprint('a')\n```\n\n```py\nprint('b')\n```"
        result = validate(original, humanized)
        assert not result.ok
        assert any("Code block" in e for e in result.errors)

    def test_modified_indented_code_fails(self) -> None:
        original = "    foo = 1\n    print(foo)\n"
        humanized = "    bar = 1\n    print(bar)\n"
        result = validate(original, humanized)
        assert not result.ok
        assert any("Indented code block" in e for e in result.errors)

    def test_modified_markdown_link_fails(self) -> None:
        original = "See [docs](https://example.com/docs)."
        humanized = "See [documentation](https://example.com/docs)."
        result = validate(original, humanized)
        assert not result.ok
        assert any("Markdown link" in e for e in result.errors)

    def test_added_robust_aiism_fails(self) -> None:
        original = "Run tests."
        humanized = "Run tests with a robust approach."
        result = validate(original, humanized)
        assert not result.ok
        assert any("AI-ism count increased" in e for e in result.errors)

    def test_modified_blockquote_fails(self) -> None:
        original = "Before:\n\n> Great question! Delve into this.\n\nAfter text."
        humanized = "Before:\n\n> Delve into this.\n\nAfter text."
        result = validate(original, humanized)
        assert not result.ok
        assert any("Blockquote" in e for e in result.errors)

    def test_modified_table_fails(self) -> None:
        original = (
            "| A | B |\n"
            "|---|---|\n"
            "| delve | leverage |\n"
        )
        humanized = (
            "| A | B |\n"
            "|---|---|\n"
            "| look at | use |\n"
        )
        result = validate(original, humanized)
        assert not result.ok
        assert any("table" in e.lower() for e in result.errors)

    def test_modified_yaml_frontmatter_fails(self) -> None:
        original = "---\nname: x\ndesc: delve here\n---\n\nBody."
        humanized = "---\nname: x\ndesc: look at here\n---\n\nBody."
        result = validate(original, humanized)
        assert not result.ok
        assert any("frontmatter" in e.lower() for e in result.errors)

    def test_added_furthermore_fails(self) -> None:
        original = "Run tests."
        humanized = "Run tests. Furthermore, check coverage."
        result = validate(original, humanized)
        assert not result.ok
        assert any("AI-ism count increased" in e for e in result.errors)


# ---------- end-to-end ----------


def test_full_humanize_round_trip(tmp_path: Path) -> None:
    from scripts.humanize import humanize_file

    src = tmp_path / "doc.md"
    src.write_text(
        "# Notes\n\nGreat question! It's important to note that tests should pass.\n\n"
        "```bash\nnpm test\n```\n\nSee https://example.com.\n"
    )
    ok = humanize_file(src, deterministic=True)
    assert ok

    backup = tmp_path / "doc.original.md"
    assert backup.exists()
    assert "Great question" in backup.read_text()

    new_text = src.read_text()
    assert "Great question" not in new_text
    assert "important to note" not in new_text
    assert "npm test" in new_text
    assert "https://example.com" in new_text


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.parametrize(
    "original_path",
    sorted(FIXTURE_DIR.glob("*.original.md")) if FIXTURE_DIR.exists() else [],
    ids=lambda p: p.stem.replace(".original", ""),
)
def test_fixture_matches_committed_output(original_path: Path) -> None:
    """Regression test: humanize_deterministic must match the committed fixture.

    If this fails, either the regex changed (update fixtures intentionally) or
    a regression slipped in. Regenerate with:

        python3 -c "import sys;sys.path.insert(0,'humanizer-humanize');
        from scripts.humanize import humanize_deterministic;
        from pathlib import Path;
        [p.with_name(p.name.replace('.original.md','.md')).write_text(
            humanize_deterministic(p.read_text()))
         for p in Path('tests/humanizer-humanize/fixtures').glob('*.original.md')]"
    """
    expected = original_path.with_name(original_path.name.replace(".original.md", ".md"))
    assert expected.exists(), f"Expected output missing: {expected}"
    original_text = original_path.read_text()
    actual = humanize_deterministic(original_text)
    assert actual == expected.read_text(), (
        f"Fixture drift for {original_path.name}. "
        f"Regenerate fixtures or fix the regression."
    )
    result = validate(original_text, expected.read_text())
    assert result.ok, f"Committed fixture fails validator: {result.errors}"


def test_refuses_sensitive_path(tmp_path: Path) -> None:
    f = tmp_path / ".env"
    f.write_text("SECRET=hunter2\n")
    assert not should_compress(f)


@pytest.mark.skipif(
    not os.environ.get("HUMANIZER_RUN_LLM_TESTS"),
    reason="LLM tests opt-in via HUMANIZER_RUN_LLM_TESTS=1 (costs API credits)",
)
def test_llm_smoke(tmp_path: Path) -> None:
    from scripts.humanize import humanize_file

    src = tmp_path / "doc.md"
    src.write_text(
        "Great question! It's important to note that tests should pass before pushing.\n"
    )
    ok = humanize_file(src, deterministic=False)
    assert ok
    new_text = src.read_text()
    assert "Great question" not in new_text
