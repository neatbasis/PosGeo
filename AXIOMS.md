# 📘 AXIOMS.md

## Canonical Forms of Positive Geometries

### Theory–to–Engine Bridge (v0.1, Literature-Aligned)

---

# 0. Purpose of This Document

This document records:

1. **Theoretical axioms** assumed from positive geometry theory.
2. **Derived structural consequences** used operationally.
3. **Executable invariants** enforced in the engine.
4. **Theorem–dependency structure** clarifying logical flow.
5. **Design implications** linking axioms to architecture.
6. **Scope boundaries** defining v0.1 limits.

This repository does **not** reprove positive geometry theory.

It operationalizes selected properties in the **convex 2D affine case** and builds an engine that enforces them symbolically.

Primary reference:

Arkani-Hamed, Bai, Lam (2017) — *Positive Geometries and Canonical Forms*

---

# I. Theoretical Axioms (Assumed from Literature)

These axioms reflect the definitional framework of positive geometries.

---

## T-A1 — Positive Geometry Structure

A pair ((X, X_{\ge 0})) consists of:

* A real semi-algebraic subset (X_{\ge 0}),
* Embedded in a complex projective variety (X),
* With a stratified boundary decomposition into algebraic hypersurfaces.

A semi-algebraic set is called a **positive geometry** only if it satisfies the canonical-form properties below.

---

## T-A2 — Stratified Boundary Recursion

The boundary decomposes into finitely many strata:

* Codimension-1 facets,
* Codimension-2 intersections,
* …
* Zero-dimensional vertices.

Each boundary stratum is itself a positive geometry (or empty).

The recursive structure terminates in dimension zero.

---

## T-A3 — Existence of Canonical Form (Definitional)

A pair ((X, X_{\ge 0})) is a positive geometry if there exists a rational top-degree differential form (\Omega(X_{\ge 0})) satisfying T-A4–T-A6.

Existence is part of the definition of a positive geometry.
It is not guaranteed for arbitrary semi-algebraic sets.

---

## T-A4 — Logarithmic Singularity Condition

The canonical form has only simple logarithmic poles along boundary components.

Locally near a facet defined by (f = 0):

[
\Omega = \frac{df}{f} \wedge \omega + \eta
]

where:

* (\omega) is regular,
* (\eta) is regular along (f=0).

Higher-order poles are forbidden.

---

## T-A5 — Recursive Residue Property

For every facet (F):

[
\operatorname{Res}*F \Omega(X*{\ge 0}) = \Omega(F)
]

The canonical form is defined recursively via boundary restriction.

---

## T-A6 — Boundary-Only Poles (Final Form)

The canonical form may have poles only along true geometric boundary components.

Intermediate constructions (e.g., triangulations) may contain spurious poles,
but these must cancel in the final total form.

---

## T-A7 — Uniqueness up to Orientation (Scoped)

If two rational top-forms satisfy:

* Logarithmic singularity condition (T-A4),
* Recursive residue property (T-A5),
* Boundary-only poles (T-A6),

then their difference is holomorphic.

In the affine rational convex 2D setting considered here:

* The ambient affine space admits no nonzero holomorphic top-forms compatible with the boundary divisor.
* Therefore, the canonical form is unique up to global orientation sign.

This uniqueness depends on:

* Rationality,
* Absence of interior singularities,
* Ambient space assumptions.

---

## T-A8 — Top-Degree Condition

The canonical form is of degree equal to (\dim(X)).

---

# II. Orientation Axioms

Orientation is structural, not cosmetic.

---

## O1 — Global Orientation Dependence

Reversing the orientation of (X_{\ge 0}) multiplies (\Omega) by −1.

---

## O2 — Boundary Orientation Inheritance

Facet orientations are induced via the boundary operator.

Residue signs must respect induced orientation.

---

## O3 — Parity Consistency

If vertex ordering changes parity, (\Omega) changes sign globally but retains identical recursive structure.

