import dataclasses
import enum

from aoc import helpers


@dataclasses.dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, o: 'Direction'):
        match o:
            case Direction.UP:
                return Position(self.row - 1, self.col)
            case Direction.DOWN:
                return Position(self.row + 1, self.col)
            case Direction.RIGHT:
                return Position(self.row, self.col + 1)
            case Direction.LEFT:
                return Position(self.row, self.col - 1)


class Direction(enum.Enum):
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()

    def rotated_clockwise(self):
        return ROTATE_CLOCKWISE_MAP[self]


ROTATE_CLOCKWISE_MAP = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}


@dataclasses.dataclass(frozen=True)
class State:
    pos: Position
    direction: Direction


@dataclasses.dataclass(frozen=True)
class Input:
    max: Position
    start: State
    obstacles: set[Position]


def parse_input(lines: list[str]):
    start = None
    obstacles = set[Position]()
    pos = None
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            pos = Position(row=row, col=col)
            if c == '#':
                obstacles.add(pos)
            if c == 'v':
                start = State(pos, Direction.DOWN)
            if c == '>':
                start = State(pos, Direction.RIGHT)
            if c == '^':
                start = State(pos, Direction.UP)
            if c == '<':
                start = State(pos, Direction.LEFT)

    assert pos is not None
    assert start is not None
    return Input(max=pos, start=start, obstacles=obstacles)


def iterate(state: State, input: Input):
    next_pos = state.pos + state.direction
    if next_pos in input.obstacles:
        return State(pos=state.pos, direction=state.direction.rotated_clockwise())
    return State(pos=next_pos, direction=state.direction)


def is_pos_in_bounds(pos: Position, input: Input):
    return 0 <= pos.row <= input.max.row and 0 <= pos.col <= input.max.col


def gen_states(input: Input):
    state = input.start
    yield state
    while True:
        state = iterate(state, input)
        if not is_pos_in_bounds(state.pos, input):
            return
        yield state


def solution(lines: list[str]):
    return len(set(state.pos for state in gen_states(parse_input(lines))))


if __name__ == '__main__':
    helpers.run_solution(solution)
