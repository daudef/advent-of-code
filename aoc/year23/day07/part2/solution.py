from aoc import helpers
from aoc.year23.day07.part1 import solution as sol1


def get_type_of_hand(hand: tuple[int, ...]):
    hand_without_jokers = [c for c in hand if c != 0]
    joker_count = len(hand) - len(hand_without_jokers)
    sorted_card_counts = sol1.get_sorted_card_counts(hand_without_jokers)
    if len(sorted_card_counts) == 0:
        sorted_card_counts = [0]
    sorted_card_counts[0] += joker_count
    return sol1.convert_sorted_card_counts_to_hand_type(sorted_card_counts)


def solution(input: list[str]):
    games = sorted(sol1.parse_games(input, 'J23456789TQKA', get_type_of_hand))
    return sum((i + 1) * g.bid for i, g in enumerate(games))


if __name__ == '__main__':
    helpers.run_solution(solution)
