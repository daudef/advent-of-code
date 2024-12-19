import typing

from aoc import helpers
from aoc.lib import Delta, Pos, djikstra

Input: typing.TypeAlias = list[Pos]


def parse_input(lines: list[str]):
    return [
        Pos(col=int(line.partition(',')[0]), row=int(line.partition(',')[-1])) for line in lines
    ]


def get_stop(input: Input):
    n = 71 if len(input) > 50 else 7
    return Pos(n, n)


def find_path(input: Input, stop: Pos):
    wall_set = set(input)

    def transition(pos: Pos):
        for delta in Delta.of_norm(1):
            neighbor = pos + delta
            if neighbor.in_range(stop) and neighbor not in wall_set:
                yield neighbor, 1

    return djikstra([Pos(0, 0)], [stop - Delta(1, 1)], transition)


def solution(lines: list[str]):
    input = parse_input(lines)[:1024]
    stop = get_stop(input)
    path = find_path(input, stop)
    assert path is not None
    return path.cost


if __name__ == '__main__':
    helpers.run_solution(solution)
