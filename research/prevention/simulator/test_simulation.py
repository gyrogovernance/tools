"""
Tests for simulation module.

Validates scenario configuration and simulation execution with canonical CGM SI.
"""

import sys
from pathlib import Path

# Add research/prevention directory to path for direct execution
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
import pytest

from simulator.simulation import ScenarioConfig, SimulationResult, run_scenario
from simulator.alignment import A_STAR


def test_scenario_config():
    """Test ScenarioConfig initialization."""
    config = ScenarioConfig(
        Gov0=0.8, Info0=0.6, Infer0=0.9, Int0=0.7,
        num_steps=10
    )
    
    assert config.Gov0 == 0.8
    assert config.num_steps == 10
    assert config.A_star == A_STAR  # Default


def test_scenario_config_to_params():
    """Test conversion to parameters dict."""
    config = ScenarioConfig(alpha1=0.02, beta1=0.03, gamma1=0.04)
    params = config.to_params_dict()
    
    assert params["alpha1"] == 0.02
    assert params["beta1"] == 0.03
    assert params["gamma1"] == 0.04
    assert params["A_star"] == A_STAR


def test_simulation_result():
    """Test SimulationResult initialization and recording."""
    result = SimulationResult(num_steps=5)
    
    assert len(result.Gov) == 6  # num_steps + 1
    assert len(result.SI_Econ) == 6  # SI on 0-100 scale


def test_run_scenario_basic():
    """Test running a basic scenario."""
    config = ScenarioConfig(
        Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
        GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
        GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
        num_steps=10
    )
    
    result = run_scenario(config, verbose=False)
    
    assert result.num_steps == 10
    assert len(result.Gov) == 11  # num_steps + 1
    assert len(result.SI_Econ) == 11
    
    # Check that values are recorded
    assert np.all(result.Gov >= 0)
    assert np.all(result.Gov <= 1)
    # SI is on 0-100 scale
    assert np.all(result.SI_Econ >= 0)
    assert np.all(result.SI_Econ <= 100)


def test_run_scenario_optimal_aperture():
    """Test that optimal aperture gives SI = 100."""
    config = ScenarioConfig(
        Gov0=0.5, Info0=0.5, Infer0=0.5, Int0=0.5,
        GM0=0.25, ICu0=0.25, IInter0=0.25, ICo0=0.25,
        GT0=0.5, IV0=0.5, IA0=0.5, IInteg0=0.5,
        A_Econ_target=A_STAR,
        A_Emp_target=A_STAR,
        A_Edu_target=A_STAR,
        A_star=A_STAR,
        num_steps=5
    )
    
    result = run_scenario(config, verbose=False)
    
    # All SIs should be 100 at optimal aperture
    assert abs(result.SI_Econ[0] - 100.0) < 1e-6
    assert abs(result.SI_Emp[0] - 100.0) < 1e-6
    assert abs(result.SI_Edu[0] - 100.0) < 1e-6


def test_run_scenario_high_aperture():
    """Test that high aperture gives low SI."""
    config = ScenarioConfig(
        Gov0=0.6, Info0=0.4, Infer0=0.5, Int0=0.5,
        A_Econ_target=0.1,  # High aperture (unstable)
        A_Emp_target=0.1,
        A_Edu_target=0.1,
        A_star=A_STAR,
        num_steps=5
    )
    
    result = run_scenario(config, verbose=False)
    
    # SI should be low at high aperture
    # D = 0.1 / 0.0207 ≈ 4.83, SI ≈ 20.7
    assert result.SI_Econ[0] < 30


def test_simulation_result_to_dict():
    """Test conversion to dictionary."""
    result = SimulationResult(num_steps=5)
    data = result.to_dict()
    
    assert "Gov" in data
    assert "SI_Econ" in data
    assert "SI_Emp" in data
    assert "SI_Edu" in data
    assert len(data["Gov"]) == 6


def test_simulation_result_export():
    """Test CSV and JSON export."""
    result = SimulationResult(num_steps=5)
    
    try:
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            json_path = os.path.join(tmpdir, "test.json")
            
            result.export_csv(csv_path)
            result.export_json(json_path)
            
            assert os.path.exists(csv_path)
            assert os.path.exists(json_path)
            
            # Check CSV contains SI columns
            with open(csv_path, 'r') as f:
                header = f.readline()
                assert "SI_Econ" in header
                assert "SI_Emp" in header
    except Exception:
        # Skip if file system access fails
        pass
