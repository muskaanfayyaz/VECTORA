"""Independent symbolic and numerical verification helpers."""

from __future__ import annotations

import sympy as sp

from calculations.force_fields import ForceField, X, Y, symbolic_curl
from calculations.integrals import IntegralResult
from calculations.paths import Segment


def verify_curl(field: ForceField) -> bool:
    """Verify that the symbolic curl equals the stored metadata."""
    return bool(sp.simplify(symbolic_curl(field) - field.curl) == 0)


def verify_potential_gradient(field: ForceField) -> bool:
    """Verify the conservative field's potential gradient."""
    if field.potential is None:
        return False
    potential = -(X**2 + Y**2)
    gradient = sp.Matrix([sp.diff(potential, X), sp.diff(potential, Y)])
    return bool(gradient == sp.Matrix([field.symbolic_x, field.symbolic_y]))


def verify_tolerance(result: IntegralResult, expected: float, tolerance: float = 1e-8) -> bool:
    """Check a numerical result against an independently supplied analytical value."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    return abs(result.work - expected) <= tolerance


def symbolic_segment_integrand(field: ForceField, segment: Segment) -> sp.Expr:
    """Return the exact symbolic integrand F(r(t)) dot r'(t)."""
    fx = field.symbolic_x.subs({X: segment.symbolic_curve[0], Y: segment.symbolic_curve[1]})
    fy = field.symbolic_y.subs({X: segment.symbolic_curve[0], Y: segment.symbolic_curve[1]})
    return sp.simplify(fx * segment.symbolic_derivative[0] + fy * segment.symbolic_derivative[1])


def symbolic_segment_work(field: ForceField, segment: Segment) -> sp.Expr:
    """Integrate one segment exactly over t in [0, 1]."""
    return sp.simplify(sp.integrate(symbolic_segment_integrand(field, segment), (sp.Symbol("t", real=True), 0, 1)))
