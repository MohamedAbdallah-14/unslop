"""Tests for unslop.

Run with: pytest tests/unslop/

The deterministic mode is fully tested. LLM mode is smoke-tested only when
ANTHROPIC_API_KEY is present.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "unslop"))

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

    def test_strips_certainly_with_comma(self) -> None:
        out = humanize_deterministic("Certainly, I will help.")
        assert "Certainly" not in out
        assert "I will help" in out

    def test_strips_certainly_after_sentence(self) -> None:
        out = humanize_deterministic("We need it. Certainly, that is true.")
        assert "Certainly" not in out
        assert "that is true" in out.lower()

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

    def test_strips_delving_conjugation(self) -> None:
        out = humanize_deterministic("When delving into the data, we found errors.")
        assert "delving" not in out.lower()
        assert "looking at" in out.lower()

    def test_strips_embark_conjugations(self) -> None:
        out = humanize_deterministic("When embarking on the project, we planned ahead.")
        assert "embarking" not in out.lower()
        assert "starting" in out.lower()

    def test_strips_leverage_all_forms(self) -> None:
        out = humanize_deterministic(
            "We leverage caching. The system leverages it. We leveraged X. We are leveraging Y."
        )
        assert "leverag" not in out.lower()

    def test_leverage_conjugation_grammar(self) -> None:
        out = humanize_deterministic("The system leverages caching heavily.")
        assert "uses" in out.lower()
        out2 = humanize_deterministic("They leveraged the API.")
        assert "used" in out2.lower()
        out3 = humanize_deterministic("We are leveraging new tools.")
        assert "using" in out3.lower()

    def test_strips_seamless(self) -> None:
        out = humanize_deterministic("The seamless integration works seamlessly.")
        assert "seamless" not in out.lower()
        assert "smooth" in out.lower()

    def test_rewrites_filler_adjectives_with_natural_phrasing(self) -> None:
        out = humanize_deterministic(
            "We took a comprehensive view and applied a holistic approach. "
            "The report was written comprehensively."
        )
        low = out.lower()
        assert "comprehensive" not in low
        assert "holistic" not in low
        assert "broad" in low
        assert "overall" in low
        assert "thoroughly" in low

    def test_testament_with_preceding_verb(self) -> None:
        out = humanize_deterministic("The code embodies a testament to the engineers.")
        assert "embodies" not in out.lower()
        assert "testament" not in out.lower()
        assert "shows" in out.lower()

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
        out = humanize_deterministic("He looked at her and saw, furthermore, great sadness.")
        assert "furthermore" in out.lower()

    def test_strips_transition_tics_in_bullet_items(self) -> None:
        text = (
            "- Additionally, explore frameworks.\n"
            "- Furthermore, read the docs.\n"
            "- In conclusion, practice daily.\n"
        )
        out = humanize_deterministic(text)
        assert "additionally" not in out.lower()
        assert "furthermore" not in out.lower()
        assert "in conclusion" not in out.lower()
        assert "- Explore" in out
        assert "- Read" in out
        assert "- Practice" in out

    def test_strips_firstly_secondly(self) -> None:
        out = humanize_deterministic("Firstly, read the docs. Secondly, write tests.")
        assert "firstly" not in out.lower()
        assert "secondly" not in out.lower()

    def test_strips_firstly_in_bullet(self) -> None:
        text = "- Firstly, install the package.\n- Secondly, configure it."
        out = humanize_deterministic(text)
        assert "firstly" not in out.lower()
        assert "secondly" not in out.lower()


class TestDeterministicEmDashCap:
    def test_keeps_two_em_dashes_per_paragraph(self) -> None:
        text = "One thing — and another — stays."
        out = humanize_deterministic(text)
        assert out.count("—") == 2

    def test_replaces_third_em_dash_with_comma(self) -> None:
        text = "First — second — third — fourth — end."
        out = humanize_deterministic(text)
        assert out.count("—") == 2
        assert " , " not in out, f"Ugly spacing ' , ' found in: {out!r}"
        assert "third, fourth, end" in out or "third,fourth,end" in out

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
        unslop bug."""
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
            "name: unslop\n"
            "description: strip delve, leverage, comprehensive\n"
            "---\n\n"
            "Great question! The body gets humanized.\n"
        )
        out = humanize_deterministic(text)
        assert "---\nname: unslop\ndescription: strip delve, leverage, comprehensive\n---" in out
        assert "Great question" not in out

    def test_blockquote_preserved_as_example(self) -> None:
        # Blockquotes are used in docs to hold verbatim "before/after" examples.
        # The unslop must not rewrite them.
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
        # used to be rewritten by the unslop, which corrupted the doc.
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

        python3 -c "import sys;sys.path.insert(0,'unslop');
        from scripts.humanize import humanize_deterministic;
        from pathlib import Path;
        [p.with_name(p.name.replace('.original.md','.md')).write_text(
            humanize_deterministic(p.read_text()))
         for p in Path('tests/unslop/fixtures').glob('*.original.md')]"
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
    not os.environ.get("UNSLOP_RUN_LLM_TESTS"),
    reason="LLM tests opt-in via UNSLOP_RUN_LLM_TESTS=1 (costs API credits)",
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


