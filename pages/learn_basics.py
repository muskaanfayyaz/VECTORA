import streamlit as st

from calculations.force_fields import CONSERVATIVE_FIELD, NON_CONSERVATIVE_FIELD
from calculations.paths import PATHS
from visualizations.plots import paths_overview_plot, vector_field_plot


def render() -> None:
    st.title("Learn the basics")
    st.caption("Start with intuition, then connect each idea to the mathematics used by VECTORA.")
    st.info("Beginner route: read the cards from top to bottom, then try the simulator.")

    concepts = [
        ("1. What is a force?", "A force is a push or pull. It has both size and direction, so we represent it with a vector.", r"\mathbf F=\langle F_x,F_y\rangle", "Think of pushing a box: the push is most effective when it points in the direction the box moves.", "A force tells us how motion is influenced at each moment."),
        ("2. What is a force field?", "A force field assigns a force vector to every position. The arrows in the explorer show what an object would feel at each point.", r"\mathbf F(x,y)", "Wind can have a different direction and strength at different locations.", "The input is position; the output is a force vector."),
        ("3. What is work?", "Work measures how much a force contributes to displacement. A force perpendicular to motion contributes no work.", r"W=\mathbf F\cdot\mathbf d", "Pushing forward helps; pushing sideways changes direction but does not add forward work.", "The dot product keeps only the component of force along motion."),
    ]
    for title, explanation, formula, analogy, takeaway in concepts:
        with st.container(border=True):
            st.subheader(title)
            st.write(explanation)
            st.latex(formula)
            st.caption(f"Analogy: {analogy}")
            st.success(f"Key idea: {takeaway}")

    st.subheader("4. The path from A to B")
    st.write("The same object can travel between the same endpoints using different routes. Keeping A and B fixed is essential: it lets us test the effect of the route alone.")
    st.pyplot(paths_overview_plot(NON_CONSERVATIVE_FIELD, tuple(PATHS.values())), clear_figure=True)
    st.markdown("**Path 1:** straight diagonal · **Path 2:** horizontal then vertical · **Path 3:** vertical then horizontal")

    with st.expander("5. Parametrization and line integrals"):
        st.write("A parameter t moves from 0 to 1 along a curve. The curve tells us the position and its derivative tells us the instantaneous direction of travel.")
        st.latex(r"\mathbf r(t)=\langle x(t),y(t)\rangle,\qquad d\mathbf r=\mathbf r'(t)\,dt")
        st.latex(r"W=\int_C\mathbf F\cdot d\mathbf r=\int_a^b\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt")
        st.markdown("- **F** is the force at the current position.\n- **dr** is a tiny displacement.\n- **F · dr** is the tiny amount of work.\n- The integral adds every tiny contribution along the whole path.")

    with st.expander("6. Conservative and non-conservative fields"):
        left, right = st.columns(2)
        with left:
            st.subheader("Conservative")
            st.write("This field points toward the origin and has a potential function. Only the endpoints determine work.")
            st.latex(CONSERVATIVE_FIELD.equation)
            st.pyplot(vector_field_plot(CONSERVATIVE_FIELD, (-2, 2), 11), clear_figure=True)
        with right:
            st.subheader("Non-conservative")
            st.write("This field circulates around the origin. Different routes can accumulate different work.")
            st.latex(NON_CONSERVATIVE_FIELD.equation)
            st.pyplot(vector_field_plot(NON_CONSERVATIVE_FIELD, (-2, 2), 11), clear_figure=True)

    with st.expander("7. Curl in plain language"):
        st.write("Curl measures local rotational tendency. In two dimensions it is ∂Fy/∂x − ∂Fx/∂y. A zero curl supports path independence on a suitable simply connected domain; it is not a universal test without domain assumptions.")
        st.latex(r"\operatorname{curl}\mathbf F=\frac{\partial F_y}{\partial x}-\frac{\partial F_x}{\partial y}")
        st.success("Takeaway: zero curl plus the domain assumptions points toward a conservative field; nonzero curl signals circulation.")
