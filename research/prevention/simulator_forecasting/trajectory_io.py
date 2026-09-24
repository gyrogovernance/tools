"""I/O helpers for simulator-generated trajectories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pandas as pd

SIMULATOR_DIR = Path(__file__).resolve().parent.parent / "simulator"


def load_trajectory(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    time_column = next((c for c in frame.columns if c.startswith("time (")), None)
    if time_column is None:
        raise ValueError("Trajectory CSV must contain a simulator time column")
    frame = frame.set_index(time_column)
    frame.index.name = "step"
    return frame.apply(pd.to_numeric, errors="coerce")


def save_trajectory(frame: pd.DataFrame, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    output = frame.copy()
    output.index.name = "time (steps)"
    output.to_csv(path)
    return path


def write_json(payload: dict, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def scenario_csv_paths(results_dir: str | Path = SIMULATOR_DIR / "results") -> Dict[str, Path]:
    directory = Path(results_dir)
    return {
        "weak_coupling": directory / "scenario1_weak.csv",
        "canonical": directory / "scenario2_canonical.csv",
        "strong_coupling": directory / "scenario3_strong.csv",
        "low_aperture": directory / "scenario4_low_a.csv",
        "asymmetric": directory / "scenario5_asymmetric.csv",
        "at_astar": directory / "scenario6_at_astar.csv",
        "uniform_weights": directory / "scenario7_uniform.csv",
    }


def load_existing_trajectories(results_dir: str | Path = SIMULATOR_DIR / "results") -> Dict[str, pd.DataFrame]:
    return {name: load_trajectory(path) for name, path in scenario_csv_paths(results_dir).items() if path.exists()}
