"""Random walk simulation routines."""

from __future__ import annotations

import numpy as np
import pandas as pd

from diffusionlab.config import SimulationConfig


def initialize_positions(n_particles: int) -> np.ndarray:
    """Return initial particle positions at the origin."""
    if n_particles <= 0:
        raise ValueError("n_particles must be greater than 0.")

    return np.zeros((n_particles, 2), dtype=float)


def generate_lattice_steps(
    n_particles: int,
    step_length: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate one random 2D lattice step for each particle."""
    directions = np.array(
        [
            [1.0, 0.0],
            [-1.0, 0.0],
            [0.0, 1.0],
            [0.0, -1.0],
        ]
    )
    choices = rng.integers(0, len(directions), size=n_particles)
    return directions[choices] * step_length


def apply_reflecting_boundary(
    positions: np.ndarray,
    box_size: float,
) -> np.ndarray:
    """Reflect positions back into a square box centered at the origin."""
    half_box = box_size / 2.0
    reflected = positions.copy()

    reflected = np.where(reflected > half_box, 2 * half_box - reflected, reflected)
    reflected = np.where(reflected < -half_box, -2 * half_box - reflected, reflected)

    return reflected


def simulate_random_walk(config: SimulationConfig) -> pd.DataFrame:
    """Simulate a 2D random walk and return trajectories as a DataFrame."""
    rng = np.random.default_rng(config.seed)
    positions = initialize_positions(config.n_particles)

    records = []
    for step in range(config.n_steps + 1):
        if step % config.save_every == 0:
            for particle_id, (x_position, y_position) in enumerate(positions):
                records.append(
                    {
                        "step": step,
                        "time": step * config.time_step,
                        "particle": particle_id,
                        "x": x_position,
                        "y": y_position,
                    }
                )

        if step < config.n_steps:
            positions = positions + generate_lattice_steps(
                config.n_particles,
                config.step_length,
                rng,
            )

            if config.boundary == "reflecting":
                positions = apply_reflecting_boundary(
                    positions,
                    box_size=config.box_size,
                )

    return pd.DataFrame.from_records(records)