# posgeo/forms/residues2d.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple, List, Dict

import sympy as sp

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
    u, t = chart.u, chart.t

    f_ut = sp.simplify(form.prefactor.subs({x: chart.x_of, y: chart.y_of}))
    g = sp.simplify(chart.s * sp.limit(u * f_ut, u, 0))
    return Canonical1Form(t, sp.simplify(g))


def pullback_1form(form: Canonical1Form, t_new: sp.Symbol, t_old_expr: sp.Expr) -> Canonical1Form:
    """
    Pull back omega = g(t_old) d(t_old) under t_old = t_old_expr(t_new):
      omega = g(t_old_expr) * d(t_old_expr)/d(t_new) dt_new
    """
    g_new = sp.simplify(form.prefactor.subs({form.t: t_old_expr}) * sp.diff(t_old_expr, t_new))
    return Canonical1Form(t_new, sp.simplify(g_new))


def m1_facet_charts_all(x: sp.Symbol, y: sp.Symbol) -> Dict[str, List[FacetChart]]:
    """
    Provide multiple charts per facet for chart-independence testing.

    IMPORTANT: each chart must have its own (u,t) symbols, otherwise SymPy will
    conflate parameters across charts.
    """
    def ut(name: str) -> tuple[sp.Symbol, sp.Symbol]:
        u = sp.Symbol(f"u__{name}", real=True)
        t = sp.Symbol(f"t__{name}", real=True)
        return u, t

    charts: Dict[str, List[FacetChart]] = {}

    # L1: x=0
    u0, t0 = ut("L1_x__t=y")
    u1, t1 = ut("L1_x__t=1-y")
    charts["L1_x"] = [
        FacetChart(name="L1_x__t=y", u=u0, t=t0, x_of=u0, y_of=t0, s=sp.Integer(1)),
        FacetChart(name="L1_x__t=1-y", u=u1, t=t1, x_of=u1, y_of=1 - t1, s=sp.Integer(-1)),
    ]

    # L2: y=0
    u0, t0 = ut("L2_y__t=x")
    u1, t1 = ut("L2_y__t=1-x")
    charts["L2_y"] = [
        FacetChart(name="L2_y__t=x", u=u0, t=t0, x_of=t0, y_of=u0, s=sp.Integer(-1)),
        FacetChart(name="L2_y__t=1-x", u=u1, t=t1, x_of=1 - t1, y_of=u1, s=sp.Integer(1)),
    ]

    # L3: x=1
    u0, t0 = ut("L3_1mx__t=y")
    u1, t1 = ut("L3_1mx__t=1-y")
    charts["L3_1mx"] = [
        FacetChart(name="L3_1mx__t=y", u=u0, t=t0, x_of=1 - u0, y_of=t0, s=sp.Integer(-1)),
        FacetChart(name="L3_1mx__t=1-y", u=u1, t=t1, x_of=1 - u1, y_of=1 - t1, s=sp.Integer(1)),
    ]

    # L4: y=1
    u0, t0 = ut("L4_1my__t=x")
    u1, t1 = ut("L4_1my__t=1-x")
    charts["L4_1my"] = [
        FacetChart(name="L4_1my__t=x", u=u0, t=t0, x_of=t0, y_of=1 - u0, s=sp.Integer(1)),
        FacetChart(name="L4_1my__t=1-x", u=u1, t=t1, x_of=1 - t1, y_of=1 - u1, s=sp.Integer(-1)),
    ]

    # L5: x+y=1/2
    u0, t0 = ut("L5__t=x")
    u1, t1 = ut("L5__t=y")
    charts["L5_xpy_mhalf"] = [
        FacetChart(
            name="L5__t=x",
            u=u0,
            t=t0,
            x_of=t0,
            y_of=sp.Rational(1, 2) - t0 + u0,
            s=sp.Integer(-1),
        ),
        FacetChart(
            name="L5__t=y",
            u=u1,
            t=t1,
            x_of=sp.Rational(1, 2) - t1 + u1,
            y_of=t1,
            s=sp.Integer(1),
        ),
    ]

    assert isinstance(charts, dict)
    return charts
    
def expected_interval_prefactor_for_m1_facet(facet_name: str, t: sp.Symbol) -> sp.Expr:
    """
    Expected canonical 1-form on each boundary segment (interval) in parameter t.
    Interval (a,b): prefactor = 1/(t-a) + 1/(b-t)
    """
    if facet_name == "L1_x":  # x=0, y in [1/2,1]
        a, b = sp.Rational(1, 2), sp.Rational(1)
    elif facet_name == "L2_y":  # y=0, x in [1/2,1]
        a, b = sp.Rational(1, 2), sp.Rational(1)
    elif facet_name == "L3_1mx":  # x=1, y in [0,1]
        a, b = sp.Rational(0), sp.Rational(1)
    elif facet_name == "L4_1my":  # y=1, x in [0,1]
        a, b = sp.Rational(0), sp.Rational(1)
    elif facet_name == "L5_xpy_mhalf":  # x+y=1/2, x in [0,1/2] (equivalently y in [0,1/2])
        a, b = sp.Rational(0), sp.Rational(1, 2)
    else:
        raise KeyError(f"Unknown facet: {facet_name}")

    return sp.simplify(1 / (t - a) + 1 / (b - t))
    
