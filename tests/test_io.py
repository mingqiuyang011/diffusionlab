"""Tests for input and output helpers."""

import pandas as pd

from diffusionlab.io import load_dataframe, save_dataframe, save_json


def test_save_and_load_dataframe_preserves_values(tmp_path):
    """A saved CSV file should be readable without changing table values."""
    path = tmp_path / "data.csv"
    data = pd.DataFrame(
        {
            "step": [0, 1],
            "x": [0.0, 1.0],
            "y": [0.0, -1.0],
        }
    )

    save_dataframe(data, path)
    loaded = load_dataframe(path)

    pd.testing.assert_frame_equal(data, loaded)


def test_save_json_creates_output_file(tmp_path):
    """Summary dictionaries should be saved as JSON files."""
    path = tmp_path / "summary.json"

    save_json({"estimated_diffusion_coefficient": 0.25}, path)

    assert path.exists()