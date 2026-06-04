import json
import random
from pathlib import Path

# Get path to activities.json relative to this script
script_dir = Path(__file__).parent
data_file = script_dir.parent.parent / "data" / "activities.json"

data = json.load(open(data_file))
print('Sample of 10 random activities:')
for a in random.sample(data, 10):
    print(f"\n✓ ID: {a['id']} | {a['city']} | {a['category']}")
    print(f"  Duration: {a['duration_hours']}h | Energy: {a['energy']} | Weather: {', '.join(a['weather'])}")
    print(f"  → {a['description']}")
