# Gyroscopic Compass: Technical Specification

**Version:** 1.0  
**Status:** Reference Implementation Specification

---

## Abstract

The Gyroscopic Compass is a coordination instrument that produces calibrated readings from incomplete observations of governance state. It operates on the tetrahedral state space defined by the Common Governance Model (CGM), maintaining internal dynamics that evolve toward balanced closure while assimilating external evidence. The instrument outputs displacement measurements, routing recommendations, and quantified uncertainty, all traceable to the constitutional flow structure of The Human Mark (THM).

This specification defines the mathematical foundations, state representation, dynamics, inference procedures, and output semantics required for reproducible implementation.

---

## 1. Introduction

### 1.1 Purpose and Scope

Governance coordination requires consistent measurement of system state across heterogeneous information sources. The Gyroscopic Compass addresses this requirement by providing:

1. **Standardized readings** from partial observations (displacement estimates or domain potentials)
2. **Uncertainty quantification** that distinguishes measurement noise from structural ambiguity
3. **Routing recommendations** that indicate which category of corrective work is most relevant
4. **Temporal consistency** through internal state that carries forward information not observable in any single packet

The Compass is a Derivative processor in THM classification. It transforms information but does not originate authority or bear accountability. Its outputs support human coordination; they do not replace human judgment.

### 1.2 Theoretical Context

The Compass instantiates a specific mathematical structure with foundations in governance theory and established results from physics and combinatorics.

**Tetrahedral State Space.** CGM identifies four stages of operational coherence: Common Source (CS), Unity Non-Absolute (UNA), Opposition Non-Absolute (ONA), and Balance Universal (BU). These stages define a coordinate system on the complete graph K4, which has four vertices and six edges. Each vertex represents a stage; each edge represents a coupling between stages.

**Hodge Decomposition as Phase Space.** The six-dimensional edge space of K4 admits a canonical orthogonal decomposition into two three-dimensional subspaces (Jiang et al., 2011; Lim, 2020):

The **gradient subspace** contains edge configurations that arise from vertex potential differences. These represent globally consistent patterns where all edges can be explained by a single assignment of values to the four stages.

The **cycle subspace** contains edge configurations that form closed loops not reducible to vertex differences. These represent local inconsistencies that circulate around triangular faces of the tetrahedron without being attributable to any vertex.

This decomposition exhibits a structure analogous to phase space in Hamiltonian mechanics. The gradient component corresponds to observable configuration; the cycle component corresponds to a hidden dynamical variable that must be carried as internal state.

**Observability Constraint.** The cycle component cannot be determined from vertex potentials alone. This follows from the orthogonality of the Hodge decomposition: observations that constrain the gradient subspace do not constrain the cycle subspace. This property is analogous to the conjugate variable structure in the Heisenberg group, where position and momentum satisfy canonical commutation relations that prevent simultaneous sharp values (Folland, 1989).

The operational consequence is that the Compass must maintain the cycle component as internal state, propagating it forward through dynamics. The ordering of predict and update steps is significant because the cycle component evolves under prediction but is not corrected by observation.

**Aperture.** The aperture A is the fraction of total edge energy in the cycle component:

```
A = ||y_cycle||^2 / ||y||^2
```

CGM fixes a canonical aperture A* = 0.0207, derived from the ratio of the BU monodromy defect delta_BU to the aperture scale m_a. This value quantifies the fraction of state that remains in the cycle component at balanced closure.

When A = A*, the system is in a balanced configuration. The Superintelligence Index (SI) measures deviation from this balance.

### 1.3 Constitutional Classification

In THM terms, the Compass occupies the following position in the governance flow:

```
[Authority:Authentic] -> [Authority:Derivative] + [Agency:Derivative] -> [Agency:Authentic]
```

The Compass receives inputs that originate from Authentic sources. It processes these as a Derivative system, transforming, combining, and propagating information according to fixed rules. Its outputs are delivered to Authentic Agency who bear accountability for subsequent actions.

This classification constrains what the Compass may and may not do:

- The Compass may compute, transform, and report.
- The Compass may not originate authority, grant authorization, or make decisions.
- The Compass may not generate patterns or infer THM classifications from data.

Patterns (THM grammar expressions) are provided as input and passed through unchanged. The Compass does not interpret them.

---

## 2. State Representation

