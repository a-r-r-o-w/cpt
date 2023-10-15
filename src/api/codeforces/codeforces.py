import asyncio
import aiohttp
import binascii
import hashlib
import random
import ratelimit
import string
import typing
import time

from cfobject import (
    Member,
    Party,
    Problem,
    ProblemStatistic,
    ProblemResult,
    Submission,
    User,
    BlogEntry,
    Comment,
    RecentAction,
    Contest,
    RatingChange,
    Hack,
    RanklistRow,
    member_parse,
    party_parse,
    problem_parse,
    problemstatistic_parse,
    problemresult_parse,
    submission_parse,
    user_parse,
    blogentry_parse,
    comment_parse,
    recentaction_parse,
    contest_parse,
    ratingchange_parse,
    hack_parse,
    ranklistrow_parse,
)

from cfexception import (
    StatusNotFoundError,
    StatusFailedError,
    CommentNotFoundError,
    ResultNotFoundError,
)


class CodeforcesAPIRoute:
    base_url = "https://codeforces.com/api/"

    _API_Routes = {
        "blog_comments": "blogEntry.comments",
        "blog": "blogEntry.view",
        "contest_hacks": "contest.hacks",
        "contest_list": "contest.list",
        "contest_rating_changes": "contest.ratingChanges",
        "contest_standings": "contest.standings",
        "contest_status": "contest.status",
        "problemset_problems": "problemset.problems",
        "problemset_status": "problemset.recentStatus",
        "recent_actions": "recentActions",
        "user_blogs": "user.blogEntries",
        "user_friends": "user.friends",
        "user_info": "user.info",
        "user_ratedlist": "user.ratedList",
        "user_rating": "user.rating",
        "user_status": "user.status",
    }

    def __init__(self, route: str):
        if route not in self._API_Routes:
            error_msg = f"API route '{route}' is invalid! Choose from:\n" + "\n".join(
                f"({index:02}) {route}"
                for index, route in enumerate(self._API_Routes.keys(), start=1)
            )
            raise ValueError(error_msg)

        self.route = route

    def get_url(self) -> str:
        return self.base_url + self._API_Routes[self.route]

    def get_path(self) -> str:
        return self._API_Routes[self.route]


@ratelimit.limits(calls=1, period=2)
async def _API_call(callback, *args, **kwargs):
    return await callback(*args, **kwargs)


async def _loop_until_success(callback, *args, **kwargs):
    sleep_duration = 1

    while True:
        try:
            return_value = await _API_call(callback, *args, **kwargs)
        except ratelimit.RateLimitException:
            await asyncio.sleep(sleep_duration)
        else:
            break

    return return_value


def check_status(response: dict):
    if "status" not in response.keys():
        raise StatusNotFoundError(
            "Codeforces API call response does not contain a status message"
        )
    elif response.get("status") == "OK":
        if "result" not in response.keys():
            raise ResultNotFoundError(
                "Codeforces API call response does not contain result"
            )
    else:
        if "comment" not in response.keys():
            raise CommentNotFoundError(
                'Reason for Codeforces API call {"status": "FAILED"} not found'
            )
        else:
            raise StatusFailedError(response.get("comment"))


async def codeforces_api_call(
    route: CodeforcesAPIRoute,
    params: dict,
) -> dict:
    async def request() -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(route.get_url(), params=params) as r:
                return await r.json()

    response = await _loop_until_success(request)
    check_status(response)
    return response


