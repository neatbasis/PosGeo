# posgeo (Work In Proggress)

**Executable Specification of Canonical Form Axioms for a 2D Positive Geometry**

## Purpose

This repository implements a minimal, symbolic verification framework for the canonical differential form of a convex positive geometry.

The objective is not merely to compute a form, but to encode the defining axioms of canonical forms as executable invariants and verify them rigorously in a concrete example.

In its current state, the repository provides a complete structural validation of the canonical 2-form associated with a nontrivial convex pentagon (“M1 region”) in two dimensions.

The author provides no guarantees that any of this is actually true right now. 

**Consider this repository as a Draft!!!**

---

## Conceptual Framing

Canonical forms of positive geometries (cf. Arkani-Hamed et al.) are uniquely characterized by structural properties:

1. Logarithmic singularities only on boundary components
2. Absence of spurious poles
3. Residues along facets equal canonical forms of the boundary geometries
4. Triangulation independence
5. Orientation-consistent recursive factorization

This repository encodes these properties directly as symbolic tests.

The philosophy is:

> If any of these invariants fail, the form is not canonical.

Thus, the test suite serves as an executable specification of canonical form axioms in this example.

---

## Implemented Geometry: The M1 Pentagon

The region is defined by the inequalities:

* ( x > 0 )
* ( y > 0 )
* ( 1 - x > 0 )
* ( 1 - y > 0 )
* ( x + y - \tfrac{1}{2} > 0 )

Vertices (counterclockwise order):

```
(0, 1/2), (0, 1), (1, 1), (1, 0), (1/2, 0)
```

Two independent triangulations are implemented.

---

## Structural Invariants Enforced

### 1. Triangulation Confluence

The canonical form of a positive geometry must be independent of triangulation.

To enforce this invariant, the repository implements two independent triangulations of the M1 pentagon. These triangulations are not part of the geometry itself; they serve as falsifiability instruments for the construction.

We require symbolically that:

[
\Omega_A = \Omega_B
]

Equality is enforced by exact symbolic simplification and independently confirmed numerically over sampled interior points.

If the forms differed, this would indicate either:

* Failure of internal pole cancellation,
* Incorrect orientation handling,
* Or violation of canonical form axioms.

Thus, multiple triangulations are used strictly to verify structural confluence, not as competing constructions.

---

### 2. Pole Locality (No Spurious Poles)

The denominator factors of the canonical form are proven to be subsets of the boundary facet equations.

Internal triangulation poles cancel symbolically.

This ensures that the form has singularities only on geometric boundaries.

---

### 3. Residue Factorization

For each boundary facet:

* The residue of the canonical 2-form is computed.
* The result is verified to match the canonical 1-form of the corresponding interval:

[
\omega = \frac{1}{t-a} + \frac{1}{b-t}
]

This encodes the recursive defining property of canonical forms.

---

### 4. Chart-Independence

Each facet is equipped with multiple coordinate charts.

Residues computed in distinct charts are proven to agree after explicit pullback:

[
\omega(t_1) \longrightarrow \omega(t_1(t_0)) \frac{dt_1}{dt_0}
]

Degenerate constant reparameterizations are explicitly detected and rejected.

This ensures coordinate invariance of boundary structure.

---

### 5. Deterministic Orientation

Boundary orientation is fixed via:

* CCW vertex ordering
* Outward-normal detection
* Explicit sign correction

This resolves ambiguities between:

* Normal direction,
* Chart parameter direction,
* Boundary orientation.

Residues are therefore deterministic, not merely equal up to sign.

---

## Demo

Run:

```bash
python -m posgeo.demos.demo_m1_pentagon
```

The demo prints:

* Canonical form prefactors from both triangulations
* Symbolic equality check
* Residue comparisons per facet

When comparing residues, output of the form:

```
Diff: X or Y
```

means:

* If either expression simplifies to zero, the forms agree (possibly up to orientation convention).

The full deterministic sign consistency is enforced in the test suite.

---

## Test Suite

Run:

```bash
pytest
```

The test suite enforces:

* API contract stability
* Triangulation confluence (symbolic and numeric)
* Pole locality
* Residue correctness
* Chart-independence via pullback
* Deterministic orientation consistency
* Non-degenerate reparameterizations

Failure of any test indicates violation of a canonical form axiom.

---

## What This Repository Is

* A minimal executable model of canonical form axioms
* A symbolic verification laboratory
* A structural, not numerical, implementation
* A foundation for higher-dimensional generalization

---

## What It Is Not (Yet)

* Not a general polytope engine
* Not higher-dimensional
* Not amplituhedron-scale
* Not optimized for performance

The focus is structural correctness and axiomatic fidelity.

---

## Research Direction

Future extensions may include:

* Arbitrary convex polytopes
* Higher-dimensional positive geometries
* Recursive boundary factorization checks
* Automatic triangulation generation
* Extensions toward Grassmannian / amplituhedron-type geometries

---

## Summary

This repository encodes canonical form axioms as executable symbolic invariants and verifies them in a nontrivial 2D example.

It is intended as a minimal, rigorous computational laboratory for studying canonical differential forms of positive geometries.
