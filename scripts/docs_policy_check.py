#!/usr/bin/env python3
"""Enforce documentation policy coupling for README reference updates."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

README = "README.md"
AXIOMS = "AXIOMS.md"
TRACEABILITY = "tests/AXIOM_TRACEABILITY.md"
VALID_STATUSES = {"implemented", "partial", "out-of-scope"}


@dataclass(frozen=True)
class Section:
    title: str
    start: int
    end: int


def run_git(*args: str) -> str:
    cmd = ["git", *args]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        print(
            "git executable not found; install git on the runner or use an image with git preinstalled.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        failing_cmd = exc.cmd if exc.cmd else cmd
        if isinstance(failing_cmd, (list, tuple)):
            cmd_text = shlex.join(str(part) for part in failing_cmd)
        else:
            cmd_text = str(failing_cmd)

        print(f"git command failed: {cmd_text}", file=sys.stderr)
        if exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)

        code = exc.returncode if isinstance(exc.returncode, int) and exc.returncode != 0 else 1
        raise SystemExit(code) from exc


def parse_sections(readme_text: str) -> dict[str, Section]:
    lines = readme_text.splitlines()
    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    headings: list[tuple[int, int, str]] = []

    for idx, line in enumerate(lines, start=1):
        match = heading_re.match(line)
        if match:
            headings.append((idx, len(match.group(1)), match.group(2).strip()))

    sections: dict[str, Section] = {}
    for i, (line_no, level, title) in enumerate(headings):
        end = len(lines)
        for next_line_no, next_level, _ in headings[i + 1 :]:
            if next_level <= level:
                end = next_line_no - 1
                break
        sections[title] = Section(title=title, start=line_no, end=end)

    return sections


def parse_changed_lines(base: str, head: str, file_path: str) -> set[int]:
    diff = run_git("diff", "--unified=0", f"{base}..{head}", "--", file_path)
    changed: set[int] = set()

    for line in diff.splitlines():
        if not line.startswith("@@"):
            continue
        match = re.search(r"\+(\d+)(?:,(\d+))?", line)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        if count == 0:
            continue
        changed.update(range(start, start + count))

    return changed


def changed_in_section(changed_lines: set[int], section: Section) -> bool:
    return any(section.start <= line_no <= section.end for line_no in changed_lines)


def extract_added_reference_urls(base: str, head: str) -> set[str]:
    diff = run_git("diff", "--unified=0", f"{base}..{head}", "--", README)
    urls: set[str] = set()
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for url in re.findall(r"\((https?://[^)]+)\)", line):
            urls.add(url.rstrip("/"))
    return urls


def extract_table_statuses(readme_text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    row_re = re.compile(r"^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(implemented|partial|out-of-scope)\s*\|\s*$")
    url_re = re.compile(r"\((https?://[^)]+)\)")

    for line in readme_text.splitlines():
        match = row_re.match(line.strip())
        if not match:
            continue
        source_cell = match.group(1)
        status = match.group(3)
        for url in url_re.findall(source_cell):
            statuses[url.rstrip("/")] = status

    return statuses


def get_changed_files(base: str, head: str) -> set[str]:
    output = run_git("diff", "--name-only", f"{base}..{head}")
    return {line.strip() for line in output.splitlines() if line.strip()}


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD~1", help="Base revision for diff")
    parser.add_argument("--head", default="HEAD", help="Head revision for diff")
    args = parser.parse_args(list(argv) if argv is not None else None)

    base = args.base
    head = args.head
    changed_files = get_changed_files(base, head)

    if README not in changed_files:
        return 0

    readme_text = Path(README).read_text(encoding="utf-8")
    sections = parse_sections(readme_text)

    references_section = sections.get("📚 Foundational Papers & Articles")
    scope_table_section = sections.get("Source-to-scope status table")

    if references_section is None or scope_table_section is None:
        print("docs policy check: unable to locate required README sections.", file=sys.stderr)
        return 1

    readme_changed = parse_changed_lines(base, head, README)
    touched_references = changed_in_section(readme_changed, references_section)

    if touched_references:
        touched_scope_table = changed_in_section(readme_changed, scope_table_section)

        axioms_changed = AXIOMS in changed_files
        touched_limitations = False
        if axioms_changed:
            axioms_text = Path(AXIOMS).read_text(encoding="utf-8")
            axioms_sections = parse_sections(axioms_text)
            limitations = axioms_sections.get("VII. Explicit Limitations (v0.2)")
            if limitations:
                axioms_changed_lines = parse_changed_lines(base, head, AXIOMS)
                touched_limitations = changed_in_section(axioms_changed_lines, limitations)

        trace_changed = TRACEABILITY in changed_files
        touched_provenance = False
        if trace_changed:
            trace_text = Path(TRACEABILITY).read_text(encoding="utf-8")
            trace_sections = parse_sections(trace_text)
            provenance = trace_sections.get("Literature provenance (non-normative)")
            if provenance:
                trace_changed_lines = parse_changed_lines(base, head, TRACEABILITY)
                touched_provenance = changed_in_section(trace_changed_lines, provenance)

        if not (touched_scope_table or touched_limitations or touched_provenance):
            print(
                "docs policy check failed: README reference section changed, but none of the required coupled sections were updated:",
                file=sys.stderr,
            )
            print("- README.md Source-to-scope status table", file=sys.stderr)
            print("- AXIOMS.md VII. Explicit Limitations (v0.2)", file=sys.stderr)
            print("- tests/AXIOM_TRACEABILITY.md Literature provenance (non-normative)", file=sys.stderr)
            return 1

    table_statuses = extract_table_statuses(readme_text)
    added_urls = extract_added_reference_urls(base, head)

    missing = [
        url for url in sorted(added_urls) if table_statuses.get(url) not in VALID_STATUSES
    ]
    if missing:
        print(
            "docs policy check failed: added reference URLs must appear in the README source-to-scope table with status implemented/partial/out-of-scope.",
            file=sys.stderr,
        )
        for url in missing:
            print(f"- {url}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