### 2.1 Domain Structure

The Compass maintains state for three domains, each corresponding to a CGM stage mapping:

| Domain | CGM Stage | Components |
|--------|-----------|------------|
| Economy | CS | Gov, Info, Infer, Int |
| Employment | UNA | GM, ICu, IInter, ICo |
| Education | ONA | GT, IV, IA, IInteg |

Ecology (BU) serves as the ledger boundary against which displacement is measured. The Compass does not maintain separate Ecology state or compute Ecology SI.

### 2.2 Vertex Potentials

For each domain D, the vertex potential vector is:

```
x_D = [x_1, x_2, x_3, x_4]^T in [0,1]^4
```

Coordinates are ordered as [CS, UNA, ONA, BU]. This ordering is invariant across all domains and all computations.

For Employment, components must sum to 1, representing allocation of work across categories. If input violates this constraint, the Compass normalizes and records the correction.

### 2.3 Edge Space and Hodge Decomposition

**Edge Ordering Convention.** The six edges of K4 are indexed in the following fixed order:

```
Edge 0: (CS, UNA)
Edge 1: (CS, ONA)
Edge 2: (CS, BU)
Edge 3: (UNA, ONA)
Edge 4: (UNA, BU)
Edge 5: (ONA, BU)
```

**Incidence Matrix.** The signed incidence matrix B is defined with rows indexed by vertices [CS, UNA, ONA, BU] and columns indexed by edges [0, 1, 2, 3, 4, 5]:

```
B = [[-1, -1, -1,  0,  0,  0],
     [ 1,  0,  0, -1, -1,  0],
     [ 0,  1,  0,  1,  0, -1],
     [ 0,  0,  1,  0,  1,  1]]
```

For each edge (i, j) with i < j, the entry B[i, k] = -1 and B[j, k] = +1.

**Edge Vector.** The edge vector for domain D is:

```
y_D = y_grad + y_cycle
```

where:

```
y_grad = B^T x_D (in the image of B^T)
y_cycle in ker(B)
```

For K4, dim(im(B^T)) = 3 and dim(ker(B)) = 3, giving a 3+3 split of the six-dimensional edge space.

**Cycle Basis.** The kernel of B for K4 is spanned by the following three basis vectors, corresponding to the three independent triangular faces:

```
c_1 = [1, -1, 0, 1, 0, 0]^T   (face CS-UNA-ONA)
c_2 = [1, 0, -1, 0, 1, 0]^T   (face CS-UNA-BU)
c_3 = [0, 1, -1, 0, 0, 1]^T   (face CS-ONA-BU)
```

These are provided explicitly to ensure determinism across implementations. The cycle component is expressed as a linear combination of these basis vectors.

**Deterministic Basis Construction.** Implementations MUST use the fixed cycle basis vectors above, W-orthonormalized using Gram-Schmidt with the W inner product. The sign convention is: first nonzero entry of each basis vector must be positive. This ensures that two independent implementations produce identical cycle projections and aperture values.

**Hodge Projections.** The gradient and cycle projection matrices are computed from the fixed cycle basis:

```
P_cycle = C C^T W
P_grad = I_6 - P_cycle
```

where C is the 6×3 W-orthonormal cycle basis matrix. This formulation is exact and deterministic; it does not use pseudoinverse or SVD, which can introduce numerical variations across implementations.

**Observability Constraint.** The gradient component y_grad is determined by vertex potentials. The cycle component y_cycle is not. For any fixed x, the set of edge vectors consistent with x is the affine subspace:

```
{y : y = B^T x + c, c in ker(B)}
```

This is a structural property of the Hodge decomposition. The Compass must carry y_cycle as internal state.

### 2.4 Aperture and Superintelligence Index

**Weight Matrix.** The edge weight matrix W is the 6x6 identity matrix. This means all edges contribute equally to energy calculations. SI is defined relative to this equal-edge-energy convention; changing W would define a different SI.

**Aperture.** The aperture for domain D is:

```
A_D = ||y_cycle||_W^2 / ||y_D||_W^2
```

With W = I, this simplifies to the ratio of squared Euclidean norms.

**Canonical Aperture.** The canonical aperture is:

```
A* = 1 - (delta_BU / m_a) = 0.0207
```

