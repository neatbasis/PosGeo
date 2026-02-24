# 📘 AXIOMS.md

## Canonical Forms of Positive Geometries

### Theory–to–Engine Bridge (v0.2, Literature-Governed)

---

# 0. Purpose of This Document

This document specifies the **definition-level mathematical constraints** governing canonical forms of positive geometries and the corresponding **engine-level enforcement strategy** for the convex affine 2D domain implemented in this repository.

This repository:

* Does **not** reprove positive geometry theory.
* Does **not** claim universality.
* Implements a scoped, executable validator for canonical-form constraints in convex affine 2D polygons.

Primary reference:

Arkani-Hamed, Bai, Lam (2017) — *Positive Geometries and Canonical Forms*

---

# 0.1 Epistemic Classification

Every statement below is classified as:

* **D — Definition:** Part of the ABL definitional framework.
* **Th — Theorem (Scoped):** Proven under stated hypotheses.
* **A — Assumption (v0.2 Scope):** Assumed true within this repository’s domain.
* **E — Engineering Constraint:** Enforced by implementation.
* **R — Regression Oracle:** Used for falsification, not definitional grounding.
* **Drift Trigger:** Expands beyond canonical log-regime.

---

# I. Definitional Framework (ABL-Aligned)

---

## T-A1 — Positive Geometry Structure

**Status: D**

A pair ((X, X_{\ge 0})) consists of:

* A complex projective variety (X),
* A real semi-algebraic subset (X_{\ge 0}),
* A stratified boundary decomposition into algebraic hypersurfaces.

Only those pairs satisfying the canonical-form conditions below qualify as (rational) positive geometries.

This is a **definitional filter**, not a theorem about arbitrary semi-algebraic sets.

---

## T-A2 — Stratified Boundary Recursion

**Status: D**

The boundary decomposes into finitely many strata:

* Codimension-1 facets,
* Codimension-2 intersections,
* …
* Zero-dimensional vertices.

Each boundary stratum must itself be a positive geometry (or empty).

The recursion terminates in dimension zero.

---

## T-A3 — Existence of Canonical Form

**Status: D**

A pair is a positive geometry if there exists a **nonzero rational top-degree differential form** satisfying T-A4–T-A6.

Existence is definitional.
It is not guaranteed for arbitrary semi-algebraic sets.

---

## T-A4 — Logarithmic Singularity Condition

**Status: D**

The canonical form has only **simple poles** along boundary components.

Locally near a facet defined by (f = 0):

[
\Omega = \frac{df}{f} \wedge \omega + \eta
]

where:

* (\omega) is regular,
* (\eta) is regular along (f=0).

Higher-order poles are forbidden.

---

### Operational Corollary (2D Scope)

**Status: E (enforced)**

Log-purity must hold **recursively under restriction**:

* Codimension-1 (facets): simple pole only.
* Codimension-2 (vertices): no hidden higher-order behavior under iterated residue / local coordinate restriction.

A form that passes facet-level checks but develops higher-order poles at intersections **fails canonical log-purity**.

---

## T-A5 — Recursive Residue Property

**Status: D**

For each facet (F):

[
\operatorname{Res}*F \Omega(X*{\ge 0}) = \Omega(F)
]

The canonical form is defined recursively via boundary restriction.

---

## T-A6 — Boundary-Only Poles (Final Form)

**Status: D**

The final canonical form may have poles **only on true geometric boundary components**.

Intermediate constructions (e.g., triangulations) may introduce spurious poles, but:

> Spurious-pole cancellation is a **global identity**.
> It is not required (and generally not expected) to occur pairwise.

---

## T-A7 — Uniqueness up to Orientation (Scoped)

**Status: Th (under hypothesis) + A (v0.2)**

If two rational top-forms satisfy:

* T-A4 (log-purity),
* T-A5 (recursive residues),
* T-A6 (boundary-only poles),

then their difference has no residues and is therefore holomorphic.

Uniqueness follows under the hypothesis:

[
H^0(X, K_X) = 0
]

(i.e., no nonzero holomorphic top forms on (X)).

---

### v0.2 Assumption

Within the convex affine 2D rational polygon model:

* The ambient model is treated as satisfying the no-holomorphic-obstruction condition.
* Therefore uniqueness holds up to global orientation.

This is a **scoped assumption**, not a universal theorem.

---

## T-A8 — Top-Degree Condition

**Status: D**

The canonical form has degree equal to (\dim(X)).

---

# II. Orientation Structure

