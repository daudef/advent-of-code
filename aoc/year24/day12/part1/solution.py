import dataclasses
import typing

from aoc import helpers
from aoc.lib import Delta, Grid, Pos

Input: typing.TypeAlias = Grid[str]


def parse_input(lines: list[str]):
    return Grid[str].parse(lines, converter=str)


@dataclasses.dataclass
class Region:
    letter: str
    positions: list[Pos]


def gen_regions(input: Input):
    visited = set[Pos]()
    for pos, letter in input.items():
        if pos in visited:
            continue

        region = Region(letter, [])
        to_visit: list[Pos] = [pos]
        region_visited = set[Pos]()
        while len(to_visit) > 0:
            candidate = to_visit.pop()
            if candidate in visited or candidate in region_visited:
                continue
            region_visited.add(candidate)
            if input.get(candidate) == letter:
                region.positions.append(candidate)
                to_visit.extend(
                    candidate_neighbor
                    for delta in Delta.of_norm(1)
                    if (candidate_neighbor := candidate + delta) not in visited
                    and candidate_neighbor not in region_visited
                )

        yield region
        visited.update(region.positions)


Barrier: typing.TypeAlias = tuple[Pos, Pos]


def get_region_barriers(region: Region, input: Input):
    visited = set[Barrier]()
    for interior_pos in region.positions:
        for delta in Delta.of_norm(1):
            exterior_pos_candidate = interior_pos + delta
            barrier = (interior_pos, exterior_pos_candidate)
            if barrier in visited:
                continue
            visited.add(barrier)
            if input.get(exterior_pos_candidate) != region.letter:
                yield barrier


def solution(lines: list[str]):
    input = parse_input(lines)
    regions = list(gen_regions(input))

    return sum(
        len(region.positions) * len(list(get_region_barriers(region, input))) for region in regions
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
