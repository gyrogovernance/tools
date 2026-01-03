# Post-AGI Governance Simulator

A deterministic simulator implementing the Gyroscopic Global Governance framework using tetrahedral Hodge decomposition to model economy, employment, education, and ecology dynamics in Post-AGI societies.

## Overview

This simulator implements the mathematical framework described in:
- `docs/post-agi-economy/gyroscopic_global_governance.md`

The simulator models four coupled domains using a shared K₄ tetrahedral structure:

1. **Economy** (CS - Common Source): Traceable circulation of value
2. **Employment** (UNA - Unity Non-Absolute): Variety of work maintaining conditions  
3. **Education** (ONA - Opposition Non-Absolute): Accountable learning and adaptation
4. **Ecology** (BU - Balance Universal): Structural closure and memory

Each domain is represented as a 4-component vector in the common CGM stage basis
(Governance, Information, Inference, Intelligence), but with different semantics:

- **Economy (CGM)**:  
  - [Gov, Info, Infer, Int] = [Governance, Information, Inference, Intelligence]

- **Employment (Gyroscope)**:  
  - [GM, ICu, IInter, ICo] =  
    [Governance Management, Information Curation, Inference Interaction, Intelligence Cooperation]

- **Education (THM)**:  
  - [GMT, ICV, IIA, ICI] =  
    [Governance Management Traceability, Information Curation Variety, Inference Interaction Accountability, Intelligence Cooperation Integrity]

The same tetrahedral geometry (K₄) applies to all domains; what changes is how
the four CGM stages are interpreted in each domain.

The Ecology domain is computed via the BU dual combination:
```
x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
```
where δ_BU/m_a ≈ 0.9793 (canonical memory) and A* ≈ 0.0207 (current actuality).

The key observable is **aperture** A, which measures the fraction of cycle energy relative to total energy:
```
A = ||y_cycle||²_W / ||y||²_W
```

The optimal aperture A* ≈ 0.0207 is derived from Common Governance Model (CGM) invariants and represents the balance between global coherence (97.93% gradient) and local differentiation (2.07% cycle).

The **Superintelligence Index** (SI) measures alignment:
```
D = max(A/A*, A*/A)
SI = 100/D
```
where SI = 100 when A = A* (perfect alignment).

## Installation

