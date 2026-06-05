"""Load and manage activity data from JSON."""

import json
from importlib import resources
from typing import Any, Dict, List


ACTIVITIES_RESOURCE = resources.files("touch_grass_cli").joinpath("data").joinpath("activities.json")


def load_activities() -> List[Dict[str, Any]]:
    """
    Load activities from the packaged activities.json resource.
    
    Returns:
        List of activity dictionaries
        
    Raises:
        FileNotFoundError: If the packaged activities.json resource does not exist
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        with ACTIVITIES_RESOURCE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "Packaged activities file not found: touch_grass_cli/data/activities.json"
        ) from error
