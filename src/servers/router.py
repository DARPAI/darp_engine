from fastapi import APIRouter
from fastapi import Depends

from .schemas import Server
from .schemas import ServerCreate
from .service import ServerService


router = APIRouter(prefix="/servers")


@router.post("/", response_model=Server)
async def create(
    data: ServerCreate, service: ServerService = Depends(ServerService.get_new_instance)
) -> Server:
    return await service.create(data)
