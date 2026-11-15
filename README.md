# Line Integrals & Work Done by a Force

**VECTORA** is an interactive Streamlit simulator for project **PEF26-G13**. It compares a conservative field
`F = <-2x, -2y>` with the non-conservative field `F = <-y, x>` along three paths from
`A = (0, 0)` to `B = (2, 2)`.

## Features

- Field explorer with magnitude-colored quiver plots, curl, and potential information.
- Beginner-friendly Learn the basics center with analogies, formulas, and visual examples.
- Path simulator with configurable sampling resolution.
- Numerical, piecewise line integrals using SciPy.
- Symbolic curl and potential-gradient verification using SymPy.
- Comparison tables/charts, mathematical derivations, and an interactive quiz.
- About page documenting objectives, methodology, technologies, and limitations.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `pytest`.

## Expected results

| Field | Straight | Horizontal then vertical | Vertical then horizontal |
|---|---:|---:|---:|
| Conservative | -8 | -8 | -8 |
| Non-conservative | 0 | 4 | -4 |

These values are calculated by `calculations/integrals.py`, not hardcoded into the UI.
