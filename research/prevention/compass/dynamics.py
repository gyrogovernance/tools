"""
Dynamics Module

Discrete-time update rules for domain states on K4 geometry.
Coupling coefficients derived from CGM stage weights.

Cross-domain flows:
    - α: Education → Economy (closed loop: Education → Economy → Employment → Education)
    - β: Economy → Employment
    - γ: Employment → Education

Reference: CGM Paper Section 4
"""

import numpy as np
from typing import Dict, Tuple

from .domains import EconomyState, EmploymentState, EducationState
from .geometry import (
    hodge_decomposition, compute_aperture, get_cycle_basis
)
from .cgm_constants import (
    A_STAR, derive_all_coefficients, KAPPA_0
)


def ensure_aperture(state) -> float:
    """
    Read aperture from state, enforcing internal invariant that A is set.
    """
    if state.A is None:
        raise RuntimeError("Internal invariant violated: state.A must be set")
    return float(state.A)


def get_default_params(coupling_strength: float = 1.0) -> Dict[str, float]:
    """
    Returns CGM-derived coupling parameters.
    
    Args:
        coupling_strength: Multiplier for kappa.
    
    Returns:
        Dict with alpha, beta, gamma coefficients.
    """
    return derive_all_coefficients(coupling_strength)


def update_economy_potentials(
    econ_state: EconomyState,
    edu_state: EducationState,
    params: Dict[str, float],
    A_Econ_current: float
) -> np.ndarray:
    """
    Updates economy potentials from education influence.
    
    Implements alpha couplings (Education → Economy).
    Part of the closed loop: Education → Economy → Employment → Education.
    
    Update equations:
        x_i(t+1) = x_i(t) + alpha_i * (source_i - x_i) - alpha_j * (A - A*)
    
    Args:
        econ_state: Current economy state
        edu_state: Current education state
        params: Dict with keys:
            - "alpha1" through "alpha8": CGM-derived coefficients
            - "A_star": Target aperture (default from CGM)
    
    Returns:
        x_next: Updated potential vector [Gov, Info, Infer, Int].
    """
    # Get current values
    Gov = econ_state.Gov
    Info = econ_state.Info
    Infer = econ_state.Infer
    Int = econ_state.Int
    
    # Get A_star first (CGM canonical value)
    A_star = params.get("A_star", A_STAR)
    A_Econ = A_Econ_current
    
    # Get education capacities (source of Egress flow)
    GMT = edu_state.GMT
    ICV = edu_state.ICV
    IIA = edu_state.IIA
    ICI = edu_state.ICI
    
    # Get CGM-derived coefficients (must be provided via params)
    # No fallback - caller must use derive_all_coefficients() or ScenarioConfig
    alpha1 = params["alpha1"]
    alpha2 = params["alpha2"]
    alpha3 = params["alpha3"]
    alpha4 = params["alpha4"]
    alpha5 = params["alpha5"]
    alpha6 = params["alpha6"]
    alpha7 = params["alpha7"]
    alpha8 = params["alpha8"]
    
    # Update potentials with aperture feedback and cross-domain flow
    x_current = np.array([Gov, Info, Infer, Int])
    delta = np.array([
        alpha1 * (GMT - Gov) - alpha2 * (A_Econ - A_star),
        alpha3 * (ICV - Info) - alpha4 * (A_Econ - A_star),
        alpha5 * (IIA - Infer) - alpha6 * (A_Econ - A_star),
        alpha7 * (ICI - Int) - alpha8 * (A_Econ - A_star)
    ])
    
    x_raw = x_current + delta
    
    # Clip to [0, 1]
    x_next = np.array([
        np.clip(x_raw[0], 0.0, 1.0),
        np.clip(x_raw[1], 0.0, 1.0),
        np.clip(x_raw[2], 0.0, 1.0),
        np.clip(x_raw[3], 0.0, 1.0)
    ])
    
    return x_next


