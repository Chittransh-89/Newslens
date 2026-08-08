from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NewsLens API"
    allowed_origins: str = "http://localhost:3000"
    request_timeout_seconds: float = 12.0
    user_agent: str = "NewsLens/1.0 (+https://github.com)"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        """Return the configured comma-separated browser origins as a clean list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Create and cache application settings loaded from environment variables."""
    return Settings()
