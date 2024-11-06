import dataclasses

from aoc import helpers


def parse_char(c: str):
    if c == '.':
        return False
    if c == '#':
        return True
    raise RuntimeError(f'invalid char {c}')


def parse(lines: list[str]):
    return [[parse_char(c) for c in line] for line in lines]


def expand_vert(grid: list[list[bool]]):
    new_grid: list[list[bool]] = []
    for row in grid:
        if not any(row):
            new_grid.append(row.copy())
        new_grid.append(row)
    return new_grid


def transpose(grid: list[list[bool]]):
    new_grid: list[list[bool]] = []
    if len(grid) > 0:
        for j in range(len(grid[0])):
            new_grid.append([grid[i][j] for i in range(len(grid))])
    return new_grid


def expand(grid: list[list[bool]]):
    grid = expand_vert(grid)
    grid = transpose(grid)
    grid = expand_vert(grid)
    return transpose(grid)


@dataclasses.dataclass(frozen=True)
class Position:
    row: int
    col: int


def gen_galaxy_positions(grid: list[list[bool]]):
    for row_index, row in enumerate(grid):
        for col_index, c in enumerate(row):
            if c:
                yield Position(row_index, col_index)


def distance_between_pos(p1: Position, p2: Position):
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)


def display_grid(grid: list[list[bool]]):
    for row in grid:
        print(''.join('#' if c else '.' for c in row))


def sum_of_distances(positions: list[Position]):
    return round(sum(distance_between_pos(p1, p2) for p1 in positions for p2 in positions) / 2)


def solution(lines: list[str]):
    grid = expand(parse(lines))
    positions = list(gen_galaxy_positions(grid))
    return sum_of_distances(positions)


if __name__ == '__main__':
    helpers.run_solution(solution)
