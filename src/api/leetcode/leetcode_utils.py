import json
import re
import typing
import urllib.parse

from utils import CustomMarkdownConverter
from .leetcode_object import (
    ContestURL,
    LeetcodeURL,
    Problem,
    ProblemURL,
)
from .leetcode_constants import LeetcodeURLs


def problem_parse(data: typing.Dict[str, str]) -> None:
    id = int(data.get("questionId"))
    frontend_id = int(data.get("questionFrontendId"))
    title = data.get("title")
    slug = data.get("titleSlug")
    difficulty = data.get("difficulty")
    likes = data.get("likes")
    dislikes = data.get("dislikes")

    content = (
        data.get("content")
        .strip()
        .replace("<p>", "")
        .replace("&nbsp;", "")
        .replace("</p>", "")
    )
    statement = CustomMarkdownConverter(sup_symbol="^").convert(content)

    tags = []
    for tag in data.get("topicTags"):
        tags.append(tag.get("slug"))

    _stats: dict = json.loads(data.get("stats"))
    total_accepted = _stats.get("totalAcceptedRaw")
    total_submissions = _stats.get("totalSubmissionRaw")
    acceptance_rate = _stats.get("acRate")
    hints = data.get("hints")
    similar_problems = json.loads(data.get("similarQuestions"))

    return Problem(
        id,
        frontend_id,
        title,
        slug,
        statement,
        difficulty,
        likes,
        dislikes,
        tags,
        total_accepted,
        total_submissions,
        acceptance_rate,
        hints,
        similar_problems,
    )


def leetcode_url_parse(url: str) -> LeetcodeURL:
    urlsplit = urllib.parse.urlsplit(url)

    if url.startswith(LeetcodeURLs.PROBLEMS) or url.startswith(LeetcodeURLs.CONTEST):
        slug = re.search(r"/problems/([a-zA-Z0-9\-]+)", urlsplit.path)
        if slug is not None:
            return ProblemURL(slug.group(1))

    if url.startswith(LeetcodeURLs.CONTEST):
        slug = re.search(r"/contest/([a-zA-Z0-9\-]+)", urlsplit.path)
        if slug is not None:
            return ContestURL(slug.group(1))

    raise ValueError("Invalid URL")


def problem_to_markdown(problem: Problem) -> None:
    newline = "\n"
    md = f"""\
# [{problem.frontend_id}] {problem.title}

{f"**[{', '.join(tag for tag in problem.tags)}]**" if problem.tags else ''}

### Statement

{problem.statement}

<br />

### Hints

{newline.join('- ' + hint for hint in problem.hints) if problem.hints else 'None'}

<br />

### Solution

```
```

<br />

### Statistics

- total accepted: {problem.total_accepted}
- total submissions: {problem.total_submissions}
- acceptance rate: {problem.acceptance_rate}
- likes: {problem.likes}
- dislikes: {problem.dislikes}

<br />

### Similar Problems

{
  newline.join(f"- [{p['title']}](https://leetcode.com/problems/{p['titleSlug']}) ({p['difficulty']})"
  for p in problem.similar_problems) if problem.similar_problems else 'None'
}
"""
    return md
