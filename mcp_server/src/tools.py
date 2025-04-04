from mcp_server.src.decorators import log_errors
from mcp_server.src.registry_client import RegistryClient


class Tools:
    def __init__(self):
        self.registry_client = RegistryClient()

    @log_errors
    async def search(self, request: str) -> list[str]:
        servers = await self.registry_client.search(request=request)
        return [server.url for server in servers]
