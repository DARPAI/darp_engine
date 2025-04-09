from typing import Any

from openai.types.chat import ChatCompletionMessage
from openai.types.chat import ChatCompletionToolMessageParam
from pydantic import BaseModel
from pydantic import ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Tool(BaseSchema):
    name: str
    description: str
    input_schema: dict[str, Any]


class RegistryServer(BaseSchema):
    name: str
    description: str
    url: str
    logo: str | None
    id: int
    tools: list[Tool]


class ToolInfo(BaseSchema):
    tool_name: str
    server: RegistryServer


class RoutingResponse(BaseSchema):
    conversation: list[ChatCompletionMessage | ChatCompletionToolMessageParam]
