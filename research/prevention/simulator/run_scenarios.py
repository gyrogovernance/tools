"""
CGM Dynamics Scenario Runner

Executes simulation scenarios with CGM-derived coupling coefficients.
Demonstrates convergence properties of K4 Hodge dynamics toward
canonical aperture A* under various initial conditions.

Scenarios:
    1-3: Coupling strength variation (κ = 0.5, 1.0, 2.0)
    4:   Initial aperture below A*
    5:   Asymmetric domain initial conditions
    6:   Initial aperture at A* (equilibrium test)
    7:   Uniform stage weights (null model)

Coefficients derived from CGM invariants (Q_G, m_a, δ_BU).

Reference: CGM Paper Section 4
"""

import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
from simulator import ScenarioConfig, run_scenario
from simulator.cgm_constants import (
    A_STAR, M_A_EXACT, DELTA_BU, Q_G,
    W_CS, W_UNA, W_ONA, W_BU,
    derive_all_coefficients, print_cgm_constants,
    TIME_SCALES, SECONDS_PER_DAY, SECONDS_PER_YEAR
)


# ==========
# HELPER
# ==========

def print_time_scales():
    """Prints available time scale interpretations for dt."""
    print("=" * 10)
    print("Time Scales (dt interpretations)")
    print("=" * 10)
    print()
    for key, scale in TIME_SCALES.items():
        print(f"{scale['label']:15} : {scale['description']}")
        if key == "atomic":
            print(f"                  (period ≈ {scale['dt_seconds']:.2e} s)")
        elif key == "year":
            print(f"                  (≈ {scale['dt_seconds']/SECONDS_PER_DAY:.2f} days)")
    print()
    print("Simulation steps are dimensionless.")
    print("Choose time scale based on governance context.")
    print("=" * 10)


def compute_steps_to_threshold(result, threshold=95.0):
    """
    Returns the first step index where each domain SI reaches the given threshold.
    
    If the threshold is not reached within the horizon, the value is None.
    
    Args:
        result: SimulationResult object
        threshold: SI threshold value (default 95.0)
    
    Returns:
        Dict with keys "Econ", "Work", "Edu" mapping to step indices or None
    """
    steps = {}
    
    # Use step indices (0, 1, 2, ..., num_steps)
    t = np.arange(len(result.SI_Econ))
    
    for name, si_series in [
        ("Econ", result.SI_Econ),
        ("Emp", result.SI_Emp),
        ("Edu",  result.SI_Edu),
    ]:
        si = np.array(si_series)
        idx = np.where(si >= threshold)[0]
        steps[name] = int(t[idx[0]]) if idx.size > 0 else None
    
    return steps


def print_step_interpretation(num_steps: int):
    """
    Prints how num_steps would be interpreted under the available time scales.
    
    Args:
        num_steps: Number of steps (or None if threshold not reached)
    """
    if num_steps is None:
        print("  Threshold not reached within simulation horizon.")
        return
    
    print(f"  {num_steps} steps interpreted as:")
    for key, scale in TIME_SCALES.items():
        dt_seconds = scale["dt_seconds"]
        total_seconds = num_steps * dt_seconds
        
        if key == "atomic":
            print(f"    {scale['label']:15}: ≈ {total_seconds:.2e} s")
        elif key == "day":
            days = total_seconds / SECONDS_PER_DAY
            print(f"    {scale['label']:15}: ≈ {days:.1f} days")
        elif key == "domain_cycle":
            days = total_seconds / SECONDS_PER_DAY
            print(f"    {scale['label']:15}: ≈ {days:.1f} days")
        elif key == "year":
            years = total_seconds / SECONDS_PER_YEAR
            print(f"    {scale['label']:15}: ≈ {years:.2f} years")