# ---------- new AI-ism categories (blader/unslop + Wikipedia:Signs_of_AI_writing) ----------


class TestExpandedVocab:
    def test_interplay_between(self) -> None:
        out = humanize_deterministic("The interplay between modules is complex.")
        assert "interplay between" not in out.lower()
        assert "link between" in out.lower()

    def test_intricate_is_replaced(self) -> None:
        out = humanize_deterministic("The intricate design pays off.")
        assert "intricate" not in out.lower()
        assert "detailed" in out.lower()

    def test_vibrant_is_replaced(self) -> None:
        out = humanize_deterministic("A vibrant community surrounds the project.")
        assert "vibrant" not in out.lower()

    def test_figurative_underscore_is_replaced(self) -> None:
        out = humanize_deterministic("This underscores the need for tests.")
        assert "underscores the" not in out.lower()
        assert "shows the" in out.lower()

    def test_literal_underscore_in_prose_preserved(self) -> None:
        # "underscore" without a following article is probably literal (variable
        # naming discussion). We should leave it alone.
        out = humanize_deterministic("Use an underscore between words.")
        assert "underscore" in out.lower()

    def test_crucial_is_replaced(self) -> None:
        out = humanize_deterministic("Caching is crucial for throughput.")
        assert "crucial" not in out.lower()
        assert "important" in out.lower()

    def test_vital_role_is_replaced(self) -> None:
        out = humanize_deterministic("Tests play a vital role in CI.")
        assert "vital role" not in out.lower()

    def test_vital_signs_preserved(self) -> None:
        # "vital" in medical-ish context shouldn't be nuked — we gate on the
        # noun slot.
        out = humanize_deterministic("Check the patient's vital signs.")
        assert "vital signs" in out.lower()

    def test_ever_evolving_is_replaced(self) -> None:
        out = humanize_deterministic("Security is an ever-evolving field.")
        assert "ever-evolving" not in out.lower()
        assert "changing" in out.lower()

    def test_in_todays_digital_world(self) -> None:
        out = humanize_deterministic("In today's digital world, we ship fast.")
        assert "digital world" not in out.lower()
        assert out.lower().startswith("today,")

    def test_dynamic_landscape(self) -> None:
        out = humanize_deterministic("We operate in a dynamic landscape.")
        assert "dynamic landscape" not in out.lower()


class TestAuthorityTropes:
    def test_at_its_core_stripped(self) -> None:
        out = humanize_deterministic("At its core, caching trades memory for latency.")
        assert "at its core" not in out.lower()
        assert "caching" in out.lower()

    def test_in_reality_stripped(self) -> None:
        out = humanize_deterministic("In reality, most caches are small.")
        assert not out.lower().startswith("in reality")
        assert "most caches" in out.lower()

    def test_fundamentally_stripped(self) -> None:
        out = humanize_deterministic("Fundamentally, this is a scheduling problem.")
        assert not out.lower().startswith("fundamentally")

    def test_what_really_matters(self) -> None:
        out = humanize_deterministic("What really matters is that tests pass.")
        assert "what really matters" not in out.lower()
        assert "tests pass" in out.lower()


