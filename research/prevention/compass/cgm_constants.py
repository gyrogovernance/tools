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

# Aperture scale (BU threshold) from exact formula m_a = 1/(2√(2π))
M_A = 1 / (2 * np.sqrt(2 * np.pi))

# Quantum gravity horizon
Q_G = 4 * np.pi  # Q_G = 4π ≈ 12.566

# BU monodromy defect
DELTA_BU = 0.195342176580  # δ_BU ≈ 0.1953 rad

# Canonical aperture: A* = 1 - δ_BU/m_a ≈ 0.0207
A_STAR = 1 - (DELTA_BU / M_A)

# Default initial aperture for Post-AGI deployment states
# Based on GGG paper estimates: current Post-AGI deployment states around A ≈ 0.12–0.15
A_INIT_DEFAULT = 0.12


# ==========
# DIMENSIONLESS ACTIONS
# ==========

S_CS = S_P / M_A
S_UNA = U_P / M_A
S_ONA = O_P / M_A
S_BU = M_A


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


def compute_governance_rate(dt: float = 1.0, tau: float = M_A) -> float:
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
        coeffs["alpha2"] = kappa * weights["w_CS"]
        coeffs["alpha4"] = kappa * weights["w_UNA"]
        coeffs["alpha6"] = kappa * weights["w_ONA"]
        coeffs["alpha8"] = kappa * weights["w_BU"]
    
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
        coeffs["beta2"] = kappa * weights["w_CS"]
        coeffs["beta4"] = kappa * weights["w_UNA"]
        coeffs["beta6"] = kappa * weights["w_ONA"]
        coeffs["beta8"] = kappa * weights["w_BU"]
    
    return coeffs


def derive_gamma_coefficients(
    kappa: float,
    weights: Dict[str, float] = None,
    include_aperture_feedback: bool = True
) -> Dict[str, float]:
    """
    γ coefficients for employment → education flow.
    
    Education responds to Employment in the GGG ordering.
    Ingress flow; coefficients use the same kappa * w[i] structure as other domains.
    
    Each nonzero coefficient couples a CGM stage:
        γ₂:   Governance Traceability ← Governance Management    (CS)
        γ₅:   Information Variety ← Information Curation         (UNA)
        γ₈:   Inference Accountability ← Inference Interaction   (ONA)
        γ₁₁:  Intelligence Integrity ← Intelligence Cooperation  (BU)
    
    Note: γ₁, γ₄, γ₇, γ₁₀ (economy terms) are computed as zero and not used in dynamics.
    
    Args:
        kappa: Governance rate.
        weights: Stage weights dict. If None, uses CGM-derived weights.
        include_aperture_feedback: Include feedback coefficients (γ₃, γ₆, γ₉, γ₁₂).
    
    Returns:
        Dict with gamma1 through gamma12 (gamma1,4,7,10 unused in dynamics).
    """
    if weights is None:
        weights = compute_stage_weights(include_bu=True)
    
    # Economy terms (gamma1,4,7,10) are not used in GGG ordering (Education responds only to Employment)
    coeffs = {
        "gamma1": 0.0,
        "gamma2": kappa * weights["w_CS"],
        "gamma4": 0.0,
        "gamma5": kappa * weights["w_UNA"],
        "gamma7": 0.0,
        "gamma8": kappa * weights["w_ONA"],
        "gamma10": 0.0,
        "gamma11": kappa * weights["w_BU"],
    }
    
    if include_aperture_feedback:
        coeffs["gamma3"] = kappa * weights["w_CS"]
        coeffs["gamma6"] = kappa * weights["w_UNA"]
        coeffs["gamma9"] = kappa * weights["w_ONA"]
        coeffs["gamma12"] = kappa * weights["w_BU"]
    
    return coeffs


def derive_all_coefficients(
    coupling_strength: float = 1.0,
    dt: float = 1.0,
    use_uniform_stage_weights: bool = False
) -> Dict[str, float]:
    """
    Derives all coupling coefficients from CGM structure.
    
    Stage weights from S_CS, S_UNA, S_ONA, S_BU (or uniform for null model).
    Global rate from Q_G and m_a.
    
    Args:
        coupling_strength: Multiplier for κ.
        dt: Simulation time step.
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
    coeffs.update(derive_gamma_coefficients(kappa, weights))
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



