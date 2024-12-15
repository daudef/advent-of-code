import collections
import dataclasses
import functools

from aoc import helpers
from aoc.lib import Delta, Pos


@dataclasses.dataclass
class Vehicle:
    pos: Pos
    speed: Delta


@dataclasses.dataclass
class Input:
    vehicles: list[Vehicle]
    max_pos: Pos


def parse_vehicle(line: str):
    # p=3,0 v=-2,-2
    pos_part, speed_part = line.split()
    pos_prefix = 'p='
    assert pos_part.startswith(pos_prefix)
    pos_part = pos_part.removeprefix(pos_prefix)
    col, row = pos_part.split(',')
    speed_prefix = 'v='
    assert speed_part.startswith(speed_prefix)
    speed_part = speed_part.removeprefix(speed_prefix)
    dcol, drow = speed_part.split(',')
    return Vehicle(pos=Pos(row=int(row), col=int(col)), speed=Delta(drow=int(drow), dcol=int(dcol)))


def parse_input(lines: list[str]):
    max_pos = Pos(col=101, row=103) if len(lines) > 20 else Pos(col=11, row=7)
    return Input(vehicles=[parse_vehicle(line) for line in lines], max_pos=max_pos)


def gen_vehicle_positions(vehicle: Vehicle, input: Input):
    pos = vehicle.pos
    while True:
        yield pos
        pos += vehicle.speed
        pos = pos.wrap(input.max_pos)


def get_quadrant_of_pos(pos: Pos, input: Input):
    mid = Pos(input.max_pos.row // 2, input.max_pos.col // 2)

    if pos.row < mid.row:
        quadrant = 0
    elif pos.row > mid.row:
        quadrant = 2
    else:
        return None

    if pos.col < mid.col:
        pass
    elif pos.col > mid.col:
        quadrant += 1
    else:
        return None

    return quadrant


def solution(lines: list[str]):
    input = parse_input(lines)
    quandrant_counts = collections.Counter[int | None]()

    for vehicle in input.vehicles:
        pos_iter = gen_vehicle_positions(vehicle, input)
        for _ in range(100):
            next(pos_iter)
        quandrant_counts.update([get_quadrant_of_pos(next(pos_iter), input)])

    return functools.reduce(
        lambda a, b: a * b, (c for (q, c) in quandrant_counts.items() if q is not None)
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
