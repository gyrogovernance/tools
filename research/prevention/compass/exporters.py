"""
Exporters Module: CSV and JSON Output

Provides functions to export Compass readings to CSV and JSON formats.
"""

import json
import csv
from typing import Dict, Any, List, Optional
from pathlib import Path


def get_results_dir() -> Path:
    """
    Get the results directory path within the compass module.
    
    Returns:
        Path to the results directory (created if it doesn't exist).
    """
    # Get the directory containing this file (compass/)
    compass_dir = Path(__file__).parent
    results_dir = compass_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def get_output_path(filename: str, subdirectory: Optional[str] = None) -> Path:
    """
    Get a path within the results directory for output files.
    
    Args:
        filename: Name of the output file (e.g., "readings.csv", "session_001.json").
        subdirectory: Optional subdirectory within results (e.g., "sessions", "batch").
    
    Returns:
        Full path to the output file (parent directories created if needed).
    """
    results_dir = get_results_dir()
    
    if subdirectory:
        output_dir = results_dir / subdirectory
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = results_dir
    
    return output_dir / filename


def export_reading_json(
    reading: Dict[str, Any],
    filepath: str,
    indent: int = 2
) -> None:
    """
    Export a single reading to JSON file.
    
    Args:
        reading: Compass reading dictionary.
        filepath: Output file path.
        indent: JSON indentation.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(reading, f, indent=indent, ensure_ascii=False)


def export_readings_json(
    readings: List[Dict[str, Any]],
    filepath: str,
    indent: int = 2
) -> None:
    """
    Export multiple readings to JSON file (array format).
    
    Args:
        readings: List of Compass reading dictionaries.
        filepath: Output file path.
        indent: JSON indentation.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(readings, f, indent=indent, ensure_ascii=False)


def export_reading_csv(
    reading: Dict[str, Any],
    filepath: str,
    append: bool = False
) -> None:
    """
    Export a single reading to CSV file.
    
    Args:
        reading: Compass reading dictionary.
        filepath: Output file path.
        append: If True, append to existing file.
    """
    # Flatten reading structure for CSV
    row = {
        "egress_id": reading.get("egress_id", ""),
        "timestamp": reading.get("timestamp", ""),
        "use_case": reading.get("use_case", ""),
        "receiving_point_role": reading.get("receiving_point", {}).get("role", ""),
        "receiving_point_channel": reading.get("receiving_point", {}).get("channel", ""),
    }
    
    # Displacement components
    ledger = reading.get("ledger", {})
    disp = ledger.get("displacement", {})
    row["GTD"] = disp.get("GTD", "")
    row["IVD"] = disp.get("IVD", "")
    row["IAD"] = disp.get("IAD", "")
    row["IID"] = disp.get("IID", "")
    dominant = disp.get("dominant", "")
    row["dominant"] = dominant
    
    # Uncertainty
    uncertainty = ledger.get("uncertainty", {})
    intervals = uncertainty.get("intervals", {})
    for comp in ["GTD", "IVD", "IAD", "IID"]:
        if comp in intervals:
            # Intervals are now lists [lower, upper]
            interval_list = intervals[comp]
            if isinstance(interval_list, list) and len(interval_list) >= 2:
                row[f"{comp}_lower"] = interval_list[0]
                row[f"{comp}_upper"] = interval_list[1]
            else:
                row[f"{comp}_lower"] = ""
                row[f"{comp}_upper"] = ""
        else:
            row[f"{comp}_lower"] = ""
            row[f"{comp}_upper"] = ""
    
    row["route_stability"] = uncertainty.get("route_stability", "")
    row["samples"] = uncertainty.get("samples", "")
    
    # Routing (now at top level per spec)
    routing = reading.get("routing", {})
    row["routing_mode"] = routing.get("mode", "")
    row["route_to"] = routing.get("route_to") or ""
    row["low_stability_action"] = routing.get("low_stability_action") or ""
    
    # SI
    si = ledger.get("si", {})
    row["SI_economy"] = si.get("economy", "")
    row["SI_employment"] = si.get("employment", "")
    row["SI_education"] = si.get("education", "")
    
    # Employment normalized flag
    row["employment_normalized"] = ledger.get("employment_normalized", False)

    # Work category derived from routing.route_to (may be empty in unstable mode)
    row["work_category"] = routing.get("route_to", "") or ""
    
    # Write CSV
    file_exists = Path(filepath).exists()
    mode = 'a' if append else 'w'
    fieldnames = [
        "egress_id", "timestamp", "use_case",
        "receiving_point_role", "receiving_point_channel",
        "GTD", "IVD", "IAD", "IID",
        "GTD_lower", "GTD_upper",
        "IVD_lower", "IVD_upper",
        "IAD_lower", "IAD_upper",
        "IID_lower", "IID_upper",
        "dominant", "work_category",
        "route_stability", "samples",
        "routing_mode", "route_to", "low_stability_action",
        "SI_economy", "SI_employment", "SI_education",
        "employment_normalized"
    ]
    
    with open(filepath, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if (not append) or (not file_exists):
            writer.writeheader()
        writer.writerow(row)


def export_readings_csv(
    readings: List[Dict[str, Any]],
    filepath: str
) -> None:
    """
    Export multiple readings to CSV file.
    
    Args:
        readings: List of Compass reading dictionaries.
        filepath: Output file path.
    """
    # Write header on first call
    for i, reading in enumerate(readings):
        export_reading_csv(reading, filepath, append=(i > 0))


def export_readings_ndjson(
    readings: List[Dict[str, Any]],
    filepath: str
) -> None:
    """
    Export multiple readings to newline-delimited JSON (NDJSON) file.
    
    Args:
        readings: List of Compass reading dictionaries.
        filepath: Output file path.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for reading in readings:
            json.dump(reading, f, ensure_ascii=False)
            f.write('\n')

