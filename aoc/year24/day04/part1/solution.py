import dataclasses

from aoc import helpers


@dataclasses.dataclass(frozen=True)
class PosDelta:
    drow: int
    dcol: int

    def __mul__(self, o: int):
        return PosDelta(drow=self.drow * o, dcol=self.dcol * o)


@dataclasses.dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def __add__(self, o: PosDelta):
        return Pos(row=self.row + o.drow, col=self.col + o.dcol)


@dataclasses.dataclass
class Grid:
    cells: list[str]
    row_count: int
    col_count: int

    def at(self, pos: Pos):
        if 0 <= pos.row < self.row_count and 0 <= pos.col < self.col_count:
            return self.cells[pos.row][pos.col]
        return None


def parse_grid(lines: list[str]):
    return Grid(cells=lines, row_count=len(lines), col_count=len(lines[0]))


def search_deltas_at_position(grid: Grid, word: str, pos: Pos):
    for drow in (-1, 0, 1):
        for dcol in (-1, 0, 1):
            if drow == 0 and dcol == 0:
                continue
            delta = PosDelta(drow=drow, dcol=dcol)

            if all(grid.at(pos + (delta * k)) == c for k, c in enumerate(word)):
                yield delta


def search_delta_pos(grid: Grid, word: str):
    for row in range(grid.row_count):
        for col in range(grid.col_count):
            pos = Pos(row=row, col=col)
            for delta in search_deltas_at_position(grid, word, pos):
                yield pos, delta


def solution(lines: list[str]):
    grid = parse_grid(lines)
    return sum(1 for _ in search_delta_pos(grid, word='XMAS'))


if __name__ == '__main__':
    helpers.run_solution(solution)
