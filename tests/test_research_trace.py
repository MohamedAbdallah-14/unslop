"""Guardrail tests for docs/research/IMPLEMENTATION_TRACE.md.

The research trace is useful only if each mapping points to real research files
and real implementation files. This test keeps that contract live in CI.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "docs" / "research" / "IMPLEMENTATION_TRACE.md"


def _mapping_rows(trace_text: str) -> list[list[str]]:
    """Return parsed table rows from the main mapping section."""
    in_mapping = False
    rows: list[list[str]] = []
    for raw_line in trace_text.splitlines():
        line = raw_line.strip()
        if line == "## The mapping":
            in_mapping = True
            continue
        if in_mapping and line.startswith("## "):
            break
        if not in_mapping:
            continue
        if not line.startswith("|"):
            continue
        if line.startswith("| Research finding |") or line.startswith("|---|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 4:
            rows.append(cells)
    return rows


def _backticks(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def _looks_like_file_path(token: str) -> bool:
    if "/" in token:
        return True
    return token.endswith(
        (".md", ".py", ".sh", ".json", ".toml", ".ps1", ".js")
    )


def test_trace_rows_point_to_real_files_and_categories() -> None:
    trace = TRACE_PATH.read_text()
    rows = _mapping_rows(trace)
    assert rows, "No mapping rows found in IMPLEMENTATION_TRACE.md"

    for research_finding, source_col, _implementation_col, where_col in rows:
        cat_numbers = re.findall(r"Cat\s+(\d{2})", source_col)
        assert cat_numbers, f"Missing category reference: {research_finding}"
        for cat in cat_numbers:
            idx = ROOT / "docs" / "research" / f"{cat}-"  # prefix match below
            matching = sorted((ROOT / "docs" / "research").glob(f"{cat}-*/INDEX.md"))
            assert matching, f"Missing research INDEX for Cat {cat}: {idx}*"

        where_paths = [p for p in _backticks(where_col) if _looks_like_file_path(p)]
        assert where_paths, f"Missing implementation file path(s): {research_finding}"
        for rel_path in where_paths:
            abs_path = ROOT / rel_path
            assert abs_path.exists(), f"Missing implementation file: {rel_path}"


def test_trace_identifiers_exist_in_cited_files() -> None:
    trace = TRACE_PATH.read_text()
    rows = _mapping_rows(trace)

    for research_finding, _source_col, implementation_col, where_col in rows:
        identifiers = _backticks(implementation_col)
        where_paths = [p for p in _backticks(where_col) if _looks_like_file_path(p)]
        if not identifiers or not where_paths:
            continue

        blobs: list[str] = []
        for rel_path in where_paths:
            abs_path = ROOT / rel_path
            if abs_path.exists():
                blobs.append(abs_path.read_text())
        combined = "\n".join(blobs)

        for ident in identifiers:
            # Skip markers that are not literal code identifiers.
            if ident.startswith("[") or ident.startswith("http"):
                continue
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_\-]*", ident) is None:
                continue
            assert ident in combined, (
                f"Identifier `{ident}` from trace row not found in cited files: "
                f"{research_finding}"
            )
