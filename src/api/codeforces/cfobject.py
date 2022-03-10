import typing
import json

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
  
  def __str__ (self) -> str:
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
  
  def __str__ (self) -> str:
    newline = '\n'
    party = f"""\
Contest ID: {self.to_str(self.contest_id)}

Members:
{newline.join(self.to_str(member) for member in self.members)}

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
  Tags: {self.to_str(self.tags)}
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
  
  def __str__ (self) -> str:
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
Relative Time: {self.to_str(self.relative_time_seconds)}
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

class BlogEntry (CodeforcesObject):
  def __init__ (
    self,
    id: int,
    original_locale: str,
    creation_time_seconds: int,
    author_handle: str,
    title: str,
    content: str,
    locale: str,
    modification_time_seconds: int,
    allow_view_history: bool,
    tags: typing.List[str],
    rating: int
  ):
    self.id = id
    self.original_locale = original_locale
    self.creation_time_seconds = creation_time_seconds
    self.author_handle = author_handle
    self.title = title
    self.content = content
    self.locale = locale
    self.modification_time_seconds = modification_time_seconds
    self.allow_view_history = allow_view_history
    self.tags = tags
    self.rating = rating
  
  def __str__ (self) -> str:
    blogentry = f"""\
    ID: {self.to_str(self.id)}
Author: {self.to_str(self.author_handle)}
 Title: {self.to_str(self.title)}
Rating: {self.to_str(self.rating)}

{self.to_str(self.content)}

Tags: {self.to_str(self.tags)}

    Creation time: {self.to_str(datetime.fromtimestamp(self.creation_time_seconds))}
Modification time: {self.to_str(datetime.fromtimestamp(self.modification_time_seconds))}
     View history: {self.to_str(self.allow_view_history)}
  Original Locale: {self.to_str(self.original_locale)}
           Locale: {self.to_str(self.locale)}
"""
    return blogentry

class Comment (CodeforcesObject):
  def __init__ (
    self,
    id: int,
    creation_time_seconds: int,
    commentator_handle: str,
    locale: str,
    text: str,
    rating: int,
    parent_comment_id: int
  ):
    self.id = id
    self.creation_time_seconds = creation_time_seconds
    self.commentator_handle = commentator_handle
    self.locale = locale
    self.text = text
    self.rating = rating
    self.parent_comment_id = parent_comment_id
  
  def __str__ (self) -> str:
    comment = f"""\
Author: {self.to_str(self.commentator_handle)}
Rating: {self.to_str(self.rating)}
Locale: {self.to_str(self.locale)}

Comment ID: {self.to_str(self.id)}
 Parent ID: {self.to_str(self.parent_comment_id)}

{self.to_str(self.text)}

Creation time: {self.to_str(datetime.fromtimestamp(self.creation_time_seconds))}
"""
    return comment

class RecentAction (CodeforcesObject):
  def __init__ (
    self,
    time_seconds: int,
    blog_entry: BlogEntry,
    comment: Comment
  ):
    self.time_seconds = time_seconds
    self.blog_entry = blog_entry
    self.comment = comment
  
  def __str__ (self) -> str:
    recentaction = f"""\
Time: {self.to_str(datetime.fromtimestamp(self.time_seconds))}

{self.to_str(self.blog_entry)}

{self.to_str(self.comment)}
"""
    return recentaction

class Contest (CodeforcesObject):
  def __init__ (
    self,
    id: int,
    name: str,
    type: str,
    phase: str,
    frozen: bool,
    duration_seconds: int,
    start_time_seconds: int,
    relative_time_seconds: int,
    prepared_by: str,
    website_url: str,
    description: str,
    difficulty: int,
    kind: str,
    icpc_region: str,
    country: str,
    city: str,
    season: str
  ):
    self.id = id
    self.name = name
    self.type = type
    self.phase = phase
    self.frozen = frozen
    self.duration_seconds = duration_seconds
    self.start_time_seconds = start_time_seconds
    self.relative_time_seconds = relative_time_seconds
    self.prepared_by = prepared_by
    self.website_url = website_url
    self.description = description
    self.difficulty = difficulty
    self.kind = kind
    self.icpc_region = icpc_region
    self.country = country
    self.city = city
    self.season = season
  
  def __str__ (self) -> str:
    contest = f"""\
  ID: {self.to_str(self.id)}
