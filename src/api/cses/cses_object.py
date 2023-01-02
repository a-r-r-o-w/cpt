import typing

from .cses_constants import cses_urls

class CSESObject:
  """Represents a CSES Object"""

  def __repr__ (self):
    return f'<{self.__class__.__name__}>'


class Problem (CSESObject):
  """Represents a CSES Problem Object"""
  
  def __init__ (
    self,
    id: int,
    name: str,
    statement: str,
    time_limit: int,
    memory_limit: int,
    total_accepted: int,
    total_submissions: int,
    success_rate: float
  ) -> None:
    self.id = id
    self.name = name
    self.statement = statement
    self.time_limit = time_limit
    self.memory_limit = memory_limit
    self.total_accepted = total_accepted
    self.total_submissions = total_submissions
    self.success_rate = success_rate
  
  def __repr__ (self) -> str:
    return f'<{self.__class__.__name__}> [{self.id} - {self.name}]'
