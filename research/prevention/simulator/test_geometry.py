"""
Tests for geometry module.

Validates K4 structure, Hodge decomposition, and aperture computation.
"""

import sys
from pathlib import Path

# Add research/prevention directory to path for direct execution
# This allows tests to be run directly as scripts
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
import pytest

from simulator.geometry import (
    get_incidence_matrix,
    get_weight_matrix,
    compute_projections,
    hodge_decomposition,
    compute_aperture,
    construct_edge_vector_with_aperture,
    get_cycle_basis
)


def test_incidence_matrix():
    """Test that incidence matrix has correct structure."""
    B = get_incidence_matrix()
    
    assert B.shape == (4, 6)
    assert np.all(B.sum(axis=0) == 0)  # Each column sums to 0 (edge: -1 + 1 = 0)


def test_weight_matrix():
    """Test weight matrix creation."""
    W_identity = get_weight_matrix()
    assert np.allclose(W_identity, np.eye(6))
    
    weights = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    W = get_weight_matrix(weights)
    assert np.allclose(W, np.diag(weights))


def test_projections_idempotent():
    """Test that P_grad and P_cycle are idempotent."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    P_grad, P_cycle = compute_projections(B, W)
    
    # P_grad^2 ≈ P_grad
    assert np.allclose(P_grad @ P_grad, P_grad, atol=1e-10)
    
    # P_cycle^2 ≈ P_cycle
    assert np.allclose(P_cycle @ P_cycle, P_cycle, atol=1e-10)
    
    # P_grad @ P_cycle ≈ 0
    assert np.allclose(P_grad @ P_cycle, np.zeros((6, 6)), atol=1e-10)


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


def test_construct_edge_vector_with_aperture_zero():
    """Test constructing edge vector with zero aperture."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = construct_edge_vector_with_aperture(x, B, W, target_aperture=0)
    
    # Should be pure gradient
    y_expected = B.T @ x
    assert np.allclose(y, y_expected, atol=1e-10)


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


def test_construct_edge_vector_with_aperture_none():
    """Test constructing edge vector with None aperture (should return gradient)."""
    B = get_incidence_matrix()
    W = get_weight_matrix()
    
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = construct_edge_vector_with_aperture(x, B, W, target_aperture=None)
    
    y_expected = B.T @ x
    assert np.allclose(y, y_expected, atol=1e-10)


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

