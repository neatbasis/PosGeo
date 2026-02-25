import pytest
import sympy as sp

from posgeo.forms.residues2d import FacetChart, expected_interval_prefactor_from_chart_ccw, residue_2form_on_facet
from posgeo.geometry.internal_boundary_fixture import SquareHoleRegionFixture
from posgeo.geometry.region2d import Region2D
from posgeo.typing import Canonical2Form
from posgeo.validation import singularity_report


def _outer_region_from_fixture() -> Region2D:
    fixture = SquareHoleRegionFixture.build()
    return Region2D(x=fixture.x, y=fixture.y, facets=fixture.outer_facets)


def _unit_square_charts(x: sp.Symbol, y: sp.Symbol):
    _ = (x, y)
    return {
        "outer_left": [
            FacetChart("outer_left__t=y", sp.Symbol("u__ol"), sp.Symbol("t__ol"), sp.Symbol("u__ol"), sp.Symbol("t__ol"), 1)
        ],
        "outer_bottom": [
            FacetChart("outer_bottom__t=x", sp.Symbol("u__ob"), sp.Symbol("t__ob"), sp.Symbol("t__ob"), sp.Symbol("u__ob"), -1)
        ],
        "outer_right": [
            FacetChart(
                "outer_right__t=y",
                sp.Symbol("u__or"),
                sp.Symbol("t__or"),
                1 - sp.Symbol("u__or"),
                sp.Symbol("t__or"),
                -1,
            )
        ],
        "outer_top": [
            FacetChart(
                "outer_top__t=x",
                sp.Symbol("u__ot"),
                sp.Symbol("t__ot"),
                sp.Symbol("t__ot"),
                1 - sp.Symbol("u__ot"),
                1,
            )
        ],
    }


def test_singularity_report_rejects_hole_boundary_factor_for_single_loop_region():
    region = _outer_region_from_fixture()
    x, y = region.x, region.y

    synthetic = Canonical2Form(
        x=x,
        y=y,
        prefactor=1 / (x * y * (1 - x) * (1 - y) * (x - sp.Rational(2, 5))),
    )

    report = singularity_report(synthetic, region, _unit_square_charts(x, y))

    assert report.passed is False
    assert report.boundary_mapping_status is False
    assert "non-boundary-pole" in report.failure_reasons


def test_ccw_endpoint_solver_fails_when_internal_facet_is_queried_with_outer_loop_vertices_only():
    fixture = SquareHoleRegionFixture.build()
    region = Region2D(
        x=fixture.x,
        y=fixture.y,
        facets={**fixture.outer_facets, **fixture.inner_facets},
    )

    u, t = sp.symbols("u t", real=True)
    inner_left_chart = FacetChart(
        name="inner_left__t=y",
        u=u,
        t=t,
        x_of=sp.Rational(2, 5) - u,
        y_of=t,
        s=1,
    )

    with pytest.raises(ValueError, match="Expected 2 vertices on facet inner_left, got 0"):
        expected_interval_prefactor_from_chart_ccw(
            region,
            "inner_left",
            inner_left_chart,
            list(fixture.outer_vertices_ccw),
        )


def test_residue_sign_depends_on_internal_boundary_orientation_choice():
    fixture = SquareHoleRegionFixture.build()
    x, y = fixture.x, fixture.y

    form = Canonical2Form(x=x, y=y, prefactor=1 / (x * (x - sp.Rational(2, 5))))

    u, t = sp.symbols("u t", real=True)
    outer_left_chart = FacetChart("outer_left", u=u, t=t, x_of=u, y_of=t, s=1)

    # Naively reusing outer-boundary chart direction on an internal boundary.
    inner_left_reused = FacetChart(
        "inner_left_reused",
        u=u,
        t=t,
        x_of=sp.Rational(2, 5) - u,
        y_of=t,
        s=1,
    )
    # Orientation-aware chart direction that points toward the hole interior.
    inner_left_oriented = FacetChart(
        "inner_left_oriented",
        u=u,
        t=t,
        x_of=sp.Rational(2, 5) + u,
        y_of=t,
        s=1,
    )

    outer_residue = residue_2form_on_facet(form, outer_left_chart).simplify().prefactor
    reused_inner_residue = residue_2form_on_facet(form, inner_left_reused).simplify().prefactor
    oriented_inner_residue = residue_2form_on_facet(form, inner_left_oriented).simplify().prefactor

    assert reused_inner_residue == outer_residue
    assert oriented_inner_residue == -outer_residue
