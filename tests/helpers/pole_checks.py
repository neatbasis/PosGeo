import math

import sympy as sp


def normalize_linear_factor(expr: sp.Expr, *vars: sp.Symbol) -> sp.Expr:
    """Normalize a linear factor up to overall nonzero rational scale."""
    if not vars:
        raise ValueError("At least one variable symbol is required.")

    poly = sp.Poly(sp.factor(expr), *vars, domain="QQ")

    coeffs = [sp.Rational(poly.coeff_monomial(v)) for v in vars]
    constant = sp.Rational(poly.coeff_monomial(1))

    denoms = [sp.denom(c) for c in (*coeffs, constant)]
    lcm = sp.ilcm(*[int(d) for d in denoms if d != 0] or [1])

    ints = [int(c * lcm) for c in (*coeffs, constant)]

    g = 0
    for value in ints:
        g = math.gcd(g, abs(value))

    if g == 0:
        return sp.Integer(0)

    ints = [value // g for value in ints]

    for value in ints:
        if value != 0:
            if value < 0:
                ints = [-val for val in ints]
            break

    linear = sum(sp.Rational(ai) * v for ai, v in zip(ints[:-1], vars)) + sp.Rational(ints[-1])
    return sp.factor(linear)


def normalized_denominator_factors(prefactor: sp.Expr, *vars: sp.Symbol):
    """Return normalized (factor, multiplicity) pairs from denominator factorization."""
    denom = sp.factor(sp.denom(prefactor))
    factors = sp.factor_list(denom)[1]
    return [(normalize_linear_factor(factor, *vars), multiplicity) for factor, multiplicity in factors]


def assert_multiplicity_one(factors_with_multiplicity):
    for factor, multiplicity in factors_with_multiplicity:
        assert multiplicity == 1, f"Non-simple pole multiplicity for {factor}: {multiplicity}"


def assert_boundary_subset(factors_with_multiplicity, boundary_exprs, *vars: sp.Symbol):
    boundary_factors = {normalize_linear_factor(expr, *vars) for expr in boundary_exprs}
    factor_set = {factor for factor, _ in factors_with_multiplicity}
    assert factor_set.issubset(boundary_factors), (
        f"Found non-boundary pole factors: {factor_set - boundary_factors}"
    )


def assert_no_spurious_locus(form_prefactor: sp.Expr, locus_expr: sp.Expr, *vars: sp.Symbol):
    """
    Assert no denominator factor is proportional to ``locus_expr``.

    This is useful for quickly probing that a known internal/cancellation locus
    does not survive in the final prefactor.
    """
    normalized_locus = normalize_linear_factor(locus_expr, *vars)
    factors = normalized_denominator_factors(form_prefactor, *vars)
    den_factors = {factor for factor, _ in factors}
    assert normalized_locus not in den_factors, (
        f"Spurious pole locus survived in denominator: {locus_expr}"
    )
