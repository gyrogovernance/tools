"""
CGM Constants Module

Defines constants derived from the Common Governance Model:
- Stage thresholds: s_p, u_p, o_p, m_a
- Dimensionless actions: S_CS, S_UNA, S_ONA, S_BU
- Invariants: Q_G, delta_BU, A*
- Stage weights: w_CS, w_UNA, w_ONA, w_BU
- Governance rate kappa

Reference: CGM Paper Section 3
"""

import numpy as np
from typing import Dict


# ==========
# FUNDAMENTAL CONSTANTS
# ==========

# Stage thresholds (from CGM modal logic)
S_P = np.pi / 2          # CS threshold: π/2 ≈ 1.5708
U_P = 1 / np.sqrt(2)     # UNA threshold: 1/√2 ≈ 0.7071
O_P = np.pi / 4          # ONA threshold: π/4 ≈ 0.7854

# Aperture scale (BU threshold)
M_A = 1 / (2 * np.sqrt(2 * np.pi))  # m_a = 1/(2√(2π)) ≈ 0.1995
M_A_EXACT = 0.199471140201

# Quantum gravity horizon
Q_G = 4 * np.pi  # Q_G = 4π ≈ 12.566

# BU monodromy defect
DELTA_BU = 0.195342176580  # δ_BU ≈ 0.1953 rad

# Canonical aperture: A* = 1 - δ_BU/m_a ≈ 0.0207
A_STAR = 1 - (DELTA_BU / M_A_EXACT)

# BU duality ratio (Ingress/Egress asymmetry)
BU_DUALITY_RATIO = DELTA_BU / M_A_EXACT  # ≈ 0.9793


# ==========
# DIMENSIONLESS ACTIONS
# ==========

S_CS = S_P / M_A_EXACT    # CS action ≈ 7.88
S_UNA = U_P / M_A_EXACT   # UNA action ≈ 3.55
S_ONA = O_P / M_A_EXACT   # ONA action ≈ 3.94
S_BU = M_A_EXACT          # BU action = m_a


# ==========
# STAGE WEIGHTS
# ==========

def compute_stage_weights(include_bu: bool = False) -> Dict[str, float]:
    """
    Computes stage weights from dimensionless actions.
    
    Args:
        include_bu: Include BU in normalization.
    
    Returns:
        Dict with w_CS, w_UNA, w_ONA, and optionally w_BU.
    """
    if include_bu:
        total_S = S_CS + S_UNA + S_ONA + S_BU
        return {
            "w_CS": S_CS / total_S,
            "w_UNA": S_UNA / total_S,
            "w_ONA": S_ONA / total_S,
            "w_BU": S_BU / total_S
        }
    else:
        total_S = S_CS + S_UNA + S_ONA
        return {
            "w_CS": S_CS / total_S,
            "w_UNA": S_UNA / total_S,
            "w_ONA": S_ONA / total_S
        }


STAGE_WEIGHTS = compute_stage_weights(include_bu=False)
W_CS = STAGE_WEIGHTS["w_CS"]    # ≈ 0.513
W_UNA = STAGE_WEIGHTS["w_UNA"]  # ≈ 0.231
W_ONA = STAGE_WEIGHTS["w_ONA"]  # ≈ 0.256

STAGE_WEIGHTS_WITH_BU = compute_stage_weights(include_bu=True)
W_BU = STAGE_WEIGHTS_WITH_BU["w_BU"]  # ≈ 0.013


# ==========
# GOVERNANCE RATE
# ==========

def compute_base_governance_rate() -> float:
    """
    Base governance rate from aperture constraint Q_G m_a² = 1/2.
    
    κ₀ = 1/(2Q_G) = 1/(8π) ≈ 0.0398
    """
    return 1 / (2 * Q_G)


KAPPA_0 = compute_base_governance_rate()  # ≈ 0.0398


def compute_governance_rate(dt: float = 1.0, tau: float = M_A_EXACT) -> float:
    """
    Per-step governance rate: κ = κ₀ × (dt/τ).
    
    Args:
        dt: Simulation time step.
        tau: Governance time unit (default m_a).
    
    Returns:
        Per-step governance rate.
    """
    return KAPPA_0 * (dt / tau)


# ==========
# TIME SCALES
# ==========
# Physical interpretations of simulation time step dt.
# These anchor the dimensionless dynamics to physical reality.

# Atomic time scale: Caesium-133 hyperfine transition
# 9,192,631,770 periods define one SI second
CESIUM_PERIOD_S = 1.0 / 9192631770  # ≈ 1.09e-10 seconds

# Earth rotation (1 day = 1 gyration)
SECONDS_PER_DAY = 86400.0

