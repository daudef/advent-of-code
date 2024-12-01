import dataclasses

from aoc import helpers


@dataclasses.dataclass
class Input:
    l1: list[int]
    l2: list[int]


def parse_input(lines: list[str]):
    input = Input(l1=[], l2=[])
    for line in lines:
        v1, v2 = line.split()
        input.l1.append(int(v1))
        input.l2.append(int(v2))
    return input


def gen_differences(input: Input):
    for i1, i2 in zip(sorted(input.l1), sorted(input.l2), strict=True):
        yield abs(i1 - i2)


def solution(lines: list[str]):
    return sum(gen_differences(parse_input(lines)))


if __name__ == '__main__':
    helpers.run_solution(solution)
