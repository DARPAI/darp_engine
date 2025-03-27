from fastapi import Depends
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import ServerCreate
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
        db_tools = [
            DBTool(**tool.model_dump(exclude_none=True), server_url=data.url)
            for tool in tools
        ]
        server = Server(**data.model_dump(exclude_none=True), tools=db_tools)
        self.session.add(server)
        await self.session.flush()
        return await self.get_server(server.id)

    @classmethod
    def get_new_instance(
        cls, session: AsyncSession = Depends(get_session)
    ) -> "ServerRepository":
        return cls(session)
