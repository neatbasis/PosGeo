# Axioms: TA-RR, TA-VN

import sympy as sp

from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    m1_pentagon_vertices,
)
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
    expected_interval_prefactor_from_chart,
    expected_interval_prefactor_from_chart_ccw,
)
from posgeo.geometry.region2d import PentagonM1Region
from tests.helpers.orientation_consistency import equal_up_to_sign
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def test_residue_chart_independence_orientation_agnostic_structural():
    """Axiom IDs: TA-RR, TA-E3. Test type: structural.

Orientation-agnostic layer: each chart residue matches the canonical interval 1-form up to ±.
"""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    verts = list(m1_pentagon_vertices())

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet}"

        for ch in charts:
            res = residue_2form_on_facet(omega2, ch).simplify()
            context = f"{facet}/{ch.name}"
            res_prefactor = assert_valid_symbolic_value(
                res.prefactor, context=context, quantity="residue prefactor"
            )

            exp = expected_interval_prefactor_from_chart(facet, ch, verts)
            exp_prefactor = assert_valid_symbolic_value(
                exp, context=context, quantity="expected interval prefactor"
            )
            assert equal_up_to_sign(res_prefactor, exp_prefactor), (
                f"[{facet}] residue in {ch.name} does not match expected interval form up to sign.\n"
                f"res={res.prefactor}\nexp={exp}\n"
                f"diff={sp.simplify(res.prefactor - exp)}\n"
                f"diff(signflip)={sp.simplify(res.prefactor + exp)}"
            )


def test_residue_chart_independence_orientation_fixed_deterministic():
    """Axiom IDs: TA-RR, TA-E3. Test type: failure-mode.

Orientation-fixed layer: CCW-oriented residues are deterministic and exact in every chart.
"""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    verts = list(m1_pentagon_vertices())

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet}"

        for ch in charts:
            res = residue_2form_on_facet(omega2, ch).simplify()
            exp = expected_interval_prefactor_from_chart_ccw(facet, ch, verts, region=region)
            context = f"{facet}/{ch.name}"
            res_prefactor = assert_valid_symbolic_value(
                res.prefactor, context=context, quantity="residue prefactor"
            )
            exp_prefactor = assert_valid_symbolic_value(
                exp, context=context, quantity="expected interval prefactor"
            )

            assert sp.simplify(res_prefactor - exp_prefactor) == 0, (
                f"[{facet}] deterministic residue mismatch in {ch.name}\n"
                f"res={res.prefactor}\nexp={exp}\n"
                f"diff={sp.simplify(res.prefactor - exp)}"
            )