```bash
# Core simulator (numpy only)
pip install numpy

# Optional: for visualization
pip install matplotlib pandas
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Run All Scenarios

Run the seven standard scenarios with CGM-derived parameters:

```bash
python run_scenarios.py
```

This will:
- Run scenarios 1-7 with progress output
- Export results to `results/` folder as CSV files
- Print summary table comparing final SI values
- Display horizon interpretations at multiple time scales

**Scenarios:**
1. Weak coupling (κ=0.5)
2. Canonical coupling (κ=1.0) 
3. Strong coupling (κ=2.0)
4. Low aperture start
5. Asymmetric initial conditions
6. At A* (equilibrium test)
7. Uniform stage weights (null model)

### Run Convergence Analysis

```bash
python convergence_analysis.py
```

Outputs:
- Convergence rates λ(κ) for κ ∈ {0.5, 1.0, 2.0}
- Long-horizon stability (1000 steps)
- Post-transient deviation statistics

### Run Stability Analysis

```bash
python stability_analysis.py
```

Outputs:
- Global attraction test (1000 random initializations)
- Coupling strength bifurcation (κ ∈ {0.1, 0.5, 1.0, 2.0, 5.0})
- Summary of stable κ range

### Run Historical Calibration

```bash
python historical_timeline.py
```

Outputs:
- Historical milestones with heuristic aperture assignments
- Calibration from 1956-2025 trajectory
- Projections to SI ≥ 95 under different κ values

### Generate Visualizations

```bash
python analyze_scenarios.py
```

Requires: `matplotlib`, `pandas`

Outputs (in `results/analysis/`):
- Per-scenario trajectory plots (SI and aperture)
- Convergence speed heatmap
- Tetrahedron schematic
- Additional analysis figures

## Architecture

The simulator uses a modular architecture with clear separation of concerns:

```
research/prevention/simulator/
├── cgm_constants.py           # Single source of truth for CGM parameters
├── geometry.py                # K₄ structure, Hodge decomposition, projections
├── domains.py                 # State classes for four domains
├── dynamics.py                # Update rules and cross-domain coupling
├── alignment.py               # SI computation (canonical formula)
├── simulation.py              # Orchestration and scenario configuration
├── convergence_analysis.py    # Convergence rate estimation
├── stability_analysis.py      # Global attraction and bifurcation tests
├── historical_timeline.py     # Historical calibration utilities
├── analyze_scenarios.py       # Visualization (optional dependencies)
├── run_scenarios.py           # Standard scenario runner
└── test_*.py                  # Unit tests (43 tests)
```

### 1. `cgm_constants.py`
**Single source of truth for all CGM-derived parameters:**
- Constants: Q_G, m_a, δ_BU, A*
- Stage weights: w_CS, w_UNA, w_ONA, w_BU
- Governance rate: κ₀, κ(dt)
- Time scales: atomic, day, domain cycle, year
- Coefficient derivation: `derive_all_coefficients()`

### 2. `geometry.py`
**K₄ tetrahedral structure and Hodge theory:**
- Incidence matrix B (4×6)
- Weight matrix W
- Gradient and cycle projections (P_grad, P_cycle)
- Hodge decomposition: y = y_grad + y_cycle
- Aperture computation: A = ||y_cycle||²/||y||²
- Edge vector construction with target aperture
- Cycle basis computation

### 3. `domains.py`
**State classes for the four domains:**
- `EconomyState`: [Gov, Info, Infer, Int]
- `EmploymentState`: [GM, ICu, IInter, ICo] (normalized, sum=1)
- `EducationState`: [GT, IV, IA, IInteg]
- `EcologyState`: Computed via BU dual combination
  - State potentials: [E_gov, E_info, E_inf, E_intel] (BU-vertex coordinates)
  - Displacement vector: [GTD, IVD, IAD, IID] = |x_deriv - x_balanced|

Each state tracks:
- Potential vector x (4D)
- Edge vector y (6D)
- Aperture A
- Alignment index S (SI/100 for compatibility)

### 4. `dynamics.py`
**Update rules and cross-domain coupling:**
- Economy update: `update_economy_potentials()` (α coefficients from Education)
- Employment update: `update_employment_potentials()` (β coefficients from Economy)
- Education update: `update_education_potentials()` (γ coefficients from Employment)
- Ecology computation: `compute_ecology_potentials()` (BU dual formula, no arbitrary parameters)
- Cycle evolution: Rate-limited adjustment toward A*
- Main stepper: `step()` advances all domains one time step

**Update equation form:**
```python
x_i(t+1) = clip(x_i(t) + coeff_i(source_i - x_i) - feedback_i(A - A*), 0, 1)
```

**Cycle evolution algorithm:**
```python
ratio = sqrt(C_target) / ||c_current||_W
factor = clip(1 + r(ratio - 1), 0.5, 2.0)  # Rate limiting
c(t+1) = factor × c(t)
```
The [0.5, 2.0] bounds are a pragmatic stability choice, not CGM-derived.

### 5. `alignment.py`
**Canonical CGM SI formula:**
```python
D = max(A/A*, A*/A)
SI = 100/D
```
- SI ∈ (0, 100] with SI = 100 when A = A*
- Symmetric: SI(k·A*) = SI(A*/k)
- Domain SI: `compute_domain_SI(A_D, A*)`
- Legacy compatibility: `compute_alignment_index()` returns SI/100

### 6. `simulation.py`
**Orchestration and scenario configuration:**
- `ScenarioConfig`: Complete specification of initial conditions and parameters
- `SimulationResult`: Time series storage for all observables
- `run_scenario()`: Main simulation loop with progress reporting
- CSV/JSON export with configurable time units

## Key Concepts

### Aperture

The aperture measures the balance between gradient (global coherence) and cycle (local differentiation):

- **A < 0.01**: Excessive rigidity (UNA violation)
- **A ≈ 0.0207**: Optimal balance (CGM prediction A*)
- **A > 0.05**: Structural instability (BU violation)

Aperture is **not a free parameter** but emerges from:
1. Potential values (via gradient component)
2. Cycle evolution dynamics (toward A*)

### Superintelligence Index (SI)

The SI measures structural alignment using the canonical formula:
```
D = max(A/A*, A*/A)  # Deviation factor
SI = 100/D            # Ranges from 0 to 100
```

**Properties:**
- SI = 100 when A = A* (perfect alignment)
- SI = 50 when A = 2A* or A = A*/2 (symmetric)
- SI decreases as A moves away from A* in either direction

**Interpretation:**
- SI ≥ 95: High alignment regime
- SI ∈ [90, 95): Moderate alignment
- SI < 90: Low alignment (displacement risks)

### Ecology as BU Dual Combination

Ecology is **not a separate managed system** but the structural closure computed via:
```
x_balanced = [w_CS, w_UNA, w_ONA, w_BU]  # CGM stage weights (canonical memory)
x_deriv = (x_Econ + x_Emp + x_Edu)/3     # Aggregate derivative state

