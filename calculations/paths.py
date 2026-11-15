"""Parameterized curves used by the simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

Point = tuple[float, float]
ArrayFunction = Callable[[float], np.ndarray]


@dataclass(frozen=True)
class Segment:
    """One parameterized path segment over t in [0, 1]."""

    name: str
    curve: ArrayFunction
    derivative: ArrayFunction
    formula: str
    symbolic_curve: tuple[sp.Expr, sp.Expr]
    symbolic_derivative: tuple[sp.Expr, sp.Expr]

    def sample(self, resolution: int = 100) -> np.ndarray:
        """Sample the segment, including both endpoints."""
        if resolution < 2:
            raise ValueError("resolution must be at least 2")
        return np.array([self.curve(t) for t in np.linspace(0.0, 1.0, resolution)])


@dataclass(frozen=True)
class Path:
    """A possibly piecewise path from a start to an end point."""

    key: str
    name: str
    segments: tuple[Segment, ...]
    description: str

    @property
    def start(self) -> np.ndarray:
        return self.segments[0].curve(0.0)

    @property
    def end(self) -> np.ndarray:
        return self.segments[-1].curve(1.0)


def _segment(
    name: str,
    curve: ArrayFunction,
    derivative: ArrayFunction,
    formula: str,
    symbolic_curve: tuple[sp.Expr, sp.Expr],
    symbolic_derivative: tuple[sp.Expr, sp.Expr],
) -> Segment:
    return Segment(name, curve, derivative, formula, symbolic_curve, symbolic_derivative)


t = sp.symbols("t", real=True)


PATHS: dict[str, Path] = {
    "straight": Path(
        "straight",
        "Straight line",
        (_segment("Straight segment", lambda value: np.array([2 * value, 2 * value]), lambda _value: np.array([2.0, 2.0]), r"\mathbf r(t)=\langle2t,2t\rangle", (2 * t, 2 * t), (2, 2)),),
        "A direct diagonal path from A to B.",
    ),
    "horizontal_vertical": Path(
        "horizontal_vertical",
        "Horizontal then vertical",
        (
            _segment("Horizontal segment", lambda value: np.array([2 * value, 0.0]), lambda _value: np.array([2.0, 0.0]), r"\mathbf r_1(t)=\langle2t,0\rangle", (2 * t, 0), (2, 0)),
            _segment("Vertical segment", lambda value: np.array([2.0, 2 * value]), lambda _value: np.array([0.0, 2.0]), r"\mathbf r_2(t)=\langle2,2t\rangle", (2, 2 * t), (0, 2)),
        ),
        "Move along the x-axis, then straight up.",
    ),
    "vertical_horizontal": Path(
        "vertical_horizontal",
        "Vertical then horizontal",
        (
            _segment("Vertical segment", lambda value: np.array([0.0, 2 * value]), lambda _value: np.array([0.0, 2.0]), r"\mathbf r_1(t)=\langle0,2t\rangle", (0, 2 * t), (0, 2)),
            _segment("Horizontal segment", lambda value: np.array([2 * value, 2.0]), lambda _value: np.array([2.0, 0.0]), r"\mathbf r_2(t)=\langle2t,2\rangle", (2 * t, 2), (2, 0)),
        ),
        "Move upward first, then across to B.",
    ),
}


def get_path(key: str) -> Path:
    """Return a registered path or raise a clear error."""
    try:
        return PATHS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown path: {key}") from exc
