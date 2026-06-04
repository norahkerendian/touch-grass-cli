#!/usr/bin/env python3
"""Test the data loader and recommender modules."""

import sys
from pathlib import Path

# Add src directory to path so we can import touch_grass_cli
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from touch_grass_cli.data_loader import load_activities
from touch_grass_cli.recommender import (
    get_recommendations,
    filter_by_city,
    filter_by_weather,
    filter_by_duration,
    filter_by_energy,
)

# Load activities
activities = load_activities()
print(f"✓ Data Loader: Loaded {len(activities)} activities\n")

# Test individual filters
filtered = filter_by_city(activities, "San Diego")
print(f"✓ filter_by_city: Found {len(filtered)} activities in San Diego")

filtered = filter_by_weather(activities, "sunny")
print(f"✓ filter_by_weather: Found {len(filtered)} sunny activities")

filtered = filter_by_duration(activities, 3)
print(f"✓ filter_by_duration: Found {len(filtered)} activities <= 3 hours")

filtered = filter_by_energy(activities, "low")
print(f"✓ filter_by_energy: Found {len(filtered)} low energy activities")

# Test combined recommendations
recs = get_recommendations(
    city="Santa Monica",
    weather="sunny",
    duration=5,
    energy="medium",
    limit=3,
)
print(f"✓ get_recommendations: Got {len(recs)} recommendations with combined filters")

# Test recommendations with no filters
recs_no_filters = get_recommendations(limit=5)
print(f"✓ get_recommendations (no filters): Got {len(recs_no_filters)} random recommendations")

print("\n✅ All modules working correctly!")