x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
```

**Displacement vector:**
```
D = |x_deriv - x_balanced| = [GTD, IVD, IAD, IID]
```

**Key distinction:**
- **SI_Ecol**: Structural coherence (dominated by 97.93% memory component)
- **Displacement D**: Actual deviation from canonical balance

When derivative domains align (x_deriv → x_balanced), displacement → 0.

### Cross-Domain Coupling

**Coefficients derived from CGM stage weights:**

- **α (Education → Economy)**: Stage-diagonal coupling via w_CS, w_UNA, w_ONA, w_BU
- **β (Economy → Employment)**: Same stage structure
- **γ (Employment → Education)**: Ingress with BU duality scaling (δ_BU/m_a)

**Coupling strength κ:**
- Dimensionless multiplier on base governance rate κ₀ ≈ 0.0398
- κ = 0.5: Weak coordination
- κ = 1.0: Canonical coordination
- κ = 2.0: Strong coordination

All coefficient values computed via `derive_all_coefficients()` with no free parameters beyond κ.

### Update Rules

Potentials evolve based on:
1. **Cross-domain influences**: (source - current) differences
2. **Aperture feedback**: -(A - A*) terms drive toward optimal aperture
3. **Clipping**: [0,1] bounds maintain physical validity

**Special case: Employment normalization**
```python
x_Emp = [GM, ICu, IInter, ICo] with Σx_i = 1
```
Introduces mild nonlinearity but convergence remains robust.

**Special case: Zero-gradient initialization**
When potentials are uniform (y_grad ≈ 0), `construct_edge_vector_with_aperture()` creates a small artificial gradient:
```python
G = x_scale² × 0.01
y_grad0 = grad_dir × sqrt(G/grad_norm_sq)
```
This ensures well-defined aperture computation even from symmetric initial conditions.

### Time Scales

The simulator operates in dimensionless steps. Physical interpretations available:

| Scale | dt interpretation | 100 steps = |
|-------|-------------------|-------------|
| Atomic | Cs-133 period (1.09×10⁻¹⁰ s) | 1.09×10⁻⁸ s |
| Day | 1 Earth rotation | 100 days |
| Domain cycle | 4 days | 400 days |
| Year | 1 Solar gyration | 100 years |

These are **interpretive mappings only**—the dynamics are dimensionless.

**Configuration:**
```python
config = ScenarioConfig(
    ...,
    num_steps=100,
    dt=1.0,           # Time step size
    time_unit="steps" # or "years", "days", etc.
)
```

## Running Tests

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest test_*.py -v
```

