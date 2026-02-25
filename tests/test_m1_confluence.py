# Axioms: TA-TC, TA-E1

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    triangulation_B_m1,
)


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
    for (xv, yv) in pts:
        delta = sp.simplify(
            omegaA.prefactor.subs({x: xv, y: yv}) - omegaB.prefactor.subs({x: xv, y: yv})
        )
        assert delta == 0
