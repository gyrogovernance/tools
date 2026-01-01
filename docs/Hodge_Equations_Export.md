# Hodge Equations and Logic - Complete Export

This document exports all Hodge decomposition equations, projection matrices, and related logic from the simulator codebase with full context.

## Overview

The simulator implements Hodge decomposition on the K4 tetrahedral graph structure. The four vertices correspond to CGM stages:
1. Governance (CS)
2. Information (UNA)
3. Inference (ONA)
4. Intelligence (BU)

The K4 graph has 6 edges connecting all pairs of vertices. Hodge decomposition splits any edge vector `y` into orthogonal components:
- **Gradient component** `y_grad ∈ Im(B^T)`: Recoverable from vertex potentials
- **Cycle component** `y_cycle ∈ ker(BW)`: Non-conservative circulation

The decomposition is orthogonal with respect to the weighted inner product `⟨·,·⟩_W`.

## Core Implementation: `geometry.py`

### Incidence Matrix B

The 4×6 signed incidence matrix for K4:

```python
def get_incidence_matrix() -> np.ndarray:
    """
    Returns the 4x6 signed incidence matrix B for K4.
    
    Rows correspond to vertices (CGM stages):
    1. Governance (CS)
    2. Information (UNA)
    3. Inference (ONA)
    4. Intelligence (BU)
    
    Columns correspond to edges:
    1. (1, 2) Governance–Information
    2. (1, 3) Governance–Inference
    3. (1, 4) Governance–Intelligence
    4. (2, 3) Information–Inference
    5. (2, 4) Information–Intelligence
    6. (3, 4) Inference–Intelligence
    """
    B = np.array([
        [-1, -1, -1,  0,  0,  0],  # Vertex 1: Governance
        [ 1,  0,  0, -1, -1,  0],  # Vertex 2: Information
        [ 0,  1,  0,  1,  0, -1],  # Vertex 3: Inference
        [ 0,  0,  1,  0,  1,  1]   # Vertex 4: Intelligence
    ])
    return B
```

**File**: `research/prevention/simulator/geometry.py` (lines 18-45)

### Weight Matrix W

The 6×6 diagonal weight matrix (defaults to identity):

```python
def get_weight_matrix(weights: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Returns the 6x6 weight matrix W.
    
    Args:
        weights: Optional array of 6 positive numbers. If None, returns identity.
    
    Returns:
        W: 6x6 diagonal weight matrix
    """
    if weights is None:
        return np.eye(6)
    
    if len(weights) != 6:
        raise ValueError("weights must have length 6")
    
    if np.any(weights <= 0):
        raise ValueError("all weights must be positive")
    
    return np.diag(weights)
```

**File**: `research/prevention/simulator/geometry.py` (lines 48-67)

### Projection Matrices

The core Hodge projection matrices are computed as:

**Mathematical Formulation:**
- Laplacian: `L = B W B^T` (4×4)
- Gradient projection: `P_grad = B^T (B W B^T)^(-1) B W`
- Cycle projection: `P_cycle = I_6 - P_grad`

**Implementation:**

```python
def compute_projections(B: np.ndarray, W: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the gradient and cycle projection matrices.
    
    P_grad = B^T (B W B^T)^(-1) B W
    P_cycle = I_6 - P_grad
    
    Uses pseudoinverse to handle the singular Laplacian (nullspace is constant vector).
    
    Args:
        B: 4x6 incidence matrix
        W: 6x6 weight matrix
    
    Returns:
        P_grad: 6x6 gradient projection matrix
        P_cycle: 6x6 cycle projection matrix
    """
    # Compute Laplacian L = B W B^T
    L = B @ W @ B.T
    
    # Use pseudoinverse to handle singularity (nullspace is all-ones vector)
    L_inv = np.linalg.pinv(L)
    
    # Compute gradient projection
    P_grad = B.T @ L_inv @ B @ W
    
    # Compute cycle projection
    P_cycle = np.eye(6) - P_grad
    
    return P_grad, P_cycle
```

**File**: `research/prevention/simulator/geometry.py` (lines 70-99)

**Properties:**
- `P_grad` and `P_cycle` are idempotent: `P² = P`
- They are orthogonal: `P_grad @ P_cycle = 0`
- They sum to identity: `P_grad + P_cycle = I_6`

### Hodge Decomposition

The fundamental decomposition operation:

