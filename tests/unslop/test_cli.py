"""CLI tests for the unslop command-line interface.

The CLI has no existing direct test coverage — the hooks, humanize,
stylometry, and other modules were tested in isolation but the argparse
wiring, one-shot commands, and I/O paths weren't exercised end-to-end.
This fills that gap."""

from __future__ import annotations

import io
import json
import sys

import pytest

from unslop.scripts import cli


def _run(argv: list[str], stdin: str | None = None, monkeypatch=None) -> tuple[int, str, str]:
    """Run the CLI with argv, optional stdin. Capture stdout + stderr.

    Returns (exit_code, stdout, stderr)."""
    out = io.StringIO()
    err = io.StringIO()
    if monkeypatch is not None:
        monkeypatch.setattr(sys, "stdout", out)
        monkeypatch.setattr(sys, "stderr", err)
        if stdin is not None:
            monkeypatch.setattr(sys, "stdin", io.StringIO(stdin))
    code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


def _fake_anthropic_token() -> str:
    return "sk-ant-api03-" + "abcdefghijklmnopqrstuvwxyz1234567890"


def _fake_openai_project_token() -> str:
    return "sk-proj-" + "abcdefghijklmnopqrstuvwxyz1234567890"


class TestVersionAndHelp:
    def test_version_flag_exits_zero(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["unslop", "--version"])
        with pytest.raises(SystemExit) as exc:
            cli.main(["--version"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "unslop" in captured.out

    def test_help_flag_exits_zero(self):
        with pytest.raises(SystemExit) as exc:
            cli.main(["--help"])
        assert exc.value.code == 0


class TestStdinDeterministic:
    """Pure deterministic path on stdin (no LLM, no network)."""

    def test_basic_humanize_stdin(self, monkeypatch):
        text = "Great question! I'd be happy to delve into this."
        code, out, _err = _run(
            ["--stdin", "--deterministic"], stdin=text, monkeypatch=monkeypatch
        )
        assert code in (0, 2)
        assert "Great question" not in out
        assert "delve" not in out.lower()

    def test_json_output_stdin(self, monkeypatch):
        code, out, err = _run(
            ["--stdin", "--deterministic", "--json"],
            stdin="delve into this tapestry of testaments.",
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        payload = json.loads(err)
        assert payload["path"] == "<stdin>"
        assert "validation" in payload
        assert "report" in payload

    def test_diff_output_stdin(self, monkeypatch):
        code, out, _err = _run(
            ["--stdin", "--deterministic", "--diff"],
            stdin="Great question. Delve in.",
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        assert "---" in out or "+++" in out or "@@" in out

    def test_unknown_intensity_rejected(self, capsys):
        with pytest.raises(SystemExit):
            cli.main(["--stdin", "--deterministic", "--mode", "aggressive"])


class TestSecretGuard:
    def test_stdin_llm_mode_refuses_secret_like_content(self, monkeypatch):
        monkeypatch.setattr(cli, "_llm_available", lambda: True)
        code, out, err = _run(
            ["--stdin"],
            stdin=f"Token: {_fake_anthropic_token()}",
            monkeypatch=monkeypatch,
        )
        assert code == 1
        assert out == ""
        assert "--deterministic" in err

    def test_stdin_llm_mode_refusal_can_emit_json(self, monkeypatch):
        monkeypatch.setattr(cli, "_llm_available", lambda: True)
        code, out, err = _run(
            ["--stdin", "--json"],
            stdin=f"Token: {_fake_openai_project_token()}",
            monkeypatch=monkeypatch,
        )
        assert code == 1
        assert out == ""
        payload = json.loads(err)
        assert payload["ok"] is False
        assert payload["error_code"] == "sensitive_content_refused"
        assert "--deterministic" in payload["hint"]

    def test_file_llm_mode_refuses_secret_like_content(self, tmp_path, monkeypatch):
        src = tmp_path / "notes.md"
        src.write_text(
            f"Token: {_fake_anthropic_token()}\n",
            encoding="utf-8",
        )
        code, _out, err = _run([str(src)], monkeypatch=monkeypatch)
        assert code == 1
        assert "--deterministic" in err

    def test_deterministic_allows_secret_like_content_without_network(self, monkeypatch):
        code, out, _err = _run(
            ["--stdin", "--deterministic"],
            stdin=f"Token: {_fake_anthropic_token()}",
            monkeypatch=monkeypatch,
        )
        assert code == 0
        assert "sk-ant-api03" in out

    def test_detector_feedback_stdin_not_blocked_by_llm_availability(self, monkeypatch):
        class FakeOutcome:
            final_text = f"Token: {_fake_anthropic_token()}"
            original_probability = 0.9
            final_probability = 0.9
            reason_stopped = "test"

            def to_dict(self):
                return {"reason_stopped": self.reason_stopped}

        monkeypatch.setattr(cli, "_llm_available", lambda: True)
        monkeypatch.setattr(
            "unslop.scripts.detector.feedback_loop",
            lambda *args, **kwargs: FakeOutcome(),
        )
        code, out, _err = _run(
            ["--stdin", "--detector-feedback"],
            stdin=f"Token: {_fake_anthropic_token()}",
            monkeypatch=monkeypatch,
        )
        assert code == 0
        assert "sk-ant-api03" in out

    def test_diff_json_combination_rejected(self):
        with pytest.raises(SystemExit):
            cli.main(["--stdin", "--deterministic", "--diff", "--json"])


class TestStripReasoningStdin:
    """--strip-reasoning should remove reasoning traces before humanize."""

    def test_strips_thinking_block(self, monkeypatch):
        text = (
            "<thinking>planning the response</thinking>\n"
            "Here is the answer.\n"
        )
        code, out, _err = _run(
            ["--stdin", "--deterministic", "--strip-reasoning"],
            stdin=text,
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        assert "planning the response" not in out
        assert "answer" in out

    def test_strips_markdown_section(self, monkeypatch):
        text = (
            "## Reasoning\nprivate.\n\n## Conclusion\npublic answer.\n"
        )
        code, out, _err = _run(
            ["--stdin", "--deterministic", "--strip-reasoning"],
            stdin=text,
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        assert "private" not in out
        assert "public answer" in out


class TestStripReasoningFile:
    """--strip-reasoning on file mode should write a .reasoning.md sidecar."""

    def test_sidecar_written(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text(
            "<thinking>hidden plan</thinking>\n\nReal content.\n", encoding="utf-8"
        )
        code, _out, _err = _run(
            ["--deterministic", "--strip-reasoning", "--no-backup", str(src)],
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        sidecar = tmp_path / "doc.reasoning.md"
        assert sidecar.exists()
        content = sidecar.read_text(encoding="utf-8")
        assert "hidden plan" in content
        rewritten = src.read_text(encoding="utf-8")
        assert "<thinking>" not in rewritten
        assert "Real content" in rewritten

    def test_sidecar_not_written_when_no_reasoning(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text("Just ordinary prose.\n", encoding="utf-8")
        code, _out, _err = _run(
            ["--deterministic", "--strip-reasoning", "--no-backup", str(src)],
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        sidecar = tmp_path / "doc.reasoning.md"
        assert not sidecar.exists()


class TestSurprisalOneShot:
    """--surprisal-variance is a one-shot that exits after printing JSON."""

    def test_missing_deps_prints_error(self, monkeypatch):
        monkeypatch.setenv("UNSLOP_SKIP_SURPRISAL", "1")
        code, _out, err = _run(
            ["--stdin", "--surprisal-variance"],
            stdin="hello world",
            monkeypatch=monkeypatch,
        )
        assert code == 1
        assert "surprisal" in err.lower()

    def test_empty_input_still_prints_zero_reading(self, monkeypatch):
        # Empty input short-circuits before loading the LM, so works
        # even without deps.
        code, out, _err = _run(
            ["--stdin", "--surprisal-variance"], stdin="", monkeypatch=monkeypatch
        )
        assert code == 0
        payload = json.loads(out)
        assert payload["token_count"] == 0
        assert payload["surprisal_stdev"] == 0.0


class TestFileMode:
    def test_file_mode_writes_backup(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text("Great question! Just delve.", encoding="utf-8")
        code, _out, _err = _run(
            ["--deterministic", str(src)], monkeypatch=monkeypatch
        )
        assert code in (0, 2)
        backup = tmp_path / "doc.original.md"
        assert backup.exists()
        assert "delve" in backup.read_text(encoding="utf-8").lower()
        assert "delve" not in src.read_text(encoding="utf-8").lower()

    def test_no_backup_flag_skips_backup(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text("delve into this.", encoding="utf-8")
        code, _out, _err = _run(
            ["--deterministic", "--no-backup", str(src)], monkeypatch=monkeypatch
        )
        assert code in (0, 2)
        backup = tmp_path / "doc.original.md"
        assert not backup.exists()

    def test_backup_exists_refuses_rerun(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text("delve.\n", encoding="utf-8")
        backup = tmp_path / "doc.original.md"
        backup.write_text("earlier.\n", encoding="utf-8")
        code, _out, _err = _run(
            ["--deterministic", str(src)], monkeypatch=monkeypatch
        )
        assert code != 0

    def test_dry_run_does_not_write(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        original = "Great question! Delve."
        src.write_text(original, encoding="utf-8")
        code, _out, _err = _run(
            ["--deterministic", "--dry-run", str(src)], monkeypatch=monkeypatch
        )
        assert code in (0, 2)
        assert src.read_text(encoding="utf-8") == original

    def test_missing_file_reports_error(self, tmp_path, monkeypatch):
        ghost = tmp_path / "does-not-exist.md"
        code, _out, _err = _run(
            ["--deterministic", str(ghost)], monkeypatch=monkeypatch
        )
        assert code != 0


class TestReportFlag:
    def test_report_requires_deterministic(self, tmp_path):
        src = tmp_path / "doc.md"
        src.write_text("x\n", encoding="utf-8")
        report = tmp_path / "r.json"
        with pytest.raises(SystemExit):
            cli.main(["--report", str(report), str(src)])

    def test_report_writes_audit_trail(self, tmp_path, monkeypatch):
        src = tmp_path / "doc.md"
        src.write_text(
            "Great question! Let's delve into this testament.\n", encoding="utf-8"
        )
        report = tmp_path / "r.json"
        code, _out, _err = _run(
            [
                "--deterministic",
                "--no-backup",
                "--report",
                str(report),
                str(src),
            ],
            monkeypatch=monkeypatch,
        )
        assert code in (0, 2)
        assert report.exists()
        payload = json.loads(report.read_text(encoding="utf-8"))
        assert isinstance(payload, list)
        assert len(payload) == 1
        assert "report" in payload[0]


class TestDetectorMaxIterationsSentinel:
    """Regression: explicit --detector-max-iterations 4 must not silently become 6."""

    def test_explicit_4_stays_4_in_aggressive(self):
        parser = cli._build_parser()
        args = parser.parse_args(
            ["--stdin", "--detector-feedback", "--detector-loop-aggressive",
             "--detector-max-iterations", "4"]
        )
        assert cli._detector_feedback_max_iterations(args) == 4

    def test_default_aggressive_maps_to_6(self):
        parser = cli._build_parser()
        args = parser.parse_args(
            ["--stdin", "--detector-feedback", "--detector-loop-aggressive"]
        )
        assert cli._detector_feedback_max_iterations(args) == 6

    def test_default_non_aggressive_maps_to_4(self):
        parser = cli._build_parser()
        args = parser.parse_args(
            ["--stdin", "--detector-feedback"]
        )
        assert cli._detector_feedback_max_iterations(args) == 4


class TestDetectorSurprisalFlag:
    """--detector-surprisal opt-in; no model load by default."""

    def test_flag_present_in_parser(self):
        parser = cli._build_parser()
        args = parser.parse_args(["--stdin", "--detector-feedback", "--detector-surprisal"])
        assert args.detector_surprisal is True

    def test_flag_default_is_false(self):
        parser = cli._build_parser()
        args = parser.parse_args(["--stdin", "--detector-feedback"])
        assert args.detector_surprisal is False

    def test_model_forwarded(self):
        parser = cli._build_parser()
        args = parser.parse_args([
            "--stdin", "--detector-feedback", "--detector-surprisal",
            "--surprisal-model", "gpt2",
        ])
        assert args.surprisal_model == "gpt2"

    def test_no_surprisal_fn_when_flag_absent(self, monkeypatch):
        calls = []

        def spy_loop(*args, **kwargs):
            calls.append(kwargs.get("surprisal_fn"))
            class FakeOutcome:
                final_text = "done"
                original_probability = 0.9
                final_probability = 0.3
                reason_stopped = "test"
                def to_dict(self):
                    return {"reason_stopped": "test", "iterations": []}
            return FakeOutcome()

        monkeypatch.setattr("unslop.scripts.detector.feedback_loop", spy_loop)
        _run(
            ["--stdin", "--detector-feedback"],
            stdin="The team shipped.",
            monkeypatch=monkeypatch,
        )
        assert calls[0] is None

    def test_surprisal_fn_passed_when_flag_set(self, monkeypatch):
        calls = []

        def spy_loop(*args, **kwargs):
            calls.append(kwargs.get("surprisal_fn"))
            class FakeOutcome:
                final_text = "done"
                original_probability = 0.9
                final_probability = 0.3
                reason_stopped = "test"
                def to_dict(self):
                    return {"reason_stopped": "test", "iterations": []}
            return FakeOutcome()

        monkeypatch.setattr("unslop.scripts.detector.feedback_loop", spy_loop)
        monkeypatch.setattr(
            "unslop.scripts.cli._build_surprisal_fn",
            lambda model: (lambda text: 1.0),
        )
        _run(
            ["--stdin", "--detector-feedback", "--detector-surprisal"],
            stdin="The team shipped.",
            monkeypatch=monkeypatch,
        )
        assert calls[0] is not None

    def test_help_mentions_detector_surprisal(self, capsys):
        with pytest.raises(SystemExit):
            cli.main(["--help"])
        captured = capsys.readouterr()
        assert "--detector-surprisal" in captured.out


class TestSurprisalDiagnostic:
    """When --detector-surprisal deps are missing, emit one clear stderr message."""

    def test_emits_one_diagnostic_when_import_fails(self, monkeypatch, capsys):
        import sys as _sys
        import unslop.scripts.cli as cli_mod
        monkeypatch.setattr(cli_mod, "_SURPRISAL_WARNING_EMITTED", False)

        key = "unslop.scripts.surprisal"
        saved = _sys.modules.pop(key, None)
        monkeypatch.setitem(_sys.modules, key, None)

        result = cli_mod._build_surprisal_fn("distilgpt2")
        assert result is None
        captured = capsys.readouterr()
        assert "--detector-surprisal requested but dependencies unavailable" in captured.err
        assert "pip install unslop[surprisal]" in captured.err

        if saved is not None:
            _sys.modules[key] = saved

    def test_no_repeated_warning_across_calls(self, monkeypatch, capsys):
        import sys as _sys
        import unslop.scripts.cli as cli_mod
        monkeypatch.setattr(cli_mod, "_SURPRISAL_WARNING_EMITTED", False)

        key = "unslop.scripts.surprisal"
        saved = _sys.modules.pop(key, None)
        monkeypatch.setitem(_sys.modules, key, None)

        cli_mod._build_surprisal_fn("distilgpt2")
        monkeypatch.setattr(cli_mod, "_SURPRISAL_WARNING_EMITTED", True)
        cli_mod._build_surprisal_fn("distilgpt2")
        captured = capsys.readouterr()
        assert captured.err.count("--detector-surprisal requested") == 1

        if saved is not None:
            _sys.modules[key] = saved


class TestNoInputError:
    def test_no_files_and_no_stdin_errors(self):
        with pytest.raises(SystemExit):
            cli.main([])

    def test_output_requires_single_file(self, tmp_path):
        a = tmp_path / "a.md"
        b = tmp_path / "b.md"
        a.write_text("x\n", encoding="utf-8")
        b.write_text("x\n", encoding="utf-8")
        with pytest.raises(SystemExit):
            cli.main(
                [
                    "--deterministic",
                    "--output",
                    str(tmp_path / "out.md"),
                    str(a),
                    str(b),
                ]
            )
