from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import ServerCreate
from .schemas import ServerUpdate
from .schemas import Tool
from src.database import get_session
from src.database import Server
from src.database import Tool as DBTool
from src.errors import ServerNotFoundError


class ServerRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_servers(
        self, id: int | None = None, name: str | None = None, url: str | None = None
    ) -> list[Server]:
        if id is None and name is None and url is None:
            raise ValueError("At least one of 'id', 'name', or 'url' must be provided.")

        query = select(Server).options(selectinload(Server.tools))
        query = query.filter(
            or_(
                (Server.id == id),
                (func.lower(Server.name) == func.lower(name)),
                (Server.url == url),
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_server(self, id: int) -> Server:
        query = select(Server).filter(Server.id == id)
        query = query.options(selectinload(Server.tools))
        result = await self.session.execute(query)
        server = result.scalars().first()
        if server is None:
            raise ServerNotFoundError(id)
        return server

    async def create_server(self, data: ServerCreate, tools: list[Tool]) -> Server:
        db_tools = self._convert_tools(tools, data.url)
        server = Server(**data.model_dump(exclude_none=True), tools=db_tools)
        self.session.add(server)
        await self.session.flush()
        return await self.get_server(server.id)

    async def get_all_servers(self) -> Select:
        return select(Server).options(selectinload(Server.tools))

    async def delete_server(self, id: int) -> None:
        query = delete(Server).where(Server.id == id)
        await self.session.execute(query)

    async def update_server(
        self, id: int, data: ServerUpdate, tools: list[Tool]
    ) -> Server:
        server = await self.get_server(id)
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(server, key, value)
        server.tools.clear()
        await self.session.flush()
        server.tools.extend(self._convert_tools(tools, server.url))
        await self.session.flush()
        await self.session.refresh(server)
        return server

    def _convert_tools(self, tools: list[Tool], url: str) -> list[DBTool]:
        return [
            DBTool(**tool.model_dump(exclude_none=True), server_url=url)
            for tool in tools
        ]

    @classmethod
    def get_new_instance(
        cls, session: AsyncSession = Depends(get_session)
    ) -> "ServerRepository":
        return cls(session)
