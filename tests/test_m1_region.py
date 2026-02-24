import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region


def test_region_is_nonempty_and_sampler_works():
    region = PentagonM1Region.build()
    pts = region.sample_interior_points(n=20)
    assert len(pts) == 20
    for (xv, yv) in pts:
        assert region.contains(xv, yv)