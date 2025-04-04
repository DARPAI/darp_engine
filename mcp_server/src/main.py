from mcp.server.fastmcp import FastMCP

from mcp_server.src.settings import settings
from mcp_server.src.tools import Tools


mcp: FastMCP = FastMCP(settings.server_json.name, port=settings.mcp_port)
tools: Tools = Tools()


@mcp.tool()
async def search_urls(request: str) -> list[str]:
    """Return URLs of the best MCP servers for processing the given request."""
    return await tools.search(request=request)


if __name__ == "__main__":
    mcp.run(transport="sse")