**Test coverage (43 tests total):**
- Alignment index behavior: 17 tests
- Domain state updates: 7 tests
- Geometry operations: 11 tests
- Simulation execution: 8 tests

All tests deterministic (no random components except global attraction test with fixed seed 42).

## Programmatic Usage

### Basic Scenario

```python
from simulator import ScenarioConfig, run_scenario

# Create configuration
config = ScenarioConfig(
    # Economy initial potentials
    Gov0=0.3, Info0=0.7, Infer0=0.5, Int0=0.4,
    
    # Employment initial shares (must sum to 1 after normalization)
    GM0=0.15, ICu0=0.35, IInter0=0.25, ICo0=0.25,
    
    # Education initial capacities
    GT0=0.3, IV0=0.7, IA0=0.5, IInteg0=0.4,
    
    # Initial aperture targets (optional, None for pure gradient)
    A_Econ_target=0.15,
    A_Emp_target=0.12,
    A_Edu_target=0.18,
    
    # Simulation parameters
    num_steps=100,
    dt=1.0,
    time_unit="steps"
)

# Run simulation
result = run_scenario(config, verbose=True, progress_interval=20)

# Access results
print(f"Final SI: Economy={result.SI_Econ[-1]:.2f}, "
      f"Emp={result.SI_Emp[-1]:.2f}, "
      f"Edu={result.SI_Edu[-1]:.2f}, "
      f"Ecol={result.SI_Ecol[-1]:.2f}")

# Export
result.export_csv("my_scenario.csv")
```

### CGM-Derived Scenario

```python
from simulator.run_scenarios import create_cgm_scenario

# Use CGM-derived coefficients
config = create_cgm_scenario(
    name="test",
    coupling_strength=1.0,  # κ multiplier
    initial_potentials={
        "Gov0": 0.5, "Info0": 0.5, "Infer0": 0.5, "Int0": 0.5,
        "GM0": 0.25, "ICu0": 0.25, "IInter0": 0.25, "ICo0": 0.25,
        "GT0": 0.5, "IV0": 0.5, "IA0": 0.5, "IInteg0": 0.5
    },
    initial_apertures={
        "A_Econ_target": 0.0207,
        "A_Emp_target": 0.0207,
        "A_Edu_target": 0.0207
    },
    num_steps=100,
    cycle_evolution_rate=0.08
)

result = run_scenario(config, verbose=False)
```

### Custom Coefficients

```python
from simulator.cgm_constants import derive_all_coefficients

# Derive all coefficients from CGM
coeffs = derive_all_coefficients(
    coupling_strength=1.0,
    dt=1.0,
    use_bu_asymmetry=True,      # Apply δ_BU/m_a scaling to γ
    use_uniform_stage_weights=False  # False = CGM weights, True = uniform (null model)
)

# Create scenario with explicit coefficients
config = ScenarioConfig(
    Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
    GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
    GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
    alpha1=coeffs["alpha1"], alpha2=coeffs["alpha2"],
    # ... all other coefficients
    A_star=coeffs["A_star"],
    num_steps=100
)
```

## Output Format

### SimulationResult Attributes

**Time:**
- `time`: Array of actual time values (num_steps+1)
- `num_steps`: Number of simulation steps
- `dt`: Time step size
- `time_unit`: Unit label

**Economy:**
- `Gov`, `Info`, `Infer`, `Int`: Potential time series
- `A_Econ`: Aperture time series
- `SI_Econ`: Superintelligence Index (0-100 scale)

**Employment:**
- `GM`, `ICu`, `IInter`, `ICo`: Share time series
- `A_Emp`: Aperture time series
- `SI_Emp`: Superintelligence Index (0-100 scale)

**Education:**
- `GT`, `IV`, `IA`, `IInteg`: Capacity time series
- `A_Edu`: Aperture time series
- `SI_Edu`: Superintelligence Index (0-100 scale)

