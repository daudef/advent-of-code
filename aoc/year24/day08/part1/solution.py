import collections
import dataclasses
import functools
import itertools

from aoc import helpers
from aoc.lib import Pos


@dataclasses.dataclass
class Input:
    freq_poses_map: dict[str, set[Pos]]
    stop: Pos


def parse_input(lines: list[str]):
    input = Input(collections.defaultdict(set), stop=Pos.parse_stop(lines))
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c != '.':
                input.freq_poses_map[c].add(Pos(row, col))
    return input


def get_resonant_poses(p1: Pos, p2: Pos, input: Input, *, min_dist: int, max_dist: int | None):
    delta = p1 - p2
    if delta.is_zero():
        return

    for start, direction in ((p1, 1), (p2, -1)):
        for i in itertools.count(min_dist):
            pos = start + direction * i * delta
            if pos.in_range(input.stop):
                yield pos
            else:
                break

            if max_dist is not None and i >= max_dist:
                break


def get_all_freq_resonant_poses(freq: str, input: Input, *, min_dist: int, max_dist: int | None):
    return {
        pos
        for p1, p2 in itertools.combinations(input.freq_poses_map[freq], 2)
        for pos in get_resonant_poses(p1, p2, input, min_dist=min_dist, max_dist=max_dist)
    }


def get_all_resonant_poses(input: Input, min_dist: int, max_dist: int | None):
    return functools.reduce(
        lambda a, b: a.union(b),
        [
            get_all_freq_resonant_poses(freq, input, min_dist=min_dist, max_dist=max_dist)
            for freq in input.freq_poses_map
        ],
    )


def solution(lines: list[str]):
    return len(get_all_resonant_poses(parse_input(lines), min_dist=1, max_dist=1))


if __name__ == '__main__':
    helpers.run_solution(solution)