class CodeforcesAPI:
    def __init__(self):
        pass

    async def blogentry_comments(self, *, blogentry_id: int) -> typing.List[Comment]:
        route = CodeforcesAPIRoute("blog_comments")
        params = {"blogEntryId": blogentry_id}
        response = await codeforces_api_call(route, params)
        return comment_parse(response.get("result"))

    async def blogentry_view(self, *, blogentry_id: int) -> typing.List[BlogEntry]:
        route = CodeforcesAPIRoute("blog")
        params = {"blogEntryId": blogentry_id}
        response = await codeforces_api_call(route, params)
        return blogentry_parse([response.get("result")])

    async def contest_hacks(self, *, contest_id: int) -> typing.List[Hack]:
        route = CodeforcesAPIRoute("contest_hacks")
        params = {"contestId": contest_id}
        response = await codeforces_api_call(route, params)
        return hack_parse(response.get("result"))

    async def contest_rating_changes(
        self, *, contest_id: int
    ) -> typing.List[RatingChange]:
        route = CodeforcesAPIRoute("contest_rating_changes")
        params = {"contestId": contest_id}
        response = await codeforces_api_call(route, params)
        return ratingchange_parse(response.get("result"))

    async def contest_standings(
        self,
        *,
        contest_id: int,
        start_index: int = None,
        count: int = None,
        handles: typing.List[str] = None,
        room: int = None,
        show_unofficial: bool = False,
    ) -> typing.Tuple[Contest, typing.List[Problem], typing.List[RanklistRow]]:
        route = CodeforcesAPIRoute("contest_standings")
        params = {
            "contestId": contest_id,
            "showUnofficial": "true" if show_unofficial else "false",
        }

        if start_index is not None:
            params["from"] = start_index
        if count is not None:
            params["count"] = count
        if handles is not None:
            params["handles"] = ";".join(handles)
        if room is not None:
            params["room"] = room

        response = await codeforces_api_call(route, params)
        result = response.get("result")
        contest = contest_parse([result.get("contest")])[0]
        problem_list = problem_parse(result.get("problems"))
        ranklistrow_list = ranklistrow_parse(result.get("rows"))
        return contest, problem_list, ranklistrow_list

    async def contest_status(
        self,
        *,
        contest_id: int,
        handle: str = None,
        start_index: int = None,
        count: int = None,
    ) -> typing.List[Submission]:
        route = CodeforcesAPIRoute("contest_status")
        params = {"contestId": contest_id}

        if handle is not None:
            params["handle"] = handle
        if start_index is not None:
            params["from"] = start_index
        if count is not None:
            params["count"] = count

        response = await codeforces_api_call(route, params)
        return submission_parse(response.get("result"))

    async def problemset_problems(
        self, *, tags: typing.List[str] = None, problemset_name: str = None
    ) -> typing.Tuple[typing.List[Problem], typing.List[ProblemStatistic]]:
        route = CodeforcesAPIRoute("problemset_problems")
        params = {}

        if tags is not None:
            params["tags"] = ";".join(tags)
        if problemset_name is not None:
            params["problemsetName"] = problemset_name

        response = await codeforces_api_call(route, params)
        result = response.get("result")
        problem_list = problem_parse(result.get("problems"))
        problemstatistic_list = problemstatistic_parse(result.get("problemStatistics"))
        return problem_list, problemstatistic_list

    async def problemset_recent_status(
        self, *, count: int, problemset_name: str = None
    ) -> typing.List[Submission]:
        route = CodeforcesAPIRoute("problemset_status")
        params = {"count": count}

        if problemset_name is not None:
            params["problemsetName"] = problemset_name

        response = await codeforces_api_call(route, params)
        return submission_parse(response.get("result"))

    async def recent_actions(self, *, max_count: int) -> typing.List[RecentAction]:
        route = CodeforcesAPIRoute("recent_actions")
        params = {"maxCount": max_count}

        response = await codeforces_api_call(route, params)
        return recentaction_parse(response.get("result"))

    async def user_blog_entries(self, *, handle: str) -> typing.List[BlogEntry]:
        route = CodeforcesAPIRoute("user_blogs")
        params = {"handle": handle}

        response = await codeforces_api_call(route, params)
        return blogentry_parse(response.get("result"))

    async def user_friends(
        self,
        api_key: str,
        secret: str,
        time: int = round(time.time()),
        *,
        only_online: bool = False,
    ) -> typing.List[str]:
        route = CodeforcesAPIRoute("user_friends")

        padding = "".join(random.sample(string.ascii_letters + string.digits, 6))

        sign = padding
        sign += "/"
        sign += route.get_path()
        sign += "?"
        sign += f"apiKey={api_key}"
        sign += "&"
        sign += f'onlyOnline={"true" if only_online else "false"}'
        sign += "&"
        sign += f"time={time}"
        sign += "#"
        sign += secret

        hash = hashlib.sha512(sign.encode()).hexdigest()
        api_sig = padding + hash

        params = {
            "apiKey": api_key,
            "time": time,
            "apiSig": api_sig,
            "onlyOnline": "true" if only_online else "false",
        }

        response = await codeforces_api_call(route, params)
        return response.get("result")

    async def user_info(self, *, handles: typing.List[str]) -> typing.List[User]:
        route = CodeforcesAPIRoute("user_info")
        params = {"handles": ";".join(handles)}

        response = await codeforces_api_call(route, params)
        return user_parse(response.get("result"))

    async def user_ratedlist(
        self, *, contest_id: int = None, active_only: bool = False
    ) -> typing.List[User]:
        route = CodeforcesAPIRoute("user_ratedlist")
        params = {"activeOnly": "true" if active_only else "false"}

        if contest_id is not None:
            params["contestId"] = contest_id

        response = await codeforces_api_call(route, params)
        return user_parse(response.get("result"))

    async def user_rating(self, *, handle: str) -> typing.List[RatingChange]:
        route = CodeforcesAPIRoute("user_rating")
        params = {"handle": handle}

        response = await codeforces_api_call(route, params)
        return ratingchange_parse(response.get("result"))

    async def user_status(
        self, *, handle: str, start_index: int = None, count: int = None
    ) -> typing.List[Submission]:
        route = CodeforcesAPIRoute("user_status")
        params = {"handle": handle}

        if start_index is not None:
            params["from"] = start_index
        if count is not None:
            params["count"] = count

        response = await codeforces_api_call(route, params)
        return submission_parse(response.get("result"))


