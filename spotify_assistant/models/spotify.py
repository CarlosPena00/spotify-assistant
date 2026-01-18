from typing import TypedDict


class SpotifyTrack(TypedDict):
    """Spotify track search result."""

    id: str
    name: str
    artist: str
    uri: str  # spotify:track:xxx format for playlist creation
    url: str  # https://open.spotify.com/track/xxx web URL
