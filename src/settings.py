from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    database_url: str
    db_pool_size: int = 50
    db_max_overflow: int = 25
    log_dir: Path = Path("logs")

    @property
    def database_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.database_url}"

    @property
    def database_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.database_url}"


settings = Settings()
