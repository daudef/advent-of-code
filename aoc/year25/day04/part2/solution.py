from aoc import helpers
from aoc.lib import Delta
from aoc.year25.day04.part1 import solution as p1


def solution(lines: list[str]):
    grid = p1.parse_lines(lines)
    to_check = set(pos for pos, is_paper in grid.items() if is_paper)
    count = 0
    while len(to_check) > 0:
        pos = to_check.pop()
        if p1.can_be_remove(pos, grid):
            count += 1
            grid[pos] = False
            to_check.update(pos + d for d in Delta.ring(1))
    return count


if __name__ == '__main__':
    helpers.run_solution(solution)