---

## O1 — Global Orientation Dependence

**Status: D**

Reversing orientation multiplies (\Omega) by −1.

---

## O2 — Boundary Orientation Inheritance

**Status: D**

Facet orientations are induced by the boundary operator.

Residue signs must respect induced orientation.

---

## O3 — Parity Consistency

**Status: D**

Parity changes in vertex ordering change the global sign only.

---

# III. Structural Consequences (Convex 2D Scope)

---

## S-C1 — Finite Pole Set

**Status: Derived (Th within scope)**

From finite boundary decomposition, pole set is finite.

---

## S-C2 — No Spurious Poles in Final Form

**Status: D + E**

Final canonical form contains poles only on true boundary components.

Spurious poles in intermediate constructions must vanish in final expression.

---

## S-C3 — Triangulation Independence (Scoped)

**Status: Th (in ABL framework) + R (engine use)**

If:

[
\Omega = \sum \Omega(\text{subregion})
]

over a valid triangulation, then result is independent of triangulation.

In this repository:

* Triangulation is used as a **regression oracle**.
* It is not part of the definition of the canonical form.

---

## S-C4 — Deterministic Orientation Signs

**Status: Derived**

Residue signs are uniquely determined once global orientation is fixed.

---

# IV. 2D Convex Polytope Specialization (v0.2 Domain)

Applies only to bounded convex polygons with linear facets in affine (\mathbb{R}^2).

---

## P-1 — Expected Rational Normal Form (Target Representation)

**Status: Engineering target, not definitional**

Canonical forms are expected to admit representation:

[
\Omega = \frac{P(x,y)}{\prod_i L_i(x,y)}, dx \wedge dy
]

where (L_i=0) define facets.

Equivalent representations may appear as sums with cancellations.

This is a **normal-form target for testing**, not a required axiom.

---

## P-2 — Numerator Cancellation Requirement

**Status: E**

Numerator must eliminate all non-boundary poles, including hidden poles revealed under stratified restriction.

---

## P-3 — Residue Dimension Reduction

**Status: D (instantiated)**

Facet residues produce canonical 1-forms on boundary intervals.

Vertex residues produce ±1 (orientation).

---

## P-4 — Boundary Reconstruction Principle (Scoped)

**Status: Th (scoped)**

In convex affine 2D polygons:

A rational top-form satisfying:

* Simple poles on facets,
* Correct recursive residues,
* No spurious poles,

equals the canonical form up to orientation,

provided existence and uniqueness hypotheses hold.

This is not claimed beyond the v0.2 domain.

---

# V. Computational Enforcement Layer

---

## E1 — Exact Rational Arithmetic

Floating-point arithmetic is forbidden in invariant verification.

---

## E2 — Invariant Gate (SingularityGate)

A candidate form must satisfy:

1. Top-degree condition
2. Log-purity (facet + vertex-level enforcement)
3. Recursive residue correctness
4. Boundary-only poles (global confluence check)
5. Orientation consistency

Failure invalidates the form within scope.

---

## E3 — Residue Operator as Primitive

Residue computation must be:

* Deterministic,
* Chart-consistent,
* Orientation-aware.

---

## E4 — Triangulation as Regression Oracle

Multiple construction paths must agree.

Construction ≠ definition.

---

# VI. Theorem–Dependency Structure (Scoped)

---

## T1 — Canonical Form Determination (2D Scope)

Depends on:

* T-A4
* T-A5
* T-A6
* T-A7

---

## T2 — Triangulation Confluence (Scoped)

Depends on:

* T-A5
* T-A7

Used as regression oracle.

---

## T3 — Orientation Consistency

Depends on:

* O1
* O2
* T-A5

---

# VII. Explicit Limitations (v0.2)

Not treated:

* Projective infinity boundary components
* Unbounded regions
* Nonlinear boundaries
* Higher dimensions
* Grassmannian geometries
* Amplituhedron canonical forms
* Pushforward generality proofs
* Non-logarithmic regimes (covariant forms/pairings)
* Pseudo-positive/null geometries ((\Omega \equiv 0))

Admitting non-log singularities is a **Drift Trigger**:
spurious cancellation semantics must be redefined.

---

# VIII. Strategic Principle

Canonical form = constraints:

* Log-purity (stratified)
* Recursive residues
* Boundary-only poles
* Orientation coherence

The engine’s role:

> Validate constraint satisfaction within declared scope.

Construction methods are secondary.

Constraint satisfaction is primary.
