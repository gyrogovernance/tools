"""GGG-native preference scoring for forecasted simulator continuations."""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd

from .schema import A_STAR, APERTURE_CHANNELS, DISPLACEMENT_CHANNELS, SI_CHANNELS


def _available(frame: pd.DataFrame, channels) -> list[str]:
    return [channel for channel in channels if channel in frame.columns]


def _mean_abs_second_diff(series: np.ndarray) -> float:
    if len(series) < 3:
        return 0.0
    second = np.diff(series, n=2)
    finite = second[np.isfinite(second)]
    return float(np.mean(np.abs(finite))) if len(finite) else 0.0


def _relative_progress(end_value: float, start_value: float) -> float:
    scale = abs(start_value) + 1e-8
    return float(-(end_value - start_value) / scale)


def _certainty(point: pd.DataFrame, quantiles: Dict[float, pd.DataFrame], channels: list[str]) -> float:
    if 0.1 not in quantiles or 0.9 not in quantiles:
        return np.nan
    widths = []
    for channel in channels:
        if channel not in point.columns:
            continue
        width = (quantiles[0.9][channel] - quantiles[0.1][channel]).to_numpy(float)
        center = np.abs(point[channel].to_numpy(float)) + 1e-8
        finite = np.isfinite(width) & np.isfinite(center)
        if finite.any():
            widths.append(np.mean(width[finite] / center[finite]))
    if not widths:
        return np.nan
    return float(1.0 / (1.0 + np.mean(widths)))


def score_continuation(
    history: pd.DataFrame,
    continuation: pd.DataFrame,
    quantiles: Optional[Dict[float, pd.DataFrame]] = None,
    a_star: float = A_STAR,
) -> dict:
    """Score a continuation window under GGG alignment objectives.

    Higher component values indicate a more preferred continuation. The composite
    preference score averages the available finite components.
    """
    history = history.astype(float)
    continuation = continuation.astype(float)
    last = history.iloc[-1]
    scores: dict[str, float] = {}

    si_channels = _available(continuation, SI_CHANNELS)
    if si_channels:
        si_values = continuation[si_channels].to_numpy(float)
        scores["si_level"] = float(np.nanmean(si_values) / 100.0)
        start_si = float(np.nanmean([last[channel] for channel in si_channels if channel in last.index]))
        end_si = float(np.nanmean(si_values[-max(1, len(continuation) // 3):]))
        scores["si_progress"] = float((end_si - start_si) / 100.0)
        scores["smoothness"] = float(1.0 / (1.0 + np.mean([
            _mean_abs_second_diff(continuation[channel].to_numpy(float)) for channel in si_channels
        ])))

    aperture_channels = _available(continuation, APERTURE_CHANNELS)
    if aperture_channels:
        deviations = []
        for channel in aperture_channels:
            deviations.append(np.abs(continuation[channel].to_numpy(float) - a_star) / a_star)
        scores["aperture_proximity"] = float(1.0 / (1.0 + np.nanmean(np.vstack(deviations))))

    if "V_CGM" in continuation.columns and "V_CGM" in last.index:
        scores["lyapunov_relief"] = _relative_progress(
            float(continuation["V_CGM"].iloc[-1]), float(last["V_CGM"])
        )

    displacement_channels = _available(continuation, DISPLACEMENT_CHANNELS)
    if displacement_channels:
        disp = continuation[displacement_channels].to_numpy(float)
        scores["displacement_level"] = float(1.0 / (1.0 + np.nanmean(disp)))
        start_disp = float(np.nanmean([last[channel] for channel in displacement_channels if channel in last.index]))
        end_disp = float(np.nanmean(disp[-1]))
        scores["displacement_relief"] = _relative_progress(end_disp, start_disp)

    if quantiles:
        certainty_channels = si_channels + aperture_channels
        certainty = _certainty(continuation, quantiles, certainty_channels)
        if np.isfinite(certainty):
            scores["certainty"] = certainty

    finite = [value for value in scores.values() if np.isfinite(value)]
    scores["preference_score"] = float(np.mean(finite)) if finite else np.nan
    return scores


def rank_preference_table(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["rank"] = frame.groupby(["origin", "horizon", "source"])["preference_score"].rank(
        ascending=False, method="average"
    )
    return frame.sort_values(["origin", "horizon", "source", "rank", "scenario"]).reset_index(drop=True)
