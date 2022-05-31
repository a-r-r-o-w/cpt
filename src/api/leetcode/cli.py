import os

from .leetcode import LeetcodeAPI
from .lcutils import (
  problem_url_parse,
  problem_to_markdown
)
from utils import cd

class LeetcodeCLI:
  """LeetCode CLI"""

  def __init__ (self):
    self._api = LeetcodeAPI()
  
  async def clone (self, url: str, *, path: str = '.') -> None:
    """Clone a LeetCode Problem
    :param str url: (required) problem url (example: https://leetcode.com/problems/two-sum/)
    :param str path: (optional) path (default is current working directory)
    :raises ValueError: invalid url
    """
    
    parsed_url = problem_url_parse(url)
    problem = await self._api.question_data(slug = parsed_url.slug)

    with cd(path):
      filename = f'{problem.frontend_id}-{problem.slug}.md'
      with open(filename, 'w') as file:
        file.write(problem_to_markdown(problem))
