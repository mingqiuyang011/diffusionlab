"""Tests for MSD and diffusion coefficient analysis."""

import pandas as pd
import pytest

from diffusionlab.analysis import compute_msd, fit_diffusion_coefficient


def test_compute_msd_for_known_positions():
    """MSD should match hand-calculated squared displacements."""
    trajectories = pd.DataFrame(
        {
            "step": [0, 0, 1, 1],
            "time": [0.0, 0.0, 1.0, 1.0],
            "particle": [0, 1, 0, 1],
            "x": [0.0, 0.0, 3.0, 0.0],
            "y": [0.0, 0.0, 4.0, 2.0],
        }
    )

    msd = compute_msd(trajectories)

    step_one_msd = msd.loc[msd["step"] == 1, "msd"].iloc[0]
    assert step_one_msd == pytest.approx(14.5)


def test_fit_diffusion_coefficient_from_linear_msd():
    """For MSD = 4Dt with D=0.25, the estimated D should be 0.25."""
    msd = pd.DataFrame(
        {
            "step": [0, 1, 2, 3],
            "time": [0.0, 1.0, 2.0, 3.0],
            "msd": [0.0, 1.0, 2.0, 3.0],
        }
    )

    result = fit_diffusion_coefficient(msd)

    assert result["fit_slope"] == pytest.approx(1.0)
    assert result["estimated_diffusion_coefficient"] == pytest.approx(0.25)