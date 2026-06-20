"""Tests for random walk simulation routines."""

import numpy as np
import pandas as pd

from diffusionlab.config import SimulationConfig
from diffusionlab.random_walk import (
    apply_reflecting_boundary,
    generate_lattice_steps,
    initialize_positions,
    simulate_random_walk,
)


def test_initialize_positions_starts_all_particles_at_origin():
    """All particles should start at x=0 and y=0."""
    positions = initialize_positions(5)

    assert positions.shape == (5, 2)
    assert np.allclose(positions, 0.0)


def test_generated_steps_have_expected_length():
    """Each lattice step should have length equal to step_length."""
    rng = np.random.default_rng(42)
    steps = generate_lattice_steps(
        n_particles=100,
        step_length=2.0,
        rng=rng,
    )

    lengths = np.sqrt(steps[:, 0] ** 2 + steps[:, 1] ** 2)
    assert np.allclose(lengths, 2.0)


def test_same_seed_produces_same_trajectories():
    """Using the same random seed should make simulations reproducible."""
    config = SimulationConfig(
        n_particles=10,
        n_steps=20,
        step_length=1.0,
        time_step=1.0,
        seed=123,
    )

    first = simulate_random_walk(config)
    second = simulate_random_walk(config)

    pd.testing.assert_frame_equal(first, second)


def test_reflecting_boundary_keeps_positions_inside_box():
    """Positions outside the box should be reflected back inside."""
    positions = np.array(
        [
            [6.0, 0.0],
            [-6.0, 0.0],
            [0.0, 6.0],
            [0.0, -6.0],
        ]
    )

    reflected = apply_reflecting_boundary(positions, box_size=10.0)

    assert np.all(reflected <= 5.0)
    assert np.all(reflected >= -5.0)