from aoc import helpers
from aoc.year25.day02.part1 import solution as p1  # pyright: ignore[reportUnusedImport]


def get_invalid_ids_in_range(r: range):
    return {
        i
        for i in r
        for pattern_count in range(2, (len(str(i))) + 1)
        if p1.is_invalid_id(i, pattern_count)
    }


def solution(lines: list[str]):
    return sum(sum(get_invalid_ids_in_range(r)) for r in p1.parse_lines(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
