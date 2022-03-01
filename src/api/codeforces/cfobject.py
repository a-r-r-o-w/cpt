import typing
from datetime import datetime

def _try_typecast (value: typing.Any, to_type: typing.Type, default: typing.Any = None) -> typing.Any:
  try:
    typecasted_value = to_type(value)
  except TypeError:
    typecasted_value = default
  return typecasted_value

class CodeforcesObject:
  @staticmethod
  def to_str (attribute):
    return 'None' if attribute is None else str(attribute)

  def __repr__ (self):
    return f'<{self.__class__.__name__}>'

class Member (CodeforcesObject):
  def __init__ (
    self,
    handle: str,
    name: str
  ):
    self.handle = handle
    self.name = name
  
  def __str__ (self):
    member = f"""\
Handle: {self.to_str(self.handle)}
  Name: {self.to_str(self.name)}
"""
    return member

class Party (CodeforcesObject):
  def __init__ (
    self,
    contest_id: int,
    members: typing.List[Member],
    participant_type: str,
    team_id: int,
    team_name: str,
    ghost: bool,
    room: int,
    start_time_seconds: int
  ):
    self.contest_id = contest_id
    self.members = members
    self.participant_type = participant_type
    self.team_id = team_id
    self.team_name = team_name
    self.ghost = ghost
    self.room = room
    self.start_time_seconds = start_time_seconds
  
  def __str__ (self):
    party = f"""\
Contest ID: {self.to_str(self.contest_id)}
   Members: [{', '.join(self.to_str(member) for member in self.members)}]

  Team ID: {self.to_str(self.team_id)}
Team Name: {self.to_str(self.team_name)}
    Ghost: {self.to_str(self.ghost)}
     Room: {self.to_str(self.room)}

Participant Type: {self.to_str(self.participant_type)}
      Start Time: {self.to_str(datetime.fromtimestamp(self.start_time_seconds))}
"""
    return party

