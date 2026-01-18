# Spotify API Reference

## Search Track Response

Response from `client.search(q=query, type="track", limit=1)`:

```py
{
    "tracks": {
        "href": "https://api.spotify.com/v1/search?offset=0&limit=1&query=track%3AAgora%20Estou%20Sofrendo%20artist%3ACalcinha%20Preta&type=track",
        "limit": 1,
        "next": None,
        "offset": 0,
        "previous": None,
        "total": 0,
        "items": [
            {
                "album": {
                    "album_type": "album",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/6Kps94g1Npexh3LrinIOvC"
                            },
                            "href": "https://api.spotify.com/v1/artists/6Kps94g1Npexh3LrinIOvC",
                            "id": "6Kps94g1Npexh3LrinIOvC",
                            "name": "Calcinha Preta",
                            "type": "artist",
                            "uri": "spotify:artist:6Kps94g1Npexh3LrinIOvC",
                        }
                    ],
                    "available_markets": ["AR", ...],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/album/7Gsa8Q0NbrI7eDQBdLAHyP"
                    },
                    "href": "https://api.spotify.com/v1/albums/7Gsa8Q0NbrI7eDQBdLAHyP",
                    "id": "7Gsa8Q0NbrI7eDQBdLAHyP",
                    "images": [
                        {
                            "height": 640,
                            "width": 640,
                            "url": "https://i.scdn.co/image/ab67616d0000b273f83a34b012596419d97a37da",
                        },
                        {
                            "height": 300,
                            "width": 300,
                            "url": "https://i.scdn.co/image/ab67616d00001e02f83a34b012596419d97a37da",
                        },
                        {
                            "height": 64,
                            "width": 64,
                            "url": "https://i.scdn.co/image/ab67616d00004851f83a34b012596419d97a37da",
                        },
                    ],
                    "is_playable": True,
                    "name": "CP 25 Anos (Ao Vivo em Aracaju)",
                    "release_date": "2020-12-08",
                    "release_date_precision": "day",
                    "total_tracks": 21,
                    "type": "album",
                    "uri": "spotify:album:7Gsa8Q0NbrI7eDQBdLAHyP",
                },
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/6Kps94g1Npexh3LrinIOvC"
                        },
                        "href": "https://api.spotify.com/v1/artists/6Kps94g1Npexh3LrinIOvC",
                        "id": "6Kps94g1Npexh3LrinIOvC",
                        "name": "Calcinha Preta",
                        "type": "artist",
                        "uri": "spotify:artist:6Kps94g1Npexh3LrinIOvC",
                    },
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/7MiDcPa6UiV3In7lIM71IN"
                        },
                        "href": "https://api.spotify.com/v1/artists/7MiDcPa6UiV3In7lIM71IN",
                        "id": "7MiDcPa6UiV3In7lIM71IN",
                        "name": "Gusttavo Lima",
                        "type": "artist",
                        "uri": "spotify:artist:7MiDcPa6UiV3In7lIM71IN",
                    },
                ],
                "available_markets": ["AR", ...],
                "disc_number": 1,
                "duration_ms": 260510,
                "explicit": False,
                "external_ids": {"isrc": "BCFZF2000012"},
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/006rHBBNLJMpQs8fRC2GDe"
                },
                "href": "https://api.spotify.com/v1/tracks/006rHBBNLJMpQs8fRC2GDe",
                "id": "006rHBBNLJMpQs8fRC2GDe",
                "is_local": False,
                "is_playable": True,
                "name": "Agora Estou Sofrendo - Ao Vivo",
                "popularity": 56,
                "preview_url": None,
                "track_number": 4,
                "type": "track",
                "uri": "spotify:track:006rHBBNLJMpQs8fRC2GDe",
            }
        ],
    }
}
```

### Fields Used by `search_track()`

From `tracks.items[0]`:

| Field | Description |
|-------|-------------|
| `id` | Spotify track ID |
| `name` | Track name |
| `artists[0].name` | Primary artist name |
| `uri` | Spotify URI (e.g., `spotify:track:xxx`) |
| `external_urls.spotify` | Web URL (e.g., `https://open.spotify.com/track/xxx`) |
