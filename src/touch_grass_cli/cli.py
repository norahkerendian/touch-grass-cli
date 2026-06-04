import typer
from typing import Any, Iterable, Optional

from touch_grass_cli.ai import generate_plan
from touch_grass_cli.data_loader import load_activities
from touch_grass_cli.planner import build_context, build_prompt
from touch_grass_cli.recommender import get_recommendations, format_activity

app = typer.Typer()


def _format_options(values: Iterable[Any]) -> str:
    """Format filter values for compact CLI help."""
    return ", ".join(str(value) for value in sorted(values))


def _get_filter_options(field: str) -> str:
    try:
        activities = load_activities()
    except (FileNotFoundError, RuntimeError, ValueError):
        return "options unavailable"

    if field == "weather":
        values = {
            weather
            for activity in activities
            for weather in activity.get("weather", [])
            if weather
        }
    else:
        values = {
            activity.get(field)
            for activity in activities
            if activity.get(field) is not None
        }

    return _format_options(values)


@app.callback()
def main():
    """Touch Grass CLI."""
    pass


@app.command()
def plan(
    city: Optional[str] = typer.Option(
        None,
        "--city",
        help=f"Filter by city. Options: {_get_filter_options('city')}"
    ),
    weather: Optional[str] = typer.Option(
        None,
        "--weather",
        help=f"Filter by weather. Options: {_get_filter_options('weather')}"
    ),
    hours: Optional[int] = typer.Option(
        None,
        "--hours",
        help=f"Filter by maximum duration in hours. Available activity durations: {_get_filter_options('duration_hours')}"
    ),
    energy: Optional[str] = typer.Option(
        None,
        "--energy",
        help=f"Filter by energy level. Options: {_get_filter_options('energy')}"
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        help=f"Filter by activity category. Options: {_get_filter_options('category')}"
    ),
    surprise: bool = typer.Option(
        False,
        "--surprise",
        help="Ignore all filters and get a random surprise activity!"
    ),
):
    """
    Get personalized activity recommendations.
    
    All filters are optional. If no filters are provided, you'll get
    random recommendations from all available activities.
    
    Use --surprise to ignore all filters and get a random activity!
    
    Examples:
    
        touch-grass plan
        touch-grass plan --city "San Diego"
        touch-grass plan --city "Los Angeles" --energy "low" --hours 3
        touch-grass plan --weather "sunny" --energy "high"
        touch-grass plan --category "outdoors"
        touch-grass plan --surprise
    """
    try:
        # Surprise mode overrides all filters
        if surprise:
            recommendations = get_recommendations(limit=1)
        else:
            # Get recommendations based on filters
            recommendations = get_recommendations(
                city=city,
                weather=weather,
                duration=hours,
                energy=energy,
                category=category,
                limit=5
            )
        
        if not recommendations:
            typer.echo("No activities found matching your filters.", err=True)
            raise typer.Exit(code=1)
        
        # Display recommendations header
        if surprise:
            typer.echo("\n🎉 Touch Grass - Surprise Activity! 🎉\n")
            typer.echo("Get out there and try something unexpected today!\n")
        else:
            typer.echo("\n🌿 Touch Grass - Activity Recommendations 🌿\n")
            
            # Show active filters
            active_filters = []
            if city:
                active_filters.append(f"📍 City: {city}")
            if weather:
                active_filters.append(f"☀️  Weather: {weather}")
            if hours:
                active_filters.append(f"⏱️  Max Duration: {hours} hours")
            if energy:
                active_filters.append(f"💪 Energy Level: {energy}")
            if category:
                active_filters.append(f"🏷️  Category: {category}")
            
            if active_filters:
                typer.echo("Active Filters:")
                for filter_str in active_filters:
                    typer.echo(f"  {filter_str}")
                typer.echo()
            else:
                typer.echo("✨ Showing random activities from all available options\n")
            
            typer.echo(f"Found {len(recommendations)} activity recommendation{'s' if len(recommendations) != 1 else ''}:\n")
        
        for i, activity in enumerate(recommendations, 1):
            typer.echo(format_activity(activity))
        
    except FileNotFoundError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error
    except (RuntimeError, ValueError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error


if __name__ == "__main__":
    app()
