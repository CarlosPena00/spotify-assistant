from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from spotify_assistant.cli import app
from spotify_assistant.services.csv_manager import read_track_pairs

runner = CliRunner()


@pytest.fixture
def temp_csv_path(tmp_path: Path) -> Path:
    """Return a temporary CSV path and patch settings."""
    return tmp_path / "track_pairs.csv"


def test_populate_csv_with_all_arguments_succeeds(temp_csv_path: Path) -> None:
    """Test populate-csv with all required arguments."""
    with patch("spotify_assistant.cli.settings") as mock_settings:
        mock_settings.track_pairs_path = temp_csv_path

        result = runner.invoke(
            app,
            [
                "populate-csv",
                "--brazilian-artist",
                "Falamansa",
                "--brazilian-track",
                "Xote dos Milagres",
                "--original-artist",
                "Dominguinhos",
                "--original-track",
                "Xote dos Milagres",
            ],
        )

    assert result.exit_code == 0
    assert "Added:" in result.output
    assert "Falamansa" in result.output

    rows = read_track_pairs(temp_csv_path)
    assert len(rows) == 1
    assert rows[0]["brazilian_artist"] == "Falamansa"


def test_populate_csv_with_short_options(temp_csv_path: Path) -> None:
    """Test populate-csv with short option flags."""
    with patch("spotify_assistant.cli.settings") as mock_settings:
        mock_settings.track_pairs_path = temp_csv_path

        result = runner.invoke(
            app,
            [
                "populate-csv",
                "-ba",
                "Falamansa",
                "-bt",
                "Xote dos Milagres",
                "-oa",
                "Dominguinhos",
                "-ot",
                "Xote dos Milagres",
            ],
        )

    assert result.exit_code == 0
    assert "Added:" in result.output


def test_populate_csv_missing_arguments_fails() -> None:
    """Test populate-csv fails when arguments are missing."""
    result = runner.invoke(
        app,
        [
            "populate-csv",
            "--brazilian-artist",
            "Falamansa",
        ],
    )

    assert result.exit_code == 2
    assert "Missing option" in result.output


def test_populate_csv_no_arguments_shows_error() -> None:
    """Test populate-csv with no arguments shows error."""
    result = runner.invoke(app, ["populate-csv"])

    assert result.exit_code == 2
    assert "Missing option" in result.output


def test_populate_csv_shows_duplicate_warning(temp_csv_path: Path) -> None:
    """Test populate-csv shows warning for duplicate entries."""
    with patch("spotify_assistant.cli.settings") as mock_settings:
        mock_settings.track_pairs_path = temp_csv_path

        # First entry
        runner.invoke(
            app,
            [
                "populate-csv",
                "-ba",
                "Falamansa",
                "-bt",
                "Xote dos Milagres",
                "-oa",
                "Dominguinhos",
                "-ot",
                "Xote dos Milagres",
            ],
        )

        # Duplicate entry
        result = runner.invoke(
            app,
            [
                "populate-csv",
                "-ba",
                "Falamansa",
                "-bt",
                "Xote dos Milagres",
                "-oa",
                "Dominguinhos",
                "-ot",
                "Xote dos Milagres",
            ],
        )

    assert result.exit_code == 1
    assert "Warning:" in result.output
    assert "already exists" in result.output


def test_populate_csv_validation_error(temp_csv_path: Path) -> None:
    """Test populate-csv shows validation errors for empty fields."""
    with patch("spotify_assistant.cli.settings") as mock_settings:
        mock_settings.track_pairs_path = temp_csv_path

        result = runner.invoke(
            app,
            [
                "populate-csv",
                "-ba",
                "Falamansa",
                "-bt",
                "   ",  # Whitespace only
                "-oa",
                "Dominguinhos",
                "-ot",
                "Xote dos Milagres",
            ],
        )

    assert result.exit_code == 1
    assert "Validation error" in result.output


def test_populate_csv_help() -> None:
    """Test populate-csv --help shows usage."""
    result = runner.invoke(app, ["populate-csv", "--help"])

    assert result.exit_code == 0
    assert "--brazilian-artist" in result.output