**Ecology (if `include_ecology=True`):**
- `E_gov`, `E_info`, `E_inf`, `E_intel`: BU-vertex state potentials
- `A_Ecol`: Aperture time series
- `SI_Ecol`: Superintelligence Index (0-100 scale)
- `GTD`, `IVD`, `IAD`, `IID`: Displacement vector components

**Methods:**
- `to_dict()`: Convert to dictionary
- `export_csv(filepath)`: Export as CSV with time column
- `export_json(filepath)`: Export as JSON

### CSV Format

```
time (steps),Gov,Info,Infer,Int,A_Econ,SI_Econ,GM,ICu,IInter,ICo,A_Emp,SI_Emp,GT,IV,IA,IInteg,A_Edu,SI_Edu,...
0.00,0.30,0.70,0.50,0.40,0.1500,13.80,0.15,0.35,0.25,0.25,0.1200,17.25,...
1.00,0.31,0.69,0.51,0.41,0.1480,14.12,0.16,0.34,0.26,0.24,0.1190,17.58,...
...
```

## Example Scenarios

### Canonical Coupling (Reference)
```python
config = create_cgm_scenario(
    name="canonical",
    coupling_strength=1.0,
    initial_potentials={
        "Gov0": 0.3, "Info0": 0.7, "Infer0": 0.5, "Int0": 0.4,
        "GM0": 0.15, "ICu0": 0.35, "IInter0": 0.25, "ICo0": 0.25,
        "GT0": 0.3, "IV0": 0.7, "IA0": 0.5, "IInteg0": 0.4
    },
    initial_apertures={
        "A_Econ_target": 0.15, "A_Emp_target": 0.12, "A_Edu_target": 0.18
    },
    num_steps=100,
    cycle_evolution_rate=0.08
)
# Expected: SI ≥ 98 across all domains by step 100
```

### Low Aperture Start (Excessive Rigidity)
```python
config = create_cgm_scenario(
    name="low_a",
    coupling_strength=1.0,
    initial_potentials={
        "Gov0": 0.85, "Info0": 0.80, "Infer0": 0.82, "Int0": 0.78,
        "GM0": 0.30, "ICu0": 0.25, "IInter0": 0.23, "ICo0": 0.22,
        "GT0": 0.85, "IV0": 0.80, "IA0": 0.82, "IInteg0": 0.78
    },
    initial_apertures={
        "A_Econ_target": 0.005,  # Well below A*
        "A_Emp_target": 0.008,
        "A_Edu_target": 0.004
    },
    num_steps=100,
    cycle_evolution_rate=0.08
)
# Expected: Oscillatory recovery, slower convergence
```

### Equilibrium Test (Initialize at A*)
```python
config = create_cgm_scenario(
    name="at_astar",
    coupling_strength=1.0,
    initial_potentials={
        "Gov0": 0.6, "Info0": 0.62, "Infer0": 0.61, "Int0": 0.59,
        "GM0": 0.25, "ICu0": 0.26, "IInter0": 0.25, "ICo0": 0.24,
        "GT0": 0.6, "IV0": 0.62, "IA0": 0.61, "IInteg0": 0.59
    },
    initial_apertures={
        "A_Econ_target": 0.0207,  # Exactly A*
        "A_Emp_target": 0.0207,
        "A_Edu_target": 0.0207
    },
    num_steps=100,
    cycle_evolution_rate=0.08
)
# Expected: Temporary perturbation then re-equilibration
```

