from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence, Tuple

import sympy as sp

from posgeo.forms.residues2d import FacetChart
from posgeo.geometry.region2d import Region2D
from posgeo.typing import Canonical2Form


@dataclass(frozen=True)
class ChartOrderCheck:
    facet_name: str
    chart_name: str
    first_order_limit: sp.Expr
    second_order_limit: sp.Expr
    passed: bool
    failure_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class SingularityReport:
    detected_pole_loci: Tuple[sp.Expr, ...]
    multiplicities: Tuple[Tuple[sp.Expr, int], ...]
    boundary_mapping_status: bool
    local_chart_order_checks: Tuple[ChartOrderCheck, ...]
    failure_reasons: Tuple[str, ...]

    @property
    def passed(self) -> bool:
        return len(self.failure_reasons) == 0


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


def normalized_denominator_factors(prefactor: sp.Expr, *vars: sp.Symbol) -> Tuple[Tuple[sp.Expr, int], ...]:
    """Return normalized `(factor, multiplicity)` pairs from denominator factorization."""
    denom = sp.factor(sp.denom(prefactor))
    factors = sp.factor_list(denom)[1]
    return tuple((normalize_linear_factor(factor, *vars), multiplicity) for factor, multiplicity in factors)


def has_pole_locus(prefactor: sp.Expr, locus_expr: sp.Expr, *vars: sp.Symbol) -> bool:
    """Return whether `locus_expr` appears as a (normalized) denominator pole factor."""
    normalized_locus = normalize_linear_factor(locus_expr, *vars)
    factors = normalized_denominator_factors(prefactor, *vars)
    return normalized_locus in {factor for factor, _ in factors}


def assert_no_pole_locus(prefactor: sp.Expr, locus_expr: sp.Expr, *vars: sp.Symbol) -> None:
    """Assert that `locus_expr` does not survive as a denominator pole factor."""
    if has_pole_locus(prefactor, locus_expr, *vars):
        raise AssertionError(f"Spurious pole locus survived in denominator: {locus_expr}")


def _is_invalid_symbolic_value(expr: sp.Expr) -> bool:
    val = sp.simplify(expr)
    return bool(val.has(sp.nan) or val.has(sp.zoo) or val is sp.oo or val is -sp.oo)


def _check_chart_local_orders(
    prefactor: sp.Expr,
    x: sp.Symbol,
    y: sp.Symbol,
    charts: Mapping[str, Sequence[FacetChart]],
) -> Tuple[ChartOrderCheck, ...]:
    checks: list[ChartOrderCheck] = []
    for facet_name, facet_charts in charts.items():
        for chart in facet_charts:
            f_ut = sp.simplify(prefactor.subs({x: chart.x_of, y: chart.y_of}))
            lim1 = sp.simplify(sp.limit(chart.u * f_ut, chart.u, 0))
            lim2 = sp.simplify(sp.limit((chart.u**2) * f_ut, chart.u, 0))

            reasons: list[str] = []
            if _is_invalid_symbolic_value(lim1):
                reasons.append("chart-first-order-invalid")
            elif sp.simplify(lim1) == 0:
                reasons.append("chart-first-order-zero")

            if _is_invalid_symbolic_value(lim2):
                reasons.append("chart-second-order-invalid")
            elif sp.simplify(lim2) != 0:
                reasons.append("chart-second-order-nonzero")

            checks.append(
                ChartOrderCheck(
                    facet_name=facet_name,
                    chart_name=chart.name,
                    first_order_limit=lim1,
                    second_order_limit=lim2,
                    passed=len(reasons) == 0,
                    failure_reasons=tuple(reasons),
                )
            )

    return tuple(checks)


def singularity_report(
    form: Canonical2Form,
    region: Region2D,
    charts: Mapping[str, Sequence[FacetChart]],
) -> SingularityReport:
    factors = normalized_denominator_factors(form.prefactor, form.x, form.y)
    detected_loci = tuple(factor for factor, _ in factors)

    boundary_factors = {
        normalize_linear_factor(f.expr, form.x, form.y)
        for f in region.facets.values()
    }
    non_boundary = {factor for factor, _ in factors if factor not in boundary_factors}
    boundary_ok = len(non_boundary) == 0

    failure_reasons: list[str] = []
    if not boundary_ok:
        failure_reasons.append("non-boundary-pole")

    if any(multiplicity != 1 for _, multiplicity in factors):
        failure_reasons.append("non-simple-multiplicity")

    chart_checks = _check_chart_local_orders(form.prefactor, form.x, form.y, charts)
    if any(not check.passed for check in chart_checks):
        failure_reasons.append("chart-order-failed")

    return SingularityReport(
        detected_pole_loci=detected_loci,
        multiplicities=factors,
        boundary_mapping_status=boundary_ok,
        local_chart_order_checks=chart_checks,
        failure_reasons=tuple(failure_reasons),
    )


def assert_log_pure(
    form: Canonical2Form,
    region: Region2D,
    charts: Mapping[str, Sequence[FacetChart]],
) -> SingularityReport:
    report = singularity_report(form, region, charts)
    if report.passed:
        return report

    details = []
    for factor, multiplicity in report.multiplicities:
        if multiplicity != 1:
            details.append(f"multiplicity[{factor}]={multiplicity}")

    for check in report.local_chart_order_checks:
        if check.failure_reasons:
            details.append(
                f"chart[{check.facet_name}/{check.chart_name}]="
                f"{','.join(check.failure_reasons)}"
            )

    raise AssertionError(
        "TA-LP log-purity failed: "
        f"reasons={report.failure_reasons}; "
        f"details={'; '.join(details) if details else 'none'}"
    )
