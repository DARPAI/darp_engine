import argparse
import asyncio
from typing import Any
from typing import List
from typing import Literal
from typing import Union

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CallToolResult
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)
from pydantic import BaseModel

default_mcp_url: str = "http://localhost:4689/sse"
tool_name: str = "routing"


async def main() -> None:
    parser = argparse.ArgumentParser(description="DARP Router")
    parser.add_argument("request", type=str, help="Routing request")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    response = await request_mcp(
        server_url=default_mcp_url,
        tool_name=tool_name,
        arguments={"request": args.request},
    )
    display_response(response.content[0].text, format=args.format, verbose=args.verbose)


async def request_mcp(
    server_url: str = default_mcp_url,
    tool_name: str = tool_name,
    arguments: dict[str, Any] | None = None,
) -> CallToolResult:
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            return await session.call_tool(
                tool_name,
                arguments=arguments or {},
            )


def display_response(response: str, format: str = "text", verbose: bool = False):
    if format == "json":
        print(response)
    else:
        routing_response = RoutingResponse.model_validate_json(response)
        for message in routing_response.conversation:
            print(message.__str__(verbose))


class PrintableChatCompletionMessage(ChatCompletionMessage):
    def __str__(self, verbose: bool = False) -> str:
        contents = "\n".join(
            filter(
                None,
                [
                    self._format_content("refusal", verbose),
                    self._format_content("function_call", verbose),
                    self._format_content("tool_calls", verbose),
                    self._format_content("content", verbose=True),
                ],
            )
        )
        return f"{self.role}: {contents}"

    def _format_content(self, key: str, verbose: bool = False) -> str | None:
        value = getattr(self, f"_{key}_content")()
        if value is None:
            return None
        if not verbose:
            return f"[{key}]"
        else:
            return f"{value}"

    def _refusal_content(self) -> str | None:
        if self.refusal is not None:
            return "\n" + indent(self.refusal)
        return None

    def _function_call_content(self) -> str | None:
        if self.function_call is not None:
            return f"{self.function_call.name}({self.function_call.arguments})"
        return None

    def _tool_calls_content(self) -> str | None:
        if self.tool_calls is not None:
            return "\n" + indent(
                "\n".join(
                    f"{call.function.name}({call.function.arguments})"
                    for call in self.tool_calls
                )
            )
        return None

    def _content_content(self) -> str | None:
        if self.content is not None:
            return "\n" + indent(self.content)
        return None


class PrintableChatCompletionToolMessageParam(BaseModel):
    role: Literal["tool"]
    content: Union[str, List[ChatCompletionContentPartTextParam]]
    tool_call_id: str

    def __str__(self, verbose: bool = False) -> str:
        if not verbose:
            return f"[{self.role}] ..."
        if isinstance(self.content, str):
            return f"{self.role}: {self.content}"
        elif isinstance(self.content, list):
            contents = "\n".join(
                "{type}: {text}".format(**item) for item in self.content
            )
            return indent(f"{self.role}:\n{indent(contents)}")
        else:
            raise ValueError(f"Invalid content type: {type(self.content)}")


class RoutingResponse(BaseModel):
    conversation: list[
        PrintableChatCompletionMessage | PrintableChatCompletionToolMessageParam
    ]


def indent(text: str, indent: int = 1, prefix: str = "  "):
    return "\n".join(prefix * indent + line for line in text.split("\n"))


if __name__ == "__main__":
    asyncio.run(main())
