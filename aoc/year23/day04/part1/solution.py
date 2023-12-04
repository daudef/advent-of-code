import dataclasses
from aoc import helpers


@dataclasses.dataclass
class Card:
    id: int
    numbers1: list[int]
    numbers2: list[int]


def parse_card(s: str):
    name, _, numbers = s.partition(':')
    n1s, _, n2s = numbers.partition('|')
    return Card(
        id=int(name.lower().removeprefix('card')),
        numbers1=[int(n) for n in n1s.split()],
        numbers2=[int(n) for n in n2s.split()],
    )


def score_of_card(line: str):
    card = parse_card(line)
    size_common = len(set(card.numbers1).intersection(card.numbers2))
    if size_common == 0:
        return 0
    return 2 ** (size_common - 1)


def solution(input: list[str]):
    return sum(score_of_card(line) for line in input)


if __name__ == '__main__':
    helpers.run_solution(solution)
