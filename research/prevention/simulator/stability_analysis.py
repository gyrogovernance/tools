"""
Stability Analysis Module

Provides fixed-point analysis and Jacobian eigenvalue computation
to verify that A* is a stable attractor of the CGM dynamics.

Reference: CGM Paper Section 4
"""

import sys
from pathlib import Path
import numpy as np
from typing import Dict, Tuple, List

parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from simulator.cgm_constants import A_STAR, derive_all_coefficients
from simulator import ScenarioConfig, run_scenario


# ==========
# FUNCTIONS
# ==========

def compute_numerical_jacobian(
    f: callable,
    x0: np.ndarray,
    epsilon: float = 1e-6
) -> np.ndarray:
    """
    Computes Jacobian of f at x0 via finite differences.
    
    Args:
        f: Function mapping R^n -> R^n.
        x0: Point to evaluate Jacobian.
        epsilon: Finite difference step.
    
    Returns:
        Jacobian matrix (n x n).
    """
    n = len(x0)
    J = np.zeros((n, n))
    f0 = f(x0)
    
    for j in range(n):
        x_plus = x0.copy()
        x_plus[j] += epsilon
        f_plus = f(x_plus)
        J[:, j] = (f_plus - f0) / epsilon
    
    return J


def check_fixed_point_stability(
    jacobian: np.ndarray
) -> Tuple[bool, np.ndarray, float]:
    """
    Checks stability via eigenvalue analysis.
    
    For discrete-time systems, stability requires all eigenvalues
    inside the unit circle: |lambda_i| < 1.
    
    Args:
        jacobian: Jacobian matrix at fixed point.
    
    Returns:
        (is_stable, eigenvalues, spectral_radius)
    """
    eigenvalues = np.linalg.eigvals(jacobian)
    spectral_radius = np.max(np.abs(eigenvalues))
    is_stable = spectral_radius < 1.0
    
    return (is_stable, eigenvalues, spectral_radius)


def verify_global_attraction(
    n_samples: int = 1000,
    coupling_strength: float = 1.0,
    num_steps: int = 200,
    convergence_threshold: float = 90.0
) -> Tuple[int, int, List[float]]:
    """
    Verifies A* is globally attracting by sampling initial conditions.
    
    Samples initial apertures uniformly from [0.01, 0.99]^3 and
    counts how many converge to SI >= threshold.
    
    Args:
        n_samples: Number of random initial conditions (default 1000 for rigor).
        coupling_strength: CGM coupling multiplier.
        num_steps: Simulation steps.
        convergence_threshold: SI threshold for convergence.
    
    Returns:
        (converged_count, total_count, final_SIs)
    """
    np.random.seed(42)
    
    coeffs = derive_all_coefficients(coupling_strength=coupling_strength, dt=1.0)
    
    converged = 0
    final_SIs = []
    
    for _ in range(n_samples):
        # Random initial apertures
        A_init = np.random.uniform(0.01, 0.99, 3)
        
        config = ScenarioConfig(
            Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
            GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
            GMT0=0.5, ICV0=0.5, IIA0=0.5, ICI0=0.5,
            A_Econ_target=A_init[0],
            A_Emp_target=A_init[1],
            A_Edu_target=A_init[2],
            **coeffs,
            cycle_evolution_rate=0.08,
            num_steps=num_steps,
            dt=1.0,
            time_unit="steps"
        )
        
        result = run_scenario(config, verbose=False)
        final_si = result.SI_Econ[-1]
        final_SIs.append(final_si)
        
        if final_si >= convergence_threshold:
            converged += 1
    
    return (converged, n_samples, final_SIs)


def analyze_coupling_bifurcation(
    kappa_values: List[float],
    num_steps: int = 200
) -> Dict[float, Tuple[float, bool]]:
    """
    Analyzes how final SI varies with coupling strength.
    
    Tests whether system converges for different kappa values.
    
    Args:
        kappa_values: List of coupling strengths to test.
        num_steps: Simulation steps.
    
    Returns:
        Dict mapping kappa -> (final_SI, converged).
    """
    results = {}
    
    for kappa in kappa_values:
        coeffs = derive_all_coefficients(coupling_strength=kappa, dt=1.0)
        
        config = ScenarioConfig(
            Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
            GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
            GMT0=0.5, ICV0=0.5, IIA0=0.5, ICI0=0.5,
            A_Econ_target=0.15,
            A_Emp_target=0.15,
            A_Edu_target=0.15,
            **coeffs,
            cycle_evolution_rate=0.08,
            num_steps=num_steps,
            dt=1.0,
            time_unit="steps"
        )
        
        result = run_scenario(config, verbose=False)
        final_si = result.SI_Econ[-1]
        converged = final_si >= 90.0
        
        results[kappa] = (final_si, converged)
    
    return results


def run_stability_analysis(verbose: bool = True) -> Dict:
    """
    Runs full stability analysis.
    
    Args:
        verbose: Print results.
    
    Returns:
        Analysis results.
    """
    if verbose:
        print("=" * 10)
        print("Stability Analysis")
        print("=" * 10)
        print()
    
    # Global attraction test
    if verbose:
        print("Testing global attraction (1000 samples)...")
    
    converged, total, final_SIs = verify_global_attraction(
        n_samples=1000,
        coupling_strength=1.0,
        num_steps=200
    )
    
    if verbose:
        print(f"Converged: {converged}/{total} ({100*converged/total:.1f}%)")
        print(f"SI range: [{min(final_SIs):.1f}, {max(final_SIs):.1f}]")
        print(f"SI mean: {np.mean(final_SIs):.1f}")
        print()
    
    # Bifurcation analysis
    if verbose:
        print("Coupling strength bifurcation:")
    
    kappa_values = [0.1, 0.5, 1.0, 2.0, 5.0]
    bifurcation = analyze_coupling_bifurcation(kappa_values)
    
    if verbose:
        for kappa, (si, conv) in bifurcation.items():
            status = "OK" if conv else "FAIL"
            print(f"  kappa={kappa:.1f}: SI={si:.1f} [{status}]")
        print()
    
    # Summary
    if verbose:
        print("=" * 10)
        print("Summary")
        print("=" * 10)
        if converged == total:
            print("A* is globally attracting (all samples converged)")
        else:
            print(f"Warning: {total - converged} samples did not converge")
        
        stable_range = [k for k, (_, c) in bifurcation.items() if c]
        if stable_range:
            print(f"Stable kappa range: [{min(stable_range)}, {max(stable_range)}]")
        print("=" * 10)
    
    return {
        "global_attraction": {
            "converged": converged,
            "total": total,
            "rate": converged / total
        },
        "bifurcation": bifurcation,
        "final_SIs": final_SIs
    }


if __name__ == "__main__":
    run_stability_analysis(verbose=True)

