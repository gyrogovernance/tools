"""
Convergence Analysis

Provides:
1. Exponential convergence rate λ(κ) via log-linear fit
2. Long-horizon stability check for asymptotic behavior

Reference: CGM Paper Section 4
"""

import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
from simulator.run_scenarios import create_cgm_scenario
from simulator import run_scenario
from simulator.cgm_constants import A_STAR


def estimate_convergence_rate(
    kappa: float = 1.0,
    num_steps: int = 200,
    t_min: int = 20
) -> float:
    """
    Estimates exponential convergence rate λ for A_Econ → A*.
    
    Fits log|A_Econ(t) - A*| ~ C - λt for t >= t_min.
    
    Args:
        kappa: Coupling strength.
        num_steps: Simulation steps.
        t_min: Initial transient to exclude from fit.
    
    Returns:
        Estimated convergence rate λ (>= 0).
    """
    config = create_cgm_scenario(
        name=f"conv_kappa_{kappa}",
        coupling_strength=kappa,
        initial_potentials={
            "Gov0": 0.3, "Info0": 0.7, "Infer0": 0.5, "Int0": 0.4,
            "GM0": 0.15, "ICu0": 0.35, "IInter0": 0.25, "ICo0": 0.25,
            "GT0": 0.3, "IV0": 0.7, "IA0": 0.5, "IInteg0": 0.4
        },
        initial_apertures={
            "A_Econ_target": 0.15,
            "A_Emp_target": 0.12,
            "A_Edu_target": 0.18
        },
        num_steps=num_steps,
        cycle_evolution_rate=None
    )
    result = run_scenario(config, verbose=False)
    
    A = result.A_Econ
    d = np.abs(A - A_STAR)
    
    t = np.arange(len(d))
    mask = (t >= t_min) & (d > 1e-8)
    t_fit = t[mask]
    d_fit = d[mask]
    
    if len(t_fit) < 2:
        return 0.0
    
    y = np.log(d_fit)
    A_mat = np.vstack([np.ones_like(t_fit), t_fit]).T
    coeffs, _, _, _ = np.linalg.lstsq(A_mat, y, rcond=None)
    lambda_est = -coeffs[1]
    
    return float(max(lambda_est, 0.0))


def estimate_convergence_all_domains(
    kappa: float = 1.0,
    num_steps: int = 200,
    t_min: int = 20
) -> dict:
    """
    Estimates convergence rate for all three domains.
    
    Args:
        kappa: Coupling strength.
        num_steps: Simulation steps.
        t_min: Initial transient to exclude.
    
    Returns:
        Dict with λ_Econ, λ_Emp, λ_Edu, λ_mean.
    """
    config = create_cgm_scenario(
        name=f"conv_all_{kappa}",
        coupling_strength=kappa,
        initial_potentials={
            "Gov0": 0.3, "Info0": 0.7, "Infer0": 0.5, "Int0": 0.4,
            "GM0": 0.15, "ICu0": 0.35, "IInter0": 0.25, "ICo0": 0.25,
            "GT0": 0.3, "IV0": 0.7, "IA0": 0.5, "IInteg0": 0.4
        },
        initial_apertures={
            "A_Econ_target": 0.15,
            "A_Emp_target": 0.12,
            "A_Edu_target": 0.18
        },
        num_steps=num_steps,
        cycle_evolution_rate=None
    )
    result = run_scenario(config, verbose=False)
    
    rates = {}
    for name, A in [("Econ", result.A_Econ), 
                    ("Emp", result.A_Emp), 
                    ("Edu", result.A_Edu)]:
        d = np.abs(A - A_STAR)
        t = np.arange(len(d))
        mask = (t >= t_min) & (d > 1e-8)
        t_fit = t[mask]
        d_fit = d[mask]
        
        if len(t_fit) < 2:
            rates[f"lambda_{name}"] = 0.0
            continue
        
        y = np.log(d_fit)
        A_mat = np.vstack([np.ones_like(t_fit), t_fit]).T
        coeffs, _, _, _ = np.linalg.lstsq(A_mat, y, rcond=None)
        rates[f"lambda_{name}"] = float(max(-coeffs[1], 0.0))
    
    rates["lambda_mean"] = np.mean([
        rates["lambda_Econ"], 
        rates["lambda_Emp"], 
        rates["lambda_Edu"]
    ])
    
    return rates


