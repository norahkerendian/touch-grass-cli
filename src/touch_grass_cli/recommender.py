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


def filter_by_category(activities: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """
    Filter activities by category.

    Args:
        activities: List of activity dictionaries
        category: Category name (case-insensitive match)

    Returns:
        Filtered list of activities with matching category
    """
    if not category:
        return activities

    category_lower = category.lower()
    return [a for a in activities if a.get("category", "").lower() == category_lower]


def get_recommendations(
    city: Optional[str] = None,
    weather: Optional[str] = None,
    duration: Optional[int] = None,
    energy: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Get activity recommendations based on filters.
    
    Args:
        city: Filter by city (optional)
        weather: Filter by weather (optional)
        duration: Filter by max duration in hours (optional)
        energy: Filter by energy level (optional)
        category: Filter by activity category (optional)
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

    if category:
        activities = filter_by_category(activities, category)
    
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
    "sunny":  "☀️  sunny",
    "cloudy": "⛅ cloudy",
    "rainy":  "🌧️ rainy",
    "any":    "🌈 any",
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

import textwrap
from typing import Dict, Any
from wcwidth import wcswidth  # pip install wcwidth

import unicodedata

def visible_len(s: str) -> int:
    """Return visual terminal width, stripping variation selectors that confuse wcswidth."""
    # Remove variation selectors (U+FE00–U+FE0F) which add 0 width but aren't counted right
    cleaned = "".join(c for c in s if unicodedata.category(c) != "Mn" and c not in "\uFE0F\uFE0E")
    w = wcswidth(cleaned)
    return w if w >= 0 else len(cleaned)

def pad_to(s: str, width: int) -> str:
    """Pad string s with spaces so its visual width equals `width`."""
    return s + " " * (width - visible_len(s))

def row(content: str, box_width: int) -> str:
    """Pad content to exactly box_width visual columns and wrap in │ borders."""
    return f"│ {pad_to(content, box_width)} │"

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

    BOX_WIDTH = 60
    OUTER = BOX_WIDTH + 2

    title   = f"#{activity_id}  {city_icon} {city}"
    energy_icon = energy_str.split()[0]  # grab just the emoji
    tags = f"{cat_icon} category: {category}   {energy_icon} energy: {energy}"
    details = f"🕐 {duration}h   🌤️ {weather_str}"

    wrapped = textwrap.wrap(description, width=BOX_WIDTH)

    divider = f"├{'─' * OUTER}┤"
    top     = f"╭{'─' * OUTER}╮"
    bottom  = f"╰{'─' * OUTER}╯"

    lines = [
        f"\n{top}",
        row(title, BOX_WIDTH),
        divider,
        row(tags, BOX_WIDTH),
        row(details, BOX_WIDTH),
        divider,
        *[row(line, BOX_WIDTH) for line in wrapped],
        bottom,
        "",
    ]
    return "\n".join(lines)
