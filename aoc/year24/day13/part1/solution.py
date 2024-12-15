import dataclasses
import typing

from aoc import helpers
from aoc.lib import Delta, Pos


@dataclasses.dataclass
class Problem:
    a: Delta
    b: Delta
    prize: Pos


def parse_delta(s: str, name: typing.Literal['X', 'Y']):
    # X+26
    s = s.strip()
    prefix = f'{name}+'
    assert s.startswith(prefix), (s, prefix)
    s = s.removeprefix(prefix)
    return int(s)


def parse_button(line: str, name: typing.Literal['A', 'B']):
    # Button A: X+26, Y+66
    prefix = f'Button {name}: '
    assert line.startswith(prefix), (line, prefix)
    line = line.removeprefix(prefix)
    x_delta, y_delta = line.split(',')
    return Delta(drow=parse_delta(y_delta, 'Y'), dcol=parse_delta(x_delta, 'X'))


def parse_coordinate(s: str, name: typing.Literal['X', 'Y']):
    # X=7237
    s = s.strip()
    prefix = f'{name}='
    assert s.startswith(prefix), (s, prefix)
    s = s.removeprefix(prefix)
    return int(s)


def parse_prize(line: str):
    # Prize: X=7237, Y=4563
    prefix = 'Prize: '
    assert line.startswith(prefix)
    line = line.removeprefix(prefix)
    x_coord, y_coord = line.split(',')
    return Pos(row=parse_coordinate(y_coord, 'Y'), col=parse_coordinate(x_coord, 'X'))


def parse_problem(lines: tuple[str, str, str]):
    # Button A: X+32, Y+60
    # Button B: X+93, Y+51
    # Prize: X=7237, Y=4563
    return Problem(
        a=parse_button(lines[0], 'A'), b=parse_button(lines[1], 'B'), prize=parse_prize(lines[2])
    )


def parse_problems(lines: list[str]):
    i = 0
    problems: list[Problem] = []
    while i + 2 < len(lines):
        problems.append(parse_problem((lines[i], lines[i + 1], lines[i + 2])))
        if i + 3 < len(lines):
            assert lines[i + 3] == ''
        i += 4
    return problems


@dataclasses.dataclass
class Solution:
    a: int
    b: int


def get_solution_cost(solution: Solution):
    return 3 * solution.a + solution.b


def solve_problem(problem: Problem):
    ratio = problem.prize.row / problem.prize.col
    b = 1
    a = -(problem.b.drow - (ratio * problem.b.dcol)) / (problem.a.drow - (ratio * problem.a.dcol))
    total_row = a * problem.a.drow + b * problem.b.drow
    coef = problem.prize.row / total_row
    candidate = Solution(a=round(coef * a), b=round(coef * b))
    pos = Pos(0, 0) + candidate.a * problem.a + candidate.b * problem.b
    return candidate if pos == problem.prize else None


def solution(lines: list[str]):
    problems = parse_problems(lines)

    return sum(
        get_solution_cost(solution)
        for problem in problems
        if (solution := solve_problem(problem)) is not None
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
