from .leetcode import LeetcodeAPI
from .leetcode_object import ContestURL, ProblemURL
from .leetcode_utils import leetcode_url_parse, problem_to_markdown
from utils import cd


class LeetcodeCLI:
    """LeetCode Command Line Interface"""

    def __init__(self) -> None:
        self.api = LeetcodeAPI()

    async def clone(self, url: str, *, path: str = ".") -> None:
        r"""Clone a LeetCode Problem

        Parameters:
            url (str):
                Problem or Contest URL
                (example problem url: https://leetcode.com/problems/two-sum/)
                (example contest url: https://leetcode.com/contest/weekly-contest-100/)
            path (str): Path (default is current working directory)
        
        Raises:
            ValueError: invalid url
        """

        parsed_url = leetcode_url_parse(url)

        with cd(path):
            if isinstance(parsed_url, ProblemURL):
                await self._clone_problem(parsed_url)
            elif isinstance(parsed_url, ContestURL):
                await self._clone_contest(parsed_url)
    
    async def _clone_problem(self, parsed_url: ProblemURL) -> None:
        problem = await self.api.get_problem_data(slug=parsed_url.slug)
        filename = f"{problem.frontend_id}-{problem.slug}.md"
        
        with open(filename, "w") as file:
            file.write(problem_to_markdown(problem))
    
    async def _clone_contest(self, parsed_url: ContestURL) -> None:
        contest_problems = await self.api.get_contest_data(slug=parsed_url.slug)

        for problem in contest_problems:
            filename = f"{problem.frontend_id}-{problem.slug}.md"
            with open(filename, "w") as file:
                file.write(problem_to_markdown(problem))
