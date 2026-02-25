# Axiom Traceability Matrix

This artifact maps normalized axiom IDs in `AXIOMS.md` to executable tests, and records the exact falsification criteria that those tests are designed to trigger.

## Scope and policy

- **Mandatory axioms in this repository:** `TA-LP`, `TA-RR`, `TA-VN`, `TA-E1`, `TA-E3`, `TA-GC`, `TA-TC`.
- Every mandatory axiom must have:
  - at least one **structural** test (positive invariant check), and
  - at least one **failure-mode** test (condition that would fail on known drift modes).
- Test functions encode this metadata in their docstrings via:
  - `Axiom IDs: ...`
  - `Test type: structural|failure-mode`

## Formal condition traceability

| Axiom ID | Formal condition summary | Exact falsification criteria (from `AXIOMS.md`) | Structural tests | Failure-mode tests |
|---|---|---|---|---|
| `TA-LP` | Log-purity: only simple poles on true boundary strata, including vertex-local checks. | Fails iff a boundary-aligned factor has multiplicity `>= 2`, or vertex-local restriction reveals higher-order behavior, or a singularity appears away from the true boundary set. | `tests/test_m1_simple_poles_only.py::test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits` ; `tests/test_m1_vertex_residues.py::test_m1_vertex_endpoint_residues_orientation_free_are_pm_one` | `tests/test_m1_vertex_residues.py::test_m1_vertex_endpoint_residues_ccw_fixed_are_plus_one` |
| `TA-RR` | Recursive residues agree with boundary canonical forms up to orientation convention. | Fails iff some true facet has `simplify(Res_F(Ω)-Ω(F)) != 0` after orientation normalization. | `tests/test_m1_residues.py::test_residues_orientation_agnostic_structural_layer` ; `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_orientation_agnostic_structural` ; `tests/test_m1_orientation_consistency.py::test_orientation_consistency_structural_up_to_sign` ; `tests/test_m1_vertex_residues.py::test_m1_terminal_residue_chains_2d_to_vertex_are_pm_one` | `tests/test_m1_residues.py::test_residues_orientation_fixed_deterministic_layer` ; `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_orientation_fixed_deterministic` ; `tests/test_m1_orientation_consistency.py::test_orientation_consistency_deterministic_fixed_sign` ; `tests/test_m1_vertex_residues.py::test_m1_vertex_endpoint_residues_ccw_fixed_are_plus_one` |
| `TA-VN` | Final-form pole set is a subset of true boundary components only. | Fails iff an irreducible denominator factor remains after global simplification and cannot be mapped to any true boundary component. | `tests/test_m1_pole_locality.py::test_only_boundary_poles_in_final_form` | `tests/test_m1_residues.py::test_residues_orientation_fixed_deterministic_layer` |
| `TA-E1` | Certification path uses exact symbolic rationals, not floating semantics. | Fails iff certification depends on floating coefficients or approximate numeric comparison instead of exact symbolic equality. | `tests/test_m1_confluence.py::test_triangulation_confluence_symbolic` | `tests/test_m1_confluence.py::test_triangulation_confluence_exact_rational_regression` |
| `TA-E3` | Residue operator is deterministic across admissible charts (modulo orientation sign). | Fails iff two admissible chart residues for the same boundary disagree beyond allowed orientation sign. | `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_orientation_agnostic_structural` ; `tests/test_m1_orientation_consistency.py::test_orientation_consistency_structural_up_to_sign` | `tests/test_m1_residues_chart_independence.py::test_residue_chart_independence_orientation_fixed_deterministic` ; `tests/test_m1_orientation_consistency.py::test_orientation_consistency_deterministic_fixed_sign` ; `tests/test_reparam_nonconstant.py::test_reparam_is_not_constant_for_all_m1_chart_pairs` |
| `TA-GC` | Global confluence/cancellation removes non-boundary poles only after whole-expression simplification. | Fails iff whole-expression simplification leaves any non-boundary pole in the final form. | `tests/test_m1_pole_locality.py::test_only_boundary_poles_in_final_form` | `tests/test_m1_simple_poles_only.py::test_m1_final_form_has_only_simple_boundary_poles_and_chart_order_one_limits` |
| `TA-TC` | Triangulation confluence: valid triangulations yield symbolically identical canonical forms. | Fails iff there exists a valid triangulation pair whose globally simplified difference is nonzero. | `tests/test_m1_confluence.py::test_triangulation_confluence_symbolic` | `tests/test_m1_confluence.py::test_triangulation_confluence_exact_rational_regression` |

## Coverage enforcement

`tests/test_axiom_traceability_contract.py` enforces that every mandatory axiom above has both structural and failure-mode tests as declared in test docstrings.

## Multi-geometry coverage

- Canonical invariant tests for confluence and residue/chart behavior are parametrized across multiple convex polygon fixtures via `tests/helpers/geometry_cases.py` (currently `m1_pentagon` and `q1_quadrilateral`).
- This extends the same axiom checks beyond the original M1 pentagon while preserving exact symbolic criteria and failure modes.
