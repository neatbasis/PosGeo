from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple

import sympy as sp

from posgeo.geometry.lines import OrientedLine2D

Vertex = Tuple[sp.Rational, sp.Rational]
FacetEquation = Tuple[str, sp.Expr]
ChartDef = Tuple[str, sp.Expr, sp.Expr, int]

_X = sp.Symbol("x")
_Y = sp.Symbol("y")


@dataclass(frozen=True)
class NamedFixture2D:
    name: str
    vertices: Tuple[Vertex, ...]
    facet_equations: Tuple[FacetEquation, ...]
    chart_defs: Mapping[str, Tuple[ChartDef, ...]]
    triangulation_a: Tuple[Tuple[int, int, int], ...]
    triangulation_b: Tuple[Tuple[int, int, int], ...]

    def build_region(self) -> "Region2D":
        from posgeo.geometry.region2d import Region2D

        x, y = sp.symbols("x y", real=True)
        facets = {
            facet_name: OrientedLine2D(x, y, sp.simplify(expr.subs({_X: x, _Y: y})))
            for facet_name, expr in self.facet_equations
        }
        return Region2D(x=x, y=y, facets=facets)


M1_PENTAGON_FIXTURE = NamedFixture2D(
    name="m1_pentagon",
    vertices=(
        (sp.Rational(0), sp.Rational(1, 2)),
        (sp.Rational(0), sp.Rational(1)),
        (sp.Rational(1), sp.Rational(1)),
        (sp.Rational(1), sp.Rational(0)),
        (sp.Rational(1, 2), sp.Rational(0)),
    ),
    facet_equations=(
        ("L1_x", _X),
        ("L2_y", _Y),
        ("L3_1mx", 1 - _X),
        ("L4_1my", 1 - _Y),
        ("L5_xpy_mhalf", _X + _Y - sp.Rational(1, 2)),
    ),
    chart_defs={
        "L1_x": (
            ("L1_x__t=y", sp.Symbol("u"), sp.Symbol("t"), 1),
            ("L1_x__t=1-y", sp.Symbol("u"), 1 - sp.Symbol("t"), -1),
        ),
        "L2_y": (
            ("L2_y__t=x", sp.Symbol("t"), sp.Symbol("u"), -1),
            ("L2_y__t=1-x", 1 - sp.Symbol("t"), sp.Symbol("u"), 1),
        ),
        "L3_1mx": (
            ("L3_1mx__t=y", 1 - sp.Symbol("u"), sp.Symbol("t"), -1),
            ("L3_1mx__t=1-y", 1 - sp.Symbol("u"), 1 - sp.Symbol("t"), 1),
        ),
        "L4_1my": (
            ("L4_1my__t=x", sp.Symbol("t"), 1 - sp.Symbol("u"), 1),
            ("L4_1my__t=1-x", 1 - sp.Symbol("t"), 1 - sp.Symbol("u"), -1),
        ),
        "L5_xpy_mhalf": (
            ("L5__t=x", sp.Symbol("t"), sp.Rational(1, 2) - sp.Symbol("t") + sp.Symbol("u"), -1),
            ("L5__t=y", sp.Rational(1, 2) - sp.Symbol("t") + sp.Symbol("u"), sp.Symbol("t"), 1),
        ),
    },
    triangulation_a=((1, 2, 3), (1, 3, 4), (1, 4, 0)),
    triangulation_b=((3, 4, 0), (3, 0, 1), (3, 1, 2)),
)