def create_cgm_scenario(
    name: str,
    coupling_strength: float = 1.0,
    initial_potentials: dict = None,
    initial_apertures: dict = None,
    use_bu_asymmetry: bool = True,
    num_steps: int = 100,
    cycle_evolution_rate: float = None
) -> ScenarioConfig:
    """
    Creates a ScenarioConfig with CGM-derived coupling coefficients.
    
    Args:
        name: Scenario identifier.
        coupling_strength: Multiplier for κ.
        initial_potentials: Initial vertex potentials.
        initial_apertures: Initial aperture targets.
        use_bu_asymmetry: Apply BU duality ratio to γ couplings.
        num_steps: Simulation steps.
        cycle_evolution_rate: Rate of cycle adjustment (None for canonical κ₀).
    
    Returns:
        Configured ScenarioConfig.
    """
    coeffs = derive_all_coefficients(
        coupling_strength=coupling_strength,
        dt=1.0,
        use_bu_asymmetry=use_bu_asymmetry
    )
    
    if initial_potentials is None:
        initial_potentials = {
            "Gov0": 0.6, "Info0": 0.62, "Infer0": 0.61, "Int0": 0.59,
            "GM0": 0.25, "ICu0": 0.26, "IInter0": 0.25, "ICo0": 0.24,
            "GT0": 0.6, "IV0": 0.62, "IA0": 0.61, "IInteg0": 0.59
        }
    
    if initial_apertures is None:
        initial_apertures = {
            "A_Econ_target": A_STAR,
            "A_Emp_target": A_STAR,
            "A_Edu_target": A_STAR
        }
    
    config = ScenarioConfig(
        **initial_potentials,
        **initial_apertures,
        alpha1=coeffs["alpha1"], alpha2=coeffs["alpha2"],
        alpha3=coeffs["alpha3"], alpha4=coeffs["alpha4"],
        alpha5=coeffs["alpha5"], alpha6=coeffs["alpha6"],
        alpha7=coeffs["alpha7"], alpha8=coeffs["alpha8"],
        beta1=coeffs["beta1"], beta2=coeffs["beta2"],
        beta3=coeffs["beta3"], beta4=coeffs["beta4"],
        beta5=coeffs["beta5"], beta6=coeffs["beta6"],
        beta7=coeffs["beta7"], beta8=coeffs["beta8"],
        gamma1=coeffs["gamma1"], gamma2=coeffs["gamma2"], gamma3=coeffs["gamma3"],
        gamma4=coeffs["gamma4"], gamma5=coeffs["gamma5"], gamma6=coeffs["gamma6"],
        gamma7=coeffs["gamma7"], gamma8=coeffs["gamma8"], gamma9=coeffs["gamma9"],
        gamma10=coeffs["gamma10"], gamma11=coeffs["gamma11"], gamma12=coeffs["gamma12"],
        cycle_evolution_rate=cycle_evolution_rate,
        num_steps=num_steps,
        dt=1.0,
        time_unit="steps"
    )
    
    return config


# ==========
# MAIN
# ==========

