from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import sympy as sp


@dataclass(frozen=True)
class OrientedLine2D:
    """
    A linear function L(x,y) such that L > 0 is the "inside" side.
    """
    x: sp.Symbol
    y: sp.Symbol
    expr: sp.Expr  # linear in x,y

    def grad(self) -> Tuple[sp.Expr, sp.Expr]:
        return (sp.diff(self.expr, self.x), sp.diff(self.expr, self.y))

    def normalized(self) -> "OrientedLine2D":
        """
        Normalize up to a positive scalar: set gcd-like scaling not attempted;
        just make leading coefficient canonical for comparisons.
        """
        a = sp.Poly(self.expr, self.x, self.y).coeff_monomial(self.x)
        b = sp.Poly(self.expr, self.x, self.y).coeff_monomial(self.y)
        c = sp.Poly(self.expr, self.x, self.y).coeff_monomial(1)

        # Pick a deterministic sign: first nonzero among (a,b,c) should be positive
        for v in (a, b, c):
            if v != 0:
                if sp.sign(v) == -1:
                    return OrientedLine2D(self.x, self.y, -self.expr)
                return self
        return self  # zero shouldn't happen

    def eval_at(self, xv: float, yv: float) -> float:
        return float(self.expr.subs({self.x: xv, self.y: yv}))