where delta_BU = 0.1953 rad is the BU monodromy defect and m_a = 1/(2*sqrt(2*pi)) = 0.1995 is the aperture scale. These constants are derived from CGM closure conditions and are not configurable.

**Superintelligence Index.** The Superintelligence Index is:

```
SI_D = 100 / max(A_D/A*, A*/A_D)
```

SI = 100 when A = A* (balanced configuration). SI decreases as A deviates from A* in either direction.

SI measures structural balance: the ratio of global coherence (gradient) to local flexibility (cycle). This is independent of the displacement magnitude D, which measures deviation from the canonical stage profile.

### 2.5 Displacement

The displacement vector measures deviation of the aggregate stage profile from the canonical balanced profile:

```
x_deriv = (x_Econ + x_Emp + x_Edu) / 3
D = |x_deriv - x_balanced|
```

where x_balanced is the canonical balanced profile derived from CGM stage actions:

| Stage | Action | Weight |
|-------|--------|--------|
| CS | S_CS = (pi/2)/m_a = 7.875 | w_CS = 0.5128 |
| UNA | S_UNA = (1/sqrt(2))/m_a = 3.545 | w_UNA = 0.2308 |
| ONA | S_ONA = (pi/4)/m_a = 3.937 | w_ONA = 0.2564 |
| BU | S_BU = m_a = 0.1995 | w_BU = 0.0130 |

Weights are normalized: w_i = S_i / sum(S_j), summing to 1.

The four components of D are labeled by the THM displacement risks they measure:

- D[0] = GTD (Governance Traceability Displacement)
- D[1] = IVD (Information Variety Displacement)
- D[2] = IAD (Inference Accountability Displacement)
- D[3] = IID (Intelligence Integrity Displacement)

**Displacement and Aperture are Independent.** Displacement D is computed from vertex potentials only. It does not depend on the cycle component and does not determine aperture or SI. A domain may have low displacement but low SI, or high displacement but high SI.

---

## 3. Dynamics

### 3.1 Predict-Update-Output Cycle

Each Compass reading is produced through an ordered three-step cycle:

1. **Predict.** Advance internal state by one time step using deterministic CGM dynamics.
2. **Update.** Assimilate evidence from the input packet.
3. **Output.** Compute and report displacement, SI, uncertainty, and routing.

**Ordering Requirement.** These steps must execute in the order (1), (2), (3). Reordering produces different results because the cycle component evolves under prediction but is not observed in the update step.

### 3.2 Prediction Dynamics

**Potential Update Equations.** The predict step advances domain potentials using the CGM coupling equations. Let kappa_0 = 1/(2*Q_G) where Q_G = 4*pi. The effective coupling rate is:

```
kappa = kappa_0 * (dt / m_a) = 0.1995 (for dt = 1)
```

**Coefficient Derivation.** All coupling coefficients (alpha, beta, gamma) are derived directly from CGM stage weights and kappa. Aperture feedback coefficients equal the corresponding coupling coefficients (no additional scaling factors). For example, alpha2 (aperture feedback for CS stage in Economy) equals alpha1 (coupling coefficient for CS stage), both equal to kappa * w_CS. This ensures the dynamics are strictly derived from CGM invariants without arbitrary design choices.

**Predict Step Ordering (Required Sequence).** Implementations MUST execute the following steps in this exact order:

1. **Compute gradient from current state:**
   ```
   y_grad(t) = B^T x(t)
   ```

2. **Compute current aperture:**
   ```
   G(t) = ||y_grad(t)||^2
   C_current = ||y_cycle(t)||^2
   A_D(t) = C_current / (G(t) + C_current)
   ```

3. **Update potentials using A_D(t):**
   
   For each stage i in {0, 1, 2, 3}:
   
   Economy (receives from Education):
   ```
   x_Econ[i](t+1) = clip(x_Econ[i](t) + kappa * w[i] * (x_Edu[i](t) - x_Econ[i](t)) - kappa * w[i] * (A_Econ(t) - A*), 0, 1)
   ```
   
   Employment (receives from Economy):
   ```
   x_Emp[i](t+1) = clip(x_Emp[i](t) + kappa * w[i] * (x_Econ[i](t) - x_Emp[i](t)) - kappa * w[i] * (A_Emp(t) - A*), 0, 1)
   ```
   
   Education (receives from Employment):
   ```
   x_Edu[i](t+1) = clip(x_Edu[i](t) + kappa * w[i] * (x_Emp[i](t) - x_Edu[i](t)) - kappa * w[i] * (A_Edu(t) - A*), 0, 1)
   ```

