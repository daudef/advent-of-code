from aoc import helpers
from aoc.year23.day09.part1 import solution as p1


def solution(lines: list[str]):
    input = p1.Input.parse(lines)
    return sum(p1.predict_next_value(values, is_negative=True) for values in input.values_list)


if __name__ == '__main__':
    helpers.run_solution(solution)
