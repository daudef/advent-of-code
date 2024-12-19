import dataclasses
import enum

from aoc import helpers
from aoc.lib import Delta, Grid, Pos, djikstra


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


@dataclasses.dataclass(frozen=True)
class State:
    pos: Pos
    dir: Delta


CLOCKWISE_DELTA_MAP = {
    Delta(0, 1): Delta(1, 0),
    Delta(1, 0): Delta(0, -1),
    Delta(0, -1): Delta(-1, 0),
    Delta(-1, 0): Delta(0, 1),
}

ANTI_CLOCKWISE_DELTA_MAP = {v: k for k, v in CLOCKWISE_DELTA_MAP.items()}


def transition(state: State, input: Input):
    forward = state.pos + state.dir
    wall_forward = input.grid[forward]
    if not wall_forward:
        yield (State(forward, state.dir), 1)

    for dir_map in [CLOCKWISE_DELTA_MAP, ANTI_CLOCKWISE_DELTA_MAP]:
        yield (State(state.pos, dir=dir_map[state.dir]), 1000)


def get_best_path(input: Input):
    return djikstra(
        starts=[State(input.start, Delta(0, 1))],
        ends=[State(input.end, dir) for dir in Delta.of_norm(1)],
        graph=lambda s: transition(s, input),
    )


def solution(lines: list[str]):
    input = parse_input(lines)
    path = get_best_path(input)
    assert path is not None
    return path.cost


if __name__ == '__main__':
    helpers.run_solution(solution)
