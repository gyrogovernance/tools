"""
Simulation Runner and Scenario Configuration

Coordinates scenario execution, tracks trajectories, and exports results.

Reference: gyroscopic_global_governance.md Section 4
"""

import numpy as np
from typing import Dict, List, Optional, Any
import json
import csv
from pathlib import Path

from .geometry import (
    get_incidence_matrix, get_weight_matrix, compute_projections
)
from .domains import EconomyState, EmploymentState, EducationState, EcologyState
from .dynamics import step
from .alignment import compute_domain_SI, A_STAR
from .geometry import (
    construct_edge_vector_with_aperture, hodge_decomposition, compute_aperture
)
from .lyapunov import precompute_cgm_lyapunov_constants, compute_total_lyapunov


class ScenarioConfig:
    """
    Scenario configuration container.
    
    Stores initial conditions, parameters, and aperture settings.
    """
    
    def __init__(
        self,
        # Initial economy potentials
        Gov0: float = 0.5,
        Info0: float = 0.5,
        Infer0: float = 0.5,
        Int0: float = 0.5,
        # Initial employment shares
        GM0: float = 0.25,
        ICu0: float = 0.25,
        IInter0: float = 0.25,
        ICo0: float = 0.25,
        # Initial education capacities (THM principles)
        GMT0: float = 0.5,      # Governance Management Traceability
        ICV0: float = 0.5,     # Information Curation Variety
        IIA0: float = 0.5,      # Inference Interaction Accountability
        ICI0: float = 0.5,    # Intelligence Cooperation Integrity
        # Note: Ecology initial values are CGM-derived from indirect domains
        # via BU dual combination: x_Ecol = (δ_BU/m_a)·x_balanced + A*·x_deriv
        # No arbitrary initial ecology parameters needed.
        # Target apertures
        A_Econ_target: Optional[float] = 0.0207,
        A_Emp_target: Optional[float] = 0.0207,
        A_Edu_target: Optional[float] = 0.0207,
        A_Ecol_target: Optional[float] = 0.0207,
        # Enable/disable ecology
        include_ecology: bool = True,
        # Update parameters
        alpha1: float = 0.01,
        alpha2: float = 0.01,
        alpha3: float = 0.01,
        alpha4: float = 0.01,
        alpha5: float = 0.01,
        alpha6: float = 0.01,
        alpha7: float = 0.01,
        alpha8: float = 0.01,
        beta1: float = 0.01,
        beta2: float = 0.01,
        beta3: float = 0.01,
        beta4: float = 0.01,
        beta5: float = 0.01,
        beta6: float = 0.01,
        beta7: float = 0.01,
        beta8: float = 0.01,
        gamma1: float = 0.01,
        gamma2: float = 0.01,
        gamma3: float = 0.01,
        gamma4: float = 0.01,
        gamma5: float = 0.01,
        gamma6: float = 0.01,
        gamma7: float = 0.01,
        gamma8: float = 0.01,
        gamma9: float = 0.01,
        gamma10: float = 0.01,
        gamma11: float = 0.01,
        gamma12: float = 0.01,
        # Other parameters
        A_star: float = A_STAR,
        alignment_weights: Optional[Dict[str, float]] = None,
        cycle_evolution_rate: float = None,  # If None, uses canonical rate κ₀ ≈ 0.04
        # Simulation parameters
        num_steps: int = 100,
        dt: float = 1.0,
        time_unit: str = "steps"
    ):
        """Initialize scenario configuration."""
        self.Gov0 = Gov0
        self.Info0 = Info0
        self.Infer0 = Infer0
        self.Int0 = Int0
        self.GM0 = GM0
        self.ICu0 = ICu0
        self.IInter0 = IInter0
        self.ICo0 = ICo0
        self.GMT0 = GMT0
        self.ICV0 = ICV0
        self.IIA0 = IIA0
        self.ICI0 = ICI0
        # Ecology initial values are CGM-derived (no arbitrary parameters)
        self.A_Econ_target = A_Econ_target
        self.A_Emp_target = A_Emp_target
        self.A_Edu_target = A_Edu_target
        self.A_Ecol_target = A_Ecol_target
        self.include_ecology = include_ecology
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.alpha4 = alpha4
        self.alpha5 = alpha5
        self.alpha6 = alpha6
        self.alpha7 = alpha7
        self.alpha8 = alpha8
        self.beta1 = beta1
        self.beta2 = beta2
        self.beta3 = beta3
        self.beta4 = beta4
        self.beta5 = beta5
        self.beta6 = beta6
        self.beta7 = beta7
        self.beta8 = beta8
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.gamma3 = gamma3
        self.gamma4 = gamma4
        self.gamma5 = gamma5
        self.gamma6 = gamma6
        self.gamma7 = gamma7
        self.gamma8 = gamma8
        self.gamma9 = gamma9
        self.gamma10 = gamma10
        self.gamma11 = gamma11
        self.gamma12 = gamma12
        self.A_star = A_star
        self.alignment_weights = alignment_weights or {}
        self.cycle_evolution_rate = cycle_evolution_rate
        self.num_steps = num_steps
        self.dt = dt  # Time step size (e.g., 1.0 for 1 year per step, 0.1 for 0.1 years per step)
        self.time_unit = time_unit  # Unit label (e.g., "years", "months", "decades", "steps")
    
    def to_params_dict(self) -> Dict[str, Any]:
        """Converts configuration to parameters dict for dynamics."""
        return {
            "alpha1": self.alpha1,
            "alpha2": self.alpha2,
            "alpha3": self.alpha3,
            "alpha4": self.alpha4,
            "alpha5": self.alpha5,
            "alpha6": self.alpha6,
            "alpha7": self.alpha7,
            "alpha8": self.alpha8,
            "beta1": self.beta1,
            "beta2": self.beta2,
            "beta3": self.beta3,
            "beta4": self.beta4,
            "beta5": self.beta5,
            "beta6": self.beta6,
            "beta7": self.beta7,
            "beta8": self.beta8,
            "gamma1": self.gamma1,
            "gamma2": self.gamma2,
            "gamma3": self.gamma3,
            "gamma4": self.gamma4,
            "gamma5": self.gamma5,
            "gamma6": self.gamma6,
            "gamma7": self.gamma7,
            "gamma8": self.gamma8,
            "gamma9": self.gamma9,
            "gamma10": self.gamma10,
            "gamma11": self.gamma11,
            "gamma12": self.gamma12,
            "A_star": self.A_star,
            "alignment_weights": self.alignment_weights
        }
    
    def to_aperture_settings(self) -> Dict[str, Optional[float]]:
        """Converts configuration to aperture settings dict."""
        return {
            "A_Econ_target": self.A_Econ_target,
            "A_Emp_target": self.A_Emp_target,
            "A_Edu_target": self.A_Edu_target,
            "A_Ecol_target": self.A_Ecol_target,
            "cycle_evolution_rate": self.cycle_evolution_rate
        }


