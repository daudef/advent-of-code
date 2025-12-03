from aoc import helpers
from aoc.year25.day03.part1 import solution as p1


def solution(lines: list[str]):
    return sum(p1.find_best_joltage(bank, 12) for bank in p1.parse_lines(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
