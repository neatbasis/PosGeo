import sympy as sp
import pytest

from posgeo.forms.residues2d import (
    FacetChart,
    expected_interval_prefactor_from_chart_ccw,
    residue_2form_on_facet,
)
from posgeo.geometry.internal_boundary_fixture import SquareHoleRegionFixture
from posgeo.geometry.region2d import Region2D
from posgeo.typing import Canonical2Form
from posgeo.validation.singularity_gate import singularity_report


def _inner_left_facet_chart(x: sp.Symbol, y: sp.Symbol) -> FacetChart:
    u = sp.Symbol("u__inner_left", real=True)
    t = sp.Symbol("t__inner_left", real=True)
    return FacetChart(
        name="I_L__t=y",
        u=u,
        t=t,
        x_of=sp.Rational(1, 3) + u,
        y_of=t,
        s=sp.Integer(1),
    )


def _inner_bottom_facet_chart(x: sp.Symbol, y: sp.Symbol) -> FacetChart:
    u = sp.Symbol("u__inner_bottom", real=True)
    t = sp.Symbol("t__inner_bottom", real=True)
    return FacetChart(
        name="I_B__t=x",
        u=u,
        t=t,
        x_of=t,
        y_of=sp.Rational(1, 3) + u,
        s=sp.Integer(-1),
    )


def test_ta_vn_ta_gc_boundary_mapping_flags_inner_component_as_non_boundary_under_single_component_model():
    """Axiom IDs: TA-VN, TA-GC. Test type: failure-mode.

    Existing denominator-to-boundary matching only inspects `region.facets`.
    For a region with a hole, inner-component boundary factors are real boundaries
    but are incorrectly marked as non-boundary if only the enclosing component is supplied.
    """
    fixture = SquareHoleRegionFixture.build()
    x, y = fixture.x, fixture.y

    charts = {"I_L": [_inner_left_facet_chart(x, y)]}
    form = Canonical2Form(
        x=x,
        y=y,
        prefactor=1 / ((x - sp.Rational(1, 3)) * (y - sp.Rational(1, 3)) * (sp.Rational(2, 3) - y)),
    )

    report = singularity_report(form, fixture.enclosing_region, charts)

    assert report.boundary_mapping_status is False
    assert "non-boundary-pole" in report.failure_reasons


def test_orientation_deterministic_ccw_endpoint_solver_fails_for_flattened_two_component_boundary():
    """Axiom IDs: TA-E3. Test type: failure-mode.

    Deterministic orientation utilities assume one CCW boundary loop with adjacent
    facet endpoints in a single cyclic list; this fails for inner boundary components.
    """
    fixture = SquareHoleRegionFixture.build()
    x, y = fixture.x, fixture.y
    chart = _inner_bottom_facet_chart(x, y)

    pseudo_region = Region2D(
        x=x,
        y=y,
        facets={**fixture.enclosing_region.facets, "I_B": fixture.all_boundary_facets["I_B"]},
    )

    with pytest.raises(ValueError, match="not adjacent in CCW order"):
        expected_interval_prefactor_from_chart_ccw(
            pseudo_region,
            "I_B",
            chart,
            list(fixture.flattened_vertices_assuming_single_ccw_loop),
        )


def test_boundary_strata_residue_recursion_requires_component_specific_orientation_signs():
    """Axiom IDs: TA-RR. Test type: failure-mode.

    Inner-loop terminal residues remain non-zero but violate the deterministic
    outer-loop convention (+1 at both oriented endpoints).
    """
    fixture = SquareHoleRegionFixture.build()
    x, y = fixture.x, fixture.y
    chart = _inner_left_facet_chart(x, y)

    form = Canonical2Form(
        x=x,
        y=y,
        prefactor=1 / ((x - sp.Rational(1, 3)) * (y - sp.Rational(1, 3)) * (sp.Rational(2, 3) - y)),
    )
    res = residue_2form_on_facet(form, chart).simplify()

    t = res.t
    ts = sp.Rational(1, 3)
    te = sp.Rational(2, 3)

    r_start_ccw = sp.simplify(sp.limit(-(t - ts) * res.prefactor, t, ts))
    r_end_ccw = sp.simplify(sp.limit((t - te) * res.prefactor, t, te))

    assert r_start_ccw != 0
    assert r_end_ccw != 0
    assert r_start_ccw != 1 or r_end_ccw != 1