class SimulationResult:
    """
    Container for simulation results.
    
    Stores time series of all state variables and metrics.
    
    SI values use the canonical CGM formula:
        D = max(A/A*, A*/A)
        SI = 100/D
    
    All SI values are on [0, 100] scale where:
        - SI = 100 means A = A* (perfect alignment)
        - SI < 100 means deviation from optimal aperture
    """
    
    def __init__(self, num_steps: int, dt: float = 1.0, time_unit: str = "steps"):
        """
        Initialize result containers.
        
        Args:
            num_steps: Number of simulation steps
            dt: Time step size (default 1.0)
            time_unit: Unit label for time (default "steps")
        """
        self.num_steps = num_steps
        self.dt = dt
        self.time_unit = time_unit
        
        # Economy
        self.Gov = np.zeros(num_steps + 1)
        self.Info = np.zeros(num_steps + 1)
        self.Infer = np.zeros(num_steps + 1)
        self.Int = np.zeros(num_steps + 1)
        self.A_Econ = np.zeros(num_steps + 1)
        self.SI_Econ = np.zeros(num_steps + 1)  # Renamed from S_Econ, now 0-100 scale
        
        # Employment
        self.GM = np.zeros(num_steps + 1)
        self.ICu = np.zeros(num_steps + 1)
        self.IInter = np.zeros(num_steps + 1)
        self.ICo = np.zeros(num_steps + 1)
        self.A_Emp = np.zeros(num_steps + 1)
        self.SI_Emp = np.zeros(num_steps + 1)  # Renamed from S_Work, now 0-100 scale
        
        # Education
        self.GMT = np.zeros(num_steps + 1)
        self.ICV = np.zeros(num_steps + 1)
        self.IIA = np.zeros(num_steps + 1)
        self.ICI = np.zeros(num_steps + 1)
        self.A_Edu = np.zeros(num_steps + 1)
        self.SI_Edu = np.zeros(num_steps + 1)  # Renamed from S_Edu, now 0-100 scale
        
        # Ecology (BU-vertex, CGM-derived)
        self.E_gov = np.zeros(num_steps + 1)  # State potentials
        self.E_info = np.zeros(num_steps + 1)
        self.E_inf = np.zeros(num_steps + 1)
        self.E_intel = np.zeros(num_steps + 1)
        self.A_Ecol = np.zeros(num_steps + 1)
        self.SI_Ecol = np.zeros(num_steps + 1)
        # Displacement vector: D = |x_deriv - x_balanced|
        self.GTD = np.zeros(num_steps + 1)
        self.IVD = np.zeros(num_steps + 1)
        self.IAD = np.zeros(num_steps + 1)
        self.IID = np.zeros(num_steps + 1)
        
        # Flag for whether ecology is included
        self.include_ecology = True
        
        # Human-AI decomposition metrics
        self.human_frac_Econ = np.zeros(num_steps + 1)
        self.ai_metric_Econ = np.zeros(num_steps + 1)
        self.human_frac_Emp = np.zeros(num_steps + 1)
        self.ai_metric_Emp = np.zeros(num_steps + 1)
        self.human_frac_Edu = np.zeros(num_steps + 1)
        self.ai_metric_Edu = np.zeros(num_steps + 1)
        
        # Lyapunov governance potential (CGM-derived)
        self.V_CGM = np.zeros(num_steps + 1)
        self.V_grad_total = np.zeros(num_steps + 1)
        self.V_cycle_total = np.zeros(num_steps + 1)
        # Per-domain contributions
        self.V_grad_Econ = np.zeros(num_steps + 1)
        self.V_cycle_Econ = np.zeros(num_steps + 1)
        self.V_grad_Emp = np.zeros(num_steps + 1)
        self.V_cycle_Emp = np.zeros(num_steps + 1)
        self.V_grad_Edu = np.zeros(num_steps + 1)
        self.V_cycle_Edu = np.zeros(num_steps + 1)
        self.V_grad_Ecol = np.zeros(num_steps + 1)
        self.V_cycle_Ecol = np.zeros(num_steps + 1)
        
        # Time array (actual time values)
        self.time = np.arange(num_steps + 1) * dt
    
    def record_step(self, t: int, econ_state: EconomyState,
                   emp_state: EmploymentState, edu_state: EducationState,
                   A_star: float = A_STAR, ecol_state: EcologyState = None):
        """
        Record state at time step t.
        
        Computes SI using canonical CGM formula:
            D = max(A/A*, A*/A)
            SI = 100/D
        
        Args:
            t: Time step index
            econ_state: Economy state
            emp_state: Employment state
            edu_state: Education state
            A_star: Target aperture (default 0.0207)
            ecol_state: Ecology state (optional)
        """
        # Economy
        self.Gov[t] = econ_state.Gov
        self.Info[t] = econ_state.Info
        self.Infer[t] = econ_state.Infer
        self.Int[t] = econ_state.Int
        self.A_Econ[t] = econ_state.A if econ_state.A is not None else 0.0
        # Compute SI using canonical CGM formula
        self.SI_Econ[t] = compute_domain_SI(self.A_Econ[t], A_star)
        
        # Employment
        self.GM[t] = emp_state.GM
        self.ICu[t] = emp_state.ICu
        self.IInter[t] = emp_state.IInter
        self.ICo[t] = emp_state.ICo
        self.A_Emp[t] = emp_state.A if emp_state.A is not None else 0.0
        # Compute SI using canonical CGM formula
        self.SI_Emp[t] = compute_domain_SI(self.A_Emp[t], A_star)
        
        # Education
        self.GMT[t] = edu_state.GMT
        self.ICV[t] = edu_state.ICV
        self.IIA[t] = edu_state.IIA
        self.ICI[t] = edu_state.ICI
        self.A_Edu[t] = edu_state.A if edu_state.A is not None else 0.0
        # Compute SI using canonical CGM formula
        self.SI_Edu[t] = compute_domain_SI(self.A_Edu[t], A_star)
        
        # Ecology (if provided)
        if ecol_state is not None:
            self.include_ecology = True
            self.E_gov[t] = ecol_state.E_gov
            self.E_info[t] = ecol_state.E_info
            self.E_inf[t] = ecol_state.E_inf
            self.E_intel[t] = ecol_state.E_intel
            self.A_Ecol[t] = ecol_state.A if ecol_state.A is not None else 0.0
            self.SI_Ecol[t] = compute_domain_SI(self.A_Ecol[t], A_star)
            # Record displacement vector
            self.GTD[t] = ecol_state.GTD
            self.IVD[t] = ecol_state.IVD
            self.IAD[t] = ecol_state.IAD
            self.IID[t] = ecol_state.IID
        else:
            self.include_ecology = False
        
        # Human-AI decomposition metrics (computed in dynamics.step)
        if hasattr(econ_state, 'human_metric'):
            self.human_frac_Econ[t] = econ_state.human_metric
            self.ai_metric_Econ[t] = econ_state.ai_metric
        if hasattr(emp_state, 'human_metric'):
            self.human_frac_Emp[t] = emp_state.human_metric
            self.ai_metric_Emp[t] = emp_state.ai_metric
        if hasattr(edu_state, 'human_metric'):
            self.human_frac_Edu[t] = edu_state.human_metric
            self.ai_metric_Edu[t] = edu_state.ai_metric
    
    def record_lyapunov(
        self,
        t: int,
        V_total: float,
        V_grad_total: float,
        V_cycle_total: float,
        V_details: Dict[str, Dict[str, float]]
    ):
        """
        Record Lyapunov governance potential values at time step t.

        V_total = V_stage + V_apert, where:
          - V_stage: aggregate stage-profile displacement ||x_deriv - x_balanced||² / 2
          - V_apert: sum of per-domain aperture deviations (log(A_D/A*))² / 2

        Args:
            t: Time step index
            V_total: Total Lyapunov potential V_CGM
            V_grad_total: Stage-profile displacement term (mapped from V_stage)
            V_cycle_total: Aperture deviation term (mapped from V_apert)
            V_details: Per-domain contributions dict with "V_apert" and "A" keys
        """
        self.V_CGM[t] = V_total
        self.V_grad_total[t] = V_grad_total  # Maps to V_stage
        self.V_cycle_total[t] = V_cycle_total  # Maps to V_apert
        
        # Per-domain contributions
        # V_cycle_* fields store V_apert_D (aperture deviation per domain)
        # V_grad_* fields are left zero (stage term is system-level only)
        if "economy" in V_details:
            self.V_grad_Econ[t] = 0.0  # Stage term is aggregate only
            self.V_cycle_Econ[t] = V_details["economy"]["V_apert"]
        if "employment" in V_details:
            self.V_grad_Emp[t] = 0.0  # Stage term is aggregate only
            self.V_cycle_Emp[t] = V_details["employment"]["V_apert"]
        if "education" in V_details:
            self.V_grad_Edu[t] = 0.0  # Stage term is aggregate only
            self.V_cycle_Edu[t] = V_details["education"]["V_apert"]
        if "ecology" in V_details:
            self.V_grad_Ecol[t] = 0.0  # Stage term is aggregate only
            self.V_cycle_Ecol[t] = V_details["ecology"]["V_apert"]
    
    def to_dict(self) -> Dict[str, np.ndarray]:
        """Convert results to dictionary."""
        result = {
            "time": self.time,
            "Gov": self.Gov,
            "Info": self.Info,
            "Infer": self.Infer,
            "Int": self.Int,
            "A_Econ": self.A_Econ,
            "SI_Econ": self.SI_Econ,
            "GM": self.GM,
            "ICu": self.ICu,
            "IInter": self.IInter,
            "ICo": self.ICo,
            "A_Emp": self.A_Emp,
            "SI_Emp": self.SI_Emp,
            "GMT": self.GMT,
            "ICV": self.ICV,
            "IIA": self.IIA,
            "ICI": self.ICI,
            "A_Edu": self.A_Edu,
            "SI_Edu": self.SI_Edu,
            # Lyapunov governance potential
            "V_CGM": self.V_CGM,
            "V_grad_total": self.V_grad_total,
            "V_cycle_total": self.V_cycle_total,
            "V_grad_Econ": self.V_grad_Econ,
            "V_cycle_Econ": self.V_cycle_Econ,
            "V_grad_Emp": self.V_grad_Emp,
            "V_cycle_Emp": self.V_cycle_Emp,
            "V_grad_Edu": self.V_grad_Edu,
            "V_cycle_Edu": self.V_cycle_Edu,
        }
        if self.include_ecology:
            result.update({
                "E_gov": self.E_gov,
                "E_info": self.E_info,
                "E_inf": self.E_inf,
                "E_intel": self.E_intel,
                "A_Ecol": self.A_Ecol,
                "SI_Ecol": self.SI_Ecol,
                "GTD": self.GTD,
                "IVD": self.IVD,
                "IAD": self.IAD,
                "IID": self.IID,
                "V_grad_Ecol": self.V_grad_Ecol,
                "V_cycle_Ecol": self.V_cycle_Ecol,
            })
        return result
    
    def export_csv(self, filepath: str):
        """Export results to CSV file."""
        data = self.to_dict()
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header with time unit
            header = [f"time ({self.time_unit})"] + [key for key in data.keys() if key != "time"]
            writer.writerow(header)
            
            # Data rows
            for t in range(self.num_steps + 1):
                row = [self.time[t]] + [data[key][t] for key in data.keys() if key != "time"]
                writer.writerow(row)
    
    def export_json(self, filepath: str):
        """Export results to JSON file."""
        data = self.to_dict()
        
        # Convert numpy arrays to lists
        json_data = {key: arr.tolist() for key, arr in data.items()}
        json_data["num_steps"] = self.num_steps
        
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)


