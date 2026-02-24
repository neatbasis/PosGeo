import sympy as sp
from posgeo.forms.residues2d import m1_facet_charts_all

def test_m1_facet_charts_all_returns_dict():
    x,y = sp.symbols("x y", real=True)
    charts = m1_facet_charts_all(x,y)
    assert isinstance(charts, dict)
    assert all(isinstance(v, list) and len(v) >= 1 for v in charts.values())
