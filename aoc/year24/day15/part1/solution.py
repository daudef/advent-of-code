import dataclasses
import enum
import itertools

from aoc import helpers
from aoc.lib import Delta, Grid, Pos


class Cell(enum.Enum):
    WALL = '#'
    BOX = 'O'

    ROBOT = '@'


DELTA_CHAR_MAP = {
    '<': Delta(drow=0, dcol=-1),
    '>': Delta(drow=0, dcol=1),
    'v': Delta(drow=1, dcol=0),
    '^': Delta(drow=-1, dcol=0),
}


@dataclasses.dataclass
class Input:
    grid: Grid[Cell | None]
    robot: Pos
    moves: list[Delta]


def parse_input(lines: list[str]):
    grid_lines: list[str] = []
    moves_lines: list[str] = []
    reached_empty_line = False
    for line in lines:
        if line == '':
            reached_empty_line = True
        elif reached_empty_line:
            moves_lines.append(line)
        else:
            grid_lines.append(line)

    cell_char_map = {c.value: c for c in Cell}
    grid = Grid[Cell | None].parse(grid_lines, converter=lambda c: cell_char_map.get(c))
    robot = next(pos for pos, cell in grid.items() if cell == Cell.ROBOT)
    moves = [DELTA_CHAR_MAP[c] for line in moves_lines for c in line]

    return Input(grid, robot, moves)


def display(input: Input):
    for line in input.grid.values:
        print(''.join(cell.value if cell is not None else '.' for cell in line))


def apply_move(move: Delta, input: Input):
    positions: list[Pos] = [input.robot]
    while True:
        pos = positions[-1] + move
        cell = input.grid.get(pos)
        if cell == Cell.WALL:
            return
        positions.append(pos)
        if cell is None:
            break

    for p1, p2 in itertools.pairwise(reversed(positions)):
        assert input.grid[p1] is None
        input.grid[p1] = input.grid[p2]
        input.grid[p2] = None

    input.robot = positions[1]


def get_score(input: Input):
    return sum(100 * pos.row + pos.col for pos, cell in input.grid.items() if cell == Cell.BOX)


def solution(lines: list[str]):
    input = parse_input(lines)
    display(input)
    for move in input.moves:
        apply_move(move, input)
        # print(f'\n{next(c for c, d in  DELTA_CHAR_MAP.items() if d == move)}\n')
        # display(input)
    return get_score(input)


if __name__ == '__main__':
    helpers.run_solution(solution)
