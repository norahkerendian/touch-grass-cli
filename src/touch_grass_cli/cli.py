import typer

app = typer.Typer()

@app.callback()
def main():
    """Summer Quest CLI."""
    pass

@app.command()
def plan(
    budget: int = typer.Option(
        20,
        help="Maximum budget in dollars"
    )
):
    print(f"Planning an adventure under ${budget}")

if __name__ == "__main__":
    app()