from typing import Self

import instructor
from httpx import AsyncClient
from openai import AsyncOpenAI

from .prompts import get_top_servers
from .schemas import SearchResponse
from .schemas import SearchServer
from src.logger import logger
from src.settings import settings


class SearchService:
    def __init__(self) -> None:
        http_client: AsyncClient = (
            AsyncClient()
            if settings.llm_proxy is None
            else AsyncClient(proxy=settings.llm_proxy)
        )
        self.llm = instructor.from_openai(AsyncOpenAI(http_client=http_client))

    async def _get_search_response(
        self, servers: list[SearchServer], query: str
    ) -> SearchResponse:
        prompt = get_top_servers.format(servers_list=servers, request=query)
        completion = await self.llm.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_model=SearchResponse,
        )
        logger.debug(f"{completion=}")
        return completion

    @staticmethod
    def _collect_urls(search_response: SearchResponse) -> list[str]:
        server_urls = set()
        for solution_step in search_response.solution_steps:
            server_urls.add(solution_step.best_server.url)
            server_urls |= {server.url for server in solution_step.additional_servers}
        return list(server_urls)

    async def get_fitting_servers(
        self, servers: list[SearchServer], query: str
    ) -> list[str]:
        search_response = await self._get_search_response(servers=servers, query=query)
        return self._collect_urls(search_response=search_response)

    @classmethod
    async def get_new_instance(cls) -> Self:
        return cls()
