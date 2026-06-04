# Testing Guide

This directory contains test files for the Summer Quest CLI project.

## Test Files

### `test_data_loader.py`
Tests the data loader and recommender modules including all filter functions:
- `load_activities()` - Load activities from JSON
- `filter_by_city()` - Filter by location
- `filter_by_weather()` - Filter by weather conditions
- `filter_by_duration()` - Filter by duration
- `filter_by_energy()` - Filter by energy level
- `get_recommendations()` - Combined filtering and recommendation

**Run:**
```bash
python tests/test_data_loader.py
```

### `test_activities_sample.py`
Displays a sample of activities from the dataset to verify data quality and structure.

**Run:**
```bash
python tests/test_activities_sample.py
```

### `test_cli_scenarios.py`
Tests all CLI usage scenarios:
- No filters (random recommendations)
- Single filter
- Multiple filters
- Surprise mode (random activity ignoring filters)

**Run:**
```bash
python tests/test_cli_scenarios.py
```

## CLI Usage Modes

### 1. Random Recommendations (No Filters)
```bash
python -m touch_grass_cli.cli plan
```
Returns 5 random activities from all 1,909 available.

### 2. Filtered Recommendations
```bash
python -m touch_grass_cli.cli plan --city "San Diego"
python -m touch_grass_cli.cli plan --city "Los Angeles" --energy "low" --hours 3
python -m touch_grass_cli.cli plan --weather "sunny" --energy "high"
```
Returns up to 5 activities matching the specified filters.

### 3. Surprise Mode (NEW!)
```bash
python -m touch_grass_cli.cli plan --surprise
```
Ignores all filters and returns 1 random activity with a celebratory message!

## Running All Tests

```bash
# Run individual test files from project root
python tests/test_data_loader.py
python tests/test_activities_sample.py
python tests/test_cli_scenarios.py
```

## Notes

- All tests add the `src/` directory to `sys.path` automatically
- Tests should be run from the project root directory
- No external dependencies required - uses only Python standard library
- Surprise mode is perfect for when you can't decide - it picks something unexpected for you!