Q1_QUADRILATERAL_FIXTURE = NamedFixture2D(
    name="q1_quadrilateral",
    vertices=(
        (sp.Rational(0), sp.Rational(0)),
        (sp.Rational(2), sp.Rational(0)),
        (sp.Rational(3), sp.Rational(1)),
        (sp.Rational(0), sp.Rational(1)),
    ),
    facet_equations=(
        ("Q1_Lx", _X),
        ("Q1_By", _Y),
        ("Q1_T1my", 1 - _Y),
        ("Q1_D2mXpy", 2 - _X + _Y),
    ),
    chart_defs={
        "Q1_Lx": (
            ("Q1_Lx__t=y", sp.Symbol("u"), sp.Symbol("t"), 1),
            ("Q1_Lx__t=1-y", sp.Symbol("u"), 1 - sp.Symbol("t"), -1),
        ),
        "Q1_By": (
            ("Q1_By__t=x", sp.Symbol("t"), sp.Symbol("u"), -1),
            ("Q1_By__t=2-x", 2 - sp.Symbol("t"), sp.Symbol("u"), 1),
        ),
        "Q1_T1my": (
            ("Q1_T1my__t=x", sp.Symbol("t"), 1 - sp.Symbol("u"), 1),
            ("Q1_T1my__t=3-x", 3 - sp.Symbol("t"), 1 - sp.Symbol("u"), -1),
        ),
        "Q1_D2mXpy": (
            ("Q1_D2mXpy__t=x", sp.Symbol("t") + sp.Symbol("u"), sp.Symbol("t") - 2, -1),
            ("Q1_D2mXpy__t=y", sp.Symbol("t") + 2 + sp.Symbol("u"), sp.Symbol("t"), -1),
        ),
    },
    triangulation_a=((0, 1, 2), (0, 2, 3)),
    triangulation_b=((0, 1, 3), (1, 2, 3)),
)


H1_HEXAGON_FIXTURE = NamedFixture2D(
    name="h1_hexagon",
    vertices=(
        (sp.Rational(0), sp.Rational(1)),
        (sp.Rational(0), sp.Rational(2)),
        (sp.Rational(1), sp.Rational(2)),
        (sp.Rational(2), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(0)),
        (sp.Rational(1), sp.Rational(0)),
    ),
    facet_equations=(
        ("H1_x", _X),
        ("H2_y", _Y),
        ("H3_2mx", 2 - _X),
        ("H4_2my", 2 - _Y),
        ("H5_xpy_m1", _X + _Y - 1),
        ("H6_3mxmy", 3 - _X - _Y),
    ),
    chart_defs={
        "H1_x": (
            ("H1_x__t=y", sp.Symbol("u"), sp.Symbol("t"), 1),
            ("H1_x__t=2-y", sp.Symbol("u"), 2 - sp.Symbol("t"), -1),
        ),
        "H2_y": (
            ("H2_y__t=x", sp.Symbol("t"), sp.Symbol("u"), -1),
            ("H2_y__t=2-x", 2 - sp.Symbol("t"), sp.Symbol("u"), 1),
        ),
        "H3_2mx": (
            ("H3_2mx__t=y", 2 - sp.Symbol("u"), sp.Symbol("t"), -1),
            ("H3_2mx__t=2-y", 2 - sp.Symbol("u"), 2 - sp.Symbol("t"), 1),
        ),
        "H4_2my": (
            ("H4_2my__t=x", sp.Symbol("t"), 2 - sp.Symbol("u"), 1),
            ("H4_2my__t=2-x", 2 - sp.Symbol("t"), 2 - sp.Symbol("u"), -1),
        ),
        "H5_xpy_m1": (
            ("H5_xpy_m1__t=x", sp.Symbol("t"), 1 - sp.Symbol("t") + sp.Symbol("u"), -1),
            ("H5_xpy_m1__t=y", 1 - sp.Symbol("t") + sp.Symbol("u"), sp.Symbol("t"), 1),
        ),
        "H6_3mxmy": (
            ("H6_3mxmy__t=x", sp.Symbol("t") + sp.Symbol("u"), 3 - sp.Symbol("t"), 1),
            ("H6_3mxmy__t=y", sp.Symbol("t"), 3 - sp.Symbol("t") - sp.Symbol("u"), 1),
        ),
    },
    triangulation_a=((1, 2, 3), (1, 3, 4), (1, 4, 5), (1, 5, 0)),
    triangulation_b=((4, 5, 0), (4, 0, 1), (4, 1, 2), (4, 2, 3)),
)


FIXTURES2D: Dict[str, NamedFixture2D] = {
    M1_PENTAGON_FIXTURE.name: M1_PENTAGON_FIXTURE,
    Q1_QUADRILATERAL_FIXTURE.name: Q1_QUADRILATERAL_FIXTURE,
    H1_HEXAGON_FIXTURE.name: H1_HEXAGON_FIXTURE,
}
