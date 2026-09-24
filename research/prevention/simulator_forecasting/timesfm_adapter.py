"""Zero-shot TimesFM 3 adapter for simulator trajectories."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Optional

import numpy as np
import pandas as pd

from .baselines import _future_index
from .schema import ForecastConfig

DEFAULT_CHECKPOINT = "google/timesfm-3.0-pytorch"
WEIGHT_LICENSE = "timesfm-non-commercial-license-v1.0"


class TimesFMUnavailableError(RuntimeError):
    pass


class TimesFMAdapter:
    """Frozen TimesFM inference wrapper with no training interface."""

    def __init__(self, config: Optional[ForecastConfig] = None):
        self.config = config or ForecastConfig()
        self._forecaster = None

    def ensure_loaded(self) -> None:
        if self._forecaster is not None:
            return
        try:
            from timesfm3 import TimesFM3Forecaster
            self._forecaster = TimesFM3Forecaster.from_pretrained(
                DEFAULT_CHECKPOINT, device=self.config.device
            )
        except Exception as exc:
            raise TimesFMUnavailableError(str(exc)) from exc

    def predict(self, train: pd.DataFrame, horizon: Optional[int] = None) -> tuple[pd.DataFrame, dict[float, pd.DataFrame]]:
        self.ensure_loaded()
        horizon = horizon or self.config.horizon
        context = train.astype(float).to_numpy(dtype=np.float32).T
        output = self._forecaster.predict(
            context=context,
            horizon=horizon,
            return_quantiles=True,
            use_symmetric_averaging=True,
            make_positive=False,
            sort_quantiles=True,
            use_znorm=False,
            padding_mode="none",
            ts_id="ggg_simulator_trajectory",
        )
        values = np.asarray(output.forecast)
        if values.ndim == 1:
            values = values[:, None]
        elif values.shape[0] == len(train.columns) and values.shape[1] == horizon:
            values = values.T
        index = _future_index(train, horizon)
        point = pd.DataFrame(values, index=index, columns=train.columns)
        quantiles = {}
        raw = output.quantiles
        if raw is not None:
            raw = np.asarray(raw)
            if raw.ndim == 3:
                # TimesFM returns [series, horizon, quantile].
                for i, quantile in enumerate(self.config.quantiles):
                    quantiles[float(quantile)] = pd.DataFrame(raw[:, :, i].T, index=index, columns=train.columns)
            elif raw.ndim == 2:
                for i, quantile in enumerate(self.config.quantiles):
                    quantiles[float(quantile)] = pd.DataFrame(raw[:, i:i + 1], index=index, columns=train.columns)
        return point, quantiles

    def manifest(self, scenario: str, channels: list[str]) -> dict:
        payload = {"scenario": scenario, "channels": channels, "config": asdict(self.config), "checkpoint": DEFAULT_CHECKPOINT, "weight_license": WEIGHT_LICENSE}
        payload["config_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]
        return payload
