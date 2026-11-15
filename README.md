# VECTORA

## Interactive Line Integrals and Work Done by a Force Simulator

**Project ID:** PEF26-G13  
**Subject:** Multivariable calculus  
**Application type:** Interactive scientific education platform  
**Deadline:** November 30, 2026

VECTORA is an interactive Streamlit application that connects the theory of
vector fields and line integrals with visual experiments. It investigates a
central question in multivariable calculus:

> If an object moves between the same two points along different paths, does
> the force do the same amount of work?

The application compares one conservative field with one non-conservative
field, calculates work along three trajectories, visualizes the force
directions, and verifies the mathematics numerically and symbolically.

---

## 1. Project objectives

VECTORA was designed to help a beginner, university student, or classroom
demonstration understand:

1. What a two-dimensional vector field represents.
2. How a curve is parameterized.
3. How a force produces work along a trajectory.
4. How a line integral accumulates work along a complete path.
5. What makes a vector field conservative.
6. How a potential function gives path-independent work.
7. What curl says about local rotation.
8. Why a non-conservative field can produce different work on different paths.
9. How numerical integration can be checked against exact mathematics.

The application is intentionally educational. It is a focused two-dimensional
model, not a general-purpose physics engine.

---

## 2. The controlled experiment

To test **path dependence**, the starting and ending points are kept fixed:

$$
A=(0,0), \qquad B=(2,2).
$$

Keeping the endpoints fixed is important. If the endpoints and the route were
changed at the same time, a different work value could be caused by either
change. VECTORA changes only the route so that the comparison isolates the
effect of path geometry.

The three paths are:

### Path 1: Straight diagonal

$$
\mathbf r(t)=\langle 2t,2t\rangle,\qquad 0\leq t\leq 1.
$$

$$
\mathbf r'(t)=\langle2,2\rangle.
$$

### Path 2: Horizontal, then vertical

This is a piecewise path and must be integrated segment by segment.

$$
\mathbf r_1(t)=\langle2t,0\rangle,\qquad
\mathbf r_1'(t)=\langle2,0\rangle
$$

followed by

$$
\mathbf r_2(t)=\langle2,2t\rangle,\qquad
\mathbf r_2'(t)=\langle0,2\rangle.
$$

### Path 3: Vertical, then horizontal

$$
\mathbf r_1(t)=\langle0,2t\rangle,\qquad
\mathbf r_1'(t)=\langle0,2\rangle
$$

followed by

$$
\mathbf r_2(t)=\langle2t,2\rangle,\qquad
\mathbf r_2'(t)=\langle2,0\rangle.
$$

Every segment uses $0\leq t\leq1$. The segment results are then added.

---

## 3. Mathematical foundation

### 3.1 Vector fields

A two-dimensional vector field assigns a vector to every position:

$$
\mathbf F(x,y)=\langle F_x(x,y),F_y(x,y)\rangle.
$$

The vector has:

- **Magnitude:** the strength of the force.
- **Direction:** the direction in which the force pushes or pulls.
- **Position dependence:** the force may change as $(x,y)$ changes.

The arrows in VECTORA's field plots represent direction and relative size.
The background color represents force magnitude.

### 3.2 Work along a curve

For a force $\mathbf F$ and a parameterized curve $\mathbf r(t)$, work is

$$
W=\int_C\mathbf F\cdot d\mathbf r
 =\int_a^b
\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt.
$$

The terms mean:

- $\mathbf F(\mathbf r(t))$: force at the current position.
- $\mathbf r'(t)$: direction and rate of travel.
- The dot product: the component of force aligned with the motion.
- The integral: the sum of all infinitesimal work contributions.

For a piecewise curve $C=C_1\cup C_2$:

$$
\int_C\mathbf F\cdot d\mathbf r
=\int_{C_1}\mathbf F\cdot d\mathbf r
+\int_{C_2}\mathbf F\cdot d\mathbf r.
$$

