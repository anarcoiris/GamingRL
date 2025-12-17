"""Utility functions for checkers environment."""

import json
from typing import Dict, Any, Optional
import numpy as np


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    with open(config_path, "r") as f:
        return json.load(f)


def action_to_dict(action) -> Dict:
    """Convert action to dictionary format.

    Args:
        action: Action object (Move or dict)

    Returns:
        Dictionary representation of action
    """
    if isinstance(action, dict):
        return action
    elif hasattr(action, "to_dict"):
        return action.to_dict()
    else:
        raise ValueError(f"Cannot convert action of type {type(action)} to dict")


def dict_to_action(action_dict: Dict):
    """Convert dictionary to action format.

    Args:
        action_dict: Dictionary with action data

    Returns:
        Action dictionary
    """
    # Validate action structure
    required_keys = ["from", "to"]
    for key in required_keys:
        if key not in action_dict:
            raise ValueError(f"Action missing required key: {key}")

    # Ensure all keys are present with defaults
    return {
        "from": tuple(action_dict["from"]),
        "to": tuple(action_dict["to"]),
        "captures": [tuple(c) for c in action_dict.get("captures", [])],
        "promotion": action_dict.get("promotion", False),
        "sequence_length": action_dict.get("sequence_length", 1),
    }

