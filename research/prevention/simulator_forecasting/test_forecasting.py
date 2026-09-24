"""Tests for simulator-only forecasting and scenario preference ranking."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .baselines import drift_forecast, last_value_forecast
from .evaluation import evaluate_model, point_metrics
from .scenario_ranking import rank_scenarios, ranking_agreement, summarize_rankings
from .scenario_scoring import score_continuation
from .schema import A_STAR, selected_channels


def test_primary_channels_are_simulator_channels():
    columns = ["A_Econ", "SI_Econ", "V_CGM", "GTD", "GDP"]
    assert selected_channels(columns) == ("A_Econ", "SI_Econ", "V_CGM", "GTD")


def test_baselines_preserve_horizon_and_columns():
    frame = pd.DataFrame({"SI_Econ": [1.0, 2.0, 3.0], "A_Econ": [0.1, 0.2, 0.3]}, index=[0, 1, 2])
    for forecast_fn in (last_value_forecast, drift_forecast):
        forecast = forecast_fn(frame, 2)
        assert forecast.shape == (2, 2)
        assert list(forecast.columns) == list(frame.columns)


def test_rolling_origin_uses_future_only_for_scoring():
    frame = pd.DataFrame({"SI_Econ": np.arange(20, dtype=float)}, index=np.arange(20))
    results = evaluate_model(frame, "last", last_value_forecast, min_train=10, horizon=3)
    assert len(results) == 8
    assert set(results["origin"]) == set(range(10, 18))
    assert (results["n"] == 3).all()


def test_point_metrics_are_per_series():
    actual = pd.DataFrame({"A": [1.0, 2.0], "B": [10.0, 20.0]})
    forecast = pd.DataFrame({"A": [2.0, 2.0], "B": [8.0, 24.0]})
    metrics = point_metrics(actual, forecast).set_index("series_id")
    assert metrics.loc["A", "mae"] == 0.5
    assert metrics.loc["B", "mae"] == 3.0


def _make_history(si: float = 40.0, aperture: float = 0.15, v: float = 0.5, disp: float = 0.4) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "A_Econ": [aperture],
            "A_Emp": [aperture],
            "A_Edu": [aperture],
            "SI_Econ": [si],
            "SI_Emp": [si],
            "SI_Edu": [si],
            "V_CGM": [v],
            "GTD": [disp],
            "IVD": [disp],
            "IAD": [disp],
            "IID": [disp],
        },
        index=[0],
    )


def _make_continuation(si: float, aperture: float, v: float, disp: float, steps: int = 4) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "A_Econ": np.full(steps, aperture),
            "A_Emp": np.full(steps, aperture),
            "A_Edu": np.full(steps, aperture),
            "SI_Econ": np.linspace(si - 2, si, steps),
            "SI_Emp": np.linspace(si - 2, si, steps),
            "SI_Edu": np.linspace(si - 2, si, steps),
            "V_CGM": np.linspace(v + 0.1, v, steps),
            "GTD": np.linspace(disp + 0.05, disp, steps),
            "IVD": np.linspace(disp + 0.05, disp, steps),
            "IAD": np.linspace(disp + 0.05, disp, steps),
            "IID": np.linspace(disp + 0.05, disp, steps),
        },
        index=np.arange(1, steps + 1),
    )


def test_score_continuation_prefers_high_alignment_path():
    history = _make_history()
    preferred = score_continuation(history, _make_continuation(si=95.0, aperture=A_STAR, v=0.1, disp=0.05))
    weaker = score_continuation(history, _make_continuation(si=35.0, aperture=0.4, v=0.8, disp=0.6))
    assert preferred["preference_score"] > weaker["preference_score"]
    assert preferred["si_level"] > weaker["si_level"]
    assert preferred["aperture_proximity"] > weaker["aperture_proximity"]


def test_rank_scenarios_orders_by_predicted_continuation_quality():
    strong = pd.DataFrame(
        {
            "A_Econ": np.linspace(0.15, A_STAR, 60),
            "A_Emp": np.linspace(0.15, A_STAR, 60),
            "A_Edu": np.linspace(0.15, A_STAR, 60),
            "SI_Econ": np.linspace(20, 98, 60),
            "SI_Emp": np.linspace(20, 98, 60),
            "SI_Edu": np.linspace(20, 98, 60),
            "V_CGM": np.linspace(0.8, 0.05, 60),
            "GTD": np.linspace(0.5, 0.05, 60),
            "IVD": np.linspace(0.5, 0.05, 60),
            "IAD": np.linspace(0.5, 0.05, 60),
            "IID": np.linspace(0.5, 0.05, 60),
        }
    )
    weak = strong.copy()
    weak["SI_Econ"] = np.linspace(20, 30, 60)
    weak["SI_Emp"] = np.linspace(20, 30, 60)
    weak["SI_Edu"] = np.linspace(20, 30, 60)
    weak["A_Econ"] = np.linspace(0.15, 0.35, 60)
    weak["A_Emp"] = np.linspace(0.15, 0.35, 60)
    weak["A_Edu"] = np.linspace(0.15, 0.35, 60)
    weak["V_CGM"] = np.linspace(0.8, 0.9, 60)

    ranked = rank_scenarios(
        trajectories={"strong": strong, "weak": weak},
        forecast_fn=last_value_forecast,
        origins=[40],
        horizons=[10],
        context_length=20,
    )
    forecast = ranked[ranked["source"] == "forecast"].set_index("scenario")
    assert forecast.loc["strong", "rank"] < forecast.loc["weak", "rank"]
    summary = summarize_rankings(ranked)
    assert set(summary["scenario"]) == {"strong", "weak"}
    agreement = ranking_agreement(ranked)
    assert len(agreement) == 1
    assert bool(agreement.iloc[0]["top_match"])
