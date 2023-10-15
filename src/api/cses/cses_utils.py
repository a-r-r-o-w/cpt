import bs4

from .cses_object import Problem


def problem_parse(data: str) -> Problem:
    soup = bs4.BeautifulSoup(data, features="lxml")

    id: int = 0
    name: str = ""
    statement: str = ""
    time_limit: int = 0
    memory_limit: int = 0
    total_accepted: int = 0
    total_submissions: int = 0
    success_rate: float = 0

    print(soup.prettify())

    return Problem(
        id,
        name,
        statement,
        time_limit,
        memory_limit,
        total_accepted,
        total_submissions,
        success_rate,
    )
