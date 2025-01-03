import asyncio
import contextlib
import dataclasses
import functools
import inspect
import pathlib
import sqlite3
import sys
import tempfile
import time
import typing

import cyclopts
import httpx
import rich.highlighter
import typer

type Solution = typing.Callable[[list[str]], str | int]

AOC_BASE_URL = 'https://adventofcode.com'
BASE_DIR = pathlib.Path(__file__).parent


def run_main(main: typing.Callable[..., typing.Any]):
    if asyncio.iscoroutinefunction(main):

        @functools.wraps(main)
        def wrapper(*args: typing.Any, **kwargs: typing.Any):  # noqa: ANN401
            asyncio.run(main(*args, **kwargs))

        callable = wrapper
    else:
        callable = main

    rich.get_console().highlighter = rich.highlighter.NullHighlighter()
    app = typer.Typer(pretty_exceptions_enable=False)
    app.command()(callable)
    app()


def _get_session_cookie():
    # Get firefox cookie db path
    assert sys.platform == 'darwin'
    firefox_profile_dir = pathlib.Path(
        '~/Library/Application Support/Firefox/Profiles/'
    ).expanduser()
    profiles = list(firefox_profile_dir.iterdir())
    profile = next((p for p in profiles if p.name.endswith('default-release')), None) or profiles[0]
    cookies_db_path = profile / 'cookies.sqlite'

    # Get session cookie
    with tempfile.TemporaryDirectory(dir='.') as dir:
        new_cookie_db_path = pathlib.Path(dir) / 'cookie.db'
        new_cookie_db_path.write_bytes(cookies_db_path.read_bytes())
        with sqlite3.connect(new_cookie_db_path) as db:
            cookie = next(
                db.execute(
                    """
                        SELECT value
                        FROM moz_cookies
                        WHERE host = '.adventofcode.com'
                        AND name = 'session'
                    """
                )
            )[0]
            assert isinstance(cookie, str)
            return cookie


@contextlib.asynccontextmanager
async def _get_http_client():
    async with httpx.AsyncClient(
        headers={'user-agent': '', 'cookie': f'session={_get_session_cookie()}'}
    ) as http_client:
        yield http_client


async def _request_text(
    url: str, method: str, http_client: httpx.AsyncClient, data: dict[str, typing.Any] | None = None
):
    response = await http_client.request(method=method, url=url, data=data)
    if response.status_code != 200:
        raise RuntimeError(
            f'{method.upper()} {url} responded {response.status_code}: {response.text}'
        )
    return response.text


def format_short_year(year: int):
    return year % 100


def format_long_year(year: int):
    if 70 <= year < 100:
        year += 1900
    if 0 <= year < 70:
        year += 2000
    return year


@dataclasses.dataclass
class Day:
    year: int
    day: int

    def __post_init__(self):
        self.year = format_long_year(self.year)

    @property
    def dir_path(self):
        return BASE_DIR / f'year{format_short_year(self.year):0>2}' / f'day{self.day:0>2}'

    @property
    def day_url(self):
        return f'{AOC_BASE_URL}/{self.year}/day/{self.day}'

    @staticmethod
    def parse_from_dir_path(path: pathlib.Path):
        year = int(path.parent.name.removeprefix('year'))
        day = int(path.name.removeprefix('day'))
        return Day(year=year, day=day)

    async def get_input(self, http_client: httpx.AsyncClient):
        return await _request_text(f'{self.day_url}/input', 'get', http_client)


@dataclasses.dataclass
class Problem:
    day: Day
    part: int

    @property
    def dir_path(self):
        return self.day.dir_path / f'part{self.part}'

    @property
    def exemple_input_path(self):
        return self.dir_path / 'exemple_input.txt'

    @property
    def exemple_result_path(self):
        return self.dir_path / 'exemple_result.txt'

    @property
    def solution_path(self):
        return self.dir_path / 'solution.py'

    @staticmethod
    def parse_from_dir_path(path: pathlib.Path):
        part = int(path.name.removeprefix('part'))

        assert part in {1, 2}
        return Problem(Day.parse_from_dir_path(path.parent), part=part)

    async def post_answer(self, answer: str):
        async with _get_http_client() as http_client:
            return await _request_text(
                f'{self.day.day_url}/answer',
                'post',
                http_client,
                data={'level': self.part, 'answer': answer},
            )


@dataclasses.dataclass
class Result:
    answer: str
    duration_s: float

    @property
    def formated_duration(self):
        if self.duration_s < 1:
            return f'{self.duration_s * 1000:0.0f}ms'
        return f'{self.duration_s:1.1f}s'


def time_and_run_solution(sol: Solution, input: list[str]):
    t0 = time.perf_counter()
    answer = str(sol(input))
    duration_s = time.perf_counter() - t0
    return Result(answer=answer, duration_s=duration_s)


async def _run_solution(sol: Solution, execute_real_input: bool):
    problem = Problem.parse_from_dir_path(pathlib.Path(inspect.getfile(sol)).parent)

    exemple_input = problem.exemple_input_path.read_text(encoding='utf-8').splitlines()
    exemple_result = str(sol(exemple_input))
    print(f'result on exemple: {exemple_result}', end='')

    try:
        expected_result = problem.exemple_result_path.read_text(encoding='utf-8')
    except Exception:
        print('\nerror: cannot find expected result')
        exit()

    if exemple_result != expected_result:
        print(f' (expected {expected_result})')
        exit()
    else:
        print(' (ok)')

    if not execute_real_input:
        print('skipping real input')
        return

    async with _get_http_client() as http_client:
        try:
            input = (await problem.day.get_input(http_client)).splitlines()
        except Exception:
            print('Cannot find input for the day')
            raise

    print('result on real input: ', end='')

    result = time_and_run_solution(sol, input)

    print(f'{result.answer} ({result.formated_duration})')

    print('posting ... ', end='')

    response = await problem.post_answer(answer=result.answer)
    if 'Did you already complete it?' in response:
        print('did you already complete it?')
    elif 'You gave an answer too recently' in response:
        print('please wait a bit.')
    elif "That's not the right answer" in response:
        print('wrong answer ...')
    elif "That's the right answer" in response:
        print('right answer :)')
    else:
        print('unknown response: ', response)


def run_solution(sol: Solution):
    APP = cyclopts.App()

    @APP.default
    async def _(*, real_input: bool = True):
        await _run_solution(sol, execute_real_input=real_input)

    APP()
