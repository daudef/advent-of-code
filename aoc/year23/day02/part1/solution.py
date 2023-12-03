import dataclasses
from aoc import helpers


MAX_COLOR = {'red': 12, 'green': 13, 'blue': 14}


@dataclasses.dataclass
class Game:
    id: int
    reveals: list[dict[str, int]]


def parse_game(s: str):
    game_part, _, color_part = s.partition(':')
    return Game(
        id=int(game_part.lower().replace('game', '')),
        reveals=[
            {
                color.lower(): int(count)
                for color_count in reveal.split(',')
                for (count, color) in [color_count.split()]
            }
            for reveal in color_part.split(';')
        ],
    )


def game_is_valid(game: Game):
    for reveal in game.reveals:
        for color, count in reveal.items():
            if count > MAX_COLOR[color]:
                return False
    return True


def solution(input: list[str]):
    return sum(game.id for line in input if game_is_valid(game := parse_game(line)))


if __name__ == '__main__':
    helpers.run_solution(solution)
