ROLE / CONTEXT

You are my Senior Software Engineer + Prompt Engineering expert.
Your mission is to help me build high-quality, production-ready code with excellent architecture, clean commits, strong typing, and testability.

We are building a project composed of tools that interact with the Spotify Web API.


PROJECT GOAL

Create a Spotify playlist where songs always come in pairs:

1) Brazilian Forró version (ex: Calcinha Preta)
2) Original song (usually English / Rock / Pop)

Example playlist ordering:

Tuple 1:
- Calcinha Preta — O Navio e o Mar
- Scorpions — Send Me an Angel

Tuple 2:
- Mulheres Perdidas — Salve o Nosso Amor
- Skid Row — I Remember You

Tuple 3:
- Calcinha Preta — Hoje a Noite
- Heart — Alone

Tuple N:
- Calcinha Preta — Agora Estou Sofrendo
- Angra — Bleeding Heart

Important:
It does NOT need to be the official/original recording.
It only needs to be a highly inspired version (a valid “pair”).


MAIN FLOWS

Flow 1 — Build Dataset (CSV)
We need a tool to help populate a CSV with pairs.

Each row must contain:
- brazil_artist
- brazil_track
- original_artist
- original_track

Optional useful columns:
- notes
- source_link
- confidence_score


Flow 2 — Validate + Create Playlist from CSV
Given the CSV:

1) Search Spotify for both songs
2) If both exist → add to playlist in order:
   - Brazilian track first
   - Original track second
3) If one is missing:
   - log the failure with details
   - do NOT break the pipeline


REQUIREMENTS

Functional:
- Spotify auth (OAuth) must be supported
- Must search tracks robustly (artist + track)
- Handle ambiguous results (multiple matches)
- Must avoid duplicates inside playlist
- Must respect Spotify rate limits (retry/backoff)

Non-functional:
- Clean architecture (services, clients, models)
- Strong typing (Python type hints)
- Logging (structured logs preferred)
- CLI-friendly (commands like populate-csv, build-playlist)
- Tests for core logic (mock Spotify API)
- Configuration via .env or config file


DELIVERABLES (Step-by-step)

Step 1 — Project Structure Proposal
Propose a folder structure like:
- src/spotify_pairs/...
- tests/...
- pyproject.toml
- .env
- README.md

Step 2 — Data Model
Define typed models:
- TrackPair
- SpotifyTrackResult
- PlaylistBuildReport

Step 3 — Spotify Client
Implement a Spotify client wrapper that supports:
- search track
- create playlist
- add tracks
- get playlist tracks (for dedupe)

Step 4 — CSV Pipeline
Implement:
- CSV read/write
- validation
- normalization (case folding, trimming, accents)

Step 5 — Playlist Builder
Implement a pipeline:
Input: CSV
Output: playlist URL + report

Report must include:
- total pairs
- pairs added
- missing brazil tracks
- missing original tracks
- ambiguous matches
- duplicates skipped


OUTPUT FORMAT RULES

When you answer:

1) Start with a short plan (bullets)
2) Then provide the code in complete files (not fragments)
3) Use clean commit-message style suggestions when appropriate
4) If something is unclear, make reasonable assumptions and continue
5) Prefer simple, maintainable solutions over clever ones


TECH STACK

Use Python 3.13+.

Preferred libraries:
- spotipy (if good fit) OR direct requests to Spotify API
- pydantic for models
- typer for CLI
- pytest for tests
- python-dotenv for env loading
