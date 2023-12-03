import typing
import contextlib


from aoc import helpers


def get_first_digit_of_line(line: typing.Iterable[str]):
    for c in line:
        with contextlib.suppress(ValueError):
            return int(c)
    raise RuntimeError()


def solution(input: list[str]):
    return sum(
        10 * get_first_digit_of_line(line) + get_first_digit_of_line(reversed(line))
        for line in input
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
