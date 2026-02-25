from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import sympy as sp

from .lines import OrientedLine2D
from .fixtures2d import M1_PENTAGON_FIXTURE, Q1_QUADRILATERAL_FIXTURE


@dataclass(frozen=True)
class Region2D:
    """
    Region defined by linear inequalities L_i(x,y) >= 0 (strict positivity is assumed in sampling/tests).
    """
    x: sp.Symbol
    y: sp.Symbol
    facets: Dict[str, OrientedLine2D]  # name -> oriented line (inside is >=0)

    def contains(self, xv: float, yv: float, eps: float = 1e-12) -> bool:
        for ln in self.facets.values():
            if ln.eval_at(xv, yv) <= eps:
                return False
        return True

    def _contains_symbolic(self, xv: sp.Rational, yv: sp.Rational) -> bool:
        """Exact strict interior check for symbolic/rational substitutions."""
        for ln in self.facets.values():
            value = sp.simplify(ln.expr.subs({self.x: xv, self.y: yv}))
            if value <= 0:
                return False
        return True

    def fixed_interior_rational_points(
        self,
        n: int = 25,
        *,
        max_denominator: int = 20,
    ) -> List[Tuple[sp.Rational, sp.Rational]]:
        """
        Deterministic exact interior points from an ordered rational lattice scan.

        This is useful for QA/tests that need reproducible, exact substitutions.
        """
        if n <= 0:
            return []

        pts: List[Tuple[sp.Rational, sp.Rational]] = []
        seen = set()
        for denom in range(2, max_denominator + 1):
            for ix in range(1, denom):
                xv = sp.Rational(ix, denom)
                for iy in range(1, denom):
                    yv = sp.Rational(iy, denom)
                    key = (xv, yv)
                    if key in seen:
                        continue
                    if self._contains_symbolic(xv, yv):
                        seen.add(key)
                        pts.append(key)
                        if len(pts) == n:
                            return pts

        raise RuntimeError(
            f"Failed to deterministically produce {n} interior rational points; got {len(pts)}."
        )

    def fixed_interior_float_points(self, n: int = 25) -> List[Tuple[float, float]]:
        """Deterministic float-valued interior sample derived from exact rationals."""
        return [
            (float(xv), float(yv))
            for xv, yv in self.fixed_interior_rational_points(n=n)
        ]

    def sample_interior_points(
        self,
        n: int = 25,
        *,
        deterministic: bool = False,
    ) -> List[Tuple[float, float]]:
        """Backwards-compatible sampling API, now always deterministic."""
        _ = deterministic  # retained for API compatibility
        return self.fixed_interior_float_points(n=n)


class PentagonM1Region:
    """
    A concrete convex pentagon inside the unit square:
      x > 0
      y > 0
      1-x > 0
      1-y > 0
      x+y-1/2 > 0

    Vertices (cyclic order):
      (0, 1/2), (0, 1), (1, 1), (1, 0), (1/2, 0)
    """

    @staticmethod
    def build() -> Region2D:
        return M1_PENTAGON_FIXTURE.build_region()

    @staticmethod
    def vertices():
        return M1_PENTAGON_FIXTURE.vertices


class QuadrilateralQ1Region:
    """
    Convex quadrilateral:
      x > 0
      y > 0
      1-y > 0
      2-x+y > 0

    Vertices (cyclic order):
      (0,0), (2,0), (3,1), (0,1)
    """

    @staticmethod
    def build() -> Region2D:
        return Q1_QUADRILATERAL_FIXTURE.build_region()

    @staticmethod
    def vertices():
        return Q1_QUADRILATERAL_FIXTURE.vertices
