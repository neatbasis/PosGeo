# Axioms: TA-LP, TA-GC

import pytest
import sympy as sp

from posgeo.forms.canonical2d import canonical_form_from_triangulation
from posgeo.typing import Canonical2Form
from posgeo.validation import assert_log_pure, singularity_report
from tests.helpers.geometry_cases import GEOMETRY_CASES
from tests.helpers.pole_checks import format_failure_reasons


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits(geometry_case):
    """Axiom IDs: TA-LP, TA-GC. Test type: failure-mode."""
    region = geometry_case.build_region()
    x, y = region.x, region.y

    omega = canonical_form_from_triangulation(geometry_case.tri_a(x, y)).simplify()
    charts = geometry_case.facet_charts(x, y)

    report = assert_log_pure(omega, region, charts)

    assert report.boundary_mapping_status is True
    assert all(multiplicity == 1 for _, multiplicity in report.multiplicities)
    assert report.detected_pole_loci
    assert all(check.passed for check in report.local_chart_order_checks)


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_assert_log_pure_reports_failures_machine_readably(geometry_case):
    region = geometry_case.build_region()
    x, y = region.x, region.y
    charts = geometry_case.facet_charts(x, y)

    boundary_facets = list(region.facets.values())
    primary = sp.simplify(boundary_facets[0].expr)
    secondary = sp.simplify(boundary_facets[1].expr)

    # Squared boundary factor violates simple-pole multiplicity and local chart order checks.
    bad = Canonical2Form(x=x, y=y, prefactor=1 / (primary**2 * secondary))
    report = singularity_report(bad, region, charts)

    assert report.passed is False
    assert "non-simple-multiplicity" in report.failure_reasons
    assert any(m == 2 for _, m in report.multiplicities)

    failed_chart_checks = [check for check in report.local_chart_order_checks if not check.passed]
    assert failed_chart_checks
    assert any("chart-second-order-nonzero" in check.failure_reasons for check in failed_chart_checks)

    with pytest.raises(AssertionError, match="TA-LP log-purity failed"):
        assert_log_pure(bad, region, charts)


def test_singularity_report_failure_reasons_snapshot():
    region = GEOMETRY_CASES[0].build_region()
    x, y = region.x, region.y
    charts = GEOMETRY_CASES[0].facet_charts(x, y)

    bad = Canonical2Form(x=x, y=y, prefactor=1 / (x**2 * (x + y + 7)))
    report = singularity_report(bad, region, charts)

    formatted_reasons = tuple(format_failure_reasons(report).split(" | "))

    assert set(formatted_reasons) == {
        "non-boundary-pole",
        "non-simple-multiplicity",
        "chart-order-failed",
    }
    assert len(formatted_reasons) == 3

    assert "non-boundary-pole" in report.failure_reasons
    assert "non-simple-multiplicity" in report.failure_reasons
    assert "chart-order-failed" in report.failure_reasons
    assert len(report.failure_reasons) == 3
