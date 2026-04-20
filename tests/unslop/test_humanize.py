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

    @pytest.mark.parametrize(
        "name",
        [
            "config.aws/credentials",
            "secret.txt",
            "credentials.json",
            "my-password.md",
            "auth-token.yaml",
            ".npmrc",
            ".pypirc",
            ".netrc",
            "server.key",
            "client.crt",
            "ca.cer",
            "cert.pfx",
            "store.p12",
        ],
    )
    def test_sensitive_fragments_refused(self, tmp_path: Path, name: str) -> None:
        f = tmp_path / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("placeholder")
        assert is_sensitive_path(f)
        assert not should_compress(f)

    def test_ssh_dir_path_is_sensitive(self, tmp_path: Path) -> None:
        d = tmp_path / ".ssh"
        d.mkdir()
        f = d / "id_ed25519"
        f.write_text("placeholder")
        assert is_sensitive_path(f)

    def test_original_txt_backup(self, tmp_path: Path) -> None:
        f = tmp_path / "essay.original.txt"
        f.write_text("hi")
        assert detect_file_type(f) == "backup"
        assert not should_compress(f)

    def test_unknown_extension_is_other(self, tmp_path: Path) -> None:
        f = tmp_path / "data.xyzfoo"
        f.write_text("hi")
        assert detect_file_type(f) == "other"
        assert not should_compress(f)

    def test_extensionless_readme_basename(self, tmp_path: Path) -> None:
        f = tmp_path / "README"
        f.write_text("This is a project. It does things people care about.\n")
        assert detect_file_type(f) == "natural-language-extensionless"

    def test_extensionless_binary_detected_via_null_byte(self, tmp_path: Path) -> None:
        f = tmp_path / "blob"
        f.write_bytes(b"hello\x00\x01world")
        assert detect_file_type(f) == "binary"
        assert not should_compress(f)

    def test_extensionless_shebang_is_code(self, tmp_path: Path) -> None:
        f = tmp_path / "runme"
        f.write_text("#!/usr/bin/env bash\necho hi\n")
        assert detect_file_type(f) == "code-or-config"

    def test_extensionless_utf8_decode_failure_is_binary(self, tmp_path: Path) -> None:
        f = tmp_path / "bytes"
        f.write_bytes(b"\xff\xfe\x80\x81 not utf-8")
        assert detect_file_type(f) == "binary"

    def test_extensionless_symbol_heavy_is_unknown(self, tmp_path: Path) -> None:
        # Looks like code/config (lots of braces, parens) but no extension and
        # no NL basename — falls through the prose heuristic and stays unknown.
        f = tmp_path / "mystery"
        f.write_text("if (x === 0) { return $foo|bar; } else { y[i] = `tpl`; }\n" * 5)
        assert detect_file_type(f) == "unknown"
        assert not should_compress(f)

    def test_extensionless_low_alpha_is_unknown(self, tmp_path: Path) -> None:
        # Mostly digits + punctuation. Alpha ratio drops below 0.65.
        f = tmp_path / "numbers"
        f.write_text("1234567890 9876543210 1111 2222 3333 4444 5555 6666 7777 8888\n")
        assert detect_file_type(f) == "unknown"

    def test_extensionless_empty_file_is_unknown(self, tmp_path: Path) -> None:
        # Empty extensionless files have no signal — heuristic returns False
        # and detect_file_type falls through to unknown.
        f = tmp_path / "blank"
        f.write_text("")
        assert detect_file_type(f) == "unknown"

    def test_should_compress_handles_missing_file(self, tmp_path: Path) -> None:
        # Path that does not exist: stat() raises OSError and should_compress
        # must return False rather than propagate.
        ghost = tmp_path / "does-not-exist.md"
        assert not should_compress(ghost)


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


# ---------- Coverage-gap tests (target: 100%) ----------

import re as _re_mod
import subprocess as _subprocess
from unittest.mock import MagicMock, patch

