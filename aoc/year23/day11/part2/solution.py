import contextlib

from aoc import helpers
from aoc.year23.day11.part1 import solution as p1


def get_sorted_empty_rows(grid: list[list[bool]]):
    return [row_index for row_index, row in enumerate(grid) if not any(row)]


def get_sorted_empty_cols(grid: list[list[bool]]):
    return get_sorted_empty_rows(p1.transpose(grid))


def expend_positions_vert(
    positions: list[p1.Position], grid: list[list[bool]], expension_multiplier: int
):
    with contextlib.suppress(StopIteration):
        current_expension = 0
        sorted_positions_it = iter(sorted(positions, key=lambda p: p.row))
        current_position = next(sorted_positions_it)
        for row_index in [*get_sorted_empty_rows(grid), len(grid)]:
            while True:
                if current_position.row >= row_index:
                    break

                yield p1.Position(
                    row=current_position.row + current_expension, col=current_position.col
                )
                current_position = next(sorted_positions_it)

            current_expension += expension_multiplier - 1


def transpose_positions(positions: list[p1.Position]):
    return [p1.Position(row=p.col, col=p.row) for p in positions]


def expend_positions(
    positions: list[p1.Position], grid: list[list[bool]], expension_multiplier: int
):
    positions = list(expend_positions_vert(positions, grid, expension_multiplier))
    positions = transpose_positions(positions)
    grid = p1.transpose(grid)
    positions = list(expend_positions_vert(positions, grid, expension_multiplier))
    return transpose_positions(positions)


def solution(lines: list[str]):
    if len(lines) <= 10:
        expension_multiplier = 100
    else:
        expension_multiplier = 1000000

    grid = p1.parse(lines)
    positions = list(p1.gen_galaxy_positions(grid))
    positions = expend_positions(positions, grid, expension_multiplier)
    return p1.sum_of_distances(positions)


if __name__ == '__main__':
    helpers.run_solution(solution)
