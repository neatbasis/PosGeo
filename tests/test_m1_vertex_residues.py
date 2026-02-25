# Axioms: TA-RR, TA-VN

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


def _assert_valid_scalar(label: str, value: sp.Expr) -> None:
    simplified = sp.simplify(value)
    assert simplified not in {sp.nan, sp.zoo, sp.oo, -sp.oo}, (
        f"{label} produced an invalid symbolic value: {simplified}"
    )


def _endpoint_residue(prefactor: sp.Expr, t: sp.Symbol, endpoint: sp.Expr, *, orientation_sign: int) -> sp.Expr:
    residue = sp.simplify(sp.limit(orientation_sign * (t - endpoint) * prefactor, t, endpoint))
    _assert_valid_scalar("endpoint residue", residue)
    return residue


def _assert_simple_pole(prefactor: sp.Expr, t: sp.Symbol, endpoint: sp.Expr) -> None:
    c1 = sp.simplify(sp.limit((t - endpoint) * prefactor, t, endpoint))
    c2 = sp.simplify(sp.limit((t - endpoint) ** 2 * prefactor, t, endpoint))

    _assert_valid_scalar("first Laurent coefficient", c1)
    _assert_valid_scalar("second Laurent coefficient", c2)

    assert c1 != 0, f"Expected non-zero first Laurent coefficient at endpoint {endpoint}, got {c1}"
    assert c2 == 0, f"Expected simple pole at endpoint {endpoint}, second coefficient was {c2}"


def test_m1_vertex_endpoint_residues_orientation_free_are_pm_one():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(m1_pentagon_vertices())

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t = res.t
            ts, te = interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw)

            _assert_simple_pole(res.prefactor, t, ts)
            _assert_simple_pole(res.prefactor, t, te)

            start = _endpoint_residue(res.prefactor, t, ts, orientation_sign=1)
            end = _endpoint_residue(res.prefactor, t, te, orientation_sign=1)

            assert start in {sp.Integer(1), sp.Integer(-1)}, (
                f"{facet_name}/{chart.name} start endpoint residue not in ±1: {start}"
            )
            assert end in {sp.Integer(1), sp.Integer(-1)}, (
                f"{facet_name}/{chart.name} end endpoint residue not in ±1: {end}"
            )


def test_m1_vertex_endpoint_residues_ccw_fixed_are_plus_one():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(m1_pentagon_vertices())

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            res = residue_2form_on_facet(omega2, chart).simplify()
            t = res.t
            ts, te = interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw)

            # Endpoint-local CCW coordinates: w_start = ts - t, w_end = t - te.
            r_start_ccw = _endpoint_residue(res.prefactor, t, ts, orientation_sign=-1)
            r_end_ccw = _endpoint_residue(res.prefactor, t, te, orientation_sign=1)

            assert sp.simplify(r_start_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW start residue != +1: {r_start_ccw}"
            )
            assert sp.simplify(r_end_ccw - 1) == 0, (
                f"{facet_name}/{chart.name} CCW end residue != +1: {r_end_ccw}"
            )


def test_m1_terminal_residue_chains_2d_to_vertex_are_pm_one():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    verts_ccw = list(m1_pentagon_vertices())

    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    for facet_name, charts in m1_facet_charts_all(x, y).items():
        for chart in charts:
            residue_on_facet = residue_2form_on_facet(omega2, chart).simplify()
            t = residue_on_facet.t
            ts, te = interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw)

            chain_start = _endpoint_residue(residue_on_facet.prefactor, t, ts, orientation_sign=1)
            chain_end = _endpoint_residue(residue_on_facet.prefactor, t, te, orientation_sign=1)

            assert sp.simplify(chain_start**2 - 1) == 0, (
                f"{facet_name}/{chart.name} chain-to-start residue not ±1: {chain_start}"
            )
            assert sp.simplify(chain_end**2 - 1) == 0, (
                f"{facet_name}/{chart.name} chain-to-end residue not ±1: {chain_end}"
            )
