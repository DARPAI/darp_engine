from fastapi import HTTPException
from fastapi import status

import src
from src.servers.schemas import Server


class FastApiError(HTTPException):

    def __init__(self, message: str, **kwargs) -> None:
        self.detail = {"message": message, **kwargs}


class ServerAlreadyExistsError(FastApiError):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, servers: list["src.database.models.server.Server"]) -> None:
        servers_str = ", ".join(server.name for server in servers)
        message = f"Server already exists: {servers_str}"
        dict_servers = [
            Server.model_validate(server).model_dump() for server in servers
        ]
        super().__init__(message=message, servers=dict_servers)


class ServerNotFoundError(FastApiError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, id: int) -> None:
        super().__init__(message=f"Server not found: {id}", id=id)