### 3.3 Conservative fields

A field is conservative on a domain if there is a scalar potential
$\phi(x,y)$ such that

$$
\mathbf F=\nabla\phi
=\left\langle\frac{\partial\phi}{\partial x},
\frac{\partial\phi}{\partial y}\right\rangle.
$$

For a conservative field,

$$
W=\phi(B)-\phi(A),
$$

so the work depends only on the endpoints and not on the path.

### 3.4 Curl

For a planar field $\mathbf F=\langle P,Q\rangle$, the scalar two-dimensional
curl is

$$
\mathrm{curl}\,\mathbf F
=\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}.
$$

On a suitable simply connected domain with continuously differentiable
components, zero curl implies conservativeness. A nonzero curl proves that
the field is not conservative on that domain.

The domain condition matters: zero curl alone is not sufficient on domains with
holes.

---

## 4. Force fields used in the experiment

### 4.1 Conservative, gravity-like field

$$
\mathbf F_c(x,y)=\langle-2x,-2y\rangle.
$$

The field points toward the origin. Its potential is

$$
\phi(x,y)=-(x^2+y^2).
$$

Verification:

$$
\nabla\phi
=\left\langle\frac{\partial}{\partial x}[-(x^2+y^2)],
\frac{\partial}{\partial y}[-(x^2+y^2)]\right\rangle
=\langle-2x,-2y\rangle
=\mathbf F_c.
$$

Its curl is

$$
\frac{\partial(-2y)}{\partial x}
-\frac{\partial(-2x)}{\partial y}
=0-0=0.
$$

The potential theorem predicts:

$$
W=\phi(2,2)-\phi(0,0)
=-(2^2+2^2)-0=-8.
$$

### 4.2 Non-conservative, swirling field

$$
\mathbf F_{nc}(x,y)=\langle-y,x\rangle.
$$

This field circulates counterclockwise around the origin. Its curl is

$$
\frac{\partial x}{\partial x}
-\frac{\partial(-y)}{\partial y}
=1-(-1)=2.
$$

Because the curl is nonzero, this field is not conservative on the plane.
There is no globally defined scalar potential $\phi$ satisfying
$\nabla\phi=\mathbf F_{nc}$.

---

## 5. Exact work calculations

The interface calculates these values with SciPy quadrature. The following
derivations explain why the results are expected.

### 5.1 Conservative field

#### Straight path

$$
\mathbf F_c(\mathbf r(t))
=\langle-4t,-4t\rangle.
$$

$$
\mathbf F_c(\mathbf r(t))\cdot\mathbf r'(t)
=\langle-4t,-4t\rangle\cdot\langle2,2\rangle
=-16t.
$$

$$
W=\int_0^1-16t\,dt=-8.
$$

#### Horizontal then vertical

Horizontal segment:

$$
\mathbf F_c(2t,0)=\langle-4t,0\rangle,
\qquad
\mathbf F_c\cdot\mathbf r_1'=-8t,
$$

$$
W_1=\int_0^1-8t\,dt=-4.
$$

Vertical segment:

$$
\mathbf F_c(2,2t)=\langle-4,-4t\rangle,
\qquad
\mathbf F_c\cdot\mathbf r_2'=-8t,
$$

$$
W_2=\int_0^1-8t\,dt=-4.
$$

$$
W=W_1+W_2=-4-4=-8.
$$

#### Vertical then horizontal

Vertical segment:

$$
\mathbf F_c(0,2t)=\langle0,-4t\rangle,
\qquad
\mathbf F_c\cdot\mathbf r_1'=-8t,
$$

$$
W_1=-4.
$$

Horizontal segment:

$$
\mathbf F_c(2t,2)=\langle-4t,-4\rangle,
\qquad
\mathbf F_c\cdot\mathbf r_2'=-8t,
$$

$$
W_2=-4.
$$

$$
W=-8.
$$

### 5.2 Non-conservative field

#### Straight path

