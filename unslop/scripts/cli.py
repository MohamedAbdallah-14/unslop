"""Command-line interface for unslop.

Reads a markdown / text file (or stdin), strips AI-isms while preserving code,
URLs, paths, and headings, and writes the result (or a diff, or a JSON report).

Examples:
  humanize path/to/README.md                  # LLM mode, in-place, balanced
  humanize --deterministic --mode full README.md
  humanize --stdin --deterministic < in.md > out.md
  humanize --diff notes.md                    # show unified diff, don't write
  humanize --dry-run --json *.md              # batch, no writes, JSON report
  humanize --report replacements.json --deterministic notes.md

Exit codes:
  0  success (or no changes needed in --dry-run)
  1  usage error, file not found, sensitive path refused
  2  validation failure (structure changed, or LLM retry ceiling hit)
  3  partial failure in batch mode (some files succeeded, some failed)
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

USAGE_EPILOG = """\
Modes:
  --deterministic   Fast regex pass, no API call, no subprocess.
  (default)         LLM mode: Anthropic SDK when ANTHROPIC_API_KEY is set,
                    falls back to `claude --print` CLI on PATH.

Intensity (--mode):
  subtle    Trim stock vocab only. Keep structure roughly intact.
  balanced  Default. Strip sycophancy, hedging, transitions, stock vocab,
            authority tropes, signposting, em-dash pileups.
  full      Strong rewrite. Everything balanced does, plus filler phrases
            and negative-parallelism knockouts.

Input:
  <file>...         One or more paths. Glob expansion is done by your shell.
  --stdin           Read from stdin, write humanized text to stdout.
                    Forces --no-backup, --deterministic friendly.
  -                 Alias for --stdin when used as the single filepath.

Output:
  --output PATH     Write to PATH instead of overwriting input. Single-file only.
  --diff            Print unified diff to stdout. Implies --dry-run.
  --dry-run         Don't write anything; just validate + report.
  --no-backup       Skip the <stem>.original.md backup.
  --json            Emit machine-readable JSON per file.
  --report PATH     Write full replacement audit trail to PATH as JSON.
  --quiet / -q      Suppress progress lines on stdout.