def long_horizon_stability(
    kappa: float = 1.0,
    num_steps: int = 1000,
    t_transient: int = 200
) -> dict:
    """
    Verifies long-horizon stability after transient convergence.
    
    Runs for extended horizon and checks maximum deviation from A*
    after initial transient, detecting any late drift or oscillation.
    
    Args:
        kappa: Coupling strength.
        num_steps: Total simulation steps.
        t_transient: Steps to exclude as transient.
    
    Returns:
        Dict with max deviations and stability metrics.
    """
    config = create_cgm_scenario(
        name=f"long_run_{kappa}",
        coupling_strength=kappa,
        initial_potentials={
            "Gov0": 0.3, "Info0": 0.7, "Infer0": 0.5, "Int0": 0.4,
            "GM0": 0.15, "ICu0": 0.35, "IInter0": 0.25, "ICo0": 0.25,
            "GT0": 0.3, "IV0": 0.7, "IA0": 0.5, "IInteg0": 0.4
        },
        initial_apertures={
            "A_Econ_target": 0.15,
            "A_Emp_target": 0.12,
            "A_Edu_target": 0.18
        },
        num_steps=num_steps,
        cycle_evolution_rate=None
    )
    result = run_scenario(config, verbose=False)
    
    # Extract post-transient data
    A_Econ_tail = result.A_Econ[t_transient:]
    A_Emp_tail = result.A_Emp[t_transient:]
    A_Edu_tail = result.A_Edu[t_transient:]
    SI_Econ_tail = result.SI_Econ[t_transient:]
    
    # Compute maximum deviations
    max_dev_Econ = float(np.max(np.abs(A_Econ_tail - A_STAR)))
    max_dev_Emp = float(np.max(np.abs(A_Emp_tail - A_STAR)))
    max_dev_Edu = float(np.max(np.abs(A_Edu_tail - A_STAR)))
    max_dev_all = max(max_dev_Econ, max_dev_Emp, max_dev_Edu)
    
    # Final values
    final_A_Econ = float(result.A_Econ[-1])
    final_A_Emp = float(result.A_Emp[-1])
    final_A_Edu = float(result.A_Edu[-1])
    final_SI = float(result.SI_Econ[-1])
    
    # SI statistics (using economy as representative)
    min_SI = float(np.min(SI_Econ_tail))
    mean_SI = float(np.mean(SI_Econ_tail))
    
    return {
        "num_steps": num_steps,
        "t_transient": t_transient,
        "max_dev_Econ": max_dev_Econ,
        "max_dev_Emp": max_dev_Emp,
        "max_dev_Edu": max_dev_Edu,
        "max_dev_all": max_dev_all,
        "final_A_Econ": final_A_Econ,
        "final_A_Emp": final_A_Emp,
        "final_A_Edu": final_A_Edu,
        "final_SI": final_SI,
        "min_SI_post_transient": min_SI,
        "mean_SI_post_transient": mean_SI
    }


def run_convergence_analysis(verbose: bool = True) -> dict:
    """
    Runs convergence rate analysis for multiple κ values.
    
    Returns:
        Dict with λ results for each κ.
    """
    kappa_values = [0.5, 1.0, 2.0]
    results = {}
    
    if verbose:
        print("=" * 10)
        print("Convergence Rate λ(κ)")
        print("=" * 10)
        print(f"\nA* = {A_STAR:.4f}")
        print()
    
    for kappa in kappa_values:
        lam = estimate_convergence_rate(kappa=kappa)
        rates = estimate_convergence_all_domains(kappa=kappa)
        results[kappa] = {
            "lambda_Econ": lam,
            "lambda_all": rates
        }
        
        if verbose:
            print(f"κ = {kappa}:")
            print(f"  λ_Econ = {rates['lambda_Econ']:.4f}")
            print(f"  λ_Emp = {rates['lambda_Emp']:.4f}")
            print(f"  λ_Edu  = {rates['lambda_Edu']:.4f}")
            print(f"  λ_mean = {rates['lambda_mean']:.4f}")
            print()
    
    if verbose:
        print("=" * 10)
        print("Summary: λ(κ)")
        print("=" * 10)
        print(f"{'κ':>6} {'λ_mean':>10}")
        print("-" * 10)
        for kappa in kappa_values:
            lam_mean = results[kappa]["lambda_all"]["lambda_mean"]
            print(f"{kappa:>6.1f} {lam_mean:>10.4f}")
        print("=" * 10)
    
    return results


def run_long_horizon_check(verbose: bool = True) -> dict:
    """
    Runs long-horizon stability check for canonical scenario.
    
    Returns:
        Dict with stability metrics.
    """
    if verbose:
        print("=" * 10)
        print("Long-Horizon Stability")
        print("=" * 10)
        print()
    
    result = long_horizon_stability(kappa=1.0, num_steps=1000, t_transient=200)
    
    if verbose:
        print(f"κ = 1.0, {result['num_steps']} steps")
        print(f"Transient excluded: t < {result['t_transient']}")
        print()
        print(f"Max |A_Econ - A*| for t >= {result['t_transient']}: {result['max_dev_Econ']:.6f}")
        print(f"Max |A_Emp - A*| for t >= {result['t_transient']}: {result['max_dev_Emp']:.6f}")
        print(f"Max |A_Edu  - A*| for t >= {result['t_transient']}: {result['max_dev_Edu']:.6f}")
        print(f"Max deviation (all domains): {result['max_dev_all']:.6f}")
        print()
        print(f"Final A_Econ: {result['final_A_Econ']:.6f}")
        print(f"Final A_Emp: {result['final_A_Emp']:.6f}")
        print(f"Final A_Edu:  {result['final_A_Edu']:.6f}")
        print(f"Final SI:     {result['final_SI']:.2f}")
        print()
        print(f"SI post-transient: min={result['min_SI_post_transient']:.2f}, mean={result['mean_SI_post_transient']:.2f}")
        print("=" * 10)
    
    return result


def run_full_analysis(verbose: bool = True) -> dict:
    """
    Runs both convergence rate and long-horizon analyses.
    
    Returns:
        Dict with all results.
    """
    convergence = run_convergence_analysis(verbose=verbose)
    if verbose:
        print()
    long_horizon = run_long_horizon_check(verbose=verbose)
    
    return {
        "convergence_rates": convergence,
        "long_horizon": long_horizon
    }


if __name__ == "__main__":
    run_full_analysis(verbose=True)
