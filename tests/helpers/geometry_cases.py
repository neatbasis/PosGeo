from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import sympy as sp

from posgeo.forms.canonical2d import (
    Triangulation2D,
    m1_pentagon_vertices,
    q1_quadrilateral_vertices,
    triangulation_A_m1,
    triangulation_A_q1,
    triangulation_B_m1,
    triangulation_B_q1,
)
from posgeo.forms.residues2d import FacetChart, m1_facet_charts_all, q1_facet_charts_all
from posgeo.forms.simplex2d import Triangle2D
from posgeo.geometry.lines import OrientedLine2D
from posgeo.geometry.region2d import PentagonM1Region, QuadrilateralQ1Region, Region2D


@dataclass(frozen=True)
class GeometryCase:
    name: str
    build_region: Callable[[], Region2D]
    vertices: Callable[[], Tuple[Tuple[sp.Rational, sp.Rational], ...]]
    tri_a: Callable[[sp.Symbol, sp.Symbol], Triangulation2D]
    tri_b: Callable[[sp.Symbol, sp.Symbol], Triangulation2D]
    facet_charts: Callable[[sp.Symbol, sp.Symbol], Dict[str, List[FacetChart]]]


def h1_hexagon_region() -> Region2D:
    x, y = sp.symbols("x y", real=True)
    facets = {
        "H1_x": OrientedLine2D(x, y, x),
        "H2_y": OrientedLine2D(x, y, y),
        "H3_2mx": OrientedLine2D(x, y, 2 - x),
        "H4_2my": OrientedLine2D(x, y, 2 - y),
        "H5_xpy_m1": OrientedLine2D(x, y, x + y - 1),
        "H6_3mxmy": OrientedLine2D(x, y, 3 - x - y),
    }
    return Region2D(x=x, y=y, facets=facets)


def h1_hexagon_vertices() -> Tuple[Tuple[sp.Rational, sp.Rational], ...]:
    return (
        (sp.Rational(0), sp.Rational(1)),
        (sp.Rational(0), sp.Rational(2)),
        (sp.Rational(1), sp.Rational(2)),
        (sp.Rational(2), sp.Rational(1)),
        (sp.Rational(2), sp.Rational(0)),
        (sp.Rational(1), sp.Rational(0)),
    )


def triangulation_A_h1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    v0, v1, v2, v3, v4, v5 = h1_hexagon_vertices()
    tris = (
        Triangle2D.from_vertices(x, y, v1, v2, v3),
        Triangle2D.from_vertices(x, y, v1, v3, v4),
        Triangle2D.from_vertices(x, y, v1, v4, v5),
        Triangle2D.from_vertices(x, y, v1, v5, v0),
    )
    return Triangulation2D(triangles=tris)


def triangulation_B_h1(x: sp.Symbol, y: sp.Symbol) -> Triangulation2D:
    v0, v1, v2, v3, v4, v5 = h1_hexagon_vertices()
    tris = (
        Triangle2D.from_vertices(x, y, v4, v5, v0),
        Triangle2D.from_vertices(x, y, v4, v0, v1),
        Triangle2D.from_vertices(x, y, v4, v1, v2),
        Triangle2D.from_vertices(x, y, v4, v2, v3),
    )
    return Triangulation2D(triangles=tris)


def h1_facet_charts_all(x: sp.Symbol, y: sp.Symbol) -> Dict[str, List[FacetChart]]:
    _ = (x, y)

    def chart(name: str, x_of: sp.Expr, y_of: sp.Expr, s: int) -> FacetChart:
        u = sp.Symbol(f"u__{name}", real=True)
        t = sp.Symbol(f"t__{name}", real=True)
        return FacetChart(
            name=name,
            u=u,
            t=t,
            x_of=sp.simplify(x_of.subs({sp.Symbol("u"): u, sp.Symbol("t"): t})),
            y_of=sp.simplify(y_of.subs({sp.Symbol("u"): u, sp.Symbol("t"): t})),
            s=sp.Integer(s),
        )

    u, t = sp.Symbol("u"), sp.Symbol("t")
    return {
        "H1_x": [
            chart("H1_x__t=y", u, t, 1),
            chart("H1_x__t=2-y", u, 2 - t, -1),
        ],
        "H2_y": [
            chart("H2_y__t=x", t, u, -1),
            chart("H2_y__t=2-x", 2 - t, u, 1),
        ],
        "H3_2mx": [
            chart("H3_2mx__t=y", 2 - u, t, -1),
            chart("H3_2mx__t=2-y", 2 - u, 2 - t, 1),
        ],
        "H4_2my": [
            chart("H4_2my__t=x", t, 2 - u, 1),
            chart("H4_2my__t=2-x", 2 - t, 2 - u, -1),
        ],
        "H5_xpy_m1": [
            chart("H5_xpy_m1__t=x", t, 1 - t + u, -1),
            chart("H5_xpy_m1__t=y", 1 - t + u, t, 1),
        ],
        "H6_3mxmy": [
            chart("H6_3mxmy__t=x", t + u, 3 - t, 1),
            chart("H6_3mxmy__t=y", t, 3 - t - u, 1),
        ],
    }


GEOMETRY_CASES: Tuple[GeometryCase, ...] = (
    GeometryCase(
        name="m1_pentagon",
        build_region=PentagonM1Region.build,
        vertices=m1_pentagon_vertices,
        tri_a=triangulation_A_m1,
        tri_b=triangulation_B_m1,
        facet_charts=m1_facet_charts_all,
    ),
    GeometryCase(
        name="q1_quadrilateral",
        build_region=QuadrilateralQ1Region.build,
        vertices=q1_quadrilateral_vertices,
        tri_a=triangulation_A_q1,
        tri_b=triangulation_B_q1,
        facet_charts=q1_facet_charts_all,
    ),
    GeometryCase(
        name="h1_hexagon",
        build_region=h1_hexagon_region,
        vertices=h1_hexagon_vertices,
        tri_a=triangulation_A_h1,
        tri_b=triangulation_B_h1,
        facet_charts=h1_facet_charts_all,
    ),
)
