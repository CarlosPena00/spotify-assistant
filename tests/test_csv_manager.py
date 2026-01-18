import csv
from pathlib import Path

import pytest

from spotify_assistant.exceptions import CSVFormatError
from spotify_assistant.exceptions import DuplicateTrackPairError
from spotify_assistant.models.tracks import TrackPair
from spotify_assistant.services.csv_manager import TRACK_PAIRS_HEADERS
from spotify_assistant.services.csv_manager import append_track_pair
from spotify_assistant.services.csv_manager import ensure_csv_exists
from spotify_assistant.services.csv_manager import find_duplicate
from spotify_assistant.services.csv_manager import read_track_pairs
from spotify_assistant.services.csv_manager import validate_track_pair


@pytest.fixture
def csv_path(tmp_path: Path) -> Path:
    """Return a temporary CSV file path."""
    return tmp_path / "track_pairs.csv"


@pytest.fixture
def sample_pair() -> TrackPair:
    """Return a sample track pair."""
    return TrackPair(
        brazilian_artist="Falamansa",
        brazilian_track="Xote dos Milagres",
        original_artist="Dominguinhos",
        original_track="Xote dos Milagres",
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
        in_playlist=False,
    )


def test_ensure_csv_exists_creates_file_with_headers(csv_path: Path) -> None:
    """Test that ensure_csv_exists creates a CSV file with proper headers."""
    assert not csv_path.exists()

    ensure_csv_exists(csv_path)

    assert csv_path.exists()
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == TRACK_PAIRS_HEADERS


def test_ensure_csv_exists_creates_parent_directories(tmp_path: Path) -> None:
    """Test that ensure_csv_exists creates parent directories."""
    nested_path = tmp_path / "nested" / "dir" / "track_pairs.csv"

    ensure_csv_exists(nested_path)

    assert nested_path.exists()


def test_ensure_csv_exists_does_not_overwrite_existing(csv_path: Path) -> None:
    """Test that ensure_csv_exists does not overwrite existing file."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.write_text("existing content")

    ensure_csv_exists(csv_path)

    assert csv_path.read_text() == "existing content"


def test_read_track_pairs_returns_empty_list_for_new_file(csv_path: Path) -> None:
    """Test that read_track_pairs returns empty list for new file."""
    result = read_track_pairs(csv_path)

    assert result == []


def test_read_track_pairs_raises_for_invalid_headers(csv_path: Path) -> None:
    """Test that read_track_pairs raises CSVFormatError for invalid headers."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["wrong", "headers"])

    with pytest.raises(CSVFormatError, match="Invalid CSV headers"):
        read_track_pairs(csv_path)


def test_read_track_pairs_returns_all_rows(
    csv_path: Path, sample_pair: TrackPair
) -> None:
    """Test that read_track_pairs returns all rows from CSV."""
    ensure_csv_exists(csv_path)
    append_track_pair(csv_path, sample_pair)

    result = read_track_pairs(csv_path)

    assert len(result) == 1
    assert result[0]["brazilian_artist"] == sample_pair["brazilian_artist"]
    assert result[0]["brazilian_track"] == sample_pair["brazilian_track"]
    assert result[0]["original_artist"] == sample_pair["original_artist"]
    assert result[0]["original_track"] == sample_pair["original_track"]
    assert "added_at" in result[0]


def test_append_track_pair_adds_to_file(csv_path: Path, sample_pair: TrackPair) -> None:
    """Test that append_track_pair adds row to CSV file."""
    row = append_track_pair(csv_path, sample_pair)

    assert row["brazilian_artist"] == sample_pair["brazilian_artist"]
    assert row["brazilian_track"] == sample_pair["brazilian_track"]
    assert row["original_artist"] == sample_pair["original_artist"]
    assert row["original_track"] == sample_pair["original_track"]
    assert row["added_at"]  # type: ignore # Should have timestamp

    # Verify it's in the file
    rows = read_track_pairs(csv_path)
    assert len(rows) == 1


def test_append_track_pair_raises_for_duplicate(
    csv_path: Path, sample_pair: TrackPair
) -> None:
    """Test that append_track_pair raises DuplicateTrackPairError for duplicate."""
    append_track_pair(csv_path, sample_pair)

    with pytest.raises(DuplicateTrackPairError, match="Track pair already exists"):
        append_track_pair(csv_path, sample_pair)


def test_find_duplicate_case_insensitive(sample_pair: TrackPair) -> None:
    """Test that find_duplicate performs case-insensitive comparison."""
    dataset: list[TrackPair] = [
        TrackPair(
            brazilian_artist="FALAMANSA",
            brazilian_track="XOTE DOS MILAGRES",
            original_artist="DOMINGUINHOS",
            original_track="XOTE DOS MILAGRES",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]

    result = find_duplicate(dataset, sample_pair)

    assert result is not None
    assert result["brazilian_artist"] == "FALAMANSA"


def test_find_duplicate_returns_none_when_not_found(sample_pair: TrackPair) -> None:
    """Test that find_duplicate returns None when no duplicate found."""
    result = find_duplicate([], sample_pair)

    assert result is None


def test_validate_track_pair_accepts_valid_pair(sample_pair: TrackPair) -> None:
    """Test that validate_track_pair returns empty list for valid pair."""
    errors = validate_track_pair(sample_pair)

    assert errors == []


def test_validate_track_pair_rejects_empty_fields() -> None:
    """Test that validate_track_pair rejects empty fields."""
    pair = TrackPair(
        brazilian_artist="",
        brazilian_track="",
        original_artist="",
        original_track="",
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
        in_playlist=False,
    )

    errors = validate_track_pair(pair)

    assert len(errors) == 4
    assert "Brazilian artist cannot be empty" in errors
    assert "Brazilian track cannot be empty" in errors
    assert "Original artist cannot be empty" in errors
    assert "Original track cannot be empty" in errors


def test_validate_track_pair_rejects_whitespace_only_fields() -> None:
    """Test that validate_track_pair rejects whitespace-only fields."""
    pair = TrackPair(
        brazilian_artist="   ",
        brazilian_track="\t",
        original_artist="\n",
        original_track="  \t  ",
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
        in_playlist=False,
    )

    errors = validate_track_pair(pair)

    assert len(errors) == 4
