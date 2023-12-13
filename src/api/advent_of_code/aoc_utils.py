import bs4
import markdownify

from .aoc_object import Problem


class CustomMarkdownConverter(markdownify.MarkdownConverter):
    def convert_a(
        self, el: bs4.BeautifulSoup, text: str, convert_as_inline: bool
    ) -> str:
        href = el.get("href")
        return f"[{text}]({href})"

    def convert_em(
        self, el: bs4.BeautifulSoup, text: str, convert_as_inline: bool
    ) -> str:
        return f"*{text}*"


def problem_parse(data: str, year: int, day: int) -> Problem:
    soup = bs4.BeautifulSoup(data, features="lxml")

    day_desc: bs4.BeautifulSoup = soup.find_all("article", class_="day-desc")[0]
    description = str(day_desc)

    return Problem(
        year=year,
        day=day,
        description=description,
    )


def problem_to_markdown(problem: Problem) -> str:
    data = f"{problem.description}"
    md = CustomMarkdownConverter().convert(data).strip()
    return md
