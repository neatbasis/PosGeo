# Axioms: TA-LP, TA-GC

import pytest
import sympy as sp

from posgeo.forms.residues2d import m1_facet_charts_all
from posgeo.geometry.lines import OrientedLine2D
from posgeo.geometry.region2d import PentagonM1Region, Region2D
from posgeo.typing import Canonical2Form
from posgeo.validation import assert_log_pure, singularity_report
from posgeo.validation.preconditions import (
    OutOfScopeInputError,
    assert_canonical_scope,
    validate_canonical_scope,
)


def _unit_square_region() -> Region2D:
    x, y = sp.symbols("x y", real=True)
    facets = {
        "left": OrientedLine2D(x, y, x),
        "bottom": OrientedLine2D(x, y, y),
        "right": OrientedLine2D(x, y, 1 - x),
        "top": OrientedLine2D(x, y, 1 - y),
    }
    return Region2D(x=x, y=y, facets=facets)


def test_higher_order_pole_is_explicitly_rejected_by_singularity_report():
    """Axiom IDs: TA-LP, TA-GC. Test type: negative/failure-mode."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    synthetic_higher_order = Canonical2Form(x=x, y=y, prefactor=1 / (x**2 * y))
    report = singularity_report(synthetic_higher_order, region, m1_facet_charts_all(x, y))

    assert report.passed is False
    assert "non-simple-multiplicity" in report.failure_reasons
    assert "chart-order-failed" in report.failure_reasons
    assert any(multiplicity == 2 for _, multiplicity in report.multiplicities)

    failed_checks = [c for c in report.local_chart_order_checks if not c.passed]
    assert failed_checks
    assert any("chart-second-order-nonzero" in c.failure_reasons for c in failed_checks)



def test_higher_order_pole_is_explicitly_rejected_by_assert_log_pure():
    """Axiom IDs: TA-LP, TA-GC. Test type: negative/failure-mode."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    synthetic_higher_order = Canonical2Form(x=x, y=y, prefactor=1 / (x**2 * y))

    with pytest.raises(AssertionError, match="TA-LP log-purity failed") as exc_info:
        assert_log_pure(synthetic_higher_order, region, m1_facet_charts_all(x, y))

    message = str(exc_info.value)
    assert "non-simple-multiplicity" in message
    assert "chart-order-failed" in message


def test_assert_canonical_scope_exposes_unsupported_geometry_class_explicitly():
    """Axiom IDs: TA-GC. Test type: negative/scope-exclusion."""
    region = _unit_square_region()
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

    violations = validate_canonical_scope(
        region=region,
        vertices=vertices,
        geometry_class="projective_quadric_2d",
    )
    assert {v.code for v in violations} == {"unsupported-geometry-class"}

    with pytest.raises(OutOfScopeInputError, match="unsupported-geometry-class") as exc_info:
        assert_canonical_scope(
            region=region,
            vertices=vertices,
            geometry_class="projective_quadric_2d",
        )

    message = str(exc_info.value)
    assert "out-of-scope input" in message
    assert "supported=['convex_polygon_2d_linear']" in message
