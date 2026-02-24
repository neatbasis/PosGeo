import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1


def _normalize_linear(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    """
    Normalize a linear expression a*x + b*y + c up to overall nonzero rational scaling.
    Returns a canonical representative so comparisons work even if SymPy multiplies by 2, etc.
    """
    expr = sp.factor(expr)
    poly = sp.Poly(expr, x, y, domain="QQ")

    a = sp.Rational(poly.coeff_monomial(x))
    b = sp.Rational(poly.coeff_monomial(y))
    c = sp.Rational(poly.coeff_monomial(1))

    # Clear denominators to integers
    denoms = [sp.denom(a), sp.denom(b), sp.denom(c)]
    lcm = sp.ilcm(*[int(d) for d in denoms if d != 0] or [1])

    ai = int(a * lcm)
    bi = int(b * lcm)
    ci = int(c * lcm)

    # gcd for integers
    import math
    g = 0
    for v in (ai, bi, ci):
        g = math.gcd(g, abs(v))
    if g == 0:
        return sp.Integer(0)

    ai //= g
    bi //= g
    ci //= g

    # Fix sign: first nonzero among (ai,bi,ci) should be positive
    for v in (ai, bi, ci):
        if v != 0:
            if v < 0:
                ai, bi, ci = -ai, -bi, -ci
            break

    return sp.factor(sp.Rational(ai) * x + sp.Rational(bi) * y + sp.Rational(ci))


def test_only_boundary_poles_in_final_form():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    denom = sp.factor(sp.denom(omega.prefactor))
    factors = sp.factor_list(denom)[1]
    denom_factors = { _normalize_linear(fac, x, y) for (fac, pow_) in factors }

    boundary_factors = { _normalize_linear(f.expr, x, y) for f in region.facets.values() }

    # Expect: final form has poles only on boundary lines (internal triangulation poles cancel)
    assert denom_factors.issubset(boundary_factors), (
        f"Found non-boundary pole factors: {denom_factors - boundary_factors}"
    )