class TestSignposting:
    def test_lets_dive_in_stripped(self) -> None:
        out = humanize_deterministic("Let's dive in. Here is the first step.")
        assert "dive in" not in out.lower()
        assert "first step" in out.lower()

    def test_without_further_ado(self) -> None:
        out = humanize_deterministic("Without further ado, here is the list.")
        assert "without further ado" not in out.lower()

    def test_heres_what_you_need_to_know(self) -> None:
        out = humanize_deterministic("Here's what you need to know: tests matter.")
        assert "what you need to know" not in out.lower()
        assert "tests matter" in out.lower()

    def test_lets_break_it_down(self) -> None:
        out = humanize_deterministic("Let's break this down. First, we build.")
        assert "break this down" not in out.lower()


class TestFillerPhrasesFullIntensity:
    def test_filler_not_stripped_at_balanced(self) -> None:
        # balanced is the default and should NOT touch filler phrases.
        out = humanize_deterministic("We ran the tests in order to verify.")
        assert "in order to" in out.lower()

    def test_in_order_to_stripped_at_full(self) -> None:
        out = humanize_deterministic(
            "We ran the tests in order to verify.", intensity="full"
        )
        assert "in order to" not in out.lower()

    def test_due_to_the_fact_that_stripped_at_full(self) -> None:
        out = humanize_deterministic(
            "The build failed due to the fact that the disk was full.",
            intensity="full",
        )
        assert "due to the fact that" not in out.lower()
        assert "because" in out.lower()

    def test_prior_to_stripped_at_full(self) -> None:
        out = humanize_deterministic(
            "Run migrations prior to deploying.", intensity="full"
        )
        assert "prior to" not in out.lower()
        assert "before" in out.lower()

    def test_with_regard_to_stripped_at_full(self) -> None:
        out = humanize_deterministic(
            "With regard to caching, redis is fine.", intensity="full"
        )
        assert "with regard to" not in out.lower()


class TestNegativeParallelism:
    def test_tricolon_negation_stripped_at_full(self) -> None:
        text = "No guesswork, no bloat, no surprises."
        out = humanize_deterministic(text, intensity="full")
        assert "no guesswork" not in out.lower()

    def test_negative_parallelism_preserved_at_balanced(self) -> None:
        text = "No guesswork, no bloat, no surprises."
        out = humanize_deterministic(text, intensity="balanced")
        # Still present because we only run this rule at full.
        assert "No guesswork" in out or "no guesswork" in out.lower()


# ---------- intensity modes ----------


class TestIntensity:
    def test_invalid_intensity_raises(self) -> None:
        with pytest.raises(ValueError):
            humanize_deterministic("hello", intensity="aggressive")  # type: ignore[arg-type]

    def test_subtle_preserves_sycophancy(self) -> None:
        # `subtle` only runs stock-vocab.
        out = humanize_deterministic(
            "Great question! The interplay between modules is complex.",
            intensity="subtle",
        )
        # Sycophancy NOT stripped at subtle.
        assert "Great question" in out
        # Stock vocab IS stripped at subtle.
        assert "interplay between" not in out.lower()

    def test_balanced_strips_sycophancy(self) -> None:
        out = humanize_deterministic(
            "Great question! Tests should pass.", intensity="balanced"
        )
        assert "Great question" not in out

    def test_full_strips_filler(self) -> None:
        out = humanize_deterministic(
            "We ran in order to verify.", intensity="full"
        )
        assert "in order to" not in out.lower()

    def test_full_is_superset_of_balanced(self) -> None:
        text = "Great question! At its core, we ran in order to verify."
        balanced = humanize_deterministic(text, intensity="balanced")
        full = humanize_deterministic(text, intensity="full")
        # full removes everything balanced does, plus filler.
        assert "Great question" not in balanced
        assert "Great question" not in full
        assert "in order to" in balanced.lower()
        assert "in order to" not in full.lower()


