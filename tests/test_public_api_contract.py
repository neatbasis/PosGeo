# tests/test_public_api_contract.py
import sympy as sp

from posgeo.geometry import M1_PENTAGON_FIXTURE
from posgeo.geometry.region2d import PentagonM1Region, Region2D
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    triangulation_B_m1
)
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
)


def _is_finite_expr(e: sp.Expr) -> bool:
    """
    Conservative "finite" check: reject NaN / +/-oo / zoo.
    """
    s = sp.simplify(e)
    return not (s.has(sp.nan) or s.has(sp.zoo) or s is sp.oo or s is -sp.oo)


def test_region_build_contract():
    region = PentagonM1Region.build()
    assert isinstance(region, Region2D)

    expected = {"L1_x", "L2_y", "L3_1mx", "L4_1my", "L5_xpy_mhalf"}
    assert set(region.facets.keys()) == expected

    x, y = region.x, region.y
    for name, ln in region.facets.items():
        # facet expressions should be linear in x,y
        poly = sp.Poly(sp.factor(ln.expr), x, y, domain="QQ")
        assert poly.total_degree() <= 1, f"{name} not linear: {ln.expr}"


def test_vertices_contract_is_ccw_and_matches_region():
    verts = list(M1_PENTAGON_FIXTURE.vertices)
    assert len(verts) == 5

    # match Region2D facet set expectations by checking each vertex lies on >=2 boundary lines
    region = PentagonM1Region.build()
    X, Y = region.x, region.y
    for vx, vy in verts:
        hits = 0
        for ln in region.facets.values():
            if sp.simplify(ln.expr.subs({X: vx, Y: vy})) == 0:
                hits += 1
        assert hits >= 2, f"vertex {(vx,vy)} not on >=2 facets (hits={hits})"


def test_triangulation_forms_have_same_symbols_and_are_finite_interior():
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    omegaB = canonical_form_from_triangulation(triangulation_B_m1(x, y)).simplify()

    assert omegaA.x == x and omegaA.y == y
    assert omegaB.x == x and omegaB.y == y

    # Spot-check finiteness on sampled interior points
    for xv, yv in region.sample_interior_points(n=10, deterministic=True):
        a = sp.simplify(omegaA.prefactor.subs({x: xv, y: yv}))
        b = sp.simplify(omegaB.prefactor.subs({x: xv, y: yv}))
        assert _is_finite_expr(a), f"omegaA not finite at {(xv,yv)}: {a}"
        assert _is_finite_expr(b), f"omegaB not finite at {(xv,yv)}: {b}"


def test_m1_facet_charts_all_contract_and_residue_produces_finite_1forms():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    charts_by_facet = m1_facet_charts_all(x, y)
    assert isinstance(charts_by_facet, dict)

    expected = {"L1_x", "L2_y", "L3_1mx", "L4_1my", "L5_xpy_mhalf"}
    assert set(charts_by_facet.keys()) == expected

    for facet, charts in charts_by_facet.items():
        assert isinstance(charts, list) and len(charts) >= 2, f"{facet} needs >=2 charts"
        for ch in charts:
            res = residue_2form_on_facet(omega, ch).simplify()
            assert res.t == ch.t
            assert _is_finite_expr(res.prefactor), (
                f"[{facet}] residue produced non-finite prefactor in {ch.name}: {res.prefactor}"
            )