"""


def _get_version() -> str:
    try:
        from . import __version__
        return __version__
    except Exception:
        return "0.0.0"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="unslop",
        description=(
            "Humanize markdown / text files. Strips AI-isms (sycophancy, stock "
            "vocab, hedging, em-dash pileups, authority tropes, signposting) "
            "while preserving fenced code, inline code, URLs, paths, and "
            "headings byte-for-byte."
        ),
        epilog=USAGE_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"unslop {_get_version()}"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="One or more input files. Use '-' or --stdin to read from stdin.",
    )
    parser.add_argument(
        "--deterministic",
        action="store_true",
        help="Use the deterministic regex pass only (no API, no subprocess).",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=("subtle", "balanced", "full"),
        default="balanced",
        help="Intensity level. Default: balanced.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read from stdin, write to stdout. Implies --no-backup.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write humanized output to this path instead of overwriting input.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print unified diff and exit without writing. Implies --dry-run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report; do not write to disk.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip the <stem>.original.md backup. Use with care.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report per file instead of human-readable text.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help=(
            "Write the full replacement audit trail to this JSON file. "
            "Works only with --deterministic; LLM mode cannot produce a "
            "byte-level audit trail."
        ),
    )
    parser.add_argument(
        "--structural",
        action="store_true",
        help=(
            "Enable the Phase 1 structural pass: split overlong sentences at "
            "safe boundaries and collapse parallel bullet-soup. Raises sentence-"
            "length variance (σ), the #1 AI-detector signal. Opt-in for now."
        ),
    )
    parser.add_argument(
        "--detector-feedback",
        action="store_true",
        help=(
            "Run the output through an AI-text detector and re-humanize with "
            "escalating intensity until the score falls below target. Opt-in; "
            "first run downloads ~500MB of HF weights (or run `python3 -m "
            "unslop.scripts.fetch_detectors` ahead of time)."
        ),
    )
    parser.add_argument(
        "--detector-target",
        type=float,
        default=0.5,
        help="Stop escalating once the detector score drops below this. Default 0.5.",
    )
    parser.add_argument(
        "--detector-max-iterations",
        type=int,
        default=3,
        help="Cap how many escalation steps to try. Default 3.",
    )
    parser.add_argument(
        "--detector-model",
        choices=("tmr", "desklib"),
        default="tmr",
        help="Which detector to use. TMR (~500MB) is the default.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress lines on stdout.",
    )
    return parser


def _process_stdin(args: argparse.Namespace) -> int:
    from .humanize import humanize_deterministic_with_report, humanize_llm
    from .validate import validate

    text = sys.stdin.read()
    feedback = None

    if args.detector_feedback:
        from .detector import DetectorUnavailable, feedback_loop

        try:
            outcome = feedback_loop(
                text,
                target_probability=args.detector_target,
                max_iterations=args.detector_max_iterations,
                detector=args.detector_model,
            )
        except DetectorUnavailable as exc:
            sys.stderr.write(f"detector feedback disabled: {exc}\n")
            return 1
        humanized = outcome.final_text
        feedback = outcome
        report = None
    elif args.deterministic or not _llm_available():
        humanized, report = humanize_deterministic_with_report(
            text, intensity=args.mode, structural=args.structural
        )
    else:
        humanized = humanize_llm(text, intensity=args.mode)
        report = None

    result = validate(text, humanized)
    if args.diff:
        _emit_diff(sys.stdout, "stdin", text, humanized)
    else:
        sys.stdout.write(humanized)

    if args.json and not args.quiet:
        payload = {
            "path": "<stdin>",
            "ok": result.ok,
            "validation": result.to_dict(),
        }
        if report is not None:
            payload["report"] = report.to_dict()
        if feedback is not None:
            payload["detector_feedback"] = feedback.to_dict()
        sys.stderr.write(json.dumps(payload, indent=2) + "\n")
    elif feedback is not None and not args.quiet:
        sys.stderr.write(
            f"detector: {feedback.original_probability:.1%} → "
            f"{feedback.final_probability:.1%} "
            f"({feedback.reason_stopped})\n"
        )

    return 0 if result.ok else 2


def _llm_available() -> bool:
    import os
    import shutil
    return bool(os.environ.get("ANTHROPIC_API_KEY")) or shutil.which("claude") is not None


def _emit_diff(out, label: str, before: str, after: str) -> None:
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"{label} (original)",
        tofile=f"{label} (humanized)",
    )
    out.writelines(diff)


def _process_file_detector_feedback(
    path: Path,
    args: argparse.Namespace,
    write: bool,
    report_accumulator: list[dict],
) -> int:
    """File-mode detector feedback loop. Separate path because the backup +
    validate + write sequence differs from humanize_file_ex — we validate
    the FINAL humanized text against the original, not an intermediate."""
    from .detector import DetectorUnavailable, feedback_loop
    from .validate import format_report, validate

    original = path.read_text(encoding="utf-8")
    try:
        outcome = feedback_loop(
            original,
            target_probability=args.detector_target,
            max_iterations=args.detector_max_iterations,
            detector=args.detector_model,
        )
    except DetectorUnavailable as exc:
        sys.stderr.write(f"[{path.name}] detector feedback disabled: {exc}\n")
        return 1

    humanized = outcome.final_text
    result = validate(original, humanized)

    if args.diff:
        _emit_diff(sys.stdout, str(path), original, humanized)
    elif args.output is not None and result.ok:
        args.output.write_text(humanized, encoding="utf-8")
        if not args.quiet:
            sys.stdout.write(f"[{path.name}] wrote humanized text to {args.output}\n")
    elif write and result.ok:
        backup = path.with_name(path.stem + ".original.md")
        if not args.no_backup and not backup.exists():
            backup.write_text(original, encoding="utf-8")
        path.write_text(humanized, encoding="utf-8")

    if args.json:
        payload = {
            "path": str(path),
            "ok": result.ok,
            "validation": result.to_dict(),
            "detector_feedback": outcome.to_dict(),
        }
        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    elif not args.quiet:
        sys.stdout.write(format_report(result) + "\n")
        sys.stdout.write(
            f"  detector: {outcome.original_probability:.1%} → "
            f"{outcome.final_probability:.1%} "
            f"({outcome.reason_stopped})\n"
        )

    if args.report is not None:
        report_accumulator.append(
            {"path": str(path), "detector_feedback": outcome.to_dict()}
        )

    return 0 if result.ok else 2


def _process_file(
    path: Path,
    args: argparse.Namespace,
    report_accumulator: list[dict],
) -> int:
    from .detect import detect_file_type, should_compress
    from .humanize import humanize_file_ex
    from .validate import format_report

    if not path.exists():
        sys.stderr.write(f"Error: file not found: {path}\n")
        return 1
    if not path.is_file():
        sys.stderr.write(f"Error: not a file: {path}\n")
        return 1

    path = path.resolve()
    file_type = detect_file_type(path)

    if not args.quiet:
        sys.stdout.write(f"[{path.name}] detected: {file_type}\n")

    if not should_compress(path):
        sys.stdout.write(f"[{path.name}] skipped (not natural-language prose)\n")
        return 0

    write = not (args.dry_run or args.diff)
    if args.output is not None:
        write = False  # handle --output explicitly below

    if args.detector_feedback:
        return _process_file_detector_feedback(path, args, write, report_accumulator)

    outcome = humanize_file_ex(
        path,
        deterministic=args.deterministic,
        intensity=args.mode,
        backup=not args.no_backup,
        write=write,
        structural=args.structural,
    )

    if args.diff:
        _emit_diff(sys.stdout, str(path), outcome.original, outcome.humanized)
    elif args.output is not None and outcome.ok:
        args.output.write_text(outcome.humanized, encoding="utf-8")
        if not args.quiet:
            sys.stdout.write(f"[{path.name}] wrote humanized text to {args.output}\n")

    file_payload = {
        "path": str(path),
        "ok": outcome.ok,
        "attempts": outcome.attempts,
        "error": outcome.error,
    }
    if outcome.validation is not None and hasattr(outcome.validation, "to_dict"):
        file_payload["validation"] = outcome.validation.to_dict()
    if outcome.report is not None:
        file_payload["report"] = outcome.report.to_dict()

    if args.json:
        sys.stdout.write(json.dumps(file_payload, indent=2) + "\n")
    elif not args.quiet:
        if outcome.validation is not None and hasattr(outcome.validation, "to_dict"):
            sys.stdout.write(format_report(outcome.validation) + "\n")
        if outcome.report is not None:
            counts = outcome.report.counts_by_rule
            if counts:
                sys.stdout.write(
                    f"  replacements: {sum(counts.values())} "
                    f"({', '.join(f'{k}={v}' for k, v in sorted(counts.items()))})\n"
                )
        if outcome.error:
            sys.stderr.write(f"[{path.name}] {outcome.error}\n")

    if args.report is not None and outcome.report is not None:
        report_accumulator.append({"path": str(path), "report": outcome.report.to_dict()})

    if not outcome.ok:
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # --diff implies --dry-run. --stdin forces no-backup.
    if args.diff:
        args.dry_run = True
    if args.stdin:
        args.no_backup = True

    # --- stdin mode ---
    if args.stdin or args.files == ["-"]:
        return _process_stdin(args)

    if not args.files:
        parser.error("no input files (pass a path, or --stdin)")

    if args.output is not None and len(args.files) != 1:
        parser.error("--output requires exactly one input file")

    if args.report is not None and not args.deterministic:
        parser.error("--report requires --deterministic")

    paths = [Path(p) for p in args.files]
    report_accumulator: list[dict] = []

    exit_codes = [_process_file(p, args, report_accumulator) for p in paths]

    if args.report is not None:
        args.report.write_text(
            json.dumps(report_accumulator, indent=2) + "\n", encoding="utf-8"
        )
        if not args.quiet:
            sys.stdout.write(f"wrote audit trail to {args.report}\n")

    if all(code == 0 for code in exit_codes):
        return 0
    if all(code != 0 for code in exit_codes):
        # All files failed — surface the worst code.
        return max(exit_codes)
    # Mixed — partial success
    return 3


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
