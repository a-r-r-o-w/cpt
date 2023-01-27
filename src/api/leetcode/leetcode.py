import asyncio
import aiohttp
import aiolimiter
import typing

from .leetcode_graphql import get_object
from .leetcode_object import (
  Problem
)
from .leetcode_utils import (
  problem_parse
)


class LeetcodeAPI:
  """Leetcode API"""

  __base_url = 'https://leetcode.com/'
  __api_url = __base_url + 'graphql'

  async def call (self, data: typing.Dict[str, str]) -> typing.Dict[str, str]:
    if self.csrf is None:
      await self.get_csrf()
    async with self.limiter:
      async with self.session.post(self.__api_url, data = data, headers = self.headers) as r:
        return await r.json()

  async def get_csrf (self) -> None:
    async with self.limiter:
      async with self.session.get(self.__base_url) as r:
        self.csrf = r.cookies.get('csrftoken').value
        self.headers.update({
          'Referer': self.__base_url,
          'Content-Type': 'application/json',
          'X-CSRFToken': self.csrf
        })

  def __init__ (self) -> None:
    self.session = aiohttp.ClientSession()
    self.limiter = aiolimiter.AsyncLimiter(1, 2)
    self.headers = {}
    self.csrf = None
  
  def __del__ (self) -> None:
    loop = asyncio.get_event_loop()
    if loop.is_running():
      loop.create_task(self.session.close())
    else:
      loop.run_until_complete(self.session.close())

  async def get_problem_data (
    self, *,
    slug: str
  ) -> Problem:
    obj = get_object('question_data', {'titleSlug': slug})
    return problem_parse((await self.call(obj)).get('data').get('question'))
