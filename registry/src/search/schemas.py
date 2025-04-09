from pydantic import Field

from registry.src.base_schema import BaseSchema


class SearchServerURL(BaseSchema):
    url: str


class SearchServer(SearchServerURL):
    id: int
    name: str
    description: str


class SolutionStep(BaseSchema):
    step_description: str
    best_server_description: str = Field(
        ...,
        description="Description of the best server for this step, copy this from `mcp_servers` entry",
    )
    best_server_name: str = Field(
        ...,
        description="Name of the best server for this step, copy this from `mcp_servers` entry",
    )
    best_server: SearchServerURL = Field(
        ..., description="The best server for this step"
    )
    confidence: str = Field(
        ...,
        description="How confident you are that this server is enough for this step?",
    )
    additional_servers: list[SearchServerURL] = Field(
        ...,
        description="Alternative servers if you think the `best_server` may not be enough",
    )


class SearchResponse(BaseSchema):
    solution_steps: list[SolutionStep] = Field(
        ..., description="List of solution steps and servers for each step"
    )
