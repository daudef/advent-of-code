import dataclasses
import enum
import operator
from functools import reduce

from aoc import helpers


class Operator(enum.Enum):
    ADD = enum.auto()
    MUL = enum.auto()

    @staticmethod
    def parse(c: str) -> 'Operator':
        match c:
            case '+':
                return Operator.ADD
            case '*':
                return Operator.MUL
            case _:
                raise ValueError(f'invalid operator: {c}')


@dataclasses.dataclass(frozen=True, slots=True)
class Column:
    operator: Operator
    values: list[int]


def parse(lines: list[str]):
    values = [list(map(int, line.split())) for line in lines[:-1]]
    operators = [Operator.parse(c) for c in lines[-1].split()]
    return [
        Column(operator, [value_line[i] for value_line in values])
        for i, operator in enumerate(operators)
    ]


def compute(col: Column):
    match col.operator:
        case Operator.ADD:
            op = operator.add
        case Operator.MUL:
            op = operator.mul
    return reduce(op, col.values)


def solution(lines: list[str]):
    return sum(compute(col) for col in parse(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
