import dataclasses
import enum
import functools

from aoc import helpers


class Direction(enum.Enum):
    UP = enum.auto()
    LEFT = enum.auto()
    DOWN = enum.auto()
    RIGHT = enum.auto()

    @functools.cached_property
    def inverse(self):
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT


@dataclasses.dataclass(frozen=True)
class Position:
    row: int
    col: int

    def apply_dir(self, dir: Direction):
        match dir:
            case Direction.UP:
                return Position(row=self.row - 1, col=self.col)
            case Direction.DOWN:
                return Position(row=self.row + 1, col=self.col)
            case Direction.LEFT:
                return Position(row=self.row, col=self.col - 1)
            case Direction.RIGHT:
                return Position(row=self.row, col=self.col + 1)


@dataclasses.dataclass
class Connector:
    dir1: Direction
    dir2: Direction

    def char(self):
        match (self.dir1, self.dir2):
            case (Direction.UP, Direction.RIGHT):
                return '╚'
            case (Direction.UP, Direction.DOWN):
                return '║'
            case (Direction.LEFT, Direction.RIGHT):
                return '═'
            case (Direction.LEFT, Direction.UP):
                return '╝'
            case (Direction.DOWN, Direction.LEFT):
                return '╗'
            case (Direction.RIGHT, Direction.DOWN):
                return '╔'
            case _:
                raise RuntimeError()

    def other_from(self, dir: Direction):
        if dir.inverse == self.dir1:
            return self.dir2
        if dir.inverse == self.dir2:
            return self.dir1
        return None


@dataclasses.dataclass
class Start:
    def char(self):
        return '╬'


@staticmethod
def parse_connector(s: str):
    match s:
        case '|':
            return Connector(Direction.UP, Direction.DOWN)
        case '-':
            return Connector(Direction.LEFT, Direction.RIGHT)
        case 'L':
            return Connector(Direction.UP, Direction.RIGHT)
        case 'J':
            return Connector(Direction.LEFT, Direction.UP)
        case '7':
            return Connector(Direction.DOWN, Direction.LEFT)
        case 'F':
            return Connector(Direction.RIGHT, Direction.DOWN)
        case '.':
            return None
        case 'S':
            return Start()
        case _:
            raise RuntimeError(f'unknown character: {s}')


@dataclasses.dataclass
class Input:
    grid: list[list[Connector | Start | None]]

    @staticmethod
    def parse(lines: list[str]):
        return Input(grid=[[parse_connector(c) for c in line] for line in lines])

    def start_pos(self):
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if isinstance(cell, Start):
                    return Position(row=row_index, col=col_index)
        raise RuntimeError('No start found')

    def cell_at(self, pos: Position):
        return self.grid[pos.row][pos.col]

    def display(self):
        for line in self.grid:
            print(''.join((' ' if c is None else c.char()) for c in line))


def get_path(input: Input):
    start_pos = input.start_pos()
    for dir in Direction:
        pos = start_pos.apply_dir(dir)
        path = [dir]
        while True:
            cell = input.cell_at(pos)
            if isinstance(cell, Start):
                return path
            if cell is None:
                break
            other_dir = cell.other_from(dir)
            if other_dir is None:
                break
            dir = other_dir
            pos = pos.apply_dir(dir)
            path.append(dir)


def solution(lines: list[str]):
    input = Input.parse(lines)
    path = get_path(input)
    assert path is not None
    return len(path) // 2


if __name__ == '__main__':
    helpers.run_solution(solution)
