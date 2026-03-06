# uv run python -m spotify_assistant.main_comedy
import time

import pandas as pd
from loguru import logger

from spotify_assistant.clients.spotify import add_tracks_to_playlist
from spotify_assistant.clients.spotify import search_track
from spotify_assistant.settings import settings

DTYPES = {
    "artist": "string",
    "track": "string",
    "added_at": "string",
    "source": "string",
    "has_spotify": "boolean",
    "in_playlist": "boolean",
}

REQUEST_DELAY = 0.1  # seconds between API calls


def load_dataset() -> pd.DataFrame:
    """Load comedy tracks CSV into DataFrame."""
    return pd.read_csv(
        settings.track_pairs_path,
        low_memory=False,
        dtype=DTYPES,  # type: ignore
        keep_default_na=True,
        na_values=["", "null", "None"],
    )


def save_dataset(df: pd.DataFrame) -> None:
    """Save DataFrame back to CSV."""
    df.to_csv(settings.track_pairs_path, index=False)
    logger.info(f"Saved {len(df)} rows to {settings.track_pairs_path}")


def should_skip_row(row: pd.Series) -> bool:  # type: ignore[type-arg]
    """Check if row should be skipped."""
    if row.in_playlist is True:
        return True
    if row.has_spotify is False:
        return True
    return False


def process_row(row: pd.Series) -> pd.Series:  # type: ignore[type-arg]
    """Process a single comedy track row."""
    track_name = f"{row.artist} - {row.track}"

    if should_skip_row(row):
        logger.debug(f"SKIP: {track_name}")
        return row

    logger.info(f"Processing: {track_name}")

    found = search_track(row.track, row.artist)
    if not found:
        logger.warning(f"  Not found: {track_name}")
        row["has_spotify"] = False
        return row

    row["has_spotify"] = True
    logger.success(f"  Found: {found['name']} by {found['artist']}")
    time.sleep(REQUEST_DELAY)

    add_tracks_to_playlist(settings.TARGET_PLAYLIST_ID, [found["uri"]])
    row["in_playlist"] = True
    logger.success("  Added to playlist!")

    return row


def main() -> None:
    """Main entry point for processing comedy tracks."""
    logger.info(f"Loading dataset from {settings.track_pairs_path}")
    df = load_dataset()
    logger.info(f"Loaded {len(df)} tracks")

    already_in_playlist = df["in_playlist"].sum()
    logger.info(f"Already in playlist: {already_in_playlist}")

    processed = []
    added_count = 0
    not_found_count = 0

    for _, row in df.iterrows():
        initial_in_playlist = row.in_playlist
        updated_row = process_row(row.copy())
        processed.append(updated_row)

        if updated_row.in_playlist is True and initial_in_playlist is not True:
            added_count += 1
        if updated_row.has_spotify is False:
            not_found_count += 1

    result_df = pd.DataFrame(processed)
    save_dataset(result_df)

    logger.info("=" * 50)
    logger.info("SUMMARY")
    logger.info(f"  Total tracks: {len(df)}")
    logger.info(f"  Added to playlist this run: {added_count}")
    logger.info(f"  Not found on Spotify: {not_found_count}")
    logger.info(f"  Total in playlist: {result_df['in_playlist'].sum()}")


if __name__ == "__main__":
    main()