def update_employment_potentials(
    emp_state: EmploymentState,
    econ_state: EconomyState,
    params: Dict[str, float],
    A_Emp_current: float
) -> np.ndarray:
    """
    Updates employment potentials from economy influence.
    
    Implements beta couplings (Economy -> Employment).
    
    Args:
        emp_state: Current employment state.
        econ_state: Current economy state.
        params: Coupling coefficients.
    
    Returns:
        x_next: Updated, normalized potentials.
    """
    # Get current values
    GM = emp_state.GM
    ICu = emp_state.ICu
    IInter = emp_state.IInter
    ICo = emp_state.ICo
    
    # Get A_star first (CGM canonical value)
    A_star = params.get("A_star", A_STAR)
    A_Emp = A_Emp_current
    
    # Get economy potentials (source of Egress flow)
    Gov = econ_state.Gov
    Info = econ_state.Info
    Infer = econ_state.Infer
    Int = econ_state.Int
    
    # Get CGM-derived coefficients (must be provided via params)
    beta1 = params["beta1"]  # CS coupling (Governance Management)
    beta2 = params["beta2"]  # CS feedback
    beta3 = params["beta3"]  # UNA coupling (Information Curation)
    beta4 = params["beta4"]  # UNA feedback
    beta5 = params["beta5"]  # ONA coupling (Inference Interaction)
    beta6 = params["beta6"]  # ONA feedback
    beta7 = params["beta7"]  # BU coupling (Intelligence Cooperation)
    beta8 = params["beta8"]  # BU feedback
    
    # Update potentials with RESTORING dynamics
    x_current = np.array([GM, ICu, IInter, ICo])
    
    delta = np.array([
        beta1 * (Gov - GM) - beta2 * (A_Emp - A_star),
        beta3 * (Info - ICu) - beta4 * (A_Emp - A_star),
        beta5 * (Infer - IInter) - beta6 * (A_Emp - A_star),
        beta7 * (Int - ICo) - beta8 * (A_Emp - A_star)
    ])
    
    x_raw = x_current + delta
    
    # Clip to [0, 1]
    pre_norm = np.array([
        np.clip(x_raw[0], 0.0, 1.0),
        np.clip(x_raw[1], 0.0, 1.0),
        np.clip(x_raw[2], 0.0, 1.0),
        np.clip(x_raw[3], 0.0, 1.0)
    ])
    
    total = np.sum(pre_norm)
    if total > 0:
        x_next = pre_norm / total
    else:
        x_next = np.array([0.25, 0.25, 0.25, 0.25])

    return x_next


