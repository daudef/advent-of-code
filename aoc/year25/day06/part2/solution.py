from aoc import helpers
from aoc.year25.day06.part1 import solution as p1


def parse(lines: list[str]):
    columns: list[p1.Column] = []
    values: list[int] = []
    for i in range(len(lines[0]) - 1, -1, -1):
        value_s = ''.join(line[i] for line in lines[:-1]).strip()
        operator_s = lines[-1][i].strip()
        if value_s == '':
            continue
        values.append(int(value_s))
        if operator_s != '':
            columns.append(p1.Column(p1.Operator.parse(operator_s), values))
            values = []
    return columns


def solution(lines: list[str]):
    return sum(p1.compute(col) for col in parse(lines))


if __name__ == '__main__':
    helpers.run_solution(solution)
