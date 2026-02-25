# Axioms: TA-TC, TA-E1

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    triangulation_B_m1,
)
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def test_triangulation_confluence_symbolic():
    """Exact identity gate: triangulation A and B must match symbolically."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    omegaB = canonical_form_from_triangulation(triangulation_B_m1(x, y)).simplify()

    assert sp.simplify(omegaA.prefactor - omegaB.prefactor) == 0


def test_triangulation_confluence_exact_rational_regression():
    """Finite-sample exact rational smoke test; not a substitute for symbolic equality."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    omegaB = canonical_form_from_triangulation(triangulation_B_m1(x, y)).simplify()

    # Smoke-check equality on a fixed-size deterministic interior rational sample only.
    # The symbolic test above remains the conclusive confluence check.
    pts = region.fixed_interior_rational_points(n=15)
    for i, (xv, yv) in enumerate(pts):
        point_id = f"confluence-subs[pt#{i}:x={xv},y={yv}]"
        prefactor_a = assert_valid_symbolic_value(
            omegaA.prefactor.subs({x: xv, y: yv}),
            context=point_id,
            quantity="triangulation-A prefactor",
        )
        prefactor_b = assert_valid_symbolic_value(
            omegaB.prefactor.subs({x: xv, y: yv}),
            context=point_id,
            quantity="triangulation-B prefactor",
        )
        delta = assert_valid_symbolic_value(
            prefactor_a - prefactor_b,
            context=point_id,
            quantity="prefactor delta",
        )
        assert delta == 0, f"{point_id}: expected zero A-B difference, got {delta}"
