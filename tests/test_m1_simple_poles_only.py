# Axioms: TA-LP, TA-GC

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from posgeo.forms.residues2d import m1_facet_charts_all
from tests.helpers.pole_checks import (
    assert_boundary_subset,
    assert_multiplicity_one,
    normalized_denominator_factors,
)


def test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits():
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    factors = normalized_denominator_factors(omega.prefactor, x, y)
    assert_boundary_subset(factors, [f.expr for f in region.facets.values()], x, y)
    assert_multiplicity_one(factors)

    for charts in m1_facet_charts_all(x, y).values():
        for chart in charts:
            f_ut = sp.simplify(omega.prefactor.subs({x: chart.x_of, y: chart.y_of}))

            lim1 = sp.simplify(sp.limit(chart.u * f_ut, chart.u, 0))
            lim2 = sp.simplify(sp.limit((chart.u**2) * f_ut, chart.u, 0))

            assert lim1 not in {sp.Integer(0), sp.oo, -sp.oo, sp.zoo, sp.nan}, (
                f"Expected finite nonzero first-order limit on {chart.name}, got {lim1}"
            )
            assert lim2 == 0, f"Expected second-order coefficient to vanish on {chart.name}, got {lim2}"
