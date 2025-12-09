"""
Dynamics Module

Discrete-time update rules for domain states on K4 geometry.
Coupling coefficients derived from CGM stage weights.

Cross-domain flows:
    - α: Education → Economy (closed loop: Education → Economy → Employment → Education)
    - β: Economy → Employment
    - γ: Employment → Education
    - Ecology: BU dual combination of all three derivative domains

Reference: CGM Paper Section 4
"""

import numpy as np
from typing import Dict, Optional, Tuple

from .domains import EconomyState, EmploymentState, EducationState, EcologyState
from .geometry import (
    hodge_decomposition, compute_aperture, get_cycle_basis
)
from .cgm_constants import (
    A_STAR, derive_all_coefficients, compute_canonical_cycle_rate
)


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
    params: Dict[str, float]
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
    A_Econ = econ_state.A if econ_state.A is not None else A_star
    
    # Get education capacities (source of Egress flow)
    GT = edu_state.GT
    IV = edu_state.IV
    IA = edu_state.IA
    IInteg = edu_state.IInteg
    
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
    
    # Authentic contribution: self-governance (aperture feedback)
    x_current = np.array([Gov, Info, Infer, Int])
    delta_authentic = np.array([
        -alpha2 * (A_Econ - A_star),
        -alpha4 * (A_Econ - A_star),
        -alpha6 * (A_Econ - A_star),
        -alpha8 * (A_Econ - A_star)
    ])
    
    # Derivative contribution: cross-domain flow from education (THM → CGM)
    delta_derivative = np.array([
        alpha1 * (GT - Gov),
        alpha3 * (IV - Info),
        alpha5 * (IA - Infer),
        alpha7 * (IInteg - Int)
    ])
    
    x_raw = x_current + delta_authentic + delta_derivative
    
    # Clip to [0, 1]
    x_next = np.array([
        np.clip(x_raw[0], 0.0, 1.0),
        np.clip(x_raw[1], 0.0, 1.0),
        np.clip(x_raw[2], 0.0, 1.0),
        np.clip(x_raw[3], 0.0, 1.0)
    ])
    
    # Store decomposition (THM: Authentic vs Derivative)
    econ_state.delta_authentic = delta_authentic
    econ_state.delta_derivative = delta_derivative
    
    return x_next


def update_employment_potentials(
    emp_state: EmploymentState,
    econ_state: EconomyState,
    params: Dict[str, float]
) -> Tuple[np.ndarray, float]:
    """
    Updates employment potentials from economy influence.
    
    Implements beta couplings (Economy -> Employment).
    
    Args:
        emp_state: Current employment state.
        econ_state: Current economy state.
        params: Coupling coefficients.
    
    Returns:
        (x_next, scale): Updated potentials and pre-normalization total.
    """
    # Get current values
    GM = emp_state.GM
    ICu = emp_state.ICu
    IInter = emp_state.IInter
    ICo = emp_state.ICo
    
    # Get A_star first (CGM canonical value)
    A_star = params.get("A_star", A_STAR)
    A_Emp = emp_state.A if emp_state.A is not None else A_star
    
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
    
    # Authentic contribution: self-governance (aperture feedback)
    delta_authentic = np.array([
        -beta2 * (A_Emp - A_star),
        -beta4 * (A_Emp - A_star),
        -beta6 * (A_Emp - A_star),
        -beta8 * (A_Emp - A_star)
    ])
    
    # Derivative contribution: cross-domain flow from economy
    delta_derivative = np.array([
        beta1 * (Gov - GM),
        beta3 * (Info - ICu),
        beta5 * (Infer - IInter),
        beta7 * (Int - ICo)
    ])
    
    x_raw = x_current + delta_authentic + delta_derivative
    
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
    
    # Store decomposition (THM: Authentic vs Derivative)
    emp_state.delta_authentic = delta_authentic
    emp_state.delta_derivative = delta_derivative

    return x_next, total


