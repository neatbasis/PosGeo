from __future__ import annotations

from pathlib import Path

import pytest

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.validation.preconditions import OutOfScopeInputError, assert_canonical_scope


_CANONICAL_INVARIANT_FILES = {
    "test_m1_confluence.py",
    "test_m1_pole_locality.py",
    "test_m1_residues.py",
    "test_m1_residues_chart_independence.py",
    "test_m1_simple_poles_only.py",
    "test_m1_vertex_residues.py",
    "test_chart_jacobian_sign_matches_s.py",
    "test_reparam_nonconstant.py",
}


@pytest.fixture(autouse=True)
def enforce_repository_scope_preconditions(request: pytest.FixtureRequest) -> None:
    """Gate canonical-form invariant tests behind repository scope assumptions."""
    test_file = Path(str(request.node.fspath)).name
    if test_file not in _CANONICAL_INVARIANT_FILES:
        return

    region = PentagonM1Region.build()
    vertices = list(PentagonM1Region.vertices())
    try:
        assert_canonical_scope(
            region=region,
            vertices=vertices,
            geometry_class="convex_polygon_2d_linear",
        )
    except OutOfScopeInputError as exc:
        pytest.fail(f"out-of-scope input: {exc}", pytrace=False)
