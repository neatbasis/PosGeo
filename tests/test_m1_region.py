import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region


def test_region_is_nonempty_and_sampler_works():
    region = PentagonM1Region.build()
    pts = region.sample_interior_points(n=20, deterministic=True)
    assert len(pts) == 20
    for (xv, yv) in pts:
        assert region.contains(xv, yv)


def test_region_fixed_rational_points_are_exact_and_interior():
    region = PentagonM1Region.build()
    pts = region.fixed_interior_rational_points(n=20)
    assert len(pts) == 20
    for xv, yv in pts:
        assert isinstance(xv, sp.Rational)
        assert isinstance(yv, sp.Rational)
        assert region._contains_symbolic(xv, yv)