def initialize_states(
    config: ScenarioConfig,
    B: np.ndarray,
    W: np.ndarray,
    P_grad: np.ndarray,
    P_cycle: np.ndarray
) -> tuple:
    """
    Initializes domain states from configuration.
    
    Args:
        config: Scenario configuration
        B: Incidence matrix
        W: Weight matrix
        P_grad: Gradient projection matrix
        P_cycle: Cycle projection matrix
    
    Returns:
        (econ_state, emp_state, edu_state[, ecol_state]): Initialized states
    """
    # Create initial states
    econ_state = EconomyState(config.Gov0, config.Info0, config.Infer0, config.Int0)
    emp_state = EmploymentState(config.GM0, config.ICu0, config.IInter0, config.ICo0)
    edu_state = EducationState(
        config.GMT0, config.ICV0, config.IIA0, config.ICI0
    )
    
    # Construct initial edge vectors with target apertures
    x_econ = econ_state.to_potential_vector()
    x_emp = emp_state.to_potential_vector()
    x_edu = edu_state.to_potential_vector()
    
    y_econ = construct_edge_vector_with_aperture(
        x_econ, B, W, config.A_Econ_target
    )
    y_emp = construct_edge_vector_with_aperture(
        x_emp, B, W, config.A_Emp_target
    )
    y_edu = construct_edge_vector_with_aperture(
        x_edu, B, W, config.A_Edu_target
    )
    
    # Compute initial apertures and SI using canonical CGM formula
    # SI = 100 / max(A/A*, A*/A)
    y_grad_econ, y_cycle_econ = hodge_decomposition(y_econ, P_grad, P_cycle)
    A_Econ0 = compute_aperture(y_econ, y_cycle_econ, W)
    SI_Econ0 = compute_domain_SI(A_Econ0, config.A_star)
    
    y_grad_emp, y_cycle_emp = hodge_decomposition(y_emp, P_grad, P_cycle)
    A_Emp0 = compute_aperture(y_emp, y_cycle_emp, W)
    emp_scale = np.sum(x_emp)
    SI_Emp0 = compute_domain_SI(A_Emp0, config.A_star)
    
    y_grad_edu, y_cycle_edu = hodge_decomposition(y_edu, P_grad, P_cycle)
    A_Edu0 = compute_aperture(y_edu, y_cycle_edu, W)
    SI_Edu0 = compute_domain_SI(A_Edu0, config.A_star)
    
    # Update states with computed values
    # S field stores SI/100 for backward compatibility
    econ_state.y = y_econ
    econ_state.A = A_Econ0
    econ_state.S = SI_Econ0 / 100.0
    
    emp_state.y = y_emp
    emp_state.A = A_Emp0
    emp_state.S = SI_Emp0 / 100.0
    emp_state.scale = emp_scale
    
    edu_state.y = y_edu
    edu_state.A = A_Edu0
    edu_state.S = SI_Edu0 / 100.0
    
    # Initialize ecology if configured
    # Ecology uses CGM-derived BU dual combination (NO arbitrary parameters)
    if config.include_ecology:
        from .dynamics import compute_ecology_potentials
        
        # Compute initial ecology potentials from all three indirect domains
        # x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
        # where x_deriv = (x_econ + x_emp + x_edu) / 3.0 (CGM BU-Ingress memory)
        x_ecol, displacement_vector = compute_ecology_potentials(econ_state, emp_state, edu_state)
        
        ecol_state = EcologyState(
            E_gov=x_ecol[0],
            E_info=x_ecol[1],
            E_inf=x_ecol[2],
            E_intel=x_ecol[3],
            GTD=displacement_vector[0],
            IVD=displacement_vector[1],
            IAD=displacement_vector[2],
            IID=displacement_vector[3]
        )
        
        y_ecol = construct_edge_vector_with_aperture(
            x_ecol, B, W, config.A_Ecol_target
        )
        
        y_grad_ecol, y_cycle_ecol = hodge_decomposition(y_ecol, P_grad, P_cycle)
        A_Ecol0 = compute_aperture(y_ecol, y_cycle_ecol, W)
        SI_Ecol0 = compute_domain_SI(A_Ecol0, config.A_star)
        
        ecol_state.y = y_ecol
        ecol_state.A = A_Ecol0
        ecol_state.S = SI_Ecol0 / 100.0
        
        return econ_state, emp_state, edu_state, ecol_state
    
    return econ_state, emp_state, edu_state


