import sympy as sp

from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from posgeo.forms.residues2d import m1_facet_charts_all, pullback_1form, residue_2form_on_facet
from posgeo.geometry.region2d import PentagonM1Region
from tests.helpers.orientation_consistency import (
    equal_up_to_sign,
    jacobian_det,
    solve_reparam_t1_of_t0,
)
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def test_orientation_consistency_structural_up_to_sign():
    """Axiom IDs: TA-E3, TA-RR. Test type: structural.

Orientation-agnostic layer: Jacobian orientation bits and pullback residues agree up to ±.
"""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet_name}"

        for chart in charts:
            det = jacobian_det(chart)
            assert det in (1, -1), f"Unexpected Jacobian sign for {facet_name}/{chart.name}: det={det}"

        base = charts[0]
        base_res = residue_2form_on_facet(omega2, base).simplify()
        base_context = f"{facet_name}/{base.name}"
        base_prefactor = assert_valid_symbolic_value(
            base_res.prefactor, context=base_context, quantity="residue prefactor"
        )

        for chart in charts[1:]:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t0 = base.t
            t1_of_t0 = solve_reparam_t1_of_t0(base, chart)
            pulled = pullback_1form(res, t_new=t0, t_old_expr=t1_of_t0).simplify()

            pulled_context = f"{facet_name}/{base.name}<={chart.name}"
            pulled_prefactor = assert_valid_symbolic_value(
                pulled.prefactor,
                context=pulled_context,
                quantity="pulled residue prefactor",
            )

            assert equal_up_to_sign(pulled_prefactor, base_prefactor), (
                f"[{facet_name}] pullback mismatch (up to sign) for {base.name} <= {chart.name}\n"
                f"base={base_prefactor}\n"
                f"pulled={pulled_prefactor}\n"
                f"t1(t0)={t1_of_t0}"
            )


def test_orientation_consistency_deterministic_fixed_sign():
    """Axiom IDs: TA-E3, TA-RR. Test type: failure-mode.

Orientation-fixed layer: Jacobian sign equals chart.s and pullback residues match exactly.
"""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet_name}"

        for chart in charts:
            det = jacobian_det(chart)
            assert sp.simplify(det - chart.s) == 0, (
                f"Jacobian sign mismatch on {facet_name}/{chart.name}: det={det}, s={chart.s}"
            )

        base = charts[0]
        base_res = residue_2form_on_facet(omega2, base).simplify()
        base_context = f"{facet_name}/{base.name}"
        base_prefactor = assert_valid_symbolic_value(
            base_res.prefactor, context=base_context, quantity="residue prefactor"
        )

        for chart in charts[1:]:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t0 = base.t
            t1_of_t0 = solve_reparam_t1_of_t0(base, chart)
            pulled = pullback_1form(res, t_new=t0, t_old_expr=t1_of_t0).simplify()

            pulled_context = f"{facet_name}/{base.name}<={chart.name}"
            pulled_prefactor = assert_valid_symbolic_value(
                pulled.prefactor,
                context=pulled_context,
                quantity="pulled residue prefactor",
            )

            assert sp.simplify(pulled_prefactor - base_prefactor) == 0, (
                f"[{facet_name}] deterministic pullback mismatch for {base.name} <= {chart.name}\n"
                f"base={base_prefactor}\n"
                f"pulled={pulled_prefactor}\n"
                f"t1(t0)={t1_of_t0}\n"
                f"diff={sp.simplify(pulled_prefactor - base_prefactor)}"
            )
