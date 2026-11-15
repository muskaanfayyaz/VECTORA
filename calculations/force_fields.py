"""Definitions and symbolic properties of the force fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

Point = tuple[float, float]
VectorFunction = Callable[[float, float], tuple[float, float]]


@dataclass(frozen=True)
class ForceField:
    """A two-dimensional vector field and its analytical metadata."""

    key: str
    name: str
    equation: str
    function: VectorFunction
    potential: str | None
    curl: float
    description: str
    symbolic_x: sp.Expr
    symbolic_y: sp.Expr

    def evaluate(self, point: Point) -> np.ndarray:
        """Evaluate the field at a point."""
        values = self.function(*point)
        return np.asarray(values, dtype=float)


X, Y = sp.symbols("x y", real=True)


def conservative_force(x: float, y: float) -> tuple[float, float]:
    return -2.0 * x, -2.0 * y


def non_conservative_force(x: float, y: float) -> tuple[float, float]:
    return -y, x


CONSERVATIVE_FIELD = ForceField(
    key="conservative",
    name="Conservative field",
    equation=r"\mathbf{F}(x,y)=\langle -2x,-2y\rangle",
    function=conservative_force,
    potential=r"\phi(x,y)=-(x^2+y^2)",
    curl=0.0,
    description="The field points toward the origin and has path-independent work.",
    symbolic_x=-2 * X,
    symbolic_y=-2 * Y,
)

NON_CONSERVATIVE_FIELD = ForceField(
    key="non_conservative",
    name="Non-conservative field",
    equation=r"\mathbf{F}(x,y)=\langle -y,x\rangle",
    function=non_conservative_force,
    potential=None,
    curl=2.0,
    description="The field circulates counterclockwise, so work depends on the path.",
    symbolic_x=-Y,
    symbolic_y=X,
)

FIELDS: dict[str, ForceField] = {
    CONSERVATIVE_FIELD.key: CONSERVATIVE_FIELD,
    NON_CONSERVATIVE_FIELD.key: NON_CONSERVATIVE_FIELD,
}


def get_field(key: str) -> ForceField:
    """Return a registered force field or raise a clear error."""
    try:
        return FIELDS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown force field: {key}") from exc


def symbolic_curl(field: ForceField) -> sp.Expr:
    """Compute the scalar two-dimensional curl symbolically."""
    return sp.simplify(sp.diff(field.symbolic_y, X) - sp.diff(field.symbolic_x, Y))


def symbolic_gradient(field: ForceField) -> sp.Matrix | None:
    """Return the gradient of a potential when the field has one."""
    if field.potential is None:
        return None
    potential = -(X**2 + Y**2)
    return sp.Matrix([sp.diff(potential, X), sp.diff(potential, Y)])
