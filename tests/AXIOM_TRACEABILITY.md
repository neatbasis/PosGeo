# Test Axiom Traceability

This lightweight metadata layer maps normalized axiom IDs in `AXIOMS.md` to concrete executable checks.

## Axiom → Tests

- **TA-LP**
  - `tests/test_m1_pole_locality.py::test_only_boundary_poles_in_final_form`
  - `tests/test_m1_simple_poles_only.py::test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits`

- **TA-GC**
  - `tests/test_m1_pole_locality.py::test_only_boundary_poles_in_final_form`
  - `tests/test_m1_simple_poles_only.py::test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits`

- **TA-RR**
  - `tests/test_m1_residues.py::test_residues_match_interval_forms_up_to_sign`
  - `tests/test_m1_residues.py::test_residues_match_interval_forms_deterministic_sign`
  - `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_deterministic_sign`
  - `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_up_to_pullback_and_sign`
  - `tests/test_m1_vertex_residues.py::test_m1_terminal_residue_chains_2d_to_vertex_are_pm_one`

- **TA-VN**
  - `tests/test_m1_residues.py::test_residues_match_interval_forms_up_to_sign`
  - `tests/test_m1_residues.py::test_residues_match_interval_forms_deterministic_sign`
  - `tests/test_m1_vertex_residues.py::test_m1_vertex_endpoint_residues_orientation_free_are_pm_one`
  - `tests/test_m1_vertex_residues.py::test_m1_vertex_endpoint_residues_ccw_fixed_are_plus_one`

- **TA-TC**
  - `tests/test_m1_confluence.py::test_triangulation_confluence_symbolic`
  - `tests/test_m1_confluence.py::test_triangulation_confluence_exact_rational_regression`

- **TA-E1**
  - `tests/test_m1_confluence.py::test_triangulation_confluence_symbolic`
  - `tests/test_m1_confluence.py::test_triangulation_confluence_exact_rational_regression`
