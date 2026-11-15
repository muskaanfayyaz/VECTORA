"""Tests for the mathematical engine."""

import pytest
import sympy as sp

from calculations.force_fields import CONSERVATIVE_FIELD, NON_CONSERVATIVE_FIELD
from calculations.integrals import line_integral
from calculations.paths import PATHS
from calculations.verification import (
    symbolic_segment_integrand,
    symbolic_segment_work,
    verify_curl,
    verify_potential_gradient,
    verify_tolerance,
)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (CONSERVATIVE_FIELD, {"straight": -8.0, "horizontal_vertical": -8.0, "vertical_horizontal": -8.0}),
        (NON_CONSERVATIVE_FIELD, {"straight": 0.0, "horizontal_vertical": 4.0, "vertical_horizontal": -4.0}),
    ],
)
def test_all_field_path_combinations(field, expected):
    for path_key, value in expected.items():
        result = line_integral(field, PATHS[path_key])
        assert verify_tolerance(result, value)


def test_symbolic_properties():
    assert verify_curl(CONSERVATIVE_FIELD)
    assert verify_curl(NON_CONSERVATIVE_FIELD)
    assert verify_potential_gradient(CONSERVATIVE_FIELD)
    assert not verify_potential_gradient(NON_CONSERVATIVE_FIELD)
    assert sp.simplify(sp.diff(-2 * sp.Symbol("x"), sp.Symbol("x"))) == -2


@pytest.mark.parametrize("path", PATHS.values())
def test_path_endpoints(path):
    assert tuple(path.start) == (0.0, 0.0)
    assert tuple(path.end) == (2.0, 2.0)


def test_piecewise_segments_are_reported():
    result = line_integral(NON_CONSERVATIVE_FIELD, PATHS["horizontal_vertical"])
    assert len(result.segments) == 2
    assert result.segments[0].work == pytest.approx(0.0)
    assert result.segments[1].work == pytest.approx(4.0)


def test_symbolic_integrands_and_work():
    straight = PATHS["straight"].segments[0]
    horizontal = PATHS["horizontal_vertical"].segments[0]
    vertical = PATHS["horizontal_vertical"].segments[1]
    assert symbolic_segment_integrand(NON_CONSERVATIVE_FIELD, straight) == 0
    assert symbolic_segment_integrand(NON_CONSERVATIVE_FIELD, horizontal) == 0
    assert symbolic_segment_integrand(NON_CONSERVATIVE_FIELD, vertical) == 4
    assert symbolic_segment_work(CONSERVATIVE_FIELD, straight) == -8
