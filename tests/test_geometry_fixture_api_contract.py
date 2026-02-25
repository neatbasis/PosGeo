import pytest
import sympy as sp

from posgeo.forms.canonical2d import Triangulation2D, canonical_form_from_triangulation
from posgeo.forms.residues2d import FacetChart, residue_2form_on_facet
from posgeo.geometry import FIXTURES2D
from posgeo.geometry.region2d import Region2D
from tests.helpers.geometry_cases import GEOMETRY_CASES


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_geometry_case_maps_to_product_fixture_contract(geometry_case):
    assert geometry_case.name in FIXTURES2D

    region = geometry_case.build_region()
    assert isinstance(region, Region2D)

    fixture = FIXTURES2D[geometry_case.name]
    assert tuple(geometry_case.vertices()) == fixture.vertices
    assert set(region.facets.keys()) == {name for name, _ in fixture.facet_equations}


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_geometry_case_triangulation_contract(geometry_case):
    region = geometry_case.build_region()
    vertices = geometry_case.vertices()

    tri_a = geometry_case.tri_a(region.x, region.y)
    tri_b = geometry_case.tri_b(region.x, region.y)

    assert isinstance(tri_a, Triangulation2D)
    assert isinstance(tri_b, Triangulation2D)

    omega_a = canonical_form_from_triangulation(tri_a, region=region, vertices=vertices).simplify()
    omega_b = canonical_form_from_triangulation(tri_b, region=region, vertices=vertices).simplify()

    assert omega_a.x == region.x and omega_a.y == region.y
    assert omega_b.x == region.x and omega_b.y == region.y


@pytest.mark.parametrize("geometry_case", GEOMETRY_CASES, ids=lambda c: c.name)
def test_geometry_case_facet_chart_contract(geometry_case):
    region = geometry_case.build_region()
    omega = canonical_form_from_triangulation(
        geometry_case.tri_a(region.x, region.y),
        region=region,
        vertices=geometry_case.vertices(),
    ).simplify()

    charts_by_facet = geometry_case.facet_charts(region.x, region.y)
    assert set(charts_by_facet.keys()) == set(region.facets.keys())

    for facet_name, charts in charts_by_facet.items():
        assert isinstance(charts, list) and len(charts) >= 2
        for chart in charts:
            assert isinstance(chart, FacetChart)
            residue = residue_2form_on_facet(omega, chart).simplify()
            assert residue.t == chart.t
            assert not residue.prefactor.has(sp.nan)
            assert not residue.prefactor.has(sp.zoo)
            assert residue.prefactor is not sp.oo and residue.prefactor is not -sp.oo
            assert facet_name in region.facets
