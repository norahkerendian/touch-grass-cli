import typer
from typing import Optional

from touch_grass_cli.ai import generate_plan
from touch_grass_cli.planner import build_context, build_prompt
from touch_grass_cli.recommender import get_recommendations, format_activity

app = typer.Typer()


@app.callback()
def main():
    """Summer Quest CLI."""
    pass


@app.command()
def plan(
    city: Optional[str] = typer.Option(
        None,
        "--city",
        help="Filter by city (e.g., San Diego, Los Angeles)"
    ),
    weather: Optional[str] = typer.Option(
        None,
        "--weather",
        help="Filter by weather (sunny, cloudy, rainy, any)"
    ),
    hours: Optional[int] = typer.Option(
        None,
        "--hours",
        help="Filter by maximum duration in hours"
    ),
    energy: Optional[str] = typer.Option(
        None,
        "--energy",
        help="Filter by energy level (low, medium, high)"
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
    
        summer-quest plan
        summer-quest plan --city "San Diego"
        summer-quest plan --city "Los Angeles" --energy "low" --hours 3
        summer-quest plan --weather "sunny" --energy "high"
        summer-quest plan --surprise
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
                limit=5
            )
        
        if not recommendations:
            typer.echo("No activities found matching your filters.", err=True)
            raise typer.Exit(code=1)
        
        # Display recommendations header
        if surprise:
            typer.echo("\n🎉 Summer Quest - Surprise Activity! 🎉\n")
            typer.echo("Get out there and try something unexpected today!\n")
        else:
            typer.echo("\n🌿 Summer Quest - Activity Recommendations 🌿\n")
            
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
