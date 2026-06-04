#!/usr/bin/env python3
"""Display sample activities from the dataset."""

import json
import random
import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from touch_grass_cli.data_loader import load_activities

# Load and display sample activities
activities = load_activities()
print(f"\n📊 Activity Dataset Overview")
print(f"{'=' * 80}")
print(f"Total Activities: {len(activities)}\n")

print('Sample of 10 random activities:')
print("=" * 80)
for a in random.sample(activities, 10):
    print(f"\n✓ ID: {a['id']} | {a['city']:<20} | {a['category']:<15} | {a['energy']:<8}")
    print(f"  Duration: {a['duration_hours']}h | Weather: {', '.join(a['weather'])}")
    print(f"  → {a['description']}")

print("\n" + "=" * 80)
