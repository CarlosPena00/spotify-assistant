import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spotify_assistant.models.spotify import SpotifyTrack
from spotify_assistant.settings import settings


def get_spotify_client() -> spotipy.Spotify:
    """Create authenticated Spotify client using client credentials flow."""
    auth_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


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
