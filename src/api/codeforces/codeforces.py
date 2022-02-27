import asyncio
import aiohttp
import ratelimit
import typing
import json

from cfobject import (
  Problem, ProblemStatistic,
  User,
  problem_parse, problemstatistic_parse,
  user_parse
)

from cfexception import (
  StatusNotFoundError,
  StatusFailedError,
  CommentNotFoundError,
  ResultNotFoundError
)

@ratelimit.limits(calls = 1, period = 2)
async def _API_call (callback, *args, **kwargs):
  return await callback(*args, **kwargs)

async def codeforces_api_call (callback, *args, **kwargs):
  sleep_duration = 1
  
  while True:
    try:
      return_value = await _API_call(callback, *args, **kwargs)
    except ratelimit.RateLimitException:
      await asyncio.sleep(sleep_duration)
    else:
      break

  return return_value

def check_status (response: dict):
  if 'status' not in response.keys():
    raise StatusNotFoundError('Codeforces API call response does not contain a status message')
  elif response.get('status') == 'OK':
    if 'result' not in response.keys():
      raise ResultNotFoundError('Codeforces API call response does not contain result')
  else:
    if 'comment' not in response.keys():
      raise CommentNotFoundError('Reason for Codeforces API call {"status": "FAILED"} not found')
    else:
      raise StatusFailedError(response.get('comment'))

class CodeforcesAPIRoute:
  base_url = 'https://codeforces.com/api/'

  _API_Routes = {
    'blog_comments': 'blogEntry.comments',
    'blog': 'blogEntry.view',
    'contest_hacks': 'contest.hacks',
    'contest_list': 'contest.list',
    'contest_rating_changes': 'contest.ratingChanges',
    'contest_standings': 'contest.standings',
    'contest_status': 'contest.status',
    'problemset_problems': 'problemset.problems',
    'problemset_status': 'problemset.recentStatus',
    'recent_actions': 'recentActions',
    'user_blogs': 'user.blogEntries',
    'user_friends': 'user.friends',
    'user_info': 'user.info',
    'user_ratedlist': 'user.ratedList',
    'user_rating': 'user.rating',
    'user_status': 'user.status',
  }

  def __init__ (self, route: str):
    if route not in self._API_Routes:
      error_msg = f"API route '{route}' is invalid! Choose from:\n" + '\n'.join(
        f'({index:02}) {route}'
        for index, route in enumerate(self._API_Routes.keys(), start = 1)
      )
      raise ValueError(error_msg)
    
    self.route = route
  
  def get_url (self) -> str:
    return self.base_url + self._API_Routes[self.route]

class CodeforcesAPI:
  def __init__ (self):
    pass
  
  async def user_info (
    self,
    handles: typing.List[str]
  ) -> typing.List[User]:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_info')
      params = {
        'handles': ';'.join(handles)
      }
      
      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          response = await r.json()
      
      return response
    
    response = await codeforces_api_call(request)
    check_status(response)
    
    user_list = user_parse(response['result'])
    return user_list
  
  async def problemset_problems (
    self,
    tags: typing.List[str] = None,
    problemset_name: str = None
  ) -> typing.Tuple[typing.List[Problem], typing.List[ProblemStatistic]]:
    async def request () -> dict:
      route = CodeforcesAPIRoute('problemset_problems')
      params = {}

      if tags is not None:
        params['tags'] = ';'.join(tags)
      if problemset_name is not None:
        params['problemsetName'] = problemset_name

      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          response = await r.json()
      
      return response
    
    response = await codeforces_api_call(request)
    check_status(response)
    
    problems_list = problem_parse(response['result']['problems'])
    problemstatistics_list = problemstatistic_parse(response['result']['problemStatistics'])
    return problems_list, problemstatistics_list

if __name__ == '__main__':
  api = CodeforcesAPI()
  
  async def main ():
    user = await api.user_info(handles = ['4rrow', 'SlavicG', 'Etherite'])
    problem = await api.problemset_problems(['meet-in-the-middle', 'matrices'])

    for i in user:
      print(i)
    
    print(problem[0][0])
    print(problem[1][0])

    # tasks = []
    # task = asyncio.ensure_future(api.problemset_problems(['meet-in-the-middle', 'dp']))
    # tasks.append(task)
    # for i in range(3):
    #   task = asyncio.ensure_future(api.user_info(handles = ['4rrow', 'SlavicG']))
    #   tasks.append(task)
    # r = await asyncio.gather(*tasks)
    # return r
  
  asyncio.run(main())
