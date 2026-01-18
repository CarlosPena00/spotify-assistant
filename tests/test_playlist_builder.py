from spotify_assistant.models.spotify import SpotifyTrack
from spotify_assistant.models.tracks import TrackPair
from spotify_assistant.services.playlist_builder import build_playlist_from_csv
from spotify_assistant.services.playlist_builder import process_track_pair
from spotify_assistant.services.playlist_builder import validate_track_availability


def dummy_search_track(track_name, artist):
    if "notfound" in track_name.lower():
        return None
    return SpotifyTrack(
        id="dummyid",
        name=track_name,
        artist=artist,
        uri=f"spotify:track:{track_name}",
        url=f"https://open.spotify.com/track/{track_name}",
    )


def test_process_track_pair_found(monkeypatch):
    pair = TrackPair(
        brazilian_artist="A",
        brazilian_track="B",
        original_artist="C",
        original_track="D",
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
        in_playlist=False,
    )
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )
    res = process_track_pair(pair, 0)
    assert res["brazilian_track"] is not None
    assert res["original_track"] is not None
    assert not res["added_to_playlist"]


def test_process_track_pair_not_found(monkeypatch):
    pair = TrackPair(
        brazilian_artist="A",
        brazilian_track="NotFound",
        original_artist="C",
        original_track="D",
        added_at=None,
        source=None,
        brazilian_has_spotify=None,
        original_has_spotify=None,
        in_playlist=False,
    )
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )
    res = process_track_pair(pair, 0)
    assert res["brazilian_track"] is None
    assert res["original_track"] is not None


def test_build_playlist_from_csv_adds_to_playlist(tmp_path, monkeypatch):
    """Test that build_playlist_from_csv adds tracks and updates CSV."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="B",
            original_artist="C",
            original_track="D",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        ),
        TrackPair(
            brazilian_artist="A2",
            brazilian_track="NotFound",
            original_artist="C2",
            original_track="D2",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        ),
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.add_tracks_to_playlist",
        lambda *a, **k: None,
    )

    results = build_playlist_from_csv(csv_path, "playlistid")
    after = read_track_pairs(csv_path)
    # First pair found - added to playlist
    assert results[0]["brazilian_track"] is not None
    assert results[0]["added_to_playlist"] is True
    assert after[0]["in_playlist"] is True
    # Second pair not found - marked unavailable
    assert results[1]["brazilian_track"] is None
    assert after[1]["brazilian_has_spotify"] is False


def test_build_playlist_from_csv_marks_not_found(tmp_path, monkeypatch):
    """Test that build_playlist_from_csv marks tracks as not found."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="NotFound",
            original_artist="C",
            original_track="D",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.add_tracks_to_playlist",
        lambda *a, **k: None,
    )

    build_playlist_from_csv(csv_path, "playlistid")
    after = read_track_pairs(csv_path)
    assert after[0]["brazilian_has_spotify"] is False


def test_validate_track_availability_when_brazilian_not_found(tmp_path, monkeypatch):
    """When Brazilian track not found, marks as False and skips original."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="NotFound",
            original_artist="C",
            original_track="D",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )

    results = validate_track_availability(csv_path, dry_run=False)

    assert len(results) == 1
    assert results[0]["brazilian_found"] is False
    assert results[0]["original_found"] is None  # Skipped original search

    after = read_track_pairs(csv_path)
    assert after[0]["brazilian_has_spotify"] is False


def test_validate_track_availability_when_original_not_found(tmp_path, monkeypatch):
    """When Brazilian found but original not found, marks original_has_spotify=False."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="BrazilianTrack",
            original_artist="C",
            original_track="NotFound",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )

    results = validate_track_availability(csv_path, dry_run=False)

    assert len(results) == 1
    assert results[0]["brazilian_found"] is True
    assert results[0]["original_found"] is False

    after = read_track_pairs(csv_path)
    assert after[0]["brazilian_has_spotify"] is True
    assert after[0]["original_has_spotify"] is False


def test_validate_track_availability_when_both_found(tmp_path, monkeypatch):
    """When both tracks found, marks both as True."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="BrazilianTrack",
            original_artist="C",
            original_track="OriginalTrack",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )

    results = validate_track_availability(csv_path, dry_run=False)

    assert len(results) == 1
    assert results[0]["brazilian_found"] is True
    assert results[0]["original_found"] is True

    after = read_track_pairs(csv_path)
    assert after[0]["brazilian_has_spotify"] is True
    assert after[0]["original_has_spotify"] is True


def test_validate_track_availability_skips_already_marked_unavailable(
    tmp_path, monkeypatch
):
    """Skips pairs already marked as unavailable."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="Track",
            original_artist="C",
            original_track="D",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=False,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )

    results = validate_track_availability(csv_path, dry_run=False)

    assert len(results) == 1
    assert results[0]["skipped"] is True
    assert results[0]["brazilian_found"] is None
    assert results[0]["original_found"] is None


def test_validate_track_availability_dry_run(tmp_path, monkeypatch):
    """Dry run does not update CSV."""
    csv_path = tmp_path / "track_pairs.csv"
    pairs = [
        TrackPair(
            brazilian_artist="A",
            brazilian_track="NotFound",
            original_artist="C",
            original_track="D",
            added_at="2024-01-01T00:00:00Z",
            source=None,
            brazilian_has_spotify=None,
            original_has_spotify=None,
            in_playlist=False,
        )
    ]
    from spotify_assistant.services.csv_manager import read_track_pairs
    from spotify_assistant.services.csv_manager import write_track_pairs

    write_track_pairs(csv_path, pairs)
    monkeypatch.setattr(
        "spotify_assistant.services.playlist_builder.search_track", dummy_search_track
    )

    results = validate_track_availability(csv_path, dry_run=True)

    assert results[0]["brazilian_found"] is False
    after = read_track_pairs(csv_path)
    assert after[0]["brazilian_has_spotify"] is None  # Not updated