$$
\mathbf F_{nc}(2t,2t)=\langle-2t,2t\rangle.
$$

$$
\mathbf F_{nc}\cdot\mathbf r'
=\langle-2t,2t\rangle\cdot\langle2,2\rangle=0.
$$

$$
W=0.
$$

#### Horizontal then vertical

Horizontal segment:

$$
\mathbf F_{nc}(2t,0)=\langle0,2t\rangle,
\qquad
\mathbf F_{nc}\cdot\mathbf r_1'=0,
$$

$$
W_1=0.
$$

Vertical segment:

$$
\mathbf F_{nc}(2,2t)=\langle-2t,2\rangle,
\qquad
\mathbf F_{nc}\cdot\mathbf r_2'=4,
$$

$$
W_2=\int_0^1 4\,dt=4.
$$

$$
W=0+4=4.
$$

#### Vertical then horizontal

Vertical segment:

$$
\mathbf F_{nc}(0,2t)=\langle-2t,0\rangle,
\qquad
\mathbf F_{nc}\cdot\mathbf r_1'=0,
$$

$$
W_1=0.
$$

Horizontal segment:

$$
\mathbf F_{nc}(2t,2)=\langle-2,2t\rangle,
\qquad
\mathbf F_{nc}\cdot\mathbf r_2'=-4,
$$

$$
W_2=\int_0^1-4\,dt=-4.
$$

$$
W=0-4=-4.
$$

### Expected results

| Force field | Straight | Horizontal then vertical | Vertical then horizontal |
|---|---:|---:|---:|
| Conservative | $-8$ | $-8$ | $-8$ |
| Non-conservative | $0$ | $4$ | $-4$ |

The values are not hardcoded into the interface. They are produced by the
line-integral engine and checked by automated tests.

---

## 6. Application pages

The application uses a grouped sidebar so users can follow a learning path.

### Discover

#### Dashboard

Introduces the project, shows all three routes together, explains the
controlled experiment, and summarizes the central discovery.

#### Learn the basics

Introduces force, force fields, work, paths, parametrization, line integrals,
conservative fields, non-conservative fields, and curl in beginner-friendly
language.

### Explore

#### Force field explorer

Users can:

- Select either force field.
- Change the plot range.
- Change vector density.
- Inspect the force at a chosen coordinate.
- View $F_x$, $F_y$, magnitude, curl, and potential information.

#### Path simulator

Users can:

- Select a force field.
- Select any of the three required paths.
- Adjust visualization resolution.
- View force vectors and the trajectory.
- View path length.
- Expand each segment to see its parametrization and derivative.

### Calculate

#### Work calculator

Users can:

- Select a force field.
- Select a path.
- View each piecewise segment separately.
- View numerical work and error estimates.
- Compare all three paths.
- Expand the detailed mathematical derivation.
- Compare numerical results with exact symbolic work.

#### Field comparison

Shows work tables, path-independence status, curl values, and a comparison
chart. It makes the main result visible immediately:

- Conservative field: same work for every tested path.
- Non-conservative field: different work for different paths.

### Understand

#### Mathematical analysis

Provides the university-level definitions, formulas, curl discussion,
potential-function explanation, computed segment results, and exact symbolic
integrands.

#### Knowledge check

Provides one-question-at-a-time multiple-choice and true/false questions with:

- Immediate feedback.
- Explanations.
- Score tracking.
- Restart functionality.

### Project

#### About VECTORA

Documents the project overview, problem statement, objectives, methodology,
technologies, expected findings, and limitations.

---

## 7. Software architecture

```text
VECTORA/
├── app.py
├── requirements.txt
├── README.md
├── calculations/
│   ├── __init__.py
│   ├── force_fields.py
│   ├── paths.py
│   ├── integrals.py
│   └── verification.py
├── visualizations/
│   ├── __init__.py
│   └── plots.py
├── pages/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── learn_basics.py
│   ├── force_explorer.py
│   ├── path_simulator.py
│   ├── work_calculator.py
│   ├── comparison.py
│   ├── mathematical_analysis.py
│   ├── quiz.py
│   └── about.py
└── tests/
    ├── __init__.py
    └── test_calculations.py
```

