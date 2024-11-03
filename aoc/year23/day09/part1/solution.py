import dataclasses
import itertools

from aoc import helpers


def predict_next_value(values: list[int], is_negative: bool = False) -> int:
    if all(value == 0 for value in values):
        return 0

    next_diff = predict_next_value(
        [v2 - v1 for v1, v2 in itertools.pairwise(values)], is_negative=is_negative
    )

    if is_negative:
        return values[0] - next_diff

    return values[-1] + next_diff


@dataclasses.dataclass
class Input:
    values_list: list[list[int]]

    @staticmethod
    def parse(lines: list[str]):
        return Input(values_list=[[int(val) for val in line.split()] for line in lines])


def solution(lines: list[str]):
    input = Input.parse(lines)
    return sum(predict_next_value(values) for values in input.values_list)


if __name__ == '__main__':
    helpers.run_solution(solution)
