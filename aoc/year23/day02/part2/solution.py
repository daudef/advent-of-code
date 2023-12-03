import functools

from aoc import helpers
from aoc.year23.day02.part1.solution import Game, parse_game

COLORS = ['red', 'blue', 'green']


def power_of_game(game: Game):
    max_of_colors: dict[str, int] = {}
    for reveal in game.reveals:
        for color, count in reveal.items():
            if count > max_of_colors.get(color, 0):
                max_of_colors[color] = count
    return functools.reduce(lambda a, b: a * b, [max_of_colors.get(c, 0) for c in COLORS], 1)


def solution(input: list[str]):
    return sum(power_of_game(parse_game(line)) for line in input)


if __name__ == '__main__':
    helpers.run_solution(solution)
