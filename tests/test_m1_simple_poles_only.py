# Axioms: TA-LP, TA-GC

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from posgeo.forms.residues2d import m1_facet_charts_all
from tests.helpers.pole_checks import (
    assert_boundary_pole_invariant,
)
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits():
    """Axiom IDs: TA-LP, TA-GC. Test type: failure-mode."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    assert_boundary_pole_invariant(
        omega.prefactor,
        [f.expr for f in region.facets.values()],
        x,
        y,
        require_simple_poles=True,
    )

    for charts in m1_facet_charts_all(x, y).values():
        for chart in charts:
            f_ut = sp.simplify(omega.prefactor.subs({x: chart.x_of, y: chart.y_of}))

            chart_context = f"facet-limit[{chart.name}]"
            lim1 = assert_valid_symbolic_value(
                sp.limit(chart.u * f_ut, chart.u, 0),
                context=chart_context,
                quantity="first-order limit",
            )
            lim2 = assert_valid_symbolic_value(
                sp.limit((chart.u**2) * f_ut, chart.u, 0),
                context=chart_context,
                quantity="second-order limit",
            )

            assert lim1 != sp.Integer(0), (
                f"{chart_context}: expected nonzero first-order limit, got {lim1}"
            )
            assert lim2 == 0, (
                f"{chart_context}: expected second-order coefficient to vanish, got {lim2}"
            )
