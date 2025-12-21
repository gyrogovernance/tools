"""
Compass Scenario Runner

Executes the 5 validation scenarios defined in Section 10 of the Compass specification.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add research/prevention to path
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from compass import (
    CompassEngine,
    get_output_path,
    export_reading_json,
    export_readings_json
)


# ==========
# SCENARIO DEFINITIONS (from Section 10 of spec)
# ==========

def create_scenario_packets() -> List[Dict[str, Any]]:
    """Create scenario packets exactly as specified in Section 10."""
    
    base_timestamp = "2024-01-01T00:00:00Z"
    scenarios = []
    
    # Scenario 1: Active Routing
    scenarios.append({
        "name": "scenario_1_active_routing",
        "description": "Active routing mode - GTD dominant",
        "packet": {
            "id": "EGR-001",
            "timestamp": base_timestamp,
            "use_case": "support_center",
            "scope": "Active routing test",
            "receiving_point": {"role": "Deployment reviewer", "channel": "ticket://ops/8841"},
            "config": {"measurement_noise": 0.05},
            "displacement_estimate": {
                "GTD": 0.30,
                "IVD": 0.20,
                "IAD": 0.25,
                "IID": 0.15
            }
        }
    })
    
    # Scenario 2: Computed from Potentials
    scenarios.append({
        "name": "scenario_2_computed_from_potentials",
        "description": "Displacement computed from potentials",
        "packet": {
            "id": "EGR-002",
            "timestamp": base_timestamp,
            "use_case": "fund_allocation",
            "scope": "Computed displacement test",
            "receiving_point": {"role": "Analyst", "channel": "main"},
            "potentials": {
                "economy": {"Gov": 0.60, "Info": 0.55, "Infer": 0.50, "Int": 0.58},
                "employment": {"GM": 0.25, "ICu": 0.25, "IInter": 0.25, "ICo": 0.25},
                "education": {"GT": 0.55, "IV": 0.50, "IA": 0.52, "IInteg": 0.60}
            }
        }
    })
    
    # Scenario 3: Unstable Routing
    scenarios.append({
        "name": "scenario_3_unstable_routing",
        "description": "Unstable routing due to high noise",
        "packet": {
            "id": "EGR-003",
            "timestamp": base_timestamp,
            "use_case": "support_center",
            "scope": "Unstable routing test",
            "receiving_point": {"role": "Coordinator", "channel": "main"},
            "config": {"measurement_noise": 0.20},
            "displacement_estimate": {
                "GTD": 0.27,
                "IVD": 0.26,
                "IAD": 0.25,
                "IID": 0.24
            }
        }
    })
    
    # Scenario 4: Session Continuity (two packets in the same session)
    scenarios.append({
        "name": "scenario_4_session_continuity",
        "description": "Two packets in the same session to test continuity",
        "packets": [
            {
                "id": "PKT-001",
                "session_id": "SES-A",
                "timestamp": base_timestamp,
                "use_case": "support_center",
                "scope": "Session continuity test (packet 1)",
                "receiving_point": {"role": "Coordinator", "channel": "main"},
                "displacement_estimate": {
                    "GTD": 0.30,
                    "IVD": 0.20,
                    "IAD": 0.25,
                    "IID": 0.15
                }
            },
            {
                "id": "PKT-002",
                "session_id": "SES-A",
                "timestamp": base_timestamp,
                "use_case": "support_center",
                "scope": "Session continuity test (packet 2)",
                "receiving_point": {"role": "Coordinator", "channel": "main"},
                "displacement_estimate": {
                    "GTD": 0.28,
                    "IVD": 0.22,
                    "IAD": 0.24,
                    "IID": 0.16
                }
            }
        ]
    })
    
    # Scenario 5: Determinism Test
    scenarios.append({
        "name": "scenario_5_determinism",
        "description": "Determinism test with fixed session and egress IDs",
        "packet": {
            "id": "DET-001",
            "session_id": "DET-SESSION",
            "timestamp": base_timestamp,
            "use_case": "support_center",
            "scope": "Determinism test",
            "receiving_point": {"role": "Coordinator", "channel": "main"},
            "config": {"measurement_noise": 0.05},
            "displacement_estimate": {
                "GTD": 0.35,
                "IVD": 0.22,
                "IAD": 0.28,
                "IID": 0.18
            }
        }
    })
    
    return scenarios


# ==========
# ANALYSIS AND OUTPUT
# ==========

def print_scenario_summary(scenario_name: str, reading: Dict[str, Any]):
    """Print informative summary for a scenario."""
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"{'='*60}")
    
    # Routing info
    routing = reading.get("routing", {})
    print(f"Routing Mode: {routing.get('mode', 'N/A')}")
    print(f"Route To: {routing.get('route_to', 'N/A')}")
    if routing.get('work_indicated'):
        print(f"Work Indicated: {routing.get('work_indicated')}")
    
    # Displacement
    ledger = reading.get("ledger", {})
    disp = ledger.get("displacement", {})
    print(f"\nDisplacement (posterior means):")
    print(f"  GTD: {disp.get('GTD', 0):.4f}")
    print(f"  IVD: {disp.get('IVD', 0):.4f}")
    print(f"  IAD: {disp.get('IAD', 0):.4f}")
    print(f"  IID: {disp.get('IID', 0):.4f}")
    print(f"  Dominant: {disp.get('dominant', 'N/A')}")
    
    # Source
    source = ledger.get("source", "N/A")
    print(f"\nSource: {source}")
    
    # Observed field
    if "observed" in ledger:
        print(f"Observed: {ledger['observed']}")
    
    # Uncertainty
    uncertainty = ledger.get("uncertainty", {})
    stability = uncertainty.get("route_stability", 0)
    print(f"\nUncertainty:")
    print(f"  Route Stability: {stability:.4f}")
    print(f"  MC Samples: {uncertainty.get('samples', 0)}")
    
    # SI
    si = ledger.get("si", {})
    print(f"\nSuperintelligence Index:")
    print(f"  Economy: {si.get('economy', 0):.2f}")
    print(f"  Employment: {si.get('employment', 0):.2f}")
    print(f"  Education: {si.get('education', 0):.2f}")
    
    # Employment normalization
    if "employment_normalized" in ledger:
        print(f"\nEmployment Normalized: {ledger['employment_normalized']}")


def print_overall_summary(all_readings: List[Dict[str, Any]]):
    """Print overall summary statistics."""
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    
    routing_modes = {}
    dominant_components = {}
    work_categories = {}
    sources = {}
    
    for reading in all_readings:
        # Routing modes
        mode = reading.get("routing", {}).get("mode", "unknown")
        routing_modes[mode] = routing_modes.get(mode, 0) + 1
        
        # Dominant components
        disp = reading.get("ledger", {}).get("displacement", {})
        dominant = disp.get("dominant", "unknown")
        dominant_components[dominant] = dominant_components.get(dominant, 0) + 1
        
        # Work categories (derived from dominant)
        work_cat_map = {"GTD": "GM", "IVD": "ICu", "IAD": "IInter", "IID": "ICo"}
        work_cat = work_cat_map.get(dominant, "unknown")
        work_categories[work_cat] = work_categories.get(work_cat, 0) + 1
        
        # Sources
        source = reading.get("ledger", {}).get("source", "unknown")
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\nTotal Scenarios: {len(all_readings)}")
    
    print(f"\nRouting Mode Distribution:")
    for mode, count in sorted(routing_modes.items()):
        print(f"  {mode}: {count}")
    
    print(f"\nDominant Component Distribution:")
    for comp, count in sorted(dominant_components.items()):
        print(f"  {comp}: {count}")
    
    print(f"\nWork Category Distribution:")
    for cat, count in sorted(work_categories.items()):
        print(f"  {cat}: {count}")
    
    print(f"\nSource Distribution:")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count}")
    
    # Average stability
    stabilities = [
        r.get("ledger", {}).get("uncertainty", {}).get("route_stability", 0)
        for r in all_readings
    ]
    if stabilities:
        avg_stability = sum(stabilities) / len(stabilities)
        print(f"\nAverage Route Stability: {avg_stability:.4f}")


# ==========
# MAIN RUNNER
# ==========

def main():
    """Run all scenarios and produce outputs."""
    print("="*60)
    print("GYROSCOPIC COMPASS - SCENARIO RUNNER (Section 10)")
    print("="*60)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    
    # Initialize engine
    engine = CompassEngine()
    print("Compass Engine initialized")
    print(f"  Maintenance Threshold: {engine.maintenance_threshold}")
    print(f"  Min Route Stability: {engine.min_route_stability}")
    print(f"  MC Samples: {engine.mc_samples}")
    print()
    
    # Get scenarios
    scenarios = create_scenario_packets()
    print(f"Loaded {len(scenarios)} scenarios from specification")
    print()
    
    # Process scenarios
    all_readings = []
    session_engines = {}  # Track engines per session
    
    for i, scenario in enumerate(scenarios, 1):
        scenario_name = scenario["name"]
        
        # Some scenarios (e.g., session continuity) contain multiple packets
        packets = scenario.get("packets")
        if packets is None:
            packets = [scenario["packet"]]
        
        for j, packet in enumerate(packets, 1):
            name_with_index = scenario_name if len(packets) == 1 else f"{scenario_name}_pkt{j}"
            
            # Get or create engine for session
            session_id = packet.get("session_id")
            if session_id:
                if session_id not in session_engines:
                    session_engines[session_id] = CompassEngine()
                current_engine = session_engines[session_id]
            else:
                current_engine = engine
            
            # Process packet
            try:
                reading = current_engine.process_egress_packet(packet)
                all_readings.append(reading)
                
                # Print summary
                print_scenario_summary(name_with_index, reading)
            
            except Exception as e:
                print(f"\nERROR in scenario {name_with_index}: {e}")
                import traceback
                traceback.print_exc()
    
    # Print overall summary
    print_overall_summary(all_readings)
    
    # Export outputs
    print(f"\n{'='*60}")
    print("EXPORTING OUTPUTS")
    print(f"{'='*60}")
    
    output_dir = get_output_path("", "scenarios")
    
    # Individual JSON files (one per reading)
    for idx, reading in enumerate(all_readings, 1):
        filename = f"scenario_{idx}.json"
        filepath = get_output_path(filename, "scenarios")
        export_reading_json(reading, str(filepath))
        print(f"  Exported: {filename}")
    
    # Combined JSON array
    combined_json_path = get_output_path("all_scenarios.json", "scenarios")
    export_readings_json(all_readings, str(combined_json_path))
    print(f"  Exported: all_scenarios.json")
    
    print(f"\nAll outputs saved to: {output_dir}")
    print(f"Completed: {datetime.now().isoformat()}")
    print("="*60)


if __name__ == "__main__":
    main()
