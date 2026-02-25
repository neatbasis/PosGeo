# Axioms: TA-LP, TA-GC

import pytest
import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from posgeo.forms.residues2d import m1_facet_charts_all
from posgeo.typing import Canonical2Form
from posgeo.validation import assert_log_pure, singularity_report


def test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits():
    """Axiom IDs: TA-LP, TA-GC. Test type: failure-mode."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    charts = m1_facet_charts_all(x, y)

    report = assert_log_pure(omega, region, charts)

    assert report.boundary_mapping_status is True
    assert all(multiplicity == 1 for _, multiplicity in report.multiplicities)
    assert report.detected_pole_loci
    assert all(check.passed for check in report.local_chart_order_checks)


def test_assert_log_pure_reports_failures_machine_readably():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    charts = m1_facet_charts_all(x, y)

    # x^2 in the denominator violates simple-pole multiplicity and local chart order checks.
    bad = Canonical2Form(x=x, y=y, prefactor=1 / (x**2 * y))
    report = singularity_report(bad, region, charts)

    assert report.passed is False
    assert "non-simple-multiplicity" in report.failure_reasons
    assert any(m == 2 for _, m in report.multiplicities)

    failed_chart_checks = [check for check in report.local_chart_order_checks if not check.passed]
    assert failed_chart_checks
    assert any("chart-second-order-nonzero" in check.failure_reasons for check in failed_chart_checks)

    with pytest.raises(AssertionError, match="TA-LP log-purity failed"):
        assert_log_pure(bad, region, charts)