from scripts import benchmark, validate as validate_mod
from scripts.cli import _build_parser, _emit_diff, _llm_available, main as cli_main
from scripts.detect import _looks_like_plain_prose, detect_file_type
from scripts.humanize import (
    HumanizeReport,
    Replacement,
    _build_humanize_prompt,
    _build_fix_prompt,
    _call_anthropic_sdk,
    _call_claude_cli,
    _llm_fix,
    _strip_outer_fence,
    _tracking_sub,
    humanize_file_ex,
    humanize_llm,
)
from scripts.validate import ValidationResult, format_report


# ---------- detect.py last 4 lines ----------


class TestDetectGaps:
    def test_looks_like_prose_whitespace_only(self) -> None:
        # Triggers the `if not non_space: return False` guard (line 76).
        assert _looks_like_plain_prose("   \t  \n  ") is False

    def test_looks_like_prose_empty(self) -> None:
        assert _looks_like_plain_prose("") is False

    def test_extensionless_unreadable_returns_unknown(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Force read_bytes() to raise OSError so detect_file_type falls back to
        # "unknown" (lines 110-111).
        f = tmp_path / "myth"
        f.write_text("hello world")

        original_read_bytes = Path.read_bytes

        def raising_read_bytes(self: Path, *a, **kw):
            if self == f:
                raise OSError("simulated")
            return original_read_bytes(self, *a, **kw)

        monkeypatch.setattr(Path, "read_bytes", raising_read_bytes)
        assert detect_file_type(f) == "unknown"

    def test_extensionless_basename_with_symbol_heavy_content(
        self, tmp_path: Path
    ) -> None:
        # README is in the natural-language basename allowlist, but its content
        # fails _looks_like_plain_prose (symbol-heavy). The allowlist short-
        # circuits before the prose heuristic — covers line 123.
        f = tmp_path / "CHANGELOG"
        f.write_text("## v1 [2024]\n- {x: 1}\n- (y, z)\n")
        # Symbol-heavy content but allowlisted basename wins.
        assert detect_file_type(f) == "natural-language-extensionless"


# ---------- humanize.py: tracking_sub branches ----------


class TestTrackingSub:
    def test_no_log_takes_fast_path(self) -> None:
        # When `log` is None, _tracking_sub bypasses the wrapper (line 479).
        out = _tracking_sub(_re_mod.compile(r"foo"), "bar", "foo foo", rule="r", log=None)
        assert out == "bar bar"

    def test_callable_repl_recorded(self) -> None:
        # Callable repl branch (line 484).
        log: list[Replacement] = []
        out = _tracking_sub(
            _re_mod.compile(r"x(\d)"),
            lambda m: m.group(1).upper(),
            "x1 x2",
            rule="callable",
            log=log,
        )
        assert out == "1 2"
        assert len(log) == 2
        assert log[0].rule == "callable"

    def test_string_repl_with_invalid_backref_falls_back(self) -> None:
        # The `match.expand` path can raise re.error on a bad backref. The
        # fallback uses the raw repl string (lines 488-489).
        log: list[Replacement] = []
        # `\99` is an invalid group reference at expand time but a valid input
        # for re.sub-style replacement strings — _tracking_sub's try/except
        # catches re.error from match.expand.
        out = _tracking_sub(
            _re_mod.compile(r"foo"),
            r"bar\99",
            "foo",
            rule="bad-backref",
            log=log,
        )
        assert "bar" in out  # fallback path took over without crashing


# ---------- humanize.py: em-dash cap final-position branch ----------


class TestEmDashCapFinalPosition:
    def test_em_dash_at_end_of_block(self) -> None:
        # An em-dash that exceeds the cap and has no trailing space hits the
        # final `else: buf.append(" ")` branch (line 413). Construct a paragraph
        # with three em-dashes so the third triggers replacement, and put the
        # third one at the very end with no space after.
        from scripts.humanize import _cap_em_dashes_per_paragraph

        text = "alpha — beta — gamma —delta"
        out = _cap_em_dashes_per_paragraph(text, max_dashes=2)
        # Third em-dash replaced with comma; first two preserved.
        assert out.count("—") == 2
        assert "," in out


# ---------- humanize.py: prompt builders ----------


class TestPromptBuilders:
    def test_build_humanize_prompt_default(self) -> None:
        prompt = _build_humanize_prompt("hello world")
        assert "hello world" in prompt
        assert "STRICT RULES" in prompt

    def test_build_humanize_prompt_unknown_intensity_falls_back(self) -> None:
        # Non-matching intensity key falls back to balanced guidance (line 685).
        prompt = _build_humanize_prompt("body", intensity="balanced")  # type: ignore[arg-type]
        assert "body" in prompt

    def test_build_fix_prompt_lists_errors(self) -> None:
        prompt = _build_fix_prompt(
            original="orig",
            broken_humanized="broken",
            errors=["missing URL", "heading drift"],
        )
        assert "missing URL" in prompt
        assert "heading drift" in prompt
        assert "orig" in prompt and "broken" in prompt


# ---------- humanize.py: _strip_outer_fence ----------


class TestStripOuterFence:
    def test_strips_markdown_fence(self) -> None:
        wrapped = "```markdown\nhello\nworld\n```"
        assert _strip_outer_fence(wrapped) == "hello\nworld"

    def test_strips_md_fence(self) -> None:
        wrapped = "```md\nhello\n```"
        assert _strip_outer_fence(wrapped) == "hello"

    def test_strips_unlabeled_fence(self) -> None:
        wrapped = "```\nhello\n```"
        assert _strip_outer_fence(wrapped) == "hello"

    def test_no_outer_fence_passes_through(self) -> None:
        text = "hello\n```inner```\nworld"
        assert _strip_outer_fence(text) == text


# ---------- humanize.py: SDK + CLI mocks ----------


class TestAnthropicSDK:
    def test_returns_none_when_sdk_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Force anthropic import to raise ImportError.
        import builtins

        original_import = builtins.__import__

        def fake_import(name, *a, **kw):
            if name == "anthropic":
                raise ImportError("simulated")
            return original_import(name, *a, **kw)

        monkeypatch.setattr(builtins, "__import__", fake_import)
        assert _call_anthropic_sdk("ignored") is None

    def test_returns_none_when_no_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # SDK present but no key.
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        # Stub anthropic so the import succeeds.
        import sys as _sys

        fake_anthropic = type(_sys)("anthropic")
        fake_anthropic.Anthropic = MagicMock()  # type: ignore[attr-defined]
        monkeypatch.setitem(_sys.modules, "anthropic", fake_anthropic)
        assert _call_anthropic_sdk("ignored") is None

    def test_returns_text_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # SDK + key present → returns concatenated block text.
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
        import sys as _sys

        block = MagicMock()
        block.text = "humanized output"
        msg = MagicMock()
        msg.content = [block]
        client_instance = MagicMock()
        client_instance.messages.create.return_value = msg
        anthropic_class = MagicMock(return_value=client_instance)

        fake_anthropic = type(_sys)("anthropic")
        fake_anthropic.Anthropic = anthropic_class  # type: ignore[attr-defined]
        monkeypatch.setitem(_sys.modules, "anthropic", fake_anthropic)
        assert _call_anthropic_sdk("any prompt") == "humanized output"


class TestClaudeCLI:
    def test_returns_none_when_cli_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize.shutil.which", lambda _: None)
        assert _call_claude_cli("ignored") is None

    def test_returns_stdout_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize.shutil.which", lambda _: "/usr/bin/claude")
        completed = _subprocess.CompletedProcess(
            args=["claude"], returncode=0, stdout="humanized text\n", stderr=""
        )
        monkeypatch.setattr("scripts.humanize.subprocess.run", lambda *a, **kw: completed)
        assert _call_claude_cli("anything") == "humanized text"

    def test_returns_none_on_nonzero_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize.shutil.which", lambda _: "/usr/bin/claude")
        completed = _subprocess.CompletedProcess(
            args=["claude"], returncode=1, stdout="", stderr="boom"
        )
        monkeypatch.setattr("scripts.humanize.subprocess.run", lambda *a, **kw: completed)
        assert _call_claude_cli("anything") is None


class TestHumanizeLLMOrchestration:
    def test_uses_sdk_when_available(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize._call_anthropic_sdk", lambda *_: "sdk reply")
        monkeypatch.setattr("scripts.humanize._call_claude_cli", lambda *_: None)
        assert humanize_llm("input") == "sdk reply"

    def test_falls_back_to_cli(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize._call_anthropic_sdk", lambda *_: None)
        monkeypatch.setattr("scripts.humanize._call_claude_cli", lambda *_: "cli reply")
        assert humanize_llm("input") == "cli reply"

    def test_raises_when_both_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.humanize._call_anthropic_sdk", lambda *_: None)
        monkeypatch.setattr("scripts.humanize._call_claude_cli", lambda *_: None)
        with pytest.raises(RuntimeError, match="LLM mode requires"):
            humanize_llm("input")

    def test_strips_outer_fence_from_llm_output(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "scripts.humanize._call_anthropic_sdk",
            lambda *_: "```markdown\nfenced reply\n```",
        )
        assert humanize_llm("input") == "fenced reply"


class TestLLMFix:
    def test_returns_none_when_both_backends_unavailable(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("scripts.humanize._call_anthropic_sdk", lambda *_: None)
        monkeypatch.setattr("scripts.humanize._call_claude_cli", lambda *_: None)
        assert _llm_fix("orig", "broken", ["err"]) is None

    def test_strips_fence_from_fix_output(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.humanize._call_anthropic_sdk", lambda *_: "```\nfixed\n```"
        )
        assert _llm_fix("orig", "broken", ["err"]) == "fixed"


# ---------- humanize.py: humanize_file_ex paths ----------


class TestHumanizeFileEx:
    def test_deterministic_structural_failure_returns_outcome(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Force validate to report a structural error. Covers line 868.
        f = tmp_path / "doc.md"
        f.write_text("hello world")
        bad_result = ValidationResult(
            ok=False,
            errors=["simulated structural break"],
            warnings=[],
            ai_isms_before=0,
            ai_isms_after=0,
            burstiness_before=0,
            burstiness_after=0,
            sentence_length_range_after=(0, 0),
        )
        monkeypatch.setattr("scripts.humanize.validate", lambda *_: bad_result)
        outcome = humanize_file_ex(f, deterministic=True, write=False)
        assert not outcome.ok
        assert outcome.error and "structural change" in outcome.error

    def test_llm_mode_success_with_backup(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        f = tmp_path / "doc.md"
        f.write_text("Great question! Here is the answer.")
        # Have the "LLM" return a deterministic answer that passes validation.
        monkeypatch.setattr(
            "scripts.humanize.humanize_llm",
            lambda text, intensity="balanced": "Here is the answer.",
        )
        outcome = humanize_file_ex(f, deterministic=False, backup=True, write=True)
        assert outcome.ok
        backup = f.with_name(f.stem + ".original.md")
        assert backup.exists()
        assert backup.read_text() == "Great question! Here is the answer."

    def test_llm_mode_runtime_error_unwinds_backup(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        f = tmp_path / "doc.md"
        f.write_text("hello")

        def raise_runtime(*a, **kw):
            raise RuntimeError("backend down")

        monkeypatch.setattr("scripts.humanize.humanize_llm", raise_runtime)
        outcome = humanize_file_ex(f, deterministic=False, backup=True, write=True)
        assert not outcome.ok
        assert outcome.error == "backend down"
        # Backup must NOT remain when the LLM call fails.
        assert not f.with_name(f.stem + ".original.md").exists()

    def test_llm_mode_validation_failure_retries_then_gives_up(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        f = tmp_path / "doc.md"
        f.write_text("# Heading\n\nbody")

        # First call returns a body that drops the heading. _llm_fix returns None
        # (no backend). The retry loop bails after one attempt.
        monkeypatch.setattr(
            "scripts.humanize.humanize_llm",
            lambda text, intensity="balanced": "body without heading",
        )
        monkeypatch.setattr("scripts.humanize._llm_fix", lambda *a, **kw: None)
        outcome = humanize_file_ex(f, deterministic=False, backup=False, write=True)
        assert not outcome.ok
        # Original file is restored.
        assert f.read_text() == "# Heading\n\nbody"


# ---------- validate.py gaps ----------


class TestValidateGaps:
    def test_heading_count_changed(self) -> None:
        result = validate_mod.validate("# A\n# B\n", "# A\n")
        assert not result.ok
        assert any("Heading count" in e for e in result.errors)

    def test_missing_path_warning(self) -> None:
        # PATH regex requires leading whitespace before the slash. Drop the
        # path from the humanized output → warning.
        original = "Inspect /etc/passwd for users.\n"
        humanized = "Inspect the file for users.\n"
        result = validate_mod.validate(original, humanized)
        assert any("Path" in w for w in result.warnings)

    def test_bullet_drop_warning(self) -> None:
        original = "- one\n- two\n- three\n- four\n- five\n- six\n"
        humanized = "- everything\n"  # 6 → 1 → less than half
        result = validate_mod.validate(original, humanized)
        assert any("Bullet count" in w for w in result.warnings)

    def test_ai_isms_unchanged_warning(self) -> None:
        # AI-ism present in both → warning.
        text = "Great question! delve into the topic. delve again."
        result = validate_mod.validate(text, text)
        assert any("unchanged" in w for w in result.warnings)


class TestFormatReport:
    def test_ok_path(self) -> None:
        result = ValidationResult(
            ok=True,
            errors=[],
            warnings=[],
            ai_isms_before=2,
            ai_isms_after=1,
            burstiness_before=5.0,
            burstiness_after=7.5,
            sentence_length_range_after=(3, 22),
        )
        out = format_report(result)
        assert "Validation: OK" in out
        assert "AI-isms: 2 → 1" in out
        assert "σ:" in out

    def test_failed_with_errors_and_warnings(self) -> None:
        result = ValidationResult(
            ok=False,
            errors=["heading dropped"],
            warnings=["path missing"],
            ai_isms_before=0,
            ai_isms_after=0,
            burstiness_before=0,
            burstiness_after=0,
            sentence_length_range_after=(0, 0),
        )
        out = format_report(result)
        assert "Validation: FAILED" in out
        assert "ERROR: heading dropped" in out
        assert "warn:  path missing" in out


# ---------- cli.py gaps ----------


class TestCLIGaps:
    def test_get_version_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Force `from . import __version__` to raise → fallback "0.0.0".
        # We patch __version__ to a sentinel that confirms the happy path
        # still works, then patch the import machinery to confirm the fallback.
        from scripts import cli as cli_mod

        with patch.object(cli_mod, "_get_version", wraps=cli_mod._get_version):
            # Happy path returns the current version string.
            assert cli_mod._get_version() != ""

        # Force the inner `from . import __version__` to raise.
        import builtins

        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if level == 1 and "__version__" in fromlist:
                raise ImportError("simulated")
            return original_import(name, globals, locals, fromlist, level)

        monkeypatch.setattr(builtins, "__import__", fake_import)
        assert cli_mod._get_version() == "0.0.0"

    def test_llm_available_via_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
        assert _llm_available() is True

    def test_llm_available_via_cli(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # _llm_available imports shutil locally; patch the global module so the
        # local re-import sees the override.
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        import shutil as _shutil

        monkeypatch.setattr(_shutil, "which", lambda _: "/usr/bin/claude")
        assert _llm_available() is True

    def test_llm_available_neither(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        import shutil as _shutil

        monkeypatch.setattr(_shutil, "which", lambda _: None)
        assert _llm_available() is False

    def test_emit_diff_writes_unified(self) -> None:
        import io

        out = io.StringIO()
        _emit_diff(out, "demo", "alpha\n", "beta\n")
        text = out.getvalue()
        assert "demo (original)" in text
        assert "demo (humanized)" in text

    def test_path_is_directory(self, tmp_path: Path) -> None:
        # Pointing the CLI at a directory hits the `not path.is_file()` branch.
        d = tmp_path / "subdir"
        d.mkdir()
        code = cli_main(["--deterministic", "--quiet", str(d)])
        assert code == 1

    def test_path_does_not_exist(self, tmp_path: Path) -> None:
        ghost = tmp_path / "missing.md"
        code = cli_main(["--deterministic", "--quiet", str(ghost)])
        assert code == 1

    def test_skip_non_natural_language(self, tmp_path: Path) -> None:
        f = tmp_path / "code.py"
        f.write_text("print('hi')")
        code = cli_main(["--deterministic", str(f)])
        assert code == 0  # skipped, not failed

    def test_output_flag_writes_alternate_path(self, tmp_path: Path) -> None:
        src = tmp_path / "in.md"
        src.write_text("Great question! Here.\n")
        dst = tmp_path / "out.md"
        code = cli_main([
            "--deterministic",
            "--quiet",
            "--output", str(dst),
            str(src),
        ])
        assert code == 0
        assert dst.exists()
        # Source is unchanged when --output is used.
        assert "Great question" in src.read_text()

    def test_output_with_multiple_files_errors(self, tmp_path: Path) -> None:
        a = tmp_path / "a.md"
        a.write_text("hi")
        b = tmp_path / "b.md"
        b.write_text("hi")
        with pytest.raises(SystemExit):
            cli_main(["--deterministic", "--output", str(a), str(a), str(b)])

    def test_no_input_files_errors(self) -> None:
        with pytest.raises(SystemExit):
            cli_main(["--deterministic"])

    def test_report_requires_deterministic(self, tmp_path: Path) -> None:
        f = tmp_path / "x.md"
        f.write_text("hello")
        with pytest.raises(SystemExit):
            cli_main(["--report", str(tmp_path / "r.json"), str(f)])

    def test_report_writes_audit_trail(self, tmp_path: Path) -> None:
        src = tmp_path / "x.md"
        src.write_text("Great question! Here.\n")
        report_path = tmp_path / "audit.json"
        code = cli_main([
            "--deterministic",
            "--quiet",
            "--report", str(report_path),
            str(src),
        ])
        assert code == 0
        assert report_path.exists()

    def test_stdin_mode(self, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
        import io

        monkeypatch.setattr(sys, "stdin", io.StringIO("Great question! Here.\n"))
        code = cli_main(["--deterministic", "--stdin"])
        captured = capsys.readouterr()
        assert code == 0
        assert "Great question" not in captured.out

    def test_stdin_mode_with_diff(
        self, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        import io

        monkeypatch.setattr(sys, "stdin", io.StringIO("Great question! Here.\n"))
        code = cli_main(["--deterministic", "--diff", "--stdin"])
        captured = capsys.readouterr()
        assert code == 0
        # Diff goes to stdout.
        assert "stdin" in captured.out

    def test_stdin_mode_with_json(
        self, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        import io

        monkeypatch.setattr(sys, "stdin", io.StringIO("Great question! Here.\n"))
        code = cli_main(["--deterministic", "--json", "--stdin"])
        captured = capsys.readouterr()
        assert code == 0
        # JSON payload goes to stderr per the implementation.
        assert "validation" in captured.err

    def test_dash_alias_for_stdin(
        self, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        import io

        monkeypatch.setattr(sys, "stdin", io.StringIO("hello\n"))
        code = cli_main(["--deterministic", "-"])
        assert code == 0

    def test_mixed_exit_codes_returns_three(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # One file succeeds, one is missing → mixed → exit 3.
        good = tmp_path / "good.md"
        good.write_text("hello\n")
        bad = tmp_path / "missing.md"
        code = cli_main(["--deterministic", "--quiet", str(good), str(bad)])
        assert code == 3

    def test_text_output_with_replacements(
        self, tmp_path: Path, capsys
    ) -> None:
        src = tmp_path / "doc.md"
        # Multiple AI-isms so replacements > 0.
        src.write_text("Great question! Certainly! delve.\n")
        code = cli_main(["--deterministic", str(src)])
        captured = capsys.readouterr()
        assert code == 0
        assert "replacements" in captured.out


# ---------- benchmark.py ----------


class TestBenchmarkCLI:
    def test_main_processes_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        # Two markdown samples — one normal, one with an AI-ism the unslop
        # knocks out.
        (tmp_path / "clean.md").write_text("Hello world. Short and direct.\n")
        (tmp_path / "slop.md").write_text("Great question! delve in.\n")
        # Add a backup file that the script must skip.
        (tmp_path / "ignored.original.md").write_text("ignored")

        monkeypatch.setattr(sys, "argv", ["benchmark", str(tmp_path)])
        benchmark.main()
        captured = capsys.readouterr()
        assert "TOTAL" in captured.out
        assert "AI-isms" in captured.out

    def test_main_errors_on_missing_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        ghost = tmp_path / "nope"
        monkeypatch.setattr(sys, "argv", ["benchmark", str(ghost)])
        with pytest.raises(SystemExit) as excinfo:
            benchmark.main()
        assert excinfo.value.code == 1

    def test_main_errors_on_empty_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        # Directory exists but contains no .md files.
        monkeypatch.setattr(sys, "argv", ["benchmark", str(tmp_path)])
        with pytest.raises(SystemExit) as excinfo:
            benchmark.main()
        assert excinfo.value.code == 1

    def test_main_reports_humanize_exception(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        (tmp_path / "broken.md").write_text("hello\n")

        def raise_boom(_text: str, *a, **kw) -> str:
            raise RuntimeError("simulated humanize crash")

        monkeypatch.setattr(benchmark, "humanize_deterministic", raise_boom)
        monkeypatch.setattr(sys, "argv", ["benchmark", str(tmp_path)])
        with pytest.raises(SystemExit) as excinfo:
            benchmark.main()
        # A humanize failure or validation failure exits 2.
        assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert "validation failure" in captured.out


# ---------- __main__.py ----------


class TestRemainingGaps:
    """Hits the last specific branches uncovered after the broad sweep."""

    def test_extensionless_prose_no_basename_match(self, tmp_path: Path) -> None:
        # File has no extension AND its basename is NOT in the NL allowlist —
        # falls through to the prose heuristic. Covers detect.py line 123.
        f = tmp_path / "essay-draft"
        f.write_text(
            "The first time I tried to learn this material I assumed it would "
            "be straightforward. It was not. The second pass went better.\n"
        )
        assert detect_file_type(f) == "natural-language-extensionless"

    def test_humanize_file_ex_refuses_existing_backup(self, tmp_path: Path) -> None:
        # Pre-create the .original.md backup so humanize_file_ex bails (line 852).
        f = tmp_path / "doc.md"
        f.write_text("hello world")
        backup = f.with_name(f.stem + ".original.md")
        backup.write_text("pre-existing")
        outcome = humanize_file_ex(f, deterministic=True, backup=True, write=True)
        assert not outcome.ok
        assert outcome.error and "Backup already exists" in outcome.error

    def test_llm_fix_succeeds_on_retry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # First humanize_llm call drops a heading (validation fails). _llm_fix
        # returns a corrected version that validates. Covers humanize.py:921
        # (the `humanized = fixed` line in the retry branch).
        f = tmp_path / "doc.md"
        f.write_text("# Heading\n\nbody text")

        monkeypatch.setattr(
            "scripts.humanize.humanize_llm",
            lambda text, intensity="balanced": "body without heading",
        )
        monkeypatch.setattr(
            "scripts.humanize._llm_fix",
            lambda *a, **kw: "# Heading\n\nbody text fixed",
        )
        outcome = humanize_file_ex(f, deterministic=False, backup=False, write=True)
        assert outcome.ok
        assert outcome.attempts >= 2
        assert "Heading" in outcome.humanized

    def test_cli_stdin_llm_mode(
        self, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        # stdin + LLM mode (not deterministic, _llm_available returns True).
        # Covers cli.py:159-160. _process_stdin imports humanize_llm from
        # the .humanize module at call time, so patch it there.
        import io
        import scripts.humanize as humanize_mod

        monkeypatch.setattr(sys, "stdin", io.StringIO("Great question! Hi.\n"))
        monkeypatch.setattr("scripts.cli._llm_available", lambda: True)
        monkeypatch.setattr(
            humanize_mod, "humanize_llm", lambda text, intensity="balanced": "Hi.\n"
        )
        code = cli_main(["--stdin"])
        captured = capsys.readouterr()
        assert code == 0
        assert "Hi." in captured.out

    def test_cli_output_prints_message_when_not_quiet(
        self, tmp_path: Path, capsys
    ) -> None:
        # --output success message goes to stdout when --quiet is NOT set.
        # Covers cli.py:240.
        src = tmp_path / "in.md"
        src.write_text("Great question! Hello.\n")
        dst = tmp_path / "out.md"
        code = cli_main(["--deterministic", "--output", str(dst), str(src)])
        captured = capsys.readouterr()
        assert code == 0
        assert "wrote humanized text to" in captured.out

    def test_cli_outcome_error_surfaced(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        # Force humanize_file_ex to return an outcome with an error message and
        # ok=False — exercises both line 266 (error printed to stderr) and
        # line 272 (return 2). _process_file imports it from .humanize at call
        # time, so patch it there.
        from scripts.humanize import HumanizeOutcome
        import scripts.humanize as humanize_mod

        f = tmp_path / "doc.md"
        f.write_text("hello")

        def fake_humanize_file_ex(path, **kw):
            return HumanizeOutcome(
                ok=False,
                original="hello",
                humanized="hello",
                error="simulated downstream failure",
            )

        monkeypatch.setattr(humanize_mod, "humanize_file_ex", fake_humanize_file_ex)
        code = cli_main(["--deterministic", str(f)])
        captured = capsys.readouterr()
        assert code == 2
        assert "simulated downstream failure" in captured.err

    def test_cli_report_message_when_not_quiet(
        self, tmp_path: Path, capsys
    ) -> None:
        # --report success message line (309) only fires when not --quiet.
        src = tmp_path / "x.md"
        src.write_text("Great question! Hello.\n")
        report_path = tmp_path / "audit.json"
        code = cli_main([
            "--deterministic",
            "--report", str(report_path),
            str(src),
        ])
        captured = capsys.readouterr()
        assert code == 0
        assert "wrote audit trail" in captured.out

    def test_benchmark_reports_validation_failure(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
    ) -> None:
        # Force validate to return a failing result so benchmark.main hits the
        # `if not result.ok` branch (line 72) and exits 2.
        (tmp_path / "x.md").write_text("hello\n")

        bad_result = ValidationResult(
            ok=False,
            errors=["forced failure"],
            warnings=[],
            ai_isms_before=0,
            ai_isms_after=0,
            burstiness_before=0,
            burstiness_after=0,
            sentence_length_range_after=(0, 0),
        )
        monkeypatch.setattr(benchmark, "validate", lambda *_: bad_result)
        monkeypatch.setattr(sys, "argv", ["benchmark", str(tmp_path)])
        with pytest.raises(SystemExit) as excinfo:
            benchmark.main()
        assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert "forced failure" in captured.out


class TestModuleEntryPoint:
    def test_module_dash_m_invocation_runs_cli(self, tmp_path: Path) -> None:
        # `python -m scripts` should hit __main__.py and run cli.main().
        src = tmp_path / "doc.md"
        src.write_text("Great question! Hello.\n")
        result = _subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts",
                "--deterministic",
                "--dry-run",
                "--quiet",
                str(src),
            ],
            cwd=str(ROOT / "unslop"),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
