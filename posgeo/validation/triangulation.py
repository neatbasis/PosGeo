from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

import sympy as sp

if TYPE_CHECKING:
    from posgeo.forms.canonical2d import Triangulation2D
from posgeo.geometry.region2d import Region2D

Vertex = Tuple[sp.Rational, sp.Rational]
UndirectedEdge = Tuple[Vertex, Vertex]


@dataclass(frozen=True)
class TriangulationIssue:
    code: str
    details: Dict[str, object]


class InvalidTriangulationError(ValueError):
    def __init__(self, issues: List[TriangulationIssue]):
        self.issues = tuple(issues)
        super().__init__(f"Invalid triangulation with {len(self.issues)} issue(s): {[i.code for i in self.issues]}")



def _normalize_edge(a: Vertex, b: Vertex) -> UndirectedEdge:
    return (a, b) if a <= b else (b, a)


def _double_signed_area(v0: Vertex, v1: Vertex, v2: Vertex) -> sp.Expr:
    return sp.simplify((v1[0] - v0[0]) * (v2[1] - v0[1]) - (v1[1] - v0[1]) * (v2[0] - v0[0]))


def _polygon_double_area(vertices: Tuple[Vertex, ...]) -> sp.Expr:
    acc = sp.Integer(0)
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        acc += x1 * y2 - y1 * x2
    return sp.simplify(acc)


def validate_triangulation(
    tri: "Triangulation2D",
    *,
    region: Optional[Region2D] = None,
    vertices: Optional[Tuple[Vertex, ...]] = None,
) -> None:
    issues: List[TriangulationIssue] = []

    if not tri.triangles:
        issues.append(TriangulationIssue(code="empty_triangulation", details={}))
        raise InvalidTriangulationError(issues)

    x0 = tri.triangles[0].x
    y0 = tri.triangles[0].y

    undirected_counts: Dict[UndirectedEdge, int] = {}
    directed_counts: Dict[Tuple[Vertex, Vertex], int] = {}

    total_double_area = sp.Integer(0)

    for idx, triangle in enumerate(tri.triangles):
        if triangle.x != x0 or triangle.y != y0:
            issues.append(
                TriangulationIssue(
                    code="inconsistent_symbols",
                    details={"triangle_index": idx},
                )
            )

        v0, v1, v2 = triangle.vertices
        two_area = _double_signed_area(v0, v1, v2)
        if sp.simplify(two_area) == 0:
            issues.append(
                TriangulationIssue(
                    code="degenerate_triangle",
                    details={"triangle_index": idx, "vertices": triangle.vertices},
                )
            )
        total_double_area += sp.Abs(two_area)

        oriented_edges = ((v0, v1), (v1, v2), (v2, v0))
        for start, end in oriented_edges:
            directed_counts[(start, end)] = directed_counts.get((start, end), 0) + 1
            e = _normalize_edge(start, end)
            undirected_counts[e] = undirected_counts.get(e, 0) + 1

    if region is not None and (region.x != x0 or region.y != y0):
        issues.append(TriangulationIssue(code="region_symbol_mismatch", details={}))

    for edge, multiplicity in undirected_counts.items():
        if multiplicity not in (1, 2):
            issues.append(
                TriangulationIssue(
                    code="invalid_edge_multiplicity",
                    details={"edge": edge, "multiplicity": multiplicity},
                )
            )
        if multiplicity == 2:
            a, b = edge
            ab = directed_counts.get((a, b), 0)
            ba = directed_counts.get((b, a), 0)
            if not (ab == 1 and ba == 1):
                issues.append(
                    TriangulationIssue(
                        code="internal_edge_orientation_mismatch",
                        details={"edge": edge, "forward_count": ab, "reverse_count": ba},
                    )
                )

    if vertices is not None:
        if len(vertices) < 3:
            issues.append(TriangulationIssue(code="invalid_target_polygon", details={"vertex_count": len(vertices)}))
        else:
            poly_double_area = sp.Abs(_polygon_double_area(vertices))
            if sp.simplify(poly_double_area - total_double_area) != 0:
                issues.append(
                    TriangulationIssue(
                        code="area_mismatch",
                        details={
                            "triangulation_double_area": sp.simplify(total_double_area),
                            "target_double_area": sp.simplify(poly_double_area),
                        },
                    )
                )

    if issues:
        raise InvalidTriangulationError(issues)
