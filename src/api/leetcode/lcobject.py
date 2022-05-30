import json
import typing
import markdownify

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
  
  def to_markdown (self):
    return problem_to_markdown(self)

def problem_parse (data: dict):
  id = int(data.get('questionId'))
  frontend_id = int(data.get('questionFrontendId'))
  title = data.get('title')
  slug = data.get('titleSlug')
  difficulty = data.get('difficulty')
  likes = data.get('likes')
  dislikes = data.get('dislikes')
  
  content = data.get('content').strip().replace('<p>', '').replace('&nbsp;', '').replace('</p>', '')
  statement = markdownify.markdownify(content)
  
  tags = []
  for tag in data.get('topicTags'):
    tags.append(tag.get('slug'))
  
  _stats: dict = json.loads(data.get('stats'))
  total_accepted = _stats.get('totalAcceptedRaw')
  total_submissions = _stats.get('totalSubmissionRaw')
  acceptance_rate = _stats.get('acRate')
  hints = data.get('hints')
  similar_problems = json.loads(data.get('similarQuestions'))
  
  return Problem(
    id, frontend_id, title, slug, statement,
    difficulty, likes, dislikes, tags,
    total_accepted, total_submissions,
    acceptance_rate, hints, similar_problems
  )

def problem_to_markdown (problem: Problem):
  newline = '\n'
  md = f"""\
# [{problem.frontend_id}] {problem.title}

{f"**[{', '.join(tag for tag in problem.tags)}]**" if problem.tags else ''}

### Statement

{problem.statement}

<br>

### Hints

{newline.join('- ' + hint for hint in problem.hints) if problem.hints else 'None'}

<br>

### Solution

```
```

<br>

### Statistics

- total accepted: {problem.total_accepted}
- total submissions: {problem.total_submissions}
- acceptance rate: {problem.acceptance_rate}
- likes: {problem.likes}
- dislikes: {problem.dislikes}

<br>

### Similar Problems

{
  newline.join(f"- [{p['title']}](https://leetcode.com/problems/{p['titleSlug']}) ({p['difficulty']})"
  for p in problem.similar_problems) if problem.similar_problems else 'None'
}
"""
  return md
