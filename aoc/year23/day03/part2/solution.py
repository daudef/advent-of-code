import functools
import operator
from aoc import helpers
from aoc.year23.day03.part1.solution import Pos, NumMap, make_num_map, extend_pos, eval_num


def get_star_pos(lines: list[str]):
    for line_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == '*':
                yield Pos(line_index, col_index)


def get_pos_ajacents_nums(pos: Pos, num_map: NumMap):
    return {num for ep in extend_pos(pos) if (num := num_map.get(ep)) is not None}


def solution(input: list[str]):
    num_map = make_num_map(input)
    star_pos = list(get_star_pos(input))

    return sum(
        functools.reduce(operator.mul, [eval_num(n, input) for n in nums], 1)
        for sp in star_pos
        if len(nums := get_pos_ajacents_nums(sp, num_map)) == 2
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
