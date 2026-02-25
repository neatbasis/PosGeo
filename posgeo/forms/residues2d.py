from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import sympy as sp

from posgeo.geometry.fixtures2d import M1_PENTAGON_FIXTURE, Q1_QUADRILATERAL_FIXTURE
from posgeo.geometry.region2d import Region2D
from posgeo.typing import Canonical1Form, Canonical2Form


@dataclass(frozen=True)
class FacetChart:
    """
    Chart for computing residues along a facet.
    Parametrize (x,y) = (x(u,t), y(u,t)) such that facet is u=0 and t is the boundary parameter.

    s encodes:
      dx ∧ dy = s * du ∧ dt
    so residue prefactor along u=0 is:
      g(t) = s * lim_{u->0} (u * f(x(u,t),y(u,t)))
    producing omega = g(t) dt
    """

    name: str
    u: sp.Symbol
    t: sp.Symbol
    x_of: sp.Expr
    y_of: sp.Expr
    s: sp.Integer  # +1 or -1


def residue_2form_on_facet(form: Canonical2Form, chart: FacetChart) -> Canonical1Form:
    x, y = form.x, form.y
    u = chart.u

    f_ut = sp.simplify(form.prefactor.subs({x: chart.x_of, y: chart.y_of}))
    g = sp.simplify(chart.s * sp.limit(u * f_ut, u, 0))
    return Canonical1Form(chart.t, sp.simplify(g))


def pullback_1form(form: Canonical1Form, t_new: sp.Symbol, t_old_expr: sp.Expr) -> Canonical1Form:
    """
    Pull back omega = g(t_old) d(t_old) under t_old = t_old_expr(t_new):
      omega = g(t_old_expr) * d(t_old_expr)/d(t_new) dt_new
    """
    g_new = sp.simplify(form.prefactor.subs({form.t: t_old_expr}) * sp.diff(t_old_expr, t_new))
    return Canonical1Form(t_new, sp.simplify(g_new))


def _make_facet_charts(
    defs: Dict[str, List[Tuple[str, sp.Expr, sp.Expr, int]]],
) -> Dict[str, List[FacetChart]]:
    """Build facet charts from `(name, x_of, y_of, s)` definitions."""

    def ut(name: str) -> Tuple[sp.Symbol, sp.Symbol]:
        return (
            sp.Symbol(f"u__{name}", real=True),
            sp.Symbol(f"t__{name}", real=True),
        )

    charts: Dict[str, List[FacetChart]] = {}
    for facet_name, facet_defs in defs.items():
        charts[facet_name] = []
        for chart_name, x_builder, y_builder, sign in facet_defs:
            u, t = ut(chart_name)
            charts[facet_name].append(
                FacetChart(
                    name=chart_name,
                    u=u,
                    t=t,
                    x_of=sp.simplify(x_builder.subs({sp.Symbol("u"): u, sp.Symbol("t"): t})),
                    y_of=sp.simplify(y_builder.subs({sp.Symbol("u"): u, sp.Symbol("t"): t})),
                    s=sp.Integer(sign),
                )
            )
    return charts


def _solve_chart_t_at_vertex(chart: FacetChart, vx: sp.Rational, vy: sp.Rational) -> sp.Expr:
    """Solve for chart.t at boundary point (vx, vy) on u=0."""
    u, t = chart.u, chart.t
    x0 = sp.simplify(chart.x_of.subs({u: 0}))
    y0 = sp.simplify(chart.y_of.subs({u: 0}))

    candidates: List[sp.Expr] = []
    if t in x0.free_symbols:
        candidates.extend(sp.solve(sp.Eq(x0, vx), t))
    if t in y0.free_symbols:
        candidates.extend(sp.solve(sp.Eq(y0, vy), t))

    good: List[sp.Expr] = []
    for cand in candidates:
        cand = sp.simplify(cand)
        if sp.simplify(x0.subs({t: cand}) - vx) == 0 and sp.simplify(y0.subs({t: cand}) - vy) == 0:
            good.append(cand)

    if not good:
        raise ValueError(
            f"Could not solve t at vertex {(vx, vy)} for chart {chart.name}. "
            f"x0={x0}, y0={y0}"
        )
    return sp.simplify(sorted(good, key=lambda e: sp.count_ops(e))[0])


