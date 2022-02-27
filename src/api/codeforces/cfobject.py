from operator import index
import typing
from datetime import datetime

class CodeforcesObject:
  @staticmethod
  def to_str (attribute):
    return '' if attribute is None else str(attribute)

  def __repr__ (self):
    return f'<{self.__class__.__name__}>'

class Problem (CodeforcesObject):
  def __init__ (
    self,
    contest_id: int = None,
    problemset_name: str = None,
    index: str = None,
    name: str = None,
    type: str = None,
    points: float = None,
    rating: int = None,
    tags: typing.List[str] = None
  ):
    self.contest_id = contest_id
    self.problemset_name = problemset_name
    self.index = index
    self.name = name
    self.type = type
    self.points = points
    self.rating = rating
    self.tags = tags
  
  def __str__ (self) -> str:
    problem = f"""\
  Name: {self.to_str(self.contest_id)}{self.to_str(self.index)} {self.to_str(self.name)}
Rating: {self.to_str(self.rating)}
Points: {self.to_str(self.points)}
  Type: {self.to_str(self.type)}
  Tags: [{', '.join(self.to_str(tag) for tag in self.tags)}]
Problemset Name: {self.to_str(self.problemset_name)}
"""
    return problem

class ProblemStatistic (CodeforcesObject):
  def __init__ (
    self,
    contest_id: int = None,
    index: str = None,
    solved_count: int = None
  ):
    self.contest_id = contest_id
    self.index = index
    self.solved_count = solved_count
  
  def __str__ (self) -> str:
    problemstatistics = f"""\
    Problem: {self.to_str(self.contest_id)}{self.to_str(self.index)}
Solve Count: {self.to_str(self.solved_count)}
"""
    return problemstatistics

class User (CodeforcesObject):
  def __init__ (
    self,
    handle: str = None,
    email: str = None,
    vk_id: str = None,
    open_id: str = None,
    first_name: str = None,
    last_name: str = None,
    country: str = None,
    city: str = None,
    organization: str = None,
    contribution: int = None,
    rank: str = None,
    rating: int = None,
    max_rank: str = None,
    max_rating: int = None,
    last_online_time_seconds: int = None,
    registration_time_seconds: int = None,
    friend_of_count: int = None,
    avatar: str = None,
    title_photo: str = None
  ):
    self.handle = handle
    self.email = email
    self.vk_id = vk_id
    self.open_id = open_id
    self.first_name = first_name
    self.last_name = last_name
    self.country = country
    self.city = city
    self.organization = organization
    self.contribution = contribution
    self.rank = rank
    self.rating = rating
    self.max_rank = max_rank
    self.max_rating = max_rating
    self.last_online_time_seconds = last_online_time_seconds
    self.registration_time_seconds = registration_time_seconds
    self.friend_of_count = friend_of_count
    self.avatar = avatar
    self.title_photo = title_photo
  
  def __str__ (self) -> str:
    user = f"""\
  Name: {self.to_str(self.first_name)} {self.to_str(self.last_name)}
Handle: {self.to_str(self.handle)}
Rating: {self.to_str(self.rating)} (max: {self.to_str(self.max_rating)})
  Rank: {self.to_str(self.rank)} (max: {self.to_str(self.max_rank)})
    
       Email: {self.to_str(self.email)}
        City: {self.to_str(self.city)}
     Country: {self.to_str(self.country)}
Organization: {self.to_str(self.organization)}

Contribution: {self.to_str(self.contribution)}
Friend of {self.friend_of_count} users

Last online: {self.to_str(datetime.fromtimestamp(self.last_online_time_seconds))}
 Registered: {self.to_str(datetime.fromtimestamp(self.registration_time_seconds))}

     Avatar: {self.to_str(self.avatar)}
Title Photo: {self.to_str(self.title_photo)}
"""
    return user

def problem_parse (problems: typing.List[dict] = None) -> typing.List[Problem]:
  problem_list = []

  for problem in problems:
    try:
      contest_id = int(problem.get('contestId'))
    except TypeError:
      contest_id = 'NA'

    try:
      points = float(problem.get('points', 0))
    except TypeError:
      points = 'NA'
    
    try:
      rating = int(problem.get('rating', 0))
    except TypeError:
      rating = 'NA'
    
    problemset_name = problem.get('problemsetName')
    index = problem.get('index')
    name = problem.get('name')
    type = problem.get('type')
    tags = problem.get('tags')

    problem_list.append(Problem(
      contest_id, problemset_name, index, name,
      type, points, rating, tags
    ))
  
  return problem_list

def problemstatistic_parse (problemstatistics: typing.List[dict] = None) -> typing.List[ProblemStatistic]:
  problemstatistic_list = []

  for problemstatistic in problemstatistics:
    try:
      contest_id = int(problemstatistic.get('contestId'))
    except TypeError:
      contest_id = 'NA'
    
    index = problemstatistic.get('index')
    solved_count = problemstatistic.get('solvedCount')

    problemstatistic_list.append(ProblemStatistic(
      contest_id, index, solved_count
    ))
  
  return problemstatistic_list

def user_parse (users: typing.List[dict] = None) -> typing.List[User]:
  user_list = []

  for user in users:
    try:
      contribution = int(user.get('contribution'))
    except TypeError:
      contribution = 'NA'
    
    try:
      rating = int(user.get('rating'))
      max_rating = int(user.get('maxRating'))
    except TypeError:
      rating = 'NA'
      max_rating = 'NA'
    
    handle = user.get('handle')
    email = user.get('email')
    vk_id = user.get('vkId')
    open_id = user.get('openId')
    first_name = user.get('firstName')
    last_name = user.get('lastName')
    country = user.get('country')
    city = user.get('city')
    organization = user.get('organization')
    rank = user.get('rank')
    max_rank = user.get('maxRank')
    last_online_time_seconds = int(user.get('lastOnlineTimeSeconds'))
    registration_time_seconds = int(user.get('registrationTimeSeconds'))
    friend_of_count = int(user.get('friendOfCount'))
    avatar = user.get('avatar')
    title_photo = user.get('titlePhoto')

    user_list.append(User(
      handle, email, vk_id, open_id, first_name, last_name,
      country, city, organization, contribution, rank, rating,
      max_rank, max_rating, last_online_time_seconds,
      registration_time_seconds, friend_of_count, avatar, title_photo
    ))

  return user_list
