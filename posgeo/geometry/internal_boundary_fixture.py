from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import sympy as sp

from .lines import OrientedLine2D
from .region2d import Region2D


@dataclass(frozen=True)
class RegionWithInternalBoundaryFixture:
    """Square-with-hole fixture exposing two boundary components.

    Notes:
    - `enclosing_region` is only the outer square and is intentionally used to
      demonstrate where current invariants assume a single boundary component.
    - `outer_vertices_ccw` and `inner_vertices_cw` provide the correct component
      orientations for a region with a hole.
    """

    x: sp.Symbol
    y: sp.Symbol
    enclosing_region: Region2D
    all_boundary_facets: Dict[str, OrientedLine2D]
    outer_vertices_ccw: Tuple[Tuple[sp.Rational, sp.Rational], ...]
    inner_vertices_cw: Tuple[Tuple[sp.Rational, sp.Rational], ...]

    @property
    def flattened_vertices_assuming_single_ccw_loop(self) -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
        """Deliberately incorrect flattening used by legacy single-loop checks."""
        return self.outer_vertices_ccw + self.inner_vertices_cw


class SquareHoleRegionFixture:
    """Factory for a square with an internal square boundary component."""

    @staticmethod
    def build() -> RegionWithInternalBoundaryFixture:
        x, y = sp.symbols("x y", real=True)

        outer_facets = {
            "O_L": OrientedLine2D(x, y, x),
            "O_B": OrientedLine2D(x, y, y),
            "O_R": OrientedLine2D(x, y, 1 - x),
            "O_T": OrientedLine2D(x, y, 1 - y),
        }

        inner_facets = {
            "I_L": OrientedLine2D(x, y, x - sp.Rational(1, 3)),
            "I_B": OrientedLine2D(x, y, y - sp.Rational(1, 3)),
            "I_R": OrientedLine2D(x, y, sp.Rational(2, 3) - x),
            "I_T": OrientedLine2D(x, y, sp.Rational(2, 3) - y),
        }

        outer_vertices_ccw = (
            (sp.Rational(0), sp.Rational(0)),
            (sp.Rational(1), sp.Rational(0)),
            (sp.Rational(1), sp.Rational(1)),
            (sp.Rational(0), sp.Rational(1)),
        )

        # Correct orientation for an inner boundary component of a positively oriented region.
        inner_vertices_cw = (
            (sp.Rational(1, 3), sp.Rational(1, 3)),
            (sp.Rational(1, 3), sp.Rational(2, 3)),
            (sp.Rational(2, 3), sp.Rational(2, 3)),
            (sp.Rational(2, 3), sp.Rational(1, 3)),
        )

        return RegionWithInternalBoundaryFixture(
            x=x,
            y=y,
            enclosing_region=Region2D(x=x, y=y, facets=outer_facets),
            all_boundary_facets={**outer_facets, **inner_facets},
            outer_vertices_ccw=outer_vertices_ccw,
            inner_vertices_cw=inner_vertices_cw,
        )
