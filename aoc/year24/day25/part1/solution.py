import dataclasses
import typing

from aoc import helpers
from aoc.lib import Grid, Pos

Columns: typing.TypeAlias = tuple[int, ...]


@dataclasses.dataclass
class Input:
    locks: set[Columns]
    keys: set[Columns]


def parse_input(lines: list[str]):
    input = Input(set(), set())
    current: list[str] = []
    for line in [*lines, '']:
        if len(line) > 0:
            current.append(line)
        else:
            grid = Grid[bool].parse(current, lambda s: s == '#')
            heights: list[int] = []
            is_lock = False
            for col in range(grid.len.col):
                val = grid[Pos(0, col)]
                is_lock = val is True
                for row in range(1, grid.len.row):
                    if grid[Pos(row, col)] != val:
                        heights.append(row)
                        break
            if is_lock:
                input.locks.add(tuple(h - 1 for h in heights))
            else:
                input.keys.add(tuple(grid.len.row - h - 1 for h in heights))
            current = []
    return input


def key_lock_fit(key: Columns, lock: Columns):
    return all(h1 + h2 < 6 for h1, h2 in zip(key, lock, strict=True))


def solution(lines: list[str]):
    input = parse_input(lines)
    return sum(key_lock_fit(key, lock) for key in input.keys for lock in input.locks)


if __name__ == '__main__':
    helpers.run_solution(solution)