def facet_vertices_from_region_equations(
    region: Region2D,
    facet_name: str,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> List[Tuple[sp.Rational, sp.Rational]]:
    """Identify polygon vertices lying on a named facet via region equations."""
    if facet_name not in region.facets:
        raise KeyError(f"Unknown facet: {facet_name}")

    eq = sp.simplify(region.facets[facet_name].expr)
    on = []
    for vx, vy in verts_ccw:
        if sp.simplify(eq.subs({region.x: vx, region.y: vy})) == 0:
            on.append((vx, vy))
    return on


def oriented_edge_vertices_ccw(
    region: Region2D,
    facet_name: str,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[Tuple[sp.Rational, sp.Rational], Tuple[sp.Rational, sp.Rational]]:
    """Return (v_start, v_end) as the CCW boundary edge lying on the named facet."""
    on = facet_vertices_from_region_equations(region, facet_name, verts_ccw)
    if len(on) != 2:
        raise ValueError(f"Expected 2 vertices on facet {facet_name}, got {len(on)}: {on}")

    v_a, v_b = on
    idx = {v: i for i, v in enumerate(verts_ccw)}
    i_a, i_b = idx[v_a], idx[v_b]
    n = len(verts_ccw)

    if (i_a + 1) % n == i_b:
        return v_a, v_b
    if (i_b + 1) % n == i_a:
        return v_b, v_a
    raise ValueError(f"Facet {facet_name} vertices are not adjacent in CCW order: {on}")


def interval_endpoints_from_chart(
    chart: FacetChart,
    facet_vertices: Iterable[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[sp.Expr, sp.Expr]:
    """Extract unordered endpoint pair `(min_t,max_t)` in chart coordinates for a facet."""
    tvals = [
        _solve_chart_t_at_vertex(chart, vx, vy)
        for vx, vy in facet_vertices
    ]
    if len(tvals) != 2:
        raise ValueError(f"Expected 2 facet vertices, got {len(tvals)}")
    a, b = tvals
    return sp.Min(a, b), sp.Max(a, b)


def _interval_endpoints_from_chart_ccw_impl(
    region: Region2D,
    facet_name: str,
    chart: FacetChart,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[sp.Expr, sp.Expr]:
    """Return `(t_start,t_end)` for the CCW-oriented edge on a facet."""
    v_start, v_end = oriented_edge_vertices_ccw(region, facet_name, verts_ccw)
    ts = _solve_chart_t_at_vertex(chart, *v_start)
    te = _solve_chart_t_at_vertex(chart, *v_end)
    return sp.simplify(ts), sp.simplify(te)


def _point_inside_region(region: Region2D, px: sp.Expr, py: sp.Expr) -> bool:
    subs = {region.x: px, region.y: py}
    for f in region.facets.values():
        val = sp.simplify(f.expr.subs(subs))
        if val.is_negative is True:
            return False
        if (val.is_Rational is True or val.is_Integer is True) and val < 0:
            return False
    return True


def _chart_u_points_outward(
    region: Region2D,
    chart: FacetChart,
    facet_name: str,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> sp.Integer:
    v_start, v_end = oriented_edge_vertices_ccw(region, facet_name, verts_ccw)
    mx = (v_start[0] + v_end[0]) / 2
    my = (v_start[1] + v_end[1]) / 2
    t_mid = _solve_chart_t_at_vertex(chart, mx, my)

    eps = sp.Rational(1, 1000)
    x_eps = sp.simplify(chart.x_of.subs({chart.u: eps, chart.t: t_mid}))
    y_eps = sp.simplify(chart.y_of.subs({chart.u: eps, chart.t: t_mid}))

    inside = _point_inside_region(region, x_eps, y_eps)
    return sp.Integer(-1) if inside else sp.Integer(1)


def expected_interval_1form_prefactor(
    chart: FacetChart,
    *,
    endpoint_pair: Tuple[sp.Expr, sp.Expr],
    orientation_sign: sp.Expr = sp.Integer(1),
) -> sp.Expr:
    """Build expected interval 1-form prefactor with optional orientation sign."""
    a, b = endpoint_pair
    return sp.simplify(orientation_sign * (1 / (chart.t - a) + 1 / (b - chart.t)))


def expected_interval_prefactor_from_chart(
    region: Region2D,
    facet_name: str,
    chart: FacetChart,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> sp.Expr:
    on_facet = facet_vertices_from_region_equations(region, facet_name, verts_ccw)
    return expected_interval_1form_prefactor(
        chart,
        endpoint_pair=interval_endpoints_from_chart(chart, on_facet),
    )


def expected_interval_prefactor_from_chart_ccw(
    region: Region2D,
    facet_name: str,
    chart: FacetChart,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> sp.Expr:
    a, b = _interval_endpoints_from_chart_ccw_impl(region, facet_name, chart, verts_ccw)
    s_norm = _chart_u_points_outward(region, chart, facet_name, verts_ccw)
    return expected_interval_1form_prefactor(chart, endpoint_pair=(a, b), orientation_sign=s_norm)


# -- M1 adapters --
def m1_facet_charts_all(x: sp.Symbol, y: sp.Symbol) -> Dict[str, List[FacetChart]]:
    _ = (x, y)
    return _make_facet_charts({k: list(v) for k, v in M1_PENTAGON_FIXTURE.chart_defs.items()})


def q1_facet_charts_all(x: sp.Symbol, y: sp.Symbol) -> Dict[str, List[FacetChart]]:
    """Charts for the Q1 convex quadrilateral fixture."""
    _ = (x, y)
    return _make_facet_charts({k: list(v) for k, v in Q1_QUADRILATERAL_FIXTURE.chart_defs.items()})


# Backward-compatible M1 API adapters
def expected_interval_prefactor_for_m1_facet(facet_name: str, t: sp.Symbol) -> sp.Expr:
    from posgeo.geometry.region2d import PentagonM1Region

    region = PentagonM1Region.build()
    verts = list(M1_PENTAGON_FIXTURE.vertices)
    charts = m1_facet_charts_all(region.x, region.y)
    chart = charts[facet_name][0]
    exp = expected_interval_prefactor_from_chart(region, facet_name, chart, verts)
    return sp.simplify(exp.subs({chart.t: t}))


def interval_endpoints_from_chart_ccw(
    region: Region2D,
    facet_name: str,
    chart: FacetChart,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[sp.Expr, sp.Expr]:
    """Return `(t_start,t_end)` for the CCW-oriented edge on a facet."""
    return _interval_endpoints_from_chart_ccw_impl(region, facet_name, chart, verts_ccw)


def interval_endpoints_from_chart_ccw_compat(*args):
    """Compat shim preserving 4-arg calls and loudly rejecting deprecated 3-arg calls."""
    if len(args) == 4:
        return interval_endpoints_from_chart_ccw(*args)
    if len(args) == 3:
        raise TypeError(
            "Deprecated ambiguous call: interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw). "
            "Pass region explicitly: interval_endpoints_from_chart_ccw(region, facet_name, chart, verts_ccw)."
        )
    raise TypeError(
        "interval_endpoints_from_chart_ccw expects (region, facet_name, chart, verts_ccw)"
    )