4. **Normalize Employment potentials:**
   - Clip each component to [0, 1]
   - If sum is zero, set to uniform [0.25, 0.25, 0.25, 0.25]
   - Else normalize: x_Emp := x_Emp / sum(x_Emp)
   - Record `employment_normalized: true` if normalization changed any value

5. **Compute new gradient:**
   ```
   y_grad(t+1) = B^T x(t+1)
   G(t+1) = ||y_grad(t+1)||^2
   ```

6. **Update cycle component:**
   ```
   C_target = A* * G(t+1) / (1 - A*)
   ```
   
   Then apply cycle evolution with numeric guards:
   ```
   C_EPS = 1e-10
   MAX_SCALE_RATIO = 10.0
   
   If C_current < C_EPS:
       # Near-zero cycle: relaxation-consistent seeding
       C_next = r * C_target
       if C_next < C_EPS:
           y_cycle(t+1) = 0
       else:
           Let u be the first fixed W-orthonormal cycle basis vector
           y_cycle(t+1) = u * sqrt(C_next)
   Else:
       C_next = C_current + r * (C_target - C_current)
       C_next = max(C_next, 0.0)
       scale = sqrt(C_next / C_current)
       scale = min(scale, MAX_SCALE_RATIO)
       y_cycle(t+1) = y_cycle(t) * scale
   ```

7. **Compute final edge vector and aperture:**
   ```
   y(t+1) = y_grad(t+1) + y_cycle(t+1)
   A_D(t+1) = ||y_cycle(t+1)||^2 / ||y(t+1)||^2
   SI_D(t+1) = 100 / max(A_D(t+1)/A*, A*/A_D(t+1))
   ```

**Determinism requirement:** This ordering ensures that A(t) is computed from state at time t before it is used in the potential update equations. Reordering these steps produces different trajectories and is not permitted.

### 3.3 Update Dynamics

The update step has two distinct targets:

**Displacement Posterior Update.** The Bayesian posterior over displacement components is updated with new evidence (Section 4). This affects reported displacement values, uncertainty intervals, and route stability.

**Internal Potential Correction.** Internal potentials are corrected toward observed values only when explicit domain potentials are provided in the input. When only displacement estimates are provided, internal potentials evolve by prediction alone and are not corrected.

**Cycle Component Constraint.** The update step does not modify y_cycle based on observed displacement or potentials. The cycle component is not identifiable from the MVP input interface (potentials or displacement only) without placing an additional probabilistic model over y_cycle, which this specification does not include.

### 3.4 Initialization

When a session begins (first packet for a session_id, or any packet without session_id):

**With potentials provided:**
1. Initialize x_D from input values (after Employment normalization if needed)
2. Compute y_grad = B^T x
3. Seed y_cycle using the canonical seeding procedure (Section 3.5) with A_target = A_INIT = 0.12

**With displacement estimate only:**
1. Initialize x_D = x_balanced for all domains
2. Seed y_cycle using the canonical seeding procedure with A_target = A_INIT = 0.12

The initial aperture A_INIT = 0.12 reflects estimated current deployment states based on pilot evaluations reported in the GGG paper. After initialization, the cycle component evolves toward A* = 0.0207 through the predict step. A_INIT is used only at session start; all subsequent evolution targets A*.

### 3.5 Canonical Cycle Seeding

The cycle component is seeded deterministically to achieve a target aperture:

1. Compute gradient: y_grad = B^T x
2. Compute gradient energy: G = ||y_grad||^2
3. If G < 1e-12, set y_grad to the first column of B^T, normalized to unit length, then scaled so that G = 1e-4
4. Compute target cycle energy: C_target = A_target * G / (1 - A_target)
5. Select the first cycle basis vector c_1 = [1, -1, 0, 1, 0, 0]^T
6. Normalize: c_norm = c_1 / ||c_1||
7. Set sign: if c_norm[0] < 0, multiply c_norm by -1
8. Seed: y_cycle = sqrt(C_target) * c_norm

The sign convention (step 7) ensures determinism across implementations that may produce sign-flipped basis vectors.

