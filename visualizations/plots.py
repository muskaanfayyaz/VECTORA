"""Matplotlib figures generated from the mathematical engine."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from calculations.force_fields import ForceField
from calculations.integrals import IntegralResult
from calculations.paths import Path


def vector_field_plot(field: ForceField, extent: tuple[float, float] = (-3, 3), density: int = 17):
    if density < 5:
        raise ValueError("density must be at least 5")
    x = np.linspace(*extent, density)
    y = np.linspace(*extent, density)
    xx, yy = np.meshgrid(x, y)
    u, v = field.function(xx, yy)
    magnitude = np.hypot(u, v)
    fig, ax = plt.subplots(figsize=(8, 5))
    contour = ax.contourf(xx, yy, magnitude, levels=20, cmap="viridis", alpha=0.72)
    ax.quiver(xx, yy, u, v, color="white", alpha=0.9, pivot="mid")
    ax.set(xlabel="x", ylabel="y", title=field.name)
    ax.axhline(0, color="#263238", lw=0.8)
    ax.axvline(0, color="#263238", lw=0.8)
    fig.colorbar(contour, ax=ax, label="Force magnitude")
    fig.tight_layout()
    return fig


def path_plot(field: ForceField, path: Path, resolution: int = 100):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(-0.2, 2.2, 14)
    y = np.linspace(-0.2, 2.2, 14)
    xx, yy = np.meshgrid(x, y)
    u, v = field.function(xx, yy)
    ax.quiver(xx, yy, u, v, color="#90a4ae", alpha=0.65)
    for segment in path.segments:
        points = segment.sample(resolution)
        ax.plot(points[:, 0], points[:, 1], lw=3, label=segment.name)
    ax.scatter([0, 2], [0, 2], c=["#00bcd4", "#ff7043"], s=70, zorder=3)
    ax.annotate("A (0, 0)", (0, 0), xytext=(5, 6), textcoords="offset points")
    ax.annotate("B (2, 2)", (2, 2), xytext=(5, 6), textcoords="offset points")
    ax.set(xlim=(-0.2, 2.2), ylim=(-0.2, 2.2), xlabel="x", ylabel="y", title=path.name)
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def paths_overview_plot(field: ForceField, paths: tuple[Path, ...], resolution: int = 80):
    """Plot all comparison paths together while keeping the endpoints fixed."""
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(-0.2, 2.2, 14)
    y = np.linspace(-0.2, 2.2, 14)
    xx, yy = np.meshgrid(x, y)
    u, v = field.function(xx, yy)
    ax.quiver(xx, yy, u, v, color="#90a4ae", alpha=0.45)
    colors = ("#00a6a6", "#ef8354", "#5e60ce")
    for path, color in zip(paths, colors):
        for segment in path.segments:
            points = segment.sample(resolution)
            ax.plot(points[:, 0], points[:, 1], color=color, lw=3, label=path.name if segment is path.segments[0] else None)
    ax.scatter([0, 2], [0, 2], c=["#00bcd4", "#ff7043"], s=75, zorder=3)
    ax.annotate("A (0, 0)", (0, 0), xytext=(5, 6), textcoords="offset points")
    ax.annotate("B (2, 2)", (2, 2), xytext=(5, 6), textcoords="offset points")
    ax.set(xlim=(-0.2, 2.2), ylim=(-0.2, 2.2), xlabel="x", ylabel="y", title=f"Three routes through {field.name.lower()}")
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def work_comparison_plot(results: dict[str, dict[str, float]]):
    labels = list(next(iter(results.values())).keys())
    fields = list(results)
    values = np.array([[results[field][label] for label in labels] for field in fields])
    fig, ax = plt.subplots(figsize=(9, 5))
    width = 0.35
    positions = np.arange(len(labels))
    for index, field in enumerate(fields):
        ax.bar(positions + (index - 0.5) * width, values[index], width, label=field)
    ax.axhline(0, color="#263238", lw=0.8)
    ax.set_xticks(positions, labels, rotation=15)
    ax.set_ylabel("Work")
    ax.set_title("Work along each path")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig
