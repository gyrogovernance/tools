"""
Time-Scale Calibration for CGM Dynamics

Utilities for calibrating dimensionless CGM simulation steps to
calendar time by anchoring to empirical data points.

Approach:
    1. Define empirical aperture estimates at historical dates
    2. Run CGM dynamics with assumed coupling to match the interval
    3. Extract years_per_step as calibration factor
    4. Apply scaling for different coupling regimes

Predictions are conditional on assumed coupling parameters.
The CGM dynamics are dimensionless; this module provides one
possible dimensionful interpretation.

Reference: CGM Paper Section 4
"""

import sys
from pathlib import Path
import numpy as np
from typing import List, Tuple, Dict, Optional

parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from simulator.cgm_constants import A_STAR, derive_all_coefficients
from simulator.alignment import compute_superintelligence_index
from simulator import ScenarioConfig, run_scenario


# ==========
# DATA
# ==========

# Empirical aperture estimates at selected dates.
# Heuristic assignments for calibration purposes.
HISTORICAL_MILESTONES: List[Tuple[int, float, str]] = [
    (1956, 0.95, "Dartmouth conference"),
    (1997, 0.70, "Deep Blue"),
    (2016, 0.40, "AlphaGo"),
    (2020, 0.25, "GPT-3 release"),
    (2023, 0.15, "LLM adoption"),
    (2025, 0.12, "Present"),
]

# SI thresholds for projections
SI_THRESHOLDS: List[Tuple[str, float, str]] = [
    ("threshold_90", 0.05, "SI >= 90"),
    ("threshold_95", 0.03, "SI >= 95"),
    ("canonical", 0.0207, "A = A*"),
]

CURRENT_YEAR = 2025
CURRENT_A = 0.12


def compute_historical_si() -> List[Tuple[int, float, float, str]]:
    """
    Computes SI for each milestone.
    
    Returns:
        List of (year, aperture, SI, description) tuples.
    """
    results = []
    for year, aperture, desc in HISTORICAL_MILESTONES:
        si = compute_superintelligence_index(aperture, A_STAR)
        results.append((year, aperture, si, desc))
    return results


def compute_si_thresholds() -> List[Tuple[str, float, float, str]]:
    """
    Computes SI at projection thresholds.
    
    Returns:
        List of (name, aperture, SI, description) tuples.
    """
    results = []
    for name, aperture, desc in SI_THRESHOLDS:
        si = compute_superintelligence_index(aperture, A_STAR)
        results.append((name, aperture, si, desc))
    return results


def run_cgm_from_aperture(
    initial_aperture: float,
    coupling_strength: float = 1.0,
    num_steps: int = 200
):
    """
    Runs CGM dynamics from specified initial aperture.
    
    Args:
        initial_aperture: Starting aperture value.
        coupling_strength: Coupling parameter kappa.
        num_steps: Number of simulation steps.
    
    Returns:
        SimulationResult object.
    """
    coeffs = derive_all_coefficients(coupling_strength=coupling_strength, dt=1.0)
    config = ScenarioConfig(
        Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
        GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
        GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
        A_Econ_target=initial_aperture,
        A_Emp_target=initial_aperture,
        A_Edu_target=initial_aperture,
        **coeffs,
        cycle_evolution_rate=0.08,
        num_steps=num_steps,
        dt=1.0,
        time_unit="steps"
    )
    return run_scenario(config, verbose=False)


def find_steps_to_threshold(result, threshold: float = 95.0) -> Optional[int]:
    """
    Finds number of steps to reach SI threshold.
    
    Args:
        result: SimulationResult object.
        threshold: SI threshold value.
    
    Returns:
        Step count, or None if threshold not reached.
    """
    for i, si in enumerate(result.SI_Econ):
        if si >= threshold:
            return i
    return None


def calibrate_time_scale(
    year_start: int,
    A_start: float,
    year_end: int,
    A_end: float,
    kappa: float = 0.1,
    max_steps: int = 500
) -> Tuple[float, int]:
    """
    Calibrates years_per_step from a historical interval.
    
    Runs CGM dynamics with specified kappa until aperture crosses
    from A_start to A_end, then computes the time scaling.
    
    Args:
        year_start: Start year of calibration interval.
        A_start: Aperture at start year.
        year_end: End year of calibration interval.
        A_end: Aperture at end year.
        kappa: Assumed coupling strength for the interval.
        max_steps: Maximum simulation steps.
    
    Returns:
        (years_per_step, n_steps): Calibration factor and step count.
    """
    coeffs = derive_all_coefficients(coupling_strength=kappa, dt=1.0)
    config = ScenarioConfig(
        Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
        GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
        GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
        A_Econ_target=A_start,
        A_Emp_target=A_start,
        A_Edu_target=A_start,
        **coeffs,
        cycle_evolution_rate=0.08,
        num_steps=max_steps,
        dt=1.0,
        time_unit="steps"
    )
    result = run_scenario(config, verbose=False)
    
    n_steps = max_steps
    for i, A in enumerate(result.A_Econ):
        if A <= A_end:
            n_steps = i
            break
    
    duration_years = year_end - year_start
    years_per_step = duration_years / n_steps if n_steps > 0 else float("inf")
    return years_per_step, n_steps


