import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotify_assistant.models.spotify import SpotifyTrack
from spotify_assistant.settings import settings

PLAYLIST_SCOPES = [
    "playlist-modify-public",
    "playlist-modify-private",
]

_client: spotipy.Spotify | None = None


def get_spotify_client() -> spotipy.Spotify:
    """Get or create Spotify client using OAuth flow.

    Uses a cached client instance to avoid repeated auth prompts.
    """
    global _client
    if _client is None:
        auth_manager = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=" ".join(PLAYLIST_SCOPES),
            cache_path=".cache",
        )
        _client = spotipy.Spotify(auth_manager=auth_manager)
    return _client


def search_track(track_name: str, artist: str) -> SpotifyTrack | None:
    """Search for a track on Spotify by name and artist.

    Returns track info if found, None otherwise.
    """
    client = get_spotify_client()
    query = f"track:{track_name} artist:{artist}"
    results = client.search(q=query, type="track", limit=1)
    if results is None or "tracks" not in results:
        return None

    items = results["tracks"]["items"]
    if not items:
        return None

    track = items[0]
    return SpotifyTrack(
        id=track["id"],
        name=track["name"],
        artist=track["artists"][0]["name"],
        uri=track["uri"],
        url=track["external_urls"]["spotify"],
    )


def add_tracks_to_playlist(playlist_id: str, track_uris: list[str]) -> None:
    """Add tracks to a Spotify playlist."""
    if not track_uris:
        return
    client = get_spotify_client()
    client.playlist_add_items(playlist_id, track_uris)
