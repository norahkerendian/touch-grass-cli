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

## Running All Tests

```bash
# Run individual test files from project root
python tests/test_data_loader.py
python tests/test_activities_sample.py
```

## Notes

- All tests add the `src/` directory to `sys.path` automatically
- Tests should be run from the project root directory
- No external dependencies required - uses only Python standard library
