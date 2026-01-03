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
           For Education: [GMT, ICV, IIA, ICI]
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
    
    # Handle case when gradient energy is zero or very small
    # (e.g., all potentials equal: x = [0.5, 0.5, 0.5, 0.5])
    # In this case, we need to construct y with only cycle component
    # but we need some reference scale
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

