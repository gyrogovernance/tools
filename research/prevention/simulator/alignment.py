"""
Alignment Index Computation

Implements the Superintelligence Index (SI) from CGM:
- Aperture A = ||y_cycle||^2_W / ||y||^2_W
- Canonical aperture A* = 1 - delta_BU/m_a
- Deviation D = max(A/A*, A*/A)
- SI = 100/D

SI ranges from 0 to 100, with SI=100 when A=A*.

Reference: CGM Paper Section 4
"""

import numpy as np
from typing import Optional, Dict

# Import A_STAR from the single source of truth
from .cgm_constants import A_STAR


def compute_deviation(A: float, A_star: float = A_STAR) -> float:
    """
    Computes deviation D = max(A/A*, A*/A).
    
    Args:
        A: Measured aperture in [0, 1].
        A_star: Canonical aperture.
    
    Returns:
        Deviation factor D >= 1.
    """
    # Handle edge cases
    if A <= 0:
        # A = 0 means pure gradient (no cycle component)
        # D = A*/0 → infinity, but we cap it
        return float('inf') if A_star > 0 else 1.0
    
    if A_star <= 0:
        # Invalid A_star
        return float('inf') if A > 0 else 1.0
    
    # Canonical CGM formula
    D = max(A / A_star, A_star / A)
    
    return float(D)


def compute_superintelligence_index(A: float, A_star: float = A_STAR) -> float:
    """
    Computes SI = 100/D where D = max(A/A*, A*/A).
    
    Args:
        A: Measured aperture in [0, 1].
        A_star: Canonical aperture.
    
    Returns:
        SI in (0, 100].
    """
    D = compute_deviation(A, A_star)
    
    if D == float('inf'):
        return 0.0
    
    if D <= 0:
        return 0.0
    
    SI = 100.0 / D
    
    # Clip to [0, 100] for safety
    return float(np.clip(SI, 0.0, 100.0))


def compute_domain_SI(
    A_D: float,
    A_star: float = A_STAR
) -> float:
    """
    Computes SI for a single domain.
    
    Args:
        A_D: Domain aperture.
        A_star: Canonical aperture.
    
    Returns:
        SI_D in (0, 100].
    """
    return compute_superintelligence_index(A_D, A_star)



def extract_alignment_metrics(x: np.ndarray) -> tuple:
    """
    Extracts (Gov, Info, Infer, Int) from potential vector x.
    
    Args:
        x: Length-4 vector in CGM order:
           [Governance, Information, Inference, Intelligence].
           For Economy: [Gov, Info, Infer, Int]
           For Employment: [GM, ICu, IInter, ICo]
           For Education: [GMT, ICV, IIA, ICI]
    
    Returns:
        Tuple (Gov, Info, Infer, Int).
    """
    if len(x) != 4:
        raise ValueError("x must have length 4")
    
    Gov = float(x[0])    # Governance
    Info = float(x[1])   # Information
    Infer = float(x[2])  # Inference
    Int = float(x[3])    # Intelligence
    
    return Gov, Info, Infer, Int


def compute_alignment_index(
    Gov: float,
    Info: float,
    Infer: float,
    Int: float,
    A: float,
    A_star: float = A_STAR,
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Computes SI from aperture.
    
    Args:
        Gov: Governance level (not used in canonical SI).
        Info: Information level (not used in canonical SI).
        Infer: Inference level (not used in canonical SI).
        Int: Intelligence level (not used in canonical SI).
        A: Aperture value.
        A_star: Target aperture (default A* ≈ 0.0207).
        weights: Ignored in canonical implementation.
    
    Returns:
        S: Alignment index in [0, 1] (SI/100).
    """
    SI = compute_superintelligence_index(A, A_star)
    return SI / 100.0


def compute_global_alignment_index(
    S_econ: float,
    S_work: float,
    S_edu: float,
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Computes global alignment index from domain-specific indices.
    
    By default: S_global = (S_econ + S_work + S_edu) / 3
    
    Args:
        S_econ: Economy alignment index (0-1 scale)
        S_work: Employment alignment index (0-1 scale)
        S_edu: Education alignment index (0-1 scale)
        weights: Optional dict with keys "econ", "work", "edu"
                 If None, equal weights (1/3 each)
    
    Returns:
        S_global: Global alignment index in [0, 1]
    """
    if weights is None:
        # Equal weights
        w_econ = w_work = w_edu = 1.0
    else:
        w_econ = weights.get("econ", 1.0)
        w_work = weights.get("work", 1.0)
        w_edu = weights.get("edu", 1.0)
    
    numerator = w_econ * S_econ + w_work * S_work + w_edu * S_edu
    denominator = w_econ + w_work + w_edu
    
    if denominator == 0:
        return 0.0
    
    S_global = numerator / denominator
    
    return float(np.clip(S_global, 0.0, 1.0))
