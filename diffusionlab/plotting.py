"""Plotting routines for DiffusionLab."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from diffusionlab.io import ensure_directory


def plot_trajectories(
    trajectories: pd.DataFrame,
    output_path: str | Path,
    max_particles: int = 20,
) -> None:
    """Plot sample particle trajectories."""
    output_path = Path(output_path)
    ensure_directory(output_path.parent)

    selected_particles = trajectories["particle"].drop_duplicates().head(max_particles)

    fig, ax = plt.subplots()
    for particle_id in selected_particles:
        particle_data = trajectories[trajectories["particle"] == particle_id]
        ax.plot(particle_data["x"], particle_data["y"], linewidth=1)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Sample trajectories of 2D random walkers")
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_msd_fit(
    msd: pd.DataFrame,
    summary: dict,
    output_path: str | Path,
) -> None:
    """Plot MSD values and the fitted diffusion line."""
    output_path = Path(output_path)
    ensure_directory(output_path.parent)

    slope = summary["fit_slope"]
    intercept = summary["fit_intercept"]
    fitted_msd = slope * msd["time"] + intercept

    fig, ax = plt.subplots()
    ax.plot(msd["time"], msd["msd"], label="Simulation MSD")
    ax.plot(msd["time"], fitted_msd, linestyle="--", label="Linear fit")

    estimated_d = summary["estimated_diffusion_coefficient"]
    theoretical_d = summary["theoretical_diffusion_coefficient"]

    ax.set_xlabel("time")
    ax.set_ylabel("MSD")
    ax.set_title(
        f"MSD fit: estimated D={estimated_d:.4f}, theoretical D={theoretical_d:.4f}"
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)