from typing import Annotated

import typer

from spotify_assistant.exceptions import DuplicateTrackPairError
from spotify_assistant.models.tracks import TrackPair
from spotify_assistant.services.csv_manager import append_track_pair
from spotify_assistant.services.csv_manager import validate_track_pair
from spotify_assistant.settings import settings

app = typer.Typer(
    name="spotify-assistant",
    help="Create Spotify playlists with Forró cover + original pairs",
)


def _add_track_pair(pair: TrackPair) -> bool:
    """Add a track pair to CSV. Returns True if successful."""
    errors = validate_track_pair(pair)
    if errors:
        for error in errors:
            typer.echo(f"Validation error: {error}", err=True)
        return False

    try:
        row = append_track_pair(settings.track_pairs_path, pair)
        typer.echo(
            f"Added: {row['brazilian_artist']} - {row['brazilian_track']} "
            f"-> {row['original_artist']} - {row['original_track']}"
        )
        return True
    except DuplicateTrackPairError as e:
        typer.echo(f"Warning: {e}", err=True)
        return False


@app.command()
def populate_csv(
    brazilian_artist: Annotated[
        str,
        typer.Option("--brazilian-artist", "-ba", help="Brazilian artist name"),
    ],
    brazilian_track: Annotated[
        str,
        typer.Option("--brazilian-track", "-bt", help="Brazilian track name"),
    ],
    original_artist: Annotated[
        str,
        typer.Option("--original-artist", "-oa", help="Original artist name"),
    ],
    original_track: Annotated[
        str,
        typer.Option("--original-track", "-ot", help="Original track name"),
    ],
) -> None:
    """Add a track pair to the CSV dataset."""
    pair = TrackPair(
        brazilian_artist=brazilian_artist,
        brazilian_track=brazilian_track,
        original_artist=original_artist,
        original_track=original_track,
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
    )

    if not _add_track_pair(pair):
        raise typer.Exit(code=1)


@app.command()
def build_playlist() -> None:
    """Build Spotify playlist from CSV dataset."""
    typer.echo("build-playlist: Not implemented yet")


if __name__ == "__main__":
    app()
