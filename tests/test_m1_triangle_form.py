import sympy as sp

from posgeo.forms.simplex2d import Triangle2D
from posgeo.geometry.region2d import Region2D
from posgeo.validation import singularity_report


def test_triangle_form_has_only_simple_edge_poles():
    x, y = sp.symbols("x y", real=True)
    tri = Triangle2D.from_vertices(x, y, (sp.Rational(0), sp.Rational(0)),
                                   (sp.Rational(1), sp.Rational(0)),
                                   (sp.Rational(0), sp.Rational(1)))
    omega = tri.canonical_form()

    region = Region2D(
        x=x,
        y=y,
        facets={f"edge_{idx}": edge for idx, edge in enumerate(tri.edges)},
    )

    report = singularity_report(omega, region, charts={})

    assert report.passed is True
    assert report.boundary_mapping_status is True
    assert report.detected_pole_loci
    assert all(multiplicity == 1 for _, multiplicity in report.multiplicities)