class Problem (CodeforcesObject):
  def __init__ (
    self,
    contest_id: int,
    problemset_name: str,
    index: str,
    name: str,
    type: str,
    points: float,
    rating: int,
    tags: typing.List[str]
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
    contest_id: int,
    index: str,
    solved_count: int
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

class ProblemResult (CodeforcesObject):
  def __init__ (
    self,
    points: float,
    penalty: int,
    rejected_attempt_count: int,
    type: str,
    best_submission_time_seconds: int
  ):
    self.points = points
    self.penalty = penalty
    self.rejected_attempt_count = rejected_attempt_count
    self.type = type
    self.best_submission_time_seconds = best_submission_time_seconds
  
  def __str__ (self) -> str:
    problemresult = f"""\
   Type: {self.to_str(self.type)}
 Points: {self.to_str(self.points)}
Penalty: {self.to_str(self.penalty)}
Rejected Attempts: {self.to_str(self.rejected_attempt_count)}
Best Submission Time: {self.to_str(datetime.fromtimestamp(self.best_submission_time_seconds))}
"""
    return problemresult

class Submission (CodeforcesObject):
  def __init__ (
    self,
    id: int,
    contest_id: int,
    creation_time_seconds: int,
    relative_time_seconds: int,
    problem: Problem,
    author: Party,
    programming_language: str,
    verdict: str,
    testset: str,
    passed_test_count: int,
    time_consumed_millis: int,
    memory_consumed_bytes: int,
    points: float
  ):
    self.id = id
    self.contest_id = contest_id
    self.creation_time_seconds = creation_time_seconds
    self.relative_time_seconds = relative_time_seconds
    self.problem = problem
    self.author = author
    self.programming_language = programming_language
    self.verdict = verdict
    self.testset = testset
    self.passed_test_count = passed_test_count
    self.time_consumed_millis = time_consumed_millis
    self.memory_consumed_bytes = memory_consumed_bytes
    self.points = points
  
  def __str__ (self):
    submission = f"""\
        ID: {self.to_str(self.id)}
Contest ID: {self.to_str(self.contest_id)}

{self.to_str(self.problem)}

Language: {self.to_str(self.programming_language)}
 Verdict: {self.to_str(self.verdict)}
 Testset: {self.to_str(self.testset)}
  Passed: {self.to_str(self.passed_test_count)}

Author:
{self.to_str(self.author)}

Creation Time: {self.to_str(datetime.fromtimestamp(self.creation_time_seconds))}
Relative Time: {self.to_str(datetime.fromtimestamp(self.relative_time_seconds))}
"""
    return submission

class User (CodeforcesObject):
  def __init__ (
    self,
    handle: str,
    email: str,
    vk_id: str,
    open_id: str,
    first_name: str,
    last_name: str,
    country: str,
    city: str,
    organization: str,
    contribution: int,
    rank: str,
    rating: int,
    max_rank: str,
    max_rating: int,
    last_online_time_seconds: int,
    registration_time_seconds: int,
    friend_of_count: int,
    avatar: str,
    title_photo: str
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

def member_parse (members: typing.List[dict]) -> typing.List[Member]:
  member_list = []

  for member in members:
    handle = member.get('handle')
    name = member.get('name')

    member_list.append(Member(handle, name))
  
  return member_list

def party_parse (parties: typing.List[dict]) -> typing.List[Party]:
  party_list = []

  for party in parties:
    contest_id = _try_typecast(party.get('contestId', int, 'NA'))
    room = _try_typecast(party.get('room'), int, 'NA')
    start_time_seconds = _try_typecast(party.get('startTimeSeconds'), int, 'NA')
    team_id = _try_typecast(party.get('teamId'), int, 'NA')
    members = member_parse([party.get('members')])[0]
    participant_type = party.get('participantType')
    team_name = party.get('teamName')
    ghost = party.get('ghost')

    party_list.append(Party(
      contest_id, members, participant_type, team_id,
      team_name, ghost, room, start_time_seconds
    ))
  
  return party_list

def problem_parse (problems: typing.List[dict]) -> typing.List[Problem]:
  problem_list = []

  for problem in problems:
    contest_id = _try_typecast(problem.get('contestId'), int, 'NA')
    points = _try_typecast(problem.get('points'), float, 0.0)
    rating = _try_typecast(problem.get('rating'), int, 0)
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

def problemstatistic_parse (problemstatistics: typing.List[dict]) -> typing.List[ProblemStatistic]:
  problemstatistic_list = []

  for problemstatistic in problemstatistics:
    contest_id = _try_typecast(problemstatistic.get('contestId'), int, 'NA')
    index = problemstatistic.get('index')
    solved_count = problemstatistic.get('solvedCount')

    problemstatistic_list.append(ProblemStatistic(
      contest_id, index, solved_count
    ))
  
  return problemstatistic_list

def problemresult_parse (problemresults: typing.List[dict]) -> typing.List[ProblemResult]:
  problemresult_list = []

  for problemresult in problemresults:
    penalty = _try_typecast(problemresult.get('penalty'), int, 'NA')
    best_submission_time_seconds = \
      _try_typecast(problemresult.get('bestSubmissionTimeSeconds'), int, 'NA')
    points = float(problemresult.get('points'))
    rejected_attempt_count = int(problemresult.get('rejectedAttemptCount'))
    type = problemresult.get('type')

    problemresult_list.append(ProblemResult(
      points, penalty, rejected_attempt_count,
      type, best_submission_time_seconds
    ))
  
  return problemresult_list

def submission_parse (submissions: typing.List[dict]) -> typing.List[Submission]:
  submission_list = []

  for submission in submissions:
    problem = None
    party = None
    
    if submission.get('problem') is not None:
      problem = problem_parse([submission.get('problem')])[0]
    
    if submission.get('party') is not None:
      party = party_parse([submission.get('party')])[0]
    
    contest_id = _try_typecast(submission.get('contestId'), int, 'NA')
    points = _try_typecast(submission.get('points'), float, 0.0)
    id = int(submission.get('id'))
    creation_time_seconds = int(submission.get('creationTimeSeconds'))
    relative_time_seconds = int(submission.get('relativeTimeSeconds'))
    programming_language = submission.get('programmingLanguage')
    verdict = submission.get('verdict')
    testset = submission.get('testset')
    passed_test_count = int(submission.get('passedTestCount'))
    time_consumed_millis = int(submission.get('timeConsumedMillis'))
    memory_consumed_bytes = int(submission.get('memoryConsumedBytes'))

    submission_list.append(Submission(
      id, contest_id, creation_time_seconds, relative_time_seconds, problem,
      party, programming_language, verdict, testset, passed_test_count,
      time_consumed_millis, memory_consumed_bytes, points
    ))
  
  return submission_list

def user_parse (users: typing.List[dict]) -> typing.List[User]:
  user_list = []

  for user in users:
    contribution = _try_typecast(user.get('contribution'), int, 'NA')
    rating = _try_typecast(user.get('rating'), int, 'NA')
    max_rating = _try_typecast(user.get('maxRating'), int, 'NA')
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