def update_education_potentials(
    edu_state: EducationState,
    econ_state: EconomyState,
    emp_state: EmploymentState,
    params: Dict[str, float],
    A_Edu_current: float
) -> np.ndarray:
    """
    Updates education potentials from employment influence.
    
    Implements gamma couplings (Employment -> Education).
    Education responds to Employment in the GGG ordering.
    
    Args:
        edu_state: Current education state.
        econ_state: Current economy state (unused, kept for compatibility).
        work_state: Current employment state.
        params: Coupling coefficients.
    
    Returns:
        Updated potentials [GMT, ICV, IIA, ICI].
    """
    # Get current values
    GMT = edu_state.GMT
    ICV = edu_state.ICV
    IIA = edu_state.IIA
    ICI = edu_state.ICI
    
    # Get A_star first (CGM canonical value)
    A_star = params.get("A_star", A_STAR)
    A_Edu = A_Edu_current
    
    # Get employment shares (source of Ingress flow)
    GM = emp_state.GM
    ICu = emp_state.ICu
    IInter = emp_state.IInter
    ICo = emp_state.ICo
    
    # Get CGM-derived coefficients (must be provided via params)
    # CS stage (Governance) - Systems Operation
    gamma2 = params["gamma2"]   # GMT ← GM
    gamma3 = params["gamma3"]   # CS feedback
    
    # UNA stage (Information)
    gamma5 = params["gamma5"]   # ICV ← ICu
    gamma6 = params["gamma6"]   # UNA feedback
    
    # ONA stage (Inference)
    gamma8 = params["gamma8"]   # IIA ← IInter
    gamma9 = params["gamma9"]   # ONA feedback
    
    # BU stage (Intelligence)
    gamma11 = params["gamma11"]  # ICI ← ICo
    gamma12 = params["gamma12"]  # BU feedback
    
    # Update potentials with RESTORING dynamics
    x_current = np.array([GMT, ICV, IIA, ICI])
    
    delta = np.array([
        gamma2 * (GM - GMT) - gamma3 * (A_Edu - A_star),
        gamma5 * (ICu - ICV) - gamma6 * (A_Edu - A_star),
        gamma8 * (IInter - IIA) - gamma9 * (A_Edu - A_star),
        gamma11 * (ICo - ICI) - gamma12 * (A_Edu - A_star)
    ])
    
    x_raw = x_current + delta
    
    # Clip to [0, 1]
    x_next = np.array([
        np.clip(x_raw[0], 0.0, 1.0),
        np.clip(x_raw[1], 0.0, 1.0),
        np.clip(x_raw[2], 0.0, 1.0),
        np.clip(x_raw[3], 0.0, 1.0)
    ])
    
    return x_next



def update_cycle_component(
    y_current: np.ndarray,
    y_grad_new: np.ndarray,
    A_target: float,
    B: np.ndarray,
    W: np.ndarray,
    P_cycle: np.ndarray,
    cycle_evolution_rate: float = None
) -> np.ndarray:
    """
    Updates cycle component toward target aperture using energy relaxation.
    
    Energy relaxation: C_next = C_current + r * (C_target - C_current)
    Preserves direction, adjusts magnitude.
    
    Args:
        y_current: Current edge vector (6D).
        y_grad_new: New gradient component.
        A_target: Target aperture.
        B: Incidence matrix (4x6).
        W: Weight matrix (6x6).
        P_cycle: Cycle projection (6x6).
        cycle_evolution_rate: Evolution rate r. If None, uses canonical rate.
    
    Returns:
        Updated cycle component (6D).
    """
    if cycle_evolution_rate is None:
        cycle_evolution_rate = KAPPA_0
    
    r = float(cycle_evolution_rate)
    if not (0.0 <= r <= 1.0):
        raise ValueError("cycle_evolution_rate must be in [0,1]")
    
    # Current cycle component and energy
    c_current = P_cycle @ y_current
    C_current = float(c_current.T @ W @ c_current)
    
    # Gradient energy and target cycle energy
    G = float(y_grad_new.T @ W @ y_grad_new)
    G = max(G, 1e-12)
    
    A = float(np.clip(A_target, 0.0, 0.99))
    if A <= 0.0:
        return np.zeros(6)
    
    C_target = (A * G) / (1.0 - A)
    
    # Energy relaxation
    C_next = C_current + r * (C_target - C_current)
    C_next = max(C_next, 0.0)
    
    C_EPS = 1e-10
    if C_current < C_EPS:
        if C_next < C_EPS:
            return np.zeros(6)
        # Seed along fixed basis direction
        basis = get_cycle_basis(B, W)
        u = basis[:, 0]
        return u * np.sqrt(C_next)
    
    # Preserve direction, rescale magnitude
    scale = np.sqrt(C_next / C_current)
    MAX_SCALE_RATIO = 10.0
    scale = min(scale, MAX_SCALE_RATIO)
    return c_current * scale


