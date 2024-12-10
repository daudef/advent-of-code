import collections

from aoc import helpers
from aoc.lib import Pos
from aoc.year24.day10.part1 import solution as p1


def compute_trail_counts(input: p1.Input):
    trail_counts: dict[Pos, int] = collections.defaultdict(int)
    for top_pos, value in input.grid.items():
        if value != 9:
            continue

        def explore_rec(pos: Pos):
            trail_counts[pos] += 1
            for down_pos in input.down_neighbors[pos]:
                explore_rec(down_pos)

        explore_rec(top_pos)
    return trail_counts


def get_score(reachable_tops: dict[Pos, int], input: p1.Input):
    return sum(reachable_tops[pos] for pos, value in input.grid.items() if value == 0)


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    return get_score(compute_trail_counts(input), input)


if __name__ == '__main__':
    helpers.run_solution(solution)
