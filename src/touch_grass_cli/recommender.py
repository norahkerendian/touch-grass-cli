"""Recommend activities based on filters."""

import random
from typing import List, Dict, Any, Optional
import textwrap

from touch_grass_cli.data_loader import load_activities


def filter_by_city(activities: List[Dict[str, Any]], city: str) -> List[Dict[str, Any]]:
    """
    Filter activities by city.
    
    Args:
        activities: List of activity dictionaries
        city: City name (case-insensitive match)
        
    Returns:
        Filtered list of activities
    """
    if not city:
        return activities
    
    city_lower = city.lower()
    return [a for a in activities if a.get("city", "").lower() == city_lower]


def filter_by_weather(activities: List[Dict[str, Any]], weather: str) -> List[Dict[str, Any]]:
    """
    Filter activities by weather condition.
    
    Args:
        activities: List of activity dictionaries
        weather: Weather condition (e.g., "sunny", "rainy", "any")
        
    Returns:
        Filtered list of activities that support the specified weather
    """
    if not weather:
        return activities
    
    weather_lower = weather.lower()
    return [a for a in activities if weather_lower in [w.lower() for w in a.get("weather", [])]]


def filter_by_duration(activities: List[Dict[str, Any]], max_hours: int) -> List[Dict[str, Any]]:
    """
    Filter activities by maximum duration.
    
    Args:
        activities: List of activity dictionaries
        max_hours: Maximum duration in hours
        
    Returns:
        Filtered list of activities that fit within the duration
    """
    if not max_hours or max_hours <= 0:
        return activities
    
    return [a for a in activities if a.get("duration_hours", 0) <= max_hours]


def filter_by_energy(activities: List[Dict[str, Any]], energy_level: str) -> List[Dict[str, Any]]:
    """
    Filter activities by energy level.
    
    Args:
        activities: List of activity dictionaries
        energy_level: Energy level ("low", "medium", or "high")
        
    Returns:
        Filtered list of activities with matching energy level
    """
    if not energy_level:
        return activities
    
    energy_lower = energy_level.lower()
    return [a for a in activities if a.get("energy", "").lower() == energy_lower]


def get_recommendations(
    city: Optional[str] = None,
    weather: Optional[str] = None,
    duration: Optional[int] = None,
    energy: Optional[str] = None,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Get activity recommendations based on filters.
    
    Args:
        city: Filter by city (optional)
        weather: Filter by weather (optional)
        duration: Filter by max duration in hours (optional)
        energy: Filter by energy level (optional)
        limit: Maximum number of recommendations to return (default 5)
        
    Returns:
        List of recommended activities (up to 'limit' items)
    """
    activities = load_activities()
    
    # Apply filters in sequence
    if city:
        activities = filter_by_city(activities, city)
    
    if weather:
        activities = filter_by_weather(activities, weather)
    
    if duration:
        activities = filter_by_duration(activities, duration)
    
    if energy:
        activities = filter_by_energy(activities, energy)
    
    # Randomly select up to 'limit' activities
    if len(activities) == 0:
        return []
    
    return random.sample(activities, min(limit, len(activities)))

# def format_activity(activity: Dict[str, Any]) -> str:
#     activity_id = activity.get("id", "N/A")
#     city = activity.get("city", "Unknown")
#     category = activity.get("category", "Unknown")
#     duration = activity.get("duration_hours", "N/A")
#     energy = activity.get("energy", "Unknown")
#     weather = ", ".join(activity.get("weather", ["any"]))
#     description = activity.get("description", "No description")

#     box_width = 77  # inner width between │ and │
#     wrapped = textwrap.wrap(description, width=box_width - 2)  # -2 for "│ " and " │"
#     desc_lines = "\n".join(f"│ {line:<{box_width - 2}} │" for line in wrapped)

#     return f"""
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ ID: {activity_id:<6} | {city:<20} | {category:<15} | {energy:<8} │
# ├─────────────────────────────────────────────────────────────────────────────┤
# │ Duration: {duration}h | Weather: {weather:<30} │
# ├─────────────────────────────────────────────────────────────────────────────┤
# {desc_lines}
# └─────────────────────────────────────────────────────────────────────────────┘
# """

import textwrap
from typing import Dict, Any

# Emoji maps
CATEGORY_EMOJI = {
    "outdoors": "🌿",
    "food": "🍜",
    "exercise": "💪",
    "creative": "🎨",
    "social": "🤝",
    "relaxing": "😌",
    "adventure": "🗺️",
    "sightseeing": "📸",
    "learning": "📚",
    "entertainment": "🎉",
    "shopping": "🛍️",
}

ENERGY_EMOJI = {
    "low": "🌙 low",
    "medium": "⚡ medium",
    "high": "🔥 high",
}

WEATHER_EMOJI = {
    "sunny": "☀️ sunny",
    "cloudy": "⛅ cloudy",
    "rainy": "🌧️ rainy",
    "any": "🌈 any",
}

CITY_EMOJI = {
    "San Diego": "🌊",
    "La Jolla": "🐬",
    "Coronado": "🏰",
    "Del Mar": "🏇",
    "Carlsbad": "🌸",
    "Encinitas": "🤙",
    "Oceanside": "⛵",
    "Los Angeles": "🎬",
    "Santa Monica": "🎡",
    "Pasadena": "🌺",
    "Irvine": "🏙️",
    "Newport Beach": "⛵",
    "Laguna Beach": "🎨",
}


def format_activity(activity: Dict[str, Any]) -> str:
    activity_id = activity.get("id", "N/A")
    city = activity.get("city", "Unknown")
    category = activity.get("category", "Unknown")
    duration = activity.get("duration_hours", "N/A")
    energy = activity.get("energy", "unknown")
    weather_list = activity.get("weather", ["any"])
    description = activity.get("description", "No description")

    city_icon = CITY_EMOJI.get(city, "📍")
    cat_icon = CATEGORY_EMOJI.get(category, "✨")
    energy_str = ENERGY_EMOJI.get(energy, f"⚡ {energy}")
    weather_str = "  ".join(WEATHER_EMOJI.get(w, w) for w in weather_list)
    duration_str = f"{'⏱️'} {duration}h"

    BOX_WIDTH = 60          # inner content width (between │ and │)
    OUTER = BOX_WIDTH + 2   # including the two │ chars

    def row(content: str) -> str:
        """Pad content to exactly BOX_WIDTH and wrap in │ borders."""
        # Strip ANSI/emoji length issues by padding to visible width
        return f"│ {content:<{BOX_WIDTH}} │"

    # Title row: ID + city
    title = f"#{activity_id}  {city_icon} {city}"
    title_row = row(title)

    # Tags row: category, energy
    tags = f"{cat_icon} {category}   {energy_str}"
    tags_row = row(tags)

    # Details row: duration + weather
    details = f"{duration_str}   🌤 {weather_str}"
    details_row = row(details)

    # Wrapped description rows
    wrapped = textwrap.wrap(description, width=BOX_WIDTH)
    desc_rows = "\n".join(row(line) for line in wrapped)

    divider  = f"├{'─' * (OUTER)}┤"
    top      = f"╭{'─' * (OUTER)}╮"
    bottom   = f"╰{'─' * (OUTER)}╯"

    return (
        f"\n{top}\n"
        f"{title_row}\n"
        f"{divider}\n"
        f"{tags_row}\n"
        f"{details_row}\n"
        f"{divider}\n"
        f"{desc_rows}\n"
        f"{bottom}\n"
    )