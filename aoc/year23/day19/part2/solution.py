import functools
import typing

from aoc import helpers
from aoc.year23.day19.part1 import solution as p1

ObjectRange: typing.TypeAlias = dict[str, range]


def obj_range_size(obj_range: p1.ObjectRange):
    return functools.reduce(
        lambda a, b: a * b, [len(obj_range.get(k, range(1, 4001))) for k in 'xmas']
    )


def solution(lines: list[str]):
    input = p1.Input.parse(lines)
    return sum(obj_range_size(obj_range) for obj_range in input.get_ranges())


if __name__ == '__main__':
    helpers.run_solution(solution)
