"""Transparent baselines for simulator trajectory forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _future_index(frame: pd.DataFrame, horizon: int) -> pd.Index:
    last = float(frame.index[-1])
    step = float(np.median(np.diff(frame.index))) if len(frame.index) > 1 else 1.0
    return pd.Index([last + step * i for i in range(1, horizon + 1)], name=frame.index.name)


def last_value_forecast(train: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return pd.DataFrame(np.tile(train.iloc[-1].to_numpy(), (horizon, 1)), index=_future_index(train, horizon), columns=train.columns)


def drift_forecast(train: pd.DataFrame, horizon: int) -> pd.DataFrame:
    values = train.astype(float)
    if len(values) < 2:
        return last_value_forecast(train, horizon)
    slope = values.iloc[-1] - values.iloc[-2]
    steps = np.arange(1, horizon + 1)[:, None]
    forecast = values.iloc[-1].to_numpy()[None, :] + steps * slope.to_numpy()[None, :]
    return pd.DataFrame(forecast, index=_future_index(train, horizon), columns=train.columns)


def linear_trend_forecast(train: pd.DataFrame, horizon: int) -> pd.DataFrame:
    values = train.astype(float)
    x = np.arange(len(values), dtype=float)
    future_x = np.arange(len(values), len(values) + horizon, dtype=float)
    result = {}
    for column in values.columns:
        y = values[column].to_numpy()
        slope, intercept = np.polyfit(x, y, 1) if len(y) >= 2 else (0.0, float(y[-1]))
        result[column] = intercept + slope * future_x
    return pd.DataFrame(result, index=_future_index(train, horizon))


BASELINES = {
    "last_value": last_value_forecast,
    "drift": drift_forecast,
    "linear_trend": linear_trend_forecast,
}
