from aoc import helpers
from aoc.lib import Delta
from aoc.year24.day20.part1 import solution as p1

deltas_of_norm_1 = list(Delta.of_norm(1))


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    cost_threshold = 50 if len(lines) < 20 else 100
    return p1.solve(input, cost_threshold, max_cheat_size=20)


if __name__ == '__main__':
    helpers.run_solution(solution)
