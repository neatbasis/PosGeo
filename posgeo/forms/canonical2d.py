from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import sympy as sp

from posgeo.forms.simplex2d import Triangle2D
from posgeo.geometry.fixtures2d import M1_PENTAGON_FIXTURE, Q1_QUADRILATERAL_FIXTURE
from posgeo.typing import Canonical2Form
from posgeo.validation.triangulation import validate_triangulation


@dataclass(frozen=True)
class Triangulation2D:
    """
    A triangulation of a polygonal region specified by triangles.
    """
    triangles: Tuple[Triangle2D, ...]


def canonical_form_from_triangulation(
    tri: Triangulation2D,
    *,
    region=None,
    vertices: Optional[Tuple[Tuple[sp.Rational, sp.Rational], ...]] = None,
) -> Canonical2Form:
    validate_triangulation(tri, region=region, vertices=vertices)
    x = tri.triangles[0].x
    y = tri.triangles[0].y
    f = sum((t.canonical_form().prefactor for t in tri.triangles), sp.Integer(0))
    return Canonical2Form(x, y, sp.simplify(f))


def m1_pentagon_vertices() -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
    """
    Cyclic order (counterclockwise):
      v0=(0,1/2), v1=(0,1), v2=(1,1), v3=(1,0), v4=(1/2,0)
    """
    return M1_PENTAGON_FIXTURE.vertices


def _triangulation_from_indices(
    vertices: Tuple[Tuple[sp.Rational, sp.Rational], ...],
    indices: Tuple[Tuple[int, int, int], ...],
    x: sp.Symbol,
    y: sp.Symbol,
) -> Triangulation2D:
    triangles = tuple(
        Triangle2D.from_vertices(x, y, vertices[i], vertices[j], vertices[k])
        for i, j, k in indices
    )
    return Triangulation2D(triangles=triangles)


def triangulation_A_m1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """
    Fan triangulation around vertex v1=(0,1):
      (v1,v2,v3), (v1,v3,v4), (v1,v4,v0)
    """
    return _triangulation_from_indices(
        M1_PENTAGON_FIXTURE.vertices,
        M1_PENTAGON_FIXTURE.triangulation_a,
        x,
        y,
    )


def triangulation_B_m1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """
    Fan triangulation around vertex v3=(1,0):
      (v3,v4,v0), (v3,v0,v1), (v3,v1,v2)
    """
    return _triangulation_from_indices(
        M1_PENTAGON_FIXTURE.vertices,
        M1_PENTAGON_FIXTURE.triangulation_b,
        x,
        y,
    )


def q1_quadrilateral_vertices() -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
    """
    Cyclic order (counterclockwise):
      v0=(0,0), v1=(2,0), v2=(3,1), v3=(0,1)
    """
    return Q1_QUADRILATERAL_FIXTURE.vertices


def triangulation_A_q1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """Diagonal (v0,v2): triangles (v0,v1,v2) and (v0,v2,v3)."""
    return _triangulation_from_indices(
        Q1_QUADRILATERAL_FIXTURE.vertices,
        Q1_QUADRILATERAL_FIXTURE.triangulation_a,
        x,
        y,
    )


def triangulation_B_q1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """Diagonal (v1,v3): triangles (v0,v1,v3) and (v1,v2,v3)."""
    return _triangulation_from_indices(
        Q1_QUADRILATERAL_FIXTURE.vertices,
        Q1_QUADRILATERAL_FIXTURE.triangulation_b,
        x,
        y,
    )
