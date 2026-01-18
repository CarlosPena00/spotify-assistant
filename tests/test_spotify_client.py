from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

import spotify_assistant.clients.spotify as spotify_module
from spotify_assistant.clients.spotify import get_spotify_client
from spotify_assistant.clients.spotify import search_track


@pytest.fixture(autouse=True)
def reset_spotify_client():
    """Reset the cached Spotify client before each test."""
    spotify_module._client = None
    yield
    spotify_module._client = None


@pytest.fixture
def mock_search_response() -> dict:
    """Return a mock Spotify search response."""
    return {
        "tracks": {
            "items": [
                {
                    "id": "abc123",
                    "name": "Umbrella",
                    "artists": [{"name": "Rihanna"}],
                    "uri": "spotify:track:abc123",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/abc123"
                    },
                }
            ]
        }
    }


@pytest.fixture
def mock_empty_search_response() -> dict:
    """Return a mock Spotify search response with no results."""
    return {"tracks": {"items": []}}


def test_search_track_returns_track_when_found(mock_search_response: dict) -> None:
    """Test that search_track returns SpotifyTrack when track is found."""
    with patch(
        "spotify_assistant.clients.spotify.get_spotify_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_client.search.return_value = mock_search_response
        mock_get_client.return_value = mock_client

        result = search_track("Umbrella", "Rihanna")

        assert result is not None
        assert result["id"] == "abc123"
        assert result["name"] == "Umbrella"
        assert result["artist"] == "Rihanna"
        assert result["uri"] == "spotify:track:abc123"
        assert result["url"] == "https://open.spotify.com/track/abc123"
        mock_client.search.assert_called_once_with(
            q="track:Umbrella artist:Rihanna", type="track", limit=1
        )


def test_search_track_returns_none_when_not_found(
    mock_empty_search_response: dict,
) -> None:
    """Test that search_track returns None when no track is found."""
    with patch(
        "spotify_assistant.clients.spotify.get_spotify_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_client.search.return_value = mock_empty_search_response
        mock_get_client.return_value = mock_client

        result = search_track("NonExistent Track", "Unknown Artist")

        assert result is None


def test_search_track_uses_first_result_when_multiple(
    mock_search_response: dict,
) -> None:
    """Test that search_track uses the first result when multiple are returned."""
    mock_search_response["tracks"]["items"].append(
        {
            "id": "def456",
            "name": "Umbrella (Remix)",
            "artists": [{"name": "Rihanna"}],
            "uri": "spotify:track:def456",
            "external_urls": {"spotify": "https://open.spotify.com/track/def456"},
        }
    )

    with patch(
        "spotify_assistant.clients.spotify.get_spotify_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_client.search.return_value = mock_search_response
        mock_get_client.return_value = mock_client

        result = search_track("Umbrella", "Rihanna")

        assert result is not None
        assert result["id"] == "abc123"  # First result


def test_get_spotify_client_uses_oauth() -> None:
    """Test that get_spotify_client uses OAuth from settings."""
    oauth_path = "spotify_assistant.clients.spotify.SpotifyOAuth"
    spotify_path = "spotify_assistant.clients.spotify.spotipy.Spotify"
    settings_path = "spotify_assistant.clients.spotify.settings"
    with (
        patch(oauth_path) as mock_oauth,
        patch(spotify_path) as mock_spotify,
        patch(settings_path) as mock_settings,
    ):
        mock_settings.SPOTIFY_CLIENT_ID = "test_client_id"
        mock_settings.SPOTIFY_CLIENT_SECRET = "test_client_secret"
        mock_settings.SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

        get_spotify_client()

        mock_oauth.assert_called_once_with(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8888/callback",
            scope="playlist-modify-public playlist-modify-private",
            cache_path=".cache",
        )
        mock_spotify.assert_called_once()
