from aoc import helpers
from aoc.year23.day12.part1 import solution as p1


def solution(lines: list[str]) -> int:
    rows = p1.parse_rows(lines)
    for row in rows:
        new_cells: list[p1.Cell] = []
        for _ in range(5):
            if len(new_cells) > 0:
                new_cells.append(None)
            new_cells.extend(row.cells)
        row.cells = new_cells
        row.group_sizes *= 5

    return p1.count_arrangements(rows)


if __name__ == '__main__':
    helpers.run_solution(solution)