def interval_endpoints_from_chart(
    facet_name: str,
    chart: FacetChart,
    vertices: list[tuple[sp.Rational, sp.Rational]],
) -> tuple[sp.Rational, sp.Rational]:
    """
    Determine the interval endpoints in the chart parameter t by evaluating t at the
    two polygon vertices that lie on the given facet (u=0 boundary).

    We identify facet membership by checking the facet equation == 0 at the vertex.
    For M1 facets, we can infer the facet equation from the chart by eliminating u:
      on facet: u=0, so the facet is defined by the condition chart.u == 0 in that chart.
    But we already know which facet, so use the original M1 facet definitions implicitly
    via the known five equations.
    """
    x, y = chart.x_of.free_symbols, chart.y_of.free_symbols  # not used
    # We'll just hardcode the M1 facet equations here (for M1 only):
    X, Y = sp.symbols("x y", real=True)

    facet_eqs = {
        "L1_x": X,
        "L2_y": Y,
        "L3_1mx": 1 - X,
        "L4_1my": 1 - Y,
        "L5_xpy_mhalf": X + Y - sp.Rational(1, 2),
    }
    if facet_name not in facet_eqs:
        raise KeyError(f"Unknown facet: {facet_name}")

    eq = sp.simplify(facet_eqs[facet_name])

    on_facet = []
    for (vx, vy) in vertices:
        if sp.simplify(eq.subs({X: vx, Y: vy})) == 0:
            on_facet.append((vx, vy))

    if len(on_facet) != 2:
        raise ValueError(f"Expected 2 vertices on facet {facet_name}, got {len(on_facet)}: {on_facet}")

    # Evaluate chart.t at those vertices, using u=0 chart inversion:
    # We need t for each vertex. For our M1 charts, x_of(u,t), y_of(u,t) are simple enough
    # that we can solve for t by substituting u=0 and matching either x or y.
    u = chart.u
    t = chart.t

    x0 = sp.simplify(chart.x_of.subs({u: 0}))
    y0 = sp.simplify(chart.y_of.subs({u: 0}))

    tvals = []
    for (vx, vy) in on_facet:
        sol = sp.solve(sp.Eq(x0, vx), t, dict=True)
        if not sol:
            sol = sp.solve(sp.Eq(y0, vy), t, dict=True)
        if not sol:
            raise ValueError(f"Could not solve for t on facet {facet_name} at vertex {(vx,vy)} in chart {chart.name}")
        tvals.append(sp.simplify(sol[0][t]))

    a, b = tvals[0], tvals[1]
    return (sp.Min(a, b), sp.Max(a, b))
    
def expected_interval_prefactor_from_chart(
    facet_name: str,
    chart: FacetChart,
    vertices: list[tuple[sp.Rational, sp.Rational]],
) -> sp.Expr:
    a, b = interval_endpoints_from_chart(facet_name, chart, vertices)
    t = chart.t
    return sp.simplify(1/(t - a) + 1/(b - t))
    

# --- M1 facet equations (for identifying which vertices lie on which facet) ---
def _m1_facet_eqs(X: sp.Symbol, Y: sp.Symbol) -> Dict[str, sp.Expr]:
    return {
        "L1_x": X,
        "L2_y": Y,
        "L3_1mx": 1 - X,
        "L4_1my": 1 - Y,
        "L5_xpy_mhalf": X + Y - sp.Rational(1, 2),
    }