### Mathematical engine

- `force_fields.py`: field definitions, symbolic components, potential
  metadata, and curl calculations.
- `paths.py`: parameterized curves, derivatives, symbolic path expressions,
  endpoints, and piecewise segments.
- `integrals.py`: SciPy-based numerical line integration and error estimates.
- `verification.py`: symbolic curl, gradient, exact segment integrands, exact
  segment work, and tolerance checks.

### Visualization layer

`visualizations/plots.py` generates:

- Vector-field quiver plots.
- Single-path plots.
- All-path comparison plots.
- Work comparison bar charts.

### Interface layer

The page modules render the educational interface. They call the mathematical
engine rather than duplicating field definitions or hardcoding work results.

---

## 8. Technologies

- **Python 3.11+:** application language.
- **Streamlit:** interactive web interface and navigation.
- **NumPy:** numerical arrays and vector calculations.
- **SciPy:** numerical quadrature for line integrals.
- **SymPy:** symbolic differentiation, curl, gradients, and exact integrals.
- **Matplotlib:** vector-field, trajectory, and comparison plots.
- **Pandas:** comparison tables.
- **pytest:** automated mathematical tests.

---

## 9. Installation and execution

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The application opens at the local Streamlit address shown in the terminal,
usually `http://localhost:8501`.

### Running the tests

```powershell
pytest -q
```

The test suite verifies:

- All six field/path combinations.
- Conservative potential gradient.
- Both curl calculations.
- All path endpoints.
- Piecewise segment work.
- Exact symbolic segment integrands and work.
- Numerical tolerance.

---

## 10. Scientific validation

The project uses two complementary forms of validation:

1. **Numerical validation:** SciPy evaluates
   $$
   \int_0^1\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt
   $$
   for each segment.
2. **Symbolic validation:** SymPy independently derives curl, checks
   $\nabla\phi=\mathbf F_c$, and integrates the symbolic segment integrands.

The numerical and exact results agree within the configured tolerance.

---

## 11. Interpretation of the findings

The conservative field has zero curl, a valid potential function, and equal
work for all three routes. This demonstrates path independence:

$$
W_{\text{straight}}
=W_{\text{horizontal}\to\text{vertical}}
=W_{\text{vertical}\to\text{horizontal}}
=-8.
$$

The swirling field has curl $2$, no global potential on the plane, and
different work values:

$$
0,\qquad4,\qquad-4.
$$

This demonstrates path dependence. The direction of each route matters because
the force circulates around the origin.

The experiment therefore supports the project conclusion:

> A conservative force is path independent, while a non-conservative swirling
> force can do different amounts of work along different paths connecting the
> same endpoints.

---

## 12. Scope and limitations

- The model is two-dimensional.
- The endpoints are fixed at $(0,0)$ and $(2,2)$.
- The application uses two selected analytic vector fields.
- The three paths are simple analytic curves, not arbitrary user-drawn paths.
- The plots are educational visualizations, not physical measurements.
- Work values are expressed in abstract mathematical units because no physical
  mass, time, or unit system is specified.
- The zero-curl criterion is presented with its necessary domain assumption.

These limitations keep the demonstration focused and mathematically
transparent.

---

## 13. Conclusion

VECTORA turns a multivariable-calculus experiment into an interactive learning
workflow:

1. Learn the meaning of a force and vector field.
2. See the same endpoints connected by three different routes.
3. Parameterize each route.
4. Compute the line integral segment by segment.
5. Compare conservative and non-conservative behavior.
6. Verify the result numerically and symbolically.
7. Test understanding through the knowledge check.

The project makes the abstract relationship between force, motion, path,
potential, curl, and work visible and testable.
