"""
Lyapunov Governance Potential for CGM K₄ Dynamics

Defines V_CGM, a Lyapunov-style governance potential derived directly
from CGM invariants on the K₄ tetrahedral graph.

CGM fixes two types of invariants:

1. BU dynamic (aperture) per domain:
   - Aperture A_D = ||y_cycle||²_W / ||y||²_W should converge to A*.

2. BU memory (stage profile) at Ecology:
   - Aggregate indirect vertex profile x_deriv = (x_Econ + x_Emp + x_Edu)/3
     should converge to x_balanced = [w_CS, w_UNA, w_ONA, w_BU].

We therefore define:

    V_apert = (1/2) Σ_D (log(A_D / A*))²
    V_stage = (1/2) ||x_deriv - x_balanced||²

and

    V_CGM = V_apert + V_stage

This V_CGM is zero if and only if:
    - Each domain has A_D = A* (aperture balance),
    - The aggregate indirect profile equals the canonical BU-balanced profile.

It is non-negative elsewhere, and depends only on CGM invariants:
    - A* from δ_BU, m_a
    - x_balanced from stage actions S_CS, S_UNA, S_ONA, S_BU
    - Apertures from Hodge decomposition and W
    - Aggregate vertex potentials from domain states

Public API:
    - precompute_cgm_lyapunov_constants() -> x_balanced
    - compute_total_lyapunov(domain_states, B, W, P_grad, P_cycle, x_balanced, A_star)

"""

from typing import Dict, Tuple, TYPE_CHECKING

import numpy as np

from .cgm_constants import compute_stage_weights, A_STAR
from .geometry import hodge_decomposition, compute_aperture

if TYPE_CHECKING:
    from .domains import DomainStateBase


def precompute_cgm_lyapunov_constants() -> np.ndarray:
    """
    Precomputes the canonical CGM balanced vertex profile for Lyapunov use.

    Returns:
        x_balanced: (4,) canonical balanced profile [w_CS, w_UNA, w_ONA, w_BU],
                    where w_* are normalised stage actions including BU.
    """
    weights = compute_stage_weights(include_bu=True)
    x_balanced = np.array([
        weights["w_CS"],
        weights["w_UNA"],
        weights["w_ONA"],
        weights["w_BU"],
    ], dtype=float)
    return x_balanced


def compute_total_lyapunov(
    domain_states: Dict[str, "DomainStateBase"],
    B: np.ndarray,
    W: np.ndarray,
    P_grad: np.ndarray,
    P_cycle: np.ndarray,
    x_balanced: np.ndarray,
    A_star: float = A_STAR
) -> Tuple[float, float, float, Dict[str, Dict[str, float]]]:
    """
    Computes the total CGM Lyapunov governance potential across domains.

    V_CGM = V_apert + V_stage, where:

      V_apert = (1/2) Σ_D (log(A_D / A*))²
      V_stage = (1/2) ||x_deriv - x_balanced||²

    with:
      - A_D: Aperture of each domain D, derived from y_D and W.
      - x_deriv: Aggregate indirect profile =
                 (x_Econ + x_Emp + x_Edu) / 3 in stage order.

    Args:
        domain_states: Dict mapping domain name ("economy", "employment",
                       "education", optionally "ecology") to DomainStateBase.
        B: 4x6 incidence matrix.
        W: 6x6 weight matrix.
        P_grad: 6x6 gradient projection matrix.
        P_cycle: 6x6 cycle projection matrix.
        x_balanced: (4,) canonical balanced vertex profile.
        A_star: Canonical aperture A*.

    Returns:
        V_total: Total Lyapunov potential V_CGM.
        V_apert_total: Sum of aperture deviation terms.
        V_stage: Stage-profile displacement term.
        details: Per-domain aperture contributions:
                 details[domain_name] = {
                     "V_apert": ...,
                     "A": ...,
                 }
    """
    V_apert_total = 0.0
    details: Dict[str, Dict[str, float]] = {}

    # --- 1. Per-domain aperture contributions ---
    for name, state in domain_states.items():
        if state.y is None:
            continue

        y = state.y
        # Hodge decomposition to recover cycle component
        y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
        A_D = compute_aperture(y, y_cycle, W)

        # Use a symmetric, scale-free deviation: (log(A_D/A_star))²
        eps = 1e-12
        A_clipped = max(A_D, eps)
        ratio = A_clipped / A_star
        log_dev = np.log(ratio)
        V_apert_D = 0.5 * (log_dev ** 2)

        V_apert_total += V_apert_D
        details[name] = {
            "V_apert": V_apert_D,
            "A": A_D,
        }

    # --- 2. Aggregate stage-profile displacement (Economy, Employment, Education) ---
    # We only aggregate the three indirect domains; Ecology is BU dual.
    x_econ = domain_states["economy"].to_potential_vector()
    x_emp = domain_states["employment"].to_potential_vector()
    x_edu = domain_states["education"].to_potential_vector()

    x_deriv = (x_econ + x_emp + x_edu) / 3.0
    delta_x = x_deriv - x_balanced
    V_stage = 0.5 * float(delta_x.T @ delta_x)

    V_total = V_apert_total + V_stage

    return V_total, V_apert_total, V_stage, details
