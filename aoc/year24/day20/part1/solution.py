import dataclasses
import enum

from aoc import helpers
from aoc.lib import Delta, Grid, Pos, djikstra_gen


class Cell(enum.Enum):
    EMPTY = '.'
    WALL = '#'
    START = 'S'
    END = 'E'


@dataclasses.dataclass
class Input:
    grid: Grid[bool]
    start: Pos
    end: Pos


def parse_input(lines: list[str]):
    char_cell_map = {cell.value: cell for cell in Cell}
    grid = Grid[Cell].parse(lines, char_cell_map.__getitem__)
    start = grid.find(Cell.START)
    end = grid.find(Cell.END)
    assert start is not None
    assert end is not None
    return Input(grid=grid.map(lambda c: [c == Cell.WALL]), start=start, end=end)


def solve(input: Input, cost_threshold: int, max_cheat_size: int):
    deltas_of_norm_1 = list(Delta.of_norm(1))
    cheat_deltas = [list(Delta.of_norm(i)) for i in range(max_cheat_size + 1)]

    def transition(pos: Pos):
        return [
            (new_pos, 1)
            for delta in deltas_of_norm_1
            if input.grid.get(new_pos := pos + delta) is False
        ]

    start_cost_map_no_cheat = {
        path.nodes[-1]: path.cost for path in djikstra_gen(starts=[input.end], graph=transition)
    }

    end_cost_map_no_cheat = {
        (path.nodes[-1].row, path.nodes[-1].col): path.cost
        for path in djikstra_gen(starts=[input.start], graph=transition)
    }

    best_cost = start_cost_map_no_cheat[input.start]
    to_beat = best_cost - cost_threshold

    result = 0
    for cheat_start, cost_to_start in start_cost_map_no_cheat.items():
        if cost_to_start > to_beat:
            continue
        to_beat_minus_start = to_beat - cost_to_start
        for cheat_size in range(2, max_cheat_size + 1):
            if cheat_size > to_beat_minus_start:
                continue
            to_beat_minus_start_a_cheat = to_beat_minus_start - cheat_size

            for delta in cheat_deltas[cheat_size]:
                end_cost = end_cost_map_no_cheat.get(
                    (cheat_start.row + delta.drow, cheat_start.col + delta.dcol)
                )
                result += end_cost is not None and to_beat_minus_start_a_cheat >= end_cost

    return result


def solution(lines: list[str]):
    input = parse_input(lines)
    cost_threshold = 10 if len(lines) < 20 else 100
    return solve(input, cost_threshold, max_cheat_size=2)


if __name__ == '__main__':
    helpers.run_solution(solution)