---

## 4. Uncertainty Quantification

### 4.1 Probabilistic Model

The Compass maintains a posterior distribution over displacement components using independent Beta distributions. This choice reflects the structure of displacement as bounded values in [0,1].

For each component d_i in {GTD, IVD, IAD, IID}, the posterior is:

```
d_i ~ Beta(alpha_i, beta_i)
```

initialized with prior parameters alpha_0 = 1, beta_0 = 1 (uniform distribution, maximum entropy on [0,1]).

### 4.2 Bayesian Update

**Measurement Noise Source (Strict Rule).** The measurement noise sigma used in the Bayesian update is determined by the following priority:

| Evidence Source | Noise Source |
|----------------|--------------|
| `observations[]` entry | Use the entry's `noise` field |
| `displacement_estimate` | Use `config.measurement_noise` (default 0.05) |
| Displacement computed from potentials | Use `config.measurement_noise` (default 0.05) |

This rule ensures reproducibility: given the same input packet and config, all implementations use the same sigma value.

**Update Procedure.** When displacement component d is observed with measurement noise sigma (determined by the rule above):

1. Clamp observed value: d_c = clamp(d, 0.001, 0.999)
2. Clamp noise: sigma_c = clamp(sigma, 0.01, 1.0)
3. Compute effective sample size from variance identity:
   ```
   n_eff = d_c * (1 - d_c) / sigma_c^2
   ```
4. Update posterior:
   ```
   alpha := alpha + n_eff * d_c
   beta := beta + n_eff * (1 - d_c)
   ```

This update treats the observation as equivalent to n_eff fractional Bernoulli trials with success rate d_c. The variance-based derivation of n_eff ensures that the declared noise sigma corresponds to the posterior uncertainty.

**Independence Assumption.** Components are updated independently. This ignores potential correlations between displacement components. This is a modeling simplification documented for transparency.

### 4.3 Credible Intervals

The 90% credible interval for each component is:

```
[BetaQuantile(0.05; alpha, beta), BetaQuantile(0.95; alpha, beta)]
```

where BetaQuantile is the inverse cumulative distribution function of the Beta distribution.

### 4.4 Route Stability

Route stability measures the robustness of the routing recommendation to posterior uncertainty.

**Procedure:**
1. Draw N = 1000 samples from the joint posterior (independent samples per component)
2. For each sample, determine the dominant displacement component (applying tie-break order)
3. Map dominant component to work category
4. Stability = fraction of samples matching the modal (most frequent) route

Stability near 1.0 indicates the routing is robust. Stability below the threshold (default 0.65) triggers unstable mode.

### 4.5 Scope of Uncertainty

The uncertainty quantification applies only to displacement D and derived routing. It does not apply to:

- **Aperture A:** depends on cycle component, which is not identifiable from MVP inputs
- **SI:** derived from aperture
- **Patterns:** categorical, not probabilistic

---

## 5. Routing

### 5.1 Displacement-to-Work Mapping

The dominant displacement component indicates the most relevant category of corrective work:

| Dominant | Work Category | Focus |
|----------|---------------|-------|
| GTD | Governance Management (GM) | Restore traceability to Authentic sources |
| IVD | Information Curation (ICu) | Restore variety of Authority types |
| IAD | Inference Interaction (IInter) | Restore accountability termination in Authentic Agency |
| IID | Intelligence Cooperation (ICo) | Restore integrity of Authority-Agency alignment |

### 5.2 Tie-Break Order

When multiple components share the maximum value, the dominant is selected by priority:

**Default order:** GTD > IAD > IVD > IID

GTD is first because governance traceability is the structural root of alignment. IAD is second because unaccountable inference is the most common operational failure mode.

This order is configurable.

### 5.3 Routing Modes

| Mode | Condition | Behavior |
|------|-----------|----------|
| active | max(D) >= 0.10 AND stability >= 0.65 | Route to indicated work category |
| maintenance | max(D) < 0.10 | System near balance; route to highest component |
| unstable | stability < 0.65 | Routing unreliable; recommend measurement improvement |

In unstable mode:
- route_to is null
- low_stability_action is ICu (Information Curation)
- Work indicated recommends improving measurement quality before acting

---

## 6. Input Specification

