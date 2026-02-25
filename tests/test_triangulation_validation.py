import sympy as sp
import pytest

from posgeo.forms.canonical2d import Triangulation2D, canonical_form_from_triangulation
from posgeo.forms.simplex2d import Triangle2D
from posgeo.validation import InvalidTriangulationError


def _error_codes(err: InvalidTriangulationError) -> set[str]:
    return {issue.code for issue in err.issues}


def test_triangulation_overlap_failure_mode():
    x, y = sp.symbols("x y", real=True)
    tri = Triangle2D.from_vertices(
        x, y,
        (sp.Rational(0), sp.Rational(0)),
        (sp.Rational(1), sp.Rational(0)),
        (sp.Rational(0), sp.Rational(1)),
    )
    triangulation = Triangulation2D(triangles=(tri, tri))

    with pytest.raises(InvalidTriangulationError) as exc:
        canonical_form_from_triangulation(
            triangulation,
            vertices=(
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(0)),
                (sp.Rational(0), sp.Rational(1)),
            ),
        )

    codes = _error_codes(exc.value)
    assert "internal_edge_orientation_mismatch" in codes
    assert "area_mismatch" in codes


def test_triangulation_gap_failure_mode():
    x, y = sp.symbols("x y", real=True)
    triangulation = Triangulation2D(
        triangles=(
            Triangle2D.from_vertices(
                x, y,
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(1)),
            ),
        )
    )

    with pytest.raises(InvalidTriangulationError) as exc:
        canonical_form_from_triangulation(
            triangulation,
            vertices=(
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(1)),
                (sp.Rational(0), sp.Rational(1)),
            ),
        )

    assert "area_mismatch" in _error_codes(exc.value)


def test_triangulation_internal_orientation_mismatch_failure_mode():
    x, y = sp.symbols("x y", real=True)
    triangulation = Triangulation2D(
        triangles=(
            Triangle2D.from_vertices(
                x, y,
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(1)),
            ),
            Triangle2D.from_vertices(
                x, y,
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(0), sp.Rational(1)),
                (sp.Rational(1), sp.Rational(1)),
            ),
        )
    )

    with pytest.raises(InvalidTriangulationError) as exc:
        canonical_form_from_triangulation(
            triangulation,
            vertices=(
                (sp.Rational(0), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(0)),
                (sp.Rational(1), sp.Rational(1)),
                (sp.Rational(0), sp.Rational(1)),
            ),
        )

    assert "internal_edge_orientation_mismatch" in _error_codes(exc.value)
