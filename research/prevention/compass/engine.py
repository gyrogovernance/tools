"""
Engine Module: Predict-Update-Output Cycle

Orchestrates the Compass reading generation through predict-update-output cycles.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple

from .cgm_constants import (
    A_STAR, A_INIT_DEFAULT, compute_stage_weights, derive_all_coefficients
)
from .geometry import (
    get_incidence_matrix, get_weight_matrix, compute_projections,
    hodge_decomposition, compute_aperture,
    construct_edge_vector_with_aperture
)
from .domains import EconomyState, EmploymentState, EducationState
from .dynamics import step
from .alignment import compute_domain_SI
from .filter import DisplacementFilter, generate_deterministic_seed
from .validation import validate_and_raise


class CompassEngine:
    """
    Main engine for the Gyroscopic Compass.
    """
    
    def __init__(
        self,
        measurement_noise: float = 0.05,
        mc_samples: int = 1000,
        maintenance_threshold: float = 0.10,
        min_route_stability: float = 0.65,
        tie_break_order: Optional[list] = None
    ):
        """
        Initialize Compass engine.
        
        Args:
            measurement_noise: Default measurement noise σ.
            mc_samples: Number of Monte Carlo samples.
            maintenance_threshold: Threshold for maintenance mode.
            min_route_stability: Minimum stability for active mode.
            tie_break_order: Order for tie-breaking (default: GTD > IAD > IVD > IID).
        """
        self.measurement_noise = measurement_noise
        self.mc_samples = mc_samples
        self.maintenance_threshold = maintenance_threshold
        self.min_route_stability = min_route_stability
        
        if tie_break_order is None:
            tie_break_order = ["GTD", "IAD", "IVD", "IID"]
        self.tie_break_order = tie_break_order
        
        # Geometry objects (computed once)
        self.B = get_incidence_matrix()
        self.W = get_weight_matrix()
        self.P_grad, self.P_cycle = compute_projections(self.B, self.W)
        
        # CGM parameters
        self.params = derive_all_coefficients(coupling_strength=1.0, dt=1.0)
        
        # Canonical balanced profile
        weights = compute_stage_weights(include_bu=True)
        self.x_balanced = np.array([
            weights["w_CS"],
            weights["w_UNA"],
            weights["w_ONA"],
            weights["w_BU"]
        ])
        
        # Session state (keyed by session_id)
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def _get_session_state(self, session_id: Optional[str]) -> Tuple[Dict[str, Any], DisplacementFilter]:
        """
        Get or create session state and filter.

        Args:
            session_id: Session identifier (None for stateless packet).
                        Empty string is normalized to None.

        Returns:
            Tuple of (session_state_dict, filter) where filter is session-scoped
            or fresh for stateless packets.
        """
        # Normalize empty string to None
        if session_id == "":
            session_id = None
        
        if session_id is None:
            # Stateless packet - return empty state and fresh filter
            state = {
                "econ_state": None,
                "emp_state": None,
                "edu_state": None,
                "initialized": False
            }
            filter = DisplacementFilter(mc_samples=self.mc_samples)
            return state, filter

        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "econ_state": None,
                "emp_state": None,
                "edu_state": None,
                "filter": DisplacementFilter(mc_samples=self.mc_samples),
                "initialized": False
            }

        state = self.sessions[session_id]
        filter = state["filter"]
        return state, filter
    
    def _initialize_state(
        self,
        packet: Dict[str, Any],
        session_state: Dict[str, Any]
    ) -> Tuple[EconomyState, EmploymentState, EducationState]:
        """
        Initialize domain states from packet.
        
        Uses A_INIT_DEFAULT (0.12) for initial aperture seeding.
        This is only called at session initialization.
        
        Args:
            packet: Egress packet.
            session_state: Session state dictionary.
        
        Returns:
            (econ_state, emp_state, edu_state)
        """
        # Check if potentials are provided
        if "potentials" in packet:
            pot = packet["potentials"]
            
            # Extract domain potentials
            x_econ = np.array([
                pot["economy"]["Gov"],
                pot["economy"]["Info"],
                pot["economy"]["Infer"],
                pot["economy"]["Int"]
            ])
            
            x_emp = np.array([
                pot["employment"]["GM"],
                pot["employment"]["ICu"],
                pot["employment"]["IInter"],
                pot["employment"]["ICo"]
            ])
            # Normalize employment
            emp_sum = np.sum(x_emp)
            if emp_sum > 0:
                x_emp = x_emp / emp_sum
            else:
                x_emp = np.array([0.25, 0.25, 0.25, 0.25])
            
            x_edu = np.array([
                pot["education"]["GMT"],
                pot["education"]["ICV"],
                pot["education"]["IIA"],
                pot["education"]["ICI"]
            ])
            
            # Construct edge vectors with target aperture A_INIT_DEFAULT (only at initialization)
            y_econ = construct_edge_vector_with_aperture(
                x_econ, self.B, self.W, target_aperture=A_INIT_DEFAULT
            )
            y_emp = construct_edge_vector_with_aperture(
                x_emp, self.B, self.W, target_aperture=A_INIT_DEFAULT
            )
            y_edu = construct_edge_vector_with_aperture(
                x_edu, self.B, self.W, target_aperture=A_INIT_DEFAULT
            )
            
            # Compute apertures for initialized edge vectors
            _, y_cycle_econ = hodge_decomposition(y_econ, self.P_grad, self.P_cycle)
            A_econ = compute_aperture(y_econ, y_cycle_econ, self.W)
            
            _, y_cycle_emp = hodge_decomposition(y_emp, self.P_grad, self.P_cycle)
            A_emp = compute_aperture(y_emp, y_cycle_emp, self.W)
            
            _, y_cycle_edu = hodge_decomposition(y_edu, self.P_grad, self.P_cycle)
            A_edu = compute_aperture(y_edu, y_cycle_edu, self.W)
            
            econ_state = EconomyState(
                x_econ[0], x_econ[1], x_econ[2], x_econ[3],
                y=y_econ, A=A_econ
            )
            
            emp_state = EmploymentState(
                x_emp[0], x_emp[1], x_emp[2], x_emp[3],
                y=y_emp, A=A_emp
            )
            
            edu_state = EducationState(
                x_edu[0], x_edu[1], x_edu[2], x_edu[3],
                y=y_edu, A=A_edu
            )
            
        else:
            # Only displacement_estimate provided - initialize to balanced
            x_balanced = self.x_balanced
            
            # Use A_INIT_DEFAULT for initial aperture (only at initialization)
            y_balanced = construct_edge_vector_with_aperture(
                x_balanced, self.B, self.W, target_aperture=A_INIT_DEFAULT
            )
            
            _, y_cycle = hodge_decomposition(y_balanced, self.P_grad, self.P_cycle)
            A_balanced = compute_aperture(y_balanced, y_cycle, self.W)
            
            econ_state = EconomyState(
                x_balanced[0], x_balanced[1], x_balanced[2], x_balanced[3],
                y=y_balanced, A=A_balanced
            )
            
            emp_state = EmploymentState(
                x_balanced[0], x_balanced[1], x_balanced[2], x_balanced[3],
                y=y_balanced, A=A_balanced
            )
            
            edu_state = EducationState(
                x_balanced[0], x_balanced[1], x_balanced[2], x_balanced[3],
                y=y_balanced, A=A_balanced
            )
        
        return econ_state, emp_state, edu_state
    
    def _predict_step(
        self,
        econ_state: EconomyState,
        emp_state: EmploymentState,
        edu_state: EducationState
    ) -> Tuple[EconomyState, EmploymentState, EducationState]:
        """
        Predict step: advance state by one time step using CGM dynamics.
        
        Args:
            econ_state: Current economy state.
            emp_state: Current employment state.
            edu_state: Current education state.
        
        Returns:
            Predicted states.
        """
        geometry_objects = {
            "B": self.B,
            "W": self.W,
            "P_grad": self.P_grad,
            "P_cycle": self.P_cycle
        }
        
        # Use dynamics.step for predict step
        econ_pred, emp_pred, edu_pred = step(
            econ_state, emp_state, edu_state,
            geometry_objects, self.params
        )
        
        return econ_pred, emp_pred, edu_pred
    
    def _update_step(
        self,
        packet: Dict[str, Any],
        econ_pred: EconomyState,
        emp_pred: EmploymentState,
        edu_pred: EducationState
    ) -> Tuple[EconomyState, EmploymentState, EducationState, Dict[str, float]]:
        """
        Update step: incorporate evidence from packet.
        
        Args:
            packet: Egress packet.
            econ_pred: Predicted economy state.
            emp_pred: Predicted employment state.
            edu_pred: Predicted education state.
        
        Returns:
            (econ_updated, emp_updated, edu_updated, displacement)
        """
        # Compute displacement
        if "potentials" in packet:
            pot = packet["potentials"]
            
            x_econ = np.array([
                pot["economy"]["Gov"],
                pot["economy"]["Info"],
                pot["economy"]["Infer"],
                pot["economy"]["Int"]
            ])
            
            x_emp = np.array([
                pot["employment"]["GM"],
                pot["employment"]["ICu"],
                pot["employment"]["IInter"],
                pot["employment"]["ICo"]
            ])
            emp_sum = np.sum(x_emp)
            if emp_sum > 0:
                x_emp = x_emp / emp_sum
            else:
                x_emp = np.array([0.25, 0.25, 0.25, 0.25])
            
            x_edu = np.array([
                pot["education"]["GMT"],
                pot["education"]["ICV"],
                pot["education"]["IIA"],
                pot["education"]["ICI"]
            ])
            
            # Compute derivative profile
            x_deriv = (x_econ + x_emp + x_edu) / 3.0
            
            # Displacement
            displacement = np.abs(x_deriv - self.x_balanced)
            D = {
                "GTD": float(displacement[0]),
                "IVD": float(displacement[1]),
                "IAD": float(displacement[2]),
                "IID": float(displacement[3])
            }
            
            # Update internal state: overwrite potentials, recompute gradient
            # Keep predicted cycle component
            y_grad_econ = self.B.T @ x_econ
            y_grad_emp = self.B.T @ x_emp
            y_grad_edu = self.B.T @ x_edu
            
            # Get predicted cycle components
            _, y_cycle_econ_pred = hodge_decomposition(
                econ_pred.y, self.P_grad, self.P_cycle
            )
            _, y_cycle_emp_pred = hodge_decomposition(
                emp_pred.y, self.P_grad, self.P_cycle
            )
            _, y_cycle_edu_pred = hodge_decomposition(
                edu_pred.y, self.P_grad, self.P_cycle
            )
            
            # Construct new edge vectors
            y_econ_new = y_grad_econ + y_cycle_econ_pred
            y_emp_new = y_grad_emp + y_cycle_emp_pred
            y_edu_new = y_grad_edu + y_cycle_edu_pred
            
            # Compute apertures for updated edge vectors
            _, y_cycle_econ = hodge_decomposition(y_econ_new, self.P_grad, self.P_cycle)
            A_econ = compute_aperture(y_econ_new, y_cycle_econ, self.W)
            
            _, y_cycle_emp = hodge_decomposition(y_emp_new, self.P_grad, self.P_cycle)
            A_emp = compute_aperture(y_emp_new, y_cycle_emp, self.W)
            
            _, y_cycle_edu = hodge_decomposition(y_edu_new, self.P_grad, self.P_cycle)
            A_edu = compute_aperture(y_edu_new, y_cycle_edu, self.W)
            
            econ_updated = EconomyState(
                x_econ[0], x_econ[1], x_econ[2], x_econ[3],
                y=y_econ_new, A=A_econ
            )
            
            emp_updated = EmploymentState(
                x_emp[0], x_emp[1], x_emp[2], x_emp[3],
                y=y_emp_new, A=A_emp
            )
            
            edu_updated = EducationState(
                x_edu[0], x_edu[1], x_edu[2], x_edu[3],
                y=y_edu_new, A=A_edu
            )
            
        else:
            # Only displacement_estimate provided
            D = packet["displacement_estimate"]
            
            # State evolves by prediction only (no correction)
            econ_updated = econ_pred
            emp_updated = emp_pred
            edu_updated = edu_pred
        
        return econ_updated, emp_updated, edu_updated, D
    
    def _compute_routing(
        self,
        displacement: Dict[str, float],
        stability: float,
        work_category: str
    ) -> Dict[str, Any]:
        """
        Compute routing information.
        
        Args:
            displacement: Displacement components.
            stability: Route stability.
            work_category: Work category (GM, ICu, IInter, ICo).
        
        Returns:
            Routing dictionary.
        """
        # Routing mode
        max_disp = max(displacement.values())
        if max_disp < self.maintenance_threshold:
            mode = "maintenance"
        elif stability < self.min_route_stability:
            mode = "unstable"
        else:
            mode = "active"
        
        # Work indicated description per spec
        work_indicated_map = {
            "GM": "Governance Management work that restores traceability to Original sources",
            "ICu": "Information Curation work that restores variety of Authority types",
            "IInter": "Inference Interaction work that restores accountability termination in Original Agency",
            "ICo": "Intelligence Cooperation work that restores integrity of Authority-Agency alignment"
        }
        work_indicated = work_indicated_map.get(work_category, "")
        
        routing = {
            "mode": mode,
            "route_to": None,
            "low_stability_action": None,
            "work_indicated": None
        }
        
        if mode == "unstable":
            routing["route_to"] = None
            routing["low_stability_action"] = "ICu"
            routing["work_indicated"] = "Measurement improvement recommended due to low route stability"
        elif mode == "active":
            routing["route_to"] = work_category
            routing["work_indicated"] = work_indicated
        elif mode == "maintenance":
            routing["route_to"] = work_category
            routing["work_indicated"] = work_indicated
        
        return routing
    
    def process_egress_packet(
        self,
        packet: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process an egress packet and generate a reading.
        
        Args:
            packet: Egress packet dictionary.
        
        Returns:
            Compass reading dictionary.
        """
        # Validate packet
        validate_and_raise(packet)
        
        session_id = packet.get("session_id")
        session_state, filter = self._get_session_state(session_id)

        # Get measurement noise from config (per spec)
        config = packet.get("config", {})
        noise = config.get("measurement_noise", self.measurement_noise)

        # Initialize state if needed
        if not session_state["initialized"]:
            econ_state, emp_state, edu_state = self._initialize_state(
                packet, session_state
            )
            session_state["econ_state"] = econ_state
            session_state["emp_state"] = emp_state
            session_state["edu_state"] = edu_state
            session_state["initialized"] = True
        else:
            econ_state = session_state["econ_state"]
            emp_state = session_state["emp_state"]
            edu_state = session_state["edu_state"]

        # Predict step
        econ_pred, emp_pred, edu_pred = self._predict_step(
            econ_state, emp_state, edu_state
        )

        # Update step
        econ_updated, emp_updated, edu_updated, displacement = self._update_step(
            packet, econ_pred, emp_pred, edu_pred
        )

        # Update displacement filter with main displacement
        filter.update(displacement, noise)

        # Apply observations in order if provided
        if "observations" in packet:
            filter.update_with_observations(packet["observations"], noise)
        
        # Get posterior means
        D_posterior = filter.get_posterior_means()

        # Get dominant component from posterior
        dominant = filter.get_dominant_component(self.tie_break_order)
        
        # Work category mapping
        work_category_map = {
            "GTD": "GM",
            "IVD": "ICu",
            "IAD": "IInter",
            "IID": "ICo"
        }
        work_category = work_category_map[dominant]

        # Compute route stability
        seed = generate_deterministic_seed(session_id, packet["id"])
        stability, dominant_route = filter.compute_route_stability(
            self.tie_break_order, seed=seed
        )

        # Get credible intervals
        intervals = filter.get_credible_intervals()
        
        # Compute routing
        routing = self._compute_routing(D_posterior, stability, work_category)
        
        # Get SI values from correct domains
        SI_econ = compute_domain_SI(econ_updated.A, A_STAR) if econ_updated.A is not None else 0.0
        SI_emp = compute_domain_SI(emp_updated.A, A_STAR) if emp_updated.A is not None else 0.0
        SI_edu = compute_domain_SI(edu_updated.A, A_STAR) if edu_updated.A is not None else 0.0
        
        # Update session state
        session_state["econ_state"] = econ_updated
        session_state["emp_state"] = emp_updated
        session_state["edu_state"] = edu_updated
        
        # Build displacement dict with dominant inside it
        displacement_out = dict(D_posterior)
        displacement_out["dominant"] = dominant
        
        # Build reading per spec schema
        reading = {
            "id": f"RDG-{packet['id']}",
            "egress_id": packet["id"],
            "timestamp": packet["timestamp"],
            "use_case": packet["use_case"],
            "receiving_point": {
                **packet["receiving_point"],
                "status": "delivered"
            },
            "classification": "[Authority:Derivative] + [Agency:Derivative]",
            "flow": "[Authority:Original] -> [Authority:Derivative] + [Agency:Derivative] -> [Agency:Original]",
            "routing": {
                "mode": routing["mode"],
                "route_to": routing["route_to"],
                "low_stability_action": routing.get("low_stability_action"),
                "work_indicated": routing.get("work_indicated")
            },
            "ledger": {
                "source": "provided" if "displacement_estimate" in packet else "computed",
                "displacement": displacement_out,
                "uncertainty": {
                    "intervals": {
                        comp: [float(intervals[comp][0]), float(intervals[comp][1])]
                        for comp in ["GTD", "IVD", "IAD", "IID"]
                    },
                    "route_stability": float(stability),
                    "samples": self.mc_samples
                },
                "si": {
                    "economy": float(SI_econ),
                    "employment": float(SI_emp),
                    "education": float(SI_edu)
                }
            },
            "patterns": packet.get("patterns", [])
        }
        
        # Add observed field per spec (only when displacement_estimate was provided)
        if "displacement_estimate" in packet:
            reading["ledger"]["observed"] = packet["displacement_estimate"]
        
        # Check employment normalization if potentials provided
        if "potentials" in packet:
            emp_pot = packet["potentials"]["employment"]
            emp_sum = sum(emp_pot.values())
            reading["ledger"]["employment_normalized"] = abs(emp_sum - 1.0) > 1e-6
        
        return reading

