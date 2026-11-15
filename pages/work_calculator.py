import pandas as pd
import streamlit as st

from calculations.force_fields import FIELDS
from calculations.integrals import line_integral
from calculations.paths import PATHS
from calculations.verification import symbolic_segment_integrand, symbolic_segment_work


def _show_result(field_key: str, path_key: str) -> None:
    field = FIELDS[field_key]
    path = PATHS[path_key]
    result = line_integral(field, path)
    st.subheader(f"{field.name} — {path.name}")
    st.latex(r"W=\int_0^1 \mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt")
    rows = []
    for segment_result in result.segments:
        segment = segment_result.segment
        rows.append({"Segment": segment.name, "Parametrization": segment.formula, "Work": segment_result.work, "Estimated error": segment_result.error})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.success(f"Total work: {result.work:.10g}")
    st.caption(f"Numerical integration error estimate: {result.error:.3e}")
    exact_work = sum(symbolic_segment_work(field, segment_result.segment) for segment_result in result.segments)
    st.info(f"Independent analytical check: {exact_work} work units.")
    st.caption("The endpoints are intentionally fixed at A = (0, 0) and B = (2, 2), so only the force and route change between experiments.")
    with st.expander("What does this result mean?"):
        st.write("The sign tells us whether the field contributes energy along the selected direction. For a piecewise route, each segment is calculated independently and then added.")
    with st.expander("Show detailed mathematics"):
        for segment_result in result.segments:
            segment = segment_result.segment
            st.markdown(f"**{segment.name}**")
            st.latex(segment.formula)
            st.latex(r"\mathbf F(\mathbf r(t))=" + field.equation)
            st.latex(r"\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)=" + str(symbolic_segment_integrand(field, segment)))
            st.latex(r"\int_0^1 " + str(symbolic_segment_integrand(field, segment)) + r"\,dt")
            st.write(f"Numerical segment result: {segment_result.work:.10g}")


def render() -> None:
    st.title("Work Calculator")
    st.caption("Follow the complete calculation from force field and path to final work.")
    st.info("The experiment uses fixed endpoints A = (0, 0) and B = (2, 2) so every path comparison is fair.")
    field_key = st.selectbox("Force field", list(FIELDS), format_func=lambda value: FIELDS[value].name)
    path_key = st.selectbox("Path", list(PATHS), format_func=lambda value: PATHS[value].name)
    _show_result(field_key, path_key)
    if st.checkbox("Compare all three paths"):
        for key in PATHS:
            _show_result(field_key, key)