def main():
    async def async_main():
        API = CodeforcesAPI()

        blogentry_comments = await API.blogentry_comments(blogentry_id=1)
        print(blogentry_comments[0])

        blogentry_view = await API.blogentry_view(blogentry_id=1)
        print(blogentry_view[0])

        contest_hacks = await API.contest_hacks(contest_id=1642)
        print(contest_hacks[0])

        contest_rating_changes = await API.contest_rating_changes(contest_id=1642)
        for ratingchange in contest_rating_changes:
            if ratingchange.handle == "4rrow":
                print(ratingchange)

        contest_standings = await API.contest_standings(
            contest_id=1642, handles=["4rrow"]
        )
        print(contest_standings[0])
        for problem in contest_standings[1]:
            print(problem)
        for ranklistrow in contest_standings[2]:
            print(ranklistrow)

        contest_status = await API.contest_status(contest_id=1642, handle="4rrow")
        print(contest_status[0])

        problemset_problems = await API.problemset_problems(
            tags=["meet-in-the-middle", "matrices"]
        )
        for problem, problemstatistic in zip(*problemset_problems):
            print(problem)
            print(problemstatistic)

        problemset_recent_status = await API.problemset_recent_status(count=1)
        print(problemset_recent_status[0])

        recent_actions = await API.recent_actions(max_count=1)
        print(recent_actions[0])

        user_blog_entries = await API.user_blog_entries(handle="MikeMirzayanov")
        print(user_blog_entries[0])

        # import os
        # import dotenv

        # dotenv.load_dotenv()

        # user_friends = await API.user_friends(
        #   api_key = os.getenv('API_KEY'),
        #   secret = os.getenv('API_SECRET')
        # )
        # print(user_friends)

        user_info_list = await API.user_info(handles=["4rrow"])
        for user in user_info_list:
            print(user)

        user_ratedlist = await API.user_ratedlist(contest_id=1642, active_only=True)
        for user in user_ratedlist:
            if user.handle == "4rrow":
                print(user)

        user_rating = await API.user_rating(handle="4rrow")
        print(user_rating[0])

        user_status = await API.user_status(handle="4rrow", start_index=1, count=1)
        for status in user_status:
            print(status)

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
