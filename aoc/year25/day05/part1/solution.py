import dataclasses

from aoc import helpers


@dataclasses.dataclass(frozen=True, slots=True)
class Input:
    ranges: list[range]
    ids: list[int]


def parse(lines: list[str]) -> Input:
    ranges: list[range] = []
    line_it = iter(lines)
    while line := next(line_it):
        start, _, end = line.partition('-')
        ranges.append(range(int(start), int(end) + 1))

    ids = list(map(int, line_it))
    return Input(ranges, ids)


def solution(lines: list[str]):
    input = parse(lines)
    return sum(any(id in range for range in input.ranges) for id in input.ids)


if __name__ == '__main__':
    helpers.run_solution(solution)
