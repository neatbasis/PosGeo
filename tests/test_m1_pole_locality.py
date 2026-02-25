from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from tests.helpers.pole_checks import assert_boundary_subset, normalized_denominator_factors


def test_only_boundary_poles_in_final_form():
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    factors = normalized_denominator_factors(omega.prefactor, x, y)

    # Expect: final form has poles only on boundary lines (internal triangulation poles cancel)
    assert_boundary_subset(factors, [f.expr for f in region.facets.values()], x, y)
