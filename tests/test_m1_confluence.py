import random

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


def test_triangulation_confluence_numeric_regression():
    """Finite-sample numeric smoke test; not a substitute for symbolic equality."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    omegaB = canonical_form_from_triangulation(triangulation_B_m1(x, y)).simplify()

    # Smoke-check equality on a fixed-size interior sample only.
    # The symbolic test above remains the conclusive confluence check.
    pts = region.sample_interior_points(n=15)
    for (xv, yv) in pts:
        a = complex(omegaA.prefactor.subs({x: xv, y: yv}).evalf(50))
        b = complex(omegaB.prefactor.subs({x: xv, y: yv}).evalf(50))
        assert abs(a - b) < 1e-10
