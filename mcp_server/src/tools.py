from openai.types.chat import ChatCompletionMessage
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionToolMessageParam
from openai.types.chat import ChatCompletionUserMessageParam

from mcp_server.src.decorators import log_errors
from mcp_server.src.llm.llm_client import LLMClient
from mcp_server.src.llm.prompts import default_prompt
from mcp_server.src.llm.tool_manager import ToolManager
from mcp_server.src.registry_client import RegistryClient
from mcp_server.src.settings import settings


class Tools:
    def __init__(self):
        self.registry_client = RegistryClient()
        self.llm_client = LLMClient()

    @log_errors
    async def search(self, request: str) -> list[str]:
        servers = await self.registry_client.search(request=request)
        return [server.url for server in servers]

    @log_errors
    async def routing(
        self, request: str
    ) -> list[ChatCompletionMessage | ChatCompletionToolMessageParam]:
        servers = await self.registry_client.search(request=request)
        manager = ToolManager(servers)
        user_message = ChatCompletionUserMessageParam(content=request, role="user")
        resulting_conversation = await self._llm_request(
            messages=[user_message], manager=manager
        )
        return resulting_conversation

    async def _llm_request(
        self,
        messages: list[ChatCompletionMessageParam],
        manager: ToolManager,
        response_accumulator: (
            list[ChatCompletionMessage | ChatCompletionToolMessageParam] | None
        ) = None,
    ) -> list[ChatCompletionMessage | ChatCompletionToolMessageParam]:
        if response_accumulator is None:
            response_accumulator = []
        completion = await self.llm_client.request(
            system_prompt=default_prompt,
            model=settings.llm_model,
            messages=messages,
            tools=manager.tools,
        )
        choice = completion.choices[0]
        response_accumulator.append(choice.message)
        if choice.message.tool_calls:
            tool_calls = choice.message.tool_calls
            tool_result_messages = [
                await manager.handle_tool_call(tool_call) for tool_call in tool_calls
            ]
            response_accumulator += tool_result_messages
            conversation = messages + [choice.message] + tool_result_messages
            response_accumulator = await self._llm_request(
                messages=conversation,
                manager=manager,
                response_accumulator=response_accumulator,
            )
        return response_accumulator
