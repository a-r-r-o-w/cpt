import asyncio
import aiohttp
import ratelimit
import typing
import json

from cfobject import (
  BlogEntry, Problem, ProblemStatistic, RatingChange,
  Submission, User,
  problem_parse, problemstatistic_parse, ratingchange_parse,
  submission_parse, user_parse, blogentry_parse
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
  
  async def problemset_problems (
    self, *,
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
          return await r.json()
    
    response = await codeforces_api_call(request)
    check_status(response)
    
    problems_list = problem_parse(response['result']['problems'])
    problemstatistics_list = problemstatistic_parse(response['result']['problemStatistics'])
    return problems_list, problemstatistics_list
  
  async def user_blogentries (
    self, *,
    handle: str
  ) -> BlogEntry:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_blogs')
      params = {
        'handle': handle
      }

      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          return await r.json()
      
    response = await codeforces_api_call(request)
    check_status(response)
    return blogentry_parse(response['result'])
  
  async def user_info (
    self, *,
    handles: typing.List[str]
  ) -> typing.List[User]:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_info')
      params = {
        'handles': ';'.join(handles)
      }
      
      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          return await r.json()
    
    response = await codeforces_api_call(request)
    check_status(response)
    return user_parse(response['result'])
  
  async def user_ratedlist (
    self, *,
    contest_id: int = None,
    active_only: bool = False
  ) -> typing.List[User]:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_ratedlist')
      params = {
        'activeOnly': 'true' if active_only else 'false',
        'contestId': contest_id
      }

      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          return await r.json()
    
    response = await codeforces_api_call(request)
    check_status(response)
    return user_parse(response['result'])

  async def user_rating (
    self, *,
    handle: str
  ) -> RatingChange:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_rating')
      params = {
        'handle': handle
      }

      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          return await r.json()
      
    response = await codeforces_api_call(request)
    check_status(response)
    return ratingchange_parse(response['result'])
  
  async def user_status (
    self, *,
    handle: str,
    start_index: int = 1,
    count: int = 1
  ) -> typing.List[Submission]:
    async def request () -> dict:
      route = CodeforcesAPIRoute('user_status')
      params = {
        'handle': handle,
        'from': start_index,
        'count': count
      }

      async with aiohttp.ClientSession() as session:
        async with session.get(route.get_url(), params = params) as r:
          return await r.json()
    
    response = await codeforces_api_call(request)
    check_status(response)
    return submission_parse(response['result'])

def main ():
  async def async_main ():
    API = CodeforcesAPI()

    problemset_problems = await API.problemset_problems(tags = ['meet-in-the-middle', 'matrices'])
    for problem, problemstatistic in zip(*problemset_problems):
      print(problem)
      print(problemstatistic)

    user_info_list = await API.user_info(handles = ['4rrow', 'SlavicG', 'Etherite'])
    for user in user_info_list:
      print(user)
    
    user_ratedlist = await API.user_ratedlist(contest_id = 1642, active_only = True)
    for user in user_ratedlist:
      if user.handle == '4rrow':
        print(user)
    
    user_status = await API.user_status(handle = '4rrow', start_index = 1, count = 1)
    for status in user_status:
      print(status)
    
    ratingchange = await API.user_rating(handle = '4rrow')
    print(ratingchange[0])
  
  asyncio.run(async_main())

if __name__ == '__main__':
  main()
