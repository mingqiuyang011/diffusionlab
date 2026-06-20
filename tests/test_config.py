"""Tests for configuration loading and validation."""

import json

import pytest

from diffusionlab.config import SimulationConfig, load_config, validate_config


def test_load_config_reads_required_values(tmp_path):
    """A JSON configuration file should be converted into SimulationConfig."""
    config_path = tmp_path / "config.json"
    config_data = {
        "n_particles": 10,
        "n_steps": 20,
        "step_length": 1.0,
        "time_step": 1.0,
        "seed": 42,
        "boundary": "none",
        "box_size": None,
        "save_every": 1,
    }
    config_path.write_text(json.dumps(config_data), encoding="utf-8")

    config = load_config(config_path)

    assert config.n_particles == 10
    assert config.n_steps == 20
    assert config.seed == 42


def test_invalid_particle_number_raises_value_error():
    """A simulation cannot have zero or negative particles."""
    config = SimulationConfig(
        n_particles=0,
        n_steps=10,
        step_length=1.0,
        time_step=1.0,
        seed=42,
    )

    with pytest.raises(ValueError, match="n_particles"):
        validate_config(config)


def test_reflecting_boundary_requires_positive_box_size():
    """Reflecting boundary conditions need a finite simulation box."""
    config = SimulationConfig(
        n_particles=10,
        n_steps=10,
        step_length=1.0,
        time_step=1.0,
        seed=42,
        boundary="reflecting",
        box_size=None,
    )

    with pytest.raises(ValueError, match="box_size"):
        validate_config(config)