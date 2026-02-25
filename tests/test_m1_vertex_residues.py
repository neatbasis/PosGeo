# Axioms: TA-RR, TA-VN

import sympy as sp

from posgeo.geometry import M1_PENTAGON_FIXTURE
from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
)
from posgeo.forms.residues2d import (
    interval_endpoints_from_chart_ccw,
    m1_facet_charts_all,
    residue_2form_on_facet,
)
from tests.helpers.symbolic_validity import assert_valid_symbolic_value


def _endpoint_residue(
    prefactor: sp.Expr,
    t: sp.Symbol,
    endpoint: sp.Expr,
    *,
    orientation_sign: int,
    context: str,
) -> sp.Expr:
    return assert_valid_symbolic_value(
        sp.limit(orientation_sign * (t - endpoint) * prefactor, t, endpoint),
        context=context,
        quantity="endpoint residue",
    )


def _assert_simple_pole(prefactor: sp.Expr, t: sp.Symbol, endpoint: sp.Expr, *, context: str) -> None:
    c1 = assert_valid_symbolic_value(
        sp.limit((t - endpoint) * prefactor, t, endpoint),
        context=context,
        quantity="first Laurent coefficient",
    )
    c2 = assert_valid_symbolic_value(
        sp.limit((t - endpoint) ** 2 * prefactor, t, endpoint),
        context=context,
        quantity="second Laurent coefficient",
    )

    assert c1 != 0, f"{context}: expected non-zero first Laurent coefficient, got {c1}"
    assert c2 == 0, f"{context}: expected simple pole, second coefficient was {c2}"


def test_m1_vertex_endpoint_residues_orientation_free_are_pm_one():
    """Axiom IDs: TA-LP, TA-RR. Test type: structural."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(M1_PENTAGON_FIXTURE.vertices)

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t = res.t
            ts, te = interval_endpoints_from_chart_ccw(region, facet_name, chart, verts_ccw)

            start_context = f"{facet_name}/{chart.name}:start@{ts}"
            end_context = f"{facet_name}/{chart.name}:end@{te}"

            _assert_simple_pole(res.prefactor, t, ts, context=start_context)
            _assert_simple_pole(res.prefactor, t, te, context=end_context)

            start = _endpoint_residue(
                res.prefactor, t, ts, orientation_sign=1, context=start_context
            )
            end = _endpoint_residue(
                res.prefactor, t, te, orientation_sign=1, context=end_context
            )

            assert start in {sp.Integer(1), sp.Integer(-1)}, (
                f"{facet_name}/{chart.name} start endpoint residue not in ±1: {start}"
            )
            assert end in {sp.Integer(1), sp.Integer(-1)}, (
                f"{facet_name}/{chart.name} end endpoint residue not in ±1: {end}"
            )


def test_m1_vertex_endpoint_residues_ccw_fixed_are_plus_one():
    """Axiom IDs: TA-RR. Test type: failure-mode."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(M1_PENTAGON_FIXTURE.vertices)

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t = res.t
            ts, te = interval_endpoints_from_chart_ccw(region, facet_name, chart, verts_ccw)

            # Endpoint-local CCW coordinates: w_start = ts - t, w_end = t - te.
            start_context = f"{facet_name}/{chart.name}:ccw-start@{ts}"
            end_context = f"{facet_name}/{chart.name}:ccw-end@{te}"

            r_start_ccw = _endpoint_residue(
                res.prefactor, t, ts, orientation_sign=-1, context=start_context
            )
            r_end_ccw = _endpoint_residue(
                res.prefactor, t, te, orientation_sign=1, context=end_context
            )

            assert sp.simplify(r_start_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW start residue != +1: {r_start_ccw}"
            )
            assert sp.simplify(r_end_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW end residue != +1: {r_end_ccw}"
            )


def test_m1_terminal_residue_chains_2d_to_vertex_are_pm_one():
    """Axiom IDs: TA-RR. Test type: structural."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(M1_PENTAGON_FIXTURE.vertices)

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            residue_on_facet = residue_2form_on_facet(omega2, chart).simplify()
            t = residue_on_facet.t
            ts, te = interval_endpoints_from_chart_ccw(region, facet_name, chart, verts_ccw)

            start_context = f"{facet_name}/{chart.name}:chain-start@{ts}"
            end_context = f"{facet_name}/{chart.name}:chain-end@{te}"

            chain_start = _endpoint_residue(
                residue_on_facet.prefactor, t, ts, orientation_sign=1, context=start_context
            )
            chain_end = _endpoint_residue(
                residue_on_facet.prefactor, t, te, orientation_sign=1, context=end_context
            )

            assert sp.simplify(chain_start**2 - 1) == 0, (
                f"{facet_name}/{chart.name} chain-to-start residue not ±1: {chain_start}"
            )
            assert sp.simplify(chain_end**2 - 1) == 0, (
                f"{facet_name}/{chart.name} chain-to-end residue not ±1: {chain_end}"
            )
