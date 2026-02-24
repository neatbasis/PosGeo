Proposal for an **“Amplituhedron/Associahedron Compiler”** style Python package: typed objects at each layer, explicit invariants, and minimal “roll-your-own” by leaning on SymPy + NetworkX + existing polytope tooling where possible.

---

# Package goal

A small library that can:

1. accept **boundary data** (kinematics or origami boundary)
2. produce a **combinatorial object** (triangulation / plabic graph / cluster)
3. map to a **positive geometry region** (polytope cell)
4. output the **canonical form** (symbolic) and allow **numeric evaluation**
5. validate **boundary/factorization** properties via residues

You can use it for the ABHY associahedron immediately, and keep the door open for amplituhedron later.

---

# Minimal module layout

```
posgeo/
  __init__.py
  typing.py
  kinematics/
    mandelstam.py
    planar_vars.py
    constraints.py
  combinatorics/
    triangulations.py
    plabic.py
    cluster.py
  geometry/
    polytope.py
    associahedron.py
    cells.py
  forms/
    canonical.py
    residues.py
    pushforward.py
  backends/
    sympy_backend.py
    networkx_backend.py
    polytope_backend.py
  demos/
    demo_a4_interval.py
    demo_a5_pentagon.py
    demo_factorization.py
  tests/
    ...
```

---

# Core data model (typed “compiler IR”)

## 1) Boundary data (input IR)

### `BoundarySpec`

Represents the minimal external information that defines a positive geometry instance.

```python
@dataclass(frozen=True)
class BoundarySpec:
    kind: Literal["abhy_phi3", "origami_momentum", "amplituhedron_twistor"]
    n: int
    ordering: tuple[int, ...]          # cyclic order for planar sector
    params: dict[str, Any]             # e.g. fixed constants, gauge choices
    symbols: dict[str, sympy.Symbol]   # optional symbolic handles
```

**Invariants**

* `ordering` is a permutation of `1..n`
* `kind` selects which constraints / maps are legal

---

## 2) Constraint set (the “type checker”)

### `PositivityConstraints`

A normalized representation of inequalities and equalities.

```python
@dataclass(frozen=True)
class PositivityConstraints:
    equalities: list[sympy.Expr]       # == 0
    inequalities: list[sympy.Expr]     # > 0 (or >= 0 depending)
    domain_symbols: tuple[sympy.Symbol, ...]
```

**Responsibilities**

* convert kinematics into planar variables
* enforce momentum conservation / slice conditions
* encode positivity (ABHY: planar invariants (X_{i,j} > 0))

---

## 3) Combinatorial object (middle IR)

### For associahedron demos: `Triangulation`

```python
@dataclass(frozen=True)
class Triangulation:
    n: int
    diagonals: frozenset[tuple[int, int]]  # e.g. (1,3), (1,4)
```

* vertices of associahedron ↔ triangulations
* adjacency ↔ flips

### For amplituhedron / origami path later: `PlabicGraph`

Use NetworkX under the hood, but wrap it with constraints.

```python
@dataclass
class PlabicGraph:
    n: int
    graph: networkx.Graph
    coloring: dict[Any, Literal["black", "white"]]
    boundary_nodes: tuple[Any, ...]
```

**Invariants**

* planar embedding exists
* bicoloring valid

---

## 4) Geometry object (target IR)

### `PolytopeRegion`

A generic convex polytope region described by halfspaces.

```python
@dataclass(frozen=True)
class PolytopeRegion:
    dim: int
    variables: tuple[sympy.Symbol, ...]
    halfspaces: list[sympy.Expr]      # each interpreted as >= 0
    facets: list["Facet"]             # symbolic identification
```

### `AssociahedronABHY(PolytopeRegion)`

Specialization that knows:

* how to build halfspaces from ABHY construction for given `n`
* which facets correspond to which planar channels
* how to enumerate vertices via triangulations

---