Name: {self.to_str(self.name)}
Type: {self.to_str(self.type)}

 Phase: {self.to_str(self.phase)}
Frozen: {self.to_str(self.frozen)}

   Start Time: {self.to_str(self.to_str(datetime.fromtimestamp(self.start_time_seconds)))}
Relative Time: {self.to_str(self.relative_time_seconds)}
 Duration (s): {self.to_str(self.duration_seconds)}

Prepared By: {self.to_str(self.prepared_by)}
Description: {self.to_str(self.description)}
Website URL: {self.to_str(self.website_url)}
 Difficulty: {self.to_str(self.difficulty)}

ICPC Region: {self.to_str(self.icpc_region)}
     Season: {self.to_str(self.season)}
       Kind: {self.to_str(self.kind)}
   Location: {self.to_str(self.city)}, {self.to_str(self.country)}
"""
    return contest

class RatingChange (CodeforcesObject):
  def __init__ (
    self,
    contest_id: int,
    contest_name: str,
    handle: str,
    rank: int,
    rating_update_time_seconds: int,
    old_rating: int,
    new_rating: int
  ):
    self.contest_id = contest_id
    self.contest_name = contest_name
    self.handle = handle
    self.rank = rank
    self.rating_update_time_seconds = rating_update_time_seconds
    self.old_rating = old_rating
    self.new_rating = new_rating

  def __str__ (self) -> str:
    rating_change = f"""\
Handle: {self.to_str(self.handle)}
  Rank: {self.to_str(self.rank)}

  Contest ID: {self.to_str(self.contest_id)}
Contest Name: {self.to_str(self.contest_name)}

Old Rating: {self.to_str(self.old_rating)}
New Rating: {self.to_str(self.new_rating)}

Rating Update Time: {self.to_str(datetime.fromtimestamp(self.rating_update_time_seconds))}
"""
    return rating_change

class Hack (CodeforcesObject):
  def __init__ (
    self,
    id: int,
    creation_time_seconds: int,
    hacker: Party,
    defender: Party,
    verdict: str,
    problem: Problem,
    test: str,
    judge_protocol: dict
  ):
    self.id = id
    self.creation_time_seconds = creation_time_seconds
    self.hacker = hacker
    self.defender = defender
    self.verdict = verdict
    self.problem = problem
    self.test = test
    self.judge_protocol = judge_protocol
  
  def __str__ (self) -> str:
    hack = f"""\
ID: {self.to_str(self.id)}
Creation Time: {self.to_str(datetime.fromtimestamp(self.creation_time_seconds))}

Hacker:
{self.to_str(self.hacker)}

Defender:
{self.to_str(self.defender)}

Problem:
{self.to_str(self.problem)}

Verdict: {self.to_str(self.verdict)}
   Test: {self.to_str(self.test)}

Judge Protocol: {self.to_str(json.dumps(self.judge_protocol, indent = 2))}
"""
    return hack

class RanklistRow (CodeforcesObject):
  def __init__ (
    self,
    party: Party,
    rank: int,
    points: float,
    penalty: int,
    successful_hack_count: int,
    unsuccessful_hack_count: int,
    problem_results: typing.List[ProblemResult],
    last_submission_time_seconds: int
  ):
    self.party = party
    self.rank = rank
    self.points = points
    self.penalty = penalty
    self.successful_hack_count = successful_hack_count
    self.unsuccessful_hack_count = unsuccessful_hack_count
    self.problem_results = problem_results
    self.last_submission_time_seconds = last_submission_time_seconds
  
  def __str__ (self) -> str:
    ranklist_row = f"""\
