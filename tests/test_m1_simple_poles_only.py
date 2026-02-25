import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from posgeo.forms.residues2d import m1_facet_charts_all


def _normalize_linear(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    """Normalize ax+by+c up to nonzero rational scale for exact set comparisons."""
    poly = sp.Poly(sp.factor(expr), x, y, domain="QQ")

    a = sp.Rational(poly.coeff_monomial(x))
    b = sp.Rational(poly.coeff_monomial(y))
    c = sp.Rational(poly.coeff_monomial(1))

    denoms = [sp.denom(a), sp.denom(b), sp.denom(c)]
    lcm = sp.ilcm(*[int(d) for d in denoms if d != 0] or [1])

    ai, bi, ci = int(a * lcm), int(b * lcm), int(c * lcm)

    import math

    g = 0
    for val in (ai, bi, ci):
        g = math.gcd(g, abs(val))

    if g == 0:
        return sp.Integer(0)

    ai //= g
    bi //= g
    ci //= g

    for val in (ai, bi, ci):
        if val != 0:
            if val < 0:
                ai, bi, ci = -ai, -bi, -ci
            break

    return sp.factor(sp.Rational(ai) * x + sp.Rational(bi) * y + sp.Rational(ci))


def test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits():
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    denom = sp.factor(sp.denom(omega.prefactor))

    factors = sp.factor_list(denom)[1]
    boundary_factors = {_normalize_linear(f.expr, x, y) for f in region.facets.values()}

    for fac, multiplicity in factors:
        normalized = _normalize_linear(fac, x, y)
        assert normalized in boundary_factors, f"Non-boundary pole factor found: {fac}"
        assert multiplicity == 1, f"Non-simple pole multiplicity for {fac}: {multiplicity}"

    for charts in m1_facet_charts_all(x, y).values():
        for chart in charts:
            f_ut = sp.simplify(omega.prefactor.subs({x: chart.x_of, y: chart.y_of}))

            lim1 = sp.simplify(sp.limit(chart.u * f_ut, chart.u, 0))
            lim2 = sp.simplify(sp.limit((chart.u**2) * f_ut, chart.u, 0))

            assert lim1 not in {sp.Integer(0), sp.oo, -sp.oo, sp.zoo, sp.nan}, (
                f"Expected finite nonzero first-order limit on {chart.name}, got {lim1}"
            )
            assert lim2 == 0, f"Expected second-order coefficient to vanish on {chart.name}, got {lim2}"
