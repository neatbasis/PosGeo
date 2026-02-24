from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import sympy as sp

from .lines import OrientedLine2D


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

    def sample_interior_points(self, n: int = 25) -> List[Tuple[float, float]]:
        """
        Simple rejection sampler for the M1 pentagon (bounded within [0,1]^2).
        Works because M1 region is defined inside the unit square.
        """
        import random

        pts: List[Tuple[float, float]] = []
        attempts = 0
        while len(pts) < n and attempts < 100000:
            attempts += 1
            xv = random.random()
            yv = random.random()
            if self.contains(xv, yv):
                pts.append((xv, yv))
        if len(pts) < n:
            raise RuntimeError(f"Failed to sample {n} interior points; got {len(pts)}.")
        return pts


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
        x, y = sp.symbols("x y", real=True)
        facets = {
            "L1_x": OrientedLine2D(x, y, x),
            "L2_y": OrientedLine2D(x, y, y),
            "L3_1mx": OrientedLine2D(x, y, 1 - x),
            "L4_1my": OrientedLine2D(x, y, 1 - y),
            "L5_xpy_mhalf": OrientedLine2D(x, y, x + y - sp.Rational(1, 2)),
        }
        return Region2D(x=x, y=y, facets=facets)
    @staticmethod
    def vertices():
        import sympy as sp
        return (
            (sp.Rational(0), sp.Rational(1, 2)),
            (sp.Rational(0), sp.Rational(1)),
            (sp.Rational(1), sp.Rational(1)),
            (sp.Rational(1), sp.Rational(0)),
            (sp.Rational(1, 2), sp.Rational(0)),
        )