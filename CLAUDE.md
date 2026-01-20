# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spotify Assistant is a CLI tool for creating Spotify playlists with Brazilian cover + original song pairs. Currently supports **Forró** and **Brega** genres.

### Supported Playlists

| Genre | Playlist ID | Data File |
|-------|-------------|-----------|
| Forró | `5GPUwEgfNguHbfwODwtkw1` | `forro_pairs.csv` |
| Brega | `6sJ94BPtTWlF9I2cxh0PTK` | `brega_pairs.csv` |

### Main Flows
1. **CSV Dataset Builder** — Manage a CSV with track pairs (brazilian artist/track + original artist/track)
2. **Playlist Builder** — Read CSV → search Spotify → create playlist with pairs in order

### Switching Playlists
Set `TARGET_PLAYLIST_ID` and `TRACK_PAIRS_FILENAME` in `.env` to switch between genres.

## Commands

```bash
# Package management (using uv)
uv add <package>              # Add dependency
uv run python <script>        # Run Python script
uv run pytest                 # Run all tests
uv run pytest tests/test_file.py::test_name  # Run single test

# Linting and type checking
uv run ruff check .           # Lint
uv run ruff check --fix .     # Lint with auto-fix
uv run ruff format .          # Format code
uv run mypy spotify_assistant/  # Type check

# Pre-commit hooks
pre-commit run --all-files    # Run all hooks manually
```

## Code Style

- **Python 3.13+** required
- **Type hints**: All `spotify_assistant/` code must have full type coverage
- **Modern syntax**: Use `str | None` (not `Optional`), `list` (not `List`), `dict` (not `Dict`)
- **KISS**: Prefer pure functions and dataclasses over classes
- **TypedDict**: Use for all structured data (API payloads, configs) — place in `spotify_assistant/models/`
- **Pydantic BaseModel**: Use for FastStream/message broker schemas
- **Forbidden**: `dict[str, Any]`, untyped `JSONResponse`
- **Imports**: Single-line imports enforced by ruff isort

## Configuration

- Settings defined in `spotify_assistant/settings.py` using Pydantic
- Environment values loaded from `.env`
- **Secrets**: Always read secrets via `settings` object, never use `os.getenv()` directly

## Testing

- Naming pattern: `test_<function>_<scenario>` (e.g., `test_search_track_when_not_found`)
- Every FastAPI endpoint needs a smoke test
- Mock external I/O (Spotify API, databases)
- Target: 90% coverage minimum
