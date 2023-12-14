import itertools
from aoc import helpers
from aoc.year23.day14.part1 import solution as sol1  # pyright: ignore[reportUnusedImport]


def turn_rocks(rocks: sol1.Rocks):
    new_rocks = [[sol1.Rock.EMPTY for _ in rocks] for _ in rocks[0]]
    for line_index, line in enumerate(rocks):
        for row_index, rock in enumerate(line):
            if rock != sol1.Rock.EMPTY:
                new_rocks[row_index][len(rocks) - 1 - line_index] = rock
    return new_rocks


def cycle(rocks: sol1.Rocks):
    for _ in range(4):
        sol1.move_rocks(rocks)
        rocks = turn_rocks(rocks)
    return rocks


def hash_rocks(rocks: sol1.Rocks):
    return hash(tuple(r for line in rocks for r in line))


def solution(input: list[str]):
    rocks = sol1.parse_input(input)

    hash_index_map: dict[int, int] = {}
    scores: list[int] = []

    for index in itertools.count():
        rocks = cycle(rocks)
        scores.append(sol1.score_rocks(rocks))

        rock_hash = hash_rocks(rocks)
        if (previous_index := hash_index_map.get(rock_hash)) is not None:
            break
        else:
            hash_index_map[rock_hash] = index
    else:
        raise RuntimeError()

    cycle_to_go = 1_000_000_000 - index
    period = index - previous_index
    offset_in_cycle = cycle_to_go % period

    return scores[previous_index + offset_in_cycle - 1]


if __name__ == '__main__':
    helpers.run_solution(solution)
