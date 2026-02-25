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

# Happy Path Validation

Use this ordered checklist for a quick confidence pass:

1. Run the demo (`python -m posgeo.demos.demo_m1_pentagon`) and confirm triangulation confluence plus residue printouts (links to **TA-TC** and **TA-RR**).
2. Run `pytest` to enforce the full invariant set end-to-end (covers **TA-TC**, **TA-LP**, **TA-RR**, **TA-E3**, and **TA-VN/TA-GC**).
3. Treat a fully green run as justification that canonical-form axioms hold for the currently declared scope only (convex affine bounded 2D linear-facet geometry over exact rationals).
4. When reporting results, explicitly map outcomes to the invariant categories already listed: **TA-TC**, **TA-LP**, **TA-RR**, **TA-E3**, and **TA-VN/TA-GC**.

## Reproducibility & Supported Environments

CI is configured to run the full `pytest` suite as a required check on pinned interpreter and symbolic-algebra versions:

* Python 3.10, 3.11, and 3.12
* SymPy 1.12 and 1.13.3
* pytest 8.3.5

Local development should target Python >= 3.10 (matching `pyproject.toml`) and prefer one of the CI-pinned SymPy versions for reproducible symbolic behavior.

When debugging symbolic discrepancies, reproduce against one CI matrix tuple first (for example Python 3.11 + SymPy 1.13.3) before widening comparisons.

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

* **Chaim Even-Zohar, Tsviqa Lakrec, Ran J. Tessler(2025)**
  *The Amplituhedron BCFW Triangulation*
  [https://arxiv.org/abs/2112.02703](https://arxiv.org/abs/2112.02703)
  
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
