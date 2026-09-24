"""Forecast schema for simulator-generated trajectories only."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple

A_STAR = 0.0207

APERTURE_CHANNELS = ("A_Econ", "A_Emp", "A_Edu")
SI_CHANNELS = ("SI_Econ", "SI_Emp", "SI_Edu")
DISPLACEMENT_CHANNELS = ("GTD", "IVD", "IAD", "IID")

PRIMARY_GROUPS: Dict[str, Tuple[str, ...]] = {
    "aperture": ("A_Econ", "A_Emp", "A_Edu", "A_Ecol"),
    "alignment": ("SI_Econ", "SI_Emp", "SI_Edu", "SI_Ecol"),
    "lyapunov": ("V_CGM", "V_grad_total", "V_cycle_total"),
    "displacement": ("GTD", "IVD", "IAD", "IID"),
}

SCENARIO_NAMES = (
    "weak_coupling", "canonical", "strong_coupling", "low_aperture",
    "asymmetric", "at_astar", "uniform_weights",
)


@dataclass(frozen=True)
class ForecastConfig:
    context_length: int = 40
    horizon: int = 10
    min_train: int = 40
    quantiles: Tuple[float, ...] = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    device: str = "cpu"
    model: str = "timesfm"

    def to_dict(self) -> dict:
        return asdict(self)


def available_channels(columns) -> Dict[str, Tuple[str, ...]]:
    columns = set(columns)
    return {
        group: tuple(channel for channel in channels if channel in columns)
        for group, channels in PRIMARY_GROUPS.items()
    }


def selected_channels(columns) -> Tuple[str, ...]:
    grouped = available_channels(columns)
    return tuple(dict.fromkeys(channel for channels in grouped.values() for channel in channels))
