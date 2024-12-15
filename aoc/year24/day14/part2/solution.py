from aoc import helpers
from aoc.lib import Delta, Pos
from aoc.year24.day14.part1 import solution as p1


def solution(lines: list[str]):
    input = p1.parse_input(lines)

    pos_iters = [p1.gen_vehicle_positions(vehicle, input) for vehicle in input.vehicles]

    for time in range(1_000_000):
        pos_set = set(next(it) for it in pos_iters)
        if any(
            all(pos + d in pos_set for norm in range(1, 3) for d in Delta.of_norm(norm))
            for pos in pos_set
        ):
            break
    else:
        raise RuntimeError('not found')

    for i in range(input.max_pos.row):
        print(''.join('*' if Pos(i, j) in pos_set else ' ' for j in range(input.max_pos.col)))

    return time


if __name__ == '__main__':
    helpers.run_solution(solution)
