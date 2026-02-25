import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    m1_pentagon_vertices,
    triangulation_A_m1,
)
from posgeo.forms.residues2d import (
    interval_endpoints_from_chart_ccw,
    m1_facet_charts_all,
    residue_2form_on_facet,
)


def test_m1_vertex_endpoint_residues_are_simple_and_ccw_positive_one():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(m1_pentagon_vertices())

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t = res.t
            ts, te = interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw)

            # Medium check: endpoint poles are simple.
            c1_start = sp.simplify(sp.limit((t - ts) * res.prefactor, t, ts))
            c2_start = sp.simplify(sp.limit((t - ts) ** 2 * res.prefactor, t, ts))
            c1_end = sp.simplify(sp.limit((t - te) * res.prefactor, t, te))
            c2_end = sp.simplify(sp.limit((t - te) ** 2 * res.prefactor, t, te))

            for label, c1, c2 in (
                ("start", c1_start, c2_start),
                ("end", c1_end, c2_end),
            ):
                assert c1 not in {sp.Integer(0), sp.oo, -sp.oo, sp.zoo, sp.nan}, (
                    f"{facet_name}/{chart.name} {label} endpoint first coefficient invalid: {c1}"
                )
                assert c2 == 0, f"{facet_name}/{chart.name} {label} endpoint has second-order term: {c2}"

            # Strong check: iterated endpoint residues in CCW convention are +1.
            # We use endpoint-local coordinates that vanish at each endpoint:
            # w_start = (ts - t), w_end = (t - te).
            r_start_ccw = sp.simplify(sp.limit((ts - t) * res.prefactor, t, ts))
            r_end_ccw = sp.simplify(sp.limit((t - te) * res.prefactor, t, te))

            assert sp.simplify(r_start_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW start residue != +1: {r_start_ccw}"
            )
            assert sp.simplify(r_end_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW end residue != +1: {r_end_ccw}"
            )
