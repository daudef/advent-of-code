import enum
from aoc import helpers


class Rock(enum.Enum):
    ROUND = enum.auto()
    SQUARE = enum.auto()
    EMPTY = enum.auto()

    @property
    def symbol(self):
        match self:
            case Rock.ROUND:
                return 'O'
            case Rock.SQUARE:
                return '#'
            case Rock.EMPTY:
                return '.'


SYMBOL_CELL_MAP = {r.symbol: r for r in Rock}


def parse_line(line: str):
    return [SYMBOL_CELL_MAP[c] for c in line]


def parse_input(input: list[str]):
    return [parse_line(line) for line in input]


type Rocks = list[list[Rock]]


def move_rocks(rocks: Rocks):
    min_positions = [0 for _ in rocks[0]]
    for line_index, rock_line in enumerate(rocks):
        for row, rock in enumerate(rock_line):
            match rock:
                case Rock.EMPTY:
                    pass
                case Rock.ROUND:
                    rock_line[row] = Rock.EMPTY
                    rocks[min_positions[row]][row] = rock
                    min_positions[row] += 1
                case Rock.SQUARE:
                    min_positions[row] = line_index + 1


def display_rocks(rocks: Rocks):
    for line in rocks:
        print(''.join(r.symbol for r in line))
    print()


def score_rocks(rocks: Rocks):
    return sum(
        sum(r == Rock.ROUND for r in line) * (len(rocks) - i) for i, line in enumerate(rocks)
    )


def solution(input: list[str]):
    rocks = parse_input(input)
    move_rocks(rocks)
    return score_rocks(rocks)


if __name__ == '__main__':
    helpers.run_solution(solution)
