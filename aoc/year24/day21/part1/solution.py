import dataclasses
import enum
import itertools
import typing

from aoc import helpers
from aoc.lib import Delta, Grid, Pos, djikstra_gen

RAW_DOOR_KEYPAD = """\
789
456
123
 0A"""

RAW_ROBOT_KEYPAD = """\
 ^A
<v>"""


class Cell(enum.Enum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    ACTIVATE = 'A'
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'


CHAR_CELL_MAP: typing.Mapping[str, Cell] = {cell.value: cell for cell in Cell}


CELL_DELTA_MAP = {
    Cell.LEFT: Delta(drow=0, dcol=-1),
    Cell.RIGHT: Delta(drow=0, dcol=1),
    Cell.UP: Delta(drow=-1, dcol=0),
    Cell.DOWN: Delta(drow=1, dcol=0),
}

DELTA_TO_CELL_MAP = {delta: cell for cell, delta in CELL_DELTA_MAP.items()}


@dataclasses.dataclass
class Keypad:
    grid: Grid[Cell | None]
    shortest_paths: dict[tuple[Cell, Cell], list[Cell]]


def path_compare_key(path: list[Cell]):
    return (
        len(path),
        sum(c1 != c2 for c1, c2 in itertools.pairwise(path)),
        len(path) > 0 and path[0] != Cell.LEFT,
        len(path) > 0 and path[0] != Cell.DOWN,
        len(path) > 0 and path[0] != Cell.UP,
        len(path) > 0 and path[0] != Cell.RIGHT,
    )


def parse_keypad(s: str):
    keypad = Keypad(Grid([[CHAR_CELL_MAP.get(c) for c in line] for line in s.splitlines()]), {})

    def graph(pos: Pos):
        for delta in Delta.of_norm(1):
            if keypad.grid.get(new_pos := pos + delta) is not None:
                yield new_pos, 1

    for start_pos, start_cell in keypad.grid.items():
        if start_cell is None:
            continue
        for path in djikstra_gen([start_pos], graph, all_paths=True):
            end_pos = path.nodes[-1]
            end_cell = keypad.grid.get(end_pos)
            if end_cell is None:
                continue

            new_path = [
                DELTA_TO_CELL_MAP[delta]
                for (n1, n2) in itertools.pairwise(path.nodes)
                if (delta := n2 - n1) != Delta(0, 0)
            ]
            previous_path = keypad.shortest_paths.get((start_cell, end_cell))

            if previous_path is None or path_compare_key(new_path) < path_compare_key(
                previous_path
            ):
                keypad.shortest_paths[(start_cell, end_cell)] = new_path

    return keypad


def expend_code(code: list[Cell], keypad: Keypad):
    return [
        cell
        for cell_pair in itertools.pairwise(itertools.chain([Cell.ACTIVATE], code))
        for cell in itertools.chain(keypad.shortest_paths[cell_pair], [Cell.ACTIVATE])
    ]


# @dataclasses.dataclass(frozen=True, slots=True)
# class State:
#     positions: tuple[Pos, ...]
#     code: tuple[Cell, ...]


# def transition(
#     state: State, keypads: tuple[Grid[Cell | None], ...], searched_code: tuple[Cell, ...]
# ):
#     for cell in [Cell.UP, Cell.RIGHT, Cell.DOWN, Cell.LEFT, Cell.ACTIVATE]:
#         for i, (pos, keypad) in reversed(
#             list(enumerate(zip(state.positions, keypads, strict=True)))
#         ):
#             delta = CELL_DELTA_MAP.get(cell)
#             if delta is not None:
#                 new_pos = pos + delta
#                 if keypad.get(new_pos) is not None:
#                     yield (
#                         State(
#                             (*state.positions[:i], new_pos, *state.positions[i + 1 :]), state.code
#                         ),
#                         1,
#                     )
#                 break

#             assert cell == Cell.ACTIVATE, cell
#             cell = keypad.get(pos)
#             assert cell is not None
#             if (
#                 i == 0
#                 and len(state.code) < len(searched_code)
#                 and searched_code[len(state.code)] == cell
#             ):
#                 yield State(state.positions, code=(*state.code, cell)), 1


def parse_code(s: str):
    return [CHAR_CELL_MAP[c] for c in s]


def get_path_of_code(code: list[Cell], robot_count: int):
    door_keypad = parse_keypad(RAW_DOOR_KEYPAD)
    robot_keypad = parse_keypad(RAW_ROBOT_KEYPAD)

    for keypad in [door_keypad, *(robot_keypad for _ in range(robot_count))]:
        code = [
            cell
            for cell_pair in itertools.pairwise(itertools.chain([Cell.ACTIVATE], code))
            for cell in itertools.chain(keypad.shortest_paths[cell_pair], [Cell.ACTIVATE])
        ]

    return code


def solution(lines: list[str]):
    return sum(
        (len(get_path_of_code(parse_code(line), robot_count=2))) * int(line[:-1]) for line in lines
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
