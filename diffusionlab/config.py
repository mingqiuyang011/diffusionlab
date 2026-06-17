"""Configuration handling for DiffusionLab."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class SimulationConfig:
    """Parameters used by a random walk simulation."""

    n_particles: int
    n_steps: int
    step_length: float
    time_step: float
    seed: int
    boundary: str = "none"
    box_size: float | None = None
    save_every: int = 1


def load_config(path: str | Path) -> SimulationConfig:
    """Load and validate a simulation configuration from a JSON file."""
    config_path = Path(path)

    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    config = SimulationConfig(**data)
    validate_config(config)
    return config


def validate_config(config: SimulationConfig) -> None:
    """Validate user-facing simulation parameters."""
    if config.n_particles <= 0:
        raise ValueError("n_particles must be greater than 0.")

    if config.n_steps <= 0:
        raise ValueError("n_steps must be greater than 0.")

    if config.step_length <= 0:
        raise ValueError("step_length must be greater than 0.")

    if config.time_step <= 0:
        raise ValueError("time_step must be greater than 0.")

    if config.save_every <= 0:
        raise ValueError("save_every must be greater than 0.")

    allowed_boundaries = {"none", "reflecting"}
    if config.boundary not in allowed_boundaries:
        raise ValueError(
            f"boundary must be one of {sorted(allowed_boundaries)}."
        )

    if config.boundary == "reflecting":
        if config.box_size is None or config.box_size <= 0:
            raise ValueError(
                "box_size must be a positive number when boundary is reflecting."
            )
