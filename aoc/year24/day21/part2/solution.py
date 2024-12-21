from aoc import helpers
from aoc.year24.day21.part1 import solution as p1


def solution(lines: list[str]):
    return sum(
        (len(p1.get_path_of_code(p1.parse_code(line), robot_count=15))) * int(line[:-1])
        for line in lines
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
