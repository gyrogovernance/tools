"""
Gyroscopic Compass: Coordination tool for balance maintenance.

The Compass produces standardized readings from incomplete and noisy inputs,
identifying displacement patterns and routing corrective work.
"""

from .engine import CompassEngine
from .validation import ValidationError, validate_egress_packet, validate_and_raise
from .filter import DisplacementFilter, generate_deterministic_seed
from .exporters import (
    export_reading_json, export_readings_json,
    export_reading_csv, export_readings_csv,
    export_readings_ndjson,
    get_results_dir, get_output_path
)

__version__ = "1.0"

__all__ = [
    "CompassEngine",
    "ValidationError",
    "validate_egress_packet",
    "validate_and_raise",
    "DisplacementFilter",
    "generate_deterministic_seed",
    "export_reading_json",
    "export_readings_json",
    "export_reading_csv",
    "export_readings_csv",
    "export_readings_ndjson",
    "get_results_dir",
    "get_output_path"
]