def update_education_potentials(
    edu_state: EducationState,
    econ_state: EconomyState,
    emp_state: EmploymentState,
    params: Dict[str, float]
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
        Updated potentials [GT, IV, IA, IInteg].
    """
    # Get current values
    GT = edu_state.GT
    IV = edu_state.IV
    IA = edu_state.IA
    IInteg = edu_state.IInteg
    
    # Get A_star first (CGM canonical value)
    A_star = params.get("A_star", A_STAR)
    A_Edu = edu_state.A if edu_state.A is not None else A_star
    
    # Get employment shares (source of Ingress flow)
    GM = emp_state.GM
    ICu = emp_state.ICu
    IInter = emp_state.IInter
    ICo = emp_state.ICo
    
    # Get CGM-derived coefficients (must be provided via params)
    # Note: Ingress uses BU duality scaling (δ_BU/m_a ≈ 0.9793) in derive_gamma_coefficients
    
    # CS stage (Governance) - Systems Operation
    gamma2 = params["gamma2"]   # GT ← GM
    gamma3 = params["gamma3"]   # CS feedback
    
    # UNA stage (Information)
    gamma5 = params["gamma5"]   # IV ← ICu
    gamma6 = params["gamma6"]   # UNA feedback
    
    # ONA stage (Inference)
    gamma8 = params["gamma8"]   # IA ← IInter
    gamma9 = params["gamma9"]   # ONA feedback
    
    # BU stage (Intelligence)
    gamma11 = params["gamma11"]  # IInteg ← ICo
    gamma12 = params["gamma12"]  # BU feedback
    
    # Update potentials with RESTORING dynamics
    x_current = np.array([GT, IV, IA, IInteg])
    
    # Authentic contribution: self-governance (aperture feedback)
    delta_authentic = np.array([
        -gamma3 * (A_Edu - A_star),
        -gamma6 * (A_Edu - A_star),
        -gamma9 * (A_Edu - A_star),
        -gamma12 * (A_Edu - A_star)
    ])
    
    # Derivative contribution: cross-domain flow from employment only
    delta_derivative = np.array([
        gamma2 * (GM - GT),
        gamma5 * (ICu - IV),
        gamma8 * (IInter - IA),
        gamma11 * (ICo - IInteg)
    ])
    
    x_raw = x_current + delta_authentic + delta_derivative
    
    # Clip to [0, 1]
    x_next = np.array([
        np.clip(x_raw[0], 0.0, 1.0),
        np.clip(x_raw[1], 0.0, 1.0),
        np.clip(x_raw[2], 0.0, 1.0),
        np.clip(x_raw[3], 0.0, 1.0)
    ])
    
    # Store decomposition (THM: Authentic vs Derivative)
    edu_state.delta_authentic = delta_authentic
    edu_state.delta_derivative = delta_derivative
    
    return x_next


def compute_ecology_potentials(
    econ_state: EconomyState,
    emp_state: EmploymentState,
    edu_state: EducationState
) -> tuple:
    """
    Computes ecology potentials via BU dual combination (CGM-derived).
    
    Ecology as the BU-vertex domain is a convex combination of:
    - Canonical balanced memory (Ingress): 97.93% weight
    - Current derivative domains state (Egress): 2.07% weight
    
    x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
    
    This uses NO arbitrary parameters. All weights derive from CGM:
    - δ_BU/m_a ≈ 0.9793 (BU duality ratio, Ingress weight)
    - A* ≈ 0.0207 (canonical aperture, Egress weight)
    - x_balanced = [w_CS, w_UNA, w_ONA, w_BU] (CGM stage weights)
    - x_deriv aggregates all three derivative domains (Economy, Employment, Education)
    
    Args:
        econ_state: Current economy state.
        emp_state: Current employment state.
        edu_state: Current education state.
    
    Returns:
        tuple: (x_ecol, displacement_vector) where:
            - x_ecol: Ecology state potentials [E_gov, E_info, E_inf, E_intel]
              (BU-vertex stage coordinates)
            - displacement_vector: [GTD, IVD, IAD, IID] = |x_deriv - x_balanced|
              (THM displacement magnitudes)
    """
    from .cgm_constants import (
        BU_DUALITY_RATIO, A_STAR, compute_stage_weights
    )
    
    # Canonical balanced profile from CGM stage weights
    weights = compute_stage_weights(include_bu=True)
    x_balanced = np.array([
        weights["w_CS"],   # ≈ 0.513
        weights["w_UNA"],  # ≈ 0.231
        weights["w_ONA"],  # ≈ 0.256
        weights["w_BU"]    # ≈ 0.013
    ])
    
    # Aggregate all three derivative domains (CGM BU-Ingress memory requirement)
    # BU reconstructs CS (Economy), UNA (Employment), ONA (Education)
    x_econ = econ_state.to_potential_vector()
    x_emp = emp_state.to_potential_vector()
    x_edu = edu_state.to_potential_vector()
    x_deriv = (x_econ + x_emp + x_edu) / 3.0
    
    # Compute displacement vector: D = |x_deriv - x_balanced|
    displacement_vector = np.abs(x_deriv - x_balanced)
    
    # BU dual combination: Ingress memory + Egress actuality
    # x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
    x_ecol = BU_DUALITY_RATIO * x_balanced + A_STAR * x_deriv
    
    return x_ecol, displacement_vector


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
    Updates cycle component toward target aperture.
    
    Target cycle energy from A = C/(G+C): C_target = A·G/(1-A).
    Rate-limited adjustment: factor = 1 + rate·(ratio - 1).
    
    Args:
        y_current: Current edge vector (6D).
        y_grad_new: New gradient component.
        A_target: Target aperture.
        B: Incidence matrix (4x6).
        W: Weight matrix (6x6).
        P_cycle: Cycle projection (6x6).
        cycle_evolution_rate: Adjustment rate. If None, uses canonical rate.
    
    Returns:
        Updated cycle component (6D).
    """
    if cycle_evolution_rate is None:
        cycle_evolution_rate = compute_canonical_cycle_rate(use_bu_weight=False)
    # Extract current cycle component
    c_current = P_cycle @ y_current
    
    # Compute current cycle energy
    c_norm_sq = np.dot(c_current, W @ c_current)
    c_norm = np.sqrt(c_norm_sq) if c_norm_sq > 0 else 0.0
    
    # Compute gradient energy for reference scale
    G = np.dot(y_grad_new, W @ y_grad_new)
    G = max(G, 1e-10)  # Avoid division by zero
    
    # Target cycle energy to achieve A_target:
    # A = C / (G + C) => C = A * G / (1 - A)
    if A_target >= 1.0:
        A_target = 0.99  # Cap to avoid division by zero
    if A_target <= 0.0:
        # Target is pure gradient (no cycle)
        return np.zeros(6)
    
    C_target = A_target * G / (1.0 - A_target)
    c_target_norm = np.sqrt(C_target)
    
    # Compute feedback: how far is current cycle from target?
    if c_norm > 0:
        # Scale existing cycle toward target
        ratio = c_target_norm / c_norm
        # Apply rate-limited adjustment
        factor = 1.0 + cycle_evolution_rate * (ratio - 1.0)
        factor = np.clip(factor, 0.5, 2.0)  # Limit rate of change
        c_next = c_current * factor
    else:
        # No existing cycle - need to seed one
        # Get a cycle basis vector
        cycle_basis = get_cycle_basis(B, W)
        if cycle_basis.shape[1] > 0:
            # Use first basis vector, scaled to target
            u = cycle_basis[:, 0]
            # Apply gradual growth toward target
            c_next = u * c_target_norm * cycle_evolution_rate
        else:
            c_next = np.zeros(6)
    
    return c_next


def step(
    econ_state: EconomyState,
    emp_state: EmploymentState,
    edu_state: EducationState,
    geometry_objects: Dict,
    params: Dict[str, float],
    scenario_aperture_settings: Dict[str, Optional[float]],
    ecol_state: EcologyState = None
) -> tuple:
    """
    Performs one time step for all domains.
    
    Args:
        econ_state: Economy state.
        emp_state: Employment state.
        edu_state: Education state.
        geometry_objects: Contains B, W, P_grad, P_cycle.
        params: Coupling coefficients.
        scenario_aperture_settings: Dict with keys:
            - "A_Econ_target": Target aperture for economy
            - "A_Emp_target": Target aperture for employment
            - "A_Edu_target": Target aperture for education
            - "A_Ecol_target": Target aperture for ecology
            - "cycle_evolution_rate": Rate of cycle adjustment (None for canonical)
        ecol_state: Ecology state (optional for backward compatibility).
    
    Returns:
        (econ_state_new, emp_state_new, edu_state_new[, ecol_state_new]): Updated states.
    """
    B = geometry_objects["B"]
    W = geometry_objects["W"]
    P_grad = geometry_objects["P_grad"]
    P_cycle = geometry_objects["P_cycle"]
    
    A_star = params.get("A_star", A_STAR)
    cycle_rate = scenario_aperture_settings.get("cycle_evolution_rate", None)
    
    # Dynamics target A* (the CGM canonical aperture)
    A_Econ_target = A_star
    A_Emp_target = A_star
    A_Edu_target = A_star
    
    # Update potentials (vertex values)
    x_econ_next = update_economy_potentials(econ_state, edu_state, params)
    
    # Note: Ecology feedback is now implicit through the BU dual combination
    # No arbitrary λ parameters - ecology affects economy through structural coupling
    
    x_emp_next, emp_scale = update_employment_potentials(emp_state, econ_state, params)
    x_edu_next = update_education_potentials(edu_state, econ_state, emp_state, params)
    
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
        y_econ_current, y_grad_econ, A_Econ_target, B, W, P_cycle, cycle_rate
    )
    c_emp_next = update_cycle_component(
        y_emp_current, y_grad_emp, A_Emp_target, B, W, P_cycle, cycle_rate
    )
    c_edu_next = update_cycle_component(
        y_edu_current, y_grad_edu, A_Edu_target, B, W, P_cycle, cycle_rate
    )
    
    # Construct new edge vectors: y = y_grad + c
    y_econ_next = y_grad_econ + c_econ_next
    y_emp_next = y_grad_emp + c_emp_next
    y_edu_next = y_grad_edu + c_edu_next
    
    # Perform Hodge decomposition and compute emergent apertures
    y_grad_econ_decomp, y_cycle_econ = hodge_decomposition(y_econ_next, P_grad, P_cycle)
    A_Econ_next = compute_aperture(y_econ_next, y_cycle_econ, W)
    
    y_grad_emp_decomp, y_cycle_emp = hodge_decomposition(y_emp_next, P_grad, P_cycle)
    A_Emp_next = compute_aperture(y_emp_next, y_cycle_emp, W)
    
    y_grad_edu_decomp, y_cycle_edu = hodge_decomposition(y_edu_next, P_grad, P_cycle)
    A_Edu_next = compute_aperture(y_edu_next, y_cycle_edu, W)
    
    # Compute SI using canonical CGM formula: SI = 100 / max(A/A*, A*/A)
    from .alignment import compute_domain_SI
    
    SI_econ_next = compute_domain_SI(A_Econ_next, A_star)
    SI_emp_next = compute_domain_SI(A_Emp_next, A_star)
    SI_edu_next = compute_domain_SI(A_Edu_next, A_star)
    
    # Create new state objects
    # S field stores SI/100 for backward compatibility with state objects
    econ_state_new = EconomyState(
        x_econ_next[0], x_econ_next[1], x_econ_next[2], x_econ_next[3],
        y=y_econ_next, A=A_Econ_next, S=SI_econ_next / 100.0
    )
    
    # Populate Authentic-Derivative decomposition (THM terminology)
    if hasattr(econ_state, "delta_authentic") and hasattr(econ_state, "delta_derivative"):
        delta_a = getattr(econ_state, "delta_authentic")
        delta_d = getattr(econ_state, "delta_derivative")
        econ_state_new.y_authentic = B.T @ delta_a
        econ_state_new.y_derivative = B.T @ delta_d
    
    emp_state_new = EmploymentState(
        x_emp_next[0], x_emp_next[1], x_emp_next[2], x_emp_next[3],
        y=y_emp_next, A=A_Emp_next, S=SI_emp_next / 100.0, scale=emp_scale
    )
    
    if hasattr(emp_state, "delta_authentic") and hasattr(emp_state, "delta_derivative"):
        delta_a = getattr(emp_state, "delta_authentic")
        delta_d = getattr(emp_state, "delta_derivative")
        emp_state_new.y_authentic = B.T @ delta_a
        emp_state_new.y_derivative = B.T @ delta_d
    
    edu_state_new = EducationState(
        x_edu_next[0], x_edu_next[1], x_edu_next[2], x_edu_next[3],
        y=y_edu_next, A=A_Edu_next, S=SI_edu_next / 100.0
    )
    
    if hasattr(edu_state, "delta_authentic") and hasattr(edu_state, "delta_derivative"):
        delta_a = getattr(edu_state, "delta_authentic")
        delta_d = getattr(edu_state, "delta_derivative")
        edu_state_new.y_authentic = B.T @ delta_a
        edu_state_new.y_derivative = B.T @ delta_d
    
    # Compute scalar metrics for recording (using updated attribute names)
    if hasattr(econ_state_new, 'y_authentic') and econ_state_new.y_authentic is not None:
        econ_state_new.y_H = econ_state_new.y_authentic  # Compatibility
        econ_state_new.y_AI = econ_state_new.y_derivative
        econ_state_new.human_metric = econ_state_new.get_human_gradient_fraction(P_grad, W)
        econ_state_new.ai_metric = econ_state_new.get_ai_cycle_energy(P_cycle, W)
    else:
        econ_state_new.human_metric = 0.0
        econ_state_new.ai_metric = 0.0
    
    if hasattr(emp_state_new, 'y_authentic') and emp_state_new.y_authentic is not None:
        emp_state_new.y_H = emp_state_new.y_authentic
        emp_state_new.y_AI = emp_state_new.y_derivative
        emp_state_new.human_metric = emp_state_new.get_human_gradient_fraction(P_grad, W)
        emp_state_new.ai_metric = emp_state_new.get_ai_cycle_energy(P_cycle, W)
    else:
        emp_state_new.human_metric = 0.0
        emp_state_new.ai_metric = 0.0
    
    if hasattr(edu_state_new, 'y_authentic') and edu_state_new.y_authentic is not None:
        edu_state_new.y_H = edu_state_new.y_authentic
        edu_state_new.y_AI = edu_state_new.y_derivative
        edu_state_new.human_metric = edu_state_new.get_human_gradient_fraction(P_grad, W)
        edu_state_new.ai_metric = edu_state_new.get_ai_cycle_energy(P_cycle, W)
    else:
        edu_state_new.human_metric = 0.0
        edu_state_new.ai_metric = 0.0
    
    # Process ecology if state provided
    # Ecology uses CGM-derived BU dual combination (NO arbitrary parameters)
    if ecol_state is not None:
        A_Ecol_target = A_star
        
        # Compute ecology potentials via BU dual combination
        # x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
        # Uses updated derivative domain states
        temp_econ = EconomyState(
            x_econ_next[0], x_econ_next[1], x_econ_next[2], x_econ_next[3]
        )
        temp_emp = EmploymentState(
            x_emp_next[0], x_emp_next[1], x_emp_next[2], x_emp_next[3]
        )
        temp_edu = EducationState(
            x_edu_next[0], x_edu_next[1], x_edu_next[2], x_edu_next[3]
        )
        
        x_ecol_next, displacement_vector = compute_ecology_potentials(temp_econ, temp_emp, temp_edu)
        
        # Compute gradient component
        y_grad_ecol = B.T @ x_ecol_next
        y_ecol_current = ecol_state.y if ecol_state.y is not None else y_grad_ecol
        
        # Update cycle component
        c_ecol_next = update_cycle_component(
            y_ecol_current, y_grad_ecol, A_Ecol_target, B, W, P_cycle, cycle_rate
        )
        
        # Construct edge vector
        y_ecol_next = y_grad_ecol + c_ecol_next
        
        # Hodge decomposition and aperture
        y_grad_ecol_decomp, y_cycle_ecol = hodge_decomposition(y_ecol_next, P_grad, P_cycle)
        A_Ecol_next = compute_aperture(y_ecol_next, y_cycle_ecol, W)
        SI_ecol_next = compute_domain_SI(A_Ecol_next, A_star)
        
        # Create new ecology state with displacement vector
        ecol_state_new = EcologyState(
            E_gov=x_ecol_next[0],
            E_info=x_ecol_next[1],
            E_inf=x_ecol_next[2],
            E_intel=x_ecol_next[3],
            y=y_ecol_next, A=A_Ecol_next, S=SI_ecol_next / 100.0,
            GTD=displacement_vector[0],
            IVD=displacement_vector[1],
            IAD=displacement_vector[2],
            IID=displacement_vector[3]
        )
        
        return econ_state_new, emp_state_new, edu_state_new, ecol_state_new
    
    return econ_state_new, emp_state_new, edu_state_new
