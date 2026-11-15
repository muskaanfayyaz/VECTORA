import streamlit as st


def render() -> None:
    st.title("About VECTORA")
    st.caption("Interactive Physics & Calculus Laboratory · Project PEF26-G13")
    st.subheader("Project overview")
    st.write("VECTORA is an educational simulation of vector fields, parametrized curves, line integrals, and work done by a force. It lets learners connect equations with visible motion and measurable results.")
    st.subheader("Problem statement")
    st.write("When an object moves from A = (0, 0) to B = (2, 2), does the route change the work done by a force? VECTORA answers this experimentally and analytically.")
    st.subheader("Objectives")
    st.markdown("- Explain line integrals to beginners.\n- Compare conservative and non-conservative fields.\n- Visualize force direction and path geometry.\n- Verify numerical work using symbolic mathematics.")
    st.subheader("Methodology")
    st.write("The application evaluates each path segment using SciPy numerical integration, while SymPy independently verifies curl and the conservative potential gradient. Matplotlib renders the vector fields and trajectories.")
    st.subheader("Technology")
    st.write("Python 3.11+, Streamlit, NumPy, SciPy, SymPy, Matplotlib, Pandas, and pytest.")
    with st.expander("Models and expected finding"):
        st.latex(r"\mathbf F_c=\langle-2x,-2y\rangle,\quad \phi=-(x^2+y^2),\quad \operatorname{curl}\mathbf F_c=0")
        st.latex(r"\mathbf F_{nc}=\langle-y,x\rangle,\quad \operatorname{curl}\mathbf F_{nc}=2")
        st.write("The conservative field gives the same work on all three paths. The non-conservative field gives different values.")
    with st.expander("Limitations"):
        st.write("This is a two-dimensional educational model using selected analytic fields and fixed endpoints. It demonstrates the ideas clearly but is not a general-purpose physics engine.")
    st.success("Conclusion: VECTORA makes path independence visible, calculable, and explainable.")
