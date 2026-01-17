import typer

app = typer.Typer(
    name="spotify-assistant",
    help="Create Spotify playlists with Forró cover + original pairs",
)


@app.command()
def populate_csv() -> None:
    """Add track pairs to the CSV dataset."""
    typer.echo("populate-csv: Not implemented yet")


@app.command()
def build_playlist() -> None:
    """Build Spotify playlist from CSV dataset."""
    typer.echo("build-playlist: Not implemented yet")


if __name__ == "__main__":
    app()
