# tests/test_reparam_nonconstant.py
import sympy as sp

from posgeo.forms.residues2d import m1_facet_charts_all
from tests.helpers.orientation_consistency import solve_reparam_t1_of_t0


def test_reparam_is_not_constant_for_all_m1_chart_pairs():
    """Axiom IDs: TA-E3. Test type: failure-mode."""
    x, y = sp.symbols("x y", real=True)
    charts_by_facet = m1_facet_charts_all(x, y)

    for facet, charts in charts_by_facet.items():
        assert len(charts) >= 2
        ch0 = charts[0]
        t0 = ch0.t

        for ch in charts[1:]:
            t1_of_t0 = solve_reparam_t1_of_t0(ch0, ch)

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
