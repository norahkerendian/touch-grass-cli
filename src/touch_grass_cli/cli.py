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
    budget: int = typer.Option(
        20,
        "--budget",
        help="Maximum budget in dollars"
    ),
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
):
    """
    Get personalized activity recommendations.
    
    Use filters to narrow down suggestions:
    - --city: Filter by location
    - --weather: Filter by weather conditions
    - --hours: Filter by activity duration
    - --energy: Filter by energy level required
    """
    try:
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
        
        # Display recommendations
        typer.echo("\n🌿 Summer Quest - Activity Recommendations 🌿\n")
        
        if city:
            typer.echo(f"📍 City: {city}")
        if weather:
            typer.echo(f"☀️  Weather: {weather}")
        if hours:
            typer.echo(f"⏱️  Max Duration: {hours} hours")
        if energy:
            typer.echo(f"💪 Energy Level: {energy}")
        
        typer.echo(f"\n Found {len(recommendations)} activity recommendations:\n")
        
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
