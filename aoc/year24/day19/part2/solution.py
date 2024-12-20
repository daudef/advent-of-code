from aoc import helpers
from aoc.year24.day19.part1 import solution as p1


def solution(lines: list[str]):
    input = p1.parse_input(lines)
    prefix_map = p1.make_prefix_map(input)
    cache = dict[str, int]()
    return sum(p1.try_make_word(word, prefix_map, cache) for word in input.targets)


if __name__ == '__main__':
    helpers.run_solution(solution)
