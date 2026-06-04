# Touch Grass CLI

Touch Grass is a command-line activity recommender for finding something fun to do outside, around town, or nearby. It loads a local activity dataset, applies optional filters, and prints a small set of randomized recommendations.

The CLI command is:

```bash
touch-grass plan
```

## Features

- Get random activity recommendations from the full dataset.
- Filter by city, weather, duration, energy level, and category.
- Use surprise mode when you want the CLI to pick one unexpected activity.
- See available filter options directly in the help output.
- Regenerate the synthetic activity dataset from source templates.

## Quick Start

This project uses `uv` for running the package and managing dependencies.

```bash
uv sync
uv run touch-grass plan
```

To see every available CLI option:

```bash
uv run touch-grass plan --help
```

## Usage

Run the planner with no filters to get five random recommendations:

```bash
uv run touch-grass plan
```

Filter by city:

```bash
uv run touch-grass plan --city "San Diego"
```

Combine filters:

```bash
uv run touch-grass plan --city "Los Angeles" --energy low --hours 3
```

Filter by category:

```bash
uv run touch-grass plan --category outdoors
```

Filter by weather:

```bash
uv run touch-grass plan --weather sunny --energy high
```

Use surprise mode to ignore all filters and return one random activity:

```bash
uv run touch-grass plan --surprise
```

## Filters

All filters are optional.

| Option | Description |
| --- | --- |
| `--city` | Matches activities in a specific city. |
| `--weather` | Matches activities that support a weather condition. |
| `--hours` | Returns activities with `duration_hours` less than or equal to this value. |
| `--energy` | Matches activities by energy level. |
| `--category` | Matches activities in a specific category. |
| `--surprise` | Ignores filters and returns one random activity. |

The help output lists the current available values from `data/activities.json`, so users do not have to guess:

```bash
uv run touch-grass plan --help
```

Current filter values include:

- Cities: Carlsbad, Coronado, Del Mar, Encinitas, Irvine, La Jolla, Laguna Beach, Los Angeles, Newport Beach, Oceanside, Pasadena, San Diego, Santa Monica
- Weather: any, cloudy, sunny
- Energy: high, low, medium
- Categories: adventure, creative, entertainment, exercise, food, learning, outdoor, outdoors, relaxing, shopping, sightseeing, social
- Durations: 1, 2, 3, 4, 5, 6, 8 hours

## Dataset

The activity data lives in:

```text
data/activities.json
```

Each activity contains:

- `id`
- `city`
- `category`
- `duration_hours`
- `weather`
- `energy`
- `description`

To regenerate the dataset:

```bash
uv run python src/touch_grass_cli/generate_activities.py
```

The generator creates a synthetic dataset from activity templates in `src/touch_grass_cli/generate_activities.py`.

## Project Structure

```text
.
|-- data/
|   `-- activities.json
|-- src/
|   `-- touch_grass_cli/
|       |-- cli.py
|       |-- data_loader.py
|       |-- generate_activities.py
|       `-- recommender.py
|-- tests/
|   |-- test_activities_sample.py
|   |-- test_cli_scenarios.py
|   `-- test_data_loader.py
|-- pyproject.toml
`-- README.md
```

## Testing

Run the data loader and recommender checks:

```bash
uv run python tests/test_data_loader.py
```

Display a sample of activities:

```bash
uv run python tests/test_activities_sample.py
```

Run CLI scenario checks:

```bash
uv run python tests/test_cli_scenarios.py
```

## Development Notes

- The package entry point is configured in `pyproject.toml` as `touch-grass`.
- Recommendation logic lives in `src/touch_grass_cli/recommender.py`.
- CLI option help is generated from the current dataset, so updating `activities.json` updates the help text automatically.
- Invalid filter values are not rejected before running the search; they return no matching activities.
