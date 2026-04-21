"""Tests for the reasoning-trace sanitizer (unslop.scripts.reasoning)."""

from unslop.scripts.reasoning import ReasoningReport, strip_reasoning_traces


class TestXmlStripping:
    """XML-style wrappers must be removed end-to-end."""

    def test_strip_thinking_tag(self):
        text = "Before.\n<thinking>\nI should answer carefully.\n</thinking>\nAfter."
        cleaned, report = strip_reasoning_traces(text)
        assert "<thinking>" not in cleaned
        assert "should answer" not in cleaned
        assert "Before." in cleaned
        assert "After." in cleaned
        assert report.blocks_stripped == 1
        assert "xml:thinking" in report.patterns_matched

    def test_strip_think_tag_deepseek_style(self):
        text = "<think>r1 reasoning</think>\nFinal answer."
        cleaned, report = strip_reasoning_traces(text)
        assert "r1 reasoning" not in cleaned
        assert "Final answer." in cleaned
        assert report.blocks_stripped == 1

    def test_strip_analysis_and_plan(self):
        text = (
            "<analysis>first</analysis>\n"
            "<plan>1. do x\n2. do y</plan>\n"
            "Actual output here."
        )
        cleaned, report = strip_reasoning_traces(text)
        assert "first" not in cleaned
        assert "do x" not in cleaned
        assert "Actual output here." in cleaned
        assert report.blocks_stripped == 2

    def test_case_insensitive_tags(self):
        text = "<THINKING>loud</THINKING>\nQuiet."
        cleaned, _ = strip_reasoning_traces(text)
        assert "loud" not in cleaned
        assert "Quiet." in cleaned

    def test_multiple_same_tag(self):
        text = "<think>one</think> mid <think>two</think> end"
        cleaned, report = strip_reasoning_traces(text)
        assert "one" not in cleaned
        assert "two" not in cleaned
        assert "mid" in cleaned and "end" in cleaned
        assert report.blocks_stripped == 2

    def test_inline_tag_name_in_prose_survives(self):
        # Word-like use of a tag name shouldn't be matched. Without a `<`
        # the pattern cannot fire.
        text = "The thinking tag is how Claude emits reasoning."
        cleaned, report = strip_reasoning_traces(text)
        assert cleaned == text
        assert report.blocks_stripped == 0


class TestMarkdownStripping:
    """Markdown reasoning sections must be stripped to the next heading."""

    def test_strip_reasoning_section(self):
        text = (
            "# Doc\n\n"
            "Intro paragraph.\n\n"
            "## Reasoning\n\n"
            "Private thoughts here.\n"
            "More private thoughts.\n\n"
            "## Conclusion\n\n"
            "Public answer.\n"
        )
        cleaned, report = strip_reasoning_traces(text)
        assert "Private thoughts" not in cleaned
        assert "## Reasoning" not in cleaned
        assert "## Conclusion" in cleaned
        assert "Public answer." in cleaned
        assert report.blocks_stripped == 1
        assert "markdown:Reasoning" in report.patterns_matched

    def test_strip_thought_process_section(self):
        text = (
            "## Thought Process\nSome reasoning.\n\n"
            "## Final Answer\nDone.\n"
        )
        cleaned, _ = strip_reasoning_traces(text)
        assert "Some reasoning" not in cleaned
        assert "Final Answer" in cleaned

    def test_strip_at_eof(self):
        text = "## Conclusion\nAnswer.\n\n## Scratchpad\nInternal notes.\n"
        cleaned, report = strip_reasoning_traces(text)
        assert "Internal notes" not in cleaned
        assert "Answer." in cleaned
        assert report.blocks_stripped == 1

    def test_named_section_in_body_not_stripped(self):
        # Plain prose mentioning "reasoning" should survive. We only strip
        # lines that *are* headings, not lines that mention the word.
        text = "## Summary\nMy reasoning was sound.\n"
        cleaned, report = strip_reasoning_traces(text)
        assert cleaned.strip() == text.strip()
        assert report.blocks_stripped == 0


class TestSidecarOutput:
    """Stripped content should be retained for the CLI sidecar."""

    def test_stripped_content_populated(self):
        text = "<thinking>kept aside</thinking>\nMain."
        _, report = strip_reasoning_traces(text)
        assert "kept aside" in report.stripped_content

    def test_multiple_blocks_concatenated(self):
        text = "<think>a</think>\n<analysis>b</analysis>\nend"
        _, report = strip_reasoning_traces(text)
        assert "a" in report.stripped_content
        assert "b" in report.stripped_content
        assert "---" in report.stripped_content

    def test_report_to_dict_shape(self):
        text = "<thinking>x</thinking>\nY."
        _, report = strip_reasoning_traces(text)
        d = report.to_dict()
        assert d["blocks_stripped"] == 1
        assert d["patterns_matched"] == ["xml:thinking"]
        assert d["stripped_bytes"] > 0


class TestSafety:
    """Idempotency and edge cases."""

    def test_empty_input(self):
        cleaned, report = strip_reasoning_traces("")
        assert cleaned == ""
        assert report.blocks_stripped == 0

    def test_no_reasoning_is_noop(self):
        text = "Just a paragraph.\n\nAnd another.\n"
        cleaned, report = strip_reasoning_traces(text)
        assert cleaned == text
        assert report.blocks_stripped == 0

    def test_idempotent(self):
        text = "<thinking>x</thinking>\nMain body."
        once, _ = strip_reasoning_traces(text)
        twice, report2 = strip_reasoning_traces(once)
        assert once == twice
        assert report2.blocks_stripped == 0

    def test_preserves_code_fence_that_mentions_tag(self):
        # Tag inside a fenced code block should survive. The sanitizer
        # doesn't parse code fences itself — that is humanize.py's
        # _protect step. But it must not greedily swallow a fence either.
        # Here, the XML pattern will match because there's a real closing
        # tag — that's expected behavior. The strip_reasoning=True
        # contract is: the *caller* applies this to their text; if their
        # text has reasoning tags inside code, they wanted them stripped.
        # So this test only checks ordinary non-tagged fenced content.
        text = (
            "```python\n"
            "def f(): return 1  # reasoning about f\n"
            "```\n"
            "Final."
        )
        cleaned, report = strip_reasoning_traces(text)
        assert "def f()" in cleaned
        assert "reasoning about f" in cleaned
        assert report.blocks_stripped == 0

    def test_collapses_blank_runs(self):
        text = (
            "Paragraph one.\n\n"
            "<thinking>noise</thinking>\n\n\n"
            "Paragraph two."
        )
        cleaned, _ = strip_reasoning_traces(text)
        # The triple+ newlines left by stripping should collapse to a
        # single blank line — no visible gap from the removed block.
        assert "\n\n\n" not in cleaned
        assert "Paragraph one." in cleaned
        assert "Paragraph two." in cleaned


class TestReportDefaults:
    def test_empty_report_to_dict(self):
        r = ReasoningReport()
        d = r.to_dict()
        assert d == {
            "blocks_stripped": 0,
            "patterns_matched": [],
            "stripped_bytes": 0,
        }
