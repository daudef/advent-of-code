import itertools

from aoc import helpers
from aoc.year25.day05.part1 import solution as p1


def range_union(r1: range, r2: range) -> range | None:
    if max(r1.start, r2.start) <= min(r1.stop, r2.stop):
        return range(min(r1.start, r2.start), max(r1.stop, r2.stop))
    return None


def solution(lines: list[str]):
    ranges: list[range] = p1.parse(lines).ranges
    while True:
        for (i1, r1), (i2, r2) in itertools.product(enumerate(ranges), enumerate(ranges)):
            if i1 < i2 and (union := range_union(r1, r2)) is not None:
                ranges = [*ranges[:i1], *ranges[i1 + 1 : i2], *ranges[i2 + 1 :], union]
                break
        else:
            break

    return sum(len(r) for r in ranges)


if __name__ == '__main__':
    helpers.run_solution(solution)
