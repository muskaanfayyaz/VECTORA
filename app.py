"""Streamlit entry point for the Line Integrals simulator."""

import streamlit as st

from pages import about, comparison, dashboard, force_explorer, learn_basics, mathematical_analysis, path_simulator, quiz, work_calculator

st.set_page_config(page_title="Line Integrals Simulator", page_icon="∫", layout="wide")
st.markdown(
    """<style>
    .stApp { background: #f5f8fa; }
    [data-testid="stSidebar"] { background: #102a43; }
    [data-testid="stSidebar"] * { color: #f5f8fa; }
    h1, h2, h3 { color: #102a43; }
    </style>""",
    unsafe_allow_html=True,
)

page = st.navigation(
    {
        "Discover": [
            st.Page(dashboard.render, title="Dashboard", url_path="dashboard", icon=":material/dashboard:", help="Introduction and project overview."),
            st.Page(learn_basics.render, title="Learn the basics", url_path="learn-basics", icon=":material/menu_book:", help="Understand the ideas before simulating."),
        ],
        "Explore": [
            st.Page(force_explorer.render, title="Force field explorer", url_path="force-explorer", icon=":material/explore:", help="Discover how forces act in different directions."),
            st.Page(path_simulator.render, title="Path simulator", url_path="path-simulator", icon=":material/timeline:", help="Visualize an object's journey along different routes."),
        ],
        "Calculate": [
            st.Page(work_calculator.render, title="Work calculator", url_path="work-calculator", icon=":material/calculate:", help="Calculate work using line integrals."),
            st.Page(comparison.render, title="Field comparison", url_path="comparison", icon=":material/compare_arrows:", help="Compare conservative and non-conservative fields."),
        ],
        "Understand": [
            st.Page(mathematical_analysis.render, title="Mathematical analysis", url_path="mathematical-analysis", icon=":material/functions:", help="Explore equations, derivations, curl, and potential functions."),
            st.Page(quiz.render, title="Knowledge check", url_path="quiz", icon=":material/school:", help="Test your understanding through interactive questions."),
        ],
        "Project": [
            st.Page(about.render, title="About VECTORA", url_path="about", icon=":material/info:", help="Objectives, methodology, technologies, and project information."),
        ],
    },
    position="sidebar",
)

with st.sidebar:
   st.title("VECTORA")
   st.caption("Interactive Physics & Calculus Laboratory")
   st.info("New here? Start with **Learn the basics**, then try the **Path simulator**.")

page.run()