# Domain rotation (4 days = 1 full domain cycle)
# Each domain gets one "day" in the governance cycle:
#   Day 1: Economy (CS), Day 2: Employment (UNA),
#   Day 3: Education (ONA), Day 4: Ecology (BU)
SECONDS_PER_DOMAIN_CYCLE = 4 * SECONDS_PER_DAY

# Solar gyration (1 year)
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY

# Time scale options for dt interpretation
TIME_SCALES = {
    "atomic": {
        "dt_seconds": CESIUM_PERIOD_S,
        "label": "atomic cycle",
        "description": "Caesium-133 hyperfine transition period"
    },
    "day": {
        "dt_seconds": SECONDS_PER_DAY,
        "label": "day",
        "description": "1 Earth rotation"
    },
    "domain_cycle": {
        "dt_seconds": SECONDS_PER_DOMAIN_CYCLE,
        "label": "4 days",
        "description": "1 domain cycle (4 Earth rotations)"
    },
    "year": {
        "dt_seconds": SECONDS_PER_YEAR,
        "label": "year",
        "description": "1 Solar gyration"
    }
}


def get_time_scale_factor(from_scale: str, to_scale: str) -> float:
    """
    Computes conversion factor between time scales.
    
    Args:
        from_scale: Source time scale ("atomic", "day", "domain_cycle", "year")
        to_scale: Target time scale
    
    Returns:
        Conversion factor (from_scale / to_scale in seconds)
    """
    if from_scale not in TIME_SCALES or to_scale not in TIME_SCALES:
        raise ValueError(f"Unknown time scale. Options: {list(TIME_SCALES.keys())}")
    
    from_seconds = TIME_SCALES[from_scale]["dt_seconds"]
    to_seconds = TIME_SCALES[to_scale]["dt_seconds"]
    
    return from_seconds / to_seconds


def steps_to_physical_time(num_steps: int, time_scale: str = "year") -> float:
    """
    Converts simulation steps to physical time.
    
    Args:
        num_steps: Number of simulation steps
        time_scale: Time scale for dt ("atomic", "day", "domain_cycle", "year")
    
    Returns:
        Physical time in the specified units
    """
    if time_scale not in TIME_SCALES:
        raise ValueError(f"Unknown time scale. Options: {list(TIME_SCALES.keys())}")
    
    return float(num_steps)  # 1 step = 1 unit of the chosen scale


def physical_time_to_steps(time_value: float, time_scale: str = "year") -> int:
    """
    Converts physical time to simulation steps.
    
    Args:
        time_value: Physical time value
        time_scale: Time scale ("atomic", "day", "domain_cycle", "year")
    
    Returns:
        Number of simulation steps (rounded)
    """
    if time_scale not in TIME_SCALES:
        raise ValueError(f"Unknown time scale. Options: {list(TIME_SCALES.keys())}")
    
    return int(round(time_value))


def compute_canonical_cycle_rate(use_bu_weight: bool = True) -> float:
    """
    Canonical cycle evolution rate derived from CGM invariants.
    
    Options:
        - κ₀ ≈ 0.0398 (base governance rate)
        - κ₀ × W_BU ≈ 0.0005 (BU-weighted, slower)
    
    Args:
        use_bu_weight: If True, scale by W_BU for slower evolution.
    
    Returns:
        Canonical cycle rate.
    """
    if use_bu_weight:
        return KAPPA_0 * W_BU
    return KAPPA_0


# ==========
# COUPLING COEFFICIENTS
# ==========

def derive_alpha_coefficients(
    kappa: float,
    weights: Dict[str, float] = None,
    include_aperture_feedback: bool = True
) -> Dict[str, float]:
    """
    α coefficients for education → economy flow.
    
    Implements the closed loop: Education → Economy → Employment → Education.
    Each coefficient couples a CGM stage across domains:
        α₁: Governance ← Governance Traceability      (CS)
        α₃: Information ← Information Variety        (UNA)
        α₅: Inference ← Inference Accountability     (ONA)
        α₇: Intelligence ← Intelligence Integrity    (BU)
    
    Args:
        kappa: Governance rate.
        weights: Stage weights dict. If None, uses CGM-derived weights.
        include_aperture_feedback: Include feedback coefficients.
    
    Returns:
        Dict with alpha1 through alpha8.
    """
    if weights is None:
        weights = compute_stage_weights(include_bu=True)
    
    # Cross-domain terms: Education → Economy (THM capacities shape CGM operations)
    coeffs = {
        "alpha1": kappa * weights["w_CS"],
        "alpha3": kappa * weights["w_UNA"],
        "alpha5": kappa * weights["w_ONA"],
        "alpha7": kappa * weights["w_BU"],
    }
    
    if include_aperture_feedback:
        feedback_scale = 1.5
        coeffs["alpha2"] = feedback_scale * kappa * weights["w_CS"]
        coeffs["alpha4"] = feedback_scale * kappa * weights["w_UNA"]
        coeffs["alpha6"] = feedback_scale * kappa * weights["w_ONA"]
        coeffs["alpha8"] = feedback_scale * kappa * weights["w_BU"]
    
    return coeffs