def project_threshold_year(
    A_initial: float,
    year_initial: int,
    years_per_step_base: float,
    kappa_base: float,
    kappa_target: float = 1.0,
    si_threshold: float = 95.0,
    max_steps: int = 500
) -> Tuple[int, float, int]:
    """
    Projects the year when SI crosses a threshold.
    
    The time scaling adjusts inversely with coupling:
        years_per_step = years_per_step_base * (kappa_base / kappa_target)
    
    Args:
        A_initial: Starting aperture.
        year_initial: Starting year.
        years_per_step_base: Calibrated base rate.
        kappa_base: Coupling used in calibration.
        kappa_target: Coupling for projection.
        si_threshold: SI threshold to reach.
        max_steps: Maximum simulation steps.
    
    Returns:
        (projected_year, final_SI, n_steps): Projection results.
    """
    years_per_step = years_per_step_base * (kappa_base / kappa_target)
    
    coeffs = derive_all_coefficients(coupling_strength=kappa_target, dt=1.0)
    config = ScenarioConfig(
        Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
        GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
        GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
        A_Econ_target=A_initial,
        A_Emp_target=A_initial,
        A_Edu_target=A_initial,
        **coeffs,
        cycle_evolution_rate=0.08,
        num_steps=max_steps,
        dt=1.0,
        time_unit="steps"
    )
    result = run_scenario(config, verbose=False)
    
    n_steps = max_steps
    for i, si in enumerate(result.SI_Econ):
        if si >= si_threshold:
            n_steps = i
            break
    
    projected_year = year_initial + int(n_steps * years_per_step)
    final_si = result.SI_Econ[-1]
    return projected_year, final_si, n_steps


def run_analysis(verbose: bool = True) -> Dict:
    """
    Runs calibration and projection analysis.
    
    Returns:
        Dictionary with calibration and projection results.
    """
    historical_si = compute_historical_si()
    si_thresholds = compute_si_thresholds()
    
    if verbose:
        print("=" * 10)
        print("Milestones")
        print("=" * 10)
        for year, a, si, desc in historical_si:
            print(f"{year}: A={a:.3f}, SI={si:.1f} ({desc})")
        print()
        
        print("=" * 10)
        print("SI Thresholds")
        print("=" * 10)
        print(f"A* = {A_STAR:.4f}")
        for name, a, si, desc in si_thresholds:
            print(f"  {name}: A={a:.4f}, SI={si:.1f} ({desc})")
        print()
    
    # Calibration interval: 1956 -> 2025
    year_start = 1956
    A_start = 0.95
    kappa_calibration = 0.1
    
    years_per_step, n_hist = calibrate_time_scale(
        year_start=year_start,
        A_start=A_start,
        year_end=CURRENT_YEAR,
        A_end=CURRENT_A,
        kappa=kappa_calibration,
        max_steps=500
    )
    
    if verbose:
        print("=" * 10)
        print("Calibration")
        print("=" * 10)
        print(f"Interval: {year_start} -> {CURRENT_YEAR}")
        print(f"Aperture: {A_start:.2f} -> {CURRENT_A:.2f}")
        print(f"κ: {kappa_calibration}")
        print(f"Steps: {n_hist}")
        print(f"years_per_step: {years_per_step:.3f}")
        print()
    
    if verbose:
        print("=" * 10)
        print("Projections (SI >= 95)")
        print("=" * 10)
        print(f"Initial: A={CURRENT_A:.2f}, year={CURRENT_YEAR}")
        print()
    
    projections = {}
    for kappa in [0.5, 1.0, 2.0, 5.0]:
        year_proj, final_si, steps = project_threshold_year(
            A_initial=CURRENT_A,
            year_initial=CURRENT_YEAR,
            years_per_step_base=years_per_step,
            kappa_base=kappa_calibration,
            kappa_target=kappa,
            si_threshold=95.0,
            max_steps=500
        )
        yps = years_per_step * (kappa_calibration / kappa)
        projections[kappa] = {
            "year": year_proj,
            "final_si": final_si,
            "steps": steps,
            "years_per_step": yps
        }
        if verbose:
            print(f"κ={kappa}:")
            print(f"  years_per_step: {yps:.3f}")
            print(f"  Steps: {steps}")
            print(f"  Year: {year_proj}")
            print()
    
    if verbose:
        print("=" * 10)
        print("Parameters")
        print("=" * 10)
        print(f"A* = {A_STAR:.4f}")
        print(f"κ_calibration = {kappa_calibration}")
        print(f"years_per_step_base = {years_per_step:.3f}")
        print("=" * 10)
    
    return {
        "milestones": historical_si,
        "si_thresholds": si_thresholds,
        "calibration": {
            "years_per_step": years_per_step,
            "n_steps": n_hist,
            "kappa": kappa_calibration
        },
        "projections": projections
    }


if __name__ == "__main__":
    run_analysis(verbose=True)
