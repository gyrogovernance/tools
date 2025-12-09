"""
Tests for domain state classes.

Validates state initialization, potential vector conversion, and updates.
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

from simulator.domains import EconomyState, EmploymentState, EducationState


def test_economy_state():
    """
    Test EconomyState initialization and methods.
    
    Economy (CGM): Gov=Governance, Info=Information, Infer=Inference, Int=Intelligence
    """
    state = EconomyState(Gov=0.8, Info=0.6, Infer=0.9, Int=0.7)
    
    assert state.Gov == 0.8
    assert state.Info == 0.6
    assert state.Infer == 0.9
    assert state.Int == 0.7
    
    x = state.to_potential_vector()
    assert np.allclose(x, [0.8, 0.6, 0.9, 0.7])
    
    state.update_from_potential_vector(np.array([0.5, 0.4, 0.6, 0.3]))
    assert state.Gov == 0.5
    assert state.Info == 0.4
    assert state.Infer == 0.6
    assert state.Int == 0.3


def test_economy_state_clipping():
    """Test that EconomyState clips values to [0, 1]."""
    state = EconomyState(Gov=-0.1, Info=1.5, Infer=0.5, Int=0.5)
    
    assert 0.0 <= state.Gov <= 1.0
    assert 0.0 <= state.Info <= 1.0
    assert state.Info == 1.0  # Clipped from 1.5


def test_employment_state():
    """
    Test EmploymentState initialization and normalization.
    
    Employment (Gyroscope): GM=Governance Management, ICu=Information Curation,
    IInter=Inference Interaction, ICo=Intelligence Cooperation
    """
    state = EmploymentState(GM=0.3, ICu=0.2, IInter=0.3, ICo=0.2)
    
    # Should be normalized to sum = 1
    total = state.GM + state.ICu + state.IInter + state.ICo
    assert abs(total - 1.0) < 1e-10
    
    x = state.to_potential_vector()
    assert abs(np.sum(x) - 1.0) < 1e-10


def test_employment_state_normalization():
    """Test that EmploymentState normalizes shares."""
    # Shares that don't sum to 1
    state = EmploymentState(GM=0.5, ICu=0.5, IInter=0.5, ICo=0.5)
    
    total = state.GM + state.ICu + state.IInter + state.ICo
    assert abs(total - 1.0) < 1e-10


def test_employment_state_update():
    """Test EmploymentState update and renormalization."""
    state = EmploymentState(GM=0.25, ICu=0.25, IInter=0.25, ICo=0.25)
    
    # Update with values that don't sum to 1
    state.update_from_potential_vector(np.array([0.4, 0.3, 0.2, 0.1]))
    
    total = state.GM + state.ICu + state.IInter + state.ICo
    assert abs(total - 1.0) < 1e-10


def test_education_state():
    """
    Test EducationState initialization and methods.
    
    Education (THM): GT=Governance Traceability, IV=Information Variety,
    IA=Inference Accountability, IInteg=Intelligence Integrity
    """
    state = EducationState(
        GT=0.8, IV=0.6, IA=0.9, IInteg=0.7
    )
    
    assert state.GT == 0.8
    assert state.IV == 0.6
    assert state.IA == 0.9
    assert state.IInteg == 0.7
    
    x = state.to_potential_vector()
    assert np.allclose(x, [0.8, 0.6, 0.9, 0.7])
    
    state.update_from_potential_vector(np.array([0.5, 0.4, 0.6, 0.3]))
    assert state.GT == 0.5
    assert state.IV == 0.4
    assert state.IA == 0.6
    assert state.IInteg == 0.3


def test_education_state_clipping():
    """Test that EducationState clips values to [0, 1]."""
    state = EducationState(
        GT=-0.1, IV=1.5, IA=0.5, IInteg=0.5
    )
    
    assert 0.0 <= state.GT <= 1.0
    assert 0.0 <= state.IV <= 1.0
    assert state.IV == 1.0  # Clipped from 1.5

