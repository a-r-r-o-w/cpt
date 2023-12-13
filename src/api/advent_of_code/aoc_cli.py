from .aoc import AdventOfCodeAPI
from .aoc_utils import problem_to_markdown
from utils import cd


class AdventOfCodeCLI:
    """CSES Command Line Interface"""

    def __init__(self):
        self.api = AdventOfCodeAPI()

    async def clone(self, url: str, *, path: str = ".") -> None:
        """
        Clone an Advent of Code Problem.
        
        Parameters:
            url (str):
                Problem URL (example: https://adventofcode.com/2023/day/1)
            path (str, *optional*):
                Location where problem is to be saved (default is current working directory)
        """
        
        url_split = url.split("/")
        year = int(url_split[-3])
        day = int(url_split[-1])
        problem = await self.api.get_problem_data(year=year, day=day)
        
        with cd(path):
            filename = f"README.md"

            with open(filename, "w") as file:
                file.write(problem_to_markdown(problem))