def _vertices_on_facet_m1(
    facet_name: str,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> List[Tuple[sp.Rational, sp.Rational]]:
    X, Y = sp.symbols("x y", real=True)
    eqs = _m1_facet_eqs(X, Y)
    if facet_name not in eqs:
        raise KeyError(f"Unknown facet: {facet_name}")
    eq = sp.simplify(eqs[facet_name])

    on = []
    for vx, vy in verts_ccw:
        if sp.simplify(eq.subs({X: vx, Y: vy})) == 0:
            on.append((vx, vy))
    return on


def _oriented_edge_vertices_ccw(
    facet_name: str,
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[Tuple[sp.Rational, sp.Rational], Tuple[sp.Rational, sp.Rational]]:
    """
    Return (v_start, v_end) as the CCW-oriented boundary edge lying on this facet.
    """
    on = _vertices_on_facet_m1(facet_name, verts_ccw)
    if len(on) != 2:
        raise ValueError(f"Expected 2 vertices on facet {facet_name}, got {len(on)}: {on}")

    vA, vB = on
    idx = {v: i for i, v in enumerate(verts_ccw)}
    if vA not in idx or vB not in idx:
        raise ValueError(f"Facet vertices not found in verts_ccw list: {on}")

    iA, iB = idx[vA], idx[vB]
    n = len(verts_ccw)

    # If vB is the next vertex after vA, the CCW edge is vA -> vB
    if (iA + 1) % n == iB:
        return vA, vB
    # If vA is the next vertex after vB, CCW edge is vB -> vA
    if (iB + 1) % n == iA:
        return vB, vA

    raise ValueError(
        f"Facet {facet_name} vertices are not adjacent in CCW order: {vA} (i={iA}), {vB} (i={iB})"
    )


def _solve_chart_t_at_vertex(chart: "FacetChart", vx: sp.Rational, vy: sp.Rational) -> sp.Expr:
    """
    Solve for chart.t at the boundary point (vx, vy) on u=0.
    We use x(u=0,t) and y(u=0,t) and solve for t.
    """
    u = chart.u
    t = chart.t

    x0 = sp.simplify(chart.x_of.subs({u: 0}))
    y0 = sp.simplify(chart.y_of.subs({u: 0}))

    # Try x equation first if it contains t; otherwise y equation.
    candidates = []
    if t in (x0 - vx).free_symbols:
        candidates.extend(sp.solve(sp.Eq(x0, vx), t))
    if t in (y0 - vy).free_symbols:
        candidates.extend(sp.solve(sp.Eq(y0, vy), t))

    # Filter candidates that satisfy BOTH x and y
    good = []
    for cand in candidates:
        cand = sp.simplify(cand)
        if sp.simplify(x0.subs({t: cand}) - vx) == 0 and sp.simplify(y0.subs({t: cand}) - vy) == 0:
            good.append(cand)

    if not good:
        raise ValueError(
            f"Could not solve t at vertex {(vx, vy)} for chart {chart.name}. "
            f"x0={x0}, y0={y0}"
        )

    # Prefer simplest
    good = sorted(good, key=lambda e: sp.count_ops(e))
    return sp.simplify(good[0])


def interval_endpoints_from_chart_ccw(
    facet_name: str,
    chart: "FacetChart",
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
) -> Tuple[sp.Expr, sp.Expr]:
    """
    Return (t_start, t_end) for the CCW-oriented boundary edge on this facet,
    expressed in the chart's parameter t (on u=0).
    """
    v_start, v_end = _oriented_edge_vertices_ccw(facet_name, verts_ccw)
    ts = _solve_chart_t_at_vertex(chart, *v_start)
    te = _solve_chart_t_at_vertex(chart, *v_end)
    return sp.simplify(ts), sp.simplify(te)
    
def _point_inside_region(region, px, py) -> bool:
    subs = {region.x: px, region.y: py}
    for f in region.facets.values():
        if sp.N(f.expr.subs(subs)) < -1e-12:
            return False
    return True


def _chart_u_points_outward(region, chart: FacetChart, facet_name: str, verts_ccw):
    """
    Decide if +u points outward by sampling a boundary point and stepping in +u.
    Returns +1 if outward, -1 if inward (needs sign flip).
    """
    # take CCW-oriented edge endpoints, then midpoint
    v_start, v_end = _oriented_edge_vertices_ccw(facet_name, verts_ccw)
    mx = (v_start[0] + v_end[0]) / 2
    my = (v_start[1] + v_end[1]) / 2

    # solve t at midpoint on u=0
    t_mid = _solve_chart_t_at_vertex(chart, mx, my)

    # step a little in +u
    eps = sp.Rational(1, 1000)
    x_eps = sp.simplify(chart.x_of.subs({chart.u: eps, chart.t: t_mid}))
    y_eps = sp.simplify(chart.y_of.subs({chart.u: eps, chart.t: t_mid}))

    inside = _point_inside_region(region, x_eps, y_eps)
    # if +u leads inside, then +u is inward, so outward sign is -1
    return sp.Integer(-1) if inside else sp.Integer(1)


def expected_interval_prefactor_from_chart_ccw(
    facet_name: str,
    chart: "FacetChart",
    verts_ccw: List[Tuple[sp.Rational, sp.Rational]],
    *,
    region=None,
) -> sp.Expr:
    """
    CCW-oriented expected interval prefactor. If region is provided, additionally
    correct for whether +u is inward or outward for this chart.
    """
    a, b = interval_endpoints_from_chart_ccw(facet_name, chart, verts_ccw)
    t = chart.t
    base = sp.simplify(1 / (t - a) + 1 / (b - t))

    if region is None:
        return base

    # correct sign if chart normal points inward
    s_norm = _chart_u_points_outward(region, chart, facet_name, verts_ccw)
    return sp.simplify(s_norm * base)
