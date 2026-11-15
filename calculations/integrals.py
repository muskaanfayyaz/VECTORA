"""Numerical line-integral calculations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from calculations.force_fields import ForceField
from calculations.paths import Path, Segment


@dataclass(frozen=True)
class SegmentResult:
    """Detailed work calculation for one segment."""

    segment: Segment
    work: float
    error: float


@dataclass(frozen=True)
class IntegralResult:
    """Total work and its piecewise contributions."""

    field: ForceField
    path: Path
    segments: tuple[SegmentResult, ...]

    @property
    def work(self) -> float:
        return sum(segment.work for segment in self.segments)

    @property
    def error(self) -> float:
        return sum(segment.error for segment in self.segments)


def integrate_segment(field: ForceField, segment: Segment, tolerance: float = 1e-10) -> SegmentResult:
    """Integrate F(r(t)) dot r'(t) from t=0 to 1."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    def integrand(t: float) -> float:
        point = segment.curve(t)
        force = field.evaluate((float(point[0]), float(point[1])))
        return float(np.dot(force, segment.derivative(t)))

    work, error = quad(integrand, 0.0, 1.0, epsabs=tolerance, epsrel=tolerance)
    return SegmentResult(segment, float(work), float(error))


def line_integral(field: ForceField, path: Path, tolerance: float = 1e-10) -> IntegralResult:
    """Integrate work over every path segment and sum the results."""
    return IntegralResult(
        field=field,
        path=path,
        segments=tuple(integrate_segment(field, segment, tolerance) for segment in path.segments),
    )