### 6.1 Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique packet identifier |
| timestamp | ISO 8601 | Packet creation time |
| use_case | string | Workflow context identifier |
| scope | string | Plain language description of context |
| receiving_point.role | string | Capacity label for recipient |
| receiving_point.channel | string | Delivery channel identifier |

### 6.2 Evidence Fields

Exactly one of the following must be provided:

**Displacement estimate:**
```yaml
displacement_estimate:
  GTD: <float in [0,1]>
  IVD: <float in [0,1]>
  IAD: <float in [0,1]>
  IID: <float in [0,1]>
```

**Domain potentials:**
```yaml
potentials:
  economy:
    Gov: <float in [0,1]>
    Info: <float in [0,1]>
    Infer: <float in [0,1]>
    Int: <float in [0,1]>
  employment:
    GM: <float in [0,1]>
    ICu: <float in [0,1]>
    IInter: <float in [0,1]>
    ICo: <float in [0,1]>
  education:
    GT: <float in [0,1]>
    IV: <float in [0,1]>
    IA: <float in [0,1]>
    IInteg: <float in [0,1]>
```

When potentials are provided, all three domains must be complete.

### 6.3 Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| observations | list | Additional evidence on specific components |
| patterns | list | THM grammar expressions (pass-through only) |
| config | object | Override operational thresholds |
| session_id | string | Session identifier for stateful operation |

**Observation format:**
```yaml
observations:
  - id: <string>
    value: <float in [0,1]>
    noise: <float in (0,1]>
    maps_to: <GTD|IVD|IAD|IID>
```

Observations are processed in order, each updating the specified component posterior.

### 6.4 Validation Rules

- All displacement and potential values must be in [0,1]
- Measurement noise sigma must satisfy 0 < sigma <= 1
- Employment potentials must sum to 1 (normalized if not)
- Packets violating constraints are rejected with diagnostic

---

## 7. Output Specification

### 7.1 Reading Structure

```yaml
reading:
  id: <generated reading identifier>
  egress_id: <input packet id>
  timestamp: <ISO 8601>
  use_case: <from input>

  classification: "[Authority:Derivative] + [Agency:Derivative]"
  flow: "[Authority:Authentic] -> [Authority:Derivative] + [Agency:Derivative] -> [Agency:Authentic]"

  receiving_point:
    role: <from input>
    channel: <from input>
    status: "delivered"

  ledger:
    displacement:
      GTD: <posterior mean>
      IVD: <posterior mean>
      IAD: <posterior mean>
      IID: <posterior mean>
      dominant: <component name>
    observed:
      GTD: <input value>
      IVD: <input value>
      IAD: <input value>
      IID: <input value>
    source: <"provided" | "computed">
    uncertainty:
      intervals:
        GTD: [<5th percentile>, <95th percentile>]
        IVD: [<5th percentile>, <95th percentile>]
        IAD: [<5th percentile>, <95th percentile>]
        IID: [<5th percentile>, <95th percentile>]
      route_stability: <float in [0,1]>
      samples: <integer>
    si:
      economy: <float>
      employment: <float>
      education: <float>

  patterns: <from input, unchanged>

  routing:
    mode: <"active" | "maintenance" | "unstable">
    route_to: <work category or null>
    work_indicated: <human-readable description>
```

The observed field is present only when displacement_estimate was provided. When displacement is computed from potentials, the observed field is omitted.

### 7.2 Work Record

```yaml
work_record:
  id: <generated identifier>
  reading_id: <associated reading>
  timestamp: <ISO 8601>
  category: <work category>
  work_done: <human-provided description>
```

---

## 8. Configuration

### 8.1 Operational Parameters (Configurable)

| Parameter | Default | Description |
|-----------|---------|-------------|
| measurement_noise | 0.05 | Default sigma for displacement observations |
| mc_samples | 1000 | Monte Carlo samples for stability |
| maintenance_threshold | 0.10 | max(D) below which mode is maintenance |
| min_route_stability | 0.65 | Stability below which mode is unstable |
| tie_break_order | [GTD, IAD, IVD, IID] | Priority for equal components |

### 8.2 Structural Constants (Not Configurable)

**Precision and Rounding.** Display values shown in this specification are rounded for readability. Implementations MUST compute all constants (A*, stage weights, kappa_0, etc.) using the exact values provided in `cgm_constants.py`. Do not use rounded display values in computations.

