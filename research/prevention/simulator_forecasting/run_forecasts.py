"""Run forecastability diagnostics and scenario preference ranking."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .baselines import BASELINES
from .evaluation import evaluate_model
from .scenario_ranking import (
    rank_scenarios,
    ranking_agreement,
    ranking_stability,
    summarize_rankings,
)
from .schema import ForecastConfig, selected_channels
from .timesfm_adapter import TimesFMAdapter, TimesFMUnavailableError
from .trajectory_io import load_existing_trajectories, write_json

PACKAGE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PACKAGE_DIR / "results"


def _parse_int_list(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def run_forecast(args: argparse.Namespace) -> int:
    trajectories = load_existing_trajectories()
    if not trajectories:
        raise FileNotFoundError(
            "No simulator trajectories found. Run research/prevention/simulator/run_scenarios.py first."
        )
    config = ForecastConfig(
        context_length=args.context,
        horizon=args.horizon,
        min_train=args.min_train,
        device=args.device,
    )
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    all_metrics = []
    adapter = None
    for scenario, frame in trajectories.items():
        channels = list(selected_channels(frame.columns))
        if not channels:
            continue
        target = frame[channels].dropna(axis=1, how="all")
        if len(target) < config.min_train + config.horizon:
            continue
        for model_name, forecast_fn in BASELINES.items():
            def baseline_fn(train, horizon, fn=forecast_fn):
                return fn(train.tail(config.context_length), horizon)
            metrics = evaluate_model(target, model_name, baseline_fn, config.min_train, config.horizon)
            if not metrics.empty:
                metrics.insert(0, "scenario", scenario)
                all_metrics.append(metrics)
        if args.model in {"timesfm", "all"}:
            adapter = adapter or TimesFMAdapter(config)
            def timesfm_fn(train, horizon, current=adapter):
                return current.predict(train.tail(config.context_length), horizon)
            try:
                metrics = evaluate_model(target, "timesfm", timesfm_fn, config.min_train, config.horizon)
                if not metrics.empty:
                    metrics.insert(0, "scenario", scenario)
                    all_metrics.append(metrics)
                write_json(adapter.manifest(scenario, channels), RESULTS_DIR / f"{scenario}_timesfm_manifest.json")
            except TimesFMUnavailableError as exc:
                if args.require_timesfm:
                    raise
                print(f"Skipping TimesFM for {scenario}: {exc}")
    if not all_metrics:
        raise RuntimeError("No forecast metrics were produced")
    metrics = pd.concat(all_metrics, ignore_index=True)
    metrics.to_csv(RESULTS_DIR / "metrics_per_origin.csv", index=False)
    summary = metrics.groupby(["scenario", "model", "series_id"], as_index=False).agg(
        origins=("origin", "count"), mae=("mae", "mean"), rmse=("rmse", "mean"),
        bias=("bias", "mean"), max_abs_error=("max_abs_error", "mean"),
        coverage=("coverage", "mean"), mean_width=("mean_width", "mean"),
    )
    summary.to_csv(RESULTS_DIR / "metrics_summary.csv", index=False)
    write_json(
        {
            "config": config.to_dict(),
            "scenarios": list(trajectories),
            "experiment": "forecastability",
        },
        RESULTS_DIR / "manifest.json",
    )
    print(summary.to_string(index=False))
    return 0


def run_rank(args: argparse.Namespace) -> int:
    trajectories = load_existing_trajectories()
    if not trajectories:
        raise FileNotFoundError(
            "No simulator trajectories found. Run research/prevention/simulator/run_scenarios.py first."
        )
    origins = _parse_int_list(args.origins)
    horizons = _parse_int_list(args.rank_horizons)
    config = ForecastConfig(
        context_length=args.context,
        horizon=max(horizons),
        min_train=min(origins),
        device=args.device,
        model=args.rank_model,
    )
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.rank_model == "timesfm":
        adapter = TimesFMAdapter(config)
        def forecast_fn(train, horizon):
            return adapter.predict(train.tail(config.context_length), horizon)
        try:
            adapter.ensure_loaded()
        except TimesFMUnavailableError:
            if args.require_timesfm:
                raise
            raise
    else:
        baseline = BASELINES[args.rank_model]
        def forecast_fn(train, horizon, fn=baseline):
            return fn(train.tail(config.context_length), horizon)

    ranked = rank_scenarios(
        trajectories=trajectories,
        forecast_fn=forecast_fn,
        origins=origins,
        horizons=horizons,
        context_length=config.context_length,
    )
    if ranked.empty:
        raise RuntimeError("No scenario rankings were produced")
    summary = summarize_rankings(ranked)
    agreement = ranking_agreement(ranked)
    stability = ranking_stability(ranked, source="forecast")

    ranked.to_csv(RESULTS_DIR / "scenario_rankings.csv", index=False)
    summary.to_csv(RESULTS_DIR / "scenario_rank_summary.csv", index=False)
    agreement.to_csv(RESULTS_DIR / "scenario_rank_agreement.csv", index=False)
    stability.to_csv(RESULTS_DIR / "scenario_rank_stability.csv", index=False)
    write_json(
        {
            "experiment": "scenario_preference_ranking",
            "config": config.to_dict(),
            "origins": origins,
            "horizons": horizons,
            "rank_model": args.rank_model,
            "scenarios": list(trajectories),
        },
        RESULTS_DIR / "scenario_rank_manifest.json",
    )
    print("Scenario preference summary")
    print(summary.to_string(index=False))
    if not agreement.empty:
        print()
        print("Forecast vs actual ranking agreement")
        print(agreement.to_string(index=False))
    if not stability.empty:
        print()
        print("Forecast ranking stability")
        print(stability.to_string(index=False))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Forecast GGG simulator trajectories and rank scenarios by predicted continuation quality"
    )
    parser.add_argument("command", choices=("forecast", "rank", "all"), nargs="?", default="forecast")
    parser.add_argument("--model", choices=("baselines", "timesfm", "all"), default="all")
    parser.add_argument("--rank-model", choices=("timesfm", "last_value", "drift", "linear_trend"), default="timesfm")
    parser.add_argument("--context", type=int, default=40)
    parser.add_argument("--horizon", type=int, default=10)
    parser.add_argument("--min-train", type=int, default=40)
    parser.add_argument("--origins", default="40,50,60,70")
    parser.add_argument("--rank-horizons", default="5,10,20")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--require-timesfm", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "forecast":
        return run_forecast(args)
    if args.command == "rank":
        return run_rank(args)
    code = run_forecast(args)
    if code != 0:
        return code
    return run_rank(args)


if __name__ == "__main__":
    raise SystemExit(main())
