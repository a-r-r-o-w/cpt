import asyncio
import aiohttp
import ratelimit

from .lcgraphql import get_object
from .lcobject import (
  Problem
)
from .lcutils import (
  problem_parse
)

class LeetcodeAPI:
  __base_url = 'https://leetcode.com/'
  __api_url = __base_url + 'graphql'

  @ratelimit.limits(calls = 1, period = 2)
  async def call (self, data):
    if self.csrf is None:
      await self.get_csrf()
    async with self.session.post(self.__api_url, data = data, headers = self.headers) as r:
      return await r.json()

  async def get_csrf (self):
    async with self.session.get(self.__base_url) as r:
      self.csrf = r.cookies.get('csrftoken').value
      self.headers.update({
        'Referer': self.__base_url,
        'Content-Type': 'application/json',
        'X-CSRFToken': self.csrf
      })

  def __init__ (self):
    self.session = aiohttp.ClientSession()
    self.headers = {}
    self.csrf = None
  
  def __del__ (self):
    loop = asyncio.get_event_loop()
    if loop.is_running():
      loop.create_task(self.session.close())
    else:
      loop.run_until_complete(self.session.close())

  async def question_data (
    self, *,
    slug: str
  ) -> Problem:
    obj = get_object('question_data', {'titleSlug': slug})
    return problem_parse((await self.call(obj)).get('data').get('question'))
