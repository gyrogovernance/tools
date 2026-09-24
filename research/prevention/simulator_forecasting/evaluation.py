"""Leakage-free rolling-origin evaluation."""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List

import numpy as np
import pandas as pd


def origins(frame: pd.DataFrame, min_train: int, horizon: int) -> List[int]:
    return list(range(min_train, len(frame) - horizon + 1))


def point_metrics(actual: pd.DataFrame, forecast: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in actual.columns.intersection(forecast.columns):
        error = (forecast[column] - actual[column]).to_numpy(dtype=float)
        finite = np.isfinite(error)
        values = error[finite]
        rows.append({
            "series_id": column,
            "mae": float(np.mean(np.abs(values))) if len(values) else np.nan,
            "rmse": float(np.sqrt(np.mean(values ** 2))) if len(values) else np.nan,
            "bias": float(np.mean(values)) if len(values) else np.nan,
            "max_abs_error": float(np.max(np.abs(values))) if len(values) else np.nan,
            "n": int(len(values)),
        })
    return pd.DataFrame(rows)


def interval_metrics(actual: pd.DataFrame, quantiles: Dict[float, pd.DataFrame], lower: float = 0.1, upper: float = 0.9) -> pd.DataFrame:
    if lower not in quantiles or upper not in quantiles:
        return pd.DataFrame(columns=["series_id", "coverage", "mean_width"])
    rows = []
    for column in actual.columns.intersection(quantiles[lower].columns):
        y = actual[column].to_numpy(float)
        lo = quantiles[lower][column].to_numpy(float)
        hi = quantiles[upper][column].to_numpy(float)
        finite = np.isfinite(y) & np.isfinite(lo) & np.isfinite(hi)
        rows.append({
            "series_id": column,
            "coverage": float(np.mean((y[finite] >= lo[finite]) & (y[finite] <= hi[finite]))) if finite.any() else np.nan,
            "mean_width": float(np.mean(hi[finite] - lo[finite])) if finite.any() else np.nan,
        })
    return pd.DataFrame(rows)


def evaluate_model(frame: pd.DataFrame, model_name: str, forecast_fn: Callable, min_train: int, horizon: int) -> pd.DataFrame:
    records = []
    for origin in origins(frame, min_train, horizon):
        train = frame.iloc[:origin]
        actual = frame.iloc[origin:origin + horizon].copy()
        forecast_result = forecast_fn(train, horizon)
        if isinstance(forecast_result, tuple):
            forecast, quantiles = forecast_result
        else:
            forecast, quantiles = forecast_result, {}
        forecast.index = actual.index
        metrics = point_metrics(actual, forecast)
        intervals = interval_metrics(actual, quantiles)
        merged = metrics.merge(intervals, on="series_id", how="left")
        merged["model"] = model_name
        merged["origin"] = origin
        merged["horizon"] = horizon
        records.append(merged)
    return pd.concat(records, ignore_index=True) if records else pd.DataFrame()