## 5) Canonical form object (output IR)

### `CanonicalForm`

Represented as a rational function times wedge of differentials.

```python
@dataclass(frozen=True)
class CanonicalForm:
    variables: tuple[sympy.Symbol, ...]
    numerator: sympy.Expr
    denominator: sympy.Expr
    orientation: tuple[sympy.Symbol, ...]  # order in wedge product

    def as_sympy(self) -> sympy.Expr: ...
```

You can store it as:
[
\Omega = f(x), dx_1 \wedge \cdots \wedge dx_d
]
with (f) rational.

---

# Key algorithms (compiler passes)

## Pass A — Build planar kinematic variables

**Input:** `BoundarySpec(kind="abhy_phi3")`
**Output:** `PositivityConstraints` + list of planar variables (X_{i,j})

This is where you map e.g. (s_{ij}) to the ABHY “diagonal” variables and impose the linear slice.

## Pass B — Build the associahedron region

**Input:** constraints + slice parameters
**Output:** `AssociahedronABHY` polytope in dimension `n-3`

## Pass C — Canonical form extraction

Several options, increasing sophistication:

### C1 (fast, practical): vertex-cone / triangulation formula for simple polytopes

For associahedra you can compute canonical form as a sum of vertex contributions (or triangulate into simplices).

* feasible for n ≤ 7 as a demo
* easy to validate residues

### C2 (more general): compute canonical form by “boundary recursion”

Enforce:

* poles only on facets
* residues on each facet equal canonical forms of lower-dimensional faces

This is the “uniqueness from boundary” mode — extremely aligned with your constraints worldview.

## Pass D — Residue / factorization checker

Given a facet equation (X_{i,j} = 0):

* compute residue of the canonical form at that pole
* verify it matches the product of lower-point objects (ABHY factorization)

---

# Practical demo suite (what you can show in a notebook)

## Demo 1: A4 interval (n=4)

* build region: `0 < s < -u`
* canonical form: `ds/s + ds/t`
* verify poles are only at endpoints

## Demo 2: A5 pentagon (n=5)

* build ABHY pentagon in 2D slice
* visualize vertices (triangulations)
* compute canonical form by triangulating the pentagon into triangles
* show it equals 5-term (\phi^3) amplitude

## Demo 3: Boundary = factorization

Pick facet `X_{13} → 0`:

* compute residue
* show it equals `m_4 * m_3` (or the correct lower-point combination)

## Demo 4: “No diagram summing”

Compare:

* brute enumeration of planar cubic graphs (Catalan number)
* canonical form evaluation (polytope-based)
  Show scaling and structural clarity.

---

# Backends so you don’t roll your own

## Symbolics

* **SymPy**: expressions, rational simplification, residues (via series / `residue` patterns)

## Graphs

* **NetworkX**: triangulation adjacency graphs, flips, plabic scaffolding

## Polytopes

Depending on how far you want to go:

* **pycddlib** (CDD via Python): H-rep ↔ V-rep conversions (halfspaces ↔ vertices)
* **pypoman**: polytope operations + visualization helpers (often uses cddlib)
* **polymake** (external, optional): heavyweight but great if you’re okay calling out

If you want “pure Python minimal”, you can still:

* hardcode ABHY halfspaces for small n
* triangulate using combinatorics (no V-rep needed for small demos)

---

# What v0.1 could look like (Definition of Done)

* `AssociahedronABHY.from_n(n, slice_params=...)` returns a polytope
* `canonical_form(region)` returns `CanonicalForm` for n=4,5,6
* `residue(form, facet)` works for those and passes factorization tests
* demos produce plots + symbolic checks

---

# Why?

This is essentially a **contract-driven compiler**:

* boundary data is your “input schema”
* constraints are “type checking”
* combinatorial layer is “IR”
* geometry is “target representation”
* canonical form is “executable artifact”
* residues are your “unit tests / invariants”

