# Axioms: TA-RR, TA-VN

# tests/test_m1_residues.py
import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1, m1_pentagon_vertices
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
    expected_interval_prefactor_from_chart,
    expected_interval_prefactor_from_chart_ccw
)
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def test_residues_match_interval_forms_up_to_sign():
    """TA-RR: structural residue relation (orientation-agnostic, up to ±) on every chart."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    verts = list(m1_pentagon_vertices())

    charts_by_facet = m1_facet_charts_all(x, y)

    for facet_name, charts in charts_by_facet.items():
        for chart in charts:
            res = residue_2form_on_facet(omega, chart).simplify()
            expected = expected_interval_prefactor_from_chart(facet_name, chart, verts)
            context = f"{facet_name}/{chart.name}"

            res_prefactor = assert_valid_symbolic_value(
                res.prefactor, context=context, quantity="residue prefactor"
            )
            expected_prefactor = assert_valid_symbolic_value(
                expected, context=context, quantity="expected interval prefactor"
            )

            diff1 = sp.simplify(res_prefactor - expected_prefactor)
            diff2 = sp.simplify(res_prefactor + expected_prefactor)

            assert (diff1 == 0) or (diff2 == 0), (
                f"[TA-RR] Residue mismatch on {facet_name} in chart {chart.name}\n"
                f"res={res.prefactor}\nexp={expected}\n"
                f"diff={diff1}, diff(signflip)={diff2}"
            )
        
def test_residues_match_interval_forms_deterministic_sign():
    """TA-RR+O2: orientation-fixed residue relation in CCW convention (no ± ambiguity) on every chart."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    verts = list(m1_pentagon_vertices())

    for facet, charts in charts_by_facet.items():
        for chart in charts:
            res = residue_2form_on_facet(omega, chart).simplify()
            exp = expected_interval_prefactor_from_chart_ccw(facet, chart, verts, region=region)
            context = f"{facet}/{chart.name}"

            res_prefactor = assert_valid_symbolic_value(
                res.prefactor, context=context, quantity="residue prefactor"
            )
            exp_prefactor = assert_valid_symbolic_value(
                exp, context=context, quantity="expected interval prefactor"
            )

            assert sp.simplify(res_prefactor - exp_prefactor) == 0, (
                f"[TA-RR+O2][{facet}] deterministic residue mismatch in {chart.name}\n"
                f"res={res.prefactor}\nexp={exp}\n"
                f"diff={sp.simplify(res.prefactor - exp)}"
            )
