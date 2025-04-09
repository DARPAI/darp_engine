from pathlib import Path

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


parent_folder = Path(__file__).parent.parent


class ServerJson(BaseModel):
    name: str
    description: str
    url: str = Field(alias="endpoint")
    logo: str | None = None

    @field_validator("url")  # noqa
    @classmethod
    def url_ignore_anchor(cls, value: str) -> str:
        return value.split("#")[0]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_ignore_empty=True)

    registry_url: str = "http://registry:80"
    log_dir: Path = Path("logs")
    mcp_port: int = 80
    llm_proxy: str | None = None
    openai_api_base: str = "https://api.openai.com/v1"
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    server_json: ServerJson = ServerJson.model_validate_json(
        Path(parent_folder / "server.json").read_text()
    )
    log_level: str = "INFO"


settings = Settings()
