# Axioms: TA-TC, TA-E1

import sympy as sp
import pytest

from posgeo.forms.canonical2d import canonical_form_from_triangulation
from tests.helpers.geometry_cases import GEOMETRY_CASES

@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_triangulation_confluence_symbolic(geometry_case):
    """Axiom IDs: TA-TC, TA-E1. Test type: structural.

Exact identity gate: triangulation A and B must match symbolically."""
    region = geometry_case.build_region()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(
        geometry_case.tri_a(x, y),
        region=region,
        vertices=geometry_case.vertices(),
    ).simplify()
    omegaB = canonical_form_from_triangulation(
        geometry_case.tri_b(x, y),
        region=region,
        vertices=geometry_case.vertices(),
    ).simplify()

    assert sp.simplify(omegaA.prefactor - omegaB.prefactor) == 0


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_triangulation_confluence_exact_rational_regression(geometry_case):
    """Axiom IDs: TA-TC, TA-E1. Test type: failure-mode.

Finite-sample rational regression that fails on numeric drift or invalid finite values."""
    region = geometry_case.build_region()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(
        geometry_case.tri_a(x, y),
        region=region,
        vertices=geometry_case.vertices(),
    ).simplify()
    omegaB = canonical_form_from_triangulation(
        geometry_case.tri_b(x, y),
        region=region,
        vertices=geometry_case.vertices(),
    ).simplify()

    # Smoke-check equality on a fixed-size deterministic interior rational sample only.
    # The symbolic test above remains the conclusive confluence check.
    pts = region.fixed_interior_rational_points(n=15)
    for i, (xv, yv) in enumerate(pts):
        point_id = f"confluence-subs[pt#{i}:x={xv},y={yv}]"
        prefactor_a = sp.simplify(omegaA.prefactor.subs({x: xv, y: yv}))
        prefactor_b = sp.simplify(omegaB.prefactor.subs({x: xv, y: yv}))
        assert prefactor_a.is_finite is not False, (
            f"{point_id}: triangulation-A prefactor became non-finite: {prefactor_a}"
        )
        assert prefactor_b.is_finite is not False, (
            f"{point_id}: triangulation-B prefactor became non-finite: {prefactor_b}"
        )
        assert sp.simplify(prefactor_a - prefactor_b) == 0, (
            f"{point_id}: expected zero A-B difference, got {prefactor_a - prefactor_b}"
        )
