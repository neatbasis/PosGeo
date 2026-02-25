"""Meta-tests enforcing axiom traceability metadata coverage."""

from __future__ import annotations

import importlib
import inspect
import re
from collections import defaultdict

MANDATORY_AXIOMS = {"TA-LP", "TA-RR", "TA-VN", "TA-E1", "TA-E3", "TA-GC", "TA-TC"}
TEST_TYPE_PATTERN = re.compile(r"Test type:\s*(structural|failure-mode)", re.IGNORECASE)
AXIOM_PATTERN = re.compile(r"Axiom IDs:\s*([A-Z0-9,\-\s]+?)(?:\.|\n)", re.IGNORECASE)
MODULES = [
    "tests.test_m1_pole_locality",
    "tests.test_m1_simple_poles_only",
    "tests.test_m1_residues",
    "tests.test_m1_residues_chart_independence",
    "tests.test_m1_vertex_residues",
    "tests.test_m1_confluence",
    "tests.test_reparam_nonconstant",
]


def _parse_metadata(doc: str) -> tuple[set[str], str]:
    axiom_match = AXIOM_PATTERN.search(doc)
    type_match = TEST_TYPE_PATTERN.search(doc)
    assert axiom_match is not None, f"missing `Axiom IDs:` marker in docstring: {doc!r}"
    assert type_match is not None, f"missing `Test type:` marker in docstring: {doc!r}"

    axiom_ids = {token.strip() for token in axiom_match.group(1).split(",") if token.strip()}
    test_type = type_match.group(1).lower()
    return axiom_ids, test_type


def test_mandatory_axioms_have_structural_and_failure_mode_coverage():
    """Axiom IDs: TA-LP, TA-RR, TA-VN, TA-E1, TA-E3, TA-GC, TA-TC. Test type: structural."""
    coverage: dict[str, set[str]] = defaultdict(set)

    for module_name in MODULES:
        module = importlib.import_module(module_name)
        for _, fn in inspect.getmembers(module, inspect.isfunction):
            if not fn.__name__.startswith("test_"):
                continue
            doc = inspect.getdoc(fn)
            if not doc:
                continue
            axiom_ids, test_type = _parse_metadata(doc)
            for axiom_id in axiom_ids:
                coverage[axiom_id].add(test_type)

    for axiom_id in sorted(MANDATORY_AXIOMS):
        assert "structural" in coverage[axiom_id], (
            f"{axiom_id} missing structural coverage in test docstring metadata"
        )
        assert "failure-mode" in coverage[axiom_id], (
            f"{axiom_id} missing failure-mode coverage in test docstring metadata"
        )