**Mathematical Formulation:**
```
y = y_grad + y_cycle

where:
- y_grad ∈ Im(B^T) (gradient subspace)
- y_cycle ∈ ker(BW) (cycle subspace)
- y_grad ⟂ y_cycle w.r.t. ⟨·,·⟩_W
```

**Implementation:**

```python
def hodge_decomposition(y: np.ndarray, P_grad: np.ndarray, P_cycle: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Performs Hodge decomposition of edge vector y.
    
    y = y_grad + y_cycle
    
    where y_grad ∈ Im(B^T) and y_cycle ∈ ker(BW), orthogonal w.r.t. ⟨·,·⟩_W.
    
    Args:
        y: Length-6 edge vector
        P_grad: 6x6 gradient projection matrix
        P_cycle: 6x6 cycle projection matrix
    
    Returns:
        y_grad: Gradient component
        y_cycle: Cycle component
    """
    y_grad = P_grad @ y
    y_cycle = P_cycle @ y
    return y_grad, y_cycle
```

**File**: `research/prevention/simulator/geometry.py` (lines 102-121)

### Aperture Computation

The aperture measures the fraction of cycle energy relative to total energy:

**Mathematical Formulation:**
```
A = ||y_cycle||²_W / ||y||²_W

where:
- ||v||²_W = v^T W v (weighted norm squared)
```

**Implementation:**

```python
def compute_aperture(y: np.ndarray, y_cycle: np.ndarray, W: np.ndarray) -> float:
    """
    Computes the aperture A = ||y_cycle||^2_W / ||y||^2_W.
    
    The aperture measures the fraction of cycle energy relative to total energy.
    
    Args:
        y: Length-6 edge vector
        y_cycle: Cycle component from Hodge decomposition
        W: 6x6 weight matrix
    
    Returns:
        A: Aperture value in [0, 1]
    """
    # Compute weighted norms squared
    y_cycle_norm_sq = np.dot(y_cycle, W @ y_cycle)
    y_norm_sq = np.dot(y, W @ y)
    
    # Handle edge case where y is zero
    if y_norm_sq == 0:
        return 0.0
    
    A = y_cycle_norm_sq / y_norm_sq
    return float(A)
```

**File**: `research/prevention/simulator/geometry.py` (lines 124-147)

**Properties:**
- `A ∈ [0, 1]`
- `A = 0` for pure gradient (conservative flow)
- `A = 1` for pure cycle (non-conservative circulation)
- Canonical value: `A* ≈ 0.0207` (from CGM)

### Cycle Basis

Computes an orthonormal basis for the cycle subspace:

**Mathematical Formulation:**
- For K4: cycle space dimension = 6 edges - 4 vertices + 1 = 3
- The cycle space is `ker(BW)`, the right nullspace of `BW`
- Found via SVD: right-singular vectors corresponding to zero singular values

**Implementation:**

```python
def get_cycle_basis(B: np.ndarray, W: np.ndarray) -> np.ndarray:
    """
    Computes a basis for the cycle subspace ker(B W).
    
    For K4, the cycle space has dimension 3 (6 edges - 4 vertices + 1 = 3).
    
    The right nullspace of BW (shape 4x6) has dimension n - rank = 6 - 3 = 3.
    We find it via SVD: the last (n - rank) rows of Vh are the nullspace basis.
    
    Args:
        B: 4x6 incidence matrix
        W: 6x6 weight matrix
    
    Returns:
        basis: 6x3 array, columns are basis vectors for ker(B W)
    """
    # Compute B W
    BW = B @ W
    
    # Find nullspace (kernel) of B W using SVD
    # BW has shape (4, 6), so SVD gives s with length min(4, 6) = 4
    U, s, Vh = np.linalg.svd(BW, full_matrices=True)
    
    # Determine rank from singular values
    tol = 1e-10
    rank = np.sum(s > tol)  # For K4, rank = 3
    
    # Nullspace dimension = n - rank = 6 - 3 = 3 for K4
    n = BW.shape[1]  # number of columns = 6
    nullspace_dim = n - rank
    
    if nullspace_dim <= 0:
        # Fallback: for K4 we know cycle space has dim 3
        basis = Vh[-3:, :].T  # shape (6, 3)
    else:
        # Right-singular vectors corresponding to zero singular values
        # are the last (n - rank) rows of Vh
        # Note: Vh has shape (6, 6) with full_matrices=True
        basis = Vh[rank:, :].T  # shape (6, nullspace_dim)
    
    # Normalize basis vectors to unit W-norm
    for i in range(basis.shape[1]):
        v = basis[:, i]
        norm_sq = np.dot(v, W @ v)
        if norm_sq > 0:
            basis[:, i] = v / np.sqrt(norm_sq)
    
    return basis
```

