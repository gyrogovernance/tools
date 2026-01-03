"""
Tests for validation module
"""

import sys
from pathlib import Path

import pytest

# Add research/prevention to path to allow importing compass package
test_file = Path(__file__).absolute()
compass_dir = test_file.parent.parent
prevention_dir = compass_dir.parent

prevention_path = str(prevention_dir)
if prevention_path not in sys.path:
    sys.path.insert(0, prevention_path)

from compass.validation import validate_egress_packet, ValidationError, validate_and_raise


def _base_packet(packet_id: str):
    return {
        "id": packet_id,
        "timestamp": "2024-01-01T00:00:00Z",
        "use_case": "support_center",
        "scope": "Test scope",
        "receiving_point": {"role": "coordinator", "channel": "main"},
    }


def test_valid_packet_with_displacement():
    packet = _base_packet("test-001")
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}

    errors = validate_egress_packet(packet)
    assert errors == []


def test_valid_packet_with_potentials():
    packet = _base_packet("test-002")
    packet["use_case"] = "fund_allocation"
    packet["receiving_point"] = {"role": "analyst", "channel": "secondary"}
    packet["potentials"] = {
        "economy": {"Gov": 0.5, "Info": 0.3, "Infer": 0.15, "Int": 0.05},
        "employment": {"GM": 0.4, "ICu": 0.3, "IInter": 0.2, "ICo": 0.1},
        "education": {"GMT": 0.45, "ICV": 0.25, "IIA": 0.2, "ICI": 0.1},
    }

    errors = validate_egress_packet(packet)
    assert errors == []


def test_missing_required_field():
    packet = {
        "id": "test-003",
        "timestamp": "2024-01-01T00:00:00Z",
        "use_case": "support_center",
        "scope": "Test scope",
        "displacement_estimate": {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1},
    }

    errors = validate_egress_packet(packet)
    assert any("receiving_point" in err for err in errors)


def test_both_displacement_and_potentials():
    packet = _base_packet("test-004")
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}
    packet["potentials"] = {"economy": {"Gov": 0.5, "Info": 0.3, "Infer": 0.15, "Int": 0.05}}

    errors = validate_egress_packet(packet)
    assert any("both" in err.lower() for err in errors)


def test_validate_and_raise():
    # Provide a packet that fails for a single clear reason
    packet = _base_packet("test-005")
    del packet["receiving_point"]  # Missing required field
    with pytest.raises(ValidationError) as exc_info:
        validate_and_raise(packet)
    assert "receiving_point" in str(exc_info.value)


def test_use_case_is_free_string_identifier():
    packet = _base_packet("test-006")
    packet["use_case"] = "some_new_use_case_identifier"
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}

    errors = validate_egress_packet(packet)
    assert errors == []


def test_patterns_validation():
    packet = _base_packet("test-007")
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}
    packet["patterns"] = ["pattern1", "pattern2"]

    assert validate_egress_packet(packet) == []

    packet["patterns"] = "not a list"
    errors = validate_egress_packet(packet)
    assert any("patterns must be a list" in err for err in errors)

    packet["patterns"] = ["valid", 123, "also valid"]
    errors = validate_egress_packet(packet)
    assert any("patterns[1] must be a string" in err for err in errors)


def test_session_id_empty_string_rejected():
    packet = _base_packet("test-008")
    packet["session_id"] = ""
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}

    errors = validate_egress_packet(packet)
    assert any("session_id" in err for err in errors)


def test_config_measurement_noise_validation():
    packet = _base_packet("test-009")
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}

    packet["config"] = {"measurement_noise": 0.0}
    errors = validate_egress_packet(packet)
    assert any("measurement_noise" in err for err in errors)

    packet["config"] = {"measurement_noise": 1.1}
    errors = validate_egress_packet(packet)
    assert any("measurement_noise" in err for err in errors)


def test_observations_validation():
    packet = _base_packet("test-010")
    packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}
    packet["observations"] = [{"maps_to": "GTD", "value": 0.4, "noise": 0.02}]
    assert validate_egress_packet(packet) == []

    packet["observations"] = [{"maps_to": "BAD", "value": 0.4, "noise": 0.02}]
    errors = validate_egress_packet(packet)
    assert any("maps_to" in err for err in errors)

    packet["observations"] = [{"maps_to": "GTD", "value": 1.5, "noise": 0.02}]
    errors = validate_egress_packet(packet)
    assert any("value" in err.lower() for err in errors)

    packet["observations"] = [{"maps_to": "GTD", "value": 0.4, "noise": 0.0}]
    errors = validate_egress_packet(packet)
    assert any("noise" in err for err in errors)
