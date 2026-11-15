import pandas as pd
import streamlit as st

from calculations.force_fields import FIELDS
from calculations.integrals import line_integral
from calculations.paths import PATHS
from visualizations.plots import work_comparison_plot


def render() -> None:
    st.title("Conservative vs Non-Conservative")
    st.caption("The main discovery: same endpoints do not always mean the same work.")
    st.info("This is a controlled comparison: every row uses A = (0, 0) and B = (2, 2); only the path changes.")
    rows = []
    chart_data = {}
    for field in FIELDS.values():
        chart_data[field.name] = {}
        for path in PATHS.values():
            work = line_integral(field, path).work
            chart_data[field.name][path.name] = work
            rows.append({"Field": field.name, "Curl": field.curl, "Path": path.name, "Work": work, "Path independent": field.curl == 0})
    for field in FIELDS.values():
        field_rows = [row for row in rows if row["Field"] == field.name]
        with st.container(border=True):
            st.subheader(field.name)
            st.write("Path independent." if field.curl == 0 else "Path dependent.")
            st.dataframe(pd.DataFrame(field_rows), hide_index=True, width="stretch")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.pyplot(work_comparison_plot(chart_data), clear_figure=True)
    st.markdown("A zero curl field has identical work for these paths; the circulating field changes work when the route changes.")