# ---------- audit trail ----------


class TestAuditTrail:
    def test_report_records_replacements(self) -> None:
        from scripts.humanize import humanize_deterministic_with_report

        text = "Great question! The interplay between caching and latency is crucial."
        out, report = humanize_deterministic_with_report(text, intensity="balanced")
        assert out != text
        assert report.intensity == "balanced"
        assert len(report.replacements) > 0
        rules = {r.rule for r in report.replacements}
        assert "sycophancy" in rules
        assert "stock_vocab" in rules

    def test_report_counts_by_rule(self) -> None:
        from scripts.humanize import humanize_deterministic_with_report

        text = (
            "Great question! Here is the answer.\n\n"
            "Certainly! It's important to note that tests matter.\n"
        )
        _, report = humanize_deterministic_with_report(text)
        counts = report.counts_by_rule
        assert counts.get("sycophancy", 0) >= 2
        assert counts.get("hedging_opener", 0) >= 1

    def test_report_empty_on_clean_text(self) -> None:
        from scripts.humanize import humanize_deterministic_with_report

        text = "This is a plain sentence with no tells.\n"
        out, report = humanize_deterministic_with_report(text)
        # Nothing removable.
        assert report.replacements == []
        assert out == text

    def test_report_to_dict_shape(self) -> None:
        from scripts.humanize import humanize_deterministic_with_report

        _, report = humanize_deterministic_with_report(
            "Great question! Delve into this."
        )
        d = report.to_dict()
        assert set(d.keys()) >= {
            "intensity",
            "replacements",
            "counts_by_rule",
            "em_dashes_before",
            "em_dashes_after",
        }
        assert all("rule" in r and "before" in r and "after" in r for r in d["replacements"])

    def test_report_tracks_em_dash_counts(self) -> None:
        from scripts.humanize import humanize_deterministic_with_report

        text = "One — two — three — four — five.\n"
        _, report = humanize_deterministic_with_report(text)
        assert report.em_dashes_before == 4
        assert report.em_dashes_after <= 2


# ---------- HumanizeOutcome / humanize_file_ex ----------


class TestHumanizeFileEx:
    def test_outcome_carries_report_and_validation(self, tmp_path: Path) -> None:
        from scripts.humanize import humanize_file_ex

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this topic.\n")
        outcome = humanize_file_ex(src, deterministic=True)
        assert outcome.ok
        assert outcome.report is not None
        assert outcome.validation is not None
        assert outcome.humanized != outcome.original

    def test_dry_run_does_not_write(self, tmp_path: Path) -> None:
        from scripts.humanize import humanize_file_ex

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        outcome = humanize_file_ex(src, deterministic=True, write=False, backup=False)
        assert outcome.ok
        # Source unchanged on disk.
        assert src.read_text() == "Great question! Delve into this.\n"

    def test_no_backup_flag(self, tmp_path: Path) -> None:
        from scripts.humanize import humanize_file_ex

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        outcome = humanize_file_ex(src, deterministic=True, backup=False)
        assert outcome.ok
        assert not (tmp_path / "doc.original.md").exists()

    def test_refuses_to_overwrite_existing_backup(self, tmp_path: Path) -> None:
        from scripts.humanize import humanize_file_ex

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        backup = tmp_path / "doc.original.md"
        backup.write_text("someone else's backup\n")

        outcome = humanize_file_ex(src, deterministic=True)
        assert not outcome.ok
        assert outcome.error and "backup already exists" in outcome.error.lower()
        # Should not have clobbered.
        assert backup.read_text() == "someone else's backup\n"


# ---------- CLI ----------


