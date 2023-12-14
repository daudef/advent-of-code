import dataclasses
import enum
from aoc import helpers


class Cell(enum.Enum):
    OK = enum.auto()
    ERR = enum.auto()
    UNKNOWN = enum.auto()

    @property
    def symbol(self):
        match self:
            case Cell.OK:
                return '.'
            case Cell.ERR:
                return '#'
            case Cell.UNKNOWN:
                return '?'

    def __repr__(self):
        return self.symbol


CHAR_CELL_MAP = {c.symbol: c for c in Cell}


def parse_cells(cells: str):
    return [CHAR_CELL_MAP[c] for c in cells]


@dataclasses.dataclass
class Row:
    cells: list[Cell]
    group_sizes: list[int]

    @staticmethod
    def parse(line: str):
        cells, sizes = line.split()
        return Row(cells=parse_cells(cells), group_sizes=[int(n) for n in sizes.split(',')])


@dataclasses.dataclass
class ErrGroup:
    are_unknown: list[bool]
    unknown_count: int
    err_count: int


def parse_groups(row: Row):
    return [
        ErrGroup(
            are_unknown=(are_unknown := [Cell.UNKNOWN == c for c in parse_cells(group)]),
            unknown_count=sum(are_unknown),
            err_count=len(are_unknown) - sum(are_unknown),
        )
        for group in ''.join(c.symbol for c in row.cells).replace(Cell.OK.symbol, ' ').split()
    ]


def parse_rows(lines: list[str]):
    return [Row.parse(line) for line in lines]


def solution(input: list[str]):
    for row in parse_rows(input):
        print(row)
        for group in parse_groups(row):
            print(group)
        print()

    return 0


if __name__ == '__main__':
    helpers.run_solution(solution)
