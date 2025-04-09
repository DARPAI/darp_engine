import json

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CallToolResult
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat import ChatCompletionToolMessageParam
from openai.types.chat import ChatCompletionToolParam

from mcp_server.src.schemas import RegistryServer
from mcp_server.src.schemas import ToolInfo


class ToolManager:
    def __init__(self, servers: list[RegistryServer]) -> None:
        self.renamed_tools: dict[str, ToolInfo] = {}
        self.tools: list[ChatCompletionToolParam] = self.set_tools(servers)

    def rename_and_save(self, tool_name: str, server: RegistryServer) -> str:
        renamed_tool = f"{tool_name}_mcp_{server.name}"
        self.renamed_tools[renamed_tool] = ToolInfo(tool_name=tool_name, server=server)
        return renamed_tool

    def set_tools(self, servers: list[RegistryServer]) -> list[ChatCompletionToolParam]:
        return [
            ChatCompletionToolParam(
                type="function",
                function={
                    "name": self.rename_and_save(tool.name, server=server),
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            )
            for server in servers
            for tool in server.tools
        ]

    @staticmethod
    async def _request_mcp(
        arguments: str,
        server_url: str,
        tool_name: str,
    ) -> CallToolResult:
        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                return await session.call_tool(
                    tool_name,
                    arguments=(json.loads(arguments) if arguments else None),
                )

    async def handle_tool_call(
        self, tool_call: ChatCompletionMessageToolCall
    ) -> ChatCompletionToolMessageParam:
        tool_info = self.renamed_tools.get(tool_call.function.name)
        if not tool_info:
            return ChatCompletionToolMessageParam(
                role="tool",
                content="Error: Incorrect tool name",
                tool_call_id=tool_call.id,
            )
        tool_call_result = await self._request_mcp(
            arguments=tool_call.function.arguments,
            server_url=tool_info.server.url,
            tool_name=tool_info.tool_name,
        )
        return ChatCompletionToolMessageParam(
            role="tool",
            content=tool_call_result.content[0].text,
            tool_call_id=tool_call.id,
        )
