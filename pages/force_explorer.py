import streamlit as st

from calculations.force_fields import FIELDS
from calculations.verification import symbolic_curl
from visualizations.plots import vector_field_plot


def render() -> None:
    st.title("Force Field Explorer")
    st.caption("Inspect how force direction and strength change across space.")
    key = st.selectbox("Choose a force field", list(FIELDS), format_func=lambda value: FIELDS[value].name)
    field = FIELDS[key]
    left, right = st.columns(2)
    with left:
        limit = st.slider("Plot range", 2, 5, 3)
    with right:
        density = st.slider("Vector density", 9, 25, 17, step=2)
    st.latex(field.equation)
    st.pyplot(vector_field_plot(field, (-limit, limit), density), clear_figure=True)
    st.subheader("Inspect one coordinate")
    x, y = st.columns(2)
    point = (x.number_input("x coordinate", -10.0, 10.0, 1.0, key="inspect-x"), y.number_input("y coordinate", -10.0, 10.0, 1.0, key="inspect-y"))
    force = field.evaluate(point)
    magnitude = float((force[0] ** 2 + force[1] ** 2) ** 0.5)
    metrics = st.columns(3)
    metrics[0].metric("Fx", f"{force[0]:.3g}")
    metrics[1].metric("Fy", f"{force[1]:.3g}")
    metrics[2].metric("Magnitude", f"{magnitude:.3g}")
    st.caption("The force vector at the selected coordinate tells you the instantaneous push or pull there.")
    left, right = st.columns(2)
    left.metric("Curl", str(symbolic_curl(field)))
    right.metric("Potential", field.potential or "None on the plane")
    st.write(field.description)
