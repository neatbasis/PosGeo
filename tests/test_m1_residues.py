# tests/test_m1_residues.py
import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1, m1_pentagon_vertices
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
    expected_interval_prefactor_for_m1_facet,
    expected_interval_prefactor_from_chart_ccw
)


def test_residues_match_interval_forms_up_to_sign():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts = {k: v[0] for k, v in m1_facet_charts_all(x, y).items()}

    for facet_name, chart in charts.items():
        res = residue_2form_on_facet(omega, chart).simplify()
        expected = expected_interval_prefactor_for_m1_facet(facet_name, res.t)

        diff1 = sp.simplify(res.prefactor - expected)
        diff2 = sp.simplify(res.prefactor + expected)

        assert (diff1 == 0) or (diff2 == 0), (
            f"Residue mismatch on {facet_name}\n"
            f"res={res.prefactor}\nexp={expected}\n"
            f"diff={diff1}, diff(signflip)={diff2}"
        )
        
def test_residues_match_interval_forms_deterministic_sign():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts = {k: v[0] for k, v in m1_facet_charts_all(x, y).items()}
    verts = list(m1_pentagon_vertices())

    for facet, chart in charts.items():
        res = residue_2form_on_facet(omega, chart).simplify()
        exp = expected_interval_prefactor_from_chart_ccw(facet, chart, verts, region=region)
        
        assert sp.simplify(res.prefactor - exp) == 0, (
            f"[{facet}] deterministic residue mismatch in {chart.name}\n"
            f"res={res.prefactor}\nexp={exp}\n"
            f"diff={sp.simplify(res.prefactor - exp)}"
        )
