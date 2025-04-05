from typing import Any

from pydantic import ConfigDict
from pydantic import Field

from registry.src.base_schema import BaseSchema


class Tool(BaseSchema):
    model_config = ConfigDict(populate_by_name=True, **BaseSchema.model_config)
    name: str
    description: str
    input_schema: dict[str, Any] = Field(validation_alias="inputSchema")


class ServerCreate(BaseSchema):
    name: str
    description: str
    url: str
    logo: str


class ServerRead(ServerCreate):
    id: int


class ServerWithTools(ServerRead):
    tools: list[Tool]


class ServerUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    url: str | None = None
    logo: str | None = None