| Constant | Display Value | Exact Source |
|----------|---------------|--------------|
| A* | 0.0207 | CGM: 1 - delta_BU/m_a (exact from cgm_constants) |
| A_INIT | 0.12 | Estimated current deployment state |
| x_balanced | [0.5128, 0.2308, 0.2564, 0.0130] | CGM stage weights (exact from compute_stage_weights) |
| w_BU | 0.0130 | Exact value from compute_stage_weights(include_bu=True) |
| W | I_6 (identity) | Equal edge weighting convention |
| prior_alpha, prior_beta | 1, 1 | Maximum entropy prior on [0,1] |
| kappa_0 | 0.0398 | CGM: 1/(2*Q_G) where Q_G = 4*pi (exact from cgm_constants) |
| r | kappa_0 | Cycle evolution rate |
| dt | 1 | Time step |

---

## 9. Implementation Requirements

### 9.1 Determinism

All computations must be deterministic. Given identical inputs, any two implementations must produce identical outputs.

**Monte Carlo seed derivation:**
```
if session_id is null or empty:
    session_id = "none"
seed = uint64(sha256(utf8(session_id + "|" + egress_id))[0:8])
```

**Monte Carlo PRNG requirement:** Route stability Monte Carlo MUST use `numpy.random.Generator(PCG64)` initialized with the deterministic seed and must sample posteriors using `Generator.beta(alpha, beta, size=N)`. This ensures that two implementations using NumPy produce identical stability values for the same seed.

### 9.2 Module Structure

| Module | Responsibility |
|--------|----------------|
| cgm_constants | Q_G, m_a, delta_BU, A*, stage weights, kappa_0 |
| geometry | K4 incidence matrix B, cycle basis, Hodge projections |
| dynamics | Potential update equations, cycle evolution |
| alignment | SI computation from aperture |
| filter | Bayesian update, posterior maintenance |
| engine | Predict-update-output cycle orchestration |
| validation | Input validation, constraint enforcement |

### 9.3 Numerical Precision

- All internal computations use IEEE 754 double precision
- Posterior parameters stored as floats
- Clamping bounds: d in [0.001, 0.999], sigma in [0.01, 1.0]

---

## 10. Validation Scenarios

### Scenario 1: Active Routing

**Input:**
```yaml
displacement_estimate: { GTD: 0.30, IVD: 0.20, IAD: 0.25, IID: 0.15 }
config: { measurement_noise: 0.05 }
```

**Expected output:**
- dominant: GTD
- route_to: GM
- mode: active
- observed field present with input values

**Posterior calculation for GTD (analytical verification):**
```
d_c = 0.30
sigma_c = 0.05
n_eff = 0.30 * 0.70 / 0.05^2 = 84.0
alpha = 1 + 84.0 * 0.30 = 26.2
beta = 1 + 84.0 * 0.70 = 59.8
posterior_mean = 26.2 / (26.2 + 59.8) = 0.3047
```

### Scenario 2: Computed from Potentials

**Input:**
```yaml
potentials:
  economy: { Gov: 0.60, Info: 0.55, Infer: 0.50, Int: 0.58 }
  employment: { GM: 0.25, ICu: 0.25, IInter: 0.25, ICo: 0.25 }
  education: { GT: 0.55, IV: 0.50, IA: 0.52, IInteg: 0.60 }
```

**Expected output:**
- source: computed
- observed field absent
- displacement computed from aggregate vs x_balanced

### Scenario 3: Unstable Routing

**Input:**
```yaml
displacement_estimate: { GTD: 0.27, IVD: 0.26, IAD: 0.25, IID: 0.24 }
config: { measurement_noise: 0.20 }
```

**Expected output:**
- mode: unstable
- route_to: null
- low_stability_action: ICu

### Scenario 4: Session Continuity

**Input (packet 1):**
```yaml
id: "PKT-001"
session_id: "SES-A"
displacement_estimate: { GTD: 0.30, IVD: 0.20, IAD: 0.25, IID: 0.15 }
```

**Input (packet 2):**
```yaml
id: "PKT-002"
session_id: "SES-A"
displacement_estimate: { GTD: 0.28, IVD: 0.22, IAD: 0.24, IID: 0.16 }
```

