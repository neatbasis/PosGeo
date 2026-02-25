from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import sympy as sp

from posgeo.forms.canonical2d import (
    Triangulation2D,
    triangulation_A_h1,
    triangulation_A_m1,
    triangulation_A_q1,
    triangulation_B_h1,
    triangulation_B_m1,
    triangulation_B_q1,
)
from posgeo.forms.residues2d import (
    FacetChart,
    h1_facet_charts_all,
    m1_facet_charts_all,
    q1_facet_charts_all,
)
from posgeo.geometry import H1_HEXAGON_FIXTURE, M1_PENTAGON_FIXTURE, Q1_QUADRILATERAL_FIXTURE
from posgeo.geometry.region2d import Region2D


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
        name=M1_PENTAGON_FIXTURE.name,
        build_region=M1_PENTAGON_FIXTURE.build_region,
        vertices=lambda: M1_PENTAGON_FIXTURE.vertices,
        tri_a=triangulation_A_m1,
        tri_b=triangulation_B_m1,
        facet_charts=m1_facet_charts_all,
    ),
    GeometryCase(
        name=Q1_QUADRILATERAL_FIXTURE.name,
        build_region=Q1_QUADRILATERAL_FIXTURE.build_region,
        vertices=lambda: Q1_QUADRILATERAL_FIXTURE.vertices,
        tri_a=triangulation_A_q1,
        tri_b=triangulation_B_q1,
        facet_charts=q1_facet_charts_all,
    ),
    GeometryCase(
        name=H1_HEXAGON_FIXTURE.name,
        build_region=H1_HEXAGON_FIXTURE.build_region,
        vertices=lambda: H1_HEXAGON_FIXTURE.vertices,
        tri_a=triangulation_A_h1,
        tri_b=triangulation_B_h1,
        facet_charts=h1_facet_charts_all,
    ),
)
