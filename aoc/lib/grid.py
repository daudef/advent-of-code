import dataclasses
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class Delta:
    drow: int
    dcol: int

    def __mul__(self, o: int):
        return Delta(drow=self.drow * o, dcol=self.dcol * o)

    def __rmul__(self, o: int):
        return Delta(drow=self.drow * o, dcol=self.dcol * o)

    def __neg__(self):
        return Delta(drow=-self.drow, dcol=-self.dcol)

    def __add__(self, o: 'Delta'):
        return Delta(drow=self.drow + o.drow, dcol=self.dcol + o.dcol)

    def __sub__(self, o: 'Delta'):
        return Delta(drow=self.drow - o.drow, dcol=self.dcol - o.dcol)

    def is_zero(self):
        return self.drow == 0 and self.dcol == 0

    @staticmethod
    def of_norm(n: int):
        for drow in range(-n, n + 1):
            for dcol in (n - abs(drow), abs(drow) - n) if (abs(drow) != n) else (0,):
                yield Delta(drow, dcol)


@dataclasses.dataclass(frozen=True, slots=True)
class Pos:
    row: int
    col: int

    def __add__(self, o: Delta):
        return Pos(row=self.row + o.drow, col=self.col + o.dcol)

    @typing.overload
    def __sub__(self, o: 'Pos') -> Delta:
        ...

    @typing.overload
    def __sub__(self, o: 'Delta') -> 'Pos':
        ...

    def __sub__(self, o: 'Pos | Delta'):
        if isinstance(o, Delta):
            return Pos(row=self.row - o.drow, col=self.col - o.dcol)
        return Delta(drow=self.row - o.row, dcol=self.col - o.col)

    def in_range(self, stop: 'Pos', *, start: 'Pos | None' = None):
        if self.row >= stop.row or self.col >= stop.col:
            return False
        if start is not None:
            return self.row >= start.row and self.col >= start.col
        return self.row >= 0 and self.col >= 0

    @staticmethod
    def parse_stop(lines: list[str]):
        row = len(lines)
        assert row > 0
        col = len(lines[0])
        assert all(col == len(line) for line in lines)
        return Pos(row=row, col=col)


@dataclasses.dataclass
class Grid[T]:
    values: list[list[T]]
    len: Pos

    def items(self):
        for row, line in enumerate(self.values):
            for col, value in enumerate(line):
                yield Pos(row, col), value

    @staticmethod
    def parse(lines: list[str], converter: typing.Callable[[str], T]):
        return Grid(
            values=[[converter(c) for c in line] for line in lines], len=Pos.parse_stop(lines)
        )

    def __getitem__(self, pos: Pos):
        return self.values[pos.row][pos.col]

    def get(self, pos: Pos):
        if pos.in_range(self.len):
            return self[pos]
        return None