def step(
    econ_state: EconomyState,
    emp_state: EmploymentState,
    edu_state: EducationState,
    geometry_objects: Dict,
    params: Dict[str, float]
) -> Tuple[EconomyState, EmploymentState, EducationState]:
    """
    Performs one time step for all domains using CGM dynamics.
    
    Args:
        econ_state: Economy state.
        emp_state: Employment state.
        edu_state: Education state.
        geometry_objects: Contains B, W, P_grad, P_cycle.
        params: Coupling coefficients (including A_star).
    
    Returns:
        (econ_state_new, emp_state_new, edu_state_new): Updated states.
    """
    B = geometry_objects["B"]
    W = geometry_objects["W"]
    P_grad = geometry_objects["P_grad"]
    P_cycle = geometry_objects["P_cycle"]
    
    A_star = params.get("A_star", A_STAR)
    
    # Compute A(t) from current state (required for predict-step ordering)
    A_Econ_t = ensure_aperture(econ_state)
    A_Emp_t = ensure_aperture(emp_state)
    A_Edu_t = ensure_aperture(edu_state)
    
    # Dynamics target apertures fixed to CGM canonical A*
    A_Econ_target = A_star
    A_Emp_target = A_star
    A_Edu_target = A_star
    
    # Update potentials (vertex values) using A(t)
    x_econ_next = update_economy_potentials(econ_state, edu_state, params, A_Econ_t)
    
    x_emp_next = update_employment_potentials(emp_state, econ_state, params, A_Emp_t)
    x_edu_next = update_education_potentials(edu_state, econ_state, emp_state, params, A_Edu_t)
    
    # Compute gradient components (from potentials)
    y_grad_econ = B.T @ x_econ_next
    y_grad_emp = B.T @ x_emp_next
    y_grad_edu = B.T @ x_edu_next
    
    # Get current edge vectors (or initialize from gradient)
    y_econ_current = econ_state.y if econ_state.y is not None else y_grad_econ
    y_emp_current = emp_state.y if emp_state.y is not None else y_grad_emp
    y_edu_current = edu_state.y if edu_state.y is not None else y_grad_edu
    
    # Update cycle components with feedback toward target aperture
    c_econ_next = update_cycle_component(
        y_econ_current, y_grad_econ, A_Econ_target, B, W, P_cycle, None
    )
    c_emp_next = update_cycle_component(
        y_emp_current, y_grad_emp, A_Emp_target, B, W, P_cycle, None
    )
    c_edu_next = update_cycle_component(
        y_edu_current, y_grad_edu, A_Edu_target, B, W, P_cycle, None
    )
    
    # Construct new edge vectors: y = y_grad + c
    y_econ_next = y_grad_econ + c_econ_next
    y_emp_next = y_grad_emp + c_emp_next
    y_edu_next = y_grad_edu + c_edu_next
    
    # Perform Hodge decomposition and compute emergent apertures
    _, y_cycle_econ = hodge_decomposition(y_econ_next, P_grad, P_cycle)
    A_Econ_next = compute_aperture(y_econ_next, y_cycle_econ, W)
    
    _, y_cycle_emp = hodge_decomposition(y_emp_next, P_grad, P_cycle)
    A_Emp_next = compute_aperture(y_emp_next, y_cycle_emp, W)
    
    _, y_cycle_edu = hodge_decomposition(y_edu_next, P_grad, P_cycle)
    A_Edu_next = compute_aperture(y_edu_next, y_cycle_edu, W)
    
    # Create new state objects
    econ_state_new = EconomyState(
        x_econ_next[0], x_econ_next[1], x_econ_next[2], x_econ_next[3],
        y=y_econ_next, A=A_Econ_next
    )
    
    emp_state_new = EmploymentState(
        x_emp_next[0], x_emp_next[1], x_emp_next[2], x_emp_next[3],
        y=y_emp_next, A=A_Emp_next
    )
    
    edu_state_new = EducationState(
        x_edu_next[0], x_edu_next[1], x_edu_next[2], x_edu_next[3],
        y=y_edu_next, A=A_Edu_next
    )
    
    return econ_state_new, emp_state_new, edu_state_new