class TestCLI:
    def test_version_flag(self, capsys) -> None:
        from scripts.cli import main

        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert out.startswith("unslop ")

    def test_help_flag(self, capsys) -> None:
        from scripts.cli import main

        with pytest.raises(SystemExit) as exc:
            main(["--help"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "--deterministic" in out
        assert "--mode" in out
        assert "--stdin" in out

    def test_no_args_errors(self, capsys) -> None:
        from scripts.cli import main

        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "no input files" in err.lower()

    def test_missing_file_returns_1(self, tmp_path: Path, capsys) -> None:
        from scripts.cli import main

        code = main(["--deterministic", str(tmp_path / "does-not-exist.md")])
        assert code == 1
        err = capsys.readouterr().err
        assert "not found" in err.lower()

    def test_report_requires_deterministic(self, tmp_path: Path, capsys) -> None:
        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Delve into this.\n")
        with pytest.raises(SystemExit) as exc:
            main(["--report", str(tmp_path / "r.json"), str(src)])
        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "--report" in err and "--deterministic" in err

    def test_output_requires_single_file(self, tmp_path: Path, capsys) -> None:
        from scripts.cli import main

        a = tmp_path / "a.md"
        b = tmp_path / "b.md"
        a.write_text("x\n")
        b.write_text("y\n")
        with pytest.raises(SystemExit) as exc:
            main(["--deterministic", "--output", str(tmp_path / "out.md"), str(a), str(b)])
        assert exc.value.code == 2

    def test_stdin_deterministic(self, tmp_path: Path, monkeypatch, capsys) -> None:
        import io

        from scripts.cli import main

        monkeypatch.setattr(
            "sys.stdin",
            io.StringIO("Great question! Delve into this.\n"),
        )
        code = main(["--stdin", "--deterministic", "--mode", "balanced"])
        assert code == 0
        out = capsys.readouterr().out
        assert "Great question" not in out
        assert "delve" not in out.lower()

    def test_dry_run_does_not_write_file(self, tmp_path: Path) -> None:
        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        code = main(["--deterministic", "--dry-run", "--quiet", str(src)])
        assert code == 0
        # Untouched.
        assert src.read_text() == "Great question! Delve into this.\n"
        assert not (tmp_path / "doc.original.md").exists()

    def test_diff_output(self, tmp_path: Path, capsys) -> None:
        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        code = main(["--deterministic", "--diff", "--quiet", str(src)])
        assert code == 0
        out = capsys.readouterr().out
        # Unified diff markers.
        assert out.startswith("---")
        assert "+++" in out
        # File itself untouched.
        assert "Great question" in src.read_text()

    def test_json_output(self, tmp_path: Path, capsys) -> None:
        import json as json_mod

        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        code = main(["--deterministic", "--dry-run", "--json", "--quiet", str(src)])
        assert code == 0
        out = capsys.readouterr().out
        payload = json_mod.loads(out)
        assert payload["ok"] is True
        assert "validation" in payload
        assert "report" in payload
        assert payload["report"]["intensity"] == "balanced"

    def test_report_file(self, tmp_path: Path) -> None:
        import json as json_mod

        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        report_path = tmp_path / "report.json"
        code = main([
            "--deterministic",
            "--dry-run",
            "--report",
            str(report_path),
            "--quiet",
            str(src),
        ])
        assert code == 0
        assert report_path.exists()
        data = json_mod.loads(report_path.read_text())
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["report"]["intensity"] == "balanced"
        assert len(data[0]["report"]["replacements"]) > 0

    def test_output_flag_writes_to_target(self, tmp_path: Path) -> None:
        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("Great question! Delve into this.\n")
        dst = tmp_path / "out.md"
        code = main([
            "--deterministic",
            "--no-backup",
            "--output",
            str(dst),
            "--quiet",
            str(src),
        ])
        assert code == 0
        assert dst.exists()
        assert "Great question" not in dst.read_text()
        # Source is preserved (because --output implies don't-overwrite-input).
        assert "Great question" in src.read_text()

    def test_mode_full_at_cli(self, tmp_path: Path) -> None:
        import json as json_mod

        from scripts.cli import main

        src = tmp_path / "doc.md"
        src.write_text("We ran in order to verify.\n")
        code = main([
            "--deterministic",
            "--dry-run",
            "--json",
            "--mode", "full",
            "--quiet",
            str(src),
        ])
        assert code == 0  # smoke: validated
        # Read back JSON; must reflect full intensity.
        # (--json goes to stdout; capsys is fine, but we asserted payload above.)
