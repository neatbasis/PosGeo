#!/usr/bin/env python3
"""Guardrail: test helpers must not define geometry/chart fixtures.

Invariant tests must consume fixtures from product modules (`posgeo.geometry`,
`posgeo.forms`) instead of creating local geometry constructors in
`tests/helpers/`.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Iterable

HELPERS_DIR = Path("tests/helpers")
TARGET_TYPES = {"Region2D", "FacetChart"}
SELECTOR_FILE = HELPERS_DIR / "geometry_cases.py"


def _is_target_type_expr(node: ast.AST | None) -> bool:
    if node is None:
        return False

    if isinstance(node, ast.Name):
        return node.id in TARGET_TYPES

    if isinstance(node, ast.Attribute):
        return node.attr in TARGET_TYPES

    if isinstance(node, ast.Subscript):
        return _is_target_type_expr(node.value) or _is_target_type_expr(node.slice)

    if isinstance(node, ast.Tuple):
        return any(_is_target_type_expr(elt) for elt in node.elts)

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _is_target_type_expr(node.left) or _is_target_type_expr(node.right)

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return any(target in node.value for target in TARGET_TYPES)

    return False


def _call_targets_type(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in TARGET_TYPES
    if isinstance(func, ast.Attribute):
        return func.attr in TARGET_TYPES
    return False


def find_violations(file_path: Path) -> list[str]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _is_target_type_expr(node.returns):
                type_str = ast.unparse(node.returns) if node.returns is not None else "<unknown>"
                violations.append(
                    f"{file_path}:{node.lineno}: function `{node.name}` return annotation uses `{type_str}`"
                )

        if isinstance(node, ast.Return) and isinstance(node.value, ast.Call) and _call_targets_type(node.value):
            ctor = ast.unparse(node.value.func)
            violations.append(f"{file_path}:{node.lineno}: return statement constructs `{ctor}(...)`")

    if file_path == SELECTOR_FILE:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _call_targets_type(node):
                ctor = ast.unparse(node.func)
                violations.append(
                    f"{file_path}:{node.lineno}: selector file must not construct `{ctor}(...)`"
                )

    return violations


def collect_helper_files(base_dir: Path = HELPERS_DIR) -> list[Path]:
    return sorted(path for path in base_dir.glob("*.py") if path.is_file())


def run_guardrail(base_dir: Path = HELPERS_DIR) -> list[str]:
    violations: list[str] = []
    for helper in collect_helper_files(base_dir):
        violations.extend(find_violations(helper))
    return violations


def main(argv: Iterable[str] | None = None) -> int:
    _ = argv
    if not HELPERS_DIR.exists():
        print(f"fixture guardrail: helpers directory not found: {HELPERS_DIR}", file=sys.stderr)
        return 1

    violations = run_guardrail(HELPERS_DIR)
    if violations:
        print(
            "fixture guardrail failed: define geometry/chart fixtures only in "
            "`posgeo.geometry` and `posgeo.forms`, not in tests/helpers.",
            file=sys.stderr,
        )
        for item in violations:
            print(f"- {item}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
