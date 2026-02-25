from __future__ import annotations

import sympy as sp


def equal_up_to_sign(a: sp.Expr, b: sp.Expr) -> bool:
    return sp.simplify(a - b) == 0 or sp.simplify(a + b) == 0


def jacobian_det(chart) -> sp.Expr:
    return sp.simplify(
        sp.diff(chart.x_of, chart.u) * sp.diff(chart.y_of, chart.t)
        - sp.diff(chart.x_of, chart.t) * sp.diff(chart.y_of, chart.u)
    )


def solve_reparam_t1_of_t0(ch0, ch) -> sp.Expr:
    """Solve for t1 = t1(t0) on u=0 by equating boundary parameterizations."""
    t0 = ch0.t
    t1 = ch.t

    x0 = sp.simplify(ch0.x_of.subs({ch0.u: 0}))
    y0 = sp.simplify(ch0.y_of.subs({ch0.u: 0}))
    x1 = sp.simplify(ch.x_of.subs({ch.u: 0}))
    y1 = sp.simplify(ch.y_of.subs({ch.u: 0}))

    eqs = []
    if t1 in sp.simplify(x1 - x0).free_symbols:
        eqs.append(sp.Eq(x1, x0))
    if t1 in sp.simplify(y1 - y0).free_symbols:
        eqs.append(sp.Eq(y1, y0))

    sol = sp.solve(eqs, t1, dict=True) if eqs else []
    for s in sol:
        cand = sp.simplify(s[t1])
        if t0 in cand.free_symbols:
            return cand
    if sol:
        return sp.simplify(sol[0][t1])

    sol = sp.solve([sp.Eq(x1, x0), sp.Eq(y1, y0)], t1, dict=True)
    for s in sol:
        cand = sp.simplify(s[t1])
        if t0 in cand.free_symbols:
            return cand
    if sol:
        return sp.simplify(sol[0][t1])

    raise AssertionError(f"Could not solve a valid reparameterization t1(t0) for {ch0.name} vs {ch.name}.")
