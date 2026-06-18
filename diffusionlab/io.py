"""Input and output utilities for DiffusionLab."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not already exist."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_dataframe(data: pd.DataFrame, path: str | Path) -> None:
    """Save a DataFrame as CSV."""
    output_path = Path(path)
    ensure_directory(output_path.parent)
    data.to_csv(output_path, index=False)


def load_dataframe(path: str | Path) -> pd.DataFrame:
    """Load a CSV file as a DataFrame."""
    return pd.read_csv(path)


def save_json(data: dict, path: str | Path) -> None:
    """Save a dictionary as a JSON file."""
    output_path = Path(path)
    ensure_directory(output_path.parent)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)