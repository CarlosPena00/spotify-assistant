# Brazilian Cover Playlist Builder

A Python tool that creates Spotify playlists pairing Brazilian music covers with their original international hits. Supports **Forró**, **Brega**, and **Não Entendi na 5ª Série** (comedy/double-entendre).

## The Playlists

### Forró Inventou Tudo: O Resto é Cover

[![Spotify Playlist](https://img.shields.io/badge/Spotify-Forró_Playlist-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://open.spotify.com/playlist/5GPUwEgfNguHbfwODwtkw1)

**[Forró Inventou Tudo: O Resto é Cover](https://open.spotify.com/playlist/5GPUwEgfNguHbfwODwtkw1)** — 144 tracks | ~9 hours

Inspired by Lucas Uchoa's "Música Original / Versão em Forró" concept, this playlist celebrates the Brazilian tradition of transforming international hits into Forró anthems with accordion, zabumba, and triangle.

| Forró Artist | Forró Track | Original Artist | Original Track |
|--------------|-------------|-----------------|----------------|
| Calcinha Preta | Louca Por Ti | Kansas | Dust in the Wind |
| Forró da Brucelose | Te Quero Mais | Guns N' Roses | Sweet Child O' Mine |
| Forró Estourado | Liga o Som | Nirvana | Come As You Are |
| Aviões do Forró | Blá Blá Blá | Natalie Imbruglia | Torn |
| Calcinha Preta | Hoje à Noite | Heart | Alone |

### Brega Inventou Tudo: O Resto é Cover

[![Spotify Playlist](https://img.shields.io/badge/Spotify-Brega_Playlist-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://open.spotify.com/playlist/6sJ94BPtTWlF9I2cxh0PTK)

**[Brega Inventou Tudo: O Resto é Cover](https://open.spotify.com/playlist/6sJ94BPtTWlF9I2cxh0PTK)**

Brega, originating from Recife (Pernambuco) and Belém (Pará), has its own tradition of reimagining international pop hits with synthesizers and tecnobrega beats.

| Brega Artist | Brega Track | Original Artist | Original Track |
|--------------|-------------|-----------------|----------------|
| Banda DJavú | Porque te quero amor | Beyoncé | Halo |
| AR-15 | Sempre Te Amarei | Hoobastank | The Reason |
| Fruto Sensual | Está no Ar | Bonnie Tyler | Total Eclipse of the Heart |
| Companhia do Tecno | Sonhar | Van Halen | Dreams |
| Sedutora | Bateu a química | Miley Cyrus | Wrecking Ball |

## Motivation

In Brazilian popular music, bands have a long tradition of adapting international pop and rock hits, translating lyrics to Portuguese and reimagining them with regional styles. These covers often became massive hits in their own right, sometimes eclipsing the originals in popularity within Brazil.

This project automates the curation of these musical pairs, making it easy to discover:
- How international hits transform into Brazilian regional styles
- The creative liberties taken in Portuguese adaptations
- The breadth of genres covered: from Guns N' Roses to Britney Spears, Nirvana to Lady Gaga

### Não Entendi na 5ª Série

[![Spotify Playlist](https://img.shields.io/badge/Spotify-Comedy_Playlist-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://open.spotify.com/playlist/4WiFm0EqBnmJbD7Pqs4nRU)

**[Não Entendi na 5ª Série](https://open.spotify.com/playlist/4WiFm0EqBnmJbD7Pqs4nRU)**

Brazilian comedy classics with double-entendre lyrics — the songs you sang as a kid without realizing what they actually meant. From Genival Lacerda's forró classics to Mamonas Assassinas' absurdist rock. Your brain is now officially off.

## Data Summary

| Genre | Tracks | Data File | Flow |
|-------|--------|-----------|------|
| Forró | 72 pairs | `forro_pairs.csv` | cover + original |
| Brega | 31 pairs | `brega_pairs.csv` | cover + original |
| Comedy | — | `comedy_tracks.csv` | single track |

## How It Works

**Cover playlists (Forró, Brega):**
```
CSV (forro_pairs.csv / brega_pairs.csv)
                    ↓
            Search Spotify API
             (cover + original)
                    ↓
         Add both tracks to playlist
                    ↓
            Update CSV status
```

**Comedy playlist:**
```
CSV (comedy_tracks.csv)
                    ↓
            Search Spotify API
                    ↓
          Add track to playlist
                    ↓
            Update CSV status
```

1. **Dataset Management**: Maintain a CSV of tracks/pairs with metadata
2. **Spotify Search**: Query the API for each track
3. **Playlist Building**: Add matched tracks sequentially to the target playlist
4. **Status Tracking**: Mark which tracks were found and added

## Configuration

Set environment variables in `.env` to switch between playlists:

```bash
# Forró (cover + original pairs) → main.py
TARGET_PLAYLIST_ID="5GPUwEgfNguHbfwODwtkw1"
TRACK_PAIRS_FILENAME="forro_pairs.csv"

# Brega (cover + original pairs) → main.py
TARGET_PLAYLIST_ID="6sJ94BPtTWlF9I2cxh0PTK"
TRACK_PAIRS_FILENAME="brega_pairs.csv"

# Não Entendi na 5ª Série (single tracks) → main_comedy.py
TARGET_PLAYLIST_ID="4WiFm0EqBnmJbD7Pqs4nRU"
TRACK_PAIRS_FILENAME="comedy_tracks.csv"
```

## Tech Stack

- **Python 3.13+**
- **Spotipy** — Spotify Web API wrapper
- **Pandas** — CSV operations
- **Pydantic** — Settings and validation
- **Loguru** — Logging

## Usage

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Add your Spotify API credentials

# Run the playlist builder (Forró / Brega)
uv run python -m spotify_assistant.main

# Run the comedy playlist builder
uv run python -m spotify_assistant.main_comedy
```

## Development

```bash
# Run tests
uv run pytest

# Type checking
uv run mypy spotify_assistant/

# Linting
uv run ruff check .
uv run ruff format .
```

## Contributing

Know a Forró or Brega cover that's missing? Open an issue or PR with:
- Brazilian artist and track name
- Original artist and track name
- Genre (Forró or Brega)
- Source URL (if available)
