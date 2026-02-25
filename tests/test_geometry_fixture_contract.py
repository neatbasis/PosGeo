import sympy as sp

from posgeo.geometry import FIXTURES2D


def test_fixture_vertices_and_facets_are_self_consistent():
    for fixture in FIXTURES2D.values():
        region = fixture.build_region()
        verts = list(fixture.vertices)
        assert len(verts) >= 3, f"{fixture.name}: needs at least 3 vertices"

        for vx, vy in verts:
            hits = sum(
                1
                for ln in region.facets.values()
                if sp.simplify(ln.expr.subs({region.x: vx, region.y: vy})) == 0
            )
            assert hits >= 2, f"{fixture.name}: vertex {(vx, vy)} not on >=2 facets"

        for facet_name, ln in region.facets.items():
            on_facet = [
                i
                for i, (vx, vy) in enumerate(verts)
                if sp.simplify(ln.expr.subs({region.x: vx, region.y: vy})) == 0
            ]
            assert len(on_facet) == 2, f"{fixture.name}/{facet_name}: expected 2 vertices on facet"
            i, j = on_facet
            n = len(verts)
            adjacent = (i + 1) % n == j or (j + 1) % n == i
            assert adjacent, f"{fixture.name}/{facet_name}: facet vertices are not adjacent in CCW order"

        cx = sp.Rational(1, len(verts)) * sum(vx for vx, _ in verts)
        cy = sp.Rational(1, len(verts)) * sum(vy for _, vy in verts)
        for facet_name, ln in region.facets.items():
            value = sp.simplify(ln.expr.subs({region.x: cx, region.y: cy}))
            assert value > 0, f"{fixture.name}/{facet_name}: centroid not inside oriented half-space"
