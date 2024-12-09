import collections

from aoc import helpers
from aoc.year24.day09.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def move_blocks(input: p1.Input):
    block_ids = input.block_ids[:]

    len_start_map = collections.defaultdict[int, int](int)

    for r in reversed(input.block_ranges):
        n = len(r)
        start = len_start_map[n]
        limit = len(block_ids) - n + 1

        while start < limit and any(b is not None for b in block_ids[start : start + n]):
            start += 1

        len_start_map[n] = start

        if start >= r.start:
            continue

        block_ids[start : start + n] = block_ids[r.start : r.stop]
        block_ids[r.start : r.stop] = [None for _ in range(n)]

    return block_ids


def solution(lines: list[str]):
    return p1.compute_checksum(move_blocks(p1.parse_block_ids(lines[0])))


if __name__ == '__main__':
    helpers.run_solution(solution)
