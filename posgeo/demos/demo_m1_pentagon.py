from __future__ import annotations

import sympy as sp

from posgeo.geometry.region2d import PentagonM1Region
from posgeo.forms.canonical2d import (
    canonical_form_from_triangulation,
    triangulation_A_m1,
    triangulation_B_m1,
)
from posgeo.forms.residues2d import (
    m1_facet_charts_all,
    residue_2form_on_facet,
    expected_interval_prefactor_for_m1_facet,
)


def main() -> None:
    region = PentagonM1Region.build()
    x, y = region.x, region.y

    omegaA = canonical_form_from_triangulation(triangulation_A_m1(x, y)).simplify()
    omegaB = canonical_form_from_triangulation(triangulation_B_m1(x, y)).simplify()

    print("OmegaA prefactor:", omegaA.prefactor)
    print("OmegaB prefactor:", omegaB.prefactor)
    print("Simplify(A-B):", sp.simplify(omegaA.prefactor - omegaB.prefactor))

    charts = {k: v[0] for k, v in m1_facet_charts_all(x, y).items()}
    for name, chart in charts.items():
        res = residue_2form_on_facet(omegaA, chart).simplify()
        exp = expected_interval_prefactor_for_m1_facet(name, res.t)
        print(f"\nFacet {name}")
        print("Residue prefactor:", res.prefactor)
        print("Expected:", exp)
        print("Diff:", sp.simplify(res.prefactor - exp), "or", sp.simplify(res.prefactor + exp))


if __name__ == "__main__":
    main()
