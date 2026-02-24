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


---

# 📚 Foundational Papers & Articles

This project is inspired by the development of **positive geometry**, the **amplituhedron**, and related structures connecting combinatorics, geometry, and scattering amplitudes.

---

## 🔷 The Amplituhedron

* **N. Arkani-Hamed, J. Trnka (2013)**
  *The Amplituhedron*
  [https://arxiv.org/abs/1312.2007](https://arxiv.org/abs/1312.2007)
  Introduces the amplituhedron as a geometric object whose canonical form computes scattering amplitudes in planar N=4 SYM.

* **N. Arkani-Hamed, J. Trnka (2014)**
  *Into the Amplituhedron*
  [https://arxiv.org/abs/1312.7878](https://arxiv.org/abs/1312.7878)
  Develops geometric and combinatorial aspects of the amplituhedron construction.

---

## 🔷 Positive Grassmannian & Plabic Graphs

* **A. Postnikov (2006)**
  *Total Positivity, Grassmannians, and Networks*
  [https://arxiv.org/abs/math/0609764](https://arxiv.org/abs/math/0609764)
  Introduces plabic graphs and the combinatorial structure of the positive Grassmannian.

* **N. Arkani-Hamed et al. (2016)**
  *Scattering Amplitudes and the Positive Grassmannian*
  [https://arxiv.org/abs/1212.5605](https://arxiv.org/abs/1212.5605)
  Establishes the deep connection between scattering amplitudes and positive geometry.

---

## 🔷 Associahedron & ABHY Construction

* **N. Arkani-Hamed, Y. Bai, S. He, G. Yan (2017)**
  *Scattering Forms and the Positive Geometry of Kinematics*
  [https://arxiv.org/abs/1711.09102](https://arxiv.org/abs/1711.09102)
  Introduces the kinematic associahedron (ABHY construction) and identifies tree-level scalar amplitudes as canonical forms of a polytope in kinematic space.

* **N. Arkani-Hamed, Y. Bai, S. He (2017)**
  *The All-Loop Integrand for Scattering Amplitudes in Planar N=4 SYM*
  [https://arxiv.org/abs/1703.04541](https://arxiv.org/abs/1703.04541)
  Explores recursive and geometric structures underlying amplitude factorization.

---

## 🔷 Canonical Forms & Positive Geometry (General Framework)

* **N. Arkani-Hamed, Y. Bai, T. Lam (2017)**
  *Positive Geometries and Canonical Forms*
  [https://arxiv.org/abs/1703.04541](https://arxiv.org/abs/1703.04541)
  Formalizes the notion of positive geometries and their canonical differential forms.

* **SAGEX Review (2022)**
  *Scattering Amplitudes and Positive Geometry*
  [https://arxiv.org/abs/2203.13018](https://arxiv.org/abs/2203.13018)
  Comprehensive review of positive geometry, amplituhedron, associahedron, and canonical forms.

---

## 🔷 Origami Connection & Momentum Amplituhedron

* **P. Galashin (2024)**
  *Origami and the Momentum Amplituhedron*
  (arXiv link — October 2024 preprint)
  Establishes a correspondence between origami crease patterns and regions of the momentum amplituhedron, resolving the triangulation conjecture.

* **Kevin Hartnett (2025)**
  *Origami Patterns Solve a Major Physics Riddle*
  Quanta Magazine
  [https://www.quantamagazine.org/origami-patterns-solve-a-major-physics-riddle-20251006/](https://www.quantamagazine.org/origami-patterns-solve-a-major-physics-riddle-20251006/)
  Accessible overview of the origami–amplituhedron connection.

---

## 🔷 Scattering Amplitude Methods (Pre-Amplituhedron Foundations)

* **Britto, Cachazo, Feng, Witten (2005)**
  *Direct Proof of Tree-Level Recursion Relation in Yang-Mills Theory*
  [https://arxiv.org/abs/hep-th/0501052](https://arxiv.org/abs/hep-th/0501052)
  Introduces BCFW recursion, a precursor to geometric interpretations.

* **Parke, Taylor (1986)**
  *An Amplitude for n Gluon Scattering*
  [https://doi.org/10.1103/PhysRevLett.56.2459](https://doi.org/10.1103/PhysRevLett.56.2459)
  Early indication that scattering amplitudes admit unexpectedly simple closed forms.

---

## 🔷 Conceptual & Popular Expositions

* **Kevin Hartnett (2013)**
  *A Jewel at the Heart of Quantum Physics*
  Quanta Magazine
  [https://www.quantamagazine.org/a-jewel-at-the-heart-of-quantum-physics-20130917/](https://www.quantamagazine.org/a-jewel-at-the-heart-of-quantum-physics-20130917/)
  Introduced the amplituhedron to a broad scientific audience.

* **N. Arkani-Hamed (various lectures)**
  IAS and public lecture series on amplitudes and positive geometry.
  (Many available on YouTube and IAS lecture archives.)

---

# 🧭 Conceptual Themes This Project Builds On

* Geometry replaces diagrammatic enumeration
* Canonical forms are uniquely determined by boundary structure
* Positivity encodes physical consistency
* Factorization corresponds to geometric boundaries
* Combinatorics ↔ geometry ↔ physics equivalence
* Constraint-defined systems over rule-defined systems
