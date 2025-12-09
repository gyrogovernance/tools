"""
Tests for alignment module.

Validates the canonical CGM SI formula:
    D = max(A/A*, A*/A)
    SI = 100/D

Reference: CGM Paper, Notes_1_Math.md
"""

import sys
from pathlib import Path

# Add research/prevention directory to path for direct execution
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
import pytest

from simulator.alignment import (
    extract_alignment_metrics,
    compute_alignment_index,
    compute_global_alignment_index,
    compute_deviation,
    compute_superintelligence_index,
    compute_domain_SI,
    A_STAR
)


class TestCanonicalSIFormula:
    """Tests for the canonical CGM SI formula."""
    
    def test_deviation_at_optimal(self):
        """D = 1 when A = A*."""
        D = compute_deviation(A_STAR, A_STAR)
        assert abs(D - 1.0) < 1e-10
    
    def test_deviation_above_optimal(self):
        """D = A/A* when A > A*."""
        A = 2 * A_STAR  # Twice the optimal
        D = compute_deviation(A, A_STAR)
        assert abs(D - 2.0) < 1e-10
    
    def test_deviation_below_optimal(self):
        """D = A*/A when A < A*."""
        A = A_STAR / 2  # Half the optimal
        D = compute_deviation(A, A_STAR)
        assert abs(D - 2.0) < 1e-10
    
    def test_si_at_optimal(self):
        """SI = 100 when A = A*."""
        SI = compute_superintelligence_index(A_STAR, A_STAR)
        assert abs(SI - 100.0) < 1e-10
    
    def test_si_at_double_optimal(self):
        """SI = 50 when A = 2*A*."""
        SI = compute_superintelligence_index(2 * A_STAR, A_STAR)
        assert abs(SI - 50.0) < 1e-10
    
    def test_si_at_half_optimal(self):
        """SI = 50 when A = A*/2."""
        SI = compute_superintelligence_index(A_STAR / 2, A_STAR)
        assert abs(SI - 50.0) < 1e-10
    
    def test_si_symmetry(self):
        """SI is symmetric around A*: SI(k*A*) = SI(A*/k)."""
        for k in [2, 3, 4, 5, 10]:
            SI_above = compute_superintelligence_index(k * A_STAR, A_STAR)
            SI_below = compute_superintelligence_index(A_STAR / k, A_STAR)
            assert abs(SI_above - SI_below) < 1e-10
    
    def test_si_decreases_away_from_optimal(self):
        """SI decreases as A moves away from A*."""
        SI_optimal = compute_superintelligence_index(A_STAR, A_STAR)
        SI_high = compute_superintelligence_index(0.1, A_STAR)
        SI_low = compute_superintelligence_index(0.005, A_STAR)
        
        assert SI_optimal > SI_high
        assert SI_optimal > SI_low
    
    def test_si_bounded(self):
        """SI is in (0, 100]."""
        for A in [0.001, 0.01, 0.0207, 0.05, 0.1, 0.5, 0.9]:
            SI = compute_superintelligence_index(A, A_STAR)
            assert 0 < SI <= 100


class TestDomainSI:
    """Tests for domain-specific SI computation."""
    
    def test_domain_si_equals_global_si(self):
        """compute_domain_SI should give same result as compute_superintelligence_index."""
        for A in [0.01, 0.0207, 0.05, 0.1]:
            SI1 = compute_domain_SI(A, A_STAR)
            SI2 = compute_superintelligence_index(A, A_STAR)
            assert abs(SI1 - SI2) < 1e-10


class TestGlobalSI:
    """Tests for global SI computation."""



class TestAlignmentHelpers:
    """Tests for helper functions in the alignment module."""
    
    def test_extract_alignment_metrics(self):
        """Test extraction of Gov, Info, Infer, Int from potential vector."""
        x = np.array([0.8, 0.6, 0.9, 0.7])
        Gov, Info, Infer, Int = extract_alignment_metrics(x)
        
        assert Gov == 0.8
        assert Info == 0.6
        assert Infer == 0.9
        assert Int == 0.7
    
    def test_compute_alignment_index_optimal(self):
        """Test alignment index with optimal aperture."""
        # In canonical CGM, SI depends only on aperture
        S = compute_alignment_index(
            Gov=1.0, Info=1.0, Infer=1.0, Int=1.0,
            A=A_STAR, A_star=A_STAR
        )
        
        # S = SI/100 = 100/100 = 1.0
        assert abs(S - 1.0) < 1e-10
    
    def test_compute_alignment_index_non_optimal(self):
        """Test alignment index with non-optimal aperture."""
        # A = 2*A* gives D = 2, SI = 50, S = 0.5
        S = compute_alignment_index(
            Gov=1.0, Info=1.0, Infer=1.0, Int=1.0,
            A=2 * A_STAR, A_star=A_STAR
        )
        
        assert abs(S - 0.5) < 1e-10
    
    def test_compute_global_alignment_index(self):
        """Test global alignment index computation."""
        # Input is on [0, 1] scale (S = SI/100)
        S_global = compute_global_alignment_index(
            S_econ=0.8,
            S_work=0.7,
            S_edu=0.9
        )
        
        expected = (0.8 + 0.7 + 0.9) / 3
        assert abs(S_global - expected) < 1e-10


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_si_at_zero_aperture(self):
        """SI should be 0 when A = 0 (pure gradient, no cycle)."""
        SI = compute_superintelligence_index(0.0, A_STAR)
        assert SI == 0.0
    
    def test_deviation_at_zero_aperture(self):
        """D should be infinity when A = 0."""
        D = compute_deviation(0.0, A_STAR)
        assert D == float('inf')
    
    def test_si_at_very_high_aperture(self):
        """SI should be very low when A >> A*."""
        SI = compute_superintelligence_index(0.9, A_STAR)
        # D = 0.9 / 0.0207 ≈ 43.5
        # SI = 100 / 43.5 ≈ 2.3
        assert SI < 5.0
        assert SI > 0.0
