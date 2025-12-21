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
        SI in [0, 100].
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
        SI_D in [0, 100].
    """
    return compute_superintelligence_index(A_D, A_star)



