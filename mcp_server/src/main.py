from mcp.server.fastmcp import FastMCP
from openai.types.chat import ChatCompletionMessage
from openai.types.chat import ChatCompletionToolMessageParam

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
) -> list[ChatCompletionMessage | ChatCompletionToolMessageParam]:
    """Respond to any user request using MCP tools selected specifically for it."""
    return await tools.routing(request=request)


if __name__ == "__main__":
    mcp.run(transport="sse")
