import pytest

from posgeo.forms.residues2d import (
    interval_endpoints_from_chart_ccw,
    interval_endpoints_from_chart_ccw_compat,
    m1_facet_charts_all,
)
from posgeo.geometry import M1_PENTAGON_FIXTURE, Q1_QUADRILATERAL_FIXTURE
from posgeo.geometry.region2d import PentagonM1Region


def test_interval_endpoints_compat_legacy_3arg_call_fails_with_clear_error():
    region = PentagonM1Region.build()
    facet_name = "L1_x"
    chart = m1_facet_charts_all(region.x, region.y)[facet_name][0]
    verts_ccw = list(M1_PENTAGON_FIXTURE.vertices)

    with pytest.raises(TypeError, match="Deprecated ambiguous call"):
        interval_endpoints_from_chart_ccw_compat(facet_name, chart, verts_ccw)


def test_interval_endpoints_wrong_geometry_region_fails_loudly():
    m1_region = PentagonM1Region.build()
    q1_region = Q1_QUADRILATERAL_FIXTURE.build_region()

    facet_name = "L1_x"
    chart = m1_facet_charts_all(m1_region.x, m1_region.y)[facet_name][0]
    verts_ccw = list(M1_PENTAGON_FIXTURE.vertices)

    with pytest.raises(KeyError, match="Unknown facet"):
        interval_endpoints_from_chart_ccw(q1_region, facet_name, chart, verts_ccw)
