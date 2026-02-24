# tests/test_reparam_nonconstant.py
import sympy as sp

from posgeo.forms.residues2d import m1_facet_charts_all


def _solve_reparam_t1_of_t0(ch0, ch) -> sp.Expr:
    """
    Minimal reparam solver used ONLY for detecting degenerate constant maps.

    We solve on u=0:
      (x0(t0), y0(t0)) = (x1(t1), y1(t1))
    and expect a non-constant relation t1 = t1(t0).
    """
    t0 = ch0.t
    t1 = ch.t

    x0 = sp.simplify(ch0.x_of.subs({ch0.u: 0}))
    y0 = sp.simplify(ch0.y_of.subs({ch0.u: 0}))
    x1 = sp.simplify(ch.x_of.subs({ch.u: 0}))
    y1 = sp.simplify(ch.y_of.subs({ch.u: 0}))

    # Prefer equations that actually contain t1
    eqs = []
    if t1 in (x1 - x0).free_symbols:
        eqs.append(sp.Eq(x1, x0))
    if t1 in (y1 - y0).free_symbols:
        eqs.append(sp.Eq(y1, y0))

    sol = sp.solve(eqs, t1, dict=True) if eqs else []
    if not sol:
        sol = sp.solve([sp.Eq(x1, x0), sp.Eq(y1, y0)], t1, dict=True)

    assert sol, f"Could not solve reparam for {ch0.name} vs {ch.name}"
    return sp.simplify(sol[0][t1])


def test_reparam_is_not_constant_for_all_m1_chart_pairs():
    x, y = sp.symbols("x y", real=True)
    charts_by_facet = m1_facet_charts_all(x, y)

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2
        ch0 = charts[0]
        t0 = ch0.t

        for ch in charts[1:]:
            t1_of_t0 = _solve_reparam_t1_of_t0(ch0, ch)

            # This is the exact historical failure mode:
            # SymPy "solved" degenerate equations and returned a constant.
            assert t0 in t1_of_t0.free_symbols, (
                f"[{facet}] Reparameterization unexpectedly constant:\n"
                f"{ch0.name} -> {ch.name}\n"
                f"t1(t0) = {t1_of_t0}"
            )

            # and derivative must not vanish identically
            dt = sp.simplify(sp.diff(t1_of_t0, t0))
            assert dt != 0, (
                f"[{facet}] Reparameterization derivative vanished:\n"
                f"{ch0.name} -> {ch.name}\n"
                f"t1(t0) = {t1_of_t0}\n"
                f"dt1/dt0 = {dt}"
            )

