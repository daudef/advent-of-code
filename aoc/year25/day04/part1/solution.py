from aoc import helpers
from aoc.lib import Delta, Grid, Pos


def parse_lines(lines: list[str]) -> Grid[bool]:
    return Grid[bool].parse(lines, converter=lambda c: c == '@')


def can_be_remove(pos: Pos, grid: Grid[bool]) -> bool:
    return (grid.get(pos) or False) and sum(
        (grid.get(pos + delta) or False) for delta in Delta.ring(1)
    ) < 4


def solution(lines: list[str]):
    grid = parse_lines(lines)
    return sum(can_be_remove(pos, grid) for (pos, _) in grid.items())


if __name__ == '__main__':
    helpers.run_solution(solution)
