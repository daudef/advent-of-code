import collections
import dataclasses

from aoc import helpers
from aoc.year24.day01.part1 import solution as p1


@dataclasses.dataclass
class Counts:
    c1: collections.Counter[int]
    c2: collections.Counter[int]


def compute_counts(input: p1.Input):
    return Counts(c1=collections.Counter(input.l1), c2=collections.Counter(input.l2))


def gen_similarities(counts: Counts):
    for i, count1 in counts.c1.items():
        count2 = counts.c2.get(i, 0)
        yield i * count1 * count2


def solution(lines: list[str]):
    return sum(gen_similarities(compute_counts(p1.parse_input(lines))))


if __name__ == '__main__':
    helpers.run_solution(solution)
