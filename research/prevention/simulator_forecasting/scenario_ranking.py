"""Scenario preference ranking from forecasted GGG continuations."""

from __future__ import annotations

from typing import Callable, Dict, List, Sequence

import numpy as np
import pandas as pd

from .scenario_scoring import rank_preference_table, score_continuation
from .schema import selected_channels


ForecastFn = Callable[[pd.DataFrame, int], object]


def _prepare_target(frame: pd.DataFrame) -> pd.DataFrame:
    channels = list(selected_channels(frame.columns))
    return frame[channels].dropna(axis=1, how="all")


def score_scenario_origin(
    scenario: str,
    frame: pd.DataFrame,
    forecast_fn: ForecastFn,
    origin: int,
    context_length: int,
    horizon: int,
) -> list[dict]:
    target = _prepare_target(frame)
    if len(target) < origin + horizon:
        return []
    history = target.iloc[:origin]
    context = history.tail(context_length)
    actual = target.iloc[origin:origin + horizon].copy()
    forecast_result = forecast_fn(context, horizon)
    if isinstance(forecast_result, tuple):
        forecast, quantiles = forecast_result
    else:
        forecast, quantiles = forecast_result, {}
    forecast = forecast.copy()
    forecast.index = actual.index
    aligned_quantiles = {}
    if quantiles:
        for quantile, frame_q in quantiles.items():
            aligned = frame_q.copy()
            aligned.index = actual.index
            aligned_quantiles[quantile] = aligned

    rows = []
    forecast_scores = score_continuation(history, forecast, quantiles=aligned_quantiles or None)
    forecast_scores.update({
        "scenario": scenario,
        "origin": origin,
        "horizon": horizon,
        "source": "forecast",
    })
    rows.append(forecast_scores)

    actual_scores = score_continuation(history, actual, quantiles=None)
    actual_scores.update({
        "scenario": scenario,
        "origin": origin,
        "horizon": horizon,
        "source": "actual",
    })
    rows.append(actual_scores)
    return rows


def rank_scenarios(
    trajectories: Dict[str, pd.DataFrame],
    forecast_fn: ForecastFn,
    origins: Sequence[int],
    horizons: Sequence[int],
    context_length: int,
) -> pd.DataFrame:
    rows: List[dict] = []
    for origin in origins:
        for horizon in horizons:
            for scenario, frame in trajectories.items():
                rows.extend(
                    score_scenario_origin(
                        scenario=scenario,
                        frame=frame,
                        forecast_fn=forecast_fn,
                        origin=origin,
                        context_length=context_length,
                        horizon=horizon,
                    )
                )
    return rank_preference_table(rows)


def summarize_rankings(ranked: pd.DataFrame) -> pd.DataFrame:
    if ranked.empty:
        return ranked
    aggregations = {
        "mean_preference": ("preference_score", "mean"),
        "mean_rank": ("rank", "mean"),
        "best_rank": ("rank", "min"),
        "worst_rank": ("rank", "max"),
        "evaluations": ("preference_score", "count"),
    }
    optional = {
        "mean_si_level": "si_level",
        "mean_si_progress": "si_progress",
        "mean_aperture_proximity": "aperture_proximity",
        "mean_lyapunov_relief": "lyapunov_relief",
        "mean_displacement_level": "displacement_level",
        "mean_certainty": "certainty",
    }
    for label, column in optional.items():
        if column in ranked.columns:
            aggregations[label] = (column, "mean")
    summary = (
        ranked.groupby(["scenario", "source"], as_index=False)
        .agg(**aggregations)
        .sort_values(["source", "mean_rank", "scenario"])
        .reset_index(drop=True)
    )
    return summary


def ranking_agreement(ranked: pd.DataFrame) -> pd.DataFrame:
    """Compare forecast ranks with actual-continuation ranks at matched cells."""
    if ranked.empty:
        return pd.DataFrame()
    forecast = ranked[ranked["source"] == "forecast"][
        ["scenario", "origin", "horizon", "rank", "preference_score"]
    ].rename(columns={"rank": "forecast_rank", "preference_score": "forecast_score"})
    actual = ranked[ranked["source"] == "actual"][
        ["scenario", "origin", "horizon", "rank", "preference_score"]
    ].rename(columns={"rank": "actual_rank", "preference_score": "actual_score"})
    merged = forecast.merge(actual, on=["scenario", "origin", "horizon"], how="inner")
    if merged.empty:
        return merged
    records = []
    for (origin, horizon), group in merged.groupby(["origin", "horizon"]):
        if len(group) < 2:
            continue
        spearman = group["forecast_rank"].corr(group["actual_rank"], method="spearman")
        top_forecast = group.sort_values("forecast_rank").iloc[0]["scenario"]
        top_actual = group.sort_values("actual_rank").iloc[0]["scenario"]
        records.append({
            "origin": origin,
            "horizon": horizon,
            "spearman": float(spearman) if np.isfinite(spearman) else np.nan,
            "top_forecast": top_forecast,
            "top_actual": top_actual,
            "top_match": top_forecast == top_actual,
            "n_scenarios": int(len(group)),
        })
    return pd.DataFrame(records)


def ranking_stability(ranked: pd.DataFrame, source: str = "forecast") -> pd.DataFrame:
    subset = ranked[ranked["source"] == source]
    if subset.empty:
        return pd.DataFrame()
    pivot = subset.pivot_table(
        index="scenario",
        columns=["origin", "horizon"],
        values="rank",
        aggfunc="mean",
    )
    records = []
    for scenario, row in pivot.iterrows():
        values = row.to_numpy(dtype=float)
        finite = values[np.isfinite(values)]
        records.append({
            "scenario": scenario,
            "mean_rank": float(np.mean(finite)) if len(finite) else np.nan,
            "rank_std": float(np.std(finite)) if len(finite) else np.nan,
            "best_rank": float(np.min(finite)) if len(finite) else np.nan,
            "worst_rank": float(np.max(finite)) if len(finite) else np.nan,
            "cells": int(len(finite)),
        })
    return pd.DataFrame(records).sort_values(["mean_rank", "rank_std"]).reset_index(drop=True)
