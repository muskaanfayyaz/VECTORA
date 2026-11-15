import streamlit as st
import numpy as np

from calculations.force_fields import FIELDS
from calculations.paths import PATHS
from visualizations.plots import path_plot


def render() -> None:
    st.title("Path Simulator")
    st.caption("All three routes connect the same endpoints. The question is whether changing the route changes total work.")
    st.info("Changing the path means changing the route between A and B—not changing A or B. Use the selector below to inspect each required route.")
    field = FIELDS[st.selectbox("Force field", list(FIELDS), format_func=lambda value: FIELDS[value].name)]
    path = PATHS[st.selectbox("Trajectory", list(PATHS), format_func=lambda value: PATHS[value].name)]
    resolution = st.slider("Visualization resolution", 20, 300, 100)
    st.pyplot(path_plot(field, path, resolution), clear_figure=True)
    st.write(path.description)
    path_length = sum(
        float(np.linalg.norm(np.diff(segment.sample(resolution), axis=0), axis=1).sum())
        for segment in path.segments
    )
    st.metric("Approximate path length", f"{path_length:.3f}")
    for segment in path.segments:
        with st.expander(segment.name):
            st.latex(segment.formula)
            velocity = segment.derivative(0.0)
            st.latex(r"\frac{d\mathbf r}{dt}=\langle" + f"{velocity[0]:.3g},{velocity[1]:.3g}" + r"\rangle")
