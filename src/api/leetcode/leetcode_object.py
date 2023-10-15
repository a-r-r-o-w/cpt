from typing import List, Union

from .leetcode_constants import LeetcodeURLs


class LeetcodeObject:
    """Represents a Leetcode Object"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Problem(LeetcodeObject):
    """Represents a Leetcode Problem"""

    def __init__(
        self,
        id: int,
        frontend_id: int,
        title: str,
        slug: str,
        statement: str,
        difficulty: str,
        likes: int,
        dislikes: int,
        tags: List[str],
        total_accepted: int,
        total_submissions: int,
        acceptance_rate: float,
        hints: List[str],
        similar_problems: List[dict],
    ) -> None:
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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.frontend_id} - {self.title}]>"


class ProblemURL(LeetcodeObject):
    r"""Represents a Leetcode Problem URL"""

    def __init__(self, slug: str):
        self.slug = slug
        self.url = LeetcodeURLs.PROBLEMS + self.slug


class ContestURL(LeetcodeObject):
    r"""Represents a Leetcode Contest URL"""

    def __init__(self, slug: str):
        self.slug = slug
        self.url = LeetcodeURLs.CONTEST + self.slug


LeetcodeURL = Union[ProblemURL, ContestURL]
