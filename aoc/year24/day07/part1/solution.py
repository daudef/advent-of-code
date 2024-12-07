import dataclasses
import operator
import typing

from aoc import helpers


@dataclasses.dataclass
class Equation:
    value: int
    operands: list[int]


def parse_equation(s: str):
    raw_value, raw_operands = s.split(':')
    return Equation(value=int(raw_value), operands=list(map(int, raw_operands.split())))


@dataclasses.dataclass
class Operator:
    id: str
    f: typing.Callable[[int, int], int]


@dataclasses.dataclass
class Combination:
    operator_ids: list[str]
    value: int


def gen_possible_values(
    operands: list[int],
    operators: list[Operator],
    operator_ids: list[str],
    *,
    stop_if_above: int | None,
) -> typing.Iterator[Combination]:
    if stop_if_above is not None and operands[0] > stop_if_above:
        return

    if len(operands) == 1:
        yield Combination(operator_ids=operator_ids, value=operands[0])
        return

    a, b, *other = operands
    for op in operators:
        yield from gen_possible_values(
            [op.f(a, b), *other], operators, [op.id, *(operator_ids)], stop_if_above=stop_if_above
        )


def get_equation_possible(
    equation: Equation, operators: list[Operator], *, operators_are_increasing: bool
):
    return any(
        combination.value == equation.value
        for combination in gen_possible_values(
            equation.operands,
            operators,
            [],
            stop_if_above=equation.value if operators_are_increasing else None,
        )
    )


@dataclasses.dataclass
class Input:
    equations: list[Equation]


def parse_input(lines: list[str]):
    return Input(equations=[parse_equation(line) for line in lines])


PLUS_OPERATOR = Operator(id='+', f=operator.add)
MUL_OPERATOR = Operator(id='*', f=operator.mul)


def solution(lines: list[str]):
    return sum(
        equation.value
        for equation in parse_input(lines).equations
        if get_equation_possible(
            equation, [PLUS_OPERATOR, MUL_OPERATOR], operators_are_increasing=True
        )
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