def derive_beta_coefficients(
    kappa: float,
    weights: Dict[str, float] = None,
    include_aperture_feedback: bool = True
) -> Dict[str, float]:
    """
    β coefficients for economy → employment flow.
    
    Employment responds to Economy in the GGG ordering.
    Each coefficient couples a CGM stage across domains:
        β₁: Governance Management ← Governance  (CS)
        β₃: Information Curation ← Information  (UNA)
        β₅: Inference Interaction ← Inference   (ONA)
        β₇: Intelligence Cooperation ← Intelligence (BU)
    
    Args:
        kappa: Governance rate.
        weights: Stage weights dict. If None, uses CGM-derived weights.
        include_aperture_feedback: Include feedback coefficients.
    
    Returns:
        Dict with beta1 through beta8.
    """
    if weights is None:
        weights = compute_stage_weights(include_bu=True)
    
    coeffs = {
        "beta1": kappa * weights["w_CS"],
        "beta3": kappa * weights["w_UNA"],
        "beta5": kappa * weights["w_ONA"],
        "beta7": kappa * weights["w_BU"],
    }
    
    if include_aperture_feedback:
        feedback_scale = 1.5
        coeffs["beta2"] = feedback_scale * kappa * weights["w_CS"]
        coeffs["beta4"] = feedback_scale * kappa * weights["w_UNA"]
        coeffs["beta6"] = feedback_scale * kappa * weights["w_ONA"]
        coeffs["beta8"] = feedback_scale * kappa * weights["w_BU"]
    
    return coeffs


def derive_gamma_coefficients(
    kappa: float,
    weights: Dict[str, float] = None,
    use_bu_asymmetry: bool = True,
    include_aperture_feedback: bool = True
) -> Dict[str, float]:
    """
    γ coefficients for employment → education flow.
    
    Education responds to Employment in the GGG ordering.
    Ingress flow with optional BU duality scaling (δ_BU/m_a ≈ 0.9793).
    
    Each coefficient couples a CGM stage:
        γ₂:   Governance Traceability ← Governance Management    (CS)
        γ₅:   Information Variety ← Information Curation         (UNA)
        γ₈:   Inference Accountability ← Inference Interaction   (ONA)
        γ₁₁:  Intelligence Integrity ← Intelligence Cooperation (BU)
    
    Note: γ₁, γ₄, γ₇, γ₁₀ (economy terms) are computed but not used in dynamics.
    
    Args:
        kappa: Governance rate.
        weights: Stage weights dict. If None, uses CGM-derived weights.
        use_bu_asymmetry: Scale by BU duality ratio.
        include_aperture_feedback: Include feedback coefficients.
    
    Returns:
        Dict with gamma1 through gamma12 (gamma1,4,7,10 unused in dynamics).
    """
    if weights is None:
        weights = compute_stage_weights(include_bu=True)
    ingress_scale = BU_DUALITY_RATIO if use_bu_asymmetry else 1.0
    
    # Economy terms (gamma1,4,7,10) are not used in GGG ordering (Education responds only to Employment)
    coeffs = {
        "gamma1": 0.0,
        "gamma2": kappa * weights["w_CS"] * ingress_scale,
        "gamma4": 0.0,
        "gamma5": kappa * weights["w_UNA"] * ingress_scale,
        "gamma7": 0.0,
        "gamma8": kappa * weights["w_ONA"] * ingress_scale,
        "gamma10": 0.0,
        "gamma11": kappa * weights["w_BU"] * ingress_scale,
    }
    
    if include_aperture_feedback:
        feedback_scale = 1.5
        coeffs["gamma3"] = feedback_scale * kappa * weights["w_CS"]
        coeffs["gamma6"] = feedback_scale * kappa * weights["w_UNA"]
        coeffs["gamma9"] = feedback_scale * kappa * weights["w_ONA"]
        coeffs["gamma12"] = feedback_scale * kappa * weights["w_BU"]
    
    return coeffs


