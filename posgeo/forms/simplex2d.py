from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import sympy as sp

from posgeo.geometry.lines import OrientedLine2D
from posgeo.typing import Canonical2Form


def _line_expr_through_points(x: sp.Symbol, y: sp.Symbol, p: Tuple[sp.Rational, sp.Rational], q: Tuple[sp.Rational, sp.Rational]) -> sp.Expr:
    """
    Returns linear expression L(x,y) = a*x + b*y + c such that L(p)=L(q)=0.
    """
    (x1, y1), (x2, y2) = p, q
    # Using determinant form:
    # |x y 1|
    # |x1 y1 1| = 0 gives line equation through p and q.
    # |x2 y2 1|
    return sp.Matrix([[x, y, 1], [x1, y1, 1], [x2, y2, 1]]).det()


def _orient_line_positive_at_point(x: sp.Symbol, y: sp.Symbol, expr: sp.Expr, interior: Tuple[sp.Rational, sp.Rational]) -> sp.Expr:
    val = sp.simplify(expr.subs({x: interior[0], y: interior[1]}))
    if val == 0:
        raise ValueError("Interior point lies on the line; cannot orient.")
    if val < 0:
        return -expr
    return expr


@dataclass(frozen=True)
class Triangle2D:
    x: sp.Symbol
    y: sp.Symbol
    vertices: Tuple[Tuple[sp.Rational, sp.Rational], Tuple[sp.Rational, sp.Rational], Tuple[sp.Rational, sp.Rational]]
    edges: Tuple[OrientedLine2D, OrientedLine2D, OrientedLine2D]  # oriented inward (>=0 inside)

    @staticmethod
    def from_vertices(
        x: sp.Symbol,
        y: sp.Symbol,
        v0: Tuple[sp.Rational, sp.Rational],
        v1: Tuple[sp.Rational, sp.Rational],
        v2: Tuple[sp.Rational, sp.Rational],
    ) -> "Triangle2D":
        verts = (v0, v1, v2)
        # centroid as interior point
        cx = sp.Rational(1, 3) * (v0[0] + v1[0] + v2[0])
        cy = sp.Rational(1, 3) * (v0[1] + v1[1] + v2[1])
        interior = (cx, cy)

        # edges are lines through (v1,v2), (v2,v0), (v0,v1)
        e0 = _line_expr_through_points(x, y, v1, v2)
        e1 = _line_expr_through_points(x, y, v2, v0)
        e2 = _line_expr_through_points(x, y, v0, v1)

        e0 = _orient_line_positive_at_point(x, y, e0, interior)
        e1 = _orient_line_positive_at_point(x, y, e1, interior)
        e2 = _orient_line_positive_at_point(x, y, e2, interior)

        return Triangle2D(
            x=x,
            y=y,
            vertices=verts,
            edges=(OrientedLine2D(x, y, sp.simplify(e0)),
                   OrientedLine2D(x, y, sp.simplify(e1)),
                   OrientedLine2D(x, y, sp.simplify(e2))),
        )

    def canonical_form(self) -> Canonical2Form:
        """
        Canonical 2-form of a triangle:
          Omega = f(x,y) dx ∧ dy
        where
          f = sum_{cyc} det(∇l_i, ∇l_j)/(l_i l_j)
        """
        l = [e.expr for e in self.edges]
        grads = [e.grad() for e in self.edges]

        def det2(a, b):
            return sp.simplify(a[0] * b[1] - a[1] * b[0])

        f = (
            det2(grads[0], grads[1]) / (l[0] * l[1])
            + det2(grads[1], grads[2]) / (l[1] * l[2])
            + det2(grads[2], grads[0]) / (l[2] * l[0])
        )
        return Canonical2Form(self.x, self.y, sp.simplify(f))