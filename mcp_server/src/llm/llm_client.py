from httpx import AsyncClient
from openai import APIError
from openai import AsyncOpenAI
from openai import InternalServerError
from openai import NOT_GIVEN
from openai import OpenAIError
from openai.types.chat import ChatCompletion
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionToolParam

from mcp_server.src.logger import logger
from mcp_server.src.settings import settings

default_http_client: AsyncClient = (
    AsyncClient()
    if settings.llm_proxy is None
    else AsyncClient(proxy=settings.llm_proxy)
)


class LLMClient:
    def __init__(
        self,
        http_client: AsyncClient = default_http_client,
    ) -> None:
        self.openai_client = AsyncOpenAI(http_client=http_client)

    @staticmethod
    def _get_full_messages(
        system_prompt: str | None, messages: list[ChatCompletionMessageParam]
    ) -> list[ChatCompletionMessageParam]:
        system_message: list[dict] = []
        if system_prompt:
            system_message = [
                {
                    "role": "system",
                    "content": system_prompt,
                    # Anthropic prompt caching
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        full_messages = system_message + messages
        return full_messages

    async def request(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
    ) -> ChatCompletion:
        full_messages = self._get_full_messages(
            system_prompt=system_prompt, messages=messages
        )
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=full_messages,
                max_tokens=max_tokens,
                tools=tools or NOT_GIVEN,
                timeout=30,
            )
        except APIError as error:
            logger.error(f"{error.code=} {error.body=}")
            raise
        except InternalServerError as error:
            logger.error(error.response.json())
            raise
        except OpenAIError as error:
            logger.error(
                f"Request to Provider failed with the following exception:\n{error}"
            )
            raise
        return response