Party:
{self.to_str(self.party)}

   Rank: {self.to_str(self.rank)}
 Points: {self.to_str(self.points)}
Penalty: {self.to_str(self.penalty)}
  Hacks: +{self.to_str(self.successful_hack_count)}, -{self.to_str(self.unsuccessful_hack_count)}

Problem Results:
{self.to_str(self.problem_results)}

Last Submission Time: {
  self.to_str(datetime.fromtimestamp(self.last_submission_time_seconds))
  if self.last_submission_time_seconds != -1
  else 'NA'
}
"""
    return ranklist_row

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
    contest_id = _try_typecast(party.get('contestId'), int, 'NA')
    room = _try_typecast(party.get('room'), int, 'NA')
    start_time_seconds = _try_typecast(party.get('startTimeSeconds'), int, 'NA')
    team_id = _try_typecast(party.get('teamId'), int, 'NA')
    members = member_parse(party.get('members'))
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
    author = None
    
    if submission.get('problem') is not None:
      problem = problem_parse([submission.get('problem')])[0]
    
    if submission.get('author') is not None:
      author = party_parse([submission.get('author')])[0]
    
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
      author, programming_language, verdict, testset, passed_test_count,
      time_consumed_millis, memory_consumed_bytes, points
    ))
  
  return submission_list

def user_parse (users: typing.List[dict]) -> typing.List[User]:
  user_list = []

  for user in users:
    contribution = int(user.get('contribution'))
    rating = int(user.get('rating'))
    max_rating = int(user.get('maxRating'))
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

def blogentry_parse (blogentries: typing.List[dict]) -> typing.List[BlogEntry]:
  blogentry_list = []

  for blogentry in blogentries:
    id = int(blogentry.get('id'))
    original_locale = blogentry.get('originalLocale')
    creation_time_seconds = int(blogentry.get('creationTimeSeconds'))
    author_handle = blogentry.get('authorHandle')
    title = blogentry.get('title')
    content = blogentry.get('content')
    locale = blogentry.get('locale')
    modification_time_seconds = int(blogentry.get('modificationTimeSeconds'))
    allow_view_history = blogentry.get('allowViewHistory')
    tags = blogentry.get('tags')
    rating = int(blogentry.get('rating'))

    blogentry_list.append(BlogEntry(
      id, original_locale, creation_time_seconds, author_handle,
      title, content, locale, modification_time_seconds,
      allow_view_history, tags, rating
    ))
  
  return blogentry_list

def comment_parse (comments: typing.List[dict]) -> typing.List[Comment]:
  comment_list = []

  for comment in comments:
    parent_comment_id = _try_typecast(comment.get('parentCommentId'), int, 'NA')
    id = int(comment.get('id'))
    creation_time_seconds = int(comment.get('creationTimeSeconds'))
    commentator_handle = comment.get('commentatorHandle')
    locale = comment.get('locale')
    text = comment.get('text')
    rating = int(comment.get('rating'))

    comment_list.append(Comment(
      id, creation_time_seconds, commentator_handle,
      locale, text, rating, parent_comment_id
    ))
  
  return comment_list

def recentaction_parse (recentactions: typing.List[dict]) -> typing.List[RecentAction]:
  recentaction_list = []

  for recentaction in recentactions:
    comment = None
    blog_entry = None

    if recentaction.get('comment') is not None:
      comment = comment_parse([recentaction.get('comment')])[0]
    if recentaction.get('blogEntry') is not None:
      blog_entry = blogentry_parse([recentaction.get('blogEntry')])[0]
    
    time_seconds = int(recentaction.get('timeSeconds'))

    recentaction_list.append(RecentAction(
      time_seconds, blog_entry, comment
    ))
  
  return recentaction_list

def contest_parse (contests: typing.List[dict]) -> typing.List[Contest]:
  contest_list = []

  for contest in contests:
    start_time_seconds = _try_typecast(contest.get('startTimeSeconds'), int, 'NA')
    relative_time_seconds = _try_typecast(contest.get('relativeTimeSeconds'), int, 'NA')
    difficulty = _try_typecast(contest.get('difficulty'), int, 'NA')
    id = int(contest.get('id'))
    name = contest.get('name')
    type = contest.get('type')
    phase = contest.get('phase')
    frozen = contest.get('frozen')
    duration_seconds = contest.get('durationSeconds')
    prepared_by = contest.get('preparedBy')
    website_url = contest.get('websiteUrl')
    description = contest.get('description')
    kind = contest.get('kind')
    icpc_region = contest.get('icpcRegion')
    country = contest.get('country')
    city = contest.get('city')
    season = contest.get('season')

    contest_list.append(Contest(
      id, name, type, phase, frozen, duration_seconds,
      start_time_seconds, relative_time_seconds,
      prepared_by, website_url, description, difficulty,
      kind, icpc_region, country, city, season
    ))
  
  return contest_list

def ratingchange_parse (ratingchanges: typing.List[dict]) -> typing.List[RatingChange]:
  ratingchange_list = []

  for ratingchange in ratingchanges:
    contest_id = _try_typecast(ratingchange.get('contestId'), int, 'NA')
    rank = _try_typecast(ratingchange.get('rank'), int, 'NA')
    old_rating = _try_typecast(ratingchange.get('oldRating'), int, 'NA')
    new_rating = _try_typecast(ratingchange.get('newRating'), int, 'NA')
    rating_update_time_seconds = _try_typecast(ratingchange.get('ratingUpdateTimeSeconds'), int, 0)
    contest_name = ratingchange.get('contestName')
    handle = ratingchange.get('handle')

    ratingchange_list.append(RatingChange(
      contest_id, contest_name, handle, rank,
      rating_update_time_seconds, old_rating, new_rating
    ))
  
  return ratingchange_list

def hack_parse (hacks: typing.List[dict]) -> typing.List[Hack]:
  hack_list = []

  for hack in hacks:
    hacker = None
    defender = None
    problem = None

    if hack.get('hacker') is not None:
      hacker = party_parse([hack.get('hacker')])[0]
    if hack.get('defender') is not None:
      defender = party_parse([hack.get('defender')])[0]
    if hack.get('problem') is not None:
      problem = problem_parse([hack.get('problem')])[0]
    
    id = int(hack.get('id'))
    creation_time_seconds = int(hack.get('creationTimeSeconds'))
    verdict = hack.get('verdict')
    test = hack.get('test')
    judge_protocol = hack.get('judgeProtocol')

    hack_list.append(Hack(
      id, creation_time_seconds, hacker, defender,
      verdict, problem, test, judge_protocol
    ))
  
  return hack_list

def ranklistrow_parse (ranklistrows: typing.List[dict]) -> typing.List[RanklistRow]:
  ranklistrow_list = []

  for ranklistrow in ranklistrows:
    party = None
    problem_results = []

    if ranklistrow.get('party') is not None:
      party = party_parse([ranklistrow.get('party')])[0]
    if ranklistrow.get('problemResult') is not None:
      problem_results = problemresult_parse(ranklistrow.get('problemResult'))
    
    last_submission_time_seconds = \
      _try_typecast(ranklistrow.get('lastSubmissionTimeSeconds'), int, -1)
    rank = int(ranklistrow.get('rank'))
    points = float(ranklistrow.get('points'))
    penalty = int(ranklistrow.get('penalty'))
    successful_hack_count = int(ranklistrow.get('successfulHackCount'))
    unsuccessful_hack_count = int(ranklistrow.get('unsuccessfulHackCount'))

    ranklistrow_list.append(RanklistRow(
      party, rank, points, penalty,
      successful_hack_count, unsuccessful_hack_count,
      problem_results, last_submission_time_seconds
    ))

  return ranklistrow_list
