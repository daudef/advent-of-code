import typing
from aoc import helpers
from aoc.year23.day06.part1 import solution as sol1


def merge_ints(ints: typing.Iterable[int]):
    return int(''.join(str(i) for i in ints))


def merge_games(games: list[sol1.Game]):
    return sol1.Game(
        time=merge_ints(g.time for g in games), distance=merge_ints(g.distance for g in games)
    )


def solution(input: list[str]):
    games = list(sol1.parse_games(input))
    game = merge_games(games)
    window = sol1.get_game_window(game)
    if window is None:
        return 0
    return window[1] - window[0] + 1


if __name__ == '__main__':
    helpers.run_solution(solution)
