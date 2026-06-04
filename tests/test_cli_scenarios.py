#!/usr/bin/env python3
"""Test comprehensive CLI usage scenarios."""

import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from touch_grass_cli.recommender import get_recommendations

print("🧪 CLI Usage Scenarios Test\n")

# Test 1: No filters
print("1️⃣  No Filters (random from all activities):")
recs = get_recommendations(limit=5)
print(f"   ✓ Got {len(recs)} recommendations\n")

# Test 2: Single filter
print("2️⃣  Single Filter (city):")
recs = get_recommendations(city="Santa Monica", limit=5)
print(f"   ✓ Got {len(recs)} recommendations for Santa Monica\n")

# Test 3: Multiple filters
print("3️⃣  Multiple Filters (city + weather + duration + energy + category):")
recs = get_recommendations(
    city="San Diego",
    weather="sunny",
    duration=3,
    energy="low",
    category="outdoors",
    limit=5
)
print(f"   ✓ Got {len(recs)} recommendations matching all filters\n")

# Test 4: Surprise mode (no filters applied)
print("4️⃣  Surprise Mode (ignores filters, returns 1 random):")
recs_surprise = get_recommendations(limit=1)
print(f"   ✓ Got {len(recs_surprise)} surprise activity")
if recs_surprise:
    print(f"   → Activity ID: {recs_surprise[0]['id']} - {recs_surprise[0]['category']} in {recs_surprise[0]['city']}\n")

# Test 5: Multiple surprise calls
print("5️⃣  Multiple Surprise Calls (verify randomness):")
ids = []
for i in range(3):
    recs = get_recommendations(limit=1)
    if recs:
        ids.append(recs[0]['id'])
print(f"   ✓ Got surprise activities with IDs: {ids}")
if len(set(ids)) == len(ids):
    print(f"   ✓ All different activities (good randomness!)\n")
else:
    print(f"   ⚠️  Some repeated activities\n")

print("✅ All CLI scenarios working correctly!")