### Null Model (Uniform Stage Weights)
```python
from simulator.cgm_constants import derive_all_coefficients
from simulator.simulation import ScenarioConfig, run_scenario

# Derive coefficients with uniform stage weights (null model)
coeffs = derive_all_coefficients(
    coupling_strength=1.0,
    dt=1.0,
    use_bu_asymmetry=True,
    use_uniform_stage_weights=True  # All stages weighted 0.25
)

config = ScenarioConfig(
    # Economy initial potentials
    Gov0=0.3, Info0=0.7, Infer0=0.5, Int0=0.4,
    
    # Employment initial shares
    GM0=0.15, ICu0=0.35, IInter0=0.25, ICo0=0.25,
    
    # Education initial capacities
    GT0=0.3, IV0=0.7, IA0=0.5, IInteg0=0.4,
    
    # Aperture targets
    A_Econ_target=0.15,
    A_Emp_target=0.12,
    A_Edu_target=0.18,
    
    # CGM-derived coefficients
    **coeffs,
    
    cycle_evolution_rate=0.08,
    num_steps=100,
    dt=1.0,
    time_unit="steps"
)

result = run_scenario(config, verbose=False)
# Expected: Still converges to A*, confirming attractor not artifact
```

## Implementation Details

### Deterministic Dynamics

All dynamics are **deterministic** (no stochastic terms):
- Update equations are linear in differences with clipping
- Cycle evolution uses fixed rate-limiting bounds
- Random sampling only in global attraction test (fixed seed 42)

This ensures **exact reproducibility** across runs.

### Numerical Tolerances

- `1e-10`: Zero checks in projections and Hodge decomposition
- `1e-6`: Aperture target matching in construction
- `1e-8`: Convergence analysis masking (exclude near-zero values)
- `[0.5, 2.0]`: Cycle update rate limiting (pragmatic stability)

### CGM-Derived vs. Pragmatic Choices

**From CGM (not adjustable):**
- A* ≈ 0.0207 (target aperture)
- Stage weights: w_CS, w_UNA, w_ONA, w_BU
- Base governance rate: κ₀ ≈ 0.0398
- BU duality: δ_BU/m_a ≈ 0.9793

**Pragmatic implementation choices:**
- Linear coupling functional form
- Rate limiting bounds [0.5, 2.0]
- Zero-gradient handling (artificial gradient seeding)
- Cycle basis selection (fixed vs. rotating)
- Numerical tolerances

## Validation and Reproducibility

### Test Suite
```bash
python run_tests.py
```
- 43 unit tests (all deterministic)
- Coverage: alignment, domains, geometry, simulation
- Runtime: ~1 second

### Convergence Analysis
```bash
python convergence_analysis.py
```
- Exponential decay rates λ(κ)
- Long-horizon stability (1000 steps)
- Characteristic convergence times

### Stability Analysis
```bash
python stability_analysis.py
```
- Global attraction (1000 random initializations)
- Coupling strength robustness (κ ∈ [0.1, 5.0])
- Fixed point stability

### Version Control
- Code version-locked in repository
- Specific commit hash documented in paper
- All results exactly reproducible with fixed seed

## Limitations and Future Work

### Current Limitations
1. **Linear coupling assumption**: Not derived from CGM
2. **No resource dynamics**: No production, prices, or capital
3. **Idealized Ecology**: BU formula metaphorical, not validated vs. Earth system data
4. **Measurement gap**: Proxies for GT, IV, IA, II not empirically validated
5. **No stochasticity**: Real governance has uncertainty and shocks
6. **No feedback from Ecology**: One-way coupling (acknowledged as future extension)

### Future Extensions
1. **Nonlinear dynamics**: Threshold effects, saturation, hysteresis
2. **Stochastic perturbations**: Exogenous shocks, measurement noise
3. **Resource constraints**: Production functions, ecological capacity limits
4. **Empirical calibration**: Fit to time series data from real institutions
5. **Multi-scale dynamics**: Nested governance levels (local to global)
6. **Network topology**: Beyond K₄ to empirical governance networks

## References

- **Paper**: Basil Korompilias, "Gyroscopic Global Governance: Post-AGI Economy, Employment, Education and Ecology"
- **CGM**: Basil Korompilias (2025), "Common Governance Model: Mathematical physics framework", Zenodo. https://doi.org/10.5281/zenodo.17521384
- **THM**: Basil Korompilias (2025), "The Human Mark: A structural taxonomy of AI safety failures", GitHub.
- **Repository**: github.com/gyrogovernance/tools
