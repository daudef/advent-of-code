from aoc import helpers
from aoc.lib import Delta
from aoc.year24.day12.part1 import solution as p1


def group_barriers(barriers: set[p1.Barrier]):
    visited = set[p1.Barrier]()

    for barrier in sorted(barriers, key=lambda b: (b[0].row, b[0].col, b[1].row, b[1].col)):
        if barrier in visited:
            continue
        barrier_delta = barrier[1] - barrier[0]
        if abs(barrier_delta.drow) == 1 and barrier_delta.dcol == 0:
            search_delta = Delta(drow=0, dcol=1)
        else:
            assert abs(barrier_delta.dcol) == 1 and barrier_delta.drow == 0
            search_delta = Delta(drow=1, dcol=0)

        barrier_group = [barrier]
        while True:
            next_inside_pos = barrier_group[-1][0] + search_delta
            next_outside_pos = next_inside_pos + barrier_delta
            next_barrier = (next_inside_pos, next_outside_pos)
            if next_barrier not in barriers:
                break
            barrier_group.append(next_barrier)
        visited.update(barrier_group)
        yield barrier_group


def solution(lines: list[str]):
    input = p1.parse_input(lines)

    return sum(
        len(region.positions)
        * len(list(group_barriers(set(p1.get_region_barriers(region, input)))))
        for region in p1.gen_regions(input)
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