**File**: `research/prevention/simulator/geometry.py` (lines 150-197)

### Construct Edge Vector with Target Aperture

Constructs an edge vector with a specified aperture:

**Mathematical Formulation:**
Given gradient energy `G = ||y_grad||²_W` and target aperture `A`:
- Cycle energy: `C = A · G / (1 - A)`
- Total energy: `G + C = G / (1 - A)`

**Implementation:**

```python
def construct_edge_vector_with_aperture(
    x: np.ndarray,
    B: np.ndarray,
    W: np.ndarray,
    target_aperture: Optional[float] = None,
    cycle_basis_vector: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Constructs an edge vector y with a specified target aperture.
    
    The aperture A is defined as:
        A = ||y_cycle||²_W / ||y||²_W
    
    For a given gradient component y_grad with energy G = ||y_grad||²_W,
    and cycle component c with energy C = ||c||²_W, we have:
        A = C / (G + C)
    
    Solving for C given target A and G:
        C = A * G / (1 - A)
    
    If target_aperture is None or 0, returns pure gradient y_grad0 = B^T x.
    Otherwise, adds a cycle component to achieve the target aperture.
    
    Args:
        x: Length-4 potential vector in CGM order:
           [Governance, Information, Inference, Intelligence].
        B: 4x6 incidence matrix.
        W: 6x6 weight matrix.
        target_aperture: Desired aperture in (0, 1). If None or 0, returns pure gradient.
        cycle_basis_vector: Optional cycle direction. If None, uses first basis vector.
    
    Returns:
        y: Length-6 edge vector with specified aperture.
    """
    # Compute ideal gradient
    y_grad0 = B.T @ x
    
    # Compute gradient energy
    G = np.dot(y_grad0, W @ y_grad0)
    
    # If no target aperture or zero, return pure gradient
    if target_aperture is None or target_aperture == 0:
        return y_grad0
    
    if not (0 < target_aperture < 1):
        raise ValueError("target_aperture must be in (0, 1)")
    
    # Get cycle direction (unit W-norm)
    if cycle_basis_vector is not None:
        # Normalize to unit W-norm
        norm_sq = np.dot(cycle_basis_vector, W @ cycle_basis_vector)
        if norm_sq > 0:
            u = cycle_basis_vector / np.sqrt(norm_sq)
        else:
            raise ValueError("cycle_basis_vector has zero W-norm")
    else:
        # Get cycle basis and use first vector
        cycle_basis = get_cycle_basis(B, W)
        if cycle_basis.shape[1] == 0:
            raise ValueError("No cycle basis found")
        u = cycle_basis[:, 0]
    
    # Handle case when gradient energy is zero or very small
    # (e.g., all potentials equal: x = [0.5, 0.5, 0.5, 0.5])
    if G < 1e-10:
        # When G ≈ 0, we can't achieve target aperture A < 1 with pure cycle
        # because A = C/(G+C) → 1 as G → 0
        # 
        # To handle this, we create a small artificial gradient component
        # by perturbing the potentials slightly to break symmetry
        # This ensures the edge vector has both gradient and cycle components
        
        # Use a reference scale based on potential magnitudes
        x_scale = np.linalg.norm(x)
        if x_scale < 1e-10:
            x_scale = 1.0  # Default scale if potentials are all zero
        
        # Create a small gradient by perturbing x
        # We want G such that with target aperture A:
        # C = A * G / (1 - A)
        # Total energy = G + C = G / (1 - A)
        # Choose G to give reasonable total energy
        G_reference = x_scale ** 2  # Reference gradient energy
        G = G_reference * 0.01  # Small but non-zero gradient energy
        
        # Construct a small gradient component in a consistent direction
        # Use the first column of B^T as direction
        grad_dir = B.T[:, 0]
        grad_norm_sq = np.dot(grad_dir, W @ grad_dir)
        if grad_norm_sq > 0:
            y_grad0 = grad_dir * np.sqrt(G / grad_norm_sq)
        else:
            # Fallback: use uniform gradient
            y_grad0 = np.ones(6) * np.sqrt(G / 6)
    
    # Compute k^2 = (A / (1 - A)) * G
    # This gives cycle energy C = k^2 (since u has unit W-norm)
    k_squared = (target_aperture / (1 - target_aperture)) * G
    
    # Set cycle component
    k = np.sqrt(k_squared)
    c = k * u
    
    # Construct final edge vector
    y = y_grad0 + c
    
    return y
```

