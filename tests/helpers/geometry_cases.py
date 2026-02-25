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
from posgeo.geometry.region2d import PentagonM1Region, QuadrilateralQ1Region, Region2D


@dataclass(frozen=True)
class GeometryCase:
    name: str
    build_region: Callable[[], Region2D]
    vertices: Callable[[], Tuple[Tuple[sp.Rational, sp.Rational], ...]]
    tri_a: Callable[[sp.Symbol, sp.Symbol], Triangulation2D]
    tri_b: Callable[[sp.Symbol, sp.Symbol], Triangulation2D]
    facet_charts: Callable[[sp.Symbol, sp.Symbol], Dict[str, List[FacetChart]]]


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
)
