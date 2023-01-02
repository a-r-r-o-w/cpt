import asyncio
import aiohttp
import ratelimit
import typing

from .cses_constants import cses_urls
from .cses_object import (
  Problem
)
from .cses_utils import (
  problem_parse
)


class CSESAPI:
  """CSES API"""

  @ratelimit.limits(calls = 1, period = 2)
  async def call (self, url: str) -> typing.Dict[str, str]:
    async with self.session.get(url, headers = self.headers) as r:
      return await r.text()

  def __init__ (self) -> None:
    self.session = aiohttp.ClientSession()
    self.headers = {}
  
  def __del__ (self) -> None:
    loop = asyncio.get_event_loop()
    if loop.is_running():
      loop.create_task(self.session.close())
    else:
      loop.run_until_complete(self.session.close())
  
  async def get_problem_data (
    self, *,
    id: int
  ) -> Problem:
    url = cses_urls['task'].format(id = id)
    return problem_parse(await self.call(url))
