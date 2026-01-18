from pathlib import Path
from typing import TypedDict

from spotify_assistant.clients.spotify import add_tracks_to_playlist
from spotify_assistant.clients.spotify import search_track
from spotify_assistant.models.spotify import SpotifyTrack
from spotify_assistant.models.tracks import TrackPair
from spotify_assistant.services.csv_manager import read_track_pairs
from spotify_assistant.services.csv_manager import update_track_pair

TARGET_PLAYLIST_ID = "5GPUwEgfNguHbfwODwtkw1"


class ValidationResult(TypedDict):
    pair: TrackPair
    index: int
    brazilian_found: bool | None
    original_found: bool | None
    skipped: bool


def validate_track_availability(
    csv_path: Path, dry_run: bool = False
) -> list[ValidationResult]:
    """Validate Spotify availability for track pairs and update CSV.

    For each track pair:
    1. If brazilian_has_spotify is already False, skip
    2. Search for Brazilian track - if not found, mark as False and skip
    3. If Brazilian found, search for original - if not found, mark as False
    4. Update CSV with availability status
    """
    pairs = read_track_pairs(csv_path)
    results: list[ValidationResult] = []

    for idx, pair in enumerate(pairs):
        result: ValidationResult = {
            "pair": pair,
            "index": idx,
            "brazilian_found": None,
            "original_found": None,
            "skipped": False,
        }

        # Skip if already marked as unavailable
        if pair["brazilian_has_spotify"] is False:
            result["skipped"] = True
            results.append(result)
            continue

        # Search Brazilian track
        brazilian = search_track(pair["brazilian_track"], pair["brazilian_artist"])
        if not brazilian:
            result["brazilian_found"] = False
            pair["brazilian_has_spotify"] = False
            if not dry_run:
                update_track_pair(csv_path, idx, pair)
            results.append(result)
            continue

        # Brazilian found
        result["brazilian_found"] = True
        pair["brazilian_has_spotify"] = True

        # Skip original search if already marked unavailable
        if pair["original_has_spotify"] is False:
            if not dry_run:
                update_track_pair(csv_path, idx, pair)
            result["skipped"] = True
            results.append(result)
            continue

        # Search original track
        original = search_track(pair["original_track"], pair["original_artist"])
        if not original:
            result["original_found"] = False
            pair["original_has_spotify"] = False
        else:
            result["original_found"] = True
            pair["original_has_spotify"] = True

        if not dry_run:
            update_track_pair(csv_path, idx, pair)
        results.append(result)

    return results


class ProcessResult(TypedDict):
    pair: TrackPair
    index: int
    brazilian_track: SpotifyTrack | None
    original_track: SpotifyTrack | None
    added_to_playlist: bool


def process_track_pair(pair: TrackPair, index: int) -> ProcessResult:
    """Search for both tracks, return results without side effects."""
    brazilian = search_track(pair["brazilian_track"], pair["brazilian_artist"])
    original = search_track(pair["original_track"], pair["original_artist"])
    return {
        "pair": pair,
        "index": index,
        "brazilian_track": brazilian,
        "original_track": original,
        "added_to_playlist": False,
    }


def build_playlist_from_csv(csv_path: Path, playlist_id: str) -> list[ProcessResult]:
    """Main orchestration: read CSV, search tracks, add to playlist, update CSV."""
    pairs = read_track_pairs(csv_path)
    results: list[ProcessResult] = []
    for idx, pair in enumerate(pairs):
        if pair["in_playlist"]:
            continue
        if (
            pair["brazilian_has_spotify"] is False
            or pair["original_has_spotify"] is False
        ):
            continue
        res = process_track_pair(pair, idx)
        # Update CSV if not found
        changed = False
        if not res["brazilian_track"]:
            pair["brazilian_has_spotify"] = False
            changed = True
        if not res["original_track"]:
            pair["original_has_spotify"] = False
            changed = True
        if changed:
            update_track_pair(csv_path, idx, pair)
            res["added_to_playlist"] = False
            results.append(res)
            continue
        # Add to playlist
        if res["brazilian_track"] and res["original_track"]:
            add_tracks_to_playlist(
                playlist_id,
                [res["brazilian_track"]["uri"], res["original_track"]["uri"]],
            )
            pair["in_playlist"] = True
            update_track_pair(csv_path, idx, pair)
            res["added_to_playlist"] = True
        results.append(res)
    return results