---

# III. Structural Consequences (Derived in Convex 2D Case)

---

## S-C1 — Finite Pole Set

From T-A1 and T-A2:

Only finitely many codimension-1 facets exist.

Therefore the canonical form has finitely many poles.

---

## S-C2 — No Spurious Poles (Final Form)

From T-A4 and T-A6:

All poles in the final canonical form correspond to true boundary components.

---

## S-C3 — Triangulation Independence (Scoped)

In classes where positive triangulations exist (e.g., convex polytopes):

If the canonical form is computed as

[
\Omega = \sum \Omega(\text{subregion})
]

then the result is independent of triangulation.

Triangulation is a computational tool, not part of the definition.

---

## S-C4 — Deterministic Orientation Signs

Once global orientation is fixed, all residue signs are uniquely determined.

---

# IV. 2D Convex Polytope Specialization (v0.1 Domain)

Applies only to convex polygons in affine 2D with linear facets.

---

## P-1 — Rational Representation Structure

For linear facet equations (L_i(x,y)=0):

[
\Omega = \frac{P(x,y)}{\prod_i L_i(x,y)}, dx \wedge dy
]

---

## P-2 — Numerator Cancellation Requirement

The numerator must cancel all potential poles not corresponding to true boundary components.

---

## P-3 — Residue Dimension Reduction

Facet residues produce canonical 1-forms on boundary intervals.

---

## P-4 — Boundary Reconstruction Principle (Conditional)

For convex 2D polytopes:

Boundary equations together with recursive residue constraints determine the canonical form uniquely up to orientation, provided:

* Existence is assumed,
* Rationality holds,
* Ambient holomorphic obstructions are absent.

This is a scoped computational principle, not a universal theorem.

---

# V. Computational Axioms (Executable Constraints)

These are engineering constraints.

---

## E1 — Exact Rational Arithmetic

All validation must use exact rational arithmetic.

Floating-point approximations invalidate invariant verification.

---

## E2 — Invariant Gate

A candidate canonical form must satisfy:

1. Top-degree condition
2. Simple logarithmic poles (within enforcement limits)
3. Correct recursive residues
4. No spurious poles in final form
5. Orientation consistency

Failure invalidates the form within declared scope.

---

## E3 — Residue Operator as Primitive

Residue computation must be:

* Deterministic,
* Chart-independent (within affine domain),
* Orientation-aware.

---

## E4 — Triangulation as Test Instrument

Triangulation may generate candidate forms.

Axioms validate them.

Construction ≠ definition.

---

# VI. Theorem–Dependency Structure

---

## T1 — Canonical Form Determination (Scoped)

In the convex affine 2D case:

A rational top-form satisfying:

* Simple poles on true facets,
* Correct recursive residues,
* No spurious poles,

equals the canonical form up to orientation.

Depends on:

T-A4, T-A5, T-A6, T-A7.

---

## T2 — Triangulation Independence (Scoped)

In triangulable convex classes:

[
\sum \Omega(\text{subregion})
]

is independent of triangulation.

Depends on:

T-A5, T-A7.

---

## T3 — Orientation Consistency

Once global orientation is fixed, residue signs are determined.

Depends on:

O1, O2, T-A5.

---

# VII. Explicit Limitations (v0.1)

This repository does not treat:

* Projective infinity boundary components
* Unbounded regions
* Nonlinear boundary hypersurfaces
* Non-logarithmic singularities
* Covariant forms
* Higher-dimensional positive geometries
* Amplituhedron canonical forms
* Grassmannian geometries
* General constructive existence proofs

All claims are restricted to convex affine 2D polygons.

---

# VIII. Strategic Principle

The canonical form is defined by constraints:

* Logarithmic singularities,
* Recursive residues,
* Boundary-only poles,
* Orientation structure.

The computational problem is:

> Construct a form satisfying these constraints.

The engine enforces them within scope.

Construction mechanisms are secondary to constraint validation.

