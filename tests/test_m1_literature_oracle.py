"""Literature-backed regression oracle for the M1 canonical prefactor.

Reference source and normalization are documented in ``AXIOMS.md``
(Appendix A, "M1 Pentagon Closed-Form Oracle"). The form is normalized with
counterclockwise vertex order and ambient orientation ``dx ∧ dy``.
"""

import sympy as sp

from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    triangulation_B_m1,
)


def _m1_closed_form_reference(x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    """Independently encoded closed form for the M1 pentagon prefactor."""
    return -(x * y + x + y) / (
        x * y * (x - 1) * (y - 1) * (2 * x + 2 * y - 1)
    )


def test_m1_prefactor_matches_closed_form_oracle() -> None:
    x, y = sp.symbols("x y", real=True)

    reference = _m1_closed_form_reference(x, y)
    engine_a = canonical_form_from_triangulation(triangulation_A_m1(x, y)).prefactor
    engine_b = canonical_form_from_triangulation(triangulation_B_m1(x, y)).prefactor

    assert sp.simplify(engine_a - reference) == 0
    assert sp.simplify(engine_b - reference) == 0


def test_m1_prefactor_rational_spot_checks() -> None:
    x, y = sp.symbols("x y", real=True)

    reference = _m1_closed_form_reference(x, y)
    engine = canonical_form_from_triangulation(triangulation_A_m1(x, y)).prefactor

    test_points = (
        (sp.Rational(3, 5), sp.Rational(2, 5)),
        (sp.Rational(4, 5), sp.Rational(3, 5)),
        (sp.Rational(7, 10), sp.Rational(1, 5)),
    )
    for x0, y0 in test_points:
        e_val = sp.simplify(engine.subs({x: x0, y: y0}))
        r_val = sp.simplify(reference.subs({x: x0, y: y0}))
        assert e_val == r_val

