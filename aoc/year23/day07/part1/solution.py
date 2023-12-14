import collections
import dataclasses
import enum
import typing
from aoc import helpers


class HandType(enum.IntEnum):
    FIVE = 6
    FOUR = 5
    FULL_HOUSE = 4
    THREE = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH = 0


@dataclasses.dataclass(frozen=True)
class Game:
    hand: tuple[int, ...]
    bid: int
    type: HandType

    def __gt__(self, other: 'Game'):
        if self.type != other.type:
            return self.type > other.type
        if self.hand != other.hand:
            return self.hand > other.hand
        return self.bid > other.bid


type Typer = typing.Callable[[tuple[int, ...]], HandType]


def parse_game(line: str, card_order: str, typer: Typer):
    card_values = {c: i for (i, c) in enumerate(card_order)}
    parts = line.split()
    assert len(parts) == 2
    hand = tuple(card_values[c] for c in parts[0])
    return Game(hand=hand, bid=int(parts[1]), type=typer(hand))


def get_sorted_card_counts(hand: typing.Sequence[int]):
    return sorted(collections.Counter(hand).values(), reverse=True)


def convert_sorted_card_counts_to_hand_type(sorted_card_counts: list[int]):
    assert sum(sorted_card_counts) == 5
    assert len(sorted_card_counts) <= 5
    if sorted_card_counts == [5]:
        return HandType.FIVE
    if sorted_card_counts == [4, 1]:
        return HandType.FOUR
    if sorted_card_counts == [3, 2]:
        return HandType.FULL_HOUSE
    if sorted_card_counts == [3, 1, 1]:
        return HandType.THREE
    if sorted_card_counts == [2, 2, 1]:
        return HandType.TWO_PAIR
    if sorted_card_counts == [2, 1, 1, 1]:
        return HandType.PAIR
    if sorted_card_counts == [1, 1, 1, 1, 1]:
        return HandType.HIGH
    raise AssertionError


def get_type_of_hand(hand: tuple[int, ...]):
    return convert_sorted_card_counts_to_hand_type(get_sorted_card_counts(hand))


def parse_games(lines: list[str], card_order: str, typer: Typer):
    return [parse_game(line, card_order, typer) for line in lines]


def solution(input: list[str]):
    games = sorted(parse_games(input, '23456789TJQKA', get_type_of_hand))
    return sum((i + 1) * g.bid for i, g in enumerate(games))


if __name__ == '__main__':
    helpers.run_solution(solution)
