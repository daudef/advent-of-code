from aoc import helpers
from aoc.year24.day11.part1 import solution as p1


def solution(lines: list[str]):
    return sum(p1.get_stone_count(v, 75, {}) for v in p1.parse_input(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
