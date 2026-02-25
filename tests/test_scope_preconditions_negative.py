import sympy as sp
import pytest

from posgeo.geometry.lines import OrientedLine2D
from posgeo.geometry.region2d import PentagonM1Region, Region2D
from posgeo.validation.preconditions import (
    OutOfScopeInputError,
    assert_canonical_scope,
    validate_canonical_scope,
)


def _square_region(*, flip_x_sign: bool = False, nonlinear: bool = False) -> Region2D:
    x, y = sp.symbols("x y", real=True)
    x_expr = -x if flip_x_sign else x
    top_expr = x**2 + y if nonlinear else y
    facets = {
        "left": OrientedLine2D(x, y, x_expr),
        "bottom": OrientedLine2D(x, y, top_expr),
        "right": OrientedLine2D(x, y, 1 - x),
        "top": OrientedLine2D(x, y, 1 - y),
    }
    return Region2D(x=x, y=y, facets=facets)


def _codes(region: Region2D, vertices, *, geometry_class: str = "convex_polygon_2d_linear") -> set[str]:
    violations = validate_canonical_scope(region=region, vertices=vertices, geometry_class=geometry_class)
    return {v.code for v in violations}


def test_validate_canonical_scope_reports_nonlinear_facet():
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    codes = _codes(_square_region(nonlinear=True), vertices)
    assert "nonlinear-facet" in codes


def test_validate_canonical_scope_reports_degenerate_polygon():
    vertices = [(0, 0), (1, 0), (2, 0)]
    codes = _codes(_square_region(), vertices)
    assert "degenerate-polygon" in codes


def test_validate_canonical_scope_reports_non_strict_convexity():
    vertices = [(0, 0), (1, 0), (2, 0), (2, 1), (0, 1)]
    codes = _codes(_square_region(), vertices)
    assert "non-strictly-convex" in codes


def test_validate_canonical_scope_reports_inconsistent_orientation():
    vertices = [(0, 0), (1, 0), (sp.Rational(1, 2), sp.Rational(1, 2)), (1, 1), (0, 1)]
    codes = _codes(_square_region(), vertices)
    assert "inconsistent-orientation" in codes


def test_validate_canonical_scope_reports_inward_normal_inconsistency():
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    codes = _codes(_square_region(flip_x_sign=True), vertices)
    assert "inward-normal-inconsistent" in codes


def test_validate_canonical_scope_reports_unsupported_geometry_class():
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    codes = _codes(_square_region(), vertices, geometry_class="ellipse_2d")
    assert "unsupported-geometry-class" in codes


def test_assert_canonical_scope_raises_with_informative_message():
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    with pytest.raises(OutOfScopeInputError, match="out-of-scope input") as exc_info:
        assert_canonical_scope(region=_square_region(nonlinear=True), vertices=vertices)

    msg = str(exc_info.value)
    assert "nonlinear-facet" in msg
    assert "is not linear" in msg


def test_assert_canonical_scope_raises_for_unsupported_geometry_class():
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    with pytest.raises(OutOfScopeInputError, match="unsupported-geometry-class") as exc_info:
        assert_canonical_scope(region=_square_region(), vertices=vertices, geometry_class="ellipse_2d")

    assert "supported=['convex_polygon_2d_linear']" in str(exc_info.value)


def test_positive_control_m1_scope_is_clean():
    region = PentagonM1Region.build()
    vertices = list(PentagonM1Region.vertices())

    violations = validate_canonical_scope(region=region, vertices=vertices)
    assert violations == ()

    assert_canonical_scope(region=region, vertices=vertices)
