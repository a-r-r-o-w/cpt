import aiohttp
import aiolimiter
import asyncio
from typing import Dict

from .aoc_constants import aoc_urls
from .aoc_object import Problem
from .aoc_utils import problem_parse


class AdventOfCodeAPI:
    """Advent of Code API"""

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()
        self.limiter = aiolimiter.AsyncLimiter(1, 2)
        self.headers = {}

    def __del__(self) -> None:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(self.session.close())
        else:
            loop.run_until_complete(self.session.close())

    async def call(self, url: str) -> Dict[str, str]:
        async with self.limiter:
            async with self.session.get(url, headers=self.headers) as r:
                return await r.text()

    async def get_problem_data(self, *, year: int, day: int) -> Problem:
        url = aoc_urls["problem"].format(year=year, day=day)
        return problem_parse(await self.call(url), year=year, day=day)
