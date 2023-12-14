import dataclasses
import functools
import math
import operator

from aoc import helpers


@dataclasses.dataclass
class Game:
    time: int
    distance: int


def parse_games(lines: list[str]):
    values = [
        [int(i) for i in line.partition(':')[-1].split()] for line in lines if len(line.strip()) > 0
    ]
    assert len(values) == 2
    for time, distance in zip(values[0], values[1], strict=True):
        yield Game(time=time, distance=distance)


def get_game_window(game: Game):
    if game.time**2 <= 4 * game.distance:
        return None
    half_time = game.time / 2
    delta = math.sqrt((half_time**2) - game.distance)
    return (math.floor(half_time - delta) + 1, math.ceil(half_time + delta) - 1)


def solution(input: list[str]):
    games = list(parse_games(input))
    return functools.reduce(
        operator.mul,
        [(w[1] - w[0] + 1 if (w := get_game_window(g)) is not None else 0) for g in games],
    )


if __name__ == '__main__':
    helpers.run_solution(solution)
