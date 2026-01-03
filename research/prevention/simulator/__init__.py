"""
Post-AGI-ASI Governance Simulator

A simulator for Gyroscopic Global Governance using tetrahedral Hodge decomposition
to model economy, employment, education, and ecology in post-AGI societies.

Implements the Common Governance Model (CGM) with four CGM elements
(Governance, Information, Inference, Intelligence) organized within the
Gyroscopic Global Governance (GGG) framework:

CGM Stages map to domains:
- CS  → Governance     | w_CS ≈ 0.51
  - Economy: Governance (Gov)
  - Employment: Governance Management (GM)
  - Education: Governance Management Traceability (GMT)
- UNA → Information    | w_UNA ≈ 0.23
  - Economy: Information (Info)
  - Employment: Information Curation (ICu)
  - Education: Information Curation Variety (ICV)
- ONA → Inference      | w_ONA ≈ 0.26
  - Economy: Inference (Infer)
  - Employment: Inference Interaction (IInter)
  - Education: Inference Interaction Accountability (IIA)
- BU  → Intelligence   | w_BU ≈ 0.01
  - Economy: Intelligence (Int)
  - Employment: Intelligence Cooperation (ICo)
  - Education: Intelligence Cooperation Integrity (ICI)

Ecology (CGM–Gyroscope–THM) aggregates all three derivative domains:
- E_gov: aggregates (Gov + GM + GMT) → yields GTD as displacement
- E_info: aggregates (Info + ICu + ICV) → yields IVD as displacement
- E_inf: aggregates (Infer + IInter + IIA) → yields IAD as displacement
- E_intel: aggregates (Int + ICo + ICI) → yields IID as displacement

Four domains form a higher-level tetrahedron (meta-K₄):
- V₁: Economy (CGM) - responds to Education (closed loop: Education → Economy → Employment → Education)
- V₂: Employment (Gyroscope) - responds to Economy
- V₃: Education (THM) - responds to Employment
- V₄: Ecology (CGM–Gyroscope–THM) - BU dual combination of all three derivative domains

Ecology is computed via BU dual combination (NO arbitrary parameters):
    x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv

Where δ_BU/m_a ≈ 0.9793 (Ingress memory) and A* ≈ 0.0207 (Egress actuality).

Each domain has its own SI computed from aperture:
    SI_D = 100 / max(A_D/A*, A*/A_D)

Time scales for physical interpretation of dt:
- Atomic cycle (Caesium-133 hyperfine transition)
- Day (1 Earth rotation)
- Domain cycle (4 days, 1 per domain)
- Year (1 Solar gyration)

Modules:
    - cgm_constants: CGM invariants, stage weights, time scales, derived coefficients
    - geometry: K4 tetrahedral structure and Hodge decomposition
    - domains: State classes for Economy, Employment, Education, and Ecology
    - alignment: Superintelligence Index (SI) computation per domain
    - dynamics: CGM stage-structured update rules
    - simulation: Scenario configuration and simulation runner
"""

from .cgm_constants import (
    # Fundamental constants
    A_STAR, M_A_EXACT, DELTA_BU, Q_G,
    S_P, U_P, O_P,
    # Stage weights
    W_CS, W_UNA, W_ONA, W_BU,
    # Dimensionless actions
    S_CS, S_UNA, S_ONA, S_BU,
    # Governance rate
    KAPPA_0, BU_DUALITY_RATIO,
    # Time scales
    TIME_SCALES, SECONDS_PER_DAY, SECONDS_PER_YEAR,
    get_time_scale_factor, steps_to_physical_time,
    # Functions
    derive_all_coefficients,
    compute_governance_rate,
    compute_stage_weights
)

from .geometry import (
    get_incidence_matrix,
    get_weight_matrix,
    compute_projections,
    hodge_decomposition,
    compute_aperture,
    construct_edge_vector_with_aperture
)

from .domains import (
    DomainStateBase,
    EconomyState,
    EmploymentState,
    EducationState,
    EcologyState
)

from .alignment import (
    extract_alignment_metrics,
    compute_alignment_index,
    compute_global_alignment_index,
    compute_superintelligence_index,
    compute_domain_SI
)

from .dynamics import (
    update_economy_potentials,
    update_employment_potentials,
    update_education_potentials,
    compute_ecology_potentials,
    step,
    get_default_params
)

from .simulation import (
    ScenarioConfig,
    SimulationResult,
    run_scenario
)

from .lyapunov import (
    precompute_cgm_lyapunov_constants,
    compute_total_lyapunov
)

__version__ = "0.6.0"  # Removed global SI, domain SIs only

__all__ = [
    # CGM Constants
    "A_STAR", "M_A_EXACT", "DELTA_BU", "Q_G",
    "S_P", "U_P", "O_P",
    "W_CS", "W_UNA", "W_ONA", "W_BU",
    "S_CS", "S_UNA", "S_ONA", "S_BU",
    "KAPPA_0", "BU_DUALITY_RATIO",
    "TIME_SCALES", "SECONDS_PER_DAY", "SECONDS_PER_YEAR",
    "get_time_scale_factor", "steps_to_physical_time",
    "derive_all_coefficients",
    "compute_governance_rate",
    "compute_stage_weights",
    # Geometry
    "get_incidence_matrix",
    "get_weight_matrix",
    "compute_projections",
    "hodge_decomposition",
    "compute_aperture",
    "construct_edge_vector_with_aperture",
    # Domains
    "DomainStateBase",
    "EconomyState",
    "EmploymentState",
    "EducationState",
    "EcologyState",
    # Alignment
    "extract_alignment_metrics",
    "compute_alignment_index",
    "compute_global_alignment_index",
    "compute_superintelligence_index",
    "compute_domain_SI",
    # Dynamics
    "update_economy_potentials",
    "update_employment_potentials",
    "update_education_potentials",
    "compute_ecology_potentials",
    "step",
    "get_default_params",
    # Simulation
    "ScenarioConfig",
    "SimulationResult",
    "run_scenario",
    # Lyapunov
    "precompute_cgm_lyapunov_constants",
    "compute_total_lyapunov"
]

