class AdventOfCodeObject:
    """Represents an AdventOfCode Object"""

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

class Problem(AdventOfCodeObject):
    """Represents and AdventOfCode Problem"""

    def __init__(
        self,
        year: int,
        day: int,
        description: str,
    ) -> None:
        self.year = year
        self.day = day
        self.description = description
