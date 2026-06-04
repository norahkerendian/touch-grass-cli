"""Load and manage activity data from JSON."""

import json
from pathlib import Path
from typing import List, Dict, Any


def get_activities_path() -> Path:
    """Get the path to the activities.json file."""
    return Path(__file__).parent.parent.parent / "data" / "activities.json"


def load_activities() -> List[Dict[str, Any]]:
    """
    Load activities from data/activities.json.
    
    Returns:
        List of activity dictionaries
        
    Raises:
        FileNotFoundError: If activities.json does not exist
        json.JSONDecodeError: If JSON is invalid
    """
    activities_path = get_activities_path()
    
    if not activities_path.exists():
        raise FileNotFoundError(f"Activities file not found at {activities_path}")
    
    with open(activities_path, "r") as f:
        data = json.load(f)
    
    return data
