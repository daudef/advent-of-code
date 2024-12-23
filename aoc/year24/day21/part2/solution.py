from aoc import helpers
from aoc.year24.day21.part1 import solution as p1


def solution(lines: list[str]):
    return sum(p1.get_score_of_line(line, robot_count=25) for line in lines)


if __name__ == '__main__':
    helpers.run_solution(solution)
