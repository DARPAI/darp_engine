from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi_pagination import add_pagination
from fastapi_pagination import Page
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ServerCreate
from .schemas import ServerUpdate
from .schemas import ServerWithTools
from .service import ServerService
from registry.src.database import get_session
from registry.src.database import Server
from registry.src.search.schemas import SearchServer
from registry.src.search.service import SearchService


router = APIRouter(prefix="/servers")
add_pagination(router)


@router.post("/", response_model=ServerWithTools)
async def create(
    data: ServerCreate, service: ServerService = Depends(ServerService.get_new_instance)
) -> Server:
    return await service.create(data)


@router.get("/search", response_model=list[ServerWithTools])
async def search(
    query: str,
    service: ServerService = Depends(ServerService.get_new_instance),
    search_service: SearchService = Depends(SearchService.get_new_instance),
) -> list[Server]:
    servers = await service.get_search_servers()
    formatted_servers = [SearchServer.model_validate(server) for server in servers]
    server_urls = await search_service.get_fitting_servers(
        servers=formatted_servers, query=query
    )
    return await service.get_servers_by_urls(server_urls=server_urls)


@router.delete("/{id}")
async def delete_server(
    id: int, service: ServerService = Depends(ServerService.get_new_instance)
) -> None:
    return await service.delete_server(id=id)


@router.get("/", response_model=Page[ServerWithTools])
async def get_all_servers(
    params: Params = Depends(),
    service: ServerService = Depends(ServerService.get_new_instance),
    session: AsyncSession = Depends(get_session),
) -> Page[Server]:
    servers: Select = await service.get_all_servers()
    return await paginate(session, servers, params)


@router.get("/{id}", response_model=ServerWithTools)
async def get_server_by_id(
    id: int,
    service: ServerService = Depends(ServerService.get_new_instance),
) -> Server:
    return await service.get_server_by_id(id=id)


@router.get("", response_model=list[ServerWithTools])
async def get_servers_by_ids(
    ids: list[int] = Query(...),
    service: ServerService = Depends(ServerService.get_new_instance),
) -> list[Server]:
    return await service.get_servers_by_ids(ids=ids)


@router.put("/{id}", response_model=ServerWithTools)
async def update_server(
    id: int,
    data: ServerUpdate,
    service: ServerService = Depends(ServerService.get_new_instance),
) -> Server:
    return await service.update_server(id=id, data=data)
