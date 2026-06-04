import typer

app = typer.Typer()

@app.callback()
def main():
    """Summer Quest CLI."""
    pass

@app.command()
def plan():
    """Generate a summer activity plan."""
    print("Summer Quest coming soon!")

if __name__ == "__main__":
    app()