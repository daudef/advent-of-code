import contextlib
from aoc import helpers


def rev_str(s: str):
    return ''.join(reversed(s))


NAMED_DIGITS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def get_first_digit_of_line(line: str, named_digits: dict[str, int]):
    for i, c in enumerate(line):
        with contextlib.suppress(ValueError):
            return int(c)

        for name, value in named_digits.items():
            if line[i : i + len(name)] == name:
                return value

    raise RuntimeError()


def solution(input: list[str]):
    rev_named_digits = {rev_str(k): v for k, v in NAMED_DIGITS.items()}

    return sum(
        10 * get_first_digit_of_line(line, NAMED_DIGITS)
        + get_first_digit_of_line(rev_str(line), rev_named_digits)
        for line in input
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
