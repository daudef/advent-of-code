from aoc import helpers
from aoc.year24.day04.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def solution(lines: list[str]):
    grid = p1.parse_grid(lines)
    pos_deltas = set(p1.search_delta_pos(grid, 'MAS'))

    return sum(
        1
        for pos, delta in pos_deltas
        if (
            delta == p1.PosDelta(-1, -1)
            and (
                (pos + p1.PosDelta(0, -2), p1.PosDelta(-1, 1)) in pos_deltas
                or (pos + p1.PosDelta(-2, 0), p1.PosDelta(1, -1)) in pos_deltas
            )
        )
        or (
            delta == p1.PosDelta(1, 1)
            and (
                (pos + p1.PosDelta(0, 2), p1.PosDelta(1, -1)) in pos_deltas
                or (pos + p1.PosDelta(2, 0), p1.PosDelta(-1, 1)) in pos_deltas
            )
        )
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
