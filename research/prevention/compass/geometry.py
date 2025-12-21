"""
Geometry Module: K4 Tetrahedral Structure and Hodge Decomposition

Implements the K4 graph incidence matrix, Hodge decomposition, and aperture
computation as specified in Notes_1_Math.md and gyroscopic_global_governance.md.

The four vertices correspond to CGM stages:
1. Governance
2. Information
3. Inference
4. Intelligence
"""

import numpy as np
from typing import Optional, Tuple


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
    
    Returns:
        B: 4x6 numpy array
    """
    B = np.array([
        [-1, -1, -1,  0,  0,  0],  # Vertex 1: Governance
        [ 1,  0,  0, -1, -1,  0],  # Vertex 2: Information
        [ 0,  1,  0,  1,  0, -1],  # Vertex 3: Inference
        [ 0,  0,  1,  0,  1,  1]   # Vertex 4: Intelligence
    ])
    return B


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


def compute_projections(B: np.ndarray, W: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the gradient and cycle projection matrices using fixed cycle basis.
    
    P_cycle = C C^T W where C is the fixed W-orthonormal cycle basis
    P_grad = I_6 - P_cycle
    
    This ensures the Hodge split is exact and deterministic.
    
    Args:
        B: 4x6 incidence matrix (unused, kept for compatibility)
        W: 6x6 weight matrix
    
    Returns:
        P_grad: 6x6 gradient projection matrix
        P_cycle: 6x6 cycle projection matrix
    """
    # Get fixed cycle basis (W-orthonormal)
    C = get_cycle_basis_fixed(W)  # shape (6, 3)
    
    # If columns are W-orthonormal, P_cycle = C C^T W
    P_cycle = C @ (C.T @ W)
    P_grad = np.eye(6) - P_cycle
    
    return P_grad, P_cycle


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


def get_cycle_basis_fixed(W: np.ndarray) -> np.ndarray:
    """
    Returns the fixed cycle basis for K4 (three face cycles).
    
    The cycle space for K4 has dimension 3, corresponding to the three
    independent triangular faces. This function returns a W-orthonormal
    basis with deterministic sign convention.
    
    Args:
        W: 6x6 weight matrix
    
    Returns:
        basis: 6x3 array, columns are W-orthonormal basis vectors
    """
    # Basis vectors in R^6 for K4 cycle space (faces)
    # Face 1: CS-UNA-ONA (edges 0, 3, 1)
    # Face 2: CS-UNA-BU (edges 0, 4, 2)
    # Face 3: CS-ONA-BU (edges 1, 5, 2)
    C = np.array([
        [ 1,  1,  0],  # Edge 0: CS-UNA
        [-1,  0,  1],  # Edge 1: CS-ONA
        [ 0, -1, -1],  # Edge 2: CS-BU
        [ 1,  0,  0],  # Edge 3: UNA-ONA
        [ 0,  1,  0],  # Edge 4: UNA-BU
        [ 0,  0,  1],  # Edge 5: ONA-BU
    ], dtype=float)

    # W-orthonormalize columns (Gram-Schmidt with W inner product)
    def w_dot(a, b):
        return float(a.T @ W @ b)

    Q = np.zeros_like(C)
    for j in range(C.shape[1]):
        v = C[:, j].copy()
        for k in range(j):
            v = v - w_dot(Q[:, k], v) * Q[:, k]
        norm = np.sqrt(max(w_dot(v, v), 0.0))
        if norm == 0:
            raise ValueError("Cycle basis construction failed (zero norm)")
        Q[:, j] = v / norm

        # Sign convention: first nonzero entry positive
        nz = np.flatnonzero(np.abs(Q[:, j]) > 1e-12)
        if nz.size > 0 and Q[nz[0], j] < 0:
            Q[:, j] *= -1.0

    return Q  # shape (6,3), W-orthonormal


def get_cycle_basis(B: np.ndarray, W: np.ndarray) -> np.ndarray:
    """
    Returns the fixed cycle basis for K4.
    
    Args:
        B: 4x6 incidence matrix (unused, kept for compatibility)
        W: 6x6 weight matrix
    
    Returns:
        basis: 6x3 array, columns are W-orthonormal basis vectors
    """
    return get_cycle_basis_fixed(W)


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
           For Economy: [Gov, Info, Infer, Int]
           For Employment: [GM, ICu, IInter, ICo]
           For Education: [GT, IV, IA, IInteg]
           For Ecology: [E_gov, E_info, E_inf, E_intel]
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
    
    # Guard against zero gradient (G = 0 edge case)
    # If ||B^T x||_W² is numerically zero, replace with deterministic seed
    eps = 1e-12
    G_MIN = 1e-4
    
    if G < eps:
        # Use first column of B^T as fixed deterministic direction
        v0 = B.T[:, 0]
        v0_norm_sq = np.dot(v0, W @ v0)
        
        if v0_norm_sq > 0:
            # Normalize v0 to unit W-norm, then scale to achieve G_MIN
            v0_normalized = v0 / np.sqrt(v0_norm_sq)
            y_grad0 = v0_normalized * np.sqrt(G_MIN)
            G = G_MIN
        else:
            # Fallback: use uniform vector (should not happen with valid B)
            y_grad0 = np.ones(6) / np.sqrt(6) * np.sqrt(G_MIN)
            G = G_MIN
    
    # Compute k^2 = (A / (1 - A)) * G
    # This gives cycle energy C = k^2 (since u has unit W-norm)
    k_squared = (target_aperture / (1 - target_aperture)) * G
    
    # Set cycle component
    k = np.sqrt(k_squared)
    c = k * u
    
    # Construct final edge vector
    y = y_grad0 + c
    
    return y

