# posgeo

## Executable Specification of Canonical Form Axioms for a 2D Positive Geometry

---

## Project Status

* **v0.1 (current focus)** — Structural validation of canonical-form axioms in a concrete 2D example (M1 pentagon)
* **v0.2 (implemented, hardening in progress)** — Strengthened log-singularity enforcement (SingularityGate)
* **v0.3 (planned)** — Boundary-first reconstruction engine (triangulation-free solver)

---

## Purpose

This repository implements a **minimal symbolic verification framework** for the canonical differential form of a convex positive geometry.

The objective is not merely to compute a form, but to encode the defining structural axioms of canonical forms as executable invariants and verify them rigorously in a concrete example.

The current milestone (v0.1) focuses on:

* Triangulation confluence
* Pole locality
* Residue recursion
* Chart invariance
* Deterministic orientation handling

The M1 pentagon serves as a nontrivial structural testbed.

---

## Domain Contract (Explicit Scope)

All guarantees and invariants currently apply only within:

* Convex
* Affine
* 2D
* Bounded
* Linear-facet
* Exact rational arithmetic

### Not Currently Supported

* Unbounded or projective geometries
* Nonlinear boundary curves
* Higher-dimensional geometries
* Non-logarithmic singularities
* Floating-point validation

Any extension beyond this domain requires explicit revision of assumptions and invariants.

### What this does NOT prove

* It does **not** claim universality beyond the convex affine 2D linear-facet domain stated above.
* It does **not** provide guarantees for projective, nonlinear-boundary, or higher-dimensional geometries.
* It does **not** yet provide triangulation-free reconstruction; v0.3 is planned and not shipped.
* It does **not** replace formal proofs in the cited positive-geometry literature.

---

# Conceptual Framing

Canonical forms of positive geometries (cf. Arkani-Hamed–Bai–Lam) are uniquely characterized by structural properties:

1. Logarithmic singularities only on boundary components
2. Absence of spurious poles
3. Residues along facets equal canonical forms of boundary geometries
4. Triangulation independence
5. Orientation-consistent recursive factorization

This repository encodes these properties directly as symbolic tests.

> If any of these invariants fail, the form is not canonical.

Thus, the test suite functions as an executable specification of canonical-form axioms in this example.

---

# Implemented Geometry: The M1 Pentagon

The region is defined by the inequalities:

* ( x > 0 )
* ( y > 0 )
* ( 1 - x > 0 )
* ( 1 - y > 0 )
* ( x + y - \tfrac{1}{2} > 0 )

Vertices (counterclockwise order):

```id="m1-vertices"
(0, 1/2)
(0, 1)
(1, 1)
(1, 0)
(1/2, 0)
```

Two independent triangulations are implemented.

These triangulations are not part of the geometry itself; they serve as falsifiability instruments for structural validation.

---

# Structural Invariants Enforced (v0.1)

## 1. Triangulation Confluence

The canonical form must be independent of triangulation.

Symbolically:

[
\Omega_A = \Omega_B
]

Equality is enforced via exact symbolic simplification and independently confirmed numerically over interior sample points.

A mismatch would indicate:

* Failure of internal pole cancellation
* Incorrect orientation handling
* Violation of canonical-form axioms

Triangulation is used strictly as a regression instrument, not as the definition of canonical form.

---

## 2. Pole Locality (No Spurious Poles)

The denominator factors of the canonical form must correspond to boundary facet equations.

Internal triangulation poles cancel symbolically.

This ensures singularities occur only on geometric boundaries.

---

## 3. Residue Factorization

For each boundary facet:

* The residue of the canonical 2-form is computed.
* It must match the canonical 1-form of the corresponding interval:

[
\omega = \frac{1}{t-a} + \frac{1}{b-t}
]

This encodes recursive boundary structure.

---

## 4. Chart-Independence

Each facet is equipped with multiple coordinate charts.

Residues computed in distinct charts must agree after explicit pullback:

[
\omega(t_1) \longrightarrow \omega(t_1(t_0)) \frac{dt_1}{dt_0}
]

Degenerate constant reparameterizations are detected and rejected.

This enforces coordinate invariance of boundary structure.

---

## 5. Deterministic Orientation

Boundary orientation is fixed via:

