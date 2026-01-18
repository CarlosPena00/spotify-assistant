# uv run python -m spotify_assistant.main
import time

import pandas as pd
from loguru import logger

from spotify_assistant.clients.spotify import add_tracks_to_playlist
from spotify_assistant.clients.spotify import search_track
from spotify_assistant.settings import settings

DTYPES = {
    "brazilian_artist": "string",
    "brazilian_track": "string",
    "original_artist": "string",
    "original_track": "string",
    "added_at": "string",
    "source": "string",
    "brazilian_has_spotify": "boolean",
    "original_has_spotify": "boolean",
    "in_playlist": "boolean",
}

REQUEST_DELAY = 0.1  # seconds between API calls


def load_dataset() -> pd.DataFrame:
    """Load track pairs CSV into DataFrame."""
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


def search_brazilian_track(row: pd.Series) -> str | None:
    """Search for Brazilian track. Returns URI if found, None otherwise."""
    brazilian = search_track(row.brazilian_track, row.brazilian_artist)
    if not brazilian:
        logger.warning(
            f"  BR not found: {row.brazilian_artist} - {row.brazilian_track}"
        )
        return None
    logger.success(f"  BR found: {brazilian['name']} by {brazilian['artist']}")
    time.sleep(REQUEST_DELAY)
    return brazilian["uri"]


def search_original_track(row: pd.Series) -> str | None:
    """Search for Original track. Returns URI if found, None otherwise."""
    original = search_track(row.original_track, row.original_artist)
    if not original:
        logger.warning(
            f"  ORIG not found: {row.original_artist} - {row.original_track}"
        )
        return None
    logger.success(f"  ORIG found: {original['name']} by {original['artist']}")
    time.sleep(REQUEST_DELAY)
    return original["uri"]


def should_skip_row(row: pd.Series) -> bool:
    """Check if row should be skipped."""
    if row.in_playlist is True:
        return True
    if row.brazilian_has_spotify is False:
        return True
    if row.original_has_spotify is False:
        return True
    return False


def process_row(row: pd.Series) -> pd.Series:
    """Process a single track pair row."""
    pair_name = (
        f"{row.brazilian_artist} - {row.brazilian_track} -> "
        f"{row.original_artist} - {row.original_track}"
    )

    if should_skip_row(row):
        logger.debug(f"SKIP: {pair_name}")
        return row

    logger.info(f"Processing: {pair_name}")

    # Search Brazilian track
    brazilian_uri = search_brazilian_track(row)
    if not brazilian_uri:
        row["brazilian_has_spotify"] = False
        return row
    row["brazilian_has_spotify"] = True

    # Search Original track
    original_uri = search_original_track(row)
    if not original_uri:
        row["original_has_spotify"] = False
        return row
    row["original_has_spotify"] = True

    # Add to playlist
    add_tracks_to_playlist(settings.TARGET_PLAYLIST_ID, [brazilian_uri, original_uri])
    row["in_playlist"] = True
    logger.success("  Added to playlist!")

    return row


def main() -> None:
    """Main entry point for processing track pairs."""
    logger.info(f"Loading dataset from {settings.track_pairs_path}")
    df = load_dataset()
    logger.info(f"Loaded {len(df)} track pairs")

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
        if (
            updated_row.brazilian_has_spotify is False
            or updated_row.original_has_spotify is False
        ):
            not_found_count += 1

    result_df = pd.DataFrame(processed)
    save_dataset(result_df)

    logger.info("=" * 50)
    logger.info("SUMMARY")
    logger.info(f"  Total pairs: {len(df)}")
    logger.info(f"  Added to playlist this run: {added_count}")
    logger.info(f"  Not found on Spotify: {not_found_count}")
    logger.info(f"  Total in playlist: {result_df['in_playlist'].sum()}")


if __name__ == "__main__":
    main()
