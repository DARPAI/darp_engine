from httpx import AsyncClient

from mcp_server.src.schemas import RegistryServer
from mcp_server.src.settings import settings


class RegistryClient:
    def __init__(self):
        self.client = AsyncClient(base_url=settings.registry_url)
        self.timeout = 90

    async def search(self, request: str) -> list[RegistryServer]:
        response = await self.client.get(
            "/servers/search", params=dict(query=request), timeout=self.timeout
        )
        assert (
            response.status_code == 200
        ), f"{response.status_code=} {response.content=}"
        data = response.json()
        return [RegistryServer.model_validate(server) for server in data]
