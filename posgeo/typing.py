from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import sympy as sp


@dataclass(frozen=True)
class Canonical2Form:
    """
    Represents Omega = f(x,y) dx ∧ dy
    """
    x: sp.Symbol
    y: sp.Symbol
    prefactor: sp.Expr

    def simplify(self) -> "Canonical2Form":
        return Canonical2Form(self.x, self.y, sp.simplify(self.prefactor))


@dataclass(frozen=True)
class Canonical1Form:
    """
    Represents omega = g(t) dt
    """
    t: sp.Symbol
    prefactor: sp.Expr

    def simplify(self) -> "Canonical1Form":
        return Canonical1Form(self.t, sp.simplify(self.prefactor))