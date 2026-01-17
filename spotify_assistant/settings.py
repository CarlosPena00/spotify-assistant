from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str

    DATA_DIR: Path = Path("data")
    TRACK_PAIRS_FILENAME: str = "track_pairs.csv"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def track_pairs_path(self) -> Path:
        """Get the full path to the track pairs CSV file."""
        return self.DATA_DIR / self.TRACK_PAIRS_FILENAME


settings = Settings()  # type: ignore
