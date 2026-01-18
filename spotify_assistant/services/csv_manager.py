import csv
from datetime import UTC
from datetime import datetime
from pathlib import Path

from spotify_assistant.exceptions import CSVFormatError
from spotify_assistant.exceptions import DuplicateTrackPairError
from spotify_assistant.models.tracks import TrackPair

TRACK_PAIRS_HEADERS = [
    "brazilian_artist",
    "brazilian_track",
    "original_artist",
    "original_track",
    "added_at",
    "source",
    "brazilian_has_spotify",
    "original_has_spotify",
    "in_playlist",
]


def _parse_bool(value: str) -> bool | None:
    """Parse CSV string to bool. Empty string returns None."""
    if value == "":
        return None
    return value.lower() == "true"


def _bool_to_csv(value: bool | None) -> str:
    """Convert bool to CSV string. None returns empty string."""
    if value is None:
        return ""
    return "True" if value else "False"


def _str_or_none(value: str) -> str | None:
    """Convert empty string to None."""
    return value if value else None


def ensure_csv_exists(csv_path: Path) -> None:
    """Ensure CSV file exists with proper headers. Creates it if missing."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(TRACK_PAIRS_HEADERS)


def read_track_pairs(csv_path: Path) -> list[TrackPair]:
    """Read all track pairs from CSV file."""
    ensure_csv_exists(csv_path)

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            return []

        if list(reader.fieldnames) != TRACK_PAIRS_HEADERS:
            actual = list(reader.fieldnames)
            raise CSVFormatError(
                f"Invalid CSV headers. Expected {TRACK_PAIRS_HEADERS}, got {actual}"
            )

        rows: list[TrackPair] = []
        for row in reader:
            track_pair = TrackPair(
                brazilian_artist=row["brazilian_artist"],
                brazilian_track=row["brazilian_track"],
                original_artist=row["original_artist"],
                original_track=row["original_track"],
                added_at=_str_or_none(row["added_at"]),
                source=_str_or_none(row["source"]),
                brazilian_has_spotify=_parse_bool(row["brazilian_has_spotify"]),
                original_has_spotify=_parse_bool(row["original_has_spotify"]),
                in_playlist=_parse_bool(row["in_playlist"]) or False,
            )
            rows.append(track_pair)
        return rows


def find_duplicate(dataset: list[TrackPair], pair: TrackPair) -> TrackPair | None:
    """Find a duplicate track pair in the dataset (case-insensitive comparison)."""
    for row in dataset:
        if (
            row["brazilian_artist"].lower() == pair["brazilian_artist"].lower()
            and row["brazilian_track"].lower() == pair["brazilian_track"].lower()
            and row["original_artist"].lower() == pair["original_artist"].lower()
            and row["original_track"].lower() == pair["original_track"].lower()
        ):
            return row
    return None


def validate_track_pair(pair: TrackPair) -> list[str]:
    """Validate track pair fields. Returns list of error messages (empty if valid)."""
    errors: list[str] = []

    if not pair["brazilian_artist"].strip():
        errors.append("Brazilian artist cannot be empty")
    if not pair["brazilian_track"].strip():
        errors.append("Brazilian track cannot be empty")
    if not pair["original_artist"].strip():
        errors.append("Original artist cannot be empty")
    if not pair["original_track"].strip():
        errors.append("Original track cannot be empty")

    return errors


def append_track_pair(csv_path: Path, pair: TrackPair) -> TrackPair:
    """Append a track pair to CSV. Raises DuplicateTrackPairError if exists."""
    ensure_csv_exists(csv_path)

    existing = read_track_pairs(csv_path)
    duplicate = find_duplicate(existing, pair)

    if duplicate is not None:
        artist = pair["brazilian_artist"]
        track = pair["brazilian_track"]
        raise DuplicateTrackPairError(f"Track pair already exists: {artist} - {track}")

    added_at = datetime.now(UTC).isoformat()
    row = TrackPair(
        brazilian_artist=pair["brazilian_artist"],
        brazilian_track=pair["brazilian_track"],
        original_artist=pair["original_artist"],
        original_track=pair["original_track"],
        added_at=added_at,
        source=pair["source"],
        brazilian_has_spotify=pair["brazilian_has_spotify"],
        original_has_spotify=pair["original_has_spotify"],
        in_playlist=False,
    )

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                row["brazilian_artist"],
                row["brazilian_track"],
                row["original_artist"],
                row["original_track"],
                row["added_at"] or "",
                row["source"] or "",
                _bool_to_csv(row["brazilian_has_spotify"]),
                _bool_to_csv(row["original_has_spotify"]),
                _bool_to_csv(row["in_playlist"]),
            ]
        )

    return row
