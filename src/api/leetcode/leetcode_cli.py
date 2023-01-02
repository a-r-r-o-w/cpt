import os

from .leetcode import LeetcodeAPI
from .leetcode_object import (
  Problem, ProblemURL
)
from .leetcode_utils import (
  problem_url_parse,
  problem_to_markdown
)
from utils import cd

class LeetcodeCLI:
  """LeetCode Command Line Interface"""

  def __init__ (self) -> None:
    self.api = LeetcodeAPI()
  
  async def clone (self, url: str, *, path: str = '.') -> None:
    """Clone a LeetCode Problem
    :param str url: (required) problem url (example: https://leetcode.com/problems/two-sum/)
    :param str path: (optional) path (default is current working directory)
    :raises ValueError: invalid url
    """
    
    parsed_url: ProblemURL = problem_url_parse(url)
    problem: Problem = await self.api.get_problem_data(slug = parsed_url.slug)

    with cd(path):
      filename = f'{problem.frontend_id}-{problem.slug}.md'
      with open(filename, 'w') as file:
        file.write(problem_to_markdown(problem))
