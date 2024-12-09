from aoc import helpers
from aoc.year24.day08.part1 import solution as p1


def solution(lines: list[str]):
    return len(p1.get_all_resonant_poses(p1.parse_input(lines), min_dist=0, max_dist=None))


if __name__ == '__main__':
    helpers.run_solution(solution)
