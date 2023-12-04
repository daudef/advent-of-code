from aoc import helpers
from aoc.year23.day04.part1 import solution as part1


def common_in_card(card: part1.Card):
    return len(set(card.numbers1).intersection(card.numbers2))


def score_of_card(card: part1.Card):
    size_common = common_in_card(card)
    if size_common == 0:
        return 0
    return 2 ** (size_common - 1)


def solution(input: list[str]):
    cards = [part1.parse_card(line) for line in input]
    card_id_count = {card.id: 1 for card in cards}

    for card in cards:
        count = card_id_count[card.id]
        common = common_in_card(card)
        for id in range(card.id + 1, card.id + 1 + common):
            if id in card_id_count:
                card_id_count[id] += count

    return sum(card_id_count.values())


if __name__ == '__main__':
    helpers.run_solution(solution)