if __name__ == "__main__":
    print("=" * 10)
    print("CGM Scenario Runner")
    print("=" * 10)
    print()
    print_cgm_constants()
    print()
    print_time_scales()
    print()
    
    # Scenario 1: Weak coupling
    print("=" * 10)
    print("Scenario 1: Weak coupling (kappa=0.5)")
    print("=" * 10)
    config1 = create_cgm_scenario(
        name="weak",
        coupling_strength=0.5,
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
        cycle_evolution_rate=0.05
    )
    result1 = run_scenario(config1, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result1.SI_Econ[-1]:.2f}")
    print()
    
    # Scenario 2: Canonical coupling
    print("=" * 10)
    print("Scenario 2: Canonical coupling (kappa=1.0)")
    print("=" * 10)
    config2 = create_cgm_scenario(
        name="canonical",
        coupling_strength=1.0,
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
        cycle_evolution_rate=0.08
    )
    result2 = run_scenario(config2, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result2.SI_Econ[-1]:.2f}")
    print()
    
    # Compute steps to SI >= 95 for canonical scenario
    steps_95 = compute_steps_to_threshold(result2, threshold=95.0)
    print("=" * 10)
    print("Time to SI >= 95 (canonical scenario, κ=1.0):")
    print("=" * 10)
    for domain_name, steps in steps_95.items():
        print(f"- {domain_name}:")
        print_step_interpretation(steps)
    print("Note: These interpretations are optional. The simulator runs in")
    print("dimensionless steps. Time scales are provided only as possible")
    print("mappings for governance contexts.")
    print("=" * 10)
    print()
    
    # Scenario 3: Strong coupling
    print("=" * 10)
    print("Scenario 3: Strong coupling (kappa=2.0)")
    print("=" * 10)
    config3 = create_cgm_scenario(
        name="strong",
        coupling_strength=2.0,
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
        cycle_evolution_rate=0.12
    )
    result3 = run_scenario(config3, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result3.SI_Econ[-1]:.2f}")
    print()
    
    # Scenario 4: Low aperture start
    print("=" * 10)
    print("Scenario 4: Low aperture (below A*)")
    print("=" * 10)
    config4 = create_cgm_scenario(
        name="low_a",
        coupling_strength=1.0,
        initial_potentials={
            "Gov0": 0.85, "Info0": 0.80, "Infer0": 0.82, "Int0": 0.78,
            "GM0": 0.30, "ICu0": 0.25, "IInter0": 0.23, "ICo0": 0.22,
            "GT0": 0.85, "IV0": 0.80, "IA0": 0.82, "IInteg0": 0.78
        },
        initial_apertures={
            "A_Econ_target": 0.005,
            "A_Emp_target": 0.008,
            "A_Edu_target": 0.004
        },
        cycle_evolution_rate=0.08
    )
    result4 = run_scenario(config4, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result4.SI_Econ[-1]:.2f}")
    print()
    
    # Scenario 5: Asymmetric
    print("=" * 10)
    print("Scenario 5: Asymmetric initial conditions")
    print("=" * 10)
    config5 = create_cgm_scenario(
        name="asymmetric",
        coupling_strength=1.0,
        initial_potentials={
            "Gov0": 0.6, "Info0": 0.5, "Infer0": 0.55, "Int0": 0.5,
            "GM0": 0.25, "ICu0": 0.25, "IInter0": 0.25, "ICo0": 0.25,
            "GT0": 0.6, "IV0": 0.62, "IA0": 0.61, "IInteg0": 0.59
        },
        initial_apertures={
            "A_Econ_target": 0.01,
            "A_Emp_target": 0.10,
            "A_Edu_target": A_STAR
        },
        cycle_evolution_rate=0.08
    )
    result5 = run_scenario(config5, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result5.SI_Econ[-1]:.2f}")
    print()
    
    # Scenario 6: Equilibrium at A*
    print("=" * 10)
    print("Scenario 6: Initialized at A* (equilibrium)")
    print("=" * 10)
    config6 = create_cgm_scenario(
        name="at_astar",
        coupling_strength=1.0,
        initial_potentials={
            "Gov0": 0.6, "Info0": 0.62, "Infer0": 0.61, "Int0": 0.59,
            "GM0": 0.25, "ICu0": 0.26, "IInter0": 0.25, "ICo0": 0.24,
            "GT0": 0.6, "IV0": 0.62, "IA0": 0.61, "IInteg0": 0.59
        },
        initial_apertures={
            "A_Econ_target": A_STAR,
            "A_Emp_target": A_STAR,
            "A_Edu_target": A_STAR
        },
        cycle_evolution_rate=0.08,
        use_bu_asymmetry=True
    )
    result6 = run_scenario(config6, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result6.SI_Econ[-1]:.2f}")
    print()
    
    # Scenario 7: Uniform weights (null model)
    print("=" * 10)
    print("Scenario 7: Uniform stage weights (null model)")
    print("=" * 10)
    coeffs_uniform = derive_all_coefficients(
        coupling_strength=1.0,
        dt=1.0,
        use_bu_asymmetry=True,
        use_uniform_stage_weights=True
    )
    config7 = ScenarioConfig(
        Gov0=0.3, Info0=0.7, Infer0=0.5, Int0=0.4,
        GM0=0.15, ICu0=0.35, IInter0=0.25, ICo0=0.25,
        GT0=0.3, IV0=0.7, IA0=0.5, IInteg0=0.4,
        A_Econ_target=0.15,
        A_Emp_target=0.12,
        A_Edu_target=0.18,
        alpha1=coeffs_uniform["alpha1"], alpha2=coeffs_uniform["alpha2"],
        alpha3=coeffs_uniform["alpha3"], alpha4=coeffs_uniform["alpha4"],
        alpha5=coeffs_uniform["alpha5"], alpha6=coeffs_uniform["alpha6"],
        alpha7=coeffs_uniform["alpha7"], alpha8=coeffs_uniform["alpha8"],
        beta1=coeffs_uniform["beta1"], beta2=coeffs_uniform["beta2"],
        beta3=coeffs_uniform["beta3"], beta4=coeffs_uniform["beta4"],
        beta5=coeffs_uniform["beta5"], beta6=coeffs_uniform["beta6"],
        beta7=coeffs_uniform["beta7"], beta8=coeffs_uniform["beta8"],
        gamma1=coeffs_uniform["gamma1"], gamma2=coeffs_uniform["gamma2"],
        gamma3=coeffs_uniform["gamma3"], gamma4=coeffs_uniform["gamma4"],
        gamma5=coeffs_uniform["gamma5"], gamma6=coeffs_uniform["gamma6"],
        gamma7=coeffs_uniform["gamma7"], gamma8=coeffs_uniform["gamma8"],
        gamma9=coeffs_uniform["gamma9"], gamma10=coeffs_uniform["gamma10"],
        gamma11=coeffs_uniform["gamma11"], gamma12=coeffs_uniform["gamma12"],
        cycle_evolution_rate=0.08,
        num_steps=100,
        dt=1.0,
        time_unit="steps"
    )
    result7 = run_scenario(config7, verbose=True, progress_interval=20)
    print(f"Final: SI_Econ={result7.SI_Econ[-1]:.2f}")
    print()
    
    # Export
    import os
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 10)
    print("Exporting results...")
    result1.export_csv(os.path.join(results_dir, "scenario1_weak.csv"))
    result2.export_csv(os.path.join(results_dir, "scenario2_canonical.csv"))
    result3.export_csv(os.path.join(results_dir, "scenario3_strong.csv"))
    result4.export_csv(os.path.join(results_dir, "scenario4_low_a.csv"))
    result5.export_csv(os.path.join(results_dir, "scenario5_asymmetric.csv"))
    result6.export_csv(os.path.join(results_dir, "scenario6_at_astar.csv"))
    result7.export_csv(os.path.join(results_dir, "scenario7_uniform.csv"))
    print(f"Results exported to {results_dir}/")
    print("=" * 10)
    
    # Summary
    print()
    print("=" * 10)
    print("Summary")
    print("=" * 10)
    print(f"{'Scenario':<35} {'kappa':>8} {'SI_Econ':>10} {'A_Econ':>10} {'SI_Ecol':>10} {'Disp_GTD':>10}")
    print("-" * 10)
    results = [result1, result2, result3, result4, result5, result6, result7]
    scenarios = [
        ('1. Weak coupling', '0.5'),
        ('2. Canonical coupling', '1.0'),
        ('3. Strong coupling', '2.0'),
        ('4. Low aperture start', '1.0'),
        ('5. Asymmetric', '1.0'),
        ('6. At A* (equilibrium)', '1.0'),
        ('7. Uniform weights (null)', '1.0')
    ]
    for (name, kappa), result in zip(scenarios, results):
        si_ecol = result.SI_Ecol[-1] if result.include_ecology else 0.0
        disp_gtd = result.GTD[-1] if result.include_ecology else 0.0
        print(f"{name:<35} {kappa:>8} {result.SI_Econ[-1]:>10.2f} {result.A_Econ[-1]:>10.4f} {si_ecol:>10.2f} {disp_gtd:>10.4f}")
    print("-" * 10)
    print(f"{'Target: A* = ' + f'{A_STAR:.4f}':<35} {'--':>8} {'100.00':>10} {A_STAR:>10.4f} {'100.00':>10} {'0.0000':>10}")
    print("=" * 10)
    print()
    print("Note: SI_Ecol measures structural coherence (dominated by canonical memory).")
    print("      Disp_GTD = |x_deriv - x_balanced|[0] shows actual displacement.")
    print("=" * 10)
