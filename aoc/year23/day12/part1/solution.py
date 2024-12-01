import dataclasses
import typing

from aoc import helpers

Cell: typing.TypeAlias = bool | None

CHAR_CELL_MAP: dict[str, Cell] = {'?': None, '.': False, '#': True}


def parse_cells(cells: str):
    return [CHAR_CELL_MAP[c] for c in cells]


@dataclasses.dataclass
class Row:
    cells: list[Cell]
    group_sizes: list[int]

    @staticmethod
    def parse(line: str):
        cells, sizes = line.split()
        return Row(cells=parse_cells(cells), group_sizes=[int(n) for n in sizes.split(',')])


def parse_rows(lines: list[str]):
    return [Row.parse(line) for line in lines]


BacktrackCache: typing.TypeAlias = dict[tuple[int, int], int]


def backtrack(index: int, group_index: int, row: Row, cache: BacktrackCache) -> int:
    cache_key = (index, group_index)
    if (result := cache.get(cache_key)) is not None:
        return result

    if group_index == len(row.group_sizes):
        return 1

    group_size = row.group_sizes[group_index]

    if index + group_size > len(row.cells):
        return 0

    total = 0

    if row.cells[index] is not True:
        total += backtrack(index + 1, group_index, row, cache)

    if all(row.cells[index + i] is not False for i in range(group_size)) and (
        index + group_size == len(row.cells) or row.cells[index + group_size] is not True
    ):
        total += backtrack(index + group_size + 1, group_index + 1, row, cache)

    if cache_key not in cache:
        cache[cache_key] = total

    return total


def count_arrangements(rows: list[Row]):
    res = sum(backtrack(0, 0, row, {}) for row in rows)
    return res


def solution(lines: list[str]) -> int:
    return count_arrangements(parse_rows(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
