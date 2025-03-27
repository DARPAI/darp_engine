from fastapi import Depends
from mcp import ClientSession
from mcp.client.sse import sse_client
from sqlalchemy import Select

from .repository import ServerRepository
from .schemas import ServerCreate
from .schemas import ServerUpdate
from .schemas import Tool
from src.database import Server
from src.errors import ServerAlreadyExistsError
from src.errors import ServerNotFoundError


class ServerService:

    def __init__(self, repo: ServerRepository) -> None:
        self.repo = repo

    async def create(self, data: ServerCreate) -> Server:
        await self._assure_server_not_exists(name=data.name, url=data.url)
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

    async def delete_server(self, id: int) -> None:
        await self._assure_server_found(id)
        await self.repo.delete_server(id=id)

    async def get_all_servers(self) -> Select:
        return await self.repo.get_all_servers()

    async def get_server_by_id(self, id: int) -> Server:
        await self._assure_server_found(id)
        return await self.repo.get_server(id=id)

    async def get_servers_by_ids(self, ids: list[int]) -> list[Server]:
        servers = []
        for id in ids:
            await self._assure_server_found(id)
            servers.append(await self.repo.get_server(id=id))
        return servers

    async def update_server(self, id: int, data: ServerUpdate) -> Server:
        await self._assure_server_found(id)
        await self._assure_server_not_exists(name=data.name, url=data.url)
        if data.url:
            tools = await self._get_tools(data.url)
        else:
            server = await self.repo.get_server(id=id)
            tools = await self._get_tools(server.url)
        return await self.repo.update_server(id, data, tools)

    async def _assure_server_found(self, id: int) -> None:
        if not await self.repo.find_servers(id=id):
            raise ServerNotFoundError(id)

    async def _assure_server_not_exists(self, **kwargs) -> None:
        if servers := await self.repo.find_servers(**kwargs):
            raise ServerAlreadyExistsError(servers)

    @classmethod
    def get_new_instance(
        cls, repo: ServerRepository = Depends(ServerRepository.get_new_instance)
    ) -> "ServerService":
        return cls(repo=repo)
