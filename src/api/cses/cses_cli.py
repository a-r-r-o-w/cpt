from .cses import CSESAPI


class CSESCLI:
    """CSES Command Line Interface"""

    def __init__(self):
        self.api = CSESAPI()

    async def clone(self, url: str, *, path: str = ".") -> None:
        """Clone a CSES Problem
        :param str url: (required) problem url (example: https://leetcode.com/problems/two-sum/)
        :param str path: (optional) path (default is current working directory)
        :raises ValueError: invalid url
        """
        id = int(url.split("/")[-1])
        problem = await self.api.get_problem_data(id=id)
