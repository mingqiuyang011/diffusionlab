"""Command-line interface for DiffusionLab."""

from __future__ import annotations

import argparse
from pathlib import Path

from diffusionlab.analysis import compute_msd, summarize_results
from diffusionlab.config import load_config
from diffusionlab.io import save_dataframe, save_json
from diffusionlab.plotting import plot_msd_fit, plot_trajectories
from diffusionlab.random_walk import simulate_random_walk


def run_pipeline(config_path: str | Path, output_directory: str | Path) -> None:
    """Run simulation, analysis, and plotting from a configuration file."""
    config = load_config(config_path)
    output_directory = Path(output_directory)

    trajectories = simulate_random_walk(config)
    msd = compute_msd(trajectories)
    summary = summarize_results(msd, config)

    save_dataframe(trajectories, output_directory / "trajectories.csv")
    save_dataframe(msd, output_directory / "msd.csv")
    save_json(summary, output_directory / "summary.json")

    plot_trajectories(trajectories, output_directory / "trajectories.png")
    plot_msd_fit(msd, summary, output_directory / "msd_fit.png")

    print(f"Results written to: {output_directory}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Simulate 2D random walks and estimate diffusion coefficients."
        )
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Run simulation, analysis, and plotting.",
    )
    run_parser.add_argument(
        "--config",
        required=True,
        help="Path to a JSON configuration file.",
    )
    run_parser.add_argument(
        "--out",
        required=True,
        help="Directory where output files will be written.",
    )

    return parser


def main() -> None:
    """Entry point for the diffusionlab command."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        run_pipeline(args.config, args.out)