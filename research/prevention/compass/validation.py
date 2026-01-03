"""
Validation Module for Gyroscopic Compass

Validates egress packets according to the Compass specification.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


class ValidationError(Exception):
    """Raised when packet validation fails."""
    pass


def validate_egress_packet(packet: Dict[str, Any]) -> List[str]:
    """
    Validates an egress packet and returns a list of errors.
    
    Args:
        packet: Egress packet dictionary.
    
    Returns:
        List of error messages (empty if valid).
    """
    errors = []
    
    # Required fields
    required_fields = [
        "id",
        "timestamp",
        "use_case",
        "scope",
        "receiving_point"
    ]
    
    for field in required_fields:
        if field not in packet:
            errors.append(f"Missing required field: {field}")
    
    # Validate receiving_point structure
    if "receiving_point" in packet:
        rp = packet["receiving_point"]
        if not isinstance(rp, dict):
            errors.append("receiving_point must be a dictionary")
        else:
            if "role" not in rp:
                errors.append("receiving_point.role is required")
            if "channel" not in rp:
                errors.append("receiving_point.channel is required")
    
    # Validate timestamp format (ISO 8601)
    if "timestamp" in packet:
        try:
            datetime.fromisoformat(packet["timestamp"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            errors.append("timestamp must be valid ISO 8601 format")
    
    # Validate exactly-one-of rule: displacement_estimate or complete potentials
    has_displacement = "displacement_estimate" in packet
    has_potentials = "potentials" in packet
    
    if not has_displacement and not has_potentials:
        errors.append("Exactly one of 'displacement_estimate' or 'potentials' must be provided")
    elif has_displacement and has_potentials:
        errors.append("Cannot provide both 'displacement_estimate' and 'potentials'")
    
    # Validate displacement_estimate if provided
    if has_displacement:
        de = packet["displacement_estimate"]
        if not isinstance(de, dict):
            errors.append("displacement_estimate must be a dictionary")
        else:
            required_disp = ["GTD", "IVD", "IAD", "IID"]
            for comp in required_disp:
                if comp not in de:
                    errors.append(f"displacement_estimate missing component: {comp}")
                else:
                    val = de[comp]
                    if not isinstance(val, (int, float)):
                        errors.append(f"displacement_estimate.{comp} must be numeric")
                    elif not (0 <= val <= 1):
                        errors.append(f"displacement_estimate.{comp} must be in [0, 1]")
    
    # Validate potentials if provided
    if has_potentials:
        pot = packet["potentials"]
        if not isinstance(pot, dict):
            errors.append("potentials must be a dictionary")
        else:
            required_domains = ["economy", "employment", "education"]
            for domain in required_domains:
                if domain not in pot:
                    errors.append(f"potentials missing domain: {domain}")
                else:
                    domain_pot = pot[domain]
                    if not isinstance(domain_pot, dict):
                        errors.append(f"potentials.{domain} must be a dictionary")
                    else:
                        # Validate domain components
                        if domain == "economy":
                            required_components = ["Gov", "Info", "Infer", "Int"]
                        elif domain == "employment":
                            required_components = ["GM", "ICu", "IInter", "ICo"]
                        elif domain == "education":
                            required_components = ["GMT", "ICV", "IIA", "ICI"]
                        else:
                            required_components = []
                        
                        for comp in required_components:
                            if comp not in domain_pot:
                                errors.append(f"potentials.{domain} missing component: {comp}")
                            else:
                                val = domain_pot[comp]
                                if not isinstance(val, (int, float)):
                                    errors.append(f"potentials.{domain}.{comp} must be numeric")
                                elif not (0 <= val <= 1):
                                    errors.append(f"potentials.{domain}.{comp} must be in [0, 1]")
    
    # Validate config if provided (per spec: must be a dict)
    if "config" in packet:
        config = packet["config"]
        if not isinstance(config, dict):
            errors.append("config must be a dictionary")
        else:
            # Validate measurement_noise if provided
            if "measurement_noise" in config:
                noise = config["measurement_noise"]
                if not isinstance(noise, (int, float)):
                    errors.append("config.measurement_noise must be numeric")
                elif not (0 < noise <= 1):
                    errors.append("config.measurement_noise must be in (0, 1]")

    # Validate observations if provided
    if "observations" in packet:
        observations = packet["observations"]
        if not isinstance(observations, list):
            errors.append("observations must be a list")
        else:
            for i, obs in enumerate(observations):
                if not isinstance(obs, dict):
                    errors.append(f"observations[{i}] must be a dictionary")
                    continue

                # Check required fields
                if "maps_to" not in obs:
                    errors.append(f"observations[{i}] missing required field 'maps_to'")
                elif obs["maps_to"] not in ["GTD", "IVD", "IAD", "IID"]:
                    errors.append(f"observations[{i}].maps_to must be one of GTD, IVD, IAD, IID")

                if "value" not in obs:
                    errors.append(f"observations[{i}] missing required field 'value'")
                else:
                    value = obs["value"]
                    if not isinstance(value, (int, float)):
                        errors.append(f"observations[{i}].value must be numeric")
                    elif not (0 <= value <= 1):
                        errors.append(f"observations[{i}].value must be in [0, 1]")

                # Check optional noise override
                if "noise" in obs:
                    noise = obs["noise"]
                    if not isinstance(noise, (int, float)):
                        errors.append(f"observations[{i}].noise must be numeric")
                    elif not (0 < noise <= 1):
                        errors.append(f"observations[{i}].noise must be in (0, 1]")
    
    # Validate session_id if provided (should be a string or null)
    if "session_id" in packet:
        sid = packet["session_id"]
        if sid is not None and not isinstance(sid, str):
            errors.append("session_id must be a string or null")
        elif sid == "":
            errors.append("session_id must be a non-empty string or null")
    
    # Validate patterns if provided
    if "patterns" in packet:
        patterns = packet["patterns"]
        if not isinstance(patterns, list):
            errors.append("patterns must be a list")
        else:
            for i, pattern in enumerate(patterns):
                if not isinstance(pattern, str):
                    errors.append(f"patterns[{i}] must be a string")
    
    return errors


def validate_and_raise(packet: Dict[str, Any]) -> None:
    """
    Validates packet and raises ValidationError if invalid.
    
    Args:
        packet: Egress packet dictionary.
    
    Raises:
        ValidationError: If validation fails.
    """
    errors = validate_egress_packet(packet)
    if errors:
        raise ValidationError(f"Packet validation failed: {'; '.join(errors)}")

