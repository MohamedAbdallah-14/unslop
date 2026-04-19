"""Command-line interface for humanizer-humanize.

Usage:
  humanize [--deterministic] <filepath>
  humanize -h | --help
"""

from __future__ import annotations

import sys
from pathlib import Path


USAGE = """\
Usage: humanize [--deterministic] <filepath>

Rewrite a markdown / text file to remove AI-isms while preserving code,
URLs, paths, and headings. The original is backed up as <stem>.original.md.

Options:
  --deterministic   Use the fast regex pass (no API call, no subprocess).
                    Default: LLM mode (Anthropic SDK or `claude --print`).
  -h, --help        Show this message.
"""


def print_usage() -> None:
    sys.stdout.write(USAGE)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print_usage()
        sys.exit(0 if args else 1)

    deterministic = False
    if args[0] == "--deterministic":
        deterministic = True
        args = args[1:]

    if len(args) != 1:
        print_usage()
        sys.exit(1)

    filepath = Path(args[0])
    if not filepath.exists():
        sys.stderr.write(f"Error: file not found: {filepath}\n")
        sys.exit(1)
    if not filepath.is_file():
        sys.stderr.write(f"Error: not a file: {filepath}\n")
        sys.exit(1)

    filepath = filepath.resolve()

    from .detect import detect_file_type, should_compress
    from .humanize import humanize_file

    file_type = detect_file_type(filepath)
    sys.stdout.write(f"Detected: {file_type}\n")

    if not should_compress(filepath):
        sys.stdout.write(f"Skipping: file is not natural language ({filepath.name})\n")
        sys.exit(0)

    mode_label = "deterministic regex" if deterministic else "LLM (Claude)"
    sys.stdout.write(f"Starting humanization ({mode_label})...\n")

    try:
        success = humanize_file(filepath, deterministic=deterministic)
    except KeyboardInterrupt:
        sys.stderr.write("\nInterrupted.\n")
        sys.exit(130)
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)

    if success:
        backup = filepath.with_name(filepath.stem + ".original.md")
        sys.stdout.write(f"\nDone.\n  humanized: {filepath}\n  backup:    {backup}\n")
        sys.exit(0)
    else:
        if deterministic:
            sys.stderr.write("Humanization failed validation in deterministic mode.\n")
        else:
            sys.stderr.write("Humanization failed validation after retries.\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
