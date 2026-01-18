# Forró Inventou Tudo: O Resto é Cover

A Python tool that creates Spotify playlists pairing Brazilian Forró covers with their original international hits.

[![Spotify Playlist](https://img.shields.io/badge/Spotify-Playlist-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://open.spotify.com/playlist/5GPUwEgfNguHbfwODwtkw1)

## The Playlist

**[Forró Inventou Tudo: O Resto é Cover](https://open.spotify.com/playlist/5GPUwEgfNguHbfwODwtkw1)** — 144 tracks | ~9 hours

Inspired by Lucas Uchoa's "Música Original / Versão em Forró" concept, this playlist celebrates the Brazilian tradition of transforming international hits into Forró anthems.

### What's Inside

Each pair features the **Forró cover** followed by its **original version**:

| Forró Artist | Forró Track | Original Artist | Original Track |
|--------------|-------------|-----------------|----------------|
| Calcinha Preta | Louca Por Ti | Kansas | Dust in the Wind |
| Forró da Brucelose | Te Quero Mais | Guns N' Roses | Sweet Child O' Mine |
| Forró Estourado | Liga o Som | Nirvana | Come As You Are |
| Aviões do Forró | Blá Blá Blá | Natalie Imbruglia | Torn |
| Calcinha Preta | Hoje à Noite | Heart | Alone |
| Aline Mel e Forró na Veia | Dona do Prazer | Britney Spears | Toxic |
| Noda de Caju | Lindos Momentos | Cyndi Lauper | Time After Time |

## Motivation

In Brazilian Forró culture, bands have a long tradition of adapting international pop and rock hits, translating lyrics to Portuguese and reimagining the songs with accordion, zabumba, and triangle. These covers became massive hits in their own right, sometimes eclipsing the originals in popularity within Brazil.

This project automates the curation of these musical pairs, making it easy to discover:
- How a power ballad transforms into a Forró romântico
- The creative liberties taken in Portuguese adaptations
- The breadth of genres covered: from Guns N' Roses to Britney Spears, Nirvana to ABBA

## Data Insights

**72 track pairs** curated from:
- Existing Spotify playlists
- Brazilian music journalism (iBahia, Jornal da Paraíba, Aratu On)
- Fan-contributed sources

**Top Forró Artists by Covers:**
- Calcinha Preta (23 covers)
- Desejo De Menina (7 covers)
- Forrozão Tropykália (6 covers)
- Limão com Mel (6 covers)

**Original Artists Covered:**
- Rock legends: Guns N' Roses, Nirvana, Scorpions, Europe, Heart, Aerosmith
- Pop icons: Britney Spears, Rihanna, Beyoncé, Lady Gaga, Bruno Mars
- Classic artists: ABBA, Air Supply, Simon & Garfunkel, Bee Gees

## How It Works

```
CSV Dataset (track_pairs.csv)
         ↓
    Load pairs
         ↓
  Search Spotify API
   (cover + original)
         ↓
   Add to playlist
         ↓
  Update CSV status
```

1. **Dataset Management**: Maintain a CSV of track pairs with metadata
2. **Spotify Search**: Query the API for both the Forró cover and original
3. **Playlist Building**: Add matched pairs sequentially to the target playlist
4. **Status Tracking**: Mark which pairs were found and added

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

# Run the playlist builder
uv run python -m spotify_assistant.main
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

Know a Forró cover that's missing? Open an issue or PR with:
- Brazilian artist and track name
- Original artist and track name
- Source URL (if available)