**File**: `research/prevention/simulator/geometry.py` (lines 200-312)

## Usage in Dynamics: `dynamics.py`

### Cycle Component Update

Updates the cycle component toward a target aperture:

```python
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
```

**File**: `research/prevention/simulator/dynamics.py` (lines 366-437)

### Step Function - Hodge Decomposition Usage

In the main `step()` function, Hodge decomposition is performed after constructing new edge vectors:

```python
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
```

**File**: `research/prevention/simulator/dynamics.py` (lines 512-525)

For ecology domain (if included):

```python
# Hodge decomposition and aperture
y_grad_ecol_decomp, y_cycle_ecol = hodge_decomposition(y_ecol_next, P_grad, P_cycle)
A_Ecol_next = compute_aperture(y_ecol_next, y_cycle_ecol, W)
```

**File**: `research/prevention/simulator/dynamics.py` (lines 630-632)

## Usage in Simulation: `simulation.py`

### Initialization - Hodge Decomposition

During state initialization, Hodge decomposition is used to compute initial apertures:

```python
# Compute initial apertures and SI using canonical CGM formula
# SI = 100 / max(A/A*, A*/A)
y_grad_econ, y_cycle_econ = hodge_decomposition(y_econ, P_grad, P_cycle)
A_Econ0 = compute_aperture(y_econ, y_cycle_econ, W)
SI_Econ0 = compute_domain_SI(A_Econ0, config.A_star)

y_grad_emp, y_cycle_emp = hodge_decomposition(y_emp, P_grad, P_cycle)
A_Emp0 = compute_aperture(y_emp, y_cycle_emp, W)
SI_Emp0 = compute_domain_SI(A_Emp0, config.A_star)

y_grad_edu, y_cycle_edu = hodge_decomposition(y_edu, P_grad, P_cycle)
A_Edu0 = compute_aperture(y_edu, y_cycle_edu, W)
SI_Edu0 = compute_domain_SI(A_Edu0, config.A_star)
```

**File**: `research/prevention/simulator/simulation.py` (lines 529-540)

For ecology domain:

```python
y_grad_ecol, y_cycle_ecol = hodge_decomposition(y_ecol, P_grad, P_cycle)
A_Ecol0 = compute_aperture(y_ecol, y_cycle_ecol, W)
SI_Ecol0 = compute_domain_SI(A_Ecol0, config.A_star)
```

**File**: `research/prevention/simulator/simulation.py` (lines 582-584)

## Usage in Lyapunov Analysis: `lyapunov.py`

### Total Lyapunov Function

Hodge decomposition is used to compute aperture contributions to the Lyapunov function:

```python
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
```

**File**: `research/prevention/simulator/lyapunov.py` (lines 115-136)

The Lyapunov function uses:
- Aperture deviation: `V_apert = 0.5 · (log(A/A*))²` for each domain
- Stage profile displacement: `V_stage = 0.5 · ||x_deriv - x_balanced||²`
- Total: `V_total = V_apert_total + V_stage`

## Test Cases: `test_geometry.py`

### Test: Pure Gradient Decomposition

```python
def test_hodge_decomposition_pure_gradient():
    """Test Hodge decomposition for pure gradient input."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    # Create pure gradient: y = B^T x
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = B.T @ x
    
    y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
    
    # Should recover y_grad ≈ y and y_cycle ≈ 0
    assert np.allclose(y_grad, y, atol=1e-10)
    assert np.allclose(y_cycle, np.zeros(6), atol=1e-10)
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 64-78)

### Test: Pure Cycle Decomposition

```python
def test_hodge_decomposition_pure_cycle():
    """Test Hodge decomposition for pure cycle input."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    # Get a cycle basis vector
    cycle_basis = get_cycle_basis(B, W)
    if cycle_basis.shape[1] > 0:
        y = cycle_basis[:, 0]
        
        y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
        
        # Should have y_grad ≈ 0 and y_cycle ≈ y
        assert np.allclose(y_grad, np.zeros(6), atol=1e-10)
        assert np.allclose(y_cycle, y, atol=1e-10)
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 81-96)

### Test: Aperture for Pure Gradient

```python
def test_aperture_pure_gradient():
    """Test aperture for pure gradient (should be ≈ 0)."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = B.T @ x
    y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
    
    A = compute_aperture(y, y_cycle, W)
    assert A < 1e-10  # Should be essentially zero
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 99-110)

