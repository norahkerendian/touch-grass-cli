import typer

from touch_grass_cli.ai import generate_plan
from touch_grass_cli.planner import build_context, build_prompt

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
    )
):
    context = build_context(budget)
    prompt = build_prompt(context)
    try:
        response = generate_plan(prompt)
    except (RuntimeError, ValueError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    print(response)


if __name__ == "__main__":
    app()