def run_scenario(
    config: ScenarioConfig,
    weights: Optional[np.ndarray] = None,
    verbose: bool = True,
    progress_interval: int = 10
) -> SimulationResult:
    """
    Runs a simulation scenario.
    
    Args:
        config: Scenario configuration
        weights: Optional edge weights (6-element array). If None, uses identity.
        verbose: If True, print progress updates
        progress_interval: Print progress every N steps
    
    Returns:
        result: SimulationResult with time series data
    """
    # Initialize geometry
    B = get_incidence_matrix()
    W = get_weight_matrix(weights)
    P_grad, P_cycle = compute_projections(B, W)
    
    geometry_objects = {
        "B": B,
        "W": W,
        "P_grad": P_grad,
        "P_cycle": P_cycle
    }
    
    # Precompute CGM equilibrium quantities for Lyapunov computation
    x_balanced = precompute_cgm_lyapunov_constants()
    
    # Initialize states (pass P_grad and P_cycle to avoid recomputation)
    states = initialize_states(config, B, W, P_grad, P_cycle)
    
    if config.include_ecology:
        econ_state, emp_state, edu_state, ecol_state = states
    else:
        econ_state, emp_state, edu_state = states
        ecol_state = None
    
    # Initialize result container
    result = SimulationResult(config.num_steps, dt=config.dt, time_unit=config.time_unit)
    result.include_ecology = config.include_ecology
    
    # Record initial state
    result.record_step(0, econ_state, emp_state, edu_state, 
                       A_star=config.A_star, ecol_state=ecol_state)
    
    # Compute and record initial Lyapunov potential
    domain_states_init = {
        "economy": econ_state,
        "employment": emp_state,
        "education": edu_state,
    }
    if ecol_state is not None:
        domain_states_init["ecology"] = ecol_state
    
    V_total_init, V_apert_init, V_stage_init, V_details_init = compute_total_lyapunov(
        domain_states_init, B, W, P_grad, P_cycle, x_balanced, config.A_star
    )
    result.record_lyapunov(0, V_total_init, V_stage_init, V_apert_init, V_details_init)
    
    if verbose:
        time_label = f"Time ({config.time_unit})"
        if config.include_ecology:
            print(f"\n{'Step':<6} {time_label:<12} {'SI_Econ':<10} {'SI_Emp':<10} {'SI_Edu':<10} {'SI_Ecol':<10}")
            print(f"{'-'*6} {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
            print(f"{0:<6} {result.time[0]:<12.2f} {result.SI_Econ[0]:<10.2f} "
                  f"{result.SI_Emp[0]:<10.2f} {result.SI_Edu[0]:<10.2f} {result.SI_Ecol[0]:<10.2f}")
        else:
            print(f"\n{'Step':<6} {time_label:<12} {'SI_Econ':<10} {'SI_Emp':<10} {'SI_Edu':<10}")
            print(f"{'-'*6} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")
            print(f"{0:<6} {result.time[0]:<12.2f} {result.SI_Econ[0]:<10.2f} "
                  f"{result.SI_Emp[0]:<10.2f} {result.SI_Edu[0]:<10.2f}")
    
    # Get parameters
    params = config.to_params_dict()
    aperture_settings = config.to_aperture_settings()
    
    # Run simulation
    for t in range(1, config.num_steps + 1):
        step_result = step(
            econ_state, emp_state, edu_state,
            geometry_objects, params, aperture_settings,
            ecol_state=ecol_state
        )
        
        if config.include_ecology:
            econ_state, emp_state, edu_state, ecol_state = step_result
        else:
            econ_state, emp_state, edu_state = step_result
            
        result.record_step(t, econ_state, emp_state, edu_state, 
                          A_star=config.A_star, ecol_state=ecol_state)
        
        # Compute and record Lyapunov governance potential
        domain_states = {
            "economy": econ_state,
            "employment": emp_state,
            "education": edu_state,
        }
        if ecol_state is not None:
            domain_states["ecology"] = ecol_state
        
        V_total, V_apert, V_stage, V_details = compute_total_lyapunov(
            domain_states, B, W, P_grad, P_cycle, x_balanced, config.A_star
        )
        result.record_lyapunov(t, V_total, V_stage, V_apert, V_details)
        
        # Print progress
        if verbose and (t % progress_interval == 0 or t == config.num_steps):
            if config.include_ecology:
                print(f"{t:<6} {result.time[t]:<12.2f} {result.SI_Econ[t]:<10.2f} "
                      f"{result.SI_Emp[t]:<10.2f} {result.SI_Edu[t]:<10.2f} {result.SI_Ecol[t]:<10.2f}")
            else:
                print(f"{t:<6} {result.time[t]:<12.2f} {result.SI_Econ[t]:<10.2f} "
                      f"{result.SI_Emp[t]:<10.2f} {result.SI_Edu[t]:<10.2f}")
    
    if verbose:
        print()
    
    return result

