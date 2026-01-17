from typing import NotRequired
from typing import TypedDict


class TrackPair(TypedDict):
    """Track pair: Brazilian Forró cover + original English song."""

    brazilian_artist: str
    brazilian_track: str
    original_artist: str
    original_track: str
    added_at: NotRequired[str]  # ISO timestamp, set when saving to CSV
