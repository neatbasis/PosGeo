import sympy as sp

_INVALID_SYMBOLIC_VALUES = {sp.nan, sp.zoo, sp.oo, -sp.oo}


def is_invalid_symbolic_value(value: sp.Expr) -> bool:
    """Return True when ``value`` simplifies to a symbolic non-finite sentinel."""
    simplified = sp.simplify(value)
    return simplified in _INVALID_SYMBOLIC_VALUES


def assert_valid_symbolic_value(value: sp.Expr, *, context: str, quantity: str = "value") -> sp.Expr:
    """Assert ``value`` is not one of SymPy's invalid non-finite sentinels.

    Returns the simplified value for convenient downstream checks.
    """
    simplified = sp.simplify(value)
    assert simplified not in _INVALID_SYMBOLIC_VALUES, (
        f"{context}: invalid symbolic {quantity}: {simplified}"
    )
    return simplified
