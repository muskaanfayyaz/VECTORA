import streamlit as st

from calculations.force_fields import CONSERVATIVE_FIELD, NON_CONSERVATIVE_FIELD
from calculations.integrals import line_integral
from calculations.paths import PATHS
from visualizations.plots import paths_overview_plot


def render() -> None:
    st.title("Understand the force behind every path.")
    st.caption("VECTORA · Interactive Physics & Calculus Laboratory · PEF26-G13")
    st.write("Explore how forces interact with motion, calculate work along different trajectories, and discover why some forces depend on the path while others do not.")
    st.info("Imagine pushing an object from A = (0, 0) to B = (2, 2). We keep these endpoints fixed so the only variable is the route. VECTORA tests whether the amount of work depends on that route.")
    st.pyplot(paths_overview_plot(NON_CONSERVATIVE_FIELD, tuple(PATHS.values())), clear_figure=True)
    st.subheader("The three paths in this experiment")
    path_cards = st.columns(3)
    path_details = [
        ("Path 1 · Straight line", r"\mathbf r(t)=\langle2t,2t\rangle", "Direct diagonal route."),
        ("Path 2 · Horizontal → vertical", r"\mathbf r_1(t)=\langle2t,0\rangle,\ \mathbf r_2(t)=\langle2,2t\rangle", "Move right, then move up."),
        ("Path 3 · Vertical → horizontal", r"\mathbf r_1(t)=\langle0,2t\rangle,\ \mathbf r_2(t)=\langle2t,2\rangle", "Move up, then move right."),
    ]
    for card, (title, formula, explanation) in zip(path_cards, path_details):
        with card:
            with st.container(border=True):
                st.subheader(title)
                st.latex(formula)
                st.write(explanation)
    st.caption("All three routes start at A and finish at B. Only their geometry changes.")

    st.subheader("What you can do")
    cards = st.columns(4)
    for card, title, text in zip(
        cards,
        ["Explore force fields", "Visualize different paths", "Calculate work", "Compare results"],
        ["See direction, magnitude, curl, and potential.", "Watch three routes connect the same endpoints.", "Follow every step of the line integral.", "Make path independence obvious."],
    ):
        with card:
            with st.container(border=True):
                st.subheader(title)
                st.write(text)

    st.subheader("How VECTORA works")
    steps = st.columns(4)
    for step, number, label in zip(steps, range(1, 5), ["Choose a force field", "Select a path", "Calculate the work", "Understand the result"]):
        step.metric(f"Step {number}", label)

    st.subheader("The central discovery")
    conservative = [line_integral(CONSERVATIVE_FIELD, path).work for path in PATHS.values()]
    non_conservative = [line_integral(NON_CONSERVATIVE_FIELD, path).work for path in PATHS.values()]
    left, right = st.columns(2)
    left.success(f"Conservative field: all three paths give {conservative[0]:.0f} work units.")
    right.warning(f"Non-conservative field: paths give {', '.join(f'{value:.0f}' for value in non_conservative)} work units.")
