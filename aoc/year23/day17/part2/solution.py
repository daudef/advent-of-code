from aoc import helpers
from aoc.year23.day17.part1 import solution as p1


def solution(lines: list[str]):
    return p1.solve(lines, mom_range=p1.MomentumRange(min_len=4, max_len=10))


if __name__ == '__main__':
    helpers.run_solution(solution)
