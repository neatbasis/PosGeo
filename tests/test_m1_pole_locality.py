# Axioms: TA-LP, TA-GC

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import canonical_form_from_triangulation, triangulation_A_m1
from tests.helpers.pole_checks import assert_boundary_pole_invariant


def test_only_boundary_poles_in_final_form():
    """Axiom IDs: TA-VN, TA-GC. Test type: structural."""
    region = PentagonM1Region.build()
    x, y = region.x, region.y
    omega = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()

    # Expect: final form has poles only on boundary lines (internal triangulation poles cancel).
    assert_boundary_pole_invariant(
        omega.prefactor,
        [f.expr for f in region.facets.values()],
        x,
        y,
        require_simple_poles=True,
    )
