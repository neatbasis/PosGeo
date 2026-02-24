import sympy as sp

from posgeo.forms.simplex2d import Triangle2D


def test_triangle_form_has_only_edge_poles():
    x, y = sp.symbols("x y", real=True)
    tri = Triangle2D.from_vertices(x, y, (sp.Rational(0), sp.Rational(0)),
                                   (sp.Rational(1), sp.Rational(0)),
                                   (sp.Rational(0), sp.Rational(1)))
    omega = tri.canonical_form()
    denom = sp.factor(sp.denom(omega.prefactor))

    # For the standard right triangle, edges are x=0, y=0, 1-x-y=0 (up to scaling).
    # We just check denominator factors are linear and correspond to some edge expressions.
    edge_exprs = [sp.factor(e.expr) for e in tri.edges]
    factors = sp.factor_list(denom)[1]
    for fac, power in factors:
        # Each factor should match (up to scaling) one of the edges.
        ok = any(sp.simplify(fac / ee) == 1 or sp.simplify(fac / ee) == -1 for ee in edge_exprs)
        assert ok, f"Unexpected denominator factor {fac}, edges={edge_exprs}"