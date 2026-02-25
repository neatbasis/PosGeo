# Axioms: TA-RR, TA-VN

# tests/test_m1_residues_chart_independence.py

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    m1_pentagon_vertices,
)
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
    pullback_1form,
    expected_interval_prefactor_from_chart,
    expected_interval_prefactor_from_chart_ccw,
)


def _equal_up_to_sign(a: sp.Expr, b: sp.Expr) -> bool:
    return sp.simplify(a - b) == 0 or sp.simplify(a + b) == 0




def _solve_reparam_t1_of_t0(ch0, ch) -> sp.Expr:
    """
    Solve for t1 = t1(t0) on u=0 by equating boundary parameterizations.
    Assumes each chart has distinct symbols (your current implementation does).
    """
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

    # Fallback: solve full system
    sol = sp.solve([sp.Eq(x1, x0), sp.Eq(y1, y0)], t1, dict=True)
    for s in sol:
        cand = sp.simplify(s[t1])
        if t0 in cand.free_symbols:
            return cand
    if sol:
        return sp.simplify(sol[0][t1])

    raise AssertionError("Could not solve a valid reparameterization t1(t0).")


def test_residue_chart_independence_deterministic_sign():
    """TA-RR+O2: CCW-oriented residues are exact (no ±) and chart-independent after pullback."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    verts = list(m1_pentagon_vertices())

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet}"

        ch0 = charts[0]
        res0 = residue_2form_on_facet(omega2, ch0).simplify()
        exp0 = expected_interval_prefactor_from_chart_ccw(facet, ch0, verts, region=region)

        assert sp.simplify(res0.prefactor - exp0) == 0, (
            f"[{facet}] residue in {ch0.name} does not match CCW-expected interval form.\n"
            f"res={res0.prefactor}\nexp={exp0}\n"
            f"diff={sp.simplify(res0.prefactor - exp0)}"
        )

        for ch in charts[1:]:
            res = residue_2form_on_facet(omega2, ch).simplify()
            exp = expected_interval_prefactor_from_chart_ccw(facet, ch, verts, region=region)

            assert sp.simplify(res.prefactor - exp) == 0, (
                f"[{facet}] residue in {ch.name} does not match CCW-expected interval form.\n"
                f"res={res.prefactor}\nexp={exp}\n"
                f"diff={sp.simplify(res.prefactor - exp)}"
            )

            # Pullback compare
            t0 = ch0.t
            t1_of_t0 = _solve_reparam_t1_of_t0(ch0, ch)
            res_pulled = pullback_1form(res, t_new=t0, t_old_expr=t1_of_t0).simplify()

            assert sp.simplify(res_pulled.prefactor - res0.prefactor) == 0, (
                f"[{facet}] deterministic chart-independence failed between {ch0.name} and {ch.name}\n"
                f"res0(t0)={res0.prefactor}\n"
                f"res1(t1)={res.prefactor}\n"
                f"t1(t0)={t1_of_t0}\n"
                f"pulled={res_pulled.prefactor}\n"
                f"diff={sp.simplify(res_pulled.prefactor - res0.prefactor)}"
            )


def test_residue_chart_independence_up_to_pullback_and_sign():
    """
    TA-RR (structural): orientation-agnostic residue relation, checked chart-by-chart.

    For each facet, we provide >=2 coordinate charts (u,t) with the facet at u=0.
    We compute the residue 1-form in each chart and verify:

      1) In each chart, the residue equals the canonical 1-form of the boundary interval,
         with endpoints derived from the chart + polygon vertices (chart-aware oracle),
         up to an overall sign (orientation).
      2) Residues computed in different charts agree after pullback along the boundary
         reparameterization t1 = t1(t0), again up to an overall sign.
    """
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega2 = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    verts = list(m1_pentagon_vertices())

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2, f"Need >=2 charts for {facet}"

        ch0 = charts[0]
        res0 = residue_2form_on_facet(omega2, ch0).simplify()

        exp0 = expected_interval_prefactor_from_chart(facet, ch0, verts)
        assert _equal_up_to_sign(res0.prefactor, exp0), (
            f"[{facet}] residue in {ch0.name} does not match expected interval form.\n"
            f"res={res0.prefactor}\nexp={exp0}\n"
            f"diff={sp.simplify(res0.prefactor - exp0)}\n"
            f"diff(signflip)={sp.simplify(res0.prefactor + exp0)}"
        )

        for ch in charts[1:]:
            res = residue_2form_on_facet(omega2, ch).simplify()

            exp = expected_interval_prefactor_from_chart(facet, ch, verts)
            assert _equal_up_to_sign(res.prefactor, exp), (
                f"[{facet}] residue in {ch.name} does not match expected interval form.\n"
                f"res={res.prefactor}\nexp={exp}\n"
                f"diff={sp.simplify(res.prefactor - exp)}\n"
                f"diff(signflip)={sp.simplify(res.prefactor + exp)}"
            )

            t0 = ch0.t
            t1_of_t0 = _solve_reparam_t1_of_t0(ch0, ch)

            res_pulled = pullback_1form(res, t_new=t0, t_old_expr=t1_of_t0).simplify()

            assert _equal_up_to_sign(res_pulled.prefactor, res0.prefactor), (
                f"[{facet}] chart-independence failed between {ch0.name} and {ch.name}\n"
                f"res0(t0)={res0.prefactor}\n"
                f"res1(t1)={res.prefactor}\n"
                f"t1(t0)={t1_of_t0}\n"
                f"pulled={res_pulled.prefactor}\n"
                f"diff={sp.simplify(res_pulled.prefactor - res0.prefactor)}\n"
                f"diff(signflip)={sp.simplify(res_pulled.prefactor + res0.prefactor)}"
            )
