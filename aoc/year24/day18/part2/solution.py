from aoc import helpers
from aoc.year24.day18.part1 import solution as p1


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    stop = p1.get_stop(input)

    left = 0
    right = len(input)
    while right - left > 1:
        mid = (left + right) // 2
        path = p1.find_path(input[:mid], stop)
        if path is None:
            right = mid
        else:
            left = mid

    print(input[left])
    return left


if __name__ == '__main__':
    helpers.run_solution(solution)
