from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import sympy as sp

from posgeo.geometry.lines import OrientedLine2D

Vertex = Tuple[sp.Rational, sp.Rational]


@dataclass(frozen=True)
class RegionWithInternalBoundaryFixture:
    """Container for a polygonal region with one internal polygonal hole boundary."""

    x: sp.Symbol
    y: sp.Symbol
    outer_facets: Dict[str, OrientedLine2D]
    inner_facets: Dict[str, OrientedLine2D]
    outer_vertices_ccw: Tuple[Vertex, ...]
    inner_vertices_cw: Tuple[Vertex, ...]


class SquareHoleRegionFixture:
    """Unit square with a centered square hole: outer boundary CCW, inner boundary CW."""

    @staticmethod
    def build() -> RegionWithInternalBoundaryFixture:
        x, y = sp.symbols("x y", real=True)

        outer_facets = {
            "outer_left": OrientedLine2D(x, y, x),
            "outer_bottom": OrientedLine2D(x, y, y),
            "outer_right": OrientedLine2D(x, y, 1 - x),
            "outer_top": OrientedLine2D(x, y, 1 - y),
        }

        # Hole corners are at (2/5,2/5), (3/5,2/5), (3/5,3/5), (2/5,3/5).
        # Facets are oriented so "inside" means outside the hole.
        inner_facets = {
            "inner_left": OrientedLine2D(x, y, sp.Rational(2, 5) - x),
            "inner_bottom": OrientedLine2D(x, y, sp.Rational(2, 5) - y),
            "inner_right": OrientedLine2D(x, y, x - sp.Rational(3, 5)),
            "inner_top": OrientedLine2D(x, y, y - sp.Rational(3, 5)),
        }

        outer_vertices_ccw = (
            (sp.Rational(0), sp.Rational(0)),
            (sp.Rational(1), sp.Rational(0)),
            (sp.Rational(1), sp.Rational(1)),
            (sp.Rational(0), sp.Rational(1)),
        )

        inner_vertices_cw = (
            (sp.Rational(2, 5), sp.Rational(2, 5)),
            (sp.Rational(2, 5), sp.Rational(3, 5)),
            (sp.Rational(3, 5), sp.Rational(3, 5)),
            (sp.Rational(3, 5), sp.Rational(2, 5)),
        )

        return RegionWithInternalBoundaryFixture(
            x=x,
            y=y,
            outer_facets=outer_facets,
            inner_facets=inner_facets,
            outer_vertices_ccw=outer_vertices_ccw,
            inner_vertices_cw=inner_vertices_cw,
        )