* CCW vertex ordering
* Outward-normal detection
* Explicit sign correction

Residues are therefore deterministic, not merely equal up to sign.

---

# Demo

Run:

```bash id="demo-run"
python -m posgeo.demos.demo_m1_pentagon
```

The demo prints:

* Canonical form prefactors from both triangulations
* Symbolic equality check
* Residue comparisons per facet

Short interpretation guide:

* `Simplify(A-B): 0` is the confluence success condition.
* For each facet, residue comparison is valid if either `res - expected == 0` or `res + expected == 0`.
* Sign differences can arise from chart orientation conventions and are checked more strictly in tests.
* Authoritative orientation checks live in `tests/test_m1_residues.py` and `tests/test_m1_orientation_consistency.py`.

---

# Test Suite

Run:

```bash id="test-run"
pytest
```

The test suite enforces:

* API contract stability
* Triangulation confluence (symbolic and numeric)
* Pole locality
* Residue correctness
* Chart-independence
* Deterministic orientation
* Non-degenerate reparameterizations

Failure of any test indicates violation of canonical-form axioms within the declared domain.

## Implementation Map

* `posgeo/forms/canonical2d.py` — triangulation and canonical-form assembly.
* `posgeo/forms/residues2d.py` — facet charts, residues, and reparameterization helpers.
* `posgeo/validation/preconditions.py` — scope gating.
* `posgeo/validation/singularity_gate.py` — log-purity gate/report.
* `tests/AXIOM_TRACEABILITY.md` — axiom-to-test mapping.

# Happy Path Validation

Use this ordered checklist for a quick confidence pass:

1. Run the demo (`python -m posgeo.demos.demo_m1_pentagon`) and confirm triangulation confluence plus residue printouts (links to **TA-TC** and **TA-RR**).
2. Run `pytest` to enforce the full invariant set end-to-end (covers **TA-TC**, **TA-LP**, **TA-RR**, **TA-E3**, and **TA-VN/TA-GC**).
3. Treat a fully green run as justification that canonical-form axioms hold for the currently declared scope only (convex affine bounded 2D linear-facet geometry over exact rationals).
4. When reporting results, explicitly map outcomes to the invariant categories already listed: **TA-TC**, **TA-LP**, **TA-RR**, **TA-E3**, and **TA-VN/TA-GC**.

## Reproducibility & Supported Environments

### Reproducibility

Recommended baseline tuple for bug reports and local verification: **Python 3.11 + SymPy 1.13.3**.

