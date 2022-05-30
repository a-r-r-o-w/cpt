import asyncio
import aiohttp
import ratelimit

import lcgraphql

from lcobject import (
  Problem,
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

  async def question_data (
    self, *,
    title: str
  ) -> Problem:
    obj = lcgraphql.get_object('question_data', {'titleSlug': title})
    return problem_parse((await self.call(obj)).get('data').get('question'))

if __name__ == '__main__':
  async def main ():
    api = LeetcodeAPI()
    
    # problem = await api.question_data(title = 'divide-two-integers')
    problem = await api.question_data(title = 'minimum-obstacle-removal-to-reach-corner')
    print(problem.to_markdown())

    await api.session.close()
  
  asyncio.run(main())
