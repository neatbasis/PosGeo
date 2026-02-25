import sympy as sp

from posgeo.validation.singularity_gate import (
    normalize_linear_factor,
    normalized_denominator_factors,
)


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
    normalized_locus = normalize_linear_factor(locus_expr, *vars)
    factors = normalized_denominator_factors(form_prefactor, *vars)
    den_factors = {factor for factor, _ in factors}
    assert normalized_locus not in den_factors, (
        f"Spurious pole locus survived in denominator: {locus_expr}"
    )


def assert_boundary_pole_invariant(
    prefactor: sp.Expr,
    boundary_exprs,
    *vars: sp.Symbol,
    require_simple_poles: bool = True,
    internal_locus_exprs=None,
):
    factors = normalized_denominator_factors(prefactor, *vars)
    assert_boundary_subset(factors, boundary_exprs, *vars)

    if require_simple_poles:
        assert_multiplicity_one(factors)

    if internal_locus_exprs:
        den_factors = {factor for factor, _ in factors}
        for locus_expr in internal_locus_exprs:
            normalized_locus = normalize_linear_factor(locus_expr, *vars)
            assert normalized_locus not in den_factors, (
                f"Spurious pole locus survived in denominator: {locus_expr}"
            )

    return factors
