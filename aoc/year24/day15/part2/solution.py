import dataclasses
import enum
import itertools

from aoc import helpers
from aoc.lib import Delta, Grid, Pos
from aoc.year24.day15.part1 import solution as p1


class Cell(enum.Enum):
    WALL = '#'
    BOX_L = '['
    BOX_R = ']'
    ROBOT = '@'
    EMPTY = '.'


@dataclasses.dataclass
class Input:
    grid: Grid[Cell]
    robot: Pos
    moves: list[Delta]


def convert_cell(p1_cell: p1.Cell | None) -> tuple[Cell, Cell]:
    match p1_cell:
        case None:
            return (Cell.EMPTY, Cell.EMPTY)
        case p1.Cell.WALL:
            return (Cell.WALL, Cell.WALL)
        case p1.Cell.BOX:
            return (Cell.BOX_L, Cell.BOX_R)
        case p1.Cell.ROBOT:
            return (Cell.ROBOT, Cell.EMPTY)


def parse_input(lines: list[str]):
    p1_input = p1.parse_input(lines)
    return Input(
        grid=Grid(
            [
                [cell for p1_cell in line for cell in convert_cell(p1_cell)]
                for line in p1_input.grid.values
            ]
        ),
        robot=Pos(row=p1_input.robot.row, col=p1_input.robot.col * 2),
        moves=p1_input.moves,
    )


def apply_horizontal_move(move: Delta, input: Input):
    assert move.drow == 0
    positions: list[Pos] = [input.robot]
    while True:
        pos = positions[-1] + move
        cell = input.grid[pos]
        if cell == Cell.WALL:
            return
        positions.append(pos)
        if cell == Cell.EMPTY:
            break

    for pos1, pos2 in itertools.pairwise(reversed(positions)):
        assert input.grid[pos1] is Cell.EMPTY
        input.grid[pos1] = input.grid[pos2]
        input.grid[pos2] = Cell.EMPTY

    input.robot = positions[1]


def _apply_vertical_move_rec(
    source: Pos, move: Delta, grid: Grid[Cell]
) -> list[tuple[Pos, Pos]] | None:
    dest = source + move
    cell = grid[dest]
    assert cell != Cell.ROBOT

    match grid[dest]:
        case Cell.WALL:
            return None
        case Cell.EMPTY:
            return [(source, dest)]
        case Cell.BOX_L:
            other_dest = dest + Delta(drow=0, dcol=1)
            assert grid[other_dest] == Cell.BOX_R, (other_dest, grid[other_dest])
        case Cell.BOX_R:
            other_dest = dest + Delta(drow=0, dcol=-1)
            assert grid[other_dest] == Cell.BOX_L, (other_dest, grid[other_dest])
        case Cell.ROBOT:
            raise RuntimeError(f'found robot at {source}')

    boxes_to_move_1 = _apply_vertical_move_rec(dest, move, grid)
    if boxes_to_move_1 is None:
        return None
    boxes_to_move_2 = _apply_vertical_move_rec(other_dest, move, grid)
    if boxes_to_move_2 is None:
        return None

    move_set_1 = set(boxes_to_move_1)

    return [
        *boxes_to_move_1,
        *(move for move in boxes_to_move_2 if move not in move_set_1),
        (source, dest),
    ]


def apply_vertical_move(move: Delta, input: Input):
    assert move.dcol == 0
    boxes_to_move = _apply_vertical_move_rec(input.robot, move, input.grid)
    if boxes_to_move is None:
        return

    for source, dest in boxes_to_move:
        assert input.grid[dest] is Cell.EMPTY
        input.grid[dest] = input.grid[source]
        input.grid[source] = Cell.EMPTY

        if input.grid[dest] == Cell.ROBOT:
            input.robot = dest

    return


def apply_move(move: Delta, input: Input):
    if move.dcol == 0:
        return apply_vertical_move(move, input)
    if move.drow == 0:
        return apply_horizontal_move(move, input)

    raise RuntimeError(f'Invalid move {move}')


def display(input: Input):
    for line in input.grid.values:
        print(''.join(cell.value for cell in line))


def get_score(input: Input):
    return sum(100 * pos.row + pos.col for pos, cell in input.grid.items() if cell == Cell.BOX_L)


def solution(lines: list[str]):
    input = parse_input(lines)
    # display(input)
    for move in input.moves:
        # print(f'\n{next(c for c, d in  p1.DELTA_CHAR_MAP.items() if d == move)}\n')
        apply_move(move, input)
        # display(input)
    return get_score(input)


if __name__ == '__main__':
    helpers.run_solution(solution)
