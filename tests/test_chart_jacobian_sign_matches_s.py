import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.residues2d import m1_facet_charts_all


def test_chart_jacobian_sign_matches_s_for_all_m1_facet_charts():
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            jac_det = sp.simplify(
                sp.diff(chart.x_of, chart.u) * sp.diff(chart.y_of, chart.t)
                - sp.diff(chart.x_of, chart.t) * sp.diff(chart.y_of, chart.u)
            )

            assert sp.simplify(jac_det - chart.s) == 0, (
                f"Jacobian sign mismatch on {facet_name}/{chart.name}: det={jac_det}, s={chart.s}"
            )
