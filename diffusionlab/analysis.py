"""Analysis routines for random walk trajectories."""

from __future__ import annotations

import numpy as np
import pandas as pd

from diffusionlab.config import SimulationConfig


def compute_msd(trajectories: pd.DataFrame) -> pd.DataFrame:
    """Compute mean squared displacement for each recorded time step."""
    required_columns = {"step", "time", "particle", "x", "y"}
    missing_columns = required_columns.difference(trajectories.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    data = trajectories.copy()
    data["squared_displacement"] = data["x"] ** 2 + data["y"] ** 2

    msd = (
        data.groupby(["step", "time"], as_index=False)["squared_displacement"]
        .mean()
        .rename(columns={"squared_displacement": "msd"})
    )

    return msd


def fit_diffusion_coefficient(msd: pd.DataFrame) -> dict[str, float]:
    """Estimate the 2D diffusion coefficient from MSD(t) = 4Dt."""
    if len(msd) < 2:
        raise ValueError("At least two MSD points are required for fitting.")

    slope, intercept = np.polyfit(msd["time"], msd["msd"], deg=1)
    estimated_diffusion = slope / 4.0

    return {
        "fit_slope": float(slope),
        "fit_intercept": float(intercept),
        "estimated_diffusion_coefficient": float(estimated_diffusion),
    }


def theoretical_diffusion_coefficient(config: SimulationConfig) -> float:
    """Return the theoretical diffusion coefficient for a 2D lattice walk."""
    return config.step_length**2 / (4.0 * config.time_step)


def summarize_results(
    msd: pd.DataFrame,
    config: SimulationConfig,
) -> dict[str, float | int | str | None]:
    """Create a summary dictionary for a simulation result."""
    fit = fit_diffusion_coefficient(msd)
    theoretical = theoretical_diffusion_coefficient(config)
    estimated = fit["estimated_diffusion_coefficient"]

    relative_error = abs(estimated - theoretical) / theoretical

    return {
        **fit,
        "theoretical_diffusion_coefficient": float(theoretical),
        "relative_error": float(relative_error),
        "n_particles": config.n_particles,
        "n_steps": config.n_steps,
        "step_length": config.step_length,
        "time_step": config.time_step,
        "seed": config.seed,
        "boundary": config.boundary,
        "box_size": config.box_size,
    }