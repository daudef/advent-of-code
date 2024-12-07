from aoc import helpers
from aoc.year24.day07.part1 import solution as p1

CONCAT_OPERATOR = p1.Operator(id='||', f=lambda a, b: int(f'{a}{b}'))


def solution(lines: list[str]):
    return sum(
        equation.value
        for equation in p1.parse_input(lines).equations
        if p1.get_equation_possible(
            equation,
            [p1.PLUS_OPERATOR, p1.MUL_OPERATOR, CONCAT_OPERATOR],
            operators_are_increasing=True,
        )
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
