import collections
import dataclasses

from aoc import helpers
from aoc.lib import Delta, Grid, Pos


@dataclasses.dataclass
class Input:
    grid: Grid[int]
    up_neighbors: dict[Pos, set[Pos]]
    down_neighbors: dict[Pos, set[Pos]]


def parse_input(lines: list[str]):
    input = Input(
        Grid[int].parse(lines, int), collections.defaultdict(set), collections.defaultdict(set)
    )
    for pos, value in input.grid.items():
        for delta in Delta.of_norm(1):
            neighbor_pos = pos + delta
            if input.grid.get(neighbor_pos) == value + 1:
                input.up_neighbors[pos].add(neighbor_pos)
            if input.grid.get(neighbor_pos) == value - 1:
                input.down_neighbors[pos].add(neighbor_pos)
    return input


def compute_reachable_tops(input: Input):
    reachable_tops: dict[Pos, set[Pos]] = collections.defaultdict(set)
    for top_pos, value in input.grid.items():
        if value != 9:
            continue

        def explore_rec(pos: Pos):
            reachable_tops[pos].add(top_pos)
            for down_pos in input.down_neighbors[pos]:
                explore_rec(down_pos)

        explore_rec(top_pos)
    return reachable_tops


def get_score(reachable_tops: dict[Pos, set[Pos]], input: Input):
    return sum(len(reachable_tops[pos]) for pos, value in input.grid.items() if value == 0)


def solution(lines: list[str]):
    input = parse_input(lines)
    return get_score(compute_reachable_tops(input), input)


if __name__ == '__main__':
    helpers.run_solution(solution)