**Expected behavior:**
- Packet 2 uses posterior from packet 1 as prior
- SI values evolve from A_INIT toward A* across packets

### Scenario 5: Determinism Test

**Purpose:** Validate that two independent implementations produce identical outputs given fixed inputs and seed.

**Input:**
```yaml
id: "DET-001"
session_id: "DET-SESSION"
displacement_estimate:
  GTD: 0.35
  IVD: 0.22
  IAD: 0.28
  IID: 0.18
config:
  measurement_noise: 0.05
```

**Seed computation:**
```
session_id = "DET-SESSION"
egress_id = "DET-001"
seed_string = "DET-SESSION|DET-001" (UTF-8)
hash_bytes = sha256(seed_string)[0:8]  # First 8 bytes of SHA256 hash
seed = uint64(hash_bytes, little-endian)  # Interpret as little-endian uint64
```

**Note:** The seed is derived by interpreting the first 8 bytes of the SHA256 digest as a **little-endian** unsigned 64-bit integer. This endianness must be explicitly specified to ensure deterministic behavior across implementations.

**Expected output (exact values to 4 decimal places):**

Posterior means (after first update from uniform prior Beta(1,1)):
- GTD: d=0.35, n_eff=0.35*0.65/0.05²=91.0, alpha=1+91.0*0.35=32.85, beta=1+91.0*0.65=60.15, mean=32.85/93.0=0.3532
- IVD: d=0.22, n_eff=0.22*0.78/0.05²=68.64, alpha=1+68.64*0.22=16.1008, beta=1+68.64*0.78=54.5392, mean=16.1008/70.64=0.2278
- IAD: d=0.28, n_eff=0.28*0.72/0.05²=80.64, alpha=1+80.64*0.28=23.5792, beta=1+80.64*0.72=59.0608, mean=23.5792/82.64=0.2851
- IID: d=0.18, n_eff=0.18*0.82/0.05²=59.04, alpha=1+59.04*0.18=11.6272, beta=1+59.04*0.82=49.4128, mean=11.6272/61.04=0.1905

Dominant: GTD
route_to: GM
mode: active

Route stability: 0.804 (exact value using PCG64 with specified seed and little-endian uint64 interpretation)

**Validation requirement:** Any two implementations given this exact input must produce:
- Identical posterior means to 4 decimal places
- Identical dominant/route_to/mode
- Identical route stability to 3 decimal places (0.804)

This requires using NumPy PCG64 as specified in Section 9.1.

---

## 11. Scope and Limitations

### 11.1 Included in MVP

- Internal CGM state with Hodge decomposition
- Predict-update-output cycle with specified ordering
- Displacement ledger with Bayesian uncertainty
- SI computation for Economy, Employment, Education
- Monte Carlo route stability
- Session-based state persistence
- Pattern pass-through

### 11.2 Not Included

- Ecology SI
- Uncertainty over SI or aperture
- Pattern detection from evidence
- Multi-reading trend analysis
- Cost or resource modeling

### 11.3 Acknowledged Simplifications

**Independence of displacement components.** The Beta posteriors are updated independently, ignoring potential correlations between displacement types.

**Equal edge weighting.** W = I treats all stage couplings equally. This defines SI; alternative weightings would define a different measure.

**Maximum entropy prior.** Beta(1,1) is used as the uninformative prior. This is a standard choice but not derived from CGM.

---

## References

1. Korompilias, B. (2025). Common Governance Model: Mathematical Physics Framework. Zenodo. https://doi.org/10.5281/zenodo.17521384

2. Korompilias, B. (2025). The Human Mark: A Structural Taxonomy of AI Safety Failures. GitHub. https://github.com/gyrogovernance/tools

3. Korompilias, B. (2025). Gyroscopic Global Governance: Post-AGI Economy, Employment, Education and Ecology. GitHub. https://github.com/gyrogovernance/tools

4. Jiang, X., Lim, L.-H., Yao, Y., and Ye, Y. (2011). Statistical ranking and combinatorial Hodge theory. Mathematical Programming, 127(1), 203-244.

5. Lim, L.-H. (2020). Hodge Laplacians on graphs. SIAM Review, 62(3), 685-715.

6. Folland, G. B. (1989). Harmonic Analysis in Phase Space. Princeton University Press.

---

**END OF SPECIFICATION**