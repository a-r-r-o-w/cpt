import typing

from .lcconstants import leetcode_urls

class LeetcodeObject:
  def __repr__ (self):
    return f'<{self.__class__.__name__}>'

class Problem (LeetcodeObject):
  def __init__ (
    self,
    id: int,
    frontend_id: int,
    title: str,
    slug: str,
    statement: str,
    difficulty: str,
    likes: int,
    dislikes: int,
    tags: typing.List[str],
    total_accepted: int,
    total_submissions: int,
    acceptance_rate: float,
    hints: typing.List[str],
    similar_problems: typing.List[dict]
  ):
    self.id = id
    self.frontend_id = frontend_id
    self.title = title
    self.slug = slug
    self.statement = statement
    self.difficulty = difficulty
    self.likes = likes
    self.dislikes = dislikes
    self.tags = tags
    self.total_accepted = total_accepted
    self.total_submissions = total_submissions
    self.acceptance_rate = acceptance_rate
    self.hints = hints
    self.similar_problems = similar_problems
  
  def __repr__ (self):
    return f'<{self.__class__.__name__} [{self.frontend_id} - {self.title}]>'

class ProblemURL (LeetcodeObject):
  def __init__ (self, slug: str):
    self.slug = slug
    self.url = leetcode_urls.get('problems') + self.slug
