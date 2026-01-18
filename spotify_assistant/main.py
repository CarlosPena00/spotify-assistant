# uv run python -m spotify_assistant.main
import time

import pandas as pd

from spotify_assistant.clients.spotify import add_tracks_to_playlist
from spotify_assistant.clients.spotify import search_track
from spotify_assistant.settings import settings

dtypes = {
    "brazilian_artist": "string",
    "brazilian_track": "string",
    "original_artist": "string",
    "original_track": "string",
    "added_at": "string",
    "source": "string",
    "brazilian_has_spotify": "boolean",
    "original_has_spotify": "boolean",
    "in_playlist": "boolean",
}
dataset = pd.read_csv(
    settings.track_pairs_path,
    low_memory=False,
    dtype=dtypes,  # type: ignore
    keep_default_na=True,
    na_values=["", "null", "None"],
)

new_dataset = []
for _, data in dataset.iterrows():
    if data.in_playlist is True:
        new_dataset.append(data)
        continue
    print(
        f"{data.brazilian_artist} - {data.brazilian_track} -> "
        f"{data.original_artist} - {data.original_track}"
    )
    if not pd.isna(data.brazilian_has_spotify):
        continue
    result_brazilian = search_track(
        track_name=data.brazilian_track,
        artist=data.brazilian_artist,
    )
    if not result_brazilian:
        data["brazilian_has_spotify"] = False
        new_dataset.append(data)
        print("Not found on Spotify.")
        continue
    if not pd.isna(data.original_has_spotify):
        continue
    result_original = search_track(
        track_name=data.original_track,
        artist=data.original_artist,
    )
    if result_original is None:
        data["original_has_spotify"] = False
        new_dataset.append(data)
        print("Not found on Spotify.")
        continue
    data["brazilian_has_spotify"] = True
    data["original_has_spotify"] = True
    result = add_tracks_to_playlist(
        playlist_id=settings.TARGET_PLAYLIST_ID,
        track_uris=[result_brazilian["uri"], result_original["uri"]],
    )
    data["in_playlist"] = result is not None
    new_dataset.append(data)
    print(data)
    time.sleep(0.3)

pd.DataFrame(new_dataset).to_csv(settings.track_pairs_path, index=False)
