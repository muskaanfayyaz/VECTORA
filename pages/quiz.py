import streamlit as st


QUESTIONS = [
    ("Which field is path independent?", ["Conservative", "Non-conservative", "Both always", "Neither"], "Conservative", "A conservative field has a potential function and path-independent work."),
    ("What is the curl of <-y, x>?", ["0", "1", "2", "-2"], "2", "d(x)/dx - d(-y)/dy = 1 - (-1) = 2."),
    ("What is the conservative work from (0,0) to (2,2)?", ["-8", "-4", "0", "8"], "-8", "Use phi(B)-phi(A) = -8 - 0."),
    ("True or false: a line integral adds force contributions along a curve.", ["True", "False"], "True", "The integral accumulates F(r(t)) dot r'(t) over the complete path."),
]


def render() -> None:
    st.title("Knowledge check")
    st.caption("One question at a time, with immediate feedback and an explanation.")
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_checked" not in st.session_state:
        st.session_state.quiz_checked = False
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = set()
    index = st.session_state.quiz_index
    question, options, answer, explanation = QUESTIONS[index]
    st.progress((index + 1) / len(QUESTIONS), text=f"Question {index + 1} of {len(QUESTIONS)}")
    choice = st.radio(question, options, key=f"quiz-choice-{index}")
    if st.button("Check answer", type="primary"):
        if index not in st.session_state.quiz_answered:
            st.session_state.quiz_answered.add(index)
            st.session_state.quiz_checked = True
            if choice == answer:
                st.session_state.quiz_score += 1
        else:
            st.session_state.quiz_checked = True
        if choice == answer:
            st.success("Correct")
        else:
            st.error(f"Not quite. Correct answer: {answer}")
        st.caption(explanation)
    if st.session_state.quiz_checked and index < len(QUESTIONS) - 1:
        if st.button("Next question"):
            st.session_state.quiz_index += 1
            st.session_state.quiz_checked = False
            st.rerun()
    if st.session_state.quiz_checked and index == len(QUESTIONS) - 1:
        st.metric("Final score", f"{st.session_state.quiz_score}/{len(QUESTIONS)}")
    if st.button("Restart quiz"):
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_checked = False
        st.session_state.quiz_answered = set()
        st.rerun()
