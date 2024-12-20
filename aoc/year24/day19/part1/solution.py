import collections
import dataclasses

from aoc import helpers


@dataclasses.dataclass
class Input:
    availables: list[str]
    targets: list[str]


def parse_input(lines: list[str]):
    return Input(
        availables=[word.strip() for word in lines[0].split(',')],
        targets=[line.strip() for line in lines[2:]],
    )


def make_prefix_map(input: Input):
    prefix_map = collections.defaultdict[str, set[str]](set)
    for word in input.availables:
        prefix_map[word[0]].add(word)
    return prefix_map


def try_make_word(word: str, prefix_map: dict[str, set[str]], cache: dict[str, int]) -> int:
    if word in cache:
        return cache[word]

    if len(word) == 0:
        return 1

    results = 0
    for candidate in prefix_map[word[0]]:
        if word.startswith(candidate):
            results += try_make_word(word.removeprefix(candidate), prefix_map, cache)

    cache[word] = results
    return results


def solution(lines: list[str]):
    input = parse_input(lines)
    prefix_map = make_prefix_map(input)
    cache = dict[str, int]()
    return sum(try_make_word(word, prefix_map, cache) > 0 for word in input.targets)


if __name__ == '__main__':
    helpers.run_solution(solution)
