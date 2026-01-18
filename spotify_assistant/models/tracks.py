from typing import TypedDict


class TrackPair(TypedDict):
    """Track pair: Brazilian Forró cover + original English song."""

    brazilian_artist: str
    brazilian_track: str
    original_artist: str
    original_track: str
    added_at: str | None  # ISO timestamp, set when saving to CSV
    source: str | None  # URL source where the pair was found
    brazilian_has_spotify: bool | None  # True, False, or None (not checked)
    original_has_spotify: bool | None  # True, False, or None (not checked)