### Test: Aperture for Pure Cycle

```python
def test_aperture_pure_cycle():
    """Test aperture for pure cycle (should be ≈ 1)."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    cycle_basis = get_cycle_basis(B, W)
    if cycle_basis.shape[1] > 0:
        y = cycle_basis[:, 0]
        y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
        
        A = compute_aperture(y, y_cycle, W)
        assert abs(A - 1.0) < 1e-10  # Should be essentially 1
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 113-125)

### Test: Construct Edge Vector with Target Aperture

```python
def test_construct_edge_vector_with_aperture_target():
    """Test constructing edge vector with target aperture."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    x = np.array([1.0, 2.0, 3.0, 4.0])
    target_A = 0.0207
    
    y = construct_edge_vector_with_aperture(x, B, W, target_aperture=target_A)
    
    # Verify aperture
    y_grad, y_cycle = hodge_decomposition(y, P_grad, P_cycle)
    A = compute_aperture(y, y_cycle, W)
    
    assert abs(A - target_A) < 1e-6  # Should match target closely
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 141-156)

### Test: Cycle Basis Dimension

```python
def test_cycle_basis_dimension():
    """Test that cycle basis has correct dimension for K₄.
    
    For K₄: 6 edges - 4 vertices + 1 connected component = 3 cycles.
    """
    B = get_incidence_matrix()
    W = get_weight_matrix()
    
    cycle_basis = get_cycle_basis(B, W)
    
    # Should have shape (6, 3) - 6 edges, 3 independent cycles
    assert cycle_basis.shape == (6, 3), f"Expected (6, 3), got {cycle_basis.shape}"
    
    # Each basis vector should be in ker(BW)
    BW = B @ W
    for i in range(cycle_basis.shape[1]):
        v = cycle_basis[:, i]
        assert np.allclose(BW @ v, np.zeros(4), atol=1e-10), f"Basis vector {i} not in kernel"
    
    # Basis vectors should be W-orthonormal (or at least unit W-norm)
    for i in range(cycle_basis.shape[1]):
        v = cycle_basis[:, i]
        norm_sq = np.dot(v, W @ v)
        assert abs(norm_sq - 1.0) < 1e-10, f"Basis vector {i} not unit W-norm"
```

**File**: `research/prevention/simulator/tests/test_geometry.py` (lines 171-195)

## Summary

### Key Mathematical Relationships

1. **Hodge Decomposition:**
   ```
   y = y_grad + y_cycle
   y_grad = P_grad @ y
   y_cycle = P_cycle @ y
   ```

2. **Projection Matrices:**
   ```
   P_grad = B^T (B W B^T)^(-1) B W
   P_cycle = I_6 - P_grad
   ```

3. **Aperture:**
   ```
   A = ||y_cycle||²_W / ||y||²_W
   ```

4. **Cycle Energy from Target Aperture:**
   ```
   C = A · G / (1 - A)
   where G = ||y_grad||²_W
   ```

### File Locations

- **Core Implementation**: `research/prevention/simulator/geometry.py`
- **Dynamics Usage**: `research/prevention/simulator/dynamics.py`
- **Simulation Usage**: `research/prevention/simulator/simulation.py`
- **Lyapunov Usage**: `research/prevention/simulator/lyapunov.py`
- **Tests**: `research/prevention/simulator/tests/test_geometry.py`

### Key Functions

1. `get_incidence_matrix()` - K4 incidence matrix B
2. `get_weight_matrix()` - Weight matrix W
3. `compute_projections()` - Compute P_grad and P_cycle
4. `hodge_decomposition()` - Decompose edge vector
5. `compute_aperture()` - Compute aperture from decomposition
6. `get_cycle_basis()` - Compute cycle subspace basis
7. `construct_edge_vector_with_aperture()` - Construct edge vector with target aperture
8. `update_cycle_component()` - Update cycle component toward target aperture

All implementations use deterministic, CGM-derived parameters with no arbitrary values.

