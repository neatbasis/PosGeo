from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

import sympy as sp

from posgeo.geometry.region2d import Region2D


SUPPORTED_GEOMETRY_CLASSES = {"convex_polygon_2d_linear"}


@dataclass(frozen=True)
class ScopeViolation:
    code: str
    detail: str


class OutOfScopeInputError(ValueError):
    """Raised when a region/input does not satisfy repository scope assumptions."""


Point2 = Tuple[sp.Expr, sp.Expr]


def _is_linear_in_xy(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> bool:
    poly = sp.Poly(sp.expand(expr), x, y)
    return poly.total_degree() <= 1


def _signed_area(vertices: Sequence[Point2]) -> sp.Expr:
    area2 = sp.Integer(0)
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1
    return sp.simplify(sp.Rational(1, 2) * area2)


def _cross_z(a: Point2, b: Point2, c: Point2) -> sp.Expr:
    ax, ay = a
    bx, by = b
    cx, cy = c
    return sp.simplify((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))


def validate_canonical_scope(
    *,
    region: Region2D,
    vertices: Sequence[Point2],
    geometry_class: str = "convex_polygon_2d_linear",
) -> Tuple[ScopeViolation, ...]:
    """Validate scoped assumptions for canonical-form invariant checks."""
    issues: list[ScopeViolation] = []

    if geometry_class not in SUPPORTED_GEOMETRY_CLASSES:
        issues.append(
            ScopeViolation(
                code="unsupported-geometry-class",
                detail=(
                    f"got geometry_class={geometry_class!r}; "
                    f"supported={sorted(SUPPORTED_GEOMETRY_CLASSES)}"
                ),
            )
        )

    if len(vertices) < 3:
        issues.append(ScopeViolation("not-a-polygon", f"need >=3 vertices, got {len(vertices)}"))
        return tuple(issues)

    x, y = region.x, region.y
    for name, ln in region.facets.items():
        if not _is_linear_in_xy(ln.expr, x, y):
            issues.append(
                ScopeViolation(
                    code="nonlinear-facet",
                    detail=f"facet {name} is not linear in ({x}, {y}): {sp.expand(ln.expr)}",
                )
            )

    # Orientation consistency and bounded convex polygon checks rely on cyclic vertices.
    area = _signed_area(vertices)
    if sp.simplify(area) == 0:
        issues.append(ScopeViolation("degenerate-polygon", "signed area is zero"))
    else:
        orientation = 1 if area > 0 else -1
        n = len(vertices)
        for i in range(n):
            turn = _cross_z(vertices[i], vertices[(i + 1) % n], vertices[(i + 2) % n])
            if sp.simplify(turn) == 0:
                issues.append(
                    ScopeViolation(
                        "non-strictly-convex",
                        f"collinear consecutive vertices at indices {(i, (i + 1) % n, (i + 2) % n)}",
                    )
                )
                continue
            if (turn > 0) != (orientation > 0):
                issues.append(
                    ScopeViolation(
                        "inconsistent-orientation",
                        f"turn sign mismatch near vertex index {(i + 1) % n}",
                    )
                )
                break

    # Half-space orientation check: polygon centroid should be strictly inside every facet.
    cx = sp.simplify(sum(vx for vx, _ in vertices) / len(vertices))
    cy = sp.simplify(sum(vy for _, vy in vertices) / len(vertices))
    for name, ln in region.facets.items():
        val = sp.simplify(ln.expr.subs({x: cx, y: cy}))
        if val <= 0:
            issues.append(
                ScopeViolation(
                    "inward-normal-inconsistent",
                    f"facet {name} does not orient interior as >=0 at centroid ({cx},{cy}); value={val}",
                )
            )

    # Boundary coverage sanity: each vertex should sit on at least two facets (polygon corners).
    for i, (vx, vy) in enumerate(vertices):
        hits = 0
        for ln in region.facets.values():
            if sp.simplify(ln.expr.subs({x: vx, y: vy})) == 0:
                hits += 1
        if hits < 2:
            issues.append(
                ScopeViolation(
                    "vertex-not-on-boundary",
                    f"vertex index {i}={vx, vy} lies on only {hits} facets",
                )
            )

    return tuple(issues)


def assert_canonical_scope(
    *,
    region: Region2D,
    vertices: Sequence[Point2],
    geometry_class: str = "convex_polygon_2d_linear",
) -> None:
    violations = validate_canonical_scope(region=region, vertices=vertices, geometry_class=geometry_class)
    if not violations:
        return
    msg = "; ".join(f"{v.code}: {v.detail}" for v in violations)
    raise OutOfScopeInputError(f"out-of-scope input: {msg}")
