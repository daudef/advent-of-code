import dataclasses
from aoc import helpers


@dataclasses.dataclass(frozen=True)
class Num:
    start: int
    end: int


def nums_from_line(line: str):
    start = None
    for i, c in enumerate(line):
        if not c.isdigit():
            if start is not None:
                yield Num(start, i)
                start = None
        else:
            if start is None:
                start = i

    if start is not None:
        yield Num(start, len(line))


@dataclasses.dataclass(frozen=True)
class Pos:
    line: int
    column: int


@dataclasses.dataclass(frozen=True)
class LinedNum:
    line: int
    num: Num


type NumMap = dict[Pos, LinedNum]


def make_num_map(lines: list[str]):
    num_map: NumMap = {}
    for line_index, line in enumerate(lines):
        for num in nums_from_line(line):
            lined_num = LinedNum(line_index, num)
            for col_index in range(num.start, num.end):
                num_map[Pos(line_index, col_index)] = lined_num
    return num_map


def get_symbol_pos(lines: list[str]):
    for line_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if not char.isdigit() and char != '.':
                yield Pos(line_index, col_index)


def extend_pos(pos: Pos):
    for lined in (-1, 0, 1):
        for cold in (-1, 0, 1):
            yield Pos(line=pos.line + lined, column=pos.column + cold)


def eval_num(num: LinedNum, lines: list[str]):
    return int(lines[num.line][num.num.start : num.num.end])


def solution(input: list[str]):
    num_map = make_num_map(input)
    symbol_pos = list(get_symbol_pos(input))
    extended_symbol_pos = {ep for p in symbol_pos for ep in extend_pos(p)}
    covered_nums = {num for pos in extended_symbol_pos if (num := num_map.get(pos)) is not None}
    return sum(eval_num(num, input) for num in covered_nums)


if __name__ == '__main__':
    helpers.run_solution(solution)
