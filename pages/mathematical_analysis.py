import streamlit as st

from calculations.force_fields import FIELDS
from calculations.integrals import line_integral
from calculations.paths import PATHS
from calculations.verification import symbolic_segment_integrand, symbolic_segment_work


def render() -> None:
    st.title("Mathematical Analysis")
    st.caption("Use this page after Learn the basics if you want the university-level derivation.")
    st.markdown(r"""
### Work and line integrals
For a parameterized curve $\mathbf r(t)$, the work is
$$W=\int_C\mathbf F\cdot d\mathbf r=\int_a^b\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt.$$

### Conservative fields
If $\mathbf F=\nabla\phi$, then $W=\phi(B)-\phi(A)$ and the result is path independent.
For $\mathbf F=\langle-2x,-2y\rangle$, $\phi=-(x^2+y^2)$ and
$\nabla\phi=\mathbf F$. Its curl is zero.

### Non-conservative fields
For $\mathbf F=\langle-y,x\rangle$, the scalar curl is
$$\frac{\partial F_y}{\partial x}-\frac{\partial F_x}{\partial y}=2.$$
This circulation prevents a global potential function on the plane.
""")
    st.subheader("Computed segment derivations")
    for field in FIELDS.values():
        with st.expander(field.name):
            for path in PATHS.values():
                result = line_integral(field, path)
                st.write(f"{path.name}: " + ", ".join(f"{part.work:.6g}" for part in result.segments) + f" = {result.work:.6g}")
                with st.expander(f"Show exact integrands for {path.name}"):
                    for segment in path.segments:
                        st.latex(r"\int_0^1 " + str(symbolic_segment_integrand(field, segment)) + r"\,dt=" + str(symbolic_segment_work(field, segment)))
    st.info("Numerical values come from SciPy quadrature. The exact field identities, curl, and conservative potential are verified symbolically in the mathematical engine.")
