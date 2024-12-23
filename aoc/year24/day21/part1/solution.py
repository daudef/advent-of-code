import dataclasses
import functools
import itertools

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


CELLS = '0123456789<^v>A'


CELL_DELTA_MAP = {
    '<': Delta(drow=0, dcol=-1),
    '>': Delta(drow=0, dcol=1),
    '^': Delta(drow=-1, dcol=0),
    'v': Delta(drow=1, dcol=0),
}
DELTA_TO_CELL_MAP = {delta: cell for cell, delta in CELL_DELTA_MAP.items()}


@dataclasses.dataclass
class Keypad:
    grid: Grid[str]
    shortest_paths: dict[tuple[str, str], str]


def path_compare_key(path: str):
    return (
        len(path),
        sum(c1 != c2 for c1, c2 in itertools.pairwise(path)),
        len(path) > 0 and path[0] != '<',
        len(path) > 0 and path[0] != 'v',
        len(path) > 0 and path[0] != '^',
        len(path) > 0 and path[0] != '>',
    )


def transition(pos: Pos, grid: Grid[str]):
    for delta in Delta.of_norm(1):
        if grid.get(new_pos := pos + delta):
            yield new_pos, 1


def parse_keypad(s: str):
    keypad = Keypad(Grid([list(c.strip() for c in line) for line in s.splitlines()]), {})
    for start_pos, start_cell in keypad.grid.items():
        if start_cell:
            for path in djikstra_gen(
                [start_pos], lambda s: transition(s, keypad.grid), all_paths=True
            ):
                if end_cell := keypad.grid.get(path.nodes[-1]):
                    new_path = ''.join(
                        DELTA_TO_CELL_MAP[delta]
                        for (n1, n2) in itertools.pairwise(path.nodes)
                        if (delta := n2 - n1) != Delta(0, 0)
                    )
                    key = (start_cell, end_cell)
                    keypad.shortest_paths[key] = min(
                        new_path, keypad.shortest_paths.get(key, new_path), key=path_compare_key
                    )
    return keypad


def get_path_length_of_code(code: str, robot_count: int):
    door_keypad = parse_keypad(RAW_DOOR_KEYPAD)
    robot_keypad = parse_keypad(RAW_ROBOT_KEYPAD)

    @functools.cache
    def expend_pair_rec(pair: tuple[str, str], i: int) -> int:
        keypad = door_keypad if i == 0 else robot_keypad
        code = keypad.shortest_paths[pair] + 'A'
        if i == robot_count:
            return len(code)

        return sum(expend_pair_rec(new_pair, i + 1) for new_pair in itertools.pairwise('A' + code))

    return sum(expend_pair_rec(pair, 0) for pair in itertools.pairwise('A' + code))


def get_score_of_line(line: str, robot_count: int):
    path_length = get_path_length_of_code(line, robot_count)
    value = int(line[:-1])
    return path_length * value


def solution(lines: list[str]):
    return sum(get_score_of_line(line, robot_count=2) for line in lines)


if __name__ == '__main__':
    helpers.run_solution(solution)
