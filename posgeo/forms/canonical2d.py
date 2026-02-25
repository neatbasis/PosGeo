from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import sympy as sp

from posgeo.forms.simplex2d import Triangle2D
from posgeo.typing import Canonical2Form


@dataclass(frozen=True)
class Triangulation2D:
    """
    A triangulation of a polygonal region specified by triangles.
    """
    triangles: Tuple[Triangle2D, ...]


def canonical_form_from_triangulation(tri: Triangulation2D) -> Canonical2Form:
    if not tri.triangles:
        raise ValueError("Triangulation has no triangles.")
    x = tri.triangles[0].x
    y = tri.triangles[0].y
    f = sum((t.canonical_form().prefactor for t in tri.triangles), sp.Integer(0))
    return Canonical2Form(x, y, sp.simplify(f))


def m1_pentagon_vertices() -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
    """
    Cyclic order (counterclockwise):
      v0=(0,1/2), v1=(0,1), v2=(1,1), v3=(1,0), v4=(1/2,0)
    """
    return (
        (sp.Rational(0), sp.Rational(1, 2)),
        (sp.Rational(0), sp.Rational(1)),
        (sp.Rational(1), sp.Rational(1)),
        (sp.Rational(1), sp.Rational(0)),
        (sp.Rational(1, 2), sp.Rational(0)),
    )


def triangulation_A_m1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """
    Fan triangulation around vertex v1=(0,1):
      (v1,v2,v3), (v1,v3,v4), (v1,v4,v0)
    """
    v = m1_pentagon_vertices()
    v0, v1, v2, v3, v4 = v
    tris = (
        Triangle2D.from_vertices(x, y, v1, v2, v3),
        Triangle2D.from_vertices(x, y, v1, v3, v4),
        Triangle2D.from_vertices(x, y, v1, v4, v0),
    )
    return Triangulation2D(triangles=tris)


def triangulation_B_m1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """
    Fan triangulation around vertex v3=(1,0):
      (v3,v4,v0), (v3,v0,v1), (v3,v1,v2)
    """
    v = m1_pentagon_vertices()
    v0, v1, v2, v3, v4 = v
    tris = (
        Triangle2D.from_vertices(x, y, v3, v4, v0),
        Triangle2D.from_vertices(x, y, v3, v0, v1),
        Triangle2D.from_vertices(x, y, v3, v1, v2),
    )
    return Triangulation2D(triangles=tris)


def q1_quadrilateral_vertices() -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
    """
    Cyclic order (counterclockwise):
      v0=(0,0), v1=(2,0), v2=(3,1), v3=(0,1)
    """
    return (
        (sp.Rational(0), sp.Rational(0)),
        (sp.Rational(2), sp.Rational(0)),
        (sp.Rational(3), sp.Rational(1)),
        (sp.Rational(0), sp.Rational(1)),
    )


def triangulation_A_q1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """Diagonal (v0,v2): triangles (v0,v1,v2) and (v0,v2,v3)."""
    v0, v1, v2, v3 = q1_quadrilateral_vertices()
    tris = (
        Triangle2D.from_vertices(x, y, v0, v1, v2),
        Triangle2D.from_vertices(x, y, v0, v2, v3),
    )
    return Triangulation2D(triangles=tris)


def triangulation_B_q1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    """Diagonal (v1,v3): triangles (v0,v1,v3) and (v1,v2,v3)."""
    v0, v1, v2, v3 = q1_quadrilateral_vertices()
    tris = (
        Triangle2D.from_vertices(x, y, v0, v1, v3),
        Triangle2D.from_vertices(x, y, v1, v2, v3),
    )
    return Triangulation2D(triangles=tris)