From the repository root, a minimal setup and verification flow is:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e . sympy==1.13.3 pytest==8.3.5
python -m posgeo.demos.demo_m1_pentagon
pytest
```

Symbolic simplification and expression forms can vary across Python/SymPy versions, so equivalent mathematics may print differently. The CI matrix is the source of truth for supported combinations and expected pass/fail behavior.

Canonical dependency references:

* `pyproject.toml` for project-level Python/dependency constraints.
* `.github/workflows/ci.yml.disabled` for the tested matrix tuple definitions.

---

# Upcoming Work

## v0.2 — Strengthened Log-Singularity Enforcement

### Already shipped

The v0.2 SingularityGate path is present and exercised in tests via:

* `posgeo.validation.singularity_gate`
* `assert_log_pure`
* `singularity_report`

Current behavior (as validated in `tests/test_m1_simple_poles_only.py`) already includes:

* Explicit detection of non-simple pole multiplicities
* Local chart-order checks for second-order behavior
* Machine-readable failure reasons for log-purity failures

### Remaining hardening work

Ongoing v0.2 hardening focuses on expanding coverage and robustness, including:

* Broader stress cases beyond the current M1 workflows
* Additional diagnostics and reporting ergonomics for failing chart checks
* Further tightening of coordinate-invariant validation paths

This continues the shift from denominator-only heuristics toward definition-level log-singularity enforcement.

---

## v0.3 — Boundary Reconstruction Engine

Longer-term goals include:

* Constraint-based canonical-form construction
* Triangulation-free solver
* Using log-purity validation as a termination oracle

---

# What This Repository Is

* A minimal executable model of canonical-form axioms
* A symbolic verification laboratory
* A structural (not numerical) implementation
* A foundation for higher-dimensional generalization

---

# What It Is Not (Yet)

* Not a general polytope engine
* Not higher-dimensional
* Not amplituhedron-scale
* Not optimized for performance
* Not a general existence proof

The focus is structural correctness and axiomatic fidelity.

---

# Research Direction

Future extensions may include:

* Arbitrary convex polytopes
* Higher-dimensional positive geometries
* Recursive boundary factorization checks
* Automatic triangulation generation
* Extensions toward Grassmannian / amplituhedron-type geometries

The long-term aim is to treat canonical-form axioms as executable contracts.

---

# 📚 Foundational Papers & Articles

This project builds on the development of **positive geometry**, the **amplituhedron**, and related structures connecting combinatorics, geometry, and scattering amplitudes.

---

## 🔷 The Amplituhedron

* **N. Arkani-Hamed, J. Trnka (2013)**
  *The Amplituhedron*
  [https://arxiv.org/abs/1312.2007](https://arxiv.org/abs/1312.2007)

* **N. Arkani-Hamed, J. Trnka (2014)**
  *Into the Amplituhedron*
  [https://arxiv.org/abs/1312.7878](https://arxiv.org/abs/1312.7878)

---

## 🔷 Positive Grassmannian & Plabic Graphs

* **A. Postnikov (2006)**
  *Total Positivity, Grassmannians, and Networks*
  [https://arxiv.org/abs/math/0609764](https://arxiv.org/abs/math/0609764)

* **N. Arkani-Hamed et al. (2016)**
  *Scattering Amplitudes and the Positive Grassmannian*
  [https://arxiv.org/abs/1212.5605](https://arxiv.org/abs/1212.5605)

---

## 🔷 Associahedron & ABHY Construction

* **N. Arkani-Hamed, Y. Bai, S. He, G. Yan (2017)**
  *Scattering Forms and the Positive Geometry of Kinematics, Color and the Worldsheet*
  [https://arxiv.org/abs/1711.09102](https://arxiv.org/abs/1711.09102)

* **N. Arkani-Hamed, Y. Bai, S. He (2017)**
  *The All-Loop Integrand for Scattering Amplitudes in Planar N=4 SYM*
  [https://arxiv.org/abs/1008.2958](https://arxiv.org/abs/1008.2958)
  Explores recursive and geometric structures underlying amplitude factorization.

---

## 🔷 Canonical Forms & Positive Geometry

* **N. Arkani-Hamed, Y. Bai, T. Lam (2017)**
  *Positive Geometries and Canonical Forms*
  [https://arxiv.org/abs/1703.04541](https://arxiv.org/abs/1703.04541)

* **SAGEX Review (2022)**
  *Scattering Amplitudes and Positive Geometry*
  [https://arxiv.org/abs/2203.13018](https://arxiv.org/abs/2203.13018)

---

## 🔷 Origami & Momentum Amplituhedron

* **P. Galashin (2024)**
  *Amplituhedra and origami*
  [https://arxiv.org/abs/2410.09574](https://arxiv.org/abs/2410.09574)

* **Kevin Hartnett (2025)**
  *Origami Patterns Solve a Major Physics Riddle*
  [https://www.quantamagazine.org/origami-patterns-solve-a-major-physics-riddle-20251006/](https://www.quantamagazine.org/origami-patterns-solve-a-major-physics-riddle-20251006/)

* **Jordana Cepelewicz (2024)**
  *How to Build an Origami Computer* (NOTE: This seems highly relevant, )
  [https://www.quantamagazine.org/how-to-build-an-origami-computer-20240130/](https://www.quantamagazine.org/how-to-build-an-origami-computer-20240130/)
  
## 🔷 Others

* **Chaim Even-Zohar, Tsviqa Lakrec, Ran J. Tessler (2025)**
  *The Amplituhedron BCFW Triangulation*
  [https://arxiv.org/abs/2112.02703](https://arxiv.org/abs/2112.02703)
  
* **Benincasa, Paolo and Parisi, Matteo (2020)**
  *Positive Geometries and Differential Forms with Non-Logarithmic Singularities I*
  [https://arxiv.org/abs/2005.03612](https://arxiv.org/abs/2005.03612)
  
* **Gabriele Dian, Elia Mazzucchelli, Felix Tellander (2025)**
  *The two-loop Amplituhedron*
  [https://arxiv.org/abs/2410.11501](https://arxiv.org/abs/2410.11501)
  
* **Nima Arkani-Hamed, Cameron Langer, Akshay Yelleshpur Srikant, and Jaroslav Trnka (2019)**
  *Deep Into the Amplituhedron: Amplitude Singularities at All Loops and Legs*
  [https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.051601](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.051601)

## How sources map to this implementation

| Source | What theorem/claim is used here | Status in repo | Where enforced |
|---|---|---|---|
| Arkani-Hamed, Bai, Lam (2017), [1703.04541](https://arxiv.org/abs/1703.04541) | Canonical-form axiom basis for log-purity, residue recursion, no-spurious-pole boundary visibility, and triangulation confluence. | implemented | `TA-LP`, `TA-RR`, `TA-VN`, `TA-TC` in `AXIOMS.md`; executable checks in `tests/test_m1_simple_poles_only.py`, `tests/test_m1_residues.py`, `tests/test_m1_pole_locality.py`, `tests/test_m1_confluence.py`, and `tests/AXIOM_TRACEABILITY.md`. |
| Benincasa–Parisi (2020), [2005.03612](https://arxiv.org/abs/2005.03612) | Non-logarithmic singularity regimes are treated as outside the current validator contract. | out of scope | Declared as limitation in `README.md` scope clauses (“Non-logarithmic singularities” not supported) and tied to `TA-LP` scope caveats in `AXIOMS.md`. |
| Dian–Mazzucchelli–Tellander (2025), [2410.11501](https://arxiv.org/abs/2410.11501) | Two-loop amplituhedron weighted/internal-boundary machinery is acknowledged as beyond the convex affine 2D polygon implementation. | out of scope | Captured by `README.md` exclusions (“Not amplituhedron-scale”, no higher-dimensional/projective support) and `TA-LP`/`TA-VN` scope caveats in `AXIOMS.md`. |
| Arkani-Hamed et al., PRL 122.051601 (2019) | Conceptual motivation for loop-level amplituhedron singularity structure only; not used as an executable gate in this codebase. | partial | Referenced in literature context only; no dedicated axiom ID or direct test gate beyond the existing `TA-*` registry and `tests/AXIOM_TRACEABILITY.md` contract. |
  
## 🔷 Scattering Amplitude Methods (Pre-Amplituhedron Foundations)

* **Britto, Cachazo, Feng, Witten (2005)**
  *Direct Proof of Tree-Level Recursion Relation in Yang-Mills Theory*
  [https://arxiv.org/abs/hep-th/0501052](https://arxiv.org/abs/hep-th/0501052)
  Introduces BCFW recursion, a precursor to geometric interpretations.

* **Parke, Taylor (1986)**
  *An Amplitude for n Gluon Scattering*
  [https://doi.org/10.1103/PhysRevLett.56.2459](https://doi.org/10.1103/PhysRevLett.56.2459)
  Early indication that scattering amplitudes admit unexpectedly simple closed forms.
  
* **Sugimoto, Teruhisa (2025)**
  *Convex pentagonal monotiles in the 15 Type families*
  [https://arxiv.org/abs/2501.07090v1](https://arxiv.org/abs/2501.07090v1)
  
* **Wolchover, Natalie (2017)**
  *Pentagon Tiling Proof Solves Century-Old Math Problem*
  [https://www.quantamagazine.org/pentagon-tiling-proof-solves-century-old-math-problem-20170711/](https://www.quantamagazine.org/pentagon-tiling-proof-solves-century-old-math-problem-20170711/)
---

# 🧭 Conceptual Themes

* Geometry replaces diagrammatic enumeration
* Canonical forms are fixed by boundary structure
* Positivity encodes physical consistency
* Factorization corresponds to geometric boundaries
* Combinatorics ↔ geometry ↔ physics equivalence
* Constraint-defined systems over rule-defined systems

---

## Summary

`posgeo` encodes canonical-form axioms as executable symbolic invariants and validates them in a nontrivial 2D example.

The current focus (v0.1) is structural validation.

Future milestones strengthen singularity enforcement and enable boundary-driven construction.

Validation precedes automation.
