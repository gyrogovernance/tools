"""
Tests for CompassEngine
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

from compass import CompassEngine


def _base_packet(packet_id: str, use_case: str = "support_center"):
    return {
        "id": packet_id,
        "timestamp": "2024-01-01T00:00:00Z",
        "use_case": use_case,
        "scope": "Test scope",
        "receiving_point": {"role": "coordinator", "channel": "main"},
    }


class TestCompassEngine:
    def test_basic_displacement_processing(self):
        engine = CompassEngine()

        packet = _base_packet("test-001")
        packet["config"] = {"measurement_noise": 0.05}
        packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}

        reading = engine.process_egress_packet(packet)

        # Top-level structure
        assert reading["egress_id"] == "test-001"
        assert reading["use_case"] == "support_center"
        assert reading["receiving_point"]["status"] == "delivered"
        assert "routing" in reading
        assert "ledger" in reading
        assert "patterns" in reading

        # Ledger structure
        ledger = reading["ledger"]
        assert ledger["source"] == "provided"
        assert "observed" in ledger
        assert ledger["observed"] == packet["displacement_estimate"]

        # Displacement posterior present
        disp = ledger["displacement"]
        for k in ["GTD", "IVD", "IAD", "IID", "dominant"]:
            assert k in disp

        # Uncertainty structure
        unc = ledger["uncertainty"]
        assert "intervals" in unc
        assert "route_stability" in unc
        assert "samples" in unc
        for comp in ["GTD", "IVD", "IAD", "IID"]:
            lo, hi = unc["intervals"][comp]
            assert 0.0 <= lo <= hi <= 1.0

        # SI present
        si = ledger["si"]
        for dom in ["economy", "employment", "education"]:
            assert dom in si
            assert 0.0 <= si[dom] <= 100.0

    def test_potentials_processing(self):
        engine = CompassEngine()

        packet = _base_packet("test-002", use_case="fund_allocation")
        packet["receiving_point"] = {"role": "analyst", "channel": "secondary"}
        packet["config"] = {"measurement_noise": 0.05}
        packet["potentials"] = {
            "economy": {"Gov": 0.5, "Info": 0.3, "Infer": 0.15, "Int": 0.05},
            "employment": {"GM": 0.4, "ICu": 0.3, "IInter": 0.2, "ICo": 0.1},  # sums to 1
            "education": {"GT": 0.45, "IV": 0.25, "IA": 0.2, "IInteg": 0.1},
        }

        reading = engine.process_egress_packet(packet)

        assert reading["ledger"]["source"] == "computed"
        assert "observed" not in reading["ledger"]
        assert reading["ledger"]["employment_normalized"] is False

    def test_employment_normalization_flag(self):
        engine = CompassEngine()

        packet = _base_packet("test-003")
        packet["config"] = {"measurement_noise": 0.05}
        packet["potentials"] = {
            "economy": {"Gov": 0.5, "Info": 0.3, "Infer": 0.15, "Int": 0.05},
            "employment": {"GM": 0.5, "ICu": 0.4, "IInter": 0.3, "ICo": 0.2},  # Sum = 1.4
            "education": {"GT": 0.45, "IV": 0.25, "IA": 0.2, "IInteg": 0.1},
        }

        reading = engine.process_egress_packet(packet)
        assert reading["ledger"]["employment_normalized"] is True

    def test_session_scoping(self):
        engine = CompassEngine()

        packet1 = _base_packet("test-s1-001")
        packet1["session_id"] = "session-1"
        packet1["config"] = {"measurement_noise": 0.05}
        packet1["displacement_estimate"] = {"GTD": 0.8, "IVD": 0.1, "IAD": 0.05, "IID": 0.05}
        reading1 = engine.process_egress_packet(packet1)

        packet2 = _base_packet("test-s2-001")
        packet2["session_id"] = "session-2"
        packet2["config"] = {"measurement_noise": 0.05}
        packet2["displacement_estimate"] = {"GTD": 0.1, "IVD": 0.8, "IAD": 0.05, "IID": 0.05}
        reading2 = engine.process_egress_packet(packet2)

        assert reading1["ledger"]["displacement"]["dominant"] == "GTD"
        assert reading2["ledger"]["displacement"]["dominant"] == "IVD"

    def test_stateless_packets(self):
        engine = CompassEngine()

        packet1 = _base_packet("test-stateless-001")
        packet1["config"] = {"measurement_noise": 0.05}
        packet1["displacement_estimate"] = {"GTD": 0.8, "IVD": 0.1, "IAD": 0.05, "IID": 0.05}

        packet2 = _base_packet("test-stateless-002")
        packet2["config"] = {"measurement_noise": 0.05}
        packet2["displacement_estimate"] = {"GTD": 0.1, "IVD": 0.8, "IAD": 0.05, "IID": 0.05}

        reading1 = engine.process_egress_packet(packet1)
        reading2 = engine.process_egress_packet(packet2)

        assert reading1["ledger"]["displacement"]["dominant"] == "GTD"
        assert reading2["ledger"]["displacement"]["dominant"] == "IVD"

    def test_session_continuity_updates_posterior(self):
        engine = CompassEngine()

        pkt1 = _base_packet("cont-001")
        pkt1["session_id"] = "SES-CONT"
        pkt1["config"] = {"measurement_noise": 0.05}
        pkt1["displacement_estimate"] = {"GTD": 0.30, "IVD": 0.20, "IAD": 0.25, "IID": 0.15}
        r1 = engine.process_egress_packet(pkt1)

        pkt2 = _base_packet("cont-002")
        pkt2["session_id"] = "SES-CONT"
        pkt2["config"] = {"measurement_noise": 0.05}
        pkt2["displacement_estimate"] = {"GTD": 0.28, "IVD": 0.22, "IAD": 0.24, "IID": 0.16}
        r2 = engine.process_egress_packet(pkt2)

        # Compare with stateless processing of pkt2 (fresh engine)
        engine_stateless = CompassEngine()
        pkt2_stateless = _base_packet("cont-002-stateless")
        pkt2_stateless["config"] = {"measurement_noise": 0.05}
        pkt2_stateless["displacement_estimate"] = pkt2["displacement_estimate"]
        r2_stateless = engine_stateless.process_egress_packet(pkt2_stateless)

        d2 = r2["ledger"]["displacement"]
        d2s = r2_stateless["ledger"]["displacement"]

        # At least one posterior mean should differ due to session memory
        diffs = [abs(d2[k] - d2s[k]) for k in ["GTD", "IVD", "IAD", "IID"]]
        assert any(delta > 1e-9 for delta in diffs)

    def test_routing_modes(self):
        # Active mode (clear dominant + low noise)
        engine_active = CompassEngine()
        packet_active = _base_packet("test-routing-active")
        packet_active["config"] = {"measurement_noise": 0.05}
        packet_active["displacement_estimate"] = {"GTD": 0.8, "IVD": 0.1, "IAD": 0.05, "IID": 0.05}

        reading_active = engine_active.process_egress_packet(packet_active)
        assert reading_active["routing"]["mode"] == "active"
        assert reading_active["routing"]["route_to"] == "GM"

        # Maintenance mode (all below maintenance threshold after posterior update)
        # Use minimum measurement_noise (0.01) to make posterior track small observations
        # rather than being biased upward by uniform Beta(1,1) prior
        engine_maint = CompassEngine()
        packet_maint = _base_packet("test-routing-maint")
        packet_maint["config"] = {"measurement_noise": 0.01}  # minimum clamp
        packet_maint["displacement_estimate"] = {"GTD": 0.05, "IVD": 0.04, "IAD": 0.03, "IID": 0.02}

        reading_maint = engine_maint.process_egress_packet(packet_maint)
        assert reading_maint["routing"]["mode"] == "maintenance"
        assert reading_maint["routing"]["route_to"] in ["GM", "ICu", "IInter", "ICo"]

        # Unstable mode (close values + high noise should reduce stability deterministically)
        engine_unstable = CompassEngine()
        packet_unstable = _base_packet("test-routing-unstable")
        packet_unstable["config"] = {"measurement_noise": 0.20}
        packet_unstable["displacement_estimate"] = {"GTD": 0.27, "IVD": 0.26, "IAD": 0.25, "IID": 0.24}

        reading_unstable = engine_unstable.process_egress_packet(packet_unstable)
        stability = reading_unstable["ledger"]["uncertainty"]["route_stability"]

        assert stability < engine_unstable.min_route_stability
        assert reading_unstable["routing"]["mode"] == "unstable"
        assert reading_unstable["routing"]["route_to"] is None
        assert reading_unstable["routing"]["low_stability_action"] == "ICu"

    def test_observations_functionality(self):
        engine = CompassEngine()

        packet = _base_packet("test-obs-001")
        packet["config"] = {"measurement_noise": 0.05}
        packet["displacement_estimate"] = {"GTD": 0.2, "IVD": 0.15, "IAD": 0.3, "IID": 0.1}
        packet["observations"] = [
            {"maps_to": "GTD", "value": 0.4, "noise": 0.02},
            {"maps_to": "IAD", "value": 0.2, "noise": 0.03},
        ]

        reading = engine.process_egress_packet(packet)
        disp = reading["ledger"]["displacement"]

        assert disp["GTD"] > 0.25
        assert disp["IAD"] < 0.25

    def test_spec_determinism_scenario(self):
        """
        Determinism + numeric expectations from the spec determinism scenario:
        - Posterior means to 4 decimals
        - Route stability to 3 decimals
        """
        engine1 = CompassEngine()
        engine2 = CompassEngine()

        packet = _base_packet("DET-001")
        packet["session_id"] = "DET-SESSION"
        packet["use_case"] = "support_center"
        packet["config"] = {"measurement_noise": 0.05}
        packet["displacement_estimate"] = {
            "GTD": 0.35,
            "IVD": 0.22,
            "IAD": 0.28,
            "IID": 0.18,
        }

        reading1 = engine1.process_egress_packet(packet)
        reading2 = engine2.process_egress_packet(packet)

        # Full determinism (same input -> identical output dict sections)
        assert reading1["ledger"]["displacement"] == reading2["ledger"]["displacement"]
        assert reading1["ledger"]["uncertainty"]["route_stability"] == reading2["ledger"]["uncertainty"]["route_stability"]
        assert reading1["routing"] == reading2["routing"]

        disp = reading1["ledger"]["displacement"]
        assert disp["dominant"] == "GTD"
        assert reading1["routing"]["mode"] == "active"
        assert reading1["routing"]["route_to"] == "GM"

        # Posterior means (approx to 4 decimals)
        assert disp["GTD"] == pytest.approx(0.3532, abs=5e-4)
        assert disp["IVD"] == pytest.approx(0.2278, abs=5e-4)
        assert disp["IAD"] == pytest.approx(0.2851, abs=5e-4)
        assert disp["IID"] == pytest.approx(0.1905, abs=5e-4)

        # Route stability (approx to 3 decimals)
        # With explicit PCG64(seed) and deterministic tie-breaking, route stability should match spec
        assert reading1["ledger"]["uncertainty"]["route_stability"] == pytest.approx(0.804, abs=5e-4)
