from typing import Self

from fastapi import Depends
from mcp import ClientSession
from mcp.client.sse import sse_client
from sqlalchemy import Select

from .repository import ServerRepository
from .schemas import ServerCreate
from .schemas import ServerRead
from .schemas import ServerUpdate
from .schemas import Tool
from registry.src.database import Server
from registry.src.errors import ServerAlreadyExistsError
from registry.src.errors import ServerNotFoundError
from registry.src.logger import logger


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
            dict_servers = [
                ServerRead.model_validate(server).model_dump() for server in servers
            ]
            raise ServerAlreadyExistsError(dict_servers)

    async def get_search_servers(self) -> list[Server]:
        servers_query = await self.repo.get_all_servers()
        servers = (await self.repo.session.execute(servers_query)).scalars().all()
        return list(servers)

    async def get_servers_by_urls(self, server_urls: list[str]) -> list[Server]:
        servers = await self.repo.get_servers_by_urls(urls=server_urls)
        if len(server_urls) != len(servers):
            retrieved_server_urls = {server.url for server in servers}
            missing_server_urls = set(server_urls) - retrieved_server_urls
            logger.warning(
                f"One or more server urls are incorrect {missing_server_urls=}"
            )
        return servers

    @classmethod
    def get_new_instance(
        cls, repo: ServerRepository = Depends(ServerRepository.get_new_instance)
    ) -> Self:
        return cls(repo=repo)
