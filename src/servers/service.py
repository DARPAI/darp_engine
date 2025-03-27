from fastapi import Depends
from mcp import ClientSession
from mcp.client.sse import sse_client

from .repository import ServerRepository
from .schemas import ServerCreate
from .schemas import Tool
from src.database import Server
from src.errors import ServerAlreadyExistsError


class ServerService:

    def __init__(self, repo: ServerRepository) -> None:
        self.repo = repo

    async def create(self, data: ServerCreate) -> Server:
        if servers := await self.repo.find_servers(name=data.name, url=data.url):
            raise ServerAlreadyExistsError(servers)

        tools = await self._get_tools(data.url)
        return await self.repo.create_server(data, tools)

    async def _get_tools(self, server_url: str) -> list[Tool]:
        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                return [
                    Tool(**tool.model_dump(exclude_none=True)) for tool in tools.tools
                ]

    @classmethod
    def get_new_instance(
        cls, repo: ServerRepository = Depends(ServerRepository.get_new_instance)
    ) -> "ServerService":
        return cls(repo=repo)