def derive_all_coefficients(
    coupling_strength: float = 1.0,
    dt: float = 1.0,
    use_bu_asymmetry: bool = True,
    use_uniform_stage_weights: bool = False
) -> Dict[str, float]:
    """
    Derives all coupling coefficients from CGM structure.
    
    Stage weights from S_CS, S_UNA, S_ONA, S_BU (or uniform for null model).
    BU asymmetry from δ_BU/m_a.
    Global rate from Q_G and m_a.
    
    Args:
        coupling_strength: Multiplier for κ.
        dt: Simulation time step.
        use_bu_asymmetry: Apply BU duality to γ coefficients.
        use_uniform_stage_weights: Use uniform weights (null model baseline).
    
    Returns:
        Dict with all coefficients plus A_star.
    """
    kappa = compute_governance_rate(dt) * coupling_strength
    
    if use_uniform_stage_weights:
        weights = {"w_CS": 0.25, "w_UNA": 0.25, "w_ONA": 0.25, "w_BU": 0.25}
    else:
        weights = compute_stage_weights(include_bu=True)
    
    coeffs = {}
    coeffs.update(derive_alpha_coefficients(kappa, weights))
    coeffs.update(derive_beta_coefficients(kappa, weights))
    coeffs.update(derive_gamma_coefficients(kappa, weights, use_bu_asymmetry))
    coeffs["A_star"] = A_STAR
    
    return coeffs


# ==========
# STAGE-VERTEX MAPPING
# ==========

STAGE_VERTEX_MAP = {
    "CS": {
        "economy": "Gov",
        "employment": "GM",
        "education": "GT"
    },
    "UNA": {
        "economy": "Info",
        "employment": "ICu",
        "education": "IV"
    },
    "ONA": {
        "economy": "Infer",
        "employment": "IInter",
        "education": "IA"
    },
    "BU": {
        "economy": "Int",
        "employment": "ICo",
        "education": "IInteg"
    }
}

# Cross-domain flows
# Each flow covers all four CGM stages simultaneously.
# α: Egress from Education to Economy (THM → CGM)
# β: Egress from Economy to Employment (CGM → Gyroscope)
# γ: Ingress from Employment to Education (Gyroscope → THM)
FLOW_STRUCTURE = {
    "alpha": {
        "source": "education",
        "target": "economy",
        "direction": "egress"
    },
    "beta": {
        "source": "economy",
        "target": "employment",
        "direction": "egress"
    },
    "gamma": {
        "source": "employment",
        "target": "education",
        "direction": "ingress"
    }
}


# ==========
# VERIFICATION
# ==========

def print_cgm_constants():
    """Prints CGM constants for verification."""
    print("=" * 10)
    print("CGM Constants")
    print("=" * 10)
    print(f"\nQ_G = 4π = {Q_G:.6f}")
    print(f"m_a = 1/(2√(2π)) = {M_A_EXACT:.12f}")
    print(f"δ_BU = {DELTA_BU:.12f} rad")
    print(f"A* = 1 - δ_BU/m_a = {A_STAR:.6f}")
    print(f"δ_BU/m_a = {BU_DUALITY_RATIO:.6f}")
    
    print(f"\nS_CS = {S_CS:.6f}")
    print(f"S_UNA = {S_UNA:.6f}")
    print(f"S_ONA = {S_ONA:.6f}")
    print(f"S_BU = {S_BU:.6f}")
    
    print(f"\nw_CS = {W_CS:.6f}")
    print(f"w_UNA = {W_UNA:.6f}")
    print(f"w_ONA = {W_ONA:.6f}")
    print(f"w_BU = {W_BU:.6f}")
    
    print(f"\nκ₀ = 1/(2Q_G) = {KAPPA_0:.6f}")
    print(f"κ(dt=1) = {compute_governance_rate(1.0):.6f}")
    
    print(f"\nVerification: Q_G × m_a² = {Q_G * M_A_EXACT**2:.6f} (expect 0.5)")
    print("=" * 10)


def print_derived_coefficients(coupling_strength: float = 1.0):
    """Prints derived coupling coefficients."""
    coeffs = derive_all_coefficients(coupling_strength)
    
    print("=" * 10)
    print(f"Coefficients (κ × {coupling_strength})")
    print("=" * 10)
    
    print("\nα (education → economy):")
    for i in [1, 3, 5, 7]:
        print(f"  α{i} = {coeffs[f'alpha{i}']:.6f}")
    
    print("\nβ (economy → employment):")
    for i in [1, 3, 5, 7]:
        print(f"  β{i} = {coeffs[f'beta{i}']:.6f}")
    
    print("\nγ (employment → education, γ1,4,7,10 unused):")
    for i in [1, 2, 4, 5, 7, 8, 10, 11]:
        print(f"  γ{i} = {coeffs[f'gamma{i}']:.6f}")
    
    print(f"\nA* = {coeffs['A_star']:.6f}")
    print("=" * 10)


if __name__ == "__main__":
    print_cgm_constants()
    print()
    print_derived_coefficients(1.0)
