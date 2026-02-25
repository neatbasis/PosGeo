from pathlib import Path

from scripts import fixture_guardrail_check


def test_guardrail_passes_for_current_helpers():
    violations = fixture_guardrail_check.run_guardrail(Path("tests/helpers"))
    assert violations == []


def test_guardrail_flags_local_region_constructor(tmp_path):
    helper = tmp_path / "bad_helper.py"
    helper.write_text(
        """
from posgeo.geometry.region2d import Region2D

def build_region() -> Region2D:
    return Region2D(x=None, y=None, facets={})
""".strip()
        + "\n",
        encoding="utf-8",
    )

    violations = fixture_guardrail_check.find_violations(helper)

    assert any("return annotation uses `Region2D`" in item for item in violations)
    assert any("constructs `Region2D(...)`" in item for item in violations)


def test_guardrail_flags_local_facet_chart_constructor(tmp_path):
    helper = tmp_path / "bad_chart_helper.py"
    helper.write_text(
        """
from posgeo.forms.residues2d import FacetChart

def make_chart():
    return FacetChart(name='f', facet_name='f', u=None, t=None, x_of=None, y_of=None)
""".strip()
        + "\n",
        encoding="utf-8",
    )

    violations = fixture_guardrail_check.find_violations(helper)

    assert any("constructs `FacetChart(...)`" in item for item in violations)
