from mcp.server.fastmcp import FastMCP

from .schemas import RoutingResponse
from mcp_server.src.settings import settings
from mcp_server.src.tools import Tools


mcp: FastMCP = FastMCP(settings.server_json.name, port=settings.mcp_port)
tools: Tools = Tools()


@mcp.tool()
async def search_urls(request: str) -> list[str]:
    """Return URLs of the best MCP servers for processing the given request."""
    return await tools.search(request=request)


@mcp.tool()
async def routing(
    request: str,
) -> str:
    """Respond to any user request using MCP tools selected specifically for it."""
    response = await tools.routing(request=request)
    return RoutingResponse(conversation=response).model_dump_json()


if __name__ == "__main__":
    mcp.run(transport="sse")
